# AAON — numbers reader — 10-Q 0000824142-26-000055 (quarter ended 2026-06-30)

Directory check: the directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. It holds no prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome window. The `window` block in input_trends.json is the analysis window: triggering period 2026-06-30, years end 2025-12-31.

Prior flags: input_prior_predictions.md says "None on record". There is nothing to carry forward.

How the items read:
- Every number in an item is copied as printed. None is derived.
- `expected_direction` is the sign of the printed change.
  - Quarter cells use the year-over-year change (against quarters-back-4); `what_changed` also gives the quarter-over-quarter sign.
  - Year cells use the year-over-year change (against years-back-1).
  - For a fact, it is the direction from the comparative value printed beside it.
  - It is `none` where the input prints no change.

Periods the record does not reach:
- The trend table asked for 8 quarters and 5 years and holds 6 quarters and 5 years.
- **quarters-back-2** (target end 2025-12-30) and **quarters-back-6** (target end 2024-12-31) have no cells. Both give the reason: "no quarter ending within 20 days of [date] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
- The fourth-quarter derivation named there is not in this directory, so no fourth-quarter figure exists in my input.

Inputs that do not exist here:
- No articulation-check file is in the directory, so there are no articulation gaps to report from one.
- No restatement-trace file is in the directory.
- I compared the superseded facts in input_numbers.json against the later filing's fact for the same period. These cover receivables, inventory, assets, contract liabilities, warranty, reserves and equity at 2025-12-31 and 2024-12-31, plus option, award and loan details. Each pair printed the same value, so I found no restated prior value.
- No trend cell says that a period rests on a different concept. The concept differences reported below come from the facts.

Formula baseline I cannot quote:
- The `research_and_development_capitalized` block in years-back-0 prints no `paragraph_id`, so I write no item for it.
- It prints `earnings_with_rnd_capitalized` 131433000.0, `research_and_development_amortization` 34360000.0, `research_and_development_asset` 144300000.0 and `life_years` 5.
- `book_value_with_rnd_capitalized` is missing: the record tags no us-gaap:StockholdersEquity.
- `capitalized_development_cost` and `capitalized_over_expense` are missing: the record tags no us-gaap:CapitalizedComputerSoftwareAdditions.

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-01..2026-06-30)

```json
{ "id": "earnings_quality_accruals_over_total_assets_latest_quarter_insufficient",
  "what_changed": "insufficient. The trend table could not fill accruals over total assets for the quarter 2026-04-01..2026-06-30. The cell's reason is that the record has no operating cash flow for that three-month period; the facts in this input carry operating cash flow for 2026-01-01..2026-06-30 only. Both quarter-over-quarter and year-over-year print 'accruals_over_total_assets is not filled in quarters-back-0', so no change exists.",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000824142-26-000055:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_latest_quarter_trend",
  "what_changed": "Bad-debt reserve ratio is 0.003375830490213683. Quarter-over-quarter change is -0.0007017534383393581 (against quarters-back-1); year-over-year change is -0.004234085672712993 (against quarters-back-4). The cell places it lowest of the 6 filled quarters. Inputs: allowance 1222000.0, receivables 360763000.0.",
  "account": "allowance for doubtful accounts against gross receivables",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_quarter_trend",
  "what_changed": "Contract liabilities over revenue is 0.020338896544684328. Quarter-over-quarter change is -0.09080016361598023; year-over-year change is -0.08799093299438754. The cell places it lowest of the 6 filled quarters. Inputs: contract liabilities 12752000.0, quarterly revenue 626976000.0.",
  "account": "contract liabilities (customer deposits and billings in excess) over revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_days_sales_of_inventory_latest_quarter_trend",
  "what_changed": "Days sales of inventory is 63.54436494304351. Quarter-over-quarter change is -12.236462056910788; year-over-year change is -29.898070316834655. The cell places it lowest of the 6 filled quarters. Inputs: inventory 331328000.0, quarterly cost of goods sold 474485000.0.",
  "account": "inventory against cost of goods sold",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_latest_quarter_trend",
  "what_changed": "Days sales outstanding is 52.3615465344766. Quarter-over-quarter change is -0.18946607076834 (down); year-over-year change is 2.541947539717853 (up). The cell places it third highest of the 6 filled quarters, the middle of its history. Inputs: receivables 360763000.0, quarterly revenue 626976000.0.",
  "account": "trade receivables against revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_latest_quarter_trend",
  "what_changed": "Gross margin is 0.24321664625121217. Quarter-over-quarter change is -0.008254368124884531; year-over-year change is -0.02230890684009726. The cell places it lowest of the 6 filled quarters. Inputs: revenue 626976000.0, cost of goods sold 474485000.0.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_latest_quarter_trend",
  "what_changed": "Inventory reserve ratio is 0.019826274869615607. Quarter-over-quarter change is 0.0005256934575601675 (up); year-over-year change is -0.003494858843891925 (down). The cell places it second lowest of the 6 filled quarters. Inputs: reserve 6569000.0, net inventory 331328000.0.",
  "account": "inventory valuation reserve against inventory",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_latest_quarter_insufficient",
  "what_changed": "insufficient. The trend table cannot fill the non-GAAP gap in any period, because companyfacts carries no non-GAAP measure. Both changes print 'non_gaap_gap is not filled in quarters-back-0'. The input holds no filed non-GAAP figure to set against GAAP net income for this quarter.",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-06-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000824142-26-000055:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_latest_quarter_trend",
  "what_changed": "Receivables over revenue is 0.5754016102689736. Quarter-over-quarter change is -0.008498529789303544 (down); year-over-year change is 0.02793348944744889 (up). The cell places it third highest of the 6 filled quarters, the middle of its history.",
  "account": "trade receivables over quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_latest_quarter_trend",
  "what_changed": "Soft-asset share is 0.6336329729895052. Quarter-over-quarter change is -0.00045899264518911576 (down); year-over-year change is 0.0334384628627592 (up). The cell places it second highest of the 6 filled quarters. Inputs: assets 1863683000.0, PP&E 682779000.0, cash 13000.0.",
  "account": "assets other than PP&E and cash, over total assets",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_latest_quarter_trend",
  "what_changed": "Warranty reserve ratio is 0.058424883887102534. Quarter-over-quarter change is -0.00485690692700632; year-over-year change is -0.017841216181261575. The cell places it lowest of the 6 filled quarters. Inputs: warranty accrual 36631000.0, quarterly revenue 626976000.0.",
  "account": "standard product warranty accrual against revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarters ended 2026-03-31 and 2025-06-30",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_quarterly_history_too_short_insufficient",
  "what_changed": "insufficient for a trend claim. Quarterly accruals over total assets is filled in only 2 quarters: quarters-back-1 (0.0032524786110837943) and quarters-back-5. The cell places quarters-back-1 lowest of the 2 filled quarters; two points do not make a trend. The quarters-back-1 quarter-over-quarter change prints 'accruals_over_total_assets is not filled in quarters-back-2'. Its year-over-year change is -0.026363124610899402.",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "quarters on record through 2026-06-30",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0000824142-26-000055:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

### Trend table — years-back-0 (2025-01-01..2025-12-31)

For every year cell the quarter-over-quarter field prints "an annual period has no preceding quarter".

```json
{ "id": "earnings_quality_accruals_over_total_assets_latest_year_trend",
  "what_changed": "Accruals over total assets is 0.06347961174259269. Year-over-year change is 0.08387810259632905 (against years-back-1). The cell places it highest of the 5 filled years. Inputs: net income 107593000.0, operating cash flow 534000.0, assets 1686510000.0.",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_full_year_operating_cash_flow_trend_input",
  "what_changed": "The operating-cash-flow input to the 2025 accruals cell is 534000.0, against net income 107593000.0 in the same cell. The 10-K fact for 2024 operating cash flow prints 192532000.",
  "account": "net cash provided by operating activities",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31",
  "quote": "\"value\": 534000.0",
  "paragraph_id": "0000824142-26-000055:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_latest_year_trend",
  "what_changed": "Bad-debt reserve ratio is 0.004143239519156148. Year-over-year change is -0.0028479776800463957. The cell places it third highest of the 5 filled years, the middle of its history. Inputs: allowance 1308000.0, receivables 314387000.0.",
  "account": "allowance for doubtful accounts against gross receivables",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_year_trend",
  "what_changed": "Contract liabilities over revenue is 0.05594018623151623. Year-over-year change is 0.04351925897219096. The cell places it highest of the 5 filled years. Inputs: contract liabilities 80670000.0, revenue 1442076000.0.",
  "account": "contract liabilities over revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_days_sales_of_inventory_latest_year_trend",
  "what_changed": "Days sales of inventory is 90.23518202265912. Year-over-year change is 4.866793196410811. The cell places it second lowest of the 5 filled years. Inputs: inventory 261151000.0, cost of goods sold 1056352000.0.",
  "account": "inventory against cost of goods sold",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_latest_year_trend",
  "what_changed": "Days sales outstanding is 79.57365284492634. Year-over-year change is 34.63006549323328. The cell places it highest of the 5 filled years. Inputs: receivables 314387000.0, revenue 1442076000.0.",
  "account": "trade receivables against revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_latest_year_trend",
  "what_changed": "Gross margin is 0.26747827437666255. Year-over-year change is -0.06327087086731253. The cell places it third highest of the 5 filled years, the middle of its history. Inputs: revenue 1442076000.0, cost of goods sold 1056352000.0.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_latest_year_trend",
  "what_changed": "Inventory reserve ratio is 0.02046325688969217. Year-over-year change is -0.007239229504502686. The cell places it second lowest of the 5 filled years. Inputs: reserve 5344000.0, net inventory 261151000.0.",
  "account": "inventory valuation reserve against inventory",
  "expected_direction": "down",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_latest_year_insufficient",
  "what_changed": "insufficient. The non-GAAP gap is not filled for 2025, and its year-over-year change prints 'non_gaap_gap is not filled in years-back-0'. The ratio is filled in none of the 11 periods on record.",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "year ended 2025-12-31",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000824142-26-000055:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_latest_year_trend",
  "what_changed": "Receivables over revenue is 0.21801000779431876. Year-over-year change is 0.09521332104105902. The cell places it highest of the 5 filled years.",
  "account": "trade receivables over annual revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_latest_year_trend",
  "what_changed": "Soft-asset share is 0.6256915168009677. Year-over-year change is 0.05996247900934493. The cell places it highest of the 5 filled years. Inputs: assets 1686510000.0, PP&E 631262000.0, cash 13000.0.",
  "account": "assets other than PP&E and cash, over total assets",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_latest_year_trend",
  "what_changed": "Warranty reserve ratio is 0.02077907128334429. Year-over-year change is 0.0005056326446239434. The cell places it second highest of the 5 filled years. Inputs: warranty accrual 29965000.0, revenue 1442076000.0.",
  "account": "standard product warranty accrual against revenue",
  "expected_direction": "up",
  "horizon": "year ended 2025-12-31 against year ended 2024-12-31",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000824142-26-000055:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

### Changes of tag and concept, from the numeric facts

```json
{ "id": "structure_and_disclosure_changes_disposal_result_income_statement_concept",
  "what_changed": "For 2025-01-01..2025-06-30, the second-quarter 10-Q prints the disposal result as 40000 under GainLossOnDispositionOfAssets. In the segment reconciliation it prints the same period as -40000 under GainLossOnDispositionOfAssets1. One period carries two concepts with opposite printed signs. The quarters 2026-04-01..2026-06-30 and 2025-04-01..2025-06-30 print 0 under both.",
  "account": "gain or loss on disposal of assets",
  "expected_direction": "none",
  "horizon": "six months ended 2025-06-30, as filed 2026-08-10",
  "quote": "\"value\": \"40000\"",
  "paragraph_id": "0000824142-26-000055:facts:GainLossOnDispositionOfAssets:2025-01-01..2025-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_disposal_result_segment_concept_sign",
  "what_changed": "For the same six months, the second-quarter 10-Q prints -40000 under GainLossOnDispositionOfAssets1, opposite in sign to the 40000 it prints under GainLossOnDispositionOfAssets. The release's reconciliation shows the line as 'Add: loss on disposal of assets' 40, while its income statement shows 'Gain on disposal of assets' (40).",
  "account": "gain or loss on disposal of assets (segment reconciliation)",
  "expected_direction": "none",
  "horizon": "six months ended 2025-06-30, as filed 2026-08-10",
  "quote": "\"value\": \"-40000\"",
  "paragraph_id": "0000824142-26-000055:facts:GainLossOnDispositionOfAssets1:2025-01-01..2025-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_disposal_result_first_quarter_sign_convention",
  "what_changed": "The first-quarter 10-Q (filed 2026-05-07) prints GainLossOnDispositionOfAssets1 as positive 40000 for 2025-01-01..2025-03-31. The 10-K prints the same concept negative (-4000 for 2025), and the second-quarter 10-Q prints it negative (-40000 for the six months). The sign this filer gives the concept differs from filing to filing. The periods differ, so this is a change of convention, not a restated value.",
  "account": "gain or loss on disposal of assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2025-03-31, as filed 2026-05-07",
  "quote": "\"value\": \"40000\"",
  "paragraph_id": "0000824142-26-000036:facts:GainLossOnDispositionOfAssets1:2025-01-01..2025-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_disposal_result_annual_concept_pair",
  "what_changed": "The 10-K prints the 2025 disposal result as 4000 under GainLossOnDispositionOfAssets (2024: 23000; 2023: 13000). In its segment section it prints the same years as -4000, -23000 and -13000 under GainLossOnDispositionOfAssets1. The two concepts carry opposite signs in every year.",
  "account": "gain or loss on disposal of assets",
  "expected_direction": "none",
  "horizon": "years ended 2023-12-31 to 2025-12-31, as filed 2026-03-02",
  "quote": "\"value\": \"-4000\"",
  "paragraph_id": "0000824142-26-000005:facts:GainLossOnDispositionOfAssets1:2025-01-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_equity_concept_not_stockholders_equity",
  "what_changed": "The filer tags total equity as StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest. It prints 1010416000 at 2026-06-30, 934209000 at 2026-03-31, 894985000 at 2025-12-31 and 832746000 at 2025-06-30. The trend table's R&D baseline reports that no us-gaap:StockholdersEquity is tagged in any period. That is why the book-value baseline is missing: the equity is in the input under another concept.",
  "account": "total stockholders' equity",
  "expected_direction": "up",
  "horizon": "balance at 2026-06-30 against 2025-12-31",
  "quote": "\"tag\": \"StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest\"",
  "paragraph_id": "0000824142-26-000055:facts:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest:2026-06-30" }
```

### Two values for one date

```json
{ "id": "articulation_and_the_filed_history_contract_asset_allowance_two_concepts",
  "what_changed": "At 2025-12-31 the 10-K prints the contract-asset credit-loss allowance under two concepts with different values: 598000 under ContractWithCustomerAssetAccumulatedAllowanceForCreditLoss and 599000 under ContractWithCustomerAssetAccumulatedAllowanceForCreditLossCurrent. The first-quarter 10-Q repeats 598000 under the first concept for 2025-12-31. The second-quarter 10-Q prints 598000 under the first concept for 2025-12-31 and 599000 under each concept for 2026-06-30. No articulation check exists in my input to say which figure the balance sheet uses.",
  "account": "allowance for credit losses on contract assets",
  "expected_direction": "none",
  "horizon": "balance at 2025-12-31",
  "quote": "\"value\": \"599000\"",
  "paragraph_id": "0000824142-26-000005:facts:ContractWithCustomerAssetAccumulatedAllowanceForCreditLossCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_contract_asset_gross_two_concepts",
  "what_changed": "At 2026-06-30 the second-quarter 10-Q prints ContractWithCustomerAssetGross as 259472000, ContractWithCustomerAssetNet as 258873000 and the balance-sheet ContractWithCustomerAssetNetCurrent as 258873000. At the same date it prints ContractWithCustomerAssetGrossCurrent as 794659000, and 298674000 at 2025-06-30. The two 'gross' concepts carry different values for the same date, and the input does not say what the GrossCurrent figure measures.",
  "account": "contract assets (costs and estimated earnings in excess of billings)",
  "expected_direction": "none",
  "horizon": "balance at 2026-06-30",
  "quote": "\"value\": \"794659000\"",
  "paragraph_id": "0000824142-26-000055:facts:ContractWithCustomerAssetGrossCurrent:2026-06-30" }
```

```json
{ "id": "articulation_and_the_filed_history_option_proceeds_rounding_duplicate",
  "what_changed": "In the 10-K, the same paragraph prints two values for 2025 proceeds from stock options exercised: 17144000 (decimals -3) and 17100000 (decimals -5). This is a rounding duplicate within one filing, not a restated value.",
  "account": "proceeds from stock options exercised",
  "expected_direction": "none",
  "horizon": "year ended 2025-12-31",
  "quote": "\"value\": \"17100000\"",
  "paragraph_id": "0000824142-26-000005:facts:ProceedsFromStockOptionsExercised:2025-01-01..2025-12-31" }
```

### Liquidity, cash flow and capital

```json
{ "id": "liquidity_and_capital_half_year_operating_cash_flow",
  "what_changed": "Net cash from operating activities for 2026-01-01..2026-06-30 is 54968000, against -31040000 for 2025-01-01..2025-06-30. The first-quarter 10-Q printed 33994000 for the first quarter of 2026. No quarterly figure for 2026-04-01..2026-06-30 is filed, which is why the quarter's accruals cell is empty.",
  "account": "net cash provided by (used in) operating activities",
  "expected_direction": "up",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"54968000\"",
  "paragraph_id": "0000824142-26-000055:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_drawdown_half_year",
  "what_changed": "The cash-flow change in contract liabilities for 2026-01-01..2026-06-30 is -67918000, against 18839000 for the first half of 2025. The first-quarter 10-Q printed -25441000 for the first quarter of 2026. The balance is 12752000 at 2026-06-30, against 80670000 at 2025-12-31.",
  "account": "contract liabilities (customer deposits)",
  "expected_direction": "down",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"-67918000\"",
  "paragraph_id": "0000824142-26-000055:facts:IncreaseDecreaseInContractWithCustomerLiability:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_revolver_balance",
  "what_changed": "The revolving line of credit is 435000000 at 2026-06-30, against 398320000 at 2025-12-31; the first-quarter 10-Q printed 425154000 at 2026-03-31. Maximum borrowing capacity is 600000000 at both dates. Half-year borrowings are 597485000 and repayments 560805000.",
  "account": "revolving credit facility borrowings",
  "expected_direction": "up",
  "horizon": "balance at 2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"435000000\"",
  "paragraph_id": "0000824142-26-000055:facts:LineOfCredit:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_remaining_borrowing_capacity",
  "what_changed": "Remaining revolver capacity is 163692000 at 2026-06-30, against 201026000 at 2025-12-31; the first-quarter 10-Q printed 173538000 at 2026-03-31. Letters of credit under the facility are 1308000 at 2026-06-30, against 654000.",
  "account": "remaining borrowing capacity on the revolver",
  "expected_direction": "down",
  "horizon": "balance at 2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"163692000\"",
  "paragraph_id": "0000824142-26-000055:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2026-06-30:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember" }
```

```json
{ "id": "liquidity_and_capital_restricted_cash_build",
  "what_changed": "Restricted cash is 12714000 at 2026-06-30, against 1226000 at 2025-12-31. Cash and cash equivalents print 13000 at both dates. Cash, cash equivalents and restricted cash together print 12727000 at 2026-06-30, against 1239000 at 2025-12-31.",
  "account": "restricted cash",
  "expected_direction": "up",
  "horizon": "balance at 2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"12714000\"",
  "paragraph_id": "0000824142-26-000055:facts:RestrictedCash:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_half_year",
  "what_changed": "Payments for machinery and equipment are 97282000 for 2026-01-01..2026-06-30, against 82515000 for the first half of 2025. The 10-K prints 190563000 for 2025. Net PP&E is 682779000 at 2026-06-30, against 631262000 at 2025-12-31.",
  "account": "capital expenditure",
  "expected_direction": "up",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"97282000\"",
  "paragraph_id": "0000824142-26-000055:facts:PaymentsToAcquireMachineryAndEquipment:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_stopped",
  "what_changed": "Payments for repurchase of equity are 0 for 2026-01-01..2026-06-30, against 29992000 for the first half of 2025. Tax-withholding share payments are 4468000, against 9167000. Proceeds from stock options exercised are 29100000, against 10025000.",
  "account": "share repurchases",
  "expected_direction": "down",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0000824142-26-000055:facts:PaymentsForRepurchaseOfEquity:2026-01-01..2026-06-30" }
```

### Estimates, reserves and tax

```json
{ "id": "estimates_and_discretion_negative_bad_debt_provision",
  "what_changed": "The provision for doubtful accounts is -62000 for 2026-01-01..2026-06-30, a negative provision, against 270000 for the first half of 2025. Write-offs are 2000 for the quarter and 74000 for the six months. The allowance is 1222000 at 2026-06-30, against 1308000 at 2025-12-31, while net receivables are 360763000, against 314387000.",
  "account": "provision for doubtful accounts",
  "expected_direction": "down",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"-62000\"",
  "paragraph_id": "0000824142-26-000055:facts:ProvisionForDoubtfulAccounts:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_half_year",
  "what_changed": "Inventory write-downs are 1225000 for 2026-01-01..2026-06-30, against 288000 for the first half of 2025. The inventory valuation reserve is 6569000 at 2026-06-30, against 5344000 at 2025-12-31 and 5480000 at 2025-06-30.",
  "account": "inventory write-down and valuation reserve",
  "expected_direction": "up",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"1225000\"",
  "paragraph_id": "0000824142-26-000055:facts:InventoryWriteDown:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accruals_issued_quarter",
  "what_changed": "Warranty accruals issued are 10987000 for 2026-04-01..2026-06-30, against 3599000 for the same quarter of 2025. Warranty payments are 5803000, against 3447000. The standard warranty accrual is 36631000 at 2026-06-30, against 31447000 at 2026-03-31 and 23762000 at 2025-06-30.",
  "account": "standard product warranty accrual",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"10987000\"",
  "paragraph_id": "0000824142-26-000055:facts:StandardProductWarrantyAccrualWarrantiesIssued:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_accrued_sales_commissions",
  "what_changed": "Accrued sales commissions are 15247000 at 2026-06-30, against 25535000 at 2025-12-31. In the same accrued-liabilities table, taxes payable are 4075000, against 143000, and employee-related liabilities are 33966000, against 27156000.",
  "account": "accrued sales commissions",
  "expected_direction": "down",
  "horizon": "balance at 2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"15247000\"",
  "paragraph_id": "0000824142-26-000055:facts:AccruedSalesCommissionCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_quarter",
  "what_changed": "The effective tax rate is 0.098 for 2026-04-01..2026-06-30, against 0.206 for the same quarter of 2025. It is 0.161 for the six months, against 0.139. Income tax expense is 6188000 for the quarter, against 4018000, on pre-tax income of 62847000, against 19505000.",
  "account": "income tax expense and effective tax rate",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"0.098\"",
  "paragraph_id": "0000824142-26-000055:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_excess_tax_benefit_share_based_compensation",
  "what_changed": "The rate reconciliation prints the share-based-compensation excess tax benefit as -0.184 for 2026-04-01..2026-06-30, against -0.095 for the same quarter of 2025. The amount is -11591000, against -1856000. For the six months it is -12394000, against -9020000.",
  "account": "excess tax benefit from share-based compensation",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"-0.184\"",
  "paragraph_id": "0000824142-26-000055:facts:EffectiveIncomeTaxRateReconciliationShareBasedCompensationExcessTaxBenefitPercent:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_law_change_impact",
  "what_changed": "For 2026-01-01..2026-06-30 the second-quarter 10-Q prints deferred income tax expense of -36200000 attributed to the impact of tax-law changes. Other attributions are bonus depreciation -7000000.0 and permanent expensing of domestic costs -4200000. Total deferred income tax expense for the six months is 7823000, against -2423000. The deferred tax liability is 38136000 at 2026-06-30, against 30313000 at 2025-12-31.",
  "account": "deferred income tax",
  "expected_direction": "none",
  "horizon": "six months ended 2026-06-30",
  "quote": "\"value\": \"-36200000\"",
  "paragraph_id": "0000824142-26-000055:facts:DeferredIncomeTaxExpenseBenefit:2026-01-01..2026-06-30:aaon:DeferredTaxLiabilityAxis=aaon:DeferredTaxLiabilityImpactOfTaxLawChangesMember" }
```

### Segments and related parties

```json
{ "id": "structure_and_disclosure_changes_intersegment_eliminations_oklahoma",
  "what_changed": "Intersegment revenue eliminations for the AAON Oklahoma segment are -91359000 for 2026-04-01..2026-06-30, against -5318000 for the same quarter of 2025. For the six months they are -135868000, against -9157000. Coil Products eliminations are -7660000, against -3439000. The first-quarter 10-Q printed -44509000 for Oklahoma for the first quarter of 2026, against -3839000.",
  "account": "intersegment revenue eliminations",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"-91359000\"",
  "paragraph_id": "0000824142-26-000055:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:IntersegmentEliminationMember,us-gaap:StatementBusinessSegmentsAxis=aaon:AAONOklahomaMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_loan",
  "what_changed": "Related-party loans payable are 48200000 at 2026-04-16. The same transaction with counterparty Investor1 prints maximum borrowing capacity 50500000, net debt proceeds 35200000 and debt issuance proceeds 12900000. Earlier dated instances print 22500000 (2019-10-24), 23800000 (2023-04-25) and 16000000.0 (2024-02-27). The first-quarter 10-Q tagged the 2026-04-16 facts with SubsequentEventMember; the second-quarter 10-Q tags them without it.",
  "account": "related-party loans payable",
  "expected_direction": "up",
  "horizon": "transaction dated 2026-04-16",
  "quote": "\"value\": \"48200000\"",
  "paragraph_id": "0000824142-26-000055:facts:LoansPayable:2026-04-16:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_revenue",
  "what_changed": "Related-party revenue is 1088000 for 2026-04-01..2026-06-30, against 2213000 for the same quarter of 2025; for the six months it is 3691000, against 3308000. Related-party receivables are 746000 at 2026-06-30, against 335000 at 2025-12-31. Other related-party transactions are 337000 for the quarter, against 704000.",
  "account": "related-party revenue and receivables",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"1088000\"",
  "paragraph_id": "0000824142-26-000055:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-04-01..2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

### Earnings-release figures set against the filed facts

```json
{ "id": "across_documents_release_cash_figure_against_filed_cash",
  "what_changed": "The release's $12.7 million is cash, cash equivalents and restricted cash. The second-quarter 10-Q prints that total as 12727000 at 2026-06-30, so the two agree. Of it, the 10-Q prints cash and cash equivalents as 13000 and restricted cash as 12714000. The release's $435.0 million revolver balance agrees with the filed 435000000.",
  "account": "cash, cash equivalents and restricted cash",
  "expected_direction": "none",
  "horizon": "balance at 2026-06-30",
  "quote": "As of June 30, 2026, the Company had cash, cash equivalents and restricted cash of $12.7 million and a balance on its revolving credit facility of $435.0 million.",
  "paragraph_id": "0000824142-26-000052:8k_2_02:56" }
```

```json
{ "id": "results_against_expectations_release_gross_margin_outlook_lowered",
  "what_changed": "The release's outlook table lowers the full-year 2026 gross profit margin guide from the prior 27%-28% to 25%-26%. The same table raises sales growth to 55%-60% from 40%-45%. The quarter's gross margin cell prints 0.24321664625121217, lowest of the 6 filled quarters.",
  "account": "gross profit margin guidance",
  "expected_direction": "down",
  "horizon": "fiscal year 2026",
  "quote": "| Gross Profit Margin | 25%-26% | 27%-28% |  |",
  "paragraph_id": "0000824142-26-000052:8k_2_02:37" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_release_coil_segment_margin_figures",
  "what_changed": "The release's AAON Coil Products table prints gross profit margin of 16.0% for the quarter ended 2026-06-30, against 24.1% for the quarter ended 2026-03-31 and 17.5% for the quarter ended 2025-06-30. The 10-Q facts print Coil segment gross profit of 23538000 for the quarter, against 28302000 in the first quarter.",
  "account": "AAON Coil Products segment gross margin",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against the quarter ended 2026-03-31",
  "quote": "| Gross profit margin | 16.0 | % | 24.1 | % | 17.5 | % |",
  "paragraph_id": "0000824142-26-000052:8k_2_02:47" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_release_backlog_sequential_figures",
  "what_changed": "The release prints total backlog of 1,970,844 thousand at 2026-06-30, against 2,129,455 thousand at 2026-03-31 and 995,320 thousand at 2025-06-30. BASX-branded backlog is 1,430,379 thousand, against 1,619,649 thousand at 2026-03-31. It states the sequential decline as 7.4%.",
  "account": "order backlog",
  "expected_direction": "down",
  "horizon": "balance at 2026-06-30 against 2026-03-31",
  "quote": "Compared to the first quarter of 2026, total backlog decreased 7.4%, primarily reflecting accelerated backlog conversion into record revenue and the inherent timing variability of large BASX project awards.",
  "paragraph_id": "0000824142-26-000052:8k_2_02:34" }
```

## Seen in the notes

The input marks no fact as sitting inside a note. No fact in input_numbers.json carries an in-note field, and the trend cells carry none either. I therefore cannot place any fact under this heading, and I write no items here.

That includes the warranty, allowance, inventory-reserve, tax-reconciliation, contract-asset, related-party, debt and segment facts reported above. I took them as numeric facts and listed them under the first heading only.

This is a missing input marker, not a judgement that nothing in the filing came from a note.
