"""The pipeline's exchange calendar, worked by hand.

Every date asserted here was read off a printed calendar, not off the module:
Memorial Day is the last Monday of May; Good Friday is two days before Easter
Sunday; Juneteenth is the 19th of June, observed the Friday before when it
falls on a Saturday; New Year's Day on a Saturday is not observed on the
Friday; the exchange closed on 2025-01-09 for a national day of mourning;
Columbus Day is the second Monday of October, when EDGAR is closed and the
exchange is open.
"""

from __future__ import annotations

import datetime as dt

from src import exchange_calendar as calendar


def test_easter_2026_is_the_fifth_of_april_and_good_friday_the_third():
    assert calendar._easter(2026) == dt.date(2026, 4, 5)
    assert dt.date(2026, 4, 3) in calendar.exchange_holidays(2026)
    assert dt.date(2026, 4, 3) not in calendar.federal_holidays(2026)
    assert not calendar.is_trading_day(dt.date(2026, 4, 3))


def test_memorial_day_2026_is_monday_the_twenty_fifth_of_may():
    assert dt.date(2026, 5, 25) in calendar.exchange_holidays(2026)
    assert not calendar.is_trading_day(dt.date(2026, 5, 25))
    # Friday the 22nd, then Tuesday the 26th and Wednesday the 27th
    assert calendar.trading_days_from(dt.date(2026, 5, 22), 3) == [
        dt.date(2026, 5, 22), dt.date(2026, 5, 26), dt.date(2026, 5, 27)]


def test_juneteenth_2027_falls_on_a_saturday_and_is_observed_the_friday_before():
    assert dt.date(2027, 6, 19).weekday() == 5
    assert dt.date(2027, 6, 18) in calendar.exchange_holidays(2027)
    assert dt.date(2027, 6, 18) in calendar.federal_holidays(2027)


def test_new_years_day_2028_on_a_saturday_is_not_observed():
    assert dt.date(2028, 1, 1).weekday() == 5
    assert dt.date(2028, 1, 1) not in calendar.exchange_holidays(2028)
    assert dt.date(2027, 12, 31) not in calendar.exchange_holidays(2027)
    assert calendar.is_trading_day(dt.date(2027, 12, 31))


def test_the_day_of_mourning_in_january_2025_is_a_closure_listed_by_hand():
    assert dt.date(2025, 1, 9) in calendar.SPECIAL_CLOSURES
    assert not calendar.is_trading_day(dt.date(2025, 1, 9))
    assert calendar.is_trading_day(dt.date(2025, 1, 8))
    assert calendar.is_trading_day(dt.date(2025, 1, 10))


def test_columbus_day_2026_is_open_on_the_exchange_and_closed_at_edgar():
    assert calendar.is_trading_day(dt.date(2026, 10, 12))
    assert dt.date(2026, 10, 12) in calendar.federal_holidays(2026)
    assert calendar.next_business_day(dt.date(2026, 10, 9)) == dt.date(2026, 10, 13)
    # an ordinary Thursday: EDGAR's next business day is the Friday
    assert calendar.next_business_day(dt.date(2026, 5, 7)) == dt.date(2026, 5, 8)


def test_weekends_are_not_trading_days():
    assert not calendar.is_trading_day(dt.date(2026, 5, 9))     # Saturday
    assert not calendar.is_trading_day(dt.date(2026, 5, 10))    # Sunday
    assert calendar.trading_days_from(dt.date(2026, 5, 9), 1) == [dt.date(2026, 5, 11)]
