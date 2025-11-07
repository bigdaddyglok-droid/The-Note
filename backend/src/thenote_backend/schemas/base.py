from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field, computed_field
from uuid import uuid4


class IntentType(str, Enum):
    CREATIVE_SESSION = "creative_session"
    MIX_FEEDBACK = "mix_feedback"
    PERFORMANCE_COACHING = "performance_coaching"
    ANALYTICS_ONLY = "analytics_only"


class ModuleType(str, Enum):
    LIVE_AUDIO = "live_audio_input"
    SOUND_UNDERSTANDING = "sound_understanding"
    LANGUAGE_LYRIC = "language_lyric"
    IMAGINATION = "imagination"
    VOICE_SYNTH = "voice_performance"
    MEMORY = "adaptive_memory"
    CONTROLLER = "controller"


class SessionMetadata(BaseModel):
    session_id: str = Field(default_factory=lambda: f"sess_{uuid4().hex}")
    user_id: str
    intent: IntentType
    daw: str | None = None
    key: str | None = Field(default=None, pattern=r"^[A-G](#|b)?m?$")
    tempo: float | None = Field(default=None, gt=0, lt=400)
    emotional_goal: str | None = None
    references: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SessionState(BaseModel):
    metadata: SessionMetadata
    active: bool = True
    attributes: Dict[str, Any] = Field(default_factory=dict)

    def tag(self, key: str, value: Any) -> None:
        self.attributes[key] = value


class ModuleEvent(BaseModel):
    session_id: str
    source: ModuleType
    target: ModuleType | Literal["broadcast"]
    payload: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @computed_field(return_type=str)
    def label(self) -> str:
        return f"{self.source}->{self.target}:{self.session_id}"
