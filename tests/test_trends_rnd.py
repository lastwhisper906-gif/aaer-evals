"""The research-and-development-capitalized column, judged by hand on two companies.

`docs/INPUT_SPEC.md` §5 item 1 adds one column to the trend table: book value
and earnings with research and development capitalized. ESCO and Ciena, their
latest fiscal year each, with every term a number typed in here and every
quantity written out term by term. Nothing in this file came from running
`src/trends.py`.

Where each number was read:

- The three newest years of expense, the year's net income and the year-end
  equity are printed in the company's own 10-K, which is committed, and the test
  finds each one there with `tests/independent_text.py`, which imports nothing
  from `src/`.
- The three older years of expense are in 10-Ks this repository does not
  commit. They are read from the committed companyfacts record, by the
  accession of the 10-K that reported them, through `tests/companyfacts_source.py`,
  which opens the gzip itself.

The life is five years, straight line, a full year's weight on the year the
money was spent, and no tax effect — the default `docs/needs_judgment.md`
names. So, for a year:

    asset        = e0 * 5/5 + e1 * 4/5 + e2 * 3/5 + e3 * 2/5 + e4 * 1/5
    amortization = (e1 + e2 + e3 + e4 + e5) / 5
    earnings     = net income + e0 - amortization
    book value   = equity + asset

where `eK` is the expense K years back.

**Capitalized development cost.** Of the twelve, ESCO alone capitalizes one in
its latest 10-K — "Additions to capitalized software and other", 15,844
thousand for 2025 — and it tags that line `ese:PaymentsToAcquireAdditionalCapitalizedSoftware`,
its own extension, which companyfacts does not carry. Ciena says in words that
it "has not capitalized any software development costs", and tags no zero. Both
cells are therefore missing, and the test asserts they were not filled with a
zero: a number read from a sentence would be the model's job, not Python's.
"""

from __future__ import annotations

import copy
import functools
import gzip

import pytest

from src import cutoff_guard, trends
from tests import companyfacts_source as source
from tests import independent_text

LIFE = 5


@functools.lru_cache(maxsize=None)
def trigger(ticker: str) -> dict:
    """The 10-Q this run is about: its filing date is the cutoff."""
    return cutoff_guard.one_document(ticker, "10-Q", "primary_html")


@functools.lru_cache(maxsize=None)
def table(ticker: str) -> dict:
    report = trigger(ticker)
    return trends.table(ticker, report["filing_date"],
                        period_end=report["report_date"])


@functools.lru_cache(maxsize=None)
def ten_k_text(ticker: str) -> str:
    """The committed 10-K, tags stripped the naive way, whitespace removed.

    The zero-width spaces these filings pad their table cells with go too: they
    are layout, and `\\s` does not match them.
    """
    entry = cutoff_guard.one_document(ticker, "10-K", "primary_html")
    raw = entry["full_path"].read_bytes()
    if entry["full_path"].suffix == ".gz":
        raw = gzip.decompress(raw)
    text = independent_text.strip(raw.decode("utf-8")).replace("\u200b", "")
    return independent_text.squeeze(text)


def printed(ticker: str, phrase: str) -> None:
    assert independent_text.squeeze(phrase) in ten_k_text(ticker), \
        f"{ticker} 10-K does not print {phrase!r}"


def column(ticker: str, label: str = "FY-0") -> dict:
    row = {row["label"]: row for row in table(ticker)["years"]}[label]
    return row["research_and_development_capitalized"]


def in_the_record(ticker: str, tag: str, period: str, value: float,
                  accession: str, filed: str) -> None:
    """The typed number is the record's own row, and the rule settles on it."""
    standing = source.reported(ticker, tag, period, trigger(ticker)["filing_date"])
    assert {(row["val"], row["accn"], row["filed"]) for row in standing} == \
        {(value, accession, filed)}, f"{ticker} {tag} {period}: {standing}"


def expense_matches(cell: list[dict], expected: list[tuple]) -> None:
    assert [entry["years_back"] for entry in cell] == list(range(LIFE + 1))
    for entry, (period, value, accession, filed) in zip(cell, expected):
        assert "missing" not in entry, entry
        assert (entry["tag"], entry["period"], entry["value"],
                entry["accession"], entry["filed"]) == \
            ("ResearchAndDevelopmentExpense", period, value, accession, filed)


# --- ESCO, fiscal 2025 -------------------------------------------------------

ESE_TEN_K = "0001104659-25-117276"
ESE_EXPENSE = [
    ("2024-10-01..2025-09-30", 23_000_000.0, ESE_TEN_K, "2025-12-01"),
    ("2023-10-01..2024-09-30", 12_000_000.0, ESE_TEN_K, "2025-12-01"),
    ("2022-10-01..2023-09-30", 13_000_000.0, ESE_TEN_K, "2025-12-01"),
    ("2021-10-01..2022-09-30", 12_300_000.0, "0001410578-24-002064", "2024-11-29"),
    ("2020-10-01..2021-09-30", 15_400_000.0, "0001410578-23-002596", "2023-11-29"),
    ("2019-10-01..2020-09-30", 13_300_000.0, "0001410578-22-003540", "2022-11-29"),
]


def test_escos_expense_is_what_its_filings_report():
    printed("ESE", "research and development expenses from continuing operations "
                   "were approximately $ 23.0 million, $ 12.0 million and "
                   "$ 13.0 million for 2025, 2024 and 2023")
    printed("ESE", "Net earnings $ 299,223 101,881 92,545")
    printed("ESE", "Total shareholders\u2019 equity 1,540,871")
    for period, value, accession, filed in ESE_EXPENSE:
        in_the_record("ESE", "ResearchAndDevelopmentExpense", period, value,
                      accession, filed)


def test_escos_fiscal_2025_capitalized_by_hand():
    cell = column("ESE")
    expense_matches(cell["research_and_development_expense"], ESE_EXPENSE)
    assert cell["net_income"]["value"] == 299_223_000.0
    assert cell["stockholders_equity"]["value"] == 1_540_871_000.0

    asset = (23_000_000.0 * 5 / 5 + 12_000_000.0 * 4 / 5 + 13_000_000.0 * 3 / 5
             + 12_300_000.0 * 2 / 5 + 15_400_000.0 * 1 / 5)
    amortization = (12_000_000.0 + 13_000_000.0 + 12_300_000.0
                    + 15_400_000.0 + 13_300_000.0) / 5
    assert cell["research_and_development_asset"]["value"] == \
        pytest.approx(asset, rel=1e-12)
    assert cell["research_and_development_amortization"]["value"] == \
        pytest.approx(amortization, rel=1e-12)
    assert cell["earnings_with_rnd_capitalized"]["value"] == \
        pytest.approx(299_223_000.0 + 23_000_000.0 - amortization, rel=1e-12)
    assert cell["book_value_with_rnd_capitalized"]["value"] == \
        pytest.approx(1_540_871_000.0 + asset, rel=1e-12)


def test_escos_capitalized_software_is_in_the_filing_and_not_in_the_record():
    """The 10-K prints the line; the record has no us-gaap row for the year."""
    printed("ESE", "Additions to capitalized software and other ( 15,844 ) "
                   "( 11,903 ) ( 10,271 )")
    for tag in ("CapitalizedComputerSoftwareAdditions",):
        assert not source.for_period(source.rows("ESE", tag),
                                     "2024-10-01..2025-09-30")
    cell = column("ESE")
    assert "value" not in cell["capitalized_development_cost"]
    assert "CapitalizedComputerSoftwareAdditions" in \
        cell["capitalized_development_cost"]["missing"]
    assert "value" not in cell["capitalized_over_expense"]


# --- Ciena, fiscal 2025 ------------------------------------------------------

CIEN_TEN_K = "0001628280-25-056698"
CIEN_EXPENSE = [
    ("2024-11-03..2025-11-01", 848_329_000.0, CIEN_TEN_K, "2025-12-12"),
    ("2023-10-29..2024-11-02", 767_497_000.0, CIEN_TEN_K, "2025-12-12"),
    ("2022-10-30..2023-10-28", 750_559_000.0, CIEN_TEN_K, "2025-12-12"),
    ("2021-10-31..2022-10-29", 624_656_000.0, "0000936395-24-000044", "2024-12-20"),
    ("2020-11-01..2021-10-30", 536_666_000.0, "0000936395-23-000044", "2023-12-15"),
    ("2019-11-03..2020-10-31", 529_888_000.0, "0000936395-22-000065", "2022-12-16"),
]


def test_cienas_expense_is_what_its_filings_report():
    printed("CIEN", "Research and development 848,329 767,497 750,559")
    printed("CIEN", "Net income $ 123,338 $ 83,956 $ 254,827")
    printed("CIEN", "Total stockholders\u2019 equity 2,729,323 2,816,138")
    for period, value, accession, filed in CIEN_EXPENSE:
        in_the_record("CIEN", "ResearchAndDevelopmentExpense", period, value,
                      accession, filed)


def test_cienas_fiscal_2025_capitalized_by_hand():
    cell = column("CIEN")
    expense_matches(cell["research_and_development_expense"], CIEN_EXPENSE)
    assert cell["net_income"]["value"] == 123_338_000.0
    assert cell["stockholders_equity"]["value"] == 2_729_323_000.0

    asset = (848_329_000.0 * 5 / 5 + 767_497_000.0 * 4 / 5 + 750_559_000.0 * 3 / 5
             + 624_656_000.0 * 2 / 5 + 536_666_000.0 * 1 / 5)
    amortization = (767_497_000.0 + 750_559_000.0 + 624_656_000.0
                    + 536_666_000.0 + 529_888_000.0) / 5
    assert cell["research_and_development_asset"]["value"] == \
        pytest.approx(asset, rel=1e-12)
    assert cell["research_and_development_amortization"]["value"] == \
        pytest.approx(amortization, rel=1e-12)
    assert cell["earnings_with_rnd_capitalized"]["value"] == \
        pytest.approx(123_338_000.0 + 848_329_000.0 - amortization, rel=1e-12)
    assert cell["book_value_with_rnd_capitalized"]["value"] == \
        pytest.approx(2_729_323_000.0 + asset, rel=1e-12)


def test_a_zero_ciena_states_in_words_is_not_a_zero_in_the_column():
    printed("CIEN", "Accordingly, Ciena has not capitalized any software "
                    "development costs.")
    assert not source.rows("CIEN", "CapitalizedComputerSoftwareAdditions")
    cell = column("CIEN")
    assert "value" not in cell["capitalized_development_cost"]
    assert cell["capitalized_development_cost"]["missing"]
    assert "value" not in cell["capitalized_over_expense"]


# --- the rules around the arithmetic -----------------------------------------

def test_the_asset_rolls_forward_by_expense_less_amortization():
    """asset this year = asset last year + this year's expense - amortization.

    A property of straight-line amortization, not of these numbers, checked on
    Ciena's two newest years; the older year's expense runs six years back to
    fiscal 2019, typed from the 10-K `0000936395-21-000054` row of the record.
    """
    in_the_record("CIEN", "ResearchAndDevelopmentExpense", "2018-11-04..2019-11-02",
                  548_139_000.0, "0000936395-21-000054", "2021-12-17")
    this, last = column("CIEN", "FY-0"), column("CIEN", "FY-1")
    assert this["research_and_development_asset"]["value"] == pytest.approx(
        last["research_and_development_asset"]["value"] + 848_329_000.0
        - this["research_and_development_amortization"]["value"], rel=1e-12)


def test_a_year_the_record_lacks_is_missing_and_never_a_zero():
    """ESCO's fiscal 2021 expense taken out of a copy of the record: every
    quantity that needs it says so by naming the year, and none is filled."""
    report = trigger("ESE")
    document = copy.deepcopy(trends.read_record("ESE", report["filing_date"]))
    rows = document["facts"]["us-gaap"]["ResearchAndDevelopmentExpense"]["units"]["USD"]
    rows[:] = [row for row in rows if row["end"] != "2021-09-30"]
    payload = trends.trends(document, report["filing_date"],
                            period_end=report["report_date"])
    cell = payload["years"][0]["research_and_development_capitalized"]
    for name in ("research_and_development_asset",
                 "research_and_development_amortization",
                 "earnings_with_rnd_capitalized",
                 "book_value_with_rnd_capitalized"):
        assert "value" not in cell[name], name
        assert "4 year(s) back" in cell[name]["missing"], name
    assert cell["research_and_development_expense"][4]["missing"]


def test_the_column_does_not_move_the_tables_periods():
    """The three terms the column reads are not evidence of a fiscal period."""
    for term in trends.COLUMN_ONLY_TERMS:
        for tag in trends.CONCEPTS[term][1]:
            assert tag not in trends.PERIOD_TAGS, tag


def test_every_filing_the_column_read_is_named_as_read():
    payload = table("ESE")
    named = set(payload["source"]["filings_read"])
    for accession in ("0001410578-22-003540", "0001410578-23-002596",
                      "0001410578-24-002064", ESE_TEN_K):
        assert accession in named, accession
