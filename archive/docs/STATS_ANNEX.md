# FB-09 — Monte-Carlo error, seed, and exactness annex for the published statistics

> Korean original (frozen): [STATS_ANNEX.ko.md](STATS_ANNEX.ko.md) — this English version is canonical; every number is byte-equal to the Korean source.

## Purpose

This annex displays, in one place, the simulation error of the Monte-Carlo
permutation p-values recorded in the committed
`analysis/results_stats.json` and `analysis/wave2_results.json`, and the
seed and provenance of the AUC confidence intervals. It also shows the full
enumeration count of each permutation design.

## Method

`tools/stats_annex.py` reads only the two JSON artifacts as statistical
input. For each recorded p-value it computes MC-SE = `sqrt(p(1-p)/B)` and
`p ± 1.96·MC-SE` using the iteration count B=100,000 stated in the analysis
source; B is never back-derived from the p-value. The permutation-p
estimator is `(ge+1)/(n+1)` as implemented in the analysis source. Full
enumeration counts are computed with `math.comb(n, n_t)`. The script uses
no randomness and no external packages.

## Regenerable actual output

Below is the actual output of `./.venv/bin/python tools/stats_annex.py`.

```text
MONTE-CARLO PERMUTATION P-VALUES
label | artifact key | p | B (source) | MC-SE | 95% MC interval | estimator (source)
wave1 primary | analysis/results_stats.json:primary.perm_p_one_sided | 0.00114 | 100000 (analysis/stats.py:16) | 0.000106709905819 | [0.000930848584594, 0.00134915141541] | (ge+1)/(n+1) (analysis/stats.py:41)
wave1 secondary | analysis/results_stats.json:secondary.perm_p_one_sided | 0.00207 | 100000 (analysis/stats.py:16) | 0.00014372595799 | [0.00178829712234, 0.00235170287766] | (ge+1)/(n+1) (analysis/stats.py:41)
wave1 Beneish separation | analysis/results_stats.json:baselines.beneish_m.own_separation.perm_p | 0.498245 | 100000 (analysis/stats.py:16) | 0.00158112909016 | [0.495145986983, 0.501344013017] | (ge+1)/(n+1) (analysis/stats.py:41)
wave1 Beneish residual | analysis/results_stats.json:baselines.beneish_m.r2_residual_test.perm_p | 0.00529 | 100000 (analysis/stats.py:16) | 0.000229390843322 | [0.00484039394709, 0.00573960605291] | (ge+1)/(n+1) (analysis/stats.py:41)
wave1 Dechow separation | analysis/results_stats.json:baselines.dechow_f.own_separation.perm_p | 0.267897 | 100000 (analysis/stats.py:16) | 0.00140045777298 | [0.265152102765, 0.270641897235] | (ge+1)/(n+1) (analysis/stats.py:41)
wave1 Dechow residual | analysis/results_stats.json:baselines.dechow_f.r2_residual_test.perm_p | 0.00097 | 100000 (analysis/stats.py:16) | 9.84407994685e-05 | [0.000777056033042, 0.00116294396696] | (ge+1)/(n+1) (analysis/stats.py:41)
wave2 original | analysis/wave2_results.json:original.perm_p | 0.0011599884001159987 | 100000 (analysis/legacy/wave2_analyze_v1.py:29) | 0.00010764027253 | [0.000949013465958, 0.00137096333427] | (ge+1)/(n+1) (analysis/legacy/wave2_analyze_v1.py:34)
wave2 perturbed | analysis/wave2_results.json:perturbed.perm_p | 0.004269957300426995 | 100000 (analysis/legacy/wave2_analyze_v1.py:29) | 0.000206197108735 | [0.00386581096731, 0.00467410363355] | (ge+1)/(n+1) (analysis/legacy/wave2_analyze_v1.py:34)
pooled secondary | analysis/wave2_results.json:pooled_secondary.perm_p | 2.999970000299997e-05 | 100000 (analysis/legacy/wave2_analyze_v1.py:29) | 1.73201616681e-05 | [-3.94781686653e-06, 6.39472168725e-05] | (ge+1)/(n+1) (analysis/legacy/wave2_analyze_v1.py:34)

EXACT-PERMUTATION FEASIBILITY
design | C(n,n_t) | enumerable on commodity hardware
6v16 | 74613 | yes
8v22 | 5852925 | yes
9v23 | 28048800 | yes
17v45 | 739632519584070 | no

SEED AND AUC-CI PROVENANCE
artifact key | value | provenance
analysis/results_stats.json:seed | 20260707 | recorded in artifact
analysis/results_stats.json:primary.auc_boot95 | [0.599,0.983] | recorded in artifact
analysis/results_stats.json:secondary.auc_boot95 | [0.722,0.969] | recorded in artifact
analysis/wave2_results.json:seed | 20260707 | not in artifact; source: analysis/legacy/wave2_analyze_v1.py:12
analysis/wave2_results.json:original.auc_ci | [0.616,0.983] | recorded in artifact; method source: analysis/legacy/wave2_analyze_v1.py:40-44
```

## What this annex does not do

This annex does not recompute or revise the frozen statistics, and it adds
no new statistical claims. The MC intervals are not confidence intervals of
the recorded p-values themselves — they display the Monte-Carlo error that
arises from finite iterations. The exact-permutation rows are feasibility
notes on full enumeration, not exact-permutation test results. The existing
primary·secondary·exploratory classification is unchanged.

All results are scoped to a single Claude-based pipeline (PROJECT.md §5-5).
Grading: Claude-assisted, human-finalized. No positions ·
educational/informational · not investment advice.
