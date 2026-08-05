# TASK: P6a — multiple-testing disclosure (Phase 6, audit item 24)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration. audit/FEEDBACK_TRIAGE.md line 24 confirmed
  this ABSENT on HEAD: grep for family-wise / 다중 검정 / bonferroni /
  holm / FDR across RESULTS.md, METHOD.md, docs/methodology_limitations.md
  returns 0 hits. RESULTS.md publishes 13 rows, several carrying p-values.
- INV-03/INV-06: you may NOT change any published number, threshold,
  decision rule, or metric definition. This task ADDS disclosure only.
  Adjusted values are NEW derived statistics published in a NEW path
  alongside the originals — never a replacement, never an edit to an
  existing RESULTS.md cell value.
- Precedent to follow exactly: FB-09 (ac29b6d) put its annex in a NEW
  file docs/STATS_ANNEX.md and touched published docs only with pointer
  lines + doc-count refresh. Do the same shape here.
- Direction constraint: NO new top-level docs. docs/ is fine.

## Required content
1. Enumerate the test family explicitly: which published p-values are
   pre-registered confirmatory (with the plan file + freeze commit that
   pre-registered each), which are context-only, and which are
   EXPLORATORY (L4 / E2 trajectory / exploratory_combo). Cite the row
   number in RESULTS.md for each. The families must not be pooled —
   the no-pooling discipline in RESULTS.md applies here too.
2. State the multiplicity problem in plain terms for the confirmatory
   family only, and give a Holm–Bonferroni step-down adjustment of that
   family computed deterministically in Python (stdlib only; INV-11 —
   no new dependency). Report adjusted p alongside raw p in a new table.
   Do NOT recompute or restate any raw p-value: read them from the
   frozen artifacts the RESULTS.md Source column already names.
3. Say plainly whether each confirmatory conclusion survives adjustment
   at the pre-registered alpha. If a conclusion does not survive, say so
   in the same sentence as the conclusion — no burying.
4. An honest limits paragraph: Holm controls FWER, not FDR; the
   permutation p-values are Monte-Carlo estimates (cross-reference
   docs/STATS_ANNEX.md for MC error) so adjusted values inherit that
   error; and adjustment cannot repair the selection/survivorship bias
   already disclosed for the control sets.
5. Pointer lines from RESULTS.md and METHOD.md to the new annex.
   Pointer text only — no cell edits, no number edits.

## Files in scope
- docs/MULTIPLE_TESTING.md — create (annex; INV-14 scope + disclaimer
  lines; SPECIFICATION-adjacent header not required, this is analysis).
- tools/multiple_testing.py — create; stdlib-only deterministic Holm
  computation reading the frozen artifacts named by RESULTS.md.
- tools/test_multiple_testing.py — create; must include a case with a
  known hand-computable Holm result, and a fail-closed test that the
  tool refuses when a source artifact is missing rather than inventing.
- RESULTS.md, METHOD.md — pointer line only.
- README/REPRODUCING doc-count blocks if make docs-refresh requires it.

## Check command
check: ./.venv/bin/python -m pytest tools/test_multiple_testing.py -q && ./.venv/bin/python tools/lint_publication.py && ./.venv/bin/python tools/lint_doc_counts.py

## Acceptance criteria
1. Confirmatory vs exploratory family split is explicit and each member
   cites its pre-registration source; no pooling across tasks/layers.
2. Holm computed in stdlib Python, deterministic, tested against a
   hand-computed case; fail-closed on missing artifacts (tested).
3. Zero published numbers changed — diff shows no edit to any existing
   RESULTS.md value cell. Pointer lines only in published docs.
4. Non-surviving conclusions, if any, stated in the same sentence as
   the conclusion.
5. Limits paragraph covers FWER-vs-FDR, MC error inheritance, and that
   adjustment does not repair selection bias.
