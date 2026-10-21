# What frontier accounting and finance analysts look at, against what this pipeline computes

Read on the night of 2026-10-21 for the owner's instruction "어떤분석을 해야하는지
프론티어 회계, 재무전문가는 어떤 지표를 보는지 모두 분석해서 분석할때 참고해주고":
what the forensic accounting, credit and valuation literature and practice look
at, mapped key by key to `docs/CHECKLIST.md`, `src/calculator.py`
(`calculator.json`) and `src/baselines.py` (`baselines.json`). Every row below
names its source; a row marked **missing** names the judge a change would need,
because a formula added without a hand-computed expected value is not a task
(`CLAUDE.md`). Nothing here changes a prompt or a formula: that is the
improvement loop's work, measured, or the owner's.

## 1. The frameworks, and where each one stands here

| Framework | What it watches | Here |
|---|---|---|
| Schilit, *Financial Shenanigans* (7 earnings shenanigans; later editions add cash-flow and key-metric shenanigans) | revenue recognized early or fictitious, one-time gains as operating, expenses shifted later, liabilities unrecorded, income shifted later, future expenses pulled forward; cash flow dressed by working-capital timing, factoring, capitalizing; non-GAAP and KPI drift | the accounting analyst's seven areas are this list in the pipeline's words (`CHECKLIST.md` §1, §11); `cash_flow_engineering_and_off_balance_sheet` covers factoring (`proceeds_from_sale_of_receivables`), supplier finance (`supplier_finance_obligation`), capitalization; `non_gaap_gap_widening` is a Python indicator |
| Beneish M-score (1999; 2013 accruals variant) | DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA | `baselines.json: beneish_m_score`, with its inputs and the −1.78 line, never handed to an agent |
| Sloan (1996) accruals | balance-sheet accruals over average assets | `baselines.json: accruals_over_assets`; `calculator: earnings_versus_cash.accruals_over_average_assets` |
| Dechow, Ge, Larson and Sloan (2011) F-score, model 1 | RSST accruals, ΔAR, ΔINV, soft assets, Δcash sales, ΔROA, issuance; logit −7.893 + 0.790 RSST + 2.518 ΔAR + 1.191 ΔINV + 1.979 %SFT + 0.171 ΔCashSales − 0.932 ΔROA + 1.029 Issue; F = p/0.0037 | **missing as a score**; `soft_assets_rising`, `accruals_high`, `receivables_outrun_revenue`, `net_stock_issuance` are its pieces as separate indicators. Judge for adding it: the Enron worked example in the teaching note (logit −4.575 → F 2.76) as the hand-computed case, plus one company's inputs read off companyfacts by hand |
| Montier C-score (2008) | six yes/no flags: NI−CFO divergence widening, DSO rising, DSI rising, other current assets/revenue rising, depreciation/PPE falling, asset growth high | **missing as a score**; five of six pieces exist (`operating_cash_flow_over_net_income`, `days_sales_outstanding`, `days_sales_of_inventory`, `asset_growth_high`, depreciation and PPE are terms); other current assets is not a term. Judge: one company's six flags by hand from its companyfacts |
| Piotroski F-score (2000) | nine binary signals | `baselines.json: piotroski_f_score` |
| Altman Z (1968), Ohlson O (1980) | distress scores | `baselines.json: altman_z_score` (needs market value; written with its reason until a price exists), `ohlson_o_score` |
| CFA Institute, *Financial Reporting Quality* (Level II) | earnings persistence and accruals; receivables growing faster than revenue; fourth-quarter concentration; allowances swinging; goodwill over assets; off-balance-sheet items; CFO far below operating income; unusual or absent items | `receivables_outrun_revenue`, `fourth_quarter_dump`, `bad_debt_reserve_thinning`, `inventory_reserve_thinning`, `warranty_reserve_thinning`, `earnings_too_smooth`, `operating_cash_flow_over_net_income`; **goodwill over total assets is missing** as a number (`goodwill_headroom_shrinking` is read by the model from the note) |
| SEC enforcement (Cornerstone FY2024–2025) | revenue recognition and internal-control violations in 58% of FY2024 actions; revenue in about a third of settled orders | the `revenue_recognition` and `controls_audit_and_filing_signals` areas; the ground truth of this project is the restatement and the AAER (`src/restatement_trace.py`) |
| Moody's and S&P corporate methodologies | Debt/EBITDA, EBIT or EBITDA interest coverage, CFO or FFO or RCF over debt, debt to capital, asset coverage, revenue stability; standard adjustments for leases and pensions | `debt_over_ebitda`, `interest_coverage`, `net_debt`, `liabilities_over_assets`, `operating_lease_liability` as a term; **CFO over total debt and debt to capital are missing**; the lease adjustment to debt is a term, not folded into leverage |
| Damodaran (DCF practice) | ROIC = after-tax operating income over (book equity + book debt − cash); reinvestment rate = (net capex + Δnon-cash working capital) / after-tax operating income; growth = reinvestment × ROIC; sales-to-capital | `return_on_invested_capital`, `free_cash_flow_to_firm`; **reinvestment rate and sales-to-capital are missing** as numbers the valuation analyst could cite against the drivers it chooses |
| 2026 oversight research (reward hacking; Huang et al., SpecBench) | metrics kept outside the agent's control, independent recomputation | the gates, `evals/`, the measurement (`docs/improve_loop.md`) |

## 2. What the analysts can already cite, by area

Counted off `runs/FN/0001408710-26-000028/calculator_filings_only.json`: 120
numeric fields, of which the accounting analyst's seven areas draw on
`earnings_versus_cash.*` (cash over net income, accruals, the working-capital
articulation gaps and their share of net income), `ratios.efficiency.*` (DSO,
DSI, DPO, the cash conversion cycle), the reserves as terms
(`bad_debt_allowance`, `inventory_reserve`, `warranty_accrual`), the
off-balance-sheet terms, `concentration`, and the trend table; the financial
analyst on `ratios.profitability.*` with DuPont, `ratios.liquidity.*`,
`ratios.solvency.*`, `ratios.growth.*`, `free_cash_flow.*` (four measures). The
formula baselines sit beside them and never enter an agent's input.

## 3. Gaps, each with the judge a change would need

Ranked by how often the literature and the enforcement record lean on them, and
by how cheap the arithmetic is from terms the calculator already holds.

| # | Add | Where | Inputs already held | Judge (expected value from the source, never from the code) |
|---|---|---|---|---|
| 1 | cash conversion pair: free cash flow over net income; operating cash flow over EBITDA | `calculator: free_cash_flow`, `ratios.solvency` | yes | hand computation in the test from one company's companyfacts values, written out |
| 2 | capital expenditure over depreciation and amortization (maintenance versus growth; Schilit's capitalization lens) | `calculator: earnings_versus_cash` | yes | same |
| 3 | operating cash flow over total debt; debt over (debt + equity) | `calculator: ratios.solvency` | yes | same; Moody's and S&P both publish the definitions |
| 4 | goodwill and intangibles over total assets, and their change | `calculator: earnings_versus_cash` (the soft-assets family) | goodwill is not yet a term: `fetch_companyfacts` would add `Goodwill` and `IntangibleAssetsNetExcludingGoodwill` | the tag values read off companyfacts by hand for one company |
| 5 | share-based compensation over revenue and over operating cash flow (the add-back's weight in cash flow) | `calculator: earnings_versus_cash` | yes (`share_based_compensation`) | hand computation |
| 6 | reinvestment rate and sales-to-capital (Damodaran) | `calculator: valuation` inputs, shown to the valuation analyst | yes | the 3M worked example in Damodaran's notes (reinvestment rate 44% at g 3%, ROC 6.76%) as the hand case |
| 7 | Montier C-score | `baselines.json` | five of six | one company's six flags by hand; other current assets needs a new term (`OtherAssetsCurrent`) |
| 8 | Dechow F-score, model 1 | `baselines.json` | RSST needs long-term investments and preferred stock terms; issuance needs `ProceedsFromIssuanceOfCommonStock` and long-term debt issuance | the Enron example and one company's hand case |
| 9 | effective tax rate against the statutory rate, and the discrete-items share | `calculator: tax_rate` exists as a rate; the statutory comparison is missing | yes for the rate | hand computation; the statutory rate is a constant with its source |
| 10 | days payable against the supplier-finance obligation (stretched payables disguised as financing) | `cash_flow_engineering` area | yes (`supplier_finance_obligation`, `accounts_payable`) | hand computation |

Rows 1 to 3, 5 and 9 are arithmetic over terms every run already holds and are
one pull request with their tests; rows 4, 7 and 8 need new companyfacts terms
first; row 6 is for the valuation analyst and changes what that layer sees,
which `src/agent_inputs.py` and its test hold. All of them are calculator
formulas, so by the owner's rule of 2026-09-28 each pull request needs the two
lenses before it opens.

## 4. What the analysts should read for, in words (for the prompts, measured first)

The literature's unanimous short list, in the order enforcement cases actually
occur: revenue recognized before it is earned (receivables outrunning revenue,
deferred revenue shrinking against growth, bill-and-hold and channel terms in
the notes, fourth-quarter concentration); reserves released into income
(allowances and warranty and inventory reserves thinning while the base grows);
costs moved onto the balance sheet (capitalized development, capex above
depreciation, soft assets rising); cash flow dressed (factoring, supplier
finance, payables stretched, one-time tax or working-capital timing); and the
tells around them (a new critical audit matter, an auditor change, a finance
officer leaving, a non-GAAP gap widening, a filing late). The accounting
analyst's prompt names each of these already; what it does not do is name the
numbers to cite for each, which rows 1 to 5 above would give it. Any change to
the prompts is a candidate for the improvement loop, measured against held-in
and held-out runs, never written in on the strength of this report.

## Sources

- Schilit framework summaries: [Journal of Forensic and Investigative Accounting, 2010, vol. 2 issue 2](http://web.nacva.com/JFIA/), [MAAW summary](https://maaw.info/ArticleSummaries/ArtSumSchilit2002.htm), [Validea](https://blog.validea.com/accounting-shenanigans-companies-use-to-trick-investors/)
- Dechow, Ge, Larson, Sloan (2011) model 1, coefficients and the Enron example: [OSU teaching note](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/3/40936/files/2016/12/F-Score-xx23jg.pdf); the paper: [SSRN 997483](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=997483)
- Beneish and Dechow compared: [Emerald, Polish companies](https://www.emerald.com/cemj/article/34/3/488/1304262/Evaluating-the-efficacy-of-modified-Beneish-and)
- Montier C-score: [quant-investing glossary](https://www.quant-investing.com/glossary/c-score-montier), [Old School Value](https://oldschoolvalue.com/stock-valuation/c-score-montier), [GMT Research](https://www.gmtresearch.com/montiers-c-score/)
- Piotroski and Altman: [Umbrex](https://umbrex.com/resources/frameworks/finance-frameworks/piotroski-f-score/), [fairpriceindex](https://www.fairpriceindex.com/education/piotroski-f-score), [Altman Z](https://www.geminiq.com/blog/altman-z-score-financial-distress)
- CFA Institute reading outline: [Financial Reporting Quality](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/financial-reporting-quality); study notes: [AnalystPrep earnings quality](https://analystprep.com/study-notes/cfa-level-2/indicators-earning-quality/), [cash flow quality](https://analystprep.com/study-notes/cfa-level-2/indicators-cash-flow-quality/)
- SEC enforcement: [Cornerstone FY2024](https://www.cornerstone.com/insights/reports/sec-accounting-and-auditing-enforcement-activity-year-in-review-fy-2024/), [Cornerstone 2025](https://www.cornerstone.com/insights/reports/sec-accounting-and-auditing-enforcement-activity2025-year-in-review/), [Floyd Advisory 2024](https://floydadvisory.com/wp-content/uploads/2025/02/Floyd-Advisory_AAER_Q4-2024-Annual.pdf)
- Credit ratios: [Moody's ratio distributions](https://www.moodys.com/sites/products/defaultresearch/2005700000436062.pdf), [Moody's 2021 steel methodology](https://ratings.moodys.com/api/rmc-documents/356428), [S&P fundamentals overview (CFI)](https://corporatefinanceinstitute.com/resources/commercial-lending/standard-poors-fundamentals-of-corporate-credit-analysis/)
- Damodaran: [FCFF notes](https://pages.stern.nyu.edu/~adamodar/pdfiles/eqnotes/fcff.pdf), [valuation session slides](https://pages.stern.nyu.edu/~adamodar/podcasts/valspr15/valsession10.pdf)
