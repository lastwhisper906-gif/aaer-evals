"""The gate over the three analyses: what an analyst wrote, held to what it saw.

The owner's decision of 2026-09-28: agents read and judge, Python calculates,
and every number in any output comes from `calculator.json` or companyfacts. An
analyst writes no digit of its own. It writes the path of a `calculator.json`
field in braces, `{ratios.liquidity.current_ratio}`, and this file checks the
path resolves to a number before the memo puts the number there. The rule for
the three analyses is the same rule the quote gate applies to reports:
**every item carries something Python verifies, and a failed item is dropped
and counted.** An item stands only when

- every `{path}` in its words resolves to a number in `calculator.json`;
- its words carry no digit outside a `{path}`, a verbatim quote, an id, a form
  name (10-K, 10-Q, 8-K) or a four-digit year;
- every `evidence` id is an item id of one of the reports the analyst saw;
- every `quote` string-matches the file it names in `quote_from`, which the
  analyst saw, whitespace folded as the quote gate folds it;
- every `fields` entry resolves to a number;
- no word of it is one the owner ruled out: "fraud", "manipulation" in any
  analysis, and "buy", "sell", "alpha" as well;
- its enumerated values are the enumerated values.

A section or an area that fails keeps its key and loses its words, which are
replaced by the reason, because an area of the accounting analysis is never
skipped and a dropped area must still say that it was dropped. The `limits`
sentence must be the rules version's own, character for character.

    python3.12 -m src.analysis_check --kind accounting --agent-dir <dir> \\
        --calculator <calculator.json> --out analysis_accounting.json
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

try:
    from src import calculator, interpreter_pin, quote_gate
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import calculator, interpreter_pin, quote_gate

BAD_INPUT = 2

LIMITS = {
    "accounting": ("This analysis finds where the numbers and the explanations disagree, and "
                   "where the company differs from its own past. It does not judge intent, "
                   "and it cannot see evidence outside the filings, such as invoices or "
                   "contracts."),
    "financial": ("This analysis reads the company's health from its own filed numbers "
                  "against its own past. It forecasts nothing, and it cannot see what is "
                  "not in the filings."),
    "valuation": ("This valuation is a set of stated assumptions run through a stated "
                  "formula. It states no recommendation to trade, and a different reader "
                  "choosing different drivers would reach a different value."),
}

# The area lists are the rules version's, read from the one file that states them.
AREAS_FILE = Path(__file__).resolve().parent.parent / "rules" / "pilot" / "analyst_areas.json"
_AREAS = json.loads(AREAS_FILE.read_text(encoding="utf-8"))
ACCOUNTING_AREAS = tuple(_AREAS["accounting"])
FINANCIAL_SECTIONS = ("profitability", "efficiency", "liquidity", "solvency", "growth",
                      "free_cash_flow")
FINANCIAL_AREAS = tuple(_AREAS["financial"])
VALUATION_KEYS = ("value_range", "price_position", "market_implied_growth",
                  "accounting_adjustments")
OUTCOMES = ("confirms", "contradicts", "unresolved")
DIRECTIONS = ("reduce", "increase")
APPLIES_TO = ("cash_flow", "earnings")

# Each a pattern, so a derivative is caught with its root -- "fraudulent",
# "manipulated" -- and the Korean words are held to the same rule as the English.
# The Korean ones are phrases, not syllables: 사기업 is a private company, 검사기 a
# tester, 자사주 매수 a buyback and 매도가능증권 an available-for-sale security, and
# none of them is the word the owner ruled out.
FORBIDDEN_EVERYWHERE = (r"\bfraud\w*", r"\bmanipulat\w*", "분식", "회계부정", "회계 부정",
                        "사기 행위", "사기행위", "사기적", "사기죄", "조작")
FORBIDDEN_IN_VALUATION = (r"\bbuy\b", r"\bsell\b", r"\balpha\b",
                          r"매수\s*(?:를\s*)?(?:추천|의견|권)", r"매도\s*(?:를\s*)?(?:추천|의견|권)")

# `{path}` or `{path|pct}`: a calculator field, and how to show it.
PLACEHOLDER = re.compile(r"\{([a-z0-9_.-]+)(?:\|(pct))?\}")
# What a digit may be, outside a placeholder and a quote: a name the filing
# itself uses -- a form, a date, a year named as a year, an item, a note, a
# standard, a fiscal quarter -- and never a quantity. Bounded by anything that is
# not a Latin letter or digit, so a form name followed by a Korean particle
# ("8-K의") is still a form name.
#
# A bare four-digit number, 1950 to 2049, is a year only when the words around it
# say so. Before it, a year-context word or phrase: "in", "through", "since",
# "until", "by", "year", "during", "early", "late", "mid", "due", "as of",
# "end of", "year-end", "first half of", "second half of", "half of", "start of",
# "beginning of", "six months of", "first-quarter", "회계연도", or a month name;
# "fiscal", "calendar", "FY" and "Q1".."Q4" are the alternatives above. After
# it: "fiscal year", "guidance", "outlook", a possessive ("2022's"), a month
# name, or the Korean 년, 회계연도, 상반기, 하반기, 분기, 말, 기준. "of" alone is
# not a year context -- "inventory of 2048" is a count -- so it counts only inside
# those phrases; "to" is not one -- "rose to 2030 orders" is a count; and "by"
# names an amount as often as a date ("cut headcount by 2030", "grew by 2026",
# "up by 1999"), so it counts only away from a word of change and only before
# a hard terminator ("by 2030.", "by 2030 and 2031").
#
# After a context word the number is a year only when what follows it is a
# year-terminator: the end of the text, punctuation or any character outside
# the Latin alphabet, a connector ("and", "or", "to", "through", a dash, ".."),
# another year, a year-context-after word, a month, or a function word or time
# word ("the", "was", "quarter", "amendment") -- never a bare noun, so "in 2030
# orders" and "by 2030 orders" are counts while "by 2030." and "in 2030 and 2031"
# are years. A range or a list of four-digit numbers is years only when a member
# has a year-context word of its own: "in 2030 and 2031" and "2021 and 2022
# guidance" are years, "inventory of 2021 and 2022" and a bare "2024–2026" are
# numbers. A year is never written after a currency sign, a sign, a decimal point
# or a digit, never before a decimal, and never before a quantity word, which
# keeps "in 2048 units" and "by 1950 basis points" numbers whatever word stands
# before them. "2026 stores", "€2026", "USD 2026", "2026 Million", "2026 bn" and
# "-2026" have no year context and are numbers.
YEAR = r"(?:19[5-9]\d|20[0-4]\d)"
DATE = r"(?:19|20)\d{2}-\d{2}-\d{2}"
MONTH = (r"(?:January|February|March|April|May|June|July|August|September|October"
         r"|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)")
CHANGE_WORDS = ("cut", "grew", "grow", "grows", "rose", "rise", "rises", "fell", "fall",
                "falls", "up", "down", "increased", "decreased", "reduced", "declined",
                "dropped", "jumped", "climbed", "expanded", "shrank", "improved", "raised",
                "lowered", "higher", "lower", "off")
NOT_AFTER_A_CHANGE_WORD = "".join(rf"(?<!\b{word}\s)" for word in CHANGE_WORDS)
YEAR_CONTEXT_BEFORE = (
    r"(?:in|through|since|until|year|during|early|late|mid|due|as of|회계연도"
    r"|(?:year|quarter|period)[- ]end(?: of)?|end of"
    r"|(?:(?:first|second|1st|2nd)[- ])?half of|start of|beginning of|close of"
    r"|(?:months?|weeks?|quarters?) of|(?:first|second|third|fourth)[- ]quarter"
    r"|" + MONTH + r")")
YEAR_CONTEXT_AFTER = (r"(?:fiscal year|guidance|outlook|['’]s|" + MONTH
                      + r"|년|회계연도|상반기|하반기|분기|말|기준)")
CONNECTOR = r"(?:and|or|to|through)"
FUNCTION_OR_TIME_WORD = (
    r"(?:the|an?|its?|this|that|these|those|which|when|where|while|as|at|with|than|from"
    r"|of|on|in|for|but|because|so|there|it|he|she|they|we|was|were|is|are|has|had|have"
    r"|will|would|could|should|may|might|can|did|does|do|ran|saw|ended|began|closed"
    r"|opened|under|against|after|before|over|into|onto|by|until|through|during|alone"
    r"|only|also|still|then|now|quarter|half|period|fiscal|annual|filing|report|results"
    r"|release|amendment|figure|figures|level|levels|peak|trough|low|high|window|cash"
    r"|balance|date|dates)")
QUANTITY_WORD = (r"(?:million|billion|trillion|thousand|percent|per\s*cent|%|units|basis"
                 r"|points|bps|shares|dollars|employees|customers|days|times|bn|mn|mm)")
NOT_A_QUANTITY = r"(?![.,]\d)(?!\s*(?i:" + QUANTITY_WORD + r"))"
NOT_A_YEAR_HERE = r"(?<![$€£¥₩+\-−.,\d])" + YEAR + NOT_A_QUANTITY
LIST_SEPARATOR = r"(?:\s*[-–—]\s*|\s*,\s*|\s*,?\s*(?i:" + CONNECTOR + r")\s+)"
YEARS = YEAR + r"(?:" + LIST_SEPARATOR + YEAR + r")*"
YEAR_TERMINATOR = (r"(?=\s*(?:$|[^\sA-Za-z0-9]|" + YEAR + r"|(?i:" + CONNECTOR + "|"
                   + FUNCTION_OR_TIME_WORD + "|" + YEAR_CONTEXT_AFTER + r")(?![A-Za-z0-9])))")
# "by" names an amount as often as a date ("cut headcount by 2030", "up by 1999"),
# so after "by" the terminator is the hard kind alone: punctuation, a connector,
# another year or a year-context-after word -- "by 2030." and "by 2030 and 2031"
# are years; "by 2030" at the end of the text and "by 2030 the" are not.
HARD_TERMINATOR = (r"(?=\s*(?:[^\sA-Za-z0-9]|" + YEAR + r"|(?i:" + CONNECTOR + "|"
                   + YEAR_CONTEXT_AFTER + r")(?![A-Za-z0-9])))")
ALLOWED_DIGITS = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    r"10-K|10-Q|8-K|COVID-19"
    r"|(?:19|20)\d{2}-\d{2}-\d{2}"
    r"|(?:[Ff]iscal|[Cc]alendar|FY)[\s-]*(?:19|20)\d{2}"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November"
    r"|December)\s+\d{1,2},?\s+(?:19|20)\d{2}"
    r"|Items? \d{1,2}(?:\.\d{2})?[A-C]?(?!\s*(?:million|billion|thousand|percent|%|units))"
    r"|(?:ASC|Topic)\s+\d{3}(?:-\d{2,3})*(?!\s*(?:million|billion|thousand|percent|%|units))"
    r"|ASU\s+\d{4}-\d{2}"
    r"|Notes? \d{1,2}(?![\d.,])(?!\s*(?:million|billion|thousand|percent|%|units))"
    r"|Q[1-4](?:\s+(?:of\s+)?(?:fiscal\s+)?(?:19|20)\d{2})?"
    r"|FY\d{2,4}"
    # A year, a date, a range or a list of years after a year-context word, joined
    # by whitespace or a hyphen, and followed by a year-terminator: "in 2026",
    # "the second half of 2026", "mid-2026", "in 2024-09-29..2025-09-27",
    # "in 2030 and 2031".
    + r"|(?i:" + YEAR_CONTEXT_BEFORE + r")(?:\s+|-)(?:" + DATE + "|" + YEARS + r")"
    + NOT_A_QUANTITY + YEAR_TERMINATOR
    # "by", not after a word of change, and only before a hard terminator.
    + r"|(?i:" + NOT_AFTER_A_CHANGE_WORD + r"by)\s+(?:" + DATE + "|" + YEARS + r")"
    + NOT_A_QUANTITY + HARD_TERMINATOR
    # A year, or a list of years, before a year-context word: "2026 guidance",
    # "2026년", "2021 and 2022 guidance".
    + r"|" + r"(?<![$€£¥₩+\-−.,\d])" + YEARS + NOT_A_QUANTITY
    + r"(?=\s*(?i:" + YEAR_CONTEXT_AFTER + r"))"
    + r")(?![A-Za-z0-9])")
# A brace that is not a whole placeholder is a placeholder written wrong, and is
# printed literally if it stands.
BRACE = re.compile(r"[{}]")
DIGIT = re.compile(r"\d")
ANOMALY_ID = re.compile(r"[a-z]+(?:_[a-z]+)*")

# The keys whose values are an analyst's own words.
PROSE_KEYS = ("finding", "verdict", "why", "what", "name", "name_ko", "reading", "reason",
              "history", "assumption")


class AnalysisInputError(Exception):
    """The analysis is not there or not JSON. Never repaired."""


def fold(text: str) -> str:
    """The quote gate's own fold: each whitespace character read as one space,
    one for one, a run never collapsed and nothing trimmed (the owner's decision
    of 2026-09-23, `src/quote_gate.py`)."""
    return quote_gate.folded(text)


def report_ids(text: str) -> set[str]:
    """Every item id a report carries: the `"id"` of each fenced JSON item."""
    found = set()
    for block in re.findall(r"```json\s*(.*?)```", text, re.S):
        try:
            item = json.loads(block)
        except ValueError:
            continue
        items = item if isinstance(item, list) else [item]
        for one in items:
            if isinstance(one, dict) and isinstance(one.get("id"), str) and one["id"].strip():
                found.add(one["id"])
    return found


# --- one string -----------------------------------------------------------------------

def words_problem(text, fields: dict, *, forbidden: tuple[str, ...]) -> str | None:
    """Why these words cannot stand, or None."""
    if text is None or text == "":
        return None
    if not isinstance(text, str):
        return f"{text!r} is not text"
    for path, _ in PLACEHOLDER.findall(text):
        if calculator.field_value(fields, path) is None:
            return f"{{{path}}} is not a number in the calculator this analyst saw"
    bare = PLACEHOLDER.sub(" ", text)
    if BRACE.search(bare):
        return "a brace that is not a whole {path} placeholder"
    bare = ALLOWED_DIGITS.sub(" ", bare)
    if DIGIT.search(bare):
        return (f"a number written in the analyst's own words: "
                f"{bare[max(0, DIGIT.search(bare).start() - 40):][:80]!r}")
    lowered = text.lower()
    for pattern in forbidden:
        found = re.search(pattern, lowered)
        if found:
            return f"a ruled-out word ({found.group(0)!r})"
    return None


def field_cited(fields: dict, path) -> bool:
    """A cited field stands when it is a number, or a cell that states why it has none.

    A citation may point at a figure Python declined to compute -- a cash
    runway is not computed when free cash flow is positive, and the cell says
    so -- because citing the stated reason is reading the calculator. A number
    written into a sentence is held to more: `{path}` must be a number.
    """
    if not isinstance(path, str):
        return False
    if calculator.field_value(fields, path) is not None:
        return True
    node = fields
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
            node = node[int(part)]
        else:
            return False
    return isinstance(node, dict) and any(key in node for key in ("missing", "reason", "note"))


def quote_problem(item: dict, sources: dict[str, str]) -> str | None:
    quote = item.get("quote")
    if quote in (None, ""):
        return None
    named = item.get("quote_from")
    if named not in sources:
        return f"quote_from {named!r} is not a file this analyst saw"
    if fold(quote) not in fold(sources[named]):
        return f"the quote does not string-match {named}"
    return None


def item_problem(item, fields: dict, sources: dict[str, str], upstream: set[str], *,
                 forbidden: tuple[str, ...]) -> str | None:
    """Why one item, of any analysis, is dropped; None when it stands."""
    if not isinstance(item, dict):
        return "the item is not an object"
    for key in PROSE_KEYS:
        problem = words_problem(item.get(key), fields, forbidden=forbidden)
        if problem:
            return f"{key}: {problem}"
    for path in item.get("fields") or []:
        if not field_cited(fields, path):
            return f"fields: {path!r} is not a field of calculator.json"
    for identifier in item.get("evidence") or []:
        if identifier not in upstream:
            return f"evidence: {identifier!r} is not an item of a report this analyst saw"
    problem = quote_problem(item, sources)
    if problem:
        return problem
    return None


# --- the three analyses -------------------------------------------------------------------

def _check_block(payload: dict, key: str, names, fields, sources, upstream, dropped,
                 *, forbidden, required: bool) -> None:
    """A dict of named sections: a failing one keeps its name and loses its words."""
    block = payload.get(key)
    if not isinstance(block, dict):
        block = {}
    for name in names:
        entry = block.get(name)
        if entry is None:
            if required:
                block[name] = {"dropped": "the analyst wrote nothing for it"}
                dropped.append({"where": f"{key}.{name}", "reason": "missing"})
            continue
        problem = item_problem(entry, fields, sources, upstream, forbidden=forbidden)
        if problem:
            block[name] = {"dropped": problem}
            dropped.append({"where": f"{key}.{name}", "reason": problem})
    payload[key] = block


def _check_list(payload: dict, key: str, fields, sources, upstream, dropped, *, forbidden,
                extra=None) -> None:
    kept = []
    for position, item in enumerate(payload.get(key) or []):
        problem = item_problem(item, fields, sources, upstream, forbidden=forbidden)
        if problem is None and extra is not None:
            problem = extra(item)
        if problem:
            dropped.append({"where": f"{key}[{position}]",
                            "id": item.get("id") if isinstance(item, dict) else None,
                            "reason": problem})
        else:
            kept.append(item)
    payload[key] = kept


def _check_summary(payload: dict, fields, dropped, *, forbidden) -> None:
    summary = payload.get("summary_ko")
    if not isinstance(summary, dict):
        payload["summary_ko"] = {}
        return
    for name, text in list(summary.items()):
        problem = words_problem(text, fields, forbidden=forbidden)
        if problem:
            summary[name] = None
            dropped.append({"where": f"summary_ko.{name}", "reason": problem})


def _limits(payload: dict, kind: str, dropped: list) -> None:
    if payload.get("limits") != LIMITS[kind]:
        dropped.append({"where": "limits", "reason": "not the rules version's sentence; "
                                                     "replaced by it"})
    payload["limits"] = LIMITS[kind]


def anomaly_problem(areas: tuple[str, ...]):
    def check(item: dict) -> str | None:
        if not item.get("evidence") and not item.get("fields"):
            return ("the anomaly cites no report item and no calculator field, so it "
                    "rests on nothing Python can check")
        identifier = item.get("id")
        if not isinstance(identifier, str) or not ANOMALY_ID.fullmatch(identifier):
            return f"the anomaly id {identifier!r} is not a plain name"
        if item.get("area") not in areas:
            return f"the area {item.get('area')!r} is not one of {', '.join(areas)}"
        if not identifier.startswith(item["area"] + "_"):
            return "the anomaly id does not start with its area"
        outcome = item.get("numbers_vs_prose")
        if outcome is not None and outcome not in OUTCOMES:
            return f"numbers_vs_prose {outcome!r} is not one of {', '.join(OUTCOMES)}"
        return None
    return check


def adjustment_problem(fields: dict):
    def check(item: dict) -> str | None:
        if item.get("direction") not in DIRECTIONS:
            return f"direction {item.get('direction')!r} is not one of {', '.join(DIRECTIONS)}"
        if item.get("applies_to") not in APPLIES_TO:
            return f"applies_to {item.get('applies_to')!r} is not one of {', '.join(APPLIES_TO)}"
        if calculator.adjustment_amount(fields, item.get("calculator_field")) is None:
            return (f"calculator_field {item.get('calculator_field')!r} is not a dollar "
                    f"amount under {' or '.join(calculator.ADJUSTMENT_ROOTS)}")
        if not item.get("quote"):
            return "an adjustment carries no quote"
        return None
    return check


def reconciliation_problem(notes_ids: set[str], numbers_ids: set[str]):
    def check(item: dict) -> str | None:
        if item.get("outcome") not in OUTCOMES:
            return f"outcome {item.get('outcome')!r} is not one of {', '.join(OUTCOMES)}"
        if item.get("notes_item") not in notes_ids:
            return f"notes_item {item.get('notes_item')!r} is not an item of report_notes_text.md"
        for identifier in item.get("numbers_items") or []:
            if identifier not in numbers_ids:
                return f"numbers_items: {identifier!r} is not an item of report_numbers.md"
        return None
    return check


def paragraph_ids(sources: dict[str, str]) -> set[str]:
    """Every paragraph id printed on an `[id]` line of the input files."""
    found = {match.group(1) for text in sources.values()
             for match in re.finditer(r"^\[([^\]\s]+)\]", text, re.M)}
    found |= {match.group(1) for text in sources.values()
              for match in re.finditer(r'"paragraph_id":\s*"([^"]+)"', text)}
    return found


def check(kind: str, payload: dict, *, fields: dict, sources: dict[str, str],
          excluded: set[str] | frozenset = frozenset(), paragraph_ids: bool = False) -> dict:
    """The analysis with every failing item dropped, and the list of drops.

    `excluded` is the ids the quote gate dropped from the reports: they are still
    printed in the report files the analyst read, and a citation of one is a
    citation of an item that did not stand.
    """
    if not isinstance(payload, dict):
        raise AnalysisInputError(f"the {kind} analysis is not a JSON object")
    payload = copy.deepcopy(payload)
    notes_ids = report_ids(sources.get("report_notes_text.md", "")) - set(excluded)
    numbers_ids = report_ids(sources.get("report_numbers.md", "")) - set(excluded)
    if paragraph_ids:
        # The single-agent control has no upstream report: it cites the
        # paragraphs of its own input, and each is verified by its quote.
        notes_ids = numbers_ids = globals()["paragraph_ids"](sources)
    upstream = notes_ids | numbers_ids
    dropped: list[dict] = []
    forbidden = FORBIDDEN_EVERYWHERE + (FORBIDDEN_IN_VALUATION if kind == "valuation" else ())
    if kind == "accounting":
        _check_block(payload, "areas", ACCOUNTING_AREAS, fields, sources, upstream, dropped,
                     forbidden=forbidden, required=True)
        _check_list(payload, "reconciliation", fields, sources, upstream, dropped,
                    forbidden=forbidden, extra=reconciliation_problem(notes_ids, numbers_ids))
        _check_list(payload, "anomalies", fields, sources, upstream, dropped,
                    forbidden=forbidden, extra=anomaly_problem(ACCOUNTING_AREAS))
        _check_list(payload, "adjustments", fields, sources, upstream, dropped,
                    forbidden=forbidden, extra=adjustment_problem(fields))
    elif kind == "financial":
        _check_block(payload, "sections", FINANCIAL_SECTIONS, fields, sources, upstream,
                     dropped, forbidden=forbidden, required=True)
        for key in ("dupont", "path_to_distress"):
            entry = payload.get(key)
            problem = ("the analyst wrote nothing for it" if entry is None else
                       item_problem(entry, fields, sources, upstream, forbidden=forbidden))
            if problem:
                payload[key] = {"dropped": problem}
                dropped.append({"where": key, "reason": problem})
        _check_list(payload, "anomalies", fields, sources, upstream, dropped,
                    forbidden=forbidden, extra=anomaly_problem(FINANCIAL_AREAS))
    elif kind == "valuation":
        _check_block(payload, "readings", (), fields, sources, upstream, dropped,
                     forbidden=forbidden, required=False)
        payload.pop("readings", None)
        for key in VALUATION_KEYS:
            entry = payload.get(key)
            problem = ("the analyst wrote nothing for it" if entry is None else
                       item_problem(entry, fields, sources, upstream, forbidden=forbidden))
            if problem:
                payload[key] = {"dropped": problem}
                dropped.append({"where": key, "reason": problem})
        _check_list(payload, "most_sensitive", fields, sources, upstream, dropped,
                    forbidden=forbidden)
    else:
        raise AnalysisInputError(f"no analysis is called {kind!r}")
    _check_summary(payload, fields, dropped, forbidden=forbidden)
    _limits(payload, kind, dropped)
    payload["normalized_quotes"] = normalized_quotes(payload, sources)
    payload["dropped_items"] = dropped
    payload["dropped_count"] = len(dropped)
    return payload


# --- the valuation analyst's first pass --------------------------------------------------

def check_assumptions(payload: dict, *, fields: dict, sources: dict[str, str]) -> dict:
    """Every driver a number, every driver with a reason and a quote or a field.

    A scenario whose drivers fail is dropped whole and counted: the DCF runs on
    the six drivers together or not at all, and Python never fills one in.
    """
    if not isinstance(payload, dict):
        raise AnalysisInputError("assumptions.json is not a JSON object")
    payload = copy.deepcopy(payload)
    dropped = []
    scenarios = payload.get("scenarios") or {}
    for name in calculator.SCENARIOS:
        scenario = scenarios.get(name)
        problem = None
        if not isinstance(scenario, dict):
            problem = "no such scenario"
        else:
            reasons = scenario.get("reasons") or {}
            for driver in calculator.DRIVERS:
                value = scenario.get(driver)
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    problem = f"{driver} is not a number"
                    break
                reason = reasons.get(driver)
                if not isinstance(reason, dict) or not reason.get("reason"):
                    problem = f"{driver} carries no reason"
                    break
                if not reason.get("quote") and not reason.get("fields"):
                    problem = f"{driver} carries neither a quote nor a calculator field"
                    break
                problem = item_problem(reason, fields, sources, set(),
                                       forbidden=FORBIDDEN_EVERYWHERE + FORBIDDEN_IN_VALUATION)
                if problem:
                    problem = f"{driver}: {problem}"
                    break
        if problem:
            dropped.append({"where": f"scenarios.{name}", "reason": problem})
            scenarios.pop(name, None)
    payload["scenarios"] = scenarios
    overrides = payload.get("wacc_overrides") or {}
    for name, chosen in list(overrides.items()):
        problem = None
        if name != "pre_tax_cost_of_debt":
            problem = "only the pre-tax cost of debt may be chosen"
        elif not isinstance(chosen, dict) or not isinstance(chosen.get("value"), (int, float)):
            problem = "no value"
        else:
            problem = quote_problem(chosen, sources) or (None if chosen.get("quote")
                                                         else "no quote")
        if problem:
            dropped.append({"where": f"wacc_overrides.{name}", "reason": problem})
            overrides.pop(name)
    payload["wacc_overrides"] = overrides
    payload["dropped_items"] = dropped
    payload["dropped_count"] = len(dropped)
    return payload


def normalized_quotes(payload, sources: dict[str, str]) -> int:
    """How many standing quotes matched only through the whitespace fold, counted
    as the quote gate counts them."""
    count = 0

    def walk(node):
        nonlocal count
        if isinstance(node, dict):
            if isinstance(node.get("quote"), str) and node.get("quote_from") in sources:
                if quote_gate.folded_characters(node["quote"], sources[node["quote_from"]]):
                    count += 1
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
    walk({key: value for key, value in payload.items() if key != "dropped_items"})
    return count


def read_sources(agent_dir: Path, names: tuple[str, ...]) -> dict[str, str]:
    """The files an analyst saw, by name, as the text it saw."""
    out = {}
    for name in names:
        path = Path(agent_dir) / name
        if path.is_file():
            out[name] = path.read_text(encoding="utf-8")
    return out


SOURCES = {
    "accounting": ("report_numbers.md", "report_notes_text.md"),
    "financial": ("report_numbers.md", "report_notes_text.md"),
    "valuation": ("input_mdna.md", "input_8k.md", "analysis_accounting.json",
                  "analysis_financial.json", "report_numbers.md", "report_notes_text.md"),
    "assumptions": ("input_mdna.md", "input_8k.md", "analysis_accounting.json",
                    "analysis_financial.json"),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="drop and count what an analysis cannot stand on")
    parser.add_argument("--kind", required=True,
                        choices=["accounting", "financial", "valuation", "assumptions"])
    parser.add_argument("--agent-dir", required=True)
    parser.add_argument("--written", required=True, help="the file the analyst wrote")
    parser.add_argument("--calculator", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    try:
        payload = json.loads(Path(args.written).read_text(encoding="utf-8"))
        fields = json.loads(Path(args.calculator).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"analysis_check: {exc}", file=sys.stderr)
        return BAD_INPUT
    sources = read_sources(Path(args.agent_dir), SOURCES[args.kind])
    try:
        out = (check_assumptions(payload, fields=fields, sources=sources)
               if args.kind == "assumptions" else
               check(args.kind, payload, fields=fields, sources=sources))
    except AnalysisInputError as exc:
        print(f"analysis_check: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    print(f"analysis_check: {args.kind} -- {out['dropped_count']} dropped", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
