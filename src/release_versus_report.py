"""The earnings release printed beside the report, line by line.

The release (8-K exhibit 99.1) is furnished, not filed, and carries less
liability than the 10-Q or 10-K that follows it. A practitioner's first check is
therefore to set what the release prints for a line beside what the report tags
for the same period. This module does the setting-beside; the calculator hands
it the report's side as a reader and puts the result in `calculator.json` as
`release_versus_report`.

**What it reads.** The paragraphs of the release as `src/parse_8k.py` builds them
(`parse_8k.earnings_release`, the structure `input_8k.md` is written from): a
table is one paragraph of pipe rows, with the paragraph's id. Nothing here parses
`input_8k.md` as text.

**Which row is which line.** `ROW_LABELS` states, per line, the row labels the
line is read from, each compared whole (case, spacing, dashes and a trailing
footnote mark aside) and never as a fragment. Every label is confirmed in a
committed release (`tests/test_release_versus_report.py`), and a label that two
lines both claim is refused when this file is imported (`refuse_shared_labels`).
A line none of whose labels is in any table of the release is `not_in_release`:
the release prints no row under a label this file states, which is a statement
about the labels as much as about the release.

**Which column is which period.** A table says its columns in its header rows:
a span ("Three Months Ended", also run together as "EndedJune 30,") and a date. The
two are read only where the header says both, the date is the report's own period
end, and the count of numbers in a row equals the count of columns the header names
(a "Change" or "% of" column is a column). A table whose header does not say so --
"Q2 FY27", a guidance table, a segment table with segments for columns -- is not
read, and it keeps the line from `agrees`: `period_not_read`, with the reason. A unit
(in millions, in thousands) comes from the table's own header or a table before it,
or from a title line that is only that statement; a sentence that mentions millions
is not a unit, and none is ever assumed.

**Every table votes.** For a line and a span, every table of the release that prints
it is compared, each row of it, each cell at its own table's printed precision, and
each is listed with its paragraph id. The line is `differs` if any cell differs and
`agrees` only if every cell agrees (`PRECEDENCE`: `differs`, then a cell no one could
say was GAAP, then a report fact that is not there, then a table that could not be
read, then `agrees`). Left out of a dollar line, and listed under `excluded_rows`:
rows under a per share, shares, percent or component heading, and rows whose figure is
printed as a percent. A table under a short heading that names no statement
(`is_segment_heading`: "Climate Solutions Americas (CSA)") is a segment's, listed
under `segment_cells_not_compared`.

**GAAP and non-GAAP.** A heading or header cell that says non-GAAP or adjusted
(`NON_GAAP_WORDS`) makes its block `non_gaap`: listed under `not_gaap` and not held to
the report. One that says both, or two side-by-side blocks nothing names, are
`unidentified`: `block_not_identified`, never `agrees`. A row label that says GAAP is
GAAP wherever it sits, and a non-GAAP total row closes the block its heading opened.

**Agreement is at the release's own precision.** A release printing `4,133` in
millions has a step of one million, and agrees with every report fact that
rounds, half up, to 4,133 million; a release printing `1,570.7` has a step of a
tenth of a million; per-share figures step by the decimals printed. A cash
outflow printed in parentheses is compared by its size, as the taxonomy states a
payment. A net income row not labelled "attributable" is also held to the report's
`ProfitLoss` (net income before the noncontrolling interest) and says so. The
difference is the release's value less the report's, in dollars, and `sign` says
which way: `release_larger`, `release_smaller` or `equal`.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import ROUND_HALF_UP, Decimal

LINES = ("revenue", "cost_of_revenue", "operating_income", "pretax_income",
         "income_tax_expense", "net_income", "diluted_earnings_per_share",
         "operating_cash_flow", "capital_expenditure")

# Which row labels are which line. Each label is in a committed release
# (`tests/test_release_versus_report.py` finds it there). "Sales" alone, "Diluted"
# alone and the labels that print an expense with the opposite sign
# ("Income tax (expense) benefit") are left out on purpose.
ROW_LABELS: dict[str, tuple[str, ...]] = {
    "revenue": ("Net revenue", "Total net revenue", "Net sales", "Total net sales",
                "Revenue", "Total revenue", "Revenues", "Total revenues"),
    "cost_of_revenue": ("Cost of revenue", "Total cost of revenue", "Cost of revenues",
                        "Cost of sales", "Total cost of sales", "Total cost of goods sold",
                        "Costs of goods sold"),
    "operating_income": ("Operating income", "Income from operations", "Operating income (loss)",
                         "Operating profit", "GAAP operating income",
                         "GAAP income from operations"),
    "pretax_income": ("Income before income taxes", "Income before provision for income taxes",
                      "Earnings before income taxes", "Income before income tax",
                      "Income from continuing operations before income taxes",
                      "Earnings before taxes (EBT)"),
    "income_tax_expense": ("Income tax expense", "Provision for income taxes",
                           "Income tax provision", "Income tax (benefit) expense"),
    "net_income": ("Net income", "Net earnings", "Net income (loss)", "Net earnings (loss)",
                   "GAAP net income", "Net income (GAAP)",
                   "Net income attributable to Generac Holdings Inc.",
                   "Net income attributable to Johnson Controls",
                   "Net earnings (loss) attributable to common shareowners"),
    "diluted_earnings_per_share": ("Diluted earnings per share", "Earnings per share - diluted",
                                   "Diluted EPS", "GAAP diluted EPS",
                                   "GAAP diluted net income per share",
                                   "Diluted earnings per share (EPS)",
                                   "GAAP net income per share, diluted"),
    "operating_cash_flow": ("Net cash provided by operating activities",
                            "Change in cash from operating activities",
                            "Net cash flows provided by operating activities",
                            "Cash generated by operating activities",
                            "GAAP net cash provided by operating activities"),
    "capital_expenditure": ("Capital expenditures", "Purchases of property and equipment",
                            "Purchases of property, plant, and equipment",
                            "Expenditures for property and equipment",
                            "Payments for acquisition of property, plant and equipment"),
}

PER_SHARE = ("diluted_earnings_per_share",)
BY_SIZE = ("capital_expenditure",)        # printed in parentheses as an outflow


class ReleaseLabelError(Exception):
    """A label belongs to two lines, so a row under it would be two things."""


_DASHES = str.maketrans({"—": "-", "–": "-", "‐": "-", "‑": "-",
                         "−": "-", "’": "'", "​": ""})
_FOOTNOTE = re.compile(r"(?:\s*\((?:\d{1,2}|[a-z])\)|\s*\*+)+$")


def normal_label(text: str) -> str:
    """A row label as it is compared: lower case, one space, plain dashes, no
    trailing footnote mark or colon."""
    text = text.translate(_DASHES).strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = _FOOTNOTE.sub("", text).rstrip(":").strip()
    return text


def label_owners(table: dict[str, tuple[str, ...]]) -> dict[str, list[str]]:
    owners: dict[str, list[str]] = {}
    for line, labels in table.items():
        for label in labels:
            owners.setdefault(normal_label(label), [])
            if line not in owners[normal_label(label)]:
                owners[normal_label(label)].append(line)
    return owners


def refuse_shared_labels(table: dict[str, tuple[str, ...]]) -> dict[str, str]:
    """label -> line, or `ReleaseLabelError` naming a label two lines claim."""
    shared = {label: lines for label, lines in label_owners(table).items() if len(lines) > 1}
    if shared:
        named = "; ".join(f"{label!r} is claimed by {', '.join(lines)}"
                          for label, lines in sorted(shared.items()))
        raise ReleaseLabelError(f"a row label cannot be two lines: {named}")
    return {label: lines[0] for label, lines in label_owners(table).items()}


LINE_OF_LABEL = refuse_shared_labels(ROW_LABELS)


# --- the cells --------------------------------------------------------------------

_NUMBER = re.compile(r"^\(?\$?\s*\(?(-?[\d,]*\d(?:\.\d+)?)\)?\s*(?:%|bps?|pts?|x)?\)?$", re.I)
_DASH_ONLY = re.compile(r"^\$?\s*[-—–]+\s*%?$")
_SKIPPED = {"", "$", "%", ")", "(", "bp", "bps", "pt", "pts", "x"}


def read_number(text: str) -> tuple[Decimal, int] | None:
    """A printed figure as a number and its printed decimals, or None.

    Parentheses and a leading minus are negative; a lone dash is zero. A cell
    that is not a figure (a label, a date, a year) is None.
    """
    cell = text.translate(_DASHES).strip()
    if cell.lower() in _SKIPPED:
        return None
    if _DASH_ONLY.match(cell):
        return Decimal(0), 0
    found = _NUMBER.match(cell)
    if not found:
        return None
    body = found.group(1).replace(",", "")
    negative = body.startswith("-") or cell.lstrip("$ ").startswith("(")
    value = Decimal(body.lstrip("-"))
    decimals = len(body.split(".")[1]) if "." in body else 0
    return (-value if negative else value), decimals


def _is_year(text: str) -> bool:
    return bool(re.fullmatch(r"(?:19|20)\d\d\**", text.strip()))


def cells_of(row: str) -> list[str]:
    """The cells of one pipe row, as `html_text.pipe_rows` wrote them."""
    return row[2:-2].split(" | ") if row.startswith("| ") and row.endswith(" |") else [row]


# --- the header ---------------------------------------------------------------------

_MONTH = ("jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|"
          "sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?")
# A header cell may run its words together ("Six Months EndedJune 30,"), so a month
# is also read straight after the word "ended".
_DATE = re.compile(rf"(?:(?<![A-Za-z])|(?<=[Ee]nded))({_MONTH})\.?\s*(\d{{1,2}})"
                   rf"(?:\s*,\s*((?:19|20)\d\d))?(?!\d)", re.I)
_SPAN = re.compile(r"\b(three|six|nine|twelve)\s+months?\s+ended|"
                   r"\b(?:fiscal\s+)?(quarter|years?)\s+ended", re.I)
_MONTHS_OF = {"three": 3, "six": 6, "nine": 9, "twelve": 12, "quarter": 3, "year": 12, "years": 12}
_CHANGE = re.compile(r"change|chg|variance|y-?t-?y|y/y|q/q|yoy|qoq|growth|percent|% of", re.I)
_UNIT = re.compile(r"\bin\s+(thousands|millions|billions)\b", re.I)
_SCALE = {"thousands": 1_000, "millions": 1_000_000, "billions": 1_000_000_000}

# Which words say a block of a table is not the GAAP statement. A heading or header
# cell with one of these and no plain "GAAP" is non-GAAP; with both it is not
# identified; with plain "GAAP" alone it is GAAP; a table that says neither and
# repeats no column is read as the statement it looks like.
NON_GAAP_WORDS = ("non-gaap", "non gaap", "nongaap", "adjusted", "pro forma", "excluding")
_GAAP_WORD = re.compile(r"\bgaap\b")
# A heading whose rows are not the line in dollars: per share, shares, percent, or the
# components of an expense (a summary of share-based compensation by function).
NOT_DOLLARS = re.compile(r"per (?:common )?(?:share|unit)|earnings per|^basic\b|^diluted\b|"
                         r"\bshares\b|percent|% of|\bmargin\b|\bratio\b|"
                         r"summary of|compensation|by (?:segment|region|product)|of which|"
                         r"included in")


def _month_number(name: str) -> int:
    return ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov",
            "dec"].index(name[:3].lower()) + 1


def unit_statement(text: str) -> str | None:
    found = _UNIT.search(text)
    return found.group(1).lower() if found else None


def block_of(text: str) -> str | None:
    """`gaap`, `non_gaap` or `unidentified` for a heading or header cell that names one,
    else None."""
    words = re.sub(r"non[-\s]+gaap", "non-gaap", normal_label(text))
    non = any(word in words for word in NON_GAAP_WORDS)
    plain = bool(_GAAP_WORD.search(words.replace("non-gaap", "")))
    if non and plain:
        return "unidentified"
    return "non_gaap" if non else ("gaap" if plain else None)


# A paragraph that is only a unit statement, as a statement's title line prints it:
# "(In millions, except per share amounts)". A sentence that mentions millions is not
# one, so a unit never comes from prose.
_TITLE_UNIT = re.compile(r"^\(?[^.\d]{0,100}\bin (thousands|millions|billions)\b[^.\d]{0,80}\)?$",
                         re.I)

# A short heading above a table that names none of these is a segment's or a product's
# ("Climate Solutions Americas (CSA)"): the table's rows are that part of the company's,
# not the line, and are listed and not compared.
STATEMENT_WORDS = ("consolidated", "condensed", "statement", "results", "summary",
                   "reconciliation", "balance", "cash flow", "income", "operations",
                   "financial", "guidance", "outlook", "gaap", "unaudited", "total",
                   "revenue", "earnings", "highlights", "supplemental")


def is_segment_heading(text: str | None) -> bool:
    if not text:
        return False
    words = text.strip()
    if len(words.split()) > 12 or re.search(r"\d|[.:;]", words):
        return False
    return not any(word in words.lower() for word in STATEMENT_WORDS)


class Unread(Exception):
    """A table, or one of its rows, that cannot be read; the message is the reason."""


def _tokens(cells: list[str]) -> list[tuple]:
    out = []
    for cell in cells:
        text = cell.strip()
        if not text:
            continue
        date = _DATE.search(text)
        if date:
            out.append(("date", _month_number(date.group(1)), int(date.group(2)),
                        int(date.group(3)) if date.group(3) else None))
        elif _is_year(text):
            out.append(("year", int(text.rstrip("*"))))
        elif _CHANGE.search(text) and not _SPAN.search(text) and not _UNIT.search(text):
            out.append(("change",))
    return out


def _is_data_row(cells: list[str]) -> bool:
    filled = [cell.strip() for cell in cells if cell.strip()]
    if not filled or read_number(filled[0]) is not None:
        return False
    return any(read_number(cell) is not None and not _is_year(cell) for cell in filled[1:])


def _assign_blocks(columns: list[dict], labels: list[str]) -> None:
    """Say which block each column belongs to: by the header's own group labels, shared
    out over the columns in order; with none, a table that repeats a column is two
    blocks nothing names, and a table that does not is the statement."""
    count = len(columns)
    keys = [(c.get("months"), c.get("end")) for c in columns if "change" not in c]
    for index, column in enumerate(columns):
        if labels and len(labels) > 1 and count % len(labels) == 0:
            column["block"] = labels[index // (count // len(labels))]
        elif labels and len(labels) > 1:
            column["block"] = "unidentified"
        elif labels:
            column["block"] = labels[0]
        elif "change" not in column and keys.count((column["months"], column["end"])) > 1:
            column["block"] = "unidentified"
        else:
            column["block"] = "gaap"


def read_header(rows: list[list[str]]) -> dict:
    """The columns a table's header names, or `Unread`.

    Returns `columns` (each `change` or a period with `months`, `end` and `block`),
    `first_data_row` and `unit` (the table's own unit statement, or None).
    """
    first = next((index for index, cells in enumerate(rows) if _is_data_row(cells)), None)
    if first is None or first == 0:
        raise Unread("the table has no header rows above its first row of figures")
    header = rows[:first]
    unit = next((u for cells in header for cell in cells if (u := unit_statement(cell))), None)
    labels = [b for cells in header for cell in cells if cell.strip() and (b := block_of(cell))]

    # Spans: a cell that says "Three Months Ended" (with or without its date).
    spans = []
    for cells in header:
        for cell in cells:
            found = _SPAN.search(cell)
            if found:
                spans.append(_MONTHS_OF[(found.group(1) or found.group(2)).lower()])

    # The cells that carry a whole column in one cell: span and a date with its year.
    whole = []
    for cells in header:
        for cell in cells:
            span, date = _SPAN.search(cell), _DATE.search(cell)
            if span and date and date.group(3):
                whole.append({"months": _MONTHS_OF[(span.group(1) or span.group(2)).lower()],
                              "end": dt.date(int(date.group(3)), _month_number(date.group(1)),
                                             int(date.group(2)))})
    if whole:
        _assign_blocks(whole, labels)
        return {"columns": whole, "first_data_row": first, "unit": unit}

    token_rows = [_tokens(cells) for cells in header]
    numbered = [index for index, tokens in enumerate(token_rows) if len(tokens) >= 2]
    if not numbered:
        raise Unread("the header names no dates: its columns are not dated periods")
    last = numbered[-1]
    columns = list(token_rows[last])
    earlier = [token for tokens in token_rows[:last] for token in tokens if token[0] == "date"]

    resolved: list[dict | None] = [None] * len(columns)
    for index, column in enumerate(columns):
        if column[0] == "change":
            resolved[index] = {"change": True}
        elif column[0] == "date" and column[3] is not None:
            resolved[index] = {"end": dt.date(column[3], column[1], column[2])}
    year_columns = [index for index, column in enumerate(columns) if column[0] == "year"]
    if year_columns:
        sources = [token for token in earlier if token[3] is None]
        # one month and day for every year, or one for each run of years that
        # follows it ("Three Months Ended June 30," over two years, then "Six
        # Months Ended June 30," over the next two)
        if sources and len(year_columns) % len(sources) == 0:
            sources = [token for token in sources
                       for _ in range(len(year_columns) // len(sources))]
        if len(sources) != len(year_columns):
            raise Unread("the header's month and day cannot be paired with its years")
        for index, source in zip(year_columns, sources):
            resolved[index] = {"end": dt.date(columns[index][1], source[1], source[2])}
    if any(column is None for column in resolved):
        raise Unread("the header's dates are not all complete")

    count = len(resolved)
    if not spans:
        raise Unread("the header does not say how long the columns' periods are")
    if len(spans) > 1 and count % len(spans):
        raise Unread("the header's spans cannot be shared out over its columns")
    size = count // len(spans) if len(spans) > 1 else count
    for index, column in enumerate(resolved):
        column["months"] = spans[min(index // size, len(spans) - 1)] if len(spans) > 1 else spans[0]
    _assign_blocks(resolved, labels)
    return {"columns": resolved, "first_data_row": first, "unit": unit}


# --- the cells of a release -------------------------------------------------------------

def _step(scale: int, decimals: int) -> Decimal:
    return Decimal(scale) / (Decimal(10) ** decimals)


def agrees_at_the_release_precision(release: Decimal, report: float, scale: int,
                                    decimals: int) -> bool:
    """True when the report fact, rounded half up to the release's own step, is the
    figure the release printed."""
    step = _step(scale, decimals)
    printed = release * Decimal(scale) / step
    return (Decimal(str(report)) / step).quantize(Decimal(1), rounding=ROUND_HALF_UP) == printed


def _rows_of(paragraph: str) -> list[list[str]] | None:
    lines = paragraph.split("\n")
    if not lines or not all(line.startswith("| ") and line.endswith(" |") for line in lines):
        return None
    return [cells_of(line) for line in lines]


def _label_of(cells: list[str]) -> tuple[int, str] | None:
    for index, cell in enumerate(cells):
        if cell.strip():
            return index, cell.strip()
    return None


def _sign(difference: Decimal) -> str:
    return "equal" if difference == 0 else ("release_larger" if difference > 0
                                            else "release_smaller")


def _figures(cells: list[str]) -> list[dict]:
    """The figures of a row after its label, each with whether it is printed as a percent
    (a `%` in the cell or a standalone `%` cell after it)."""
    out = []
    for index, cell in enumerate(cells):
        found = read_number(cell)
        if found is None:
            if cell.strip() == "%" and out:
                out[-1]["percent"] = True
            continue
        out.append({"text": cell.strip(), "value": found[0], "decimals": found[1],
                    "percent": "%" in cell})
    return out


def read_cells(paragraph_ids: list[str], paragraphs: list[str], period_end: str) -> dict:
    """Every cell of every table of the release that is one of the lines, for the period.

    Returns `cells` (each with its line, span, label, text, value, scale, decimals,
    paragraph id and block), `unread` (line -> tables and rows that could not be read,
    with the reason), `excluded` (rows left out as per share or percent) and
    `seen` (the lines some table has a row for).
    """
    end = dt.date.fromisoformat(period_end)
    cells, unread, excluded, seen, segments = [], {}, [], set(), []
    last_unit, above = None, None
    for paragraph_id, paragraph in zip(paragraph_ids, paragraphs):
        rows = _rows_of(paragraph)
        if rows is None:
            title = _TITLE_UNIT.match(paragraph.strip())
            last_unit = unit_statement(paragraph) if title else last_unit
            above = None if title else paragraph   # prose is not a table's unit; a title line is
            continue
        heading, above = above, None
        carried = last_unit
        for row in rows:
            last_unit = unit_statement(" ".join(row)) or last_unit

        def note(line, label, reason):
            unread.setdefault(line, []).append({"paragraph_id": paragraph_id, "label": label,
                                                "reason": reason})

        def matched(row):
            placed = _label_of(row)
            line = LINE_OF_LABEL.get(normal_label(placed[1])) if placed else None
            return line if line and any(read_number(c) is not None
                                        for c in row[placed[0] + 1:]) else None

        if not any(matched(row) for row in rows):
            continue
        try:
            header = read_header(rows)
        except Unread as reason:
            for row in rows:
                if matched(row):
                    note(matched(row), _label_of(row)[1], str(reason))
                    seen.add(matched(row))
            continue
        columns = header["columns"]
        scale_name = header["unit"] or carried
        row_block, not_dollars, reset_block = None, False, False
        for index, row in enumerate(rows):
            if index < header["first_data_row"]:
                continue
            placed = _label_of(row)
            if placed is None:
                continue
            if reset_block:
                row_block, reset_block = None, False
            if _is_data_row(row) and block_of(placed[1]) == "non_gaap":
                reset_block = True      # a non-GAAP total closes the block its heading opened
            line = matched(row)
            if not _is_data_row(row) and not line:
                # a heading: it says which block, and whether the rows under it are dollars
                row_block = block_of(placed[1]) or row_block
                not_dollars = bool(NOT_DOLLARS.search(normal_label(placed[1])))
                continue
            if not line:
                continue
            seen.add(line)
            figures = _figures(row[placed[0] + 1:])
            if not_dollars and line not in PER_SHARE:
                excluded.append({"paragraph_id": paragraph_id, "label": placed[1],
                                 "cell": figures[0]["text"] if figures else "",
                                 "reason": "a per share, share count or percent row"})
                continue
            if len(figures) != len(columns):
                note(line, placed[1], f"the row prints {len(figures)} figures and the header "
                                      f"names {len(columns)} columns")
                continue
            if line not in PER_SHARE and scale_name is None:
                note(line, placed[1], "no unit statement (in millions, in thousands) is "
                                      "printed for the table or a table before it")
                continue
            for column, figure in zip(columns, figures):
                if "change" in column or column["end"] != end:
                    continue
                if line not in PER_SHARE and figure["percent"]:
                    excluded.append({"paragraph_id": paragraph_id, "label": placed[1],
                                     "cell": figure["text"], "span_months": column["months"],
                                     "reason": "a per share, share count or percent row"})
                    continue
                scale = 1 if line in PER_SHARE else _SCALE[scale_name]
                if is_segment_heading(heading):
                    segments.append({"line": line, "span_months": column["months"],
                                     "paragraph_id": paragraph_id, "label": placed[1],
                                     "cell": figure["text"], "heading": heading.strip()})
                    continue
                cells.append({
                    "line": line, "months": column["months"], "paragraph_id": paragraph_id,
                    "label": placed[1], "cell": figure["text"], "value": figure["value"],
                    "decimals": figure["decimals"], "scale_value": scale,
                    "block": block_of(placed[1]) or row_block or column["block"],
                    "release": {"label": placed[1], "cell": figure["text"],
                                "paragraph_id": paragraph_id,
                                "scale": "dollars" if line in PER_SHARE else scale_name,
                                "printed_decimals": figure["decimals"],
                                "value": float(figure["value"] * scale)}})
    return {"cells": cells, "unread": unread, "excluded": excluded, "seen": seen,
            "segments": segments}


# The order a line's verdict is taken in: a difference anywhere is the line's, a cell no
# one could say was GAAP, a report fact that is not there, or a table that could not be
# read each keep the line from `agrees`.
PRECEDENCE = ("differs", "block_not_identified", "report_fact_missing", "period_not_read",
              "agrees")


def line_verdict(verdicts) -> str:
    """The most important of the verdicts of a line's cells and unread tables."""
    present = set(verdicts)
    return next((name for name in PRECEDENCE if name in present), "not_in_release")


def compare(paragraph_ids: list[str], paragraphs: list[str], period_end: str, read_report) -> dict:
    """Every line of `LINES`, every table's cell beside the report's fact.

    `read_report(line, months)` is the calculator's: the report's cell for that
    line over a span of `months` ending on the period end, or `{"missing": why}`.
    A net income printed without "attributable" is also held to the report's
    `net_income_with_noncontrolling` where the record carries it.
    """
    read = read_cells(paragraph_ids, paragraphs, period_end)
    reports: dict[tuple[str, int], dict] = {}

    def report(line: str, months: int) -> dict:
        if (line, months) not in reports:
            reports[(line, months)] = read_report(line, months)
        return reports[(line, months)]

    out = {}
    for line in LINES:
        compared, not_gaap = [], []
        for cell in (c for c in read["cells"] if c["line"] == line):
            entry = {"span_months": cell["months"], "period_end": period_end,
                     "release": cell["release"]}
            if cell["block"] == "non_gaap":
                entry["verdict"] = "not_gaap"
                not_gaap.append(entry)
                continue
            if cell["block"] == "unidentified":
                entry["verdict"] = "block_not_identified"
                compared.append(entry)
                continue
            fact = report(line, cell["months"])
            if "missing" in fact:
                entry.update(verdict="report_fact_missing", report={"missing": fact["missing"]})
                compared.append(entry)
                continue
            shown = abs(cell["value"]) if line in BY_SIZE else cell["value"]
            scale, decimals = cell["scale_value"], cell["decimals"]
            agrees = agrees_at_the_release_precision(shown, fact["value"], scale, decimals)
            held_to = fact
            if not agrees and line == "net_income" and "attributable" not in cell["label"].lower():
                other = report("net_income_with_noncontrolling", cell["months"])
                if "missing" not in other and agrees_at_the_release_precision(
                        shown, other["value"], scale, decimals):
                    agrees, held_to = True, other
                    entry["agrees_with"] = ("net income including the noncontrolling interest, "
                                            "which a row not labelled attributable prints")
            difference = shown * scale - Decimal(str(held_to["value"]))
            entry.update(report=held_to, difference=float(difference), sign=_sign(difference),
                         verdict="agrees" if agrees else "differs")
            compared.append(entry)
        verdicts = [e["verdict"] for e in compared] + (
            ["period_not_read"] if line in read["unread"] else [])
        if compared or line in read["unread"]:
            out[line] = {"verdict": line_verdict(verdicts), "comparisons": compared}
            if line in read["unread"]:
                out[line]["unread"] = read["unread"][line]
        elif not_gaap:
            out[line] = {"verdict": "not_gaap", "comparisons": []}
        elif line in read["seen"]:
            out[line] = {"verdict": "period_not_read", "comparisons": [],
                         "reason": f"a table prints the line, and none of its columns is the "
                                   f"period ending {period_end}"}
        else:
            out[line] = {"verdict": "not_in_release",
                         "reason": "no table of the release prints a row under one of the "
                                   "stated labels",
                         "labels": list(ROW_LABELS[line])}
        if not_gaap:
            out[line]["not_gaap"] = not_gaap
        parts = [e for e in read["segments"] if e["line"] == line]
        if parts:
            out[line]["segment_cells_not_compared"] = parts
        excluded = [e for e in read["excluded"]
                    if LINE_OF_LABEL.get(normal_label(e["label"])) == line]
        if excluded:
            out[line]["excluded_rows"] = excluded
    return out
