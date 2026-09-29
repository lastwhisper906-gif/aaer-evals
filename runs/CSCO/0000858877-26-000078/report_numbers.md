<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# CSCO — numbers reader — 10-Q 0000858877-26-000078 (filed 2026-05-19, quarter ended 2026-04-25)

## What the input holds, and what it does not

- **Files read in full.** I read all four input files: input_trends.json, input_numbers.json, input_8k.md and input_prior_predictions.md. None of them contains prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.
- **Prior flags.** input_prior_predictions.md says: "None on record." There are no earlier flags, management explanations or outcomes to carry forward.
- **8-K contradicts itself.**
  - It says "no 8-K filed at or before 2026-05-19 is on record, so this bundle has no earnings release and no verbatim item body."
  - Yet its own item-code list includes "2026-05-13 0000858877-26-000075 — 2.02, 2.05, 9.01".
  - The file has no release figures and no paragraph ids, so no item below quotes it.
  - Nothing in my input gives an expectation or guidance baseline, so no item compares results with expectations.
- **Periods the record does not reach.**
  - quarters-back-3 (target end 2025-07-26) and quarters-back-7 (target end 2024-07-27) have no cells.
  - The reason the table gives for both: "no quarter ending within 20 days of [target] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
  - The output of that fourth-quarter derivation is **not** in my input.
  - So each quarterly metric has at most 6 filled quarters of history. The quarterly accruals ratio has 2, which is **insufficient** for a trend claim.
- **Sections that are absent, not findings of "none".**
  - input_numbers.json holds only `ticker`, `cutoff`, `documents` and `facts`. It has no articulation checks, no restatement traces and no tag-change notices.
  - Neither file says that any period rests on a different concept.
  - So I report zero articulation gaps from a check, zero restated prior values and zero tag changes. That is because the checks are missing from my input, not because they came back clean.
  - Across the facts I read, no paragraph context shows a different value in an earlier filing.
  - Two paragraph ids in this filing print the same period at two precisions. They are listed below as filed-history items, not as restatements.
- **R&D capitalization baseline (years-back-0).**
  - Printed values:
    - book_value_with_rnd_capitalized 71079400000.0
    - earnings_with_rnd_capitalized 12439200000.0
    - research_and_development_amortization 7040800000.0
    - research_and_development_asset 24236400000.0
    - life_years 5
  - These print at period level with no paragraph_id, so I cannot quote them and they have no item.
  - Its capitalized_development_cost and capitalized_over_expense are missing: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
- **How `expected_direction` is used.**
  - For trend cells it follows the sign of the printed year_over_year change. For quarterly cells, the quarter_over_quarter change is also given in `what_changed`.
  - For facts it compares the figure with the comparative period printed in the same filing.
  - It is `none` where a cell is insufficient or no comparative is printed.

## Seen in the statements

### Trend table — quarters-back-0 (2026-01-25..2026-04-25)

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_latest_quarter",
  "what_changed": "receivables_over_revenue (receivables / revenue) is 0.4090650842749826. Quarter-over-quarter change against quarters-back-1: -0.021321260112273865. Year-over-year change against quarters-back-4: 0.03610586454213932. Position: second highest of the 6 filled quarters. Inputs: AccountsReceivableNetCurrent 6480000000.0 at 2026-04-25; revenue 15841000000.0. Six filled quarters is a short history.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:receivables_over_revenue:2026-01-25..2026-04-25" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_latest_quarter",
  "what_changed": "days_sales_outstanding (receivables / revenue * days_in_period) is 37.22492266902342. Quarter-over-quarter change against quarters-back-1: -1.9402346702169169. Year-over-year change against quarters-back-4: 3.2856336733346794. Position: second highest of the 6 filled quarters. Quarters-back-1, at 39.16515733924034, is the highest of the 6.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:days_sales_outstanding:2026-01-25..2026-04-25" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_latest_quarter",
  "what_changed": "contract_liabilities_over_revenue is 1.0381920333312291. Quarter-over-quarter change against quarters-back-1: -0.017186167203007585. Year-over-year change against quarters-back-4: -0.09835471908943672. Position: lowest of the 6 filled quarters. Inputs: ContractWithCustomerLiabilityCurrent 16446000000.0 at 2026-04-25; revenue 15841000000.0.",
  "account": "ContractWithCustomerLiabilityCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:contract_liabilities_over_revenue:2026-01-25..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_latest_quarter",
  "what_changed": "bad_debt_reserve_ratio (bad_debt_allowance / (receivables + bad_debt_allowance)) is 0.011139935907218068. Quarter-over-quarter change against quarters-back-1: -0.00023390426039641803. Year-over-year change against quarters-back-4: -0.004161426287221192. Position: lowest of the 6 filled quarters. Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 73000000.0; AccountsReceivableNetCurrent 6480000000.0.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:bad_debt_reserve_ratio:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_latest_quarter",
  "what_changed": "days_sales_of_inventory (inventory / cost_of_revenue * days_in_period) is 74.36695018226003. Quarter-over-quarter change against quarters-back-1: 8.025123885068282. Year-over-year change against quarters-back-4: 21.45953897306274. Position: highest of the 6 filled quarters. Inputs: InventoryNet 4708000000.0 at 2026-04-25; CostOfGoodsAndServicesSold 5761000000.0.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:days_sales_of_inventory:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_latest_quarter",
  "what_changed": "gross_margin ((revenue - cost_of_revenue) / revenue) is 0.6363234644277508. Quarter-over-quarter change against quarters-back-1: -0.013360554075083297. Year-over-year change against quarters-back-4: -0.01941192323215446. Position: lowest of the 6 filled quarters. Inputs: revenue 15841000000.0; CostOfGoodsAndServicesSold 5761000000.0.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:gross_margin:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_latest_quarter",
  "what_changed": "soft_asset_share ((assets - property_plant_and_equipment - cash) / assets) is 0.9230560909945359. Quarter-over-quarter change against quarters-back-1: 0.0025642412081192667. Year-over-year change against quarters-back-4: 0.0085196831870189. Position: highest of the 6 filled quarters. Inputs: Assets 125546000000.0; CashAndCashEquivalentsAtCarryingValue 7083000000.0; PropertyPlantAndEquipmentNet 2577000000.0.",
  "account": "Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:soft_asset_share:2026-01-25..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_latest_quarter",
  "what_changed": "warranty_reserve_ratio (warranty_accrual / revenue) is 0.02342023862129916. Quarter-over-quarter change against quarters-back-1: -0.0011416220862387888. Year-over-year change against quarters-back-4: -0.00456760504256401. Position: lowest of the 6 filled quarters. Inputs: ProductWarrantyAccrual 371000000.0 at 2026-04-25; revenue 15841000000.0.",
  "account": "ProductWarrantyAccrual",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000858877-26-000078:trends:warranty_reserve_ratio:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_latest_quarter",
  "what_changed": "insufficient: accruals_over_total_assets is not filled in quarters-back-0 because the record has no quarter-alone operating cash flow. Only 2 quarters in the table are filled for this ratio, which does not support a trend claim. The nine-month operating cash flow appears below as a fact.",
  "account": "NetCashProvidedByUsedInOperatingActivities, NetIncomeLoss, Assets",
  "expected_direction": "none",
  "horizon": "quarter 2026-01-25..2026-04-25",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-25..2026-04-25: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000858877-26-000078:trends:accruals_over_total_assets:2026-01-25..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_latest_quarter",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled in quarters-back-0. The record tags no InventoryValuationReserves in any period, so this ratio is filled in 0 periods.",
  "account": "InventoryValuationReserves",
  "expected_direction": "none",
  "horizon": "quarter 2026-01-25..2026-04-25",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000858877-26-000078:trends:inventory_reserve_ratio:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_latest_quarter",
  "what_changed": "insufficient: non_gaap_gap is not filled in quarters-back-0. No us-gaap concept carries a non-GAAP measure, and there is no earnings release in the 8-K bundle, so this ratio is filled in 0 periods.",
  "account": "non_gaap_net_income",
  "expected_direction": "none",
  "horizon": "quarter 2026-01-25..2026-04-25",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000858877-26-000078:trends:non_gaap_gap:2026-01-25..2026-04-25" }
```

### Trend table — years-back-0 (2024-07-28..2025-07-26)

For every annual cell, quarter-over-quarter reads "an annual period has no preceding quarter".

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_latest_year",
  "what_changed": "accruals_over_total_assets ((net_income - operating_cash_flow) / assets) is -0.032815170372308675. Year-over-year change against years-back-1: -0.02831403303135556. Position: third highest of the 5 filled years. Inputs: NetIncomeLoss 10180000000.0; NetCashProvidedByUsedInOperatingActivities 14193000000.0; Assets 122291000000.0 at 2025-07-26.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:accruals_over_total_assets:2024-07-28..2025-07-26" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_latest_year",
  "what_changed": "bad_debt_reserve_ratio is 0.010192023633677992. Year-over-year change against years-back-1: -0.0026549934956781804. Position: lowest of the 5 filled years. Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 69000000.0; AccountsReceivableNetCurrent 6701000000.0 at 2025-07-26.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:bad_debt_reserve_ratio:2024-07-28..2025-07-26" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_latest_year",
  "what_changed": "contract_liabilities_over_revenue is 0.2897588872806863. Year-over-year change against years-back-1: -0.01225029436345998. Position: second highest of the 5 filled years. Inputs: ContractWithCustomerLiabilityCurrent 16416000000.0; revenue 56654000000.0.",
  "account": "ContractWithCustomerLiabilityCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:contract_liabilities_over_revenue:2024-07-28..2025-07-26" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_latest_year",
  "what_changed": "days_sales_of_inventory is 57.97905759162304. Year-over-year change against years-back-1: -6.725659140919781. Position: third highest of the 5 filled years. Inputs: InventoryNet 3164000000.0 at 2025-07-26; CostOfGoodsAndServicesSold 19864000000.0.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:days_sales_of_inventory:2024-07-28..2025-07-26" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_latest_year",
  "what_changed": "days_sales_outstanding is 43.05369435520881. Year-over-year change against years-back-1: -2.1731517314406332. Position: third highest of the 5 filled years. Inputs: AccountsReceivableNetCurrent 6701000000.0; revenue 56654000000.0.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:days_sales_outstanding:2024-07-28..2025-07-26" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_latest_year",
  "what_changed": "gross_margin is 0.6493804497475907. Year-over-year change against years-back-1: 0.0020559511136855058. Position: highest of the 5 filled years. Inputs: revenue 56654000000.0; CostOfGoodsAndServicesSold 19864000000.0.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:gross_margin:2024-07-28..2025-07-26" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_latest_year",
  "what_changed": "receivables_over_revenue is 0.1182793800967275. Year-over-year change against years-back-1: -0.005970197064397345. Position: third highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:receivables_over_revenue:2024-07-28..2025-07-26" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_latest_year",
  "what_changed": "soft_asset_share is 0.9144744911726946. Year-over-year change against years-back-1: -0.008379229901469665. Position: second highest of the 5 filled years. Inputs: Assets 122291000000.0; cash 8346000000.0; PropertyPlantAndEquipmentNet 2113000000.0.",
  "account": "Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:soft_asset_share:2024-07-28..2025-07-26" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_latest_year",
  "what_changed": "warranty_reserve_ratio is 0.0070427507325166805. Year-over-year change against years-back-1: 0.0003145013783914458. Position: highest of the 5 filled years. Inputs: ProductWarrantyAccrual 399000000.0 at 2025-07-26; revenue 56654000000.0.",
  "account": "ProductWarrantyAccrual",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-07-28..2025-07-26 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000858877-26-000078:trends:warranty_reserve_ratio:2024-07-28..2025-07-26" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_latest_year",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled in years-back-0. The record tags no InventoryValuationReserves in any period.",
  "account": "InventoryValuationReserves",
  "expected_direction": "none",
  "horizon": "fiscal year 2024-07-28..2025-07-26",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000858877-26-000078:trends:inventory_reserve_ratio:2024-07-28..2025-07-26" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_latest_year",
  "what_changed": "insufficient: non_gaap_gap is not filled in years-back-0. No us-gaap concept carries a non-GAAP measure.",
  "account": "non_gaap_net_income",
  "expected_direction": "none",
  "horizon": "fiscal year 2024-07-28..2025-07-26",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000858877-26-000078:trends:non_gaap_gap:2024-07-28..2025-07-26" }
```

### Filed history — one fact printed at two precisions

```json
{ "id": "articulation_and_the_filed_history_receivables_printed_at_two_precisions",
  "what_changed": "This paragraph id prints AccountsReceivableNetCurrent at 2026-04-25 twice in the same filing: 6480000000 (decimals -6) and 6500000000 (decimals -8). The trend table uses 6480000000.0. This is a rounding difference within one filing, not a restated prior value.",
  "account": "AccountsReceivableNetCurrent",
  "expected_direction": "none",
  "horizon": "balance at 2026-04-25",
  "quote": "\"value\": \"6500000000\"",
  "paragraph_id": "0000858877-26-000078:facts:AccountsReceivableNetCurrent:2026-04-25" }
```

```json
{ "id": "articulation_and_the_filed_history_contract_liability_printed_at_two_precisions",
  "what_changed": "This paragraph id prints ContractWithCustomerLiability at 2026-04-25 twice in the same filing: 28599000000 (decimals -6) and 28600000000 (decimals -8). This is a rounding difference within one filing, not a restated prior value.",
  "account": "ContractWithCustomerLiability",
  "expected_direction": "none",
  "horizon": "balance at 2026-04-25",
  "quote": "\"value\": \"28600000000\"",
  "paragraph_id": "0000858877-26-000078:facts:ContractWithCustomerLiability:2026-04-25" }
```

### Numeric facts — this 10-Q

```json
{ "id": "liquidity_and_capital_operating_cash_flow_nine_months",
  "what_changed": "Operating cash flow for the nine months is 8791000000, against 9959000000 for 2024-07-28..2025-04-26 in the same filing. The record holds no quarter-alone figure.",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "down",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"8791000000\"",
  "paragraph_id": "0000858877-26-000078:facts:NetCashProvidedByUsedInOperatingActivities:2025-07-27..2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_inventory_balance",
  "what_changed": "InventoryNet is 4708000000 at 2026-04-25, against 3164000000 at 2025-07-26. The trend table's inventory input at 2026-01-24 is 3920000000.0.",
  "account": "InventoryNet",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"4708000000\"",
  "paragraph_id": "0000858877-26-000078:facts:InventoryNet:2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_inventory_cash_flow_change_nine_months",
  "what_changed": "The inventory change line in the cash flow statement is 1549000000 for the nine months, against -541000000 for the prior-year nine months.",
  "account": "IncreaseDecreaseInInventories",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"1549000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncreaseDecreaseInInventories:2025-07-27..2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_inventory_purchase_commitments_next_twelve_months",
  "what_changed": "Unrecorded inventory purchase obligations due in the next twelve months are 14149000000 at 2026-04-25, against 7202000000 at 2025-07-26 in the same filing. The prior 10-Q (0000858877-26-000021) printed 9615000000 at 2026-01-24.",
  "account": "UnrecordedUnconditionalPurchaseObligationDueInNextRollingTwelveMonths (InventoriesMember)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"14149000000\"",
  "paragraph_id": "0000858877-26-000078:facts:UnrecordedUnconditionalPurchaseObligationDueInNextRollingTwelveMonths:2026-04-25:us-gaap:UnrecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:InventoriesMember" }
```

```json
{ "id": "liquidity_and_capital_inventory_purchase_commitments_total",
  "what_changed": "Total unrecorded inventory purchase obligations are 16033000000 at 2026-04-25, against 7599000000 at 2025-07-26.",
  "account": "UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount (InventoriesMember)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"16033000000\"",
  "paragraph_id": "0000858877-26-000078:facts:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount:2026-04-25:us-gaap:UnrecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:InventoriesMember" }
```

```json
{ "id": "liquidity_and_capital_recorded_inventory_purchase_obligation",
  "what_changed": "The recorded liability for inventory purchase obligations is 209000000 at 2026-04-25, against 206000000 at 2025-07-26.",
  "account": "RecordedUnconditionalPurchaseObligation (InventoriesMember)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"209000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RecordedUnconditionalPurchaseObligation:2026-04-25:us-gaap:RecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:InventoriesMember" }
```

```json
{ "id": "liquidity_and_capital_current_debt",
  "what_changed": "DebtCurrent is 11932000000 at 2026-04-25, against 5232000000 at 2025-07-26. The commercial paper component in the input is 8434000000, against 3482000000.",
  "account": "DebtCurrent",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"11932000000\"",
  "paragraph_id": "0000858877-26-000078:facts:DebtCurrent:2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_accrued_income_taxes_current",
  "what_changed": "Current accrued income taxes are 173000000 at 2026-04-25, against 1857000000 at 2025-07-26.",
  "account": "AccruedIncomeTaxesCurrent",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"173000000\"",
  "paragraph_id": "0000858877-26-000078:facts:AccruedIncomeTaxesCurrent:2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_income_taxes_payable_cash_flow_nine_months",
  "what_changed": "The cash flow line for the change in accrued income taxes payable is -2342000000 for the nine months, against -2002000000 for the prior-year nine months.",
  "account": "IncreaseDecreaseInAccruedIncomeTaxesPayable",
  "expected_direction": "down",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"-2342000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncreaseDecreaseInAccruedIncomeTaxesPayable:2025-07-27..2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_quarter",
  "what_changed": "Stock repurchased and retired in the quarter is 1252000000 (16000000 shares). Earlier quarters printed in this filing: 1351000000 (2025-10-26..2026-01-24), 2001000000 (2025-07-27..2025-10-25), 1252000000 (2025-04-27..2025-07-26) and 1504000000 (2025-01-26..2025-04-26).",
  "account": "StockRepurchasedAndRetiredDuringPeriodValue",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"1252000000\"",
  "paragraph_id": "0000858877-26-000078:facts:StockRepurchasedAndRetiredDuringPeriodValue:2026-01-25..2026-04-25" }
```

```json
{ "id": "liquidity_and_capital_repurchase_authorization_remaining",
  "what_changed": "The remaining repurchase authorization is 9600000000 at 2026-04-25, printed at decimals -8. The filing prints no comparative.",
  "account": "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1",
  "expected_direction": "none",
  "horizon": "balance at 2026-04-25",
  "quote": "\"value\": \"9600000000\"",
  "paragraph_id": "0000858877-26-000078:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-04-25" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_change_nine_months",
  "what_changed": "The cash flow line for the change in accounts receivable is -187000000 for the nine months, against -1406000000 for the prior-year nine months.",
  "account": "IncreaseDecreaseInAccountsReceivable",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"-187000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncreaseDecreaseInAccountsReceivable:2025-07-27..2026-04-25" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations",
  "what_changed": "Remaining performance obligations are 43462000000 at 2026-04-25, against 43533000000 at 2025-07-26.",
  "account": "RevenueRemainingPerformanceObligation",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"43462000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RevenueRemainingPerformanceObligation:2026-04-25" }
```

```json
{ "id": "revenue_recognition_contract_liability_total",
  "what_changed": "The total contract liability is 28599000000 at 2026-04-25 (decimals -6), against 28779000000 at 2025-07-26. The current portion used by the trend table is 16446000000.0, against 16416000000.0.",
  "account": "ContractWithCustomerLiability",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"28599000000\"",
  "paragraph_id": "0000858877-26-000078:facts:ContractWithCustomerLiability:2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_provision_quarter",
  "what_changed": "The provision for doubtful accounts is 1000000 in the quarter, against 13000000 in the same quarter a year earlier.",
  "account": "ProvisionForDoubtfulAccounts",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"1000000\"",
  "paragraph_id": "0000858877-26-000078:facts:ProvisionForDoubtfulAccounts:2026-01-25..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_allowance_balance",
  "what_changed": "The allowance for doubtful accounts is 73000000 at 2026-04-25. Other balances in the input: 76000000 at 2026-01-24, 69000000.0 at 2025-07-26 (trend input), 82000000 at 2025-04-26 and 87000000 at 2024-07-27.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-25 against 2025-04-26",
  "quote": "\"value\": \"73000000\"",
  "paragraph_id": "0000858877-26-000078:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_balance",
  "what_changed": "The product warranty accrual is 371000000 at 2026-04-25. The same filing prints 399000000 at 2025-07-26, 396000000 at 2025-04-26 and 362000000 at 2024-07-27.",
  "account": "ProductWarrantyAccrual",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-25 against 2025-07-26 and 2025-04-26",
  "quote": "\"value\": \"371000000\"",
  "paragraph_id": "0000858877-26-000078:facts:ProductWarrantyAccrual:2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_warranty_preexisting_adjustment_nine_months",
  "what_changed": "The change in estimate for pre-existing warranties is 0 for the nine months, against 40000000 for the prior-year nine months.",
  "account": "ProductWarrantyAccrualPreexistingIncreaseDecrease",
  "expected_direction": "down",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0000858877-26-000078:facts:ProductWarrantyAccrualPreexistingIncreaseDecrease:2025-07-27..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_warranty_payments_nine_months",
  "what_changed": "Warranty settlements are 337000000 for the nine months, against 306000000 for the prior-year nine months. Warranties issued in the same nine months are 309000000.",
  "account": "ProductWarrantyAccrualPayments",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"337000000\"",
  "paragraph_id": "0000858877-26-000078:facts:ProductWarrantyAccrualPayments:2025-07-27..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_warranty_issued_nine_months",
  "what_changed": "Warranties issued are 309000000 for the nine months, against 300000000 for the prior-year nine months.",
  "account": "ProductWarrantyAccrualWarrantiesIssued",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"309000000\"",
  "paragraph_id": "0000858877-26-000078:facts:ProductWarrantyAccrualWarrantiesIssued:2025-07-27..2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_equity_securities_without_readily_determinable_fair_value",
  "what_changed": "Equity securities without a readily determinable fair value are 2946000000 at 2026-04-25, against 1921000000 at 2025-07-26.",
  "account": "EquitySecuritiesWithoutReadilyDeterminableFairValueAmount",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"2946000000\"",
  "paragraph_id": "0000858877-26-000078:facts:EquitySecuritiesWithoutReadilyDeterminableFairValueAmount:2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits",
  "what_changed": "Unrecognized tax benefits are 2500000000 at 2026-04-25, printed at decimals -8. The fiscal 2025 10-K facts in the input carry 2337000000, so the two precisions differ.",
  "account": "UnrecognizedTaxBenefits",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"2500000000\"",
  "paragraph_id": "0000858877-26-000078:facts:UnrecognizedTaxBenefits:2026-04-25" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_rate_impact",
  "what_changed": "Unrecognized tax benefits that would affect the effective tax rate are 1700000000 at 2026-04-25 (decimals -8). This filing prints no comparative.",
  "account": "UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate",
  "expected_direction": "none",
  "horizon": "balance at 2026-04-25",
  "quote": "\"value\": \"1700000000\"",
  "paragraph_id": "0000858877-26-000078:facts:UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate:2026-04-25" }
```

```json
{ "id": "earnings_quality_revenue_quarter",
  "what_changed": "Revenue is 15841000000 in the quarter, against 14149000000 in the same quarter a year earlier. The trend table's revenue for quarters-back-1 is 15349000000.0.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"15841000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_revenue_nine_months",
  "what_changed": "Revenue is 46073000000 for the nine months, against 41981000000 for the prior-year nine months.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"46073000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-07-27..2026-04-25" }
```

```json
{ "id": "earnings_quality_americas_segment_revenue_quarter",
  "what_changed": "Americas segment revenue is 9569000000 in the quarter, against 8380000000 a year earlier. For the nine months it is 27403000000, against 24834000000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (AmericasSegmentMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"9569000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=csco:AmericasSegmentMember" }
```

```json
{ "id": "earnings_quality_emea_segment_revenue_quarter",
  "what_changed": "EMEA segment revenue is 4054000000 in the quarter, against 3736000000 a year earlier. For the nine months it is 12262000000, against 11179000000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (EuropeMiddleEastAndAfricaSegmentMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"4054000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=csco:EuropeMiddleEastAndAfricaSegmentMember" }
```

```json
{ "id": "earnings_quality_apjc_segment_revenue_quarter",
  "what_changed": "APJC segment revenue is 2218000000 in the quarter, against 2034000000 a year earlier. For the nine months it is 6409000000, against 5968000000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (AsiaPacificJapanAndChinaSegmentMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"2218000000\"",
  "paragraph_id": "0000858877-26-000078:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=csco:AsiaPacificJapanAndChinaSegmentMember" }
```

```json
{ "id": "earnings_quality_americas_segment_product_cost_quarter",
  "what_changed": "Americas product cost of sales is 2864000000 in the quarter, against 2091000000 a year earlier.",
  "account": "CostOfGoodsAndServicesSold (AmericasSegmentMember, ProductMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"2864000000\"",
  "paragraph_id": "0000858877-26-000078:facts:CostOfGoodsAndServicesSold:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:StatementBusinessSegmentsAxis=csco:AmericasSegmentMember" }
```

```json
{ "id": "earnings_quality_emea_segment_product_cost_quarter",
  "what_changed": "EMEA product cost of sales is 881000000 in the quarter, against 790000000 a year earlier.",
  "account": "CostOfGoodsAndServicesSold (EuropeMiddleEastAndAfricaSegmentMember, ProductMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"881000000\"",
  "paragraph_id": "0000858877-26-000078:facts:CostOfGoodsAndServicesSold:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:StatementBusinessSegmentsAxis=csco:EuropeMiddleEastAndAfricaSegmentMember" }
```

```json
{ "id": "earnings_quality_apjc_segment_product_cost_quarter",
  "what_changed": "APJC product cost of sales is 582000000 in the quarter, against 481000000 a year earlier.",
  "account": "CostOfGoodsAndServicesSold (AsiaPacificJapanAndChinaSegmentMember, ProductMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"582000000\"",
  "paragraph_id": "0000858877-26-000078:facts:CostOfGoodsAndServicesSold:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:StatementBusinessSegmentsAxis=csco:AsiaPacificJapanAndChinaSegmentMember" }
```

```json
{ "id": "earnings_quality_gross_profit_quarter",
  "what_changed": "Gross profit is 10080000000 in the quarter, against 9278000000 a year earlier. For the nine months it is 29797000000, against 27510000000. The gross_margin trend cell above sits at the lowest of its 6 filled quarters.",
  "account": "GrossProfit",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"10080000000\"",
  "paragraph_id": "0000858877-26-000078:facts:GrossProfit:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_corporate_unallocated_gross_profit_quarter",
  "what_changed": "Gross profit not allocated to segments is -378000000 in the quarter, against -425000000 a year earlier. For the nine months it is -1154000000, against -1397000000.",
  "account": "GrossProfit (CorporateNonSegmentMember)",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"-378000000\"",
  "paragraph_id": "0000858877-26-000078:facts:GrossProfit:2026-01-25..2026-04-25:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "earnings_quality_operating_income_quarter",
  "what_changed": "Operating income is 3960000000 in the quarter, against 3202000000 a year earlier.",
  "account": "OperatingIncomeLoss",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"3960000000\"",
  "paragraph_id": "0000858877-26-000078:facts:OperatingIncomeLoss:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_other_nonoperating_income_quarter",
  "what_changed": "Other non-operating income (expense) is 242000000 in the quarter, against -102000000 a year earlier.",
  "account": "OtherNonoperatingIncomeExpense",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"242000000\"",
  "paragraph_id": "0000858877-26-000078:facts:OtherNonoperatingIncomeExpense:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_investment_gains_nine_months",
  "what_changed": "Gains (losses) on investments are 500000000 for the nine months, against -52000000 for the prior-year nine months.",
  "account": "GainLossOnInvestments",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"500000000\"",
  "paragraph_id": "0000858877-26-000078:facts:GainLossOnInvestments:2025-07-27..2026-04-25" }
```

```json
{ "id": "earnings_quality_pretax_income_quarter",
  "what_changed": "Income before income taxes is 4039000000 in the quarter, against 2947000000 a year earlier. For the nine months it is 11076000000, against 8101000000.",
  "account": "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"4039000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_income_tax_expense_quarter",
  "what_changed": "Income tax expense is 666000000 in the quarter, against 456000000 a year earlier.",
  "account": "IncomeTaxExpenseBenefit",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"666000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncomeTaxExpenseBenefit:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_income_tax_expense_nine_months",
  "what_changed": "Income tax expense is 1668000000 for the nine months, against 471000000 for the prior-year nine months.",
  "account": "IncomeTaxExpenseBenefit",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"1668000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncomeTaxExpenseBenefit:2025-07-27..2026-04-25" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_quarter",
  "what_changed": "The effective tax rate is 0.165 in the quarter, against 0.155 a year earlier. The prior 10-Q (0000858877-26-000021) printed 0.129 for 2025-10-26..2026-01-24.",
  "account": "EffectiveIncomeTaxRateContinuingOperations",
  "expected_direction": "up",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"0.165\"",
  "paragraph_id": "0000858877-26-000078:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_nine_months",
  "what_changed": "The effective tax rate is 0.151 for the nine months, against 0.058 for the prior-year nine months.",
  "account": "EffectiveIncomeTaxRateContinuingOperations",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"0.151\"",
  "paragraph_id": "0000858877-26-000078:facts:EffectiveIncomeTaxRateContinuingOperations:2025-07-27..2026-04-25" }
```

```json
{ "id": "earnings_quality_share_based_compensation_quarter",
  "what_changed": "Share-based compensation expense is 914000000 in the quarter, against 945000000 a year earlier.",
  "account": "AllocatedShareBasedCompensationExpense",
  "expected_direction": "down",
  "horizon": "quarter 2026-01-25..2026-04-25 against 2025-01-26..2025-04-26",
  "quote": "\"value\": \"914000000\"",
  "paragraph_id": "0000858877-26-000078:facts:AllocatedShareBasedCompensationExpense:2026-01-25..2026-04-25" }
```

```json
{ "id": "earnings_quality_share_based_compensation_nine_months",
  "what_changed": "Share-based compensation expense is 2903000000 for the nine months, against 2693000000 for the prior-year nine months.",
  "account": "AllocatedShareBasedCompensationExpense",
  "expected_direction": "up",
  "horizon": "nine months 2025-07-27..2026-04-25 against 2024-07-28..2025-04-26",
  "quote": "\"value\": \"2903000000\"",
  "paragraph_id": "0000858877-26-000078:facts:AllocatedShareBasedCompensationExpense:2025-07-27..2026-04-25" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_private_company_funding_commitments",
  "what_changed": "Commitments to privately held companies, tagged on the related-party axis, are 600000000 at 2026-04-25, against 300000000 at 2025-07-26. Both are printed at decimals -8.",
  "account": "CommitmentsAndContingencies (RelatedPartyTransactionsByRelatedPartyAxis=InvestmentsInPrivatelyHeldCompaniesMember)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"600000000\"",
  "paragraph_id": "0000858877-26-000078:facts:CommitmentsAndContingencies:2026-04-25:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=csco:InvestmentsInPrivatelyHeldCompaniesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_channel_partner_financing_guarantees",
  "what_changed": "The maximum exposure under guarantees of third-party channel partner financing is 127000000 at 2026-04-25, against 123000000 at 2025-07-26.",
  "account": "GuaranteeObligationsMaximumExposure (ThirdPartyChannelPartnerMember)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-25 against 2025-07-26",
  "quote": "\"value\": \"127000000\"",
  "paragraph_id": "0000858877-26-000078:facts:GuaranteeObligationsMaximumExposure:2026-04-25:us-gaap:FinancingReceivableRecordedInvestmentByClassOfFinancingReceivableAxis=csco:ThirdPartyChannelPartnerMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_brazil_tax_possible_loss",
  "what_changed": "The estimated possible loss in the Brazilian tax authority matter (tax years 2003-2007) is 155000000 in this 10-Q. The fiscal 2025 10-K facts in the input carry 141000000 for the same matter, for a different period context.",
  "account": "IncomeTaxExaminationEstimateOfPossibleLoss (BrazilianTaxAuthorityMember)",
  "expected_direction": "none",
  "horizon": "as of the nine months 2025-07-27..2026-04-25",
  "quote": "\"value\": \"155000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncomeTaxExaminationEstimateOfPossibleLoss:2025-07-27..2026-04-25:us-gaap:IncomeTaxAuthorityNameAxis=csco:BrazilianTaxAuthorityMember,us-gaap:TaxPeriodAxis=csco:TaxYear2003Through2007Member" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_brazil_tax_interest",
  "what_changed": "Interest in the Brazilian tax authority matter is 966000000 in this 10-Q. The fiscal 2025 10-K facts in the input carry 816000000, for a different period context.",
  "account": "IncomeTaxExaminationInterestExpense (BrazilianTaxAuthorityMember)",
  "expected_direction": "none",
  "horizon": "as of the nine months 2025-07-27..2026-04-25",
  "quote": "\"value\": \"966000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncomeTaxExaminationInterestExpense:2025-07-27..2026-04-25:us-gaap:IncomeTaxAuthorityNameAxis=csco:BrazilianTaxAuthorityMember,us-gaap:TaxPeriodAxis=csco:TaxYear2003Through2007Member" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_brazil_tax_penalties",
  "what_changed": "Penalties in the Brazilian tax authority matter are 320000000 in this 10-Q. The fiscal 2025 10-K facts in the input carry 289000000, for a different period context.",
  "account": "IncomeTaxExaminationPenaltiesExpense (BrazilianTaxAuthorityMember)",
  "expected_direction": "none",
  "horizon": "as of the nine months 2025-07-27..2026-04-25",
  "quote": "\"value\": \"320000000\"",
  "paragraph_id": "0000858877-26-000078:facts:IncomeTaxExaminationPenaltiesExpense:2025-07-27..2026-04-25:us-gaap:IncomeTaxAuthorityNameAxis=csco:BrazilianTaxAuthorityMember,us-gaap:TaxPeriodAxis=csco:TaxYear2003Through2007Member" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter",
  "what_changed": "A dividend of 0.42 per share was declared on 2026-05-13, tagged as a subsequent event.",
  "account": "CommonStockDividendsPerShareDeclared (SubsequentEventMember)",
  "expected_direction": "none",
  "horizon": "subsequent event 2026-05-13",
  "quote": "\"value\": \"0.42\"",
  "paragraph_id": "0000858877-26-000078:facts:CommonStockDividendsPerShareDeclared:2026-05-13..2026-05-13:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

## Seen in the notes

No items.

- No fact in input_numbers.json carries a marker saying whether its element sat inside a note. The facts print `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession` and `filing_date`, and in places `superseded_by`. None of these fields is a note flag.
- Deciding which facts came from notes would be my own judgement, and the instructions say not to make it. So I have placed no item here.
- The facts above that usually come from note tables stay under "Seen in the statements", unsplit:
  - the warranty rollforward;
  - purchase commitments;
  - the Brazilian tax matter;
  - unrecognized tax benefits;
  - guarantees;
  - commitments to private companies;
  - segment revenue and cost;
  - share-based compensation.
- A later split has no marker to split on. It should not read this empty section as "no findings in the notes".
