"""A second reader of the companyfacts record, written for the tests alone.

`src/trends.py` picks one row out of the record and then reports which row it
picked. Asserting that its report agrees with its own reading of the record
proves nothing about either, so this module opens the committed
`tests/fixtures/{ticker}/companyfacts.json.gz` itself — `gzip`, `json`, and
nothing else — and **imports nothing from `src/`**. It is the same device
`tests/independent_text.py` is for the HTML strippers.

It knows three things, each of them stated by `docs/INPUT_SPEC.md` rather than
by the module under test:

1. A fact row lives at `facts[namespace][tag]["units"][unit]`, carries `val`,
   `accn` and `filed`, and has either `start` and `end` (a duration) or `end`
   alone (an instant). Those are EDGAR's own keys.
2. **The cutoff applies to the rows.** A row whose own `filed` is later than the
   run's cutoff is not an input. Dates are parsed before they are compared, so
   an unusable cutoff raises here rather than sorting as a large string.
3. **"When a period is reported more than once, the latest filing before the
   cutoff wins"** (§1). If that filing states two values for one period, this
   module returns both and lets the test say what should happen.
4. **The numeric facts come from the periodic financial statements.** §1's
   table gives them one row — *"10-K, 10-Q, /A | all numeric facts"* — puts
   DEF 14A under **Not fetched**, and gives an 8-K 8.01 or 9.01 *"item codes
   only"*. A catalogue of every filing's facts carries the rest anyway, so the
   row's own `form` is read here before its value is.

`period` is written the way `docs/INPUT_SPEC.md` §2.2 writes it inside a fact
id: `start..end` for a duration, the date alone for an instant.
"""

from __future__ import annotations

import datetime as dt
import functools
import gzip
import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NAMESPACE = "us-gaap"
UNIT = "USD"


@functools.lru_cache(maxsize=None)
def record(ticker: str) -> dict:
    """The committed companyfacts document, every row of it, ungated."""
    path = FIXTURES / ticker / "companyfacts.json.gz"
    return json.loads(gzip.decompress(path.read_bytes()))


def rows(ticker: str, tag: str, *, namespace: str = NAMESPACE,
         unit: str = UNIT, every_form: bool = False) -> list[dict]:
    """The rows the record holds for one concept in one unit.

    The periodic financial statements only, unless `every_form` asks for the
    whole catalogue — which is what shows that the rule leaves something out.
    """
    concept = record(ticker).get("facts", {}).get(namespace, {}).get(tag)
    found = list((concept or {}).get("units", {}).get(unit, []))
    return found if every_form else [row for row in found if a_statement(row)]


def a_statement(row: dict) -> bool:
    """§1's own list: the numeric facts are 10-K, 10-Q and their amendments."""
    return str(row.get("form") or "").startswith(("10-K", "10-Q"))


def units(ticker: str, tag: str, *, namespace: str = NAMESPACE) -> list[str]:
    concept = record(ticker).get("facts", {}).get(namespace, {}).get(tag)
    return sorted((concept or {}).get("units", {}))


def spelled(row: dict) -> str:
    """The period of one row, in the spelling a fact id uses."""
    return f"{row['start']}..{row['end']}" if row.get("start") else row["end"]


def inside(candidates: list[dict], cutoff: str) -> list[dict]:
    """The rows filed at or before the cutoff. Dates, not strings."""
    limit = dt.date.fromisoformat(cutoff)
    return [row for row in candidates
            if dt.date.fromisoformat(row["filed"]) <= limit]


def for_period(candidates: list[dict], period: str) -> list[dict]:
    return [row for row in candidates if spelled(row) == period]


def latest(candidates: list[dict]) -> list[dict]:
    """The rows of the newest filing date among them. Empty in, empty out."""
    if not candidates:
        return []
    newest = max(row["filed"] for row in candidates)
    return [row for row in candidates if row["filed"] == newest]


def reported(ticker: str, tag: str, period: str, cutoff: str) -> list[dict]:
    """The rows the rule leaves standing for one concept and one period."""
    return latest(for_period(inside(rows(ticker, tag), cutoff), period))


def one_value(ticker: str, tag: str, period: str, cutoff: str) -> float:
    """The single value the rule settles on, or an assertion the test will fail."""
    standing = reported(ticker, tag, period, cutoff)
    values = sorted({row["val"] for row in standing})
    assert len(values) == 1, f"{ticker} us-gaap:{tag} {period}: {values}"
    return float(values[0])
