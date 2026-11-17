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
                            "GAAP net cash provided by operating activities",
                            "Cash flow from operations", "Cash from operations",
                            "Operating cash flow"),
    "capital_expenditure": ("Capital expenditures", "Purchases of property and equipment",
                            "Purchases of property, plant, and equipment",
                            "Expenditures for property and equipment",
                            "Payments for acquisition of property, plant and equipment"),
}

PER_SHARE = ("diluted_earnings_per_share",)
# A row of basic earnings per share is the diluted line's row, held to `EarningsPerShareBasic`
# and hinted `basic`; the name is the pseudo-line `row_lines` gives it and the report is asked.
BASIC = "basic_earnings_per_share"
# The noncontrolling interest's income as the report tags it (a pseudo-line the reader is asked
# for, never a line of the release): its sign, where it is tagged, decides the sign of the row.
NCI = "net_income_to_noncontrolling"
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


# What a period's sub-column is called. A name that says adjustments, adj., special items,
# impact, change or variance is not a dollar of the line, and is listed unread with its name.
# Adjusted, non-GAAP, organic and constant currency are `not_gaap`. A name with GAAP in it (and
# not non or adjusted) or `reported` is the statement's. Any other name is compared and labelled
# `unidentified`: an unknown never hides a difference.
_SUB_UNREAD = re.compile(r"\badjustments?\b|\badj\b|special items?|impact|change|variance", re.I)
_SUB_NOT_GAAP = re.compile(r"adjusted|non[-\s]*gaap|organic|constant[-\s]+currency", re.I)
_SUB_GAAP = re.compile(r"gaap|reported", re.I)


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
    """`gaap`, `not_gaap` or `unidentified` for a sub-column that is compared, None for one
    that is not a dollar of the line."""
    if _SUB_UNREAD.search(label):
        return None
    if _SUB_NOT_GAAP.search(label):
        return "not_gaap"
    return "gaap" if _SUB_GAAP.search(label) else "unidentified"


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
_UNIT_PHRASE = re.compile(r"\(?\s*(?:\$\s*)?(?:(?:(?:u\.s\.\s*)?dollars|amounts|figures)\s*)?in\s+(?:thousands|millions|billions)\b"
                          r"[^()]*\)?|\(\s*unaudited\s*\)", re.I)


def heading_text(label: str) -> str:
    """A heading's own words: `Other financial data (in millions):` is `Other financial data`.
    Empty for a row that is only a unit statement."""
    return re.sub(r"\s+", " ", _UNIT_PHRASE.sub(" ", label)).strip(" :-")


# The plain synonyms of capital expenditure: a purchase, acquisition or payment for property,
# equipment, plant or fixtures. A label that also covers something else (intangible assets,
# software, a net figure, an amount still payable) is only printed under another label.
_CAPEX_VERB = re.compile(r"^(?:purchases?|acquisitions?|payments?|expenditures?)\b")
_CAPEX_THING = re.compile(r"\b(?:property|equipment|fixtures|plant|leasehold improvements|"
                          r"capital assets)\b")
# What a row names that makes it a different payment, whatever else it holds: it is not the line
# and not a candidate for it.
_CAPEX_NOT = re.compile(r"financ|debt|\btax|insurance|contingent|consideration|repair|material|"
                        r"\bleases?\b")
_CAPEX_MORE = re.compile(r"intangible|software|securit|investment|business|real estate|capitalized|"
                         r"\bnet\b|deposit|loan|payable|accrued|unpaid|non-?cash|"
                         r"proceeds|sale\b|discontinued")


def capex_synonym(label: str) -> str | None:
    """`line` if the label is a plain synonym of capital expenditure, `other` if it holds the
    words and something else besides, else None."""
    words = normal_label(label)
    if not (_CAPEX_VERB.match(words) and _CAPEX_THING.search(words)) or _CAPEX_NOT.search(words):
        return None
    return "other" if _CAPEX_MORE.search(words) else "line"


# A heading that says shares or weighted average opens a share block, never a per share block;
# `per share`, `per diluted share` are not it.
_SHARE_BLOCK = re.compile(r"weighted|\bshares?\b|\bunits\b")
_PER_SHARE_WORDS = re.compile(r"\bper\s+(?:[\w-]+\s+){0,2}(?:shares?|units?)\b")
_NOT_EPS = re.compile(r"weighted|outstanding|adjusted|non-?\s*gaap|continuing|discontinued|before|"
                      r"dividend|book|cash flow|\bbasic\b|\bshares\b|\bused\b|number of")


def is_per_share_heading(text: str) -> bool:
    """A heading whose rows are per share: it says per share, or opens with Basic or Diluted,
    and does not say it counts shares or a weighted average."""
    words = normal_label(text)
    if not PER_SHARE_HEADING.search(words):
        return False
    return not _SHARE_BLOCK.search(_PER_SHARE_WORDS.sub(" ", words))


def eps_label(label: str) -> bool:
    """A row label that is diluted earnings per share by its own words: it says diluted and
    per share (`Net income attributable to common shareholders per common share - diluted`)."""
    words = re.sub(r"basic\s*(?:and|&|,|/)\s*diluted|diluted\s*(?:and|&|,|/)\s*basic", "diluted",
                   normal_label(label))                      # basic and diluted are equal
    return bool(re.search(r"\bdiluted\b", words) and _PER_SHARE_WORDS.search(words)
                and not _NOT_EPS.search(words))


def basic_eps_label(label: str) -> bool:
    """A row label that is basic earnings per share by its own words: `Basic`, or one that says
    basic and per share (`Basic net income per common share`)."""
    words = normal_label(label)
    if words == "basic":
        return True
    return bool(re.search(r"\bbasic\b", words) and not re.search(r"\bdiluted\b", words)
                and _PER_SHARE_WORDS.search(words) and not _NOT_EPS.search(
                    re.sub(r"\bbasic\b", " ", words)))


def heading_kind(text: str) -> str | None:
    """`basic` or `diluted` for a per share heading that says which, else None. `Basic and
    diluted` is `diluted`: the two are equal."""
    words = normal_label(text)
    if re.search(r"\bdiluted\b", words):
        return "diluted"
    return "basic" if re.search(r"\bbasic\b", words) else None


def line_of_label(label: str) -> str | None:
    """The line a row label is: a stated label, a diluted per share label, or a plain synonym
    of capital expenditure."""
    return LINE_OF_LABEL.get(normal_label(label)) or (
        "diluted_earnings_per_share" if eps_label(label) else None) or (
        "capital_expenditure" if capex_synonym(label) == "line" else None)


def row_lines(rows: list[list[str]]) -> list[str | None]:
    """The line each row of a table is, by its label and its heading: `Diluted` under a per share
    heading is diluted earnings per share, and under a heading about shares it is not."""
    first = next((i for i, cells in enumerate(rows) if _is_data_row(cells)), len(rows))
    per_share, diluted, basic, out = False, False, False, [None] * len(rows)
    for index, row in enumerate(rows):
        placed = _label_of(row)
        if placed is None:
            continue
        if not _is_data_row(row):
            if _tokens(row) or _SPAN.search(" ".join(row)) or (index < first and placed[0] != 0):
                continue
            text = heading_text(placed[1])
            if text or not unit_statement(" ".join(row)):
                per_share = is_per_share_heading(text)
                diluted = per_share and bool(re.search(r"\bdiluted\b", normal_label(text)))
                basic = per_share and heading_kind(text) == "basic"
            continue
        line = line_of_label(placed[1])
        if per_share and diluted and (line == "net_income" or (
                line is None and _names_attributable_net_income(placed[1]))):
            line = "diluted_earnings_per_share"         # Net earnings under `Diluted:`
        elif per_share and basic and line and line not in PER_SHARE:
            line = BASIC                                # Net earnings under `Basic:`
        out[index] = line or (
            "diluted_earnings_per_share" if normal_label(placed[1]) == "diluted" and per_share
            else None) or (BASIC if basic_eps_label(placed[1]) and (
                per_share or normal_label(placed[1]) != "basic") else None)
    return out


# A row that is the net income of the noncontrolling interest, not a payment to it.
_NCI_ROW = re.compile(r"non-?\s*controlling|minority")
_NCI_NOT_INCOME = re.compile(r"distribution|dividend|contribution|purchase|acquisition|payment|"
                             r"\bsale\b|equity|capital|redemption|redeemed|total")


def is_noncontrolling_row(label: str) -> bool:
    words = label.lower()
    return bool(_NCI_ROW.search(words)) and not _NCI_NOT_INCOME.search(words)


def _names_attributable_net_income(label: str) -> bool:
    """A dollar row that says attributable to and names net income or earnings: the parent's
    row, which makes an unlabelled net income the total before the noncontrolling interest. A
    per share row (`Net income per share attributable to ...`) is not."""
    words = label.lower()
    return ("attributable to" in words and re.search(r"net income|net earnings|earnings|income", words)
            is not None and not re.search(r"per (?:common |ordinary )?share|per unit|\bshares\b", words))


# A row printed under another label is only a candidate for the line if it could be the line
# in dollars: not a non-GAAP or adjusted measure, a deferred or current part, a weighted
# average or a share count, or a rate (growth, margin, rate, percent, change): a rate is not a
# dollar row of the line.
_NOT_THE_LINE = re.compile(r"non-?\s*gaap|adjusted|deferred|current|weighted|\bshares?\b|"
                           r"growth|margin|\brate\b|percent|%|\bchange")


# Words that qualify a stated label without naming another quantity: `Total consolidated net
# revenue` is still the revenue. A row whose label holds a stated label and anything else
# (`ISG operating income`, `Adjustments to reconcile net income`, `... - continuing operations`,
# which leaves out the discontinued part) is another figure, listed.
_QUALIFIERS = {"total", "consolidated", "of", "the", "and", "in", "from", "for", "gaap",
               "reported", "-", "as"}


def other_label_candidates(label: str) -> list[tuple[str, bool]]:
    """The lines one of whose stated labels is inside this row label, as whole words, each with
    whether the rest of the label is only qualifiers (then the row is the line's figure under
    another label and is compared) or names something more (then it is only listed):
    `Total consolidated net revenue` is compared, `Capital expenditures and capitalized software
    development costs` is listed. Only a row no stated label matches is asked."""
    words = normal_label(label)
    if _NOT_THE_LINE.search(_flatten(label)):
        return []
    out = []
    for line, stated in ROW_LABELS.items():
        comparable, found = False, False
        for name in stated:
            match = re.search(rf"(?<![\w-]){re.escape(normal_label(name))}(?![\w])", words)
            if match:
                found = True
                rest = re.sub(r"\([a-z0-9]{1,2}\)", " ", words[:match.start()] + " " + words[match.end():])
                tokens = re.findall(r"[\w'-]+", rest)
                comparable = comparable or all(t in _QUALIFIERS for t in tokens)
        if found:
            out.append((line, comparable))
    if capex_synonym(label) == "other":       # more than the plain purchase: listed, never compared
        out = [(line, comparable and line != "capital_expenditure") for line, comparable in out]
        if all(line != "capital_expenditure" for line, _ in out):
            out.append(("capital_expenditure", False))
    return out


def lines_named_in(label: str) -> list[str]:
    """The lines a row label holds a stated label of (`other_label_candidates`, names only)."""
    return [line for line, _ in other_label_candidates(label)]


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
    noncontrolling_tables, noncontrolling = set(), {}
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
            printed_lines[paragraph_id] = {"diluted_earnings_per_share" if name == BASIC else name
                                           for name in lines_of if name}
        for column in columns:
            near_a_year_earlier = abs((end - column.get("end", end)).days - 364) <= 20
            if "change" not in column and column["end"] != end and not near_a_year_earlier:
                unread_columns.append({"paragraph_id": paragraph_id,
                                       "date": column["end"].isoformat(),
                                       "span_months": column["months"],
                                       "reason": "a column that is neither the period nor "
                                                 "the year before it"})
        row_hint, per_share, component, reset_hint = None, False, False, False
        per_kind = None
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
            if _is_data_row(row) and scale_name and not per_share:
                nci = is_noncontrolling_row(placed[1])
                parent_row = (not nci and _names_attributable_net_income(placed[1])
                              and not re.search(r"continuing|discontinued", placed[1].lower()))
                if nci:
                    noncontrolling_tables.add(paragraph_id)
                if nci or parent_row:
                    shown_row = _figures(row[placed[0] + 1:])
                    if len(shown_row) == len(columns):
                        for column, figure in zip(columns, shown_row):
                            if ("change" in column or column["end"] != end or figure["percent"]):
                                continue
                            held_rows = noncontrolling.setdefault(
                                (paragraph_id, column["months"]), {})
                            held_rows.setdefault("noncontrolling" if nci else "parent", {
                                "label": placed[1], "cell": figure["text"],
                                "paragraph_id": paragraph_id, "decimals": figure["decimals"],
                                "step": float(_SCALE[scale_name] * Decimal(10) ** -figure["decimals"]),
                                "printed": str(figure["value"]), "scale": _SCALE[scale_name],
                                "value": float(figure["value"] * _SCALE[scale_name])})
            if not _is_data_row(row) and not line:
                # a heading: it labels the rows under it and compares nothing away
                # (a unit it carries only sets the unit: its own words are read)
                words = normal_label(own_words)
                row_hint = heading_hint(own_words) or row_hint
                per_share = is_per_share_heading(own_words)
                per_kind = heading_kind(own_words) if per_share else None
                component = bool(COMPONENT_HEADING.search(words))
                continue
            if not line:
                # a row whose label holds a stated label's words and is none of them
                near = other_label_candidates(placed[1]) if _is_data_row(row) else []
                shown = _figures(row[placed[0] + 1:])
                if near and len(shown) == len(columns):
                    for column, figure in zip(columns, shown):
                        if "change" in column or column["end"] != end or figure["percent"]:
                            continue
                        for name, comparable in near:
                            if comparable and name not in PER_SHARE and scale_name:
                                # the line's figure under another label: compared, hint
                                # `another_label`, so a difference shows and no line agrees
                                # over an unread figure
                                scale = _SCALE[scale_name]
                                hint = ("segment" if table_segment else "not_gaap" if (
                                    block_of(placed[1]) == "not_gaap" or (
                                        column["block"] == "not_gaap" and column["source"] == "group")
                                ) else "another_label")
                                cells.append({
                                    "line": name, "months": column["months"],
                                    "paragraph_id": paragraph_id, "label": placed[1],
                                    "cell": figure["text"], "value": figure["value"],
                                    "decimals": figure["decimals"], "scale_value": scale,
                                    "block": hint,
                                    "release": {"label": placed[1], "cell": figure["text"],
                                                "paragraph_id": paragraph_id, "block": hint,
                                                "scale": scale_name,
                                                "printed_decimals": figure["decimals"],
                                                "value": float(figure["value"] * scale)}})
                                seen.add(name)
                            else:
                                other_label_rows.setdefault(name, []).append({
                                    "label": placed[1], "paragraph_id": paragraph_id,
                                    "cell": figure["text"], "span_months": column["months"]})
                continue
            # A per share block has no closing mark, and a row in it is never dropped by how its
            # figures look. `Basic` rows, and the rows under a `Basic:` heading, are held to
            # EarningsPerShareBasic (hint `basic`); a row under any other per share heading is
            # held to the figure its own label names, or listed unread.
            basic_row = line == BASIC       # its own line, outside the nine, from `row_lines`
            if not basic_row and per_share and line not in PER_SHARE:
                note(line, placed[1], "a row under a per share heading that names neither basic "
                                      "nor diluted, whose own label names no per share figure")
                continue
            seen.add(line)
            per_row = line in PER_SHARE or basic_row
            figures = _figures(row[placed[0] + 1:])
            use = columns
            sub = header.get("sub")
            if sub and len(figures) == len(columns) * len(sub):
                use = _expand(columns, sub)         # Reported, Adjustments, Adjusted, ... each
            if len(figures) != len(use):
                dollars = [f for f in figures if not f["percent"]]
                if not dollars and not per_row:
                    excluded.append({"line": line, "paragraph_id": paragraph_id, "label": placed[1],
                                     "cell": figures[0]["text"] if figures else "",
                                     "reason": "a row printed as a percent, which is not dollars"})
                    continue
                if len(dollars) == len(columns) and not per_row:
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
            if not per_row and scale_name is None:
                note(line, placed[1], "no unit statement (in millions, in thousands) is "
                                      "printed for the table or a table before it")
                continue
            for column, figure in zip(use, figures):
                if "change" in column or column["end"] != end:
                    continue
                if not per_row and figure["percent"]:
                    excluded.append({"line": line, "paragraph_id": paragraph_id, "label": placed[1],
                                     "cell": figure["text"], "span_months": column["months"],
                                     "reason": "a cell printed as a percent, which is not dollars"})
                    continue
                scale = 1 if per_row else _SCALE[scale_name]
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
                if basic_row and hint == "gaap":
                    hint = "basic"           # the basic figure's own hint, as GAAP as the line's
                cells.append({
                    "line": line, "months": column["months"], "paragraph_id": paragraph_id,
                    "label": placed[1], "cell": figure["text"], "value": figure["value"],
                    # a basic row is held to the cent at least: `2` or a dash is not a step of one
                    "decimals": max(figure["decimals"], 2) if basic_row else figure["decimals"],
                    "scale_value": scale, "block": hint,
                    "release": {"label": placed[1], "cell": figure["text"],
                                "paragraph_id": paragraph_id, "block": hint,
                                "scale": "dollars" if per_row else scale_name,
                                "printed_decimals": figure["decimals"],
                                "value": float(figure["value"] * scale)}})
    candidates = {pid: lines for pid, lines in printed_lines.items() if len(lines) >= 4}
    statement = (min(candidates, key=lambda pid: (-len(candidates[pid]),
                                                  paragraph_ids.index(pid)))
                 if candidates else None)
    return {"cells": cells, "unread": unread, "excluded": excluded, "seen": seen,
            "unread_columns": unread_columns, "statement": statement,
            "cash_flow_statements": cash_flow_statements, "other_label_rows": other_label_rows,
            "attributable_tables": attributable_tables,
            "noncontrolling_tables": noncontrolling_tables, "noncontrolling": noncontrolling}


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


_INCOME_WORDS = re.compile(r"\b(?:income|earnings|profit)\b")
_LOSS_WORDS = re.compile(r"\b(?:loss|losses)\b")


def _income_added(label: str, printed: Decimal, tagged: Decimal | None = None) -> list[Decimal]:
    """What the noncontrolling interest adds to the parent's row to make the consolidated net
    income. Where the report tags the interest's income for the period (`tagged`, signed:
    positive is income), the tag decides. Otherwise the sign is read from the row's words, never
    from a prefix: a label with an income word (income, earnings, profit) and no loss word is
    income, a bare figure `+|figure|`; a loss word (loss, losses) and no income word is a loss,
    `-|figure|`. A figure in parentheses is not read from its words (filers differ, and Generac
    prints a loss as `(234)` under an income label), and a label with both kinds of word or
    neither does not say: both signs are returned."""
    if tagged is not None:
        return [tagged]
    words = " ".join(label.lower().split())
    size = abs(printed)
    income, loss = bool(_INCOME_WORDS.search(words)), bool(_LOSS_WORDS.search(words))
    if printed < 0:
        return [size, -size]
    if income and not loss:
        return [size]
    if loss and not income:
        return [-size]
    return [size, -size]


def _identity(cell: dict, rows: dict, parent_fact: dict, nci_fact: dict | None = None) -> dict:
    """A consolidated net income in a table that prints the noncontrolling interest, with no
    ProfitLoss on record: held to the table's own identity, consolidated is the parent's row
    plus the noncontrolling interest's income, at the printed precision. The sign of the
    noncontrolling figure is read from its row (`_income_added`), never tried both ways unless
    the row does not say, and then the cell is `block_not_identified` and never `agrees`. A row
    that breaks the identity differs, with the three cells; a table that does not print all
    three is a fact not on record."""
    held = ("the table's own identity: consolidated net income is the parent's row plus the "
            "noncontrolling interest's income (the tagged "
            "NetIncomeLossAttributableToNoncontrollingInterest decides its sign and its size "
            "where the report tags it, and the printed row is held to it; else the sign is read "
            "from the row), and the parent's row is held to NetIncomeLoss")
    nci, parent = rows.get("noncontrolling"), rows.get("parent")
    if nci is None or parent is None:
        return {"verdict": "report_fact_missing", "held_to": held,
                "report": {"missing": "ProfitLoss is not on record, and the table does not print "
                                      "both the noncontrolling interest and the parent's row "
                                      "for the period"}}
    total = Decimal(str(cell["release"]["value"]))
    kept = Decimal(str(parent["value"]))
    tagged = (Decimal(str(nci_fact["value"])) if nci_fact and "missing" not in nci_fact
              else None)
    added = _income_added(nci["label"], Decimal(str(nci["value"])), tagged)
    # The tolerance is one step, which is exact: each of the three printed figures is the true
    # figure rounded to the nearest step, so their residual is at most 1.5 steps, and the figures
    # all lie on the step's lattice, so a residual counted in whole steps is at most 1.
    step = max(cell["scale_value"] * Decimal(10) ** -cell["decimals"],
               Decimal(str(nci["step"])), Decimal(str(parent["step"])))
    residuals = [total - (kept + a) for a in added]
    residual = min(residuals, key=abs)
    holds = [r for r in residuals if abs(r) <= step]
    cells = [{"role": role, "label": c["label"], "cell": c["cell"], "paragraph_id": c["paragraph_id"]}
             for role, c in (("consolidated", {"label": cell["label"], "cell": cell["cell"],
                                               "paragraph_id": cell["paragraph_id"]}),
                             ("noncontrolling", nci), ("parent", parent))]
    entry = {"held_to": held, "report": parent_fact if "missing" not in parent_fact
             else {"missing": parent_fact["missing"]}}
    if "missing" in parent_fact:
        return dict(entry, verdict="report_fact_missing")
    parent_difference = Decimal(parent["printed"]) * parent["scale"] - Decimal(str(parent_fact["value"]))
    parent_agrees = agrees_at_the_release_precision(
        Decimal(parent["printed"]), parent_fact["value"], parent["scale"], parent["decimals"])
    broken = not holds
    difference = residual if broken else parent_difference
    printed_agrees = tagged is None or agrees_at_the_release_precision(
        abs(Decimal(nci["printed"])), float(abs(tagged)), nci["scale"], nci["decimals"])
    # where the row's words say the sign (income words alone, or loss words alone) and the figure
    # is bare, its sign must be the tag's; a parenthesised or ambiguous row stays sign-free
    printed_sign = Decimal(nci["printed"])
    said = _income_added(nci["label"], printed_sign, None)
    sign_agrees = not (tagged is not None and tagged != 0 and printed_sign > 0 and len(said) == 1
                       and (said[0] > 0) != (tagged > 0))
    verdict = ("differs" if broken or not parent_agrees or not printed_agrees or not sign_agrees
               else "agrees")
    if not printed_agrees:
        entry["reason"] = "the printed noncontrolling figure differs from the report's"
    elif not sign_agrees:
        entry["reason"] = "the printed noncontrolling figure's sign differs from the report's"
    if verdict == "agrees" and len(added) > 1:
        verdict = "block_not_identified"
        entry["reason"] = "the sign of the noncontrolling figure is not stated"
    entry.update(difference=float(difference), sign=_sign(difference), verdict=verdict,
                 identity={"cells": cells, "residual": float(residual), "step": float(step),
                           "parent_agrees_with_the_report": parent_agrees})
    return entry


def statement_verdict(verdicts: list[str]) -> str:
    """The face statement's own verdict for a line, from its cells in the statement: `agrees`
    only if every one agrees, else the weakest, most important first: `differs`,
    `block_not_identified`, `report_fact_missing`; `not_compared` if it has none."""
    if not verdicts:
        return "not_compared"
    return next((v for v in ("differs", "block_not_identified", "report_fact_missing")
                 if v in verdicts), "agrees")


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
    for line in LINES + (BASIC,):
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
            if wants_total and "missing" in fact and cell["paragraph_id"] in read["noncontrolling_tables"]:
                # the table prints the noncontrolling interest: the consolidated cell is not
                # NetIncomeLoss. The parent's own row is held to NetIncomeLoss, and this cell to
                # the table's identity: consolidated less noncontrolling is the parent's row
                entry.update(_identity(cell, read["noncontrolling"].get(
                    (cell["paragraph_id"], cell["months"]), {}), report(parent, cell["months"]),
                    report(NCI, cell["months"])))
                compared.append(entry)
                continue
            if wants_total and "missing" in fact:
                held = parent
                fact = report(parent, cell["months"])
                nci_fact = report(NCI, cell["months"])
                tagged = "missing" not in nci_fact
                if read["noncontrolling_tables"] or (tagged and nci_fact["value"] != 0):
                    # the interest exists (a table of the release prints it, or the report tags
                    # a figure), and this table does not print it: the figure is consolidated
                    if tagged and "missing" not in fact:
                        fact = {"value": fact["value"] + nci_fact["value"],
                                "tag": f"{fact['tag']} + {nci_fact['tag']}",
                                "id": f"{fact['id']} + {nci_fact['id']}",
                                "period": fact.get("period"), "unit": fact.get("unit")}
                        entry["held_to"] = ("NetIncomeLoss plus the tagged "
                                            "NetIncomeLossAttributableToNoncontrollingInterest: "
                                            "ProfitLoss is not on record, and a noncontrolling "
                                            "interest exists, so this table's net income is the "
                                            "consolidated figure")
                    else:
                        fact = {"missing": "ProfitLoss is not on record, a noncontrolling "
                                           "interest exists, and the report does not tag its "
                                           "income for the period, so the consolidated net "
                                           "income cannot be told from the parent's"}
                else:
                    entry["held_to"] = ("NetIncomeLoss: ProfitLoss is not on record for the "
                                        "period, and no noncontrolling interest is printed or "
                                        "tagged, so the total is the parent's")
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
                verdicts.append("differs" if hint in ("gaap", "basic") else "differs_outside_gaap")
            elif verdict == "agrees" and hint == "unidentified":
                verdicts.append("block_not_identified")
            else:
                verdicts.append(verdict)
        if line in read["unread"]:
            verdicts.append("period_not_read")
        if line == BASIC and not compared and line not in read["seen"]:
            continue                 # no basic row anywhere: no tenth line
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
        outside = [e for e in compared if e["verdict"] == "differs" and e["block"] not in ("gaap", "basic")]
        if outside:
            out[line]["differs_outside_gaap"] = [
                {"hint": e["block"], "paragraph_id": e["release"]["paragraph_id"],
                 "release": e["release"], "report": e["report"],
                 "difference": e["difference"]} for e in outside]
        listed = read["other_label_rows"].get(line)
        if listed and out[line]["verdict"] != "printed_under_another_label":
            out[line]["other_label_rows"] = listed        # listed, not compared, never silent
        excluded = [e for e in read["excluded"] if e["line"] == line]
        if excluded:
            out[line]["excluded_rows"] = excluded
        # the face statement's own verdict, beside the line's and never borrowed by it
        statement = read["statement"]
        mine = [e["verdict"] for e in compared if e["release"]["paragraph_id"] == statement]
        out[line]["statement"] = {"paragraph_id": statement, "verdict": statement_verdict(mine)}
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
