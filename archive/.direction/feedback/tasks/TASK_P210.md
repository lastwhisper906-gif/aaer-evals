# TASK: P2-10 — specs/SEALED_ANALYST_V0_1.md: decision-grade task schema + deterministic scoring (SPEC ONLY)

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- D-P50 Phase 2 #10 signed scope. SPEC ONLY: no schemas/ wiring, no
  call-path code, zero model calls. One new file under specs/ (this
  cycle's governance-diet slot; P2-09 used the previous cycle's).

## Objective

PROVENANCE: the decomposition "decision-grade output (3-level verdict /
falsifiable calls / covenant-style triggers)" and the scoring-formula list
(disclosure-event mapping, XBRL trigger recomputation, sector-ETF
excess-return windows and thresholds) are the OWNER'S DIRECTION TEXT
VERBATIM (D-P50 Phase 2 #10 original wording — the BACKLOG line
abbreviated it; cite D-P50 in the spec header).

Author specs/SEALED_ANALYST_V0_1.md: the "Sealed Analyst" task contract —
a decision-grade evaluatee output (3-level verdict / falsifiable calls /
covenant-style triggers) as an embedded JSON Schema (fenced block, NOT a
file in schemas/) plus a DETERMINISTIC scoring formula for every field.
The direction's filter governs every number: "recomputable from committed
artifacts."

## Required content

1. Task definition: what the Sealed Analyst produces per case — a 3-level
   verdict (enumerated levels with decision semantics), a set of
   FALSIFIABLE CALLS (each call = a proposition with a resolution date and
   a mechanical resolution rule), and COVENANT-STYLE TRIGGERS (threshold
   conditions on named XBRL series that, if crossed within a window,
   resolve the call).
2. The JSON Schema v0.1 (draft-7, embedded fenced block): field-by-field,
   additionalProperties: false, enums for verdict levels and trigger
   comparators, required arrays, format annotations consistent with the
   pinned jsonschema's date-only checker reality (D-P38 boundary — note
   it). Style-consistent with schemas/llm_output_v2.json (ordinal
   discipline; no probability vocabulary; INV-13 vocabulary rules in
   descriptions).
3. Deterministic scoring formula PER FIELD:
   - verdict: mapping to disclosure events (Item 4.02 non-reliance,
     restatement filings, AAER) with the event-source hierarchy and
     precedence rules — defined so that GIVEN a committed event registry
     snapshot, scoring is pure recomputation;
   - falsifiable calls: resolution = recomputation from committed XBRL
     facts at resolution date (state the exact comparator semantics,
     rounding, missing-data fail-closed rule);
   - triggers: XBRL trigger recomputation formulas (tag, unit, period
     alignment per the repo's existing cutoff/alignment conventions —
     cite pipeline/cutoff_guard.py conventions);
   - sector-ETF excess-return windows/thresholds: DEMOTED to a clearly
     marked NON-NORMATIVE APPENDIX (owner direction names the formula, so
     it must be pre-registered — but price/ETF data is NOT in committed
     artifacts today, so ETF-based fields are EXCLUDED from the v0.1
     normative schema entirely; the appendix pre-registers formula +
     window/threshold constants + data-provenance rules, states the
     INV-23 supervised-fetch precondition, and notes the INV-14
     no-position posture explicitly. Promotion to normative = a future
     schema version behind owner signature).
4. Every constant's justification: source from committed artifacts where
   possible (e.g. threshold families echoing decision_table.json's
   threshold grid), else marked PRE-REGISTERED CONSTANT with rationale —
   nothing silently arbitrary.
5. Worked example: one fully-populated instance (synthetic case, clearly
   marked synthetic) + its scoring walkthrough showing pure
   recomputation, field by field.
6. Execution preconditions checklist (owner-signature activated): event
   registry design, price-data acquisition (INV-23), schema wiring
   (schemas/ + FREEZE_REV), relationship to the forward cycle (INV-22 —
   this schema is a candidate for future cycles, NOT a change to
   cycle_001's sealed protocol).
7. CONSISTENCY CONSTRAINT: map the 3-level verdict onto
   specs/RISK_SCORE_SEMANTICS.md's existing decision vocabulary
   (decision_state: flag|review|no_flag|abstain, ordinal discipline) —
   either a stated mapping or an explicit supersession declaration; two
   competing decision vocabularies in specs/ without a relation is
   forbidden.
8. Anti-scope note: what v0.1 deliberately excludes (no portfolio
   construction, no advice semantics — INV-14 disclaimers embedded).

## Files in scope
- specs/SEALED_ANALYST_V0_1.md — create. Header: SPECIFICATION ONLY +
  INV-14 scope/disclaimer lines.

## Read-only / forbidden paths
- Everything else, especially schemas/ (no wiring), pipeline/, Makefile,
  forward/, BOTTLENECKS.md.

## Check command
check: ./.venv/bin/python tools/lint_publication.py && ./.venv/bin/python tools/check_sealed_analyst_spec.py

## Acceptance criteria
1. All 8 sections; exactly one draft-07 schema fence, check_schema-clean;
   every OTHER json fence (worked example) machine-validates against it
   (the check proves both); every constant sourced-or-preregistered; ETF
   axis non-normative appendix only; RISK_SCORE_SEMANTICS mapping present.
2. No fraud vocabulary toward non-enforced companies; synthetic example
   clearly synthetic (INV-13).
3. Check passes; diff = the one new file.

## Notes
- MERGE PROTOCOL (orchestrator): D-entry with protected-path disclosure
  line (specs/); docs-refresh check (no test change expected).
