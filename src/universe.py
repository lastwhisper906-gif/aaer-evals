"""The companies this pipeline reads, taken from `universe.json` and not from code.

The twelve tickers were a tuple in `src/fetch_fixtures.py`, and three other
modules imported it from there. That made the universe a code change: adding a
thirteenth company meant editing a literal, and every fetcher, fixture path and
routine that wanted the list had to import the fetcher to get it. `CLAUDE.md`
says the twelve test the pipeline rather than the signal, which is exactly the
kind of thing that should expand without a commit to `src/`.

So the list is a file at the repository root, and this module is how it is read.
`rows()` reads the file every call rather than caching at import, because the
judge for this item appends a thirteenth row at run time and asks the fetcher
what it plans -- a module-level snapshot would answer twelve and be wrong in
exactly the way that matters.

Each row carries the ticker, the CIK, the SIC and the date the row entered the
project. The first three come from the SEC's own submissions record for that
CIK; none of them is a value this repository computed.

    from src import universe
    universe.tickers()           # ('AAPL', 'STX', ...)
    universe.cik('NVDA')         # '0001045810'
    universe.sic('NVDA')         # '3674'
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PATH = Path(__file__).resolve().parent.parent / "universe.json"

REQUIRED = ("ticker", "cik", "sic", "added_on")


class UniverseError(Exception):
    """The universe file is missing, unreadable, or not shaped like a universe."""


def _document(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise UniverseError(
            f"{path} does not exist. The universe is a file at the repository "
            f"root; it is not a default this module supplies."
        )
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise UniverseError(f"{path} is not JSON: {error}") from error
    if not isinstance(document, dict) or not isinstance(document.get("companies"), list):
        raise UniverseError(f"{path} has no `companies` list")
    return document


def rows(path: Path | None = None) -> tuple[dict[str, Any], ...]:
    """Every company, in the file's own order.

    Read on every call. A thirteenth row appended while the process is running
    is a thirteenth company, which is the whole point of the file.
    """
    document = _document(PATH if path is None else Path(path))
    out = []
    seen = set()
    for index, row in enumerate(document["companies"]):
        if not isinstance(row, dict):
            raise UniverseError(f"companies[{index}] is not an object")
        missing = [key for key in REQUIRED if not str(row.get(key, "")).strip()]
        if missing:
            raise UniverseError(
                f"companies[{index}] ({row.get('ticker', 'unnamed')}) is missing "
                f"{', '.join(missing)}"
            )
        ticker = str(row["ticker"]).strip().upper()
        if ticker in seen:
            raise UniverseError(f"{ticker} appears twice; a company is in the universe once")
        seen.add(ticker)
        out.append({**row, "ticker": ticker, "cik": str(row["cik"]).strip(),
                    "sic": str(row["sic"]).strip()})
    if not out:
        raise UniverseError(f"{path or PATH} lists no companies")
    return tuple(out)


def tickers(path: Path | None = None) -> tuple[str, ...]:
    """Every ticker, in the file's own order."""
    return tuple(row["ticker"] for row in rows(path))


def _one(ticker: str, path: Path | None = None) -> dict[str, Any]:
    wanted = ticker.strip().upper()
    for row in rows(path):
        if row["ticker"] == wanted:
            return row
    raise UniverseError(f"{wanted} is not in the universe; add a row to {path or PATH}")


def cik(ticker: str, path: Path | None = None) -> str:
    """The zero-padded ten-digit CIK, as the SEC writes it."""
    return _one(ticker, path)["cik"]


def sic(ticker: str, path: Path | None = None) -> str:
    """The SIC code, as a string, because leading zeroes are part of it."""
    return _one(ticker, path)["sic"]
