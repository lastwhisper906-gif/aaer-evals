# TASK: R4-01/02/03(ii)/04 — test-quality bundle (test-only additions)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Fix shapes are SPECIFIED with evidence in
  .direction/feedback/replenish_R4_2026-08-05.md — read it first and
  implement those shapes; this task file only lists scope. Test-only:
  NO production-code changes anywhere.

## Files in scope (tests only)
- pipeline/test_payload_blindness.py — R4-01: capture-based send-site
  test per the report (run_case with mocked call_model + adversarial
  non-underscore marker key fixture; assert captured user_payload keys ==
  allowlist and no forbidden substring, both arms; plus the probe_runner
  capture variant per test_probe_runner_v2ds precedent).
- tools/test_verify_blindness.py — R4-02: check_history unit tests per
  the report's shape (vacuous-pass regressions must fail: at minimum a
  fixture where criteria commit does NOT precede, and the
  ancestor-check-skipped path).
- pipeline/test_crossmodel_gpt.py — R4-03 option (ii): pin current
  resume behavior with a test + make fingerprint-less existing output a
  FAIL (assert the runner records FAIL rather than silently accepting) —
  if that requires a production change it is OUT of scope; then ONLY pin
  current behavior and mark the acceptance-gap in the test docstring.
- pipeline/test_no_guard_bypass.py — R4-04: positive control — a fixture
  source string containing a known-forbidden raw-read pattern must be
  flagged by the scan; if the scan regex breaks, this test goes red.

## Read-only / forbidden paths
- ALL production code (pipeline/*.py non-test, tools/*.py non-test,
  scoring/, analysis/); harness/, CLAUDE.md, AGENTS.md,
  PROJECT_INVARIANTS.md, Makefile, docs/, README*.

## Check command
check: ./.venv/bin/python -m pytest pipeline tools -q

## Acceptance criteria
1. R4-01: the new test FAILS if runner.py's send site is reverted to the
   exclusion-based pre-FB-01 shape (verify by reasoning through the
   assertion — it must key off captured runner output, not _render).
2. R4-02: check_history's vacuous-pass classes covered; tests use tmp
   git fixtures per the file's existing conventions.
3. R4-03: behavior pinned; fingerprint-less handling asserted per option
   (ii) without production edits (docstring gap-note if needed).
4. R4-04: positive control present and discriminating.
5. Check passes; diff touches ONLY the four test files.
