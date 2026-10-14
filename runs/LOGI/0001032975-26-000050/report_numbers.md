<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
## Seen in the statements

Run: LOGI, triggering filing 0001032975-26-000050 (10-Q for the quarter ended 2026-06-30, filed 2026-07-29), cutoff 2026-07-29. Nothing in my directory is a price, return, short-interest figure, outcome window or another company's file. The prior-predictions file says: "None on record."

Conventions used in every item. `expected_direction` is the direction my input itself points. For a trend cell, it is the sign of the change Python printed. For a fact pair, it is the order of the two printed values. For a release sentence, it is the direction of the company's own stated figures. It is "none" where no change or figure is printed. `horizon` names the two periods the printed comparison spans, or the forward window the company names. I did no arithmetic. Every number below is copied as printed.

What my input does not hold, said once here because there is nothing to quote:
- No articulation checks, no restatement traces and no fourth-quarter derivation are in my directory. So no articulation gap, restated prior value or derived fourth quarter can be reported. I did not build any of them myself. The trend table takes some prior-period inputs from later filings. For example, the quarter ended 2025-06-30's revenue and net income come from 0001032975-26-000050, not the original 10-Q. The table prints no flag that any such value differs from what an earlier filing reported.
- Change of tag: no cell in the trend table says a period rests on a different concept. Every filled cell uses the same concepts in every period: RevenueFromContractWithCustomerExcludingAssessedTax, AccountsReceivableNetCurrent, ContractWithCustomerLiabilityCurrent, StandardProductWarrantyAccrual, NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets, CashAndCashEquivalentsAtCarryingValue and PropertyPlantAndEquipmentNet. No tag-change item exists.
- Periods the record does not reach: quarters-back-1 (target 2026-03-31) and quarters-back-5 (target 2025-04-01) have no cells. The reason each prints is: "no quarter ending within 20 days of 2026-03-31 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The quarters-back-5 reason is identical, with 2025-04-01. The derivation's output is not in my input. As a result, every quarter-over-quarter change for quarters-back-0 does not exist.
- The trend table's research-and-development capitalization baseline prints values with no paragraph_id. These include book_value_with_rnd_capitalized and earnings_with_rnd_capitalized. Its capitalized_development_cost is missing: the record "tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period". With nothing to quote it under, I write no item on it.
- The 8-K file's item-code index and late-filing list carry no paragraph id, so I write no item from them. They list an item 3.01 filing on 2025-10-02, an item 4.02 filing on 2014-09-04, an item 4.01 filing on 2014-11-13, and four NT 10-K/10-Q notices from 2014 to 2015.
- Coverage: input_numbers.json is 57,288 lines and would not fit in my context whole. I read:
  - the document list and the first fact rows;
  - the current 10-Q's facts at lines 45536–48830, 49400–49700, 50600–52900, 54400–54660 and 55290–57288;
  - spot samples from the prior 10-Q (0001032975-26-000011) and 10-K (0001032975-26-000021) regions.

  Unread: lines 48830–49400, 49700–50600, 52900–54400 and 54660–55290 of the current 10-Q, and most of the prior 10-Q and 10-K fact rows.

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "accruals_over_total_assets for the quarter ended 2026-06-30 is 0.017101608427231588 (formula (net_income - operating_cash_flow) / assets; printed inputs: net income 235697000, operating cash flow 166708000, assets 4034065000). Year-over-year change against quarters-back-4 is 0.011499095124268133. There is no quarter-over-quarter change: 'accruals_over_total_assets is not filled in quarters-back-1'. Position: highest of the 2 filled quarters. Only two quarters are filled, because quarters-back-2, -3, -6 and -7 have no operating-cash-flow row. That is insufficient for a trend claim.",
  "account": "accruals (net income less operating cash flow) over total assets",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"",
  "paragraph_id": "0001032975-26-000050:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. bad_debt_reserve_ratio is not filled for the quarter ended 2026-06-30, and neither change exists. The cell gives the reason quoted. The current 10-Q's facts do carry AllowanceForDoubtfulAccountsReceivableCurrent at 2026-06-30, but only split by allowance type (cooperative marketing, customer incentive programs, pricing programs, other). No entity-wide row exists, which matches the reason. See the notes items.",
  "account": "allowance for doubtful accounts over receivables",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30; no comparison exists",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001032975-26-000050:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "contract_liabilities_over_revenue for the quarter ended 2026-06-30 is 0.03365780283140787 (printed inputs: ContractWithCustomerLiabilityCurrent 41306000, quarterly revenue 1227234000). Year-over-year change against quarters-back-4 is 0.007720779054350563. There is no quarter-over-quarter change (not filled in quarters-back-1). Position: highest of the 6 filled quarters. The ratio uses the current contract liability only.",
  "account": "current contract liabilities over revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001032975-26-000050:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_insufficient",
  "what_changed": "insufficient. days_sales_of_inventory is not filled for the quarter ended 2026-06-30 because no cost-of-revenue row exists (reason quoted). The ratio is filled in no period of the table (0 of 13). The current 10-Q's income-statement facts go from revenue to GrossProfit with no cost-of-goods-sold fact in my input.",
  "account": "inventory over cost of revenue (days)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30; no comparison exists",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2026-04-01..2026-06-30: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001032975-26-000050:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "days_sales_outstanding for the quarter ended 2026-06-30 is 49.5693787818786 (formula receivables / revenue * days_in_period; printed inputs: AccountsReceivableNetCurrent 668497000, revenue 1227234000, 91 days). Year-over-year change against quarters-back-4 is -0.8997695953583715. There is no quarter-over-quarter change (not filled in quarters-back-1). Position: third lowest of the 6 filled quarters.",
  "account": "accounts receivable, net (days sales outstanding)",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001032975-26-000050:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_insufficient",
  "what_changed": "insufficient. gross_margin is not filled for the quarter ended 2026-06-30 because no cost-of-revenue row exists (reason quoted). It is filled in no period of the table (0 of 13). The company itself prints a gross margin in the 8-K; see the across-documents item. No trend-table value exists to set it against.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30; no comparison exists",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2026-04-01..2026-06-30: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001032975-26-000050:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled for the quarter ended 2026-06-30. The record tags no InventoryValuationReserves in any period (reason quoted). The current 10-Q's inventory facts I read are tagged net of reserves (InventoryRawMaterialsNetOfReserves, InventoryFinishedGoodsNetOfReserves), with no reserve amount among them.",
  "account": "inventory valuation reserve over inventory",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30; no comparison exists",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001032975-26-000050:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient. non_gaap_gap is not filled for the quarter ended 2026-06-30 because no us-gaap concept carries a non-GAAP measure (reason quoted). The 8-K prints 'Net income - Non-GAAP' 269,007 against 'Net income - GAAP' 235,697 (in thousands) for the quarter. Python computed no gap from them, and I compute none.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30; no comparison exists",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001032975-26-000050:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "receivables_over_revenue for the quarter ended 2026-06-30 is 0.544718448152512 (printed inputs: receivables 668497000, revenue 1227234000). Year-over-year change against quarters-back-4 is -0.009887577970971173. There is no quarter-over-quarter change (not filled in quarters-back-1). Position: third lowest of the 6 filled quarters.",
  "account": "accounts receivable, net over revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001032975-26-000050:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "soft_asset_share for the quarter ended 2026-06-30 is 0.5382573161314952 (formula (assets - property_plant_and_equipment - cash) / assets; printed inputs: assets 4034065000, PP&E 113021000, cash 1749679000). Year-over-year change against quarters-back-4 is -0.033225223236379886. There is no quarter-over-quarter change (not filled in quarters-back-1). Position: second lowest of the 6 filled quarters.",
  "account": "soft assets over total assets",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001032975-26-000050:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
  "what_changed": "warranty_reserve_ratio for the quarter ended 2026-06-30 is 0.04015452635764655 (printed inputs: StandardProductWarrantyAccrual 49279000, quarterly revenue 1227234000). Year-over-year change against quarters-back-4 is -0.0035902403633605445. There is no quarter-over-quarter change (not filled in quarters-back-1). Position: third lowest of the 6 filled quarters.",
  "account": "product warranty accrual over revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001032975-26-000050:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "accruals_over_total_assets for the year ended 2026-03-31 is -0.08471158773035721 (printed inputs: net income 711187000, operating cash flow 1037207000, assets 3848588000). Year-over-year change against years-back-1 is -0.02507395555585635. An annual period has no quarter-over-quarter change. Position: second lowest of the 5 filled years.",
  "account": "accruals (net income less operating cash flow) over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001032975-26-000050:trends:accruals_over_total_assets:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. bad_debt_reserve_ratio is not filled for the year ended 2026-03-31, and no change exists. It is filled in no period of the table (0 of 13). The cell gives the reason quoted.",
  "account": "allowance for doubtful accounts over receivables",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-03-31; no comparison exists",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-03-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001032975-26-000050:trends:bad_debt_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "contract_liabilities_over_revenue for the year ended 2026-03-31 is 0.00798469496841509 (printed inputs: ContractWithCustomerLiabilityCurrent 38652000, annual revenue 4840761000). Year-over-year change against years-back-1 is 0.0023209043253713353. Position: highest of the 4 filled years. years-back-4 has no contract-liabilities row, so only four years are filled.",
  "account": "current contract liabilities over revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 4 filled years\"",
  "paragraph_id": "0001032975-26-000050:trends:contract_liabilities_over_revenue:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_insufficient",
  "what_changed": "insufficient. days_sales_of_inventory is not filled for the year ended 2026-03-31 because no cost-of-revenue row exists for that year (reason quoted). No change exists.",
  "account": "inventory over cost of revenue (days)",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-03-31; no comparison exists",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2025-04-01..2026-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001032975-26-000050:trends:days_sales_of_inventory:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "days_sales_outstanding for the year ended 2026-03-31 is 38.14306366292407 (printed inputs: receivables 505867000 at 2026-03-31, annual revenue 4840761000, 365 days). Year-over-year change against years-back-1 is 1.7187096705202904. Position: second lowest of the 5 filled years.",
  "account": "accounts receivable, net (days sales outstanding)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001032975-26-000050:trends:days_sales_outstanding:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_insufficient",
  "what_changed": "insufficient. gross_margin is not filled for the year ended 2026-03-31 because no cost-of-revenue row exists for that year (reason quoted). No change exists.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-03-31; no comparison exists",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2025-04-01..2026-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001032975-26-000050:trends:gross_margin:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled for the year ended 2026-03-31 because the record tags no InventoryValuationReserves in any period (reason quoted). No change exists.",
  "account": "inventory valuation reserve over inventory",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-03-31; no comparison exists",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001032975-26-000050:trends:inventory_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient. non_gaap_gap is not filled for the year ended 2026-03-31 because no us-gaap concept carries a non-GAAP measure (reason quoted). No change exists.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-03-31; no comparison exists",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001032975-26-000050:trends:non_gaap_gap:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "receivables_over_revenue for the year ended 2026-03-31 is 0.10450154428198376 (printed inputs: receivables 505867000, annual revenue 4840761000). Year-over-year change against years-back-1 is 0.004708793617863805. Position: second lowest of the 5 filled years.",
  "account": "accounts receivable, net over revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001032975-26-000050:trends:receivables_over_revenue:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "soft_asset_share for the year ended 2026-03-31 is 0.5172255383013199 (printed inputs: assets 3848588000, PP&E 116454000, cash 1741546000). Year-over-year change against years-back-1 is -0.025783880368264733. Position: lowest of the 5 filled years.",
  "account": "soft assets over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001032975-26-000050:trends:soft_asset_share:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "warranty_reserve_ratio for the year ended 2026-03-31 is 0.010378946616038264 (printed inputs: StandardProductWarrantyAccrual 50242000 at 2026-03-31, annual revenue 4840761000). Year-over-year change against years-back-1 is -0.0004190950533726999. Position: third highest of the 5 filled years.",
  "account": "product warranty accrual over revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001032975-26-000050:trends:warranty_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_cost_of_goods_sold_has_no_fact",
  "what_changed": "The current 10-Q's income-statement facts print GrossProfit 607940000 for the quarter ended 2026-06-30 (478962000 a year earlier). In my input the statement facts run from revenue (f-32, f-33) straight to gross profit (f-38, f-39), so there is no cost-of-goods-sold fact. The 8-K's statement prints a 'Cost of goods sold' line (618,599 in thousands) and a separate 'Amortization of intangible assets' line within gross profit. This is why gross margin and days of inventory could not be filled. Gross profit is present; its cost side is not in the record.",
  "account": "cost of goods sold / gross profit",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 and quarter ended 2025-06-30",
  "quote": "\"value\": \"607940000\"",
  "paragraph_id": "0001032975-26-000050:facts:GrossProfit:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_increase_in_cash_flow",
  "what_changed": "The cash-flow statement prints IncreaseDecreaseInAccountsReceivable of 162667000 for the quarter ended 2026-06-30 and 166767000 for the quarter ended 2025-06-30. The balance sheet prints AccountsReceivableNetCurrent 668497000 at 2026-06-30 and 505867000 at 2026-03-31. Receivables rose within the quarter in both years. The trend table places days sales outstanding third lowest of 6 filled quarters.",
  "account": "accounts receivable, net",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance; flow against quarter ended 2025-06-30",
  "quote": "\"value\": \"162667000\"",
  "paragraph_id": "0001032975-26-000050:facts:IncreaseDecreaseInAccountsReceivable:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_inflow_smaller",
  "what_changed": "The cash-flow statement prints IncreaseDecreaseInAccountsPayable of 56210000 for the quarter ended 2026-06-30 against 135003000 for the quarter ended 2025-06-30. The balance sheet prints AccountsPayableCurrent 585798000 at 2026-06-30 and 530983000 at 2026-03-31.",
  "account": "accounts payable",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"56210000\"",
  "paragraph_id": "0001032975-26-000050:facts:IncreaseDecreaseInAccountsPayable:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_change",
  "what_changed": "The cash-flow statement prints IncreaseDecreaseInAccruedLiabilities of 6038000 for the quarter ended 2026-06-30 against -51861000 for the quarter ended 2025-06-30. The balance sheet prints AccruedLiabilitiesCurrent 764666000 at 2026-06-30 and 781990000 at 2026-03-31.",
  "account": "accrued and other liabilities",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"6038000\"",
  "paragraph_id": "0001032975-26-000050:facts:IncreaseDecreaseInAccruedLiabilities:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_quarterly",
  "what_changed": "NetCashProvidedByUsedInOperatingActivities is 166708000 for the quarter ended 2026-06-30 against 125045000 for the quarter ended 2025-06-30. Net income for the same quarters prints 235697000 and 146015000. Net income is the larger in both quarters, which is why the accruals ratio is positive in both filled quarters.",
  "account": "operating cash flow",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"166708000\"",
  "paragraph_id": "0001032975-26-000050:facts:NetCashProvidedByUsedInOperatingActivities:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_inventory_balance_without_cost_of_sales",
  "what_changed": "InventoryNet prints 491743000 at 2026-06-30 and 489948000 at 2026-03-31. The cash-flow line IncreaseDecreaseInInventories prints 707000 for the quarter ended 2026-06-30 and -17304000 a year earlier. With no cost-of-goods-sold fact in the record, inventory cannot be put into days. That ratio is insufficient, and I do not estimate it.",
  "account": "inventories",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"491743000\"",
  "paragraph_id": "0001032975-26-000050:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "earnings_quality_other_current_assets_balance",
  "what_changed": "OtherAssetsCurrent prints 211324000 at 2026-06-30 and 177895000 at 2026-03-31. The cash-flow line IncreaseDecreaseInOtherOperatingAssets prints 29789000 for the quarter against 19817000 a year earlier. The input does not say what the balance holds beyond the note breakdown (see the notes items). It does not say whether the tariff refunds named in the 8-K sit in it.",
  "account": "other current assets",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"211324000\"",
  "paragraph_id": "0001032975-26-000050:facts:OtherAssetsCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases",
  "what_changed": "PaymentsForRepurchaseOfCommonStock prints 113616000 for the quarter ended 2026-06-30 against 121657000 for the quarter ended 2025-06-30. The 8-K says the company returned $114 million through share repurchases. Treasury shares print 17218000 at 2026-06-30 and 17282000 at 2026-03-31. Weighted diluted shares print 145038000 against 149053000 a year earlier.",
  "account": "share repurchases",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"113616000\"",
  "paragraph_id": "0001032975-26-000050:facts:PaymentsForRepurchaseOfCommonStock:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_tax_withholding_on_share_settlements",
  "what_changed": "PaymentsRelatedToTaxWithholdingForShareBasedCompensation prints 35644000 for the quarter ended 2026-06-30 against 16038000 for the quarter ended 2025-06-30. Net cash used in financing prints -140653000 against -134433000.",
  "account": "tax withholding on net share settlement of restricted stock units",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"35644000\"",
  "paragraph_id": "0001032975-26-000050:facts:PaymentsRelatedToTaxWithholdingForShareBasedCompensation:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_tariff_refunds_in_gross_margin",
  "what_changed": "The earnings release says the quarter's GAAP gross margin (49.5 percent, up 780 basis points) and non-GAAP gross margin (49.8 percent, up 770 basis points) include $61 million in tariff refunds. The input gives no breakdown of the margin with the refunds removed. The trend table holds no gross margin for any period.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "These numbers include $61 million in tariff refunds.",
  "paragraph_id": "0001032975-26-000047:8k_2_02:11" }
```

```json
{ "id": "earnings_quality_tariff_refunds_in_operating_income",
  "what_changed": "The release says GAAP operating income ($259 million, up 60 percent) and non-GAAP operating income ($290 million, up 44 percent) include the same $61 million in tariff refunds. The 10-Q fact OperatingIncomeLoss prints 258551000 for the quarter and 162094000 a year earlier.",
  "account": "operating income",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "Non-GAAP operating income was $290 million, up 44 percent, compared to Q1 of the prior year. These numbers include $61 million in tariff refunds.",
  "paragraph_id": "0001032975-26-000047:8k_2_02:12" }
```

```json
{ "id": "earnings_quality_operating_growth_excluding_tariff_refunds",
  "what_changed": "The chief financial officer says reported results benefited from tariff refunds. Excluding them, he says, non-GAAP operating income grew 14 percent year over year, against the 44 percent the release reports with them. No dollar figure for the ex-refund amount is in my input.",
  "account": "non-GAAP operating income",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "our operational performance was impressive even excluding these refunds, with non-GAAP operating income growing 14 percent year over year",
  "paragraph_id": "0001032975-26-000047:8k_2_02:17" }
```

```json
{ "id": "earnings_quality_full_year_margin_helped_by_tariff_refunds",
  "what_changed": "The release says the company still expects full-year non-GAAP operating margin near the high end of its 15 to 18 percent long-term range. It says that expectation is helped by this quarter's tariff refunds as well as operating performance. The refunds therefore support the full-year margin view, not only the quarter.",
  "account": "non-GAAP operating margin",
  "expected_direction": "none",
  "horizon": "fiscal year ending 2027-03-31, per the release",
  "quote": "helped by strong operating performance and this quarter",
  "paragraph_id": "0001032975-26-000047:8k_2_02:26" }
```

```json
{ "id": "across_documents_gross_margin_printed_in_release_not_in_trend_table",
  "what_changed": "The release prints GAAP gross margin of 49.5 percent for the quarter (41.7 percent a year earlier in its reconciliation table). The trend table cannot fill gross margin in any period because the record has no cost-of-revenue row. The figure exists only in the company's own release, and nothing in my input checks it.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "GAAP gross margin was 49.5 percent, up 780 basis points, compared to Q1 of the prior year.",
  "paragraph_id": "0001032975-26-000047:8k_2_02:11" }
```

```json
{ "id": "across_documents_preliminary_release_against_filed_quarter",
  "what_changed": "The release, filed 2026-07-28, labels its figures preliminary and subject to adjustment through the 10-Q filing. The 10-Q (0001032975-26-000050) was filed 2026-07-29. On the lines I set side by side, the release's figures (in thousands) and the 10-Q facts (in dollars) show the same digits. The lines are: net sales 1,227,234 / 1227234000, gross profit 607,940 / 607940000, operating income 258,551 / 258551000, net income 235,697 / 235697000, receivables 668,497 / 668497000, cash 1,749,679 / 1749679000 and operating cash flow 166,708 / 166708000. The prior-year column agrees the same way (net sales 1,147,703 / 1147703000; net income 146,015 / 146015000). No adjustment between release and filing is visible on these lines.",
  "account": "headline income statement, balance sheet and cash flow lines",
  "expected_direction": "none",
  "horizon": "release 2026-07-28 against 10-Q filed 2026-07-29",
  "quote": "These preliminary results for the three months ended June 30, 2026 are subject to adjustments",
  "paragraph_id": "0001032975-26-000047:8k_2_02:50" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_semiconductor_supplier_closure",
  "what_changed": "The release discloses that in late June 2026 a serious incident at the manufacturing facilities of one of the company's semiconductor suppliers temporarily closed it. It says this is likely to impact the company's ability to meet future demand and that the company is working on several mitigation plans.",
  "account": "net sales (supply constraint)",
  "expected_direction": "down",
  "horizon": "fiscal Q2 and Q3 of the year ending 2027-03-31, per the release",
  "quote": "resulted in its temporary closure, which is likely to impact the Company",
  "paragraph_id": "0001032975-26-000047:8k_2_02:23" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_supplier_incident_net_sales_impact",
  "what_changed": "The release estimates the supplier incident's negative impact on fiscal Q3 net sales at up to $200 million, 'based on limited available information'. It expects the incident to be largely resolved by Q4, with little to no Q4 impact. For scale, the trend input prints revenue of 1421479000 for the quarter ended 2025-12-31, the prior-year fiscal Q3. I do not set the two against each other numerically.",
  "account": "net sales",
  "expected_direction": "down",
  "horizon": "fiscal Q3 of the year ending 2027-03-31 (quarter ending 2026-12-31), per the release",
  "quote": "For Q3, based on limited available information, the negative impact of the supplier incident is estimated to be up to $200 million in net sales.",
  "paragraph_id": "0001032975-26-000047:8k_2_02:25" }
```

```json
{ "id": "results_against_expectations_outlook_includes_supplier_headwind",
  "what_changed": "The Q2 outlook midpoint still contemplates growth, despite a Q2 headwind of about $20 million in net sales from the supplier incident. The outlook table prints sales growth of '0% - 3%' in both US dollars and constant currency. The release reports Q1 growth as 7 percent in US dollars and 5 percent in constant currency.",
  "account": "net sales growth",
  "expected_direction": "down",
  "horizon": "fiscal Q2 of the year ending 2027-03-31 (quarter ending 2026-09-30), per the release",
  "quote": "The midpoint of the Q2 outlook contemplates growth despite a Q2 headwind of approximately $20 million in net sales caused by this supplier incident.",
  "paragraph_id": "0001032975-26-000047:8k_2_02:24" }
```

```json
{ "id": "results_against_expectations_sales_outlook_range",
  "what_changed": "The release's Q2 outlook prints sales of $1,185 to $1,220 million. The trend input prints revenue of 1186056000 for the quarter ended 2025-09-30, the prior-year Q2. The quarter just reported prints 1227234000.",
  "account": "net sales",
  "expected_direction": "none",
  "horizon": "fiscal Q2 of the year ending 2027-03-31 (quarter ending 2026-09-30), per the release",
  "quote": "$1,185 - $1,220 million",
  "paragraph_id": "0001032975-26-000047:8k_2_02:20" }
```

```json
{ "id": "results_against_expectations_operating_income_outlook_range",
  "what_changed": "The release's Q2 outlook prints non-GAAP operating income of $185 to $210 million. The quarter just reported prints non-GAAP operating income of 290,374 (in thousands), which includes the $61 million in tariff refunds. The release gives no GAAP reconciliation for the outlook.",
  "account": "non-GAAP operating income",
  "expected_direction": "down",
  "horizon": "fiscal Q2 of the year ending 2027-03-31 against the quarter ended 2026-06-30",
  "quote": "$185 - $210 million",
  "paragraph_id": "0001032975-26-000047:8k_2_02:20" }
```

```json
{ "id": "results_against_expectations_operating_income_above_own_outlook",
  "what_changed": "The chief financial officer says the quarter exceeded the company's own operating-income outlook. The outlook given for this quarter is not in my input, so the size of the beat does not exist here.",
  "account": "operating income",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against the company's prior outlook for it",
  "quote": "Strong gross margin resilience allowed us to exceed our operating income outlook",
  "paragraph_id": "0001032975-26-000047:8k_2_02:17" }
```

```json
{ "id": "results_against_expectations_no_formal_full_year_outlook",
  "what_changed": "The company is not issuing a formal full-year outlook for the fiscal year ending 2027-03-31. My input does not show whether an earlier release did issue one.",
  "account": "full-year outlook",
  "expected_direction": "none",
  "horizon": "fiscal year ending 2027-03-31",
  "quote": "While Logitech is not issuing a formal full-year FY27 outlook, demand momentum from Q1 is expected to carry into the remainder of the year.",
  "paragraph_id": "0001032975-26-000047:8k_2_02:22" }
```

## Seen in the notes

No fact in my input carries an in-note mark. Every fact row I read has only these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date. None says whether its element sat inside a note. The items below are current-10-Q facts that come after the primary statements in the instance (f-299 onward). They are breakdowns by allowance type, inventory component, accrued-liability component, warranty roll-forward, tax rate, repurchase program, product category and region. Putting them here is my reading of where they sit, not a marker, so a later split should treat the placement as unverified.

```json
{ "id": "revenue_recognition_gross_receivables_before_allowances",
  "what_changed": "AccountsReceivableGrossCurrent prints 1008529000 at 2026-06-30 and 792466000 at 2026-03-31. Net receivables print 668497000 and 505867000. The allowance rows between gross and net are the four program-type items below.",
  "account": "accounts receivable, gross",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"1008529000\"",
  "paragraph_id": "0001032975-26-000050:facts:AccountsReceivableGrossCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_pricing_program_allowance",
  "what_changed": "The receivable allowance for pricing programs prints 172875000 at 2026-06-30 and 144800000 at 2026-03-31. It is the largest of the four allowance types printed.",
  "account": "allowance for pricing programs (receivables)",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"172875000\"",
  "paragraph_id": "0001032975-26-000050:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30:us-gaap:ValuationAllowancesAndReservesTypeAxis=logi:AllowanceForPricingProgramsMember" }
```

```json
{ "id": "revenue_recognition_customer_incentive_program_allowance",
  "what_changed": "The receivable allowance for customer incentive programs prints 89805000 at 2026-06-30 and 73999000 at 2026-03-31.",
  "account": "allowance for customer incentive programs (receivables)",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"89805000\"",
  "paragraph_id": "0001032975-26-000050:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30:us-gaap:ValuationAllowancesAndReservesTypeAxis=logi:AllowanceForCustomerIncentiveProgramsMember" }
```

```json
{ "id": "revenue_recognition_cooperative_marketing_allowance",
  "what_changed": "The receivable allowance for cooperative marketing arrangements prints 59924000 at 2026-06-30 and 49964000 at 2026-03-31. The 10-K's valuation-allowance schedule prints this allowance at 44457000 at 2025-03-31.",
  "account": "allowance for cooperative marketing arrangements (receivables)",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"59924000\"",
  "paragraph_id": "0001032975-26-000050:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30:us-gaap:ValuationAllowancesAndReservesTypeAxis=logi:AllowanceForCooperativeMarketingArrangementsMember" }
```

```json
{ "id": "estimates_and_discretion_other_receivable_allowances",
  "what_changed": "The 'other' receivable allowance prints 17428000 at 2026-06-30 and 17836000 at 2026-03-31.",
  "account": "other allowances (receivables)",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"17428000\"",
  "paragraph_id": "0001032975-26-000050:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30:us-gaap:ValuationAllowancesAndReservesTypeAxis=logi:OtherAllowancesMember" }
```

```json
{ "id": "estimates_and_discretion_receivable_allowances_tagged_only_by_program_type",
  "what_changed": "Every AllowanceForDoubtfulAccountsReceivableCurrent fact I read at 2026-06-30 and 2026-03-31 carries a ValuationAllowancesAndReservesTypeAxis member: cooperative marketing, customer incentive programs, pricing programs or other. None is entity-wide. This is why the trend table finds 'no row for bad_debt_allowance' in any period and the bad-debt reserve ratio is insufficient everywhere. The allowances are mostly sales-incentive reserves, not credit-loss reserves.",
  "account": "receivable allowances (structure of tagging)",
  "expected_direction": "none",
  "horizon": "2026-06-30 and 2026-03-31 balances",
  "quote": "\"member\": \"logi:OtherAllowancesMember\"",
  "paragraph_id": "0001032975-26-000050:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30:us-gaap:ValuationAllowancesAndReservesTypeAxis=logi:OtherAllowancesMember" }
```

```json
{ "id": "estimates_and_discretion_finished_goods_inventory_net_of_reserves",
  "what_changed": "InventoryFinishedGoodsNetOfReserves prints 432449000 at 2026-06-30 and 427464000 at 2026-03-31. It is tagged net of reserves, with no reserve amount alongside, which matches the trend table's missing inventory reserve.",
  "account": "finished goods inventory, net of reserves",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"432449000\"",
  "paragraph_id": "0001032975-26-000050:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_raw_materials_inventory_net_of_reserves",
  "what_changed": "InventoryRawMaterialsNetOfReserves prints 59294000 at 2026-06-30 and 62484000 at 2026-03-31. It is tagged net of reserves.",
  "account": "raw materials inventory, net of reserves",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"59294000\"",
  "paragraph_id": "0001032975-26-000050:facts:InventoryRawMaterialsNetOfReserves:2026-06-30" }
```

```json
{ "id": "earnings_quality_prepaid_and_other_current_assets",
  "what_changed": "PrepaidExpenseAndOtherAssetsCurrent prints 171992000 at 2026-06-30 and 119295000 at 2026-03-31, within other current assets of 211324000 and 177895000. The facts I read do not say what the line holds. They do not say whether the $61 million in tariff refunds the release names, or any receivable for them, is in it.",
  "account": "prepaid expenses and other current assets",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"171992000\"",
  "paragraph_id": "0001032975-26-000050:facts:PrepaidExpenseAndOtherAssetsCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_value_added_tax_receivable",
  "what_changed": "ValueAddedTaxReceivable prints 39332000 at 2026-06-30 and 58600000 at 2026-03-31.",
  "account": "value added tax receivable",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"39332000\"",
  "paragraph_id": "0001032975-26-000050:facts:ValueAddedTaxReceivable:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_employee_related_liabilities",
  "what_changed": "EmployeeRelatedLiabilitiesCurrent prints 144477000 at 2026-06-30 and 165404000 at 2026-03-31.",
  "account": "accrued personnel expenses",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"144477000\"",
  "paragraph_id": "0001032975-26-000050:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_accrued_liabilities",
  "what_changed": "OtherAccruedLiabilitiesCurrent prints 174694000 at 2026-06-30 and 193550000 at 2026-03-31. Total accrued and other current liabilities print 764666000 and 781990000.",
  "account": "other accrued current liabilities",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"174694000\"",
  "paragraph_id": "0001032975-26-000050:facts:OtherAccruedLiabilitiesCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_current_taxes_payable",
  "what_changed": "TaxesPayableCurrent prints 45991000 at 2026-06-30 and 37843000 at 2026-03-31.",
  "account": "current taxes payable",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"45991000\"",
  "paragraph_id": "0001032975-26-000050:facts:TaxesPayableCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_sales_and_excise_tax_payable",
  "what_changed": "SalesAndExciseTaxPayableCurrent prints 27700000 at 2026-06-30 and 36292000 at 2026-03-31.",
  "account": "VAT and sales tax payable",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"27700000\"",
  "paragraph_id": "0001032975-26-000050:facts:SalesAndExciseTaxPayableCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_noncurrent_contract_liabilities",
  "what_changed": "ContractWithCustomerLiabilityNoncurrent prints 55725000 at 2026-06-30 and 53624000 at 2026-03-31. The current portion prints 41306000 and 38652000. The trend table's contract-liabilities ratio uses the current portion only, so this non-current balance is outside it.",
  "account": "non-current contract liabilities",
  "expected_direction": "up",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"55725000\"",
  "paragraph_id": "0001032975-26-000050:facts:ContractWithCustomerLiabilityNoncurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_current_warranty_accrual",
  "what_changed": "ProductWarrantyAccrualClassifiedCurrent prints 34958000 at 2026-06-30 and 35488000 at 2026-03-31. ProductWarrantyAccrualNoncurrent prints 14321000 and 14754000. The total StandardProductWarrantyAccrual prints 49279000 at 2026-06-30 against 50242000 at 2026-03-31 and 50206000 at 2025-06-30.",
  "account": "product warranty accrual",
  "expected_direction": "down",
  "horizon": "2026-06-30 balance against 2026-03-31 balance",
  "quote": "\"value\": \"34958000\"",
  "paragraph_id": "0001032975-26-000050:facts:ProductWarrantyAccrualClassifiedCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accruals_issued",
  "what_changed": "The warranty roll-forward prints StandardProductWarrantyAccrualWarrantiesIssued of 8496000 for the quarter ended 2026-06-30, against 8622000 a year earlier. Net sales printed for those quarters are 1227234000 and 1147703000. The facts give no separate change-in-estimate line in what I read, and I compute no accrual rate.",
  "account": "warranty accruals for warranties issued",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"8496000\"",
  "paragraph_id": "0001032975-26-000050:facts:StandardProductWarrantyAccrualWarrantiesIssued:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_payments",
  "what_changed": "The warranty roll-forward prints StandardProductWarrantyAccrualPayments of 9553000 for the quarter ended 2026-06-30, against 8249000 a year earlier. In the quarter just ended, the printed payments are larger than the printed accruals for warranties issued (8496000). The foreign-currency line prints -94000.",
  "account": "warranty settlements",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"9553000\"",
  "paragraph_id": "0001032975-26-000050:facts:StandardProductWarrantyAccrualPayments:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate",
  "what_changed": "EffectiveIncomeTaxRateContinuingOperations prints 0.145 for the quarter ended 2026-06-30 and 0.163 for the quarter ended 2025-06-30. The provision prints 39883000 on the statement and 39900000 rounded in the tax note, against 28470000 and 28500000 a year earlier.",
  "account": "effective income tax rate",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"0.145\"",
  "paragraph_id": "0001032975-26-000050:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_remaining_repurchase_authorization",
  "what_changed": "The remaining authorized amount under the 2026 share repurchase program prints 1300000000 at 2026-06-30. Repurchases under that program print 100775000 for the quarter, and under the 2023 program 0 (124135000 a year earlier).",
  "account": "share repurchase authorization",
  "expected_direction": "none",
  "horizon": "2026-06-30 balance",
  "quote": "\"value\": \"1300000000\"",
  "paragraph_id": "0001032975-26-000050:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-06-30:srt:ShareRepurchaseProgramAxis=logi:TwentyTwentySixShareRepurchaseProgramMember" }
```

```json
{ "id": "revenue_recognition_gaming_category_sales",
  "what_changed": "Gaming net sales print 354230000 for the quarter ended 2026-06-30 against 315875000 a year earlier. The release prints the change as 12 percent and notes that gaming includes Streamlabs streaming services revenue.",
  "account": "net sales, gaming",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"354230000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailGamingMember" }
```

```json
{ "id": "revenue_recognition_keyboards_and_combos_category_sales",
  "what_changed": "Keyboards and combos net sales print 227798000 for the quarter ended 2026-06-30 against 222492000 a year earlier. The release prints the change as 2 percent.",
  "account": "net sales, keyboards and combos",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"227798000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailKeyboardsDesktopsMember" }
```

```json
{ "id": "revenue_recognition_pointing_devices_category_sales",
  "what_changed": "Pointing devices net sales print 227312000 for the quarter ended 2026-06-30 against 195780000 a year earlier. The release prints the change as 16 percent, and its chief executive cites double-digit growth in pointing devices.",
  "account": "net sales, pointing devices",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"227312000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailPointingDevicesMember" }
```

```json
{ "id": "revenue_recognition_video_collaboration_category_sales",
  "what_changed": "Video collaboration net sales print 185260000 for the quarter ended 2026-06-30 against 166716000 a year earlier. The release prints the change as 11 percent.",
  "account": "net sales, video collaboration",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"185260000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailVideoCollaborationMember" }
```

```json
{ "id": "revenue_recognition_webcams_category_sales",
  "what_changed": "Webcams net sales print 76581000 for the quarter ended 2026-06-30 against 84374000 a year earlier. The release prints the change as (9) percent.",
  "account": "net sales, webcams",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"76581000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailWebcamsMember" }
```

```json
{ "id": "revenue_recognition_tablet_accessories_category_sales",
  "what_changed": "Tablet and other accessories net sales print 89395000 for the quarter ended 2026-06-30 against 91227000 a year earlier. The release prints the change as (2) percent.",
  "account": "net sales, tablet accessories",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"89395000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailTabletAndOtherAccessoriesMember" }
```

```json
{ "id": "revenue_recognition_headsets_category_sales",
  "what_changed": "Headsets net sales print 44133000 for the quarter ended 2026-06-30 against 45523000 a year earlier. The release prints the change as (3) percent.",
  "account": "net sales, headsets",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"44133000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:RetailHeadsetsMember" }
```

```json
{ "id": "revenue_recognition_other_products_category_sales",
  "what_changed": "'Other' product net sales (mainly mobile and PC speakers, per the release) print 22525000 for the quarter ended 2026-06-30 against 25716000 a year earlier. The release prints the change as (12) percent.",
  "account": "net sales, other products",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"22525000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=logi:OtherRetailProductsMember" }
```

```json
{ "id": "revenue_recognition_americas_region_sales",
  "what_changed": "Americas net sales print 515916000 for the quarter ended 2026-06-30 against 461690000 a year earlier.",
  "account": "net sales, Americas",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"515916000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_emea_region_sales",
  "what_changed": "EMEA net sales print 343732000 for the quarter ended 2026-06-30 against 346840000 a year earlier.",
  "account": "net sales, EMEA",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"343732000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_asia_pacific_region_sales",
  "what_changed": "Asia Pacific net sales print 367586000 for the quarter ended 2026-06-30 against 339173000 a year earlier.",
  "account": "net sales, Asia Pacific",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"367586000\"",
  "paragraph_id": "0001032975-26-000050:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```
