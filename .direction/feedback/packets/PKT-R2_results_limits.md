# PKT-R2 — RESULTS.md limits-column amendments (OWNER SIGNATURE REQUIRED — INV-18)

Two sentence-level additions to the published claims table's limits column
(the surface RESULTS.md's own header makes load-bearing). No number
changes. CLAIMS.json syncs in the same commit (char-level lock,
tools/test_claims_ledger.py). Full evidence:
.direction/feedback/replenish_R2_2026-08-05.md (R2-01, R2-02).

## Edit 1 — Row 2 (wave-1 perturbed frame), append to limits cell:
"; frame is asymmetric — controls were never perturbed (J14
no-new-grading contract): perturbation-induced score shifts are not
separable from identity-removal effects (same limit DECISION_TABLE
carries for this frame)"

## Edit 2 — Row 11 (Calibration), append to limits cell:
"; ECE is computed at the case-control design prevalence (~27-28%) — it
measures in-sample departure only and is not an estimate of deployment
calibration error"

## Why signature: RESULTS.md is the owner-signed publication surface;
additive-honesty edits still change signed text. Both amendments mirror
limits the repo already states elsewhere (DECISION_TABLE.md:37-38;
calibration criterion analysis/calibration.py:57 scope).
## Exact commands after signature:
  # orchestrator or owner applies the two appends + CLAIMS.json sync,
  # runs: .venv/bin/python -m pytest tools/test_claims_ledger.py -q
  #       && make verify-public
