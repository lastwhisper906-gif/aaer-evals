"""The one reader of `expected_values.json`, so no value can arrive unsourced.

An expected value comes from the source, never from the first run of the code it
judges (`CLAUDE.md`). The parsers arrived with fixtures that broke that rule: the
numbers they were held to were produced by running them. Splitting the file was
the fix that stays fixed, and this is the half that makes it stick.

`tests/fixtures/{ticker}/expected_values.json` is a flat object, one entry per
expectation, keyed by the dotted path the old file nested. Every entry is exactly
`{"value": ..., "from": "..."}` — the note names where the value came from, in
one line. There is no depth at which a bare number can hide, so the check below
is one loop, and a value written without a source cannot be read at all.

`expected.json` is a different file for a different reason: it is the
extraction-drift baseline `src/extraction_checks.py` reads, it is the pipeline's
own output by construction, and it is not an expected value. Keeping both in one
file is what let a self-certified number pass for an expectation.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@functools.lru_cache(maxsize=None)
def entries(ticker: str) -> dict:
    """Every expectation recorded for one company, unchecked."""
    path = FIXTURES / ticker / "expected_values.json"
    return json.loads(path.read_text(encoding="utf-8"))


def value(ticker: str, key: str):
    """The expected value at `key`, or an error naming what is missing.

    A key that is not there is not a hole to fill in: it is an expectation this
    project deleted because nothing outside the parsers could source it. The
    assertion that read it goes too.
    """
    recorded = entries(ticker)
    if key not in recorded:
        raise KeyError(f"{ticker}: expected_values.json has no {key!r} — a deleted "
                       f"expectation stays deleted; delete the assertion, not the key")
    entry = recorded[key]
    if not isinstance(entry, dict) or set(entry) != {"value", "from"} \
            or not str(entry["from"]).strip():
        raise ValueError(f"{ticker} {key}: an expected value has to name its source")
    return entry["value"]


def source(ticker: str, key: str) -> str:
    """The one-line note saying where the value at `key` came from."""
    value(ticker, key)
    return entries(ticker)[key]["from"]
