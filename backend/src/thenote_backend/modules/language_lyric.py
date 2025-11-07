from __future__ import annotations

from typing import List

from ..schemas import (
    LyricInsight,
    LyricLineInsight,
    LyricRequest,
    ModuleEvent,
    ModuleType,
    Syllable,
)
from ..services.event_bus import event_bus
from ..services.telemetry import telemetry
from ..utils import text as text_utils
from ..utils.logging import get_logger


class LanguageLyricModule:
    def __init__(self) -> None:
        self._logger = get_logger("module.language_lyric")

    async def analyze(self, request: LyricRequest) -> LyricInsight:
        lines = [line for line in request.text.splitlines() if line.strip()]
        insights: List[LyricLineInsight] = []
        grammar_notes: List[str] = []
        for line in lines:
            analysis = text_utils.analyze_line(line)
            syllables = [
                Syllable(text=data.text, stress=data.stress, phonemes=data.phonemes)
                for data in analysis["syllables"]
            ]
            if line.endswith("ing") and not line.lower().startswith("sing"):
                grammar_notes.append(f"Consider varying gerund ending in: \"{line}\"")
            insights.append(
                LyricLineInsight(
                    original=line,
                    normalized=analysis["normalized"],
                    syllables=syllables,
                    ipa=list(analysis["ipa"]),
                    rhyme_key=str(analysis["rhyme_key"]),
                )
            )
        suggestions = text_utils.extract_terms(request.text, exclude=text_utils.VOWELS)
        insight = LyricInsight(
            session_id=request.session_id,
            section_id=request.section_id,
            lines=insights,
            grammar_notes=grammar_notes,
            term_suggestions=suggestions,
        )
        self._logger.info(
            "lyric_analyzed",
            extra={
                "extra_data": {
                    "session_id": request.session_id,
                    "section_id": request.section_id,
                    "lines": len(insights),
                    "grammar_notes": len(grammar_notes),
                }
            },
        )
        await telemetry.increment("lyrics.analyzed")
        await event_bus.publish(
            ModuleEvent(
                session_id=request.session_id,
                source=ModuleType.LANGUAGE_LYRIC,
                target=ModuleType.IMAGINATION,
                payload=insight.model_dump(),
            )
        )
        return insight
