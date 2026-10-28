# Numbers report — Dell Technologies, quarterly report for the second quarter of fiscal 2027

## What I read, and what is not here

- **Read, in full:**
  - the earnings release attached to the current report filed September 1, 2026 (second quarter of fiscal 2027, the three months ended July 31, 2026);
  - the trend table;
  - the numeric facts of the annual report for fiscal 2026 (filed March 16, 2026), of the quarterly report for the first quarter of fiscal 2027 (filed June 9, 2026) and of the quarterly report for the second quarter of fiscal 2027 (filed September 8, 2026);
  - my prior flags.
- **Prior flags:** none on record. This company has no earlier run, so nothing carries forward.
- **Out-of-bounds data:** nothing in my directory is an abnormal return, short interest, another company's file, a prior probability or an outcome window.
  - One fact touches the rule on prices. The annual report's stock-award note carries a fact under the tag SharePrice: the company's own class C share price at January 30, 2026, which the note uses to value unvested awards. The same note also prints per-share award values, such as grant-date fair values and an option exercise price.
  - These figures are part of the filing and dated before it. They are not market data and not an outcome window, so I did not treat the run as broken.
  - I do not quote or use any of them. I flag them here so the run's owner can decide whether the extraction should drop them.
- **Arithmetic:** every number below is copied as my input prints it. I computed none. Where a number does not exist in my input, I say so.

How to read two of the fields:
- **`expected_direction`** is the direction the named account or ratio moved in the comparison the item reports.
  - For a quarter, I take the change against the same quarter a year earlier, because that comparison is seasonally matched. The table prints both changes, and both are in `what_changed`.
  - For a year, I take the change against the year before.
  - For a balance, I take the change against the latest earlier balance the item names.
  - It is `none` where the cell is insufficient, where the printed change is nil, or where my input holds only one point.
- **`horizon`** names the periods the item's comparison spans.

Not in my input, stated once here and not as items:
- **Articulation checks:** my input holds none, so I have no articulation gap to report.
- **Restatement traces:** my input holds none, so I report no restated prior value.
  - Facts that a later filing reported again carry a `superseded_by` field naming the quarterly report filed September 8, 2026.
  - That field says the fact was reported again. It does not say the value changed.
  - Two items below cover the filed history: the year-end balances the trend table uses, and one year-end balance printed at two precisions.
- **Change of tag:** none in the trend table. In every period the table holds, each metric's inputs rest on the same concept: revenues, cost of revenue, accounts receivable net, inventory net, allowance for doubtful accounts, current contract liabilities, standard product warranty accrual, assets, cash and cash equivalents, property plant and equipment net, net income and operating cash flow. Outside the table, one fact is placed on a differently named axis in the two quarterly reports: severance charged to research and development. An item below covers it.
- **Fourth-quarter derivation:** not in my input.
- **A period the record does not reach:** the fourth quarter of fiscal 2026, the quarter ending January 30, 2026, has no cells in the trend table.
  - The reason the period gives: no quarter ending within twenty days of January 30, 2026 is in the record.
  - The commonest cause is a fiscal fourth quarter, which no filing reports as a duration. The annual report states the year, and the three quarterly reports state the first three quarters.
  - The quarter is left to a separate fourth-quarter derivation, which my input does not hold.
  - As a result, the first quarter of fiscal 2027 has no quarter-over-quarter change in any metric.
- **The research-and-development-capitalized baseline:** the trend table prints it for each of the five years, but it carries no paragraph_id. I cannot quote it, so I write no item from it. Its capitalized-development-cost input is missing in every year, because the record tags no capitalized computer software additions concept.
- **Quarterly cash flow:** the quarterly report for the second quarter of fiscal 2027 states its cash flow statement only for the six months to July 31, 2026, against the six months to August 1, 2025. My input holds no three-month cash flow fact for the second quarter. The three-month figures for that quarter exist only in the earnings release. The quarterly report for the first quarter states its own three months.
- **Annual-report figures without their own item:** a few annual-report figures below sit in the `what_changed` text of a related item rather than in their own item, because I did not keep the row they print on and so cannot quote it. They are capitalized costs to fulfil contracts, the single-customer share of revenue, the financing receivable history, the annual tax rate, contract liabilities, purchase obligations, total debt, goodwill at earlier year ends, annual equity-security gains and capitalized software.

## Seen in the statements

### Trend table: the second quarter of fiscal 2027 (May 2, 2026 to July 31, 2026)

```json
{ "id": "earnings_quality_accruals_against_assets_quarterly_cell_insufficient",
  "what_changed": "insufficient. The accruals ratio (net income less operating cash flow, over total assets) has no value for the second quarter of fiscal 2027: the record holds operating cash flow, but not for this three-month period. No change against the first quarter of fiscal 2027 or against the second quarter of fiscal 2026 exists, and no position in history. The earnings release prints the quarter's operating cash flow (see the release items below), but the table did not compute the ratio and I do not.",
  "account": "net income against operating cash flow (accruals), over total assets",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2027",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-05-02..2026-07-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001571996-26-000046:trends:accruals_over_total_assets:2026-05-02..2026-07-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_quarterly_ratio",
  "what_changed": "The bad debt reserve ratio (allowance for doubtful accounts over receivables plus allowance) is 0.002437538086532602 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: -0.0005318807557796882. Change against the second quarter of fiscal 2026: -0.0030569674079728927. It sits lowest of the 7 filled quarters. Inputs as printed: allowance 56000000.0 and accounts receivable, net 22918000000.0 at July 31, 2026. The comparison cells print an allowance of 77000000.0 at May 1, 2026 and 83000000.0 at August 1, 2025.",
  "account": "allowance for doubtful accounts against accounts receivable, net",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"lowest of the 7 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:bad_debt_reserve_ratio:2026-05-02..2026-07-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_against_revenue_quarterly",
  "what_changed": "Current contract liabilities over the quarter's revenue is 0.3142577334951353 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: 0.013336242687234212. Change against the second quarter of fiscal 2026: -0.14782582373216185. It sits second lowest of the 7 filled quarters. Inputs as printed: current contract liabilities 14761000000.0 at July 31, 2026 and revenue 46971000000.0 for the quarter. The year-earlier cell prints 13759000000.0 and 29776000000.0.",
  "account": "current contract liabilities (short-term deferred revenue) against revenue",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"second lowest of the 7 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:contract_liabilities_over_revenue:2026-05-02..2026-07-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "Days sales of inventory is 52.16310815540777 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: 14.178305049473217. Change against the second quarter of fiscal 2026: 25.191140544737376. It sits highest of the 6 filled quarters. The history holds six quarters, not seven, because the cost-of-revenue row is absent for the fourth quarter of fiscal 2025. Inputs as printed: inventory, net 21290000000.0 at July 31, 2026 and cost of revenue 37141000000.0 for the quarter. The comparison cells print inventory of 15052000000.0 at May 1, 2026 and 7211000000.0 at August 1, 2025.",
  "account": "inventory, net against cost of revenue",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:days_sales_of_inventory:2026-05-02..2026-07-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "Days sales outstanding is 44.400545017138235 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: -9.262928364550561. Change against the second quarter of fiscal 2026: -1.5120355846887463. It sits third highest of the 7 filled quarters. The first quarter of fiscal 2027 sits highest, at 53.663473381688796. Inputs as printed: accounts receivable, net 22918000000.0 at July 31, 2026 and revenue 46971000000.0 for the quarter.",
  "account": "accounts receivable, net against revenue",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"third highest of the 7 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:days_sales_outstanding:2026-05-02..2026-07-31" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "Gross margin is 0.20927806518915926 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: 0.03177703877613067. Change against the second quarter of fiscal 2026: 0.026345502051061453. It sits third highest of the 6 filled quarters. The first quarter of fiscal 2027 sits lowest of the 6, at 0.1775010264130286. Inputs as printed: revenue 46971000000.0 and cost of revenue 37141000000.0.",
  "account": "gross margin (revenue less cost of revenue, over revenue)",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:gross_margin:2026-05-02..2026-07-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_quarterly_cell_insufficient",
  "what_changed": "insufficient. The inventory reserve ratio has no value for the second quarter of fiscal 2027, and none in any period of the table: the record tags no inventory valuation reserve concept in any period. The cell says the record cannot tell whether the company does not tag the reserve or states it only by segment. No change and no position exist.",
  "account": "inventory valuation reserve against inventory",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2027",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001571996-26-000046:trends:inventory_reserve_ratio:2026-05-02..2026-07-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell_insufficient",
  "what_changed": "insufficient. The gap between non-GAAP and GAAP net income has no value for the second quarter of fiscal 2027, and none in any period of the table: the record carries no non-GAAP measure. The earnings release prints both net income figures (see the release item below). The gap itself does not exist in my input, and I do not compute it.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2027",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001571996-26-000046:trends:non_gaap_gap:2026-05-02..2026-07-31" }
```

```json
{ "id": "revenue_recognition_receivables_against_revenue_quarterly",
  "what_changed": "Receivables over the quarter's revenue is 0.48791807711140917 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: -0.10179042158846768. Change against the second quarter of fiscal 2026: -0.016615775655920262. It sits third highest of the 7 filled quarters. The first quarter of fiscal 2027 sits highest, at 0.5897084986998768. Inputs as printed: accounts receivable, net 22918000000.0 and revenue 46971000000.0. The first-quarter cell prints receivables of 25854000000.0.",
  "account": "accounts receivable, net against revenue",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"third highest of the 7 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:receivables_over_revenue:2026-05-02..2026-07-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "Soft asset share (total assets less property, plant and equipment and cash, over total assets) is 0.8509651236724153 at July 31, 2026. Change against May 1, 2026: 0.01215663377135967. Change against August 1, 2025: 0.014719945597596928. It sits third highest of the 7 filled quarters. Inputs as printed: assets 127393000000.0, property, plant and equipment, net 7417000000.0, and cash and cash equivalents 11569000000.0.",
  "account": "total assets other than property, plant and equipment and cash",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"third highest of the 7 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:soft_asset_share:2026-05-02..2026-07-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_quarterly",
  "what_changed": "The standard product warranty accrual over the quarter's revenue is 0.025696706478465437 for the second quarter of fiscal 2027. Change against the first quarter of fiscal 2027: 0.002089206820603113. Change against the second quarter of fiscal 2026: 0.010953288961001707. It sits highest of the 7 filled quarters, and the first quarter of fiscal 2027 sits second highest. Inputs as printed: warranty accrual 1207000000.0 at July 31, 2026 and revenue 46971000000.0. The comparison cells print an accrual of 1035000000.0 at May 1, 2026 and 439000000.0 at August 1, 2025.",
  "account": "standard product warranty accrual against revenue",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the first quarter of fiscal 2027 and the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"highest of the 7 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:warranty_reserve_ratio:2026-05-02..2026-07-31" }
```

### Trend table: fiscal 2026 (February 1, 2025 to January 30, 2026)

```json
{ "id": "earnings_quality_accruals_against_assets_annual",
  "what_changed": "The accruals ratio (net income less operating cash flow, over total assets) is -0.0518235491578303 for fiscal 2026. Change against fiscal 2025: -0.052713875945380774. It sits second lowest of the 5 filled years. Fiscal 2025 sits highest, at 0.0008903267875504727. Inputs as printed: net income 5936000000.0, operating cash flow 11185000000.0, and assets 101286000000.0 at January 30, 2026. The operating cash flow input is above the net income input for fiscal 2026.",
  "account": "net income against operating cash flow (accruals), over total assets",
  "expected_direction": "down",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:accruals_over_total_assets:2025-02-01..2026-01-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_annual_ratio",
  "what_changed": "The bad debt reserve ratio is 0.004359642169629713 at the end of fiscal 2026. Change against fiscal 2025: -0.0017208519911655765. It sits lowest of the 5 filled years. Inputs as printed: allowance 77000000.0 and accounts receivable, net 17585000000.0 at January 30, 2026, both taken from the quarterly report filed September 8, 2026. The fiscal 2025 cell prints an allowance of 63000000.0 and receivables of 10298000000.0.",
  "account": "allowance for doubtful accounts against accounts receivable, net",
  "expected_direction": "down",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:bad_debt_reserve_ratio:2025-02-01..2026-01-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_against_revenue_annual",
  "what_changed": "Current contract liabilities over the year's revenue is 0.11744085680565097 for fiscal 2026. Change against fiscal 2025: -0.02563154266278478. It sits lowest of the 5 filled years. Inputs as printed: current contract liabilities 13334000000.0 at January 30, 2026 and revenue 113538000000.0. The fiscal 2025 cell prints 13673000000.0 and 95567000000.0.",
  "account": "current contract liabilities (short-term deferred revenue) against revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:contract_liabilities_over_revenue:2025-02-01..2026-01-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "Days sales of inventory is 41.82567625590382 for fiscal 2026. Change against fiscal 2025: 8.931129920610417. It sits highest of the 5 filled years. Inputs as printed: inventory, net 10437000000.0 at January 30, 2026 and cost of revenue 90831000000.0. The fiscal 2025 cell prints inventory of 6716000000.0 and cost of revenue of 74317000000.0.",
  "account": "inventory, net against cost of revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:days_sales_of_inventory:2025-02-01..2026-01-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "Days sales outstanding is 56.37707199351759 for fiscal 2026. Change against fiscal 2025: 17.153574342654842. It sits highest of the 5 filled years. Inputs as printed: accounts receivable, net 17585000000.0 at January 30, 2026 and revenue 113538000000.0.",
  "account": "accounts receivable, net against revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:days_sales_outstanding:2025-02-01..2026-01-30" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "Gross margin is 0.19999471542567246 for fiscal 2026. Change against fiscal 2025: -0.02236237436473637. It sits lowest of the 5 filled years. Inputs as printed: revenue 113538000000.0 and cost of revenue 90831000000.0.",
  "account": "gross margin (revenue less cost of revenue, over revenue)",
  "expected_direction": "down",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:gross_margin:2025-02-01..2026-01-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_annual_cell_insufficient",
  "what_changed": "insufficient. The inventory reserve ratio has no value for fiscal 2026, and none in any of the five years: the record tags no inventory valuation reserve concept in any period. No change and no position exist.",
  "account": "inventory valuation reserve against inventory",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001571996-26-000046:trends:inventory_reserve_ratio:2025-02-01..2026-01-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell_insufficient",
  "what_changed": "insufficient. The gap between non-GAAP and GAAP net income has no value for fiscal 2026, and none in any of the five years: the record carries no non-GAAP measure. No change and no position exist.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001571996-26-000046:trends:non_gaap_gap:2025-02-01..2026-01-30" }
```

```json
{ "id": "revenue_recognition_receivables_against_revenue_annual",
  "what_changed": "Receivables over the year's revenue is 0.1548820659162571 for fiscal 2026. Change against fiscal 2025: 0.047125204238062754. It sits highest of the 5 filled years. Inputs as printed: accounts receivable, net 17585000000.0 at January 30, 2026 and revenue 113538000000.0.",
  "account": "accounts receivable, net against revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:receivables_over_revenue:2025-02-01..2026-01-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "Soft asset share is 0.8202713109412949 at January 30, 2026. Change against January 31, 2025: -0.05471928419827321. It sits lowest of the 5 filled years. Inputs as printed: assets 101286000000.0, property, plant and equipment, net 6676000000.0, and cash and cash equivalents 11528000000.0. The fiscal 2025 cell prints cash of 3633000000.0.",
  "account": "total assets other than property, plant and equipment and cash",
  "expected_direction": "down",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:soft_asset_share:2025-02-01..2026-01-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_annual",
  "what_changed": "The standard product warranty accrual over the year's revenue is 0.003963430745653438 for fiscal 2026. Change against fiscal 2025: -0.00047324718710577834. It sits lowest of the 5 filled years. Inputs as printed: warranty accrual 450000000.0 at January 30, 2026 and revenue 113538000000.0. The annual ratio sets a year-end accrual against a full year of revenue, so it is not on the scale of the quarterly cells.",
  "account": "standard product warranty accrual against revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026, against fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001571996-26-000046:trends:warranty_reserve_ratio:2025-02-01..2026-01-30" }
```

### Trend table: cells that show how far the history reaches

```json
{ "id": "earnings_quality_accruals_quarterly_history_too_short",
  "what_changed": "insufficient for a quarterly trend. The accruals ratio fills only 2 of the quarters the table holds: the first quarter of fiscal 2027 at -0.005595537493582102 and the first quarter of fiscal 2026 at -0.021077714719865543. The change printed between them is 0.015482177226283441. For the second quarter of fiscal 2027, the third and second quarters of fiscal 2026, and the fourth and third quarters of fiscal 2025, the cells give the same reason: operating cash flow is in the record, but not for that period. Two points do not support a trend claim.",
  "account": "net income against operating cash flow (accruals), over total assets",
  "expected_direction": "none",
  "horizon": "the quarters from the third quarter of fiscal 2025 to the second quarter of fiscal 2027",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"",
  "paragraph_id": "0001571996-26-000046:trends:accruals_over_total_assets:2026-01-31..2026-05-01" }
```

```json
{ "id": "earnings_quality_gross_margin_cell_without_cost_of_revenue_row",
  "what_changed": "insufficient. Gross margin has no value for the fourth quarter of fiscal 2025 (November 2, 2024 to January 31, 2025). Revenue for that quarter is in the record, since the receivables cell for the quarter is filled with revenue of 23931000000.0, but cost of revenue is not. That is why the quarterly gross margin history holds 6 filled quarters, not 7.",
  "account": "gross margin (revenue less cost of revenue, over revenue)",
  "expected_direction": "none",
  "horizon": "the fourth quarter of fiscal 2025",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2024-11-02..2025-01-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001571996-26-000046:trends:gross_margin:2024-11-02..2025-01-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_cell_without_cost_of_revenue_row",
  "what_changed": "insufficient. Days sales of inventory has no value for the fourth quarter of fiscal 2025 (November 2, 2024 to January 31, 2025), because cost of revenue is not in the record for that quarter. That is why the quarterly inventory-days history holds 6 filled quarters, not 7.",
  "account": "inventory, net against cost of revenue",
  "expected_direction": "none",
  "horizon": "the fourth quarter of fiscal 2025",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2024-11-02..2025-01-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001571996-26-000046:trends:days_sales_of_inventory:2024-11-02..2025-01-31" }
```

### The filed history of the year-end balances

```json
{ "id": "articulation_and_the_filed_history_year_end_balances_reported_again",
  "what_changed": "The annual report's balance facts at January 30, 2026 carry a superseded_by field naming the quarterly report filed September 8, 2026. For the balances the trend table uses at that date, the annual report prints the same figures the table takes from the later report: inventory 10437000000, accounts receivable, net 17585000000, allowance for doubtful accounts 77000000, current contract liabilities 13334000000, assets 101286000000, cash and cash equivalents 11528000000, and property, plant and equipment, net 6676000000. The quarterly report for the first quarter of fiscal 2027 prints the same inventory (10437000000), cash (11528000000) and property, plant and equipment (6676000000) at that date. No trace in my input says any of these was reported differently, and I see no difference between the printings.",
  "account": "year-end balance sheet at January 30, 2026",
  "expected_direction": "none",
  "horizon": "the annual report for fiscal 2026 against the quarterly reports for the first and second quarters of fiscal 2027",
  "quote": "\"superseded_by\": \"0001571996-26-000046\"",
  "paragraph_id": "0001571996-26-000008:facts:InventoryNet:2026-01-30" }
```

```json
{ "id": "articulation_and_the_filed_history_supplier_finance_year_end_two_printings",
  "what_changed": "The annual report states supplier finance program obligations of 1983000000 at January 30, 2026, to the nearest million. The quarterly report for the second quarter of fiscal 2027 prints the same date as 2000000000.0, to the nearest hundred million. The two printings differ in precision. No restatement trace in my input says the value changed, so I report a difference of rounding between the filings, not a restated value. The annual report also states 1368000000 at January 31, 2025, with additions of 6052000000 and settlements of 5437000000 in fiscal 2026.",
  "account": "supplier finance program obligations",
  "expected_direction": "none",
  "horizon": "January 30, 2026, as printed in the annual report for fiscal 2026 and in the quarterly report for the second quarter of fiscal 2027",
  "quote": "\"value\": \"1983000000\"",
  "paragraph_id": "0001571996-26-000008:facts:SupplierFinanceProgramObligation:2026-01-30" }
```

### Earnings release figures the trend table does not hold

```json
{ "id": "across_documents_release_operating_cash_flow_for_the_quarter",
  "what_changed": "The earnings release prints operating cash flow ('Change in cash from operating activities') of 2,225 million for the second quarter of fiscal 2027, against 2,543 million a year earlier, with a printed change of (13)%. For the six months it is 6,306 million against 5,339 million, printed change 18%. This is the three-month figure the trend table lacks for the quarter, which is why its accruals cell is insufficient. Net income on the same table is 4,133 million against 1,164 million. The quarterly report states only the six-month figures, 6306000000 against 5339000000, which match the release's six-month figures. The quarterly report for the first quarter of fiscal 2027 states 4081000000 for its own three months (see the first-quarter item below).",
  "account": "operating cash flow",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026",
  "quote": "| Change in cash from operating activities | $ | 2,225 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:35" }
```

```json
{ "id": "earnings_quality_release_reconciling_adjustments_negative",
  "what_changed": "The release's cash flow statement prints adjustments to reconcile net income to operating cash flow of (1,908) million for the second quarter of fiscal 2027, against 1,379 million a year earlier. For the six months they are (1,265) million against 3,210 million. With a negative adjustment, operating cash flow (2,225 million) is printed below net income (4,133 million) for the quarter. The release's adjusted free cash flow table puts 6,667 million of the quarter's operating cash flow impact on the change in financing receivables (see the item below).",
  "account": "operating cash flow against net income",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "| Adjustments to reconcile net income to net cash provided by operating activities | (1,908) |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:74" }
```

```json
{ "id": "across_documents_release_non_gaap_net_income",
  "what_changed": "The release prints non-GAAP net income of 4,591 million for the second quarter of fiscal 2027, against GAAP net income of 4,133 million. A year earlier the figures were 1,591 million and 1,164 million. For the six months they are 7,781 million against 7,571 million (a year earlier, 2,677 million against 2,129 million). The trend table's non-GAAP gap cell is insufficient because the record holds no non-GAAP measure. The gap is not printed, and I do not compute it.",
  "account": "non-GAAP net income",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "| Non-GAAP net income | $ | 4,591 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:35" }
```

```json
{ "id": "earnings_quality_release_equity_investment_gains_removed_from_non_gaap",
  "what_changed": "In the release's bridge from net income to non-GAAP net income, fair value adjustments on equity investments are (73) million for the second quarter of fiscal 2027, against (4) million a year earlier. For the six months they are (704) million against (21) million. These are amounts the non-GAAP measure removes from GAAP net income. On the income statement, interest and other, net is (254) million for the quarter and 38 million for the six months, against (333) million and (415) million a year earlier. The quarterly report for the first quarter of fiscal 2027 states unrealized gains on equity securities at fair value of 631000000 for its three months. The quarterly report for the second quarter states 632000000 for the six months and 1000000 for the second quarter (see the numeric-fact items below).",
  "account": "fair value adjustments on equity investments, within interest and other, net",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "| Fair value adjustments on equity investments | (73) |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:103" }
```

```json
{ "id": "liquidity_and_capital_release_free_cash_flow_down",
  "what_changed": "The release prints free cash flow (operating cash flow less capital expenditures and capitalized software development costs, net) of 986 million for the second quarter of fiscal 2027, against 1,868 million a year earlier, with a printed change of (47)%. For the six months it is 4,104 million against 4,096 million. Capital expenditures and capitalized software development costs are (1,239) million in the quarter, against (675) million. The quarterly report states capital expenditures of 2202000000 for the six months, against 1243000000. The annual report states capitalized software, net of 526000000 at January 30, 2026, against 623000000 a year earlier.",
  "account": "free cash flow",
  "expected_direction": "down",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026",
  "quote": "| Free cash flow | $ | 986 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:116" }
```

```json
{ "id": "liquidity_and_capital_release_financing_receivables_added_back",
  "what_changed": "The release's adjusted free cash flow of 8,149 million for the second quarter of fiscal 2027 (2,518 million a year earlier) adds two items to free cash flow of 986 million: 6,667 million for financing receivables (592 million a year earlier) and 496 million for equipment under operating leases (58 million a year earlier). Footnote (b) says financing receivables represent the operating cash flow impact from the change in financing receivables. On the balance sheet, short-term financing receivables are 12,805 million at July 31, 2026, against 8,458 million at January 30, 2026; long-term financing receivables are 7,625 million against 5,822 million. The quarterly report's cash flow statement states the change in financing receivables at 6404000000 for the six months, against 569000000.",
  "account": "financing receivables",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026; balances at July 31, 2026 against January 30, 2026",
  "quote": "| Financing receivables (b) | 6,667 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:116" }
```

```json
{ "id": "estimates_and_discretion_release_financing_receivable_allowance",
  "what_changed": "The release's balance sheet prints the allowance on short-term financing receivables at 186 million at July 31, 2026, against 121 million at January 30, 2026, and on long-term financing receivables at 128 million against 92 million. The allowance on trade accounts receivable is 56 million against 77 million. The trend table's bad debt ratio covers only the trade receivable allowance.",
  "account": "allowance for financing receivables",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against January 30, 2026",
  "quote": "| Short-term financing receivables, net of allowance of $186 and $121 | 12,805 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:69" }
```

```json
{ "id": "liquidity_and_capital_release_inventories_balance",
  "what_changed": "The release's balance sheet prints inventories of 21,290 million at July 31, 2026, against 10,437 million at January 30, 2026. These are the same inventory figures the trend table uses. The quarterly report for the first quarter of fiscal 2027 states inventory of 15052000000 at May 1, 2026.",
  "account": "inventories",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against January 30, 2026",
  "quote": "| Inventories | 21,290 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:69" }
```

```json
{ "id": "liquidity_and_capital_release_accounts_payable_balance",
  "what_changed": "The release's balance sheet prints accounts payable of 49,723 million at July 31, 2026, against 33,630 million at January 30, 2026. Total current liabilities are 83,703 million against 63,269 million, and total current assets are 80,547 million against 57,602 million.",
  "account": "accounts payable",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against January 30, 2026",
  "quote": "| Accounts payable | 49,723 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:69" }
```

```json
{ "id": "liquidity_and_capital_release_share_repurchases_and_debt_proceeds",
  "what_changed": "The release's cash flow statement prints repurchases of common stock of (3,796) million in the second quarter of fiscal 2027, against (940) million a year earlier. Proceeds from debt are 4,386 million against 962 million, and repayments of debt are (1,017) million against (1,114) million. Short-term debt is 8,481 million and long-term debt 25,985 million at July 31, 2026, against 7,990 million and 23,513 million at January 30, 2026. The annual report states a total debt figure of 31763000000 at January 30, 2026, against 24788000000 at January 31, 2025. The quarterly report for the first quarter of fiscal 2027 states a total debt carrying amount of 31413000000 at May 1, 2026. The quarterly report for the second quarter states treasury stock acquired at cost of 3861000000 in the quarter (931000000 a year earlier) and 5477000000 for the six months; its cash flow statement states repurchases of 5424000000 for the six months, against 2920000000. The first-quarter report states class C shares repurchased at a cost of 1600000000 in its three months, against 2000000000.0 a year earlier. These are different lines and I do not reconcile them.",
  "account": "share repurchases and debt",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026; balances at July 31, 2026 against January 30, 2026",
  "quote": "| Repurchases of common stock | (3,796) |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:74" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised",
  "what_changed": "The release raises full-year fiscal 2027 revenue guidance from 167.0 billion to 192.0 billion, with a printed change of 69% year over year. AI-optimized servers revenue guidance goes from 60.0 billion to 74.0 billion. GAAP diluted earnings per share guidance goes from 17.31 to 24.37, and non-GAAP from 17.90 to 25.50. Guidance for the third quarter of fiscal 2027 is revenue of 49.0 billion, GAAP diluted earnings per share of 6.10, and non-GAAP diluted earnings per share of 6.50. These are the company's own expectations. No outside expectation is in my input.",
  "account": "revenue guidance",
  "expected_direction": "up",
  "horizon": "full-year fiscal 2027 and the third quarter of fiscal 2027",
  "quote": "raising our full-year FY27 revenue outlook by $25 billion to $192 billion",
  "paragraph_id": "0001571996-26-000039:8k_2_02:13" }
```

```json
{ "id": "revenue_recognition_release_services_revenue_flat",
  "what_changed": "The release prints services revenue of 5,859 million for the second quarter of fiscal 2027, against 5,841 million a year earlier, with a printed change of —%. For the six months it is 11,596 million against 11,620 million. Products revenue is 41,112 million against 23,935 million, printed change 72%. Services cost of revenue is 3,151 million against 3,285 million.",
  "account": "services revenue",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026",
  "quote": "| Services | 5,859 |",
  "paragraph_id": "0001571996-26-000039:8k_2_02:63" }
```

### Numeric facts: quarterly reports for the first and second quarters of fiscal 2027

None of the facts below carries a note marker in my input (see "Seen in the notes").

```json
{ "id": "estimates_and_discretion_warranty_accrual_balance_fact",
  "what_changed": "The quarterly report filed September 8, 2026 states the standard product warranty accrual at 1207000000 at July 31, 2026. The same report states 1035000000 at May 1, 2026, 450000000 at January 30, 2026, and 439000000 at August 1, 2025. Warranty payments in the second quarter are 211000000, against 225000000 a year earlier. The quarterly report for the first quarter of fiscal 2027 states the same 450000000 at January 30, 2026 and 1035000000 at May 1, 2026, against 424000000 at January 31, 2025 and 415000000 at May 2, 2025; its warranty payments are 234000000 in the first quarter, against 220000000. This accrual is the input behind the warranty ratio's place at the top of its quarterly history.",
  "account": "standard product warranty accrual",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against May 1, 2026, January 30, 2026 and August 1, 2025",
  "quote": "\"value\": \"1207000000\"",
  "paragraph_id": "0001571996-26-000046:facts:StandardProductWarrantyAccrual:2026-07-31" }
```

```json
{ "id": "liquidity_and_capital_supplier_finance_obligation_fact",
  "what_changed": "The quarterly report states supplier finance program obligations of 3100000000 at July 31, 2026, against 2000000000.0 at January 30, 2026. The quarterly report for the first quarter of fiscal 2027 already stated 3100000000 at May 1, 2026. All of these are stated to the nearest hundred million. The annual report states the January 30, 2026 balance as 1983000000 and the January 31, 2025 balance as 1368000000 (see the filed-history item above). Accounts payable rose from 33630000000 to 49723000000 over the same six months (see the payables item below).",
  "account": "supplier finance program obligations",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against May 1, 2026 and January 30, 2026",
  "quote": "\"value\": \"3100000000\"",
  "paragraph_id": "0001571996-26-000046:facts:SupplierFinanceProgramObligation:2026-07-31" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_fact",
  "what_changed": "The quarterly report states the restructuring reserve at 339000000 at July 31, 2026, against 242000000 at May 1, 2026, 136000000 at January 30, 2026, and 211000000 at August 1, 2025. Restructuring costs are 261000000 in the second quarter of fiscal 2027, against 204000000 a year earlier, and 488000000 for the six months against 334000000. Payments are 164000000 in the quarter, against 144000000. The quarterly report for the first quarter of fiscal 2027 states restructuring costs of 227000000 in its three months, against 130000000 a year earlier, payments of 121000000 against 217000000, and a reserve of 242000000 at May 1, 2026 against 151000000 at May 2, 2025.",
  "account": "restructuring reserve",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against May 1, 2026, January 30, 2026 and August 1, 2025; the first and second quarters and first six months of fiscal 2027 against fiscal 2026",
  "quote": "\"value\": \"339000000\"",
  "paragraph_id": "0001571996-26-000046:facts:RestructuringReserve:2026-07-31" }
```

```json
{ "id": "earnings_quality_severance_in_research_and_development_fact",
  "what_changed": "The quarterly report states severance costs charged to research and development of 149000000 in the second quarter of fiscal 2027, against 28000000 a year earlier; for the six months, 189000000 against 61000000. Severance charged to selling, general and administrative is 87000000 against 128000000, and to cost of revenue 25000000 against 48000000. The quarterly report states research and development expense of 1109000000 for the quarter, against 785000000. The quarterly report for the first quarter of fiscal 2027 states severance charged to research and development of 40000000 in its three months, to selling, general and administrative 106000000 (67000000 a year earlier), and to cost of sales 81000000 (30000000 a year earlier).",
  "account": "severance costs by income statement line",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026",
  "quote": "\"value\": \"149000000\"",
  "paragraph_id": "0001571996-26-000046:facts:SeveranceCosts1:2026-05-02..2026-07-31:us-gaap:StatementOfIncomeLocationBalanceAxis=us-gaap:ResearchAndDevelopmentExpense" }
```

```json
{ "id": "structure_and_disclosure_changes_severance_line_placed_on_a_different_axis",
  "what_changed": "The two quarterly reports place severance charged to research and development on differently named dimensions. The quarterly report for the first quarter of fiscal 2027 states 40000000 for its three months under the axis us-gaap:IncomeStatementLocationAxis with the member us-gaap:ResearchAndDevelopmentExpenseMember. The quarterly report for the second quarter states 149000000 for its quarter under the axis us-gaap:StatementOfIncomeLocationBalanceAxis with the member us-gaap:ResearchAndDevelopmentExpense. The concept, SeveranceCosts1, is the same in both. My input holds no trace saying whether earlier periods were re-tagged, so I report only the difference visible in the two element names.",
  "account": "severance costs charged to research and development",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2027 against the second quarter of fiscal 2027",
  "quote": "\"value\": \"40000000\"",
  "paragraph_id": "0001571996-26-000030:facts:SeveranceCosts1:2026-01-31..2026-05-01:us-gaap:IncomeStatementLocationAxis=us-gaap:ResearchAndDevelopmentExpenseMember" }
```

```json
{ "id": "revenue_recognition_sales_type_lease_revenue_fact",
  "what_changed": "The quarterly report states sales-type lease revenue of 3711000000 for the second quarter of fiscal 2027, against 181000000 a year earlier; for the six months, 4245000000 against 300000000. Cost of goods sold on sales-type leases is 3244000000 in the quarter, against 178000000, and the selling profit on sales-type leases is 467000000, against 3000000. Lease income on sales-type leases is 81000000, against 92000000. The quarterly report for the first quarter of fiscal 2027 states sales-type lease revenue of 534000000 for its three months, against 119000000 a year earlier. The annual report states 886000000 for the whole of fiscal 2026 (see the annual item below).",
  "account": "sales-type lease revenue",
  "expected_direction": "up",
  "horizon": "the first and second quarters of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "\"value\": \"3711000000\"",
  "paragraph_id": "0001571996-26-000046:facts:SalesTypeLeaseRevenue:2026-05-02..2026-07-31" }
```

```json
{ "id": "liquidity_and_capital_financing_receivable_originations_fact",
  "what_changed": "The quarterly report states financing receivables originated (payments to acquire finance receivables) of 7500000000 in the second quarter of fiscal 2027, against 2400000000 a year earlier; for the six months, 10300000000 against 4000000000.0. All are stated to the nearest hundred million. Gross financing receivables are 20542000000 at July 31, 2026, against 14295000000 at January 30, 2026. The annual report states 11900000000 originated in the whole of fiscal 2026 (see the annual item below).",
  "account": "financing receivable originations",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "\"value\": \"7500000000\"",
  "paragraph_id": "0001571996-26-000046:facts:PaymentsToAcquireFinanceReceivables:2026-05-02..2026-07-31" }
```

```json
{ "id": "estimates_and_discretion_financing_receivable_credit_loss_provision_fact",
  "what_changed": "The quarterly report states a provision for credit losses on financing receivables of 122000000 in the second quarter of fiscal 2027, against 11000000 a year earlier; for the six months, 131000000 against 12000000. The allowance is 314000000 at July 31, 2026, against 212000000 at May 1, 2026, 213000000 at January 30, 2026 and 151000000 at August 1, 2025. Write-offs are 20000000 in the quarter, against 4000000. The annual report states a provision of 91000000 for the whole of fiscal 2026 (see the annual item below).",
  "account": "allowance for credit losses on financing receivables",
  "expected_direction": "up",
  "horizon": "the second quarter of fiscal 2027, against the second quarter of fiscal 2026; the allowance at July 31, 2026 against May 1, 2026, January 30, 2026 and August 1, 2025",
  "quote": "\"value\": \"122000000\"",
  "paragraph_id": "0001571996-26-000046:facts:ProvisionForLoanLossesExpensed:2026-05-02..2026-07-31:us-gaap:AccountsNotesLoansAndFinancingReceivableByReceivableTypeAxis=us-gaap:LoansAndFinanceReceivablesMember" }
```

```json
{ "id": "estimates_and_discretion_financing_receivables_lower_credit_score_mix_fact",
  "what_changed": "The quarterly report states gross financing receivables in the credit-score band below 660 at 4424000000 at July 31, 2026, against 1813000000 at January 30, 2026. The quarterly report for the first quarter of fiscal 2027 states 1883000000 in that band at May 1, 2026, and the annual report states 1339000000 at January 31, 2025. Of the 4424000000, 3048000000 was originated in the current fiscal year. The band from 660 to 719 holds 8623000000, against 6036000000, and the band above 720 holds 7495000000, against 6446000000. The three bands total 20542000000, against 14295000000. Receivables 31 to 90 days past due are 132000000, against 195000000, and those more than 90 days past due are 106000000, against 115000000.",
  "account": "financing receivables by customer credit score",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against May 1, 2026, January 30, 2026 and January 31, 2025",
  "quote": "\"value\": \"4424000000\"",
  "paragraph_id": "0001571996-26-000046:facts:NotesReceivableGross:2026-07-31:us-gaap:CreditScoreFicoAxis=dell:FICOScoreLessThan660Member" }
```

```json
{ "id": "liquidity_and_capital_inventory_build_in_cash_flow_fact",
  "what_changed": "The quarterly report's cash flow statement states the change in inventories at 10940000000 for the six months to July 31, 2026, against 615000000 for the six months to August 1, 2025. The quarterly report for the first quarter of fiscal 2027 states 4715000000 for its three months. By component, raw materials are 15894000000 at July 31, 2026, against 10634000000 at May 1, 2026 and 6696000000 at January 30, 2026; work in process is 4174000000, against 3483000000 and 2772000000; finished goods are 1222000000, against 935000000 and 969000000; total inventory is 21290000000, against 15052000000 and 10437000000.",
  "account": "inventories, by component",
  "expected_direction": "up",
  "horizon": "the six months to July 31, 2026, against the six months to August 1, 2025; balances at July 31, 2026 against May 1, 2026 and January 30, 2026",
  "quote": "\"value\": \"10940000000\"",
  "paragraph_id": "0001571996-26-000046:facts:IncreaseDecreaseInInventories:2026-01-31..2026-07-31" }
```

```json
{ "id": "liquidity_and_capital_payables_build_in_cash_flow_fact",
  "what_changed": "The quarterly report's cash flow statement states the change in accounts payable at 16203000000 for the six months to July 31, 2026, against 6615000000 a year earlier. The quarterly report for the first quarter of fiscal 2027 states 11661000000 for its three months. The change in contract liabilities is 3089000000, against -390000000. The change in accounts receivable is 5428000000, against 4574000000. Other non-cash items are 454000000, against -389000000. Purchase obligations stated at July 31, 2026 are 22400000000 for the rest of the fiscal year, 4900000000 in the next twelve months, 6100000000 in the second year and 800000000 in the third year. At May 1, 2026 the first-quarter report states 16900000000 for the rest of the fiscal year, 1200000000 in the next twelve months, 1400000000 in the second year and 800000000 in the third year. The annual report states purchase obligations of 16800000000 for the next twelve months at January 30, 2026.",
  "account": "accounts payable and other working capital",
  "expected_direction": "up",
  "horizon": "the six months to July 31, 2026, against the six months to August 1, 2025; purchase obligations at July 31, 2026 against May 1, 2026 and January 30, 2026",
  "quote": "\"value\": \"16203000000\"",
  "paragraph_id": "0001571996-26-000046:facts:IncreaseDecreaseInAccountsPayable:2026-01-31..2026-07-31" }
```

```json
{ "id": "across_documents_first_quarter_operating_cash_flow_fact",
  "what_changed": "The quarterly report for the first quarter of fiscal 2027 (filed June 9, 2026) states operating cash flow of 4081000000 for the three months to May 1, 2026. It is the one three-month operating cash flow of fiscal 2027 in the filed record. The trend table's accruals cell for that quarter is filled; the cell for the second quarter is not. For the second quarter, the release prints 2,225 million for the three months and 6,306 million for the six months, and the quarterly report prints 6306000000 for the six months. My input holds no three-month operating cash flow for the first quarter of fiscal 2026 from this report, so I state no comparison.",
  "account": "operating cash flow",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2027",
  "quote": "\"value\": \"4081000000\"",
  "paragraph_id": "0001571996-26-000030:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-31..2026-05-01" }
```

```json
{ "id": "earnings_quality_investment_gains_in_the_six_months_fact",
  "what_changed": "The quarterly report for the second quarter of fiscal 2027 states gain on investments of 700000000 for the six months to July 31, 2026, and 0 for the second quarter; the same periods of fiscal 2026 are 0 and 0. Unrealized gains on equity securities at fair value are 632000000 for the six months and 1000000 for the quarter, against -2000000 and -17000000 a year earlier. The quarterly report for the first quarter of fiscal 2027 states unrealized gains on equity securities at fair value of 631000000 for its three months. The annual report states unrealized gains on equity securities at fair value of 126000000 for fiscal 2026, against 121000000 for fiscal 2025 and 17000000 for fiscal 2024. Investments are 2700000000 at July 31, 2026, against 1700000000 at January 30, 2026, and the unrecognized holding gain on held-to-maturity securities is 1800000000, against 1100000000.",
  "account": "gains on investments, within interest and other, net",
  "expected_direction": "up",
  "horizon": "the six months to July 31, 2026 and the first and second quarters of fiscal 2027, against the same periods of fiscal 2026",
  "quote": "\"value\": \"700000000\"",
  "paragraph_id": "0001571996-26-000046:facts:GainLossOnInvestments:2026-01-31..2026-07-31" }
```

```json
{ "id": "earnings_quality_equity_securities_upward_revaluation_fact",
  "what_changed": "The quarterly report for the second quarter of fiscal 2027 states upward price adjustments of 600000000 for the six months to July 31, 2026 on equity securities without a readily determinable fair value. The quarterly report for the first quarter of fiscal 2027 states 600000000 under the same concept for its three months to May 1, 2026. Both are stated to the nearest hundred million. The quarterly report states no figure under this concept for the same six months of fiscal 2026, so no year-over-year comparison exists.",
  "account": "equity securities without readily determinable fair value",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2027 and the six months to July 31, 2026",
  "quote": "\"value\": \"600000000\"",
  "paragraph_id": "0001571996-26-000046:facts:EquitySecuritiesWithoutReadilyDeterminableFairValueUpwardPriceAdjustmentAnnualAmount:2026-01-31..2026-07-31" }
```

```json
{ "id": "revenue_recognition_ai_optimized_server_revenue_fact",
  "what_changed": "The quarterly report states revenue from AI-optimized servers and networking of 16401000000 in the second quarter of fiscal 2027, against 8208000000 a year earlier; for the six months, 32533000000 against 10090000000. In the same segment, traditional servers and networking is 10531000000 against 4736000000, and storage is 4850000000 against 3856000000. Infrastructure Solutions Group revenue is 31782000000 against 16800000000. Client Solutions Group revenue is 15034000000 against 12503000000, of which commercial is 13192000000 against 10781000000 and consumer is 1842000000 against 1722000000. The quarterly report for the first quarter of fiscal 2027 states AI-optimized servers and networking revenue of 16132000000 for its three months, against 1882000000 a year earlier; traditional servers and networking 8543000000 against 4439000000; storage 4334000000 against 3996000000; Infrastructure Solutions Group 29009000000 against 10317000000; and Client Solutions Group 14609000000 against 12509000000.",
  "account": "revenue by segment and product",
  "expected_direction": "up",
  "horizon": "the first and second quarters of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "\"value\": \"16401000000\"",
  "paragraph_id": "0001571996-26-000046:facts:Revenues:2026-05-02..2026-07-31:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,srt:ProductOrServiceAxis=dell:AIOptimizedServersAndNetworkingMember,us-gaap:StatementBusinessSegmentsAxis=dell:InfrastructureSolutionsGroupMember" }
```

```json
{ "id": "earnings_quality_infrastructure_segment_operating_income_fact",
  "what_changed": "The quarterly report states Infrastructure Solutions Group operating income of 4781000000 in the second quarter of fiscal 2027, against 1470000000 a year earlier; for the six months, 7836000000 against 2468000000. The segment's cost of revenue is 24269000000, against 13164000000; its selling, general and administrative expense is 2036000000, against 1604000000; and its research and development expense is 696000000, against 562000000. Client Solutions Group operating income is 1142000000, against 803000000. Total segment operating income is 5923000000, against 2273000000, and consolidated operating income is 5385000000, against 1773000000. The quarterly report for the first quarter of fiscal 2027 states Infrastructure Solutions Group operating income of 3055000000 for its three months, against 998000000, with segment cost of revenue of 23475000000 against 7050000000; Client Solutions Group operating income is 1170000000 against 653000000, and consolidated operating income 3656000000 against 1165000000.",
  "account": "segment operating income",
  "expected_direction": "up",
  "horizon": "the first and second quarters of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "\"value\": \"4781000000\"",
  "paragraph_id": "0001571996-26-000046:facts:OperatingIncomeLoss:2026-05-02..2026-07-31:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=dell:InfrastructureSolutionsGroupMember" }
```

```json
{ "id": "structure_and_disclosure_changes_corporate_non_segment_revenue_fact",
  "what_changed": "The quarterly report states revenue outside the two reportable segments (corporate, non-segment) of 155000000 in the second quarter of fiscal 2027, against 473000000 a year earlier; for the six months, 379000000 against 1025000000. Its operating income is 6000000, against 11000000. The quarterly report for the first quarter of fiscal 2027 states 224000000 for its three months, against 552000000. The same second-quarter report states that a business disposed of by sale (the member the filer names dell:SecureWorksCorp.Member) carried consideration of 900000000 at February 3, 2025, with a gain on disposal of 200000000 in the six months to August 1, 2025.",
  "account": "corporate and other revenue",
  "expected_direction": "down",
  "horizon": "the first and second quarters of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "\"value\": \"155000000\"",
  "paragraph_id": "0001571996-26-000046:facts:Revenues:2026-05-02..2026-07-31:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_fact",
  "what_changed": "The quarterly report for the second quarter of fiscal 2027 states remaining performance obligations of 132000000000 at July 31, 2026, stated to the nearest billion, of which 0.77 is expected to be recognized from August 1, 2026 and 0.14 from August 1, 2027. The quarterly report for the first quarter of fiscal 2027 states 97000000000 at May 1, 2026, of which 0.80 is expected from May 2, 2026 and 0.10 from May 2, 2027. The annual report states 82000000000 at January 30, 2026 (see the annual item below). The three points rise at each date. Total contract liabilities are 29718000000 at July 31, 2026, against 27452000000 at May 1, 2026, 26930000000 at January 30, 2026 and 26181000000 at August 1, 2025; the annual report states 25965000000 at January 31, 2025 and 29145000000 at February 2, 2024. Of the July 31, 2026 total, non-current contract liabilities are 14957000000, against 12422000000 at August 1, 2025. Revenue recognized in the second quarter from the opening contract liability balance is 5006000000, against 5111000000 a year earlier; in the first quarter it is 5018000000, against 5100000000; for the whole of fiscal 2026 the annual report states 20050000000, against 21179000000 for fiscal 2025. The annual report also states capitalized costs to fulfil contracts of 2700000000 at January 30, 2026, against 4800000000 a year earlier, with amortization of 6300000000 in fiscal 2026, 7600000000 in fiscal 2025 and 8000000000.0 in fiscal 2024. Three points of remaining performance obligations over six months are a short history.",
  "account": "remaining performance obligations and contract liabilities",
  "expected_direction": "up",
  "horizon": "July 31, 2026 against May 1, 2026 and January 30, 2026; contract liabilities against May 1, 2026, January 30, 2026, August 1, 2025 and the two earlier year ends",
  "quote": "\"value\": \"132000000000\"",
  "paragraph_id": "0001571996-26-000046:facts:RevenueRemainingPerformanceObligation:2026-07-31" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_fact",
  "what_changed": "The quarterly report states an effective tax rate of 0.195 for the second quarter of fiscal 2027, against 0.192 a year earlier; for the six months, 0.166 against 0.156. Income tax expense is 998000000 in the quarter, against 276000000. The quarterly report for the first quarter of fiscal 2027 states 0.129 for its three months, against 0.109. The annual report states an effective tax rate of 0.183 for fiscal 2026, against 0.094 for fiscal 2025 and 0.175 for fiscal 2024, with income tax expense of 1327000000, 472000000 and 715000000.",
  "account": "effective income tax rate",
  "expected_direction": "up",
  "horizon": "the first and second quarters of fiscal 2027 and the six months to July 31, 2026, against the same periods of fiscal 2026",
  "quote": "\"value\": \"0.195\"",
  "paragraph_id": "0001571996-26-000046:facts:EffectiveIncomeTaxRateContinuingOperations:2026-05-02..2026-07-31" }
```

```json
{ "id": "liquidity_and_capital_stockholders_deficit_fact",
  "what_changed": "The quarterly report states total stockholders' equity of -1427000000 at July 31, 2026, against -2470000000 at January 30, 2026, -1404000000 at May 1, 2026 and -2766000000 at August 1, 2025. Total liabilities are 128820000000, against total assets of 127393000000. Treasury stock is 20010000000, against 14533000000.",
  "account": "stockholders' equity (deficit)",
  "expected_direction": "down",
  "horizon": "July 31, 2026 against May 1, 2026",
  "quote": "\"value\": \"-1427000000\"",
  "paragraph_id": "0001571996-26-000046:facts:StockholdersEquity:2026-07-31" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_guarantee_exposure_fact",
  "what_changed": "The quarterly report states a maximum exposure under guarantees of 8600000000 at July 31, 2026, stated to the nearest hundred million. My input holds no earlier figure under this concept from this report, so no comparison exists.",
  "account": "guarantee obligations, maximum exposure",
  "expected_direction": "none",
  "horizon": "July 31, 2026",
  "quote": "\"value\": \"8600000000\"",
  "paragraph_id": "0001571996-26-000046:facts:GuaranteeObligationsMaximumExposure:2026-07-31" }
```

```json
{ "id": "estimates_and_discretion_goodwill_and_intangibles_balance_fact",
  "what_changed": "The quarterly report states goodwill of 19448000000 at July 31, 2026, against 19547000000 at January 30, 2026, and intangible assets, net of 4347000000, against 4533000000. The quarterly report for the first quarter of fiscal 2027 states goodwill of 19504000000 at May 1, 2026, with a foreign currency translation change of -43000000 in its three months, and intangible assets, net of 4439000000. The annual report states goodwill of 19120000000 at January 31, 2025 and 19700000000 at February 2, 2024, and amortization of intangible assets of 497000000 in fiscal 2026, against 667000000 in fiscal 2025 and 833000000 in fiscal 2024. Impairment of intangible assets is 0 in the first quarter, the second quarter and the six months of both years.",
  "account": "goodwill and intangible assets",
  "expected_direction": "down",
  "horizon": "July 31, 2026 against May 1, 2026 and January 30, 2026",
  "quote": "\"value\": \"19448000000\"",
  "paragraph_id": "0001571996-26-000046:facts:Goodwill:2026-07-31" }
```

### Numeric facts: the annual report for fiscal 2026

None of the facts below carries a note marker in my input either.

```json
{ "id": "revenue_recognition_remaining_performance_obligation_year_end_fact",
  "what_changed": "The annual report states remaining performance obligations of 82000000000 at January 30, 2026, of which 0.78 is expected to be recognized from January 31, 2026 and 0.11 from January 31, 2027. The quarterly reports state 97000000000 at May 1, 2026 and 132000000000 at July 31, 2026 (see the quarterly item above).",
  "account": "remaining performance obligations",
  "expected_direction": "up",
  "horizon": "January 30, 2026 against May 1, 2026 and July 31, 2026",
  "quote": "\"value\": \"82000000000\"",
  "paragraph_id": "0001571996-26-000008:facts:RevenueRemainingPerformanceObligation:2026-01-30" }
```

```json
{ "id": "liquidity_and_capital_receivables_from_contract_manufacturers",
  "what_changed": "The annual report states gross notes receivable from its three largest contract manufacturers (the member the filer names dell:ThreeLargestContractManufacturersMember) of 13200000000 at January 30, 2026, against 5400000000 a year earlier.",
  "account": "notes receivable from contract manufacturers",
  "expected_direction": "up",
  "horizon": "January 30, 2026 against January 31, 2025",
  "quote": "\"value\": \"13200000000\"",
  "paragraph_id": "0001571996-26-000008:facts:NotesReceivableGross:2026-01-30:srt:MajorCustomersAxis=dell:ThreeLargestContractManufacturersMember" }
```

```json
{ "id": "liquidity_and_capital_financing_receivable_originations_annual_history",
  "what_changed": "The annual report states financing receivables originated of 11900000000 in fiscal 2026, against 8400000000 in fiscal 2025 and 8400000000 in fiscal 2024. The provision for credit losses on financing receivables is 91000000 in fiscal 2026, against 54000000 and 92000000. Write-offs are 31000000, against 71000000 and 49000000. The allowance is 213000000 at January 30, 2026, against 153000000, 170000000 and 201000000 at the three earlier year ends. Receivables more than 90 days past due are 115000000, against 219000000 a year earlier. The credit-score band below 660 holds 1813000000, against 1339000000. The second quarter of fiscal 2027 alone states 7500000000 originated, and the six months state 10300000000 (see the quarterly item above).",
  "account": "financing receivable originations and credit losses",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"11900000000\"",
  "paragraph_id": "0001571996-26-000008:facts:PaymentsToAcquireFinanceReceivables:2025-02-01..2026-01-30" }
```

```json
{ "id": "revenue_recognition_sales_type_lease_revenue_annual_history",
  "what_changed": "The annual report states sales-type lease revenue of 886000000 in fiscal 2026, against 1992000000 in fiscal 2025 and 1140000000 in fiscal 2024. Selling profit on sales-type leases is 88000000, against 289000000 and 286000000. Lease income on sales-type leases is 357000000, against 305000000 and 175000000. The second quarter of fiscal 2027 alone states 3711000000 of sales-type lease revenue (see the quarterly item above).",
  "account": "sales-type lease revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"886000000\"",
  "paragraph_id": "0001571996-26-000008:facts:SalesTypeLeaseRevenue:2025-02-01..2026-01-30" }
```

```json
{ "id": "revenue_recognition_ai_optimized_server_revenue_annual_history",
  "what_changed": "The annual report states revenue from AI-optimized servers and networking of 24683000000 in fiscal 2026, against 9286000000 in fiscal 2025 and 1873000000 in fiscal 2024. Traditional servers and networking is 19512000000, against 17850000000 and 15751000000. Storage is 16631000000, against 16457000000 and 16261000000. Infrastructure Solutions Group revenue is 60826000000, against 43593000000 and 33885000000. Total revenue is 113538000000, against 95567000000 and 88425000000. United States revenue is 63140000000, against 51014000000 and 43986000000, and revenue outside the United States is 50398000000, against 44553000000 and 44439000000. The annual report also states that a single customer accounted for 0.12 of fiscal 2026 revenue. The first two quarters of fiscal 2027 state 16132000000 and 16401000000 for AI-optimized servers and networking (see the quarterly item above).",
  "account": "revenue by product and geography",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"24683000000\"",
  "paragraph_id": "0001571996-26-000008:facts:Revenues:2025-02-01..2026-01-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,srt:ProductOrServiceAxis=dell:AIOptimizedServersAndNetworkingMember,us-gaap:StatementBusinessSegmentsAxis=dell:InfrastructureSolutionsGroupMember" }
```

```json
{ "id": "earnings_quality_infrastructure_segment_operating_income_annual_history",
  "what_changed": "The annual report states Infrastructure Solutions Group operating income of 7111000000 in fiscal 2026, against 5579000000 in fiscal 2025 and 4286000000 in fiscal 2024. The segment's cost of revenue is 45022000000, against 29352000000 and 20943000000. Its selling, general and administrative expense is 6457000000, against 6593000000 and 6752000000. Its research and development expense is 2236000000, against 2069000000 and 1904000000. Total segment operating income is 9944000000, against 8551000000 and 7998000000. Consolidated operating income is 8149000000, against 6237000000 and 5411000000. Among the reconciling items, amortization of intangible assets is 497000000, against 667000000 and 833000000; stock-based compensation is 723000000, against 785000000 and 878000000; and other corporate expenses are 622000000, against 840000000 and 756000000. Operating income outside the segments is 47000000, against -22000000 and -120000000.",
  "account": "segment operating income",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"7111000000\"",
  "paragraph_id": "0001571996-26-000008:facts:OperatingIncomeLoss:2025-02-01..2026-01-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=dell:InfrastructureSolutionsGroupMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_client_segment_operating_income_annual_history",
  "what_changed": "The annual report states Client Solutions Group operating income of 2833000000 in fiscal 2026, against 2972000000 in fiscal 2025 and 3712000000 in fiscal 2024. It is lower in each of the two later years, while the segment's revenue is 50984000000, against 48393000000 and 48916000000. The segment's cost of revenue is 43691000000, against 41195000000 and 40658000000. Its selling, general and administrative expense is 3898000000, against 3750000000 and 4080000000. Its research and development expense is 562000000, against 476000000 and 466000000. Commercial revenue is 44062000000, against 40844000000 and 39814000000. Consumer revenue is 6922000000, against 7549000000 and 9102000000, also lower in each later year. In the second quarter of fiscal 2027 the quarterly report states segment operating income of 1142000000, against 803000000 a year earlier, and consumer revenue of 1842000000, against 1722000000 (see the quarterly items above).",
  "account": "client segment operating income",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"2833000000\"",
  "paragraph_id": "0001571996-26-000008:facts:OperatingIncomeLoss:2025-02-01..2026-01-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=dell:ClientSolutionsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_corporate_non_segment_revenue_annual_history",
  "what_changed": "The annual report states revenue outside the two reportable segments of 1728000000 in fiscal 2026, against 3581000000 in fiscal 2025 and 5624000000 in fiscal 2024. Operating income outside the segments is 47000000, against -22000000 and -120000000. The first two quarters of fiscal 2027 state 224000000 and 155000000 (see the quarterly item above).",
  "account": "corporate and other revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"1728000000\"",
  "paragraph_id": "0001571996-26-000008:facts:Revenues:2025-02-01..2026-01-30:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_annual_history",
  "what_changed": "The annual report states class C treasury stock acquired at a cost of 6000000000.0 in fiscal 2026 (54000000 shares), against 2600000000 (22000000 shares) in fiscal 2025 and 2100000000 (34000000 shares) in fiscal 2024. The costs are stated to the nearest hundred million. Shares outstanding are 652000000 at January 30, 2026, against 696000000 at January 31, 2025. Weighted average diluted shares are 684000000 in fiscal 2026, against 720000000 and 736000000. Dividends declared are 0.525 per share in each quarter of fiscal 2026, against 0.445 in each quarter of fiscal 2025. Cash dividends are 360000000, 355000000, 351000000 and 344000000 in the four quarters of fiscal 2026. Diluted earnings per share are 8.68 in fiscal 2026, against 6.38 and 4.60.",
  "account": "share repurchases, share count and dividends",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"6000000000.0\"",
  "paragraph_id": "0001571996-26-000008:facts:TreasuryStockValueAcquiredCostMethod:2025-02-01..2026-01-30:us-gaap:StatementClassOfStockAxis=us-gaap:CommonClassCMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_raised_after_year_end",
  "what_changed": "As a subsequent event, the annual report states a dividend declared on February 26, 2026 of 0.630 per share, against 0.525 per share in each quarter of fiscal 2026. At the same date it states a remaining class C repurchase authorization of 15200000000.",
  "account": "dividend per share and repurchase authorization",
  "expected_direction": "up",
  "horizon": "February 26, 2026 against the quarters of fiscal 2026",
  "quote": "\"value\": \"0.630\"",
  "paragraph_id": "0001571996-26-000008:facts:CommonStockDividendsPerShareDeclared:2026-02-26..2026-02-26:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "earnings_quality_stock_based_compensation_annual_history",
  "what_changed": "The annual report states stock-based compensation expense of 723000000 in fiscal 2026, against 785000000 in fiscal 2025 and 878000000 in fiscal 2024, lower in each later year. Of the fiscal 2026 expense, 157000000 sits in cost of sales and 566000000 in operating expenses, against 152000000 and 633000000 in fiscal 2025. The related tax benefit is 135000000, against 143000000 and 157000000. Unrecognized compensation cost for restricted stock units is 700000000 at January 30, 2026.",
  "account": "stock-based compensation",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025 and fiscal 2024",
  "quote": "\"value\": \"723000000\"",
  "paragraph_id": "0001571996-26-000008:facts:AllocatedShareBasedCompensationExpense:2025-02-01..2026-01-30" }
```

```json
{ "id": "liquidity_and_capital_inventory_components_year_end_fact",
  "what_changed": "The annual report states raw materials and supplies of 6696000000 at January 30, 2026, against 4432000000 at January 31, 2025. Work in process is 2772000000, against 1128000000, and finished goods are 969000000 at January 30, 2026. The January 30, 2026 figures are the same ones the quarterly report for the second quarter of fiscal 2027 prints (see the inventory item above), where raw materials reach 15894000000 at July 31, 2026.",
  "account": "inventories, by component",
  "expected_direction": "up",
  "horizon": "January 30, 2026 against January 31, 2025",
  "quote": "\"value\": \"6696000000\"",
  "paragraph_id": "0001571996-26-000008:facts:InventoryRawMaterialsAndSuppliesNetOfReserves:2026-01-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_amounts_in_cost_of_sales",
  "what_changed": "The annual report states amounts with a related party in cost of sales of 1010000000 for products and 2810000000 for services in fiscal 2024, and related-party product revenue of 103000000 in fiscal 2024. I quote only these fiscal 2024 values and state no later comparison.",
  "account": "related-party amounts in cost of sales",
  "expected_direction": "none",
  "horizon": "fiscal 2024",
  "quote": "\"value\": \"1010000000\"",
  "paragraph_id": "0001571996-26-000008:facts:RelatedPartiesAmountInCostOfSales:2023-02-04..2024-02-02:srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

## Seen in the notes

No fact in my input carries a marker saying whether its element sat inside a note. Each fact prints only an id, a paragraph_id, a tag, a context, a unit, decimals, a value, the form, the accession, the filing date and, for some, a superseded_by field. So I can place no item here.

Many of the numeric-fact items above use tags that do not appear on the condensed statements in the earnings release. Examples are the warranty accrual, supplier finance obligations, the restructuring reserve, severance by income-statement line, sales-type lease revenue, financing receivable originations, the credit-loss provision, the credit-score bands, investment gains, segment and product revenue, remaining performance obligations, the tax rate, guarantees and goodwill. From the annual report there are also contract-manufacturer receivables, treasury stock, the subsequent-event dividend, stock-based compensation, inventory components and related-party amounts. I have not judged where those elements sat. They carry no marker either way, and I list them under the statements heading only because that heading is where unmarked numeric facts go.
