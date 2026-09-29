Numbers reader: STX (Seagate Technology Holdings plc), filing 0001137789-26-000159 (10-K for the fiscal year ended 2026-07-03, filed 2026-08-04). Earnings release: 8-K 0001137789-26-000153 (filed 2026-07-28).

What my directory holds, and what it does not:

- Present: input_8k.md, input_numbers.json, input_prior_predictions.md, input_trends.json.
- Not present: the articulation checks, the restatement traces and the fourth-quarter derivation. Because there are no articulation checks, I report no articulation gap. None exists in my input. Because there are no restatement traces, I report no restated prior value. In input_numbers.json some facts carry a "superseded_by" field, which names a later filing that reported the same context. No fact prints an earlier value that differs, so nothing in my input says a period was reported differently. No row anywhere in my input says a period rests on a different concept, so I report no change of tag. The facts' taxonomy namespace differs by document (us-gaap/2024 in the January 10-Q, us-gaap/2025 in the April 10-Q, us-gaap/2026 in the 10-K). That is the taxonomy year, not a change of concept.
- Prior flags: input_prior_predictions.md says "None on record."
- Nothing forbidden is in my directory: no prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome window. One market-derived figure appears among the 10-K's cover-page facts: dei:EntityPublicFloat, which is a filed fact. I did not use it.
- A period the record does not reach: quarters-back-0 (target end 2026-07-03, the fiscal fourth quarter) has no cells at all. The reason it gives: "no quarter ending within 20 days of 2026-07-03 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The output of that derivation is not in my directory. So no fourth-quarter metric, change or position in history exists in my input. quarters-back-4 (target end 2025-07-04) has no cells for the same reason. The only fourth-quarter figures I have are the ones the 8-K prints; they are listed as items below.
- A formula baseline I cannot quote: the trend table's research-and-development-capitalized block for years-back-0 prints earnings_with_rnd_capitalized 3135200000.0, book_value_with_rnd_capitalized 4400600000.0, research_and_development_asset 2233600000.0 and research_and_development_amortization 803800000.0. Its capitalized_development_cost is missing: "the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period". None of these rows prints a paragraph_id, so none of them becomes an item. Only its research-and-development expense input, which is also a numeric fact with its own paragraph_id, is quoted below.
- How much I read: I read input_8k.md, input_prior_predictions.md and input_trends.json in full. input_numbers.json is 60,156 lines (about 2 MB) of XBRL facts, and I had no search tool. I read these lines of it: 1–10,749 (the January 10-Q facts through its debt note); probes at 20,000, 30,000 and 33,000; 34,400–38,099 (the end of the April 10-Q facts and the start of the 10-K facts: cover, balance sheet, income statement, comprehensive income and the start of the cash flow statement); and 60,000–60,156 (the end of the 10-K facts). About 44,000 lines were not read: 10,750–34,399 (the rest of the January 10-Q and nearly all of the April 10-Q) and 38,100–59,999 (the rest of the 10-K's cash flow, equity and note facts). Facts in those ranges may hold things this report does not list, for example a 2026-07-03 value for the receivables allowance, the noncurrent contract liability or the supplier-finance obligation. Every fact I read has the same fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and sometimes superseded_by.
- Conventions: "expected_direction" is the sign of the change my input prints for the item. For trend cells it is the year-over-year change. For a pair of filed facts or release figures it is the direction from the earlier printed figure to the later one. It is "none" where no change is printed. "horizon" names the two periods being compared.
- The notes split: my input marks no fact as sitting inside a note (no fact carries such a field). So I have placed nothing under "Seen in the notes" by my own judgment. Every fact item is listed under the statements heading with its own paragraph_id.

## Seen in the statements

Trend table, years-back-0 (fiscal year 2025-06-28..2026-07-03; 371 days, against 364 for years-back-1):

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "Accruals over total assets for fiscal 2026 (net income minus operating cash flow, over assets) is -0.04913758523866827. Its year-over-year change against years-back-1 is -0.09724926416176437. It is the third highest of the 5 filled years. Inputs as printed: net income 3184000000.0, operating cash flow 3674000000.0, assets 9972000000.0, all from 0001137789-26-000159. years-back-1 printed 0.0481116789230961 (highest of the 5 filled years).",
  "account": "net income less net cash provided by operating activities, over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:accruals_over_total_assets:2025-06-28..2026-07-03" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "insufficient. The table has no bad-debt reserve ratio for fiscal 2026: the allowance concepts are in the record, but not for 2026-07-03. No fiscal 2026 value, change or position exists. The last filled year, years-back-1, printed 0.004153686396677051 (second lowest of the 4 filled years).",
  "account": "allowance for doubtful accounts over gross receivables",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-07-03",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-07-03: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001137789-26-000159:trends:bad_debt_reserve_ratio:2025-06-28..2026-07-03" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "insufficient. The table has no contract-liabilities ratio in any period: the companyfacts record tags none of the four current or total contract-liability and deferred-revenue concepts it searches. No value, change or position exists. See the separate fact item: the company does tag the noncurrent contract-liability concept.",
  "account": "contract liabilities (deferred revenue) over revenue",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-07-03",
  "quote": "\"missing\": \"no row for contract_liabilities: the companyfacts record tags none of us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001137789-26-000159:trends:contract_liabilities_over_revenue:2025-06-28..2026-07-03" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_annual",
  "what_changed": "Days sales of inventory for fiscal 2026 is 87.81693536236251. Its year-over-year change against years-back-1 is -1.0689388109459514. It is the third highest of the 5 filled years. Inputs as printed: inventory 1571000000.0 at 2026-07-03, cost of revenue 6637000000.0. The period is 371 days, against 364 for years-back-1.",
  "account": "inventories, net, against cost of revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:days_sales_of_inventory:2025-06-28..2026-07-03" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "Days sales outstanding for fiscal 2026 is 46.667814678146776. Its year-over-year change against years-back-1 is 8.295164353864045. It is the second highest of the 5 filled years. Inputs as printed: receivables 1534000000.0 at 2026-07-03, revenue 12195000000.0. The period is 371 days, against 364 for years-back-1. years-back-1 printed 38.37265032428273.",
  "account": "accounts receivable, net, against revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:days_sales_outstanding:2025-06-28..2026-07-03" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "Gross margin for fiscal 2026 is 0.45576055760557604. Its year-over-year change against years-back-1 is 0.10399623969857374. It is the highest of the 5 filled years. Inputs as printed: revenue 12195000000.0, cost of revenue 6637000000.0.",
  "account": "revenue less cost of revenue, over revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:gross_margin:2025-06-28..2026-07-03" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "insufficient. The table has no inventory-reserve ratio in any period: the companyfacts record tags no us-gaap:InventoryValuationReserves. No value, change or position exists.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-07-03",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001137789-26-000159:trends:inventory_reserve_ratio:2025-06-28..2026-07-03" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual",
  "what_changed": "insufficient. The table has no non-GAAP gap in any period, because companyfacts holds no non-GAAP measure. No value, change or position exists. The 8-K prints GAAP and non-GAAP net income side by side (separate item). The gap between them is not printed anywhere in my input.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-07-03",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001137789-26-000159:trends:non_gaap_gap:2025-06-28..2026-07-03" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "Receivables over revenue for fiscal 2026 is 0.12578925789257892. Its year-over-year change against years-back-1 is 0.02036988886982416. It is the second highest of the 5 filled years. Inputs as printed: receivables 1534000000.0 at 2026-07-03, revenue 12195000000.0. years-back-1 printed 0.10541936902275476.",
  "account": "accounts receivable, net, over revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:receivables_over_revenue:2025-06-28..2026-07-03" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "Soft-asset share (assets less property, plant and equipment and cash, over assets) for fiscal 2026 is 0.6251504211793021. Its year-over-year change against years-back-1 is -0.0572626412661672. It is the second lowest of the 5 filled years. Inputs as printed: assets 9972000000.0, property, plant and equipment 2034000000.0, cash 1704000000.0. years-back-1 printed 0.6824130624454693 (highest of the 5 filled years).",
  "account": "total assets other than property, plant and equipment and cash, over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:soft_asset_share:2025-06-28..2026-07-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "Warranty reserve ratio (warranty accrual over revenue) for fiscal 2026 is 0.016236162361623615. Its year-over-year change against years-back-1 is 0.0011762525012300792. It is the third highest of the 5 filled years. Inputs as printed: standard product warranty accrual 198000000.0 at 2026-07-03, revenue 12195000000.0. The years-back-1 accrual input is 137000000.0. Annual cells divide by a full year's revenue and quarterly cells by a quarter's, so the two rows are not on the same base.",
  "account": "standard product warranty accrual over revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001137789-26-000159:trends:warranty_reserve_ratio:2025-06-28..2026-07-03" }
```

Trend table, quarters-back-1 (2026-01-03..2026-04-03, the fiscal third quarter). This is the latest quarter the table fills; the fiscal fourth quarter has no cells (see above):

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "insufficient. The table has no accruals ratio for the fiscal third quarter: operating cash flow is in the record, but not for this three-month period. Across all quarters the table fills this metric in only 2 quarters, which cannot support a trend claim.",
  "account": "net income less net cash provided by operating activities, over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-03",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-03..2026-04-03: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001137789-26-000159:trends:accruals_over_total_assets:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "insufficient. The table has no bad-debt reserve ratio for the fiscal third quarter: the allowance concepts are in the record, but not for 2026-04-03. It fills this metric in no quarter at all.",
  "account": "allowance for doubtful accounts over gross receivables",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-03",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-04-03: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001137789-26-000159:trends:bad_debt_reserve_ratio:2026-01-03..2026-04-03" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "insufficient. The table has no contract-liabilities ratio for the fiscal third quarter or any other period: none of the four searched concepts is tagged.",
  "account": "contract liabilities (deferred revenue) over revenue",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-03",
  "quote": "\"missing\": \"no row for contract_liabilities: the companyfacts record tags none of us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001137789-26-000159:trends:contract_liabilities_over_revenue:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_quarterly",
  "what_changed": "Days sales of inventory for the fiscal third quarter is 83.62162162162163. The quarter-over-quarter change against quarters-back-2 is 0.9545506695294534. The year-over-year change against quarters-back-5 is -12.058378378378364. It is the second lowest of the 6 filled quarters. Inputs as printed: inventory 1530000000.0 at 2026-04-03, cost of revenue 1665000000.0, 91 days.",
  "account": "inventories, net, against cost of revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-04-03 against quarter ended 2025-03-28 (year over year) and quarter ended 2026-01-02 (sequential)",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001137789-26-000159:trends:days_sales_of_inventory:2026-01-03..2026-04-03" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "Days sales outstanding for the fiscal third quarter is 35.00224935732648. The quarter-over-quarter change against quarters-back-2 is -5.13438781081512. The year-over-year change against quarters-back-5 is 8.797619727696848. It is the third highest of the 6 filled quarters. Inputs as printed: receivables 1197000000.0 at 2026-04-03, revenue 3112000000.0, 91 days. quarters-back-2 printed 40.1366371681416 (highest of the 6 filled quarters).",
  "account": "accounts receivable, net, against revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-04-03 against quarter ended 2025-03-28 (year over year) and quarter ended 2026-01-02 (sequential)",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001137789-26-000159:trends:days_sales_outstanding:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "Gross margin for the fiscal third quarter is 0.46497429305912596. The quarter-over-quarter change against quarters-back-2 is 0.04869110721841802. The year-over-year change against quarters-back-5 is 0.1131224412072741. It is the highest of the 6 filled quarters. Inputs as printed: revenue 3112000000.0, cost of revenue 1665000000.0.",
  "account": "revenue less cost of revenue, over revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-04-03 against quarter ended 2025-03-28 (year over year) and quarter ended 2026-01-02 (sequential)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001137789-26-000159:trends:gross_margin:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
  "what_changed": "insufficient. The table has no inventory-reserve ratio for the fiscal third quarter or any other period: us-gaap:InventoryValuationReserves is not tagged.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-03",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001137789-26-000159:trends:inventory_reserve_ratio:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly",
  "what_changed": "insufficient. The table has no non-GAAP gap for the fiscal third quarter or any other period, because companyfacts holds no non-GAAP measure.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-04-03",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001137789-26-000159:trends:non_gaap_gap:2026-01-03..2026-04-03" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "Receivables over revenue for the fiscal third quarter is 0.3846401028277635. The quarter-over-quarter change against quarters-back-2 is -0.05642184407489137. The year-over-year change against quarters-back-5 is 0.09667713986480053. It is the third highest of the 6 filled quarters. Inputs as printed: receivables 1197000000.0 at 2026-04-03, revenue 3112000000.0.",
  "account": "accounts receivable, net, over revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-04-03 against quarter ended 2025-03-28 (year over year) and quarter ended 2026-01-02 (sequential)",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0001137789-26-000159:trends:receivables_over_revenue:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "Soft-asset share for the fiscal third quarter is 0.6628430049482681. The quarter-over-quarter change against quarters-back-2 is -0.01366135885513109. The year-over-year change against quarters-back-5 is -0.016295017262202616. It is the third lowest of the 6 filled quarters. Inputs as printed: assets 8892000000.0, property, plant and equipment 1852000000.0, cash 1146000000.0, all at 2026-04-03.",
  "account": "total assets other than property, plant and equipment and cash, over total assets",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-04-03 against quarter ended 2025-03-28 (year over year) and quarter ended 2026-01-02 (sequential)",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001137789-26-000159:trends:soft_asset_share:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
  "what_changed": "Warranty reserve ratio (warranty accrual over quarterly revenue) for the fiscal third quarter is 0.057519280205655526. The quarter-over-quarter change against quarters-back-2 is 0.0008821120640626068. The year-over-year change against quarters-back-5 is -0.00451775683138151. It is the third lowest of the 6 filled quarters. Inputs as printed: standard product warranty accrual 179000000.0 at 2026-04-03, revenue 3112000000.0.",
  "account": "standard product warranty accrual over revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-04-03 against quarter ended 2025-03-28 (year over year) and quarter ended 2026-01-02 (sequential)",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001137789-26-000159:trends:warranty_reserve_ratio:2026-01-03..2026-04-03" }
```

Numeric facts (input_numbers.json; none carries a note marker):

```json
{ "id": "earnings_quality_research_and_development_expense",
  "what_changed": "The 10-K reports research and development expense of 755000000 for fiscal 2026, against 724000000 for fiscal 2025 (the trend table's baseline input from the same filing). This is the only row of the trend table's R&D-capitalized baseline that carries a paragraph_id. The baseline's capitalized development cost is missing because us-gaap:CapitalizedComputerSoftwareAdditions is not tagged.",
  "account": "research and development expense (product development)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"value\": \"755000000\"",
  "paragraph_id": "0001137789-26-000159:facts:ResearchAndDevelopmentExpense:2025-06-28..2026-07-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_noncurrent",
  "what_changed": "The 10-K reports a noncurrent product warranty accrual of 125000000 at 2026-07-03, against 77000000 at 2025-06-27. The current warranty accrual is 73000000, against 60000000. The January 10-Q reported 94000000 noncurrent and 66000000 current at 2026-01-02.",
  "account": "product warranty accrual, noncurrent",
  "expected_direction": "up",
  "horizon": "balance at 2026-07-03 against balance at 2025-06-27",
  "quote": "\"value\": \"125000000\"",
  "paragraph_id": "0001137789-26-000159:facts:ProductWarrantyAccrualNoncurrent:2026-07-03" }
```

```json
{ "id": "revenue_recognition_contract_liability_noncurrent_tagged",
  "what_changed": "The January 10-Q tags us-gaap:ContractWithCustomerLiabilityNoncurrent at 200000000 at 2026-01-02, against 211000000 at 2025-06-27. The 2025-06-27 fact carries superseded_by 0001137789-26-000159, so the 10-K also reports that context. This concept is not among the four the trend table searched, which is why the table's contract-liabilities ratio is insufficient. No 2026-07-03 value exists in the portion of input_numbers.json I read.",
  "account": "contract liabilities, noncurrent",
  "expected_direction": "down",
  "horizon": "balance at 2026-01-02 against balance at 2025-06-27",
  "quote": "\"value\": \"200000000\"",
  "paragraph_id": "0001137789-26-000026:facts:ContractWithCustomerLiabilityNoncurrent:2026-01-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_charge",
  "what_changed": "The 10-K reports a loss contingency loss of 105000000 for fiscal 2026, against 0 for fiscal 2025 and 0 for fiscal 2024. The 8-K presents it as a legal settlement of 105 (in millions) in fiscal 2026.",
  "account": "loss contingency, loss in period (legal settlement)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"value\": \"105000000\"",
  "paragraph_id": "0001137789-26-000159:facts:LossContingencyLossInPeriod:2025-06-28..2026-07-03" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_litigation_settlement_amount",
  "what_changed": "The April 10-Q reports a litigation settlement loss of 175000000 as of 2026-04-03, and a gain (loss) related to litigation settlement of -105000000 for the quarter 2026-01-03..2026-04-03. An earlier 10-Q period, 2024-06-29..2025-03-28, reports a loss contingency loss in period of 300000000.",
  "account": "litigation settlement",
  "expected_direction": "none",
  "horizon": "as of 2026-04-03",
  "quote": "\"value\": \"175000000\"",
  "paragraph_id": "0001137789-26-000088:facts:LitigationSettlementLoss:2026-04-03..2026-04-03" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_accrual",
  "what_changed": "The April 10-Q reports loss contingency accruals at 2026-04-03 of 90000000 in other noncurrent liabilities and 45000000 in accrued liabilities.",
  "account": "loss contingency accrual",
  "expected_direction": "none",
  "horizon": "balance at 2026-04-03",
  "quote": "\"value\": \"90000000\"",
  "paragraph_id": "0001137789-26-000088:facts:LossContingencyAccrualAtCarryingValue:2026-04-03:us-gaap:BalanceSheetLocationAxis=us-gaap:OtherNoncurrentLiabilitiesMember" }
```

```json
{ "id": "earnings_quality_loss_on_debt_extinguishment",
  "what_changed": "The 10-K reports gains (losses) on extinguishment of debt of -151000000 for fiscal 2026, against -7000000 for fiscal 2025 and -29000000 for fiscal 2024. The 8-K excludes this net loss from debt transactions from non-GAAP results.",
  "account": "gains (losses) on extinguishment of debt",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "\"value\": \"-151000000\"",
  "paragraph_id": "0001137789-26-000159:facts:GainsLossesOnExtinguishmentOfDebt:2025-06-28..2026-07-03" }
```

```json
{ "id": "earnings_quality_induced_conversion_expense",
  "what_changed": "The January 10-Q reports induced conversion expense of 61000000 on 2025-11-12 for the 3.50% exchangeable senior notes due June 2028. On that date 500000000 of principal was converted, and 4300000 shares were issued.",
  "account": "induced conversion of convertible debt expense",
  "expected_direction": "none",
  "horizon": "event on 2025-11-12",
  "quote": "\"value\": \"61000000\"",
  "paragraph_id": "0001137789-26-000026:facts:InducedConversionOfConvertibleDebtExpense:2025-11-12..2025-11-12:us-gaap:DebtInstrumentAxis=us-gaap:ConvertibleDebtMember,us-gaap:LongtermDebtTypeAxis=stx:ConvertibleSeniorNote350PercentDueJune2028Member" }
```

```json
{ "id": "liquidity_and_capital_current_portion_of_long_term_debt",
  "what_changed": "The 10-K reports a current portion of long-term debt of 185000000 at 2026-07-03, against 0 at 2025-06-27. The January 10-Q reported 998000000 at 2026-01-02.",
  "account": "long-term debt, current portion",
  "expected_direction": "up",
  "horizon": "balance at 2026-07-03 against balance at 2025-06-27",
  "quote": "\"value\": \"185000000\"",
  "paragraph_id": "0001137789-26-000159:facts:LongTermDebtCurrent:2026-07-03" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_noncurrent",
  "what_changed": "The 10-K reports long-term debt less current portion of 3380000000 at 2026-07-03, against 4995000000 at 2025-06-27.",
  "account": "long-term debt, noncurrent",
  "expected_direction": "down",
  "horizon": "balance at 2026-07-03 against balance at 2025-06-27",
  "quote": "\"value\": \"3380000000\"",
  "paragraph_id": "0001137789-26-000159:facts:LongTermDebtNoncurrent:2026-07-03" }
```

```json
{ "id": "liquidity_and_capital_stockholders_equity",
  "what_changed": "The 10-K reports total shareholders' equity of 2167000000 at 2026-07-03, against -453000000 at 2025-06-27.",
  "account": "total shareholders' equity (deficit)",
  "expected_direction": "up",
  "horizon": "balance at 2026-07-03 against balance at 2025-06-27",
  "quote": "\"value\": \"2167000000\"",
  "paragraph_id": "0001137789-26-000159:facts:StockholdersEquity:2026-07-03" }
```

```json
{ "id": "liquidity_and_capital_supplier_finance_program_obligation",
  "what_changed": "The January 10-Q reports a supplier finance program obligation of 44000000 at 2026-01-02, against 20000000 at 2025-06-27. No 2026-07-03 value exists in the portion of input_numbers.json I read.",
  "account": "supplier finance program obligation",
  "expected_direction": "up",
  "horizon": "balance at 2026-01-02 against balance at 2025-06-27",
  "quote": "\"value\": \"44000000\"",
  "paragraph_id": "0001137789-26-000026:facts:SupplierFinanceProgramObligation:2026-01-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_year_end",
  "what_changed": "The 10-K reports a subsequent-event dividend declared of 0.74 per share on 2026-07-28. The April 10-Q reported a subsequent-event dividend of 0.74 declared on 2026-04-28, so the rate is unchanged.",
  "account": "cash dividends declared per ordinary share",
  "expected_direction": "none",
  "horizon": "declaration on 2026-07-28 against declaration on 2026-04-28",
  "quote": "\"value\": \"0.74\"",
  "paragraph_id": "0001137789-26-000159:facts:CommonStockDividendsPerShareDeclared:2026-07-28..2026-07-28:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

Figures in the 8-K earnings release (these fill in where the trend table has no fourth-quarter cell and no non-GAAP row):

```json
{ "id": "across_documents_release_fourth_quarter_revenue",
  "what_changed": "The release prints revenue of 3,629 (in millions) for the fiscal fourth quarter of 2026, against 2,444 for the fiscal fourth quarter of 2025. The trend table has no fourth-quarter cell, so no position in the filed history is printed for this quarter.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-07-03 against quarter ended 2025-06-27",
  "quote": "| Revenue ($M) | $ | 3,629 |  | $ | 2,444 |  | $ | 3,629 |  | $ | 2,444 |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:27" }
```

```json
{ "id": "across_documents_release_fourth_quarter_gross_margin",
  "what_changed": "The release prints GAAP gross margin of 52.3% for the fiscal fourth quarter of 2026, against 37.4% a year earlier, and non-GAAP gross margin of 52.7% against 37.9%. The trend table has no fourth-quarter gross-margin cell. Its latest filled quarter, quarters-back-1, printed 0.46497429305912596 (highest of the 6 filled quarters). Where the fourth quarter sits in the filed history is not printed anywhere in my input.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-07-03 against quarter ended 2025-06-27",
  "quote": "| Gross Margin | 52.3% |  | 37.4% |  | 52.7% |  | 37.9% |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:27" }
```

```json
{ "id": "across_documents_release_fourth_quarter_net_income",
  "what_changed": "The release prints GAAP net income of 1,294 (in millions) for the fiscal fourth quarter of 2026, against 488 a year earlier, and non-GAAP net income of 1,319 against 556.",
  "account": "net income",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-07-03 against quarter ended 2025-06-27",
  "quote": "| Net Income ($M) | $ | 1,294 |  | $ | 488 |  | $ | 1,319 |  | $ | 556 |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:27" }
```

```json
{ "id": "across_documents_release_non_gaap_net_income_annual",
  "what_changed": "The release prints fiscal 2026 GAAP net income of 3,184 (in millions) and non-GAAP net income of 3,538; for fiscal 2025 the figures are 1,469 and 1,733. The trend table's non_gaap_gap is insufficient because companyfacts holds no non-GAAP measure. The gap between the two figures is not printed anywhere in my input, so I do not state it.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "| Net Income ($M) | $ | 3,184 |  | $ | 1,469 |  | $ | 3,538 |  | $ | 1,733 |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:29" }
```

```json
{ "id": "earnings_quality_release_income_tax_provision",
  "what_changed": "The release prints a provision for income taxes of 211 (in millions) for the fiscal fourth quarter of 2026, against 4 a year earlier, and 506 for fiscal 2026, against 44 for fiscal 2025. The 10-K facts agree for the years: 506000000 and 44000000.",
  "account": "provision for income taxes",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "| Provision for income taxes | 211 |  |  | 4 |  |  | 506 |  |  | 44 |  |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:59" }
```

```json
{ "id": "earnings_quality_release_accrued_expenses_cash_flow_change",
  "what_changed": "The release's cash flow statement prints the change in accrued expenses, income taxes and warranty as 528 (in millions) for fiscal 2026, against (155) for fiscal 2025. Net cash provided by operating activities is 3,674, against 1,083.",
  "account": "change in accrued expenses, income taxes and warranty (operating cash flow)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "| Accrued expenses, income taxes and warranty | 528 |  |  | (155) |  |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:63" }
```

```json
{ "id": "liquidity_and_capital_release_free_cash_flow",
  "what_changed": "The release prints free cash flow of 1,118 (in millions) for the fiscal fourth quarter of 2026, against 425 a year earlier, and 3,105 for fiscal 2026, against 818 for fiscal 2025. It also prints fourth-quarter operating cash flow of 1,305, against 508; the trend table has no quarterly operating-cash-flow cell for this quarter.",
  "account": "free cash flow (non-GAAP)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-07-03 against fiscal year ended 2025-06-27",
  "quote": "| Free Cash Flow |  | $ | 1,118 |  |  | $ | 425 |  |  | $ | 3,105 |  |  | $ | 818 |",
  "paragraph_id": "0001137789-26-000153:8k_2_02:82" }
```

```json
{ "id": "results_against_expectations_release_revenue_guidance",
  "what_changed": "The release guides fiscal first-quarter 2027 revenue to 4.1 billion, plus or minus 100 million. That is above the 3,629 million of fourth-quarter revenue the release prints.",
  "account": "revenue guidance",
  "expected_direction": "up",
  "horizon": "fiscal first quarter 2027 against quarter ended 2026-07-03",
  "quote": "•Revenue of $4.1 billion, plus or minus $100 million",
  "paragraph_id": "0001137789-26-000153:8k_2_02:37" }
```

```json
{ "id": "results_against_expectations_release_non_gaap_eps_guidance",
  "what_changed": "The release guides fiscal first-quarter 2027 non-GAAP diluted EPS to 7.30, plus or minus 0.20. That is above the fourth-quarter non-GAAP diluted EPS of 5.71 the release prints.",
  "account": "non-GAAP diluted EPS guidance",
  "expected_direction": "up",
  "horizon": "fiscal first quarter 2027 against quarter ended 2026-07-03",
  "quote": "•Non-GAAP diluted EPS of $7.30, plus or minus $0.20",
  "paragraph_id": "0001137789-26-000153:8k_2_02:38" }
```

## Seen in the notes

My input marks no fact as sitting inside a note: none of the facts I read carries a note field. So I have placed no item here. Every numeric-fact item above keeps its own paragraph_id, so a later split can re-sort them without re-deriving where they came from. I did not sort any fact into this section by my own judgment.
