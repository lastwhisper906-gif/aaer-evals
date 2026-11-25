# ANET — notes text reader — 10-Q 0001596532-26-000175 (period ended June 30, 2026)

## Input check

- Read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- No forbidden material found. There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no prior probability and no outcome window. The income statement, balance sheet and cash flow tables in input_8k.md are part of the exhibit 99.1 body of the 8-K. The MD&A tables are part of MD&A.
- Not in my directory: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report. input_controls.md is titled "controls and the auditor's report" but contains only Item 4, which is normal for a 10-Q. I make no finding about any of these.
- 8-K: only the Item 2.02 / 9.01 body (0001596532-26-000174, filed 2026-08-04) is present. The item-code list shows a 5.07 filed 2026-06-02, but its body is not in my input. Late-filing notifications: none.
- Prior predictions: none on record. There are no earlier flags to carry forward.
- MD&A paragraphs shown as text are marked changed against 0001596532-26-000078, but the earlier MD&A wording is not in my input. For those paragraphs, `what_changed` gives what the text now says and states that the added words cannot be isolated. Prior wording is available only for the note paragraphs in the note change history: notes:4, notes:19, notes:20, notes:60, notes:61, notes:63 and notes:68.
- I did no arithmetic. Where this report gives a current amount next to a prior one, it repeats what the prose says. Any comparison is for the numbers reader and the supervisors.

## Items

```json
{ "id": "liquidity_and_capital_purchase_commitments_receipt_timing",
  "what_changed": "The commitments paragraph now gives non-cancellable purchase commitments as of June 30, 2026: $9.7 billion in total, of which $9.4 billion is expected to be received within 12 months and $0.3 billion after 12 months. The prior paragraph (0001596532-26-000078:note_history:1) gave $8.9 billion, $7.6 billion and $1.3 billion as of March 31, 2026. I repeat both sets of figures and compare neither. MD&A (mdna:54) says in prose that the company has 'increased' its purchase commitments, and mdna:74 repeats the June figures. A scope sentence was dropped from this paragraph; that is a separate item.",
  "account": "inventories (off-balance-sheet purchase commitments)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "As of June 30, 2026, we had non-cancellable purchase commitments not recorded on our balance sheet of $9.7 billion, of which $9.4 billion have expected receipt dates within 12 months, and $0.3 billion have expected receipt dates greater than 12 months.",
  "paragraph_id": "0001596532-26-000175:notes:60",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_purchase_obligation_scope_sentence_removed",
  "what_changed": "This sentence was in the March 31, 2026 commitments paragraph and has been removed from the June 30, 2026 paragraph (notes:60). It is also absent from the MD&A version (mdna:74). The current text describes commitments only for finished goods and strategic components bought through contract manufacturers. It no longer says whether software and technology licenses, property and equipment, and other corporate goods and services are inside the stated total. Nothing in the prose says the two period totals are on the same basis.",
  "account": "purchase commitments (off-balance-sheet); inventories",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Our purchase obligations also encompass software and technology licenses, property and equipment, and other corporate goods and services.",
  "paragraph_id": "0001596532-26-000078:note_history:1",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_contract_manufacturer_deposits",
  "what_changed": "Deposits paid to contract manufacturers to secure purchase commitments are now stated as $124.4 million as of June 30, 2026. The prior paragraph (0001596532-26-000078:note_history:2) gave $95.5 million as of March 31, 2026. Both give $53.0 million at December 31, 2025. No cause is given. The deposits sit in prepaid expenses and other current assets and in other assets. The prose gives levels, not a direction.",
  "account": "prepaid expenses and other current assets; other assets",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "We also had deposits to our contract manufacturers to secure our purchase commitments in the amount of $124.4 million and $53.0 million as of June 30, 2026 and December 31, 2025, respectively",
  "paragraph_id": "0001596532-26-000175:notes:61",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_purchase_commitments_raised_for_memory_and_silicon_supply",
  "what_changed": "The liquidity paragraph is marked changed; the prior wording is not in my input. It now says the company has increased purchase commitments for three reasons: to respond to the rapid deployment of AI networks, to navigate tightening supply in the memory and silicon markets, and (mdna:55) to reduce overall lead times. It says this 'will increase our working capital requirements in the future'. It also says inventory and purchase commitments are expected to remain elevated and volatile as new product introductions ramp. Management gives a cause for the inventory and commitment level.",
  "account": "inventories; working capital; operating cash flow",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In particular, we have increased our purchase commitments to respond to the rapid deployment of AI networks, and to navigate the tightening supply within the memory and silicon markets",
  "paragraph_id": "0001596532-26-000175:mdna:54",
  "explanation": true }
```

```json
{ "id": "revenue_recognition_extended_payment_terms_large_customers",
  "what_changed": "The same marked-changed liquidity paragraph says certain large customer arrangements include extended payment terms. It says these may cause timing differences in working capital and operating cash flows. The prior wording is not in my input, so I cannot say whether this sentence is new this quarter. The receivables sentence in the operating cash flow narrative (mdna:59) attributes the receivable increase to billings and does not mention these terms.",
  "account": "accounts receivable",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Additionally, our working capital and operating cash flows may experience timing differences as a result of certain large customer arrangements that include extended payment terms.",
  "paragraph_id": "0001596532-26-000175:mdna:54",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_property_project_remaining_capex_range",
  "what_changed": "The Santa Clara building paragraph now estimates remaining capital expenditures at approximately $110.0 million to $135.0 million as of June 30, 2026. The prior paragraph (0001596532-26-000078:note_history:5; the history shows it as removed and the new one as added) gave approximately $130.0 million to $150.0 million as of March 31, 2026. Completion is still expected at the end of fiscal 2026. The text does not say whether the total project budget changed; answering that needs the quarter's capital spending, which is for the numbers reader. MD&A mdna:76 repeats the sentence, and mdna:54 refers to the 'ongoing construction'.",
  "account": "property and equipment, net (construction-in-process); purchases of property and equipment",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "As of June 30, 2026, the estimated remaining capital expenditures related to this project are expected to be approximately $110.0 million to $135.0 million through the end of fiscal 2026 when we expect construction to be completed.",
  "paragraph_id": "0001596532-26-000175:notes:63",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_no_share_repurchases_remaining_authorization",
  "what_changed": "The note says no shares were repurchased during the six months ended June 30, 2026. It gives $817.9 million remaining under the $1.5 billion program authorized in May 2025. The text gives no reason for the absence of repurchases. MD&A mdna:68 to mdna:69 says the same. The 2025 comparative financing narrative (mdna:66) describes open-market repurchases in that period.",
  "account": "repurchases of common stock (financing cash flow); stockholders' equity",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "We did not repurchase any shares during the six months ended June 30, 2026. As of June 30, 2026, the remaining authorized amount for repurchases under the Repurchase Program was $817.9 million.",
  "paragraph_id": "0001596532-26-000175:notes:70",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_financing_taxes_paid_under_repurchase_plans",
  "what_changed": "The financing narrative for the six months of 2026 says outflows included taxes paid under equity incentive plans and under stock repurchase plans. notes:70 and mdna:69 say no shares were repurchased in the period. The prose does not name the tax paid under the repurchase plans. The 8-K cash flow statement (0001596532-26-000174:8k_2_02:49) has an 'Other' financing line that no prose in my input describes.",
  "account": "cash used in financing activities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "consisting of proceeds from the issuance of stock under equity incentive plans, and offset by taxes paid under equity incentive and stock repurchase plans",
  "paragraph_id": "0001596532-26-000175:mdna:65",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_income_tax_payable_timing",
  "what_changed": "The operating cash flow narrative for the six months of 2026 attributes part of the working-capital inflow to an increase in income tax payables. It says the increase relates to the timing of payments. Because the prose calls it timing, it implies the payable reverses when the tax is paid.",
  "account": "income taxes payable; operating cash flow",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "a $198.4 million increase in income tax payables related to timing of payments",
  "paragraph_id": "0001596532-26-000175:mdna:59",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_acceptance_periods_and_evaluation_inventory_volatility",
  "what_changed": "The AI-demand paragraph is marked changed; the prior wording is not in my input. It says new product introductions and expanded AI use cases have led to more customer trials and more contracts with acceptance periods. It says this has increased the 'volatility and magnitude' of evaluation inventory and product deferred revenue. It also says that if trial or acceptance requirements are not met, the company may have to accept product returns, could not recognize revenue on those transactions, and may write down inventory. Management gives a cause for the evaluation inventory level.",
  "account": "inventories (evaluation inventory); deferred revenue (product)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "This has resulted in increased customer trials and contracts with acceptance periods, and an increase in the volatility and magnitude of our evaluation inventory and product deferred revenue balances, which in turn may create variability in our revenue results on a quarterly and annual basis.",
  "paragraph_id": "0001596532-26-000175:mdna:11",
  "explanation": true }
```

```json
{ "id": "narrative_signs_of_operating_pressure_ai_demand_forecasting_and_customer_purchase_shifts",
  "what_changed": "The same marked-changed paragraph says three things about large customers' AI spending. Their prioritization of AI infrastructure has at times come with reductions or mix changes in previously planned purchases and with cost cuts in non-AI capital spending. It names offerings from potential new market entrants. It says the long-term trajectory of AI-driven demand is unknown, so demand for new products is hard to forecast and can make revenue volatile. The prior wording is not in my input.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "In addition, although the focus on deployment of AI-enabled solutions has driven increased demand for networking, the long-term trajectory is unknown. As such, demand estimates for our new products are difficult to forecast and can create volatility in our revenue.",
  "paragraph_id": "0001596532-26-000175:mdna:11",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_evaluation_inventory_in_finished_goods",
  "what_changed": "The inventory footnote now gives evaluation inventory within finished goods: $616.0 million at June 30, 2026 and $403.7 million at December 31, 2025. The footnote gives no cause. mdna:11 links evaluation inventory to customer trials and acceptance-period contracts, and to possible returns and inventory write-downs. The footnote itself gives amounts only, so I set no direction.",
  "account": "inventories (finished goods)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The balance includes evaluation inventory totaling $616.0 million and $403.7 million as of June 30, 2026 and December 31, 2025, respectively.",
  "paragraph_id": "0001596532-26-000175:notes:28",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_deferred_cost_of_goods_sold_tracks_deferred_product_revenue",
  "what_changed": "The footnote to the prepaid table says deferred cost of goods sold had increased as of June 30, 2026. It attributes this to a corresponding increase in deferred product revenue. Deferred cost of goods sold is the cost of product already delivered whose revenue is deferred, so it is inventory carried outside the inventory line until acceptance. I flag this as a management explanation on that basis. The prior footnote wording is not in my input.",
  "account": "prepaid expenses and other current assets (deferred cost of goods sold); deferred revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase as of June 30, 2026 was driven by a corresponding increase in deferred product revenue.",
  "paragraph_id": "0001596532-26-000175:notes:32",
  "explanation": true }
```

```json
{ "id": "revenue_recognition_deferred_revenue_acceptance_terms_cash_flow",
  "what_changed": "The operating cash flow narrative for the six months of 2026 attributes the deferred revenue increase mainly to product deferred revenue on customer contracts with acceptance terms, and also to more customer PCS contracts. It names this as the main working-capital inflow.",
  "account": "deferred revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase in deferred revenue of $1.5 billion primarily resulting from an increase in product deferred revenue related to customer contracts with acceptance terms and an increase in customer PCS contracts",
  "paragraph_id": "0001596532-26-000175:mdna:59",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_receivables_rise_attributed_to_billings",
  "what_changed": "The operating cash flow narrative for the six months of 2026 attributes the increase in accounts receivable to increased product and service billings. The same sentence lists a $288.2 million increase in inventory and gives no cause for it. The extended payment terms named in mdna:54 are not mentioned here.",
  "account": "accounts receivable",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase in accounts receivable of $379.3 million due to increased product and service billings",
  "paragraph_id": "0001596532-26-000175:mdna:59",
  "explanation": true }
```

```json
{ "id": "earnings_quality_other_assets_deferred_cost_of_sales",
  "what_changed": "The operating cash flow narrative for the six months of 2026 attributes the increase in other assets to more deferred cost of sales, linked to higher product revenue deferrals. This is the cash-flow counterpart of the notes:32 footnote. Deferred cost of sales is delivered product cost held until revenue is recognized, so I flag this as an inventory-type explanation.",
  "account": "prepaid expenses and other current assets; other assets (deferred cost of sales)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "a $619.7 million increase in other assets driven by increased deferred cost of sales associated with higher product revenue deferrals",
  "paragraph_id": "0001596532-26-000175:mdna:59",
  "explanation": true }
```

```json
{ "id": "earnings_quality_deferred_tax_cause_deferred_revenue",
  "what_changed": "The 2026 narrative attributes the increase in deferred taxes mainly to the increase in deferred revenue. The 2025 comparative paragraph (mdna:60) also named Section 174 capitalization of research and development costs as a cause. The 2026 sentence does not mention Section 174.",
  "account": "deferred tax assets; deferred income taxes (cash flow)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "offset by a $213.1 million increase in deferred taxes primarily due to the increase in deferred revenue",
  "paragraph_id": "0001596532-26-000175:mdna:59",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_other_performance_obligations_binding_product_agreements",
  "what_changed": "Other performance obligations are now stated as $1.3 billion as of June 30, 2026. That is $427.8 million of unbilled multi-year PCS and service contracts plus $875.1 million of binding contractual agreements with certain customers, mainly for future product shipments. The prior-period figures for this block are not in my input. The prose gives levels, not a direction.",
  "account": "remaining performance obligations (unbilled); future product and service revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Other performance obligations totaling $1.3 billion as of June 30, 2026 include unbilled multi-year PCS and service contract amounts of $427.8 million, and $875.1 million of binding contractual agreements with certain customers that are primarily related to future product shipments.",
  "paragraph_id": "0001596532-26-000175:notes:45",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations_timing",
  "what_changed": "The note now gives $8.4 billion of revenue expected to be recognized in future periods from contract liabilities, deferred revenue and other performance obligations as of June 30, 2026. About 91% is expected within two years and 9% in years three to five. The prior-period figures for this block are not in my input.",
  "account": "deferred revenue; contract liabilities; remaining performance obligations",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Total revenue from our contract liabilities, deferred revenue and other performance obligations that is expected to be recognized in future periods amounts to $8.4 billion as of June 30, 2026. Approximately 91% of this future revenue is expected to be recognized over the next two years and the remaining 9% is expected to be recognized during the third to the fifth year.",
  "paragraph_id": "0001596532-26-000175:notes:47",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_and_silicon_supply_gross_margin",
  "what_changed": "The outlook paragraph is marked changed; the prior wording is not in my input. It now says supply chain inflation and material scarcity, including tightening supply in the memory and silicon markets, 'have continued' to pressure gross margin. The sentence continues into mdna:16: if tariff or non-tariff measures escalate or supply worsens and the costs cannot be passed on, gross margins 'could be further impacted'.",
  "account": "gross margin; cost of revenue",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Simultaneously, supply chain inflation and material scarcity, such as the tightening of supply conditions in the memory and silicon markets, have continued to put pressure on our gross margin.",
  "paragraph_id": "0001596532-26-000175:mdna:15",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_elevated_inventory_and_purchase_commitments_outlook",
  "what_changed": "The same marked-changed paragraph expects inventory and purchase commitments to remain elevated and volatile. It gives four causes: new product introductions, shifts in customer demand, tightening supply conditions and changing supplier lead times. Management gives a cause for the inventory level. The prior wording is not in my input.",
  "account": "inventories",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In addition, we expect inventory and purchase commitments to remain elevated and subject to volatility as a result of new product introductions, shifts in customer demand, tightening supply conditions and fluctuations in supplier lead times.",
  "paragraph_id": "0001596532-26-000175:mdna:15",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_excess_obsolete_inventory_and_supplier_liability_risk",
  "what_changed": "The same marked-changed paragraph says this volatility creates a 'heightened risk' of excess or obsolete inventory charges and supplier liability charges. This is a risk statement about future reserve charges; it does not explain a recorded number. The prior wording is not in my input.",
  "account": "inventory reserves (excess and obsolete); supplier liability accrual; cost of revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "This volatility creates a heightened risk of excess or obsolete inventory and supplier liability charges.",
  "paragraph_id": "0001596532-26-000175:mdna:15",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_gross_margin_decline_large_customer_discounts",
  "what_changed": "The prose says gross margin decreased, to 62.9% for the three months and 62.4% for the six months, from 65.2% and 64.5%. It attributes the decrease mainly to a larger share of sales to large end customers, who generally receive higher discounts. It names customer mix only. mdna:15 says supply chain inflation and memory and silicon scarcity 'have continued to put pressure' on gross margin, and mdna:30 lists those factors. mdna:31 does not cite them for this period's decrease.",
  "account": "gross margin; cost of revenue",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease was primarily driven by an increased proportion of our sales to large end customers who generally receive higher discounts.",
  "paragraph_id": "0001596532-26-000175:mdna:31",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_product_revenue_demand_and_shipments",
  "what_changed": "The revenue paragraph gives the product revenue increase: $728.2 million or 38.8% for the three months, and $1,347.0 million or 37.7% for the six months. It attributes this to healthy customer demand and higher shipments of switching and routing platforms across the customer base. It attributes the service revenue increase to continued growth in initial and renewal support contracts as the installed base expands. The prior wording is not in my input.",
  "account": "product revenue; service revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "This increase reflects healthy customer demand and higher shipments of our switching and routing platforms across our customer base.",
  "paragraph_id": "0001596532-26-000175:mdna:25",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_non_americas_share_large_global_customer_mix",
  "what_changed": "The same paragraph says Non-Americas revenue was 23.0% and 19.4% of total revenue for the three and six months of 2026, against 21.8% and 21.0% a year earlier. It attributes these 'fluctuations' mainly to the geographic mix of sales to large global customers. I do not compare the percentages.",
  "account": "revenue by geography",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "These fluctuations are primarily driven by changes in the geographic mix of sales to our large global customers across our Non-Americas regions.",
  "paragraph_id": "0001596532-26-000175:mdna:25",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_press_release_reported_revenue",
  "what_changed": "The earnings release gives second-quarter 2026 revenue of $3.036 billion. It states growth of 12.1% over the first quarter of 2026 and 37.7% over the second quarter of 2025. The CEO quote (8k_2_02:9) and the headline (8k_2_02:5) call it the company's first $3 billion quarter.",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Revenue of $3.036 billion, an increase of 12.1% compared to the first quarter of 2026, and an increase of 37.7% from the second quarter of 2025.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:11",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_press_release_non_gaap_eps_growth_headline",
  "what_changed": "The release headline claims 40% year-over-year growth in non-GAAP EPS. The non-GAAP comparatives have been recast under the changed tax methodology (8k_2_02:40). The CFO quote (8k_2_02:15) says 'EPS up 39.7%' and does not name the basis. I do not reconcile either figure.",
  "account": "non-GAAP diluted net income per share",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Delivered 40% growth in non-GAAP EPS year-over-year as the company achieved its first $3+ billion revenue quarter.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_press_release_revenue_guidance",
  "what_changed": "New guidance for the third quarter of 2026: revenue of approximately $3.3 billion. The prose gives a level and states no change from the second quarter, so I set no direction. Comparing it with the reported quarter is for the numbers reader.",
  "account": "total revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Revenue of approximately $3.3 billion;",
  "paragraph_id": "0001596532-26-000174:8k_2_02:24",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_press_release_non_gaap_operating_margin_guidance",
  "what_changed": "New guidance for the third quarter of 2026: non-GAAP operating margin of 48 to 49%. The release reports second-quarter non-GAAP operating margin of 49.9% (8k_2_02:12). The guidance prose states no direction, and I do not compare the two.",
  "account": "non-GAAP operating margin",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Non-GAAP operating margin of 48 - 49%; and",
  "paragraph_id": "0001596532-26-000174:8k_2_02:25",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_press_release_non_gaap_eps_guidance",
  "what_changed": "New guidance for the third quarter of 2026: non-GAAP diluted EPS of $1.06 to $1.08. Under 8k_2_02:27 the guidance excludes stock-based compensation, intangible amortization, tax benefits on stock-based awards and the tax effect of exclusions. No GAAP reconciliation is given. The prose states no direction.",
  "account": "non-GAAP diluted net income per share",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Non-GAAP diluted net income per share between $1.06 and $1.08.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:26",
  "explanation": false }
```

```json
{ "id": "earnings_quality_cost_of_revenue_attributed_to_revenue_growth",
  "what_changed": "MD&A says cost of revenue increased by $359.2 million or 46.9% for the three months and $662.7 million or 44.3% for the six months. It attributes the increase mainly to a 'corresponding increase' in product and service revenues; the sentence ends in mdna:29. Whether cost moved in step with revenue is for the numbers reader to check. The same MD&A says gross margin decreased (mdna:31).",
  "account": "cost of revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Cost of revenue increased by $359.2 million, or 46.9%, and $662.7 million, or 44.3% for the three and six months ended June 30, 2026, compared to the same periods in 2025. These increases were primarily driven by a corresponding increase",
  "paragraph_id": "0001596532-26-000175:mdna:28",
  "explanation": false }
```

```json
{ "id": "earnings_quality_research_and_development_new_product_introduction_costs",
  "what_changed": "The R&D explanation names two main drivers. Personnel costs rose by $33.3 million (three months) and $59.4 million (six months). New product introduction costs rose by $8.3 million (three months) and $58.8 million (six months). The prior wording is not in my input.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase for the three and six months periods was primarily driven by increased personnel costs of $33.3 million and $59.4 million, as well as an increase in new product introduction costs of $8.3 million and $58.8 million.",
  "paragraph_id": "0001596532-26-000175:mdna:37",
  "explanation": false }
```

```json
{ "id": "earnings_quality_sales_and_marketing_headcount_growth",
  "what_changed": "MD&A says sales and marketing expense increased by $23.8 million (18.8%) for the three months and $48.8 million for the six months. It attributes the increase mainly to higher personnel costs from headcount growth. The prior wording is not in my input.",
  "account": "sales and marketing expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "which was primarily driven by increased personnel costs due to headcount growth",
  "paragraph_id": "0001596532-26-000175:mdna:40",
  "explanation": false }
```

```json
{ "id": "earnings_quality_interest_income_higher_cash_and_securities",
  "what_changed": "MD&A attributes the favorable movement in other income (expense), net mainly to higher interest income: $32.0 million for the three months and $50.9 million for the six months. It says this came from higher cash and marketable securities balances.",
  "account": "other income (expense), net; interest income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by increased interest income of $32.0 million and $50.9 million due to an increase in our cash and marketable securities balances",
  "paragraph_id": "0001596532-26-000175:mdna:47",
  "explanation": false }
```

```json
{ "id": "earnings_quality_effective_tax_rate_lower_equity_compensation_benefits",
  "what_changed": "The tax note says the effective tax rate increased for the three and six months of 2026, mainly because tax benefits from equity-based compensation decreased. MD&A mdna:51 carries the same sentence. The release's non-GAAP reconciliation removes tax benefits on stock-based awards (8k_2_02:39, 8k_2_02:53).",
  "account": "provision for income taxes; effective tax rate",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in the effective tax rate in the three and six months ended June 30, 2026, as compared to the same periods in 2025, was primarily due to a decrease in tax benefits attributable to equity-based compensation.",
  "paragraph_id": "0001596532-26-000175:notes:85",
  "explanation": false }
```

```json
{ "id": "earnings_quality_non_gaap_prior_period_recast_for_tax_method",
  "what_changed": "The release says the 2025 non-GAAP comparatives were recast for the change in how non-GAAP income taxes on stock-based awards are calculated. The recast raised 2025 non-GAAP net income by $10.7 million (three months) and $30.4 million (six months). It raised non-GAAP diluted EPS by nil (three months) and $0.03 (six months). The growth claims in 8k_2_02:5 and 8k_2_02:15 are measured against these recast comparatives.",
  "account": "non-GAAP net income; non-GAAP diluted net income per share (prior-period comparatives)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The retrospective application of this change resulted in an increase to non-GAAP net income of $10.7 million and $30.4 million for the three and six months ended June 30, 2025, respectively.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:40",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_non_gaap_tax_effect_definition",
  "what_changed": "The release defines its non-GAAP tax adjustment this way. Since the fourth quarter of fiscal 2025 it excludes only the direct excess tax benefits of stock-based awards; it no longer excludes their discrete indirect effects. Management says this better aligns with industry practice, and all prior periods are recast (8k_2_02:55). By the release's own words the change is not new this quarter, but it still governs the comparatives and the non-GAAP EPS guidance basis in this release.",
  "account": "non-GAAP net income; non-GAAP diluted net income per share",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Effective the fourth quarter of fiscal year 2025, the company updated its methodology for calculating the income tax effect of non-GAAP adjustments.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:53",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_velocloud_allocation_still_preliminary",
  "what_changed": "The acquisition note now covers the three and six months ended June 30, 2026 and says the carrying value of goodwill did not change in those periods. It still calls the VeloCloud purchase price allocation 'preliminary'. The acquisition was completed on June 30, 2025, and this report's period ends on June 30, 2026. The text does not say whether the allocation is final or whether the measurement period has closed; that is for the supervisors.",
  "account": "goodwill; intangible assets, net",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The preliminary purchase price allocation based on the estimated fair values of the assets acquired and liabilities assumed as of the acquisition date, included $268.4 million of intangible assets, $148.0 million of goodwill and $116.4 million of net tangible liabilities assumed as of June 30, 2025.",
  "paragraph_id": "0001596532-26-000175:notes:53",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_unrealized_loss_aging_column_dropped",
  "what_changed": "The March 31, 2026 unrealized-loss table (0001596532-26-000078:note_history:9) had columns for losses within 12 months, losses of 12 months or greater, and a total, and it had a commercial paper row. The June 30, 2026 table (notes:19) shows only the within-12-months column for four security types. This new sentence replaces the 12-months-or-greater column and says those positions were not material. notes:17 says no credit losses or non-credit impairments were recognized and that all unrealized gains or losses went to other comprehensive income (loss).",
  "account": "marketable securities; accumulated other comprehensive income (loss)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Debt securities in unrealized losses positions 12 months or greater were not material as of June 30, 2026",
  "paragraph_id": "0001596532-26-000175:notes:20",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_cfo_trading_plan_modified",
  "what_changed": "New this quarter: on June 2, 2026 the CFO modified a Rule 10b5-1 trading arrangement first adopted on December 11, 2025. The arrangement covers the sale of shares that may be earned from performance-based RSUs, a number the company says cannot be determined. It runs until December 31, 2026 (notes:94). The text does not say what the modification changed.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "On June 2, 2026, Chantelle Breithaupt, our Senior Vice President and Chief Financial Officer, modified her Rule 10b5-1 trading arrangement previously adopted on December 11, 2025",
  "paragraph_id": "0001596532-26-000175:notes:93",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_director_trading_plan_adopted",
  "what_changed": "New this quarter: on June 9, 2026 director Mark Templeton adopted a Rule 10b5-1 trading arrangement to sell up to 50,000 shares. It runs until June 30, 2027 or until all trades are completed.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "On June 9, 2026, Mark Templeton, a member of our Board of Directors, adopted a Rule 10b5-1 trading arrangement providing for the sale from time to time of an aggregate of up to 50,000 shares of our common stock.",
  "paragraph_id": "0001596532-26-000175:notes:95",
  "explanation": false }
```

```json
{ "id": "across_documents_broad_based_growth_claim_versus_large_customer_mix",
  "what_changed": "In the earnings release the CFO calls the quarter's growth 'strong, broad-based'. The 10-Q MD&A attributes the gross margin decrease mainly to a larger share of sales to large end customers (mdna:31). It attributes Non-Americas revenue fluctuations to the geographic mix of sales to large global customers (mdna:25). The two documents characterize the source of growth differently. I do not test either against the numbers.",
  "account": "revenue; gross margin",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Our second quarter 2026 reflects strong, broad-based growth, with revenue up 37.7% and EPS up 39.7%.",
  "paragraph_id": "0001596532-26-000174:8k_2_02:15",
  "explanation": false }
```

```json
{ "id": "across_documents_investing_narrative_omits_capex_and_other_lines",
  "what_changed": "The 2026 investing narrative describes investing cash flows only as purchases, maturities and sales of marketable securities. The 8-K cash flow statement (0001596532-26-000174:8k_2_02:49) also shows a 'Purchases of property and equipment' line and an 'Other' investing line for the 2026 six months. No prose in my input describes either line, even though the building project still has remaining spend (notes:63).",
  "account": "cash used in investing activities; purchases of property and equipment",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "purchases of marketable securities of $4.3 billion. These amounts were partially offset by proceeds from maturities and sales of marketable securities of $2.0 billion.",
  "paragraph_id": "0001596532-26-000175:mdna:62",
  "explanation": false }
```

Items: 43. Items with `explanation` true: 7. These are liquidity_and_capital_purchase_commitments_raised_for_memory_and_silicon_supply, revenue_recognition_extended_payment_terms_large_customers, revenue_recognition_acceptance_periods_and_evaluation_inventory_volatility, revenue_recognition_deferred_cost_of_goods_sold_tracks_deferred_product_revenue, revenue_recognition_receivables_rise_attributed_to_billings, earnings_quality_other_assets_deferred_cost_of_sales and estimates_and_discretion_elevated_inventory_and_purchase_commitments_outlook.

Twelve items come from MD&A paragraphs that are marked changed but whose prior wording is not in my input: the mdna:11, mdna:15, mdna:25, mdna:28, mdna:31, mdna:37, mdna:40, mdna:47, mdna:54, mdna:59, mdna:62 and mdna:65 items. Each reports what the text now says and cannot isolate the added words.

## Paragraphs shown as text that are not items

Insufficient (3): mdna:8, mdna:30, 0001596532-26-000174:8k_2_02:51.

### Notes (0001596532-26-000175)

- notes:4: date rolled forward. Per the history, "three months ended March 31, 2026" became "three and six months ended June 30, 2026". The reclassification sentence is unchanged.
- notes:9: the history shows no change. ASU 2024-03 is pending and still under evaluation.
- notes:10: the history shows no change. ASU 2025-11 is pending and still under evaluation.
- notes:13: fair-value hierarchy table; amounts only.
- notes:14: date rolled forward. There were still no transfers between levels.
- notes:16: amortized cost and unrealized gains/losses table; amounts only.
- notes:17: reads as standing impairment language with the period dates rolled. The history does not cover this block. Its content is cited in structure_and_disclosure_changes_unrealized_loss_aging_column_dropped.
- notes:19: unrealized-loss table re-laid out. The substance is in the item from notes:20; otherwise amounts only.
- notes:21: date rolled forward. There are still no maturities beyond three years.
- notes:22: maturity table; amounts only.
- notes:23: duration figure (about 1.4 years) restated in a standing sentence; amounts only. The prior figure is not in my input.
- notes:27: inventory table; amounts only.
- notes:31: prepaid expenses table; amounts only.
- notes:35: property and equipment table; amounts only.
- notes:39: contract liabilities rollforward table; amounts only.
- notes:40: current portion of contract liabilities in a standing sentence; amounts only.
- notes:43: deferred revenue rollforward table; amounts only.
- notes:50: other income table; amounts only.
- notes:56: intangible assets table; amounts only.
- notes:58: future amortization schedule; amounts only.
- notes:59: heading.
- notes:62: heading.
- notes:64: heading.
- notes:65: guarantees and indemnification. The history shows no change; standing text.
- notes:66: heading.
- notes:67: ordinary-course legal sentence. The history shows no change.
- notes:68: date rolled forward. Per the history, "March 31, 2026" became "June 30, 2026" and nothing else changed.
- notes:69: heading.
- notes:74: RSU activity table; amounts only.
- notes:77: stock-based compensation table; amounts only.
- notes:78: unamortized compensation ($1.5 billion over about 3.9 years) in a standing sentence; amounts only.
- notes:80: EPS table; amounts only.
- notes:82: antidilutive awards table; amounts only.
- notes:84: effective tax rate table; amounts only.
- notes:89: revenue by geography table; amounts only.
- notes:90: U.S. revenue footnote; amounts only.
- notes:92: long-lived assets by geography table; amounts only.
- notes:94: continuation of notes:93. Covered by related_parties_contingencies_and_subsequent_events_cfo_trading_plan_modified.

### MD&A (0001596532-26-000175)

- mdna:8: insufficient. The paragraph is marked changed, but the prior wording is not in my input. It is a strategy description ("network-as-a-service approach") with no amount, estimate, commitment or risk.
- mdna:16: continuation of the mdna:15 sentence across a page break. The cost pass-through clause is folded into narrative_signs_of_operating_pressure_memory_and_silicon_supply_gross_margin. The macro-demand sentence and the closing caution are standing caution.
- mdna:18: heading; period rolled forward.
- mdna:20: revenue and cost of revenue table; amounts only.
- mdna:22: revenue by geography table; amounts only.
- mdna:29: continuation of mdna:28. Covered by earnings_quality_cost_of_revenue_attributed_to_revenue_growth.
- mdna:30: insufficient. A standing list of gross margin factors, marked changed. The prior wording is not in my input, so I cannot tell which factor was added or removed.
- mdna:34: operating expense table; amounts only.
- mdna:43: G&A increase ("increased slightly"); amounts only, no cause stated.
- mdna:46: other income table; amounts only.
- mdna:50: effective tax rate table; amounts only.
- mdna:51: same sentence as notes:85. Covered by earnings_quality_effective_tax_rate_lower_equity_compensation_benefits.
- mdna:53: cash, equivalents and marketable securities total and the amount held abroad; amounts only.
- mdna:55: continuation of mdna:54. Covered by liquidity_and_capital_purchase_commitments_raised_for_memory_and_silicon_supply.
- mdna:57: cash flow summary table; amounts only.
- mdna:60: 2025 comparative operating cash flow narrative, rolled to six months. It describes 2025, not a current change. Its Section 174 reference is used in earnings_quality_deferred_tax_cause_deferred_revenue.
- mdna:63: 2025 comparative investing narrative (VeloCloud). Prior-year period.
- mdna:66: 2025 comparative financing narrative. Prior-year period.
- mdna:68: repurchase program description, same as notes:70. Covered by liquidity_and_capital_no_share_repurchases_remaining_authorization.
- mdna:69: same as notes:70. Covered by the same item.
- mdna:74: purchase obligations with the same figures as notes:60. Covered by liquidity_and_capital_purchase_commitments_receipt_timing and by structure_and_disclosure_changes_purchase_obligation_scope_sentence_removed (the scope sentence is absent here too).
- mdna:76: property project sentence, same as notes:63. Covered by liquidity_and_capital_property_project_remaining_capex_range.
- mdna:78: off-balance-sheet statement; date rolled forward.

### Item 4 (0001596532-26-000175)

- item_4_controls:1: heading.
- item_4_controls:2: heading.
- item_4_controls:3: standard conclusion that disclosure controls are effective as of the period end. No deficiency, material weakness or remediation is stated.
- item_4_controls:4: heading.
- item_4_controls:5: no changes in internal control over financial reporting during the quarter; standard language with the period date.
- item_4_controls:6: heading.
- item_4_controls:7: inherent-limitations boilerplate.

### 8-K Item 2.02, exhibit 99.1 (0001596532-26-000174)

- 8k_2_02:1, 8k_2_02:2, 8k_2_02:3: exhibit header and filing-system labels.
- 8k_2_02:4: release title.
- 8k_2_02:6: Fortune 500 and Gartner recognition; promotional, no amount or risk.
- 8k_2_02:7: product announcement; no amount, estimate or risk.
- 8k_2_02:8: dateline.
- 8k_2_02:9: CEO quote; promotional. The $3 billion milestone is covered by the items from 8k_2_02:5 and 8k_2_02:11.
- 8k_2_02:10: heading.
- 8k_2_02:12: GAAP and non-GAAP operating margins; amounts only.
- 8k_2_02:13: GAAP and non-GAAP diluted EPS; amounts only.
- 8k_2_02:14: reconciliation pointer; boilerplate.
- 8k_2_02:16: heading.
- 8k_2_02:17: webinar promotion.
- 8k_2_02:18: Gartner recognition; promotional.
- 8k_2_02:19: product announcement (7060XE7 Series).
- 8k_2_02:20: product and technology description.
- 8k_2_02:21: continuation of 8k_2_02:20.
- 8k_2_02:22: heading.
- 8k_2_02:23: lead-in to the outlook. Covered by the three guidance items.
- 8k_2_02:27: standard statement of guidance exclusions and why no GAAP reconciliation is given. Cited in results_against_expectations_press_release_non_gaap_eps_guidance.
- 8k_2_02:28: heading.
- 8k_2_02:29: conference call logistics.
- 8k_2_02:30: webcast logistics.
- 8k_2_02:31, 8k_2_02:32, 8k_2_02:33: headings.
- 8k_2_02:34: income statement; amounts only.
- 8k_2_02:35: page number.
- 8k_2_02:36, 8k_2_02:37, 8k_2_02:38: headings.
- 8k_2_02:39: GAAP to non-GAAP reconciliation table; amounts only.
- 8k_2_02:41, 8k_2_02:42, 8k_2_02:43: headings.
- 8k_2_02:44: balance sheet; amounts only.
- 8k_2_02:45: page number.
- 8k_2_02:46, 8k_2_02:47, 8k_2_02:48: headings.
- 8k_2_02:49: cash flow statement; amounts only. Its property-and-equipment, investing 'Other' and financing 'Other' lines are named in across_documents_investing_narrative_omits_capex_and_other_lines and liquidity_and_capital_financing_taxes_paid_under_repurchase_plans.
- 8k_2_02:50: heading.
- 8k_2_02:51: insufficient. Safe-harbor risk list. No prior release is in my input, so I cannot identify any added or removed risk.
- 8k_2_02:52: heading.
- 8k_2_02:54: page number.
- 8k_2_02:55: continuation of 8k_2_02:53. Covered by structure_and_disclosure_changes_non_gaap_tax_effect_definition.
- 8k_2_02:56: standard statement of why non-GAAP measures are useful.
- 8k_2_02:57: standard statement of non-GAAP limitations.
- 8k_2_02:58: heading.
- 8k_2_02:59: company description.
- 8k_2_02:60: trademark notice.
- 8k_2_02:61: investor contacts.

### Note change history

The history entries are prior and current versions of paragraphs already accounted for above.

- 0001596532-26-000175:note_history:1 is notes:60, :2 is notes:61, :3 is notes:63, :4 is notes:68, :6 is notes:4, :7 is notes:19 and :8 is notes:20.
- 0001596532-26-000078:note_history:1, :2, :4, :5, :6 and :9 are the prior-period versions. They are quoted or cited in the items where they matter.
