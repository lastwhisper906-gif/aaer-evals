# TASK: FB-03 — legacy fingerprint auto-trust → stale-by-default with explicit opt-in

## Mode hint
mode: default

## PRE-FLIGHT — read first

- INV-17 (fetch-first) has ALREADY been satisfied by the orchestrator.
  Your sandbox blocks `.git` writes — DO NOT run `git fetch` and DO NOT
  abort because it fails.

## Objective

Today `pipeline/runner.py:113-116` silently trusts any schema-valid
existing output that has NO fingerprint ("legacy") and skips it — so
prompt/schema/pipeline drift keeps stale outputs alive invisibly
(EXT_FB_B item 7, verified). After this task the DEFAULT reports such an
output as STALE and REFUSES — an explicit FAIL status, no model call, no
files written (re-running is an owner-gated decision, DP-Q7; the runner
must never burn quota by surprise). Accepting legacy outputs becomes an
explicit opt-in flag.

## Files in scope

- pipeline/runner.py — modify:
  (i) `run_case(...)` gains keyword arg `accept_legacy_output: bool =
  False`. Gate ONLY the conditional at `:113-116` — the parse at
  `:109-112` keeps running unconditionally (it feeds the
  fingerprint-match skip at `:130`). With `accept_legacy_output=True`,
  keep the skip with status "skip (legacy output ACCEPTED via
  --accept-legacy-output — fingerprint 없음)". With the default False,
  return status "FAIL (stale_legacy_output — fingerprint 없음;
  --accept-legacy-output으로 명시 수용하거나 소유자 게이트 재실행)"
  BEFORE build_payload — no model call, no write. The `FAIL (` prefix
  makes main()'s existing failure counting produce a non-zero exit with
  no changes to main() beyond the flag.
  (ii) `main()` gains `--accept-legacy-output` (store_true), threaded to
  every `run_case` call.
  (iii) Update the module docstring line (`:13`) describing idempotency to
  match the new default (legacy = stale FAIL unless explicitly accepted).
- pipeline/test_fingerprint_idempotency.py — modify
  `test_legacy_valid_output_skips` and add coverage:
  (a) default: legacy output → NO model call (`_never_called` pattern),
  status starts with "FAIL" and mentions the flag, the original legacy
  file's bytes are UNCHANGED, and NO `.fp-` sibling is created;
  (b) `accept_legacy_output=True`: no model call, status contains
  "ACCEPTED";
  (c) keep the other idempotency tests untouched (fingerprint-match skip
  is unaffected).

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- pipeline/runner_api.py (no fingerprint logic — confirmed out of scope),
  pipeline/cli_client.py, pipeline/cutoff_guard.py,
  pipeline/build_payload.py, pipeline/probe_runner.py, pipeline/date_shift.py
- schemas/, runs/, forward/, analysis/, scoring/, docs/, METHOD.md,
  README*, REPRODUCING*

## Check command
check: ./.venv/bin/python -m pytest pipeline -q

## Acceptance criteria

1. Default `run_case` treats fingerprint-less schema-valid outputs as
   stale and REFUSES: status starts with "FAIL (stale_legacy_output",
   no model call, no file written, original byte-identical.
2. `--accept-legacy-output` CLI flag + `accept_legacy_output` kwarg
   restore the skip, with an explicit "ACCEPTED" status string.
3. Fingerprint-match idempotent skip (`:126-128` area) behaves exactly as
   before (existing tests still pass unmodified).
4. Module docstring reflects the new default.
5. Check command passes; diff touches ONLY the two files in scope.

## Explicitly out of scope

- Any real model invocation (tests use the existing mocks; the loop never
  runs the evaluatee — actual re-runs are owner-gated, DP-Q7).
- runner_api.py, provenance manifests for legacy files, analysis-side
  "published numbers must have fingerprints" gating (candidate follow-up,
  not this task).
- Behavior changes to the fp-sibling naming or fingerprint computation.

## Notes / context

- INV-03 disclosure D-entry authored by the ORCHESTRATOR at merge, not by
  this task.
- The fp-sibling mechanism (`runner.py:126-134`) is the
  disclose-don't-revise instrument: originals are never overwritten.
