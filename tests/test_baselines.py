"""The formula baselines, each published formula applied by hand to one frozen fixture.

Qualcomm, the run its 10-Q of 2026-07-29 triggers. The current fiscal year is
fiscal 2025, which ended 2025-09-28; the prior year is fiscal 2024; and the
balance sheet of 2023-09-24 is the one fiscal 2024 opened on. Nothing in this
file came from running `src/baselines.py`.

Where each number was read:

- Every fiscal 2025 and fiscal 2024 amount is printed in Qualcomm's own 10-K,
  which is committed, and `test_every_term_is_printed_in_the_ten_k` finds each
  one there with `tests/independent_text.py`, which imports nothing from `src/`.
  They are typed below in millions, as the 10-K prints them.
- The same amounts are then found in the committed companyfacts record, by the
  accession and filing date of the row the cutoff rule leaves standing, through
  `tests/companyfacts_source.py`, which opens the gzip itself. Where a later
  10-Q restated a balance-sheet column without changing it, that 10-Q is the
  latest filing at or before the cutoff and its row is the one typed.
- Total assets at 2023-09-24 are not printed in the fiscal 2025 10-K; they are
  read from the record, by the accession of the fiscal 2024 10-K that reported
  them, the way `tests/test_trends_rnd.py` reads its older years.
- The GNP price-level index is typed from the ALFRED vintage committed under
  `src/price_level_index/`, and each quarter typed is asserted to be a line of
  that file.

**The papers, so the coefficients can be checked against them and not against
this code.**

- Beneish, M. D. (1999). The Detection of Earnings Manipulation. *Financial
  Analysts Journal* 55(5): 24-36. The eight-variable unweighted probit:
  M = -4.84 + .920 DSRI + .528 GMI + .404 AQI + .892 SGI + .115 DEPI
  - .172 SGAI + 4.679 TATA - .327 LVGI, with total accruals the change in
  working capital other than cash, less depreciation:
  ((change in current assets - change in cash) - (change in current liabilities
  - change in current maturities of long-term debt - change in income tax
  payable) - depreciation and amortization) / total assets.
- Sloan, R. G. (1996). Do Stock Prices Fully Reflect Information in Accruals and
  Cash Flows about Future Earnings? *The Accounting Review* 71(3): 289-315. The
  same balance-sheet accruals with the change in debt included in current
  liabilities, scaled by average total assets.
- Hirshleifer, D., Hou, K., Teoh, S. H. and Zhang, Y. (2004). Do investors
  overvalue firms with bloated balance sheets? *Journal of Accounting and
  Economics* 38: 297-331. Net operating assets = (operating assets - operating
  liabilities) / lagged total assets; operating assets = total assets - cash and
  short-term investment; operating liabilities = total assets - short-term debt
  - long-term debt - minority interest - preferred stock - common equity.
- Piotroski, J. D. (2000). Value Investing: The Use of Historical Financial
  Statement Information to Separate Winners from Losers. *Journal of Accounting
  Research* 38 (Supplement): 1-41. Nine binary signals: return on assets and
  operating cash flow over beginning-of-year assets positive, return on assets
  rose, cash flow above return on assets, long-term debt over average assets
  fell, current ratio rose, no common equity issued, gross margin rose, sales
  over beginning-of-year assets rose.
- Ohlson, J. A. (1980). Financial Ratios and the Probabilistic Prediction of
  Bankruptcy. *Journal of Accounting Research* 18(1): 109-131. Model 1:
  O = -1.32 - .407 SIZE + 6.03 TLTA - 1.43 WCTA + .0757 CLCA - 1.72 OENEG
  - 2.37 NITA - 1.83 FUTL + .285 INTWO - .521 CHIN, where SIZE is the log of
  total assets over the GNP price-level index with 1968 at 100, total assets as
  reported in dollars, and the index year the year before the balance sheet's.
- Altman, E. I. (1968). Financial Ratios, Discriminant Analysis and the
  Prediction of Corporate Bankruptcy. *Journal of Finance* 23(4): 589-609.
  Z = .012X1 + .014X2 + .033X3 + .006X4 + .999X5, the first four ratios written
  as percentages.
- Cohen, L., Malloy, C. and Nguyen, Q. (2020). Lazy Prices. *Journal of Finance*
  75(3): 1371-1415. Cosine similarity of term-frequency vectors.

**The note cosine similarity** is the one row that cannot be typed out whole:
the two filings' notes run to about six thousand words each. So it is judged
twice. Once by hand, on a note short enough to count — the inventory table,
whose words are typed below and whose text is found printed in both 10-Qs — and
once on the whole, by a recount written in this file that imports nothing from
`src/baselines.py`.
"""

from __future__ import annotations

import collections
import copy
import functools
import gzip
import hashlib
import json
import math
import re
import shutil
from pathlib import Path

import pytest

from src import baselines, cutoff_guard, extract_notes, trends
from tests import companyfacts_source as source
from tests import independent_text

REPO_ROOT = Path(__file__).resolve().parent.parent
TICKER = "QCOM"
MILLION = 1_000_000.0

TRIGGER = "0000804328-26-000086"       # the 10-Q, filed 2026-07-29
PRIOR_QUARTER = "0000804328-26-000061"  # the 10-Q before it, filed 2026-04-29
TEN_K = "0000804328-25-000085"          # fiscal 2025, filed 2025-11-05
OLDER_TEN_K = "0000804328-24-000075"    # fiscal 2024, filed 2024-11-06
CUTOFF = "2026-07-29"

Y2025, Y2024, Y2023 = "2025-09-28", "2024-09-29", "2023-09-24"
FY2025, FY2024 = "2024-09-30..2025-09-28", "2023-09-25..2024-09-29"
CURRENT, PRIOR, TWO_BACK = "current_year", "prior_year", "two_years_back"

# (term, year) → (us-gaap tag, period, millions as printed, accession, filed)
TERMS = {
    ("cash", CURRENT): ("CashAndCashEquivalentsAtCarryingValue", Y2025, 5_520, TRIGGER, CUTOFF),
    ("cash", PRIOR): ("CashAndCashEquivalentsAtCarryingValue", Y2024, 7_849, TEN_K, "2025-11-05"),
    ("short_term_investments", CURRENT): ("MarketableSecuritiesCurrent", Y2025, 4_635, TRIGGER, CUTOFF),
    ("receivables", CURRENT): ("AccountsAndOtherReceivablesNetCurrent", Y2025, 4_315, TRIGGER, CUTOFF),
    ("receivables", PRIOR): ("AccountsAndOtherReceivablesNetCurrent", Y2024, 3_929, TEN_K, "2025-11-05"),
    ("current_assets", CURRENT): ("AssetsCurrent", Y2025, 25_754, TRIGGER, CUTOFF),
    ("current_assets", PRIOR): ("AssetsCurrent", Y2024, 25_231, TEN_K, "2025-11-05"),
    ("property_plant_and_equipment", CURRENT): ("PropertyPlantAndEquipmentNet", Y2025, 4_690, TRIGGER, CUTOFF),
    ("property_plant_and_equipment", PRIOR): ("PropertyPlantAndEquipmentNet", Y2024, 4_665, TEN_K, "2025-11-05"),
    ("assets", CURRENT): ("Assets", Y2025, 50_143, TRIGGER, CUTOFF),
    ("assets", PRIOR): ("Assets", Y2024, 55_154, TEN_K, "2025-11-05"),
    ("assets", TWO_BACK): ("Assets", Y2023, 51_040, OLDER_TEN_K, "2024-11-06"),
    ("debt_in_current_liabilities", CURRENT): ("DebtCurrent", Y2025, 0, TRIGGER, CUTOFF),
    ("debt_in_current_liabilities", PRIOR): ("DebtCurrent", Y2024, 1_364, TEN_K, "2025-11-05"),
    ("current_maturities_of_long_term_debt", CURRENT): ("LongTermDebtCurrent", Y2025, 0, TRIGGER, CUTOFF),
    ("current_maturities_of_long_term_debt", PRIOR): ("LongTermDebtCurrent", Y2024, 1_364, TEN_K, "2025-11-05"),
    ("current_liabilities", CURRENT): ("LiabilitiesCurrent", Y2025, 9_144, TRIGGER, CUTOFF),
    ("current_liabilities", PRIOR): ("LiabilitiesCurrent", Y2024, 10_504, TEN_K, "2025-11-05"),
    ("long_term_debt", CURRENT): ("LongTermDebtNoncurrent", Y2025, 14_811, TEN_K, "2025-11-05"),
    ("long_term_debt", PRIOR): ("LongTermDebtNoncurrent", Y2024, 13_270, TEN_K, "2025-11-05"),
    ("total_liabilities", CURRENT): ("Liabilities", Y2025, 28_937, TRIGGER, CUTOFF),
    ("retained_earnings", CURRENT): ("RetainedEarningsAccumulatedDeficit", Y2025, 20_646, TRIGGER, CUTOFF),
    ("total_equity", CURRENT): ("StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
                                Y2025, 21_206, TRIGGER, CUTOFF),
    ("income_taxes_payable", CURRENT): ("AccruedIncomeTaxesCurrent", Y2025, 1_007, TRIGGER, CUTOFF),
    ("income_taxes_payable", PRIOR): ("AccruedIncomeTaxesCurrent", Y2024, 1_080, TEN_K, "2025-11-05"),
    ("revenue", CURRENT): ("Revenues", FY2025, 44_284, TEN_K, "2025-11-05"),
    ("revenue", PRIOR): ("Revenues", FY2024, 38_962, TEN_K, "2025-11-05"),
    ("cost_of_revenue", CURRENT): ("CostOfRevenue", FY2025, 19_738, TEN_K, "2025-11-05"),
    ("cost_of_revenue", PRIOR): ("CostOfRevenue", FY2024, 17_060, TEN_K, "2025-11-05"),
    ("selling_general_and_administrative", CURRENT):
        ("SellingGeneralAndAdministrativeExpense", FY2025, 3_110, TEN_K, "2025-11-05"),
    ("selling_general_and_administrative", PRIOR):
        ("SellingGeneralAndAdministrativeExpense", FY2024, 2_759, TEN_K, "2025-11-05"),
    ("interest_expense", CURRENT): ("InterestExpense", FY2025, 664, TEN_K, "2025-11-05"),
    ("pretax_income", CURRENT):
        ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
         FY2025, 12_663, TEN_K, "2025-11-05"),
    ("net_income", CURRENT): ("NetIncomeLoss", FY2025, 5_541, TEN_K, "2025-11-05"),
    ("net_income", PRIOR): ("NetIncomeLoss", FY2024, 10_142, TEN_K, "2025-11-05"),
    ("depreciation_and_amortization", CURRENT):
        ("DepreciationDepletionAndAmortization", FY2025, 1_602, TEN_K, "2025-11-05"),
    ("depreciation_and_amortization", PRIOR):
        ("DepreciationDepletionAndAmortization", FY2024, 1_706, TEN_K, "2025-11-05"),
    ("operating_cash_flow", CURRENT):
        ("NetCashProvidedByUsedInOperatingActivities", FY2025, 14_012, TEN_K, "2025-11-05"),
    ("common_stock_issued", CURRENT): ("ProceedsFromIssuanceOfCommonStock", FY2025, 404, TEN_K, "2025-11-05"),
}

# The lines of the 10-K each fiscal 2025 and fiscal 2024 number above is on.
PRINTED = [
    "Cash and cash equivalents$5,520 $7,849",
    "Marketable securities4,635 5,451",
    "Accounts receivable, net4,315 3,929",
    "Total current assets25,754 25,231",
    "Property, plant and equipment, net4,690 4,665",
    "Total assets$50,143 $55,154",
    "Short-term debt— 1,364",
    "Total current liabilities9,144 10,504",
    "Long-term debt14,811 13,270",
    "Total liabilities28,937 28,880",
    "Retained earnings20,646 25,687",
    "Total stockholders’ equity21,206 26,274",
    "Income taxes payable1,007 1,080",
    "Total revenues44,284 38,962 35,820",
    "Cost of revenues19,738 17,060 15,869",
    "Selling, general and administrative3,110 2,759 2,483",
    "Interest expense(664)(697)(694)",
    "Income from continuing operations before income taxes12,663 10,336 7,443",
    "Net income$5,541 $10,142 $7,232",
    "Depreciation and amortization expense1,602 1,706 1,809",
    "Net cash provided by operating activities14,012 12,202 11,299",
    "Proceeds from issuance of common stock404 383 434",
]

# The GNP implicit price deflator, index 2017 = 100, as the committed ALFRED
# vintage of 2026-04-29 carries it: the four quarters of 2024, the year before
# the fiscal 2025 balance sheet's, and the four of 1968, the base year.
INDEX_2024 = (124.284, 125.077, 125.605, 126.359)
INDEX_1968 = (17.948, 18.137, 18.315, 18.573)
# The same quarters of 2024 in the vintage of 2025-08-29, before the annual
# revision of September 2025 moved them.
INDEX_2024_EARLIER = (124.074, 124.853, 125.441, 126.166)

# Planted on purpose, and not Qualcomm's market value: no price is committed
# for these companies, so Altman's market-value ratio is judged on a number
# this file chose.
PLANTED_MARKET_VALUE = 150_000 * MILLION


def m(term: str, year: str) -> float:
    """A typed number, in millions."""
    return float(TERMS[(term, year)][2])


@functools.lru_cache(maxsize=None)
def payload(form: str = "10-Q") -> dict:
    return baselines.baselines(TICKER, form)


@functools.lru_cache(maxsize=None)
def printed_text(form: str, role: str = "primary_html") -> str:
    entry = cutoff_guard.one_document(TICKER, form, role)
    raw = entry["full_path"].read_bytes()
    if entry["full_path"].suffix == ".gz":
        raw = gzip.decompress(raw)
    text = independent_text.strip(raw.decode("utf-8")).replace("​", "")
    return independent_text.squeeze(text)


def mean(values) -> float:
    return sum(values) / len(values)


# --- the typed numbers are the source's ---------------------------------------

def test_every_term_is_printed_in_the_ten_k():
    text = printed_text("10-K")
    for line in PRINTED:
        assert independent_text.squeeze(line) in text, f"the 10-K does not print {line!r}"


def test_every_term_is_the_records_own_row():
    for (term, year), (tag, period, millions, accession, filed) in TERMS.items():
        standing = source.reported(TICKER, tag, period, CUTOFF)
        assert {(row["val"], row["accn"], row["filed"]) for row in standing} == \
            {(millions * MILLION, accession, filed)}, f"{term} {year}: {standing}"


def test_every_term_the_baselines_read_is_the_typed_row():
    """Each row's inputs name the tag, the value and the filing typed above."""
    seen = 0
    for row in ("beneish_m_score", "accruals_over_assets", "net_operating_assets",
                "piotroski_f_score", "ohlson_o_score", "altman_z_score"):
        for term, by_year in payload()[row]["inputs"].items():
            for year, cell in by_year.items():
                tag, period, millions, accession, filed = TERMS[(term, year)]
                assert (cell["tag"], cell["period"], cell["value"], cell["accession"],
                        cell["filed"]) == (tag, period, millions * MILLION, accession,
                                           filed), f"{row} {term} {year}: {cell}"
                seen += 1
    assert seen > len(TERMS)


def test_the_fiscal_years_are_the_ten_ks_own():
    assert payload()["fiscal_years"] == {
        CURRENT: {"start": "2024-09-30", "end": Y2025},
        PRIOR: {"start": "2023-09-25", "end": Y2024},
        TWO_BACK: {"start": "2022-09-26", "end": Y2023},
    }
    assert payload()["cutoff"] == CUTOFF
    assert payload()["trigger"]["accession"] == TRIGGER


def test_receivables_are_the_balance_sheet_total_and_not_the_notes_trade_figure():
    """The 10-K prints 4,315; the record also carries a trade figure of 2,855
    under `AccountsReceivableNetCurrent`, which the trend table reads first."""
    assert source.one_value(TICKER, "AccountsReceivableNetCurrent", Y2025, CUTOFF) == \
        2_855 * MILLION
    cell = payload()["beneish_m_score"]["inputs"]["receivables"][CURRENT]
    assert cell["value"] == 4_315 * MILLION


# --- Beneish, by hand -----------------------------------------------------------

def test_the_beneish_m_score_by_hand():
    c, p = CURRENT, PRIOR
    dsri = (4_315 / 44_284) / (3_929 / 38_962)
    gmi = ((38_962 - 17_060) / 38_962) / ((44_284 - 19_738) / 44_284)
    aqi = (1 - (25_754 + 4_690) / 50_143) / (1 - (25_231 + 4_665) / 55_154)
    sgi = 44_284 / 38_962
    depi = (1_706 / (1_706 + 4_665)) / (1_602 / (1_602 + 4_690))
    sgai = (3_110 / 44_284) / (2_759 / 38_962)
    lvgi = ((9_144 + 14_811) / 50_143) / ((10_504 + 13_270) / 55_154)
    total_accruals = (((25_754 - 25_231) - (5_520 - 7_849))
                      - ((9_144 - 10_504) - (0 - 1_364) - (1_007 - 1_080))
                      - 1_602)
    tata = total_accruals / 50_143
    m_score = (-4.84 + 0.920 * dsri + 0.528 * gmi + 0.404 * aqi + 0.892 * sgi
               + 0.115 * depi - 0.172 * sgai + 4.679 * tata - 0.327 * lvgi)

    # The same arithmetic again off the typed table, so a typo in one of the
    # two copies cannot pass for a result.
    assert dsri == (m("receivables", c) / m("revenue", c)) / (m("receivables", p) / m("revenue", p))
    assert total_accruals == 1_173

    row = payload()["beneish_m_score"]
    assert "missing" not in row, row.get("missing")
    got = row["component_values"]
    for name, expected in (("days_sales_in_receivables_index", dsri),
                           ("gross_margin_index", gmi),
                           ("asset_quality_index", aqi),
                           ("sales_growth_index", sgi),
                           ("depreciation_index", depi),
                           ("sales_general_and_administrative_expenses_index", sgai),
                           ("leverage_index", lvgi),
                           ("total_accruals_to_total_assets", tata)):
        assert got[name] == pytest.approx(expected, rel=1e-12), name
    assert row["total_accruals"] == pytest.approx(1_173 * MILLION, rel=1e-12)
    assert row["value"] == pytest.approx(m_score, rel=1e-12)


def test_the_beneish_coefficients_are_the_papers():
    assert baselines.BENEISH["coefficients"] == {
        "constant": -4.84,
        "days_sales_in_receivables_index": 0.920,
        "gross_margin_index": 0.528,
        "asset_quality_index": 0.404,
        "sales_growth_index": 0.892,
        "depreciation_index": 0.115,
        "sales_general_and_administrative_expenses_index": -0.172,
        "total_accruals_to_total_assets": 4.679,
        "leverage_index": -0.327,
    }


# --- Sloan, by hand ---------------------------------------------------------------

def test_accruals_over_average_assets_by_hand():
    accruals = (((25_754 - 25_231) - (5_520 - 7_849))
                - ((9_144 - 10_504) - (0 - 1_364) - (1_007 - 1_080))
                - 1_602)
    average = (50_143 + 55_154) / 2
    row = payload()["accruals_over_assets"]
    assert "missing" not in row, row.get("missing")
    assert row["accruals"] == pytest.approx(accruals * MILLION, rel=1e-12)
    assert row["average_total_assets"] == pytest.approx(average * MILLION, rel=1e-12)
    assert row["value"] == pytest.approx(accruals / average, rel=1e-12)


# --- Hirshleifer and others, by hand -----------------------------------------------

def test_net_operating_assets_by_hand():
    operating_assets = 50_143 - (5_520 + 4_635)
    operating_liabilities = 50_143 - 0 - 14_811 - 21_206
    row = payload()["net_operating_assets"]
    assert "missing" not in row, row.get("missing")
    assert row["component_values"]["operating_assets"] == \
        pytest.approx(operating_assets * MILLION, rel=1e-12)
    assert row["component_values"]["operating_liabilities"] == \
        pytest.approx(operating_liabilities * MILLION, rel=1e-12)
    assert row["value"] == pytest.approx(
        (operating_assets - operating_liabilities) / 55_154, rel=1e-12)


# --- Piotroski, by hand -------------------------------------------------------------

def test_the_piotroski_f_score_by_hand():
    roa_now, roa_before = 5_541 / 55_154, 10_142 / 51_040
    cfo_now = 14_012 / 55_154
    leverage_now = 14_811 / ((50_143 + 55_154) / 2)
    leverage_before = 13_270 / ((55_154 + 51_040) / 2)
    current_ratio_now, current_ratio_before = 25_754 / 9_144, 25_231 / 10_504
    margin_now = (44_284 - 19_738) / 44_284
    margin_before = (38_962 - 17_060) / 38_962
    turnover_now, turnover_before = 44_284 / 55_154, 38_962 / 51_040

    # Each signal, decided by hand from the quotients above:
    expected = {
        "return_on_assets_positive": 1,           # 0.100 > 0
        "operating_cash_flow_positive": 1,        # 0.254 > 0
        "return_on_assets_rose": 0,               # 0.100 against 0.199: fell
        "cash_flow_exceeds_return_on_assets": 1,  # 0.254 > 0.100
        "leverage_fell": 0,                       # 0.281 against 0.250: rose
        "current_ratio_rose": 1,                  # 2.82 against 2.40
        "no_common_equity_issued": 0,             # 404 million of proceeds
        "gross_margin_rose": 0,                   # 0.554 against 0.562
        "asset_turnover_rose": 1,                 # 0.803 against 0.763
    }
    assert roa_now > 0 and cfo_now > 0 and roa_now < roa_before and cfo_now > roa_now
    assert leverage_now > leverage_before
    assert current_ratio_now > current_ratio_before
    assert margin_now < margin_before and turnover_now > turnover_before

    row = payload()["piotroski_f_score"]
    assert "missing" not in row, row.get("missing")
    assert row["signal_values"] == expected
    assert row["value"] == 5
    measures = row["measures"]
    assert measures["return_on_assets"][CURRENT] == pytest.approx(roa_now, rel=1e-12)
    assert measures["return_on_assets"][PRIOR] == pytest.approx(roa_before, rel=1e-12)
    assert measures["leverage"][CURRENT] == pytest.approx(leverage_now, rel=1e-12)
    assert measures["leverage"][PRIOR] == pytest.approx(leverage_before, rel=1e-12)
    assert measures["asset_turnover"][PRIOR] == pytest.approx(turnover_before, rel=1e-12)


# --- Ohlson, by hand ----------------------------------------------------------------

def test_the_price_level_index_quarters_are_the_committed_vintage():
    directory = REPO_ROOT / "src" / "price_level_index"
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    for vintage in manifest["vintages"]:
        raw = (directory / vintage["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == vintage["sha256"]
    later = (directory / "gnp_implicit_price_deflator_vintage_2026-04-29.csv").read_text()
    earlier = (directory / "gnp_implicit_price_deflator_vintage_2025-08-29.csv").read_text()
    lines, earlier_lines = set(later.splitlines()), set(earlier.splitlines())
    for quarter, value in zip(("01-01", "04-01", "07-01", "10-01"), INDEX_2024):
        assert f"2024-{quarter},{value:.3f}" in lines
    for quarter, value in zip(("01-01", "04-01", "07-01", "10-01"), INDEX_1968):
        assert f"1968-{quarter},{value:.3f}" in lines
        assert f"1968-{quarter},{value:.3f}" in earlier_lines
    for quarter, value in zip(("01-01", "04-01", "07-01", "10-01"), INDEX_2024_EARLIER):
        assert f"2024-{quarter},{value:.3f}" in earlier_lines


def test_the_ohlson_o_score_by_hand():
    index = mean(INDEX_2024) / mean(INDEX_1968) * 100
    size = math.log(50_143 * MILLION / index)
    tlta = 28_937 / 50_143
    wcta = (25_754 - 9_144) / 50_143
    clca = 9_144 / 25_754
    oeneg = 0                                   # 28,937 of liabilities < 50,143 of assets
    nita = 5_541 / 50_143
    futl = 14_012 / 28_937
    intwo = 0                                   # neither year is a loss
    chin = (5_541 - 10_142) / (abs(5_541) + abs(10_142))
    o_score = (-1.32 - 0.407 * size + 6.03 * tlta - 1.43 * wcta + 0.0757 * clca
               - 1.72 * oeneg - 2.37 * nita - 1.83 * futl + 0.285 * intwo
               - 0.521 * chin)

    row = payload()["ohlson_o_score"]
    assert "missing" not in row, row.get("missing")
    level = row["price_level_index"]
    assert (level["vintage_date"], level["year"], level["base_year"]) == \
        ("2026-04-29", 2024, 1968)
    assert level["value"] == pytest.approx(index, rel=1e-12)
    got = row["component_values"]
    for name, expected in (("size", size),
                           ("total_liabilities_over_total_assets", tlta),
                           ("working_capital_over_total_assets", wcta),
                           ("current_liabilities_over_current_assets", clca),
                           ("liabilities_exceed_assets", oeneg),
                           ("net_income_over_total_assets", nita),
                           ("funds_from_operations_over_total_liabilities", futl),
                           ("net_loss_in_both_years", intwo),
                           ("change_in_net_income", chin)):
        assert got[name] == pytest.approx(expected, rel=1e-12), name
    assert row["value"] == pytest.approx(o_score, rel=1e-12)


def test_the_ohlson_coefficients_are_the_papers():
    assert baselines.OHLSON["coefficients"] == {
        "constant": -1.32,
        "size": -0.407,
        "total_liabilities_over_total_assets": 6.03,
        "working_capital_over_total_assets": -1.43,
        "current_liabilities_over_current_assets": 0.0757,
        "liabilities_exceed_assets": -1.72,
        "net_income_over_total_assets": -2.37,
        "funds_from_operations_over_total_liabilities": -1.83,
        "net_loss_in_both_years": 0.285,
        "change_in_net_income": -0.521,
    }


# --- Altman, by hand ----------------------------------------------------------------

def test_the_altman_ratios_by_hand_and_no_score_without_a_market_value():
    row = payload()["altman_z_score"]
    assert "value" not in row
    assert "market value of equity" in row["missing"]
    assert row["component_values"] == pytest.approx({
        "working_capital_over_total_assets": (25_754 - 9_144) / 50_143,
        "retained_earnings_over_total_assets": 20_646 / 50_143,
        "earnings_before_interest_and_taxes_over_total_assets": (12_663 + 664) / 50_143,
        "sales_over_total_assets": 44_284 / 50_143,
    }, rel=1e-12)


def test_the_altman_z_score_by_hand_on_a_planted_market_value():
    x1 = (25_754 - 9_144) / 50_143
    x2 = 20_646 / 50_143
    x3 = (12_663 + 664) / 50_143
    x4 = PLANTED_MARKET_VALUE / (28_937 * MILLION)
    x5 = 44_284 / 50_143
    z = (0.012 * (100 * x1) + 0.014 * (100 * x2) + 0.033 * (100 * x3)
         + 0.006 * (100 * x4) + 0.999 * x5)
    document = trends.read_record(TICKER, CUTOFF)
    planted = {"value": PLANTED_MARKET_VALUE, "source": "planted by the test"}
    row = baselines.formula_baselines(document, CUTOFF, period_end="2026-06-28",
                                      market_value_of_equity=planted)["rows"]["altman_z_score"]
    assert "missing" not in row, row.get("missing")
    assert row["component_values"]["market_value_of_equity_over_total_liabilities"] == \
        pytest.approx(x4, rel=1e-12)
    assert row["value"] == pytest.approx(z, rel=1e-12)
    assert baselines.ALTMAN["coefficients"] == {
        "working_capital_over_total_assets": 0.012,
        "retained_earnings_over_total_assets": 0.014,
        "earnings_before_interest_and_taxes_over_total_assets": 0.033,
        "market_value_of_equity_over_total_liabilities": 0.006,
        "sales_over_total_assets": 0.999,
    }


# --- the note cosine similarity -----------------------------------------------------

def test_cosine_similarity_by_hand_on_planted_text():
    """Case folds, digits and punctuation separate words, and nothing else is done.

    now:    revenue 2, rose 1, share 1        |now|    = sqrt(4 + 1 + 1)
    before: revenue 1, fell 1                 |before| = sqrt(1 + 1)
    dot:    revenue 2 * 1 = 2
    """
    now = baselines.words("Revenue rose; revenue-share 10%.")
    before = baselines.words("REVENUE fell.")
    assert dict(now) == {"revenue": 2, "rose": 1, "share": 1}
    assert dict(before) == {"revenue": 1, "fell": 1}
    assert baselines.cosine(now, before) == pytest.approx(2 / (math.sqrt(6) * math.sqrt(2)),
                                                          rel=1e-12)
    assert baselines.cosine(now, baselines.words("12,345 (678)")) is None


def test_a_note_tagged_inside_another_is_counted_once():
    """Planted: a table tagged inside its note repeats the note's words.

    Counted once, both filings hold alpha 1 and beta 1, and the cosine is 1.
    Counted twice, the later one would hold beta 2, (1 + 2) / (sqrt 5 * sqrt 2).
    Qualcomm's instances nest nothing, so only a planted pair asks this.
    """
    def filing(sections):
        return {"accession": "planted", "filing_date": "2026-01-01",
                "sections": [{"name": name, "contained_in": inside, "text": text}
                             for name, inside, text in sections]}

    now = filing([("note", None, "Alpha beta"), ("note_table", "note", "beta")])
    before = filing([("note", None, "alpha BETA")])
    row = baselines.note_cosine_similarity(now, before)
    assert row["value"] == pytest.approx(1.0, rel=1e-12)
    assert row["current"]["words"] == 2
    assert row["added"] == [] and row["removed"] == []
    assert row["sections"] == {"note": pytest.approx(1.0, rel=1e-12)}


def test_the_inventory_note_by_hand():
    """Qualcomm's inventory table in both 10-Qs, every word counted here.

    The two tables differ in one word: the June column heading against the
    March one. "Work-in-process" is three words and every figure is dropped.

    words     inventories in millions june/march september raw materials work
              process finished goods
    counts    1 2 1 1 1 1 1 1 1 1 1, the same in both
    dot       1 + 2*2 + 1 + 0 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 13
    |now|^2 = |before|^2 = 1 + 4 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 14
    """
    for form, role, heading in (("10-Q", "primary_html", "June 28,2026"),
                                ("10-Q", "prior_period", "March 29,2026")):
        table = (f"Inventories (in millions){heading}September 28,2025Raw materials"
                 f"$")
        assert independent_text.squeeze(table) in printed_text(form, role), role
    assert independent_text.squeeze(
        "Work-in-process5,005 3,985 Finished goods2,692 2,205") in \
        printed_text("10-Q", "primary_html")
    assert independent_text.squeeze(
        "Work-in-process4,346 3,985 Finished goods2,442 2,205") in \
        printed_text("10-Q", "prior_period")

    row = payload()["note_cosine_similarity"]
    assert row["sections"]["us-gaap:ScheduleOfInventoryCurrentTableTextBlock"] == \
        pytest.approx(13 / 14, rel=1e-12)


def test_the_whole_of_the_notes_by_an_independent_recount():
    """Every top-level note of both instances, recounted here and compared."""
    def recount(role):
        payload_ = extract_notes.extract(TICKER, "10-Q", role=role, cutoff=CUTOFF)
        counts = collections.Counter()
        for section in payload_["sections"]:
            if section["contained_in"] is None:
                counts.update(re.findall(r"[a-z]+", section["text"].lower()))
        return payload_["accession"], counts

    now_accession, now = recount("xbrl_instance")
    before_accession, before = recount("prior_period_xbrl_instance")
    assert (now_accession, before_accession) == (TRIGGER, PRIOR_QUARTER)
    dot = sum(now[word] * before[word] for word in now)
    expected = dot / (math.sqrt(sum(v * v for v in now.values()))
                      * math.sqrt(sum(v * v for v in before.values())))
    row = payload()["note_cosine_similarity"]
    assert row["value"] == pytest.approx(expected, rel=1e-12)
    assert (row["current"]["accession"], row["prior"]["accession"]) == \
        (TRIGGER, PRIOR_QUARTER)
    assert row["current"]["words"] == sum(now.values())
    assert row["prior"]["words"] == sum(before.values())


def test_the_notes_the_later_quarter_added_are_named():
    """The two tags are in the June instance and not in the March one."""
    def raw(role):
        entry = cutoff_guard.one_document(TICKER, "10-Q", role)
        data = entry["full_path"].read_bytes()
        return gzip.decompress(data) if entry["full_path"].suffix == ".gz" else data

    now, before = raw("xbrl_instance"), raw("prior_period_xbrl_instance")
    for tag in (b"SubsequentEventsTextBlock", b"ScheduleOfShortTermDebtTextBlock"):
        assert tag in now and tag not in before
    row = payload()["note_cosine_similarity"]
    assert sorted(row["added"]) == ["us-gaap:ScheduleOfShortTermDebtTextBlock",
                                    "us-gaap:SubsequentEventsTextBlock"]
    assert row["removed"] == []


def test_an_annual_trigger_has_no_prior_notes_to_compare_and_says_so():
    """The fixture stores a prior-period instance for the 10-Q and not the 10-K."""
    assert cutoff_guard.documents(TICKER, form="10-K",
                                  role="prior_period_xbrl_instance") == []
    row = payload("10-K")["note_cosine_similarity"]
    assert "value" not in row
    assert "prior_period_xbrl_instance" in row["missing"]


# --- the cutoff -----------------------------------------------------------------------

def test_a_vintage_dated_after_the_cutoff_is_not_read():
    """The 10-K's own run, at 2025-11-05, reads the vintage of 2025-08-29."""
    row = payload("10-K")["ohlson_o_score"]
    level = row["price_level_index"]
    assert (level["vintage_date"], level["year"]) == ("2025-08-29", 2024)
    assert level["value"] == pytest.approx(
        mean(INDEX_2024_EARLIER) / mean(INDEX_1968) * 100, rel=1e-12)
    assert row["component_values"]["size"] == pytest.approx(
        math.log(50_143 * MILLION / (mean(INDEX_2024_EARLIER) / mean(INDEX_1968) * 100)),
        rel=1e-12)


def test_the_price_level_index_at_each_side_of_each_vintage():
    def at(year, cutoff):
        return baselines.price_level_index(year, cutoff_guard.parse_date(cutoff))

    assert "no committed vintage" in at(2024, "2025-08-28")["missing"]
    on_the_day = at(2024, "2025-08-29")
    assert on_the_day["vintage_date"] == "2025-08-29"
    assert on_the_day["value"] == pytest.approx(
        mean(INDEX_2024_EARLIER) / mean(INDEX_1968) * 100, rel=1e-12)
    part_of_a_year = at(2025, "2026-04-28")
    assert part_of_a_year["vintage_date"] == "2025-08-29"
    assert "2 of the four quarters of 2025" in part_of_a_year["missing"]
    assert "value" not in part_of_a_year
    later = at(2025, "2026-04-29")
    assert later["vintage_date"] == "2026-04-29"
    assert later["value"] == pytest.approx(
        mean((127.485, 128.155, 129.337, 130.529)) / mean(INDEX_1968) * 100, rel=1e-12)


def test_a_vintage_whose_bytes_changed_is_refused(tmp_path):
    directory = tmp_path / "price_level_index"
    shutil.copytree(REPO_ROOT / "src" / "price_level_index", directory)
    path = directory / "gnp_implicit_price_deflator_vintage_2026-04-29.csv"
    path.write_text(path.read_text().replace("2024-01-01,124.284", "2024-01-01,100.000"))
    with pytest.raises(baselines.BaselineInputError, match="hashes to"):
        baselines.price_level_index(2024, cutoff_guard.parse_date("2026-07-29"),
                                    directory=directory)


def test_a_record_holding_a_row_filed_after_the_cutoff_is_refused():
    document = copy.deepcopy(trends.read_record(TICKER, CUTOFF))
    rows = document["facts"]["us-gaap"]["Assets"]["units"]["USD"]
    late = dict(rows[-1])
    late["filed"] = "2026-07-30"
    rows.append(late)
    with pytest.raises(baselines.BaselineInputError, match="after the cutoff"):
        baselines.formula_baselines(document, CUTOFF, period_end="2026-06-28")


def test_the_record_is_read_through_the_catalogue_gate():
    """Every row that reached the baselines was filed at or before the cutoff."""
    with cutoff_guard.recording() as opened:
        baselines.baselines(TICKER, "10-Q")
    record = cutoff_guard.one_document(TICKER, "companyfacts",
                                       "standard_taxonomy_history")["full_path"]
    assert record.resolve() in {Path(path).resolve() for path in opened}
    for row in ("beneish_m_score", "piotroski_f_score", "ohlson_o_score"):
        for by_year in payload()[row]["inputs"].values():
            for cell in by_year.values():
                assert cell["filed"] <= CUTOFF


# --- a term that is not there is not a zero ----------------------------------------------

def test_a_term_the_record_lacks_empties_the_rows_that_need_it_and_no_other():
    document = copy.deepcopy(trends.read_record(TICKER, CUTOFF))
    for tag in ("AccruedIncomeTaxesCurrent", "TaxesPayableCurrent"):
        document["facts"]["us-gaap"].pop(tag, None)
    rows = baselines.formula_baselines(document, CUTOFF, period_end="2026-06-28")["rows"]
    for name in ("beneish_m_score", "accruals_over_assets"):
        assert "value" not in rows[name], name
        assert "income_taxes_payable" in rows[name]["missing"], name
    for name in ("net_operating_assets", "piotroski_f_score", "ohlson_o_score"):
        assert "value" in rows[name], name


def test_an_index_over_two_different_concepts_is_refused():
    """The prior year's balance-sheet receivables taken out of a copy: the prior
    year falls to the trade figure under another tag, and an index of two
    different things is not computed."""
    document = copy.deepcopy(trends.read_record(TICKER, CUTOFF))
    rows = document["facts"]["us-gaap"]["AccountsAndOtherReceivablesNetCurrent"]["units"]["USD"]
    rows[:] = [row for row in rows if row["end"] != Y2024]
    beneish = baselines.formula_baselines(document, CUTOFF,
                                          period_end="2026-06-28")["rows"]["beneish_m_score"]
    assert "value" not in beneish
    assert "different concept" in beneish["missing"]
    assert "AccountsReceivableNetCurrent" in beneish["missing"]


# --- what is not computed, and the file itself ---------------------------------------------

def test_the_loughran_mcdonald_row_is_missing_with_its_reason_and_no_hash():
    row = payload()["loughran_mcdonald_negative"]
    assert "value" not in row
    assert "academic research" in row["missing"]
    assert "word_list" in payload()["manifest"]
    assert "sha256" not in payload()["manifest"]["word_list"]
    assert payload()["manifest"]["word_list"]["missing"]


def test_every_row_the_checklist_names_is_a_key():
    """The row keys are `docs/CHECKLIST.md`'s own, read out of its scorecard tables."""
    checklist = (REPO_ROOT / "docs" / "CHECKLIST.md").read_text(encoding="utf-8")
    for key in ("beneish_m_score", "accruals_over_assets", "net_operating_assets",
                "note_cosine_similarity", "loughran_mcdonald_negative",
                "piotroski_f_score", "ohlson_o_score", "altman_z_score"):
        assert f"| `{key}` |" in checklist, key
        assert key in payload(), key


def test_no_row_answers_the_market_direction():
    for key, row in payload().items():
        if isinstance(row, dict):
            assert "market_direction" not in row, key


def test_the_manifest_names_the_index_vintage_and_the_filings_read():
    manifest = payload()["manifest"]
    assert manifest["price_level_index"]["vintage_date"] == "2026-04-29"
    assert manifest["price_level_index"]["sha256"] == \
        "9abb183a812a41589010e5f4c18cd9cdc147c7c71aca6f49556d15609995bafa"
    assert set(manifest["record"]["filings_read"]) == {TRIGGER, TEN_K, OLDER_TEN_K}


def test_the_command_line_writes_the_file(tmp_path, capsys):
    out = tmp_path / "baselines.json"
    assert baselines.main(["--ticker", TICKER, "--out", str(out)]) == 0
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["piotroski_f_score"]["value"] == 5
    assert "6 of 8 rows computed" in capsys.readouterr().out


def test_the_command_line_refuses_a_company_with_no_record(tmp_path, capsys):
    out = tmp_path / "baselines.json"
    assert baselines.main(["--ticker", "ZZZZ", "--out", str(out)]) == baselines.BAD_INPUT
    assert not out.exists()
    assert "baselines:" in capsys.readouterr().err
