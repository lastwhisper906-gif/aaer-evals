<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# EXTR — numbers reader — 10-K 0001193125-26-352872, fiscal year ended 2026-06-30

## What this input holds, and what it does not

- My directory holds four files: `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md`, `input_trends.json`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.
- My input has **no articulation checks, no restatement traces and no fourth-quarter derivation**. `input_numbers.json` holds only `ticker`, `cutoff`, `documents` (the 10-Q 0001193125-26-029334, the 10-Q 0001193125-26-197200 and the 10-K 0001193125-26-352872) and `facts`. So no articulation gap computed by Python and no Python restatement trace exists for me to report. Python also computed no fourth-quarter figure, and I do not derive one.
- **Restated prior values:** none found where I compared. The 10-Q 0001193125-26-029334 prints the 2025-06-30 balance sheet. Every line of it carries the same value as the 10-K's 2025-06-30 column, and the same as the release's prior-year column: cash, receivables, inventory, prepaid, current assets, PP&E, right-of-use assets, goodwill, intangibles, other assets, total assets, payables, accrued compensation, warranty, deferred revenue (current and non-current), debt (current and non-current), lease liabilities, deferred taxes, other liabilities, equity lines and totals. Facts that a later filing re-reports carry a `superseded_by` field. That field does not say whether the value changed. I did not compare the 10-Q 0001193125-26-029334's 2025-12-31 facts that are marked as superseded by the 10-Q 0001193125-26-197200 (for example equity 95912000 and warranty 9628000).
- **quarters-back-0 (target end 2026-06-30) has no cells.** The reason the period gives: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The derivation that sentence points to is not in my input. So no quarterly trend metric exists for the quarter the filing closes. **quarters-back-4 (target end 2025-07-01)** has no cells for the same reason. The latest filled quarter is quarters-back-1 (2026-01-01..2026-03-31), and its cells are itemized below as well.
- Prior predictions: "None on record." There are no earlier flags to carry forward.
- The research-and-development capitalization baseline in `input_trends.json` prints values (`book_value_with_rnd_capitalized`, `earnings_with_rnd_capitalized`, `research_and_development_asset`, `research_and_development_amortization`) with no `paragraph_id`. It sits outside every trend cell, so it cannot be quoted and is not itemized. Its `capitalized_development_cost` and `capitalized_over_expense` are missing in every year: "the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
- **No fact in `input_numbers.json` carries an in-note marker.** Every fact I read has the same fields (`id`, `paragraph_id`, `tag`, `context`, `unit`, `decimals`, `value`, `form`, `source_accession`, `filing_date`, and sometimes `superseded_by`), with nothing that says whether its element sat inside a note. The split between the two headings below therefore cannot rest on the marker the instructions describe. How I split instead is stated at the head of "Seen in the notes".
- **Reading coverage of `input_numbers.json` (60,774 lines).** I read these 10-K facts line by line: the balance sheet, income statement and comprehensive income, the cash flow statement, and the revenue, receivables, reserve, inventory, PP&E, contract-liability, warranty, debt, subsequent-event, lease, commitment, repurchase, deferred-tax and EPS notes. I only sampled the 10-K equity-statement detail, fair value, derivative, intangible, share-based-compensation and income-tax rate detail. In the 10-Q 0001193125-26-029334 I read the balance sheet, income statement, comprehensive income and equity-statement facts. The rest of that 10-Q, and the 10-Q 0001193125-26-197200 apart from its last EPS facts, I only sampled. Facts I did not read may hold findings this report does not carry.
- Late-filing notifications: the 8-K file lists none on or before 2026-08-17.
- `expected_direction` is the direction I expect the named account to move over the horizon. It is `none` wherever the input gives no basis for a direction, and on every item that is insufficient.

## Seen in the statements

### Trend table — years-back-0 (2025-07-01..2026-06-30), every metric

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "Accruals over total assets for the year is -0.06882454974058028. In years-back-1 it was -0.13830689427324236, which was second lowest of the 5 filled years. The printed year-over-year change is 0.06948234453266208. Inputs: net income 42119000.0 against operating cash flow 123182000.0 and assets 1177821000.0. A year earlier: net income -7467000.0 against operating cash flow 152031000.0. The ratio is still negative (operating cash flow above net income), but it is now the highest of the five filled years: net income rose while operating cash flow fell. Operating cash flow includes proceeds from receivables sold under a purchase agreement (see the notes).",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:accruals_over_total_assets:2025-07-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "The allowance over receivables-plus-allowance at 2026-06-30 is 0.0028776019579809533. At 2025-06-30 it was 0.005423904426251383, which was second highest of the 5 filled years. The printed change is -0.00254630246827043. Inputs: allowance 475000.0 against net receivables 164593000.0, where a year earlier it was 691000.0 against 126708000.0. The allowance fell while receivables rose, and the ratio is the lowest of the five filled years. The annual days-sales-outstanding cell rose in the same year. The ratio reads only the doubtful-accounts allowance against net receivables. The receivables note also carries a product-returns allowance and a gross receivables figure, itemized under the notes.",
  "account": "allowance for doubtful accounts (AllowanceForDoubtfulAccountsReceivableCurrent) over net receivables plus allowance",
  "expected_direction": "up",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:bad_debt_reserve_ratio:2025-07-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "Current contract liabilities over revenue for the year is 0.2568672468609598. In years-back-1 it was 0.2851393821591187, which was the highest of the 5 filled years. The printed change is -0.028272135298158918. Inputs: ContractWithCustomerLiabilityCurrent 329713000.0 against revenue 1283593000.0, where a year earlier it was 325078000.0 against 1140067000.0. The ratio counts the current portion only. The non-current portion (ContractWithCustomerLiabilityNoncurrent 323077000 against 292415000) is not in this cell.",
  "account": "current contract liabilities (deferred revenue, current) over revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:contract_liabilities_over_revenue:2025-07-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "Days sales of inventory for the year is 51.636458139516066. In years-back-1 it was 86.88209495521419, which was second highest of the 5 filled years. The printed change is -35.24563681569812. Inputs: InventoryNet 69950000.0 against cost of revenue 494452000.0, where a year earlier it was 102578000.0 against 430940000.0. Inventory fell while cost of revenue rose, and the value is second lowest of the five filled years. Non-cancelable inventory purchase commitments sit off the balance sheet (see the notes).",
  "account": "inventory (InventoryNet), days of cost of revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:days_sales_of_inventory:2025-07-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "Days sales outstanding for the year is 46.803344206457965. In years-back-1 it was 40.566405307758224, which was second lowest of the 5 filled years. The printed change is 6.236938898699741. years-back-1 had itself risen from years-back-2 (29.326441121264445, the lowest of the 5) by a printed 11.23996418649378. Inputs: net receivables 164593000.0 against revenue 1283593000.0. The value is third highest of the five filled years and has risen in each of the last two years. The receivable input is after receivables sold under a purchase agreement in fiscal 2026 (see the notes).",
  "account": "accounts receivable, net (AccountsReceivableNetCurrent), days of revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:days_sales_outstanding:2025-07-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "Gross margin for the year is 0.6147906696281453. In years-back-1 it was 0.6220046716552624, which was the highest of the 5 filled years. The printed change is -0.0072140020271170835. Inputs: revenue 1283593000.0 and cost of revenue 494452000.0. The value is second highest of the five filled years.",
  "account": "gross margin (revenue less CostOfGoodsAndServicesSold, over revenue)",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:gross_margin:2025-07-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "insufficient. The cell has no value because no inventory-reserve row exists at 2026-06-30. The coverage block prints this ratio as filled in no period of the table (\"filled\": 0). The 10-K reports inventory only net of reserves (raw materials and finished goods), and its cash-flow write-down (InventoryWriteDown) is itemized below.",
  "account": "inventory valuation reserve over inventory",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-352872:trends:inventory_reserve_ratio:2025-07-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual",
  "what_changed": "insufficient. The record carries no non-GAAP net income, so the gap was not computed in any period (\"filled\": 0). The release prints its own GAAP-to-non-GAAP reconciliation, itemized separately below. No Python-computed gap exists.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001193125-26-352872:trends:non_gaap_gap:2025-07-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "Receivables over revenue for the year is 0.12822834029166566. In years-back-1 it was 0.11114083645961158, which was second lowest of the 5 filled years. The printed change is 0.017087503832054082. Inputs: receivables 164593000.0 against revenue 1283593000.0, where a year earlier it was 126708000.0 against 1140067000.0. The value is third highest of the five filled years.",
  "account": "accounts receivable, net over revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:receivables_over_revenue:2025-07-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "Soft-asset share at 2026-06-30 is 0.7708879362823383. In years-back-1 it was 0.7605734561895496, which was second lowest of the 5 filled years. The printed change is 0.01031448009278868. Inputs: assets 1177821000.0, PP&E 58095000.0, cash 211758000.0. The value is third highest of the five filled years.",
  "account": "assets other than PP&E and cash, over total assets",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001193125-26-352872:trends:soft_asset_share:2025-07-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "insufficient. No warranty-accrual row exists at 2026-06-30 under any of the three concepts the table looks for, and the coverage block prints the ratio as filled in no period (\"filled\": 0). The filings do state a warranty balance, but under ProductWarrantyAccrualClassifiedCurrent, a concept this cell does not read (itemized below). The ratio is missing because of the concept, not because the balance is absent.",
  "account": "warranty accrual over revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-352872:trends:warranty_reserve_ratio:2025-07-01..2026-06-30" }
```

### Trend table — quarters-back-1 (2026-01-01..2026-03-31), the latest filled quarter

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "Days sales outstanding for the quarter is 46.213636966112716. The printed quarter-over-quarter change against quarters-back-2 is 2.104856593383296, and the year-over-year change against quarters-back-5 is 14.723364387423413. The two preceding filled quarters sit just below: quarters-back-2 at 44.10878037272942 (second highest) and quarters-back-3 at 43.23580396138536 (third highest). The value is the highest of the six filled quarters. No fourth-quarter cell exists, so the input does not say where the closing quarter sits.",
  "account": "accounts receivable, net, days of quarterly revenue",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:days_sales_outstanding:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "Receivables over quarterly revenue is 0.5134848551790302. The printed quarter-over-quarter change is 0.03404159025805825 and the year-over-year change is 0.16359293763803795. Inputs: receivables 162710000.0 against revenue 316874000.0. The value is the highest of the six filled quarters.",
  "account": "accounts receivable, net over quarterly revenue",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:receivables_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "Current deferred revenue over quarterly revenue is 1.0559339043279032. The printed quarter-over-quarter change is 0.023728195434296273 and the year-over-year change is -0.04014876557244995. Inputs: DeferredRevenueCurrent 334598000.0 against revenue 316874000.0. The value is third lowest of the six filled quarters.",
  "account": "current deferred revenue over quarterly revenue",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "Days sales of inventory for the quarter is 56.84546278743921. The printed quarter-over-quarter change is -5.758273628369331 and the year-over-year change is -38.63393150749369. Inputs: InventoryNet 76634000.0 against cost of revenue 121330000.0. The value is the lowest of the six filled quarters.",
  "account": "inventory, days of quarterly cost of revenue",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:days_sales_of_inventory:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "Gross margin for the quarter is 0.6171033281367357. The printed quarter-over-quarter change is 0.003499490753705148 and the year-over-year change is 0.0005623183126552966. The value is third highest of the six filled quarters.",
  "account": "quarterly gross margin",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:gross_margin:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "Soft-asset share at 2026-03-31 is 0.7746636924602157. The printed quarter-over-quarter change is 0.005712597793304908 and the year-over-year change is -0.0156579713160091. The value is second lowest of the six filled quarters.",
  "account": "assets other than PP&E and cash, over total assets",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:soft_asset_share:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "insufficient. The latest filled quarter has no operating-cash-flow row for the three-month period, so quarterly accruals were not computed. The coverage block lists the same gap for quarters-back-2, -5 and -6.",
  "account": "quarterly accruals over total assets",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-01..2026-03-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-352872:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_thin_history",
  "what_changed": "insufficient for a trend. Only two quarters of accruals are filled, so their order is the whole of the history. quarters-back-3 (2025-07-01..2025-09-30) reads 0.017007646458829163, with net income 5611000.0 against operating cash flow -13998000.0. The printed year-over-year change against quarters-back-7 (-0.02753276549587657) is 0.04454041195470573. In that quarter, operating cash flow was negative while net income was positive.",
  "account": "quarterly accruals over total assets",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"",
  "paragraph_id": "0001193125-26-352872:trends:accruals_over_total_assets:2025-07-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "insufficient. No allowance row exists at 2026-03-31, and none exists at any quarter-end in the table. The allowance is filled only for the five fiscal year-ends, so the input has no quarterly reserve path.",
  "account": "allowance for doubtful accounts over net receivables plus allowance",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-03-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001193125-26-352872:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

### Change of concept

```json
{ "id": "structure_and_disclosure_changes_contract_liabilities_concept_annual_cells",
  "what_changed": "The contract-liabilities metric rests on two different concepts. Every annual cell (years-back-0 through -4) reads ContractWithCustomerLiabilityCurrent, and this year's input is 329713000.0. Every filled quarterly cell reads DeferredRevenueCurrent (next item). The annual and quarterly series of one metric are built on different tags.",
  "account": "current contract liabilities / deferred revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"tag\": \"ContractWithCustomerLiabilityCurrent\"",
  "paragraph_id": "0001193125-26-352872:trends:contract_liabilities_over_revenue:2025-07-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_liabilities_concept_quarterly_cells",
  "what_changed": "The quarterly contract-liabilities cells (quarters-back-1, -2, -3, -5, -6, -7) all read DeferredRevenueCurrent, and the latest filled quarter's input is 334598000.0. The annual cells of the same metric read ContractWithCustomerLiabilityCurrent, so the metric changes concept between its quarterly and annual periods.",
  "account": "current contract liabilities / deferred revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"tag\": \"DeferredRevenueCurrent\"",
  "paragraph_id": "0001193125-26-352872:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_liabilities_same_amount_two_concepts_filing",
  "what_changed": "The 10-K files the current deferred revenue on its balance sheet as DeferredRevenueCurrent 329713000 at 2026-06-30 (325078000 at 2025-06-30). It also files ContractWithCustomerLiabilityCurrent at the same 329713000 (325078000). So the trend table's annual/quarterly concept split is a choice between two concepts the company files at the same amount. It is not a change in the amount.",
  "account": "current deferred revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"329713000\"",
  "paragraph_id": "0001193125-26-352872:facts:DeferredRevenueCurrent:2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_warranty_balance_concept_outside_trend_search",
  "what_changed": "The balance-sheet line 'Accrued warranty' is filed as ProductWarrantyAccrualClassifiedCurrent: 10953000 at 2026-06-30 and 9684000 at 2025-06-30 in the 10-K, and 9628000 at 2025-12-31 in the 10-Q 0001193125-26-029334. The trend table searches StandardProductWarrantyAccrual, ProductWarrantyAccrual and StandardProductWarrantyAccrualCurrent, so the warranty ratio is insufficient in every period although a warranty balance is filed in every period I read.",
  "account": "accrued warranty",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"10953000\"",
  "paragraph_id": "0001193125-26-352872:facts:ProductWarrantyAccrualClassifiedCurrent:2026-06-30" }
```

### Numeric facts — statements of the 10-K

```json
{ "id": "articulation_and_the_filed_history_depreciation_as_filed",
  "what_changed": "The 10-K files fiscal 2026 depreciation (Depreciation) as 15809000, 14704000 for fiscal 2025 and 24134000 for fiscal 2024. The fiscal 2026 figure equals the release's cash-flow-statement line (15,809), not the release's Adjusted EBITDA line (15,624). The EBITDA table is the one that departs from the filing.",
  "account": "depreciation",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"15809000\"",
  "paragraph_id": "0001193125-26-352872:facts:Depreciation:2025-07-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_history",
  "what_changed": "The 10-K files the inventory write-down (InventoryWriteDown, the cash-flow line 'Provision for excess and obsolete inventory') as 4160000 for fiscal 2026, 2618000 for fiscal 2025 and 71068000 for fiscal 2024. The trend table has no inventory-reserve balance in any period, so this flow is the only reserve-side history in my input. Three annual points do not support a trend claim.",
  "account": "inventory reserve (excess and obsolete write-down)",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"4160000\"",
  "paragraph_id": "0001193125-26-352872:facts:InventoryWriteDown:2025-07-01..2026-06-30" }
```

### 8-K earnings release (0001193125-26-333840) — figures

```json
{ "id": "results_against_expectations_release_gaap_gross_margin_without_trend_cell",
  "what_changed": "No trend cell exists for the quarter ended 2026-06-30. The release's own figure is the only gross margin in my input for that quarter: 62.2% against 61.6% a year earlier and 61.7% the quarter before. Python did not compute it, and I do not recompute it.",
  "account": "GAAP gross margin, quarter ended 2026-06-30",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "GAAP gross margin 62.2%, compared to 61.6% last year and 61.7% last quarter",
  "paragraph_id": "0001193125-26-333840:8k_2_02:17" }
```

```json
{ "id": "results_against_expectations_release_gaap_earnings_guidance_range",
  "what_changed": "For the quarter ending 2026-09-30, the company guides GAAP EPS of $0.00 - $0.02 and GAAP operating margin of 1.6% - 2.4%. It reports $0.13 GAAP diluted EPS and a 6.2% GAAP operating margin for the quarter ended 2026-06-30. The guidance reconciliation lists litigation charges, restructuring and system transition costs among the reconciling lines (next items).",
  "account": "GAAP earnings per share and operating margin",
  "expected_direction": "down",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "| GAAP | 61.6% - 62.1% |  | 1.6% - 2.4% |  | $0.00 - $0.02 |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:62" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_litigation_charge_guided_release",
  "what_changed": "Guidance for the quarter ending 2026-09-30 carries litigation charges of 3.4% - 3.5% of operating margin, 0.08 per share. Among the reconciling lines, only share-based compensation is larger. I found no litigation-accrual fact in the 10-K facts I read.",
  "account": "litigation charges",
  "expected_direction": "up",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "| Litigation charges | — |  | 3.4% - 3.5% |  | 0.08 |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:62" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_litigation_net_benefit_guided_release",
  "what_changed": "Full fiscal 2027 guidance carries a litigation benefit, net, of (0.3)% of operating margin and (0.03) per share. The first-quarter guidance carries a litigation charge. The release names no recovery or settlement that would produce the later benefit.",
  "account": "litigation charges (benefit), net",
  "expected_direction": "down",
  "horizon": "fiscal 2027 (ending 2027-06-30)",
  "quote": "| Litigation benefit, net | — |  | (0.3)% |  | (0.03) |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:67" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_litigation_charges_reported_release",
  "what_changed": "Litigation charges excluded from non-GAAP: 5,715 for the quarter against 22,006 a year earlier, and 8,849 for fiscal 2026 against 34,722 for fiscal 2025 (thousands). Litigation charges appear in every period the reconciliation shows, and guidance carries them into the next quarter.",
  "account": "litigation charges",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Litigation charges |  | 5,715 |  |  |  | 22,006 |  |  |  | 8,849 |  |  |  | 34,722 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:122" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_revolving_facility_release",
  "what_changed": "After the balance-sheet date, the company entered into a $500.0 million revolving credit facility on 2026-07-29 and repaid its existing term loan and credit facility. The 8-K index lists a 2026-07-30 filing with items 1.01, 1.02 and 2.03. Fiscal 2027 guidance carries debt refinancing charges of 0.01 per share. The 10-K files the draw on the new facility (itemized under the notes).",
  "account": "long-term debt and credit facility",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "Strengthened financial flexibility with a $500.0 million revolving credit facility entered into on July 29, 2026",
  "paragraph_id": "0001193125-26-333840:8k_2_02:33" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_release_statement",
  "what_changed": "Net cash provided by operating activities is 123,182 for fiscal 2026 against 152,031 for fiscal 2025 (thousands), against net income of 42,119 against (7,467). Operating cash flow fell in the year net income turned positive, which is the movement behind the annual accruals cell sitting highest of five years. Operating cash flow includes proceeds from receivables sold under a purchase agreement (see the notes).",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Net cash provided by operating activities |  |  | 123,182 |  |  |  | 152,031 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "earnings_quality_prepaid_and_other_assets_cash_use_release",
  "what_changed": "The change in prepaid expenses and other assets used (53,648) of operating cash in fiscal 2026 against (23,118) in fiscal 2025 (thousands). The balance sheet line 'Prepaid expenses and other current assets' is 103,495 against 74,265. The release does not say what the increase consists of.",
  "account": "prepaid expenses and other assets",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Prepaid expenses and other assets |  |  | (53,648 | ) |  |  | (23,118 | ) |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "earnings_quality_other_liabilities_cash_use_release",
  "what_changed": "The change in other current and long-term liabilities is (37,399) in fiscal 2026 against 16,602 in fiscal 2025 (thousands): a use of cash after a source the year before. The balance sheet line 'Other accrued liabilities' is 62,109 against 100,552. The release does not say what was paid.",
  "account": "other current and long-term liabilities",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Other current and long-term liabilities |  |  | (37,399 | ) |  |  | 16,602 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "structure_and_disclosure_changes_cloud_computing_amortization_line_release",
  "what_changed": "The cash flow statement carries a new adjustment line, 'Amortization of cloud computing implementation costs': 5,212 in fiscal 2026 against — in fiscal 2025 (thousands). The release separately describes multi-phase system transition costs that are not capitalizable (22,380 excluded from non-GAAP in fiscal 2026).",
  "account": "amortization of capitalized cloud computing implementation costs",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Amortization of cloud computing implementation costs |  |  | 5,212 |  |  |  | — |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "articulation_and_the_filed_history_depreciation_cash_flow_statement_release",
  "what_changed": "The release's cash flow statement prints fiscal 2026 depreciation of 15,809 (thousands). The Adjusted EBITDA table of the same release prints 'Depreciation expense' of 15,624 for the same year (next item). For fiscal 2025 both tables print 14,704. The two tables of one release disagree on fiscal 2026 depreciation, and the 10-K files 15809000. My input carries no articulation check, so no computed size for the gap exists.",
  "account": "depreciation",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "| Depreciation |  |  | 15,809 |  |  |  | 14,704 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "articulation_and_the_filed_history_depreciation_adjusted_ebitda_table_release",
  "what_changed": "The Adjusted EBITDA reconciliation prints fiscal 2026 depreciation expense of 15,624, against the cash flow statement's 15,809 and the 10-K's filed 15809000. Fiscal 2025 is 14,704 in both tables. The table also prints a single 'Amortization expense' line (8,602 for fiscal 2026), while the cash flow statement prints two amortization lines.",
  "account": "depreciation",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "| Depreciation expense |  | 4,024 |  |  |  | 3,443 |  |  |  | 15,624 |  |  |  | 14,704 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:124" }
```

```json
{ "id": "estimates_and_discretion_excess_and_obsolete_inventory_provision_release",
  "what_changed": "The provision for excess and obsolete inventory is 4,160 in fiscal 2026 against 2,618 in fiscal 2025 (thousands), rising while inventory fell (69,950 against 102,578 on the balance sheet). The trend table has no inventory-reserve value in any period.",
  "account": "inventory reserve (excess and obsolete provision)",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Provision for excess and obsolete inventory |  |  | 4,160 |  |  |  | 2,618 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "estimates_and_discretion_credit_loss_provision_release",
  "what_changed": "The provision for credit losses is 565 in fiscal 2026 against 157 in fiscal 2025 (thousands). The provision rose while the year-end allowance fell (475000.0 against 691000.0 in the trend cell). The 10-K roll-forward files write-offs of 781000, larger than the provision (itemized under the notes).",
  "account": "allowance for credit losses",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Provision for credit losses |  |  | 565 |  |  |  | 157 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "estimates_and_discretion_accrued_warranty_balance_release",
  "what_changed": "The release balance sheet prints accrued warranty of 10,953 at 2026-06-30 against 9,684 at 2025-06-30 (thousands). The trend table's warranty ratio never reaches this balance, because the balance is filed under ProductWarrantyAccrualClassifiedCurrent.",
  "account": "accrued warranty",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Accrued warranty |  |  | 10,953 |  |  |  | 9,684 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:85" }
```

```json
{ "id": "earnings_quality_non_gaap_adjustments_total_release",
  "what_changed": "The company's own total of non-GAAP adjustments to GAAP net income is 25,366 for the quarter against 41,296 a year earlier, and 101,003 for fiscal 2026 against 119,891 for fiscal 2025 (thousands). The trend table's non-GAAP gap is insufficient in every period, so this printed total is the only measure of the gap in my input.",
  "account": "non-GAAP adjustments to GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Total non-GAAP adjustments to GAAP net income | $ | 25,366 |  |  | $ | 41,296 |  |  | $ | 101,003 |  |  | $ | 119,891 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:123" }
```

```json
{ "id": "structure_and_disclosure_changes_other_non_recurring_costs_adjustment_release",
  "what_changed": "A non-GAAP adjustment category appears that has no amount in the prior year: 'Other non-recurring costs (benefit)', 3,648 for fiscal 2026 against — for fiscal 2025, and (231) for the quarter against —. The release defines it as external advisory and professional fees for non-recurring transactions.",
  "account": "non-GAAP adjustments — other non-recurring costs",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Other non-recurring costs (benefit) |  | (231 | ) |  |  | — |  |  |  | 3,648 |  |  |  | — |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:122" }
```

```json
{ "id": "earnings_quality_income_tax_benefit_release_statement",
  "what_changed": "The statement of operations prints a provision for (benefit from) income taxes of (135) for the quarter ended 2026-06-30, a benefit, against a 3,937 provision a year earlier. For the full year it prints 9,355 against 11,740 (thousands). The release says a valuation allowance remains against U.S. deferred tax assets; the 10-K's allowance is itemized under the notes.",
  "account": "provision for income taxes",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "| Provision for (benefit from) income taxes |  |  | (135 | ) |  |  | 3,937 |  |  |  | 9,355 |  |  |  | 11,740 |  |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:90" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_release",
  "what_changed": "Repurchases of common stock, including accelerated share repurchases, used (87,000) in fiscal 2026 against (37,993) in fiscal 2025 (thousands). Cash fell to 211,758 from 231,745, and treasury stock rose to 361,935 from 275,794. The 10-K files 5377808 shares acquired in fiscal 2026, 3299807 of them through an accelerated share repurchase settled 2026-01-30, and 113000000 of authorization remaining.",
  "account": "treasury stock / share repurchases",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "| Repurchase of common stock including accelerated share repurchases |  |  | (87,000 | ) |  |  | (37,993 | ) |",
  "paragraph_id": "0001193125-26-333840:8k_2_02:95" }
```

```json
{ "id": "liquidity_and_capital_net_cash_release",
  "what_changed": "The release's net cash (cash less gross debt) is $46.8 million at 2026-06-30, against $11.3 million at the end of the third quarter and $51.7 million a year earlier.",
  "account": "net cash (cash and equivalents less gross debt)",
  "expected_direction": "none",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "Q4 net cash was $46.8 million, as compared to net cash of $11.3 million at the end of Q3 2026 and net cash of $51.7 million at the end of Q4 in the prior year.",
  "paragraph_id": "0001193125-26-333840:8k_2_02:32" }
```

## Seen in the notes

No fact in my input carries the in-note marker, so no item below was placed by that marker. These items come from 10-K facts whose line does not appear on any statement the release prints (balance sheet, statement of operations, cash flows); that is the test I used to put them here. A later split should treat that placement as my reading, not as the extraction's marker.

```json
{ "id": "estimates_and_discretion_product_returns_allowance_lowest_balance",
  "what_changed": "The allowance for product returns (ValuationAllowancesAndReservesBalance, AllowanceForProductReturnsMember) is 18721000 at 2026-06-30. The earlier balances the 10-K prints are 23666000 at 2025-06-30, 52336000 at 2024-06-30 and 35125000 at 2023-06-30, so this is the lowest of the four year-end balances. Fiscal 2026 charges to cost and expense were 21801000 against deductions of 26746000; the deductions were larger. Product revenue in the same year was 809624000 against 704462000. The reserve fell while product sales rose. The trend table has no cell for this reserve, and four year-end balances do not support a trend claim.",
  "account": "allowance for product returns (offset against receivables)",
  "expected_direction": "up",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"18721000\"",
  "paragraph_id": "0001193125-26-352872:facts:ValuationAllowancesAndReservesBalance:2026-06-30:us-gaap:ValuationAllowancesAndReservesTypeAxis=extr:AllowanceForProductReturnsMember" }
```

```json
{ "id": "estimates_and_discretion_doubtful_accounts_write_offs_above_provision",
  "what_changed": "The doubtful-accounts roll-forward files write-offs of 781000 for fiscal 2026, 381000 for fiscal 2025 and 177000 for fiscal 2024. The provision (ProvisionForLoanLeaseAndOtherLosses) is 565000, 157000 and 210000 for the same years. Fiscal 2026 write-offs exceeded the provision, and the allowance closed at 475000 against 691000, 915000 and 882000 at the three prior year-ends.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"781000\"",
  "paragraph_id": "0001193125-26-352872:facts:AllowanceForDoubtfulAccountsReceivableWriteOffs:2025-07-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_gross_against_net",
  "what_changed": "The receivables note files gross receivables (AccountsReceivableGrossCurrent) of 349523000 at 2026-06-30 against 327067000 at 2025-06-30. Net receivables are 164593000 against 126708000. Against that, the doubtful-accounts allowance is 475000 and the product-returns allowance is 18721000. No trend cell reads the gross figure. The bad-debt ratio uses net receivables plus the doubtful-accounts allowance as its base. My input carries no check reconciling gross to net, so whether those two allowances are the whole difference is not computed anywhere I can see.",
  "account": "accounts receivable, gross and net",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"349523000\"",
  "paragraph_id": "0001193125-26-352872:facts:AccountsReceivableGrossCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_trade_receivables_sold_under_purchase_agreement",
  "what_changed": "The 10-K files proceeds of 20000000 for fiscal 2026 from sales of trade accounts receivable under an accounts receivable purchase agreement (ProceedsFromSaleOfFinanceReceivables). The 10-K facts I read print this amount for fiscal 2026 only. Receivables sold leave the balance sheet, and their proceeds are not separated from operating cash flow in any trend cell. Both the days-sales-outstanding cells and the accruals cell read the post-sale figures.",
  "account": "trade receivables sold / operating cash flow",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"20000000\"",
  "paragraph_id": "0001193125-26-352872:facts:ProceedsFromSaleOfFinanceReceivables:2025-07-01..2026-06-30:us-gaap:AccountsNotesLoansAndFinancingReceivableByReceivableTypeAxis=us-gaap:TradeAccountsReceivableMember,us-gaap:TypeOfArrangementAxis=extr:AccountsReceivablePurchaseAgreementMember" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_and_contract_liability",
  "what_changed": "Remaining performance obligation is 652800000 at 2026-06-30. It is filed as 0.51 expected from 2026-07-01, 0.24 from 2027-07-01 and 0.25 from 2028-07-01. Total contract liability (ContractWithCustomerLiability) is 652790000 against 617493000: subscription and support 637038000 against 603363000, other 15752000 against 14130000. The current portion is 329713000 against 325078000 and the non-current portion 323077000 against 292415000. Revenue recognized from opening contract liabilities is 318300000 for fiscal 2026, 296300000 for fiscal 2025 and 275700000 for fiscal 2024.",
  "account": "contract liabilities and remaining performance obligation",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"652800000\"",
  "paragraph_id": "0001193125-26-352872:facts:RevenueRemainingPerformanceObligation:2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_concentration_single_distributor",
  "what_changed": "One distributor (Jenne) accounts for 0.25 of receivables at fiscal 2026 year-end, against 0.22 a year earlier. ScanSource is filed at 0.15 of receivables for fiscal 2026. Revenue concentration for fiscal 2026 is Westcon 0.18, Jenne 0.16 and TD Synnex 0.15, against 0.18, 0.18 and 0.18 for fiscal 2025.",
  "account": "accounts receivable concentration",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"0.25\"",
  "paragraph_id": "0001193125-26-352872:facts:ConcentrationRiskPercentage1:2025-07-01..2026-06-30:srt:MajorCustomersAxis=extr:JenneIncMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "estimates_and_discretion_warranty_roll_forward",
  "what_changed": "Warranty roll-forward for fiscal 2026: warranties issued (StandardProductWarrantyAccrualWarrantiesIssued) 12544000 and payments 11275000, against 11540000 and 12798000 for fiscal 2025. The balance (ProductWarrantyAccrualClassifiedCurrent) is 10953000 at 2026-06-30, 9684000 at 2025-06-30, 10942000 at 2024-06-30 and 12322000 at 2023-06-30. The flows are filed under the StandardProductWarrantyAccrual family and the balance under a different concept.",
  "account": "accrued warranty",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"12544000\"",
  "paragraph_id": "0001193125-26-352872:facts:StandardProductWarrantyAccrualWarrantiesIssued:2025-07-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_components_net_of_reserves",
  "what_changed": "The inventory note files components only net of reserves. Raw materials (InventoryRawMaterialsNetOfReserves) are 24727000 at 2026-06-30 against 44808000, and finished goods 45223000 against 57770000. No reserve amount is filed beside them among the facts I read, which matches the trend table's missing inventory-reserve row.",
  "account": "inventory components",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"24727000\"",
  "paragraph_id": "0001193125-26-352872:facts:InventoryRawMaterialsNetOfReserves:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_noncancelable_inventory_purchase_commitments",
  "what_changed": "The 10-K files non-cancelable inventory purchase commitments (PurchaseCommitmentRemainingMinimumAmountCommitted, NonCancelableInventoryMember) of 112500000 at 2026-06-30. On-balance-sheet inventory is 69950000. The release says supply is secured into fiscal 2028. I found no prior-year amount for this commitment among the facts I read.",
  "account": "inventory purchase commitments",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"112500000\"",
  "paragraph_id": "0001193125-26-352872:facts:PurchaseCommitmentRemainingMinimumAmountCommitted:2026-06-30:us-gaap:PurchaseCommitmentExcludingLongtermCommitmentAxis=extr:NonCancelableInventoryMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_revolver_draw_filed",
  "what_changed": "As a subsequent event, the 10-K files a draw of 200000000 on 2026-07-29 under the new 2026 credit agreement's revolving facility. The facility has a maximum capacity of 500000000 and 300000000 remaining. At 2026-06-30, long-term debt was 165000000, with 20000000 due in the next twelve months and 145000000 in year two. The prior revolver had 0 drawn, 135600000 of capacity and 14400000 of letters of credit. The filed interest rate on the amended credit agreement was 0.0577 for fiscal 2026 against 0.0643. The post-year-end draw is larger than the year-end debt balance.",
  "account": "long-term debt and revolving credit facility",
  "expected_direction": "up",
  "horizon": "next fiscal quarter (ending 2026-09-30)",
  "quote": "\"value\": \"200000000\"",
  "paragraph_id": "0001193125-26-352872:facts:ProceedsFromLongTermLinesOfCredit:2026-07-29..2026-07-29:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember,us-gaap:DebtInstrumentAxis=extr:TwoThousandTwentySixCreditAgreementMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "earnings_quality_tax_valuation_allowance_remaining",
  "what_changed": "The deferred tax asset valuation allowance is 194596000 at 2026-06-30 against 207313000 at 2025-06-30. Gross deferred tax assets are 232568000 against 236302000, and net deferred tax assets 37972000 against 28989000. The release says the non-GAAP and GAAP tax provisions will align once the U.S. valuation allowance is released. A release would run through the GAAP tax line.",
  "account": "deferred tax asset valuation allowance",
  "expected_direction": "down",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"194596000\"",
  "paragraph_id": "0001193125-26-352872:facts:DeferredTaxAssetsValuationAllowance:2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_capitalized_software_amortization_begins",
  "what_changed": "The 10-K files capitalized computer software amortization (CapitalizedComputerSoftwareAmortization1) of 1200000 for fiscal 2026, against 0 for fiscal 2025 and 0 for fiscal 2024. PP&E gross for software and software development costs is 68302000 against 62089000. The trend table's R&D baseline found no CapitalizedComputerSoftwareAdditions in any period.",
  "account": "capitalized software",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"1200000\"",
  "paragraph_id": "0001193125-26-352872:facts:CapitalizedComputerSoftwareAmortization1:2025-07-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_capitalized_commissions",
  "what_changed": "Capitalized contract costs for commissions (CapitalizedContractCostNet, CommissionFeesMember) are 32100000 at 2026-06-30 against 26900000 at 2025-06-30. Amortization of those costs is 14200000 for fiscal 2026, 12500000 for fiscal 2025 and 10900000 for fiscal 2024.",
  "account": "capitalized contract costs (sales commissions)",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "\"value\": \"32100000\"",
  "paragraph_id": "0001193125-26-352872:facts:CapitalizedContractCostNet:2026-06-30:us-gaap:CapitalizedContractCostAxis=extr:CommissionFeesMember" }
```
