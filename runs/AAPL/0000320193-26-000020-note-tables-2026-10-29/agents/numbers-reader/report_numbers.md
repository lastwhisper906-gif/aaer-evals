# Numbers report: Apple Inc., quarterly report for the third quarter of fiscal 2026 (period ended June 27, 2026, filed July 31, 2026)

## What my directory holds, and what it does not

- I read all four input files in full: the earnings release, the numeric facts, the prior predictions and the trend table. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.
- **Prior flags.** There are none on record. The prior-predictions file says this company has no earlier run, so I carry nothing forward.
- **Articulation checks.** My directory holds none, so I have no articulation gap to report.
- **Restatement traces.** My directory holds no separate restatement trace. I found restated prior values only through the "superseded" marks on the numeric facts. Only one value changed when it was filed again: other non-current assets at September 27, 2025 (items below). Every other superseded fact I read was filed again with the same value.
- **Changes of tag.** No input says that any period rests on a different concept. Every trend cell uses the same tags in every period, so I report no change of tag.
- **Fourth-quarter derivation.** It is not in my directory. Two quarters the table asks for therefore have no cells at all: the fourth quarter of fiscal 2025 (target September 27, 2025) and the fourth quarter of fiscal 2024 (target September 28, 2024). The reason the table prints begins "no quarter ending within 20 days of 2025-09-27 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration". It gives the same reason for September 28, 2024. The table then says the quarter has to be derived from the annual report and the three quarterly reports, and that derivation is not in my input.
- **Formula baseline for research and development capitalized.** For fiscal 2025 this block prints values but no paragraph id, so I cannot quote it and do not itemize it. Its capitalized-development-cost input is missing for fiscal 2025.
- **Note markers.** No numeric fact carries a marker saying whether its element sat inside a note. The "Seen in the notes" heading below is therefore empty. Facts that look like note-table figures are reported under the statements, as numeric facts.
- **How I set expected_direction.**
  - For a trend cell, it is the sign of the change the table printed. Where the change against the prior quarter and the change against the prior year disagree, or no change is printed, it is "none".
  - For a pair of printed figures, it is the direction the later figure stands against the earlier one. I compute no difference.

## Seen in the statements

### Trend table: the third quarter of fiscal 2026

```json
{ "id": "earnings_quality_accruals_quarterly_cell_insufficient",
  "what_changed": "insufficient. The accruals-over-total-assets cell for the third quarter of fiscal 2026 is empty because the record holds no operating cash flow for the three months alone. The numeric facts hold only the nine-month figure (116996000000), and I do not derive a quarter from it. The earnings release calls June-quarter operating cash flow a record, but no three-month figure for it exists in my input. Across the whole quarterly series this ratio is filled in only two quarters, which supports no trend claim.",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "no row for operating_cash_flow in 2026-03-29..2026-06-27",
  "paragraph_id": "0000320193-26-000020:trends:accruals_over_total_assets:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_quarterly_cell_insufficient",
  "what_changed": "insufficient. The record holds no allowance for credit losses at June 27, 2026. This ratio is filled in no period the table holds, quarterly or annual.",
  "account": "allowance for doubtful accounts over receivables",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "no row for bad_debt_allowance in 2026-06-27",
  "paragraph_id": "0000320193-26-000020:trends:bad_debt_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_cell",
  "what_changed": "Current contract liabilities over quarterly revenue is 0.08717109772704425. The table prints a change of 0.003247151835549064 against the second quarter of fiscal 2026 and -0.008313610257132023 against the third quarter of fiscal 2025. Inputs: current contract liabilities of 9538000000 at June 27, 2026 and revenue of 109417000000. Six quarters are filled; the two fourth quarters are missing.",
  "account": "deferred revenue (current contract liabilities) against revenue",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "third highest of the 6 filled quarters",
  "paragraph_id": "0000320193-26-000020:trends:contract_liabilities_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_quarterly_cell",
  "what_changed": "Days sales of inventory is 18.47076692224642. The table prints a change of 7.585228918948722 against the second quarter of fiscal 2026 and 7.755416550610027 against the third quarter of fiscal 2025. Inputs: inventory of 11092000000 at June 27, 2026 and cost of sales of 54647000000. The release prints inventories of 11,092 against 5,718 at September 27, 2025, and an inventory cash outflow of (5,461) for the nine months.",
  "account": "inventories",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "highest of the 6 filled quarters",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_of_inventory:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_cell",
  "what_changed": "Days sales outstanding is 26.113108566310537. The table prints a change of 1.2817569329819989 against the second quarter of fiscal 2026 and -0.5541996986092812 against the third quarter of fiscal 2025. Inputs: trade receivables of 31398000000 at June 27, 2026 and revenue of 109417000000.",
  "account": "accounts receivable, net",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "second highest of the 6 filled quarters",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_outstanding:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_cell",
  "what_changed": "Gross margin is 0.500562069879452. The table prints a change of 0.007856284874415254 against the second quarter of fiscal 2026 and 0.035655013007615644 against the third quarter of fiscal 2025. Inputs: revenue of 109417000000 and cost of sales of 54647000000. The release says this margin includes about 2 percentage points from tariff refunds (separate item below), and no figure without the refunds exists in my input.",
  "account": "gross margin: revenue and cost of sales",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "highest of the 6 filled quarters",
  "paragraph_id": "0000320193-26-000020:trends:gross_margin:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_quarterly_cell_insufficient",
  "what_changed": "insufficient. No inventory valuation reserve is tagged in any period, so this ratio is filled nowhere. The reserve behind the inventory build cannot be read from my input.",
  "account": "inventory valuation reserve over inventory",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.",
  "paragraph_id": "0000320193-26-000020:trends:inventory_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell_insufficient",
  "what_changed": "insufficient. No non-GAAP net income exists in my input, so the gap between adjusted and reported earnings cannot be read.",
  "account": "non-GAAP net income against reported net income",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only",
  "paragraph_id": "0000320193-26-000020:trends:non_gaap_gap:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_cell",
  "what_changed": "Receivables over quarterly revenue is 0.2869572369924235. The table prints a change of 0.014085241021780215 against the second quarter of fiscal 2026 and -0.006090106578123977 against the third quarter of fiscal 2025. Inputs: trade receivables of 31398000000 and revenue of 109417000000.",
  "account": "accounts receivable, net, against revenue",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "second highest of the 6 filled quarters",
  "paragraph_id": "0000320193-26-000020:trends:receivables_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_cell",
  "what_changed": "Soft-asset share is 0.7626322188767071. The table prints a change of 0.020494362553845846 against the second quarter of fiscal 2026 and 0.018373632774352555 against the third quarter of fiscal 2025. Inputs: total assets of 383266000000, cash of 39544000000 and net property, plant and equipment of 51431000000 at June 27, 2026.",
  "account": "total assets less cash and less net property, plant and equipment, over total assets",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "third highest of the 6 filled quarters",
  "paragraph_id": "0000320193-26-000020:trends:soft_asset_share:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_quarterly_cell_insufficient",
  "what_changed": "insufficient. The record holds no warranty accrual at June 27, 2026. Across every period the table holds, this ratio is filled only in fiscal 2021, a single point that supports no trend claim.",
  "account": "product warranty accrual over revenue",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "no row for warranty_accrual in 2026-06-27",
  "paragraph_id": "0000320193-26-000020:trends:warranty_reserve_ratio:2026-03-29..2026-06-27" }
```

### Trend table: fiscal 2025

```json
{ "id": "earnings_quality_accruals_annual_cell",
  "what_changed": "Accruals over total assets for fiscal 2025 is 0.0014697654220982572. The table prints a change of 0.06864604905407809 against fiscal 2024. Inputs: net income of 112010000000 and operating cash flow of 111482000000, both from the annual report filed October 31, 2025, and total assets of 359241000000 at September 27, 2025, taken from the third-quarter quarterly report. Total assets at that date is printed the same in all three filings.",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "up",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "highest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:accruals_over_total_assets:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_annual_cell_insufficient",
  "what_changed": "insufficient. The record holds no allowance for credit losses at September 27, 2025. This ratio is filled in none of the five years.",
  "account": "allowance for doubtful accounts over receivables",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "no row for bad_debt_allowance in 2025-09-27",
  "paragraph_id": "0000320193-26-000020:trends:bad_debt_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_cell",
  "what_changed": "Current contract liabilities over annual revenue is 0.02175840600152345 for fiscal 2025. The table prints a change of 0.0006631076266976656 against fiscal 2024. Inputs: current contract liabilities of 9055000000 at September 27, 2025 and revenue of 416161000000.",
  "account": "deferred revenue (current contract liabilities) against revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "highest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:contract_liabilities_over_revenue:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_annual_cell",
  "what_changed": "Days sales of inventory is 9.419587255611875 for fiscal 2025. The table prints a change of -3.1883461132175164 against fiscal 2024. Inputs: inventory of 5718000000 at September 27, 2025 and cost of sales of 220960000000.",
  "account": "inventories",
  "expected_direction": "down",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "second lowest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_of_inventory:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_cell",
  "what_changed": "Days sales outstanding is 34.79141005524304 for fiscal 2025. The table prints a change of 3.6912783534772124 against fiscal 2024. Inputs: trade receivables of 39777000000 at September 27, 2025 and revenue of 416161000000.",
  "account": "accounts receivable, net",
  "expected_direction": "up",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "highest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_outstanding:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_cell",
  "what_changed": "Gross margin is 0.4690516410716045 for fiscal 2025. The table prints a change of 0.0069881429192651945 against fiscal 2024. Inputs: revenue of 416161000000 and cost of sales of 220960000000.",
  "account": "gross margin: revenue and cost of sales",
  "expected_direction": "up",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "highest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:gross_margin:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_annual_cell_insufficient",
  "what_changed": "insufficient. No inventory valuation reserve is tagged in any period, so this ratio is filled in none of the five years.",
  "account": "inventory valuation reserve over inventory",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.",
  "paragraph_id": "0000320193-26-000020:trends:inventory_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell_insufficient",
  "what_changed": "insufficient. No non-GAAP net income exists in my input for fiscal 2025.",
  "account": "non-GAAP net income against reported net income",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only",
  "paragraph_id": "0000320193-26-000020:trends:non_gaap_gap:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_cell",
  "what_changed": "Receivables over annual revenue is 0.09558079685506331 for fiscal 2025. The table prints a change of 0.010140874597464877 against fiscal 2024. Inputs: trade receivables of 39777000000 at September 27, 2025 and revenue of 416161000000.",
  "account": "accounts receivable, net, against revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "highest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:receivables_over_revenue:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_cell",
  "what_changed": "Soft-asset share is 0.7612521956012815 for fiscal 2025. The table prints a change of -0.03155014973270931 against fiscal 2024. Inputs: total assets of 359241000000, cash of 35934000000 and net property, plant and equipment of 49834000000 at September 27, 2025.",
  "account": "total assets less cash and less net property, plant and equipment, over total assets",
  "expected_direction": "down",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "lowest of the 5 filled years",
  "paragraph_id": "0000320193-26-000020:trends:soft_asset_share:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_annual_cell_insufficient",
  "what_changed": "insufficient. The record holds no warranty accrual at September 27, 2025. Of the five years, the ratio is filled only in fiscal 2021.",
  "account": "product warranty accrual over revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "no row for warranty_accrual in 2025-09-27",
  "paragraph_id": "0000320193-26-000020:trends:warranty_reserve_ratio:2024-09-29..2025-09-27" }
```

### Restated prior values

```json
{ "id": "articulation_and_the_filed_history_other_noncurrent_assets_as_first_filed",
  "what_changed": "Restated prior value. The annual report filed October 31, 2025 reported other non-current assets at September 27, 2025 as 83727000000. The fact is marked superseded by the third-quarter quarterly report, which carries 72634000000 for the same date. Total non-current assets (211284000000) and total assets (359241000000) at that date are printed the same in the annual report and both later quarterly reports. Neither later filing re-reports the annual report's own breakdown of the balance, so my input cannot show which part moved.",
  "account": "other non-current assets",
  "expected_direction": "down",
  "horizon": "the balance sheet at September 27, 2025, as first filed in the annual report",
  "quote": "83727000000",
  "paragraph_id": "0000320193-25-000079:facts:OtherAssetsNoncurrent:2025-09-27" }
```

```json
{ "id": "articulation_and_the_filed_history_other_noncurrent_assets_as_refiled",
  "what_changed": "Restated prior value, as refiled. The third-quarter quarterly report carries other non-current assets at September 27, 2025 as 72634000000, against 83727000000 in the annual report. The release prints the same comparative, 72,634, beside a new balance-sheet line for intangible assets, net. No number in my input reconciles the two filings.",
  "account": "other non-current assets",
  "expected_direction": "down",
  "horizon": "the balance sheet at September 27, 2025, as carried in the quarterly report for the third quarter of fiscal 2026",
  "quote": "72634000000",
  "paragraph_id": "0000320193-26-000020:facts:OtherAssetsNoncurrent:2025-09-27" }
```

```json
{ "id": "articulation_and_the_filed_history_other_noncurrent_assets_in_earlier_quarterly_report",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026, filed May 1, 2026, already carried other non-current assets at September 27, 2025 as 72634000000, not the annual report's 83727000000. The quarterly report for the first quarter of fiscal 2026 is not among my numeric facts, so I cannot say in which filing the change first appeared.",
  "account": "other non-current assets",
  "expected_direction": "down",
  "horizon": "the balance sheet at September 27, 2025, as carried in the quarterly report for the second quarter of fiscal 2026",
  "quote": "72634000000",
  "paragraph_id": "0000320193-26-000013:facts:OtherAssetsNoncurrent:2025-09-27" }
```

### Structure, and figures across documents

```json
{ "id": "structure_and_disclosure_changes_intangible_assets_new_balance_sheet_line",
  "what_changed": "The release's balance sheet prints a line for intangible assets, net: 20,342 at June 27, 2026 and 11,093 at September 27, 2025, in millions. No fact in my input carries this balance-sheet line in either quarterly report, and the annual report's balance sheet in my input has no such line for September 27, 2025. The same comparative date is where other non-current assets was refiled lower (items above). The line is a presentation change that my tagged numbers do not trace.",
  "account": "intangible assets, net, and other non-current assets",
  "expected_direction": "up",
  "horizon": "the balance sheet at June 27, 2026 against September 27, 2025",
  "quote": "Intangible assets, net | 20,342",
  "paragraph_id": "0000320193-26-000018:8k_2_02:33" }
```

```json
{ "id": "across_documents_intangible_assets_note_fact_against_release_line",
  "what_changed": "The third-quarter quarterly report tags intangible assets, net, excluding goodwill as 25417000000 at June 27, 2026 and 13301000000 at September 27, 2025. Gross amounts are 38220000000 and 24950000000; accumulated amortization is 12803000000 and 11649000000. The second-quarter quarterly report tagged 25797000000 at March 28, 2026. The release's balance-sheet line prints 20,342 and 11,093. These printed figures are not the same, and nothing in my input reconciles them or says on which line any remainder sits.",
  "account": "intangible assets, net",
  "expected_direction": "none",
  "horizon": "June 27, 2026 and September 27, 2025, quarterly report against earnings release",
  "quote": "25417000000",
  "paragraph_id": "0000320193-26-000020:facts:IntangibleAssetsNetExcludingGoodwill:2026-06-27" }
```

```json
{ "id": "earnings_quality_gross_margin_printed_with_tariff_refunds",
  "what_changed": "The release attributes about 2 percentage points of the quarter's gross margin to tariff refunds. The trend cell's 0.500562069879452, the highest of six filled quarters, includes that benefit. My input holds no tagged figure for the refunds and no gross margin without them.",
  "account": "cost of sales: tariff refunds",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "Company gross margin was 50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7" }
```

```json
{ "id": "earnings_quality_diluted_earnings_printed_with_tariff_refunds",
  "what_changed": "Diluted earnings per share is 2.02 in the release and in the quarterly report's fact, against 1.57 in the third quarter of fiscal 2025. The release says 0.11 of it comes from tariff refunds. No tagged figure in my input isolates the refund.",
  "account": "net income: tariff refunds",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026, against the third quarter of fiscal 2025",
  "quote": "Diluted earnings per share was $2.02, up 29 percent year over year, and included a favorable impact of $0.11 from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7" }
```

```json
{ "id": "estimates_and_discretion_inventory_build_in_components",
  "what_changed": "Raw materials and purchased parts, net of reserves, are 7645000000 at June 27, 2026 against 2124000000 at September 27, 2025. Finished goods are 3447000000 against 3594000000. The inventory build behind the days-of-inventory reading sits in components, not finished goods. No inventory reserve is tagged in any period, so the reserve against the build cannot be read.",
  "account": "inventories: components and finished goods",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against September 27, 2025",
  "quote": "7645000000",
  "paragraph_id": "0000320193-26-000020:facts:InventoryRawMaterialsAndPurchasedPartsNetOfReserves:2026-06-27" }
```

```json
{ "id": "revenue_recognition_total_contract_liabilities",
  "what_changed": "Total contract liabilities are 14900000000 at June 27, 2026 against 13700000000 at September 27, 2025. Revenue recognized out of contract liabilities is tagged at 4086000000 for the third quarter of fiscal 2026, against 4015000000 for the third quarter of fiscal 2025.",
  "account": "deferred revenue (total contract liabilities)",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against September 27, 2025",
  "quote": "14900000000",
  "paragraph_id": "0000320193-26-000020:facts:ContractWithCustomerLiability:2026-06-27" }
```

```json
{ "id": "revenue_recognition_single_customer_share_of_trade_receivables",
  "what_changed": "The customer the filer tags as CustomerOneMember holds 0.18 of trade receivables in the period to June 27, 2026. That compares with 0.17 in the second-quarter quarterly report and 0.12 for fiscal 2025. Cellular network carriers hold 0.27, against 0.34 for fiscal 2025.",
  "account": "accounts receivable: credit concentration",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026, against fiscal 2025",
  "quote": "0.18",
  "paragraph_id": "0000320193-26-000020:facts:ConcentrationRiskPercentage1:2025-09-28..2026-06-27:srt:MajorCustomersAxis=aapl:CustomerOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:TradeAccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CreditConcentrationRiskMember" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_and_working_capital",
  "what_changed": "Operating cash flow for the first nine months of fiscal 2026 is 116996000000, against 81754000000 a year earlier. Within it:\n- Other current and non-current assets used 16266000000 (6116000000 a year earlier).\n- Other current and non-current liabilities provided 10016000000; a year earlier they used 15161000000.\n- Income taxes paid were 26555000000, against 37332000000.\nNo three-month operating cash flow exists in my input.",
  "account": "cash generated by operating activities",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026, against the first nine months of fiscal 2025",
  "quote": "116996000000",
  "paragraph_id": "0000320193-26-000020:facts:NetCashProvidedByUsedInOperatingActivities:2025-09-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_other_noncurrent_liabilities",
  "what_changed": "The release prints other non-current liabilities of 55,080 at June 27, 2026 against 41,549 at September 27, 2025, in millions. My input holds no breakdown of this line at June 27, 2026, so what grew cannot be read.",
  "account": "other non-current liabilities",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against September 27, 2025",
  "quote": "Other non-current liabilities | 55,080",
  "paragraph_id": "0000320193-26-000018:8k_2_02:33" }
```

```json
{ "id": "liquidity_and_capital_term_debt_and_commercial_paper",
  "what_changed": "Term debt is tagged at 82300000000 at June 27, 2026 against 90700000000 at September 27, 2025. Commercial paper is tagged at 2000000000 against 8000000000. No long-term debt was issued in the nine months (0, against 4481000000 a year earlier), and 8146000000 was repaid.",
  "account": "term debt and commercial paper",
  "expected_direction": "down",
  "horizon": "June 27, 2026 against September 27, 2025",
  "quote": "82300000000",
  "paragraph_id": "0000320193-26-000020:facts:LongTermDebt:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_dividend_declared_per_share",
  "what_changed": "Dividends declared per share are 0.27 in the third quarter of fiscal 2026, against 0.26 in the third quarter of fiscal 2025 and 0.26 in the second quarter of fiscal 2026. The release declares 0.27, payable August 13, 2026.",
  "account": "dividends",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "0.27",
  "paragraph_id": "0000320193-26-000020:facts:CommonStockDividendsPerShareDeclared:2026-03-29..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases",
  "what_changed": "Repurchases paid are 62094000000 in the first nine months of fiscal 2026, against 70579000000 a year earlier. The debt-and-equity facts tag 215000000 shares retired for 61800000000.",
  "account": "repurchases of common stock",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026, against the first nine months of fiscal 2025",
  "quote": "62094000000",
  "paragraph_id": "0000320193-26-000020:facts:PaymentsForRepurchaseOfCommonStock:2025-09-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_research_and_development_expense",
  "what_changed": "Research and development expense is 11729000000 in the third quarter of fiscal 2026, against 8866000000 in the third quarter of fiscal 2025 and 11419000000 in the second quarter of fiscal 2026. For the nine months it is 34035000000, against 25684000000.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026, against the second quarter of fiscal 2026 and the third quarter of fiscal 2025",
  "quote": "11729000000",
  "paragraph_id": "0000320193-26-000020:facts:ResearchAndDevelopmentExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_ipad_revenue_lower",
  "what_changed": "iPad revenue is 6191000000 in the third quarter of fiscal 2026, against 6581000000 in the third quarter of fiscal 2025. It is the only product or service category whose quarterly revenue is lower than a year earlier: iPhone, Mac, Wearables, Home and Accessories, and Services are all higher.",
  "account": "revenue: iPad",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026, against the third quarter of fiscal 2025",
  "quote": "6191000000",
  "paragraph_id": "0000320193-26-000020:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-03-29..2026-06-27:srt:ProductOrServiceAxis=aapl:IPadMember" }
```

## Seen in the notes

This heading has no items. No numeric fact in my input carries the marker that says whether its element sat inside a note when it was extracted, and I am not to judge that myself.

Some facts above look like note-table figures: the intangible-asset amounts, the inventory components, the contract liabilities, the credit concentrations and the term debt. They are reported under the statements because only the marker could move them here. A run whose directory name says "note tables" should have carried that marker, so its absence looks like a gap in the pipeline rather than a property of the filing.
