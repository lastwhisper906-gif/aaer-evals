<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# LFUS — numbers reader — 10-Q 0001628280-26-050481 (period ended 2026-06-27)

## How to read this report

- Every number below is copied as printed in my input. None is computed here.
- `expected_direction`: for trend items, the sign of the change Python printed for the named account. For 8-K and fact items, it is the direction between the two printed figures the item names. It is `none` where nothing is printed to compare. It is not a forecast.
- `horizon` names the periods the printed figures cover.
- I read all four input files in full:
  - input_8k.md
  - input_numbers.json (104321 lines)
  - input_prior_predictions.md
  - input_trends.json
- None of them contains prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.

## What the record does not reach

- **quarters-back-0 (target end 2026-06-27), the quarter this 10-Q reports**, has no cells. The reason the period gives: "no quarter ending within 20 days of 2026-06-27 is in the companyfacts record; the companyfacts record's newest row was filed 2026-05-06, before this run's cutoff 2026-07-29 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it".
  - No trend metric exists for this quarter.
  - Current-quarter figures appear below only as 8-K rows and 10-Q facts, quoted as printed.
  - The newest quarter in the trend table is quarters-back-1 (2025-12-28..2026-03-28), itemized below.
- **quarters-back-2 (2025-12-27) and quarters-back-6 (2024-12-28)** also have no cells. Their reason: "no quarter ending within 20 days of … is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
  - My input holds no fourth-quarter derivation, so these quarters do not exist for me.
  - That is also why no quarter-over-quarter change is printed for quarters-back-1.

## Sections my input does not contain

- `input_numbers.json` holds `documents` and `facts` only. It has no articulation checks, no restatement traces, no fourth-quarter derivation and no tag-change records.
- **Articulation gaps:** none can be reported, because none is computed in my input.
- **Restated prior values:** Python printed no restatement trace. Two filed-history differences are itemized below:
  1. The ScenarioAdjustmentMember pair on fiscal 2024 cost of goods sold and inventory, from the 10-K.
  2. Basler's acquisition-date goodwill. The 10-K tags it as 152343000; both 10-Qs tag it as 160977000.

  I did not compare every fact across filings.
- **Changes of tag:** every trend input uses the same concept in every period. Nowhere does my input say a period rests on a different concept. The concepts are:
  - RevenueFromContractWithCustomerIncludingAssessedTax
  - CostOfGoodsAndServicesSold
  - AccountsReceivableNetCurrent
  - AllowanceForDoubtfulAccountsReceivableCurrent
  - InventoryNet
  - InventoryValuationReserves
  - DeferredRevenue
  - Assets
  - CashAndCashEquivalentsAtCarryingValue
  - PropertyPlantAndEquipmentNet
  - NetIncomeLoss
  - NetCashProvidedByUsedInOperatingActivities
- The years-back-0 R&D capitalization baseline prints no `paragraph_id`, so it is not itemized. Its printed values are:
  - book_value_with_rnd_capitalized 2732037600.0
  - earnings_with_rnd_capitalized -49657400.0
  - research_and_development_amortization 84856400.0
  - research_and_development_asset 306003600.0
  - capitalized_development_cost is missing: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period."
- The 8-K's filing-history lists print no `[id]`, so they are not itemized. They show:
  - an NT 10-K filed 2025-02-27 (0001140361-25-006294) for the period ended 2024-12-28
  - an Item 4.01 8-K filed 2023-08-16
  - an Item 1.01/2.03 8-K filed 2026-03-13
  - Item 5.02 8-Ks filed 2026-01-08, 2026-03-05 and 2026-04-28
- Prior predictions: none on record for this company.

## Seen in the statements

### Trend table — years-back-0 (fiscal year 2024-12-29..2025-12-27)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual", "what_changed": "Accruals over total assets for the fiscal year 2024-12-29..2025-12-27 is -0.12774578219347169; the year-over-year change against years-back-1 is -0.059028879203862045. Inputs as printed: net income -71700000.0 and operating cash flow 433764000.0 (10-K 0001628280-26-009585), assets 3956796000.0. Lowest of the 5 filled years.", "account": "accruals over total assets: (net income - operating cash flow) / assets", "expected_direction": "down", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual", "what_changed": "Bad-debt reserve ratio at 2025-12-27 is 0.17505133003852025; the year-over-year change against years-back-1 is -0.01703838318545267. Inputs as printed: allowance 77073000.0, receivables 363215000.0. Lowest of the 5 filled years.", "account": "allowance for doubtful accounts / (receivables + allowance)", "expected_direction": "down", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:bad_debt_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual", "what_changed": "Contract liabilities over revenue for the fiscal year is 0.004699756190980659; the year-over-year change against years-back-1 is 0.003989046522042642. Inputs as printed: DeferredRevenue 11215000.0 at 2025-12-27, revenue 2386294000.0. Highest of the 5 filled years.", "account": "deferred revenue (contract liabilities) / revenue", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:contract_liabilities_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual", "what_changed": "Days sales of inventory for the fiscal year is 102.41223143912755; the year-over-year change against years-back-1 is -5.569926816206944. Inputs as printed: inventory 416472000.0, cost of revenue 1480251000.0. Lowest of the 5 filled years.", "account": "inventory / cost of revenue * days in period", "expected_direction": "down", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_of_inventory:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual", "what_changed": "Days sales outstanding for the fiscal year is 55.404011408485296; the year-over-year change against years-back-1 is 6.493746149909313. Inputs as printed: receivables 363215000.0, revenue 2386294000.0. Highest of the 5 filled years.", "account": "receivables / revenue * days in period", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_outstanding:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_gross_margin_annual", "what_changed": "Gross margin for the fiscal year is 0.37968624151089514; the year-over-year change against years-back-1 is 0.020204087307437724. Inputs as printed: revenue 2386294000.0, cost of revenue 1480251000.0. Third highest of the 5 filled years.", "account": "(revenue - cost of revenue) / revenue", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:gross_margin:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual", "what_changed": "Inventory reserve ratio at 2025-12-27 is 0.19856076759061833; the year-over-year change against years-back-1 is 0.038749778167811666. Inputs as printed: InventoryValuationReserves 82695000.0, inventory 416472000.0. Highest of the 5 filled years.", "account": "inventory valuation reserves / net inventory", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:inventory_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual", "what_changed": "Receivables over revenue for the fiscal year is 0.15220882255078377; the year-over-year change against years-back-1 is 0.017839961950300298. Inputs as printed: receivables 363215000.0, revenue 2386294000.0. Highest of the 5 filled years.", "account": "receivables / revenue", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:receivables_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual", "what_changed": "Soft-asset share at 2025-12-27 is 0.7209785392019199; the year-over-year change against years-back-1 is 0.02983266478304869. Inputs as printed: assets 3956796000.0, property plant and equipment 540640000.0, cash 563391000.0. Third highest of the 5 filled years.", "account": "(assets - PP&E - cash) / assets", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:soft_asset_share:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient", "what_changed": "insufficient: the non-GAAP gap cannot be filled for the fiscal year because the record holds no non-GAAP net income; the same reason is printed for every held period.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "fiscal year ended 2025-12-27", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001628280-26-050481:trends:non_gaap_gap:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient", "what_changed": "insufficient: the warranty reserve ratio cannot be filled for the fiscal year because none of the three warranty-accrual concepts is tagged in any period; the cell says the filing, not this record, would show whether the company does not tag it or states it only by segment.", "account": "warranty accrual relative to revenue", "expected_direction": "none", "horizon": "fiscal year ended 2025-12-27", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period.", "paragraph_id": "0001628280-26-050481:trends:warranty_reserve_ratio:2024-12-29..2025-12-27" }
```

### Trend table — quarters-back-1 (2025-12-28..2026-03-28), the newest quarter the record reaches

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly", "what_changed": "Accruals over total assets for the quarter 2025-12-28..2026-03-28 is -0.0013249338764412966; the year-over-year change against quarters-back-5 is 0.0043812541497453925; no quarter-over-quarter change is printed because the cell is not filled in quarters-back-2. Inputs as printed: net income 75147000.0, operating cash flow 80258000.0, assets 3857551000.0. Only 2 quarters are filled, which is insufficient for a trend claim.", "account": "accruals over total assets: (net income - operating cash flow) / assets", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly", "what_changed": "Bad-debt reserve ratio at 2026-03-28 is 0.173363219553052; the year-over-year change against quarters-back-5 is -0.005528562854355407. Inputs as printed: allowance 79896000.0, receivables 380963000.0.", "account": "allowance for doubtful accounts / (receivables + allowance)", "expected_direction": "down", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"third highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:bad_debt_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly", "what_changed": "Contract liabilities over revenue for the quarter is 0.010218138146548771; the year-over-year change against quarters-back-5 is 0.005572697984328197. Inputs as printed: DeferredRevenue 6713000.0 at 2026-03-28, revenue 656969000.0.", "account": "deferred revenue (contract liabilities) / revenue", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:contract_liabilities_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly", "what_changed": "Days sales of inventory for the quarter is 94.63756020058587; the year-over-year change against quarters-back-5 is -14.730463519270884. Inputs as printed: inventory 418922000.0, cost of revenue 402820000.0.", "account": "inventory / cost of revenue * days in period", "expected_direction": "down", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_of_inventory:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly", "what_changed": "Days sales outstanding for the quarter is 52.769054552041275; the year-over-year change against quarters-back-5 is 0.5915644608102397. Inputs as printed: receivables 380963000.0, revenue 656969000.0.", "account": "receivables / revenue * days in period", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_outstanding:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly", "what_changed": "Gross margin for the quarter is 0.3868508255336249; the year-over-year change against quarters-back-5 is 0.012949720189474434. Inputs as printed: revenue 656969000.0, cost of revenue 402820000.0.", "account": "(revenue - cost of revenue) / revenue", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:gross_margin:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly", "what_changed": "Inventory reserve ratio at 2026-03-28 is 0.19954311303774927; the year-over-year change against quarters-back-5 is 0.02631450229025825. Inputs as printed: InventoryValuationReserves 83593000.0, inventory 418922000.0.", "account": "inventory valuation reserves / net inventory", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:inventory_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly", "what_changed": "Receivables over revenue for the quarter is 0.5798797203521019; the year-over-year change against quarters-back-5 is 0.006500708360552054. Inputs as printed: receivables 380963000.0, revenue 656969000.0.", "account": "receivables / revenue", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:receivables_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly", "what_changed": "Soft-asset share at 2026-03-28 is 0.7368213667168626; the year-over-year change against quarters-back-5 is 0.02719039019409586. Inputs as printed: assets 3857551000.0, property plant and equipment 533528000.0, cash 481697000.0.", "account": "(assets - PP&E - cash) / assets", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:soft_asset_share:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient", "what_changed": "insufficient: the non-GAAP gap cannot be filled for the quarter because the record holds no non-GAAP net income.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "quarter ended 2026-03-28", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001628280-26-050481:trends:non_gaap_gap:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient", "what_changed": "insufficient: the warranty reserve ratio cannot be filled for the quarter because none of the three warranty-accrual concepts is tagged in any period.", "account": "warranty accrual relative to revenue", "expected_direction": "none", "horizon": "quarter ended 2026-03-28", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period.", "paragraph_id": "0001628280-26-050481:trends:warranty_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_comparative_quarter_insufficient", "what_changed": "insufficient: for 2025-03-30..2025-06-28, the prior-year counterpart of the quarter this 10-Q reports, accruals cannot be filled because operating cash flow is not in the record as a discrete quarter. The same reason is printed for 2025-06-29..2025-09-27 and 2024-06-30..2024-09-28.", "account": "accruals over total assets", "expected_direction": "none", "horizon": "quarter ended 2025-06-28", "quote": "\"missing\": \"no row for operating_cash_flow in 2025-03-30..2025-06-28: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2025-03-30..2025-06-28" }
```

### Earnings release (8-K 0001628280-26-050382, Item 2.02, Exhibit 99.1)

```json
{ "id": "results_against_expectations_management_reports_performance_above_own_expectations", "what_changed": "The CEO says results exceeded the company's own expectations. The earlier expectation it refers to is not in my input, so the size of the beat cannot be stated.", "account": "net sales and earnings against the company's own outlook", "expected_direction": "up", "horizon": "quarter ended 2026-06-27", "quote": "We delivered strong second quarter results, with performance exceeding our expectations reflecting broad-based demand strength and disciplined execution across the portfolio", "paragraph_id": "0001628280-26-050382:8k_2_02:15" }
```

```json
{ "id": "results_against_expectations_company_net_sales_guidance", "what_changed": "Guidance for the next quarter: net sales $780 - $800 million, adjusted diluted EPS $4.85 to $5.05, adjusted effective tax rate about 23% - 24%. Paragraph 8k_2_02:16 expects approximately 26% total revenue growth versus the prior year, supported by record bookings and contributions from the Basler acquisition. No earlier guidance or outside estimate is in my input.", "account": "net sales guidance", "expected_direction": "up", "horizon": "fiscal third quarter of 2026 (the quarter after 2026-06-27)", "quote": "Net sales in the range of $780 - $800 million", "paragraph_id": "0001628280-26-050382:8k_2_02:19" }
```

```json
{ "id": "earnings_quality_restructuring_impairment_and_other_charges_increase", "what_changed": "Restructuring, impairment and other charges: 20,021 (thousands) for the three months ended 2026-06-27 against 2,506 a year earlier; 27,443 for six months against 11,525. The segment table's unallocated 'Other (a)' line is (20,357) against (4,020).", "account": "restructuring, impairment and other charges", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "| Restructuring, impairment, and other charges |  | 20,021 |  |  | 2,506 |  |  | 27,443 |  |  | 11,525 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:53" }
```

```json
{ "id": "earnings_quality_non_gaap_adjustments_per_share", "what_changed": "The company's own reconciliation: GAAP diluted EPS $3.49 against adjusted diluted EPS $4.19 for Q2-26, a per-share adjustment of 0.70 (Q2-25 0.55; YTD-26 1.06; YTD-25 0.99). This is the release's figure, not the trend table's non_gaap_gap, which is insufficient.", "account": "GAAP to adjusted diluted EPS gap", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "| EPS impact of Non-GAAP adjustments (below) |  | 0.70 |  |  | 0.55 |  |  | 1.06 |  |  | 0.99 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_purchase_accounting_inventory_step_up", "what_changed": "Purchase accounting inventory adjustments (reflected in cost of sales, footnote b) of $5.4 million year to date in 2026 and none in either second quarter, against (0.5) year to date in 2025; they are added back in the adjusted figures. The covenant EBITDA schedule adds back a 'Purchase accounting inventory step-up charge' of 6.4 for the twelve months ended 2026-06-27.", "account": "cost of sales: acquired-inventory step-up", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "| Purchase accounting inventory adjustments (b) |  | — |  |  | — |  |  | 5.4 |  |  | (0.5) |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:69" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_decline", "what_changed": "GAAP effective tax rate 23.6% in Q2-26 against 26.7% in Q2-25, and 23.0% year to date against 27.0%; adjusted effective rate 21.9% against 23.4%. Footnote (e) reports $2.7 million of tax benefits from statute-of-limitations lapses on previously unrecognized tax benefits, recognized in the first quarter of 2026.", "account": "effective income tax rate", "expected_direction": "down", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "| Effective rate |  | 23.6 | % |  | 26.7 | % |  | 23.0 | % |  | 27.0 | % |", "paragraph_id": "0001628280-26-050382:8k_2_02:81" }
```

```json
{ "id": "estimates_and_discretion_indemnification_receivable_reversal", "what_changed": "Other income, net for 2026 includes the reversal of a $2.7 million indemnification receivable, tied to the same tax-reserve releases; it is excluded from the adjusted figures.", "account": "other income, net: indemnification receivable", "expected_direction": "none", "horizon": "first quarter of 2026 (within six months ended 2026-06-27)", "quote": "(d) 2026 included the reversal of an indemnification receivable of $2.7 million related to lapses in the statute of limitations for previously unrecognized tax benefits recognized in the first quarter of 2026.", "paragraph_id": "0001628280-26-050382:8k_2_02:90" }
```

```json
{ "id": "earnings_quality_foreign_exchange_loss_turns_to_gain", "what_changed": "Foreign exchange (gain) loss: (160) gain in Q2-26 against a 10,448 loss in Q2-25; (2,573) gain year to date against a 15,291 loss. The company treats it as a non-operating non-GAAP adjustment.", "account": "foreign exchange (gain) loss", "expected_direction": "down", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "| Foreign exchange (gain) loss |  | (160) |  |  | 10,448 |  |  | (2,573) |  |  | 15,291 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:53" }
```

```json
{ "id": "revenue_recognition_trade_receivables_and_allowance_balance", "what_changed": "Trade receivables net 423,590 at 2026-06-27 against 363,215 at 2025-12-27 (thousands), with the allowance 86,865 against 77,073. The trend table has no ratio for this date.", "account": "trade receivables and allowance", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "| Trade receivables, less allowances of $86,865 and $77,073 at June 27, 2026 and December 27, 2025, respectively |  | 423,590 |  |  | 363,215 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_inventories_balance", "what_changed": "Inventories 433,755 at 2026-06-27 against 416,472 at 2025-12-27 (thousands). The trend table has no ratio for this date.", "account": "inventories", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "| Inventories |  | 433,755 |  |  | 416,472 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:49" }
```

```json
{ "id": "liquidity_and_capital_receivables_absorbed_operating_cash", "what_changed": "Change in trade receivables absorbed 65,720 (thousands) of operating cash in the six months to 2026-06-27 against 52,635 a year earlier.", "account": "cash flow: change in trade receivables", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "| Trade receivables |  | (65,720) |  |  | (52,635) |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:57" }
```

```json
{ "id": "liquidity_and_capital_inventory_build_absorbed_operating_cash", "what_changed": "Change in inventories absorbed 21,254 (thousands) of operating cash in the six months to 2026-06-27, against a release of 23,316 a year earlier.", "account": "cash flow: change in inventories", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "| Inventories |  | (21,254) |  |  | 23,316 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:57" }
```

```json
{ "id": "liquidity_and_capital_payables_funded_operating_cash", "what_changed": "Change in accounts payable provided 39,159 (thousands) of operating cash in the six months to 2026-06-27, against a use of 7,001 a year earlier. Balance-sheet accounts payable is 248,972 against 211,079 at 2025-12-27.", "account": "cash flow: change in accounts payable", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "| Accounts payable |  | 39,159 |  |  | (7,001) |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:57" }
```

```json
{ "id": "liquidity_and_capital_all_other_financing_inflow", "what_changed": "'All other cash provided by financing activities' is an inflow of 72,179 (thousands) in the six months to 2026-06-27, against an outflow of 813 a year earlier. The release gives no breakdown, and my input does not say what the line contains.", "account": "financing cash flow: all other", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "| All other cash provided by financing activities |  | 72,179 |  |  | (813) |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:57" }
```

```json
{ "id": "liquidity_and_capital_credit_facility_repayment", "what_changed": "Net payments of the credit facility were 166,250 (thousands) in the six months to 2026-06-27, against 57,500 a year earlier. Long-term debt less current portion is 529,660 at 2026-06-27 against 706,394 at 2025-12-27; interest expense in Q2 is 5,739 against 8,568.", "account": "debt", "expected_direction": "down", "horizon": "six months ended 2026-06-27; balances 2026-06-27 against 2025-12-27", "quote": "| Net payments of credit facility |  | (166,250) |  |  | (57,500) |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:57" }
```

```json
{ "id": "liquidity_and_capital_free_cash_flow", "what_changed": "Free cash flow, as the company defines it: 127.3 ($ millions) in Q2-26 against 72.6 in Q2-25, and 193.5 year to date against 115.2. Operating cash flow is 146.2 against 82.5 for Q2; capital expenditures are (18.9) against (9.9).", "account": "free cash flow", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "| Free cash flow |  | $ | 127.3 |  |  | $ | 72.6 |  |  | $ | 193.5 |  |  | $ | 115.2 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_trailing_impairment_in_covenant_ebitda", "what_changed": "The covenant Consolidated EBITDA schedule for the twelve months ended 2026-06-27 starts from a Net Loss of $(8.2) million and adds back impairment charges of 315.1. The 10-K tags fiscal 2025 AssetImpairmentCharges of 302052000 and GoodwillImpairmentLoss of 301185000 (items below).", "account": "impairment charges in trailing covenant EBITDA", "expected_direction": "none", "horizon": "twelve months ended 2026-06-27", "quote": "| Impairment charges |  | 315.1 |  |", "paragraph_id": "0001628280-26-050382:8k_2_02:82" }
```

```json
{ "id": "liquidity_and_capital_covenant_net_leverage", "what_changed": "Consolidated net leverage ratio of 0.8x, against the 3.50:1.00 level at which an Event of Default is triggered (paragraph 8k_2_02:83). Net debt is 493.8 ($ millions) and Consolidated EBITDA is 623.9.", "account": "covenant net leverage", "expected_direction": "none", "horizon": "twelve months ended 2026-06-27", "quote": "| Consolidated Net Leverage Ratio (as defined in the Credit Agreement) * |  | 0.8x |", "paragraph_id": "0001628280-26-050382:8k_2_02:82" }
```

```json
{ "id": "liquidity_and_capital_covenant_ebitda_definition_amended", "what_changed": "The Credit Agreement was amended in Q1 2026 so that restructuring charges and business optimization expenses can be added back in covenant EBITDA. The filing-history list also shows an Item 1.01/2.03 8-K filed 2026-03-13.", "account": "credit agreement covenant definition", "expected_direction": "none", "horizon": "from the first quarter of 2026", "quote": "The Credit Agreement was amended in Q1 2026 and now allows to add restructuring charges and business optimization expenses in addition to the prior credit agreement.", "paragraph_id": "0001628280-26-050382:8k_2_02:84" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_segment_operating_income", "what_changed": "Transportation segment operating income 25,691 (thousands) in Q2-26 against 28,074, a decline of (8.5)% on sales growth of 1.7%. Year to date it is 49,794 against 46,991 (+6.0%). Segment operating margin is 14.1% against 15.6%.", "account": "Transportation segment operating income", "expected_direction": "down", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "| Transportation |  | 25,691 |  |  | 28,074 |  |  |  |  | (8.5) | % |  | 49,794 |  |  | 46,991 |  |  |  |  | 6.0 | % |", "paragraph_id": "0001628280-26-050382:8k_2_02:61" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_ebitda_margin", "what_changed": "Transportation adjusted EBITDA margin fell to 18.6% (-190 bps), which the company attributes to lower commercial vehicle profitability.", "account": "Transportation segment adjusted EBITDA margin", "expected_direction": "down", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "Adjusted EBITDA margin for the second quarter 2026 decreased to 18.6% (-190 bps) driven by lower commercial vehicle profitability which more than offset passenger vehicle margin expansion.", "paragraph_id": "0001628280-26-050382:8k_2_02:28" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_auto_sensor_declines", "what_changed": "Passenger vehicle sales fell on lower global car builds and auto sensor declines. The reconciliation table shows auto sensor products at (10)% reported and (12)% organic for the quarter (8k_2_02:75), and (10)% organic year to date. The 10-K tags Automotive Sensors reporting-unit goodwill of 274900000 at 2025-12-27, after an 8600000 impairment in 2024-09-29..2024-12-28. The 10-Q tags auto sensor net sales of 15294000 in Q2-26 against 16989000 in Q2-25.", "account": "Transportation: passenger car and auto sensor sales", "expected_direction": "down", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "Passenger vehicle sales were impacted by lower global passenger car builds and auto sensor product declines.", "paragraph_id": "0001628280-26-050382:8k_2_02:27" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_industrial_operating_margin", "what_changed": "Industrial segment operating margin 18.3% in Q2-26 against 19.2%, a change of (0.9) points, while segment sales rose 52.5%, 36 points of it from the Basler acquisition. Year to date the margin is 17.6% against 17.4%.", "account": "Industrial segment operating margin", "expected_direction": "down", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "| Industrial |  | 18.3 | % |  | 19.2 | % |  | (0.9) | % |  | 17.6 | % |  | 17.4 | % |  | 0.2 | % |", "paragraph_id": "0001628280-26-050382:8k_2_02:64" }
```

```json
{ "id": "structure_and_disclosure_changes_basler_acquired_growth", "what_changed": "Industrial net sales +52% with +16% organic; the Basler acquisition added +36 points. Company net sales are $739 million, +20%, with organic growth +14% (8k_2_02:8); acquisitions contribute 6 points of total growth (8k_2_02:73).", "account": "net sales: acquired against organic growth", "expected_direction": "up", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "The Basler acquisition contributed +36% to growth.", "paragraph_id": "0001628280-26-050382:8k_2_02:30" }
```

```json
{ "id": "liquidity_and_capital_dividend_increase", "what_changed": "Quarterly dividend raised to $0.80 from $0.75 per share (+7%), payable 2026-09-03. Cash dividends paid were 37,872 (thousands) in six months against 34,677; there were no share repurchases, against 27,553 a year earlier.", "account": "dividend per share", "expected_direction": "up", "horizon": "dividend payable 2026-09-03 against the prior quarter's", "quote": "The company will pay a cash dividend of $0.80 per share on its common stock, a 7% increase from the prior quarter dividend of $0.75 per share.", "paragraph_id": "0001628280-26-050382:8k_2_02:33" }
```

### Numeric facts — 10-K 0001628280-26-009585 (filed 2026-02-19)

```json
{ "id": "articulation_and_the_filed_history_prior_period_cost_of_sales_adjustment", "what_changed": "The fiscal 2025 10-K tags cost of goods and services sold for fiscal 2024 (2023-12-31..2024-12-28) with an adjustment of 12300000 on the ScenarioAdjustmentMember. The same value appears twice (f-419 and f-421). It is paired with an InventoryNet adjustment of -12300000 at 2024-12-28. My input holds no Python restatement trace, so the originally reported fiscal 2024 figures are not in front of me; the trend table's fiscal 2024 inputs (cost of revenue 1403226000.0, inventory 416273000.0) come from this same 10-K.", "account": "cost of goods sold, fiscal 2024 (prior-period adjustment)", "expected_direction": "up", "horizon": "fiscal year ended 2024-12-28 as presented in the 10-K filed 2026-02-19", "quote": "\"value\": \"12300000\"", "paragraph_id": "0001628280-26-009585:facts:CostOfGoodsAndServicesSold:2023-12-31..2024-12-28:srt:StatementScenarioAxis=us-gaap:ScenarioAdjustmentMember" }
```

```json
{ "id": "articulation_and_the_filed_history_prior_period_inventory_adjustment", "what_changed": "The fiscal 2025 10-K tags InventoryNet at 2024-12-28 with an adjustment of -12300000 on the ScenarioAdjustmentMember. It is the counterpart of the fiscal 2024 cost-of-sales adjustment of 12300000.", "account": "inventory at 2024-12-28 (prior-period adjustment)", "expected_direction": "down", "horizon": "balance at 2024-12-28 as presented in the 10-K filed 2026-02-19", "quote": "\"value\": \"-12300000\"", "paragraph_id": "0001628280-26-009585:facts:InventoryNet:2024-12-28:srt:StatementScenarioAxis=us-gaap:ScenarioAdjustmentMember" }
```

```json
{ "id": "earnings_quality_goodwill_impairment_annual", "what_changed": "Fiscal 2025 goodwill impairment of 301185000, all in the Electronics segment; the reporting-unit fact for Electronics Passive Products and Sensors is 301200000. The fiscal 2024 figure is 44763000. Accumulated goodwill impairment is 396982000 at 2025-12-27.", "account": "goodwill impairment", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"value\": \"301185000\"", "paragraph_id": "0001628280-26-009585:facts:GoodwillImpairmentLoss:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_restructuring_and_impairment_provisions_annual", "what_changed": "Fiscal 2025 restructuring, settlement and impairment provisions of 320050000, against 108441000 in fiscal 2024 and 16501000 in fiscal 2023. The same year shows operating income of 37528000 and net income of -71700000.", "account": "restructuring, settlement and impairment provisions", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"value\": \"320050000\"", "paragraph_id": "0001628280-26-009585:facts:RestructuringSettlementAndImpairmentProvisions:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_corporate_unallocated_operating_loss_annual", "what_changed": "The 10-K tags fiscal 2025 operating income on the CorporateNonSegmentMember as -326341000. Consolidated operating income for the year is 37528000. No prior-year corporate figure is itemized here, so no direction is stated.", "account": "unallocated corporate operating loss", "expected_direction": "none", "horizon": "fiscal year ended 2025-12-27", "quote": "\"value\": \"-326341000\"", "paragraph_id": "0001628280-26-009585:facts:OperatingIncomeLoss:2024-12-29..2025-12-27:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "earnings_quality_annual_effective_tax_rate_on_small_pretax_income", "what_changed": "The 10-K tags the fiscal 2025 effective income tax rate as 20.878. Income before income taxes is tagged 3607000, and net income -71700000. The rate reconciliation tags tax contingencies at -5827000. No prior-year rate is itemized here.", "account": "effective income tax rate, fiscal year", "expected_direction": "none", "horizon": "fiscal year ended 2025-12-27", "quote": "\"value\": \"20.878\"", "paragraph_id": "0001628280-26-009585:facts:EffectiveIncomeTaxRateContinuingOperations:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_valuation_allowance_increase", "what_changed": "Deferred tax asset valuation allowance of 97557000 at 2025-12-27 against 55468000 at 2024-12-28. The rate reconciliation tags a change in the valuation allowance for the German tax authority (country:DE) of 26839000 for fiscal 2025.", "account": "deferred tax asset valuation allowance", "expected_direction": "up", "horizon": "2025-12-27 against 2024-12-28", "quote": "\"value\": \"97557000\"", "paragraph_id": "0001628280-26-009585:facts:DeferredTaxAssetsValuationAllowance:2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_sales_discounts_and_allowances_reserve", "what_changed": "The valuation-and-qualifying-accounts schedule tags a reserve for sales discounts and allowances of 74553000 at 2025-12-27, and an allowance for credit losses of 2520000. The balance-sheet allowance used in the bad_debt_reserve_ratio is 77073000 at the same date. No prior-year schedule balance is itemized here.", "account": "reserve for sales discounts and allowances", "expected_direction": "none", "horizon": "balance at 2025-12-27", "quote": "\"value\": \"74553000\"", "paragraph_id": "0001628280-26-009585:facts:ValuationAllowancesAndReservesBalance:2025-12-27:us-gaap:ValuationAllowancesAndReservesTypeAxis=lfus:SECSchedule1209ReserveSalesDiscountsandAllowancesMember" }
```

```json
{ "id": "estimates_and_discretion_goodwill_headroom_industrial_controls", "what_changed": "At the 2025-09-27 test, the Industrial Controls reporting unit's fair value exceeded its carrying amount by 0.22. It carries goodwill of 238500000 at 2025-12-27, after a 36100000 impairment in 2024-09-29..2024-12-28. Other units: Commercial Vehicle 0.99, Electronics Passive Products and Sensors 0.87, Passenger Car 1.53, Industrial Circuit Protection 3.03. The range at 2025-12-27 is a minimum of 0.22 and a maximum of 3.03.", "account": "goodwill impairment-test headroom", "expected_direction": "none", "horizon": "impairment test at 2025-09-27", "quote": "\"value\": \"0.22\"", "paragraph_id": "0001628280-26-009585:facts:ReportingUnitPercentageOfFairValueInExcessOfCarryingAmount:2025-09-27:us-gaap:ReportingUnitAxis=lfus:IndustrialControlsMember" }
```

```json
{ "id": "estimates_and_discretion_dortmund_fab_goodwill_impairment", "what_changed": "Goodwill impairment of 64600000 tagged to the Dortmund Fab acquisition for 2025-09-28..2025-12-27. That acquisition recognized goodwill of 57321000 at 2024-12-31.", "account": "goodwill impairment: Dortmund Fab", "expected_direction": "up", "horizon": "fiscal fourth quarter 2025-09-28..2025-12-27", "quote": "\"value\": \"64600000\"", "paragraph_id": "0001628280-26-009585:facts:GoodwillImpairmentLoss:2025-09-28..2025-12-27:us-gaap:BusinessAcquisitionAxis=lfus:DortmundFabMember" }
```

```json
{ "id": "structure_and_disclosure_changes_basler_purchase_accounting", "what_changed": "Basler Electric was acquired on 2025-12-10/11. Net assets acquired are 350301000, including goodwill of 152343000 and intangibles of 150000000. Consideration transferred of 350300000 carries superseded_by 0001628280-26-031041, meaning a later filing also reports it. A provisional inventory adjustment of 6400000 (2025-09-28..2025-12-27) carries superseded_by 0001628280-26-050481; the 10-Q tags the same 6400000. Revenue since acquisition in fiscal 2025 is 3700000. The 10-Qs report this goodwill differently (item articulation_and_the_filed_history_basler_acquisition_goodwill_revised).", "account": "acquired goodwill and purchase accounting: Basler", "expected_direction": "up", "horizon": "acquisition date 2025-12-10", "quote": "\"value\": \"152343000\"", "paragraph_id": "0001628280-26-009585:facts:Goodwill:2025-12-10:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "liquidity_and_capital_acquisition_spend_annual", "what_changed": "Cash paid for acquisitions, net of cash acquired: 407718000 in fiscal 2025 against 0 in fiscal 2024 and 198810000 in fiscal 2023.", "account": "payments to acquire businesses", "expected_direction": "up", "horizon": "fiscal year ended 2025-12-27 against fiscal year ended 2024-12-28", "quote": "\"value\": \"407718000\"", "paragraph_id": "0001628280-26-009585:facts:PaymentsToAcquireBusinessesNetOfCashAcquired:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_noncurrent_allowance_past_due_ninety_days", "what_changed": "AllowanceForDoubtfulAccountsReceivableNoncurrent on the 90-days-or-more past-due member is 9300000 at 2025-12-27 against 3800000 at 2024-12-28. The same tag without the past-due member is 2500000 against 1600000. My input does not explain the tag beyond its name.", "account": "noncurrent receivable allowance, 90+ days past due", "expected_direction": "up", "horizon": "2025-12-27 against 2024-12-28", "quote": "\"value\": \"9300000\"", "paragraph_id": "0001628280-26-009585:facts:AllowanceForDoubtfulAccountsReceivableNoncurrent:2025-12-27:us-gaap:FinancingReceivablesPeriodPastDueAxis=us-gaap:FinancingReceivablesEqualToGreaterThan90DaysPastDueMember" }
```

```json
{ "id": "estimates_and_discretion_employee_related_accruals", "what_changed": "Current employee-related liabilities of 114662000 at 2025-12-27 against 67639000 at 2024-12-28. Total accrued liabilities are 199271000 against 148276000.", "account": "employee-related accrued liabilities", "expected_direction": "up", "horizon": "2025-12-27 against 2024-12-28", "quote": "\"value\": \"114662000\"", "paragraph_id": "0001628280-26-009585:facts:EmployeeRelatedLiabilitiesCurrent:2025-12-27" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_accrual", "what_changed": "Noncurrent loss contingency accrual of 2200000 (EUR 1800000) at 2025-12-27 against 2300000 (EUR 2200000) at 2024-12-28.", "account": "loss contingency accrual", "expected_direction": "down", "horizon": "2025-12-27 against 2024-12-28", "quote": "\"value\": \"2200000\"", "paragraph_id": "0001628280-26-009585:facts:LossContingencyAccrualCarryingValueNoncurrent:2025-12-27" }
```

```json
{ "id": "liquidity_and_capital_revolver_remaining_capacity", "what_changed": "Remaining borrowing capacity on the line of credit is 598900000 at 2025-12-27, with 100000000 drawn. Total long-term debt is 802627000 against 856114000 a year earlier.", "account": "revolving credit availability", "expected_direction": "none", "horizon": "2025-12-27", "quote": "\"value\": \"598900000\"", "paragraph_id": "0001628280-26-009585:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2025-12-27:us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember" }
```

```json
{ "id": "liquidity_and_capital_debt_maturities_second_year", "what_changed": "Scheduled long-term debt principal due in the second year after 2025-12-27 is 371250000. The next twelve months carry 96233000, the third year 111977000, the fourth year 0, the fifth year 125000000 and after the fifth year 100000000. The 8-K says the credit agreement and notes mature from 2027 to 2031.", "account": "debt maturities", "expected_direction": "none", "horizon": "maturities from 2025-12-27", "quote": "\"value\": \"371250000\"", "paragraph_id": "0001628280-26-009585:facts:LongTermDebtMaturitiesRepaymentsOfPrincipalInYearTwo:2025-12-27" }
```

### Numeric facts — 10-Q 0001628280-26-050481 (filed 2026-07-29), the report this run is about

```json
{ "id": "results_against_expectations_net_sales_reported_quarter", "what_changed": "Net sales 738781000 for 2026-03-29..2026-06-27 against 613413000 for 2025-03-30..2025-06-28; six months 1395750000 against 1167720000. By segment for the quarter: Electronics 406420000 against 335666000, Transportation 182411000 against 179400000, Industrial 149950000 against 98347000. The trend table holds no ratio for this quarter, and no pre-quarter expectation for these sales is in my input.", "account": "net sales", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"738781000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "results_against_expectations_geographic_net_sales_china_and_united_states", "what_changed": "Net sales to China 184067000 in the quarter against 146343000 a year earlier; United States 267404000 against 219480000; other countries 287310000 against 247590000. Six months: China 339970000 against 275737000.", "account": "net sales by geography", "expected_direction": "up", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"184067000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:srt:StatementGeographicalAxis=country:CN" }
```

```json
{ "id": "earnings_quality_gross_profit_reported_quarter", "what_changed": "Gross profit 306064000 in the quarter against 232054000 a year earlier, on cost of goods sold of 432717000. No gross-margin ratio for this quarter exists in my input; the trend table's newest gross_margin cell is quarters-back-1.", "account": "gross profit", "expected_direction": "up", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"306064000\"", "paragraph_id": "0001628280-26-050481:facts:GrossProfit:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_selling_general_administrative_expense_quarter", "what_changed": "Selling, general and administrative expense 120578000 in the quarter against 95517000 a year earlier.", "account": "selling, general and administrative expense", "expected_direction": "up", "horizon": "three months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"120578000\"", "paragraph_id": "0001628280-26-050481:facts:SellingGeneralAndAdministrativeExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_restructuring_and_asset_impairment_tagged_quarter", "what_changed": "Restructuring costs and asset impairment charges 20021000 in the quarter against 2506000; six months 27443000 against 11525000. Within the quarter: restructuring charges 6875000 (employee severance 5207000, other 1668000), other asset impairment charges 13146000 (Electronics 12898000, Transportation 248000, Industrial 0). By segment the quarter's total is Electronics 17585000, Transportation 1732000, Industrial 704000.", "account": "restructuring and asset impairment charges", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"20021000\"", "paragraph_id": "0001628280-26-050481:facts:RestructuringCostsAndAssetImpairmentCharges:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_long_lived_asset_impairment_quarter", "what_changed": "Impairment of long-lived assets held for use of 13100000 in the quarter, on assets not in discontinued operations. The cash-flow statement adds back asset impairment charges of 13146000 for the six months to 2026-06-27 against 136000 a year earlier. Proceeds from sale of property, plant and equipment are 9115000 against 712000. Net PP&E is 513160000 at 2026-06-27 against 540640000 at 2025-12-27.", "account": "long-lived asset impairment", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"13100000\"", "paragraph_id": "0001628280-26-050481:facts:ImpairmentOfLongLivedAssetsHeldForUse:2026-03-29..2026-06-27:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupNotDiscontinuedOperationsMember" }
```

```json
{ "id": "earnings_quality_operating_income_reported_quarter", "what_changed": "Operating income 119724000 in the quarter against 92778000; six months 220889000 against 162928000. Segment operating income totals 140081000 against 96798000; the corporate non-segment line is -20357000 against -4020000.", "account": "operating income", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"119724000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_segment_operating_income_electronics_and_industrial", "what_changed": "Electronics segment operating income 86916000 in the quarter against 49861000; Industrial 27474000 against 18863000; Transportation 25691000 against 28074000. Six months: Electronics 157195000 against 96627000, Industrial 48235000 against 31937000.", "account": "segment operating income", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"86916000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=lfus:ElectronicsSegmentMember" }
```

```json
{ "id": "results_against_expectations_net_income_and_diluted_eps_quarter", "what_changed": "Net income 89405000 in the quarter against 57342000; six months 164552000 against 100913000. Diluted EPS 3.49 against 2.30, basic EPS 3.53 against 2.32; diluted shares 25620000 against 24905000. Income before income taxes 117064000 against 78214000; income tax expense 27659000. No pre-quarter expectation for EPS is in my input.", "account": "net income and diluted EPS", "expected_direction": "up", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"89405000\"", "paragraph_id": "0001628280-26-050481:facts:NetIncomeLoss:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_tagged_quarter", "what_changed": "The 10-Q tags the quarter's effective tax rate as 0.236 against 0.267 a year earlier, and six months 0.230 against 0.270. The first-quarter 10-Q tagged 0.223 for 2025-12-28..2026-03-28.", "account": "effective income tax rate", "expected_direction": "down", "horizon": "three and six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"0.236\"", "paragraph_id": "0001628280-26-050481:facts:EffectiveIncomeTaxRateContinuingOperations:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_deferred_tax_expense_swing", "what_changed": "Deferred income tax expense of 10026000 for the six months to 2026-06-27 against a benefit of -807000 a year earlier. The 10-K reported the deferred tax valuation allowance rising to 97557000 at 2025-12-27.", "account": "deferred income tax expense", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"10026000\"", "paragraph_id": "0001628280-26-050481:facts:DeferredIncomeTaxExpenseBenefit:2025-12-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_polytronics_realized_gain", "what_changed": "The 10-Q tags a realized gain on equity securities (Polytronics) of 7400000 for the quarter. Other non-operating income is 2919000 in the quarter against 4452000. The fair-value table lists equity securities of 7676000 at 2025-12-27; the table at 2026-06-27 lists cash equivalents 567152000 and trading debt securities 27639000 and no equity-securities line.", "account": "non-operating gain on equity securities", "expected_direction": "none", "horizon": "three months ended 2026-06-27", "quote": "\"value\": \"7400000\"", "paragraph_id": "0001628280-26-050481:facts:EquitySecuritiesFvNiRealizedGainLoss:2026-03-29..2026-06-27:srt:ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=lfus:PolytronicsMember" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_six_months", "what_changed": "Net cash provided by operating activities 226474000 for the six months to 2026-06-27 against 148225000. Investing -26724000 against -89704000 (capital expenditures 33021000 against 32999000); financing -131943000 against -120543000. Cash and cash equivalents 628224000 at 2026-06-27 against 563391000 at 2025-12-27. No accruals ratio for this period exists in my input.", "account": "operating cash flow", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"226474000\"", "paragraph_id": "0001628280-26-050481:facts:NetCashProvidedByUsedInOperatingActivities:2025-12-28..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_receivable_allowance_tagged_quarter_end", "what_changed": "Allowance for doubtful accounts 86865000 at 2026-06-27 against 77073000 at 2025-12-27, on net trade receivables of 423590000. The trend table has no bad_debt_reserve_ratio cell for this date; its quarters-back-1 input was 79896000.", "account": "allowance for doubtful accounts", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"86865000\"", "paragraph_id": "0001628280-26-050481:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_tagged_quarter_end", "what_changed": "Inventory valuation reserves 80530000 at 2026-06-27 against 82695000 at 2025-12-27 and 83593000 at 2026-03-28. Net inventory 433755000 against 416472000; raw materials 198883000 against 186662000, work in process 137394000 against 131129000, finished goods 178008000 against 181376000. The trend table has no inventory_reserve_ratio cell for this date.", "account": "inventory valuation reserves", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27 and 2026-03-28", "quote": "\"value\": \"80530000\"", "paragraph_id": "0001628280-26-050481:facts:InventoryValuationReserves:2026-06-27" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_tagged_quarter_end", "what_changed": "Deferred revenue 4989000 at 2026-06-27 against 11215000 at 2025-12-27 and 6713000 at 2026-03-28. The cash-flow change in contract liabilities is -4308000 for the six months against 2844000 a year earlier. The trend table has no contract_liabilities_over_revenue cell for this quarter.", "account": "deferred revenue (contract liabilities)", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27 and 2026-03-28", "quote": "\"value\": \"4989000\"", "paragraph_id": "0001628280-26-050481:facts:DeferredRevenue:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_employee_related_accruals_quarter_end", "what_changed": "Current employee-related liabilities 107717000 at 2026-06-27 against 114662000 at 2025-12-27. Other accrued liabilities 37587000 against 29733000; total accrued liabilities 191873000 against 199271000; current restructuring reserve 5258000 against 6014000.", "account": "employee-related accrued liabilities", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"107717000\"", "paragraph_id": "0001628280-26-050481:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_tagged_quarter_end", "what_changed": "Long-term debt 629660000 at 2026-06-27 against 802627000 at 2025-12-27; current 100000000 against 96233000, noncurrent 529660000 against 706394000. By instrument: line of credit 200000000 against 100000000, unsecured term debt 0 against 266250000, notes payable 0 against 1233000. Six-month repayments: unsecured debt 66250000, long-term lines of credit 100000000; debt issuance costs paid 2169000. Remaining line-of-credit capacity 599900000 at 2026-06-27. Interest paid 13091000 against 17834000 for six months.", "account": "long-term debt", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"629660000\"", "paragraph_id": "0001628280-26-050481:facts:LongTermDebt:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_revolver_capacity_raised", "what_changed": "Maximum borrowing capacity of the unsecured revolving credit facility is tagged 800000000 at 2026-03-12, against 700000000 at 2022-06-30. The unsecured capacity tagged without the revolving member at 2026-03-12 is 300000000. The SOFR spread range is 0.0100 to 0.0175 and the unused commitment fee 0.0010 to 0.00175. The filing-history list shows an Item 1.01/2.03 8-K filed 2026-03-13.", "account": "revolving credit facility capacity", "expected_direction": "up", "horizon": "2026-03-12 against 2022-06-30", "quote": "\"value\": \"800000000\"", "paragraph_id": "0001628280-26-050481:facts:LineOfCreditFacilityMaximumBorrowingCapacity:2026-03-12:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember,us-gaap:LongtermDebtTypeAxis=us-gaap:UnsecuredDebtMember" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_balance_quarter_end", "what_changed": "Goodwill 1203861000 at 2026-06-27 against 1211411000 at 2025-12-27. The six-month roll-forward tags goodwill acquired of 8634000 (all Industrial) and foreign-currency translation of -16184000. Accumulated impairment is 388216000 against 396982000. By segment at 2026-06-27: Electronics 711678000, Transportation 196124000, Industrial 296059000.", "account": "goodwill", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"1203861000\"", "paragraph_id": "0001628280-26-050481:facts:Goodwill:2026-06-27" }
```

```json
{ "id": "articulation_and_the_filed_history_basler_acquisition_goodwill_revised", "what_changed": "Restated prior value, from the filed history. The 10-K (filed 2026-02-19) tags Basler Electric acquisition-date goodwill at 2025-12-10 as 152343000. The first-quarter 10-Q (0001628280-26-031041) and this 10-Q tag it at 2025-12-11 as 160977000. The purchase-price allocation in this 10-Q is: intangibles 145000000 (the 10-K had 150000000), net assets 353119000 (the 10-K had 350301000), inventory 20703000, receivables 14739000, PP&E 21532000. This 10-Q tags six-month measurement-period adjustments: goodwill 8600000, intangibles -5000000.0, inventory -2600000, PP&E -1700000. Python printed no restatement trace, and the two context dates differ by one day. I state both filed values without computing a difference.", "account": "Basler acquisition-date goodwill", "expected_direction": "up", "horizon": "acquisition date, as filed 2026-02-19 against as filed 2026-05-06 and 2026-07-29", "quote": "\"value\": \"160977000\"", "paragraph_id": "0001628280-26-050481:facts:Goodwill:2025-12-11:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_measurement_period_intangibles_adjustment", "what_changed": "Measurement-period adjustment to Basler acquired intangibles of -5000000.0 for the six months to 2026-06-27, alongside inventory -2600000, PP&E -1700000 and goodwill 8600000. Basler net intangibles are 145000000 at 2026-06-27: customer lists, trademarks and trade names 130000000, patents and developed technology 15000000.", "account": "acquired intangibles: Basler measurement-period adjustment", "expected_direction": "down", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"-5000000.0\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationProvisionalInformationInitialAccountingIncompleteAdjustmentIntangibles:2025-12-28..2026-06-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "structure_and_disclosure_changes_pro_forma_revenue_basler_and_dortmund", "what_changed": "Pro forma revenue including Basler and Dortmund Fab is 648941000 for the quarter ended 2025-06-28, against reported 613413000. For the quarter ended 2026-06-27 pro forma equals reported, at 738781000. Pro forma net income for the quarter ended 2025-06-28 is 60141000, against reported 57342000. The 10-Q also tags Basler's revenue at the acquisition date as 130000000.", "account": "pro forma revenue", "expected_direction": "up", "horizon": "three months ended 2026-06-27 against pro forma three months ended 2025-06-28", "quote": "\"value\": \"648941000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessAcquisitionsProFormaRevenue:2025-03-30..2025-06-28:us-gaap:BusinessAcquisitionAxis=lfus:BaslerAndDortmundFabMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_pension_expense_forecast_moved", "what_changed": "This 10-Q tags a forecast subsequent-event pension expense range of 6000000 (minimum) to 8000000 (maximum) for 2026-12-27..2027-03-31. The first-quarter 10-Q tagged the same range for 2026-06-28..2026-09-26, so the forecast period has moved later. My input does not state the reason.", "account": "forecast pension expense (subsequent event)", "expected_direction": "none", "horizon": "2026-12-27..2027-03-31, as tagged in the 10-Q filed 2026-07-29", "quote": "\"value\": \"6000000\"", "paragraph_id": "0001628280-26-050481:facts:PensionExpense:2026-12-27..2027-03-31:srt:RangeAxis=srt:MinimumMember,srt:StatementScenarioAxis=srt:ScenarioForecastMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_purchases_atec", "what_changed": "Purchases from ATEC (a 24% equity-method investee) are 5000000.0 for the six months to 2026-06-27 against 3300000 a year earlier; 2800000 in Q2-26 against 1400000. Accounts payable to ATEC is 1200000 at 2026-06-27 against 2100000 at 2025-12-27. Powersem (45%): purchases 900000 year to date against 1100000; sales to Powersem 700000 against 600000. EBTech (15%): purchases 200000 against 700000.", "account": "related-party purchases", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against 2025-06-28", "quote": "\"value\": \"5000000.0\"", "paragraph_id": "0001628280-26-050481:facts:RelatedPartyTransactionPurchasesFromRelatedParty:2025-12-28..2026-06-27:srt:CounterpartyNameAxis=lfus:ATECMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

## Seen in the notes

No item is placed here, because no fact in my input carries a marker saying its element sat inside a note.

The fields present on facts in `input_numbers.json` are:
- id, paragraph_id, tag, prefix, namespace
- context (start/end or instant, segment, and on some facts typed_segment), context_ref
- unit, decimals, value, number, nil
- form, source_accession, filing_date
- on some facts, superseded_by

None of these fields says whether the element sat inside a note. I did not judge note membership myself. Every fact item above sits under "Seen in the statements" for that reason. Some of those items come from tables that are plausibly note disclosures, for example:
- purchase-price allocation
- goodwill roll-forward
- debt schedule
- restructuring
- related parties
- pension

If a later input carries the marker, those items can be moved here without re-reading.
