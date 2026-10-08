# TTMI numbers report: filing 0001193125-26-335107 (10-Q, period ending 2026-06-29)

This part sits outside the items. It records what the input holds, what it does not hold, and how much of it I read.

**What I read.** `input_trends.json`, `input_8k.md` and `input_prior_predictions.md` were read in full. `input_numbers.json` (59,059 lines, 2.1MB) is too large to read whole in one working context. These ranges were read in full:
- lines 1 to 6,099: the document list; the 10-K's balance sheet, income statement, comprehensive income and equity statement; the start of the 10-K's cash flow statement.
- lines 39,240 to 47,199: the end of the Q1 10-Q facts, then the current 10-Q's cover facts, balance sheet, income statement, comprehensive income, equity statement, cash flow statement and supplemental cash flow facts, then its first note rows (derivatives, contract balances, segment revenue).
- lines 57,800 to 59,059: the current 10-Q's last note rows (derivative and debt fair values, supplier finance, lines of credit).

I spot-checked 30 to 45 lines at about 12,000, 20,000, 25,000, 30,000, 38,600, 45,500, 50,000 and 53,500. The rest of lines 6,100 to 39,239 was not read; that is mostly the 10-K's notes and the Q1 10-Q. Lines 47,200 to 57,799 were not read either; that is most of the current 10-Q's notes. A finding that sits only in those unread ranges is missing from this report.

**What the numbers file holds.** It holds four top-level keys: `ticker`, `cutoff`, `documents` and `facts`. It has no articulation checks, no restatement traces and no fourth-quarter derivation. So I report no articulation gap and no restated prior value.

No trend cell says a period rests on a different concept. Each filled metric uses the same tags in every period it fills, so no tag change comes from the trend table. The one member rename I saw is in a note row; it is itemized under the notes heading as a printed difference, not as a Python finding.

Facts from the 10-K (0001193125-26-051976) and the Q1 10-Q (0001193125-26-201403) carry a `superseded_by` field naming 0001193125-26-335107. That field says a later filing printed the same context. It does not say the value differs. For every 2025-12-29 balance I read in both the 10-K and the current 10-Q, the two print the same value, as does stockholders' equity at 2024-12-30.

**No note marker.** Every fact I read has the same fields: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, sometimes `superseded_by`, and once a `typed_segment` inside a context. None carries a marker saying whether its element sat inside a note. The items under the notes heading are therefore placed there by me, from where the rows sit after the cash flow statement in the 10-Q's extraction order. Each of those items says so.

**Periods the record does not reach.** `quarters-back-2` (target 2025-12-29) and `quarters-back-6` (target 2024-12-30) have no cells. The reason each gives: "no quarter ending within 20 days of 2025-12-29 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration" (the same wording, with 2024-12-30, for quarters-back-6). The table says these quarters are derived by src/fourth_quarter.py, but no fourth-quarter derivation is in my directory.

**8-K.** The bundle's first line says no 8-K filed at or before 2026-08-05 is on record. Its index nonetheless lists 8-Ks through 2026-06-18. Either way it holds:
- no earnings release for this quarter (the latest item 2.02 in the index is dated 2026-04-29);
- no item text;
- no [id] paragraph.

Nothing in it is quotable and no item comes from it. The index lists a 2026-06-03 8-K with items 1.01, 1.02, 2.03 and 3.03, and a 2026-06-18 8-K with items 8.01 and 9.01, as item codes only.

**Prior predictions.** There are none on record.

**R&D capitalisation block.** Each year in the trend table carries a `research_and_development_capitalized` block with no `paragraph_id`, so none of it is itemized. For years-back-0 it prints:
- book_value_with_rnd_capitalized 1846636600.0
- earnings_with_rnd_capitalized 182071800.0
- research_and_development_asset 84383600.0
- research_and_development_amortization 24368200.0

capitalized_development_cost is missing because no us-gaap:CapitalizedComputerSoftwareAdditions fact is tagged in any period. Parts of the block are missing in years-back-3 and years-back-4, where R&D expense before 2018 is not in the record.

**Market-derived figure.** The facts include dei:EntityPublicFloat from the 10-K cover. It is a cover-page figure, not a price series, and I make no use of it.

**Conventions.**
- `expected_direction` for a trend cell is the sign the table's printed changes share. For a quarter, both quarter_over_quarter and year_over_year must agree; for a year, year_over_year alone is used (an annual period has no preceding quarter). It is `none` where the quarterly signs disagree or the cell is insufficient. It says which way the printed change points; it is not a forecast I computed.
- Fact items carry no Python-computed change, so their direction is `none`.
- `horizon` is the next quarter for quarterly cells and facts, and the next fiscal year for annual cells.
- All values are copied as printed. None is derived.

## Seen in the statements

**Trend table, quarters-back-0 (2026-03-31..2026-06-29)**

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_quarterly", "what_changed": "receivables_over_revenue in quarters-back-0 (2026-03-31..2026-06-29) is 0.7172353279803676. Its quarter_over_quarter change against quarters-back-1 is -0.013378779275630248 and its year_over_year change against quarters-back-4 is 0.03924769827905872. It is the third highest of the 6 filled quarters.", "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-335107:trends:receivables_over_revenue:2026-03-31..2026-06-29" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_quarterly", "what_changed": "days_sales_outstanding in quarters-back-0 (2026-03-31..2026-06-29) is 65.26841484621345. Its quarter_over_quarter change against quarters-back-1 is -1.2174689140823602 and its year_over_year change against quarters-back-4 is 3.5715405433943346. It is the third highest of the 6 filled quarters.", "account": "AccountsReceivableNetCurrent against RevenueFromContractWithCustomerExcludingAssessedTax (days)", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-335107:trends:days_sales_outstanding:2026-03-31..2026-06-29" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_quarterly", "what_changed": "contract_liabilities_over_revenue in quarters-back-0 (2026-03-31..2026-06-29) is 0.1860158915755527. Its quarter_over_quarter change against quarters-back-1 is -0.020289015419444778 and its year_over_year change against quarters-back-4 is -0.03589122579446541. It is the lowest of the 6 filled quarters.", "account": "ContractWithCustomerLiabilityCurrent over RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "down", "horizon": "next quarter", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-335107:trends:contract_liabilities_over_revenue:2026-03-31..2026-06-29" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_quarterly", "what_changed": "days_sales_of_inventory in quarters-back-0 (2026-03-31..2026-06-29) is 35.37691682361436. Its quarter_over_quarter change against quarters-back-1 is -2.9794336302849658 and its year_over_year change against quarters-back-4 is -3.731031167156644. It is the lowest of the 6 filled quarters.", "account": "InventoryNet against CostOfGoodsAndServicesSold (days)", "expected_direction": "down", "horizon": "next quarter", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-335107:trends:days_sales_of_inventory:2026-03-31..2026-06-29" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_quarterly", "what_changed": "gross_margin in quarters-back-0 (2026-03-31..2026-06-29) is 0.21100259547793246. Its quarter_over_quarter change against quarters-back-1 is -0.0031654187446932547 and its year_over_year change against quarters-back-4 is 0.00828600233319668. It is the second highest of the 6 filled quarters.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax less CostOfGoodsAndServicesSold, over revenue", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-335107:trends:gross_margin:2026-03-31..2026-06-29" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_quarterly", "what_changed": "soft_asset_share in quarters-back-0 (2026-03-31..2026-06-29) is 0.6159814879105484. Its quarter_over_quarter change against quarters-back-1 is -0.012933139710946562 and its year_over_year change against quarters-back-4 is -0.001904813653808457. It is the third lowest of the 6 filled quarters.", "account": "Assets less PropertyPlantAndEquipmentNet less CashAndCashEquivalentsAtCarryingValue, over Assets", "expected_direction": "down", "horizon": "next quarter", "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-335107:trends:soft_asset_share:2026-03-31..2026-06-29" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly_insufficient", "what_changed": "insufficient: accruals_over_total_assets is not filled in quarters-back-0, because the record has no operating cash flow for the three months 2026-03-31..2026-06-29. The 10-Q prints operating cash flow only for the six months 2025-12-30..2026-06-29 (see earnings_quality_operating_cash_flow_year_to_date_only_fact). The three-month figure does not exist in my input and I do not derive it. In the quarterly table this ratio is filled only in quarters-back-1 and quarters-back-5, each printed as one of 2 filled quarters, which supports no trend claim.", "account": "NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities, over Assets", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for operating_cash_flow in 2026-03-31..2026-06-29: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0001193125-26-335107:trends:accruals_over_total_assets:2026-03-31..2026-06-29" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly_insufficient", "what_changed": "insufficient: bad_debt_reserve_ratio is not filled in quarters-back-0. The allowance concepts are in the record, but none is tagged for 2026-06-29. No quarter in the table holds this ratio; it is filled only in the five annual periods.", "account": "AllowanceForDoubtfulAccountsReceivable against AccountsReceivableNetCurrent", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-29: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0001193125-26-335107:trends:bad_debt_reserve_ratio:2026-03-31..2026-06-29" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_quarterly_insufficient", "what_changed": "insufficient: inventory_reserve_ratio is not filled in quarters-back-0 or in any other period. The companyfacts record tags no us-gaap:InventoryValuationReserves fact in any period.", "account": "InventoryValuationReserves against InventoryNet", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001193125-26-335107:trends:inventory_reserve_ratio:2026-03-31..2026-06-29" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_quarterly_insufficient", "what_changed": "insufficient: warranty_reserve_ratio is not filled in quarters-back-0 or in any other period. The companyfacts record tags none of the standard product warranty accrual concepts in any period.", "account": "StandardProductWarrantyAccrual / ProductWarrantyAccrual / StandardProductWarrantyAccrualCurrent", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001193125-26-335107:trends:warranty_reserve_ratio:2026-03-31..2026-06-29" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_quarterly_insufficient", "what_changed": "insufficient: non_gaap_gap is not filled in quarters-back-0 or in any other period. No us-gaap concept carries a non-GAAP measure, and this bundle holds no earnings release that would state one.", "account": "non-GAAP net income against NetIncomeLoss", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001193125-26-335107:trends:non_gaap_gap:2026-03-31..2026-06-29" }
```

**Trend table, years-back-0 (2024-12-31..2025-12-29)**

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_annual", "what_changed": "receivables_over_revenue in years-back-0 (2024-12-31..2025-12-29) is 0.1939690573555445. Its year_over_year change against years-back-1 is 0.010319298251779213. It is the highest of the 5 filled years.", "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "up", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:receivables_over_revenue:2024-12-31..2025-12-29" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_annual", "what_changed": "days_sales_outstanding in years-back-0 (2024-12-31..2025-12-29) is 70.6047368774182. Its year_over_year change against years-back-1 is 3.756224563647635. It is the highest of the 5 filled years.", "account": "AccountsReceivableNetCurrent against RevenueFromContractWithCustomerExcludingAssessedTax (days)", "expected_direction": "up", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:days_sales_outstanding:2024-12-31..2025-12-29" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_annual", "what_changed": "contract_liabilities_over_revenue in years-back-0 (2024-12-31..2025-12-29) is 0.060428820391247424. Its year_over_year change against years-back-1 is -0.009539367141425746. It is the second highest of the 5 filled years.", "account": "ContractWithCustomerLiabilityCurrent over RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:contract_liabilities_over_revenue:2024-12-31..2025-12-29" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_annual", "what_changed": "days_sales_of_inventory in years-back-0 (2024-12-31..2025-12-29) is 39.49423667449284. Its year_over_year change against years-back-1 is -2.1743583743985155. It is the third highest of the 5 filled years.", "account": "InventoryNet against CostOfGoodsAndServicesSold (days)", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:days_sales_of_inventory:2024-12-31..2025-12-29" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_annual", "what_changed": "gross_margin in years-back-0 (2024-12-31..2025-12-29) is 0.20702497466749473. Its year_over_year change against years-back-1 is 0.011599976724599975. It is the highest of the 5 filled years.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax less CostOfGoodsAndServicesSold, over revenue", "expected_direction": "up", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:gross_margin:2024-12-31..2025-12-29" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_annual", "what_changed": "soft_asset_share in years-back-0 (2024-12-31..2025-12-29) is 0.6062985195807341. Its year_over_year change against years-back-1 is 0.0019475833372157858. It is the third highest of the 5 filled years.", "account": "Assets less PropertyPlantAndEquipmentNet less CashAndCashEquivalentsAtCarryingValue, over Assets", "expected_direction": "up", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:soft_asset_share:2024-12-31..2025-12-29" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_annual", "what_changed": "accruals_over_total_assets in years-back-0 (2024-12-31..2025-12-29) is -0.02979795231192311. Its year_over_year change against years-back-1 is 0.022209336973529937. It is the highest of the 5 filled years. The inputs as printed are net_income 177448000.0, operating_cash_flow 291882000.0 and assets 3840331000.0.", "account": "NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities, over Assets", "expected_direction": "up", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:accruals_over_total_assets:2024-12-31..2025-12-29" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_annual", "what_changed": "bad_debt_reserve_ratio in years-back-0 (2024-12-31..2025-12-29) is 0.0027825244023675336. Its year_over_year change against years-back-1 is -0.004405558605827501. It is the lowest of the 5 filled years. As printed, the allowance input is 1573000.0 at 2025-12-29 against 3248000.0 at 2024-12-30.", "account": "AllowanceForDoubtfulAccountsReceivable against AccountsReceivableNetCurrent", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-335107:trends:bad_debt_reserve_ratio:2024-12-31..2025-12-29" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_annual_insufficient", "what_changed": "insufficient: inventory_reserve_ratio is not filled in years-back-0 or in any other year. The companyfacts record tags no us-gaap:InventoryValuationReserves fact in any period.", "account": "InventoryValuationReserves against InventoryNet", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001193125-26-335107:trends:inventory_reserve_ratio:2024-12-31..2025-12-29" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_annual_insufficient", "what_changed": "insufficient: warranty_reserve_ratio is not filled in years-back-0 or in any other year. The companyfacts record tags none of the standard product warranty accrual concepts in any period.", "account": "StandardProductWarrantyAccrual / ProductWarrantyAccrual / StandardProductWarrantyAccrualCurrent", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001193125-26-335107:trends:warranty_reserve_ratio:2024-12-31..2025-12-29" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_annual_insufficient", "what_changed": "insufficient: non_gaap_gap is not filled in years-back-0 or in any other year. No us-gaap concept carries a non-GAAP measure.", "account": "non-GAAP net income against NetIncomeLoss", "expected_direction": "none", "horizon": "none (insufficient)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001193125-26-335107:trends:non_gaap_gap:2024-12-31..2025-12-29" }
```

**Numeric facts: face statements of the current 10-Q (0001193125-26-335107), read in full**

```json
{ "id": "earnings_quality_operating_cash_flow_year_to_date_only_fact", "what_changed": "The 10-Q prints NetCashProvidedByUsedInOperatingActivities only for the six months 2025-12-30..2026-06-29: 118172000. The same six months a year earlier (2024-12-31..2025-06-30) print 87149000. No three-month operating cash flow for 2026-03-31..2026-06-29 exists in my input, so the quarter's accruals cannot be read from it, and I do not derive them.", "account": "NetCashProvidedByUsedInOperatingActivities", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"118172000\"", "paragraph_id": "0001193125-26-335107:facts:NetCashProvidedByUsedInOperatingActivities:2025-12-30..2026-06-29" }
```

```json
{ "id": "earnings_quality_income_tax_benefit_fact", "what_changed": "IncomeTaxExpenseBenefit for 2026-03-31..2026-06-29 prints -1800000, a benefit, against pretax income of 81247000 for the same quarter. For 2025-04-01..2025-06-30 the 10-Q prints tax expense of 3995000 against pretax income of 45525000. Six-month tax prints 6737000 (2025-12-30..2026-06-29) against 12808000 (2024-12-31..2025-06-30). The rows do not say what produced the benefit.", "account": "IncomeTaxExpenseBenefit", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"-1800000\"", "paragraph_id": "0001193125-26-335107:facts:IncomeTaxExpenseBenefit:2026-03-31..2026-06-29" }
```

```json
{ "id": "earnings_quality_unrealized_derivative_loss_fact", "what_changed": "UnrealizedGainLossOnDerivatives prints -13994000 for 2026-03-31..2026-06-29 and 0 for 2025-04-01..2025-06-30. It is printed among the quarter's non-operating lines and appears again, at -13994000, in the six-month cash flow statement. NonoperatingIncomeExpense prints -27808000 for the quarter against -16244000 a year earlier.", "account": "UnrealizedGainLossOnDerivatives", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"-13994000\"", "paragraph_id": "0001193125-26-335107:facts:UnrealizedGainLossOnDerivatives:2026-03-31..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_debt_extinguishment_loss_fact", "what_changed": "GainsLossesOnExtinguishmentOfDebt prints -747000 for 2026-03-31..2026-06-29 and 0 for 2025-04-01..2025-06-30. The six-month figure is also -747000.", "account": "GainsLossesOnExtinguishmentOfDebt", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"-747000\"", "paragraph_id": "0001193125-26-335107:facts:GainsLossesOnExtinguishmentOfDebt:2026-03-31..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_debt_proceeds_fact", "what_changed": "ProceedsFromIssuanceOfLongTermDebt prints 199159000 for 2025-12-30..2026-06-29 against 0 for 2024-12-31..2025-06-30. PaymentsOfDebtIssuanceCosts prints 4737000 against 0.", "account": "ProceedsFromIssuanceOfLongTermDebt", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"199159000\"", "paragraph_id": "0001193125-26-335107:facts:ProceedsFromIssuanceOfLongTermDebt:2025-12-30..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_debt_repayments_fact", "what_changed": "RepaymentsOfLongTermDebt prints 143310000 for 2025-12-30..2026-06-29 against 1895000 for 2024-12-31..2025-06-30. NetCashProvidedByUsedInFinancingActivities prints 45554000 against -19770000.", "account": "RepaymentsOfLongTermDebt", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"143310000\"", "paragraph_id": "0001193125-26-335107:facts:RepaymentsOfLongTermDebt:2025-12-30..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_noncurrent_fact", "what_changed": "LongTermDebtNoncurrent prints 969456000 at 2026-06-29 against 912336000 at 2025-12-29. LongTermDebtCurrent prints 4000000 against 3815000.", "account": "LongTermDebtNoncurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"969456000\"", "paragraph_id": "0001193125-26-335107:facts:LongTermDebtNoncurrent:2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_paid_fact", "what_changed": "PaymentsToAcquirePropertyPlantAndEquipment prints 169205000 for 2025-12-30..2026-06-29 against 123726000 for 2024-12-31..2025-06-30. ProceedsFromSaleOfPropertyPlantAndEquipment prints 11988000 against 272000. NetCashProvidedByUsedInInvestingActivities prints -157217000 against -123454000.", "account": "PaymentsToAcquirePropertyPlantAndEquipment", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"169205000\"", "paragraph_id": "0001193125-26-335107:facts:PaymentsToAcquirePropertyPlantAndEquipment:2025-12-30..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_unpaid_fact", "what_changed": "CapitalExpendituresIncurredButNotYetPaid prints 140132000 for 2025-12-30..2026-06-29 against 59126000 for 2024-12-31..2025-06-30. This is a supplemental cash flow line, not part of the investing total.", "account": "CapitalExpendituresIncurredButNotYetPaid", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"140132000\"", "paragraph_id": "0001193125-26-335107:facts:CapitalExpendituresIncurredButNotYetPaid:2025-12-30..2026-06-29" }
```

```json
{ "id": "revenue_recognition_contract_assets_fact", "what_changed": "ContractWithCustomerAssetNetCurrent prints 596036000 at 2026-06-29 against 468006000 at 2025-12-29. The cash flow statement prints IncreaseDecreaseInContractWithCustomerAsset of 128030000 for 2025-12-30..2026-06-29 against 43591000 a year earlier. No trend-table metric covers contract assets; receivables_over_revenue and days_sales_outstanding use AccountsReceivableNetCurrent only.", "account": "ContractWithCustomerAssetNetCurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"596036000\"", "paragraph_id": "0001193125-26-335107:facts:ContractWithCustomerAssetNetCurrent:2026-06-29" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_change_fact", "what_changed": "IncreaseDecreaseInAccountsReceivable prints 156402000 for 2025-12-30..2026-06-29 against 46741000 for 2024-12-31..2025-06-30. AccountsReceivableNetCurrent prints 720143000 at 2026-06-29 against 563741000 at 2025-12-29.", "account": "AccountsReceivableNetCurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"156402000\"", "paragraph_id": "0001193125-26-335107:facts:IncreaseDecreaseInAccountsReceivable:2025-12-30..2026-06-29" }
```

```json
{ "id": "earnings_quality_accounts_payable_fact", "what_changed": "AccountsPayableCurrent prints 812987000 at 2026-06-29 against 543538000 at 2025-12-29. IncreaseDecreaseInAccountsPayable prints 192182000 for 2025-12-30..2026-06-29 against 47458000 a year earlier.", "account": "AccountsPayableCurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"812987000\"", "paragraph_id": "0001193125-26-335107:facts:AccountsPayableCurrent:2026-06-29" }
```

```json
{ "id": "earnings_quality_inventory_cash_flow_change_fact", "what_changed": "IncreaseDecreaseInInventories prints 57915000 for 2025-12-30..2026-06-29 against 25354000 a year earlier. InventoryNet prints 307972000 at 2026-06-29 against 250057000 at 2025-12-29.", "account": "InventoryNet", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"57915000\"", "paragraph_id": "0001193125-26-335107:facts:IncreaseDecreaseInInventories:2025-12-30..2026-06-29" }
```

```json
{ "id": "earnings_quality_prepaid_and_other_current_assets_fact", "what_changed": "PrepaidExpenseAndOtherAssetsCurrent prints 117843000 at 2026-06-29 against 72368000 at 2025-12-29. IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets prints 44185000 for 2025-12-30..2026-06-29 against 7876000 a year earlier.", "account": "PrepaidExpenseAndOtherAssetsCurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"117843000\"", "paragraph_id": "0001193125-26-335107:facts:PrepaidExpenseAndOtherAssetsCurrent:2026-06-29" }
```

```json
{ "id": "earnings_quality_share_based_compensation_fact", "what_changed": "ShareBasedCompensation prints 37648000 for 2025-12-30..2026-06-29 against 17975000 for 2024-12-31..2025-06-30. The quarter's equity statement prints 13292000 of share-based compensation for 2026-03-31..2026-06-29.", "account": "ShareBasedCompensation", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"37648000\"", "paragraph_id": "0001193125-26-335107:facts:ShareBasedCompensation:2025-12-30..2026-06-29" }
```

```json
{ "id": "earnings_quality_net_income_reported_fact", "what_changed": "NetIncomeLoss prints 83047000 for 2026-03-31..2026-06-29 against 41530000 for 2025-04-01..2025-06-30. OperatingIncomeLoss prints 109055000 against 61769000, and EarningsPerShareDiluted prints 0.77 against 0.4. Revenue prints 1004054000 against 730621000. My input holds no expectation to set these against.", "account": "NetIncomeLoss", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"83047000\"", "paragraph_id": "0001193125-26-335107:facts:NetIncomeLoss:2026-03-31..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_fact", "what_changed": "PaymentsForRepurchaseOfCommonStock prints 0 for 2025-12-30..2026-06-29 against 17875000 for 2024-12-31..2025-06-30.", "account": "PaymentsForRepurchaseOfCommonStock", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"0\"", "paragraph_id": "0001193125-26-335107:facts:PaymentsForRepurchaseOfCommonStock:2025-12-30..2026-06-29" }
```

```json
{ "id": "estimates_and_discretion_employee_related_liabilities_fact", "what_changed": "EmployeeRelatedLiabilitiesCurrent prints 120967000 at 2026-06-29 against 132967000 at 2025-12-29. IncreaseDecreaseInEmployeeRelatedLiabilities prints -12000000 for 2025-12-30..2026-06-29 against -6232000 a year earlier.", "account": "EmployeeRelatedLiabilitiesCurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"120967000\"", "paragraph_id": "0001193125-26-335107:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-29" }
```

```json
{ "id": "estimates_and_discretion_other_liabilities_fact", "what_changed": "OtherLiabilitiesCurrent prints 139243000 at 2026-06-29 against 106250000 at 2025-12-29, and OtherLiabilitiesNoncurrent prints 143315000 against 116021000. IncreaseDecreaseInOtherOperatingLiabilities prints 34342000 for 2025-12-30..2026-06-29 against 3810000 a year earlier.", "account": "OtherLiabilitiesCurrent", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"139243000\"", "paragraph_id": "0001193125-26-335107:facts:OtherLiabilitiesCurrent:2026-06-29" }
```

```json
{ "id": "earnings_quality_restructuring_charges_fact", "what_changed": "RestructuringCharges prints 340000 for 2026-03-31..2026-06-29 against 1408000 for 2025-04-01..2025-06-30, and 636000 for the six months against 2122000.", "account": "RestructuringCharges", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"340000\"", "paragraph_id": "0001193125-26-335107:facts:RestructuringCharges:2026-03-31..2026-06-29" }
```

## Seen in the notes

No fact in my input is marked as sitting inside a note. I placed each item below here myself: each row comes after the cash flow statement in the current 10-Q's extraction order, and its concept or dimensions do not appear on the face statements I read. Treat the placement as mine, not the extractor's.

```json
{ "id": "estimates_and_discretion_loss_on_contracts_note", "what_changed": "LossOnContracts prints 20954000 for 2025-12-30..2026-06-29. The same 10-Q prints 33163000 for 2024-12-31..2025-12-29. The rows do not say whether the amount is a charge or an accrued balance. I found no row for 2024-12-31..2025-06-30 in the part of the file I read. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "LossOnContracts", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"20954000\"", "paragraph_id": "0001193125-26-335107:facts:LossOnContracts:2025-12-30..2026-06-29" }
```

```json
{ "id": "liquidity_and_capital_derivative_notional_usd_chf_note", "what_changed": "At 2026-06-18, DerivativeNotionalAmount prints 381083000 in USD and 306200000 in CHF, and DerivativeFixedInterestRate prints 0.06 and, for CHF, 0.03025. At 2026-06-29, DerivativeFairValueOfDerivativeNet prints 13994000; undimensioned DerivativeLiabilitiesNoncurrent prints 20819000 and DerivativeAssetsCurrent 6825000. ChangeInUnrealizedGainLossOnFairValueHedgingInstruments1 prints -13994000 for the quarter. This matches the -13994000 income statement line in earnings_quality_unrealized_derivative_loss_fact. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "DerivativeNotionalAmount", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"381083000\"", "paragraph_id": "0001193125-26-335107:facts:DerivativeNotionalAmount:2026-06-18" }
```

```json
{ "id": "liquidity_and_capital_term_loan_carrying_amount_note", "what_changed": "The term loan due 2030 (ttmi:TermLoanDueTwoThousandThirtyMember) has a carrying amount of 395675000 at 2026-06-29 against 336778000 at 2025-12-29. Its fair value prints 401000000 against 345806000. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "LongTermDebt (term loan due 2030)", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"395675000\"", "paragraph_id": "0001193125-26-335107:facts:LongTermDebt:2026-06-29:us-gaap:FairValueByMeasurementBasisAxis=us-gaap:CarryingReportedAmountFairValueDisclosureMember,us-gaap:LongtermDebtTypeAxis=ttmi:TermLoanDueTwoThousandThirtyMember" }
```

```json
{ "id": "liquidity_and_capital_revolving_credit_facility_note", "what_changed": "Carrying amounts at 2026-06-29 against 2025-12-29: the revolving credit facility due May 2031 prints 80000000 against 0; the Asia asset-based lending revolving loan due June 2028 prints 0 against 80000000; the other loan prints 0 against 1981000; the senior notes due 2029 print 497781000 against 497392000. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "LongTermDebt (revolving credit facility due May 2031)", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"80000000\"", "paragraph_id": "0001193125-26-335107:facts:LongTermDebt:2026-06-29:us-gaap:FairValueByMeasurementBasisAxis=us-gaap:CarryingReportedAmountFairValueDisclosureMember,us-gaap:LongtermDebtTypeAxis=ttmi:RevolvingCreditFacilityDueMayTwoThousandThirtyOneMember" }
```

```json
{ "id": "structure_and_disclosure_changes_asset_based_lending_member_renamed_note", "what_changed": "The same balance at 2025-12-29 is printed under two different members. The Q1 10-Q (0001193125-26-201403) prints 80000000 under ttmi:AssetBackedLendingRevolvingLoansMember, and that row carries no superseded_by field. The current 10-Q prints 80000000 under ttmi:AsiaAssetBasedLendingRevolvingLoanDueJuneTwoThousandTwentyEightMember. Same value, different member. This is a printed difference I observed, not a tag change flagged by Python. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "LongTermDebt (asset-based lending revolving loan)", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"80000000\"", "paragraph_id": "0001193125-26-335107:facts:LongTermDebt:2025-12-29:us-gaap:FairValueByMeasurementBasisAxis=us-gaap:CarryingReportedAmountFairValueDisclosureMember,us-gaap:LongtermDebtTypeAxis=ttmi:AsiaAssetBasedLendingRevolvingLoanDueJuneTwoThousandTwentyEightMember" }
```

```json
{ "id": "liquidity_and_capital_supplier_finance_obligation_note", "what_changed": "SupplierFinanceProgramObligation prints 15307000 at 2026-06-29 against 12535000 at 2025-12-29. The Q1 10-Q prints 16375000 at 2026-03-30. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "SupplierFinanceProgramObligation", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"15307000\"", "paragraph_id": "0001193125-26-335107:facts:SupplierFinanceProgramObligation:2026-06-29" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_note", "what_changed": "RevenueRemainingPerformanceObligation prints 425149000 at 2026-06-29, with an expected-timing start date of 2026-06-30 on its typed axis. RevenueRemainingPerformanceObligationPercentage prints 0.61 at 2026-06-29; the row does not print the timing that percentage refers to. I read no earlier figure for the same row. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "RevenueRemainingPerformanceObligation", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"425149000\"", "paragraph_id": "0001193125-26-335107:facts:RevenueRemainingPerformanceObligation:2026-06-29:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized_note", "what_changed": "ContractWithCustomerLiabilityRevenueRecognized prints 68944000 for 2025-12-30..2026-06-29 against 54970000 for 2024-12-31..2025-06-30. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "ContractWithCustomerLiabilityRevenueRecognized", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"68944000\"", "paragraph_id": "0001193125-26-335107:facts:ContractWithCustomerLiabilityRevenueRecognized:2025-12-30..2026-06-29" }
```

```json
{ "id": "revenue_recognition_aerospace_defense_segment_revenue_note", "what_changed": "Revenue for aerospace and defense components in the Aerospace and Defense segment prints 371165000 for 2026-03-31..2026-06-29 against 325092000 for 2025-04-01..2025-06-30. Automotive components in the Commercial segment print 79465000 for the current quarter. I did not read the remaining segment rows. [Placed here by the reader; the input marks no fact as sitting in a note.]", "account": "RevenueFromContractWithCustomerExcludingAssessedTax (Aerospace and Defense segment)", "expected_direction": "none", "horizon": "next quarter", "quote": "\"value\": \"371165000\"", "paragraph_id": "0001193125-26-335107:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-03-31..2026-06-29:srt:ProductOrServiceAxis=ttmi:AerospaceAndDefenseComponentsMember,us-gaap:StatementBusinessSegmentsAxis=ttmi:AerospaceAndDefenseMember" }
```
