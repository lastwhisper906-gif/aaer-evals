<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# ESE — numbers reader — 10-Q 0001104659-26-093266 (quarter ended 2026-06-30, filed 2026-08-10)

**What I read.** I read all four input files in full:

- input_trends.json
- input_numbers.json, which holds three documents:
  - 10-K 0001104659-25-117276
  - 10-Q 0001104659-26-058482
  - 10-Q 0001104659-26-093266
- input_8k.md: 8-K 0001104659-26-092033, filed 2026-08-06, with its exhibit 99.1 release
- input_prior_predictions.md

The directory holds no prices, no returns, no short interest, no other company's files, no prior probability and no outcome window. This is not a broken run.

**Prior flags.** input_prior_predictions.md says: "None on record. This company has no earlier run under the given run root, so there are no flags, no management explanations and no outcomes to carry forward." No prior flags exist to carry forward.

**What my input does not contain.** I write these as absent; I did not derive any of them.

- **Articulation checks.** No section exists, so I have no Python-computed articulation gap to report. One pair of facts in the numeric facts prints different values for the same period under two tags; it is reported below as a printed difference, not as a computed gap.
- **Restatement traces.** No section exists. Several earlier-filing facts carry `superseded_by`, but every re-reported value I found is printed identically by the later filing. No restated prior value exists in my input.
- **Fourth-quarter derivation.** No output from src/fourth_quarter.py is in my input. No fiscal-fourth-quarter figure exists for me to report.
- **Tag changes.** No trend cell or fact says a period rests on a different concept. No tag-change item exists.
- **In-note markers.** No fact in input_numbers.json carries a marker saying its element sat inside a note.

**Periods the record does not reach.** Two requested quarters have no cells at all:

- **quarters-back-3** (target end 2025-09-30). The reason given: "no quarter ending within 20 days of 2025-09-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
- **quarters-back-7** (target end 2024-10-01). The reason is the same, with the date 2024-10-01.

Because both fiscal fourth quarters are missing, each quarterly position in history ranks against 6 filled quarters only. No quarterly trend claim beyond that ranking is supported.

## Seen in the statements

**Trend table, quarters-back-0 (2026-04-01..2026-06-30, 91 days)**

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarter_cell",
  "what_changed": "Days sales outstanding is 71.79918708539438 (receivables 267493000.0 against quarterly revenue 339027000.0). Change against quarters-back-1 is -2.92466135370681; change against quarters-back-4 is -1.2915520556039155. The table places it lowest of the 6 filled quarters. Six quarters with no fiscal fourth quarters support the ranking only, not a trend.",
  "account": "Accounts receivable, net against revenue (days sales outstanding)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarter_cell",
  "what_changed": "Receivables over revenue is 0.7890020558834547. Change against quarters-back-1 is -0.04126292677322507; change against quarters-back-4 is -0.01419287973191119. Lowest of the 6 filled quarters.",
  "account": "Accounts receivable, net against quarterly revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarter_cell",
  "what_changed": "Days sales of inventory is 110.8275209105454 (inventory 240542000.0 against quarterly cost of revenue 197508000.0). Change against quarters-back-1 is -9.03193782020179; change against quarters-back-4 is -12.929347457679441. Lowest of the 6 filled quarters.",
  "account": "Inventories, net against cost of revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarter_cell",
  "what_changed": "Gross margin is 0.41742693059844793. Change against quarters-back-1 is -0.0070722466848737175; change against quarters-back-4 is 0.005763458417469058. Third lowest of the 6 filled quarters: down on the prior quarter, up on the year-ago quarter.",
  "account": "Gross margin (revenue less cost of revenue, over revenue)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarter_cell",
  "what_changed": "Bad-debt reserve ratio is 0.010036823892970153 (allowance 2712000.0 against receivables 267493000.0). Change against quarters-back-1 is -0.003952787553633989; change against quarters-back-4 is -0.0036664608345180483. Lowest of the 6 filled quarters: the allowance covers a smaller share of receivables than in any other filled quarter.",
  "account": "Allowance for doubtful accounts against gross receivables",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarter_cell",
  "what_changed": "Contract liabilities over quarterly revenue is 0.8499087093358346 (current contract liabilities 288142000.0 against revenue 339027000.0). Change against quarters-back-1 is -0.02098134403568741; change against quarters-back-4 is 0.15615077936256028. Third highest of the 6 filled quarters.",
  "account": "Contract liabilities (current) against quarterly revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarter_cell",
  "what_changed": "Soft-asset share is 0.8973067388759436 (assets 2420003000.0, cash 73236000.0, net PP&E 175282000.0). Change against quarters-back-1 is 0.0066722111399051265; change against quarters-back-4 is -0.0008516805323903753. Second highest of the 6 filled quarters.",
  "account": "Assets other than cash and PP&E, over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001104659-26-093266:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarter_cell_insufficient",
  "what_changed": "insufficient: the table could not fill accruals over total assets for this quarter because no operating-cash-flow row exists for the three-month period. The 10-Q tags operating cash flow year-to-date only, and no quarterly operating cash flow figure exists in my input.",
  "account": "Accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001104659-26-093266:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarter_cell_insufficient",
  "what_changed": "insufficient: the record tags no inventory valuation reserve in any period, so no inventory reserve ratio exists for this quarter.",
  "account": "Inventory valuation reserve against inventory",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001104659-26-093266:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarter_cell_insufficient",
  "what_changed": "insufficient: the table cannot compute a non-GAAP gap because no us-gaap concept carries a non-GAAP measure. The release prints its own adjusted figures, reported below under the release items. No Python-computed gap exists.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001104659-26-093266:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarter_cell_insufficient",
  "what_changed": "insufficient: the warranty accrual concepts exist in the record but not for 2026-06-30, so no warranty reserve ratio exists for this quarter.",
  "account": "Product warranty accrual",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001104659-26-093266:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

**Trend table, years-back-0 (fiscal year 2024-10-01..2025-09-30, 365 days)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_year_cell",
  "what_changed": "Accruals over total assets is 0.023765468463998327. Inputs:\n- net income (NetIncomeLoss): 299223000.0\n- operating cash flow (NetCashProvidedByUsedInOperatingActivities): 241939000.0\n- assets: 2410388000.0\nBoth net income and operating cash flow are totals that include discontinued operations. Change against years-back-1 is 0.037722131613534396. Highest of the 5 filled years.",
  "account": "Accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:accruals_over_total_assets:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_year_cell",
  "what_changed": "Bad-debt reserve ratio is 0.012482522521119026 (allowance 3205000.0 against receivables 253554000.0). Change against years-back-1 is 0.0003224940558000135. Third highest of the 5 filled years.",
  "account": "Allowance for doubtful accounts against gross receivables",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:bad_debt_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_year_cell",
  "what_changed": "Contract liabilities over annual revenue is 0.19772902387099367 (216590000.0 against 1095388000.0). Change against years-back-1 is 0.10977164692526147. Highest of the 5 filled years.",
  "account": "Contract liabilities (current) against annual revenue",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:contract_liabilities_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_year_cell",
  "what_changed": "Days sales of inventory is 125.3337206350908 (inventory 217807000.0 against cost of revenue 634303000.0). Change against years-back-1 is -9.506569250029514. Third highest of the 5 filled years.",
  "account": "Inventories, net against cost of revenue",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:days_sales_of_inventory:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_year_cell",
  "what_changed": "Days sales outstanding is 84.48806267733443 (receivables 253554000.0 against revenue 1095388000.0). Change against years-back-1 is -3.9534323500121786. Second highest of the 5 filled years.",
  "account": "Accounts receivable, net against revenue (days sales outstanding)",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:days_sales_outstanding:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_gross_margin_year_cell",
  "what_changed": "Gross margin is 0.420933039251845. Change against years-back-1 is -0.0018289947216972857. Second highest of the 5 filled years.",
  "account": "Gross margin (revenue less cost of revenue, over revenue)",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:gross_margin:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_year_cell",
  "what_changed": "Receivables over revenue is 0.23147414432146418. Change against years-back-1 is -0.010169284715001947. Second highest of the 5 filled years.",
  "account": "Accounts receivable, net against annual revenue",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:receivables_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_year_cell",
  "what_changed": "Soft-asset share is 0.8863904898298531 (assets 2410388000.0, cash 101350000.0, net PP&E 172493000.0). Change against years-back-1 is 0.0034424092041664967. Highest of the 5 filled years.",
  "account": "Assets other than cash and PP&E, over total assets",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001104659-26-093266:trends:soft_asset_share:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_year_cell_insufficient",
  "what_changed": "insufficient: the record tags no inventory valuation reserve in any period, so no annual inventory reserve ratio exists.",
  "account": "Inventory valuation reserve against inventory",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001104659-26-093266:trends:inventory_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_year_cell_insufficient",
  "what_changed": "insufficient: no us-gaap concept carries a non-GAAP measure, so the table has no annual non-GAAP gap.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001104659-26-093266:trends:non_gaap_gap:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_year_cell_insufficient",
  "what_changed": "insufficient: the warranty accrual concepts exist in the record but not for 2025-09-30, so no annual warranty reserve ratio exists.",
  "account": "Product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-09-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001104659-26-093266:trends:warranty_reserve_ratio:2024-10-01..2025-09-30" }
```

**Formula baselines' inputs (years-back-0 research-and-development capitalization)**

```json
{ "id": "estimates_and_discretion_research_and_development_expense_baseline",
  "what_changed": "FY2025 R&D expense is 23000000, against 12000000.0 for years_back 1 in the same baseline.\n\nThe baseline prints:\n- research_and_development_asset: 48400000.0\n- research_and_development_amortization: 13200000.0\n- earnings_with_rnd_capitalized: 309023000.0, against net income 299223000.0\n- book_value_with_rnd_capitalized: 1589271000.0\n\ninsufficient for the capitalized-over-expense ratio. The table says \"no row for capitalized_development_cost in 2024-10-01..2025-09-30: us-gaap:CapitalizedComputerSoftwareAdditions is in the record, but not for this period\".",
  "account": "Research and development expense; capitalized development cost",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30 against fiscal 2024",
  "quote": "\"value\": \"23000000\"",
  "paragraph_id": "0001104659-25-117276:facts:ResearchAndDevelopmentExpense:2024-10-01..2025-09-30" }
```

**Numeric facts — 10-Q 0001104659-26-093266 unless the paragraph_id says otherwise**

```json
{ "id": "liquidity_and_capital_current_income_tax_payable_balance",
  "what_changed": "Current income taxes payable (AccruedIncomeTaxesCurrent) prints:\n- 5754000 at 2026-06-30\n- 62007000 at 2025-09-30, in the same filing\n- 5619000 at 2026-03-31, in the prior 10-Q\nThe balance fell in the first half and stayed near that level through the third quarter.",
  "account": "Current income tax payable",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"5754000\"",
  "paragraph_id": "0001104659-26-093266:facts:AccruedIncomeTaxesCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_income_taxes_paid_year_to_date",
  "what_changed": "Income taxes paid for 2025-10-01..2026-06-30 is 71905000, against 29059000 for 2024-10-01..2025-06-30. The prior 10-Q printed 67862000 for the six months. This sits alongside the drop in current income tax payable.",
  "account": "Income taxes paid (cash flow supplemental)",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"71905000\"",
  "paragraph_id": "0001104659-26-093266:facts:IncomeTaxesPaid:2025-10-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_continuing_operations_operating_cash_flow_year_to_date",
  "what_changed": "Operating cash flow from continuing operations for the nine months is 193377000, against 88299000 a year earlier. The prior 10-Q printed 134622000 for the six months. No three-month operating cash flow fact exists, which is why the quarterly accruals cell is insufficient.",
  "account": "Net cash provided by operating activities, continuing operations",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"193377000\"",
  "paragraph_id": "0001104659-26-093266:facts:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations:2025-10-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_total_operating_cash_flow_year_to_date",
  "what_changed": "Total operating cash flow for the nine months is 134037000, against 132002000 a year earlier. The total includes the discontinued-operations outflow reported in the next item.",
  "account": "Net cash provided by operating activities (total)",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"134037000\"",
  "paragraph_id": "0001104659-26-093266:facts:NetCashProvidedByUsedInOperatingActivities:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_discontinued_operations_operating_cash_outflow",
  "what_changed": "Operating cash flow from discontinued operations for the nine months is -59340000, against 43703000 a year earlier. The prior 10-Q printed the same -59340000 for the six months to 2026-03-31.",
  "account": "Cash provided by (used in) operating activities, discontinued operations",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"-59340000\"",
  "paragraph_id": "0001104659-26-093266:facts:CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations:2025-10-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_working_capital_change_year_to_date",
  "what_changed": "IncreaseDecreaseInOperatingCapital for the nine months is -2983000, against 33473000 a year earlier. The prior 10-Q printed -7304000 against 30033000 for the six months. The release cash-flow table prints the same line as 2,983 and (33,473) under 'Changes in assets and liabilities': a presentation sign, not a different amount.",
  "account": "Changes in operating assets and liabilities",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"-2983000\"",
  "paragraph_id": "0001104659-26-093266:facts:IncreaseDecreaseInOperatingCapital:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_noncurrent_balance",
  "what_changed": "Non-current long-term debt prints 65000000 at 2026-06-30, against 166000000 at 2025-09-30 and 125000000 at 2026-03-31 (prior 10-Q). Total LongTermDebt is 85000000 against 186000000. For the nine months, repayments of debt were 231000000 and proceeds from long-term debt 130000000.",
  "account": "Long-term debt, non-current",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"65000000\"",
  "paragraph_id": "0001104659-26-093266:facts:LongTermDebtNoncurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_delayed_draw_term_loan_balance",
  "what_changed": "The senior incremental delayed-draw term loan prints 40000000 at 2026-06-30, against 161000000 at 2025-09-30 and 100000000 at 2026-03-31.",
  "account": "Senior incremental delayed-draw term loan",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"40000000\"",
  "paragraph_id": "0001104659-26-093266:facts:LongTermDebt:2026-06-30:us-gaap:DebtInstrumentAxis=ese:SeniorIncrementalDelayedDrawTermLoanFacilityMember" }
```

```json
{ "id": "liquidity_and_capital_revolving_credit_balance",
  "what_changed": "Revolving credit facility borrowings print 45000000 at 2026-06-30, against 25000000 at 2025-09-30 and 45000000 at 2026-03-31.",
  "account": "Revolving credit facility borrowings",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"45000000\"",
  "paragraph_id": "0001104659-26-093266:facts:LongTermDebt:2026-06-30:us-gaap:DebtInstrumentAxis=us-gaap:RevolvingCreditFacilityMember" }
```

```json
{ "id": "liquidity_and_capital_senior_secured_term_loan_commitment",
  "what_changed": "A senior secured term loan facility with face amount 500000000 is tagged at 2026-05-29. Facts at the same date:\n- Term Loan B face amount: 500000000\n- revolver maximum borrowing capacity: 500000000\nThe 8-K index lists a 2026-06-03 filing with items 1.01, 1.02, 2.03 and 9.01. The release attributes $0.20 per share of Q3 charges to 'debt financing' for the pending Megger acquisition. The input gives no drawn amount for these facilities.",
  "account": "Long-term debt (committed acquisition financing)",
  "expected_direction": "up",
  "horizon": "Q1 fiscal 2027, the Megger closing the release anticipates",
  "quote": "\"value\": \"500000000\"",
  "paragraph_id": "0001104659-26-093266:facts:DebtInstrumentFaceAmount:2026-05-29:us-gaap:DebtInstrumentAxis=ese:SeniorSecuredTermLoanFacilityMember" }
```

```json
{ "id": "liquidity_and_capital_term_loan_b_commitment",
  "what_changed": "A senior secured Term Loan B facility with face amount 500000000 is tagged at 2026-05-29, alongside the senior secured term loan and the 500000000 revolver capacity. Nothing drawn under it is tagged at 2026-06-30.",
  "account": "Long-term debt (committed acquisition financing)",
  "expected_direction": "up",
  "horizon": "Q1 fiscal 2027, the Megger closing the release anticipates",
  "quote": "\"value\": \"500000000\"",
  "paragraph_id": "0001104659-26-093266:facts:DebtInstrumentFaceAmount:2026-05-29:us-gaap:DebtInstrumentAxis=ese:SeniorSecuredTermLoanBFacilityMember" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_decline",
  "what_changed": "Cash and equivalents print 73236000 at 2026-06-30, against 101350000 at 2025-09-30 and 92252000 at 2026-03-31. The nine-month net change in cash is -28114000.",
  "account": "Cash and cash equivalents",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"73236000\"",
  "paragraph_id": "0001104659-26-093266:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_current_borrowing_capacity",
  "what_changed": "Line-of-credit current borrowing capacity prints:\n- 442000000 at 2026-06-30\n- 440000000 at 2026-03-31 (prior 10-Q)\n- 465000000 at 2025-09-30 (10-K)\nLetters of credit outstanding are 12700000 at 2026-06-30 against 14500000 at 2026-03-31.",
  "account": "Undrawn credit availability",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"442000000\"",
  "paragraph_id": "0001104659-26-093266:facts:LineOfCreditFacilityCurrentBorrowingCapacity:2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_quarter",
  "what_changed": "Effective tax rate on continuing operations:\n- Q3: 0.201, against 0.251 a year earlier\n- nine months: 0.21, against 0.234\n- Q2 fiscal 2026: 0.235 (prior 10-Q)\n- fiscal 2025: 0.239 (10-K)\nQ3 income tax expense is 8219000 against 8314000, on pretax income of 40954000 against 33069000. The lower rate supports reported Q3 EPS. The input gives no reason for it.",
  "account": "Income tax expense, continuing operations",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"0.201\"",
  "paragraph_id": "0001104659-26-093266:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_interest_expense_quarter",
  "what_changed": "Q3 InterestIncomeExpenseNet is -8713000, against -7921000. The rate during the period is 0.0498 against 0.0603. Debt balances are lower, so the release's as-adjusted interest of (1,850) points to debt-financing charges inside Q3 GAAP interest. If the 2026-05-29 facilities are drawn at the Megger closing, interest expense would rise; the input gives no drawn amount.",
  "account": "Interest expense",
  "expected_direction": "up",
  "horizon": "after the Megger closing (Q1 fiscal 2027 per the release)",
  "quote": "\"value\": \"-8713000\"",
  "paragraph_id": "0001104659-26-093266:facts:InterestIncomeExpenseNet:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_amortization_of_intangibles_year_to_date",
  "what_changed": "Amortization of intangible assets is:\n- nine months: 61086000, against 32735000 a year earlier\n- Q3: 20342000, against 16753000\n- Q2 fiscal 2026: 20420000 (prior 10-Q)\nThe release excludes $0.52 per share of acquisition-related amortization from Q3 adjusted EPS.",
  "account": "Amortization of acquired intangible assets",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"61086000\"",
  "paragraph_id": "0001104659-26-093266:facts:AmortizationOfIntangibleAssets:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_other_intangibles_accumulated_amortization",
  "what_changed": "The 'other intangible assets' class prints:\n- accumulated amortization: 48506000 at 2026-06-30, against 24829000 at 2025-09-30\n- net: 27895000, against 52162000\n- gross: 76401000, against 76991000\nThe 10-K's Maritime purchase allocation included a 61300000 backlog intangible. The input does not say which class holds it.",
  "account": "Finite-lived intangible assets, other class",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"48506000\"",
  "paragraph_id": "0001104659-26-093266:facts:FiniteLivedIntangibleAssetsAccumulatedAmortization:2026-06-30:us-gaap:FiniteLivedIntangibleAssetsByMajorClassAxis=us-gaap:OtherIntangibleAssetsMember" }
```

```json
{ "id": "revenue_recognition_contract_assets_balance",
  "what_changed": "Current contract assets print 127620000 at 2026-06-30, against 90730000 at 2025-09-30 and 103532000 at 2026-03-31 (prior 10-Q).",
  "account": "Contract assets (unbilled revenue)",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"127620000\"",
  "paragraph_id": "0001104659-26-093266:facts:ContractWithCustomerAssetNetCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized_year_to_date",
  "what_changed": "Revenue recognized from opening contract liabilities is 74000000 for the nine months. The prior 10-Q tagged 56000000 for the three months 2026-01-01..2026-03-31; the periods differ, so the two are not compared. Total contract liabilities (ContractWithCustomerLiability) print 293400000 at 2026-06-30 against 224700000 at 2025-09-30.",
  "account": "Contract liabilities",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30",
  "quote": "\"value\": \"74000000\"",
  "paragraph_id": "0001104659-26-093266:facts:ContractWithCustomerLiabilityRevenueRecognized:2025-10-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_balance",
  "what_changed": "Remaining performance obligations print 1540500000 at 2026-06-30, against 1470000000 at 2026-03-31 (prior 10-Q) and 1133600000 at 2025-09-30 (10-K). The release's backlog table ends at 1,540,515 thousand.",
  "account": "Remaining performance obligations (backlog)",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"1540500000\"",
  "paragraph_id": "0001104659-26-093266:facts:RevenueRemainingPerformanceObligation:2026-06-30:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-07-01" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_share_from_july",
  "what_changed": "The share of remaining performance obligations tagged to the expected-timing start date 2026-07-01 is 0.59. The prior 10-Q printed 0.55 for start date 2026-04-01. The input states the start date only, not the length of the window.",
  "account": "Remaining performance obligations, expected timing",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2026-03-31",
  "quote": "\"value\": \"0.59\"",
  "paragraph_id": "0001104659-26-093266:facts:RevenueRemainingPerformanceObligationPercentage:2026-06-30:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-07-01" }
```

```json
{ "id": "estimates_and_discretion_allowance_for_doubtful_accounts_balance",
  "what_changed": "The allowance for doubtful accounts prints 2712000 at 2026-06-30, against 3205000 at 2025-09-30 and 3644000 at 2026-03-31. Net receivables over the same dates are 267493000, 253554000 and 256835000: the allowance fell while receivables rose.",
  "account": "Allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"2712000\"",
  "paragraph_id": "0001104659-26-093266:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_work_in_process_inventory_balance",
  "what_changed": "Inventory components at 2026-06-30, against 2025-09-30:\n- work in process: 59650000, against 46825000 (63243000 at 2026-03-31)\n- raw materials: 125153000, against 118338000\n- finished goods: 55739000, against 52644000\n- total inventories: 240542000, against 217807000",
  "account": "Inventories by component",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"59650000\"",
  "paragraph_id": "0001104659-26-093266:facts:InventoryWorkInProcessNetOfReserves:2026-06-30" }
```

```json
{ "id": "earnings_quality_other_current_assets_balance",
  "what_changed": "Other current assets print 46620000 at 2026-06-30, against 25065000 at 2025-09-30 and 37084000 at 2026-03-31. The input does not break the line down.",
  "account": "Other current assets",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"46620000\"",
  "paragraph_id": "0001104659-26-093266:facts:OtherAssetsCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_accounts_payable_balance",
  "what_changed": "Accounts payable print 116539000 at 2026-06-30, against 96534000 at 2025-09-30 and 106677000 at 2026-03-31.",
  "account": "Accounts payable",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30 and 2026-03-31",
  "quote": "\"value\": \"116539000\"",
  "paragraph_id": "0001104659-26-093266:facts:AccountsPayableCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_capitalized_software_gross_balance",
  "what_changed": "Capitalized software development at 2026-06-30, against 2025-09-30:\n- gross: 146078000, against 138144000\n- accumulated amortization: 108658000, against 100818000\n- net: 37420000, against 37326000\nThe release's cash-flow table prints 'Additions to capitalized software and other' as (7,874) for the nine months, against (13,018). The trend table could not fill capitalized development cost for fiscal 2025.",
  "account": "Capitalized software development costs",
  "expected_direction": "none",
  "horizon": "balance sheet 2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"146078000\"",
  "paragraph_id": "0001104659-26-093266:facts:FiniteLivedIntangibleAssetsGross:2026-06-30:us-gaap:FiniteLivedIntangibleAssetsByMajorClassAxis=us-gaap:SoftwareDevelopmentMember" }
```

```json
{ "id": "estimates_and_discretion_goodwill_movement_year_to_date",
  "what_changed": "Goodwill acquired in the nine months is 5100000, all of it in A&D; the foreign-currency translation change is -6700000. Goodwill prints 760275000 at 2026-06-30, against 761931000 at 2025-09-30. No impairment fact is tagged for the nine months.",
  "account": "Goodwill",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30",
  "quote": "\"value\": \"5100000\"",
  "paragraph_id": "0001104659-26-093266:facts:GoodwillAcquiredDuringPeriod:2025-10-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_megger_consideration",
  "what_changed": "Megger Group Limited consideration is tagged at 2350000000 on 2026-04-15, made up of 900000000 cash and 1400000000 in equity interests. For scale, total assets at 2026-06-30 are 2420003000 and goodwill 760275000. Release paragraph 0001104659-26-092033:8k_2_02:33 says the company continues 'to anticipate closing on the transaction in Q1 of fiscal 2027'.",
  "account": "Goodwill and acquired intangible assets",
  "expected_direction": "up",
  "horizon": "Q1 fiscal 2027 (anticipated closing)",
  "quote": "\"value\": \"2350000000\"",
  "paragraph_id": "0001104659-26-093266:facts:BusinessCombinationConsiderationTransferred1:2026-04-15..2026-04-15:us-gaap:BusinessAcquisitionAxis=ese:MeggerGroupLimitedMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_megger_equity_consideration",
  "what_changed": "The equity portion of the Megger consideration is tagged at 1400000000. For reference:\n- Q3 weighted diluted shares: 25980000\n- shares outstanding at 2026-07-31: 25907567\nThe 8-K index shows a 2026-04-16 filing with items 1.01, 3.02 and 9.01. The input gives no share count for the issuance.",
  "account": "Shares outstanding / stockholders' equity",
  "expected_direction": "up",
  "horizon": "Q1 fiscal 2027 (anticipated closing)",
  "quote": "\"value\": \"1400000000\"",
  "paragraph_id": "0001104659-26-093266:facts:BusinessCombinationConsiderationTransferredEquityInterestsIssuedAndIssuable:2026-04-15..2026-04-15:us-gaap:BusinessAcquisitionAxis=ese:MeggerGroupLimitedMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_megger_cash_consideration",
  "what_changed": "The cash portion of the Megger consideration is tagged at 900000000. Against that, cash at 2026-06-30 is 73236000, alongside the 2026-05-29 term loan commitments of 500000000 and 500000000.",
  "account": "Payments to acquire businesses (investing outflow)",
  "expected_direction": "up",
  "horizon": "Q1 fiscal 2027 (anticipated closing)",
  "quote": "\"value\": \"900000000\"",
  "paragraph_id": "0001104659-26-093266:facts:PaymentsToAcquireBusinessesGross:2026-04-15..2026-04-15:us-gaap:BusinessAcquisitionAxis=ese:MeggerGroupLimitedMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_revenue",
  "what_changed": "Related-party revenue at subsidiaries is:\n- Q3: 1700000\n- nine months: 3900000\n- Q2 fiscal 2026: 1000000; six months: 2300000 (prior 10-Q)\n- fiscal 2025: 4700000 (10-K)\nAgainst Q3 revenue of 339027000.",
  "account": "Revenue from related parties",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against prior quarters",
  "quote": "\"value\": \"1700000\"",
  "paragraph_id": "0001104659-26-093266:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ConsolidatedEntitiesAxis=srt:SubsidiariesMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "earnings_quality_discontinued_operations_income_year_to_date",
  "what_changed": "Income from discontinued operations, net of tax, is 1177000 for the nine months, against 9126000 a year earlier. Q3 shows none (tax effect 0), against 1310000 a year earlier. Nine-month net income of 96159000 includes the 1177000.",
  "account": "Income from discontinued operations",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"1177000\"",
  "paragraph_id": "0001104659-26-093266:facts:IncomeLossFromDiscontinuedOperationsNetOfTax:2025-10-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_share_based_compensation_year_to_date",
  "what_changed": "Share-based compensation is 10182000 for the nine months, against 7934000 a year earlier.",
  "account": "Stock compensation expense",
  "expected_direction": "none",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"10182000\"",
  "paragraph_id": "0001104659-26-093266:facts:ShareBasedCompensation:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_operating_lease_discount_rate",
  "what_changed": "The weighted-average operating lease discount rate is 0.0486 at 2026-06-30, against 0.0475 at 2025-06-30 and 0.0485 at 2026-03-31. The finance-lease rate is 0.0478 against 0.0473.",
  "account": "Lease liabilities (discount rate assumption)",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-06-30",
  "quote": "\"value\": \"0.0486\"",
  "paragraph_id": "0001104659-26-093266:facts:OperatingLeaseWeightedAverageDiscountRatePercent:2026-06-30" }
```

```json
{ "id": "earnings_quality_utility_solutions_segment_operating_income_quarter",
  "what_changed": "USG segment operating income is 21983000 for Q3, against 21540000, on segment revenue of 99963000 against 92357000. The release reports USG adjusted EBIT margin at 22.3 percent against 23.6 percent.",
  "account": "Utility Solutions Group segment operating income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"21983000\"",
  "paragraph_id": "0001104659-26-093266:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=ese:UtilitySolutionsGroupMember" }
```

**Filed history: re-reported values, contexts and printed differences**

```json
{ "id": "articulation_and_the_filed_history_superseded_values_unchanged",
  "what_changed": "The prior 10-Q's LongTermDebt fact at 2025-09-30 (186000000) is marked superseded by the current 10-Q, which prints 186000000 at 2025-09-30. Other superseded prior-filing facts are printed identically by the later filing, including:\n- cash: 101350000\n- AOCI: -2468000\n- retained earnings at 2025-09-30: 1373911000\n- revolver: 25000000\n- delayed-draw term loan: 161000000\n- capitalized software gross: 138144000\n- the 2026-03-31 equity components\nNo restated prior value exists in my input, and no restatement-trace section was supplied.",
  "account": "Prior-period balances as re-reported",
  "expected_direction": "none",
  "horizon": "periods ended 2025-09-30 and 2026-03-31 as re-filed on 2026-08-10",
  "quote": "\"superseded_by\": \"0001104659-26-093266\"",
  "paragraph_id": "0001104659-26-058482:facts:LongTermDebt:2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_megger_fact_context_redated",
  "what_changed": "The prior 10-Q (filed 2026-05-11) tagged the Megger consideration of 2350000000 to a 2026-08-15..2026-08-15 context with SubsequentEventMember; its 900000000 cash and 1400000000 equity facts carry the same context. The current 10-Q tags the same three values to 2026-04-15..2026-04-15 without the subsequent-event axis. The values are unchanged; only the context date and axis differ, so this is not a restatement.",
  "account": "Business combination consideration (Megger)",
  "expected_direction": "none",
  "horizon": "10-Q filed 2026-05-11 against 10-Q filed 2026-08-10",
  "quote": "\"value\": \"2350000000\"",
  "paragraph_id": "0001104659-26-058482:facts:BusinessCombinationConsiderationTransferred1:2026-08-15..2026-08-15:us-gaap:BusinessAcquisitionAxis=ese:MeggerGroupLimitedMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "articulation_and_the_filed_history_translation_adjustment_two_tags_differ",
  "what_changed": "Within the current 10-Q, the prior-year foreign-currency translation adjustment prints different values under two tags:\n- equity-statement tag (OtherComprehensiveIncomeForeignCurrencyTransactionAndTranslationAdjustmentNetOfTaxPortionAttributableToParent, AOCI member): 23076000 for 2025-04-01..2025-06-30 and 13181000 for 2024-10-01..2025-06-30\n- comprehensive-income tag (OtherComprehensiveIncomeLossForeignCurrencyTransactionAndTranslationAdjustmentNetOfTax): 23075000 and 13180000\nFor the current periods both tags print -2116000 and -12959000. No Python articulation check covers this pair; I report only that the printed values are not identical.",
  "account": "Other comprehensive income, foreign currency translation",
  "expected_direction": "none",
  "horizon": "three and nine months ended 2025-06-30, as printed in the 10-Q filed 2026-08-10",
  "quote": "\"value\": \"23076000\"",
  "paragraph_id": "0001104659-26-093266:facts:OtherComprehensiveIncomeForeignCurrencyTransactionAndTranslationAdjustmentNetOfTaxPortionAttributableToParent:2025-04-01..2025-06-30:us-gaap:StatementEquityComponentsAxis=us-gaap:AccumulatedOtherComprehensiveIncomeMember" }
```

**Figures in the 8-K earnings release (0001104659-26-092033, filed 2026-08-06)**

```json
{ "id": "results_against_expectations_full_year_adjusted_eps_guidance_release_figures",
  "what_changed": "Full-year fiscal 2026 adjusted EPS guidance is raised to $8.30 - $8.40. The release states the initial November guidance was $7.50 - $7.80 and the May update $8.00 - $8.25. Nine-month adjusted EPS is printed at 5.75, against 3.71.",
  "account": "Adjusted EPS from continuing operations (non-GAAP)",
  "expected_direction": "up",
  "horizon": "fiscal year ending 2026-09-30 (10-K)",
  "quote": "Raising full year Adjusted EPS guidance to a range of $8.30 - $8.40 per share (38 to 39 percent growth)",
  "paragraph_id": "0001104659-26-092033:8k_2_02:37" }
```

```json
{ "id": "results_against_expectations_fourth_quarter_adjusted_eps_guidance_release_figures",
  "what_changed": "Fiscal fourth-quarter 2026 adjusted EPS is guided to $2.55 - $2.65; the release states this is 10 to 14 percent growth on the prior year's fourth quarter. No filing reports the fiscal fourth quarter as a duration, and no fourth-quarter derivation is in my input.",
  "account": "Adjusted EPS from continuing operations (non-GAAP), fiscal Q4",
  "expected_direction": "up",
  "horizon": "fiscal fourth quarter 2026 (visible only through the fiscal 2026 10-K)",
  "quote": "Adjusted EPS is expected to be in the range of $2.55 - $2.65 per share",
  "paragraph_id": "0001104659-26-092033:8k_2_02:38" }
```

```json
{ "id": "results_against_expectations_full_year_sales_guidance_release_figures",
  "what_changed": "Fiscal 2026 sales guidance is $1.30 to $1.33 billion, with the lower end raised. Nine-month revenue is 938027000, and fiscal 2025 revenue was 1095388000.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "fiscal year ending 2026-09-30 (10-K)",
  "quote": "now expect Sales to be in the range of $1.30 to $1.33 billion",
  "paragraph_id": "0001104659-26-092033:8k_2_02:36" }
```

```json
{ "id": "earnings_quality_adjusted_eps_exclusions_quarter_release_figures",
  "what_changed": "Q3 GAAP EPS from continuing operations is 1.26 and adjusted EPS is 2.20. The release excludes $0.94 per share: $0.03 restructuring, $0.20 debt financing, $0.19 Megger acquisition costs and $0.52 acquisition-related amortization.\n\nComparable exclusions:\n- Q3 fiscal 2025: $0.64\n- nine months: $2.09, against $0.95\nThe trend table's non-GAAP gap is insufficient, so these release figures are the only measure of the gap in my input.",
  "account": "Adjusted EPS reconciliation (non-GAAP)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "Q3 2026 Adjusted EPS from continuing operations excludes $0.94 per share of after-tax charges",
  "paragraph_id": "0001104659-26-092033:8k_2_02:54" }
```

```json
{ "id": "earnings_quality_adjusted_interest_expense_excludes_debt_financing_release_figures",
  "what_changed": "In the release's segment table, Q3 2026 interest expense is (8,713) GAAP but (1,850) as adjusted; Q3 2025 is (7,921) on both bases. The nine-month table prints (13,992) GAAP against (7,129) as adjusted for 2026. The adjustment matches the $0.20 per share 'debt financing' exclusion tied to the pending Megger acquisition.",
  "account": "Interest expense, GAAP against as-adjusted",
  "expected_direction": "none",
  "horizon": "quarter and nine months ended 2026-06-30",
  "quote": "| Less: Interest expense |  |  | (8,713 | ) |  |  | (7,921 | ) |  |  | (1,850 | ) |  |  | (7,921 | ) |",
  "paragraph_id": "0001104659-26-092033:8k_2_02:63" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_nrg_renewables_orders_release_figures",
  "what_changed": "NRG orders fell 27 percent to $13.5 million, which the release links to the expiration of U.S. renewables tax credits. NRG sales fell $5.3 million (29 percent) in the quarter (paragraph 0001104659-26-092033:8k_2_02:25). Doble growth offset both at the USG level.",
  "account": "USG segment revenue, NRG renewables business",
  "expected_direction": "down",
  "horizon": "following quarters of fiscal 2026 and fiscal 2027",
  "quote": "NRG orders decreased $5.0 million (27 percent) to $13.5 million, related to the expiration of U.S. renewables tax credits.",
  "paragraph_id": "0001104659-26-092033:8k_2_02:27" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_utility_solutions_adjusted_margin_release_figures",
  "what_changed": "USG adjusted EBIT margin is 22.3 percent, against 23.6 percent, even though USG sales rose to $100.0 million from $92.4 million. A&D and Test adjusted margins rose, to 30.0 percent from 28.8 and to 16.4 percent from 15.9.",
  "account": "Utility Solutions Group adjusted EBIT margin",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "Adjusted EBIT increased $0.5 million in Q3 2026 to $22.3 million (22.3 percent margin) from $21.8 million (23.6 percent margin) in Q3 2025.",
  "paragraph_id": "0001104659-26-092033:8k_2_02:26" }
```

```json
{ "id": "results_against_expectations_aerospace_defense_orders_comparison_release_figures",
  "what_changed": "A&D entered orders fell 66 percent to $195.7 million because the year-ago quarter held $364.2 million of acquired Maritime backlog. Book-to-bill was 1.16. The release's total Q3 entered orders are 409,538 thousand, and ending backlog is 1,540,515 thousand against 1,470,004 at 4/1/26.",
  "account": "Entered orders and backlog, A&D segment",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "Q3 2026 Entered Orders decreased $386.7 million (66 percent) to $195.7 million, as Q3 2025 contained $364.2 million in acquired backlog related to the Maritime acquisition",
  "paragraph_id": "0001104659-26-092033:8k_2_02:23" }
```

```json
{ "id": "across_documents_release_figures_match_quarterly_report",
  "what_changed": "Release figures agree with the 10-Q facts for every line I checked:\n- continuing operating cash flow: 193,377 against 88,299, matching facts 193377000 and 88299000\n- Q3 net sales: 339,027, matching 339027000\n- Q3 net earnings: 32,735, matching 32735000\n- current income tax payable: 5,754 against 62,007, matching 5754000 and 62007000\n- long-term debt: 65,000, matching 65000000\nNo disagreement between the release (filed 2026-08-06) and the 10-Q (filed 2026-08-10) exists in my input.",
  "account": "Release figures against filed 10-Q facts",
  "expected_direction": "none",
  "horizon": "quarter and nine months ended 2026-06-30",
  "quote": "Net cash provided by operating activities from Continuing Operations was $193 million YTD, an increase of $105 million compared to the prior year period.",
  "paragraph_id": "0001104659-26-092033:8k_2_02:16" }
```

## Seen in the notes

None of the facts in input_numbers.json carries the marker that says whether its element sat inside a note when it was extracted. The trend cells, the formula-baseline inputs and the release figures carry no such marker either. Without that marker I cannot separate note-table findings from statement findings, and I do not judge it myself. So no item is placed under this heading. Every finding above is listed under "Seen in the statements".
