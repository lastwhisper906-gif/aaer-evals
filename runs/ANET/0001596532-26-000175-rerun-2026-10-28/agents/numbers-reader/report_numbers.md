ANET — numbers reader — trigger 0001596532-26-000175 (10-Q, quarter ended 2026-06-30), with 8-K 0001596532-26-000174 (Item 2.02, filed 2026-08-04)

**What the directory holds.** The directory holds four files:
- `input_8k.md`: the earnings release.
- `input_numbers.json`: numeric facts from the 10-K 0001596532-26-000013, the 10-Q 0001596532-26-000078 and the 10-Q 0001596532-26-000175.
- `input_trends.json`: the trend table.
- `input_prior_predictions.md`: "None on record".

Nothing in the directory is a price, an abnormal return, short interest, another company's file, a prior run's probability or an outcome window. The run is not broken on that count.

**What the directory does not hold.** There are no articulation checks, no restatement traces and no fourth-quarter derivation file.
- **Articulation gaps.** None is reported, because Python computed none in this input, and I do not compute one.
- **Restated prior values.** The only one my input states is the 8-K's recast of non-GAAP comparatives (item below).
  - Some numeric facts were re-reported by a later filing (`superseded_by`). Every one I compared prints the same value in the later filing:
    - StockholdersEquity at 2026-03-31 (13487100000) and at 2025-03-31 (10119100000).
    - ContractWithCustomerLiability at 2026-03-31 (6198700000) and at 2025-03-31 (3088800000).
    - The 2025-12-31 balance sheet, as printed by the 10-K, the first-quarter 10-Q and this 10-Q.
  - So no fact item shows a period reported differently. This is my reading of printed values, not a Python trace.
- **Tag changes.** The input prints none. Every cell input I read for quarters-back-0 and years-back-0 rests on the same concept the other periods use.
- **8-K against the 10-Q.** The 8-K's statement tables print the same figures as the 10-Q facts I compared. Examples, in millions: total revenue 3,035.7, net income 1,212.9, total assets 23,720.1, operating cash flow for the six months 2,776.5. I raise no across-documents item.

**Periods the record does not reach.** quarters-back-2 (target 2025-12-30) and quarters-back-6 (target 2024-12-31) have no cells. The reason printed for quarters-back-2 is:

> "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py"

quarters-back-6 prints the same reason with 2024-12-31. The fourth-quarter derivation is not in my input, so no fourth-quarter value appears in this report. The coverage prints 8 quarters and 5 years requested, and 11 periods on record.

**Formula baseline not itemized.** years-back-0 carries a `research_and_development_capitalized` block. It prints:
- book_value_with_rnd_capitalized 15326808000.0
- earnings_with_rnd_capitalized 4018032000.0
- research_and_development_amortization 730668000.0
- research_and_development_asset 2956308000.0
- capitalized_development_cost and capitalized_over_expense: missing, because "the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".

The block prints no `paragraph_id`. I cannot quote it under one, and I do not compose one, so it stays out of the items.

**Conventions used in the items.**
- **expected_direction** is the sign of the printed year-over-year change in the cell: quarters-back-0 against quarters-back-4, or years-back-0 against years-back-1. It is `none` where the cell is insufficient. It records which way the printed number moved; it is not a forecast.
- For 8-K figures and facts, expected_direction records which side of one printed figure another printed figure sits on. No difference is computed.
- **horizon** names the comparison.

## Seen in the statements

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend_cell",
  "what_changed": "Receivables over revenue for quarters-back-0 (2026-04-01..2026-06-30) is printed as 0.7465164541950786 (formula receivables / revenue; AccountsReceivableNetCurrent 2266200000.0 at 2026-06-30 over quarterly revenue 3035700000.0). Printed change: 0.03636510683442895 against quarters-back-1 and 0.010123130537604053 against quarters-back-4. Position as printed: highest of the 6 filled quarters.",
  "account": "Accounts receivable, net, against revenue",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-4 (year over year); quarter over quarter against quarters-back-1 also printed",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend_cell",
  "what_changed": "Days sales outstanding for quarters-back-0 (2026-04-01..2026-06-30, 91 days) is printed as 67.93299733175215 (formula receivables / revenue * days_in_period; receivables 2266200000.0, revenue 3035700000.0). Printed change: 4.019376069293678 against quarters-back-1 and 0.9212048789219693 against quarters-back-4. Position as printed: highest of the 6 filled quarters.",
  "account": "Accounts receivable, net, in days of revenue",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-4 (year over year); quarter over quarter against quarters-back-1 also printed",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend_cell",
  "what_changed": "Contract liabilities over revenue for quarters-back-0 (2026-04-01..2026-06-30) is printed as 1.6802384952399776 (formula contract_liabilities / revenue; the contract-liability input is ContractWithCustomerLiabilityCurrent 5100700000.0 at 2026-06-30, revenue 3035700000.0). Printed change: -0.13205386356400917 against quarters-back-1 and 0.4159061294925175 against quarters-back-4; the two printed changes point in opposite directions. Position as printed: second highest of the 6 filled quarters.",
  "account": "Deferred revenue, current (contract liabilities), against revenue",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-4 (year over year); quarter over quarter against quarters-back-1 also printed",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend_cell",
  "what_changed": "Days sales of inventory for quarters-back-0 (2026-04-01..2026-06-30, 91 days) is printed as 205.00470943664473 (formula inventory / cost_of_revenue * days_in_period; InventoryNet 2535300000.0 at 2026-06-30, cost of revenue 1125400000.0). Printed change: -2.5132134465174545 against quarters-back-1 and -39.55036756674863 against quarters-back-4. Position as printed: lowest of the 6 filled quarters.",
  "account": "Inventories, in days of cost of revenue",
  "expected_direction": "down",
  "horizon": "quarters-back-0 against quarters-back-4 (year over year); quarter over quarter against quarters-back-1 also printed",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend_cell",
  "what_changed": "Gross margin for quarters-back-0 (2026-04-01..2026-06-30) is printed as 0.6292782554270844 (formula (revenue - cost_of_revenue) / revenue; revenue 3035700000.0, cost of revenue 1125400000.0). Printed change: 0.010304464360270105 against quarters-back-1 and -0.0232072307848169 against quarters-back-4; the two printed changes point in opposite directions. Position as printed: second lowest of the 6 filled quarters. The 8-K prints GAAP gross margin of 62.9% against 65.2% for the year-ago quarter (paragraph 0001596532-26-000174:8k_2_02:39).",
  "account": "Gross margin",
  "expected_direction": "down",
  "horizon": "quarters-back-0 against quarters-back-4 (year over year); quarter over quarter against quarters-back-1 also printed",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_quarterly_trend_cell",
  "what_changed": "Soft asset share for quarters-back-0 (2026-04-01..2026-06-30) is printed as 0.8902744929405862 (formula (assets - property_plant_and_equipment - cash) / assets; Assets 23720100000.0, PropertyPlantAndEquipmentNet 312500000.0, CashAndCashEquivalentsAtCarryingValue 2290200000.0, all at 2026-06-30). Printed change: 0.030638817739145563 against quarters-back-1 and 0.03408550284732503 against quarters-back-4. Position as printed: highest of the 6 filled quarters.",
  "account": "Total assets other than property and equipment and cash, as a share of total assets",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-4 (year over year); quarter over quarter against quarters-back-1 also printed",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cell_insufficient",
  "what_changed": "insufficient: accruals over total assets has no value for quarters-back-0. The record holds this filing's operating cash flow only for 2026-01-01..2026-06-30 (six months), not for the quarter, and no quarterly figure is derived here. Across the table the ratio is filled in 7 periods: quarters-back-1 (printed as lowest of the 2 filled quarters), quarters-back-5 and the five years. Two filled quarters support no quarterly trend claim.",
  "account": "Net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "quarters-back-0 (2026-04-01..2026-06-30)",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001596532-26-000175:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_cell_insufficient",
  "what_changed": "insufficient: the bad-debt reserve ratio has no value for quarters-back-0. The allowance concepts are in the record, but not at 2026-06-30. Across the whole table the ratio is filled in 2 periods (years-back-3 and years-back-4), which supports no trend claim.",
  "account": "Allowance for credit losses on accounts receivable, against receivables",
  "expected_direction": "none",
  "horizon": "quarters-back-0 (2026-04-01..2026-06-30)",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001596532-26-000175:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_cell_insufficient",
  "what_changed": "insufficient: the inventory reserve ratio has no value for quarters-back-0, and none in any period of the table (filled 0). The record never tags us-gaap:InventoryValuationReserves. This input cannot show whether the filing states a reserve outside that tag.",
  "account": "Inventory valuation reserve, against inventory",
  "expected_direction": "none",
  "horizon": "quarters-back-0 (2026-04-01..2026-06-30)",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_cell_insufficient",
  "what_changed": "insufficient: the warranty reserve ratio has no value for quarters-back-0, and none in any period of the table (filled 0). The record never tags any of the three product-warranty accrual concepts. This input cannot show whether the filing states a warranty accrual outside them.",
  "account": "Product warranty accrual, against revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-0 (2026-04-01..2026-06-30)",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell_insufficient",
  "what_changed": "insufficient: the non-GAAP gap has no value for quarters-back-0, and none in any period of the table (filled 0), because companyfacts carries no non-GAAP measure. The 8-K prints non-GAAP net income of 1,301.7 and GAAP net income of 1,212.9 (in millions) for the quarter (paragraph 0001596532-26-000174:8k_2_02:39). The gap between them is not computed here.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarters-back-0 (2026-04-01..2026-06-30)",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001596532-26-000175:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend_cell",
  "what_changed": "Receivables over revenue for years-back-0 (2025-01-01..2025-12-31) is printed as 0.20952285774564997. Inputs: AccountsReceivableNetCurrent 1886900000.0 at 2025-12-31, taken from 0001596532-26-000175; 2025 revenue 9005700000.0 from the 10-K 0001596532-26-000013. Printed change against years-back-1: 0.04666640845890552. Position as printed: second highest of the 5 filled years.",
  "account": "Accounts receivable, net, against revenue",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend_cell",
  "what_changed": "Days sales outstanding for years-back-0 (2025-01-01..2025-12-31, 365 days) is printed as 76.47584307716224 (receivables 1886900000.0, revenue 9005700000.0). Printed change against years-back-1: 16.87038263821377. Position as printed: second highest of the 5 filled years.",
  "account": "Accounts receivable, net, in days of revenue",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend_cell",
  "what_changed": "Contract liabilities over revenue for years-back-0 (2025-01-01..2025-12-31) is printed as 0.44445184716346314 (the contract-liability input is ContractWithCustomerLiabilityCurrent 4002600000.0 at 2025-12-31; revenue 9005700000.0). Printed change against years-back-1: 0.19780393409639285. Position as printed: highest of the 5 filled years.",
  "account": "Deferred revenue, current (contract liabilities), against revenue",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend_cell",
  "what_changed": "Days sales of inventory for years-back-0 (2025-01-01..2025-12-31) is printed as 253.3801359283287 (InventoryNet 2247100000.0 at 2025-12-31; cost of revenue 3237000000.0). Printed change against years-back-1: -13.943536338571533. Position as printed: second lowest of the 5 filled years.",
  "account": "Inventories, in days of cost of revenue",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend_cell",
  "what_changed": "Gross margin for years-back-0 (2025-01-01..2025-12-31) is printed as 0.6405609780472368 (revenue 9005700000.0, cost of revenue 3237000000.0). Printed change against years-back-1: -0.000769289976923937. Position as printed: second highest of the 5 filled years.",
  "account": "Gross margin",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_annual_trend_cell",
  "what_changed": "Soft asset share for years-back-0 (2025-01-01..2025-12-31) is printed as 0.888578098166449 (Assets 19448600000.0, PropertyPlantAndEquipmentNet 203100000.0, CashAndCashEquivalentsAtCarryingValue 1963900000.0, all at 2025-12-31). Printed change against years-back-1: 0.09231067957189898. Position as printed: highest of the 5 filled years.",
  "account": "Total assets other than property and equipment and cash, as a share of total assets",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend_cell",
  "what_changed": "Accruals over total assets for years-back-0 (2025-01-01..2025-12-31) is printed as -0.044244829962053825 (formula (net_income - operating_cash_flow) / assets; net income 3511400000.0, operating cash flow 4371900000.0, Assets 19448600000.0). Printed change against years-back-1: 0.016714020499712497. The printed change is positive while the value itself stays negative. Position as printed: second lowest of the 5 filled years.",
  "account": "Net income less operating cash flow, over total assets",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1 (year over year)",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_cell_insufficient",
  "what_changed": "insufficient: the bad-debt reserve ratio has no value for years-back-0. The allowance concepts are in the record, but not at 2025-12-31. Only years-back-3 and years-back-4 carry the ratio, and two periods support no trend claim.",
  "account": "Allowance for credit losses on accounts receivable, against receivables",
  "expected_direction": "none",
  "horizon": "years-back-0 (2025-01-01..2025-12-31)",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-12-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001596532-26-000175:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_cell_insufficient",
  "what_changed": "insufficient: the inventory reserve ratio has no value for years-back-0 or for any year. The record never tags us-gaap:InventoryValuationReserves.",
  "account": "Inventory valuation reserve, against inventory",
  "expected_direction": "none",
  "horizon": "years-back-0 (2025-01-01..2025-12-31)",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_cell_insufficient",
  "what_changed": "insufficient: the warranty reserve ratio has no value for years-back-0 or for any year. The record never tags any of the three product-warranty accrual concepts.",
  "account": "Product warranty accrual, against revenue",
  "expected_direction": "none",
  "horizon": "years-back-0 (2025-01-01..2025-12-31)",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell_insufficient",
  "what_changed": "insufficient: the non-GAAP gap has no value for years-back-0 or for any year, because companyfacts carries no non-GAAP measure. No annual non-GAAP figure is in my input.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "years-back-0 (2025-01-01..2025-12-31)",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001596532-26-000175:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_prior_period_recast_figures",
  "what_changed": "Restated prior value. The release recasts its year-ago non-GAAP comparatives under a changed method for the income tax on stock-based awards. Per paragraphs 0001596532-26-000174:8k_2_02:53 and :55, the method took effect in the fourth quarter of fiscal 2025: direct excess tax benefits are still excluded, but the discrete indirect effects no longer are. The recast raises non-GAAP net income for the three and six months ended June 30, 2025 by $10.7 million and $30.4 million, and non-GAAP diluted EPS by nil and $0.03. The filing that printed the figures before the recast is not in my input, so the originally reported values are not shown here. The numeric facts show no GAAP period re-reported with a different value.",
  "account": "Non-GAAP net income and non-GAAP diluted net income per share, prior-period comparatives",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2025, as recast in this release",
  "quote": "(1) Prior period amounts have been updated to conform to the current period presentation to reflect the change in methodology for calculating non-GAAP income taxes associated with stock-based awards. The retrospective application of this change resulted in an increase to non-GAAP net income of $10.7 million and $30.4 million for the three and six months ended June 30, 2025, respectively.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:40" }
```

```json
{ "id": "results_against_expectations_next_quarter_revenue_guidance_figure",
  "what_changed": "The release guides third-quarter 2026 revenue to approximately $3.3 billion. It reports second-quarter revenue of $3.036 billion (paragraph 0001596532-26-000174:8k_2_02:11), so the guide sits above the reported quarter. No growth rate is printed for the guide, and none is computed here. My input holds no earlier guidance for the reported quarter and no outside expectation, so it cannot show whether the quarter met either.",
  "account": "Revenue",
  "expected_direction": "up",
  "horizon": "next quarter (third quarter of 2026), against the reported second quarter",
  "quote": "Revenue of approximately $3.3 billion;",
  "paragraph_id": "0001596532-26-000174:8k_2_02:24" }
```

```json
{ "id": "results_against_expectations_next_quarter_non_gaap_operating_margin_guidance_figure",
  "what_changed": "The release guides third-quarter 2026 non-GAAP operating margin to 48 - 49%. The second-quarter non-GAAP operating margin is printed as 49.9% (paragraph 0001596532-26-000174:8k_2_02:12). Both ends of the guided range sit below that printed figure.",
  "account": "Non-GAAP operating margin",
  "expected_direction": "down",
  "horizon": "next quarter (third quarter of 2026), against the reported second quarter",
  "quote": "Non-GAAP operating margin of 48 - 49%; and",
  "paragraph_id": "0001596532-26-000174:8k_2_02:25" }
```

```json
{ "id": "results_against_expectations_next_quarter_non_gaap_eps_guidance_figure",
  "what_changed": "The release guides third-quarter 2026 non-GAAP diluted net income per share to between $1.06 and $1.08. The second-quarter non-GAAP diluted EPS is printed as $1.02 (paragraph 0001596532-26-000174:8k_2_02:13). Both ends of the guided range sit above that printed figure.",
  "account": "Non-GAAP diluted net income per share",
  "expected_direction": "up",
  "horizon": "next quarter (third quarter of 2026), against the reported second quarter",
  "quote": "Non-GAAP diluted net income per share between $1.06 and $1.08.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:26" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_year_to_date_fact",
  "what_changed": "Net cash provided by operating activities is printed as 2776500000 for 2026-01-01..2026-06-30. The same filing prints 1841800000 for 2025-01-01..2025-06-30 (paragraph 0001596532-26-000175:facts:NetCashProvidedByUsedInOperatingActivities:2025-01-01..2025-06-30). This is the six-month figure. The record prints no three-month figure for the quarter, which is why the quarterly accruals cell is insufficient, and none is derived here.",
  "account": "Net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "six months to 2026-06-30 against six months to 2025-06-30",
  "quote": "\"value\": \"2776500000\"",
  "paragraph_id": "0001596532-26-000175:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_payments_fact",
  "what_changed": "Payments for repurchase of common stock are printed as 0 for 2026-01-01..2026-06-30. The same filing prints 983000000.0 for 2025-01-01..2025-06-30 (paragraph 0001596532-26-000175:facts:PaymentsForRepurchaseOfCommonStock:2025-01-01..2025-06-30). The 8-K cash-flow table prints the same pair: a dash against (983.0).",
  "account": "Repurchases of common stock (financing cash flow)",
  "expected_direction": "down",
  "horizon": "six months to 2026-06-30 against six months to 2025-06-30",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001596532-26-000175:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-06-30" }
```

## Seen in the notes

No items.

This heading is meant for facts marked as having sat inside a note when they were extracted. No fact in `input_numbers.json` carries that marker. Each fact prints these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and on some, superseded_by. None prints a note marker.

Without the marker I do not sort facts into this heading myself, so none is itemized here. For the same reason, the following fact groups are not itemized under the first heading either:
- the fair-value hierarchy and available-for-sale securities tables
- inventory components, including evaluation inventory
- the contract-liability rollforward and remaining performance obligations
- intangible assets and their amortization schedule
- purchase commitments
- the stock repurchase authorization
- share-based compensation detail
- the earnings-per-share computation

The two facts itemized under the first heading come from the cash flow statement. The 8-K's statement tables print both as well.
