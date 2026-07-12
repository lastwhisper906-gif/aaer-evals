# DISSEMINATION_DATES_MEMO — Q-M02 조사 결과 (2026-07-13, 무호출, 스펙 무변경)

**결론: 입수 가능(obtainable) — 과거 공표일은 FINRA 연도별 일정표의 아카이브
스냅샷에서 프로그램적으로 복원할 수 있다.** 이 세션은 조사·계획까지만 —
구현·스펙 개정 없음 (B4 스펙 §2의 LAG=14 상수는 그대로 유효).

## 1. 실측 (2026-07-13)

- **현행 페이지** (finra.org/filing-reporting/regulatory-filing-systems/
  short-interest): 2025·2026 두 해분 일정표, **Publication Date 열 포함**
  (Settlement / Due / Publication). 과거 연도 링크·아카이브 없음.
- **Wayback Machine**: 동일 URL의 연 1회 이상 스냅샷 실측 —
  20200718 · 20210116 · 20220317 · 20230127 · 20240320 · 20250114 · 20260118
  (CDX API, statuscode 200). 구 URL 형태(`/filing-reporting/short-interest`,
  `/short-interest-reporting`)는 2019-09·2019-12 스냅샷 존재.
- **2020-07-18 스냅샷 파싱 검증**: 표 3열 = Settlement Date / Due Date /
  **Exchange Receipt Date** (현행 "Publication Date"의 전신 명칭), 26행.
  예시 행: 결제 2020-01-15 → 마감 01-17 → 수신 01-27 (**+12일**) ·
  결제 2020-01-31 → 02-04 → 02-11 (**+11일**) · 결제 2020-02-14 → 02-19 →
  02-26 (**+12일**).
- **상수 안전성**: 관측 지연 11–12 캘린더일 ≤ 사전 등록 LAG 14 — 표본 내
  보수성 유지 (전수 검증은 구현 단계 몫).

## 2. 커버리지 전망

- 2019–2026: 스냅샷 실측 확보 (위 목록) — B4 아카이브 구간(결제일
  2017-12-29~)의 2019+ 부분은 복원 가능.
- **2018 (및 2017-12-29)**: 현행 URL 스냅샷 부재 — 구 URL 형태의 2018년대
  스냅샷 탐색 필요 (CDX 추가 조회로 확인, 구현 단계 첫 작업). 미발견 시
  2018년분만 LAG=14 유지하는 혼합 테이블도 스펙 개정안에 명시 가능.

## 3. 단계적 구현 계획 (빌드 없음 — 소유자 GO 시 1세션 분량)

1. CDX로 연도별 최적 스냅샷 목록 확정 (2018 커버리지 포함 여부 확정).
2. 스냅샷 HTML → (settlement, due, publication) 3열 테이블 파싱 —
   결정론 스크립트 + 원본 HTML 아카이브(체크섬) 동반.
3. `data/` 하위에 settlement→publication 매핑 커밋 (연도별 출처 URL 병기).
4. **스펙 개정 D-엔트리** (B4 스펙 §2의 사전 등록 조건): LAG 상수 →
   실측 공표일 치환, 미커버 결제일은 LAG=14 유지 명시. 재실행 시 D56/D57과
   동일한 1차-결과-보존 규율.
5. 영향 추정: 공표 지연 실측(11–12일)이 상수(14일)보다 짧으므로 치환은
   일부 경계 케이스의 보고서를 **추가 편입**시키는 방향 — 커버리지 증가
   가능성, 방향 중립(케이스 선별 재량 0).

## 4. 출처

- 현행: <https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest>
- 아카이브 검증 표본: <http://web.archive.org/web/20200718232030/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest>
- CDX API: `web.archive.org/cdx/search/cdx?url=finra.org/filing-reporting/...`

Q-M02는 "입수 가능 — 구현은 소유자 GO 게이트"로 전환된다 (screener S-09 동일).
