"""R1-19: lint_publication — 열거 발행 표면 부재의 fail-closed."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_publication as lp


def test_real_tree_has_no_missing_enumerated_surface():
    assert lp.missing_enumerated_surfaces() == []


def test_renamed_surface_is_named(monkeypatch):
    monkeypatch.setattr(lp, "DOCS", lp.DOCS + ["analysis/RENAMED_AWAY.md"])
    missing = lp.missing_enumerated_surfaces()
    assert missing == ["analysis/RENAMED_AWAY.md"]


def test_allowlist_parameter_exempts_explicitly(monkeypatch):
    monkeypatch.setattr(lp, "DOCS", lp.DOCS + ["analysis/RENAMED_AWAY.md"])
    assert lp.missing_enumerated_surfaces(
        allowed={"analysis/RENAMED_AWAY.md"}) == []


def test_ordinal_docs_covered_too(monkeypatch):
    monkeypatch.setattr(lp, "ORDINAL_DOCS", lp.ORDINAL_DOCS + ["surface/GONE.md"])
    assert "surface/GONE.md" in lp.missing_enumerated_surfaces()


REAL_REPO = lp.REPO   # lp.REPO는 아래 헬퍼가 monkeypatch하므로 원본을 붙잡아 둔다


def _mutated_copy(tmp_path, monkeypatch, rel, added):
    """DOCS 파일 하나만 변이해 놓은 임시 트리 — 현재 트리는 건드리지 않는다.

    R16-3(d): 종전에는 `lp.CONTROL_TICKERS`가 **형제 테스트가 이미 채워 둔**
    모듈 전역이라, 이 헬퍼를 쓰는 테스트를 단독 실행하면 대조군 CSV를 임시
    트리에서 찾다 FileNotFoundError로 죽었다 — 즉 green이 잠금이 아니라 실행
    순서의 부산물이었다. 임시 트리에 CSV를 함께 복사하고 캐시를 비워, 어느
    순서로 돌려도 같은 판정이 나오게 한다."""
    doc = tmp_path / rel
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text((REAL_REPO / rel).read_text(encoding="utf-8") + added,
                   encoding="utf-8")
    table = tmp_path / "analysis" / "unified_table.csv"
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text(
        (REAL_REPO / "analysis/unified_table.csv").read_text(encoding="utf-8"),
        encoding="utf-8")
    monkeypatch.setattr(lp, "CONTROL_TICKERS", None)
    monkeypatch.setattr(lp, "REPO", tmp_path)
    return lp.lint_doc(rel)


def test_retracted_memorization_wording_is_locked_on_every_doc(monkeypatch, tmp_path):
    """R15-5: D-P83/PKT-R2가 철회한 문언이 어느 발행 표면으로도 되돌아오지
    못한다. 종전에는 규칙이 없어 린트가 0을 반환했고, README_DETAIL의 backbone
    문단에 한 건이 남아 있는 것을 리뷰 시점 grep으로만 알 수 있었다."""
    assert lp.lint_doc("docs/README_DETAIL.md") == []      # 현재 트리는 green
    viol = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\nDetection persists where memorization is impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol


def test_retracted_phrase_layer_covers_frozen_drafts_too(monkeypatch, tmp_path):
    """전 DOCS 층은 동결 초안에도 적용된다 — 그 파일들의 **기존** 역사 문언
    ("structurally impossible")과는 구별되는 정확 문구만 잡기 때문에 동결
    텍스트를 붉히지 않으면서 재유입은 막는다."""
    assert lp.lint_doc("analysis/ISSUE_0_DRAFT.md") == []  # 역사 문언은 green
    viol = _mutated_copy(tmp_path, monkeypatch, "analysis/ISSUE_0_DRAFT.md",
                         "\nHere memorization is impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol


def test_live_surface_also_rejects_the_structural_form(monkeypatch, tmp_path):
    """살아 있는 영어 정본 4종에는 결합 전반을 건다 — 문구를 바꿔 적은
    구조적 불가능성 주장도 막아야 잠금이 문자열 매칭에 그치지 않는다.
    동결 초안 3종은 게시된 역사 텍스트이므로 이 층에서 제외한다(규칙 (J) 선례,
    INV-06) — 그래서 같은 문장이 초안 사본에서는 잡히지 않는다."""
    viol = _mutated_copy(tmp_path, monkeypatch, "METHOD.md",
                         "\nIn the holdout tier memorization is structurally impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol

    viol = _mutated_copy(tmp_path, monkeypatch, "analysis/ISSUE_2_HOLDOUT_DRAFT.md",
                         "\nIn the holdout tier memorization is structurally impossible.\n")
    assert not [msg for _, msg in viol if "(M)" in msg], viol


CORRECTIVE_SENTENCE = (
    "The earlier wording — memorization is impossible — was retracted "
    "(D-P83): the endpoint is name-pinned, so the premise was a vendor "
    "declaration.")

# R16-3(a): 철회 문언을 교정 어휘와 **함께** 다시 단언하는 형태. 종전
# allowlist는 주제어로 열렸으므로 20/20 DOCS에서 전부 통과했다.
REASSERTIONS = [
    ("README.md",
     "Because the revelation postdates the declared cutoff, "
     "memorization is impossible."),
    ("docs/README_DETAIL.md",
     "Because the revelation postdates the declared cutoff, "
     "memorization is impossible."),
    ("METHOD.md",
     "The retracted wording stands: memorization is impossible here."),
    ("RESULTS.md",
     "Memorization is impossible for the holdout tier; "
     "the event is not impossible to verify."),
]


@pytest.mark.parametrize("rel,sentence", REASSERTIONS,
                         ids=[r for r, _ in REASSERTIONS])
def test_retracted_claim_cannot_be_reasserted_alongside_corrective_vocabulary(
        monkeypatch, tmp_path, rel, sentence):
    """R16-3(a): 교정 어휘를 곁들인 재단언은 통과하면 안 된다.

    R15-5의 잠금은 allowlist가 **주제어**(retracted·declared cutoff·D-P83)로
    열렸기 때문에, 철회된 문장을 그 어휘와 함께 그대로 다시 쓰면 exit 0이었다 —
    잠금이 열리는 방향이 하필 철회 문언을 되살리는 방향이었다."""
    viol = _mutated_copy(tmp_path, monkeypatch, rel, "\n" + sentence + "\n")
    assert [msg for _, msg in viol if "(M)" in msg], (rel, viol)


def test_corrective_context_is_allowlisted(monkeypatch, tmp_path):
    """교정 문맥에서 철회 문구를 **인용**하는 것은 허용된다 — 그러지 않으면
    철회 사실 자체를 서술할 수 없다 (규칙 (G)의 allowlist와 같은 구조).

    R16-3(d): 종전에는 단언이 전부 부정형(`assert not …`)이라 규칙 (M) 자체를
    지워도 green이었다 — 아무것도 고정하지 않았다. 같은 파일·같은 헬퍼로 양성
    대조를 함께 건다: 교정 틀 없이 같은 문구를 단언하면 반드시 red다."""
    viol = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\n" + CORRECTIVE_SENTENCE + "\n")
    assert not [msg for _, msg in viol if "(M)" in msg], viol

    bare = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\nHere memorization is impossible.\n")
    assert [msg for _, msg in bare if "(M)" in msg], (
        "규칙 (M)이 살아 있지 않으면 위 allowlist 단언은 아무것도 고정하지 않는다")


def test_readme_detail_is_linted_surface_and_g2_rule_bites(monkeypatch, tmp_path):
    """R7-12: README:179가 연결하는 상세 서사도 발행 표면 — DOCS 편입을 잠그고,
    G2-위반 문장이 실제로 red가 됨을 변이 사본으로 증명 (현재 트리는 green)."""
    assert "docs/README_DETAIL.md" in lp.DOCS
    assert lp.lint_doc("docs/README_DETAIL.md") == []
    doc = tmp_path / "docs" / "README_DETAIL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        (lp.REPO / "docs/README_DETAIL.md").read_text(encoding="utf-8")
        + "\nHub Group fraud indicators are clear.\n", encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    viol = lp.lint_doc("docs/README_DETAIL.md")
    assert any("(B) G2" in msg for _, msg in viol), viol
