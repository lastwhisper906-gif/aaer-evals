"""Every published run's accounting and financial analysis, on one page.

The owner's request of 2026-10-28: the two analyses, for every company, on one
screen a reader can take in. This reads each run under `runs/` that has both
analyses and writes one self-contained HTML page: a company list down the side,
and for the company chosen, the accounting analysis and the financial analysis
side by side, each with its key figures, its areas or sections in Korean, and
every anomaly it listed.

Nothing on the page is written here. The Korean sentences are the analysts'
`summary_ko`, each `{path}` filled with the number the calculator holds there by
`src/memo.py`'s `fill`, from the file that analyst was handed, exactly as the
run's own `memo_ko.md` prints them; the area and section names are the memo's.
The key figures are calculator cells, printed by the same `fill`. A sentence the
gate dropped is shown as dropped, never quoted. There is no composite score and
no rank across companies (CLAUDE.md): the companies are listed by ticker.

    python -m src.analysis_page --runs runs --out analysis.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from src import interpreter_pin, memo
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, memo

BAD_INPUT = 2

# The figures shown above each analysis, each a calculator path with its Korean
# name, printed as the memo prints a `{path}` (`|pct` as a percentage).
ACCOUNTING_FIGURES = (
    ("영업현금흐름 ÷ 순이익 (최근 4분기)", "earnings_versus_cash.operating_cash_flow_over_net_income"),
    ("발생액 ÷ 평균자산", "earnings_versus_cash.accruals_over_average_assets|pct"),
    ("매출채권회수일수", "ratios.efficiency.days_sales_outstanding"),
    ("재고일수", "ratios.efficiency.days_sales_of_inventory"),
)
FINANCIAL_FIGURES = (
    ("매출총이익률", "ratios.profitability.gross_margin|pct"),
    ("영업이익률", "ratios.profitability.operating_margin|pct"),
    ("투하자본이익률", "ratios.profitability.return_on_invested_capital|pct"),
    ("매출 성장 (전년 동기)", "ratios.growth.revenue.year_over_year|pct"),
    ("유동비율", "ratios.liquidity.current_ratio"),
    ("부채 ÷ EBITDA", "ratios.solvency.debt_over_ebitda"),
    ("이자보상배율", "ratios.solvency.interest_coverage"),
    ("잉여현금흐름 (회계 조정 반영)", "free_cash_flow.free_cash_flow_quality_adjusted"),
)
# The one figure read from the final calculator, not the analysts' view: the
# free cash flow Python adjusted with the accounting analyst's adjustments,
# which the view handed to the analysts holds before any adjustment.
FROM_THE_FINAL_CALCULATOR = ("free_cash_flow.free_cash_flow_quality_adjusted",)
OUTCOMES = ("contradicts", "unresolved", "confirms")


def _load(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def figure(fields: dict, path: str) -> str | None:
    """A calculator cell as the memo prints it, or None where it holds no number."""
    bare = path.split("|", 1)[0]
    value = memo.analysis_check.placeholder_value(fields, bare)
    if value is None:
        return None
    return memo.fill("{" + path + "}", fields)


def figures(seen: dict, wanted, final: dict | None = None) -> list[dict]:
    out = []
    for label, path in wanted:
        bare = path.split("|", 1)[0]
        source = final if final is not None and bare in FROM_THE_FINAL_CALCULATOR else seen
        text = figure(source, path)
        out.append({"label": label, "text": text or "계산되지 않음", "path": bare,
                    "missing": text is None})
    return out


def original(source, field: str, seen: dict, text: str) -> dict:
    """The analyst's English reading an entry's Korean sentence summarizes, filled
    as the sentence is, with the area's verdict where it has one; nothing for an
    entry the gate dropped, nor for one whose Korean sentence it dropped: the
    memo prints the dropped notice alone there, and so does the page."""
    if text == memo.DROPPED_KO or not isinstance(source, dict) or "dropped" in source \
            or not source.get(field):
        return {}
    out = {"original": memo.fill(source[field], seen)}
    if source.get("verdict"):
        out["verdict"] = memo.fill(source["verdict"], seen)
    return out


def anomalies(analysis: dict, fields: dict, names: dict) -> list[dict]:
    out = []
    for item in analysis.get("anomalies") or []:
        outcome = item.get("numbers_vs_prose")
        out.append({"id": item.get("id"),
                    "name": item.get("name_ko") or item.get("name") or item.get("id"),
                    "area": names.get(item.get("area"), item.get("area")),
                    "outcome": outcome if outcome in OUTCOMES else None,
                    "outcome_ko": memo.OUTCOME_KO.get(outcome),
                    "detail": memo.fill(item.get("what"), fields)})
    return out


def accounting(analysis: dict | None, seen: dict, fields: dict) -> dict | None:
    if analysis is None:
        return None
    summary = analysis.get("summary_ko") or {}
    areas = []
    for key, name in memo.ACCOUNTING_KO.items():
        text = memo._entry(summary, key, analysis, "areas", seen)
        areas.append({"key": key, "name": name, "text": text,
                      **original((analysis.get("areas") or {}).get(key), "finding", seen, text)})
    quality = (fields.get("free_cash_flow") or {}).get("free_cash_flow_quality_adjusted") or {}
    adjustments = [{"name": item.get("name"),
                    "text": (f"{memo.korean_number(item['amount'], 'USD')} "
                             f"{'차감' if item['direction'] == 'reduce' else '가산'}"),
                    "path": item.get("calculator_field")}
                   for item in quality.get("adjustments_applied") or []]
    return {"areas": areas, "anomalies": anomalies(analysis, seen, memo.ACCOUNTING_KO),
            "adjustments": adjustments, "dropped": analysis.get("dropped_count") or 0,
            "figures": figures(seen, ACCOUNTING_FIGURES), "limits": memo.LIMITS_KO["accounting"]}


def financial(analysis: dict | None, seen: dict, fields: dict | None = None) -> dict | None:
    if analysis is None:
        return None
    summary = analysis.get("summary_ko") or {}
    sections = []
    for key, name in memo.FINANCIAL_KO.items():
        block = "sections" if key in memo.analysis_check.FINANCIAL_SECTIONS else None
        source = (analysis.get(block) or {}).get(key) if block else analysis.get(key)
        text = memo._entry(summary, key, analysis, block, seen)
        sections.append({"key": key, "name": name, "text": text,
                         **original(source, "reading", seen, text)})
    return {"sections": sections, "anomalies": anomalies(analysis, seen, memo.FINANCIAL_KO),
            "dropped": analysis.get("dropped_count") or 0,
            "figures": figures(seen, FINANCIAL_FIGURES, fields),
            "limits": memo.LIMITS_KO["financial"]}


def run_entry(run: Path) -> dict | None:
    """One run as the page shows it, or None for a run without a calculator."""
    fields = _load(run / "calculator.json")
    if fields is None:
        return None
    seen = _load(run / "calculator_filings_only.json") or fields
    manifest = _load(run / "input_manifest.json") or {}
    grade = _load(run / "grade.json")
    models = sorted({row.get("model_served") for row in (manifest.get("agents") or {}).values()
                     if isinstance(row, dict) and row.get("model_served")})
    return {
        "ticker": run.parent.name, "run": f"{run.parent.name}/{run.name}",
        "accession": fields.get("accession"), "form": fields.get("form"),
        "period_end": fields.get("period_end"), "filing_date": fields.get("cutoff"),
        "rerun": "-rerun-" in run.name, "models": models,
        "grade": ({"score": grade.get("score"), "dealbreakers": len(grade.get("dealbreakers") or [])}
                  if grade else None),
        "accounting": accounting(_load(run / "analysis_accounting.json"), seen, fields),
        "financial": financial(_load(run / "analysis_financial.json"), seen, fields),
    }


def collect(root: Path) -> list[dict]:
    """Every run with both analyses, newest filing first within a company, a
    rerun before the run it repeats; the companies by ticker."""
    entries = []
    for run in sorted(root.glob("*/*/")):
        if not (run / "analysis_accounting.json").is_file() \
                or not (run / "analysis_financial.json").is_file():
            continue
        entry = run_entry(run)
        if entry is not None:
            entries.append(entry)
    entries.sort(key=lambda e: (e["ticker"], [-ord(c) for c in (e["filing_date"] or "")],
                                not e["rerun"], e["run"]))
    return entries


TEMPLATE = Path(__file__).with_name("analysis_page.html")


def page(entries: list[dict]) -> str:
    # every "<" written as its escape, so no text in the data -- a "</script>",
    # a "<!--<script>" -- can end or swallow the element that holds it
    data = json.dumps(entries, ensure_ascii=False).replace("<", "\\u003c")
    return TEMPLATE.read_text(encoding="utf-8").replace("__RUNS_JSON__", data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", default="runs")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    entries = collect(Path(args.runs))
    if not entries:
        print(f"analysis_page: no run under {args.runs} holds both analyses", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(page(entries), encoding="utf-8")
    print(f"analysis_page: {len(entries)} runs of "
          f"{len({e['ticker'] for e in entries})} companies → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
