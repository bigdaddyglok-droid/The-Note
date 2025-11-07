from __future__ import annotations

import hashlib
import math
from typing import List, Sequence

import numpy as np

from ..schemas.analysis import (
    EmotionEstimate,
    PitchEstimate,
    RhythmEstimate,
    SpectralBand,
    TimbreDescriptor,
)

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def hz_to_note(hz: float) -> str:
    if hz <= 0:
        return "C3"
    midi = int(round(69 + 12 * math.log2(hz / 440.0)))
    octave = midi // 12 - 1
    name = NOTE_NAMES[midi % 12]
    return f"{name}{octave}"


def _to_mono(waveform: np.ndarray) -> np.ndarray:
    return waveform if waveform.ndim == 1 else waveform.mean(axis=1)


def detect_pitch(waveform: np.ndarray, sample_rate: int) -> PitchEstimate:
    mono = _to_mono(waveform).astype(np.float64)
    mono -= np.mean(mono)
    energy = np.sum(np.square(mono))
    if energy == 0:
        return PitchEstimate(hz=261.63, note="C4", confidence=0.0)
    autocorr = np.correlate(mono, mono, mode="full")[len(mono) - 1 :]
    min_period = max(1, sample_rate // 1000)
    max_period = max(min_period + 1, sample_rate // 40)
    segment = autocorr[min_period:max_period]
    if segment.size == 0 or not np.any(segment):
        return PitchEstimate(hz=261.63, note="C4", confidence=0.1)
    peak_index = int(np.argmax(segment)) + min_period
    hz = sample_rate / peak_index
    note = hz_to_note(hz)
    confidence = float(np.clip(segment.max() / autocorr[0], 0, 1))
    return PitchEstimate(hz=float(hz), note=note, confidence=confidence)


def detect_rhythm(waveform: np.ndarray, sample_rate: int) -> RhythmEstimate:
    mono = np.abs(_to_mono(waveform))
    frame = max(1, int(sample_rate * 0.1))
    window = np.ones(frame) / frame
    envelope = np.convolve(mono, window, mode="valid")
    if envelope.size < 3:
        return RhythmEstimate(bpm=120.0, swing=0.0, time_signature=(4, 4))
    peaks = np.where((envelope[1:-1] > envelope[:-2]) & (envelope[1:-1] > envelope[2:]))[0]
    if len(peaks) < 2:
        return RhythmEstimate(bpm=100.0, swing=0.0, time_signature=(4, 4))
    intervals = np.diff(peaks) / sample_rate
    mean_interval = float(np.mean(intervals))
    if mean_interval <= 0:
        bpm = 120.0
    else:
        bpm = 60.0 / mean_interval
    swing = float(np.clip(np.std(intervals) / (mean_interval + 1e-6), 0, 1))
    return RhythmEstimate(bpm=float(np.clip(bpm, 50, 220)), swing=swing, time_signature=(4, 4))


def compute_spectral_energy(waveform: np.ndarray, sample_rate: int) -> Sequence[SpectralBand]:
    mono = _to_mono(waveform)
    if mono.size == 0:
        return []
    spectrum = np.abs(np.fft.rfft(mono))
    freqs = np.fft.rfftfreq(len(mono), 1 / sample_rate)
    total = float(np.sum(spectrum) + 1e-9)
    bands = {
        "sub_bass": (20, 60),
        "bass": (60, 250),
        "low_mid": (250, 500),
        "mid": (500, 2000),
        "high_mid": (2000, 6000),
        "presence": (6000, 12000),
        "brilliance": (12000, 20000),
    }
    results: List[SpectralBand] = []
    for name, (low, high) in bands.items():
        mask = (freqs >= low) & (freqs < high)
        energy = float(np.sum(spectrum[mask]) / total)
        results.append(SpectralBand(band=name, energy=energy))
    return results


def estimate_emotion(pitch: PitchEstimate, rhythm: RhythmEstimate) -> EmotionEstimate:
    tempo_score = np.clip((rhythm.bpm - 60) / 160, 0, 1)
    pitch_score = np.clip((pitch.hz - 140) / 600, 0, 1)
    valence = float(tempo_score * 0.55 + pitch_score * 0.45)
    arousal = float(np.clip(tempo_score * 0.7 + rhythm.swing * 0.3, 0, 1))
    label = "uplifting" if valence > 0.6 else "contemplative" if valence > 0.3 else "somber"
    return EmotionEstimate(valence=valence * 2 - 1, arousal=arousal * 2 - 1, label=label)


def compute_timbre(bands: Sequence[SpectralBand]) -> TimbreDescriptor:
    mapping = {band.band: band.energy for band in bands}
    brightness = mapping.get("presence", 0.0) + mapping.get("brilliance", 0.0)
    warmth = mapping.get("bass", 0.0) + mapping.get("low_mid", 0.0)
    roughness = mapping.get("high_mid", 0.0)
    breathiness = mapping.get("mid", 0.0) * 0.5
    return TimbreDescriptor(
        brightness=float(np.clip(brightness, 0, 1)),
        warmth=float(np.clip(warmth, 0, 1)),
        roughness=float(np.clip(roughness, 0, 1)),
        breathiness=float(np.clip(breathiness, 0, 1)),
    )


def checksum_audio(data: np.ndarray) -> str:
    normalized = (data * 32767).astype(np.int16).tobytes()
    return hashlib.sha256(normalized).hexdigest()
