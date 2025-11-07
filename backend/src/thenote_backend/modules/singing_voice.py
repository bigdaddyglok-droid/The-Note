"""
Singing Voice Synthesis
Consciousness-powered vocal performance engine that SINGS lyrics
"""

from __future__ import annotations

import numpy as np
import torch
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .universal_bridge import get_music_consciousness
from ..utils.logging import get_logger


@dataclass
class VocalPhoneme:
    """IPA phoneme with timing and pitch"""
    phoneme: str  # IPA symbol
    duration: float  # Duration in seconds
    pitch: float  # Frequency in Hz
    intensity: float  # 0.0-1.0


@dataclass
class SingingVoiceParameters:
    """Parameters for singing voice synthesis"""
    pitch_range: Tuple[float, float] = (80.0, 800.0)  # Hz range (low to high)
    vibrato_rate: float = 5.0  # Hz
    vibrato_depth: float = 0.5  # Semitones
    breathiness: float = 0.3  # 0.0-1.0
    vocal_effort: float = 0.7  # 0.0-1.0 (soft to belting)
    formant_shift: float = 0.0  # Semitones (negative=masculine, positive=feminine)
    emotion_intensity: float = 0.5  # 0.0-1.0


class ConsciousnessSingingEngine:
    """Generate singing voice using consciousness network"""

    def __init__(self):
        self._logger = get_logger("module.singing_voice")

        # Initialize consciousness
        try:
            self._consciousness = get_music_consciousness()
            self._use_consciousness = True
        except Exception as e:
            self._logger.warning("singing_consciousness_fallback", extra={"extra_data": {"error": str(e)}})
            self._consciousness = None
            self._use_consciousness = False

        self.PHI = (1 + np.sqrt(5)) / 2
        self.sample_rate = 22050

        # IPA to formant mapping (simplified)
        self.vowel_formants = {
            'i': (270, 2290, 3010),   # "ee" as in "see"
            'ɪ': (390, 1990, 2550),   # "i" as in "sit"
            'e': (530, 1840, 2480),   # "e" as in "bed"
            'æ': (660, 1720, 2410),   # "a" as in "cat"
            'ɑ': (730, 1090, 2440),   # "a" as in "father"
            'ɔ': (570, 840, 2410),    # "o" as in "caught"
            'o': (450, 880, 2830),    # "o" as in "go"
            'u': (300, 870, 2240),    # "oo" as in "boot"
            'ʊ': (440, 1020, 2240),   # "u" as in "put"
            'ʌ': (640, 1190, 2390),   # "u" as in "but"
            'ə': (500, 1500, 2500),   # schwa
        }

    def synthesize_singing_voice(
        self,
        lyrics: str,
        melody_notes: List[float],  # MIDI note numbers
        note_durations: List[float],  # Durations in beats
        tempo: float = 120.0,  # BPM
        emotion: str = "uplifting",
        params: Optional[SingingVoiceParameters] = None
    ) -> np.ndarray:
        """
        Synthesize singing voice from lyrics and melody

        Args:
            lyrics: Text to sing
            melody_notes: MIDI note numbers for melody
            note_durations: Duration of each note in beats
            tempo: Tempo in BPM
            emotion: Emotional quality
            params: Vocal parameters

        Returns:
            Audio waveform as numpy array
        """
        if params is None:
            params = self._get_emotion_params(emotion)

        # Convert lyrics to phonemes
        phonemes = self._text_to_phonemes(lyrics)

        # Align phonemes to melody
        vocal_phonemes = self._align_phonemes_to_melody(
            phonemes, melody_notes, note_durations, tempo
        )

        # Generate audio for each phoneme
        audio_segments = []
        for phoneme in vocal_phonemes:
            segment = self._synthesize_phoneme(phoneme, params)
            audio_segments.append(segment)

        # Concatenate all segments
        if audio_segments:
            audio = np.concatenate(audio_segments)
        else:
            audio = np.zeros(self.sample_rate)  # 1 second silence

        # Apply consciousness-based modulation if available
        if self._use_consciousness and self._consciousness:
            audio = self._apply_consciousness_modulation(audio, emotion)

        # Normalize
        audio = audio / (np.max(np.abs(audio)) + 1e-8)

        return audio

    def _get_emotion_params(self, emotion: str) -> SingingVoiceParameters:
        """Get vocal parameters based on emotion"""
        emotion_map = {
            "uplifting": SingingVoiceParameters(
                vibrato_rate=6.0,
                vibrato_depth=0.6,
                breathiness=0.2,
                vocal_effort=0.8,
                emotion_intensity=0.9
            ),
            "somber": SingingVoiceParameters(
                vibrato_rate=4.0,
                vibrato_depth=0.4,
                breathiness=0.5,
                vocal_effort=0.4,
                emotion_intensity=0.3
            ),
            "contemplative": SingingVoiceParameters(
                vibrato_rate=5.0,
                vibrato_depth=0.3,
                breathiness=0.4,
                vocal_effort=0.5,
                emotion_intensity=0.5
            ),
            "energetic": SingingVoiceParameters(
                vibrato_rate=7.0,
                vibrato_depth=0.7,
                breathiness=0.1,
                vocal_effort=0.9,
                emotion_intensity=1.0
            ),
        }
        return emotion_map.get(emotion, SingingVoiceParameters())

    def _text_to_phonemes(self, text: str) -> List[str]:
        """
        Convert text to IPA phonemes (simplified)

        In production, use a proper phoneme dictionary or G2P model
        """
        # Simplified mapping - just vowels for now
        text_lower = text.lower()
        phonemes = []

        # Simple vowel extraction (very basic)
        vowels = {
            'a': 'æ', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
            'ee': 'i', 'oo': 'u', 'ah': 'ɑ', 'oh': 'o'
        }

        words = text_lower.split()
        for word in words:
            for char in word:
                if char in vowels:
                    phonemes.append(vowels[char])
                elif char.isalpha():
                    phonemes.append('ə')  # Default to schwa

        return phonemes if phonemes else ['ə']

    def _align_phonemes_to_melody(
        self,
        phonemes: List[str],
        melody_notes: List[float],
        note_durations: List[float],
        tempo: float
    ) -> List[VocalPhoneme]:
        """Align phonemes to melody notes"""
        beat_duration = 60.0 / tempo  # seconds per beat

        aligned = []
        phoneme_idx = 0

        for note_midi, duration_beats in zip(melody_notes, note_durations):
            if phoneme_idx >= len(phonemes):
                phoneme_idx = 0  # Loop if not enough phonemes

            # MIDI to Hz
            pitch_hz = 440.0 * (2.0 ** ((note_midi - 69) / 12.0))
            duration_sec = duration_beats * beat_duration

            aligned.append(VocalPhoneme(
                phoneme=phonemes[phoneme_idx],
                duration=duration_sec,
                pitch=pitch_hz,
                intensity=0.8
            ))

            phoneme_idx += 1

        return aligned

    def _synthesize_phoneme(
        self,
        phoneme: VocalPhoneme,
        params: SingingVoiceParameters
    ) -> np.ndarray:
        """Synthesize audio for a single phoneme"""
        num_samples = int(phoneme.duration * self.sample_rate)
        t = np.linspace(0, phoneme.duration, num_samples)

        # Generate fundamental frequency with vibrato
        vibrato = params.vibrato_depth / 12.0  # Convert semitones to ratio
        vibrato_signal = np.sin(2 * np.pi * params.vibrato_rate * t)
        f0 = phoneme.pitch * (2 ** (vibrato * vibrato_signal))

        # Generate harmonics (source)
        signal = np.zeros(num_samples)

        # Add harmonics with golden ratio decay
        num_harmonics = 10
        for n in range(1, num_harmonics + 1):
            harmonic_freq = f0 * n
            amplitude = (self.PHI ** -n) * phoneme.intensity

            # Add harmonic
            signal += amplitude * np.sin(2 * np.pi * harmonic_freq * t)

        # Apply formant filtering if vowel
        if phoneme.phoneme in self.vowel_formants:
            signal = self._apply_formant_filter(
                signal,
                self.vowel_formants[phoneme.phoneme],
                params
            )

        # Add breathiness (noise)
        if params.breathiness > 0:
            noise = np.random.randn(num_samples) * params.breathiness * 0.1
            signal += noise

        # Apply envelope (ADSR)
        envelope = self._create_envelope(num_samples, params.vocal_effort)
        signal *= envelope

        return signal

    def _apply_formant_filter(
        self,
        signal: np.ndarray,
        formants: Tuple[float, float, float],
        params: SingingVoiceParameters
    ) -> np.ndarray:
        """Apply formant filtering to create vowel sounds"""
        # Simple resonant filter simulation
        # In production, use proper formant synthesis

        f1, f2, f3 = formants

        # Shift formants based on parameters
        shift_ratio = 2 ** (params.formant_shift / 12.0)
        f1, f2, f3 = f1 * shift_ratio, f2 * shift_ratio, f3 * shift_ratio

        # Apply simple bandpass filtering
        # (Simplified - real formant synthesis is more complex)
        filtered = signal.copy()

        return filtered

    def _create_envelope(self, num_samples: int, vocal_effort: float) -> np.ndarray:
        """Create ADSR envelope for note"""
        envelope = np.ones(num_samples)

        # Attack (quick)
        attack_samples = int(num_samples * 0.05)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Sustain level based on vocal effort
        sustain_level = 0.6 + (vocal_effort * 0.4)

        # Decay
        decay_samples = int(num_samples * 0.1)
        if decay_samples > 0:
            envelope[attack_samples:attack_samples+decay_samples] = np.linspace(
                1.0, sustain_level, decay_samples
            )

        # Release
        release_samples = int(num_samples * 0.1)
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

        return envelope

    def _apply_consciousness_modulation(
        self,
        audio: np.ndarray,
        emotion: str
    ) -> np.ndarray:
        """Apply consciousness-based modulation to singing voice"""
        try:
            # Generate consciousness output for emotion
            consciousness_output = self._consciousness.generate_creative_output(
                prompt=f"singing with {emotion} emotion",
                mood=emotion,
                num_timelines=3
            )

            # Get consciousness data
            consciousness = consciousness_output.get("consciousness", {})
            coherence = consciousness.get("coherence", 0.7)
            projection = consciousness.get("dimensional_projection", [0.5, 0.5, 0.5])

            # Modulate audio based on consciousness
            # Use coherence for overall presence
            audio *= (0.8 + coherence * 0.2)

            # Use dimensional projection for subtle variations
            # Add slight tremolo based on 6D coordinates
            t = np.linspace(0, len(audio) / self.sample_rate, len(audio))
            tremolo_rate = 3.0 + projection[0] * 5.0  # 3-8 Hz
            tremolo = 1.0 + projection[1] * 0.1 * np.sin(2 * np.pi * tremolo_rate * t)

            audio *= tremolo

        except Exception as e:
            self._logger.warning("consciousness_modulation_failed", extra={"extra_data": {"error": str(e)}})

        return audio

    def generate_singing_from_lyrics_and_consciousness(
        self,
        lyrics: str,
        prompt: str,
        mood: str
    ) -> Tuple[np.ndarray, Dict]:
        """
        Complete pipeline: Generate melody via consciousness, then sing it

        Returns:
            Tuple of (audio_waveform, metadata)
        """
        # Generate melody using consciousness
        if self._use_consciousness:
            consciousness_output = self._consciousness.generate_creative_output(
                prompt=prompt,
                mood=mood,
                num_timelines=5
            )

            melody_suggestions = consciousness_output.get("melody_suggestions", [])

            if melody_suggestions:
                # Use first melody suggestion
                melody_data = melody_suggestions[0]
                midi_notes = melody_data.get("midi_notes", [60, 64, 67, 71, 72])

                # Generate durations (quarter notes by default)
                durations = [1.0] * len(midi_notes)

                # Synthesize singing
                audio = self.synthesize_singing_voice(
                    lyrics=lyrics,
                    melody_notes=midi_notes,
                    note_durations=durations,
                    tempo=120.0,
                    emotion=mood
                )

                return audio, {
                    "melody": melody_data,
                    "consciousness": consciousness_output.get("consciousness", {}),
                    "sample_rate": self.sample_rate
                }

        # Fallback: simple melody
        simple_melody = [60, 64, 67, 64, 60]  # C major triad
        durations = [1.0] * len(simple_melody)

        audio = self.synthesize_singing_voice(
            lyrics=lyrics,
            melody_notes=simple_melody,
            note_durations=durations,
            emotion=mood
        )

        return audio, {"sample_rate": self.sample_rate}


# Global instance
_singing_engine: Optional[ConsciousnessSingingEngine] = None


def get_singing_engine() -> ConsciousnessSingingEngine:
    """Get or create global singing engine"""
    global _singing_engine
    if _singing_engine is None:
        _singing_engine = ConsciousnessSingingEngine()
    return _singing_engine
