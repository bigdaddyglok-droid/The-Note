"""
Knowledge Base API
Endpoints for accessing The Note's deep musical knowledge
Latin etymology, frequency science, water dynamics, psychology
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List

from ..modules.knowledge_base import get_knowledge_base

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class EtymologyResponse(BaseModel):
    """Etymology explanation response"""
    word: str
    explanation: Optional[str]


class FrequencyResponse(BaseModel):
    """Frequency science response"""
    frequency_hz: float
    explanation: str
    water_dynamics: str


class BrainwaveResponse(BaseModel):
    """Brainwave entrainment response"""
    tempo_bpm: float
    brainwave_state: str
    state_description: str
    explanation: str


class EmotionResponse(BaseModel):
    """Emotion mapping response"""
    emotion: str
    explanation: str


class VocabularyResponse(BaseModel):
    """Vocabulary suggestion response"""
    theme: str
    words: List[str]


class ComprehensiveResponse(BaseModel):
    """Comprehensive scientific explanation"""
    frequency_hz: float
    tempo_bpm: float
    emotion: str
    explanation: str


@router.get("/etymology", response_model=EtymologyResponse)
async def get_etymology(
    word: str = Query(..., description="Word to explain etymology for")
) -> EtymologyResponse:
    """
    Get etymology explanation for a word

    The Note will explain Latin roots and meaning

    Example: /knowledge/etymology?word=resonance
    """
    kb = get_knowledge_base()
    explanation = kb.get_etymology(word)

    return EtymologyResponse(
        word=word,
        explanation=explanation
    )


@router.get("/vocabulary", response_model=VocabularyResponse)
async def suggest_vocabulary(
    theme: str = Query("sound", description="Theme for vocabulary (sound, light, water, emotion, time, space)"),
    level: str = Query("advanced", description="Vocabulary level")
) -> VocabularyResponse:
    """
    Get advanced vocabulary suggestions for lyric writing

    Themes:
    - sound: Musical and auditory words
    - light: Luminous and radiant words
    - water: Fluid and flowing words
    - emotion: Feeling and sentiment words
    - time: Temporal and eternal words
    - space: Cosmic and ethereal words

    Example: /knowledge/vocabulary?theme=water&level=advanced
    """
    kb = get_knowledge_base()
    words = kb.suggest_vocabulary(theme, level)

    return VocabularyResponse(
        theme=theme,
        words=words
    )


@router.get("/frequency", response_model=FrequencyResponse)
async def explain_frequency(
    frequency_hz: float = Query(..., description="Frequency in Hz to explain")
) -> FrequencyResponse:
    """
    Explain the science and effects of a frequency

    Includes:
    - Chakra resonance
    - Emotional effects
    - Healing properties
    - Brainwave state correlation
    - Water cymatics patterns

    Example: /knowledge/frequency?frequency_hz=432.0
    """
    kb = get_knowledge_base()
    freq_explanation = kb.explain_frequency(frequency_hz)
    water_explanation = kb.explain_water_resonance(frequency_hz)

    return FrequencyResponse(
        frequency_hz=frequency_hz,
        explanation=freq_explanation,
        water_dynamics=water_explanation
    )


@router.get("/brainwave", response_model=BrainwaveResponse)
async def explain_brainwave(
    tempo_bpm: float = Query(..., description="Musical tempo in BPM")
) -> BrainwaveResponse:
    """
    Explain how tempo affects brainwave entrainment

    Brainwave states:
    - Delta (40-60 BPM): Deep sleep, healing
    - Theta (60-75 BPM): Meditation, creativity
    - Alpha (75-90 BPM): Relaxed flow state
    - Beta (90-140 BPM): Active thinking
    - Gamma (140-180 BPM): Peak performance

    Example: /knowledge/brainwave?tempo_bpm=120
    """
    kb = get_knowledge_base()
    state, description = kb.map_tempo_to_brainwave(tempo_bpm)
    explanation = kb.explain_brainwave_entrainment(tempo_bpm)

    return BrainwaveResponse(
        tempo_bpm=tempo_bpm,
        brainwave_state=state,
        state_description=description,
        explanation=explanation
    )


@router.get("/emotion", response_model=EmotionResponse)
async def explain_emotion(
    emotion: str = Query(..., description="Emotion to explain (joy, sadness, peace, excitement)")
) -> EmotionResponse:
    """
    Explain the science of how music creates emotion

    Includes:
    - Recommended frequencies
    - Chord progressions
    - Tempo ranges
    - Rhythm patterns
    - Cognitive effects
    - Color associations

    Example: /knowledge/emotion?emotion=joy
    """
    kb = get_knowledge_base()
    explanation = kb.explain_emotion_mapping(emotion)

    return EmotionResponse(
        emotion=emotion,
        explanation=explanation
    )


@router.get("/comprehensive", response_model=ComprehensiveResponse)
async def comprehensive_explanation(
    frequency_hz: float = Query(432.0, description="Frequency in Hz"),
    tempo_bpm: float = Query(120.0, description="Tempo in BPM"),
    emotion: str = Query("peace", description="Target emotion")
) -> ComprehensiveResponse:
    """
    Get comprehensive scientific explanation of all parameters

    Combines:
    - Frequency science
    - Brainwave entrainment
    - Water dynamics
    - Emotion-cognition mapping

    Example: /knowledge/comprehensive?frequency_hz=528&tempo_bpm=90&emotion=joy
    """
    kb = get_knowledge_base()
    explanation = kb.generate_comprehensive_explanation(
        frequency=frequency_hz,
        tempo=tempo_bpm,
        emotion=emotion
    )

    return ComprehensiveResponse(
        frequency_hz=frequency_hz,
        tempo_bpm=tempo_bpm,
        emotion=emotion,
        explanation=explanation
    )


@router.get("/info")
async def get_knowledge_info():
    """Get information about The Note's knowledge base"""
    return {
        "knowledge_domains": [
            "Latin Etymology & Vocabulary",
            "Frequency Science & Solfeggio Frequencies",
            "Water Dynamics & Cymatics",
            "Brainwave Entrainment",
            "Affective Psychology & Emotion Mapping"
        ],
        "solfeggio_frequencies": [174, 285, 396, 417, 432, 528, 639, 741, 852, 963],
        "brainwave_states": ["Delta", "Theta", "Alpha", "Beta", "Gamma"],
        "emotions": ["joy", "sadness", "peace", "excitement"],
        "vocabulary_themes": ["sound", "light", "water", "emotion", "time", "space"],
        "latin_roots": ["son", "vox", "cant", "phon", "cord", "spir", "anim", "lum", "flect", "vibr"]
    }
