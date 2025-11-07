import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from thenote_backend.modules.memory import AdaptiveMemory
from thenote_backend.schemas import MemoryQuery, MemoryRecord


@pytest.mark.asyncio
async def test_memory_retention(monkeypatch, tmp_path):
    monkeypatch.setenv("THE_NOTE_DATA_DIR", str(tmp_path))
    memory = AdaptiveMemory()
    user_id = "artist_42"
    old_timestamp = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    recent_timestamp = datetime.now(timezone.utc).isoformat()

    old_record = MemoryRecord(
        session_id="sess_old",
        user_id=user_id,
        consent_token="consent_old",
        profile_embedding=[0.1, 0.2, 0.3],
        context_summary="Old snapshot",
        retention_policy="30_days",
        created_at=old_timestamp,
    )
    await memory.upsert(old_record)

    new_record = MemoryRecord(
        session_id="sess_new",
        user_id=user_id,
        consent_token="consent_new",
        profile_embedding=[0.5, 0.5, 0.5],
        context_summary="Current snapshot",
        retention_policy="30_days",
        created_at=recent_timestamp,
    )
    await memory.upsert(new_record)

    records = await memory.list_recent(MemoryQuery(user_id=user_id, limit=10))
    assert len(records) == 1
    assert records[0].session_id == "sess_new"

    profile = await memory.fetch_profile(MemoryQuery(user_id=user_id, limit=5))
    assert profile is not None
    assert profile.user_id == user_id
    assert profile.preferences["retention_policy"] == "30_days"
    assert profile.embeddings == [0.5, 0.5, 0.5]
