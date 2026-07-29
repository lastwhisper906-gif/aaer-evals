# DIRECTION_CONTEXT

> 소유자 목소리 문서. 출처: 저장소 + 소유자 MEMORY_DUMP (2026-07-29,
> 전권 위임 지시문). 저장소·덤프 어느 쪽도 답하지 않는 질문은 맨 아래
> "OPEN (owner)"에 질문 그대로 남긴다 — 지어낸 답은 없다. 이 파일은
> direction-loop의 H9 보호 대상 — 루프는 읽기만 하고 절대 편집하지 않는다.

## Current priority ordering

1. **궤적 레이어 오탐 71.4%가 과학적 병목 1순위다** — 결정 테이블과 모든
   실무자(practitioner) 주장을 막고 있다 (BN-01, RESULTS.md 행 13).
2. **2026-11-15 첫 sealed forward 사이클이 캘린더 크리티컬 1순위다**
   (BN-02·BN-03).
3. 게시·독자 발송 케이던스(BN-04)는 계속 진행한다.
4. **인프라(이 direction-loop 포함)는 배경 작업이다** — 위 어느 것도
   지연시켜서는 안 된다.

인프라 단서 조항은 루프 자신에게도 명시적으로 적용된다: 과거 커스텀
2-AI 하네스는 codex-plugin-cc 대비 평가에서 거의 전 차원 열세로 판정
났다 — 인프라는 병목 대비 자기 정당화를 통과해야 한다는 것이 상시
교훈이다. 소유자는 병목 직결 작업보다 인프라 다듬기로 흐르는 성향이
문서화되어 있다. **리뷰어의 bottleneck_irrelevant 카테고리는 바로 이
성향을 잡으라고 존재한다 — 공격적으로 발동할 것.**

## Rejected approaches

리뷰어는 아래를 재제안하지 않는다 (한 줄 이유 포함):

- **소박한 AAER 패턴 fraud 예측** — 학계 복제에 불과하고 오염
  (contamination) 교란 미해결. 이 프로젝트의 창립 피벗 자체.
- **에이전트 프레임워크 / 무거운 의존성** — 런타임 의존성은 고정 5개뿐
  (INV-11).
- **교차 벤더 발견-교집합(finding-intersection) 리뷰** — 모델들은 서로소
  결함 클래스를 찾는다 → 교집합 대신 관할 분리(jurisdiction split)로
  대체 (Claude=방향, Codex=정확성).
- **SaaS·직접 수익화** — F-1/OPT 신분이 배제. 경로는 연구 게시 + 고용
  프리미엄이며, 법적 루트는 Lowe v. SEC의 publisher's exclusion.
- **제출 연대기(filing chronology)를 공짜 기준선으로** — 진짜 공짜
  벤치마크는 비정상 공매도 잔고(abnormal short interest, Karpoff/Lou
  2010) → `specs/B4_short_interest.md`.
- **무제한 커스텀 하네스 구축** — 위 인프라 단서 조항 참조.
- **결과를 본 뒤의 임계값 재보정(post-hoc recalibration) 일체** —
  범주적 기각. E2 조기성(earliness) 결과(LLM 리드타임 우위처럼 보였던
  것)가 임계 비대칭 아티팩트(오탐 71.4% vs 0%)로 판명된 것이 근거 —
  FPR-매칭 비교가 비타협인 이유다. 사전 등록된 엔진 변경은 오직
  ENGINE_DECISION v2(FPR-매칭 비교 + 대조군 확장) 경유
  (`specs/ENGINE_DECISION.md`).

## Unwritten reasons

- **대조군 규모**: 기록된 것 — Phase 2 프로브가 실험군 기업 인지 88.9%
  vs 대조군 0/23을 측정했고, ENGINE_DECISION v2가 대조군 **확장**을 사전
  등록해 두었다. 그 이상의 규모 선정 근거: OPEN (아래 Q12).
- 나머지 미기록 사유 질문(Q9·Q10·Q11)은 OPEN — 아래 참조.

## What "good" looks like this quarter

두 목록의 합집합이 이번 분기의 성공 상태다:

- (저장소 기록분) 게시 4종 실행 + 독자 응답 "몰랐던 것" ≥2
  (PROJECT.md §9) + seal 준비 완료.
- (소유자 추가분) **2026-11-15 사이클이 실제로 실행·봉인됨**; 오탐
  71.4%가 **실질적으로 감소했거나, 게시된 결정 테이블에서 정직하게
  성격 규정됨**; 인프라 사이클이 아니라 **케이던스가 지속되고 있음**.
- The repository is READABLE BY ITS TARGET AUDIENCE (US academics and
  practitioners): headline evidence documents in English, a README that
  survives 90 seconds without internal identifiers, an open feedback
  channel, and citation-grade identity (account name, DOI). "Audit-ready
  but unread" fails this quarter regardless of everything else.
- (경계 확정 — D114, 2026-07-29) 위 영어 표면(D29)은 **모든 독자 대면
  문서**로 확장된다: AUDIT_INDEX.md·REPRODUCING.md는 영어 정본 + `.ko.md`
  원본 보존(F-01/F-02 규약), ERRATA.md는 현행 유지(보호·append-only 우선),
  향후 독자 대면 신규 문서는 영어 정본이 기본값이다.

## Standing suspicions

- **잔여 암기 — 계속 의심한다.** 상시 규칙: 헤드라인급 양성 분리 결과는
  FPR-매칭 전까지 유죄 추정으로 다룬다. LLM 분리 자체는 실재한다
  (B3 귀속 0.147 < 0.2)지만 그 원천은 여전히 열려 있고, 미발견
  E2형 아티팩트를 포함할 수 있다.
- **E2급 아티팩트의 일반형**: 임계가 균등화(threshold-equalized)되지
  않은 비교가 있는 곳 어디든 조용한 어긋남을 의심한다. 알려진 사례는
  하네스 핀 불일치(BN-03).
- **정체(identity) 처리**: 3-arm 결과(+6.0pp fictional vs anonymous,
  사전 등록 임계 10pp 미만)가 현행 익명화 입장의 근거다
  (`analysis/IDENTITY_3ARM_PLAN.md`). **익명화 입장을 조용히 약화시키는
  어떤 변경도 플래그할 것.**

## OPEN (owner) — 저장소도 덤프도 답하지 않은 질문 (지어내지 않음)

- Q2. 궤적 레이어 오탐 71.4%는 Cycle-2까지 봉인해 두는 게 방침인가?
  (우선순위 1이라는 답은 위에 있으나, "Cycle-2 전 개입 금지"인지는 미답.)
- Q3. 2026-08-18 Stony Brook 이동 전후로 주당 투입 시간이 어떻게
  바뀌는가? 8월 중순 이후를 "유지 모드"로 봐야 하나?
- Q5. FREEZE_REV3 raw-API(종량) 경로는 영구 기각인가, 조건(예: 구독
  quota 부족) 하에 재개 가능한 보류인가?
- Q6. 타 LLM 벤치마크 금지 vs 교차 패밀리 채점자(Q-F07) 구분 — 전자는
  기각, 후자는 게이트 안내가 맞는가?
- Q9. 피평가자 핀이 claude-sonnet-5인 이유(비용? 재현성? 시점 고정?).
- Q10. 발행 표면을 GitHub Issues로 정한 이유 (블로그·논문 대비).
- Q11. 첫 seal 날짜를 2026-11-15로 정한 근거.
- Q14. PROJECT.md §9의 통과선은 지금도 유효한 기준인가, v1.0 발행 이후
  갱신이 필요한가?
- Q17. GRDX 78(홀드아웃 tier 단일 최고점 = 대조군 오탐)을 우연으로
  보나, 구조적 약점의 신호로 보나?
- Q18. 동일 계열 관대화(L-6) — P1 교차 채점자를 결국 실행할 생각인가?

## 루프 접촉 경계 (소유자 언어 그대로)

"결과를 본 뒤 바꾸면 revert로 되돌릴 수 없는 모든 것 — seal, 컷오프,
임계값, 유니버스/대조군 구성, 사전 등록, 채점 비밀, 타임스탬프 — 은
루프가 **제안만 하고 절대 실행하지 않는다**. 그 밖의 모든 것: 루프가
결정하고 실행하며, 나는 사후에 원장을 검토한다."
