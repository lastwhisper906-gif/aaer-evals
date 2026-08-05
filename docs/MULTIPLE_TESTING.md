# P6a — 다중 검정 공개 부록

## 검정군의 사전 분류

아래 열거 범위는 `analysis/results_stats.json`과
`analysis/wave2_results.json`에 기록된 p값 11개 전부다. 이는
`docs/STATS_ANNEX.md`가 고정한 순열 p값 9개에 같은 동결 산출물의 Fisher
정확검정 2개를 더한 완전한 목록이다. RESULTS.md의 과제·계층 간 no-pooling
원칙에 따라 서로 다른 과제나 계층의 유의성을 합치지 않는다.

| RESULTS 행 | 동결 source key | 분류 | 사전 등록 근거와 freeze commit |
|---|---|---|---|
| 1 | `primary.perm_p_one_sided` | T1 사전 등록 확증 | `analysis/ANALYSIS_PLAN.md` §1, commit `5f4ca65` |
| 1 | `primary.fisher_2x2.p_one_sided` | T1 사전 등록 확증 | `analysis/ANALYSIS_PLAN.md` §1, commit `5f4ca65` |
| 2 | `secondary.perm_p_one_sided` | T1 사전 등록 확증(perturbed frame) | `analysis/ANALYSIS_PLAN.md` §0–§1, commit `5f4ca65` |
| 2 | `secondary.fisher_2x2.p_one_sided` | T1 사전 등록 확증(perturbed frame) | `analysis/ANALYSIS_PLAN.md` §1, commit `5f4ca65` |
| 12 | `baselines.beneish_m.own_separation.perm_p` | T1 맥락 전용 기계 기준선 | `analysis/ANALYSIS_PLAN.md` §5, commit `5f4ca65`; LLM 확증군과 합치지 않음 |
| 12 | `baselines.beneish_m.r2_residual_test.perm_p` | T1 사전 등록 R2 판정 진단, 확증 유의성 검정군 제외 | `analysis/ANALYSIS_PLAN.md` §4, commit `5f4ca65`; 유의성 주장이 아니라 R2 기계 의존 규칙의 입력이므로 제외 |
| 12 | `baselines.dechow_f.own_separation.perm_p` | T1 맥락 전용 기계 기준선 | `analysis/ANALYSIS_PLAN.md` §5, commit `5f4ca65`; LLM 확증군과 합치지 않음 |
| 12 | `baselines.dechow_f.r2_residual_test.perm_p` | T1 사전 등록 R2 판정 진단, 확증 유의성 검정군 제외 | `analysis/ANALYSIS_PLAN.md` §4, commit `5f4ca65`; 유의성 주장이 아니라 R2 기계 의존 규칙의 입력이므로 제외 |
| 3 | `original.perm_p` | T1 사전 등록 확증(wave-2 standalone) | `analysis/ANALYSIS_PLAN_WAVE2.md` §1–§2, commit `9438b0c` |
| 3 | `perturbed.perm_p` | T1 사전 등록 확증(wave-2 perturbed frame) | `analysis/ANALYSIS_PLAN_WAVE2.md` §1–§2, commit `9438b0c`; `analysis/wave2_summary.md`에 게시 |
| 3 | `pooled_secondary.perm_p` | T1 맥락 전용 pooled secondary | `analysis/ANALYSIS_PLAN_WAVE2.md` §8, commit `9438b0c`; standalone 결론과 합치지 않음 |

JSON 목록 밖의 게시 p값도 별도 군으로 유지한다. RESULTS 행 6의 T2 E1 exact
permutation은 `analysis/HOLDOUT_CONTROLS_PLAN.md` §4, commit `c1b85a7`에서
결론 근거가 아닌 **CONTEXT ONLY**로 사전 고정됐다. RESULTS 행 13의
**EXPLORATORY L4 / E2 trajectory / `exploratory_combo`**는
`analysis/EARLINESS_PLAN.md` §3, commit `c1b85a7` 및
`analysis/DECISION_TABLE.md` §4의 사후 탐색이며, 그 행의 `llm_p`는 0–100
모델 점수이지 p값이 아니다. 어느 것도 T1 확증군과 합치지 않는다.

따라서 Holm 계산 대상은 T1 확증 유의성 검정 여섯 개뿐이다. R2 잔차 검정은
사전 등록됐지만 유의성 결론이 아니라 R2 판정 규칙을 구동하고, 기계 기준선과
pooled secondary는 맥락값이므로 이 군에서 제외한다.

## 확증군의 다중성 및 Holm–Bonferroni 보정

같은 확증 서술에 여러 검정을 제시하면 모두를 α=0.05로 따로 판정할 때 적어도
하나가 우연히 유의해질 확률이 커진다. `tools/multiple_testing.py`는 위 동결
JSON의 값을 직접 읽고 표준 라이브러리만으로 결정론적 Holm step-down 보정을
한다. 아래는 `./.venv/bin/python tools/multiple_testing.py`의 실제 출력이다.

```text
label | frozen source | raw p | Holm adjusted p
RESULTS row 1: wave-1 identity-exposed | analysis/results_stats.json:primary.perm_p_one_sided | 0.00114 | 0.00684
RESULTS row 1: wave-1 identity-exposed Fisher | analysis/results_stats.json:primary.fisher_2x2.p_one_sided | 0.003145 | 0.009435
RESULTS row 2: wave-1 perturbed | analysis/results_stats.json:secondary.perm_p_one_sided | 0.00207 | 0.00828
RESULTS row 2: wave-1 perturbed Fisher | analysis/results_stats.json:secondary.fisher_2x2.p_one_sided | 0.059613 | 0.059613
RESULTS row 3: wave-2 standalone | analysis/wave2_results.json:original.perm_p | 0.0011599884001159987 | 0.00684
RESULTS row 3: wave-2 perturbed | analysis/wave2_results.json:perturbed.perm_p | 0.004269957300426995 | 0.009435
```

다음 표는 그 출력에서 파생한 결론 표이며 raw p는 동결 산출물에서 읽은 값이다.

| RESULTS 행 | 검정 | raw p | Holm adjusted p | 사전 등록 α=0.05 결론 |
|---|---|---:|---:|---|
| 1 | permutation | 0.00114 | 0.00684 | wave-1 identity-exposed 분리는 보정 후에도 유의하며 결론이 유지된다. |
| 1 | Fisher exact | 0.003145 | 0.009435 | wave-1 identity-exposed 임계값 분리는 보정 후에도 유의하며 결론이 유지된다. |
| 2 | permutation | 0.00207 | 0.00828 | wave-1 perturbed 분리는 보정 후에도 유의하며 결론이 유지된다. |
| 2 | Fisher exact | 0.059613 | 0.059613 | wave-1 perturbed 임계값 분리는 원래도 보정 후에도 유의하지 않아 결론이 유지되지 않는다. |
| 3 | standalone permutation | 0.0011599884001159987 | 0.00684 | wave-2 standalone 분리는 보정 후에도 유의하며 결론이 유지된다. |
| 3 | perturbed permutation | 0.004269957300426995 | 0.009435 | wave-2 perturbed 분리는 보정 후에도 유의하며 결론이 유지된다. |

보정은 기존 수치·임계·판정 규칙을 대체하지 않는 병행 파생 통계다.

## 한계

Holm은 family-wise error rate(FWER)를 통제하며 false discovery rate(FDR)를
통제하는 절차는 아니다. 이 순열 p값들은 Monte-Carlo 추정치이므로
([docs/STATS_ANNEX.md](STATS_ANNEX.md)의 MC 오차 참조) 보정값도 그 오차를
그대로 물려받는다. 또한 다중성 보정은 대조군에 이미 공개된 선택 편향과
생존자 편향을 고치지 못한다.

본 결과는 Claude 기반 단일 파이프라인에 한정된다. 채점: Claude 보조 + 인간
최종 확정. 포지션 없음 · 교육·정보 목적 · 투자 조언 아님.
