<!-- the quote gate removed 3 item(s) from this copy; input_manifest.json lists each with its reason -->
# ADTN — numbers reader — 10-Q 0001193125-26-331632 (period ended 2026-06-30)

## Before the items

**Inputs read in full.** input_trends.json, input_numbers.json, input_8k.md (8-K 0001193125-26-331458, filed 2026-08-04) and input_prior_predictions.md. None of them holds prices, returns, short interest, another company's data, a prior probability or an outcome window.

**Prior flags.** None are on record. input_prior_predictions.md reads: "None on record. This company has no earlier run under the given run root".

**Inputs this run lacks.**
- My directory holds no articulation-check file, no restatement-trace file and no fourth-quarter-derivation file. So I cannot write any articulation-gap item, and no derived fourth-quarter value exists for me to read.
- **No restated prior value.** Facts in input_numbers.json carry `superseded_by` where a later filing re-reports them. None of the superseded rows I read prints a value that differs from the later filing's value for the same paragraph_id. The one exception differs only in precision: the allowance, covered as an item below. So no item reports a restated prior value.

**A period the record does not reach.** quarters-back-2 (target end 2025-12-30) has no cells. The reason the table gives is: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". No derived value for that quarter is in my input. As a result, the cells for quarters-back-3 and quarters-back-1 have no quarter-over-quarter change against it.

**Printed but not quotable** (no paragraph_id). These are mentioned here only and are not items:
- **R&D-capitalized baseline for years-back-0.** It prints:
  - earnings_with_rnd_capitalized -16475200.0;
  - research_and_development_asset 627664400.0;
  - research_and_development_amortization 175095200.0.
  
  Two fields are missing. book_value_with_rnd_capitalized has no StockholdersEquity row for 2025-12-31. capitalized_development_cost is missing because the record "tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
- **8-K item-code list and late-filing list.** These lines carry no [id].
  - Item 4.02 (non-reliance) filings: 2025-05-13, 2024-02-20, 2023-08-10.
  - Late-filing notices: NT 10-Q 2025-05-13 (listed "for the period ended 2025-05-13"), NT 10-K 2024-02-29, NT 10-Q 2023-08-10, NT 10-Q 2019-08-12.
  - An item 2.02 filing on 2026-07-22, ahead of this 2026-08-04 release.
  - Items 1.01, 1.02 and 2.03 on 2026-07-23.
  - Items 5.02 and 8.01 on 2026-06-26, and item 5.02 on 2026-04-07.

**Facts seen in my earlier reading but not written as items.** I could not re-confirm their dimensional paragraph_ids character for character, and an item I cannot quote is not written:
- receivables held with a factor (3700000 at 2026-06-30);
- developed technology acquired in the half year (16700000);
- redeemable non-controlling interest redemption value (14168000 at 2026-06-30; 49615000 at 2025-12-31);
- equity-method ownership (0.281 at 2026-06-30; 0.292 at 2025-12-31);
- remaining performance obligation (214200000 at 2026-06-30; 209700000 at 2025-12-31);
- the Wells Fargo cash thresholds in the 10-K.

**How expected_direction is filled.**
- Trend items: the sign of the change the table itself prints. For a quarter that is year_over_year against quarters-back-4; for a year it is year_over_year against years-back-1.
- 8-K items: "up" or "down" only where the release itself states a direction.
- Everything else is "none", including every cell where no change is printed. Nothing here is computed.

## Seen in the statements

### Trend table — quarter ended 2026-06-30 (quarters-back-0)

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_trend_cell",
  "what_changed": "insufficient. The table cannot fill accruals over total assets for the quarter ended 2026-06-30 because the record has no three-month operating cash flow row for 2026-04-01..2026-06-30. Its two change fields read 'accruals_over_total_assets is not filled in quarters-back-0'. No value, change or position exists. The 8-K prints a three-month operating cash flow figure (see liquidity_and_capital_release_quarterly_operating_cash_flow_row), but no accrual ratio has been computed from it, and none is here.",
  "account": "accruals over total assets: (net income - operating cash flow) / assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-331632:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend_cell",
  "what_changed": "Bad-debt reserve ratio is 0.0075245633582705085, with inputs allowance 1560000.0 and receivables 205761000.0. Change against quarters-back-1 is -8.395707926547348e-05; against quarters-back-4 it is -5.2563115896187874e-05. It is the third highest of the 7 filled quarters. The prior quarter's cell is the highest of the 7 (see estimates_and_discretion_bad_debt_reserve_ratio_prior_quarter_peak).",
  "account": "allowance for doubtful accounts / (receivables + allowance)",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"third highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend_cell",
  "what_changed": "Current contract liabilities over quarterly revenue is 0.2799648581164235, with inputs contract liabilities 78711000.0 and revenue 281146000.0. Change against quarters-back-1 is -0.037254439577276977; against quarters-back-4 it is 0.0434406454615576. It is the second highest of the 7 filled quarters. The prior quarter's cell is the highest.",
  "account": "current contract liabilities (unearned revenue) / revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"second highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend_cell",
  "what_changed": "Days sales of inventory is 107.21971838934508, with inputs inventory 208778000.0 and cost of revenue 177195000.0 tagged CostOfRevenue. Change against quarters-back-1 is -1.448608223325209; against quarters-back-4 it is -24.276880946171104. It is the lowest of the 6 filled quarters on the same concepts. One other filled quarter rests on a different cost concept and is not compared (see the tag-change items).",
  "account": "inventory / cost of revenue * days in period",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters on the same concepts; 1 other filled quarter rests on a different concept and is not compared\"",
  "paragraph_id": "0001193125-26-331632:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend_cell",
  "what_changed": "Days sales outstanding is 66.59974177117938, with inputs receivables 205761000.0 and revenue 281146000.0. Change against quarters-back-1 is -1.1860638956480756; against quarters-back-4 it is 10.033547436140822. It is the fourth highest of the 7 filled quarters.",
  "account": "receivables / revenue * days in period",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"fourth highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend_cell",
  "what_changed": "Gross margin is 0.36974027729364817, with inputs revenue 281146000.0 and cost of revenue 177195000.0 tagged CostOfRevenue. Change against quarters-back-1 is -0.025203900331261797; against quarters-back-4 it is -0.003462070783071758. It is the second lowest of the 6 filled quarters on the same concepts. One other filled quarter rests on a different cost concept and is not compared.",
  "account": "(revenue - cost of revenue) / revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters on the same concepts; 1 other filled quarter rests on a different concept and is not compared\"",
  "paragraph_id": "0001193125-26-331632:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend_cell",
  "what_changed": "insufficient. The table cannot fill the inventory reserve ratio for the quarter ended 2026-06-30: InventoryValuationReserves is in the record, but not for 2026-06-30. No value, change or position exists. This metric has no filled quarter anywhere in the window. The only filled periods are the years 2021 to 2023 (see estimates_and_discretion_inventory_reserve_ratio_last_filled_year).",
  "account": "inventory valuation reserve / inventory",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-331632:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend_cell",
  "what_changed": "insufficient. The table cannot fill the non-GAAP gap in any period, because companyfacts holds no non-GAAP measure. No value, change or position exists. The 8-K prints a non-GAAP net income line (see earnings_quality_release_non_gaap_net_income_row). No gap has been computed from it, and none is here.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001193125-26-331632:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend_cell",
  "what_changed": "Receivables over quarterly revenue is 0.7318652941887844, with inputs receivables 205761000.0 and revenue 281146000.0. Change against quarters-back-1 is -0.02131032433152069; against quarters-back-4 it is 0.11025876303451454. It is the fourth highest of the 7 filled quarters.",
  "account": "accounts receivable, net / revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"fourth highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend_cell",
  "what_changed": "Soft-asset share is 0.8241349054446194, with inputs assets 1149961000.0, cash 79236000.0 and PP&E 123002000.0. Change against quarters-back-1 is 0.003128160678289804; against quarters-back-4 it is 0.003537928559899872. It is the second highest of the 7 filled quarters.",
  "account": "(assets - PP&E - cash) / assets",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"second highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend_cell",
  "what_changed": "insufficient. The table cannot fill the warranty reserve ratio for the quarter ended 2026-06-30: none of the three warranty-accrual concepts is in the record for 2026-06-30. No value, change or position exists. The last filled quarter is the one ended 2024-12-31 (see estimates_and_discretion_warranty_reserve_ratio_last_filled_quarter).",
  "account": "product warranty accrual / revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-331632:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

### Trend table — year ended 2025-12-31 (years-back-0)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend_cell",
  "what_changed": "Accruals over total assets for 2025 is -0.14564053091217632, with inputs net income -45656000.0, operating cash flow 129767000.0 and assets 1204493000.0. Change against years-back-1 is 0.3353675456172295. It is the second lowest of the 5 filled years. The 2024 cell is the lowest of the 5.",
  "account": "(net income - operating cash flow) / assets",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend_cell",
  "what_changed": "Bad-debt reserve ratio at 2025-12-31 is 0.006216834508620079, with inputs allowance 1318000.0 and receivables 210687000.0. Change against years-back-1 is -0.0010323708669445226. It is the second highest of the 5 filled years.",
  "account": "allowance for doubtful accounts / (receivables + allowance)",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend_cell",
  "what_changed": "Current contract liabilities over annual revenue for 2025 is 0.08077176102387233, with inputs contract liabilities 87541000.0 and revenue 1083807000.0. Change against years-back-1 is 0.023656926621236647. It is the highest of the 5 filled years.",
  "account": "current contract liabilities (unearned revenue) / revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend_cell",
  "what_changed": "Days sales of inventory for 2025 is 117.72954255948999, with inputs inventory 215736000.0 and cost of revenue 668852000.0 tagged CostOfRevenue. Change against years-back-1 is -42.20513690241499. It is the lowest of the 4 filled years on the same concepts. One other filled year (2021) rests on a different cost concept and is not compared.",
  "account": "inventory / cost of revenue * days in period",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001193125-26-331632:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend_cell",
  "what_changed": "Days sales outstanding for 2025 is 70.95428890937224, with inputs receivables 210687000.0 and revenue 1083807000.0. Change against years-back-1 is 0.33808897873240085. It is the third highest of the 5 filled years.",
  "account": "receivables / revenue * days in period",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend_cell",
  "what_changed": "Gross margin for 2025 is 0.38286798295268437, with inputs revenue 1083807000.0 and cost of revenue 668852000.0 tagged CostOfRevenue. Change against years-back-1 is 0.03155447506296699. It is the highest of the 4 filled years on the same concepts. One other filled year (2021) rests on a different cost concept and is not compared.",
  "account": "(revenue - cost of revenue) / revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001193125-26-331632:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend_cell",
  "what_changed": "insufficient. The table cannot fill the inventory reserve ratio for 2025: InventoryValuationReserves is in the record, but not for 2025-12-31. Its year-over-year field reads 'inventory_reserve_ratio is not filled in years-back-0'. No value, change or position exists. The record's inventory-reserve history stops at 2023-12-31.",
  "account": "inventory valuation reserve / inventory",
  "expected_direction": "none",
  "horizon": "year ended 2025-12-31",
  "quote": "\"missing\": \"no row for inventory_reserve in 2025-12-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-331632:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend_cell",
  "what_changed": "insufficient. The table cannot fill the non-GAAP gap for 2025, or for any year, because companyfacts holds no non-GAAP measure. No value, change or position exists.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "year ended 2025-12-31",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001193125-26-331632:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend_cell",
  "what_changed": "Receivables over annual revenue for 2025 is 0.1943953120804719, with inputs receivables 210687000.0 and revenue 1083807000.0. Change against years-back-1 is 0.001454875111510573. It is the third highest of the 5 filled years.",
  "account": "accounts receivable, net / revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend_cell",
  "what_changed": "Soft-asset share at 2025-12-31 is 0.8172841187121884, with inputs assets 1204493000.0, cash 95696000.0 and PP&E 124384000.0. Change against years-back-1 is -0.026943267048158637. It is the second lowest of the 5 filled years.",
  "account": "(assets - PP&E - cash) / assets",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend_cell",
  "what_changed": "insufficient. The table cannot fill the warranty reserve ratio for 2025: none of the three warranty-accrual concepts is in the record for 2025-12-31. No value, change or position exists. The last filled year is 2024.",
  "account": "product warranty accrual / revenue",
  "expected_direction": "none",
  "horizon": "year ended 2025-12-31",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-12-31: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-331632:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

### Trend table — short histories and prior-quarter cells

```json
{ "id": "earnings_quality_accruals_over_total_assets_two_filled_quarters_only",
  "what_changed": "insufficient for a quarterly trend. Accruals over total assets is filled in only 2 of the window's quarters, quarters-back-1 and quarters-back-5. Every other quarter lacks a three-month operating cash flow row. The quarters-back-1 value is -0.011806083537892795, with inputs net income -1321000.0, operating cash flow 12670000.0 and assets 1185067000.0. Its year-over-year change against quarters-back-5 is 0.03382433920222884. Two points do not support a trend claim.",
  "account": "(net income - operating cash flow) / assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_prior_quarter_peak",
  "what_changed": "The bad-debt reserve ratio for the quarter ended 2026-03-31 is 0.007608520437535982, with inputs allowance 1652000.0 and receivables 215473000.0. Its year-over-year change against quarters-back-5 is 0.00038266475194417143. It is the highest of the 7 filled quarters, and the current quarter's cell sits just below it.",
  "account": "allowance for doubtful accounts / (receivables + allowance)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_prior_quarter_peak",
  "what_changed": "Current contract liabilities over revenue for the quarter ended 2026-03-31 is 0.3172192976937005, with inputs contract liabilities 90752000.0 and revenue 286086000.0. Its year-over-year change against quarters-back-5 is 0.048962548791607996. It is the highest of the 7 filled quarters. The current quarter is the second highest.",
  "account": "current contract liabilities (unearned revenue) / revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 7 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_last_filled_quarter",
  "what_changed": "insufficient for a quarterly trend. The warranty reserve ratio is filled in only 2 quarters, the ones ended 2024-09-30 and 2024-12-31. The 2024-12-31 cell prints 0.018579216971653517, with ProductWarrantyAccrual 4512000.0 from filing 0000950170-25-075366. Since then, no warranty-accrual concept is in the record for any quarter-end.",
  "account": "product warranty accrual / revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2024-12-31; no later filled quarter",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0001193125-26-331632:trends:warranty_reserve_ratio:2024-10-01..2024-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_last_filled_year",
  "what_changed": "The last filled year of the warranty reserve ratio is 2024, at 0.004889890757759667. Its change against years-back-2 is -0.0007188465148884925, and it is the lowest of the 4 filled years. The warranty accrual input is ProductWarrantyAccrual 4512000.0 from 0000950170-25-075366, filed 2025-05-20. The 2025 cell is unfilled.",
  "account": "product warranty accrual / revenue",
  "expected_direction": "down",
  "horizon": "year ended 2024-12-31 against year ended 2023-12-31",
  "quote": "\"position_in_history\": \"lowest of the 4 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:warranty_reserve_ratio:2024-01-01..2024-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_last_filled_year",
  "what_changed": "insufficient for any current read. The inventory reserve ratio is filled for 2021, 2022 and 2023 only. The last filled cell (2023) is 0.23056178278915943, with inputs reserve 83100000.0 and inventory 360424000.0. Its change against years-back-3 is 0.09723811737074531. Neither 2024 nor 2025 nor any quarter in the window has a reserve row.",
  "account": "inventory valuation reserve / inventory",
  "expected_direction": "up",
  "horizon": "year ended 2023-12-31 against year ended 2022-12-31",
  "quote": "\"position_in_history\": \"second highest of the 3 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:inventory_reserve_ratio:2023-01-01..2023-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_earliest_filled_year",
  "what_changed": "The earliest filled inventory reserve ratio (2021) is 0.3188196524436883, with inputs reserve 44600000.0 and inventory 139891000.0. It is the highest of the 3 filled years. Its year-over-year field reads 'the year 1 back is outside the requested window'.",
  "account": "inventory valuation reserve / inventory",
  "expected_direction": "none",
  "horizon": "year ended 2021-12-31",
  "quote": "\"position_in_history\": \"highest of the 3 filled years\"",
  "paragraph_id": "0001193125-26-331632:trends:inventory_reserve_ratio:2021-01-01..2021-12-31" }
```

### Trend table — change of tag (a period resting on a different concept)


```json
{ "id": "articulation_and_the_filed_history_days_sales_of_inventory_cost_concept_change_quarterly",
  "what_changed": "Change of tag. Days sales of inventory for the quarter ended 2024-12-31 is 156.9724193716731. It rests on CostOfGoodsAndServicesSold 153296000.0 from 0000950170-25-075366, against CostOfRevenue in every other filled quarter, so it is compared with nothing.",
  "account": "cost of revenue concept behind days sales of inventory",
  "expected_direction": "none",
  "horizon": "quarter ended 2024-12-31",
  "quote": "\"position_in_history\": \"the only filled quarter on the same concepts; 6 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0001193125-26-331632:trends:days_sales_of_inventory:2024-10-01..2024-12-31" }
```


```json
{ "id": "articulation_and_the_filed_history_days_sales_of_inventory_cost_concept_change_annual",
  "what_changed": "Change of tag. Days sales of inventory for 2021 is 148.16080864238728 and rests on CostOfGoodsAndServicesSold. The other four filled years rest on CostOfRevenue, so 2021 is compared with nothing.",
  "account": "cost of revenue concept behind days sales of inventory",
  "expected_direction": "none",
  "horizon": "year ended 2021-12-31",
  "quote": "\"position_in_history\": \"the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared\"",
  "paragraph_id": "0001193125-26-331632:trends:days_sales_of_inventory:2021-01-01..2021-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_cost_of_revenue_tagged_under_two_concepts",
  "what_changed": "The current 10-Q states cost of revenue for the quarter ended 2026-06-30 under us-gaap:CostOfGoodsAndServicesSold as well as under us-gaap:CostOfRevenue. The trend table's input for this quarter is CostOfRevenue 177195000.0. This dual tagging is the same pair of concepts whose alternation causes the tag-change exclusions above.",
  "account": "cost of revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"177195000\"",
  "paragraph_id": "0001193125-26-331632:facts:CostOfGoodsAndServicesSold:2026-04-01..2026-06-30" }
```

### Numeric facts

```json
{ "id": "results_against_expectations_quarter_revenue_fact",
  "what_changed": "Revenue for the quarter ended 2026-06-30 is tagged 281146000. The same filing tags the quarter ended 2025-06-30 at 265068000.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"281146000\"",
  "paragraph_id": "0001193125-26-331632:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "results_against_expectations_quarter_operating_loss_fact",
  "what_changed": "Operating loss for the quarter ended 2026-06-30 is tagged -10071000. The prior-year quarter is tagged -13318000 in the same filing. The 8-K prints operating income of 6,375 thousand for the quarter ended 2026-03-31.",
  "account": "operating income (loss)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"-10071000\"",
  "paragraph_id": "0001193125-26-331632:facts:OperatingIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "results_against_expectations_quarter_net_loss_fact",
  "what_changed": "Net loss attributable to the company for the quarter ended 2026-06-30 is tagged -10905000. The prior-year quarter is tagged -20531000.",
  "account": "net income (loss) attributable to ADTRAN Holdings",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"-10905000\"",
  "paragraph_id": "0001193125-26-331632:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "results_against_expectations_quarter_diluted_loss_per_share_fact",
  "what_changed": "Diluted loss per share for the quarter ended 2026-06-30 is tagged -0.13.",
  "account": "diluted earnings (loss) per share",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"-0.13\"",
  "paragraph_id": "0001193125-26-331632:facts:EarningsPerShareDiluted:2026-04-01..2026-06-30" }
```

```json
{ "id": "across_documents_gain_on_investments_fact_sign",
  "what_changed": "GainLossOnInvestments for the quarter ended 2026-06-30 is tagged positive (5274000). On that concept a positive value is a gain. The 8-K's statement of loss labels the same 5,274 line 'Net investment loss', while its other-income reconciliation labels it 'Net investment gain (loss)'. See the two across_documents release items.",
  "account": "net investment gain (loss)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"5274000\"",
  "paragraph_id": "0001193125-26-331632:facts:GainLossOnInvestments:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_loss_on_investments_prior_quarter_fact",
  "what_changed": "GainLossOnInvestments for the quarter ended 2026-03-31 is tagged -850000 in the Q1 10-Q. The sign of the investment line differs between consecutive quarters.",
  "account": "net investment gain (loss)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"value\": \"-850000\"",
  "paragraph_id": "0001193125-26-205276:facts:GainLossOnInvestments:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_quarter_fact",
  "what_changed": "The effective tax rate for the quarter ended 2026-06-30 is tagged -0.10. The prior-year quarter is tagged -0.059. The rate is negative: tax expense on a pre-tax loss.",
  "account": "effective income tax rate",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"-0.10\"",
  "paragraph_id": "0001193125-26-331632:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_half_year_fact",
  "what_changed": "The effective tax rate for the six months ended 2026-06-30 is tagged -0.534. The six months ended 2025-06-30 is tagged -0.023.",
  "account": "effective income tax rate",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"-0.534\"",
  "paragraph_id": "0001193125-26-331632:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_prior_quarter_fact",
  "what_changed": "The effective tax rate for the quarter ended 2026-03-31 is tagged 0.673 in the Q1 10-Q, so the effective rate swung widely across the two quarters of 2026. Only these printed rates exist here; no rate is derived.",
  "account": "effective income tax rate",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"value\": \"0.673\"",
  "paragraph_id": "0001193125-26-205276:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-03-31" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_half_year_fact",
  "what_changed": "Operating cash flow for the six months ended 2026-06-30 is tagged 38585000, against 75341000 for the six months ended 2025-06-30. The record has no three-month figure, which is why the quarterly accrual cell is empty.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"38585000\"",
  "paragraph_id": "0001193125-26-331632:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_fact",
  "what_changed": "Cash and cash equivalents at 2026-06-30 are tagged 79236000, against 95696000 at 2025-12-31.",
  "account": "cash and cash equivalents",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "\"value\": \"79236000\"",
  "paragraph_id": "0001193125-26-331632:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_charge_half_year_fact",
  "what_changed": "The inventory reserve provision for the six months ended 2026-06-30 is tagged 277000, against 9176000 for the six months ended 2025-06-30. The 8-K labels the line 'Inventory reserves'. The company tags it us-gaap:InventoryLIFOReservePeriodCharge, not a valuation-reserve concept. That may be why the trend table finds no InventoryValuationReserves row for these periods and leaves the inventory reserve ratio unfilled.",
  "account": "inventory reserve provision (cash flow add-back)",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"277000\"",
  "paragraph_id": "0001193125-26-331632:facts:InventoryLIFOReservePeriodCharge:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_charge_negative_full_year_fact",
  "what_changed": "The 10-K tags the inventory reserve charge for 2025 as negative (-2541000), a net release. The same concept is 5316000 for 2024 and 25546000 for 2023.",
  "account": "inventory reserve provision",
  "expected_direction": "none",
  "horizon": "year ended 2025-12-31",
  "quote": "\"value\": \"-2541000\"",
  "paragraph_id": "0001193125-26-073878:facts:InventoryLIFOReservePeriodCharge:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_charge_prior_quarter_fact",
  "what_changed": "The Q1 10-Q tags the inventory reserve charge for the quarter ended 2026-03-31 at 143000, against 3339000 for the quarter ended 2025-03-31.",
  "account": "inventory reserve provision",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"value\": \"143000\"",
  "paragraph_id": "0001193125-26-205276:facts:InventoryLIFOReservePeriodCharge:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_change_half_year_fact",
  "what_changed": "IncreaseDecreaseInAccountsReceivable for the six months ended 2026-06-30 is tagged -1758000, against -25754000 for the six months ended 2025-06-30. On this concept a negative value is a decrease in receivables, so receivables released less cash than in the prior-year half.",
  "account": "change in accounts receivable",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"-1758000\"",
  "paragraph_id": "0001193125-26-331632:facts:IncreaseDecreaseInAccountsReceivable:2026-01-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized_quarter_fact",
  "what_changed": "Revenue recognised from the opening contract-liability balance is tagged 19200000 for the quarter ended 2026-06-30, against 12800000 for the quarter ended 2025-06-30. The six-month figures are 42400000 and 34700000.",
  "account": "revenue recognised from contract liabilities",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"value\": \"19200000\"",
  "paragraph_id": "0001193125-26-331632:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-04-01..2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_purchase_obligation_fact",
  "what_changed": "The purchase obligation at 2026-06-30 is tagged 232000000. Earlier filings tag 223700000 at 2026-03-31 (Q1 10-Q) and 205900000 at 2025-12-31 (10-K).",
  "account": "purchase obligations",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "\"value\": \"232000000\"",
  "paragraph_id": "0001193125-26-331632:facts:PurchaseObligation:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_retirement_plan_corrective_liability_fact",
  "what_changed": "A current employee-related liability on the 401(k) savings plan member is tagged 1400000 at 2026-06-30. The 8-K says a $1.4 million provision for a 401(k) plan corrective action was reversed in the quarter after an IRS compliance statement. A liability of the same amount still tagged at 2026-06-30 is something the inputs do not reconcile.",
  "account": "employee-related liabilities, 401(k) plan",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "\"value\": \"1400000\"",
  "paragraph_id": "0001193125-26-331632:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-30:us-gaap:RetirementPlanTypeAxis=adtn:FourZeroOneKSavingsPlansMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_retirement_plan_corrective_liability_year_end_fact",
  "what_changed": "The Q1 10-Q tags the same 401(k)-plan employee liability at 1400000 for 2025-12-31.",
  "account": "employee-related liabilities, 401(k) plan",
  "expected_direction": "none",
  "horizon": "2025-12-31",
  "quote": "\"value\": \"1400000\"",
  "paragraph_id": "0001193125-26-205276:facts:EmployeeRelatedLiabilitiesCurrent:2025-12-31:us-gaap:RetirementPlanTypeAxis=adtn:FourZeroOneKSavingsPlansMember" }
```

```json
{ "id": "estimates_and_discretion_internally_developed_technology_payments_fact",
  "what_changed": "Cash paid for intangibles in the six months ended 2026-06-30 is tagged 16737000, against 20444000 a year earlier. The 8-K labels this 'Intangibles - internally developed technology'. Internally developed technology is being capitalised, yet the trend table's capitalised-development baseline is empty, because CapitalizedComputerSoftwareAdditions is never tagged.",
  "account": "payments to acquire intangible assets (internally developed technology)",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"16737000\"",
  "paragraph_id": "0001193125-26-331632:facts:PaymentsToAcquireIntangibleAssets:2026-01-01..2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_new_credit_agreement_capacity_fact",
  "what_changed": "A subsequent event dated 2026-07-21: a New Credit Agreement with maximum borrowing capacity tagged 350000000. The 10-K tags the prior Wells Fargo facility at the same 350000000 capacity, with 25000000 drawn. The 8-K item list shows items 1.01, 1.02 and 2.03 filed 2026-07-23, but that list is not quotable.",
  "account": "revolving credit facility",
  "expected_direction": "none",
  "horizon": "2026-07-21, after the balance-sheet date",
  "quote": "\"value\": \"350000000\"",
  "paragraph_id": "0001193125-26-331632:facts:LineOfCreditFacilityMaximumBorrowingCapacity:2026-07-21:us-gaap:CreditFacilityAxis=adtn:NewCreditAgreementMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "liquidity_and_capital_new_credit_agreement_current_capacity_fact",
  "what_changed": "The New Credit Agreement's current borrowing capacity at 2026-07-21 is tagged 50000000, against the 350000000 maximum.",
  "account": "revolving credit facility, current capacity",
  "expected_direction": "none",
  "horizon": "2026-07-21",
  "quote": "\"value\": \"50000000\"",
  "paragraph_id": "0001193125-26-331632:facts:LineOfCreditFacilityCurrentBorrowingCapacity:2026-07-21:us-gaap:CreditFacilityAxis=adtn:NewCreditAgreementMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "liquidity_and_capital_new_credit_agreement_commitment_fee_fact",
  "what_changed": "The New Credit Agreement's commitment fee is tagged 0.0025. Its basis spreads are tagged at minimum and maximum levels for base-rate and term-benchmark loans; for example, the base-rate maximum is 0.0225.",
  "account": "revolving credit facility, commitment fee",
  "expected_direction": "none",
  "horizon": "2026-07-21",
  "quote": "\"value\": \"0.0025\"",
  "paragraph_id": "0001193125-26-331632:facts:LineOfCreditFacilityCommitmentFeePercentage:2026-07-21..2026-07-21:us-gaap:CreditFacilityAxis=adtn:NewCreditAgreementMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "controls_audit_and_filings_prior_quarter_diluted_shares_tagged_to_earlier_year",
  "what_changed": "The Q1 10-Q tags diluted weighted shares of 80321000 to the context 2024-01-01..2024-03-31. It also tags basic and diluted EPS of -0.01 to that context. These figures equal what the 8-K prints for the quarter ended 2026-03-31 (80,321 thousand shares and EPS of (0.01)). The 2024 context looks mis-dated in the Q1 filing's XBRL.",
  "account": "XBRL tagging of the Q1 10-Q",
  "expected_direction": "none",
  "horizon": "Q1 10-Q filed 2026-05-05",
  "quote": "\"value\": \"80321000\"",
  "paragraph_id": "0001193125-26-205276:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2024-01-01..2024-03-31" }
```

```json
{ "id": "controls_audit_and_filings_prior_quarter_remaining_performance_obligation_scale",
  "what_changed": "The Q1 10-Q tags the remaining performance obligation on the non-cancellable maintenance, SaaS and hardware-order member at 159200, with decimals -2. The 10-K tags remaining performance obligations at 209700000. The Q1 value looks mis-scaled. Only the printed figures are compared; nothing is computed.",
  "account": "XBRL tagging, remaining performance obligation",
  "expected_direction": "none",
  "horizon": "2026-03-31",
  "quote": "\"value\": \"159200\"",
  "paragraph_id": "0001193125-26-205276:facts:RevenueRemainingPerformanceObligation:2026-03-31:srt:ProductOrServiceAxis=adtn:Non-CancellableContractualMaintenanceAgreementsContractualSaasAndSubscriptionServicesAndHardwareOrdersMember" }
```

```json
{ "id": "controls_audit_and_filings_prior_quarter_developed_technology_acquired_scale",
  "what_changed": "The Q1 10-Q tags developed technology acquired in the quarter ended 2026-03-31 at 8400, with decimals -2, while the cash-flow line for internally developed technology runs in the millions. The value looks mis-scaled.",
  "account": "XBRL tagging, finite-lived intangibles acquired (developed technology)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"value\": \"8400\"",
  "paragraph_id": "0001193125-26-205276:facts:FinitelivedIntangibleAssetsAcquired1:2026-01-01..2026-03-31:us-gaap:FiniteLivedIntangibleAssetsByMajorClassAxis=us-gaap:DevelopedTechnologyRightsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_allowance_stated_at_two_precisions",
  "what_changed": "The allowance for doubtful accounts at 2026-06-30 is tagged twice under one paragraph_id: 1560000 (decimals -3, the trend input) and 1600000 (decimals -5). The two differ only in rounding precision. This is not a restatement. The 2025-12-31 allowance likewise appears as 1318000 and 1300000.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "\"value\": \"1600000\"",
  "paragraph_id": "0001193125-26-331632:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30" }
```

### 8-K earnings release figures (exhibit 99.1, 0001193125-26-331458)

```json
{ "id": "results_against_expectations_release_revenue_growth_statement",
  "what_changed": "The release states second-quarter revenue of $281.1 million, up 6.1% year over year.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "Revenue: $281.1 million, up 6.1 % year-over-year.",
  "paragraph_id": "0001193125-26-331458:8k_2_02:5" }
```

```json
{ "id": "results_against_expectations_release_gross_margin_row",
  "what_changed": "The release prints GAAP gross margin of 37.0% for the quarter ended 2026-06-30, 39.5% for the quarter ended 2026-03-31 and 37.3% for the quarter ended 2025-06-30. The six-month figures are 38.2% and 37.9%.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Gross Margin |  |  | 37.0 | % |  |  | 39.5 | % |  |  | 37.3 | % |  |  |  | 38.2 | % |  |  | 37.9 | % |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:57" }
```

```json
{ "id": "results_against_expectations_release_operating_income_row",
  "what_changed": "The release prints an operating loss of (10,071) thousand for the quarter ended 2026-06-30 and operating income of 6,375 thousand for the quarter ended 2026-03-31. The quarter ended 2025-06-30 shows (13,318) thousand. The six-month figures are (3,696) and (17,286) thousand.",
  "account": "operating income (loss)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Operating (Loss) Income |  | $ | (10,071 | ) |  | $ | 6,375 |  |  | $ | (13,318 | ) |  |  | $ | (3,696 | ) |  | $ | (17,286 | ) |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:88" }
```

```json
{ "id": "results_against_expectations_release_operating_margin_row",
  "what_changed": "The release prints a GAAP operating margin of -3.6% for the quarter ended 2026-06-30, 2.2% for the quarter ended 2026-03-31 and -5.0% for the quarter ended 2025-06-30. Non-GAAP operating margin is 3.8%, 6.9% and 3.0% for the same quarters.",
  "account": "operating margin",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Operating Margin |  |  | -3.6 | % |  |  | 2.2 | % |  |  | -5.0 | % |  |  |  | -0.7 | % |  |  | -3.4 | % |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:88" }
```

```json
{ "id": "results_against_expectations_release_diluted_loss_per_share_statement",
  "what_changed": "The release states a GAAP diluted loss per share of $0.13 alongside non-GAAP diluted earnings per share of $0.04.",
  "account": "earnings (loss) per share",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "GAAP diluted loss per share of $0.13; non-GAAP diluted earnings per share of $0.04.",
  "paragraph_id": "0001193125-26-331458:8k_2_02:9" }
```

```json
{ "id": "results_against_expectations_third_quarter_outlook",
  "what_changed": "Guidance for the third quarter of 2026: revenue of $275.0 million to $295.0 million and a non-GAAP operating margin of 1.5% to 5.5%. No GAAP reconciliation of the guidance is given.",
  "account": "revenue and non-GAAP operating margin guidance",
  "expected_direction": "none",
  "horizon": "quarter ending 2026-09-30",
  "quote": "For the third quarter of 2026, the Company expects revenue to be within a range of $275.0 million to $295.0 million. Non-GAAP operating margin is expected to be within a range of 1.5% to 5.5%.",
  "paragraph_id": "0001193125-26-331458:8k_2_02:14" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_near_term_factors_statement",
  "what_changed": "The CEO attributes the second-quarter results to 'a specific set of near-term factors' without naming them in the release.",
  "account": "management commentary on quarterly results",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "While our second quarter results were affected by a specific set of near-term factors, it does not change the underlying strength or trajectory of our business.",
  "paragraph_id": "0001193125-26-331458:8k_2_02:11" }
```

```json
{ "id": "liquidity_and_capital_release_quarterly_operating_cash_flow_row",
  "what_changed": "The release prints three-month operating cash flow: 25,915 thousand for the quarter ended 2026-06-30, 12,670 thousand for the quarter ended 2026-03-31 and 32,160 thousand for the quarter ended 2025-06-30. This three-month figure exists only in the release, not in the companyfacts record the trend table uses. No accrual ratio is computed from it here.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Net cash provided by operating activities |  | $ | 25,915 |  |  | $ | 12,670 |  |  | $ | 32,160 |  |  |  | $ | 38,585 |  |  | $ | 75,341 |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:126" }
```


```json
{ "id": "estimates_and_discretion_release_inventory_reserves_row",
  "what_changed": "The cash-flow add-back for inventory reserves is 277 thousand for the six months ended 2026-06-30, against 9,176 thousand for the six months ended 2025-06-30.",
  "account": "inventory reserves",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Inventory reserves |  |  | 277 |  |  |  | 9,176 |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "revenue_recognition_release_receivables_change_row",
  "what_changed": "Cash from the change in accounts receivable is 1,758 thousand for the six months ended 2026-06-30, against 25,754 thousand for the six months ended 2025-06-30.",
  "account": "change in accounts receivable",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Accounts receivable, net |  |  | 1,758 |  |  |  | 25,754 |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "revenue_recognition_release_securitized_receivables_row",
  "what_changed": "Payments for beneficial interests in securitized accounts receivable are (478) thousand for the six months ended 2026-06-30, against (49) thousand a year earlier. This shows a receivables securitization or factoring arrangement is in use.",
  "account": "beneficial interests in securitized receivables",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Payments for beneficial interests in securitized accounts receivable |  |  | (478 | ) |  |  | (49 | ) |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "revenue_recognition_release_current_unearned_revenue_row",
  "what_changed": "Current unearned revenue is 78,711 thousand at 2026-06-30, against 87,541 thousand at 2025-12-31.",
  "account": "unearned revenue, current",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "| Unearned revenue |  | 78,711 |  |  |  | 87,541 |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:41" }
```

```json
{ "id": "revenue_recognition_release_noncurrent_unearned_revenue_row",
  "what_changed": "Non-current unearned revenue is 24,959 thousand at 2026-06-30, against 27,143 thousand at 2025-12-31.",
  "account": "unearned revenue, non-current",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "| Non-current unearned revenue |  | 24,959 |  |  |  | 27,143 |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:41" }
```

```json
{ "id": "liquidity_and_capital_release_accrued_expenses_change_row",
  "what_changed": "The change in accrued expenses and other liabilities is (20,468) thousand for the six months ended 2026-06-30, against (11,305) thousand a year earlier.",
  "account": "accrued expenses and other liabilities (cash-flow change)",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Accrued expenses and other liabilities |  |  | (20,468 | ) |  |  | (11,305 | ) |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "liquidity_and_capital_release_accounts_payable_change_row",
  "what_changed": "The change in accounts payable is 10,941 thousand for the six months ended 2026-06-30, against (6,242) thousand a year earlier.",
  "account": "accounts payable (cash-flow change)",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Accounts payable |  |  | 10,941 |  |  |  | (6,242 | ) |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "estimates_and_discretion_release_internally_developed_technology_row",
  "what_changed": "The investing outflow for internally developed technology is (16,737) thousand for the six months ended 2026-06-30, against (20,444) thousand a year earlier. The release's non-GAAP measures exclude 'purchases of property, plant and equipment, and developed technologies' when computing free cash flow.",
  "account": "capitalised internally developed technology",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Intangibles - internally developed technology |  |  | (16,737 | ) |  |  | (20,444 | ) |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "liquidity_and_capital_release_redemption_of_noncontrolling_interest_row",
  "what_changed": "Cash paid to redeem the redeemable non-controlling interest is (13,766) thousand for the six months ended 2026-06-30, against (19,363) thousand a year earlier. The carrying amount on the balance sheet is 359,160 thousand at 2026-06-30, against 373,328 thousand at 2025-12-31.",
  "account": "redeemable non-controlling interest",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "| Redemption of redeemable non-controlling interest |  |  | (13,766 | ) |  |  | (19,363 | ) |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:51" }
```

```json
{ "id": "earnings_quality_release_non_gaap_net_income_row",
  "what_changed": "The release prints non-GAAP net income attributable to the company of 2,830 thousand for the quarter ended 2026-06-30, against a GAAP net loss attributable of (10,905) thousand. The quarter ended 2026-03-31 shows 10,662 and the quarter ended 2025-06-30 shows (1,750). The trend table's non-GAAP gap is unfilled because these figures are not in companyfacts. No gap is computed here.",
  "account": "non-GAAP net income attributable to ADTRAN Holdings",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Non-GAAP Net Income (Loss) attributable to ADTRAN Holdings, Inc. |  | $ | 2,830 |  |  | $ | 10,662 |  |  | $ | (1,750 | ) |  |  | $ | 13,492 |  |  | $ | 406 |  |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:112" }
```

```json
{ "id": "across_documents_net_investment_line_labelled_loss",
  "what_changed": "The release's condensed statement of loss labels the investment line 'Net investment loss' while printing 5,274 thousand unbracketed for the quarter ended 2026-06-30. The XBRL fact for the same line is a positive GainLossOnInvestments (a gain). The label and the sign disagree.",
  "account": "net investment gain (loss)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Net investment loss |  |  | 5,274 |  |  |  | 3,075 |  |  |  | 4,424 |  |  |  | 1,389 |  |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:45" }
```

```json
{ "id": "across_documents_net_investment_line_labelled_gain_or_loss",
  "what_changed": "The release's other-income reconciliation labels the same line 'Net investment gain (loss)'. It prints 5,274 thousand unbracketed for the quarter ended 2026-06-30 and (850) thousand bracketed for the quarter ended 2026-03-31. The same release thus gives the line two different labels.",
  "account": "net investment gain (loss)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "| Net investment gain (loss) |  |  | 5,274 |  |  |  | (850 | ) |  |  | 3,075 |  |  |  | 4,424 |  |  |  | 1,389 |  |",
  "paragraph_id": "0001193125-26-331458:8k_2_02:98" }
```

```json
{ "id": "controls_audit_and_filings_internal_investigation_fees_prior_year_quarter",
  "what_changed": "Footnote (12) of the operating-expense reconciliation attaches to the 2025 columns, (3,153) thousand in the quarter ended 2025-06-30. It says these professional fees include costs of an internal investigation and related employee exit costs. The same wording appears at footnotes (5), (9) and (18).",
  "account": "professional fees and other expenses (non-GAAP adjustment)",
  "expected_direction": "none",
  "horizon": "quarter and six months ended 2025-06-30",
  "quote": "Includes professional fees related to an internal investigation and related employee exit costs, fees relating to other one-time professional fees and business expenses.",
  "paragraph_id": "0001193125-26-331458:8k_2_02:76" }
```

```json
{ "id": "controls_audit_and_filings_retirement_plan_corrective_action_reversal",
  "what_changed": "In the quarter ended 2026-06-30, professional fees and other expenses (excluded from non-GAAP) net $1.6 million of employee exit costs against a $1.4 million reversal of a 401(k) plan corrective-action provision. The reversal followed an IRS compliance statement approving a retroactive amendment. The operating-income reconciliation's version, footnote (3), cites $2.0 million of exit costs including cost of revenue. The 10-Q still tags a 1400000 401(k)-plan liability at 2026-06-30.",
  "account": "401(k) plan corrective-action provision",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "offset by a $1.4 million reversal of a provision in connection with a 401(k) plan corrective action",
  "paragraph_id": "0001193125-26-331458:8k_2_02:69" }
```

## Seen in the notes

No item is placed here. No fact in input_numbers.json carries a marker for whether its element sat inside a note. Every fact row has only these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, where re-reported, superseded_by.

Without that marker, sorting facts into this section would mean judging which ones came from notes, and the instructions rule that out. So every numeric fact item sits under "Seen in the statements". That includes facts that plausibly come from note tables: purchase obligations, the 401(k)-plan liability, the subsequent-event credit agreement, contract-liability revenue recognised and the Q1 tagging anomalies.

This is a defect in the input: the reader that later splits off notes will have to re-derive the split, because the marker is missing.
