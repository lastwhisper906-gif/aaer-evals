<!-- the quote gate removed 2 item(s) from this copy; input_manifest.json lists each with its reason -->
# QCOM — numbers reader — 10-Q 0000804328-26-000086 (quarter ended 2026-06-28)

Notes on this run, outside the items:

- **Inputs read.** I read input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json in full. None of them contains prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.
- **Inputs missing.** My instructions name four inputs that are not in this directory: the articulation checks, the restatement traces, the fourth-quarter derivation (src/fourth_quarter.py output) and the formula baselines beyond the inputs printed inside trend cells.
  - Because the articulation checks are missing, there are no articulation gaps I can report.
  - I found restated prior values only by reading the `superseded_by` marker on the numeric facts and comparing the two printed values. Exactly one value differs (Alphawave goodwill, item below). Every other superseded fact I compared carries the same value in the later filing, including:
    - inventory and its components
    - receivables and accrued income taxes
    - restricted cash and equity balances
    - the U.S. federal valuation-allowance change
    - the full-year tax-rate forecasts
    - the Alphawave consideration and the other Alphawave allocation lines
- **Prior predictions.** None on record. There is nothing to carry forward.
- **Periods the record does not reach.** quarters-back-3 (target 2025-09-28) and quarters-back-7 (target 2024-09-29) have no cells. The reason the table gives for both: "no quarter ending within 20 days of 2025-09-28 [resp. 2024-09-29] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". That derivation is not in my input.
  - As a result, every quarterly position below is out of 6 filled quarters. Every annual position is out of 5 filled years. A six-point quarterly history is short; positions describe it and do not establish a trend.
- **Values I cannot quote.** The years-back-0 research-and-development-capitalised block prints values without a paragraph_id, so I cannot quote them and wrote no item:
  - earnings_with_rnd_capitalized 6771800000.0
  - research_and_development_amortization 7811200000.0
  - research_and_development_asset 26160000000.0
  - book_value_with_rnd_capitalized: missing, "no row for stockholders_equity in 2025-09-28: us-gaap:StockholdersEquity is in the record, but not for this period"
  - capitalized_development_cost: never tagged
- **expected_direction.** For trend cells, this is the sign shared by every change Python printed on the row; it is `none` where the printed changes disagree or the cell is insufficient. For facts, it is the direction of the quoted value against the comparative printed alongside it in my input. I computed no number. Every figure below is copied as printed.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly_grid", "what_changed": "insufficient. Accruals over total assets has no value for the quarter 2026-03-30..2026-06-28: operating cash flow is in the record only as year-to-date durations, not for this three-month period, so neither the quarter-over-quarter nor the year-over-year change exists. The ratio is also unfilled in quarters-back-1, -4 and -5; the quarterly grid holds it only where a discrete quarter of operating cash flow was filed.", "account": "Accruals (NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities) over Assets", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for operating_cash_flow in 2026-03-30..2026-06-28: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0000804328-26-000086:trends:accruals_over_total_assets:2026-03-30..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly_grid", "what_changed": "insufficient. No allowance for credit losses is in the record at 2026-06-28 under any of the three concepts the table looks for; the ratio is unfilled in every quarter and every year of the table (filled count 0), so there is no value, no change and no position.", "account": "Allowance for doubtful accounts over receivables", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-28: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0000804328-26-000086:trends:bad_debt_reserve_ratio:2026-03-30..2026-06-28" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_quarterly_grid", "what_changed": "Current contract liabilities over quarterly revenue is 0.028149190710767064 (DeferredRevenueCurrent 280000000.0 over Revenues 9947000000.0). Change against quarters-back-1: -0.0023253823621643445; against quarters-back-4: 0.0006528086557743007. Third highest of the 6 filled quarters. The two printed changes have opposite signs.", "account": "DeferredRevenueCurrent (unearned revenues) over Revenues", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"", "paragraph_id": "0000804328-26-000086:trends:contract_liabilities_over_revenue:2026-03-30..2026-06-28" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_quarterly_grid", "what_changed": "Days sales of inventory is 163.27387580299785 (InventoryNet 8379000000.0 at 2026-06-28 against CostOfRevenue 4670000000.0 for the quarter). Change against quarters-back-1: 26.439590088712123; against quarters-back-4: 38.05503081819542. Highest of the 6 filled quarters. Both printed changes are positive.", "account": "InventoryNet against CostOfRevenue", "expected_direction": "up", "horizon": "next two quarters (through fiscal first quarter 2027)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0000804328-26-000086:trends:days_sales_of_inventory:2026-03-30..2026-06-28" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_quarterly_grid", "what_changed": "insufficient. No receivables row exists at 2026-06-28 under the three concepts the table reads (AccountsReceivableNetCurrent, ReceivablesNetCurrent, AccountsReceivableNet). The 10-Q tags its balance-sheet receivable line as AccountsAndOtherReceivablesNetCurrent (4668000000 at 2026-06-28), a concept the table does not read, so days sales outstanding is unfilled in every filled quarter (quarters-back-0, -1, -2, -4, -5, -6). See the receivables concept items below.", "account": "Receivables over revenue times days", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for receivables in 2026-06-28: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"", "paragraph_id": "0000804328-26-000086:trends:days_sales_outstanding:2026-03-30..2026-06-28" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_quarterly_grid", "what_changed": "Gross margin is 0.5305117120739922 (Revenues 9947000000.0, CostOfRevenue 4670000000.0). Change against quarters-back-1: -0.007180523042528253; against quarters-back-4: -0.025108162503914233. Lowest of the 6 filled quarters. Both printed changes are negative. The 8-K attributes pressure to a broad-based increase in input costs (item across_documents_input_cost_pressure_beside_lowest_gross_margin).", "account": "Gross margin (Revenues less CostOfRevenue, over Revenues)", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0000804328-26-000086:trends:gross_margin:2026-03-30..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_quarterly_grid", "what_changed": "insufficient. The record tags no us-gaap:InventoryValuationReserves in any period, so the inventory reserve ratio is unfilled in every quarter and year (filled count 0). The inventory components the 10-Q does tag are each stated net of reserves (see the inventory component items), so the reserve itself is not visible in my input.", "account": "Inventory valuation reserve over gross inventory", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0000804328-26-000086:trends:inventory_reserve_ratio:2026-03-30..2026-06-28" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_quarterly_grid", "what_changed": "insufficient. No us-gaap concept carries non-GAAP net income, so the table holds no non-GAAP gap in any period (filled count 0). The 8-K prints Non-GAAP net income of $2,356 million against GAAP net income of $2,002 million for the third quarter of fiscal 2026 (paragraph 0000804328-26-000085:8k_2_02:18); no gap is computed in my input, and I do not compute one.", "account": "Non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000804328-26-000086:trends:non_gaap_gap:2026-03-30..2026-06-28" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_quarterly_grid", "what_changed": "insufficient. Same cause as days sales outstanding: no receivables row at 2026-06-28 under the concepts the table reads, because the 10-Qs tag the line as AccountsAndOtherReceivablesNetCurrent. Unfilled in every filled quarter, so no value, change or position exists.", "account": "Receivables over revenue", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for receivables in 2026-06-28: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"", "paragraph_id": "0000804328-26-000086:trends:receivables_over_revenue:2026-03-30..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_trend_quarterly_grid", "what_changed": "Soft asset share is 0.8300416615824429 (Assets 57367000000.0, PropertyPlantAndEquipmentNet 5217000000.0, CashAndCashEquivalentsAtCarryingValue 4533000000.0). Change against quarters-back-1: 0.01391872683027262; against quarters-back-4: 0.011296446315044673. Highest of the 6 filled quarters. Both printed changes are positive. Over the same months the balance sheet shows goodwill, deferred tax assets and inventory higher and cash lower (items below).", "account": "Assets less PP&E and cash, over Assets", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0000804328-26-000086:trends:soft_asset_share:2026-03-30..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_quarterly_grid", "what_changed": "insufficient. The record tags none of the three warranty-accrual concepts in any period, so the warranty reserve ratio is unfilled throughout the table (filled count 0).", "account": "Product warranty accrual over revenue", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0000804328-26-000086:trends:warranty_reserve_ratio:2026-03-30..2026-06-28" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_annual_grid", "what_changed": "Accruals over total assets for fiscal 2025 (2024-09-30..2025-09-28) is -0.16893684063578165 (NetIncomeLoss 5541000000.0, operating cash flow 14012000000.0, Assets 50143000000.0). Change against years-back-1: -0.131586875084779. Lowest of the 5 filled years. The quarter-over-quarter field reads 'an annual period has no preceding quarter'. Net income sat far below operating cash flow in a year the 10-K shows a 0.56 effective tax rate and a valuation allowance of 8016000000 (estimates item below).", "account": "Accruals (NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities) over Assets", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27), first annual filing after this quarter", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:accruals_over_total_assets:2024-09-30..2025-09-28" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_annual_grid", "what_changed": "insufficient. No allowance for credit losses at 2025-09-28 under the concepts the table reads; unfilled in all five years, so there is no value, change or position.", "account": "Allowance for doubtful accounts over receivables", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-09-28: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0000804328-26-000086:trends:bad_debt_reserve_ratio:2024-09-30..2025-09-28" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_annual_grid", "what_changed": "Contract liabilities over revenue for fiscal 2025 is 0.008084183903893054 (DeferredRevenueCurrent 358000000.0 at 2025-09-28, Revenues 44284000000.0). Change against years-back-1: 0.0004613719332549962. Second lowest of the 5 filled years.", "account": "DeferredRevenueCurrent over Revenues", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:contract_liabilities_over_revenue:2024-09-30..2025-09-28" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_annual_grid", "what_changed": "Days sales of inventory for fiscal 2025 is 120.3497821461141 (InventoryNet 6526000000.0 at 2025-09-28, CostOfRevenue 19738000000.0). Change against years-back-1: -19.32976064403833. Second lowest of the 5 filled years. The quarterly grid has since moved to the highest of its 6 filled quarters (163.27387580299785).", "account": "InventoryNet against CostOfRevenue", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:days_sales_of_inventory:2024-09-30..2025-09-28" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_annual_grid", "what_changed": "Days sales outstanding for fiscal 2025 is 23.467166470960166 (AccountsReceivableNetCurrent 2855000000.0 from the 10-K at 2025-09-28, Revenues 44284000000.0). Change against years-back-1: 1.1188013972986504. Third highest of the 5 filled years. The receivables input is the 10-K's AccountsReceivableNetCurrent, not the balance-sheet line 'Accounts receivable, net' (AccountsAndOtherReceivablesNetCurrent 4315000000 at the same date).", "account": "AccountsReceivableNetCurrent over Revenues times days", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:days_sales_outstanding:2024-09-30..2025-09-28" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_annual_grid", "what_changed": "Gross margin for fiscal 2025 is 0.5542859723602204 (Revenues 44284000000.0, CostOfRevenue 19738000000.0). Change against years-back-1: -0.007851494915586787. Lowest of the 5 filled years. The latest quarter (0.5305117120739922) is the lowest of the 6 filled quarters.", "account": "Gross margin (Revenues less CostOfRevenue, over Revenues)", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:gross_margin:2024-09-30..2025-09-28" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_annual_grid", "what_changed": "insufficient. us-gaap:InventoryValuationReserves is tagged in no period; the annual cell is unfilled, as in every year of the table.", "account": "Inventory valuation reserve over gross inventory", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0000804328-26-000086:trends:inventory_reserve_ratio:2024-09-30..2025-09-28" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_annual_grid", "what_changed": "insufficient. No us-gaap concept carries a non-GAAP measure; the annual cell is unfilled in all five years.", "account": "Non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000804328-26-000086:trends:non_gaap_gap:2024-09-30..2025-09-28" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_annual_grid", "what_changed": "Receivables over revenue for fiscal 2025 is 0.06447023755758287 (AccountsReceivableNetCurrent 2855000000.0, Revenues 44284000000.0). Change against years-back-1: 0.004232056766042394. Third highest of the 5 filled years. Same receivables-concept caveat as days sales outstanding.", "account": "AccountsReceivableNetCurrent over Revenues", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:receivables_over_revenue:2024-09-30..2025-09-28" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_trend_annual_grid", "what_changed": "Soft asset share for fiscal 2025 is 0.7963823464890414 (Assets 50143000000.0, PropertyPlantAndEquipmentNet 4690000000.0, CashAndCashEquivalentsAtCarryingValue 5520000000.0 at 2025-09-28). Change against years-back-1: 0.023274321685763266. Second highest of the 5 filled years.", "account": "Assets less PP&E and cash, over Assets", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000804328-26-000086:trends:soft_asset_share:2024-09-30..2025-09-28" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_annual_grid", "what_changed": "insufficient. None of the warranty-accrual concepts is tagged in any period; the annual cell is unfilled.", "account": "Product warranty accrual over revenue", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0000804328-26-000086:trends:warranty_reserve_ratio:2024-09-30..2025-09-28" }
```

```json
{ "id": "articulation_and_the_filed_history_alphawave_goodwill_restated_by_later_filing", "what_changed": "Restated prior value. The 10-Q filed 2026-04-29 (0000804328-26-000061) reported goodwill recognised on the Alphawave acquisition at the 2025-12-18 acquisition date as 2215000000, and that fact is marked superseded_by 0000804328-26-000086. The current 10-Q reports 2210000000 for the same instant and member. The other Alphawave allocation lines are printed with the same values in both filings: consideration 2300000000, total assets acquired 2895000000, liabilities assumed 621000000, net assets including goodwill 2274000000, intangibles 239000000, indefinite-lived intangibles 107000000, cash 51000000. My input does not say why goodwill moved. This is the only superseded fact I found whose later value differs.", "account": "Goodwill, Alphawave acquisition (purchase-price allocation)", "expected_direction": "down", "horizon": "until the Alphawave purchase-price allocation is final; my input does not state when", "quote": "\"value\": \"2215000000\"", "paragraph_id": "0000804328-26-000061:facts:Goodwill:2025-12-18:us-gaap:BusinessAcquisitionAxis=qcom:AlphawaveMember" }
```

```json
{ "id": "articulation_and_the_filed_history_receivables_tagged_with_broader_concept_in_quarterly_filings", "what_changed": "Concept difference between filings. The current 10-Q tags the balance-sheet line 'Accounts receivable, net' as us-gaap:AccountsAndOtherReceivablesNetCurrent: 4668000000 at 2026-06-28, 4315000000 at 2025-09-28, and 4347000000 at 2026-03-29 in 0000804328-26-000061. The trend table reads only AccountsReceivableNetCurrent, ReceivablesNetCurrent or AccountsReceivableNet, so every quarterly receivables cell is missing. On the line itself, the balance is higher at 2026-06-28 than at both earlier dates.", "account": "AccountsAndOtherReceivablesNetCurrent (balance-sheet accounts receivable, net)", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"4668000000\"", "paragraph_id": "0000804328-26-000086:facts:AccountsAndOtherReceivablesNetCurrent:2026-06-28" }
```

```json
{ "id": "articulation_and_the_filed_history_receivables_trend_input_narrower_than_balance_sheet_line", "what_changed": "Concept difference inside the annual trend cell. The fiscal 2025 days-sales-outstanding and receivables-over-revenue cells rest on the 10-K's us-gaap:AccountsReceivableNetCurrent of 2855000000.0 at 2025-09-28. The balance-sheet line at the same date is AccountsAndOtherReceivablesNetCurrent 4315000000, and the 10-K also tags UnbilledContractsReceivable 1443000000. The annual receivables ratios therefore measure a narrower receivable than the face line, and the quarterly grid cannot be compared with them.", "account": "AccountsReceivableNetCurrent (trend input) against AccountsAndOtherReceivablesNetCurrent (balance sheet)", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27), when the next 10-K restates the line", "quote": "\"value\": 2855000000.0", "paragraph_id": "0000804328-26-000086:trends:days_sales_outstanding:2024-09-30..2025-09-28" }
```

```json
{ "id": "structure_and_disclosure_changes_segment_cost_of_revenue_sign_flipped_between_filings", "what_changed": "Sign convention differs by filing for the same concept and member. The current 10-Q tags QCT segment CostOfRevenue (ConsolidationItemsAxis=OperatingSegmentsMember, QctMember) as -4452000000 for the quarter and -4497000000 for the prior-year quarter. The 10-Q filed 2026-04-29 also tags it negative (-4700000000). The 10-K tags the fiscal 2025 QCT CostOfRevenue positive (19302000000). Consolidated CostOfRevenue is positive in every filing (4670000000 this quarter). Any series built across these filings from the segment fact flips sign at the 10-K/10-Q boundary.", "account": "CostOfRevenue, QCT operating segment", "expected_direction": "none", "horizon": "next 10-K (fiscal year 2026)", "quote": "\"value\": \"-4452000000\"", "paragraph_id": "0000804328-26-000086:facts:CostOfRevenue:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QctMember" }
```

```json
{ "id": "structure_and_disclosure_changes_commercial_paper_context_dimension_dropped", "what_changed": "Context change for the same concept. The current 10-Q tags CommercialPaper without a dimension: 498000000 at 2026-06-28 and 0 at 2025-09-28. The 10-Q filed 2026-04-29 tagged it under CreditFacilityAxis=CommercialPaperMember (498000000 at 2026-03-29, 0 at 2025-09-28). Values agree where both exist. The current filing also splits short-term debt into CommercialPaper 498000000 and LongTermDebtCurrent 1991000000.", "account": "CommercialPaper", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"498000000\"", "paragraph_id": "0000804328-26-000086:facts:CommercialPaper:2026-06-28" }
```

```json
{ "id": "earnings_quality_inventory_balance_build_on_balance_sheet", "what_changed": "Net inventory is 8379000000 at 2026-06-28, against 6526000000 at 2025-09-28 (same filing) and 7368000000 at 2026-03-29 (0000804328-26-000061). It is higher than at both earlier dates. The trend table puts quarterly days sales of inventory at the highest of 6 filled quarters.", "account": "InventoryNet", "expected_direction": "up", "horizon": "next two quarters (through fiscal first quarter 2027)", "quote": "\"value\": \"8379000000\"", "paragraph_id": "0000804328-26-000086:facts:InventoryNet:2026-06-28" }
```

```json
{ "id": "earnings_quality_inventory_work_in_process_component", "what_changed": "Work in process, net of reserves, is 5005000000 at 2026-06-28, against 3985000000 at 2025-09-28 and 4346000000 at 2026-03-29 (0000804328-26-000061). It is the largest of the three tagged components.", "account": "InventoryWorkInProcessNetOfReserves", "expected_direction": "up", "horizon": "next two quarters (through fiscal first quarter 2027)", "quote": "\"value\": \"5005000000\"", "paragraph_id": "0000804328-26-000086:facts:InventoryWorkInProcessNetOfReserves:2026-06-28" }
```

```json
{ "id": "earnings_quality_inventory_raw_materials_component", "what_changed": "Raw materials, net of reserves, is 682000000 at 2026-06-28, against 336000000 at 2025-09-28 and 580000000 at 2026-03-29 (0000804328-26-000061).", "account": "InventoryRawMaterialsNetOfReserves", "expected_direction": "up", "horizon": "next two quarters (through fiscal first quarter 2027)", "quote": "\"value\": \"682000000\"", "paragraph_id": "0000804328-26-000086:facts:InventoryRawMaterialsNetOfReserves:2026-06-28" }
```

```json
{ "id": "earnings_quality_inventory_finished_goods_component", "what_changed": "Finished goods, net of reserves, is 2692000000 at 2026-06-28, against 2205000000 at 2025-09-28 and 2442000000 at 2026-03-29 (0000804328-26-000061).", "account": "InventoryFinishedGoodsNetOfReserves", "expected_direction": "up", "horizon": "next two quarters (through fiscal first quarter 2027)", "quote": "\"value\": \"2692000000\"", "paragraph_id": "0000804328-26-000086:facts:InventoryFinishedGoodsNetOfReserves:2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_inventory_build_absorbs_operating_cash", "what_changed": "The cash-flow statement's increase in inventories is 1798000000 for 2025-09-29..2026-06-28, against -33000000 for 2024-09-30..2025-06-29. The 10-Q filed 2026-04-29 showed 802000000 for 2025-09-29..2026-03-29. The 8-K prints the line as 'Inventories | (1,798)'.", "account": "IncreaseDecreaseInInventories", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"1798000000\"", "paragraph_id": "0000804328-26-000086:facts:IncreaseDecreaseInInventories:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_lower_in_filed_cash_flow_statement", "what_changed": "Net cash from operating activities is 8405000000 for 2025-09-29..2026-06-28, against 10016000000 for 2024-09-30..2025-06-29. The 10-Q filed 2026-04-29 showed 7414000000 for 2025-09-29..2026-03-29 (against 7141000000). Net income for the same year-to-date span is 12377000000 against 8658000000. A discrete-quarter operating cash flow is not in the record, which is why quarterly accruals is insufficient.", "account": "NetCashProvidedByUsedInOperatingActivities", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"8405000000\"", "paragraph_id": "0000804328-26-000086:facts:NetCashProvidedByUsedInOperatingActivities:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditures_higher", "what_changed": "Payments to acquire productive assets are 1578000000 for 2025-09-29..2026-06-28, against 785000000 for 2024-09-30..2025-06-29. Net PP&E is 5217000000 at 2026-06-28 against 4690000000 at 2025-09-28.", "account": "PaymentsToAcquireProductiveAssets", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"1578000000\"", "paragraph_id": "0000804328-26-000086:facts:PaymentsToAcquireProductiveAssets:2025-09-29..2026-06-28" }
```


```json
{ "id": "estimates_and_discretion_deferred_tax_asset_jump", "what_changed": "Net deferred tax assets are 5679000000 at 2026-06-28, against 743000000 at 2025-09-28 and 5968000000 at 2026-03-29 (0000804328-26-000061). The balance stepped up in the March quarter alongside the U.S. federal valuation-allowance change (next item) and is lower at June than at March.", "account": "DeferredIncomeTaxAssetsNet", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"5679000000\"", "paragraph_id": "0000804328-26-000086:facts:DeferredIncomeTaxAssetsNet:2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_federal_valuation_allowance_release", "what_changed": "Change in the U.S. federal deferred-tax valuation allowance is -5700000000 for 2025-12-29..2026-03-29, after +5700000000 for fiscal 2025 (2024-09-30..2025-09-28), both on ValuationAllowanceByDeferredTaxAssetAxis=U.S.FederalMember. Both values are carried unchanged from the 10-Q filed 2026-04-29. The 10-K shows the total valuation allowance at 8016000000 at 2025-09-28 against 2061000000 a year earlier, and a fiscal 2025 effective tax rate of 0.56 against 0.02. The allowance was built in one year and released in the next.", "account": "ValuationAllowanceDeferredTaxAssetChangeInAmount (U.S. federal)", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"-5700000000\"", "paragraph_id": "0000804328-26-000086:facts:ValuationAllowanceDeferredTaxAssetChangeInAmount:2025-12-29..2026-03-29:us-gaap:ValuationAllowanceByDeferredTaxAssetAxis=qcom:U.S.FederalMember" }
```

```json
{ "id": "estimates_and_discretion_income_tax_benefit_in_filed_year_to_date", "what_changed": "Income tax expense (benefit) is -4136000000 for 2025-09-29..2026-06-28, against 1034000000 for 2024-09-30..2025-06-29. The 10-Q filed 2026-04-29 showed -5138000000 for the March quarter alone. This quarter's expense is 460000000 against 286000000. Year-to-date net income of 12377000000 against pre-tax income of 8241000000 reflects the benefit.", "account": "IncomeTaxExpenseBenefit", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"-4136000000\"", "paragraph_id": "0000804328-26-000086:facts:IncomeTaxExpenseBenefit:2025-09-29..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_rise_in_latest_quarter", "what_changed": "Effective tax rate is 0.19 for 2026-03-30..2026-06-28, against 0.10 for 2025-03-31..2025-06-29. The 10-Q filed 2026-04-29 showed -2.30 for 2025-12-29..2026-03-29. The 8-K applies a fixed estimated Non-GAAP tax rate (structure item below).", "account": "EffectiveIncomeTaxRateContinuingOperations", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"0.19\"", "paragraph_id": "0000804328-26-000086:facts:EffectiveIncomeTaxRateContinuingOperations:2026-03-30..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_negative_full_year_effective_tax_rate_forecast", "what_changed": "The 10-Q tags a forecast (ScenarioForecastMember) effective tax rate of -0.40 for 2025-09-29..2026-09-27, the full fiscal 2026. The FDDEI-specific forecast rate is 0.13. Both are the same values the 10-Q filed 2026-04-29 printed, which this filing supersedes without change.", "account": "EffectiveIncomeTaxRateContinuingOperations (forecast, fiscal 2026)", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"-0.40\"", "paragraph_id": "0000804328-26-000086:facts:EffectiveIncomeTaxRateContinuingOperations:2025-09-29..2026-09-27:srt:StatementScenarioAxis=srt:ScenarioForecastMember" }
```

```json
{ "id": "liquidity_and_capital_accrued_income_taxes_lower", "what_changed": "Accrued income taxes, current, are 557000000 at 2026-06-28, against 1007000000 at 2025-09-28 and 508000000 at 2026-03-29 (0000804328-26-000061).", "account": "AccruedIncomeTaxesCurrent", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"557000000\"", "paragraph_id": "0000804328-26-000086:facts:AccruedIncomeTaxesCurrent:2026-06-28" }
```

```json
{ "id": "earnings_quality_nonoperating_income_jump", "what_changed": "Investment and other income, net (NonoperatingIncomeExpense) is 1014000000 for 2026-03-30..2026-06-28, against 358000000 for the prior-year quarter. The March quarter showed 94000000 (0000804328-26-000061). Pre-tax income of 2462000000 includes it, while operating income is 1626000000.", "account": "NonoperatingIncomeExpense", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"1014000000\"", "paragraph_id": "0000804328-26-000086:facts:NonoperatingIncomeExpense:2026-03-30..2026-06-28" }
```

```json
{ "id": "earnings_quality_realized_gains_on_marketable_securities", "what_changed": "Realized gains on marketable securities are 726000000 for 2026-03-30..2026-06-28, against 204000000 for the prior-year quarter and -64000000 for the March quarter (0000804328-26-000061). Year to date they are 605000000 against 241000000. The 8-K says gains of this kind 'cannot be accurately forecast' and are left out of the outlook.", "account": "MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"726000000\"", "paragraph_id": "0000804328-26-000086:facts:MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments:2026-03-30..2026-06-28" }
```

```json
{ "id": "earnings_quality_strategic_investments_segment_pretax_contribution", "what_changed": "QSI (strategic investments) segment earnings before taxes are 768000000 for 2026-03-30..2026-06-28. The 8-K reconciliation removes this amount ('Less QSI' 768 on EBT) in arriving at Non-GAAP EBT of $2,693 million, against GAAP EBT of $2,462 million.", "account": "IncomeLossFromContinuingOperationsBeforeIncomeTaxes, QSI segment", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"768000000\"", "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QsiMember" }
```

```json
{ "id": "results_against_expectations_operating_income_decline", "what_changed": "Operating income is 1626000000 for 2026-03-30..2026-06-28, against 2762000000 for the prior-year quarter. Year to date it is 7302000000 against 9437000000.", "account": "OperatingIncomeLoss", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"1626000000\"", "paragraph_id": "0000804328-26-000086:facts:OperatingIncomeLoss:2026-03-30..2026-06-28" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_research_and_development_growth", "what_changed": "Research and development expense is 2607000000 for the quarter against 2226000000 a year earlier. Year to date it is 7523000000 against 6672000000. Revenue fell over the same quarter (9947000000 against 10365000000).", "account": "ResearchAndDevelopmentExpense", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"2607000000\"", "paragraph_id": "0000804328-26-000086:facts:ResearchAndDevelopmentExpense:2026-03-30..2026-06-28" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_selling_general_and_administrative_growth", "what_changed": "Selling, general and administrative expense is 976000000 for the quarter against 771000000 a year earlier. Year to date it is 2738000000 against 2200000000.", "account": "SellingGeneralAndAdministrativeExpense", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"976000000\"", "paragraph_id": "0000804328-26-000086:facts:SellingGeneralAndAdministrativeExpense:2026-03-30..2026-06-28" }
```

```json
{ "id": "estimates_and_discretion_restructuring_charge_in_other_operating_expense", "what_changed": "Restructuring and related cost is 68000000 for 2026-03-30..2026-06-28 and 97000000 year to date. The 10-Q filed 2026-04-29 showed 29000000 for 2025-09-29..2026-03-29. The income statement's 'Other' operating line (OtherOperatingIncomeExpenseNet) is -68000000 this quarter against 0 a year earlier.", "account": "RestructuringAndRelatedCostIncurredCost", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"68000000\"", "paragraph_id": "0000804328-26-000086:facts:RestructuringAndRelatedCostIncurredCost:2026-03-30..2026-06-28" }
```

```json
{ "id": "results_against_expectations_revenue_decline_against_prior_year", "what_changed": "Revenues are 9947000000 for 2026-03-30..2026-06-28, against 10365000000 for the prior-year quarter; the 8-K prints the change as (4%). Year to date they are 32798000000 against 33013000000. The March quarter was 10599000000 (0000804328-26-000061).", "account": "Revenues", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, guided at $9.7B - $10.5B)", "quote": "\"value\": \"9947000000\"", "paragraph_id": "0000804328-26-000086:facts:Revenues:2026-03-30..2026-06-28" }
```

```json
{ "id": "results_against_expectations_net_income_decline_in_latest_quarter", "what_changed": "Net income is 2002000000 for the quarter against 2666000000 a year earlier; the 8-K prints (25%). Year to date it is 12377000000 against 8658000000; that figure carries the March-quarter tax benefit.", "account": "NetIncomeLoss", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"2002000000\"", "paragraph_id": "0000804328-26-000086:facts:NetIncomeLoss:2026-03-30..2026-06-28" }
```

```json
{ "id": "results_against_expectations_diluted_earnings_per_share", "what_changed": "Diluted EPS is 1.87 for the quarter against 2.43 a year earlier; the 8-K prints (23%) and Non-GAAP diluted EPS of $2.21 against $2.77. Year to date it is 11.53 against 7.79.", "account": "EarningsPerShareDiluted", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, GAAP diluted EPS guided at $1.22 - $1.42)", "quote": "\"value\": \"1.87\"", "paragraph_id": "0000804328-26-000086:facts:EarningsPerShareDiluted:2026-03-30..2026-06-28" }
```


```json
{ "id": "results_against_expectations_automotive_revenue_growth", "what_changed": "QCT automotive revenues are 1588000000 for the quarter against 984000000 a year earlier; the 8-K prints +61%. Year to date they are 4015000000 against 2904000000. IoT is 1830000000 against 1681000000 (+9% in the 8-K).", "account": "Revenues, QCT segment, Automotive", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"1588000000\"", "paragraph_id": "0000804328-26-000086:facts:Revenues:2026-03-30..2026-06-28:srt:ProductOrServiceAxis=qcom:AutomotiveMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QctMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_chip_segment_pretax_decline", "what_changed": "QCT segment earnings before taxes are 2192000000 for the quarter against 2671000000 a year earlier. The 8-K prints EBT as a percentage of revenues at 26% against 30% (-4 points). QCT segment revenue is 8504000000 against 8993000000.", "account": "IncomeLossFromContinuingOperationsBeforeIncomeTaxes, QCT segment", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"2192000000\"", "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QctMember" }
```

```json
{ "id": "revenue_recognition_largest_customer_concentration_rise", "what_changed": "Customer X's share of revenue is 0.23 for the quarter against 0.18 for the prior-year quarter. Year to date it is 0.24 against 0.20. The March quarter was 0.24 (0000804328-26-000061). Customer Y is 0.20 for the quarter against 0.21.", "account": "ConcentrationRiskPercentage1, Customer X, share of revenue", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"0.23\"", "paragraph_id": "0000804328-26-000086:facts:ConcentrationRiskPercentage1:2026-03-30..2026-06-28:srt:MajorCustomersAxis=qcom:CustomerXMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_current_contract_liabilities_lower", "what_changed": "Current unearned revenues are 280000000 at 2026-06-28, against 358000000 at 2025-09-28 and 323000000 at 2026-03-29 (the quarters-back-1 trend input). Noncurrent unearned revenues are 81000000 against 71000000.", "account": "DeferredRevenueCurrent", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"280000000\"", "paragraph_id": "0000804328-26-000086:facts:DeferredRevenueCurrent:2026-06-28" }
```

```json
{ "id": "revenue_recognition_unearned_revenue_cash_flow_drawdown", "what_changed": "The cash-flow change in unearned revenues is -225000000 for 2025-09-29..2026-06-28, against 3000000 a year earlier. The 10-Q filed 2026-04-29 showed -194000000 for the first half.", "account": "IncreaseDecreaseInDeferredRevenue", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"-225000000\"", "paragraph_id": "0000804328-26-000086:facts:IncreaseDecreaseInDeferredRevenue:2025-09-29..2026-06-28" }
```

```json
{ "id": "revenue_recognition_revenue_from_obligations_satisfied_earlier", "what_changed": "Revenue recognised this quarter from performance obligations satisfied in previous periods is 165000000, against 189000000 a year earlier. The March quarter was 132000000 (0000804328-26-000061). Year to date it is 417000000 against 691000000.", "account": "ContractWithCustomerPerformanceObligationSatisfiedInPreviousPeriod", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"165000000\"", "paragraph_id": "0000804328-26-000086:facts:ContractWithCustomerPerformanceObligationSatisfiedInPreviousPeriod:2026-03-30..2026-06-28" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_build", "what_changed": "The cash-flow increase in receivables is 264000000 for 2025-09-29..2026-06-28, against -535000000 a year earlier; the 8-K prints the line as 'Accounts receivable, net | (264)'. The 10-Q filed 2026-04-29 showed -58000000 for the first half. The receivables line is higher at 2026-06-28 (4668000000) than at 2025-09-28 (4315000000) while quarterly revenue is lower than a year earlier.", "account": "IncreaseDecreaseInReceivables", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"264000000\"", "paragraph_id": "0000804328-26-000086:facts:IncreaseDecreaseInReceivables:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_short_term_debt_appears", "what_changed": "Short-term debt (DebtCurrent) is 2489000000 at 2026-06-28, against 0 at 2025-09-28 and 498000000 at 2026-03-29 (0000804328-26-000061). The current filing tags it as CommercialPaper 498000000 and LongTermDebtCurrent 1991000000.", "account": "DebtCurrent", "expected_direction": "up", "horizon": "next four quarters (current maturities)", "quote": "\"value\": \"2489000000\"", "paragraph_id": "0000804328-26-000086:facts:DebtCurrent:2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_reclassified_lower", "what_changed": "Long-term debt is 12781000000 at 2026-06-28 against 14811000000 at 2025-09-28. Over the same span LongTermDebtCurrent went from 0 to 1991000000, and no long-term debt was issued or repaid year to date (both 0, against 1487000000 issued and 1365000000 repaid a year earlier). Long-term debt fair value (Level 2) is 14000000000.0 at 2026-06-28.", "account": "LongTermDebt", "expected_direction": "down", "horizon": "next four quarters", "quote": "\"value\": \"12781000000\"", "paragraph_id": "0000804328-26-000086:facts:LongTermDebt:2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_commercial_paper_issuance", "what_changed": "Commercial paper proceeds are 3238000000 for 2025-09-29..2026-06-28 and repayments 2743000000, against 998000000 and 998000000 a year earlier. The first half showed 1246000000 and 750000000 (0000804328-26-000061). Repayment of debt of an acquired company is 174000000.", "account": "ProceedsFromIssuanceOfCommercialPaper", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"3238000000\"", "paragraph_id": "0000804328-26-000086:facts:ProceedsFromIssuanceOfCommercialPaper:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_lower", "what_changed": "Cash and cash equivalents are 4533000000 at 2026-06-28, against 5520000000 at 2025-09-28. Marketable securities, current, are 3771000000 against 4635000000.", "account": "CashAndCashEquivalentsAtCarryingValue", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"4533000000\"", "paragraph_id": "0000804328-26-000086:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_restricted_cash_released", "what_changed": "Restricted cash, current, is 0 at 2026-06-28, against 2323000000 at 2025-09-28. The 8-K's cash-flow statement notes that the opening total included '$2,323 classified as restricted cash at September 28, 2025'.", "account": "RestrictedCashCurrent", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"0\"", "paragraph_id": "0000804328-26-000086:facts:RestrictedCashCurrent:2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_total_cash_decrease", "what_changed": "Total cash, cash equivalents and restricted cash decreased by 3310000000 over 2025-09-29..2026-06-28, against a decrease of 78000000 a year earlier. Investing used 1648000000 (against 329000000) and financing used 10046000000 (against 9760000000).", "account": "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect", "expected_direction": "down", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "\"value\": \"-3310000000\"", "paragraph_id": "0000804328-26-000086:facts:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases", "what_changed": "Repurchases and retirements of common stock are 6806000000 for 2025-09-29..2026-06-28, against 6347000000 a year earlier. The first half showed 5442000000 (0000804328-26-000061). Shares outstanding are 1057000000 at 2026-06-28 against 1074000000 at 2025-09-28.", "account": "PaymentsForRepurchaseOfCommonStock", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"6806000000\"", "paragraph_id": "0000804328-26-000086:facts:PaymentsForRepurchaseOfCommonStock:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_remaining_repurchase_authorization", "what_changed": "Remaining authorised repurchase amount across programs is 20600000000 at 2026-06-28, against 21900000000 at 2026-03-29 (0000804328-26-000061).", "account": "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1", "expected_direction": "down", "horizon": "next four quarters", "quote": "\"value\": \"20600000000\"", "paragraph_id": "0000804328-26-000086:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-06-28:srt:ShareRepurchaseProgramAxis=qcom:StockRepurchaseProgramsAuthorizedAndRemainingMember" }
```

```json
{ "id": "liquidity_and_capital_dividends_paid", "what_changed": "Dividends paid are 2868000000 for 2025-09-29..2026-06-28, against 2848000000 a year earlier. Dividends declared per share are 0.92 this quarter against 0.89.", "account": "PaymentsOfOrdinaryDividends", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "\"value\": \"2868000000\"", "paragraph_id": "0000804328-26-000086:facts:PaymentsOfOrdinaryDividends:2025-09-29..2026-06-28" }
```

```json
{ "id": "liquidity_and_capital_interest_rate_swap_notional_higher", "what_changed": "Interest-rate swap notional is 5000000000.0 at 2026-06-28, against 3600000000 at 2025-09-28. The 10-Q filed 2026-04-29 showed 5000000000.0 at 2026-03-29.", "account": "DerivativeNotionalAmount, interest rate swaps", "expected_direction": "up", "horizon": "next four quarters", "quote": "\"value\": \"5000000000.0\"", "paragraph_id": "0000804328-26-000086:facts:DerivativeNotionalAmount:2026-06-28:us-gaap:DerivativeInstrumentRiskAxis=us-gaap:InterestRateSwapMember" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_growth_from_acquisitions", "what_changed": "Goodwill is 14274000000 at 2026-06-28, against 11358000000 at 2025-09-28. Other intangible assets, net, are 1510000000 against 1148000000. Alphawave goodwill (2210000000 in this filing) and the other fiscal 2026 acquisitions (737000000, next item) are tagged in the same filing.", "account": "Goodwill", "expected_direction": "up", "horizon": "fiscal year 2026 (ending 2026-09-27), annual impairment test", "quote": "\"value\": \"14274000000\"", "paragraph_id": "0000804328-26-000086:facts:Goodwill:2026-06-28" }
```

```json
{ "id": "structure_and_disclosure_changes_other_acquisitions_goodwill", "what_changed": "Goodwill from the other fiscal 2026 business acquisitions is 737000000 at 2026-06-28, for 7 businesses with payments of 1100000000. At 2026-03-29 the 10-Q filed 2026-04-29 showed 698000000 for 6 businesses with payments of 985000000. By segment it is QCT 661000000 and Data Center 76000000. Intangibles acquired are 295000000 against 272000000.", "account": "Goodwill, other fiscal 2026 acquisitions", "expected_direction": "up", "horizon": "until purchase-price allocations are final; my input does not state when", "quote": "\"value\": \"737000000\"", "paragraph_id": "0000804328-26-000086:facts:Goodwill:2026-06-28:us-gaap:BusinessAcquisitionAxis=qcom:A2026OtherBusinessAcquisitionsMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_modular_acquisition_after_quarter_end", "what_changed": "Subsequent event on 2026-07-28: the 10-Q tags consideration transferred for Modular of 3100000000, with 18000000 shares issued or issuable. Of those, 4000000 are executive shares subject to service requirements, valued at 700000000. The 8-K headline says the company 'Completed Acquisition of Modular Inc'. None of this is in the 2026-06-28 balance sheet.", "account": "BusinessCombinationConsiderationTransferred1, Modular (subsequent event)", "expected_direction": "up", "horizon": "next quarter (fiscal fourth quarter 2026, first balance sheet including Modular)", "quote": "\"value\": \"3100000000\"", "paragraph_id": "0000804328-26-000086:facts:BusinessCombinationConsiderationTransferred1:2026-07-28..2026-07-28:us-gaap:BusinessAcquisitionAxis=qcom:ModularMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "across_documents_input_cost_pressure_beside_lowest_gross_margin", "what_changed": "The 8-K business outlook describes a broad-based rise in input costs, says pricing actions are expected to benefit gross margins 'over time', and states these factors are reflected in both third-quarter performance and fourth-quarter guidance. On the numbers, quarterly gross margin is the lowest of 6 filled quarters (0.5305117120739922), annual gross margin is the lowest of 5 filled years, and inventory is at its highest days level of 6 filled quarters. The paragraph gives no figure for the cost increase or the timing of the pricing benefit.", "account": "Gross margin; CostOfRevenue", "expected_direction": "none", "horizon": "next two quarters (through fiscal first quarter 2027)", "quote": "The semiconductor industry is experiencing a broad-based increase in input costs, across wafer fabrication, assembly, test, advanced packaging, memory and other materials.", "paragraph_id": "0000804328-26-000085:8k_2_02:29" }
```

```json
{ "id": "across_documents_revenue_at_high_end_of_guidance_claim", "what_changed": "The CEO quote says quarterly revenues were at the high end of guidance. The prior quarter's guidance range is not in my input, so I cannot check the claim against a range. The filed figure is revenue of 9947000000 against 10365000000 a year earlier, a decline the 8-K prints as (4%).", "account": "Revenues", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "our third quarter results reflect solid execution of our growth strategy, with quarterly revenues at the high end of guidance", "paragraph_id": "0000804328-26-000085:8k_2_02:16" }
```

```json
{ "id": "results_against_expectations_revenue_guidance_range", "what_changed": "The 8-K guides revenue of $9.7B - $10.5B for the next quarter, with QCT $8.4B - $9.0B and QTL $1.2B - $1.4B. For comparison, this quarter's revenue is 9947000000. The outlook excludes items such as investment gains that 'cannot be accurately forecast'.", "account": "Revenues (guidance)", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "Revenues |  | $9.7B - $10.5B", "paragraph_id": "0000804328-26-000085:8k_2_02:31" }
```

```json
{ "id": "results_against_expectations_gaap_eps_guidance_range", "what_changed": "The 8-K guides GAAP diluted EPS of $1.22 - $1.42 and Non-GAAP diluted EPS of $2.05 - $2.25 for the next quarter. The reconciling items are share-based compensation ($0.72) and other items ($0.11), the latter 'primarily related to acquisition-related items'. This quarter's GAAP diluted EPS is 1.87.", "account": "EarningsPerShareDiluted (guidance)", "expected_direction": "down", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "GAAP diluted EPS |  | $1.22 - $1.42", "paragraph_id": "0000804328-26-000085:8k_2_02:31" }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_fixed_tax_rate_method", "what_changed": "Method change in the non-GAAP measures. From the first quarter of fiscal 2026 the company applies a fixed estimated Non-GAAP tax rate, set annually and re-evaluated periodically, and prior periods were not updated because 'the effect would not be material'. Non-GAAP comparisons across the fiscal 2025/2026 boundary therefore mix two tax methods. The GAAP effective tax rate swung from -2.30 in the March quarter to 0.19 in the June quarter.", "account": "Non-GAAP provision for income taxes", "expected_direction": "none", "horizon": "fiscal year 2026 (ending 2026-09-27)", "quote": "Beginning in the first quarter of fiscal 2026, we are applying a fixed estimated Non-GAAP tax rate to determine our Non-GAAP provision for income taxes.", "paragraph_id": "0000804328-26-000085:8k_2_02:71" }
```

```json
{ "id": "across_documents_capital_return_in_latest_quarter", "what_changed": "The 8-K states the third-quarter capital return as $2.3 billion: $973 million of dividends ($0.92 per share) and $1.4 billion of repurchases of 8 million shares. This matches the 10-Q's dividend per share of 0.92. The 10-Q's repurchase payments are year-to-date (6806000000); the quarter's share is not tagged separately in my input.", "account": "Dividends and share repurchases", "expected_direction": "none", "horizon": "next quarter (fiscal fourth quarter 2026, ending 2026-09-27)", "quote": "we returned $2.3 billion to stockholders, including $973 million, or $0.92 per share, of cash dividends paid and $1.4 billion through repurchases of 8 million shares of common stock", "paragraph_id": "0000804328-26-000085:8k_2_02:27" }
```

## Seen in the notes

No items. My instructions say each numeric fact is marked with whether its element sat inside a note when it was extracted. No fact in input_numbers.json carries that marker. Each fact row holds only:

- id, paragraph_id, tag, prefix, namespace
- context, context_ref, unit, decimals
- value, number, nil
- form, source_accession, filing_date
- superseded_by, where present

I was told not to judge note membership myself, and the marker that would decide it is absent. So every fact-based item sits under the heading above, and none is placed here. Several of them are of a kind a filing commonly states in a note, for example:

- inventory components
- the valuation-allowance change and the tax-rate forecasts
- segment and product revenues
- customer concentration
- acquisitions, goodwill by acquisition and the Modular subsequent event
- swap notionals

They are not placed here because this input cannot say which ones sat in a note. The split the later version needs cannot be made from this run's input. This is a broken marker, not an empty finding.
