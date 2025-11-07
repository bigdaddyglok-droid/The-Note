"""
Musical Knowledge Base
Latin roots, etymology, frequency science, water dynamics, psychology
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LatinRoot:
    """Latin root with etymology"""
    root: str
    meaning: str
    examples: List[str]


@dataclass
class FrequencyKnowledge:
    """Knowledge about a specific frequency"""
    frequency_hz: float
    note: str
    chakra: Optional[str]
    emotion: str
    brainwave_state: Optional[str]
    healing_properties: List[str]
    psychological_effect: str


@dataclass
class WaterPattern:
    """Cymatics pattern in water"""
    frequency_hz: float
    pattern_type: str
    geometry: str
    description: str


class MusicalKnowledgeBase:
    """
    Deep knowledge system for music, language, science, and psychology
    The Note's intelligence for explaining WHY things work
    """

    def __init__(self):
        self._latin_roots = self._initialize_latin_roots()
        self._frequency_knowledge = self._initialize_frequency_knowledge()
        self._water_patterns = self._initialize_water_patterns()
        self._brainwave_states = self._initialize_brainwave_states()
        self._emotion_mappings = self._initialize_emotion_mappings()

    # ==================== LATIN ROOTS & ETYMOLOGY ====================

    def _initialize_latin_roots(self) -> Dict[str, LatinRoot]:
        """Initialize Latin root knowledge base"""
        return {
            "son": LatinRoot(
                root="son",
                meaning="sound",
                examples=["sonnet", "resonance", "sonic", "dissonance", "unison"]
            ),
            "vox": LatinRoot(
                root="vox",
                meaning="voice",
                examples=["vocal", "vocalize", "vocation", "advocate", "invoke"]
            ),
            "cant": LatinRoot(
                root="cant",
                meaning="to sing",
                examples=["cantata", "incantation", "chant", "recant", "descant"]
            ),
            "phon": LatinRoot(
                root="phon",
                meaning="sound, voice",
                examples=["phoneme", "symphony", "telephone", "cacophony", "euphony"]
            ),
            "cord": LatinRoot(
                root="cord",
                meaning="heart",
                examples=["accord", "discord", "chord", "cordial", "record"]
            ),
            "spir": LatinRoot(
                root="spir",
                meaning="breathe",
                examples=["inspire", "expire", "aspire", "respire", "spirit"]
            ),
            "anim": LatinRoot(
                root="anim",
                meaning="life, soul",
                examples=["animate", "unanimous", "magnanimous", "inanimate"]
            ),
            "lum": LatinRoot(
                root="lum",
                meaning="light",
                examples=["luminous", "illuminate", "luminary", "luminescence"]
            ),
            "flect": LatinRoot(
                root="flect",
                meaning="bend, curve",
                examples=["reflect", "inflection", "deflect", "circumflex"]
            ),
            "vibr": LatinRoot(
                root="vibr",
                meaning="shake, move",
                examples=["vibration", "vibrate", "vibrant", "vibrancy"]
            ),
        }

    def get_etymology(self, word: str) -> Optional[str]:
        """Get etymology explanation for a word"""
        word_lower = word.lower()

        for root_key, root_data in self._latin_roots.items():
            if root_key in word_lower:
                return (
                    f"'{word}' contains the root '{root_data.root}' meaning '{root_data.meaning}'. "
                    f"Related words: {', '.join(root_data.examples[:3])}"
                )

        return None

    def suggest_vocabulary(self, theme: str, level: str = "advanced") -> List[str]:
        """Suggest advanced vocabulary for lyrics"""
        vocabulary_bank = {
            "light": ["luminescent", "effulgent", "phosphorescent", "incandescent", "radiant"],
            "sound": ["resonant", "sonorous", "euphonic", "cacophonous", "harmonious"],
            "water": ["undulate", "cascade", "ripple", "confluence", "ebb"],
            "emotion": ["ineffable", "sublime", "transcendent", "ephemeral", "melancholic"],
            "time": ["ephemeral", "perpetual", "transient", "immutable", "temporal"],
            "space": ["ethereal", "celestial", "astral", "cosmic", "void"],
        }

        return vocabulary_bank.get(theme.lower(), ["resonant", "luminous", "ethereal"])

    # ==================== FREQUENCY SCIENCE ====================

    def _initialize_frequency_knowledge(self) -> Dict[float, FrequencyKnowledge]:
        """Initialize frequency science knowledge"""
        return {
            432.0: FrequencyKnowledge(
                frequency_hz=432.0,
                note="A4",
                chakra="Heart",
                emotion="Peace, harmony",
                brainwave_state="Alpha (relaxed awareness)",
                healing_properties=[
                    "Reduces stress and anxiety",
                    "Promotes emotional balance",
                    "Enhances meditation",
                    "Synchronizes with nature (8 Hz Schumann resonance)"
                ],
                psychological_effect="Creates sense of wholeness and alignment with universal frequency"
            ),
            528.0: FrequencyKnowledge(
                frequency_hz=528.0,
                note="C5",
                chakra="Solar Plexus/Heart",
                emotion="Love, transformation",
                brainwave_state="Alpha/Theta",
                healing_properties=[
                    "DNA repair (Solfeggio frequency)",
                    "Promotes love and miracles",
                    "Enhances creativity",
                    "Cellular regeneration"
                ],
                psychological_effect="Awakens intuition, activates imagination, generates positive energy"
            ),
            639.0: FrequencyKnowledge(
                frequency_hz=639.0,
                note="D#5",
                chakra="Heart",
                emotion="Connection, relationships",
                brainwave_state="Alpha",
                healing_properties=[
                    "Enhances communication",
                    "Promotes understanding",
                    "Balances relationships",
                    "Opens heart chakra"
                ],
                psychological_effect="Fosters empathy, tolerance, and harmonious relationships"
            ),
            741.0: FrequencyKnowledge(
                frequency_hz=741.0,
                note="F#5",
                chakra="Throat",
                emotion="Expression, intuition",
                brainwave_state="Beta",
                healing_properties=[
                    "Awakens intuition",
                    "Clears toxins",
                    "Enhances self-expression",
                    "Problem-solving clarity"
                ],
                psychological_effect="Activates third eye, enhances spiritual awareness"
            ),
            174.0: FrequencyKnowledge(
                frequency_hz=174.0,
                note="F3",
                chakra="Root",
                emotion="Safety, grounding",
                brainwave_state="Delta",
                healing_properties=[
                    "Pain relief",
                    "Physical grounding",
                    "Security and stability",
                    "Reduces physical pain"
                ],
                psychological_effect="Provides foundation, reduces anxiety, promotes feeling of safety"
            ),
        }

    def explain_frequency(self, frequency_hz: float) -> str:
        """Explain the science and effects of a frequency"""
        # Find closest known frequency
        closest_freq = min(self._frequency_knowledge.keys(),
                          key=lambda x: abs(x - frequency_hz))

        if abs(closest_freq - frequency_hz) < 10:  # Within 10 Hz
            knowledge = self._frequency_knowledge[closest_freq]
            explanation = (
                f"{frequency_hz:.1f} Hz ({knowledge.note}) resonates with the {knowledge.chakra} chakra. "
                f"This frequency evokes {knowledge.emotion}. "
                f"Psychologically, it {knowledge.psychological_effect.lower()}. "
                f"Healing properties: {', '.join(knowledge.healing_properties[:2])}."
            )
            return explanation

        # General frequency range explanation
        if frequency_hz < 100:
            return f"{frequency_hz:.1f} Hz is in the sub-bass range - felt more than heard, creates deep physical resonance."
        elif frequency_hz < 250:
            return f"{frequency_hz:.1f} Hz is in the bass range - provides foundation, grounding, physical presence."
        elif frequency_hz < 2000:
            return f"{frequency_hz:.1f} Hz is in the midrange - carries harmonic richness, vocal clarity."
        elif frequency_hz < 8000:
            return f"{frequency_hz:.1f} Hz is in the high midrange - adds brilliance, presence, definition."
        else:
            return f"{frequency_hz:.1f} Hz is in the treble range - provides air, sparkle, spatial dimension."

    # ==================== WATER DYNAMICS & CYMATICS ====================

    def _initialize_water_patterns(self) -> Dict[float, WaterPattern]:
        """Initialize cymatics and water science knowledge"""
        return {
            432.0: WaterPattern(
                frequency_hz=432.0,
                pattern_type="Sacred geometry",
                geometry="Hexagonal/Flower of Life",
                description="Creates harmonious geometric patterns in water, resembling flower petals or snowflakes"
            ),
            528.0: WaterPattern(
                frequency_hz=528.0,
                pattern_type="DNA helix",
                geometry="Spiral/Helix",
                description="Forms spiral patterns that mirror DNA double helix structure"
            ),
            40.0: WaterPattern(
                frequency_hz=40.0,
                pattern_type="Concentric circles",
                geometry="Circular ripples",
                description="Creates perfect concentric circular patterns, like dropping stone in still water"
            ),
        }

    def explain_water_resonance(self, frequency_hz: float) -> str:
        """Explain how frequency affects water structure"""
        # Check for known cymatics pattern
        if frequency_hz in self._water_patterns:
            pattern = self._water_patterns[frequency_hz]
            return (
                f"At {frequency_hz} Hz, water molecules form {pattern.pattern_type} patterns. "
                f"The geometric structure is {pattern.geometry}. {pattern.description}. "
                f"Since the human body is 60-70% water, this frequency directly restructures our cellular water."
            )

        # General water science
        return (
            f"Sound at {frequency_hz} Hz creates standing wave patterns in water through cymatics. "
            f"These vibrations reorganize water molecule clusters, affecting cellular hydration and "
            f"information transfer in biological systems. Every frequency leaves its geometric signature."
        )

    # ==================== BRAINWAVE PSYCHOLOGY ====================

    def _initialize_brainwave_states(self) -> Dict[str, Dict]:
        """Initialize brainwave state knowledge"""
        return {
            "Delta": {
                "range": (0.5, 4.0),
                "state": "Deep sleep, healing, regeneration",
                "musical_tempo": (40, 60),
                "characteristics": "Unconscious, restorative, dreamless sleep",
                "instruments": ["Deep bass", "Tibetan bowls", "Gongs"],
            },
            "Theta": {
                "range": (4.0, 8.0),
                "state": "Meditation, creativity, intuition",
                "musical_tempo": (60, 75),
                "characteristics": "Subconscious access, vivid imagery, deep meditation",
                "instruments": ["Soft pads", "Ocean sounds", "Ambient drones"],
            },
            "Alpha": {
                "range": (8.0, 14.0),
                "state": "Relaxed awareness, flow state",
                "musical_tempo": (75, 90),
                "characteristics": "Calm focus, present moment, creative flow",
                "instruments": ["Acoustic guitar", "Soft piano", "Nature sounds"],
            },
            "Beta": {
                "range": (14.0, 30.0),
                "state": "Active thinking, concentration",
                "musical_tempo": (90, 140),
                "characteristics": "Alert, focused, problem-solving",
                "instruments": ["Rhythmic drums", "Clear vocals", "Bright synths"],
            },
            "Gamma": {
                "range": (30.0, 100.0),
                "state": "Peak performance, transcendence",
                "musical_tempo": (140, 180),
                "characteristics": "Heightened perception, unified consciousness",
                "instruments": ["Fast percussion", "High frequency harmonics", "Complex polyrhythms"],
            },
        }

    def map_tempo_to_brainwave(self, tempo_bpm: float) -> Tuple[str, str]:
        """Map musical tempo to brainwave state"""
        for state, data in self._brainwave_states.items():
            min_tempo, max_tempo = data["musical_tempo"]
            if min_tempo <= tempo_bpm <= max_tempo:
                return state, data["state"]

        return "Beta", "Active thinking"

    def explain_brainwave_entrainment(self, tempo_bpm: float) -> str:
        """Explain how tempo affects brainwaves"""
        state, description = self.map_tempo_to_brainwave(tempo_bpm)
        brainwave_data = self._brainwave_states[state]

        explanation = (
            f"At {tempo_bpm} BPM, music entrains the brain toward {state} waves "
            f"({brainwave_data['range'][0]}-{brainwave_data['range'][1]} Hz). "
            f"This induces {description}. "
            f"Characteristics: {brainwave_data['characteristics']}. "
            f"Ideal instruments: {', '.join(brainwave_data['instruments'])}."
        )

        return explanation

    # ==================== EMOTION-COGNITION MAPPING ====================

    def _initialize_emotion_mappings(self) -> Dict[str, Dict]:
        """Initialize affective psychology mappings"""
        return {
            "joy": {
                "frequencies": [528, 639],
                "chord": "Major",
                "tempo_range": (120, 140),
                "rhythm": "Syncopated, upbeat",
                "cognitive_effect": "Enhances memory, promotes creativity, releases dopamine",
                "color": "Yellow, Orange",
                "element": "Fire",
            },
            "sadness": {
                "frequencies": [396, 417],
                "chord": "Minor",
                "tempo_range": (60, 80),
                "rhythm": "Slow, flowing",
                "cognitive_effect": "Promotes introspection, emotional processing, releases oxytocin",
                "color": "Blue, Gray",
                "element": "Water",
            },
            "peace": {
                "frequencies": [432, 528],
                "chord": "Major 7th, Sus4",
                "tempo_range": (70, 90),
                "rhythm": "Steady, gentle",
                "cognitive_effect": "Reduces cortisol, activates parasympathetic nervous system",
                "color": "Green, Blue",
                "element": "Air",
            },
            "excitement": {
                "frequencies": [741, 852],
                "chord": "Major, Power chords",
                "tempo_range": (140, 180),
                "rhythm": "Fast, driving",
                "cognitive_effect": "Releases adrenaline, heightens focus, increases heart rate",
                "color": "Red, Orange",
                "element": "Fire",
            },
        }

    def explain_emotion_mapping(self, emotion: str) -> str:
        """Explain the science of how music creates emotion"""
        emotion_lower = emotion.lower()

        if emotion_lower in self._emotion_mappings:
            mapping = self._emotion_mappings[emotion_lower]
            return (
                f"To evoke {emotion}, use frequencies around {mapping['frequencies']} Hz with "
                f"{mapping['chord']} chords. Tempo should be {mapping['tempo_range'][0]}-{mapping['tempo_range'][1]} BPM "
                f"with {mapping['rhythm']} rhythm. Cognitively, this {mapping['cognitive_effect']}. "
                f"Associated with {mapping['element']} element and {mapping['color']} colors in synesthesia."
            )

        return f"Emotion '{emotion}' evokes unique cognitive and physiological responses through musical parameters."

    # ==================== INTEGRATED KNOWLEDGE QUERIES ====================

    def generate_comprehensive_explanation(
        self,
        frequency: float,
        tempo: float,
        emotion: str
    ) -> str:
        """Generate complete scientific explanation"""
        freq_explanation = self.explain_frequency(frequency)
        brainwave_explanation = self.explain_brainwave_entrainment(tempo)
        emotion_explanation = self.explain_emotion_mapping(emotion)
        water_explanation = self.explain_water_resonance(frequency)

        return (
            f"🎵 Frequency Science:\n{freq_explanation}\n\n"
            f"🧠 Brainwave Entrainment:\n{brainwave_explanation}\n\n"
            f"💧 Water Dynamics:\n{water_explanation}\n\n"
            f"❤️ Emotion-Cognition Mapping:\n{emotion_explanation}"
        )


# Global instance
_knowledge_base: Optional[MusicalKnowledgeBase] = None


def get_knowledge_base() -> MusicalKnowledgeBase:
    """Get or create global knowledge base"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = MusicalKnowledgeBase()
    return _knowledge_base
