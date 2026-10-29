"""Contract liabilities split and billings, judged against the filings.

docs/HEDGE_FUND_ANALYSIS.md §5.2 row 19. Expected values, read by eye from the
committed filings and through `tests/companyfacts_source.py` (which imports
nothing from `src/`):

- **Fortinet's billings.** The 10-K filed 2026-02-25
  (`tests/fixtures/FTNT/10-K/ftnt-20251231.htm.gz`), Key Metrics: "We define
  billings as revenue recognized in accordance with generally accepted
  accounting principles ... plus the change in deferred revenue from the
  beginning to the end of the period less any deferred revenue balances
  acquired from business combinations during the period", and "Total billings
  were $7.55 billion in 2025". The reconciliation: revenue 6,799.6, change in
  deferred revenue 754.9, less deferred revenue acquired (0.8), billings
  7,553.7; for 2024, 5,955.8 + 625.9 - 49.2 = 6,532.5. Deferred revenue
  7,115.8, 6,360.9 and 5,735.0 at the three year ends (millions).
- **Arista's balances.** The 10-K filed 2026-02-17
  (`tests/fixtures/ANET/10-K/anet-20251231.htm`): deferred revenue 4,002.6 and
  1,727.3, non-current 1,369.8 and 1,064.1 (balance sheet); deferred cost of
  goods sold 1,197.0 and 291.3 (prepaid expenses note); and the deferred
  revenue rollforward, beginning balance 2,791.4, revenue recognized from
  beginning balance (1,691.5), ending balance 5,372.4 (millions).
"""

from __future__ import annotations

import json

import pytest

from src import calculator
from tests import companyfacts_source as source

MILLION = 1_000_000
SECTION = "contract_liabilities_and_billings"

FTNT = {"ticker": "FTNT", "cutoff": "2026-02-25", "period_end": "2025-12-31", "form": "10-K"}
ANET = {"ticker": "ANET", "cutoff": "2026-02-17", "period_end": "2025-12-31", "form": "10-K"}


@pytest.fixture(scope="module")
def fortinet():
    return calculator.calculate(**FTNT)


@pytest.fixture(scope="module")
def arista():
    return calculator.calculate(**ANET)


def deferred_revenue(ticker: str, date: str, cutoff: str) -> float:
    return (source.one_value(ticker, "DeferredRevenueCurrent", date, cutoff)
            + source.one_value(ticker, "DeferredRevenueNoncurrent", date, cutoff))


# --- Fortinet: billings under its own definition --------------------------------------------

def test_fortinets_rows_are_the_printed_figures():
    cut = FTNT["cutoff"]
    assert deferred_revenue("FTNT", "2025-12-31", cut) == pytest.approx(7_115.8 * MILLION)
    assert deferred_revenue("FTNT", "2024-12-31", cut) == pytest.approx(6_360.9 * MILLION)
    assert deferred_revenue("FTNT", "2023-12-31", cut) == pytest.approx(5_735.0 * MILLION)
    revenue = source.one_value("FTNT", "RevenueFromContractWithCustomerExcludingAssessedTax",
                               "2025-01-01..2025-12-31", cut)
    assert revenue == 6_799.6 * MILLION


def test_billings_are_fortinets_within_rounding(fortinet):
    """Revenue plus the change in deferred revenue, in millions:

      6,799.6 + (7,115.8 - 6,360.9) = 6,799.6 + 754.9 = 7,554.5

    Fortinet prints 7,553.7 after subtracting 0.8 of deferred revenue acquired in
    business combinations, which no fact in the record states over a period, so
    the figure here is the company's plus that 0.8 -- "$7.55 billion" either way.
    """
    cell = fortinet[SECTION]["billings"]
    assert cell["value"] == pytest.approx(7_554.5 * MILLION)
    assert abs(cell["value"] - 7.55e9) < 0.005e9          # the printed $7.55 billion
    assert cell["value"] - 7_553.7 * MILLION == pytest.approx(0.8 * MILLION)
    acquired = cell["contract_liabilities_acquired_in_business_combinations"]
    assert acquired["value"] is None and "none is subtracted" in acquired["missing"]
    assert cell["unit"] == "USD"


def test_the_change_is_read_under_one_tag_at_both_ends(fortinet):
    """The 10-K tags DeferredRevenueCurrent; the 10-Qs before it tagged the same
    balance ContractWithCustomerLiabilityCurrent. Both ends of the change are read
    under the tag the record carries at both."""
    change = fortinet[SECTION]["billings"]["inputs"]["change_in_contract_liabilities"]
    for end in ("at_the_end", "a_year_before"):
        parts = change["inputs"][end]["parts"]
        assert parts["current"]["tag"] == "DeferredRevenueCurrent", end
        assert parts["noncurrent"]["tag"] == "DeferredRevenueNoncurrent", end
        assert parts["current"]["accession"] == "0001262039-26-000007", end
        assert parts["current"]["filed"] == "2026-02-25", end


def test_billings_growth_less_revenue_growth_is_worked_by_hand(fortinet):
    """A year earlier: 5,955.8 + (6,360.9 - 5,735.0) = 6,581.7 (Fortinet: 6,532.5
    after 49.2 acquired). So, in millions,

      (7,554.5 / 6,581.7 - 1) - (6,799.6 / 5,955.8 - 1) = 0.147804... - 0.141677...
    """
    assert fortinet[SECTION]["billings_a_year_earlier"]["value"] == pytest.approx(6_581.7 * MILLION)
    expected = (7_554.5 - 6_581.7) / 6_581.7 - (6_799.6 - 5_955.8) / 5_955.8
    cell = fortinet[SECTION]["billings_growth_minus_revenue_growth"]
    assert cell["value"] == pytest.approx(expected, rel=1e-9)


def test_duration_is_the_noncurrent_share(fortinet):
    """3,479.8 / (3,636.0 + 3,479.8) = 3,479.8 / 7,115.8."""
    cell = fortinet[SECTION]["contract_liability_duration"]
    assert cell["value"] == pytest.approx(3_479.8 / 7_115.8, rel=1e-9)


# --- Arista: the balances, the rollforward and deferred cost --------------------------------

def test_aristas_balances_are_the_printed_figures(arista):
    balances = arista[SECTION]["balances"]
    now, ago = balances["contract_liabilities_now"], balances["contract_liabilities_a_year_earlier"]
    millions = lambda cell: pytest.approx(cell["value"] / MILLION, abs=1e-6)  # noqa: E731
    assert millions(now["parts"]["current"]) == 4_002.6
    assert millions(ago["parts"]["current"]) == 1_727.3
    assert millions(now["parts"]["noncurrent"]) == 1_369.8
    assert millions(ago["parts"]["noncurrent"]) == 1_064.1
    assert millions(balances["deferred_cost_now"]) == 1_197.0
    assert millions(balances["deferred_cost_a_year_earlier"]) == 291.3
    cut = ANET["cutoff"]
    assert source.one_value("ANET", "DeferredCostsCurrent", "2025-12-31", cut) == 1_197_000_000
    assert source.one_value("ANET", "ContractWithCustomerLiabilityCurrent", "2025-12-31", cut) \
        == 4_002_600_000


def test_aristas_duration_and_revenue_from_the_opening_balance(arista):
    """Duration: 1,369.8 / (4,002.6 + 1,369.8) = 1,369.8 / 5,372.4.
    The rollforward: 1,691.5 recognized from a beginning balance of 2,791.4
    (1,727.3 + 1,064.1), so 1,691.5 / 2,791.4."""
    section = arista[SECTION]
    assert section["contract_liability_duration"]["value"] == pytest.approx(1_369.8 / 5_372.4,
                                                                            rel=1e-9)
    cell = section["revenue_from_opening_contract_liabilities"]
    assert cell["value"] == pytest.approx(1_691.5 / 2_791.4, rel=1e-9)
    recognized = cell["inputs"]["revenue_recognized_from_opening_balance"]
    assert (recognized["tag"], recognized["accession"], recognized["filed"]) == (
        "ContractWithCustomerLiabilityRevenueRecognized", "0001596532-26-000013", "2026-02-17")


def test_deferred_cost_over_product_deferred_revenue_is_null_where_no_product_split_is_filed(
        arista, tmp_path):
    """Arista's filing states no product deferred revenue (its instance has no
    contract liability on the product axis), so the ratio is null with the reason,
    with no bundle and with one that holds nothing on that axis."""
    cell = arista[SECTION]["deferred_cost_over_product_deferred_revenue"]
    assert cell["value"] is None and "no run bundle was given" in cell["missing"]
    (tmp_path / "input_numbers.json").write_text(json.dumps({"facts": []}), encoding="utf-8")
    out = calculator.calculate(**ANET, bundle=tmp_path)
    cell = out[SECTION]["deferred_cost_over_product_deferred_revenue"]
    assert cell["value"] is None
    assert "states no fact on srt:ProductOrServiceAxis = us-gaap:ProductMember" in cell["missing"]


def test_a_planted_product_deferred_revenue_is_divided_into_deferred_cost(tmp_path):
    """A value the test plants: 3,000.0 million of contract liabilities on the
    product axis at 2025-12-31, so 1,197.0 / 3,000.0 = 0.399. A planted service
    fact beside it is not read."""
    def fact(member: str, number: float, ident: str) -> dict:
        return {"id": ident, "tag": "ContractWithCustomerLiability", "prefix": "us-gaap",
                "unit": "iso4217:USD", "number": number, "nil": False, "form": "10-K",
                "context": {"instant": "2025-12-31",
                            "segment": [{"dimension": "srt:ProductOrServiceAxis", "member": member}]},
                "source_accession": "0001596532-26-000013", "filing_date": "2026-02-17"}
    facts = [fact("us-gaap:ProductMember", 3_000.0 * MILLION, "P:f-1"),
             fact("us-gaap:ServiceMember", 2_372.4 * MILLION, "P:f-2")]
    (tmp_path / "input_numbers.json").write_text(json.dumps({"facts": facts}), encoding="utf-8")
    out = calculator.calculate(**ANET, bundle=tmp_path)
    cell = out[SECTION]["deferred_cost_over_product_deferred_revenue"]
    assert cell["value"] == pytest.approx(1_197.0 / 3_000.0, rel=1e-12)
    assert cell["inputs"]["product_deferred_revenue"]["id"] == "P:f-1"


def test_the_section_reaches_the_filings_only_view(fortinet):
    view = calculator.filings_only(fortinet)
    assert view[SECTION]["billings"]["value"] == fortinet[SECTION]["billings"]["value"]


def test_a_noncurrent_line_never_tagged_leaves_billings_null_not_current_alone():
    """Planted: current deferred revenue at three year ends and no noncurrent or
    total line in any filing. The noncurrent line is not read as a zero, so the
    balance, the change and billings are null with the reason."""
    def instant(end: str, value: float) -> dict:
        return {"end": end, "val": value, "accn": "P-1", "form": "10-K", "filed": "2026-02-01"}

    def year(start: str, end: str, value: float) -> dict:
        return {"start": start, "end": end, "val": value, "accn": "P-1", "form": "10-K",
                "filed": "2026-02-01"}
    record = calculator.Record({"ticker": "TEST", "facts": {"us-gaap": {
        "Revenues": {"units": {"USD": [year("2025-01-01", "2025-12-31", 1_000.0),
                                       year("2024-01-01", "2024-12-31", 900.0),
                                       year("2023-01-01", "2023-12-31", 800.0)]}},
        "DeferredRevenueCurrent": {"units": {"USD": [instant("2025-12-31", 300.0),
                                                     instant("2024-12-31", 250.0),
                                                     instant("2023-12-31", 200.0)]}}}}})
    periods = calculator.trigger_periods(record.usd, "2025-12-31", "10-K")
    terms = calculator.gather(record, periods)
    section = calculator.contract_liabilities_and_billings(record, terms, periods, [])
    assert section["billings"]["value"] is None
    assert "contract_liabilities_noncurrent" in section["billings"]["missing"]
    assert section["balances"]["contract_liabilities_now"]["value"] is None
