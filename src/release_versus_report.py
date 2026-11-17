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

**A heading may label a cell, never hide it.** For a line and a span, every dollar cell of
every table under one of the line's labels is compared, each at its own table's printed
precision, each listed with its paragraph id. A cell carries a `block` hint (`gaap`,
`not_gaap`, `segment`, `component`, `unidentified`) and no hint takes it out of the
comparison. The line is `differs` if a `gaap` cell differs, `differs_outside_gaap` if
only cells with another hint differ (each listed with its hint, paragraph id and both
values), and `agrees` only if every compared cell agrees (`PRECEDENCE`: `differs`,
`differs_outside_gaap`, `block_not_identified` (a cell that agrees but could not be told as
GAAP), `report_fact_missing`, `period_not_read`, then `agrees`). The only cells not held
to a dollar fact are per share rows (under a heading that says per share, `Basic:` or
`Diluted:`) and cells printed as a percent, because they are not dollars.

**Hints come from structure where structure exists.** `not_gaap` only when a column's own
header or the row's own label says Non-GAAP, or the header is the whole word Adjusted
(never "(As Adjusted)", "excluding" or "pro forma"). `segment` only when a header cell or
the heading above the table is the name of a member of the report's own instance on
`StatementBusinessSegmentsAxis` (`names_a_segment`); a company's name is not one.
`component` is a heading's word ("Summary of ...", "by segment", "including") labelling
the parts under it, never a row that starts with "Total". A heading that says non-GAAP
or adjusted labels the rows under it `unidentified`; a non-GAAP total row closes it.

**The face statement** is the table printing at least four of the lines under their labels
with a column for the period, the most lines first and the earlier on a tie, chosen
without a value. Each line carries `statement`: `agrees`, `differs` or `not_compared`,
with the paragraph id, beside its own verdict and never lending it one. Tables that could
not be read are grouped by kind (`guidance`, `non_gaap`, `segment_column`, `undated`,
`unit_not_stated`) and a column that is neither the period nor the year before it is
listed with its date.

**Agreement is at the release's own precision.** A release printing `4,133` in
millions has a step of one million, and agrees with every report fact that
rounds, half up, to 4,133 million; a release printing `1,570.7` has a step of a
tenth of a million; per-share figures step by the decimals printed. A cost, a capital
expenditure and an income tax expense printed in parentheses are compared by their size,
as the taxonomy states a payment; an income tax whose label says benefit is signed,
expense positive. In a table that prints an `attributable` net income row, an unlabelled
net income row is the total before the noncontrolling interest and is held to `ProfitLoss`
alone; in a table that prints none it is held to `NetIncomeLoss`, and the cell also says
what `ProfitLoss` would have made of it. The difference is the release's value less the
report's, in dollars, and `sign` says which way: `release_larger`, `release_smaller` or
`equal`.
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
                           "Income tax provision", "Income tax (benefit) expense",
                           "Income tax (expense) benefit", "Income taxes"),
    "net_income": ("Net income", "Net earnings", "Net income (loss)", "Net earnings (loss)",
                   "GAAP net income", "Net income (GAAP)",
                   "Net income attributable to Generac Holdings Inc.",
                   "Net income attributable to Johnson Controls",
                   "Net earnings (loss) attributable to common shareowners"),
    "diluted_earnings_per_share": ("Diluted earnings per share", "Earnings per share - diluted",
                                   "Diluted EPS", "GAAP diluted EPS",
                                   "GAAP diluted net income per share",
                                   "Diluted earnings per share (EPS)",
                                   "Diluted net income per potential common share",
                                   "GAAP net income per share, diluted"),
    "operating_cash_flow": ("Net cash provided by operating activities",
                            "Change in cash from operating activities",
                            "Net cash flows provided by operating activities",
                            "Net cash flows provided by (used in) operating activities",
                            "Cash generated by operating activities",
                            "GAAP net cash provided by operating activities"),
    "capital_expenditure": ("Capital expenditures", "Purchases of property and equipment",
                            "Purchases of property, plant, and equipment",
                            "Expenditures for property and equipment",
                            "Payments for acquisition of property, plant and equipment"),
}

PER_SHARE = ("diluted_earnings_per_share",)
BY_SIZE = ("capital_expenditure", "cost_of_revenue")   # printed in parentheses as an outflow


class ReleaseLabelError(Exception):
    """A label belongs to two lines, so a row under it would be two things."""


_DASHES = str.maketrans({"—": "-", "–": "-", "‐": "-", "‑": "-",
                         "−": "-", "’": "'", "​": ""})
# A reconciliation prints a line with the word that says what is done with it: `Less: Capital
# expenditures` is the capital expenditures line, and is compared as it.
_PREFIX = re.compile(r"^(?:less|add|plus|minus|deduct)\s*:\s*")
_FOOTNOTE = re.compile(r"(?:\s*\((?:\d{1,2}|[a-z])\)|\s*\*+)+$")


def normal_label(text: str) -> str:
    """A row label as it is compared: lower case, one space, plain dashes, no
    trailing footnote mark or colon."""
    text = text.translate(_DASHES).strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = _PREFIX.sub("", text)
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

# What a cell is labelled with, and never what keeps it from being compared. A hint is one
# of: `gaap`, `not_gaap`, `segment`, `component`, `unidentified`. `not_gaap` comes only from
# structure: a column's own header, or the row's own label, says "Non-GAAP", or the header
# is the whole word "Adjusted" (never "(As Adjusted)", "excluding" or "pro forma").
# A heading above rows that says non-GAAP or adjusted is prose, and labels them
# `unidentified`.
HINTS = ("gaap", "not_gaap", "segment", "component", "unidentified")
_GAAP_WORD = re.compile(r"\bgaap\b")
_NON_GAAP = re.compile(r"non[-\s]*gaap")
# Headings whose rows are per share: the one kind of row, with a percent cell, that is not
# held to a dollar fact, because it is not dollars.
PER_SHARE_HEADING = re.compile(r"^(?:per (?:common )?share|earnings per share|net income per share|"
                               r"basic|diluted)\b")
# Headings whose rows are parts of a line, not the line: they are compared and labelled.
COMPONENT_HEADING = re.compile(r"summary of|compensation|by (?:segment|region|product)|of which|"
                               r"included in|including|by function")


def _month_number(name: str) -> int:
    return ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov",
            "dec"].index(name[:3].lower()) + 1


def unit_statement(text: str) -> str | None:
    found = _UNIT.search(text)
    return found.group(1).lower() if found else None


def _flatten(text: str) -> str:
    return re.sub(r"non[-\s]+gaap", "non-gaap", normal_label(text))


def block_of(text: str) -> str | None:
    """The hint a row label or a heading gives: `gaap`, `not_gaap` (row labels only) or
    `unidentified` when it names both, else None. A heading's non-GAAP is prose, and
    `heading_hint` turns it into `unidentified`."""
    words = _flatten(text)
    non = bool(_NON_GAAP.search(words))
    plain = bool(_GAAP_WORD.search(words.replace("non-gaap", "")))
    if non and plain:
        return "unidentified"
    return "not_gaap" if non else ("gaap" if plain else None)


def header_hint(text: str) -> str | None:
    """The hint a header cell gives its columns: non-GAAP, or the whole word Adjusted as the
    column's label, is `not_gaap`; GAAP alone is `gaap`; both is `unidentified`."""
    words = _flatten(text)
    if re.fullmatch(r"adjusted(?: results)?", words) or words.startswith("adjusted "):
        return "unidentified" if _GAAP_WORD.search(words.replace("non-gaap", "")) else "not_gaap"
    return block_of(text)


def heading_hint(text: str) -> str | None:
    """What a heading above rows labels them: GAAP, or `unidentified` if it says non-GAAP
    or adjusted or both."""
    words = _flatten(text)
    if _NON_GAAP.search(words) or re.search(r"\badjusted\b", words):
        return "unidentified"
    return "gaap" if _GAAP_WORD.search(words) else None


# A paragraph that is only a unit statement, as a statement's title line prints it:
# "(In millions, except per share amounts)". A sentence that mentions millions is not
# one, so a unit never comes from prose.
_TITLE_UNIT = re.compile(r"^\(?[^.\d]{0,100}\bin (thousands|millions|billions)\b[^.\d]{0,80}\)?$",
                         re.I)

def segment_label(member: str) -> str:
    """A segment member's name as words: `carr:ClimateSolutionsAmericasSegmentMember` is
    `climate solutions americas`. The instance carries the members and not their labels,
    so the name is the member's own local name."""
    local = member.split(":")[-1]
    local = re.sub(r"(?:Segment)?Member$", "", local)
    words = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", local)
    return re.sub(r"\s+", " ", words).strip().lower()


def _words_of(text: str) -> str:
    text = re.sub(r"\([^)]*\)", " ", text.lower().replace("&", " and "))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", text)).strip()


def names_a_segment(text: str | None, segment_labels) -> bool:
    """True when the text is the name of a segment member of the report's own instance
    (`us-gaap:StatementBusinessSegmentsAxis`). A company's name is not one."""
    if not text or not segment_labels:
        return False
    words = _words_of(text)
    return bool(words) and any(words == _words_of(label) for label in segment_labels)


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
    """Give each column the hint its header's group labels give, shared out over the
    columns in order (`source` is then `group`: the column's own header); one label is the
    whole table's (`source` is `table`: a title a heading below may overrule); with none, a
    table that repeats a column is two blocks nothing names (`unidentified`), and a table
    that does not is read as the statement (`gaap`)."""
    count = len(columns)
    keys = [(c.get("months"), c.get("end")) for c in columns if "change" not in c]
    for index, column in enumerate(columns):
        column["source"] = "group" if len(labels) > 1 else "table"
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


# What a period's sub-column is called. Only `Reported`, `As reported` and `GAAP` are the
# statement's; `Adjusted` and `non-GAAP` are not GAAP; any other name (Adjustments, Special
# Items, Impact, Adj.) is not a dollar of the line, and is listed unread with its name.
_SUB_GAAP = re.compile(r"^(?:as reported|reported|gaap)$", re.I)


def _sub_columns(header: list[list[str]], count: int) -> list[str] | None:
    """The labels a period's columns split into (`Reported`, `Adjustments`, `Adjusted`), when a
    header row prints them once for every period column, in the same order each time."""
    for cells in header:
        labels = [c.strip() for c in cells if c.strip() and not unit_statement(c)
                  and not any(ch.isdigit() for ch in c)]
        if count and len(labels) % count == 0 and len(labels) // count >= 2:
            k = len(labels) // count
            if labels[:k] * count == labels:
                return labels[:k]
    return None


def _sub_kind(label: str) -> str | None:
    """`gaap`, `not_gaap`, or None for a sub-column that is not a dollar of the line."""
    if _SUB_GAAP.match(label.strip()):
        return "gaap"
    return "not_gaap" if header_hint(label) == "not_gaap" else None


def _expand(columns: list[dict], sub: list[str]) -> list[dict]:
    """Each period column as the sub-columns its header names."""
    out = []
    for column in columns:
        for label in sub:
            kind = _sub_kind(label)
            if "change" in column or kind is None:
                out.append({"change": True, "sub_column": label})
            else:
                out.append(dict(column, block=kind, source="group"))
    return out


def _date(year: int, month: int, day: int) -> dt.date:
    """A date a header names, or `Unread`: "February 29" in a year without one is the
    table's problem and never an exception."""
    try:
        return dt.date(year, month, day)
    except ValueError:
        raise Unread(f"the header's date {day}/{month}/{year} is not a date") from None


def read_header(rows: list[list[str]], segment_labels=()) -> dict:
    """The columns a table's header names, or `Unread`.

    Returns `columns` (each `change` or a period with `months`, `end` and `block`, the
    hint its header gives), `first_data_row`, `unit` (the table's own unit statement, or
    None) and `segment` (the header names a segment of the report's instance).
    """
    first = next((index for index, cells in enumerate(rows) if _is_data_row(cells)), None)
    if first is None or first == 0:
        raise Unread("the table has no header rows above its first row of figures")
    header = rows[:first]
    unit = next((u for cells in header for cell in cells if (u := unit_statement(cell))), None)
    labels = [b for cells in header for cell in cells if cell.strip() and (b := header_hint(cell))]
    segment = any(names_a_segment(cell, segment_labels) for cells in header for cell in cells)

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
                              "end": _date(int(date.group(3)), _month_number(date.group(1)),
                                           int(date.group(2)))})
    if whole:
        _assign_blocks(whole, labels)
        return {"columns": whole, "first_data_row": first, "unit": unit, "segment": segment,
                "sub": _sub_columns(header, len(whole))}

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
            resolved[index] = {"end": _date(column[3], column[1], column[2])}
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
            resolved[index] = {"end": _date(columns[index][1], source[1], source[2])}
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
    return {"columns": resolved, "first_data_row": first, "unit": unit, "segment": segment,
            "sub": _sub_columns(header, len(resolved))}


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


# A statement of cash flows is known by what it prints, not by a value: its operating,
# investing and financing lines, or two of them and the change in cash. A summary table
# that prints net income beside operating cash flow is not one.
_CASH_FLOW_LINE = re.compile(
    r"^(?:net )?cash(?: flows?)?(?: \(?(?:provided|used|generated)[^)]*\)?)*.*"
    r"\b(operating|investing|financing) activities|"
    r"^change in cash from (operating|investing|financing) activities")
_CASH_AT_AN_END = re.compile(r"^cash\b.*\b(?:beginning|end) of (?:the )?(?:period|year)")


def is_a_statement_of_cash_flows(rows: list[list[str]]) -> bool:
    """True when the table prints the cash at the beginning or the end of the period beside at
    least two of its operating, investing and financing cash flow lines, each with a figure. A
    change in cash alone, or a reconciliation that prints operating cash flow and capital
    expenditure, is not one."""
    kinds, ends = set(), False
    for cells in rows:
        placed = _label_of(cells)
        if not placed or not any(read_number(c) is not None for c in cells[placed[0] + 1:]):
            continue
        label = normal_label(placed[1])
        found = _CASH_FLOW_LINE.search(label)
        if found:
            kinds.add(found.group(1) or found.group(2))
        elif _CASH_AT_AN_END.search(label):
            ends = True
    return ends and len(kinds) >= 2


_GUIDANCE = re.compile(r"guidance|outlook|forecast|expect|previous|updated|range", re.I)


def table_kind(rows: list[list[str]], reason: str, segment_labels=()) -> str:
    """What kind of table could not be read, by what its own header cells say: `guidance`,
    `non_gaap`, `segment_column` (the figures are the segments', one column each), `undated`,
    or what was wrong with its rows."""
    if "unit statement" in reason:
        return "unit_not_stated"
    first = next((i for i, cells in enumerate(rows) if _is_data_row(cells)), len(rows))
    text = " ".join(cell for cells in rows[:first] for cell in cells)
    if _GUIDANCE.search(text):
        return "guidance"
    if _NON_GAAP.search(_flatten(text)) or re.search(r"\badjusted\b", text, re.I):
        return "non_gaap"
    if ("figures and the header names" in reason
            or re.search(r"segment|reported|adjustments", text, re.I)
            or any(names_a_segment(cell, segment_labels) for cells in rows[:first] for cell in cells)):
        return "segment_column"
    return "undated"


# The unit a heading row carries only sets the unit; the heading is what is left of it.
_UNIT_PHRASE = re.compile(r"\(?\s*(?:\$\s*)?(?:u\.s\.\s*dollars\s*)?in\s+(?:thousands|millions|billions)\b"
                          r"[^()]*\)?|\(\s*unaudited\s*\)", re.I)


def heading_text(label: str) -> str:
    """A heading's own words: `Other financial data (in millions):` is `Other financial data`.
    Empty for a row that is only a unit statement."""
    return re.sub(r"\s+", " ", _UNIT_PHRASE.sub(" ", label)).strip(" :-")


# The plain synonyms of capital expenditure: a purchase, acquisition or payment for property,
# equipment, plant or fixtures. A label that also covers something else (intangible assets,
# software, a net figure, an amount still payable) is only printed under another label.
_CAPEX_VERB = re.compile(r"^(?:purchases?|acquisitions?|payments?|expenditures?)\b")
_CAPEX_THING = re.compile(r"\b(?:property|equipment|fixtures|plant)\b")
_CAPEX_MORE = re.compile(r"intangible|software|securit|investment|business|real estate|capitalized|"
                         r"\bnet\b|\bleases?\b|deposit|loan|payable|accrued|unpaid|non-?cash|"
                         r"financed|proceeds|sale\b")


def capex_synonym(label: str) -> str | None:
    """`line` if the label is a plain synonym of capital expenditure, `other` if it holds the
    words and something else besides, else None."""
    words = normal_label(label)
    if not (_CAPEX_VERB.match(words) and _CAPEX_THING.search(words)):
        return None
    return "other" if _CAPEX_MORE.search(words) else "line"


def line_of_label(label: str) -> str | None:
    """The line a row label is: a stated label, or a plain synonym of capital expenditure."""
    return LINE_OF_LABEL.get(normal_label(label)) or (
        "capital_expenditure" if capex_synonym(label) == "line" else None)


def row_lines(rows: list[list[str]]) -> list[str | None]:
    """The line each row of a table is, by its label and its heading: `Diluted` under a per share
    heading is diluted earnings per share, and under a heading about shares it is not."""
    first = next((i for i, cells in enumerate(rows) if _is_data_row(cells)), len(rows))
    per_share, out = False, [None] * len(rows)
    for index, row in enumerate(rows):
        placed = _label_of(row)
        if placed is None:
            continue
        if not _is_data_row(row):
            if _tokens(row) or _SPAN.search(" ".join(row)) or (index < first and placed[0] != 0):
                continue
            text = heading_text(placed[1])
            if text or not unit_statement(" ".join(row)):
                per_share = bool(PER_SHARE_HEADING.search(normal_label(text)))
            continue
        out[index] = line_of_label(placed[1]) or (
            "diluted_earnings_per_share" if normal_label(placed[1]) == "diluted" and per_share
            else None)
    return out


def _names_attributable_net_income(label: str) -> bool:
    """A dollar row that says attributable to and names net income or earnings: the parent's
    row, which makes an unlabelled net income the total before the noncontrolling interest. A
    per share row (`Net income per share attributable to ...`) is not."""
    words = label.lower()
    return ("attributable to" in words and re.search(r"net income|net earnings|earnings|income", words)
            is not None and not re.search(r"per (?:common |ordinary )?share|per unit|\bshares\b", words))


# A row printed under another label is only a candidate for the line if it could be the line
# in dollars: not a non-GAAP or adjusted measure, a deferred or current part, a weighted
# average or a share count.
_NOT_THE_LINE = re.compile(r"non-?\s*gaap|adjusted|deferred|current|weighted|\bshares?\b")


def lines_named_in(label: str) -> list[str]:
    """The lines one of whose stated labels is inside this row label, as whole words:
    `Capital expenditures and capitalized software development costs` holds
    `Capital expenditures`. Only a row no stated label matches is asked."""
    words = normal_label(label)
    if _NOT_THE_LINE.search(_flatten(label)):
        return []
    named = [line for line, stated in ROW_LABELS.items()
             if any(re.search(rf"(?<![\w-]){re.escape(normal_label(name))}(?![\w])", words)
                    for name in stated)]
    if capex_synonym(label) == "other" and "capital_expenditure" not in named:
        named.append("capital_expenditure")
    return named


def read_cells(paragraph_ids: list[str], paragraphs: list[str], period_end: str,
               segment_labels=()) -> dict:
    """Every dollar cell of every table of the release under a line's labels, for the period.

    Each cell is returned with its `block` hint; no hint takes a cell out. Returns `cells`,
    `unread` (line -> tables and rows that could not be read, each with a `kind`),
    `excluded` (per share rows and percent cells: not dollars), `unread_columns` (columns
    of a read table that are neither the period nor the year before it, with their date),
    `seen` (the lines some table has a row for) and `statement` (the paragraph id of the
    table that prints the most of the lines with a column for the period, at least four,
    chosen without looking at a value).
    """
    end = dt.date.fromisoformat(period_end)
    cells, unread, excluded, seen, unread_columns = [], {}, [], set(), []
    cash_flow_statements, other_label_rows, attributable_tables = set(), {}, set()
    printed_lines: dict[str, set[str]] = {}
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

        def note(line, label, reason, kind=None):
            unread.setdefault(line, []).append({
                "paragraph_id": paragraph_id, "label": label, "reason": reason,
                "kind": kind or table_kind(rows, reason, segment_labels)})

        lines_of = row_lines(rows)
        candidates = any(_is_data_row(row) and not lines_of[i] and lines_named_in(_label_of(row)[1])
                         for i, row in enumerate(rows))
        if not any(lines_of) and not candidates:
            continue
        try:
            header = read_header(rows, segment_labels)
        except Unread as reason:
            for i, row in enumerate(rows):
                if lines_of[i]:
                    note(lines_of[i], _label_of(row)[1], str(reason))
                    seen.add(lines_of[i])
            continue
        columns = header["columns"]
        if is_a_statement_of_cash_flows(rows):
            cash_flow_statements.add(paragraph_id)
        for label in header.get("sub") or []:
            if _sub_kind(label) is None:
                for column in columns:
                    if "change" not in column:
                        unread_columns.append({
                            "paragraph_id": paragraph_id, "sub_column": label,
                            "date": column["end"].isoformat(), "span_months": column["months"],
                            "reason": f"the sub-column {label!r} is not a dollar of the line"})
        scale_name = header["unit"] or carried
        table_segment = header["segment"] or names_a_segment(heading, segment_labels)
        if any("change" not in c and c["end"] == end for c in columns):
            printed_lines[paragraph_id] = {name for name in lines_of if name}
        for column in columns:
            near_a_year_earlier = abs((end - column.get("end", end)).days - 364) <= 20
            if "change" not in column and column["end"] != end and not near_a_year_earlier:
                unread_columns.append({"paragraph_id": paragraph_id,
                                       "date": column["end"].isoformat(),
                                       "span_months": column["months"],
                                       "reason": "a column that is neither the period nor "
                                                 "the year before it"})
        row_hint, per_share, component, reset_hint = None, False, False, False
        for index, row in enumerate(rows):
            placed = _label_of(row)
            if placed is None:
                continue
            if index < header["first_data_row"]:
                # a heading row among the header's own rows: label in the first cell, and
                # no date or span for a column
                if placed[0] != 0 or _tokens(row) or _SPAN.search(" ".join(row)):
                    continue
            own_words = heading_text(placed[1])
            if (unit_statement(" ".join(row)) and not _is_data_row(row)
                    and not own_words):
                continue                 # a row that is only a unit statement changes nothing
            if reset_hint:
                row_hint, reset_hint = None, False
            if _is_data_row(row) and block_of(placed[1]) == "not_gaap":
                reset_hint = True       # a non-GAAP total closes the block its heading opened
            line = lines_of[index]
            if _is_data_row(row) and _names_attributable_net_income(placed[1]) and not per_share:
                attributable_tables.add(paragraph_id)
            if not _is_data_row(row) and not line:
                # a heading: it labels the rows under it and compares nothing away
                # (a unit it carries only sets the unit: its own words are read)
                words = normal_label(own_words)
                row_hint = heading_hint(own_words) or row_hint
                per_share = bool(PER_SHARE_HEADING.search(words))
                component = bool(COMPONENT_HEADING.search(words))
                continue
            if not line:
                # a row whose label holds a stated label's words and is none of them
                near = lines_named_in(placed[1]) if _is_data_row(row) else []
                shown = _figures(row[placed[0] + 1:])
                if near and len(shown) == len(columns):
                    for column, figure in zip(columns, shown):
                        if "change" not in column and column["end"] == end and not figure["percent"]:
                            for name in near:
                                other_label_rows.setdefault(name, []).append({
                                    "label": placed[1], "paragraph_id": paragraph_id,
                                    "cell": figure["text"], "span_months": column["months"]})
                continue
            seen.add(line)
            figures = _figures(row[placed[0] + 1:])
            if per_share and line not in PER_SHARE:
                excluded.append({"line": line, "paragraph_id": paragraph_id, "label": placed[1],
                                 "cell": figures[0]["text"] if figures else "",
                                 "reason": "a per share row, which is not dollars"})
                continue
            use = columns
            sub = header.get("sub")
            if sub and len(figures) == len(columns) * len(sub):
                use = _expand(columns, sub)         # Reported, Adjustments, Adjusted, ... each
            if len(figures) != len(use):
                dollars = [f for f in figures if not f["percent"]]
                if not dollars and line not in PER_SHARE:
                    excluded.append({"line": line, "paragraph_id": paragraph_id, "label": placed[1],
                                     "cell": figures[0]["text"] if figures else "",
                                     "reason": "a row printed as a percent, which is not dollars"})
                    continue
                if len(dollars) == len(columns) and line not in PER_SHARE:
                    # dollars and percents in one row: the dollars are compared, the percents not
                    for f in figures:
                        if f["percent"]:
                            excluded.append({
                                "line": line, "paragraph_id": paragraph_id, "label": placed[1],
                                "cell": f["text"],
                                "reason": "a cell printed as a percent, which is not dollars"})
                    figures = dollars
                else:
                    note(line, placed[1], f"the row prints {len(figures)} figures and the "
                                          f"header names {len(columns)} columns")
                    continue
                use = columns
            if line not in PER_SHARE and scale_name is None:
                note(line, placed[1], "no unit statement (in millions, in thousands) is "
                                      "printed for the table or a table before it")
                continue
            for column, figure in zip(use, figures):
                if "change" in column or column["end"] != end:
                    continue
                if line not in PER_SHARE and figure["percent"]:
                    excluded.append({"line": line, "paragraph_id": paragraph_id, "label": placed[1],
                                     "cell": figure["text"], "span_months": column["months"],
                                     "reason": "a cell printed as a percent, which is not dollars"})
                    continue
                scale = 1 if line in PER_SHARE else _SCALE[scale_name]
                label_hint = block_of(placed[1])
                hint = column["block"]
                if row_hint and column["source"] != "group":
                    hint = row_hint                  # a heading below a table-wide title
                if component and not placed[1].lower().startswith("total"):
                    hint = "component"
                if table_segment:
                    hint = "segment"
                if label_hint == "not_gaap" or (column["block"] == "not_gaap"
                                                 and column["source"] == "group"):
                    hint = "unidentified" if label_hint == "gaap" else "not_gaap"
                elif label_hint in ("gaap", "unidentified"):
                    hint = label_hint
                cells.append({
                    "line": line, "months": column["months"], "paragraph_id": paragraph_id,
                    "label": placed[1], "cell": figure["text"], "value": figure["value"],
                    "decimals": figure["decimals"], "scale_value": scale, "block": hint,
                    "release": {"label": placed[1], "cell": figure["text"],
                                "paragraph_id": paragraph_id, "block": hint,
                                "scale": "dollars" if line in PER_SHARE else scale_name,
                                "printed_decimals": figure["decimals"],
                                "value": float(figure["value"] * scale)}})
    candidates = {pid: lines for pid, lines in printed_lines.items() if len(lines) >= 4}
    statement = (min(candidates, key=lambda pid: (-len(candidates[pid]),
                                                  paragraph_ids.index(pid)))
                 if candidates else None)
    return {"cells": cells, "unread": unread, "excluded": excluded, "seen": seen,
            "unread_columns": unread_columns, "statement": statement,
            "cash_flow_statements": cash_flow_statements, "other_label_rows": other_label_rows,
            "attributable_tables": attributable_tables}


# The order a line's verdict is taken in. A difference in a GAAP cell is the line's; a
# difference in a cell labelled anything else is named as outside GAAP; then a cell that
# agrees but could not be told as GAAP, a report fact that is not there, and a table that
# could not be read each keep the line from `agrees`.
PRECEDENCE = ("differs", "differs_outside_gaap", "block_not_identified", "report_fact_missing",
              "period_not_read", "agrees")


def line_verdict(verdicts) -> str:
    """The most important of the verdicts of a line's cells and unread tables."""
    present = set(verdicts)
    return next((name for name in PRECEDENCE if name in present), "not_in_release")


def _printed_as(line: str, label: str, value: Decimal) -> Decimal:
    """The release's figure in the taxonomy's sign. A cost, a capital expenditure and an income
    tax expense are stated as their size and printed in parentheses by many releases, so
    they are compared by size; an income tax whose label says benefit is signed, expense
    positive; and a label that says `(expense) benefit` prints the expense negative and the
    benefit positive, so its sign is turned over (Carrier's `(180)` is an expense of 180)."""
    words = label.lower()
    if line == "income_tax_expense":
        if "(expense)" in words:
            return -value
        return value if "benefit" in words else abs(value)
    return abs(value) if line in BY_SIZE else value


def compare_release(paragraph_ids: list[str], paragraphs: list[str], period_end: str, read_report,
                    segment_labels=()) -> dict:
    """The release set beside the report, line by line.

    `read_report(line, months)` is the calculator's: the report's cell for that line over a
    span of `months` ending on the period end, or `{"missing": why}`. Returns `lines`, the
    `statement` table's paragraph id, `unread_columns` and `unread_tables` by kind.
    """
    read = read_cells(paragraph_ids, paragraphs, period_end, segment_labels)
    reports: dict[tuple[str, int], dict] = {}

    def report(line: str, months: int) -> dict:
        if (line, months) not in reports:
            reports[(line, months)] = read_report(line, months)
        return reports[(line, months)]

    with_attributable = read["attributable_tables"]
    # a table that prints an operating cash flow line is a statement of cash flows, whose net
    # income is the consolidated one by construction
    cash_flow_tables = read["cash_flow_statements"]
    out = {}
    for line in LINES:
        compared = []
        for cell in (c for c in read["cells"] if c["line"] == line):
            entry = {"span_months": cell["months"], "period_end": period_end,
                     "release": cell["release"], "block": cell["block"]}
            generic = line == "net_income" and "attributable" not in cell["label"].lower()
            parent, total = "net_income", "net_income_with_noncontrolling"
            # an unlabelled net income is the total before the noncontrolling interest in a table
            # with a parent's row and in a statement of cash flows: held to ProfitLoss
            wants_total = generic and (cell["paragraph_id"] in with_attributable
                                       or cell["paragraph_id"] in cash_flow_tables)
            held = total if wants_total else line
            fact = report(held, cell["months"])
            if wants_total and "missing" in fact:
                held = parent
                fact = report(parent, cell["months"])
                entry["held_to"] = ("NetIncomeLoss: ProfitLoss is not on record for the period, "
                                    "so the total before the noncontrolling interest cannot be "
                                    "told from the parent's")
            if "missing" in fact:
                entry.update(verdict="report_fact_missing", report={"missing": fact["missing"]})
                compared.append(entry)
                continue
            shown = _printed_as(line, cell["label"], cell["value"])
            scale, decimals = cell["scale_value"], cell["decimals"]
            agrees = agrees_at_the_release_precision(shown, fact["value"], scale, decimals)
            difference = shown * scale - Decimal(str(fact["value"]))
            entry.update(report=fact, difference=float(difference), sign=_sign(difference),
                         verdict="agrees" if agrees else "differs")
            if generic and not (held == total and cell["paragraph_id"] in with_attributable):
                other_line = total if held == parent else parent
                other = report(other_line, cell["months"])
                if "missing" not in other and other["value"] != fact["value"]:
                    entry["also_against"] = {
                        other_line: other,
                        "difference": float(shown * scale - Decimal(str(other["value"]))),
                        "agrees": agrees_at_the_release_precision(shown, other["value"], scale,
                                                                  decimals)}
            compared.append(entry)

        verdicts = []
        for entry in compared:
            verdict, hint = entry["verdict"], entry["block"]
            if verdict == "differs":
                verdicts.append("differs" if hint == "gaap" else "differs_outside_gaap")
            elif verdict == "agrees" and hint == "unidentified":
                verdicts.append("block_not_identified")
            else:
                verdicts.append(verdict)
        if line in read["unread"]:
            verdicts.append("period_not_read")
        if compared or line in read["unread"]:
            out[line] = {"verdict": line_verdict(verdicts), "comparisons": compared}
            if line in read["unread"]:
                out[line]["unread"] = read["unread"][line]
        elif line in read["seen"]:
            out[line] = {"verdict": "period_not_read", "comparisons": [],
                         "reason": f"a table prints the line, and none of its columns is the "
                                   f"period ending {period_end}"}
        elif read["other_label_rows"].get(line):
            out[line] = {"verdict": "printed_under_another_label",
                         "reason": "no stated label matches, and a row whose label holds one "
                                   "of their words prints a figure for the period; it is not "
                                   "taken to be the line",
                         "rows": read["other_label_rows"][line]}
        else:
            out[line] = {"verdict": "not_in_release",
                         "reason": "no table of the release prints a row under one of the "
                                   "stated labels",
                         "labels": list(ROW_LABELS[line])}
        outside = [e for e in compared if e["verdict"] == "differs" and e["block"] != "gaap"]
        if outside:
            out[line]["differs_outside_gaap"] = [
                {"hint": e["block"], "paragraph_id": e["release"]["paragraph_id"],
                 "release": e["release"], "report": e["report"],
                 "difference": e["difference"]} for e in outside]
        excluded = [e for e in read["excluded"] if e["line"] == line]
        if excluded:
            out[line]["excluded_rows"] = excluded
        # the face statement's own verdict, beside the line's and never borrowed by it
        statement = read["statement"]
        mine = [e for e in compared if e["release"]["paragraph_id"] == statement
                and e["verdict"] in ("agrees", "differs")]
        out[line]["statement"] = {
            "paragraph_id": statement,
            "verdict": ("not_compared" if not mine else
                        "differs" if any(e["verdict"] == "differs" for e in mine) else "agrees")}
    by_kind: dict[str, list[dict]] = {}
    for line, notes in read["unread"].items():
        for item in notes:
            by_kind.setdefault(item["kind"], []).append(dict(item, line=line))
    return {"lines": out, "statement": read["statement"],
            "unread_columns": read["unread_columns"], "unread_tables": by_kind}


def compare(paragraph_ids: list[str], paragraphs: list[str], period_end: str, read_report,
            segment_labels=()) -> dict:
    """`compare_release`'s lines alone."""
    return compare_release(paragraph_ids, paragraphs, period_end, read_report,
                           segment_labels)["lines"]
