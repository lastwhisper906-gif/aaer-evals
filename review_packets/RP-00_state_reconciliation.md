# Review Packet 00 — 상태 조정 (Phase 0)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 작성: 2026-07-06. 본 packet은 차단 게이트를 대체하는 비동기 검토 문서다 (D14).
> 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (§5-5).

## 1. 상태 요약 (실측)

| 항목 | 결과 |
|---|---|
| 0-1 매니페스트 | **PASS** — 재수집 전 153파일/24,664,847B → T04 재수집 후 **155파일/24,923,194B** 기준선 재생성, 재검증 PASS |
| 0-2 D1 | `tools/validate_schemas.py`에 `check_scheme_type_by_group()` 코드 강제 + 단위 테스트 신설. pytest 22건 전부 통과, validate PASS |
| 0-2 D2/D3 | GP-3·GP-1 서명 규칙의 소유자 재확인으로 `scoring/overrides.md` GA-001 부속에 기록 (변경 0) |
| 0-3 D18 감사 | **백데이트 필요 항목 없음** — 킬 스위치 1차 표(`d5986ba` 07-05 17:02)·GO 선언(`599a2e9` 07-05 17:08) 모두 결정 당일 커밋 확인. 유일한 미확정분이던 실험군 8은 소유자 지시(07-06)로 확정, `scoring/decisions_log.md` D18 절에 정직 주석과 함께 기록 |
| 0-4 T04 | 전신 CIK 0001170565 submissions 재수집 (27건) — 합산 34분기 = 서명된 diff §B-1과 정확 일치. 매니페스트 155파일로 재작성 |
| 0-4 T13 | **EDGAR vehicle 확인 성공**: 2014-05-13 당일 NT 10-Q 실재 (전신 CIK 0001364479, accession 0001104659-14-038216; 익일 8-K). [primary-indirect] 등급 → EDGAR 확인으로 상향, candidates.json revelation_source 갱신 |
| 0-5 모델 고정 | 피평가자 `claude-sonnet-5` / 채점자 `claude-fable-5` (폴백 `claude-opus-4-8`) — 근거·기각 대안은 decisions_log "모델 고정 기록" |
| 0-5 D12 | 구 브랜치 `claude/treatment-group-expansion-mi2ba7` 로컬·원격 삭제 완료 |

## 2. REVIEW.md (07-03) ↔ HANDOFF.md (07-06) 조정표

| REVIEW 항목 | 07-05 GO까지의 처리 | 잔여 |
|---|---|---|
| 0 스키마 실검토 재서명 | GP-0 항목 0 서명 완료 (07-05) | D1 코드 강제 — **본 세션에서 완료** |
| 1 재검증 diff 서명 | GP-0 항목 1 — §A-1 9건 + §B-1 20건 전건 승인 | 없음 |
| 2 폭로일 원칙 + 편입 기준 | GP-2(원칙 A + 12건 확정) + GP-4(② 채택) 서명 | 없음 |
| 3 A/B 기준 서명 | GP-5 — v1 SIGNED (설계 선택 4가지 개별 확정) | 없음 |
| 4 킬 스위치 판정 | GP-6 — **GO** (A형 23, borderline 2건 B 확정) | 후속: 실험군 확정(본 세션 D18), 대조군 매칭(Phase 2-6) |
| HANDOFF 후속 2건 | — | T04 재수집·T13 vehicle — **본 세션에서 완료** |
| 금요일 회고 3회 이월 | — | D11 → Review Packet 02에 편입 예정 |

## 3. Claude 재량 판단 (감사 대상)

1. **모델 고정** (조항 적용 불능 상태에서의 수립 — decisions_log 근거·기각 대안 전문).
   - **오버라이드 방법**: decisions_log의 pin 2줄 수정 + freeze 전이면 재실행 비용 0.
     freeze 후·실행 후면 §5-6 이력 공개 + 전체 재실행 (24 evaluatee 호출 + 채점).
2. **T13 등급 상향** (기계 실측 기반 — NT 10-Q accession 인용).
   - **오버라이드 방법**: candidates.json revelation_source 문자열 원복 1커밋. 재실행 불요
     (컷오프 날짜 자체는 불변 — 2014-05-13 유지).
3. **D18 감사 판정** "격차 없음" — git 로그가 근거이므로 반박은 로그 제시로 족함.

## 4. 불확실성 종합

- T13 NT 10-Q가 명령 ¶33이 서술한 바로 그 공개 신호인지는 **정황 강함**(같은 날, 같은
  내용 유형 — Q1 10-Q 제출 불능)이나 문서 본문 대조는 미수행 (NT 10-Q 본문 미보유).
  현 기록은 "EDGAR vehicle 확인"이지 "본문 축어 확인"이 아님.
- 모델 카탈로그의 가용성(특히 Fable 5의 조직 접근성)은 실행 시점에만 확정 가능 — 폴백
  규칙으로 처리.
- **실행 격차**: 본 환경에 API 자격 증명 없음 — Phase 3 실 호출은 자격 증명 제공 시까지
  스테이징 (아래 "requires credentials" 목록 유지).

**학습 노트(§10)**: "미커밋 결정"이라는 전제조차 감사 대상이다 — D18의 전제를 그대로
믿고 정직 주석을 붙였다면, 존재하지 않는 격차를 자백하는 기록이 생겼을 것이다.
