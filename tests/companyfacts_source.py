"""The committed companyfacts document, opened here as the source it is.

`src/trends.py` reads the same file through `src/cutoff_guard.py` and turns its
rows into facts. This module opens it again, on its own, and offers nothing but
what EDGAR wrote: the value under a `(tag, unit, accession, period)` key, the
date the filing carrying it was filed, and the `frame` EDGAR stamped on it.

That separation is the point. A trend cell says which fact it took a number
from; the claim that the number *is* that fact's is only worth anything if the
fact is looked up somewhere other than in the code that read it. So no import
from `src/` appears here, the file is opened by name, and the keys are EDGAR's
own — `accn`, `val`, `filed`, `frame`.

The twelve documents are ninety megabytes of JSON before they are parsed, so
each is read once and kept as the index the tests ask it for.
"""

from __future__ import annotations

import functools
import gzip
import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"

# A gzipped fixture says so in its first two bytes, so a reader never has to
# ask the manifest what it is holding.
GZIP_MAGIC = b"\x1f\x8b"

STORED = "companyfacts.json"


def _document(ticker: str) -> dict:
    for name in (f"{STORED}.gz", STORED):
        path = FIXTURES / ticker / name
        if path.is_file():
            raw = path.read_bytes()
            return json.loads(gzip.decompress(raw) if raw[:2] == GZIP_MAGIC else raw)
    raise AssertionError(f"{ticker} has no companyfacts document under {FIXTURES}")


def period_of(row: dict) -> str:
    """How `src/trends.py` names a row's period inside a fact id."""
    return f"{row['start']}..{row['end']}" if row.get("start") else row["end"]


@functools.lru_cache(maxsize=None)
def values(ticker: str) -> dict[tuple[str, str, str, str], tuple[float, str]]:
    """(tag, unit, accession, period) → the value EDGAR wrote and the date filed."""
    index = {}
    for tag, concept in _document(ticker)["facts"]["us-gaap"].items():
        for unit, rows in concept["units"].items():
            for row in rows:
                index[(tag, unit, row["accn"], period_of(row))] = (
                    float(row["val"]), row["filed"])
    return index


@functools.lru_cache(maxsize=None)
def stamped_frames(ticker: str) -> dict[tuple[str, str], dict[str, int]]:
    """(start, end) → the frames EDGAR stamped on rows of that period, and how many.

    EDGAR stamps a `frame` on the one row it treats as canonical for a calendar
    frame, so a period collects a stamp from every concept EDGAR framed it in.
    Almost always they agree; where they do not, the count is what says which
    answer is EDGAR's and which is a stray.
    """
    frames: dict[tuple[str, str], dict[str, int]] = {}
    for concept in _document(ticker)["facts"]["us-gaap"].values():
        for rows in concept["units"].values():
            for row in rows:
                if not row.get("frame") or not row.get("start"):
                    continue
                seen = frames.setdefault((row["start"], row["end"]), {})
                seen[row["frame"]] = seen.get(row["frame"], 0) + 1
    return frames


@functools.lru_cache(maxsize=None)
def accessions(ticker: str) -> frozenset[str]:
    """Every accession any row of this company's companyfacts came from."""
    return frozenset(row["accn"]
                     for concept in _document(ticker)["facts"]["us-gaap"].values()
                     for rows in concept["units"].values()
                     for row in rows)


@functools.lru_cache(maxsize=None)
def as_of(ticker: str) -> str:
    """The date the record was filtered to when it was fetched."""
    return _document(ticker)["as_of"]
