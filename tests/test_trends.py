"""Every number in the trend table, checked against the record it names.

The table is built from the companyfacts history — 8 quarters and 5 years for
each of the twelve — with the XBRL instances filling what companyfacts has not
loaded. A cell says which fact and which filing it took each term from, and
this file is what makes that a claim rather than a caption. It is in two
halves, deliberately, because 12 companies × 13 periods × 11 ratios is
thousands of values and a hand computation at that size stops being a hand
computation and becomes a generator sharing code with the thing it judges.

**One.** For three companies and two periods each — Apple, Cisco and Carrier,
three different fiscal calendars — every ratio is written out term by term
below, with figures typed off the two source documents, so a reader can follow
the arithmetic without running anything.

**Two.** For every other cell, each term of each ratio is asserted equal to the
named fact in the record the cell names: a companyfacts row is looked up in
`tests/fixtures/{ticker}/companyfacts.json.gz` through `companyfacts_source`,
which imports nothing from `src/`, and an instance fact by its own id in
`input_numbers.json`. That is a weaker claim than the ratio being right — it
does not say the right fact was chosen — and deliberately so: it is a claim the
code under test cannot manufacture, because the value has to be in a document
this file opened for itself. The ratio is then recomputed here from those
values with this file's own copy of the eleven formulas.

The other half is the absences. Every one of the thirteen requested calendar
frames is either filled or named with a reason; the tests assert that none of
them was quietly dropped and that none was quietly filled with a zero.
"""

from __future__ import annotations

import datetime as dt
import functools
import hashlib
import json
import re
import tempfile
from pathlib import Path

import pytest

from src import cutoff_guard, extract_numbers, trends
from src.fetch_fixtures import TICKERS
from tests import companyfacts_source


@functools.lru_cache(maxsize=None)
def numbers(ticker: str) -> dict:
    """`input_numbers.json` for one company, exactly as `--out` would write it."""
    return json.loads(json.dumps(
        extract_numbers.extract(ticker, ("10-K", "10-Q")), default=str))


@functools.lru_cache(maxsize=None)
def table(ticker: str) -> dict:
    return trends.trends(numbers(ticker))


def rows(payload: dict) -> list[dict]:
    return payload["quarters"] + payload["years"]


def by_id(ticker: str) -> dict[str, dict]:
    return {fact["id"]: fact for fact in numbers(ticker)["facts"]}


def days_of(row: dict) -> int:
    return (dt.date.fromisoformat(row["end"]) - dt.date.fromisoformat(row["start"])).days + 1


def frame_row(payload: dict, frame: str) -> dict:
    """The one row of the table standing in a calendar frame."""
    found = [row for row in rows(payload) if row["frame"] == frame]
    assert len(found) == 1, f"{payload['ticker']}: {len(found)} rows in {frame}"
    return found[0]


def named_fact(ticker: str, source: dict) -> dict:
    """The fact a cell names, read out of the record the cell names.

    A companyfacts fact id is `{accession}:companyfacts:{tag}:{unit}:{period}`
    and every part of it has to agree with the fields printed beside it, or the
    id is decoration. The value and the filing date then come from the document
    `companyfacts_source` opened, not from anything in `src/`. An instance fact
    is its own id in `input_numbers.json`, which is the file the reader holds.
    """
    if source["record"] == "companyfacts":
        accession, marker, tag, unit, period = source["fact_id"].split(":")
        assert marker == "companyfacts"
        assert (accession, tag, unit) == (source["accession"], source["tag"],
                                          source["unit"])
        held = companyfacts_source.values(ticker).get((tag, unit, accession, period))
        assert held is not None, f"{ticker}: {source['fact_id']} is in no companyfacts row"
        value, filed = held
        assert filed == source["filed"], f"{ticker}: {source['fact_id']}"
        start, _, end = period.partition("..")
        context = {"start": start, "end": end} if end else {"instant": start}
        return {"number": value, "context": context, "tag": tag}
    fact = by_id(ticker).get(source["fact_id"])
    assert fact is not None, f"{ticker}: {source['fact_id']} is in no instance"
    assert fact["tag"] == source["tag"]
    assert fact["source_accession"] == source["accession"]
    assert fact["filing_date"] == source["filed"]
    return {"number": fact["number"], "context": fact["context"], "tag": fact["tag"]}


# The eleven formulas again, written out here rather than imported. `v` is the
# term values `named_fact` read back out of the record each cell names.
RECOMPUTE = {
    "receivables_over_revenue": lambda v, d: v["receivables"] / v["revenue"],
    "days_sales_outstanding": lambda v, d: v["receivables"] * d / v["revenue"],
    "days_sales_of_inventory": lambda v, d: v["inventory"] * d / v["cost_of_revenue"],
    "accruals_over_total_assets":
        lambda v, d: (v["net_income"] - v["operating_cash_flow"]) / v["assets"],
    "gross_margin": lambda v, d: 1 - v["cost_of_revenue"] / v["revenue"],
    "bad_debt_reserve_ratio":
        lambda v, d: v["bad_debt_allowance"] / (v["receivables"] + v["bad_debt_allowance"]),
    "inventory_reserve_ratio": lambda v, d: v["inventory_reserve"] / v["inventory"],
    "warranty_reserve_ratio": lambda v, d: v["warranty_accrual"] / v["revenue"],
    "soft_asset_share":
        lambda v, d: 1 - (v["property_plant_and_equipment"] + v["cash"]) / v["assets"],
    "contract_liabilities_over_revenue":
        lambda v, d: v["contract_liabilities"] / v["revenue"],
    "non_gaap_gap":
        lambda v, d: (v["non_gaap_net_income"] - v["net_income"]) / abs(v["net_income"]),
}


def test_the_ratio_list_is_the_input_specs_list():
    """docs/INPUT_SPEC.md §5 item 1, all eleven, no extras."""
    assert set(trends.RATIOS) == {
        "receivables_over_revenue", "days_sales_outstanding",
        "days_sales_of_inventory", "accruals_over_total_assets", "gross_margin",
        "bad_debt_reserve_ratio", "inventory_reserve_ratio",
        "warranty_reserve_ratio", "soft_asset_share",
        "contract_liabilities_over_revenue", "non_gaap_gap"}
    assert set(RECOMPUTE) == set(trends.RATIOS)


# --- (b) every ratio is reproducible from the fact ids it names --------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_ratio_recomputes_from_its_named_fact_ids(ticker):
    """Claim two: every term is the value its own record holds, and the ratio
    is those values divided.

    The lookup is `named_fact`, which reads the companyfacts document itself
    for a history row and `input_numbers.json` for an instance fact. Nothing
    here asks `src/trends.py` what a fact says.
    """
    checked = 0
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            if "value" not in cell:
                continue
            values = {}
            for term, source in cell["inputs"].items():
                fact = named_fact(ticker, source)
                assert fact["number"] == source["value"], \
                    f"{ticker} {row['label']} {name} {term}"
                values[term] = fact["number"]
            assert abs(RECOMPUTE[name](values, days_of(row)) - cell["value"]) <= 1e-9, \
                f"{ticker} {row['label']} {name}"
            checked += 1
    assert checked, f"{ticker}: nothing to recompute"


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_filled_ratio_names_a_fact_for_every_term_of_its_formula(ticker):
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            if "value" not in cell:
                continue
            assert cell["formula"] == trends.RATIOS[name]["formula"]
            for term in trends.RATIOS[name]["terms"]:
                assert term in cell["inputs"], f"{ticker} {row['label']} {name}"
                assert cell["inputs"][term]["fact_id"]
            words = set(re.findall(r"[a-z_]+", cell["formula"])) - {"days_in_period", "abs"}
            assert words == set(cell["inputs"]), f"{ticker} {name}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_fact_used_belongs_to_the_period_it_is_used_for(ticker):
    """No borrowing across periods: a duration term is the period itself, and a
    balance-sheet term is the instant at its end. The period comes out of the
    record the cell names, so a fact id that names one period and a value from
    another fails here."""
    for row in rows(table(ticker)):
        for cell in row["ratios"].values():
            for term, source in cell.get("inputs", {}).items():
                context = named_fact(ticker, source)["context"]
                if trends.CONCEPTS[term][0] == "duration":
                    assert (context["start"], context["end"]) == (row["start"], row["end"])
                else:
                    assert context["instant"] == row["end"]
                assert not context.get("segment")


# --- (c) a ratio that cannot be computed is absent, and says why -------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_a_ratio_that_cannot_be_computed_is_absent_not_zero(ticker):
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            if "value" in cell:
                assert isinstance(cell["value"], float)
                continue
            assert set(cell) >= {"missing"}
            assert isinstance(cell["missing"], str) and cell["missing"]
            assert "value" not in cell and "inputs" not in cell
            for change in ("year_over_year", "quarter_over_quarter"):
                assert cell[change]["reason"]
                assert "change" not in cell[change]


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_change_is_absent_unless_both_periods_are_filled(ticker):
    payload = table(ticker)
    labelled = {row["label"]: row for row in rows(payload)}
    for row in rows(payload):
        for name, cell in row["ratios"].items():
            for key in ("year_over_year", "quarter_over_quarter"):
                change = cell[key]
                if "change" not in change:
                    assert change["reason"]
                    continue
                other = labelled[change["against"]]
                assert abs((cell["value"] - other["ratios"][name]["value"])
                           - change["change"]) <= 1e-9


def test_no_ratio_is_ever_filled_for_the_non_gaap_gap():
    """An honest zero. companyfacts is the standard taxonomy and an instance
    carries us-gaap and dei facts; a non-GAAP measure is in neither — so the gap
    needs the 8-K exhibit, and the table says so instead of inventing it."""
    for ticker in TICKERS:
        for row in rows(table(ticker)):
            if not row["filled"]:
                continue
            cell = row["ratios"]["non_gaap_gap"]
            assert "value" not in cell
            assert "no us-gaap concept carries a non-GAAP measure" in cell["missing"]
        block = {entry["ratio"]: entry for entry in table(ticker)["coverage"]["ratios"]}
        assert block["non_gaap_gap"]["filled"] == 0


def test_a_zero_denominator_is_a_reason_not_an_infinity():
    facts = [
        {"id": "x:1", "tag": "Revenues", "prefix": "us-gaap", "number": 0.0, "nil": False,
         "unit": "iso4217:USD", "filing_date": "2026-01-01", "source_accession": "x",
         "context": {"start": "2025-01-01", "end": "2025-03-31", "segment": []}},
        {"id": "x:2", "tag": "AccountsReceivableNetCurrent", "prefix": "us-gaap",
         "number": 5.0, "nil": False, "unit": "iso4217:USD", "filing_date": "2026-01-01",
         "source_accession": "x",
         "context": {"instant": "2025-03-31", "segment": []}},
    ]
    period = {"start": "2025-01-01", "end": "2025-03-31", "days": 90}
    cell = trends.ratio(facts, "receivables_over_revenue", period)
    assert "value" not in cell
    assert cell["missing"] == "revenue is zero in 2025-01-01..2025-03-31"


def test_a_segmented_fact_is_not_a_consolidated_total():
    fact = {"number": 1.0, "nil": False,
            "context": {"segment": [{"dimension": "srt:ProductOrServiceAxis",
                                     "member": "us-gaap:ProductMember"}]}}
    assert not trends.usable(fact)
    assert trends.usable({"number": 1.0, "nil": False, "context": {"segment": []}})
    assert not trends.usable({"number": 1.0, "nil": False, "superseded_by": "later",
                              "context": {"segment": []}})


# --- (d) every requested period is listed --------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_coverage_lists_all_eight_quarters_and_five_years(ticker):
    """Changed with the source: a requested period used to be named by
    `target_end`, the date 91 or 365 days back from the newest period on
    record, and this asserted the reason repeated it. A period is now named by
    its calendar frame, which is what a comparison across companies joins on,
    so the reason repeats the frame. The claim is the one it always was —
    every missing period says which period it was and why it is empty — and
    `target_end` is gone rather than kept beside its replacement, because a
    frame's calendar end can fall after the run's cutoff and
    `tests/test_assemble_bundle.py` refuses that in a file a bundle carries.
    `trends.frame_bounds` still turns a frame into its two dates.
    """
    payload = table(ticker)
    assert payload["coverage"]["requested"] == {"quarters": 8, "years": 5}
    assert [row["label"] for row in payload["coverage"]["quarters"]] == \
        [f"Q-{index}" for index in range(8)]
    assert [row["label"] for row in payload["coverage"]["years"]] == \
        [f"FY-{index}" for index in range(5)]
    for entry in payload["coverage"]["quarters"] + payload["coverage"]["years"]:
        assert entry["status"] in ("filled", "missing")
        if entry["status"] == "missing":
            assert entry["reason"] and entry["frame"]
            assert entry["frame"] in entry["reason"]
        else:
            assert entry["start"] < entry["end"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_requested_period_is_either_filled_or_named(ticker):
    """Nothing is dropped: thirteen frames go out, and each is a period or a
    reason.

    This test used to read "the fixture set cannot fill thirteen periods and
    says which", and asserted at least one was missing. That was true of a
    one-10-K, one-10-Q input and is no longer true of the history: Cisco and
    Carrier now fill all thirteen. The claim that survives the change — and the
    one that was always the point — is the identity below.
    """
    payload = table(ticker)
    entries = payload["coverage"]["quarters"] + payload["coverage"]["years"]
    assert len(entries) == 13
    missing = [entry for entry in entries if entry["status"] == "missing"]
    assert len(missing) == 13 - sum(1 for row in rows(payload) if row["filled"])
    for entry in missing:
        assert entry["reason"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_unfilled_ratio_is_named_in_coverage(ticker):
    payload = table(ticker)
    from_rows = {(row["label"], name)
                 for row in rows(payload) if row["filled"]
                 for name, cell in row["ratios"].items() if "value" not in cell}
    from_rows |= {(row["label"], name) for row in rows(payload) if not row["filled"]
                  for name in trends.RATIOS}
    from_coverage = {(entry["period"], block["ratio"])
                     for block in payload["coverage"]["ratios"]
                     for entry in block["missing"]}
    assert from_rows == from_coverage
    for block in payload["coverage"]["ratios"]:
        assert block["filled"] + len(block["missing"]) == 13
        for entry in block["missing"]:
            assert entry["reason"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_filled_period_is_a_quarter_or_a_year_by_its_own_dates(ticker):
    payload = table(ticker)
    for row in payload["quarters"]:
        if row["filled"]:
            assert 80 <= days_of(row) <= 100 == row["days"] or row["days"] == days_of(row)
            assert trends.QUARTER_DAYS[0] <= row["days"] <= trends.QUARTER_DAYS[1]
    for row in payload["years"]:
        if row["filled"]:
            assert trends.YEAR_DAYS[0] <= row["days"] <= trends.YEAR_DAYS[1]
            assert row["days"] == days_of(row)


# --- the hand-typed oracle ---------------------------------------------------

def test_apples_fiscal_2025_gross_margin_is_the_filings_own_arithmetic():
    """AAPL FY2025: revenue $416,161m, cost of sales $220,960m."""
    row = frame_row(table("AAPL"), "CY2025")
    cell = row["ratios"]["gross_margin"]
    assert cell["inputs"]["revenue"]["value"] == 416161000000.0
    assert cell["inputs"]["cost_of_revenue"]["value"] == 220960000000.0
    assert abs(cell["value"] - (416161000000.0 - 220960000000.0) / 416161000000.0) <= 1e-12


def test_nvidias_latest_quarter_gross_margin_is_the_filings_own_arithmetic():
    """NVDA's quarter: revenue $96,221m, cost of revenue $24,079m."""
    row = frame_row(table("NVDA"), "CY2026Q2")
    cell = row["ratios"]["gross_margin"]
    assert cell["inputs"]["revenue"]["value"] == 96221000000.0
    assert cell["inputs"]["cost_of_revenue"]["value"] == 24079000000.0
    assert abs(cell["value"] - 0.7497531723844068) <= 1e-12


def test_ciscos_days_sales_outstanding_is_the_filings_own_arithmetic():
    """CSCO's quarter: receivables $6,480m over revenue $15,841m across 91 days.

    Retyped from the filing, not from the extractor. Cisco's 10-Q
    `0000858877-26-000078`, CONSOLIDATED BALANCE SHEETS (in millions,
    except par value) (Unaudited), the April 25, 2026 column:

        Accounts receivable, net of allowance of $73 at April 25, 2026
        and $69 at July 26, 2025 ................................. 6,480

    and the MD&A table "Accounts receivable, net $ 6,480 $ 6,701 $ (221)"
    prints the same figure. The oracle here used to say `6,500,000,000`,
    which is the note's sentence "Accounts receivable, net was $6.5 billion"
    — the same number rounded to two significant figures, tagged at decimals
    −8 against the balance sheet's −6. `pick_fact` sorted its two candidates
    on the id string, `"f-525" > "f-36"`, so the rounded one won and the
    published DSO was 37.3398 instead of 37.2249.
    """
    row = frame_row(table("CSCO"), "CY2026Q1")
    cell = row["ratios"]["days_sales_outstanding"]
    assert row["label"] == "Q-0"
    assert row["days"] == 91
    assert cell["inputs"]["receivables"]["value"] == 6480000000.0
    # companyfacts is EDGAR's own deduplication of the filing's cells and keeps
    # the precisely stated one, so the history states no `decimals` and the
    # rounded narrative cell is not in it at all. The instance still holds both,
    # and the precision rule that chooses between them is the test below.
    assert cell["inputs"]["receivables"]["record"] == "companyfacts"
    assert cell["inputs"]["receivables"]["decimals"] is None
    assert cell["inputs"]["revenue"]["value"] == 15841000000.0
    assert abs(cell["value"] - 6480000000.0 / 15841000000.0 * 91) <= 1e-9
    assert abs(cell["value"] - 37.2249226690) <= 1e-9


def test_the_more_precise_of_two_cells_for_one_fact_is_the_one_used():
    """The general rule behind the case above, stated on the pair itself."""
    facts = numbers("CSCO")["facts"]
    candidates = [fact for fact in facts
                  if fact["tag"] == "AccountsReceivableNetCurrent"
                  and fact["prefix"] == "us-gaap"
                  and (fact["context"] or {}).get("instant") == "2026-04-25"
                  and trends.usable(fact)]
    assert {fact["number"] for fact in candidates} == {6480000000.0, 6500000000.0}
    picked = trends.pick_fact(facts, "receivables",
                              {"start": "2026-01-25", "end": "2026-04-25", "days": 91})
    assert picked["number"] == 6480000000.0
    assert trends._precision(picked) == -6.0
    coarse = next(fact for fact in candidates if fact["number"] == 6500000000.0)
    assert trends._precision(coarse) == -8.0
    assert picked["id"] < coarse["id"]      # the id order would have chosen the other


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_emitted_change_subtracts_two_different_concepts(ticker):
    """`CONCEPTS` gives a term several acceptable tags and `pick_fact` takes the
    first the filings carry, so two periods of one ratio can rest on different
    us-gaap concepts. Subtracting those is not a change. 24 of 134 emitted
    changes did it, and ESCO's `deferred_revenue_diverging` input flipped sign."""
    payload = table(ticker)
    by_label = {row["label"]: row for row in payload["quarters"] + payload["years"]}
    checked = 0
    for row in payload["quarters"] + payload["years"]:
        for name, cell in row["ratios"].items():
            for key in ("year_over_year", "quarter_over_quarter"):
                entry = cell.get(key) or {}
                if "change" not in entry:
                    continue
                other = by_label[entry["against"]]["ratios"][name]
                mine = {term: got["tag"] for term, got in cell["inputs"].items()}
                theirs = {term: got["tag"] for term, got in other["inputs"].items()}
                assert mine == theirs, f"{ticker} {row['label']} {name} {key}"
                checked += 1
    assert checked, f"{ticker}: no change was emitted, so nothing was tested"


def test_a_refused_change_names_both_concepts():
    """The refusal has to be readable, or it is just an absence."""
    refusals = []
    for ticker in TICKERS:
        payload = table(ticker)
        for row in payload["quarters"] + payload["years"]:
            for cell in row["ratios"].values():
                for key in ("year_over_year", "quarter_over_quarter"):
                    entry = cell.get(key) or {}
                    if "different concept in each period" in (entry.get("reason") or ""):
                        refusals.append(entry["reason"])
    assert refusals, "no ratio in the fixture set changes concept between periods"
    for reason in refusals:
        assert reason.count("us-gaap:") >= 2


@pytest.mark.parametrize("ticker", TICKERS)
def test_coverage_separates_a_period_on_record_from_one_carrying_a_ratio(ticker):
    """A period is "on record" when the numbers hold any consolidated duration
    of that length. Cisco's Q-1, Q-2, Q-5 and Q-6 were on record on the strength
    of two share-repurchase facts and carried no ratio; "10 of 13 filled" was a
    true sentence about the wrong thing."""
    payload = table(ticker)
    rows_here = payload["quarters"] + payload["years"]
    coverage = payload["coverage"]
    assert coverage["periods_on_record"] == sum(1 for row in rows_here if row["filled"])
    assert coverage["periods_with_at_least_one_ratio"] == sum(
        1 for row in rows_here
        if row["filled"] and any("value" in cell for cell in row["ratios"].values()))
    assert coverage["periods_with_at_least_one_ratio"] <= coverage["periods_on_record"]


def test_the_command_reports_both_period_counts(tmp_path, capsys):
    source = tmp_path / "input_numbers.json"
    source.write_text(json.dumps(numbers("CSCO")), encoding="utf-8")
    assert trends.main(["--numbers", str(source),
                        "--out", str(tmp_path / "out.json")]) == 0
    printed = capsys.readouterr().out
    coverage = table("CSCO")["coverage"]
    assert f"{coverage['periods_with_at_least_one_ratio']} of 13 periods carry a ratio" \
        in printed
    assert f"{coverage['periods_on_record']} of 13 are on record" in printed


def test_carriers_gross_margin_is_missing_because_it_is_only_reported_by_segment():
    """The reason matters as much as the absence: Carrier tags cost of sales on
    the product and service axes and never as one consolidated number, so the
    ratio is not computable and the reader is told which of the three ways."""
    row = frame_row(table("CARR"), "CY2025")
    missing = row["ratios"]["gross_margin"]["missing"]
    assert "cost_of_revenue" in missing
    assert "only by segment" in missing


# --- (e) determinism ---------------------------------------------------------

def test_two_runs_are_byte_identical(tmp_path):
    source = tmp_path / "input_numbers.json"
    source.write_text(json.dumps(numbers("LFUS")), encoding="utf-8")
    first, second = tmp_path / "a.json", tmp_path / "b.json"
    assert trends.main(["--numbers", str(source), "--out", str(first)]) == 0
    assert trends.main(["--numbers", str(source), "--out", str(second)]) == 0
    assert first.read_bytes() == second.read_bytes()


def test_the_output_does_not_depend_on_the_order_of_the_facts_file(tmp_path):
    """Reversing the file must not change one digit — dict-ordering and
    'whichever came first' are the two ways this file could stop being
    reproducible."""
    payload = numbers("TTMI")
    reversed_facts = dict(payload)
    reversed_facts["facts"] = list(reversed(payload["facts"]))
    assert trends.render(trends.trends(reversed_facts)) == \
        trends.render(trends.trends(payload))


def test_the_command_rejects_a_file_that_is_not_the_numbers_file(tmp_path):
    bad = tmp_path / "no.json"
    bad.write_text('{"facts": []}', encoding="utf-8")
    assert trends.main(["--numbers", str(bad), "--out", str(tmp_path / "x.json")]) == 2
    missing = tmp_path / "nothing.json"
    assert trends.main(["--numbers", str(missing), "--out", str(tmp_path / "y.json")]) == 2


def test_an_empty_numbers_file_still_lists_all_thirteen_periods():
    payload = trends.trends({"ticker": "NONE", "facts": []})
    assert len(payload["coverage"]["quarters"]) == 8
    assert len(payload["coverage"]["years"]) == 5
    assert all(entry["status"] == "missing"
               for entry in payload["coverage"]["quarters"] + payload["coverage"]["years"])
    assert all(block["filled"] == 0 for block in payload["coverage"]["ratios"])


# --- (f) claim one: every ratio of six named periods, written out ------------
#
# Three companies with three fiscal calendars — Apple's year ends in September,
# Cisco's in July, Carrier's on 31 December — and two periods each, the newest
# quarter and the newest year the record reaches.
#
# Every figure below was read out of a source document and typed here. The
# companyfacts ones are the `val` EDGAR wrote under the accession beside them in
# `tests/fixtures/{ticker}/companyfacts.json.gz`. Carrier's June 2026 quarter is
# in no companyfacts row at all — EDGAR had not loaded that filing when the
# fixture was fetched — so its figures are the instance's own, and
# `tests/fixtures/CARR/10-Q/carr-20260630_htm.xml` carries revenue as
# `contextRef="c-15" decimals="-6" id="f-47" unitRef="usd">6351000000<`.
# Carrier's 2025 balance sheet is in both records and agrees in both; the
# instance wins it because the 10-Q that carries it was filed after any
# companyfacts row for that date, which is the point-in-time rule.
#
# Each ratio is the division written out term by term, so the arithmetic can be
# followed off the page. A ratio not listed under `ratios` is listed under
# `missing`, and the test checks both directions, so a value appearing where
# none should fails as loudly as one going missing.

APPLE_QUARTER = {
    "frame": "CY2026Q2", "period": ("2026-03-29", "2026-06-27", 91),
    "terms": {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                    109_417_000_000, "0000320193-26-000020", "companyfacts"),
        "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                            54_647_000_000, "0000320193-26-000020", "companyfacts"),
        "receivables": ("AccountsReceivableNetCurrent",
                        31_398_000_000, "0000320193-26-000020", "companyfacts"),
        "inventory": ("InventoryNet",
                      11_092_000_000, "0000320193-26-000020", "companyfacts"),
        "assets": ("Assets",
                   383_266_000_000, "0000320193-26-000020", "companyfacts"),
        "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                         51_431_000_000, "0000320193-26-000020",
                                         "companyfacts"),
        "cash": ("CashAndCashEquivalentsAtCarryingValue",
                 39_544_000_000, "0000320193-26-000020", "companyfacts"),
        "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                 9_538_000_000, "0000320193-26-000020", "companyfacts"),
    },
    "ratios": {
        "receivables_over_revenue": 31_398_000_000 / 109_417_000_000,
        "days_sales_outstanding": 31_398_000_000 / 109_417_000_000 * 91,
        "days_sales_of_inventory": 11_092_000_000 / 54_647_000_000 * 91,
        "gross_margin": (109_417_000_000 - 54_647_000_000) / 109_417_000_000,
        "soft_asset_share": (383_266_000_000 - 51_431_000_000 - 39_544_000_000)
        / 383_266_000_000,
        "contract_liabilities_over_revenue": 9_538_000_000 / 109_417_000_000,
    },
    # A 10-Q states cash flow for the year to date and never for the quarter, so
    # the quarter has no operating cash flow and the accruals ratio has no
    # numerator. Apple tags no inventory reserve at all, and its warranty
    # accrual and bad-debt allowance are annual.
    "missing": ("accruals_over_total_assets", "bad_debt_reserve_ratio",
                "inventory_reserve_ratio", "warranty_reserve_ratio", "non_gaap_gap"),
}

APPLE_YEAR = {
    "frame": "CY2025", "period": ("2024-09-29", "2025-09-27", 364),
    "terms": {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                    416_161_000_000, "0000320193-25-000079", "companyfacts"),
        "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                            220_960_000_000, "0000320193-25-000079", "companyfacts"),
        "net_income": ("NetIncomeLoss",
                       112_010_000_000, "0000320193-25-000079", "companyfacts"),
        "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                111_482_000_000, "0000320193-25-000079", "companyfacts"),
        "receivables": ("AccountsReceivableNetCurrent",
                        39_777_000_000, "0000320193-26-000020", "companyfacts"),
        "inventory": ("InventoryNet",
                      5_718_000_000, "0000320193-26-000020", "companyfacts"),
        "assets": ("Assets",
                   359_241_000_000, "0000320193-26-000020", "companyfacts"),
        "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                         49_834_000_000, "0000320193-26-000020",
                                         "companyfacts"),
        "cash": ("CashAndCashEquivalentsAtCarryingValue",
                 35_934_000_000, "0000320193-26-000020", "companyfacts"),
        "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                 9_055_000_000, "0000320193-26-000020", "companyfacts"),
    },
    "ratios": {
        "receivables_over_revenue": 39_777_000_000 / 416_161_000_000,
        "days_sales_outstanding": 39_777_000_000 / 416_161_000_000 * 364,
        "days_sales_of_inventory": 5_718_000_000 / 220_960_000_000 * 364,
        "accruals_over_total_assets": (112_010_000_000 - 111_482_000_000)
        / 359_241_000_000,
        "gross_margin": (416_161_000_000 - 220_960_000_000) / 416_161_000_000,
        "soft_asset_share": (359_241_000_000 - 49_834_000_000 - 35_934_000_000)
        / 359_241_000_000,
        "contract_liabilities_over_revenue": 9_055_000_000 / 416_161_000_000,
    },
    "missing": ("bad_debt_reserve_ratio", "inventory_reserve_ratio",
                "warranty_reserve_ratio", "non_gaap_gap"),
}

CISCO_QUARTER = {
    "frame": "CY2026Q1", "period": ("2026-01-25", "2026-04-25", 91),
    "terms": {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                    15_841_000_000, "0000858877-26-000078", "companyfacts"),
        "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                            5_761_000_000, "0000858877-26-000078", "companyfacts"),
        "receivables": ("AccountsReceivableNetCurrent",
                        6_480_000_000, "0000858877-26-000078", "companyfacts"),
        "bad_debt_allowance": ("AllowanceForDoubtfulAccountsReceivableCurrent",
                               73_000_000, "0000858877-26-000078", "companyfacts"),
        "inventory": ("InventoryNet",
                      4_708_000_000, "0000858877-26-000078", "companyfacts"),
        "warranty_accrual": ("ProductWarrantyAccrual",
                             371_000_000, "0000858877-26-000078", "companyfacts"),
        "assets": ("Assets",
                   125_546_000_000, "0000858877-26-000078", "companyfacts"),
        "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                         2_577_000_000, "0000858877-26-000078",
                                         "companyfacts"),
        "cash": ("CashAndCashEquivalentsAtCarryingValue",
                 7_083_000_000, "0000858877-26-000078", "companyfacts"),
        "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                 16_446_000_000, "0000858877-26-000078", "companyfacts"),
    },
    "ratios": {
        "receivables_over_revenue": 6_480_000_000 / 15_841_000_000,
        "days_sales_outstanding": 6_480_000_000 / 15_841_000_000 * 91,
        "days_sales_of_inventory": 4_708_000_000 / 5_761_000_000 * 91,
        "gross_margin": (15_841_000_000 - 5_761_000_000) / 15_841_000_000,
        "bad_debt_reserve_ratio": 73_000_000 / (6_480_000_000 + 73_000_000),
        "warranty_reserve_ratio": 371_000_000 / 15_841_000_000,
        "soft_asset_share": (125_546_000_000 - 2_577_000_000 - 7_083_000_000)
        / 125_546_000_000,
        "contract_liabilities_over_revenue": 16_446_000_000 / 15_841_000_000,
    },
    "missing": ("accruals_over_total_assets", "inventory_reserve_ratio",
                "non_gaap_gap"),
}

CISCO_YEAR = {
    "frame": "CY2025", "period": ("2024-07-28", "2025-07-26", 364),
    "terms": {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                    56_654_000_000, "0000858877-25-000111", "companyfacts"),
        "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                            19_864_000_000, "0000858877-25-000111", "companyfacts"),
        "net_income": ("NetIncomeLoss",
                       10_180_000_000, "0000858877-25-000111", "companyfacts"),
        "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                14_193_000_000, "0000858877-25-000111", "companyfacts"),
        "receivables": ("AccountsReceivableNetCurrent",
                        6_701_000_000, "0000858877-26-000078", "companyfacts"),
        "bad_debt_allowance": ("AllowanceForDoubtfulAccountsReceivableCurrent",
                               69_000_000, "0000858877-26-000078", "companyfacts"),
        "inventory": ("InventoryNet",
                      3_164_000_000, "0000858877-26-000078", "companyfacts"),
        "warranty_accrual": ("ProductWarrantyAccrual",
                             399_000_000, "0000858877-26-000078", "companyfacts"),
        "assets": ("Assets",
                   122_291_000_000, "0000858877-26-000078", "companyfacts"),
        "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                         2_113_000_000, "0000858877-26-000078",
                                         "companyfacts"),
        "cash": ("CashAndCashEquivalentsAtCarryingValue",
                 8_346_000_000, "0000858877-26-000078", "companyfacts"),
        "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                 16_416_000_000, "0000858877-26-000078", "companyfacts"),
    },
    "ratios": {
        "receivables_over_revenue": 6_701_000_000 / 56_654_000_000,
        "days_sales_outstanding": 6_701_000_000 / 56_654_000_000 * 364,
        "days_sales_of_inventory": 3_164_000_000 / 19_864_000_000 * 364,
        "accruals_over_total_assets": (10_180_000_000 - 14_193_000_000)
        / 122_291_000_000,
        "gross_margin": (56_654_000_000 - 19_864_000_000) / 56_654_000_000,
        "bad_debt_reserve_ratio": 69_000_000 / (6_701_000_000 + 69_000_000),
        "warranty_reserve_ratio": 399_000_000 / 56_654_000_000,
        "soft_asset_share": (122_291_000_000 - 2_113_000_000 - 8_346_000_000)
        / 122_291_000_000,
        "contract_liabilities_over_revenue": 16_416_000_000 / 56_654_000_000,
    },
    "missing": ("inventory_reserve_ratio", "non_gaap_gap"),
}

CARRIER_QUARTER = {
    "frame": "CY2026Q2", "period": ("2026-04-01", "2026-06-30", 91),
    "terms": {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                    6_351_000_000, "0001783180-26-000032", "xbrl_instance"),
        "receivables": ("ReceivablesNetCurrent",
                        3_246_000_000, "0001783180-26-000032", "xbrl_instance"),
        "inventory": ("InventoryNet",
                      2_759_000_000, "0001783180-26-000032", "xbrl_instance"),
        "inventory_reserve": ("InventoryValuationReserves",
                              328_000_000, "0001783180-26-000032", "xbrl_instance"),
        "warranty_accrual": ("ProductWarrantyAccrual",
                             935_000_000, "0001783180-26-000032", "xbrl_instance"),
        "assets": ("Assets",
                   37_372_000_000, "0001783180-26-000032", "xbrl_instance"),
        "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                         3_162_000_000, "0001783180-26-000032",
                                         "xbrl_instance"),
        "cash": ("CashAndCashEquivalentsAtCarryingValue",
                 1_344_000_000, "0001783180-26-000032", "xbrl_instance"),
        "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                 816_000_000, "0001783180-26-000032", "xbrl_instance"),
    },
    "ratios": {
        "receivables_over_revenue": 3_246_000_000 / 6_351_000_000,
        "days_sales_outstanding": 3_246_000_000 / 6_351_000_000 * 91,
        "inventory_reserve_ratio": 328_000_000 / 2_759_000_000,
        "warranty_reserve_ratio": 935_000_000 / 6_351_000_000,
        "soft_asset_share": (37_372_000_000 - 3_162_000_000 - 1_344_000_000)
        / 37_372_000_000,
        "contract_liabilities_over_revenue": 816_000_000 / 6_351_000_000,
    },
    # Carrier tags cost of sales on the product and service axes and never as a
    # consolidated total, so two ratios have no denominator and one has no
    # numerator.
    "missing": ("days_sales_of_inventory", "accruals_over_total_assets",
                "gross_margin", "bad_debt_reserve_ratio", "non_gaap_gap"),
}

CARRIER_YEAR = {
    "frame": "CY2025", "period": ("2025-01-01", "2025-12-31", 365),
    "terms": {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                    21_747_000_000, "0001783180-26-000008", "companyfacts"),
        "net_income": ("NetIncomeLoss",
                       1_484_000_000, "0001783180-26-000008", "companyfacts"),
        "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                2_513_000_000, "0001783180-26-000008", "companyfacts"),
        "bad_debt_allowance": ("AllowanceForDoubtfulAccountsReceivable",
                               81_000_000, "0001783180-26-000008", "companyfacts"),
        "receivables": ("ReceivablesNetCurrent",
                        2_639_000_000, "0001783180-26-000032", "xbrl_instance"),
        "inventory": ("InventoryNet",
                      2_483_000_000, "0001783180-26-000032", "xbrl_instance"),
        "inventory_reserve": ("InventoryValuationReserves",
                              337_000_000, "0001783180-26-000032", "xbrl_instance"),
        "warranty_accrual": ("ProductWarrantyAccrual",
                             893_000_000, "0001783180-26-000032", "xbrl_instance"),
        "assets": ("Assets",
                   37_190_000_000, "0001783180-26-000032", "xbrl_instance"),
        "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                         3_165_000_000, "0001783180-26-000032",
                                         "xbrl_instance"),
        "cash": ("CashAndCashEquivalentsAtCarryingValue",
                 1_555_000_000, "0001783180-26-000032", "xbrl_instance"),
        "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                 691_000_000, "0001783180-26-000032", "xbrl_instance"),
    },
    "ratios": {
        "receivables_over_revenue": 2_639_000_000 / 21_747_000_000,
        "days_sales_outstanding": 2_639_000_000 / 21_747_000_000 * 365,
        "accruals_over_total_assets": (1_484_000_000 - 2_513_000_000) / 37_190_000_000,
        "bad_debt_reserve_ratio": 81_000_000 / (2_639_000_000 + 81_000_000),
        "inventory_reserve_ratio": 337_000_000 / 2_483_000_000,
        "warranty_reserve_ratio": 893_000_000 / 21_747_000_000,
        "soft_asset_share": (37_190_000_000 - 3_165_000_000 - 1_555_000_000)
        / 37_190_000_000,
        "contract_liabilities_over_revenue": 691_000_000 / 21_747_000_000,
    },
    "missing": ("days_sales_of_inventory", "gross_margin", "non_gaap_gap"),
}

BY_HAND = {
    ("AAPL", "quarter"): APPLE_QUARTER, ("AAPL", "year"): APPLE_YEAR,
    ("CSCO", "quarter"): CISCO_QUARTER, ("CSCO", "year"): CISCO_YEAR,
    ("CARR", "quarter"): CARRIER_QUARTER, ("CARR", "year"): CARRIER_YEAR,
}


@pytest.mark.parametrize("ticker,kind", sorted(BY_HAND))
def test_every_ratio_of_a_named_period_is_the_arithmetic_written_out(ticker, kind):
    expected = BY_HAND[(ticker, kind)]
    row = frame_row(table(ticker), expected["frame"])
    assert (row["start"], row["end"], row["days"]) == expected["period"]
    assert set(expected["ratios"]) | set(expected["missing"]) == set(trends.RATIOS)

    for name, cell in row["ratios"].items():
        where = f"{ticker} {expected['frame']} {name}"
        if name in expected["missing"]:
            assert "value" not in cell, where
            assert cell["missing"], where
            continue
        assert "value" in cell, f"{where}: {cell.get('missing')}"
        assert abs(cell["value"] - expected["ratios"][name]) <= 1e-12, where
        assert set(cell["inputs"]) == set(trends.RATIOS[name]["terms"]), where
        for term, source in cell["inputs"].items():
            tag, value, accession, record = expected["terms"][term]
            assert (source["tag"], source["value"], source["accession"],
                    source["record"]) == (tag, float(value), accession, record), \
                f"{where} {term}"


def test_the_hand_written_periods_are_the_newest_the_record_reaches():
    """The six blocks above are each company's `Q-0` and `FY-0`, so they are
    the rows a reader looks at first and the rows a change lands in."""
    for (ticker, kind), expected in BY_HAND.items():
        row = frame_row(table(ticker), expected["frame"])
        assert row["label"] == ("Q-0" if kind == "quarter" else "FY-0"), ticker


# --- (g) the calendar frames -------------------------------------------------

def test_a_frame_is_a_calendar_frame_and_the_rows_are_consecutive():
    """`CY2025Q3`, not "the third quarter of fiscal 2025". The rows step back
    one calendar frame at a time, which is what makes `Q-0` against `Q-4` a
    year-over-year comparison and what lets a comparer line two companies up."""
    for ticker in TICKERS:
        payload = table(ticker)
        quarters = [row["frame"] for row in payload["quarters"]]
        years = [row["frame"] for row in payload["years"]]
        assert all(re.fullmatch(r"CY[0-9]{4}Q[1-4]", frame) for frame in quarters), ticker
        assert all(re.fullmatch(r"CY[0-9]{4}", frame) for frame in years), ticker
        for index, frame in enumerate(quarters):
            assert trends.step_back(quarters[0], index) == frame, ticker
        for index, frame in enumerate(years):
            assert trends.step_back(years[0], index) == frame, ticker
        assert [row["label"] for row in payload["quarters"]] == \
            [f"Q-{index}" for index in range(8)]
        assert [row["label"] for row in payload["years"]] == \
            [f"FY-{index}" for index in range(5)]


def test_the_frame_of_a_period_is_the_calendar_period_its_middle_day_is_in():
    """Written out on four periods with three fiscal calendars, so the rule can
    be checked without running it: the middle day, then the calendar period."""
    # 2026-03-29 to 2026-06-27 is 91 days; the 46th is 2026-05-13, in April to
    # June, so the second calendar quarter of 2026.
    assert trends.frame_of("2026-03-29", "2026-06-27", "quarter") == "CY2026Q2"
    # 2026-01-25 to 2026-04-25 is 91 days; the 46th is 2026-03-11, in January to
    # March. Cisco's third fiscal quarter is a first calendar one.
    assert trends.frame_of("2026-01-25", "2026-04-25", "quarter") == "CY2026Q1"
    # 2024-09-29 to 2025-09-27 is 364 days; the 183rd is 2025-03-30, in 2025.
    assert trends.frame_of("2024-09-29", "2025-09-27", "year") == "CY2025"
    # 2025-01-01 to 2025-12-31 is a calendar year and is its own frame.
    assert trends.frame_of("2025-01-01", "2025-12-31", "year") == "CY2025"


def test_a_frame_names_its_own_calendar_dates_and_steps_back_by_one():
    assert trends.frame_bounds("CY2025Q3") == (dt.date(2025, 7, 1), dt.date(2025, 9, 30))
    assert trends.frame_bounds("CY2025Q4") == (dt.date(2025, 10, 1), dt.date(2025, 12, 31))
    assert trends.frame_bounds("CY2021") == (dt.date(2021, 1, 1), dt.date(2021, 12, 31))
    assert trends.step_back("CY2025Q1", 1) == "CY2024Q4"
    assert trends.step_back("CY2026Q2", 4) == "CY2025Q2"
    assert trends.step_back("CY2025", 4) == "CY2021"


# Seagate's fiscal year ends within a day or two of 1 July, so its middle day
# lands on either side of New Year depending on whether the year ran 52 or 53
# weeks, and EDGAR's own stamps do not survive it either: EDGAR calls the year
# ending 2026-07-03 `CY2026` and the one ending 2025-06-27 `CY2024`, skipping
# `CY2025` for this company altogether, and it stamps `CY2023` on ten rows of
# the year ending 2023-06-30 while giving the same frame to the year ending
# 2024-06-28. Named as two periods rather than excused as a class, and asserted
# from both sides below, so the list cannot quietly grow.
FRAME_DIFFERS_FROM_EDGAR = {
    ("STX", "2025-06-28", "2026-07-03"): ("CY2025", "CY2026"),
    ("STX", "2022-07-02", "2023-06-30"): ("CY2022", "CY2023"),
}


def test_the_frame_rule_agrees_with_the_frames_edgar_stamped():
    """EDGAR stamps a `frame` on the row it treats as canonical for a calendar
    frame. Where it stamped one on a period this table fills, the rule here has
    to give the same answer — that is what makes the rule EDGAR's reading of the
    calendar and not this file's.

    A row pushed off a taken frame is compared against the frame it was pushed
    off, because that is what the rule computed for it.
    """
    checked, exceptions = 0, set()
    for ticker in TICKERS:
        stamps = companyfacts_source.stamped_frames(ticker)
        for row in rows(table(ticker)):
            if not row["filled"]:
                continue
            seen = stamps.get((row["start"], row["end"]))
            if not seen:
                continue
            checked += 1
            edgar = max(seen.items(), key=lambda pair: (pair[1], pair[0]))[0]
            computed = row["frame_shifted_from"] or row["frame"]
            key = (ticker, row["start"], row["end"])
            if key in FRAME_DIFFERS_FROM_EDGAR:
                assert (computed, edgar) == FRAME_DIFFERS_FROM_EDGAR[key], key
                exceptions.add(key)
                continue
            assert computed == edgar, f"{ticker} {row['label']} {row['start']}..{row['end']}"
    assert checked > 100, f"only {checked} filled periods carry an EDGAR stamp"
    # Both sides: every named exception has to still be one, or the list is an
    # excuse for something that stopped happening.
    assert exceptions == set(FRAME_DIFFERS_FROM_EDGAR)


def test_two_fiscal_years_claiming_one_frame_do_not_become_one_row():
    """The positive control for the push rule, on Seagate's own two years.

    Both compute `CY2022`. Without the rule one of them would overwrite the
    other and the five annual rows would be four years and a repeat.
    """
    assert trends.frame_of("2022-07-02", "2023-06-30", "year") == "CY2022"
    assert trends.frame_of("2021-07-03", "2022-07-01", "year") == "CY2022"
    taken = trends.by_frame([{"start": "2022-07-02", "end": "2023-06-30", "days": 364},
                             {"start": "2021-07-03", "end": "2022-07-01", "days": 364}],
                            "year")
    assert sorted(taken) == ["CY2021", "CY2022"]
    assert taken["CY2022"]["end"] == "2023-06-30"
    assert taken["CY2022"]["frame_shifted_from"] is None
    assert taken["CY2021"]["end"] == "2022-07-01"
    assert taken["CY2021"]["frame_shifted_from"] == "CY2022"


def test_seagates_five_annual_rows_are_five_consecutive_fiscal_years():
    """What the push rule buys: the year-over-year change subtracts the year
    before, not the year before that."""
    years = table("STX")["years"]
    assert [row["frame"] for row in years] == \
        ["CY2025", "CY2024", "CY2023", "CY2022", "CY2021"]
    assert [row["end"] for row in years] == \
        ["2026-07-03", "2025-06-27", "2024-06-28", "2023-06-30", "2022-07-01"]
    ends = [dt.date.fromisoformat(row["end"]) for row in years]
    for newer, older in zip(ends, ends[1:]):
        assert trends.YEAR_DAYS[0] <= (newer - older).days <= trends.YEAR_DAYS[1]
    assert [(row["frame"], row["frame_shifted_from"]) for row in years
            if row["frame_shifted_from"]] == [("CY2021", "CY2022")]


def test_year_over_year_compares_the_same_calendar_quarter_a_year_earlier():
    for ticker in TICKERS:
        payload = table(ticker)
        labelled = {row["label"]: row for row in rows(payload)}
        for row in payload["quarters"]:
            for cell in row["ratios"].values():
                against = cell["year_over_year"].get("against")
                if against is None:
                    continue
                assert labelled[against]["frame"] == trends.step_back(row["frame"], 4)
                other = cell["quarter_over_quarter"].get("against")
                if other is not None:
                    assert labelled[other]["frame"] == trends.step_back(row["frame"], 1)


# --- (h) the two records, and where each cell came from ----------------------

def test_the_table_reaches_filings_the_fixture_set_does_not_hold():
    """The point of reading companyfacts: a cell whose accession is in no
    document this fixture set committed is a number the instance could not have
    supplied. Eight quarters and five years do not fit in one 10-K and one 10-Q.
    """
    for ticker in TICKERS:
        held = {row["accession"] for form in ("10-K", "10-Q", "8-K")
                for row in cutoff_guard.documents(ticker, form=form)}
        used = {source["accession"] for row in rows(table(ticker))
                for cell in row["ratios"].values()
                for source in (cell.get("inputs") or {}).values()}
        assert used - held, f"{ticker}: every cell came from a committed filing"
        assert used & held, f"{ticker}: no cell came from a committed filing"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_accessions_companyfacts_has_not_loaded_are_named(ticker):
    """EDGAR loads companyfacts filing by filing and runs behind. Which filings
    it had not reached is the source's own gap, and the table names it rather
    than leaving a reader to notice a quarter is thin.

    Checked against the companyfacts document itself, which is what says which
    accessions it holds rows from.
    """
    payload = table(ticker)
    named = {entry["accession"]
             for entry in payload["source"]["accessions_with_no_companyfacts_row"]}
    loaded = companyfacts_source.accessions(ticker)
    held = {row["accession"] for form in ("10-K", "10-Q")
            for row in cutoff_guard.documents(ticker, form=form)
            if row["accession"]}
    assert named == held - loaded


def test_the_two_quarterlies_edgar_had_not_loaded_are_read_out_of_the_instance():
    """Carrier's and Littelfuse's July 2026 quarterlies are in no companyfacts
    row, so the quarter each reports has nothing in the history to look up. It
    is read out of the filing's own XBRL instead, and every cell says so — the
    one thing it must not be is a zero.
    """
    for ticker, accession, frame in (("CARR", "0001783180-26-000032", "CY2026Q2"),
                                     ("LFUS", "0001628280-26-050481", "CY2026Q2")):
        payload = table(ticker)
        assert [entry["accession"] for entry
                in payload["source"]["accessions_with_no_companyfacts_row"]] == [accession]
        row = frame_row(payload, frame)
        assert row["filled"], ticker
        filled = [cell for cell in row["ratios"].values() if "value" in cell]
        assert filled, ticker
        for cell in filled:
            assert cell["value"] != 0
            for term, source in cell["inputs"].items():
                assert source["record"] == "xbrl_instance", f"{ticker} {term}"
                assert source["accession"] == accession
                assert source["value"] != 0


# --- (i) the cutoff ----------------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_no_fact_filed_after_the_cutoff_reaches_a_cell(ticker):
    payload = table(ticker)
    cutoff = payload["cutoff"]
    assert cutoff
    for row in rows(payload):
        for cell in row["ratios"].values():
            for source in (cell.get("inputs") or {}).values():
                assert source["filed"] <= cutoff, f"{ticker} {source['fact_id']}"


def test_an_earlier_cutoff_takes_the_later_filings_back_out():
    """companyfacts is a catalogue of many filings, so the cutoff is applied to
    its rows and not to the document. Apple's ten-K run stops at 2025-10-31, and
    everything the four filings after it reported has to be gone — the value a
    later filing restated included.
    """
    early = trends.trends(dict(numbers("AAPL"), cutoff="2025-10-31"))
    assert early["cutoff"] == "2025-10-31"
    filed = [source["filed"] for row in rows(early)
             for cell in row["ratios"].values()
             for source in (cell.get("inputs") or {}).values()]
    assert filed
    assert max(filed) <= "2025-10-31"

    # The window ends where the record does. Apple's fourth fiscal quarter is
    # reported only inside the year, so at this cutoff the newest quarter on
    # record is the one ending 2025-06-28.
    assert early["quarters"][0]["frame"] == "CY2025Q2"
    assert early["quarters"][0]["end"] == "2025-06-28"
    assert early["years"][0]["frame"] == "CY2025"
    assert early["years"][0]["end"] == "2025-09-27"

    # And the balance-sheet terms now name the ten-K rather than the July 2026
    # ten-Q that repeated them.
    cell = frame_row(early, "CY2025")["ratios"]["soft_asset_share"]
    assert cell["inputs"]["assets"]["accession"] == "0000320193-25-000079"
    assert cell["inputs"]["assets"]["value"] == 359241000000.0


# --- (j) what is absent, and why ---------------------------------------------

def test_a_quarter_absent_because_it_is_the_fourth_names_the_year_that_covers_it():
    """Apple's fourth fiscal quarter is never reported as a quarter — it is the
    year less the nine months — so `CY2025Q3` is empty. The reason names the
    frame and the annual period that covers it, which is where the quarter
    went. Deriving it from there is a separate piece of work.

    Those two period dates are Apple's own fiscal year, stated by the 10-K
    filed on 2025-10-31 — inside the cutoff, and so allowed in a bundle. The
    frame's own calendar dates are not printed anywhere: see `trends._absent`.
    """
    entry = {row["frame"]: row for row in table("AAPL")["coverage"]["quarters"]}["CY2025Q3"]
    assert entry["status"] == "missing"
    assert "target_end" not in entry
    # The frame, then a semicolon: not "CY2025Q3 (2025-07-01..2025-09-30)".
    assert "quarter-length period in CY2025Q3;" in entry["reason"]
    assert "2024-09-29..2025-09-27" in entry["reason"]
    assert "(CY2025) covers it" in entry["reason"]


ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def test_every_absent_frame_names_itself_and_stays_inside_the_cutoff():
    """Both halves matter. A frame with no period says which frame, so nothing
    is dropped silently; and every date in the sentence is one a filing stated
    at or before the cutoff. The frame's own calendar dates are not spelled
    out, because they can fall after it — Apple's fiscal 2025 sits in CY2025,
    which ends two months after the 10-K that reported it was filed — and
    `src/assemble_bundle.py` puts this file in front of the predictor.

    Generac is why the claim is the cutoff and not "no calendar date": its
    fiscal year *is* the calendar year, so the annual period that covers its
    empty CY2025Q4 really does end on 2025-12-31. That date is the filing's,
    and inside the cutoff. `trends._absent` is where the frame's own bounds are
    left out, and the test above pins the shape on Apple.
    """
    seen = 0
    for ticker in TICKERS:
        payload = table(ticker)
        cutoff = payload["cutoff"]
        for entry in payload["coverage"]["quarters"] + payload["coverage"]["years"]:
            if entry["status"] != "missing":
                continue
            seen += 1
            assert entry["frame"] in entry["reason"], (ticker, entry["frame"])
            for date in ISO_DATE.findall(entry["reason"]):
                assert date <= cutoff, (ticker, entry["frame"], date, cutoff)
    # A floor, not a count: pinning the number of absences would be an expected
    # value read off a run of the table. This only says the loop had work to do.
    assert seen > 5, f"only {seen} frames were absent, so little was checked"


def test_a_term_reported_only_by_segment_here_is_told_apart_from_one_never_reported():
    """Three absences a reader would act on differently, and the message says
    which. Carrier's cost of sales is the middle one: companyfacts holds it as a
    consolidated total for 2022, 2023 and 2024, and the 2025 filing puts it on
    the product and service axes only."""
    facts = [{"id": "x:1", "tag": "CostOfRevenue", "prefix": "us-gaap", "number": 5.0,
              "nil": False, "unit": "iso4217:USD", "filing_date": "2026-01-01",
              "source_accession": "x",
              "context": {"start": "2025-01-01", "end": "2025-03-31",
                          "segment": [{"dimension": "srt:ProductOrServiceAxis",
                                       "member": "us-gaap:ProductMember"}]}}]
    period = {"start": "2025-01-01", "end": "2025-03-31", "days": 90}
    assert "never as a consolidated total" in \
        trends.why_missing(facts, "cost_of_revenue", period)

    elsewhere = dict(facts[0], id="x:2",
                     context={"start": "2024-01-01", "end": "2024-03-31", "segment": []})
    both = trends.why_missing(facts + [elsewhere], "cost_of_revenue", period)
    assert "a consolidated total in other periods" in both
    assert "only by segment" in both

    other_period = {"start": "2023-01-01", "end": "2023-03-31", "days": 90}
    assert "reported, but not for this period" in \
        trends.why_missing([elsewhere], "cost_of_revenue", other_period)

    # The fourth: the tag is there and is not money. Every ratio here divides
    # one dollar figure by another, so a share count is not a candidate and the
    # message must not call it one.
    shares = dict(elsewhere, id="x:3", unit="shares")
    assert "as an amount in USD" in \
        trends.why_missing([shares], "cost_of_revenue", period)


def test_only_a_plain_dollar_amount_is_a_term():
    """The two records write the unit differently and a per-share figure writes
    a divide. All three have to be told apart by one rule."""
    assert trends.money({"unit": "iso4217:USD"})
    assert trends.money({"unit": "USD"})
    assert not trends.money({"unit": "shares"})
    assert not trends.money({"unit": "xbrli:shares"})
    assert not trends.money({"unit": "USD/shares"})
    assert not trends.money({"unit": "iso4217:USD/xbrli:shares"})
    assert not trends.money({})


def test_a_company_with_no_companyfacts_document_says_so_and_fills_nothing():
    """Fail closed and say why. The table is still thirteen named frames."""
    payload = trends.trends({"ticker": "NONE", "facts": []})
    assert payload["source"]["companyfacts"]["read"] is False
    assert "NONE" in payload["source"]["companyfacts"]["reason"]
    assert len(payload["coverage"]["quarters"]) == 8
    assert len(payload["coverage"]["years"]) == 5


# --- (k) the catalogue, on a document small enough to read -------------------
#
# The twelve committed documents are ninety megabytes and every row in them is
# EDGAR's. These four tests are the rules stated on a document written here, so
# each has a positive control beside its refusal: a companyfacts row filed after
# the cutoff is dropped, a document whose bytes changed is refused, and the date
# gate that would refuse the whole catalogue does not apply to it.

def _catalogue(tmp_path, *, sha=None, filing_date="2026-07-30", ticker="TEST"):
    """A fixture tree holding one small companyfacts document and its manifest."""
    facts = {
        "Revenues": {"units": {"USD": [
            {"start": "2026-01-01", "end": "2026-03-31", "val": 100, "accn": "first",
             "fy": 2026, "fp": "Q1", "form": "10-Q", "filed": "2026-04-30"},
            {"start": "2026-04-01", "end": "2026-06-30", "val": 200, "accn": "second",
             "fy": 2026, "fp": "Q2", "form": "10-Q", "filed": "2026-07-30"}]}},
        "AccountsReceivableNetCurrent": {"units": {"USD": [
            {"end": "2026-03-31", "val": 10, "accn": "first",
             "fy": 2026, "fp": "Q1", "form": "10-Q", "filed": "2026-04-30"},
            {"end": "2026-06-30", "val": 20, "accn": "second",
             "fy": 2026, "fp": "Q2", "form": "10-Q", "filed": "2026-07-30"}]}},
    }
    folder = tmp_path / ticker
    folder.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps({"ticker": ticker, "cik": "0000000001", "as_of": "2026-09-01",
                       "url": "", "note": "", "entity_name": "Test Company",
                       "facts": {"us-gaap": facts}}, indent=2) + "\n").encode("utf-8")
    (folder / "companyfacts.json").write_bytes(raw)
    (folder / "manifest.json").write_text(json.dumps({
        "ticker": ticker, "cik": "0000000001", "as_of": "2026-09-01",
        "source": "EDGAR",
        "documents": [{"form": "companyfacts", "role": "standard_taxonomy_history",
                       "accession": "", "filing_date": filing_date, "report_date": "",
                       "items": "", "date_basis": "a catalogue, not a filing",
                       "url": "", "path": "companyfacts.json", "stored": "identity",
                       "bytes": len(raw),
                       "sha256": sha or hashlib.sha256(raw).hexdigest()}]}, indent=2))
    return tmp_path


def _test_table(root, cutoff):
    return trends.trends({"ticker": "TEST", "cutoff": cutoff, "facts": []},
                         fixtures_root=root)


def test_the_catalogue_is_read_even_though_its_own_date_is_after_the_cutoff():
    """The positive control for the rule the module's docstring states: a
    catalogue is not a filing, so the date gate that refuses a document filed
    after the cutoff does not refuse this one. Its newest row is dated after the
    cutoff below, and the document is still read."""
    with tempfile.TemporaryDirectory() as folder:
        root = _catalogue(Path(folder), filing_date="2026-07-30")
        payload = _test_table(root, "2026-05-31")
        stored = json.loads((root / "TEST" / "manifest.json").read_text())
        assert stored["documents"][0]["filing_date"] == "2026-07-30" > "2026-05-31"
        assert payload["source"]["companyfacts"]["read"] is True
        assert payload["source"]["companyfacts"]["rows"] == 2
        # And the date the payload reports is the newest row it kept, not the
        # newest row the catalogue holds.
        assert payload["source"]["companyfacts"]["filed_through"] == "2026-04-30"


def test_a_catalogue_row_filed_after_the_cutoff_is_dropped():
    with tempfile.TemporaryDirectory() as folder:
        root = _catalogue(Path(folder))

        whole = _test_table(root, "2026-09-01")
        assert whole["quarters"][0]["frame"] == "CY2026Q2"
        cell = whole["quarters"][0]["ratios"]["receivables_over_revenue"]
        assert cell["value"] == 20 / 200
        assert cell["inputs"]["revenue"]["accession"] == "second"

        early = _test_table(root, "2026-05-31")
        assert early["source"]["companyfacts"]["rows"] == 2
        assert early["quarters"][0]["frame"] == "CY2026Q1"
        cell = early["quarters"][0]["ratios"]["receivables_over_revenue"]
        assert cell["value"] == 10 / 100
        assert cell["inputs"]["revenue"]["accession"] == "first"
        assert "second" not in json.dumps(early)


def test_a_catalogue_that_is_no_longer_the_bytes_the_manifest_hashed_is_refused():
    """A fixture is a record. The date gate does not apply to a catalogue, so
    the sha256 is the check that it is still the document that was fetched."""
    with tempfile.TemporaryDirectory() as folder:
        root = _catalogue(Path(folder), sha="0" * 64)
        payload = _test_table(root, "2026-09-01")
        assert payload["source"]["companyfacts"]["read"] is False
        assert "no longer the bytes" in payload["source"]["companyfacts"]["reason"]
        assert all(not row["filled"] for row in rows(payload))


def test_the_committed_catalogues_are_still_the_bytes_their_manifests_hashed():
    """The other side of the test above: read for all twelve, every day the gate
    runs, so the refusal is not a rule about a file nobody opens."""
    for ticker in TICKERS:
        assert table(ticker)["source"]["companyfacts"]["read"] is True, ticker
        assert table(ticker)["source"]["companyfacts"]["rows"] > 1000, ticker
