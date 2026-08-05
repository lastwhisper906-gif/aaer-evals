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

## Edit 3 (R3-04, folded per its disposition) — analysis/error_analysis_wave2_holdout.md:
prepend ONE dated-snapshot blockquote ABOVE the H1 (position preserves the
ko token-equivalence lock, same mechanism as the existing pointer):
"> Snapshot of 2026-07-08 (OWNER-GATE-E session). Two assertions are
SUPERSEDED by later signed work and preserved unchanged per
disclose-don't-revise: human_finalized=false (superseded by GA-001(b)
progress — see AUDIT_INDEX) and 'E1 not run' (superseded by the E1
matched-controls run, RESULTS row 6)."

## Edits 4-8 (R6 round — published sentences asserting unsupported certainty; full evidence replenish_R6_2026-08-05.md):
4. README:~59 + METHOD holdout framing: "structurally impossible
   memorization" → "where the revelation postdates the evaluatee's
   *declared* training cutoff AND measured non-recognition was
   demonstrated (k=5 gate, positive controls)".
5. RESULTS rows 8/9/10 limits, append: "; two known selection effects
   with opposite signs — undetected fraud in controls (specificity ↓) vs
   hindsight no-restatement certification (E5 window cutoff+3y,
   specificity ↑); net direction unknown".
6. RESULTS rows 1/3/13 limits, append: "; treatment rosters were
   pre-screened for in-principle public-data detectability (A-type rule)
   — rates are conditional on that screen".
7. RESULTS row 4 limits, append: "; endpoint 0% is 0/3 (CP95 [0%,
   70.8%]); the perturbation gradient shares the frame confound published
   in README_DETAIL".
8. Frozen ISSUE notices (D99 post-publication-notice channel, owner
   posts): generalize ISSUE_2's HUBG boundary caveat; define "A-type" in
   ISSUE_1; FPR sign note for ISSUE_0.
Also OPTIONAL edit 9: one README "Want to check our work?" line linking
the committed adversarial premise-verification record
(.direction/feedback/replenish_R6_2026-08-05.md — 7 premises held, one by
independent recomputation).
CLAIMS.json syncs with every RESULTS edit (char-lock).

## Why signature: RESULTS.md is the owner-signed publication surface;
additive-honesty edits still change signed text. Both amendments mirror
limits the repo already states elsewhere (DECISION_TABLE.md:37-38;
calibration criterion analysis/calibration.py:57 scope).
## Exact commands after signature:
  # orchestrator or owner applies the two appends + CLAIMS.json sync,
  # runs: .venv/bin/python -m pytest tools/test_claims_ledger.py -q
  #       && make verify-public
