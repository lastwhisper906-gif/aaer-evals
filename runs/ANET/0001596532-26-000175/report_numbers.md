<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_numbers — ANET (Arista Networks), 10-Q 0001596532-26-000175, period ended 2026-06-30

Read in full: input_8k.md, input_numbers.json, input_prior_predictions.md, input_trends.json.

**Run check.** The directory holds only those four files. None of them holds prices, abnormal returns, short interest, another company's filing, a prior run's probability or an outcome window. input_prior_predictions.md reads "None on record". The task message listed other tickers, accession numbers and dates (FTNT, JCI, POWL, FELE, MSI, FLEX, AVGO, FFIV, LOGI). Those lines are not files in this directory and carry no prices or returns. Nothing here uses them.

**Periods the record does not reach (no cells, so no items).** Two quarters in the trend window have no cells:
- quarters-back-2 (target 2025-12-30): "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
- quarters-back-6 (target 2024-12-31): the same reason, with 2024-12-31.

The input contains no fourth-quarter derivation, so no figure for either fourth quarter exists here, and none is derived.

**Inputs that are absent.**
- No articulation checks are in the input, so no articulation gap can be reported.
- No restatement traces are in the input. The only restated prior values come from the earnings release, where the company recast its 2025 non-GAAP figures. They are itemized below.
- No trend cell and no fact row says that a period rests on a different concept, so there is no tag-change item.
  - An observation only, not flagged by the input and not itemized: the 10-K tags capital spending as PaymentsToAcquireProductiveAssets, while the 10-Qs use PaymentsToAcquirePropertyPlantAndEquipment.
- Many 2025-12-31 facts from the 10-K and the first-quarter 10-Q carry `superseded_by` (a later filing re-reported them). The input does not say any value changed, and the rows I read show the same printed value. No restated-value item comes from them.
- The R&D-capitalized baseline in years-back-0 prints no paragraph_id, so it cannot be quoted and is not itemized. Its printed values:
  - book_value_with_rnd_capitalized 15326808000.0
  - earnings_with_rnd_capitalized 4018032000.0
  - research_and_development_amortization 730668000.0
  - research_and_development_asset 2956308000.0
  - capitalized_development_cost and capitalized_over_expense are missing: the companyfacts record tags no us-gaap:CapitalizedComputerSoftwareAdditions in any period.
- The 8-K's list of item codes and its late-filing line ("none on or before 2026-08-05") print no paragraph id, so they are not itemized.
- The facts file holds several thousand rows. The fact items below are the rows that bear on the trend metrics and on the earnings release. Fair-value-hierarchy splits and RSU roll-forward rows were read but are not itemized.
  - Facts from the 10-K and the first-quarter 10-Q are not itemized, except the inventory write-down. Their rows could not be re-checked character for character for this report, and a quote that does not match is dropped. This includes the reseller concentration percentages.

**Conventions.** `expected_direction` is the direction of the printed change in the account. For a quarterly trend cell it follows the printed year_over_year change, and a quarter_over_quarter change of the other sign is stated in what_changed. For a fact or a release row it is the reported period against the comparative named in what_changed. It is `none` where the item is insufficient or no comparative is printed. `horizon` names the periods the change spans. Neither field is a forecast. Every number below is copied as printed; none is computed here.

## Seen in the statements

**Trend table: quarters-back-0 (2026-04-01..2026-06-30, 91 days)**

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
  "what_changed": "receivables_over_revenue is 0.7465164541950786 (formula as printed: receivables / revenue; receivables 2266200000.0, revenue 3035700000.0). quarter_over_quarter change 0.03636510683442895 against quarters-back-1; year_over_year change 0.010123130537604053 against quarters-back-4. position_in_history: highest of the 6 filled quarters. The history is six filled quarters; quarters-back-2 and quarters-back-6 have no cells.",
  "account": "accounts receivable, net (AccountsReceivableNetCurrent) over revenue",
  "expected_direction": "up",
  "horizon": "quarter 2026-04-01..2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
  "what_changed": "days_sales_outstanding is 67.93299733175215 (formula as printed: receivables / revenue * days_in_period; receivables 2266200000.0, revenue 3035700000.0, 91 days). quarter_over_quarter change 4.019376069293678 against quarters-back-1; year_over_year change 0.9212048789219693 against quarters-back-4. position_in_history: highest of the 6 filled quarters.",
  "account": "accounts receivable, net; days sales outstanding",
  "expected_direction": "up",
  "horizon": "quarter 2026-04-01..2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"value\": 67.93299733175215",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
  "what_changed": "contract_liabilities_over_revenue is 1.6802384952399776 (formula as printed: contract_liabilities / revenue). The numerator is tag ContractWithCustomerLiabilityCurrent, 5100700000.0, the current portion only; revenue is 3035700000.0. quarter_over_quarter change -0.13205386356400917 against quarters-back-1 (down); year_over_year change 0.4159061294925175 against quarters-back-4 (up). position_in_history: second highest of the 6 filled quarters.",
  "account": "deferred revenue, current (ContractWithCustomerLiabilityCurrent) over revenue",
  "expected_direction": "up",
  "horizon": "quarter 2026-04-01..2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
  "what_changed": "days_sales_of_inventory is 205.00470943664473 (formula as printed: inventory / cost_of_revenue * days_in_period; inventory 2535300000.0, cost_of_revenue 1125400000.0). quarter_over_quarter change -2.5132134465174545 against quarters-back-1; year_over_year change -39.55036756674863 against quarters-back-4. position_in_history: lowest of the 6 filled quarters.",
  "account": "inventories, net; days sales of inventory",
  "expected_direction": "down",
  "horizon": "quarter 2026-04-01..2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend",
  "what_changed": "gross_margin is 0.6292782554270844 (formula as printed: (revenue - cost_of_revenue) / revenue; revenue 3035700000.0, cost_of_revenue 1125400000.0). quarter_over_quarter change 0.010304464360270105 against quarters-back-1 (up); year_over_year change -0.0232072307848169 against quarters-back-4 (down). position_in_history: second lowest of the 6 filled quarters.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "quarter 2026-04-01..2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001596532-26-000175:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend",
  "what_changed": "soft_asset_share is 0.8902744929405862 (formula as printed: (assets - property_plant_and_equipment - cash) / assets; assets 23720100000.0, cash 2290200000.0, property_plant_and_equipment 312500000.0). quarter_over_quarter change 0.030638817739145563 against quarters-back-1; year_over_year change 0.03408550284732503 against quarters-back-4. position_in_history: highest of the 6 filled quarters.",
  "account": "soft assets over total assets",
  "expected_direction": "up",
  "horizon": "quarter 2026-04-01..2026-06-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"value\": 0.8902744929405862",
  "paragraph_id": "0001596532-26-000175:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_trend",
  "what_changed": "insufficient: accruals_over_total_assets has no value for this quarter. The cell gives the quoted reason, and its quarter_over_quarter and year_over_year read 'accruals_over_total_assets is not filled in quarters-back-0'. The table fills this ratio in only two quarters (quarters-back-1, the lowest of the 2 filled quarters, and quarters-back-5), which does not support a trend claim. The input holds a six-month operating cash flow (the release's cash flow statement) but no three-month figure, and none is derived here.",
  "account": "total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "quarter 2026-04-01..2026-06-30",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001596532-26-000175:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
  "what_changed": "insufficient: there is no bad_debt_allowance row for 2026-06-30. The three allowance tags are in the record, but not for this period. The coverage list fills this ratio in only 2 periods of the whole table (years-back-3 and years-back-4) and in no quarter, so there is no quarterly history at all.",
  "account": "allowance for credit losses on receivables",
  "expected_direction": "none",
  "horizon": "quarter 2026-04-01..2026-06-30",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001596532-26-000175:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend",
  "what_changed": "insufficient: the companyfacts record tags us-gaap:InventoryValuationReserves in no period, so this ratio is filled in 0 periods of the table. The cell says the record cannot tell whether the company does not tag the reserve or states it only by segment.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "quarter 2026-04-01..2026-06-30",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend",
  "what_changed": "insufficient: the companyfacts record tags none of the three warranty-accrual concepts in any period, so this ratio is filled in 0 periods of the table.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "quarter 2026-04-01..2026-06-30",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend",
  "what_changed": "insufficient: companyfacts holds no non-GAAP measure, so this ratio is filled in 0 periods. The release prints non-GAAP net income 1,301.7 and GAAP net income 1,212.9 (in millions) for the quarter. No gap ratio exists in the input, and none is computed here.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter 2026-04-01..2026-06-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001596532-26-000175:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

**Trend table: years-back-0 (2025-01-01..2025-12-31, 365 days)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend",
  "what_changed": "accruals_over_total_assets is -0.044244829962053825 (formula as printed: (net_income - operating_cash_flow) / assets; net_income 3511400000.0 and operating_cash_flow 4371900000.0 from 10-K 0001596532-26-000013, assets 19448600000.0 from 0001596532-26-000175). year_over_year change 0.016714020499712497 against years-back-1; quarter_over_quarter reads 'an annual period has no preceding quarter'. position_in_history: second lowest of the 5 filled years.",
  "account": "total accruals over total assets",
  "expected_direction": "up",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"value\": -0.044244829962053825",
  "paragraph_id": "0001596532-26-000175:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
  "what_changed": "contract_liabilities_over_revenue is 0.44445184716346314 (contract_liabilities 4002600000.0, tag ContractWithCustomerLiabilityCurrent; revenue 9005700000.0). year_over_year change 0.19780393409639285 against years-back-1. position_in_history: highest of the 5 filled years.",
  "account": "deferred revenue, current over revenue",
  "expected_direction": "up",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend",
  "what_changed": "days_sales_of_inventory is 253.3801359283287 (inventory 2247100000.0; cost_of_revenue 3237000000.0). year_over_year change -13.943536338571533 against years-back-1. position_in_history: second lowest of the 5 filled years.",
  "account": "inventories, net; days sales of inventory",
  "expected_direction": "down",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"value\": 253.3801359283287",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend",
  "what_changed": "days_sales_outstanding is 76.47584307716224 (receivables 1886900000.0; revenue 9005700000.0; 365 days). year_over_year change 16.87038263821377 against years-back-1. position_in_history: second highest of the 5 filled years.",
  "account": "accounts receivable, net; days sales outstanding",
  "expected_direction": "up",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"value\": 76.47584307716224",
  "paragraph_id": "0001596532-26-000175:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend",
  "what_changed": "gross_margin is 0.6405609780472368 (revenue 9005700000.0; cost_of_revenue 3237000000.0). year_over_year change -0.000769289976923937 against years-back-1. position_in_history: second highest of the 5 filled years.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"value\": 0.6405609780472368",
  "paragraph_id": "0001596532-26-000175:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend",
  "what_changed": "receivables_over_revenue is 0.20952285774564997 (receivables 1886900000.0; revenue 9005700000.0). year_over_year change 0.04666640845890552 against years-back-1. position_in_history: second highest of the 5 filled years.",
  "account": "accounts receivable, net over revenue",
  "expected_direction": "up",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"value\": 0.20952285774564997",
  "paragraph_id": "0001596532-26-000175:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend",
  "what_changed": "soft_asset_share is 0.888578098166449 (assets 19448600000.0; cash 1963900000.0; property_plant_and_equipment 203100000.0). year_over_year change 0.09231067957189898 against years-back-1. position_in_history: highest of the 5 filled years.",
  "account": "soft assets over total assets",
  "expected_direction": "up",
  "horizon": "year 2025-01-01..2025-12-31 against years-back-1",
  "quote": "\"value\": 0.888578098166449",
  "paragraph_id": "0001596532-26-000175:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
  "what_changed": "insufficient: there is no bad_debt_allowance row for 2025-12-31, and year_over_year reads 'bad_debt_reserve_ratio is not filled in years-back-0'. The ratio is filled only in years-back-3 and years-back-4. Two filled periods do not support a trend claim, and the allowance has no row in the three most recent years.",
  "account": "allowance for credit losses on receivables",
  "expected_direction": "none",
  "horizon": "year 2025-01-01..2025-12-31",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-12-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001596532-26-000175:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend",
  "what_changed": "insufficient: us-gaap:InventoryValuationReserves is tagged in no period of the companyfacts record, so the ratio is filled in 0 of the 5 years.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "year 2025-01-01..2025-12-31",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend",
  "what_changed": "insufficient: no warranty-accrual concept is tagged in any period, so the ratio is filled in 0 of the 5 years.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "year 2025-01-01..2025-12-31",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001596532-26-000175:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend",
  "what_changed": "insufficient: companyfacts holds no non-GAAP measure, so the ratio is filled in 0 of the 5 years. The input has no full-year 2025 non-GAAP net income.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "year 2025-01-01..2025-12-31",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001596532-26-000175:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

**Restated prior values (8-K earnings release 0001596532-26-000174)**

```json
{ "id": "articulation_and_the_filed_history_non_gaap_net_income_recast",
  "what_changed": "Prior-year non-GAAP net income is restated. The release says the retrospective change in its non-GAAP tax method raised non-GAAP net income by $10.7 million for the three months and $30.4 million for the six months ended June 30, 2025. The recast comparatives in the reconciliation are 934.2 and 1,780.1 (in millions). The figures as first reported are not in the input.",
  "account": "non-GAAP net income, prior-year comparatives",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2025, as restated in the release for the period ended June 30, 2026",
  "quote": "The retrospective application of this change resulted in an increase to non-GAAP net income of $10.7 million and $30.4 million for the three and six months ended June 30, 2025, respectively.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:40" }
```

```json
{ "id": "articulation_and_the_filed_history_non_gaap_diluted_eps_recast",
  "what_changed": "Prior-year non-GAAP diluted EPS is restated: an increase of nil for the three months and $0.03 for the six months ended June 30, 2025. The recast comparatives printed are $0.73 and $1.40.",
  "account": "non-GAAP diluted net income per share, prior-year comparatives",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2025",
  "quote": "The impact of this change on non-GAAP diluted net income per share was an increase of nil and $0.03 for the three and six months ended June 30, 2025, respectively.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:40" }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_income_tax_methodology",
  "what_changed": "The release states that, from the fourth quarter of fiscal 2025, the method for the income tax effect of non-GAAP adjustments changed. Direct excess tax benefits on stock awards are still excluded, but the discrete indirect effects of those awards no longer are.",
  "account": "income tax effect of non-GAAP adjustments",
  "expected_direction": "none",
  "horizon": "from the fourth quarter of fiscal 2025 onward",
  "quote": "Effective the fourth quarter of fiscal year 2025, the company updated its methodology for calculating the income tax effect of non-GAAP adjustments.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:53" }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_prior_results_recast",
  "what_changed": "Every prior-period non-GAAP result in the release is recast to the new method, so the non-GAAP comparatives in this release are not the figures first reported.",
  "account": "non-GAAP results, all prior periods presented",
  "expected_direction": "none",
  "horizon": "all prior periods presented in the release",
  "quote": "All prior period non-GAAP results presented in this release have been recast to conform to the current period presentation.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:55" }
```

**Earnings release figures (8-K 0001596532-26-000174, filed 2026-08-04)**

```json
{ "id": "results_against_expectations_revenue_growth",
  "what_changed": "The release prints revenue of $3.036 billion: up 12.1% on the first quarter of 2026 and up 37.7% on the second quarter of 2025.",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "three months ended June 30, 2026 against the prior quarter and the year-earlier quarter",
  "quote": "Revenue of $3.036 billion, an increase of 12.1% compared to the first quarter of 2026, and an increase of 37.7% from the second quarter of 2025.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:11" }
```

```json
{ "id": "results_against_expectations_operating_margin",
  "what_changed": "GAAP operating margin is 45.4% against 44.7% a year earlier; non-GAAP operating margin is 49.9% against 48.8%.",
  "account": "operating margin, GAAP and non-GAAP",
  "expected_direction": "up",
  "horizon": "three months ended June 30, 2026 against three months ended June 30, 2025",
  "quote": "GAAP and non-GAAP operating margin of 45.4% and 49.9%, respectively, compared to GAAP and non-GAAP operating margin of 44.7% and 48.8% in the second quarter of 2025.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:12" }
```

```json
{ "id": "results_against_expectations_diluted_earnings_per_share",
  "what_changed": "GAAP diluted EPS is $0.95 against $0.70; non-GAAP diluted EPS is $1.02 against $0.73. The $0.73 comparative is a recast figure (see the restated items above).",
  "account": "diluted earnings per share, GAAP and non-GAAP",
  "expected_direction": "up",
  "horizon": "three months ended June 30, 2026 against three months ended June 30, 2025",
  "quote": "GAAP and non-GAAP diluted earnings per share of $0.95 and $1.02, respectively, compared to GAAP and non-GAAP diluted earnings per share of $0.70 and $0.73 in the second quarter of 2025.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:13" }
```

```json
{ "id": "results_against_expectations_revenue_outlook",
  "what_changed": "Next-quarter revenue outlook of approximately $3.3 billion, against $3.036 billion just reported. The input has no consensus or other outside expectation to compare it with.",
  "account": "total revenue, company outlook",
  "expected_direction": "up",
  "horizon": "third quarter of 2026",
  "quote": "Revenue of approximately $3.3 billion;",
  "paragraph_id": "0001596532-26-000174:8k_2_02:24" }
```

```json
{ "id": "results_against_expectations_non_gaap_operating_margin_outlook",
  "what_changed": "Next-quarter non-GAAP operating margin outlook of 48 - 49%, against 49.9% printed for the quarter just reported.",
  "account": "non-GAAP operating margin, company outlook",
  "expected_direction": "down",
  "horizon": "third quarter of 2026",
  "quote": "Non-GAAP operating margin of 48 - 49%; and",
  "paragraph_id": "0001596532-26-000174:8k_2_02:25" }
```

```json
{ "id": "results_against_expectations_non_gaap_eps_outlook",
  "what_changed": "Next-quarter non-GAAP diluted EPS outlook of $1.06 to $1.08, against $1.02 printed for the quarter just reported.",
  "account": "non-GAAP diluted net income per share, company outlook",
  "expected_direction": "up",
  "horizon": "third quarter of 2026",
  "quote": "Non-GAAP diluted net income per share between $1.06 and $1.08.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:26" }
```

```json
{ "id": "across_documents_gaap_gross_margin_against_trend_cell",
  "what_changed": "The release prints GAAP gross margin of 62.9% for the quarter against 65.2% a year earlier, and 62.4% against 64.5% for six months. The trend cell for the same quarter prints 0.6292782554270844. The input has no articulation check that reconciles the two documents, and none is computed here.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "three and six months ended June 30, 2026 against the same periods of 2025",
  "quote": "| GAAP gross margin |  | 62.9 | % |  | 65.2 | % |  | 62.4 | % |  | 64.5 | % |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_non_gaap_net_income_against_gaap",
  "what_changed": "Non-GAAP net income is 1,301.7 against 934.2 a year earlier (recast), and 2,409.9 against 1,780.1 for six months. GAAP net income printed in the same table is 1,212.9 against 888.8 (in millions). No gap ratio is in the input, and none is computed.",
  "account": "non-GAAP net income",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2026 against the same periods of 2025",
  "quote": "| Non-GAAP net income(1) |  | $ | 1,301.7 |  |  | $ | 934.2 |  |  | $ | 2,409.9 |  |  | $ | 1,780.1 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_tax_benefits_on_stock_awards_excluded",
  "what_changed": "Tax benefits on stock-based awards removed from non-GAAP net income: (30.9) for the quarter against (32.1), and (65.3) against (80.1) for six months (in millions). The printed exclusion is smaller than a year earlier.",
  "account": "tax benefits on stock-based awards, non-GAAP reconciling item",
  "expected_direction": "down",
  "horizon": "three and six months ended June 30, 2026 against the same periods of 2025",
  "quote": "| Tax benefits on stock-based awards(1) |  | (30.9) |  |  | (32.1) |  |  | (65.3) |  |  | (80.1) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_intangible_amortization_excluded",
  "what_changed": "Intangible asset amortization added back to non-GAAP operating income and net income: 15.3 against 5.0 for the quarter, and 30.6 against 10.6 for six months (in millions). The gross-profit add-back row prints 7.0 against 2.6.",
  "account": "intangible asset amortization, non-GAAP reconciling item",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2026 against the same periods of 2025",
  "quote": "| Intangible asset amortization |  | 15.3 |  |  | 5.0 |  |  | 30.6 |  |  | 10.6 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_strategic_investment_gains_excluded",
  "what_changed": "Gains on strategic investments removed from non-GAAP net income: (6.0) against (5.4) for the quarter, and (8.8) against (10.9) for six months (in millions).",
  "account": "gains/losses on strategic investments, non-GAAP reconciling item",
  "expected_direction": "up",
  "horizon": "three months ended June 30, 2026 against three months ended June 30, 2025",
  "quote": "| (Gains)/losses on strategic investments |  | (6.0) |  |  | (5.4) |  |  | (8.8) |  |  | (10.9) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_income_tax_effect_on_non_gaap_exclusions",
  "what_changed": "Income tax effect on non-GAAP exclusions: (10.0) against (7.3) for the quarter, and (23.7) against (20.3) for six months (in millions). These are figures under the new tax method; the prior-year figures are recast.",
  "account": "income tax effect on non-GAAP exclusions",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2026 against the same periods of 2025",
  "quote": "| Income tax effect on non-GAAP exclusions(1) |  | (10.0) |  |  | (7.3) |  |  | (23.7) |  |  | (20.3) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_research_and_development_expense",
  "what_changed": "Research and development expense is 348.2 against 296.5 for the quarter, and 691.9 against 562.9 for six months (in millions).",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "three and six months ended June 30, 2026 against the same periods of 2025",
  "quote": "| Research and development |  | 348.2 |  |  | 296.5 |  |  | 691.9 |  |  | 562.9 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:34" }
```

```json
{ "id": "revenue_recognition_non_current_deferred_revenue",
  "what_changed": "Non-current deferred revenue is 1,765.2 at June 30, 2026 against 1,369.8 at December 31, 2025 (in millions). The trend ratio uses the current portion only, so this balance sits outside contract_liabilities_over_revenue.",
  "account": "deferred revenue, non-current",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "| Deferred revenue, non-current |  | 1,765.2 |  |  | 1,369.8 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:44" }
```

```json
{ "id": "earnings_quality_other_current_liabilities",
  "what_changed": "Other current liabilities are 538.4 at June 30, 2026 against 246.8 at December 31, 2025 (in millions).",
  "account": "other current liabilities",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "| Other current liabilities |  | 538.4 |  |  | 246.8 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:44" }
```

```json
{ "id": "earnings_quality_deferred_tax_assets",
  "what_changed": "Deferred tax assets are 2,001.6 at June 30, 2026 against 1,773.6 at December 31, 2025 (in millions).",
  "account": "deferred tax assets",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "| Deferred tax assets |  | 2,001.6 |  |  | 1,773.6 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:44" }
```

```json
{ "id": "earnings_quality_other_assets_balance",
  "what_changed": "Other (non-current) assets are 826.5 at June 30, 2026 against 668.8 at December 31, 2025 (in millions).",
  "account": "other assets, non-current",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "| Other assets |  | 826.5 |  |  | 668.8 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:44" }
```

```json
{ "id": "liquidity_and_capital_accumulated_other_comprehensive_loss",
  "what_changed": "Accumulated other comprehensive income (loss) is (40.5) at June 30, 2026 against 12.0 at December 31, 2025 (in millions).",
  "account": "accumulated other comprehensive income (loss)",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "| Accumulated other comprehensive income (loss) |  | (40.5) |  |  | 12.0 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:44" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow",
  "what_changed": "Net cash provided by operating activities is 2,776.5 for the six months ended June 30, 2026 against 1,841.8 a year earlier (in millions). No three-month figure is in the input.",
  "account": "net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Net cash provided by operating activities |  | 2,776.5 |  |  | 1,841.8 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "revenue_recognition_receivables_operating_cash_use",
  "what_changed": "The change in accounts receivable used (379.3) of operating cash in six months, against (483.1) a year earlier (in millions).",
  "account": "accounts receivable, net, change in operating cash flow",
  "expected_direction": "down",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Accounts receivable, net |  | (379.3) |  |  | (483.1) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_inventory_operating_cash_use",
  "what_changed": "The change in inventories used (288.2) of operating cash in six months, against (224.5) a year earlier (in millions).",
  "account": "inventories, change in operating cash flow",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Inventories |  | (288.2) |  |  | (224.5) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_other_assets_operating_cash_outflow",
  "what_changed": "The change in other assets used (619.7) of operating cash in six months, against (403.2) a year earlier (in millions).",
  "account": "other assets, change in operating cash flow",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Other assets |  | (619.7) |  |  | (403.2) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_operating_cash_inflow",
  "what_changed": "The change in deferred revenue provided 1,493.5 of operating cash in six months, against 1,141.4 a year earlier (in millions).",
  "account": "deferred revenue, change in operating cash flow",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Deferred revenue |  | 1,493.5 |  |  | 1,141.4 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_deferred_income_taxes_in_operating_cash_flow",
  "what_changed": "Deferred income taxes are (213.1) in the six-month operating cash flow, against (337.9) a year earlier (in millions).",
  "account": "deferred income taxes, operating cash flow adjustment",
  "expected_direction": "down",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Deferred income taxes |  | (213.1) |  |  | (337.9) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_income_taxes_net_in_operating_cash_flow",
  "what_changed": "The change in income taxes, net provided 198.4 in six months, against 152.4 a year earlier (in millions).",
  "account": "income taxes, net, change in operating cash flow",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Income taxes, net |  | 198.4 |  |  | 152.4 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_accounts_payable_in_operating_cash_flow",
  "what_changed": "The change in accounts payable provided 40.9 in six months, against 160.0 a year earlier (in millions).",
  "account": "accounts payable, change in operating cash flow",
  "expected_direction": "down",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Accounts payable |  | 40.9 |  |  | 160.0 |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_other_liabilities_in_operating_cash_flow",
  "what_changed": "The change in other liabilities is 30.8 in six months, against (49.7) a year earlier (in millions).",
  "account": "other liabilities, change in operating cash flow",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Other liabilities |  | 30.8 |  |  | (49.7) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

```json
{ "id": "liquidity_and_capital_purchases_of_property_and_equipment",
  "what_changed": "Purchases of property and equipment are (84.2) in six months, against (52.4) a year earlier (in millions).",
  "account": "capital expenditure",
  "expected_direction": "up",
  "horizon": "six months ended June 30, 2026 against six months ended June 30, 2025",
  "quote": "| Purchases of property and equipment |  | (84.2) |  |  | (52.4) |  |",
  "paragraph_id": "0001596532-26-000174:8k_2_02:49" }
```

**Numeric facts (input_numbers.json)**

```json
{ "id": "earnings_quality_effective_tax_rate_quarterly",
  "what_changed": "The effective income tax rate for the quarter is 0.194, against 0.177 for 2025-04-01..2025-06-30. Income tax expense rows print 291400000 against 191400000.",
  "account": "effective income tax rate",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"0.194\"",
  "paragraph_id": "0001596532-26-000175:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_cumulative",
  "what_changed": "The effective income tax rate for 2026-01-01..2026-06-30 is 0.195, against 0.163 for 2025-01-01..2025-06-30. Income tax expense rows print 539900000 against 332600000.",
  "account": "effective income tax rate",
  "expected_direction": "up",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"0.195\"",
  "paragraph_id": "0001596532-26-000175:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_total_contract_liabilities",
  "what_changed": "Total contract liabilities (current plus non-current) are 6865900000 at 2026-06-30. The same filing prints 6198700000 at 2026-03-31, 5372400000 at 2025-12-31, 4061700000 at 2025-06-30, 3088800000 at 2025-03-31 and 2791400000 at 2024-12-31.",
  "account": "contract liabilities (deferred revenue), total",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2026-03-31, 2025-12-31 and 2025-06-30",
  "quote": "\"value\": \"6865900000\"",
  "paragraph_id": "0001596532-26-000175:facts:ContractWithCustomerLiability:2026-06-30" }
```

```json
{ "id": "revenue_recognition_revenue_released_from_contract_liabilities",
  "what_changed": "Revenue recognized from contract liabilities is 1036000000 for the quarter, against 337400000 for 2025-04-01..2025-06-30. The six-month rows print 2212500000 against 735800000.",
  "account": "revenue recognized from opening contract liabilities",
  "expected_direction": "up",
  "horizon": "three and six months ended 2026-06-30 against the same periods of 2025",
  "quote": "\"value\": \"1036000000\"",
  "paragraph_id": "0001596532-26-000175:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_deferred_costs_current",
  "what_changed": "Current deferred costs are 1621900000 at 2026-06-30, against 1197000000 at 2025-12-31.",
  "account": "deferred costs, current",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"1621900000\"",
  "paragraph_id": "0001596532-26-000175:facts:DeferredCostsCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_prepaid_and_other_current_assets",
  "what_changed": "Prepaid expenses and other current assets are 2018600000 at 2026-06-30, against 1510000000 at 2025-12-31. The other-prepaid-expense row within it prints 396700000 against 313000000.0.",
  "account": "prepaid expenses and other current assets",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"2018600000\"",
  "paragraph_id": "0001596532-26-000175:facts:PrepaidExpenseAndOtherAssetsCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_evaluation_inventory",
  "what_changed": "Finished goods held as evaluation inventory are 616000000.0 at 2026-06-30, against 403700000 at 2025-12-31.",
  "account": "inventory, finished goods: evaluation inventory",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"616000000.0\"",
  "paragraph_id": "0001596532-26-000175:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30:us-gaap:PublicUtilitiesInventoryAxis=anet:EvaluationInventoryMember" }
```

```json
{ "id": "earnings_quality_raw_materials_inventory",
  "what_changed": "Raw materials inventory, net of reserves, is 859600000 at 2026-06-30, against 611200000 at 2025-12-31.",
  "account": "inventory, raw materials",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"859600000\"",
  "paragraph_id": "0001596532-26-000175:facts:InventoryRawMaterialsNetOfReserves:2026-06-30" }
```

```json
{ "id": "earnings_quality_finished_goods_inventory",
  "what_changed": "Finished goods inventory, net of reserves, is 1675700000 at 2026-06-30, against 1635900000 at 2025-12-31. Total inventory, net is 2535300000 against 2247100000.",
  "account": "inventory, finished goods",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"1675700000\"",
  "paragraph_id": "0001596532-26-000175:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_downs",
  "what_changed": "The 10-K reports an inventory write-down of 131600000 for 2025. Its rows for 2024 and 2023 read 267200000 and 234400000. Three annual points.",
  "account": "inventory write-downs",
  "expected_direction": "down",
  "horizon": "year 2025 against 2024 and 2023",
  "quote": "\"value\": \"131600000\"",
  "paragraph_id": "0001596532-26-000013:facts:InventoryWriteDown:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_purchase_commitments",
  "what_changed": "The remaining minimum committed amount of purchase commitments is 9700000000 at 2026-06-30. The earlier filings' rows read 8900000000 at 2026-03-31 and 6800000000 at 2025-12-31.",
  "account": "purchase commitments, remaining minimum amount",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-12-31",
  "quote": "\"value\": \"9700000000\"",
  "paragraph_id": "0001596532-26-000175:facts:PurchaseCommitmentRemainingMinimumAmountCommitted:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_purchase_obligations_due_near_term",
  "what_changed": "Purchase obligations due in the next twelve months are 9400000000 at 2026-06-30. No comparative row for this concept was read.",
  "account": "purchase obligations due within the next twelve months",
  "expected_direction": "none",
  "horizon": "as of 2026-06-30",
  "quote": "\"value\": \"9400000000\"",
  "paragraph_id": "0001596532-26-000175:facts:PurchaseObligationDueInNextTwelveMonths:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases",
  "what_changed": "Stock repurchased and retired is 0 for 2026-01-01..2026-06-30. The release's cash flow statement prints repurchases of (983.0) million for the six months ended June 30, 2025.",
  "account": "share repurchases",
  "expected_direction": "down",
  "horizon": "six months ended 2026-06-30 against six months ended 2025-06-30",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001596532-26-000175:facts:StockRepurchasedAndRetiredDuringPeriodValue:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_remaining_repurchase_authorization",
  "what_changed": "The remaining authorized repurchase amount is 817900000 at 2026-06-30. No comparative row for this concept was read.",
  "account": "stock repurchase program, remaining authorization",
  "expected_direction": "none",
  "horizon": "as of 2026-06-30",
  "quote": "\"value\": \"817900000\"",
  "paragraph_id": "0001596532-26-000175:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_marketable_securities_balance",
  "what_changed": "Available-for-sale debt securities total 11053100000 at 2026-06-30. Investments at fair value print 8779100000 at 2025-12-31.",
  "account": "marketable securities (available-for-sale debt securities)",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"11053100000\"",
  "paragraph_id": "0001596532-26-000175:facts:AvailableForSaleSecuritiesDebtSecurities:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_unrealized_losses_on_marketable_securities",
  "what_changed": "Gross unrealized losses on available-for-sale debt securities are 40800000 at 2026-06-30, against 1500000 at 2025-12-31. Gross unrealized gains print 2300000 against 27500000.",
  "account": "available-for-sale debt securities, gross unrealized loss",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"40800000\"",
  "paragraph_id": "0001596532-26-000175:facts:AvailableForSaleDebtSecuritiesAccumulatedGrossUnrealizedLossBeforeTax:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_securities_in_continuous_unrealized_loss_position",
  "what_changed": "Fair value of debt securities that have been in a continuous unrealized loss position for under twelve months is 8489700000 at 2026-06-30, with an accumulated loss of 40800000. No comparative row was read.",
  "account": "available-for-sale debt securities in an unrealized loss position",
  "expected_direction": "none",
  "horizon": "as of 2026-06-30",
  "quote": "\"value\": \"8489700000\"",
  "paragraph_id": "0001596532-26-000175:facts:DebtSecuritiesAvailableForSaleContinuousUnrealizedLossPositionLessThan12Months:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_construction_in_progress",
  "what_changed": "Construction in progress (gross property and equipment) is 213500000 at 2026-06-30, against 107900000 at 2025-12-31.",
  "account": "property and equipment: construction in progress",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"213500000\"",
  "paragraph_id": "0001596532-26-000175:facts:PropertyPlantAndEquipmentGross:2026-06-30:us-gaap:PropertyPlantAndEquipmentByTypeAxis=us-gaap:ConstructionInProgressMember" }
```

```json
{ "id": "liquidity_and_capital_property_and_equipment_net",
  "what_changed": "Property and equipment, net is 312500000 at 2026-06-30, against 203100000 at 2025-12-31. It is an input to soft_asset_share.",
  "account": "property and equipment, net",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"312500000\"",
  "paragraph_id": "0001596532-26-000175:facts:PropertyPlantAndEquipmentNet:2026-06-30" }
```

```json
{ "id": "earnings_quality_stock_based_compensation_expense",
  "what_changed": "Share-based compensation expense is 120400000 for the quarter, against 85200000 for 2025-04-01..2025-06-30. The six-month rows print 241300000 against 178200000.",
  "account": "stock-based compensation expense",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"120400000\"",
  "paragraph_id": "0001596532-26-000175:facts:AllocatedShareBasedCompensationExpense:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_interest_income",
  "what_changed": "Interest income is 122400000 for the quarter, against 90400000 for 2025-04-01..2025-06-30.",
  "account": "interest income",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"122400000\"",
  "paragraph_id": "0001596532-26-000175:facts:InterestIncomeOther:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_nonoperating_income",
  "what_changed": "Nonoperating income is 126300000 for the quarter, against 94000000.0 for 2025-04-01..2025-06-30. Other nonoperating gains print 3900000 against 3600000.",
  "account": "other income (expense), net",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"126300000\"",
  "paragraph_id": "0001596532-26-000175:facts:NonoperatingIncomeExpense:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_total_revenue",
  "what_changed": "Revenue is 3035700000 for the quarter, against 2204800000 for 2025-04-01..2025-06-30. The six-month rows print 5744700000 against 4209600000.",
  "account": "revenue from contracts with customers",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"3035700000\"",
  "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_americas_revenue",
  "what_changed": "Americas revenue is 2337900000 for the quarter, against 1724100000 for 2025-04-01..2025-06-30.",
  "account": "revenue, Americas",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"2337900000\"",
  "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_united_states_revenue",
  "what_changed": "United States revenue is 2319600000 for the quarter, against 1712100000 for 2025-04-01..2025-06-30.",
  "account": "revenue, United States",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"2319600000\"",
  "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:US" }
```

```json
{ "id": "revenue_recognition_emea_revenue",
  "what_changed": "EMEA revenue is 438200000 for the quarter, against 281600000 for 2025-04-01..2025-06-30.",
  "account": "revenue, EMEA",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"438200000\"",
  "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_asia_pacific_revenue",
  "what_changed": "Asia-Pacific revenue is 259600000 for the quarter, against 199100000 for 2025-04-01..2025-06-30.",
  "account": "revenue, Asia-Pacific",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
  "quote": "\"value\": \"259600000\"",
  "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "earnings_quality_acquired_intangible_assets_net",
  "what_changed": "Finite-lived intangible assets, net are 258200000 at 2026-06-30, against 288800000 at 2025-12-31. Gross is 490300000 at both dates; accumulated amortization is 232100000 against 201500000.",
  "account": "finite-lived intangible assets, net",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2025-12-31",
  "quote": "\"value\": \"258200000\"",
  "paragraph_id": "0001596532-26-000175:facts:FiniteLivedIntangibleAssetsNet:2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_acquisition_consideration",
  "what_changed": "The VeloCloud acquisition, dated 2025-06-30, is still disclosed. Consideration transferred is 300000000.0, of which 116400000 is liabilities incurred. Finite-lived intangibles acquired are 268400000 and goodwill acquired is 148000000.0. The acquisition falls inside the year-over-year window of the quarterly trend cells.",
  "account": "business combination: VeloCloud",
  "expected_direction": "none",
  "horizon": "acquisition dated 2025-06-30",
  "quote": "\"value\": \"300000000.0\"",
  "paragraph_id": "0001596532-26-000175:facts:BusinessCombinationConsiderationTransferred1:2025-06-30..2025-06-30:us-gaap:BusinessAcquisitionAxis=anet:VeloCloudMember" }
```

## Seen in the notes

No item. The instructions say each fact is marked with whether its element sat inside a note when it was extracted, but no fact row in input_numbers.json carries such a mark. Each row holds only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and sometimes superseded_by. The trend table and the release carry no such mark either. Putting a finding here would mean judging note status myself, so none is placed here. Every fact item above sits under "Seen in the statements" only because nothing marks it as from a note.
