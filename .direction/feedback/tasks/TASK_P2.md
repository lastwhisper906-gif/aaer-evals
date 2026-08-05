# TASK: Phase 2 — schema v2 hard constraints + semantic validator (P0-3/P0-4)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration. D-P73 Phase 2 executes the ALREADY-SIGNED v2
  plan (D-P44a/D-P46) — do not redesign. v1 (schemas/llm_output.json)
  stays byte-frozen; wave-1/2 labels are Phase 6's concern, not yours.

## Objective

Upgrade schemas/llm_output_v2.json from rename-only (v2.0) to the
direction's hard-constraint contract (v2.1), with a semantic validator
for the rules JSON Schema can't express, and update the v2 lock test to
a v2.1 contract test.

## Design contract

1. schemas/llm_output_v2.json (v2.1):
   - checklist: minItems 8, maxItems 8; item_id enum CL1..CL8;
   - top_signals: items enum CL1..CL8;
   - fingerprint: REQUIRED (promote from optional);
   - pattern constraints: pipeline_version/commit fields ^[0-9a-f]{7,40}$;
     accession fields the 18-digit dashed pattern already used by
     cutoff_guard._normalize_accession (mirror it); case_id the repo's
     neutral-id pattern (inspect real ids);
   - description header bumps to v2.1 citing D-P73 Phase 2.
2. aaer_eval/output_contract_v2.py (semantic validator — rules the
   schema cannot express without contortion; direction explicitly says
   do not contort):
   - checklist item_ids exactly {CL1..CL8} each once (set equality —
     schema enums+minmax can't enforce uniqueness-of-each);
   - risk-tier/score consistency: misstatement_risk_score >= 70 →
     overall.risk_tier == "elevated"; score < 40 → risk_tier != 
     "elevated" (mirror the signed plan's thresholds — verify the tier
     vocabulary from the v1 schema enum before hardcoding);
   - top_signals ⊆ checklist item_ids that actually appear.
   API: validate_v2(record) -> list[str] violations; empty = pass.
3. tools/test_schema_v2.py: REPLACE the v2.0 structural-diff-lock
   contract with a v2.1 contract test (documented supersession comment
   citing this task): assert the hard constraints exist in the schema;
   assert v1 untouched (keep that half); semantic validator tests:
   valid record passes; each violation class fires (missing CL id, dup
   id, 7-item list, 9-item list, tier/score inconsistency both
   directions, top_signal not in checklist, fingerprint absent).
4. Metrics demotion: v2 concerns FUTURE runs — do NOT touch analysis/
   or published calibration rows (Phase 6 labels those). The schema
   description notes "primary metrics: AUC, permutation, rank
   correlation — ECE/Brier not computed for v2 outputs (D-P73)".

## Files in scope
- schemas/llm_output_v2.json, aaer_eval/output_contract_v2.py (new),
  tools/test_schema_v2.py. NOTHING else (v1 schema/runner untouched).

## Check command
check: ./.venv/bin/python -m pytest tools -q && ./.venv/bin/python tools/validate_schemas.py

## Acceptance criteria
1. v2.1 constraints all present and check_schema-clean; v1 byte-frozen.
2. Semantic validator covers the enumerated classes; every class has a
   firing test.
3. The superseded v2.0 diff-lock is replaced with documented rationale
   (not silently deleted).
4. Check passes; diff = the three files.
