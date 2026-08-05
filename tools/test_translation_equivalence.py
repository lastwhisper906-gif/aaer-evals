"""Lock numeric fidelity between canonical translations and frozen originals."""

from collections import Counter
from pathlib import Path
import re


REPO = Path(__file__).resolve().parents[1]
TRANSLATION_PAIRS = (
    ("analysis/DECISION_TABLE.md", "analysis/DECISION_TABLE.ko.md"),
)
FROZEN_NOTE = "> 한국어 원본 (동결) — 영어 정본: DECISION_TABLE.md (F-01/F-02, D-P50)"
HANGUL = re.compile(r"[\uac00-\ud7a3]")
# Intervals and ratios are matched before their constituent numbers.
NUMERIC_TOKEN = re.compile(
    r"(?<![\d.])(?:\[\d+(?:\.\d+)?%, \d+(?:\.\d+)?%\]|"
    r"\d+(?:\.\d+)?/\d+(?:\.\d+)?|"
    r"\d+(?:\.\d+)?%|\d+(?:\.\d+)?(?:[-–]\d+(?:\.\d+)?)?)(?![\d.])"
)


def _without_added_pointer_lines(text: str) -> str:
    """Exclude only leading blockquotes identifying the F-01/F-02 companion."""
    lines = text.splitlines()
    while lines and (not lines[0].strip() or lines[0].startswith(">")):
        line = lines[0]
        if line.startswith(">") and (
            "F-01/F-02" in line or "Korean original" in line
        ):
            lines.pop(0)
            if lines and not lines[0].strip():
                lines.pop(0)
            continue
        break
    return "\n".join(lines)


def _numeric_tokens(text: str) -> Counter[str]:
    return Counter(NUMERIC_TOKEN.findall(_without_added_pointer_lines(text)))


def test_translation_numeric_tokens_match() -> None:
    for en_path, ko_path in TRANSLATION_PAIRS:
        en_tokens = _numeric_tokens((REPO / en_path).read_text(encoding="utf-8"))
        ko_tokens = _numeric_tokens((REPO / ko_path).read_text(encoding="utf-8"))
        missing = ko_tokens - en_tokens
        extra = en_tokens - ko_tokens
        assert en_tokens == ko_tokens, (
            f"{en_path} numeric-token mismatch vs {ko_path}; "
            f"missing={dict(missing)}, extra={dict(extra)}"
        )


def test_frozen_note_and_english_only() -> None:
    for en_path, ko_path in TRANSLATION_PAIRS:
        en_text = (REPO / en_path).read_text(encoding="utf-8")
        ko_text = (REPO / ko_path).read_text(encoding="utf-8")
        assert ko_text.startswith(FROZEN_NOTE + "\n")
        assert not HANGUL.search(en_text), f"Hangul found in {en_path}"
