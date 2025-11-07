from __future__ import annotations

import asyncio
import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Sequence

from ..schemas import MemoryProfile, MemoryQuery, MemoryRecord
from ..services.telemetry import telemetry
from ..utils.logging import get_logger


RETENTION_WINDOWS = {
    "30_days": timedelta(days=30),
    "90_days": timedelta(days=90),
    "180_days": timedelta(days=180),
}


def _resolve_db_path() -> Path:
    base = os.getenv("THE_NOTE_DATA_DIR")
    target = Path(base) if base else Path(__file__).resolve().parents[2] / ".data"
    target.mkdir(parents=True, exist_ok=True)
    return target / "memory.sqlite3"


class AdaptiveMemory:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._logger = get_logger("module.adaptive_memory")
        self._db_path = _resolve_db_path()
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_database(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    consent_token TEXT NOT NULL,
                    profile_embedding TEXT NOT NULL,
                    context_summary TEXT NOT NULL,
                    retention_policy TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_records_user ON records(user_id)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_records_session ON records(session_id)"
            )

    def _serialize_embedding(self, embedding: Sequence[float]) -> str:
        return json.dumps(list(embedding))

    def _deserialize_embedding(self, payload: str) -> List[float]:
        return [float(value) for value in json.loads(payload)]

    def _prune_retention(
        self, conn: sqlite3.Connection, user_id: str, retention_policy: str
    ) -> None:
        if retention_policy == "session_only":
            conn.execute("DELETE FROM records WHERE user_id = ? AND retention_policy = ?", (user_id, retention_policy))
            return
        if retention_policy in RETENTION_WINDOWS:
            window = RETENTION_WINDOWS[retention_policy]
        else:
            window = RETENTION_WINDOWS["90_days"]
        threshold = (datetime.now(timezone.utc) - window).isoformat()
        conn.execute(
            "DELETE FROM records WHERE user_id = ? AND created_at < ?",
            (user_id, threshold),
        )

    async def upsert(self, record: MemoryRecord) -> None:
        async with self._lock:
            with self._connect() as conn:
                self._prune_retention(conn, record.user_id, record.retention_policy)
                conn.execute(
                    """
                    INSERT INTO records (
                        session_id,
                        user_id,
                        consent_token,
                        profile_embedding,
                        context_summary,
                        retention_policy,
                        created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.session_id,
                        record.user_id,
                        record.consent_token,
                        self._serialize_embedding(record.profile_embedding),
                        record.context_summary,
                        record.retention_policy,
                        record.created_at,
                    ),
                )
            self._logger.info(
                "memory_upserted",
                extra={
                    "extra_data": {
                        "session_id": record.session_id,
                        "user_id": record.user_id,
                        "retention": record.retention_policy,
                    }
                },
            )
            await telemetry.increment("memory.upserts")

    async def fetch_profile(self, query: MemoryQuery) -> Optional[MemoryProfile]:
        async with self._lock:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT profile_embedding, retention_policy
                    FROM records
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (query.user_id, query.limit),
                ).fetchall()
        if not rows:
            return None
        embeddings = [self._deserialize_embedding(row["profile_embedding"]) for row in rows]
        if not embeddings or not embeddings[0]:
            averaged: List[float] = []
        else:
            length = len(embeddings[0])
            sums = [0.0] * length
            for vector in embeddings:
                for idx, value in enumerate(vector):
                    sums[idx] += value
            averaged = [total / len(embeddings) for total in sums]
        preferences = {"retention_policy": rows[0]["retention_policy"]}
        return MemoryProfile(user_id=query.user_id, preferences=preferences, embeddings=averaged)

    async def list_recent(self, query: MemoryQuery) -> List[MemoryRecord]:
        async with self._lock:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT session_id, user_id, consent_token, profile_embedding, context_summary,
                           retention_policy, created_at
                    FROM records
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (query.user_id, query.limit),
                ).fetchall()
        await telemetry.increment("memory.queries")
        records: List[MemoryRecord] = []
        for row in rows:
            records.append(
                MemoryRecord(
                    session_id=row["session_id"],
                    user_id=row["user_id"],
                    consent_token=row["consent_token"],
                    profile_embedding=self._deserialize_embedding(row["profile_embedding"]),
                    context_summary=row["context_summary"],
                    retention_policy=row["retention_policy"],
                    created_at=row["created_at"],
                )
            )
        return records
