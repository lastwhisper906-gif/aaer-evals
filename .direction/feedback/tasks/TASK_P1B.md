# TASK: P1b — grader fingerprints + fingerprint-match skip (P0-2)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration (continues P1a). D-P73 Phase 1 signs the
  scoring/grader_runner.py touch.
- Mirror pipeline/runner.py's established fingerprint discipline (compute
  → skip-on-match → versioned sibling on mismatch → never overwrite) —
  read runner.py:57-141 and test_fingerprint_idempotency.py first.

## Objective

Grading records gain a full provenance fingerprint; the schema-valid-only
skip (grader_runner.py:11,:110) becomes fingerprint-match skip. Committed
legacy grades (fingerprint-less) are never modified; new grading runs are
owner-gated anyway (no model calls in this task — tests use the existing
stub-CLI pattern in the grader tests).

## Design contract

1. FINGERPRINT (canonical-JSON sha256'd fields, per the direction):
   evaluatee_output_sha256, answer_key_sha256, rubric_sha256 (inspect:
   if the rubric is embedded in SYSTEM, record the SYSTEM prompt hash
   here AND as grader_system_prompt_sha256 with a comment explaining the
   identity; if a separate rubric artifact exists, hash it),
   grade_schema_sha256, grader_system_prompt_sha256, grader_model
   (the ACTUAL used_model incl. fallback), grader_harness_version,
   pipeline_commit.
2. SKIP: existing grade with matching fingerprint → skip (멱등). Existing
   grade WITHOUT fingerprint → FAIL-CLOSED status "stale_legacy_grade"
   (FB-03/D-P37 precedent — no silent trust, no auto re-call;
   --accept-legacy-grade opt-in flag mirrors --accept-legacy-output).
   Existing grade with DIFFERENT fingerprint → versioned sibling
   {neutral}.fp-<8>.json, original untouched.
3. Fingerprint-match sibling skip: if the sibling for the current
   fingerprint already exists and validates → skip (R1-01 lesson —
   include the third-run _never_called-style regression).
4. Tests (stub CLI, zero model calls): fingerprint content correctness;
   idempotent skip; legacy fail-closed + opt-in; mismatch sibling;
   sibling idempotency; original-bytes-untouched assertions.

## Files in scope
- scoring/grader_runner.py; its existing test file (extend); nothing else.

## Read-only / forbidden paths
- Everything else. grades outputs in runs/ or scoring/ dirs: tests use
  tmp_path only.

## Check command
check: ./.venv/bin/python -m pytest scoring tools -q

## Acceptance criteria
1. Fingerprint covers all 8 fields with real content hashes (test
   verifies each field changes the fingerprint).
2. Skip semantics exactly per contract incl. the R1-01 sibling lesson;
   legacy = fail-closed with opt-in.
3. No committed grade file modified (git status clean of runs/ and
   grade dirs).
4. Check passes; diff = the two files.
