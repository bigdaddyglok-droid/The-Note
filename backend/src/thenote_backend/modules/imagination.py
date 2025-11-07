from __future__ import annotations

import random
from typing import Dict, List

from ..schemas import (
    GenerationBundle,
    GenerationRequest,
    GeneratedItem,
    ModuleEvent,
    ModuleType,
)
from ..services.event_bus import event_bus
from ..utils.text import normalize_text
from ..services.telemetry import telemetry
from ..utils.logging import get_logger
from .universal_bridge import get_music_consciousness


class ImaginationEngine:
    def __init__(self) -> None:
        self._seed_phrases: Dict[str, List[str]] = {
            "uplifting": [
                "Rise like auroras in magnetic skies",
                "Hearts bloom in stereo light",
                "We are the thunder behind the dawn",
            ],
            "contemplative": [
                "Echoes drift on lavender dusk",
                "Moonlit questions soften the air",
                "Silence sketches silver outlines",
            ],
            "somber": [
                "Rain etches maps on midnight glass",
                "Hollow choirs breathe in grayscale",
                "Embers sleep beneath the pulse",
            ],
        }
        self._logger = get_logger("module.imagination")

        # Initialize universal consciousness engine
        try:
            self._consciousness = get_music_consciousness()
            self._use_consciousness = True
            self._logger.info("imagination_consciousness_enabled", extra={"extra_data": {"status": "active"}})
        except Exception as e:
            self._logger.warning("imagination_consciousness_fallback", extra={"extra_data": {"reason": str(e)}})
            self._consciousness = None
            self._use_consciousness = False

    def _lyric_payload(self, prompt: str, mood: str) -> Dict[str, List[str]]:
        base = normalize_text(prompt).title()

        # Use consciousness engine if available
        if self._use_consciousness and self._consciousness:
            try:
                consciousness_output = self._consciousness.generate_creative_output(
                    prompt=prompt,
                    mood=mood,
                    num_timelines=5
                )
                lines = consciousness_output.get("lyric_suggestions", [])
                if lines and len(lines) > 0:
                    self._logger.info("lyric_consciousness_generation", extra={"extra_data": {"lines": len(lines)}})
                    return {"prompt": base, "lines": lines, "consciousness": consciousness_output.get("consciousness", {})}
            except Exception as e:
                self._logger.warning("lyric_consciousness_fallback", extra={"extra_data": {"error": str(e)}})

        # Fallback to seed phrases
        options = self._seed_phrases.get(mood, self._seed_phrases["uplifting"])
        lines = random.sample(options, k=min(3, len(options)))
        return {"prompt": base, "lines": lines}

    def _melody_payload(self, tempo: float | None, key: str | None) -> Dict[str, List[str]]:
        scale = key or "Cmaj"
        tempo_val = tempo or 120.0
        notes = ["C4", "E4", "G4", "B4", "C5"] if "maj" in scale.lower() else ["A3", "C4", "E4", "G4", "A4"]
        durations = ["quarter", "eighth", "quarter", "quarter", "half"]
        phrasing = [f"{note}:{duration}" for note, duration in zip(notes, durations)]
        return {"tempo": tempo_val, "key": scale, "phrasing": phrasing}

    def _metaphor_payload(self, prompt: str) -> Dict[str, str]:
        # Use consciousness engine if available
        if self._use_consciousness and self._consciousness:
            try:
                consciousness_output = self._consciousness.generate_creative_output(
                    prompt=prompt,
                    mood="contemplative",  # Metaphors are contemplative
                    num_timelines=3
                )
                metaphors = consciousness_output.get("metaphors", [])
                if metaphors and len(metaphors) > 0:
                    self._logger.info("metaphor_consciousness_generation", extra={"extra_data": {"count": len(metaphors)}})
                    return metaphors[0]  # Return first metaphor
            except Exception as e:
                self._logger.warning("metaphor_consciousness_fallback", extra={"extra_data": {"error": str(e)}})

        # Fallback to simple generation
        normalized = normalize_text(prompt)
        elements = normalized.split()
        if len(elements) < 2:
            elements.extend(["frequency", "light"])
        subject = random.choice(elements)
        anchor = random.choice(["nebula", "rainstorm", "heartbeat", "lighthouse"])
        metaphor = f"{subject.title()} as a {anchor}"
        explanation = (
            f"The metaphor ties {subject} to {anchor}, conveying evolving resonance and dynamic contrast."
        )
        return {"metaphor": metaphor, "explanation": explanation}

    def _structure_payload(self) -> Dict[str, List[str]]:
        sections = ["Intro", "Verse", "Pre-Chorus", "Chorus", "Bridge", "Outro"]
        motifs = ["Rhythm Swell", "Tonal Bloom", "Dynamic Surge", "Call and Response"]
        structure = [f"{section}: {random.choice(motifs)}" for section in sections]
        return {"structure": structure}

    async def generate(self, request: GenerationRequest) -> GenerationBundle:
        mood = "uplifting"
        outputs: List[GeneratedItem] = []
        for mode in request.modes:
            if mode == "lyric":
                payload = self._lyric_payload(request.prompt, mood)
            elif mode == "melody":
                payload = self._melody_payload(request.tempo, request.key)
            elif mode == "metaphor":
                payload = self._metaphor_payload(request.prompt)
            else:
                payload = self._structure_payload()
            outputs.append(
                GeneratedItem(
                    type=mode,
                    payload=payload,
                    confidence=random.uniform(0.72, 0.95),
                )
            )
        bundle = GenerationBundle(session_id=request.session_id, request_id=request.request_id, outputs=outputs)
        self._logger.info(
            "generation_complete",
            extra={
                "extra_data": {
                    "session_id": request.session_id,
                    "request_id": request.request_id,
                    "modes": list(request.modes),
                }
            },
        )
        await telemetry.increment("imagination.requests")
        await event_bus.publish(
            ModuleEvent(
                session_id=request.session_id,
                source=ModuleType.IMAGINATION,
                target=ModuleType.VOICE_SYNTH,
                payload=bundle.model_dump(),
            )
        )
        return bundle
