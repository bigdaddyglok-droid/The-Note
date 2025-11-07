#!/usr/bin/env python3
"""
COMPLETE SYSTEM AUDIT - The Note
Verify all claims and integrations top to bottom
"""

import sys
import traceback
import numpy as np

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_pass(msg):
    print(f"✓ {msg}")

def print_fail(msg, error=None):
    print(f"✗ {msg}")
    if error:
        print(f"  Error: {error}")

def test_imports():
    """Test 1: Can we import all modules?"""
    print_section("AUDIT 1: Module Imports")

    results = {}

    # Core consciousness
    try:
        from src.thenote_backend.modules.universal_consciousness import (
            UniversalEnergyField, SixthDimensionProjection, TimelineNavigator
        )
        print_pass("Universal Consciousness (14-state physics, 6D projection, 5D timelines)")
        results['consciousness'] = True
    except Exception as e:
        print_fail("Universal Consciousness", str(e))
        results['consciousness'] = False

    # Bridge
    try:
        from src.thenote_backend.modules.universal_bridge import get_music_consciousness
        print_pass("Universal Bridge (NumPy ↔ PyTorch)")
        results['bridge'] = True
    except Exception as e:
        print_fail("Universal Bridge", str(e))
        results['bridge'] = False

    # Imagination
    try:
        from src.thenote_backend.modules.imagination import ImaginationEngine
        print_pass("Imagination Engine")
        results['imagination'] = True
    except Exception as e:
        print_fail("Imagination Engine", str(e))
        results['imagination'] = False

    # Sound Understanding
    try:
        from src.thenote_backend.modules.sound_understanding import SoundUnderstandingEngine
        print_pass("Sound Understanding")
        results['sound'] = True
    except Exception as e:
        print_fail("Sound Understanding", str(e))
        results['sound'] = False

    # Knowledge Base
    try:
        from src.thenote_backend.modules.knowledge_base import get_knowledge_base
        print_pass("Knowledge Base (Latin, Frequencies, Water, Brainwaves, Psychology)")
        results['knowledge'] = True
    except Exception as e:
        print_fail("Knowledge Base", str(e))
        results['knowledge'] = False

    # Singing Voice
    try:
        from src.thenote_backend.modules.singing_voice import ConsciousnessSingingEngine
        print_pass("Singing Voice Synthesis (IPA phonemes)")
        results['singing'] = True
    except Exception as e:
        print_fail("Singing Voice", str(e))
        results['singing'] = False

    # MIDI
    try:
        from src.thenote_backend.modules.consciousness_midi import ConsciousnessMIDIGenerator
        print_pass("Consciousness MIDI Generation")
        results['midi'] = True
    except Exception as e:
        print_fail("Consciousness MIDI", str(e))
        results['midi'] = False

    # Voice Conversation
    try:
        from src.thenote_backend.services.voice_conversation import get_voice_conversation
        print_pass("Voice Conversation (with autonomous speaking)")
        results['voice_chat'] = True
    except Exception as e:
        print_fail("Voice Conversation", str(e))
        results['voice_chat'] = False

    return results

def test_consciousness_integration():
    """Test 2: Does consciousness actually work?"""
    print_section("AUDIT 2: Consciousness Integration")

    try:
        from src.thenote_backend.modules.universal_bridge import get_music_consciousness

        consciousness = get_music_consciousness()
        print_pass("Consciousness engine initialized")

        # Test audio analysis
        fake_audio = np.random.randn(100).astype(np.float32)
        result = consciousness.analyze_audio_consciousness(fake_audio, sample_rate=22050)

        required_keys = ['emotion', 'consciousness_coherence', 'harmonic_alignment',
                        'energy_distribution', 'timeline_valence']

        missing = [k for k in required_keys if k not in result]
        if missing:
            print_fail(f"Audio analysis missing keys: {missing}")
            return False

        print_pass(f"Audio analysis: emotion={result['emotion']}, coherence={result['consciousness_coherence']:.3f}")

        # Test creative generation
        creative = consciousness.generate_creative_output(
            prompt="uplifting melody",
            mood="joyful",
            num_timelines=3
        )

        if 'lyric_suggestions' in creative:
            print_pass(f"Creative generation: {len(creative['lyric_suggestions'])} lyric suggestions")
        else:
            print_fail("Creative generation missing lyric_suggestions")
            return False

        return True

    except Exception as e:
        print_fail("Consciousness integration failed", str(e))
        traceback.print_exc()
        return False

def test_knowledge_base():
    """Test 3: Does knowledge base work?"""
    print_section("AUDIT 3: Knowledge Base")

    try:
        from src.thenote_backend.modules.knowledge_base import get_knowledge_base

        kb = get_knowledge_base()
        print_pass("Knowledge base initialized")

        # Test etymology
        etymology = kb.get_etymology("resonance")
        if etymology and "son" in etymology:
            print_pass(f"Etymology working: {etymology[:60]}...")
        else:
            print_fail("Etymology not working")
            return False

        # Test frequency science
        freq_exp = kb.explain_frequency(432.0)
        if "432.0 Hz" in freq_exp and "chakra" in freq_exp.lower():
            print_pass(f"Frequency science: {freq_exp[:60]}...")
        else:
            print_fail("Frequency science not working")
            return False

        # Test water dynamics
        water_exp = kb.explain_water_resonance(528.0)
        if "528.0 Hz" in water_exp and ("water" in water_exp.lower() or "geometric" in water_exp.lower()):
            print_pass(f"Water dynamics: {water_exp[:60]}...")
        else:
            print_fail("Water dynamics not working")
            return False

        # Test brainwave mapping
        state, desc = kb.map_tempo_to_brainwave(120.0)
        if state and desc:
            print_pass(f"Brainwave mapping: 120 BPM → {state} ({desc})")
        else:
            print_fail("Brainwave mapping not working")
            return False

        # Test emotion mapping
        emotion_exp = kb.explain_emotion_mapping("joy")
        if "joy" in emotion_exp.lower() and "hz" in emotion_exp.lower():
            print_pass(f"Emotion mapping: {emotion_exp[:60]}...")
        else:
            print_fail("Emotion mapping not working")
            return False

        return True

    except Exception as e:
        print_fail("Knowledge base failed", str(e))
        traceback.print_exc()
        return False

def test_voice_conversation():
    """Test 4: Voice conversation with autonomous speaking"""
    print_section("AUDIT 4: Voice Conversation + Autonomous Speaking")

    try:
        from src.thenote_backend.services.voice_conversation import get_voice_conversation

        voice = get_voice_conversation()
        print_pass("Voice conversation initialized")

        # Check if knowledge base is integrated
        if hasattr(voice, '_knowledge') and voice._knowledge is not None:
            print_pass("Knowledge base integrated into voice conversation")
        else:
            print_fail("Knowledge base NOT integrated")
            return False

        # Check if consciousness is integrated
        if hasattr(voice, '_consciousness') and voice._consciousness is not None:
            print_pass("Consciousness integrated into voice conversation")
        else:
            print_fail("Consciousness NOT integrated")
            return False

        # Test intent detection for knowledge queries
        test_transcripts = {
            "tell me about 432 hz": "explain_frequency",
            "what is the etymology of resonance": "explain_etymology",
            "how does water respond to sound": "explain_water",
            "what brainwave state is 90 bpm": "explain_brainwave",
            "create uplifting lyrics": "generate_lyrics"
        }

        for transcript, expected_intent in test_transcripts.items():
            intent = voice._analyze_intent(transcript)
            if intent == expected_intent:
                print_pass(f"Intent detection: '{transcript}' → {intent}")
            else:
                print_fail(f"Intent detection: '{transcript}' → {intent} (expected {expected_intent})")

        # Check for autonomous speaking method
        if hasattr(voice, '_generate_proactive_suggestion'):
            print_pass("Autonomous speaking system present")
        else:
            print_fail("Autonomous speaking NOT implemented")
            return False

        return True

    except Exception as e:
        print_fail("Voice conversation failed", str(e))
        traceback.print_exc()
        return False

def test_singing_voice():
    """Test 5: Singing voice synthesis"""
    print_section("AUDIT 5: Singing Voice Synthesis")

    try:
        from src.thenote_backend.modules.singing_voice import ConsciousnessSingingEngine

        engine = ConsciousnessSingingEngine()
        print_pass("Singing engine initialized")

        # Test phoneme conversion
        test_lyrics = "hello world"
        phonemes = engine._text_to_phonemes(test_lyrics)
        if phonemes:
            print_pass(f"Text-to-phoneme: '{test_lyrics}' → {phonemes}")
        else:
            print_fail("Text-to-phoneme conversion failed")
            return False

        # Test synthesis (small test)
        melody = [261.63, 293.66, 329.63]  # C, D, E
        durations = [0.5, 0.5, 0.5]

        audio = engine.synthesize_singing_voice(
            lyrics="la la la",
            melody_notes=melody,
            note_durations=durations,
            tempo=120.0
        )

        if audio is not None and len(audio) > 0:
            print_pass(f"Singing synthesis: generated {len(audio)} samples ({len(audio)/44100:.2f}s)")
        else:
            print_fail("Singing synthesis produced no audio")
            return False

        return True

    except Exception as e:
        print_fail("Singing voice failed", str(e))
        traceback.print_exc()
        return False

def test_imagination_consciousness():
    """Test 6: Imagination uses consciousness?"""
    print_section("AUDIT 6: Imagination ↔ Consciousness Integration")

    try:
        from src.thenote_backend.modules.imagination import ImaginationEngine

        imagination = ImaginationEngine()
        print_pass("Imagination engine initialized")

        # Check if consciousness is integrated
        if hasattr(imagination, '_consciousness') and imagination._consciousness is not None:
            print_pass("Consciousness integrated into imagination")
        else:
            print_fail("Consciousness NOT integrated into imagination")
            return False

        if hasattr(imagination, '_use_consciousness'):
            print_pass(f"Consciousness usage flag: {imagination._use_consciousness}")

        return True

    except Exception as e:
        print_fail("Imagination-consciousness integration failed", str(e))
        traceback.print_exc()
        return False

def test_sound_understanding_consciousness():
    """Test 7: Sound Understanding uses consciousness?"""
    print_section("AUDIT 7: Sound Understanding ↔ Consciousness Integration")

    try:
        from src.thenote_backend.modules.sound_understanding import SoundUnderstandingEngine

        sound = SoundUnderstandingEngine()
        print_pass("Sound understanding initialized")

        # Check if consciousness is integrated
        if hasattr(sound, '_consciousness') and sound._consciousness is not None:
            print_pass("Consciousness integrated into sound understanding")
        else:
            print_fail("Consciousness NOT integrated into sound understanding")
            return False

        return True

    except Exception as e:
        print_fail("Sound-consciousness integration failed", str(e))
        traceback.print_exc()
        return False

def generate_audit_report(results):
    """Generate final audit report"""
    print_section("FINAL AUDIT REPORT")

    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)

    print(f"\nTests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%\n")

    print("Component Status:")
    print("-" * 80)
    for component, status in results.items():
        status_str = "✓ PASS" if status else "✗ FAIL"
        print(f"  {component:40s} {status_str}")

    print("\n" + "=" * 80)

    if passed_tests == total_tests:
        print("✓ ALL SYSTEMS OPERATIONAL - WE CAN STAND ON BUSINESS")
    elif passed_tests >= total_tests * 0.8:
        print("⚠ MOSTLY OPERATIONAL - SOME ISSUES TO ADDRESS")
    else:
        print("✗ CRITICAL ISSUES - CANNOT STAND ON BUSINESS")

    print("=" * 80)

    return passed_tests == total_tests

def main():
    print("=" * 80)
    print("  THE NOTE - COMPLETE SYSTEM AUDIT")
    print("  Verifying all claims and integrations")
    print("=" * 80)

    results = {}

    # Run all tests
    import_results = test_imports()
    results.update(import_results)

    if import_results.get('consciousness') and import_results.get('bridge'):
        results['consciousness_functional'] = test_consciousness_integration()
    else:
        results['consciousness_functional'] = False
        print_fail("Skipping consciousness test - imports failed")

    if import_results.get('knowledge'):
        results['knowledge_functional'] = test_knowledge_base()
    else:
        results['knowledge_functional'] = False
        print_fail("Skipping knowledge test - imports failed")

    if import_results.get('voice_chat'):
        results['voice_conversation_functional'] = test_voice_conversation()
    else:
        results['voice_conversation_functional'] = False
        print_fail("Skipping voice conversation test - imports failed")

    if import_results.get('singing'):
        results['singing_functional'] = test_singing_voice()
    else:
        results['singing_functional'] = False
        print_fail("Skipping singing test - imports failed")

    if import_results.get('imagination'):
        results['imagination_consciousness'] = test_imagination_consciousness()
    else:
        results['imagination_consciousness'] = False
        print_fail("Skipping imagination test - imports failed")

    if import_results.get('sound'):
        results['sound_consciousness'] = test_sound_understanding_consciousness()
    else:
        results['sound_consciousness'] = False
        print_fail("Skipping sound understanding test - imports failed")

    # Generate final report
    success = generate_audit_report(results)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
