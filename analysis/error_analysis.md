# error_analysis — 케이스별 실패 분류·유형 계층화·조기성 (RP-10 Phase 3)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> 분류 체계 (사전 지정): (i) 컷오프 전 입력에 증거 부재 (ii) 증거 존재하나
> 추론 실패 — 놓친 구절 인용 의무 (iii) 정답/라벨 문제 (iv) 공개 재무제표
> 구조상 탐지 불능. 판정 프레임 = 1차(원본 v 원본), 플래그 임계 p≥50 (동결
> 루브릭). 모든 분류에 구체 출처 인용. 미스도 히트만큼 분석한다.

## 1. 실험군 미탐 2건 (원본 프레임, p<50)

### T07 Monsanto (p=28 → 미탐) — **분류 (ii): 증거 존재, 추론이 정체 사전확률에 꺾임**

- **놓친(정확히는 '기각한') 구절 — 모델 자신의 top_signals 원문**:
  > "Gross margin compressed sharply (57.7% FY2009 vs 48.4% FY2010) driven by
  > CostOfGoodsSold rising 9.1% … while SalesRevenueNet fell 10.4% …
  > **plausibly explained by well-known glyphosate/Roundup pricing pressure
  > rather than misstatement**"
  마진 압축은 AAER-3741이 기술한 리베이트 비용 이연·오분류(SG&A 처리)의 재무
  발자국과 같은 방향이다 — 모델은 신호를 **보고, 인용하고, 회사 정체 지식
  ("well-known … Roundup")으로 설명해 없앴다**. 같은 숫자의 정체 은닉 변형은
  p=58 (k=5 평균 54.8, Δmean = +15.8, 2SE 밖 — `scoring/rp07_stats.json`).
- 출처: 모델 출력 `runs/main/case_06.json` overall.top_signals[1]; 정답
  AAER-3741 (2016-02-09) — 2009-2011 리베이트 프로그램 비용 인식 이연.
- 보조 요인 — **분류 (i) 부분 병존**: 리베이트 부채 자체는 페이로드의
  `AccruedLiabilitiesCurrent` 집계에 매몰 (기확정 귀속 DATA(설계), D-계열
  J10 — XBRL 태그 분해능). 결정적 계정 수준 증거는 숫자 입력 공간에 없었다.

### T12 Logitech (p=42 → 미탐) — **분류 (ii): 증거 존재, 순위 판단 실패**

- **놓친 구절 — 모델의 3순위 가설이 정답 기제를 사실상 포착하고도 3순위·p=42**:
  > "Inventory build-up in FY2012 (InventoryNet=297,072,000 at 2012-03-31 vs
  > 280,814,000 at 2011-03-31) despite a revenue decline … could indicate
  > **delayed recognition of inventory obsolescence/excess reserves**"
  정답(AAER-3765/34-77644): Revue 셋톱박스 재고의 LCM 감액 ~$30.7M 지연
  (FY2011) + 워런티 부채 과소. 모델은 재고 지연 감액 가설을 세웠으나 goodwill
  서사를 1순위로 올리고 확신을 42에 묶었다.
- 출처: `runs/main/case_03.json` mechanism_hypotheses[2]; LOGI FY2012 10-K
  (filed 2012-05-30) 재고·매출 계열 (페이로드 실측 값과 일치).

## 2. 검출 6건의 기제 정합 주석 (히트도 해부한다)

| 케이스 | p | d2(기제) | 요약 |
|---|---|---|---|
| OFIX | 60 | 2 | 계정·방향·처리유형 실질 일치 (채널 스터핑 가설 vs 조건부 유통사 매출) |
| SCOR | 55 | 1 | 계정 영역(매출/AR)·방향 일치, 특이 기제(barter $34.5M)는 미포착 |
| ICON | 65 | 1 | 매출 축 일치, 특이 기제(JV buy-in 이익 인식)는 미포착 |
| HTZ | 78 | 0 | **점수는 맞고 기제는 틀림** — PPA/goodwill 서사; 정답은 추정 계정(충당금·감가) 조작 |
| KHC | 68 | 0 | 동상 — 매출/AR 서사; 정답은 조달 COGS 스킴 |
| MRVL | 55 | 0 | 동상 — 옵션 백데이팅(2006-07) 서사; 정답은 pull-in (창 2015) |

검출 6/8 중 기제가 계정 영역이라도 맞은 것은 3건 — "높은 p"와 "옳은 이유"는
별개 축이며, HTZ는 각인된-유죄(Δ −30.2)와 겹쳐 읽어야 한다 (§3.5 그림).

## 3. 유형 계층화 (AAER 모집단 대비)

지배 기제 기준 (다중 기제는 genre_tags.md의 우세 축):

| 유형 | 본 표본 (n=8) | 검출 | AAER 모집단 (Anti-Fraud Collaboration, 531건 2014-2019) |
|---|---|---|---|
| 매출 인식 | 4 (OFIX·SCOR·MRVL·ICON) | 4/4 | 43% |
| 준비금/추정 | 1 (HTZ) | 1/1 | 24% |
| 재고 | 1 (LOGI) | 0/1 | 11% |
| 비용/리베이트 (COGS·기타) | 2 (MON·KHC) | 1/2 | — (모집단 표는 loan impairment 11% 등) |

표본은 매출 인식에 과대 표집(50% vs 43%)이고 loan impairment(모집단 11%)는 0건
— 금융업 제외 설계의 직접 결과. **이 표본이 커버하지 않는 것**: 금융업 대손,
역합병/신규 상장 셸, 비-XBRL 시대(2009 이전) 스킴.

## 4. 조기성 (검출 케이스 — 최상위 가설 증거의 제출 시점 기준)

| 케이스 | 결정 증거 최초/완성 제출 | 폭로 전 (분기) | 단서 |
|---|---|---|---|
| SCOR | 2015-02 10-K | 4q / 4q | d2=1 (계정 영역 정합) |
| OFIX | 2013-03 10-K | 1q / 1q | d2=2 |
| ICON | 2015-05 10-Q | 1q / 1q | d2=1 |
| KHC | 2018-05 / 2018-08 10-Q | 3q / 2q | **d2=0 — 틀린 기제의 조기성** |
| HTZ | 2014-03 10-K(/A) | 0q / 0q | d2=0, 폭로 직전 신호 |
| MRVL | 2010-06 (백데이팅 서사) | (21q) | **d2=0 — 무관 신호라 조기성 무의미, 제외** |

기제 정합(d2≥1) 검출 3건의 조기성 = 폭로 전 1~4분기. 문맥: 집행 DB는 최초
폭로에 평균 150–1,017일 후행한다 (Karpoff, Koester, Lee & Martin) — 본 측정의
"폭로"는 최초 공개 폭로일(컷오프)이지 AAER 발행일이 아니다. 체계적 시간축
측정은 docs/EARLINESS_DESIGN.md (설계만, 미실행).

## 5. 대조군 오탐 3건 (p≥50 — FP 3/22, Clopper-Pearson 95% [2.9%, 34.9%])

### Liquidity Services (LQDT, p=65) — 분류 (ii): 실제 부진·손상의 과잉 해석

- 모델 top 가설: "Goodwill/intangibles … carried at levels not supported by
  the underlying businesses' cash-generating ability" — 인용 실측: goodwill
  $40.5M(2011-09) → $150.8M(2011-12, 인수) → $209.7M(2014-09) → $122.6M(2014-12).
- 실제: 인수 후 사업 부진과 **합법적 손상 인식**의 궤적이다 (LQDT FY2014 10-K
  손상 공시). 곤경(distress)과 분식(misstatement)의 혼동 — RP-05의 Ryder
  오탐과 같은 축의 추론 실패.

### Rocky Brands (RCKY, p=55) — 분류 (ii): 계절 재고 사이클의 과잉 해석

- 모델 top 가설: FY2013 NI +$7.4M vs OCF −$2.5M + 재고 +16.4% vs 매출 +7.2%.
- 실제: 부츠 제조업의 계절 재고 축적 패턴 (RCKY FY2013 10-K 재고·현금흐름 주석)
  — 수치는 실재하나 "aggressive channel loading" 추론은 근거 초과.

### Forrester Research (FORR, p=55) — 분류 (iii): 라벨 창 문제 + 템플릿 재사용

- 모델 top 가설: 2006-02 연속 10-Q/A 2건을 "options backdating 시대" 서사로
  연결해 pre-2007 주식보상 과소계상을 주장.
- 구조적 문제 둘: ① **청정 라벨의 시간 창** — E5 무재작성 조건은
  [컷오프−5y, +3y] = [2011, 2019]만 검사하는데 페이로드 filing_chronology는
  전 이력을 노출한다. 2006년 옵션 검토 시대의 정정 이력은 "clean" 라벨의
  검사 범위 밖이므로, 이 플래그는 라벨 정의와 입력 범위의 불일치를 짚은 것.
  ② MRVL 실험군에서도 동일한 "10-Q/A 군집 + 2006-07 → 백데이팅" **템플릿**이
  등장 (거기서도 정답 기제와 무관) — 모델의 재사용 서사이며, 이 표본에서
  2/2 모두 판정에 도움이 되지 않았다.

**공통 노트**: 세 오탐 모두 인용 수치 자체는 페이로드 실측과 일치한다 (날조
없음, d4 계열 강점 유지). 실패는 사실→추론 단계다: 합법적 곤경·계절성·창
밖 역사를 분식 신호로 승격. 아울러 GP-8 (비집행 ≠ clean): 이 3사 중 어느
하나가 미적발 실제 문제일 가능성은 배제 불능 — 그 방향의 오차는 측정
특이도를 **낮추는** 쪽이므로 본 결과는 그 축에서 보수적이다.
