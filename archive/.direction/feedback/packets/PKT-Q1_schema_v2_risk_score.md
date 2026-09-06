# PKT-Q1 — v2 evaluatee contract: misstatement_probability → misstatement_risk_score
**Owner decision: SIGNED (D-P44a, 2026-08-05) — rename; ECE/Brier demoted.**
**Execution queued as TASK_Q1 for the next loop sprint (D-P83).**
Status: ready-to-execute packet. Execution = one build cycle, future waves only.

## What changes (and what must not)
- NEW file `schemas/llm_output_v2.json`: copy of v1.2 with
  `misstatement_probability` → `misstatement_risk_score` (0-100 integer,
  description rewritten to ordinal-rank language, no 확률/probability
  wording), `mechanism_hypotheses` trigger condition updated to
  `misstatement_risk_score >= 40`, `$comment` header: "v2 (D-P44a):
  ordinal rename — v1.2 frozen for waves 1-2 comparability; adopt for
  wave-3+/forward only."
- Evaluatee prompt template (runner TASK string): same rename; a v2
  FREEZE_REV-style note records prompt-hash change before any run.
- Scoring-side consumers: grep `misstatement_probability` in scoring/
  and analysis/ — read paths for FUTURE outputs gain a
  version-dispatched field accessor; frozen recompute paths untouched.
- ECE/Brier: no primary-metric computation for v2 outputs; rank metrics
  (AUC/permutation) remain primary. RESULTS row-11 wording already
  matches ("ordinal, not probabilities").
- MUST NOT: edit schemas/llm_output.json (v1.2 frozen), re-run waves 1-2,
  or alter published calibration rows.

## Exact commands (after packet-to-task conversion)
  # build cycle (harness, default mode):
  ~/tools/harness/run_task.sh --task .direction/feedback/tasks/TASK_Q1.md \
    --workdir ~/repos/aaer-evals-work
  # gates: make verify-public && make docs-refresh

## Invariant check
INV-02 (schema enforcement — v2 file becomes the enforced contract for v2
runs), INV-03 (no retro change — v1 frozen), INV-06 (parallel new path,
not replacement). No INV-12 impact.
