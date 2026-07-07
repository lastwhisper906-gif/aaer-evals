# RP-09 Instructions: Grade Finalization on Record + Performance Round

## Philosophy (read once, then act accordingly)
This project exists to produce an honest answer to one question: can an LLM
detect accounting fraud from public financial data? The value is the answer
itself — detection quality, false-positive behavior, temporal earliness,
generalization — whether positive or negative. Nothing is being packaged or
sold. Judge every task by one test: does it make the answer more honest and
sharper?
Process exists only to keep the measurement honest. Exactly THREE invariants:
  I1. BLINDNESS — evaluatee calls receive only case_input schema fields.
  I2. CUTOFF — no data from on/after the revelation date reaches the evaluatee.
  I3. RESULT IMMUTABILITY — produced raw outputs and grades are never edited
      (frozen: runs/main, runs/perturbed, runs/hardening, scoring/grades/,
      scoring/probe_results/, RP-05, finalized RP-06 — and, after Stage 0,
      the finalized grades).
Do NOT generate gate packages, sign-off queues, or ceremony documents. Log
decisions as one JSON line each. Never create owner reading work unless it
changes a result or a launch decision.
Owner touchpoint this round: ONE decision at the end (§Final).
Resumability: commit+push+update HANDOFF.md per stage; stages idempotent;
on restart resume from first incomplete stage. Never block on the owner.
Commit this instruction verbatim to review_packets/RP-09_instructions.md first.

## Stage 0 — Record the Owner's Grade Finalization (do this before anything else)
The owner has finalized the 26 grades via this instruction, INCLUDING accepting
the proposed resolutions on the 5 model-flagged (⚑MODEL) items and the MRVL
DATA(design) PROPOSAL ruling as proposed. Actions:
  - Update all grade statuses from proposed/pending to FINAL in one commit,
    referencing this instruction's commit hash as the authorization.
  - One JSON decision-log line recording: date, scope (26 grades incl. 5
    ⚑MODEL + MRVL), basis (owner instruction RP-09).
  - From this commit forward, scoring/grades/ contents are frozen under I3.
  - If ANY grade item lacks a concrete proposed resolution to accept (i.e.,
    finalization would require inventing a judgment), do NOT invent it — leave
    that item unfinalized, and surface it as the only open item in §Final.
The treatment-side answer-key evaluation is hereby closed.

## Stage 1 — Deferred Robustness Experiment: Closure
Context: in the k=5 re-draw robustness check, draw 3 was the single draw where
treatment-vs-control median separation fell to 9.0pp, below the pre-registered
10pp threshold. Whether that is sampling noise or real fragility is unresolved;
the bottleneck is k=1 on the original (unperturbed) side.
  - Check whether RP-07's D-2 (original-side re-draw, 32 evaluatee calls) was
    executed (look for runs/rp07/ artifacts). Report the finding explicitly.
  - If unrun, run it now: commit RNG seeds before any call; identical evaluatee
    model pin, payload schema, I1–I2 conditions; discard and report any pin
    mismatches; RP-06-format call accounting (assert API-key absence).
  - Deliver the completed delta decomposition: per-case outside/inside-noise
    for all 8 treatment cases; a plain-language verdict on the draw-3 event
    (noise vs. real fragility); whether the Monsanto interpretation holds
    (the one company unrecognized in both identity probes moved −30 under
    perturbation → unrecognized cases score analytically, from the numbers).
  One page, liftable into any future write-up.

## Stage 2 — Control Group v2 (bigger and better-matched, one shot)
A control's scientific role: as similar as possible to its treatment case in
everything EXCEPT fraud, so discrimination can only come from fraud signal.
Amend criteria to CONTROL_CRITERIA_v2 in a single commit bundling:
  (i)  order-bug fix: supplementary-SIC expansion runs BEFORE the size-band
       filter, restoring wrongly-absent candidates (Garmin, Forrester,
       General Mills) to the eligible pool by rule;
  (ii) 2–3 matched controls PER treatment case, target 16–24 total, with an
       explicit match-quality ordering (size distance → industry proximity →
       era overlap) so selection stays a pure function of criteria + pool;
  (iii) the Steven Madden ambiguity fix as a criteria-level rule (e.g., ticker
       requirement or the Accuray swap logic — a rule, not a hand edit).
Re-run selection (pure function, no network). Output:
runs/rp09/control_group_v2.json.
Documentation: ONE table (company | matched treatment case | size distance |
industry note | one-line reason), a short group-level coverage paragraph, and
the 3 picks most worth a human glance. Discretionary calls → JSON lines only.
Emit the final company list as a paste-ready block for an external
AAER/enforcement web screen (owner runs it in claude.ai) — the one cheap check
protecting the false-positive measurement from hidden frauds in the controls.

## Stage 3 — Scoring-Ready Package (prepare so launch is one command; do NOT launch)
3a. Runbook: a single command scoring all v2 controls under the frozen protocol
    (evaluatee pin, payload schema, I1–I2, seed step included).
3b. Recognition probes on controls: extend the treatment-side identity probe
    ("can you tell which company this is?") to every control company, bundled
    into the same runbook. Write the analysis plan FIRST (one page): the
    recognized-fraud(high score) vs. recognized-clean(low score) comparison
    directly tests whether memorized identity inflates scores — state in
    advance what pattern supports/refutes inflation.
3c. Power pre-computation: for 8 treatment vs. 16–24 controls, what
    separations / AUC / false-positive-rate differences are resolvable at the
    pre-registered thresholds, and whether a 9.0pp-style event falls inside or
    outside design resolution. Half a page of numbers, committed before any
    control scores exist.
3d. Parallelization: verify evaluatee calls run concurrently; if sequential,
    fix at builder level with tests. Report expected wall-clock for the full
    control run (scoring + probes).

## Stage 4 — Temporal Signature Design (how early does the signal appear?)
Design — do not run — the measurement answering the temporal question: does
fraud signal appear only near public revelation, or accumulate quarters/years
earlier? Real knowledge about how fraud's financial footprint grows.
Per treatment case, the design scores the SAME company at multiple historical
snapshots (filings at 1, 2, 3… periods before revelation), yielding a
score-over-time trajectory. Deliverables: per-case snapshot feasibility (which
filings exist in XBRL at each lookback), trajectory spec (per-snapshot payload
under I1–I2, each snapshot's cutoff = that snapshot's own date), call-count
estimate, and a mock of the core finding chart (score vs. periods-before-
revelation, treatment trajectories against control baselines).
File: docs/EARLINESS_DESIGN.md. Flag infeasible cases now, while it's cheap.

## Stage 5 — Post-Cutoff Holdout Recon (lightweight)
Candidate list ONLY: AAERs with public revelation dates after the evaluatee
model's training cutoff — company, AAER number, revelation date, fraud-type
one-liner, XBRL feasibility guess. docs/FUTURE_HOLDOUT_CANDIDATES.md.
This is the future test where memorization is structurally impossible — the
cleanest version of the question. No packaging, no scoring.

## Stage 6 — Incremental Audit (minimal)
Record last-audited commit in docs/AUDIT_STATE.md; audit only the diff since
the previous round's final commit, against I1–I3 and test health. Do not
re-audit the whole repository.

## Final Report — built for ONE owner decision
Four-sentence Korean summary, then exactly one decision:
  "Approve control_group_v2 and launch scoring: YES / AMEND".
Support: Stage 0 confirmation (grades FINAL, or the single unfinalizable item
if any); the Stage 1 verdict (lead with it); the Stage 2 table + 3 picks worth
a glance + web-screen paste block; power numbers; expected wall-clock and call
budget for the control run; I3 immutability proof (empty git diff over frozen
paths). Everything else lives in the repo, not the report.
Evaluatee-call budget this run: Stage 1's 32 (if unrun) — nothing else
launches before the owner's YES. Push all, report the commit range.
