"""The date gate, and the scan that says nothing walked around it.

The gate is only worth as much as the guarantee that every extractor uses it,
so the last test here is not about dates at all: it reads every module in
`src/` and fails on a read of a fixture or a bundle that does not go through
`src/cutoff_guard.py`. Run it on its own to see what it found:

    python3.12 tests/test_cutoff_guard.py
"""

from __future__ import annotations

import ast
import datetime as dt
import json
from pathlib import Path

import pytest

from src import cutoff_guard
from src.cutoff_guard import CutoffGuardError, CutoffViolationError

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
FIXTURES = REPO_ROOT / "tests" / "fixtures"

# The AAPL 10-K in the fixtures was filed on this date; the gate's whole job is
# the comparison against it, so the test states it rather than reading it back
# out of the same manifest the gate reads.
AAPL_10K = FIXTURES / "AAPL" / "10-K" / "aapl-20250927.htm"
AAPL_10K_FILED = dt.date(2025, 10, 31)


def test_a_document_filed_on_the_cutoff_is_allowed():
    text = cutoff_guard.load_document(AAPL_10K, AAPL_10K_FILED)
    assert text.lstrip().startswith("<")


def test_a_document_filed_one_day_after_the_cutoff_is_refused():
    with pytest.raises(CutoffViolationError) as caught:
        cutoff_guard.load_document(AAPL_10K, AAPL_10K_FILED - dt.timedelta(days=1))
    assert caught.value.doc_date == AAPL_10K_FILED
    assert caught.value.cutoff_date == AAPL_10K_FILED - dt.timedelta(days=1)


def test_the_day_after_is_refused_for_every_recorded_document():
    for ticker in sorted(p.name for p in FIXTURES.iterdir() if (p / "manifest.json").is_file()):
        for row in cutoff_guard.documents(ticker):
            filed = dt.date.fromisoformat(row["filing_date"])
            cutoff_guard.load_bytes(row["full_path"], filed)  # allowed on the day
            with pytest.raises(CutoffViolationError):
                cutoff_guard.load_bytes(row["full_path"], filed - dt.timedelta(days=1))


def _fixture_tree(tmp_path: Path, filing_date, body: bytes = b"<html>hi</html>") -> Path:
    """A one-document fixture root whose recorded filing date is under test."""
    root = tmp_path / "fixtures"
    ticker_dir = root / "ZZZZ" / "10-K"
    ticker_dir.mkdir(parents=True)
    (ticker_dir / "doc.htm").write_bytes(body)
    entry = {"form": "10-K", "role": "primary_html", "accession": "0000000000-00-000000",
             "url": "https://example.invalid/doc.htm", "path": "10-K/doc.htm",
             "stored": "identity", "bytes": len(body)}
    if filing_date is not _MISSING:
        entry["filing_date"] = filing_date
    (root / "ZZZZ" / "manifest.json").write_text(json.dumps(
        {"ticker": "ZZZZ", "as_of": "2026-09-01", "documents": [entry]}) + "\n")
    return root


_MISSING = object()


def test_a_missing_filing_date_is_refused(tmp_path):
    root = _fixture_tree(tmp_path, _MISSING)
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_document(root / "ZZZZ" / "10-K" / "doc.htm", "2026-09-01",
                                   fixtures_root=root)


def test_a_null_filing_date_is_refused(tmp_path):
    root = _fixture_tree(tmp_path, None)
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_document(root / "ZZZZ" / "10-K" / "doc.htm", "2026-09-01",
                                   fixtures_root=root)


def test_an_unparseable_filing_date_is_refused(tmp_path):
    root = _fixture_tree(tmp_path, "31 October 2025")
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_document(root / "ZZZZ" / "10-K" / "doc.htm", "2026-09-01",
                                   fixtures_root=root)


def test_a_document_nobody_recorded_is_refused(tmp_path):
    root = _fixture_tree(tmp_path, "2025-10-31")
    stranger = root / "ZZZZ" / "10-K" / "not-in-the-manifest.htm"
    stranger.write_bytes(b"<html>hi</html>")
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_document(stranger, "2026-09-01", fixtures_root=root)


def test_an_unparseable_cutoff_is_refused():
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_document(AAPL_10K, "later")


def test_default_cutoff_is_the_fixture_set_as_of_date():
    assert cutoff_guard.default_cutoff("AAPL") == dt.date(2026, 9, 1)


def test_a_bundle_file_that_is_not_there_is_refused(tmp_path):
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_bundle_file(tmp_path, "input_numbers.json")


# --- the bypass scan -------------------------------------------------------

READERS = ("read_text", "read_bytes", "glob", "open")
# The fetcher is the module that *creates* fixtures from EDGAR; it is upstream
# of the gate, not behind it. It is listed here rather than silently skipped.
EXEMPT = {"cutoff_guard.py", "fetch_fixtures.py"}


def _mentions_a_document_root(node: ast.Call) -> str | None:
    """The source of the parts of a read call that name what is being read."""
    parts: list[ast.AST] = []
    if isinstance(node.func, ast.Name) and node.func.id == "open":
        parts = list(node.args)
    elif isinstance(node.func, ast.Attribute) and node.func.attr in READERS:
        parts = [node.func.value] + list(node.args)
    if not parts:
        return None
    source = " ".join(ast.unparse(part) for part in parts)
    return source if ("fixtures" in source.lower() or "runs" in source.lower()) else None


def bypass_scan(src_dir: Path = SRC) -> list[str]:
    """One line per read of a fixture or a bundle that skips the gate."""
    found = []
    for path in sorted(src_dir.glob("*.py")):
        if path.name in EXEMPT:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            source = _mentions_a_document_root(node)
            if source is not None:
                found.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}: {source}")
    return found


def test_no_module_reads_a_fixture_or_a_bundle_behind_the_gate():
    found = bypass_scan()
    assert not found, "reads that skip src/cutoff_guard.py:\n" + "\n".join(found)


if __name__ == "__main__":
    lines = bypass_scan()
    print("\n".join(lines) if lines else
          f"bypass scan: {len(list(SRC.glob('*.py')))} modules in src/, "
          f"{len(EXEMPT)} exempt ({', '.join(sorted(EXEMPT))}), 0 reads skip the gate")
