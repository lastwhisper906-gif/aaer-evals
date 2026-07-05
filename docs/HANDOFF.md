# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-05 심야 세션 — 표본 점검 후속)

> 다음 세션은 CLAUDE.md → PROJECT.md → 이 문서 → REVIEW.md/GATE_PACKAGE.md 순으로 읽을 것.

## 현재 상태 (2026-07-05 저녁 기준)

- **git**: main = origin/main = `HEAD`(이 커밋). 브랜치 16커밋이 `3ca0794`로 --no-ff 머지됨
  (사용자 서명 결정 — 사유는 머지 커밋 메시지에 기록). 작업 브랜치
  `claude/treatment-group-expansion-mi2ba7`은 머지 완료 후 잔존(삭제 여부 미결정).
- **데이터**: `~/aaer-data/` 153파일 24.66MB, SHA-256 기준선 커밋됨
  (`data/manifests/aaer_data_manifest.json`). 존재·무결성 확인은
  `python tools/verify_manifest.py` (디렉터리 부재/변조/누락 모두 exit 1).
  **월요일 검토 시작 전에 이걸 먼저 실행할 것** (07-05 조용한 소실 사고의 교훈).
- **CI**: pytest(15) + validate_schemas + verify_manifest --schema-only (`.github/workflows/ci.yml`).

## 심야 세션 추가분 (표본 점검 후속 — commit `d63c9d8`~)

- **피평가자 입력 v1.1**: 사용자 표본 점검이 값 수준 누출 2건 발견 → 서명 정정.
  중립 ID(case_NN, 셔플) + 컷오프 시점 사명 + 단일 티커. 매핑은
  `scoring/id_mapping.json` (채점 전용 — 피평가자·pipeline/ 접근 금지. 사용자 검토로
  data/scoring/에서 이동: 데이터가 아니라 채점 인프라).
  방어 ④(값 수준 스캔) 신설, 총 20 tests. **오버라이드 첫 2건 기록됨**
  (`scoring/overrides.md` OV-001/OV-002 — §9 지표의 첫 데이터 포인트).
- **사용자 검토 반영 (심야 2차)**: ① GP-6에 **페이로드 규약** 문언 추가(피평가자 호출
  = evaluatee_input v1.1 필드만 + 케이스별 독립 호출 — 방어 ④는 파일 위치만 지킴,
  실제 주입 경로의 최종 보증은 이 규약. 채점 프로토콜 고정 시 서명) ② GP-9에 ①의
  성립 조건(독립 호출) 명문화 — 배치 호출이면 재검토 ③ GP-2에 T18 점검 절차(원칙
  먼저 서명 → 채택일 도출, 역순 = 사후 정당화 위험) ④ L-1 플래그 기준을 명부(중국
  RTO 6건) AND 기계적 인용 결손의 2단 규칙으로 고정 (재량 배제).
- 신설 문서: `docs/methodology_limitations.md` (L-1 암기 한계 + memorization_suspect
  채점 플래그 초안 — 채점 프로토콜 고정 시 편입 여부 서명 필요).
- GATE_PACKAGE에 GP-8(중국 RTO 군집 매칭 기준)·GP-9(대조군 컷오프 규약 약한 누출) 추가,
  GP-2에 표본 점검 3건(T25/T07/T18) 보강 — 점검 지시문의 세 날짜는 폭로일이 아니라
  **컷오프일**이었음(혼동 주의).

## ★ 게이트 완료 (2026-07-05 심야 유도 서명 세션 — 월요일 안건 소진)

- **GP-0~GP-9 + 실행 규약 3조항 전부 서명 완료** (GATE_PACKAGE.md 서명란에 전문).
  폭로일 원칙 A 서명 → 5건 이동(T02/T12/T13/T19/T26), A/B 기준 v1 고정(G1 = 연차≥2
  AND 총≥6, 40-F 포함), T16 AAER-4105 기입, 30건 ab_classification 기입·서명.
- **킬 스위치: A형 23 / B형 7 → GO 선언** (borderline T01/T09는 본인 판정 B 확정).
  1차 표: `scoring/ab_first_pass.md`.
- **실험군 8 제안안**: `scoring/treatment_group_proposal.md` — 선정 기준+8건+스왑 후보.
  **확정 아님** — 다음 세션이 맑은 눈으로 서명할 것.

## 다음 세션이 할 일

1. `python tools/verify_manifest.py` → PASS 확인 (실패 시 fetch_primary_sources.py 재실행 후 재검증)
2. **실험군 8 선정 기준·명단 서명** (`scoring/treatment_group_proposal.md`) — 특히
   기준 6(중국 RTO T06 포함 여부)과 비전형 3건 제외에 동의하는지.
3. 대조군 8 후보 수집 지시 (GP-8 장르/섹터 매칭, GP-9 컷오프 복사).
4. 후속 확인 2건: T13 폭로일(2014-05-13)의 EDGAR vehicle / T04 전신 CIK(0001170565)
   submissions 재수집(fetch EXTRA_CIKS 추가) + 매니페스트 재생성.
3. 서명 후: Claude에게 A/B 기준 1차 적용 표(케이스 × 질문 + 인용) 작성 지시 가능 (서명 전 금지).
4. 오버라이드는 `scoring/overrides.md` OV-NNN, 서명은 GATE_PACKAGE 서명란 + 커밋.

## 미결·주의 사항

- **T19 OSIR 소장 공백**: 금요일 재검증이 인용한 `comp-pr2017-207.pdf`가 복원본에 없음
  (LR-23978 페이지의 소장 링크가 SEC 자리표시자 `compxxxxx.pdf`). 처리 선택지는
  GATE_PACKAGE GP-7 — **해결하지 말고 서명부터**. ③(대체 경로) 채택 시 매니페스트 재생성
  필수(`verify_manifest.py --write` + 커밋).
- **T30 LK 소장 PDF**: 기계 추출 불가(인코딩 손상), 사람 눈으로는 읽힘 — 월요일 원문 대조
  시 직접 열람.
- **금요일 회고란(docs/daily_log/2026-07-03.md) 미기입** — §8-7의 재검토 창구가 빈 채로
  이틀째. 소급 기입 권장.
- 매니페스트의 `fetched_at`은 파일 mtime(= 07-05 복원 시각)이지 금요일 최초 수집 시각이
  아님 — 대조 항목 아니므로 무해하나 해석 시 유의.
- 세션 지시문의 "1차 소스 없는 3건" 표현은 실측과 다름: 실패 URL 3 / 케이스 2 / 실공백 1
  (GP-7 대장 참조). 이후 문서에서 "3건"으로 인용하지 말 것.

## 이 세션(07-05 저녁)이 한 일 요약

머지+push+패리티 검증 / 무결성 매니페스트+검증기+CI / 실패 fetch 3건 전수 추적(결함 대장) /
GATE_PACKAGE.md 신설(GP-0~7) / 이 문서·데일리 로그. 판정·서명은 0건 (전부 월요일 인간 몫).
