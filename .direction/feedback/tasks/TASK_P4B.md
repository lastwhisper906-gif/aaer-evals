# TASK: P4b — specs/PROSPECTIVE_METRICS.md (SPEC ONLY, zero model calls)

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration. D-P73 Phase 4 names this file. SPEC ONLY.
  Subsumes/extends PKT-Q6's metrics half (D-P44c signed both-design) and
  the DP-Q6 base-rate math — cite both plus specs/POSTCUTOFF_ACCUMULATION
  (D111) and docs/POWER_ANALYSIS (its PR-AUC/PPV out-of-scope note routes
  HERE). This cycle's one-new-doc slot.

## Required content (direction text is the contract)
1. Outcome taxonomy SEPARATED with per-outcome base-rate and lag notes:
   Item 4.02 non-reliance / restatement (Big-R vs little-r) / formal
   investigation disclosure / SEC complaint / AAER — each with observed
   or literature-sourced base-rate (mark ESTIMATE where not derivable
   from committed artifacts) and disclosure-lag characteristics.
2. Metrics, per-outcome and pooled: PR-AUC, PPV, top-1/5/10% precision,
   alerts per 1,000 firms, firms-reviewed-per-true-case; 6/12/24-month
   horizons; deterministic definitions (tie handling, threshold-free
   vs thresholded).
3. Sealed-forward integration: how these feed the forward-cycle design
   (INV-22 boundary — cycle_001 protocol untouched; this specifies the
   metric contract future cycles pre-register), full-universe score
   retention doctrine (D-P44c), threshold freeze discipline.
4. Universe expansion plan for cycle 2: rule-defined screen, size bands,
   E[events] arithmetic per outcome at the chosen sizes (checkable
   arithmetic), INV-23 supervised-fetch preconditions, workload/cost
   arithmetic (cost-per-screen source: BUYER_METRICS owner-input prices,
   cite don't recompute).
5. Small-N honesty: what N each metric needs to be meaningful (cite
   POWER_ANALYSIS machinery where applicable; PR-AUC at tiny positives =
   per-case evidence only).
6. Owner decisions (options/rationale/default, unresolved): outcome
   priority ordering; universe size; horizon emphasis.

## Files in scope
- specs/PROSPECTIVE_METRICS.md — create. SPECIFICATION ONLY header +
  INV-14 lines. G2 manual pass footer.

## Check command
check: ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. All 6 sections; every number sourced-or-ESTIMATE; no call-path code;
   owner decisions unresolved; INV-22 boundary explicit.
2. Manual G2/INV-13 footer. Diff = the one new file.
