# 교차-웨이브 종합 (P2) — 암기 dose-response + 통합표 + 웨이브별 규칙

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08.
> 재현: `python analysis/synthesis.py` (결정론, seed 20260708) → `synthesis.json` +
> `unified_table.csv` + `fig_memorization_doseresponse.png`. 동결 함수만 재사용
> (probe_verdict.name_match · screens.run_case · stats.auc/boot_auc_ci) — 재채점 없음.
> **범위 한정(§5-5)**: Claude 단일 파이프라인(claude-sonnet-5 핀) 한정.

## 1. 암기 dose-response (핵심 그림) — 2축 병기 (D34/D35)

| tier | name-ID(암기 대리)¹ | outcome-knowledge(직접)² | 분리 AUC (부트 95% CI) | 규칙 |
|---|---|---|---|---|
| wave-1 (유명) | **50.0%** | 미측정 (후속 사이클) | **0.824** [0.599, 0.983] | R3 (암기 얽힘) |
| wave-2 (덜 유명) | **21.9%** | **88.9%** (8/9, CP [51.7%, 99.7%]; 대조군 **0/23** CP [0%, 14.8%]) | **0.829** [0.616, 0.983] | R4 (잔여 능력) |
| 홀드아웃 (컷오프후·암기불가) | **0.0%** (recognition gate 0/3) | **0%** (gate 3/3 비인지, k=5 재검 0/5×3) | N=3, AUC 불가 — per-case HUBG 70·GNE 42·WMK 32 | H2 |

² **outcome-recognition 프로브 (2026-07-10 실행, 사전 등록 D34 — branchless, R/H
판정 입력 아님)**: 실명 노출 하 knows_event 계기(홀드아웃 게이트와 동일 문구).
`analysis/outcome_recognition_results.json`. **두 계기는 채널이 다르다** — name-ID는
익명 페이로드에서 이름 복원(대리), knows_event는 실명 노출 하 사건 상기(직접).
§reconcile: 실험군 9 중 **event_only 5** (BRX·CGI·MDXG·TNGO·WFT — 익명 페이로드에서
이름은 복원 못 하나 실명을 주면 사건을 앎) = name-ID 계기의 거짓음성 방향 실증
(methodology_limitations §Instrument bias directions 1행). **정직 판독**: "wave-2는
덜 암기됨(wave-1의 절반)" 서사는 **name-ID 계기에 한정**된 서술이다 — 직접 계기로는
정체-노출 프레임(발행 1차 프레임)에서 실험군 8/9의 사건 지식이 가용했다. 직접
계기로 정렬한 축은 **wave-2 88.9% → 홀드아웃 0%** — 암기 제거는 wave-1→wave-2
사이가 아니라 **wave-2→홀드아웃 사이에서 일어난다**. R4는 불변 (R4의 입력은
perturbation dominance 3/9이지 본 프로브가 아님 — 사전 등록 무분기).

**판독 (백본 = standalone 유의성)**: 암기 대리지표(name-ID)가 50% → ~22% → 0%로
반감·소멸하는 동안, **각 wave의 standalone 순열 유의성이 독립 생존한다** — wave-1
p=0.00114 · wave-2 p=0.00116 — 그리고 암기가 구조적으로 불가능한 홀드아웃에서도
가장 misstatement-like한 HUBG를 70으로 탐지(E1 매칭 대조군 상회 + 5-draw robust,
2026-07-09). ⇒ **분리는 암기로 설명되지 않는다** — Issue #0의 R3 헤드라인("분리의
일부는 암기, 일부는 분석")을 암기 제거 축에서 독립 확증. **2차 gradient 관찰**:
AUC 0.824 [0.599, 0.983] → 0.829 [0.616, 0.983]는 점추정이 나란하다는 관찰일 뿐,
**CI 폭이 동등성 주장을 금지한다** (N=30·32 부트스트랩). 세 표본은 시대·유명도·라벨
tier가 달라 **통제 실험이 아니라 gradient 판독**이다.

¹ **name-ID 21.9%는 동결 `name_match` 규칙값(7/32)**. wave2_summary 산문의 25%(8/32)는
단일 경계 케이스 DAR(구명 "Darling International" 미처리)를 사람이 인식으로 계수한 값.
발행 규약 선택 = OWNER_QUEUE Q-E02. 어느 값이든 반감 서사 불변. 상세: `synthesis.json`
§wave2_name_id_reconcile.

## 1b. 정체 3-arm 방향 실험 (D36/D37, 2026-07-10 — 사전 등록 판독 그대로)

wave-2 실험군 9사: (a) 익명(동결 교란) · (b) **가공 사명**(동일 교란 페이로드에
실존-충돌 전수 스크린 통과 가공 이름만 중첩, 신규 9호출) · (c) 실명(동결 원본).
결과 (`analysis/identity_3arm_results.json`): **median(b−a) = +6.0pp ·
median(c−b) = −2.0pp** (부호검정 p=0.07/0.73, 병기 전용¹ᵇ) → 사전 등록 분류 **(ii)**:
"**암기의 점수 기여가 작다는 방향 증거 (a≈b≈c). N=9 방향 증거.**" — 인과 확정
서술 금지(사전 프레이밍 제약), R3/R4/H 판정 불변.

- **1차 증거 = b−a (+6.0pp)**: 동일 교란 페이로드에 이름 토큰만 다르다 — 이 설계에서
  **유일한 깨끗한 인과 대비**다.
- **2차 관찰 = c−b (−2.0pp)**: arm (c)는 실명과 함께 **실수치(원본 스케일)까지 복원**
  되므로, (b) 가공명+교란 대비는 **정체 효과와 스케일 복원 효과가 혼입(confounded)된
  비교**다 — 단독 해석 금지, 병기 전용 (L-7).
- **해상도 한계**: (a)·(c)는 과거 동결 draw, (b)는 신규 draw — arm 간 비교는 draw
  잡음을 포함한다 (케이스당 5-draw 밴드 12–18pp ≈ ±10pp, E5 §7 실측
  `holdout_redraw_results.json`). ±6pp median은 그 해상도 내의 방향 판독이다.

D35의 outcome-knowledge 8/9와 겹쳐 읽으면: 모델은 실명 하에서 사건을 대부분
알지만(§1 2축), 그 지식이 wave-2 점수를 가공명 대비 끌어올리지 않았다 — 두 측정은
서로 독립 계기이며 종합 해석은 소유자 검토 대상.

¹ᵇ 정직 교정 (D39): 본 문단 초판(D37)의 부호검정 병기값 "p=0.18/1.0"은 전사 오류
— 동결 기계 판독(`identity_3arm_results.json`)은 b−a p=0.0703 (7/8 양positive) ·
c−b p=0.7266이다. JSON 정본 채택; 분류 (ii)·median 값은 불변 (판정 입력은 10pp 바의
median뿐, 부호검정은 애초 병기 전용).

## 2. 통합 점수표 → `unified_table.csv` (65행)

전 실험군·대조군(wave-1 30 + wave-2 32 + 홀드아웃 3) 1행/사, 열: wave · ticker · group ·
llm_score · flag(p≥50) · llm_perturbed · perturb_delta · recognized(동결규칙) · m_score ·
m_flag(≤−1.78) · f_score · f_flag(≥1). M/F는 동결 `screens.run_case`(오프라인) 실측.

- 기계 기준선의 한계 재확인: 홀드아웃 HUBG는 M/F **계산불능**(결측)인데 LLM은 70 탐지 →
  LLM 신호는 Beneish/Dechow 복제가 아님(R2·H2 정합).

## 3. 웨이브별 발동 규칙 (자동 흐름)

- wave-1 = **R3**(암기 얽힘) · wave-2 = **R4**(잔여 능력) · 홀드아웃 = **H2**(per-case, N=3).
- **E3 의존**: wave-2 규칙은 E3(교란 재추첨) 확정 시 사전 등록 규칙에 따라 자동 갱신 —
  median-delta dominance ≥5/9면 R3가 R4를 supersede(그때 본 표·그림·Issue 자동 갱신).
  현재 단일 draw 기준 3/9 → R4. (E3 미실행: launch-ready.)

## 4. 3층 서사 (Issue #0/#1/#2 공통 골격)

유명 사건(wave-1) → R3 암기 얽힘(점수 팽창) → 덜 유명(wave-2) → R4 잔여 능력(name-ID
반감) → 컷오프후 홀드아웃(암기 불가) → 신호 약화하나 붕괴 아님(HUBG는 M/F가 계산조차
못한 곳에서 탐지). **"bounds, not eliminates"** — 암기를 제거할수록 점수는 내려가되
신호는 잔존.

## 5. 면책

단일 Claude 파이프라인 한정, 채점 Claude 보조 + 인간 확정 대기. 대조군="비집행"(무결
아님). 홀드아웃 G2 provisional. 통제 실험 아님(표본 이질) — gradient 방향 증거.
