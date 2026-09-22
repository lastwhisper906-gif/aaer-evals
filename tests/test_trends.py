"""The trend table, judged against the companyfacts record and against the filings.

Two claims, because "every ratio for twelve companies over 8 quarters and 5
years" is thousands of values and a test that generated them would share the
code it judges.

**(a) Three companies, two periods each, every ratio by hand.** Apple's fiscal
2025 and its June 2026 quarter, Cisco's April 2026 quarter and its fiscal 2025,
Carrier's 2024 and its March 2026 quarter. Every term is a number typed in here,
every ratio is written out term by term, and each number was read twice: once
out of the committed `companyfacts.json.gz` and once out of the filing that
reported it — `416,161` and `220,960` are printed in Apple's 10-K,
`15,841` and `6,480` in Cisco's 10-Q, `22,486` and `16,505` in Carrier's.
Nothing in this block came from running `src/trends.py`.

**(b) Everything else, against the row it names.** For every filled ratio of
every company, each term's tag, value, accession and filing date are looked up
in the committed record by `tests/companyfacts_source.py`, which opens the
gzip itself and imports nothing from `src/`. The claim is weaker than "the ratio
is right" — it is "the numerator and the denominator are the rows the table says
they are, they are inside the cutoff, and no later filing inside the cutoff
reports the period differently" — but it is one the code under test cannot
manufacture, and the ratio is then recomputed from those values with a second
copy of the eleven formulas written out below.

The other half is the absences. A fiscal fourth quarter is reported by nobody,
several ratios are in no filing at all, and the tests assert that each one is
named with a reason and that none was quietly filled with a zero.
"""

from __future__ import annotations

import datetime as dt
import functools
import json
import re

import pytest

from src import cutoff_guard, trends
from src.fetch_fixtures import TICKERS
from tests import companyfacts_source as source


@functools.lru_cache(maxsize=None)
def trigger(ticker: str) -> dict:
    """The manifest's row for the report this run is about: that company's 10-Q.

    A real trigger rather than the fixture set's own as-of date, so every test
    below is run against a cutoff that leaves rows out. Its `filing_date` is the
    cutoff and its `report_date` — EDGAR's period of report — is what the
    quarter window is anchored on. Both are the manifest's, not the table's.
    """
    return cutoff_guard.one_document(ticker, "10-Q", "primary_html")


def cutoff(ticker: str) -> str:
    return trigger(ticker)["filing_date"]


@functools.lru_cache(maxsize=None)
def table(ticker: str) -> dict:
    """The table as `src/assemble_bundle.py` builds it: cutoff and anchor both."""
    return trends.table(ticker, cutoff(ticker),
                        period_end=trigger(ticker)["report_date"])


def rows(payload: dict) -> list[dict]:
    return payload["quarters"] + payload["years"]


def period(ticker: str, label: str) -> dict:
    return {row["label"]: row for row in rows(table(ticker))}[label]


# The eleven formulas again, written out here rather than imported. `v` is the
# term values the table named, looked up in the record by `companyfacts_source`.
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


def test_the_table_reads_the_companyfacts_record_and_not_a_single_instance():
    """The point of the row. `read_record` goes through the gate's catalogue
    route, and the table says which record it read."""
    payload = table("AAPL")
    assert payload["source"]["record"] == "companyfacts"
    assert payload["source"]["cik"] == "0000320193"
    assert payload["cutoff"] == cutoff("AAPL")
    # Every filing a term came from is one the committed record names inside the
    # cutoff, and there are more of them than the route this replaces could ever
    # have reached: that one read a single 10-K and a single 10-Q, so two
    # accessions was its ceiling. Neither half of this is a number read off a
    # run of the table.
    read = payload["source"]["filings_read"]
    named = {row["accn"]
             for concept in source.record("AAPL")["facts"]["us-gaap"].values()
             for row in source.inside(concept.get("units", {}).get(source.UNIT, []),
                                      cutoff("AAPL"))}
    assert set(read) <= named
    assert len(read) > 2


# --- (a) the hand oracle -----------------------------------------------------
#
# Six periods, every term typed in from the record and cross-read in the filing,
# every ratio written out term by term. `hand` does the comparing so the six
# functions below are nothing but the arithmetic.

def hand(row: dict, *, dates: tuple, terms: dict, ratios: dict, missing: set) -> None:
    assert (row["start"], row["end"], row["days"]) == dates
    for name, cell in row["ratios"].items():
        if name in missing:
            assert "value" not in cell, f"{name} should not be computable here"
            assert cell["missing"]
            continue
        assert name in ratios, f"{name} is filled and has no hand value"
    for name, expected in ratios.items():
        cell = row["ratios"][name]
        assert "value" in cell, f"{name}: {cell.get('missing')}"
        assert cell["value"] == pytest.approx(expected, rel=0, abs=1e-12)
        for term, (tag, value, accession, filed) in terms.items():
            if term not in cell["inputs"]:
                continue
            got = cell["inputs"][term]
            assert (got["tag"], got["value"], got["accession"], got["filed"]) == \
                (tag, value, accession, filed), f"{name} {term}"
    named = {term for cell in row["ratios"].values()
             for term in (cell.get("inputs") or {})}
    assert named <= set(terms), f"a term with no hand value: {named - set(terms)}"


def test_apples_fiscal_2025_every_ratio_by_hand():
    """AAPL FY2025, 2024-09-29..2025-09-27, from the 10-K `0000320193-25-000079`
    and the balance sheet as the June 2026 10-Q restates the record of it."""
    revenue = 416_161_000_000.0
    cost_of_revenue = 220_960_000_000.0
    net_income = 112_010_000_000.0
    operating_cash_flow = 111_482_000_000.0
    receivables = 39_777_000_000.0
    inventory = 5_718_000_000.0
    assets = 359_241_000_000.0
    property_plant_and_equipment = 49_834_000_000.0
    cash = 35_934_000_000.0
    contract_liabilities = 9_055_000_000.0
    days = 364
    annual, quarterly = "0000320193-25-000079", "0000320193-26-000020"
    hand(
        period("AAPL", "FY-0"),
        dates=("2024-09-29", "2025-09-27", days),
        terms={
            "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                        revenue, annual, "2025-10-31"),
            "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                                cost_of_revenue, annual, "2025-10-31"),
            "net_income": ("NetIncomeLoss", net_income, annual, "2025-10-31"),
            "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                    operating_cash_flow, annual, "2025-10-31"),
            "receivables": ("AccountsReceivableNetCurrent",
                            receivables, quarterly, "2026-07-31"),
            "inventory": ("InventoryNet", inventory, quarterly, "2026-07-31"),
            "assets": ("Assets", assets, quarterly, "2026-07-31"),
            "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                             property_plant_and_equipment,
                                             quarterly, "2026-07-31"),
            "cash": ("CashAndCashEquivalentsAtCarryingValue",
                     cash, quarterly, "2026-07-31"),
            "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                     contract_liabilities, quarterly, "2026-07-31"),
        },
        ratios={
            "receivables_over_revenue": 39_777_000_000.0 / 416_161_000_000.0,
            "days_sales_outstanding": 39_777_000_000.0 / 416_161_000_000.0 * 364,
            "days_sales_of_inventory": 5_718_000_000.0 / 220_960_000_000.0 * 364,
            "accruals_over_total_assets":
                (112_010_000_000.0 - 111_482_000_000.0) / 359_241_000_000.0,
            "gross_margin":
                (416_161_000_000.0 - 220_960_000_000.0) / 416_161_000_000.0,
            "soft_asset_share":
                (359_241_000_000.0 - 49_834_000_000.0 - 35_934_000_000.0)
                / 359_241_000_000.0,
            "contract_liabilities_over_revenue":
                9_055_000_000.0 / 416_161_000_000.0,
        },
        missing={"bad_debt_reserve_ratio", "inventory_reserve_ratio",
                 "warranty_reserve_ratio", "non_gaap_gap"},
    )


def test_apples_june_2026_quarter_every_ratio_by_hand():
    """AAPL 2026-03-29..2026-06-27, from the 10-Q `0000320193-26-000020`.

    No accruals ratio: operating cash flow is stated year to date, so no
    quarter-length duration carries it, and the cell says so."""
    filing, filed = "0000320193-26-000020", "2026-07-31"
    hand(
        period("AAPL", "Q-0"),
        dates=("2026-03-29", "2026-06-27", 91),
        terms={
            "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                        109_417_000_000.0, filing, filed),
            "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                                54_647_000_000.0, filing, filed),
            "net_income": ("NetIncomeLoss", 29_789_000_000.0, filing, filed),
            "receivables": ("AccountsReceivableNetCurrent",
                            31_398_000_000.0, filing, filed),
            "inventory": ("InventoryNet", 11_092_000_000.0, filing, filed),
            "assets": ("Assets", 383_266_000_000.0, filing, filed),
            "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                             51_431_000_000.0, filing, filed),
            "cash": ("CashAndCashEquivalentsAtCarryingValue",
                     39_544_000_000.0, filing, filed),
            "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                     9_538_000_000.0, filing, filed),
        },
        ratios={
            "receivables_over_revenue": 31_398_000_000.0 / 109_417_000_000.0,
            "days_sales_outstanding": 31_398_000_000.0 / 109_417_000_000.0 * 91,
            "days_sales_of_inventory": 11_092_000_000.0 / 54_647_000_000.0 * 91,
            "gross_margin":
                (109_417_000_000.0 - 54_647_000_000.0) / 109_417_000_000.0,
            "soft_asset_share":
                (383_266_000_000.0 - 51_431_000_000.0 - 39_544_000_000.0)
                / 383_266_000_000.0,
            "contract_liabilities_over_revenue":
                9_538_000_000.0 / 109_417_000_000.0,
        },
        missing={"accruals_over_total_assets", "bad_debt_reserve_ratio",
                 "inventory_reserve_ratio", "warranty_reserve_ratio",
                 "non_gaap_gap"},
    )


def test_ciscos_april_2026_quarter_every_ratio_by_hand():
    """CSCO 2026-01-25..2026-04-25, from the 10-Q `0000858877-26-000078`.

    Receivables are `6,480`, the balance sheet's own figure — the note's
    sentence "Accounts receivable, net was $6.5 billion" is the same number
    rounded, and on the instance route it won a tie and published a DSO of
    37.3398 where the balance sheet gives 37.2249. companyfacts carries the
    balance-sheet cell and not the sentence.
    """
    filing, filed = "0000858877-26-000078", "2026-05-19"
    hand(
        period("CSCO", "Q-0"),
        dates=("2026-01-25", "2026-04-25", 91),
        terms={
            "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                        15_841_000_000.0, filing, filed),
            "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                                5_761_000_000.0, filing, filed),
            "net_income": ("NetIncomeLoss", 3_373_000_000.0, filing, filed),
            "receivables": ("AccountsReceivableNetCurrent",
                            6_480_000_000.0, filing, filed),
            "bad_debt_allowance": ("AllowanceForDoubtfulAccountsReceivableCurrent",
                                   73_000_000.0, filing, filed),
            "inventory": ("InventoryNet", 4_708_000_000.0, filing, filed),
            "warranty_accrual": ("ProductWarrantyAccrual",
                                 371_000_000.0, filing, filed),
            "assets": ("Assets", 125_546_000_000.0, filing, filed),
            "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                             2_577_000_000.0, filing, filed),
            "cash": ("CashAndCashEquivalentsAtCarryingValue",
                     7_083_000_000.0, filing, filed),
            "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                     16_446_000_000.0, filing, filed),
        },
        ratios={
            "receivables_over_revenue": 6_480_000_000.0 / 15_841_000_000.0,
            "days_sales_outstanding": 6_480_000_000.0 / 15_841_000_000.0 * 91,
            "days_sales_of_inventory": 4_708_000_000.0 / 5_761_000_000.0 * 91,
            "gross_margin":
                (15_841_000_000.0 - 5_761_000_000.0) / 15_841_000_000.0,
            "bad_debt_reserve_ratio":
                73_000_000.0 / (6_480_000_000.0 + 73_000_000.0),
            "warranty_reserve_ratio": 371_000_000.0 / 15_841_000_000.0,
            "soft_asset_share":
                (125_546_000_000.0 - 2_577_000_000.0 - 7_083_000_000.0)
                / 125_546_000_000.0,
            "contract_liabilities_over_revenue":
                16_446_000_000.0 / 15_841_000_000.0,
        },
        missing={"accruals_over_total_assets", "inventory_reserve_ratio",
                 "non_gaap_gap"},
    )


def test_ciscos_fiscal_2025_every_ratio_by_hand():
    """CSCO FY2025, 2024-07-28..2025-07-26, from the 10-K `0000858877-25-000111`
    with the balance sheet as the April 2026 10-Q holds it."""
    annual, quarterly = "0000858877-25-000111", "0000858877-26-000078"
    hand(
        period("CSCO", "FY-0"),
        dates=("2024-07-28", "2025-07-26", 364),
        terms={
            "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                        56_654_000_000.0, annual, "2025-09-03"),
            "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                                19_864_000_000.0, annual, "2025-09-03"),
            "net_income": ("NetIncomeLoss", 10_180_000_000.0, annual, "2025-09-03"),
            "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                    14_193_000_000.0, annual, "2025-09-03"),
            "receivables": ("AccountsReceivableNetCurrent",
                            6_701_000_000.0, quarterly, "2026-05-19"),
            "bad_debt_allowance": ("AllowanceForDoubtfulAccountsReceivableCurrent",
                                   69_000_000.0, quarterly, "2026-05-19"),
            "inventory": ("InventoryNet", 3_164_000_000.0, quarterly, "2026-05-19"),
            "warranty_accrual": ("ProductWarrantyAccrual",
                                 399_000_000.0, quarterly, "2026-05-19"),
            "assets": ("Assets", 122_291_000_000.0, quarterly, "2026-05-19"),
            "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                             2_113_000_000.0, quarterly, "2026-05-19"),
            "cash": ("CashAndCashEquivalentsAtCarryingValue",
                     8_346_000_000.0, quarterly, "2026-05-19"),
            "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                     16_416_000_000.0, quarterly, "2026-05-19"),
        },
        ratios={
            "receivables_over_revenue": 6_701_000_000.0 / 56_654_000_000.0,
            "days_sales_outstanding": 6_701_000_000.0 / 56_654_000_000.0 * 364,
            "days_sales_of_inventory": 3_164_000_000.0 / 19_864_000_000.0 * 364,
            "accruals_over_total_assets":
                (10_180_000_000.0 - 14_193_000_000.0) / 122_291_000_000.0,
            "gross_margin":
                (56_654_000_000.0 - 19_864_000_000.0) / 56_654_000_000.0,
            "bad_debt_reserve_ratio":
                69_000_000.0 / (6_701_000_000.0 + 69_000_000.0),
            "warranty_reserve_ratio": 399_000_000.0 / 56_654_000_000.0,
            "soft_asset_share":
                (122_291_000_000.0 - 2_113_000_000.0 - 8_346_000_000.0)
                / 122_291_000_000.0,
            "contract_liabilities_over_revenue":
                16_416_000_000.0 / 56_654_000_000.0,
        },
        missing={"inventory_reserve_ratio", "non_gaap_gap"},
    )


def test_carriers_2024_every_ratio_by_hand():
    """CARR 2024, a 366-day year, ten of the eleven ratios filled.

    Its cost of sales is the case where the two ends of one ratio come from two
    filings: `16,505` is reported by the 2024 10-K `0001783180-25-000008` and by
    nothing later, while revenue for the same year is restated verbatim by the
    2025 10-K, which is therefore the latest filing for it. The table names both.
    """
    twenty_four = "0001783180-25-000008"
    twenty_five = "0001783180-26-000008"
    quarterly = "0001783180-26-000026"
    hand(
        period("CARR", "FY-1"),
        dates=("2024-01-01", "2024-12-31", 366),
        terms={
            "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                        22_486_000_000.0, twenty_five, "2026-02-05"),
            "cost_of_revenue": ("CostOfGoodsAndServicesSold",
                                16_505_000_000.0, twenty_four, "2025-02-11"),
            "net_income": ("NetIncomeLoss", 5_604_000_000.0, twenty_five, "2026-02-05"),
            "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                    563_000_000.0, twenty_five, "2026-02-05"),
            "receivables": ("ReceivablesNetCurrent",
                            2_651_000_000.0, twenty_five, "2026-02-05"),
            "bad_debt_allowance": ("AllowanceForDoubtfulAccountsReceivable",
                                   97_000_000.0, twenty_five, "2026-02-05"),
            "inventory": ("InventoryNet", 2_299_000_000.0, twenty_five, "2026-02-05"),
            "inventory_reserve": ("InventoryValuationReserves",
                                  215_000_000.0, twenty_five, "2026-02-05"),
            "warranty_accrual": ("ProductWarrantyAccrual",
                                 786_000_000.0, quarterly, "2026-04-30"),
            "assets": ("Assets", 37_403_000_000.0, twenty_five, "2026-02-05"),
            "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                             2_999_000_000.0, twenty_five, "2026-02-05"),
            "cash": ("CashAndCashEquivalentsAtCarryingValue",
                     3_969_000_000.0, twenty_five, "2026-02-05"),
            "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                     553_000_000.0, twenty_five, "2026-02-05"),
        },
        ratios={
            "receivables_over_revenue": 2_651_000_000.0 / 22_486_000_000.0,
            "days_sales_outstanding": 2_651_000_000.0 / 22_486_000_000.0 * 366,
            "days_sales_of_inventory": 2_299_000_000.0 / 16_505_000_000.0 * 366,
            "accruals_over_total_assets":
                (5_604_000_000.0 - 563_000_000.0) / 37_403_000_000.0,
            "gross_margin":
                (22_486_000_000.0 - 16_505_000_000.0) / 22_486_000_000.0,
            "bad_debt_reserve_ratio":
                97_000_000.0 / (2_651_000_000.0 + 97_000_000.0),
            "inventory_reserve_ratio": 215_000_000.0 / 2_299_000_000.0,
            "warranty_reserve_ratio": 786_000_000.0 / 22_486_000_000.0,
            "soft_asset_share":
                (37_403_000_000.0 - 2_999_000_000.0 - 3_969_000_000.0)
                / 37_403_000_000.0,
            "contract_liabilities_over_revenue":
                553_000_000.0 / 22_486_000_000.0,
        },
        missing={"non_gaap_gap"},
    )


def test_carriers_march_2026_quarter_every_ratio_by_hand():
    """CARR 2026-01-01..2026-03-31, a 90-day quarter, from the 10-Q
    `0001783180-26-000026`. No cost of sales: Carrier tags it on the product and
    service axes and companyfacts holds the entity-wide fact alone, so the two
    ratios that need it are absent and say which of the ways.

    `Q-1`, not `Q-0`, and the label comes off the manifest rather than off the
    table: the run's trigger is the 10-Q whose period of report is 2026-06-30,
    which is `Q-0`, and this quarter is the one before it. Carrier's record was
    fetched on 2026-04-30 and holds no June quarter, so `Q-0` is empty and says
    why — anchored on the record instead, this quarter would wear the label of
    the one the run is actually about.
    """
    assert trigger("CARR")["report_date"] == "2026-06-30"
    filing, filed = "0001783180-26-000026", "2026-04-30"
    hand(
        period("CARR", "Q-1"),
        dates=("2026-01-01", "2026-03-31", 90),
        terms={
            "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                        5_341_000_000.0, filing, filed),
            "net_income": ("NetIncomeLoss", 238_000_000.0, filing, filed),
            "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",
                                    79_000_000.0, filing, filed),
            "receivables": ("ReceivablesNetCurrent",
                            3_130_000_000.0, filing, filed),
            "inventory": ("InventoryNet", 2_581_000_000.0, filing, filed),
            "inventory_reserve": ("InventoryValuationReserves",
                                  345_000_000.0, filing, filed),
            "warranty_accrual": ("ProductWarrantyAccrual",
                                 910_000_000.0, filing, filed),
            "assets": ("Assets", 37_186_000_000.0, filing, filed),
            "property_plant_and_equipment": ("PropertyPlantAndEquipmentNet",
                                             3_122_000_000.0, filing, filed),
            "cash": ("CashAndCashEquivalentsAtCarryingValue",
                     1_371_000_000.0, filing, filed),
            "contract_liabilities": ("ContractWithCustomerLiabilityCurrent",
                                     722_000_000.0, filing, filed),
        },
        ratios={
            "receivables_over_revenue": 3_130_000_000.0 / 5_341_000_000.0,
            "days_sales_outstanding": 3_130_000_000.0 / 5_341_000_000.0 * 90,
            "accruals_over_total_assets":
                (238_000_000.0 - 79_000_000.0) / 37_186_000_000.0,
            "inventory_reserve_ratio": 345_000_000.0 / 2_581_000_000.0,
            "warranty_reserve_ratio": 910_000_000.0 / 5_341_000_000.0,
            "soft_asset_share":
                (37_186_000_000.0 - 3_122_000_000.0 - 1_371_000_000.0)
                / 37_186_000_000.0,
            "contract_liabilities_over_revenue":
                722_000_000.0 / 5_341_000_000.0,
        },
        missing={"days_sales_of_inventory", "gross_margin",
                 "bad_debt_reserve_ratio", "non_gaap_gap"},
    )


def test_the_hand_checked_cutoffs_are_the_manifests_own_filing_dates():
    """The six blocks above name accessions and filing dates. Their cutoffs come
    from the fixture manifests, so a refetch that moved one is a failure here and
    not a silently different table."""
    assert cutoff("AAPL") == "2026-07-31"
    assert cutoff("CSCO") == "2026-05-19"
    assert cutoff("CARR") == "2026-07-28"


# --- (b) every term is the row the table says it is --------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_term_names_a_row_that_is_in_the_committed_record(ticker):
    """Tag, period, value, accession and filing date, looked up in the gzip by a
    reader that imports nothing from `src/`."""
    limit, checked = dt.date.fromisoformat(cutoff(ticker)), 0
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            for term, got in (cell.get("inputs") or {}).items():
                assert got["unit"] == source.UNIT
                matching = [candidate
                            for candidate in source.rows(ticker, got["tag"])
                            if source.spelled(candidate) == got["period"]
                            and candidate["accn"] == got["accession"]
                            and candidate["filed"] == got["filed"]
                            and float(candidate["val"]) == got["value"]]
                assert matching, f"{ticker} {row['label']} {name} {term}: {got}"
                assert dt.date.fromisoformat(got["filed"]) <= limit
                assert got["id"] == \
                    f"{got['accession']}:facts:{got['tag']}:{got['period']}"
                checked += 1
    assert checked, f"{ticker}: no term to look up"


@functools.lru_cache(maxsize=None)
def forms_by_accession(ticker: str) -> dict:
    """Every accession in the record and the form EDGAR files it under."""
    found: dict[str, set] = {}
    for concept in source.record(ticker)["facts"]["us-gaap"].values():
        for rows_here in concept.get("units", {}).values():
            for row in rows_here:
                found.setdefault(row["accn"], set()).add(str(row.get("form")))
    return found


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_term_comes_from_a_filing_the_input_spec_does_not_read(ticker):
    """`docs/INPUT_SPEC.md` §1 gives the numeric facts to "10-K, 10-Q, /A",
    lists DEF 14A under **Not fetched**, and gives an 8-K 8.01 or 9.01 "item
    codes only". companyfacts carries every filing's facts regardless, so the
    rule has to be applied when the record is read — and the form of each
    accession is looked up here in the gzip, not taken from the table."""
    forms = forms_by_accession(ticker)
    checked = 0
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            for term, got in (cell.get("inputs") or {}).items():
                named = forms.get(got["accession"], set())
                assert named, f"{ticker} {got['accession']} is in no row"
                for form in named:
                    assert form.startswith(("10-K", "10-Q")), \
                        f"{ticker} {row['label']} {name} {term}: {form}"
                checked += 1
    assert checked, f"{ticker}: no term to check"


def test_generacs_year_takes_the_ten_ks_net_income_and_not_the_proxy_statements():
    """The case the rule exists for, with both numbers typed in.

    Generac's 2025 net income is in the record twice: `159,554,000` from the
    10-K `0001437749-26-004568` filed 2026-02-18, and `161,400,000` from the
    proxy statement `0001104659-26-051499` filed 2026-04-29, whose
    pay-versus-performance table states it to the hundred thousand. The proxy is
    the later filing, so "the latest filing wins" hands it the year unless the
    form is read first — and the accruals ratio then divides a proxy's rounded
    earnings by a 10-K's cash flow and names the proxy as its source.
    """
    both = {row["accn"]: row["val"] for row
            in source.for_period(source.rows("GNRC", "NetIncomeLoss",
                                             every_form=True),
                                 "2025-01-01..2025-12-31")}
    assert both["0001437749-26-004568"] == 159_554_000
    assert both["0001104659-26-051499"] == 161_400_000
    assert "DEF 14A" in forms_by_accession("GNRC")["0001104659-26-051499"]

    cell = period("GNRC", "FY-0")["ratios"]["accruals_over_total_assets"]
    assert cell["inputs"]["net_income"]["value"] == 159_554_000.0
    assert cell["inputs"]["net_income"]["accession"] == "0001437749-26-004568"
    assert cell["inputs"]["net_income"]["filed"] == "2026-02-18"
    # And the ratio itself, by hand, from the three rows it names.
    cash = cell["inputs"]["operating_cash_flow"]["value"]
    assets = cell["inputs"]["assets"]["value"]
    assert (cash, assets) == (437_978_000.0, 5_573_679_000.0)
    assert cell["value"] == pytest.approx(
        (159_554_000.0 - 437_978_000.0) / 5_573_679_000.0, rel=0, abs=1e-12)


def test_carriers_recast_eight_k_is_not_the_filing_behind_a_number():
    """An 8-K 8.01 with a recast of the prior years' segments states the same
    concepts a 10-K does, and is often the latest filing to state an old period.
    §1 gives that form "item codes only", so it is not the source of a number
    here — the 10-K that reported the period is."""
    filings = forms_by_accession("CARR")
    assert "8-K" in filings["0001783180-25-000058"]
    named = {got["accession"]
             for row in rows(table("CARR"))
             for cell in row["ratios"].values()
             for got in (cell.get("inputs") or {}).values()}
    assert named
    assert "0001783180-25-000058" not in named


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_later_filing_inside_the_cutoff_reports_the_period_differently(ticker):
    """The rule: the latest filing at or before the cutoff wins. Restated here
    against the record, so a table that took the first-reported value, or the
    highest, or whichever row came first in the file, fails."""
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            for term, got in (cell.get("inputs") or {}).items():
                standing = source.reported(ticker, got["tag"], got["period"],
                                           cutoff(ticker))
                assert standing, f"{ticker} {row['label']} {name} {term}"
                assert {float(candidate["val"]) for candidate in standing} == \
                    {got["value"]}, f"{ticker} {row['label']} {name} {term}"
                assert {candidate["filed"] for candidate in standing} == \
                    {got["filed"]}


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_ratio_recomputes_from_the_values_the_record_holds(ticker):
    """The second copy of the eleven formulas, over the values looked up above."""
    checked = 0
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            if "value" not in cell:
                continue
            values = {term: source.one_value(ticker, got["tag"], got["period"],
                                             cutoff(ticker))
                      for term, got in cell["inputs"].items()}
            assert RECOMPUTE[name](values, row["days"]) == \
                pytest.approx(cell["value"], rel=0, abs=1e-9), \
                f"{ticker} {row['label']} {name}"
            checked += 1
    assert checked, f"{ticker}: nothing to recompute"


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_filled_ratio_names_a_row_for_every_term_of_its_formula(ticker):
    for row in rows(table(ticker)):
        for name, cell in row["ratios"].items():
            if "value" not in cell:
                continue
            assert cell["formula"] == trends.RATIOS[name]["formula"]
            for term in trends.RATIOS[name]["terms"]:
                assert term in cell["inputs"], f"{ticker} {row['label']} {name}"
            words = set(re.findall(r"[a-z_]+", cell["formula"])) - {"days_in_period", "abs"}
            assert words == set(cell["inputs"]), f"{ticker} {name}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_term_belongs_to_the_period_it_is_used_for(ticker):
    """No borrowing across periods: a duration term is the period itself, and a
    balance-sheet term is the instant at its end."""
    for row in rows(table(ticker)):
        for cell in row["ratios"].values():
            for term, got in (cell.get("inputs") or {}).items():
                if trends.CONCEPTS[term][0] == "duration":
                    assert got["period"] == f"{row['start']}..{row['end']}"
                else:
                    assert got["period"] == row["end"]


# --- the cutoff --------------------------------------------------------------

def earlier_trigger(ticker: str) -> str:
    """The earlier of a company's two triggers, so the cutoff really cuts.

    Read at the later of the two, ten of these twelve records hold nothing after
    it — the triggering report is the newest filing in them — and a cutoff that
    excludes nothing is a cutoff that tests nothing. The other two, Carrier and
    Littelfuse, were fetched before their 10-Q and are older than it either way.
    Seagate is the one company whose 10-K is the later of its two triggers,
    which is why this takes the earlier and not the annual one.
    """
    return min(cutoff_guard.one_document(ticker, form, "xbrl_instance")["filing_date"]
               for form in ("10-K", "10-Q"))


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_row_filed_after_the_cutoff_is_in_the_record_and_not_in_the_table(ticker):
    """Hundreds of rows sit past the earlier trigger of every one of these
    records — that is what a catalogue is — and none of them is behind a number
    in the table read at that trigger."""
    early = earlier_trigger(ticker)
    limit = dt.date.fromisoformat(early)
    ungated = source.record(ticker)["facts"]["us-gaap"]
    later = [row for concept in ungated.values()
             for unit_rows in concept.get("units", {}).values()
             for row in unit_rows
             if dt.date.fromisoformat(row["filed"]) > limit]
    assert later, f"{ticker}: the cutoff leaves nothing out, so it tests nothing"

    document = trends.read_record(ticker, early)
    assert trends.filed_after(document, limit) == []
    payload = trends.trends(document, early)
    for row in rows(payload):
        for name, cell in row["ratios"].items():
            for term, got in (cell.get("inputs") or {}).items():
                assert dt.date.fromisoformat(got["filed"]) <= limit, \
                    f"{ticker} {row['label']} {name} {term}"

    # And the run's own cutoff, which is the one every other test here uses.
    assert trends.filed_after(trends.read_record(ticker, cutoff(ticker)),
                              dt.date.fromisoformat(cutoff(ticker))) == []


def test_a_record_holding_a_late_row_is_refused_rather_than_trimmed():
    """The gate's catalogue route drops late rows. A record that arrived another
    way is refused here: a table one row past its cutoff is a look-ahead
    violation, not a smaller answer."""
    document = {"ticker": "PLANT", "facts": {"us-gaap": {"Assets": {"units": {"USD": [
        {"end": "2025-12-31", "val": 1.0, "accn": "later", "filed": "2026-03-01"},
    ]}}}}}
    with pytest.raises(trends.TrendInputError) as caught:
        trends.trends(document, "2026-02-28")
    assert "filed after the cutoff" in str(caught.value)
    assert trends.trends(document, "2026-03-01")["ticker"] == "PLANT"


@pytest.mark.parametrize("filed", [None, "", "last Tuesday"])
def test_a_row_with_no_readable_date_is_refused_and_not_treated_as_early(filed):
    """An absent date is not an early date, and it is not a late one either."""
    row = {"end": "2025-12-31", "val": 1.0, "accn": "a"}
    if filed is not None:
        row["filed"] = filed
    document = {"ticker": "PLANT",
                "facts": {"us-gaap": {"Assets": {"units": {"USD": [row]}}}}}
    with pytest.raises(trends.TrendInputError) as caught:
        trends.trends(document, "2026-03-01")
    assert "no date this can read" in str(caught.value)


def test_the_cutoff_is_parsed_before_anything_is_compared_to_it():
    """A string cutoff that sorts above every ISO date would admit the whole
    record at exit 0 — the look-ahead arriving in silence."""
    document = {"ticker": "PLANT", "facts": {}}
    with pytest.raises(trends.TrendInputError):
        trends.trends(document, "garbage")
    with pytest.raises(trends.TrendInputError):
        trends.trends(document, None)


def test_an_earlier_cutoff_yields_the_value_that_filing_reported():
    """Carrier's 2024 revenue is in three filings. Read at the 2025 10-K's own
    filing date, the row is that filing's; read at the 2026 cutoff it is the
    later one. Both are `22,486` — the record has no restatement here — so the
    claim the test makes is about which filing is named, not about the value."""
    early = trends.table("CARR", "2025-02-11")
    year = {row["label"]: row for row in early["years"]}["FY-0"]
    assert (year["start"], year["end"]) == ("2024-01-01", "2024-12-31")
    revenue = year["ratios"]["gross_margin"]["inputs"]["revenue"]
    assert revenue["accession"] == "0001783180-25-000008"
    assert revenue["filed"] == "2025-02-11"
    assert revenue["value"] == 22_486_000_000.0

    late = period("CARR", "FY-1")["ratios"]["gross_margin"]["inputs"]["revenue"]
    assert late["accession"] == "0001783180-26-000008"
    assert late["filed"] == "2026-02-05"
    assert late["value"] == revenue["value"]


# --- what is absent, and why -------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_a_ratio_that_cannot_be_computed_is_absent_not_zero(ticker):
    for row in rows(table(ticker)):
        for cell in row["ratios"].values():
            if "value" in cell:
                assert isinstance(cell["value"], float)
                continue
            assert isinstance(cell["missing"], str) and cell["missing"]
            assert "inputs" not in cell
            for change in ("year_over_year", "quarter_over_quarter"):
                assert cell[change]["reason"]
                assert "change" not in cell[change]


def test_no_ratio_is_ever_filled_for_the_non_gaap_gap():
    """An honest zero. companyfacts carries us-gaap and dei facts, and a
    non-GAAP measure is neither — so the gap needs the 8-K exhibit, and this
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


def test_a_fiscal_fourth_quarter_is_named_as_derived_and_not_as_an_absence():
    """Nobody reports it: the 10-K states the year and the three 10-Qs state the
    first three quarters. Apple's Q-3 and Q-7 are the fourth quarters of its two
    fiscal years, and the slot says where the number comes from instead."""
    quarters = {row["label"]: row for row in table("AAPL")["quarters"]}
    for label, target in (("Q-3", "2025-09-27"), ("Q-7", "2024-09-28")):
        assert not quarters[label]["filled"]
        assert quarters[label]["target_end"] == target
        assert "derived by src/fourth_quarter.py" in quarters[label]["reason"]
    # And the record really does hold no such duration, checked independently.
    for tag in ("RevenueFromContractWithCustomerExcludingAssessedTax",
                "NetIncomeLoss"):
        spans = {source.spelled(row) for row in source.rows("AAPL", tag)
                 if row.get("start")}
        assert "2025-06-29..2025-09-27" not in spans


def test_carriers_cost_of_sales_is_missing_because_the_record_holds_no_such_row():
    """Carrier tags cost of sales on the product and service axes, and
    companyfacts holds the entity-wide fact alone. The reason names both ways
    that can happen rather than asserting the one the record cannot see."""
    missing = period("CARR", "Q-1")["ratios"]["gross_margin"]["missing"]
    assert "cost_of_revenue" in missing
    assert "us-gaap:CostOfGoodsAndServicesSold" in missing
    assert "not for this period" in missing
    # Independently: the concept is in the record, and not for that quarter.
    spans = {source.spelled(row)
             for row in source.rows("CARR", "CostOfGoodsAndServicesSold")}
    assert spans and "2026-01-01..2026-03-31" not in spans


def test_a_row_from_a_form_this_table_does_not_read_is_not_a_row():
    """Planted, because no committed record has a period only a proxy reports.

    The two ways a row is not a statement: a form the spec does not read, and no
    form at all — a fact whose filing cannot be named is a fact whose source a
    reader cannot check. Both leave the term missing, and the reason says which
    filings did report it rather than claiming nobody tagged the concept.
    """
    def one(form: dict) -> dict:
        row = {"start": "2025-10-01", "end": "2025-12-31", "val": 7.0,
               "accn": "proxy", "filed": "2026-02-01"}
        return {"ticker": "PLANT", "facts": {"us-gaap": {
            "Revenues": {"units": {"USD": [dict(row, **form)]}}}}}

    for form, named in (({"form": "DEF 14A"}, "DEF 14A"),
                        ({}, "an unnamed form")):
        document = one(form)
        index = trends.observations(document)
        assert index == {}
        reason = trends.why_missing(document, index, "revenue",
                                    {"start": "2025-10-01", "end": "2025-12-31"})
        assert named in reason
        assert "periodic financial statements" in reason

    # And the same row under a 10-K is read, so the test is about the form.
    document = one({"form": "10-K"})
    assert trends.observations(document)["Revenues"]
    assert "periodic financial statements" not in trends.why_missing(
        document, trends.observations(document), "revenue",
        {"start": "2025-07-01", "end": "2025-09-30"})


def test_a_concept_the_record_carries_only_in_another_unit_says_so():
    """Every term of every ratio is an amount of money. A tag reported in shares
    is not a smaller amount of money."""
    document = {"ticker": "PLANT", "facts": {"us-gaap": {
        "InventoryNet": {"units": {"shares": [
            {"end": "2025-12-31", "val": 4.0, "accn": "a", "filed": "2025-01-01", "form": "10-K"}]}},
        "Assets": {"units": {"USD": [
            {"end": "2025-12-31", "val": 10.0, "accn": "a", "filed": "2025-01-01", "form": "10-K"}]}},
    }}}
    index = trends.observations(document)
    reason = trends.why_missing(document, index, "inventory",
                                {"start": "2025-10-01", "end": "2025-12-31"})
    assert "only in shares" in reason
    assert "USD" in reason


def test_two_values_for_one_period_in_one_filing_are_refused_not_chosen_between():
    """`docs/INPUT_SPEC.md` settles a repeated period by filing date. When that
    leaves two values there is nothing to choose between, and choosing anyway is
    how a wrong number gets published with a source note attached."""
    rows_here = [
        {"start": "2025-10-01", "end": "2025-12-31", "val": 100.0,
         "accn": "one", "filed": "2026-02-01"},
        {"start": "2025-10-01", "end": "2025-12-31", "val": 200.0,
         "accn": "one", "filed": "2026-02-01"},
    ]
    settled = trends.as_filed(rows_here, "us-gaap:Revenues for 2025-10-01..2025-12-31")
    assert "value" not in settled
    assert "[100.0, 200.0]" in settled["missing"]
    assert "two values for one period" in settled["missing"]


def test_a_zero_denominator_is_a_reason_not_an_infinity():
    document = {"ticker": "PLANT", "facts": {"us-gaap": {
        "Revenues": {"units": {"USD": [
            {"start": "2025-10-01", "end": "2025-12-31", "val": 0.0,
             "accn": "a", "filed": "2026-01-01", "form": "10-K"}]}},
        "AccountsReceivableNetCurrent": {"units": {"USD": [
            {"end": "2025-12-31", "val": 5.0, "accn": "a", "filed": "2026-01-01", "form": "10-K"}]}},
    }}}
    index = trends.observations(document)
    cell = trends.ratio(document, index, "receivables_over_revenue",
                        {"start": "2025-10-01", "end": "2025-12-31", "days": 92})
    assert "value" not in cell
    assert cell["missing"] == "revenue is zero in 2025-10-01..2025-12-31"


def test_a_duration_under_a_tag_no_term_names_is_not_a_fiscal_period():
    """TTM Technologies' record carries one `us-gaap:LossOnContracts` fact that
    starts its 2025 year a day early. Counting every annual-length span as a
    year takes a slot in the window from a real one."""
    document = {"ticker": "PLANT", "facts": {"us-gaap": {
        "LossOnContracts": {"units": {"USD": [
            {"start": "2024-12-30", "end": "2025-12-29", "val": 1.0,
             "accn": "a", "filed": "2026-01-01", "form": "10-K"}]}},
        "Revenues": {"units": {"USD": [
            {"start": "2024-12-31", "end": "2025-12-29", "val": 2.0,
             "accn": "a", "filed": "2026-01-01", "form": "10-K"}]}},
    }}}
    index = trends.observations(document)
    assert [(entry["start"], entry["end"]) for entry in trends.periods(index, "year")] \
        == [("2024-12-31", "2025-12-29")]


# --- coverage ----------------------------------------------------------------

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
def test_every_requested_period_is_either_filled_or_given_a_reason(ticker):
    """The count is not asserted to be large. It is asserted to be accounted
    for: thirteen slots, each one filled or explained, and the two numbers that
    say how many carry a ratio against how many are on record at all."""
    payload = table(ticker)
    listed = payload["coverage"]["quarters"] + payload["coverage"]["years"]
    assert len(listed) == 13
    filled = [entry for entry in listed if entry["status"] == "filled"]
    assert len(filled) == sum(1 for row in rows(payload) if row["filled"])
    assert payload["coverage"]["periods_on_record"] == len(filled)
    assert payload["coverage"]["periods_with_at_least_one_ratio"] == sum(
        1 for row in rows(payload)
        if row["filled"] and any("value" in cell for cell in row["ratios"].values()))
    assert payload["coverage"]["periods_with_at_least_one_ratio"] <= \
        payload["coverage"]["periods_on_record"]


@functools.lru_cache(maxsize=None)
def fiscal_year_ends(ticker: str, at: str | None = None) -> tuple[str, ...]:
    """Every fiscal-year end in the record, by EDGAR's own labelling of it.

    `form` and `fp` are companyfacts' keys and not this table's rules: a
    duration a 10-K reported for the period `FY` ends on the fiscal year end.
    Read through `companyfacts_source`, which imports nothing from `src/`, and
    filtered to a cutoff — the run's own by default — like everything else here.
    """
    ends = set()
    for concept in source.record(ticker)["facts"]["us-gaap"].values():
        rows_here = concept.get("units", {}).get(source.UNIT, [])
        for row in source.inside(rows_here, at or cutoff(ticker)):
            if (row.get("start") and row.get("fp") == "FY"
                    and str(row.get("form", "")).startswith("10-K")):
                ends.add(row["end"])
    return tuple(sorted(ends))


@functools.lru_cache(maxsize=None)
def record_newest_filing(ticker: str) -> str:
    """The newest statement filing in the committed record, by the second reader.

    The same two rules the table reads the record under, restated from
    `docs/INPUT_SPEC.md` rather than imported: a periodic financial statement,
    filed at or before the run's cutoff.
    """
    return max(row["filed"]
               for concept in source.record(ticker)["facts"]["us-gaap"].values()
               for rows_here in concept.get("units", {}).values()
               for row in source.inside(rows_here, cutoff(ticker))
               if source.a_statement(row))


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_window_is_anchored_on_the_triggering_reports_own_period(ticker):
    """`Q-0` is the quarter this run is about, filled or not.

    Anchored on the newest quarter in the record instead, a record fetched
    before its trigger renames every quarter one step back: Carrier's record was
    fetched 2026-04-30 against a 10-Q filed 2026-07-28, so the March quarter
    wore `Q-0`, the June quarter the run is about appeared in no slot, and the
    table reported twelve of thirteen periods on record. The anchor is the
    manifest's `report_date` for the trigger — EDGAR's period of report — and
    not a date this table chose.
    """
    payload = table(ticker)
    end = trigger(ticker)["report_date"]
    assert payload["window"]["triggering_period_end"] == end
    assert payload["window"]["quarters_end"] == end
    assert payload["quarters"][0]["label"] == "Q-0"
    assert payload["coverage"]["quarters"][0]["target_end"] == end
    if payload["quarters"][0]["filled"]:
        assert payload["quarters"][0]["end"] == end


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_record_older_than_its_trigger_says_so_where_the_period_is_missing(ticker):
    """Two of the twelve records were fetched before the 10-Q that triggers the
    run, so the run's own quarter is in no row of them. That is stated — in the
    window block and in the empty slot itself — rather than left as a table that
    silently starts one quarter early. Which two is read off the committed
    record by `companyfacts_source`, not off the table."""
    payload = table(ticker)
    stale = record_newest_filing(ticker) < cutoff(ticker)
    said = payload["window"]["record_predates_the_trigger"]
    assert bool(said) == stale, ticker
    if not stale:
        assert payload["quarters"][0]["filled"], ticker
        return
    assert record_newest_filing(ticker) in said
    assert cutoff(ticker) in said
    assert not payload["quarters"][0]["filled"]
    assert said in payload["quarters"][0]["reason"]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_year_window_ends_at_the_fiscal_year_the_run_is_about(ticker, form):
    """`FY-0` is the newest fiscal year at or before the run's own period.

    On an annual trigger that is the trigger's own period; on a quarterly one it
    is the last fiscal year that ended before it. Both sides of the comparison
    come from the manifest and from EDGAR's own `FY` labelling inside the
    record, read by `companyfacts_source` — never from the table. The quarter
    window had this and the year window did not, which left a record fetched the
    day before a 10-K reporting the prior year as `FY-0`.
    """
    report = cutoff_guard.one_document(ticker, form, "primary_html")
    payload = trends.table(ticker, report["filing_date"],
                           period_end=report["report_date"])
    ends = [end for end in fiscal_year_ends(ticker, report["filing_date"])
            if end <= report["report_date"]]
    assert ends, f"{ticker} {form}: the record labels no fiscal year at the cutoff"
    year = payload["years"][0]
    if form == "10-K":
        # The trigger is the fiscal year. Its own period, to the day.
        assert year["target_end"] == report["report_date"]
        assert max(ends) == report["report_date"]
    else:
        assert year["target_end"] == max(ends)
    assert year["label"] == "FY-0"
    assert payload["window"]["years_end"] == year["target_end"]
    if year["filled"]:
        assert year["end"] == max(ends)


def test_a_record_older_than_an_annual_trigger_leaves_the_year_empty(tmp_path):
    """The path a stale record opens on the annual route, which no committed
    bundle takes: Carrier's 10-K was filed 2026-02-05 for the year ended
    2025-12-31, and a record fetched the day before holds 2024 as its newest
    year. Reading that as `FY-0` hands a reader the wrong year under the right
    label — every ratio in the slot correct, and about a year earlier than the
    run. The expected values are the manifest's dates and the record filtered by
    hand at the planted fetch date."""
    report = cutoff_guard.one_document("CARR", "10-K", "primary_html")
    assert (report["filing_date"], report["report_date"]) == ("2026-02-05", "2025-12-31")
    before = "2026-02-04"

    # Independently: at that fetch date the record's newest fiscal year is 2024.
    ends = fiscal_year_ends("CARR", before)
    assert max(ends) == "2024-12-31"

    payload = trends.trends(trends.read_record("CARR", before),
                            report["filing_date"], period_end=report["report_date"])
    year = payload["years"][0]
    assert year["label"] == "FY-0"
    assert year["target_end"] == "2025-12-31"
    assert not year["filled"]
    assert "fetched before the triggering report" in year["reason"]
    assert payload["years"][1]["end"] == "2024-12-31"


def test_the_two_records_older_than_their_trigger_are_the_ones_the_fixtures_hold():
    """Named, so a refetch that makes them current is a failure here and not a
    quietly different table. Both sides come from the committed manifests."""
    stale = {ticker for ticker in TICKERS
             if record_newest_filing(ticker) < cutoff(ticker)}
    assert stale == {"CARR", "LFUS"}


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_only_window_the_record_cannot_fill_is_the_fourth_quarters(ticker):
    """Why the row exists, and the exact size of what is still missing.

    One 10-K and one 10-Q carry three fiscal years and two quarters between
    them, so seven of the thirteen slots were reported missing for no reason but
    the input. The record fills all five years, and every quarter it does not
    fill is one of exactly two things, each asserted rather than assumed:

    * a fiscal fourth quarter, which nobody reports as a duration — its target
      end lands on a fiscal year end that EDGAR itself labels `FY` in a 10-K,
      within a week, because a 52/53-week year end moves by up to seven days
      against the 364-day step the window walks back on; or
    * a period the record does not reach, because the record was fetched before
      the filing that first states it — true of two of these twelve, and the
      slot says so.

    So the count is a consequence and not a floor chosen after the fact.
    """
    payload = table(ticker)
    assert len(payload["coverage"]["years"]) == 5
    assert all(entry["status"] == "filled" for entry in payload["coverage"]["years"])

    ends = [dt.date.fromisoformat(end) for end in fiscal_year_ends(ticker)]
    assert ends, f"{ticker}: the record labels no fiscal year at all"
    newest = dt.date.fromisoformat(record_newest_filing(ticker))
    empty = [entry for entry in payload["coverage"]["quarters"]
             if entry["status"] != "filled"]
    for entry in empty:
        target = dt.date.fromisoformat(entry["target_end"])
        if "derived by src/fourth_quarter.py" in entry["reason"]:
            assert min(abs((end - target).days) for end in ends) <= 7, \
                f"{ticker} {entry['label']} {entry['target_end']} is not a year end"
            continue
        assert newest < dt.date.fromisoformat(cutoff(ticker)), \
            f"{ticker} {entry['label']}: empty for neither of the two reasons"
        assert "fetched before the triggering report" in entry["reason"]
    assert len(empty) <= 3
    assert payload["coverage"]["periods_with_at_least_one_ratio"] == 13 - len(empty)


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
            assert trends.QUARTER_DAYS[0] <= row["days"] <= trends.QUARTER_DAYS[1]
            assert row["days"] == trends._days(row["start"], row["end"])
    for row in payload["years"]:
        if row["filled"]:
            assert trends.YEAR_DAYS[0] <= row["days"] <= trends.YEAR_DAYS[1]
            assert row["days"] == trends._days(row["start"], row["end"])


# --- the changes -------------------------------------------------------------

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
                assert (cell["value"] - other["ratios"][name]["value"]) == \
                    pytest.approx(change["change"], rel=0, abs=1e-9)


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_emitted_change_subtracts_two_different_concepts(ticker):
    """`CONCEPTS` gives a term several acceptable tags and the first the record
    carries is taken, so two periods of one ratio can rest on different us-gaap
    concepts. Subtracting those is not a change."""
    payload = table(ticker)
    by_label = {row["label"]: row for row in rows(payload)}
    checked = 0
    for row in rows(payload):
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
        for row in rows(table(ticker)):
            for cell in row["ratios"].values():
                for key in ("year_over_year", "quarter_over_quarter"):
                    entry = cell.get(key) or {}
                    if "different concept in each period" in (entry.get("reason") or ""):
                        refusals.append(entry["reason"])
    assert refusals, "no ratio in the twelve records changes concept between periods"
    for reason in refusals:
        assert reason.count("us-gaap:") >= 2


def test_an_annual_period_has_no_quarter_over_quarter_change():
    for row in table("AAPL")["years"]:
        for cell in row["ratios"].values():
            assert cell["quarter_over_quarter"]["reason"] == \
                "an annual period has no preceding quarter"


# --- determinism and the command ---------------------------------------------

def test_two_runs_are_byte_identical(tmp_path):
    first, second = tmp_path / "a.json", tmp_path / "b.json"
    assert trends.main(["--ticker", "LFUS", "--cutoff", cutoff("LFUS"),
                        "--out", str(first)]) == 0
    assert trends.main(["--ticker", "LFUS", "--cutoff", cutoff("LFUS"),
                        "--out", str(second)]) == 0
    assert first.read_bytes() == second.read_bytes()


def test_the_output_does_not_depend_on_the_order_of_the_rows_in_the_record():
    """Reversing every unit's rows must not change one digit — dict ordering and
    "whichever came first" are the two ways this file could stop being
    reproducible."""
    document = trends.read_record("TTMI", cutoff("TTMI"))
    reversed_rows = {
        namespace: {tag: dict(concept, units={unit: list(reversed(rows_here))
                                              for unit, rows_here in concept["units"].items()})
                    for tag, concept in concepts.items()}
        for namespace, concepts in document["facts"].items()}
    assert trends.render(trends.trends(dict(document, facts=reversed_rows),
                                       cutoff("TTMI"))) == \
        trends.render(trends.trends(document, cutoff("TTMI")))


def test_the_command_reports_both_period_counts(tmp_path, capsys):
    assert trends.main(["--ticker", "CSCO", "--cutoff", cutoff("CSCO"),
                        "--out", str(tmp_path / "out.json")]) == 0
    printed = capsys.readouterr().out
    written = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    coverage = written["coverage"]
    assert f"{coverage['periods_with_at_least_one_ratio']} of 13 periods carry a ratio" \
        in printed
    assert f"{coverage['periods_on_record']} of 13 are on record" in printed


def test_the_command_defaults_to_the_fixture_sets_own_as_of_date(tmp_path):
    assert trends.main(["--ticker", "ESE", "--out", str(tmp_path / "out.json")]) == 0
    written = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert written["cutoff"] == str(cutoff_guard.default_cutoff("ESE"))


def test_an_empty_cutoff_is_refused_rather_than_defaulted(tmp_path, capsys):
    """A cutoff given as an empty string is a cutoff that is wrong, not one that
    is absent. `args.cutoff or default_cutoff(...)` reads the two as the same
    thing and answers with the fixture set's own as-of date, which is months
    after every trigger here — look-ahead arriving at exit 0."""
    out = tmp_path / "out.json"
    assert trends.main(["--ticker", "ESE", "--cutoff", "", "--out", str(out)]) == 2
    assert not out.exists()
    assert "cutoff" in capsys.readouterr().err
    # And the absent case still takes the default, which is the other half.
    assert trends.main(["--ticker", "ESE", "--out", str(out)]) == 0


def test_the_command_refuses_a_company_with_no_record(tmp_path, capsys):
    assert trends.main(["--ticker", "NOSUCH", "--cutoff", "2026-01-01",
                        "--out", str(tmp_path / "out.json")]) == 2
    assert "NOSUCH" in capsys.readouterr().err


def test_a_record_with_no_facts_object_is_refused():
    with pytest.raises(trends.TrendInputError):
        trends.trends({"ticker": "PLANT"}, "2026-01-01")
    with pytest.raises(trends.TrendInputError):
        trends.trends({"facts": {}}, "2026-01-01")


def test_an_empty_record_still_lists_all_thirteen_periods():
    payload = trends.trends({"ticker": "NONE", "facts": {}}, "2026-01-01")
    assert len(payload["coverage"]["quarters"]) == 8
    assert len(payload["coverage"]["years"]) == 5
    assert all(entry["status"] == "missing"
               for entry in payload["coverage"]["quarters"] + payload["coverage"]["years"])
    assert all(block["filled"] == 0 for block in payload["coverage"]["ratios"])
