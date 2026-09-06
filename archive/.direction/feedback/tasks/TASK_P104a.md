# TASK: P1-04a — BN-11: English-canonical analysis/DECISION_TABLE.md (F-01/F-02)

## Mode hint
mode: inverted

## PRE-FLIGHT — read first
- INV-17 already satisfied by the orchestrator. DO NOT run `git fetch`;
  do not abort on its failure.
- D-P50 owner direction Phase 1 #4 orders this; the analysis/ and
  tools/lint_publication.py touches are signed-scope.

## Objective

BN-11: the README headline's most load-bearing evidence link
(`analysis/DECISION_TABLE.md`, 111 lines) is Korean-only. Apply the
established F-01/F-02 protocol (D114 precedent, AUDIT_INDEX/REPRODUCING
pattern): the original path becomes the ENGLISH canonical, the current
Korean text is preserved verbatim at `analysis/DECISION_TABLE.ko.md`,
numeric fidelity is machine-locked, and both files enter the publication
lint's DOCS list in the SAME commit (D115/D118 learning note: surface
promotion and lint enrollment must not split).

## Files in scope

- analysis/DECISION_TABLE.ko.md — create: byte-exact copy of the current
  analysis/DECISION_TABLE.md, with ONLY a one-line header note appended
  at the very top: "> 한국어 원본 (동결) — 영어 정본: DECISION_TABLE.md
  (F-01/F-02, D-P50)". Nothing else changes.
- analysis/DECISION_TABLE.md — replace content by PROMOTING the existing
  draft `docs/DECISION_TABLE_EN_DRAFT.md` (the Q-F11 artifact): use it
  verbatim where it matches the current Korean content, remove its DRAFT
  banner, translate and insert the fig_tradeoff figure block + caption
  (ko original lines ~8-12 — the only content added since the draft),
  and add as the second line the English back-pointer per D114/D118
  precedent: "> Korean original: [DECISION_TABLE.ko.md](DECISION_TABLE.ko.md)
  (frozen)." Translation rules:
  (i) EVERY numeric token (numbers, percentages, intervals, thresholds,
  currency, dates, counts like 12/12, 5/7) appears IDENTICALLY — no
  rounding, reformatting, or unit conversion;
  (ii) governance identifiers (D94, Q-O02, CP95, T≥50 etc.) stay as-is —
  this is an evidence document, not the README first screen;
  (iii) the header owner-signature blockquote, the fig_tradeoff figure
  block (added 2026-08-05), all table structure, and all
  section numbering preserved 1:1;
  (iv) INV-13/14 vocabulary discipline: no fraud-vocabulary toward
  non-enforced companies (current text is compliant — do not introduce
  any); keep the "ordinal, not calibrated probability" sentences intact
  in translation;
  (v) tone: plain, precise English — translate meaning, never editorialize
  or add/drop caveats.
- tools/lint_publication.py — modify DOCS list only: add
  "analysis/DECISION_TABLE.md" and "analysis/DECISION_TABLE.ko.md"
  (D115/D118 pattern). NO other change to the lint.
- docs/DECISION_TABLE_EN_DRAFT.md — DELETE in this same commit (its
  banner "unadopted English translation" becomes false the moment the
  promotion lands; leaving it creates a divergent orphan).
- tools/test_translation_equivalence.py — create: a reusable
  token-equivalence test: for each (en, ko) pair in an explicit registry,
  strip each file's added pointer/banner blockquote lines (the ko
  frozen-note and the en Korean-original pointer — define the exclusion
  precisely as leading blockquote lines containing 'F-01/F-02' or
  'Korean original'), then extract the multiset of numeric tokens (regex
  for numbers incl. decimals, percentages, ratios a/b, intervals) and
  assert equality, reporting missing/extra tokens. Also assert the ko
  file contains the frozen-original header note and the en file contains
  NO Hangul anywhere (no exclusions needed — the back-pointer is
  English).

## Read-only / forbidden paths
- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- Every other analysis/ file, runs/, scoring/, schemas/, README*,
  RESULTS*, BOTTLENECKS.md (flip = orchestrator), ERRATA.md,
  docs/methodology_limitations.md (P1-04b/c, separate cycles)

## Check command
check: ./.venv/bin/python -m pytest tools -q && ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. DECISION_TABLE.md is complete English (no Hangul), 1:1 structure,
   every numeric token identical (test-locked); .ko.md is the byte-exact
   original + the single header note.
2. Both files in lint DOCS; lint_publication RC=0 on the finished tree.
3. Token-equivalence test exists, is registry-extensible, and fails on a
   single-token corruption (verify by reading assertions).
4. Check command passes; diff touches ONLY the five listed paths (en, ko, lint DOCS, new test, draft deletion).

## Explicitly out of scope
- methodology_limitations / ERRATA (P1-04b/c); README caption changes;
  BN-11 status flip (orchestrator); any numeric or substantive change.

## Notes / context
- MERGE PROTOCOL (orchestrator): docs-refresh; reader gate (2 personas)
  on the English table BEFORE merge; atlas/case_{05,07,11,14}.md
  attribute verbatim Korean quotes to "analysis/DECISION_TABLE.md §4" —
  repoint those attributions to DECISION_TABLE.ko.md at merge (they
  become factually wrong after promotion); Q-F11 → RESOLVED flip citing
  D-P50 + BN-11 flip in the D-entry.
