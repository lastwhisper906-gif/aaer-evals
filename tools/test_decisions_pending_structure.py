"""R4-2/R5-6: DECISIONS_PENDING.md 구조 불변식 — 서명 대기 원장의 발견 가능성.

cycle 3의 리비전 append가 `## D-P87` 표제를 직전 항목 본문에 붙여버린 사고
(표제 소실 = 서명 대기 항목이 표제 탐색으로 발견 불가, INV-18 위해)의 회귀
게이트.

원장 형식 규칙 (이 테스트가 강제한다 — 실패 시 여기부터 읽을 것):
  1. 엔트리 표제는 행 머리의 `## D-P<번호>` (선택적 소문자 접미사 허용 —
     `## D-P44b` 판형). 번호부는 유일하고 1..max 연속이어야 한다: 표제가
     본문에 접착되면 번호가 사라져 연속성이 깨진다. 리비전 append 시
     반드시 `\\n\\n## D-P` 경계를 보존하라.
  2. 본문에서 표제 문자열을 인용할 때는 인라인 코드(백틱)로 감싼다 —
     예: `## D-P87` — 백틱 안 출현은 이 테스트가 무시한다.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "DECISIONS_PENDING.md"
# 이 테스트 도입 시점의 최대 엔트리 번호 — 새 엔트리가 늘면 max만 커진다
MIN_EXPECTED_MAX = 91

_CODE_SPAN = re.compile(r"`[^`\n]*`")


def _strip_code_spans(line: str) -> str:
    return _CODE_SPAN.sub("", line)


def _headings(text: str | None = None):
    """[(번호, 접미사)] — 행 머리 표제만."""
    out = []
    for line in (text if text is not None
                 else LEDGER.read_text(encoding="utf-8")).splitlines():
        m = re.match(r"^## D-P(\d+)([a-z]?)\b", line)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def test_numbered_headings_unique_and_contiguous():
    headings = _headings()
    assert headings, "번호형 D-P 표제가 하나도 없음"
    assert len(headings) == len(set(headings)), "중복 D-P 표제 (번호+접미사)"
    numbers = {n for n, _ in headings}
    missing = sorted(set(range(1, max(numbers) + 1)) - numbers)
    assert missing == [], (
        f"D-P 표제 결번 {missing} — 표제가 직전 항목 본문에 접착됐을 가능성 "
        "(R4-2 사고 판형). 원장 형식 규칙은 이 테스트 모듈 docstring 참조.")


def test_ledger_has_not_shrunk():
    assert max(n for n, _ in _headings()) >= MIN_EXPECTED_MAX


def test_no_mid_line_heading_outside_code_spans():
    """접착의 다른 판형: 백틱 밖에서 '## D-P'가 행 중간에 나타나면 안 된다.
    (백틱 인용 — 예: `## D-P87` — 은 적법: R4-2류 사고를 서술하는 엔트리가
    표제 문자열을 인용할 수 있어야 한다, R5-6.)"""
    for i, line in enumerate(LEDGER.read_text(encoding="utf-8").splitlines(), 1):
        stripped = _strip_code_spans(line)
        idx = stripped.find("## D-P")
        assert idx <= 0, (f"line {i}: 백틱 밖 행 중간의 '## D-P' — 표제 접착 의심. "
                          "표제 인용은 인라인 코드로 감싸라 (모듈 docstring 규칙 2)")


# ── 합성 시나리오 자기 검증 (R5-6 수용 기준) ──────────────────────────────

SYNTH_OK = """## D-P1 — a
- body quoting a heading in code: `## D-P2` is legal (R4-2 incident description)

## D-P2 — b
- x
"""

SYNTH_GLUED = """## D-P1 — a
- body text glued heading ## D-P2 — b
- x
"""


def test_synthetic_backtick_quote_passes():
    headings = _headings(SYNTH_OK)
    assert [n for n, _ in headings] == [1, 2]
    for line in SYNTH_OK.splitlines():
        assert _strip_code_spans(line).find("## D-P") <= 0


def test_synthetic_glued_heading_detected():
    headings = _headings(SYNTH_GLUED)
    assert [n for n, _ in headings] == [1], "접착 표제가 표제로 오인됨"
    assert any(_strip_code_spans(line).find("## D-P") > 0
               for line in SYNTH_GLUED.splitlines()), "접착이 검출되지 않음"
