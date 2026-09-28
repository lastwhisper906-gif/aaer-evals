"""EODHD's All World end-of-day prices: the paid fallback.

One month at twenty dollars if the WRDS account is refused, bulk-download
fifteen years, cancel. It is the fallback and not the choice because it carries
no delisting return either -- it retains the *rows* of a delisted ticker, which
is more than a free API does, but the return on the delisting day is not in the
data, so the study would run on the Shumway default for every delisted row
rather than on CRSP's own number for most of them.

Two endpoints, both under `https://eodhd.com/api`:

* `/eod/{TICKER}.US?fmt=json` -- the daily rows. The `.US` suffix is EODHD's
  exchange code and is part of the symbol, not an argument.
* `/exchange-symbol-list/US?delisted=1&fmt=json` -- the delisted listing, which
  is how a caller learns a ticker is gone rather than misspelt. A symbol absent
  from the live list and present here stopped trading; a symbol absent from both
  was never right.

A price row as EODHD documents it:

    {"date": "2008-09-17", "open": 0.3, "high": 0.36, "low": 0.11,
     "close": 0.21, "adjusted_close": 0.21, "volume": 471504000}

The date is already a calendar day, and `adjusted_close` is already the frame's
own column name. The `delisted=1` listing is a list of objects whose `Code` is
the symbol and whose `Exchange` names the exchange -- the exchange is what
decides which Shumway default a missing delisting return takes, so it is read
here rather than guessed later.

The token comes from `$EODHD_TOKEN`. EODHD takes it as a query parameter only,
which is the source's own interface and not a choice made here; it is still read
from the environment and never from a file in this tree.
"""

from __future__ import annotations

import datetime as dt
import os
from typing import Any

from src.prices import PriceError, Unconfigured, row

NAME = "eodhd"
BASE = "https://eodhd.com/api"
TOKEN_VARIABLE = "EODHD_TOKEN"
EXCHANGE_SUFFIX = ".US"
TIMEOUT_SECONDS = 60


def credential(environ: dict[str, str] | None = None) -> str:
    token = (environ if environ is not None else os.environ).get(TOKEN_VARIABLE, "").strip()
    if not token:
        raise Unconfigured(
            f"${TOKEN_VARIABLE} is not set, so the {NAME} backend was never asked. "
            f"It is the paid fallback: one month, a bulk download, then cancel."
        )
    return token


def symbol(ticker: str) -> str:
    """The symbol EODHD names, which carries its exchange code."""
    bare = ticker.strip().upper()
    return bare if bare.endswith(EXCHANGE_SUFFIX) else f"{bare}{EXCHANGE_SUFFIX}"


def rows_from(payload: Any, *, ticker: str, security_id: str | None = None) -> list[dict]:
    """EODHD's daily response as the shared frame. Judged by the fixture."""
    if not isinstance(payload, list):
        raise PriceError(f"the {NAME} daily response is not a list of rows")
    out = []
    for entry in payload:
        if not isinstance(entry, dict):
            raise PriceError(f"an {NAME} row is not an object")
        missing = [key for key in ("date", "close", "adjusted_close") if key not in entry]
        if missing:
            raise PriceError(
                f"an {NAME} row has no {', '.join(missing)} -- refused, because every "
                f"return is computed from the adjusted close"
            )
        try:
            day = dt.date.fromisoformat(str(entry["date"]))
        except ValueError as error:
            raise PriceError(f"date={entry['date']!r} is not a date") from error
        out.append(
            row(
                date=day,
                security_id=security_id,
                ticker=ticker,
                close=entry["close"],
                adjusted_close=entry["adjusted_close"],
                volume=entry.get("volume"),
                delisting_return=None,
                delisting_code=None,
            )
        )
    return sorted(out, key=lambda entry: entry["date"])


def delisted_from(payload: Any) -> dict[str, dict[str, str]]:
    """The delisted listing, keyed by symbol, carrying the exchange.

    The exchange decides which of the two Shumway defaults a missing delisting
    return takes, so it is read off the source rather than assumed.
    """
    if not isinstance(payload, list):
        raise PriceError(f"the {NAME} delisted listing is not a list")
    listing = {}
    for entry in payload:
        if not isinstance(entry, dict) or "Code" not in entry:
            raise PriceError(f"an {NAME} delisted row has no Code")
        listing[str(entry["Code"]).upper()] = {
            "ticker": str(entry["Code"]).upper(),
            "name": str(entry.get("Name", "")),
            "exchange": str(entry.get("Exchange", "")),
        }
    return listing


def _get(path: str, params: dict[str, str], token: str) -> Any:
    import requests

    session = requests.Session()
    # `requests` otherwise reads the process's `~/.netrc` and its proxy
    # variables, which route the request.
    session.trust_env = False
    try:
        response = session.get(
            f"{BASE}{path}",
            params={**params, "api_token": token, "fmt": "json"},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException as error:
        # EODHD takes the token in the query string, so the address of a failed
        # request -- which `requests` puts in its message -- carries the token.
        # The name of the failure is enough to act on, and `from None` drops
        # the chain that would print the address anyway.
        raise PriceError(
            f"{NAME} could not be reached for {path}: {type(error).__name__}"
        ) from None
    if response.status_code != 200:
        raise PriceError(
            f"{NAME} answered {response.status_code} for {path}: "
            f"{response.text.replace(token, '<token>')[:200]}"
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
    params = {}
    if start is not None:
        params["from"] = start.isoformat()
    if end is not None:
        params["to"] = end.isoformat()
    payload = _get(f"/eod/{symbol(ticker)}", params, token)
    return rows_from(payload, ticker=ticker.strip().upper())


def delisted(*, environ: dict[str, str] | None = None) -> dict[str, dict[str, str]]:
    """Every symbol EODHD records as having stopped trading on a US exchange."""
    token = credential(environ)
    return delisted_from(_get("/exchange-symbol-list/US", {"delisted": "1"}, token))
