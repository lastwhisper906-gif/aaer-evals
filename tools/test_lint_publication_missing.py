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
