"""R4-2: DECISIONS_PENDING.md 구조 불변식 — 서명 대기 원장의 발견 가능성.

cycle 3의 리비전 append가 `## D-P87` 표제를 직전 항목 본문에 붙여버린 사고
(표제 소실 = 서명 대기 항목이 표제 탐색으로 발견 불가, INV-18 위해)의 회귀
게이트: 번호형 표제는 유일하고 1..max 연속이어야 한다 — 표제가 본문에
접착되면 번호가 사라져 연속성이 깨진다.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "DECISIONS_PENDING.md"
# 이 테스트 도입 시점의 최대 엔트리 번호 — 새 엔트리가 늘면 max만 커진다
MIN_EXPECTED_MAX = 91


def _numbered_headings():
    text = LEDGER.read_text(encoding="utf-8")
    return [int(m.group(1)) for m in re.finditer(r"^## D-P(\d+)\b", text, re.M)]


def test_numbered_headings_unique_and_contiguous():
    nums = _numbered_headings()
    assert nums, "번호형 D-P 표제가 하나도 없음"
    assert len(nums) == len(set(nums)), "중복 D-P 표제 번호"
    missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
    assert missing == [], (
        f"D-P 표제 결번 {missing} — 표제가 직전 항목 본문에 접착됐을 가능성 "
        "(R4-2 사고 판형); 리비전 append 시 '\\n\\n## D-P' 경계를 보존하라")


def test_ledger_has_not_shrunk():
    assert max(_numbered_headings()) >= MIN_EXPECTED_MAX


def test_every_heading_starts_at_line_start_with_title():
    """접착의 다른 판형: '## D-P' 문자열이 행 중간에 나타나면 안 된다."""
    for i, line in enumerate(LEDGER.read_text(encoding="utf-8").splitlines(), 1):
        idx = line.find("## D-P")
        assert idx <= 0, f"line {i}: 행 중간의 '## D-P' — 표제 접착 의심"
