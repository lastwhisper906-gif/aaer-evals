"""The exchange calendar, by rule, and EDGAR's business days beside it.

A market table's rows are the days the price series had, and a check that read
them as the calendar the table is held to would be checking the table against
itself: a table missing a row would pass with its window one trading day late.
This module is the calendar that check is made against instead. The New York
Stock Exchange closes on weekends and on the holidays worked below; closures
outside the rules -- the national days of mourning -- are listed by hand in
`SPECIAL_CLOSURES`, and the owner extends that list. EDGAR's business days are
the federal holidays, which differ from the exchange's on three days a year:
the exchange closes on Good Friday and EDGAR does not, and EDGAR closes on
Columbus Day and Veterans Day and the exchange does not.

The owner's graders under `evals/` carry the same calendar and are independent
by design: the pipeline never imports `evals/`, so this copy is the pipeline's
own, and each is judged by its own hand-worked tests.
"""

from __future__ import annotations

import datetime as dt

# days the exchange closed outside its holiday rules: national days of mourning
SPECIAL_CLOSURES = frozenset({dt.date(2018, 12, 5), dt.date(2025, 1, 9)})


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    first = dt.date(year, month, 1)
    return first + dt.timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> dt.date:
    last = (dt.date(year, month, 28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return last - dt.timedelta(days=(last.weekday() - weekday) % 7)


def _easter(year: int) -> dt.date:
    """Gregorian Easter Sunday (the anonymous algorithm); 2026-04-05 by hand."""
    a, b, c = year % 19, year // 100, year % 100
    d, e, f = b // 4, b % 4, (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    ll = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ll) // 451
    month = (h + ll - 7 * m + 114) // 31
    day = (h + ll - 7 * m + 114) % 31 + 1
    return dt.date(year, month, day)


def _observed(day: dt.date) -> dt.date:
    """A fixed-date holiday on a Saturday is observed the Friday before, on a
    Sunday the Monday after."""
    if day.weekday() == 5:
        return day - dt.timedelta(days=1)
    if day.weekday() == 6:
        return day + dt.timedelta(days=1)
    return day


def _shared_holidays(year: int) -> set[dt.date]:
    out = set()
    new_year = dt.date(year, 1, 1)
    if new_year.weekday() == 6:
        out.add(new_year + dt.timedelta(days=1))
    elif new_year.weekday() < 5:
        out.add(new_year)      # on a Saturday it is not observed on the Friday
    out.add(_nth_weekday(year, 1, 0, 3))        # Martin Luther King Jr. Day
    out.add(_nth_weekday(year, 2, 0, 3))        # Presidents' Day
    out.add(_last_weekday(year, 5, 0))          # Memorial Day
    if year >= 2022:
        out.add(_observed(dt.date(year, 6, 19)))    # Juneteenth
    out.add(_observed(dt.date(year, 7, 4)))     # Independence Day
    out.add(_nth_weekday(year, 9, 0, 1))        # Labor Day
    out.add(_nth_weekday(year, 11, 3, 4))       # Thanksgiving
    out.add(_observed(dt.date(year, 12, 25)))   # Christmas
    return out


def exchange_holidays(year: int) -> set[dt.date]:
    return _shared_holidays(year) | {_easter(year) - dt.timedelta(days=2)}   # Good Friday


def federal_holidays(year: int) -> set[dt.date]:
    return _shared_holidays(year) | {_nth_weekday(year, 10, 0, 2),          # Columbus Day
                                     _observed(dt.date(year, 11, 11))}      # Veterans Day


def is_trading_day(day: dt.date) -> bool:
    return day.weekday() < 5 and day not in exchange_holidays(day.year) \
        and day not in SPECIAL_CLOSURES


def trading_days_from(day: dt.date, count: int) -> list[dt.date]:
    """The first `count` trading days on or after `day`."""
    out = []
    while len(out) < count:
        if is_trading_day(day):
            out.append(day)
        day += dt.timedelta(days=1)
    return out


def next_business_day(day: dt.date) -> dt.date:
    """EDGAR's next business day after `day`: not a weekend, not a federal holiday."""
    day += dt.timedelta(days=1)
    while day.weekday() >= 5 or day in federal_holidays(day.year):
        day += dt.timedelta(days=1)
    return day
