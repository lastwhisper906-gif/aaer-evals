# TASK: Q1 — schemas/llm_output_v2.json rename execution (PKT-Q1, signed D-P44a; queued D-P83)

## Mode hint
mode: default

## PRE-FLIGHT
- Owner decision SIGNED (D-P44a 2026-08-05); execution queued by D-P83.
- Execute exactly .direction/feedback/packets/PKT-Q1_schema_v2_risk_score.md
  "What changes (and what must not)".
- MUST NOT: edit schemas/llm_output.json (v1.2 frozen), re-run waves 1-2,
  alter published calibration rows.

## Check command
check: ./.venv/bin/python -m pytest tools/test_schema_v2.py -q && ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. misstatement_probability -> misstatement_risk_score (0-100 int, ordinal
   language, trigger >= 40) in llm_output_v2.json only; $comment header per packet.
2. Scoring-side future-output accessors version-dispatched; frozen paths untouched.
3. FREEZE_REV-style note records the prompt-hash change before any run.
