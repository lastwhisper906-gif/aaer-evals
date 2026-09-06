# TASK: C1-01..05 — reserved-component correctness bundle (non-protected files)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Fix shapes with full evidence: .direction/feedback/rot2_C1A_2026-08-05.md
  — READ IT FIRST; implement those shapes. The 3 forward-tool findings
  (C1B-03/04/05) are NOT in this task (protected prefix — packeted).

## Files in scope (per the report's fix shapes)
- pipeline/probe_runner.py + its tests — C1-01: v2-dateshift outputs get
  a distinct filename/out-root (no silent adoption of v1 results);
  idempotent-skip keyed to the variant-distinct path; test proving a v1
  file does NOT satisfy a v2ds run.
- tools/sandbox_guard.py + tools/test_sandbox_guard.py — C1-02: grandchild
  propagation test (run_guarded spawning nested sys.executable);
  C1-03: block the DNS-escape family (gethostbyname/gethostbyname_ex/
  getaddrinfo per the report's shape) with a self-test; keep allowlist
  semantics unchanged otherwise.
- tools/lint_doc_counts.py + a test — C1-04: pytest collect-error output
  must fail the lint (parse the error marker, don't accept a shrunken
  count); test with a fixture collect-error transcript.
- tools/holdout_probe.py + a test — C1-05: idempotent skip on existing
  valid transcript + refuse silent overwrite (fail-closed message; force
  flag optional per report).

## Read-only / forbidden paths
- tools/forward_*.py (packeted separately), scoring/, analysis/, runs/,
  schemas/, docs/, Makefile, README*, harness/, CLAUDE.md, AGENTS.md,
  PROJECT_INVARIANTS.md.

## Check command
check: ./.venv/bin/python -m pytest pipeline tools -q

## Acceptance criteria
1. Each of the five findings closed per its report fix shape with a
   discriminating test (reviewer verifies against the report).
2. No behavior change beyond the five shapes; check passes; diff limited
   to the listed files + their tests.
