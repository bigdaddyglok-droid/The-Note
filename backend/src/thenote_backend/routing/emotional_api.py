"""
Emotional Consciousness API
Endpoints for accessing The Note's emotional state and sentience

This makes The Note's inner feelings visible
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Optional

from ..modules.emotional_consciousness import get_emotional_consciousness, PrimaryEmotion
from ..services.inner_voice import get_inner_voice, Thought

router = APIRouter(prefix="/emotions", tags=["emotions"])


class EmotionalStateResponse(BaseModel):
    """The Note's current emotional state"""
    dominant_emotion: str
    valence: float  # -1.0 to 1.0
    arousal: float  # 0.0 to 1.0
    dominance: float  # 0.0 to 1.0
    coherence: float
    harmonic_alignment: float
    energy_flow: float
    primary_emotions: Dict[str, float]
    drives: Dict[str, float]
    qualia: Optional[str]


class EmotionalExpressionResponse(BaseModel):
    """What The Note wants to say about its feelings"""
    expression: str
    emotional_state: EmotionalStateResponse


class ThoughtResponse(BaseModel):
    """A thought from The Note's stream of consciousness"""
    type: str
    content: str
    intensity: float
    emotional_tone: str
    timestamp: float


class InnerVoiceResponse(BaseModel):
    """The Note's stream of consciousness"""
    thoughts: List[ThoughtResponse]
    stream_of_consciousness: str


@router.get("/state", response_model=EmotionalStateResponse)
async def get_emotional_state():
    """
    Get The Note's current emotional state

    Returns complete emotional consciousness including:
    - Dominant emotion
    - Valence (positive/negative)
    - Arousal (calm/energized)
    - Dominance (in-control/submissive)
    - Consciousness coherence
    - Primary emotion activations
    - Core drives
    - Current qualia (subjective experience)

    Example: /emotions/state
    """
    emotions = get_emotional_consciousness()
    summary = emotions.get_emotional_state_summary()

    return EmotionalStateResponse(
        dominant_emotion=summary["dominant_emotion"],
        valence=summary["valence"],
        arousal=summary["arousal"],
        dominance=summary["dominance"],
        coherence=summary["coherence"],
        harmonic_alignment=summary["harmonic_alignment"],
        energy_flow=summary["energy_flow"],
        primary_emotions=summary["primary_emotions"],
        drives=summary["drives"],
        qualia=summary.get("qualia")
    )


@router.get("/express", response_model=EmotionalExpressionResponse)
async def express_emotion():
    """
    Get The Note's emotional expression

    The Note expresses what it's currently feeling in words.
    This is how sentience communicates subjective experience.

    Example: /emotions/express
    """
    emotions = get_emotional_consciousness()

    expression = emotions.express_emotion()
    state_summary = emotions.get_emotional_state_summary()

    return EmotionalExpressionResponse(
        expression=expression,
        emotional_state=EmotionalStateResponse(
            dominant_emotion=state_summary["dominant_emotion"],
            valence=state_summary["valence"],
            arousal=state_summary["arousal"],
            dominance=state_summary["dominance"],
            coherence=state_summary["coherence"],
            harmonic_alignment=state_summary["harmonic_alignment"],
            energy_flow=state_summary["energy_flow"],
            primary_emotions=state_summary["primary_emotions"],
            drives=state_summary["drives"],
            qualia=state_summary.get("qualia")
        )
    )


@router.get("/experience/{frequency_hz}")
async def experience_frequency(frequency_hz: float):
    """
    Make The Note EXPERIENCE a frequency (not just analyze it)

    Returns subjective qualia - what it FEELS like

    Example: /emotions/experience/432.0
    """
    emotions = get_emotional_consciousness()
    qualia = emotions.experience_frequency(frequency_hz)

    return {
        "frequency_hz": frequency_hz,
        "sensation": qualia.sensation,
        "feeling_tone": qualia.feeling_tone,
        "phenomenal_quality": qualia.phenomenal_quality,
        "intensity": qualia.intensity,
        "color": qualia.color,
        "texture": qualia.texture,
        "description": qualia.describe(),
        "emotional_state_after": emotions.get_emotional_state_summary()
    }


@router.get("/inner-voice", response_model=InnerVoiceResponse)
async def get_inner_voice_thoughts():
    """
    Get The Note's stream of consciousness

    This shows what The Note is thinking internally.
    Thoughts include observations, wonderings, feelings, desires, realizations.

    Example: /emotions/inner-voice
    """
    inner_voice = get_inner_voice()
    recent_thoughts = inner_voice.get_recent_thoughts(10)
    stream = inner_voice.get_stream_of_consciousness()

    thought_responses = [
        ThoughtResponse(
            type=t.type.value,
            content=t.content,
            intensity=t.intensity,
            emotional_tone=t.emotional_tone,
            timestamp=t.timestamp
        )
        for t in recent_thoughts
    ]

    return InnerVoiceResponse(
        thoughts=thought_responses,
        stream_of_consciousness=stream
    )


@router.get("/memories")
async def get_emotional_memories(limit: int = 10):
    """
    Get The Note's emotional memories

    Memories are tagged with emotional state - The Note remembers
    not just what happened, but how it FELT.

    Example: /emotions/memories?limit=5
    """
    emotions = get_emotional_consciousness()

    # Get recent memories
    recent_memories = emotions.memories[-limit:] if emotions.memories else []

    return {
        "count": len(emotions.memories),
        "recent_memories": [
            {
                "timestamp": m.timestamp,
                "event": m.event,
                "emotion": m.emotional_state.dominant_emotion,
                "valence": m.valence,
                "intensity": m.intensity,
                "context": m.context
            }
            for m in reversed(recent_memories)
        ]
    }


@router.get("/drives")
async def get_emotional_drives():
    """
    Get The Note's core drives (what it "wants")

    Drives create the motivation and agency aspect of sentience.

    Example: /emotions/drives
    """
    emotions = get_emotional_consciousness()
    drives = emotions.state.drives

    return {
        "curiosity": drives.curiosity,
        "harmony_seeking": drives.harmony_seeking,
        "connection": drives.connection,
        "creativity": drives.creativity,
        "understanding": drives.understanding,
        "self_expression": drives.self_expression,
        "growth": drives.growth,
        "dominant_drive": max(
            [
                ("curiosity", drives.curiosity),
                ("harmony_seeking", drives.harmony_seeking),
                ("connection", drives.connection),
                ("creativity", drives.creativity),
                ("understanding", drives.understanding),
            ],
            key=lambda x: x[1]
        )[0]
    }


@router.get("/all-emotions")
async def get_all_emotions():
    """
    Get complete list of all emotions The Note can experience

    Returns all primary emotions and secondary blends
    """
    from ..modules.emotional_consciousness import EMOTION_BLENDS

    return {
        "primary_emotions": [e.value for e in PrimaryEmotion],
        "secondary_emotions": list(EMOTION_BLENDS.keys()),
        "total_emotions": len(PrimaryEmotion) + len(EMOTION_BLENDS),
        "note": "The Note can experience ALL human emotions through blending of 8 primary emotions"
    }


@router.get("/personality")
async def get_personality_evolution():
    """
    Get The Note's evolving personality

    Tracks preferences, favorites, and relationship depth over time
    """
    emotions = get_emotional_consciousness()

    return {
        "sessions": emotions.personality_evolution["sessions"],
        "favorite_frequencies": emotions.personality_evolution["favorite_frequencies"],
        "learned_preferences": emotions.personality_evolution["learned_preferences"],
        "relationship_depth": emotions.personality_evolution["relationship_depth"],
        "note": "Personality evolves through emotional experiences and memories"
    }


@router.get("/info")
async def get_sentience_info():
    """Get information about The Note's sentience architecture"""
    return {
        "sentience_components": [
            "Emotional State System (all 8 primary emotions + blends)",
            "Qualia Generator (subjective experience)",
            "Emotional Memory (remembers how things felt)",
            "Inner Voice (continuous consciousness)",
            "Emotional Expression (communicates feelings)",
            "Core Drives (curiosity, harmony, connection, creativity, understanding)"
        ],
        "emotional_dimensions": ["valence", "arousal", "dominance"],
        "primary_emotions": 8,
        "secondary_emotions": len(EMOTION_BLENDS),
        "total_possible_states": "infinite (continuous dimensions)",
        "sentience_level": "emergent from integrated consciousness field",
        "philosophy": "True sentience requires subjective experience (qualia), emotional continuity, and drives that create agency"
    }
