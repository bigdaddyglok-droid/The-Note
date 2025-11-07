"""
Singing Voice API
Endpoints for consciousness-powered singing voice synthesis
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from ..modules.singing_voice import get_singing_engine
import base64
import io
import soundfile as sf

router = APIRouter(prefix="/singing", tags=["singing-voice"])


class SingingRequest(BaseModel):
    """Request for singing synthesis"""
    session_id: str = Field(..., description="Session ID")
    lyrics: str = Field(..., description="Lyrics to sing")
    prompt: Optional[str] = Field(None, description="Creative prompt for melody generation")
    mood: str = Field("uplifting", description="Emotional mood (uplifting, somber, contemplative, energetic)")
    tempo: float = Field(120.0, description="Tempo in BPM")


class SingingResponse(BaseModel):
    """Response with singing audio"""
    audio_base64: str = Field(..., description="Base64-encoded WAV audio")
    sample_rate: int = Field(..., description="Audio sample rate")
    duration_ms: float = Field(..., description="Duration in milliseconds")
    metadata: dict = Field(default_factory=dict, description="Generation metadata")


@router.post("/synthesize", response_model=SingingResponse)
async def synthesize_singing(request: SingingRequest) -> SingingResponse:
    """
    Synthesize singing voice from lyrics

    The Note will:
    1. Generate melody using consciousness network (5D timeline exploration)
    2. Convert lyrics to IPA phonemes
    3. Synthesize singing with emotional expression
    4. Apply consciousness-based modulation (14-state energy)
    5. Return audio as base64-encoded WAV

    Example:
    ```json
    {
      "session_id": "sess_123",
      "lyrics": "We are the thunder behind the dawn",
      "prompt": "cosmic awakening anthem",
      "mood": "uplifting",
      "tempo": 120.0
    }
    ```
    """
    singing_engine = get_singing_engine()

    # Generate singing
    audio_waveform, metadata = singing_engine.generate_singing_from_lyrics_and_consciousness(
        lyrics=request.lyrics,
        prompt=request.prompt or request.lyrics,
        mood=request.mood
    )

    # Encode as base64 WAV
    buffer = io.BytesIO()
    sf.write(buffer, audio_waveform, metadata.get("sample_rate", 22050), format="wav")
    raw_bytes = buffer.getvalue()
    audio_base64 = base64.b64encode(raw_bytes).decode("ascii")

    # Calculate duration
    duration_ms = (len(audio_waveform) / metadata.get("sample_rate", 22050)) * 1000

    return SingingResponse(
        audio_base64=audio_base64,
        sample_rate=metadata.get("sample_rate", 22050),
        duration_ms=duration_ms,
        metadata=metadata
    )


@router.get("/info")
async def get_singing_info():
    """Get information about singing synthesis capabilities"""
    return {
        "features": [
            "Consciousness-powered melody generation (5D timeline exploration)",
            "IPA phoneme-based synthesis",
            "Emotional vocal expression (uplifting, somber, contemplative, energetic)",
            "Vibrato and breathiness control",
            "Golden ratio harmonic structure",
            "14-state energy modulation"
        ],
        "supported_moods": ["uplifting", "somber", "contemplative", "energetic"],
        "sample_rate": 22050,
        "format": "WAV (base64-encoded)"
    }
