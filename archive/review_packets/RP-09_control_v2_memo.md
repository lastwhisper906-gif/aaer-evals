# RP-09 Stage 2 — 대조군 v2 선정 메모 (PROPOSED, 소유자 §Final 결정 대상)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> 기준: `docs/CONTROL_CRITERIA_v2.md` (실행 전 커밋 b22e84e + S0 개정 커밋 —
> 이력 §8 공개). 선정: `tools/control_v2.py select` — 기준+검증된 풀의 순수 함수
> (재실행 = 동일 결과, 네트워크 없음). 풀: 8케이스 × 1차+보충 SIC 전수(무조건
> 확장), 4층 검증 **PASS (격리 0)**. 산출: `runs/rp09/control_group_v2.json`
> (**22선정**, criteria_sha256 `2d62a2d9…`). RP-09가 명명한 복원 3건 전부 복원:
> GRMN(무조건 확장) · FORR(T21 SIC 정정 8700 — top pick) · GIS(E4-v2 + S0 개정
> — top pick). 본 결과는 Claude 기반 단일 파이프라인에 한정 (§5-5).

## 1. 선정 표 (22 — 케이스당 2–3, S2-v2 전순서: 규모 버킷→SIC 계층→FYE→CIK)

| 회사 [티커] | 매칭 실험군 | 규모 거리 | 산업 노트 | 한 줄 사유 |
|---|---|---|---|---|
| Air Products [APD] | T07 MON | 0.152 | 산업가스 (2810, 보충) | 매출 축 최근접 — 화학 대분류 내 규모 1위 매치 |
| Mosaic [MOS] | T07 MON | 0.290* | 비료 (2870, 1차) | 장르 정확 일치 (농화학) — *자산 축 대체 (매출 PIT 불능) |
| Celanese [CE] | T07 MON | 0.574 | 특수화학 (2820) | 화학 규모 3위 — 케이스 3번째 슬롯 |
| Masimo [MASI] | T11 OFIX | 0.065 | 환자 모니터링 (3845) | 신규 SIC 전수의 산물 — 의료기기 최근접 |
| Accuray [ARAY] | T11 OFIX | 0.122 | 방사선수술 (3841, 1차) | v1.1 선정 승계 — 1차 SIC 정확 |
| Merit Medical [MMSI] | T11 OFIX | 0.159 | 일회용 의료기기 (3841, 1차) | 1차 SIC + FYE 정확 일치 |
| Teledyne [TDY] | T12 LOGI | 0.013 | 계측·전자 (3812) | 전 그룹 최근접 (1.3%) |
| Ciena [CIEN] | T12 LOGI | 0.135 | 네트워크 장비 (3661) | 하드웨어 제조 인접 |
| Garmin [GRMN] | T12 LOGI | 0.257 | 소비자 전자 (3812) | **복원 대상** — 소비자 하드웨어 장르 최고 정합 |
| Ryder [R] | T13 HTZ | 0.518 | 차량 리스 (7510, 1차) | 1차 SIC 유일 밴드 내 — RP-01 재선정 |
| Upbound(구 Rent-A-Center) [UPBD] | T13 HTZ | 1.244 | 렌탈 (7359) | 밴드 내 차선 — 렌탈 장르 (거리 열위 주의) |
| InterDigital [IDCC] | T16 ICON | 0.104 | IP 라이선싱 (6794, 1차) | 라이선싱 수익 모델 정확 일치 |
| Rocky Brands [RCKY] | T16 ICON | 0.477 | 신발 (3140, 1차) | ICON의 이중 정체(브랜드/신발) 중 신발 축 |
| Dolby [DLB] | T16 ICON | 0.733 | 기술 라이선싱 (6794, 1차) | 라이선싱 축 보강 |
| First Solar [FSLR] | T17 MRVL | 0.089 | 태양광 모듈 (3674, 1차) | v1.1 승계 — 반도체 SIC 최근접 |
| Amkor [AMKR] | T17 MRVL | 0.169 | 반도체 패키징 (3674, 1차) | 반도체 공급망 정합 |
| Analog Devices [ADI] | T17 MRVL | 0.258 | 아날로그 반도체 (3674, 1차) | 팹리스/설계 장르 최고 정합 — **⚑아래 §3** |
| Forrester [FORR] | T21 SCOR | 0.053 | 리서치·데이터 (8700) | **복원 대상** — 데이터/리서치 판매 모델 정합, FYE 정확 |
| Exponent [EXPO] | T21 SCOR | 0.051 | 컨설팅 (8742) | 동버킷 차순위 (tier 규칙) — 전문서비스 |
| Liquidity Services [LQDT] | T21 SCOR | 0.188 | 온라인 마켓플레이스 (7389, 1차) | v1.1 승계 — 1차 SIC |
| General Mills [GIS] | T28 KHC | 0.511 | 포장식품 (2040) | **복원 대상** — KHC 유일 실질 동종·동규모 |
| Campbell's [CPB] | T28 KHC | 1.105 | 포장식품 (2000) | 밴드 내 차선 — 거리 열위 (KHC $26B의 구조적 희소성) |

케이스당: T07 3 · T11 3 · T12 3 · T13 **2** · T16 3 · T17 3 · T21 3 · T28 **2**
(T13·T28은 풀 소진 — 자격자 전원 선정, S3-v2 최소 2 충족).

## 2. 그룹 수준 커버리지

시대축은 컷오프 1:1 복사로 구조 일치 (2011-06~2019-02). 산업축은 8케이스 전부
1차 또는 선언 보충 SIC 내에서 채워졌고, 22선정 중 1차 SIC가 12, 보충이 10 —
보충 의존은 주로 규모 희소 케이스(T07 화학, T12 하드웨어, T21 서비스)다. 규모축
중위 거리 0.19(≈21%)로 v1.1(8선정 중위 0.14)보다 소폭 넓어졌는데 이는 케이스당
3배수 확장의 산술적 결과다. 구조적 약점 두 곳을 명시한다: ① T13(HTZ $10.8B
렌터카)은 미국 상장 유니버스에 동규모 동종이 Ryder뿐이라 2번째 대조(UPBD)의
거리가 1.24로 열위 ② T28(KHC $26.2B)도 같은 구조로 CPB 거리 1.11. 이 두
케이스의 오탐/판별 해석은 케이스별 매치 품질을 병기해 읽어야 한다 (검정력
사전 계산의 시나리오가 이 비대칭을 포함). Hormel(SIC 2011)은 선언 SIC 목록
밖이라 풀에 없음 — 선언 동결의 알려진 비용으로 기록.

## 3. 사람 눈이 가장 필요한 3건

1. **Analog Devices (T17 3순위)** — 2008 옵션 백데이팅 SEC 화해가 **AAER 색인에
   무인쇄**라 E4로 잡히지 않는다 (v1.1 memo·D20이 "승격 시 웹 2차 선행"을 조건
   걸었던 그 회사가 이번엔 기계 선정권 안). 웹 스크린에서 최우선 확인 —
   부적격 판明 시 alt1 Benchmark Electronics로 기계 교체 (오버라이드 1줄).
2. **Campbell's (T28 2순위)** — E4-v2 단일 토큰 규칙이 인명 오탐을 걸러 기계
   통과시켰으나 v1에서 수기 검토가 필요했던 이름이고, 거리 1.11은 그룹 최악.
   "KHC의 대조로 쓸 수 있는 수준인가"는 사람 판단.
3. **Upbound/Rent-A-Center (T13 2순위)** — 거리 1.24 + 소비자 렌탈 vs 렌터카
   장르 거리. 2000년대 초 Rent-A-Center 관련 집행 이력 유무 웹 확인 권장.

## 4. 재량 기록 (JSON 줄 — 규칙이 결정하지 못한 지점 전수)

{"discretionary":"S1-asset-substitute","case":"T07","company":"Mosaic","reason":"매출 PIT 불능(태그 부재) → 총자산 축 대체 (criteria S1 단서, v1과 동일 측정)","date":"2026-07-07"}
{"discretionary":"inherited-condition","case":"T17","company":"Analog Devices","reason":"D20 ③ 단서 승계 — 선정권 진입 시 웹 2차 확인 선행 (2008 백데이팅 화해 색인 무인쇄). 본 라운드는 소유자 웹 스크린이 그 이행 경로","date":"2026-07-07"}

## 5. 외부 웹 스크린 — 붙여넣기 블록 (claude.ai에서 실행)

```
아래는 회계부정 탐지 연구의 '무사기 대조군' 후보 22개사입니다.
각 회사에 대해 다음을 웹에서 확인해 주세요 (컷오프일 기준 ±5년):
1. SEC AAER/회계 집행 조치(본사 또는 전신 법인 대상)가 있는가?
2. 회계 부정·재작성(restatement)·내부고발·감사인 사임 등 회계 신뢰성 사건이 있는가?
3. 있다면 사건명·연도·출처 링크를, 없다면 "확인 안 됨"을 표로 정리해 주세요.

- Air Products & Chemicals, Inc. [APD] — 컷오프 2011-06-28
- Mosaic Co [MOS] (구사명: Global Nutrition Solutions Inc) — 컷오프 2011-06-28
- Celanese Corp [CE] — 컷오프 2011-06-28
- Masimo Corp [MASI] — 컷오프 2013-07-28
- Accuray Inc [ARAY] — 컷오프 2013-07-28
- Merit Medical Systems Inc [MMSI] — 컷오프 2013-07-28
- Teledyne Technologies Inc [TDY] — 컷오프 2013-08-06
- Ciena Corp [CIEN] — 컷오프 2013-08-06
- Garmin Ltd [GRMN] — 컷오프 2013-08-06
- Ryder System Inc [R] — 컷오프 2014-05-12
- Upbound Group, Inc. [UPBD] (구사명: Rent-A-Center Inc) — 컷오프 2014-05-12
- InterDigital, Inc. [IDCC] — 컷오프 2015-08-09
- Rocky Brands, Inc. [RCKY] (구사명: Rocky Shoes & Boots Inc) — 컷오프 2015-08-09
- Dolby Laboratories, Inc. [DLB] — 컷오프 2015-08-09
- First Solar, Inc. [FSLR] — 컷오프 2015-09-10
- Amkor Technology, Inc. [AMKR] — 컷오프 2015-09-10
- Analog Devices Inc [ADI] — 컷오프 2015-09-10 ← 2008 옵션 백데이팅 화해 여부 최우선 확인
- Forrester Research, Inc. [FORR] — 컷오프 2016-02-28
- Exponent Inc [EXPO] (구사명: Failure Group Inc) — 컷오프 2016-02-28
- Liquidity Services Inc [LQDT] — 컷오프 2016-02-28
- General Mills Inc [GIS] — 컷오프 2019-02-20
- Campbell's Co [CPB] (구사명: Campbell Soup Co) — 컷오프 2019-02-20

주의: 동명이인(개인·타사)과 혼동하지 마시고, CIK/티커로 법인을 특정해 주세요.
```
