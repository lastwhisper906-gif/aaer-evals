<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
Palo Alto Networks: numbers read for the quarterly report for the third quarter of fiscal 2026 (three months ended April 30, 2026, filed June 3, 2026).

**Broken-run check.** Nothing in my directory carries prices, abnormal returns, short interest, another company's files, a prior probability or an outcome window. The prior-flags file says no earlier run is on record, so there are no flags to carry forward.

**How much of the input I read.** I read the trend table in full, and the current-report listing and the prior-flags file in full. The numeric-facts file has 93,456 lines and is larger than my context can hold. From it I read:
- the header and the list of three documents;
- the current quarterly report's balance sheet, from short-term investments through total liabilities and stockholders' equity;
- the current report's income statement, from product revenue through diluted loss per share;
- short samples from the annual report for fiscal 2025, the quarterly report for the second quarter of fiscal 2026, and the current report's investment and revenue-breakdown facts.

I did not read the other facts, including the current report's cash and cash-flow rows, so nothing from them appears below. If an item is absent here, that does not mean the fact is absent from the filing.

**What the bundle does not hold.**
- No articulation checks, so there is no articulation gap to report. That is a gap in the bundle, not a finding that the statements articulate.
- No restatement traces, so no restated prior value can be reported from them.
- No fourth-quarter derivation. The trend table's reason text points to a separate program for it, but the derivation itself is not in my input.
- No earnings-release figures. The current-report file opens by saying no current report filed on or before June 3, 2026 is on record. Its own list then shows one dated June 2, 2026 carrying the results-of-operations item and the exhibits item. The input contradicts itself, and the release body is not here, so nothing below is checked against a release.
- No change of tag: in every filled trend cell, each formula input rests on the same concept in every period.
- No inside-a-note marker on any fact I read. Every fact row carries the same fields (id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date). None of them says whether the element sat inside a note. I was told not to judge this myself, so every fact item below sits under the first heading and the second heading holds no items. Some of these facts carry a breakdown member (product or service, region, fair-value level, award type), and nothing in the input says whether they came from a note table. A later split cannot rely on where I placed them.

**Periods the record does not reach.** The fourth quarter of fiscal 2025 (ended July 31, 2025) and the fourth quarter of fiscal 2024 (target end August 1, 2024) have no cells at all. The reason each period gives: "no quarter ending within 20 days of 2025-07-31 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration" (the same wording, with 2024-08-01, for the earlier quarter). As a result, the first-quarter cells have no quarter-over-quarter comparison.

**Research-and-development capitalization block.** The annual cells print this block with no paragraph_id, so I cannot quote it as an item. For fiscal 2025 it prints:
- earnings with research and development capitalized: 1770080000.0 (net income 1133900000.0);
- book value with research and development capitalized: 13013180000.0 (stockholders' equity 7824000000.0);
- capitalized development cost and its ratio to expense: missing, because the record tags no capitalized software additions in any period. Both are insufficient.

**How the fields are filled.**
- `expected_direction` is the direction of the printed change, not a forecast from anything outside the input. For quarterly cells it is the direction both printed comparisons agree on. For annual cells it is the year-over-year change. For facts it is the current value against the comparison date in the same report.
- It is `none` for an insufficient cell, for an item with nothing to compare, or where the printed change is a single rounding step.
- `horizon` is the next filed figures, through the annual report for fiscal 2026.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_ratio_quarterly_trend", "what_changed": "insufficient: accruals over total assets cannot be filled for the third quarter of fiscal 2026 because the record holds operating cash flow only year-to-date, not for the three months ended April 30, 2026. The quarterly measure is filled only for the first quarter of fiscal 2026 and the first quarter of fiscal 2025 (2 filled quarters), which supports no quarterly trend.", "account": "net income against operating cash flow, over total assets", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"missing\": \"no row for operating_cash_flow in 2026-02-01..2026-04-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0001327567-26-000015:trends:accruals_over_total_assets:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend", "what_changed": "Bad-debt reserve ratio for the third quarter of fiscal 2026 is 0.002099370188943317. Change against the second quarter of fiscal 2026 is -0.004006782934588858; against the third quarter of fiscal 2025 it is -0.0033071380228285895. It sits lowest of the 6 filled quarters. Inputs: allowance 6000000.0 and receivables 2852000000.0 at April 30, 2026; the second-quarter cell's inputs are 13000000.0 and 2116000000.0. The allowance prints in whole millions, so this ratio moves in coarse steps. Six quarters is a short history.", "account": "allowance for doubtful accounts against gross receivables", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend", "what_changed": "Current contract liabilities over quarterly revenue for the third quarter of fiscal 2026 is 2.3694203864090606. Change against the second quarter of fiscal 2026 is -0.03921492584999875; against the third quarter of fiscal 2025 it is -0.1455643230710617. It sits lowest of the 6 filled quarters. Inputs: current contract liabilities 7113000000.0 at April 30, 2026 and revenue 3002000000.0; the second-quarter cell's inputs are 6248000000.0 and 2594000000.0, so both inputs rose while the ratio fell.", "account": "current contract liabilities (deferred revenue) against revenue", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001327567-26-000015:trends:contract_liabilities_over_revenue:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend", "what_changed": "insufficient: days sales of inventory cannot be filled for the third quarter of fiscal 2026 because the record holds no inventory row at April 30, 2026. It is filled in no quarter of the table, only in the fiscal 2025 and fiscal 2024 annual cells.", "account": "inventory against cost of revenue", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"missing\": \"no row for inventory in 2026-04-30: us-gaap:InventoryNet is in the record, but not for this period\"", "paragraph_id": "0001327567-26-000015:trends:days_sales_of_inventory:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend", "what_changed": "Days sales outstanding for the third quarter of fiscal 2026 is 84.55296469020652 (89 days in the period). Change against the second quarter of fiscal 2026 is 9.505933078795579; against the third quarter of fiscal 2025 it is 8.7338296967596. It sits highest of the 6 filled quarters. Inputs: receivables 2852000000.0 at April 30, 2026 and revenue 3002000000.0; the second-quarter cell's receivables are 2116000000.0.", "account": "accounts receivable, net, against revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001327567-26-000015:trends:days_sales_outstanding:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend", "what_changed": "Gross margin for the third quarter of fiscal 2026 is 0.6755496335776149. Change against the second quarter of fiscal 2026 is -0.060379433500257096; against the third quarter of fiscal 2025 it is -0.05402660058577524. It sits lowest of the 6 filled quarters. Inputs: revenue 3002000000.0 and cost of revenue 974000000.0, both from the current report. The input does not say why cost of revenue rose.", "account": "revenue less cost of revenue, over revenue", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001327567-26-000015:trends:gross_margin:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend", "what_changed": "insufficient: the inventory reserve ratio cannot be filled for the third quarter of fiscal 2026, or any period, because the record tags no inventory valuation reserve. The record cannot say whether the company leaves the concept untagged or states it only by segment.", "account": "inventory valuation reserve", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001327567-26-000015:trends:inventory_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend", "what_changed": "insufficient: the gap between non-GAAP and GAAP net income cannot be filled for the third quarter of fiscal 2026 because no us-gaap concept carries a non-GAAP measure, and the earnings release that would carry one is not in the bundle.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001327567-26-000015:trends:non_gaap_gap:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend", "what_changed": "Receivables over quarterly revenue for the third quarter of fiscal 2026 is 0.950033311125916. Change against the second quarter of fiscal 2026 is 0.13430470665405791; against the third quarter of fiscal 2025 it is 0.09813291794111922. It sits highest of the 6 filled quarters. Inputs: receivables 2852000000.0 and revenue 3002000000.0.", "account": "accounts receivable, net, against revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001327567-26-000015:trends:receivables_over_revenue:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend", "what_changed": "Soft-asset share for the third quarter of fiscal 2026 is 0.9379674058704016. Change against the second quarter of fiscal 2026 is 0.12384354182460311; against the third quarter of fiscal 2025 it is 0.06295149880402828. It sits highest of the 6 filled quarters. Inputs: total assets 46266000000.0, property and equipment 506000000.0 and cash 2364000000.0 at April 30, 2026. The second-quarter cell prints total assets 24979000000.0 and cash 4158000000.0 at January 31, 2026.", "account": "total assets less property and equipment and cash, over total assets", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001327567-26-000015:trends:soft_asset_share:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend", "what_changed": "insufficient: the warranty reserve ratio cannot be filled for the third quarter of fiscal 2026, or any period, because the record tags none of the product warranty accrual concepts. The record cannot say whether the company leaves them untagged or states them only by segment.", "account": "product warranty accrual", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001327567-26-000015:trends:warranty_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_accruals_ratio_annual_trend", "what_changed": "Accruals over total assets for fiscal 2025 (year ended July 31, 2025) is -0.10952239565659994; change against fiscal 2024 is -0.07550691861454581. It sits second highest of the 5 filled years. Inputs: net income 1133900000.0 and operating cash flow 3716000000.0 from the fiscal 2025 annual report; total assets 23576000000.0 as re-presented in the current report.", "account": "net income against operating cash flow, over total assets", "expected_direction": "down", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:accruals_over_total_assets:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend", "what_changed": "Bad-debt reserve ratio for fiscal 2025 is 0.0033613445378151263; change against fiscal 2024 is 0.0005053984580771116. It sits third highest of the 5 filled years. Inputs: allowance 10000000.0 and receivables 2965000000.0 at July 31, 2025, both as re-presented in the current report.", "account": "allowance for doubtful accounts against gross receivables", "expected_direction": "up", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend", "what_changed": "Current contract liabilities over annual revenue for fiscal 2025 is 0.6834029170959172; change against fiscal 2024 is -0.006861797946125847. It sits second highest of the 5 filled years. Inputs: current contract liabilities 6302000000.0 at July 31, 2025 and revenue 9221500000.0.", "account": "current contract liabilities (deferred revenue) against revenue", "expected_direction": "down", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:contract_liabilities_over_revenue:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend", "what_changed": "Days sales of inventory for fiscal 2025 is 16.88325991189427; change against fiscal 2024 is -3.7166818130474546. It sits lowest of the 2 filled years. Inputs: inventory 113400000.0 at July 31, 2025 and cost of revenue 2451600000.0. Two years of history: insufficient for any trend claim.", "account": "inventory against cost of revenue", "expected_direction": "none", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"lowest of the 2 filled years\"", "paragraph_id": "0001327567-26-000015:trends:days_sales_of_inventory:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend", "what_changed": "Days sales outstanding for fiscal 2025 is 117.35888955159137 (365 days); change against fiscal 2024 is -2.0316554499657684. It sits second lowest of the 5 filled years. Inputs: receivables 2965000000.0 at July 31, 2025 and revenue 9221500000.0. The annual measure divides by a year of revenue and the quarterly one by a quarter, so the two series are not compared here.", "account": "accounts receivable, net, against revenue", "expected_direction": "down", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:days_sales_outstanding:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend", "what_changed": "Gross margin for fiscal 2025 is 0.734143035297945; change against fiscal 2024 is -0.009338746078573212. It sits second highest of the 5 filled years. Inputs: revenue 9221500000.0 and cost of revenue 2451600000.0.", "account": "revenue less cost of revenue, over revenue", "expected_direction": "down", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:gross_margin:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend", "what_changed": "insufficient: the inventory reserve ratio cannot be filled for fiscal 2025, or any year, because the record tags no inventory valuation reserve.", "account": "inventory valuation reserve", "expected_direction": "none", "horizon": "the annual report for fiscal 2026", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001327567-26-000015:trends:inventory_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend", "what_changed": "insufficient: the gap between non-GAAP and GAAP net income cannot be filled for fiscal 2025, or any year, because no us-gaap concept carries a non-GAAP measure.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "the annual report for fiscal 2026", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001327567-26-000015:trends:non_gaap_gap:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend", "what_changed": "Receivables over annual revenue for fiscal 2025 is 0.3215312042509353; change against fiscal 2024 is -0.0046724706167071695. It sits second lowest of the 5 filled years. Inputs: receivables 2965000000.0 and revenue 9221500000.0.", "account": "accounts receivable, net, against revenue", "expected_direction": "down", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:receivables_over_revenue:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend", "what_changed": "Soft-asset share for fiscal 2025 is 0.8873430607397353; change against fiscal 2024 is -0.017798778797254. It sits third highest of the 5 filled years. Inputs: total assets 23576000000.0, property and equipment 387000000.0 and cash 2269000000.0 at July 31, 2025, all as re-presented in the current report.", "account": "total assets less property and equipment and cash, over total assets", "expected_direction": "down", "horizon": "the annual report for fiscal 2026", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001327567-26-000015:trends:soft_asset_share:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend", "what_changed": "insufficient: the warranty reserve ratio cannot be filled for fiscal 2025, or any year, because the record tags none of the product warranty accrual concepts.", "account": "product warranty accrual", "expected_direction": "none", "horizon": "the annual report for fiscal 2026", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001327567-26-000015:trends:warranty_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "articulation_and_the_filed_history_balance_sheet_totals_print_equal", "what_changed": "Total liabilities and stockholders' equity at April 30, 2026 prints 46266000000, the same figure total assets prints. At July 31, 2025 both print 23576000000. This is a match of printed figures only. Python's articulation checks are not in my input, so no other tie is reported, and none is worked out here.", "account": "total liabilities and stockholders' equity against total assets", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"46266000000\"", "paragraph_id": "0001327567-26-000015:facts:LiabilitiesAndStockholdersEquity:2026-04-30" }
```


```json
{ "id": "structure_and_disclosure_changes_rounding_to_whole_millions", "what_changed": "Precision of the reported figures changed. Inputs from the fiscal 2025 filings and earlier print to tenths of a million: the allowance is 10600000.0 at April 30, 2025, 8500000.0 at January 31, 2025 and 8600000.0 at October 31, 2024, and annual revenue is 9221500000.0. Inputs from fiscal 2026 filings print whole millions: the allowance is 14000000.0, 13000000.0 and 6000000.0. The current report tags its facts with decimals -6, while the second-quarter report's facts that I read carry decimals -5. Small balances such as the allowance therefore move in whole-million steps from the first quarter of fiscal 2026.", "account": "precision of reported amounts", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": 10600000.0", "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2025-02-01..2025-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_total_assets_balance", "what_changed": "Total assets at April 30, 2026 print 46266000000; the July 31, 2025 row in the same report prints 23576000000, and the second-quarter trend cell prints 24979000000.0 at January 31, 2026. The facts I read do not say what caused the change.", "account": "total assets", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"46266000000\"", "paragraph_id": "0001327567-26-000015:facts:Assets:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_balance", "what_changed": "Goodwill at April 30, 2026 prints 21902000000; the July 31, 2025 row in the same report prints 4567000000. The cause is not stated in the facts I read.", "account": "goodwill", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"21902000000\"", "paragraph_id": "0001327567-26-000015:facts:Goodwill:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_intangible_assets_balance", "what_changed": "Intangible assets, net, excluding goodwill, at April 30, 2026 print 7283000000; the July 31, 2025 row prints 763000000.", "account": "intangible assets, net", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"7283000000\"", "paragraph_id": "0001327567-26-000015:facts:IntangibleAssetsNetExcludingGoodwill:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_paid_in_capital_balance", "what_changed": "Common stock and additional paid-in capital at April 30, 2026 print 24608000000; the July 31, 2025 row prints 5292000000.", "account": "common stock and additional paid-in capital", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"24608000000\"", "paragraph_id": "0001327567-26-000015:facts:CommonStocksIncludingAdditionalPaidInCapital:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_common_shares_issued", "what_changed": "Common shares issued at April 30, 2026 print 813000000, and shares outstanding print the same; the July 31, 2025 rows print 668000000 for both.", "account": "common shares issued and outstanding", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"813000000\"", "paragraph_id": "0001327567-26-000015:facts:CommonStockSharesIssued:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_stockholders_equity_balance", "what_changed": "Total stockholders' equity at April 30, 2026 prints 27668000000; the July 31, 2025 row prints 7824000000.", "account": "total stockholders' equity", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"27668000000\"", "paragraph_id": "0001327567-26-000015:facts:StockholdersEquity:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_retained_earnings_balance", "what_changed": "Retained earnings at April 30, 2026 print 3073000000; the July 31, 2025 row prints 2484000000.", "account": "retained earnings", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"3073000000\"", "paragraph_id": "0001327567-26-000015:facts:RetainedEarningsAccumulatedDeficit:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_accumulated_other_comprehensive_income", "what_changed": "Accumulated other comprehensive income at April 30, 2026 prints -13000000; the July 31, 2025 row prints 48000000.", "account": "accumulated other comprehensive income (loss)", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"-13000000\"", "paragraph_id": "0001327567-26-000015:facts:AccumulatedOtherComprehensiveIncomeLossNetOfTax:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_convertible_debt_current_portion", "what_changed": "Convertible debt, current, at April 30, 2026 prints 160000000; the July 31, 2025 row prints 0.", "account": "convertible senior notes, current", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"160000000\"", "paragraph_id": "0001327567-26-000015:facts:ConvertibleDebtCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_convertible_debt_noncurrent_portion", "what_changed": "Convertible debt, noncurrent, at April 30, 2026 prints 1192000000; the July 31, 2025 row prints 0.", "account": "convertible senior notes, noncurrent", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"1192000000\"", "paragraph_id": "0001327567-26-000015:facts:ConvertibleDebtNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_convertible_notes_face_amount", "what_changed": "Face amount of the convertible senior notes due 2030 prints 1250000000 at February 11, 2026. The list of current reports shows one dated February 11, 2026 carrying a material-agreement item and a direct-financial-obligation item, and one dated April 13, 2026 carrying the same two items. Their bodies are not in my input, so they are not tied to this figure.", "account": "convertible senior notes due 2030, face amount", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"1250000000\"", "paragraph_id": "0001327567-26-000015:facts:DebtInstrumentFaceAmount:2026-02-11:us-gaap:DebtInstrumentAxis=panw:ConvertibleSeniorNotesDue2030Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleDebtMember" }
```

```json
{ "id": "liquidity_and_capital_interest_expense_line", "what_changed": "Interest expense for the third quarter of fiscal 2026 prints 0 while convertible notes are on the balance sheet. The third quarter of fiscal 2025 prints 1000000, and the nine months print 0 against 3000000. The change is one whole-million step, so no direction is drawn; the facts I read do not explain the zero.", "account": "interest expense", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"0\"", "paragraph_id": "0001327567-26-000015:facts:InterestExpenseNonoperating:2026-02-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_long_term_investments_balance", "what_changed": "Long-term investments at April 30, 2026 print 3881000000; the July 31, 2025 row prints 5555000000.", "account": "long-term investments", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"3881000000\"", "paragraph_id": "0001327567-26-000015:facts:LongTermInvestments:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_short_term_investments_balance", "what_changed": "Short-term investments at April 30, 2026 print 747000000; the July 31, 2025 row prints 635000000.", "account": "short-term investments", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"747000000\"", "paragraph_id": "0001327567-26-000015:facts:ShortTermInvestments:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_current_assets_balance", "what_changed": "Total current assets at April 30, 2026 print 7713000000; the July 31, 2025 row prints 7523000000.", "account": "total current assets", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"7713000000\"", "paragraph_id": "0001327567-26-000015:facts:AssetsCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_current_liabilities_balance", "what_changed": "Total current liabilities at April 30, 2026 print 9006000000; the July 31, 2025 row prints 7988000000.", "account": "total current liabilities", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"9006000000\"", "paragraph_id": "0001327567-26-000015:facts:LiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_total_liabilities_balance", "what_changed": "Total liabilities at April 30, 2026 print 18598000000; the July 31, 2025 row prints 15752000000.", "account": "total liabilities", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"18598000000\"", "paragraph_id": "0001327567-26-000015:facts:Liabilities:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_balance", "what_changed": "Accounts payable at April 30, 2026 print 293000000; the July 31, 2025 row prints 232000000.", "account": "accounts payable", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"293000000\"", "paragraph_id": "0001327567-26-000015:facts:AccountsPayableCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_balance", "what_changed": "Accrued liabilities at April 30, 2026 print 760000000; the July 31, 2025 row prints 846000000.", "account": "accrued liabilities, current", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"760000000\"", "paragraph_id": "0001327567-26-000015:facts:AccruedLiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_employee_related_liabilities_balance", "what_changed": "Accrued compensation (employee-related liabilities) at April 30, 2026 prints 680000000; the July 31, 2025 row prints 608000000.", "account": "employee-related liabilities, current", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"680000000\"", "paragraph_id": "0001327567-26-000015:facts:EmployeeRelatedLiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_prepaid_and_other_current_assets", "what_changed": "Prepaid expenses and other current assets at April 30, 2026 print 705000000; the July 31, 2025 row prints 520000000.", "account": "prepaid expenses and other current assets", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"705000000\"", "paragraph_id": "0001327567-26-000015:facts:PrepaidExpenseAndOtherAssetsCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_other_noncurrent_liabilities", "what_changed": "Other long-term liabilities at April 30, 2026 print 930000000; the July 31, 2025 row prints 887000000.", "account": "other liabilities, noncurrent", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"930000000\"", "paragraph_id": "0001327567-26-000015:facts:OtherLiabilitiesNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_property_and_equipment_balance", "what_changed": "Property and equipment, net, at April 30, 2026 prints 506000000; the July 31, 2025 row prints 387000000.", "account": "property and equipment, net", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"506000000\"", "paragraph_id": "0001327567-26-000015:facts:PropertyPlantAndEquipmentNet:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_other_noncurrent_assets", "what_changed": "Other noncurrent assets at April 30, 2026 print 593000000; the July 31, 2025 row prints 422000000.", "account": "other assets, noncurrent", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"593000000\"", "paragraph_id": "0001327567-26-000015:facts:OtherAssetsNoncurrent:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_operating_lease_right_of_use_asset", "what_changed": "Operating lease right-of-use assets at April 30, 2026 print 678000000; the July 31, 2025 row prints 347000000.", "account": "operating lease right-of-use assets", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"678000000\"", "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseRightOfUseAsset:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_operating_lease_liability_noncurrent", "what_changed": "Long-term operating lease liabilities at April 30, 2026 print 719000000; the July 31, 2025 row prints 338000000.", "account": "operating lease liabilities, noncurrent", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"719000000\"", "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseLiabilityNoncurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_assets_balance", "what_changed": "Deferred income tax assets, net, at April 30, 2026 print 2380000000; the July 31, 2025 row prints 2424000000.", "account": "deferred income tax assets, net", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2380000000\"", "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxAssetsNet:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_liabilities_balance", "what_changed": "Deferred income tax liabilities, net, at April 30, 2026 print 259000000; the July 31, 2025 row prints 89000000.", "account": "deferred income tax liabilities, net", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"259000000\"", "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxLiabilitiesNet:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_capitalized_contract_costs_current", "what_changed": "Capitalized contract costs (deferred contract costs), current, at April 30, 2026 print 454000000; the July 31, 2025 row prints 419000000.", "account": "capitalized contract costs, current", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"454000000\"", "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostNetCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_capitalized_contract_costs_noncurrent", "what_changed": "Capitalized contract costs, noncurrent, at April 30, 2026 print 551000000; the July 31, 2025 row prints 586000000.", "account": "capitalized contract costs, noncurrent", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"551000000\"", "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostNetNoncurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_allowance_for_doubtful_accounts_balance", "what_changed": "Allowance for doubtful accounts at April 30, 2026 prints 6000000; the July 31, 2025 row prints 10000000. The second-quarter trend cell prints 13000000.0 at January 31, 2026.", "account": "allowance for doubtful accounts", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"6000000\"", "paragraph_id": "0001327567-26-000015:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_accounts_receivable_balance", "what_changed": "Accounts receivable, net, at April 30, 2026 prints 2852000000; the July 31, 2025 row prints 2965000000. The second-quarter trend cell prints 2116000000.0 at January 31, 2026.", "account": "accounts receivable, net", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2852000000\"", "paragraph_id": "0001327567-26-000015:facts:AccountsReceivableNetCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_financing_receivables_current_balance", "what_changed": "Notes and loans receivable (financing receivables), current, at April 30, 2026 print 591000000; the July 31, 2025 row prints 715000000.", "account": "financing receivables, current", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"591000000\"", "paragraph_id": "0001327567-26-000015:facts:NotesAndLoansReceivableNetCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_financing_receivables_noncurrent_balance", "what_changed": "Notes and loans receivable, noncurrent, at April 30, 2026 print 779000000; the July 31, 2025 row prints 1002000000.", "account": "financing receivables, noncurrent", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"779000000\"", "paragraph_id": "0001327567-26-000015:facts:NotesAndLoansReceivableNetNoncurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_noncurrent_balance", "what_changed": "Contract liabilities (deferred revenue), noncurrent, at April 30, 2026 print 6492000000; the July 31, 2025 row prints 6450000000. The current portion prints 7113000000 against 6302000000.", "account": "contract liabilities, noncurrent", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"6492000000\"", "paragraph_id": "0001327567-26-000015:facts:ContractWithCustomerLiabilityNoncurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_total_revenue_line", "what_changed": "Total revenue for the third quarter of fiscal 2026 prints 3002000000; the third quarter of fiscal 2025 prints 2289000000 in the same report.", "account": "total revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"3002000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_total_revenue_cumulative_line", "what_changed": "Total revenue for the first nine months of fiscal 2026 prints 8070000000; the first nine months of fiscal 2025 print 6685000000.", "account": "total revenue, nine months", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"8070000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_product_revenue_line", "what_changed": "Product revenue for the third quarter of fiscal 2026 prints 594000000; the third quarter of fiscal 2025 prints 453000000. Nine months: 1542000000 against 1228000000.", "account": "product revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"594000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_subscription_and_support_revenue_line", "what_changed": "Service (subscription and support) revenue for the third quarter of fiscal 2026 prints 2408000000; the third quarter of fiscal 2025 prints 1836000000. Nine months: 6528000000 against 5457000000.", "account": "subscription and support revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2408000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "earnings_quality_product_cost_of_revenue_line", "what_changed": "Product cost of revenue for the third quarter of fiscal 2026 prints 167000000; the third quarter of fiscal 2025 prints 101000000. Nine months: 371000000 against 277000000.", "account": "product cost of revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"167000000\"", "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "earnings_quality_subscription_and_support_cost_of_revenue_line", "what_changed": "Service (subscription and support) cost of revenue for the third quarter of fiscal 2026 prints 807000000; the third quarter of fiscal 2025 prints 518000000. Nine months: 1926000000 against 1495000000. Total cost of revenue prints 974000000 against 619000000.", "account": "subscription and support cost of revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"807000000\"", "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "earnings_quality_gross_profit_line", "what_changed": "Gross profit for the third quarter of fiscal 2026 prints 2028000000; the third quarter of fiscal 2025 prints 1670000000. Nine months: 5773000000 against 4913000000.", "account": "gross profit", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2028000000\"", "paragraph_id": "0001327567-26-000015:facts:GrossProfit:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_research_and_development_expense", "what_changed": "Research and development expense for the third quarter of fiscal 2026 prints 734000000; the third quarter of fiscal 2025 prints 494000000. Nine months: 1773000000 against 1480000000.", "account": "research and development expense", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"734000000\"", "paragraph_id": "0001327567-26-000015:facts:ResearchAndDevelopmentExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_selling_and_marketing_expense", "what_changed": "Sales and marketing expense for the third quarter of fiscal 2026 prints 1161000000; the third quarter of fiscal 2025 prints 793000000. Nine months: 2804000000 against 2271000000.", "account": "sales and marketing expense", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"1161000000\"", "paragraph_id": "0001327567-26-000015:facts:SellingAndMarketingExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_general_and_administrative_expense", "what_changed": "General and administrative expense for the third quarter of fiscal 2026 prints 316000000; the third quarter of fiscal 2025 prints 164000000. Nine months: 673000000 against 416000000.", "account": "general and administrative expense", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"316000000\"", "paragraph_id": "0001327567-26-000015:facts:GeneralAndAdministrativeExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_total_operating_expenses", "what_changed": "Total operating expenses for the third quarter of fiscal 2026 print 2211000000, larger than the quarter's gross profit of 2028000000; the third quarter of fiscal 2025 prints 1451000000.", "account": "total operating expenses", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2211000000\"", "paragraph_id": "0001327567-26-000015:facts:OperatingExpenses:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_operating_loss_line", "what_changed": "Operating income for the third quarter of fiscal 2026 prints -183000000, a loss; the third quarter of fiscal 2025 prints 219000000.", "account": "operating income (loss)", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"-183000000\"", "paragraph_id": "0001327567-26-000015:facts:OperatingIncomeLoss:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_operating_income_cumulative_line", "what_changed": "Operating income for the first nine months of fiscal 2026 prints 523000000; the first nine months of fiscal 2025 print 746000000.", "account": "operating income, nine months", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"523000000\"", "paragraph_id": "0001327567-26-000015:facts:OperatingIncomeLoss:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_pretax_loss_line", "what_changed": "Income before income taxes for the third quarter of fiscal 2026 prints -156000000; the third quarter of fiscal 2025 prints 311000000. Nine months: 805000000 against 1004000000.", "account": "income (loss) before income taxes", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"-156000000\"", "paragraph_id": "0001327567-26-000015:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_income_tax_expense_against_pretax_loss", "what_changed": "Income tax expense for the third quarter of fiscal 2026 prints 21000000 against a pre-tax loss of -156000000; the third quarter of fiscal 2025 prints 49000000 against pre-tax income of 311000000. Nine months: 216000000 against 124000000. A tax charge on a pre-tax loss is printed; the facts I read do not explain it.", "account": "provision for income taxes", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"21000000\"", "paragraph_id": "0001327567-26-000015:facts:IncomeTaxExpenseBenefit:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_net_loss_line", "what_changed": "Net income for the third quarter of fiscal 2026 prints -177000000, a loss; the third quarter of fiscal 2025 prints 262000000.", "account": "net income (loss)", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"-177000000\"", "paragraph_id": "0001327567-26-000015:facts:NetIncomeLoss:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_net_income_cumulative_line", "what_changed": "Net income for the first nine months of fiscal 2026 prints 589000000; the first nine months of fiscal 2025 print 880000000.", "account": "net income, nine months", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"589000000\"", "paragraph_id": "0001327567-26-000015:facts:NetIncomeLoss:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_basic_loss_per_share", "what_changed": "Basic earnings per share for the third quarter of fiscal 2026 prints -0.22; the third quarter of fiscal 2025 prints 0.39. Nine months: 0.81 against 1.33.", "account": "basic earnings (loss) per share", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"-0.22\"", "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareBasic:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_diluted_loss_per_share", "what_changed": "Diluted earnings per share for the third quarter of fiscal 2026 prints -0.22; the third quarter of fiscal 2025 prints 0.37.", "account": "diluted earnings (loss) per share", "expected_direction": "down", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"-0.22\"", "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareDiluted:2026-02-01..2026-04-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_commitments_and_contingencies_caption", "what_changed": "The commitments and contingencies caption on the balance sheet is tagged as nil at April 30, 2026 and at July 31, 2025: a caption with no amount. I read no contingency amounts.", "account": "commitments and contingencies", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"nil\": true", "paragraph_id": "0001327567-26-000015:facts:CommitmentsAndContingencies:2026-04-30" }
```

```json
{ "id": "revenue_recognition_americas_revenue_line", "what_changed": "Revenue from the Americas for the third quarter of fiscal 2026 prints 2018000000; the third quarter of fiscal 2025 prints 1530000000. Nine months: 5371000000 against 4474000000. The input does not mark whether this breakdown sat in a note.", "account": "revenue, Americas", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2018000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_europe_middle_east_africa_revenue_line", "what_changed": "Revenue from Europe, the Middle East and Africa for the third quarter of fiscal 2026 prints 633000000; the third quarter of fiscal 2025 prints 480000000. Nine months: 1714000000 against 1402000000. The input does not mark whether this breakdown sat in a note.", "account": "revenue, Europe, the Middle East and Africa", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"633000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_asia_pacific_revenue_line", "what_changed": "Revenue from Asia Pacific for the third quarter of fiscal 2026 prints 351000000; the third quarter of fiscal 2025 prints 279000000. Nine months: 985000000 against 809000000. The input does not mark whether this breakdown sat in a note.", "account": "revenue, Asia Pacific", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"351000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "revenue_recognition_support_revenue_line", "what_changed": "Support revenue for the third quarter of fiscal 2026 prints 776000000; the third quarter of fiscal 2025 prints 602000000. Nine months: 2128000000 against 1798000000. The input does not mark whether this breakdown sat in a note.", "account": "support revenue", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"776000000\"", "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=panw:SupportMember" }
```

```json
{ "id": "liquidity_and_capital_foreign_government_debt_level_two_fair_value", "what_changed": "The current report prints the fair value of foreign government debt securities held in long-term investments, measured with level two inputs, as 26000000 at July 31, 2025. I did not read the April 30, 2026 counterpart. The input does not mark whether this fact sat in a note.", "account": "investments at fair value, foreign government debt, level two", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"26000000\"", "paragraph_id": "0001327567-26-000015:facts:InvestmentsFairValueDisclosure:2025-07-31:us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel2Member,us-gaap:FinancialInstrumentAxis=us-gaap:ForeignGovernmentDebtSecuritiesMember,us-gaap:InvestmentTypeAxis=us-gaap:OtherLongTermInvestmentsMember" }
```

```json
{ "id": "earnings_quality_diluted_share_count_prior_report", "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints 711000000 weighted-average diluted shares for that quarter; the second quarter of fiscal 2025 prints 709000000. Six months: 713000000 against 709000000.", "account": "weighted-average diluted shares", "expected_direction": "up", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"711000000\"", "paragraph_id": "0001327567-26-000005:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_basic_earnings_per_share_prior_report", "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints basic earnings per share of 0.61 for that quarter. The comparison row fell outside the lines I read.", "account": "basic earnings per share", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"0.61\"", "paragraph_id": "0001327567-26-000005:facts:EarningsPerShareBasic:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_share_based_compensation_in_product_cost", "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints share-based compensation in product cost of revenue of 2000000 for the second quarter of fiscal 2025. The current-year row's value (1000000) printed just before it, but its id fell outside the lines I read, so no comparison is drawn. The input does not mark whether this fact sat in a note.", "account": "share-based compensation, product cost of revenue", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2000000\"", "paragraph_id": "0001327567-26-000005:facts:AllocatedShareBasedCompensationExpense:2024-11-01..2025-01-31:srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:IncomeStatementLocationAxis=us-gaap:CostOfSalesMember" }
```

```json
{ "id": "estimates_and_discretion_performance_unit_tranche_vesting_share", "what_changed": "The fiscal 2025 annual report prints 0.25 as the vesting share of the second tranche of performance stock units subject to service and stock-price conditions under the 2021 equity incentive plan, for fiscal 2023. The third and fourth tranches print 0.25 as well. Nothing to compare. The input does not mark whether this fact sat in a note.", "account": "performance stock units, tranche vesting share", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"0.25\"", "paragraph_id": "0001327567-25-000027:facts:SharebasedCompensationArrangementBySharebasedPaymentAwardAwardVestingRightsPercentage:2022-08-01..2023-07-31:panw:MarketConditionAxis=panw:MarketConditionStockPriceTargetsMember,us-gaap:AwardTypeAxis=panw:PerformanceStockUnitsPSUsSubjectToServiceAndMarketConditionsMember,us-gaap:PlanNameAxis=panw:A2021EquityIncentivePlanMember,us-gaap:VestingAxis=us-gaap:ShareBasedCompensationAwardTrancheTwoMember" }
```

```json
{ "id": "estimates_and_discretion_performance_units_vested_grant_date_fair_value", "what_changed": "The fiscal 2025 annual report prints 64.65 as the weighted-average grant-date fair value per share of performance stock units vested in fiscal 2025. Nothing to compare. The input does not mark whether this fact sat in a note.", "account": "performance stock units vested, weighted-average grant-date fair value", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"64.65\"", "paragraph_id": "0001327567-25-000027:facts:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodWeightedAverageGrantDateFairValue:2024-08-01..2025-07-31:us-gaap:AwardTypeAxis=panw:PerformanceStockUnitsPSUsMember" }
```

```json
{ "id": "estimates_and_discretion_restricted_units_forfeited", "what_changed": "The fiscal 2025 annual report prints 2200000 restricted stock units forfeited in fiscal 2025. Nothing to compare. The input does not mark whether this fact sat in a note.", "account": "restricted stock units forfeited", "expected_direction": "none", "horizon": "through the annual report for fiscal 2026", "quote": "\"value\": \"2200000\"", "paragraph_id": "0001327567-25-000027:facts:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsForfeitedInPeriod:2024-08-01..2025-07-31:us-gaap:AwardTypeAxis=us-gaap:RestrictedStockUnitsRSUMember" }
```

## Seen in the notes

No items. Each fact was supposed to say whether its element sat inside a note when it was extracted, but none of the facts I read carries that marker. I was told not to judge this myself, so I cannot sort any fact here without re-deriving its origin. The facts above with a breakdown member include:
- revenue by region and the support revenue line;
- the level-two fair-value fact;
- the convertible notes face amount;
- share-based compensation in product cost;
- the stock-unit facts.

Those are the likeliest to have come from note tables, but the input does not say so. Until the marker is present, this section cannot be filled.
