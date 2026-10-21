<!-- the quote gate removed 5 item(s) from this copy; input_manifest.json lists each with its reason -->
Numbers reader — Vistance Networks, Inc. (VISN) — trigger 0001193125-26-336708 (10-Q for the period ended 2026-06-30, filed 2026-08-06), with the earnings release 0001193125-26-336705 (8-K item 2.02, filed 2026-08-06).

What my directory held. input_trends.json (the trend table), input_numbers.json (three XBRL instances listed under "documents" — 10-K 0001193125-26-072523, 10-Q 0001193125-26-193963, 10-Q 0001193125-26-336708 — and their "facts"), input_8k.md (item codes, late-filing notices, and the item 2.02 release), and input_prior_predictions.md, which says no earlier run is on record. Nothing in the directory is a price, a return, short interest, another company's file, a prior probability or an outcome window.

What my directory did not hold. There is no articulation-check file, no restatement-trace file and no fourth-quarter derivation: input_numbers.json has only the keys ticker, cutoff, documents and facts. So no articulation gap computed by Python exists to report. The restated prior values below come from 10-K facts that print a "superseded_by" field whose later value for the same date is printed elsewhere in my input (a trend-cell input or the release balance sheet). I set the two values next to each other and do no arithmetic on them.

How much of input_numbers.json I read. The file has 84,673 lines, which is more than fits in my context. I read lines 1–3,799 (the 10-K income statement, comprehensive income and balance sheet facts), 30,000–30,329 (10-K share-based compensation facts), 60,000–60,329 (10-Q cash flow facts) and 83,300–84,673 (the 10-Q's last facts, including restructuring, dividends and subsequent events). Facts outside those ranges were not read, and no item rests on them. The other three files were read in full.

Periods. The trend table requested 8 quarters and 5 years, and every one is "filled" ("periods_on_record": 13). No period falls outside the record, so there is no unreached period to report. Outside the itemized quarters-back-0 and years-back-0 cells, the table also leaves these cells unfilled:
- accruals_over_total_assets in quarters-back-2, -3, -4, -6 and -7: no operating cash flow row exists for those three-month periods.
- days_sales_of_inventory and gross_margin in quarters-back-2 and -6: no cost-of-revenue row exists for those fourth quarters, and no fourth-quarter derivation is in my input.
- inventory_reserve_ratio and non_gaap_gap in every period.

The years-back-0 R&D-capitalization block prints no paragraph_id, so it cannot be quoted on its own. Its printed values are cited inside the R&D item.

Field conventions. expected_direction is the sign of the change the input prints for the item: the quarter-over-quarter change for quarterly cells, the year-over-year change for annual cells, the later filed value against the earlier one for restated values, and the printed comparison for release figures. It is "none" where no change exists, where the input forbids a comparison, or where the item is a provenance or structure observation. horizon names the comparison the change is printed against. No item has a probability, and none ranks by size.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cell", "what_changed": "insufficient: accruals_over_total_assets has no value in quarters-back-0 (2026-04-01..2026-06-30), so it has no change and no position in history. The cell's reason: the record has an operating cash flow row, but not for this three-month period. The filed record does print the six-month figure (0001193125-26-336708:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30, -299400000), and the release prints the quarter's figure (0001193125-26-336705:8k_2_02:34). Neither is a value this cell holds, and nothing is derived from them here.", "account": "net income less operating cash flow, over total assets", "expected_direction": "none", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4: no comparison exists", "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0001193125-26-336708:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_prior_filled_quarter_cell", "what_changed": "The latest filled quarter of accruals_over_total_assets is quarters-back-1 (2026-01-01..2026-03-31). Value 1.0535733970237002. No quarter-over-quarter change exists because quarters-back-2 is not filled. Change 0.9242476650792188 against quarters-back-5. Inputs, all from 0001193125-26-193963: net income 5508000000.0, operating cash flow -226600000.0, assets 5443000000.0. Only 2 quarters of this ratio are filled, which does not support a trend claim: insufficient for a trend.", "account": "net income less operating cash flow, over total assets", "expected_direction": "up", "horizon": "quarters-back-1 against quarters-back-5", "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"", "paragraph_id": "0001193125-26-336708:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_cell", "what_changed": "Value 0.0017793594306049821. Change -7.20026429205402e-05 against quarters-back-1 and -0.01286763740817268 against quarters-back-4. Inputs: allowance 500000.0 and net receivables 280500000.0, both from 0001193125-26-336708. The quarters-back-1 inputs (allowance 700000.0, receivables 377400000.0) come from 0001193125-26-193963. The quarters-back-4 inputs (allowance 13900000.0, receivables 935100000.0) come from 0000950170-25-101615, filed 2025-08-04. The release says amounts for all periods presented were recast for the RUCKUS sale (0001193125-26-336705:8k_2_02:18).", "account": "allowance for doubtful accounts against gross trade receivables", "expected_direction": "down", "horizon": "quarters-back-0 against quarters-back-1 (quarter over quarter) and quarters-back-4 (year over year)", "quote": "\"position_in_history\": \"lowest of the 8 filled quarters\"", "paragraph_id": "0001193125-26-336708:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_cell", "what_changed": "Value 0.11827284105131414. Change -0.14115912164474353 against quarters-back-1 and -0.23964138295362258 against quarters-back-4. Inputs: current contract liabilities 37800000.0 and revenue 319600000.0, both from 0001193125-26-336708. quarters-back-1 inputs: contract liabilities 122400000.0 and revenue 471800000.0, both from 0001193125-26-193963. quarters-back-4 inputs: contract liabilities 116000000.0 from 0000950170-25-101615 and revenue 324100000.0 from 0001193125-26-336708. The position ranks only the 6 quarters whose revenue rests on the same concept.", "account": "current contract liabilities (deferred revenue) against quarterly revenue", "expected_direction": "down", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"", "paragraph_id": "0001193125-26-336708:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_cell", "what_changed": "Value 138.1509433962264 days. Change 10.805290309288154 against quarters-back-1 and -287.515912772051 against quarters-back-4. Inputs: inventory 313800000.0 and cost of revenue 206700000.0, both from 0001193125-26-336708. quarters-back-1 inputs: inventory 336900000.0 and cost of revenue 238100000.0, both from 0001193125-26-193963. quarters-back-4 pairs inventory 822800000.0 from 0000950170-25-101615 with cost of revenue 175900000.0 from 0001193125-26-336708. The release balance sheet prints inventories, net of 313.8 at June 30, 2026 against 238.7 at December 31, 2025 (0001193125-26-336705:8k_2_02:57).", "account": "inventories, net against cost of sales", "expected_direction": "up", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-336708:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_cell", "what_changed": "Value 79.86702127659574 days. Change 7.874651628439736 against quarters-back-1 and -182.68805431735677 against quarters-back-4. Inputs: net receivables 280500000.0 and revenue 319600000.0, both from 0001193125-26-336708. quarters-back-1 inputs: receivables 377400000.0 and revenue 471800000.0, both from 0001193125-26-193963. quarters-back-4 pairs receivables 935100000.0 from 0000950170-25-101615 with revenue 324100000.0 from 0001193125-26-336708, so the year-over-year change is measured against a cell whose two inputs come from different filings. The position ranks only the 6 quarters on the same concepts.", "account": "accounts receivable, net against quarterly revenue", "expected_direction": "up", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"", "paragraph_id": "0001193125-26-336708:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_cell", "what_changed": "Value 0.3532540675844806. Change -0.14208293962196283 against quarters-back-1 and -0.1040122082563093 against quarters-back-4. Inputs: revenue 319600000.0 and cost of revenue 206700000.0, both from 0001193125-26-336708. The quarters-back-4 inputs (revenue 324100000.0, cost 175900000.0) are also from 0001193125-26-336708. The quarters-back-1 inputs (revenue 471800000.0, cost 238100000.0) are from 0001193125-26-193963. The release attributes the year-over-year decline to strong license sales in the prior-year quarter, memory chip pricing and stranded costs (0001193125-26-336705:8k_2_02:17). It prints adjusted gross profit as % of sales of 35.3% against 45.8% (0001193125-26-336705:8k_2_02:65).", "account": "gross margin (net sales less cost of sales, over net sales)", "expected_direction": "down", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001193125-26-336708:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_cell", "what_changed": "insufficient: inventory_reserve_ratio is not filled in quarters-back-0, or in any period of the table. The record tags no us-gaap:InventoryValuationReserves fact, and the cell says the record cannot tell whether the company does not tag the concept or states it only by segment. No value, change or position exists.", "account": "inventory valuation reserve against gross inventory", "expected_direction": "none", "horizon": "quarters-back-0: no comparison exists", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001193125-26-336708:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell", "what_changed": "insufficient: non_gaap_gap is not filled in quarters-back-0, or in any period, because no us-gaap concept carries a non-GAAP measure. The release prints non-GAAP adjusted net income of $28.2 million and GAAP income from continuing operations of $26.1 million for the quarter (0001193125-26-336705:8k_2_02:21). The table holds no gap, and none is derived here.", "account": "non-GAAP adjusted net income against GAAP income", "expected_direction": "none", "horizon": "quarters-back-0: no comparison exists", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001193125-26-336708:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_cell", "what_changed": "Value 0.8776595744680851. Change 0.07774435615524067 against quarters-back-1 and -2.0075610364544696 against quarters-back-4. The inputs are the same as for days_sales_outstanding: receivables 280500000.0 and revenue 319600000.0 from 0001193125-26-336708. quarters-back-1 uses receivables 377400000.0 and revenue 471800000.0 from 0001193125-26-193963. quarters-back-4 pairs receivables 935100000.0 from 0000950170-25-101615 with revenue 324100000.0 from 0001193125-26-336708. The position ranks only the 6 quarters on the same concepts.", "account": "accounts receivable, net against quarterly revenue", "expected_direction": "up", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"", "paragraph_id": "0001193125-26-336708:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_cell", "what_changed": "Value 0.9541008922443377. Change 0.4255872049395425 against quarters-back-1 and 0.0714653574663332 against quarters-back-4. Inputs, all from 0001193125-26-336708: assets 3496800000.0, cash 113600000.0, PP&E 46900000.0. quarters-back-1 inputs, from 0001193125-26-193963: assets 5443000000.0, cash 2510000000.0, PP&E 56300000.0. The release cash flow statement prints a special distribution paid to common shareholders of (2,316.3) in the quarter (0001193125-26-336705:8k_2_02:58).", "account": "assets other than cash and PP&E, over total assets", "expected_direction": "up", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"highest of the 8 filled quarters\"", "paragraph_id": "0001193125-26-336708:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_cell", "what_changed": "Value 0.02471839799749687. Change 0.007550106348493055 against quarters-back-1 and 0.008056873776577399 against quarters-back-4. Inputs: warranty accrual 7900000.0 and revenue 319600000.0, both from 0001193125-26-336708. quarters-back-1 pairs warranty accrual 8100000.0 from 0001193125-26-336708 with revenue 471800000.0 from 0001193125-26-193963. The quarters-back-4 inputs (warranty 5400000.0, revenue 324100000.0) are both from 0001193125-26-336708. The position ranks only the 6 quarters on the same concepts.", "account": "product warranty accrual against quarterly revenue", "expected_direction": "up", "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4", "quote": "\"position_in_history\": \"highest of the 6 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"", "paragraph_id": "0001193125-26-336708:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_cell", "what_changed": "Value 0.20924127627787856. Change 0.27652907279116806 against years-back-1. Inputs: net income 2283700000.0 and operating cash flow 322900000.0 from the 10-K 0001193125-26-072523, and assets 9371000000.0 from 0001193125-26-336708. That net income includes 2025 income from discontinued operations, net of tax, of 1959400000, as the 10-K prints it (0001193125-26-072523:facts:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity:2025-01-01..2025-12-31).", "account": "net income less operating cash flow, over total assets", "expected_direction": "up", "horizon": "years-back-0 (2025-01-01..2025-12-31) against years-back-1", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_cell", "what_changed": "Value 0.004369992716678805. Change -0.0019341838002636695 against years-back-1. Inputs: allowance 1200000.0 and receivables 273400000.0, both from 0001193125-26-336708 (the 10-Q's 2025-12-31 column). For the same date the 10-K printed 1600000 and 350400000; see the restated-value items. The years-back-1 inputs (allowance 1600000.0, receivables 252200000.0) are from 0001193125-26-072523.", "account": "allowance for doubtful accounts against gross trade receivables", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_cell", "what_changed": "Value 0.00957755228825844. Change -0.05891658918432944 against years-back-1. Inputs: contract liabilities 18500000.0 from 0001193125-26-336708 against revenue 1931600000.0 from 0001193125-26-072523. years-back-1 sets contract liabilities 94700000.0 against revenue 1382600000.0, both from 0001193125-26-072523.", "account": "current contract liabilities against annual revenue", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_cell", "what_changed": "Value 89.29537767756483 days. Change -100.41266090764418 against years-back-1. Inputs: inventory 238700000.0 from 0001193125-26-336708 (the 10-K printed 310400000 for the same date) against cost of revenue 975700000.0 from 0001193125-26-072523. years-back-1 sets inventory 403000000.0 against cost of revenue 777500000.0, both from 0001193125-26-072523.", "account": "inventories, net against annual cost of sales", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_cell", "what_changed": "Value 51.662352453924214 days. Change -15.099690074645139 against years-back-1. Inputs: receivables 273400000.0 from 0001193125-26-336708 (the 10-K printed 350400000 for the same date) against revenue 1931600000.0 from 0001193125-26-072523. years-back-1 sets receivables 252200000.0 against revenue 1382600000.0, both from 0001193125-26-072523.", "account": "accounts receivable, net against annual revenue", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_cell", "what_changed": "Value 0.494874715261959. Change 0.05722101932676443 against years-back-1. Inputs: revenue 1931600000.0 and cost of revenue 975700000.0, both from 0001193125-26-072523. The years-back-1 revenue 1382600000.0 and cost 777500000.0 come from the same filing.", "account": "gross margin", "expected_direction": "up", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_cell", "what_changed": "insufficient: inventory_reserve_ratio is not filled in years-back-0, or in any year, because the record tags no us-gaap:InventoryValuationReserves fact. No value, change or position exists.", "account": "inventory valuation reserve against gross inventory", "expected_direction": "none", "horizon": "years-back-0: no comparison exists", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001193125-26-336708:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell", "what_changed": "insufficient: non_gaap_gap is not filled in years-back-0, or in any year, because no us-gaap concept carries a non-GAAP measure. No value, change or position exists.", "account": "non-GAAP adjusted net income against GAAP income", "expected_direction": "none", "horizon": "years-back-0: no comparison exists", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001193125-26-336708:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_cell", "what_changed": "Value 0.14154069165458688. Change -0.040869260609263824 against years-back-1. The inputs are the same as for days_sales_outstanding: receivables 273400000.0 from 0001193125-26-336708 against revenue 1931600000.0 from 0001193125-26-072523.", "account": "accounts receivable, net against annual revenue", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_cell", "what_changed": "Value 0.9291644434958916. Change -0.015242529925085901 against years-back-1. Inputs, all from 0001193125-26-336708: assets 9371000000.0, cash 613500000.0, PP&E 50300000.0. For the same date the 10-K printed cash 754400000 and PP&E 58600000, with total assets the same 9371000000. The years-back-1 inputs, from 0001193125-26-072523, are assets 8747500000.0, cash 404100000.0 and PP&E 82200000.0.", "account": "assets other than cash and PP&E, over total assets", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_cell", "what_changed": "Value 0.004089873679850901. Change -0.0009730512442052246 against years-back-1. Inputs: warranty accrual 7900000.0 from 0001193125-26-336708 against revenue 1931600000.0 from 0001193125-26-072523. years-back-1 sets warranty accrual 7000000.0 from 0001193125-26-336708 against revenue 1382600000.0 from 0001193125-26-072523.", "account": "product warranty accrual against annual revenue", "expected_direction": "down", "horizon": "years-back-0 against years-back-1", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001193125-26-336708:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```




```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_days_sales_outstanding_recent", "what_changed": "Change of tag. In quarters-back-2 (2025-10-01..2025-12-31), days_sales_outstanding rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (514500000.0, from 0001193125-26-072523). quarters-back-1 and quarters-back-3 rest on RevenueFromContractWithCustomerExcludingAssessedTax, so the table prints no quarter-over-quarter change on either side of this quarter. Value 48.887852283770656, 'lowest of the 2 filled quarters on the same concepts'. Change -6.99461399753956 against quarters-back-6, which rests on the same concept. Two quarters on one concept do not support a trend claim: insufficient.", "account": "revenue concept under days sales outstanding", "expected_direction": "none", "horizon": "quarters-back-2 against quarters-back-1 and quarters-back-3", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:days_sales_outstanding:2025-10-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_days_sales_outstanding_older", "what_changed": "Change of tag. In quarters-back-6 (2024-10-01..2024-12-31), days_sales_outstanding rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (415200000.0, from 0001193125-26-072523). quarters-back-5 and quarters-back-7 rest on RevenueFromContractWithCustomerExcludingAssessedTax. Value 55.882466281310215, 'highest of the 2 filled quarters on the same concepts'. No year-over-year change exists because the quarter 4 back is outside the window. insufficient for a trend.", "account": "revenue concept under days sales outstanding", "expected_direction": "none", "horizon": "quarters-back-6 against quarters-back-5 and quarters-back-7", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:days_sales_outstanding:2024-10-01..2024-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_receivables_over_revenue_recent", "what_changed": "Change of tag. In quarters-back-2, receivables_over_revenue rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (514500000.0, from 0001193125-26-072523), unlike quarters-back-1 and quarters-back-3. Value 0.5313896987366376, 'lowest of the 2 filled quarters on the same concepts'. Change -0.07602841301673435 against quarters-back-6. insufficient for a trend.", "account": "revenue concept under receivables over revenue", "expected_direction": "none", "horizon": "quarters-back-2 against quarters-back-1 and quarters-back-3", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:receivables_over_revenue:2025-10-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_receivables_over_revenue_older", "what_changed": "Change of tag. In quarters-back-6, receivables_over_revenue rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (415200000.0, from 0001193125-26-072523), unlike quarters-back-5 and quarters-back-7. Value 0.6074181117533719, 'highest of the 2 filled quarters on the same concepts'. insufficient for a trend.", "account": "revenue concept under receivables over revenue", "expected_direction": "none", "horizon": "quarters-back-6 against quarters-back-5 and quarters-back-7", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:receivables_over_revenue:2024-10-01..2024-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_contract_liabilities_over_revenue_recent", "what_changed": "Change of tag. In quarters-back-2, contract_liabilities_over_revenue rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (514500000.0) against contract liabilities 18500000.0 from 0001193125-26-336708. Value 0.03595724003887269, 'lowest of the 2 filled quarters on the same concepts'. Change -0.19212561159889224 against quarters-back-6. insufficient for a trend.", "account": "revenue concept under contract liabilities over revenue", "expected_direction": "none", "horizon": "quarters-back-2 against quarters-back-1 and quarters-back-3", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:contract_liabilities_over_revenue:2025-10-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_contract_liabilities_over_revenue_older", "what_changed": "Change of tag. In quarters-back-6, contract_liabilities_over_revenue rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (415200000.0) against contract liabilities 94700000.0, both from 0001193125-26-072523. Value 0.22808285163776493, 'highest of the 2 filled quarters on the same concepts'. insufficient for a trend.", "account": "revenue concept under contract liabilities over revenue", "expected_direction": "none", "horizon": "quarters-back-6 against quarters-back-5 and quarters-back-7", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:contract_liabilities_over_revenue:2024-10-01..2024-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_warranty_reserve_ratio_recent", "what_changed": "Change of tag. In quarters-back-2, warranty_reserve_ratio rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (514500000.0) against a warranty accrual of 7900000.0 from 0001193125-26-336708. Value 0.015354713313896987, 'lowest of the 2 filled quarters on the same concepts'. Change -0.0015046315801299885 against quarters-back-6. insufficient for a trend.", "account": "revenue concept under warranty reserve ratio", "expected_direction": "none", "horizon": "quarters-back-2 against quarters-back-1 and quarters-back-3", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:warranty_reserve_ratio:2025-10-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_concept_switch_warranty_reserve_ratio_older", "what_changed": "Change of tag. In quarters-back-6, warranty_reserve_ratio rests on revenue tagged us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax (415200000.0, from 0001193125-26-072523) against a warranty accrual of 7000000.0 from 0001193125-26-336708. Value 0.016859344894026976, 'highest of the 2 filled quarters on the same concepts'. insufficient for a trend.", "account": "revenue concept under warranty reserve ratio", "expected_direction": "none", "horizon": "quarters-back-6 against quarters-back-5 and quarters-back-7", "quote": "\"tag\": \"RevenueFromContractWithCustomerIncludingAssessedTax\"", "paragraph_id": "0001193125-26-336708:trends:warranty_reserve_ratio:2024-10-01..2024-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_cash_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K (0001193125-26-072523, filed 2026-02-26) printed cash and cash equivalents of 754400000. That fact is marked superseded_by 0001193125-26-336708, and the 10-Q's value for the same date, used as the years-back-0 input, is 613500000.0. The release balance sheet prints 613.5 at December 31, 2025 (0001193125-26-336705:8k_2_02:57). No restatement trace in my input explains the difference. The release says amounts were recast for the RUCKUS sale (0001193125-26-336705:8k_2_02:18).", "account": "cash and cash equivalents", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"754400000\"", "paragraph_id": "0001193125-26-072523:facts:CashAndCashEquivalentsAtCarryingValue:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_allowance_for_doubtful_accounts_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed an allowance for doubtful accounts of 1600000, marked superseded_by 0001193125-26-336708. The 10-Q's value, used in the years-back-0 and quarters-back-2 bad-debt cells, is 1200000.0, and the release balance sheet caption prints $1.2 (0001193125-26-336705:8k_2_02:57).", "account": "allowance for doubtful accounts", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"1600000\"", "paragraph_id": "0001193125-26-072523:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_accounts_receivable_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed net accounts receivable of 350400000, marked superseded_by 0001193125-26-336708. The 10-Q's value, used as the years-back-0 and quarters-back-2 input, is 273400000.0, and the release balance sheet prints 273.4 (0001193125-26-336705:8k_2_02:57).", "account": "accounts receivable, net", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"350400000\"", "paragraph_id": "0001193125-26-072523:facts:AccountsReceivableNetCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_inventory_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed net inventories of 310400000, marked superseded_by 0001193125-26-336708. The 10-Q's value, used as the years-back-0 input, is 238700000.0, and the release balance sheet prints 238.7 (0001193125-26-336705:8k_2_02:57).", "account": "inventories, net", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"310400000\"", "paragraph_id": "0001193125-26-072523:facts:InventoryNet:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_prepaid_and_other_current_assets_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed prepaid expenses and other current assets of 56500000, marked superseded_by 0001193125-26-336708. The release balance sheet prints 46.0 for that date (0001193125-26-336705:8k_2_02:57). I did not read the 10-Q fact itself.", "account": "prepaid expenses and other current assets", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"56500000\"", "paragraph_id": "0001193125-26-072523:facts:PrepaidExpenseAndOtherAssetsCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_current_assets_held_for_sale_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed current assets of the disposal group of 4324500000, marked superseded_by 0001193125-26-336708. The release balance sheet prints current assets held for sale of 4,624.6 for that date (0001193125-26-336705:8k_2_02:57).", "account": "current assets held for sale (disposal group)", "expected_direction": "up", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"4324500000\"", "paragraph_id": "0001193125-26-072523:facts:AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_accumulated_depreciation_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed accumulated depreciation on PP&E of 174500000, marked superseded_by 0001193125-26-336708. The release balance sheet caption prints accumulated depreciation of $134.7 for that date (0001193125-26-336705:8k_2_02:57).", "account": "accumulated depreciation, property, plant and equipment", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"174500000\"", "paragraph_id": "0001193125-26-072523:facts:AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_property_plant_and_equipment_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed net PP&E of 58600000, marked superseded_by 0001193125-26-336708. The 10-Q's value, used in the years-back-0 soft_asset_share cell, is 50300000.0, and the release balance sheet prints 50.3 (0001193125-26-336705:8k_2_02:57).", "account": "property, plant and equipment, net", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"58600000\"", "paragraph_id": "0001193125-26-072523:facts:PropertyPlantAndEquipmentNet:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_goodwill_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed goodwill of 764600000, marked superseded_by 0001193125-26-336708. The release balance sheet prints goodwill of 268.7 for that date and 268.7 at June 30, 2026 (0001193125-26-336705:8k_2_02:57).", "account": "goodwill", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"764600000\"", "paragraph_id": "0001193125-26-072523:facts:Goodwill:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_other_intangible_assets_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed other intangible assets, net of 839100000, marked superseded_by 0001193125-26-336708. The release balance sheet prints 719.1 for that date and 678.3 at June 30, 2026 (0001193125-26-336705:8k_2_02:57).", "account": "other intangible assets, net", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"839100000\"", "paragraph_id": "0001193125-26-072523:facts:OtherIntangibleAssetsNet:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_deferred_tax_assets_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed net deferred income tax assets of 1765900000, marked superseded_by 0001193125-26-336708. The release balance sheet prints deferred income taxes (asset) of 1,722.3 for that date (0001193125-26-336705:8k_2_02:57).", "account": "deferred income tax assets, net", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"1765900000\"", "paragraph_id": "0001193125-26-072523:facts:DeferredIncomeTaxAssetsNet:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_other_noncurrent_assets_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed other noncurrent assets of 146600000, marked superseded_by 0001193125-26-336708. The release balance sheet prints 118.4 for that date (0001193125-26-336705:8k_2_02:57).", "account": "other noncurrent assets", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"146600000\"", "paragraph_id": "0001193125-26-072523:facts:OtherAssetsNoncurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_noncurrent_assets_held_for_sale_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed noncurrent assets of the disposal group of 0, marked superseded_by 0001193125-26-336708. The release balance sheet prints noncurrent assets held for sale of 696.0 for that date (0001193125-26-336705:8k_2_02:57).", "account": "noncurrent assets held for sale (disposal group)", "expected_direction": "up", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"0\"", "paragraph_id": "0001193125-26-072523:facts:DisposalGroupIncludingDiscontinuedOperationAssetsNoncurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_accounts_payable_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed accounts payable of 213300000, marked superseded_by 0001193125-26-336708. The release balance sheet prints 161.4 for that date and 183.3 at June 30, 2026 (0001193125-26-336705:8k_2_02:57).", "account": "accounts payable", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"213300000\"", "paragraph_id": "0001193125-26-072523:facts:AccountsPayableCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_accrued_and_other_liabilities_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed accrued and other liabilities of 498300000, marked superseded_by 0001193125-26-336708. The release balance sheet prints 306.7 for that date and 222.2 at June 30, 2026 (0001193125-26-336705:8k_2_02:57).", "account": "accrued and other liabilities", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"498300000\"", "paragraph_id": "0001193125-26-072523:facts:AccruedLiabilitiesAndOtherLiabilities:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_current_liabilities_held_for_sale_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed current liabilities of the disposal group of 783900000, marked superseded_by 0001193125-26-336708. The release balance sheet prints current liabilities held for sale of 1,027.4 for that date (0001193125-26-336705:8k_2_02:57).", "account": "current liabilities held for sale (disposal group)", "expected_direction": "up", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"783900000\"", "paragraph_id": "0001193125-26-072523:facts:LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_deferred_tax_liabilities_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed net deferred income tax liabilities of 67200000, marked superseded_by 0001193125-26-336708. The release balance sheet prints deferred income taxes (liability) of 67.3 for that date (0001193125-26-336705:8k_2_02:57). The two printed figures are not the same.", "account": "deferred income tax liabilities, net", "expected_direction": "up", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"67200000\"", "paragraph_id": "0001193125-26-072523:facts:DeferredIncomeTaxLiabilitiesNet:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_other_noncurrent_liabilities_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed other noncurrent liabilities of 273500000, marked superseded_by 0001193125-26-336708. The release balance sheet prints 153.4 for that date and 179.0 at June 30, 2026 (0001193125-26-336705:8k_2_02:57).", "account": "other noncurrent liabilities", "expected_direction": "down", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"273500000\"", "paragraph_id": "0001193125-26-072523:facts:OtherLiabilitiesNoncurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_noncurrent_liabilities_held_for_sale_reported_differently", "what_changed": "Restated prior value. For 2025-12-31 the 10-K printed noncurrent liabilities of the disposal group of 0, marked superseded_by 0001193125-26-336708. The release balance sheet prints noncurrent liabilities held for sale of 120.0 for that date (0001193125-26-336705:8k_2_02:57).", "account": "noncurrent liabilities held for sale (disposal group)", "expected_direction": "up", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"0\"", "paragraph_id": "0001193125-26-072523:facts:LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationNoncurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_balance_sheet_totals_unchanged_across_filings", "what_changed": "Superseded but not changed. For 2025-12-31 the 10-K's total assets (9371000000), total current assets (5796200000), total current liabilities (1495500000), long-term debt (7260200000) and total liabilities (9096400000) are all marked superseded_by 0001193125-26-336708. The trend input (assets 9371000000.0) and the release balance sheet (5,796.2; 1,495.5; 7,260.2; 9,096.4) print the same amounts, while the components in the restated-value items above moved between lines.", "account": "balance sheet totals", "expected_direction": "none", "horizon": "2025-12-31 as filed on 2026-02-26 against as filed on 2026-08-06", "quote": "\"value\": \"9371000000\"", "paragraph_id": "0001193125-26-072523:facts:Assets:2025-12-31" }
```

```json
{ "id": "controls_audit_and_filings_share_counts_identical_across_balance_sheet_dates", "what_changed": "The 10-K prints common shares outstanding of 215887001 at both 2025-12-31 and 2024-12-31 (0001193125-26-072523:facts:CommonStockSharesOutstanding:2024-12-31), and common shares issued of 223260316 at both dates. Its weighted average basic shares differ between the years: 219500000 for 2025 and 214400000 for 2024. The 2025-12-31 share facts are marked superseded_by 0001193125-26-336708. The release prints issued and outstanding shares of 223,260,316 and treasury shares of 18,665,426 at December 31, 2025 (0001193125-26-336705:8k_2_02:57). Reported as printed; no figure is derived.", "account": "common shares outstanding", "expected_direction": "none", "horizon": "2024-12-31 and 2025-12-31 as filed on 2026-02-26", "quote": "\"value\": \"215887001\"", "paragraph_id": "0001193125-26-072523:facts:CommonStockSharesOutstanding:2025-12-31" }
```

```json
{ "id": "earnings_quality_research_and_development_expense_filed_annual", "what_changed": "The 10-K prints research and development expense of 283500000 for 2025, against 247500000 for 2024 and 318800000 for 2023. The trend table's years-back-0 R&D-capitalization block prints earnings_with_rnd_capitalized of 2109960000.0 against net income of 2283700000.0, and book_value_with_rnd_capitalized of -37680000.0 against stockholders' equity of -1004100000.0, using a 5-year life. That block prints no paragraph_id, and the table finds no capitalized development cost tagged in any period. The release prints quarterly R&D of 30.8 against 43.1 (0001193125-26-336705:8k_2_02:56).", "account": "research and development expense", "expected_direction": "up", "horizon": "2025 against 2024", "quote": "\"value\": \"283500000\"", "paragraph_id": "0001193125-26-072523:facts:ResearchAndDevelopmentExpense:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_discontinued_operations_inside_annual_net_income", "what_changed": "The 10-K prints 2025 income from discontinued operations, net of tax, of 1959400000. It sits inside net income of 2283700000, the net income feeding the years-back-0 accruals cell, alongside income from continuing operations of 324300000. The 2024 figure is -109500000.", "account": "income from discontinued operations, net of tax", "expected_direction": "up", "horizon": "2025 against 2024", "quote": "\"value\": \"1959400000\"", "paragraph_id": "0001193125-26-072523:facts:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_tax_benefit_lifts_annual_continuing_income", "what_changed": "The 10-K prints 2025 income tax expense (benefit) of -269400000, against continuing-operations pre-tax income of 54900000 and income from continuing operations of 324300000. For 2024 it prints -66900000, -272900000 and -206000000.", "account": "income tax expense (benefit), continuing operations", "expected_direction": "down", "horizon": "2025 against 2024", "quote": "\"value\": \"-269400000\"", "paragraph_id": "0001193125-26-072523:facts:IncomeTaxExpenseBenefit:2025-01-01..2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_used_cumulative_filed", "what_changed": "The 10-Q prints net cash used in operating activities of -299400000 for 2026-01-01..2026-06-30, against -109800000 for 2025-01-01..2025-06-30 (0001193125-26-336708:facts:NetCashProvidedByUsedInOperatingActivities:2025-01-01..2025-06-30). This is the row the quarters-back-0 accruals cell says exists in the record, though not for the three-month period. The release says these cash flows include discontinued operations (0001193125-26-336705:8k_2_02:13).", "account": "net cash from operating activities", "expected_direction": "down", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"-299400000\"", "paragraph_id": "0001193125-26-336708:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_payables_and_accruals_cash_outflow", "what_changed": "The 10-Q prints a change in accounts payable and accrued liabilities of -183000000 for the six months to 2026-06-30, against 125900000 for the six months to 2025-06-30 (0001193125-26-336708:facts:IncreaseDecreaseInAccountsPayableAndAccruedLiabilities:2025-01-01..2025-06-30). The release's quarterly column prints 91.5 against 105.4 (0001193125-26-336705:8k_2_02:58).", "account": "accounts payable and accrued liabilities (cash flow change)", "expected_direction": "down", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"-183000000\"", "paragraph_id": "0001193125-26-336708:facts:IncreaseDecreaseInAccountsPayableAndAccruedLiabilities:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_restructuring_charges_rise", "what_changed": "The 10-Q prints restructuring charges of 8400000 for 2026-04-01..2026-06-30, against 1600000 for 2025-04-01..2025-06-30. For the six months it prints 15100000 against 11500000. By segment, the quarter's charge prints as 6900000 for Aurora and 1500000 for corporate and other.", "account": "restructuring costs, net", "expected_direction": "up", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "\"value\": \"8400000\"", "paragraph_id": "0001193125-26-336708:facts:RestructuringCharges:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_rise", "what_changed": "The 10-Q prints a restructuring reserve of 7500000 at 2026-06-30, against 2300000 at 2025-12-31 (0001193125-26-336708:facts:RestructuringReserve:2025-12-31). It prints the whole balance under the CommScope NEXT plan's employee-related costs member and within accrued and other liabilities. The noncurrent portion prints 0 at both dates.", "account": "restructuring reserve", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"7500000\"", "paragraph_id": "0001193125-26-336708:facts:RestructuringReserve:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_ruckus_sale_proceeds", "what_changed": "Subsequent event tagged in the 10-Q: proceeds of 1846000000 from the divestiture of the RUCKUS segment on 2026-07-01. The release says the sale to Belden closed July 1, 2026 for approximately $1.846 billion in cash, subject to certain adjustments (0001193125-26-336705:8k_2_02:18).", "account": "proceeds from divestiture of businesses", "expected_direction": "up", "horizon": "after the 2026-06-30 balance-sheet date", "quote": "\"value\": \"1846000000\"", "paragraph_id": "0001193125-26-336708:facts:ProceedsFromDivestitureOfBusinesses:2026-07-01..2026-07-01:us-gaap:StatementBusinessSegmentsAxis=visn:RuckusMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_special_distribution_declared", "what_changed": "Subsequent event: a dividend of 5 per share declared on 2026-08-05 under the 2026 dividends member. An earlier declaration of 10 per share is tagged for 2026-04-01..2026-04-07 (0001193125-26-336708:facts:CommonStockDividendsPerShareDeclared:2026-04-01..2026-04-07:us-gaap:DividendsAxis=visn:S2026DividendsMember). The release describes a special distribution of $5.00 per share to be paid by the end of August 2026, bringing the total returned this year to $15.00 per share (0001193125-26-336705:8k_2_02:16).", "account": "dividends declared per common share", "expected_direction": "up", "horizon": "after the 2026-06-30 balance-sheet date", "quote": "\"value\": \"5\"", "paragraph_id": "0001193125-26-336708:facts:CommonStockDividendsPerShareDeclared:2026-08-05..2026-08-05:us-gaap:DividendsAxis=visn:S2026DividendsMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "liquidity_and_capital_common_dividends_recorded_against_cash_paid", "what_changed": "The 10-Q prints common dividends of 2373700000 for the six months to 2026-06-30, and 2316300000 for 2026-04-01..2026-06-30 under the 2026 dividends member (0001193125-26-336708:facts:DividendsCommonStock:2026-04-01..2026-06-30:us-gaap:DividendsAxis=visn:S2026DividendsMember). The release cash flow statement prints a special distribution paid to common shareholders of (2,316.3) in both the quarter and the six-month column (0001193125-26-336705:8k_2_02:58). As printed, the six-month recorded figure and the paid figure are not the same; no difference is derived here.", "account": "dividends on common stock", "expected_direction": "up", "horizon": "six months to 2026-06-30", "quote": "\"value\": \"2373700000\"", "paragraph_id": "0001193125-26-336708:facts:DividendsCommonStock:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_no_share_repurchases_under_authorization", "what_changed": "The 10-Q prints stock repurchased of 0 for the six months to 2026-06-30. The release says the company will continue to evaluate buybacks under the $100 million of authority the Board has approved (0001193125-26-336705:8k_2_02:16).", "account": "treasury stock repurchases", "expected_direction": "none", "horizon": "six months to 2026-06-30", "quote": "\"value\": \"0\"", "paragraph_id": "0001193125-26-336708:facts:StockRepurchasedDuringPeriodValue:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_divestiture_proceeds_cumulative", "what_changed": "The 10-Q prints proceeds from divestitures of 10541700000 for the six months to 2026-06-30, against 2041800000 a year earlier, and net cash from investing activities of 10537500000. Over the same six months the release prints long-term debt repaid of (7,370.8), redemption of Series A convertible preferred stock of (1,278.7) and the special distribution of (2,316.3) (0001193125-26-336705:8k_2_02:58).", "account": "proceeds from divestiture of businesses", "expected_direction": "up", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"10541700000\"", "paragraph_id": "0001193125-26-336708:facts:ProceedsFromDivestitureOfBusinesses:2026-01-01..2026-06-30" }
```

The items below take their figures from the 8-K earnings release (0001193125-26-336705) and its condensed statements.


```json
{ "id": "narrative_signs_of_operating_pressure_memory_chip_pricing_and_stranded_costs", "what_changed": "The CFO attributes the year-over-year decline in Aurora revenue and adjusted EBITDA to strong license sales in the prior-year quarter, memory chip pricing and stranded costs from the divestitures. Core non-GAAP adjusted EBITDA prints 45.5 against 80.2, a (43.3)% change (0001193125-26-336705:8k_2_02:31).", "account": "Aurora net sales and adjusted EBITDA", "expected_direction": "down", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "This was generally aligned with our expectations and down versus the prior year due to strong license sales in the second quarter of 2025, memory chip pricing and stranded costs associated with the divestitures.", "paragraph_id": "0001193125-26-336705:8k_2_02:17" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_aurora_operating_income_drop", "what_changed": "Aurora segment operating income prints 7.0 against 49.6, a (85.9)% change. Corporate and other prints (15.9) against (41.8), and total operating income (loss) (8.9) against 7.8. Aurora net sales print 319.2 against 322.5, a (1.0)% change (0001193125-26-336705:8k_2_02:27).", "account": "Aurora segment operating income", "expected_direction": "down", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "| Aurora (1) |  | $ | 7.0 |  |  | $ | 49.6 |  |  |  | (85.9 | ) | % |", "paragraph_id": "0001193125-26-336705:8k_2_02:29" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_regional_sales_declines", "what_changed": "Net sales fell 1.4% year over year to $319.6 million. The region table prints EMEA at 14.6 against 19.8, a (26.3)% change, and Canada at 15.0 against 17.7, a (15.3)% change. The United States prints 258.1 against 255.4, a 1.1% change (0001193125-26-336705:8k_2_02:25).", "account": "net sales by region", "expected_direction": "down", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "Net sales in the second quarter of 2026 decreased 1.4% year-over-year to $319.6 million with decreases in the Europe, Middle East and Africa (EMEA) region and Canada, partially offset by increases in the United States (U.S.), the Asia Pacific (APAC) region and the Caribbean and Latin America (CALA) region.", "paragraph_id": "0001193125-26-336705:8k_2_02:20" }
```

```json
{ "id": "liquidity_and_capital_special_distribution_and_year_end_cash_outlook", "what_changed": "Management expects to end 2026, after the special distribution, with $700 to $750 million of cash and no outstanding debt. The release balance sheet prints cash and cash equivalents of 113.6 and long-term debt of — at June 30, 2026 (0001193125-26-336705:8k_2_02:57). Total liquidity at quarter end was approximately $288.6 million, with $137.0 million available on the revolver (0001193125-26-336705:8k_2_02:37).", "account": "cash and cash equivalents", "expected_direction": "up", "horizon": "year-end 2026 outlook against the 2026-06-30 balance", "quote": "Following, the special distribution, we expect to end the year with between $700 and $750 million of cash with no outstanding debt allowing us to further invest in Vistance.", "paragraph_id": "0001193125-26-336705:8k_2_02:16" }
```

```json
{ "id": "estimates_and_discretion_expected_tax_refund_from_divestiture_strategy", "what_changed": "Management expects a $160 million tax refund in 2027 from its divestiture tax strategy. The release balance sheet prints prepaid expenses and other current assets of 230.4 and deferred income tax assets of 460.2 at June 30, 2026 (0001193125-26-336705:8k_2_02:57). The release does not say where the expected refund sits.", "account": "income taxes receivable / deferred tax assets", "expected_direction": "up", "horizon": "2027", "quote": "In addition in 2027, we expect a tax refund of $160 million related to our divesture tax strategy.", "paragraph_id": "0001193125-26-336705:8k_2_02:16" }
```

```json
{ "id": "liquidity_and_capital_release_operating_cash_used_in_quarter", "what_changed": "The release prints quarterly operating cash use of $72.7 million and free cash flow of $(74.7) million. Its cash flow statement prints (72.7) against 77.1 in the prior-year quarter, with prepaid expenses and other assets of (163.2) and inventories of (61.3) among the changes (0001193125-26-336705:8k_2_02:58). The release says these cash flows include discontinued operations (0001193125-26-336705:8k_2_02:13).", "account": "net cash from operating activities", "expected_direction": "down", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "GAAP cash flow used in operations in the second quarter of 2026 was $72.7 million.", "paragraph_id": "0001193125-26-336705:8k_2_02:34" }
```


```json
{ "id": "articulation_and_the_filed_history_release_cash_flow_columns_disagree_on_period_end_cash", "what_changed": "The release cash flow statement prints two different figures for 'cash, cash equivalents and restricted cash at end of period' on the same date, June 30, 2026: 95.1 in the three-months column and 151.6 in the six-months column. The three-months column then prints 'Less: Restricted cash in prepaid expenses and other assets' of 56.5, where the six-months column prints —. Both columns print cash and cash equivalents at end of period of 151.6. Separately, the release says the 151.6 includes $38.0 million in assets held for sale (0001193125-26-336705:8k_2_02:36), and the balance sheet prints cash and cash equivalents of 113.6. My input holds no articulation check covering this, so it is reported as printed, with no arithmetic.", "account": "cash, cash equivalents and restricted cash", "expected_direction": "none", "horizon": "2026-06-30, three-month and six-month columns", "quote": "| Cash, cash equivalents and restricted cash at end of period |  |  | 95.1 |  |  |  | 571.1 |  |  |  | 151.6 |  |  |  | 571.1 |  |", "paragraph_id": "0001193125-26-336705:8k_2_02:58" }
```

```json
{ "id": "earnings_quality_tax_benefit_turns_pretax_loss_into_quarterly_income", "what_changed": "For the quarter the release prints:\n- loss from continuing operations before income taxes of (2.6), against 8.4 a year earlier;\n- an income tax benefit of 28.7, against an expense of (2.5);\n- income from continuing operations of 26.1, against 5.9 (342.4% in the summary table).\n\nOperating income (loss) prints (8.9) against 7.8. The non-GAAP reconciliation prints tax effects of adjustments and other tax items of (39.6) against (9.2) (0001193125-26-336705:8k_2_02:59).", "account": "income tax (expense) benefit, continuing operations", "expected_direction": "up", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "| Income tax (expense) benefit |  |  | 28.7 |", "paragraph_id": "0001193125-26-336705:8k_2_02:56" }
```

```json
{ "id": "earnings_quality_prepaid_and_other_current_assets_jump", "what_changed": "The release balance sheet prints prepaid expenses and other current assets of 230.4 at June 30, 2026, against 46.0 at December 31, 2025; the 10-K printed 56500000 for that date. The quarter's cash flow statement prints a change in prepaid expenses and other assets of (163.2). Its three-months column shows restricted cash of 56.5 held in prepaid expenses and other assets (0001193125-26-336705:8k_2_02:58). The release does not say what else the balance holds.", "account": "prepaid expenses and other current assets", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "| Prepaid expenses and other current assets |  |  | 230.4 |  |  |  | 46.0 |  |", "paragraph_id": "0001193125-26-336705:8k_2_02:57" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_asset_reduction", "what_changed": "The release balance sheet prints noncurrent deferred income tax assets of 460.2 at June 30, 2026, against 1,722.3 at December 31, 2025; the 10-K printed 1765900000 for that date. The cash flow statement prints deferred income taxes of 1,236.0 for the six months and (229.5) for the quarter (0001193125-26-336705:8k_2_02:58).", "account": "deferred income tax assets", "expected_direction": "down", "horizon": "2026-06-30 against 2025-12-31", "quote": "| Deferred income taxes |  |  | 460.2 |  |  |  | 1,722.3 |  |", "paragraph_id": "0001193125-26-336705:8k_2_02:57" }
```

```json
{ "id": "structure_and_disclosure_changes_all_periods_recast_for_ruckus_sale", "what_changed": "The release says that, with RUCKUS sold on July 1, 2026, the results relate to continuing operations of the remaining Aurora segment, and that all periods presented have been recast. The trend table mixes recast and earlier-filed inputs (see the structure items above). The release also says its cash flows are not segregated between continuing and discontinued operations (0001193125-26-336705:8k_2_02:13).", "account": "presentation of continuing and discontinued operations", "expected_direction": "none", "horizon": "all periods presented in the release", "quote": "For all periods presented, amounts have been recast to reflect these changes.", "paragraph_id": "0001193125-26-336705:8k_2_02:18" }
```

```json
{ "id": "earnings_quality_release_adjusted_gross_profit_share_by_quarter", "what_changed": "The release prints adjusted gross profit as a share of sales of 45.8% (Q2 2025), 35.6% (Q3 2025), 37.2% (Q4 2025), 39.0% (Q1 2026) and 35.3% (Q2 2026). For the same quarters it prints GAAP gross profit, as reported, of 148.2, 120.4, 129.2, 116.3 and 112.9. In the trend table, the quarters-back-0 gross margin is 0.3532540675844806, 'lowest of the 6 filled quarters'.", "account": "gross profit as a share of sales", "expected_direction": "down", "horizon": "Q2 2025 through Q2 2026", "quote": "| Adjusted gross profit as % of sales |  | 45.8 | % |  | 35.6 | % |  | 37.2 | % |  | 39.0 | % |  | 35.3 | % |", "paragraph_id": "0001193125-26-336705:8k_2_02:65" }
```

```json
{ "id": "earnings_quality_transition_service_income_falls", "what_changed": "Transition service agreement income prints 0.5 for the quarter against 10.3 a year earlier, and 1.6 for the six months against 19.0. The segment footnote says corporate costs tied to RUCKUS will be reallocated to the remaining segment from the third quarter of 2026, partly offset by income from the Belden TSA (0001193125-26-336705:8k_2_02:31).", "account": "transition service agreement income", "expected_direction": "down", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "| Transition service agreement income |  |  | 0.5 |  |  |  | 10.3 |", "paragraph_id": "0001193125-26-336705:8k_2_02:56" }
```

```json
{ "id": "earnings_quality_release_non_gaap_income_against_gaap", "what_changed": "The release prints non-GAAP adjusted net income of $28.2 million against GAAP income from continuing operations of $26.1 million for the quarter, and $36.7 million against $5.9 million a year earlier. The trend table's non_gaap_gap cell is not filled, because no us-gaap concept carries a non-GAAP measure, so no gap is computed. The non-GAAP per-share figure uses diluted shares of 233.8 million and 272.6 million (0001193125-26-336705:8k_2_02:59).", "account": "non-GAAP adjusted net income", "expected_direction": "down", "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30", "quote": "Non-GAAP adjusted net income for the second quarter of 2026 was $28.2 million, or $0.12 per diluted share, decreased compared to $36.7 million, or $0.13 per diluted share, in the same prior year period.", "paragraph_id": "0001193125-26-336705:8k_2_02:21" }
```

## Seen in the notes

No items. None of the facts I read in input_numbers.json carries a field saying whether its element sat inside a note. Each fact prints only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession and filing_date, plus superseded_by on some. This holds in both the 10-K and the 10-Q ranges I read, including dimensional facts such as share-based award activity, restructuring by plan and revenue by geography. Without that mark I do not judge which facts came from a note, so every fact-based item above sits under the statements heading. Facts I did not read (see the opening paragraphs) could carry the mark, and that is unverified.
