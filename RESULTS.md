# RESULTS.md — Single table of published numbers (row-level limits alongside)

> Authored by Claude Code, pending human audit (GA-001 (b)). Zero new claims —
> every row links a frozen-artifact path. Existence-proof framing: these are
> not performance estimates. Re-verify: `make verify-public`. Task tags and the
> no-pooling discipline are in the "Three tasks" section of
> [docs/README_DETAIL.md](docs/README_DETAIL.md) (D106 ④).
> Identifier glossary (D/Q/RP/R3/R4/E5/L4/CP95 and friends):
> [AUDIT_INDEX.md](AUDIT_INDEX.md).
> Grading: Claude-assisted, human-finalized. All results are scoped to a
> single Claude-based pipeline.
> Korean original: [RESULTS.ko.md](RESULTS.ko.md).
> Multiple-testing classification and Holm adjustment: [docs/MULTIPLE_TESTING.md](docs/MULTIPLE_TESTING.md).

| # | [Task] Measurement | Published number | Limits of this row (misread if not read together) | Source |
|---|---|---|---|---|
| 1 | [T1] wave-1 identity–exposure separation (treatment 8 vs control 22) | permutation p 0.00114 · mean diff +19.8pp · AUC 0.824 [0.599, 0.983] | Upper bound entangled with memorization — R3 triggered (5 of 8 over threshold), name-ID 50%. N=30 small sample, wide CI | `analysis/results_stats.json` |
| 2 | [T1] wave-1 perturbed frame (primary reading) | permutation p 0.0021 · AUC 0.864 [0.722, 0.969] · flags 4/8 | A *less-contaminated* measurement, not a clean lower bound — residual identity recognition after perturbation 5–6/8; the v1 frame is partially de-anonymized (accession numbers and filing chronology retained) | `analysis/results_stats.json` · `docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md` |
| 3 | [T1] wave-2 separation (treatment 9 vs control 23) | permutation p 0.00116 · mean diff +20.6pp · AUC 0.829 [0.616, 0.983] · flags 7/9 | R4 framing constraint (no accuracy/AUC comparison claims). Under direct probing, outcome knowledge is available for 8/9 (88.9%, CP [51.7%, 99.7%]) | `analysis/wave2_results.json` (rev2 parallel path: `analysis/out/wave2_rev2/`, ERRATA E-002) |
| 4 | [T1] name-ID axis | 50% (15/30) → 21.9% (7/32) → 0% | 21.9% is the frozen-rule value — a rename-aware human reading of 25% (borderline case DAR) is footnoted alongside (Q-E02) | `analysis/name_probe_results.json` · `analysis/synthesis.json` |
| 5 | [T2] post-cutoff holdout per-case scores | HUBG 70 · GNE 42 · WMK 32 (0–100 ordinal) | N=3, per-case only — H1 (permutation significance) not claimed. Labels are provisional Big-R (4.02 unreliable), not confirmed enforcement. The HUBG hit is a tier hit with the mechanism missed (anchored on the 2018 restatement cluster) | `runs/holdout/` · `analysis/label_tags_holdout.json` |
| 6 | [T2] E1 matched controls | HUBG 70 > all matched controls (RXO 42 · BCO 30 · XPO 20); separation in only 1 of 3 cases | Exact permutation p=0.20 is CONTEXT ONLY. The single highest score in the holdout tier is a control false positive (GRDX 78) — HUBG does not exceed the pooled control set | `analysis/holdout_controls_results.json` |
| 7 | [T2] holdout draw robustness (k=5) | HUBG ≥50 in 5/5 draws [58–76]; WMK [28–42] · GNE [30–42] 0/5 | The published number is draw-1 — the bands are companion statistics | `runs/holdout/mainscore_redraw/` (E5 §7) |
| 8 | [T1] FPR wave-1 | 3/22 = 13.6% CP95 [2.9%, 34.9%] | Controls are "non-enforcement," not "clean" — the bias direction pushes specificity downward (survivorship and selection bias; README Limitations) | `analysis/results_stats.json` |
| 9 | [T1] FPR wave-2 | 5/23 = 21.7% CP95 [7.5%, 43.7%] | Same as above; additionally, the 5 false positives are not hallucinations but positive misreadings of real figures (grounded; top of dim4) | `analysis/wave2_results.json` · `analysis/error_analysis_wave2_holdout.md` |
| 10 | [T2] FPR holdout controls | 2/9 = 22.2% CP95 [2.8%, 60.0%] | No silent pooling of FPR across tiers — CP intervals overlap heavily; worse-but-not-provably | `analysis/holdout_controls_results.json` |
| 11 | [T1] Calibration | ECE wave-2 0.179 (wave-1 0.209) | **Scores are ordinal (0–100 ranks), not probabilities** — no calibration improvement (null-ish); recalibration at N≈30–60 is noise-dominated (`specs/calibration_scope.md`) | `analysis/calibration_wave2.json` |
| 12 | [T1] Mechanical baseline comparison | Beneish M p 0.498/AUC 0.510 · Dechow F p 0.268/AUC 0.573 · LLM rank correlation w1 −0.075/−0.144 · w2 0.333/0.293 (rev2 tie-aware) | Same 30 companies, same PIT window only. The v1 w2 correlation values 0.337/0.265 came from an implementation that did not average ties — both values are far from the R2 threshold of 0.7, with no effect on the verdict (E-002) | `analysis/baseline_table.csv` · `ERRATA.md` E-002 |
| 13 | [Exploratory L4] E2 trajectory single threshold | T≥50: detection 12/12 CP [73.5%, 100%] · **false positives 5/7 = 71.4%** CP [29.0%, 96.3%] | **No dominant strategy for a standalone LLM threshold at the trajectory layer** — sensitive thresholds travel with false positives, and a false-positive-controlling threshold (T=70) kills detection first (1/12). The EXPLORATORY combined rule (B3≥2 AND llm_p≥T) has 0/7 false positives but is a post-hoc rule — registered only as a Cycle-2 sealed candidate | `analysis/DECISION_TABLE.md` §4 (signed D94) |

No prose wall — the narrative context for each row lives in the README
headline section and the published issues (linked from the README Publication
section). When citing any number from this table, cite that row's limits
column with it.
