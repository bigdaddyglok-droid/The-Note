from __future__ import annotations

import base64
import io
import math
from typing import Tuple

import numpy as np
import soundfile as sf

from ..schemas import ModuleEvent, ModuleType, RenderInstruction, RenderedAudio
from ..services.event_bus import event_bus
from ..utils.audio import checksum_audio
from ..services.telemetry import telemetry
from ..utils.logging import get_logger
from .singing_voice import get_singing_engine


class VoicePerformanceSynth:
    def __init__(self) -> None:
        self.sample_rate = 22_050
        self._logger = get_logger("module.voice_synth")

        # Initialize singing engine
        try:
            self._singing_engine = get_singing_engine()
            self._use_singing = True
            self._logger.info("singing_engine_enabled", extra={"extra_data": {"status": "active"}})
        except Exception as e:
            self._logger.warning("singing_engine_fallback", extra={"extra_data": {"error": str(e)}})
            self._singing_engine = None
            self._use_singing = False

    def _text_to_pitches(self, text: str) -> Tuple[np.ndarray, np.ndarray]:
        frequencies = []
        amplitudes = []
        base_freq = 220.0
        for index, char in enumerate(text):
            ascii_val = ord(char)
            offset = (ascii_val % 24) - 12
            freq = base_freq * (2 ** (offset / 12))
            frequencies.append(freq)
            amplitude = 0.6 + 0.4 * math.sin(index / 5)
            amplitudes.append(amplitude)
        return np.array(frequencies), np.array(amplitudes)

    def _render_waveform(self, frequencies: np.ndarray, amplitudes: np.ndarray) -> np.ndarray:
        duration = max(1.2, len(frequencies) * 0.08)
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        waveform = np.zeros_like(t)
        envelope = np.linspace(0.8, 0.2, len(frequencies))
        for idx, freq in enumerate(frequencies):
            amp = amplitudes[idx] * envelope[idx % len(envelope)]
            waveform += amp * np.sin(2 * np.pi * freq * t)
        waveform = np.tanh(waveform)  # soft clipping
        return waveform.astype(np.float32)

    def _encode_waveform(self, waveform: np.ndarray) -> Tuple[str, float, float]:
        buffer = io.BytesIO()
        sf.write(buffer, waveform, self.sample_rate, format="wav")
        raw_bytes = buffer.getvalue()
        loudness = float(np.sqrt(np.mean(np.square(waveform))))
        duration_ms = len(waveform) / self.sample_rate * 1000
        encoded = base64.b64encode(raw_bytes).decode("ascii")
        return encoded, duration_ms, loudness

    async def render(self, instruction: RenderInstruction) -> RenderedAudio:
        # Try singing synthesis first if enabled
        if self._use_singing and self._singing_engine and hasattr(instruction, 'mode') and instruction.mode == 'singing':
            try:
                # Extract parameters from instruction
                mood = getattr(instruction, 'mood', 'uplifting')
                prompt = getattr(instruction, 'prompt', instruction.text)

                # Generate singing
                waveform, metadata = self._singing_engine.generate_singing_from_lyrics_and_consciousness(
                    lyrics=instruction.text,
                    prompt=prompt,
                    mood=mood
                )

                self._logger.info("singing_synthesis_used", extra={"extra_data": {"mood": mood}})
            except Exception as e:
                self._logger.warning("singing_synthesis_fallback", extra={"extra_data": {"error": str(e)}})
                # Fall back to simple rendering
                frequencies, amplitudes = self._text_to_pitches(instruction.text)
                waveform = self._render_waveform(frequencies, amplitudes)
        else:
            # Use simple tone-based rendering
            frequencies, amplitudes = self._text_to_pitches(instruction.text)
            waveform = self._render_waveform(frequencies, amplitudes)

        encoded, duration_ms, loudness = self._encode_waveform(waveform)
        checksum = checksum_audio(waveform)
        rendered = RenderedAudio(
            session_id=instruction.session_id,
            render_id=instruction.render_id,
            url_or_blob=encoded,
            duration_ms=duration_ms,
            loudness=loudness,
            checksum=checksum,
        )
        self._logger.info(
            "voice_render_complete",
            extra={
                "extra_data": {
                    "session_id": instruction.session_id,
                    "render_id": instruction.render_id,
                    "duration_ms": duration_ms,
                    "loudness": loudness,
                }
            },
        )
        await telemetry.increment("voice.renders")
        await event_bus.publish(
            ModuleEvent(
                session_id=instruction.session_id,
                source=ModuleType.VOICE_SYNTH,
                target=ModuleType.MEMORY,
                payload=rendered.model_dump(),
            )
        )
        return rendered
