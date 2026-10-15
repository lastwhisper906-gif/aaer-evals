# FLEX — 10-Q, 2026-06-26 기간 (제출일 2026-07-31) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: 최근 누적 연간 기준 영업현금흐름은 순이익의 1.605배로 이익이 아직 현금으로 뒷받침되지만, 이번 분기에는 영업현금흐름(276,000,000.000)이 순이익(285,000,000.000)보다 적어 과거와 달라졌습니다. 매입채무가 34.0억 달러 늘어 매출채권과 재고 증가를 메웠기 때문에, 현금흐름이 공급업체 신용에 기대고 있다는 점에 주의해야 합니다.
- **매출 인식**: 이번 분기 매출채권 회수일수는 55.3일로 기록된 분기 중 가장 길고, 매출이 20.6% 늘어나는 동안 매출채권은 11.1억 달러 늘었습니다. 회사는 그 이유를 설명하지 않았고 계약부채는 매출 대비 줄어들어, 매출 인식 쪽은 경계가 필요합니다.
- **추정치와 충당금**: 대손충당금 비율이 0.2%로 과거보다 얇아졌는데, 같은 시기 매출채권은 사상 최고 수준이어서 충당금이 부족할 수 있습니다. 구조조정 환입과 조건부 대가 환입이 이익을 늘렸지만 규모는 작고, 재고·보증 충당금은 태그가 없어 확인할 수 없습니다.
- **비용 이연(자본화)**: 연구개발비 자본화 여부는 자료가 없어 검증할 수 없지만, 연성자산 비중이 78.2%로 역대 최고입니다. 유형자산이 늘었는데도 감가상각비는 전년 분기보다 적고, 분사 비용 같은 '일회성' 비용이 반복되며 비GAAP 이익에서 빠지고 있습니다.
- **현금흐름 조정과 부외 항목**: 공급망 금융 잔액은 1.3억 달러로 작고 거의 변하지 않아 영업현금흐름을 부풀린 증거는 없습니다. 다만 매출채권 매각 규모는 자료에 없어 측정할 수 없고, 계산기의 주주 잉여현금흐름 44.1억 달러는 차입금 상환이 잡히지 않아 과대 계상되어 있습니다.
- **내부통제·감사·공시 신호**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **문서 간 대조**: 8-K 실적 발표의 매출 79.3억 달러, 영업현금흐름 2.8억 달러 등 숫자는 10-Q와 일치하며, 방향성을 가진 주석 항목 중 숫자와 모순되는 것은 없습니다. 다만 구조조정을 문서마다 '인식'과 '환입'으로 다르게 설명하고, EPP 인수를 중요하지 않다고 하면서 성장 요인으로 드는 등 설명이 엇갈립니다.
- **업종 관점(반도체·하드웨어)**: 한 고객이 이번 분기 매출의 12.0%를 차지하고 상위 고객 비중도 높아지는 등 고객 집중이 커지고 있으며, 그 매출은 분사 예정 부문에 몰려 있습니다. 재고일수는 과거 대비 낮은 편이지만 재고 충당금과 구매 약정은 자료에 없어 진부화 위험은 확인할 수 없습니다.

**이상 징후 목록** (44건, 건수 기준 없이 모두 적음)

- 최근 분기 순이익이 영업현금흐름을 넘어섬 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 최근 누적 현금전환율이 직전 회계연도들보다 낮아짐 — 이익 대 현금 · 숫자로 판단 불가
- 매입채무 증가가 영업현금흐름을 떠받침 — 이익 대 현금 · 숫자로 판단 불가
- 매출채권과 재고 증가가 각각 연간 순이익을 웃돎 — 이익 대 현금 · 숫자로 판단 불가
- 현금흐름표와 재무상태표의 운전자본 변동 대사 불가 — 이익 대 현금 · 숫자로 판단 불가
- 순이익 변동이 영업현금흐름 변동보다 작음 — 이익 대 현금 · 숫자로 판단 불가
- 사업 매각 이익이 분기 순이익을 끌어올림 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 매출채권 회수일수가 기록상 최고 — 매출 인식 · 숫자로 판단 불가
- 매출 증가에도 계약부채(선수금) 감소 — 매출 인식 · 숫자로 판단 불가
- 미청구 계약자산이 분기 중 증가 — 매출 인식 · 숫자로 판단 불가
- 고객에게 부여한 워런트가 매출에서 차감되며 분사 시 가속 행사 가능 — 매출 인식 · 숫자로 판단 불가
- 매출 성장에 가격 전가와 인수 매출 포함 — 매출 인식 · 숫자가 설명을 뒷받침
- 고객 통제 재고 증가로 기타유동자산 증가 — 매출 인식 · 숫자로 판단 불가
- 매출채권은 최고인데 대손충당금 비율은 하락 — 추정치와 충당금 · 숫자로 판단 불가
- 퇴직급여 추정 환입으로 영업이익 증가 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 조건부 대가 부채 전액 환입 — 추정치와 충당금 · 숫자로 판단 불가
- EPP 영업권·무형자산 배분이 잠정적이며 내용연수가 긺 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 관세 환급금의 회계 처리 위치 미공시 — 추정치와 충당금 · 숫자로 판단 불가
- 해외 세무 합의 관련 공시 삭제 — 추정치와 충당금 · 숫자로 판단 불가
- 우크라이나 공장 피격 손실 내역이 주석에서 빠짐 — 추정치와 충당금 · 숫자로 판단 불가
- 법인세 비용이 전년 대비 증가 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 연성자산 비중이 역대 최고 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 유형자산·설비투자는 늘었는데 감가상각비는 감소 — 비용 이연(자본화) · 숫자로 판단 불가
- 일회성이라던 비용이 반복되며 비GAAP에서 제외 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 매출채권 매각(팩토링)이 있으나 규모 측정 불가 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 대출 신디케이션으로 차입·상환이 부풀려지고 계산기는 상환을 누락 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 주식보상비용 증가 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 분사 분리 비용이 영업현금흐름에 반영 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 싱가포르 외 보유 현금 비중이 설명 없이 급변 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 인수가 있었던 분기에도 내부통제 변화 없음으로 보고 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 최고회계책임자의 주식 매도 거래계획 채택 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 임원 변경 등 8-K 본문이 자료에 없음 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 대출 계약 체결 월이 서로 다르게 기재 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 통화스와프의 재무상태표 계정 위치 불일치 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 실적 발표의 비GAAP 주석이 가이던스 분기를 잘못 표기 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 부채 주석에서 약정 준수 문구와 신용한도 설명 삭제 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 순이익 XBRL 태그가 전년 분기와 달라짐 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 사업부문 재편 및 소비자기기 시장 구분 삭제 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 회계기준 관련 문단이 설명 없이 삭제 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 구조조정을 문서마다 인식·환입·다른 금액으로 서술 — 문서 간 대조 · 숫자로 판단 불가
- MD&A의 매출총이익률 개선 폭이 계산값보다 큼 — 문서 간 대조 · 숫자로 판단 불가
- EPP 인수를 중요하지 않다면서 성장 요인으로 제시 — 문서 간 대조 · 숫자로 판단 불가
- 고객 집중도 상승, 분사 예정 부문에 집중 — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침
- 재고일수가 전년 대비 상승(과거 대비로는 낮은 수준) — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- 없음

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: 최근 네 분기 합산 기준 매출총이익률 9.5%, 영업이익률 5.0%, 순이익률 3.3%로 마진은 얇지만, 연간 매출총이익률 9.4%가 기록된 연도 중 최고이고 영업이익률도 다년 평균 4.2%보다 높아 수익성은 개선되고 있습니다. 투하자본이익률(ROIC)은 분기 세전이익 태그가 없어 계산되지 않았습니다.
- **효율성**: 분기 매출채권 회수기간(DSO)은 55.3일로 기록상 최고이고 재고도 늘었지만, 매입채무 지급기간이 103.3일로 길어 현금전환주기는 32.9일로 짧게 유지됩니다. 즉 공급업체 신용이 운전자본을 떠받치고 있습니다.
- **유동성**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **지급능력**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **성장**: 분기 매출은 전년 대비 20.6%, 영업이익은 26.0% 늘었지만 일부는 메모리 가격 전가와 EPP 인수 덕분입니다. 반면 영업현금흐름 증가율은 전년 대비 -30.8%로, 이익 성장이 현금으로 이어지지 않고 있습니다.
- **잉여현금흐름**: 최근 네 분기 단순 잉여현금흐름은 8.3억 달러로 양수지만, 주식보상과 인수 대금을 빼면 -4.7억 달러로 음수입니다. 주주잉여현금흐름 44.1억 달러는 차입 상환 항목이 기록에 없어 부풀려져 있고, 기업잉여현금흐름은 세율을 구할 분기 세전이익 태그가 없어 계산되지 않았습니다.
- **듀퐁 분해**: 자기자본이익률 18.4%는 순이익률 3.3% × 자산회전율 1.320 × 자기자본승수 4.186의 곱이며, 이를 떠받치는 것은 얇은 마진이 아니라 높은 자기자본승수(레버리지)입니다. 이번 분기 차입금과 매입채무로 자산이 크게 늘어 승수는 높아지는 방향입니다.
- **압박이 위기로 바뀌는 조건**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)

**재무 압박 징후 목록** (13건)

- 현금과 매출채권만으로는 부족한 유동부채 상환 능력
- 인수용 정기대출 이후 늘어나는 부채와 이자비용
- 레버리지와 무형자산 비중이 높아진 재무상태표
- 메모리 가격 상승과 함께 늘어나는 재고
- 늘어난 매입채무에 기대 유지되는 짧은 현금전환주기
- 마진이 아닌 레버리지가 떠받치는 자기자본이익률
- 메모리 가격 전가로 희석되는 얇은 마진
- 높아진 유효세율
- 새로 언급된 중동 분쟁과 호르무즈 해협 물류 차질
- 관세를 고객에게 전가하는 데 대한 의존
- 분사 시 조기 가득될 수 있는 고객 워런트(매출 차감)
- 이익은 늘지만 모든 구간에서 줄어드는 영업현금흐름
- 일부는 메모리 가격·관세 전가·인수에서 나온 매출 성장

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: -0.7% · 과거 5년 연평균: 3.0%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (free_cash_flow_to_firm: tax_rate: pretax_income over the trailing four quarters needs the this year to date: no row for pretax_income in 2026-04-01..2026-06-26: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest, us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments is in the record, but not for this period) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.8% — DGS10 on 2026-07-31; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-07-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 5.0% — interest_expense / average debt; interest_expense prior_fiscal_year + this_year_to_date - prior_year_to_date
  - 세율: (계산 안 됨: pretax_income over the trailing four quarters needs the this year to date: no row for pretax_income in 2026-04-01..2026-06-26: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest, us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments is in the record, but not for this period)
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: 52.2억 달러 — debt_current + debt_noncurrent; 0000866374-26-000030:facts:LongTermDebtCurrent:2026-06-26, 0000866374-26-000030:facts:LongTermDebtNoncurrent:2026-06-26
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- **가치 범위**: 주가 자료가 주어지지 않아 베타, 시가총액, 자기자본비용을 구할 수 없었고, 그래서 WACC와 DCF 가치 범위가 계산되지 않았습니다. 기본 시나리오는 첫해 매출 성장률을 최근 네 분기 성장률 12.2%보다 조금 높게, 최근 세 회계연도 연복리 성장률 -0.7%보다는 훨씬 높게 잡았습니다. 즉 최근의 회복이 이어진다는 판단입니다.
- **주가의 위치**: 주가 자료가 없어(Tiingo 토큰 없음) 주가가 가치 범위의 어디에 있는지 판단할 수 없습니다. 순부채 23.8억 달러 같은 재무상태표 쪽 자료만 남아 있습니다.
- **시장이 가정한 성장률**: 역DCF가 실행되지 않아 현재 주가가 몇 퍼센트의 성장을 가정하는지는 알 수 없고, 추정하지도 않습니다. 비교 기준으로 보면 회사의 최근 세 회계연도 연복리 성장률은 -0.7%, 최근 네 분기 성장률은 12.2%이고, 회사의 연간 가이던스는 이보다 훨씬 높은 성장을 제시합니다.
- **가장 민감한 가정**: 민감도 표가 계산되지 않아 가치에 가장 큰 영향을 주는 가정을 표에서 읽을 수는 없습니다. 대신 회사의 과거 기록과 가장 멀리 떨어진 가정은 첫해 매출 성장률과 열째 해 영업이익률입니다. 기본·낙관 시나리오의 장기 영업이익률은 과거 최고치 4.9%보다 높습니다.
- **회계 조정이 바꾼 가치**: 회계 분석에서 조정 항목을 하나도 쓰지 않았고 가치 평가도 계산되지 않아, 회계 조정이 가치를 움직인 정도는 없습니다. 다만 매입채무가 34.0억 달러 늘어 현금흐름을 떠받쳤기 때문에, 모든 시나리오에서 첫해 재투자율을 높게 잡았습니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for depreciation_and_amortization in 2025-04-01..2026-03-31: us-gaap:DepreciationDepletionAndAmorti)
- accruals_over_assets: 계산 안 됨 (current year: no row for income_taxes_payable: the companyfacts record tags none of us-gaap:AccruedIncomeTaxesCurrent, u)
- net_operating_assets: 계산 안 됨 (current year: no row for short_term_investments: the companyfacts record tags none of us-gaap:ShortTermInvestments, us-g)
- piotroski_f_score: 8.000
- altman_z_score: 계산 안 됨 (Altman's fourth ratio is the market value of equity over the book value of total debt, and no market value of equity was)
- ohlson_o_score: -4.233

## 계산하지 못한 항목

- free_cash_flow_to_firm: tax_rate: pretax_income over the trailing four quarters needs the this year to date: no row for pretax_income in 2026-04-01..2026-06-26: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest, us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments is in the record, but not for this period
- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
