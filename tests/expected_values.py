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

**A note is checked, not just counted.** "Non-empty prose" is not provenance: it
would accept `"somewhere"`, and a parser-produced number could be relabelled into
the file with nobody the wiser. So a note has to name one of the source kinds
this project actually has, and every file it cites has to exist — with the thing
inside it a reader can grep for, never a line number. Line numbers were the first
thing to rot: the citations written into these notes were already stale in the
commit that wrote them, because the test files moved underneath them.

`expected.json` is a different file for a different reason: it is the
extraction-drift baseline `src/extraction_checks.py` reads, it is the pipeline's
own output by construction, and it is not an expected value. Keeping both in one
file is what let a self-certified number pass for an expectation.
"""

from __future__ import annotations

import functools
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# The kinds of source this project has. A note names one of them in its own
# words; a note that names none is not saying where its value came from.
SOURCE_KINDS = ("read by eye", "already judged", "the filing", "the exhibit",
                "the submissions index", "hand computation", "by construction",
                "xbrl instance", "companyfacts")

# `tests/test_parse_8k.py:119` is a promise about a line, and the line moves.
# Cite the file, or the file and a name in it — both survive an edit.
LINE_CITATION = re.compile(r"\b[\w/.\-]+\.(?:py|md):\d+")
CITATION = re.compile(r"\b((?:src|tests|docs)/[\w/.\-]+\.(?:py|md))(?:::(\w+))?")


@functools.lru_cache(maxsize=None)
def _cited(path: str) -> str | None:
    """One cited file's text, or None if it is not in this repository."""
    target = REPO / path
    return target.read_text(encoding="utf-8") if target.is_file() else None


@functools.lru_cache(maxsize=None)
def unsourced(note: str) -> str:
    """What is wrong with this source note, or an empty string.

    Cached on the note itself, and the files it cites cached beside it: a few
    hundred distinct notes back tens of thousands of reads.
    """
    if not note.strip():
        return "the source note is empty"
    if not any(kind in note.lower() for kind in SOURCE_KINDS):
        return f"the note names no source kind, only prose: {note[:60]!r}"
    stale = LINE_CITATION.search(note)
    if stale:
        return (f"{stale.group(0)} cites a line number, which the next edit of that "
                f"file makes a lie — cite the file, or file::name")
    for path, anchor in CITATION.findall(note):
        text = _cited(path)
        if text is None:
            return f"{path} is cited and is not a file in this repository"
        if anchor and anchor not in text:
            return f"{path} does not contain {anchor!r}"
    return ""


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
    if not isinstance(entry, dict) or set(entry) != {"value", "from"}:
        raise ValueError(f"{ticker} {key}: an expected value has to name its source")
    wrong = unsourced(str(entry["from"]))
    if wrong:
        raise ValueError(f"{ticker} {key}: {wrong}")
    return entry["value"]


def source(ticker: str, key: str) -> str:
    """The one-line note saying where the value at `key` came from."""
    value(ticker, key)
    return entries(ticker)[key]["from"]
