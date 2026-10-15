# LITE — 10-K, 2026-06-27 기간 (제출일 2026-08-17) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: 영업현금흐름 7.5억 달러가 영업이익 5.2억 달러보다 커서 영업이익은 현금으로 뒷받침됩니다. 순손실 -69.4억 달러는 현금이 나가지 않는 사채 소멸손실 때문이며, 발생액 비율 -1.052가 과거 최저인 것도 그 때문입니다.
- **매출 인식**: 매출은 83.2% 늘었고 마지막 분기 영업현금흐름이 매출보다 빠르게 늘어, 매출을 앞당긴 징후는 보이지 않습니다. 다만 매출채권이 계약자산으로 태그되어 회전일수를 계산할 수 없고, 최대 고객의 매출채권 비중 30.4%가 매출 비중 26.6%보다 빠르게 올랐습니다.
- **추정치와 충당금**: 법인세 혜택 -2.4억 달러는 대부분 미국 평가충당금 환입이라는 판단에서 나온 일회성 이익입니다. 대손충당금은 매출채권이 크게 늘었는데도 350만 달러에 머물러 있습니다.
- **비용 이연(자본화)**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **현금흐름 조정과 부외 항목**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **내부통제·감사·공시 신호**: 감사의견은 적정이고 중요한 취약점도 없습니다. 하지만 후속사건 주석이 'TBD'로 제출되는 등 작성·태깅 오류가 많고, 이전 분기 수치가 설명 없이 바뀌었습니다.
- **문서 간 대조**: 8-K의 매출 30.1억 달러와 순손실 -69.4억 달러는 10-K와 일치합니다. 그러나 부품·시스템 매출 태그가 서로 뒤바뀌어 있고, 단일 부문이라는 서술과도 모순됩니다.
- **업종 관점(반도체·하드웨어)**: 최대 고객 A의 매출 비중이 26.6%로 전년 15.4%보다 크게 올랐습니다. 재고 6.9억 달러와 구매약정이 함께 늘었지만 재고충당금은 공시되지 않았으며, 우선주를 산 NVIDIA가 주요 고객인지도 알 수 없습니다.

**이상 징후 목록** (47건, 건수 기준 없이 모두 적음)

- 발생액 비율 역대 최저 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 매입채무 증가분과 현금흐름표 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 재고 증감 소폭 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 매출채권 증감 대사 불가 — 이익 대 현금 · 숫자로 판단 불가
- 이익 변동성이 현금보다 훨씬 큼 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 성과급의 주식에서 현금으로 전환 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 매출채권이 한 고객에 매출보다 빠르게 집중 — 매출 인식 · 숫자로 판단 불가
- 매출채권 회전일수 산출 불가 — 매출 인식 · 숫자로 판단 불가
- 계약부채 증가, 일부는 인수한 불리한 계약 — 매출 인식 · 숫자가 설명을 뒷받침
- 고객에게 청구한 관세의 매출 인식 — 매출 인식 · 숫자로 판단 불가
- 그린즈버러 공급계약의 대리인 순액 인식 — 매출 인식 · 숫자로 판단 불가
- 최대 분기 매출, 현금은 더 빠르게 증가 — 매출 인식 · 숫자가 설명을 뒷받침
- 매출채권 급증에도 대손충당금 동결 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 미국 누적손실에도 평가충당금 환입 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 평가충당금 환입액이 공시마다 다름 — 추정치와 충당금 · 숫자로 판단 불가
- 연속된 해의 법인세 혜택 — 추정치와 충당금 · 숫자로 판단 불가
- 보증충당금 비율 소폭 하락 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 영업단위 재편 후 정성평가만 실시 — 추정치와 충당금 · 숫자로 판단 불가
- 태국 투자청 면세 요건 소급 판단 — 추정치와 충당금 · 숫자로 판단 불가
- 미인식 세무혜택 증가 — 추정치와 충당금 · 숫자로 판단 불가
- 비GAAP 조정 항목 확대 — 비용 이연(자본화) · 숫자로 판단 불가
- 기타 비용과 구조조정 비용의 반복 — 비용 이연(자본화) · 숫자로 판단 불가
- 연성자산 비중 최저 — 비용 이연(자본화) · 숫자로 판단 불가
- 미지급 설비투자 급증 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 주식보상 원천징수 세금의 재무활동 분류 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 전환사채 발행대금이 차입 합계에서 누락 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 전환 초과가치의 현금 결제 선택권 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 후속사건 주석이 'TBD'로 제출 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 주석 작성 오류 다수 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 단일 부문 서술과 부문 태그의 모순 — 내부통제·감사·공시 신호 · 숫자가 설명과 모순
- 매출채권을 계약자산으로 태그 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 태그 선택으로 매출총이익률·재고 분석 불가 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 동일한 유동성 부채의 이중 태그 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 그린즈버러 인수가격 배분의 설명 없는 수정 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 클라우드라이트 조건부대가 부호 반전 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 핵심감사사항이 재고 하나뿐 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- CFO의 주식거래계획 변경 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 계속기업 의문 문구 삭제 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 부품·시스템 매출 태그 뒤바뀜 — 문서 간 대조 · 숫자가 설명과 모순
- 보도자료 내 기타 비용 금액 불일치 — 문서 간 대조 · 숫자가 설명과 모순
- 매각예정자산 손상 금액·명칭 불일치 — 문서 간 대조 · 숫자로 판단 불가
- 에스크로 합의금 표시 방식 상이 — 문서 간 대조 · 숫자가 설명을 뒷받침
- 재고 증가, 충당금 미공시 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가
- 구매약정 증가와 취소 조건 약화 — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침
- 고객 집중도 상승 — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침
- 우선주 투자자의 고객 여부 미공시 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가
- 위탁생산업체와의 거래 흐름 불명확 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- Capital spending incurred but unpaid at year end: 1.2억 달러 차감 (`earnings_versus_cash.working_capital.accounts_payable.articulation_gap`)
- US valuation-allowance release inside the income tax benefit: 2.4억 달러 차감 (`terms.trailing_four_quarters.income_tax_expense`)

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **효율성**: 매출채권·재고·매입채무 회전일수와 현금전환주기는 태그 문제로 계산되지 않았고, 총자산회전율은 0.523입니다. 성장 과정에서 매출채권과 재고가 현금을 흡수했고, 그중 상당 부분은 매입채무 증가로 메워졌습니다.
- **유동성**: 유동비율이 1.678로 낮아졌지만, 영업 악화 때문이 아니라 모든 전환사채가 유동부채로 분류되었기 때문이며, 현금과 단기투자는 27.4억 달러로 늘었습니다. 잉여현금흐름이 양수라 현금 소진 기간은 계산되지 않으나, 마지막 분기에는 전환 대금과 세금 납부로 현금이 줄었습니다.
- **지급능력**: 이자보상배율은 24.073, 자산 대비 부채 비율은 36.5%로 건전합니다. 계산된 총부채 32.3억 달러와 EBITDA 대비 부채 4.098은 같은 금액의 두 줄을 이중으로 더해 부풀려져 있으며, 실제 약점은 부채 대부분이 일 년 안에 만기가 오는 것으로 분류된 점입니다.
- **성장**: 마지막 분기 매출은 직전 분기보다 24.5%, 전년 같은 분기보다 109.3% 늘었고, 연간 매출 성장률 83.2%는 회사의 과거 성장률을 크게 웃돕니다. 순이익 성장률은 부채소멸손실 때문에 사업 실적을 보여주지 못하며, 성장은 한 고객에 크게 기대고 있습니다.
- **잉여현금흐름**: 단순 잉여현금흐름은 3.0억 달러로 양수로 돌아섰고, 주식보상과 인수 대금을 뺀 품질조정 잉여현금흐름은 9,190만 달러입니다. 기업잉여현금흐름은 세전이익 행이 없어 계산되지 않았고, 주주잉여현금흐름 -5.0억 달러는 전환사채 발행 대금이 빠져 있어 믿기 어렵습니다.
- **듀퐁 분해**: 자기자본이익률 -240.0%는 순이익률 -230.1%, 총자산회전율 0.523, 자기자본승수 1.995를 곱한 값이며, 이를 좌우하는 것은 부채소멸손실이 만든 순이익률입니다. 자기자본이 자산보다 훨씬 빨리 늘어 레버리지 요인은 줄어들고 있습니다.
- **압박이 위기로 바뀌는 조건**: 현재 공시 수치로 보면 이 회사는 부실과 거리가 멉니다. 부실로 가려면 전환 청구가 현금과 단기투자 27.4억 달러로 감당할 수 없을 만큼 커지거나, 영업이익 5.2억 달러가 이자비용 2,180만 달러를 감당하지 못할 만큼 줄거나, 잉여현금흐름 3.0억 달러가 계속 음수로 돌아서거나, 최대 고객이 구매나 대금 지급을 멈춰야 합니다.

**재무 압박 징후 목록** (22건)

- 세 해 연속 영업손실 뒤의 흑자 전환, 공장 가동률에 의존
- 미국 누적 손실에도 평가충당금 환입에 기댄 법인세 혜택
- 중국 세제 혜택 만료
- 증설 자산의 가동 개시에 따른 감가상각 증가
- 매출 성장에 따른 매출채권과 재고의 현금 흡수
- 한 고객에 집중된 매출채권과 제자리인 대손충당금
- 마지막 분기의 현금 감소
- 주식 순결제에 따른 원천징수 세금 현금 지출
- 미지급 설비투자가 부풀린 잉여현금흐름
- 늘어난 구매 약정과 약해진 해지 조건 문구
- 일 년 내 만기로 분류된 부채와 이중 합산된 레버리지 지표
- 증가하는 미인식 세무 혜택
- 크게 음수로 돌아선 순이익 성장률
- 한 고객에 집중된 매출 성장
- 경영진의 매출총이익률 하락 압력 경고
- 물량 증가를 일부 상쇄한 트랜시버 판매가 하락
- 공급을 넘어선 수요와 물량 배분
- 희토류 무역 제한 언급
- 성장기 중의 인력 감축
- 비경상적 법률 비용과 정부 조사
- 인수 제품 관련 보증충당금 증가
- 비GAAP 기준으로 제시된 실적 헤드라인과 전망

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: 19.5% · 과거 5년 연평균: 11.6%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (free_cash_flow_to_firm: tax_rate: no row for pretax_income in 2025-06-29..2026-06-27: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest, us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments is in the record, but not for this period) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.7% — DGS10 on 2026-08-17; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-08-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 0.7% — interest_expense / average debt; interest_expense the fiscal year
  - 세율: (계산 안 됨: no row for pretax_income in 2025-06-29..2026-06-27: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest, us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments is in the record, but not for this period)
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: 32.3억 달러 — debt_current + debt_noncurrent; 0001628280-26-057358:facts:LongTermDebtCurrent:2026-06-27, 0001628280-26-057358:facts:ShortTermBorrowings:2026-06-27, 0001628280-26-057358:facts:LongTermDebtNoncurrent:2026-06-27
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- **가치 범위**: 주가 시계열이 주어지지 않아 베타와 자기자본비용, 그리고 WACC를 계산할 수 없었고, 그래서 Python은 가치 범위와 시나리오별 기업가치·주당가치를 계산하지 않았습니다. 계산된 자본비용 요소는 무위험이자율 4.7%, 주식위험프리미엄 4.3%, 세전 부채비용 0.7%뿐이며, 법인세율도 세전이익 행이 없어 비어 있습니다.
- **주가의 위치**: 입력 자료에 기준일 주가가 없으므로 주가가 가치 범위의 어디에 있는지 말할 수 없습니다. 주가가 필요한 시가총액, 시장 기업가치, 잉여현금흐름 수익률도 같은 이유로 계산되지 않았습니다.
- **시장이 가정한 성장률**: 역DCF가 계산되지 않아 주가에 담긴 성장률은 제시하지 않습니다. 회사 기록을 보면 2026 회계연도 매출은 83.2% 늘어 최근 세 해 복리 성장률 19.5%와 다섯 해 복리 성장률 11.6%를 크게 웃돌았고, 회사는 2027 회계연도 첫 분기 매출을 마지막 분기 매출 1,006,300,000.000보다 높게 제시했습니다.
- **가장 민감한 가정**: 민감도 표가 계산되지 않아 가치가 어느 가정에 가장 민감한지는 읽을 수 없습니다. 대신 회사 기록과 비교하면 판단이 가장 많이 들어간 가정은 첫해 매출 성장률과 영업이익률 경로로, 기본·낙관 시나리오의 첫해 성장률은 세 해 복리 성장률 19.5%를 크게 넘고, 열째 해 영업이익률은 비관 시나리오에서 2022 회계연도의 17.7%보다 낮고 낙관 시나리오에서 2021 회계연도 고점 30.2% 수준입니다.
- **회계 조정이 바꾼 가치**: 가치 계산이 없었으므로 회계 조정이 가치를 얼마나 움직였는지는 계산되지 않았습니다. 회계 분석에서 나온 미지급 설비투자와 미국 평가충당금 환입 두 조정은 품질조정 잉여현금흐름에만 적용되어 91,900,000.000을 -2.7억 달러로 낮췄고, 같은 유동부채가 두 번 태그되어 계산된 순부채 5.0억 달러는 부풀려져 있습니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for receivables in 2026-06-27: us-gaap:ReceivablesNetCurrent, us-gaap:AccountsAndOtherReceivablesNe)
- accruals_over_assets: 계산 안 됨 (current year: no row for income_taxes_payable in 2026-06-27: us-gaap:AccruedIncomeTaxesCurrent, us-gaap:TaxesPayableCurr)
- net_operating_assets: 0.840
- piotroski_f_score: 계산 안 됨 (current year: no row for common_stock_issued in 2025-06-29..2026-06-27: us-gaap:ProceedsFromIssuanceOfCommonStock, us-ga)
- altman_z_score: 계산 안 됨 (current year: no row for pretax_income in 2025-06-29..2026-06-27: us-gaap:IncomeLossFromContinuingOperationsBeforeIncome)
- ohlson_o_score: -3.726

## 계산하지 못한 항목

- free_cash_flow_to_firm: tax_rate: no row for pretax_income in 2025-06-29..2026-06-27: us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest, us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments is in the record, but not for this period
- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
