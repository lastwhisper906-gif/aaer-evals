<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# FLEX — 10-Q 0000866374-26-000030 (quarter ended 2026-06-26) — numbers reader

Conventions. `expected_direction` records the sign of the change Python printed for the quoted row (a negative printed change is `down`, a positive one `up`); where Python printed no change, or the cell is unfilled, it is `none`. It is not a forecast. `horizon` names the comparison window the item rests on. Every number below is copied from the input as printed; none is computed here.

What the input does not hold, stated once and outside the items:

- **quarters-back-1 (target end 2026-03-27) has no cells.** Its reason, as printed: "no quarter ending within 20 days of 2026-03-27 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". No fourth-quarter derivation is in my directory, so that quarter stays empty, and every quarter-over-quarter change for quarters-back-0 is unavailable.
- **No articulation checks, restatement traces or fourth-quarter derivation are in my directory.** My directory holds only input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. So there are no articulation-gap items and no restatement-trace items. Restated values are covered only as far as the numeric facts themselves show them (see the end of the first section).
- **The research-and-development capitalization baseline under each year is unfilled in all five years**, and that block prints no `paragraph_id`, so it cannot be quoted. The reasons it gives: there is no `ResearchAndDevelopmentExpense` row for any year from 2021-04-01 on, and the record tags no `us-gaap:CapitalizedComputerSoftwareAdditions` in any period.
- **The 8-K item-code list and the late-filing list carry no paragraph ids**, so I do not quote them. The late-filing list says "none on or before 2026-07-31".
- **Prior predictions:** none on record.
- **Nothing outside my remit is in the directory** (no prices, returns, short interest, other companies' files, prior probabilities or outcome window).

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-01..2026-06-26)

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cell", "what_changed": "Accruals over total assets is 0.0003571712040638146 (net income 285000000 tagged ProfitLoss, operating cash flow 276000000, assets 25198000000). No quarter-over-quarter change: quarters-back-1 is not filled. No year-over-year change: net income rests on us-gaap:ProfitLoss here and on us-gaap:NetIncomeLoss in quarters-back-4, so Python did not compare them. Position: the only filled quarter on the same concepts. insufficient: one comparable quarter supports no trend claim. In quarters-back-2, -3, -5, -6 and -7 the ratio is unfilled for lack of a discrete-quarter operating cash flow (separate item below).", "account": "accruals: net income less operating cash flow, over total assets", "expected_direction": "none", "horizon": "quarter ended 2026-06-26; no comparable quarter on record", "quote": "\"position_in_history\": \"the only filled quarter on the same concepts; 1 other filled quarter rests on a different concept and is not compared\"", "paragraph_id": "0000866374-26-000030:trends:accruals_over_total_assets:2026-04-01..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_cell", "what_changed": "Bad-debt reserve ratio is 0.0019817677368212444 (allowance 10000000 against receivables 5036000000). Year-over-year change against quarters-back-4: -0.00030656178262955655. No quarter-over-quarter change: quarters-back-1 is not filled. Position: second lowest of the 7 filled quarters.", "account": "allowance for doubtful accounts over gross receivables", "expected_direction": "down", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"second lowest of the 7 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-26" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_cell", "what_changed": "Contract liabilities over revenue is 0.05562563067608476 (ContractWithCustomerLiability 441000000 against revenue 7928000000). Year-over-year change against quarters-back-4: -0.012815433962698512. No quarter-over-quarter change: quarters-back-1 is not filled. Position: second lowest of the 7 filled quarters.", "account": "contract liabilities (ContractWithCustomerLiability) over revenue", "expected_direction": "down", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"second lowest of the 7 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-26" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_cell", "what_changed": "Days sales of inventory is 78.22363104361153 (InventoryNet 6453000000, CostOfGoodsAndServicesSold 7177000000, 87-day quarter). Year-over-year change against quarters-back-4: 1.6737730178891326. No quarter-over-quarter change: quarters-back-1 is not filled. Position: third lowest of the 6 filled quarters.", "account": "inventory over cost of revenue, in days", "expected_direction": "up", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:days_sales_of_inventory:2026-04-01..2026-06-26" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_cell", "what_changed": "Days sales outstanding is 55.263874873864786 (AccountsReceivableNetCurrent 5036000000 against revenue 7928000000, 87-day quarter). Year-over-year change against quarters-back-4: 2.7449395126480525. No quarter-over-quarter change: quarters-back-1 is not filled. Position: highest of the 7 filled quarters.", "account": "accounts receivable over revenue, in days", "expected_direction": "up", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"highest of the 7 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:days_sales_outstanding:2026-04-01..2026-06-26" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_cell", "what_changed": "Gross margin is 0.09472754793138244 (revenue 7928000000, CostOfGoodsAndServicesSold 7177000000). Year-over-year change against quarters-back-4: 0.0052978901367056325. No quarter-over-quarter change: quarters-back-1 is not filled. Position: second highest of the 6 filled quarters.", "account": "gross margin", "expected_direction": "up", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:gross_margin:2026-04-01..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_cell", "what_changed": "insufficient. The inventory reserve ratio is unfilled: the record tags no us-gaap:InventoryValuationReserves in any period. The same reason prints in every quarter and every year the table holds, so the ratio has no history at all.", "account": "inventory valuation reserve over inventory", "expected_direction": "none", "horizon": "quarter ended 2026-06-26; no period on record", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment \\u2014 the filing says which, and this record cannot\"", "paragraph_id": "0000866374-26-000030:trends:inventory_reserve_ratio:2026-04-01..2026-06-26" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell", "what_changed": "insufficient. The non-GAAP gap is unfilled: no us-gaap concept carries a non-GAAP measure. The same reason prints in every quarter and year the table holds. The 8-K release prints a non-GAAP net income, but the table holds no gap and none is derived here.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "quarter ended 2026-06-26; no period on record", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000866374-26-000030:trends:non_gaap_gap:2026-04-01..2026-06-26" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_cell", "what_changed": "Receivables over revenue is 0.6352169525731585 (AccountsReceivableNetCurrent 5036000000 against revenue 7928000000). Year-over-year change against quarters-back-4: 0.0384108689229683. No quarter-over-quarter change: quarters-back-1 is not filled. Position: highest of the 7 filled quarters.", "account": "accounts receivable over quarterly revenue", "expected_direction": "up", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"highest of the 7 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:receivables_over_revenue:2026-04-01..2026-06-26" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_cell", "what_changed": "Soft-asset share is 0.781927137074371 (assets 25198000000, PropertyPlantAndEquipmentNet 2655000000, cash 2840000000). Year-over-year change against quarters-back-4: 0.020689420160300287. No quarter-over-quarter change: quarters-back-1 is not filled. Position: highest of the 7 filled quarters.", "account": "assets other than PP&E and cash, over total assets", "expected_direction": "up", "horizon": "year over year: quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"position_in_history\": \"highest of the 7 filled quarters\"", "paragraph_id": "0000866374-26-000030:trends:soft_asset_share:2026-04-01..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_cell", "what_changed": "insufficient. The warranty reserve ratio is unfilled: the record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. The same reason prints in every quarter and every year the table holds.", "account": "warranty accrual", "expected_direction": "none", "horizon": "quarter ended 2026-06-26; no period on record", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment \\u2014 the filing says which, and this record cannot\"", "paragraph_id": "0000866374-26-000030:trends:warranty_reserve_ratio:2026-04-01..2026-06-26" }
```

### Trend table — years-back-0 (2025-04-01..2026-03-31)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_cell", "what_changed": "Accruals over total assets for the fiscal year is -0.036491387126019945 (NetIncomeLoss 880000000, operating cash flow 1685000000, assets 22060000000). Year-over-year change against years-back-1: -0.0002039163681721648. Position: lowest of the 5 filled years.", "account": "accruals: net income less operating cash flow, over total assets", "expected_direction": "down", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:accruals_over_total_assets:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_cell", "what_changed": "Bad-debt reserve ratio at fiscal year end is 0.0017068487305312568 (allowance 8000000 against receivables 4679000000). Year-over-year change against years-back-1: -0.00019635953483035287. Position: lowest of the 5 filled years.", "account": "allowance for doubtful accounts over gross receivables", "expected_direction": "down", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:bad_debt_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_cell", "what_changed": "Contract liabilities over revenue is 0.015440280862649567 (ContractWithCustomerLiability 431000000 against revenue 27914000000). Year-over-year change against years-back-1: 0.0008352368925569776. Position: second lowest of the 4 filled years on the same concepts; the fifth year rests on a different concept (tag change, separate item).", "account": "contract liabilities over annual revenue", "expected_direction": "up", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"", "paragraph_id": "0000866374-26-000030:trends:contract_liabilities_over_revenue:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_cell", "what_changed": "Days sales of inventory for the fiscal year is 84.36511388801011 (InventoryNet 5845000000, CostOfGoodsAndServicesSold 25288000000, 365 days). Year-over-year change against years-back-1: 5.883304186517577. Position: second lowest of the 5 filled years.", "account": "inventory over cost of revenue, in days", "expected_direction": "up", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:days_sales_of_inventory:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_cell", "what_changed": "Days sales outstanding for the fiscal year is 61.18202335745504 (AccountsReceivableNetCurrent 4679000000 against revenue 27914000000, 365 days). Year-over-year change against years-back-1: 9.273488898074106. Position: highest of the 5 filled years.", "account": "accounts receivable over revenue, in days", "expected_direction": "up", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:days_sales_outstanding:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_cell", "what_changed": "Gross margin for the fiscal year is 0.09407465787776743 (revenue 27914000000, CostOfGoodsAndServicesSold 25288000000). Year-over-year change against years-back-1: 0.007722819656716021. Position: highest of the 5 filled years.", "account": "gross margin", "expected_direction": "up", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:gross_margin:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_cell", "what_changed": "insufficient. The inventory reserve ratio for the fiscal year is unfilled: the record tags no us-gaap:InventoryValuationReserves in any period.", "account": "inventory valuation reserve over inventory", "expected_direction": "none", "horizon": "fiscal year ended 2026-03-31; no period on record", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment \\u2014 the filing says which, and this record cannot\"", "paragraph_id": "0000866374-26-000030:trends:inventory_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell", "what_changed": "insufficient. The non-GAAP gap for the fiscal year is unfilled: no us-gaap concept carries a non-GAAP measure.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "fiscal year ended 2026-03-31; no period on record", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000866374-26-000030:trends:non_gaap_gap:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_cell", "what_changed": "Receivables over revenue for the fiscal year is 0.16762198180124668 (AccountsReceivableNetCurrent 4679000000 against revenue 27914000000). Year-over-year change against years-back-1: 0.025406818898833172. Position: highest of the 5 filled years.", "account": "accounts receivable over annual revenue", "expected_direction": "up", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:receivables_over_revenue:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_cell", "what_changed": "Soft-asset share at fiscal year end is 0.7781504986400726 (assets 22060000000, PropertyPlantAndEquipmentNet 2505000000, cash 2389000000). Year-over-year change against years-back-1: 0.02944259373827185. Position: highest of the 5 filled years.", "account": "assets other than PP&E and cash, over total assets", "expected_direction": "up", "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000866374-26-000030:trends:soft_asset_share:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_cell", "what_changed": "insufficient. The warranty reserve ratio for the fiscal year is unfilled: the record tags no product-warranty accrual concept in any period.", "account": "warranty accrual", "expected_direction": "none", "horizon": "fiscal year ended 2026-03-31; no period on record", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment \\u2014 the filing says which, and this record cannot\"", "paragraph_id": "0000866374-26-000030:trends:warranty_reserve_ratio:2025-04-01..2026-03-31" }
```

### Trend table — cells unfilled in earlier quarters the table holds

```json
{ "id": "earnings_quality_accruals_unfilled_without_discrete_quarter_cash_flow", "what_changed": "insufficient. Accruals over total assets is unfilled in quarters-back-2, -3, -5, -6 and -7, each time because operating cash flow is in the record but not for that discrete quarter. Only quarters-back-0 and quarters-back-4 are filled, and they rest on different net-income tags, so no quarterly accrual history exists.", "account": "operating cash flow by discrete quarter", "expected_direction": "none", "horizon": "quarters-back-2 through quarters-back-7", "quote": "\"missing\": \"no row for operating_cash_flow in 2025-09-27..2025-12-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0000866374-26-000030:trends:accruals_over_total_assets:2025-09-27..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_unfilled_without_cost_of_revenue", "what_changed": "insufficient. Gross margin is unfilled in quarters-back-5 (2025-01-01..2025-03-31): cost of revenue is in the record but not for that period. This is why gross margin and days sales of inventory count 6 filled quarters, not 7.", "account": "cost of revenue for the quarter ended 2025-03-31", "expected_direction": "none", "horizon": "quarters-back-5", "quote": "\"missing\": \"no row for cost_of_revenue in 2025-01-01..2025-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0000866374-26-000030:trends:gross_margin:2025-01-01..2025-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_unfilled_without_cost_of_revenue", "what_changed": "insufficient. Days sales of inventory is unfilled in quarters-back-5 (2025-01-01..2025-03-31) for the same missing cost of revenue.", "account": "cost of revenue for the quarter ended 2025-03-31", "expected_direction": "none", "horizon": "quarters-back-5", "quote": "\"missing\": \"no row for cost_of_revenue in 2025-01-01..2025-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0000866374-26-000030:trends:days_sales_of_inventory:2025-01-01..2025-03-31" }
```

### Changes of tag

```json
{ "id": "structure_and_disclosure_changes_net_income_tag_profit_loss_against_net_income_loss", "what_changed": "Net income in the accruals formula rests on us-gaap:ProfitLoss for the quarter ended 2026-06-26 and on us-gaap:NetIncomeLoss for the quarter ended 2025-06-27, so Python printed no year-over-year accrual change. The annual cells use NetIncomeLoss.", "account": "net income tag", "expected_direction": "none", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "\"reason\": \"accruals_over_total_assets rests on a different concept in each period, so the difference would not be a change \\u2014 net_income: us-gaap:ProfitLoss in quarters-back-0 and us-gaap:NetIncomeLoss in quarters-back-4\"", "paragraph_id": "0000866374-26-000030:trends:accruals_over_total_assets:2026-04-01..2026-06-26" }
```

```json
{ "id": "structure_and_disclosure_changes_net_income_tag_prior_year_quarter_side", "what_changed": "The other side of the same net-income tag change: the quarter ended 2025-06-27 (accruals -0.010819569307965711 on NetIncomeLoss 192000000) is the only filled quarter on its concepts, so it is not compared with the current quarter.", "account": "net income tag", "expected_direction": "none", "horizon": "quarter ended 2025-06-27", "quote": "\"position_in_history\": \"the only filled quarter on the same concepts; 1 other filled quarter rests on a different concept and is not compared\"", "paragraph_id": "0000866374-26-000030:trends:accruals_over_total_assets:2025-04-01..2025-06-27" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_liabilities_tag_current_portion", "what_changed": "Contract liabilities rest on us-gaap:ContractWithCustomerLiability in years-back-3 (and in years-back-0 through -2), but on us-gaap:ContractWithCustomerLiabilityCurrent in years-back-4, so Python printed no change between those two years.", "account": "contract liabilities tag", "expected_direction": "none", "horizon": "fiscal year ended 2023-03-31 against fiscal year ended 2022-03-31", "quote": "\"reason\": \"contract_liabilities_over_revenue rests on a different concept in each period, so the difference would not be a change \\u2014 contract_liabilities: us-gaap:ContractWithCustomerLiability in years-back-3 and us-gaap:ContractWithCustomerLiabilityCurrent in years-back-4\"", "paragraph_id": "0000866374-26-000030:trends:contract_liabilities_over_revenue:2022-04-01..2023-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_liabilities_tag_oldest_year_side", "what_changed": "The other side of the same contract-liabilities tag change: the fiscal year ended 2022-03-31 (ContractWithCustomerLiabilityCurrent 615000000, ratio 0.02496650834246742) is alone on its concept.", "account": "contract liabilities tag", "expected_direction": "none", "horizon": "fiscal year ended 2022-03-31", "quote": "\"position_in_history\": \"the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared\"", "paragraph_id": "0000866374-26-000030:trends:contract_liabilities_over_revenue:2021-04-01..2022-03-31" }
```

### 8-K earnings release figures (0000866374-26-000026, filed 2026-07-29)

```json
{ "id": "results_against_expectations_release_net_sales_growth", "what_changed": "The release prints quarterly net sales of $7.9 billion, up 21% against the prior year (Schedule I: 7,928 against 6,575, in millions).", "account": "net sales", "expected_direction": "up", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "•Reported Q1 net sales of $7.9 billion, up 21% versus the prior year.", "paragraph_id": "0000866374-26-000026:8k_2_02:5" }
```

```json
{ "id": "results_against_expectations_release_updated_full_year_sales_guidance", "what_changed": "Fiscal 2027 net sales guidance is printed as $33.7 billion to $35.2 billion. The release's own table sets this against a prior range of $32.3 - $33.8 billion; adjusted EPS guidance is printed as $4.42 - $4.74 against a prior $4.21 - $4.51.", "account": "full-year net sales guidance", "expected_direction": "up", "horizon": "fiscal year ending March 2027", "quote": "•Net Sales: $33.7 billion to $35.2 billion, growth of 23% at the midpoint", "paragraph_id": "0000866374-26-000026:8k_2_02:31" }
```

```json
{ "id": "structure_and_disclosure_changes_release_guidance_excludes_planned_spin_off", "what_changed": "The full-year guidance does not give effect to the planned spin-off of the Cloud and Power Infrastructure segment.", "account": "segment structure: Cloud and Power Infrastructure", "expected_direction": "none", "horizon": "fiscal year ending March 2027", "quote": "†Reflects expected results for the full fiscal year and does not give effect to the planned spin-off of the Cloud and Power Infrastructure segment", "paragraph_id": "0000866374-26-000026:8k_2_02:38" }
```

```json
{ "id": "liquidity_and_capital_release_free_cash_flow_against_prior_year", "what_changed": "The release prints free cash flow of $41 million for the quarter against $268 million a year earlier. Operating cash flow is 276 against 399 (Schedule IV), and purchases of property and equipment are (236) against (133). Free cash flow is a non-GAAP measure; it is copied from the release, not computed.", "account": "free cash flow (non-GAAP)", "expected_direction": "down", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "During the three month periods ended June 26, 2026 and June 27, 2025, the Company recognized $41 million and $268 million of free cash inflow, respectively.", "paragraph_id": "0000866374-26-000026:8k_2_02:91" }
```

```json
{ "id": "liquidity_and_capital_release_working_capital_outflow", "what_changed": "The release's cash-flow schedule prints changes in working capital and other, net of (149) for the quarter against 65 a year earlier (in millions).", "account": "changes in working capital and other, net", "expected_direction": "down", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "|  | Changes in working capital and other, net | (149) |  |  | 65 |  |", "paragraph_id": "0000866374-26-000026:8k_2_02:65" }
```

```json
{ "id": "liquidity_and_capital_release_acquisition_outflow", "what_changed": "The release prints acquisition of businesses, net of cash acquired, of (1,134) for the quarter against (41) a year earlier (in millions). In the same quarter, proceeds from bank borrowings and long-term debt are 2,830.", "account": "acquisition of businesses, net of cash acquired", "expected_direction": "up", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "|  | Acquisition of businesses, net of cash acquired | (1,134) |  |  | (41) |  |", "paragraph_id": "0000866374-26-000026:8k_2_02:65" }
```

```json
{ "id": "liquidity_and_capital_release_long_term_debt_balance", "what_changed": "The release's balance sheet prints long-term debt, net of current portion, of 5,219 at June 26, 2026 against 3,751 at March 31, 2026 (in millions).", "account": "long-term debt, net of current portion", "expected_direction": "up", "horizon": "June 26, 2026 against March 31, 2026", "quote": "| Long-term debt, net of current portion | 5,219 |  |  | 3,751 |  |", "paragraph_id": "0000866374-26-000026:8k_2_02:62" }
```

```json
{ "id": "estimates_and_discretion_release_goodwill_balance", "what_changed": "The release's balance sheet prints goodwill of 1,831 at June 26, 2026 against 1,369 at March 31, 2026, and other intangible assets, net, of 736 against 283 (in millions). The soft-asset share is highest of the 7 filled quarters in the trend table.", "account": "goodwill", "expected_direction": "up", "horizon": "June 26, 2026 against March 31, 2026", "quote": "| Goodwill | 1,831 |  |  | 1,369 |  |", "paragraph_id": "0000866374-26-000026:8k_2_02:62" }
```

```json
{ "id": "revenue_recognition_release_contract_assets_balance", "what_changed": "The release's balance sheet prints contract assets of 1,386 at June 26, 2026 against 1,063 at March 31, 2026 (in millions). Accounts receivable, net, is 5,036 against 4,679.", "account": "contract assets", "expected_direction": "up", "horizon": "June 26, 2026 against March 31, 2026", "quote": "|  | Contract assets | 1,386 |  |  | 1,063 |  |", "paragraph_id": "0000866374-26-000026:8k_2_02:62" }
```

```json
{ "id": "estimates_and_discretion_release_restructuring_reversal", "what_changed": "The release's statement of operations prints restructuring and impairment charges (reversal) of (2) in operating expenses for the quarter against 7 a year earlier (in millions). Cost-of-sales restructuring charges are 4 against 16.", "account": "restructuring and impairment charges (reversal)", "expected_direction": "down", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "|  | Restructuring and impairment charges (reversal) | (2) |  |  | 7 |  |", "paragraph_id": "0000866374-26-000026:8k_2_02:56" }
```

```json
{ "id": "earnings_quality_release_other_income_includes_divestiture_gain", "what_changed": "Schedule V of the release (its notes to Schedules I and II; prose, not a table) says GAAP results for the quarter include a $46 million gain on the divestiture of a subsidiary, which the release excludes from non-GAAP net income. Schedule I prints other charges (income), net, of (37) against 7.", "account": "other charges (income), net", "expected_direction": "none", "horizon": "quarter ended 2026-06-26", "quote": "the Company recognized a $46 million gain on the divestiture of a subsidiary.", "paragraph_id": "0000866374-26-000026:8k_2_02:87" }
```

```json
{ "id": "earnings_quality_release_legal_and_other_spin_off_costs", "what_changed": "Schedule V (prose) says legal and other charges for the quarter are about $53 million, mostly for the planned spin-off, plus $14 million of acquisition costs. Schedule II prints legal and other of 67 against 6 a year earlier.", "account": "legal and other charges (non-GAAP adjustment)", "expected_direction": "up", "horizon": "quarter ended 2026-06-26 against quarter ended 2025-06-27", "quote": "During the three month period ended June 26, 2026, the Company incurred approximately $53 million primarily related to the planned spin-off of its Cloud and Power Infrastructure segment into a separate publicly traded company as well as $14 million of acquisition costs.", "paragraph_id": "0000866374-26-000026:8k_2_02:83" }
```

```json
{ "id": "estimates_and_discretion_release_normalized_non_gaap_tax_rate", "what_changed": "Schedule V (prose) says that from fiscal 2026 the company uses an annual normalized tax rate to tax-effect its non-GAAP adjustments, a method change for the non-GAAP figures.", "account": "tax effect of non-GAAP adjustments", "expected_direction": "none", "horizon": "fiscal 2026 onward", "quote": "Effective in fiscal year 2026, the Company adopted an annual normalized tax rate for the purpose of determining the tax effect of non-GAAP adjustments.", "paragraph_id": "0000866374-26-000026:8k_2_02:88" }
```

### Numeric facts and restated prior values

There is no restatement trace to read, so no restated prior value can be reported as such: insufficient. The numeric facts mark a fact a later filing re-reported with a `superseded_by` field. For the re-reported 2025-03-31 balances whose later value the trend inputs also print, the two printed values are the same string:

- cash 2289000000 (10-Q 0000866374-26-000005 against 10-K 0000866374-26-000012)
- accounts receivable 3671000000
- inventory 5071000000
- property, plant and equipment 2330000000
- assets 18381000000
- stockholders' equity 5002000000 (against 10-Q 0000866374-26-000030)

None of these is a restated value. A full comparison across every superseded fact belongs to the restatement trace, which is absent.

None of the facts I read prints a note marker. So the restructuring-reserve rollforward below is reported here, under its own fact, with that caveat; I do not judge where it sits.

```json
{ "id": "estimates_and_discretion_severance_restructuring_reserve_rollforward", "what_changed": "The employee-severance restructuring reserve is 42000000 at 2026-06-26. The same 10-Q prints 63000000 at 2026-03-31, restructuring charges of 1000000, payments of 22000000 and an accrual adjustment of 0 for the quarter (all on RestructuringCostAndReserveAxis=EmployeeSeveranceMember). The current portion is 42000000 and the noncurrent portion 0. The fact carries no note marker.", "account": "restructuring reserve, employee severance", "expected_direction": "down", "horizon": "2026-06-26 against 2026-03-31", "quote": "\"value\": \"42000000\"", "paragraph_id": "0000866374-26-000030:facts:RestructuringReserve:2026-06-26:us-gaap:RestructuringCostAndReserveAxis=us-gaap:EmployeeSeveranceMember" }
```

```json
{ "id": "liquidity_and_capital_severance_restructuring_payments", "what_changed": "Payments against the employee-severance restructuring reserve are 22000000 for the quarter ended 2026-06-26, against new restructuring charges of 1000000 to that reserve. The fact carries no note marker.", "account": "payments for restructuring, employee severance", "expected_direction": "none", "horizon": "quarter ended 2026-06-26", "quote": "\"value\": \"22000000\"", "paragraph_id": "0000866374-26-000030:facts:PaymentsForRestructuring:2026-04-01..2026-06-26:us-gaap:RestructuringCostAndReserveAxis=us-gaap:EmployeeSeveranceMember" }
```

## Seen in the notes

No items. Each fact in input_numbers.json prints these fields: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date` and, on some, `superseded_by`. None of them says whether the element sat inside a note. Without that marker, nothing can be placed here without my own judgment of where a table sat, and the instructions do not ask for that judgment. Dimensional facts that may come from note tables, such as the restructuring-reserve rollforward, are reported in the first section, each flagged as carrying no note marker.
