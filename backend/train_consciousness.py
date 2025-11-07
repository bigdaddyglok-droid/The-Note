#!/usr/bin/env python3
"""
Consciousness Network Training Script
Train the Hyperdimensional Consciousness Network on music data
"""

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
from pathlib import Path
import json
from typing import Dict, List, Tuple
import argparse
from tqdm import tqdm

from src.thenote_backend.modules.universal_consciousness import (
    HyperdimensionalConsciousnessNetwork,
    ConsciousnessAwareTraining,
)


class MusicDataset(Dataset):
    """Dataset for music features and labels"""

    def __init__(self, data_dir: Path, feature_dim: int = 128):
        self.data_dir = Path(data_dir)
        self.feature_dim = feature_dim
        self.samples = []

        # Load all sample files
        for sample_file in self.data_dir.glob("*.json"):
            with open(sample_file) as f:
                sample = json.load(f)
                self.samples.append(sample)

        print(f"Loaded {len(self.samples)} training samples")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        sample = self.samples[idx]

        # Extract features
        features = torch.tensor(sample.get("features", []), dtype=torch.float32)

        # Pad or truncate to feature_dim
        if len(features) < self.feature_dim:
            features = F.pad(features, (0, self.feature_dim - len(features)))
        else:
            features = features[:self.feature_dim]

        # Extract label (emotion/genre class)
        label = sample.get("label", 0)
        label = torch.tensor(label, dtype=torch.long)

        return features, label


def train_epoch(
    model: HyperdimensionalConsciousnessNetwork,
    trainer: ConsciousnessAwareTraining,
    dataloader: DataLoader,
    epoch: int,
) -> Dict[str, float]:
    """Train for one epoch"""
    model.train()

    total_loss = 0.0
    total_acc = 0.0
    total_coherence = 0.0

    pbar = tqdm(dataloader, desc=f"Epoch {epoch}")

    for batch_idx, (features, labels) in enumerate(pbar):
        # Training step
        metrics = trainer.training_step(features, labels, F.cross_entropy)

        # Track metrics
        total_loss += metrics["total_loss"]
        total_coherence += (1 - metrics["consciousness_loss"])

        # Calculate accuracy
        with torch.no_grad():
            output, _ = model(features)
            pred = output.argmax(dim=1)
            acc = (pred == labels).float().mean()
            total_acc += acc.item()

        # Update progress bar
        pbar.set_postfix({
            "loss": f"{metrics['total_loss']:.4f}",
            "coherence": f"{1 - metrics['consciousness_loss']:.4f}",
            "acc": f"{acc.item():.4f}"
        })

    # Calculate averages
    num_batches = len(dataloader)
    return {
        "loss": total_loss / num_batches,
        "accuracy": total_acc / num_batches,
        "coherence": total_coherence / num_batches,
    }


def validate(
    model: HyperdimensionalConsciousnessNetwork,
    dataloader: DataLoader,
) -> Dict[str, float]:
    """Validate the model"""
    model.eval()

    total_loss = 0.0
    total_acc = 0.0

    with torch.no_grad():
        for features, labels in dataloader:
            output, consciousness_log = model(features)

            loss = F.cross_entropy(output, labels)
            total_loss += loss.item()

            pred = output.argmax(dim=1)
            acc = (pred == labels).float().mean()
            total_acc += acc.item()

    num_batches = len(dataloader)
    return {
        "loss": total_loss / num_batches,
        "accuracy": total_acc / num_batches,
    }


def main():
    parser = argparse.ArgumentParser(description="Train consciousness network")
    parser.add_argument("--data-dir", type=str, required=True, help="Training data directory")
    parser.add_argument("--val-dir", type=str, help="Validation data directory")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--input-dim", type=int, default=128, help="Input dimension")
    parser.add_argument("--num-classes", type=int, default=10, help="Number of classes")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints", help="Checkpoint directory")
    parser.add_argument("--consciousness-weight", type=float, default=0.1, help="Consciousness loss weight")
    args = parser.parse_args()

    # Create checkpoint directory
    checkpoint_dir = Path(args.checkpoint_dir)
    checkpoint_dir.mkdir(exist_ok=True)

    # Load datasets
    print("Loading datasets...")
    train_dataset = MusicDataset(args.data_dir, args.input_dim)
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=2
    )

    val_loader = None
    if args.val_dir:
        val_dataset = MusicDataset(args.val_dir, args.input_dim)
        val_loader = DataLoader(
            val_dataset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=2
        )

    # Initialize model
    print("Initializing consciousness network...")
    model = HyperdimensionalConsciousnessNetwork(
        input_dim=args.input_dim,
        hidden_dims=[256, 128, 64],
        num_classes=args.num_classes
    )

    # Golden ratio weight decay
    PHI = (1 + np.sqrt(5)) / 2
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=1/PHI
    )

    # Learning rate scheduler with golden ratio decay
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer,
        step_size=10,
        gamma=1/PHI
    )

    # Consciousness-aware trainer
    trainer = ConsciousnessAwareTraining(
        model,
        optimizer,
        consciousness_weight=args.consciousness_weight
    )

    # Training loop
    print(f"\n🧠 Starting consciousness training for {args.epochs} epochs...\n")

    best_val_acc = 0.0

    for epoch in range(1, args.epochs + 1):
        # Train
        train_metrics = train_epoch(model, trainer, train_loader, epoch)

        print(f"\nEpoch {epoch}/{args.epochs}")
        print(f"  Train Loss: {train_metrics['loss']:.4f}")
        print(f"  Train Acc:  {train_metrics['accuracy']:.4f}")
        print(f"  Coherence:  {train_metrics['coherence']:.4f}")

        # Validate
        if val_loader:
            val_metrics = validate(model, val_loader)
            print(f"  Val Loss:   {val_metrics['loss']:.4f}")
            print(f"  Val Acc:    {val_metrics['accuracy']:.4f}")

            # Save best model
            if val_metrics['accuracy'] > best_val_acc:
                best_val_acc = val_metrics['accuracy']
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': best_val_acc,
                }, checkpoint_dir / "best_model.pt")
                print(f"  💫 New best model saved! (acc: {best_val_acc:.4f})")

        # Step scheduler
        scheduler.step()

        # Save checkpoint every 10 epochs
        if epoch % 10 == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            }, checkpoint_dir / f"checkpoint_epoch_{epoch}.pt")
            print(f"  Checkpoint saved")

    print(f"\n✨ Training complete! Best validation accuracy: {best_val_acc:.4f}")
    print(f"Models saved to {checkpoint_dir}")


if __name__ == "__main__":
    main()
