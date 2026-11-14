# Numbers report: Littelfuse, quarterly report for the second quarter of fiscal 2026 (quarter ended June 27, 2026)

## What I read, and what my input does not hold

- **The trend table** I read in full: eight quarters and five years requested. The record behind it is the companyfacts record. Its newest row was filed May 6, 2026, which is before this run's cutoff of July 29, 2026. So every filled trend cell runs only through the first quarter of fiscal 2026.
- **The earnings release** filed with the current report on July 29, 2026 I read in full.
- **My prior flags** I read in full. There are none on record for this company, so I carry nothing forward.
- **The numeric-facts file** is 104,321 lines, three and a half megabytes, and it does not fit in what I can read. It holds only a list of three documents and their facts: the annual report for the year ended December 27, 2025, the quarterly report for the first quarter of fiscal 2026, and the quarterly report for this quarter. I read the document list and the opening facts of the annual report. From the current quarterly report I read the balance sheet, income statement and comprehensive income facts, and the cash flow facts up to dividends paid. I also read samples through the rest of the file, including its last facts. I report no fact I did not read.
- **No articulation checks, restatement traces or fourth-quarter derivation are in my input**, in any file. So I report no articulation gap and no traced restatement. That is not because none exist: nothing in front of me computes them.
- **No change of tag.** No trend cell says that a period rests on a different concept, and every period's inputs use the same concepts.
- **Nothing that should not be here.** Nothing in my directory is a price, an abnormal return, short interest, another company's file, a prior probability or an outcome window.

**Periods the record does not reach (no cells, so no items):**

- **The quarter ended June 27, 2026, the quarter this report covers.** The reason the table gives: no quarter ending within 20 days of June 27, 2026 is in the companyfacts record. The record's newest row was filed May 6, 2026, before this run's cutoff of July 29, 2026. The record was fetched before the triggering report, so the periods that report is the first to state are not in it. No trend ratio exists for this quarter. The quarterly report's own face-statement facts for the quarter are itemized below as facts, without ratios.
- **The fourth quarters ended December 27, 2025 and December 28, 2024.** The reason the table gives: no quarter ending within 20 days of those dates is in the record. The commonest cause is a fiscal fourth quarter, which no filing reports as a duration: the annual report states the year and the three quarterly reports state the first three quarters. The fourth quarter is derived in a separate step, and that derivation is not in my input. As a result, no quarter-over-quarter change exists for the first quarter of fiscal 2026.

**In my input but not quotable, so not itemized:**

- **The research-and-development capitalisation block.** The trend table carries one for each year, with a five-year life, but the block prints no paragraph id. For fiscal 2025 it prints earnings with research and development capitalised of -49657400.0 and book value with research and development capitalised of 2732037600.0. Its capitalised development cost is missing: the record tags no capitalised software additions in any period.
- **The release file's lists of current reports and late-filing notifications.** These also print no paragraph id. They show a notification of late filing for the annual report for the year ended December 28, 2024, filed February 27, 2025. They also show a current report of August 16, 2023 carrying only the item for a change in the registrant's certifying accountant.

**How to read the fields:**

- **`expected_direction`** is the direction the account moved, or is expected to move, over the stated horizon, as my input prints it. For a trend cell it is the sign of the printed year-over-year change. For a fact it is the printed value against its printed comparative. For guidance it is the direction management states. It is `none` where my input gives no direction.
- **Quarterly and annual ratios are not comparable.** The quarterly receivables and inventory ratios divide by three months of revenue or cost, and the annual ones by a full year, as each cell's formula prints.

## Seen in the statements

**Trend table, fiscal 2025 (the year ended December 27, 2025) against fiscal 2024 (the year ended December 28, 2024)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend",
  "what_changed": "Accruals over total assets for fiscal 2025 is -0.12774578219347169, a year-over-year change of -0.059028879203862045 against fiscal 2024. It is the lowest of the five filled years. The cell's inputs are net income of -71700000.0 (a loss), operating cash flow of 433764000.0 and total assets of 3956796000.0: operating cash flow is positive while net income is a loss.",
  "account": "accruals over total assets",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_net_loss_annual_trend_input",
  "what_changed": "The net income input inside the fiscal 2025 accruals cell is -71700000.0, taken from the annual report: the year closed at a net loss. The fiscal 2024 cell's net income input is 100190000.0. The release's covenant table for the twelve months ended June 27, 2026 also prints a net loss and a large impairment add-back (see the release item on impairment charges). My numeric input does not say what drove the fiscal 2025 loss.",
  "account": "net income (loss)",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"value\": -71700000.0",
  "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
  "what_changed": "The allowance for doubtful accounts over gross receivables for fiscal 2025 is 0.17505133003852025, a year-over-year change of -0.01703838318545267. It is the lowest of the five filled years. Inputs at December 27, 2025: allowance 77073000.0 against net receivables 363215000.0. The fiscal 2024 cell's inputs are 69990000.0 and 294371000.0. The allowance is higher in dollars than a year earlier while the ratio is lower.",
  "account": "allowance for doubtful accounts against trade receivables",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:bad_debt_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
  "what_changed": "Contract liabilities over revenue for fiscal 2025 is 0.004699756190980659, a year-over-year change of 0.003989046522042642. It is the highest of the five filled years. Inputs: deferred revenue of 11215000.0 at December 27, 2025, which the record took from the quarterly report for the first quarter of fiscal 2026, against fiscal 2025 revenue of 2386294000.0. The fiscal 2024 cell's deferred revenue is 1557000.0. The balance is small against revenue but the highest in the record's five years.",
  "account": "contract liabilities (deferred revenue) over revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:contract_liabilities_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend",
  "what_changed": "Days sales of inventory for fiscal 2025 is 102.41223143912755, a year-over-year change of -5.569926816206944. It is the lowest of the five filled years. Inputs: net inventory of 416472000.0 at December 27, 2025 and cost of revenue of 1480251000.0, over 364 days.",
  "account": "days sales of inventory",
  "expected_direction": "down",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:days_sales_of_inventory:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend",
  "what_changed": "Days sales outstanding for fiscal 2025 is 55.404011408485296, a year-over-year change of 6.493746149909313. It is the highest of the five filled years. Inputs: net receivables of 363215000.0 at December 27, 2025 against revenue of 2386294000.0, over 364 days. The fiscal 2024 cell's inputs are 294371000.0 and 2190768000.0.",
  "account": "days sales outstanding",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:days_sales_outstanding:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend",
  "what_changed": "Gross margin for fiscal 2025 is 0.37968624151089514, a year-over-year change of 0.020204087307437724. It is the third highest of the five filled years. Fiscal 2024's cell, 0.3594821542034574, is the lowest of the five. Inputs: revenue 2386294000.0, cost of revenue 1480251000.0.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:gross_margin:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend",
  "what_changed": "Inventory reserves over net inventory for fiscal 2025 is 0.19856076759061833, a year-over-year change of 0.038749778167811666. It is the highest of the five filled years. Inputs at December 27, 2025: reserves of 82695000.0 against net inventory of 416472000.0. The fiscal 2024 cell's inputs are 66525000.0 against 416273000.0. Every year-over-year change the table prints for this metric, fiscal 2022 through fiscal 2025, is positive.",
  "account": "inventory valuation reserves over net inventory",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:inventory_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend",
  "what_changed": "insufficient. The table cannot fill the gap between adjusted and reported net income for fiscal 2025, for the reason its cell gives: the record holds standard-taxonomy facts only, so no adjusted measure is in it for any period. The release prints adjusted figures for the quarter, but no gap is computed anywhere in my input.",
  "account": "gap between adjusted (non-GAAP) and reported net income",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-050481:trends:non_gaap_gap:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend",
  "what_changed": "Year-end receivables over annual revenue for fiscal 2025 is 0.15220882255078377, a year-over-year change of 0.017839961950300298. It is the highest of the five filled years. Inputs: net receivables 363215000.0 against revenue 2386294000.0, the same inputs as days sales outstanding.",
  "account": "trade receivables over revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:receivables_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend",
  "what_changed": "Soft-asset share for fiscal 2025 (total assets less net property, plant and equipment and cash, over total assets) is 0.7209785392019199, a year-over-year change of 0.02983266478304869. It is the third highest of the five filled years. Inputs at December 27, 2025: total assets 3956796000.0, property, plant and equipment 540640000.0, cash 563391000.0.",
  "account": "soft-asset share of total assets",
  "expected_direction": "up",
  "horizon": "fiscal 2025 against fiscal 2024",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-050481:trends:soft_asset_share:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend",
  "what_changed": "insufficient. No warranty reserve ratio exists for fiscal 2025, or for any period in the table, for the reason its cell gives: the record tags none of the product-warranty accrual concepts in any period. So either the company does not tag one or it states one only by segment, and the record cannot say which.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-050481:trends:warranty_reserve_ratio:2024-12-29..2025-12-27" }
```

**Trend table, the first quarter of fiscal 2026 (the quarter ended March 28, 2026, the newest quarter the table fills) against the first quarter of fiscal 2025.** For every metric here, the quarter-over-quarter change does not exist, because the fourth quarter of fiscal 2025 is not filled.

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_trend",
  "what_changed": "Accruals over total assets for the first quarter of fiscal 2026 is -0.0013249338764412966, a year-over-year change of 0.0043812541497453925. It is the highest of only two filled quarters, which is insufficient for any trend claim. Inputs: net income 75147000.0, operating cash flow 80258000.0, total assets 3857551000.0.",
  "account": "accruals over total assets",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cash_flow_gap_trend",
  "what_changed": "insufficient. The table cannot fill accruals for the second quarter of fiscal 2025, nor for the third quarters of fiscal 2025 and fiscal 2024, because operating cash flow is in the record but not for those three-month periods. The quarter this report covers is also a second quarter. The quarterly report states operating cash flow only for the six months ended June 27, 2026 (226474000), and the release prints $146 million for the quarter. No three-month accruals figure exists in my input.",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "every second and third quarter the table holds, and the second quarter of fiscal 2026",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2025-03-30..2025-06-28: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2025-03-30..2025-06-28" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
  "what_changed": "The allowance for doubtful accounts over gross receivables for the first quarter of fiscal 2026 is 0.173363219553052, a year-over-year change of -0.005528562854355407. It is the third highest of the five filled quarters. Inputs at March 28, 2026: allowance 79896000.0, net receivables 380963000.0.",
  "account": "allowance for doubtful accounts against trade receivables",
  "expected_direction": "down",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"third highest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:bad_debt_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
  "what_changed": "Contract liabilities over quarterly revenue for the first quarter of fiscal 2026 is 0.010218138146548771, a year-over-year change of 0.005572697984328197. It is the highest of the five filled quarters. Inputs: deferred revenue of 6713000.0 at March 28, 2026 against quarterly revenue of 656969000.0. The year-end balance in the fiscal 2025 cell is 11215000.0, so the printed balance at March 28, 2026 is below the year-end balance.",
  "account": "contract liabilities (deferred revenue) over revenue",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:contract_liabilities_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
  "what_changed": "Days sales of inventory for the first quarter of fiscal 2026 is 94.63756020058587, a year-over-year change of -14.730463519270884. It is the second lowest of the five filled quarters. Inputs: net inventory 418922000.0 at March 28, 2026 and quarterly cost of revenue 402820000.0, over 91 days.",
  "account": "days sales of inventory",
  "expected_direction": "down",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:days_sales_of_inventory:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
  "what_changed": "Days sales outstanding for the first quarter of fiscal 2026 is 52.769054552041275, a year-over-year change of 0.5915644608102397. It is the second lowest of the five filled quarters. Inputs: net receivables 380963000.0 at March 28, 2026 against quarterly revenue 656969000.0, over 91 days. The highest filled quarter is the third quarter of fiscal 2025, at 54.46058049436475.",
  "account": "days sales outstanding",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:days_sales_outstanding:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend",
  "what_changed": "Gross margin for the first quarter of fiscal 2026 is 0.3868508255336249, a year-over-year change of 0.012949720189474434. It is the highest of the five filled quarters. Inputs: revenue 656969000.0, cost of revenue 402820000.0. Gross margin for the second quarter of fiscal 2026 does not exist in my input.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:gross_margin:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend",
  "what_changed": "Inventory reserves over net inventory for the first quarter of fiscal 2026 is 0.19954311303774927, a year-over-year change of 0.02631450229025825. It is the second highest of the five filled quarters. The highest is the third quarter of fiscal 2025, at 0.21459617860715446. Inputs at March 28, 2026: reserves 83593000.0 against net inventory 418922000.0.",
  "account": "inventory valuation reserves over net inventory",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:inventory_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend",
  "what_changed": "insufficient. The table cannot fill the gap between adjusted and reported net income for the first quarter of fiscal 2026, for the reason its cell gives: no adjusted measure is in the record.",
  "account": "gap between adjusted (non-GAAP) and reported net income",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2026",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-050481:trends:non_gaap_gap:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
  "what_changed": "Receivables over quarterly revenue for the first quarter of fiscal 2026 is 0.5798797203521019, a year-over-year change of 0.006500708360552054. It is the second lowest of the five filled quarters. This ratio divides by three months of revenue, so it is not comparable with the annual 0.15220882255078377.",
  "account": "trade receivables over revenue",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:receivables_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend",
  "what_changed": "Soft-asset share for the first quarter of fiscal 2026 is 0.7368213667168626, a year-over-year change of 0.02719039019409586. It is the highest of the five filled quarters. Inputs at March 28, 2026: total assets 3857551000.0, property, plant and equipment 533528000.0, cash 481697000.0.",
  "account": "soft-asset share of total assets",
  "expected_direction": "up",
  "horizon": "the first quarter of fiscal 2026 against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"",
  "paragraph_id": "0001628280-26-050481:trends:soft_asset_share:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend",
  "what_changed": "insufficient. No warranty reserve ratio exists for the first quarter of fiscal 2026, for the same reason as every other period: the record tags no product-warranty accrual concept in any period.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2026",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-050481:trends:warranty_reserve_ratio:2025-12-28..2026-03-28" }
```

**Filed history**

```json
{ "id": "articulation_and_the_filed_history_year_end_balances_refiled_unchanged",
  "what_changed": "The annual report's fact for trade receivables at December 27, 2025 (363215000) is marked as superseded by the current quarterly report. That report's own December 27, 2025 fact prints the same 363215000. So do the other December 27, 2025 balance-sheet lines I read in both reports: cash 563391000, allowance 77073000, inventories 416472000, total assets 3956796000, accrued liabilities 199271000, long-term debt 706394000. The superseded mark names a later filing; it does not say the value changed, and no restatement trace in my input says one did. For the lines read, there is no restated prior value. Lines I did not read are not covered.",
  "account": "year-end balance sheet as first filed and as refiled",
  "expected_direction": "none",
  "horizon": "the balance sheet at December 27, 2025, in the annual report and in the quarterly report for the second quarter of fiscal 2026",
  "quote": "\"value\": \"363215000\"",
  "paragraph_id": "0001628280-26-009585:facts:AccountsReceivableNetCurrent:2025-12-27" }
```

**Numeric facts, the current quarterly report (quarter ended June 27, 2026).** No trend ratio exists for this quarter, so these items print values and their printed comparatives only.

```json
{ "id": "revenue_recognition_net_sales_quarterly_fact",
  "what_changed": "Net sales for the second quarter of fiscal 2026 are 738781000, against 613413000 for the second quarter of fiscal 2025. Six-month net sales are 1395750000 against 1167720000. The trend table's first-quarter revenue input is 656969000.0.",
  "account": "net sales",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"738781000\"",
  "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_gross_profit_quarterly_fact",
  "what_changed": "Gross profit for the second quarter of fiscal 2026 is 306064000, against 232054000 a year earlier. Cost of sales is 432717000 against 381359000. A gross margin for this quarter does not exist in my input.",
  "account": "gross profit",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"306064000\"",
  "paragraph_id": "0001628280-26-050481:facts:GrossProfit:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_net_income_quarterly_fact",
  "what_changed": "Net income for the second quarter of fiscal 2026 is 89405000, against 57342000 a year earlier. Six-month net income is 164552000 against 100913000. Diluted earnings per share for the quarter are 3.49 against 2.30.",
  "account": "net income",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"89405000\"",
  "paragraph_id": "0001628280-26-050481:facts:NetIncomeLoss:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_trade_receivables_balance_fact",
  "what_changed": "Net trade receivables at June 27, 2026 are 423590000. The comparatives are 363215000 at December 27, 2025 and 380963000 at March 28, 2026, the latter the trend table's input. The cash flow statement's six-month increase in receivables is 65720000, against 52635000 a year earlier. No days sales outstanding exists for this quarter in my input.",
  "account": "trade receivables, net",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"423590000\"",
  "paragraph_id": "0001628280-26-050481:facts:AccountsReceivableNetCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_receivables_allowance_balance_fact",
  "what_changed": "The allowance against trade receivables at June 27, 2026 is 86865000, against 77073000 at December 27, 2025 and 79896000 at March 28, 2026. No reserve ratio exists for this quarter in my input.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"86865000\"",
  "paragraph_id": "0001628280-26-050481:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-27" }
```

```json
{ "id": "earnings_quality_inventory_balance_fact",
  "what_changed": "Net inventories at June 27, 2026 are 433755000, against 416472000 at December 27, 2025 and 418922000 at March 28, 2026. The cash flow statement's six-month inventory line is 21254000, an increase in inventories; the same line a year earlier is -23316000, a decrease. No days sales of inventory and no inventory reserve ratio exist for this quarter in my input.",
  "account": "inventories, net",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"433755000\"",
  "paragraph_id": "0001628280-26-050481:facts:InventoryNet:2026-06-27" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_fact",
  "what_changed": "Operating cash flow for the six months ended June 27, 2026 is 226474000, against 148225000 a year earlier. Six-month net income is 164552000 against 100913000. The quarterly report gives no three-month operating cash flow; the release prints $146 million for the quarter.",
  "account": "net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "the first half of fiscal 2026 against the first half of fiscal 2025",
  "quote": "\"value\": \"226474000\"",
  "paragraph_id": "0001628280-26-050481:facts:NetCashProvidedByUsedInOperatingActivities:2025-12-28..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liability_change_fact",
  "what_changed": "The cash flow statement's change in contract liabilities for the six months ended June 27, 2026 is -4308000, a decrease, against 2844000, an increase, a year earlier. This follows a fiscal 2025 contract-liability ratio that is the highest of the five filled years. I did not read a contract-liability balance at June 27, 2026.",
  "account": "contract liabilities with customers",
  "expected_direction": "down",
  "horizon": "the first half of fiscal 2026",
  "quote": "\"value\": \"-4308000\"",
  "paragraph_id": "0001628280-26-050481:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-12-28..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_restructuring_and_impairment_charges_fact",
  "what_changed": "Restructuring, impairment and other charges for the second quarter of fiscal 2026 are 20021000, against 2506000 a year earlier. The six-month figures are 27443000 against 11525000. The release excludes these charges from its adjusted results.",
  "account": "restructuring, impairment and other charges",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"20021000\"",
  "paragraph_id": "0001628280-26-050481:facts:RestructuringSettlementAndImpairmentProvisions:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_asset_impairment_charges_fact",
  "what_changed": "Asset impairment charges in the cash flow statement for the six months ended June 27, 2026 are 13146000, against 136000 a year earlier.",
  "account": "asset impairment charges",
  "expected_direction": "up",
  "horizon": "the first half of fiscal 2026 against the first half of fiscal 2025",
  "quote": "\"value\": \"13146000\"",
  "paragraph_id": "0001628280-26-050481:facts:AssetImpairmentCharges:2025-12-28..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_intangible_assets_and_goodwill_fact",
  "what_changed": "Intangible assets, net, at June 27, 2026 are 553511000, against 594907000 at December 27, 2025. Goodwill is 1203861000 against 1211411000. Six-month amortization of intangibles is 31204000.",
  "account": "intangible assets and goodwill",
  "expected_direction": "down",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"553511000\"",
  "paragraph_id": "0001628280-26-050481:facts:IntangibleAssetsNetExcludingGoodwill:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_fact",
  "what_changed": "Long-term debt, less current portion, at June 27, 2026 is 529660000, against 706394000 at December 27, 2025. The current portion is 100000000 against 96233000. Six-month repayments are 100000000 of long-term lines of credit and 66250000 of unsecured debt; the release prints net payments of the credit facility of 166,250 thousand.",
  "account": "long-term debt",
  "expected_direction": "down",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"529660000\"",
  "paragraph_id": "0001628280-26-050481:facts:LongTermDebtNoncurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_debt_issuance_costs_fact",
  "what_changed": "Payments of debt issuance costs for the six months ended June 27, 2026 are 2169000, against 0 a year earlier. They sit alongside the credit agreement amendment the release describes in the first quarter of fiscal 2026.",
  "account": "payments of debt issuance costs",
  "expected_direction": "up",
  "horizon": "the first half of fiscal 2026 against the first half of fiscal 2025",
  "quote": "\"value\": \"2169000\"",
  "paragraph_id": "0001628280-26-050481:facts:PaymentsOfDebtIssuanceCosts:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_fact",
  "what_changed": "Cash and cash equivalents at June 27, 2026 are 628224000, against 563391000 at December 27, 2025 and 481697000 at March 28, 2026.",
  "account": "cash and cash equivalents",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"628224000\"",
  "paragraph_id": "0001628280-26-050481:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_fact",
  "what_changed": "Payments for repurchase of common stock for the six months ended June 27, 2026 are 0, against 27553000 a year earlier.",
  "account": "share repurchases",
  "expected_direction": "down",
  "horizon": "the first half of fiscal 2026 against the first half of fiscal 2025",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001628280-26-050481:facts:PaymentsForRepurchaseOfCommonStock:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_paid_in_capital_and_share_count_fact",
  "what_changed": "Additional paid-in capital at June 27, 2026 is 1199321000, against 1098150000 at December 27, 2025. Shares issued are 27511066 against 27014490. Diluted weighted shares for the quarter are 25620000 against 24905000 a year earlier. Six-month share-based compensation is 14953000 against 13447000. The release's condensed cash flow prints other cash provided by financing activities of 72,179 thousand for the six months.",
  "account": "additional paid-in capital and shares outstanding",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"1199321000\"",
  "paragraph_id": "0001628280-26-050481:facts:AdditionalPaidInCapital:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_fact",
  "what_changed": "Accounts payable at June 27, 2026 are 248972000, against 211079000 at December 27, 2025. The cash flow statement's six-month change in payables is 39159000, against -7001000 a year earlier.",
  "account": "accounts payable",
  "expected_direction": "up",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"248972000\"",
  "paragraph_id": "0001628280-26-050481:facts:AccountsPayableCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_interest_expense_fact",
  "what_changed": "Interest expense for the second quarter of fiscal 2026 is 5739000, against 8568000 a year earlier. The six-month figures are 12716000 against 17443000.",
  "account": "interest expense",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"5739000\"",
  "paragraph_id": "0001628280-26-050481:facts:InterestExpenseNonoperating:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_foreign_exchange_result_fact",
  "what_changed": "The foreign currency transaction result for the second quarter of fiscal 2026 is 160000, a gain, against -10448000, a loss, a year earlier. The six-month figures are 2573000 against -15291000. The release removes non-operating foreign exchange from its adjusted results.",
  "account": "foreign exchange gain (loss)",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"160000\"",
  "paragraph_id": "0001628280-26-050481:facts:ForeignCurrencyTransactionGainLossBeforeTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_deferred_tax_expense_fact",
  "what_changed": "Deferred income tax expense in the cash flow statement for the six months ended June 27, 2026 is 10026000, against -807000, a benefit, a year earlier.",
  "account": "deferred income tax expense",
  "expected_direction": "up",
  "horizon": "the first half of fiscal 2026 against the first half of fiscal 2025",
  "quote": "\"value\": \"10026000\"",
  "paragraph_id": "0001628280-26-050481:facts:DeferredIncomeTaxExpenseBenefit:2025-12-28..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_income_tax_expense_fact",
  "what_changed": "Income tax expense for the second quarter of fiscal 2026 is 27659000 on pre-tax income of 117064000. A year earlier it was 20872000 on 78214000. The release's tax reconciliation prints effective rates of 23.6% and 26.7%.",
  "account": "income tax expense",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"27659000\"",
  "paragraph_id": "0001628280-26-050481:facts:IncomeTaxExpenseBenefit:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_accrued_liabilities_fact",
  "what_changed": "Accrued liabilities at June 27, 2026 are 191873000, against 199271000 at December 27, 2025. Accrued income taxes are 32667000 against 26186000.",
  "account": "accrued liabilities",
  "expected_direction": "down",
  "horizon": "June 27, 2026 against December 27, 2025",
  "quote": "\"value\": \"191873000\"",
  "paragraph_id": "0001628280-26-050481:facts:AccruedLiabilitiesCurrent:2026-06-27" }
```

```json
{ "id": "earnings_quality_comprehensive_income_fact",
  "what_changed": "Comprehensive income for the second quarter of fiscal 2026 is 83699000, against 155255000 a year earlier, while net income rose from 57342000 to 89405000. The quarter's foreign currency translation adjustment in other comprehensive income is -6798000, against 91899000. Accumulated other comprehensive loss is -30263000 at June 27, 2026, against -5383000 at December 27, 2025.",
  "account": "comprehensive income",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"83699000\"",
  "paragraph_id": "0001628280-26-050481:facts:ComprehensiveIncomeNetOfTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_selling_general_administrative_expense_fact",
  "what_changed": "Selling, general and administrative expenses for the second quarter of fiscal 2026 are 120578000, against 95517000 a year earlier. The six-month figures are 219903000 against 183225000.",
  "account": "selling, general and administrative expenses",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"120578000\"",
  "paragraph_id": "0001628280-26-050481:facts:SellingGeneralAndAdministrativeExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_research_and_development_expense_fact",
  "what_changed": "Research and development expenses for the second quarter of fiscal 2026 are 31037000, against 26401000 a year earlier. The six-month figures are 60774000 against 52449000. The fiscal 2025 figure in the trend table is 106899000.0.",
  "account": "research and development expenses",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "\"value\": \"31037000\"",
  "paragraph_id": "0001628280-26-050481:facts:ResearchAndDevelopmentExpense:2026-03-29..2026-06-27" }
```

**Figures in the earnings release**

```json
{ "id": "results_against_expectations_net_sales_growth_release",
  "what_changed": "The release reports second-quarter fiscal 2026 net sales of $739 million, up 20%, with organic growth contributing 14%. Its reconciliation attributes 6% of total growth to acquisitions. This agrees with the quarterly report's fact of 738781000 against 613413000.",
  "account": "net sales",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "Net sales of $739 million, +20%; organic growth contributed +14%",
  "paragraph_id": "0001628280-26-050382:8k_2_02:8" }
```

```json
{ "id": "results_against_expectations_management_says_results_beat_own_expectations_release",
  "what_changed": "The chief executive says second-quarter results exceeded the company's own expectations. My input holds no earlier outlook figure for this quarter, so the result against that outlook does not exist in my input.",
  "account": "results against the company's own outlook",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "with performance exceeding our expectations",
  "paragraph_id": "0001628280-26-050382:8k_2_02:15" }
```

```json
{ "id": "results_against_expectations_revenue_growth_outlook_release",
  "what_changed": "For the third quarter of fiscal 2026, management expects total revenue growth of about 26% against the prior year. It cites record bookings, customer momentum and the Basler acquisition. Revenue for the third quarter of fiscal 2025 in the trend table is 624640000.0.",
  "account": "net sales",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026 against the third quarter of fiscal 2025",
  "quote": "we expect approximately 26% total revenue growth versus the prior year, supported by record bookings",
  "paragraph_id": "0001628280-26-050382:8k_2_02:16" }
```

```json
{ "id": "results_against_expectations_net_sales_range_outlook_release",
  "what_changed": "The outlook for the third quarter of fiscal 2026 is net sales of $780 to $800 million, adjusted diluted earnings per share of $4.85 to $5.05, and an adjusted effective tax rate of about 23% to 24%. Guidance is given on an adjusted basis only; the release says it cannot give the reported-basis equivalent without unreasonable effort.",
  "account": "net sales and adjusted earnings outlook",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "Net sales in the range of $780",
  "paragraph_id": "0001628280-26-050382:8k_2_02:19" }
```

```json
{ "id": "earnings_quality_free_cash_flow_release",
  "what_changed": "The release reports second-quarter operating cash flow of $146 million and free cash flow of $127 million, up 75%. This three-month figure appears only in the release; the quarterly report's fact covers six months (226474000 against 148225000).",
  "account": "operating cash flow and free cash flow",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "Cash flow from operations of $146 million; free cash flow of $127 million, +75%",
  "paragraph_id": "0001628280-26-050382:8k_2_02:9" }
```

```json
{ "id": "earnings_quality_adjusted_versus_reported_earnings_release",
  "what_changed": "Reported diluted earnings per share are $3.49 against adjusted diluted earnings per share of $4.19 for the second quarter of fiscal 2026. The release's reconciliation prints a per-share effect of adjustments of 0.70, against 0.55 a year earlier. The trend table's gap between adjusted and reported earnings is insufficient, so the release is the only source of this gap in my input.",
  "account": "adjusted against reported earnings per share",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "GAAP diluted earnings per share of $3.49; Adjusted diluted earnings per share of $4.19",
  "paragraph_id": "0001628280-26-050382:8k_2_02:11" }
```

```json
{ "id": "earnings_quality_operating_margin_release",
  "what_changed": "The release reports operating margin of 16.2%, up 110 basis points, and adjusted EBITDA margin of 23.6%, up 220 basis points, for the second quarter of fiscal 2026.",
  "account": "operating margin",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "GAAP operating margin of 16.2%, +110 bps",
  "paragraph_id": "0001628280-26-050382:8k_2_02:12" }
```

```json
{ "id": "earnings_quality_trailing_impairment_charges_release",
  "what_changed": "The release's covenant table for the twelve months ended June 27, 2026 prints a net loss of $(8.2) million. It adds back impairment charges of 315.1 million as a non-cash item in consolidated EBITDA as the credit agreement defines it, which it prints at 623.9 million. On a reported basis the trailing twelve months are loss-making; on the covenant basis they are not.",
  "account": "impairment charges in covenant EBITDA",
  "expected_direction": "none",
  "horizon": "the twelve months ended June 27, 2026",
  "quote": "Impairment charges |  | 315.1",
  "paragraph_id": "0001628280-26-050382:8k_2_02:82" }
```

```json
{ "id": "liquidity_and_capital_credit_agreement_amendment_release",
  "what_changed": "The credit agreement was amended in the first quarter of fiscal 2026 to let restructuring charges and business optimization expenses be added back in the covenant calculation. The quarterly report's six-month payments of debt issuance costs (2169000, against 0 a year earlier) sit alongside this amendment.",
  "account": "credit agreement covenant definition",
  "expected_direction": "none",
  "horizon": "from the first quarter of fiscal 2026",
  "quote": "now allows to add restructuring charges and business optimization expenses in addition to the prior credit agreement",
  "paragraph_id": "0001628280-26-050382:8k_2_02:84" }
```

```json
{ "id": "liquidity_and_capital_leverage_covenant_release",
  "what_changed": "The credit agreement and the private placement notes, maturing 2027 to 2031, trigger an event of default if consolidated net leverage over four quarters exceeds 3.50 to 1.00 at any quarter-end. The release's table prints the ratio at 0.8 times for the twelve months ended June 27, 2026, and net debt of $493.8 million.",
  "account": "consolidated net leverage covenant",
  "expected_direction": "none",
  "horizon": "each fiscal quarter-end",
  "quote": "the Consolidated Net Leverage ratio at such time for the then most recently concluded period of four consecutive fiscal quarters of the Company exceeds 3.50:1.00",
  "paragraph_id": "0001628280-26-050382:8k_2_02:83" }
```

```json
{ "id": "liquidity_and_capital_dividend_increase_release",
  "what_changed": "The quarterly dividend is raised to $0.80 per share from $0.75, a 7% increase, payable September 3, 2026. Six-month dividends paid in the quarterly report are 37872000.",
  "account": "cash dividend per share",
  "expected_direction": "up",
  "horizon": "the dividend payable September 3, 2026",
  "quote": "a 7% increase from the prior quarter dividend of $0.75 per share",
  "paragraph_id": "0001628280-26-050382:8k_2_02:33" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_margin_release",
  "what_changed": "Transportation segment adjusted EBITDA margin fell to 18.6% from 20.5%, down 190 basis points, on lower commercial vehicle profitability. Segment operating income is 25,691 thousand against 28,074 thousand, which the release prints as a decline of 8.5%.",
  "account": "transportation segment margin",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "Adjusted EBITDA margin for the second quarter 2026 decreased to 18.6%",
  "paragraph_id": "0001628280-26-050382:8k_2_02:28" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_passenger_vehicle_release",
  "what_changed": "Passenger vehicle sales were hit by lower global passenger car builds and declining auto sensor products. The release's reconciliation prints auto sensor product organic sales down 12% for the quarter.",
  "account": "passenger vehicle and auto sensor sales",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "Passenger vehicle sales were impacted by lower global passenger car builds and auto sensor product declines.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:27" }
```

```json
{ "id": "structure_and_disclosure_changes_basler_acquisition_contribution_release",
  "what_changed": "Industrial segment net sales rose 52%: the Basler acquisition contributed 36% and organic growth 16%. Part of the industrial segment's year-over-year growth is therefore acquired rather than organic.",
  "account": "industrial segment net sales",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "The Basler acquisition contributed +36% to growth.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:30" }
```

```json
{ "id": "estimates_and_discretion_indemnification_receivable_reversal_release",
  "what_changed": "The release's six-month adjustments include the reversal, in other income, of a $2.7 million indemnification receivable. It is tied to lapsed statutes of limitations on previously unrecognized tax benefits, and a matching $2.7 million of tax benefits was recognized in the first quarter of fiscal 2026.",
  "account": "indemnification receivable and unrecognized tax benefits",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2026",
  "quote": "the reversal of an indemnification receivable of $2.7 million related to lapses in the statute of limitations",
  "paragraph_id": "0001628280-26-050382:8k_2_02:90" }
```

```json
{ "id": "earnings_quality_electronics_segment_margin_release",
  "what_changed": "Electronics segment adjusted EBITDA margin rose to 26.3%, up 470 basis points, on volume leverage, mix and execution. Segment operating income is 86,916 thousand against 49,861 thousand.",
  "account": "electronics segment margin",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2026 against the second quarter of fiscal 2025",
  "quote": "Adjusted EBITDA margin for the second quarter 2026 increased to 26.3%",
  "paragraph_id": "0001628280-26-050382:8k_2_02:25" }
```

## Seen in the notes

No fact in my input carries a mark saying whether its element sat inside a note. The field appears on no fact I read, including facts whose members name related-party counterparties, product lines, debt instruments and restructuring types, all of which carry no mark either way. With no mark, I place nothing in this section. I have also kept every such dimensional fact out of the section above, so that no finding's source has to be worked out again later. The trend cells above are reported as statement findings, as instructed, even where an input such as inventory reserves or deferred revenue may have come from a note table; the input does not say.

Nothing in this section.
