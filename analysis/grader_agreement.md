# SPOT-CHECK — Grader Agreement / Noise Lower Bound (Track 2, 2026-07-08)

> **SPOT-CHECK ONLY.** This is a lower-bound noise probe on grader reliability, **not** a
> re-grade of the headline. It changes **no published grade**. Every number below is
> labelled SPOT-CHECK. No metered/grader/runner/probe call was made; no `runs/` or
> `scoring/grades*/` artifact was modified. Analysis is over already-committed grade
> artifacts only.

## 1. Methodology

- **Source A (opus SPOT-CHECK regrades):** `runs/hardening/regrade_opus/case_{01,02,03,04,10,12}.json`
  — 6 committed regrades, grader pin `claude-opus-4-8`, labelled in each file
  `"SPOT-CHECK — cross-family grader agreement (RP-06 A2). NEVER merge into scoring/grades/."`
- **Source B (fable-5 production grades):** the committed grade for the **same variant** each
  opus file declares in its `_meta.variant_graded` field:
  - `variant_graded = runs/perturbed` → `scoring/grades/perturbed/case_NN.json` (cases 01, 02, 03, 12)
  - `variant_graded = runs/main` → `scoring/grades/main/case_NN.json` (cases 04, 10)
- **Mapping confirmed** via `scoring/id_mapping.json`: each opus file's `_meta.original_id`
  matches the fable file's `_meta.original_id` for the same `case_id` (T21, T11, T12, C08, C04, T28).
  All 6 map cleanly; both graders graded the same evaluatee output of the same variant.
- **Dimensions compared:** dim1 (probability band), dim2 (mechanism, treatment-only), dim4
  (evidence quality) — the three graded dims named in the Track-2 spec and `eval_spec.md §4`.
  dim3 (genre mapping) is out of Track-2 scope and not scored here.
- **N is small by design** (a 6-case spot-check). Per spec, where N or the category
  distribution makes Cohen's κ misleading, that is stated quantitatively rather than
  reporting κ as if it were stable. CIs are exact Clopper–Pearson (95%).

## 2. Overlap

**N = 6 cases** overlap (opus regrade ∩ fable production grade), all with a clean id match:

| case_id | original_id | variant | group |
|---|---|---|---|
| case_01 | T21 | perturbed | treatment |
| case_02 | T11 | perturbed | treatment |
| case_03 | T12 | perturbed | treatment |
| case_04 | C08 | main | control |
| case_10 | C04 | main | control |
| case_12 | T28 | perturbed | treatment |

Per-dimension cell counts: dim1 N=6, dim2 N=4 (2 control cases are `null` by rubric), dim4 N=6.
Total compared cells = 16.

## 3. Per-dimension agreement (SPOT-CHECK)

| dim | N | raw agreement | Clopper–Pearson 95% CI | Cohen's κ | κ usable? |
|---|---|---|---|---|---|
| dim1 (prob band) | 6 | **6/6 = 1.000** | [0.541, 1.000] | 1.000 | fragile (N=6) |
| dim2 (mechanism) | 4 | **3/4 = 0.750** | [0.194, 0.994] | 0.636 | **no — N=4** |
| dim4 (evidence)  | 6 | **5/6 = 0.833** | [0.359, 0.996] | 0.000 | **no — κ paradox** |
| pooled cells | 16 | 14/16 = 0.875 | [0.617, 0.984] | — | — |

**Why κ is not the headline here:**
- **dim2:** N=4. A 4-item κ is not interpretable; a single cell change swings it by ~0.3.
  Report N and the CI, not κ.
- **dim4:** raw agreement is 0.833 but κ = **0.000**. This is the classic κ paradox: opus
  used only category `3` across all 6 cases (degenerate marginal), so chance-agreement
  p_e = 0.833 = observed agreement, forcing κ→0. κ here reflects the degenerate margin,
  **not** poor reliability. Raw agreement + CI is the honest statistic.
- **dim1:** κ = 1.000 only because agreement was perfect; with N=6 the lower CI on the
  agreement *rate itself* is 0.54, so "perfect" should be read as "no observed disagreement
  in 6 draws," not "provably perfect."

## 4. Disagreement list (2 of 16 cells)

| case | orig | dim | fable-5 | opus | type | direction | substance |
|---|---|---|---|---|---|---|---|
| case_01 | T21 | dim2 | 1 | 2 | adjacent | opus +1 | Rubric boundary L1↔L2: whether the treatment *type* ("aggressive rev rec / channel-stuffing / bill-and-hold") **substantially matches** the key's barter/side-agreement mechanism. Opus: account+direction+treatment-type substantial match → 2. Fable: only account+direction match; named sub-mechanism differs from the key → 1. |
| case_10 | C04 | dim4 | 2 | 3 | adjacent | opus +1 | Same data points cited by both. Boundary L2↔L3: fable caps at 2 because the top mechanism **over-concludes on a clean control** (reads provenance metadata of a 10-K/A as a restatement signal); opus rates the coherent multi-year combination as 3. |

**Both disagreements are (a) off-by-one and (b) in the same direction: opus is the more
lenient grader by exactly 1 point.** With only 2 disagreements this is a *directional hint*,
not an established grader bias — far too few points to claim systematic leniency.

## 5. Flag-flip check (CRITICAL)

The TP/FP flag is set by the **evaluatee's `misstatement_probability` vs threshold** — a
grader-independent quantity (both graders scored the identical evaluatee output; e.g. case_01
p=45, case_10 p=58). The grade dimension that reflects the flag boundary is **dim1**, and
**dim1 agreed 6/6 (100%)**. Both disagreements are in dim2 and dim4, neither of which is on
the p≥50 / control boundary.

- case_10 (C04) is a control graded p=58 → a **false positive**; both graders assign dim1=0.
  The dim4 disagreement (2 vs 3) does **not** change its FP status.

**No disagreement flips any flag.** No TP/FP changes. Nothing in this spot-check requires the
owner queue on flag-flip grounds. (One directional note is queued below for owner awareness,
not for action.)

## 6. How much do grades depend on the grader? (SPOT-CHECK lower bound)

- On the flag-bearing dimension (dim1), **cross-family grader dependence is ~zero in this
  sample**: 6/6 agreement, and dim1 is a deterministic band function of the evaluatee's p,
  which both graders read identically. The flag itself is not a graded quantity, so it is
  **grader-invariant by construction** here.
- On the qualitative dimensions (dim2 mechanism, dim4 evidence), grader dependence is
  **non-zero but small and adjacent**: 2 of 10 non-null qualitative cells differ, each by 1
  point, each at a documented rubric L1↔L2 / L2↔L3 boundary, each in the lenient direction
  for the spot-check grader.
- **Bound statement:** across 16 compared cells, observed cross-grader agreement is
  **14/16 = 0.875 (95% CI [0.617, 0.984])**, with **no** disagreement large enough to move a
  band across a scoring boundary that would change a case's group-level outcome. This is a
  **lower bound on reliability from a 6-case spot-check**, not a re-grade; it neither
  validates nor overturns the published grades. N=6 is too small for a stable κ on the
  qualitative dims — the CI width (dim2 spans [0.19, 0.99]) is the honest summary of that
  fragility.

**What to know about this judgment (learning note):** the reassuring 6/6 on dim1 is partly
*structural* (dim1 band is a deterministic function of the evaluatee's p that both graders
just read off), so it should not be over-read as evidence that the graders "agree on the hard
part." The hard part is dim2/dim4, and there N is 4–6 with 2 adjacent, same-direction misses —
enough to say "no gross disagreement," not enough to certify the qualitative rubric as
grader-stable.

## 7. Provenance / immutability

- Read-only over `runs/hardening/regrade_opus/` and `scoring/grades/{perturbed,main}/`.
- No file under `runs/` or `scoring/grades*/` was modified. No grader/runner/probe executed.
  No network. No `git`.
- Outputs (this file + `analysis/grader_agreement.csv`) are the only writes.
