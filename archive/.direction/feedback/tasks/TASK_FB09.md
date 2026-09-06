# TASK: FB-09 — Monte-Carlo error / seed / exactness annex for published statistics

## Mode hint
mode: inverted

## PRE-FLIGHT — read first

- INV-17 already satisfied by the orchestrator. DO NOT run `git fetch`;
  do not abort on its failure.

## Objective

EXT_FB_B item 10 (executable subset): published Monte-Carlo permutation
p-values carry no Monte-Carlo standard error, the bootstrap/seed
provenance of AUC CIs is not surfaced in one place, and no doc states
where exact permutation is feasible. Produce a deterministic annex
(script + doc + tests) that reports these FROM COMMITTED ARTIFACTS ONLY —
no frozen number is recomputed or revised, no analysis/ file is touched.

## Files in scope

- tools/stats_annex.py — create: stdlib-only, deterministic, no RNG.
  (i) reads analysis/results_stats.json and analysis/wave2_results.json;
  (ii) for each Monte-Carlo permutation p-value it reports MC-SE =
  sqrt(p(1-p)/B) and a 95% MC interval p ± 1.96·SE. B must be taken from
  the analysis SOURCE code (read-only: cite file:line in a comment, e.g.
  the n_permutations constant in the wave-1/wave-2 analyzers) — NEVER
  inferred by inverting p-values; if a B cannot be located for some
  p-value, the row prints "B: not located in source — MC-SE not computed"
  (honest gap, no guess);
  (iii) exact-permutation feasibility via math.comb for EVERY design
  whose MC p appears in the annex — 8v22, 9v23, AND the pooled design
  behind pooled_secondary (17v45: C(62,17) is astronomically large —
  this row shows MC was necessary, not merely convenient): print C(n,
  n_t) and whether full enumeration is feasible (report the count; NO
  threshold editorializing beyond "enumerable on commodity hardware:
  yes/no" with the count shown);
  (iii-b) state the permutation p estimator form (ge+1)/(n+1) with its
  source citation (the stats module) — the raw artifact values (e.g.
  116/100001, 3/100001) only reconcile under it and readers will check;
  (iv) seed/provenance table: the seed values and CI-method fields AS
  RECORDED in the artifacts (e.g. results_stats.json "seed", auc_boot95;
  wave2 auc_ci) with artifact key paths. For provenance absent from the
  ARTIFACT but present in the analysis SOURCE, report it as
  "not in artifact; source: <file:line>" with the actual value (e.g.
  wave2_results.json has no seed field — the seed lives in the wave-2
  analyzer source; cite file:line, never guess, never report
  source-locatable provenance as merely 'absent');
  (v) --json flag mirroring the printed tables.
- docs/STATS_ANNEX.md — create: annex doc, FB-07/POWER_ANALYSIS.md
  conventions: purpose · method · pasted actual script output (marked
  regenerable) · what this does NOT do (no recomputation, no revision,
  no new statistics claims; exact-permutation rows are feasibility notes,
  not results) · repo-standard scope/disclaimer phrasing (INV-14) · no
  recommendations.
- tools/test_stats_annex.py — create: (a) determinism (two runs
  identical); (b) MC-SE formula spot-check against a hand-computed value;
  (c) every p-value mentioned in the annex equals the committed artifact
  value exactly (read both, compare — the annex can never drift from
  artifacts); (d) --json parses and matches printed numbers; (e) the
  B citations in comments point at real files (existence check of the
  cited paths).

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- analysis/ (ALL — read-only source of truth), runs/, forward/, scoring/,
  schemas/, pipeline/
- every existing tools/ and docs/ file (new files only)
- README*, REPRODUCING*, METHOD.md, RESULTS.md, CLAIMS.json

## Check command
check: ./.venv/bin/python -m pytest tools -q

## Acceptance criteria

1. tools/stats_annex.py stdlib-only, deterministic, artifact-faithful
   (test c), honest about unlocatable B (no inversion inference).
2. docs/STATS_ANNEX.md contains actual output, the not-doing section,
   INV-14 phrasing, no recommendations.
3. Tests (a)-(e) pass; check command passes.
4. Diff touches ONLY the three new files.

## Explicitly out of scope

- Recomputing any statistic; editing analysis/; running permutations or
  bootstrap; changing primary/secondary/exploratory tiering (B10's
  tiering ask is a measurement-condition question — owner-gated).
- PR-AUC/PPV (DP-Q6 scope).

## Notes / context

- MERGE PROTOCOL: new test file changes pytest count — verify-public red
  at lint_doc_counts until orchestrator runs `make docs-refresh` at
  merge (established precedent); not a builder failure.
- INV-03 disclosure D-entry authored by the ORCHESTRATOR at merge.
- Known artifact facts (verify, don't trust): results_stats.json has
  "seed": 20260707 and auc_boot95 lists; wave2_results.json has perm_p
  values like 0.0011599884... and auc_ci; the permutation-count constant
  lives in the analysis/ source files.
