# FEEDBACK_TRIAGE.md — 2026-08 external audit feedback vs current HEAD

> Direction: "External Audit Feedback Integration" (owner-approved verbally,
> D-P73). Every item verified against HEAD (98012f9 lineage) by direct
> inspection — nothing assumed from memory. This file is this sprint's one
> permitted new document (audit/ protected path — created under the
> direction's explicit naming, disclosed in D-P73).
> PRECONDITION STANDING: **E-003 unsigned** (ERRATA has no E-003; synthesis
> artifacts unregenerated) — phases touching published numbers BUILD ON
> BRANCH, merge after signature+push.

| item | reviewer claim | current-main status | evidence | disposition |
|---|---|---|---|---|
| P0-1 result-selection nondeterminism | analyzers select score files by directory glob; unregistered/duplicate/missing files undetectable | **CONFIRMED open** | 12+ glob selections: analysis/baselines.py:26,29,35 · decision_table.py:101 (wave-2 case list FROM glob) · name_probes.py:28 · name_probes_v2ds.py:38,56 · buyer_metrics_build.py:72 · b3_compute.py:65 · label_tags_holdout.py:33 · scoring/analyze_rp05.py:28,110 | **Phase 1** (manifests + fail-closed + no-glob) |
| P0-2 grader fingerprints missing | grading records carry no fingerprint; skip = schema-valid-only | **CONFIRMED open** | scoring/grader_runner.py:11 ("파일 존재+스키마 통과 = skip"), :110 _existing_grade_valid | **Phase 1** (grader fingerprint + fp-match skip) |
| P0-3 probability framing | prompt/schema demand probability | **PARTIALLY resolved** | schemas/llm_output_v2.json exists (risk_score rename, D-P46) but is rename-only by design; adoption unwired (FREEZE_REV-gated) | **Phase 2** executes the signed plan |
| P0-4 schema laxity | checklist minItems 1, no CL enum etc. | **PARTIALLY** | v1 frozen (correct); v2 lacks the hard constraints (NB-01 scoped rename-only; structural-diff lock will need a v2.1 contract update) | **Phase 2** |
| P1-4 verify-* split | verify-public overpromises; split targets | **PARTIALLY** | R5/D-P68 honest-scope wording + sandboxed variant landed; `verify-claims`/`verify-fixture-pipeline` targets absent (Makefile:0 hits) | **Phase 3** (aliases keep verify-public) |
| P1-5 CLAIMS.json as gate driver | machine map + verify iterates it | **PARTIALLY** | CLAIMS.json exists, drift-locked (D-P41); columns lack recompute_command/limitation-ref; no gate iterates it | **Phase 3** |
| figure gate | cover every referenced figure + data/config hash | **PARTIALLY** | tools/verify_figures.py (D-P52) covers 2 current-gen figures w/ data-hash sidecars; 3 legacy referenced figures excluded (semantic reasons recorded); config hash absent | **Phase 3** extend |
| grader/result lineage gates missing (gate-SYSTEM attack) | the gate set lacks whole gate types | **CONFIRMED** (P0-1/2 are the proof) | this class was invisible to R1-R6 lenses — lens read code for defects, not the gate system for missing gate types | **Harness self-improvement** (new lens) + Phase 1 |
| threat_model.md says "Anthropic SDK direct calls" | stale doc claim | **REFUTED — stale** | no docs/threat_model.md exists on HEAD; repo-wide grep "Anthropic SDK" = 0 hits; the threat model lives in METHOD.md §3 and correctly describes `claude -p` isolation | record refutation only |
| candidates "PENDING HUMAN SIGN-OFF" contradiction | metadata says pending while finalized elsewhere | **CONFIRMED open** | data/candidates/candidates.json:3 + COLLECTION_NOTES.md:3 + reverification_diff.md:3 still say PENDING; roster freeze signed later (D-ledger) | **Phase 6** (dated supersession headers; data/ protected → packet if needed) |
| multiple-testing paragraph | absent | **CONFIRMED absent** | grep RESULTS/METHOD family-wise/다중 검정 = 0 | **Phase 6** |
| README November section | absent | **CONFIRMED absent** | grep November/11월 README = 0 | **Phase 6** |
| BN-07/11/12/13/14/16/18, README rewrite, figure relabel | (prior-session fixes) | **VERIFIED RESOLVED on HEAD** | BOTTLENECKS.md flip entries D-P52..P58; README rewrite e05db78+R3 repairs d91e852; fig relabel 68099ae — all with gate-green commits | no action |
| result-selection divergence audit | recompute all published numbers post-manifest | open (depends on Phase 1) | — | **Phase 1 step 4** — INV-03 path; unchanged-numbers is itself a recorded finding |

## Carry-overs from D-P50 loop (Phase 6 intake)
- R1-04 (deferred figure-PNG hash tie) — now SUBSUMED by Phase 3 figure-gate
  extension. R4-06 (translation lock vs future erratum) — becomes live the
  moment E-003 is signed (the erratum will append EN-only; the ERRATA pair
  lock already handles EN-only appends — verify at signature time). C1B
  forward trio = PKT-FWD (owner). PKT queue unchanged.
