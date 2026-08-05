"""Lock numeric fidelity between canonical translations and frozen originals."""

from collections import Counter
from pathlib import Path
import re


REPO = Path(__file__).resolve().parents[1]
# (en, ko, ko_frozen_marker_line, en_truncate_at) — truncate handles entries
# appended to the English canonical after the Korean snapshot froze.
TRANSLATION_PAIRS = (
    ("analysis/error_analysis_wave2_holdout.md",
     "analysis/error_analysis_wave2_holdout.ko.md",
     "> 한국어 원본 (동결) — 영어 정본: error_analysis_wave2_holdout.md (F-01/F-02, D-P50)",
     None),
    ("analysis/DECISION_TABLE.md", "analysis/DECISION_TABLE.ko.md",
     "> 한국어 원본 (동결) — 영어 정본: DECISION_TABLE.md (F-01/F-02, D-P50)",
     None),
    ("docs/methodology_limitations.md", "docs/methodology_limitations.ko.md",
     "> 동결 스냅샷: L-1–L-8 (F-01/F-02) — L-9 이후 신규 한계는 영어 정본에만 추가된다.",
     "\n## L-9"),
    ("ERRATA.md", "ERRATA.ko.md",
     "> 한국어 원본 (동결 스냅샷: E-001–E-002) — 영어 정본: ERRATA.md (F-01/F-02, D-P50); 이후 정정 항목은 영어 정본에만 추가된다.",
     None),
)
HANGUL = re.compile(r"[\uac00-\ud7a3]")
# Intervals and ratios are matched before their constituent numbers.
NUMERIC_TOKEN = re.compile(
    r"(?<![\d.])(?:\[\d+(?:\.\d+)?%, \d+(?:\.\d+)?%\]|"
    r"\d+(?:\.\d+)?/\d+(?:\.\d+)?|"
    r"\d+(?:\.\d+)?%|\d+(?:\.\d+)?(?:[-–]\d+(?:\.\d+)?)?)(?!\d)(?!\.\d)"
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
    for en_path, ko_path, _marker, en_truncate in TRANSLATION_PAIRS:
        en_text = (REPO / en_path).read_text(encoding="utf-8")
        if en_truncate and en_truncate in en_text:
            en_text = en_text[: en_text.index(en_truncate)]
        en_tokens = _numeric_tokens(en_text)
        ko_tokens = _numeric_tokens((REPO / ko_path).read_text(encoding="utf-8"))
        missing = ko_tokens - en_tokens
        extra = en_tokens - ko_tokens
        assert en_tokens == ko_tokens, (
            f"{en_path} numeric-token mismatch vs {ko_path}; "
            f"missing={dict(missing)}, extra={dict(extra)}"
        )


def test_frozen_note_and_english_only() -> None:
    for en_path, ko_path, marker, _en_truncate in TRANSLATION_PAIRS:
        en_text = (REPO / en_path).read_text(encoding="utf-8")
        ko_head = "\n".join((REPO / ko_path).read_text(encoding="utf-8").splitlines()[:6])
        assert marker in ko_head, f"frozen marker missing in {ko_path} header"
        visible = re.sub(r"<!--.*?-->", "", en_text, flags=re.S)  # canary comments are non-surface
        assert not HANGUL.search(visible), f"Hangul found in {en_path}"
