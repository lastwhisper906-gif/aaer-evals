<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# PANW — numbers reader report

Filing `0001327567-26-000015`: 10-Q for the quarter ended 2026-04-30, filed 2026-06-03, cutoff 2026-06-03.

## What my input holds, and what it does not

- **Directory check.** The directory has four files: `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md` and `input_trends.json`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window, so on that count this is not a broken run.
- **Prior flags.** There are none. `input_prior_predictions.md` says there is no earlier run for this company.
- **8-K.** There is no earnings release and no item body in my input.
  - The file's header says "no 8-K filed at or before 2026-06-03 is on record". Its own item-code list, however, shows `2026-06-02 0001327567-26-000012 — 2.02, 9.01`. The two do not agree, and I report that as found.
  - The file has no `[id]` lines, so nothing in it can be quoted. There are no 8-K figures, so no `across_documents` or `results_against_expectations` item can be written.
- **Articulation checks, restatement traces, fourth-quarter derivation.**
  - None of these is in my directory. `input_numbers.json` has only four top-level keys: `ticker`, `cutoff`, `documents` and `facts`.
  - So there is no articulation gap, no restated prior value and no change of tag that I can quote, and none is written as an item. This means the input is missing, not that no gaps exist.
  - Nothing in my input says any period rests on a different concept. Every filled trend cell prints the same tag for each of its inputs across periods.
- **Periods the record does not reach.** Two quarters have no cells at all: `quarters-back-3` (target 2025-07-31) and `quarters-back-7` (target 2024-08-01). The reason the period gives is: "no quarter ending within 20 days of 2025-07-31 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The second period gives the same reason with 2024-08-01. The derivation it names is not in my directory. Of the 8 quarters requested, 6 are filled; all 5 requested years are filled.
- **Numeric facts: coverage.** `input_numbers.json` has 93,456 lines, roughly 1.6M tokens, which is more than I can hold at once. I did **not** read it end to end.
  - I read lines 1–300, 10000–10044, 30000–30039, 50000–50039, 60000–60029, 61500–65518, 68400–70039, 80000–80039, 87000–87044 and 92700–93456.
  - Lines 61854–65518 and 68400–70039 cover the current 10-Q's balance sheet, income statement and cash flow statement.
  - Only facts I read are written as items. Facts in the unread ranges, which include most of the 10-K's and prior 10-Q's facts and most of the current 10-Q's note-level detail, are not reported here.
- **In-note marker.** No fact I read carries a field saying whether its element sat inside a note. Each fact has only these fields: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession` and `filing_date`. See the second heading for how this is handled.
- **Formula baseline without a paragraph_id.** `years-back-0` holds a `research_and_development_capitalized` block. None of its derived rows prints a `paragraph_id`, so none can be an item. As printed:
  - `book_value_with_rnd_capitalized` 13013180000.0
  - `earnings_with_rnd_capitalized` 1770080000.0
  - `research_and_development_amortization` 1347920000.0
  - `research_and_development_asset` 5189180000.0
  - `capitalized_development_cost` and `capitalized_over_expense` are missing, with the reason "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
- **How the fields are used.**
  - `expected_direction` records the direction of the printed change. For a trend cell it is the sign of the printed change. For a fact it is the direction from the printed comparative to the printed current value. It is `none` where nothing is filled or there is no comparative.
  - `horizon` names the periods compared.
  - No difference, ratio or position below was computed by me. Every number is copied as printed.

## Seen in the statements

### Trend table — quarters-back-0 (2026-02-01..2026-04-30, 89 days)

```json
{ "id": "revenue_recognition_trend_receivables_over_revenue_latest_quarter",
  "what_changed": "receivables_over_revenue is 0.950033311125916 (receivables 2852000000.0 over revenue 3002000000.0). The change against quarters-back-1 is 0.13430470665405791; against quarters-back-4 it is 0.09813291794111922. The cell prints its position as highest of the 6 filled quarters.",
  "account": "accounts receivable, net, current (AccountsReceivableNetCurrent) over revenue (RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-04-30 against quarters-back-1 (ended 2026-01-31) and quarters-back-4 (ended 2025-04-30)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:receivables_over_revenue:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_trend_days_sales_outstanding_latest_quarter",
  "what_changed": "days_sales_outstanding is 84.55296469020652 (receivables 2852000000.0, revenue 3002000000.0, 89-day quarter). The change against quarters-back-1 is 9.505933078795579; against quarters-back-4 it is 8.7338296967596. The cell prints its position as highest of the 6 filled quarters.",
  "account": "accounts receivable, net, current (AccountsReceivableNetCurrent) against revenue (RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-04-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_outstanding:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_trend_contract_liabilities_over_revenue_latest_quarter",
  "what_changed": "contract_liabilities_over_revenue is 2.3694203864090606. The formula uses only the current portion of contract liabilities (ContractWithCustomerLiabilityCurrent 7113000000.0) over quarterly revenue 3002000000.0. The change against quarters-back-1 is -0.03921492584999875; against quarters-back-4 it is -0.1455643230710617. The cell prints its position as lowest of the 6 filled quarters.",
  "account": "contract liabilities, current (ContractWithCustomerLiabilityCurrent) over revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-04-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:contract_liabilities_over_revenue:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_gross_margin_latest_quarter",
  "what_changed": "gross_margin is 0.6755496335776149 (cost of revenue 974000000.0, revenue 3002000000.0). The change against quarters-back-1 is -0.060379433500257096; against quarters-back-4 it is -0.05402660058577524. The cell prints its position as lowest of the 6 filled quarters.",
  "account": "revenue (RevenueFromContractWithCustomerExcludingAssessedTax) less cost of revenue (CostOfGoodsAndServicesSold), over revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-04-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:gross_margin:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_latest_quarter",
  "what_changed": "bad_debt_reserve_ratio is 0.002099370188943317 (allowance 6000000.0, receivables 2852000000.0). The change against quarters-back-1 is -0.004006782934588858; against quarters-back-4 it is -0.0033071380228285895. The cell prints its position as lowest of the 6 filled quarters.",
  "account": "allowance for doubtful accounts (AllowanceForDoubtfulAccountsReceivableCurrent) over receivables plus allowance",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-04-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_soft_asset_share_latest_quarter",
  "what_changed": "soft_asset_share is 0.9379674058704016 (assets 46266000000.0, property and equipment 506000000.0, cash 2364000000.0). The change against quarters-back-1 is 0.12384354182460311; against quarters-back-4 it is 0.06295149880402828. The cell prints its position as highest of the 6 filled quarters.",
  "account": "total assets less property and equipment less cash, over total assets (Assets, PropertyPlantAndEquipmentNet, CashAndCashEquivalentsAtCarryingValue)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-04-30 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001327567-26-000015:trends:soft_asset_share:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_accruals_over_total_assets_latest_quarter_insufficient",
  "what_changed": "insufficient: accruals_over_total_assets has no value for quarters-back-0, and the cell gives the quoted reason. Both its quarter-over-quarter and year-over-year entries read 'accruals_over_total_assets is not filled in quarters-back-0'. In the whole quarterly history only quarters-back-2 and quarters-back-6 are filled (2 quarters), which does not support a trend claim.",
  "account": "net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-30",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-02-01..2026-04-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001327567-26-000015:trends:accruals_over_total_assets:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_days_sales_of_inventory_latest_quarter_insufficient",
  "what_changed": "insufficient: days_sales_of_inventory has no value for quarters-back-0, and the cell gives the quoted reason. No quarter in the table is filled for this metric; only years-back-0 and years-back-1 are.",
  "account": "inventory (InventoryNet) against cost of revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-30",
  "quote": "\"missing\": \"no row for inventory in 2026-04-30: us-gaap:InventoryNet is in the record, but not for this period\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_of_inventory:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_inventory_reserve_ratio_latest_quarter_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio has no value for quarters-back-0. The cell says the record tags no inventory valuation reserve in any period, and the ratio is filled in no period of the table.",
  "account": "inventory valuation reserve (InventoryValuationReserves) against inventory",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-30",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:inventory_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_trend_warranty_reserve_ratio_latest_quarter_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio has no value for quarters-back-0. The cell says the record tags no warranty accrual concept in any period, and the ratio is filled in no period of the table.",
  "account": "product warranty accrual (StandardProductWarrantyAccrual, ProductWarrantyAccrual, StandardProductWarrantyAccrualCurrent)",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-30",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:warranty_reserve_ratio:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_trend_non_gaap_gap_latest_quarter_insufficient",
  "what_changed": "insufficient: non_gaap_gap has no value for quarters-back-0, and it is filled in no period of the table. The cell says no us-gaap concept carries a non-GAAP measure. There is also no 8-K earnings release in my input that could supply one.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001327567-26-000015:trends:non_gaap_gap:2026-02-01..2026-04-30" }
```

### Trend table — years-back-0 (fiscal year 2024-08-01..2025-07-31, 365 days)

```json
{ "id": "earnings_quality_trend_accruals_over_total_assets_latest_fiscal_year",
  "what_changed": "accruals_over_total_assets is -0.10952239565659994. Its inputs come from two filings: net income 1133900000.0 and operating cash flow 3716000000.0 from 0001327567-25-000027, and assets 23576000000.0 from 0001327567-26-000015. The change against years-back-1 is -0.07550691861454581; the quarter-over-quarter entry reads 'an annual period has no preceding quarter'. The cell prints its position as second highest of the 5 filled years.",
  "account": "net income (NetIncomeLoss) less operating cash flow (NetCashProvidedByUsedInOperatingActivities), over total assets (Assets)",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1 (ended 2024-07-31)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:accruals_over_total_assets:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_latest_fiscal_year",
  "what_changed": "bad_debt_reserve_ratio is 0.0033613445378151263 (allowance 10000000.0, receivables 2965000000.0, both from 0001327567-26-000015). The change against years-back-1 is 0.0005053984580771116. The cell prints its position as third highest of the 5 filled years.",
  "account": "allowance for doubtful accounts (AllowanceForDoubtfulAccountsReceivableCurrent) over receivables plus allowance",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:bad_debt_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_trend_contract_liabilities_over_revenue_latest_fiscal_year",
  "what_changed": "contract_liabilities_over_revenue is 0.6834029170959172 (current contract liabilities 6302000000.0 from 0001327567-26-000015 over annual revenue 9221500000.0 from 0001327567-25-000027). The change against years-back-1 is -0.006861797946125847. The cell prints its position as second highest of the 5 filled years.",
  "account": "contract liabilities, current (ContractWithCustomerLiabilityCurrent) over revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:contract_liabilities_over_revenue:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_days_sales_of_inventory_latest_fiscal_year",
  "what_changed": "days_sales_of_inventory is 16.88325991189427 (inventory 113400000.0, cost of revenue 2451600000.0). The change against years-back-1 is -3.7166818130474546. The cell prints its position as lowest of the 2 filled years. Two years of history do not support a trend claim: insufficient for a trend.",
  "account": "inventory (InventoryNet) against cost of revenue (CostOfGoodsAndServicesSold)",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_of_inventory:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_trend_days_sales_outstanding_latest_fiscal_year",
  "what_changed": "days_sales_outstanding is 117.35888955159137 (year-end receivables 2965000000.0 against annual revenue 9221500000.0, 365 days). The change against years-back-1 is -2.0316554499657684. The cell prints its position as second lowest of the 5 filled years.",
  "account": "accounts receivable, net, current against revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:days_sales_outstanding:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_gross_margin_latest_fiscal_year",
  "what_changed": "gross_margin is 0.734143035297945 (cost of revenue 2451600000.0, revenue 9221500000.0). The change against years-back-1 is -0.009338746078573212. The cell prints its position as second highest of the 5 filled years.",
  "account": "revenue less cost of revenue, over revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:gross_margin:2024-08-01..2025-07-31" }
```

```json
{ "id": "revenue_recognition_trend_receivables_over_revenue_latest_fiscal_year",
  "what_changed": "receivables_over_revenue is 0.3215312042509353 (receivables 2965000000.0, revenue 9221500000.0). The change against years-back-1 is -0.0046724706167071695. The cell prints its position as second lowest of the 5 filled years.",
  "account": "accounts receivable, net, current over revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:receivables_over_revenue:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_soft_asset_share_latest_fiscal_year",
  "what_changed": "soft_asset_share is 0.8873430607397353 (assets 23576000000.0, property and equipment 387000000.0, cash 2269000000.0). The change against years-back-1 is -0.017798778797254. The cell prints its position as third highest of the 5 filled years.",
  "account": "total assets less property and equipment less cash, over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-07-31 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001327567-26-000015:trends:soft_asset_share:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_inventory_reserve_ratio_latest_fiscal_year_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio has no value for years-back-0, and the cell gives the quoted reason. Its year-over-year entry reads 'inventory_reserve_ratio is not filled in years-back-0'.",
  "account": "inventory valuation reserve (InventoryValuationReserves) against inventory",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-07-31",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:inventory_reserve_ratio:2024-08-01..2025-07-31" }
```

```json
{ "id": "earnings_quality_trend_non_gaap_gap_latest_fiscal_year_insufficient",
  "what_changed": "insufficient: non_gaap_gap has no value for years-back-0, and the cell gives the quoted reason. Its year-over-year entry reads 'non_gaap_gap is not filled in years-back-0'.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-07-31",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001327567-26-000015:trends:non_gaap_gap:2024-08-01..2025-07-31" }
```

```json
{ "id": "estimates_and_discretion_trend_warranty_reserve_ratio_latest_fiscal_year_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio has no value for years-back-0, and the cell gives the quoted reason. Its year-over-year entry reads 'warranty_reserve_ratio is not filled in years-back-0'.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-07-31",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001327567-26-000015:trends:warranty_reserve_ratio:2024-08-01..2025-07-31" }
```

### Articulation gaps, restated prior values, changes of tag

My input contains no articulation checks, no restatement traces and no fourth-quarter derivation, so there is nothing to quote and no item is written. Nothing in my input says a period rests on a different concept.

### Numeric facts — income statement, current 10-Q (0001327567-26-000015)

```json
{ "id": "revenue_recognition_fact_total_revenue_latest_quarter",
  "what_changed": "Revenue for 2026-02-01..2026-04-30 is printed as 3002000000. The same filing prints 2289000000 for 2025-02-01..2025-04-30.",
  "account": "revenue (RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"3002000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_total_revenue_nine_months",
  "what_changed": "Revenue for 2025-08-01..2026-04-30 is printed as 8070000000. The same filing prints 6685000000 for 2024-08-01..2025-04-30.",
  "account": "revenue (RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"8070000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_product_revenue_latest_quarter",
  "what_changed": "Product revenue (ProductOrServiceAxis=ProductMember) for 2026-02-01..2026-04-30 is printed as 594000000, against 453000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 1542000000 against 1228000000.",
  "account": "revenue, product member",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"594000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_fact_service_revenue_latest_quarter",
  "what_changed": "Service revenue (ProductOrServiceAxis=ServiceMember) for 2026-02-01..2026-04-30 is printed as 2408000000, against 1836000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 6528000000 against 5457000000.",
  "account": "revenue, service member",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"2408000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "revenue_recognition_fact_subscription_revenue_latest_quarter",
  "what_changed": "Subscription revenue (ProductOrServiceAxis=panw:SubscriptionMember) for 2026-02-01..2026-04-30 is printed as 1632000000, against 1234000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 4400000000 against 3659000000.",
  "account": "revenue, subscription member",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"1632000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=panw:SubscriptionMember" }
```

```json
{ "id": "revenue_recognition_fact_support_revenue_latest_quarter",
  "what_changed": "Support revenue (ProductOrServiceAxis=panw:SupportMember) for 2026-02-01..2026-04-30 is printed as 776000000, against 602000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 2128000000 against 1798000000.",
  "account": "revenue, support member",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"776000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=panw:SupportMember" }
```

```json
{ "id": "revenue_recognition_fact_americas_revenue_latest_quarter",
  "what_changed": "Americas revenue for 2026-02-01..2026-04-30 is printed as 2018000000, against 1530000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 5371000000 against 4474000000.",
  "account": "revenue, StatementGeographicalAxis=AmericasMember",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"2018000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_fact_emea_revenue_latest_quarter",
  "what_changed": "EMEA revenue for 2026-02-01..2026-04-30 is printed as 633000000, against 480000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 1714000000 against 1402000000.",
  "account": "revenue, StatementGeographicalAxis=EMEAMember",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"633000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_fact_asia_pacific_revenue_latest_quarter",
  "what_changed": "Asia Pacific revenue for 2026-02-01..2026-04-30 is printed as 351000000, against 279000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 985000000 against 809000000.",
  "account": "revenue, StatementGeographicalAxis=AsiaPacificMember",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"351000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-02-01..2026-04-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "earnings_quality_fact_cost_of_revenue_latest_quarter",
  "what_changed": "Cost of revenue for 2026-02-01..2026-04-30 is printed as 974000000, against 619000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 2297000000 against 1772000000.",
  "account": "cost of revenue (CostOfGoodsAndServicesSold)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"974000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_service_cost_of_revenue_latest_quarter",
  "what_changed": "Service cost of revenue for 2026-02-01..2026-04-30 is printed as 807000000, against 518000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 1926000000 against 1495000000.",
  "account": "cost of revenue, service member",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"807000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "earnings_quality_fact_product_cost_of_revenue_latest_quarter",
  "what_changed": "Product cost of revenue for 2026-02-01..2026-04-30 is printed as 167000000, against 101000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 371000000 against 277000000.",
  "account": "cost of revenue, product member",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"167000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CostOfGoodsAndServicesSold:2026-02-01..2026-04-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "earnings_quality_fact_gross_profit_latest_quarter",
  "what_changed": "Gross profit for 2026-02-01..2026-04-30 is printed as 2028000000, against 1670000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 5773000000 against 4913000000.",
  "account": "gross profit (GrossProfit)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"2028000000\"",
  "paragraph_id": "0001327567-26-000015:facts:GrossProfit:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_research_and_development_expense_latest_quarter",
  "what_changed": "Research and development expense for 2026-02-01..2026-04-30 is printed as 734000000, against 494000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 1773000000 against 1480000000.",
  "account": "research and development expense (ResearchAndDevelopmentExpense)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"734000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ResearchAndDevelopmentExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_selling_and_marketing_expense_latest_quarter",
  "what_changed": "Selling and marketing expense for 2026-02-01..2026-04-30 is printed as 1161000000, against 793000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 2804000000 against 2271000000.",
  "account": "selling and marketing expense (SellingAndMarketingExpense)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"1161000000\"",
  "paragraph_id": "0001327567-26-000015:facts:SellingAndMarketingExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_general_and_administrative_expense_latest_quarter",
  "what_changed": "General and administrative expense for 2026-02-01..2026-04-30 is printed as 316000000, against 164000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 673000000 against 416000000.",
  "account": "general and administrative expense (GeneralAndAdministrativeExpense)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"316000000\"",
  "paragraph_id": "0001327567-26-000015:facts:GeneralAndAdministrativeExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_total_operating_expenses_latest_quarter",
  "what_changed": "Operating expenses for 2026-02-01..2026-04-30 are printed as 2211000000, against 1451000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 5250000000 against 4167000000.",
  "account": "operating expenses (OperatingExpenses)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"2211000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingExpenses:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_operating_loss_latest_quarter",
  "what_changed": "Operating income (loss) for 2026-02-01..2026-04-30 is printed as -183000000. The same filing prints 219000000 for 2025-02-01..2025-04-30.",
  "account": "operating income (loss) (OperatingIncomeLoss)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"-183000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingIncomeLoss:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_operating_income_nine_months",
  "what_changed": "Operating income for 2025-08-01..2026-04-30 is printed as 523000000. The same filing prints 746000000 for 2024-08-01..2025-04-30.",
  "account": "operating income (loss) (OperatingIncomeLoss)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"523000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingIncomeLoss:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_interest_expense_latest_quarter",
  "what_changed": "Nonoperating interest expense for 2026-02-01..2026-04-30 is printed as 0, against 1000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 0 against 3000000.",
  "account": "interest expense, nonoperating (InterestExpenseNonoperating)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001327567-26-000015:facts:InterestExpenseNonoperating:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_other_nonoperating_income_latest_quarter",
  "what_changed": "Other nonoperating income for 2026-02-01..2026-04-30 is printed as 8000000. The same filing prints 8000000 for 2025-02-01..2025-04-30.",
  "account": "other nonoperating income (expense) (OtherNonoperatingIncomeExpense)",
  "expected_direction": "none",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"8000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherNonoperatingIncomeExpense:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_other_nonoperating_income_nine_months",
  "what_changed": "Other nonoperating income for 2025-08-01..2026-04-30 is printed as 76000000. The same filing prints 9000000 for 2024-08-01..2025-04-30.",
  "account": "other nonoperating income (expense) (OtherNonoperatingIncomeExpense)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"76000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherNonoperatingIncomeExpense:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_pretax_loss_latest_quarter",
  "what_changed": "Income (loss) before income taxes for 2026-02-01..2026-04-30 is printed as -156000000, against 311000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 805000000 against 1004000000.",
  "account": "income (loss) before income taxes (IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"-156000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_income_tax_expense_latest_quarter",
  "what_changed": "Income tax expense for 2026-02-01..2026-04-30 is printed as 21000000, in the same quarter that pre-tax income is printed as -156000000. The comparative quarter prints 49000000; for the nine months the filing prints 216000000 against 124000000. No effective rate is in my input.",
  "account": "income tax expense (benefit) (IncomeTaxExpenseBenefit)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"21000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncomeTaxExpenseBenefit:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_net_loss_latest_quarter",
  "what_changed": "Net income (loss) for 2026-02-01..2026-04-30 is printed as -177000000. The same filing prints 262000000 for 2025-02-01..2025-04-30. The trend table's accruals cell for this quarter could not be filled because no quarterly operating cash flow is in the record.",
  "account": "net income (loss) (NetIncomeLoss)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"-177000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetIncomeLoss:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_net_income_nine_months",
  "what_changed": "Net income for 2025-08-01..2026-04-30 is printed as 589000000. The same filing prints 880000000 for 2024-08-01..2025-04-30.",
  "account": "net income (loss) (NetIncomeLoss)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"589000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetIncomeLoss:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_diluted_earnings_per_share_latest_quarter",
  "what_changed": "Diluted EPS for 2026-02-01..2026-04-30 is printed as -0.22, against 0.37 for 2025-02-01..2025-04-30. For the nine months the filing prints 0.79 against 1.24.",
  "account": "earnings per share, diluted (EarningsPerShareDiluted)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"-0.22\"",
  "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareDiluted:2026-02-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_basic_earnings_per_share_latest_quarter",
  "what_changed": "Basic EPS for 2026-02-01..2026-04-30 is printed as -0.22, against 0.39 for 2025-02-01..2025-04-30. For the nine months the filing prints 0.81 against 1.33.",
  "account": "earnings per share, basic (EarningsPerShareBasic)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"-0.22\"",
  "paragraph_id": "0001327567-26-000015:facts:EarningsPerShareBasic:2026-02-01..2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_weighted_average_basic_shares_latest_quarter",
  "what_changed": "Weighted-average basic shares for 2026-02-01..2026-04-30 are printed as 801000000, against 665000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 729000000 against 659000000.",
  "account": "weighted average shares outstanding, basic (WeightedAverageNumberOfSharesOutstandingBasic)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"801000000\"",
  "paragraph_id": "0001327567-26-000015:facts:WeightedAverageNumberOfSharesOutstandingBasic:2026-02-01..2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_weighted_average_diluted_shares_latest_quarter",
  "what_changed": "Weighted-average diluted shares for 2026-02-01..2026-04-30 are printed as 801000000, against 707000000 for 2025-02-01..2025-04-30. For the nine months the filing prints 744000000 against 708000000.",
  "account": "weighted average diluted shares outstanding (WeightedAverageNumberOfDilutedSharesOutstanding)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-04-30 against three months ended 2025-04-30",
  "quote": "\"value\": \"801000000\"",
  "paragraph_id": "0001327567-26-000015:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2026-02-01..2026-04-30" }
```

### Numeric facts — cash flow statement, current 10-Q (nine months only; no three-month cash flow figure exists in the record)

```json
{ "id": "liquidity_and_capital_fact_operating_cash_flow_nine_months",
  "what_changed": "Net cash from operating activities for 2025-08-01..2026-04-30 is printed as 3196000000. The same filing prints 2695000000 for 2024-08-01..2025-04-30. The trend table records no operating cash flow for the three months ended 2026-04-30.",
  "account": "net cash provided by operating activities (NetCashProvidedByUsedInOperatingActivities)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"3196000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetCashProvidedByUsedInOperatingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_share_based_compensation_nine_months",
  "what_changed": "Share-based compensation for 2025-08-01..2026-04-30 is printed as 1314000000. The same filing prints 941000000 for 2024-08-01..2025-04-30.",
  "account": "share-based compensation (ShareBasedCompensation)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"1314000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ShareBasedCompensation:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_depreciation_and_amortization_nine_months",
  "what_changed": "Depreciation and amortization for 2025-08-01..2026-04-30 is printed as 514000000. The same filing prints 259000000 for 2024-08-01..2025-04-30.",
  "account": "depreciation, depletion and amortization (DepreciationDepletionAndAmortization)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"514000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DepreciationDepletionAndAmortization:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_capitalized_contract_cost_amortization_nine_months",
  "what_changed": "Amortization of capitalized contract costs for 2025-08-01..2026-04-30 is printed as 410000000. The same filing prints 344000000 for 2024-08-01..2025-04-30.",
  "account": "capitalized contract cost amortization (CapitalizedContractCostAmortization)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"410000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostAmortization:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_deferred_income_taxes_nine_months",
  "what_changed": "Deferred income taxes in operating cash flow for 2025-08-01..2026-04-30 are printed as 38000000. The same filing prints -442000000 for 2024-08-01..2025-04-30.",
  "account": "deferred income taxes and tax credits (DeferredIncomeTaxesAndTaxCredits)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"38000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxesAndTaxCredits:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_contingent_consideration_remeasurement_nine_months",
  "what_changed": "The change in the contingent consideration liability, as an operating adjustment for 2025-08-01..2026-04-30, is printed as -120000000. The same filing prints 20000000 for 2024-08-01..2025-04-30.",
  "account": "change in amount of contingent consideration liability (BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-120000000\"",
  "paragraph_id": "0001327567-26-000015:facts:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_operating_lease_asset_amortization_nine_months",
  "what_changed": "Amortization of operating lease right-of-use assets for 2025-08-01..2026-04-30 is printed as 54000000. The same filing prints 48000000 for 2024-08-01..2025-04-30.",
  "account": "operating lease right-of-use asset amortization (OperatingLeaseRightOfUseAssetAmortizationExpense)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"54000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseRightOfUseAssetAmortizationExpense:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_investment_premium_accretion_nine_months",
  "what_changed": "Accretion and amortization of discounts and premiums on investments for 2025-08-01..2026-04-30 is printed as 53000000. The same filing prints 35000000 for 2024-08-01..2025-04-30.",
  "account": "accretion (amortization) of discounts and premiums, investments (AccretionAmortizationOfDiscountsAndPremiumsInvestments)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"53000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccretionAmortizationOfDiscountsAndPremiumsInvestments:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_unrealized_currency_loss_nine_months",
  "what_changed": "Unrealized foreign currency transaction gain (loss) for 2025-08-01..2026-04-30 is printed as -9000000. The same filing prints 0 for 2024-08-01..2025-04-30.",
  "account": "foreign currency transaction gain (loss), unrealized (ForeignCurrencyTransactionGainLossUnrealizedAfterTax)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-9000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ForeignCurrencyTransactionGainLossUnrealizedAfterTax:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_financing_cost_amortization_nine_months",
  "what_changed": "Amortization of financing costs and discounts for 2025-08-01..2026-04-30 is printed as 0. The same filing prints 1000000 for 2024-08-01..2025-04-30.",
  "account": "amortization of financing costs and discounts (AmortizationOfFinancingCostsAndDiscounts)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001327567-26-000015:facts:AmortizationOfFinancingCostsAndDiscounts:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_receivables_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in accounts receivable line of operating cash flow for 2025-08-01..2026-04-30 is printed as -441000000. The same filing prints -669000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in accounts receivable (IncreaseDecreaseInAccountsReceivable)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-441000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInAccountsReceivable:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_financing_receivables_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in finance receivables line of operating cash flow for 2025-08-01..2026-04-30 is printed as -347000000. The same filing prints -102000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in finance receivables (IncreaseDecreaseInFinanceReceivables)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-347000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInFinanceReceivables:2025-08-01..2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_contract_liability_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in contract liabilities line of operating cash flow for 2025-08-01..2026-04-30 is printed as 53000000. The same filing prints 64000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in contract with customer liability (IncreaseDecreaseInContractWithCustomerLiability)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"53000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-08-01..2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_prepaid_and_other_assets_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in prepaid, deferred expense and other assets line for 2025-08-01..2026-04-30 is printed as 47000000. The same filing prints -68000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in prepaid deferred expense and other assets (IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"47000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_payables_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in accounts payable line for 2025-08-01..2026-04-30 is printed as 50000000. The same filing prints 119000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in accounts payable (IncreaseDecreaseInAccountsPayable)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"50000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInAccountsPayable:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_employee_liabilities_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in employee-related liabilities line for 2025-08-01..2026-04-30 is printed as -42000000. The same filing prints -49000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in employee related liabilities (IncreaseDecreaseInEmployeeRelatedLiabilities)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-42000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInEmployeeRelatedLiabilities:2025-08-01..2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_accrued_liabilities_working_capital_change_nine_months",
  "what_changed": "The increase/decrease in accrued liabilities and other operating liabilities line for 2025-08-01..2026-04-30 is printed as 11000000. The same filing prints 34000000 for 2024-08-01..2025-04-30.",
  "account": "increase (decrease) in accrued liabilities and other operating liabilities (IncreaseDecreaseInAccruedLiabilitiesAndOtherOperatingLiabilities)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"11000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IncreaseDecreaseInAccruedLiabilitiesAndOtherOperatingLiabilities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_business_acquisition_payments_nine_months",
  "what_changed": "Payments to acquire businesses, net of cash acquired, for 2025-08-01..2026-04-30 are printed as 4563000000. The same filing prints 499000000 for 2024-08-01..2025-04-30.",
  "account": "payments to acquire businesses, net of cash acquired (PaymentsToAcquireBusinessesNetOfCashAcquired)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"4563000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsToAcquireBusinessesNetOfCashAcquired:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_capital_expenditure_nine_months",
  "what_changed": "Payments to acquire productive assets for 2025-08-01..2026-04-30 are printed as 337000000. The same filing prints 160000000 for 2024-08-01..2025-04-30.",
  "account": "payments to acquire productive assets (PaymentsToAcquireProductiveAssets)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"337000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsToAcquireProductiveAssets:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_investment_purchases_nine_months",
  "what_changed": "Payments to acquire investments for 2025-08-01..2026-04-30 are printed as 2421000000. The same filing prints 2821000000 for 2024-08-01..2025-04-30.",
  "account": "payments to acquire investments (PaymentsToAcquireInvestments)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"2421000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsToAcquireInvestments:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_investment_sale_proceeds_nine_months",
  "what_changed": "Proceeds from sales of available-for-sale debt securities for 2025-08-01..2026-04-30 are printed as 3399000000. The same filing prints 830000000 for 2024-08-01..2025-04-30.",
  "account": "proceeds from sale of available-for-sale debt securities (ProceedsFromSaleOfAvailableForSaleSecuritiesDebt)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"3399000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromSaleOfAvailableForSaleSecuritiesDebt:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_investment_maturity_proceeds_nine_months",
  "what_changed": "Proceeds from maturities, prepayments and calls of available-for-sale securities for 2025-08-01..2026-04-30 are printed as 1824000000. The same filing prints 1208000000 for 2024-08-01..2025-04-30.",
  "account": "proceeds from maturities, prepayments and calls of available-for-sale securities (ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"1824000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_investing_cash_flow_nine_months",
  "what_changed": "Net cash used in investing activities for 2025-08-01..2026-04-30 is printed as -2098000000. The same filing prints -1442000000 for 2024-08-01..2025-04-30.",
  "account": "net cash provided by (used in) investing activities (NetCashProvidedByUsedInInvestingActivities)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-2098000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetCashProvidedByUsedInInvestingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_share_repurchase_nine_months",
  "what_changed": "Payments for repurchase of common stock for 2025-08-01..2026-04-30 are printed as 1000000000. The same filing prints 0 for 2024-08-01..2025-04-30.",
  "account": "payments for repurchase of common stock (PaymentsForRepurchaseOfCommonStock)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"1000000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsForRepurchaseOfCommonStock:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_proceeds_nine_months",
  "what_changed": "Proceeds from convertible debt for 2025-08-01..2026-04-30 are printed as 10000000, against 0 for 2024-08-01..2025-04-30. Repayments of convertible debt are printed as 0 for the current nine months and 583000000 for the prior nine months.",
  "account": "proceeds from convertible debt (ProceedsFromConvertibleDebt); repayments of convertible debt (RepaymentsOfConvertibleDebt)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"10000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromConvertibleDebt:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_contingent_consideration_payments_nine_months",
  "what_changed": "Payments for contingent consideration liability, in financing activities for 2025-08-01..2026-04-30, are printed as 154000000. The same filing prints 0 for 2024-08-01..2025-04-30.",
  "account": "payment for contingent consideration liability, financing activities (PaymentForContingentConsiderationLiabilityFinancingActivities)",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"154000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentForContingentConsiderationLiabilityFinancingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_employee_share_issuance_proceeds_nine_months",
  "what_changed": "Proceeds from issuance of shares under incentive and share-based plans for 2025-08-01..2026-04-30 are printed as 264000000. The same filing prints 361000000 for 2024-08-01..2025-04-30.",
  "account": "proceeds from issuance of shares under incentive and share-based compensation plans (ProceedsFromIssuanceOfSharesUnderIncentiveAndShareBasedCompensationPlansIncludingStockOptions)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"264000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ProceedsFromIssuanceOfSharesUnderIncentiveAndShareBasedCompensationPlansIncludingStockOptions:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_share_withholding_tax_payments_nine_months",
  "what_changed": "Payments related to tax withholding for share-based compensation for 2025-08-01..2026-04-30 are printed as 125000000. The same filing prints 183000000 for 2024-08-01..2025-04-30.",
  "account": "payments related to tax withholding for share-based compensation (PaymentsRelatedToTaxWithholdingForShareBasedCompensation)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"125000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PaymentsRelatedToTaxWithholdingForShareBasedCompensation:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_financing_cash_flow_nine_months",
  "what_changed": "Net cash used in financing activities for 2025-08-01..2026-04-30 is printed as -1005000000. The same filing prints -405000000 for 2024-08-01..2025-04-30.",
  "account": "net cash provided by (used in) financing activities (NetCashProvidedByUsedInFinancingActivities)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"-1005000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NetCashProvidedByUsedInFinancingActivities:2025-08-01..2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_net_change_in_cash_nine_months",
  "what_changed": "The period increase in cash, cash equivalents and restricted cash for 2025-08-01..2026-04-30 is printed as 95000000. The same filing prints 848000000 for 2024-08-01..2025-04-30. Cash, cash equivalents and restricted cash at 2025-07-31 are printed as 2279000000.",
  "account": "cash, cash equivalents, restricted cash, period increase (decrease) including exchange rate effect",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-04-30 against nine months ended 2025-04-30",
  "quote": "\"value\": \"95000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect:2025-08-01..2026-04-30" }
```

### Numeric facts — balance sheet, current 10-Q (2026-04-30 against 2025-07-31)

```json
{ "id": "liquidity_and_capital_fact_cash_and_equivalents_balance",
  "what_changed": "Cash and cash equivalents at 2026-04-30 are printed as 2364000000. The same filing prints 2269000000 at 2025-07-31. The trend table's quarters-back-1 input for 2026-01-31, from 0001327567-26-000005, is 4158000000.0.",
  "account": "cash and cash equivalents (CashAndCashEquivalentsAtCarryingValue)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"2364000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CashAndCashEquivalentsAtCarryingValue:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_short_term_investments_balance",
  "what_changed": "Short-term investments at 2026-04-30 are printed as 747000000. The same filing prints 635000000 at 2025-07-31.",
  "account": "short-term investments (ShortTermInvestments)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"747000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ShortTermInvestments:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_long_term_investments_balance",
  "what_changed": "Long-term investments at 2026-04-30 are printed as 3881000000. The same filing prints 5555000000 at 2025-07-31.",
  "account": "long-term investments (LongTermInvestments)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"3881000000\"",
  "paragraph_id": "0001327567-26-000015:facts:LongTermInvestments:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_accounts_receivable_balance",
  "what_changed": "Accounts receivable, net, at 2026-04-30 is printed as 2852000000. The same filing prints 2965000000 at 2025-07-31. The trend table's quarters-back-1 input for 2026-01-31 is 2116000000.0.",
  "account": "accounts receivable, net, current (AccountsReceivableNetCurrent)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"2852000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccountsReceivableNetCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_allowance_for_doubtful_accounts_balance",
  "what_changed": "The allowance for doubtful accounts at 2026-04-30 is printed as 6000000. The same filing prints 10000000 at 2025-07-31. The trend table's quarters-back-1 input for 2026-01-31 is 13000000.0.",
  "account": "allowance for doubtful accounts receivable, current (AllowanceForDoubtfulAccountsReceivableCurrent)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"6000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_financing_receivables_current_balance",
  "what_changed": "Notes and loans receivable, net, current at 2026-04-30 are printed as 591000000. The same filing prints 715000000 at 2025-07-31.",
  "account": "notes and loans receivable, net, current (NotesAndLoansReceivableNetCurrent)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"591000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NotesAndLoansReceivableNetCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_financing_receivables_noncurrent_balance",
  "what_changed": "Notes and loans receivable, net, noncurrent at 2026-04-30 are printed as 779000000. The same filing prints 1002000000 at 2025-07-31.",
  "account": "notes and loans receivable, net, noncurrent (NotesAndLoansReceivableNetNoncurrent)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"779000000\"",
  "paragraph_id": "0001327567-26-000015:facts:NotesAndLoansReceivableNetNoncurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_capitalized_contract_cost_current_balance",
  "what_changed": "Capitalized contract cost, net, current at 2026-04-30 is printed as 454000000. The same filing prints 419000000 at 2025-07-31.",
  "account": "capitalized contract cost, net, current (CapitalizedContractCostNetCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"454000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostNetCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_capitalized_contract_cost_noncurrent_balance",
  "what_changed": "Capitalized contract cost, net, noncurrent at 2026-04-30 is printed as 551000000. The same filing prints 586000000 at 2025-07-31.",
  "account": "capitalized contract cost, net, noncurrent (CapitalizedContractCostNetNoncurrent)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"551000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CapitalizedContractCostNetNoncurrent:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_prepaid_and_other_current_assets_balance",
  "what_changed": "Prepaid expenses and other current assets at 2026-04-30 are printed as 705000000. The same filing prints 520000000 at 2025-07-31.",
  "account": "prepaid expense and other assets, current (PrepaidExpenseAndOtherAssetsCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"705000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PrepaidExpenseAndOtherAssetsCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_current_assets_balance",
  "what_changed": "Total current assets at 2026-04-30 are printed as 7713000000. The same filing prints 7523000000 at 2025-07-31.",
  "account": "assets, current (AssetsCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"7713000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AssetsCurrent:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_property_and_equipment_balance",
  "what_changed": "Property and equipment, net, at 2026-04-30 is printed as 506000000. The same filing prints 387000000 at 2025-07-31.",
  "account": "property, plant and equipment, net (PropertyPlantAndEquipmentNet)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"506000000\"",
  "paragraph_id": "0001327567-26-000015:facts:PropertyPlantAndEquipmentNet:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_operating_lease_asset_balance",
  "what_changed": "Operating lease right-of-use assets at 2026-04-30 are printed as 678000000. The same filing prints 347000000 at 2025-07-31.",
  "account": "operating lease right-of-use asset (OperatingLeaseRightOfUseAsset)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"678000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseRightOfUseAsset:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_goodwill_balance",
  "what_changed": "Goodwill at 2026-04-30 is printed as 21902000000. The same filing prints 4567000000 at 2025-07-31.",
  "account": "goodwill (Goodwill)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"21902000000\"",
  "paragraph_id": "0001327567-26-000015:facts:Goodwill:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_intangible_assets_balance",
  "what_changed": "Intangible assets, net, excluding goodwill, at 2026-04-30 are printed as 7283000000. The same filing prints 763000000 at 2025-07-31.",
  "account": "intangible assets, net, excluding goodwill (IntangibleAssetsNetExcludingGoodwill)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"7283000000\"",
  "paragraph_id": "0001327567-26-000015:facts:IntangibleAssetsNetExcludingGoodwill:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_deferred_tax_assets_balance",
  "what_changed": "Deferred income tax assets, net, at 2026-04-30 are printed as 2380000000. The same filing prints 2424000000 at 2025-07-31.",
  "account": "deferred income tax assets, net (DeferredIncomeTaxAssetsNet)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"2380000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxAssetsNet:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_other_noncurrent_assets_balance",
  "what_changed": "Other noncurrent assets at 2026-04-30 are printed as 593000000. The same filing prints 422000000 at 2025-07-31.",
  "account": "other assets, noncurrent (OtherAssetsNoncurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"593000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherAssetsNoncurrent:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_total_assets_balance",
  "what_changed": "Total assets at 2026-04-30 are printed as 46266000000. The same filing prints 23576000000 at 2025-07-31. The trend table's quarters-back-1 input for 2026-01-31, from 0001327567-26-000005, is 24979000000.0.",
  "account": "assets (Assets)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"46266000000\"",
  "paragraph_id": "0001327567-26-000015:facts:Assets:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_accounts_payable_balance",
  "what_changed": "Accounts payable at 2026-04-30 are printed as 293000000. The same filing prints 232000000 at 2025-07-31.",
  "account": "accounts payable, current (AccountsPayableCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"293000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccountsPayableCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_employee_related_liabilities_balance",
  "what_changed": "Employee-related liabilities, current, at 2026-04-30 are printed as 680000000. The same filing prints 608000000 at 2025-07-31.",
  "account": "employee related liabilities, current (EmployeeRelatedLiabilitiesCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"680000000\"",
  "paragraph_id": "0001327567-26-000015:facts:EmployeeRelatedLiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "estimates_and_discretion_fact_accrued_liabilities_balance",
  "what_changed": "Accrued liabilities, current, at 2026-04-30 are printed as 760000000. The same filing prints 846000000 at 2025-07-31.",
  "account": "accrued liabilities, current (AccruedLiabilitiesCurrent)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"760000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccruedLiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_contract_liabilities_current_balance",
  "what_changed": "Contract liabilities, current, at 2026-04-30 are printed as 7113000000. The same filing prints 6302000000 at 2025-07-31. The trend table's quarters-back-1 input for 2026-01-31 is 6248000000.0.",
  "account": "contract with customer liability, current (ContractWithCustomerLiabilityCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"7113000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ContractWithCustomerLiabilityCurrent:2026-04-30" }
```

```json
{ "id": "revenue_recognition_fact_contract_liabilities_noncurrent_balance",
  "what_changed": "Contract liabilities, noncurrent, at 2026-04-30 are printed as 6492000000. The same filing prints 6450000000 at 2025-07-31. This noncurrent portion is not an input to the trend table's contract_liabilities_over_revenue.",
  "account": "contract with customer liability, noncurrent (ContractWithCustomerLiabilityNoncurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"6492000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ContractWithCustomerLiabilityNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_current_balance",
  "what_changed": "Convertible debt, current, at 2026-04-30 is printed as 160000000. The same filing prints 0 at 2025-07-31.",
  "account": "convertible debt, current (ConvertibleDebtCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"160000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ConvertibleDebtCurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_debt_noncurrent_balance",
  "what_changed": "Convertible debt, noncurrent, at 2026-04-30 is printed as 1192000000. The same filing prints 0 at 2025-07-31.",
  "account": "convertible debt, noncurrent (ConvertibleDebtNoncurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"1192000000\"",
  "paragraph_id": "0001327567-26-000015:facts:ConvertibleDebtNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_convertible_notes_face_amount",
  "what_changed": "The face amount of the ConvertibleSeniorNotesDue2030Member instrument is printed as 1250000000 at instant 2026-02-11. It appears twice in the filing's facts (f-1144 and f-1456), both with this value. No comparative is in my input.",
  "account": "debt instrument face amount, convertible senior notes due 2030 (DebtInstrumentFaceAmount)",
  "expected_direction": "none",
  "horizon": "instant 2026-02-11",
  "quote": "\"value\": \"1250000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DebtInstrumentFaceAmount:2026-02-11:us-gaap:DebtInstrumentAxis=panw:ConvertibleSeniorNotesDue2030Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleDebtMember" }
```

```json
{ "id": "liquidity_and_capital_fact_current_liabilities_balance",
  "what_changed": "Total current liabilities at 2026-04-30 are printed as 9006000000. The same filing prints 7988000000 at 2025-07-31.",
  "account": "liabilities, current (LiabilitiesCurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"9006000000\"",
  "paragraph_id": "0001327567-26-000015:facts:LiabilitiesCurrent:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_deferred_tax_liabilities_balance",
  "what_changed": "Deferred income tax liabilities, net, at 2026-04-30 are printed as 259000000. The same filing prints 89000000 at 2025-07-31.",
  "account": "deferred income tax liabilities, net (DeferredIncomeTaxLiabilitiesNet)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"259000000\"",
  "paragraph_id": "0001327567-26-000015:facts:DeferredIncomeTaxLiabilitiesNet:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_operating_lease_liability_noncurrent_balance",
  "what_changed": "Operating lease liabilities, noncurrent, at 2026-04-30 are printed as 719000000. The same filing prints 338000000 at 2025-07-31.",
  "account": "operating lease liability, noncurrent (OperatingLeaseLiabilityNoncurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"719000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OperatingLeaseLiabilityNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_other_noncurrent_liabilities_balance",
  "what_changed": "Other noncurrent liabilities at 2026-04-30 are printed as 930000000. The same filing prints 887000000 at 2025-07-31.",
  "account": "other liabilities, noncurrent (OtherLiabilitiesNoncurrent)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"930000000\"",
  "paragraph_id": "0001327567-26-000015:facts:OtherLiabilitiesNoncurrent:2026-04-30" }
```

```json
{ "id": "liquidity_and_capital_fact_total_liabilities_balance",
  "what_changed": "Total liabilities at 2026-04-30 are printed as 18598000000. The same filing prints 15752000000 at 2025-07-31.",
  "account": "liabilities (Liabilities)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"18598000000\"",
  "paragraph_id": "0001327567-26-000015:facts:Liabilities:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_paid_in_capital_balance",
  "what_changed": "Common stock including additional paid-in capital at 2026-04-30 is printed as 24608000000. The same filing prints 5292000000 at 2025-07-31.",
  "account": "common stocks including additional paid in capital (CommonStocksIncludingAdditionalPaidInCapital)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"24608000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CommonStocksIncludingAdditionalPaidInCapital:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_shares_issued_balance",
  "what_changed": "Common shares issued at 2026-04-30 are printed as 813000000; common shares outstanding at 2026-04-30 are also printed as 813000000. The same filing prints 668000000 issued at 2025-07-31.",
  "account": "common stock shares issued (CommonStockSharesIssued)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"813000000\"",
  "paragraph_id": "0001327567-26-000015:facts:CommonStockSharesIssued:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_shares_outstanding_cover_page",
  "what_changed": "Shares outstanding on the cover (dei) at instant 2026-05-26 are printed as 815000000. No comparative is in my input.",
  "account": "entity common stock shares outstanding (dei:EntityCommonStockSharesOutstanding)",
  "expected_direction": "none",
  "horizon": "instant 2026-05-26",
  "quote": "\"value\": \"815000000\"",
  "paragraph_id": "0001327567-26-000015:facts:EntityCommonStockSharesOutstanding:2026-05-26" }
```

```json
{ "id": "earnings_quality_fact_accumulated_other_comprehensive_income_balance",
  "what_changed": "Accumulated other comprehensive income (loss) at 2026-04-30 is printed as -13000000. The same filing prints 48000000 at 2025-07-31.",
  "account": "accumulated other comprehensive income (loss), net of tax (AccumulatedOtherComprehensiveIncomeLossNetOfTax)",
  "expected_direction": "down",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"-13000000\"",
  "paragraph_id": "0001327567-26-000015:facts:AccumulatedOtherComprehensiveIncomeLossNetOfTax:2026-04-30" }
```

```json
{ "id": "earnings_quality_fact_retained_earnings_balance",
  "what_changed": "Retained earnings at 2026-04-30 are printed as 3073000000. The same filing prints 2484000000 at 2025-07-31.",
  "account": "retained earnings (accumulated deficit) (RetainedEarningsAccumulatedDeficit)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"3073000000\"",
  "paragraph_id": "0001327567-26-000015:facts:RetainedEarningsAccumulatedDeficit:2026-04-30" }
```

```json
{ "id": "structure_and_disclosure_changes_fact_stockholders_equity_balance",
  "what_changed": "Stockholders' equity at 2026-04-30 is printed as 27668000000. The same filing prints 7824000000 at 2025-07-31.",
  "account": "stockholders equity (StockholdersEquity)",
  "expected_direction": "up",
  "horizon": "balance at 2026-04-30 against balance at 2025-07-31",
  "quote": "\"value\": \"27668000000\"",
  "paragraph_id": "0001327567-26-000015:facts:StockholdersEquity:2026-04-30" }
```

### Numeric facts — prior 10-Q (0001327567-26-000005, filed 2026-02-18)

```json
{ "id": "related_parties_contingencies_and_subsequent_events_fact_cyberark_cash_payment",
  "what_changed": "The prior 10-Q prints PaymentsToAcquireBusinessesGross of 2300000000 for 2026-02-11, tagged with BusinessAcquisitionAxis=CyberArkSoftwareLtd.Member and SubsequentEventTypeAxis=SubsequentEventMember. No comparative is in my input.",
  "account": "payments to acquire businesses, gross, CyberArk (PaymentsToAcquireBusinessesGross)",
  "expected_direction": "none",
  "horizon": "event dated 2026-02-11, reported as a subsequent event in the quarter ended 2026-01-31",
  "quote": "\"value\": \"2300000000\"",
  "paragraph_id": "0001327567-26-000005:facts:PaymentsToAcquireBusinessesGross:2026-02-11..2026-02-11:us-gaap:BusinessAcquisitionAxis=panw:CyberArkSoftwareLtd.Member,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_fact_cyberark_shares_issued",
  "what_changed": "The prior 10-Q prints BusinessAcquisitionEquityInterestsIssuedOrIssuableNumberOfSharesIssued of 112000000 shares for 2026-02-11, tagged with the CyberArk acquisition member and the subsequent event member. No comparative is in my input.",
  "account": "equity interests issued or issuable in business acquisition, number of shares, CyberArk",
  "expected_direction": "none",
  "horizon": "event dated 2026-02-11, reported as a subsequent event in the quarter ended 2026-01-31",
  "quote": "\"value\": \"112000000\"",
  "paragraph_id": "0001327567-26-000005:facts:BusinessAcquisitionEquityInterestsIssuedOrIssuableNumberOfSharesIssued:2026-02-11..2026-02-11:us-gaap:BusinessAcquisitionAxis=panw:CyberArkSoftwareLtd.Member,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_fact_koi_security_consideration",
  "what_changed": "The prior 10-Q prints BusinessCombinationConsiderationTransferred1 of 300000000 for 2026-02-16, tagged with BusinessAcquisitionAxis=KoiSecurityLtdMember and the subsequent event member. No comparative is in my input.",
  "account": "business combination consideration transferred, Koi Security (BusinessCombinationConsiderationTransferred1)",
  "expected_direction": "none",
  "horizon": "event dated 2026-02-16, reported as a subsequent event in the quarter ended 2026-01-31",
  "quote": "\"value\": \"300000000\"",
  "paragraph_id": "0001327567-26-000005:facts:BusinessCombinationConsiderationTransferred1:2026-02-16..2026-02-16:us-gaap:BusinessAcquisitionAxis=panw:KoiSecurityLtdMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "earnings_quality_fact_interest_income_prior_quarter",
  "what_changed": "Other interest income for 2025-11-01..2026-01-31 is printed as 109000000, against 87000000 for 2024-11-01..2025-01-31. For the six months the filing prints 214000000 against 173000000.",
  "account": "interest income, other (InterestIncomeOther)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-01-31 against three months ended 2025-01-31",
  "quote": "\"value\": \"109000000\"",
  "paragraph_id": "0001327567-26-000005:facts:InterestIncomeOther:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_fact_foreign_currency_loss_prior_quarter",
  "what_changed": "Foreign currency transaction gain (loss) before tax for 2025-11-01..2026-01-31 is printed as -16000000, against 2000000 for 2024-11-01..2025-01-31. For the six months the filing prints -27000000 against -6000000.",
  "account": "foreign currency transaction gain (loss) before tax (ForeignCurrencyTransactionGainLossBeforeTax)",
  "expected_direction": "down",
  "horizon": "three months ended 2026-01-31 against three months ended 2025-01-31",
  "quote": "\"value\": \"-16000000\"",
  "paragraph_id": "0001327567-26-000005:facts:ForeignCurrencyTransactionGainLossBeforeTax:2025-11-01..2026-01-31" }
```

```json
{ "id": "earnings_quality_fact_other_nonoperating_income_prior_quarter",
  "what_changed": "Other nonoperating income (expense) for 2025-11-01..2026-01-31 is printed as 59000000, against -4000000 for 2024-11-01..2025-01-31. For the six months the filing prints 68000000 against 1000000.",
  "account": "other nonoperating income (expense) (OtherNonoperatingIncomeExpense)",
  "expected_direction": "up",
  "horizon": "three months ended 2026-01-31 against three months ended 2025-01-31",
  "quote": "\"value\": \"59000000\"",
  "paragraph_id": "0001327567-26-000005:facts:OtherNonoperatingIncomeExpense:2025-11-01..2026-01-31" }
```

## Seen in the notes

No items.

- **Why there are none.** The instructions say each fact is marked with whether its element sat inside a note. No fact I read in `input_numbers.json` carries such a marker; the fields present are listed at the top of this report. Without the marker I cannot place any fact here without judging it myself, which I was told not to do.
- **Where the facts went.** Every numeric-fact item above is under "Seen in the statements" only because no marker says otherwise. That is a default, not a judgment that each fact came from a face statement.
- **Dimensional facts, for the later split.** These items carry a dimension (axis) in their `paragraph_id`:
  - `revenue_recognition_fact_product_revenue_latest_quarter`
  - `revenue_recognition_fact_service_revenue_latest_quarter`
  - `revenue_recognition_fact_subscription_revenue_latest_quarter`
  - `revenue_recognition_fact_support_revenue_latest_quarter`
  - `revenue_recognition_fact_americas_revenue_latest_quarter`
  - `revenue_recognition_fact_emea_revenue_latest_quarter`
  - `revenue_recognition_fact_asia_pacific_revenue_latest_quarter`
  - `earnings_quality_fact_service_cost_of_revenue_latest_quarter`
  - `earnings_quality_fact_product_cost_of_revenue_latest_quarter`
  - `liquidity_and_capital_fact_convertible_notes_face_amount`
  - `related_parties_contingencies_and_subsequent_events_fact_cyberark_cash_payment`
  - `related_parties_contingencies_and_subsequent_events_fact_cyberark_shares_issued`
  - `related_parties_contingencies_and_subsequent_events_fact_koi_security_consideration`

  Whether any of them sat inside a note is not recorded in my input.
