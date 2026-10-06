"""Mechanical regression checks on one run's outputs, and the hand-worked cases.

Each check reads files a run published and nothing about how they were made:
- `files_present`: the files every analysed run publishes.
- `agents_written`: every agent the manifest records wrote its file, and the run
  records no analysis failure.
- `quotes_resolve`: every quote a report or an analysis kept is in the run's
  committed inputs, character for character after the whitespace fold.
- `cited_numbers_exist`: every number an analysis cites names a field of the
  calculator file that analyst saw.
- `nothing_after_cutoff`: no input document, calculator fact or price is dated
  after the run's cutoff.
- `calculator_finite`: every numeric value in calculator.json is finite.
- `dcf_recomputes`: every scenario's enterprise value and value per share, and the
  simple free cash flow, recompute from the run's own drivers with this file's own
  arithmetic, which reproduces the two hand-worked cases below.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

from evals.common import (FAIL, NOT_APPLICABLE, PASS, PLACEHOLDER, Result, finite, fold, load,
                          number_at, resolve, run_name, walk_strings)

REQUIRED = ("input_manifest.json", "calculator.json", "calculator_filings_only.json",
            "analysis_accounting.json", "analysis_financial.json", "analysis_valuation.json",
            "report_numbers.md", "report_notes_text.md", "memo_ko.md")

# Which calculator file each analysis was handed (docs/HOW_WE_WORK.md §3): the
# accounting and financial analysts see no price; the valuation analyst's first pass
# sees the calculator before its drivers, its second pass the whole calculator.
SEEN = {"analysis_accounting.json": "calculator_filings_only.json",
        "analysis_financial.json": "calculator_filings_only.json",
        "assumptions.json": "calculator_before_drivers.json",
        "analysis_valuation.json": "calculator.json"}
ANALYSES = tuple(SEEN)
# The directory each analysis's agent was handed: its quotes are held to what it saw.
AGENT_DIR = {"analysis_accounting.json": "accounting-analyst",
             "analysis_financial.json": "financial-analyst",
             "assumptions.json": "valuation-analyst",
             "analysis_valuation.json": "valuation-analyst-second-pass"}

FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.S)
FOLLOWS_PATHS = ("fields",)          # list entries that are calculator paths


def report_items(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    items = []
    for block in FENCE.findall(path.read_text(encoding="utf-8")):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for item in data if isinstance(data, list) else [data]:
            if isinstance(item, dict):
                items.append(item)
    return items


def inputs_text(run: Path) -> dict[str, str]:
    return {p.name: fold(p.read_text(encoding="utf-8", errors="replace"))
            for p in sorted(run.glob("input_*")) if p.is_file()}


def agent_saw(run: Path, analysis: str) -> dict[str, str]:
    """The text files an analysis's agent was handed, folded; the run's own inputs
    where the run kept no agent directory."""
    directory = run / "agents" / AGENT_DIR[analysis]
    files = [p for p in sorted(directory.iterdir()) if p.is_file()] if directory.is_dir() else []
    if not files:
        return inputs_text(run)
    return {p.name: fold(p.read_text(encoding="utf-8", errors="replace")) for p in files
            if p.name != analysis}


def quoted(node, where=""):
    """Every dictionary in a tree that carries a `quote`, with where it sits."""
    if isinstance(node, dict):
        if isinstance(node.get("quote"), str) and node["quote"].strip():
            yield where, node
        for key, value in node.items():
            if key in ("dropped_items",):
                continue
            yield from quoted(value, f"{where}.{key}" if where else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from quoted(value, f"{where}[{index}]")


def check_files_present(run: Path) -> Result:
    missing = [name for name in REQUIRED if not (run / name).is_file()]
    return Result("mechanical.files_present", run_name(run), FAIL if missing else PASS,
                  f"missing {missing}" if missing else f"{len(REQUIRED)} files", missing)


def check_agents_written(run: Path) -> Result:
    manifest = load(run / "input_manifest.json") or {}
    agents = manifest.get("agents") or {}
    silent = [name for name, record in agents.items() if record.get("result") != "written"]
    problems = list(silent)
    if not agents:
        problems.append("the manifest records no agent")
    if manifest.get("analysis_failure"):
        problems.append(f"analysis_failure: {manifest['analysis_failure']}")
    return Result("mechanical.agents_written", run_name(run), FAIL if problems else PASS,
                  "; ".join(map(str, problems)) or f"{len(agents)} agents wrote", problems)


def check_quotes_resolve(run: Path) -> Result:
    sources = inputs_text(run)
    everything = "\n".join(sources.values())
    failures, count = [], 0
    for report in ("report_numbers.md", "report_notes_text.md"):
        for item in report_items(run / report):
            quote = item.get("quote")
            if not isinstance(quote, str) or not quote.strip():
                continue
            count += 1
            if fold(quote) not in everything:
                failures.append(f"{report}:{item.get('id')}")
    for name in ANALYSES:
        tree = load(run / name)
        if tree is None:
            continue
        seen = agent_saw(run, name)
        seen_everything = "\n".join(seen.values())
        for where, node in quoted(tree):
            count += 1
            source = node.get("quote_from")
            haystack = seen.get(source, seen_everything) if isinstance(source, str) \
                else seen_everything
            if fold(node["quote"]) not in haystack:
                failures.append(f"{name}:{where}")
    return Result("mechanical.quotes_resolve", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} quotes found in the run's inputs", failures)


def check_cited_numbers_exist(run: Path) -> Result:
    failures, count = [], 0
    for name, seen in SEEN.items():
        tree = load(run / name)
        if tree is None:
            continue
        calculator = load(run / seen)
        if calculator is None:
            failures.append(f"{name}: {seen} is missing")
            continue
        for where, text in walk_strings({k: v for k, v in tree.items() if k != "dropped_items"}):
            if where.endswith(".dropped") or where == "dropped":
                continue                     # the gate's own note on what it dropped
            paths = PLACEHOLDER.findall(text)
            if where.split("[")[0].endswith(FOLLOWS_PATHS) and not paths:
                paths = [(text, "")]
            for path, _ in paths:
                count += 1
                try:
                    resolve(calculator, path)
                except KeyError:
                    failures.append(f"{name}:{where}:{path}")
    return Result("mechanical.cited_numbers_exist", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} cited paths exist", failures)


def _dates_in(node, key: str):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key and isinstance(v, str):
                yield v
            else:
                yield from _dates_in(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from _dates_in(v, key)


def check_nothing_after_cutoff(run: Path) -> Result:
    manifest = load(run / "input_manifest.json") or {}
    try:
        cutoff = dt.date.fromisoformat(manifest["cutoff"])
    except (KeyError, TypeError, ValueError):
        return Result("mechanical.nothing_after_cutoff", run_name(run), FAIL,
                      "the manifest names no cutoff")
    late = []
    for document in manifest.get("documents") or []:
        filed = document.get("filing_date")
        if filed and dt.date.fromisoformat(filed) > cutoff:
            late.append(f"document {document.get('accession')} filed {filed}")
    calculator = load(run / "calculator.json") or {}
    for filed in _dates_in(calculator, "filed"):
        if dt.date.fromisoformat(filed[:10]) > cutoff:
            late.append(f"calculator fact filed {filed}")
    market = calculator.get("cost_of_capital") or {}
    for key in ("price_date", "date", "window_last"):
        for value in _dates_in(market, key):
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) and dt.date.fromisoformat(value) > cutoff:
                late.append(f"market {key} {value}")
    return Result("mechanical.nothing_after_cutoff", run_name(run), FAIL if late else PASS,
                  f"cutoff {cutoff}" + (f"; {len(late)} late" if late else ""), late)


def check_calculator_finite(run: Path) -> Result:
    bad = []

    def walk(node, where):
        if isinstance(node, dict):
            for key, value in node.items():
                here = f"{where}.{key}" if where else key
                if key == "value" and value is not None and not finite(value) \
                        and not isinstance(value, (str, list, dict)):
                    bad.append(here)
                walk(value, here)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{where}[{index}]")
        elif isinstance(node, float) and not finite(node):
            bad.append(where)

    walk(load(run / "calculator.json") or {}, "")
    return Result("mechanical.calculator_finite", run_name(run), FAIL if bad else PASS,
                  f"{len(bad)} non-finite values" if bad else "every value finite", bad)


# --- the discounted cash flow, worked independently ----------------------------------------

YEARS = 10


def forecast(base_revenue: float, drivers: dict, tax: float, wacc: float) -> dict:
    """Growth fades linearly from year one to the terminal rate at year ten; margin and
    reinvestment move linearly from year one to year ten; free cash flow is revenue x
    margin x (1 - tax) x (1 - reinvestment); end-of-year discounting; the terminal value
    is year ten's cash flow grown once, over WACC less terminal growth."""
    g1, gt = drivers["revenue_growth_year_one"], drivers["terminal_growth"]
    m1, m10 = drivers["operating_margin_year_one"], drivers["operating_margin_year_ten"]
    r1, r10 = drivers["reinvestment_rate_year_one"], drivers["reinvestment_rate_year_ten"]
    revenue, present, cash = base_revenue, 0.0, 0.0
    for year in range(1, YEARS + 1):
        step = (year - 1) / (YEARS - 1)
        growth = g1 + (gt - g1) * step
        margin = m1 + (m10 - m1) * step
        reinvest = r1 + (r10 - r1) * step
        revenue *= 1 + growth
        cash = revenue * margin * (1 - tax) * (1 - reinvest)
        present += cash / (1 + wacc) ** year
    terminal = cash * (1 + gt) / (wacc - gt)
    return {"explicit_present": present, "terminal_value": terminal,
            "enterprise_value": present + terminal / (1 + wacc) ** YEARS}


GORDON = {"revenue_growth_year_one": 0.03, "terminal_growth": 0.03,
          "operating_margin_year_one": 0.20, "operating_margin_year_ten": 0.20,
          "reinvestment_rate_year_one": 0.40, "reinvestment_rate_year_ten": 0.40}
FADE = dict(GORDON, revenue_growth_year_one=0.12)
# Worked by hand (tests/test_calculator.py carries the full table):
#   Gordon: 1,000 x 1.03 x 0.20 x 0.75 x 0.60 = 92.7; 92.7 / (0.09 - 0.03) = 1,545.
#   Fade 12% to 3%: enterprise value 2,240.8020; (2,240.8020 - 100 - 45) / 10 = 209.5802.
HAND_WORKED = (("gordon", GORDON, 1545.0, 140.0), ("fade", FADE, 2240.8020, 209.5802))


def check_hand_worked_cases() -> list[Result]:
    """This file's arithmetic and the calculator's both reproduce the hand-worked cases."""
    results = []
    try:
        from src import calculator
    except ImportError as exc:                       # pragma: no cover
        calculator, why = None, str(exc)
    for name, drivers, enterprise, per_share in HAND_WORKED:
        own = forecast(1000.0, drivers, 0.25, 0.09)["enterprise_value"]
        problems = []
        if abs(own - enterprise) > 1e-3:
            problems.append(f"the grader's own arithmetic gives {own}, the hand case {enterprise}")
        if calculator is None:
            problems.append(f"src.calculator does not import: {why}")
        else:
            run = calculator.forecast(1000.0, drivers, 0.25, 0.09)
            share = calculator.bridge(run["enterprise_value"], 100.0, 45.0, 10.0)["value_per_share"]
            if abs(run["enterprise_value"] - enterprise) > 1e-3:
                problems.append(f"src.calculator gives {run['enterprise_value']}, the hand case {enterprise}")
            if abs(share - per_share) > 1e-4:
                problems.append(f"src.calculator gives {share} a share, the hand case {per_share}")
        results.append(Result(f"mechanical.hand_worked_{name}", "code",
                              FAIL if problems else PASS, "; ".join(problems) or
                              f"enterprise value {enterprise}, {per_share} a share", problems))
    return results


def check_dcf_recomputes(run: Path) -> Result:
    calculator = load(run / "calculator.json") or {}
    valuation = calculator.get("valuation") or {}
    failures, count = [], 0
    for name, scenario in (valuation.get("scenarios") or {}).items():
        if "enterprise_value" not in scenario:
            continue
        count += 1
        own = forecast(valuation["base_revenue"], scenario["drivers"], valuation["tax_rate"],
                       valuation["wacc"])["enterprise_value"]
        if abs(own - scenario["enterprise_value"]) > 1e-6 * max(1.0, abs(own)):
            failures.append(f"{name}: enterprise value {scenario['enterprise_value']} against {own}")
        share = (own - scenario["net_debt"] - scenario["operating_lease_liability"]) \
            / scenario["diluted_shares"]
        if abs(share - scenario["value_per_share"]) > 1e-6 * max(1.0, abs(share)):
            failures.append(f"{name}: {scenario['value_per_share']} a share against {share}")
    simple = (calculator.get("free_cash_flow") or {}).get("free_cash_flow_simple") or {}
    ttm = ((calculator.get("terms") or {}).get("trailing_four_quarters") or {})
    if finite(simple.get("value")):
        count += 1
        try:
            expected = number_at(ttm, "operating_cash_flow") - number_at(ttm, "capital_expenditure")
            if abs(expected - simple["value"]) > 1e-6 * max(1.0, abs(expected)):
                failures.append(f"simple free cash flow {simple['value']} against {expected}")
        except (KeyError, TypeError):
            failures.append("simple free cash flow without its operating cash flow and capex")
    if not count:
        return Result("mechanical.dcf_recomputes", run_name(run), NOT_APPLICABLE,
                      "no scenario and no free cash flow to recompute")
    return Result("mechanical.dcf_recomputes", run_name(run), FAIL if failures else PASS,
                  f"{count - len(failures)} of {count} recompute", failures)


RUN_CHECKS = (check_files_present, check_agents_written, check_quotes_resolve,
              check_cited_numbers_exist, check_nothing_after_cutoff, check_calculator_finite,
              check_dcf_recomputes)


def grade(run: Path) -> list[Result]:
    return [check(run) for check in RUN_CHECKS]
