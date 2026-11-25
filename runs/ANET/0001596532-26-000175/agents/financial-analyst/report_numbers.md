<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# ANET — numbers reader — 10-Q 0001596532-26-000175 (filed 2026-08-05), 8-K 0001596532-26-000174 (filed 2026-08-04)

## What the input holds, and what it does not

- Inputs read in full: `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md`, `input_trends.json`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.
- Prior flags: none. `input_prior_predictions.md` says "None on record."
- `input_numbers.json` holds only `ticker`, `cutoff`, `documents` (10-K 0001596532-26-000013, prior 10-Q 0001596532-26-000078, 10-Q 0001596532-26-000175) and `facts`. It holds **no articulation checks, no restatement traces and no fourth-quarter derivation**, so there is no articulation gap, no restated prior value and no Python-flagged change of tag to quote. The only history marker on a fact is `superseded_by`, which says that a later filing re-reported the period. Every superseded value this report compared against the later filing's figure was the same figure. One example is reported below; the input itself states no differing value.
- No fact in `input_numbers.json` carries a marker saying whether its element sat inside a note. See the second heading.
- **Periods the record does not reach.** `quarters-back-2` (target end 2025-12-30) and `quarters-back-6` (target end 2024-12-31) have no cells. The reason each gives is "no quarter ending within 20 days of 2025-12-30 [2024-12-31] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The output of that derivation is not in this directory. As a result, `quarters-back-1` has no quarter-over-quarter change for any metric, and every quarterly history below counts 6 filled quarters, not 8.
- The `years-back-0` R&D-capitalization block prints no `paragraph_id`, so none of it is written as an item. It prints `book_value_with_rnd_capitalized` 15326808000.0, `earnings_with_rnd_capitalized` 4018032000.0, `research_and_development_amortization` 730668000.0 and `research_and_development_asset` 2956308000.0. `capitalized_development_cost` is missing: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period."
- The 8-K item-code list and the late-filing line print no paragraph id, so they are not items. The list holds codes 2.02, 5.02, 5.03, 5.07, 8.01 and 9.01 only, with no 4.01 or 4.02. Late-filing notifications: "none on or before 2026-08-05".
- **What `expected_direction` means here.** It gives the way the item points for the account named, over the horizon named. For trend metrics it follows the signs Python printed. Quarterly cells whose quarter-over-quarter and year-over-year changes have the same sign take that sign. Cells whose changes have opposite signs are `none`. Annual cells take the sign of the year-over-year change. Every insufficient item is `none`.

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-01..2026-06-30, 91 days)

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly", "what_changed": "insufficient: accruals_over_total_assets is not filled in quarters-back-0 because the record holds no operating-cash-flow row for 2026-04-01..2026-06-30. The filing tags operating cash flow only year-to-date (2776500000 for 2026-01-01..2026-06-30). A three-month operating cash flow does not exist in the input and is not derived here. The ratio is filled in only 2 quarters of the record: quarters-back-1 at -0.03096529910188627 (lowest of the 2) and quarters-back-5 at 0.0118570267179254 (highest of the 2). Two values support no trend claim.", "account": "operating accruals (net income less operating cash flow) over total assets", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0001596532-26-000175:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly", "what_changed": "insufficient: bad_debt_reserve_ratio is not filled in quarters-back-0, and it is filled in none of the 6 filled quarters. The allowance concepts exist in the record but carry no 2026-06-30 row. The ratio is filled only in years-back-3 and years-back-4.", "account": "allowance for doubtful accounts over gross receivables", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0001596532-26-000175:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_quarterly", "what_changed": "contract_liabilities_over_revenue is 1.6802384952399776 (formula contract_liabilities / revenue; inputs ContractWithCustomerLiabilityCurrent 5100700000.0 at 2026-06-30 and quarterly revenue 3035700000.0). Quarter-over-quarter change against quarters-back-1: -0.13205386356400917. Year-over-year change against quarters-back-4: 0.4159061294925175. Position: second highest of the 6 filled quarters; the highest is quarters-back-1 at 1.8122923588039868. The two changes have opposite signs.", "account": "current contract liabilities (deferred revenue) relative to quarterly revenue", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"", "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_days_sales_of_inventory_trend_quarterly", "what_changed": "days_sales_of_inventory is 205.00470943664473 (formula inventory / cost_of_revenue * days_in_period; inputs InventoryNet 2535300000.0 at 2026-06-30 and quarterly cost of revenue 1125400000.0). Quarter-over-quarter change against quarters-back-1: -2.5132134465174545. Year-over-year change against quarters-back-4: -39.55036756674863. Position: lowest of the 6 filled quarters.", "account": "inventory days", "expected_direction": "down", "horizon": "next quarter", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001596532-26-000175:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_quarterly", "what_changed": "days_sales_outstanding is 67.93299733175215 (formula receivables / revenue * days_in_period; inputs AccountsReceivableNetCurrent 2266200000.0 at 2026-06-30 and quarterly revenue 3035700000.0). Quarter-over-quarter change against quarters-back-1: 4.019376069293678. Year-over-year change against quarters-back-4: 0.9212048789219693. Position: highest of the 6 filled quarters.", "account": "receivable days", "expected_direction": "up", "horizon": "next quarter", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001596532-26-000175:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_quarterly", "what_changed": "gross_margin is 0.6292782554270844 (formula (revenue - cost_of_revenue) / revenue; inputs revenue 3035700000.0 and cost of revenue 1125400000.0). Quarter-over-quarter change against quarters-back-1: 0.010304464360270105. Year-over-year change against quarters-back-4: -0.0232072307848169. Position: second lowest of the 6 filled quarters; the lowest is quarters-back-1 at 0.6189737910668143 and the highest is quarters-back-4 at 0.6524854862119013. The two changes have opposite signs.", "account": "GAAP gross margin", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"", "paragraph_id": "0001596532-26-000175:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_quarterly", "what_changed": "insufficient: inventory_reserve_ratio is not filled in quarters-back-0 or in any period of the record, because the company tags no inventory valuation reserve. The cell says the filing, not this record, would say whether the reserve is untagged or stated only by segment.", "account": "inventory valuation reserve over gross inventory", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001596532-26-000175:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_quarterly", "what_changed": "insufficient: non_gaap_gap is not filled in quarters-back-0 or in any period, because companyfacts carries no non-GAAP measure. For the quarter the release prints GAAP net income 1,212.9 and non-GAAP net income 1,301.7 (millions). The trend table computes no gap from them, and none is computed here.", "account": "gap between non-GAAP and GAAP net income", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001596532-26-000175:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_quarterly", "what_changed": "receivables_over_revenue is 0.7465164541950786 (formula receivables / revenue; inputs 2266200000.0 and 3035700000.0). Quarter-over-quarter change against quarters-back-1: 0.03636510683442895. Year-over-year change against quarters-back-4: 0.010123130537604053. Position: highest of the 6 filled quarters.", "account": "accounts receivable relative to quarterly revenue", "expected_direction": "up", "horizon": "next quarter", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001596532-26-000175:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_quarterly", "what_changed": "soft_asset_share is 0.8902744929405862 (formula (assets - property_plant_and_equipment - cash) / assets; inputs Assets 23720100000.0, PropertyPlantAndEquipmentNet 312500000.0 and CashAndCashEquivalentsAtCarryingValue 2290200000.0). Quarter-over-quarter change against quarters-back-1: 0.030638817739145563. Year-over-year change against quarters-back-4: 0.03408550284732503. Position: highest of the 6 filled quarters.", "account": "share of assets other than cash and property, plant and equipment", "expected_direction": "up", "horizon": "next quarter", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001596532-26-000175:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_quarterly", "what_changed": "insufficient: warranty_reserve_ratio is not filled in quarters-back-0 or in any period of the record, because none of the three warranty-accrual concepts is tagged.", "account": "product warranty accrual relative to revenue", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period.", "paragraph_id": "0001596532-26-000175:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

### Trend table — years-back-0 (2025-01-01..2025-12-31, 365 days)

Every annual cell's quarter-over-quarter reason is "an annual period has no preceding quarter".

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_annual", "what_changed": "accruals_over_total_assets for 2025 is -0.044244829962053825 (formula (net_income - operating_cash_flow) / assets; inputs NetIncomeLoss 3511400000.0, NetCashProvidedByUsedInOperatingActivities 4371900000.0, both from the 10-K, and Assets 19448600000.0 from the 10-Q). Year-over-year change against years-back-1: 0.016714020499712497. Position: second lowest of the 5 filled years; the lowest is years-back-1 at -0.06095885046176632.", "account": "operating accruals over total assets", "expected_direction": "up", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_annual", "what_changed": "insufficient: bad_debt_reserve_ratio is not filled for 2025. It is filled only in years-back-3 (2.0582484305855718e-05, lowest of the 2 filled years) and years-back-4 (0.0002554965633776646, highest of the 2). Two years of history support no trend claim.", "account": "allowance for doubtful accounts over gross receivables", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-12-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0001596532-26-000175:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_annual", "what_changed": "contract_liabilities_over_revenue for 2025 is 0.44445184716346314 (inputs ContractWithCustomerLiabilityCurrent 4002600000.0 at 2025-12-31 from the 10-Q and revenue 9005700000.0 from the 10-K). Year-over-year change against years-back-1: 0.19780393409639285. Position: highest of the 5 filled years.", "account": "current contract liabilities (deferred revenue) relative to annual revenue", "expected_direction": "up", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_days_sales_of_inventory_trend_annual", "what_changed": "days_sales_of_inventory for 2025 is 253.3801359283287 (inputs InventoryNet 2247100000.0 at 2025-12-31 and cost of revenue 3237000000.0). Year-over-year change against years-back-1: -13.943536338571533. Position: second lowest of the 5 filled years; the lowest is years-back-4 at 222.33865194732672.", "account": "inventory days", "expected_direction": "down", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_annual", "what_changed": "days_sales_outstanding for 2025 is 76.47584307716224 (inputs AccountsReceivableNetCurrent 1886900000.0 at 2025-12-31 and revenue 9005700000.0). Year-over-year change against years-back-1: 16.87038263821377. Position: second highest of the 5 filled years; the highest is years-back-3 at 76.90166639658003.", "account": "receivable days", "expected_direction": "up", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_annual", "what_changed": "gross_margin for 2025 is 0.6405609780472368 (inputs revenue 9005700000.0 and cost of revenue 3237000000.0). Year-over-year change against years-back-1: -0.000769289976923937. Position: second highest of the 5 filled years; the highest is years-back-1 at 0.6413302680241607.", "account": "GAAP gross margin", "expected_direction": "down", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_annual", "what_changed": "insufficient: inventory_reserve_ratio is not filled for 2025 or for any year of the record, because no inventory valuation reserve is tagged.", "account": "inventory valuation reserve over gross inventory", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001596532-26-000175:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_annual", "what_changed": "insufficient: non_gaap_gap is not filled for 2025 or for any year, because companyfacts carries no non-GAAP measure.", "account": "gap between non-GAAP and GAAP net income", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001596532-26-000175:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_annual", "what_changed": "receivables_over_revenue for 2025 is 0.20952285774564997 (inputs 1886900000.0 and 9005700000.0). Year-over-year change against years-back-1: 0.04666640845890552. Position: second highest of the 5 filled years; the highest is years-back-3 at 0.21068949697693157.", "account": "accounts receivable relative to annual revenue", "expected_direction": "up", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_annual", "what_changed": "soft_asset_share for 2025 is 0.888578098166449 (inputs Assets 19448600000.0, PropertyPlantAndEquipmentNet 203100000.0 and CashAndCashEquivalentsAtCarryingValue 1963900000.0, all at 2025-12-31). Year-over-year change against years-back-1: 0.09231067957189898. Position: highest of the 5 filled years.", "account": "share of assets other than cash and property, plant and equipment", "expected_direction": "up", "horizon": "fiscal year 2026", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001596532-26-000175:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_annual", "what_changed": "insufficient: warranty_reserve_ratio is not filled for 2025 or for any year, because no warranty-accrual concept is tagged.", "account": "product warranty accrual relative to revenue", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period.", "paragraph_id": "0001596532-26-000175:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

### Filed history and tags

```json
{ "id": "articulation_and_the_filed_history_superseded_year_end_cash_tagged", "what_changed": "The 10-K's 2025-12-31 cash fact (value 1963900000) is marked superseded by the second-quarter 10-Q. The 10-Q's 2025-12-31 cash, used as a trend input, is 1963900000.0, the same figure. The input carries no restatement trace, and no superseded fact compared in this report showed a different value. No restated prior value is found.", "account": "cash and cash equivalents", "expected_direction": "none", "horizon": "none", "quote": "\"superseded_by\": \"0001596532-26-000175\"", "paragraph_id": "0001596532-26-000013:facts:CashAndCashEquivalentsAtCarryingValue:2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_capital_expenditure_tag_annual_filing", "what_changed": "The 10-K tags 2025 capital spending as PaymentsToAcquireProductiveAssets (value 119500000; also 2024 and 2023). The 10-Qs tag the same line as PaymentsToAcquirePropertyPlantAndEquipment, including the 2025 comparative periods. The input does not itself flag this as a change of concept; it is reported as observed in the fact rows.", "account": "purchases of property and equipment", "expected_direction": "none", "horizon": "none", "quote": "\"tag\": \"PaymentsToAcquireProductiveAssets\"", "paragraph_id": "0001596532-26-000013:facts:PaymentsToAcquireProductiveAssets:2025-01-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_capital_expenditure_tag_quarterly_filing", "what_changed": "The second-quarter 10-Q tags six-month capital spending as PaymentsToAcquirePropertyPlantAndEquipment: 84200000 for 2026 and 52400000 for the 2025 comparative. The 10-K used PaymentsToAcquireProductiveAssets for the annual figure.", "account": "purchases of property and equipment", "expected_direction": "none", "horizon": "none", "quote": "\"tag\": \"PaymentsToAcquirePropertyPlantAndEquipment\"", "paragraph_id": "0001596532-26-000175:facts:PaymentsToAcquirePropertyPlantAndEquipment:2026-01-01..2026-06-30" }
```

### Numeric facts

```json
{ "id": "revenue_recognition_deferred_costs_current_tagged", "what_changed": "DeferredCostsCurrent prints 1621900000 at 2026-06-30 against 1197000000 at 2025-12-31 in the same filing. The prior 10-Q printed 1546500000 at 2026-03-31 and the 10-K printed 291300000 at 2024-12-31. The balance is higher at each later date in the record.", "account": "deferred costs, current", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"1621900000\"", "paragraph_id": "0001596532-26-000175:facts:DeferredCostsCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_total_contract_liabilities_tagged", "what_changed": "ContractWithCustomerLiability (all contract liabilities) prints 6865900000 at 2026-06-30. The same filing prints 6198700000 at 2026-03-31, 5372400000 at 2025-12-31 and 4061700000 at 2025-06-30. The release prints deferred revenue 5,100.7 and deferred revenue, non-current 1,765.2 (millions) at June 30, 2026.", "account": "contract liabilities (deferred revenue), current and non-current", "expected_direction": "up", "horizon": "next four quarters", "quote": "\"value\": \"6865900000\"", "paragraph_id": "0001596532-26-000175:facts:ContractWithCustomerLiability:2026-06-30" }
```

```json
{ "id": "revenue_recognition_revenue_from_contract_liability_balance_tagged", "what_changed": "Revenue recognized from the contract-liability balance prints 1036000000 for 2026-04-01..2026-06-30 against 337400000 for 2025-04-01..2025-06-30. The six-month figures are 2212500000 against 735800000. The prior 10-Q printed 1264400000 for 2026-01-01..2026-03-31 against 418300000.", "account": "revenue recognized out of contract liabilities", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"1036000000\"", "paragraph_id": "0001596532-26-000175:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_unbilled_product_remaining_performance_obligation_tagged", "what_changed": "Remaining performance obligations for product, unbilled, print 1300000000 at 2026-06-30 (decimals -8). The same filing also prints unbilled RPO of 427800000 and product RPO of 875100000 under other contexts; the input does not say how the three relate. The 10-K printed 503100000 for unbilled product RPO at 2025-12-31 and the prior 10-Q printed 1200000000.", "account": "remaining performance obligations, unbilled product", "expected_direction": "up", "horizon": "next four quarters", "quote": "\"value\": \"1300000000\"", "paragraph_id": "0001596532-26-000175:facts:RevenueRemainingPerformanceObligation:2026-06-30:srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:AccountsNotesLoansAndFinancingReceivablesByBillingStatusTypeAxis=us-gaap:UnbilledRevenuesMember" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_timing_tagged", "what_changed": "The filing tags 0.91 of remaining performance obligations to the period starting 2026-07-01 and 0.09 to the period starting 2028-07-01. The 10-K tagged 0.90 from 2026-01-01 and 0.10 from 2028-01-01.", "account": "timing of remaining performance obligations", "expected_direction": "none", "horizon": "next four quarters", "quote": "\"value\": \"0.91\"", "paragraph_id": "0001596532-26-000175:facts:RevenueRemainingPerformanceObligationPercentage:2026-06-30:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-07-01" }
```

```json
{ "id": "estimates_and_discretion_evaluation_inventory_tagged", "what_changed": "Finished goods held as evaluation inventory print 616000000.0 at 2026-06-30 against 403700000 at 2025-12-31 in the same filing. The prior 10-Q printed 525700000 at 2026-03-31 and the 10-K printed 422100000 at 2024-12-31.", "account": "evaluation inventory (finished goods)", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"616000000.0\"", "paragraph_id": "0001596532-26-000175:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30:us-gaap:PublicUtilitiesInventoryAxis=anet:EvaluationInventoryMember" }
```

```json
{ "id": "estimates_and_discretion_raw_materials_inventory_tagged", "what_changed": "InventoryRawMaterialsNetOfReserves prints 859600000 at 2026-06-30 against 611200000 at 2025-12-31.", "account": "raw materials inventory, net of reserves", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"859600000\"", "paragraph_id": "0001596532-26-000175:facts:InventoryRawMaterialsNetOfReserves:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_finished_goods_inventory_tagged", "what_changed": "InventoryFinishedGoodsNetOfReserves (all finished goods) prints 1675700000 at 2026-06-30 against 1635900000 at 2025-12-31. Total InventoryNet prints 2535300000 against 2247100000.", "account": "finished goods inventory, net of reserves", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"1675700000\"", "paragraph_id": "0001596532-26-000175:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_tagged", "what_changed": "The 10-K tags inventory write-downs of 131600000 for 2025, 267200000 for 2024 and 234400000 for 2023. This report found no 2026 write-down fact in the input.", "account": "inventory write-down", "expected_direction": "down", "horizon": "fiscal year 2026", "quote": "\"value\": \"131600000\"", "paragraph_id": "0001596532-26-000013:facts:InventoryWriteDown:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_purchase_commitments_tagged", "what_changed": "PurchaseCommitmentRemainingMinimumAmountCommitted prints 9700000000 at 2026-06-30 (decimals -8). The prior 10-Q printed 8900000000 at 2026-03-31 and the 10-K printed 6800000000 at 2025-12-31.", "account": "non-cancellable purchase commitments", "expected_direction": "up", "horizon": "next four quarters", "quote": "\"value\": \"9700000000\"", "paragraph_id": "0001596532-26-000175:facts:PurchaseCommitmentRemainingMinimumAmountCommitted:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_purchase_obligations_next_twelve_months_tagged", "what_changed": "PurchaseObligationDueInNextTwelveMonths prints 9400000000 at 2026-06-30. The prior 10-Q printed 7600000000 and the 10-K printed 6300000000.", "account": "purchase obligations due within twelve months", "expected_direction": "up", "horizon": "next four quarters", "quote": "\"value\": \"9400000000\"", "paragraph_id": "0001596532-26-000175:facts:PurchaseObligationDueInNextTwelveMonths:2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_tagged", "what_changed": "EffectiveIncomeTaxRateContinuingOperations prints 0.194 for 2026-04-01..2026-06-30 against 0.177 for 2025-04-01..2025-06-30; the six-month rates are 0.195 against 0.163. The prior 10-Q printed 0.195 for 2026-01-01..2026-03-31 against 0.148. The 10-K printed 0.1737 for 2025 against 0.1265 for 2024. The income tax provision for the quarter prints 291400000 against 191400000.", "account": "effective income tax rate", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"0.194\"", "paragraph_id": "0001596532-26-000175:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_deferred_income_tax_benefit_tagged", "what_changed": "DeferredIncomeTaxExpenseBenefit prints -213100000 for 2026-01-01..2026-06-30 against -337900000 for 2025-01-01..2025-06-30. The deferred tax benefit in the cash-flow reconciliation is smaller than a year earlier.", "account": "deferred income tax benefit", "expected_direction": "down", "horizon": "next quarter", "quote": "\"value\": \"-213100000\"", "paragraph_id": "0001596532-26-000175:facts:DeferredIncomeTaxExpenseBenefit:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_income_taxes_payable_change_tagged", "what_changed": "IncreaseDecreaseInIncomeTaxes prints 198400000 for 2026-01-01..2026-06-30 against 152400000 a year earlier. The prior 10-Q printed 352900000 for 2026-01-01..2026-03-31. No second-quarter-only figure exists in the input, and none is derived here.", "account": "change in income taxes payable (cash-flow reconciliation)", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"198400000\"", "paragraph_id": "0001596532-26-000175:facts:IncreaseDecreaseInIncomeTaxes:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_year_to_date_tagged", "what_changed": "NetCashProvidedByUsedInOperatingActivities prints 2776500000 for 2026-01-01..2026-06-30 against 1841800000 for 2025-01-01..2025-06-30. The prior 10-Q printed 1693500000 for 2026-01-01..2026-03-31. No operating cash flow for 2026-04-01..2026-06-30 alone exists in the input, and none is derived here.", "account": "operating cash flow", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"2776500000\"", "paragraph_id": "0001596532-26-000175:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_tagged", "what_changed": "PaymentsForRepurchaseOfCommonStock prints 0 for 2026-01-01..2026-06-30 against 983000000.0 for 2025-01-01..2025-06-30. The 10-K printed 1603100000 of stock repurchased in 2025. The remaining authorization prints 817900000 at 2026-06-30, the same figure the 10-K printed.", "account": "share repurchases", "expected_direction": "down", "horizon": "next quarter", "quote": "\"value\": \"0\"", "paragraph_id": "0001596532-26-000175:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_unrealized_losses_on_securities_tagged", "what_changed": "Gross unrealized losses on available-for-sale debt securities print 40800000 at 2026-06-30 against 1500000 at 2025-12-31; gross unrealized gains print 2300000 against 27500000. Accumulated other comprehensive income prints -40500000 against 12000000.0. Other comprehensive income for the quarter prints -21200000 against 5700000 a year earlier. The prior 10-Q printed 19500000 of unrealized losses at 2026-03-31.", "account": "unrealized losses on marketable securities / accumulated other comprehensive income", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"40800000\"", "paragraph_id": "0001596532-26-000175:facts:AvailableForSaleDebtSecuritiesAccumulatedGrossUnrealizedLossBeforeTax:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_securities_sold_before_maturity_tagged", "what_changed": "Proceeds from sales of available-for-sale debt securities print 494400000 for 2026-01-01..2026-06-30 against 15900000 a year earlier. The reclassification out of other comprehensive income for sales prints 100000 for the quarter and 300000 for the six months.", "account": "sales of marketable securities", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"494400000\"", "paragraph_id": "0001596532-26-000175:facts:ProceedsFromSaleOfAvailableForSaleSecuritiesDebt:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_current_assets_build_tagged", "what_changed": "IncreaseDecreaseInOtherCurrentAssets prints 619700000 for the six months against 403200000 a year earlier. Prepaid expenses and other current assets print 2018600000 at 2026-06-30 against 1510000000 at 2025-12-31; other prepaid expense prints 396700000 against 313000000.0.", "account": "prepaid expenses and other current assets", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"619700000\"", "paragraph_id": "0001596532-26-000175:facts:IncreaseDecreaseInOtherCurrentAssets:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accounts_payable_change_tagged", "what_changed": "IncreaseDecreaseInAccountsPayable prints 40900000 for 2026-01-01..2026-06-30 against 160000000.0 a year earlier.", "account": "change in accounts payable (cash-flow reconciliation)", "expected_direction": "down", "horizon": "next quarter", "quote": "\"value\": \"40900000\"", "paragraph_id": "0001596532-26-000175:facts:IncreaseDecreaseInAccountsPayable:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_operating_liabilities_change_tagged", "what_changed": "IncreaseDecreaseInOtherOperatingLiabilities prints 30800000 for 2026-01-01..2026-06-30 against -49700000 a year earlier.", "account": "change in other operating liabilities (cash-flow reconciliation)", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"30800000\"", "paragraph_id": "0001596532-26-000175:facts:IncreaseDecreaseInOtherOperatingLiabilities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_current_liabilities_tagged", "what_changed": "OtherLiabilitiesCurrent prints 538400000 at 2026-06-30. The release prints other current liabilities of 538.4 at June 30, 2026 against 246.8 at December 31, 2025 (millions).", "account": "other current liabilities", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"538400000\"", "paragraph_id": "0001596532-26-000175:facts:OtherLiabilitiesCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_growth_tagged", "what_changed": "Purchases of property and equipment print 84200000 for 2026-01-01..2026-06-30 against 52400000 a year earlier. Property and equipment, net prints 312500000 at 2026-06-30 against 203100000 at 2025-12-31.", "account": "capital expenditure", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"84200000\"", "paragraph_id": "0001596532-26-000175:facts:PaymentsToAcquirePropertyPlantAndEquipment:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_construction_in_progress_tagged", "what_changed": "Construction in progress (gross property and equipment) prints 213500000 at 2026-06-30 against 107900000 at 2025-12-31. U.S. property and equipment, net prints 287900000 against 184800000.", "account": "construction in progress", "expected_direction": "up", "horizon": "next four quarters", "quote": "\"value\": \"213500000\"", "paragraph_id": "0001596532-26-000175:facts:PropertyPlantAndEquipmentGross:2026-06-30:us-gaap:PropertyPlantAndEquipmentByTypeAxis=us-gaap:ConstructionInProgressMember" }
```

```json
{ "id": "liquidity_and_capital_other_investing_outflow_tagged", "what_changed": "PaymentsForProceedsFromOtherInvestingActivities prints 35000000.0 for 2026-01-01..2026-06-30 against 0 a year earlier.", "account": "other investing cash flows", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"35000000.0\"", "paragraph_id": "0001596532-26-000175:facts:PaymentsForProceedsFromOtherInvestingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_financing_outflow_tagged", "what_changed": "ProceedsFromPaymentsForOtherFinancingActivities prints -3700000 for 2026-01-01..2026-06-30 against 0 a year earlier. The prior 10-Q printed -3700000 for 2026-01-01..2026-03-31.", "account": "other financing cash flows", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"-3700000\"", "paragraph_id": "0001596532-26-000175:facts:ProceedsFromPaymentsForOtherFinancingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_equity_adjustment_tagged", "what_changed": "StockholdersEquityOther prints -400000 for 2026-01-01..2026-06-30 and 0 for 2026-04-01..2026-06-30. The prior 10-Q printed -400000 for the first quarter.", "account": "other changes in stockholders' equity", "expected_direction": "none", "horizon": "none", "quote": "\"value\": \"-400000\"", "paragraph_id": "0001596532-26-000175:facts:StockholdersEquityOther:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_stock_based_compensation_tagged", "what_changed": "AllocatedShareBasedCompensationExpense prints 120400000 for the quarter against 85200000, and 241300000 for six months against 178200000. Unrecognized compensation cost prints 1500000000 at 2026-06-30. RSUs granted in the six months carry a weighted-average grant-date fair value of 139.92; RSUs nonvested at 2025-12-31 carried 69.81. Nonvested RSUs print 24600000 at 2026-06-30 against 28100000 at 2025-12-31.", "account": "stock-based compensation expense", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"120400000\"", "paragraph_id": "0001596532-26-000175:facts:AllocatedShareBasedCompensationExpense:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_intangible_amortization_schedule_tagged", "what_changed": "FiniteLivedIntangibleAssetsNet prints 258200000 at 2026-06-30 against 288800000 at 2025-12-31. Scheduled amortization prints 30700000 for the rest of 2026, 57400000 for the next twelve months, 54000000.0 for year two and 23600000 for year three.", "account": "finite-lived intangible assets, net", "expected_direction": "down", "horizon": "next four quarters", "quote": "\"value\": \"258200000\"", "paragraph_id": "0001596532-26-000175:facts:FiniteLivedIntangibleAssetsNet:2026-06-30" }
```

```json
{ "id": "revenue_recognition_regional_revenue_americas_tagged", "what_changed": "Americas revenue prints 2337900000 for 2026-04-01..2026-06-30 against 1724100000 a year earlier; six months 4628000000 against 3322600000. U.S. revenue for the quarter prints 2319600000 against 1712100000.", "account": "revenue, Americas", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"2337900000\"", "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_regional_revenue_europe_middle_east_africa_tagged", "what_changed": "EMEA revenue prints 438200000 for 2026-04-01..2026-06-30 against 281600000 a year earlier; six months 673200000 against 456200000.", "account": "revenue, EMEA", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"438200000\"", "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_regional_revenue_asia_pacific_tagged", "what_changed": "Asia-Pacific revenue prints 259600000 for 2026-04-01..2026-06-30 against 199100000 a year earlier; six months 443500000 against 430800000.", "account": "revenue, Asia-Pacific", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"259600000\"", "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "earnings_quality_interest_income_tagged", "what_changed": "InterestIncomeOther prints 122400000 for 2026-04-01..2026-06-30 against 90400000 a year earlier. Total non-operating income prints 126300000 against 94000000.0.", "account": "interest and other income", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"122400000\"", "paragraph_id": "0001596532-26-000175:facts:InterestIncomeOther:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_diluted_share_count_tagged", "what_changed": "WeightedAverageNumberOfDilutedSharesOutstanding prints 1276000000 for 2026-04-01..2026-06-30 against 1271200000 a year earlier. Antidilutive securities excluded print 0 against 3200000. Diluted EPS prints 0.95 against 0.70.", "account": "diluted weighted-average shares", "expected_direction": "up", "horizon": "next quarter", "quote": "\"value\": \"1276000000\"", "paragraph_id": "0001596532-26-000175:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2026-04-01..2026-06-30" }
```

### Earnings release (8-K) figures, and the release against the filing

```json
{ "id": "across_documents_quarterly_revenue_release_and_filing", "what_changed": "The 10-Q tags quarterly revenue of 3035700000. The release's income statement prints total revenue of 3,035.7 (millions) against 2,204.8. The release and the filing carry the same figure.", "account": "revenue", "expected_direction": "none", "horizon": "none", "quote": "\"value\": \"3035700000\"", "paragraph_id": "0001596532-26-000175:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "across_documents_quarterly_net_income_release_and_filing", "what_changed": "The 10-Q tags quarterly net income of 1212900000. The release prints net income of 1,212.9 (millions) against 888.8. The release and the filing carry the same figure.", "account": "net income", "expected_direction": "none", "horizon": "none", "quote": "\"value\": \"1212900000\"", "paragraph_id": "0001596532-26-000175:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "across_documents_deferred_revenue_release_and_filing", "what_changed": "The trend cell's contract-liability input (ContractWithCustomerLiabilityCurrent at 2026-06-30) is 5100700000.0. The release's balance sheet prints deferred revenue of 5,100.7 (millions) against 4,002.6 at December 31, 2025. The release and the filing carry the same figure.", "account": "deferred revenue, current", "expected_direction": "none", "horizon": "none", "quote": "\"value\": 5100700000.0", "paragraph_id": "0001596532-26-000175:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "across_documents_gross_margin_release_and_trend", "what_changed": "The release prints GAAP gross margin of 62.9% for the quarter against 65.2% a year earlier, and non-GAAP gross margin of 63.4% against 65.6%. The trend table prints gross_margin 0.6292782554270844 for quarters-back-0 and 0.6524854862119013 for quarters-back-4. Both documents show the year-over-year decline.", "account": "gross margin", "expected_direction": "down", "horizon": "next quarter", "quote": "| GAAP gross margin |  | 62.9 | % |  | 65.2 | % |", "paragraph_id": "0001596532-26-000174:8k_2_02:39" }
```

```json
{ "id": "across_documents_earnings_per_share_growth_wording_release", "what_changed": "The CFO quote gives EPS growth as 39.7% without saying whether it is GAAP or non-GAAP. The headline bullet gives 40% growth in non-GAAP EPS. The release prints non-GAAP diluted EPS of 1.02 against 0.73 and GAAP diluted EPS of 0.95 against 0.70. No growth rate is computed here.", "account": "diluted earnings per share", "expected_direction": "none", "horizon": "none", "quote": "revenue up 37.7% and EPS up 39.7%", "paragraph_id": "0001596532-26-000174:8k_2_02:15" }
```

```json
{ "id": "results_against_expectations_reported_revenue_growth_release", "what_changed": "The release reports quarterly revenue of $3.036 billion, up 12.1% on the prior quarter and 37.7% on the year-earlier quarter, and calls it the company's first $3+ billion revenue quarter.", "account": "revenue", "expected_direction": "up", "horizon": "next quarter", "quote": "Revenue of $3.036 billion, an increase of 12.1% compared to the first quarter of 2026, and an increase of 37.7% from the second quarter of 2025.", "paragraph_id": "0001596532-26-000174:8k_2_02:11" }
```

```json
{ "id": "results_against_expectations_reported_operating_margin_release", "what_changed": "GAAP operating margin is 45.4% against 44.7% a year earlier; non-GAAP operating margin is 49.9% against 48.8%.", "account": "operating margin", "expected_direction": "up", "horizon": "next quarter", "quote": "GAAP and non-GAAP operating margin of 45.4% and 49.9%, respectively, compared to GAAP and non-GAAP operating margin of 44.7% and 48.8% in the second quarter of 2025.", "paragraph_id": "0001596532-26-000174:8k_2_02:12" }
```

```json
{ "id": "results_against_expectations_reported_diluted_earnings_per_share_release", "what_changed": "GAAP diluted EPS is $0.95 against $0.70; non-GAAP diluted EPS is $1.02 against $0.73.", "account": "diluted earnings per share", "expected_direction": "up", "horizon": "next quarter", "quote": "GAAP and non-GAAP diluted earnings per share of $0.95 and $1.02, respectively, compared to GAAP and non-GAAP diluted earnings per share of $0.70 and $0.73 in the second quarter of 2025.", "paragraph_id": "0001596532-26-000174:8k_2_02:13" }
```

```json
{ "id": "results_against_expectations_third_quarter_revenue_outlook_release", "what_changed": "The third-quarter 2026 outlook is revenue of approximately $3.3 billion, against $3.036 billion reported for the second quarter.", "account": "revenue", "expected_direction": "up", "horizon": "third quarter of 2026", "quote": "Revenue of approximately $3.3 billion;", "paragraph_id": "0001596532-26-000174:8k_2_02:24" }
```

```json
{ "id": "results_against_expectations_third_quarter_operating_margin_outlook_release", "what_changed": "The third-quarter 2026 outlook is a non-GAAP operating margin of 48 - 49%, against 49.9% reported for the second quarter.", "account": "non-GAAP operating margin", "expected_direction": "down", "horizon": "third quarter of 2026", "quote": "Non-GAAP operating margin of 48 - 49%; and", "paragraph_id": "0001596532-26-000174:8k_2_02:25" }
```

```json
{ "id": "results_against_expectations_third_quarter_earnings_per_share_outlook_release", "what_changed": "The third-quarter 2026 outlook is non-GAAP diluted EPS between $1.06 and $1.08, against $1.02 reported for the second quarter.", "account": "non-GAAP diluted earnings per share", "expected_direction": "up", "horizon": "third quarter of 2026", "quote": "Non-GAAP diluted net income per share between $1.06 and $1.08.", "paragraph_id": "0001596532-26-000174:8k_2_02:26" }
```

```json
{ "id": "results_against_expectations_outlook_without_gaap_reconciliation_release", "what_changed": "The outlook is given only in non-GAAP terms. The release says a GAAP reconciliation of the guidance is not available. The exclusions it names include tax benefits on stock-based awards, which it says depend on the timing of employee stock transactions and the future share price.", "account": "guidance basis", "expected_direction": "none", "horizon": "third quarter of 2026", "quote": "A reconciliation of non-GAAP guidance measures to corresponding GAAP measures is not available on a forward-looking basis without unreasonable effort", "paragraph_id": "0001596532-26-000174:8k_2_02:27" }
```

```json
{ "id": "earnings_quality_non_gaap_tax_methodology_prior_period_recast_release", "what_changed": "Prior-period non-GAAP figures were restated (recast) under a new tax methodology for stock-based awards. Non-GAAP net income rose by $10.7 million for the three months and $30.4 million for the six months ended June 30, 2025. The effect on non-GAAP diluted EPS was nil and $0.03. The reconciliation prints recast non-GAAP net income of 934.2 for the year-earlier quarter, against 1,301.7 for the current quarter.", "account": "non-GAAP net income (prior periods)", "expected_direction": "up", "horizon": "none", "quote": "The retrospective application of this change resulted in an increase to non-GAAP net income of $10.7 million and $30.4 million for the three and six months ended June 30, 2025, respectively.", "paragraph_id": "0001596532-26-000174:8k_2_02:40" }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_tax_methodology_release", "what_changed": "From the fourth quarter of 2025 the company changed how it computes the tax effect of non-GAAP adjustments. It still excludes direct excess tax benefits on stock-based awards but no longer excludes their discrete indirect effects. The reconciliation shows tax benefits on stock-based awards of (30.9) against (32.1) and an income tax effect on non-GAAP exclusions of (10.0) against (7.3).", "account": "non-GAAP income tax adjustments", "expected_direction": "none", "horizon": "none", "quote": "Effective the fourth quarter of fiscal year 2025, the company updated its methodology for calculating the income tax effect of non-GAAP adjustments.", "paragraph_id": "0001596532-26-000174:8k_2_02:53" }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_prior_periods_recast_release", "what_changed": "The release states that every prior-period non-GAAP result it presents has been recast to the current presentation, so the year-earlier non-GAAP comparatives are not the figures originally reported.", "account": "non-GAAP comparatives", "expected_direction": "none", "horizon": "none", "quote": "All prior period non-GAAP results presented in this release have been recast to conform to the current period presentation.", "paragraph_id": "0001596532-26-000174:8k_2_02:55" }
```

## Seen in the notes

No items. In `input_numbers.json` every fact prints `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and sometimes `superseded_by`. None prints whether its element sat inside a note when it was extracted. The input does not mark which tables came from notes, and this report does not judge that itself. So nothing is placed under this heading, and every numeric fact item above stays under "Seen in the statements". This marker is missing from the run's input and should be restored before the split into a separate notes reader.
