"""One price frame, three sources that do not agree on anything else.

The pattern study and the forward track need different things from a price
source and there is no one source that gives both. The study is drawn from a
past date and is full of companies that stopped trading, so it needs the
delisting return, which is the thing a free API does not carry: a request for a
delisted ticker succeeds, the rows are simply not there, and a study of
accounting failures quietly becomes a study of the survivors. The forward track
is twelve companies that are all listed today, so it needs none of that and
needs a token that takes two minutes to get.

So: **CRSP through WRDS for the study, Tiingo for the forward track, EODHD for
one paid month if the WRDS account is refused.** `docs/needs_judgment.md`
records that decision and `docs/structure_changes.md` records the day it was
made. This package is the part that lets the rest of the code not care which
one answered.

The frame
---------

Every backend returns the same list of dictionaries, built by `row()` so that
"the same frame" is enforced rather than hoped for:

| key | what it is |
|---|---|
| `date` | the trading day, a `datetime.date` |
| `security_id` | the source's own permanent identifier -- CRSP's permno, Tiingo's permaticker -- or `None` where the source has none. A ticker is not an identifier: it is reassigned, and a study that keys on one silently splices two companies together |
| `ticker` | the symbol as asked for |
| `close` | the close as the source reports it, unadjusted |
| `adjusted_close` | split- and dividend-adjusted. Every return in `src/market.py` is computed from this column and from no other |
| `volume` | shares, as the source reports them |
| `delisting_return` | the return on the delisting day, or `None` where the source does not carry one. `None` and `0.0` are different answers and are never merged |
| `delisting_code` | the source's reason for the delisting, or `None` |

`None` in the last two means *this source does not know*, never *there was no
delisting*. `delisting_return_with_default` is what turns the first into a
number, and it says which of the two it did.

What is judged where
--------------------

Each backend has a pure `rows_from`, which takes that provider's own response
and returns the frame. That function is what `tests/test_prices.py` judges,
against a response fixture hand-written from the provider's published format --
never from a call this code made, because a fixture captured from the wire
agrees with the parser that captured it whatever either of them does.

`history` is the wire. `tests/test_prices.py` judges it with a stand-in for the
one module each backend talks through -- `requests` for Tiingo and EODHD, `wrds`
for CRSP -- answering the shape that module answers, so the request each backend
builds and the path from that answer to the frame are both exercised. What no
test here reaches is the service itself. `src/probe_price_sources.py` is what
puts each backend's `history` to it, about two delisted tickers, with whatever
credential the environment holds -- and while none exists, every backend
answers `Unconfigured` there and the service is still never reached.

Credentials
-----------

From the environment, never from a file in this tree: `$TIINGO_TOKEN`,
`$EODHD_TOKEN`, and for CRSP the `wrds` package's own `~/.pgpass`. A backend
with no credential raises `Unconfigured`, which is a state the caller reports
and not an error it hides -- the whole forward track is switched off by that
exception today and says so. `src/secret_scan.py` fails the gate if a token
string ever reaches a file here.
"""

from __future__ import annotations

import datetime as dt
import os
from typing import Any

COLUMNS = (
    "date",
    "security_id",
    "ticker",
    "close",
    "adjusted_close",
    "volume",
    "delisting_return",
    "delisting_code",
)

BACKENDS = ("crsp", "tiingo", "eodhd")
DEFAULT_BACKEND = "tiingo"

# Shumway (1997), "The Delisting Bias in CRSP Data", Journal of Finance 52(1),
# and Shumway and Warther (1999), "The Delisting Bias in CRSP's Nasdaq Data and
# its Implications for the Size Effect", Journal of Finance 54(6). These are the
# literature's own numbers for a delisting return CRSP does not carry, which is
# why they are here rather than a figure this project chose. `docs/HOW_WE_WORK.md`
# step 10 carries the same two lines, and the study reports the cross-section
# both with and without the correction.
DELISTING_DEFAULT = -0.30
DELISTING_DEFAULT_NASDAQ = -0.55
NASDAQ = "nasdaq"


class PriceError(Exception):
    """The source answered with something that is not a price history."""


class Unconfigured(PriceError):
    """No credential for this backend, so it was never asked."""


def row(
    *,
    date: dt.date,
    security_id: str | None,
    ticker: str,
    close: float,
    adjusted_close: float,
    volume: float | None,
    delisting_return: float | None = None,
    delisting_code: str | None = None,
) -> dict[str, Any]:
    """One row of the shared frame, with the types the frame promises.

    Every backend builds its rows through here. A backend that returned a plain
    dictionary would be agreeing with the frame on the day it was written and
    with nothing afterwards.
    """
    if not isinstance(date, dt.date) or isinstance(date, dt.datetime):
        raise PriceError(f"date must be a calendar date, not {date!r}")
    if not ticker:
        raise PriceError("a row with no ticker cannot be attributed to a company")
    for name, value in (("close", close), ("adjusted_close", adjusted_close)):
        number = _finite(value, name)
        if number <= 0:
            raise PriceError(f"{name}={value!r} is not a price")
    return {
        "date": date,
        "security_id": str(security_id) if security_id is not None else None,
        "ticker": ticker,
        "close": _finite(close, "close"),
        "adjusted_close": _finite(adjusted_close, "adjusted_close"),
        "volume": None if volume is None else _finite(volume, "volume"),
        "delisting_return": (
            None if delisting_return is None else _finite(delisting_return, "delisting_return")
        ),
        "delisting_code": None if delisting_code is None else str(delisting_code),
    }


def _finite(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise PriceError(f"{field}={value!r} is not a number") from error
    if number != number or number in (float("inf"), float("-inf")):
        raise PriceError(f"{field}={value!r} is not finite")
    return number


def delisting_return_with_default(
    delisting_return: float | None, *, exchange: str | None
) -> tuple[float, str]:
    """The delisting return to use, and which of the two it is.

    The reason travels with the number because the study reports the
    cross-section both with and without the correction, and a corrected row that
    does not say it was corrected cannot be taken back out of the total.
    """
    if delisting_return is not None:
        return float(delisting_return), "source"
    if exchange is not None and NASDAQ in exchange.strip().lower():
        return DELISTING_DEFAULT_NASDAQ, "shumway-and-warther-1999"
    return DELISTING_DEFAULT, "shumway-1997"


def name_from_environment(environ: dict[str, str] | None = None) -> str:
    """Which backend `$PRICE_BACKEND` names, or the default."""
    chosen = (environ if environ is not None else os.environ).get("PRICE_BACKEND", "").strip()
    if not chosen:
        return DEFAULT_BACKEND
    if chosen not in BACKENDS:
        raise PriceError(
            f"PRICE_BACKEND={chosen!r} is not one of {', '.join(BACKENDS)}"
        )
    return chosen


def backend(name: str | None = None):
    """The backend module named, or the one `$PRICE_BACKEND` names."""
    chosen = name_from_environment() if name is None else name
    if chosen not in BACKENDS:
        raise PriceError(f"{chosen!r} is not one of {', '.join(BACKENDS)}")
    from importlib import import_module

    return import_module(f"{__name__}.{chosen}")


def as_csv_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """The frame in the shape `src/market.py:read_prices` already reads.

    That reader takes a directory of files with a `date` and an
    `adjusted_close` column, and its expected values are computed by hand in
    `tests/test_market.py` from a frozen fixture. Writing the frame out in the
    shape it already reads is what lets the source underneath change without
    moving one of those expected values.
    """
    return [
        {
            "date": entry["date"].isoformat(),
            "close": repr(entry["close"]),
            "adjusted_close": repr(entry["adjusted_close"]),
        }
        for entry in sorted(rows, key=lambda entry: entry["date"])
    ]
