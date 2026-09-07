"""The deterministic shrinking layer. Python only; no model touches this.

Everything here is a **deletion** or a **table rendering**. That is the whole
design constraint: this is the stage where the text handed to the predictor
stops being the filing, and every change that is not a deletion is a quote that
will later fail to match the committed input. So a paragraph is either carried
through byte-for-byte or dropped with a named reason — there is no third
outcome, and no paragraph is ever rewritten, normalised or trimmed in the
middle.

What it drops, each with its reason recorded:

    page_number                a paragraph that is only a page number
    table_of_contents_link     the "Table of Contents" line on every page
    running_header             a short line the document repeats on every page
    forward_looking_boilerplate  the safe-harbour disclaimer
    empty                      a paragraph of nothing but invisible characters

What it does to tables: renders each as `|`-delimited rows, and drops the ones
whose numbers are already in the XBRL instance — because those numbers reach
the predictor as facts, with their context, and the HTML copy of them is text
the model has to read twice. A table is dropped only when **every** numeric
cell in it is a fact of that filing. Anything else is kept, which in practice
means the non-GAAP reconciliation and the guidance table, the two tables whose
numbers are nowhere in XBRL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from src import cutoff_guard, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, html_text, interpreter_pin

BAD_INPUT = 2

_PAGE_LABEL = re.compile(r"^page\s*\d{1,4}$")
_BARE_NUMBER = re.compile(r"^\d{1,4}$")
# Page numbers climb through a document, one page at a time. A bare number in a
# table does not: `2025` and `2024` sit side by side in every column heading and
# `100` is a percentage. So a bare number is a page number only when it belongs
# to a run of them that increases in document order — three or more, each a
# little larger than the last. Everything else is data and stays.
PAGE_RUN_MIN_LENGTH = 3
PAGE_RUN_MAX_STEP = 3
_TOC_LINK = re.compile(r"^table of contents$|^index$|^back to (?:table of )?contents$")
_FORWARD_LOOKING = re.compile(
    r"forward[- ]looking statements?"
    r"|private securities litigation reform act")
_SAFE_HARBOUR = re.compile(
    r"within the meaning of|safe harbor|safe harbour|section 27a|section 21e"
    r"|actual results (?:could|may|might) differ|undertake no (?:obligation|duty)")
# A running header is "the same line with a different page number on it", and
# that is the rule, literally: a short label whose digit-masked form repeats,
# and whose digits are not the same every time. `Apple Inc. | 2025 Form 10-K |
# 21` and `… | 22` are one header. `Income before income taxes`, repeated once
# per table in the same section, is not — it is a row label, and deleting it
# would take the words the numbers belong to. The rule errs towards keeping.
_DIGITS = re.compile(r"\d+")
RUNNING_HEADER_MIN_REPEATS = 3
RUNNING_HEADER_MAX_CHARS = 140
RUNNING_HEADER_MAX_WORDS = 12
# A table with one or two numbers can match XBRL by coincidence. Below this it
# is kept, whatever the numbers say.
MIN_NUMERIC_CELLS_TO_DROP = 4

_NUMERIC_CELL = re.compile(r"^\(?\s*[$€£]?\s*-?\d[\d,]*(?:\.\d+)?\s*\)?\s*%?$")
_INVISIBLE = re.compile(r"^[\s​‌‍⁠﻿]*$")


def _shape(text: str) -> str:
    return _DIGITS.sub("#", html_text.normalized(text))


def _is_label(text: str) -> bool:
    """Short enough and few enough words to be page furniture rather than prose."""
    return (len(text) <= RUNNING_HEADER_MAX_CHARS
            and len(text.split()) <= RUNNING_HEADER_MAX_WORDS)


def cell_number(cell: str):
    """The number a table cell states, or None if the cell is not a number."""
    flat = html_text.normalized_spacing(cell).replace("−", "-")
    if not _NUMERIC_CELL.match(flat) or not any(ch.isdigit() for ch in flat):
        return None
    negative = flat.startswith("(") and flat.rstrip("%").rstrip().endswith(")")
    digits = re.sub(r"[^\d.\-]", "", flat)
    try:
        value = float(digits)
    except ValueError:
        return None
    return -abs(value) if negative else value


def fact_values(facts: list[dict]) -> set[float]:
    """Every number the filing tagged, at every scale a table might print it.

    A filing tags 307003000000 and prints "307,003" in a table headed "in
    millions", so the fact is recorded at unit, thousand, million and billion
    scale and the cell is matched against all four.
    """
    values: set[float] = set()
    for fact in facts:
        number = fact.get("number")
        if number is None:
            continue
        for scale in (1.0, 1e3, 1e6, 1e9):
            values.add(round(number / scale, 6))
            values.add(round(-number / scale, 6))
    return values


def table_is_in_xbrl(table: list[list[str]], values: set[float]) -> tuple[bool, int, int]:
    """(every number is a fact, numeric cells, matched cells)."""
    numbers = [cell_number(cell) for row in table for cell in row]
    numbers = [number for number in numbers if number is not None]
    if len(numbers) < MIN_NUMERIC_CELLS_TO_DROP:
        return False, len(numbers), 0
    matched = sum(1 for number in numbers if round(number, 6) in values)
    return matched == len(numbers), len(numbers), matched


_WORD = re.compile(r"[^\W\d_]{2,}")


def _could_be_a_header(text: str) -> bool:
    """Short, a label, worded, and carrying a page number.

    The word count is what keeps the rule off table data. `(13,196)` and
    `December 29, 2025` repeat across a section's tables with different digits
    and would otherwise look exactly like a page footer; they are the numbers
    and the period headings, and they stay.
    """
    return (_is_label(text)
            and any(character.isdigit() for character in text)
            and len(_WORD.findall(text)) >= 3)


def page_numbers(paragraphs: list[str]) -> set[int]:
    """Indices of the paragraphs that are page numbers, by the run rule above."""
    candidates = [(index, int(html_text.normalized(paragraph)))
                  for index, paragraph in enumerate(paragraphs)
                  if _BARE_NUMBER.match(html_text.normalized(paragraph))]
    if not candidates:
        return set()

    # Longest chain of increasing page numbers in document order.
    best_length = [1] * len(candidates)
    came_from: list[int | None] = [None] * len(candidates)
    for here in range(len(candidates)):
        for before in range(here):
            step = candidates[here][1] - candidates[before][1]
            if 0 < step <= PAGE_RUN_MAX_STEP and best_length[before] + 1 > best_length[here]:
                best_length[here] = best_length[before] + 1
                came_from[here] = before
    end = max(range(len(candidates)), key=lambda index: best_length[index])
    if best_length[end] < PAGE_RUN_MIN_LENGTH:
        return set()

    run, cursor = set(), end
    while cursor is not None:
        run.add(candidates[cursor][0])
        cursor = came_from[cursor]
    return run


def running_headers(paragraphs: list[str]) -> set[str]:
    """The digit-masked shapes that are page furniture in this document."""
    seen: dict[str, set[str]] = {}
    counts: Counter = Counter()
    for paragraph in paragraphs:
        if not _could_be_a_header(paragraph):
            continue
        shape = _shape(paragraph)
        counts[shape] += 1
        seen.setdefault(shape, set()).add(html_text.normalized(paragraph))
    return {shape for shape, count in counts.items()
            if count >= RUNNING_HEADER_MIN_REPEATS and len(seen[shape]) >= 2}


def drop_reason(paragraph: str, headers: set[str], is_page_number: bool = False) -> str | None:
    """Why this paragraph does not belong in the input, or None to keep it."""
    if _INVISIBLE.match(paragraph):
        return "empty"
    flat = html_text.normalized(paragraph)
    if is_page_number or _PAGE_LABEL.match(flat):
        return "page_number"
    if _TOC_LINK.match(flat):
        return "table_of_contents_link"
    if _could_be_a_header(paragraph) and _shape(paragraph) in headers:
        return "running_header"
    if _FORWARD_LOOKING.search(flat) and _SAFE_HARBOUR.search(flat):
        return "forward_looking_boilerplate"
    return None


def clean_paragraphs(paragraphs: list[str]) -> dict:
    """Keep or drop, one decision per paragraph, each drop with its reason."""
    headers = running_headers(paragraphs)
    pages = page_numbers(paragraphs)
    kept, dropped = [], []
    for index, paragraph in enumerate(paragraphs):
        reason = drop_reason(paragraph, headers, index in pages)
        if reason is None:
            kept.append(paragraph)
        else:
            dropped.append({"text": paragraph, "reason": reason})
    return {"paragraphs": kept, "dropped": dropped}


def clean(html: str, *, facts: list[dict] | None = None) -> dict:
    """Clean one HTML document: paragraphs kept or dropped, tables rendered."""
    result = clean_paragraphs(html_text.paragraphs(html))
    values = fact_values(facts or [])
    tables = []
    for number, table in enumerate(html_text.tables(html), start=1):
        in_xbrl, numeric, matched = table_is_in_xbrl(table, values)
        tables.append({
            "number": number,
            "rows": html_text.pipe_rows(table),
            "cells": [cell for row in table for cell in row],
            "cell_count": sum(len(row) for row in table),
            "numeric_cells": numeric,
            "matched_cells": matched,
            "kept": not in_xbrl,
            "reason": "already in the XBRL instance" if in_xbrl else "not in XBRL",
        })
    result["tables"] = tables
    result["dropped_tables"] = sum(1 for table in tables if not table["kept"])
    return result


def clean_section(paragraphs: list[str]) -> dict:
    """Clean an already-split section, which has no tables of its own to render."""
    return clean_paragraphs(paragraphs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="drop the furniture, render the tables")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", default="10-K")
    parser.add_argument("--role", default="primary_html")
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    ticker = args.ticker.upper()
    fixtures_root = Path(args.fixtures)
    try:
        cutoff = args.cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
        row = cutoff_guard.one_document(ticker, args.form, args.role,
                                        fixtures_root=fixtures_root)
        html = cutoff_guard.load_document(row["full_path"], cutoff,
                                          fixtures_root=fixtures_root)
        facts = []
        if args.form in ("10-K", "10-Q"):
            from src import extract_numbers
            facts = extract_numbers.extract(ticker, (args.form,), cutoff=cutoff,
                                            fixtures_root=fixtures_root)["facts"]
    except cutoff_guard.CutoffGuardError as exc:
        print(f"clean_text: {exc}", file=sys.stderr)
        return BAD_INPUT

    result = clean(html, facts=facts)
    Path(args.out).write_text(json.dumps(
        {"ticker": ticker, "form": args.form, "role": args.role,
         "cutoff": str(cutoff), **result}, indent=2) + "\n", encoding="utf-8")
    print(f"clean_text: {ticker} {args.form} {args.role} "
          f"{len(result['paragraphs'])} kept, {len(result['dropped'])} dropped, "
          f"{result['dropped_tables']}/{len(result['tables'])} tables already in XBRL "
          f"→ {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
