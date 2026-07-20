# Practitioner Brief — An LLM Accounting-Quality Screen, Backtested Against SEC Enforcement

> **DRAFT — pending owner finalization of atlas/PATTERNS.md and CPA judgment
> sections. Not for external distribution.**
>
> Authored by Claude Code, pending human audit (D15). No positions ·
> educational/informational only · not investment advice. 본 결과는 Claude 기반
> 단일 파이프라인에 한정된다 (PROJECT.md §5-5) — results are scoped to a single
> Claude-based pipeline and do not generalize to LLMs at large.
> 채점: Claude 보조 + 인간 최종 확정 (grading: Claude-assisted, human-finalized).
>
> Audience: forensic accountants, internal auditors, buy-side analysts.
> Every number in this brief traces to a frozen repository artifact (Appendix)
> and is recomputed by `tools/reproduce_analysis.py`. No new numbers appear here.

---

## Page 1 — The problem

Independent signals on public-company accounting quality are structurally
scarce. The auditor is selected and paid by the auditee. Sell-side coverage
sits inside banks with current or prospective underwriting relationships with
the covered issuer. Credit rating agencies are issuer-paid. Each of these
parties produces opinions about financial-statement reliability, and each has
an economic relationship with the company whose statements are being judged.
The practitioner who wants a conflict-free second opinion on accounting
quality — before a restatement, not after — has few instruments.

The existing conflict-free instruments are mechanical screens: Beneish M-score,
Dechow F-score, and their descendants. They are cheap and reproducible, but
their failure modes are documented and familiar to anyone who has run them at
scale: they require a specific set of financial-statement inputs and simply
cannot be computed when an issuer's filings or tagging do not supply them; they
are static formulas that a determined preparer can manage to; and they read
only the ratios in the formula, not the filing behavior, disclosure chronology,
or account-level texture around them. This repository backtests one candidate
addition to the toolkit — an LLM reading point-in-time structured disclosure
data under a frozen protocol — against SEC enforcement (AAER) cases, matched
non-enforcement controls, and a post-training-cutoff holdout.

## Page 2 — The system

```
  SEC filings (point-in-time,        deterministic Python metrics
  cutoff-guarded: no document   -->  (ratios, trends, chronology;
  after each case's cutoff date)     seeded, no wall-clock logic)
              |                                   |
              v                                   v
  LLM evidence extraction: frozen checklist prompt, structured
  JSON schema, MANDATORY verbatim citation of source figures
  and accession numbers (documents_used required)
              |
              v
  structured scoring rubric (frozen before any score existed)
  applied by a grader model  -->  HUMAN CPA FINAL SIGN-OFF
                                  (all published grades human_finalized=true)
```

**Point-in-time filings.** Every case has a cutoff date (the day before first
public revelation). All data loading passes through a cutoff guard
(`pipeline/cutoff_guard.py`); no document filed after the cutoff enters the
input. This blocks look-ahead through documents — it cannot block what the
model already knows internally, which is why the contamination program on
Page 3 exists.

**Deterministic metrics.** All quantitative computation is seeded, deterministic
Python — the LLM never does arithmetic that matters. Beneish M and Dechow F are
computed on the same inputs as mechanical baselines.

**LLM evidence extraction.** The evaluatee model (pinned `claude-sonnet-5`)
answers a frozen checklist against the deck and must cite verbatim figures and
the accession numbers of the documents used. Output is schema-validated JSON;
open-ended prompting is prohibited. The output is an ordinal 0–100 score plus
ranked, evidence-cited hypotheses.

**Structured rubric, then human sign-off.** A grader model applies a frozen
rubric; every published grade then carries `human_finalized=true` under owner
sign-off (0 overrides recorded, rubber-stamp check confirmed). Nothing in this
repository is published on model authority alone.

## Page 3 — The evidence discipline (what would falsify this)

The design assumes the reader's first objection: *the model has read about
these cases in training.* The controls below bound that risk; they do not
eliminate it, and the repository says so on its front page.

**Freeze before run.** Scoring criteria, thresholds, and the machine conclusion
rules (R1–R4 / H1–H3) were committed before any score existed — the
pre-registration is git-commit-timestamped (experiment plans at commit
`c1b85a7`). A result that required post-hoc rule changes would be visible in
the git history; none was made.

**Contamination is measured, not assumed away.** On the direct
outcome-knowledge probe, the model recalls the enforcement/restatement event
for **8 of 9 wave-2 treatment cases (88.9%, CP95 [51.7%, 99.7%]) vs 0/23
controls** — stated plainly: the wave-2 identity-exposed frame operated with
outcome knowledge broadly available, and every TASK 1 result is a reading under
disclosed residual contamination (L-1/L-5). On the name-identification probe,
anonymized-payload identification runs **50% in wave-1** and **21.9% in
wave-2**. A post-publication notice additionally discloses that the v1
perturbed frame was only **partially de-identified** (original accession
numbers and real filing chronology retained).

**Blind scoring, post-cutoff holdout.** Treatment and control cases run under
one protocol, and the structural answer to memorization is TASK 2: three
companies whose restatement events post-date the model's training cutoff. The
pre-committed recognition gate reads **knows_event 0/5 per case** across five
probe draws (positive control HTZ re-verified True) — for these events,
memorization is structurally impossible, not merely improbable.

**Sealing, forward.** The next step is prospective: a 12-company forward
watchlist is scheduled to be scored and cryptographically sealed on
**2026-11-15** (GitHub server timestamp + OpenTimestamps anchor), before any
outcome exists to memorize (`specs/FORWARD_WATCHLIST_V1.md`).

**One-command reproduction.** `python tools/reproduce_analysis.py` recomputes
every published number from committed artifacts, 0 API calls — **100/100
checks** — alongside `tools/verify_blindness.py` and `tools/verify_manifest.py`.
CI runs all of it on every push. A reader who distrusts any figure in this
brief can recompute it in minutes.

## Page 4 — What it found

The three strongest results, each with its task tier and frozen interval:

- **[TASK 1] Wave-1, perturbed (identity-masked) frame** (8 AAER treatments vs
  22 controls): separation permutation p = **0.0021**, AUC **0.864
  [0.722, 0.969]**, 4/8 treatments flagged at the pre-registered score ≥50 cut.
  Caveat L-5: perturbation scatters memorized numbers but does not remove
  identity recognition — this is the *less-contaminated* frame, not a clean
  lower bound. (The identity-exposed original frame reads p = 0.00114 and is
  the memorization-entangled upper line.)
- **[TASK 1] Wave-2, less-famous cases** (9 treatments vs 23 controls):
  standalone permutation p = **0.00116**, AUC **0.829 [0.616, 0.983]**, 7/9
  flagged. The memorization rule R3 does not fire (identity-vs-perturbed
  dominance 3/9), so the pre-committed reading is R4 — residual capability,
  with no benchmark-accuracy comparison claims permitted.
- **[TASK 2] Post-cutoff holdout, per-case (N=3, no significance claimed)**:
  **HUBG score 70** — flagged, score ≥50 in 5/5 independent redraws (band
  58–76), and above all three of its matched controls (RXO 42 · BCO 30 ·
  XPO 20). WMK 32 and GNE 42 were not flagged and show no separation from
  their controls; the exact permutation p = 0.20 is context only
  (pre-declared under-powered at N=3 — this is per-case evidence, not a
  statistical claim). The single highest score in the holdout tier belongs to
  a control false positive (GridAI, GRDX, score 78). HUBG, WMK, and GNE carry
  **provisional Item 4.02 non-reliance restatement labels — NOT confirmed
  fraud, not enforcement outcomes.**

**[TASK 1] Mechanical baselines on the same 30 companies**: Beneish M
p = 0.498 / AUC 0.510, Dechow F p = 0.268 / AUC 0.573 — no separation on this
sample; LLM rankings are essentially uncorrelated with both. The LLM signal is
not a re-implementation of the formulas.

**False-positive anatomy** (from `atlas/PATTERNS.md` §d — per-tier false-flag
rates with Clopper–Pearson 95% intervals, never pooled: [TASK 1] wave-1 FPR
3/22 = 13.6% [2.9%, 34.9%] · [TASK 1] wave-2 FPR 5/23 = 21.7% [7.5%, 43.7%] ·
[TASK 2] holdout matched controls 2/9 = 22.2% [2.8%, 60.0%]). The false
positives are not hallucinations — every cited figure in every FP entry
verifies against the sealed facts. They are **over-readings of genuine
figures**, in recurring shapes a reviewer can anticipate:

- *Distress read as misstatement*: openly disclosed goodwill impairments taken
  as evidence prior carrying values were falsified (atlas case_30, score 65).
- *Tag re-mapping and coverage artifacts read as anomalies*: an XBRL concept
  re-mapping presented as an "internally inconsistent" series (case_44); a
  sign inconsistency between two cash-flow tags (case_49); a debt
  reclassification scored as an unexplained spike (case_07).
- *Amendment chronology promoted to restatement*: 10-K/A and comment-letter
  metadata read as restatement evidence without the decisive test — did any
  value change across filings? Sealed answer in each instance: no (case_10,
  score 58; case_48; hc_07).

**Honest use boundary.** This is a hypothesis-generation and triage instrument
for expert review — not an automated decision system, not a probability
engine, not a standalone alert feed. The 0–100 output is an **uncalibrated
ordinal `misstatement_risk_score`** (wave-2 ECE 0.179, wave-1 0.209 — the
probability reading is affirmatively rejected). Per
`specs/RISK_SCORE_SEMANTICS.md`: *"A score of 70 means stronger model-assessed
risk than a score of 40 under the same frozen protocol. It does not mean a 70%
probability of misstatement."* The per-threshold trade-offs, with intervals,
are in `analysis/DECISION_TABLE.md` — whose own headline is that on the E2
trajectory layer no single-threshold LLM strategy dominates.

**The input-missing case, both halves.** [TASK 2] For HUBG, the mechanical
screens could not even be computed — Beneish M and Dechow F both failed on
missing inputs — yet the LLM flagged it (score 70) from filing chronology and
account trends. And the flag was **tier-correct but mechanism-missed**: the
model anchored its hypothesis on HUBG's 2018 amendment cluster, not on the
unrecorded-liability mechanism the 2026 non-reliance actually covers
(`atlas/case_71.md`). Read it as risk screening that survives input gaps —
not as forensic mechanism identification.

## Page 5 — Division of judgment

Who does what, and why (full table: `CONTRIBUTIONS.md`):

- **Deterministic code**: cutoff enforcement, all quantitative metrics,
  mechanical baseline formulas, permutation tests, sealing tools. Rationale:
  anything that must be exactly reproducible and immune to
  narrative drift is code, seeded, and CI-verified.
- **The model**: evidence extraction and hypothesis ranking only — forced to
  cite verbatim figures and accession numbers, schema-constrained, forbidden
  open-ended prompts. Rationale: the model's comparative advantage is reading
  breadth; its known failure mode (over-reading genuine figures, Page 4) is
  bounded by making every claim citation-checkable.
- **Humans**: everything that is a judgment. Research design, thresholds, and
  conclusion rules were owner-selected and pre-registered before any score;
  every published grade carries human final sign-off; accounting judgments in
  the atlas remain drafts until owner audit. AI output here is unaudited work
  product until owner sign-off — the owner bears final responsibility for all
  published claims.

**The commitment that disciplines all of it**: a sealed prospective cycle.
Twelve companies, enumerated by a pre-frozen rule before any score exists,
scored and sealed on **2026-11-15** under pre-registered stop rules (≥11/12
scored or the cycle aborts and is preserved as-is), zero-metered execution,
externally verifiable timestamps, and pre-registered review horizons.
Verify the protocol at `specs/FORWARD_WATCHLIST_V1.md` and the frozen universe
at `forward/cycle_001/`. Until those cycles mature, this repository claims
retrospective separation (TASK 1) and per-case evidence (TASK 2) — nothing
more.

---

## Appendix — figure-to-source map

Every figure above, its frozen source, and the verifying path. All rows
recompute via `python tools/reproduce_analysis.py` (100/100) unless noted.

| Figure in brief | Frozen source (verified path) |
|---|---|
| [TASK 1] wave-1 perturbed permutation p = 0.0021 | `analysis/results_stats.json` → `secondary.perm_p_one_sided` (0.00207, published rounding 0.0021) |
| [TASK 1] wave-1 perturbed AUC 0.864 [0.722, 0.969] | `analysis/results_stats.json` → `secondary.auc`, `secondary.auc_boot95` |
| [TASK 1] wave-1 perturbed flags 4/8 at ≥50 | `analysis/results_stats.json` → `secondary.fisher_2x2.tp`; `analysis/decision_table.json` → `layers.L1_wave1_perturbed` T=50 |
| [TASK 1] wave-1 identity-exposed p = 0.00114 | `analysis/results_stats.json` → `primary.perm_p_one_sided` |
| [TASK 1] wave-2 standalone p = 0.00116 | `analysis/wave2_results.json` → `original.perm_p` |
| [TASK 1] wave-2 AUC 0.829 [0.616, 0.983] | `analysis/wave2_results.json` → `original.auc`, `original.auc_ci` |
| [TASK 1] wave-2 flags 7/9 | `analysis/wave2_results.json` → `flags.fraud` |
| [TASK 1] wave-2 outcome-recognition 8/9 = 88.9%, CP [51.7%, 99.7%]; controls 0/23 | `analysis/outcome_recognition_results.json` → `rates.treatment`, `rates.control` |
| [TASK 1] wave-1 name-ID 50% | `analysis/name_probe_results.json` → `rate_pct` |
| [TASK 1] wave-2 name-ID 21.9% (frozen name_match rule) | `analysis/synthesis.json` → `memorization_dose_response[wave2].name_id_pct` |
| [TASK 1] wave-2 identity-vs-perturbed dominance 3/9 (R4) | `analysis/wave2_results.json` → `R3_memorization` |
| [TASK 2] holdout knows_event 0/5 per case (HUBG·WMK·GNE); HTZ positive control True | `analysis/gate_k5_results.json` → `cases.*.band_true_of_5`, `positive_control_HTZ_knows_event`; transcripts `runs/holdout/recognition_k5/` |
| [TASK 2] HUBG score 70 (flagged) | `runs/holdout/scores/case_71.json` (legacy field name `misstatement_probability` — ordinal per `specs/RISK_SCORE_SEMANTICS.md` §3) |
| [TASK 2] HUBG ≥50 in 5/5 redraws, band 58–76 | `analysis/holdout_redraw_results.json` → `per_case.HUBG` |
| [TASK 2] HUBG above matched controls RXO 42 · BCO 30 · XPO 20 | `analysis/holdout_controls_results.json` → `per_case_side_by_side.HUBG` |
| [TASK 2] WMK 32 · GNE 42 (not flagged) | `analysis/holdout_redraw_results.json` → `per_case.WMK`, `per_case.GNE` |
| [TASK 2] holdout exact permutation p = 0.20 (context only) | `analysis/holdout_controls_results.json` → `exact_perm_p_CONTEXT_ONLY` (0.2045) |
| [TASK 2] E1 control flags 2/9 = 22.2%, CP [2.8%, 60.0%] | `analysis/holdout_controls_results.json` → `control_fpr` |
| [TASK 2] GRDX control false positive, score 78 (holdout-tier maximum) | `analysis/holdout_controls_results.json` → `per_case_side_by_side.GNE.matched_controls.GRDX`; `atlas/hc_03.md` |
| [TASK 1] wave-1 FPR 3/22 = 13.6%, CP [2.9%, 34.9%] | `analysis/results_stats.json` → `primary.fpr` |
| [TASK 1] wave-2 FPR 5/23 = 21.7%, CP [7.5%, 43.7%] | `analysis/wave2_results.json` → `flags`; `analysis/decision_table.json` → `layers.L2_wave2` T=50 `fpr_ci95` |
| [TASK 1] Beneish M p = 0.498 / AUC 0.510 · Dechow F p = 0.268 / AUC 0.573 | `analysis/results_stats.json` → `baselines.beneish_m`, `baselines.dechow_f` |
| [TASK 2] HUBG Beneish M / Dechow F uncomputable (missing inputs) | `analysis/holdout_summary.md` §2 table (계산불능/결측 rows) |
| ECE wave-2 0.179 · wave-1 0.209 | `analysis/calibration_wave2.json` → `ece_10bin`; `analysis/calibration.json` → `ece_10bin` |
| FP atlas scores: case_30 score 65 · case_10 score 58 | `atlas/case_30.md`, `atlas/case_10.md` (frozen scores quoted per RP-16/D91); synthesis `atlas/PATTERNS.md` §d |
| Pre-registration commit `c1b85a7` (plans frozen before scoring) | `README.md` (Extension experiments section); `analysis/*_PLAN.md` git history |
| Reproduction 100/100, 0 API calls | `tools/reproduce_analysis.py` (run directly; CI-verified) |
| Forward seal date 2026-11-15 · 12-company universe · ≥11/12 stop rule | `specs/FORWARD_WATCHLIST_V1.md` §1–§3; `forward/cycle_001/universe.json` (`selected` = 12) |

*Labels: HUBG · WMK · GNE are provisional Item 4.02 non-reliance restatement
events (G2), monitored for upgrade — not confirmed fraud. Control companies are
"non-enforcement," not certified clean (L-8: published FPRs are conditional on
the original control-selection criteria). Full limitations: L-1 through L-8,
`docs/methodology_limitations.md`.*

*DRAFT — pending owner finalization. 채점: Claude 보조 + 인간 최종 확정.
No positions · educational/informational · not investment advice.*
