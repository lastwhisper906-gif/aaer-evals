"""The derived fourth quarter, against three companies' filings read by eye.

The expected values are not this module's output and are not a companyfacts
round trip through it. For three companies they are two figures printed on the
face of two committed filings -- the annual figure in the 10-K's income
statement and the nine-month year-to-date figure in the prior-year column of a
Q3 10-Q's income statement -- transcribed into `READ_OFF_THE_FILINGS` with the
caption each one sits under, and subtracted there so a reader can follow every
line of the arithmetic without running anything.

The subtraction is checked as arithmetic before it is used as an expectation, so
a slip in transcription fails on its own line rather than quietly becoming the
number the module is held to.

Both filings are in the fixture set and both are named by accession, and
`test_the_two_figures_were_taken_from_the_filings_they_were_read_off` closes the
loop: companyfacts stamps each row with the accession that filed it, and for all
three companies every figure the derivation used carries the accession of the
filing the number above was read off. Two records of the same two documents, and
the numbers have to agree.

Two more cases are read off the record rather than off a filing, because the
filings that carry them are not in this fixture set and the record is the source
this module reads: Seagate's 2024 net income, where the fourth quarter is bigger
than the year it sits in, and Carrier's 2022 revenue, where the year was recast
after its nine months was last stated. Both are transcribed row by row with the
accession each row carries, checked against companyfacts read straight, and
subtracted here.

The rest is over all twelve: the quarter re-adds to the year, the two periods
share a start and leave one quarter between their ends, a measure that is not
there says why and never arrives as a zero, no company reports two fiscal years
ending on the same day, and the indicator reports its value and raises no flag.
The planted documents at the end are the guards -- an absent nine months, two of
them, a filing that reports one period twice, a figure restated after the other
was last stated, an annual duration under a tag no measure names, a residual
that is not a quarter, a fact filed after the cutoff -- each with the control
that shows the same document derives cleanly once the fault is taken out.
"""

from __future__ import annotations

import datetime as dt
import functools
import hashlib
import json
from pathlib import Path

import pytest

from src import cutoff_guard, fetch_companyfacts, fourth_quarter
from src.fetch_fixtures import TICKERS
from tests.test_fetch_companyfacts import (NOT_YET_IN_COMPANYFACTS,
                                           record as companyfacts_record)

# --- what the filings say ---------------------------------------------------
#
# Per company: the fiscal year, the nine-month year-to-date period inside it,
# the two filings the figures were read off, the multiple the statement is
# printed in, and one line per measure --
#
#     measure: (the caption on the statement, annual, nine months, the quarter)
#
# The fourth quarter is the third number minus the second, done here and not by
# the module under test.

READ_OFF_THE_FILINGS = {
    # Apple Inc.
    #   10-K, fiscal year ended September 27, 2025, CONSOLIDATED STATEMENTS OF
    #   OPERATIONS, the "2025" column. Dollars in millions.
    #   10-Q for the quarter ended June 27, 2026, CONDENSED CONSOLIDATED
    #   STATEMENTS OF OPERATIONS, the "Nine Months Ended June 28, 2025" column.
    "AAPL": {
        "fiscal_year": {"start": "2024-09-29", "end": "2025-09-27"},
        "nine_months_end": "2025-06-28",
        "printed_in": 1_000_000,
        "annual_filing": ("10-K", "0000320193-25-000079"),
        "nine_months_filing": ("10-Q", "0000320193-26-000020"),
        "measures": {
            "revenue": ("Total net sales", 416_161, 313_695, 102_466),
            "cost_of_revenue": ("Total cost of sales", 220_960, 166_835, 54_125),
            "gross_profit": ("Gross margin", 195_201, 146_860, 48_341),
            "operating_income": ("Operating income", 133_050, 100_623, 32_427),
            "net_income": ("Net income", 112_010, 84_544, 27_466),
            "research_and_development": (
                "Research and development", 34_550, 25_684, 8_866),
            "selling_general_and_administrative": (
                "Selling, general and administrative", 27_601, 20_553, 7_048),
            "income_tax_expense": (
                "Provision for income taxes", 20_719, 15_381, 5_338),
        },
    },
    # QUALCOMM Incorporated
    #   10-K, fiscal year ended September 28, 2025, CONSOLIDATED STATEMENTS OF
    #   OPERATIONS, the "September 28, 2025" column. Dollars in millions.
    #   10-Q for the quarter ended June 28, 2026, CONDENSED CONSOLIDATED
    #   STATEMENTS OF OPERATIONS, the "Nine Months Ended June 29, 2025" column.
    #   Both statements show income tax as a deduction, "( 7,122 )" and
    #   "( 1,034 )"; the income taxes note states the same two figures as
    #   "Income tax expense $ 7,122" and "$ 1,034", which is the sign
    #   us-gaap:IncomeTaxExpenseBenefit carries, so that is the caption cited.
    "QCOM": {
        "fiscal_year": {"start": "2024-09-30", "end": "2025-09-28"},
        "nine_months_end": "2025-06-29",
        "printed_in": 1_000_000,
        "annual_filing": ("10-K", "0000804328-25-000085"),
        "nine_months_filing": ("10-Q", "0000804328-26-000086"),
        "measures": {
            "revenue": ("Total revenues", 44_284, 33_013, 11_271),
            "cost_of_revenue": ("Cost of revenues", 19_738, 14_704, 5_034),
            "operating_income": ("Operating income", 12_355, 9_437, 2_918),
            "net_income": ("Net income", 5_541, 8_658, -3_117),
            "research_and_development": (
                "Research and development", 9_042, 6_672, 2_370),
            "selling_general_and_administrative": (
                "Selling, general and administrative", 3_110, 2_200, 910),
            "income_tax_expense": (
                "Income tax expense, income taxes note", 7_122, 1_034, 6_088),
        },
    },
    # ESCO Technologies Inc.
    #   10-K, fiscal year ended September 30, 2025, CONSOLIDATED STATEMENTS OF
    #   OPERATIONS, the "2025" column. Dollars in thousands.
    #   10-Q for the quarter ended June 30, 2026, CONDENSED CONSOLIDATED
    #   STATEMENTS OF OPERATIONS, the "Nine Months Ended June 30, 2025" column.
    "ESE": {
        "fiscal_year": {"start": "2024-10-01", "end": "2025-09-30"},
        "nine_months_end": "2025-06-30",
        "printed_in": 1_000,
        "annual_filing": ("10-K", "0001104659-25-117276"),
        "nine_months_filing": ("10-Q", "0001104659-26-093266"),
        "measures": {
            "revenue": ("Net sales", 1_095_388, 742_714, 352_674),
            "cost_of_revenue": ("Cost of sales", 634_303, 431_068, 203_235),
            "net_income": ("Net earnings", 299_223, 80_571, 218_652),
            "selling_general_and_administrative": (
                "Selling, general and administrative expenses",
                234_638, 171_305, 63_333),
            "income_tax_expense": ("Income tax expense", 36_554, 21_841, 14_713),
        },
    },
}

NAMED = sorted(READ_OFF_THE_FILINGS)
CASES = sorted((ticker, term) for ticker in NAMED
               for term in READ_OFF_THE_FILINGS[ticker]["measures"])


@functools.lru_cache(maxsize=None)
def derived(ticker: str) -> dict:
    """One company's derivation, read once. The twelve records are large."""
    return fourth_quarter.fourth_quarters(ticker)


def latest_year(ticker: str) -> dict:
    return derived(ticker)["fiscal_years"][0]


def year_ending(ticker: str, end: str) -> dict:
    """One named fiscal year, for the two cases read off the record by hand."""
    return next(year for year in derived(ticker)["fiscal_years"]
                if year["fiscal_year"]["end"] == end)


def leaves(payload) -> list:
    """Every leaf in the payload, for the assertions that are about all of them."""
    if isinstance(payload, dict):
        return [leaf for value in payload.values() for leaf in leaves(value)]
    if isinstance(payload, list):
        return [leaf for value in payload for leaf in leaves(value)]
    return [payload]


def record_row(value: int, accession: str, start: str, end: str) -> dict:
    """One companyfacts row, as it was transcribed off the record by hand."""
    return {"value": value, "accession": accession, "start": start, "end": end}


def value_on_record(ticker: str, tag: str, transcribed: dict) -> int:
    """A transcribed row's value, checked against companyfacts read straight.

    `tests/test_fetch_companyfacts.py` keys the record by tag, unit, accession
    and period, which is what a row transcribed by hand names. Nothing here
    passes through `src/fourth_quarter.py`, so a figure it hands back is a
    figure from the source and not from the module it is used to measure.
    """
    index = companyfacts_record(ticker)["index"]
    key = (tag, "USD", transcribed["accession"],
           transcribed["start"], transcribed["end"])
    assert index.get(key) == (float(transcribed["value"]),), \
        f"companyfacts holds {index.get(key)} under {key}, " \
        f"not {transcribed['value']:,}"
    return transcribed["value"]


# --- the three companies, read off the filings -------------------------------

@pytest.mark.parametrize("ticker", NAMED)
def test_the_subtraction_written_out_is_arithmetic(ticker):
    """The table's own third column. A transcription slip fails here, before it
    can become the expectation the module is measured against."""
    wrong = [f"{term} ({caption}): {annual:,} - {nine:,} is {annual - nine:,}, "
             f"not {quarter:,}"
             for term, (caption, annual, nine, quarter)
             in sorted(READ_OFF_THE_FILINGS[ticker]["measures"].items())
             if annual - nine != quarter]
    assert not wrong, f"{ticker}:\n" + "\n".join(wrong)


@pytest.mark.parametrize("ticker,term", CASES)
def test_the_fourth_quarter_is_the_annual_figure_minus_the_nine_month_figure(
        ticker, term):
    filed = READ_OFF_THE_FILINGS[ticker]
    caption, annual, nine, quarter = filed["measures"][term]
    scale = filed["printed_in"]
    cell = latest_year(ticker)["measures"][term]

    assert "missing" not in cell, \
        f"{ticker} {term} ({caption}): {cell.get('missing')}"
    assert cell["annual"] == annual * scale, \
        f"{ticker} {term}: the filing prints {caption} as {annual:,}"
    assert cell["nine_months"] == nine * scale, \
        f"{ticker} {term}: the filing prints {caption} as {nine:,} for the nine months"
    assert cell["fourth_quarter"] == quarter * scale, \
        (f"{ticker} {term}: {annual:,} - {nine:,} = {quarter:,} "
         f"({caption}, printed in units of {scale:,})")
    assert cell["formula"] == fourth_quarter.DERIVATION


@pytest.mark.parametrize("ticker", NAMED)
def test_the_periods_are_the_ones_the_two_filings_cover(ticker):
    filed = READ_OFF_THE_FILINGS[ticker]
    year = latest_year(ticker)
    assert year["fiscal_year"]["start"] == filed["fiscal_year"]["start"]
    assert year["fiscal_year"]["end"] == filed["fiscal_year"]["end"]

    for term, cell in sorted(year["measures"].items()):
        if term not in filed["measures"]:
            continue
        assert cell["nine_month_period"] == {
            "start": filed["fiscal_year"]["start"],
            "end": filed["nine_months_end"],
            "days": fourth_quarter._days(filed["fiscal_year"]["start"],
                                         filed["nine_months_end"])}
        # The quarter nobody files: it opens the day after the nine months close
        # and shuts on the last day of the year.
        opens = (dt.date.fromisoformat(filed["nine_months_end"])
                 + dt.timedelta(days=1)).isoformat()
        assert cell["fourth_quarter_period"]["start"] == opens
        assert cell["fourth_quarter_period"]["end"] == filed["fiscal_year"]["end"]


@pytest.mark.parametrize("ticker", NAMED)
def test_the_two_figures_were_taken_from_the_filings_they_were_read_off(ticker):
    """companyfacts stamps every row with the accession that filed it, and those
    accessions are the two documents the numbers above were transcribed from."""
    filed = READ_OFF_THE_FILINGS[ticker]
    on_record = {(row["form"], row["accession"])
                 for row in cutoff_guard.documents(ticker)}
    for which in ("annual_filing", "nine_months_filing"):
        assert filed[which] in on_record, \
            f"{ticker}: {filed[which]} is not a filing in this fixture set"

    for term in sorted(filed["measures"]):
        cell = latest_year(ticker)["measures"][term]
        assert cell["annual_as_filed"]["accessions"] == [filed["annual_filing"][1]]
        assert cell["nine_months_as_filed"]["accessions"] == \
            [filed["nine_months_filing"][1]]


# --- the indicator reports a value ------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_the_dump_indicator_reports_a_value_and_raises_no_flag(ticker):
    """Until rules v0.1 there is no size that makes a fourth quarter a dump, so
    there is nothing here that could be read as one: no boolean anywhere in the
    payload, and the indicator says in its own words that it does not flag."""
    payload = derived(ticker)
    booleans = [leaf for leaf in leaves(payload) if isinstance(leaf, bool)]
    assert not booleans, f"{ticker}: the payload carries {len(booleans)} booleans"
    for year in payload["fiscal_years"]:
        indicator = year["dump_indicator"]
        assert set(indicator) == {"key", "reports", "share_of_the_year",
                                  "margin_move"}
        assert indicator["key"] == "fourth_quarter_dump"
        assert indicator["reports"] == fourth_quarter.REPORTS_A_VALUE
        assert "does not flag" in indicator["reports"]
        assert set(indicator["share_of_the_year"]) == set(fourth_quarter.MEASURES)
        assert set(indicator["margin_move"]) == set(fourth_quarter.MARGINS)


# Seagate's fiscal 2024 net income, taken from the two rows of the committed
# companyfacts record -- the source this module reads -- with the accession each
# row carries. Neither figure and neither subtraction below comes from
# `src/fourth_quarter.py`; the year the fourth quarter is bigger than is named
# here so a reader can check it against the record rather than against a run.
#
#   us-gaap:NetIncomeLoss [USD]
#     2023-07-01..2024-06-28    335,000,000   10-K  0001137789-26-000159
#     2023-07-01..2024-03-29   -178,000,000   10-Q  0001137789-25-000075
#
#     fourth quarter    335,000,000 - (-178,000,000) = 513,000,000
#     share of the year 513,000,000 / 335,000,000    = 1.531343283...
A_QUARTER_BIGGER_THAN_ITS_YEAR = {
    "ticker": "STX",
    "term": "net_income",
    "tag": "NetIncomeLoss",
    "fiscal_year_end": "2024-06-28",
    "annual": record_row(335_000_000, "0001137789-26-000159",
                         "2023-07-01", "2024-06-28"),
    "nine_months": record_row(-178_000_000, "0001137789-25-000075",
                              "2023-07-01", "2024-03-29"),
    "fourth_quarter": 513_000_000,
    "share": 1.531343283,
}


def test_the_two_rows_the_biggest_quarter_was_read_from_are_in_the_record():
    """The transcription above, checked against companyfacts read straight and
    subtracted here -- so the case the next test names rests on the source and
    not on the module the next test measures."""
    case = A_QUARTER_BIGGER_THAN_ITS_YEAR
    annual = value_on_record(case["ticker"], case["tag"], case["annual"])
    nine = value_on_record(case["ticker"], case["tag"], case["nine_months"])
    assert annual - nine == case["fourth_quarter"]
    assert case["fourth_quarter"] / annual \
        == pytest.approx(case["share"], abs=1e-9)


def test_a_quarter_that_carries_more_than_the_whole_year_is_still_only_a_value():
    """The control on the silence above. A share over one means the fourth
    quarter carried more than the entire year -- a boundary, not a chosen level
    -- and the record holds such a quarter: the one read off it above. It is
    reported, and nothing in the payload turns it into a flag."""
    case = A_QUARTER_BIGGER_THAN_ITS_YEAR
    extreme = [(ticker, year["fiscal_year"]["end"], term, share)
               for ticker in TICKERS
               for year in derived(ticker)["fiscal_years"]
               for term, share
               in sorted(year["dump_indicator"]["share_of_the_year"].items())
               if "value" in share and abs(share["value"]) > 1]
    assert (case["ticker"], case["fiscal_year_end"], case["term"]) \
        in {(ticker, end, term) for ticker, end, term, _ in extreme}, \
        f"{case['ticker']} {case['fiscal_year_end']} {case['term']} is a share " \
        f"of {case['share']} in the record and is not reported as one"
    for ticker, end, term, share in extreme:
        # The ratio never travels alone: a negative annual figure flips its
        # sign, so the two figures it was divided from go with it.
        assert set(share) == {"value", "formula", "fourth_quarter", "annual"}, \
            f"{ticker} {end} {term}"

    cell = year_ending(case["ticker"],
                       case["fiscal_year_end"])["measures"][case["term"]]
    assert cell["annual"] == case["annual"]["value"]
    assert cell["nine_months"] == case["nine_months"]["value"]
    assert cell["fourth_quarter"] == case["fourth_quarter"]


def test_the_share_of_the_year_is_the_quarter_over_the_year():
    """Divided by hand from the figures read off the filings above.

        Apple      102,466 / 416,161   = 0.246217209...
        QUALCOMM     6,088 /   7,122   = 0.854816062...  (income tax expense)
        QUALCOMM    -3,117 /   5,541   = -0.562533838... (a fourth-quarter loss)
        ESCO       218,652 / 299,223   = 0.730732597...  (net earnings)
    """
    expected = {
        ("AAPL", "revenue"): 0.246217209,
        ("QCOM", "income_tax_expense"): 0.854816062,
        ("QCOM", "net_income"): -0.562533838,
        ("ESE", "net_income"): 0.730732597,
    }
    for (ticker, term), value in sorted(expected.items()):
        share = latest_year(ticker)["dump_indicator"]["share_of_the_year"][term]
        assert share["formula"] == "fourth_quarter / annual"
        assert share["value"] == pytest.approx(value, abs=1e-9)


def test_the_margin_move_is_the_quarter_margin_less_the_nine_month_margin():
    """Also by hand, from the same figures.

        Apple gross margin, nine months  (313,695 - 166,835) / 313,695
                                         = 0.468161749...
        Apple gross margin, the quarter  (102,466 -  54,125) / 102,466
                                         = 0.471776003...
                                    move = 0.003614254...

        QUALCOMM operating margin, nine months   9,437 / 33,013 = 0.285857086...
        QUALCOMM operating margin, the quarter   2,918 / 11,271 = 0.258894508...
                                          move = -0.026962578...
    """
    apple = latest_year("AAPL")["dump_indicator"]["margin_move"]["gross_margin"]
    assert apple["nine_months"] == pytest.approx(0.468161749, abs=1e-9)
    assert apple["fourth_quarter"] == pytest.approx(0.471776003, abs=1e-9)
    assert apple["move"] == pytest.approx(0.003614254, abs=1e-9)

    qualcomm = latest_year("QCOM")["dump_indicator"]["margin_move"]["operating_margin"]
    assert qualcomm["nine_months"] == pytest.approx(0.285857086, abs=1e-9)
    assert qualcomm["fourth_quarter"] == pytest.approx(0.258894508, abs=1e-9)
    assert qualcomm["move"] == pytest.approx(-0.026962578, abs=1e-9)


def test_a_margin_whose_terms_are_not_both_there_says_which_one_is_missing():
    """ESCO tags no us-gaap:OperatingIncomeLoss for its fourth quarter, so the
    operating margin is a reason and not a number -- while its gross margin,
    whose two terms are both there, is.

        ESCO gross margin, nine months  (742,714 - 431,068) / 742,714
                                        = 0.419604316...
        ESCO gross margin, the quarter  (352,674 - 203,235) / 352,674
                                        = 0.423731264...
                                   move = 0.004126948...
    """
    moves = latest_year("ESE")["dump_indicator"]["margin_move"]
    assert "value" not in moves["operating_margin"]
    assert "operating_income" in moves["operating_margin"]["missing"]
    assert moves["gross_margin"]["nine_months"] == pytest.approx(0.419604316, abs=1e-9)
    assert moves["gross_margin"]["fourth_quarter"] == pytest.approx(
        0.423731264, abs=1e-9)
    assert moves["gross_margin"]["move"] == pytest.approx(0.004126948, abs=1e-9)


# --- over all twelve ---------------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_the_quarter_re_adds_to_the_year(ticker):
    for year in derived(ticker)["fiscal_years"]:
        for term, cell in sorted(year["measures"].items()):
            if "missing" in cell:
                continue
            assert cell["nine_months"] + cell["fourth_quarter"] == \
                pytest.approx(cell["annual"]), \
                f"{ticker} {year['fiscal_year']['end']} {term}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_two_periods_share_a_start_and_leave_one_quarter(ticker):
    for year in derived(ticker)["fiscal_years"]:
        span = year["fiscal_year"]
        assert fourth_quarter.YEAR_DAYS[0] <= span["days"] \
            <= fourth_quarter.YEAR_DAYS[1]
        for term, cell in sorted(year["measures"].items()):
            if "missing" in cell:
                continue
            nine, quarter = cell["nine_month_period"], cell["fourth_quarter_period"]
            assert nine["start"] == span["start"]
            assert nine["end"] < span["end"]
            assert fourth_quarter.NINE_MONTH_DAYS[0] <= nine["days"] \
                <= fourth_quarter.NINE_MONTH_DAYS[1]
            assert quarter["end"] == span["end"]
            assert nine["days"] + quarter["days"] == span["days"]
            assert fourth_quarter.QUARTER_DAYS[0] <= quarter["days"] \
                <= fourth_quarter.QUARTER_DAYS[1]
            assert cell["tag"] in fourth_quarter.MEASURES[term]


@pytest.mark.parametrize("ticker", TICKERS)
def test_a_measure_that_is_not_there_says_why_and_never_arrives_as_a_zero(ticker):
    """A missing figure carries no number at all. Standing a zero in for it
    would publish the whole year as the fourth quarter, in the exact shape a
    dump has."""
    numeric = {"annual", "nine_months", "fourth_quarter"}
    for year in derived(ticker)["fiscal_years"]:
        for term, cell in sorted(year["measures"].items()):
            if "missing" not in cell:
                assert numeric <= set(cell)
                continue
            where = f"{ticker} {year['fiscal_year']['end']} {term}"
            assert set(cell) == {"missing"}, \
                f"{where} carries {sorted(numeric & set(cell))} beside its reason"
            assert term in cell["missing"] and "us-gaap:" in cell["missing"], where
            assert cell["missing"].startswith("no fourth quarter for "), where
            share = year["dump_indicator"]["share_of_the_year"][term]
            assert set(share) == {"missing"}, where


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_derived_figure_names_the_filing_it_came_from(ticker):
    for year in derived(ticker)["fiscal_years"]:
        for term, cell in sorted(year["measures"].items()):
            if "missing" in cell:
                continue
            for side in ("annual_as_filed", "nine_months_as_filed"):
                stamp = cell[side]
                assert stamp["accessions"], f"{ticker} {term} {side}"
                assert dt.date.fromisoformat(stamp["filed"]) \
                    <= dt.date.fromisoformat(derived(ticker)["cutoff"])
                for older in stamp["superseded"]:
                    assert older["filed"] < stamp["filed"]
                    assert older["value"] != cell[side.replace("_as_filed", "")]


def test_the_two_filings_companyfacts_has_not_loaded_are_in_no_derived_figure():
    """`tests/test_fetch_companyfacts.py` records the two accessions in no
    companyfacts row at all. A period that would have to be looked up in one of
    them has nothing to look up, so it is absent, and no figure here rests on
    one."""
    unloaded = {accession for _, _, accession in NOT_YET_IN_COMPANYFACTS}
    named = {accession
             for ticker in TICKERS
             for year in derived(ticker)["fiscal_years"]
             for cell in year["measures"].values() if "missing" not in cell
             for side in ("annual_as_filed", "nine_months_as_filed")
             for accession in (cell[side]["accessions"]
                               + [older["accession"]
                                  for older in cell[side]["superseded"]])}
    assert not unloaded & named, \
        f"a derived figure rests on {sorted(unloaded & named)}, which companyfacts " \
        f"holds no row for"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_record_is_read_through_the_gate(ticker):
    """Not "it imports cutoff_guard": the gate records what it opened, and the
    companyfacts document has to be in that list."""
    with cutoff_guard.recording() as opened:
        fourth_quarter.fourth_quarters(ticker)
    row = cutoff_guard.one_document(ticker, fetch_companyfacts.FORM,
                                    fetch_companyfacts.ROLE)
    assert [path.name for path in opened] == [Path(row["path"]).name]


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_derivation_is_the_same_twice(ticker):
    assert fourth_quarter.render(derived(ticker)) \
        == fourth_quarter.render(fourth_quarter.fourth_quarters(ticker))


# --- the two figures have to stand on one basis ------------------------------

# Carrier's fiscal 2022 revenue, taken from the committed companyfacts record:
# four rows under one tag, each with the accession that filed it and the date it
# was filed. Neither filing that moved the year is in this fixture set as a
# document -- the record is the source for them, and it is the source this
# module reads.
#
#   us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax [USD]
#     2022-01-01..2022-12-31  20,421,000,000  10-K 0001783180-23-000012  2023-02-07
#     2022-01-01..2022-12-31  20,421,000,000  10-K 0001783180-24-000009  2024-02-06
#     2022-01-01..2022-12-31  17,288,000,000   8-K 0001783180-25-000058  2025-07-29
#     2022-01-01..2022-09-30  15,316,000,000  10-Q 0001783180-23-000065  2023-10-26
#
# The year was re-presented at 17,288,000,000 once the discontinued businesses
# came out of it. The nine months has not been re-presented since October 2023,
# when the year on record was still 20,421,000,000. So the two subtractions a
# reader can actually write are
#
#     old basis   20,421,000,000 - 15,316,000,000 = 5,105,000,000
#     new basis   17,288,000,000 - (a nine months nobody has restated)
#
# and taking the latest of each gives 17,288,000,000 - 15,316,000,000 =
# 1,972,000,000, which is Carrier's fourth quarter on neither of them.
RECAST_APART_FROM_ITS_NINE_MONTHS = {
    "ticker": "CARR",
    "term": "revenue",
    "tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
    "fiscal_year_end": "2022-12-31",
    "year_as_first_filed": record_row(
        20_421_000_000, "0001783180-23-000012", "2022-01-01", "2022-12-31"),
    "year_the_recast_displaced": record_row(
        20_421_000_000, "0001783180-24-000009", "2022-01-01", "2022-12-31"),
    "year_as_it_now_stands": record_row(
        17_288_000_000, "0001783180-25-000058", "2022-01-01", "2022-12-31"),
    "nine_months": record_row(
        15_316_000_000, "0001783180-23-000065", "2022-01-01", "2022-09-30"),
    "on_the_old_basis": 5_105_000_000,
    "across_the_two": 1_972_000_000,
}

def test_the_rows_behind_carriers_recast_year_are_in_the_record():
    """The transcription above against companyfacts read straight, and both
    subtractions done here. The second is the one this module must not publish."""
    case = RECAST_APART_FROM_ITS_NINE_MONTHS
    figures = {side: value_on_record(case["ticker"], case["tag"], case[side])
               for side in ("year_as_first_filed", "year_the_recast_displaced",
                            "year_as_it_now_stands", "nine_months")}
    assert figures["year_as_first_filed"] - figures["nine_months"] \
        == case["on_the_old_basis"]
    assert figures["year_as_it_now_stands"] - figures["nine_months"] \
        == case["across_the_two"]


def test_a_year_restated_after_its_nine_months_was_last_stated_is_refused():
    """1,972,000,000 is not Carrier's fourth quarter of 2022 on any basis, so it
    is not published as one. The reason names both filings and what the later of
    them displaced, because the reader has to be able to see which two figures
    were not subtracted and why."""
    case = RECAST_APART_FROM_ITS_NINE_MONTHS
    cell = year_ending(case["ticker"],
                       case["fiscal_year_end"])["measures"][case["term"]]
    assert set(cell) == {"missing"}, \
        f"Carrier's 2022 revenue carries {sorted(set(cell) - {'missing'})}"
    reason = cell["missing"]
    assert "different reporting bases" in reason
    assert str(case["across_the_two"]) not in reason, \
        "the reason must not read as a fourth quarter"
    displaced = case["year_the_recast_displaced"]
    for side in ("year_the_recast_displaced", "year_as_it_now_stands",
                 "nine_months"):
        assert case[side]["accession"] in reason, \
            f"{side} ({case[side]['accession']}) is not named in: {reason}"
    assert str(displaced["value"]) in reason, \
        f"the year the recast displaced is not named in: {reason}"


# --- a fiscal year is one an income-statement tag reports --------------------

def test_a_mis_started_duration_under_another_tag_is_not_a_second_fiscal_year():
    """TTM Technologies' 2025 year runs 2024-12-31..2025-12-29. One
    us-gaap:LossOnContracts row starts it a day early, and that row is in the
    record -- checked here against companyfacts read straight. It is one fact's
    date, not a year the company closed, so it is not a fiscal year."""
    index = companyfacts_record("TTMI")["index"]
    mis_started = [key for key in index
                   if key[0] == "LossOnContracts"
                   and key[3:] == ("2024-12-30", "2025-12-29")]
    assert mis_started, \
        "TTM Technologies' record no longer holds the row this test is about"

    years = [year["fiscal_year"] for year in derived("TTMI")["fiscal_years"]]
    ending_then = [year for year in years if year["end"] == "2025-12-29"]
    assert len(ending_then) == 1, ending_then
    assert ending_then[0]["start"] == "2024-12-31"


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_company_reports_two_fiscal_years_ending_on_the_same_day(ticker):
    """A company closes one fiscal year on a given date. Two of them ending
    together is a duration read as a year that is not one."""
    ends = [year["fiscal_year"]["end"] for year in derived(ticker)["fiscal_years"]]
    assert len(ends) == len(set(ends)), f"{ticker}: {sorted(ends)}"



# --- planted documents, where the expected output is put there on purpose ----

YEAR = ("2025-01-01", "2025-12-31")
NINE_MONTHS_END = "2025-09-30"


def fact(start: str, end: str, value, *, accession="0000000000-00-000000",
         filed="2026-02-01") -> dict:
    return {"start": start, "end": end, "val": value, "accn": accession,
            "filed": filed}


def plant(tmp_path: Path, concepts: dict, *, filing_date="2026-02-01") -> Path:
    """A one-company fixture root whose companyfacts record is the rows given."""
    root = tmp_path / "fixtures"
    company = root / "ZZZZ"
    company.mkdir(parents=True)
    url = "https://example.invalid/companyfacts.json"
    document = {"ticker": "ZZZZ", "cik": "0000000000", "as_of": "2026-09-01",
                "url": url, "note": fetch_companyfacts.NOTE,
                "entity_name": "Planted", "facts": {"us-gaap": concepts}}
    raw = (json.dumps(document, indent=2) + "\n").encode("utf-8")
    (company / "companyfacts.json").write_bytes(raw)
    (company / "manifest.json").write_text(json.dumps({
        "ticker": "ZZZZ", "cik": "0000000000", "as_of": "2026-09-01",
        "documents": [{
            "form": fetch_companyfacts.FORM, "role": fetch_companyfacts.ROLE,
            "accession": "", "filing_date": filing_date, "report_date": "",
            "items": "", "date_basis": fetch_companyfacts.DATE_BASIS,
            "url": url, "path": "companyfacts.json", "stored": "identity",
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}]}) + "\n")
    return root


def revenue(*rows) -> dict:
    return {"RevenueFromContractWithCustomerExcludingAssessedTax":
            {"units": {"USD": list(rows)}}}


def only_year(root: Path, **kwargs) -> dict:
    payload = fourth_quarter.fourth_quarters("ZZZZ", fixtures_root=root, **kwargs)
    return payload["fiscal_years"][0]["measures"]["revenue"]


def test_a_figure_restated_after_the_other_was_last_stated_is_refused(tmp_path):
    """The control first: the same two filings, with the year never restated,
    derive. Then the fault, in each direction -- the year moving after the nine
    months was last stated, and the nine months moving after the year was."""
    steady = plant(tmp_path / "steady", revenue(
        fact(YEAR[0], NINE_MONTHS_END, 700, accession="0000000000-00-000001",
             filed="2025-11-01"),
        fact(YEAR[0], YEAR[1], 1000, accession="0000000000-00-000002",
             filed="2026-02-01")))
    assert only_year(steady)["fourth_quarter"] == 300

    year_moved = plant(tmp_path / "year", revenue(
        fact(YEAR[0], YEAR[1], 1200, accession="0000000000-00-000001",
             filed="2025-11-01"),
        fact(YEAR[0], NINE_MONTHS_END, 700, accession="0000000000-00-000002",
             filed="2025-11-01"),
        fact(YEAR[0], YEAR[1], 1000, accession="0000000000-00-000003",
             filed="2026-02-01")))
    cell = only_year(year_moved)
    assert set(cell) == {"missing"}
    assert "the annual figure was reported 2026-02-01" in cell["missing"]
    assert "over 1200 filed 2025-11-01" in cell["missing"]
    assert "300" not in cell["missing"], \
        "the reason must not read as a fourth quarter"

    nine_moved = plant(tmp_path / "nine", revenue(
        fact(YEAR[0], YEAR[1], 1000, accession="0000000000-00-000001",
             filed="2025-11-01"),
        fact(YEAR[0], NINE_MONTHS_END, 650, accession="0000000000-00-000002",
             filed="2025-11-01"),
        fact(YEAR[0], NINE_MONTHS_END, 700, accession="0000000000-00-000003",
             filed="2026-02-01")))
    cell = only_year(nine_moved)
    assert set(cell) == {"missing"}
    assert "the nine-month figure was reported 2026-02-01" in cell["missing"]
    assert "over 650 filed 2025-11-01" in cell["missing"]


def test_a_restatement_both_figures_were_re_presented_under_still_derives(tmp_path):
    """The rule is about one figure moving under the other, not about a
    restatement. Where the later filing restates both, the pair stands."""
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1200, accession="0000000000-00-000001",
             filed="2025-11-01"),
        fact(YEAR[0], NINE_MONTHS_END, 840, accession="0000000000-00-000001",
             filed="2025-11-01"),
        fact(YEAR[0], YEAR[1], 1000, accession="0000000000-00-000002",
             filed="2026-02-01"),
        fact(YEAR[0], NINE_MONTHS_END, 700, accession="0000000000-00-000002",
             filed="2026-02-01")))
    cell = only_year(root)
    assert cell["fourth_quarter"] == 300
    assert cell["annual_as_filed"]["superseded"] == [
        {"filed": "2025-11-01", "accession": "0000000000-00-000001", "value": 1200}]


def test_an_annual_duration_under_no_measured_tag_is_not_a_fiscal_year(tmp_path):
    """The control comes first: the tag reports an annual-length duration and
    no fiscal year comes back, because there is no measure to read one off it.
    Beside a real year it would otherwise be a second one, ending the same day."""
    alone = plant(tmp_path / "alone", {"LossOnContracts": {"units": {"USD": [
        fact(YEAR[0], YEAR[1], 40)]}}})
    payload = fourth_quarter.fourth_quarters("ZZZZ", fixtures_root=alone)
    assert payload["fiscal_years"] == []
    assert payload["fiscal_years_on_record"] == 0
    assert payload["source"]["duration_facts"] == 1

    beside = plant(tmp_path / "beside", dict(
        revenue(fact(YEAR[0], YEAR[1], 1000),
                fact(YEAR[0], NINE_MONTHS_END, 700)),
        LossOnContracts={"units": {"USD": [fact("2024-12-31", YEAR[1], 40)]}}))
    payload = fourth_quarter.fourth_quarters("ZZZZ", fixtures_root=beside)
    assert payload["fiscal_years_on_record"] == 1
    assert [year["fiscal_year"]["start"] for year in payload["fiscal_years"]] \
        == [YEAR[0]]


def test_a_year_with_no_nine_month_figure_is_absent_and_not_a_zero(tmp_path):
    """The control comes first: with both rows the same document derives."""
    both = plant(tmp_path / "both", revenue(
        fact(YEAR[0], YEAR[1], 1000), fact(YEAR[0], NINE_MONTHS_END, 700)))
    assert only_year(both)["fourth_quarter"] == 300

    alone = plant(tmp_path / "alone", revenue(fact(YEAR[0], YEAR[1], 1000)))
    cell = only_year(alone)
    assert set(cell) == {"missing"}
    assert "no nine-month year-to-date" in cell["missing"]
    assert "1000" not in cell["missing"], \
        "the reason must not read as a fourth quarter of the whole year"


def test_two_nine_month_periods_under_one_tag_are_refused(tmp_path):
    """Which of the two the year runs against is not this file's to decide."""
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1000),
        fact(YEAR[0], NINE_MONTHS_END, 700),
        fact(YEAR[0], "2025-09-29", 690)))
    cell = only_year(root)
    assert set(cell) == {"missing"}
    assert "2 nine-month year-to-date periods" in cell["missing"]
    assert "not a guess" in cell["missing"]


def test_one_filing_reporting_a_period_twice_is_refused(tmp_path):
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1000),
        fact(YEAR[0], YEAR[1], 1001, accession="0000000000-00-000001"),
        fact(YEAR[0], NINE_MONTHS_END, 700)))
    cell = only_year(root)
    assert set(cell) == {"missing"}
    assert "reports [1000, 1001]" in cell["missing"]


def test_the_later_filing_wins_and_says_what_it_displaced(tmp_path):
    """The later filing re-presents the nine months as well, at the figure it
    already carried. That is what keeps the pair on one basis while the year
    moves under it -- a year that moves alone is the case above."""
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1000, accession="0000000000-00-000001",
             filed="2026-02-01"),
        fact(YEAR[0], NINE_MONTHS_END, 700, accession="0000000000-00-000001",
             filed="2026-02-01"),
        fact(YEAR[0], YEAR[1], 900, accession="0000000000-00-000002",
             filed="2026-05-01"),
        fact(YEAR[0], NINE_MONTHS_END, 700, accession="0000000000-00-000002",
             filed="2026-05-01")))
    cell = only_year(root, cutoff="2026-05-01")
    assert cell["annual"] == 900
    assert cell["fourth_quarter"] == 200
    assert cell["annual_as_filed"]["filed"] == "2026-05-01"
    assert cell["annual_as_filed"]["superseded"] == [
        {"filed": "2026-02-01", "accession": "0000000000-00-000001", "value": 1000}]


def test_a_residual_that_is_not_a_quarter_is_refused(tmp_path):
    """Two periods can share a start, be a year and be three quarters long, and
    still leave something that is not a quarter between their ends."""
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1000), fact(YEAR[0], "2025-09-19", 700)))
    cell = only_year(root)
    assert set(cell) == {"missing"}
    assert "103 days, which is not a quarter" in cell["missing"]


def test_a_fact_filed_after_the_cutoff_stops_the_derivation(tmp_path):
    """The gate checks the date recorded for the document. This checks the rows,
    so a record whose manifest date understates what is inside it is refused."""
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1000),
        fact(YEAR[0], NINE_MONTHS_END, 700, filed="2026-03-01")))
    with pytest.raises(fourth_quarter.FourthQuarterError) as caught:
        fourth_quarter.fourth_quarters("ZZZZ", cutoff="2026-02-01",
                                       fixtures_root=root)
    assert "filed after the cutoff 2026-02-01" in str(caught.value)


def test_the_record_itself_is_refused_after_the_cutoff(tmp_path):
    root = plant(tmp_path, revenue(
        fact(YEAR[0], YEAR[1], 1000), fact(YEAR[0], NINE_MONTHS_END, 700)))
    with pytest.raises(cutoff_guard.CutoffViolationError):
        fourth_quarter.fourth_quarters("ZZZZ", cutoff="2026-01-31",
                                       fixtures_root=root)


def test_an_instant_is_not_a_period_to_subtract_from(tmp_path):
    """A balance at a date has no start, and there is no fourth quarter of one."""
    root = plant(tmp_path, {"Assets": {"units": {"USD": [
        {"end": YEAR[1], "val": 5000, "accn": "0000000000-00-000000",
         "filed": "2026-02-01"}]}}})
    payload = fourth_quarter.fourth_quarters("ZZZZ", fixtures_root=root)
    assert payload["fiscal_years"] == []
    assert payload["fiscal_years_on_record"] == 0
    assert payload["source"]["duration_facts"] == 0


# --- the command line --------------------------------------------------------

def test_the_command_line_writes_the_derivation(tmp_path, capsys):
    out = tmp_path / "fourth_quarter.json"
    assert fourth_quarter.main(["--ticker", "AAPL", "--out", str(out)]) == 0
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["ticker"] == "AAPL"
    assert written["fiscal_years"][0]["measures"]["revenue"]["fourth_quarter"] \
        == 102_466 * 1_000_000
    assert "fourth_quarter: AAPL" in capsys.readouterr().out


def test_a_company_with_no_record_is_refused_rather_than_defaulted(tmp_path, capsys):
    out = tmp_path / "fourth_quarter.json"
    assert fourth_quarter.main(["--ticker", "ZZZZ", "--out", str(out)]) \
        == fourth_quarter.BAD_INPUT
    assert not out.exists()
    assert "ZZZZ" in capsys.readouterr().err
