# TASK: P1-04b2 — English-canonical analysis/error_analysis_wave2_holdout.md (Q-F15, BN-14 second half)

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- D-P50 Phase 1 #4 signed scope. F-01/F-02 protocol, P1-04a precedent.

## Objective
RESULTS row 9's source doc is Korean-only. A complete English draft
EXISTS at docs/ERROR_ANALYSIS_WAVE2_HOLDOUT_EN_DRAFT.md (Q-F15 proposal
① — PROMOTE it, do not retranslate; remove its DRAFT banner). Original
path becomes English canonical; Korean preserved
at analysis/error_analysis_wave2_holdout.ko.md; token-equivalence locked;
EN enrolled in lint DOCS.

## Files in scope
- analysis/error_analysis_wave2_holdout.ko.md — create: byte-exact copy
  of the current file + ONE header blockquote line prepended: "> 한국어
  원본 (동결) — 영어 정본: error_analysis_wave2_holdout.md (F-01/F-02, D-P50)"
- docs/ERROR_ANALYSIS_WAVE2_HOLDOUT_EN_DRAFT.md — DELETE in this commit
  (orphaned banner after promotion).
- analysis/error_analysis_wave2_holdout.md — replace with the promoted
  draft content (verbatim where current vs the ko original; translate any
  ko content added since the draft): every numeric token identical; identifiers/canaries/HTML
  comments preserved as-is (Korean inside HTML comments is allowed — the
  equivalence test strips comments for the Hangul check); second line =
  "> Korean original: [error_analysis_wave2_holdout.ko.md](error_analysis_wave2_holdout.ko.md) (frozen)."
  placed ABOVE the H1 as the leading line (the equivalence helper strips
  leading "Korean original" blockquotes — placement is load-bearing);
  the line-9 "분식" vocabulary quote must be rendered WITHOUT Hangul in
  the EN canonical (romanize as "bunsik" with a gloss or paraphrase —
  sanctioned deviation from strict 1:1, note it in a comment);
  translate meaning 1:1 otherwise, no added/dropped caveats; INV-13 vocabulary
  discipline (this doc discusses enforced historical cases — existing
  vocabulary is compliant; do not introduce new "fraud" toward
  non-enforced companies); lint rules (E)/(G) apply once enrolled (both verified clean in the draft) —
  carry tier tokens (wave-2/holdout) through and keep any lower-bound
  phrasing with its corrective clause if present in the original.
- tools/test_translation_equivalence.py — extend TRANSLATION_PAIRS with
  the new 4-tuple (marker = the ko header line; en_truncate = None).
- tools/lint_publication.py — DOCS += the EN file only (ko deferred,
  same D-P55 reason — one comment line).

## Read-only / forbidden paths
- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md; every other
  analysis/ file; runs/, scoring/, schemas/, docs/, README*, RESULTS*,
  BOTTLENECKS.md, ERRATA.md

## Check command
check: ./.venv/bin/python -m pytest tools -q && ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. EN complete (no Hangul outside HTML comments), 1:1 structure, tokens
   identical (test-locked); ko byte-exact + header note.
2. Registry + DOCS extended; lint RC=0; check passes.
3. Diff touches ONLY the five listed paths (incl. draft deletion).

## Out of scope
- ERRATA (P1-04c), BN-14 flip (orchestrator — after this lands),
  RESULTS.md row-9 link text (unchanged — path is same).

## Notes
- MERGE PROTOCOL (orchestrator): docs-refresh; reader gate 2 personas on
  the EN doc; Q-F15 + BN-14 flips; D-entry.
