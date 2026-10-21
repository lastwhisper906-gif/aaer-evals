<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
Numbers report: AMD (ADVANCED MICRO DEVICES INC, CIK 0000002488). Triggering filing: 10-Q 0000002488-26-000123 for the quarter ended 2026-06-27, filed 2026-08-05. Earnings release: 8-K 0000002488-26-000121, filed 2026-08-04. Cutoff: 2026-08-05.

Directory check. My directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. input_prior_predictions.md records no earlier run for this company, so no prior flag is carried forward.

How far I read. I read input_trends.json, input_8k.md and input_prior_predictions.md in full. input_numbers.json is 67,350 lines (about 2.2 MB) holding three documents: 10-K 0000002488-26-000018, 10-Q 0000002488-26-000076 and 10-Q 0000002488-26-000123. That is more than fits in my context, so I read it in parts:
- lines 1-3,240: the document list and the 10-K's income statement, comprehensive income and balance sheet;
- lines 29,500-30,300: the 10-K's closing tax and subsequent-event facts, and the start of the 0000002488-26-000076 block;
- lines 47,290-49,920: the 0000002488-26-000123 income statement, comprehensive income and balance sheet;
- lines 66,800-67,350: that filing's closing share-based-compensation and tax facts.
Facts outside those ranges are unread and unreported. A full pass over that file is still owed.

Conventions.
- Every quote is a verbatim line, or a substring of one, from my input.
- Trend cells are quoted by their position_in_history line, or by their missing line where the cell is empty.
- Numeric facts are quoted by their value line, or by the superseded_by line where that is the point.
- Release figures are quoted by their prose or table row.
- expected_direction is the sign of the printed change in the named account, over the horizon named. For quarterly trend cells that is the year-over-year change against quarters-back-4. It is none where a cell prints no value or no change. It is not a forecast, except in the outlook item, where it follows the release's own statement.
- Every number below is copied as printed. I computed none.

What my input does not hold, said once here rather than as items:
- Articulation checks. Neither JSON file contains any, so I report no articulation gap. I do not tie statements myself.
- Restatement traces. No trace section exists. The only trace-like field is superseded_by, which some 10-K facts print. The item articulation_and_the_filed_history_year_end_balance_sheet_superseded_unchanged_reported_fact reports what I could read of it.
- The fourth-quarter derivation. The trend table has no cells for quarters-back-2 (target end 2025-12-27) or quarters-back-6 (target end 2024-12-28), so there is nothing to quote for them. Both periods give the same reason: no quarter ending within 20 days of the target end is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration, because the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py. That derivation's output is not in my input. I report no fourth-quarter value and derive none. Because of the gap, quarters-back-1 and quarters-back-5 print no quarter-over-quarter change.
- A note marker. No fact in the parts of input_numbers.json I read says whether its element sat inside a note. See the second heading.
- A change of tag in the trend table. There is none. Every filled cell, in every period, rests on the same concepts: RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold, AccountsReceivableNetCurrent, InventoryNet, Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet, NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities and ProductWarrantyAccrual. The two concept differences I found in the numeric facts are items below.
- Ratios the table fills in no period at all: bad_debt_reserve_ratio, contract_liabilities_over_revenue, inventory_reserve_ratio and non_gaap_gap. warranty_reserve_ratio is filled in the 5 years only. accruals_over_total_assets is filled in 2 quarters and 5 years.
- The years-back-0 research-and-development capitalization baseline prints no paragraph_id, so it can't be quoted and has no item. As printed:
  - research_and_development_asset 19350000000.0;
  - research_and_development_amortization 4432200000.0;
  - earnings_with_rnd_capitalized 7993800000.0, against net_income 4335000000.0;
  - book_value_with_rnd_capitalized 82349000000.0, against stockholders_equity 62999000000.0;
  - life_years 5.
  capitalized_development_cost and capitalized_over_expense are missing because the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period. The baseline's R&D expense input has an item below.

## Seen in the statements

**Trend table, quarters-back-0 (2026-03-29..2026-06-27)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cell_insufficient",
  "what_changed": "insufficient: accruals over total assets has no value for quarters-back-0. The cell's reason is that us-gaap:NetCashProvidedByUsedInOperatingActivities and us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations are in the record but not for this three-month period, so no change is printed against quarters-back-1 or quarters-back-4. Across all quarters the table fills this ratio only in quarters-back-1 and quarters-back-5, whose cells place them among 2 filled quarters. That would not support a trend claim either. I do not derive a quarterly operating cash flow from year-to-date figures.",
  "account": "net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-03-29..2026-06-27: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000002488-26-000123:trends:accruals_over_total_assets:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_cell_insufficient",
  "what_changed": "insufficient: the bad debt reserve ratio has no value for quarters-back-0. None of the three allowance concepts the table looks for is in the record at 2026-06-27. The table fills this ratio in none of the 6 quarters or 5 years it holds, so my input carries no allowance history at all: no value, no change, no position.",
  "account": "allowance for credit losses on receivables, against receivables",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-27: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000002488-26-000123:trends:bad_debt_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_cell_insufficient",
  "what_changed": "insufficient: contract liabilities over revenue has no value for quarters-back-0. None of the four contract-liability or deferred-revenue concepts the table looks for is in the record at 2026-06-27. The ratio is filled in no period the table holds, so my input carries no deferred-revenue history.",
  "account": "contract liabilities / deferred revenue, against revenue",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for contract_liabilities in 2026-06-27: us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue is in the record, but not for this period\"",
  "paragraph_id": "0000002488-26-000123:trends:contract_liabilities_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend_cell",
  "what_changed": "Days sales of inventory for quarters-back-0 is 144.4942808925558. Inputs, both from 0000002488-26-000123: InventoryNet at 2026-06-27, 8468000000.0, and CostOfGoodsAndServicesSold for the quarter, 5333000000.0. Printed changes: -6.8588305401504215 against quarters-back-1 and 13.148193560087151 against quarters-back-4. Position: third lowest of the 6 filled quarters. The year-over-year base, quarters-back-4 (131.34608733246864), prints as the lowest of the 6 filled quarters; quarters-back-5 (157.7136682874122) prints as the highest. Six filled quarters with two missing among them is a short history.",
  "account": "inventories, net (InventoryNet) against cost of revenue (CostOfGoodsAndServicesSold)",
  "expected_direction": "up",
  "horizon": "year over year against quarters-back-4; the quarter-over-quarter change against quarters-back-1 has the opposite sign",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0000002488-26-000123:trends:days_sales_of_inventory:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend_cell",
  "what_changed": "Days sales outstanding for quarters-back-0 is 57.43507281553398. Inputs, both from 0000002488-26-000123: AccountsReceivableNetCurrent at 2026-06-27, 7281000000.0, and quarterly revenue (RevenueFromContractWithCustomerExcludingAssessedTax), 11536000000.0. Printed changes: 3.871725502552408 against quarters-back-1 and -3.1329167745766213 against quarters-back-4. Position: second lowest of the 6 filled quarters. quarters-back-1 (53.56334731298157) prints as the lowest and quarters-back-7 (96.63161753922863) as the highest.",
  "account": "accounts receivable, net (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "down",
  "horizon": "year over year against quarters-back-4; the quarter-over-quarter change against quarters-back-1 has the opposite sign",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0000002488-26-000123:trends:days_sales_outstanding:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend_cell",
  "what_changed": "Gross margin for quarters-back-0 is 0.5377080443828016, from revenue 11536000000.0 and CostOfGoodsAndServicesSold 5333000000.0 (0000002488-26-000123). Printed changes: 0.009472406033050329 against quarters-back-1 and 0.13965989864435008 against quarters-back-4. Position: highest of the 6 filled quarters. The year-over-year base, quarters-back-4 (0.39804814573845154), prints as the lowest of the 6. The release says that quarter included $800 million in inventory and related charges; see the item across_documents_prior_year_quarter_inventory_charge_base_release_figures.",
  "account": "gross margin: revenue less cost of revenue (CostOfGoodsAndServicesSold), over revenue",
  "expected_direction": "up",
  "horizon": "year over year against quarters-back-4; quarter over quarter against quarters-back-1 has the same sign",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000002488-26-000123:trends:gross_margin:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_cell_insufficient",
  "what_changed": "insufficient: the inventory reserve ratio has no value for quarters-back-0. The record tags no us-gaap:InventoryValuationReserves in any period, and it cannot say whether the company does not tag the reserve or states it only by segment. The ratio is filled in no period. The release says the quarter a year earlier carried $800 million in inventory and related charges, a reserve history would bear on that, and none exists in my input.",
  "account": "inventory valuation reserve, against inventory",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000002488-26-000123:trends:inventory_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell_insufficient",
  "what_changed": "insufficient: the non-GAAP gap has no value for quarters-back-0 because companyfacts holds only us-gaap and dei facts, and no us-gaap concept carries a non-GAAP measure. The ratio is filled in no period. The release prints both GAAP and non-GAAP net income for the quarter (item earnings_quality_non_gaap_net_income_in_release_figures), but no input computes the gap and I do not.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000002488-26-000123:trends:non_gaap_gap:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend_cell",
  "what_changed": "Receivables over revenue for quarters-back-0 is 0.6311546463245492: receivables 7281000000.0 over the quarter's revenue 11536000000.0. Printed changes: 0.04254643409398251 against quarters-back-1 and -0.03442765686347937 against quarters-back-4. Position: second lowest of the 6 filled quarters. quarters-back-1 (0.5886082122305667) prints as the lowest and quarters-back-7 (1.0618859070244904) as the highest. The quarterly cells divide by one quarter's revenue, so they are on a different basis from the annual cells.",
  "account": "accounts receivable, net (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "down",
  "horizon": "year over year against quarters-back-4; the quarter-over-quarter change against quarters-back-1 has the opposite sign",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0000002488-26-000123:trends:receivables_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend_cell",
  "what_changed": "Soft asset share for quarters-back-0 is 0.8990694260276567. Inputs at 2026-06-27, all from 0000002488-26-000123: Assets 84464000000.0, PropertyPlantAndEquipmentNet 3439000000.0 and CashAndCashEquivalentsAtCarryingValue 5086000000.0. Printed changes: 0.003386243787130372 against quarters-back-1 and -0.013119828182447502 against quarters-back-4. Position: third lowest of the 6 filled quarters.",
  "account": "total assets less property and equipment and cash, over total assets",
  "expected_direction": "down",
  "horizon": "year over year against quarters-back-4; the quarter-over-quarter change against quarters-back-1 has the opposite sign",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0000002488-26-000123:trends:soft_asset_share:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_cell_insufficient",
  "what_changed": "insufficient: the warranty reserve ratio has no value for quarters-back-0. The three warranty-accrual concepts the table looks for are in the record, but not at 2026-06-27. The table fills this ratio in none of its 6 quarters; only the 5 annual cells are filled (item estimates_and_discretion_warranty_reserve_ratio_annual_trend_cell). Nothing in my input shows the warranty accrual after 2025-12-27.",
  "account": "product warranty accrual, against revenue",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-27: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000002488-26-000123:trends:warranty_reserve_ratio:2026-03-29..2026-06-27" }
```

**Trend table, years-back-0 (2024-12-29..2025-12-27)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend_cell",
  "what_changed": "Accruals over total assets for years-back-0 is -0.04386033330733432. Inputs: NetIncomeLoss 4335000000.0 and NetCashProvidedByUsedInOperatingActivities 7709000000.0, both from the 10-K 0000002488-26-000018, and Assets at 2025-12-27, 76926000000.0, taken from 0000002488-26-000123. The value is negative, so the numerator, net income less operating cash flow, is below zero. Printed change against years-back-1: -0.023636717902717555. Position: lowest of the 5 filled years.",
  "account": "net income less operating cash flow, over total assets",
  "expected_direction": "down",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:accruals_over_total_assets:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_cell_insufficient",
  "what_changed": "insufficient: the bad debt reserve ratio has no value for years-back-0. None of the three allowance concepts is in the record at 2025-12-27. No year or quarter in the table is filled, so no allowance history exists in my input.",
  "account": "allowance for credit losses on receivables, against receivables",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-12-27: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000002488-26-000123:trends:bad_debt_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_cell_insufficient",
  "what_changed": "insufficient: contract liabilities over revenue has no value for years-back-0. None of the four contract-liability or deferred-revenue concepts is in the record at 2025-12-27. No period in the table is filled.",
  "account": "contract liabilities / deferred revenue, against revenue",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for contract_liabilities in 2025-12-27: us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue is in the record, but not for this period\"",
  "paragraph_id": "0000002488-26-000123:trends:contract_liabilities_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend_cell",
  "what_changed": "Days sales of inventory for years-back-0 is 164.85846628924344. Inputs: InventoryNet at 2025-12-27, 7920000000.0, taken from 0000002488-26-000123, and CostOfGoodsAndServicesSold for the year, 17487000000.0, from the 10-K 0000002488-26-000018. Printed change against years-back-1: 5.044071189702862. Position: highest of the 5 filled years; years-back-1 (159.81439509954058) prints as second highest.",
  "account": "inventories, net (InventoryNet) against cost of revenue (CostOfGoodsAndServicesSold)",
  "expected_direction": "up",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:days_sales_of_inventory:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend_cell",
  "what_changed": "Days sales outstanding for years-back-0 is 66.36046075233119. Inputs: AccountsReceivableNetCurrent at 2025-12-27, 6315000000.0, taken from 0000002488-26-000123, and revenue 34639000000.0 from the 10-K. Printed change against years-back-1: -21.0503594919969. Position: third highest of the 5 filled years; years-back-1 (87.4108202443281) prints as the highest.",
  "account": "accounts receivable, net (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "down",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:days_sales_outstanding:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend_cell",
  "what_changed": "Gross margin for years-back-0 is 0.4951644100580271, from revenue 34639000000.0 and CostOfGoodsAndServicesSold 17487000000.0, both from the 10-K 0000002488-26-000018. Printed change against years-back-1: 0.0016604348786592449. Position: highest of the 5 filled years.",
  "account": "gross margin: revenue less cost of revenue (CostOfGoodsAndServicesSold), over revenue",
  "expected_direction": "up",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:gross_margin:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_cell_insufficient",
  "what_changed": "insufficient: the inventory reserve ratio has no value for years-back-0. The record tags no us-gaap:InventoryValuationReserves in any period, and it cannot say whether the reserve is untagged or stated only by segment. No period is filled.",
  "account": "inventory valuation reserve, against inventory",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000002488-26-000123:trends:inventory_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell_insufficient",
  "what_changed": "insufficient: the non-GAAP gap has no value for years-back-0 because companyfacts carries no non-GAAP measure. No period is filled.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none: the cell prints no value and no change",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000002488-26-000123:trends:non_gaap_gap:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend_cell",
  "what_changed": "Receivables over revenue for years-back-0 is 0.18230895811079997: receivables 6315000000.0 over revenue 34639000000.0. Printed change against years-back-1: -0.05783065794504644. Position: third highest of the 5 filled years; years-back-1 (0.2401396160558464) prints as the highest.",
  "account": "accounts receivable, net (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "down",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:receivables_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend_cell",
  "what_changed": "Soft asset share for years-back-0 is 0.8979408782466266. Inputs at 2025-12-27, all taken from 0000002488-26-000123: Assets 76926000000.0, PropertyPlantAndEquipmentNet 2312000000.0 and CashAndCashEquivalentsAtCarryingValue 5539000000.0. Printed change against years-back-1: -0.02132355997022828. Position: second lowest of the 5 filled years.",
  "account": "total assets less property and equipment and cash, over total assets",
  "expected_direction": "down",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:soft_asset_share:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend_cell",
  "what_changed": "The warranty reserve ratio for years-back-0 is 0.00889171165449349, from ProductWarrantyAccrual at 2025-12-27, 308000000.0, and revenue 34639000000.0, both from the 10-K 0000002488-26-000018. Printed change against years-back-1: 0.0016006509602914352. The accrual input is 188000000.0 for years-back-1 and 85000000.0 for years-back-2. Position: highest of the 5 filled years. No quarterly cell is filled, so nothing in my input shows the accrual after 2025-12-27.",
  "account": "product warranty accrual (ProductWarrantyAccrual), against revenue",
  "expected_direction": "up",
  "horizon": "year over year against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000002488-26-000123:trends:warranty_reserve_ratio:2024-12-29..2025-12-27" }
```

**Filed history and concepts**

```json
{ "id": "articulation_and_the_filed_history_year_end_balance_sheet_superseded_unchanged_reported_fact",
  "what_changed": "The 10-K (0000002488-26-000018) fact for Assets at 2025-12-27, 76926000000, is marked superseded_by 0000002488-26-000123, and that filing prints 76926000000 for Assets at 2025-12-27. The same holds for every other 10-K balance-sheet fact at 2025-12-27 that I read and could match to a 10-Q fact with the same tag. Each is marked superseded_by 0000002488-26-000123 and carries the same printed value in the 10-Q: CashAndCashEquivalentsAtCarryingValue 5539000000, ShortTermInvestments 5013000000, AccountsReceivableNetCurrent 6315000000, InventoryNet 7920000000, PrepaidExpenseAndOtherAssetsCurrent 2160000000, AssetsCurrent 26947000000, PropertyPlantAndEquipmentNet 2312000000, Goodwill 25126000000, IntangibleAssetsNetExcludingGoodwill 16705000000, DeferredIncomeTaxAssetsNet 384000000, OtherAssetsNoncurrent 5452000000, AccountsPayableCurrent 2929000000, OtherLiabilitiesCurrent 402000000, LiabilitiesCurrent 9455000000, LongTermDebtNoncurrent 2348000000, OperatingLeaseLiabilityNoncurrent 625000000, DeferredIncomeTaxLiabilitiesNet 313000000, OtherLiabilitiesNoncurrent 1186000000 and CommonStockSharesIssued 1695000000. The trend table's StockholdersEquity input at 2025-12-27 from 0000002488-26-000123, 62999000000.0, is also the 10-K's printed value. I found no restated prior value at the year-end balance-sheet date. Superseded facts in the parts of input_numbers.json I did not read are unchecked.",
  "account": "balance sheet at 2025-12-27, as filed in the 10-K and as carried in the current 10-Q",
  "expected_direction": "none",
  "horizon": "10-K filed 2026-02-04 against 10-Q filed 2026-08-05, same balance-sheet date",
  "quote": "\"superseded_by\": \"0000002488-26-000123\"",
  "paragraph_id": "0000002488-26-000018:facts:Assets:2025-12-27" }
```


```json
{ "id": "structure_and_disclosure_changes_current_debt_concept_change_reported_fact",
  "what_changed": "The release labels this line 'Current portion of long-term debt, net' (874 at December 27, 2025). The 10-K (0000002488-26-000018) tags it at 2025-12-27 as ShortTermBorrowings, value 874000000, and that fact carries no superseded_by. The current 10-Q (0000002488-26-000123) tags its 2025-12-27 comparative as LongTermDebtCurrent, 874000000, and its 2026-06-27 balance as LongTermDebtCurrent, 875000000. The same line at the same date rests on a different concept in the later filing. No input states why.",
  "account": "current portion of long-term debt",
  "expected_direction": "none",
  "horizon": "10-K filed 2026-02-04 against 10-Q filed 2026-08-05, same balance-sheet date",
  "quote": "\"value\": \"874000000\"",
  "paragraph_id": "0000002488-26-000018:facts:ShortTermBorrowings:2025-12-27" }
```

```json
{ "id": "structure_and_disclosure_changes_accrued_liabilities_concept_unclear_reported_fact",
  "what_changed": "The current 10-Q's balance-sheet accrued liabilities are tagged AccruedLiabilitiesCurrentAndNoncurrent: 5250000000 at 2025-12-27 and 5546000000 at 2026-06-27. The 10-K tags the 2025-12-27 line AccruedLiabilitiesCurrent, 5250000000, and marks that fact superseded_by 0000002488-26-000123. That means the 10-Q also prints an AccruedLiabilitiesCurrent fact for that date, in a part of input_numbers.json I did not read. From what I read, it is insufficient to say whether this is a change of tag for the line or two tags in use at once.",
  "account": "accrued liabilities",
  "expected_direction": "none",
  "horizon": "10-K filed 2026-02-04 against 10-Q filed 2026-08-05, same balance-sheet date",
  "quote": "\"value\": \"5250000000\"",
  "paragraph_id": "0000002488-26-000123:facts:AccruedLiabilitiesCurrentAndNoncurrent:2025-12-27" }
```

**Numeric facts**

```json
{ "id": "earnings_quality_prior_year_quarter_income_tax_benefit_reported_fact",
  "what_changed": "In 0000002488-26-000123, IncomeTaxExpenseBenefit for the quarter 2025-03-30..2025-06-28 is -834000000, a benefit, against 252000000 for 2026-03-29..2026-06-27. EffectiveIncomeTaxRateContinuingOperations prints 12.636 for the earlier quarter and 0.098 for the current one. The release attributes the earlier quarter to a release of reserves for uncertain tax positions, (853) in its reconciliation, which it says pertains to reasonable cause relief on dual consolidated losses approved by the Internal Revenue Service in Q2'25 (paragraph 58). Year-over-year comparisons of net income (2297000000 against 872000000) therefore set the current quarter against a base that contains that benefit.",
  "account": "income tax expense (benefit)",
  "expected_direction": "up",
  "horizon": "year over year: quarter ended 2026-06-27 against quarter ended 2025-06-28",
  "quote": "\"value\": \"-834000000\"",
  "paragraph_id": "0000002488-26-000123:facts:IncomeTaxExpenseBenefit:2025-03-30..2025-06-28" }
```

```json
{ "id": "earnings_quality_nonoperating_income_in_pretax_income_reported_fact",
  "what_changed": "OtherNonoperatingIncomeExpense in 0000002488-26-000123 is 598000000 for the quarter ended 2026-06-27, against 98000000 for the quarter ended 2025-06-28. The six-month figures are 763000000 against 137000000. Income before taxes and equity income for the quarter is 2551000000. In the release, non-GAAP net income removes '(Gains) loss on long-term investments, net' of (483) (paragraph 56), and the cash flow statement shows 'Gains from long-term investments, net' of (483) for the quarter (paragraph 79). So a non-operating investment gain sits inside this quarter's GAAP pre-tax income; the release's operating income for the quarter is 1,990.",
  "account": "other income (expense), net",
  "expected_direction": "up",
  "horizon": "year over year: quarter ended 2026-06-27 against quarter ended 2025-06-28",
  "quote": "\"value\": \"598000000\"",
  "paragraph_id": "0000002488-26-000123:facts:OtherNonoperatingIncomeExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_balance_reported_fact",
  "what_changed": "In the 10-K, UnrecognizedTaxBenefits is 806000000 at 2025-12-27, against 1498000000 at 2024-12-28 and 1463000000 at 2023-12-30. UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate is 571000000 at 2025-12-27 against 1300000000 at 2024-12-28. In the current 10-Q, AccruedIncomeTaxesNoncurrent is 873000000 at 2026-06-27 against 806000000 at 2025-12-27. The release ties the 2025 reserve release to IRS relief on dual consolidated losses (paragraph 58). This estimated reserve fell across 2025, and my input holds no 2026 figure for the unrecognized benefits themselves.",
  "account": "unrecognized tax benefits",
  "expected_direction": "down",
  "horizon": "2024-12-28 to 2025-12-27",
  "quote": "\"value\": \"806000000\"",
  "paragraph_id": "0000002488-26-000018:facts:UnrecognizedTaxBenefits:2025-12-27" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_guarantee_after_year_end_reported_fact",
  "what_changed": "The 10-K prints GuaranteeObligationsMaximumExposure of 4100000000 at 2026-02-03, under SubsequentEventTypeAxis = SubsequentEventMember. That is a guarantee exposure dated after the 2025-12-27 balance sheet and the day before the 10-K's filing date, 2026-02-04. The facts I read do not say whom the guarantee covers or why. I read no 10-Q fact carrying it to 2026-06-27.",
  "account": "guarantee obligations, maximum exposure",
  "expected_direction": "none",
  "horizon": "subsequent to 2025-12-27; its state at 2026-06-27 is not in what I read",
  "quote": "\"value\": \"4100000000\"",
  "paragraph_id": "0000002488-26-000018:facts:GuaranteeObligationsMaximumExposure:2026-02-03:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_zt_systems_reported_fact",
  "what_changed": "The 10-K prints BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1 of 121000000 for 2024-12-29..2025-12-27, under BusinessAcquisitionAxis = amd:ZTSystemsMember. This is a remeasurement of contingent consideration for the ZT Systems acquisition during the year. The facts I read give neither the fact's sign convention nor the liability balance, so I state no direction.",
  "account": "contingent consideration liability, ZT Systems acquisition",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-12-27",
  "quote": "\"value\": \"121000000\"",
  "paragraph_id": "0000002488-26-000018:facts:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1:2024-12-29..2025-12-27:us-gaap:BusinessAcquisitionAxis=amd:ZTSystemsMember" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_balance_reported_fact",
  "what_changed": "AccountsPayableCurrent is 5359000000 at 2026-06-27 against 2929000000 at 2025-12-27 (0000002488-26-000123). The release's cash flow statement shows accounts payable providing 2,274 in the quarter and 2,170 over six months (paragraph 79).",
  "account": "accounts payable",
  "expected_direction": "up",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"5359000000\"",
  "paragraph_id": "0000002488-26-000123:facts:AccountsPayableCurrent:2026-06-27" }
```

```json
{ "id": "earnings_quality_other_non_current_assets_balance_reported_fact",
  "what_changed": "OtherAssetsNoncurrent is 7904000000 at 2026-06-27 against 5452000000 at 2025-12-27 (0000002488-26-000123). The release shows purchases of long-term investments of (435) in the quarter and (844) over six months, and prepaid expenses and other assets using (683) in the quarter (paragraph 79). The facts I read do not break the balance down.",
  "account": "other non-current assets",
  "expected_direction": "up",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"7904000000\"",
  "paragraph_id": "0000002488-26-000123:facts:OtherAssetsNoncurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_property_and_equipment_balance_reported_fact",
  "what_changed": "PropertyPlantAndEquipmentNet is 3439000000 at 2026-06-27 against 2312000000 at 2025-12-27 (0000002488-26-000123). The release prints capital expenditures of 808 for the quarter ended June 27, 2026, 389 for the quarter ended March 28, 2026 and 282 for the quarter ended June 28, 2025 (paragraph 84).",
  "account": "property and equipment, net",
  "expected_direction": "up",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"3439000000\"",
  "paragraph_id": "0000002488-26-000123:facts:PropertyPlantAndEquipmentNet:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_short_term_investments_balance_reported_fact",
  "what_changed": "ShortTermInvestments is 8025000000 at 2026-06-27 against 5013000000 at 2025-12-27. CashAndCashEquivalentsAtCarryingValue is 5086000000 against 5539000000. The release prints cash, cash equivalents and short-term investments of 13,111 at June 27, 2026 against 12,347 at March 28, 2026, and total debt of 3,226 (paragraph 84).",
  "account": "short-term investments",
  "expected_direction": "up",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"8025000000\"",
  "paragraph_id": "0000002488-26-000123:facts:ShortTermInvestments:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_operating_lease_liabilities_balance_reported_fact",
  "what_changed": "OperatingLeaseLiabilityNoncurrent is 1050000000 at 2026-06-27 against 625000000 at 2025-12-27 (0000002488-26-000123). The facts I read give neither the right-of-use asset nor the reason.",
  "account": "long-term operating lease liabilities",
  "expected_direction": "up",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"1050000000\"",
  "paragraph_id": "0000002488-26-000123:facts:OperatingLeaseLiabilityNoncurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_goodwill_balance_reported_fact",
  "what_changed": "Goodwill is 25470000000 at 2026-06-27 against 25126000000 at 2025-12-27. IntangibleAssetsNetExcludingGoodwill is 15635000000 against 16705000000 (0000002488-26-000123). The release names the MEXT acquisition (paragraph 37) and shows acquisitions, net of cash acquired, of (129) in the quarter (paragraph 79). The facts I read hold no impairment test and no purchase-price allocation.",
  "account": "goodwill",
  "expected_direction": "up",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"25470000000\"",
  "paragraph_id": "0000002488-26-000123:facts:Goodwill:2026-06-27" }
```

```json
{ "id": "structure_and_disclosure_changes_shares_issued_and_treasury_stock_reported_fact",
  "what_changed": "CommonStockSharesIssued is 1632000000 at 2026-06-27 against 1695000000 at 2025-12-27 (0000002488-26-000123), and CommonStockSharesOutstanding is 1632000000 at 2026-06-27. At 2025-12-27 the 10-K printed TreasuryStockCommonShares 65000000 and TreasuryStockValue 7079000000. The release balance sheet prints 'Treasury stock, at cost' as — at June 27, 2026 against (7,079) at December 27, 2025, additional paid-in capital as 61,373 against 63,365, and retained earnings as 5,909 against 6,699 (paragraph 75). Treasury shares no longer appear as a separate balance, and no input says what was done with them.",
  "account": "common stock issued and treasury stock",
  "expected_direction": "down",
  "horizon": "2025-12-27 to 2026-06-27",
  "quote": "\"value\": \"1632000000\"",
  "paragraph_id": "0000002488-26-000123:facts:CommonStockSharesIssued:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_research_and_development_expense_annual_reported_fact",
  "what_changed": "ResearchAndDevelopmentExpense in the 10-K is 8091000000 for 2024-12-29..2025-12-27, against 6456000000 and 5872000000 for the two prior years. It is the years-back-0 input to the trend table's R&D capitalization baseline, whose values print without a paragraph_id (see the opening notes). The release prints research and development of 2,528 for the quarter ended June 27, 2026 against 1,894 a year earlier (paragraph 70).",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "year over year: fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28",
  "quote": "\"value\": \"8091000000\"",
  "paragraph_id": "0000002488-26-000018:facts:ResearchAndDevelopmentExpense:2024-12-29..2025-12-27" }
```

```json
{ "id": "structure_and_disclosure_changes_discontinued_operations_result_reported_fact",
  "what_changed": "IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity in 0000002488-26-000123 is -8000000 for the quarter ended 2026-06-27, against 104000000 for the quarter ended 2025-06-28; the six-month figure is 3000000. The release says the result relates to ZT Systems' manufacturing business, divested in Q4'25, and includes measurement-period adjustments in Q1'26 (paragraph 58). It also shows a payment for working capital adjustment on divestiture of (243) in the quarter (paragraph 79). Results after the divestiture still carry adjustments to it.",
  "account": "income (loss) from discontinued operations, net of tax",
  "expected_direction": "down",
  "horizon": "year over year: quarter ended 2026-06-27 against quarter ended 2025-06-28",
  "quote": "\"value\": \"-8000000\"",
  "paragraph_id": "0000002488-26-000123:facts:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity:2026-03-29..2026-06-27" }
```

**Earnings release figures**

```json
{ "id": "across_documents_prior_year_quarter_inventory_charge_base_release_figures",
  "what_changed": "The release footnotes the quarter ended June 28, 2025 (quarters-back-4 in the trend table) as including $800 million in inventory and related charges due to the U.S. Government's export control on MI308 data center GPUs. That quarter is the year-over-year base for the quarterly gross-margin and days-sales-of-inventory cells, and both of its own cells print as the lowest of the 6 filled quarters. The release prints GAAP gross margin of 40% for Q2'25 against 54% for Q2'26 (paragraph 17).",
  "account": "cost of sales and inventory, prior-year quarter",
  "expected_direction": "none",
  "horizon": "year over year against quarters-back-4",
  "quote": "results included $800 million in inventory and related charges due to the U.S. Government's export control on AMD Instinct",
  "paragraph_id": "0000002488-26-000121:8k_2_02:18" }
```

```json
{ "id": "earnings_quality_non_gaap_net_income_in_release_figures",
  "what_changed": "The release prints GAAP net income of $2.3 billion and non-GAAP net income of $2.8 billion for the quarter. Its reconciliation (paragraph 56) runs from GAAP 2,297 to non-GAAP 2,760. It adds back stock-based compensation 503, amortization of acquisition-related intangibles 544, acquisition-related and other costs 41, loss contingency on legal matters 17 and loss from discontinued operations 8. It takes out gains on long-term investments (483), equity income in investee (6) and an income tax provision adjustment (161), using a 13% non-GAAP tax rate for fiscal 2026 (paragraph 63). The trend table cannot compute the gap (non_gaap_gap is unfilled in every period), and I do not compute it.",
  "account": "GAAP and non-GAAP net income",
  "expected_direction": "none",
  "horizon": "the quarter ended June 27, 2026",
  "quote": "Second quarter revenue was $11.5 billion, gross margin was 54%, operating income was $2.0 billion, net income was $2.3 billion and diluted earnings per share was $1.38. On a non-GAAP(*) basis, gross margin was 56%, operating income was $3.1 billion, net income was $2.8 billion and diluted earnings per share was $1.66.",
  "paragraph_id": "0000002488-26-000121:8k_2_02:12" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_legal_matters_release_figures",
  "what_changed": "The release's reconciliations carry a new adjustment, 'Loss contingency on legal matters', of 17 for the three months ended June 27, 2026. It prints — for March 28, 2026 and for June 28, 2025, and 17 for the six months. Paragraph 55 excludes it from both non-GAAP gross profit and non-GAAP operating income. The release does not name the matter, and the facts I read hold no accrual for it.",
  "account": "loss contingency on legal matters",
  "expected_direction": "up",
  "horizon": "the quarter ended June 27, 2026 against the prior quarter and the prior-year quarter",
  "quote": "| Loss contingency on legal matters |  | 17 |",
  "paragraph_id": "0000002488-26-000121:8k_2_02:88" }
```

```json
{ "id": "results_against_expectations_revenue_and_margin_outlook_release_figures",
  "what_changed": "The release guides third-quarter 2026 revenue to approximately $13 billion, plus or minus $300 million, and non-GAAP gross margin to approximately 56%. It states the midpoint as about 41% year-over-year growth and about a 13% sequential increase. The quarter just reported has revenue of 11,536 at a non-GAAP gross margin of 56% (paragraph 20).",
  "account": "revenue and non-GAAP gross margin, outlook",
  "expected_direction": "up",
  "horizon": "the third quarter of 2026, as the release states",
  "quote": "For the third quarter of 2026, AMD expects revenue to be approximately $13 billion, plus or minus $300 million. The mid-point of the revenue range represents year-over-year growth of approximately 41% and a sequential increase of approximately 13%. Non-GAAP gross margin is expected to be approximately 56%.",
  "paragraph_id": "0000002488-26-000121:8k_2_02:51" }
```

```json
{ "id": "liquidity_and_capital_free_cash_flow_in_release_figures",
  "what_changed": "Free cash flow in the release is 1,558 for the quarter ended June 27, 2026, against 2,566 for the quarter ended March 28, 2026 and 1,180 for the quarter ended June 28, 2025. Free cash flow margin prints 14%, 25% and 15%. The inputs are GAAP net cash from operating activities of continuing operations, 2,366, 2,955 and 1,462, and purchases of property and equipment, (808), (389) and (282).",
  "account": "free cash flow (non-GAAP): operating cash flow of continuing operations less capital expenditures",
  "expected_direction": "down",
  "horizon": "quarter over quarter against the quarter ended March 28, 2026",
  "quote": "| Free cash flow |  | $ | 1,558 |  |  | $ | 2,566 |  |  | $ | 1,180 |",
  "paragraph_id": "0000002488-26-000121:8k_2_02:91" }
```

```json
{ "id": "revenue_recognition_receivables_cash_use_in_release_figures",
  "what_changed": "The release cash flow statement shows the change in accounts receivable, net, using (1,246) in the quarter ended June 27, 2026, against providing 330 in the quarter ended June 28, 2025; over six months the figures are (966) against 1,078. Accounts receivable, net, prints 7,281 at June 27, 2026 against 6,315 at December 27, 2025 (paragraph 75). The trend table's quarterly days-sales-outstanding cell rises against quarters-back-1 and falls against quarters-back-4.",
  "account": "accounts receivable, net",
  "expected_direction": "up",
  "horizon": "the quarter ended June 27, 2026",
  "quote": "| Accounts receivable, net |  | (1,246) |  |  | 330 |",
  "paragraph_id": "0000002488-26-000121:8k_2_02:79" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_gaming_revenue_decline_release_figures",
  "what_changed": "The release prints Gaming business revenue of $779 million, down 31% year over year on lower semi-custom revenue. Its segment table shows Gaming at 779, against 720 for the quarter ended March 28, 2026 and 1,122 for the quarter ended June 28, 2025 (paragraph 84).",
  "account": "Gaming revenue (Client and Gaming segment)",
  "expected_direction": "down",
  "horizon": "year over year: quarter ended June 27, 2026 against quarter ended June 28, 2025",
  "quote": "Gaming business revenue was $779 million, down 31% year-over-year, due to lower semi-custom revenue.",
  "paragraph_id": "0000002488-26-000121:8k_2_02:24" }
```

## Seen in the notes

No items. This section is meant to rest on a marker each numeric fact should carry, saying whether its element sat inside a note when it was extracted. No fact in the parts of input_numbers.json I read carries one.

The fields printed on every fact are id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession and filing_date. Some facts also have superseded_by, and some have a typed_segment inside context. Facts that plainly come from note tables print exactly the same fields as facts on the face of the statements, for example:
- the share-based compensation split by income-statement line;
- the unrecognized-tax-benefit rollforward;
- income taxes paid by jurisdiction;
- the subsequent-event guarantee.

I do not judge which facts came from notes. Every numeric-fact item above sits under "Seen in the statements" by default, not because it was found to come from a statement face. Those items are the ones whose paragraph_id contains ":facts:". The missing marker is a defect in the input for the later split to fix, not a finding about AMD.
