# Review Packet 01 — 대조군 8 선정 (Phase 2-6, D17 규칙 적용)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 규칙 (사전 고정, decisions_log D17): 자격 = ① 4축 매칭 근거(산업/규모/회계기간/장르,
> 1차 소스 데이터 포인트) ② EDGAR XBRL 실측 ③ 비집행 확인(AAER 색인 부재 + SEC 집행
> 웹 검색, 일자 기록). 자격자 중 **규모+기간 최근접** 선택 (규모 = |log(매출비)| 1차,
> 근소 차이면 FYE 근접 tie-break). 컷오프 = 매칭 실험군 복사 (GP-9 ①).
> 기계 검증 데이터: `data/candidates/control_screening.json` (24후보 스크리닝,
> AAER 색인 3,339건 [AAER 987–4595] 대조 2026-07-06) + 웹 2차 검색 2026-07-06.

## 1. 확정 8건

| C-ID | 대조군 | 매칭 실험군 | 산업(SIC) | 규모 (컷오프 PIT) | FYE | 비집행 확인 |
|---|---|---|---|---|---|---|
| C01 | **MOS** Mosaic | T07 MON | 2870=MON 정확 일치 (농화학) | assets $14.7B (MON ~$17.8B) | 5월* | 색인·웹 음성 |
| C02 | **NUVA** NuVasive | T11 OFIX | 3841 (척추 의료기기 — 사업 정확) | rev $620M (OFIX $462M) | 12월 | 색인·웹 음성 (2015 DOJ FCA는 헬스케어 청구건 — 회계 아님, 주석) |
| C03 | **GRMN** Garmin | T12 LOGI | 3812 (소비자 전자기기) | rev $2.72B (LOGI $2.13B) | 12월 (LOGI 3월 — 불일치 주석) | 색인·웹 음성 |
| C04 | **R** Ryder | T13 HTZ | 7510=HTZ 정확 일치 (차량 임대) | rev $6.4B (HTZ ~$10.8B) | 12월 | 색인·웹 음성 |
| C05 | **PERY** Perry Ellis | T16 ICON | 2320 (의류 브랜드 — ICON 6794과 부분 일치, **최약 매칭**) | rev $890M (ICON $461M) | 1월말 | 색인·웹 음성 |
| C06 | **XLNX** Xilinx | T17 MRVL | 3674=MRVL 정확 일치 (팹리스 반도체) | rev $2.38B (MRVL $3.66B) | 4월초 (MRVL 1월말) | 색인·웹 음성 |
| C07 | **FORR** Forrester | T21 SCOR | 리서치/측정 서비스 | rev $293M (SCOR $369M) | 12월 | 색인 음성; 웹: 옵션 조사 **종결·무조치** (기록) |
| C08 | **GIS** General Mills | T28 KHC | 2040 (포장식품) | rev $15.7B (KHC $26.3B) | 5월 (KHC 12월 — 불일치 주석) | 색인 음성; 웹: 2004 Wells **종결·무조치** (기록) |

\* MOS의 submissions FYE 필드는 현재값(12월, 2017 변경 후) — 컷오프 시점 실측 FYE는
XBRL 연차 기말(5월)로 확인. 스크리닝 필드의 한계로 기록.

## 2. 기각·실격 후보 (전수)

| 후보 | 대상 | 사유 |
|---|---|---|
| **Apex Global Brands (구 Cherokee)** | T16 | **실격 — AAER-4199 실재** (색인 기계 검색 적중) |
| **Gartner** | T21 | **실격 — AAER-4411 실재** (색인 기계 검색 적중) |
| **Avis Budget** | T13 | **실격 — CIK 0000723612 = Cendant Corporation, AAER-1272/1276 (2000-06-14)**. 사명 검색은 음성이었으나 등록자(CIK) 계보 추적으로 발견 — GP-4의 '동일 사건(발행 주체) 귀속' 기준의 일관 적용 |
| **United Rentals** | T13 | **실격 — 2008-09 SEC 회계사기 화해** ($14M, sale-leaseback/trade package, SEC PR 2008-190, D. Conn. 08-cv-01354). AAER 색인에는 무인쇄 — 2차 웹 검색이 잡음 (GP-4 ② '집행조치 기준'상 실격) |
| FMC Corp | T07 | 자격 유지, 규모 기각 (rev $3.1B — |log| 1.22 vs MOS) |
| du Pont (EIDP) | T07 | 자격 유지, 규모 기각 (rev $31.5B — 3x) |
| Integra LifeSciences | T11 | 자격 유지, 규모 기각 ($831M vs NUVA $620M; OFIX $462M 대비 |log| 0.59 vs 0.29) |
| Plantronics | T12 | 자격 유지 — FYE 일치(3월말)이나 규모 열위 ($762M, |log| 1.03 vs GRMN 0.24). **기간축 대안으로 기록** |
| Universal Electronics | T12 | 자격 유지, 규모 기각 ($463M) |
| XCel Brands | T16 | 자격 미달 — 규모축 실패 (rev $20.7M, ICON 대비 22배 괴리; SIC 6794은 정확 일치였음) |
| Skyworks | T17 | 자격 유지 — 근소 기각 (rev $2.29B |log| 0.47 vs XLNX 0.44 + FYE 원거리) |
| Cypress | T17 | 자격 유지, 규모 기각 ($725M) |
| Nielsen | T21 | 자격 유지, 규모 기각 ($6.2B — 17x) |
| Kellanova(K) | T28 | 자격 유지 — 규모 기각 (|log| 0.71 vs GIS 0.51). **FYE 정확 일치(12월) 대안으로 기록** |
| Campbell | T28 | 자격 유지, 규모 기각 ($8.7B, |log| 1.10) |
| Wright Medical | T11 | 미해석 (EDGAR 검색 미적중 — 스크리닝 불능, 후보 제외) |

## 3. 베이스라인 (4스크린 + Piotroski — 전 후보 실행 완료)

`scoring/baselines/results/controls/`. 특기 (false-positive 분석 고가치, D17 주석):
- **GIS: F=1.66(>1.4 플래그)·C=6** — 비집행 확정(2004 SEC 조사 종결) + Piotroski 4.
  "스크린이 플래그하는 건전 기업"의 전형 — 분석 ③의 오탐 해부 1순위.
- CPB F=1.48, XELB F=2.41 (선정 제외분이나 기록).
- 선정 8건 Piotroski 5~8 (재무 건전성 축 확보), Beneish/F 대체로 무플래그.

## 4. 불확실성 종합

1. **C05 PERY가 최약 매칭**: 산업축 부분 일치(의류 제조·브랜드 vs 순수 라이선싱).
   순수 라이선싱 비교군은 Cherokee(실격)·XELB(규모 미달)·Sequential(집행 풀)로
   전멸 — 모집단 자체가 얇음. 장르축(브랜드 무형자산 중심 사업)으로 보완했으나
   ICON 특유의 '라이선시 지원 관련당사자 거래' 구조는 PERY에 없음 — 한계 명기.
2. **비집행 ≠ 무결**: '조용한 미적발' 혼입 가능성 (GP-8 서명 한계) — 특히 스크린
   플래그가 뜬 GIS. 라벨은 "SEC 비집행"이지 "clean"이 아니다.
3. AAER 색인 커버리지: 색인 페이지는 AAER 987(~1998) 이후 촘촘 — 그 이전은 웹
   검색 의존. 선정 8건 전부 웹 2차 검색 병행 완료 (2026-07-06).
4. FYE 필드가 현재값인 스크리닝 한계 (C01 각주) — 선정 판단에는 XBRL 실측 기말 사용.

## 5. 오버라이드 방법 (사후 감사용)

- **개별 교체**: candidates.json의 해당 C-엔트리 교체 + `tools/control_screening.py`
  풀에 신후보 추가 실행 + `tools/build_evaluatee_inputs.py` 재생성 + 매니페스트 재작성.
  freeze 전 비용 ≈ 커밋 1개. **freeze 후·실행 후**: 교체 케이스의 파이프라인 재실행
  (원본 1호출 + 채점 1호출) + §5-6 이력 공개.
- **선정 기준 자체 변경** (예: 규모 1차 → 기간 1차): D17 개정 기록 + 8건 재선정 +
  전 대조군 재실행 (8+8호출).

**학습 노트(§10)**: 기계 검색(색인)과 2차 검색(웹)은 서로의 사각을 메운다 — Gartner/
Cherokee는 색인이, United Rentals는 웹이, Avis는 CIK 계보 추적이 잡았다. "비집행
확인"은 단일 조회가 아니라 세 갈래 교차다.
