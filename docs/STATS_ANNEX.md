# FB-09 — 게시 통계의 Monte-Carlo 오차·시드·정확성 부록

## 목적

이 부록은 커밋된 `analysis/results_stats.json`과
`analysis/wave2_results.json`에 기록된 Monte-Carlo 순열 p값의 시뮬레이션
오차와 AUC 신뢰구간의 시드·출처를 한곳에 표시한다. 또한 각 순열 설계의 완전
열거 조합 수를 표시한다.

## 방법

`tools/stats_annex.py`는 두 JSON 산출물만 통계값의 입력으로 읽는다. 각 기록된
p값에 대해 분석 소스에 명시된 반복 수 B=100,000을 사용하여
MC-SE = `sqrt(p(1-p)/B)`와 `p ± 1.96·MC-SE`를 계산한다. B를 p값에서 역산하지
않는다. 순열 p 추정량은 분석 소스에 구현된 `(ge+1)/(n+1)`이다. 완전 열거 수는
`math.comb(n, n_t)`로 계산한다. 스크립트는 난수와 외부 패키지를 사용하지 않는다.

## 재생성 가능한 실제 출력

아래는 `./.venv/bin/python tools/stats_annex.py`의 실제 출력이다.

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

## 이 부록이 하지 않는 일

이 부록은 동결 통계값을 재계산하거나 수정하지 않으며, 새로운 통계적 주장을
추가하지 않는다. MC 구간은 기록된 p값 자체의 신뢰구간이 아니라 유한 반복에서
생기는 Monte-Carlo 오차 표시다. 정확순열 행은 완전 열거의 실행 가능성 메모일
뿐 정확순열 검정 결과가 아니다. 기존 primary·secondary·exploratory 구분도
변경하지 않는다.

본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
채점: Claude 보조 + 인간 최종 확정. 포지션 없음 · 교육·정보 목적 · 투자 조언
아님.
