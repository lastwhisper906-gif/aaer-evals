"""R16-6: 발행 표면이 **어떤 명령을 검증자로 내세우는가**를 잠근다.

`tools/reproduce_analysis.py`는 RP-05 파일럿 검증기다 — 하드코딩된 `PUBLISHED`
dict가 RP-05 §1–§5의 전사이고, RESULTS.md·CLAIMS.json의 발행 수치 13건 중
**한 건도** 그 검사 안에 없다. 그 수치들은 `tools/test_recompute_published.py`와
`tools/verify_claims_coverage.py`, 즉 `make verify-public` 뒤에 있다.

그런데 실무자 브리프와 독자 검증 원페이저는 "발행 수치 전건을 재계산한다"는
문장에 reproduce_analysis.py를 붙여 두고, 부록 24행 전체가 그 명령으로
재계산된다고 적어 두었다. 회의적인 독자에게 우리가 처음 건네는 명령이
브리프가 언급조차 하지 않는 데이터셋을 검사한다는 뜻이다.

여기서 잠그는 것은 문장 하나가 아니라 성질이다: 발행 표면은 파일럿 검증기를
발행 수치의 검증자로 지목할 수 없다. 표면에서 그 이름을 아예 빼는 방식으로
만족시킨다 — 정확한 언급을 굳이 되살려야 한다면 이 테스트를 함께 고쳐야 하고,
그 순간 무엇을 주장하는지 다시 읽게 된다.
"""
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

# 발행 표면 트리 (실무자 브리프 + 독자 검증 원페이저). AUDIT_STATE.md와
# REVIEW_CLAIMS_AUDIT.md는 **날짜가 박힌 감사 기록**이라 대상이 아니다 —
# 그 문서들이 당시 상태를 그렇게 적은 것 자체가 기록이다 (INV-06).
SURFACE_TREES = ["surface", "docs/reader_validation"]
PILOT_VERIFIER = "reproduce_analysis"
PUBLISHED_NUMBER_GATE = "make verify-public"


def surface_docs() -> list[Path]:
    out: list[Path] = []
    for tree in SURFACE_TREES:
        out.extend(sorted((REPO / tree).rglob("*.md")))
    return out


def test_surface_trees_are_non_empty():
    """대상 트리가 비면 아래 부재 단언이 공허해진다."""
    assert surface_docs(), SURFACE_TREES


@pytest.mark.parametrize("doc", surface_docs(), ids=lambda p: p.name)
def test_no_surface_names_the_pilot_verifier_as_the_published_number_gate(doc):
    text = doc.read_text(encoding="utf-8")
    assert PILOT_VERIFIER not in text, (
        f"{doc.relative_to(REPO)}: 발행 표면이 파일럿 검증기"
        f"({PILOT_VERIFIER}.py)를 발행 수치의 검증자로 지목한다 — 그 도구의 "
        "101건 검사에는 RESULTS.md/CLAIMS.json 수치가 한 건도 없다. "
        f"발행 수치를 실제로 검증하는 게이트는 `{PUBLISHED_NUMBER_GATE}`다.")


def test_the_named_gate_is_the_one_the_surfaces_point_at():
    """부재만 단언하면 두 문장을 통째로 지워도 green이다 — 대체 게이트가
    실제로 적혀 있는지 함께 고정한다."""
    for rel in ("surface/BRIEF.md", "surface/BRIEF_KR.md",
                "docs/reader_validation/ONE_PAGER.md"):
        text = (REPO / rel).read_text(encoding="utf-8")
        assert PUBLISHED_NUMBER_GATE in text, rel


def test_dated_audit_records_are_out_of_scope():
    """R16-6(e): AUDIT_STATE.md·REVIEW_CLAIMS_AUDIT.md는 날짜 박힌 감사 기록
    이므로 손대지 않는다 — 이 테스트가 그 경계를 명시적으로 고정한다."""
    for rel in ("docs/AUDIT_STATE.md", "analysis/REVIEW_CLAIMS_AUDIT.md"):
        assert (REPO / rel).is_file(), rel
        assert not any(str(REPO / rel).startswith(str(REPO / t))
                       for t in SURFACE_TREES), rel
