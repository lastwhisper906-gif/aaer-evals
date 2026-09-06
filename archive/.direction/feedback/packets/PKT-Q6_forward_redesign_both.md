# PKT-Q6 — forward-cycle redesign: expanded universe + pre-registered intermediate labels
**Owner decision: SIGNED (D-P44c, 2026-08-05) — BOTH: rule-defined
universe expansion AND intermediate labels (Item 4.02 non-reliance,
restatement) as primary outcomes; AAER as slow confirmatory label.**
Status: ready-to-execute packet. Nov 2026 seal-window clock.

## Base-rate math (stdlib-checkable, cite in the design doc)
- AAER incidence ~1-2%/yr → 12-firm universe ≈ 0.12-0.24 expected
  events/cycle → a sealed cycle with 0 treatment events cannot validate.
- 4.02 non-reliance 8-Ks run ~150-300/yr across US listings; restatements
  (Big-R + little-r) several ×100/yr → a 300-500 firm universe yields
  E[events] in the single-to-low-double digits per 12-24mo window.
- Existing precedent: holdout labels are ALREADY provisional Big-R
  (RESULTS row 5) — the redefinition makes the de-facto label honest.

## Design deltas (docs to draft in the build cycle; all pre-seal)
1. docs/FUTURE_CYCLE_PROTOCOL.md amendment (protected — owner-signed
   commit): universe rule (e.g. all US non-financial listings above
   liquidity floor, mechanical screen, frozen monthly), primary outcome =
   4.02/restatement within window, confirmatory = AAER/complaint;
   threshold frozen pre-seal; full-universe score retention (no post-hoc
   control selection).
2. OWNER_LAUNCH_GATE v2 checklist: seal = payload+score+prompt hashes,
   public timestamp; abort discipline unchanged (INV-22).
3. Workload note: scoring N hundred firms × cost 0.53 USD/screen (BUYER
   METRICS) — quota/schedule table for the November window.
## Exact commands
  ~/tools/harness/run_task.sh --task .direction/feedback/tasks/TASK_Q6_memo.md \
    --workdir ~/repos/aaer-evals-work   # drafts the design memo + math annex
