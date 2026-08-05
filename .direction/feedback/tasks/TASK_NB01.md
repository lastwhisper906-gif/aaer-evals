# TASK: NB-01 — schemas/llm_output_v2.json: risk_score rename (v1 untouched)

## Mode hint
mode: default

## PRE-FLIGHT — read first
- INV-17 already satisfied by the orchestrator. DO NOT run `git fetch`;
  do not abort on its failure.

## Objective

Owner-signed decision D-P44a (+ standing authorization D-P45): the v2
evaluatee contract renames `misstatement_probability` →
`misstatement_risk_score` and rewrites its semantics to ordinal-rank
language, resolving the published probability/ordinal conflict (EXT_FB_B
item 5) for FUTURE waves. v1.2 (`schemas/llm_output.json`) stays frozen
byte-for-byte for wave-1/2 comparability. ADOPTION (wiring into runner)
is NOT this task — it happens at the next FREEZE_REV under the pin
discipline; this task ships the versioned contract file plus a test that
proves v2 differs from v1 in exactly the intended ways.

## Files in scope

- schemas/llm_output_v2.json — create: copy of schemas/llm_output.json
  with EXACTLY these deltas:
  (1) every occurrence of `misstatement_probability` →
  `misstatement_risk_score` — ALL EIGHT sites: property keys, required
  arrays (top-level and $defs.model_output), $defs entries, the if/then
  mechanism_hypotheses trigger, the $ref VALUE STRINGS (e.g. line ~17 —
  the JSON-pointer text itself), AND the literal mention inside the
  mechanism_hypotheses field DESCRIPTION (line ~112: "misstatement_probability
  >= 40이면 최소 1개 필수" → renamed). Note check_schema does NOT resolve
  $refs — a stale $ref only surfaces in instance-validation test (d), so
  get them all;
  (2) the renamed field's description rewritten: ordinal 0-100 risk rank,
  explicitly "서수(ordinal) 위험 순위 — 보정된 확률이 아니다"; no 확률/
  probability vocabulary anywhere in the RENAMED field's description;
  fraud-vocabulary ban unchanged (INV-13 note stays);
  (3) top-level "description" gains a v2 header sentence: "v2 (D-P44a/
  D-P45, 2026-08-05): misstatement_probability → misstatement_risk_score
  서수 개명 — v1.2는 wave-1/2 비교가능성을 위해 동결; 채택은 차기
  FREEZE_REV에서."; version marker "status: v2.0" replacing v1.2 in that
  description;
  (4) NOTHING else — same $schema draft, same structure, same all other
  fields.
- tools/test_schema_v2.py — create:
  (a) structural-diff test: load both schemas, walk both trees, assert
  the ONLY differences are (i) the key/`$ref`-string rename anywhere it
  occurs, (ii) the renamed field's description, (iii) the top-level
  description, and (iv) the mechanism_hypotheses description's renamed
  mention (compare it as: v1 text with the substring renamed == v2 text).
  Any other difference fails with the JSON-pointer path in the message.
  (b) v1-untouched guard: assert schemas/llm_output.json still contains
  "misstatement_probability" and does NOT contain "risk_score".
  (c) v2 hygiene: renamed field description contains "ordinal" or "서수"
  and none of {"확률", "probability"}; Draft7Validator.check_schema
  passes for v2 (with FormatChecker availability irrelevant to schema
  check).
  (d) trigger semantics: a minimal v2 instance with
  misstatement_risk_score=45 and empty mechanism_hypotheses FAILS v2
  validation; the same with score=30 PASSES that clause (construct
  minimal valid instances per the schema's required fields).

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- schemas/llm_output.json and every OTHER existing schemas/ file —
  byte-untouched (test b guards this)
- pipeline/ (ALL — no adoption wiring), analysis/, runs/, scoring/,
  docs/, README*, METHOD.md, RESULTS.md, Makefile, .github/

## Check command
check: ./.venv/bin/python -m pytest tools -q

## Acceptance criteria

1. schemas/llm_output_v2.json exists; validate_schemas.py-style schema
   check passes; deltas are exactly (1)-(4).
2. Structural-diff test (a) passes and demonstrably fails on any
   extraneous difference (read the assertion logic).
3. v1 file byte-identical (git diff empty for it) and test (b) guards
   the invariant-relevant content.
4. Tests (a)-(d) pass; check command passes.
5. Diff touches ONLY the two new files.

## Explicitly out of scope

- Runner/prompt wiring, FREEZE_REV note, scoring-side accessors
  (adoption cycle, owner-gated by pin discipline).
- ECE/Brier demotion edits in analysis (future-wave concern).
- Any edit to v1 schemas.

## Notes / context

- MERGE PROTOCOL: orchestrator runs make docs-refresh at merge (pytest
  count changes); INV-03 disclosure D-entry by orchestrator.
- tools/validate_schemas.py globs schemas/*.json — the new file enters
  that gate automatically; ensure it passes.
