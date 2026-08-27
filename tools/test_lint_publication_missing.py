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
