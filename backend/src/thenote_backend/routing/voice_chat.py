"""
Voice Chat Endpoints
Real-time conversational interface
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

from ..services.voice_conversation import get_voice_conversation

router = APIRouter(prefix="/voice", tags=["voice-chat"])


class VoiceChatRequest(BaseModel):
    """Voice chat request"""
    session_id: str = Field(..., description="Session ID")
    transcript: str = Field(..., description="Transcribed user speech")
    audio_features: Optional[List[float]] = Field(None, description="Optional audio features")


class VoiceChatResponse(BaseModel):
    """Voice chat response"""
    response: str = Field(..., description="AI response text")
    intent: str = Field(..., description="Detected user intent")
    consciousness: dict = Field(default_factory=dict, description="Consciousness analysis data")
    session_id: str = Field(..., description="Session ID")


@router.post("/chat", response_model=VoiceChatResponse)
async def voice_chat(request: VoiceChatRequest) -> VoiceChatResponse:
    """
    Process voice input and generate conversational response

    The Note listens to your speech, understands intent, and responds
    intelligently using the consciousness network.

    Supports intents:
    - Generate lyrics/melodies/rhythms
    - Analyze audio in real-time
    - Modify creations
    - General conversation
    """
    conversation = get_voice_conversation()

    # Convert audio features if provided
    import numpy as np
    audio_features_np = None
    if request.audio_features:
        audio_features_np = np.array(request.audio_features, dtype=np.float32)

    # Process input
    result = await conversation.process_voice_input(
        transcript=request.transcript,
        audio_features=audio_features_np,
        session_id=request.session_id
    )

    return VoiceChatResponse(**result)


@router.post("/clear/{session_id}")
async def clear_conversation(session_id: str):
    """Clear conversation history for a session"""
    conversation = get_voice_conversation()
    conversation.clear_history()
    return {"status": "cleared", "session_id": session_id}


@router.get("/help")
async def get_help():
    """Get voice chat help information"""
    return {
        "capabilities": [
            "Generate lyrics with consciousness-powered creativity",
            "Create melodies exploring 5 parallel timelines",
            "Generate rhythms from timeline valences",
            "Analyze audio through 14-state energy fields",
            "Real-time conversational music creation",
            "Hands-free operation while making music"
        ],
        "example_commands": [
            "Create uplifting lyrics about cosmic awakening",
            "Generate a melody in C major",
            "Analyze what I'm playing",
            "Make a rhythm pattern",
            "Change the mood to somber",
            "Help me with lyrics"
        ]
    }
