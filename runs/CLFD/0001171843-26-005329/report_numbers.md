<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# CLFD — numbers report, 10-Q 0001171843-26-005329 (period ended 2026-06-30)

## What this report rests on, and what it could not reach

- `input_trends.json`: read in full (4640 lines).
- `input_8k.md`: read in full (Item 2.02 release 0001171843-26-005241 and the 8-K item-code list).
- `input_prior_predictions.md`: read in full. It says no prior run exists, so there are no prior flags to carry forward.
- `input_numbers.json`: **not read in full.** The file has 64838 lines (about 2.3 MB). Its top-level keys are `ticker`, `cutoff`, `documents` (three filings: 10-K 0001171843-25-007594, 10-Q 0001171843-26-003126, 10-Q 0001171843-26-005329) and `facts`. I read lines 1–2099 and 63500–64838. Lines 2100–63499 were not read, because the read tool reported that the next chunk no longer fit in the context left. Whatever those lines hold is not covered here.
- No prices, abnormal returns, short interest, other-company files, prior probabilities or outcome windows appear in what I read.
- **Articulation checks:** my input has no articulation-check section, so no articulation gap is reported.
- **Restatement traces:** my input has no restatement-trace section. In the facts I read, some 10-K facts carry `"superseded_by": "0001171843-26-005329"`. That field says a later filing re-reported the fact. It does not say whether the value changed, and no trace in my input says so. No restated prior value is reported.
- **Fourth-quarter derivation:** the trend table says fiscal fourth quarters are derived by src/fourth_quarter.py, but no derived fourth-quarter figures are in my input. No fourth-quarter number exists here.
- **Periods the record does not reach:** quarters-back-3 (target end 2025-09-30) and quarters-back-7 (target end 2024-10-01) have no cells. The reason both periods give: "no quarter ending within 20 days of 2025-09-30 [2024-10-01 for quarters-back-7] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
- **Research-and-development capitalization block (years-back-0):** it prints no `paragraph_id` of its own, so I cannot quote it as an item. Its printed values are `book_value_with_rnd_capitalized` 263260600.0 and `earnings_with_rnd_capitalized` -7332000.0. `capitalized_development_cost` is missing because the record tags no us-gaap:CapitalizedComputerSoftwareAdditions in any period.
- **Short history:** the quarterly history holds 6 filled quarters and the annual history 5 filled years. On the operating-cash-flow concept now used, `accruals_over_total_assets` has a single comparable quarter and a single comparable year. A trend claim on accruals is **insufficient**.
- Direction convention: `expected_direction` gives the sign of the change printed against the same period one year earlier (year_over_year). It is "none" where the change is printed as 0.0 or no change is printed.

## Seen in the statements

```json
[
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
    "what_changed": "Inventory reserve ratio (InventoryValuationReserves 12704000.0 over InventoryNet 33391000.0) is printed as 0.3804618010841245. The change against quarters-back-1 is printed as 0.07523428212421113 and against quarters-back-4 as 0.10531436745251321. It is the highest of the 6 filled quarters.",
    "account": "inventory valuation reserve / inventory, net",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:inventory_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_quarterly",
    "what_changed": "Days sales of inventory (InventoryNet 33391000.0, CostOfRevenue 29920000.0) is printed as 101.55685160427807. The change against quarters-back-1 is printed as -41.48232187828758 and against quarters-back-4 as -93.4877275256713. It is the lowest of the 6 filled quarters.",
    "account": "inventory, net / cost of revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:days_sales_of_inventory:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_gross_margin_quarterly",
    "what_changed": "Gross margin (RevenueFromContractWithCustomerExcludingAssessedTax 43864000.0, CostOfRevenue 29920000.0) is printed as 0.31789166514681744. The change against quarters-back-1 is printed as -0.006640916051751933 and against quarters-back-4 as -0.03499183375654985. It is the second lowest of the 6 filled quarters.",
    "account": "revenue and cost of revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:gross_margin:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_quarterly",
    "what_changed": "Days sales outstanding (AccountsReceivableNetCurrent 22055000.0, revenue 43864000.0) is printed as 45.755175086631404. The change against quarters-back-1 is printed as -8.84777335918291 and against quarters-back-4 as -16.73673563456586. It is the third lowest of the 6 filled quarters.",
    "account": "accounts receivable, net / revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:days_sales_outstanding:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_quarterly",
    "what_changed": "Receivables over revenue (22055000.0 over 43864000.0) is printed as 0.5028041218311143. The change against quarters-back-1 is printed as -0.10389530534460023 and against quarters-back-4 as -0.18392017180841602. It is the third lowest of the 6 filled quarters.",
    "account": "accounts receivable, net / revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:receivables_over_revenue:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_soft_asset_share_quarterly",
    "what_changed": "Soft asset share (Assets 267091000.0, PropertyPlantAndEquipmentNet 9265000.0, CashAndCashEquivalentsAtCarryingValue 20449000.0) is printed as 0.8887495273146605. The change against quarters-back-1 is printed as -0.03969966770558253 and against quarters-back-4 as 0.05910636376726763. It is the third highest of the 6 filled quarters.",
    "account": "total assets less PP&E and cash",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:soft_asset_share:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
    "what_changed": "Bad debt reserve ratio (AllowanceForDoubtfulAccountsReceivableCurrent 0.0, receivables 22055000.0) is printed as 0.0. The change against quarters-back-1 and against quarters-back-4 is printed as 0.0. The value is the same in all 6 filled quarters, so the allowance is tagged as zero throughout.",
    "account": "allowance for doubtful accounts",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30, against quarters-back-1 and quarters-back-4",
    "quote": "\"position_in_history\": \"the same value in all 6 filled quarters\"",
    "paragraph_id": "0001171843-26-005329:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_quarterly",
    "what_changed": "insufficient: accruals over total assets is not filled for this quarter because no quarterly operating-cash-flow row exists for 2026-04-01..2026-06-30. No value or change exists.",
    "account": "net income less operating cash flow / total assets",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
    "what_changed": "insufficient: contract liabilities over revenue cannot be filled because the record tags no contract-liability or deferred-revenue concept in any period. No value or change exists.",
    "account": "contract liabilities / deferred revenue",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"missing\": \"no row for contract_liabilities: the companyfacts record tags none of us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001171843-26-005329:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30"
  },
  {
    "id": "results_against_expectations_non_gaap_gap_quarterly",
    "what_changed": "insufficient: the non-GAAP gap cannot be filled because companyfacts carries no non-GAAP measure. No value or change exists.",
    "account": "non-GAAP net income against GAAP net income",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001171843-26-005329:trends:non_gaap_gap:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
    "what_changed": "insufficient: the warranty reserve ratio cannot be filled because the record tags no product-warranty accrual in any period. No value or change exists.",
    "account": "product warranty accrual",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001171843-26-005329:trends:warranty_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
    "what_changed": "Inventory reserve ratio for the fiscal year (InventoryValuationReserves 12438000.0 over InventoryNet 42031000.0) is printed as 0.2959244367252742. The change against years-back-1 is printed as 0.033713227369883414. It is the highest of the 5 filled years.",
    "account": "inventory valuation reserve / inventory, net",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:inventory_reserve_ratio:2024-10-01..2025-09-30"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_annual",
    "what_changed": "Days sales of inventory for the fiscal year (InventoryNet 42031000.0, CostOfRevenue 99597000.0) is printed as 154.03390664377443. The change against years-back-1 is printed as -51.85187468613603. It is the second lowest of the 5 filled years.",
    "account": "inventory, net / cost of revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:days_sales_of_inventory:2024-10-01..2025-09-30"
  },
  {
    "id": "earnings_quality_gross_margin_annual",
    "what_changed": "Gross margin for the fiscal year (revenue 150134000.0, CostOfRevenue 99597000.0) is printed as 0.3366126260540584. The change against years-back-1 is printed as 0.13077196601328367. It is the second lowest of the 5 filled years.",
    "account": "revenue and cost of revenue",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:gross_margin:2024-10-01..2025-09-30"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_annual",
    "what_changed": "Days sales outstanding for the fiscal year (AccountsReceivableNetCurrent 17991000.0, revenue 150134000.0) is printed as 43.73902646968708. The change against years-back-1 is printed as 3.3900681363537473. It is the second lowest of the 5 filled years.",
    "account": "accounts receivable, net / revenue",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:days_sales_outstanding:2024-10-01..2025-09-30"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_annual",
    "what_changed": "Receivables over revenue for the fiscal year (17991000.0 over 150134000.0) is printed as 0.1198329492320194. The change against years-back-1 is printed as 0.009589893676463845. It is the second lowest of the 5 filled years.",
    "account": "accounts receivable, net / revenue",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:receivables_over_revenue:2024-10-01..2025-09-30"
  },
  {
    "id": "earnings_quality_soft_asset_share_annual",
    "what_changed": "Soft asset share at fiscal year-end (Assets 306173000.0, PP&E 9682000.0, cash 21493000.0) is printed as 0.8981784807935383. The change against years-back-1 is printed as -0.00660623096603663. It is the second highest of the 5 filled years.",
    "account": "total assets less PP&E and cash",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:soft_asset_share:2024-10-01..2025-09-30"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
    "what_changed": "Bad debt reserve ratio at fiscal year-end (allowance 0.0, receivables 17991000.0) is printed as 0.0. The change against years-back-1 is printed as 0.0. It is tied for lowest of the 5 filled years.",
    "account": "allowance for doubtful accounts",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2025-09-30, against years-back-1",
    "quote": "\"position_in_history\": \"tied for lowest of the 5 filled years\"",
    "paragraph_id": "0001171843-26-005329:trends:bad_debt_reserve_ratio:2024-10-01..2025-09-30"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_annual",
    "what_changed": "Accruals over total assets for the fiscal year (NetIncomeLoss -8050000.0, NetCashProvidedByUsedInOperatingActivitiesContinuingOperations 26553000.0, Assets 306173000.0) is printed as -0.11301780366002227. No change against years-back-1 is printed because that year rests on a different operating-cash-flow concept. It is the only filled year on the same concepts, so a trend claim is insufficient.",
    "account": "net income less operating cash flow / total assets",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2025-09-30",
    "quote": "\"position_in_history\": \"the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2024-10-01..2025-09-30"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
    "what_changed": "insufficient: contract liabilities over revenue cannot be filled for the fiscal year because the record tags no contract-liability or deferred-revenue concept in any period. No value or change exists.",
    "account": "contract liabilities / deferred revenue",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2025-09-30",
    "quote": "\"missing\": \"no row for contract_liabilities: the companyfacts record tags none of us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001171843-26-005329:trends:contract_liabilities_over_revenue:2024-10-01..2025-09-30"
  },
  {
    "id": "results_against_expectations_non_gaap_gap_annual",
    "what_changed": "insufficient: the non-GAAP gap cannot be filled for the fiscal year because companyfacts carries no non-GAAP measure. No value or change exists.",
    "account": "non-GAAP net income against GAAP net income",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2025-09-30",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001171843-26-005329:trends:non_gaap_gap:2024-10-01..2025-09-30"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
    "what_changed": "insufficient: the warranty reserve ratio cannot be filled for the fiscal year because the record tags no product-warranty accrual in any period. No value or change exists.",
    "account": "product warranty accrual",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2025-09-30",
    "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001171843-26-005329:trends:warranty_reserve_ratio:2024-10-01..2025-09-30"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_operating_cash_flow_concept_change_annual",
    "what_changed": "Change of tag: operating cash flow rests on us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations in years-back-0 and on us-gaap:NetCashProvidedByUsedInOperatingActivities in years-back-1. The table does not compare the two years.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2025-09-30 against years-back-1",
    "quote": "\"reason\": \"accruals_over_total_assets rests on a different concept in each period, so the difference would not be a change",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2024-10-01..2025-09-30"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_operating_cash_flow_concept_change_quarterly",
    "what_changed": "Change of tag: operating cash flow rests on us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations in quarters-back-2 (value printed 0.003081514642790524) and on us-gaap:NetCashProvidedByUsedInOperatingActivities in quarters-back-6. The table does not compare the two quarters.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "quarters-back-2 against quarters-back-6",
    "quote": "\"reason\": \"accruals_over_total_assets rests on a different concept in each period, so the difference would not be a change",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2025-10-01..2025-12-31"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_concept_change_earlier_quarter",
    "what_changed": "Change of tag: the quarters-back-6 accruals cell (value printed -0.029865118886653694) rests on us-gaap:NetCashProvidedByUsedInOperatingActivities. Its position says the other filled quarter rests on a different concept and is not compared.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "quarters-back-6",
    "quote": "\"position_in_history\": \"the only filled quarter on the same concepts; 1 other filled quarter rests on a different concept and is not compared\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2024-10-01..2024-12-31"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_concept_change_lowest_earlier_year",
    "what_changed": "Change of tag: the years-back-1 accruals cell (value printed -0.10998651970501942, change against years-back-2 printed -0.14967238564110685) rests on us-gaap:NetCashProvidedByUsedInOperatingActivities. Its position says one other filled year rests on a different concept and is not compared.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "years-back-1",
    "quote": "\"position_in_history\": \"lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2023-10-01..2024-09-30"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_concept_change_second_lowest_earlier_year",
    "what_changed": "Change of tag: the years-back-2 accruals cell (value printed 0.039685865936087444) rests on us-gaap:NetCashProvidedByUsedInOperatingActivities. Its position says one other filled year rests on a different concept and is not compared.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "years-back-2",
    "quote": "\"position_in_history\": \"second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2022-10-01..2023-09-30"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_concept_change_highest_earlier_year",
    "what_changed": "Change of tag: the years-back-3 accruals cell (value printed 0.20557941412660172) rests on us-gaap:NetCashProvidedByUsedInOperatingActivities. Its position says one other filled year rests on a different concept and is not compared.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "years-back-3",
    "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2021-10-01..2022-09-30"
  },
  {
    "id": "articulation_and_the_filed_history_accruals_concept_change_second_highest_earlier_year",
    "what_changed": "Change of tag: the years-back-4 accruals cell (value printed 0.07484651857264259) rests on us-gaap:NetCashProvidedByUsedInOperatingActivities. Its position says one other filled year rests on a different concept and is not compared.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "years-back-4",
    "quote": "\"position_in_history\": \"second highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
    "paragraph_id": "0001171843-26-005329:trends:accruals_over_total_assets:2020-10-01..2021-09-30"
  }
]
```

## Seen in the notes

No items. None of the facts I read in `input_numbers.json` (lines 1–2099 and 63500–64838) carries a field marking whether its element sat inside a note. Their fields are `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and sometimes `superseded_by`. Without that marker this heading has nothing to hold, and I have not tried to judge note placement myself. Lines 2100–63499 were not read, so whether any fact there carries the marker is unknown.
