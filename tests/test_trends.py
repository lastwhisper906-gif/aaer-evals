"""Every number in the trend table, recomputed here from the fact ids it names.

The test holds its own copy of the eleven formulas and its own fact lookup, so
a ratio passes only if the value in `input_trends.json` can be reproduced by a
reader who has `input_numbers.json` and the formula string — which is the whole
claim of the file. Three of them are also checked against numbers typed in by
hand off the filings, because a formula table that agrees with itself proves
nothing about the filing.

The other half is the absences. Six of thirteen requested periods are not in
the fixture set and several ratios are in no filing at all; the tests assert
that each one is named with a reason and that none of them was quietly filled
with a zero.
"""

from __future__ import annotations

import functools
import json
import re
from pathlib import Path

import pytest

from src import extract_numbers, trends
from src.fetch_fixtures import TICKERS


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
    import datetime as dt
    return (dt.date.fromisoformat(row["end"]) - dt.date.fromisoformat(row["start"])).days + 1


# The eleven formulas again, written out here rather than imported. `v` is the
# term values looked up from `input_numbers.json` by fact id.
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
    """docs/INPUT_SPEC.md §4 item 1, all eleven, no extras."""
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
    facts = by_id(ticker)
    checked = 0
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            if "value" not in cell:
                continue
            values = {}
            for term, source in cell["inputs"].items():
                fact = facts.get(source["fact_id"])
                assert fact is not None, f"{ticker} {row['label']} {name} {term}"
                assert fact["tag"] == source["tag"]
                assert fact["number"] == source["value"]
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
    balance-sheet term is the instant at its end."""
    facts = by_id(ticker)
    for row in rows(table(ticker)):
        for cell in row["ratios"].values():
            for term, source in cell.get("inputs", {}).items():
                context = facts[source["fact_id"]]["context"]
                if trends.CONCEPTS[term][0] == "duration":
                    assert (context["start"], context["end"]) == (row["start"], row["end"])
                else:
                    assert context["instant"] == row["end"]
                assert not context["segment"]


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
    """An honest zero. `input_numbers.json` carries us-gaap and dei facts, and
    a non-GAAP measure is neither — so the gap needs the 8-K exhibit, and this
    file says so instead of inventing it."""
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
    payload = table(ticker)
    assert payload["coverage"]["requested"] == {"quarters": 8, "years": 5}
    assert [row["label"] for row in payload["coverage"]["quarters"]] == \
        [f"Q-{index}" for index in range(8)]
    assert [row["label"] for row in payload["coverage"]["years"]] == \
        [f"FY-{index}" for index in range(5)]
    for entry in payload["coverage"]["quarters"] + payload["coverage"]["years"]:
        assert entry["status"] in ("filled", "missing")
        if entry["status"] == "missing":
            assert entry["reason"] and entry["target_end"]
            assert entry["target_end"] in entry["reason"]
        else:
            assert entry["start"] < entry["end"]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_fixture_set_cannot_fill_thirteen_periods_and_says_which(ticker):
    """The honest result of a one-10-K, one-10-Q input: some periods are simply
    not there. The test asserts the shortfall is reported, not that it is small."""
    payload = table(ticker)
    missing = [entry for entry in payload["coverage"]["quarters"] + payload["coverage"]["years"]
               if entry["status"] == "missing"]
    assert missing, f"{ticker}: all thirteen periods filled — check the fixtures"
    assert len(missing) == 13 - sum(1 for row in rows(payload) if row["filled"])


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
    row = {r["label"]: r for r in table("AAPL")["years"]}["FY-0"]
    cell = row["ratios"]["gross_margin"]
    assert cell["inputs"]["revenue"]["value"] == 416161000000.0
    assert cell["inputs"]["cost_of_revenue"]["value"] == 220960000000.0
    assert abs(cell["value"] - (416161000000.0 - 220960000000.0) / 416161000000.0) <= 1e-12


def test_nvidias_latest_quarter_gross_margin_is_the_filings_own_arithmetic():
    """NVDA's quarter: revenue $96,221m, cost of revenue $24,079m."""
    row = {r["label"]: r for r in table("NVDA")["quarters"]}["Q-0"]
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
    row = {r["label"]: r for r in table("CSCO")["quarters"]}["Q-0"]
    cell = row["ratios"]["days_sales_outstanding"]
    assert row["days"] == 91
    assert cell["inputs"]["receivables"]["value"] == 6480000000.0
    assert cell["inputs"]["receivables"]["decimals"] == "-6"
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
    row = {r["label"]: r for r in table("CARR")["years"]}["FY-0"]
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
