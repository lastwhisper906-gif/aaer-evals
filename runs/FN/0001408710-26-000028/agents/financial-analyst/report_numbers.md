<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_numbers.md — FN (Fabrinet), 10-K 0001408710-26-000028, fiscal year ended 2026-06-26

## Before the items

**Input check.** My directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. I read every one in full. None of them contains prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. input_prior_predictions.md says "None on record."

**What is missing from my input.** These are stated here once and never computed:
- **Articulation checks.** My input has none, so it states no articulation gap and I report none.
- **Restatement traces.** My input has none. Some facts in input_numbers.json carry a `superseded_by` mark pointing to 0001408710-26-000028. For every superseded value I compared, the later filing prints the same value: RSU and PSU nonvested counts, warrants outstanding, purchase obligations, credit-facility capacities, guarantee amounts, geographic non-current assets, and AOCI components at 2025-06-27. My input states no restated prior value, so I report none.
- **Tag changes.** My input states no period that rests on a different concept, so I report none.
- **Fourth-quarter derivation.** My directory has no fourth-quarter derivation output. No quarterly ratio exists for the quarter ended 2026-06-26. I do not derive one.

**The period the record does not reach: quarters-back-0** (target end 2026-06-26). It has no cells, so no item is written for it. The reason the period gives: "no quarter ending within 20 days of 2026-06-26 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".

quarters-back-4 (target end 2025-06-27) is missing for the same reason, with that date in place of 2026-06-26. The only fourth-quarter figures in my input are the ones the 8-K release prints; they are quoted below.

**Rows with no paragraph_id.** The research-and-development capitalization block inside years-back-0 is entirely unfilled. Its rows print no `paragraph_id`, so I cannot write an item for them:
- book value with R&D capitalized
- earnings with R&D capitalized
- capitalized over expense
- R&D asset
- R&D amortization
- R&D expense for 0–5 years back
- capitalized development cost

The reasons they give are that the record "tags none of us-gaap:ResearchAndDevelopmentExpense in any period" and "tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period". All of these are **insufficient**.

**Accruals over total assets, quarterly.** This is filled in only 2 of the 8 quarters (quarters-back-3 and quarters-back-7). The reason given is that the 10-Qs carry no three-month operating cash flow. That is **insufficient** for any quarterly trend claim; one item below quotes the reason.

**How the fields are filled.**
- `expected_direction` is the direction of the change the quoted row prints: the sign of the printed change, or which of two printed values is larger. It is `none` where a cell is insufficient or has nothing to compare against.
- `horizon` is the window the item speaks to.
- Every number in `what_changed` is copied from the input. I computed none of them.

## Seen in the statements

### Trend table — years-back-0 (fiscal year 2025-06-28..2026-06-26)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend_cell",
  "what_changed": "accruals_over_total_assets for the year is 0.05530661134181599. The year-over-year change against years-back-1 is 0.05383668375746998. Inputs as printed: net income 473027000, operating cash flow 256725000, assets 3910961000. It sits highest of the 5 filled years; the prior year sat second lowest at 0.001469927584346013.",
  "account": "accruals over total assets (net income less operating cash flow, over assets)",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:accruals_over_total_assets:2025-06-28..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend_cell",
  "what_changed": "bad_debt_reserve_ratio for the year is 0.0010304391731756075. The year-over-year change against years-back-1 is -0.0007374282578131092. Inputs: allowance 1050000, receivables 1017933000. It sits lowest of the 5 filled years.",
  "account": "allowance for expected credit losses against receivables",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:bad_debt_reserve_ratio:2025-06-28..2026-06-26" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend_cell",
  "what_changed": "contract_liabilities_over_revenue for the year is 0.0009129307144410039. The year-over-year change against years-back-1 is -0.0033180188262142184. Inputs: contract liabilities 4237000, revenue 4641097000. It sits second lowest of the 5 filled years; years-back-1 was the highest of the 5 at 0.004230949540655222.",
  "account": "current contract liabilities (customer advances) against revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:contract_liabilities_over_revenue:2025-06-28..2026-06-26" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend_cell",
  "what_changed": "days_sales_of_inventory for the year is 91.00788672340356. The year-over-year change against years-back-1 is 20.651596690675447. Inputs: inventory 1021235000, cost of revenue 4084586000. It sits second highest of the 5 filled years; years-back-1 sat second lowest at 70.35629003272811.",
  "account": "inventory days",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:days_sales_of_inventory:2025-06-28..2026-06-26" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend_cell",
  "what_changed": "days_sales_outstanding for the year is 79.836213722747. The year-over-year change against years-back-1 is -0.9508581191680889. Inputs: receivables 1017933000, revenue 4641097000. It sits second highest of the 5 filled years; years-back-1 was the highest at 80.7870718419151.",
  "account": "trade receivables days",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:days_sales_outstanding:2025-06-28..2026-06-26" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend_cell",
  "what_changed": "gross_margin for the year is 0.11990936625543487. The year-over-year change against years-back-1 is -0.0009767028452975224. Inputs: revenue 4641097000, cost of revenue 4084586000. It sits lowest of the 5 filled years; years-back-1 sat second lowest at 0.1208860691007324.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:gross_margin:2025-06-28..2026-06-26" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend_cell",
  "what_changed": "receivables_over_revenue for the year is 0.2193302574800742. The year-over-year change against years-back-1 is -0.0026122475801320932. Inputs: receivables 1017933000, revenue 4641097000. It sits second highest of the 5 filled years; years-back-1 was the highest at 0.2219425050602063.",
  "account": "trade receivables against revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:receivables_over_revenue:2025-06-28..2026-06-26" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend_cell",
  "what_changed": "soft_asset_share for the year is 0.7540814137497153. The year-over-year change against years-back-1 is -0.003262220142958072. Inputs: assets 3910961000, PP&E net 615067000, cash 346711000. It sits second highest of the 5 filled years.",
  "account": "assets other than PP&E and cash, as a share of total assets",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001408710-26-000028:trends:soft_asset_share:2025-06-28..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled for the year. It is unfilled in every period of the table (0 filled), so there is no value, no change and no position in history.",
  "account": "inventory valuation reserve against inventory",
  "expected_direction": "none",
  "horizon": "not assessable",
  "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-26: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001408710-26-000028:trends:inventory_reserve_ratio:2025-06-28..2026-06-26" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient: non_gaap_gap is not filled for the year, nor in any period of the table (0 filled). The table holds no non-GAAP figure. The 8-K release prints non-GAAP net income, but the table does not compute a gap from it, and I do not either.",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "not assessable",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001408710-26-000028:trends:non_gaap_gap:2025-06-28..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is not filled for the year, nor in any period of the table (0 filled). No warranty accrual balance concept is tagged.",
  "account": "warranty accrual against revenue",
  "expected_direction": "none",
  "horizon": "not assessable",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001408710-26-000028:trends:warranty_reserve_ratio:2025-06-28..2026-06-26" }
```

### Trend table — other cells

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient: accruals_over_total_assets is unfilled in quarters-back-1. Across the 8 quarters requested it is filled in only quarters-back-3 and quarters-back-7, which supports no quarterly trend.",
  "account": "accruals over total assets, quarterly",
  "expected_direction": "none",
  "horizon": "not assessable",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2025-12-27..2026-03-27: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001408710-26-000028:trends:accruals_over_total_assets:2025-12-27..2026-03-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_filled_quarter_cell",
  "what_changed": "In quarters-back-1 (2025-12-27..2026-03-27), contract_liabilities_over_revenue is 0.04844547403303816. The quarter-over-quarter change is 0.03305207239051039 and the year-over-year change is 0.038208022510382134. Contract liabilities input: 58827000. It sits highest of the 6 filled quarters. The year-end balance in the 10-K is 4237000 (see the contract liability fact item). Whether this is a fourth-quarter drawdown cannot be shown, because no fourth-quarter cell exists.",
  "account": "current contract liabilities (customer advances)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-27; read over the next 2 quarters",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001408710-26-000028:trends:contract_liabilities_over_revenue:2025-12-27..2026-03-27" }
```

### Numeric facts — 10-K 0001408710-26-000028

```json
{ "id": "earnings_quality_non_marketable_equity_upward_adjustment_fact",
  "what_changed": "The upward price adjustment on equity securities without a readily determinable fair value is 56743000 for fiscal 2026. Fiscal 2025 and fiscal 2024 print 0. The same filing tags the holding at 89103000 at 2026-06-26, against 0 at 2025-06-27, and an ownership percentage of 0.138 in Raytek Semiconductor.",
  "account": "non-marketable equity securities revaluation gain (other income)",
  "expected_direction": "up",
  "horizon": "fiscal 2026; non-recurring in nature, read over the next 4 quarters",
  "quote": "\"value\": \"56743000\"",
  "paragraph_id": "0001408710-26-000028:facts:EquitySecuritiesWithoutReadilyDeterminableFairValueUpwardPriceAdjustmentAnnualAmount:2025-06-28..2026-06-26" }
```

```json
{ "id": "earnings_quality_other_nonoperating_income_swing_fact",
  "what_changed": "Other non-operating income (expense) is 57026000 for fiscal 2026, against -178000 for fiscal 2025 and 287000 for fiscal 2024.",
  "account": "other income (expense), net",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"57026000\"",
  "paragraph_id": "0001408710-26-000028:facts:OtherNonoperatingIncomeExpense:2025-06-28..2026-06-26" }
```

```json
{ "id": "earnings_quality_income_tax_expense_rise_fact",
  "what_changed": "Income tax expense is 82086000 for fiscal 2026, against 22653000 for fiscal 2025 and 15173000 for fiscal 2024. Current tax expense is 84223000 (fiscal 2025: 27812000). Income taxes paid are 29405000 (fiscal 2025: 24302000).",
  "account": "income tax expense",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"value\": \"82086000\"",
  "paragraph_id": "0001408710-26-000028:facts:IncomeTaxExpenseBenefit:2025-06-28..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_fact",
  "what_changed": "The effective income tax rate for fiscal 2026 is 0.148. The same filing prints income before income taxes of 555113000 and income tax expense of 82086000 for the year. The facts I read carry no comparable annual rate for fiscal 2025 under this tag.",
  "account": "effective income tax rate",
  "expected_direction": "none",
  "horizon": "fiscal 2026; read over the next 4 quarters",
  "quote": "\"value\": \"0.148\"",
  "paragraph_id": "0001408710-26-000028:facts:EffectiveIncomeTaxRateContinuingOperations:2025-06-28..2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_income_tax_payable_rise_fact",
  "what_changed": "Accrued income taxes, current, are 63469000 at 2026-06-26, against 7939000 at 2025-06-27. The cash flow change in income tax payable is 55530000 for fiscal 2026, against 4029000.",
  "account": "income tax payable",
  "expected_direction": "up",
  "horizon": "next 4 quarters (cash settlement)",
  "quote": "\"value\": \"63469000\"",
  "paragraph_id": "0001408710-26-000028:facts:AccruedIncomeTaxesCurrent:2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_rise_fact",
  "what_changed": "Unrecognized tax benefits are 4446000 at 2026-06-26, against 1846000 at 2025-06-27 and 1249000 at 2024-06-28. Increases from current-period positions are 2600000 for fiscal 2026, against 620000.",
  "account": "unrecognized tax benefits",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"4446000\"",
  "paragraph_id": "0001408710-26-000028:facts:UnrecognizedTaxBenefits:2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_valuation_allowance_fact",
  "what_changed": "The deferred tax asset valuation allowance is 5568000 at 2026-06-26, against 3481000 at 2025-06-27, 3613000 at 2024-06-28 and 3824000 at 2023-06-30.",
  "account": "deferred tax asset valuation allowance",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"5568000\"",
  "paragraph_id": "0001408710-26-000028:facts:DeferredTaxAssetsValuationAllowance:2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_inventory_balance_build_fact",
  "what_changed": "Inventory, net, is 1021235000 at 2026-06-26, against 581015000 at 2025-06-27. Components at 2026-06-26: raw materials 374773000 (prior 145128000), work in process 568300000 (prior 377736000), finished goods 30967000 (prior 33016000), in transit 47195000 (prior 25135000).",
  "account": "inventories",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"1021235000\"",
  "paragraph_id": "0001408710-26-000028:facts:InventoryNet:2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_inventory_cash_absorption_fact",
  "what_changed": "The cash flow line for the increase in inventories is 442901000 for fiscal 2026, against 117809000 for fiscal 2025 and -56370000 for fiscal 2024.",
  "account": "change in inventories (operating cash flow)",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"442901000\"",
  "paragraph_id": "0001408710-26-000028:facts:IncreaseDecreaseInInventories:2025-06-28..2026-06-26" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_fact",
  "what_changed": "Inventory write-down is 2681000 for fiscal 2026, against 0 for fiscal 2025 and 0 for fiscal 2024. The release calls it 'Inventory obsolescence impairment'.",
  "account": "inventory obsolescence write-down",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"2681000\"",
  "paragraph_id": "0001408710-26-000028:facts:InventoryWriteDown:2025-06-28..2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_decline_fact",
  "what_changed": "Net cash provided by operating activities is 256725000 for fiscal 2026, against 328365000 for fiscal 2025 and 413146000 for fiscal 2024. Net income over the same years is 473027000, 332527000 and 296181000.",
  "account": "operating cash flow",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025; read over the next 4 quarters",
  "quote": "\"value\": \"256725000\"",
  "paragraph_id": "0001408710-26-000028:facts:NetCashProvidedByUsedInOperatingActivities:2025-06-28..2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_rise_fact",
  "what_changed": "Payments for property, plant and equipment are 252503000 for fiscal 2026, against 121078000 for fiscal 2025 and 47528000 for fiscal 2024. PP&E net is 615067000 at 2026-06-26, against 380640000.",
  "account": "capital expenditures",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"252503000\"",
  "paragraph_id": "0001408710-26-000028:facts:PaymentsToAcquirePropertyPlantAndEquipment:2025-06-28..2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_unpaid_capital_expenditure_rise_fact",
  "what_changed": "Capital expenditures incurred but not yet paid are 86018000 for fiscal 2026, against 40781000 for fiscal 2025 and 14380000 for fiscal 2024.",
  "account": "fixed assets payable (non-cash capex)",
  "expected_direction": "up",
  "horizon": "next 2 quarters (cash settlement)",
  "quote": "\"value\": \"86018000\"",
  "paragraph_id": "0001408710-26-000028:facts:CapitalExpendituresIncurredButNotYetPaid:2025-06-28..2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_trade_payables_rise_fact",
  "what_changed": "Trade accounts payable are 1005761000 at 2026-06-26, against 637417000 at 2025-06-27. The cash flow change in trade payables is 370753000 for fiscal 2026, against 194236000.",
  "account": "trade accounts payable",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"1005761000\"",
  "paragraph_id": "0001408710-26-000028:facts:AccountsPayableTradeCurrent:2026-06-26" }
```

```json
{ "id": "revenue_recognition_trade_receivables_balance_rise_fact",
  "what_changed": "Trade accounts receivable, net, are 1017933000 at 2026-06-26, against 758894000 at 2025-06-27. Gross receivables are 1018983000, against 760238000. The cash flow change in receivables is 259258000 for fiscal 2026, against 165657000.",
  "account": "trade accounts receivable",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"1017933000\"",
  "paragraph_id": "0001408710-26-000028:facts:AccountsReceivableNetCurrent:2026-06-26" }
```

```json
{ "id": "revenue_recognition_contract_liability_balance_drop_fact",
  "what_changed": "Current contract liabilities are 4237000 at 2026-06-26, against 14467000 at 2025-06-27, 7846000 at 2024-06-28 and 3036000 at 2023-06-30. The trend table's quarters-back-1 input prints 58827000 at 2026-03-27.",
  "account": "current contract liabilities",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"4237000\"",
  "paragraph_id": "0001408710-26-000028:facts:ContractWithCustomerLiabilityCurrent:2026-06-26" }
```

```json
{ "id": "earnings_quality_other_current_assets_rise_fact",
  "what_changed": "Other current assets are 195571000 at 2026-06-26, against 116210000 at 2025-06-27. The cash flow line for other current and non-current assets is 108114000 for fiscal 2026, against 33595000.",
  "account": "other current assets",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"195571000\"",
  "paragraph_id": "0001408710-26-000028:facts:OtherAssetsCurrent:2026-06-26" }
```

```json
{ "id": "earnings_quality_other_noncurrent_assets_rise_fact",
  "what_changed": "Other non-current assets are 20717000 at 2026-06-26, against 623000 at 2025-06-27.",
  "account": "other non-current assets",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"20717000\"",
  "paragraph_id": "0001408710-26-000028:facts:OtherAssetsNoncurrent:2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_other_current_liabilities_rise_fact",
  "what_changed": "Other current liabilities (other payables in the release) are 157470000 at 2026-06-26, against 66717000 at 2025-06-27. Accrued liabilities, current, are 56549000, against 30630000.",
  "account": "other current liabilities",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"157470000\"",
  "paragraph_id": "0001408710-26-000028:facts:OtherLiabilitiesCurrent:2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_short_term_investments_decline_fact",
  "what_changed": "Short-term investments are 528344000 at 2026-06-26, against 627819000 at 2025-06-27. Cash and cash equivalents are 346711000, against 306425000.",
  "account": "short-term investments",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"528344000\"",
  "paragraph_id": "0001408710-26-000028:facts:ShortTermInvestments:2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_derivative_liabilities_rise_fact",
  "what_changed": "Current derivative liabilities are 9084000 at 2026-06-26, against 105000 at 2025-06-27. Current derivative assets are 0, against 2961000. Cash flow hedge OCI before reclassification is -11837000 for fiscal 2026, against 5075000.",
  "account": "foreign exchange forward contracts (derivative liabilities)",
  "expected_direction": "up",
  "horizon": "next 4 quarters (reclassification into cost of revenue)",
  "quote": "\"value\": \"9084000\"",
  "paragraph_id": "0001408710-26-000028:facts:DerivativeLiabilitiesCurrent:2026-06-26" }
```

```json
{ "id": "liquidity_and_capital_inventory_purchase_obligations_fact",
  "what_changed": "Unrecorded purchase obligations for inventories are 3150000000 at 2026-06-26. The Q3 10-Q (0001408710-26-000016) tagged 2740000000 at 2026-03-27.",
  "account": "inventory purchase obligations",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"3150000000\"",
  "paragraph_id": "0001408710-26-000028:facts:PurchaseObligation:2026-06-26:us-gaap:UnrecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:InventoriesMember" }
```

```json
{ "id": "revenue_recognition_customer_warrant_issued_fact",
  "what_changed": "The additional paid-in capital adjustment for warrants issued is 4800000 for fiscal 2026, against 4109000 for fiscal 2025. Warrants outstanding are 85942 at 2026-06-26, against 38192 at 2025-06-27. The release labels the cash flow add-back 'Customer warrant'.",
  "account": "customer warrant (equity-classified, tied to a customer)",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"4800000\"",
  "paragraph_id": "0001408710-26-000028:facts:AdjustmentsToAdditionalPaidInCapitalWarrantIssued:2025-06-28..2026-06-26" }
```

```json
{ "id": "revenue_recognition_customer_concentration_nvidia_fact",
  "what_changed": "NVIDIA's share of net sales is 0.163 for fiscal 2026, against 0.276 for fiscal 2025 and 0.351 for fiscal 2024. NVIDIA's share of receivables prints 0.255 for fiscal 2025; this 10-K tags no fiscal 2026 receivables share for NVIDIA.",
  "account": "customer concentration, revenue",
  "expected_direction": "down",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"0.163\"",
  "paragraph_id": "0001408710-26-000028:facts:ConcentrationRiskPercentage1:2025-06-28..2026-06-26:srt:MajorCustomersAxis=fn:NvidiaCorporationMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_customer_concentration_cisco_fact",
  "what_changed": "Cisco's share of net sales is 0.199 for fiscal 2026, against 0.182 for fiscal 2025 and 0.134 for fiscal 2024. Cisco's share of receivables is 0.161, against 0.137.",
  "account": "customer concentration, revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2026 against fiscal 2025",
  "quote": "\"value\": \"0.199\"",
  "paragraph_id": "0001408710-26-000028:facts:ConcentrationRiskPercentage1:2025-06-28..2026-06-26:srt:MajorCustomersAxis=fn:CiscoSystemsIncMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_customer_concentration_nokia_fact",
  "what_changed": "Nokia's share of net sales is 0.107 for fiscal 2026; this 10-K tags no prior-year revenue share for Nokia. Nokia's share of receivables is 0.142, against 0.120.",
  "account": "customer concentration, revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "\"value\": \"0.107\"",
  "paragraph_id": "0001408710-26-000028:facts:ConcentrationRiskPercentage1:2025-06-28..2026-06-26:srt:MajorCustomersAxis=fn:NokiaCorporationMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_customer_concentration_amazon_fact",
  "what_changed": "Amazon's share of net sales is 0.105 for fiscal 2026; this 10-K tags no prior-year revenue share for Amazon. Amazon's share of receivables is 0.115.",
  "account": "customer concentration, revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "\"value\": \"0.105\"",
  "paragraph_id": "0001408710-26-000028:facts:ConcentrationRiskPercentage1:2025-06-28..2026-06-26:srt:MajorCustomersAxis=fn:Amazon.comInc.Member,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_term_loan_proceeds_fact",
  "what_changed": "As a subsequent event dated 2026-08-17, proceeds from long-term lines of credit with Bank of Ayudhya are 75000000.0 (THB 2500000000). Facility capacity is THB 2610000000 (USD 78300000), plus a USD 100000000.0 capacity. The 2023 credit facility balance is 0 at 2026-06-26.",
  "account": "long-term borrowings (Thai bank facility)",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"75000000.0\"",
  "paragraph_id": "0001408710-26-000028:facts:ProceedsFromLongTermLinesOfCredit:2026-08-17..2026-08-17:us-gaap:LineOfCreditFacilityAxis=fn:BankOfAyudhyaPublicCompanyLimitedMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember,us-gaap:TypeOfArrangementAxis=fn:CreditFacilityAgreementMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_us_facility_acquisition_fact",
  "what_changed": "As a subsequent event dated 2026-07-27, consideration transferred for an asset acquisition of a manufacturing facility in the United States is 76900000.",
  "account": "asset acquisition (manufacturing facility)",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "\"value\": \"76900000\"",
  "paragraph_id": "0001408710-26-000028:facts:AssetAcquisitionConsiderationTransferred:2026-07-27..2026-07-27:srt:StatementGeographicalAxis=country:US,us-gaap:AssetAcquisitionAxis=fn:ManfacturingFacilityMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_litigation_damages_sought_fact",
  "what_changed": "Damages sought in the Ngan In Leng and First Laser Limited case are CNY 400000000, tagged at 2024-06-28. My input holds no accrual tied to this case, and I do not infer one.",
  "account": "loss contingency (damages sought)",
  "expected_direction": "none",
  "horizon": "unresolved; no date in input",
  "quote": "\"value\": \"400000000\"",
  "paragraph_id": "0001408710-26-000028:facts:LossContingencyDamagesSoughtValue:2024-06-28..2024-06-28:srt:LitigationCaseAxis=fn:NganInLengAndFirstLaserLimitedMember:unit=iso4217:CNY" }
```

### 8-K earnings release — 0001408710-26-000026, statement tables and highlights

```json
{ "id": "results_against_expectations_fourth_quarter_revenue_release",
  "what_changed": "The release reports fourth-quarter revenue of $1,315.8 million, against $909.7 million a year earlier. It says the figure exceeded the guidance range, but the prior guidance range is not in my input, so the 'exceeds guidance' claim cannot be checked here.",
  "account": "revenue, fourth quarter",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-26",
  "quote": "Revenue for the fourth quarter of fiscal year 2026 was $1,315.8 million, compared to $909.7 million for the fourth quarter of fiscal year 2025.",
  "paragraph_id": "0001408710-26-000026:8k_2_02:11" }
```

```json
{ "id": "earnings_quality_pillar_two_tax_provision_release_table",
  "what_changed": "The release's non-GAAP reconciliation adds back a Pillar Two tax provision of 57,447 (thousands) for both the three months and the year ended 2026-06-26, or 1.58 per diluted share. The prior-year columns print a dash.",
  "account": "income tax expense (OECD Pillar Two)",
  "expected_direction": "up",
  "horizon": "quarter and year ended 2026-06-26; continuing per guidance",
  "quote": "Tax provision related to Pillar Two | 57,447",
  "paragraph_id": "0001408710-26-000026:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_non_marketable_equity_revaluation_release_table",
  "what_changed": "The release's non-GAAP reconciliation removes a non-marketable equity securities revaluation of (56,743) (thousands), or (1.56) per diluted share, from both the fourth quarter and the year. The prior-year columns print a dash. In GAAP net income this gain sits beside the Pillar Two provision of 57,447.",
  "account": "other income — non-marketable equity revaluation",
  "expected_direction": "up",
  "horizon": "quarter and year ended 2026-06-26",
  "quote": "Non-marketable equity securities revaluation | (56,743)",
  "paragraph_id": "0001408710-26-000026:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_fourth_quarter_income_tax_expense_release_table",
  "what_changed": "Fourth-quarter income tax expense is (60,458) (thousands), against (6,029) a year earlier. Full-year income tax expense is (82,086), against (22,653).",
  "account": "income tax expense, fourth quarter",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-26",
  "quote": "Income tax expense | (60,458)",
  "paragraph_id": "0001408710-26-000026:8k_2_02:50" }
```

```json
{ "id": "earnings_quality_fourth_quarter_other_income_release_table",
  "what_changed": "Fourth-quarter other income (expense), net is 57,377 (thousands), against (67) a year earlier. The full year is 57,026, against (178).",
  "account": "other income (expense), net, fourth quarter",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-26",
  "quote": "Other income (expense), net | 57,377",
  "paragraph_id": "0001408710-26-000026:8k_2_02:50" }
```

```json
{ "id": "liquidity_and_capital_fourth_quarter_operating_cash_flow_release_table",
  "what_changed": "Fourth-quarter net cash provided by operating activities is 54,967 (thousands), against 55,093 a year earlier. The full year is 256,725, against 328,365.",
  "account": "operating cash flow, fourth quarter",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-26",
  "quote": "Net cash provided by operating activities |  | $ | 54,967",
  "paragraph_id": "0001408710-26-000026:8k_2_02:69" }
```

```json
{ "id": "liquidity_and_capital_fourth_quarter_free_cash_flow_negative_release_table",
  "what_changed": "Fourth-quarter non-GAAP free cash flow is (36,902) (thousands), against 4,683 a year earlier. Full-year free cash flow is 4,222, against 207,287. Fourth-quarter purchases of PP&E are (91,869), against (50,410).",
  "account": "free cash flow",
  "expected_direction": "down",
  "horizon": "quarter and year ended 2026-06-26",
  "quote": "Non-GAAP free cash flow |  | $ | (36,902)",
  "paragraph_id": "0001408710-26-000026:8k_2_02:69" }
```

```json
{ "id": "results_against_expectations_first_quarter_revenue_guidance_release",
  "what_changed": "Guidance for the quarter ending 2026-09-25 is revenue of $1.375 billion to $1.425 billion. GAAP diluted EPS guidance is $3.39 to $3.54 and non-GAAP is $4.10 to $4.25, on about 36.3 million diluted shares.",
  "account": "revenue guidance, next quarter",
  "expected_direction": "none",
  "horizon": "quarter ending 2026-09-25",
  "quote": "Fabrinet expects first quarter revenue to be in the range of $1.375 billion to $1.425 billion.",
  "paragraph_id": "0001408710-26-000026:8k_2_02:27" }
```

```json
{ "id": "results_against_expectations_guidance_pillar_two_add_back_release_table",
  "what_changed": "The guidance reconciliation for the quarter ending 2026-09-25 adds back a Pillar Two tax provision of 0.40 per diluted share. Total reconciling items are 0.71.",
  "account": "income tax expense (OECD Pillar Two), guided",
  "expected_direction": "up",
  "horizon": "quarter ending 2026-09-25",
  "quote": "Tax provision related to Pillar Two | 0.40",
  "paragraph_id": "0001408710-26-000026:8k_2_02:73" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_term_loan_agreement_release_text",
  "what_changed": "Under Item 1.01, a Thai subsidiary borrowed a THB 2.50 billion (about $75.0 million) term loan on 2026-08-17. The loan is guaranteed by the company, and the proceeds support capital expenditures. The same filing amends the facility to THB 2.61 billion plus $100.0 million.",
  "account": "term loan borrowing",
  "expected_direction": "up",
  "horizon": "next 4 quarters",
  "quote": "the Borrower borrowed a term loan in the original principal amount of THB 2.50 billion (approximately $75.0 million based on the applicable exchange rate as of August 17, 2026)",
  "paragraph_id": "0001408710-26-000026:8k_body:3" }
```

## Seen in the notes

My input marks no fact as sitting inside a note. No record in input_numbers.json carries a field saying where its element sat when it was extracted, and I do not judge placement myself. So nothing is listed under this heading. Every fact item above is filed under the statements heading only because no note mark exists; that is not a judgment about where the element sat.
