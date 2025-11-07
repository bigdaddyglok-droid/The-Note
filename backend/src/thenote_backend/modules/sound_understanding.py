from __future__ import annotations

import asyncio
import time
from typing import Optional

import numpy as np

from ..schemas import AnalysisFrame, AudioFrame, ModuleEvent, ModuleType
from ..services.event_bus import event_bus
from ..services.telemetry import telemetry
from ..utils.logging import get_logger
from ..utils.audio import (
    compute_spectral_energy,
    compute_timbre,
    detect_pitch,
    detect_rhythm,
    estimate_emotion,
)


class SoundUnderstandingEngine:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._store: dict[str, dict[str, AnalysisFrame]] = {}
        self._logger = get_logger("module.sound_understanding")

    async def analyze_frame(self, frame: AudioFrame) -> AnalysisFrame:
        start = time.perf_counter()
        waveform = frame.decode_waveform()
        pitch = detect_pitch(waveform, frame.sample_rate)
        rhythm = detect_rhythm(waveform, frame.sample_rate)
        spectrum = compute_spectral_energy(waveform, frame.sample_rate)
        emotion = estimate_emotion(pitch, rhythm)
        timbre = compute_timbre(spectrum)
        analysis = AnalysisFrame(
            session_id=frame.session_id,
            source_frame_id=frame.frame_id,
            pitch=pitch,
            rhythm=rhythm,
            spectrum=spectrum,
            emotion=emotion,
            timbre=timbre,
        )
        async with self._lock:
            session_store = self._store.setdefault(frame.session_id, {})
            session_store[frame.frame_id] = analysis
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._logger.info(
            "analysis_completed",
            extra={
                "extra_data": {
                    "session_id": frame.session_id,
                    "frame_id": frame.frame_id,
                    "pitch_hz": pitch.hz,
                    "bpm": rhythm.bpm,
                    "emotion": emotion.label,
                    "duration_ms": round(elapsed_ms, 2),
                }
            },
        )
        await telemetry.increment("analysis.frames")
        await telemetry.record_timing("analysis.frame_duration", elapsed_ms)
        await event_bus.publish(
            ModuleEvent(
                session_id=frame.session_id,
                source=ModuleType.SOUND_UNDERSTANDING,
                target=ModuleType.LANGUAGE_LYRIC,
                payload=analysis.model_dump(),
            )
        )
        return analysis

    async def on_event(self, event: ModuleEvent) -> Optional[AnalysisFrame]:
        if event.source != ModuleType.LIVE_AUDIO:
            if event.payload.get("request") == "retrieve":
                frame_id = event.payload["frame_id"]
                return await self.get_analysis(event.session_id, frame_id)
            return None
        frame = AudioFrame(**event.payload)
        return await self.analyze_frame(frame)

    async def get_analysis(self, session_id: str, frame_id: str) -> Optional[AnalysisFrame]:
        async with self._lock:
            return self._store.get(session_id, {}).get(frame_id)
