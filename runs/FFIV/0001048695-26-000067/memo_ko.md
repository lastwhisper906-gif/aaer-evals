# FFIV — 10-Q, 2026-06-30 기간 (제출일 2026-08-06) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: 최근 네 분기 누적 기준 영업현금흐름은 순이익의 1.444배이고 발생액 비율은 -5.0%로 음수여서, 이익이 현금으로 충분히 뒷받침되며 회사 자신의 과거 범위 안에 있습니다. 다만 평활도 지표 0.337은 이익이 현금보다 훨씬 덜 출렁인다는 뜻이고, 매입채무 증가(6,745만 달러)가 현금흐름을 받쳐 준 점은 지켜볼 부분입니다.
- **매출 인식**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **추정치와 충당금**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **비용 이연(자본화)**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **현금흐름 조정과 부외 항목**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **내부통제·감사·공시 신호**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **문서 간 대조**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **업종 관점(반도체·하드웨어)**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)

**이상 징후 목록** (7건, 건수 기준 없이 모두 적음)

- 현금보다 매끄러운 이익 — 이익 대 현금 · 숫자로 판단 불가
- 회계연도 첫 분기 발생액의 양수 전환 — 이익 대 현금 · 숫자로 판단 불가
- '유지 목적'이라지만 과거 최고를 넘은 설비투자 — 비용 이연(자본화) · 숫자로 판단 불가
- 부품 구매약정 소진과 재고 증가 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 구성 기간과 맞지 않는 유통사 누적 매출 비중 공시값 — 내부통제·감사·공시 신호 · 숫자가 설명과 모순
- 이미 소진된 구매약정을 주요 약정으로 기재한 MD&A — 문서 간 대조 · 숫자가 설명과 모순
- 매출채권 고객 집중도 확대 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- 없음

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: 최근 네 분기 매출총이익률은 81.9%로 높고, 이번 분기 값 82.2%는 기록된 여섯 분기 중 가장 높습니다. 다만 이번 분기 영업이익 증가율 8.6%가 매출 증가율 10.9%보다 낮아 영업이익률이 전년 같은 분기보다 조금 내려갔고, 자본 항목이 태그되지 않아 자기자본이익률(ROE)과 투하자본이익률(ROIC)은 계산되지 않았습니다.
- **효율성**: 이번 분기 재고일수는 75.2일로 기록된 여섯 분기 중 가장 길고, 늘어난 재고는 주로 원자재입니다. 최근 네 분기 평균 기준 현금전환주기는 40.1일이며, 매입채무 증가가 재고 증가의 일부를 상쇄하고 있습니다.
- **유동성**: 유동비율 1.665, 당좌비율 1.149로 유동성은 넉넉하고, 현금 16.1억 달러는 일 년 전 14.3억 달러보다 많습니다. 잉여현금흐름이 플러스라서 현금 소진 기간은 계산할 필요가 없지만, 이번 분기 영업현금흐름은 직전 분기 대비 -13.6% 변했습니다.
- **지급능력**: 공시 기록에 차입금 항목이 없어 총차입금은 0만 달러, 순부채는 -16.1억 달러로 순현금 상태입니다. 이자비용이 태그되지 않아 이자보상배율은 계산되지 않았지만, 기록상 갚아야 할 차입금이 없으므로 상환 부담도 보이지 않습니다.
- **성장**: 이번 분기 매출은 전년 동기 대비 10.9%, 최근 네 분기 기준 9.4% 늘어 삼 년 연평균 성장률 4.6%보다 빠르고, 회사는 연간 전망을 올렸습니다. 다만 성장은 하드웨어(시스템) 매출에 기대고 아시아태평양 매출은 줄었으며, 최근 네 분기 영업현금흐름 증가율 6.2%는 매출 증가율보다 낮습니다.
- **잉여현금흐름**: 단순 잉여현금흐름은 9.7억 달러이고, 차입이 없어 주주 잉여현금흐름 9.7억 달러도 같으며, 기업 잉여현금흐름은 6.5억 달러, 주식보상과 인수 지출을 뺀 품질조정 값은 5.2억 달러로 네 가지 모두 계산되었습니다. 자사주 매입 6.3억 달러는 품질조정 값보다 크지만 단순 잉여현금흐름보다는 작고, 현금은 오히려 늘었습니다.
- **듀퐁 분해**: 자본 항목이 없어 자기자본승수와 ROE는 계산되지 않았고, 남은 두 요소인 순이익률 22.0%와 자산회전율 0.511을 곱한 값이 총자산이익률 11.2%입니다. 수익률은 높은 이익률이 이끌고 있으며, 이전 기간의 듀퐁 값이 없어 변화는 직접 확인할 수 없습니다.
- **압박이 위기로 바뀌는 조건**: 위기가 되려면 영업현금흐름이 설비투자보다 작아져 잉여현금흐름 9.7억 달러가 마이너스로 돌아서고, 차입금 0만 달러에서 새 차입이 생기며, 유동자산 29.5억 달러가 유동부채 17.7억 달러보다 작아지는 일이 함께 일어나야 합니다. 지금 공시 수치에는 그런 조짐이 없고, 지켜볼 점은 재고 증가, 사이버 사고 비용과 소송, 그리고 자사주 매입 규모입니다.

**재무 압박 징후 목록** (12건)

- 영업비용 증가가 매출 증가를 앞질러 영업이익률이 소폭 하락
- 분기 순이익 증가가 낮아진 세율과 보험금 수령에 일부 기댐
- 재고일수가 기록된 분기 중 최고, 원자재 중심으로 재고 증가
- 전년 동기 대비 매출채권이 분기 매출보다 빠르게 늘고 대손충당금 비율은 낮아짐
- 운전자본과 설비투자가 더 많은 현금을 흡수하고 분기 영업현금흐름이 직전 분기보다 감소
- 최근 네 분기 영업이익과 영업현금흐름 증가율이 매출 증가율에 못 미침
- 아시아태평양 매출이 전년 동기보다 감소
- 매출 성장이 하드웨어(시스템)에 기대고 소프트웨어·서비스 성장은 더딤
- 분기 매출 대비 유동 이연수익 비율이 기록된 분기 중 최저
- 한 글로벌 유통사의 누적 매출 비중 상승
- 사이버 사고 비용이 계속되고 관련 소송은 미해결
- 경영진 논의에서 부품 가격 상승과 공급망 제약을 매출총이익률 위험으로 명시

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: 4.6% · 과거 5년 연평균: 5.6%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (enterprise_value: market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.7% — DGS10 on 2026-08-06; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-08-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 0.0% — no debt on the balance sheet, so it carries no weight
  - 세율: 14.9% — the effective rate, inside the bounds; income_tax_expense / pretax_income, held between 0 and 0.21
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: 0만 달러 — debt_current + debt_noncurrent; no record id on the cell
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- **가치 범위**: 주가 자료와 베타가 없어 가중평균자본비용(WACC)이 계산되지 않았고, 따라서 주당 가치 범위와 시나리오별 기업가치·주주가치도 계산되지 않았습니다. 기록에 남아 있는 입력값은 무위험이자율 4.7%, 주식위험프리미엄 4.3%, 총차입금 0만 달러 등이며, 빠진 값을 추정해 채우지 않았습니다.
- **주가의 위치**: 기준일 주가가 주어지지 않아 주가가 가치 범위의 어디쯤에 있는지 읽을 수 없습니다. 같은 주가가 필요한 잉여현금흐름 수익률 점검도 같은 이유로 계산되지 않았습니다.
- **시장이 가정한 성장률**: 역DCF가 계산되지 않아 현재 주가가 어떤 매출 성장률을 가정하는지는 알 수 없습니다. 비교 기준인 회사 기록은 삼 년 연평균 성장률 4.6%, 최근 네 분기 성장률 9.4%이며, 회사는 올해 매출 성장 전망을 높였고 기본 시나리오의 첫해 성장률은 그 전망보다 낮게 잡았습니다.
- **가장 민감한 가정**: 민감도 표가 계산되지 않아 어떤 가정이 가치를 가장 크게 움직이는지는 읽을 수 없습니다. 세 시나리오가 회사 기록을 서로 다르게 읽는 두 가정은 십 년 차 영업이익률(과거 최고 24.8%)과 첫해 매출 성장률(최근 네 분기 9.4%)입니다.
- **회계 조정이 바꾼 가치**: 회계 분석에서 조정 항목이 하나도 없었고, 품질조정 잉여현금흐름 5.2억 달러에도 주식보상과 인수 지출 외의 추가 조정은 적용되지 않았습니다. 가치평가 자체가 계산되지 않아 조정이 가치를 얼마나 바꿨는지에 대한 수치도 없습니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for selling_general_and_administrative: the companyfacts record tags none of us-gaap:SellingGeneral)
- accruals_over_assets: 계산 안 됨 (current year: no row for debt_in_current_liabilities in 2025-09-30: us-gaap:DebtCurrent, us-gaap:LongTermDebtCurrent, us)
- net_operating_assets: 계산 안 됨 (current year: no row for debt_in_current_liabilities in 2025-09-30: us-gaap:DebtCurrent, us-gaap:LongTermDebtCurrent, us)
- piotroski_f_score: 계산 안 됨 (current year: no row for long_term_debt in 2025-09-30: us-gaap:LongTermDebtNoncurrent, us-gaap:LongTermDebtAndCapitalLea)
- altman_z_score: 계산 안 됨 (current year: no row for interest_expense: the companyfacts record tags none of us-gaap:InterestExpense, us-gaap:Interes)
- ohlson_o_score: 계산 안 됨 (current year: no row for total_liabilities in 2025-09-30: us-gaap:Liabilities is in the record, but not for this period)

## 계산하지 못한 항목

- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
