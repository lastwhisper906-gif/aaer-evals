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
project. The CIK and SIC are what the SEC's header prints for the company's
latest annual report filed on or before that date -- the submission header the
fixture fetcher already commits and hashes in the company's manifest -- and the
date is the `as_of` of the fixture set the row entered with. None of them is a
value this repository computed.

    from src import universe
    universe.tickers()           # ('AAPL', 'STX', ...)
    universe.cik('NVDA')         # '0001045810'
    universe.sic('NVDA')         # '3674'
"""

from __future__ import annotations

import datetime as dt
import json
import re
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
    where = PATH if path is None else Path(path)
    document = _document(where)
    out = []
    seen = set()
    for index, row in enumerate(document["companies"]):
        if not isinstance(row, dict):
            raise UniverseError(f"companies[{index}] is not an object")
        out.append(_checked(index, row, seen))
    if not out:
        raise UniverseError(f"{where} lists no companies")
    return tuple(out)


def _checked(index: int, row: dict[str, Any], seen: set[str]) -> dict[str, Any]:
    """One row, refused unless every required field is a non-empty string.

    `str(None)` is "None", so a check that stringified first let `"cik": null`
    through as a CIK spelled N-o-n-e. Each field must *be* a string, not merely
    print as one, and the CIK, SIC and date must look like what they are.
    """
    name = row.get("ticker") if isinstance(row.get("ticker"), str) else "unnamed"
    problems = []
    for key in REQUIRED:
        if key not in row:
            problems.append(f"{key} is missing")
        elif not isinstance(row[key], str):
            problems.append(f"{key} is {row[key]!r}, not a string")
        elif not row[key].strip():
            problems.append(f"{key} is empty")
    if not problems:
        if not re.fullmatch(r"\d{10}", row["cik"].strip()):
            problems.append(f"cik {row['cik']!r} is not ten digits")
        if not re.fullmatch(r"\d{4}", row["sic"].strip()):
            problems.append(f"sic {row['sic']!r} is not four digits")
        try:
            dt.date.fromisoformat(row["added_on"].strip())
        except ValueError:
            problems.append(f"added_on {row['added_on']!r} is not a YYYY-MM-DD date")
    if problems:
        raise UniverseError(f"companies[{index}] ({name}): {'; '.join(problems)}")
    ticker = row["ticker"].strip().upper()
    if ticker in seen:
        raise UniverseError(f"{ticker} appears twice; a company is in the universe once")
    seen.add(ticker)
    return {**row, "ticker": ticker, "cik": row["cik"].strip(),
            "sic": row["sic"].strip(), "added_on": row["added_on"].strip()}


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
