"""Coverage regression checks: did each analysis answer what it is for?

An area the gate dropped is still accounted for: the record says what was dropped
and why. A regression failure is an area, section or answer that is simply absent.
How many areas were answered rather than dropped is a capability score
(`rates`), tracked and not gated.

- `accounting_areas`: the seven areas and the industry lens each carry a finding
  ("nothing found, because" is a finding) or the gate's note on why it was dropped.
- `financial_sections`: profitability, efficiency, liquidity, solvency, growth and
  the DuPont reading, the same way.
- `valuation_answer`: a value range, or the calculator's stated reason there is
  none; the market-implied growth, or its stated reason; and the revenue history it
  is read beside.
- `memo_frames`: the memo has an accounting (회계) section and a finance (재무) section.
- `forbidden_words`: no accusation word (fraud, manipulation) anywhere, and no
  recommendation word (buy, sell, alpha) where a recommendation would sit, in English
  or Korean.
- `no_combined_score`: no field that adds the frames together or ranks companies.
"""

from __future__ import annotations

import re
from pathlib import Path

from evals.common import FAIL, PASS, Result, load, run_name, walk_strings

ACCOUNTING_AREAS = ("earnings_versus_cash", "revenue_recognition", "estimates_and_reserves",
                    "cost_deferral", "cash_flow_engineering_and_off_balance_sheet",
                    "controls_audit_and_filing_signals", "cross_document_reconciliation",
                    "industry_lens")
FINANCIAL_SECTIONS = ("profitability", "efficiency", "liquidity", "solvency", "growth")

# Accusation words are banned in every analysis and the memo. Recommendation words --
# buy, sell, alpha -- are banned where a recommendation would sit: the valuation
# analysis, its assumptions and the memo. In the accounting and financial analyses
# "buy" and "sell" are what companies do ("an agreement to buy", "credit extended to
# sell product", "a plan to sell shares"), which is the line the analysis gate has
# drawn since #101. A hyphen after the word ("sell-in", "sell-through", "sell-side")
# makes a channel or market term, not a recommendation.
ACCUSATION = re.compile(r"fraud\w*|manipulat\w*|분식|회계\s*부정|사기\s*행위|사기적|사기죄|조작",
                        re.IGNORECASE)
RECOMMENDATION = re.compile(r"\balpha\b|\bbuy\b(?!-)|\bsell\b(?!-)"
                            r"|매수\s*(추천|의견|권)|매도\s*(추천|의견|권)", re.IGNORECASE)
RECOMMENDATION_FILES = ("analysis_valuation.json", "assumptions.json")
SCORE_KEY = re.compile(r"(^|_)(score|composite|rank|ranking|overall)($|_)")
PROSE_FILES = ("analysis_accounting.json", "analysis_financial.json",
               "analysis_valuation.json", "assumptions.json")


def answered(entry) -> str:
    """'answered', 'dropped' (the gate's note says why) or 'absent'."""
    if isinstance(entry, dict):
        if isinstance(entry.get("dropped"), str) and entry["dropped"].strip():
            return "dropped"
        for key in ("finding", "reading"):
            if isinstance(entry.get(key), str) and entry[key].strip():
                return "answered"
    return "absent"


def check_accounting_areas(run: Path) -> Result:
    areas = (load(run / "analysis_accounting.json") or {}).get("areas") or {}
    absent = [a for a in ACCOUNTING_AREAS if answered(areas.get(a)) == "absent"]
    return Result("coverage.accounting_areas", run_name(run), FAIL if absent else PASS,
                  f"absent: {absent}" if absent else "every area answered or its drop recorded",
                  absent)


def check_financial_sections(run: Path) -> Result:
    analysis = load(run / "analysis_financial.json") or {}
    sections = analysis.get("sections") or {}
    absent = [s for s in FINANCIAL_SECTIONS if answered(sections.get(s)) == "absent"]
    if answered(analysis.get("dupont")) == "absent":
        absent.append("dupont")
    return Result("coverage.financial_sections", run_name(run), FAIL if absent else PASS,
                  f"absent: {absent}" if absent else "every section answered or its drop recorded",
                  absent)


def check_valuation_answer(run: Path) -> Result:
    calculator = load(run / "calculator.json") or {}
    valuation = calculator.get("valuation") or {}
    problems = []
    has_range = isinstance(valuation.get("value_range_per_share"), dict)
    if not has_range and not (isinstance(valuation.get("missing"), str)
                              or all(isinstance(s, dict) and s.get("missing")
                                     for s in (valuation.get("scenarios") or {}).values())
                              and valuation.get("scenarios")):
        problems.append("no value range and no stated reason")
    reverse = valuation.get("reverse_dcf")
    if has_range and not (isinstance(reverse, dict)
                          and ("value" in reverse or isinstance(reverse.get("missing"), str))):
        problems.append("a value range with no market-implied growth and no reason")
    history = (calculator.get("earnings_versus_cash") or {}).get("history") or {}
    if not history.get("years"):
        problems.append("no revenue history to read the implied growth beside")
    reading = load(run / "analysis_valuation.json") or {}
    if answered(reading.get("value_range")) == "absent":
        problems.append("the valuation analysis does not read the range")
    return Result("coverage.valuation_answer", run_name(run), FAIL if problems else PASS,
                  "; ".join(problems) or ("range, implied growth and history" if has_range
                                          else "no range, and the reason is stated"), problems)


def check_memo_frames(run: Path) -> Result:
    memo = run / "memo_ko.md"
    text = memo.read_text(encoding="utf-8") if memo.is_file() else ""
    headings = [line for line in text.splitlines() if line.startswith("#")]
    missing = [frame for frame in ("회계", "재무") if not any(frame in h for h in headings)]
    return Result("coverage.memo_frames", run_name(run), FAIL if missing else PASS,
                  f"no heading for {missing}" if missing else "회계 and 재무 sections", missing)


def check_forbidden_words(run: Path) -> Result:
    hits = []
    for name in PROSE_FILES:
        tree = load(run / name) or {}
        for where, text in walk_strings({k: v for k, v in tree.items()
                                         if k not in ("dropped_items",)}):
            if where.endswith(".dropped") or where.endswith("quote"):
                continue        # a verbatim quote is the filer's words, not the analyst's
            patterns = (ACCUSATION, RECOMMENDATION) if name in RECOMMENDATION_FILES \
                else (ACCUSATION,)
            for pattern in patterns:
                for match in pattern.finditer(text):
                    hits.append(f"{name}:{where}: {match.group()}")
    memo = run / "memo_ko.md"
    if memo.is_file():
        for number, line in enumerate(memo.read_text(encoding="utf-8").splitlines(), 1):
            for pattern in (ACCUSATION, RECOMMENDATION):
                for match in pattern.finditer(line):
                    hits.append(f"memo_ko.md:{number}: {match.group()}")
    return Result("coverage.forbidden_words", run_name(run), FAIL if hits else PASS,
                  f"{len(hits)} found" if hits else "none", hits)


def check_no_combined_score(run: Path) -> Result:
    found = []

    def keys(node, where):
        if isinstance(node, dict):
            for key, value in node.items():
                if SCORE_KEY.search(key.lower()):
                    found.append(f"{where}.{key}" if where else key)
                keys(value, f"{where}.{key}" if where else key)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                keys(value, f"{where}[{index}]")

    for name in PROSE_FILES:
        keys(load(run / name) or {}, name)
    return Result("coverage.no_combined_score", run_name(run), FAIL if found else PASS,
                  f"score fields: {found}" if found else "none", found)


RUN_CHECKS = (check_accounting_areas, check_financial_sections, check_valuation_answer,
              check_memo_frames, check_forbidden_words, check_no_combined_score)


def grade(run: Path) -> list[Result]:
    return [check(run) for check in RUN_CHECKS]


def rates(run: Path) -> dict:
    """Capability, not regression: how much was answered rather than dropped."""
    accounting = load(run / "analysis_accounting.json") or {}
    financial = load(run / "analysis_financial.json") or {}
    areas = accounting.get("areas") or {}
    sections = dict(financial.get("sections") or {}, dupont=financial.get("dupont"))
    calculator = load(run / "calculator.json") or {}
    valuation = calculator.get("valuation") or {}
    history = (calculator.get("earnings_versus_cash") or {}).get("history") or {}
    return {
        "accounting_areas_answered": sum(answered(areas.get(a)) == "answered"
                                         for a in ACCOUNTING_AREAS) / len(ACCOUNTING_AREAS),
        "financial_sections_answered": sum(answered(sections.get(s)) == "answered"
                                           for s in FINANCIAL_SECTIONS + ("dupont",))
        / (len(FINANCIAL_SECTIONS) + 1),
        "value_range_computed": 1.0 if isinstance(valuation.get("value_range_per_share"), dict)
        else 0.0,
        "implied_growth_beside_three_and_five_year_history": 1.0 if (
            "value" in (valuation.get("reverse_dcf") or {})
            and "revenue_growth_three_year_compound" in history
            and "revenue_growth_five_year_compound" in history) else 0.0,
    }
