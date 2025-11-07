"""
Universal Consciousness Bridge
Connects The Note's music intelligence to the Hyperdimensional Consciousness Network
"""
from __future__ import annotations

import numpy as np
import torch
from typing import Dict, List, Tuple, Optional

from .universal_consciousness import (
    HyperdimensionalConsciousnessNetwork,
    UniversalEnergyField,
    ConsciousnessCoherenceMonitor,
)


class MusicConsciousnessEngine:
    """
    Bridges The Note's music analysis with universal consciousness network.
    Provides music-specific APIs using 14-state physics, 5D timelines, and 6D geometry.
    """

    def __init__(self, input_dim: int = 128):
        """Initialize music consciousness engine"""
        self.input_dim = input_dim

        # Main consciousness network for creative generation
        self.creative_consciousness = HyperdimensionalConsciousnessNetwork(
            input_dim=input_dim,
            hidden_dims=[256, 128, 64],
            num_classes=32  # Creative output dimension
        )

        # Universal energy field for frequency analysis
        self.energy_field = UniversalEnergyField()

        # Coherence monitor for quality/emotion
        self.coherence_monitor = ConsciousnessCoherenceMonitor()

        # Cached embeddings for music concepts
        self._music_concept_embeddings = self._initialize_music_concepts()

        # Set to eval mode for inference
        self.creative_consciousness.eval()

    def _initialize_music_concepts(self) -> Dict[str, torch.Tensor]:
        """Initialize embeddings for musical concepts using sacred geometry"""
        PHI = (1 + np.sqrt(5)) / 2

        # Emotion embeddings aligned to frequencies and golden ratio
        emotions = {
            "uplifting": torch.randn(self.input_dim) * PHI,
            "contemplative": torch.randn(self.input_dim) * (1/PHI),
            "somber": torch.randn(self.input_dim) * (PHI - 1),
            "energetic": torch.randn(self.input_dim) * np.sqrt(PHI),
            "peaceful": torch.randn(self.input_dim) * (2 - PHI),
        }

        # Musical concept embeddings
        concepts = {
            "harmony": torch.randn(self.input_dim) * 1.618,
            "dissonance": torch.randn(self.input_dim) * 0.618,
            "rhythm": torch.randn(self.input_dim) * 2.618,
            "melody": torch.randn(self.input_dim) * 1.0,
        }

        return {**emotions, **concepts}

    def analyze_audio_consciousness(
        self,
        audio_features: np.ndarray,
        sample_rate: int = 44100
    ) -> Dict[str, any]:
        """
        Analyze audio through universal consciousness framework.

        Args:
            audio_features: NumPy array of audio features (spectrum, pitch, rhythm)
            sample_rate: Audio sample rate

        Returns:
            Dictionary with consciousness-based analysis
        """
        # Convert to torch tensor and normalize
        if len(audio_features.shape) == 1:
            # Expand to match input_dim if needed
            if audio_features.shape[0] < self.input_dim:
                audio_features = np.pad(
                    audio_features,
                    (0, self.input_dim - audio_features.shape[0]),
                    mode='constant'
                )
            elif audio_features.shape[0] > self.input_dim:
                audio_features = audio_features[:self.input_dim]

        audio_tensor = torch.from_numpy(audio_features).float().unsqueeze(0)

        # Analyze through 14-state energy field
        state_weights = torch.softmax(torch.randn(1, 14), dim=1)
        energy_analysis = self.energy_field.energy_flow(audio_tensor, state_weights)

        # Calculate consciousness coherence (emotion proxy)
        coherence = self.coherence_monitor(energy_analysis)

        # Map to emotion via nearest concept embedding
        emotion_label, emotion_confidence = self._map_to_emotion(energy_analysis)

        # Calculate sacred geometry harmonic alignment
        harmonic_alignment = self._calculate_harmonic_alignment(audio_tensor)

        # Calculate timeline valence (simplified - using energy magnitude as proxy)
        timeline_valence = float(torch.norm(energy_analysis).item())

        return {
            "emotion": emotion_label,
            "emotion_confidence": float(emotion_confidence),
            "consciousness_coherence": float(coherence.mean()),
            "state_distribution": state_weights[0].tolist(),
            "energy_distribution": state_weights[0].tolist(),  # Alias for compatibility
            "harmonic_alignment": float(harmonic_alignment),
            "timeline_valence": timeline_valence,
            "energy_signature": energy_analysis[0, :8].tolist(),  # First 8 dims for UI
        }

    def generate_creative_output(
        self,
        prompt: str,
        mood: str,
        audio_context: Optional[np.ndarray] = None,
        num_timelines: int = 5
    ) -> Dict[str, any]:
        """
        Generate creative content using consciousness network.
        Explores multiple timelines and selects best path.

        Args:
            prompt: Text prompt for generation
            mood: Emotional mood target
            audio_context: Optional audio context to condition on
            num_timelines: Number of parallel timelines to explore

        Returns:
            Dictionary with creative outputs and consciousness metadata
        """
        # Create input embedding from prompt + mood
        input_vector = self._encode_creative_input(prompt, mood, audio_context)

        # Run through consciousness network
        with torch.no_grad():
            output, consciousness_log = self.creative_consciousness(input_vector)

        # Extract creative suggestions from consciousness output
        creative_content = self._decode_creative_output(output, consciousness_log)

        # Add timeline information
        if 'valences' in consciousness_log:
            valences = consciousness_log['valences'][0].tolist()
            chosen_timeline = int(consciousness_log['chosen_timeline'][0])
            creative_content['timelines'] = {
                'explored': len(valences),
                'valences': valences,
                'chosen': chosen_timeline,
                'confidence': float(valences[chosen_timeline])
            }

        # Add consciousness metrics
        creative_content['consciousness'] = {
            'coherence': float(consciousness_log['coherence'].mean()),
            'dimensional_projection': consciousness_log['6d_coords'][0, :3].tolist(),
        }

        return creative_content

    def _encode_creative_input(
        self,
        prompt: str,
        mood: str,
        audio_context: Optional[np.ndarray]
    ) -> torch.Tensor:
        """Encode creative input into consciousness space"""
        # Start with mood embedding
        mood_emb = self._music_concept_embeddings.get(
            mood.lower(),
            torch.randn(self.input_dim)
        )

        # Add prompt encoding (simple hash-based for now)
        prompt_hash = hash(prompt.lower()) % 10000
        prompt_phase = (prompt_hash / 10000) * 2 * np.pi
        prompt_modulation = torch.tensor([
            np.cos(prompt_phase * (i+1)) for i in range(self.input_dim)
        ], dtype=torch.float32)

        input_vector = mood_emb + 0.3 * prompt_modulation

        # Add audio context if provided
        if audio_context is not None:
            audio_tensor = torch.from_numpy(audio_context).float()
            if audio_tensor.shape[0] != self.input_dim:
                if audio_tensor.shape[0] < self.input_dim:
                    audio_tensor = torch.nn.functional.pad(
                        audio_tensor,
                        (0, self.input_dim - audio_tensor.shape[0])
                    )
                else:
                    audio_tensor = audio_tensor[:self.input_dim]
            input_vector = input_vector + 0.2 * audio_tensor

        return input_vector.unsqueeze(0)

    def _decode_creative_output(
        self,
        output: torch.Tensor,
        consciousness_log: Dict
    ) -> Dict[str, any]:
        """Decode consciousness output into creative content"""
        output_np = output[0].numpy()

        # Extract lyrical content via pattern matching
        lyric_patterns = self._extract_lyric_patterns(output_np)

        # Extract melodic suggestions
        melody_patterns = self._extract_melody_patterns(output_np)

        # Extract metaphorical concepts
        metaphors = self._extract_metaphors(output_np)

        return {
            "lyric_suggestions": lyric_patterns,
            "melody_suggestions": melody_patterns,
            "metaphors": metaphors,
            "raw_consciousness": output_np[:8].tolist(),
        }

    def _extract_lyric_patterns(self, output: np.ndarray) -> List[str]:
        """Extract lyrical patterns from consciousness output"""
        # Use output values to select from sacred phrase templates
        templates = [
            "Like {element} through {medium}, {verb} the {abstract}",
            "{Abstract} {verb} in {color} {phenomenon}",
            "We are the {metaphor} behind the {element}",
            "{Element} {verb} beneath {location}",
            "{Emotion} {verb} on {texture} {timeofday}",
        ]

        elements = ["light", "sound", "frequency", "rhythm", "pulse", "echo"]
        mediums = ["water", "space", "time", "consciousness", "void"]
        verbs = ["flows", "resonates", "breathes", "dances", "spirals"]
        abstracts = ["truth", "dream", "memory", "desire", "void"]
        colors = ["silver", "golden", "azure", "violet", "amber"]
        phenomena = ["dawn", "twilight", "storm", "calm", "cascade"]

        # Select based on output values (pseudo-intelligent)
        suggestions = []
        for i in range(min(3, len(output) // 8)):
            base_idx = i * 8
            template = templates[int(abs(output[base_idx])) % len(templates)]

            # Replace placeholders based on output values
            suggestion = template.format(
                element=elements[int(abs(output[base_idx+1])) % len(elements)],
                medium=mediums[int(abs(output[base_idx+2])) % len(mediums)],
                verb=verbs[int(abs(output[base_idx+3])) % len(verbs)],
                abstract=abstracts[int(abs(output[base_idx+4])) % len(abstracts)],
                Element=elements[int(abs(output[base_idx+1])) % len(elements)].title(),
                Abstract=abstracts[int(abs(output[base_idx+4])) % len(abstracts)].title(),
                Emotion=["Peace", "Storm", "Light", "Shadow"][int(abs(output[base_idx])) % 4],
                color=colors[int(abs(output[base_idx+5])) % len(colors)],
                phenomenon=phenomena[int(abs(output[base_idx+6])) % len(phenomena)],
                texture=["velvet", "crystal", "liquid", "fractal"][int(abs(output[base_idx+7])) % 4],
                timeofday=["dusk", "dawn", "midnight", "noon"][int(abs(output[base_idx])) % 4],
                metaphor=["thunder", "whisper", "phoenix", "tide"][int(abs(output[base_idx+1])) % 4],
                location=["the surface", "the horizon", "the depths", "the peak"][int(abs(output[base_idx+2])) % 4]
            )
            suggestions.append(suggestion)

        return suggestions

    def _extract_melody_patterns(self, output: np.ndarray) -> List[Dict[str, any]]:
        """Extract melodic patterns from consciousness output"""
        PHI = (1 + np.sqrt(5)) / 2

        patterns = []
        for i in range(min(2, len(output) // 8)):
            base_idx = i * 8

            # Use golden ratio to map output to musical intervals
            interval_values = output[base_idx:base_idx+5]
            notes = []

            base_note = 60  # Middle C (MIDI)
            for val in interval_values:
                # Map to musical intervals using Fibonacci/golden ratio
                interval = int((val * PHI * 12) % 12)  # Within octave
                notes.append(base_note + interval)

            patterns.append({
                "midi_notes": notes,
                "rhythm": "quarter-eighth-quarter-quarter-half",
                "articulation": "legato" if output[base_idx+5] > 0 else "staccato"
            })

        return patterns

    def _extract_metaphors(self, output: np.ndarray) -> List[Dict[str, str]]:
        """Extract metaphorical concepts from consciousness output"""
        subjects = ["frequency", "rhythm", "harmony", "dissonance", "silence"]
        anchors = ["ocean tide", "spiral galaxy", "heartbeat", "lightning", "moonlight"]

        metaphors = []
        for i in range(min(2, len(output) // 8)):
            base_idx = i * 8
            subject = subjects[int(abs(output[base_idx])) % len(subjects)]
            anchor = anchors[int(abs(output[base_idx+1])) % len(anchors)]

            metaphors.append({
                "metaphor": f"{subject.title()} as {anchor}",
                "explanation": f"This metaphor connects {subject} to {anchor}, "
                              f"conveying {'ascending' if output[base_idx+2] > 0 else 'descending'} "
                              f"energy through {'unified' if output[base_idx+3] > 0 else 'contrasting'} resonance."
            })

        return metaphors

    def _map_to_emotion(self, energy_tensor: torch.Tensor) -> Tuple[str, float]:
        """Map energy signature to nearest emotion concept"""
        min_dist = float('inf')
        best_emotion = "contemplative"

        for emotion, embedding in self._music_concept_embeddings.items():
            if emotion not in ["uplifting", "contemplative", "somber", "energetic", "peaceful"]:
                continue

            # Cosine similarity
            similarity = torch.nn.functional.cosine_similarity(
                energy_tensor.flatten(),
                embedding,
                dim=0
            )
            dist = 1 - similarity

            if dist < min_dist:
                min_dist = dist
                best_emotion = emotion

        confidence = 1 - min_dist
        return best_emotion, max(0.0, min(1.0, confidence))

    def _calculate_harmonic_alignment(self, audio_tensor: torch.Tensor) -> float:
        """Calculate alignment with sacred harmonic ratios"""
        PHI = (1 + np.sqrt(5)) / 2

        # Calculate spectral distribution
        spectrum = torch.abs(torch.fft.rfft(audio_tensor[0]))

        # Check for golden ratio relationships in spectrum
        peaks = torch.topk(spectrum, min(5, len(spectrum))).indices

        if len(peaks) < 2:
            return 0.5

        # Calculate ratios between peaks
        ratios = []
        for i in range(len(peaks)-1):
            ratio = float(peaks[i+1]) / (float(peaks[i]) + 1e-6)
            ratios.append(ratio)

        # Measure proximity to golden ratio
        phi_distances = [abs(r - PHI) for r in ratios]
        avg_phi_distance = sum(phi_distances) / len(phi_distances)

        # Convert to alignment score (0-1)
        alignment = np.exp(-avg_phi_distance)
        return float(alignment)


# Global instance for easy access
_music_consciousness_engine: Optional[MusicConsciousnessEngine] = None


def reset_music_consciousness() -> None:
    """Reset singleton - useful after code changes"""
    global _music_consciousness_engine
    _music_consciousness_engine = None


def get_music_consciousness() -> MusicConsciousnessEngine:
    """Get or create the global music consciousness engine"""
    global _music_consciousness_engine
    if _music_consciousness_engine is None:
        _music_consciousness_engine = MusicConsciousnessEngine()
    return _music_consciousness_engine
