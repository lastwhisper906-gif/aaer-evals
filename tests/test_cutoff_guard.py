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
import gzip
import hashlib
import json
from collections import Counter
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


# --- the companyfacts catalogue ----------------------------------------------
#
# The record is not a filing, so the cutoff is applied to its rows. Every
# expectation below comes from the two records themselves and from the fixture
# manifests that describe them — never from a run of the guard.

COMMITTED_CATALOGUE = FIXTURES / "CARR" / "companyfacts.json.gz"
PLANTED = FIXTURES / "planted_late_row"
PLANTED_CATALOGUE = PLANTED / "CARR" / "companyfacts.json.gz"

# Carrier's 10-K, accession 0001783180-26-000008, was filed on this date: it is
# the triggering report of an annual run and therefore that run's cutoff. The
# companyfacts record is dated nearly three months later, because the date a
# catalogue carries is the newest filing whose facts are in it — the manifest
# row says so in its own `date_basis`. So this is the case the whole-file gate
# refuses and this route has to serve.
CARR_10K_FILED = dt.date(2026, 2, 5)
CATALOGUE_RECORDED_DATE = dt.date(2026, 4, 30)

# Counted from the two records, by reading the files and no code of this
# project's: 12,011 fact rows each, of which 11,676 are filed on or before the
# 10-K's date in the committed record and 11,675 in the planted copy. The one
# row of difference is the plant.
ROWS_IN_THE_RECORD = 12011
COMMITTED_ROWS_AT_THE_TRIGGER = 11676
PLANTED_ROWS_AT_THE_TRIGGER = 11675

# The planted row, as `tests/fixtures/planted_late_row/CARR/manifest.json`
# describes it: total assets at the end of 2025, reported by the 10-K itself,
# dated in the copy as if the 10-Q three months later had filed it.
PLANTED_ROW = ("us-gaap", "Assets", "USD", None, "2025-12-31",
               "0001783180-26-000008", 37190000000)
PLANTED_FILED = "2026-04-30"
COMMITTED_FILED = "2026-02-05"

GZIP_MAGIC = b"\x1f\x8b"


def rows_in_the_file(path: Path, cutoff: str | None = None) -> list[tuple]:
    """Every fact row of a companyfacts file, read here and not through `src/`.

    The file is opened by name, decompressed if its first two bytes say it is
    gzip, and walked with EDGAR's own keys. Nothing in this function comes from
    the module under test, so the rows it counts are the record's rows and not
    the guard's answer about them. `cutoff` keeps the rows filed on or before
    that date, which is the rule `CLAUDE.md` states, applied by hand.
    """
    raw = path.read_bytes()
    document = json.loads(gzip.decompress(raw) if raw[:2] == GZIP_MAGIC else raw)
    return [row for row in fact_rows(document)
            if cutoff is None or row[7] <= cutoff]


def fact_rows(document: dict) -> list[tuple]:
    """(namespace, tag, unit, start, end, accession, value, filed) for every row."""
    return [(namespace, tag, unit, row.get("start"), row["end"], row["accn"],
             row["val"], row["filed"])
            for namespace, concepts in document["facts"].items()
            for tag, concept in concepts.items()
            for unit, rows in concept["units"].items()
            for row in rows]


def test_the_planted_copy_moves_one_filing_date_and_nothing_else():
    """A copy that had drifted anywhere else would be judging something else."""
    committed = rows_in_the_file(COMMITTED_CATALOGUE)
    planted = rows_in_the_file(PLANTED_CATALOGUE)
    assert len(committed) == len(planted) == ROWS_IN_THE_RECORD
    differ = [(before, after) for before, after in zip(committed, planted)
              if before != after]
    assert differ == [(PLANTED_ROW + (COMMITTED_FILED,), PLANTED_ROW + (PLANTED_FILED,))]


def test_the_whole_file_gate_refuses_the_catalogue_at_an_annual_trigger():
    """What the route exists to replace, stated as a fact about the gate.

    Carrier's record is dated after Carrier's 10-K, so `load_bytes` refuses it
    to the annual run — and 11,675 rows the run is entitled to go with it.
    """
    assert CARR_10K_FILED < CATALOGUE_RECORDED_DATE
    with pytest.raises(CutoffViolationError) as caught:
        cutoff_guard.load_bytes(PLANTED_CATALOGUE, CARR_10K_FILED,
                                fixtures_root=PLANTED)
    assert caught.value.doc_date == CATALOGUE_RECORDED_DATE


def test_a_trigger_earlier_than_the_records_own_date_yields_the_rows_inside_it():
    """The count and the rows themselves, against the file read independently."""
    document = cutoff_guard.load_catalogue(PLANTED_CATALOGUE, CARR_10K_FILED,
                                           fixtures_root=PLANTED)
    served = fact_rows(document)
    counted = rows_in_the_file(PLANTED_CATALOGUE, str(CARR_10K_FILED))
    assert len(served) == PLANTED_ROWS_AT_THE_TRIGGER
    assert len(counted) == PLANTED_ROWS_AT_THE_TRIGGER
    # A multiset, because a record may hold the same row twice and a set would
    # collapse the pair into one and still call the two sides equal.
    assert Counter(served) == Counter(counted)


def test_the_row_filed_after_the_cutoff_does_not_reach_the_reader():
    """The plant is in the file and not in what the reader gets; the same row
    at its real date, in the committed record, is served at the same cutoff.

    A route that admitted everything would fail the first assertion and a route
    that admitted nothing would fail the last.
    """
    assert PLANTED_ROW + (PLANTED_FILED,) in rows_in_the_file(PLANTED_CATALOGUE)
    served = fact_rows(cutoff_guard.load_catalogue(PLANTED_CATALOGUE, CARR_10K_FILED,
                                                   fixtures_root=PLANTED))
    assert PLANTED_ROW + (PLANTED_FILED,) not in served
    assert PLANTED_ROW + (COMMITTED_FILED,) not in served

    committed = fact_rows(cutoff_guard.load_catalogue(COMMITTED_CATALOGUE,
                                                      CARR_10K_FILED))
    assert PLANTED_ROW + (COMMITTED_FILED,) in committed
    assert len(committed) == COMMITTED_ROWS_AT_THE_TRIGGER
    assert len(committed) - len(served) == 1


def test_a_tag_the_cutoff_leaves_with_no_row_is_dropped_and_not_left_empty():
    """A tag the 10-K introduced is not in the record the day before it.

    `IncomeTaxReconciliationTaxCreditsResearch` has one row in Carrier's record
    and the 10-K filed 2026-02-05 is what reported it, so at 2026-02-04 the tag
    exists only through a filing that has not happened. It is gone, not carried
    as a name with no rows under it — a tag present only through a later filing
    is that filing showing through.
    """
    introduced = "IncomeTaxReconciliationTaxCreditsResearch"
    day_before = cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, "2026-02-04")
    on_the_day = cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, CARR_10K_FILED)
    assert introduced not in day_before["facts"]["us-gaap"]
    assert introduced in on_the_day["facts"]["us-gaap"]
    assert "Assets" in day_before["facts"]["us-gaap"]


def test_a_cutoff_before_the_first_row_leaves_the_record_empty():
    """Carrier's first companyfacts row is filed 2020-05-11, the year it was
    spun out. A day earlier the record holds nothing, and nothing is what comes
    back — not the tags with their rows taken out from under them."""
    document = cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, "2020-05-10")
    assert document["facts"] == {}
    assert document["ticker"] == "CARR"


def test_an_unparseable_cutoff_is_refused_on_the_catalogue_route():
    """A string comparison would have admitted the whole record at exit 0:
    every ISO date sorts before the word, so nothing would have been cut."""
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, "garbage")


def test_an_absent_cutoff_is_refused_on_the_catalogue_route():
    for absent in (None, "", "   "):
        with pytest.raises(CutoffGuardError):
            cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, absent)


def test_a_document_that_is_not_a_catalogue_is_refused_on_this_route():
    index = cutoff_guard.one_document("CARR", "submissions", "submissions_index")
    for path in (index["full_path"], AAPL_10K):
        with pytest.raises(CutoffGuardError):
            cutoff_guard.load_catalogue(path, CARR_10K_FILED)


def _catalogue_tree(tmp_path: Path, rows, *, sha256=None, body=None) -> Path:
    """A one-document fixture root holding a companyfacts record of its own."""
    root = tmp_path / "fixtures"
    (root / "ZZZZ").mkdir(parents=True)
    document = {"ticker": "ZZZZ", "cik": "0000000000", "as_of": "2026-09-01",
                "facts": {"us-gaap": {"Assets": {"units": {"USD": list(rows)}}}}}
    raw = body if body is not None else json.dumps(document, indent=2).encode("utf-8")
    (root / "ZZZZ" / "companyfacts.json").write_bytes(raw)
    (root / "ZZZZ" / "manifest.json").write_text(json.dumps({
        "ticker": "ZZZZ", "as_of": "2026-09-01", "documents": [
            {"form": "companyfacts", "role": "standard_taxonomy_history",
             "accession": "", "filing_date": "2026-04-30",
             "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0000000000.json",
             "path": "companyfacts.json", "stored": "identity", "bytes": len(raw),
             "sha256": sha256 or hashlib.sha256(raw).hexdigest()}]}) + "\n")
    return root


def _row(filed, value=1, end="2025-12-31"):
    row = {"end": end, "val": value, "accn": "0000000000-00-000000",
           "fy": 2025, "fp": "FY", "form": "10-K"}
    if filed is not _MISSING:
        row["filed"] = filed
    return row


def test_a_row_with_no_filing_date_is_refused_rather_than_dropped(tmp_path):
    """An absent date is not an early date, and dropping the row quietly would
    be the same silence the whole-file refusal makes, one row at a time."""
    root = _catalogue_tree(tmp_path, [_row("2025-05-01"), _row(_MISSING, value=2)])
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_catalogue(root / "ZZZZ" / "companyfacts.json",
                                    "2026-09-01", fixtures_root=root)


def test_a_row_whose_filing_date_is_not_a_date_is_refused(tmp_path):
    root = _catalogue_tree(tmp_path, [_row("2025-05-01"), _row("1 May 2025", value=2)])
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_catalogue(root / "ZZZZ" / "companyfacts.json",
                                    "2026-09-01", fixtures_root=root)


def test_a_catalogue_nobody_recorded_is_refused(tmp_path):
    root = _catalogue_tree(tmp_path, [_row("2025-05-01")])
    stranger = root / "ZZZZ" / "not-in-the-manifest.json"
    stranger.write_bytes(b"{}")
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_catalogue(stranger, "2026-09-01", fixtures_root=root)


def test_bytes_that_are_no_longer_the_ones_the_manifest_hashed_are_refused(tmp_path):
    """The date gate vouches for every other document and this route skips it,
    so the hash is what says the file is still the record."""
    root = _catalogue_tree(tmp_path, [_row("2025-05-01")], sha256="0" * 64)
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_catalogue(root / "ZZZZ" / "companyfacts.json",
                                    "2026-09-01", fixtures_root=root)


def test_a_document_with_no_facts_object_is_refused(tmp_path):
    root = _catalogue_tree(tmp_path, [], body=b'{"ticker": "ZZZZ"}')
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_catalogue(root / "ZZZZ" / "companyfacts.json",
                                    "2026-09-01", fixtures_root=root)


def test_the_catalogue_read_is_recorded_so_a_bundle_can_list_it():
    """`assemble_bundle` builds its `documents` list out of what was opened, so
    a read this module does not record is a document the bundle cannot list."""
    with cutoff_guard.recording() as seen:
        cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, CARR_10K_FILED)
    assert seen == [COMMITTED_CATALOGUE.resolve()]


def test_a_refused_catalogue_is_not_recorded_as_opened():
    with cutoff_guard.recording() as seen:
        with pytest.raises(CutoffGuardError):
            cutoff_guard.load_catalogue(COMMITTED_CATALOGUE, "garbage")
    assert seen == []


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
