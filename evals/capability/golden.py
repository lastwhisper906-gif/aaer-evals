"""Approved golden cases against their runs: found, missed and extra, with partial credit.

A case (`evals/golden/cases/*.yaml`, approved by the owner) names a filing, a frame
and what a careful analyst must find there. For every run of that filing:

- a `must_find` item is **found** when an anomaly in the case's frame matches it: its
  area matches the item's `area` when the item names one, and either its evidence
  reaches one of the item's `paragraph_ids` (an anomaly cites reader items; each
  reader item carries the filing paragraph id it quotes, which stays the same from
  run to run), or its name and text contain every word of one of the item's
  `keywords` entries (case is ignored);
- a `must_not_claim` item is **extra** when an anomaly in the frame matches its
  keywords the same way.

Score for one run of one case = (found - extra) / number of must_find items, floored
at zero. The frame decides which analyses are read: accounting reads
analysis_accounting.json; finance reads analysis_financial.json and
analysis_valuation.json. Drafts are never counted.
"""

from __future__ import annotations

from pathlib import Path

from evals.common import REPO, find_runs, load, run_name
from evals.regression.mechanical import report_items
from evals.golden_format import GoldenFormatError, load_case

CASES = REPO / "evals" / "golden" / "cases"
FRAME_FILES = {"accounting": ("analysis_accounting.json",),
               "finance": ("analysis_financial.json", "analysis_valuation.json")}


def approved_cases() -> list[tuple[Path, dict]]:
    out = []
    for path in sorted(CASES.glob("*.yaml")):
        case = load_case(path)
        if case.get("approved_by_owner") is True:
            out.append((path, case))
    return out


def runs_of(accession: str, runs: list[Path] | None = None) -> list[Path]:
    return [run for run in (runs if runs is not None else find_runs())
            if (load(run / "input_manifest.json") or {}).get("accession") == accession]


def anomalies(run: Path, frame: str) -> list[dict]:
    """The frame's anomalies, each with `paragraphs`: the filing paragraph ids its
    evidence reaches through the run's reader reports."""
    paragraph_of = {}
    for report in ("report_numbers.md", "report_notes_text.md"):
        for item in report_items(run / report):
            if item.get("id") and item.get("paragraph_id"):
                paragraph_of[item["id"]] = item["paragraph_id"]
    out = []
    for name in FRAME_FILES[frame]:
        analysis = load(run / name) or {}
        for a in analysis.get("anomalies") or []:
            if isinstance(a, dict):
                cited = set(a.get("evidence") or [])
                out.append(dict(a, paragraphs=cited | {paragraph_of[c] for c in cited
                                                       if c in paragraph_of}))
    return out


def _text(anomaly: dict) -> str:
    return " ".join(str(anomaly.get(k) or "") for k in ("id", "name", "what")).lower()


def matches(anomaly: dict, rule: dict) -> bool:
    if rule.get("area") and anomaly.get("area") != rule["area"]:
        return False
    if set(anomaly.get("paragraphs") or anomaly.get("evidence") or []) \
            & set(rule.get("paragraph_ids") or []):
        return True
    text = _text(anomaly)
    for entry in rule.get("keywords") or []:
        words = [w for w in str(entry).lower().split() if w]
        if words and all(w in text for w in words):
            return True
    return False


def score_run(case: dict, run: Path) -> dict:
    found, missed, extra = [], [], []
    candidates = anomalies(run, case["frame"])
    for item in case.get("must_find") or []:
        (found if any(matches(a, item) for a in candidates) else missed).append(item.get("what"))
    for item in case.get("must_not_claim") or []:
        if any(matches(a, item) for a in candidates):
            extra.append(item.get("what"))
    total = max(1, len(case.get("must_find") or []))
    return {"run": run_name(run), "found": found, "missed": missed, "extra": extra,
            "score": max(0.0, (len(found) - len(extra)) / total)}


def grade(runs: list[Path] | None = None) -> dict:
    try:
        cases = approved_cases()
    except GoldenFormatError as exc:
        return {"status": "error", "detail": str(exc), "score": None, "cases": []}
    if not cases:
        return {"status": "no approved cases", "score": None, "cases": [],
                "detail": "evals/golden/cases/ holds no case with approved_by_owner: true"}
    rows, scores = [], []
    for path, case in cases:
        for run in runs_of(case["filing"]["accession"], runs):
            row = dict(score_run(case, run), case=path.name)
            rows.append(row)
            scores.append(row["score"])
    return {"status": "scored" if scores else "no run of an approved case",
            "score": sum(scores) / len(scores) if scores else None, "cases": rows}
