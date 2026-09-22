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

from src import (assemble_bundle, cutoff_guard, extract_notes, extract_numbers,
                 fetch_companyfacts, restatement_trace)
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


# --- the submissions index ---------------------------------------------------
#
# The other document the date gate does not apply to, and for a while the only
# one in the fixture set with no integrity check either: `load_index` skipped
# the gate the way `load_catalogue` does but never looked at the hash, so
# nothing at all said the bytes it served were the bytes that were fetched.
#
# Every expectation below is read out of the committed fixture set — the index
# file and the `sha256` that `src/fetch_fixtures.py` wrote into the manifest
# beside it — and never out of a run of the guard.

COMMITTED_INDEX = FIXTURES / "CARR" / "submissions.json"
INDEX_FORM = "submissions"


def _role_recorded_for(form: str) -> str:
    """The role the committed manifests record one form under, read from them."""
    roles = {entry["role"]
             for manifest_path in sorted(FIXTURES.glob("*/manifest.json"))
             for entry in json.loads(manifest_path.read_text(encoding="utf-8"))["documents"]
             if entry["form"] == form}
    assert len(roles) == 1, f"{form} is recorded under {sorted(roles)}"
    return roles.pop()


def _committed_index_row() -> dict:
    manifest = json.loads((FIXTURES / "CARR" / "manifest.json").read_text(encoding="utf-8"))
    return next(entry for entry in manifest["documents"]
                if entry["form"] == INDEX_FORM)


def _index_tree(root: Path, body: bytes | None = None, *, sha256=_MISSING) -> Path:
    """A fixture root holding a copy of the committed index and its own row.

    The bytes and the recorded hash both come from the fixture set. What a test
    passes here is what it changed about the copy afterwards.
    """
    row = dict(_committed_index_row())
    if sha256 is None:
        row.pop("sha256", None)
    elif sha256 is not _MISSING:
        row["sha256"] = sha256
    (root / "CARR").mkdir(parents=True)
    (root / "CARR" / row["path"]).write_bytes(
        COMMITTED_INDEX.read_bytes() if body is None else body)
    (root / "CARR" / "manifest.json").write_text(json.dumps(
        {"ticker": "CARR", "as_of": "2026-09-01", "documents": [row]}) + "\n")
    return root / "CARR" / row["path"]


def test_the_committed_index_is_served_as_the_file_on_record():
    """The route hands back the file, and the file is the one the fetcher
    hashed — read here off the disk and out of the manifest, not from the gate."""
    served = cutoff_guard.load_index(COMMITTED_INDEX)
    assert served == COMMITTED_INDEX.read_bytes()
    assert hashlib.sha256(COMMITTED_INDEX.read_bytes()).hexdigest() == \
        _committed_index_row()["sha256"]
    assert json.loads(served)["filings"]


def test_an_index_whose_bytes_no_longer_match_the_manifest_is_refused(tmp_path):
    """The date gate vouches for every other document and this route skips it,
    so here the hash is the only thing that says the file is still the record.

    The same copy is served untouched and refused with one filing's form
    changed, so it is the alteration that did it and not the copying.
    """
    untouched = _index_tree(tmp_path / "as-committed")
    assert json.loads(cutoff_guard.load_index(
        untouched, fixtures_root=untouched.parent.parent))["filings"]

    original = COMMITTED_INDEX.read_bytes()
    altered = original.replace(b'"form": "8-K"', b'"form": "S-1"', 1)
    assert altered != original and len(altered) == len(original)
    tampered = _index_tree(tmp_path / "altered", altered)
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_index(tampered, fixtures_root=tampered.parent.parent)


def test_an_index_recorded_with_no_hash_is_refused(tmp_path):
    """Nothing else on this route says the file is still the record."""
    path = _index_tree(tmp_path, sha256=None)
    with pytest.raises(CutoffGuardError):
        cutoff_guard.load_index(path, fixtures_root=path.parent.parent)


def test_a_refused_index_is_not_recorded_as_opened(tmp_path):
    """`assemble_bundle` lists what was opened, so a refusal that recorded the
    read would publish the index as a document the bundle used."""
    path = _index_tree(tmp_path, b'{"filings": []}')
    with cutoff_guard.recording() as seen:
        with pytest.raises(CutoffGuardError):
            cutoff_guard.load_index(path, fixtures_root=path.parent.parent)
    assert seen == []


def test_the_index_read_is_still_recorded_when_it_passes():
    with cutoff_guard.recording() as seen:
        cutoff_guard.load_index(COMMITTED_INDEX)
    assert seen == [COMMITTED_INDEX.resolve()]


def test_a_document_that_is_not_the_index_is_refused_on_this_route():
    for path in (COMMITTED_CATALOGUE, AAPL_10K):
        with pytest.raises(CutoffGuardError):
            cutoff_guard.load_index(path)


# --- the shape of a manifest record ------------------------------------------
#
# A record of the wrong shape used to leave the gate as whatever Python raised
# where it was touched — `ValueError` out of `dict(entry)`, `KeyError` out of
# `entry["path"]`, `AttributeError` out of `entry.get(...)`. The two readers
# catch `CutoffGuardError` and nothing else, so each of those was a traceback
# where the reader had been written to print a refusal and exit on bad input.

MALFORMED_RECORDS = {
    "a record that is a string": ["not an object at all"],
    "a record that is a list": [["10-K", "doc.htm"]],
    "a record with no path": [{"form": "10-K", "role": "primary_html",
                               "filing_date": "2025-10-31"}],
    "a record whose path is null": [{"form": "10-K", "role": "primary_html",
                                     "filing_date": "2025-10-31", "path": None}],
    "a record whose path is empty": [{"form": "10-K", "role": "primary_html",
                                      "filing_date": "2025-10-31", "path": "  "}],
    "documents that is not a list": {"10-K": "doc.htm"},
    "documents that is a string": "10-K/doc.htm",
}


def _malformed_tree(tmp_path: Path, documents) -> Path:
    root = tmp_path / "fixtures"
    (root / "ZZZZ").mkdir(parents=True)
    (root / "ZZZZ" / "manifest.json").write_text(json.dumps(
        {"ticker": "ZZZZ", "as_of": "2026-09-01", "documents": documents}) + "\n")
    return root


@pytest.mark.parametrize("shape", sorted(MALFORMED_RECORDS))
def test_a_malformed_manifest_record_raises_the_gates_own_error(tmp_path, shape):
    root = _malformed_tree(tmp_path, MALFORMED_RECORDS[shape])
    stranger = root / "ZZZZ" / "10-K" / "doc.htm"
    for call in (lambda: cutoff_guard.documents("ZZZZ", fixtures_root=root),
                 lambda: cutoff_guard.document_record(stranger, fixtures_root=root),
                 lambda: cutoff_guard.load_document(stranger, "2026-09-01",
                                                    fixtures_root=root)):
        with pytest.raises(CutoffGuardError):
            call()


@pytest.mark.parametrize("shape", sorted(MALFORMED_RECORDS))
def test_the_two_readers_report_a_malformed_record_rather_than_dying(tmp_path, shape):
    """What the wrong error type actually cost: `src/extract_numbers.py:264`
    and `src/extract_notes.py:150` catch `CutoffGuardError` and nothing else,
    so a `ValueError` from the same manifest read came out as a traceback."""
    root = _malformed_tree(tmp_path, MALFORMED_RECORDS[shape])
    out = tmp_path / "out"
    assert extract_numbers.main(
        ["--ticker", "ZZZZ", "--fixtures", str(root), "--out", str(out)]
    ) == extract_numbers.BAD_INPUT
    assert extract_notes.main(
        ["--ticker", "ZZZZ", "--fixtures", str(root), "--out", str(out)]
    ) == extract_notes.BAD_INPUT
    assert not out.exists()


# --- one spelling of the catalogue role --------------------------------------


def test_the_gate_names_the_roles_the_committed_manifests_record():
    """Both constants against the fixture set, not against each other."""
    assert cutoff_guard.CATALOGUE_ROLE == _role_recorded_for("companyfacts")
    assert cutoff_guard.INDEX_ROLE == _role_recorded_for(INDEX_FORM)


def _string_constants(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def test_the_catalogue_role_is_written_once_and_the_rest_take_it_from_there():
    """It was hand-copied into three modules with nothing holding them equal, so
    a rename was three edits and a missed one was a role nothing would match."""
    written = [path.name for path in sorted(SRC.glob("*.py"))
               if cutoff_guard.CATALOGUE_ROLE in _string_constants(path)]
    assert written == ["cutoff_guard.py"]
    assert fetch_companyfacts.ROLE == cutoff_guard.CATALOGUE_ROLE
    assert restatement_trace.COMPANYFACTS_ROLE == cutoff_guard.CATALOGUE_ROLE
    assert assemble_bundle.FACTS_ROLE == cutoff_guard.CATALOGUE_ROLE


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
