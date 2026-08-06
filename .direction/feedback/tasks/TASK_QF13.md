# TASK: QF13 — README figure probability-framing axis labels + figure-drift gate (owner-signed D-P83)

## Mode hint
mode: default

## PRE-FLIGHT
- Q-F13 (BN-12) signed via D-P83 blanket, default option.
- Scope: reader-facing accuracy only — NO published numbers change.

## Required changes
1. README first-screen figure: axis labels must state ordinal risk score
   (0-100), not probability framing; regenerate via its committed script.
2. Figure-drift gate: extend tools/verify_figures.py sidecar mechanism so
   the first-screen figure regenerates deterministically and drift fails
   the gate (same mechanism as existing figure sidecars).

## Check command
check: ./.venv/bin/python tools/verify_figures.py && ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. Axis label language matches RESULTS row 11 ("ordinal, not probabilities").
2. Drift gate demonstrably fails on a mutated figure (test or recorded run).
3. Zero cell-value changes in any published table.
