# FELE — 10-Q, 2026-06-30 기간 (제출일 2026-07-29) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **매출 인식**: 이번 분기 매출이 두 가지 정밀도로 보고되는 바람에 이번 분기 매출채권회전일수(DSO)는 계산되지 않았습니다. 연간 DSO는 0만 달러일에서 2025 회계연도 0만 달러일로 올라 다섯 해 가운데 두 번째로 높으며, 수익인식 정책 변경이나 결제조건 연장, 미인도청구 판매에 대한 언급은 없습니다.
- **추정치와 충당금**: 대손충당금 비율이 이번 분기 말 0.9%로 기록상 가장 낮아졌습니다. 직전 분기 1.6%에서 급감하는 동안 매출채권은 늘었는데 회사는 이유를 설명하지 않으며, 제품보증충당금 비율도 2025 회계연도 0.4%로 다섯 해 중 가장 낮습니다.
- **비용 이연(자본화)**: 소프트웨어 자본화처럼 비용을 이연했는지 시험할 수치는 없으며, 연성자산 비중이 오른 것은 인수(7,690만 달러) 때문입니다. 조정 EPS는 소송 합의금과 구조조정 비용을 빼면서도 금액이 공개되지 않은 관세 환급과 판관비에 잡힌 주식스왑 이익은 그대로 두어 비대칭적으로 구성되어 있습니다.
- **현금흐름 조정과 부외 항목**: 공시에도 태그에도 매출채권 매각(팩토링)이나 공급망 금융의 흔적은 없으며, 매입채무의 전년 대비 변동도 -69만 달러에 그칩니다. 다만 계산기가 산출한 주주잉여현금흐름 8.0억 달러는 차입금 상환액을 빼지 못해 과대계상되었으므로 사용해서는 안 됩니다.
- **내부통제·감사·공시 신호**: 통제 항목은 공시통제가 유효하고 내부통제에 변화가 없다고 밝히며, 감사인 교체나 재작성, 지연 제출의 신호는 없습니다. 다만 감사보고서와 여러 첨부서류가 입력에 없어 점검 범위가 제한되고, 주요 수치가 두 가지 정밀도로 태그되어 핵심 비율을 계산하지 못했습니다.
- **문서 간 대조**: 주석과 경영진 설명 가운데 수치와 모순되는 항목은 없으며, 인수, 소송 합의, 세율, 자사주 매입에 관한 설명은 수치로 확인됩니다. 실적 발표문과 10-Q의 GAAP 수치는 일치하지만, 발표문은 MD&A가 언급한 관세 환급을 다루지 않고 유기적 물량 성장을 강조해 둘의 강조점이 다릅니다.
- **업종 관점(반도체·하드웨어)**: 재고충당금이 태그되지 않아 재고 진부화는 측정할 수 없지만, 이번 분기 재고일수는 0만 달러일로 여섯 분기 가운데 가장 낮습니다. 고객 집중 정보는 없고 구매약정은 소규모 구리 계약뿐이며, 채널 밀어내기는 이번 분기 DSO가 없어 확인할 수도 배제할 수도 없습니다.

**이상 징후 목록** (29건, 건수 기준 없이 모두 적음)

- 매출채권의 현금 흡수 확대 — 이익 대 현금 · 숫자로 판단 불가
- 매출채권 대차대조표 변동과 현금흐름표 변동의 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 재고자산 대차대조표 변동과 현금흐름표 변동의 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 첫 분기 발생액 비율의 전년 대비 상승 — 이익 대 현금 · 숫자로 판단 불가
- 비현금성 연금 정산손실로 부풀려진 2025 회계연도 현금전환율 — 이익 대 현금 · 숫자로 판단 불가
- 매입채무·미지급비용이 떠받친 영업현금흐름 개선 — 이익 대 현금 · 숫자로 판단 불가
- 보고된 매출채권에 포함된 주식스왑 자산 — 매출 인식 · 숫자가 설명을 뒷받침
- 매출채권 증가 속 대손충당금 비율 사상 최저 — 추정치와 충당금 · 숫자로 판단 불가
- 과거 대비 얇아진 제품보증충당금 — 추정치와 충당금 · 숫자로 판단 불가
- 에쏘 소송 합의금 충당: 회사 몫만 계상, 손해액·경고 문구 삭제, 법원 승인 대기 — 추정치와 충당금 · 숫자로 판단 불가
- 밝혀지지 않은 일회성 항목에 따른 유효세율 상승 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 조정 실적에서 제외되지만 반복되는 구조조정 비용 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 비용은 빼고 관세 환급과 스왑 이익은 남긴 조정 이익 — 비용 이연(자본화) · 숫자로 판단 불가
- 세전 금액으로 표시된 합의금 가산 조정 — 비용 이연(자본화) · 숫자로 판단 불가
- 인수로 인한 무형·연성자산 비중 상승 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 자사주 매입 감소만 언급하고 리볼버 차입은 빠진 MD&A — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 총 차입액을 순차입으로 계산한 주주잉여현금흐름 — 현금흐름 조정과 부외 항목 · 숫자가 설명과 모순
- 처음 나타난 비지배지분 배당 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 유월 말 통화선도 잔액 없음 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 주요 수치의 이중 정밀도 태그 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- MD&A 매출 증감 설명의 문안 오류 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 실적 발표문 내 조정 희석 EPS의 두 가지 표기 — 문서 간 대조 · 숫자로 판단 불가
- 발표문은 합의, 10-Q 태그는 계류 중인 소송 — 문서 간 대조 · 숫자로 판단 불가
- MD&A에는 있고 발표문에는 없는 관세 환급 — 문서 간 대조 · 숫자로 판단 불가
- CEO의 유기적 물량 성장 주장과 MD&A 설명의 차이 — 문서 간 대조 · 숫자로 판단 불가
- CEO의 탈수 수요 언급과 MD&A의 탈수장비 매출 감소 — 문서 간 대조 · 숫자로 판단 불가
- 환율 항목에 포함된 초인플레이션 국가 가격 인상 — 문서 간 대조 · 숫자로 판단 불가
- 도매업체 인수를 제조 부문에 편입 — 문서 간 대조 · 숫자가 설명을 뒷받침
- 연간 재고일수 상승, 재고충당금 정보 없음 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- 없음

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **효율성**: 최근 네 분기 기준 재고일수는 149.9일로 2024년의 135.8일보다 길고, 매출채권은 한 해 전보다 3,721만 달러 늘었는데 대손충당금은 오히려 줄었습니다. 매입채무는 거의 그대로여서 운전자본이 현금을 묶어 두고 있으며, 매출채권회전일수와 현금전환주기는 계산되지 않았습니다.
- **유동성**: 유동비율은 2.406으로 넉넉하지만 당좌비율은 0.987로 재고에 기대고 있고, 현금은 9,728만 달러로 한 해 전보다 적습니다. 잉여현금흐름이 플러스여서 현금 소진 기간은 계산되지 않았으며, 연초 이후 리볼버 차입이 늘어 단기부채는 커지고 남은 한도는 줄었습니다.
- **지급능력**: 부채 총액, 순부채, EBITDA 대비 부채, 이자보상배율은 원자료가 두 가지 값으로 보고되었거나 태그가 없어 계산되지 않았습니다. 한 해 전 부채 2.8억 달러는 자기자본 12.6억 달러보다 훨씬 작았고 자기자본은 14.1억 달러로 늘었지만, 평균 차입금 증가로 이자비용은 오르고 있습니다.
- **성장**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **잉여현금흐름**: 최근 네 분기 단순 잉여현금흐름은 2.2억 달러이고, 주식보상과 인수 지출을 뺀 품질 조정 잉여현금흐름도 1.3억 달러로 플러스입니다. 기업 잉여현금흐름은 감가상각비가 두 가지 값으로 보고되어 빠졌고, 주주 잉여현금흐름 8.0억 달러는 차입 상환이 반영되지 않아 과대 계산된 값이므로 그대로 읽으면 안 됩니다.
- **듀퐁 분해**: 순이익률, 자산회전율, 자기자본승수가 모두 두 가지 값으로 보고된 원자료 때문에 계산되지 않아, 어느 요인이 자기자본이익률을 이끄는지와 그 변화는 이 자료로 말할 수 없습니다. 다만 한 해 전 부채 2.8억 달러가 자기자본 12.6억 달러보다 훨씬 작아 레버리지가 주된 동력으로 보이지는 않습니다.
- **압박이 위기로 바뀌는 조건**: 현재 자료에는 재무적 곤경의 징후가 없으며, 곤경에 이르려면 영업이익 2.8억 달러가 이자비용 수준으로 무너지거나, 잉여현금흐름 2.2억 달러가 마이너스로 돌아서거나, 단기 리볼버 차입의 차환이 막히는 일이 함께 일어나야 합니다. 지켜볼 조건은 매출채권과 재고의 증가, 그리고 매출총이익률 35.0%의 추가 하락입니다.

**재무 압박 징후 목록** (21건)

- 인수가 주도한 분기 매출 성장
- 에너지 시스템 부문 영업이익, 전년 동기보다 감소
- 조정 EPS: 합의 비용은 빼고 관세 환급 이익은 유지
- 주식 스왑 손익 반전이 영업이익 증가를 부풀림
- 당좌비율 기준선 하회, 현금은 전년보다 감소
- 에소 소송 합의금 계상, 법원 승인 후 현금 지급 예정
- 인수 지출이 잉여현금흐름의 상당 부분을 흡수
- 조달 자재와 물류의 인플레이션 압력
- 수자원 시스템 부문의 불리한 제품·지역 믹스
- 대형 탈수 장비 매출 감소
- 중남미·유럽의 유기적 매출 감소
- 수자원 시스템 분기 성장 요인에 물량이 빠짐
- 최근 분기 중 최저 수준의 매출총이익률
- 규모가 밝혀지지 않은 관세 환급이 분기 이익률을 끌어올림
- 수자원 시스템 부문 구조조정 비용 급증
- 밝혀지지 않은 일회성 요인에 따른 유효세율 상승
- 매출채권은 늘고 대손충당금은 줄어듦
- 과거보다 긴 재고일수
- 매입채무는 그대로인데 운전자본은 증가
- 인수로 영업권·무형자산 증가
- 영업현금흐름, 최근 네 분기 기준 정체이며 2023년보다 낮음

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: 1.4% · 과거 5년 연평균: 11.3%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (free_cash_flow_to_firm: depreciation_and_amortization: depreciation_and_amortization over the trailing four quarters needs the this year to date: us-gaap:DepreciationDepletionAndAmortization for 2026-01-01..2026-06-30 is reported as [33895000.0, 33900000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.7% — DGS10 on 2026-07-29; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-07-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 5.7% — fallback: the risk-free rate plus one point, because interest expense is on record but refused: interest_expense over the trailing four quarters needs the this year to date: us-gaap:InterestExpense for 2026-01-01..2026-06-30 is reported as [5800000.0, 5835000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by; interest paid is not on record: interest_paid over the trailing four quarters needs the this year to date: no row for interest_paid in 2026-01-01..2026-06-30: us-gaap:InterestPaidNet, us-gaap:InterestPaid is in the record, but not for this period
  - 세율: 21.0% — the effective rate is above statutory; held at 21%; income_tax_expense / pretax_income, held between 0 and 0.21
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: (계산 안 됨: us-gaap:DebtCurrent is reported as [108491000.0, 108500000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by)
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- 세전 타인자본비용은 대체값이며, WACC와 가치 범위는 이 대체값에 기대고 있습니다: the risk-free rate plus one point, because interest expense is on record but refused: interest_expense over the trailing four quarters needs the this year to date: us-gaap:InterestExpense for 2026-01-01..2026-06-30 is reported as [5800000.0, 5835000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by; interest paid is not on record: interest_paid over the trailing four quarters needs the this year to date: no row for interest_paid in 2026-01-01..2026-06-30: us-gaap:InterestPaidNet, us-gaap:InterestPaid is in the record, but not for this period

- **가치 범위**: 주가 자료가 없어 베타, 자기자본비용, 가중평균자본비용(WACC)이 계산되지 않았으므로 가치 범위와 시나리오별 주당 가치는 산출되지 않았습니다. 게다가 첫 단계에서 제가 세운 약세·기본·강세 시나리오가 모두 탈락해, 할인율이 있었더라도 돌릴 가정이 없었습니다.
- **주가의 위치**: 기준일 주가 자체가 계산기에 없으므로, 주가가 가치 범위의 어디에 놓이는지는 말할 수 없습니다.
- **시장이 가정한 성장률**: 역DCF가 실행되지 않아 주가에 담긴 성장률은 알 수 없습니다. 비교 기준인 회사의 삼 년 복합 매출 성장률은 1.4%로 낮은데, 회사가 올린 올해 매출 가이던스는 하단마저 직전 회계연도 매출 21.3억 달러를 웃돌며, 그 성장의 일부는 인수와 환율에서 나옵니다.
- **가장 민감한 가정**: 민감도 표가 계산되지 않아 가장 민감한 가정을 표에서 읽을 수는 없으며, 빠져 있는 것은 할인율 자체입니다. 회사의 과거 기록에서 가장 크게 흔들린 가정은 매출 성장률(-2.1%에서 33.2%까지)이고, 영업이익률은 좁은 범위에 머물렀습니다.
- **회계 조정이 바꾼 가치**: 회계 분석가가 적은 조정은 없고 가치평가도 계산되지 않았으므로, 조정이 가치를 움직인 크기는 없습니다. 다만 규모가 밝혀지지 않은 관세 환급, 스왑 이익, 얇아진 대손충당금은 보고된 이익률을 지속 가능한 수준보다 높였을 수 있어, 이익률 가정을 세울 때 따져 보아야 합니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for current_maturities_of_long_term_debt in 2025-12-31: us-gaap:LongTermDebtCurrent, us-gaap:LongTe)
- accruals_over_assets: 0.024
- net_operating_assets: 계산 안 됨 (current year: no row for short_term_investments: the companyfacts record tags none of us-gaap:ShortTermInvestments, us-g)
- piotroski_f_score: 5.000
- altman_z_score: 계산 안 됨 (current year: no row for total_liabilities: the companyfacts record tags none of us-gaap:Liabilities in any period. comp)
- ohlson_o_score: 계산 안 됨 (current year: no row for total_liabilities: the companyfacts record tags none of us-gaap:Liabilities in any period. comp)

## 계산하지 못한 항목

- revenue: revenue over the trailing four quarters needs the this year to date: us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax for 2026-01-01..2026-06-30 is reported as [1123300000.0, 1123317000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by
- net_income: net_income over the trailing four quarters needs the this year to date: us-gaap:NetIncomeLoss for 2026-01-01..2026-06-30 is reported as [100072000.0, 100100000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by
- assets: us-gaap:Assets for 2026-06-30 is reported as [2150700000.0, 2150732000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by
- free_cash_flow_to_firm: depreciation_and_amortization: depreciation_and_amortization over the trailing four quarters needs the this year to date: us-gaap:DepreciationDepletionAndAmortization for 2026-01-01..2026-06-30 is reported as [33895000.0, 33900000.0] by the filing of 2026-07-29 (0000038725-26-000055) — two values for one period is not a number to divide by
- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
