"""Tiingo's daily end-of-day prices: the forward track's backend.

Twelve companies, all listed today, one daily fetch. The free tier answers that
-- fifty requests an hour, a thousand a day, internal use only -- and the
delisted question the study has to answer does not arise for a company that is
still trading. Tiingo does retain a ticker that stops trading, from about 2015,
for as long as the symbol has not been reassigned; it carries no delisting
return at all, so every row here leaves that column `None`, which the frame
reads as *this source does not know* and never as *there was no delisting*.

Two endpoints, both under `https://api.tiingo.com/tiingo/daily`:

* `/{ticker}` -- the metadata object, whose `permaTicker` is the permanent
  identifier. A ticker is reassigned and a permaticker is not, which is the
  whole reason this request is made at all.
* `/{ticker}/prices?startDate=&endDate=` -- the daily rows.

A price row as Tiingo documents it:

    {"date": "2023-10-12T00:00:00.000Z", "close": 92.7, "high": 93.0,
     "low": 92.2, "open": 92.5, "volume": 5674900, "adjClose": 92.7,
     "adjHigh": 93.0, "adjLow": 92.2, "adjOpen": 92.5, "adjVolume": 5674900,
     "divCash": 0.0, "splitFactor": 1.0}

`adjClose` is the split- and dividend-adjusted close and is what the frame's
`adjusted_close` takes. `close` is unadjusted. The date carries a time and a
zone letter that are always midnight and always universal time; the calendar day
is what a daily bar is, so the time is dropped rather than converted -- a
conversion would move a bar across a day boundary for no reason.

The token comes from `$TIINGO_TOKEN` and is sent in the `Authorization` header
rather than in the query string, so it does not reach a proxy log or a redirect.
"""

from __future__ import annotations

import datetime as dt
import os
from typing import Any

from src.prices import PriceError, Unconfigured, row

NAME = "tiingo"
BASE = "https://api.tiingo.com/tiingo/daily"
TOKEN_VARIABLE = "TIINGO_TOKEN"
TIMEOUT_SECONDS = 30


def credential(environ: dict[str, str] | None = None) -> str:
    token = (environ if environ is not None else os.environ).get(TOKEN_VARIABLE, "").strip()
    if not token:
        raise Unconfigured(
            f"${TOKEN_VARIABLE} is not set, so the {NAME} backend was never asked. "
            f"Sign up at https://www.tiingo.com and export the token; it is read "
            f"from the environment and never from a file in this tree."
        )
    return token


def _day(stamp: Any) -> dt.date:
    """The calendar day out of Tiingo's stamp, whose time is always midnight."""
    if not isinstance(stamp, str) or not stamp:
        raise PriceError(f"date={stamp!r} is not a Tiingo date")
    try:
        return dt.date.fromisoformat(stamp[:10])
    except ValueError as error:
        raise PriceError(f"date={stamp!r} is not a date") from error


def permaticker_from(metadata: Any) -> str | None:
    """Tiingo's permanent identifier for a symbol, or None if it sent none.

    A symbol is reassigned when a company leaves and another takes the letters,
    so a series keyed on the symbol splices two companies together without a
    gap. The permaticker is what the frame's `security_id` carries.
    """
    if not isinstance(metadata, dict):
        raise PriceError("the Tiingo metadata response is not an object")
    found = metadata.get("permaTicker")
    return str(found) if found else None


def rows_from(payload: Any, *, ticker: str, security_id: str | None = None) -> list[dict]:
    """Tiingo's daily response as the shared frame. Judged by the fixture."""
    if not isinstance(payload, list):
        raise PriceError(f"the {NAME} daily response is not a list of rows")
    out = []
    for entry in payload:
        if not isinstance(entry, dict):
            raise PriceError(f"a {NAME} row is not an object")
        missing = [key for key in ("date", "close", "adjClose") if key not in entry]
        if missing:
            raise PriceError(
                f"a {NAME} row has no {', '.join(missing)} -- refused, because every "
                f"return is computed from the adjusted close"
            )
        out.append(
            row(
                date=_day(entry["date"]),
                security_id=security_id,
                ticker=ticker,
                close=entry["close"],
                adjusted_close=entry["adjClose"],
                volume=entry.get("volume"),
                delisting_return=None,
                delisting_code=None,
            )
        )
    return sorted(out, key=lambda entry: entry["date"])


def _get(path: str, params: dict[str, str], token: str) -> Any:
    import requests

    response = requests.get(
        f"{BASE}{path}",
        params=params,
        headers={"Authorization": f"Token {token}", "Content-Type": "application/json"},
        timeout=TIMEOUT_SECONDS,
    )
    if response.status_code != 200:
        raise PriceError(
            f"{NAME} answered {response.status_code} for {path}: "
            f"{response.text[:200]}"
        )
    return response.json()


def history(
    ticker: str,
    start: dt.date | None = None,
    end: dt.date | None = None,
    *,
    environ: dict[str, str] | None = None,
) -> list[dict]:
    """The daily history, from the wire.

    Judged by `tests/test_prices.py` against a stand-in `requests` module, which
    checks the address, the parameters and where the token goes. Against the
    real service it has never been run: nobody here has a token yet.
    """
    token = credential(environ)
    metadata = _get(f"/{ticker.lower()}", {}, token)
    params = {}
    if start is not None:
        params["startDate"] = start.isoformat()
    if end is not None:
        params["endDate"] = end.isoformat()
    payload = _get(f"/{ticker.lower()}/prices", params, token)
    return rows_from(payload, ticker=ticker.upper(), security_id=permaticker_from(metadata))
