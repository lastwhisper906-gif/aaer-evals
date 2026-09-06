# E4 교차모델 점검 — **EXPLORATORY** (각주 전용, 발행 금지 게이트)

> 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
> 성능 비교·벤치마크 아님 — 순위 중첩도 측정만 (CROSSMODEL_PLAN §0/§3).

- N = 18 (홀드아웃 3 + wave-2 6 + E1 대조군 9) · 프레임 = 원 채점 동일(original)
- **Spearman ρ = 0.781** · 플래그(p≥50) 일치 15/18 · Cohen κ = 0.6582
- 불일치 케이스: case_52, case_71, hc_07

| case | group | sonnet-5 p | opus-4-8 p | flag 일치 |
|---|---|---|---|---|
| case_44 | wave2 | 55 | 55 | ✓ |
| case_49 | wave2 | 58 | 55 | ✓ |
| case_52 | wave2 | 40 | 52 | ✗ |
| case_60 | wave2 | 65 | 70 | ✓ |
| case_61 | wave2 | 72 | 80 | ✓ |
| case_65 | wave2 | 74 | 58 | ✓ |
| case_71 | holdout | 70 | 48 | ✗ |
| case_72 | holdout | 32 | 25 | ✓ |
| case_73 | holdout | 42 | 35 | ✓ |
| hc_01 | e1_control | 35 | 42 | ✓ |
| hc_02 | e1_control | 20 | 25 | ✓ |
| hc_03 | e1_control | 78 | 80 | ✓ |
| hc_04 | e1_control | 42 | 25 | ✓ |
| hc_05 | e1_control | 30 | 34 | ✓ |
| hc_06 | e1_control | 20 | 24 | ✓ |
| hc_07 | e1_control | 58 | 22 | ✗ |
| hc_08 | e1_control | 32 | 22 | ✓ |
| hc_09 | e1_control | 12 | 15 | ✓ |
