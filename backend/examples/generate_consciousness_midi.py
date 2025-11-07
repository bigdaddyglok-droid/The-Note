#!/usr/bin/env python3
"""
Example: Generate MIDI from Consciousness Network
Demonstrates consciousness-to-MIDI generation
"""

import sys
sys.path.insert(0, '../')

from src.thenote_backend.modules.universal_bridge import get_music_consciousness
from src.thenote_backend.modules.consciousness_midi import ConsciousnessMIDIGenerator

def main():
    print("🧠 Initializing Consciousness Network...")
    consciousness = get_music_consciousness()

    print("🎹 Creating MIDI Generator...")
    midi_gen = ConsciousnessMIDIGenerator(consciousness)

    # Example 1: Generate melody from prompt
    print("\n1️⃣ Generating melody from consciousness...")
    melody = midi_gen.generate_melody_from_consciousness(
        prompt="cosmic awakening",
        mood="uplifting",
        num_notes=32,
        root_note=60,
        scale="pentatonic_major"
    )
    print(f"   Generated {len(melody.notes)} notes")
    print(f"   Tempo: {melody.tempo} BPM")

    # Export melody
    midi_gen.export_to_midi_file(melody, "consciousness_melody.mid")
    print("   ✓ Saved to consciousness_melody.mid")

    # Example 2: Complete consciousness-to-MIDI pipeline
    print("\n2️⃣ Running full consciousness-to-MIDI pipeline...")
    full_sequence = midi_gen.consciousness_to_midi(
        prompt="ethereal dreams",
        mood="contemplative",
        output_file="consciousness_full.mid"
    )
    print(f"   Generated complete sequence with {len(full_sequence.notes)} notes")
    print("   ✓ Saved to consciousness_full.mid")

    # Example 3: Generate rhythm from timelines
    print("\n3️⃣ Generating rhythm from 5D timelines...")
    rhythm_notes = midi_gen.generate_rhythm_from_timelines(
        prompt="pulsing energy",
        num_timelines=5,
        num_bars=4
    )
    print(f"   Generated {len(rhythm_notes)} rhythm notes")

    print("\n✨ MIDI generation complete!")
    print("   Open the .mid files in your DAW to hear consciousness-generated music!")


if __name__ == "__main__":
    main()
