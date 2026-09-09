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

**The annual trigger.** The record is read through
`src/cutoff_guard.load_catalogue`, the sanctioned route into a catalogue, and
the reason is at the bottom of this file: a catalogue is dated with the newest
filing it carries a fact from, so the whole-file date gate refused the whole
record to eleven of the twelve annual runs, and the scan exited 2 for them. What
those runs get instead is asserted here — the traces the record supports at the
trigger's own date, derived from the file by `traces_in_the_file`, which opens
`companyfacts.json.gz` and imports nothing from `src/`.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from collections import defaultdict
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

# The committed record's own quiet restatement, and the one that is not in whole
# dollars: Carrier first reported the second quarter of 2023 at a dividend of
# 0.38 per share in the 10-Q filed 2023-07-27, and reported that quarter back at
# 0.37 in the 10-Q filed 2023-10-26. Both rows are read out of the document in
# the test below. 0.37 − 0.38 = −0.01, subtracted here by hand.
DIVIDEND_TAG = "CommonStockDividendsPerShareDeclared"
DIVIDEND_UNIT = "USD/shares"
DIVIDEND_PERIOD = {"start": "2023-04-01", "end": "2023-06-30"}
DIVIDEND_FIRST_REPORTED = 0.38
DIVIDEND_RESTATED = 0.37
DIVIDEND_DIFFERENCE = -0.01

# Carrier's second-quarter 2026 10-Q, filed 2026-07-28, is in no companyfacts
# row: EDGAR had not loaded it when the fixture set was fetched. It is the
# accession the manifest records for the 10-Q instance, and the absence is
# companyfacts' own — `tests/test_fetch_companyfacts.py` records the same gap.
NOT_YET_LOADED = "0001783180-26-000032"
NOT_YET_LOADED_FILED = "2026-07-28"

# The twelve companies, and the run this item is about: Carrier's 10-K, filed
# 2026-02-05, is the triggering report of an annual run and therefore that run's
# cutoff. Carrier's companyfacts record is dated 2026-04-30 — a catalogue is
# dated with the newest filing it carries a fact from — so the whole-file date
# gate refused the whole record to that run and the scan exited 2.
TWELVE = ("AAPL", "CARR", "CIEN", "CSCO", "ESE", "GNRC",
          "LFUS", "NVDA", "PANW", "QCOM", "STX", "TTMI")
ANNUAL_TRIGGER = "2026-02-05"
CATALOGUE_RECORDED_DATE = "2026-04-30"
FIXTURE_SET_AS_OF = "2026-09-01"

# Eleven of the twelve records are dated after the company's own 10-K, so eleven
# annual runs were refused. Seagate is the twelfth: its 10-K was filed the same
# day its record is dated, and `doc_date == cutoff_date` is allowed.
REFUSED_AT_THEIR_ANNUAL_TRIGGER = 11
SERVED_AT_ITS_ANNUAL_TRIGGER = "STX"

# Counted from tests/fixtures/CARR/companyfacts.json.gz by the reader below,
# which opens the file and imports nothing from `src/`. At the 10-K's own date
# the record supports 315 traces over 6,107 periods, 3,119 of them reported by
# more than one filing; at the fixture set's as-of date, 318 over 6,278. The
# annual answer is smaller, and it is an answer.
TRACES_AT_THE_ANNUAL_TRIGGER = 315
PERIODS_AT_THE_ANNUAL_TRIGGER = 6107
REPORTED_MORE_THAN_ONCE_AT_THE_ANNUAL_TRIGGER = 3119
TRACES_AT_THE_FIXTURE_AS_OF = 318
PERIODS_AT_THE_FIXTURE_AS_OF = 6278


# --- the two documents, read as documents ------------------------------------

def companyfacts(fixtures_root: Path) -> dict:
    """One companyfacts document, through the gate every reader goes through."""
    record = cutoff_guard.one_document(TICKER, restatement_trace.COMPANYFACTS_FORM,
                                       restatement_trace.COMPANYFACTS_ROLE,
                                       fixtures_root=fixtures_root)
    cutoff = cutoff_guard.default_cutoff(TICKER, fixtures_root=fixtures_root)
    return json.loads(cutoff_guard.load_bytes(record["full_path"], cutoff,
                                              fixtures_root=fixtures_root))


def rows_for_the_period(document: dict, tag=TAG, unit=UNIT, period=PERIOD) -> list[dict]:
    return [row for row in document["facts"][NAMESPACE][tag]["units"][unit]
            if (row.get("start"), row["end"]) == (period["start"], period["end"])]


def every_row(document: dict) -> list[tuple]:
    """Every fact row in one document, in the order the document holds them."""
    return [(namespace, tag, unit, index, row)
            for namespace, concepts in document["facts"].items()
            for tag, concept in concepts.items()
            for unit, rows in concept["units"].items()
            for index, row in enumerate(rows)]


# --- a second reader, for the tests alone ------------------------------------
#
# The scan reads the record through `cutoff_guard.load_catalogue` and then
# groups and compares. Judging its answer against its own reading of the file
# would assert that it agrees with itself, so everything below opens the gzip by
# name and imports nothing from `src/`.

def manifest(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "manifest.json").read_text(encoding="utf-8"))


def catalogue_row(ticker: str) -> dict:
    """The manifest row describing one company's companyfacts record."""
    return next(row for row in manifest(ticker)["documents"]
                if row["role"] == restatement_trace.COMPANYFACTS_ROLE)


def annual_trigger(ticker: str) -> str:
    """The filing date of the company's 10-K, which is an annual run's cutoff."""
    return max(row["filing_date"] for row in manifest(ticker)["documents"]
               if (row["form"], row["role"]) == ("10-K", "primary_html"))


def catalogue_in_the_file(ticker: str) -> dict:
    """One companyfacts record, decompressed and parsed the plain way."""
    return json.loads(gzip.decompress(
        (FIXTURES / ticker / "companyfacts.json.gz").read_bytes()))


def rows_in_the_file(ticker: str, cutoff: str) -> dict[tuple, list[dict]]:
    """Rows filed on or before the cutoff, gathered by the period they are about.

    `CLAUDE.md`'s rule applied by hand: document filing date <= the triggering
    report's. The key is namespace, tag, unit and the period, which is what makes
    two rows the same fact.
    """
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for namespace, concepts in catalogue_in_the_file(ticker)["facts"].items():
        for tag, concept in concepts.items():
            for unit, rows in concept["units"].items():
                for row in rows:
                    if row["filed"] <= cutoff:
                        grouped[(namespace, tag, unit,
                                 row.get("start"), row["end"])].append(row)
    return grouped


def traces_in_the_file(ticker: str, cutoff: str) -> set[tuple]:
    """The disagreements with the first-reported value, derived here from the file.

    The rule restated from `CLAUDE.md` and `docs/CHECKLIST.md` rather than
    borrowed from the module: the earliest filing to report a period is ground
    truth, one trace per distinct later value recorded at the filing that first
    carried it, and a filing that reports the period at two values is left out
    of the comparison — the whole period only when that filing is the first one.
    The tuple is `key()`'s, so the two sides are comparable.
    """
    found = set()
    for period, rows in rows_in_the_file(ticker, cutoff).items():
        namespace, tag, unit, start, end = period
        values: dict[str, set] = defaultdict(set)
        filed: dict[str, str] = {}
        for row in rows:
            values[row["accn"]].add(row["val"])
            filed.setdefault(row["accn"], row["filed"])
        at_two_values = {accession for accession in values if len(values[accession]) > 1}
        order = sorted(values, key=lambda accession: (filed[accession], accession))
        first = order[0]
        if first in at_two_values:
            continue
        first_value = next(iter(values[first]))
        reported = {first_value}
        for accession in order[1:]:
            if accession in at_two_values:
                continue
            value = next(iter(values[accession]))
            if value not in reported:
                reported.add(value)
                found.add((namespace, tag, unit, start, end,
                           first, first_value, accession, value))
    return found


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


def test_the_planted_manifest_records_the_one_document_the_directory_holds():
    """A planted record is still a record: it may not name a file it does not hold."""
    manifest = json.loads((PLANTED / TICKER / "manifest.json").read_text())
    assert [row["path"] for row in manifest["documents"]] == ["companyfacts.json.gz"]
    assert sorted(path.name for path in (PLANTED / TICKER).iterdir()) == [
        "companyfacts.json.gz", "manifest.json"]


# --- what the scan says about it ---------------------------------------------

def trace_for_the_period(payload: dict, tag=TAG, unit=UNIT, period=PERIOD) -> list[dict]:
    return [trace for trace in payload["traces"]
            if (trace["tag"], trace["unit"], trace["period"]) == (tag, unit, period)]


@pytest.fixture(scope="module")
def committed_scan() -> dict:
    return restatement_trace.scan(TICKER, fixtures_root=FIXTURES)


@pytest.fixture(scope="module")
def planted_scan() -> dict:
    return restatement_trace.scan(TICKER, fixtures_root=PLANTED)


def test_the_planted_difference_is_the_two_numbers_subtracted():
    assert PLANTED_VALUE - FIRST_REPORTED_VALUE == PLANTED_DIFFERENCE


def test_two_decimals_subtract_in_decimal_and_two_integers_stay_an_integer():
    """The three subtractions on the right are hand arithmetic, not a run's output."""
    assert json.dumps(restatement_trace.difference(0.37, 0.38)) == "-0.01"
    assert json.dumps(restatement_trace.difference(0.303, 0.344)) == "-0.041"
    planted = restatement_trace.difference(PLANTED_VALUE, FIRST_REPORTED_VALUE)
    assert planted == PLANTED_DIFFERENCE
    assert isinstance(planted, int)


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


def test_a_difference_in_cents_is_reported_in_cents_and_not_in_binary(committed_scan):
    """The committed record's own restatement, and the finding it hands the reader.

    Carrier's second-quarter 2023 dividend per share is the one committed trace
    whose two values are not whole numbers. Subtracted as floats it reports
    −0.010000000000000009, and that is what would go to the numbers reader.
    """
    rows = rows_for_the_period(companyfacts(FIXTURES), DIVIDEND_TAG, DIVIDEND_UNIT,
                               DIVIDEND_PERIOD)
    assert [row["val"] for row in rows][:2] == [DIVIDEND_FIRST_REPORTED, DIVIDEND_RESTATED]

    found = trace_for_the_period(committed_scan, DIVIDEND_TAG, DIVIDEND_UNIT,
                                 DIVIDEND_PERIOD)
    assert len(found) == 1, f"{len(found)} traces for {DIVIDEND_TAG} {DIVIDEND_PERIOD}"
    assert found[0]["first_reported"]["value"] == DIVIDEND_FIRST_REPORTED
    assert found[0]["restated"]["value"] == DIVIDEND_RESTATED
    assert found[0]["difference"] == DIVIDEND_DIFFERENCE
    assert DIVIDEND_RESTATED - DIVIDEND_FIRST_REPORTED != DIVIDEND_DIFFERENCE


def decimal_places(number) -> int:
    """How many digits after the point the number is written with in the payload."""
    written = json.dumps(number)
    return len(written.split(".")[1]) if "." in written else 0


def test_no_difference_in_the_committed_record_invents_a_digit(committed_scan):
    """Subtracting two decimals cannot need more decimal places than they carry.

    Float subtraction does exactly that — two two-place numbers report an
    eighteen-place one — so this fails the moment the arithmetic goes binary.
    """
    assert committed_scan["traces"], "no traces to check"
    for trace in committed_scan["traces"]:
        assert decimal_places(trace["difference"]) <= max(
            decimal_places(trace["first_reported"]["value"]),
            decimal_places(trace["restated"]["value"])), trace


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
    assert restatement_trace.ledger_line(committed_scan)["absent_from_companyfacts"] == 1


def test_a_filing_later_than_the_cutoff_is_outside_the_run_not_missing_from_it():
    """The absence list is cut off too, or a run names a document it may not see.

    Carrier's July 2026 10-Q is in no companyfacts row at any cutoff. A run
    triggered by the April 10-Q is not entitled to know it exists.
    """
    early = restatement_trace.scan(TICKER, cutoff="2026-05-01", fixtures_root=FIXTURES)
    assert early["cutoff"] == "2026-05-01"
    assert NOT_YET_LOADED_FILED > early["cutoff"]
    assert early["absent_from_companyfacts"] == []


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
              row(100, "third", "2025-11-01"))))
    assert ambiguous == []
    assert [(trace["first_reported"]["value"], trace["restated"]["value"],
             trace["restated"]["accession"]) for trace in found] == [(100, 90, "second")]


def test_one_restated_value_repeated_by_later_filings_is_one_trace():
    """The filing that introduced the new number is the one that restated."""
    found, _ = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01"),
              row(90, "third", "2025-11-01"),
              row(90, "fourth", "2026-02-01"))))
    assert [trace["restated"]["accession"] for trace in found] == ["second"]


def test_a_filing_that_reports_one_period_at_two_values_is_left_out_and_named():
    """Two roundings inside one document are not a restatement, and not silence.

    The filing is left out of the comparison, not the period: the third filing's
    disagreement with the first-reported 100 is still reported, because dropping
    the whole period would trade a real disagreement for silence.
    """
    found, ambiguous = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01"),
              row(90.4, "second", "2025-08-01"),
              row(80, "third", "2025-11-01"))))
    assert len(ambiguous) == 1
    assert ambiguous[0]["accessions"] == ["second"]
    assert ambiguous[0]["values"] == {"second": [90, 90.4]}
    assert [(trace["restated"]["accession"], trace["restated"]["value"])
            for trace in found] == [("third", 80)]


def test_a_period_whose_first_filing_reports_two_values_has_no_ground_truth():
    """Ground truth is the first-reported value, and two of them are not one."""
    found, ambiguous = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(101, "first", "2025-05-01"),
              row(90, "second", "2025-08-01"))))
    assert found == []
    assert [entry["accessions"] for entry in ambiguous] == [["first"]]


def test_a_row_filed_after_the_cutoff_does_not_enter_the_scan():
    """Nothing filed later enters the input, whatever the document as a whole holds.

    The row filter is `cutoff_guard.load_catalogue`'s now and not this module's,
    so this is asserted over the committed record rather than over rows written
    here: Carrier's first quarter of 2025 is reported by two filings, and at the
    annual trigger only the earlier of the two has happened.
    """
    period = (NAMESPACE, TAG, UNIT, PERIOD["start"], PERIOD["end"])
    assert FIRST_REPORTED_FILED <= ANNUAL_TRIGGER < LATER_FILED

    at_the_trigger = grouped_at(ANNUAL_TRIGGER)[period]
    assert [(entry["accn"], entry["filed"]) for entry in at_the_trigger] == [
        (FIRST_REPORTED_ACCESSION, FIRST_REPORTED_FILED)]

    later = grouped_at(FIXTURE_SET_AS_OF)[period]
    assert [(entry["accn"], entry["filed"]) for entry in later] == [
        (FIRST_REPORTED_ACCESSION, FIRST_REPORTED_FILED),
        (LATER_ACCESSION, LATER_FILED)]


def test_an_amendment_is_marked_rather_than_passed_off_as_quiet():
    """A 10-K/A says out loud what a quiet restatement does not say at all."""
    found, _ = restatement_trace.traces(restatement_trace.by_period(
        facts(row(100, "first", "2025-05-01"),
              row(90, "second", "2025-08-01", form="10-K/A"))))
    assert [trace["amendment"] for trace in found] == [True]
    assert restatement_trace.is_amendment("10-Q") is False


# --- the annual trigger: a smaller answer, where there used to be none --------
#
# `test_a_cutoff_earlier_than_the_record_refuses_the_run_rather_than_reading
# _less` used to stand here and assert the opposite: that `scan` raises
# `CutoffViolationError` at Carrier's own 10-K date. That refusal was the
# whole-file date gate applied to a catalogue, and the route this module now
# reads through is what replaced it. The assertion comes off, and what the run
# gets instead is asserted in its place.


def grouped_at(cutoff: str, ticker: str = TICKER) -> dict[tuple, list[dict]]:
    """What the scan groups at a cutoff, through the route the scan reads through."""
    record = cutoff_guard.one_document(ticker, restatement_trace.COMPANYFACTS_FORM,
                                       restatement_trace.COMPANYFACTS_ROLE,
                                       fixtures_root=FIXTURES)
    document = cutoff_guard.load_catalogue(record["full_path"], cutoff,
                                           fixtures_root=FIXTURES)
    return restatement_trace.by_period(document["facts"])


@pytest.fixture(scope="module")
def annual_scan() -> dict:
    return restatement_trace.scan(TICKER, cutoff=ANNUAL_TRIGGER, fixtures_root=FIXTURES)


def test_the_whole_file_gate_refuses_the_record_to_the_annual_run():
    """What the route replaced, stated as a fact about the gate and not assumed.

    Carrier's record is dated after Carrier's 10-K, so `load_bytes` refuses it
    to the annual run — and every row that run is entitled to goes with it.
    """
    record = cutoff_guard.one_document(TICKER, restatement_trace.COMPANYFACTS_FORM,
                                       restatement_trace.COMPANYFACTS_ROLE,
                                       fixtures_root=FIXTURES)
    assert record["filing_date"] == CATALOGUE_RECORDED_DATE > ANNUAL_TRIGGER
    with pytest.raises(CutoffViolationError):
        cutoff_guard.load_bytes(record["full_path"], ANNUAL_TRIGGER,
                                fixtures_root=FIXTURES)


def test_the_annual_trigger_gets_the_traces_the_record_supports_at_that_date(annual_scan):
    """Which traces, not merely that the scan did not raise.

    The right-hand side is `traces_in_the_file`, which opens the gzip and
    derives the disagreements by hand. The three counts are what that reader
    counts, written down so that two empty answers cannot agree with each other.
    """
    assert annual_scan["cutoff"] == ANNUAL_TRIGGER
    assert {key(trace) for trace in annual_scan["traces"]} == \
        traces_in_the_file(TICKER, ANNUAL_TRIGGER)
    assert annual_scan["counts"]["traces"] == TRACES_AT_THE_ANNUAL_TRIGGER
    assert annual_scan["counts"]["periods"] == PERIODS_AT_THE_ANNUAL_TRIGGER
    assert annual_scan["counts"]["periods_reported_more_than_once"] == \
        REPORTED_MORE_THAN_ONCE_AT_THE_ANNUAL_TRIGGER


def test_the_dividend_restatement_is_one_of_them(annual_scan):
    """A named trace inside the annual run, with the two values read by hand.

    Carrier reported the second quarter of 2023 at 0.38 a share on 2023-07-27
    and at 0.37 on 2023-10-26 — both inside a run triggered on 2026-02-05, and
    both refused to it before this route.
    """
    found = trace_for_the_period(annual_scan, DIVIDEND_TAG, DIVIDEND_UNIT,
                                 DIVIDEND_PERIOD)
    assert len(found) == 1
    assert found[0]["first_reported"]["value"] == DIVIDEND_FIRST_REPORTED
    assert found[0]["restated"]["value"] == DIVIDEND_RESTATED
    assert found[0]["restated"]["filing_date"] == "2023-10-26" <= ANNUAL_TRIGGER


def test_the_period_the_planted_copy_restates_is_not_yet_restated_here(annual_scan):
    """The control on the assertion above: silence where the record is silent.

    The 10-Q that reports Carrier's first quarter of 2025 back was filed
    2026-04-30, after the trigger, so at this cutoff the period has one filing
    and nothing to disagree with.
    """
    assert trace_for_the_period(annual_scan) == []


def test_the_annual_answer_is_smaller_than_the_fixture_sets_own(annual_scan, committed_scan):
    """Smaller, and smaller by rows filed after the trigger. Not the same answer."""
    assert committed_scan["cutoff"] == FIXTURE_SET_AS_OF
    assert committed_scan["counts"]["traces"] == TRACES_AT_THE_FIXTURE_AS_OF
    assert committed_scan["counts"]["periods"] == PERIODS_AT_THE_FIXTURE_AS_OF

    annual = {key(trace) for trace in annual_scan["traces"]}
    later = {key(trace) for trace in committed_scan["traces"]}
    assert annual < later
    assert len(later - annual) == \
        TRACES_AT_THE_FIXTURE_AS_OF - TRACES_AT_THE_ANNUAL_TRIGGER
    assert all(trace["restated"]["filing_date"] > ANNUAL_TRIGGER
               for trace in committed_scan["traces"] if key(trace) in later - annual)


def test_the_annual_run_names_no_absent_filing_it_may_not_see(annual_scan):
    """The 10-K's own facts are in the record, and the July 10-Q is outside the run."""
    assert annual_scan["absent_from_companyfacts"] == []
    assert NOT_YET_LOADED_FILED > ANNUAL_TRIGGER


def test_the_annual_run_exits_zero_rather_than_two(tmp_path):
    """It exited 2 before this: the gate refused the record and the run had
    nothing to say about the company at all."""
    assert restatement_trace.main([
        "--ticker", TICKER, "--fixtures", str(FIXTURES),
        "--cutoff", ANNUAL_TRIGGER,
        "--out", str(tmp_path / "annual.json"),
        "--ledger", str(tmp_path / "ledger.jsonl")]) == 0
    written = json.loads((tmp_path / "annual.json").read_text())
    assert written["cutoff"] == ANNUAL_TRIGGER
    assert len(written["traces"]) == TRACES_AT_THE_ANNUAL_TRIGGER
    line = json.loads((tmp_path / "ledger.jsonl").read_text())
    assert line["traces"] == TRACES_AT_THE_ANNUAL_TRIGGER


# --- the invariant both readers lean on, over the twelve committed records ----


@pytest.mark.parametrize("ticker", TWELVE)
def test_a_catalogues_recorded_date_is_its_own_newest_row(ticker):
    """A catalogue is dated with the newest filing it carries a fact from.

    That is what the manifest row says in its own `date_basis`, and it is the
    whole reason the whole-file date gate is the wrong gate for these two
    documents. It was asserted only against a record written for the purpose;
    here it is asserted over the twelve committed ones.
    """
    filed = [row["filed"] for rows in rows_in_the_file(ticker, "9999-12-31").values()
             for row in rows]
    assert filed, f"{ticker}'s record holds no rows"
    assert catalogue_row(ticker)["filing_date"] == max(filed)


def test_the_whole_file_gate_refused_eleven_of_the_twelve_annual_runs():
    """Why this item exists, counted over the fixture set rather than argued.

    Seagate is the twelfth: its 10-K was filed the same day its record is dated,
    and `doc_date == cutoff_date` is allowed.
    """
    refused = [ticker for ticker in TWELVE
               if annual_trigger(ticker) < catalogue_row(ticker)["filing_date"]]
    assert len(refused) == REFUSED_AT_THEIR_ANNUAL_TRIGGER
    assert [ticker for ticker in TWELVE if ticker not in refused] == \
        [SERVED_AT_ITS_ANNUAL_TRIGGER]


@pytest.mark.parametrize("ticker", TWELVE)
def test_the_newest_row_the_scan_sees_is_on_or_before_its_cutoff(ticker):
    """The cutoff rule, over all twelve, at each company's own annual trigger.

    The second assertion is what keeps the first from being satisfied by
    silence: every one of the twelve 10-Ks put facts into its own record, so the
    newest row the reader sees is the trigger's own date and not merely earlier
    than it. The count is the independent reader's.
    """
    cutoff = annual_trigger(ticker)
    grouped = grouped_at(cutoff, ticker)
    seen = [row["filed"] for rows in grouped.values() for row in rows]
    counted = [row["filed"] for rows in rows_in_the_file(ticker, cutoff).values()
               for row in rows]
    assert seen, f"{ticker} sees no rows at {cutoff}"
    assert max(seen) <= cutoff
    assert max(seen) == cutoff
    assert len(seen) == len(counted)


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
    assert line["absent_from_companyfacts"] == len(
        planted_scan["absent_from_companyfacts"])
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
