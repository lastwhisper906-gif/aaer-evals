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

## 2026-09-04 — external review C (`.direction/feedback/EXT_FB_C_2026-09-04.md`) vs origin/main dc7e396

> Owner-directed interactive session ("모두 반영해줘"), D-P105 (freeze) /
> D-P106 (execution). Every claim checked against HEAD by direct inspection.
> Branch `review-response/2026-09-04`; local main untouched (INV-17).

| item | reviewer claim | current-main status | evidence | disposition |
|---|---|---|---|---|
| C-1 검정력·일반화 | 12v7 · 8v22 · N=3; AUC CI [0.62, 0.98], 오탐 CI [29%, 96%]; "일반화되는 결론 없음"; 암기 불가 층은 N=3뿐 | **CONFIRMED — already disclosed, not yet stated as one sentence** | RESULTS rows 1–3·5·13 limits; `docs/POWER_ANALYSIS.md` (0.83 vs 0.65 power 0.29–0.32); README "existence-proof record"; 12v7 is the exploratory E2 layer, [0.62, 0.98] is wave-2, [29%, 96%] is the E2 T≥50 cell — three different tiers | README headline + L-13 now say explicitly: memorization is structurally excluded only in the holdout and that layer is N=3; expansion path → **Q-F23** (owner) |
| C-1b "memorization-controlled" 제목 | title claims control | **REFUTED as quoted** — string absent repo-wide; README says "measured, not eliminated" | `grep -ri "memorization-controlled"` = 0 hits; README.md:90 | no title change; L-13 records the caveat for any such reading |
| C-2 Dechow F / Beneish M 부재 | "교과서 비교군이 없다" | **REFUTED as stated, CONFIRMED as a gap** — B1/B2 pre-registered (ANALYSIS_PLAN §5, 5f4ca65), implemented (`scoring/baselines/screens.py`), published (RESULTS row 12, wave-1 only); missing were wave-2/holdout own-separation, same-subset paired comparison, threshold tables, README exposure | RESULTS row 12; `analysis/results_stats.json` baselines block; `analysis/out/wave2_rev2/` (ρ only) | **DONE** — `specs/B1B2_CROSS_TIER.md` (freeze 95cf8cd) → `analysis/b1b2_cross_tier.py` → RESULTS rows 14–15, README, L-13. Readout: 2 cells A, 2 cells B, 0 cells C. Coverage follow-up → **Q-F25** |
| C-2b B4 "식별됨, 미구현" | not implemented | **REFUTED** — implemented and run | `analysis/results_b4.json` (`comparison_established_tiers: []`, coverage wave-1 3/30 · wave-2 4/32), `specs/B4_short_interest.md`, `analysis/B4_REPORT.md` | record only; comparison is live only at a forward seal (Q-M01 PARKED) |
| C-3 단일 모델·동일 계열 채점자 | cross_grader "planned" | **CONFIRMED open** — spec final (4ee5e0b), owner packet + fail-closed skeleton landed, gate Q-F07 PARKED 2026-08-06; evaluatee swap banned by INV-12 §8-6 | `docs/CROSS_GRADER_OWNER_PACKET.md`, `tools/cross_grader_skeleton.py`, L-6 | **Q-F22** (owner: un-park A / scope amendment B / decline C; default A) |
| C-4 잔여 암기 21.9% 제거 못 함 | 1/5 of wave-2 under contamination | **CONFIRMED** — measured, not removed; subsetting cannot remove it | RESULTS row 4; L-1/L-5/L-9 | **DONE (sensitivity + statement)** — name-ID-excluded separation (RESULTS row 15: wave-2 6 vs 19 AUC 0.842, p 0.0024); outcome-knowledge exclusion leaves N=1 → stated as not computable; structural removal only via holdout/forward (Q-F23/Q-F24) |
| C-5 캘리브레이션 없음 | ECE 0.18–0.21, ordinal, no calibration attempt (reviewer concedes N) | **CONFIRMED — pre-registered non-action** | RESULTS row 11; `specs/calibration_scope.md` §2 (recalibration deferred until N ≥ 150, pre-fixed); v2 schema rename `misstatement_risk_score` (D-P46, FREEZE_REV-gated) | no new machinery (spec §2 forbids noise-dominated recalibration); recorded |
| C-6 미결: DOI · cross-grader · atlas §7–9 · B4 · 11월 forward | many open items; forward cycle not run | **CONFIRMED on main** — DOI: path signed (Q-R03/D43), owner account action pending; atlas: all 35 entries drafted through §9, none owner-finalized; forward: gate unsigned, 0 seal artifacts; **but** unmerged `context-diet` D-P104 (2026-08-29) aborted cycle_001 for cycle_002 (300 firms) | `CITATION.cff:13-15`; `atlas/INDEX.md`; `forward/cycle_001/`; context-diet fbf3414 | **Q-F24** (reconcile main vs context-diet; November runbook). DOI/atlas remain owner-manual (no session action possible) |
| C-7 한 줄 평가 (비계 > 결과) | governance maturity ≫ scientific maturity | **ACCEPTED** | — | this response adds one spec, two scripts, one test file, one report, zero new process documents beyond the ledger entries the invariants require |
