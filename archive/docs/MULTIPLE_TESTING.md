# P6a — Multiple-testing disclosure annex

> Korean original (frozen): [MULTIPLE_TESTING.ko.md](MULTIPLE_TESTING.ko.md) — this English version is canonical; every number is byte-equal to the Korean source.

## Pre-classification of the test families

The enumeration below covers all 11 p-values recorded in
`analysis/results_stats.json` and `analysis/wave2_results.json` — the 9
permutation p-values fixed by `docs/STATS_ANNEX.md` plus the 2 Fisher exact
tests from the same frozen artifacts. Per the no-pooling principle across
tasks and tiers in RESULTS.md, significance is never combined across
different tasks or tiers.

| RESULTS row | frozen source key | classification | pre-registration basis and freeze commit |
|---|---|---|---|
| 1 | `primary.perm_p_one_sided` | T1 pre-registered confirmatory | `analysis/ANALYSIS_PLAN.md` §1, commit `5f4ca65` |
| 1 | `primary.fisher_2x2.p_one_sided` | T1 pre-registered confirmatory | `analysis/ANALYSIS_PLAN.md` §1, commit `5f4ca65` |
| 2 | `secondary.perm_p_one_sided` | T1 pre-registered confirmatory (perturbed frame) | `analysis/ANALYSIS_PLAN.md` §0–§1, commit `5f4ca65` |
| 2 | `secondary.fisher_2x2.p_one_sided` | T1 pre-registered confirmatory (perturbed frame) | `analysis/ANALYSIS_PLAN.md` §1, commit `5f4ca65` |
| 12 | `baselines.beneish_m.own_separation.perm_p` | T1 context-only mechanical baseline | `analysis/ANALYSIS_PLAN.md` §5, commit `5f4ca65`; never pooled with the LLM confirmatory family |
| 12 | `baselines.beneish_m.r2_residual_test.perm_p` | T1 pre-registered R2 verdict diagnostic, excluded from the confirmatory significance family | `analysis/ANALYSIS_PLAN.md` §4, commit `5f4ca65`; excluded because it drives the mechanical R2 dependence rule, not a significance claim |
| 12 | `baselines.dechow_f.own_separation.perm_p` | T1 context-only mechanical baseline | `analysis/ANALYSIS_PLAN.md` §5, commit `5f4ca65`; never pooled with the LLM confirmatory family |
| 12 | `baselines.dechow_f.r2_residual_test.perm_p` | T1 pre-registered R2 verdict diagnostic, excluded from the confirmatory significance family | `analysis/ANALYSIS_PLAN.md` §4, commit `5f4ca65`; excluded because it drives the mechanical R2 dependence rule, not a significance claim |
| 3 | `original.perm_p` | T1 pre-registered confirmatory (wave-2 standalone) | `analysis/ANALYSIS_PLAN_WAVE2.md` §1–§2, commit `9438b0c` |
| 3 | `perturbed.perm_p` | T1 pre-registered confirmatory (wave-2 perturbed frame) | `analysis/ANALYSIS_PLAN_WAVE2.md` §1–§2, commit `9438b0c`; published in `analysis/wave2_summary.md` |
| 3 | `pooled_secondary.perm_p` | T1 context-only pooled secondary | `analysis/ANALYSIS_PLAN_WAVE2.md` §8, commit `9438b0c`; never pooled with the standalone conclusion |

Published p-values outside those JSON artifacts are also kept in separate
families. The T2 E1 exact permutation of RESULTS row 6 was pre-fixed as
**CONTEXT ONLY** — not a basis for conclusions — in
`analysis/HOLDOUT_CONTROLS_PLAN.md` §4, commit `c1b85a7`. The
**EXPLORATORY L4 / E2 trajectory / `exploratory_combo`** of RESULTS row 13
is post-hoc exploration per `analysis/EARLINESS_PLAN.md` §3, commit
`c1b85a7` and `analysis/DECISION_TABLE.md` §4, and that row's `llm_p` is a
0–100 model score, not a p-value. None of these is ever pooled with the T1
confirmatory family.

The Holm computation therefore covers exactly the six T1 confirmatory
significance tests. The R2 residual tests, although pre-registered, drive
the R2 verdict rule rather than a significance conclusion, and the
mechanical baselines and pooled secondary are context values — all excluded
from this family.

## Multiplicity of the confirmatory family and the Holm–Bonferroni adjustment

When several tests support the same confirmatory statement, judging each at
α=0.05 separately inflates the probability that at least one is significant
by chance. `tools/multiple_testing.py` reads the values directly from the
frozen JSON artifacts and performs a deterministic Holm step-down
adjustment using only the standard library. Below is the actual output of
`./.venv/bin/python tools/multiple_testing.py`.

```text
label | frozen source | raw p | Holm adjusted p
RESULTS row 1: wave-1 identity-exposed | analysis/results_stats.json:primary.perm_p_one_sided | 0.00114 | 0.00684
RESULTS row 1: wave-1 identity-exposed Fisher | analysis/results_stats.json:primary.fisher_2x2.p_one_sided | 0.003145 | 0.009435
RESULTS row 2: wave-1 perturbed | analysis/results_stats.json:secondary.perm_p_one_sided | 0.00207 | 0.00828
RESULTS row 2: wave-1 perturbed Fisher | analysis/results_stats.json:secondary.fisher_2x2.p_one_sided | 0.059613 | 0.059613
RESULTS row 3: wave-2 standalone | analysis/wave2_results.json:original.perm_p | 0.0011599884001159987 | 0.00684
RESULTS row 3: wave-2 perturbed | analysis/wave2_results.json:perturbed.perm_p | 0.004269957300426995 | 0.009435
```

The following conclusion table is derived from that output; each raw p is
read from the frozen artifacts.

| RESULTS row | test | raw p | Holm adjusted p | pre-registered α=0.05 conclusion |
|---|---|---:|---:|---|
| 1 | permutation | 0.00114 | 0.00684 | The wave-1 identity-exposed separation remains significant after adjustment; the conclusion stands. |
| 1 | Fisher exact | 0.003145 | 0.009435 | The wave-1 identity-exposed threshold separation remains significant after adjustment; the conclusion stands. |
| 2 | permutation | 0.00207 | 0.00828 | The wave-1 perturbed separation remains significant after adjustment; the conclusion stands. |
| 2 | Fisher exact | 0.059613 | 0.059613 | The wave-1 perturbed threshold separation was not significant before or after adjustment; that conclusion does not stand. |
| 3 | standalone permutation | 0.0011599884001159987 | 0.00684 | The wave-2 standalone separation remains significant after adjustment; the conclusion stands. |
| 3 | perturbed permutation | 0.004269957300426995 | 0.009435 | The wave-2 perturbed separation remains significant after adjustment; the conclusion stands. |

The adjustment is a parallel derived statistic — it replaces no existing
number, threshold, or verdict rule.

## Limitations

Holm controls the family-wise error rate (FWER); it is not a false
discovery rate (FDR) procedure. These permutation p-values are Monte-Carlo
estimates (see the MC error in [docs/STATS_ANNEX.md](STATS_ANNEX.md)), so
the adjusted values inherit that error unchanged. Multiplicity adjustment
also cannot repair the selection and survivorship biases already disclosed
for the control groups.

All results are scoped to a single Claude-based pipeline. Grading:
Claude-assisted, human-finalized. No positions · educational/informational
· not investment advice.
