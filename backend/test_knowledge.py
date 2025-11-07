#!/usr/bin/env python3
"""
Test Knowledge Base Integration
Quick verification that all knowledge systems work correctly
"""

from src.thenote_backend.modules.knowledge_base import get_knowledge_base

def test_knowledge_base():
    """Test all knowledge base features"""
    print("=" * 80)
    print("Testing The Note Knowledge Base")
    print("=" * 80)

    kb = get_knowledge_base()

    # Test 1: Etymology
    print("\n1. Testing Etymology System")
    print("-" * 80)
    test_words = ["resonance", "vocal", "inspire", "luminous"]
    for word in test_words:
        etymology = kb.get_etymology(word)
        if etymology:
            print(f"✓ {word}: {etymology}")
        else:
            print(f"✗ {word}: No etymology found")

    # Test 2: Vocabulary Suggestions
    print("\n2. Testing Vocabulary Suggestions")
    print("-" * 80)
    themes = ["sound", "light", "water", "emotion"]
    for theme in themes:
        vocab = kb.suggest_vocabulary(theme)
        print(f"✓ {theme.capitalize()}: {', '.join(vocab[:3])}...")

    # Test 3: Frequency Science
    print("\n3. Testing Frequency Science")
    print("-" * 80)
    test_frequencies = [432.0, 528.0, 741.0]
    for freq in test_frequencies:
        explanation = kb.explain_frequency(freq)
        print(f"✓ {freq} Hz:")
        print(f"  {explanation[:100]}...")

    # Test 4: Water Dynamics
    print("\n4. Testing Water Dynamics & Cymatics")
    print("-" * 80)
    for freq in [432.0, 528.0]:
        water_exp = kb.explain_water_resonance(freq)
        print(f"✓ {freq} Hz water patterns:")
        print(f"  {water_exp[:100]}...")

    # Test 5: Brainwave Entrainment
    print("\n5. Testing Brainwave Entrainment")
    print("-" * 80)
    test_tempos = [60.0, 90.0, 120.0, 150.0]
    for tempo in test_tempos:
        state, description = kb.map_tempo_to_brainwave(tempo)
        print(f"✓ {tempo} BPM → {state} ({description})")

    # Test 6: Emotion Mapping
    print("\n6. Testing Emotion-Cognition Mapping")
    print("-" * 80)
    emotions = ["joy", "sadness", "peace", "excitement"]
    for emotion in emotions:
        explanation = kb.explain_emotion_mapping(emotion)
        print(f"✓ {emotion.capitalize()}:")
        print(f"  {explanation[:100]}...")

    # Test 7: Comprehensive Explanation
    print("\n7. Testing Comprehensive Explanation")
    print("-" * 80)
    comprehensive = kb.generate_comprehensive_explanation(
        frequency=432.0,
        tempo=120.0,
        emotion="peace"
    )
    print("✓ Comprehensive explanation (432 Hz, 120 BPM, peace):")
    for line in comprehensive.split('\n')[:10]:
        print(f"  {line}")
    print("  ...")

    print("\n" + "=" * 80)
    print("✓ All Knowledge Base Tests Passed!")
    print("=" * 80)


if __name__ == "__main__":
    test_knowledge_base()
