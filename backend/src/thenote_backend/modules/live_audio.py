from __future__ import annotations

import asyncio
from typing import Callable

from ..schemas import AudioFrame, ModuleEvent, ModuleType
from ..services.event_bus import event_bus
from ..services.telemetry import telemetry
from ..utils.logging import get_logger


class LiveAudioInput:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._listeners: list[Callable[[AudioFrame], None]] = []
        self._logger = get_logger("module.live_audio")

    async def register_listener(self, listener: Callable[[AudioFrame], None]) -> None:
        async with self._lock:
            self._listeners.append(listener)

    async def ingest(self, frame: AudioFrame) -> AudioFrame:
        frame.compute_levels()
        async with self._lock:
            for listener in self._listeners:
                listener(frame)
        self._logger.info(
            "audio_frame_ingested",
            extra={
                "extra_data": {
                    "session_id": frame.session_id,
                    "frame_id": frame.frame_id,
                    "rms": frame.rms,
                    "peak": frame.peak,
                    "duration_ms": frame.duration_ms,
                }
            },
        )
        await telemetry.increment("audio.frames")
        await event_bus.publish(
            ModuleEvent(
                session_id=frame.session_id,
                source=ModuleType.LIVE_AUDIO,
                target=ModuleType.SOUND_UNDERSTANDING,
                payload=frame.model_dump(),
            )
        )
        return frame
