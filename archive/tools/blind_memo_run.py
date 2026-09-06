"""blind_memo_run.py — GIL blind-memo experiment: evaluatee calls (consumable output v1).

Two sequential evaluatee calls via the frozen call path (pipeline/cli_client.call_model,
subscription `claude -p`, isolated flags, schema-forced structured output,
model pin = runner.EVALUATEE_MODEL):

  call 1 (annual):    40-F body + EX-99.2 audited FS/notes + EX-99.1 MD&A
  call 2 (combined):  6-K body + EX-99.2 interim FS + EX-99.1 interim MD&A
                      + 40-F EX-99.3 AIF (did not fit in call 1)
                      + call 1's own flag output as incremental context

Blindness contract (task hard constraint 3/4): the evaluatee receives ONLY raw
filing text plus the generic forensic instruction below — no news, no selection
rationale, no framing. Call 2 additionally sees call 1's OWN output (sanctioned
as "quarterly as incremental context"). The AAER-experiment forbid_markers list
is NOT applied: filings legitimately contain words like "fraud" (auditor
reports), and this payload contains no ground-truth answer to leak.

Payload text is re-loaded through cutoff_guard.load_document() (registry
data/gil/registry.json) at call time — every send is logged and date-checked.

Usage: python tools/blind_memo_run.py [--stage annual|combined|all]
Output: runs/gil_memo_v1/ (flags JSON + call logs)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
from cli_client import call_model  # noqa: E402
from cutoff_guard import load_document  # noqa: E402
from runner import EVALUATEE_MODEL  # noqa: E402

REGISTRY = REPO / "data" / "gil" / "registry.json"
DATA = REPO / "data" / "gil"
OUT = REPO / "runs" / "gil_memo_v1"
CASE_ID = "OUT-GIL-V1"

# Verbatim from the task definition — do not edit without invalidating the experiment.
INSTRUCTION = (
    "You are a forensic accountant. Analyze the attached SEC filings of this company. "
    "Identify the 3-5 most significant accounting red flags or anomalies, prioritizing "
    "issues in revenue recognition, receivables, off-balance-sheet arrangements, cash "
    "flow vs earnings divergence, and footnote disclosures. For each flag: "
    "(1) describe the anomaly, (2) quote the exact supporting passage(s) verbatim "
    "with their location (item/note number), (3) explain the verification path — "
    "what a human analyst should check to confirm or dismiss this, (4) state your "
    "confidence (low/medium/high) and what additional data would change it. "
    "Base every claim strictly on the provided documents. If the documents do not "
    "support a claim, do not make it."
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["flags"],
    "properties": {
        "flags": {
            "type": "array", "minItems": 3, "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "description", "quotes",
                             "verification_path", "confidence",
                             "additional_data_that_would_change_confidence"],
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "quotes": {
                        "type": "array", "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["text", "location"],
                            "properties": {
                                "text": {"type": "string",
                                         "description": "verbatim passage from the documents"},
                                "location": {"type": "string",
                                             "description": "document + item/note number"},
                            },
                        },
                    },
                    "verification_path": {"type": "string"},
                    "confidence": {"enum": ["low", "medium", "high"]},
                    "additional_data_that_would_change_confidence": {"type": "string"},
                },
            },
        }
    },
}

ANNUAL_DOCS = [
    ("2026-02-26", "0001061894-26-000006", "40F_2026-02-26_body.txt",
     "Form 40-F (fiscal year ended 2025-12-28), filed 2026-02-26 — main form"),
    ("2026-02-26", "0001061894-26-000006", "40F_2026-02-26_ex99-2_financial_statements.txt",
     "Form 40-F Exhibit 99.2 — Audited Consolidated Financial Statements and Notes"),
    ("2026-02-26", "0001061894-26-000006", "40F_2026-02-26_ex99-1_mda.txt",
     "Form 40-F Exhibit 99.1 — Management's Discussion and Analysis (fiscal 2025)"),
]

COMBINED_DOCS = [
    ("2026-04-30", "0001061894-26-000013", "6K_2026-04-30_body.txt",
     "Form 6-K (first quarter 2026 interim filing), filed 2026-04-30 — main form"),
    ("2026-04-30", "0001061894-26-000013",
     "6K_2026-04-30_ex99-2_interim_financial_statements.txt",
     "Form 6-K Exhibit 99.2 — Condensed Interim Consolidated Financial Statements (Q1 2026)"),
    ("2026-04-30", "0001061894-26-000013", "6K_2026-04-30_ex99-1_interim_mda.txt",
     "Form 6-K Exhibit 99.1 — Interim Management's Discussion and Analysis (Q1 2026)"),
    ("2026-02-26", "0001061894-26-000006", "40F_2026-02-26_ex99-3_aif.txt",
     "Form 40-F Exhibit 99.3 — Annual Information Form (fiscal 2025)"),
]


def build_payload(docs, prior_flags: dict | None = None) -> str:
    parts = []
    if prior_flags is not None:
        parts.append(
            "Your prior analysis of this company's annual filing produced the flags "
            "below. The additional filing documents follow; update, confirm, replace "
            "or re-rank your flags into a final set of 3-5 based on all documents "
            "you have now seen.\n\nPRIOR FLAGS (your own earlier output):\n"
            + json.dumps(prior_flags, indent=2))
    for filing_date, accession, fname, label in docs:
        text = load_document(CASE_ID, str(DATA / fname), filing_date,
                             accession_no=accession, registry_path=REGISTRY)
        parts.append(f"=== BEGIN DOCUMENT: {label} ===\n{text}\n=== END DOCUMENT ===")
    return "\n\n".join(parts)


def run_stage(stage: str) -> bool:
    OUT.mkdir(parents=True, exist_ok=True)
    if stage == "annual":
        payload = build_payload(ANNUAL_DOCS)
    else:
        prior = json.loads((OUT / "flags_annual.json").read_text(encoding="utf-8"))
        payload = build_payload(COMBINED_DOCS, prior_flags=prior)
    print(f"[{stage}] payload: {len(payload):,} chars", flush=True)
    r = call_model(EVALUATEE_MODEL, INSTRUCTION, payload, SCHEMA,
                   log_dir=OUT, log_name=f"call_{stage}",
                   timeout_seconds=3600)
    print(f"[{stage}] ok={r.ok} fail={r.fail_reason} served={r.served_models} "
          f"usage={r.usage} wall={r.wall_seconds}s", flush=True)
    if not r.ok:
        return False
    (OUT / f"flags_{stage}.json").write_text(
        json.dumps(r.structured, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["annual", "combined", "all"], default="all")
    args = ap.parse_args()
    stages = ["annual", "combined"] if args.stage == "all" else [args.stage]
    for s in stages:
        if not run_stage(s):
            print(f"[{s}] FAILED — stopping", flush=True)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
