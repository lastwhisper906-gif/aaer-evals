# TASK: FB-04 — attach FormatChecker to evaluatee-path schema validators

## Mode hint
mode: default

## PRE-FLIGHT — read first

- INV-17 already satisfied by the orchestrator. Your sandbox blocks `.git`
  writes — DO NOT run `git fetch`, DO NOT abort on its failure.

## Objective

Schemas declare `"format": "date"` on cutoff-relevant fields (e.g.
`schemas/llm_output.json:59` filing_date — "filing_date > cutoff_date인
항목이 있으면 실행 무효"), but the three evaluatee-path validator call
sites use bare `Draft7Validator(schema)`, which IGNORES format entirely —
a malformed or nonsense date string passes validation (EXT_FB_B item 6,
validator half; verified). After this task all three sites validate with
`format_checker=jsonschema.FormatChecker()` and a regression test proves a
bad date is rejected.

KNOWN BOUNDARY (state in a code comment at ONE site, the runner one): the
pinned jsonschema wheel has a built-in draft-7 checker for `date` ONLY —
`date-time`, `time`, and `uri` all require extra packages (rfc3339-validator
etc. — INV-11 forbids new deps).
`run_timestamp` (`format: date-time`) and `aaer_url` (`format: uri`)
therefore remain format-unchecked; jsonschema silently skips formats
without checkers. Do NOT hand-roll checkers for them.

## Files in scope

- pipeline/runner.py — modify line ~176: `jsonschema.Draft7Validator(
  FULL_OUTPUT_SCHEMA, format_checker=jsonschema.FormatChecker())`; add the
  KNOWN BOUNDARY comment (1-3 lines) here.
- pipeline/cli_client.py — modify lines ~215 and ~329: same
  `format_checker=jsonschema.FormatChecker()` argument. NO other change to
  this file (it is a protected enforcement surface; the diff must be
  exactly these two argument additions).
- pipeline/test_output_schema_enforcement.py — two changes:
  (i) line ~120 `test_all_committed_run_outputs_validate` must ALSO pass
  `format_checker=jsonschema.FormatChecker()` — otherwise production
  validators are stricter than the regression test asserting committed-
  output validity (pre-review empirically confirmed every committed
  filing_date in runs/, forward/, pilot/ is strict ISO — this stays green
  and becomes the permanent CI answer to the frozen-output question).
  Lines ~65-66 stay bare (they assert invalidity).
  (ii) add one test: an output fixture valid under the bare validator but
  carrying a non-date string in a `format: "date"` field (e.g.
  documents_used[0].filing_date = "not-a-date") is REJECTED by (a)
  `runner`'s validation path and (b) `cli_client.output_is_valid`. Assert
  the same fixture with a proper date passes.

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- schemas/ — DO NOT touch (semantic tightening is owner-gated DP-Q1; this
  task changes only validator call sites)
- pipeline/cutoff_guard.py, build_payload.py, probe_runner.py,
  date_shift.py, runner_api.py
- runs/, forward/, analysis/, scoring/, docs/, METHOD.md, README*,
  REPRODUCING*

## Check command
check: ./.venv/bin/python -m pytest pipeline -q

## Acceptance criteria

1. All three call sites (runner.py ~:176, cli_client.py ~:215, ~:329) pass
   `format_checker=jsonschema.FormatChecker()`.
2. New test proves a non-date string in a format:"date" field fails
   validation on both the runner path and `output_is_valid`, and the
   corrected fixture passes.
3. The KNOWN BOUNDARY comment exists at the runner site; no hand-rolled
   date-time/uri checkers; no new dependencies (requirements.* untouched).
4. Check command passes; diff touches ONLY the three files in scope.

## Explicitly out of scope

- Schema file changes (checklist counts, enums, probability rename — all
  owner-gated DP-Q1).
- Adding rfc3339/uri checker dependencies (INV-11).
- tools/-side validators (already use FormatChecker where they validate
  instances).

## Notes / context

- INV-03 disclosure D-entry authored by the ORCHESTRATOR at merge.
- BOTH cli_client.py AND runner.py are on the repo's .protected-paths
  list (`pipeline/runner` prefix); this loop may touch them only because
  the owner's 2026-08-05 priority rule names schema enforcement — diffs
  there must stay surgically minimal (argument additions + the boundary
  comment), verified hunk-by-hunk in the post-review.
- Honesty note for the D-entry: cli_client.py:215 sees only schemas
  without format annotations today — that change is defense-in-depth, not
  a live-hole fix; the live holes are runner.py:~176 and output_is_valid.
