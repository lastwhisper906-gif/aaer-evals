"""The trace is judged against a difference planted on purpose.

`tests/fixtures/planted_restatement/CARR/` is a copy of the committed
companyfacts record with exactly one number changed. Carrier first reported its
first quarter of 2025 net income at 412,000,000 in the 10-Q filed 2025-05-01;
in the copy, the 10-Q filed 2026-04-30 reports that same quarter back at
389,000,000. Nothing else in the document moves — the copy is byte-identical to
the record apart from that one value, and `test_the_planted_copy_changes_that
_one_number_and_nothing_else` is what says so rather than trusting it.

So the number the scan has to report was known before the scan was written. The
first-reported side is the committed record's own value, read out of
`tests/fixtures/CARR/companyfacts.json.gz`; the later side is the value planted;
the difference is the two of them subtracted. None of the three came from
running `src/restatement_trace.py`.

The silence assertions carry their own control. `test_the_committed_record
_reports_no_trace_for_that_period` passes because the committed record agrees
with itself, and it would pass just as well if the scan reported nothing at all
— so it asserts, in the same file, that the period is one the scan does reach,
and the planted copy next door is the positive control that the scan speaks when
there is something to say.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

import pytest

from src import cutoff_guard, restatement_trace
from src.cutoff_guard import CutoffViolationError

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PLANTED = FIXTURES / "planted_restatement"

TICKER = "CARR"
NAMESPACE = "us-gaap"
TAG = "NetIncomeLoss"
UNIT = "USD"
PERIOD = {"start": "2025-01-01", "end": "2025-03-31"}

# From the committed companyfacts record: the 10-Q that first reported the
# quarter, and the 10-Q a year later that reports it back. Both rows are in
# tests/fixtures/CARR/companyfacts.json.gz at 412,000,000, which is what
# test_the_committed_record_reports_the_period_at_one_value_from_two_filings
# reads out of the document rather than restating from here.
FIRST_REPORTED_VALUE = 412_000_000
FIRST_REPORTED_ACCESSION = "0001783180-25-000030"
FIRST_REPORTED_FILED = "2025-05-01"
LATER_ACCESSION = "0001783180-26-000026"
LATER_FILED = "2026-04-30"

# Planted, in the copy alone.
PLANTED_VALUE = 389_000_000
# 389,000,000 − 412,000,000 = −23,000,000
PLANTED_DIFFERENCE = -23_000_000

# Carrier's second-quarter 2026 10-Q, filed 2026-07-28, is in no companyfacts
# row: EDGAR had not loaded it when the fixture set was fetched. It is the
# accession the manifest records for the 10-Q instance, and the absence is
# companyfacts' own — `tests/test_fetch_companyfacts.py` records the same gap.
NOT_YET_LOADED = "0001783180-26-000032"
NOT_YET_LOADED_FILED = "2026-07-28"


# --- the two documents, read as documents ------------------------------------

def companyfacts(fixtures_root: Path) -> dict:
    """One companyfacts document, through the gate every reader goes through."""
    record = cutoff_guard.one_document(TICKER, restatement_trace.COMPANYFACTS_FORM,
                                       restatement_trace.COMPANYFACTS_ROLE,
                                       fixtures_root=fixtures_root)
    cutoff = cutoff_guard.default_cutoff(TICKER, fixtures_root=fixtures_root)
    return json.loads(cutoff_guard.load_bytes(record["full_path"], cutoff,
                                              fixtures_root=fixtures_root))


def rows_for_the_period(document: dict) -> list[dict]:
    return [row for row in document["facts"][NAMESPACE][TAG]["units"][UNIT]
            if (row.get("start"), row["end"]) == (PERIOD["start"], PERIOD["end"])]


def every_row(document: dict) -> list[tuple]:
    """Every fact row in one document, in the order the document holds them."""
    return [(namespace, tag, unit, index, row)
            for namespace, concepts in document["facts"].items()
            for tag, concept in concepts.items()
            for unit, rows in concept["units"].items()
            for index, row in enumerate(rows)]


def test_the_committed_record_reports_the_period_at_one_value_from_two_filings():
    """The source side of the expected value, read out of the record itself."""
    rows = rows_for_the_period(companyfacts(FIXTURES))
    assert [(row["accn"], row["filed"], row["val"]) for row in rows] == [
        (FIRST_REPORTED_ACCESSION, FIRST_REPORTED_FILED, FIRST_REPORTED_VALUE),
        (LATER_ACCESSION, LATER_FILED, FIRST_REPORTED_VALUE),
    ]


def test_the_planted_copy_changes_that_one_number_and_nothing_else():
    """A copy that had drifted anywhere else would judge something else."""
    committed = every_row(companyfacts(FIXTURES))
    planted = every_row(companyfacts(PLANTED))
    assert len(planted) == len(committed)

    differences = [(there, here) for there, here in zip(committed, planted)
                   if there != here]
    assert len(differences) == 1, f"{len(differences)} rows differ, not one"
    (_, tag, unit, _, was), (_, _, _, _, now) = differences[0]
    assert (tag, unit) == (TAG, UNIT)
    assert (was.get("start"), was["end"]) == (PERIOD["start"], PERIOD["end"])
    assert was["accn"] == now["accn"] == LATER_ACCESSION
    assert was["val"] == FIRST_REPORTED_VALUE
    assert now["val"] == PLANTED_VALUE
    assert {key: value for key, value in was.items() if key != "val"} == \
           {key: value for key, value in now.items() if key != "val"}


def test_the_planted_copy_is_the_bytes_its_own_manifest_recorded():
    """A fixture is a record even when what it records was planted."""
    manifest = json.loads((PLANTED / TICKER / "manifest.json").read_text())
    entry = next(row for row in manifest["documents"]
                 if row["form"] == restatement_trace.COMPANYFACTS_FORM)
    raw = gzip.decompress((PLANTED / TICKER / entry["path"]).read_bytes())
    assert len(raw) == entry["bytes"]
    assert hashlib.sha256(raw).hexdigest() == entry["sha256"]
    assert manifest["planted"]["restated"]["value"] == PLANTED_VALUE


# --- what the scan says about it ---------------------------------------------

def trace_for_the_period(payload: dict) -> list[dict]:
    return [trace for trace in payload["traces"]
            if (trace["tag"], trace["unit"], trace["period"]) == (TAG, UNIT, PERIOD)]


@pytest.fixture(scope="module")
def committed_scan() -> dict:
    return restatement_trace.scan(TICKER, fixtures_root=FIXTURES)


@pytest.fixture(scope="module")
def planted_scan() -> dict:
    return restatement_trace.scan(TICKER, fixtures_root=PLANTED)


def test_the_planted_difference_is_the_two_numbers_subtracted():
    assert PLANTED_VALUE - FIRST_REPORTED_VALUE == PLANTED_DIFFERENCE


def test_the_planted_restatement_is_reported_with_the_accession_on_each_side(planted_scan):
    found = trace_for_the_period(planted_scan)
    assert len(found) == 1, f"{len(found)} traces for {TAG} {PERIOD}"
    trace = found[0]
    assert trace["first_reported"] == {"value": FIRST_REPORTED_VALUE,
                                       "accession": FIRST_REPORTED_ACCESSION,
                                       "filing_date": FIRST_REPORTED_FILED,
                                       "form": "10-Q"}
    assert trace["restated"] == {"value": PLANTED_VALUE,
                                 "accession": LATER_ACCESSION,
                                 "filing_date": LATER_FILED,
                                 "form": "10-Q"}
    assert trace["difference"] == PLANTED_DIFFERENCE
    assert trace["namespace"] == NAMESPACE
    assert trace["amendment"] is False


def test_the_committed_record_reports_no_trace_for_that_period(committed_scan):
    """The control for the assertion above: unplanted, the period is silent.

    And silent because the two filings agree, not because the period is out of
    reach — it is one of the periods this record reports more than once.
    """
    assert trace_for_the_period(committed_scan) == []
    reported_by = {row["accn"] for row in rows_for_the_period(companyfacts(FIXTURES))}
    assert reported_by == {FIRST_REPORTED_ACCESSION, LATER_ACCESSION}


def key(trace: dict) -> tuple:
    return (trace["namespace"], trace["tag"], trace["unit"],
            trace["period"]["start"], trace["period"]["end"],
            trace["first_reported"]["accession"], trace["first_reported"]["value"],
            trace["restated"]["accession"], trace["restated"]["value"])


def test_planting_one_value_adds_exactly_one_trace(committed_scan, planted_scan):
    """One changed number, one more finding. Nothing else moved with it."""
    committed = {key(trace) for trace in committed_scan["traces"]}
    planted = {key(trace) for trace in planted_scan["traces"]}
    assert committed - planted == set()
    assert planted - committed == {
        (NAMESPACE, TAG, UNIT, PERIOD["start"], PERIOD["end"],
         FIRST_REPORTED_ACCESSION, FIRST_REPORTED_VALUE,
         LATER_ACCESSION, PLANTED_VALUE)}
    assert planted_scan["counts"]["traces"] == committed_scan["counts"]["traces"] + 1


def test_a_filing_companyfacts_has_not_loaded_is_named_and_never_valued(committed_scan):
    """An absence is reported as an absence. It is not a period at zero."""
    assert committed_scan["absent_from_companyfacts"] == [
        {"form": "10-Q", "role": "xbrl_instance", "accession": NOT_YET_LOADED,
         "filing_date": NOT_YET_LOADED_FILED}]
    named = {side["accession"] for trace in committed_scan["traces"]
             for side in (trace["first_reported"], trace["restated"])}
    assert NOT_YET_LOADED not in named


def test_the_record_the_scan_read_is_named_by_its_own_hash(planted_scan, committed_scan):
    """Two documents, two hashes: a payload says which one it was read from."""
    assert planted_scan["record"]["sha256"] != committed_scan["record"]["sha256"]
    raw = gzip.decompress((PLANTED / TICKER / "companyfacts.json.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest() == planted_scan["record"]["sha256"]


# --- the rules of the scan, on rows written here ------------------------------

def facts(*rows) -> dict:
    """A companyfacts `facts` object holding one tag, in EDGAR's own shape."""
    return {NAMESPACE: {TAG: {"units": {UNIT: list(rows)}}}}


def row(value, accession, filed, form="10-Q", start="2025-01-01", end="2025-03-31"):
    return {"start": start, "end": end, "val": value, "accn": accession,
            "form": form, "filed": filed}


def test_a_value_that_comes_back_to_the_first_reported_one_is_not_a_second_trace():
    """Ground truth is the first-reported value, so 100 → 90 → 100 is one trace."""
    found, ambiguous = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01"),
              row(100, "third", "2025-11-01")), "2026-09-01"))
    assert ambiguous == []
    assert [(trace["first_reported"]["value"], trace["restated"]["value"],
             trace["restated"]["accession"]) for trace in found] == [(100, 90, "second")]


def test_one_restated_value_repeated_by_later_filings_is_one_trace():
    """The filing that introduced the new number is the one that restated."""
    found, _ = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01"),
              row(90, "third", "2025-11-01"),
              row(90, "fourth", "2026-02-01")), "2026-09-01"))
    assert [trace["restated"]["accession"] for trace in found] == ["second"]


def test_a_filing_that_reports_one_period_at_two_values_is_left_out_and_named():
    """Two roundings inside one document are not a restatement, and not silence."""
    found, ambiguous = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01"),
              row(90.4, "second", "2025-08-01")), "2026-09-01"))
    assert found == []
    assert len(ambiguous) == 1
    assert ambiguous[0]["accessions"] == ["second"]
    assert ambiguous[0]["values"] == {"second": [90, 90.4]}


def test_a_row_filed_after_the_cutoff_does_not_enter_the_scan():
    """Nothing filed later enters the input, whatever the document as a whole holds."""
    written = facts(row(100, "first", "2025-05-01"), row(90, "second", "2025-08-01"))
    assert restatement_trace.traces(restatement_trace.by_period(written, "2025-06-30")) \
        == ([], [])
    found, _ = restatement_trace.traces(restatement_trace.by_period(written, "2025-08-01"))
    assert len(found) == 1


def test_an_amendment_is_marked_rather_than_passed_off_as_quiet():
    """A 10-K/A says out loud what a quiet restatement does not say at all."""
    found, _ = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01", form="10-K/A")), "2026-09-01"))
    assert [trace["amendment"] for trace in found] == [True]
    assert restatement_trace.is_amendment("10-Q") is False


def test_a_cutoff_earlier_than_the_record_refuses_the_run_rather_than_reading_less():
    """companyfacts is dated with the newest filing it carries a fact from."""
    with pytest.raises(CutoffViolationError):
        restatement_trace.scan(TICKER, cutoff="2026-02-05", fixtures_root=FIXTURES)


# --- the one ledger line -----------------------------------------------------

def test_the_module_writes_to_the_event_ledger_by_default():
    assert restatement_trace.LEDGER == cutoff_guard.REPO_ROOT / "events" / "ledger.jsonl"


def run(tmp_path: Path, name: str) -> int:
    return restatement_trace.main([
        "--ticker", TICKER, "--fixtures", str(PLANTED),
        "--out", str(tmp_path / name), "--ledger", str(tmp_path / "ledger.jsonl")])


def test_a_run_appends_one_line_naming_what_it_found(tmp_path, planted_scan):
    assert run(tmp_path, "first.json") == 0
    lines = (tmp_path / "ledger.jsonl").read_text().splitlines()
    assert len(lines) == 1
    line = json.loads(lines[0])
    assert line["event"] == "quiet_restatement"
    assert line["ticker"] == TICKER
    assert line["source"] == "companyfacts"
    assert line["traces"] == planted_scan["counts"]["traces"]
    assert line["record_sha256"] == planted_scan["record"]["sha256"]
    assert line["absent_from_companyfacts"] == 1
    assert line["cutoff"] == planted_scan["cutoff"]

    written = json.loads((tmp_path / "first.json").read_text())
    assert trace_for_the_period(written) == trace_for_the_period(planted_scan)


def test_a_second_run_appends_and_leaves_the_first_line_where_it_was(tmp_path):
    assert run(tmp_path, "first.json") == 0
    first = (tmp_path / "ledger.jsonl").read_text()
    assert run(tmp_path, "second.json") == 0
    lines = (tmp_path / "ledger.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert lines[0] == first.splitlines()[0]


def test_a_scan_that_found_nothing_still_writes_its_line(tmp_path):
    """Otherwise "no restatement" and "never looked" read the same in the record."""
    nothing = {"ticker": TICKER, "cutoff": "2026-09-01",
               "record": {"sha256": "0" * 64},
               "counts": {"periods": 1, "periods_reported_more_than_once": 0,
                          "traces": 0, "amendments": 0},
               "absent_from_companyfacts": []}
    path = restatement_trace.append_line(
        restatement_trace.ledger_line(nothing, recorded_utc="2026-09-09T00:00:00Z"),
        tmp_path / "ledger.jsonl")
    assert json.loads(path.read_text()) == {
        "event": "quiet_restatement", "ticker": TICKER, "cutoff": "2026-09-01",
        "source": "companyfacts", "record_sha256": "0" * 64,
        "periods_reported_more_than_once": 0, "traces": 0, "amendments": 0,
        "absent_from_companyfacts": 0, "recorded_utc": "2026-09-09T00:00:00Z"}


def test_a_company_with_no_companyfacts_row_is_refused(tmp_path, capsys):
    """Exit 2, and the reason on stderr — not an empty trace list."""
    root = tmp_path / "fixtures"
    (root / TICKER).mkdir(parents=True)
    (root / TICKER / "manifest.json").write_text(json.dumps(
        {"ticker": TICKER, "as_of": "2026-09-01", "documents": []}) + "\n")
    assert restatement_trace.main([
        "--ticker", TICKER, "--fixtures", str(root),
        "--out", str(tmp_path / "out.json"),
        "--ledger", str(tmp_path / "ledger.jsonl")]) == restatement_trace.BAD_INPUT
    assert "restatement_trace:" in capsys.readouterr().err
    assert not (tmp_path / "ledger.jsonl").exists()
