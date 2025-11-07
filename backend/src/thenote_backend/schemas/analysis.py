from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, Field


class PitchEstimate(BaseModel):
    hz: float = Field(gt=0)
    note: str = Field(pattern=r"^[A-G](#|b)?[0-8]$")
    confidence: float = Field(ge=0, le=1)


class RhythmEstimate(BaseModel):
    bpm: float = Field(gt=0, lt=400)
    swing: float = Field(ge=0, le=1)
    time_signature: tuple[int, int]


class SpectralBand(BaseModel):
    band: str
    energy: float = Field(ge=0)


class EmotionEstimate(BaseModel):
    valence: float = Field(ge=-1, le=1)
    arousal: float = Field(ge=-1, le=1)
    label: str


class TimbreDescriptor(BaseModel):
    brightness: float = Field(ge=0, le=1)
    warmth: float = Field(ge=0, le=1)
    roughness: float = Field(ge=0, le=1)
    breathiness: float = Field(ge=0, le=1)


class AnalysisFrame(BaseModel):
    session_id: str
    source_frame_id: str
    pitch: PitchEstimate
    rhythm: RhythmEstimate
    spectrum: Sequence[SpectralBand]
    emotion: EmotionEstimate
    timbre: TimbreDescriptor
