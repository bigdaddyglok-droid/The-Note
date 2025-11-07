from __future__ import annotations

from typing import Literal, Sequence

from pydantic import BaseModel, Field


class GenerationMode(str):
    LYRIC = "lyric"
    MELODY = "melody"
    METAPHOR = "metaphor"
    STRUCTURE = "structure"


class GenerationRequest(BaseModel):
    session_id: str
    request_id: str = Field(pattern=r"^gen_[0-9a-f]{32}$")
    prompt: str = Field(min_length=1)
    modes: Sequence[Literal["lyric", "melody", "metaphor", "structure"]]
    emotional_goal: str | None = None
    tempo: float | None = Field(default=None, gt=0)
    key: str | None = Field(default=None, pattern=r"^[A-G](#|b)?m?$")


class GeneratedItem(BaseModel):
    type: Literal["lyric", "melody", "metaphor", "structure"]
    payload: dict
    confidence: float = Field(ge=0, le=1)


class GenerationBundle(BaseModel):
    session_id: str
    request_id: str
    outputs: Sequence[GeneratedItem]
