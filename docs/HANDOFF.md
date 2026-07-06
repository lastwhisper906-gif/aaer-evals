# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-06, 킬 스위치 GO 직후)

> 다음 세션은 CLAUDE.md → PROJECT.md → 이 문서 → GATE_PACKAGE.md 순으로 읽을 것.
> 세션 이력의 전문은 `docs/daily_log/2026-07-05.md` (총 4개 세션 기록).

## 프로젝트 위치: Week 1 게이트 통과 완료

**킬 스위치 GO 선언됨 (2026-07-05, 본인 확정)** — A형 23 / B형 7 (borderline
T01/T09는 본인 판정으로 B 확정). 판정 근거: `scoring/ab_first_pass.md`.
게이트 결정 시트(GATE_PACKAGE.md) **GP-0~GP-9 + 실행 규약 3조항 전부 서명 완료** —
서명란에 채택안·근거·일자 전문. 이제 프로젝트는 실험군 확정 → 대조군 매칭 →
블라인드 테스트(Week 2) 진입 단계다.

## 저장소·데이터 상태

- **git**: `main` == `origin/main`, 작업 트리 깨끗. CI 녹색 (pytest 20 +
  validate_schemas + verify_manifest --schema-only). 구 작업 브랜치
  `claude/treatment-group-expansion-mi2ba7`은 머지 완료 후 잔존 (삭제 여부 미결정).
- **원문 데이터**: `~/aaer-data/` 153파일 24.66MB. SHA-256 기준선
  `data/manifests/aaer_data_manifest.json`. **세션 시작 시 반드시
  `python tools/verify_manifest.py` → PASS 확인** (07-05 조용한 소실 사고의 교훈.
  실패 시 `tools/fetch_primary_sources.py` 재실행 후 재검증).
- **피평가자 입력**: `data/evaluatee/cases.json` v1.1 — 중립 ID(case_NN, 고정 시드
  셔플) + 컷오프 시점 사명 + 단일 티커. ID 매핑은 `scoring/id_mapping.json`
  (채점 전용 — 피평가자·pipeline/ 접근 금지, 정적 스캔으로 강제). 4중 방어 테스트.
- **오버라이드 기록**: OV-001/OV-002 (`scoring/overrides.md`) — 값 수준 누출 2건,
  인간 표본 점검 발견. §9 지표의 첫 데이터 포인트.

## 서명된 핵심 규칙 (이후 변경은 §5-6 이력 공개 조건)

1. **폭로일 원칙 A**: "최초의 공개적·회계특정적 신호 (소스 불문, 비공개 내부인지 제외)"
   → 적용으로 5건 이동(T02→2010-08-11, T12→2013-08-07, T13→2014-05-13,
   T19→2015-11-06, T26→2016-12-15), 컷오프·분기수 연쇄 재계산 완료.
2. **A/B 기준 v1** (`scoring/ab_criteria_draft.md` — SIGNED): G1 = 연차≥2 AND 총≥6
   (40-F 포함) / D1 좁은 문언 / 사후 폭로 경로 배제 / 임계 6.
3. **조작기간 = 명령문 정의 창** / **수치 = 명령문 인쇄 수치 기준** /
   **편입 = SEC 회계부정 집행조치 기준** (T16 AAER-4105, 동일 사건 귀속).
4. **대조군**: 장르 내 매칭(중국 RTO엔 비집행 RTO 대조군, GP-8 ①) + 컷오프는 매칭
   실험군 복사(GP-9 ① — 케이스별 독립 호출 규약과 연동 서명됨).
5. **실행 규약 3조항**: 피평가자 페이로드 = evaluatee_input v1.1 필드만 /
   케이스별 독립 호출 / memorization_suspect = 명부(중국 RTO 6건) AND 기계적 인용
   결손 (`docs/methodology_limitations.md` L-1).

## 다음 세션이 할 일 (우선순위순)

1. `python tools/verify_manifest.py` → PASS 확인.
2. **실험군 8 선정 기준·명단 서명**: `scoring/treatment_group_proposal.md` 검토 —
   제안 8건(T07 MON / T11 OFIX / T12 LOGI / T13 HTZ / T16 ICON / T17 MRVL /
   T21 SCOR / T28 KHC). 쟁점 2개를 특히 볼 것: ① 중국 RTO T06 포함 여부(포함 시
   비집행 RTO 대조군 수집 비용) ② 비전형 3건(T20/T25/T29) 제외 동의 여부.
3. 서명 후 **대조군 8 후보 수집 지시** (채점 보조가 수집, 매칭 확정은 인간).
4. 후속 확인 2건 (판정에 이미 주석 처리됨, 급하지 않음):
   - T13 폭로일 2014-05-13의 EDGAR vehicle — 당일 제출물이 로컬 사본에 없음
     (명령 ¶33 서술 기준으로 서명됨).
   - **T04 전신 CIK(0001170565) submissions 재수집** — `fetch_primary_sources.py`
     EXTRA_CIKS에 T04 추가 + 재실행 + `verify_manifest.py --write` 재생성·커밋.
     (G1 판정은 서명된 diff §B-1의 34분기 기록으로 이미 성립.)

## 미결·주의 사항

- **T19 소장 공백 / T30 소장 손상**: GP-7 ①(유지+주의문)로 서명 완료 — 도시에·채점
  기록에 근거 등급 명기 의무만 남음. T30은 원문 대조 필요 시 PDF를 사람 눈으로 열람.
- **금요일 회고란(docs/daily_log/2026-07-03.md) 미기입** — §8-7 재검토 창구, 3회째
  이월 중. 소급 기입 권장.
- 매니페스트 `fetched_at`은 07-05 복원 시각(mtime)이지 최초 수집 시각 아님 — 무해.
- **정직 기록 2건 (Week 3에서 재점검)**: ① 유도 서명 세션의 오버라이드 0건(전 항목
  추천안 채택) 패턴 ② 1차 A형 23/30 분포 — 기준 관대함 vs AAER 선택 편향, 오류 귀속
  때 F/T 예측 vs 실제 적중의 괴리로 판별.

## 역할 리마인더 (CLAUDE.md)

이 저장소의 세션은 **개발·채점 보조 Claude** — 파이프라인 안의 피평가자와 별개.
블라인드 테스트가 가까워졌으므로 특히: 피평가자의 EQ 판정을 세션에서 대신 생성하지
말 것, 피평가자에게는 `data/evaluatee/cases.json` 외 어떤 컨텍스트도 주입하지 말 것.
