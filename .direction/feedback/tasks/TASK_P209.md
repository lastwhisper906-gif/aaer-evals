# TASK: P2-09 — specs/OBSERVATORY_PILOT_V0.md (SPECIFICATION ONLY, zero model calls)

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- D-P50 Phase 2 #9 signed scope. specs/ is protected — this task is the
  sprint's ONE new top-level document (governance diet), created under
  the direction's signature; the post-review verifies it is the only one.
- HARD CONSTRAINT: no call-path code, no schema wiring, no model calls.
  INV-12/INV-20 revisions appear ONLY as owner-decision entries inside
  the spec (options/rationale/default format).

## Objective

Author specs/OBSERVATORY_PILOT_V0.md: a cross-sectional "observatory"
design measuring how LLM judgment on the same frozen cases shifts across
2-3 models with different training cutoffs. Success condition (D-P50):
"documents in a state where the owner's signature alone makes them
executable."

## Required content (all sections; every number recomputable from
committed artifacts or explicitly marked ESTIMATE)

1. Question & claim: what a judgment-delta across training cutoffs would
   demonstrate (memorization dose-response at the MODEL level — the
   cross-sectional complement of the within-model perturbation axis,
   RESULTS row 4 / L-5).
2. Target cases: the 3 post-cutoff holdout cases (HUBG/GNE/WMK, events
   2026-02/03) + a DETERMINISTICALLY ENUMERATED wave subset (exact case
   list or a mechanical selection rule — the owner signs a fixed call
   count, not a placeholder); a case × model-cutoff table of expected
   knowledge status citing each case's dates from the committed registry
   AND each candidate model's DOCUMENTED training cutoff. FEASIBILITY
   HONESTY: all wave events are 2010-2019 (knows-era for every candidate)
   and all holdout events are 2026-02/03 (after claude-sonnet-5's 2026-01
   cutoff and likely after every currently subscribable candidate's) —
   the off-diagonal contrast cells may be EMPTY today.
3. Reused probes, frozen versions AS-IS, with the CORRECT citations:
   name-ID/recognition + verbatim probes = pipeline/probe_runner.py with
   the frozen verdict rule scoring/probe_verdict.py:name_match;
   outcome-recognition (knows_event) = tools/holdout_probe.py (gate rule
   per HOLDOUT_CONTROLS_PLAN §2); perturbation delta = the committed
   runs/ arms (L-5). No new probe design.
4. Judgment-delta measurement — PER-TIER MATRIX (not one formula):
   wave cases (both arms committed: runs/perturbed/, runs/wave2/perturbed/)
   → perturbation delta (score_original − score_perturbed) + name-ID;
   holdout cases → score + knows_event recognition status ONLY, with one
   sentence stating why no perturbed arm exists (identity-visible PRIMARY
   by design — post-cutoff memorization already impossible;
   HOLDOUT_CRITERIA (f)). NO new probe arms. Cross-model contrasts defined
   per tier with deterministic formulas.
5. Go/no-go criteria, pre-registered BEFORE any run: (i) CONTRAST-CELL
   FEASIBILITY GATE: if no roster option yields at least one
   knows/cannot-know off-diagonal cell, the cross-sectional contrast is
   NO-GO and the pilot is EXPLICITLY REFRAMED as the baseline leg of a
   LONGITUDINAL observatory — measure the all-cannot-know baseline now;
   the contrast arrives when a future model's training cutoff crosses
   2026-03 (consistent with specs/POSTCUTOFF_ACCUMULATION.md accumulation
   arithmetic). Signing a spec that measures nothing would be worse than
   signing a deferral — the spec must make the owner sign the reframe
   knowingly. (ii) Minimum effect sizes with arithmetic for the GO case;
   small-N honesty limit explicit (per-case evidence only, no
   significance claims; cite docs/POWER_ANALYSIS.md where applicable).
6. Candidate model roster as OWNER DECISIONS (options/rationale/default,
   NEVER resolved here): each candidate with vehicle and invariant
   status — e.g. (a) claude-sonnet-5 (already pinned, INV-21-compliant,
   zero new decisions), (b) another Claude family model via subscription
   CLI (INV-21 pin revision needed — FREEZE_REV entry draft), (c) GPT via
   subscription Codex (D-P48 exception already in force; runner exists:
   pipeline/crossmodel_gpt.py, tranche parked D-P49). Gemini: excluded
   (no subscription path, INV-20 — state it).
7. Expected call count and cost: exact call arithmetic (cases × arms ×
   probes × models), subscription-pool framing (zero-metered), wall-time
   estimate marked ESTIMATE.
8. Execution preconditions checklist: what the owner's signature
   activates, in order (FREEZE_REV entries, launch gate, output paths —
   new separated runs/ subdirs per D-P48 pattern), each as a checkbox
   with the exact command or file to sign.
9. Relationship to the sealed forward cycle (INV-22): the observatory is
   retrospective-frozen-case work; state explicitly it does not touch
   forward/cycle_XXX or the Nov window.

## Files in scope
- specs/OBSERVATORY_PILOT_V0.md — create. Header: "SPECIFICATION ONLY —
  no call-path code; execution requires owner signature per §8" +
  the repo-standard INV-14 scope/disclaimer lines.

## Read-only / forbidden paths
- Everything else. Especially: pipeline/, schemas/, Makefile, runs/,
  forward/, BOTTLENECKS.md, PROJECT_INVARIANTS.md.

## Check command
check: ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. All 9 sections present; every number either recomputable (cite source)
   or marked ESTIMATE; owner decisions in options/rationale/default form
   and none resolved.
2. Zero call-path code anywhere; the file self-declares SPECIFICATION
   ONLY (same convention as specs/cross_grader.md).
3. lint_publication RC=0 (near-vacuous for the new file — specs/ is not
   a lint scan surface); THEREFORE explicit criterion: the file names
   HUBG/WMK/GNE only in restatement/non-reliance framing per the registry
   _meta.labels and contains NONE of the FRAUD_WORDS applied to those
   companies (INV-13) — reviewer verifies manually since no lint covers
   specs/.
4. Diff = the one new file.

## Notes
- MERGE PROTOCOL (orchestrator): docs-refresh not needed (no test-count
  change) — verify; D-entry MUST carry the disclosure line per
  D-P57/D-P59 pattern: "보호 경로 공개: specs/OBSERVATORY_PILOT_V0.md
  (.protected-paths) — D-P50 Phase 2 #9 서명 스코프"; this is the
  governance-diet document slot.
