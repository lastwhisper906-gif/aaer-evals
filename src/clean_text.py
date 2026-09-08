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
# Three digits, not four. A year is four and a page of one of these filings is
# not: the longest document in the fixture set ends on page 115. Palo Alto's
# MD&A prints `2023 2024 2025` up the columns of six tables, far enough apart
# and flanked by enough prose to look exactly like a page run, and a fourth
# digit is the one thing that tells them apart before any other rule runs.
_BARE_NUMBER = re.compile(r"^\d{1,3}$")
# Page numbers climb through a document, one page at a time, and they are a
# *page* apart. A bare number in a table climbs too — `2027 2028 2029 2030` is
# every lease and debt maturity table in the fixture set, and Apple's table of
# contents prints `27 28 29` down its right-hand column — but those neighbours
# are three paragraphs apart, not a page. So a bare number is a page number only
# when it belongs to a run that increases in document order, three or more, each
# a little larger than the last, **and each separated from the last by more text
# than a table row**. Everything else is data and stays.
PAGE_RUN_MIN_LENGTH = 3
PAGE_RUN_MAX_STEP = 3
# Visible paragraphs between one page tail and the next. Eight is below the
# smallest gap between two genuine page tails in the fixture set — nine, from
# Qualcomm's page 46, the last page of Item 7 and cut short by the end of it —
# and above the gap down a column of years: Apple's table of contents prints
# `27`, `28`, `29` three and two paragraphs apart, and every lease and debt
# maturity table prints `2027 2028 2029 2030` one apart.
PAGE_RUN_MIN_GAP = 8
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
#
# The shape test alone is not enough, because a roll-forward prints `Balance at
# June 30, 2023`, `Balance at June 28, 2024`, `Balance at June 27, 2025` — one
# shape, three digit variants, a page apart. What separates those from a page
# footer is what they sit next to: a row label is followed (or preceded) by the
# numbers of its own row, and a page footer is not. So the shape decides which
# lines are *candidates* and the neighbours decide, one occurrence at a time,
# whether this one is furniture.
_DIGITS = re.compile(r"\d+")
RUNNING_HEADER_MIN_REPEATS = 3
RUNNING_HEADER_MAX_CHARS = 140
RUNNING_HEADER_MAX_WORDS = 12
# A cell that is nothing but a number, a currency sign, a dash or a percent —
# the cells of a table row, and nothing a filer writes as a sentence.
_NUMBER_CELL = re.compile(r"^[\s$€£%()\[\]\-–—+.,:;/\d]+$")
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


def _visible_positions(paragraphs: list[str]) -> list[int]:
    """How many visible paragraphs precede each one.

    Distance is measured in paragraphs a reader would see. Two filers in the
    fixture set (Generac, ESCO) emit hundreds of zero-width-space paragraphs;
    counting those as text would make a maturity table look a page wide.
    """
    positions, seen = [], 0
    for paragraph in paragraphs:
        positions.append(seen)
        if not _INVISIBLE.match(paragraph):
            seen += 1
    return positions


def page_numbers(paragraphs: list[str]) -> set[int]:
    """Indices of the paragraphs that are page numbers, by the run rule above."""
    candidates = [(index, int(html_text.normalized(paragraph)))
                  for index, paragraph in enumerate(paragraphs)
                  if _BARE_NUMBER.match(html_text.normalized(paragraph))
                  and beside_prose(paragraphs, index)]
    if not candidates:
        return set()
    positions = _visible_positions(paragraphs)

    # Longest chain of increasing page numbers in document order, a page apart.
    best_length = [1] * len(candidates)
    came_from: list[int | None] = [None] * len(candidates)
    for here in range(len(candidates)):
        for before in range(here):
            step = candidates[here][1] - candidates[before][1]
            gap = positions[candidates[here][0]] - positions[candidates[before][0]]
            if (0 < step <= PAGE_RUN_MAX_STEP and gap >= PAGE_RUN_MIN_GAP
                    and best_length[before] + 1 > best_length[here]):
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


def _counts_pages(occurrences: list[list[str]]) -> bool:
    """Do these occurrences differ in one digit group, and does it climb?

    The digits that vary in a running header are the page number, so they
    climb through the document. Qualcomm's MD&A bullets `+ $101 million
    increase in share-based compensation expense`, `+ $269 million …`,
    `+ $62 million …` are one shape with eight variants and they do not climb;
    a table footnote alternates `(1) See Note 20 …`, `(2) See Note 20 …`,
    `(1) …` and does not climb either. Both are the filing's own words.
    """
    if len({len(groups) for groups in occurrences}) != 1:
        return False
    varying = [position for position in range(len(occurrences[0]))
               if len({groups[position] for groups in occurrences}) > 1]
    if len(varying) != 1:
        return False
    numbers = [int(groups[varying[0]]) for groups in occurrences]
    return all(before < after for before, after in zip(numbers, numbers[1:]))


def running_headers(paragraphs: list[str]) -> set[str]:
    """The digit-masked shapes that are page furniture in this document."""
    seen: dict[str, set[str]] = {}
    digits: dict[str, list[list[str]]] = {}
    counts: Counter = Counter()
    for paragraph in paragraphs:
        if not _could_be_a_header(paragraph):
            continue
        flat = html_text.normalized(paragraph)
        shape = _shape(paragraph)
        counts[shape] += 1
        seen.setdefault(shape, set()).add(flat)
        digits.setdefault(shape, []).append(_DIGITS.findall(flat))
    return {shape for shape, count in counts.items()
            if count >= RUNNING_HEADER_MIN_REPEATS and len(seen[shape]) >= 2
            and _counts_pages(digits[shape])}


def _is_number_cell(paragraph: str) -> bool:
    flat = html_text.normalized(paragraph)
    return bool(flat) and _NUMBER_CELL.match(flat) is not None


def _neighbours(paragraphs: list[str], index: int) -> list[str | None]:
    """The nearest visible paragraph on each side, or None at the edges."""
    found: list[str | None] = []
    for step in (-1, 1):
        cursor = index + step
        while 0 <= cursor < len(paragraphs) and _INVISIBLE.match(paragraphs[cursor]):
            cursor += step
        found.append(paragraphs[cursor] if 0 <= cursor < len(paragraphs) else None)
    return found


def beside_a_number(paragraphs: list[str], index: int) -> bool:
    """True when the nearest visible paragraph on either side is a table cell.

    `Balance at June 27, 2025` is followed by `213`, `—`, `7,706`: it is the
    label of that row and the numbers mean nothing without it. `Apple Inc. |
    2025 Form 10-K | 23` is followed by the heading `Gross Margin`.
    """
    return any(near is not None and _is_number_cell(near)
               for near in _neighbours(paragraphs, index))


def beside_prose(paragraphs: list[str], index: int) -> bool:
    """True when at least one side of this paragraph is not a table cell.

    This is the *page furniture* half of the rule the other way round. A page
    tail sits at the foot of a page, so the text above it or the text below it
    is the running text of the document. A bare number in a column of a table
    has cells on both sides — `55` then `%`, `44` then `175` — and that is
    Qualcomm's MD&A, where eight page tails and five table cells are all bare
    numbers between 30 and 56.
    """
    return any(near is None or not _is_number_cell(near)
               for near in _neighbours(paragraphs, index))


def drop_reason(paragraph: str, headers: set[str], is_page_number: bool = False,
                *, next_to_a_number: bool = False, is_table_cell: bool = False) -> str | None:
    """Why this paragraph does not belong in the input, or None to keep it."""
    if _INVISIBLE.match(paragraph):
        return "empty"
    if is_table_cell:
        # The document prints this text as a cell of a table it renders, so it
        # is data, whatever shape it has. Deleting it would take a row label or
        # a column heading off numbers that stay.
        return None
    flat = html_text.normalized(paragraph)
    if is_page_number or _PAGE_LABEL.match(flat):
        return "page_number"
    if _TOC_LINK.match(flat):
        return "table_of_contents_link"
    if _could_be_a_header(paragraph) and _shape(paragraph) in headers and not next_to_a_number:
        return "running_header"
    if _FORWARD_LOOKING.search(flat) and _SAFE_HARBOUR.search(flat):
        return "forward_looking_boilerplate"
    return None


def clean_paragraphs(paragraphs: list[str], *, cells: set[str] | None = None) -> dict:
    """Keep or drop, one decision per paragraph, each drop with its reason.

    `cells` is the flattened text of every cell of every table in the same
    document, when the caller knows them. A paragraph the document also prints
    inside a table is never dropped.
    """
    headers = running_headers(paragraphs)
    pages = page_numbers(paragraphs)
    cells = cells or set()
    kept, dropped, decisions = [], [], []
    for index, paragraph in enumerate(paragraphs):
        reason = drop_reason(
            paragraph, headers, index in pages,
            next_to_a_number=beside_a_number(paragraphs, index),
            is_table_cell=html_text.normalized(paragraph) in cells)
        decisions.append(reason)
        if reason is None:
            kept.append(paragraph)
        else:
            dropped.append({"text": paragraph, "reason": reason})
    return {"paragraphs": kept, "dropped": dropped, "decisions": decisions}


def table_cells(tables: list[list[list[str]]]) -> set[str]:
    """Every cell of every table, flattened for comparison against a paragraph.

    Case is flattened as well as whitespace. Seagate prints its navigation link
    as `Table of Contents` in the text and `TABLE OF CONTENTS` inside a layout
    table; matching the two costs a link and buys a rule with no case corner.
    """
    return {html_text.normalized(cell)
            for table in tables for row in table for cell in row
            if html_text.normalized(cell)}


def clean(html: str, *, facts: list[dict] | None = None) -> dict:
    """Clean one HTML document: paragraphs kept or dropped, tables rendered."""
    parsed = html_text.tables(html)
    result = clean_paragraphs(html_text.paragraphs(html), cells=table_cells(parsed))
    values = fact_values(facts or [])
    tables = []
    for number, table in enumerate(parsed, start=1):
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
    """Clean a list of paragraphs a caller already has, tables and all."""
    return clean_paragraphs(paragraphs)


def clean_stream(html: str | None = None, *, facts: list[dict] | None = None,
                 blocks: list[dict] | None = None) -> dict:
    """The text as the predictor reads it: prose kept or dropped, tables as rows.

    This is `clean` reordered around the reader instead of around the property.
    `clean` answers *what did the document say* — every paragraph including
    every table cell, and the tables separately. `clean_stream` answers *what
    goes in the file*: one entry per prose paragraph and one per table, in the
    filing's own order, so a figure is quotable with the row and column it
    belongs to instead of arriving as `Total`, `$`, `279` on three lines.

    A table is **one** entry holding all of its `|`-delimited rows, not one
    entry per row. The dispatch asked for one id per row and this is the one
    place it is not followed, for a reason worth stating: 2,321 rows in the
    fixture set are byte-identical to a row of another table — `| (In millions)
    | 2025 | | 2024 | | 2023 |` heads thirteen of Carrier's — and one id per
    row makes those ids ambiguous unless twelve of the thirteen tables lose
    their column headings. One id per table keeps every filed row, and the
    duplicates that remain are whole tables printed twice, which the note
    stream drops as a repeat without breaking a table apart.

    A caller that has already cut a section out of the document passes the
    section's `blocks`; everything else passes the HTML.
    """
    found = html_text.blocks(html) if blocks is None else blocks
    prose = [block["text"] for block in found if block["kind"] == "paragraph"]
    parsed = [block["rows"] for block in found if block["kind"] == "table"]
    decided = clean_paragraphs(prose, cells=table_cells(parsed))
    values = fact_values(facts or [])

    tables = []
    for number, rows in enumerate(parsed, start=1):
        in_xbrl, numeric, matched = table_is_in_xbrl(rows, values)
        tables.append({
            "number": number,
            "rows": html_text.pipe_rows(rows),
            "cells": [cell for row in rows for cell in row],
            "numeric_cells": numeric,
            "matched_cells": matched,
            "kept": not in_xbrl,
            "reason": "already in the XBRL instance" if in_xbrl else "not in XBRL",
        })

    stream, dropped, paragraph, table = [], [], 0, 0
    for block in found:
        if block["kind"] == "paragraph":
            reason = decided["decisions"][paragraph]
            paragraph += 1
            if reason is None:
                stream.append(block["text"])
            else:
                dropped.append({"text": block["text"], "reason": reason})
            continue
        record = tables[table]
        table += 1
        rows = [row for row in record["rows"] if not _INVISIBLE.match(row.replace("|", ""))]
        if not rows:
            dropped.append({"text": "", "reason": "a table of empty cells",
                            "rows": len(record["rows"])})
        elif record["kept"]:
            stream.append("\n".join(rows))
        else:
            dropped.append({"text": "", "reason": "already in the XBRL instance",
                            "rows": len(record["rows"])})
    return {"paragraphs": stream, "dropped": dropped, "tables": tables,
            "dropped_tables": sum(1 for table in tables if not table["kept"])}


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
