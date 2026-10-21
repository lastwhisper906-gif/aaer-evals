<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# NTAP — numbers reader — 10-Q 0001193125-26-380207 (quarter ended 2026-07-31)

## Before the items

- **Inputs read in full.** `input_trends.json`, `input_numbers.json` (three filings: 10-Q 0001193125-26-076622, 10-K 0001193125-26-259683 and the current 10-Q 0001193125-26-380207), `input_8k.md` (0001002047-26-000003) and `input_prior_predictions.md`.
- **No forbidden inputs were present.** The directory held no prices, abnormal returns or short interest, no other company's files, no prior run's probability and no outcome window.
- **No prior flags.** `input_prior_predictions.md` says: "None on record."
- **Quarters with no cells: quarters-back-1 and quarters-back-5.** quarters-back-1 has target end 2026-05-01. Its reason reads: "no quarter ending within 20 days of 2026-05-01 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". quarters-back-5 has target end 2025-05-02 and gives the same reason for that date.
  - Neither quarter has any number.
  - As a result, no quarter-over-quarter change exists for any metric in quarters-back-0.
- **Inputs missing from the directory.**
  - **Fourth-quarter derivation:** absent, so no fourth-quarter figure exists for me.
  - **Articulation checks:** absent, so I can report no articulation gap.
  - **Restatement traces:** absent. Each restated value reported below was found by reading two filings' printed facts for the same date side by side; the earlier fact carries a `superseded_by` marker. I did no arithmetic.
- **R&D-capitalized baselines are not itemized.** The `research_and_development_capitalized` block in `input_trends.json` prints its values without a `paragraph_id`, so nothing in it can be quoted. Its `capitalized_development_cost` is missing in every year; the record tags none of us-gaap:CapitalizedComputerSoftwareAdditions.
- **Every metric is in the items.** All 11 metrics in quarters-back-0 and in years-back-0 have an item below. A metric the table could not fill is marked `insufficient`.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_accruals_over_total_assets_quarterly",
    "what_changed": "Accruals over total assets for 2026-04-25..2026-07-31 is -0.011684162482884527 (inputs: net income 375000000.0, operating cash flow 503000000.0, assets 10955000000.0). Year-over-year change against quarters-back-4 is 0.03377507917431146. No quarter-over-quarter change exists: 'accruals_over_total_assets is not filled in quarters-back-1'. Position: highest of the 2 filled quarters. Only two quarters are filled because operating cash flow has no row for quarters-back-2, -3, -6 and -7. A quarterly trend claim is therefore insufficient.",
    "account": "accruals over total assets ((net income - operating cash flow) / assets)",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "highest of the 2 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:accruals_over_total_assets:2026-04-25..2026-07-31"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
    "what_changed": "insufficient. The table has no allowance row for 2026-07-31, so it cannot fill the bad-debt reserve ratio for the quarter. Neither the quarter-over-quarter nor the year-over-year change exists ('bad_debt_reserve_ratio is not filled in quarters-back-0'). The ratio is filled in none of the periods the table holds.",
    "account": "allowance for doubtful accounts / receivables",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-07-31",
    "quote": "no row for bad_debt_allowance in 2026-07-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period",
    "paragraph_id": "0001193125-26-380207:trends:bad_debt_reserve_ratio:2026-04-25..2026-07-31"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
    "what_changed": "Contract liabilities over revenue for the quarter is 1.1120987654320988 (current contract liabilities 2252000000.0, quarterly revenue 2025000000.0). Year-over-year change against quarters-back-4 is -0.3439628125024745. No quarter-over-quarter change exists: 'contract_liabilities_over_revenue is not filled in quarters-back-1'. Position: lowest of the 6 filled quarters.",
    "account": "current contract liabilities (short-term deferred revenue) / revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "lowest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:contract_liabilities_over_revenue:2026-04-25..2026-07-31"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_quarterly",
    "what_changed": "Days sales of inventory for the 98-day quarter is 60.64356435643564 (inventory 375000000.0, cost of revenue 606000000.0). Year-over-year change against quarters-back-4 is 34.389768260990955. No quarter-over-quarter change exists: 'days_sales_of_inventory is not filled in quarters-back-1'. Position: highest of the 6 filled quarters.",
    "account": "inventory (days sales of inventory)",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "highest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:days_sales_of_inventory:2026-04-25..2026-07-31"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_quarterly",
    "what_changed": "Days sales outstanding for the quarter is 46.74962962962963 (receivables 966000000.0, revenue 2025000000.0). Year-over-year change against quarters-back-4 is 0.8118490010215567. No quarter-over-quarter change exists: 'days_sales_outstanding is not filled in quarters-back-1'. Position: second lowest of the 6 filled quarters.",
    "account": "accounts receivable (days sales outstanding)",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "second lowest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:days_sales_outstanding:2026-04-25..2026-07-31"
  },
  {
    "id": "earnings_quality_gross_margin_quarterly",
    "what_changed": "Gross margin for the quarter is 0.7007407407407408 (revenue 2025000000.0, cost of revenue 606000000.0). Year-over-year change against quarters-back-4 is -0.0035568859430308297. No quarter-over-quarter change exists: 'gross_margin is not filled in quarters-back-1'. Position: second lowest of the 6 filled quarters.",
    "account": "gross margin",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "second lowest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:gross_margin:2026-04-25..2026-07-31"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
    "what_changed": "insufficient. The record tags no inventory valuation reserve in any period, so the table cannot fill the inventory reserve ratio for the quarter. Neither change exists ('inventory_reserve_ratio is not filled in quarters-back-0'). The ratio is filled in none of the periods the table holds.",
    "account": "inventory reserve / inventory",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-07-31",
    "quote": "no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period",
    "paragraph_id": "0001193125-26-380207:trends:inventory_reserve_ratio:2026-04-25..2026-07-31"
  },
  {
    "id": "results_against_expectations_non_gaap_gap_quarterly",
    "what_changed": "insufficient. The record carries no non-GAAP concept, so the table cannot fill the GAAP to non-GAAP earnings gap for the quarter. Neither change exists ('non_gaap_gap is not filled in quarters-back-0'). The release prints GAAP and non-GAAP net income separately, but no computed gap exists in my input.",
    "account": "gap between GAAP and non-GAAP net income",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-07-31",
    "quote": "no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only",
    "paragraph_id": "0001193125-26-380207:trends:non_gaap_gap:2026-04-25..2026-07-31"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_quarterly",
    "what_changed": "Receivables over revenue for the quarter is 0.47703703703703704 (receivables 966000000.0, revenue 2025000000.0). Year-over-year change against quarters-back-4 is -0.027773739101513262. No quarter-over-quarter change exists: 'receivables_over_revenue is not filled in quarters-back-1'. Position: lowest of the 6 filled quarters.",
    "account": "accounts receivable / revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "lowest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:receivables_over_revenue:2026-04-25..2026-07-31"
  },
  {
    "id": "earnings_quality_soft_asset_share_quarterly",
    "what_changed": "Soft asset share for the quarter is 0.7958922866271109 (assets 10955000000.0, cash 1573000000.0, PP&E 663000000.0). Year-over-year change against quarters-back-4 is 0.0701974834449639. No quarter-over-quarter change exists: 'soft_asset_share is not filled in quarters-back-1'. Position: highest of the 6 filled quarters.",
    "account": "soft assets ((assets - PP&E - cash) / assets)",
    "expected_direction": "up",
    "horizon": "balance at 2026-07-31 against balance at 2025-07-25",
    "quote": "highest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:soft_asset_share:2026-04-25..2026-07-31"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
    "what_changed": "Warranty reserve ratio for the quarter is 0.013333333333333334 (current warranty accrual 27000000.0 at 2026-07-31, quarterly revenue 2025000000.0). Year-over-year change against quarters-back-4 is 0.0024289074192858674. No quarter-over-quarter change exists: 'warranty_reserve_ratio is not filled in quarters-back-1'. Position: highest of the 6 filled quarters.",
    "account": "current product warranty accrual / revenue",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "highest of the 6 filled quarters",
    "paragraph_id": "0001193125-26-380207:trends:warranty_reserve_ratio:2026-04-25..2026-07-31"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_annual",
    "what_changed": "Accruals over total assets for fiscal 2025-04-26..2026-04-24 is -0.07362248696947134 (inputs: net income 1276000000.0, operating cash flow 2067000000.0, assets 10744000000.0). Year-over-year change against years-back-1 is -0.04405582338266546. No quarter-over-quarter change exists: 'an annual period has no preceding quarter'. Position: lowest of the 5 filled years.",
    "account": "accruals over total assets ((net income - operating cash flow) / assets)",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "lowest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:accruals_over_total_assets:2025-04-26..2026-04-24"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
    "what_changed": "insufficient. The table has no allowance row for 2026-04-24, so it cannot fill the bad-debt reserve ratio for the fiscal year. No year-over-year change exists ('bad_debt_reserve_ratio is not filled in years-back-0'). None of the five years is filled.",
    "account": "allowance for doubtful accounts / receivables",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-04-24",
    "quote": "no row for bad_debt_allowance in 2026-04-24: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period",
    "paragraph_id": "0001193125-26-380207:trends:bad_debt_reserve_ratio:2025-04-26..2026-04-24"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
    "what_changed": "Contract liabilities over revenue for the fiscal year is 0.33501805054151623 (current contract liabilities 2320000000.0 at 2026-04-24, annual revenue 6925000000.0). Year-over-year change against years-back-1 is -0.01175614300687089. Position: lowest of the 5 filled years.",
    "account": "current contract liabilities (short-term deferred revenue) / revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "lowest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:contract_liabilities_over_revenue:2025-04-26..2026-04-24"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_annual",
    "what_changed": "Days sales of inventory for the 364-day fiscal year is 35.57354392892399 (inventory 198000000.0, cost of revenue 2026000000.0). Year-over-year change against years-back-1 is 1.0130538829821845. Position: second highest of the 5 filled years.",
    "account": "inventory (days sales of inventory)",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "second highest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:days_sales_of_inventory:2025-04-26..2026-04-24"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_annual",
    "what_changed": "Days sales outstanding for the fiscal year is 67.59624548736463 (receivables 1286000000.0, revenue 6925000000.0). Year-over-year change against years-back-1 is -1.4153187244430399. Position: third highest of the 5 filled years.",
    "account": "accounts receivable (days sales outstanding)",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "third highest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:days_sales_outstanding:2025-04-26..2026-04-24"
  },
  {
    "id": "earnings_quality_gross_margin_annual",
    "what_changed": "Gross margin for the fiscal year is 0.7074368231046931 (revenue 6925000000.0, cost of revenue 2026000000.0). Year-over-year change against years-back-1 is 0.005519598515526969. Position: highest of the 5 filled years.",
    "account": "gross margin",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "highest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:gross_margin:2025-04-26..2026-04-24"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
    "what_changed": "insufficient. The record tags no inventory valuation reserve in any period, so the table cannot fill the inventory reserve ratio for the fiscal year. No year-over-year change exists ('inventory_reserve_ratio is not filled in years-back-0').",
    "account": "inventory reserve / inventory",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-04-24",
    "quote": "no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period",
    "paragraph_id": "0001193125-26-380207:trends:inventory_reserve_ratio:2025-04-26..2026-04-24"
  },
  {
    "id": "results_against_expectations_non_gaap_gap_annual",
    "what_changed": "insufficient. The record carries no non-GAAP concept, so the table cannot fill the GAAP to non-GAAP gap for the fiscal year. No year-over-year change exists ('non_gaap_gap is not filled in years-back-0').",
    "account": "gap between GAAP and non-GAAP net income",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-04-24",
    "quote": "no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only",
    "paragraph_id": "0001193125-26-380207:trends:non_gaap_gap:2025-04-26..2026-04-24"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_annual",
    "what_changed": "Receivables over revenue for the fiscal year is 0.1857039711191336 (receivables 1286000000.0, revenue 6925000000.0). Year-over-year change against years-back-1 is -0.0038882382539643934. Position: third highest of the 5 filled years.",
    "account": "accounts receivable / revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "third highest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:receivables_over_revenue:2025-04-26..2026-04-24"
  },
  {
    "id": "earnings_quality_soft_asset_share_annual",
    "what_changed": "Soft asset share at fiscal year-end is 0.7522338049143709 (assets 10744000000.0, cash 2070000000.0, PP&E 592000000.0). Year-over-year change against years-back-1 is 0.057602002271850306. Position: highest of the 5 filled years.",
    "account": "soft assets ((assets - PP&E - cash) / assets)",
    "expected_direction": "up",
    "horizon": "balance at 2026-04-24 against balance at 2025-04-25",
    "quote": "highest of the 5 filled years",
    "paragraph_id": "0001193125-26-380207:trends:soft_asset_share:2025-04-26..2026-04-24"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
    "what_changed": "Warranty reserve ratio for the fiscal year is 0.004187725631768953 (current warranty accrual 29000000.0 at 2026-04-24, annual revenue 6925000000.0). Year-over-year change against years-back-1 is -0.01802773389348972. The years-back-1 cell rests on the restated warranty accrual of 146000000.0 at 2025-04-25 from the 10-K; the earlier 10-Q printed 18000000 for that date. The position compares 4 years on the same concept, and one year on a different concept is not compared.",
    "account": "current product warranty accrual / revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-04-24 against fiscal year ended 2025-04-25",
    "quote": "second highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared",
    "paragraph_id": "0001193125-26-380207:trends:warranty_reserve_ratio:2025-04-26..2026-04-24"
  },
  {
    "id": "structure_and_disclosure_changes_warranty_accrual_concept_changed_between_years",
    "what_changed": "The warranty accrual input changes concept. It is us-gaap:StandardProductWarrantyAccrualCurrent (current portion) in years-back-3 and later, and us-gaap:StandardProductWarrantyAccrual (whole accrual) in years-back-4. The table therefore prints no year-over-year change for years-back-3 (value 0.002672115686890915). It also leaves years-back-4 out of every later year's position.",
    "account": "product warranty accrual",
    "expected_direction": "none",
    "horizon": "fiscal years ended 2022-04-29 and 2023-04-28",
    "quote": "warranty_accrual: us-gaap:StandardProductWarrantyAccrualCurrent in years-back-3 and us-gaap:StandardProductWarrantyAccrual in years-back-4",
    "paragraph_id": "0001193125-26-380207:trends:warranty_reserve_ratio:2022-04-30..2023-04-28"
  },
  {
    "id": "structure_and_disclosure_changes_warranty_accrual_oldest_year_on_other_concept",
    "what_changed": "The years-back-4 warranty reserve ratio is 0.00411522633744856. It rests on us-gaap:StandardProductWarrantyAccrual (26000000.0, from filing 0000950170-22-011708) and is the only filled year on that concept, so it is not compared with the four later years.",
    "account": "product warranty accrual",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2022-04-29",
    "quote": "the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared",
    "paragraph_id": "0001193125-26-380207:trends:warranty_reserve_ratio:2021-05-01..2022-04-29"
  },
  {
    "id": "articulation_and_the_filed_history_warranty_accrual_earlier_quarterly_report_value",
    "what_changed": "Restated prior value. The 10-Q filed 2026-02-26 (0001193125-26-076622) reported the current product warranty accrual at 2025-04-25 as 18000000. The fact is marked superseded by the 10-K 0001193125-26-259683, which reports 146000000 for the same date. The same 10-Q also printed a noncurrent warranty accrual of 9000000 at that date. No restatement trace exists in the input to explain the difference.",
    "account": "current product warranty accrual",
    "expected_direction": "up",
    "horizon": "balance at 2025-04-25, as filed 2026-02-26 against as filed 2026-06-05",
    "quote": "18000000",
    "paragraph_id": "0001193125-26-076622:facts:StandardProductWarrantyAccrualCurrent:2025-04-25"
  },
  {
    "id": "articulation_and_the_filed_history_warranty_accrual_annual_report_restated_value",
    "what_changed": "Restated prior value. The 10-K filed 2026-06-05 reports the current product warranty accrual at 2025-04-25 as 146000000, where the 10-Q filed 2026-02-26 printed 18000000. The 10-K's 2026-04-24 value is 29000000, matching the current 10-Q's comparative; the current 10-Q prints 27000000 at 2026-07-31. The trend table's years-back-1 warranty cell uses this restated 2025-04-25 value.",
    "account": "current product warranty accrual",
    "expected_direction": "up",
    "horizon": "balance at 2025-04-25, as filed 2026-06-05",
    "quote": "146000000",
    "paragraph_id": "0001193125-26-259683:facts:StandardProductWarrantyAccrualCurrent:2025-04-25"
  },
  {
    "id": "articulation_and_the_filed_history_warranty_ratio_prior_year_rests_on_restated_value",
    "what_changed": "The years-back-1 warranty reserve ratio is 0.022215459525258673. It is built on input 0001193125-26-259683:facts:StandardProductWarrantyAccrualCurrent:2025-04-25 (146000000.0), the restated value, not the 18000000 the earlier 10-Q filed for that date. Two things rest on the restated figure: this year's place as the highest of the comparable years, and the years-back-0 change of -0.01802773389348972. Its own year-over-year change against years-back-2 is 0.019343730105986178.",
    "account": "current product warranty accrual / revenue",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2025-04-25",
    "quote": "highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared",
    "paragraph_id": "0001193125-26-380207:trends:warranty_reserve_ratio:2024-04-27..2025-04-25"
  },
  {
    "id": "articulation_and_the_filed_history_other_accrued_liabilities_earlier_quarterly_report_value",
    "what_changed": "Restated prior value. The 10-Q filed 2026-02-26 reported other accrued liabilities at 2025-04-25 as 551000000; the 10-K reports 423000000 for the same date. Total accrued liabilities at that date is printed as 1122000000 in both filings, so the difference sits among the components of accrued liabilities, alongside the warranty accrual restatement. No restatement trace exists in the input.",
    "account": "other accrued liabilities, current",
    "expected_direction": "down",
    "horizon": "balance at 2025-04-25, as filed 2026-02-26 against as filed 2026-06-05",
    "quote": "551000000",
    "paragraph_id": "0001193125-26-076622:facts:OtherAccruedLiabilitiesCurrent:2025-04-25"
  },
  {
    "id": "articulation_and_the_filed_history_other_accrued_liabilities_annual_report_restated_value",
    "what_changed": "Restated prior value. The 10-K filed 2026-06-05 reports other accrued liabilities at 2025-04-25 as 423000000, where the 10-Q filed 2026-02-26 printed 551000000. The 10-K's 2026-04-24 value of 537000000 matches the current 10-Q's comparative.",
    "account": "other accrued liabilities, current",
    "expected_direction": "down",
    "horizon": "balance at 2025-04-25, as filed 2026-06-05",
    "quote": "423000000",
    "paragraph_id": "0001193125-26-259683:facts:OtherAccruedLiabilitiesCurrent:2025-04-25"
  },
  {
    "id": "structure_and_disclosure_changes_revenues_tag_carries_hybrid_cloud_total_quarterly",
    "what_changed": "The undimensioned us-gaap:Revenues fact for the quarter carries 1819000000. That is the figure the release prints for Hybrid Cloud segment revenues and the figure tagged for the Hybrid Cloud segment. Consolidated net revenue is tagged as RevenueFromContractWithCustomerExcludingAssessedTax at 2025000000. A reader of the us-gaap:Revenues tag would take the segment figure for total revenue; the trend table uses the contract-revenue tag.",
    "account": "revenue tagging",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-07-31",
    "quote": "1819000000",
    "paragraph_id": "0001193125-26-380207:facts:Revenues:2026-04-25..2026-07-31"
  },
  {
    "id": "structure_and_disclosure_changes_revenues_tag_carries_hybrid_cloud_total_annual",
    "what_changed": "The annual report shows the same pattern. Undimensioned us-gaap:Revenues for fiscal 2026 is 6237000000, the same figure the filing tags as the Hybrid Cloud segment total, while consolidated revenue is 6925000000 under RevenueFromContractWithCustomerExcludingAssessedTax. Its Revenues values for the two earlier years, 5907000000 and 5657000000, likewise equal its Hybrid Cloud segment totals for those years.",
    "account": "revenue tagging",
    "expected_direction": "none",
    "horizon": "fiscal years ended 2024-04-26 to 2026-04-24",
    "quote": "6237000000",
    "paragraph_id": "0001193125-26-259683:facts:Revenues:2025-04-26..2026-04-24"
  },
  {
    "id": "structure_and_disclosure_changes_statutory_rate_tag_carries_effective_rate",
    "what_changed": "The current 10-Q tags 0.225 (prior-year quarter 0.234) with EffectiveIncomeTaxRateReconciliationAtFederalStatutoryIncomeTaxRate; these are the effective tax rates the release prints (22.5% and 23.4%). The 10-K uses that same concept for the 0.21 statutory rate and tags its effective rate of 0.226 as EffectiveIncomeTaxRateContinuingOperations. The concept carries different measures in the two filings.",
    "account": "income tax rate tagging",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-07-31 and fiscal year ended 2026-04-24",
    "quote": "0.225",
    "paragraph_id": "0001193125-26-380207:facts:EffectiveIncomeTaxRateReconciliationAtFederalStatutoryIncomeTaxRate:2026-04-25..2026-07-31"
  },
  {
    "id": "liquidity_and_capital_inventory_purchase_obligations",
    "what_changed": "Inventory purchase obligations are 1900000000 at 2026-07-31. They were 1000000000 in the 10-K at 2026-04-24 and 700000000 in the prior 10-Q at 2026-01-23. Total unconditional purchase obligations are 2300000000 at 2026-07-31 (10-K: 1400000000), with 2100000000 due within the first year (10-K: 1100000000).",
    "account": "unrecorded unconditional purchase obligations, inventories",
    "expected_direction": "up",
    "horizon": "balances at 2026-01-23, 2026-04-24 and 2026-07-31",
    "quote": "1900000000",
    "paragraph_id": "0001193125-26-380207:facts:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount:2026-07-31:us-gaap:UnrecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:InventoriesMember"
  },
  {
    "id": "estimates_and_discretion_raw_materials_inventory_build",
    "what_changed": "Raw materials inventory is 120000000 at 2026-07-31, against 14000000 at 2026-04-24. Finished goods are 255000000 against 184000000, and net inventory is 375000000 against 198000000. The cash-flow statement tags an increase in inventories of 176000000 for the quarter. No inventory reserve is tagged in any period, so the input holds no reserve figure against this build.",
    "account": "inventory, raw materials",
    "expected_direction": "up",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "120000000",
    "paragraph_id": "0001193125-26-380207:facts:InventoryRawMaterialsNetOfReserves:2026-07-31"
  },
  {
    "id": "narrative_signs_of_operating_pressure_restructuring_charges_quarterly",
    "what_changed": "Restructuring charges are 56000000 in the quarter, against 2000000 in the prior-year quarter. All of fiscal 2026 carried 21000000 and fiscal 2025 carried 83000000. The release's full-year fiscal 2027 guidance reconciliation carries restructuring charges of $0.28 per share.",
    "account": "restructuring charges",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "56000000",
    "paragraph_id": "0001193125-26-380207:facts:RestructuringCharges:2026-04-25..2026-07-31"
  },
  {
    "id": "estimates_and_discretion_restructuring_reserve_balance",
    "what_changed": "The restructuring reserve is 40000000 at 2026-07-31, against 6000000 at 2026-04-24, with restructuring payments of 22000000 in the quarter. It was 16000000 at 2025-07-25 and 51000000 at 2025-04-25.",
    "account": "restructuring reserve",
    "expected_direction": "up",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "40000000",
    "paragraph_id": "0001193125-26-380207:facts:RestructuringReserve:2026-07-31"
  },
  {
    "id": "estimates_and_discretion_restructuring_reversal_prior_quarter",
    "what_changed": "The prior 10-Q (0001193125-26-076622) reported a negative restructuring charge of -3000000 for the quarter 2025-10-25..2026-01-23, meaning earlier accruals were released. The current quarter's charge is 56000000.",
    "account": "restructuring charges",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-01-23",
    "quote": "-3000000",
    "paragraph_id": "0001193125-26-076622:facts:RestructuringCharges:2025-10-25..2026-01-23"
  },
  {
    "id": "earnings_quality_operating_cash_flow_quarterly",
    "what_changed": "Operating cash flow for the quarter is 503000000, against 673000000 in the prior-year quarter, while net income is 375000000 against 233000000. Inside operating cash flow:\n- Inventories increased 176000000, against a prior-year decrease of 54000000.\n- Receivables decreased 317000000, against 466000000.\n- Accrued liabilities decreased 75000000, against 240000000.",
    "account": "net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "503000000",
    "paragraph_id": "0001193125-26-380207:facts:NetCashProvidedByUsedInOperatingActivities:2026-04-25..2026-07-31"
  },
  {
    "id": "earnings_quality_depreciation_and_amortization_quarterly",
    "what_changed": "Depreciation and amortization is 33000000 for the quarter, against 51000000 in the prior-year quarter. Fiscal 2026 was 200000000 against 243000000 in fiscal 2025. Gross PP&E is 2068000000 at 2026-07-31 (1986000000 at 2026-04-24), and accumulated depreciation is 1405000000 (1394000000).",
    "account": "depreciation and amortization",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "33000000",
    "paragraph_id": "0001193125-26-380207:facts:DepreciationAndAmortization:2026-04-25..2026-07-31"
  },
  {
    "id": "liquidity_and_capital_current_portion_of_debt",
    "what_changed": "The current portion of long-term debt is 550000000 at 2026-07-31, against 0 at 2026-04-24. Noncurrent long-term debt is 1938000000 against 2487000000, and the senior notes' face amount is 2500000000 at both dates. The 10-K maturity schedule placed 550000000 in year two. No commercial paper is outstanding at either date.",
    "account": "long-term debt, current",
    "expected_direction": "up",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "550000000",
    "paragraph_id": "0001193125-26-380207:facts:LongTermDebtCurrent:2026-07-31"
  },
  {
    "id": "liquidity_and_capital_cash_and_equivalents_balance",
    "what_changed": "Cash and cash equivalents are 1573000000 at 2026-07-31, against 2070000000 at 2026-04-24. Short-term investments are 2003000000 against 1514000000. Cash, equivalents and investments together are tagged 3576000000 against 3584000000.",
    "account": "cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "1573000000",
    "paragraph_id": "0001193125-26-380207:facts:CashAndCashEquivalentsAtCarryingValue:2026-07-31"
  },
  {
    "id": "liquidity_and_capital_repurchase_authorization_remaining",
    "what_changed": "The remaining authorized repurchase amount is 1302000000 at 2026-07-31, against 502000000 at 2026-04-24. The company repurchased 200000000 of stock in the quarter: 1500000 shares at an average cost of 133.32 per share.",
    "account": "stock repurchase program, remaining authorization",
    "expected_direction": "up",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "1302000000",
    "paragraph_id": "0001193125-26-380207:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-07-31:us-gaap:SubsidiarySaleOfStockAxis=ntap:StockRepurchaseProgramMember"
  },
  {
    "id": "revenue_recognition_remaining_performance_obligation_balance",
    "what_changed": "Remaining performance obligations are 5600000000 at 2026-07-31, with 0.44 expected to be recognized in the following twelve months. The 10-K reports 5.7 billion with 45% at 2026-04-24. Contract liabilities over revenue is the lowest of the 6 filled quarters.",
    "account": "remaining performance obligation",
    "expected_direction": "down",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "5600000000",
    "paragraph_id": "0001193125-26-380207:facts:RevenueRemainingPerformanceObligation:2026-07-31:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-08-01"
  },
  {
    "id": "estimates_and_discretion_other_accrued_liabilities_balance",
    "what_changed": "Other accrued liabilities are 737000000 at 2026-07-31, against 537000000 at 2026-04-24. Employee-related liabilities are 390000000 against 543000000, and total accrued liabilities are 1200000000 against 1151000000.",
    "account": "other accrued liabilities, current",
    "expected_direction": "up",
    "horizon": "balance at 2026-07-31 against 2026-04-24",
    "quote": "737000000",
    "paragraph_id": "0001193125-26-380207:facts:OtherAccruedLiabilitiesCurrent:2026-07-31"
  },
  {
    "id": "articulation_and_the_filed_history_acquisition_payment_two_values",
    "what_changed": "For the DataPelago acquisition dated 2026-07-16, the 10-Q tags cash paid net of cash acquired as 87000000. The quarter's cash-flow line uses the same concept at 78000000, and the release prints (78). The related facts are:\n- consideration including liabilities incurred: 106000000\n- goodwill acquired: 151000000\n- identifiable assets acquired: 198000000\n- liabilities assumed: 5000000\n- cash acquired: 9000000\nThe input holds no reconciliation of the two payment figures.",
    "account": "acquisition of business, net of cash acquired",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-07-31",
    "quote": "87000000",
    "paragraph_id": "0001193125-26-380207:facts:PaymentsToAcquireBusinessesNetOfCashAcquired:2026-07-16..2026-07-16:us-gaap:BusinessAcquisitionAxis=ntap:DataPelagoIncAcquisitionMember"
  },
  {
    "id": "across_documents_investment_purchases_gross_in_facts_net_in_release",
    "what_changed": "The 10-Q tags gross payments to acquire investments of 1603000000 (prior-year quarter 741000000) and proceeds from sales and maturities of 1109000000 (prior-year 598000000). The release's cash-flow statement prints a single line, Purchases of investments, net, of (494) against (143). The input holds no line linking the gross facts to the release's net figure.",
    "account": "purchases of investments",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "1603000000",
    "paragraph_id": "0001193125-26-380207:facts:PaymentsToAcquireInvestments:2026-04-25..2026-07-31"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_accrual_nil",
    "what_changed": "The loss contingency accrual is 0 at 2026-07-31, the same as in the 10-K at 2026-04-24. CommitmentsAndContingencies is tagged nil at both balance-sheet dates.",
    "account": "loss contingency accrual",
    "expected_direction": "none",
    "horizon": "balance at 2026-07-31",
    "quote": "0",
    "paragraph_id": "0001193125-26-380207:facts:LossContingencyAccrualAtCarryingValue:2026-07-31"
  },
  {
    "id": "across_documents_inventory_turns_release_figures",
    "what_changed": "The release prints inventory turns of 6 for Q1 FY27 against 14 for Q1 FY26; it defines turns as annualized cost of revenues divided by net inventories. It also prints DSO of 47 against 46 and DPO of 92 against 80. The direction agrees with the trend table's days sales of inventory, which is the highest of the 6 filled quarters.",
    "account": "inventory turns",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "| Inventory Turns |  |  | 6 |  |  |  |  | 14 |  |",
    "paragraph_id": "0001002047-26-000003:8k_2_02:113"
  },
  {
    "id": "across_documents_free_cash_flow_margin_release_figures",
    "what_changed": "The release prints a free cash flow margin of 19.8% against 39.8%, on free cash flow of 401 against 620 ($ millions). Net income rose to 375 from 233. Purchases of property and equipment are 102 against 53.",
    "account": "free cash flow margin",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-07-31 against quarter ended 2025-07-25",
    "quote": "| Free Cash Flow Margin |  |  | 19.8 | % |  |  |  | 39.8 | % |",
    "paragraph_id": "0001002047-26-000003:8k_2_02:114"
  },
  {
    "id": "results_against_expectations_guidance_raised_release_figures",
    "what_changed": "The release raises full fiscal 2027 guidance to:\n- net revenues of $7.975 billion - $8.225 billion\n- GAAP EPS of $7.35 - $7.65\n- non-GAAP EPS of $9.73 - $10.03\nSecond-quarter guidance is net revenues of $2.025 billion - $2.175 billion; the low end equals the first-quarter actual of 2,025 ($ millions). The input does not hold the prior guidance, so the size of the raise does not exist here.",
    "account": "fiscal 2027 revenue and EPS guidance",
    "expected_direction": "up",
    "horizon": "fiscal year ending in 2027",
    "quote": "Significantly raised fiscal year 2027 revenue and earnings per share guidance",
    "paragraph_id": "0001002047-26-000003:8k_2_02:7"
  }
]
```

## Seen in the notes

None of the facts in `input_numbers.json` carries a field saying whether its element sat inside a note. I checked every fact from all three filings. I was told not to make that judgment myself, so I cannot move any finding under this heading. Every item above therefore sits under "Seen in the statements".

```json
[]
```
