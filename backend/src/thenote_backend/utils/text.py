from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

VOWELS = "aeiouy"


IPA_MAP: Dict[str, str] = {
    "a": "ɑ",
    "e": "e",
    "i": "i",
    "o": "oʊ",
    "u": "u",
    "y": "j",
    "b": "b",
    "c": "k",
    "d": "d",
    "f": "f",
    "g": "g",
    "h": "h",
    "j": "ʤ",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "q": "k",
    "r": "ɹ",
    "s": "s",
    "t": "t",
    "v": "v",
    "w": "w",
    "x": "ks",
    "z": "z",
}


@dataclass
class SyllableData:
    text: str
    stress: str
    phonemes: List[str]


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s']", " ", text)
    return re.sub(r"\s+", " ", cleaned).strip().lower()


def split_syllables(word: str) -> List[str]:
    if len(word) <= 3:
        return [word]
    syllables: List[str] = []
    current = ""
    for char in word:
        current += char
        if char in VOWELS:
            syllables.append(current)
            current = ""
    if current:
        syllables[-1] += current
    return syllables if syllables else [word]


def stress_pattern(index: int) -> str:
    return "1" if index % 2 == 0 else "0"


def word_to_ipa(word: str) -> List[str]:
    ipa_output: List[str] = []
    for char in word:
        ipa_output.append(IPA_MAP.get(char, char))
    return ipa_output


def rhyme_key(word: str) -> str:
    last_vowel = ""
    for char in reversed(word):
        if char in VOWELS:
            last_vowel = char
            break
    ending = re.sub(r"^[^aeiouy]*", "", word[-3:])
    return last_vowel + ending


def extract_terms(text: str, exclude: Iterable[str]) -> Sequence[str]:
    tokens = [token for token in re.split(r"\W+", text.lower()) if token and token not in exclude]
    frequency = Counter(tokens)
    sorted_terms = sorted(frequency.items(), key=lambda item: (-item[1], item[0]))
    return [term for term, _ in sorted_terms[:5]]


def analyze_line(line: str) -> Dict[str, Sequence[SyllableData]]:
    normalized_line = normalize_text(line)
    words = normalized_line.split()
    syllables: List[SyllableData] = []
    for idx, word in enumerate(words):
        parts = split_syllables(word)
        for part_index, part in enumerate(parts):
            stress = stress_pattern(idx + part_index)
            phonemes = word_to_ipa(part)
            syllables.append(SyllableData(text=part, stress=stress, phonemes=phonemes))
    return {
        "normalized": normalized_line,
        "syllables": syllables,
        "ipa": [phoneme for syllable in syllables for phoneme in syllable.phonemes],
        "rhyme_key": rhyme_key(words[-1]) if words else "",
    }
