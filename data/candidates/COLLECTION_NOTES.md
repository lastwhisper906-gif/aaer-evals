# COLLECTION_NOTES — AAER 후보 수집 (Stage 3, 2026-07-03)

> 상태: **PENDING HUMAN SIGN-OFF.** 이 문서와 candidates.json은 채점 보조 Claude의 1차 수집물이다.
> A/B형 판정은 어디에도 수행하지 않았다 (`ab_classification` 전부 null, §7 게이트).
> case_id(T01~T30)는 **킬 스위치 판정 전 잠정 번호** — 폭로일 순 정렬일 뿐 선정 순위가 아니다.

## 1. 수집 방법

- 병렬 read-only 리서치 서브에이전트 7개: 시대별 상세 배치 6개(각 ~5개) + 자유 탐색 1개. 산출은 구조화 JSON만.
- 원천: SEC 보도자료·소송/행정명령 문서를 인용한 2차 소스(법률회사 알림, 언론, NYU SEED DB), EDGAR `data.sec.gov` JSON API, 공시 원문(Archives 링크는 기록용).
- 전체 원시 리서치(신뢰도·출처·폭로 후보 체인 포함): `data/candidates/raw_research.json`

### 네트워크 제약 (신뢰도에 미치는 영향 — 검증 시 필수 인지)
이 실행 환경에서 `www.sec.gov`(AAER 색인·릴리스 원문·Archives)와 `efts.sec.gov`(전문 검색)는 차단됨.
`data.sec.gov`(제출 이력 JSON)만 Exa 경유로 접근 가능. 따라서:
- **AAER 원문을 직접 열람하지 못했다.** scheme_summary는 SEC 보도자료/명령문을 인용한 2차 소스 기준 — 신뢰도 상한 medium~high, 원문 대조는 인간 검증 항목.
- 대형 filer의 제출 이력 JSON이 잘려 `pre_revelation_quarters_available`이 다수 null (30개 중 확정치 ~10개). 로컬/직접 접근 가능한 환경에서 결정론적 재계산 필요 (Week 1 백로그).

## 2. 30개 상한 선정 규칙 (편입 기준의 투명성)

배치들이 포함 판정한 케이스는 37개였다. 사용자 지정 상한(20~30)에 맞춰:
1. **AAER 번호 확정 25개 전원 편입.**
2. AAER 번호 미확인이지만 실체(재무제표 조작 + SEC 집행 + 명확한 폭로 사건)가 강한 5개 편입: Iconix(T16), Tangoe(T22), Celadon(T24), MiMedx(T26), Luckin(T30).
3. **오버플로 7개** — 편입 안 함, raw_research.json에 보존, 스왑 후보:
   Pareteum, Sequential Brands, Swisher Hygiene, Interface, Rollins, Healthcare Services Group, Akazoo.
   (Interface/Rollins/HCSG는 EPS-Initiative 행정명령이라 AAER 번호가 실제로 존재할 가능성이 높으나 이 환경에서 미확인.)

**주의**: 편입 5개(규칙 2)는 "SEC AAER 2010–2022 보유" 기준을 문언상 충족하지 못한다(소송 릴리스만 확인, 또는 번호 미확인). 유지/스왑은 인간 결정 사항 → REVIEW.md 항목 2.

### 배제 3개 (검증자용 기록)
| 케이스 | 사유 |
|---|---|
| Longtop Financial (LFT) | 발행사 AAER 없음 — 12(j) 등록취소 절차뿐. 관련 AAER-3319는 감사인(Deloitte 중국) 대상 |
| MDC Partners (MDCA) | 보수 공시·non-GAAP 공시 사건 — GAAP 재무제표 조작 아님 |
| Kandi (KNDI) | 2023 SEC 명령은 EV 공시 건. 2017 관련당사자 재무 정정은 AAER 미대상 |

## 3. 폭로일(first_revelation_date) — UNRESOLVED 및 모호 케이스

편입 30개에 문자열 "UNRESOLVED"는 없다. 단, 아래 9건은 **대안 날짜가 존재**하며 채택일이 판단 의존적 — 컷오프가 달라지므로 인간 확정 필요 (전체 후보 체인은 raw_research.json의 revelation_candidates):

| ID | 채택일 | 대안 | 쟁점 |
|---|---|---|---|
| T02 CSC | 2011-01-28 (SEC 조사 개시 8-K) | 2010-08 (10-Q 내 Nordic 조정 공시) | 이르게 잡으면 컷오프 5개월 앞당겨짐 |
| T07 MON | 2011-06-29 (조사 공개, 2차 소스) | — | EDGAR 원문으로 정확한 일자 미확정 (medium) |
| T12 LOGI | 2014-05-21 (감사위 조사 공개) | 2013-08-07 (10-K/A 중대약점 공시) | '조사'와 '약점 공시' 중 무엇이 폭로인가 |
| T16 ICON | 2015-08-10 (SEC 검토 공시) | 2015-03~08 (CFO·CEO 사임 체인) | 회계 특정적 신호 vs 경영진 이탈 신호 |
| T18 VRX | 2015-10-19 (SIRF 폭로 기사) | 2015-10-05 (R&O 소송 공개) / 10-21 (Citron) | 어떤 사건이 '시장이 알게 된' 시점인가 |
| T20 BRX | 2016-02-08 | — | 내부 인지(2015-12)는 비공개라 제외 — 원칙 확인만 |
| T21 SCOR | 2016-02-29 (NT 10-K) | 2016-03-07 (보도자료) | 12b-25가 첫 공개 신호 |
| T24 CGI | 2017-04-05 (Prescience Point) | 2016-07 (애널리스트 의문, 날짜 모호) | 이른 신호의 공개성·특정성 판단 |
| T26 MDXG | 2017-09-20 (공매도 리포트 2건) | **2016-12-15 (내부고발 소송 보도자료)** | '최초 공개 주장' 원칙대로면 2016-12-15가 옳을 수 있음 |
| T25 GE | 2017-07-21 (LTC 공시·리뷰 발표) | 2018-01-16 / 01-24 | 다단계 폭로 — 어느 마일스톤인가 (medium) |

## 4. 스키마 검증 결과 (강제 편차의 공개)

- 완전 통과 5건 (T25, T27~T30). 
- **의도된 편차 25건**: `manipulation_period_start/end`가 월(YYYY-MM) 또는 연(YYYY) 정밀도 — AAER/소장 원문이 일 단위를 제공하지 않는 경우 일자를 지어내지 않는다는 보수 원칙. 스키마 `format: date`와 충돌 (orientation_check.md 불일치 #8과 동일 계열).
- 그 외 실패 0건. `cutoff_date`는 전 케이스 `first_revelation_date` 전일 (T21은 윤년 경계: 2016-02-29 폭로 → 컷오프 2016-02-28).

## 5. 케이스별 필드 신뢰도 요약

> **주의 (2026-07-05 추가)**: 아래 표는 Stage 3 수집 당시(재검증 **이전**) 스냅샷이다 — 역사적
> 기록으로 보존하며 갱신하지 않는다. 현행 값은 `candidates.json`, 정정 내역은
> `reverification_diff.md` 참조 (예: PUDA 12→16, LOGI 19→24, null 13건 실측 채움).

(핵심 필드만: 전량은 raw_research.json의 confidence 객체. H=high M=medium L=low)

| ID | Ticker | AAER# | 폭로일 | scheme | 분기수 | XBRL | 특이사항 |
|---|---|---|---|---|---|---|---|
| T01 | RINO | H | H | H | H(11) | H(false) | China RTO, 이중장부 |
| T02 | CSC | H | M | H | L(null) | H | 폭로일 대안 존재 |
| T03 | CCME | H | M | H | H(4) | H(false) | 운영 전 SPAC 공시 제외 |
| T04 | WFT | H | H | M | L(null) | H | 다중 CIK (1453090 채택) |
| T05 | KEYP | H | H | H | L(3) | M(false) | 상장 1년차 — 분기 2~3개뿐 |
| T06 | PUDA | H | H | H | M(12) | L(false) | XBRL 플래그 잘림 — 검증 필요 |
| T07 | MON | H | M | M | H(41) | H(부분) | 폭로일 원문 미확정 |
| T08 | MILL | H | H | H | L(null) | M(false) | FY말 4/30 |
| T09 | FEED | M | H | H | M(15) | M | 회사 본건은 소송 — AAER-3542는 CFO 명령 |
| T10 | DMND | H | H | M | L(null) | M | AAER 2건 (3526/3527) |
| T11 | OFIX | H | H | H | H(43) | H | 동시 FCPA 명령(AAER-3851)은 별건 — 배제 |
| T12 | LOGI | H | M | H | H(19) | H(부분) | 폭로일 대안 존재 |
| T13 | HTZ | M(CIK) | H | M | L(null) | H | **선행 CIK 1364479로 공시 회수 필요** |
| T14 | PWE | H | H | H | L(null) | H(false) | FPI: 40-F/6-K — 10-Q 부재 |
| T15 | RATE | H | H | H | H(13) | H | 조작창 좁음(Q2 2012 중심) |
| T16 | ICON | L(null) | M | H | L(null) | M | AAER# 미확인 편입 — 인간 확정 |
| T17 | MRVL | H | H | M | L(null) | H | 조작기간 L — 회계연도 모호 |
| T18 | VRX | H | M | H | L(null) | H | 폭로일 대안 존재 |
| T19 | OSIR | H | H | H | L(null) | H | 민사소송이나 AAER-3905 확인(SEED) |
| T20 | BRX | H | H | M | M(9) | H | non-GAAP(SP NOI) 사건 |
| T21 | SCOR | H | M | H | M(34) | H | 비화폐 거래 매출 |
| T22 | TNGO | M(null) | H | H | H(17) | H | AAER 없음 확인 — 편입 유지 여부 인간 결정 |
| T23 | HAIN | H | H | M | L(null) | H | **비전형: 무벌금·무정정·비사기 조항** |
| T24 | CGI | M(null) | M | H | L(null) | H | AAER 없음(임원 102(e)는 2023) |
| T25 | GE | H | M | M | L(null) | H | 다단계 폭로, 정정 없음 |
| T26 | MDXG | M(null) | M | H | L(null) | H | 폭로일 2016-12-15 대안 강력 |
| T27 | WAGE | H | H | H | H(22) | H | AAER는 임원 대상 — 발행사 자격 인간 확정 |
| T28 | KHC | H | H | M | H(14) | H | scheme 'other' 포함(비용관리 스킴) |
| T29 | UAA | H | H | H | H(55) | M(부분) | 공시상 GAAP 위반 주장 없음(공시 사건) |
| T30 | LK | H(없음 확인) | H | H | M(2) | H(false) | FPI ADR — 6-K 2건뿐, AAER 없음 |

## 6. 학습 노트 (§10)

폭로일은 단일 사실이 아니라 **사건 체인에서의 선택**이다 — "시장이 처음 알게 된 날"의 조작적 정의(공매도 리포트 포함? 내부고발 소송 보도 포함? 10-Q 속 한 줄 공시 포함?)를 킬 스위치 판정 전에 고정하지 않으면, 컷오프가 케이스마다 다른 원칙으로 정해져 look-ahead 가드 자체가 흔들린다.
