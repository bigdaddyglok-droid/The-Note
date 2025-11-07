from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RenderInstruction(BaseModel):
    session_id: str
    render_id: str = Field(pattern=r"^render_[0-9a-f]{32}$")
    text: str
    melody: list[float] | None = None
    voice_profile: str = Field(default="luminous_alto")
    dynamics: str = Field(default="mezzo-forte")
    format: str = Field(default="wav")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RenderedAudio(BaseModel):
    session_id: str
    render_id: str
    url_or_blob: str
    duration_ms: float
    loudness: float
    checksum: str
