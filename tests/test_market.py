"""The market table, held to arithmetic done by hand on the frozen fixture.

Every number asserted here was computed from `tests/fixtures/market/` before
`src/market.py` was run, and the arithmetic is written out term by term so a
reader can follow it without running anything. That is the point: an expected
value comes from the source, never from the first run of the code it judges, and
the source here is the fixture, whose construction
`tests/fixtures/market/fixture_manifest.json` states and whose shape the first
tests below recount independently.

Every price in the fixture is a power of two times a power of five over a power
of ten, so every ratio between two of them is a terminating decimal. The returns
are therefore exact rather than rounded, which is what lets an assertion be an
equality instead of a tolerance.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path

import pytest

from src import market

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "market"
PRICES = FIXTURES / "prices"
SHORT_INTEREST = FIXTURES / "short_interest"

TICKER = "ZZZZ"
SIC = "3661"                      # telephone and telegraph apparatus: division D
SHARES_OUTSTANDING = 1_000_000_000

FILING_DATE = dt.date(2026, 5, 8)          # a Friday
AFTER_THE_CLOSE = "2026-05-08T16:30:00"
BEFORE_THE_CLOSE = "2026-05-08T15:30:00"
EARNINGS_RELEASE_FILED = dt.date(2026, 4, 24)
EARNINGS_RELEASE_ACCEPTED = "2026-04-24T16:05:00"

# --- one instant, written two ways ---------------------------------------------
#
# Daylight saving ran from 2026-03-08 to 2026-11-01, so on 2026-05-08 New York
# was four hours behind universal time: 19:00:00+00:00 is 15:00:00 there, an hour
# before the 16:00 close. The stamp with no zone is that same wall clock, which
# is how EDGAR writes acceptance.
BEFORE_THE_CLOSE_IN_NEW_YORK = "2026-05-08T15:00:00"
BEFORE_THE_CLOSE_IN_UNIVERSAL_TIME = "2026-05-08T19:00:00+00:00"
ON_THE_EXCHANGE_CLOCK = "2026-05-08T15:00:00-04:00"
# 20:00:00+00:00 is 16:00:00 in New York, which is at the close and not before
# it; a second earlier is before it. Converted they straddle the close, and
# dropped they would both sit four hours past it.
AT_THE_CLOSE_IN_UNIVERSAL_TIME = "2026-05-08T20:00:00+00:00"
A_SECOND_BEFORE_THE_CLOSE_IN_UNIVERSAL_TIME = "2026-05-08T19:59:59+00:00"

# --- EDGAR's own close, which is not the exchange's ----------------------------
#
# A submission accepted after half past five in the evening, Eastern, is deemed
# filed on the next business day. 2026-05-08 is a Friday, so that day is Monday.
AFTER_EDGARS_CLOSE = "2026-05-08T17:45:00"
NEXT_BUSINESS_DAY = dt.date(2026, 5, 11)

# --- the returns the fixture is built from, as decimals that terminate ---------
#
# The broad market alternates between 400.00 and 409.60:
#   409.60 / 400.00 - 1 = +0.024
#   400.00 / 409.60 - 1 = -0.0234375
# The stock alternates between 100.00 and 104.8576, in phase with it:
#   104.8576 / 100.00 - 1 = +0.048576
#   100.00 / 104.8576 - 1 = -0.04632568359375
MARKET_UP = Decimal("0.024")
MARKET_DOWN = Decimal("-0.0234375")
STOCK_UP = Decimal("0.048576")
STOCK_DOWN = Decimal("-0.04632568359375")

# beta is the covariance of the two series over the variance of the market. With
# two return values repeating in phase, every up day sits (up - mean) above its
# own mean and every down day the same distance below, so both sums carry the
# same count and the count cancels:
#
#   covariance = (up_stock - down_stock)(up_market - down_market) / 4
#   variance   = (up_market - down_market)^2 / 4
#   beta       = (up_stock - down_stock) / (up_market - down_market)
#              = (0.048576 + 0.04632568359375) / (0.024 + 0.0234375)
#              = 0.09490168359375 / 0.0474375
#              = 2.0005625
BETA = 2.0005625

ESTIMATION_WINDOW_FIRST = dt.date(2025, 5, 23)
ESTIMATION_WINDOW_LAST = dt.date(2026, 5, 7)

# --- the reaction days, written out term by term -------------------------------
#
# 2026-05-11  raw +0.024      market +0.024      sector  0
#             0.024 - 2.0005625 * 0.024 - 0 = 0.024 - 0.0480135 = -0.0240135
# 2026-05-12  raw  0          market -0.0234375  sector +0.024
#             0 + 2.0005625 * 0.0234375 - 0.024
#               = 0.0468881835937500 - 0.024 = 0.0228881835937500
# 2026-05-13  raw +0.048576   market  0          sector -0.0234375
#             0.048576 - 0 + 0.0234375 = 0.0720135
FILING_WINDOW_ABNORMAL = {
    dt.date(2026, 5, 11): -0.0240135,
    dt.date(2026, 5, 12): 0.02288818359375,
    dt.date(2026, 5, 13): 0.0720135,
}
# -0.0240135 + 0.0228881835937500 + 0.0720135
FILING_WINDOW = 0.07088818359375

# The filing day itself, which an after-close acceptance leaves outside the window:
#   0.024 - 2.0005625 * 0.024 - 0.024 = -0.0480135
FILING_DAY_ABNORMAL = -0.0480135
# Before the close the window is 05-08, 05-11, 05-12:
#   -0.0480135 - 0.0240135 + 0.0228881835937500 = -0.0491388164062500
FILING_WINDOW_BEFORE_THE_CLOSE = -0.04913881640625

# The earnings-release window sits inside the estimation window, where every day
# is one of the two patterns:
#   a down day: -0.04632568359375 + 2.0005625 * 0.0234375 + 0.0234375 = +0.024
#   an up day:  +0.048576 - 2.0005625 * 0.024 - 0.024 = -0.0234375
EARNINGS_WINDOW_ABNORMAL = {
    dt.date(2026, 4, 27): 0.024,
    dt.date(2026, 4, 28): -0.0234375,
    dt.date(2026, 4, 29): 0.024,
}
# 0.024 - 0.0234375 + 0.024
EARNINGS_WINDOW = 0.0245625

# --- short interest, by hand ---------------------------------------------------
#
# Thirteen reports settle inside the two years before the reaction days and are
# published in time to be seen. Their shares short over 1,000,000,000 shares:
#
#   2024-06-14  11,000,000  0.011      2025-08-15  23,000,000  0.023
#   2024-08-15  15,000,000  0.015      2025-10-15  14,000,000  0.014
#   2024-10-15   9,000,000  0.009      2025-12-15  19,000,000  0.019
#   2024-12-13  21,000,000  0.021      2026-02-13  16,000,000  0.016
#   2025-02-14  13,000,000  0.013      2026-03-31  12,000,000  0.012
#   2025-04-15  17,000,000  0.017      2026-04-21  28,000,000  0.028
#   2025-06-13  10,000,000  0.010
#
# In order: 0.009 0.010 0.011 0.012 0.013 0.014 [0.015] 0.016 0.017 0.019 0.021
#           0.023 0.028
# Thirteen values, so the median is the seventh: 0.015.
TWO_YEAR_MEDIAN = 0.015
# Before 2026-04-21's report is published the window holds twelve of them, and
# the median is the mean of the sixth and seventh: (0.014 + 0.015) / 2 = 0.0145.
MEDIAN_BEFORE_THE_LAST_REPORT = 0.0145

LAST_SETTLEMENT = dt.date(2026, 4, 21)
# 2026-04-21 is a Tuesday. Eight business days: 22 23 24 | 27 28 29 30 | 05-01.
LAST_PUBLICATION = dt.date(2026, 5, 1)
LAST_RATIO = 0.028
PREVIOUS_RATIO = 0.012            # the report settled 2026-03-31, published 2026-04-10

# Settled two trading days before the cutoff and published eight business days
# after that, which is well past it. Attaching it by settlement date would put
# 0.050 on the last rows of the table.
UNPUBLISHED_SETTLEMENT = dt.date(2026, 5, 11)
UNPUBLISHED_RATIO = 0.050
# Older than two years on every row of the table. Counting it would make the
# median of the thirteen a median of fourteen: (0.014 + 0.015) / 2 = 0.0145.
OUT_OF_WINDOW_RATIO = 0.002

ROW_COLUMNS = {"ticker", "date", "raw_return", "market_return", "sector_return",
               "beta", "abnormal_return", "window", "reaction_window",
               "short_interest_ratio", "short_interest_two_year_median",
               "short_interest_above_median"}


# --- reading the fixture without going through the module under test ----------

def closes(symbol: str) -> list[tuple[dt.date, Decimal]]:
    """The adjusted closes of one series, read here rather than by `src/market.py`."""
    text = (PRICES / f"{symbol}.csv").read_text(encoding="utf-8")
    return [(dt.date.fromisoformat(row["date"]), Decimal(row["adjusted_close"]))
            for row in csv.DictReader(text.splitlines())]


def exact_returns(symbol: str) -> dict[dt.date, Decimal]:
    bars = closes(symbol)
    return {day: close / before - 1
            for (_, before), (day, close) in zip(bars, bars[1:])}


@pytest.fixture(scope="module")
def prices():
    return market.read_prices(PRICES)


@pytest.fixture(scope="module")
def calendar(prices):
    return market.trading_calendar(prices, "SPY")


@pytest.fixture(scope="module")
def reports():
    return market.read_short_interest(SHORT_INTEREST, TICKER)


def build(accepted: str = AFTER_THE_CLOSE, *, filing_date: dt.date = FILING_DATE,
          earnings_release: bool = True, prices_directory=PRICES) -> dict:
    windows = [{"kind": "filing", "filing_date": filing_date.isoformat(),
                "accepted": accepted}]
    if earnings_release:
        windows.append({"kind": "earnings_release",
                        "filing_date": EARNINGS_RELEASE_FILED.isoformat(),
                        "accepted": EARNINGS_RELEASE_ACCEPTED})
    return market.market_table(
        ticker=TICKER, sic=SIC, shares_outstanding=SHARES_OUTSTANDING,
        prices=market.read_prices(prices_directory),
        short_interest=market.read_short_interest(SHORT_INTEREST, TICKER),
        windows=windows)


@pytest.fixture(scope="module")
def table():
    return build()


def row_on(table: dict, day: dt.date) -> dict:
    found = [row for row in table["rows"] if row["date"] == day.isoformat()]
    assert len(found) == 1, f"{day} is on {len(found)} rows"
    return found[0]


def window_of(table: dict, kind: str) -> dict:
    return next(window for window in table["windows"] if window["kind"] == kind)


# --- the fixture is what it says it is ----------------------------------------

def test_every_fixture_file_is_the_bytes_the_manifest_recorded():
    """The fixture is the answer key, so a silent edit to it moves every expectation."""
    recorded = json.loads((FIXTURES / "fixture_manifest.json").read_text(encoding="utf-8"))
    listed = {entry["path"] for entry in recorded["files"]}
    on_disk = {str(path.relative_to(FIXTURES)) for path in FIXTURES.rglob("*.csv")}
    assert on_disk == listed
    for entry in recorded["files"]:
        data = (FIXTURES / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"], f"{entry['path']}: length changed"
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], \
            f"{entry['path']}: content changed"


def test_the_estimation_window_holds_the_two_returns_and_nothing_else():
    """Recounted from the file, because beta's hand computation rests on it.

    250 trading days, 125 of each return in each series, the stock's up days the
    market's up days. Every other number in this file follows from that.
    """
    stock, broad = exact_returns(TICKER), exact_returns("SPY")
    window = [day for day in sorted(broad)
              if ESTIMATION_WINDOW_FIRST <= day <= ESTIMATION_WINDOW_LAST]
    assert len(window) == 250
    assert Counter(broad[day] for day in window) == {MARKET_UP: 125, MARKET_DOWN: 125}
    assert Counter(stock[day] for day in window) == {STOCK_UP: 125, STOCK_DOWN: 125}
    assert all((stock[day] == STOCK_UP) == (broad[day] == MARKET_UP) for day in window)


def test_the_days_before_the_estimation_window_move_the_other_way():
    """What makes the window's first day worth asserting: one day earlier is different."""
    stock, broad = exact_returns(TICKER), exact_returns("SPY")
    before = [day for day in sorted(broad) if day < ESTIMATION_WINDOW_FIRST]
    assert before[0] == dt.date(2025, 5, 12) and before[-1] == dt.date(2025, 5, 22)
    assert all((stock[day] == MARKET_UP) == (broad[day] == MARKET_DOWN)
               for day in before)


def test_the_split_is_in_the_close_column_and_not_in_the_adjusted_close(prices):
    """A module reading the close column would see a halving that never happened."""
    text = (PRICES / f"{TICKER}.csv").read_text(encoding="utf-8")
    rows = {row["date"]: row for row in csv.DictReader(text.splitlines())}
    assert rows["2025-11-04"]["close"] == "200.00"
    assert rows["2025-11-04"]["adjusted_close"] == "100.00"
    assert rows["2025-11-05"]["close"] == rows["2025-11-05"]["adjusted_close"]
    on_the_split_day = dict(prices[TICKER])[dt.date(2025, 11, 5)]
    assert on_the_split_day == pytest.approx(104.8576)


# --- beta ----------------------------------------------------------------------

def test_beta_is_the_stocks_spread_over_the_markets(prices, calendar):
    """(0.048576 + 0.04632568359375) / (0.024 + 0.0234375) = 2.0005625."""
    spread_of_the_stock = float(STOCK_UP - STOCK_DOWN)
    spread_of_the_market = float(MARKET_UP - MARKET_DOWN)
    assert spread_of_the_stock == pytest.approx(0.09490168359375)
    assert spread_of_the_market == pytest.approx(0.0474375)
    assert spread_of_the_stock / spread_of_the_market == pytest.approx(BETA)

    window = market.estimation_window(calendar, FILING_DATE)
    computed = market.beta(market.daily_returns(prices[TICKER]),
                           market.daily_returns(prices["SPY"]), window)
    assert computed == pytest.approx(BETA)


def test_the_estimation_window_is_the_250_days_before_the_filing_date(calendar):
    window = market.estimation_window(calendar, FILING_DATE)
    assert len(window) == 250
    assert window[0] == ESTIMATION_WINDOW_FIRST
    assert window[-1] == ESTIMATION_WINDOW_LAST
    assert FILING_DATE not in window


def test_one_day_more_of_estimation_window_is_a_different_beta(prices, calendar):
    """The window's edge is load-bearing, so it is asserted rather than assumed."""
    stock = market.daily_returns(prices[TICKER])
    broad = market.daily_returns(prices["SPY"])
    longer = market.estimation_window(calendar, FILING_DATE, days=251)
    assert longer[0] == dt.date(2025, 5, 22)
    assert market.beta(stock, broad, longer) != pytest.approx(BETA)


def test_the_table_carries_one_beta_and_puts_it_on_every_row(table):
    assert table["beta"] == pytest.approx(BETA)
    assert table["beta_estimation_window"] == {
        "trading_days": 250, "first": ESTIMATION_WINDOW_FIRST.isoformat(),
        "last": ESTIMATION_WINDOW_LAST.isoformat()}
    assert {row["beta"] for row in table["rows"]} == {table["beta"]}


# --- the abnormal return, term by term -----------------------------------------

def test_the_abnormal_return_is_raw_less_beta_times_market_less_sector(table):
    """Each day of the filing window leaves a different term doing the work."""
    day_zero = row_on(table, dt.date(2026, 5, 11))
    assert day_zero["raw_return"] == pytest.approx(0.024)
    assert day_zero["market_return"] == pytest.approx(0.024)
    assert day_zero["sector_return"] == pytest.approx(0.0)
    assert day_zero["abnormal_return"] == pytest.approx(0.024 - 0.0480135 - 0.0)

    day_one = row_on(table, dt.date(2026, 5, 12))
    assert day_one["raw_return"] == pytest.approx(0.0)
    assert day_one["market_return"] == pytest.approx(-0.0234375)
    assert day_one["sector_return"] == pytest.approx(0.024)
    assert day_one["abnormal_return"] == pytest.approx(0.0 + 0.04688818359375 - 0.024)

    day_two = row_on(table, dt.date(2026, 5, 13))
    assert day_two["raw_return"] == pytest.approx(0.048576)
    assert day_two["market_return"] == pytest.approx(0.0)
    assert day_two["sector_return"] == pytest.approx(-0.0234375)
    assert day_two["abnormal_return"] == pytest.approx(0.048576 - 0.0 + 0.0234375)

    for day, expected in FILING_WINDOW_ABNORMAL.items():
        assert row_on(table, day)["abnormal_return"] == pytest.approx(expected)


def test_the_reaction_window_is_the_sum_of_its_three_abnormal_returns(table):
    assert sum(FILING_WINDOW_ABNORMAL.values()) == pytest.approx(FILING_WINDOW)
    assert window_of(table, "filing")["reaction_window"] == pytest.approx(FILING_WINDOW)
    for day in FILING_WINDOW_ABNORMAL:
        assert row_on(table, day)["reaction_window"] == pytest.approx(FILING_WINDOW)


def test_a_row_carries_the_columns_the_spec_names(table):
    for row in table["rows"]:
        assert set(row) == ROW_COLUMNS


# --- reaction day zero, and everything that counts from it ---------------------

def test_an_after_close_acceptance_moves_day_zero_to_the_next_trading_day(table, calendar):
    """The window, the cutoff and the outcome window all move with day zero.

    All three are asserted because this project has already shifted one window's
    start without its end and pushed that end onto the first day of the outcome
    window.
    """
    window = window_of(table, "filing")
    assert window["day_zero"] == "2026-05-11", "the Friday filing reacts on the Monday"

    # one: still three trading days, and they are consecutive ones.
    assert window["days"] == ["2026-05-11", "2026-05-12", "2026-05-13"]
    assert len(window["days"]) == market.REACTION_WINDOW_TRADING_DAYS

    # two: the cutoff moved with it, and nothing later is in the table.
    assert table["cutoff"] == "2026-05-13"
    assert max(row["date"] for row in table["rows"]) == "2026-05-13"

    # three: the window still ends before the outcome window opens.
    opens = market.outcome_window_opens(calendar, dt.date(2026, 5, 11))
    assert opens == dt.date(2026, 5, 14)
    assert dt.date.fromisoformat(window["days"][-1]) < opens


def test_a_before_close_acceptance_leaves_day_zero_on_the_filing_date(calendar):
    """The same three bounds, one trading day earlier, and still in that order."""
    table = build(BEFORE_THE_CLOSE)
    window = window_of(table, "filing")
    assert window["day_zero"] == FILING_DATE.isoformat()
    assert window["days"] == ["2026-05-08", "2026-05-11", "2026-05-12"]
    assert table["cutoff"] == "2026-05-12"
    assert max(row["date"] for row in table["rows"]) == "2026-05-12"
    opens = market.outcome_window_opens(calendar, FILING_DATE)
    assert opens == dt.date(2026, 5, 13)
    assert dt.date.fromisoformat(window["days"][-1]) < opens
    assert window["reaction_window"] == pytest.approx(FILING_WINDOW_BEFORE_THE_CLOSE)


def test_the_filing_day_is_outside_the_window_an_after_close_acceptance_made(table):
    """It is a row like any other, and it is not in the sum."""
    filing_day = row_on(table, FILING_DATE)
    assert filing_day["abnormal_return"] == pytest.approx(FILING_DAY_ABNORMAL)
    assert filing_day["window"] is None
    assert filing_day["reaction_window"] is None


def test_an_acceptance_at_the_close_exactly_is_not_before_it(calendar):
    assert market.reaction_day_zero("2026-05-08T16:00:00", calendar) == dt.date(2026, 5, 11)
    assert market.reaction_day_zero("2026-05-08T15:59:59", calendar) == FILING_DATE


def test_an_acceptance_with_no_time_of_day_is_refused(calendar):
    with pytest.raises(market.MarketError):
        market.reaction_day_zero("2026-05-08", calendar)


def test_nothing_after_reaction_day_two_reaches_the_table(table):
    """The fixture holds 2026-05-14 onwards. The cutoff is why the table does not."""
    later = [day for day, _ in closes("SPY") if day > dt.date(2026, 5, 13)]
    assert later == [dt.date(2026, 5, 14), dt.date(2026, 5, 15), dt.date(2026, 5, 18)]
    assert not [row for row in table["rows"] if row["date"] > table["cutoff"]]


def test_the_outcome_window_is_a_function_here_and_a_word_the_table_never_uses(
        table, calendar, tmp_path):
    """The module knows when the scoring window opens and still does not write it.

    The silence is asserted with the positive control beside it: the same call
    that would have produced the date works, and `reaction_window` is in the file
    to show that a window word does reach it.
    """
    assert market.outcome_window_opens(calendar, dt.date(2026, 5, 11)) == dt.date(2026, 5, 14)
    written = market.write_table(table, tmp_path / "input_market.json")
    text = written.read_text(encoding="utf-8")
    assert "reaction_window" in text
    assert "outcome" not in text
    assert "2026-05-14" not in text


def test_the_outcome_window_refuses_a_series_that_stops_inside_it(calendar):
    """The scorer reads it after the horizon expires, and this fixture is before that."""
    with pytest.raises(market.MarketError):
        market.outcome_window(calendar, dt.date(2026, 5, 11))


def test_a_window_whose_third_day_has_not_traded_is_refused(tmp_path):
    """The read stage waits until reaction day two has closed."""
    after_day_one = ("2026-05-13", "2026-05-14", "2026-05-15", "2026-05-18")
    short = tmp_path / "prices"
    short.mkdir()
    for symbol in (TICKER, "SPY", "XLI"):
        lines = (PRICES / f"{symbol}.csv").read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if not line.startswith(after_day_one)]
        assert len(kept) == len(lines) - len(after_day_one)
        (short / f"{symbol}.csv").write_text("\n".join(kept) + "\n", encoding="utf-8")
    with pytest.raises(market.MarketError, match="reaction day two"):
        build(prices_directory=short)


# --- one instant, one reaction day zero, however it is written -----------------

def test_the_same_instant_written_with_and_without_a_zone_gives_one_day_zero(
        calendar, tmp_path):
    """15:00 in New York and 19:00 in universal time are one moment on 2026-05-08.

    Read against a New York close, the second one's own wall clock says 19:00 and
    moves day zero to the Monday, which carries the cutoff to 2026-05-13 -- one
    trading day past reaction day two of the day the market actually reacted, and
    a row of the table. So the stamp is converted before it is compared, and the
    two writings are asserted equal to each other and to the day worked out here.
    """
    on_the_exchange_clock = build(BEFORE_THE_CLOSE_IN_NEW_YORK)
    in_universal_time = build(BEFORE_THE_CLOSE_IN_UNIVERSAL_TIME)
    assert on_the_exchange_clock == in_universal_time, \
        "one instant written two ways, so it is one table"

    for table in (on_the_exchange_clock, in_universal_time):
        window = window_of(table, "filing")
        assert window["accepted"] == ON_THE_EXCHANGE_CLOCK
        # 15:00 is an hour before the 16:00 close, so day zero is the Friday.
        assert window["day_zero"] == FILING_DATE.isoformat()
        assert window["days"] == ["2026-05-08", "2026-05-11", "2026-05-12"]
        assert table["cutoff"] == "2026-05-12"
        assert window["reaction_window"] == pytest.approx(FILING_WINDOW_BEFORE_THE_CLOSE)
        opens = market.outcome_window_opens(calendar, FILING_DATE)
        assert opens == dt.date(2026, 5, 13)
        assert dt.date.fromisoformat(window["days"][-1]) < opens

    written = market.write_table(in_universal_time, tmp_path / "input_market.json")
    text = written.read_text(encoding="utf-8")
    on_file = json.loads(text)
    assert not [row for row in on_file["rows"] if row["date"] > on_file["cutoff"]]
    for day in ("2026-05-13", "2026-05-14", "2026-05-15", "2026-05-18"):
        assert day not in text


def test_a_zone_offset_is_converted_and_not_dropped(calendar):
    """The control on the test above: an offset that really does land at the close.

    Dropped, 20:00:00+00:00 would read as eight in the evening and
    19:59:59+00:00 as a second before it -- both long past the close, both moving
    day zero. Converted, the two straddle the close by one second and only one
    of them moves.
    """
    assert market.reaction_day_zero(AT_THE_CLOSE_IN_UNIVERSAL_TIME, calendar) == \
        dt.date(2026, 5, 11)
    assert market.reaction_day_zero(
        A_SECOND_BEFORE_THE_CLOSE_IN_UNIVERSAL_TIME, calendar) == FILING_DATE
    assert window_of(build(AT_THE_CLOSE_IN_UNIVERSAL_TIME), "filing")["accepted"] == \
        "2026-05-08T16:00:00-04:00"


def test_the_universal_time_letter_is_refused_rather_than_read_as_one_zone(calendar):
    """EDGAR writes Eastern and appends the letter, so the letter cannot be read.

    The two readings of that stamp are four hours and one trading day apart:
    EDGAR means half past four in New York, which is after the close, and the
    standard means half past noon there, which is before it. The module picks
    neither. The same zone written out as an offset says one thing only, and the
    two assertions below are what it says and what EDGAR would have meant.
    """
    for letter in ("2026-05-08T16:30:00Z", "2026-05-08T16:30:00z"):
        with pytest.raises(market.MarketError, match="universal-time letter"):
            market.reaction_day_zero(letter, calendar)
    assert market.reaction_day_zero("2026-05-08T16:30:00+00:00", calendar) == FILING_DATE
    assert market.reaction_day_zero(AFTER_THE_CLOSE, calendar) == dt.date(2026, 5, 11)


# --- EDGAR's own close, and the filing date it moves ---------------------------

def test_the_filing_dates_one_acceptance_instant_permits():
    """Half past five in the evening, on the same clock the exchange close is told by."""
    assert market.EDGAR_ACCEPTANCE_CLOSE == dt.time(17, 30)
    assert market.filing_dates_for("2026-05-08T17:29:59") == (FILING_DATE,)
    assert market.filing_dates_for("2026-05-08T17:30:00") == \
        (FILING_DATE, NEXT_BUSINESS_DAY)
    assert market.business_days_after(FILING_DATE, 1) == NEXT_BUSINESS_DAY
    # 21:30:00+00:00 is half past five in New York: one rule, one clock.
    assert market.filing_dates_for("2026-05-08T21:30:00+00:00") == \
        (FILING_DATE, NEXT_BUSINESS_DAY)


def test_a_filing_accepted_after_edgars_close_is_filed_the_next_business_day(
        calendar, tmp_path):
    """The legitimate case in which the acceptance day and the filing date differ.

    Accepted at 17:45 on the Friday, dated the Monday by EDGAR, and reacting on
    the Monday: day zero is the next trading day after the acceptance day, so the
    cutoff and the outcome window move with it and the window still ends before
    the outcome window opens.
    """
    table = build(AFTER_EDGARS_CLOSE, filing_date=NEXT_BUSINESS_DAY)
    window = window_of(table, "filing")
    assert window["filing_date"] == "2026-05-11"
    assert window["accepted"] == "2026-05-08T17:45:00-04:00", \
        "the acceptance day and the filing date disagree, and both are kept"
    assert window["day_zero"] == "2026-05-11"
    assert window["days"] == ["2026-05-11", "2026-05-12", "2026-05-13"]
    assert table["cutoff"] == "2026-05-13"
    opens = market.outcome_window_opens(calendar, NEXT_BUSINESS_DAY)
    assert opens == dt.date(2026, 5, 14)
    assert dt.date.fromisoformat(window["days"][-1]) < opens

    # Beta is measured over the 250 trading days before the filing date, so the
    # moved filing date moves that window one trading day at each end. Read off
    # the fixture rather than off the module: the last 250 days before 05-11 run
    # from 2025-05-26 to 2026-05-08. They still end before day zero, so the days
    # beta is measured over still touch neither the reaction window nor the
    # filing date. Beta itself is a different number over that window and no hand
    # value was worked out for it, so it is not asserted here.
    before_the_filing_date = [day for day, _ in closes("SPY") if day < NEXT_BUSINESS_DAY]
    assert before_the_filing_date[-250] == dt.date(2025, 5, 26)
    assert before_the_filing_date[-1] == FILING_DATE
    assert table["beta_estimation_window"] == {
        "trading_days": 250, "first": "2025-05-26", "last": "2026-05-08"}
    assert dt.date.fromisoformat(table["beta_estimation_window"]["last"]) < \
        dt.date.fromisoformat(window["day_zero"])

    written = market.write_table(table, tmp_path / "input_market.json")
    text = written.read_text(encoding="utf-8")
    on_file = json.loads(text)
    assert not [row for row in on_file["rows"] if row["date"] > on_file["cutoff"]]
    for day in ("2026-05-14", "2026-05-15", "2026-05-18"):
        assert day not in text


def test_a_filing_date_that_is_neither_permitted_day_is_refused(prices, reports):
    """Two more directions, on top of the impossible one further down this file.

    Two business days on from an after-hours acceptance is not a date EDGAR could
    have written; and neither is the next business day when the acceptance was
    before EDGAR's close -- 16:30 is past the exchange's close, which moves day
    zero, and short of EDGAR's, which does not move the filing date.
    """
    for filing_date, accepted in ((dt.date(2026, 5, 12), AFTER_EDGARS_CLOSE),
                                  (NEXT_BUSINESS_DAY, AFTER_THE_CLOSE)):
        with pytest.raises(market.MarketError, match="dates the filing"):
            market.market_table(
                ticker=TICKER, sic=SIC, shares_outstanding=SHARES_OUTSTANDING,
                prices=prices, short_interest=reports,
                windows=[{"kind": "filing", "filing_date": filing_date.isoformat(),
                          "accepted": accepted}])


# --- two windows, kept apart ---------------------------------------------------

def test_the_two_windows_are_recorded_separately_and_never_added(table):
    kinds = [window["kind"] for window in table["windows"]]
    assert kinds == ["earnings_release", "filing"]
    assert window_of(table, "earnings_release")["reaction_window"] == \
        pytest.approx(EARNINGS_WINDOW)
    assert window_of(table, "filing")["reaction_window"] == pytest.approx(FILING_WINDOW)
    for day, expected in EARNINGS_WINDOW_ABNORMAL.items():
        row = row_on(table, day)
        assert row["abnormal_return"] == pytest.approx(expected)
        assert row["window"] == "earnings_release"
    assert not [row for row in table["rows"]
                if row["reaction_window"] == pytest.approx(EARNINGS_WINDOW + FILING_WINDOW)]


def test_two_windows_that_share_a_trading_day_are_refused():
    """One day in two windows is the shape that lets them be added together."""
    with pytest.raises(market.MarketError):
        market.market_table(
            ticker=TICKER, sic=SIC, shares_outstanding=SHARES_OUTSTANDING,
            prices=market.read_prices(PRICES),
            short_interest=market.read_short_interest(SHORT_INTEREST, TICKER),
            windows=[{"kind": "filing", "filing_date": "2026-05-08",
                      "accepted": AFTER_THE_CLOSE},
                     {"kind": "earnings_release", "filing_date": "2026-05-11",
                      "accepted": "2026-05-11T09:00:00"}])


# --- short interest ------------------------------------------------------------

def test_the_publication_date_is_eight_business_days_after_settlement():
    """2026-04-21 is a Tuesday: 22 23 24, then 27 28 29 30, then 05-01."""
    assert market.publication_date(LAST_SETTLEMENT) == LAST_PUBLICATION
    assert market.SHORT_INTEREST_PUBLICATION_BUSINESS_DAYS == 8
    assert market.business_days_after(dt.date(2026, 4, 21), 8) == dt.date(2026, 5, 1)


def test_a_report_attaches_on_its_publication_date_and_not_on_its_settlement_date(table):
    """Both directions on one report: the settlement is 2026-04-21, the publication
    2026-05-01, and four trading days of the table lie between them."""
    for day in (dt.date(2026, 4, 27), dt.date(2026, 4, 28),
                dt.date(2026, 4, 29), dt.date(2026, 4, 30)):
        assert day > LAST_SETTLEMENT and day < LAST_PUBLICATION
        row = row_on(table, day)
        assert row["short_interest_ratio"] == pytest.approx(PREVIOUS_RATIO), \
            "attached by settlement date, which is a number the market did not have"
    for day in (dt.date(2026, 5, 1), dt.date(2026, 5, 13)):
        assert row_on(table, day)["short_interest_ratio"] == pytest.approx(LAST_RATIO)


def test_a_report_settled_before_the_cutoff_and_published_after_it_never_attaches(
        table, reports):
    """The same rule at the cutoff, where the look-ahead would be worth the most."""
    settled = [report for report in reports
               if report["settlement"] == UNPUBLISHED_SETTLEMENT]
    assert len(settled) == 1
    assert settled[0]["shares_short"] == UNPUBLISHED_RATIO * SHARES_OUTSTANDING
    assert settled[0]["publication"] > dt.date.fromisoformat(table["cutoff"])
    assert not [row for row in table["rows"]
                if row["short_interest_ratio"] == pytest.approx(UNPUBLISHED_RATIO)]


def test_the_two_year_median_is_the_seventh_of_the_thirteen_reports_in_the_window(
        table, reports):
    """0.009 0.010 0.011 0.012 0.013 0.014 [0.015] 0.016 0.017 0.019 0.021 0.023 0.028."""
    day = dt.date(2026, 5, 13)
    in_the_window = [report for report in reports
                     if report["publication"] <= day
                     and report["settlement"] >= market.years_before(day, 2)]
    assert len(in_the_window) == 13, "the count the median is the middle of"
    row = row_on(table, day)
    assert row["short_interest_two_year_median"] == pytest.approx(TWO_YEAR_MEDIAN)
    assert row["short_interest_ratio"] == pytest.approx(LAST_RATIO)
    assert row["short_interest_above_median"] is True


def test_a_report_older_than_two_years_is_not_in_the_median(table, reports):
    """Counting it would make the median of thirteen a median of fourteen, 0.0145."""
    oldest = min(reports, key=lambda report: report["settlement"])
    assert oldest["settlement"] == dt.date(2024, 4, 15)
    assert oldest["shares_short"] == OUT_OF_WINDOW_RATIO * SHARES_OUTSTANDING
    day = dt.date(2026, 5, 13)
    assert oldest["settlement"] < market.years_before(day, 2)
    assert row_on(table, day)["short_interest_two_year_median"] == \
        pytest.approx(TWO_YEAR_MEDIAN)
    assert row_on(table, day)["short_interest_two_year_median"] != \
        pytest.approx(MEDIAN_BEFORE_THE_LAST_REPORT)


def test_the_above_median_flag_is_the_ratio_against_that_median(table):
    """Both answers appear in this table, which is what says the flag is computed."""
    before = row_on(table, dt.date(2026, 4, 27))
    assert before["short_interest_ratio"] == pytest.approx(PREVIOUS_RATIO)
    assert before["short_interest_two_year_median"] == \
        pytest.approx(MEDIAN_BEFORE_THE_LAST_REPORT)
    assert before["short_interest_above_median"] is False

    after = row_on(table, dt.date(2026, 5, 1))
    assert after["short_interest_ratio"] == pytest.approx(LAST_RATIO)
    assert after["short_interest_two_year_median"] == pytest.approx(TWO_YEAR_MEDIAN)
    assert after["short_interest_above_median"] is True


def test_the_columns_are_found_by_name_and_both_date_shapes_are_read(reports):
    """One fixture file has its columns in another order and its date run together."""
    oldest = min(reports, key=lambda report: report["settlement"])
    assert oldest["file"] == "shrt20240415.csv"
    assert oldest["settlement"] == dt.date(2024, 4, 15)
    lines = (SHORT_INTEREST / "shrt20240415.csv").read_text(encoding="utf-8").splitlines()
    assert lines[0].split("|")[:3] == ["settlementDate", "symbolCode",
                                       "currentShortPositionQuantity"]
    assert lines[1].split("|")[0] == "20240415", "the date is run together"
    every_other_file = (SHORT_INTEREST / "shrt20260421.csv").read_text(encoding="utf-8")
    assert every_other_file.splitlines()[0].split("|")[0] == "accountingYearMonthNumber"
    assert every_other_file.splitlines()[1].split("|")[-1] == "2026-04-21"


def test_another_companys_row_is_not_this_companys_short_interest(reports):
    """The files carry two other symbols; an inexact match would take one of them."""
    text = (SHORT_INTEREST / "shrt20260421.csv").read_text(encoding="utf-8")
    assert "YYYY" in text and "XXXX" in text
    assert {report["shares_short"] for report in reports} \
        .isdisjoint({7_000_000, 33_000_000})
    assert market.read_short_interest(SHORT_INTEREST, "YYYY")[0]["shares_short"] \
        == 7_000_000


def test_a_company_with_no_published_report_gets_no_ratio_and_no_flag(tmp_path):
    empty = tmp_path / "short_interest"
    empty.mkdir()
    columns = market.short_interest_on([], dt.date(2026, 5, 13), SHARES_OUTSTANDING)
    assert columns == {"short_interest_ratio": None,
                       "short_interest_two_year_median": None,
                       "short_interest_above_median": None}
    assert market.read_short_interest(empty, TICKER) == []


# --- the map from SIC code to sector series ------------------------------------

def test_the_map_ships_with_the_module_as_data():
    assert market.MAP_PATH.name == "sic_to_sector_etf_map_v0.1.json"
    assert market.MAP_PATH.is_file()
    assert market.sector_map()["rules_version"] == market.RULES_VERSION


def test_every_division_carries_one_series_and_its_boundaries_map_to_it():
    divisions = market.sector_map()["divisions"]
    assert [division["division"] for division in divisions] == list("ABCDEFGHIJK")
    for division in divisions:
        for edge in (division["first_sic"], division["last_sic"]):
            assert market.sector_symbol(edge) == division["sector_etf"]
    assert market.broad_market_symbol() == "SPY"


def test_the_twelve_companies_land_in_manufacturing_under_one_series():
    """The coarseness the needs-judgment item is about, asserted rather than implied."""
    assert market.sector_symbol(SIC) == "XLI"
    assert market.division_of(SIC)["division"] == "D"
    for code in ("2000", "3571", "3674", "3999"):
        assert market.sector_symbol(code) == "XLI"


def test_a_code_in_an_unassigned_range_is_refused():
    """1800 to 1999 is in no division; a neighbour is not an answer."""
    for code in ("1800", "1999", "6800", "9050", "9800"):
        with pytest.raises(market.MarketError):
            market.sector_symbol(code)


def test_a_company_whose_series_is_not_in_the_price_data_is_refused(tmp_path):
    one = tmp_path / "prices"
    one.mkdir()
    for symbol in (TICKER, "SPY"):
        (one / f"{symbol}.csv").write_text(
            (PRICES / f"{symbol}.csv").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(market.MarketError):
        build(prices_directory=one)


# --- fail closed on what the source served -------------------------------------

def test_a_price_file_with_no_adjusted_close_column_is_refused(tmp_path):
    folder = tmp_path / "prices"
    folder.mkdir()
    (folder / "SPY.csv").write_text("date,open,close\n2026-05-08,400.00,409.60\n",
                                    encoding="utf-8")
    with pytest.raises(market.MarketError):
        market.read_prices(folder)


def test_a_date_beside_something_that_is_not_a_number_is_not_a_price(tmp_path):
    folder = tmp_path / "prices"
    folder.mkdir()
    (folder / "SPY.csv").write_text(
        "date,open,close,adjusted_close\n2026-05-08,400.00,409.60,unavailable\n",
        encoding="utf-8")
    with pytest.raises(market.MarketError):
        market.read_prices(folder)


def test_a_row_with_no_real_date_is_not_a_price(tmp_path):
    folder = tmp_path / "prices"
    folder.mkdir()
    (folder / "SPY.csv").write_text(
        "date,open,close,adjusted_close\nlast Friday,400.00,409.60,409.60\n",
        encoding="utf-8")
    with pytest.raises(market.MarketError):
        market.read_prices(folder)


def test_a_run_with_no_window_is_refused(prices, reports):
    with pytest.raises(market.MarketError):
        market.market_table(ticker=TICKER, sic=SIC,
                            shares_outstanding=SHARES_OUTSTANDING, prices=prices,
                            short_interest=reports, windows=[])


def test_a_window_kind_the_spec_does_not_name_is_refused(prices, reports):
    with pytest.raises(market.MarketError):
        market.market_table(ticker=TICKER, sic=SIC,
                            shares_outstanding=SHARES_OUTSTANDING, prices=prices,
                            short_interest=reports,
                            windows=[{"kind": "press_release",
                                      "filing_date": FILING_DATE.isoformat(),
                                      "accepted": AFTER_THE_CLOSE}])


def test_an_acceptance_that_disagrees_with_the_filing_date_is_refused(prices, reports):
    with pytest.raises(market.MarketError):
        market.market_table(ticker=TICKER, sic=SIC,
                            shares_outstanding=SHARES_OUTSTANDING, prices=prices,
                            short_interest=reports,
                            windows=[{"kind": "filing", "filing_date": "2026-05-07",
                                      "accepted": AFTER_THE_CLOSE}])


# --- end to end ----------------------------------------------------------------

def test_the_command_line_writes_input_market_json(tmp_path, capsys):
    out = tmp_path / "runs" / TICKER / "input_market.json"
    code = market.main([
        "--ticker", TICKER, "--sic", SIC,
        "--shares-outstanding", str(SHARES_OUTSTANDING),
        "--prices", str(PRICES), "--short-interest", str(SHORT_INTEREST),
        "--window", f"filing:{FILING_DATE.isoformat()}:{AFTER_THE_CLOSE}",
        "--window", (f"earnings_release:{EARNINGS_RELEASE_FILED.isoformat()}:"
                     f"{EARNINGS_RELEASE_ACCEPTED}"),
        "--out", str(out)])
    assert code == 0
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["ticker"] == TICKER
    assert written["cutoff"] == "2026-05-13"
    assert written["beta"] == pytest.approx(BETA)
    assert len(written["rows"]) == 13
    assert window_of(written, "filing")["reaction_window"] == pytest.approx(FILING_WINDOW)
    assert "2026-05-13" in capsys.readouterr().out


def test_the_command_line_says_what_it_could_not_do(tmp_path, capsys):
    code = market.main([
        "--ticker", TICKER, "--sic", "1900",
        "--shares-outstanding", str(SHARES_OUTSTANDING),
        "--prices", str(PRICES), "--short-interest", str(SHORT_INTEREST),
        "--window", f"filing:{FILING_DATE.isoformat()}:{AFTER_THE_CLOSE}",
        "--out", str(tmp_path / "input_market.json")])
    assert code == market.BAD_INPUT
    assert "divisions" in capsys.readouterr().err
