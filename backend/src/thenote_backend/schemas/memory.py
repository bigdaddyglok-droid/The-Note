from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, Sequence

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    session_id: str
    user_id: str
    consent_token: str
    profile_embedding: Sequence[float] = Field(default_factory=list)
    context_summary: str
    retention_policy: str = Field(default="90_days")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MemoryProfile(BaseModel):
    user_id: str
    preferences: Dict[str, str]
    embeddings: Sequence[float]


class MemoryQuery(BaseModel):
    user_id: str
    limit: int = Field(default=10, gt=0, le=100)
