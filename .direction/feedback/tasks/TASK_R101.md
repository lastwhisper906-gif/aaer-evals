# TASK: R1-01/02/03 — resume idempotency + cross-model pin + registry coverage (pre-launch bundle)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Three S-sized correctness fixes from the R1 replenish review
  (.direction/feedback/replenish_R1_2026-08-05.md — cite it for full
  evidence; fix shapes are specified there and repeated here). R1-02/03
  MUST land before the parked D-P49 launch command is ever executed.

## Files in scope

- pipeline/runner.py — R1-01: in run_case, before the model call on the
  stale-superseding path (write_path = fp-sibling, ~:138-141), if
  write_path.exists() and its parsed fingerprint equals the current
  fingerprint → return {"case_id": cid, "status": "skip (멱등 —
  fp-sibling 일치)"}. Two-ish lines. Nothing else.
- pipeline/test_fingerprint_idempotency.py — R1-01 regression: extend the
  stale-versioned test with a third _run using the _never_called mock —
  proving resume no longer re-calls or rewrites (assert sibling bytes
  unchanged).
- pipeline/crossmodel_gpt.py — R1-02: (i) codex_command gains a pinned
  model: module constant CODEX_MODEL_PIN (string; choose the codex CLI's
  current documented default id by INSPECTING `codex --help`/config
  OFFLINE — if not determinable offline, set the constant to a
  placeholder "OWNER-SET-BEFORE-LAUNCH" AND make the runner fail-closed
  at startup when the pin is the placeholder or absent from the command);
  pass `-c model=<pin>` (verify the exact flag syntax from codex --help
  offline; if unverifiable, implement via a CODEX_MODEL_ARGS constant
  with the same fail-closed placeholder discipline). (ii) post-call:
  reject records whose reported model fails the _pin_matches semantics
  (cli_client.py:173-176 precedent: reported == pin or
  reported.startswith(pin + "-") — plain startswith would let pin gpt-5
  accept gpt-5.2-codex) or equals MODEL_FALLBACK — case FAIL, not accept. (iii) `codex --version` check
  moves PRE-call and fail-closed (mirror cli_client.enforce_harness_pin
  shape; a version-pin constant with the same placeholder discipline).
- pipeline/test_crossmodel_gpt.py — R1-02 tests, INCLUDING the three
  existing-test updates (not out-of-scope surprises):
  (i) test_unavailable_codex_version_uses_honest_fallback (~:178-196)
  INVERTED — unavailable version is now fail-closed refusal;
  (ii) test_valid_response_writes_conformant_provenance (~:137-176)
  monkeypatches the pin constants so its "gpt-test"/"codex-cli test"
  mocks pass the new checks;
  (iii) test_dry_run_has_hashes_and_no_subprocess (~:199-216) must keep
  holding — therefore the live `codex --version` check is LAZY before
  the first real call (enforce_harness_pin's once-per-process shape,
  cli_client.py:128-146), never unconditional at startup; only the
  placeholder-string check (no subprocess) is unconditional.
  New tests: placeholder pin → refusal; wrong/missing model → FAIL.
- scoring/experiment_registry.json — R1-03: ONE additive experiment
  entry "crossmodel_gpt" with the FULL entry shape (verify_blindness.py:50
  hard-requires score_commit/label_join_commit — KeyError otherwise;
  aux_nonexperiment at registry:28-30 is the convention template):
  {"score_commit": "UNKNOWN", "label_join_commit": "UNKNOWN",
   "analysis_commit": "UNKNOWN",
   "output_globs": ["runs/crossmodel_gpt/**/*.json"],
   "perturbed_globs": [],
   "aux_globs": ["runs/crossmodel_gpt/**/*.jsonl"]}.
  NOTHING else changes in the file (protected path — additive coverage
  EXPANSION, disclosed by orchestrator D-entry).
- tools/test_blindness_registry_coverage.py — R1-03: create — assert the
  D-P49 launch out-dir (runs/crossmodel_gpt/wave1_original) is covered by
  at least one registry output_glob and the audit jsonl pattern by an
  aux_glob (pure glob-matching test, no runs/ files needed).

## Read-only / forbidden paths
- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md; every other
  scoring/ file; runs/, analysis/, schemas/, docs/, Makefile, README*;
  tools/verify_blindness.py (read-only — coverage proven by the new test)

## Check command
check: ./.venv/bin/python -m pytest pipeline tools -q

## Acceptance criteria
1. R1-01: third-run regression proves no re-call/no rewrite; sibling
   bytes byte-identical; original tests unbroken.
2. R1-02: no code path can execute a codex call without a concrete model
   pin in the command AND a pre-call version check; fallback/mismatched
   model strings are FAILs, never accepted records.
3. R1-03: registry entry additive-only (diff shows one inserted object,
   full key shape incl. score_commit/label_join_commit); coverage test
   passes, fails if the entry is removed, and asserts those two keys
   exist (two assertions — no schema-linter generalization).
4. Check passes; diff touches ONLY the six listed files.

## Out of scope
- R1-04 (deferred); any launch of the tranche; verify_blindness.py
  changes; registry-linter generalization (reviewer kill).

## Notes
- MERGE PROTOCOL (orchestrator): docs-refresh (test count changes);
  D-entry disclosing the scoring/ additive touch + updating D-P49's
  launch packet preconditions (pin must be owner-confirmed at launch).
