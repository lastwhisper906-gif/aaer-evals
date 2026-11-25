# FTNT — 10-Q, 2026-06-30 기간 (제출일 2026-07-30) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **매출 인식**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **추정치와 충당금**: 재고 평가충당금 비율이 0.288로 여섯 분기 중 최저이며, 충당금 잔액은 1.5억 달러에서 1.2억 달러로 줄었는데 재고 평가손실은 0만 달러로 태그되어 있고 회사는 그 이유를 밝히지 않았습니다. 세율은 19.2%로 하락 요인이 없고 영업권 손상도 없습니다.
- **비용 이연(자본화)**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **현금흐름 조정과 부외 항목**: 매출채권 매각이나 공급망 금융은 기록에 없고 영업현금흐름 증가는 고객 선수금에서 나옵니다. 다만 실적 발표의 조정 잉여현금흐름은 부동산 매입을 다시 더하고, 비취소 구매약정은 연말 대비 약 두 배로 늘었으나 계산기에 해당 필드가 없으며, 주식보상을 차감한 품질조정 잉여현금흐름은 28.2억 달러로 단순 잉여현금흐름 31.2억 달러보다 작습니다.
- **내부통제·감사·공시 신호**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **문서 간 대조**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **업종 관점(반도체·하드웨어)**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)

**이상 징후 목록** (22건, 건수 기준 없이 모두 적음)

- 영업현금흐름 대 순이익 비율이 최근 두 회계연도보다 높음 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 재고 현금흐름 항목과 재무상태표 변동의 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 분기 매출 대비 계약부채 비율이 여섯 분기 중 최저 — 매출 인식 · 숫자가 설명을 뒷받침
- 첫째 분기 매출채권 회전일수 고점이 둘째 분기에 반전 — 매출 인식 · 숫자로 판단 불가
- 재고 평가충당금 비율이 여섯 분기 중 최저이나 사유 미기재 — 추정치와 충당금 · 숫자로 판단 불가
- 구매약정이 두 배로 늘었는데 초과약정 부채는 감소 — 추정치와 충당금 · 숫자로 판단 불가
- 대손 충당금이 분기말에 태그되지 않은 채 대손비용은 증가 — 추정치와 충당금 · 숫자로 판단 불가
- 하드웨어 판매사임에도 보증충당부채가 어느 기간에도 태그되지 않음 — 추정치와 충당금 · 숫자로 판단 불가
- 이연계약원가 자본화가 상각을 상회 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 주식보상비용 가산 항목 증가 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 반복되는 이익이 비GAAP 실적에서 제외됨 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 실적 발표의 조정 잉여현금흐름이 부동산 매입을 가산 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 연차보고서와 분기보고서의 자본적지출 태그가 다름 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 구매약정이 두 배로 늘었으나 기록에 태그된 사실 없음 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 법인세 납부액은 줄고 법인세비용은 증가 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 자사주 매입이 순이익을 초과하고 자본이 감소 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 최고재무책임자와 최고운영책임자가 발표 전 사전 매매계획 채택 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 후속사건 주석 삭제, 잔여 매입한도는 오월 초 이후 변동 없음 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 유통사 C의 매출채권 집중도 행이 누락 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 인텔 협업은 실적 발표에만 등장 — 문서 간 대조 · 숫자로 판단 불가
- 구매약정이 보유 재고를 크게 초과 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가
- 유통사 A의 매출채권 비중이 연말 대비 하락 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- 없음

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: 최근 네 분기 기준 매출총이익률 80.2%, 영업이익률 32.4%, 순이익률 28.2%로, 영업이익률은 회사의 공시 역사상 가장 높고 삼년 평균 28.1%를 웃돈다. 다만 분기 매출총이익률 80.2%는 채워진 여섯 분기 중 최저이며, 투하자본이익률은 현금이 부채와 자본의 합을 넘어 분모가 음수가 되므로 의미 있는 수치가 아니다.
- **효율성**: 매출채권회수기간 0만 달러일, 재고일수 0만 달러일, 매입채무지급기간 0만 달러일로 현금전환주기는 0만 달러일이며 재고가 주기의 대부분을 차지한다. 분기 매출채권회수기간은 직전 분기 최고치에서 개선됐고, 분기 재고일수는 여섯 분기 중 두 번째로 낮지만 전년 연간 수치는 다섯 해 중 두 번째로 높았다.
- **유동성**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **지급능력**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **성장**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **잉여현금흐름**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **듀퐁 분해**: 자기자본이익률 117.4%는 순이익률 28.2%, 자산회전율 0만 달러, 자본승수 0만 달러의 곱이며 자본승수가 이를 이끈다. 자본승수는 차입이 아니라 이연수익으로 자산을 조달하고 자사주 매입으로 자본이 줄어든 결과로 지난 일 년 사이 더 커졌고, 총자산이익률 19.7%가 영업 수익성을 더 잘 보여준다.
- **압박이 위기로 바뀌는 조건**: 부실로 가려면 이자보상배율 0만 달러배가 무너질 만큼 영업이익이 급감하고, 양수인 단순 잉여현금흐름 31.2억 달러가 음수로 돌아서며, 그 와중에도 자사주 매입이 최근 네 분기 속도 28.6억 달러로 계속돼 현금 29.3억 달러를 소진해야 하는데, 일 년 내 만기 부채는 0만 달러이다. 압력 지점은 부품 원가와 하드웨어 비중 확대에 따른 매출총이익률 하락, 급증한 취소 불가 재고 구매약정이 수요 둔화 시 과잉재고가 될 위험, 이연수익 유입의 반전, 그리고 얇은 자본 15.5억 달러에 비해 소송·세무 우발채무가 크게 보일 수 있다는 점이다.

**재무 압박 징후 목록** (10건)

- 다음 분기 가이던스가 직전 분기 실적을 하회
- 현금만 반영한 당좌비율이 일 미만
- 자사주 매입이 순이익을 넘어 현금과 자본을 축소
- 미계상 우발채무: 증권 집단소송, 이전가격 세무조사, 면책 청구
- 데이터센터·클라우드 용량 확대로 서비스 매출총이익률 소폭 하락 전망
- 외환손실 증가와 기능통화 문장 삭제
- 매출총이익률은 여섯 분기 중 최저, 영업이익률은 확대
- 전년 재고일수 상승, 재고는 증가하는데 평가충당금 비율은 하락
- 얇은 자본 완충: 부채비율 높고 자본승수 크나, 부채 대부분은 이연수익
- 성장이 하드웨어·가격 인상 주도, 분기 매출 대비 이연수익 비율은 여섯 분기 최저

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: 15.5% · 과거 5년 연평균: 21.3%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (enterprise_value: market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.7% — DGS10 on 2026-07-30; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-07-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 2.4% — interest_expense / average debt; interest_expense prior_fiscal_year + this_year_to_date - prior_year_to_date
  - 세율: 19.2% — the effective rate, inside the bounds; income_tax_expense / pretax_income, held between 0 and 0.21
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: 5.0억 달러 — debt_current + debt_noncurrent; 0001262039-26-000021:facts:LongTermDebtCurrent:2026-06-30, 0001262039-26-000021:facts:LongTermDebtNoncurrent:2026-06-30
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- **가치 범위**: 파이썬이 가치 범위를 계산하지 못했습니다. 계산기에는 무위험이자율 4.7%, 주식위험프리미엄 4.3%, 세전 타인자본비용 2.4%는 있지만 가격 시계열이 없어 베타와 자기자본비용, 가중평균자본비용이 비어 있고, 그래서 세 시나리오 어느 것도 기업가치와 주당가치가 산출되지 않았습니다.
- **주가의 위치**: 기준일 가격 자체가 계산기에 없으므로 가격이 범위의 어디에 놓이는지는 읽을 수 없습니다. 읽을 수 있는 것은 가정의 위치뿐으로, 기본 시나리오의 첫해 매출 성장률은 최근 네 분기 성장률 18.8%보다 낮고 삼년 복합성장률 15.5%보다 약간 높게 두었으며, 순부채 -24.4억 달러와 발행주식수 7.3억 달러는 기록에 있으나 이어 붙일 기업가치가 없습니다.
- **시장이 가정한 성장률**: 역산 DCF가 돌지 않아 시장이 가격에 반영한 성장률은 없습니다. 비교 기준이 되는 회사의 기록은 삼년 복합 15.5%, 오년 복합 21.3%, 분기 전년 대비 25.6%이며, 회사는 연간 매출 가이던스를 올렸지만 그 가이던스는 이번 분기 성장률보다 낮아 하반기 둔화를 담고 있습니다.
- **가장 민감한 가정**: 민감도 격자가 계산되지 않아 순위를 매길 수 없습니다. 세 시나리오 사이에서 가장 넓게 벌어진 가정은 첫해 매출 성장률과 십년차 영업이익률이며, 할인율은 아예 비어 있어 격자가 돌았더라도 그 축이 없었을 것입니다.
- **회계 조정이 바꾼 가치**: 회계 분석가는 조정을 하나도 쓰지 않았고, 품질조정 잉여현금흐름 28.2억 달러와 단순 잉여현금흐름 31.2억 달러의 차이는 주식보상 3.0억 달러뿐입니다. 가치평가가 계산되지 않았으므로 조정이 가치를 얼마나 움직였는지도 산출된 것이 없습니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for selling_general_and_administrative: the companyfacts record tags none of us-gaap:SellingGeneral)
- accruals_over_assets: 계산 안 됨 (current year: no row for income_taxes_payable in 2025-12-31: us-gaap:AccruedIncomeTaxesCurrent, us-gaap:TaxesPayableCurr)
- net_operating_assets: 계산 안 됨 (current year: no row for short_term_investments in 2025-12-31: us-gaap:ShortTermInvestments, us-gaap:MarketableSecuritie)
- piotroski_f_score: 4.000
- altman_z_score: 계산 안 됨 (Altman's fourth ratio is the market value of equity over the book value of total debt, and no market value of equity was)
- ohlson_o_score: -3.748

## 계산하지 못한 항목

- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
