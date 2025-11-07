"""
Consciousness MIDI Generator
Generate MIDI output directly from consciousness network
"""

from __future__ import annotations

import numpy as np
import torch
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from .universal_bridge import MusicConsciousnessEngine


@dataclass
class MIDINote:
    """MIDI note representation"""
    pitch: int  # MIDI note number (0-127)
    velocity: int  # Note velocity (0-127)
    start_time: float  # Start time in beats
    duration: float  # Duration in beats
    channel: int = 0  # MIDI channel


@dataclass
class MIDISequence:
    """MIDI sequence representation"""
    notes: List[MIDINote]
    tempo: float = 120.0  # BPM
    time_signature: Tuple[int, int] = (4, 4)
    key_signature: str = "Cmaj"


class ConsciousnessMIDIGenerator:
    """Generate MIDI sequences from consciousness network"""

    def __init__(self, consciousness_engine: MusicConsciousnessEngine):
        self.consciousness = consciousness_engine
        self.PHI = (1 + np.sqrt(5)) / 2

        # Musical scales
        self.scales = {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "minor": [0, 2, 3, 5, 7, 8, 10],
            "pentatonic_major": [0, 2, 4, 7, 9],
            "pentatonic_minor": [0, 3, 5, 7, 10],
            "blues": [0, 3, 5, 6, 7, 10],
            "dorian": [0, 2, 3, 5, 7, 9, 10],
            "phrygian": [0, 1, 3, 5, 7, 8, 10],
            "lydian": [0, 2, 4, 6, 7, 9, 11],
            "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        }

    def generate_melody_from_consciousness(
        self,
        prompt: str,
        mood: str,
        num_notes: int = 16,
        root_note: int = 60,  # Middle C
        scale: str = "major"
    ) -> MIDISequence:
        """
        Generate a melody using consciousness network

        The network explores multiple timelines and generates notes
        based on 6D consciousness projection
        """
        # Generate creative output
        consciousness_output = self.consciousness.generate_creative_output(
            prompt=prompt,
            mood=mood,
            num_timelines=5
        )

        # Extract consciousness data
        consciousness_data = consciousness_output.get("consciousness", {})
        dimensional_projection = consciousness_data.get("dimensional_projection", [0.5, 0.5, 0.5])

        # Get scale intervals
        scale_intervals = self.scales.get(scale, self.scales["major"])

        # Generate notes based on consciousness output
        notes = []
        current_time = 0.0

        # Use consciousness projection for melodic contour
        for i in range(num_notes):
            # Map consciousness values to scale degrees
            # Use golden ratio for melodic movement
            phase = (i / num_notes) * 2 * np.pi
            consciousness_phase = dimensional_projection[0] * np.cos(phase * self.PHI)
            consciousness_phase += dimensional_projection[1] * np.sin(phase / self.PHI)

            # Convert to scale degree
            scale_degree = int((consciousness_phase + 1) * len(scale_intervals) / 2) % len(scale_intervals)
            pitch = root_note + scale_intervals[scale_degree]

            # Octave displacement based on second dimension
            octave_shift = int((dimensional_projection[1] - 0.5) * 24)  # Up to 2 octaves
            pitch += octave_shift
            pitch = np.clip(pitch, 0, 127)

            # Velocity based on consciousness coherence
            coherence = consciousness_data.get("coherence", 0.7)
            velocity = int(coherence * 100 + 20)  # 20-120
            velocity = np.clip(velocity, 0, 127)

            # Duration based on golden ratio
            if i % int(self.PHI * 2) == 0:
                duration = 1.0  # Longer note on golden ratio beats
            else:
                duration = 0.5

            note = MIDINote(
                pitch=int(pitch),
                velocity=int(velocity),
                start_time=current_time,
                duration=duration
            )
            notes.append(note)
            current_time += duration

        return MIDISequence(notes=notes, tempo=120.0)

    def generate_harmony_from_energy_states(
        self,
        audio_features: np.ndarray,
        root_note: int = 60,
        num_voices: int = 4
    ) -> MIDISequence:
        """
        Generate harmonic accompaniment based on 14-state energy analysis

        Each energy state influences a different voice
        """
        # Analyze audio through consciousness
        consciousness_analysis = self.consciousness.analyze_audio_consciousness(
            audio_features,
            sample_rate=44100
        )

        state_distribution = consciousness_analysis.get("state_distribution", [])
        if len(state_distribution) < 14:
            state_distribution = [1/14] * 14

        # Generate chord voicing based on energy states
        notes = []

        # Map energy states to harmonic intervals
        # Using sacred geometry ratios
        harmonic_intervals = [0, 4, 7, 12]  # Major triad + octave

        for voice_idx in range(num_voices):
            # Select energy state for this voice
            state_idx = int((voice_idx / num_voices) * 14)
            energy = state_distribution[state_idx]

            # Pitch based on energy level
            interval = harmonic_intervals[voice_idx % len(harmonic_intervals)]
            octave_shift = int(energy * 12)  # Energy influences octave
            pitch = root_note + interval + octave_shift
            pitch = np.clip(pitch, 0, 127)

            # Velocity based on energy
            velocity = int(energy * 100 + 20)
            velocity = np.clip(velocity, 0, 127)

            note = MIDINote(
                pitch=int(pitch),
                velocity=int(velocity),
                start_time=0.0,
                duration=4.0,  # Whole note
                channel=voice_idx
            )
            notes.append(note)

        harmonic_alignment = consciousness_analysis.get("harmonic_alignment", 0.5)
        tempo = 60 + (harmonic_alignment * 60)  # 60-120 BPM based on alignment

        return MIDISequence(notes=notes, tempo=tempo)

    def generate_rhythm_from_timelines(
        self,
        prompt: str,
        num_timelines: int = 5,
        num_bars: int = 4
    ) -> List[MIDINote]:
        """
        Generate rhythmic pattern from timeline exploration

        Each timeline represents a different rhythmic possibility
        """
        # Generate with multiple timelines
        consciousness_output = self.consciousness.generate_creative_output(
            prompt=prompt,
            mood="energetic",
            num_timelines=num_timelines
        )

        timelines_info = consciousness_output.get("timelines", {})
        valences = timelines_info.get("valences", [0.5] * num_timelines)

        # Generate rhythm pattern
        notes = []
        beats_per_bar = 4
        total_beats = num_bars * beats_per_bar

        for beat in range(total_beats):
            # Determine if note plays based on timeline valences
            timeline_idx = beat % num_timelines
            valence = valences[timeline_idx]

            # Higher valence = more likely to play
            if valence > 0.5:
                # Percussion note (MIDI channel 9)
                # Use different percussion instruments based on valence
                if valence > 0.8:
                    pitch = 42  # Closed hi-hat
                elif valence > 0.6:
                    pitch = 38  # Snare
                else:
                    pitch = 36  # Kick drum

                velocity = int(valence * 100 + 20)

                note = MIDINote(
                    pitch=pitch,
                    velocity=velocity,
                    start_time=float(beat),
                    duration=0.5,
                    channel=9  # Percussion channel
                )
                notes.append(note)

        return notes

    def export_to_midi_file(
        self,
        sequence: MIDISequence,
        filepath: str
    ) -> bool:
        """
        Export MIDI sequence to file

        Note: Requires mido library. Install with: pip install mido
        """
        try:
            import mido
            from mido import MidiFile, MidiTrack, Message, MetaMessage

            # Create MIDI file
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)

            # Set tempo
            tempo = mido.bpm2tempo(sequence.tempo)
            track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

            # Set time signature
            track.append(MetaMessage(
                'time_signature',
                numerator=sequence.time_signature[0],
                denominator=sequence.time_signature[1],
                time=0
            ))

            # Convert notes to MIDI messages
            # Sort by start time
            sorted_notes = sorted(sequence.notes, key=lambda n: n.start_time)

            ticks_per_beat = mid.ticks_per_beat
            last_time = 0

            for note in sorted_notes:
                # Note on
                start_ticks = int(note.start_time * ticks_per_beat)
                delta_time = start_ticks - last_time

                track.append(Message(
                    'note_on',
                    note=note.pitch,
                    velocity=note.velocity,
                    time=delta_time,
                    channel=note.channel
                ))

                last_time = start_ticks

                # Note off
                end_ticks = int((note.start_time + note.duration) * ticks_per_beat)
                delta_time = end_ticks - last_time

                track.append(Message(
                    'note_off',
                    note=note.pitch,
                    velocity=0,
                    time=delta_time,
                    channel=note.channel
                ))

                last_time = end_ticks

            # Save file
            mid.save(filepath)
            return True

        except ImportError:
            print("Error: mido library not installed. Install with: pip install mido")
            return False
        except Exception as e:
            print(f"Error exporting MIDI: {e}")
            return False

    def consciousness_to_midi(
        self,
        prompt: str,
        mood: str,
        audio_context: Optional[np.ndarray] = None,
        output_file: Optional[str] = None
    ) -> MIDISequence:
        """
        Complete consciousness-to-MIDI pipeline

        Generates melody, harmony, and rhythm from consciousness network
        """
        # Generate melody
        melody_sequence = self.generate_melody_from_consciousness(
            prompt=prompt,
            mood=mood,
            num_notes=16,
            scale="pentatonic_major" if mood == "uplifting" else "minor"
        )

        # Add harmony if audio context provided
        if audio_context is not None:
            harmony_sequence = self.generate_harmony_from_energy_states(
                audio_context,
                root_note=60
            )
            # Combine melody and harmony
            melody_sequence.notes.extend(harmony_sequence.notes)

        # Add rhythm
        rhythm_notes = self.generate_rhythm_from_timelines(
            prompt=prompt,
            num_timelines=5,
            num_bars=4
        )
        melody_sequence.notes.extend(rhythm_notes)

        # Export if filepath provided
        if output_file:
            self.export_to_midi_file(melody_sequence, output_file)

        return melody_sequence
