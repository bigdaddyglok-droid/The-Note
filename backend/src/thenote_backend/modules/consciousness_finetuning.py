"""
Consciousness Fine-Tuning Utilities
Tools for fine-tuning emotion/genre embeddings
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

from .universal_bridge import MusicConsciousnessEngine


class EmbeddingFineTuner:
    """Fine-tune music concept embeddings based on user feedback"""

    def __init__(self, consciousness_engine: MusicConsciousnessEngine):
        self.consciousness = consciousness_engine
        self.feedback_history: List[Dict] = []
        self.PHI = (1 + np.sqrt(5)) / 2

    def add_feedback(
        self,
        concept: str,
        audio_features: np.ndarray,
        was_correct: bool,
        user_rating: float = 0.5
    ) -> None:
        """
        Add user feedback for a music concept prediction

        Args:
            concept: The music concept (emotion, genre, etc.)
            audio_features: Audio features that were analyzed
            was_correct: Whether the prediction was correct
            user_rating: User rating 0.0-1.0 (0.5 = neutral)
        """
        feedback = {
            "concept": concept,
            "audio_features": audio_features.tolist(),
            "was_correct": was_correct,
            "user_rating": user_rating,
            "timestamp": torch.tensor(0).item()  # Placeholder
        }
        self.feedback_history.append(feedback)

    def fine_tune_embedding(
        self,
        concept: str,
        learning_rate: float = 0.01,
        num_steps: int = 10
    ) -> torch.Tensor:
        """
        Fine-tune embedding for a specific concept based on feedback

        Uses contrastive learning with golden ratio weighting
        """
        if concept not in self.consciousness._music_concept_embeddings:
            raise ValueError(f"Unknown concept: {concept}")

        embedding = self.consciousness._music_concept_embeddings[concept].clone()

        # Get relevant feedback
        relevant_feedback = [
            f for f in self.feedback_history
            if f["concept"] == concept
        ]

        if not relevant_feedback:
            return embedding

        # Prepare training data
        positive_features = []
        negative_features = []

        for feedback in relevant_feedback:
            features = torch.tensor(feedback["audio_features"], dtype=torch.float32)

            if feedback["was_correct"] and feedback["user_rating"] > 0.6:
                positive_features.append(features)
            elif not feedback["was_correct"] or feedback["user_rating"] < 0.4:
                negative_features.append(features)

        if not positive_features:
            return embedding

        # Convert to tensors
        positive_features = torch.stack(positive_features)

        # Fine-tuning via gradient descent
        embedding.requires_grad = True
        optimizer = torch.optim.Adam([embedding], lr=learning_rate)

        for step in range(num_steps):
            optimizer.zero_grad()

            # Contrastive loss: pull towards positive examples
            pos_similarities = F.cosine_similarity(
                embedding.unsqueeze(0),
                positive_features,
                dim=1
            )
            pos_loss = (1 - pos_similarities).mean()

            # Push away from negative examples (if any)
            neg_loss = 0.0
            if negative_features:
                negative_features_tensor = torch.stack(negative_features)
                neg_similarities = F.cosine_similarity(
                    embedding.unsqueeze(0),
                    negative_features_tensor,
                    dim=1
                )
                neg_loss = neg_similarities.mean()

            # Total loss with golden ratio weighting
            total_loss = self.PHI * pos_loss + (1 / self.PHI) * neg_loss

            total_loss.backward()
            optimizer.step()

        # Update in consciousness engine
        embedding.requires_grad = False
        self.consciousness._music_concept_embeddings[concept] = embedding

        return embedding

    def fine_tune_all_concepts(
        self,
        learning_rate: float = 0.01,
        num_steps: int = 10
    ) -> Dict[str, torch.Tensor]:
        """Fine-tune all concept embeddings based on accumulated feedback"""
        results = {}

        for concept in self.consciousness._music_concept_embeddings.keys():
            try:
                embedding = self.fine_tune_embedding(concept, learning_rate, num_steps)
                results[concept] = embedding
            except Exception as e:
                print(f"Error fine-tuning {concept}: {e}")

        return results

    def save_feedback_history(self, filepath: Path) -> None:
        """Save feedback history to disk"""
        with open(filepath, 'w') as f:
            json.dump(self.feedback_history, f, indent=2)

    def load_feedback_history(self, filepath: Path) -> None:
        """Load feedback history from disk"""
        with open(filepath, 'r') as f:
            self.feedback_history = json.load(f)

    def save_embeddings(self, filepath: Path) -> None:
        """Save fine-tuned embeddings to disk"""
        embeddings_dict = {
            concept: embedding.tolist()
            for concept, embedding in self.consciousness._music_concept_embeddings.items()
        }

        with open(filepath, 'w') as f:
            json.dump(embeddings_dict, f, indent=2)

    def load_embeddings(self, filepath: Path) -> None:
        """Load fine-tuned embeddings from disk"""
        with open(filepath, 'r') as f:
            embeddings_dict = json.load(f)

        for concept, embedding_list in embeddings_dict.items():
            embedding = torch.tensor(embedding_list, dtype=torch.float32)
            self.consciousness._music_concept_embeddings[concept] = embedding


class GenreEmbeddingTrainer:
    """Train genre-specific embeddings from music datasets"""

    def __init__(self, consciousness_engine: MusicConsciousnessEngine):
        self.consciousness = consciousness_engine
        self.PHI = (1 + np.sqrt(5)) / 2

    def train_genre_embedding(
        self,
        genre: str,
        audio_samples: List[np.ndarray],
        epochs: int = 20,
        learning_rate: float = 0.001
    ) -> torch.Tensor:
        """
        Train a new genre embedding from audio samples

        Args:
            genre: Genre name (e.g., "jazz", "classical", "electronic")
            audio_samples: List of audio feature arrays
            epochs: Number of training epochs
            learning_rate: Learning rate
        """
        if not audio_samples:
            raise ValueError("No audio samples provided")

        # Initialize embedding with golden ratio
        embedding = torch.randn(self.consciousness.input_dim) * self.PHI
        embedding.requires_grad = True

        optimizer = torch.optim.Adam([embedding], lr=learning_rate)

        # Convert samples to tensors
        samples = [torch.tensor(s, dtype=torch.float32) for s in audio_samples]

        # Ensure all samples have correct dimension
        padded_samples = []
        for sample in samples:
            if len(sample) < self.consciousness.input_dim:
                sample = F.pad(sample, (0, self.consciousness.input_dim - len(sample)))
            else:
                sample = sample[:self.consciousness.input_dim]
            padded_samples.append(sample)

        samples_tensor = torch.stack(padded_samples)

        # Training loop
        for epoch in range(epochs):
            optimizer.zero_grad()

            # Compute similarity to all samples
            similarities = F.cosine_similarity(
                embedding.unsqueeze(0),
                samples_tensor,
                dim=1
            )

            # Maximize similarity to genre samples
            loss = (1 - similarities).mean()

            # Add regularization with golden ratio
            reg_loss = torch.norm(embedding) / self.PHI
            total_loss = loss + 0.01 * reg_loss

            total_loss.backward()
            optimizer.step()

            if (epoch + 1) % 5 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss.item():.4f}")

        # Add to consciousness engine
        embedding.requires_grad = False
        self.consciousness._music_concept_embeddings[genre] = embedding

        return embedding

    def train_multiple_genres(
        self,
        genre_samples: Dict[str, List[np.ndarray]],
        epochs: int = 20
    ) -> Dict[str, torch.Tensor]:
        """
        Train embeddings for multiple genres

        Args:
            genre_samples: Dict mapping genre names to lists of audio samples
        """
        results = {}

        for genre, samples in genre_samples.items():
            print(f"\nTraining embedding for genre: {genre}")
            embedding = self.train_genre_embedding(genre, samples, epochs)
            results[genre] = embedding

        return results


class EmotionCalibrator:
    """Calibrate emotion detection based on user corrections"""

    def __init__(self, consciousness_engine: MusicConsciousnessEngine):
        self.consciousness = consciousness_engine
        self.calibration_data: Dict[str, List[Tuple[np.ndarray, str]]] = {}

    def add_correction(
        self,
        audio_features: np.ndarray,
        predicted_emotion: str,
        correct_emotion: str
    ) -> None:
        """Add a user correction for emotion prediction"""
        if correct_emotion not in self.calibration_data:
            self.calibration_data[correct_emotion] = []

        self.calibration_data[correct_emotion].append((audio_features, predicted_emotion))

    def calibrate(self, learning_rate: float = 0.005) -> Dict[str, float]:
        """
        Calibrate emotion embeddings based on corrections

        Returns accuracy improvements per emotion
        """
        improvements = {}

        for correct_emotion, corrections in self.calibration_data.items():
            if correct_emotion not in self.consciousness._music_concept_embeddings:
                continue

            embedding = self.consciousness._music_concept_embeddings[correct_emotion].clone()
            embedding.requires_grad = True

            optimizer = torch.optim.SGD([embedding], lr=learning_rate)

            # Extract features
            features_list = [torch.tensor(f, dtype=torch.float32) for f, _ in corrections]

            # Pad features
            padded_features = []
            for features in features_list:
                if len(features) < self.consciousness.input_dim:
                    features = F.pad(features, (0, self.consciousness.input_dim - len(features)))
                else:
                    features = features[:self.consciousness.input_dim]
                padded_features.append(features)

            features_tensor = torch.stack(padded_features)

            # Optimization
            for _ in range(10):
                optimizer.zero_grad()

                similarities = F.cosine_similarity(
                    embedding.unsqueeze(0),
                    features_tensor,
                    dim=1
                )

                loss = (1 - similarities).mean()
                loss.backward()
                optimizer.step()

            # Update embedding
            embedding.requires_grad = False
            old_embedding = self.consciousness._music_concept_embeddings[correct_emotion]
            self.consciousness._music_concept_embeddings[correct_emotion] = embedding

            # Calculate improvement
            improvement = F.cosine_similarity(embedding, old_embedding, dim=0).item()
            improvements[correct_emotion] = improvement

        return improvements
