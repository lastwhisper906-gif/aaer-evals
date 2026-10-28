<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
Palo Alto Networks: the quarterly report for the third quarter of fiscal 2026 (the three months ended April 30, 2026), filed June 3, 2026. The fiscal year ends July 31.

What this reading covers, and what my directory does not hold:

- **Files read in full.** I read three files in full: the trend table, the earnings-release file and my prior-flags file. The prior-flags file says there is no earlier run, so it holds no flags, explanations or outcomes to carry forward.
- **The numeric-facts file was read only in part.** It is 93,456 lines of raw tagged facts from three filings: the annual report for fiscal 2025 (filed August 29, 2025), the quarterly report for the second quarter of fiscal 2026 (filed February 18, 2026), and this quarterly report. It does not fit in my context at once. I read its opening and closing and every fact of this report's balance sheet, income statement, comprehensive-income statement and cash-flow statement. I also read the run of this report's facts that closes the file, and samples from the other two filings. I did not read the remaining lines one by one. Anything that sits only in those lines is not reported here.
- **No articulation checks, restatement traces or fourth-quarter derivation.** My directory holds none of these. This report therefore has no articulation gap, no restated prior value and no derived fourth-quarter figure, and I did not work any of them out myself.
- **No change of tag.** Nothing in the trend table says a period rests on a different concept: every filled cell uses the same tags in every period. So no change of tag is reported.
- **Two periods the record does not reach.** The fourth quarter of fiscal 2025 (target end July 31, 2025) and the fourth quarter of fiscal 2024 (target end August 1, 2024) have no cells. The reason each period gives is "no quarter ending within 20 days of 2025-07-31 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration" (with August 1, 2024 for the earlier one). The rest of the reason says that the annual report states the year and the three quarterly reports state the first three quarters, so the fourth quarter has to come from the fourth-quarter derivation, whose output is not in my directory. Because of this gap, the first quarter of fiscal 2026 and the first quarter of fiscal 2025 have no change against a preceding quarter.
- **No earnings-release text.** The earnings-release file says no current report filed on or before June 3, 2026 is on record and gives no release body. Yet its own index lists a current report filed June 2, 2026 under the results-of-operations item. The file prints no paragraph ids, so nothing in it can be quoted or made an item. No release figure exists to set against the statements. The index lists no late-filing notification on or before June 3, 2026.
- **The research-and-development baseline prints no paragraph id.** For fiscal 2025 it prints earnings with research and development capitalized of 1770080000.0 and book value with it capitalized of 13013180000.0. Its capitalized development cost and capitalized-over-expense lines are insufficient: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period". With no paragraph id to quote, none of these lines is an item.
- **Nothing out of scope.** Nothing in my directory is a price, a return, short interest, another company's file, a prior probability or an outcome window.

Every value below is copied as printed. Where an item names a second value for comparison, that value is printed in my input as well, on the row or cell named in the text.

## Seen in the statements

**The trend table: the third quarter of fiscal 2026 (February 1 to April 30, 2026)**

```json
{ "id": "revenue_recognition_trend_receivables_over_revenue_quarterly",
  "what_changed": "Receivables over revenue for the third quarter of fiscal 2026 is 0.950033311125916. Its inputs are net accounts receivable of 2852000000 at April 30, 2026 and quarter revenue of 3002000000. The change is 0.13430470665405791 against the second quarter of fiscal 2026 and 0.09813291794111922 against the third quarter of fiscal 2025. The table places it as the highest of the six filled quarters. The six filled quarters skip the two fourth quarters the record does not reach.",
  "account": "accounts receivable, net, against quarter revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the second quarter of fiscal 2026 and against the third quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:receivables_over_revenue:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_trend_days_sales_outstanding_quarterly",
  "what_changed": "Days sales outstanding for the third quarter of fiscal 2026 is 84.55296469020652. It uses receivables of 2852000000, revenue of 3002000000 and an 89-day quarter. The change is 9.505933078795579 days against the second quarter of fiscal 2026 and 8.7338296967596 days against the third quarter of fiscal 2025. It is the highest of the six filled quarters.",
  "account": "days sales outstanding",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the second quarter of fiscal 2026 and against the third quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_outstanding:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_gross_margin_quarterly",
  "what_changed": "Gross margin for the third quarter of fiscal 2026 is 0.6755496335776149, from cost of revenue of 974000000 against revenue of 3002000000. The change is -0.060379433500257096 against the second quarter of fiscal 2026 and -0.05402660058577524 against the third quarter of fiscal 2025. It is the lowest of the six filled quarters; the first quarter of fiscal 2026 cell, at 0.7421180274858529, is the highest.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the second quarter of fiscal 2026 and against the third quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:gross_margin:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_quarterly",
  "what_changed": "The allowance for doubtful accounts over gross receivables is 0.002099370188943317 for the third quarter of fiscal 2026. Its inputs are an allowance of 6000000 and net receivables of 2852000000 at April 30, 2026; the second-quarter cell prints an allowance of 13000000 and receivables of 2116000000 at January 31, 2026. The change is -0.004006782934588858 against the second quarter of fiscal 2026 and -0.0033071380228285895 against the third quarter of fiscal 2025. It is the lowest of the six filled quarters, in the same quarter where receivables over revenue and days sales outstanding are the highest.",
  "account": "allowance for doubtful accounts against receivables",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the second quarter of fiscal 2026 and against the third quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_trend_contract_liabilities_over_revenue_quarterly",
  "what_changed": "Current contract liabilities over quarter revenue is 2.3694203864090606 for the third quarter of fiscal 2026. Its inputs are current contract liabilities of 7113000000 at April 30, 2026 and revenue of 3002000000; the formula uses the current portion only. The change is -0.03921492584999875 against the second quarter of fiscal 2026 and -0.1455643230710617 against the third quarter of fiscal 2025. It is the lowest of the six filled quarters.",
  "account": "current contract liabilities (deferred revenue) against quarter revenue",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the second quarter of fiscal 2026 and against the third quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:contract_liabilities_over_revenue:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_soft_asset_share_quarterly",
  "what_changed": "The soft-asset share (total assets less property and equipment less cash, over total assets) is 0.9379674058704016 for the third quarter of fiscal 2026. Its inputs are total assets of 46266000000, cash of 2364000000 and property and equipment of 506000000 at April 30, 2026; the second-quarter cell prints total assets of 24979000000 at January 31, 2026. The change is 0.12384354182460311 against the second quarter of fiscal 2026 and 0.06295149880402828 against the third quarter of fiscal 2025. It is the highest of the six filled quarters. The balance-sheet items below print goodwill of 21902000000 and intangible assets of 7283000000 at April 30, 2026.",
  "account": "soft assets against total assets",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the second quarter of fiscal 2026 and against the third quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:soft_asset_share:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_accruals_over_total_assets_quarterly",
  "what_changed": "insufficient. Accruals over total assets cannot be filled for the third quarter of fiscal 2026. The record has no operating cash flow for the three months ended April 30, 2026; this quarterly report states operating cash flow only for the nine months to April 30, 2026 (3196000000, an item below). A three-month figure does not exist in my input, and I have not derived one. The table fills this metric in only two quarters, the first quarter of fiscal 2026 and the first quarter of fiscal 2025, and two quarters do not support a trend claim.",
  "account": "accruals (net income less operating cash flow) against total assets",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-02-01..2026-04-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001327567-26-000015:trends:accruals_over_total_assets:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_days_sales_of_inventory_quarterly",
  "what_changed": "insufficient. Days of inventory cannot be filled for the third quarter of fiscal 2026. The record holds no inventory figure at any quarter end in the table; the only filled cells are the fiscal 2025 and fiscal 2024 year ends.",
  "account": "inventory against cost of revenue",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for inventory in 2026-04-30: us-gaap:InventoryNet is in the record, but not for this period\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_of_inventory:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_inventory_reserve_ratio_quarterly",
  "what_changed": "insufficient. The inventory reserve ratio is empty in every period of the table. The record tags no inventory valuation reserve in any period. The cell adds that the record cannot tell whether the company does not tag the concept or states it only by segment.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:inventory_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_warranty_reserve_ratio_quarterly",
  "what_changed": "insufficient. The warranty reserve ratio is empty in every period of the table. The record tags no product warranty accrual, under any of the three concepts it looks for, in any period.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:warranty_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_non_gaap_gap_quarterly",
  "what_changed": "insufficient. The gap between non-GAAP and reported net income cannot be filled for any period, because the record holds standard-taxonomy facts only and no non-GAAP measure. This bundle also holds no earnings-release text, so no non-GAAP figure exists anywhere in my input.",
  "account": "non-GAAP net income against reported net income",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001327567-26-000015:trends:non_gaap_gap:2026-02-01..2026-04-30" }
```

**The trend table: fiscal 2025 (August 1, 2024 to July 31, 2025)**

```json
{ "id": "earnings_quality_trend_accruals_over_total_assets_annual",
  "what_changed": "Accruals over total assets for fiscal 2025 is -0.10952239565659994. Its inputs are net income of 1133900000 and operating cash flow of 3716000000 for fiscal 2025, and total assets of 23576000000 at July 31, 2025, taken from this quarterly report's comparative column. The change against fiscal 2024 is -0.07550691861454581. It is the second highest of the five filled years.",
  "account": "accruals (net income less operating cash flow) against total assets",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:accruals_over_total_assets:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_annual",
  "what_changed": "The allowance over gross receivables for fiscal 2025 is 0.0033613445378151263, from an allowance of 10000000 and net receivables of 2965000000 at July 31, 2025. The change against fiscal 2024 is 0.0005053984580771116. It is the third highest of the five filled years.",
  "account": "allowance for doubtful accounts against receivables",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_trend_contract_liabilities_over_revenue_annual",
  "what_changed": "Current contract liabilities over annual revenue for fiscal 2025 is 0.6834029170959172, from current contract liabilities of 6302000000 at July 31, 2025 against revenue of 9221500000. The change against fiscal 2024 is -0.006861797946125847. It is the second highest of the five filled years.",
  "account": "current contract liabilities (deferred revenue) against annual revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:contract_liabilities_over_revenue:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_days_sales_of_inventory_annual",
  "what_changed": "Days of inventory for fiscal 2025 is 16.88325991189427, from inventory of 113400000 at July 31, 2025 against cost of revenue of 2451600000. The change against fiscal 2024 is -3.7166818130474546 days. It is the lowest of only two filled years, because fiscal 2023, 2022 and 2021 have no inventory row. Two years are insufficient for a trend claim.",
  "account": "inventory against cost of revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_of_inventory:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_trend_days_sales_outstanding_annual",
  "what_changed": "Days sales outstanding for fiscal 2025 is 117.35888955159137, from receivables of 2965000000 at July 31, 2025 against annual revenue of 9221500000. The change against fiscal 2024 is -2.0316554499657684 days. It is the second lowest of the five filled years.",
  "account": "days sales outstanding",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_outstanding:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_gross_margin_annual",
  "what_changed": "Gross margin for fiscal 2025 is 0.734143035297945, from cost of revenue of 2451600000 against revenue of 9221500000. The change against fiscal 2024 is -0.009338746078573212. It is the second highest of the five filled years.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:gross_margin:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_trend_receivables_over_revenue_annual",
  "what_changed": "Receivables over revenue for fiscal 2025 is 0.3215312042509353, from receivables of 2965000000 at July 31, 2025 against revenue of 9221500000. The change against fiscal 2024 is -0.0046724706167071695. It is the second lowest of the five filled years.",
  "account": "accounts receivable, net, against annual revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:receivables_over_revenue:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_soft_asset_share_annual",
  "what_changed": "The soft-asset share for fiscal 2025 is 0.8873430607397353, from total assets of 23576000000, cash of 2269000000 and property and equipment of 387000000 at July 31, 2025. The change against fiscal 2024 is -0.017798778797254. It is the third highest of the five filled years.",
  "account": "soft assets against total assets",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:soft_asset_share:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_inventory_reserve_ratio_annual",
  "what_changed": "insufficient. The inventory reserve ratio cannot be filled for fiscal 2025, or for any year in the table, because the record tags no inventory valuation reserve in any period.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:inventory_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_warranty_reserve_ratio_annual",
  "what_changed": "insufficient. The warranty reserve ratio cannot be filled for fiscal 2025, or for any year in the table, because the record tags no product warranty accrual in any period.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:warranty_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_non_gaap_gap_annual",
  "what_changed": "insufficient. The non-GAAP gap cannot be filled for fiscal 2025, or for any year in the table, because the record carries no non-GAAP measure.",
  "account": "non-GAAP net income against reported net income",
  "expected_direction": "none",
  "horizon": "none: the cell is not filled, so there is no change to carry",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001327567-26-000015:trends:non_gaap_gap:2024-08-01..2025-07-31" }
```

**Numeric facts: this quarterly report's balance sheet, April 30, 2026 against July 31, 2025**

```json
{ "id": "structure_and_disclosure_changes_fact_total_assets",
  "what_changed": "Total assets are 46266000000 at April 30, 2026 against 23576000000 at July 31, 2025 in this report's balance sheet. The second-quarter trend cell prints 24979000000 at January 31, 2026, so the step sits inside the third quarter of fiscal 2026.",
  "account": "total assets",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025 and January 31, 2026",
  "quote": "\"value\": \"46266000000\"",
  "paragraph_id": "0001327567-26-000015:facts:Assets:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_goodwill",
  "what_changed": "Goodwill is 21902000000 at April 30, 2026 against 4567000000 at July 31, 2025. The quarterly report for the second quarter of fiscal 2026 records, as a subsequent event dated February 11, 2026, a cash payment of 2300000000 and 112000000 shares for the CyberArk acquisition (items in the notes section). No fact I read ties the goodwill balance to that acquisition.",
  "account": "goodwill",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"21902000000\"",
  "paragraph_id": "0001327567-26-000015:facts:Goodwill:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_intangible_assets",
  "what_changed": "Intangible assets, net, are 7283000000 at April 30, 2026 against 763000000 at July 31, 2025.",
  "account": "intangible assets, net",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"7283000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IntangibleAssetsNetExcludingGoodwill:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_cash_and_cash_equivalents",
  "what_changed": "Cash and cash equivalents are 2364000000 at April 30, 2026 against 2269000000 at July 31, 2025. The second-quarter trend cell prints 4158000000 at January 31, 2026, so cash is above the fiscal year end but below the end of the second quarter.",
  "account": "cash and cash equivalents",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"2364000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CashAndCashEquivalentsAtCarryingValue:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_short_term_investments",
  "what_changed": "Short-term investments are 747000000 at April 30, 2026 against 635000000 at July 31, 2025.",
  "account": "short-term investments",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"747000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ShortTermInvestments:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_accounts_receivable_net",
  "what_changed": "Accounts receivable, net, are 2852000000 at April 30, 2026 against 2965000000 at July 31, 2025. The second-quarter trend cell prints 2116000000 at January 31, 2026, so receivables are below the fiscal year end and above the end of the second quarter.",
  "account": "accounts receivable, net",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"2852000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccountsReceivableNetCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_allowance_for_doubtful_accounts",
  "what_changed": "The allowance for doubtful accounts is 6000000 at April 30, 2026 against 10000000 at July 31, 2025; the second-quarter trend cell prints 13000000 at January 31, 2026.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025 and January 31, 2026",
  "quote": "\"value\": \"6000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_financing_receivables_current",
  "what_changed": "Current financing receivables (notes and loans receivable, net) are 591000000 at April 30, 2026 against 715000000 at July 31, 2025.",
  "account": "financing receivables, current",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"591000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NotesAndLoansReceivableNetCurrent:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_capitalized_contract_cost_current",
  "what_changed": "Current capitalized contract costs (deferred commissions) are 454000000 at April 30, 2026 against 419000000 at July 31, 2025.",
  "account": "capitalized contract costs, current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"454000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostNetCurrent:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_prepaid_and_other_current_assets",
  "what_changed": "Prepaid expenses and other current assets are 705000000 at April 30, 2026 against 520000000 at July 31, 2025.",
  "account": "prepaid expenses and other current assets",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"705000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PrepaidExpenseAndOtherAssetsCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_total_current_assets",
  "what_changed": "Total current assets are 7713000000 at April 30, 2026 against 7523000000 at July 31, 2025.",
  "account": "total current assets",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"7713000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AssetsCurrent:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_property_and_equipment",
  "what_changed": "Property and equipment, net, is 506000000 at April 30, 2026 against 387000000 at July 31, 2025.",
  "account": "property and equipment, net",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"506000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PropertyPlantAndEquipmentNet:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_operating_lease_assets",
  "what_changed": "Operating lease right-of-use assets are 678000000 at April 30, 2026 against 347000000 at July 31, 2025.",
  "account": "operating lease right-of-use assets",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"678000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseRightOfUseAsset:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_long_term_investments",
  "what_changed": "Long-term investments are 3881000000 at April 30, 2026 against 5555000000 at July 31, 2025.",
  "account": "long-term investments",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"3881000000\"",
  "paragraph_id": "0001327567-26-000015:facts:LongTermInvestments:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_financing_receivables_noncurrent",
  "what_changed": "Non-current financing receivables are 779000000 at April 30, 2026 against 1002000000 at July 31, 2025.",
  "account": "financing receivables, non-current",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"779000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NotesAndLoansReceivableNetNoncurrent:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_capitalized_contract_cost_noncurrent",
  "what_changed": "Non-current capitalized contract costs are 551000000 at April 30, 2026 against 586000000 at July 31, 2025.",
  "account": "capitalized contract costs, non-current",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"551000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostNetNoncurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_deferred_tax_assets",
  "what_changed": "Deferred tax assets are 2380000000 at April 30, 2026 against 2424000000 at July 31, 2025.",
  "account": "deferred tax assets",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"2380000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxAssetsNet:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_other_noncurrent_assets",
  "what_changed": "Other non-current assets are 593000000 at April 30, 2026 against 422000000 at July 31, 2025.",
  "account": "other assets, non-current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"593000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherAssetsNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_accounts_payable",
  "what_changed": "Accounts payable are 293000000 at April 30, 2026 against 232000000 at July 31, 2025.",
  "account": "accounts payable",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"293000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccountsPayableCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_accrued_compensation",
  "what_changed": "Accrued compensation (employee-related liabilities) is 680000000 at April 30, 2026 against 608000000 at July 31, 2025.",
  "account": "accrued compensation",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"680000000\"",
  "paragraph_id": "0001327567-26-000015:facts:EmployeeRelatedLiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_accrued_and_other_liabilities",
  "what_changed": "Accrued and other current liabilities are 760000000 at April 30, 2026 against 846000000 at July 31, 2025.",
  "account": "accrued and other liabilities, current",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"760000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccruedLiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_contract_liabilities_current",
  "what_changed": "Current contract liabilities (deferred revenue) are 7113000000 at April 30, 2026 against 6302000000 at July 31, 2025; the second-quarter trend cell prints 6248000000 at January 31, 2026.",
  "account": "deferred revenue, current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025 and January 31, 2026",
  "quote": "\"value\": \"7113000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ContractWithCustomerLiabilityCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_current",
  "what_changed": "Current convertible debt is 160000000 at April 30, 2026 against 0 at July 31, 2025.",
  "account": "convertible debt, current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"160000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ConvertibleDebtCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_total_current_liabilities",
  "what_changed": "Total current liabilities are 9006000000 at April 30, 2026 against 7988000000 at July 31, 2025.",
  "account": "total current liabilities",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"9006000000\"",
  "paragraph_id": "0001327567-26-000015:facts:LiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_noncurrent",
  "what_changed": "Non-current convertible debt is 1192000000 at April 30, 2026 against 0 at July 31, 2025. The cash-flow statement prints proceeds from convertible debt of only 10000000 for the first nine months of fiscal 2026, and no fact I read says where the balance came from. A note fact prints a face amount of 1250000000 for convertible senior notes due 2030, dated February 11, 2026 (notes section).",
  "account": "convertible debt, non-current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"1192000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ConvertibleDebtNoncurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_contract_liabilities_noncurrent",
  "what_changed": "Non-current contract liabilities (deferred revenue) are 6492000000 at April 30, 2026 against 6450000000 at July 31, 2025.",
  "account": "deferred revenue, non-current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"6492000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ContractWithCustomerLiabilityNoncurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_deferred_tax_liabilities",
  "what_changed": "Deferred tax liabilities are 259000000 at April 30, 2026 against 89000000 at July 31, 2025.",
  "account": "deferred tax liabilities",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"259000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxLiabilitiesNet:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_operating_lease_liabilities_noncurrent",
  "what_changed": "Non-current operating lease liabilities are 719000000 at April 30, 2026 against 338000000 at July 31, 2025.",
  "account": "operating lease liabilities, non-current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"719000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseLiabilityNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_other_noncurrent_liabilities",
  "what_changed": "Other non-current liabilities are 930000000 at April 30, 2026 against 887000000 at July 31, 2025.",
  "account": "other liabilities, non-current",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"930000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherLiabilitiesNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_total_liabilities",
  "what_changed": "Total liabilities are 18598000000 at April 30, 2026 against 15752000000 at July 31, 2025.",
  "account": "total liabilities",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"18598000000\"",
  "paragraph_id": "0001327567-26-000015:facts:Liabilities:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_paid_in_capital",
  "what_changed": "Common stock and additional paid-in capital are 24608000000 at April 30, 2026 against 5292000000 at July 31, 2025.",
  "account": "common stock and additional paid-in capital",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"24608000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CommonStocksIncludingAdditionalPaidInCapital:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_accumulated_other_comprehensive_income",
  "what_changed": "Accumulated other comprehensive income is -13000000 at April 30, 2026 against 48000000 at July 31, 2025.",
  "account": "accumulated other comprehensive income",
  "expected_direction": "down",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"-13000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccumulatedOtherComprehensiveIncomeLossNetOfTax:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_retained_earnings",
  "what_changed": "Retained earnings are 3073000000 at April 30, 2026 against 2484000000 at July 31, 2025. The statement of equity prints retained earnings of 3250000000 at January 31, 2026.",
  "account": "retained earnings",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"3073000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RetainedEarningsAccumulatedDeficit:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_stockholders_equity",
  "what_changed": "Total stockholders' equity is 27668000000 at April 30, 2026 against 7824000000 at July 31, 2025. The statement of equity prints 9393000000 at January 31, 2026, so the step sits inside the third quarter of fiscal 2026.",
  "account": "total stockholders' equity",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025 and January 31, 2026",
  "quote": "\"value\": \"27668000000\"",
  "paragraph_id": "0001327567-26-000015:facts:StockholdersEquity:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_shares_outstanding",
  "what_changed": "Common shares outstanding are 813000000 at April 30, 2026 against 668000000 at July 31, 2025. The statement of equity prints 703000000 at January 31, 2026.",
  "account": "common shares outstanding",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025 and January 31, 2026",
  "quote": "\"value\": \"813000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CommonStockSharesOutstanding:2026-04-30" }
```

**Numeric facts: this quarterly report's income statement and comprehensive income, the third quarter of fiscal 2026 against the third quarter of fiscal 2025, and the first nine months**

```json
{ "id": "revenue_recognition_fact_product_revenue",
  "what_changed": "Product revenue is 594000000 for the third quarter of fiscal 2026 against 453000000 for the third quarter of fiscal 2025.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"594000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_fact_subscription_and_support_revenue",
  "what_changed": "Subscription and support revenue (the service line of the income statement) is 2408000000 for the third quarter of fiscal 2026 against 1836000000 for the third quarter of fiscal 2025.",
  "account": "subscription and support revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"2408000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "revenue_recognition_fact_total_revenue",
  "what_changed": "Total revenue is 3002000000 for the third quarter of fiscal 2026 against 2289000000 for the third quarter of fiscal 2025; the second-quarter trend cell prints 2594000000 for the second quarter of fiscal 2026.",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"3002000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_product_cost_of_revenue",
  "what_changed": "Product cost of revenue is 167000000 for the third quarter of fiscal 2026 against 101000000 for the third quarter of fiscal 2025.",
  "account": "product cost of revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"167000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "earnings_quality_fact_subscription_and_support_cost_of_revenue",
  "what_changed": "Subscription and support cost of revenue is 807000000 for the third quarter of fiscal 2026 against 518000000 for the third quarter of fiscal 2025.",
  "account": "subscription and support cost of revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"807000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "earnings_quality_fact_total_cost_of_revenue",
  "what_changed": "Total cost of revenue is 974000000 for the third quarter of fiscal 2026 against 619000000 for the third quarter of fiscal 2025; the second-quarter trend cell prints 685000000 for the second quarter of fiscal 2026.",
  "account": "total cost of revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"974000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_gross_profit",
  "what_changed": "Gross profit is 2028000000 for the third quarter of fiscal 2026 against 1670000000 for the third quarter of fiscal 2025.",
  "account": "gross profit",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"2028000000\"",
  "paragraph_id": "0001327567-26-000015:facts:GrossProfit:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_research_and_development_expense",
  "what_changed": "Research and development expense is 734000000 for the third quarter of fiscal 2026 against 494000000 for the third quarter of fiscal 2025.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"734000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ResearchAndDevelopmentExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_sales_and_marketing_expense",
  "what_changed": "Sales and marketing expense is 1161000000 for the third quarter of fiscal 2026 against 793000000 for the third quarter of fiscal 2025.",
  "account": "sales and marketing expense",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"1161000000\"",
  "paragraph_id": "0001327567-26-000015:facts:SellingAndMarketingExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_general_and_administrative_expense",
  "what_changed": "General and administrative expense is 316000000 for the third quarter of fiscal 2026 against 164000000 for the third quarter of fiscal 2025.",
  "account": "general and administrative expense",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"316000000\"",
  "paragraph_id": "0001327567-26-000015:facts:GeneralAndAdministrativeExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_total_operating_expenses",
  "what_changed": "Total operating expenses are 2211000000 for the third quarter of fiscal 2026 against 1451000000 for the third quarter of fiscal 2025.",
  "account": "total operating expenses",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"2211000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingExpenses:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_operating_income_or_loss",
  "what_changed": "Operating income is -183000000 for the third quarter of fiscal 2026, an operating loss, against 219000000 for the third quarter of fiscal 2025.",
  "account": "operating income (loss)",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-183000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingIncomeLoss:2026-02-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_interest_expense",
  "what_changed": "Interest expense is 0 for the third quarter of fiscal 2026 against 1000000 for the third quarter of fiscal 2025, even though convertible debt now sits on the balance sheet.",
  "account": "interest expense",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001327567-26-000015:facts:InterestExpenseNonoperating:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_pretax_income_or_loss",
  "what_changed": "Income before income taxes is -156000000 for the third quarter of fiscal 2026 against 311000000 for the third quarter of fiscal 2025.",
  "account": "income (loss) before income taxes",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-156000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_income_tax_expense",
  "what_changed": "Income tax expense is 21000000 for the third quarter of fiscal 2026, recorded on a pre-tax loss of -156000000, against 49000000 for the third quarter of fiscal 2025. The input prints no effective rate, and I have not worked one out.",
  "account": "provision for income taxes",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"21000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncomeTaxExpenseBenefit:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_net_income_or_loss",
  "what_changed": "Net income is -177000000 for the third quarter of fiscal 2026, a net loss, against 262000000 for the third quarter of fiscal 2025.",
  "account": "net income (loss)",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-177000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetIncomeLoss:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_basic_earnings_per_share",
  "what_changed": "Basic earnings per share is -0.22 for the third quarter of fiscal 2026 against 0.39 for the third quarter of fiscal 2025.",
  "account": "basic earnings (loss) per share",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-0.22\"",
  "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareBasic:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_diluted_earnings_per_share",
  "what_changed": "Diluted earnings per share is -0.22 for the third quarter of fiscal 2026 against 0.37 for the third quarter of fiscal 2025. The quarterly report for the second quarter of fiscal 2026 prints 0.61 for that quarter (item below).",
  "account": "diluted earnings (loss) per share",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-0.22\"",
  "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareDiluted:2026-02-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_weighted_average_basic_shares",
  "what_changed": "Weighted-average basic shares are 801000000 for the third quarter of fiscal 2026 against 665000000 for the third quarter of fiscal 2025.",
  "account": "weighted-average basic shares",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"801000000\"",
  "paragraph_id": "0001327567-26-000015:facts:WeightedAverageNumberOfSharesOutstandingBasic:2026-02-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_weighted_average_diluted_shares",
  "what_changed": "Weighted-average diluted shares are 801000000 for the third quarter of fiscal 2026, the same printed figure as basic shares in this loss quarter, against 707000000 for the third quarter of fiscal 2025.",
  "account": "weighted-average diluted shares",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"801000000\"",
  "paragraph_id": "0001327567-26-000015:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_other_comprehensive_income",
  "what_changed": "Other comprehensive income, net of tax, is -59000000 for the third quarter of fiscal 2026 against 62000000 for the third quarter of fiscal 2025.",
  "account": "other comprehensive income (loss)",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-59000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherComprehensiveIncomeLossNetOfTaxPortionAttributableToParent:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_comprehensive_income",
  "what_changed": "Comprehensive income is -236000000 for the third quarter of fiscal 2026 against 324000000 for the third quarter of fiscal 2025.",
  "account": "comprehensive income (loss)",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-236000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ComprehensiveIncomeNetOfTax:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_total_revenue_cumulative",
  "what_changed": "Total revenue for the first nine months of fiscal 2026 is 8070000000 against 6685000000 for the first nine months of fiscal 2025.",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"8070000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_operating_income_cumulative",
  "what_changed": "Operating income for the first nine months of fiscal 2026 is 523000000 against 746000000 for the first nine months of fiscal 2025.",
  "account": "operating income (loss)",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"523000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingIncomeLoss:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_net_income_cumulative",
  "what_changed": "Net income for the first nine months of fiscal 2026 is 589000000 against 880000000 for the first nine months of fiscal 2025.",
  "account": "net income (loss)",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"589000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetIncomeLoss:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_diluted_earnings_per_share_cumulative",
  "what_changed": "Diluted earnings per share for the first nine months of fiscal 2026 is 0.79 against 1.24 for the first nine months of fiscal 2025.",
  "account": "diluted earnings (loss) per share",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"0.79\"",
  "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareDiluted:2025-08-01..2026-04-30" }
```

**Numeric facts: this quarterly report's cash-flow statement, the first nine months of fiscal 2026 against the first nine months of fiscal 2025**

```json
{ "id": "liquidity_and_capital_fact_operating_cash_flow",
  "what_changed": "Net cash from operating activities is 3196000000 for the first nine months of fiscal 2026 against 2695000000 for the first nine months of fiscal 2025. This report states operating cash flow for the nine months only; a figure for the third quarter alone does not exist in my input.",
  "account": "net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"3196000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetCashProvidedByUsedInOperatingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_share_based_compensation",
  "what_changed": "Share-based compensation added back in operating cash flow is 1314000000 for the first nine months of fiscal 2026 against 941000000 for the first nine months of fiscal 2025.",
  "account": "share-based compensation",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"1314000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ShareBasedCompensation:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_depreciation_and_amortization",
  "what_changed": "Depreciation and amortization is 514000000 for the first nine months of fiscal 2026 against 259000000 for the first nine months of fiscal 2025.",
  "account": "depreciation and amortization",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"514000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DepreciationDepletionAndAmortization:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_deferred_income_taxes",
  "what_changed": "Deferred income taxes in operating cash flow are 38000000 for the first nine months of fiscal 2026 against -442000000 for the first nine months of fiscal 2025.",
  "account": "deferred income taxes",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"38000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxesAndTaxCredits:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_contract_cost_amortization",
  "what_changed": "Amortization of capitalized contract costs is 410000000 for the first nine months of fiscal 2026 against 344000000 for the first nine months of fiscal 2025.",
  "account": "amortization of deferred contract costs",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"410000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostAmortization:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_contingent_consideration_remeasurement",
  "what_changed": "The change in the contingent consideration liability, an operating cash-flow adjustment, is -120000000 for the first nine months of fiscal 2026 against 20000000 for the first nine months of fiscal 2025.",
  "account": "remeasurement of contingent consideration",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-120000000\"",
  "paragraph_id": "0001327567-26-000015:facts:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_receivables_change_in_cash_flow",
  "what_changed": "The change in accounts receivable in operating cash flow is -441000000 for the first nine months of fiscal 2026 against -669000000 for the first nine months of fiscal 2025, a smaller use of cash.",
  "account": "change in accounts receivable",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-441000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInAccountsReceivable:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_financing_receivables_change_in_cash_flow",
  "what_changed": "The change in financing receivables in operating cash flow is -347000000 for the first nine months of fiscal 2026 against -102000000 for the first nine months of fiscal 2025, a larger use of cash.",
  "account": "change in financing receivables",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-347000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInFinanceReceivables:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_prepaid_and_other_assets_change_in_cash_flow",
  "what_changed": "The change in prepaid expenses and other assets in operating cash flow is 47000000 for the first nine months of fiscal 2026 against -68000000 for the first nine months of fiscal 2025.",
  "account": "change in prepaid expenses and other assets",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"47000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_accounts_payable_change_in_cash_flow",
  "what_changed": "The change in accounts payable in operating cash flow is 50000000 for the first nine months of fiscal 2026 against 119000000 for the first nine months of fiscal 2025.",
  "account": "change in accounts payable",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"50000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInAccountsPayable:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_accrued_compensation_change_in_cash_flow",
  "what_changed": "The change in accrued compensation in operating cash flow is -42000000 for the first nine months of fiscal 2026 against -49000000 for the first nine months of fiscal 2025.",
  "account": "change in accrued compensation",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-42000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInEmployeeRelatedLiabilities:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_accrued_liabilities_change_in_cash_flow",
  "what_changed": "The change in accrued and other liabilities in operating cash flow is 11000000 for the first nine months of fiscal 2026 against 34000000 for the first nine months of fiscal 2025.",
  "account": "change in accrued and other liabilities",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"11000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInAccruedLiabilitiesAndOtherOperatingLiabilities:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_contract_liabilities_change_in_cash_flow",
  "what_changed": "The change in deferred revenue in operating cash flow is 53000000 for the first nine months of fiscal 2026 against 64000000 for the first nine months of fiscal 2025.",
  "account": "change in deferred revenue",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"53000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_purchases_of_investments",
  "what_changed": "Purchases of investments are 2421000000 for the first nine months of fiscal 2026 against 2821000000 for the first nine months of fiscal 2025.",
  "account": "purchases of investments",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"2421000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsToAcquireInvestments:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_sales_of_investments",
  "what_changed": "Proceeds from sales of investments are 3399000000 for the first nine months of fiscal 2026 against 830000000 for the first nine months of fiscal 2025.",
  "account": "proceeds from sales of investments",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"3399000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromSaleOfAvailableForSaleSecuritiesDebt:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_maturities_of_investments",
  "what_changed": "Proceeds from maturities of investments are 1824000000 for the first nine months of fiscal 2026 against 1208000000 for the first nine months of fiscal 2025.",
  "account": "proceeds from maturities of investments",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"1824000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities:2025-08-01..2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_acquisition_payments",
  "what_changed": "Payments for business acquisitions, net of cash acquired, are 4563000000 for the first nine months of fiscal 2026 against 499000000 for the first nine months of fiscal 2025.",
  "account": "business acquisitions, net of cash acquired",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"4563000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsToAcquireBusinessesNetOfCashAcquired:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_capital_expenditure",
  "what_changed": "Purchases of property, equipment and other assets are 337000000 for the first nine months of fiscal 2026 against 160000000 for the first nine months of fiscal 2025.",
  "account": "capital expenditure",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"337000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsToAcquireProductiveAssets:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_investing_cash_flow",
  "what_changed": "Net cash used in investing activities is -2098000000 for the first nine months of fiscal 2026 against -1442000000 for the first nine months of fiscal 2025.",
  "account": "net cash used in investing activities",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-2098000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetCashProvidedByUsedInInvestingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_repayments",
  "what_changed": "Repayments of convertible debt are 0 for the first nine months of fiscal 2026 against 583000000 for the first nine months of fiscal 2025.",
  "account": "repayments of convertible debt",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001327567-26-000015:facts:RepaymentsOfConvertibleDebt:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_proceeds",
  "what_changed": "Proceeds from convertible debt are 10000000 for the first nine months of fiscal 2026 against 0 for the first nine months of fiscal 2025. Convertible debt on the balance sheet at April 30, 2026 is 160000000 current and 1192000000 non-current, against 0 at July 31, 2025; the cash-flow facts I read do not account for the difference, and I have not worked it out.",
  "account": "proceeds from convertible debt",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"10000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromConvertibleDebt:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_share_repurchases",
  "what_changed": "Repurchases of common stock are 1000000000 for the first nine months of fiscal 2026 against 0 for the first nine months of fiscal 2025.",
  "account": "repurchases of common stock",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"1000000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsForRepurchaseOfCommonStock:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_employee_share_plan_proceeds",
  "what_changed": "Proceeds from shares issued under employee equity plans are 264000000 for the first nine months of fiscal 2026 against 361000000 for the first nine months of fiscal 2025.",
  "account": "proceeds from employee equity plans",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"264000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromIssuanceOfSharesUnderIncentiveAndShareBasedCompensationPlansIncludingStockOptions:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_tax_withholding_payments",
  "what_changed": "Taxes paid on the net share settlement of equity awards are 125000000 for the first nine months of fiscal 2026 against 183000000 for the first nine months of fiscal 2025.",
  "account": "tax withholding on share-based awards",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"125000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsRelatedToTaxWithholdingForShareBasedCompensation:2025-08-01..2026-04-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_fact_contingent_consideration_payments",
  "what_changed": "Payments of contingent consideration in financing activities are 154000000 for the first nine months of fiscal 2026 against 0 for the first nine months of fiscal 2025.",
  "account": "payments of contingent consideration",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"154000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentForContingentConsiderationLiabilityFinancingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_financing_cash_flow",
  "what_changed": "Net cash used in financing activities is -1005000000 for the first nine months of fiscal 2026 against -405000000 for the first nine months of fiscal 2025.",
  "account": "net cash used in financing activities",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-1005000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetCashProvidedByUsedInFinancingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_exchange_rate_effect_on_cash",
  "what_changed": "The effect of exchange rates on cash is 2000000 for the first nine months of fiscal 2026 against 0 for the first nine months of fiscal 2025.",
  "account": "effect of exchange rates on cash",
  "expected_direction": "up",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"2000000\"",
  "paragraph_id": "0001327567-26-000015:facts:EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_cash_including_restricted_cash",
  "what_changed": "Cash, cash equivalents and restricted cash in the cash-flow statement are 2374000000 at April 30, 2026 against 2279000000 at July 31, 2025.",
  "account": "cash, cash equivalents and restricted cash",
  "expected_direction": "up",
  "horizon": "April 30, 2026 against July 31, 2025",
  "quote": "\"value\": \"2374000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents:2026-04-30" }
```

**Numeric facts: this report's cover page, and the quarterly report for the second quarter of fiscal 2026**

```json
{ "id": "liquidity_and_capital_fact_cover_page_shares_outstanding",
  "what_changed": "The cover page of this quarterly report gives 815000000 common shares outstanding at May 26, 2026, against 813000000 on the balance sheet at April 30, 2026. This is a cover-page fact, not a statement fact.",
  "account": "common shares outstanding",
  "expected_direction": "up",
  "horizon": "May 26, 2026 against April 30, 2026",
  "quote": "\"value\": \"815000000\"",
  "paragraph_id": "0001327567-26-000015:facts:EntityCommonStockSharesOutstanding:2026-05-26" }
```

```json
{ "id": "earnings_quality_fact_diluted_earnings_per_share_earlier_report",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints diluted earnings per share of 0.61 for that quarter against 0.38 for the second quarter of fiscal 2025. It is the quarter before the -0.22 in this report.",
  "account": "diluted earnings (loss) per share",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"0.61\"",
  "paragraph_id": "0001327567-26-000005:facts:EarningsPerShareDiluted:2025-11-01..2026-01-31" }
```

## Seen in the notes

No fact in my input carries the marker that says whether its element sat inside a note: each fact prints the same fields, and none of them is that marker. The items below are placed here on my own reading, not by the marker, and need checking by whoever splits the notes into their own reader. Each is a dimensional or disclosure fact: a subsequent event, a debt instrument, a revenue split by region or by subscription and support, other-income detail, or an equity-award term. Each sits outside the run of primary-statement facts in its filing. The product revenue row below prints the same paragraph id and value as the statement item above, because the record carries it twice.

```json
{ "id": "revenue_recognition_note_subscription_revenue",
  "what_changed": "Subscription revenue is 1632000000 for the third quarter of fiscal 2026 against 1234000000 for the third quarter of fiscal 2025.",
  "account": "subscription revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"1632000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=panw:SubscriptionMember" }
```

```json
{ "id": "revenue_recognition_note_support_revenue",
  "what_changed": "Support revenue is 776000000 for the third quarter of fiscal 2026 against 602000000 for the third quarter of fiscal 2025.",
  "account": "support revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"776000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=panw:SupportMember" }
```

```json
{ "id": "revenue_recognition_note_product_revenue_disaggregation",
  "what_changed": "Product revenue appears again among the closing facts with the revenue split, at 594000000 for the third quarter of fiscal 2026 against 453000000 for the third quarter of fiscal 2025. It is the same row as the statement item.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"594000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_note_americas_revenue",
  "what_changed": "Revenue from the Americas is 2018000000 for the third quarter of fiscal 2026 against 1530000000 for the third quarter of fiscal 2025.",
  "account": "revenue, Americas",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"2018000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_note_europe_middle_east_and_africa_revenue",
  "what_changed": "Revenue from Europe, the Middle East and Africa is 633000000 for the third quarter of fiscal 2026 against 480000000 for the third quarter of fiscal 2025.",
  "account": "revenue, Europe, the Middle East and Africa",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"633000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_note_asia_pacific_revenue",
  "what_changed": "Revenue from Asia Pacific is 351000000 for the third quarter of fiscal 2026 against 279000000 for the third quarter of fiscal 2025.",
  "account": "revenue, Asia Pacific",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"351000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "liquidity_and_capital_note_convertible_senior_notes_face_amount",
  "what_changed": "This quarterly report tags a face amount of 1250000000 for convertible senior notes due 2030, at February 11, 2026, the same date as the CyberArk payment in the second-quarter report. The row has no comparative, but the balance sheet showed no convertible debt at July 31, 2025. No fact I read says whether these notes were issued or assumed.",
  "account": "convertible senior notes due 2030, face amount",
  "expected_direction": "none",
  "horizon": "a single date, February 11, 2026, with no comparative on the row",
  "quote": "\"value\": \"1250000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DebtInstrumentFaceAmount:2026-02-11:us-gaap:DebtInstrumentAxis=panw:ConvertibleSeniorNotesDue2030Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleDebtMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_note_cyberark_cash_consideration",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 records, as a subsequent event, a gross cash payment of 2300000000 for the acquisition of CyberArk on February 11, 2026. That date falls inside the third quarter of fiscal 2026, the quarter in which goodwill, intangible assets, paid-in capital and shares outstanding step up.",
  "account": "business acquisition, cash consideration",
  "expected_direction": "none",
  "horizon": "a single date, February 11, 2026, with no comparative on the row",
  "quote": "\"value\": \"2300000000\"",
  "paragraph_id": "0001327567-26-000005:facts:PaymentsToAcquireBusinessesGross:2026-02-11..2026-02-11:us-gaap:BusinessAcquisitionAxis=panw:CyberArkSoftwareLtd.Member,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_note_cyberark_shares_issued",
  "what_changed": "The same subsequent-event disclosure records 112000000 shares issued or issuable for the CyberArk acquisition on February 11, 2026. Common shares outstanding are 703000000 at January 31, 2026 and 813000000 at April 30, 2026, both in this report's statement of equity and balance sheet.",
  "account": "business acquisition, shares issued",
  "expected_direction": "none",
  "horizon": "a single date, February 11, 2026, with no comparative on the row",
  "quote": "\"value\": \"112000000\"",
  "paragraph_id": "0001327567-26-000005:facts:BusinessAcquisitionEquityInterestsIssuedOrIssuableNumberOfSharesIssued:2026-02-11..2026-02-11:us-gaap:BusinessAcquisitionAxis=panw:CyberArkSoftwareLtd.Member,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_note_koi_security_consideration",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 records, as a subsequent event, consideration of 300000000 for the acquisition of Koi Security on February 16, 2026, also inside the third quarter of fiscal 2026.",
  "account": "business acquisition, consideration transferred",
  "expected_direction": "none",
  "horizon": "a single date, February 16, 2026, with no comparative on the row",
  "quote": "\"value\": \"300000000\"",
  "paragraph_id": "0001327567-26-000005:facts:BusinessCombinationConsiderationTransferred1:2026-02-16..2026-02-16:us-gaap:BusinessAcquisitionAxis=panw:KoiSecurityLtdMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "earnings_quality_note_other_nonoperating_income",
  "what_changed": "Other non-operating income is 8000000 for the third quarter of fiscal 2026 and 8000000 for the third quarter of fiscal 2025.",
  "account": "other non-operating income",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"8000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherNonoperatingIncomeExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_note_derivative_result",
  "what_changed": "The net result on derivatives is -1000000 for the third quarter of fiscal 2026 against 0 for the third quarter of fiscal 2025.",
  "account": "gain (loss) on derivatives",
  "expected_direction": "down",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "\"value\": \"-1000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DerivativeGainLossOnDerivativeNet:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_note_foreign_currency_result_cumulative",
  "what_changed": "The foreign currency transaction result before tax is -41000000 for the first nine months of fiscal 2026 against -14000000 for the first nine months of fiscal 2025.",
  "account": "foreign currency transaction gain (loss)",
  "expected_direction": "down",
  "horizon": "the first nine months of fiscal 2026 against the first nine months of fiscal 2025",
  "quote": "\"value\": \"-41000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ForeignCurrencyTransactionGainLossBeforeTax:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_note_share_awards_granted",
  "what_changed": "This quarterly report tags 3000000 share awards other than options granted in the first nine months of fiscal 2026. The fact carries no plan or award-type dimension, and the row has no comparative.",
  "account": "share awards granted, other than options",
  "expected_direction": "none",
  "horizon": "the first nine months of fiscal 2026, with no comparative on the row",
  "quote": "\"value\": \"3000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriod:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_note_shares_available_for_grant",
  "what_changed": "This quarterly report tags 3000000 shares available for grant at April 30, 2026. The fact carries no plan dimension, and the row has no comparative.",
  "account": "shares available for grant",
  "expected_direction": "none",
  "horizon": "a single date, April 30, 2026, with no comparative on the row",
  "quote": "\"value\": \"3000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ShareBasedCompensationArrangementByShareBasedPaymentAwardNumberOfSharesAvailableForGrant:2026-04-30" }
```

```json
{ "id": "earnings_quality_note_interest_income_earlier_report",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints interest income of 109000000 for that quarter against 87000000 for the second quarter of fiscal 2025.",
  "account": "interest income",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"109000000\"",
  "paragraph_id": "0001327567-26-000005:facts:InterestIncomeOther:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_note_other_nonoperating_income_earlier_report",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints other non-operating income of 59000000 for that quarter against -4000000 for the second quarter of fiscal 2025. This report prints 8000000 for the third quarter of fiscal 2026.",
  "account": "other non-operating income",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"59000000\"",
  "paragraph_id": "0001327567-26-000005:facts:OtherNonoperatingIncomeExpense:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_note_foreign_currency_result_earlier_report",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 prints a foreign currency transaction result of -16000000 for that quarter against 2000000 for the second quarter of fiscal 2025.",
  "account": "foreign currency transaction gain (loss)",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"-16000000\"",
  "paragraph_id": "0001327567-26-000005:facts:ForeignCurrencyTransactionGainLossBeforeTax:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_note_antidilutive_awards_excluded_earlier_report",
  "what_changed": "The quarterly report for the second quarter of fiscal 2026 excludes 6000000 restricted and performance stock units from diluted earnings per share as antidilutive for that quarter, and 6000000 for the second quarter of fiscal 2025.",
  "account": "antidilutive awards excluded from diluted shares",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"6000000\"",
  "paragraph_id": "0001327567-26-000005:facts:AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount:2025-11-01..2026-01-31:us-gaap:AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareByAntidilutiveSecuritiesAxis=panw:RestrictedStockUnitsRSUsandPerformanceStockUnitsPSUsMember" }
```

```json
{ "id": "estimates_and_discretion_note_performance_unit_tranche_vesting",
  "what_changed": "The annual report for fiscal 2025 tags a vesting percentage of 0.25 for tranche one of the performance stock units with service and stock-price conditions under the 2021 equity incentive plan, in a fact for fiscal 2023. Tranches two, three and four print 0.25 as well. There is no change to carry.",
  "account": "performance stock unit vesting terms",
  "expected_direction": "none",
  "horizon": "fiscal 2023, with no comparative on the row",
  "quote": "\"value\": \"0.25\"",
  "paragraph_id": "0001327567-25-000027:facts:SharebasedCompensationArrangementBySharebasedPaymentAwardAwardVestingRightsPercentage:2022-08-01..2023-07-31:panw:MarketConditionAxis=panw:MarketConditionStockPriceTargetsMember,us-gaap:AwardTypeAxis=panw:PerformanceStockUnitsPSUsSubjectToServiceAndMarketConditionsMember,us-gaap:PlanNameAxis=panw:A2021EquityIncentivePlanMember,us-gaap:VestingAxis=us-gaap:ShareBasedCompensationAwardTrancheOneMember" }
```
