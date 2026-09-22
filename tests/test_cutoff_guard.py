"""The date gate, and the scan that says nothing walked around it.

The gate is only worth as much as the guarantee that every extractor uses it,
so the last section here is not about dates at all: it reads every module in
`src/` and fails on a read of a fixture or a bundle that does not go through
`src/cutoff_guard.py`. It follows the call into the function being called, and
follows the path back to the name it was bound to, because a scan that matched
only reads spelled out in one line let the other kind through in silence. Run
it on its own to see what it found:

    python3.12 tests/test_cutoff_guard.py
"""

from __future__ import annotations

import ast
import datetime as dt
import gzip
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

try:
    from src import cutoff_guard
except ImportError:  # run as a plain script: python3.12 tests/test_cutoff_guard.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
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
#
# The gate is worth exactly what the guarantee that everything reads through it
# is worth, so this walks every module in `src/` and fails on a read of a
# fixture or a bundle that does not. A call is a bypass when both halves below
# are true, and each half has to follow indirection or the scan's claim is true
# by indirection rather than about the code.
#
# **What this is and is not.** It reads source text: no module is imported, no
# value is evaluated, and a name is worth what the lines around it say it is
# worth. So it is a net of a stated mesh and never a proof, and the mesh is
# written out at the end of this comment rather than left to be discovered.
# What it does guarantee is that the ways around it all cost something -- a
# call boundary, a rebinding, a parameter -- where before this change the cost
# was one helper call, which is the price of nothing.
#
# **Is the call a read?** A raw `open`, `read_text`, `read_bytes` or `glob` is
# one. So is a call to a function in `src/` that reads a path it was handed:
# `fetch_fixtures.read_stored` is two `read_bytes` calls behind a name, the
# fetcher is exempt so its body is never scanned, and a module that calls it
# has read a fixture with no date gate in front of it. The reader set is grown
# to a fixed point -- a function that hands one of its own parameters to a
# known reader is a reader too -- because a list of names written here would be
# the same blindness one level up: the next helper would not be on it. The
# parameter is followed through the body as well as into the call:
# `load_manifest` builds `ticker_dir / "manifest.json"` before reading it, and
# it sits in the same module as `read_stored` and is borrowed the same way.
#
# **Is what it reads a fixture or a bundle?** The unparsed receiver and
# arguments name `fixtures` or `runs`, or a name in them stands for something
# that does. A name is followed to what it was bound to for as long as the
# names keep resolving, because `ANNUAL = ROOT / "AAPL"` is one more line than
# a single hop follows and writing that line is free. Bindings are read a scope
# at a time: `path` in one function is not `path` in the next, and a module
# read as one scope has `path` bound twice and follows neither -- which is the
# ordinary shape of a read rather than an exotic one.
#
# Two modules are not bypasses, for two different reasons. `cutoff_guard.py`
# **is** the gate, so its public functions are the sanctioned route -- but its
# private raw readers are nobody's route, and a module reaching for one of
# those has skipped the date check like any other bypass.
# `fetch_fixtures.py` builds the fixtures out of EDGAR and is upstream of the
# gate, so its own reads are exempt; the readers it exports to other modules
# are not.
#
# What is still outside this, said plainly because a scan's blind spots are
# worth as much as its findings.
#
# **The vocabulary is the mesh.** `CONTENT_READS`, `LISTINGS`, `PATH_CALLS` and
# the node kinds `_is_a_path_expression` accepts are four enumerations, and a
# way of reading a file, of making a path, or of holding one that is not in
# them is not seen. `zipfile.ZipFile`, a dataframe library's own reader, a
# descriptor, a C extension handed a path: each is invisible until its name is
# in the tuple, and adding one is a line. That is the honest shape of this
# check -- it is a list of the ways this repository writes things, kept current
# by whoever adds a new one, and never a proof that no other way exists. The
# rest of the list below is the same statement about particular shapes that
# have come up.
#
#   * A path that arrives from somewhere this module cannot see it come from:
#     a parameter its caller filled, an attribute of an object, a loop or
#     comprehension variable, a `functools.partial`, a path another function of
#     the module returns, or a name its own scope rebinds. The scan reads one
#     module and one scope at a time and follows no value across a call
#     boundary. Several places in `src/` read that way and not one of them is
#     this scan's finding, so not one of them is this scan's clean answer
#     either: `fetch_companyfacts.verify_existing`, handed a directory built
#     two frames up and reading a fixture through `read_stored`;
#     `agent_inputs`, copying and reading bundle files out of a `run` it was
#     handed; `trends`, reading `input_numbers.json` from a path off the
#     command line; and `market.read_prices` and `market.read_short_interest`,
#     which glob and read every CSV under a directory that arrives on the
#     command line and on disk is `tests/fixtures/market/`. Each has its own
#     reason written where it is:
#     `tests/test_fetch_companyfacts.py` keeps the borrowers of the fetcher's
#     helpers at one; `agent_inputs._place` says why bytes rather than
#     `load_bundle_file`, the bundle's cutoff being checked against its own
#     manifest by `src/extraction_checks.py`; and the market table is not a
#     filing -- it carries its own window rule, and the comparers are the only
#     layer that sees it.
#   * A write. A helper that opens what it is handed in order to write it is
#     not a reader, which is what keeps `fetch_fixtures.store` and everything
#     that calls it out of the report. Writing a fixture from anywhere but the
#     fetcher is a violation `tests/test_fetch_companyfacts.py` names.
#   * `cutoff_guard.load_bundle_file`. Every public function of the gate is
#     treated here as the route, and that one is the route for bundles only: it
#     opens whatever path it is handed, with no manifest lookup and no date,
#     and its own docstring says so. Handed a filing it would read the filing,
#     and this scan would not name it. It is not derivable from source text
#     either -- the gate reading its own manifest and the gate reading a
#     document it was handed are the same shape, and a rule that made the
#     unchecked readers of the gate into findings reported sixty calls that
#     read nothing, on the word `fixtures_root` in a keyword. None of the nine
#     call sites in `src/` hands it a filing today -- nine calls counted from
#     the syntax tree, not the ten lines a grep for the name returns, one of
#     which is a docstring in `src/agent_inputs.py`. A judge for that one
#     function is the next thing this scan needs, and it is not this change.
#   * A reader held as a method of a class another module defines. A method is
#     followed when the name it is called by is one this module defines or
#     imports -- `Loader().load(path)` where `load` is in this module, or a
#     lambda bound to a name here. `from src.loader import Loader` and then
#     `Loader().load(path)` is not: the name is the class's, resolving a bare
#     method name against every module in `src/` is what
#     `_reachable_readers` refuses to do, and no class in `src/` reads a file
#     through a method today.

# Reading a document's bytes. `open` covers `path.open("rb")`, `gzip.open(path)`
# -- the fixtures over 2 MB are stored gzipped, so that is a shape a fixture
# read really takes -- and the bare builtin.
# A copy is here because it moves a document's bytes past the gate exactly as
# a read does, and `shutil.copy(FIXTURES / ..., somewhere)` is one line.
COPIES = ("copy", "copy2", "copyfile", "copytree")
CONTENT_READS = ("read_text", "read_bytes", "open") + COPIES
# Listing a directory. It hands back paths and reads nothing, so it is a
# finding where a document root is spelled out -- `FIXTURES.rglob("*.htm")` is
# how a module walks the fixtures -- but it does not make the function around
# it a reader of documents. `cutoff_guard.bundle_files` lists and
# `load_bundle_file` reads; `scorecard.load_runs` lists the companies under a
# runs root it was handed and reads every run through the gate. Counting a
# listing as a read would make a reader of each of those and of everything that
# calls them.
LISTINGS = ("glob", "rglob", "iterdir", "scandir", "listdir", "walk")
READERS = CONTENT_READS + LISTINGS
# Calls that make a path out of a path. A binding to one of these is followed
# to what went into it; a call to anything else is not, because
# `payload = scan(ticker, fixtures_root=...)` names a root in its own source
# without being a path, and following that would report the ledger line written
# three lines later as a fixture read.
PATH_CALLS = ("Path", "join", "joinpath", "resolve", "absolute", "expanduser",
              "with_suffix", "with_name", "relative_to", "str", "format",
              "abspath", "realpath", "normpath", "dirname", "expandvars",
              "fspath")
# What a document is called here. Two are the roots themselves; `full_path` is
# the key `cutoff_guard.documents` puts the document's absolute path in, and it
# is how every call site in `src/` names a filing -- `row["full_path"]`, never
# a root spelled out again. A bypass written the way this repository writes
# everything else would name the row and not the root.
DOCUMENT_ROOTS = ("fixtures", "runs", "full_path")
# The gate itself. Its public functions are the route every other module is
# supposed to take, so a call to one of them is never a finding.
GATE = "cutoff_guard.py"
# The fetcher is the module that *creates* fixtures from EDGAR; it is upstream
# of the gate, not behind it. It is listed here rather than silently skipped.
EXEMPT = {GATE, "fetch_fixtures.py"}


def _parameters(function: ast.AST) -> set[str]:
    """Every name the function is handed: positional, keyword and starred."""
    args = function.args
    handed = {arg.arg for arg in args.posonlyargs + args.args + args.kwonlyargs}
    for starred in (args.vararg, args.kwarg):
        if starred is not None:
            handed.add(starred.arg)
    return handed


def _names_in(nodes) -> set[str]:
    return {name.id for node in nodes for name in ast.walk(node)
            if isinstance(name, ast.Name)}


def _own_nodes(scope: ast.AST) -> list[ast.AST]:
    """Everything inside one scope, stopping at the scopes nested in it.

    A function's own `path` is not the `path` of the function above it, and
    reading a module as one flat tree makes two of them into a name bound
    twice -- which the follower then drops, at the exact shape a read is most
    likely to have.
    """
    nodes, stack = [], list(ast.iter_child_nodes(scope))
    while stack:
        node = stack.pop()
        nodes.append(node)
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            stack.extend(ast.iter_child_nodes(node))
    return nodes


def _module_aliases(tree: ast.Module) -> dict[str, str]:
    """The word each module is spelled as here, mapped back to its own name.

    `import src.fetch_fixtures as fetcher`, `from src import fetch_fixtures as
    fetcher` and `fetcher = src.fetch_fixtures` all put the same function
    behind a word of the module's choosing, and the word a module chose must
    not be what decides whether the read is seen.
    """
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name] = alias.name.rsplit(".", 1)[-1]
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                aliases[alias.asname or alias.name] = alias.name
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, (ast.Name, ast.Attribute))):
            aliases[node.targets[0].id] = _spelled(node.value)
    return aliases


def _spelled(node: ast.AST) -> str:
    """The last word of a dotted name: what `src.fetch_fixtures` is called."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _owner(node: ast.AST, aliases: dict[str, str]) -> str:
    """The module a dotted call is reaching into, under its own name.

    `fetch_fixtures.read_stored`, `src.fetch_fixtures.read_stored` and
    `fetcher.read_stored` behind an aliased import are one function.
    """
    spelled = _spelled(node)
    return aliases.get(spelled, spelled)


def _read_parts(node: ast.Call, reachable: set[str], readers: dict[str, set[str]],
                aliases: dict[str, str], shapes=READERS) -> list[ast.AST] | None:
    """The parts of a call that say what it reads, or None if it reads nothing.

    `reachable` is the set of bare names this module can call to land in a
    reader -- the ones it defines, the ones it imports and the ones it binds to
    one. `readers` maps a reader's name to the modules defining one, which is
    what resolves the qualified spelling `fetch_fixtures.read_stored(...)`.
    `shapes` is `CONTENT_READS` where a listing must not count.
    """
    func = node.func
    handed = list(node.args) + [keyword.value for keyword in node.keywords]
    if isinstance(func, ast.Name) and func.id == "open":
        return handed
    if isinstance(func, ast.Attribute) and func.attr in shapes:
        return [func.value] + handed
    if isinstance(func, ast.Name) and func.id in reachable:
        return handed
    if isinstance(func, ast.Attribute) and _owner(func.value, aliases) + ".py" in (
            readers.get(func.attr, ())):
        return handed
    # A reader held as a method: `Loader().load(path)` reaches the same body as
    # `load(path)`, and the receiver is an instance rather than a module, so
    # there is no module name to resolve. The name is enough when it is a
    # reader *this* module defines or imports -- a class from another module
    # brings its method name with it and is outside this, as the residual list
    # above says.
    if isinstance(func, ast.Attribute) and func.attr in reachable:
        return handed
    return None


FILE_MODES = set("rwaxbt+")


def _writes(node: ast.Call) -> bool:
    """An `open` in a writing mode. It touches a document but reads none.

    The mode is recognised by being one -- `wb`, `a`, `x` -- rather than by
    where it sits, because `path.open("wb")` and `gzip.open(path, "wb")` put it
    in different places. Only an `open` is asked: any other call may be handed
    a string of its own, and `read_stored(where, "raw")` is three letters that
    all spell modes and no mode at all.

    This is what keeps `fetch_fixtures.store` out of the reader set: it opens
    the path it is handed in order to write it, and a module that borrows it
    has written a fixture rather than read one. Writing a fixture from anywhere
    but the fetcher is its own violation, and the borrower list in
    `tests/test_fetch_companyfacts.py` is what catches it.
    """
    if _spelled(node.func) != "open":
        return False
    spelled = [arg.value for arg in node.args if isinstance(arg, ast.Constant)]
    spelled += [keyword.value.value for keyword in node.keywords
                if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant)]
    modes = [word for word in spelled
             if isinstance(word, str) and word and set(word) <= FILE_MODES]
    return any(set(mode) & set("wax") for mode in modes)


def _reachable_readers(module: str, tree: ast.Module, readers: dict[str, set[str]],
                       aliases: dict[str, str]) -> set[str]:
    """The bare names this module can call to reach a reader.

    Its own functions, the ones it imports, and the ones it binds a reader to.
    Resolving a bare name against every module in `src/` instead would make two
    unrelated functions that happen to share a name into one: `run` reads a
    path it is handed in `control_single_agent.py` and reads nothing in
    `extraction_checks.py`.
    """
    reachable = {name for name, modules in readers.items() if module in modules}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            origin = (node.module or "").rsplit(".", 1)[-1] + ".py"
            for alias in node.names:
                if alias.name == "*":
                    reachable |= {name for name, modules in readers.items()
                                  if origin in modules}
                elif origin in readers.get(alias.name, ()):
                    reachable.add(alias.asname or alias.name)
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            bound_to = node.value
            if isinstance(bound_to, ast.Name) and bound_to.id in reachable:
                reachable.add(node.targets[0].id)
            elif isinstance(bound_to, ast.Attribute) and _owner(
                    bound_to.value, aliases) + ".py" in readers.get(bound_to.attr, ()):
                reachable.add(node.targets[0].id)
    return reachable


def _readers(modules: dict[str, ast.Module]) -> dict[str, set[str]]:
    """Every function in `src/` that reads a path it was handed, by name.

    Grown until it stops growing: a function that passes one of its parameters
    to a reader is a reader, however many names deep the chain runs. The gate's
    public functions are left out because they are the route; its private ones
    are left in because `cutoff_guard._read` opens a file with no date check in
    front of it and was never a route for anyone else.
    """
    functions = [(name, function.name, function) for name, tree in modules.items()
                 for function in ast.walk(tree)
                 if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))]
    # A lambda is a function with the name of whatever it was assigned to.
    functions += [(name, target, node.value)
                  for name, tree in modules.items() for node in ast.walk(tree)
                  if isinstance(node, ast.Assign) and isinstance(node.value, ast.Lambda)
                  for target in _names_in(node.targets)]
    aliases = {name: _module_aliases(tree) for name, tree in modules.items()}
    readers: dict[str, set[str]] = {}
    growing = True
    while growing:
        growing = False
        reachable = {name: _reachable_readers(name, tree, readers, aliases[name])
                     for name, tree in modules.items()}
        for module, called, function in functions:
            if module == GATE and not called.startswith("_"):
                continue
            if module in readers.get(called, ()):
                continue
            handed = _parameters(function)
            own = _own_nodes(function)
            bound = {**_bound_once(own), **_parameter_defaults(function)}
            # Calls from the whole body, nested definitions included: a closure
            # reads the parameter of the function around it, and `def go():
            # return where.read_bytes()` inside the helper reads exactly what
            # the helper was handed.
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                parts = _read_parts(node, reachable[module], readers, aliases[module],
                                    CONTENT_READS)
                if parts and not _writes(node) and _names_in(
                        _followed(parts, bound)) & handed:
                    readers.setdefault(called, set()).add(module)
                    growing = True
                    break
    return readers


def _is_a_path_expression(node: ast.AST) -> bool:
    """Something that could be a path: a `/` join, a `Path(...)` or a
    `join(...)`, a string or an f-string, or a name or attribute standing for
    one.

    A call of any other kind is not followed. `payload = scan(ticker,
    fixtures_root=...)` names a root in its own source without being a path,
    and following it would report the ledger line written three lines later as
    a fixture read. A string is followed, because `"tests/fixtures/..."` in a
    constant is the same path spelled without `Path` and has no such cost.
    """
    # `/` joins two paths; `+` and `%` join two strings that are one.
    if isinstance(node, ast.BinOp):
        return isinstance(node.op, (ast.Div, ast.Add, ast.Mod))
    if isinstance(node, ast.Call):
        return _spelled(node.func) in PATH_CALLS
    if isinstance(node, ast.Constant):
        return isinstance(node.value, str)
    # A root kept in a dictionary, a list, or on one side of a conditional.
    if isinstance(node, (ast.Dict, ast.List, ast.Tuple, ast.IfExp)):
        return True
    # A subscript because `where = row["full_path"]` is how a filing's path is
    # taken out of a manifest row, and one binding is the whole distance
    # between that and a read that says nothing.
    return isinstance(node, (ast.Name, ast.Attribute, ast.JoinedStr, ast.Subscript))


def _one_at_a_time(target: ast.AST, value: ast.AST) -> list[tuple[str, ast.AST]]:
    """One assignment as the name-and-value pairs it really is.

    `annual, quarterly = FIXTURES / ..., FIXTURES / ...` binds two names on one
    line, and a rule that read only a bare target would leave both unfollowed.
    """
    if isinstance(target, ast.Name):
        return [(target.id, value)]
    if (isinstance(target, (ast.Tuple, ast.List))
            and isinstance(value, (ast.Tuple, ast.List))
            and len(target.elts) == len(value.elts)):
        return [(name.id, element) for name, element in zip(target.elts, value.elts)
                if isinstance(name, ast.Name)]
    return []


def _bound_once(nodes) -> dict[str, ast.AST]:
    """Names bound to a path exactly once in one scope, and what they hold.

    One binding only: a name rebound in a loop has no single source line that
    can stand for it. One scope only, so the same local name in two functions
    is two names rather than one name bound twice.
    """
    bound: dict[str, list[ast.AST]] = {}
    for node in nodes:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            for name, value in _one_at_a_time(node.targets[0], node.value):
                bound.setdefault(name, []).append(value)
        elif (isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
                and node.value is not None):
            bound.setdefault(node.target.id, []).append(node.value)
    return {name: values[0] for name, values in bound.items()
            if len(values) == 1 and _is_a_path_expression(values[0])}


def _followed(parts, bound: dict[str, ast.AST]) -> list[ast.AST]:
    """The read's own parts, plus everything the names in them stand for.

    For as long as the names keep resolving, not one hop:
    `ANNUAL = FIXTURES / "AAPL"` and then `ANNUAL / "10-K" / "doc.htm"` is two,
    and stopping at one would let the second line be the hiding place the first
    line no longer is.
    """
    reached, names, seen = list(parts), _names_in(parts), set()
    while names - seen:
        name = (names - seen).pop()
        seen.add(name)
        if name in bound:
            reached.append(bound[name])
            names |= _names_in([bound[name]])
    return reached


def _every_name_bound(nodes) -> set[str]:
    """Every name this scope assigns, however and however often."""
    targets = []
    for node in nodes:
        if isinstance(node, (ast.Assign, ast.For, ast.AsyncFor, ast.comprehension)):
            targets += node.targets if isinstance(node, ast.Assign) else [node.target]
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            targets.append(node.target)
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            targets.append(node.optional_vars)
    return _names_in(targets)


def _parameter_defaults(function: ast.AST) -> dict[str, ast.AST]:
    """A default argument is a binding the enclosing scope wrote.

    `def annual_report(ticker, root=FIXTURES)` says what `root` is for every
    caller that leaves it out, and `src/assemble_bundle.py` writes exactly that
    shape. Reading only the body would leave the read looking rootless.
    """
    args = function.args
    positional = args.posonlyargs + args.args
    pairs = list(zip(positional[len(positional) - len(args.defaults):], args.defaults))
    pairs += [(arg, value) for arg, value in zip(args.kwonlyargs, args.kw_defaults)
              if value is not None]
    return {arg.arg: value for arg, value in pairs if _is_a_path_expression(value)}


def _scopes(tree: ast.Module):
    """Each scope of a module, with the path names a read in it can follow.

    A function sees what it binds itself and what the module binds around it,
    and nothing a sibling function binds.
    """
    pending = [(tree, {})]
    while pending:
        scope, inherited = pending.pop()
        own = _own_nodes(scope)
        # A name this scope assigns is this scope's name, whether or not it was
        # assigned once and whether or not the outer scope has one too. Letting
        # the outer binding stand in would answer for a local the scope rebinds
        # -- with a path that is not the one being read.
        shadowed = _every_name_bound(own)
        bound = {name: value for name, value in inherited.items()
                 if name not in shadowed}
        bound.update(_bound_once(own))
        yield own, bound
        for node in own:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                pending.append((node, {**bound, **_parameter_defaults(node)}))
            elif isinstance(node, ast.ClassDef):
                pending.append((node, bound))


def _names_a_document_root(parts, bound: dict[str, ast.AST],
                           aliases: dict[str, str]) -> bool:
    """Does what is being read sit under the fixtures or the published runs?

    The aliases are read too: `from src.cutoff_guard import FIXTURES as ROOT`
    leaves a read that says `ROOT`, and the import line is where it says what
    that is.
    """
    followed = _followed(parts, bound)
    written = " ".join(ast.unparse(part) for part in followed)
    under = " ".join(aliases.get(name, "") for name in _names_in(followed))
    haystack = f"{written} {under}".lower()
    return any(root in haystack for root in DOCUMENT_ROOTS)


def bypass_scan(src_dir: Path = SRC) -> list[str]:
    """One line per read of a fixture or a bundle that skips the gate."""
    src_dir = Path(src_dir)
    modules = {path.name: ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
               for path in sorted(src_dir.glob("*.py"))}
    readers = _readers(modules)
    found = []
    for name, tree in modules.items():
        if name in EXEMPT:
            continue
        aliases = _module_aliases(tree)
        reachable = _reachable_readers(name, tree, readers, aliases)
        for own, bound in _scopes(tree):
            for node in own:
                if not isinstance(node, ast.Call):
                    continue
                parts = _read_parts(node, reachable, readers, aliases)
                if parts and _names_a_document_root(parts, bound, aliases):
                    found.append((name, node.lineno, ast.unparse(node)))
    return [f"{src_dir.name}/{module}:{line}: {call}" for module, line, call
            in sorted(set(found))]


def test_no_module_reads_a_fixture_or_a_bundle_behind_the_gate():
    found = bypass_scan()
    assert not found, "reads that skip src/cutoff_guard.py:\n" + "\n".join(found)


# --- what the scan does and does not see -------------------------------------
#
# Every plant below is a module that could be dropped into `src/` tomorrow. The
# gate and the fetcher are copied in beside it rather than stubbed, so the scan
# works out what `read_stored` does by reading the function this project ships
# and not a stand-in written to be caught.
#
# What each of these is worth was established by running every one of them
# against the scan as it stood on the commit this branch starts from. Of the
# thirty plants it named three -- the read spelled out in one line, the two
# opens in `THROUGH_AN_OPEN_IN_BINARY_MODE`, and the spelled-out open in
# `A_FIXTURE_BEING_WRITTEN` -- and was silent on the other twenty-seven, which
# are the twenty-five bypasses reached by indirection plus the two that are
# not bypasses at all. So the expected values here are of two kinds and neither
# comes from the scan below: the silence a bypass used to meet, and the finding
# a shape already produced and must go on producing.

THROUGH_THE_FETCHERS_READER = '''
from pathlib import Path

from src import cutoff_guard, fetch_fixtures

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    row = cutoff_guard.one_document(ticker, "10-K", "primary_html")
    return fetch_fixtures.read_stored(FIXTURES / ticker / row["path"], row["stored"])
'''

THROUGH_A_HELPER_IN_THE_SAME_MODULE = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def _slurp(where):
    return where.read_bytes()


def annual_report(ticker):
    return _slurp(FIXTURES / ticker / "10-K" / "doc.htm")
'''

THROUGH_A_LOCAL_NAME = '''
from pathlib import Path

from src import fetch_fixtures

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
ANNUAL = FIXTURES / "AAPL" / "10-K" / "aapl-20250927.htm"


def annual_report():
    return fetch_fixtures.read_stored(ANNUAL, "identity")
'''

THROUGH_THE_FETCHER_SPELLED_OUT_IN_FULL = '''
from pathlib import Path

import src.fetch_fixtures

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    return src.fetch_fixtures.read_stored(FIXTURES / ticker / "10-K" / "doc.htm",
                                          "identity")
'''

THROUGH_A_BORROWED_HELPER_THAT_BUILDS_ITS_OWN_PATH = '''
from pathlib import Path

from src.fetch_fixtures import load_manifest

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def documents(ticker):
    return load_manifest(FIXTURES / ticker)["documents"]
'''

THROUGH_AN_ALIASED_FETCHER = '''
from pathlib import Path

import src.fetch_fixtures as fetcher

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    return fetcher.read_stored(FIXTURES / ticker / "10-K" / "doc.htm", "identity")
'''

A_NAME_THAT_ANOTHER_FUNCTION_ALSO_BINDS = '''
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    path = ROOT / ticker / "10-K" / "doc.htm"
    return path.read_bytes()


def scratch_copy(ticker, workspace):
    path = workspace / ticker
    return path.read_bytes()
'''

THROUGH_TWO_BINDINGS = '''
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
ANNUAL = ROOT / "AAPL"


def annual_report():
    return (ANNUAL / "10-K" / "aapl-20250927.htm").read_bytes()
'''

A_WALK_OF_THE_FIXTURES = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def every_annual_report():
    return [document.read_bytes() for document in FIXTURES.rglob("10-K/*.htm")]


def one_companys_reports(ticker):
    for document in (FIXTURES / ticker / "10-K").iterdir():
        yield document.read_bytes()
'''

THROUGH_AN_OPEN_IN_BINARY_MODE = '''
import gzip
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    with (FIXTURES / ticker / "10-K" / "doc.htm").open("rb") as document:
        return document.read()


def companyfacts(ticker):
    return gzip.open(FIXTURES / ticker / "companyfacts.json.gz").read()
'''

A_STAR_IMPORT_OF_THE_FETCHER = '''
from pathlib import Path

from src.fetch_fixtures import *

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    return read_stored(FIXTURES / ticker / "10-K" / "doc.htm", "identity")
'''

AN_OPEN_NAMED_BY_KEYWORD = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    return open(file=FIXTURES / ticker / "10-K" / "doc.htm", mode="rb").read()
'''

A_PAIR_BOUND_IN_ONE_LINE = '''
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
ANNUAL, QUARTERLY = ROOT / "AAPL" / "10-K", ROOT / "AAPL" / "10-Q"


def annual_report():
    return (ANNUAL / "aapl-20250927.htm").read_bytes()
'''

A_FIXTURE_BEING_WRITTEN = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def _spill(where, raw):
    with where.open("wb") as file:
        file.write(raw)


def keep_a_copy(ticker, raw):
    _spill(FIXTURES / ticker / "10-K" / "doc.htm", raw)


def keep_a_copy_here(ticker, raw):
    (FIXTURES / ticker / "10-K" / "doc.htm").open("wb").write(raw)
'''

A_PATH_SPELLED_AS_A_STRING = '''
import os
from pathlib import Path

ROOT = "tests/fixtures"


def annual_report(ticker):
    return open(os.path.join(ROOT, ticker, "10-K", "doc.htm"), "rb").read()


def quarterly_report(ticker):
    return Path(f"{ROOT}/{ticker}/10-Q/doc.htm").read_bytes()


def eight_k():
    where = "tests/fixtures/AAPL/8-K/doc.htm"
    return open(where, "rb").read()
'''

A_DEFAULT_ARGUMENT_THAT_IS_THE_FIXTURE_ROOT = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker, root=FIXTURES):
    return (root / ticker / "10-K" / "doc.htm").read_bytes()
'''

A_READER_HELD_AS_A_METHOD_AND_AS_A_LAMBDA = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


class Loader:
    def load(self, where):
        return where.read_bytes()


slurp = lambda where: where.read_bytes()


def annual_report(ticker):
    return Loader().load(FIXTURES / ticker / "10-K" / "doc.htm")


def quarterly_report(ticker):
    return slurp(FIXTURES / ticker / "10-Q" / "doc.htm")
'''

A_HELPER_HANDED_A_WORD_THAT_READS_LIKE_A_MODE = '''
from pathlib import Path

from src import fetch_fixtures

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def _slurp(where):
    return fetch_fixtures.read_stored(where, "raw")


def annual_report(ticker):
    return _slurp(FIXTURES / ticker / "10-K" / "doc.htm")
'''

A_LOCAL_NAME_REBOUND_OVER_A_MODULE_NAME = '''
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "map.json"


def sector_map():
    return path.read_text(encoding="utf-8")


def scratch(ticker, workspace):
    path = workspace / ticker
    path = path.with_suffix(".json")
    return path.read_text()
'''

THROUGH_A_ROW_FROM_THE_GATE = '''
from src import cutoff_guard, fetch_fixtures


def annual_report(ticker):
    row = cutoff_guard.one_document(ticker, "10-K", "primary_html")
    return fetch_fixtures.read_stored(row["full_path"], row["stored"])
'''

A_ROOT_JOINED_WITHOUT_A_SLASH = '''
import os
from pathlib import Path

ROOT = os.path.abspath("tests/fixtures")
ROOTS = {"annual": ROOT + "/AAPL/10-K"}


def annual_report():
    return open(ROOTS["annual"] + "/doc.htm", "rb").read()


def quarterly_report(ticker):
    where = "%s/%s/10-Q/doc.htm" % (ROOT, ticker)
    return Path(where).read_bytes()


def every_report():
    return [name for name in os.walk(ROOT)]
'''

A_ROW_PATH_PUT_IN_A_NAME_FIRST = '''
from src import cutoff_guard, fetch_fixtures


def annual_report(ticker):
    row = cutoff_guard.one_document(ticker, "10-K", "primary_html")
    where = row["full_path"]
    return fetch_fixtures.read_stored(where, row["stored"])


def quarterly_report(ticker):
    row = cutoff_guard.one_document(ticker, "10-Q", "primary_html")
    where = row["full_path"]
    return where.read_bytes()
'''

A_READ_INSIDE_A_NESTED_FUNCTION = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def _slurp(where):
    def go():
        return where.read_bytes()

    return go()


def annual_report(ticker):
    return _slurp(FIXTURES / ticker / "10-K" / "doc.htm")
'''

A_ROOT_RESHAPED_BY_ITS_OWN_METHODS = '''
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.joinpath("tests", "fixtures")


def annual_report(ticker):
    where = str(ROOT / ticker / "10-K" / "doc.htm")
    return open(where, "rb").read()


def quarterly_report(ticker):
    return (ROOT / ticker / "10-Q" / "doc").with_suffix(".htm").read_bytes()
'''

THE_GATES_OWN_ROOT_UNDER_ANOTHER_NAME = '''
from src.cutoff_guard import FIXTURES as ROOT


def annual_report(ticker):
    return (ROOT / ticker / "10-K" / "doc.htm").read_bytes()
'''

A_FIXTURE_COPIED_OUT = '''
import shutil
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def keep_a_copy(ticker, workspace):
    shutil.copy(FIXTURES / ticker / "10-K" / "doc.htm", workspace / "doc.htm")
'''

THROUGH_THE_GATES_PRIVATE_READER = '''
from pathlib import Path

from src import cutoff_guard

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    return cutoff_guard._read(FIXTURES / ticker / "10-K" / "doc.htm",
                              {"stored": "identity"})
'''

A_PLAIN_READ = '''
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker):
    return (FIXTURES / ticker / "10-K" / "doc.htm").read_bytes()
'''

THROUGH_THE_GATE = '''
from pathlib import Path

from src import cutoff_guard

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def annual_report(ticker, cutoff):
    row = cutoff_guard.one_document(ticker, "10-K", "primary_html")
    return cutoff_guard.load_document(FIXTURES / ticker / row["path"], cutoff)
'''

NOT_A_DOCUMENT_AT_ALL = '''
from pathlib import Path

from src import fetch_fixtures

MAP_PATH = Path(__file__).resolve().parent / "sic_to_sector_etf_map_v0.1.json"


def sector_map():
    return fetch_fixtures.read_stored(MAP_PATH, "identity")
'''


def _planted_src(tmp_path: Path, name: str, body: str) -> Path:
    """A `src/` tree: one planted module beside the real ones it reads through."""
    src = tmp_path / "src"
    src.mkdir()
    for module in sorted(EXEMPT):
        shutil.copy(SRC / module, src / module)
    (src / f"{name}.py").write_text(body, encoding="utf-8")
    return src


def _found_in_the_plant(tmp_path: Path, body: str) -> list[str]:
    """The scan's whole answer for a tree holding one planted module.

    Unfiltered on purpose: the two modules copied in beside it are the exempt
    ones, so everything reported here is about the plant, and a run where the
    exemption stopped working would say so instead of being filtered away.
    """
    return bypass_scan(_planted_src(tmp_path, "annual_reader", body))


def test_a_read_through_the_fetchers_reader_is_named(tmp_path):
    """The read the scan could not see, and why it could not see it.

    Nothing in this plant goes through the date gate: `one_document` hands back
    a manifest row and checks no cutoff, and the bytes then come out of
    `read_stored`, which is `read_bytes` behind a name in a module the scan
    skips. The scan as it stood read the call rather than what the call is made
    of, called `src/` clean, and the claim that no read skips the gate was true
    only of reads spelled out in one line.
    """
    found = _found_in_the_plant(tmp_path, THROUGH_THE_FETCHERS_READER)
    assert len(found) == 1, found
    assert "read_stored" in found[0]


def test_a_read_through_the_fetcher_spelled_out_in_full_is_named(tmp_path):
    """`src.fetch_fixtures.read_stored` and `fetch_fixtures.read_stored` are
    one function. Which spelling a module reaches for is an import style and
    must not be the thing that decides whether the read is seen."""
    found = _found_in_the_plant(tmp_path, THROUGH_THE_FETCHER_SPELLED_OUT_IN_FULL)
    assert len(found) == 1, found
    assert "read_stored" in found[0]


def test_a_read_through_a_helper_in_the_same_module_is_named(tmp_path):
    """A private one-line helper is the cheapest way around a scan that only
    matches the reader's own spelling, and it needs no import to arrange."""
    found = _found_in_the_plant(tmp_path, THROUGH_A_HELPER_IN_THE_SAME_MODULE)
    assert len(found) == 1, found
    assert "_slurp" in found[0]


def test_a_read_whose_path_arrived_through_a_module_name_is_named(tmp_path):
    """The argument says `ANNUAL`, which names no root the scan looks for. The
    binding one line up is what makes it a fixture."""
    found = _found_in_the_plant(tmp_path, THROUGH_A_LOCAL_NAME)
    assert len(found) == 1, found
    assert "read_stored" in found[0]


def test_a_read_through_a_borrowed_helper_that_builds_its_own_path_is_named(tmp_path):
    """`load_manifest` is handed a directory and reads the file inside it, so
    the path it was given reaches the read one binding later. It sits in the
    same module as `read_stored` and is borrowed the same way, and following
    the parameter only as far as the read call itself would have found the one
    and walked past the other."""
    found = _found_in_the_plant(
        tmp_path, THROUGH_A_BORROWED_HELPER_THAT_BUILDS_ITS_OWN_PATH)
    assert len(found) == 1, found
    assert "load_manifest" in found[0]


def test_a_read_through_a_fetcher_under_another_name_is_named(tmp_path):
    """`import src.fetch_fixtures as fetcher` is the same function under a word
    the module picked. Resolving only the word written at the call site would
    let any module out of the scan by renaming its import."""
    found = _found_in_the_plant(tmp_path, THROUGH_AN_ALIASED_FETCHER)
    assert len(found) == 1, found
    assert "read_stored" in found[0]


def test_a_local_name_another_function_also_binds_is_still_followed(tmp_path):
    """`path` in one function is not `path` in the next.

    Read as one scope, a module with two functions that each bind `path` has a
    name bound twice, which the follower drops -- and dropping it is the
    ordinary case rather than the exotic one. Only the fixture read is a
    finding; the one under a workspace handed in is not.
    """
    found = _found_in_the_plant(tmp_path, A_NAME_THAT_ANOTHER_FUNCTION_ALSO_BINDS)
    assert len(found) == 1, found
    assert "path.read_bytes()" in found[0]


def test_a_path_built_out_of_two_names_is_named(tmp_path):
    """One hop is a limit an extra line walks past: `ANNUAL = ROOT / "AAPL"`
    and the read says neither `fixtures` nor `ROOT`."""
    found = _found_in_the_plant(tmp_path, THROUGH_TWO_BINDINGS)
    assert len(found) == 1, found
    assert "read_bytes" in found[0]


def test_walking_the_fixtures_is_named_where_the_walk_is_written(tmp_path):
    """`rglob` and `iterdir` are how a module reaches documents it does not
    name one at a time. The read that follows is on a loop variable that stands
    for no root, so the walk itself is the line that has to be seen."""
    found = _found_in_the_plant(tmp_path, A_WALK_OF_THE_FIXTURES)
    assert len(found) == 2, found
    assert "rglob" in found[0] and "iterdir" in found[1]


def test_a_read_through_an_open_is_named(tmp_path):
    """`path.open("rb")` and `gzip.open(path)` are reads, and the scan this one
    replaces named both. Fixtures over two megabytes are stored gzipped, so
    `gzip.open` is not a hypothetical shape here. This is the plant that keeps
    a narrowing of what counts as a read from passing as a widening."""
    found = _found_in_the_plant(tmp_path, THROUGH_AN_OPEN_IN_BINARY_MODE)
    assert len(found) == 2, found
    assert ".open('rb')" in found[0] and "gzip.open" in found[1]


def test_a_read_through_a_star_import_of_the_fetcher_is_named(tmp_path):
    """`from src.fetch_fixtures import *` names no function at all, and a rule
    that matched imported names one by one would let the read through on the
    one import style that lists none of them."""
    found = _found_in_the_plant(tmp_path, A_STAR_IMPORT_OF_THE_FETCHER)
    assert len(found) == 1, found
    assert "read_stored" in found[0]


def test_an_open_whose_path_is_a_keyword_argument_is_named(tmp_path):
    """`open(file=..., mode="rb")` puts the path in a keyword, and reading only
    the positional arguments would make the keyword spelling the way out."""
    found = _found_in_the_plant(tmp_path, AN_OPEN_NAMED_BY_KEYWORD)
    assert len(found) == 1, found
    assert "10-K" in found[0]


def test_a_name_bound_beside_another_on_one_line_is_followed(tmp_path):
    """Two names bound in one statement are two bindings, and a rule that read
    only a bare target would follow neither."""
    found = _found_in_the_plant(tmp_path, A_PAIR_BOUND_IN_ONE_LINE)
    assert len(found) == 1, found
    assert "read_bytes" in found[0]


def test_writing_a_fixture_is_named_where_it_is_written_and_nowhere_else(tmp_path):
    """The scan is conservative about the open it can see and strict about what
    it calls a reader.

    An open of a fixture is reported whatever its mode, because the line names
    a document root and the scan does not decide from here what a module meant
    by it. But a helper that opens what it is handed in order to write it is
    not a reader, so the call into `_spill` is not a second finding -- and that
    is the same rule that keeps `fetch_fixtures.store` out of the reader set
    and every module that calls it out of this report. Writing a fixture
    outside the fetcher is a violation of its own, and
    `tests/test_fetch_companyfacts.py` is what names it.
    """
    found = _found_in_the_plant(tmp_path, A_FIXTURE_BEING_WRITTEN)
    assert len(found) == 1, found
    assert ".open('wb')" in found[0]


def test_a_path_spelled_as_a_string_is_followed(tmp_path):
    """A path does not have to be a `Path` to be one.

    `ROOT = "tests/fixtures"` joined with `os.path.join`, the same root in an
    f-string, and a whole path in one string constant: none of the three says
    `fixtures` at the read, all three say it one name away, and a follower that
    only accepted `/` joins and `Path(...)` would stop at the name.
    """
    found = _found_in_the_plant(tmp_path, A_PATH_SPELLED_AS_A_STRING)
    assert len(found) == 3, found


def test_a_default_argument_that_names_the_fixture_root_is_followed(tmp_path):
    """`def annual_report(ticker, root=FIXTURES)` binds `root` for every caller
    that leaves it out, and the body then reads a path that says nothing about
    where it is. `src/assemble_bundle.py` is written in this shape."""
    found = _found_in_the_plant(tmp_path, A_DEFAULT_ARGUMENT_THAT_IS_THE_FIXTURE_ROOT)
    assert len(found) == 1, found
    assert "read_bytes" in found[0]


def test_a_reader_held_as_a_method_or_a_lambda_is_named(tmp_path):
    """A reader does not stop being one for being reached through an instance
    or written on one line. `Loader().load(path)` has no module name to
    resolve, and a lambda has no `def` to find it by."""
    found = _found_in_the_plant(tmp_path, A_READER_HELD_AS_A_METHOD_AND_AS_A_LAMBDA)
    assert len(found) == 2, found
    assert "Loader().load" in found[0] and "slurp" in found[1]


def test_a_word_that_reads_like_a_mode_does_not_make_a_reader_a_writer(tmp_path):
    """`read_stored(where, "raw")` hands over an encoding, and `raw` is three
    letters that are all file modes. Asking about the mode anywhere but an
    `open` would drop this helper out of the reader set and the read with it.
    """
    found = _found_in_the_plant(tmp_path, A_HELPER_HANDED_A_WORD_THAT_READS_LIKE_A_MODE)
    assert len(found) == 1, found
    assert "_slurp" in found[0]


def test_a_local_name_shadows_the_module_name_it_reuses(tmp_path):
    """The module's `path` is a fixture; the local `path` is a scratch file
    rebound twice. The read in `sector_map` is a finding and the read in
    `scratch` is not, because a name a scope assigns is that scope's name --
    inheriting the outer one would answer for a local with a path nobody read.
    """
    found = _found_in_the_plant(tmp_path, A_LOCAL_NAME_REBOUND_OVER_A_MODULE_NAME)
    assert len(found) == 1, found
    # The two reads are told apart by the read itself, because a count of one
    # is satisfied by either of them and a judge that cannot say which is no
    # judge at all.
    assert found[0].endswith("path.read_text(encoding='utf-8')")


def test_a_read_of_a_path_the_gate_handed_back_is_named(tmp_path):
    """The bypass as this repository would actually write it.

    Nothing in `src/` spells a fixture root at a read: `cutoff_guard.documents`
    hands back rows carrying `full_path`, and every call site names the row.
    `one_document` checks no cutoff -- it is the manifest, not the gate -- so a
    module that takes its `full_path` to `read_stored` has the whole filing
    with no date check anywhere behind it, and the read says `row` and nothing
    about where `row` came from.
    """
    found = _found_in_the_plant(tmp_path, THROUGH_A_ROW_FROM_THE_GATE)
    assert len(found) == 1, found
    assert "read_stored" in found[0] and "full_path" in found[0]


def test_a_root_joined_without_a_slash_is_followed(tmp_path):
    """Not every path is built with `/` and `Path`.

    `os.path.abspath`, a root kept in a dictionary, `+`, `%` and `os.walk` are
    all one line each, and a follower that knew only `/` joins would take the
    three reads here for reads of nothing.
    """
    found = _found_in_the_plant(tmp_path, A_ROOT_JOINED_WITHOUT_A_SLASH)
    assert len(found) == 3, found
    assert "os.walk" in found[2]


def test_a_row_path_put_in_a_name_first_is_still_named(tmp_path):
    """One line away from the shape above: `where = row["full_path"]`, and then
    a read that says `where`. Both the borrowed reader and a plain
    `read_bytes` land there, and the borrower list in
    `tests/test_fetch_companyfacts.py` only ever sees the first of them."""
    found = _found_in_the_plant(tmp_path, A_ROW_PATH_PUT_IN_A_NAME_FIRST)
    assert len(found) == 2, found
    assert "read_stored" in found[0] and "read_bytes" in found[1]


def test_a_read_inside_a_nested_function_makes_its_helper_a_reader(tmp_path):
    """A closure reads the parameter of the function around it. Stopping at the
    nested `def` would make the helper a non-reader and its caller invisible,
    which is one `def` for the whole of this scan."""
    found = _found_in_the_plant(tmp_path, A_READ_INSIDE_A_NESTED_FUNCTION)
    assert len(found) == 1, found
    assert "_slurp" in found[0]


def test_a_root_reshaped_by_its_own_methods_is_followed(tmp_path):
    """`joinpath`, `resolve`, `str` and `with_suffix` all make a path out of a
    path. Following only `/` and `Path(...)` would stop at the first of them,
    and each is one line."""
    found = _found_in_the_plant(tmp_path, A_ROOT_RESHAPED_BY_ITS_OWN_METHODS)
    assert len(found) == 2, found


def test_the_fixture_root_imported_under_another_name_is_followed(tmp_path):
    """`from src.cutoff_guard import FIXTURES as ROOT` leaves a read that says
    `ROOT`. The import line is where the module says what that is."""
    found = _found_in_the_plant(tmp_path, THE_GATES_OWN_ROOT_UNDER_ANOTHER_NAME)
    assert len(found) == 1, found
    assert "read_bytes" in found[0]


def test_a_fixture_copied_out_is_named(tmp_path):
    """A copy carries the bytes past the gate exactly as a read does, and it
    does not go through anything this scan would otherwise see."""
    found = _found_in_the_plant(tmp_path, A_FIXTURE_COPIED_OUT)
    assert len(found) == 1, found
    assert "shutil.copy" in found[0]


def test_a_read_through_the_gates_own_private_reader_is_named(tmp_path):
    """`cutoff_guard._read` is the open with the check already behind it. Being
    inside the gate's module makes it the gate's business, not a route out."""
    found = _found_in_the_plant(tmp_path, THROUGH_THE_GATES_PRIVATE_READER)
    assert len(found) == 1, found
    assert "_read" in found[0]


def test_a_plain_read_is_still_named(tmp_path):
    """The case the scan already caught, kept under a judge of its own."""
    found = _found_in_the_plant(tmp_path, A_PLAIN_READ)
    assert len(found) == 1, found
    assert "read_bytes" in found[0]


def test_a_read_through_the_gate_is_not_a_finding(tmp_path):
    """The sanctioned route, which is what the rest of `src/` does all day. A
    scan that flagged this would pass every test above and be unusable."""
    assert _found_in_the_plant(tmp_path, THROUGH_THE_GATE) == []


def test_a_read_of_something_that_is_not_a_document_is_not_a_finding(tmp_path):
    """The versioned SIC map is not a filing and has no cutoff to check. The
    scan is about fixtures and bundles, not about every open in the project."""
    assert _found_in_the_plant(tmp_path, NOT_A_DOCUMENT_AT_ALL) == []


def test_the_fetchers_reader_is_recognised_by_reading_its_body():
    """Not by being named in a list here, which is where the blindness would
    come back: `read_stored` reads the path it is handed and `store` writes
    one, and the difference is in the two functions and not in this file."""
    modules = {path.name: ast.parse(path.read_text(encoding="utf-8"))
               for path in sorted(SRC.glob("*.py"))}
    readers = _readers(modules)
    assert "fetch_fixtures.py" in readers["read_stored"]
    assert "fetch_fixtures.py" in readers["load_manifest"]
    # `store` opens the path it is handed too, and what keeps it out is the
    # mode it opens with -- `packed.open("wb")` -- and not a blindness to the
    # shape, which would take `read_stored` out beside it.
    assert "store" not in readers
    # `load_runs` lists the companies under the runs root it is handed and
    # reads every run through the gate, so it hands nobody a document. A
    # listing counted as a read would make it one, and `render` above it, and
    # then `render(args.runs)` in `main` -- a line that reads nothing -- the
    # scan's only finding.
    assert "load_runs" not in readers
    assert "render" not in readers
    # The gate's public route is not a reader to be reported on; the raw open
    # underneath it is.
    assert "cutoff_guard.py" in readers["_read"]
    assert "load_document" not in readers
    assert "load_bytes" not in readers


if __name__ == "__main__":
    lines = bypass_scan()
    print("\n".join(lines) if lines else
          f"bypass scan: {len(list(SRC.glob('*.py')))} modules in src/, "
          f"{len(EXEMPT)} exempt ({', '.join(sorted(EXEMPT))}), 0 reads skip the gate")
