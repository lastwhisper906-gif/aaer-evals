"""R1-19: lint_publication — 열거 발행 표면 부재의 fail-closed."""
import sys
from pathlib import Path

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
    """DOCS 파일 하나만 변이해 놓은 임시 트리 — 현재 트리는 건드리지 않는다."""
    doc = tmp_path / rel
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text((REAL_REPO / rel).read_text(encoding="utf-8") + added,
                   encoding="utf-8")
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


def test_corrective_context_is_allowlisted(monkeypatch, tmp_path):
    """교정 문맥에서 철회 문구를 **인용**하는 것은 허용된다 — 그러지 않으면
    철회 사실 자체를 서술할 수 없다 (규칙 (G)의 allowlist와 같은 구조)."""
    viol = _mutated_copy(
        tmp_path, monkeypatch, "docs/README_DETAIL.md",
        "\nThe earlier wording — memorization is impossible — was retracted "
        "(D-P83): the endpoint is name-pinned, so the premise was a vendor "
        "declaration.\n")
    assert not [msg for _, msg in viol if "(M)" in msg], viol


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
