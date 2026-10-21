OMCL, triggering filing 0000926326-26-000022 (10-Q for the period ended 2026-06-30, filed 2026-08-05). Inputs: input_trends.json (read in full), input_8k.md (read in full), input_prior_predictions.md (read in full; no earlier run on record), input_numbers.json (see coverage below). Nothing in the directory holds prices, returns, short interest, another company's files, a prior probability or an outcome window.

Coverage of input_numbers.json (60529 lines, top-level keys `ticker`, `cutoff`, `documents`, `facts` only). I read lines 1–15650 (10-K 0000926326-26-000006 facts through the debt note), the 10-Q 0000926326-26-000012 facts at lines 33000–33040 and 40200–40998, the start of the 0000926326-26-000022 facts at lines 40998–47540 (balance sheet, income statement, equity statement, start of the cash flow statement), and lines 60000–60529. I did not read lines 15650–33000, 33040–40200 or 47540–60000. Facts in those ranges are not reported here; that includes most 0000926326-26-000012 facts and the later 0000926326-26-000022 notes and cash-flow lines.

Things the input does not hold, stated once here and not as items:

- Two quarters the record does not reach have no cells at all: quarters-back-2 (target end 2025-12-30) and quarters-back-6 (target end 2024-12-31). The reason the period gives: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py" (the same wording with 2024-12-31 for quarters-back-6). No fourth-quarter derivation is present in my input, so neither fourth quarter has a value anywhere I can read.
- There is no articulation-check section and no restatement-trace section in my input, so no articulation gap and no Python-traced restatement exists for me to report.
- No restated prior value in what I read. Every 2025-12-31 balance-sheet value in 0000926326-26-000022 that I read prints the same value as the 10-K fact it supersedes. This covers cash 196520000, allowance 8868000, receivables 216858000, inventory 100905000, other current assets 132077000, assets 1974720000, accrued liabilities 203586000, current contract liabilities 171861000, convertible notes 167596000 and equity 1231814000; the 2024-12-31 equity components also match. One 10-K fact is marked superseded by 0000926326-26-000012, and its superseding value is in a range I did not read: PropertyPlantAndEquipmentGross for SoftwareDevelopmentMember at 2025-12-31, "165885000". Whether that value changed is unchecked.
- No change of tag. Every filled trend cell, in every period, rests on the same concepts (RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold, ReceivablesNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent, InventoryNet, ContractWithCustomerLiabilityCurrent, Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet, NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities). The one concept mismatch my input shows is in the R&D baseline (item below).
- The research-and-development capitalisation baseline in years-back-0 prints values (book_value_with_rnd_capitalized 1508215400.0, earnings_with_rnd_capitalized 3049400.0, research_and_development_amortization 87674600.0, research_and_development_asset 276401400.0) but no paragraph_id, so none of it is an item. Its capitalized_development_cost and capitalized_over_expense are insufficient for every year: "no row for capitalized_development_cost in 2025-01-01..2025-12-31: us-gaap:CapitalizedComputerSoftwareAdditions is in the record, but not for this period".
- The 8-K's list of item codes and the late-filing list print no ids, so they are not items: the list shows Item 2.05 (costs of exit or disposal) on 2024-05-02, 2023-11-02, 2023-02-28, 2022-11-30 and 2017-02-15, no Item 4.01 or 4.02 on or before 2026-08-05, and one NT 10-K (filed 2015-03-02, period ended 2014-12-31).

`expected_direction` is the direction my input gives a reason to expect the named account to move over the horizon; "none" means the input gives no such reason, which is the case for most rows. Where a value sits in its history describes it; it does not decide whether it is reported.

## Seen in the statements

**Trend table, quarters-back-0 (2026-04-01..2026-06-30)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_trend_cell",
  "what_changed": "insufficient. accruals_over_total_assets has no value for 2026-04-01..2026-06-30 (quarters-back-0) because the record has no quarterly operating-cash-flow row; quarter_over_quarter and year_over_year are not filled. The ratio is filled in only 2 of the 6 filled quarters, which supports no trend claim. The 8-K prints a three-month operating cash flow figure (item below), but the table does not use it and I do not compute the ratio.",
  "account": "total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000926326-26-000022:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend_cell",
  "what_changed": "bad_debt_reserve_ratio for quarters-back-0 is 0.02972975282896311 (allowance 6957000.0 over receivables 227051000.0 plus allowance). Change against quarters-back-1: 0.0013546964289195482. Change against quarters-back-4: -0.011816085172750457. Position in history: third highest of the 6 filled quarters.",
  "account": "allowance for doubtful accounts relative to gross current receivables",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend_cell",
  "what_changed": "contract_liabilities_over_revenue for quarters-back-0 is 0.6033605801260697 (current contract liabilities 188374000.0 over quarterly revenue 312208000.0). Change against quarters-back-1: -0.08041701119960476. Change against quarters-back-4: 0.07474018241404956. Position in history: second highest of the 6 filled quarters.",
  "account": "current contract liabilities (deferred revenues) relative to quarterly revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend_cell",
  "what_changed": "days_sales_of_inventory for quarters-back-0 is 55.25944761510112 (inventory 96718000.0, quarterly cost of revenue 159273000.0, 91 days). Change against quarters-back-1: 2.5900398270916583. Change against quarters-back-4: -3.839935995321021. Position in history: third highest of the 6 filled quarters. The cost-of-revenue input for this quarter is the one the 8-K says the IEEPA tariff refund reduced (item below).",
  "account": "inventory relative to cost of revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend_cell",
  "what_changed": "days_sales_outstanding for quarters-back-0 is 66.1790889407062 (receivables 227051000.0, quarterly revenue 312208000.0, 91 days). Change against quarters-back-1: -6.370704527733196. Change against quarters-back-4: -6.69369552525977. Position in history: lowest of the 6 filled quarters. The 10-K reports receivables sold and derecognised (item below), which bears on what this ratio measures.",
  "account": "current receivables (net) relative to revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend_cell",
  "what_changed": "gross_margin for quarters-back-0 is 0.48984971557423257 (revenue 312208000.0, cost of revenue 159273000.0). Change against quarters-back-1: 0.03689050555745188. Change against quarters-back-4: 0.05043231068302173. Position in history: highest of the 6 filled quarters. The 8-K says $15 million of IEEPA tariff refunds received in the quarter mainly reduced cost of product revenues, and it guides next-quarter non-GAAP EBITDA to $32 million - $37 million against $67 million reported for this quarter (items below). The share of the margin due to the refund is not in my input.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend_cell",
  "what_changed": "insufficient. inventory_reserve_ratio has no value for quarters-back-0, or for any quarter or year in the table, because the company tags no InventoryValuationReserves fact in companyfacts. The 10-K's inventory write-down fact is an item below.",
  "account": "inventory valuation reserve relative to inventory",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000926326-26-000022:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend_cell",
  "what_changed": "insufficient. non_gaap_gap has no value for quarters-back-0 or for any period, because companyfacts holds no non-GAAP measure. The 8-K prints GAAP and non-GAAP net income for the quarter (item below). I do not compute the gap.",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000926326-26-000022:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend_cell",
  "what_changed": "receivables_over_revenue for quarters-back-0 is 0.727242735612156 (receivables 227051000.0 over quarterly revenue 312208000.0). Change against quarters-back-1: -0.07886608070383727. Change against quarters-back-4: -0.07355709368417318. Position in history: lowest of the 6 filled quarters.",
  "account": "current receivables (net) relative to revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_quarterly_trend_cell",
  "what_changed": "soft_asset_share for quarters-back-0 is 0.7928253068375508 (assets 1998859000.0, PP&E 121948000.0, cash 292165000.0). Change against quarters-back-1: -0.027183804452415194. Change against quarters-back-4: 0.034241743875885966. Position in history: third highest of the 6 filled quarters.",
  "account": "assets other than PP&E and cash, relative to total assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend_cell",
  "what_changed": "insufficient. warranty_reserve_ratio has no value for quarters-back-0 or for any period, because the company tags none of the three product-warranty accrual concepts in companyfacts.",
  "account": "product warranty accrual relative to revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000926326-26-000022:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_two_filled_quarters_only",
  "what_changed": "insufficient for a trend. The latest quarter where accruals_over_total_assets is filled is quarters-back-1 (2026-01-01..2026-03-31): -0.021526794727028047 (net income 11358000.0, operating cash flow 54500000.0, assets 2004107000.0). Its quarter-over-quarter comparison is not filled; the change against quarters-back-5 is -0.006213078988486493. Position in history: lowest of the 2 filled quarters. Two filled quarters support no trend claim.",
  "account": "total accruals over total assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0000926326-26-000022:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

**Trend table, years-back-0 (2025-01-01..2025-12-31)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend_cell",
  "what_changed": "accruals_over_total_assets for years-back-0 is -0.06342570085885593 (net income 2052000.0, operating cash flow 127300000.0, assets 1974720000.0). Change against years-back-1: 0.019174159581699282. Position in history: second highest of the 5 filled years.",
  "account": "total accruals over total assets",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend_cell",
  "what_changed": "bad_debt_reserve_ratio for years-back-0 is 0.03928656867175248 (allowance 8868000.0, receivables 216858000.0). Change against years-back-1: 0.014024539269715551. Position in history: highest of the 5 filled years.",
  "account": "allowance for doubtful accounts relative to gross current receivables",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend_cell",
  "what_changed": "contract_liabilities_over_revenue for years-back-0 is 0.14504935244694453 (current contract liabilities 171861000.0 over annual revenue 1184845000.0). Change against years-back-1: 0.01794526141606803. Position in history: highest of the 5 filled years.",
  "account": "current contract liabilities relative to annual revenue",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend_cell",
  "what_changed": "days_sales_of_inventory for years-back-0 is 54.05072328710029 (inventory 100905000.0, annual cost of revenue 681403000.0, 365 days). Change against years-back-1: 3.4465079838183357. Position in history: second lowest of the 5 filled years.",
  "account": "inventory relative to cost of revenue",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend_cell",
  "what_changed": "days_sales_outstanding for years-back-0 is 66.80466221320088 (receivables 216858000.0, annual revenue 1184845000.0, 365 days). Change against years-back-1: -17.567268974188863. Position in history: lowest of the 5 filled years.",
  "account": "current receivables (net) relative to revenue",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend_cell",
  "what_changed": "gross_margin for years-back-0 is 0.4249011474074668 (revenue 1184845000.0, cost of revenue 681403000.0). Change against years-back-1: 0.0014279339405649516. Position in history: second lowest of the 5 filled years.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend_cell",
  "what_changed": "insufficient. inventory_reserve_ratio has no value for years-back-0, or for any of the 5 years, for the reason the cell gives.",
  "account": "inventory valuation reserve relative to inventory",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000926326-26-000022:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend_cell",
  "what_changed": "insufficient. non_gaap_gap has no value for years-back-0, or for any of the 5 years, for the reason the cell gives.",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000926326-26-000022:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend_cell",
  "what_changed": "receivables_over_revenue for years-back-0 is 0.18302647181698872 (receivables 216858000.0 over annual revenue 1184845000.0). Change against years-back-1: -0.0474979303343494. Position in history: lowest of the 5 filled years.",
  "account": "current receivables (net) relative to revenue",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_annual_trend_cell",
  "what_changed": "soft_asset_share for years-back-0 is 0.8396577742667315 (assets 1974720000.0, PP&E 120111000.0, cash 196520000.0). Change against years-back-1: 0.06686290779117321. Position in history: highest of the 5 filled years.",
  "account": "assets other than PP&E and cash, relative to total assets",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000926326-26-000022:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend_cell",
  "what_changed": "insufficient. warranty_reserve_ratio has no value for years-back-0, or for any of the 5 years, for the reason the cell gives.",
  "account": "product warranty accrual relative to revenue",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000926326-26-000022:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

**Numeric facts**

```json
{ "id": "structure_and_disclosure_changes_capitalized_software_tagged_outside_baseline_concept",
  "what_changed": "The R&D capitalisation baseline looked for us-gaap:CapitalizedComputerSoftwareAdditions and found it 'in the record, but not for this period' for 2021 through 2025, so capitalized_over_expense is insufficient. The 2025 10-K reports capitalized software additions under a different concept, CapitalizedComputerSoftwarePeriodIncreaseDecrease: 28300000 for 2025 (internal-use software and software development costs, within PP&E) against 28500000 for 2024, plus 18100000 for 2025 against 17200000 for 2024 within other assets. The concept the company uses is not the one the baseline reads.",
  "account": "capitalized software development costs",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"28300000\"",
  "paragraph_id": "0000926326-26-000006:facts:CapitalizedComputerSoftwarePeriodIncreaseDecrease:2025-01-01..2025-12-31:us-gaap:PropertyPlantAndEquipmentByTypeAxis=omcl:InternalUseSoftwareandSoftwareDevelopmentCostsMember,us-gaap:StatementOfFinancialPositionLocationActivityCapitalizationAxis=us-gaap:PropertyPlantAndEquipmentMember" }
```

```json
{ "id": "liquidity_and_capital_receivables_sold_and_derecognized",
  "what_changed": "The 10-K reports financial assets transferred in sales and derecognised, at fair value: 15000000.0 at 2025-12-31, 17300000 at 2024-12-31, 5700000 at 2023-12-31. Receivables taken off the balance sheet this way are not in the ReceivablesNetCurrent input that both the days_sales_outstanding and receivables_over_revenue cells use. No 2026 value for this concept is in the parts of the numbers file I read.",
  "account": "receivables sold and derecognised",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"15000000.0\"",
  "paragraph_id": "0000926326-26-000006:facts:TransferOfFinancialAssetsAccountedForAsSalesFairValueOfDerecognizedAssets:2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_increase_in_first_half_cash_flow",
  "what_changed": "The 10-Q cash flow statement prints an increase in accounts and other receivables of 10193000 for 2026-01-01..2026-06-30, against -25863000 for 2025-01-01..2025-06-30 (the release shows these as (10,193) and 25,863 in operating cash flow). The balance-sheet receivables input is 227051000 at 2026-06-30 against 216858000 at 2025-12-31.",
  "account": "accounts and other receivables",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"10193000\"",
  "paragraph_id": "0000926326-26-000022:facts:IncreaseDecreaseInAccountsAndOtherReceivables:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_charge_first_half",
  "what_changed": "Deferred income taxes in the 10-Q cash flow statement are 10917000 for 2026-01-01..2026-06-30, against -2131000 for 2025-01-01..2025-06-30. Net deferred tax assets are 47377000 at 2026-06-30 against 58337000 at 2025-12-31. The income tax provision is 9544000 for the quarter on pre-tax income of 33833000, against 4814000 on 10453000 a year earlier. I do not compute a rate.",
  "account": "deferred tax assets and income tax provision",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"10917000\"",
  "paragraph_id": "0000926326-26-000022:facts:DeferredIncomeTaxesAndTaxCredits:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_fact",
  "what_changed": "The InventoryWriteDown fact is 0 for 2025, 5393000 for 2024 and 0 for 2023 (10-K). In the parts of the numbers file I read, this is the only inventory-valuation figure; the inventory reserve ratio stays insufficient.",
  "account": "inventory write-down",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0000926326-26-000006:facts:InventoryWriteDown:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_balance",
  "what_changed": "Remaining performance obligation at 2025-12-31 is 388000000.0 (10-K). No other period's value for this concept is in the parts of the numbers file I read.",
  "account": "remaining performance obligations",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"388000000.0\"",
  "paragraph_id": "0000926326-26-000006:facts:RevenueRemainingPerformanceObligation:2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized",
  "what_changed": "Revenue recognised in 2025 from contract liabilities is 124900000 (10-K). Total contract liabilities are 235115000 at 2025-12-31 and 217493000 at 2024-12-31; the current portion is 171861000 at 2025-12-31 and 141370000 at 2024-12-31. Contract assets, net, are 31917000 at 2025-12-31 and 40790000 at 2024-12-31. In the 10-Q, current contract liabilities are 188374000 and non-current 59517000 at 2026-06-30.",
  "account": "contract liabilities (deferred revenue)",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"124900000\"",
  "paragraph_id": "0000926326-26-000006:facts:ContractWithCustomerLiabilityRevenueRecognized:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_funds_held_for_clients",
  "what_changed": "Funds held for clients are 101104000 at 2025-12-31 and 47846000 at 2024-12-31 (10-K). Restricted cash is 54512000 at 2025-12-31 and 29413000 at 2024-12-31. Both sit outside the cash input of the soft_asset_share cell, so they count as soft assets in that ratio. Other current assets are 83641000 at 2026-06-30 against 132077000 at 2025-12-31 (10-Q); the 8-K shows the first-half change in customer funds (item below).",
  "account": "funds held for clients and restricted cash",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"101104000\"",
  "paragraph_id": "0000926326-26-000006:facts:FundsHeldForClients:2025-12-31" }
```

```json
{ "id": "revenue_recognition_customer_concentration_group_purchasing",
  "what_changed": "The concentration-risk percentage for the ten largest group purchasing organisations, against net sales revenue, is 0.61 for 2025 (10-K). No other year's value for this member is in the parts of the numbers file I read.",
  "account": "revenue concentration through group purchasing organisations",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"0.61\"",
  "paragraph_id": "0000926326-26-000006:facts:ConcentrationRiskPercentage1:2025-01-01..2025-12-31:srt:MajorCustomersAxis=omcl:TenLargestGroupPurchasingOrganizationsGPOsMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "liquidity_and_capital_primary_supplier_payments",
  "what_changed": "Payments to the primary supplier are 93900000 for 2025, 59100000 for 2024 and 65800000 for 2023 (10-K). The purchase obligation to that supplier at 2025-12-31 is 0.",
  "account": "payments to primary supplier",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"93900000\"",
  "paragraph_id": "0000926326-26-000006:facts:PaymentsToSuppliers:2025-01-01..2025-12-31:us-gaap:ShareBasedGoodsAndNonemployeeServicesTransactionBySupplierAxis=omcl:PrimarySupplierMember" }
```

```json
{ "id": "liquidity_and_capital_convertible_notes_repaid",
  "what_changed": "Repayments of convertible debt are 175000000 for 2025 (the notes due 2025, repaid 2025-09-15), 0 for 2024 and 0 for 2023 (10-K). The convertible notes due 2029 carry 167596000 at 2025-12-31 and 168203000 at 2026-06-30 (10-Q). The revolving facility has 350000000.0 of remaining capacity and 0 drawn at 2025-12-31.",
  "account": "convertible senior notes",
  "expected_direction": "none",
  "horizon": "next fiscal year",
  "quote": "\"value\": \"175000000\"",
  "paragraph_id": "0000926326-26-000006:facts:RepaymentsOfConvertibleDebt:2025-01-01..2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_cash_printed_at_two_precisions",
  "what_changed": "The same paragraph_id, CashAndCashEquivalentsAtCarryingValue at 2025-12-31 in the 10-K, prints twice: 196520000 at decimals -3 (statement) and 196500000 at decimals -5. The second is the same balance rounded; it is not a restatement. The trend cells, and the 10-Q's 2025-12-31 column, use 196520000.",
  "account": "cash and cash equivalents",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"196500000\"",
  "paragraph_id": "0000926326-26-000006:facts:CashAndCashEquivalentsAtCarryingValue:2025-12-31" }
```

**8-K earnings release (0000926326-26-000019, filed 2026-07-30)**

```json
{ "id": "across_documents_tariff_refund_lowered_cost_of_product_revenues",
  "what_changed": "The release says the company received $15 million of refunds of previously paid IEEPA tariffs in the quarter, which mainly reduced cost of product revenues and total cost of revenues. The 10-Q facts print cost of product revenues of 85668000 for 2026-04-01..2026-06-30 against 91919000 a year earlier, on product revenues of 175062000 against 163172000. This refund sits inside the cost-of-revenue input of the quarter's gross_margin and days_sales_of_inventory cells. The release does not say whether more refunds will follow.",
  "account": "cost of product revenues",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "During the quarter ended June 30, 2026, the Company received $15 million in refunds for previously paid IEEPA tariffs. This amount primarily reduced the cost of product revenues and total cost of revenues in the second quarter of 2026",
  "paragraph_id": "0000926326-26-000019:8k_2_02:17" }
```

```json
{ "id": "results_against_expectations_ebitda_guidance_step_down",
  "what_changed": "For the next quarter the release guides non-GAAP EBITDA to $32 million - $37 million, total revenues to $301 million - $307 million and product revenues to $169 million - $172 million. It reports $67 million non-GAAP EBITDA and $312 million total revenues for the quarter just ended. It raises the full-year non-GAAP EBITDA guidance to $175 million - $185 million and the non-GAAP EPS guidance to $2.15 - $2.30. The earlier ranges are not in my input.",
  "account": "non-GAAP EBITDA",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Non-GAAP EBITDA | $32 million - $37 million",
  "paragraph_id": "0000926326-26-000019:8k_2_02:26" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_recurring_revenue_growth_delayed",
  "what_changed": "The release updates annual recurring revenue guidance (now $660 million - $680 million for 2026) because certain growth opportunities are expected to take longer to develop than previously projected. It also updates product bookings guidance (now $425 million - $560 million) to its current view of the range of outcomes. The previous ranges are not in my input.",
  "account": "annual recurring revenue",
  "expected_direction": "down",
  "horizon": "fiscal year 2026",
  "quote": "our annual recurring revenue guidance to reflect certain growth opportunities that we now expect will take longer to develop than previously projected",
  "paragraph_id": "0000926326-26-000019:8k_2_02:25" }
```

```json
{ "id": "across_documents_quarterly_operating_cash_flow_printed_in_release",
  "what_changed": "The release's free-cash-flow reconciliation prints three-month GAAP net cash provided by operating activities of 68,314 for the quarter against 42,755 a year earlier (in thousands), and 122,814 for six months. The trend table found no quarterly operating-cash-flow row in companyfacts for this quarter, so its accruals_over_total_assets cell is insufficient. The release figure is not a companyfacts row and I do not compute the ratio from it.",
  "account": "operating cash flow",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "GAAP net cash provided by operating activities | $ | 68,314",
  "paragraph_id": "0000926326-26-000019:8k_2_02:99" }
```

```json
{ "id": "across_documents_non_gaap_net_income_printed_in_release",
  "what_changed": "The release prints non-GAAP net income of 43,536 against GAAP net income of 24,289 for the quarter, and 21,074 against 5,639 a year earlier (in thousands). The trend table's non_gaap_gap is insufficient because companyfacts holds no non-GAAP measure. I do not compute the gap.",
  "account": "non-GAAP net income",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Non-GAAP net income | $ | 43,536",
  "paragraph_id": "0000926326-26-000019:8k_2_02:87" }
```

```json
{ "id": "earnings_quality_new_professional_services_restructuring_add_back",
  "what_changed": "A non-GAAP add-back for Professional Services restructuring, absent ('—') a year earlier, appears this quarter: 1,761 (in thousands) in the operating-income and net-income reconciliations, of which 1,630 sits in cost of product revenues and 131 in operating expenses. The release calls these nonrecurring charges.",
  "account": "restructuring charges excluded from non-GAAP results",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Professional Services restructuring | 1,761",
  "paragraph_id": "0000926326-26-000019:8k_2_02:87" }
```

```json
{ "id": "earnings_quality_new_product_organization_restructuring_add_back",
  "what_changed": "A non-GAAP add-back for Product organization restructuring, absent ('—') a year earlier, appears this quarter: 1,929 (in thousands), described as mainly severance and related expenses. The 2025 six-month period instead carried legal and regulatory expenses (2,700), management severance (562) and executive transition costs (968).",
  "account": "restructuring charges excluded from non-GAAP results",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Product organization restructuring | 1,929",
  "paragraph_id": "0000926326-26-000019:8k_2_02:87" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_and_customer_funds",
  "what_changed": "The release's balance sheet prints accrued liabilities of 148,502 at June 30, 2026 against 203,586 at December 31, 2025 (in thousands); the 10-Q facts print 148502000 and 203586000. Other current assets are 83,641 against 132,077, and cash and cash equivalents 292,165 against 196,520. The six-month cash flow statement prints change in customer funds, net, of (23,923), against 3,307 a year earlier.",
  "account": "accrued liabilities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Accrued liabilities | 148,502",
  "paragraph_id": "0000926326-26-000019:8k_2_02:74" }
```

## Seen in the notes

No fact in the parts of input_numbers.json I read carries a mark saying its element sat inside a note. Every fact prints the same fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and sometimes superseded_by. With no mark to sort by, and since I do not judge which tables are notes, no item is placed under this heading. Facts that may come from note tables (receivables sold, primary-supplier payments, capitalized software, remaining performance obligations, funds held for clients, customer concentration) are reported once, under the heading above. The ranges of the numbers file I did not read (listed at the top) may hold facts that carry such a mark; I cannot say.
