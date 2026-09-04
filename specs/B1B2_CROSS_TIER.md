# specs/B1B2_CROSS_TIER.md — 공식 스크린(B1 Beneish M · B2 Dechow F) 교차 티어 head-to-head 사전 등록

> **freeze-commit-then-run** (INV-07): 본 스펙 커밋은 `analysis/b1b2_cross_tier.py`가
> git 이력에 존재하기 **전에** 이루어진다. 아래 프레임·부분집합 규칙·통계·판독
> 분기는 어떤 교차 티어 수치도 계산되기 전에 고정된 것이다.
> 발의: 외부 리뷰 C 항목 2 (`.direction/feedback/EXT_FB_C_2026-09-04.md`).
> 권한: 소유자 지시 2026-09-04 ("모두 반영해줘") — 집행 기록 D-P105 (사전 등록) ·
> D-P106 (실행·공개). 분류: **T1 맥락 전용 기계 기준선**
> (`docs/MULTIPLE_TESTING.md` 분류 — 확증 검정군 아님). INV-03 (b) 병행 파생
> 통계 — 임계·판정 규칙·지표 정의 변경 0, 동결·게시 산출물 접촉 0.

## 0. 리뷰어 주장과 현행 기록의 차이 (사실 정정)

- 주장: "Dechow F-score(2011), Beneish M-score 비교군 부재."
- 사실: B1/B2는 **사전 등록**(`analysis/ANALYSIS_PLAN.md` §5, commit 5f4ca65) ·
  **구현**(`scoring/baselines/screens.py`, 단일 원천) · **게시**(RESULTS.md 행 12:
  wave-1 Beneish M p 0.498 / AUC 0.510, Dechow F p 0.268 / AUC 0.573; wave-2는
  R2 판정용 ρ·잔차 검정만) 상태다. 부재한 것은 (a) wave-2·holdout 티어에서의
  스크린 **자체 분리도**, (b) **동일 계산 가능 부분집합** 위 LLM 대 스크린의
  짝(paired) 비교, (c) 동결 임계 기준 탐지/오탐/정밀도 표, (d) README 헤드라인
  노출이다. 본 스펙은 (a)–(c)를 계산하고 (d)를 결과 커밋에서 반영한다.
- "B4 단기 공매도 베이스라인은 식별됨이지 구현 안 됨"도 부정확 — B4는 구현·실행
  완료(`analysis/results_b4.json`, `specs/B4_short_interest.md`)이며 비교 성립
  tier가 0인 이유는 커버리지(wave-1 3/30 · wave-2 4/32)다. 전향 봉인에서만 성립.

## 1. 입력 — 전부 커밋 산출물 (신규 모델 호출 0 · 신규 fetch 0)

| 입력 | 파일 | 비고 |
|---|---|---|
| LLM 점수 wave-1 (30) | `analysis/unified_table.csv` `llm_score`(원본 프레임) · `llm_perturbed`(교란 프레임, T 8) | E-003 재생성본 |
| LLM 점수 wave-2 (32) | `analysis/unified_table.csv` `llm_score` | 원본 프레임 (RESULTS 행 3) |
| LLM 점수 holdout T (3) | `analysis/unified_table.csv` holdout 행 | HUBG 70 · WMK 32 · GNE 42 |
| LLM 점수 holdout C (9) | `analysis/holdout_controls_results.json` `per_case_side_by_side.*.matched_controls` | E1 프레임 (RESULTS 행 6) |
| 스크린 값 wave-1·wave-2·holdout T | `analysis/unified_table.csv` `m_score`·`f_score` | 게시 기록 그대로 (byte 무변경) |
| 스크린 값 holdout C (9) | **신규** `analysis/out/b1b2_cross_tier/screens_by_case.json` | stage-1이 동결 `screens.run_case`로 산출 (컷오프 = `data/candidates/candidates_holdout_controls.json`, `filed <= cutoff` PIT) |
| 그룹 라벨 | `unified_table.csv` `group`; holdout C = control | — |

stage-1(`analysis/b1b2_screens_all_tiers.py`, 코퍼스 의존 — `make verify-full`)은
74사 전부를 재계산해 unified_table 값과의 **일치 여부를 기록**한다(재현성 점검).
불일치 시 게시 기록 값이 우선하고 불일치는 REPORT에 공개한다 — 침묵 대체 금지.
stage-2(`analysis/b1b2_cross_tier.py`, 공개 tier)는 커밋 산출물만 읽는다.

## 2. 프레임 (사전 고정 — 티어 간 pooling 금지)

| 티어 · 프레임 | T | C | LLM 점수 열 | RESULTS 대응 |
|---|---|---|---|---|
| wave-1 **primary** — 교란 T vs 원본 C | 8 | 22 | `llm_perturbed` / `llm_score` | 행 2 (primary reading) |
| wave-1 secondary — 원본 T vs 원본 C | 8 | 22 | `llm_score` | 행 1 |
| wave-2 **primary** — 원본 | 9 | 23 | `llm_score` | 행 3 |
| holdout E1 — 원본 | 3 | 9 | holdout 행 / matched_controls | 행 5·6 |

스크린 값은 프레임과 무관하다 (교란은 LLM 입력에만 적용됐고 스크린은 원본
PIT 데이터로 계산된다) — 따라서 wave-1 두 프레임의 스크린 열은 동일하다.

## 3. 계산 가능 부분집합 · 커버리지 규칙

- 셀 = 티어·프레임 × 스크린 {B1 M, B2 F}. 부분집합 = 해당 스크린 값이 None이
  아닌 케이스. 커버리지 = n_sub / n_tier, 그룹별 병기. 침묵 대체 금지
  (ANALYSIS_PLAN §5 원칙 승계).
- **비교는 항상 동일 부분집합 위 짝 비교** — LLM도 같은 부분집합으로 재계산한다.
  동결 LLM AUC(전체 티어)와 부분집합 스크린 AUC를 직접 비교하지 않는다
  (B4 §6이 회피한 부분집합 불일치 문제).
- 부분집합에서 n_T < 3 또는 n_C < 3 → AUC·CI·순열 p 계산 안 함, 케이스별 표만.
- B4 §6의 70% 헤드라인 커버리지 하한은 짝 비교에는 적용하지 않는다(부분집합
  불일치가 없으므로 근거가 다르다). 대신 커버리지를 모든 셀에 병기하고,
  커버리지 < 70% 셀의 판독 문장에는 "computable-subset only" 표지를 의무화한다.

## 4. 통계 (전부 `aaer_eval/statistics.py`; seed = **20260904** `SEED_B1B2`, 셀별 재시드; B_perm = 100,000 · B_boot = 10,000)

- 스크린 자체 분리: AUC(tie-aware) · 부트스트랩 95% CI(percentile, 그룹별 층화
  재표집) · 단측 순열 p(평균차, `(ge+1)/(n+1)`, MC-SE 병기). 방향: 값이 높을수록
  위험 (M 높음 = 조작 가능성 높음, F 높음 = 위험 높음 — 두 스크린 모두 상방).
- LLM 동일 부분집합: 동일 3종.
- 짝 차이 **ΔAUC = AUC_LLM − AUC_screen**: 층화 짝 부트스트랩 — 재표집마다 두
  AUC를 **같은** 재표집 표본에서 계산 — percentile 95% CI. 신규 헬퍼
  `boot_paired_auc_diff_ci` (단위 테스트 포함).
- Spearman ρ(LLM, screen) 부분집합 값 (참고 — R2 판정은 rev2 값 그대로).
- 임계 표: 스크린 플래그 **M > −1.78 (1차) · M > −2.22 (2차)** ·
  **F ≥ 1.0 (1차) · F ≥ 1.4 (2차)** — `docs/baseline_screens.md`·ANALYSIS_PLAN §5
  동결 임계 재사용, 새 임계 발명 없음. LLM 플래그 **≥ 50** (동결 루브릭 임계).
  셀별 탐지 k/n_T · 오탐 k/n_C · 정밀도 TP/(TP+FP) — 전부 **정확 Clopper–Pearson
  95%** (FP=0 포함; rule-of-three를 CP95로 표기하지 않는다 — D-P92 교훈).

## 5. 판독 규칙 (사전 등록 — 결과 보기 전 고정)

1차 셀 = {wave-1 primary, wave-2 primary} × {B1, B2} = 4셀. 셀별 ΔAUC 95% CI:

- **(A)** 하한 > 0 → "동일 계산 가능 부분집합에서 LLM 점수가 스크린보다 분리도가 높다"
- **(B)** 0 포함 → "이 N에서 LLM과 스크린을 구별할 수 없다"
- **(C)** 상한 < 0 → "스크린이 LLM보다 분리도가 높다"

- 티어 간 합산·풀링 금지. secondary 프레임·holdout·임계 표·ρ는 맥락 전용.
- 어떤 판독도 RESULTS 행 1–13, R1–R4 판정, 게시 수치를 바꾸지 않는다.
- 문구 제약 (Level 2, `docs/CLAIM_HIERARCHY.md`): "이 선택 표본 · 이 PIT 데이터 ·
  계산 가능 부분집합에서"만 허용. "LLM이 기존 방법보다 낫다"류 일반 문장 금지
  (R4 프레이밍 제약 승계).

## 6. 부속 — 이름-식별 제외 민감도 (S-NID; 리뷰 항목 4)

- wave-2: `recognized == True` (동결 `name_match` 규칙, 7/32 = T 3 · C 4) 제외 →
  **6 T vs 19 C**. wave-1 원본·교란 프레임: `recognized` 15/30 (T 3 · C 12) 제외 →
  **5 T vs 10 C**.
- 통계: §4의 AUC·CI·순열 p. **판독 분기 없음** — 민감도 보고 전용. 어떤 결과도
  게시 판정을 바꾸지 않는다.
- 결과와 무관하게 게시할 문장: 결과-지식 프로브(RESULTS 행 3, wave-2 T 8/9
  knows_event) 기준으로 제외하면 T = 1 → 계산 불능. **잔여 암기는 부분집합화로
  제거되지 않는다** — 구조적 제거는 컷오프 이후 층(holdout N=3)과 전향
  사이클(Level 3)에서만 성립한다.

## 7. 산출물 (신규 경로만 — INV-06)

- `specs/B1B2_CROSS_TIER.md` (본 문서, freeze 커밋)
- `analysis/b1b2_screens_all_tiers.py` → `analysis/out/b1b2_cross_tier/screens_by_case.json` (코퍼스 tier)
- `analysis/b1b2_cross_tier.py` → `analysis/out/b1b2_cross_tier/results.json` · `REPORT.md` (공개 tier)
- `analysis/test_b1b2_cross_tier.py` · `aaer_eval/statistics.py` 헬퍼 1건
- 표면: RESULTS.md 행 14 (head-to-head) · 행 15 (S-NID) + `CLAIMS.json` 14·15,
  README 헤드라인 문장, `docs/methodology_limitations.md` L-13.
- 접촉 0: `analysis/baseline_table.csv` · `results_stats.json` · `wave2_results.json` ·
  `unified_table.csv` · `scoring/baselines/results/` · `scoring/baselines/screens.py`.

## 8. 테스트 계약

1. 결정론: 같은 seed로 두 번 실행 → 동일 `results.json`.
2. 재계산 게이트(공개 tier): 커밋 `results.json` 대비 순열 p ±3e-3 · CI ±2e-2
   (`tools/test_recompute_published.py` 관행), 정수·정확값은 동일.
3. 임계 잠금: 소스에 −1.78 · −2.22 · 1.0 · 1.4 · 50 상수 존재, 다른 임계 없음.
4. 부분집합 규칙: n_T < 3 또는 n_C < 3 셀에는 `stats` 키 없음.
5. 짝 부트스트랩 헬퍼: 동일 점수 두 벌 → Δ = 0, CI [0, 0]; 완전 분리 vs 상수 →
   CI 하한 > 0.
6. 스크린 값 무변경: `results.json` 부분집합 케이스의 m/f 값 = `unified_table.csv`
   값 (문자열 동일).

## 9. 한계 (사전 명시)

- 커버리지: wave-2 F 17/32 · M 20/32, holdout T M 1/3 · F 2/3, holdout C는
  stage-1 실측치 — 계산 가능 부분집합은 태깅 관행(금융·REIT·서비스 필러의
  총부채·COGS·SG&A 미태깅)에 따라 **비무작위**다. 부분집합 편향 방향 미지.
- 스크린은 동결 구현 그대로다. 커버리지 개선(총부채 = 부채자본합계 − 자본 유도,
  수취채권 태그 사다리 확장)은 게시 행 12 값을 바꾸므로 ERRATA·소유자 항목
  경로(Q-F25)로만 한다.
- 선택 표본·생존 편향·case-control 기저율 한계는 L-8·`docs/POWER_ANALYSIS.md`를
  승계한다. Level 2 이상 주장 불가.
- 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
  채점: Claude 보조 + 인간 최종 확정. 포지션 없음 · 교육·정보 목적 · 투자 조언 아님.
