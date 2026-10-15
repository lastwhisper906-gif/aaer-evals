# SMCI — 10-K, 2026-06-30 기간 (제출일 2026-08-31) 분석 메모

세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. 숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.

## 1. 회계

### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가

- **이익 대 현금**: 순이익은 22.3억 달러이었지만 영업현금흐름은 -68.1억 달러여서, 영업현금흐름을 순이익으로 나눈 값 -3.053은 회사 자체 기록 중 가장 나쁩니다. 원인은 재고 증가 82.2억 달러와 매출채권 증가 39.2억 달러 같은 운전자본 확대이고, 현금흐름표의 재고 변동과 재무상태표 재고 변동 사이에는 설명되지 않은 차이 -6.6억 달러가 있습니다.
- **매출 인식**: 매출채권을 매출로 나눈 값이 0.100에서 0.157로 올라 채권이 매출보다 빨리 늘었고, 회사는 일부 고객에게 결제기간 연장과 금융 약정을 제공하면서도 그 규모를 밝히지 않습니다. 고객 선수금으로 계약부채가 늘어난 점은 매출을 뒷받침하지만, 넷째 분기 순이익 1,178,217,000.000이 연간 이익의 큰 몫을 차지하는데도 10-K에는 그 설명이 없습니다.
- **추정치와 충당금**: 대손충당금 비율 0.000은 이력상 거의 최저이고 보증충당금 비율 0.001은 최저이며, 재고 평가손실은 1.9억 달러로 줄었는데 재고일수는 135.1일로 이력상 가장 깁니다. 추정치들이 이익을 높이는 쪽으로 기울어 있고, 세율 19.9%도 아직 승인되지 않은 말레이시아 세금 감면을 전제로 합니다.
- **비용 이연(자본화)**: 개발비 자본화는 태그되어 있지 않아 검증할 수 없지만, 유형자산 6.3억 달러와 감가상각비 5,300만 달러가 작아 비용을 자산으로 미룬 흔적은 보이지 않습니다. 소프트자산 비중 0.728의 상승은 재고와 채권 때문이며, 공급사 지원금이 영업비용 일부를 메우고 비GAAP 조정은 실제 비용인 주식보상 4.1억 달러를 더해 줍니다.
- **현금흐름 조정과 부외 항목**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **내부통제·감사·공시 신호**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **문서 간 대조**: 8-K 잠정 실적은 10-K와 비교한 모든 항목에서 일치했고, 넷째 분기 영업현금흐름 746,961,000.000도 맞습니다. 방향이 있는 설명은 대부분 숫자로 확인되지만, 마케팅 지원금이 판매비를 줄였다는 설명은 판매비가 늘어 숫자와 모순되고, 계산기는 총부채를 0만 달러로 읽어 실제 은행 차입과 전환사채를 놓치고 있습니다.
- **업종 관점(반도체·하드웨어)**: 재고 129.0억 달러, GPU 완제품, 줄어든 평가손실은 진부화 위험을 키우고, 구매약정 342.0억 달러는 올해 매출원가 348.4억 달러에 육박합니다. 단일 고객이 연간 매출의 28.1%를 차지하고 고객에게 투자하거나 자금을 대는 거래도 있지만, 규모가 공개되지 않아 벤더 금융 여부는 검증할 수 없습니다.

**이상 징후 목록** (43건, 건수 기준 없이 모두 적음)

- 순이익 증가에도 영업현금흐름 대규모 유출 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 재고 증가가 순이익의 몇 배를 흡수 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 매출채권 증가가 순이익을 초과하고 매입채무로 상쇄되지 않음 — 이익 대 현금 · 숫자가 설명을 뒷받침
- 현금흐름표 재고 변동과 재무상태표 재고 변동 불일치 — 이익 대 현금 · 숫자로 판단 불가
- 이익이 현금흐름보다 훨씬 평탄함 — 이익 대 현금 · 숫자로 판단 불가
- 매출채권이 매출보다 빠르게 증가 — 매출 인식 · 숫자가 설명을 뒷받침
- 결제기간 연장과 유의적 금융요소 — 매출 인식 · 숫자로 판단 불가
- 통제 이전 전 매출채권과 이연수익 동시 인식 — 매출 인식 · 숫자로 판단 불가
- 계약부채 비율 회사 이력상 최고 — 매출 인식 · 숫자가 설명을 뒷받침
- 넷째 분기 이익 집중, 10-K 설명 부재 — 매출 인식 · 숫자로 판단 불가
- 사상 최대 수주잔고 주장, 공시로는 측정 불가 — 매출 인식 · 숫자로 판단 불가
- 대손충당금이 얇고 연말에 감소 — 추정치와 충당금 · 숫자로 판단 불가
- 보증충당금 비율 회사 이력상 최저 — 추정치와 충당금 · 숫자로 판단 불가
- 재고 회전이 느려지는데 평가손실은 감소 — 추정치와 충당금 · 숫자가 설명을 뒷받침
- 구매약정 손실충당 금액 공시 중단 — 추정치와 충당금 · 숫자로 판단 불가
- 승인 전 말레이시아 세금 감면을 세율에 반영 — 추정치와 충당금 · 숫자로 판단 불가
- 미인식 세무혜택 계속 증가, OBBBA 영향 미계량 — 추정치와 충당금 · 숫자로 판단 불가
- 기준 공시 없이 관세 환급 청구 채권 인식 — 추정치와 충당금 · 숫자로 판단 불가
- 운전자본으로 소프트자산 비중 상승 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 선급 재고와 설명 없는 '타인 보유 자산' 신규 항목 — 비용 이연(자본화) · 숫자로 판단 불가
- 공급사 지원금이 영업비용 일부를 부담 — 비용 이연(자본화) · 숫자로 판단 불가
- 주식보상 증가로 비GAAP 격차 확대 — 비용 이연(자본화) · 숫자가 설명을 뒷받침
- 부외 구매약정 급증 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 현금흐름 분류가 공개되지 않은 고객 금융 약정 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 운용리스 부채 증가, 전대 수익은 영업외 처리 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 현금과 매출채권이 대주에 담보로 묶임 — 현금흐름 조정과 부외 항목 · 숫자로 판단 불가
- 차입과 주식 발행으로 영업현금 적자 보전 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 실질 비용인 주식보상 증가 — 현금흐름 조정과 부외 항목 · 숫자가 설명을 뒷받침
- 중요한 취약점과 내부통제 부적정 의견 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 재고 평가와 매출 기간귀속에 대한 핵심감사사항 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 결산 완료 전 잠정 발표, 이후 10-K와 일치 — 내부통제·감사·공시 신호 · 숫자가 설명을 뒷받침
- 특수관계자 재판매 약정 시점이 공시 간 변경 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 특수관계자 지분 공시 문장 무설명 삭제 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 특수관계자 신용·재판매·토지사용 약정 신설 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 정부 조사가 컴플라이언스와 내부통제까지 확대 — 내부통제·감사·공시 신호 · 숫자로 판단 불가
- 마케팅 지원금이 판매비를 줄였다는 설명과 달리 판매비 증가 — 문서 간 대조 · 숫자가 설명과 모순
- 고객 다변화 주장과 최대 고객 비중 상승 — 문서 간 대조 · 숫자로 판단 불가
- 광고비 설명이 주석과 MD&A에서 상이 — 문서 간 대조 · 숫자로 판단 불가
- MD&A의 기타수익 설명에서 전대 수익 누락 — 문서 간 대조 · 숫자로 판단 불가
- GPU 비중이 큰 대규모 저회전 재고 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가
- 현재 사업 규모를 넘는 구매약정 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가
- 고객 집중도가 높고 연중 변동 — 업종 관점(반도체·하드웨어) · 숫자가 설명을 뒷받침
- 회사 자금이 고객 측 거래에 투입 — 업종 관점(반도체·하드웨어) · 숫자로 판단 불가

**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)

- 없음

_한계: 이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 증거는 볼 수 없습니다._

## 2. 재무

### 2.1 재무 분석 — 이 회사는 얼마나 건강한가

- **수익성**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **효율성**: 연말 잔액 기준 재고일수는 135.1일로 기록상 가장 길고, 매출채권 회수일수도 36.6일에서 57.2일로 늘었습니다. 매입채무일수는 18.5일에 불과해 현금회전주기가 112.5일에 이릅니다.
- **유동성**: 유동비율 3.872는 넉넉해 보이지만 연간 영업현금흐름이 -68.1억 달러여서, 이 속도라면 현금과 단기투자는 13.0개월분입니다. 현금이 늘어난 것은 차입과 우선주·보통주 발행 덕분이며, 취소 불가능한 구매약정 342.0억 달러가 유동자산 전체보다 큽니다.
- **지급능력**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)
- **성장**: 매출은 77.8%, 순이익은 112.7% 늘어 손익 성장은 건강합니다. 그러나 영업현금흐름은 16.6억 달러에서 -68.1억 달러로 뒤집혔고, 회계연도 마지막 분기에만 746,961,000.000의 유입으로 돌아섰습니다.
- **잉여현금흐름**: 잉여현금흐름은 단순 -69.7억 달러, 기업 기준 -90.6억 달러, 주주 기준 -30.2억 달러, 질 조정 -73.8억 달러로 빠짐없이 계산되었고 모두 마이너스입니다. 설비투자는 1.6억 달러에 그쳐, 현금 유출의 원인은 재고와 매출채권에 묶인 운전자본입니다.
- **듀퐁 분해**: 자기자본이익률 21.5%는 얇은 순이익률 5.7%보다는 자산회전율 1.777과 자기자본승수 2.116이 떠받치고 있습니다. 전년도 분해값이 계산기에 없어 각 요소의 변화 폭은 잴 수 없고, 순이익이 매출보다 빨리 늘어 순이익률이 높아졌다는 방향만 확인됩니다.
- **압박이 위기로 바뀌는 조건**: (검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)

**재무 압박 징후 목록** (12건)

- 영업현금 유출과 짧은 현금 소진 기간
- 현금과 유동자산 전체를 넘어서는 취소 불가능한 구매약정
- 영업이 아닌 차입과 주식 발행으로 채운 현금
- 대주에게 통제되거나 담보로 잡힌 현금과 매출채권
- 부품 공급 제약과 리드타임을 앞선 선매입
- 여전히 유효하지 않은 재무보고 내부통제
- 실효세율 상승과 승인 전에 반영된 세제 혜택
- 기록상 가장 긴 재고일수
- 전년보다 길어진 매출채권 회수일수
- 재고 회전보다 훨씬 빠른 공급사 대금 지급
- 약정 검증 면제, 상환 연장, 강화되는 레버리지 약정
- 이익이 늘어나는 동안 뒤집힌 영업현금흐름

_한계: 이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다._

### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가

Python이 가치를 계산하지 못했습니다. 이유: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched

- 시장이 가정한 10년 매출 성장률: (no reverse DCF: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 과거 3년 연평균: 76.3% · 과거 5년 연평균: 61.5%

- 잉여현금흐름 수익률 (기준일 주가 기준): 기업 잉여현금흐름 / 기업가치 (enterprise_value: market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched) · 주주 잉여현금흐름 / 시가총액 (market_value_of_equity: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- WACC 구성 (각 입력값과 그 출처):
  - 무위험이자율: 4.8% — DGS10 on 2026-08-31; src/cost_of_capital/manifest.json, risk_free_rate
  - 주식위험프리미엄: 4.3% — the month starting 2026-08-01; src/cost_of_capital/manifest.json, equity_risk_premium
  - 베타: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 자기자본비용: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 세전 타인자본비용: 0.0% — no debt on the balance sheet, so it carries no weight
  - 세율: 19.9% — the effective rate, inside the bounds; income_tax_expense / pretax_income, held between 0 and 0.21
  - 시가총액: (계산 안 됨: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 총차입금: 0만 달러 — debt_current + debt_noncurrent; no record id on the cell
  - 자기자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - 타인자본 비중: (계산 안 됨: no weights: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)
  - WACC: (계산 안 됨: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched)

- **가치 범위**: 베타와 기준일 주가가 없어 할인율(WACC)을 계산하지 못했고, 그래서 가치 범위와 시나리오별 기업가치·주당가치도 나오지 않았습니다. 읽을 수 있는 것은 가정과 과거 기록의 비교뿐이며, 세 시나리오 모두 첫해 매출 성장률을 지난해 77.8%와 삼 년 복리 성장률 76.3%보다 낮게 잡았습니다.
- **주가의 위치**: 계산기에 기준일 주가가 없어 주가가 가치 범위의 어디쯤에 있는지 읽을 수 없습니다. 기업 기준 잉여현금흐름도 -90.6억 달러로 마이너스여서, 현금흐름 수익률로 교차 확인할 수도 없습니다.
- **시장이 가정한 성장률**: 역DCF를 계산하지 못해 주가가 전제하는 성장률은 알 수 없습니다. 비교 기준이 될 회사 기록은 지난해 77.8%, 오 년 복리 61.5%이고, 회사는 다음 분기 매출을 방금 끝난 분기의 11,119,777,000.000보다 훨씬 높게 제시했습니다.
- **가장 민감한 가정**: 민감도 표를 계산하지 못해 가치가 가장 민감하게 반응하는 두 가정을 표에서 읽을 수는 없습니다. 시나리오끼리 가장 크게 갈리는 가정은 첫해 매출 성장률과 첫해 재투자율이며, 세 시나리오 모두 첫해 재투자가 세후 영업이익보다 커서 기업 잉여현금흐름이 마이너스로 출발합니다.
- **회계 조정이 바꾼 가치**: 회계 분석에서 적용한 조정은 없고, 가치평가 자체가 돌지 않았으므로 조정이 가치를 움직이지도 않았습니다. 다만 계산기는 총차입금을 0만 달러로 읽어 회사가 밝힌 은행 차입금과 전환사채를 빠뜨리고 있어, 나중에 가치평가를 돌릴 때 이 차입금을 빼지 않으면 주당가치가 부풀려집니다.

_한계: 이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다._

## 참고: 공식 기준선 (위 세 분석과 합치지 않음)

- beneish_m_score: 계산 안 됨 (current year: no row for selling_general_and_administrative: the companyfacts record tags none of us-gaap:SellingGeneral)
- accruals_over_assets: 계산 안 됨 (current year: no row for debt_in_current_liabilities in 2026-06-30: us-gaap:DebtCurrent, us-gaap:LongTermDebtCurrent, us)
- net_operating_assets: 계산 안 됨 (current year: no row for debt_in_current_liabilities in 2026-06-30: us-gaap:DebtCurrent, us-gaap:LongTermDebtCurrent, us)
- piotroski_f_score: 계산 안 됨 (current year: no row for long_term_debt in 2026-06-30: us-gaap:LongTermDebtNoncurrent, us-gaap:LongTermDebtAndCapitalLea)
- altman_z_score: 계산 안 됨 (Altman's fourth ratio is the market value of equity over the book value of total debt, and no market value of equity was)
- ohlson_o_score: -5.875

## 계산하지 못한 항목

- wacc: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
- valuation: WACC is not computed: the cost of equity needs a beta and a price: no price series was given: the forward track's price source is Tiingo, and without its token no series is fetched
