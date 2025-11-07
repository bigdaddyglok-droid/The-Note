from __future__ import annotations

from typing import List, Sequence

from pydantic import BaseModel, Field


class Syllable(BaseModel):
    text: str
    stress: str = Field(pattern=r"^[0-2]$")
    phonemes: List[str]


class LyricLineInsight(BaseModel):
    original: str
    normalized: str
    syllables: Sequence[Syllable]
    ipa: Sequence[str]
    rhyme_key: str


class LyricInsight(BaseModel):
    session_id: str
    section_id: str
    lines: Sequence[LyricLineInsight]
    grammar_notes: Sequence[str]
    term_suggestions: Sequence[str]


class LyricRequest(BaseModel):
    session_id: str
    section_id: str
    text: str = Field(min_length=1)
