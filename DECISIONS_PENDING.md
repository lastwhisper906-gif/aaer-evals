# DECISIONS_PENDING.md — direction-loop 설치 중 위임 결정 원장 (owner ratify 대기)

> 2026-07-29, 소유자 전권 위임 지시("decide, execute, log") 하의 세션이
> 내린 결정 기록. 형식: options / choice / basis / revert. 소유자 추인
> 시 D-원장(scoring/decisions_log.md)으로 이관하거나 여기 서명을 남긴다.
> 이 파일 자체는 게시 산출물이 아니다.

## D-P1 — INV-16 단일 작성자 원칙: direction-loop 조건부 예외 (U1 집행)
- **Options:** (a) 조건부 예외로 개정 (b) 루프를 INV-16 위반으로 보고 중단
- **Choice:** (a) — 소유자 답변 U1 그대로: 비-main 브랜치 + 하네스 기계적
  격리(워크트리 전용·보호 경로 revert·전역 단일 루프 잠금) 하에 허용,
  루프 실행 중 main push 금지는 소유자 관행. INV-16은 §6 저장소
  규약이지 측정 조건이 아니므로 동결 규칙 위반 아님.
- **Basis:** 소유자 지시문 U1 (2026-07-29) · PROJECT_INVARIANTS.md §6
- **Revert:** PROJECT_INVARIANTS.md INV-16 예외 단락 삭제 +
  `sync_context.sh .` 재실행.

## D-P2 — D-앵커 검증: 하네스를 저장소에 적응 (U2 집행)
- **Options:** (a) 하네스 H19의 D-분기를 scoring/decisions_log.md +
  하이픈 정규화로 적응 (b) docs/decisions/ 디렉토리·별칭을 저장소에 신설
- **Choice:** (a) — 저장소를 하네스에 맞추지 않는다. verify_anchors의
  D-* 분기는 `scoring/decisions_log.md`(+ `docs/decisions/` 존재 시 병행)
  를 검사하고, "D-94"·"D94" 두 표기를 하이픈 제거 정규화 후 `^## D` 형
  헤딩과 대조한다. 리뷰어 프롬프트의 앵커 사양도 동일하게 갱신.
- **Basis:** 소유자 지시문 U2 · AUDIT_INDEX.md §1 (D-NNN 원장 위치 규약)
- **Revert:** ~/tools/direction-loop.sh verify_anchors D-분기와
  ~/tools/prompts/direction_review.md 앵커 절을 계획 v2 원문으로 복원.

## D-P3 — .loop.conf GATE_CMD (U3 집행)
- **Options:** (a) pytest 스모크 게이트 (b) make verify-public 전체 5게이트
- **Choice:** (a) `GATE_CMD=".venv/bin/python -m pytest pipeline tools
  scoring analysis -q"`. **INV-05 비위반 사유(소유자 지시 그대로 기록):**
  루프의 사이클별 게이트는 스프린트 브랜치 위의 스모크 게이트다. 전체
  verify-public 5게이트는 소유자의 main 병합을 종전과 동일하게 계속
  지배한다 — 5게이트를 다른 것으로 "대체 실측"하는 것이 아니라, 병합
  게이트 앞단에 사이클 게이트를 추가하는 것이다.
- **Basis:** 소유자 지시문 U3 · Makefile verify-public · INV-05
- **Revert:** .loop.conf 1줄 수정.

## D-P4 — DIRECTION_CONTEXT.md 작성 규칙
- **Options:** (a) 저장소+덤프에서만 합성, 미답은 OPEN 절 (b) 그럴듯한
  보완 작성
- **Choice:** (a). 답변된 항목: Q1·Q4·Q7·Q8·Q12(부분)·Q13·Q15·Q16·Q19.
  OPEN (owner)로 이관(질문 원문 그대로): Q2·Q3·Q5·Q6·Q9·Q10·Q11·Q14·
  Q17·Q18. 덤프의 사실 주장(B3 귀속 0.147, 3-arm +6.0pp, Karpoff/Lou,
  Lowe v. SEC 등)은 소유자 제공 사실로 기재 — 세션이 검증·창작하지 않음.
- **Basis:** 소유자 지시문 MEMORY_DUMP 절 ("NEVER fabricate answers")
- **Revert:** git revert (파일 단독 커밋 아님 — 해당 커밋의 파일 복원).

## D-P5 — VALIDATION_CRITERIA v1: 위임 선택분 (V3/V5/V6 정의 + V1 처리)
- **Options:** V3/V5/V6를 계획 §7.0 원문 그대로 두기 vs 판정 가능하게
  구체화; V1을 게이트에 포함 vs 소유자 사후 채점으로 명시 분리
- **Choice:** V2=0·V4≥50%는 소유자 고정값 그대로. V3는 "항목 인용 +
  선호 이상의 사실 주장 부재" 판정 규칙으로, V5는 "done_when이 why의
  문제를 해소하지 못하는 불일치" 판정 규칙으로, V6는 "≤150줄 + 모듈
  책임 + INV 강제 지점 ≥5 + BN 차단 지점 ≥3 + 인용 경로 실재" 체크로
  구체화 — 전부 인용 증거 요구. V1은 소유자 사후 채점(기계 사인오프
  비게이트, 첫 병합 결정 게이트)으로 명시. 정지 규칙: V2–V6 실패 시
  중단, 리뷰어 프롬프트 개정 최대 2회.
- **Basis:** 소유자 지시문 §1 (V2/V4 고정, "choose and justify the rest
  yourself; V1 owner-graded post-hoc") · 계획 §7.0
- **Revert:** VALIDATION_CRITERIA.md는 등록 후 동결 — 수정이 아니라
  차기 검증 라운드에서 v2로 재등록.
