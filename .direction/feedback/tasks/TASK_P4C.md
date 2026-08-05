# TASK: P4c — specs/HUMAN_BLIND_REGRADE.md (SPEC ONLY; recruiting = owner)

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration. D-P73 Phase 4 names this file. SPEC ONLY —
  the human recruiting itself is an OWNER action (packet section only).
  Cites: L-6 (intra-family grader bias — the limitation this protocol
  exists to test), EXT_FB_B item 3, DP-Q8. This cycle's doc slot.

## Required content
1. Sampling: random 20-30% of graded cases, seeded deterministic draw
   (formula + seed source), stratified across waves/arms.
2. Blinding: regrader receives mechanism + evidence quotes ONLY —
   company names, arm labels, model scores, wave membership withheld;
   the exact redaction procedure per record field (map to llm_output
   fields), and who runs the redaction (scoring-side, INV-08/09 clean).
3. Instrument: same rubric as grader (cite the frozen rubric artifact),
   response format, no access to answer keys until submission.
4. Analysis: weighted Cohen's kappa (weights defined), agreement matrix,
   FULL disagreement disclosure (every disagreement published with both
   rationales), pre-registered interpretation bands for kappa.
5. Adjudication: disputes resolved by two-human consensus, never by a
   model (EXT_FB_B item 3); "0 overrides" reporting replaced by the
   agreement matrix (the feedback's exact ask).
6. Owner packet section: recruiting criteria (accounting-literate,
   independence requirements), time estimate, compensation note
   (ESTIMATE), exact click-path/checklist to launch once a person is
   found.

## Files in scope
- specs/HUMAN_BLIND_REGRADE.md — create. SPECIFICATION ONLY header +
  INV-14 lines. G2 manual pass footer.

## Check command
check: ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. All 6 sections; deterministic sampling formula; blinding procedure
   field-mapped; kappa bands pre-registered; recruiting strictly owner.
2. Manual G2/INV-13 footer. Diff = the one new file.
