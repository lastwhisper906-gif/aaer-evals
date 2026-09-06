# TASK: FB-01 — strip perturbation-experiment markers from model-visible payload (allowlist)

## Mode hint
mode: default

## PRE-FLIGHT — read first

- INV-17 (fetch-first) has ALREADY been satisfied by the orchestrator for
  this run: `git fetch origin` executed 2026-08-05, local main in sync at
  the base commit. Your sandbox intentionally blocks `.git` writes, so DO
  NOT run `git fetch` (it fails on `.git/FETCH_HEAD`) and DO NOT abort
  because of it. Proceed directly to the file edits.
- The BASE COMMIT already contains a checkpointed previous attempt at this
  task (allowlist in three send sites, `_variant` rename, new
  `pipeline/test_payload_blindness.py`) — committed as WIP with 7 tests
  still failing. Do not rewrite that work wholesale. The remaining work is
  the dependent-test updates listed in "Files in scope" (the three test
  files marked REMAINING), plus fixing anything in the WIP the check
  command still rejects.

## Objective

The model-visible payload must contain no field name or value revealing
that a perturbation/anonymization experiment is running. Today
`pipeline/build_payload.py` puts `"variant": "perturbed"|"original"` and
`"perturb_factor_recorded_scoring_side_only": None` into the payload;
`pipeline/runner.py:123` / `pipeline/runner_api.py:41` strip only
`_`-prefixed keys, and `pipeline/probe_runner.py:56-62` pops only
`_k_internal` — so these markers reach the model in every arm. After this
task: the model-visible JSON is built from an explicit ALLOWLIST of exactly
three keys (`case`, `financial_series_point_in_time`, `filing_chronology`),
variant is a run-side-only field, and a regression test fails on any
reintroduction.

## Files in scope

- pipeline/build_payload.py — modify: rename key `"variant"` →
  `"_variant"` (same values); DELETE the
  `"perturb_factor_recorded_scoring_side_only"` key entirely (its name is
  the leak; k already lives in `_k_internal`). No other change.
- pipeline/runner.py — modify: build `user_payload` from the allowlist
  `("case", "financial_series_point_in_time", "filing_chronology")` —
  KeyError on a missing key is the desired fail-closed behavior. Do not
  keep the `startswith("_")` strip as the mechanism.
- pipeline/runner_api.py — modify: same allowlist replacement.
- pipeline/probe_runner.py — modify: replace the `payload.pop("_k_internal")`
  + full-dict dump with the same three-key allowlist for the model-visible
  dict (v2ds payloads carry extra keys like `variant` from date_shift —
  the allowlist must exclude them WITHOUT touching date_shift.py).
- pipeline/test_build_payload.py — modify: update expectations for the
  renamed/removed keys; add `"variant"`, `"perturb"` (substring, covers
  perturbed/perturb_factor) to `FORBIDDEN_PAYLOAD_SUBSTRINGS` if that list
  is applied to model-visible text (be careful: the raw payload dict
  legitimately contains `_variant`/`_k_internal` run-side keys — the
  forbidden-scan must target the model-visible serialization, not the full
  dict).
- pipeline/test_payload_blindness.py — create: pin assertions to the
  RENDERED SENT STRING, not the dict. For ALL THREE send paths (runner.py,
  runner_api.py, probe_runner.py — the latter also with its v2-dateshift
  payload shape, which carries date_shift's post-build
  `"variant": "perturbed_v2_dateshift"` key) and BOTH arms
  (`perturb=False/True`), construct the exact model-visible JSON string
  (same allowlist + json.dumps flags as the send site) and assert:
  (1) none of {"variant", "perturb", "dateshift", "anonym",
  "scoring_side"} appears case-insensitively anywhere in the serialized
  text (key names AND values covered by string-level scan; synthetic
  fixtures must not contain these words naturally);
  (2) top-level key sets of the model-visible dict are IDENTICAL across
  arms (same-protocol, INV-04);
  (3) the run-side payload still records `_variant` and `_k_internal`
  (scoring bookkeeping intact).
  Use the existing synthetic-fixture pattern from test_build_payload.py /
  test_payload_synthetic.py — no network, no real corpus.

- pipeline/test_fingerprint_idempotency.py — modify: the module-level mock
  payload (used via `monkeypatch.setattr(runner.bp, "build_payload", ...)`)
  lacks `filing_chronology` → KeyError at runner.py's allowlist. Extend the
  mock payload to the new canonical shape: keys `case`,
  `financial_series_point_in_time`, `filing_chronology`, `_variant`,
  `_k_internal`. Keep every existing assertion's intent unchanged — this is
  a fixture-shape update, not a behavior change.
- pipeline/test_output_schema_enforcement.py — modify: same fixture-shape
  update for its mocked `build_payload` in
  `test_run_case_revalidates_before_write`.
- pipeline/test_payload_synthetic.py — modify:
  `test_all_cases_respect_cutoff_and_have_no_leakage_markers` currently
  serializes the FULL payload (line ~66), which now legitimately contains
  `_variant` and trips the extended forbidden list. Scan the model-visible
  subset instead (same three-key allowlist), mirroring the updated
  `test_payload_has_no_ground_truth_or_baseline_markers` in
  test_build_payload.py. The cutoff assertions stay on the full payload.

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- pipeline/date_shift.py, pipeline/cutoff_guard.py, pipeline/cli_client.py,
  pipeline/api_client.py — protected; do not touch
- schemas/ — do not touch (semantic changes are owner-gated)
- runs/, forward/, analysis/, scoring/, docs/ — do not touch
- METHOD.md, RESULTS.md, README.md — do not touch (doc alignment is FB-02)

## Check command
check: ./.venv/bin/python -m pytest pipeline -q

## Acceptance criteria

1. `build_payload()` return value has no key `"variant"` and no key
   `"perturb_factor_recorded_scoring_side_only"`; it has `"_variant"` with
   values `"perturbed"|"original"` and `_k_internal` unchanged.
2. runner.py, runner_api.py, probe_runner.py each construct the
   model-visible payload via the explicit three-key allowlist; no
   blacklist/strip logic remains as the isolation mechanism.
3. `pipeline/test_payload_blindness.py` exists, covers criteria (1)-(3) of
   its spec above for all three send paths (incl. the v2-dateshift payload
   shape) and both arms, and fails if `"variant"` is reintroduced into any
   model-visible serialization (verify by reading the assertion, not by
   trusting the test name).
4. Full pipeline suite passes (check command).
5. Diff touches ONLY the nine files in scope.

## Explicitly out of scope

- Any evaluatee/model invocation or re-run of existing outputs.
- date_shift.py cleanup (protected; its `variant` key is neutralized by
  the allowlist).
- Schema changes, METHOD/RESULTS/README wording, fingerprint semantics
  (FB-02/FB-03), CI changes.
- Renaming `_k_internal` or altering perturbation math.

## Notes / context

- INV-04 (same protocol both arms), INV-09 (scoring secrets never in
  evaluatee-visible paths) are the governing invariants.
- Changing user_payload changes future fingerprints
  (runner.compute_fingerprint) — intended; frozen runs/ are not touched;
  legacy-output handling is FB-03's task, not this one.
- The existing value-level guard (cli_client.guard_payload +
  FORBIDDEN_PAYLOAD_SUBSTRINGS) stays as defense-in-depth; this task adds
  structural blindness at the assembly layer.
