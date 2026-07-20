# governance/FEEDBACK_RESPONSE_v1.md — 외부 피드백 대응 일괄 사전 등록 (D106)

> **Authored by Claude Code, pending human audit** (D15 규약).
> 2026-07-20 작성. status: **SIGNED — D106 발효 (owner, 2026-07-20)**.
> 원장 등재: `scoring/decisions_log.md` D106 (본 문서 §10과 동일 문면 —
> 본 문서가 원문). 이 커밋의 타임스탬프가 사전 등록의 증거다
> (freeze-commit-then-run, GA-001 (c)). 서명 이후 본 문서의 수정은 동결
> 규약 적용 — 신규 D-엔트리 전용 (§8-4).

본 결정의 동기가 된 외부 피드백이 존재한다 (2026-07-20 수신) — 원문은 본
문서에 재수록하지 않으며, Tier-3 피드백 로그 규약(D105) 경로에 보관한다.

## 0. 우산 결정의 성격과 공통 경계

7개 항목을 **단일 번호(D106)의 일괄 사전 등록**으로 묶는다. 목적: 후속
작업이 항목마다 개별 거버넌스 결정을 재생산하는 것(governance churn)의
방지 — 각 항목의 실행 산출물은 D106을 authority로 인용하고, 신규 D-엔트리
는 사전 등록 범위를 **벗어나는** 변경에만 요구된다.

**공통 OUT (전 항목 적용, 어떤 항목도 이를 무효화하지 못한다):**

- v1 동결 산출물·게시된 수치·과거 거버넌스 기록의 수정 금지 (CLAUDE.md §2).
- 소급 지표 변경 금지 — 어떤 항목도 동결된 FPR·AUC·precision·κ 등
  발행 지표를 재계산·재정의하지 않는다.
- 게시된 역사 텍스트의 수정은 소유자 서명 diff 전용 (RP-15/16 선례).
- 모델 호출·지출이 필요한 실행은 본 결정으로 승인되지 않는다 — 발사는
  전건 별도 spend gate (D103 선례: 경로 승인 ≠ 발사 승인).

---

## 1. SCHEMA_V2_RENAME — D100 등록 재확인 (지배 등록 = RISK_SCORE_SEMANTICS)

- **지배 등록 선언**: 전향 필드 명명·의미론의 지배 등록(governing
  registration)은 **D100 / `specs/RISK_SCORE_SEMANTICS.md`**다 — 확정명
  `misstatement_risk_score`, 서수 해석 규약·4필드 구조·의무 문구 전부
  포함. **본 항목은 D100을 대체(supersede)하지 않는다** — 재확인
  (reaffirm)만 한다. D100과 본 항목이 충돌하는 것으로 읽히는 경우 D100이
  우선한다.
- **D106 고유 스코프 (이 항목이 새로 성립시키는 것은 아래 3건뿐)**:
  - (a) **확률 언어 발행 lint 규칙**: 발행 주장 전면에서 확률 언어(%,
    "probability", "likelihood") 사용 금지 — 보정 연구가 **사전 등록되고
    통과하기 전까지** (재보정 하한 N ≥ 150, calibration_scope §4-2
    기고정). lint 규칙 J의 기계 차단 범위를 발행 주장 전체로 유지·확대.
  - (b) **v1→v2 호환 심(shim)**: 재현 코드 호환을 위해 레거시 키
    `misstatement_probability`를 `misstatement_risk_score`로 매핑하는
    호환 계층 1건 — v1 동결 산출물 자체는 **무수정**.
  - (c) **스키마 수준 description 문언**: v2 스키마의 해당 필드
    description을 다음 문언으로 고정 — "Uncalibrated ordinal risk score,
    0-100. Not a probability."
- **독해 규칙**: 소유자의 후속 phase 지시문에 등장하는 `risk_score` 표기
  는 전부 `misstatement_risk_score`로 읽는다 (2026-07-20 소유자 지시 —
  본 항목이 그 독해 규칙의 등록이다).
- **IN**: 위 (a)(b)(c) 3건과 독해 규칙.
- **OUT**: `specs/RISK_SCORE_SEMANTICS.md` 수정 (불요 — 지배 등록 그대로),
  `schemas/llm_output.json` v1.2의 필드명 (커밋 출력 재현성 —
  calibration_scope 범위 선언 승계), v1 동결 산출물·게시 수치 전부,
  소급 재채점.

## 2. ERROR_ATLAS_v1 — 회계 오류 아틀라스 확약

- **결정**: wave-1·wave-2·holdout **전 실험군 케이스 + 전 오탐(false
  positive)**을 포괄하는 Accounting Error Atlas를 산출한다. 기반 템플릿 =
  `output/GIL_memo_v1.md` 구조 (헤더 고지·사실/가설 분리·verbatim 인용 +
  기계 검증표·verification path·confidence-would-change-with).
- **성격 선언**: 아틀라스 엔트리는 **분석 문서(analytical document)**이지
  채점 산출물이 아니다 — 어떤 동결 지표도 변경하지 않으며, 채점 레코드에
  기입되지 않고, 지표 재계산의 입력이 되지 않는다.
- **IN**: 케이스별 아틀라스 엔트리 작성(동결 채점 레코드·동결 원장 인용은
  읽기 전용 소스), 오류 귀속 3분류(§5-3)의 서사적 부연, GIL 템플릿의
  구조 차용.
- **OUT**: 재채점·등급 변경·지표 재계산 전부, 동결 grades*/ 파일 접촉,
  현재 기업 어휘 규율 위반(§6 — 아틀라스가 현재 기업을 언급할 경우 자동
  적용), 신규 성능 주장 (아틀라스는 기존 동결 결과의 해설이다).

## 3. CONTROL_STRATIFICATION_v2 — 미래 사이클 대조군 규격

- **결정**: **모든 미래 사이클**에서 음성 대조군(negative control)은 ①
  명시적 청정성 체크리스트(cleanliness checklist)에 대한 문서화 ② 가능한
  범위에서(where feasible) 산업(2-digit SIC)·규모 밴드·회계기간 매칭 —
  두 요건을 충족해야 한다.
- **체크리스트 정의의 위치**: 청정성 체크리스트의 항목 정의는 owner plan
  2026-07-20 Phase 4가 지정하며, 후속 companion 문서
  (`docs/CONTROL_CRITERIA_v3.md` 예정)로 커밋한다 — **미래 사이클의 어떤
  대조군 선정보다 먼저 커밋**되어야 효력이 있다 (freeze-commit-then-run).
  본 항목은 요건의 존재를 사전 등록하는 것이며 체크리스트 내용 자체를
  확정하지 않는다.
- **IN**: 미래 사이클 대조군 선정 절차, CONTROL_CRITERIA_v3 작성,
  "where feasible" 판정의 문서화 의무 (매칭 불가 축은 사유와 함께 기록).
- **OUT**: 기존 대조군 집합(백테스트 wave-1/wave-2/holdout controls)과
  그로부터 발행된 FPR 전부 — **무변경**. 기존 선정 근거 문서
  (D17, CONTROL_CRITERIA v1/v2)의 소급 개정 없음.

## 4. TASK_SEPARATION — 3개 벤치마크 태스크의 공개 분리

- **결정**: 공개 문서는 다음 3개 태스크를 **명시적으로 구분된 별개
  벤치마크**로 제시하고, 태스크 간 성능 주장을 집계(aggregate)하지 않는다:
  - (a) AAER 집행 연계 회고 벤치마크 (historical, enforcement-linked)
  - (b) 재작성(restatement)/Item 4.02 비신뢰 조기 경보 벤치마크
  - (c) 탐색적 earnings-quality 모니터링 (exploratory)
- **집계 금지의 의미**: (a)의 정밀도와 (b)의 조기성(earliness)과 (c)의
  플래그를 합산·평균·혼합 인용한 단일 성능 문장을 만들지 않는다. 각
  주장은 소속 태스크와 `docs/CLAIM_HIERARCHY.md` 레벨을 명시한다 (lint
  규칙 K와 정합).
- **IN**: README 양어·발행 표면·미래 Issue 문서의 태스크 구분 서술 정비
  (게시된 역사 텍스트는 소유자 서명 diff 전용 — 공통 OUT).
- **OUT**: 각 태스크의 동결 지표 자체, 태스크 정의의 소급 재분류
  (기존 케이스의 태스크 소속은 동결 기록 그대로).

## 5. CONTRIBUTION_STATEMENT — 상비 AI-인간 기여 표

- **결정**: README에 AI-vs-인간 기여 표(standing contribution table)를
  추가하고 **최신 상태로 유지**한다. 내용 기준: PROJECT.md §7 협업 모델
  (Claude 전담 / Claude 1차 + 소유자 서명 / 소유자 확정)과 D15 저자 표시
  규약의 표 형식 공개 — "채점: Claude 보조 + 인간 최종 확정" 명시 의무
  (§5-5)의 구조화.
- **IN**: README 양어 기여 표 신설, 이후 워크플로 변경 시 갱신 의무.
- **OUT**: 과거 산출물 저자 표시의 소급 수정 (기록 그대로), 인간 예측·
  서명 기록의 날조 금지 (D15 — 표는 실제 분담의 기술이지 목표 서술이
  아니다).

## 6. EXTERNAL_SURFACE_v1 — 실무자용 단문 브리프

- **결정**: 연구 문서 밖에 별도의 실무자용 브리프(practitioner brief,
  **≤5쪽**)를 작성한다. **신규 주장 0** — 브리프의 모든 수치는 동결
  산출물 또는 재현 스크립트로 추적 가능해야 한다(trace 의무). 추적 불가
  수치는 게재 불가.
- **IN**: 브리프 1건 작성(발행 표면으로 등록 — lint 규칙 J/K 적용 대상),
  §5-5 범위 한정 문구·§6 법적 안전 규칙(해당 시)·포지션 없음 고지·면책
  문구 포함.
- **OUT**: 신규 분석·신규 수치·신규 성능 주장 전부, 연구 문서 본문의
  변경, 게시(dispatch) 자체 — 게시는 소유자 전용 (D92/D93 선례).

## 7. GRADER_INDEPENDENCE_v1 — 교차 패밀리 채점 프로토콜 확약

- **결정**: **차기 봉인(sealed) 사이클**에 교차 패밀리 채점(cross-family
  grading) 프로토콜을 실행할 것을 사전 등록한다. 상세 설계는 companion
  스펙으로 이관한다 (`specs/cross_grader.md`의 스팟체크 설계를 기반으로
  확장) — **본 결정은 실행 확약만을 성립시킨다.**
- **IN**: 실행 확약(차기 봉인 사이클), companion 스펙의 작성·동결.
- **OUT**: 채점자 모델 지명·표본 규모·지표 판독 규칙 등 상세 전부
  (companion 스펙 몫 — cross_grader.md 선례: 모델 지명은 실행 시점
  소유자 게이트), 호출·과금 승인 (별도 spend gate), 기존 사이클의 동결
  채점 레코드 소급 재채점.

---

## 8. 발효 조건과 후속 절차

1. 소유자 서명 (§9) → D106 발효.
2. 발효 시 `scoring/decisions_log.md`에 §10 엔트리 등재 [COMMIT].
3. 항목 3의 CONTROL_CRITERIA_v3, 항목 7의 companion 스펙은 발효 후
   별도 커밋 —
   각각 D106을 authority로 인용하며 신규 D-엔트리 불요 (§0 취지).
   단, 본 문서의 IN/OUT 경계를 벗어나는 내용이 필요해지면 그 시점에
   신규 D-엔트리를 요구한다.
4. 서명 전 본 문서의 수정은 자유 (초안 상태). 서명 후 수정은 동결 규약
   적용 (신규 D-엔트리 전용).

## 9. 서명란

FEEDBACK_RESPONSE_v1 / D106: SIGNED (owner, date: 2026-07-20 — 본 세션
소유자 지시 "D106 서명 발효" verbatim; D101–D105 서명 형식 선례)

## 10. 원장 엔트리 (2026-07-20 발효 — decisions_log.md 등재 문면)

{"decision":"D106","date":"2026-07-20","action":"FEEDBACK_RESPONSE_v1 우산 사전 등록 발효 — ① SCHEMA_V2_RENAME: D100/RISK_SCORE_SEMANTICS를 지배 등록으로 재확인(대체 없음, 충돌 시 D100 우선) — D106 고유분은 (a) 확률 언어 발행 lint (b) v1→v2 호환 심 misstatement_probability→misstatement_risk_score (c) v2 description 문언 'Uncalibrated ordinal risk score, 0-100. Not a probability.' + 후속 지시문 risk_score 표기의 misstatement_risk_score 독해 규칙 ② ERROR_ATLAS_v1: wave-1·2·holdout 전 실험군+전 오탐 아틀라스 확약(GIL_memo_v1 템플릿, 분석 문서 — 동결 지표 무변경) ③ CONTROL_STRATIFICATION_v2: 미래 사이클 대조군 청정성 체크리스트+2-digit SIC·규모·기간 매칭 요건(기존 대조군·FPR 무변경) ④ TASK_SEPARATION: AAER 회고/4.02 조기경보/탐색 모니터링 3태스크 공개 분리·교차 집계 금지 ⑤ CONTRIBUTION_STATEMENT: README 상비 AI-인간 기여 표 ⑥ EXTERNAL_SURFACE_v1: 실무자 브리프 ≤5쪽·신규 주장 0·전 수치 동결 산출물/재현 스크립트 추적 의무 ⑦ GRADER_INDEPENDENCE_v1: 차기 봉인 사이클 교차 패밀리 채점 실행 확약(상세는 companion 스펙). 공통 OUT: 동결 산출물·게시 수치·과거 거버넌스 무수정, 소급 지표 변경 금지, 발사는 전건 별도 spend gate","authority":"owner, 2026-07-20, governance/FEEDBACK_RESPONSE_v1.md §9 서명 (본 세션 소유자 지시 — D101–D105 형식 선례)","motivation":"외부 피드백 수신(2026-07-20) — 원문 비재수록, Tier-3 로그 규약(D105) 경로 보관","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 피드백 대응을 항목별 개별 결정으로 흘리면 각 항목이 저마다의 재량 시점을 갖게 된다 — 우산 사전 등록 하나로 묶어야 '무엇이 변하고 무엇이 동결로 남는가'의 경계가 피드백 수신 직후 단일 시점에 고정된다"}

---

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
