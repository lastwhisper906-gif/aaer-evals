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
a span ("Three Months Ended") and a date. The two are read only where the header
says both, the date is the report's own period end, and the count of numbers in
a row equals the count of columns the header names (a "Change" column is a
column). A table whose header does not say so -- "Q2 FY27", a guidance table,
a segment table with segments for columns -- is not read, and a line that has a
label in an unread table and in no readable one is `period_not_read`, with the
reason, never `not_in_release`. Where one table prints the same span twice (a
GAAP block and a non-GAAP block side by side), the first is the one read.

**Which table decides.** For one line and one span, the first table in the
release's own order that can be read. Later tables that print the same line and
span at another value are listed beside it, `later_cells_that_differ`, and do
not vote: a segment table prints its segment's "Net sales" under the same label.
Inside the deciding table the line agrees if any row under one of its labels
agrees.

**Agreement is at the release's own precision.** A release printing `4,133` in
millions has a step of one million, and agrees with every report fact that
rounds, half up, to 4,133 million; a release printing `1,570.7` has a step of a
tenth of a million; per-share figures step by the decimals printed. A cash
outflow printed in parentheses is compared by its size, as the taxonomy states a
payment. The difference is the release's value less the report's, in dollars,
and `sign` says which way: `release_larger`, `release_smaller` or `equal`.
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
_DATE = re.compile(rf"\b({_MONTH})\.?\s+(\d{{1,2}})(?:\s*,\s*((?:19|20)\d\d))?\b", re.I)
_SPAN = re.compile(r"\b(three|six|nine|twelve)\s+months?\s+ended\b|"
                   r"\b(?:fiscal\s+)?(quarter|years?)\s+ended\b", re.I)
_MONTHS_OF = {"three": 3, "six": 6, "nine": 9, "twelve": 12, "quarter": 3, "year": 12, "years": 12}
_CHANGE = re.compile(r"change|chg|variance|y-?t-?y|y/y|q/q|yoy|qoq|growth|percent", re.I)
_UNIT = re.compile(r"\bin\s+(thousands|millions|billions)\b", re.I)
_SCALE = {"thousands": 1_000, "millions": 1_000_000, "billions": 1_000_000_000}


def _month_number(name: str) -> int:
    return ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov",
            "dec"].index(name[:3].lower()) + 1


def unit_statement(text: str) -> str | None:
    found = _UNIT.search(text)
    return found.group(1).lower() if found else None


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


def read_header(rows: list[list[str]]) -> dict:
    """The columns a table's header names, or `Unread`.

    Returns `columns` (each `change` or a period with `months` and `end`),
    `first_data_row` and `unit` (the table's own unit statement, or None).
    """
    first = next((index for index, cells in enumerate(rows) if _is_data_row(cells)), None)
    if first is None or first == 0:
        raise Unread("the table has no header rows above its first row of figures")
    header = rows[:first]
    unit = next((u for cells in header for cell in cells if (u := unit_statement(cell))), None)

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
    return {"columns": resolved, "first_data_row": first, "unit": unit}


# --- the comparison -------------------------------------------------------------------

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


def compare(paragraph_ids: list[str], paragraphs: list[str], period_end: str, read_report) -> dict:
    """Every line of `LINES`, the release's cell beside the report's fact.

    `read_report(line, months)` is the calculator's: the report's cell for that
    line over a span of `months` ending on the period end, or `{"missing": why}`.
    """
    end = dt.date.fromisoformat(period_end)
    decided: dict[tuple[str, int], dict] = {}
    later: dict[tuple[str, int], list] = {}
    unread: dict[str, dict] = {}
    seen_labels: set[str] = set()
    scale_before = None

    for paragraph_id, paragraph in zip(paragraph_ids, paragraphs):
        rows = _rows_of(paragraph)
        if rows is None:
            scale_before = unit_statement(paragraph) or scale_before
            continue
        matched = []
        for cells in rows:
            placed = _label_of(cells)
            line = LINE_OF_LABEL.get(normal_label(placed[1])) if placed else None
            if line and any(read_number(cell) is not None for cell in cells[placed[0] + 1:]):
                matched.append((line, placed, cells))
        scale_here = scale_before
        for cells in rows:
            scale_before = unit_statement(" ".join(cells)) or scale_before
        if not matched:
            continue
        for line, placed, _ in matched:
            seen_labels.add(line)
        try:
            header = read_header(rows)
        except Unread as reason:
            for line, placed, _ in matched:
                unread.setdefault(line, {"paragraph_id": paragraph_id, "label": placed[1],
                                         "reason": str(reason)})
            continue
        scale_name = header["unit"] or scale_here
        columns = header["columns"]
        for line, placed, cells in matched:
            figures = [read_number(cell) for cell in cells[placed[0] + 1:]]
            figures = [(cell, found) for cell, found in
                       zip(cells[placed[0] + 1:], figures) if found is not None]
            if len(figures) != len(columns):
                unread.setdefault(line, {
                    "paragraph_id": paragraph_id, "label": placed[1],
                    "reason": f"the row prints {len(figures)} figures and the header names "
                              f"{len(columns)} columns"})
                continue
            if line not in PER_SHARE and scale_name is None:
                unread.setdefault(line, {"paragraph_id": paragraph_id, "label": placed[1],
                                         "reason": "no unit statement (in millions, in "
                                                   "thousands) is printed for the table"})
                continue
            blocks = set()
            for column, (text, (value, decimals)) in zip(columns, figures):
                if "change" in column or column["end"] != end:
                    continue
                key = (line, column["months"])
                if (paragraph_id, key) in blocks:
                    continue                      # a second block of the same span: not read
                blocks.add((paragraph_id, key))
                scale = 1 if line in PER_SHARE else _SCALE[scale_name]
                cell = {"label": placed[1], "cell": text.strip(), "paragraph_id": paragraph_id,
                        "scale": "dollars" if line in PER_SHARE else scale_name,
                        "printed_decimals": decimals,
                        "value": float(value * scale)}
                if key in decided:
                    if decided[key]["paragraph_id"] == paragraph_id:
                        decided[key]["rows"].append((value, decimals, scale, cell))
                    elif not any(agrees_at_the_release_precision(
                            first_value, float(value * scale), first_scale, first_decimals)
                            for first_value, first_decimals, first_scale, _ in
                            decided[key]["rows"]):
                        later.setdefault(key, []).append(cell)
                else:
                    decided[key] = {"paragraph_id": paragraph_id,
                                    "rows": [(value, decimals, scale, cell)]}

    out = {}
    for line in LINES:
        spans = sorted(months for (name, months) in decided if name == line)
        comparisons = []
        for months in spans:
            entry = decided[(line, months)]
            results = []
            for value, decimals, scale, cell in entry["rows"]:
                shown = abs(value) if line in BY_SIZE else value
                report = read_report(line, months)
                if "missing" in report:
                    results.append({"span_months": months, "period_end": period_end,
                                    "release": cell, "verdict": "report_fact_missing",
                                    "report": {"missing": report["missing"]}})
                    continue
                difference = shown * scale - Decimal(str(report["value"]))
                verdict = ("agrees" if agrees_at_the_release_precision(
                    shown, report["value"], scale, decimals) else "differs")
                results.append({"span_months": months, "period_end": period_end,
                                "release": cell, "report": report,
                                "difference": float(difference), "sign": _sign(difference),
                                "verdict": verdict})
            # inside the deciding table the line agrees if any row of it agrees
            pick = (next((r for r in results if r["verdict"] == "agrees"), None)
                    or results[0])
            others = [r["release"] for r in results if r is not pick]
            if others:
                pick = dict(pick, other_rows_of_the_same_table=others)
            if later.get((line, months)):
                pick = dict(pick, later_cells_that_differ=later[(line, months)])
            comparisons.append(pick)
        if comparisons:
            verdicts = {c["verdict"] for c in comparisons}
            verdict = next(name for name in ("differs", "agrees", "report_fact_missing")
                           if name in verdicts)
            out[line] = {"verdict": verdict, "comparisons": comparisons}
        elif line in unread:
            out[line] = {"verdict": "period_not_read", **unread[line]}
        elif line in seen_labels:
            out[line] = {"verdict": "period_not_read",
                         "reason": "a table prints the line, and none of its columns is the "
                                   f"period ending {period_end}"}
        else:
            out[line] = {"verdict": "not_in_release",
                         "reason": "no table of the release prints a row under one of the "
                                   "stated labels",
                         "labels": list(ROW_LABELS[line])}
    return out
