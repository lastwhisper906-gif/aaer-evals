# TASK: FB-02 — cutoff: completed-payload fail-closed invariant + truthful log keys + METHOD wording

## Mode hint
mode: default

## PRE-FLIGHT — read first

- INV-17 (fetch-first) has ALREADY been satisfied by the orchestrator for
  this run. Your sandbox intentionally blocks `.git` writes — DO NOT run
  `git fetch` and DO NOT abort because it fails. Proceed to the edits.

## Objective

Close the documented-vs-actual gap in the cutoff guarantee (EXT_FB_B item
2, verified). Today the bulk loaders SILENTLY FILTER post-cutoff rows
(`pipeline/cutoff_guard.py:207`, `:236`) while METHOD.md §2 claims any
detected post-cutoff data kills the load with an exception; the summary log
key `"facts_after_cutoff"` (`:212`) actually holds the RETAINED
(pre-cutoff) count. After this task: raw files may contain post-cutoff
content (normal for SEC companyfacts), assembly filters it explicitly, and
a COMPLETED payload containing even one post-cutoff dated row raises
CutoffGuardError; log keys say what they mean; METHOD.md describes exactly
this three-layer structure.

## Files in scope

- pipeline/cutoff_guard.py — modify:
  (i) new public function `assert_payload_pre_cutoff(payload: dict,
  cutoff_date) -> None` that re-scans every dated row in a completed
  payload — all `fact["filed"]` dates inside
  `payload["financial_series_point_in_time"]` values and all
  `row["filing_date"]` inside `payload["filing_chronology"]` (NOTE: the
  completed payload uses the RENAMED key `filing_date`, see
  build_payload.py:156 — not raw-EDGAR `filingDate`; test fixtures must
  use the payload-side names) — and raises
  `CutoffGuardError` on any date > cutoff (== cutoff allowed, matching the
  existing boundary rule). Tolerant of absent keys? NO — missing either
  payload key raises (fail-closed).
  (ii) rename summary log keys at `:212-213`:
  `facts_after_cutoff` → `facts_retained_pre_cutoff`,
  `facts_dropped` → `facts_dropped_post_cutoff` (`facts_total` unchanged).
- pipeline/build_payload.py — modify: at the end of `build_payload()`,
  call `cutoff_guard.assert_payload_pre_cutoff(payload_dict, cutoff)` on
  the completed dict just before returning it (both arms — the perturbed
  arm rescales values, never dates, so this is arm-neutral / INV-04-safe).
- pipeline/test_cutoff_guard.py — modify: add tests for
  `assert_payload_pre_cutoff`: (a) clean payload passes; (b) one
  post-cutoff `filed` in the series raises CutoffGuardError; (c) one
  post-cutoff `filingDate` in the chronology raises; (d) boundary date ==
  cutoff passes; (e) payload missing a scanned key raises. Follow the
  file's existing fixture style.
- pipeline/test_all_raw_reads_enforced.py — modify line ~106 only: the
  assertion consuming the renamed log key (`facts_dropped` →
  `facts_dropped_post_cutoff`). Do not restructure the test.
- METHOD.md — modify ONLY the §2 paragraph (under
  `<!-- source: pipeline/cutoff_guard.py -->`): describe the actual
  three-layer guarantee — (1) raw SEC files may contain post-cutoff data
  (expected); (2) loaders drop post-cutoff rows as an explicit filter and
  log retained/dropped counts (describe the BEHAVIOR — do NOT hardcode
  the literal log key names in prose; the code and its test own those);
  (3) any post-cutoff date surviving into a COMPLETED payload raises
  CutoffGuardError (fail-closed), enforced at build_payload assembly;
  single-document loads (`load_document`) keep their existing
  raise-on-violation behavior. RETAIN both existing true sentences: the
  accession/filingDate cross-validation sentence (currently METHOD.md
  §2 lines ~21-22, backed by cutoff_guard.py:205-206) and the
  bypass-scan-test sentence. Do not touch any other METHOD.md section.

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- pipeline/cli_client.py, pipeline/api_client.py, pipeline/date_shift.py,
  pipeline/runner.py, pipeline/runner_api.py — do not touch
- schemas/, runs/, forward/, analysis/, scoring/, docs/ — do not touch
- README/RESULTS/REPRODUCING — do not touch (doc counts handled by
  orchestrator)

## Check command
check: ./.venv/bin/python -m pytest pipeline -q

## Acceptance criteria

1. `assert_payload_pre_cutoff` exists in cutoff_guard.py, scans BOTH the
   series `filed` dates and chronology `filingDate` dates of a completed
   payload, raises CutoffGuardError on any date strictly after cutoff, and
   raises on missing scanned keys.
2. `build_payload()` calls it on the completed dict for both arms before
   returning.
3. Summary log keys are exactly facts_total / facts_retained_pre_cutoff /
   facts_dropped_post_cutoff; `test_all_raw_reads_enforced.py` assertion
   updated to match; no other consumer of the old names remains
   (repo-wide grep in the review).
4. METHOD.md §2 describes the three-layer guarantee truthfully; the
   bypass-scan sentence is retained; no other doc section changed.
5. New tests (a)-(e) exist in test_cutoff_guard.py and the check command
   passes.
6. Diff touches ONLY the five files in scope.

## Explicitly out of scope

- Changing loader filter behavior to raise (the filter IS the design;
  the fail-closed layer is the completed payload).
- Touching runner/cli_client send paths (FB-01, already landed).
- Any METHOD.md change beyond the §2 paragraph.
- New Makefile targets, CI changes, schema changes.

## Notes / context

- The INV-03 disclosure D-entry for this fix is authored by the
  ORCHESTRATOR at merge time, not by this task (scoring/ and docs/ stay
  forbidden for the builder).
- INV-01 (look-ahead ban) is the governing invariant; PROJECT.md §5-1.
- `_parse_date` already exists in cutoff_guard for ISO validation — reuse.
- The perturbed arm's `_variant`/`_k_internal` keys are run-side; the new
  assert function must not choke on their presence (it only reads the two
  scanned keys — but their ABSENCE raises).
