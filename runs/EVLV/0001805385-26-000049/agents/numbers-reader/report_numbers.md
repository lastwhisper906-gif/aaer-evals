# report_numbers — EVLV, 10-Q 0001805385-26-000049 (period ended 2026-06-30, filed 2026-08-11)

## What my input holds, and what it does not

- My directory holds four files: `input_trends.json`, `input_numbers.json`, `input_8k.md`, `input_prior_predictions.md`. Nothing in them is a price, a return, short interest, another company's file, a prior probability, or an outcome window.
- `input_prior_predictions.md` says no prior predictions are on record: "None on record. This company has no earlier run under the given run root". There are no earlier flags to carry forward.
- **Articulation checks.** None are in my input. No articulation file is in the directory, and the numbers file holds only `documents` and `facts`. So there are no articulation gaps to report. This means the checks are missing from my input, not that they came back clean.
- **Restatement traces.** None are in my input. Some numeric facts carry a `superseded_by` field naming a later filing that reports the same element and period. That field does not say whether the value changed. Where I could set an earlier printed value beside a later one, they are the same:
  - The 31 December 2025 balance sheet: the 10-K and Q1 10-Q facts, the Q2 10-Q facts I read, and the release's December 31, 2025 column.
  - The Q1 10-Q's `NetIncomeLoss` for 2026-01-01..2026-03-31 (-5009000) and for 2025-01-01..2025-03-31 (-1689000), against the Q2 10-Q values the trend table uses.
  - The Q1 10-Q's `RestructuringCharges` for 2025-01-01..2025-03-31 (2662000), against the release's six-month 2,662.
  
  No Python-computed restated value exists in my input. The restated items below are the company's own statements that it recast prior figures.
- **Fourth-quarter derivation.** None is in my input. Nothing in front of me holds a derived fourth quarter.
- **A period the record does not reach:** `quarters-back-2` (target end 2025-12-30) has no cells. The reason it gives: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". As a result, the comparison from the quarter before (quarters-back-1) to this one is missing, and so is every quarter-over-quarter change against it.
- **Formula baselines without a quotable id.** `years-back-0` also carries a `research_and_development_capitalized` block that prints no `paragraph_id`, so I cannot write an item for it. As printed:
  - `book_value_with_rnd_capitalized` 183188000.0
  - `earnings_with_rnd_capitalized` -31212400.0
  - `research_and_development_asset` 63766000.0
  - `research_and_development_amortization` 18693400.0
  - `capitalized_development_cost` and `capitalized_over_expense` are missing, because the record "tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
  - For years-back-1 through years-back-4, the earnings and amortization baselines are missing because the record does not reach five years back. The asset and book-value baselines are filled for years-back-1 (61840400.0 and 179491400.0) and missing for years-back-2 through years-back-4, for the same reason.
- **Prose and lists without paragraph ids.** The 8-K item-code list and the late-filing list print no paragraph ids, so they cannot be quoted. They show:
  - Item 4.02 filings on 2024-10-25, 2023-10-25 and 2021-05-12.
  - NT 10-K / NT 10-Q notices for the periods ended 2024-12-31, 2025-03-31, 2024-09-30, 2022-06-30 and 2021-03-31.
- **How the item fields are used.**
  - `expected_direction` is the sign of the printed year-over-year change for the cell: against quarters-back-4 for the latest quarter, and against years-back-1 for the latest year. For release items it is the direction the quoted figures show. It is `none` where no value exists or where the item records only a definition or tag change.
  - Values and changes are copied exactly as Python printed them. I computed nothing.
- **Coverage of the numbers file.** `input_numbers.json` is 53,496 lines covering three documents: 10-K 0001805385-26-000012, 10-Q 0001805385-26-000028 and 10-Q 0001805385-26-000049. It is too large to hold in context at once. I read:
  - lines 1–3,599 (the 10-K balance sheet, income statement and the start of its equity statement)
  - lines 18,000–18,059 (10-K tax facts)
  - lines 21,500–22,999 (the Q1 10-Q balance sheet and income statement)
  - lines 30,000–30,119 (Q1 10-Q depreciation facts)
  - lines 35,000–35,059 (Q2 10-Q balance sheet)
  - lines 53,000–53,496 (Q2 10-Q segment and restructuring facts)
  
  Every fact in those lines prints the same fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and sometimes superseded_by. None of them marks whether the element sat inside a note, including facts that plainly belong to note tables, such as tax-credit carryforwards and depreciation by asset type.

## Seen in the statements

### Trend table — latest quarter (quarters-back-0, 2026-04-01..2026-06-30, 7 filled quarters on record)

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "receivables_over_revenue = 0.9045094050693667 (AccountsReceivableNetCurrent 39575000.0 / Revenues 43753000.0). Change against quarters-back-1: -0.017460030261318815; against quarters-back-4: -0.3799669961105743. Position in its own filed history: lowest of the 7 filled quarters.",
  "account": "AccountsReceivableNetCurrent / Revenues",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "days_sales_outstanding = 82.31035586131237 (receivables 39575000.0, revenue 43753000.0, 91 days). Change against quarters-back-1: -0.6668933184493255; against quarters-back-4: -34.576996646062256. Position: lowest of the 7 filled quarters.",
  "account": "AccountsReceivableNetCurrent / Revenues",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "contract_liabilities_over_revenue = 1.7019175827943227 (ContractWithCustomerLiabilityCurrent 74464000.0 / Revenues 43753000.0). Change against quarters-back-1: 0.07624844102260808; against quarters-back-4: -0.5155111291034158. Position: second lowest of the 7 filled quarters.",
  "account": "ContractWithCustomerLiabilityCurrent / Revenues",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "bad_debt_reserve_ratio = 0.01738050900062073 (AllowanceForDoubtfulAccountsReceivableCurrent 700000.0 against receivables 39575000.0). Change against quarters-back-1: 0.0035278550630038503; against quarters-back-4: -0.0036957871915950895. Position: third lowest of the 7 filled quarters.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "gross_margin = 0.5017255959591342 (Revenues 43753000.0, CostOfRevenue 21801000.0). Change against quarters-back-1: -0.007663974063314427; against quarters-back-4: 0.0033848879945324595. Position: third lowest of the 7 filled quarters.",
  "account": "Revenues, CostOfRevenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "days_sales_of_inventory = 36.14788312462731 (InventoryNet 8660000.0, CostOfRevenue 21801000.0, 91 days). Change against quarters-back-1: 3.456607661562508; against quarters-back-4: -31.530788932214534. Position: second lowest of the 7 filled quarters.",
  "account": "InventoryNet / CostOfRevenue",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "soft_asset_share = 0.39852925108352677 (Assets 302023000.0, PropertyPlantAndEquipmentNet 128962000.0, CashAndCashEquivalentsAtCarryingValue 52696000.0). Change against quarters-back-1: 0.002260224465135796; against quarters-back-4: -0.022272255217690662. Position: third lowest of the 7 filled quarters.",
  "account": "Assets less PropertyPlantAndEquipmentNet and CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 7 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient: accruals_over_total_assets cannot be filled for the latest quarter because no discrete-quarter operating cash flow is in the record. With no value there is no change and no position. The release prints only a six-month operating cash flow.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001805385-26-000049:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio is unfilled because the record tags no inventory valuation reserve in any period. No value, change or position exists.",
  "account": "InventoryValuationReserves (untagged)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period",
  "paragraph_id": "0001805385-26-000049:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is unfilled because the record tags no warranty accrual concept in any period. No value, change or position exists.",
  "account": "StandardProductWarrantyAccrual / ProductWarrantyAccrual (untagged)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period",
  "paragraph_id": "0001805385-26-000049:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient: non_gaap_gap is unfilled because no us-gaap concept carries a non-GAAP measure. The release prints an adjusted loss, but the trend table holds no gap figure computed from it, so none exists here.",
  "account": "non-GAAP net income (not in companyfacts)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001805385-26-000049:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_two_filled_quarters_only",
  "what_changed": "insufficient for a trend claim: only 2 quarters of accruals_over_total_assets are filled on record. The one before the latest quarter (quarters-back-1) is -0.006007110054851808. Its change against quarters-back-5 is -0.009327656030740738, and it has no change against quarters-back-2, which is not filled. Two points do not make a trend.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0001805385-26-000049:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

### Trend table — latest year (years-back-0, 2025-01-01..2025-12-31, 5 filled years on record)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "accruals_over_total_assets = -0.17018879205279738 (NetIncomeLoss -33138000.0, operating cash flow 18669000.0, Assets 304409000.0). Change against years-back-1: -0.08377498016810035. Position: second lowest of the 5 filled years.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "bad_debt_reserve_ratio = 0.01908336248847047 (AllowanceForDoubtfulAccountsReceivableCurrent 600000.0, receivables 30841000.0). Change against years-back-1: -0.006117488984440332. Position: second lowest of the 4 filled years on the same concepts. The table sets aside one filled year that rests on a different allowance concept and does not compare it.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "contract_liabilities_over_revenue = 0.5135122168534321 (ContractWithCustomerLiabilityCurrent 74924000.0, Revenues 145905000.0). Change against years-back-1: -0.10754396184006432. Position: third highest of the 5 filled years.",
  "account": "ContractWithCustomerLiabilityCurrent / Revenues",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "days_sales_of_inventory = 48.16657932382477 (InventoryNet 9317000.0, CostOfRevenue 70603000.0, 365 days). Change against years-back-1: -91.65410846754065. Position: lowest of the 5 filled years.",
  "account": "InventoryNet / CostOfRevenue",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "days_sales_outstanding = 77.15270210068195 (receivables 30841000.0, Revenues 145905000.0, 365 days). Change against years-back-1: -22.895167730348717. Position: lowest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / Revenues",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "gross_margin = 0.5161029436962407 (Revenues 145905000.0, CostOfRevenue 70603000.0). Change against years-back-1: -0.056390196437586915. Position: second highest of the 5 filled years.",
  "account": "Revenues, CostOfRevenue",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "receivables_over_revenue = 0.21137726602926563 (receivables 30841000.0, Revenues 145905000.0). Change against years-back-1: -0.061977569574643315. Position: lowest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / Revenues",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "soft_asset_share = 0.4196229415030436 (Assets 304409000.0, PropertyPlantAndEquipmentNet 127522000.0, cash 49150000.0). Change against years-back-1: 0.019028296294339497. Position: highest of the 5 filled years.",
  "account": "Assets less PropertyPlantAndEquipmentNet and CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001805385-26-000049:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio is unfilled for the latest year, and for every year on record, because no inventory valuation reserve is tagged. No value, change or position exists.",
  "account": "InventoryValuationReserves (untagged)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period",
  "paragraph_id": "0001805385-26-000049:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is unfilled for the latest year, and for every year on record, because no warranty accrual concept is tagged. No value, change or position exists.",
  "account": "StandardProductWarrantyAccrual / ProductWarrantyAccrual (untagged)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period",
  "paragraph_id": "0001805385-26-000049:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient: non_gaap_gap is unfilled for the latest year because companyfacts carries no non-GAAP measure. No value, change or position exists.",
  "account": "non-GAAP net income (not in companyfacts)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001805385-26-000049:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

### Changes of tag — periods the input says rest on a different concept

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_tag_change_seen_from_following_year",
  "what_changed": "The trend table refuses a year-over-year change for bad_debt_reserve_ratio between years-back-2 and years-back-3. The allowance input is AllowanceForDoubtfulAccountsReceivableCurrent in one year and AllowanceForDoubtfulAccountsReceivable in the other.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent / AllowanceForDoubtfulAccountsReceivable",
  "expected_direction": "none",
  "horizon": "not applicable — record of a tag change",
  "quote": "bad_debt_allowance: us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent in years-back-2 and us-gaap:AllowanceForDoubtfulAccountsReceivable in years-back-3",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2023-01-01..2023-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_tag_change_seen_from_odd_year",
  "what_changed": "The year on the different concept (years-back-3) rests on AllowanceForDoubtfulAccountsReceivable (value 200000.0, filing 0001628280-25-020355). The trend table refuses its change against years-back-4, which rests on AllowanceForDoubtfulAccountsReceivableCurrent.",
  "account": "AllowanceForDoubtfulAccountsReceivable",
  "expected_direction": "none",
  "horizon": "not applicable — record of a tag change",
  "quote": "bad_debt_allowance: us-gaap:AllowanceForDoubtfulAccountsReceivable in years-back-3 and us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent in years-back-4",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2022-01-01..2022-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_odd_year_stands_alone",
  "what_changed": "Because of the tag change, the years-back-3 bad_debt_reserve_ratio (0.00750778933143136) is ranked only against itself. Its place in the history is therefore not established.",
  "account": "AllowanceForDoubtfulAccountsReceivable",
  "expected_direction": "none",
  "horizon": "not applicable — record of a tag change",
  "quote": "\"position_in_history\": \"the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared\"",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2022-01-01..2022-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_odd_year_left_out_of_highest_ranking",
  "what_changed": "The years-back-2 bad_debt_reserve_ratio (0.026300329883862803) is ranked among the 4 years on the same concept. The year on the different concept is left out.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "none",
  "horizon": "not applicable — record of a tag change",
  "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2023-01-01..2023-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_odd_year_left_out_of_second_highest_ranking",
  "what_changed": "The years-back-1 bad_debt_reserve_ratio (0.0252008514729108; change against years-back-2: -0.0010994784109520025) is ranked among the 4 years on the same concept. The year on the different concept is left out.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "none",
  "horizon": "not applicable — record of a tag change",
  "quote": "\"position_in_history\": \"second highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2024-01-01..2024-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_odd_year_left_out_of_lowest_ranking",
  "what_changed": "The years-back-4 bad_debt_reserve_ratio (0.015204500532157519; its allowance comes from filing 0001558370-22-008811) is ranked among the 4 years on the same concept. The year on the different concept is left out.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "none",
  "horizon": "not applicable — record of a tag change",
  "quote": "\"position_in_history\": \"lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001805385-26-000049:trends:bad_debt_reserve_ratio:2021-01-01..2021-12-31" }
```

### Prior figures the company says it recast (earnings release)

```json
{ "id": "articulation_and_the_filed_history_recurring_revenue_prior_quarters_reclassified_in_release",
  "what_changed": "In the key-operating-statistics table, the release reclassifies prior quarters' recurring and non-recurring revenue: short-term rental subscription revenue moves out of recurring and into non-recurring. Earlier releases therefore printed these periods differently. My input has no Python trace of the earlier figures.",
  "account": "Recurring revenue / non-recurring revenue (key operating statistic)",
  "expected_direction": "down",
  "horizon": "prior periods as previously reported",
  "quote": "*Certain prior quarter amounts have been reclassified to reflect an update to the definition of non-recurring revenue to include short term rental subscription revenue, applied consistently to all prior periods, which were previously classified as recurring revenue.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:59" }
```

```json
{ "id": "articulation_and_the_filed_history_adjusted_gross_profit_definition_revised_in_release",
  "what_changed": "The definition of adjusted gross profit and adjusted gross margin changed: losses on disposals of leased equipment are no longer excluded as non-recurring, and the prior-year adjusted figures were adjusted to match.",
  "account": "Adjusted gross profit / adjusted gross margin (non-GAAP)",
  "expected_direction": "none",
  "horizon": "prior year as previously reported",
  "quote": "*As previously disclosed, management revised its definition of non-recurring expenses to exclude losses on disposals of leased equipment, and have adjusted prior year adjusted gross profit and adjusted gross margin accordingly.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:70" }
```

```json
{ "id": "articulation_and_the_filed_history_adjusted_operating_loss_definition_revised_in_release",
  "what_changed": "The same definition change was applied to adjusted loss from operations, and the prior-year figure was recast.",
  "account": "Adjusted loss from operations (non-GAAP)",
  "expected_direction": "none",
  "horizon": "prior year as previously reported",
  "quote": "*As previously disclosed, management revised its definition of non-recurring expenses to exclude losses on disposals of leased equipment, and have adjusted prior year adjusted loss from operations accordingly.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:72" }
```

```json
{ "id": "articulation_and_the_filed_history_adjusted_ebitda_calculation_refined_in_release",
  "what_changed": "The comparative-quarter loss on disposal of leased equipment in the adjusted EBITDA reconciliation reflects a calculation refinement made later and applied to all prior quarters. Earlier releases printed those quarters' adjusted EBITDA on the earlier calculation.",
  "account": "Adjusted EBITDA (non-GAAP)",
  "expected_direction": "none",
  "horizon": "prior quarters as previously reported",
  "quote": "*Q2 2025 figure reflects refinements of our adjusted EBITDA calculation in Q3 2025, applied consistently to all prior quarters.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:78" }
```

### Earnings-release figures

```json
{ "id": "revenue_recognition_purchase_subscription_mix_raised_in_release",
  "what_changed": "Management raised its expected share of new unit deployments under the purchase subscription model. The quoted share and the prior expectation are both printed in the release.",
  "account": "Product revenue / subscription revenue mix",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "The Company now expects approximately 60% of new unit deployments in 2026 to be delivered under its purchase subscription model (compared to its prior expectation of approximately 55%), with the remaining 40% deployed through its pure subscription model.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:21" }
```

```json
{ "id": "revenue_recognition_purchase_subscription_front_loads_revenue_in_release",
  "what_changed": "Management states that a higher purchase-subscription mix pulls revenue recognition into the early years of a contract and recognizes hardware cost upfront. This bears on the timing of revenue and gross margin.",
  "account": "Revenues, CostOfRevenue (product)",
  "expected_direction": "up",
  "horizon": "early years of a typical four-year contract",
  "quote": "a higher purchase subscription mix increases revenue recognition in the early years of a typical four year customer contract and creates a modest near-term headwind to reported gross margin percentage as associated hardware costs are recognized upfront.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:21" }
```

```json
{ "id": "results_against_expectations_revenue_outlook_raised_in_release",
  "what_changed": "The full-year revenue outlook was raised. The guidance table in the same release shows the previous range, issued May 12, 2026, as $175-$180 million.",
  "account": "Revenues (guidance)",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "The Company expects total revenues in 2026 to be between $180 to $185 million, reflecting growth of approximately 23% to 27% year-over-year.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:21" }
```

```json
{ "id": "revenue_recognition_product_revenue_rise_in_release",
  "what_changed": "Product revenue for the three months ended June 30 is 9,108 (thousands) against 2,528 a year earlier. For the six months it is 22,529 against 4,850.",
  "account": "Revenues — ProductMember",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Product revenue | $ | 9,108 |  |  | $ | 2,528 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:42" }
```

```json
{ "id": "earnings_quality_product_cost_above_product_revenue_in_release",
  "what_changed": "Cost of product revenue for the three months is 10,097 (thousands), above that quarter's product revenue of 9,108. A year earlier it was 5,351 against product revenue of 2,528.",
  "account": "CostOfRevenue — ProductMember",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Cost of product revenue | 10,097 |  |  | 5,351 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:42" }
```

```json
{ "id": "revenue_recognition_license_fee_revenue_decline_in_release",
  "what_changed": "License fee and other revenue for the three months is 898 (thousands) against 3,130 a year earlier. For the six months it is 2,068 against 6,848.",
  "account": "Revenues — LicenseFeeAndOtherRevenueMember",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| License fee and other revenue | 898 |  |  | 3,130 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:42" }
```

```json
{ "id": "earnings_quality_warrant_fair_value_gain_in_release",
  "what_changed": "Other income for the three months includes a gain of 1,735 (thousands) from the change in fair value of the public warrant liability, against a 5,303 charge a year earlier. Non-operating fair-value items move the net loss away from the operating loss of (10,551).",
  "account": "Change in fair value of public warrant liability",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Change in fair value of public warrant liability | 1,735 |  |  | (5,303) |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:42" }
```

```json
{ "id": "revenue_recognition_contract_assets_rise_in_release",
  "what_changed": "The current portion of contract assets is 2,525 (thousands) at June 30, 2026, against 878 at December 31, 2025. The cash flow statement shows a (1,639) contract-asset change for the six months.",
  "account": "ContractWithCustomerAssetNetCurrent",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Current portion of contract assets | 2,525 |  |  | 878 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:47" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_build_slows_in_release",
  "what_changed": "The deferred-revenue change in operating cash flow for the six months is 605 (thousands), against 6,205 a year earlier. On the balance sheet, current deferred revenue is 74,464 at June 30, 2026 against 74,924 at December 31, 2025.",
  "account": "ContractWithCustomerLiability (deferred revenue)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Deferred revenue | 605 |  |  | 6,205 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:52" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_charge_in_release",
  "what_changed": "The release prints the inventory write-off and reserve change that the trend table could not tag: 147 (thousands) for the six months, against 1,794 a year earlier. It is a cash-flow add-back, not a reserve balance, so it does not fill the missing inventory_reserve_ratio.",
  "account": "Inventory write-off and change in inventory reserve",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Write-off of inventory and change in inventory reserve | 147 |  |  | 1,794 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:52" }
```

```json
{ "id": "estimates_and_discretion_credit_loss_allowance_change_in_release",
  "what_changed": "The change in the allowance for expected credit losses is 100 (thousands) for the six months, against 166 a year earlier.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Change in allowance for expected credit losses | 100 |  |  | 166 |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:52" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_turns_positive_in_release",
  "what_changed": "Net cash from operating activities for the six months is 8,723 (thousands), against (426) a year earlier. There is no discrete-quarter figure, which is why the quarterly accruals ratio is unfilled.",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Net cash provided by (used in) operating activities | 8,723 |  |  | (426) |",
  "paragraph_id": "0001805385-26-000047:8k_2_02:52" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_in_release",
  "what_changed": "The release reports remaining performance obligation and its sequential change.",
  "account": "Remaining performance obligation",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "Remaining Performance Obligation of $312.6 million, up $13.6 million sequentially",
  "paragraph_id": "0001805385-26-000047:8k_2_02:12" }
```

```json
{ "id": "controls_audit_and_filings_legal_costs_excluded_net_of_insurance_in_release",
  "what_changed": "The non-GAAP adjustment for legal and regulatory costs covers the internal investigation, the restatement and the resolution of the SEC investigation, net of estimated insurance recoveries. In the operating-expense reconciliation this adjustment is a positive 36 and 2,225 in the September and December 2025 quarters, and 99 in the March 2026 quarter.",
  "account": "Other non-recurring legal and regulatory costs (non-GAAP adjustment)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "Other non-recurring legal and regulatory costs include non-recurring legal, accounting and professional fees related to the internal investigation, subsequent restatement, certain non-recurring regulatory, litigation and legal matters, as well as fees related to the resolution of the Securities and Exchange Commission investigation, net of estimated insurance recoveries.",
  "paragraph_id": "0001805385-26-000047:8k_2_02:30" }
```

### Numeric facts

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_revenue_falls_to_zero",
  "what_changed": "The 10-K tags related-party revenue for the year ended 2025-12-31 as 0. The same 10-K tags 6100000 for the year ended 2024-12-31 (paragraph 0001805385-26-000012:facts:Revenues:2024-01-01..2024-12-31:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember). Related-party receivables are 0 at both year ends.",
  "account": "Revenues — RelatedPartyMember",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001805385-26-000012:facts:Revenues:2025-01-01..2025-12-31:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_appears",
  "what_changed": "The 10-K tags non-current long-term debt at 2025-12-31 as 28596000. The same 10-K tags 0 at 2024-12-31 (paragraph 0001805385-26-000012:facts:LongTermDebtNoncurrent:2024-12-31). Interest expense for 2025 is tagged 1732000, against 0 for 2024. The Q1 10-Q tags interest expense for the three months ended 2026-03-31 as 962000. The release balance sheet shows 28,737 (thousands) at June 30, 2026.",
  "account": "LongTermDebtNoncurrent",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"value\": \"28596000\"",
  "paragraph_id": "0001805385-26-000012:facts:LongTermDebtNoncurrent:2025-12-31" }
```

```json
{ "id": "earnings_quality_nonoperating_income_narrows_annual_net_loss",
  "what_changed": "The 10-K tags non-operating income for 2025 as 15387000, against an operating loss of -48463000 and a net loss of -33138000. For 2024 the corresponding non-operating figure is tagged 28290000 (paragraph 0001805385-26-000012:facts:NonoperatingIncomeExpense:2024-01-01..2024-12-31). In both years non-operating income narrows the net loss relative to the operating loss.",
  "account": "NonoperatingIncomeExpense",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"value\": \"15387000\"",
  "paragraph_id": "0001805385-26-000012:facts:NonoperatingIncomeExpense:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_nonoperating_income_behind_small_comparative_ten_q_loss",
  "what_changed": "The Q1 10-Q tags non-operating income for the three months ended 2025-03-31 as 12763000, against an operating loss of -14389000 and a net loss of -1689000. For the three months ended 2026-03-31 it tags 3426000 (paragraph 0001805385-26-000028:facts:NonoperatingIncomeExpense:2026-01-01..2026-03-31), against an operating loss of -8472000 and a net loss of -5009000. The trend table's accruals ratio for quarters-back-5 uses that -1689000 net loss.",
  "account": "NonoperatingIncomeExpense",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"12763000\"",
  "paragraph_id": "0001805385-26-000028:facts:NonoperatingIncomeExpense:2025-01-01..2025-03-31" }
```

```json
{ "id": "estimates_and_discretion_restructuring_charge_annual",
  "what_changed": "The 10-K tags restructuring charges for 2025 as 2662000, against 860000 for 2024 (paragraph 0001805385-26-000012:facts:RestructuringCharges:2024-01-01..2024-12-31). The Q1 10-Q tags the same 2662000 for the three months ended 2025-03-31 and 0 for the three months ended 2026-03-31. Impairment of long-lived assets held for use is tagged 0 for 2025 and 224000 for 2024.",
  "account": "RestructuringCharges",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"value\": \"2662000\"",
  "paragraph_id": "0001805385-26-000012:facts:RestructuringCharges:2025-01-01..2025-12-31" }
```

## Seen in the notes

No items. My instructions say each fact is marked with whether its element sat inside a note when it was extracted. No fact I read carries such a marker. Every fact prints the same fields, and none of them says statement or note, not even facts that plainly come from note tables, such as tax-credit carryforwards by jurisdiction and depreciation by asset type. Without that marker I cannot tell which findings came from a table inside a note. Deciding it myself would mean judging something the input does not state, so I have written no items under this heading. If the marker exists in the parts of the numbers file I could not read, this heading is incomplete.
