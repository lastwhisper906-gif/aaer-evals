> Korean original: [ERRATA.ko.md](ERRATA.ko.md) (frozen snapshot: E-001–E-002).

# ERRATA — Published-artifact corrections (append-only)

> Principle: frozen and published artifacts are not modified. Corrections are made only by
> adding entries to this file and publishing new code paths/new artifact paths in parallel
> (the same approach used by the 2d78faf de-identification disclosure precedent). This file
> is append-only: existing entries are not edited; they are updated through subsequent entries.
> Future errata are appended here, the English canonical; the frozen Korean snapshot is not extended.

---

## E-001 (2026-07-21) — Wave-2 analysis code diverged from the preregistered plan (F1, V1/V2/V11)

**Source**: Finding F1 from external review (main @ db8b85f, 2026-07-20) →
`audit/REVIEW_VERIFICATION.md` V1·V2·V11 (all CONFIRMED, with file:line evidence).

**Facts (what differed)**:

1. **R2 decision implementation diverged** — `analysis/ANALYSIS_PLAN_WAVE2.md` §4
   preregistered R2 as "Spearman ρ ≥ 0.7 (signed) ***igo* (and)** residual
   incremental test p ≥ 0.05," but `analysis/wave2_analyze.py:101` decided it from
   `abs(rho) >= 0.7` alone. <!-- sanctioned romanization --> The dropped conjunction
   *igo* is the finding corrected by the subsequent entry. Neither residual regression nor a residual
   permutation test exists in the wave-2 code. (`analysis/stats.py:202` from wave-1
   implements the plan; the divergence arose during the wave-2 reimplementation.)
2. **Preregistered statistics omitted** — The plan's §2 one-sided Fisher exact test,
   §3 Clopper–Pearson interval (when FP≥1), and §1 worst-case substitution
   sensitivity for INCOMPLETE are absent from the `wave2_analyze.py` output
   (`wave2_results.json`). Only flag counts and raw FPR% were stored.
3. **Inaccurate "verbatim" description** — The claim "conclusion rules R1–R4
   **verbatim**" in `analysis/ISSUE_1_WAVE2_DRAFT.md:63`, and the claims in §5 of
   the same document and `analysis/wave2_summary.md:5` that the results are reproduced
   "with `python analysis/wave2_analyze.py`," were inaccurate as of the v1 wave-2
   release. In particular, the "FPR 21.7% CP [7.5%, 43.7%]" cited by §5 was not
   produced by that command.

**Effect on conclusion figures (within the scope currently verified)**: The observed
ρ(LLM,M)=0.337 and ρ(LLM,F)=0.265 are both positive and far from 0.7, so correcting
abs→signed alone does not reverse the R2 decision. A formal comparison is recorded in
a subsequent entry below after completion of the rev2 rerun.

**Actions**:

- The v1 artifacts (`analysis/wave2_results.json`, `analysis/wave2_summary.md`,
  `analysis/ISSUE_1_WAVE2_DRAFT.md`) remain **frozen and unmodified**. The original
  implementation is preserved as `analysis/legacy/wave2_analyze_v1.py` (Task 2).
- The corrected analysis is rerun through one decision module (`aaer_eval/verdict.py`)
  and one statistics module (`aaer_eval/statistics.py`) and published in parallel as
  **wave-2 rev2** at the new path (`analysis/out/wave2_rev2/`); it does not replace v1.
- The rev2 vs v1 decision comparison is recorded after execution in the subsequent
  entry (planned as E-002). If the decision changes, no dependent work is committed
  before owner review (REMEDIATION_HARNESS_PROMPT QUARANTINE rule 1).

**Disclosure language**: This entry itself is the disclosure section. Every external
surface that subsequently cites wave-2 must link the following statement:
<!-- sanctioned romanization --> "The v1 analysis code disagreed with the preregistered
plan at 3 points (the R2 decision formula, omitted statistics, and reproducibility claim),
and was corrected and published in parallel in rev2" (*gyojeong·byeonghaeng gesi*,
"corrected and published in parallel").

---

## E-002 (2026-07-21) — Wave-2 rev2 vs v1 comparison (Task 5 complete, owner approval D1)

**Comparison basis**: v1 = frozen `analysis/wave2_results.json` (published). rev2 =
`analysis/out/wave2_rev2/wave2_results_rev2.json`
(reproduce: `PYTHONPATH=. python analysis/wave2_analyze.py`, seed 20260707).

**Decision unchanged**: Trigger rule **R4 = R4** (v1 = rev2). Primary (1st) statistics
match exactly — permutation p 0.00116, mean difference +20.57pp, Cliff δ 0.657,
AUC 0.829 [0.616, 0.983], R3 inclusion 3/9 (not triggered), perturbed secondary
(2nd) frame p 0.00427 / AUC 0.790, pooled secondary (2nd; alongside the standalone figures above)
<!-- sanctioned lint-rule addition --> p 3.0e-05 / AUC 0.831, flags 7/9 vs 5/23.

**Changed published statistics (tie-aware Spearman correction, V8)** — both values shown:

- **ρ(LLM, Beneish M): 0.337 → 0.333** (down, same n=20)
- **ρ(LLM, Dechow F): 0.265 → 0.293** (**up** — explicitly showing that the
  correction did not move only in the favorable direction, same n=17)

Cause: The Spearman implementation in v1 wave-2 used custom ranks that did not average
ties (REVIEW_VERIFICATION V8). Both values remain far from the R2 threshold of 0.7, so
the decision is unaffected.

**New output (preregistered but not produced by v1, V2)**: one-sided Fisher exact
p = 0.00573; FPR Clopper–Pearson 95% [7.5%, 43.7%]; INCOMPLETE worst-case substitution
sensitivity n_incomplete=0 (primary (1st) p unchanged); R2 residual permutation p — M 0.0035,
F 0.0023 (both < 0.05: residual separation remains significant after baseline regression,
evidence against the "machine-signal replication" explanation).

**Explicit confirmation of the source of the published CP interval**: The "FPR 21.7% CP
[7.5%, 43.7%]" cited by the published document (`analysis/ISSUE_1_WAVE2_DRAFT.md` §5)
**was not produced by the published reproducibility command (`python
analysis/wave2_analyze.py`)**. That code contained no CP calculation, and the figure's
source was outside the reproducibility path. rev2 reproduces the same interval
[7.5, 43.7] in code, confirming that the value itself was accurate; however, the
"reproducible" claim was inaccurate at the v1 point in time (specifying E-001 item 3).

**Flag for the next plan revision (not a change now)**: Under the R3 inclusion rule,
treatment cases without a perturbed draw are excluded from the inclusion numerator but
remain in the denominator (n_treatment). This behavior is identical in v1 and rev2, and
ANALYSIS_PLAN_WAVE2 does not specify this case. It must be specified explicitly in the
next plan revision (no retroactive change under the preregistration principle).

**Status**: This entry makes rev2 citable. The v1 artifacts remain frozen.

---

## E-003 (2026-08-06) — P2 synthesis layer: unified_table m_flag inversion + wave-1 median estimator

**Source**: rotation-2 C1B component review (adversarial replenish, D-P70; full
evidence `.direction/feedback/rot2_C1B_2026-08-05.md`). Owner signature recorded
2026-08-06 ("sign", D-P82) per the INV-03(c)/INV-06 correction path
(E-001/E-002 precedent: disclose-don't-revise, parallel publication).

**Facts (what was wrong)**:

1. **`analysis/unified_table.csv` m_flag inverted** — every m-scored row of the
   published 65-row cross-wave table carried `int(m <= -1.78)`, the exact
   complement of the frozen rule `m > -1.78` (`analysis/screens.py`
   flag_minus_1_78 · `analysis/baseline_screens.md` · `analysis/baselines.py` →
   `baseline_table.csv`). The companion doc `analysis/synthesis.md:76` wrote the
   defect down rather than catching it. RESULTS row 12's AUC/correlation/p are
   sourced from `baseline_table.csv` and are unaffected.
2. **`analysis/synthesis.json` wave-1 fraud_median 60.0 → 57.5** — the v1 code
   took `sorted(fr)[len(fr)//2]` (upper-middle element); wave-1 fraud n=8 is the
   repository's only even-n group, so the estimator error surfaced only there.
   True median of the eight scores: 57.5. `control_median` 33.0 is numerically
   unaffected (tied middle elements); wave-2/holdout groups are odd-n and
   unaffected; AUC/CI fields do not use the median and are unaffected.
   Verified 2026-08-06: no published surface (README, RESULTS.md,
   `analysis/*.md`) cites the 60.0 value — every "60.0" occurrence is the
   unrelated Clopper–Pearson bound "60.0%".

**Actions**:

- Code corrections were committed **before** regeneration per INV-03(c) at
  `0bf612e` (m_flag rule at 3 sites + `statistics.median`), with a
  divergence-lock test `analysis/test_synthesis_flag_convention.py`
  (2 passed, re-verified 2026-08-06).
- Following the owner signature, `analysis/unified_table.csv` and
  `analysis/synthesis.json` are regenerated by `analysis/synthesis.py` in this
  entry's commit. Originals are preserved unchanged in git history
  (pre-regeneration state: `10a97fe` and earlier); this is parallel
  publication by commit lineage, not replacement of a frozen v1-sealed path.
- The Phase-1 divergence audit (D-ledger) re-ran every analyzer and confirmed
  the only published-number deviations on regeneration are exactly these two
  known deltas.

**Disclosure language**: Any external surface that cites the cross-wave unified
table's m_flag column or the wave-1 fraud median must link this entry: "The
unified table's m_flag was computed as the complement of the frozen rule and
the wave-1 fraud median used a biased even-n estimator (60.0; corrected value
57.5); both were corrected and republished per E-003."
