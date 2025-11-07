#!/usr/bin/env python3
"""
Example: Fine-tune Consciousness Embeddings
Demonstrates embedding fine-tuning based on feedback
"""

import sys
sys.path.insert(0, '../')

import numpy as np
from src.thenote_backend.modules.universal_bridge import get_music_consciousness
from src.thenote_backend.modules.consciousness_finetuning import (
    EmbeddingFineTuner,
    GenreEmbeddingTrainer,
    EmotionCalibrator
)

def main():
    print("🧠 Initializing Consciousness Network...")
    consciousness = get_music_consciousness()

    # Example 1: Fine-tune emotion embeddings with feedback
    print("\n1️⃣ Fine-tuning emotion embeddings...")
    finetuner = EmbeddingFineTuner(consciousness)

    # Simulate user feedback
    for i in range(10):
        audio_features = np.random.randn(128)
        finetuner.add_feedback(
            concept="uplifting",
            audio_features=audio_features,
            was_correct=(i % 3 == 0),  # 1/3 correct
            user_rating=0.8 if i % 3 == 0 else 0.3
        )

    # Fine-tune based on feedback
    print("   Fine-tuning 'uplifting' embedding...")
    updated_embedding = finetuner.fine_tune_embedding("uplifting", num_steps=20)
    print(f"   ✓ Updated embedding shape: {updated_embedding.shape}")

    # Example 2: Train genre embeddings
    print("\n2️⃣ Training genre embeddings...")
    genre_trainer = GenreEmbeddingTrainer(consciousness)

    # Simulate genre-specific audio samples
    jazz_samples = [np.random.randn(128) * 0.8 for _ in range(20)]
    classical_samples = [np.random.randn(128) * 0.6 for _ in range(20)]

    genre_embeddings = genre_trainer.train_multiple_genres({
        "jazz": jazz_samples,
        "classical": classical_samples
    }, epochs=10)

    print(f"   ✓ Trained embeddings for {len(genre_embeddings)} genres")

    # Example 3: Calibrate emotion detection
    print("\n3️⃣ Calibrating emotion detection...")
    calibrator = EmotionCalibrator(consciousness)

    # Simulate corrections
    for i in range(5):
        audio_features = np.random.randn(128)
        calibrator.add_correction(
            audio_features=audio_features,
            predicted_emotion="contemplative",
            correct_emotion="somber"
        )

    improvements = calibrator.calibrate()
    print("   Calibration improvements:")
    for emotion, improvement in improvements.items():
        print(f"     {emotion}: {improvement:.4f}")

    # Save fine-tuned embeddings
    print("\n4️⃣ Saving fine-tuned embeddings...")
    from pathlib import Path
    Path("finetuned_embeddings").mkdir(exist_ok=True)

    finetuner.save_embeddings(Path("finetuned_embeddings/embeddings.json"))
    finetuner.save_feedback_history(Path("finetuned_embeddings/feedback.json"))
    print("   ✓ Saved to finetuned_embeddings/")

    print("\n✨ Fine-tuning complete!")


if __name__ == "__main__":
    main()
