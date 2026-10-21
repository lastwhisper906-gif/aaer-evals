# Numbers report: LII, 10-Q 0001069202-26-000087 (period ending 2026-06-30, cutoff 2026-07-29)

## What this report rests on

- **Directory check.** The directory holds `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md` and `input_trends.json`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. This is not a broken run.
- **Prior flags.** `input_prior_predictions.md` says there is no earlier run for this company, so there is nothing to carry forward.
- **How much I read.** I read `input_trends.json`, `input_8k.md` and `input_prior_predictions.md` in full. I did **not** read `input_numbers.json` (71,081 lines) in full, because it does not fit in my context. I read these lines:
  - 1–3549: the opening of the 10-K 0001069202-26-000028 facts, covering the balance sheet, income statement and comprehensive income.
  - 52000–52059: a probe into the Q1 10-Q 0001069202-26-000054.
  - 54380–58879 and 60000–71081: the triggering 10-Q 0001069202-26-000087.

  I did not read these lines:
  - 3550–51999: the rest of the 10-K facts and most of the Q1 10-Q facts.
  - 52060–54379: the rest of the Q1 10-Q facts.
  - 58879–59999: part of the triggering 10-Q's statement of equity.

  Anything that sits only in the unread lines is not reported here.
- **Fields in the numbers file.** The top-level keys are only `ticker`, `cutoff`, `documents` and `facts`. Each fact prints `id`, `paragraph_id`, `tag`, `context`, `value` and `number`, and some print `superseded_by`. **None of the facts I read carries a field saying whether its element sat inside a note.** Without that marker I cannot split facts between the two headings, so every fact item is under "Seen in the statements". The notes heading explains this and holds no items.
- **Checks that do not exist in my input.** Neither file has an articulation-check section, a restatement-trace section or a fourth-quarter derivation. The keys in `input_trends.json` are `coverage`, `cutoff`, `quarters`, `source`, `ticker`, `window` and `years`. So:
  - I report no articulation gaps.
  - I report no restated prior values traced by Python. In the facts I read, values marked `superseded_by` print the same value in the later filing where I could see both. I noted two of these markers below and did not call them restatements.
  - I report no change of tag. In every trend cell, each input keeps the same tag across all periods.
- **The quarter the record does not reach.** `quarters-back-0` (target end 2026-06-30) has no cells. Its printed reason is: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the companyfacts record's newest row was filed 2026-04-29, before this run's cutoff 2026-07-29 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it".
  - Every ratio for the triggering quarter is therefore missing from the trend table. The 10-Q's own facts are in `input_numbers.json`, and I quote them below without computing any ratio from them.
  - `quarters-back-6` (target end 2024-12-31) also has no cells. Its reason is: "no quarter ending within 20 days of 2024-12-31 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". No output from that derivation is in my directory.
- **The R&D capitalisation baseline.** The `research_and_development_capitalized` block in each year prints values but no `paragraph_id`, so I cannot quote it and do not itemise it. For every year it prints `capitalized_development_cost` and `capitalized_over_expense` as missing: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
- **What `expected_direction` means here.** It is the direction the item, taken alone, points for the company's next reported results (earnings and cash conversion). It is "none" wherever the printed numbers do not point anywhere. Where a value sits in its history describes it; it did not decide whether I reported it.

## Seen in the statements

### Trend table: every metric in `years-back-0` (2025-01-01..2025-12-31)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "Value 0.011808515850850115, year-over-year change 0.04899083629283907 against years-back-1, positioned second highest of the 5 filled years. Formula as printed: (net_income - operating_cash_flow) / assets. Inputs: net_income 805800000.0 and operating_cash_flow 757600000.0 (both 0001069202-26-000028), assets 4081800000.0 (0001069202-26-000054).",
  "account": "total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "Value 0.014473012089221863, year-over-year change -0.011745871398773422 against years-back-1, positioned lowest of the 5 filled years. Inputs: allowance 8500000.0 and receivables 578800000.0 (0001069202-26-000054).",
  "account": "allowance for doubtful accounts over gross receivables",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "Value 0.0020210574942736703, year-over-year change 0.0010849557961851901 against years-back-1, positioned third highest of the 5 filled years. Inputs: contract liabilities 10500000.0 (0001069202-26-000054) and revenue 5195300000.0 (0001069202-26-000028).",
  "account": "current contract liabilities over revenue",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "Value 121.5717381881231, year-over-year change 33.96917912195778 against years-back-1, positioned highest of the 5 filled years. Inputs: inventory 1152600000.0 (0001069202-26-000054) and cost of revenue 3460500000.0 (0001069202-26-000028). The history mixes filing dates. The years-back-3 inventory comes from 0001628280-24-004446 (filed 2024-02-13) and years-back-4 from 0001628280-23-004257 (filed 2023-02-21), both filed before the LIFO-to-FIFO change the 8-K places in the fourth quarter of 2025, while years-back-0 to years-back-2 draw on filings from 2026. The input does not say how much of the position the method change explains.",
  "account": "inventories",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "Value 40.66406174811849, year-over-year change -4.63625839866225 against years-back-1, positioned lowest of the 5 filled years. Inputs: year-end receivables 578800000.0 (0001069202-26-000054) and annual revenue 5195300000.0 (0001069202-26-000028).",
  "account": "accounts and notes receivable",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "Value 0.3339171943872346, year-over-year change 0.0011330407167798318 against years-back-1, positioned highest of the 5 filled years. Inputs: revenue 5195300000.0 and cost of revenue 3460500000.0 (0001069202-26-000028). The years-back-3 inputs come from 0001628280-25-004859 (filed 2025-02-11) and the years-back-4 inputs from 0001628280-24-004446, both filed before the LIFO-to-FIFO change. The input does not quantify the effect of that change on the ranking.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. The cell is not filled for any of the 5 years, because the record tags no inventory valuation reserve. No value, change or position exists.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001069202-26-000087:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient. The record holds no non-GAAP net income, so the gap between GAAP and non-GAAP earnings does not exist in the trend table for any period.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001069202-26-000087:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "Value 0.11140838835100957, year-over-year change -0.012362978170249297 against years-back-1, positioned lowest of the 5 filled years. Inputs: receivables 578800000.0 and revenue 5195300000.0.",
  "account": "accounts and notes receivable over revenue",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "Value 0.7742662550835415, year-over-year change 0.10995686281834816 against years-back-1, positioned highest of the 5 filled years. Inputs: assets 4081800000.0, net PP&E 887200000.0 and cash 34200000.0 (all 0001069202-26-000054).",
  "account": "assets other than PP&E and cash, over total assets",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "Value 0.032182934575481686, year-over-year change 0.0025272327800386282 against years-back-1, positioned highest of the 5 filled years. Inputs: warranty accrual 167200000.0 (0001069202-26-000054) and revenue 5195300000.0 (0001069202-26-000028).",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001069202-26-000087:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

### Trend table: the latest filled quarter, `quarters-back-1` (2026-01-01..2026-03-31)

`quarters-back-0` has no cells (reason given above), so this is the newest quarter the table holds.

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "Value 0.02355161087427493, positioned lowest of the 2 filled quarters. Year-over-year change -0.02431549568357655 against quarters-back-5. No quarter-over-quarter change, because accruals_over_total_assets is not filled in quarters-back-2. Two filled quarters do not support a trend claim: insufficient for trend.",
  "account": "total accruals over total assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "Value 0.013850837138508371, quarter-over-quarter change -0.000622174950713492, year-over-year change -0.010404290874667254, positioned second lowest of the 6 filled quarters. Inputs: allowance 9100000.0 and receivables 647900000.0.",
  "account": "allowance for doubtful accounts over gross receivables",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "Value 0.008809796493700995, quarter-over-quarter change 2.3185615039906377e-05, year-over-year change 0.004521152078261875, positioned highest of the 6 filled quarters. Inputs: contract liabilities 10000000.0 and revenue 1135100000.0.",
  "account": "current contract liabilities over revenue",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "Value 138.90405715743813, quarter-over-quarter change 7.292787454074613, year-over-year change 27.920047317339737, positioned highest of the 6 filled quarters. Inputs: inventory 1209700000.0 and cost of revenue 783800000.0. The quarters-back-3 and quarters-back-4 cells pair inventory filed in 2025 (0001069202-25-000048 and 0001069202-25-000032), before the LIFO-to-FIFO change, with cost of revenue from the 10-K 0001069202-26-000028 filed after it. The input does not say whether those cells sit on one basis.",
  "account": "inventories",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:days_sales_of_inventory:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "Value 51.37080433441987, quarter-over-quarter change 6.810469606386398, year-over-year change -3.3122089044389753, positioned third highest of the 6 filled quarters. Inputs: receivables 647900000.0 and revenue 1135100000.0.",
  "account": "accounts and notes receivable",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:days_sales_outstanding:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "Value 0.30948815082371595, quarter-over-quarter change -0.016285907753689932, year-over-year change -0.008337692920457107, positioned lowest of the 6 filled quarters. Inputs: revenue 1135100000.0 and cost of revenue 783800000.0.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:gross_margin:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. The cell is not filled; the record tags no inventory valuation reserve in any quarter.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001069202-26-000087:trends:inventory_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient. The cell is not filled; the record holds no non-GAAP measure. The 8-K annex reconciles only free cash flow, and that reconciliation does not fill this cell.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001069202-26-000087:trends:non_gaap_gap:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "Value 0.5707867148268875, quarter-over-quarter change 0.08643525039174105, year-over-year change -0.03680232116043303, positioned third highest of the 6 filled quarters.",
  "account": "accounts and notes receivable over revenue",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:receivables_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "Value 0.7750133948330887, quarter-over-quarter change 0.0007471397495472099, year-over-year change 0.07237404772421563, positioned highest of the 6 filled quarters. Inputs: assets 4292700000.0, net PP&E 917600000.0 and cash 48200000.0.",
  "account": "assets other than PP&E and cash, over total assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:soft_asset_share:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
  "what_changed": "Value 0.14914985463835786, quarter-over-quarter change 0.009233536646726076, year-over-year change -0.002351170907045841, positioned second highest of the 6 filled quarters. Inputs: warranty accrual 169300000.0 and revenue 1135100000.0. The printed formula, warranty_accrual / revenue, divides by one quarter's revenue, so this is not on the same scale as the annual cell.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001069202-26-000087:trends:warranty_reserve_ratio:2026-01-01..2026-03-31" }
```

### Numeric facts: the triggering 10-Q (0001069202-26-000087), which the trend table does not reach

No ratio below is computed. Each item gives the printed value and, where the same filing prints one, the comparative.

```json
{ "id": "results_against_expectations_net_sales_in_triggering_report",
  "what_changed": "Revenue for 2026-04-01..2026-06-30 printed 1545300000. The same filing prints 1500900000 for 2025-04-01..2025-06-30.",
  "account": "net sales",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"1545300000\"",
  "paragraph_id": "0001069202-26-000087:facts:Revenues:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_profit_in_triggering_report",
  "what_changed": "Gross profit for the quarter printed 539500000, against 517500000 for 2025-04-01..2025-06-30. Cost of goods sold printed 1005800000 against 983400000. Per the 8-K, the 2025 comparatives are adjusted for the LIFO-to-FIFO change.",
  "account": "gross profit",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"539500000\"",
  "paragraph_id": "0001069202-26-000087:facts:GrossProfit:2026-04-01..2026-06-30" }
```

```json
{ "id": "results_against_expectations_net_income_in_triggering_report",
  "what_changed": "Net income for the quarter printed 269000000.0, against 273900000 for 2025-04-01..2025-06-30. Diluted EPS printed 7.72 against 7.71.",
  "account": "net income",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"269000000.0\"",
  "paragraph_id": "0001069202-26-000087:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_balance_in_triggering_report",
  "what_changed": "Net receivables at 2026-06-30 printed 918100000, against 578800000 at 2025-12-31 in the same filing. The trend table's input for 2025-06-30 (seasonal comparison) is 868200000.0, from 0001069202-25-000032. The allowance at 2026-06-30 printed 7900000. No DSO for the quarter exists in my input.",
  "account": "accounts and notes receivable",
  "expected_direction": "none",
  "horizon": "next two quarterly filings",
  "quote": "\"value\": \"918100000\"",
  "paragraph_id": "0001069202-26-000087:facts:ReceivablesNetCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_receivables_cash_flow_build",
  "what_changed": "The cash-flow line for the change in accounts and notes receivable for 2026-01-01..2026-06-30 printed 345200000, against 205900000 for 2025-01-01..2025-06-30; the 8-K shows it as (345.2) and (205.9). Revenue for the same six months printed 2680400000 against 2573500000.",
  "account": "accounts and notes receivable",
  "expected_direction": "down",
  "horizon": "next two quarterly filings",
  "quote": "\"value\": \"345200000\"",
  "paragraph_id": "0001069202-26-000087:facts:IncreaseDecreaseInAccountsAndNotesReceivable:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_against_net_income",
  "what_changed": "Operating cash flow for 2026-01-01..2026-06-30 printed 188100000, against 51000000.0 for 2025-01-01..2025-06-30. Net income for the same six months printed 386200000 against 403500000. No accruals ratio for this period exists in my input, because quarters-back-0 has no cells.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "next two quarterly filings",
  "quote": "\"value\": \"188100000\"",
  "paragraph_id": "0001069202-26-000087:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_inventory_balance_in_triggering_report",
  "what_changed": "Net inventory at 2026-06-30 printed 1152400000, against 1152600000 at 2025-12-31. The trend input for 2026-03-31 is 1209700000.0. Components at 2026-06-30: finished goods 687800000, work in process 13600000, raw materials 451000000.0.",
  "account": "inventories",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"1152400000\"",
  "paragraph_id": "0001069202-26-000087:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "across_documents_inventory_cash_flow_against_release_explanation",
  "what_changed": "The cash-flow change in inventories for 2026-01-01..2026-06-30 printed 7000000.0, against 300700000 for the 2025 six months; the 8-K shows (7.0) and (300.7). The release attributes the quarter's higher operating cash flow to reduced inventory levels (paragraph 0001069202-26-000085:8k_2_02:25). The six-month receivables line printed 345200000 in the same statement.",
  "account": "inventories",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"7000000.0\"",
  "paragraph_id": "0001069202-26-000087:facts:IncreaseDecreaseInInventories:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_in_triggering_report",
  "what_changed": "The product warranty accrual at 2026-06-30 printed 174600000, against 167200000 at 2025-12-31. For 2026-01-01..2026-06-30, warranties issued printed 29000000.0 and payments printed 24700000. Current portion 54700000; noncurrent portion 119900000.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"value\": \"174600000\"",
  "paragraph_id": "0001069202-26-000087:facts:ProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_preexisting_adjustment",
  "what_changed": "The change in estimate for pre-existing warranties for 2026-01-01..2026-06-30 printed 3500000. No comparative for this line was in the lines I read.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"value\": \"3500000\"",
  "paragraph_id": "0001069202-26-000087:facts:ProductWarrantyAccrualPreexistingIncreaseDecrease:2026-01-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_in_triggering_report",
  "what_changed": "Current contract liabilities at 2026-06-30 printed 8200000, against 10500000 at 2025-12-31. Noncurrent contract liabilities printed 10700000 against 10300000. Revenue recognised from contract liabilities in 2026-04-01..2026-06-30 printed 2300000, against 800000 in the 2025 quarter.",
  "account": "contract liabilities",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"8200000\"",
  "paragraph_id": "0001069202-26-000087:facts:ContractWithCustomerLiabilityCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_provision_in_triggering_report",
  "what_changed": "The provision for credit losses for 2026-01-01..2026-06-30 printed 2500000, against 800000 for 2025-01-01..2025-06-30. The allowance at 2026-06-30 printed 7900000, against 8500000 at 2025-12-31.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "next two quarterly filings",
  "quote": "\"value\": \"2500000\"",
  "paragraph_id": "0001069202-26-000087:facts:ProvisionForDoubtfulAccounts:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_measurement_period_adjustment",
  "what_changed": "The purchase-accounting adjustment to goodwill for 2026-01-01..2026-06-30 printed 6500000. Goodwill printed 503700000 at 2026-06-30 against 497200000 at 2025-12-31. Duro Dyne and Supco goodwill printed 283700000 against 277200000.",
  "account": "goodwill",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"value\": \"6500000\"",
  "paragraph_id": "0001069202-26-000087:facts:GoodwillPurchaseAccountingAdjustments:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_commercial_paper_balance",
  "what_changed": "Commercial paper at 2026-06-30 printed 412000000.0, against 226000000.0 at 2025-12-31. Cash at 2026-06-30 printed 51500000. The weighted-average commercial paper rate printed 0.0411, against 0.0398.",
  "account": "commercial paper",
  "expected_direction": "none",
  "horizon": "next two quarterly filings",
  "quote": "\"value\": \"412000000.0\"",
  "paragraph_id": "0001069202-26-000087:facts:CommercialPaper:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_commercial_paper_issuance",
  "what_changed": "Commercial paper issued in 2026-01-01..2026-06-30 printed 910000000.0, against 141100000 in the 2025 six months. Repayments printed 724000000.0 against 112100000.",
  "account": "commercial paper",
  "expected_direction": "none",
  "horizon": "next two quarterly filings",
  "quote": "\"value\": \"910000000.0\"",
  "paragraph_id": "0001069202-26-000087:facts:ProceedsFromIssuanceOfCommercialPaper:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_interest_expense",
  "what_changed": "Interest expense for 2026-04-01..2026-06-30 printed 14700000, against 8300000 for the 2025 quarter.",
  "account": "interest expense",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"14700000\"",
  "paragraph_id": "0001069202-26-000087:facts:InterestExpense:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate",
  "what_changed": "The effective tax rate for 2026-04-01..2026-06-30 printed 0.208, against 0.194 for the 2025 quarter.",
  "account": "income tax expense",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.208\"",
  "paragraph_id": "0001069202-26-000087:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_operating_items",
  "what_changed": "Other operating income/expense, net for 2026-04-01..2026-06-30 printed -2400000, against 2700000 for the 2025 quarter. The 8-K shows this line as 'Losses (gains) and other expenses, net': 2.4 against (2.7).",
  "account": "losses (gains) and other expenses, net",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"-2400000\"",
  "paragraph_id": "0001069202-26-000087:facts:OtherOperatingIncomeExpenseNet:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_income_taxes_paid",
  "what_changed": "Income taxes paid, net, for 2026-01-01..2026-06-30 printed 113500000, against 44000000.0 for the 2025 six months. The change in income taxes payable net of receivable printed -20400000, against 55200000.",
  "account": "income taxes paid",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"113500000\"",
  "paragraph_id": "0001069202-26-000087:facts:IncomeTaxesPaidNet:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases",
  "what_changed": "Repurchases of common stock for 2026-01-01..2026-06-30 printed 151300000, against 294800000 for the 2025 six months. Remaining authorisation at 2026-06-30 printed 857700000.",
  "account": "treasury stock",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"151300000\"",
  "paragraph_id": "0001069202-26-000087:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-06-30" }
```

### Filed-history markers

```json
{ "id": "articulation_and_the_filed_history_superseded_balance_sheet_marker",
  "what_changed": "The 10-K's 2025-12-31 balance-sheet facts carry a superseded_by marker naming the triggering 10-Q. For receivables, the 10-K prints 578800000 and the 10-Q prints 578800000 for the same date. My input has no restatement trace, so this is a re-report, not a traced restatement.",
  "account": "accounts and notes receivable",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001069202-26-000087\"",
  "paragraph_id": "0001069202-26-000028:facts:ReceivablesNetCurrent:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_superseded_equity_marker",
  "what_changed": "The 10-K's stockholders' equity at 2024-12-31 (962100000) carries a superseded_by marker naming the Q1 10-Q 0001069202-26-000054. The trend table's years-back-1 baseline takes 962100000.0 for that date from 0001069202-26-000054. No differing value is visible in what I read, and no restatement trace exists in my input.",
  "account": "stockholders' equity",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001069202-26-000054\"",
  "paragraph_id": "0001069202-26-000028:facts:StockholdersEquity:2024-12-31" }
```

### From the 8-K earnings release (exhibit 99.1 to 0001069202-26-000085)

These come from neither the trend table nor the facts. I place them here because the release's tables are statements, and I keep them apart from the items above.

```json
{ "id": "results_against_expectations_eps_guidance_lowered",
  "what_changed": "Full-year EPS guidance moved to $23.00–$24.00 from $23.50–$25.00. Revenue guidance was reaffirmed at about 8% growth.",
  "account": "diluted earnings per share",
  "expected_direction": "down",
  "horizon": "current fiscal year",
  "quote": "Earnings per share guidance has been updated to a range of $23.00 to $24.00 compared to the prior range of $23.50 to $25.00.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:32" }
```

```json
{ "id": "earnings_quality_tariff_refunds_in_product_cost",
  "what_changed": "The release nets $30 million of tariff refunds into the quarter's product-cost line. Paragraph 0001069202-26-000085:8k_2_02:16 calls them 'earlier than expected'. The segment paragraphs attribute $25 million to Home Comfort Solutions and $5 million to Building Climate Solutions.",
  "account": "cost of goods sold",
  "expected_direction": "down",
  "horizon": "next two quarterly filings",
  "quote": "$11 million product cost primarily reflecting inflation and factory under absorption, net of $30 million in tariff refunds",
  "paragraph_id": "0001069202-26-000085:8k_2_02:23" }
```

```json
{ "id": "structure_and_disclosure_changes_lifo_to_fifo_comparatives",
  "what_changed": "The 2025 comparatives in the release are adjusted for a change from LIFO to FIFO in the fourth quarter of 2025. Older trend cells draw inputs filed before that change: inventory in quarters-back-3, quarters-back-4 and quarters-back-7, and revenue, cost and inventory in years-back-3 and years-back-4. My input carries no trace saying which of those values were restated.",
  "account": "inventories and cost of goods sold",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "Note: The 2025 amounts are adjusted to reflect the accounting method change from LIFO to FIFO that occurred in the fourth quarter of 2025.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:48" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_home_comfort_volume",
  "what_changed": "Home Comfort Solutions revenue fell year over year on lower volumes. The release's segment table prints 935.6 against 1,009.3 for the quarter, and the 10-Q segment fact prints 935600000 against 1009300000.",
  "account": "net sales, Home Comfort Solutions segment",
  "expected_direction": "down",
  "horizon": "next two quarterly filings",
  "quote": "Revenue declined 7% year over year, primarily reflecting lower sales volumes, partially offset by favorable mix-price and contributions from acquisitions.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:16" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_growth_from_acquisitions",
  "what_changed": "The release attributes the quarter's consolidated revenue growth to completed acquisitions.",
  "account": "net sales",
  "expected_direction": "none",
  "horizon": "next two quarterly filings",
  "quote": "Revenue: $1.5 billion was up 3%, driven by revenue from completed acquisitions.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:21" }
```

```json
{ "id": "across_documents_operating_cash_flow_explanation",
  "what_changed": "The release explains the quarter's operating cash flow rise by reduced inventory levels. The 10-Q prints the six-month inventory change at 7000000.0 and the receivables change at 345200000. No quarter-only cash-flow facts were in the lines I read.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "Operating cash flow was $172 million compared to $87 million in the prior-year quarter driven by reduced inventory levels.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:25" }
```

```json
{ "id": "liquidity_and_capital_free_cash_flow_guidance",
  "what_changed": "Free cash flow guidance is unchanged. Six-month free cash flow in the release's annex prints 98.3, against (2.1) for the 2025 six months.",
  "account": "free cash flow",
  "expected_direction": "none",
  "horizon": "current fiscal year",
  "quote": "Free Cash Flow is still estimated to be within the range of $750 million to $850 million.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:33" }
```

## Seen in the notes

None of the facts I read carries a marker saying whether its element sat inside a note when it was extracted. Neither does the trend table nor any other part of my input. So I can place no item here without judging it myself, and the instructions say I should not. Some fact items above come from elements that are usually disclosed in notes: warranty roll-forward, contract liabilities, inventory components, goodwill adjustments, commercial paper rates and the effective tax rate. They sit under "Seen in the statements" only because no marker separates them. A later split will need that marker added to the facts. This section has no items.
