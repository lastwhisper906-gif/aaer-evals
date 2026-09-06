# TASK: P4a — specs/PERTURBATION_V2.md (SPEC ONLY, zero model calls)

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- Branch audit-integration. D-P73 Phase 4 names this file. SPEC ONLY.
  Subsumes PKT-Q9 (owner-signed direction D-P44/D-P50 lineage) — cite it.
  This cycle's one-new-doc slot.

## Required content (direction text is the contract)
1. Symmetric 2x2 design: treatment/control × original/perturbed — closing
   the J14 asymmetry (cite R2-01/PKT-R2 and DECISION_TABLE's asymmetry
   limit; J14's original no-new-grading rationale and what supersedes it
   for future waves).
2. Paired per-case deltas: mean, sd, original−perturbed distributions;
   the estimators defined deterministically.
3. TWO SEPARATE ARMS: identity-removal arm vs chronology-preserving arm —
   the date-shift interaction with CL7 (filing-chronology checklist item)
   documented explicitly (v2ds precedent: date_shift.py, Q-F05).
4. Perturbation mechanics requirements: accession pseudonymization
   (not removal-only — stable fake ids), relative date shift, fiscal-
   period stability (rescale must preserve period alignment); signal-
   preservation validation plan (deterministic detectors invariant
   pre/post — Beneish/Dechow recompute on perturbed values).
5. Execution preconditions checklist (owner signature activates): which
   frozen probes re-run, cost arithmetic (ESTIMATE-marked), INV-21 pin
   gate, output paths (new separated runs/ dirs + manifests per P1a).
6. Honesty: what v2 does NOT fix (residual deep channels; L-5/L-9
   citations); relation to the frozen v1 partial-de-identification note.

## Files in scope
- specs/PERTURBATION_V2.md — create. SPECIFICATION ONLY header + INV-14
  lines. Vocabulary: G2 manual pass (lint doesn't scan specs/).

## Check command
check: ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. All 6 sections; every number sourced-or-ESTIMATE; no call-path code;
   owner-decision items in options/rationale/default form unresolved.
2. Manual G2/INV-13 pass recorded in a footer comment.
3. Diff = the one new file.
