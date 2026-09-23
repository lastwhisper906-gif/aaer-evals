"""CRSP through WRDS: the pattern study's backend, and the only one with `dlret`.

A universe drawn from a past date is full of companies that stopped trading, and
what happened on the day they stopped is the number that decides whether the
study measures accounting failure or measures survivorship. CRSP carries it --
`dlret`, the delisting return, with `dlstcd`, the reason -- and it is the
standard the literature reads because of exactly that. Stony Brook subscribes,
so it is free here; a student registers at `wrds-www.wharton.upenn.edu/register`
and the school's representative approves the account.

The `wrds` package reads `~/.pgpass`, which is Postgres's own credential file
and lives outside this tree. There is no token to set and nothing to write down
here: no credential file, no credential argument, nothing this module could
leak. Until that file exists this backend answers `Unconfigured` and the study
does not start, which is the state recorded in `docs/needs_judgment.md`.

The query
---------

`crsp.dsf` is the daily stock file -- one row per security per trading day.
`crsp.dsedelist` is the delisting event file -- at most one row per security,
carrying `dlret` and `dlstcd`. They are joined on `permno`, which is CRSP's
permanent security identifier and the reason a CRSP series never splices two
companies together the way a ticker-keyed series does.

Three conventions of the daily file that a reader has to know, and that this
module handles rather than passes on:

* **`prc` is negated when it is a bid/ask average** rather than a closing trade.
  CRSP writes the sign to mark the difference; the price is its magnitude. A
  reader that takes the sign at face value gets a negative price, and a reader
  that filters those rows out drops the thin days on purpose.
* **`cfacpr` is the cumulative price adjustment factor.** `prc / cfacpr` is the
  split-adjusted price, which is what the frame's `adjusted_close` carries.
  Where `cfacpr` is zero or missing the row is refused rather than divided.
* **`ret` already carries the delisting return on the delisting day** in the
  CRSP files that merge it. This module does not merge it a second time: it
  hands `dlret` over as its own column and leaves the arithmetic to the study,
  because a return that has been corrected twice looks exactly like one that has
  been corrected once.

One convention of the wire rather than of CRSP: `wrds.Connection.raw_sql`
answers a pandas frame, and `history` hands its rows over with
`to_dict("records")`. A missing value in a numeric column arrives there as
`float('nan')`, not `None`, and the legacy CRSP tables store `permno` and
`dlstcd` as double precision, so a column with one missing value carries every
code as a float -- `574.0`, `90001.0`. `_known` and `_code` turn the first back
into `None` and the second back into the integer CRSP publishes. Without them
every row that is not a delisting day -- nearly every row of every series --
would be refused for a delisting return that "is not finite".

`rows_from` takes the rows the query returned and is what the fixture judges.
`history` is the wire; `tests/test_prices.py` judges it with a stand-in `wrds`
module whose frame answers the shape pandas does. Nothing here imports `wrds`
until it is called -- the package is not in `requirements.txt` and the module
has to stay importable on a machine that has never had a WRDS account.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from src.prices import PriceError, Unconfigured, row

NAME = "crsp"
PGPASS = Path.home() / ".pgpass"

DAILY_TABLE = "crsp.dsf"
DELIST_TABLE = "crsp.dsedelist"

QUERY = """
    select  f.permno, f.date, f.prc, f.vol, f.cfacpr, f.ret,
            d.dlret, d.dlstcd, n.ticker, n.exchcd
    from    crsp.dsf as f
    left join crsp.dsedelist as d
           on d.permno = f.permno and d.dlstdt = f.date
    left join crsp.dsenames  as n
           on n.permno = f.permno
          and f.date between n.namedt and coalesce(n.nameendt, current_date)
    where   n.ticker = %(ticker)s
      and   f.date between %(start)s and %(end)s
    order by f.date
"""


def credential(pgpass: Path | None = None) -> Path:
    """The `~/.pgpass` the `wrds` package reads, or Unconfigured.

    There is no token here. The credential is a file Postgres already owns, in
    the user's home directory, outside this tree -- which is why this is the one
    backend whose credential cannot be committed by accident.
    """
    path = PGPASS if pgpass is None else pgpass
    if not path.exists():
        raise Unconfigured(
            f"{path} does not exist, so the {NAME} backend was never asked. "
            f"Register at https://wrds-www.wharton.upenn.edu/register/ with the "
            f"school address, wait for the approval, then write the file the "
            f"`wrds` package asks for on its first connection."
        )
    return path


def _known(value: Any) -> Any:
    """`None` for a missing value, whether it arrived as `None` or as pandas' NaN."""
    if isinstance(value, float) and value != value:
        return None
    return value


def _code(value: Any) -> Any:
    """A code CRSP publishes as an integer, back from the float pandas made of it."""
    value = _known(value)
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _price(value: Any) -> float:
    """The magnitude of `prc`, whose sign marks a bid/ask average."""
    if _known(value) is None:
        raise PriceError("prc is null, so the row carries no price")
    try:
        return abs(float(value))
    except (TypeError, ValueError) as error:
        raise PriceError(f"prc={value!r} is not a number") from error


def _day(value: Any) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError as error:
        raise PriceError(f"date={value!r} is not a date") from error


def rows_from(payload: Any, *, ticker: str | None = None) -> list[dict]:
    """The rows the query returned, as the shared frame. Judged by the fixture."""
    if not isinstance(payload, list):
        raise PriceError(f"the {NAME} result is not a list of rows")
    out = []
    for entry in payload:
        if not isinstance(entry, dict):
            raise PriceError(f"a {NAME} row is not an object")
        missing = [key for key in ("permno", "date", "prc", "cfacpr") if key not in entry]
        if missing:
            raise PriceError(
                f"a {NAME} row has no {', '.join(missing)} -- refused, because the "
                f"adjusted close is prc over cfacpr and neither can be guessed"
            )
        close = _price(entry["prc"])
        factor = _known(entry["cfacpr"])
        try:
            factor = float(factor)
        except (TypeError, ValueError) as error:
            raise PriceError(f"cfacpr={factor!r} is not a number") from error
        if factor == 0:
            raise PriceError(
                f"cfacpr is zero on {entry['date']}, so the adjusted close would be a "
                f"division by zero -- refused rather than dropped"
            )
        symbol = ticker or entry.get("ticker")
        if not symbol:
            raise PriceError("a row with no ticker cannot be attributed to a company")
        out.append(
            row(
                date=_day(entry["date"]),
                security_id=_code(entry["permno"]),
                ticker=str(symbol).upper(),
                close=close,
                adjusted_close=close / factor,
                volume=_known(entry.get("vol")),
                delisting_return=_known(entry.get("dlret")),
                delisting_code=_code(entry.get("dlstcd")),
            )
        )
    return sorted(out, key=lambda entry: entry["date"])


def history(
    ticker: str,
    start: dt.date | None = None,
    end: dt.date | None = None,
    *,
    pgpass: Path | None = None,
) -> list[dict]:
    """The daily history, from WRDS.

    Judged by `tests/test_prices.py` against a stand-in `wrds` module answering
    the frame shape pandas does, NaN included. Against the real service it has
    never been run: nobody here has a WRDS account yet.
    """
    credential(pgpass)
    try:
        import wrds
    except ImportError as error:  # the package is deliberately not a requirement
        raise Unconfigured(
            "the `wrds` package is not installed, so the crsp backend was never "
            "asked. It is not in requirements.txt: it is needed by the pattern "
            "study alone, and every other entry point has to stay importable on a "
            "machine that has no WRDS account."
        ) from error
    connection = wrds.Connection()
    try:
        frame = connection.raw_sql(
            QUERY,
            params={
                "ticker": ticker.strip().upper(),
                "start": (start or dt.date(1926, 1, 1)).isoformat(),
                "end": (end or dt.date.today()).isoformat(),
            },
        )
    finally:
        connection.close()
    return rows_from(frame.to_dict("records"), ticker=ticker.strip().upper())
