# TASK: Phase 3 — verification-surface honesty: verify-claims + CLAIMS-driven gate + figure-gate extension (P1-4/P1-5)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration. D-P73 Phase 3 signs Makefile/CLAIMS touches.
- verify-public's existing 7 commands stay VERBATIM (INV-05); new
  targets are additive; verify-public additionally becomes documented as
  the alias of the claims+fixture pair (docs wording — README/REPRODUCING
  edits allowed HERE, unlike P1a: run make docs-refresh yourself at the
  end and include the regenerated blocks; that resolves the P1a-class
  conflict in-task).

## Design contract

1. Makefile (additive targets only):
   verify-claims: reproduce_analysis + test_recompute_published subset +
     verify_figures + the new CLAIMS iterator (below);
   verify-fixture-pipeline: the synthetic-fixture pytest subset
     (pipeline tests that exercise cutoff→payload on fixtures — select by
     existing markers/paths, do not invent new fixtures);
   reproduce-corpus / rerun-evaluatee: documented-refusal stubs (echo the
     honest preconditions + exit 1 — they exist as named, labeled rungs
     of the reproduction ladder; REPRODUCING §2 already carries the
     honest scope).
2. CLAIMS.json v2: add per-claim "recompute": {"command": <exact command
   or artifact-read instruction>, "artifacts": [paths]} and
   "limitation_ref" (L-x / row-limits pointer). Keep the existing
   verbatim-lock columns unchanged (the ledger test guards them — extend
   the test for the new keys' presence, not content-lock).
3. tools/verify_claims_coverage.py: iterate CLAIMS.json — every claim's
   artifacts exist; every RESULTS table row id (1..13) appears; every
   recompute command references an existing tool/artifact; exit nonzero
   naming gaps. Wire into verify-claims target.
4. Figure gate extension: add the 3 legacy figures (reliability,
   dose-response, decomposition) to tools/verify_figures.py coverage —
   existence + sha256 pinned in a companion manifest entry with source-
   data hash where the generator is re-runnable, or existence+sha-pin
   with an honest "frozen wave-1 generator, pinned bytes" note where not
   (do NOT resurrect frozen generators); config-hash field for the two
   current-gen figures (their compute_sidecar inputs).

## Files in scope
- Makefile (additive), CLAIMS.json, tools/verify_claims_coverage.py
  (new), tools/test_claims_ledger.py (extend), tools/verify_figures.py +
  its test + sidecar/companion files, README.md/REPRODUCING.md wording
  for the ladder (one short paragraph each) + docs-refresh regenerated
  blocks.

## Read-only / forbidden paths
- verify-public recipe lines (verbatim); analysis/, runs/ artifacts
  (existence-read only), schemas/, scoring/, pipeline/.

## Check command
check: ./.venv/bin/python -m pytest tools -q && make verify-claims

## Acceptance criteria
1. make verify-claims RC=0 and fails when a RESULTS row is missing from
   CLAIMS.json (test proves via tmp copy).
2. verify-public 7 lines verbatim (diff proves); new targets additive.
3. Figure gate covers all 5 referenced figures per the two honesty modes.
4. Full verify-public RC=0 after docs-refresh; diff limited to scope.
