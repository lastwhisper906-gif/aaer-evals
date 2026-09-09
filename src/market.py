"""The market table: one row per company per trading day, and one origin for it.

`docs/INPUT_SPEC.md` section 4 names the columns -- raw return, market return,
sector return, beta, abnormal return, the reaction window, the short-interest
ratio, its two-year median and the above-median flag -- and says who reads them:
the comparers, and nothing else. Not a reader, not the supervisor, not the
scorer's input to any agent. Python does every one of these numbers, because the
comparer that reads them does no arithmetic and a rule it cannot evaluate from
its input is a rule it evaluates by guessing.

Reaction day zero is the origin
-------------------------------

`docs/INPUT_SPEC.md` puts it plainly: reaction day zero is the filing date when
EDGAR accepted the filing before the close, and the next trading day when it
accepted after the close, and **every market bound counts from it**. This
project has already made the other choice once and written the cost down: the
reaction window was measured from the filing date while an after-close
acceptance moved its start, which pushed its end onto the first day of the
60-trading-day outcome window, so the cutoff and the score were reading the same
day. So there is one origin here. The reaction window is day zero through day
two, the cutoff is day two, and the outcome window opens on day three -- all
three move together, because all three are counted from the same day.

The estimation window for beta is the one bound that is not counted from day
zero, because section 4 does not count it from there: beta is measured "over the
250 trading days before the filing date". Those 250 days end before the filing
date, so they never touch the reaction window under either acceptance time, and
an after-close acceptance leaves the filing date itself in neither.

The outcome window is a function here and is never written into the table. The
scorer reads it after the horizon expires; a layer that could read it would be
reading its own answer.

Why the date gate is not on this path
-------------------------------------

`src/cutoff_guard.py` gates a *document* by the filing date recorded for it in a
fixture manifest. Market data is not a document and has no filing date: section
1 bounds it separately and section 4 says the bound is reaction day two, which
is a bound on rows. So this module reads its price and short-interest files
directly, from a directory the caller names, and the bound lives where the
look-ahead lives -- in `market_table`, which drops every trading day after the
cutoff and has no argument that turns that off. Nothing here opens a fixture or
a run bundle, and nothing here is a second route into one.

The price source
----------------

Unchosen, and on the needs-judgment list: session 1 found Stooq answering a
scripted request with a proof-of-work page and the Yahoo endpoint refusing an
unauthenticated caller, so whether a candidate serves a delisted ticker is still
unanswered. Nothing here chooses one. The reader below takes the columns
`docs/INPUT_SPEC.md` says are fetched -- open, close, and the split- and
dividend-adjusted close -- and every return is computed from the adjusted close,
so a file that carries no `adjusted_close` column is refused rather than read
through the unadjusted one.

Short interest
--------------

FINRA's twice-monthly file, attached by **publication date** -- settlement plus
about eight business days -- and never by settlement date, because attaching it
by settlement would hand an agent a number the market did not have. The file
carries no publication column, so the date is computed: eight business days
after settlement, counting Monday to Friday. That count is FINRA's own unit and
not the trading calendar, which is why it is weekday arithmetic and not a walk
along the price series. A holiday inside the count would put the real
publication a day later than this computes, and this module carries no holiday
calendar; the limit is named rather than hidden, the fixture the tests run
against has no holidays so the count is exact there, and the day a real calendar
arrives it belongs in one place and this is it.

The denominator is `dei:EntityCommonStockSharesOutstanding` from companyfacts,
supplied by the caller as one figure. A figure per settlement date would be the
faithful version and needs a reader for the companyfacts catalogue, which does
not exist yet; opening that route is its own item.

    python3.12 -m src.market --ticker ZZZZ --sic 3661 \\
        --shares-outstanding 1000000000 --prices <dir> --short-interest <dir> \\
        --window filing:2026-05-08:2026-05-08T16:30:00 \\
        --window earnings_release:2026-04-24:2026-04-24T16:05:00 \\
        --out input_market.json
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import functools
import json
import math
import statistics
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/market.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

BAD_INPUT = 2

RULES_VERSION = "v0.1"
MAP_PATH = Path(__file__).resolve().parent / f"sic_to_sector_etf_map_{RULES_VERSION}.json"

# New York close. A filing accepted at 16:00:00 exactly was not accepted before
# the close, so it moves to the next trading day: at the close is not before it.
MARKET_CLOSE = dt.time(16, 0)

BETA_TRADING_DAYS = 250
# Day zero, day one, day two. `docs/INPUT_SPEC.md`: "An agent may see market data
# through reaction day two."
REACTION_WINDOW_TRADING_DAYS = 3
# Opens on reaction day three and is never visible to any layer.
OUTCOME_WINDOW_TRADING_DAYS = 60
SHORT_INTEREST_PUBLICATION_BUSINESS_DAYS = 8
SHORT_INTEREST_MEDIAN_YEARS = 2

WINDOW_KINDS = ("earnings_release", "filing")

PRICE_COLUMNS = ("date", "adjusted_close")
SHORT_INTEREST_COLUMNS = ("symbolCode", "currentShortPositionQuantity", "settlementDate")


class MarketError(Exception):
    """The table could not be computed from what was given. Always fail-closed."""


# --- the map from SIC code to sector series ---------------------------------

@functools.lru_cache(maxsize=None)
def sector_map(path=MAP_PATH) -> dict:
    """The versioned map, as data. Never inferred, never written from here."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def broad_market_symbol(*, path=MAP_PATH) -> str:
    """The broad-market series every abnormal return is measured against."""
    return sector_map(path)["broad_market_series"]["symbol"]


def division_of(sic, *, path=MAP_PATH) -> dict:
    """The division one SIC code falls in, so a caller can say why as well as what.

    A code in one of the classification's unassigned ranges is refused by name.
    Mapping it to a neighbouring division would be this module inventing a
    sector for a company nobody classified.
    """
    try:
        code = int(str(sic).strip())
    except ValueError as exc:
        raise MarketError(f"sic={sic!r} is not a SIC code") from exc
    for division in sector_map(path)["divisions"]:
        if int(division["first_sic"]) <= code <= int(division["last_sic"]):
            return division
    raise MarketError(
        f"SIC {code:04d} falls in none of the classification's divisions -- refused "
        f"rather than mapped to a neighbour")


def sector_symbol(sic, *, path=MAP_PATH) -> str:
    """The sector series one company's abnormal return is measured against."""
    return division_of(sic, path=path)["sector_etf"]


# --- reading what the market served -----------------------------------------

def _finite(value: str, field: str, where: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise MarketError(f"{where}: {field}={value!r} is not a number") from exc
    if not math.isfinite(number):
        raise MarketError(f"{where}: {field}={value!r} is not a finite number")
    return number


def _iso_date(value: str, field: str, where: str) -> dt.date:
    """A calendar date, written either 2026-05-08 or 20260508."""
    text = (value or "").strip()
    for shape in ("%Y-%m-%d", "%Y%m%d"):
        try:
            return dt.datetime.strptime(text, shape).date()
        except ValueError:
            continue
    raise MarketError(f"{where}: {field}={value!r} is not a date")


def read_prices(directory) -> dict[str, list[tuple[dt.date, float]]]:
    """One daily series per `.csv` in a directory, named by the file, oldest first.

    Every row has to be a real calendar date beside a finite adjusted close: a
    row that is a date beside anything else -- a blank, an error string -- is not
    a price, and counting it as one is how a source's error payload becomes
    history.
    """
    folder = Path(directory)
    if not folder.is_dir():
        raise MarketError(f"{folder} is not a directory of price series")
    series: dict[str, list[tuple[dt.date, float]]] = {}
    for path in sorted(folder.glob("*.csv")):
        reader = csv.DictReader(path.read_text(encoding="utf-8").splitlines())
        missing = [name for name in PRICE_COLUMNS if name not in (reader.fieldnames or ())]
        if missing:
            raise MarketError(
                f"{path.name} has no {', '.join(missing)} column -- refused, because "
                f"every return here is computed from the split- and "
                f"dividend-adjusted close")
        bars = [(_iso_date(row["date"], "date", path.name),
                 _finite(row["adjusted_close"], "adjusted_close", path.name))
                for row in reader]
        days = [day for day, _ in bars]
        if len(set(days)) != len(days):
            raise MarketError(f"{path.name} has a day on two rows, so its return is "
                              f"whichever row sorted first")
        series[path.stem] = sorted(bars)
    if not series:
        raise MarketError(f"{folder} holds no price series")
    return series


def read_short_interest(directory, symbol: str) -> list[dict]:
    """One company's rows from FINRA's twice-monthly files, oldest settlement first.

    Columns are found by their names in the header, never by position: the
    header is what the file states and the order has moved between vintages. The
    symbol has to match exactly -- a fuzzy match would attribute another
    company's short position to this one.
    """
    folder = Path(directory)
    if not folder.is_dir():
        raise MarketError(f"{folder} is not a directory of short-interest files")
    found = []
    for path in sorted(folder.glob("shrt*.csv")):
        reader = csv.DictReader(path.read_text(encoding="utf-8").splitlines(),
                                delimiter="|")
        missing = [name for name in SHORT_INTEREST_COLUMNS
                   if name not in (reader.fieldnames or ())]
        if missing:
            raise MarketError(f"{path.name} has no {', '.join(missing)} column")
        for row in reader:
            if row["symbolCode"].strip() != symbol:
                continue
            settlement = _iso_date(row["settlementDate"], "settlementDate", path.name)
            found.append({
                "settlement": settlement,
                "publication": publication_date(settlement),
                "shares_short": _finite(row["currentShortPositionQuantity"],
                                        "currentShortPositionQuantity", path.name),
                "file": path.name,
            })
    return sorted(found, key=lambda report: report["settlement"])


# --- the calendar and the one origin ----------------------------------------

def trading_calendar(prices: dict[str, list[tuple[dt.date, float]]],
                     symbol: str) -> list[dt.date]:
    """The trading days, which are the days the broad-market series has a close for."""
    if symbol not in prices:
        raise MarketError(f"no series named {symbol} -- there is no calendar without it")
    return [day for day, _ in prices[symbol]]


def _on_or_after(calendar: list[dt.date], day: dt.date) -> dt.date:
    for candidate in calendar:
        if candidate >= day:
            return candidate
    raise MarketError(f"the price series ends before {day}")


def _index(calendar: list[dt.date], day: dt.date) -> int:
    try:
        return calendar.index(day)
    except ValueError as exc:
        raise MarketError(f"{day} is not a trading day in this series") from exc


def next_trading_day(calendar: list[dt.date], day: dt.date) -> dt.date:
    """The first trading day strictly after `day`."""
    for candidate in calendar:
        if candidate > day:
            return candidate
    raise MarketError(f"the price series ends on or before {day}")


def trading_days_from(calendar: list[dt.date], day: dt.date, count: int) -> list[dt.date]:
    """`count` trading days starting at `day`, which has to be one."""
    start = _index(calendar, day)
    days = calendar[start:start + count]
    if len(days) < count:
        raise MarketError(
            f"the price series holds {len(days)} trading days from {day}, not {count}")
    return days


def reaction_day_zero(accepted, calendar: list[dt.date]) -> dt.date:
    """The filing date when EDGAR accepted before the close, else the next trading day.

    A date with no time of day is refused. "Before the close" is a claim about
    the acceptance *time*, and a filing whose time nobody recorded cannot make it.
    """
    when = accepted if isinstance(accepted, dt.datetime) else _acceptance(accepted)
    filed = when.date()
    if when.time() < MARKET_CLOSE:
        return _on_or_after(calendar, filed)
    return next_trading_day(calendar, filed)


def _acceptance(value) -> dt.datetime:
    """An acceptance timestamp, refusing a date with no time of day.

    `datetime.fromisoformat` reads a bare date as midnight, which is before the
    close, so a filing whose acceptance time nobody recorded would silently take
    the earlier day zero and carry the cutoff back with it.
    """
    text = str(value).strip()
    _, separator, time_of_day = text.partition("T")
    if not separator:
        _, separator, time_of_day = text.partition(" ")
    if not separator or not time_of_day.strip():
        raise MarketError(
            f"accepted={value!r} carries no time of day -- a date alone cannot say "
            f"whether the filing arrived before the close")
    try:
        return dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise MarketError(f"accepted={value!r} is not an acceptance timestamp") from exc


def reaction_window(calendar: list[dt.date], day_zero: dt.date) -> list[dt.date]:
    """Day zero through day two: the days an agent may see."""
    try:
        return trading_days_from(calendar, day_zero, REACTION_WINDOW_TRADING_DAYS)
    except MarketError as exc:
        raise MarketError(
            f"{exc} -- the read stage waits until reaction day two has closed, because "
            f"a truncated window makes not_priced mean the market has not finished") \
            from exc


def outcome_window_opens(calendar: list[dt.date], day_zero: dt.date) -> dt.date:
    """Reaction day three. Never written into the table.

    It is here so that the one origin is visible in one file: the reaction
    window ends on day two and the outcome window begins on day three, whatever
    the acceptance time did to day zero.
    """
    start = _index(calendar, day_zero) + REACTION_WINDOW_TRADING_DAYS
    if start >= len(calendar):
        raise MarketError(f"the price series ends before reaction day three of {day_zero}")
    return calendar[start]


def outcome_window(calendar: list[dt.date], day_zero: dt.date) -> list[dt.date]:
    """The 60 trading days from reaction day three, for the scorer alone.

    It refuses a series that does not reach the end of the horizon rather than
    returning a short window, because a truncated outcome window scores a
    prediction against a market that has not finished answering it.
    """
    return trading_days_from(calendar, outcome_window_opens(calendar, day_zero),
                             OUTCOME_WINDOW_TRADING_DAYS)


# --- returns, beta, abnormal return -----------------------------------------

def daily_returns(bars: list[tuple[dt.date, float]]) -> dict[dt.date, float]:
    """Close over prior close, minus one. The first day has no return and no row."""
    returns = {}
    for (_, before), (day, close) in zip(bars, bars[1:]):
        if before == 0:
            raise MarketError(f"{day}: the prior close is zero, so there is no return")
        returns[day] = close / before - 1
    return returns


def estimation_window(calendar: list[dt.date], filing_date: dt.date,
                      *, days: int = BETA_TRADING_DAYS) -> list[dt.date]:
    """The `days` trading days before the filing date, the filing date excluded."""
    before = [day for day in calendar if day < filing_date]
    if len(before) < days:
        raise MarketError(
            f"{len(before)} trading days before {filing_date}, and beta needs {days}")
    return before[-days:]


def beta(stock: dict[dt.date, float], market: dict[dt.date, float],
         window: list[dt.date]) -> float:
    """Covariance of the two return series over the window, over the market's variance."""
    try:
        xs = [market[day] for day in window]
        ys = [stock[day] for day in window]
    except KeyError as exc:
        raise MarketError(f"no return for {exc.args[0]} -- beta needs every day of "
                          f"its window") from exc
    spread = statistics.variance(xs)
    if spread == 0:
        raise MarketError("the market did not move over the estimation window, so "
                          "beta is not defined")
    return statistics.covariance(xs, ys) / spread


def abnormal_return(raw: float, market: float, sector: float, slope: float) -> float:
    """raw - beta * market - sector, the form `docs/INPUT_SPEC.md` section 4 states."""
    return raw - slope * market - sector


# --- short interest ----------------------------------------------------------

def business_days_after(day: dt.date, count: int) -> dt.date:
    """`count` weekdays after `day`. FINRA counts business days, not trading days."""
    found = day
    while count:
        found += dt.timedelta(days=1)
        if found.weekday() < 5:
            count -= 1
    return found


def publication_date(settlement: dt.date) -> dt.date:
    """When the market had the number: settlement plus eight business days."""
    return business_days_after(settlement, SHORT_INTEREST_PUBLICATION_BUSINESS_DAYS)


def years_before(day: dt.date, years: int) -> dt.date:
    """The same calendar day `years` earlier; the 29th of February becomes the 28th."""
    try:
        return day.replace(year=day.year - years)
    except ValueError:
        return day.replace(year=day.year - years, day=28)


def short_interest_on(reports: list[dict], day: dt.date, shares_outstanding: float) -> dict:
    """The three short-interest columns for one trading day.

    A report enters on its publication date, so a report settled before this day
    and published after it is not here -- that number is one the market did not
    have. The median is over every report in the trailing two years that this
    day could see, the attached one included: the column says what the ratio is
    against its own recent history, and dropping the newest reading from that
    history would be a choice `docs/INPUT_SPEC.md` does not make. The flag is
    strict, because the crowded-signal rule reads "already above its own two-year
    median" and a ratio equal to the median is not above it.
    """
    if shares_outstanding <= 0:
        raise MarketError(f"shares_outstanding={shares_outstanding!r} is not a denominator")
    published = [report for report in reports if report["publication"] <= day]
    if not published:
        return {"short_interest_ratio": None,
                "short_interest_two_year_median": None,
                "short_interest_above_median": None}
    ratio = published[-1]["shares_short"] / shares_outstanding
    floor = years_before(day, SHORT_INTEREST_MEDIAN_YEARS)
    trailing = [report["shares_short"] / shares_outstanding
                for report in published if report["settlement"] >= floor]
    median = statistics.median(trailing)
    return {"short_interest_ratio": ratio,
            "short_interest_two_year_median": median,
            "short_interest_above_median": ratio > median}


# --- the table ---------------------------------------------------------------

@dataclasses.dataclass
class Window:
    """One recorded window: which filing, when it was accepted, and its three days."""

    kind: str
    filing_date: dt.date
    accepted: dt.datetime
    day_zero: dt.date
    days: list[dt.date]
    reaction_window: float | None = None

    def recorded(self) -> dict:
        return {"kind": self.kind, "filing_date": self.filing_date.isoformat(),
                "accepted": self.accepted.isoformat(),
                "day_zero": self.day_zero.isoformat(),
                "days": [day.isoformat() for day in self.days],
                "reaction_window": self.reaction_window}


def window_from(kind: str, filing_date, accepted, calendar: list[dt.date]) -> Window:
    """One window, with day zero decided by the acceptance time and nothing else."""
    if kind not in WINDOW_KINDS:
        raise MarketError(f"{kind!r} is not a window kind: {', '.join(WINDOW_KINDS)}")
    filed = filing_date if isinstance(filing_date, dt.date) else _iso_date(
        filing_date, "filing_date", kind)
    when = accepted if isinstance(accepted, dt.datetime) else _acceptance(accepted)
    if when.date() != filed:
        raise MarketError(
            f"{kind}: accepted {when.date()} and filed {filed} -- the acceptance "
            f"timestamp is what dates the filing")
    day_zero = reaction_day_zero(when, calendar)
    return Window(kind, filed, when, day_zero, reaction_window(calendar, day_zero))


def market_table(*, ticker: str, sic, shares_outstanding: float,
                 prices: dict[str, list[tuple[dt.date, float]]],
                 short_interest: list[dict], windows: list[dict],
                 map_path=MAP_PATH) -> dict:
    """One row per trading day the run may see, and the two windows, kept apart.

    The rows run from the earliest reaction day zero through the cutoff, which is
    reaction day two of the latest window. Nothing after the cutoff is in the
    table: that is the whole of the market bound, and there is no argument that
    lifts it.
    """
    if not windows:
        raise MarketError("a run records at least one window")
    market_symbol = broad_market_symbol(path=map_path)
    sector = sector_symbol(sic, path=map_path)
    for symbol in (ticker, market_symbol, sector):
        if symbol not in prices:
            raise MarketError(f"no price series for {symbol}")
    calendar = trading_calendar(prices, market_symbol)

    recorded = sorted((window_from(w["kind"], w["filing_date"], w["accepted"], calendar)
                       for w in windows), key=lambda window: window.day_zero)
    seen: dict[dt.date, str] = {}
    for window in recorded:
        for day in window.days:
            if day in seen:
                raise MarketError(
                    f"the {seen[day]} window and the {window.kind} window share "
                    f"{day} -- two windows are recorded separately and never added")
            seen[day] = window.kind

    trigger = max(recorded, key=lambda window: (window.filing_date, window.day_zero))
    window_of_beta = estimation_window(calendar, trigger.filing_date)

    raw = daily_returns(prices[ticker])
    market = daily_returns(prices[market_symbol])
    sector_returns = daily_returns(prices[sector])
    slope = beta(raw, market, window_of_beta)

    first = min(window.days[0] for window in recorded)
    cutoff = max(window.days[-1] for window in recorded)
    rows = {}
    for day in [d for d in calendar if first <= d <= cutoff]:
        for name, series in (("raw", raw), ("market", market), ("sector", sector_returns)):
            if day not in series:
                raise MarketError(f"{day}: no {name} return, so the row cannot be computed")
        window = seen.get(day)
        row = {
            "ticker": ticker,
            "date": day.isoformat(),
            "raw_return": raw[day],
            "market_return": market[day],
            "sector_return": sector_returns[day],
            "beta": slope,
            "abnormal_return": abnormal_return(raw[day], market[day],
                                               sector_returns[day], slope),
            "window": window,
            "reaction_window": None,
        }
        row.update(short_interest_on(short_interest, day, shares_outstanding))
        rows[day] = row

    for window in recorded:
        window.reaction_window = sum(rows[day]["abnormal_return"] for day in window.days)
        for day in window.days:
            rows[day]["reaction_window"] = window.reaction_window

    return {
        "ticker": ticker,
        "rules_version": RULES_VERSION,
        "sic": str(sic),
        "sector_series": sector,
        "broad_market_series": market_symbol,
        "shares_outstanding": shares_outstanding,
        "beta": slope,
        "beta_estimation_window": {
            "trading_days": len(window_of_beta),
            "first": window_of_beta[0].isoformat(),
            "last": window_of_beta[-1].isoformat(),
        },
        "cutoff": cutoff.isoformat(),
        "windows": [window.recorded() for window in recorded],
        "rows": list(rows.values()),
    }


def write_table(table: dict, path) -> Path:
    """The table as `input_market.json`, unrounded.

    Rounding would make a window sum disagree with the rows it is the sum of,
    and a comparer that does no arithmetic has no way to tell which is right.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")
    return target


# --- the command line -------------------------------------------------------

def _window_argument(text: str) -> dict:
    parts = text.split(":", 2)
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            f"{text!r} is not kind:filing_date:accepted, for example "
            f"filing:2026-05-08:2026-05-08T16:30:00")
    return {"kind": parts[0], "filing_date": parts[1], "accepted": parts[2]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--sic", required=True)
    parser.add_argument("--shares-outstanding", required=True, type=float,
                        help="dei:EntityCommonStockSharesOutstanding, from companyfacts")
    parser.add_argument("--prices", required=True, help="a directory of daily series")
    parser.add_argument("--short-interest", required=True,
                        help="a directory of FINRA's twice-monthly files")
    parser.add_argument("--window", required=True, action="append",
                        type=_window_argument, dest="windows",
                        help="kind:filing_date:accepted, once per recorded window")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        table = market_table(
            ticker=args.ticker, sic=args.sic,
            shares_outstanding=args.shares_outstanding,
            prices=read_prices(args.prices),
            short_interest=read_short_interest(args.short_interest, args.ticker),
            windows=args.windows)
        written = write_table(table, args.out)
    except MarketError as exc:
        print(f"market: {exc}", file=sys.stderr)
        return BAD_INPUT

    print(f"{args.ticker}: {len(table['rows'])} trading days through {table['cutoff']}, "
          f"beta {table['beta']:.6f} against {table['broad_market_series']} and "
          f"{table['sector_series']} -> {written}")
    for window in table["windows"]:
        print(f"  {window['kind']}: day zero {window['day_zero']}, "
              f"reaction window {window['reaction_window']:+.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
