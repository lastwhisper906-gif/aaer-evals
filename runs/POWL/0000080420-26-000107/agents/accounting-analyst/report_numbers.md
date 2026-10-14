<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Numbers report: POWL (Powell Industries, Inc.), 10-Q 0000080420-26-000107, quarter ended 2026-06-30

**Input check.** My directory holds four files: input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. None of them contains prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. The run is not broken.

**What the input reaches, and what it does not**

- **Trend table coverage.**
  - It holds every requested period: 8 quarters, from quarters-back-0 (2026-04-01..2026-06-30) back to quarters-back-7 (2024-07-01..2024-09-30), and 5 fiscal years, from years-back-0 (2024-10-01..2025-09-30) back to years-back-4.
  - Its coverage prints `"periods_on_record": 13`, and every period prints `"status": "filled"`.
  - No requested period lies beyond the record, so there is no unreached-period statement to make. `"record_predates_the_trigger"` is `null`.
- **Missing sections.**
  - My input has no articulation-check section, no restatement-trace section and no fourth-quarter derivation.
  - With no articulation check, there is no articulation gap I can quote, and none is reported.
  - With no fourth-quarter derivation, a fiscal-fourth-quarter cost of revenue, gross margin or days of inventory does not exist here (see the two unfilled-cell items).
- **Where the restated values come from.**
  - The restated prior values below are taken from the numeric facts. In each case a later filing prints a different value, for the same concept and date, from the 10-K (0000080420-25-000152) or the prior 10-Q (0000080420-26-000070).
  - In my input every such difference falls on share counts, per-share amounts and RSU counts and values. The 10-Q's split-ratio fact and the release attribute them to the three-for-one split of 2026-04-02.
  - Checking whether each new value is three times the old one is arithmetic, and I have not done it.
- **Re-reported unchanged, so not restatements.** These values are re-reported in later filings with identical values:
  - assets, receivables, inventory, contract liabilities, cash, PP&E and stockholders' equity at 2025-09-30;
  - comparative-quarter revenue and net income;
  - stockholders' equity at 2024-09-30.
- **Prior predictions.** The file reads "None on record." Nothing is carried forward.
- **The R&D capitalisation block cannot be quoted.**
  - The `research_and_development_capitalized` block under years-back-0 prints no paragraph_id, so it is recorded here and not as an item.
  - Its printed values:
    - `book_value_with_rnd_capitalized` 667170800.0
    - `earnings_with_rnd_capitalized` 184646000.0
    - `research_and_development_amortization` 7109000.0
    - `research_and_development_asset` 26400800.0
  - `capitalized_development_cost` is missing, because no CapitalizedComputerSoftwareAdditions fact exists in any period. So `capitalized_over_expense` is insufficient.
- **8-K lines that cannot be quoted.** The 8-K's item-code history lists:
  - earlier Item 4.02 (non-reliance) filings on 2011-11-08, 2007-05-21 and 2007-04-16;
  - an NT 10-Q on 2007-05-11;
  - an Item 5.02 on 2026-07-06.

  Those lines print no paragraph id, so they are recorded here and not as items.
- **Note marker.** No numeric fact in my input carries a field saying whether its element sat inside a note (see the second heading).

**How two fields are used**

- `expected_direction` is the sign of the change printed on, or shown by, the quoted row and its cell:
  - `up` or `down` for a single clear sign;
  - `none` where no change is printed, where the quarter-over-quarter and year-over-year signs disagree, or where the metric is insufficient.

  It is not a forecast.
- `horizon` names the comparison window that change spans.

Every number in `what_changed` is copied from my input. Where a number I would want is not there, the text says it does not exist.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_trend",
  "what_changed": "insufficient. accruals_over_total_assets has no value in quarters-back-0 (2026-04-01..2026-06-30) because the record holds no operating cash flow for that three-month period. Both its quarter-over-quarter and year-over-year rows print that the metric is not filled in quarters-back-0. The table fills this ratio in only 2 of its 8 quarters: quarters-back-2 at -0.002054153630223106 (highest of the 2 filled quarters) and quarters-back-6 at -0.0025299257676609965. Two quarters do not support a quarterly accruals trend. The 10-Q prints operating cash flow only for nine months: 195038000 for 2025-10-01..2026-06-30 against 106862000 for 2024-10-01..2025-06-30. A three-month operating cash flow does not exist in my input.",
  "account": "accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000080420-26-000107:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
  "what_changed": "bad_debt_reserve_ratio is 0.001198852408866547 in quarters-back-0. Change -0.00010444228659832271 against quarters-back-1 and -7.066224954434155e-05 against quarters-back-4. Position: lowest of the 8 filled quarters. Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 435000.0 and AccountsReceivableNetCurrent 362412000.0 at 2026-06-30; the quarters-back-1 inputs were 311000.0 and 238315000.0. The reserve ratio sits at the bottom of its filed history in the same quarter that receivables_over_revenue and days_sales_outstanding sit at the top of theirs.",
  "account": "allowance for doubtful accounts against trade receivables",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 8 filled quarters\"",
  "paragraph_id": "0000080420-26-000107:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
  "what_changed": "contract_liabilities_over_revenue is 1.495996663886572 in quarters-back-0. Change 0.4356794176245826 against quarters-back-1 and 0.44975059806827966 against quarters-back-4. Position: highest of the 6 filled quarters on the same concepts. The 2 other filled quarters (quarters-back-3 and quarters-back-7) rest on a different revenue concept and are not compared. Inputs: ContractWithCustomerLiabilityCurrent 466362000.0 at 2026-06-30 against quarterly revenue 311740000.0; the quarters-back-1 inputs were 314506000.0 and 296615000.0.",
  "account": "contract liabilities (billings in excess) against quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
  "what_changed": "days_sales_of_inventory is 40.0975831750916 in quarters-back-0. Change 2.876013203987654 against quarters-back-1 and -0.5155717746497999 against quarters-back-4. Position: second lowest of the 6 filled quarters; quarters-back-3 and quarters-back-7 are unfilled (see the unfilled-cell item). Inputs: InventoryNet 95371000.0 at 2026-06-30 and CostOfGoodsAndServicesSold 216441000.0 for the quarter. The two printed changes disagree in sign.",
  "account": "inventory against quarterly cost of goods sold",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
  "what_changed": "days_sales_outstanding is 105.79165971643035 in quarters-back-0. Change 33.481257342983284 against quarters-back-1 and 38.521281441147664 against quarters-back-4. Position: highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different revenue concept and are not compared. Inputs: AccountsReceivableNetCurrent 362412000.0 at 2026-06-30 against quarterly revenue 311740000.0; the quarters-back-1 receivables input was 238315000.0. The cash-flow statement prints IncreaseDecreaseInAccountsReceivable of 146438000 for the nine months (see the receivables-build item).",
  "account": "trade receivables against quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend",
  "what_changed": "gross_margin is 0.3057002630397126 in quarters-back-0. Change 0.009235148328723575 against quarters-back-1 and -0.001345808367650303 against quarters-back-4. Position: second highest of the 6 filled quarters; the fiscal-fourth quarters quarters-back-3 and quarters-back-7 are unfilled. Inputs: revenue 311740000.0 and CostOfGoodsAndServicesSold 216441000.0. The two printed changes disagree in sign. The release prints 30.6% against 30.7% a year earlier and 29.6% in the second quarter, which carry the same two signs.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000080420-26-000107:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend",
  "what_changed": "inventory_reserve_ratio is 0.0940956894653511 in quarters-back-0. Change -0.0059460235491094054 against quarters-back-1 and 0.004469105328183454 against quarters-back-4. Position: fourth highest of the 8 filled quarters. Inputs: InventoryValuationReserves 8974000.0 and InventoryNet 95371000.0 at 2026-06-30, against 8246000.0 and 84719000.0 at 2025-09-30. The two printed changes disagree in sign.",
  "account": "excess and obsolete inventory reserve",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"fourth highest of the 8 filled quarters\"",
  "paragraph_id": "0000080420-26-000107:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend",
  "what_changed": "insufficient. non_gaap_gap has no value in quarters-back-0, and none in any of the 13 periods, because no us-gaap concept carries a non-GAAP measure. The earnings release in my input prints GAAP revenue, gross profit, net income and EPS, plus the operating measures new orders and backlog. It prints no adjusted-earnings figure, so neither source gives a gap to measure.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000080420-26-000107:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
  "what_changed": "receivables_over_revenue is 1.1625457111695643 in quarters-back-0. Change 0.3590967959090414 against quarters-back-1 and 0.4233107850675568 against quarters-back-4. Position: highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different revenue concept and are not compared. Inputs: AccountsReceivableNetCurrent 362412000.0 at 2026-06-30 against quarterly revenue 311740000.0.",
  "account": "trade receivables against quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend",
  "what_changed": "soft_asset_share is 0.4652761289203511 in quarters-back-0. Change 0.01571047897149347 against quarters-back-1 and -0.0474525185001452 against quarters-back-4. Position: third lowest of the 8 filled quarters. Inputs: Assets 1406698000.0, CashAndCashEquivalentsAtCarryingValue 633561000.0 and PropertyPlantAndEquipmentNet 118634000.0 at 2026-06-30. The two printed changes disagree in sign.",
  "account": "assets other than cash and PP&E over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"third lowest of the 8 filled quarters\"",
  "paragraph_id": "0000080420-26-000107:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend",
  "what_changed": "insufficient. warranty_reserve_ratio has no value in quarters-back-0, and the table fills it in none of its 13 periods. It looks for StandardProductWarrantyAccrual, ProductWarrantyAccrual and StandardProductWarrantyAccrualCurrent. The 10-Q tags the warranty accrual as ProductWarrantyAccrualClassifiedCurrent (6595000 at 2026-06-30), a concept the table does not read. See the warranty-accrual item for the printed balances and roll-forward.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000080420-26-000107:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend",
  "what_changed": "accruals_over_total_assets is 0.011551113451591728 for years-back-0 (fiscal year 2024-10-01..2025-09-30). Change -0.032822822638390814 against years-back-1. Position: second lowest of the 5 filled years. Inputs: NetIncomeLoss 180747000.0 and NetCashProvidedByUsedInOperatingActivities 167937000.0 (both from 10-K 0000080420-25-000152), and Assets 1108984000.0 at 2025-09-30. The quarterly measure is not filled for the latest quarter (see the quarterly accruals item).",
  "account": "accruals (net income less operating cash flow) over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:accruals_over_total_assets:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
  "what_changed": "bad_debt_reserve_ratio is 0.001692475383221498 for years-back-0. Change -0.00023472844884177388 against years-back-1. Position: second lowest of the 5 filled years. Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 368000.0 and AccountsReceivableNetCurrent 217065000.0 at 2025-09-30.",
  "account": "allowance for doubtful accounts against trade receivables",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:bad_debt_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
  "what_changed": "contract_liabilities_over_revenue is 0.2698036254050011 for years-back-0. Change -0.014447171745408438 against years-back-1. Position: third highest of the 5 filled years. Inputs: ContractWithCustomerLiabilityCurrent 297949000.0 at 2025-09-30 against annual revenue 1104318000.0.",
  "account": "contract liabilities against annual revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:contract_liabilities_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend",
  "what_changed": "days_sales_of_inventory is 39.647349721836505 for years-back-0. Change -2.8670266612884205 against years-back-1. Position: second lowest of the 5 filled years. Inputs: InventoryNet 84719000.0 at 2025-09-30 and annual CostOfGoodsAndServicesSold 779937000.0.",
  "account": "inventory against annual cost of goods sold",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_of_inventory:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend",
  "what_changed": "days_sales_outstanding is 71.7444839258257 for years-back-0. Change -5.76997739015404 against years-back-1. Position: second lowest of the 5 filled years. Inputs: AccountsReceivableNetCurrent 217065000.0 at 2025-09-30 against annual revenue 1104318000.0.",
  "account": "trade receivables against annual revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_outstanding:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend",
  "what_changed": "gross_margin is 0.293738760031078 for years-back-0. Change 0.023983851678680224 against years-back-1. Position: highest of the 5 filled years. Inputs: annual revenue 1104318000.0 and CostOfGoodsAndServicesSold 779937000.0.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:gross_margin:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend",
  "what_changed": "inventory_reserve_ratio is 0.0973335379312787 for years-back-0. Change 0.011613928740962773 against years-back-1. Position: third highest of the 5 filled years. Inputs: InventoryValuationReserves 8246000.0 and InventoryNet 84719000.0 at 2025-09-30.",
  "account": "excess and obsolete inventory reserve",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:inventory_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend",
  "what_changed": "insufficient. non_gaap_gap has no value for years-back-0, and none in any of the 5 years, because no us-gaap concept carries a non-GAAP measure.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000080420-26-000107:trends:non_gaap_gap:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend",
  "what_changed": "receivables_over_revenue is 0.19656022993376907 for years-back-0. Change -0.015227915738306758 against years-back-1. Position: second lowest of the 5 filled years. Inputs: AccountsReceivableNetCurrent 217065000.0 at 2025-09-30 against annual revenue 1104318000.0.",
  "account": "trade receivables against annual revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:receivables_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend",
  "what_changed": "soft_asset_share is 0.49342100517230186 for years-back-0. Change -0.055425123811300436 against years-back-1. Position: second lowest of the 5 filled years. Inputs: Assets 1108984000.0, CashAndCashEquivalentsAtCarryingValue 450739000.0 and PropertyPlantAndEquipmentNet 111049000.0 at 2025-09-30.",
  "account": "assets other than cash and PP&E over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000080420-26-000107:trends:soft_asset_share:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend",
  "what_changed": "insufficient. warranty_reserve_ratio has no value for years-back-0, and none in any of the 5 years, because the table does not read the concept the company uses, ProductWarrantyAccrualClassifiedCurrent. The 10-Q prints 6356000 for that concept at 2025-09-30.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-09-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000080420-26-000107:trends:warranty_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_unfilled_in_most_quarters",
  "what_changed": "insufficient. Besides quarters-back-0, the table cannot fill accruals_over_total_assets in quarters-back-1, -3, -4, -5 and -7, each for want of a three-month operating cash flow. It is filled only in quarters-back-2 and quarters-back-6, both October-to-December quarters, where the fiscal year-to-date cash flow covers that one quarter. The record therefore has no quarterly accruals history beyond 2 points.",
  "account": "operating cash flow by quarter",
  "expected_direction": "none",
  "horizon": "the 8 quarters of the trend table",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-01..2026-03-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000080420-26-000107:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_unfilled_where_only_annual_cost_is_filed",
  "what_changed": "insufficient. gross_margin is unfilled in quarters-back-3 (2025-07-01..2025-09-30) and quarters-back-7 (2024-07-01..2024-09-30): the record holds no cost of revenue for either three-month period. Both are fiscal fourth quarters, which reach the record only inside the annual 10-K. My input has no fourth-quarter derivation, so a fourth-quarter gross margin does not exist here, and the quarterly gross-margin history rests on 6 quarters.",
  "account": "cost of goods sold by quarter",
  "expected_direction": "none",
  "horizon": "the fiscal fourth quarters in the trend table",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2025-07-01..2025-09-30: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0000080420-26-000107:trends:gross_margin:2025-07-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_unfilled_where_only_annual_cost_is_filed",
  "what_changed": "insufficient. days_sales_of_inventory is unfilled in quarters-back-3 and quarters-back-7 for the same reason as gross margin: no three-month cost of revenue exists for either fiscal fourth quarter. The quarterly history rests on 6 quarters.",
  "account": "inventory against cost of goods sold by quarter",
  "expected_direction": "none",
  "horizon": "the fiscal fourth quarters in the trend table",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2025-07-01..2025-09-30: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_of_inventory:2025-07-01..2025-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_contract_liabilities_recent",
  "what_changed": "change of concept. In quarters-back-3 (2025-07-01..2025-09-30), contract_liabilities_over_revenue rests on revenue tagged RevenueFromContractWithCustomerIncludingAssessedTax: 297983000.0, from 10-K 0000080420-25-000152. Every non-fourth quarter in the table uses RevenueFromContractWithCustomerExcludingAssessedTax. For this reason the table refuses the quarter-over-quarter comparison from quarters-back-2 into this quarter and from this quarter to quarters-back-4. Value 0.9998858995311813. Its position is among only 2 quarters on that concept, which is insufficient for a trend on either concept.",
  "account": "revenue concept under contract_liabilities_over_revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-3 against its neighbouring quarters",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:contract_liabilities_over_revenue:2025-07-01..2025-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_contract_liabilities_older",
  "what_changed": "change of concept. In quarters-back-7 (2024-07-01..2024-09-30), contract_liabilities_over_revenue rests on revenue tagged RevenueFromContractWithCustomerIncludingAssessedTax: 275063000.0, from 10-K 0000080420-25-000152. The table refuses the quarter-over-quarter comparison from quarters-back-6 into this quarter. Value 1.0461712407702963. Two quarters on that concept are insufficient for a trend.",
  "account": "revenue concept under contract_liabilities_over_revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-7 against quarters-back-6",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:contract_liabilities_over_revenue:2024-07-01..2024-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_days_sales_outstanding_recent",
  "what_changed": "change of concept. In quarters-back-3, days_sales_outstanding rests on RevenueFromContractWithCustomerIncludingAssessedTax (297983000.0), while the other non-fourth quarters rest on RevenueFromContractWithCustomerExcludingAssessedTax. The quarter-over-quarter comparisons into and out of quarters-back-3 are refused. Value 67.01717883234949. Its year-over-year change against quarters-back-7, on the same concept, is printed as -4.694610830382331. Two quarters on that concept are insufficient for a trend.",
  "account": "revenue concept under days_sales_outstanding",
  "expected_direction": "none",
  "horizon": "quarters-back-3 against its neighbouring quarters",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_outstanding:2025-07-01..2025-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_days_sales_outstanding_older",
  "what_changed": "change of concept. In quarters-back-7, days_sales_outstanding rests on RevenueFromContractWithCustomerIncludingAssessedTax (275063000.0). The comparison from quarters-back-6 into this quarter is refused. Value 71.71178966273182. Two quarters on that concept are insufficient for a trend.",
  "account": "revenue concept under days_sales_outstanding",
  "expected_direction": "none",
  "horizon": "quarters-back-7 against quarters-back-6",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:days_sales_outstanding:2024-07-01..2024-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_receivables_over_revenue_recent",
  "what_changed": "change of concept. In quarters-back-3, receivables_over_revenue rests on RevenueFromContractWithCustomerIncludingAssessedTax (297983000.0). The quarter-over-quarter comparisons into and out of quarters-back-3 are refused. Value 0.7284475960037988. Its year-over-year change against quarters-back-7, on the same concept, is printed as -0.0510283785911122. Two quarters on that concept are insufficient for a trend.",
  "account": "revenue concept under receivables_over_revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-3 against its neighbouring quarters",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:receivables_over_revenue:2025-07-01..2025-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_receivables_over_revenue_older",
  "what_changed": "change of concept. In quarters-back-7, receivables_over_revenue rests on RevenueFromContractWithCustomerIncludingAssessedTax (275063000.0). The comparison from quarters-back-6 into this quarter is refused. Value 0.779475974594911. Two quarters on that concept are insufficient for a trend.",
  "account": "revenue concept under receivables_over_revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-7 against quarters-back-6",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0000080420-26-000107:trends:receivables_over_revenue:2024-07-01..2024-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_shares_outstanding_restated_for_split",
  "what_changed": "restated prior value. The 10-K (0000080420-25-000152, filed 2025-11-19) printed 12070178 shares outstanding at 2025-09-30. The prior 10-Q (0000080420-26-000070) and this 10-Q (0000080420-26-000107:facts:CommonStockSharesOutstanding:2025-09-30) print 36210534 for the same date. This 10-Q carries a stock-split conversion ratio of 3 dated 2026-04-02 (0000080420-26-000107:facts:StockholdersEquityNoteStockSplitConversionRatio1:2026-04-02..2026-04-02). The release footnote says share amounts for all periods were retroactively adjusted. No restatement trace in my input ties the two values, and the multiplication check is not done here.",
  "account": "common shares outstanding",
  "expected_direction": "up",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in the 10-Qs of 2026-05-05 and 2026-08-04",
  "quote": "\"value\": \"12070178\"",
  "paragraph_id": "0000080420-25-000152:facts:CommonStockSharesOutstanding:2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_shares_issued_restated_for_split",
  "what_changed": "restated prior value. This 10-Q prints 38628588 shares issued at 2025-09-30; the 10-K printed 12876196 for the same date. The release attributes the difference to the retroactive three-for-one split adjustment.",
  "account": "common shares issued",
  "expected_direction": "up",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in this 10-Q",
  "quote": "\"value\": \"38628588\"",
  "paragraph_id": "0000080420-26-000107:facts:CommonStockSharesIssued:2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_shares_authorized_restated_for_split",
  "what_changed": "restated prior value. This 10-Q prints 90000000 authorized shares at 2025-09-30; the 10-K printed 30000000 for the same date. The release says the split proportionately increased authorized common stock from 30,000,000 to 90,000,000 on April 2, 2026, so the 2025-09-30 figure is presented on the post-split basis.",
  "account": "common shares authorized",
  "expected_direction": "up",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in this 10-Q",
  "quote": "\"value\": \"90000000\"",
  "paragraph_id": "0000080420-26-000107:facts:CommonStockSharesAuthorized:2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_treasury_shares_restated_for_split",
  "what_changed": "restated prior value. This 10-Q prints 2418054 treasury shares at 2025-09-30; the 10-K printed 806018 for the same date. The treasury stock carrying value is unchanged at 24999000 in both filings (see the treasury-value tag item).",
  "account": "treasury shares",
  "expected_direction": "up",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in this 10-Q",
  "quote": "\"value\": \"2418054\"",
  "paragraph_id": "0000080420-26-000107:facts:TreasuryStockCommonShares:2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_equity_statement_shares_restated_for_split",
  "what_changed": "restated prior value. In the statement of equity, the 10-K printed 12876000 common shares (CommonStockMember) at 2025-09-30. This 10-Q prints 38629000 for the same date and component (0000080420-26-000107:facts:CommonStockSharesOutstanding:2025-09-30:us-gaap:StatementEquityComponentsAxis=us-gaap:CommonStockMember). The common-stock dollar component stayed at 129000 at that date.",
  "account": "common shares in the statement of stockholders' equity",
  "expected_direction": "up",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in this 10-Q",
  "quote": "\"value\": \"12876000\"",
  "paragraph_id": "0000080420-25-000152:facts:CommonStockSharesOutstanding:2025-09-30:us-gaap:StatementEquityComponentsAxis=us-gaap:CommonStockMember" }
```

```json
{ "id": "articulation_and_the_filed_history_equity_statement_opening_shares_restated_for_split",
  "what_changed": "restated prior value. In the statement of equity, this 10-Q prints 38386000 common shares (CommonStockMember) at 2024-09-30, where the 10-K printed 12795000. The treasury-share component at 2024-09-30 likewise moved from 806000 in the 10-K to 2418000 in this 10-Q; I hold that row's value but not its printed id, so it is not quoted separately. Stockholders' equity at 2024-09-30 is unchanged at 483073000.",
  "account": "opening common and treasury shares in the statement of stockholders' equity",
  "expected_direction": "up",
  "horizon": "2024-09-30 as filed in the 10-K against the same date as filed in this 10-Q",
  "quote": "\"value\": \"38386000\"",
  "paragraph_id": "0000080420-26-000107:facts:CommonStockSharesOutstanding:2024-09-30:us-gaap:StatementEquityComponentsAxis=us-gaap:CommonStockMember" }
```

```json
{ "id": "articulation_and_the_filed_history_basic_eps_comparative_restated_for_split",
  "what_changed": "restated prior value. The 10-K printed basic EPS of 4.00 for 2025-04-01..2025-06-30. This 10-Q prints 1.33 for the same quarter (0000080420-26-000107:facts:EarningsPerShareBasic:2025-04-01..2025-06-30), and the release prints $1.33 basic for that comparative quarter. Net income for the quarter is re-reported unchanged at 48234000, so the difference sits in the share denominator, which the release attributes to the split.",
  "account": "basic earnings per share",
  "expected_direction": "down",
  "horizon": "quarter 2025-04-01..2025-06-30 as filed in the 10-K against this 10-Q",
  "quote": "\"value\": \"4.00\"",
  "paragraph_id": "0000080420-25-000152:facts:EarningsPerShareBasic:2025-04-01..2025-06-30" }
```

```json
{ "id": "articulation_and_the_filed_history_diluted_eps_comparative_restated_for_split",
  "what_changed": "restated prior value. This 10-Q prints diluted EPS of 1.32 for 2025-04-01..2025-06-30; the 10-K printed 3.96 for the same quarter. Diluted weighted shares for that quarter print as 36525000 in this 10-Q.",
  "account": "diluted earnings per share",
  "expected_direction": "down",
  "horizon": "quarter 2025-04-01..2025-06-30 as filed in the 10-K against this 10-Q",
  "quote": "\"value\": \"1.32\"",
  "paragraph_id": "0000080420-26-000107:facts:EarningsPerShareDiluted:2025-04-01..2025-06-30" }
```

```json
{ "id": "articulation_and_the_filed_history_basic_eps_earlier_comparative_restated_for_split",
  "what_changed": "restated prior value. The prior 10-Q (0000080420-26-000070) prints basic EPS of 1.28 for 2025-01-01..2025-03-31; the 10-K printed 3.84 for that quarter, and its fact is marked superseded by the prior 10-Q.",
  "account": "basic earnings per share",
  "expected_direction": "down",
  "horizon": "quarter 2025-01-01..2025-03-31 as filed in the 10-K against the 10-Q of 2026-05-05",
  "quote": "\"value\": \"1.28\"",
  "paragraph_id": "0000080420-26-000070:facts:EarningsPerShareBasic:2025-01-01..2025-03-31" }
```

```json
{ "id": "articulation_and_the_filed_history_diluted_eps_earlier_comparative_restated_for_split",
  "what_changed": "restated prior value. The prior 10-Q prints diluted EPS of 1.27 for 2025-01-01..2025-03-31; the 10-K printed 3.81 for that quarter.",
  "account": "diluted earnings per share",
  "expected_direction": "down",
  "horizon": "quarter 2025-01-01..2025-03-31 as filed in the 10-K against the 10-Q of 2026-05-05",
  "quote": "\"value\": \"1.27\"",
  "paragraph_id": "0000080420-26-000070:facts:EarningsPerShareDiluted:2025-01-01..2025-03-31" }
```

```json
{ "id": "articulation_and_the_filed_history_rsu_nonvested_count_restated_for_split",
  "what_changed": "restated prior value. The 10-K printed 116886 nonvested RSUs at 2025-09-30. The prior 10-Q and this 10-Q print 350658 for the same date. This 10-Q's roll-forward for the nine months prints 60590 granted, 245130 vested, 0 forfeited and 166118 nonvested at 2026-06-30.",
  "account": "nonvested restricted stock units",
  "expected_direction": "up",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in the 10-Qs",
  "quote": "\"value\": \"116886\"",
  "paragraph_id": "0000080420-25-000152:facts:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedNumber:2025-09-30:us-gaap:AwardTypeAxis=us-gaap:RestrictedStockUnitsRSUMember" }
```

```json
{ "id": "articulation_and_the_filed_history_rsu_grant_date_value_restated_for_split",
  "what_changed": "restated prior value. This 10-Q prints a weighted-average grant-date fair value of 21.60 for nonvested RSUs at 2025-09-30; the 10-K printed 64.79 for the same date. In the same roll-forward this 10-Q prints 100.40 for grants and 12.96 for vestings in the nine months, and 63.02 for the nonvested balance at 2026-06-30. Separately, it prints 4200 restricted shares issued to non-employee directors in February 2026 at a price per share of 184.83. My input does not say whether that price is on the pre-split or post-split basis.",
  "account": "RSU weighted-average grant-date fair value",
  "expected_direction": "down",
  "horizon": "2025-09-30 as filed in the 10-K against the same date as filed in this 10-Q",
  "quote": "\"value\": \"21.60\"",
  "paragraph_id": "0000080420-26-000107:facts:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedWeightedAverageGrantDateFairValue:2025-09-30:us-gaap:AwardTypeAxis=us-gaap:RestrictedStockUnitsRSUMember" }
```

```json
{ "id": "structure_and_disclosure_changes_treasury_stock_value_concept",
  "what_changed": "change of tag, not flagged by the input. The 10-K tagged treasury stock at cost at 2025-09-30 as TreasuryStockValue (24999000). This 10-Q tags the same date as TreasuryStockCommonValue, with the same value 24999000. No trend metric reads either tag, and the value did not change.",
  "account": "treasury stock at cost",
  "expected_direction": "none",
  "horizon": "2025-09-30 as filed in the 10-K against this 10-Q",
  "quote": "\"tag\": \"TreasuryStockCommonValue\"",
  "paragraph_id": "0000080420-26-000107:facts:TreasuryStockCommonValue:2025-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_authorized_shares_instants_within_filing",
  "what_changed": "This 10-Q prints CommonStockSharesAuthorized as 30000000 at 2026-03-30 and 2026-04-01, and as 90000000 at 2026-03-31, 2026-04-02 and 2025-09-30. The 2026-03-31 and 2025-09-30 figures follow the retroactive split presentation; the 2026-03-30 and 2026-04-01 figures are the pre-split count. Read by date alone, the authorized count falls and rises again across consecutive days within one filing.",
  "account": "common shares authorized",
  "expected_direction": "none",
  "horizon": "instants around the 2026-04-02 split within this 10-Q",
  "quote": "\"value\": \"30000000\"",
  "paragraph_id": "0000080420-26-000107:facts:CommonStockSharesAuthorized:2026-04-01" }
```

```json
{ "id": "structure_and_disclosure_changes_split_booked_as_par_transfer",
  "what_changed": "In the quarter of the split, StockIssuedDuringPeriodValueNewIssues prints 259000 in the common-stock component, -259000 in additional paid-in capital, and 0 in total. The common-stock dollar component is 388000 at 2026-06-30 against 129000 at 2026-03-31. The split was booked as a par-value transfer out of APIC under a new-issues tag, with no printed effect on total equity (756184000 at 2026-06-30).",
  "account": "common stock par value and additional paid-in capital",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"-259000\"",
  "paragraph_id": "0000080420-26-000107:facts:StockIssuedDuringPeriodValueNewIssues:2026-04-01..2026-06-30:us-gaap:StatementEquityComponentsAxis=us-gaap:AdditionalPaidInCapitalMember" }
```

```json
{ "id": "structure_and_disclosure_changes_single_reportable_segment_expense_rows",
  "what_changed": "The company reports one reportable segment. For the quarter the segment rows give: revenue 311740000; cost of goods sold 216441000; general and administrative 18223000 (17242000 a year earlier); selling and marketing 8742000 (7667000); research and development 4300000; amortization of intangibles 221000; segment OperatingExpenses 247664000 (226149000). My input has no articulation check tying these rows to the income-statement lines; the release prints SG&A of 26,702 thousand for the quarter. Whether they tie is not computed here.",
  "account": "segment expense disclosure",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against the quarter ended 2025-06-30",
  "quote": "\"value\": \"1\"",
  "paragraph_id": "0000080420-26-000107:facts:NumberOfReportableSegments:2025-10-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_build_in_operating_cash_flow",
  "what_changed": "IncreaseDecreaseInAccountsReceivable is 146438000 for the nine months 2025-10-01..2026-06-30, against -2747000 for 2024-10-01..2025-06-30. Under this element a positive value is an increase in receivables. AccountsReceivableNetCurrent is 362412000.0 at 2026-06-30 against 217065000.0 at 2025-09-30 and 238315000.0 at 2026-03-31 (trend-cell inputs). In the same quarter, days_sales_outstanding and receivables_over_revenue are the highest of their 6 comparable quarters and bad_debt_reserve_ratio is the lowest of 8.",
  "account": "trade receivables",
  "expected_direction": "up",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"146438000\"",
  "paragraph_id": "0000080420-26-000107:facts:IncreaseDecreaseInAccountsReceivable:2025-10-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_assets_balance",
  "what_changed": "ContractWithCustomerAssetNetCurrent (unbilled, over-time revenue) is 116002000 at 2026-06-30 against 136679000 at 2025-09-30. Over the same span the 10-Q prints billed receivables of 362412000.0 against 217065000.0 and contract liabilities of 466362000 against 297949000. Contract receivables after allowance print 6000000.0 at 2026-06-30 (5800000 current, 200000 noncurrent) against 8100000 at 2025-09-30.",
  "account": "contract assets",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"116002000\"",
  "paragraph_id": "0000080420-26-000107:facts:ContractWithCustomerAssetNetCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized",
  "what_changed": "ContractWithCustomerLiabilityRevenueRecognized is 243700000 for the nine months to 2026-06-30: revenue recognized in the period out of contract liabilities. No prior-year nine-month comparative is in my input. Contract liabilities are 466362000 at 2026-06-30 against 297949000 at 2025-09-30.",
  "account": "contract liabilities",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30",
  "quote": "\"value\": \"243700000\"",
  "paragraph_id": "0000080420-26-000107:facts:ContractWithCustomerLiabilityRevenueRecognized:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_cumulative_catch_up_on_contract_assets",
  "what_changed": "ContractWithCustomerAssetCumulativeCatchUpAdjustmentToRevenueChangeInMeasureOfProgress is 12800000 for the nine months to 2026-06-30 against 15100000 for the nine months to 2025-06-30. The prior 10-Q printed 14200000 for the six months to 2026-03-31 (8800000 a year earlier). The 10-K printed 19200000 for fiscal 2025 (16900000 for fiscal 2024). A three-month catch-up figure for the latest quarter does not exist in my input and is not derived here. These are estimate revisions on over-time contracts, which supply 0.97 of the quarter's revenue.",
  "account": "cumulative catch-up adjustments to revenue (contract assets)",
  "expected_direction": "down",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"12800000\"",
  "paragraph_id": "0000080420-26-000107:facts:ContractWithCustomerAssetCumulativeCatchUpAdjustmentToRevenueChangeInMeasureOfProgress:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_cumulative_catch_up_on_contract_liabilities",
  "what_changed": "ContractWithCustomerLiabilityCumulativeCatchUpAdjustmentToRevenueChangeInMeasureOfProgress is -5100000 for the nine months to 2026-06-30. The prior 10-Q printed -3800000 for the six months to 2026-03-31. No prior-year nine-month comparative is in my input, and a three-month figure does not exist.",
  "account": "cumulative catch-up adjustments to revenue (contract liabilities)",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30",
  "quote": "\"value\": \"-5100000\"",
  "paragraph_id": "0000080420-26-000107:facts:ContractWithCustomerLiabilityCumulativeCatchUpAdjustmentToRevenueChangeInMeasureOfProgress:2025-10-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_share_recognized_over_time",
  "what_changed": "Revenue transferred over time is 0.97 of revenue for 2026-04-01..2026-06-30, against 0.95 for 2025-04-01..2025-06-30, and 0.96 for both nine-month periods. Revenue at a point in time is 0.03 against 0.05 for the quarter. Nearly all revenue rests on measure-of-progress estimates.",
  "account": "revenue recognized over time",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"0.97\"",
  "paragraph_id": "0000080420-26-000107:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:ProductConcentrationRiskMember,us-gaap:TimingOfTransferOfGoodOrServiceAxis=us-gaap:TransferredOverTimeMember" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations",
  "what_changed": "RevenueRemainingPerformanceObligation is 2400000000 at 2026-06-30. The prior 10-Q printed 1800000000 at 2026-03-31, and the 10-K printed 1400000000 at 2025-09-30. A typed-dimension fact prints 1300000000 with an expected-satisfaction start date of 2026-07-01; the end of that window is not printed in my input.",
  "account": "remaining performance obligations",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"2400000000\"",
  "paragraph_id": "0000080420-26-000107:facts:RevenueRemainingPerformanceObligation:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_estimate",
  "what_changed": "LossContingencyEstimateOfPossibleLoss is 9300000 at 2026-06-30. The prior 10-Q printed 7500000 at 2026-03-31, and the 10-K printed 4300000 at 2025-09-30. What the contingency is does not appear in my input.",
  "account": "estimated reasonably possible loss on contingencies",
  "expected_direction": "up",
  "horizon": "2025-09-30 to 2026-06-30 across three filings",
  "quote": "\"value\": \"9300000\"",
  "paragraph_id": "0000080420-26-000107:facts:LossContingencyEstimateOfPossibleLoss:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_surety_bonds_outstanding",
  "what_changed": "Surety bonds outstanding (GuaranteeObligationsCurrentCarryingValue, SuretyBondMember) are 492400000 at 2026-06-30. The prior 10-Q printed 432800000 and the 10-K 417300000.",
  "account": "surety bonds",
  "expected_direction": "up",
  "horizon": "2025-09-30 to 2026-06-30 across three filings",
  "quote": "\"value\": \"492400000\"",
  "paragraph_id": "0000080420-26-000107:facts:GuaranteeObligationsCurrentCarryingValue:2026-06-30:us-gaap:GuaranteeObligationsByNatureAxis=us-gaap:SuretyBondMember" }
```

```json
{ "id": "liquidity_and_capital_letters_of_credit_and_facility_headroom",
  "what_changed": "At 2026-06-30, under the domestic credit agreement (maximum 150000000: 100000000 Bank of America and 50000000 Texas Capital Bank), letters of credit outstanding are 103900000, borrowings 0 and remaining capacity 46100000. Under the UK facility (maximum 19900000), guarantees are 5700000 and remaining capacity 14200000. No comparative for these balances appears for this filing in my input.",
  "account": "credit facility usage",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "\"value\": \"46100000\"",
  "paragraph_id": "0000080420-26-000107:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2026-06-30:us-gaap:CreditFacilityAxis=us-gaap:DomesticLineOfCreditMember,us-gaap:DebtInstrumentAxis=powl:AmendedAndRestatedCreditAgreementMember" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_year_to_date",
  "what_changed": "NetCashProvidedByUsedInOperatingActivities is 195038000 for the nine months to 2026-06-30 against 106862000 a year earlier. Nine-month net income is 139437000 against 129327000. The prior 10-Q printed 94811000 for the six months (59480000 a year earlier). Investing cash flow is 14488000 against -4215000; it includes 24857000 of short-term investment maturities and 10386000 of capital expenditure. Financing cash flow is -24490000 against -21670000.",
  "account": "operating cash flow",
  "expected_direction": "up",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"195038000\"",
  "paragraph_id": "0000080420-26-000107:facts:NetCashProvidedByUsedInOperatingActivities:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_cash_balance",
  "what_changed": "Cash, cash equivalents and restricted cash are 633561000 at 2026-06-30, against 450739000 at 2025-09-30 and 398466000 at 2025-06-30. Short-term investments print 0 at 2026-06-30 against 24788000 at 2025-09-30. All of the cash is printed at fair-value Level 1 (633561000), and long-term debt under the credit agreement is 0.",
  "account": "cash and short-term investments",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"633561000\"",
  "paragraph_id": "0000080420-26-000107:facts:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_construction_in_progress",
  "what_changed": "Construction in progress (PropertyPlantAndEquipmentGross, ConstructionInProgressMember) is 13457000 at 2026-06-30 against 2110000 at 2025-09-30. Nine-month capital expenditure is 10386000 against 11380000. Operating lease right-of-use assets are 2524000 against 1664000, and leases not yet commenced total 1976000. The release says the Jacintoport fabrication yard expansion is expected to be completed by the close of Fiscal 2026.",
  "account": "property, plant and equipment under construction",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"13457000\"",
  "paragraph_id": "0000080420-26-000107:facts:PropertyPlantAndEquipmentGross:2026-06-30:us-gaap:PropertyPlantAndEquipmentByTypeAxis=us-gaap:ConstructionInProgressMember" }
```

```json
{ "id": "earnings_quality_deferred_tax_and_tax_accrual_swing",
  "what_changed": "DeferredIncomeTaxExpenseBenefit is 11636000 for the nine months to 2026-06-30 against -2847000 a year earlier. The change in accrued income taxes is -11088000 against -2543000. The effective tax rate prints 0.22 for both nine-month periods and 0.25 for both third quarters. Income tax expense is 38506000 against 36685000 for the nine months.",
  "account": "deferred and accrued income taxes",
  "expected_direction": "up",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"11636000\"",
  "paragraph_id": "0000080420-26-000107:facts:DeferredIncomeTaxExpenseBenefit:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_doubtful_accounts_provision",
  "what_changed": "ProvisionForDoubtfulAccounts is 107000 for the nine months to 2026-06-30 against -149000 a year earlier. The allowance is 435000.0 at 2026-06-30 against 368000.0 at 2025-09-30 (trend-cell inputs), while receivables are 362412000.0 against 217065000.0.",
  "account": "provision for doubtful accounts",
  "expected_direction": "up",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"107000\"",
  "paragraph_id": "0000080420-26-000107:facts:ProvisionForDoubtfulAccounts:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_balance_and_roll_forward",
  "what_changed": "The warranty accrual is tagged ProductWarrantyAccrualClassifiedCurrent. Balances: 6595000 at 2026-06-30, 6637000 at 2026-03-31, 6356000 at 2025-09-30, 6058000 at 2025-06-30, 6284000 at 2025-03-31 and 5822000 at 2024-09-30. Provisions (ProductWarrantyAccrualPeriodIncreaseDecrease) are 1209000 for the quarter against 916000, and 4872000 for the nine months against 3769000. Payments are 1232000 against 1208000 for the quarter, and 4608000 against 3549000 for the nine months. The trend table reads none of this because it looks for other warranty concepts. The balance is printed higher than a year earlier but lower than at 2026-03-31.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "quarter and nine months to 2026-06-30 against the prior-year periods",
  "quote": "\"value\": \"6595000\"",
  "paragraph_id": "0000080420-26-000107:facts:ProductWarrantyAccrualClassifiedCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_remeasured",
  "what_changed": "Level 3 contingent consideration (BusinessCombinationContingentConsiderationLiability) is 2428000 at 2026-06-30, against 2344000 at 2025-09-30. The prior 10-Q printed 2574000 at 2026-03-31, and the 10-K carried 3236000 from the 2025-08-15 Remsdaq acquisition. The remeasurement inputs are not in my input.",
  "account": "contingent consideration liability",
  "expected_direction": "none",
  "horizon": "2025-09-30 to 2026-06-30",
  "quote": "\"value\": \"2428000\"",
  "paragraph_id": "0000080420-26-000107:facts:BusinessCombinationContingentConsiderationLiability:2026-06-30" }
```

```json
{ "id": "earnings_quality_research_and_development_and_operating_expense_rows",
  "what_changed": "Research and development expense is 4300000 for the quarter against 2659000, and 11856000 against 7881000 for the nine months. Amortization of intangible assets is 221000 for the quarter against 0, following the 2025 acquisition. Net finite-lived intangibles are 5397000 at 2026-06-30 against 6138000 at 2025-09-30, and goodwill is 6049000 against 6125000, with a foreign-currency movement of -76000.",
  "account": "research and development and acquisition amortization",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"4300000\"",
  "paragraph_id": "0000080420-26-000107:facts:ResearchAndDevelopmentExpense:2026-04-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=powl:ReportableSegmentMember" }
```

```json
{ "id": "earnings_quality_interest_income_in_pretax_income",
  "what_changed": "Net interest income is 5047000 for the quarter against 3977000, and 13515000 against 11397000 for the nine months. Pre-tax income is 69123000 against 64101000 for the quarter. The release prints operating income of 64,076 against 60,124 thousand.",
  "account": "interest income",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"5047000\"",
  "paragraph_id": "0000080420-26-000107:facts:InterestIncomeExpenseNonoperatingNet:2026-04-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=powl:ReportableSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_petrochemical_revenue",
  "what_changed": "Petrochemical revenue is 18461000 for 2026-04-01..2026-06-30 against 36349000 a year earlier, and 68790000 against 113236000 for the nine months. The release says Petrochemical revenue declined 49%. It also reports a Petrochemical mega order of roughly $75 million won in the quarter.",
  "account": "revenue, Petrochemical market",
  "expected_direction": "down",
  "horizon": "quarter and nine months to 2026-06-30 against the prior-year periods",
  "quote": "\"value\": \"18461000\"",
  "paragraph_id": "0000080420-26-000107:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=powl:PetrochemicalMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_canada_and_smaller_markets_revenue",
  "what_changed": "Revenue attributed to Canada is 24140000 for the quarter against 42611000 a year earlier, and 86422000 against 108275000 for the nine months. Mexico, Central and South America is 713000 against 1881000, and light rail traction power 7961000 against 8549000, for the quarter. Net PP&E in Canada is 31411000 at 2026-06-30 against 32744000 at 2025-09-30.",
  "account": "revenue by geography and smaller markets",
  "expected_direction": "down",
  "horizon": "quarter and nine months to 2026-06-30 against the prior-year periods",
  "quote": "\"value\": \"24140000\"",
  "paragraph_id": "0000080420-26-000107:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:CA" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared",
  "what_changed": "A dividend of 0.09 per share was declared on 2026-08-03 and is tagged as a subsequent event. Dividends paid are 9792000 for the nine months against 9640000.",
  "account": "dividends",
  "expected_direction": "none",
  "horizon": "after 2026-06-30",
  "quote": "\"value\": \"0.09\"",
  "paragraph_id": "0000080420-26-000107:facts:CommonStockDividendsPerShareDeclared:2026-08-03..2026-08-03:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "across_documents_release_gross_margin_matches_facts",
  "what_changed": "The release's gross profit of $95.3 million at 30.6%, against $87.9 million at 30.7%, matches the 10-Q facts. Those print GrossProfit of 95299000 against 87899000, and the trend table prints gross_margin of 0.3057002630397126 with a year-over-year change of -0.001345808367650303. The chief executive calls 30.6% a strong gross margin performance; it is printed just below the prior-year 30.7% and above the 29.6% of the second quarter.",
  "account": "gross profit and gross margin",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "Gross profit of $95.3 million, or 30.6% of revenue, increased 8% compared to $87.9 million, or 30.7% of revenue, in the prior year",
  "paragraph_id": "0000080420-26-000103:8k_2_02:20" }
```

```json
{ "id": "across_documents_release_backlog_and_remaining_performance_obligations",
  "what_changed": "The release gives backlog of $2.4 billion at June 30, 2026, against $1.4 billion a year earlier and $1.8 billion at March 31, 2026. Its footnote defines bookings as additions to backlog (unsatisfied performance obligations). The 10-Q prints RevenueRemainingPerformanceObligation of 2400000000 at 2026-06-30, and the prior 10-Q printed 1800000000. The release's year-earlier comparison is at June 30, 2025, a date for which my input holds no performance-obligation fact; the 10-K's 1400000000 is at 2025-09-30. Release footnote (3) cautions that backlog may not be a reliable indicator of future results.",
  "account": "backlog / remaining performance obligations",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2026-03-31",
  "quote": "Backlog(3) totaled $2.4 billion as of June 30, 2026, an increase of 69% compared to $1.4 billion as of June 30, 2025, and a sequential increase of 35% compared to $1.8 billion as of March 31, 2026.",
  "paragraph_id": "0000080420-26-000103:8k_2_02:22" }
```

```json
{ "id": "across_documents_release_per_share_amounts_split_adjusted",
  "what_changed": "The release prints prior-year-quarter diluted EPS of $1.32, which matches this 10-Q's 1.32 for 2025-04-01..2025-06-30; the 10-K had printed 3.96 diluted and 4.00 basic for that quarter. The release footnote attributes the change to the retroactive split adjustment. Its current-quarter $1.42 diluted matches the 10-Q fact of 1.42.",
  "account": "earnings per share",
  "expected_direction": "none",
  "horizon": "quarter ended 2025-06-30 as filed in the 10-K against the release and this 10-Q",
  "quote": "Share and per-share amounts disclosed for all periods have been retroactively adjusted to reflect the effect of the Stock Split.",
  "paragraph_id": "0000080420-26-000103:8k_2_02:45" }
```

```json
{ "id": "across_documents_release_cash_matches_facts",
  "what_changed": "The release's $634 million of cash and short-term investments matches the 10-Q's cash of 633561000 with short-term investments of 0 at 2026-06-30. The release balance sheet prints 633,561 against 475,527 at September 30, 2025, where the 10-Q prints cash of 450739000 and short-term investments of 24788000.",
  "account": "cash and short-term investments",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "Cash and short-term investments as of June 30, 2026 totaled $634 million",
  "paragraph_id": "0000080420-26-000103:8k_2_02:14" }
```

```json
{ "id": "across_documents_release_end_market_growth",
  "what_changed": "The release attributes growth to Commercial & Other Industrial (grew 54%) and Electric Utility (grew 18%). The 10-Q facts print, for the quarter, Commercial and Other Industrial revenue of 76317000 against 49519000, and revenue tagged ElectricityMember of 88616000 against 74909000. Oil and gas is 106275000 against 105464000, Asia Pacific 11782000 against 1805000, and Middle East and Africa 15875000 against 9917000. The percentages are the release's; I have not recomputed them.",
  "account": "revenue by end market",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "The growth compared to the prior year was driven by higher revenue levels from the Commercial & Other Industrial market, which grew 54%, as well as from the Electric Utility market, which grew 18%.",
  "paragraph_id": "0000080420-26-000103:8k_2_02:19" }
```

```json
{ "id": "across_documents_release_orders_without_a_filed_counterpart",
  "what_changed": "insufficient for a cross-check. New orders of $934 million ($362 million a year earlier, $490 million in the second quarter) and a book-to-bill ratio of 3.0x appear only in the release. No XBRL fact for orders exists in my input, so these company-defined operating measures cannot be tied to filed numbers. The nearest filed figure is the performance-obligation balance.",
  "account": "new orders (bookings)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "New orders(2) totaled $934 million, an increase of 158%",
  "paragraph_id": "0000080420-26-000103:8k_2_02:12" }
```

```json
{ "id": "results_against_expectations_gross_margin_guidance",
  "what_changed": "The chief financial officer expects gross margins to stay consistent with the trailing twelve months. A trailing-twelve-month gross margin does not exist in my input and is not derived here. What the table prints: quarterly gross_margin of 0.3057002630397126 (second highest of 6 filled quarters) and fiscal 2025 gross_margin of 0.293738760031078 (highest of 5 filled years). The table has filled gross margin for neither fiscal fourth quarter it holds, because no three-month cost of revenue exists for them.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "remainder of fiscal 2026, per the release",
  "quote": "We expect that gross margins will maintain levels consistent to the trailing twelve months",
  "paragraph_id": "0000080420-26-000103:8k_2_02:28" }
```

## Seen in the notes

No numeric fact in input_numbers.json carries a field saying whether its element sat inside a note. Each fact row prints id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, on some, superseded_by. Without that marker I could only place an item here by judging where its table sat, and I am told not to make that judgement. No items are written under this heading, and none of the items above has been moved here. If a later input carries the marker, the fact-based items above can be re-sorted by it without re-reading the filings.
