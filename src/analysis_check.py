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
- its enumerated values are the enumerated values;
- and, anywhere in the file and not only in the items above, the owner's
  graders' own rules hold: a quote stands in one paragraph, one kept report
  item or one string value of the file it names; every `{path}` is a number;
  every `evidence` is a list of items that stood; no ruled-out word sits inside
  another; no key scores or ranks (`owner_problems`).

A section or an area that fails keeps its key and loses its words, which are
replaced by the reason, because an area of the accounting analysis is never
skipped and a dropped area must still say that it was dropped. The `limits`
sentence must be the rules version's own, character for character.

    python3.12 -m src.analysis_check --kind accounting --agent-dir <dir> \\
        --written <the file the analyst wrote> --calculator <calculator.json> \\
        --out analysis_accounting.json --run <run directory>

`--run` names the run directory the agent directory belongs to: the manifest's
drop rows are read from it, keyed by report, so a citation of an id the quote
gate dropped is refused here as in the pipeline, and for the valuation kinds
the run's full `input_mdna.md` and `input_8k.md` are read as `filing`, the
other side a quote is held to. A valuation or assumptions kind without `--run`
is refused: the valuation analyst's copies are trimmed to the flagged
paragraphs, written one after the other, and the trimmed copy alone cannot tell
a quote running across the junction of two blocks that were not adjacent from
one the filing printed. The
accounting and financial kinds run without it, and say that no drop row was
read.
"""

from __future__ import annotations

import argparse
import copy
from collections.abc import Mapping
import json
import math
import re
import sys
from pathlib import Path

try:
    from src import agent_inputs, calculator, interpreter_pin, quote_gate
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import agent_inputs, calculator, interpreter_pin, quote_gate

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
# A bare four-digit number, 19xx or 20xx, is a year only when the words around it
# say so; its value never decides, because a net-zero target "by 2050" and a
# comparison "since 1929" are years the same way "in 2026" is. Two kinds of
# words say so.
#
# A year-context word or phrase before it: a period phrase ("first half of",
# "second half of", "first quarter of" .. "fourth quarter of", "year-end",
# "quarter-end", "end of", "start of", "beginning of", "close of", "due", a month
# name) or a context word ("in", "for", "through", "since", "until", "year",
# "during", "early", "late", "mid", "as of", "half of" with no ordinal, "months
# of", "weeks of", "quarters of", "회계연도"). Each opens a counted noun phrase as
# readily as a date -- "in 2030 orders", "the second half of 2048 stores", "due
# 2030 vendors" are counts; "in 2030.", "the second half of 2026," years -- so
# after any of them the number is a year only when a year-terminator follows:
# the end of the text, punctuation or any character outside the Latin alphabet,
# a connector ("and", "or", "to", "through", a dash, ".."), another year, a
# year-context-after word, a month, a function word or time word ("the", "was",
# "quarter", "amendment"), one of the few verbs the published analyses write
# directly after a year ("turns", "recur", "carries", "carried", "printed",
# "assumed", "extended", "reverses", "continues", "holds"), which cannot open a counted
# noun phrase, or a hyphenated adjective that is itself followed by the end of
# the text, a full stop, a function word or one of those verbs ("the second half
# of 2025 loss-making recur", GNRC's bear case) -- never a noun or an adjective
# that can open one: "in 2030 orders", "sold in 2048 high-margin units", "in
# 2030 low-cost stores" and "the year-end 2025 balance" are counts to the rule,
# while "for 2027, a backlog", "the first half of 2027 turns", "in 2030." and
# "in 2030 and 2031" are years. "of" alone is not a year context -- "inventory
# of 2048" is a count -- so it counts only inside the phrases above and after a
# noun that names a year's measure: "margin of", "margins of", "growth of",
# "surge of", which the GNRC valuation analyst wrote ("the margin of 2023", "the
# growth of 2021 and 2022", "the pandemic-era surge of 2021"), and the elided
# "and of" that continues one of them ("the margin of the year before last and
# of 2022"); "revenue of 2048" and "inventory of 2048" stay counts. "to" is not
# one -- "rose to 2030 orders" is a count -- but after a fiscal year it is the
# connector of a range, and the range takes the terminator ("the flat stretch
# of fiscal 2022 to 2025,", AAPL's base case; "fiscal 2022 to 2048 units" keeps
# its count). "was" is not one either -- "the headcount was 2048" is a count --
# unless the clause's subject is a year: "year" written earlier in the same
# clause, no punctuation between ("the only fiscal year in the record that grew
# faster was 2021 at", AAPL's bull case), where "year-end" is not "year". And
# "by" is not one at all, because it names an amount as often as a date ("cut
# headcount by 2030.", "reduced inventory by 2048,", "up by 1999") and no word
# around it tells the two apart -- an analyst who means the date writes "by the
# end of 2030" or "in 2030", which the words above read. "fiscal", "calendar",
# "FY" and "Q1".."Q4" are the alternatives above.
#
# A year-context-after word, whole: "fiscal year", "year-end", "guidance",
# "outlook", a possessive ("2022's"), a month name, or the Korean 년, 회계연도, 상반기, 하반기,
# 분기, 말, 기준 -- "2050년", "2055 fiscal year" and "2026 December" are years
# whatever the value, while a word that merely starts like a month's short form
# is no context, nor is a verb spelled like a month in lower case: "2048
# marketing staff", "2030 novel products", "inventory of 2048 declined",
# "inventory of 2048 may fall" and "2048 march" are counts; "2026 May" and "in
# 2026 May" are years.
#
# A range or a list of four-digit numbers is years only when a member has a
# year-context word of its own and the terminator follows the list: "in 2030
# and 2031" and "2021 and 2022 guidance" are years, "inventory of 2021 and
# 2022", "the second half of 2025 and 2048 stores" and a bare "2024–2026" are
# numbers. A year is never written after a currency sign, a sign, a decimal
# point or a digit, never before a decimal, and never before a quantity word,
# which keeps "in 2048 units" and "by 1950 basis points" numbers whatever word
# stands before them. A Korean unit written against the number -- 억, 만, 천,
# 원, 개, 명, 주, 건, 대 -- is a quantity word too: "2025억" and "2048개" are
# counts, "2025년" a year; written apart it is a word of its own ("회계연도
# 2025 대비"). "2026 stores", "€2026", "USD 2026", "2026 Million", "2026 bn"
# and "-2026" have no year context and are numbers.
YEAR = r"(?:19|20)\d{2}"
DATE = r"(?:19|20)\d{2}-\d{2}-\d{2}"
MONTH = (r"(?:January|February|March|April|May|June|July|August|September|October"
         r"|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)")
# A clause: no full stop, semicolon, colon, comma or digit crossed, so a count
# between the context word and the number is never hidden under it.
WITHIN_A_CLAUSE = r"[^.;:,\d]*?"
YEAR_CONTEXT_BEFORE = (
    r"(?:(?:first|second|1st|2nd)[- ]half(?:\s+of)?"
    r"|(?:first|second|third|fourth|1st|2nd|3rd|4th)[- ]quarter(?:\s+of)?"
    r"|(?:year|quarter|period)[- ]end(?:\s+of)?|end of|start of|beginning of|close of"
    r"|due|" + MONTH
    + r"|in|for|through|since|until|year|during|early|late|mid|as of|회계연도"
    r"|half of|(?:months?|weeks?|quarters?) of"
    # A noun that names a year's measure before "of", and the elided "and of" that
    # continues it: GNRC's valuation analyst wrote "below the margin of 2023", "the
    # margins of 2021, 2022 and", "below the growth of 2021 and 2022", "the
    # pandemic-era surge of 2021" and "the margin of the year before last and of
    # 2022". "inventory of 2048" has no such noun and stays a count.
    r"|(?:margins?|growth|surge) of(?:\s" + WITHIN_A_CLAUSE + r"\sand of)?"
    # "was" after a subject that is a year, "year" earlier in the same clause: AAPL's
    # valuation analyst wrote "the only fiscal year in the record that grew faster
    # was 2021 at". "year-end" is not "year", and "the headcount was 2048" has no
    # year in its subject.
    r"|year(?![-A-Za-z0-9])" + WITHIN_A_CLAUSE + r"\swas)")
# A month after a year is a month only capitalised, whatever case the group around
# it reads in: "may" and "march" the verbs are not months.
# "peak" names a year's high as "guidance" names its forecast: "that window starts
# at the 2022 peak" (GNRC's base case); a peak count is written "the peak of 2048".
YEAR_CONTEXT_AFTER = (r"(?:fiscal year|year-end|guidance|outlook|peak|['’]s|(?-i:" + MONTH + r")"
                      r"|년|회계연도|상반기|하반기|분기|말|기준)")
CONNECTOR = r"(?:and|or|to|through)"
FUNCTION_OR_TIME_WORD = (
    r"(?:the|an?|its?|this|that|these|those|which|when|where|while|as|at|with|than|from"
    r"|on|in|for|but|because|so|there|it|he|she|they|we|was|were|is|are|has|had|have"
    r"|will|would|could|should|may|might|can|did|does|do|ran|saw|ended|began|closed"
    r"|opened|under|against|after|before|over|into|onto|by|until|through|during|alone"
    r"|only|also|still|then|now|quarter|half|period|fiscal|annual|filing|report|results"
    r"|release|amendment|figure|figures|trough|window|date|dates"
    # "once" the conjunction: "the first half of 2026 once the refund is removed"
    # (GNRC's bull case).
    r"|once)")
# Verbs the eight published analyses write directly after a year; a verb cannot
# open a counted noun phrase. No wider.
VERB_AFTER_A_YEAR = (r"(?:turns|recur|recurs|carries|carried|printed|assumed|extended|reverses"
                     r"|continues|holds"
                     # "the level the first half of 2026 earned" (GNRC's base case)
                     r"|earned)")
QUANTITY_WORD = (r"(?:million|billion|trillion|thousand|percent|per\s*cent|%|units|basis"
                 r"|points|bps|shares|dollars|employees|customers|days|times|bn|mn|mm)")
KOREAN_UNIT = r"(?:억|만|천|원|개|명|주|건|대)"
NOT_A_QUANTITY = (r"(?![.,]\d)(?!\s*(?i:" + QUANTITY_WORD + r"))(?!" + KOREAN_UNIT + r")")
LIST_SEPARATOR = r"(?:\s*[-–—]\s*|\s*,\s*|\s*,?\s*(?i:" + CONNECTOR + r")\s+)"
YEARS = YEAR + r"(?:" + LIST_SEPARATOR + YEAR + r")*"
# A hyphenated adjective after a year is a terminator only when what follows it
# cannot be the noun it modifies -- the end of the text, a full stop, a function
# word or a verb from the list above: "the second half of 2025 loss-making recur"
# (GNRC's bear case) is a year, "sold in 2048 high-margin units" a count. A
# connector is not enough, because "high-margin and low-cost units" is one
# adjective phrase; nor is a comma. A terminator word ends at a hyphen as at a
# letter, or "once" would read the start of "once-off" in "the first half of
# 2048 once-off units".
HYPHENATED_ADJECTIVE = r"[A-Za-z]+(?:-[A-Za-z]+)+"
AFTER_A_HYPHENATED_ADJECTIVE = (r"(?:$|[.;:]|(?i:" + FUNCTION_OR_TIME_WORD + "|"
                                + VERB_AFTER_A_YEAR + r")(?![A-Za-z0-9-]))")
YEAR_TERMINATOR = (r"(?=\s*(?:$|[^\sA-Za-z0-9]|" + YEAR + r"|(?i:" + CONNECTOR + "|"
                   + FUNCTION_OR_TIME_WORD + "|" + YEAR_CONTEXT_AFTER + "|" + VERB_AFTER_A_YEAR
                   + r")(?![A-Za-z0-9-])"
                   + r"|" + HYPHENATED_ADJECTIVE + r"(?![A-Za-z0-9])\s*"
                   + AFTER_A_HYPHENATED_ADJECTIVE + r"))")
ALLOWED_DIGITS = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    r"10-K|10-Q|8-K|COVID-19"
    r"|(?:19|20)\d{2}-\d{2}-\d{2}"
    # A fiscal year, or a range or list of years opening with one and followed by a
    # year-terminator: "fiscal 2025", "the flat stretch of fiscal 2022 to 2025," (AAPL's
    # base case). "fiscal 2022 to 2048 units" reads "fiscal 2022" and leaves the count.
    r"|(?:[Ff]iscal|[Cc]alendar|FY)[\s-]*(?:" + YEARS + NOT_A_QUANTITY + YEAR_TERMINATOR
    + r"|(?:19|20)\d{2})"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November"
    r"|December)\s+\d{1,2},?\s+(?:19|20)\d{2}"
    r"|Items? \d{1,2}(?:\.\d{2})?[A-C]?(?!\s*(?:million|billion|thousand|percent|%|units))"
    r"|(?:ASC|Topic)\s+\d{3}(?:-\d{2,3})*(?!\s*(?:million|billion|thousand|percent|%|units))"
    r"|ASU\s+\d{4}-\d{2}"
    r"|Notes? \d{1,2}(?![\d.,])(?!\s*(?:million|billion|thousand|percent|%|units))"
    r"|Q[1-4](?:\s+(?:of\s+)?(?:fiscal\s+)?(?:19|20)\d{2})?"
    r"|FY\d{2,4}"
    # A year, a date, a range or a list of years after a year-context word or
    # phrase, joined by whitespace or a hyphen, and followed by a year-terminator:
    # "in 2026", "the second half of 2026,", "for 2027, a backlog", "mid-2026",
    # "second-half-2025 and", "in 2024-09-29..2025-09-27", "in 2030 and 2031".
    + r"|(?i:" + YEAR_CONTEXT_BEFORE + r")(?:\s+|-)(?:" + DATE + "|" + YEARS + r")"
    + NOT_A_QUANTITY + YEAR_TERMINATOR
    # A year, or a list of years, before a whole year-context-after word: "2026
    # guidance", "2026년", "2050년", "2026 December", "2021 and 2022 guidance".
    + r"|" + r"(?<![$€£¥₩+\-−.,\d])" + YEARS + NOT_A_QUANTITY
    + r"(?=\s*(?i:" + YEAR_CONTEXT_AFTER + r")(?![A-Za-z0-9-]))"
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


def quote_problem(item: dict, sources: dict[str, str],
                  filing: dict[str, str] | None = None) -> str | None:
    """Why the item's quote fails, or None.

    The quote is held to the file the analyst saw, under the name it gives. For
    the valuation analyst's MD&A and earnings release, `filing` holds the run's
    full file under the same name, and the quote is held to that too: the copy
    the analyst saw is cut down to the flagged paragraphs, written one after
    the other with nothing between them (`src/agent_inputs.py`), so a quote
    that runs off one kept paragraph across the next one's `[id]` line, where
    the two were not adjacent in the filing, string-matches the copy and
    nothing the filing printed. The reason still says "seam": that junction.
    """
    quote = item.get("quote")
    if quote is None or quote == "":
        return None
    if not isinstance(quote, str):
        return f"the quote is {type(quote).__name__}, not text"
    named = item.get("quote_from")
    if not isinstance(named, str) or named not in sources:
        return f"quote_from {named!r} is not a file this analyst saw"
    if fold(quote) not in fold(sources[named]):
        return f"the quote does not string-match {named}"
    if filing and named in filing and fold(quote) not in fold(filing[named]):
        return (f"the quote string-matches the trimmed {named} and not the filing: it runs "
                "across a seam between two paragraphs that were not adjacent")
    return None


def item_problem(item, fields: dict, sources: dict[str, str], upstream: set[str], *,
                 forbidden: tuple[str, ...], filing: dict[str, str] | None = None,
                 fallen: frozenset[str] | set[str] = frozenset()) -> str | None:
    """Why one item, of any analysis, is dropped; None when it stands.

    `fallen` is every id the quote gate dropped from any report this analyst
    saw. A bare citation names an item by id alone, and a dropped item may
    still be printed in its report beside a kept one, so by id alone such a
    citation would name two printed items, one of which fell -- the gate's
    own reason for dropping a twin. It is refused, whatever else carries the id;
    a reconciliation row names the report and is held to that report's items.
    """
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
        if identifier in fallen:
            return (f"evidence: {identifier!r} is an id the quote gate dropped from a report "
                    "this analyst saw, so by id alone it does not name one standing item")
        if identifier not in upstream:
            return f"evidence: {identifier!r} is not an item of a report this analyst saw"
    problem = quote_problem(item, sources, filing)
    if problem:
        return problem
    return None


# --- the three analyses -------------------------------------------------------------------

def _check_block(payload: dict, key: str, names, fields, sources, upstream, dropped,
                 *, forbidden, required: bool, filing=None, fallen=frozenset()) -> None:
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
        problem = item_problem(entry, fields, sources, upstream, forbidden=forbidden,
                               filing=filing, fallen=fallen)
        if problem:
            block[name] = {"dropped": problem}
            dropped.append({"where": f"{key}.{name}", "reason": problem})
    payload[key] = block


def _check_list(payload: dict, key: str, fields, sources, upstream, dropped, *, forbidden,
                extra=None, filing=None, fallen=frozenset()) -> None:
    kept = []
    for position, item in enumerate(payload.get(key) or []):
        problem = item_problem(item, fields, sources, upstream, forbidden=forbidden,
                               filing=filing, fallen=fallen)
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


# --- the owner's rules over the whole payload ------------------------------------------
#
# The checks above walk the items the schema names. The owner's graders walk every
# key and every string of the published file (`evals/regression/mechanical.py`
# quotes_resolve, cited_items_exist and cited_numbers_exist; `coverage.py`
# forbidden_words and no_combined_score), so a quote nested under an item, a
# placeholder under a key that is not prose, an evidence that is not a list, a
# ruled-out word inside another word or a key that scores were published past
# this gate and failed there. Each rule is written out here as the grader writes
# it -- src imports nothing from evals -- and `tests/test_gate_matches_graders.py`
# holds every copy equal to the grader's and the two to the same verdict. A
# departure anywhere drops the unit that holds it: a list item is removed, an
# area, a section or a single block keeps its key and says why it was dropped, a
# scenario or an override is removed, a summary sentence is emptied, and a key the
# schema does not name is removed.

ACCUSATION = re.compile(r"fraud\w*|manipulat\w*|분식|회계\s*부정|사기\s*행위|사기적|사기죄|조작",
                        re.IGNORECASE)
RECOMMENDATION = re.compile(r"\balpha\b|\bbuy\b(?!-)|\bsell\b(?!-)"
                            r"|매수\s*(추천|의견|권)|매도\s*(추천|의견|권)", re.IGNORECASE)
SCORE_KEY = re.compile(r"(^|_)(score|composite|rank|ranking|overall)($|_)")
CITATION_KEY = re.compile(r"(.*_)?items?|(.*_)?evidence")
LABEL_KEYS = ("id", "area", "evidence", "quote_from", "paragraph_id", "frame", "severity",
              "upstream_item_id", "label", "window", "kind")
FOLLOWS_PATHS = ("fields",)
# what the gate writes about itself, never an analyst's words
BOOKKEEPING = ("dropped_items", "dropped_count", "normalized_quotes")
# the blocks of named entries, and what a departure inside one entry does to it
BLOCKS = {"areas": "replace", "sections": "replace", "readings": "replace",
          "scenarios": "remove", "wacc_overrides": "remove", "summary_ko": "empty"}
SINGLE_ITEMS = ("dupont", "path_to_distress") + VALUATION_KEYS
# what the memo prints of an analysis, which is held to the recommendation words
# whatever the analysis (`src/memo.py`): the summary sentences, an anomaly's name,
# an adjustment's name
MEMO_LISTS = ("anomalies", "adjustments")
MEMO_NAMES = ("name", "name_ko")


def walk_strings(node, where: str = ""):
    """Every string of a JSON tree, with where it sits, written as the owner's
    grader writes the place (`evals/common.py`)."""
    if isinstance(node, str):
        yield where, node
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, f"{where}.{key}" if where else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, f"{where}[{index}]")


def _items_of(text: str) -> list[dict]:
    """A report's fenced items, a list block's elements each, as the grader reads them."""
    items = []
    for block in re.findall(r"```json\s*(.*?)```", text, re.S):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        items += [one for one in (data if isinstance(data, list) else [data])
                  if isinstance(one, dict)]
    return items


def json_labels(tree) -> set[str]:
    """Every string an analysis carries under a label key, as printed and bare."""
    out = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in LABEL_KEYS:
                    for one in (value if isinstance(value, list) else [value]):
                        if isinstance(one, str):
                            out.add(json.dumps(one))
                            out.add(one)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(tree)
    return out


def quote_units(name: str, text: str, kept: dict | None = None):
    """The units a quote can stand in, as (text, keys, metadata): one `[id]`
    paragraph of a prose input (the text before the first is no unit), one kept
    item of a reader report (its string values; prose outside the fences and an
    item the gate dropped are no unit), one string value of a JSON file. A quote
    is of one thing one file said, not of the file."""
    if name.startswith("report_"):
        out = []
        for item in _items_of(text):
            if kept is not None and item.get("id") not in kept.get(name, ()):
                continue
            printed = json.dumps(item)
            out.append((" ␟ ".join(fold(value) for _, value in walk_strings(item)),
                        quote_gate.row_keys(printed), quote_gate.row_metadata(printed)))
        return out
    if name.endswith(".md") and agent_inputs.ID_LINE.search(text):
        return [(fold(body), set(), set())
                for body in quote_gate.owner_paragraphs(text).values()]
    if name.endswith(".md"):
        return [(fold(block), set(), set()) for block in re.split(r"\n\s*\n", text)
                if block.strip()]
    if name.endswith(".json"):
        try:
            tree = json.loads(text)
        except ValueError:
            return []
        printed = json.dumps(tree)
        labels = quote_gate.row_metadata(printed) | json_labels(tree)
        return [(fold(value), quote_gate.row_keys(printed), labels)
                for _, value in walk_strings(tree)]
    return [(fold(text), set(), set())]


def unit_problem(seen: dict[str, str], quote: str, kept: dict | None = None) -> str | None:
    """Why an analyst's quote stands in no one unit of the files it names, or None."""
    wanted, found = fold(quote), False
    for name, text in seen.items():
        for body, keys, metadata in quote_units(name, text, kept):
            if wanted in body:
                found = True
                if quote_gate.says_something(quote, keys, "", metadata):
                    return None
    if found:
        return "the quote carries only key names, the item's metadata or the id, nothing it says"
    return "the quote is in no one paragraph, value or kept report item of the file it names"


def kept_report_items(sources: dict[str, str], left_out) -> dict[str, set[str]]:
    """Per reader report the analyst saw, the ids that stood: every item id of the
    report less the gate's drops for it and less any id the report carries twice
    (`left_out(report)` names the drops), the owner's `kept_items`."""
    out = {}
    for report in ("report_numbers.md", "report_notes_text.md"):
        ids = [item["id"] for item in _items_of(sources.get(report, ""))
               if isinstance(item.get("id"), str) and item["id"].strip()]
        out[report] = {i for i in ids if ids.count(i) == 1 and i not in left_out(report)}
    return out


def owner_problems(payload: dict, *, kind: str, fields: dict, sources: dict[str, str],
                   filing: dict[str, str] | None, kept: dict | None,
                   citable: set[str] | None) -> list[tuple[tuple, str]]:
    """Every departure from the owner's rules anywhere in the payload, as (the
    path to it, why): a quote that does not stand in one unit of the file it
    names; a `{path}` that is not a number, or a `fields` entry that is no field,
    in any string; a ruled-out word in any string but a quote; a key that scores
    or ranks; and, when `citable` is given, an `evidence` that is not a list or
    any key naming reader items (the owner's CITATION_KEY) that names an id not
    in it -- the ids that stood in either report, read together as the owner
    reads them."""
    found: list[tuple[tuple, str]] = []
    recommend_everywhere = kind in ("valuation", "assumptions")

    def held_quote(node: dict) -> str | None:
        """Why a quote written on this object does not stand, or None."""
        quote = node.get("quote")
        if not isinstance(quote, str) or not quote.strip():
            return None
        why = quote_problem(node, sources, filing)
        if why is None:
            why = unit_problem({node["quote_from"]: sources[node["quote_from"]]}, quote, kept)
        return why

    def key_rules(key, value, here: tuple, cited: bool) -> None:
        """What a key says by itself: one that scores or ranks, and one that
        names reader items (an `evidence` that is not a list, any CITATION_KEY
        naming an id that did not stand)."""
        if SCORE_KEY.search(str(key).lower()):
            found.append((here, f"{_where(here)}: a key that adds the frames together "
                                "or ranks, which no analysis carries"))
        if cited and citable is not None and key == "evidence":
            if not isinstance(value, list):
                found.append((here, f"{_where(here)}: evidence is not a list"))
            else:
                cite(value, here)
        elif cited and citable is not None and CITATION_KEY.fullmatch(str(key)):
            cite(value if isinstance(value, list) else [value], here)

    def walk(node, path: tuple, cited: bool = True):
        where = _where(path)
        if isinstance(node, dict):
            why = held_quote(node) if cited else None
            if why:
                found.append((path, f"{where or 'quote'}: {why}"))
            for key, value in node.items():
                here = path + (key,)
                # a `dropped_items` below the top is the analyst's, not the gate's,
                # and the owner reads it as its graders do: its words, its
                # placeholders and its keys like any other (forbidden_words,
                # cited_numbers_exist and no_combined_score leave out only the top
                # one), its quotes and its citations not at all (`quoted` and
                # cited_items_exist pass over one at any depth)
                inner = cited and key != "dropped_items"
                key_rules(key, value, here, inner)
                walk(value, here, inner)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, path + (index,), cited)
        elif isinstance(node, str):
            text(node, path)

    def cite(values, path):
        for cited in values:
            if cited is None:
                continue
            if not isinstance(cited, str) or cited not in citable:
                found.append((path, f"{_where(path)}: {cited!r} is not an item that stood "
                                    "in a report this analyst saw"))
                return

    def text(value: str, path: tuple):
        where = _where(path)
        last = next((part for part in reversed(path) if isinstance(part, str)), "")
        if path and path[-1] == "dropped":
            return                      # the gate's own note on what it dropped
        paths = PLACEHOLDER.findall(value)
        for name, _ in paths:
            if calculator.field_value(fields, name) is None:
                found.append((path, f"{where}: {{{name}}} is not a number in the calculator "
                                    "this analyst saw"))
                return
        if where.split("[")[0].endswith(FOLLOWS_PATHS) and not paths \
                and not field_cited(fields, value):
            found.append((path, f"{where}: {value!r} is not a field of the calculator"))
            return
        if path and path[-1] == "quote":
            return                      # the filer's words, which the quote rule holds
        patterns = [ACCUSATION]
        if recommend_everywhere or path[:1] == ("summary_ko",) or (
                path[:1] and path[0] in MEMO_LISTS and last in MEMO_NAMES):
            patterns.append(RECOMMENDATION)
        for pattern in patterns:
            hit = pattern.search(value)
            if hit:
                found.append((path, f"{where}: a ruled-out word ({hit.group(0)!r})"))
                return

    # what the gate writes over once this walk is done, so it is never published as
    # the analyst wrote it: the bookkeeping and the rules version's limits sentence
    # in an analysis; only the drop list and its count in the assumptions, whose
    # every other key is published as written and read by the owner
    overwritten = (("dropped_items", "dropped_count") if kind == "assumptions"
                   else BOOKKEEPING + ("limits",))
    # the analysis object itself is held as any object in it is: a quote written
    # on it (the owner's `quoted` yields the root too), and each top-level key
    why = held_quote(payload)
    if why:
        found.append((("quote",), f"quote: {why}"))
    for key, value in payload.items():
        if key in overwritten:
            continue
        if SCORE_KEY.search(str(key).lower()):
            found.append(((key,), f"{key}: a key that adds the frames together or ranks, "
                                  "which no analysis carries"))
            continue
        key_rules(key, value, (key,), True)
        walk(value, (key,))
    return found


def _where(path: tuple) -> str:
    out = ""
    for part in path:
        out += f"[{part}]" if isinstance(part, int) else (f".{part}" if out else str(part))
    return out


def drop_departures(payload: dict, problems: list[tuple[tuple, str]], dropped: list) -> None:
    """Drop the unit that holds each departure, once, and record why."""
    units: dict[tuple, str] = {}
    for path, why in problems:
        top = payload.get(path[0])
        if len(path) > 1 and (isinstance(top, list) or (isinstance(top, dict)
                                                        and path[0] in BLOCKS)):
            unit = path[:2]
        else:
            unit = path[:1]
        units.setdefault(unit, why)
    removals: dict[str, list[int]] = {}
    for unit, why in units.items():
        key = unit[0]
        if len(unit) == 2 and isinstance(payload.get(key), list):
            removals.setdefault(key, []).append(unit[1])
            item = payload[key][unit[1]]
            dropped.append({"where": f"{key}[{unit[1]}]",
                            "id": item.get("id") if isinstance(item, dict) else None,
                            "reason": why})
            continue
        dropped.append({"where": _where(unit), "reason": why})
        if len(unit) == 2:
            block, name = payload[key], unit[1]
            if BLOCKS[key] == "remove" or SCORE_KEY.search(str(name).lower()):
                block.pop(name, None)
            elif BLOCKS[key] == "empty":
                block[name] = None
            else:
                block[name] = {"dropped": why}
        elif key in BLOCKS and isinstance(payload.get(key), dict):
            # the one departure that sits on a block object itself is a quote
            # written there, beside its entries: the quote goes, the entries stay
            payload[key].pop("quote", None)
            payload[key].pop("quote_from", None)
        elif key in SINGLE_ITEMS and not SCORE_KEY.search(key.lower()):
            payload[key] = {"dropped": why}
        else:
            payload.pop(key, None)
    for key, indices in removals.items():
        payload[key] = [item for index, item in enumerate(payload[key])
                        if index not in set(indices)]


def unanswered(payload: dict, kind: str, dropped: list) -> None:
    """An area, a section, the DuPont reading or the value range that carries no
    words of its own -- no non-empty `finding` or `reading` -- answers nothing,
    and the owner reads it as absent (`coverage.answered`). It keeps its key and
    says so. So does one whose whole block is missing or is not an object, since
    the owner reads every area of such a block as absent too."""
    def answered(entry) -> bool:
        if not isinstance(entry, dict):
            return False
        if isinstance(entry.get("dropped"), str) and entry["dropped"].strip():
            return True
        return any(isinstance(entry.get(key), str) and entry[key].strip()
                   for key in ("finding", "reading"))

    def hold(container: dict, name: str, where: str) -> None:
        if not answered(container.get(name)):
            why = ("the analyst wrote no finding or reading for it" if name in container
                   else "nothing stood for it")
            container[name] = {"dropped": why}
            dropped.append({"where": where, "reason": why})

    def block(key: str) -> dict:
        if not isinstance(payload.get(key), dict):
            payload[key] = {}
        return payload[key]

    if kind == "accounting":
        for name in ACCOUNTING_AREAS:
            hold(block("areas"), name, f"areas.{name}")
    elif kind == "financial":
        for name in FINANCIAL_SECTIONS:
            hold(block("sections"), name, f"sections.{name}")
        hold(payload, "dupont", "dupont")
    elif kind == "valuation":
        hold(payload, "value_range", "value_range")


def check(kind: str, payload: dict, *, fields: dict, sources: dict[str, str],
          excluded: set[str] | frozenset | Mapping[str, set[str]] = frozenset(),
          paragraph_ids: bool = False, filing: dict[str, str] | None = None) -> dict:
    """The analysis with every failing item dropped, and the list of drops.

    `excluded` is the ids the quote gate dropped from the reports: they may still
    be printed in the report files the analyst read, beside a kept item, and a
    citation of one is a citation of an item that did not stand. The gate keys
    its drops by report, and so does this: a mapping of report name to ids takes
    each id out of that report's items alone, which a reconciliation row, naming
    the report, is held to; a bare `evidence` citation names an id with no
    report, and an id dropped from either report is refused there, because the
    dropped item may still be printed beside a kept one and by id alone the
    citation would name both. A plain set takes its ids out of both reports.
    `filing` is the run's full MD&A and earnings release by
    name, for the valuation analyst, whose copies are trimmed: a quote is held
    to both (`quote_problem`).
    """
    if not isinstance(payload, dict):
        raise AnalysisInputError(f"the {kind} analysis is not a JSON object")
    payload = copy.deepcopy(payload)

    def left_out(report: str) -> set[str]:
        if isinstance(excluded, Mapping):
            return set(excluded.get(report) or ())
        return set(excluded)

    notes_ids = report_ids(sources.get("report_notes_text.md", "")) - left_out("report_notes_text.md")
    numbers_ids = report_ids(sources.get("report_numbers.md", "")) - left_out("report_numbers.md")
    # a bare citation is by id alone: an id dropped from either report is refused
    # whatever else carries it (`item_problem`); a reconciliation row names the
    # report and is held to that report's standing items alone
    fallen = frozenset(left_out("report_notes_text.md") | left_out("report_numbers.md"))
    if paragraph_ids:
        # The single-agent control has no upstream report: it cites the
        # paragraphs of its own input, and each is verified by its quote.
        notes_ids = numbers_ids = globals()["paragraph_ids"](sources)
    upstream = notes_ids | numbers_ids
    dropped: list[dict] = []
    forbidden = FORBIDDEN_EVERYWHERE + (FORBIDDEN_IN_VALUATION if kind == "valuation" else ())
    if kind == "accounting":
        _check_block(payload, "areas", ACCOUNTING_AREAS, fields, sources, upstream, dropped,
                     forbidden=forbidden, fallen=fallen, required=True, filing=filing)
        _check_list(payload, "reconciliation", fields, sources, upstream, dropped,
                    forbidden=forbidden, fallen=fallen, extra=reconciliation_problem(notes_ids, numbers_ids), filing=filing)
        _check_list(payload, "anomalies", fields, sources, upstream, dropped,
                    forbidden=forbidden, fallen=fallen, extra=anomaly_problem(ACCOUNTING_AREAS), filing=filing)
        _check_list(payload, "adjustments", fields, sources, upstream, dropped,
                    forbidden=forbidden, fallen=fallen, extra=adjustment_problem(fields), filing=filing)
    elif kind == "financial":
        _check_block(payload, "sections", FINANCIAL_SECTIONS, fields, sources, upstream,
                     dropped, forbidden=forbidden, fallen=fallen, required=True, filing=filing)
        for key in ("dupont", "path_to_distress"):
            entry = payload.get(key)
            problem = ("the analyst wrote nothing for it" if entry is None else
                       item_problem(entry, fields, sources, upstream, forbidden=forbidden, fallen=fallen,
                                    filing=filing))
            if problem:
                payload[key] = {"dropped": problem}
                dropped.append({"where": key, "reason": problem})
        _check_list(payload, "anomalies", fields, sources, upstream, dropped,
                    forbidden=forbidden, fallen=fallen, extra=anomaly_problem(FINANCIAL_AREAS), filing=filing)
    elif kind == "valuation":
        _check_block(payload, "readings", (), fields, sources, upstream, dropped,
                     forbidden=forbidden, fallen=fallen, required=False, filing=filing)
        payload.pop("readings", None)
        for key in VALUATION_KEYS:
            entry = payload.get(key)
            problem = ("the analyst wrote nothing for it" if entry is None else
                       item_problem(entry, fields, sources, upstream, forbidden=forbidden, fallen=fallen,
                                    filing=filing))
            if problem:
                payload[key] = {"dropped": problem}
                dropped.append({"where": key, "reason": problem})
        _check_list(payload, "most_sensitive", fields, sources, upstream, dropped,
                    forbidden=forbidden, fallen=fallen, filing=filing)
    else:
        raise AnalysisInputError(f"no analysis is called {kind!r}")
    _check_summary(payload, fields, dropped, forbidden=forbidden)
    # the owner's rules, over every key and string the checks above did not walk
    kept = kept_report_items(sources, left_out)
    citable = upstream if paragraph_ids else set().union(*kept.values())
    drop_departures(payload, owner_problems(
        payload, kind=kind, fields=fields, sources=sources, filing=filing,
        kept=kept, citable=citable), dropped)
    unanswered(payload, kind, dropped)
    _limits(payload, kind, dropped)
    payload["normalized_quotes"] = normalized_quotes(payload, sources)
    payload["dropped_items"] = dropped
    payload["dropped_count"] = len(dropped)
    return payload


# --- the valuation analyst's first pass --------------------------------------------------

def check_assumptions(payload: dict, *, fields: dict, sources: dict[str, str],
                      filing: dict[str, str] | None = None) -> dict:
    """Every driver a number, every driver with a reason and a quote or a field.

    A scenario whose drivers fail is dropped whole and counted: the DCF runs on
    the six drivers together or not at all, and Python never fills one in.
    `filing` is as in `check`: the run's full prose files, which a quote of the
    trimmed copy is held to as well.
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
                if isinstance(value, bool) or not isinstance(value, (int, float)) \
                        or not math.isfinite(value):
                    problem = f"{driver} is not a finite number"
                    break
                reason = reasons.get(driver)
                if not isinstance(reason, dict) or not reason.get("reason"):
                    problem = f"{driver} carries no reason"
                    break
                if not reason.get("quote") and not reason.get("fields"):
                    problem = f"{driver} carries neither a quote nor a calculator field"
                    break
                problem = item_problem(reason, fields, sources, set(),
                                       forbidden=FORBIDDEN_EVERYWHERE + FORBIDDEN_IN_VALUATION,
                                       filing=filing)
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
        elif not isinstance(chosen, dict) or isinstance(chosen.get("value"), bool) \
                or not isinstance(chosen.get("value"), (int, float)) \
                or not math.isfinite(chosen["value"]):
            problem = "no value, or one that is not a finite number"
        else:
            problem = quote_problem(chosen, sources, filing) or (None if chosen.get("quote")
                                                         else "no quote")
        if problem:
            dropped.append({"where": f"wacc_overrides.{name}", "reason": problem})
            overrides.pop(name)
    payload["wacc_overrides"] = overrides
    # a scenario the calculator does not run is checked by nobody here and read by
    # the owner's grader: it is removed, as a scenario that failed is
    for name in [name for name in scenarios if name not in calculator.SCENARIOS]:
        scenarios.pop(name)
        dropped.append({"where": f"scenarios.{name}",
                        "reason": f"not one of {', '.join(calculator.SCENARIOS)}"})
    drop_departures(payload, owner_problems(
        payload, kind="assumptions", fields=fields, sources=sources, filing=filing,
        kept=None, citable=None), dropped)
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
    parser.add_argument("--run", default=None,
                        help="the run directory: its manifest's drop rows, and for the "
                             "valuation kinds its full input_mdna.md and input_8k.md")
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    if args.kind in ("valuation", "assumptions") and not args.run:
        print(f"analysis_check: --kind {args.kind} needs --run <run directory>: the "
              "valuation analyst's input_mdna.md and input_8k.md are trimmed copies, and "
              "the trimmed copy alone cannot hold a quote across a seam between two kept "
              "paragraphs to what the filing printed; the run's full files are the other "
              "side", file=sys.stderr)
        return BAD_INPUT
    try:
        payload = json.loads(Path(args.written).read_text(encoding="utf-8"))
        fields = json.loads(Path(args.calculator).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"analysis_check: {exc}", file=sys.stderr)
        return BAD_INPUT
    sources = read_sources(Path(args.agent_dir), SOURCES[args.kind])
    filing: dict[str, str] | None = None
    excluded: dict[str, set[str]] = {}
    if args.run:
        from src import run_analysis          # lazy: that module imports this one
        run = Path(args.run)
        try:
            excluded = run_analysis.excluded_by_report(run)
        except (OSError, ValueError) as exc:
            print(f"analysis_check: {run}: the manifest's drop rows cannot be read: {exc}",
                  file=sys.stderr)
            return BAD_INPUT
        filing = {name: (run / name).read_text(encoding="utf-8")
                  for name in ("input_mdna.md", "input_8k.md") if (run / name).is_file()}
    else:
        print("analysis_check: no --run: the gate's drop rows were not read, so a citation "
              "of an id the quote gate dropped is not refused here", file=sys.stderr)
    try:
        out = (check_assumptions(payload, fields=fields, sources=sources, filing=filing)
               if args.kind == "assumptions" else
               check(args.kind, payload, fields=fields, sources=sources, excluded=excluded,
                     filing=filing))
    except AnalysisInputError as exc:
        print(f"analysis_check: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    print(f"analysis_check: {args.kind} -- {out['dropped_count']} dropped", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
