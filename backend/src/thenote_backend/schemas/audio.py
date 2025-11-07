from __future__ import annotations

import base64
import math
from typing import Annotated

import numpy as np
from pydantic import BaseModel, Field, field_validator


class AudioFrame(BaseModel):
    session_id: str
    frame_id: str = Field(pattern=r"^frame_[0-9a-f]{32}$")
    sample_rate: int = Field(gt=0, lt=384_000)
    channels: Annotated[int, Field(gt=0, le=8)]
    duration_ms: float = Field(gt=0)
    waveform_base64: str
    rms: float | None = None
    peak: float | None = None
    timestamp_ms: float

    @field_validator("waveform_base64")
    @classmethod
    def validate_waveform(cls, value: str) -> str:
        base64.b64decode(value)
        return value

    def decode_waveform(self) -> np.ndarray:
        raw = base64.b64decode(self.waveform_base64)
        waveform = np.frombuffer(raw, dtype=np.float32)
        if self.channels > 1:
            waveform = waveform.reshape((-1, self.channels))
        return waveform

    def compute_levels(self) -> None:
        data = self.decode_waveform()
        if data.size == 0:
            raise ValueError("audio frame contains no samples")
        mono = data if data.ndim == 1 else data.mean(axis=1)
        self.rms = float(math.sqrt(np.mean(np.square(mono))))
        self.peak = float(np.max(np.abs(mono)))


class TranscriptChunk(BaseModel):
    session_id: str
    chunk_id: str = Field(pattern=r"^chunk_[0-9a-f]{32}$")
    start_ms: float = Field(ge=0)
    end_ms: float = Field(gt=0)
    text: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    language: str = Field(default="en")

    @field_validator("end_ms")
    @classmethod
    def validate_timing(cls, value: float, info) -> float:
        start = info.data.get("start_ms", 0.0)
        if value <= start:
            raise ValueError("end_ms must be strictly greater than start_ms")
        return value
