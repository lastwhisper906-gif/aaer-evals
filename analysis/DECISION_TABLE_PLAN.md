# DECISION_TABLE_PLAN — 임계·결정 표 사전 등록 (freeze-commit-then-run)

> **사전 등록 문서.** 이 문서는 계산 실행 전에 단독 커밋된다 (커밋 타임스탬프가
> 증거). 계산 코드(`analysis/decision_table.py`)와 산출물
> (`analysis/decision_table.json`, `analysis/DECISION_TABLE.md`)은 이 문서
> 커밋 이후에만 작성·커밋한다. 실행 후 본 문서의 정의 변경 금지 (변경 시
> PROJECT.md §5-6 이력 공개).
>
> **미터링 0 계약**: 신규 API 호출 0. 입력은 전부 동결(frozen) 커밋 산출물.
> `runs/` 트리는 읽기 전용 — 어떤 파일도 수정·추가하지 않는다.

## 1. 목적

"p=0.0021 유의성"을 구매자 언어로 번역한다: **임계 T에서 탐지 X/N ·
오탐 Y/M [CP 95%] · 탐지당 비용 $Z**. 신규 실험이 아니라 동결 점수의
재집계다.

## 2. 입력 (전부 동결 경로 — 읽기 전용)

| 레이어 | 실험군(T) 점수 | 대조군(C) 점수 | 라벨 출처 |
|---|---|---|---|
| L1 wave-1 perturbed | `runs/perturbed/case_{01,02,03,06,08,09,12,13}.json` (n=8) | `runs/main/case_{04,05,07,10,11,14,15,16}.json` (n=8) — **프레임 비대칭 주의** ①| `scoring/id_mapping.json` (T*/C* 접두) |
| L2 wave-2 | `runs/wave2/scores/*.json` 중 fraud 9 | 동일 디렉토리 나머지 23 | `runs/wave2/fraud_case_ids.json` |
| L3 holdout + E1 대조군 | `runs/holdout/scores/case_{71,72,73}.json` (n=3) — **G2 잠정 라벨 주의** ② | `runs/holdout/controls/scores/hc_{01..09}.json` (n=9) | `data/evaluatee/cases_holdout.json` (G2 provisional) |
| L4 E2 궤적 | `analysis/e2_trajectories.json` treatment 12 | 동일 파일 control 7 | 파일 내 `group` 필드 |

- ① wave-1 perturbed 프레임은 실험군 8건만 채점되어 있다 (대조군 perturbed
  미채점 — OWNER_QUEUE Q-M06과 동일 사실). L1의 FPR 열은 **wave-1 original
  프레임 대조군**을 사용하며, 표에 프레임 비대칭을 명기한다. 신규 채점으로
  메우지 않는다 (미터링 0).
- ② holdout 3건의 라벨은 "G2 provisional — restatement/non-reliance events,
  NOT fraud". L3의 "탐지" 열은 fraud 탐지가 아니라 **잠정 라벨 이벤트 플래깅**
  이며 표에 이 명칭을 그대로 쓴다.

## 3. 그리드와 셀 정의

- **임계 그리드**: T ∈ {40, 50, 60, 70} (LLM `misstatement_probability`,
  0–100 서수 점수 — RP-16/Q-F04의 서수 규약과 일관되게 "확률"로 서술하지
  않는다).
- **플래그 규칙**:
  - L1–L3 (단일 스냅샷 레이어): 케이스 플래그 ⇔ score ≥ T.
  - L4 (궤적 레이어): 케이스 플래그 ⇔ **어느 스냅샷이든** `llm_p` ≥ T
    (buyer_metrics §2와 동일 의미론). `llm_p`가 null인 스냅샷은 계산에서
    제외(fail-closed)하고 제외 건수를 산출물에 기록한다 (대조군 j=0 null —
    D71 규약).
- **셀 내용**: 탐지 X/N_T [CP 95%] · 오탐 Y/N_C [CP 95%]. **점 추정 단독
  표기 금지** — 모든 비율에 Clopper–Pearson 95% 구간 병기. CP 구현은 동결
  `analysis/holdout_controls_analyze.clopper_pearson` import 재사용 —
  **신규 통계 코드 0**.

## 4. 비용 축

- 스크린당 비용 = **$0.5304** (`analysis/BUYER_METRICS.md` §3 실측 인용 —
  재측정·재계산 없음. E2 실측 토큰, sonnet-5 목록가 $3/$15, 캐시 과금 등가
  가중 포함).
- 레이어·임계별 **탐지당 비용** = (레이어 스크린 수 × $0.5304) / 탐지 수 X.
  - 스크린 수: L1–L3 = 채점된 케이스 파일 수 (T+C), L4 = `llm_p` 비-null
    스냅샷 수.
  - X = 0이면 "—" (정의 불능; 0으로 나누지 않는다).
- 비용은 **탐지 비용이지 정탐 비용이 아니다** — 오탐 열과 같은 표에 놓는
  것이 이 표의 존재 이유다.

## 5. 결합 규칙 후보 (EXPLORATORY — 성능 주장 금지)

- 정의: L4 궤적에서 케이스 플래그 ⇔ **동일 스냅샷**에서 `b3_score` ≥ 2 AND
  `llm_p` ≥ T (T는 §3 그리드).
- **지위**: 동결 데이터를 열람한 뒤 세운 사후(post-hoc) 규칙이므로 어떤
  소급 성능 주장도 할 수 없다. 산출물 전 표면에 EXPLORATORY 라벨 의무.
  용도는 단 하나 — **Cycle-2 사전 등록 후보** (docs/FUTURE_CYCLE_PROTOCOL
  부록에 등록, sealed 전향 검증 대상).
- 계산·표기는 하되 본문 결론·README·발행 표면에서 성능 근거로 인용 금지.

## 6. 산출물과 게이트

1. `analysis/decision_table.py` + `analysis/test_decision_table.py`
   (합성 픽스처, 무호출) — 입력은 §2 동결 경로만.
2. `analysis/decision_table.json` — 전 셀 수치 + 제외 건수 + 입력 파일 목록.
3. `analysis/DECISION_TABLE.md` — 독자용 **계단식 표만** (연속 곡선 작도
   금지 — N이 작아 과장됨). 각 표에 n 명기. 말미에: PROJECT.md §5-5 범위
   한정 문구 + "채점: Claude 보조 + 인간 최종 확정" + "본 표는 서명 전
   초안(unsigned draft)".
4. README 링크는 **사전 등록 커밋 → 계산 → 소유자 서명** 이후에만 (별도
   커밋). 서명 요청은 OWNER_QUEUE에 등록.

## 7. 범위 한정

본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
대조군은 "비집행"이지 "깨끗함 확정"이 아니며(EARLINESS_PLAN §7), 모든
수치는 §2 커버리지 안에서만 정의된다 — 유니버스 일반화 금지.
