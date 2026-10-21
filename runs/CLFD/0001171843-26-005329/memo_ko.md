# CLFD — 10-Q, 2026-06-30 기간 (제출일 2026-08-06) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: 최근 네 분기 영업현금흐름은 1,578만 달러로 순이익 -722만 달러보다 크지만, 이익이 좋아서가 아니라 호황기에 쌓은 재고를 팔아 현금을 회수했기 때문입니다(올해 아홉 달 영업현금흐름 734만 달러가 같은 기간 재고 변동액 -864만 달러가 풀어 준 현금보다 작습니다). 순손실에는 매각된 Nestor 사업의 손실이 섞여 있고 현금흐름 태그도 기간마다 달라서 비율 -2.186은 그대로 해석하기 어렵습니다.
- **매출 인식**: 분기말 매출채권회수기간(DSO)은 0만 달러일로 전년 동기 0만 달러일보다 낮아, DSO가 늘었다는 MD&A 설명과 방향이 반대입니다(전년 잔액에 매각 사업의 채권이 섞였을 가능성이 있습니다). 한 대형 지역 통신사 고객이 분기 매출의 10.0%이면서 매출채권의 21.0%를 차지하고 대손충당금은 0만 달러이어서 계속 지켜봐야 합니다.
- **추정치와 충당금**: 재고충당금 비율은 38.0%로 관측된 분기 중 가장 높아 보수적으로 쌓이고 있지만, 이번 분기 이익에는 과거 충당금을 쌓았던 재고의 판매 회수, 성과급 충당금 축소, 성과주식 보상비 환입 같은 추정 변경이 들어 있습니다. 회사는 이를 중요하지 않다고 하지만 계산기에 금액이 없어 크기를 확인할 수 없고, 대손충당금은 0만 달러이며 가이던스를 낮췄는데도 영업권 손상 징후가 없다고 판단했습니다.
- **비용 이연(자본화)**: 자본화된 소프트웨어나 개발비는 기록에 없고 설비투자는 감가상각의 0.521배 수준이라 비용을 자산으로 미룬 흔적은 없습니다. 다만 회사 스스로 반복되지 않는다고 한 관세 환급이 분기 매출총이익률 31.8%에 들어 있어 정상 수준보다 높게 보입니다.
- **현금흐름 조정과 부외 항목**: 계속영업에서는 매출채권 팩토링, 공급망 금융, 구매약정, 보증이 기록에 나타나지 않습니다. 현금흐름은 재고 축소와 설비투자 감소(최근 네 분기 318만 달러, 전년 844만 달러)로 늘었으며, 반복되기 어려운 재고 축소분은 잉여현금흐름에서 빼는 조정을 했고 주식보상비 480만 달러는 현금이 나가지 않아도 실제 비용으로 이미 차감되어 있습니다.
- **내부통제·감사·공시 신호**: 공시통제는 유효하다고 결론 내렸고 감사인 교체나 임원 이탈 공시는 없습니다. 다만 실적 발표문이 분기를 잘못 표기했고, 고객 알파벳이 공시마다 바뀌어(같은 회계연도 말 매출채권 비중이 한 공시에서는 고객 B 11.0%, 다른 공시에서는 고객 C 11.0%) 고객별 추적이 어렵습니다.
- **문서 간 대조**: 8-K 실적 발표의 분기 매출 43,864,000.000과 전년 대비 성장률 13.2%는 10-Q와 일치합니다. 그러나 '강한 현금 창출'이라는 설명은 최근 네 분기 영업현금흐름 변화율 -49.4%와 올해 현금이 재고 처분에서 나왔다는 점과 맞지 않고, MD&A의 DSO 증가와 리스부채 증가 설명도 수치와 방향이 다릅니다.
- **업종 관점(반도체·하드웨어)**: 재고 진부화는 특정 고객 주문용 완제품에 대한 충당금으로 인식되고 있고 재고일수는 0만 달러일로 낮아졌습니다. 과다 구매약정이나 고객에 투자한 뒤 매출로 돌아오는 순환 거래는 발견되지 않았고, 매출채권이 유통사가 아닌 최종 고객에게 몰려 있어 채널 밀어내기 신호는 약하지만 고객 집중은 계속 관찰해야 합니다.

**이상 징후 목록** (33건, 건수 기준 없이 모두 적음)

- 계속영업 현금흐름과 전체 순손실을 섞은 현금 대비 이익 비율 — 이익 대 현금 · 숫자로 판단 불가
- 영업현금흐름 태그 변경으로 발생액 추세 비교 단절 — 이익 대 현금 · 숫자로 판단 불가
- 재고 축소가 영업현금흐름을 떠받침 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 매출채권의 재무상태표 변동과 현금흐름표 변동 방향 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 재고 잔액 감소가 현금흐름표상 감소보다 큼 — 이익 대 현금 · 숫자로 판단 불가
- 매입채무 감소, 현금흐름표 항목 미태그 — 이익 대 현금 · 숫자로 판단 불가
- 보고 이익이 현금흐름보다 덜 변동 — 이익 대 현금 · 숫자로 판단 불가
- MD&A는 DSO 증가, 수치는 감소 — 매출 인식 · 숫자가 설명과 모순
- 한 통신사 고객의 매출채권 비중이 매출 비중을 크게 웃돔 — 매출 인식 · 숫자가 설명을 뒷받침
- 기말 매출 집중이 두 해 연속 같은 설명 — 매출 인식 · 숫자가 설명을 뒷받침
- 매출채권 집중 속 대손충당금 없음 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 재고충당금 비율 최고 수준 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 과거 충당금 설정 재고 판매 회수가 매출총이익률을 끌어올림 — 추정치와 충당금 · 숫자로 판단 불가
- 보상 관련 추정 변경이 분기 이익을 높임 — 추정치와 충당금 · 숫자로 판단 불가
- 추정 변경이 중요하지 않다는 설명 — 추정치와 충당금 · 숫자로 판단 불가
- 가이던스 하향과 주문 취소에도 영업권 손상 징후 없음 판단 — 추정치와 충당금 · 숫자로 판단 불가
- 연성자산 비중이 전년보다 높음 — 비용 이연(자본화) · 숫자로 판단 불가
- 반복되지 않는 관세 환급이 매출총이익률에 포함 — 비용 이연(자본화) · 숫자로 판단 불가
- 특정 주문 탓으로 설명된 재고 진부화 손실이 매년 반복 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 전년 비교 영업현금흐름에 매각 사업과 팩토링 현금이 섞였을 가능성 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 설비투자가 감가상각보다 적고 감소 중 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 리스 갱신에도 리스부채가 전년보다 낮음 — 현금흐름 조정과 부외 항목 · 숫자가 설명과 모순
- 회전신용한도가 갱신 대신 단기 연장 반복 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 주식보상비가 영업현금흐름 대비 크고 장기적으로 증가 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 실적 발표문의 분기 명칭 오기 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 공시마다 고객 알파벳 표기가 바뀜 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 발표문은 강한 현금 창출이라 했지만 올해 현금은 재고 처분에 의존 — 문서 간 대조 · 숫자가 설명과 모순
- 취소 주문과 회수액 설명이 발표문과 10-Q에서 다름 — 문서 간 대조 · 숫자로 판단 불가
- 관세 환급 비반복 경고가 발표문에만 있음 — 문서 간 대조 · 숫자로 판단 불가
- 분기 후 하이퍼스케일 수주가 발표문에만 등장 — 문서 간 대조 · 숫자로 판단 불가
- 같은 분기에 수요가 늘었다는 설명과 둔화됐다는 설명이 공존 — 문서 간 대조 · 숫자로 판단 불가
- 특정 주문용 완제품의 진부화 — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침
- 고객 집중이 유통사에서 통신사로 이동 — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- Remove the trailing inventory release from free cash flow: 721만 달러 차감 (`terms.trailing_four_quarters.change_in_inventory`)

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: 최근 누적 기간 기준 매출총이익률은 33.0%이지만, 영업이익률은 -0.2%, 순이익률은 -4.7%로 본업에서 거의 이익을 내지 못하고 있습니다. 이번 분기는 흑자였지만 다시 생기지 않을 관세 환급과 성과급 충당금 환입의 도움을 받았으며, 과거의 높은 이익률과 비교하면 수익성이 이 회사의 가장 큰 약점입니다.
- **효율성**: 재고 보유일수 154.5일이 현금전환주기 187.8일의 대부분을 차지하고, 자산회전율은 0.528로 낮습니다. 재고는 줄고 있지만 재고 평가충당금 비율은 38.0%로 역대 최고이고, 대손충당금은 0만 달러입니다.
- **유동성**: 유동비율 12.533, 당좌비율 9.041, 현금 및 단기투자 1.0억 달러로 유동성은 매우 튼튼하며, 잉여현금흐름이 플러스여서 현금 소진 기간은 계산되지 않습니다. 다만 자사주 매입 1,348만 달러가 잉여현금흐름보다 커서 현금성 자산이 줄고 있고, 쓰지 않은 신용한도는 몇 달씩 짧게 연장되고 있습니다.
- **지급능력**: 총차입금은 0만 달러, 순차입금은 -1.0억 달러(순현금)이고 부채/자산 비율은 7.9%여서 지급능력에는 압박이 없습니다. 이자보상배율은 이자비용 자료가 없어 계산되지 않았지만, 차입금이 없으므로 판단에 영향을 주지 않습니다.
- **성장**: 이번 분기 매출은 전년 동기보다 13.2%, 직전 분기보다 27.5% 늘었지만, 최근 누적 영업이익은 -37만 달러로 적자이고 회계연도 기준 장기 연평균 매출성장률은 -17.9%입니다. 회사는 산업 수요 제약을 이유로 올해 전망을 낮췄고, 수주잔고도 줄었습니다.
- **잉여현금흐름**: 단순 잉여현금흐름 1,260만 달러, 기업잉여현금흐름 2,398만 달러, 주주잉여현금흐름 1,260만 달러, 주식보상 차감 후 781만 달러로 모두 플러스입니다. 하지만 상당 부분이 재고 축소 같은 운전자본 감소(-2,135만 달러)에서 나와 오래 지속되기 어렵고, 순이익이 음수여서 잉여현금흐름/순이익 비율은 계산되지 않습니다.
- **듀퐁 분해**: 자기자본이익률 -2.8%는 순이익률 -4.7% × 자산회전율 0.528 × 자기자본승수 1.140으로 분해되며, 부호와 크기를 결정하는 것은 순이익률입니다. 차입금이 없어 자기자본승수는 최저 수준에 가깝고, 과거 흑자에서 적자로 크게 움직인 요소도 순이익률입니다.
- **압박이 위기로 바뀌는 조건**: 지금은 재무 위기와 거리가 멀고, 압박은 수익성과 성장에 있습니다. 위기로 번지려면 재고 축소에 기댄 잉여현금흐름(1,260만 달러)이 음수로 돌아서고, 영업적자 속에 자사주 매입으로 현금성 자산(1.0억 달러)이 크게 줄며, 그 시점에 몇 달 뒤 만기가 오는 신용한도가 필요해지는 일이 함께 일어나야 합니다.

**재무 압박 징후 목록** (18건)

- 산업 수요 제약에 따른 연간 전망 하향
- 회사 자체 연간 성과 목표 달성 가능성 소멸
- 단기 연장을 반복하는 회전신용한도
- 자사주 매입이 잉여현금흐름을 넘어서며 현금성 자산 감소
- 재고 축소에 기댄 잉여현금흐름
- 수주잔고에서 제외되고 상각된 기존 고객 주문
- 분기 매출 증가 이면의 수요 둔화와 일부 고객 시장 축소
- 전망 하향에도 손상 징후 없음으로 판단한 영업권
- 과거 대비 크게 낮아진 최근 누적 영업적자
- 일회성 항목에 흔들린, 역대 저점 부근의 분기 매출총이익률
- 회사가 중요하지 않다고 한 추정 변경에 도움받은 분기 이익
- 최근 누적 순손실과 마이너스 자기자본·총자산 수익률
- 역대 최고 수준의 재고 평가충당금 비율
- 긴 현금전환주기와 낮은 자산회전율
- 매출채권: 회수 지연 언급, 특정 고객 집중, 대손충당금 없음
- 전년 같은 시점보다 낮아진 최근 누적 영업이익과 순이익
- 연초 누적 및 최근 누적 영업현금흐름 감소
- 과거 정점보다 크게 낮은 매출

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: -17.9% · 과거 5년 연평균: 10.0%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (enterprise_value: market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.7% — DGS10 on 2026-08-06; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-08-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 5.7% — fallback: the risk-free rate plus one point, because neither interest expense nor interest paid is on record: interest_expense: interest_expense over the trailing four quarters needs the prior fiscal year: no row for interest_expense in 2024-10-01..2025-09-30: us-gaap:InterestExpense, us-gaap:InterestExpenseNonoperating, us-gaap:InterestExpenseDebt, us-gaap:InterestAndDebtExpense is in the record, but not for this period
  - 세율: 21.0% — the effective rate is above statutory; held at 21%; income_tax_expense / pretax_income, held between 0 and 0.21
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: 0만 달러 — debt_current + debt_noncurrent; no record id on the cell
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- 세전 타인자본비용은 대체값이며, WACC와 가치 범위는 이 대체값에 기대고 있습니다: the risk-free rate plus one point, because neither interest expense nor interest paid is on record: interest_expense: interest_expense over the trailing four quarters needs the prior fiscal year: no row for interest_expense in 2024-10-01..2025-09-30: us-gaap:InterestExpense, us-gaap:InterestExpenseNonoperating, us-gaap:InterestExpenseDebt, us-gaap:InterestAndDebtExpense is in the record, but not for this period

- **가치 범위**: 주가 자료와 베타가 없어 자기자본비용과 WACC가 계산되지 않았고, 그래서 세 시나리오의 기업가치, 주주가치, 주당가치는 하나도 나오지 않았습니다. 계산된 것은 무위험이자율 4.7%, 주식위험프리미엄 4.3%, 순현금 상태를 뜻하는 순차입금 -1.0억 달러 같은 구성요소뿐입니다.
- **주가의 위치**: 주가 자료가 주어지지 않아 주가가 가치 범위의 어디쯤에 있는지 읽을 수 없습니다. 주가가 시나리오보다 높은지 낮은지에 대해서는 아무 판단도 하지 않습니다.
- **시장이 가정한 성장률**: 역DCF가 실행되지 않아 주가에 담긴 성장률은 알 수 없습니다. 비교 기준이 되었을 회사 기록은 세 회계연도 연평균 매출성장률 -17.9%, 다섯 회계연도 연평균 10.0%이고, 회사는 낮춘 가이던스에서 올해 매출을 최근 네 분기 매출 1.5억 달러 근처로 제시했습니다.
- **가장 민감한 가정**: 민감도 표가 계산되지 않아 어떤 가정이 가치를 가장 크게 움직이는지는 측정되지 않았습니다. 다만 세 시나리오가 회사 기록에 비해 가장 넓게 벌어진 가정은 열 번째 해 영업이익률과 첫해 매출성장률이며, 모든 시나리오가 최근 영업이익률 -0.2%보다 높은 이익률 회복을 전제합니다.
- **회계 조정이 바꾼 가치**: 가치 평가가 실행되지 않아 회계 조정이 가치를 얼마나 바꿨는지는 계산되지 않았습니다. 회계 분석가의 유일한 조정인 재고 축소분 제거는 품질조정 잉여현금흐름을 7,806,000.000에서 593,000.000으로 낮췄고, 제 시나리오도 이 재고 축소가 앞으로 반복된다고 가정하지 않습니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for long_term_debt in 2025-09-30: us-gaap:LongTermDebtNoncurrent, us-gaap:LongTermDebtAndCapitalLea)
- accruals_over_assets: 계산 안 됨 (current year: no row for debt_in_current_liabilities in 2025-09-30: us-gaap:DebtCurrent, us-gaap:LongTermDebtCurrent, us)
- net_operating_assets: 계산 안 됨 (current year: no row for debt_in_current_liabilities in 2025-09-30: us-gaap:DebtCurrent, us-gaap:LongTermDebtCurrent, us)
- piotroski_f_score: 계산 안 됨 (current year: no row for long_term_debt in 2025-09-30: us-gaap:LongTermDebtNoncurrent, us-gaap:LongTermDebtAndCapitalLea)
- altman_z_score: 계산 안 됨 (current year: no row for interest_expense in 2024-10-01..2025-09-30: us-gaap:InterestExpense, us-gaap:InterestExpenseNon)
- ohlson_o_score: -7.107

## 계산하지 못한 항목

- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
