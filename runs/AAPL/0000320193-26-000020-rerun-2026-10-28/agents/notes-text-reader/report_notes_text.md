# report_notes_text — AAPL 0000320193-26-000020 (10-Q, quarter ended June 27, 2026)

## Input check

- Files read in full: input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md, input_prior_predictions.md.
- Nothing forbidden was found: no trend table, prices, abnormal returns, short interest, other-company files, prior-run probabilities or outcome window. The 8-K file holds the full earnings release (Exhibit 99.1) with its statements; that is an 8-K body and allowed.
- Not in the directory, so no items could come from them: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report (this is a 10-Q; the controls file holds Item 4 only).
- Prior predictions: none on record (no earlier run). There are no earlier flags to carry forward.
- 8-K coverage: the only 8-K body supplied is item 2.02 (0000320193-26-000018, filed 2026-07-30). The item-code list shows no other 8-K filed after the prior 10-Q (2026-05-01) and on or before 2026-07-31. The list shows no late-filing notifications.
- Method caveat: the note change history covers only three note tags (commitments, debt, revenue). For every other paragraph carried as text, the prior version is not in my input. Each item says what the text says now, and the only evidence that such a paragraph differs is that it was carried as text. Where I cannot say what changed in substance, the item or list line says `insufficient`.
- No arithmetic was done. Where an item gives two amounts, they are copied from the prose and not compared. Every direction below comes from what the prose says, not from a computed value.

## Items (60)

```json
{ "id": "revenue_recognition_deferred_revenue_balance_stated_in_note",
  "what_changed": "The revenue note now states total deferred revenue of $14.9 billion as of June 27, 2026 and $13.7 billion as of September 27, 2025. The prior period's text (note history) stated $14.7 billion as of March 28, 2026. The realization-timing sentence (64% within a year, 23% in one-to-two years, 11% in two-to-three years, 2% beyond three years) is worded the same as in the prior period. The prose gives no direction.",
  "account": "deferred revenue",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of June 27, 2026 and September 27, 2025, the Company had total deferred revenue of $14.9 billion and $13.7 billion, respectively.",
  "paragraph_id": "0000320193-26-000020:notes:7",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_marketable_securities_maturity_mix_stated",
  "what_changed": "The financial instruments note now gives the maturity mix of non-current marketable debt securities as of June 27, 2026. Securities other than mortgage- and asset-backed: 81% in 1 to 5 years, 16% in 5 to 10 years, 3% over 10 years. Mortgage- and asset-backed securities: 14% in 1 to 5 years, 21% in 5 to 10 years, 65% over 10 years. The prior version is not in the input, so I cannot tell whether only the date rolled.",
  "account": "non-current marketable securities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "had maturities between 1 and 5 years, 16% between 5 and 10 years, and 3% greater than 10 years",
  "paragraph_id": "0000320193-26-000020:notes:15",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_term_debt_currency_hedge_maximum_length",
  "what_changed": "The note now says that, as of June 27, 2026, the longest period over which the Company hedges the variability of future cash flows on term-debt-related foreign currency transactions is 16 years. Cash flow or fair value hedges using forwards, cross-currency swaps or other instruments are named as the tools. The prior version is not in the input.",
  "account": "derivative instruments / accumulated other comprehensive loss (cash flow hedges of term debt)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "foreign currency transactions is 16 years",
  "paragraph_id": "0000320193-26-000020:notes:20",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_term_debt_under_fair_value_hedges_stated",
  "what_changed": "The note now states the carrying amount of current and non-current term debt under fair value hedges: $10.4 billion as of June 27, 2026 and $12.6 billion as of September 27, 2025. The prose gives no direction or cause.",
  "account": "term debt (current and non-current)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "term debt subject to fair value hedges was $10.4 billion and $12.6 billion, respectively",
  "paragraph_id": "0000320193-26-000020:notes:26",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_trade_receivables_single_customer_concentration",
  "what_changed": "The credit-risk paragraph now says one customer was 10% or more of total trade receivables at both dates. That customer accounted for 18% as of June 27, 2026 and 12% as of September 27, 2025. The customer is not named. The paragraph repeats that the Company requires third-party credit support or collateral from certain customers.",
  "account": "accounts receivable, net",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "the Company had one customer that represented 10% or more of total trade receivables, which accounted for 18% and 12%, respectively",
  "paragraph_id": "0000320193-26-000020:notes:29",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_trade_receivables_carrier_concentration",
  "what_changed": "The same paragraph now states that third-party cellular network carriers accounted for 27% of total trade receivables as of June 27, 2026 and 34% as of September 27, 2025. The prose gives no direction or cause.",
  "account": "accounts receivable, net",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "third-party cellular network carriers accounted for 27% and 34% of total trade receivables",
  "paragraph_id": "0000320193-26-000020:notes:29",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_vendor_non_trade_receivables_concentration",
  "what_changed": "The note now states that two vendors each held 10% or more of vendor non-trade receivables: 47% and 22% as of June 27, 2026, and 46% and 23% as of September 27, 2025. The paragraph also gives management's account of where the balance comes from. The receivables arise from the Company selling components to manufacturing vendors who build subassemblies or final products. These sales are not booked as net sales, and any gain reduces products cost of sales when the final products are sold. The explanatory sentences read as the standing description. The prior version is not in the input, so I cannot confirm whether they are unchanged.",
  "account": "vendor non-trade receivables",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of June 27, 2026, the Company had two vendors that individually represented 10% or more of total vendor non-trade receivables, which accounted for 47% and 22%.",
  "paragraph_id": "0000320193-26-000020:notes:31",
  "explanation": true }
```

```json
{ "id": "structure_and_disclosure_changes_inventory_breakdown_added_to_details_note",
  "what_changed": "The financial statement details note now has an 'Inventories' heading (notes:33) and a table splitting inventory into components and finished goods (notes:34). The diff layer maps the prior period's notes:33 to this filing's notes:35 and the prior notes:35 to this filing's notes:37. So the two inventory paragraphs have no prior-period counterpart in this note, which means the breakdown is newly shown this quarter. No paragraph in the input, whether note, MD&A or earnings release, explains the inventory balance.",
  "account": "inventories",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Total inventories",
  "paragraph_id": "0000320193-26-000020:notes:34",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_term_debt_carrying_amount_stated_in_note",
  "what_changed": "The debt note now states the aggregate carrying amount of fixed-rate notes as $82.3 billion as of June 27, 2026 and $90.7 billion as of September 27, 2025. The prior period's text (note history) stated $82.7 billion as of March 28, 2026. The prose gives no direction or cause.",
  "account": "term debt",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "aggregate carrying amount of $82.3 billion and $90.7 billion, respectively",
  "paragraph_id": "0000320193-26-000020:notes:43",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_term_debt_fair_value_stated_in_note",
  "what_changed": "The debt note now states the fair value of the Notes (Level 2) as $71.2 billion as of June 27, 2026 and $80.4 billion as of September 27, 2025. The prior period's text (note history) stated $70.8 billion as of March 28, 2026.",
  "account": "term debt (fair value disclosure)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "based on Level 2 inputs, was $71.2 billion and $80.4 billion, respectively",
  "paragraph_id": "0000320193-26-000020:notes:43",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_share_count_stated_in_note",
  "what_changed": "The equity note now states that, in the nine months ended June 27, 2026, the Company repurchased 215 million shares for $61.8 billion. It repeats that the programs carry no minimum purchase obligation and may use 10b5-1 plans. Repurchases point to a lower share count.",
  "account": "common stock shares outstanding",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "the Company repurchased 215 million shares of its common stock for $61.8 billion",
  "paragraph_id": "0000320193-26-000020:notes:45",
  "explanation": false }
```

```json
{ "id": "earnings_quality_rsu_vesting_date_fair_value_stated",
  "what_changed": "The share-based compensation note now states the total vesting-date fair value of RSUs. It is $8.9 billion for the quarter ended June 27, 2026 and $7.0 billion for the quarter ended June 28, 2025. For the nine-month periods it is $18.4 billion and $16.3 billion.",
  "account": "share-based compensation (RSU vesting-date fair value)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The total vesting-date fair value of RSUs was $8.9 billion and $7.0 billion for the three months ended June 27, 2026 and June 28, 2025, respectively",
  "paragraph_id": "0000320193-26-000020:notes:49",
  "explanation": false }
```

```json
{ "id": "earnings_quality_unrecognized_share_based_compensation_cost_stated",
  "what_changed": "The note now states unrecognized compensation cost on outstanding RSUs of $26.7 billion as of June 27, 2026. The Company expects to recognize it over a weighted-average 2.7 years.",
  "account": "share-based compensation expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "the total unrecognized compensation cost related to outstanding RSUs was $26.7 billion, which the Company expects to recognize over a weighted-average period of 2.7 years",
  "paragraph_id": "0000320193-26-000020:notes:53",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_legal_loss_contingency_assessment",
  "what_changed": "insufficient: the paragraph is carried as changed text, but its prior version is not in the input, so I cannot tell what changed. It now states management's opinion that there was not at least a reasonable possibility of a material loss, or of a material loss greater than a recorded accrual, on asserted legal and other claims. It names no specific matter and gives no accrual amount.",
  "account": "accrued liabilities / loss contingencies",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "In the opinion of management, there was not at least a reasonable possibility the Company may have incurred a material loss, or a material loss greater than a recorded accrual, concerning loss contingencies for asserted legal and other claims.",
  "paragraph_id": "0000320193-26-000020:notes:58",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_general_counsel_trading_plan",
  "what_changed": "New trading-arrangement disclosure. On May 5, 2026, Jennifer Newstead, Senior Vice President and General Counsel, entered into a plan meant to satisfy Rule 10b5-1(c). It provides for selling up to 24,912 shares, subject to price limits, plus up to 90% of shares vesting between June 15, 2026 and March 15, 2027, net of shares withheld for taxes. The plan expires May 6, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The plan provides for the sale, subject to certain price limits, of up to 24,912 shares of common stock, as well as up to 90% of shares vesting between June 15, 2026 and March 15, 2027",
  "paragraph_id": "0000320193-26-000020:notes:62",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_executive_trading_plan",
  "what_changed": "New trading-arrangement disclosure. On May 28, 2026, Tim Cook, Chief Executive Officer, entered into a plan meant to satisfy Rule 10b5-1(c). It provides for selling up to 16,250 shares, subject to price limits, plus shares vesting during the plan, net of tax withholding. It also provides for gifting up to 37,104 shares. The plan expires October 30, 2026.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "of up to 16,250 shares of common stock, as well as shares vesting during the duration of the plan pursuant to certain equity awards granted to Mr. Cook",
  "paragraph_id": "0000320193-26-000020:notes:63",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_software_announcements_and_siri_ai",
  "what_changed": "The MD&A quarterly highlights now say that during the quarter the Company announced iOS 27, macOS 27 Golden Gate, iPadOS 27, watchOS 27, visionOS 27 and tvOS 27, and introduced Siri AI. The earnings release (8k_2_02:8) also cites Siri AI and new child safety features from WWDC26. The R&D paragraph (mdna:54) cites investments in artificial intelligence.",
  "account": "research and development (context)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "and introduced Siri AI.",
  "paragraph_id": "0000320193-26-000020:mdna:8",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_component_supply_constraints_expected_to_intensify",
  "what_changed": "The MD&A paragraph is carried as changed text. It says the Company is in a period of supply constraints and rising component costs, driven by industry supply-demand imbalances in advanced semiconductors, NAND storage and DRAM memory. It also says the Company expects these trends to intensify, which may materially hurt revenue, costs, gross margin, results and financial condition. The prior version is not in the input, so I cannot say which sentences are new. The paragraph does not mention inventory.",
  "account": "products cost of sales / products gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The Company expects these trends to intensify",
  "paragraph_id": "0000320193-26-000020:mdna:11",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_price_increases_may_reduce_demand",
  "what_changed": "The same paragraph says price increases have been taken and may be taken again. It says they may not offset the cost pressure and may reduce demand, materially hurting revenue, costs and gross margin. This is a statement that pricing actions have already been taken.",
  "account": "net sales (product demand)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Actions, such as price increases, that have been and may in the future be taken by the Company may not effectively mitigate these negative impacts",
  "paragraph_id": "0000320193-26-000020:mdna:11",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_tariff_refunds_recognized_when_received",
  "what_changed": "The tariff paragraph is carried as changed text. It says that after the Supreme Court's February 20, 2026 ruling struck down certain IEEPA tariffs, the Company applied for refunds of tariffs paid through U.S. Customs and Border Protection. It says any refunds received have been recognized as a reduction of products cost of sales. The wording links recognition to refunds received. It gives no amount received and no amount still pending.",
  "account": "products cost of sales",
  "expected_direction": "down",
  "horizon": "this quarter; next quarter if further refunds are received",
  "quote": "The Company has applied for a refund of tariffs paid, following the processes established by U.S. Customs and Border Protection, and has recognized any refunds received as a reduction of products cost of sales.",
  "paragraph_id": "0000320193-26-000020:mdna:13",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_new_trade_act_tariffs_imposed",
  "what_changed": "The tariff paragraph now refers to the recent imposition of tariffs under Section 301 of the Trade Act of 1974. It names possible further measures: Section 232 semiconductor actions, sector-based tariffs and more Section 301 actions. It says tariffs can materially affect the supply chain, the availability of rare earths and components, pricing and gross margin. It still says the January 14, 2026 initial Section 232 results imposed no additional tariffs on the Company's products.",
  "account": "products cost of sales / products gross margin",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "including the recent imposition of tariffs under Section 301 of the Trade Act of 1974",
  "paragraph_id": "0000320193-26-000020:mdna:13",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_americas_net_sales_drivers",
  "what_changed": "MD&A says Americas net sales increased in the quarter and the nine months, primarily due to higher iPhone, Services and Mac net sales. No currency effect is mentioned for Americas.",
  "account": "net sales — Americas segment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Americas net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
  "paragraph_id": "0000320193-26-000020:mdna:18",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_europe_net_sales_drivers",
  "what_changed": "MD&A says Europe net sales increased in the quarter and the nine months, primarily due to higher iPhone, Services and Mac net sales.",
  "account": "net sales — Europe segment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Europe net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
  "paragraph_id": "0000320193-26-000020:mdna:20",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_europe_currency_favorable_impact",
  "what_changed": "MD&A says strength in foreign currencies against the U.S. dollar had a net favorable impact on Europe net sales. The sentence covers the first nine months only and says nothing about the quarter alone.",
  "account": "net sales — Europe segment (currency effect)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The strength in foreign currencies relative to the U.S. dollar had a net favorable year-over-year impact on Europe net sales during the first nine months of 2026.",
  "paragraph_id": "0000320193-26-000020:mdna:20",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_greater_china_net_sales_drivers",
  "what_changed": "MD&A says Greater China net sales increased in the quarter and the nine months, primarily due to higher iPhone net sales. Only iPhone is named.",
  "account": "net sales — Greater China segment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Greater China net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone.",
  "paragraph_id": "0000320193-26-000020:mdna:22",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_greater_china_renminbi_favorable_impact",
  "what_changed": "MD&A says strength in the renminbi against the U.S. dollar had a favorable impact on Greater China net sales in both the quarter and the nine months.",
  "account": "net sales — Greater China segment (currency effect)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The strength in the renminbi relative to the U.S. dollar had a favorable year-over-year impact on Greater China net sales during the third quarter and first nine months of 2026.",
  "paragraph_id": "0000320193-26-000020:mdna:22",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_japan_net_sales_drivers",
  "what_changed": "MD&A says Japan net sales increased in the quarter and the nine months due to higher iPhone net sales. The text says 'due to', not 'primarily due to'.",
  "account": "net sales — Japan segment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Japan net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of iPhone.",
  "paragraph_id": "0000320193-26-000020:mdna:24",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_japan_yen_unfavorable_impact",
  "what_changed": "MD&A says weakness in the yen against the U.S. dollar had an unfavorable impact on Japan net sales in both the quarter and the nine months.",
  "account": "net sales — Japan segment (currency effect)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The weakness in the yen relative to the U.S. dollar had an unfavorable year-over-year impact on Japan net sales during the third quarter and first nine months of 2026.",
  "paragraph_id": "0000320193-26-000020:mdna:24",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_rest_of_asia_pacific_net_sales_drivers",
  "what_changed": "MD&A says Rest of Asia Pacific net sales increased in the quarter and the nine months, primarily due to higher iPhone, Services and Mac net sales.",
  "account": "net sales — Rest of Asia Pacific segment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Rest of Asia Pacific net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
  "paragraph_id": "0000320193-26-000020:mdna:26",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_rest_of_asia_pacific_currency_favorable_impact",
  "what_changed": "MD&A says strength in foreign currencies against the U.S. dollar had a net favorable impact on Rest of Asia Pacific net sales. The sentence covers the quarter only and says nothing about the nine months.",
  "account": "net sales — Rest of Asia Pacific segment (currency effect)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The strength in foreign currencies relative to the U.S. dollar had a net favorable year-over-year impact on Rest of Asia Pacific net sales during the third quarter of 2026.",
  "paragraph_id": "0000320193-26-000020:mdna:26",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_iphone_net_sales_pro_models",
  "what_changed": "MD&A says iPhone net sales increased in the quarter and the nine months, primarily due to higher net sales of Pro models.",
  "account": "net sales — iPhone",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "iPhone net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of Pro models.",
  "paragraph_id": "0000320193-26-000020:mdna:31",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_mac_net_sales_laptops",
  "what_changed": "MD&A says Mac net sales increased in the quarter and the nine months due to higher net sales of laptops.",
  "account": "net sales — Mac",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Mac net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of laptops.",
  "paragraph_id": "0000320193-26-000020:mdna:33",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_ipad_net_sales_decline",
  "what_changed": "MD&A says iPad net sales decreased in the quarter, primarily due to lower net sales of iPad mini and iPad Air. It separately says iPad net sales increased over the nine months, primarily due to higher sales of the base iPad, partly offset by lower iPad mini sales. This is the only product category the prose describes as declining in the quarter.",
  "account": "net sales — iPad",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "iPad net sales decreased during the third quarter of 2026 compared to the third quarter of 2025 primarily due to lower net sales of iPad mini",
  "paragraph_id": "0000320193-26-000020:mdna:35",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_wearables_home_accessories_net_sales_drivers",
  "what_changed": "MD&A says Wearables, Home and Accessories net sales increased in the quarter and the nine months due to higher net sales of Accessories and Wearables. Home is not named as a driver.",
  "account": "net sales — Wearables, Home and Accessories",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Wearables, Home and Accessories net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of Accessories and Wearables.",
  "paragraph_id": "0000320193-26-000020:mdna:37",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_services_net_sales_advertising_and_cloud",
  "what_changed": "MD&A says Services net sales increased in the quarter and the nine months, primarily due to higher net sales from advertising and cloud services.",
  "account": "net sales — Services",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Services net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales from advertising and cloud services.",
  "paragraph_id": "0000320193-26-000020:mdna:39",
  "explanation": false }
```

```json
{ "id": "earnings_quality_tariff_refunds_drive_products_gross_margin",
  "what_changed": "MD&A names tariff refunds, together with a different product mix, as the primary causes of the rise in products gross margin and gross margin percentage in the quarter and the nine months. It names higher costs, including memory, as a partial offset. The MD&A gives no amount for the refunds and does not say whether they will recur. This paragraph and mdna:13 both put the refunds in products cost of sales.",
  "account": "products gross margin / products cost of sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to a different mix of products and tariff refunds",
  "paragraph_id": "0000320193-26-000020:mdna:45",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_costs_offset_products_margin",
  "what_changed": "MD&A names higher costs, including memory, as a partial offset to the rise in products gross margin. This links to mdna:11, which cites DRAM and NAND supply-demand imbalances and expects the trends to intensify.",
  "account": "products cost of sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "partially offset by higher costs, including memory",
  "paragraph_id": "0000320193-26-000020:mdna:45",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_services_gross_margin_drivers",
  "what_changed": "MD&A says Services gross margin increased in the quarter and the nine months, primarily due to higher Services net sales and a different mix of services, partly offset by higher costs.",
  "account": "services gross margin",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Services gross margin increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher Services net sales and a different mix of services, partially offset by higher costs.",
  "paragraph_id": "0000320193-26-000020:mdna:47",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_services_gross_margin_percentage_flat",
  "what_changed": "MD&A says Services gross margin percentage was flat in the quarter. It separately says the nine-month Services gross margin percentage increased, primarily due to a different mix of services, partly offset by higher costs.",
  "account": "services gross margin percentage",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Services gross margin percentage was flat during the third quarter of 2026 compared to the third quarter of 2025.",
  "paragraph_id": "0000320193-26-000020:mdna:48",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_research_and_development_ai_infrastructure",
  "what_changed": "MD&A says R&D expense increased in the quarter and the nine months, primarily due to higher infrastructure-related costs, including investments in artificial intelligence, and headcount-related expenses.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to higher infrastructure-related costs, including investments in artificial intelligence, and headcount-related expenses",
  "paragraph_id": "0000320193-26-000020:mdna:54",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_selling_general_administrative_no_significant_driver",
  "what_changed": "MD&A says SG&A increased in the quarter and the nine months, driven by various factors, none significant individually or in aggregate. No cause is named.",
  "account": "selling, general and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increases were driven by various factors, none of which were significant individually or in the aggregate.",
  "paragraph_id": "0000320193-26-000020:mdna:56",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_below_statutory_drivers",
  "what_changed": "MD&A says the effective tax rate for the quarter and the nine months was below the statutory federal rate. The reasons given are mainly a lower effective rate on foreign earnings (including changes in unrecognized tax benefits), the U.S. federal R&D credit and share-based compensation tax benefits. State income taxes are a partial offset.",
  "account": "provision for income taxes / effective tax rate",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "primarily due to a lower effective tax rate on foreign earnings, including the impact of changes in unrecognized tax benefits, the impact of the U.S. federal R&D credit, and tax benefits from share-based compensation, partially offset by state income taxes",
  "paragraph_id": "0000320193-26-000020:mdna:60",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_increase_drivers",
  "what_changed": "MD&A says the quarter's effective tax rate was higher than in the same quarter of 2025, primarily due to a higher effective rate on foreign earnings. Changes in unrecognized tax benefits and share-based compensation tax benefits are a partial offset. It also says the nine-month rate was higher. The reasons given are a higher foreign effective rate (including unrecognized tax benefit changes), the December 2024 Treasury foreign currency loss regulations, and the tax effect of foreign currency revaluations tied to the State Aid Decision in the first quarter of 2025.",
  "account": "provision for income taxes / effective tax rate",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was higher compared to the third quarter of 2025 primarily due to a higher effective tax rate on foreign earnings, partially offset by the impact of changes in unrecognized tax benefits and tax benefits from share-based compensation",
  "paragraph_id": "0000320193-26-000020:mdna:61",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_cited_in_both_directions",
  "what_changed": "The tax prose cites changes in unrecognized tax benefits three times. In the quarterly comparison they partly offset the higher rate. In the nine-month comparison they are listed among the causes of the higher rate. In mdna:60 they are among the reasons the rate is below statutory. The prose gives no amount or direction for the unrecognized tax benefit changes themselves.",
  "account": "unrecognized tax benefits / provision for income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "including the impact of changes in unrecognized tax benefits, the impact of foreign currency loss regulations issued by the U.S. Department of the Treasury in December 2024",
  "paragraph_id": "0000320193-26-000020:mdna:61",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_manufacturing_purchase_obligations_stated",
  "what_changed": "MD&A now states manufacturing purchase obligations of $57.0 billion as of June 27, 2026, of which $56.2 billion is payable within 12 months. The prose gives no direction. Read alongside mdna:11 (supply constraints).",
  "account": "manufacturing purchase obligations (off-balance-sheet)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As of June 27, 2026, the Company had manufacturing purchase obligations of $57.0 billion, with $56.2 billion payable within 12 months.",
  "paragraph_id": "0000320193-26-000020:mdna:66",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_other_purchase_obligations_stated",
  "what_changed": "MD&A now states other purchase obligations of $29.3 billion as of June 27, 2026, of which $9.2 billion is payable within 12 months. These cover supplier arrangements, licensed IP and content, distribution rights, and capital assets for product manufacturing.",
  "account": "other purchase obligations (off-balance-sheet)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As of June 27, 2026, the Company had other purchase obligations of $29.3 billion, with $9.2 billion payable within 12 months.",
  "paragraph_id": "0000320193-26-000020:mdna:68",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_deemed_repatriation_tax_fully_paid",
  "what_changed": "MD&A says that during the first nine months the Company paid the remaining $8.8 billion of the deemed repatriation tax payable under the Tax Cuts and Jobs Act. The word 'remaining' implies the payable is extinguished and no further installments are due.",
  "account": "deemed repatriation tax payable (other liabilities) / cash paid for income taxes",
  "expected_direction": "down",
  "horizon": "this quarter; no further installments implied over the next 12 months",
  "quote": "the Company paid the remaining $8.8 billion balance of the deemed repatriation tax payable",
  "paragraph_id": "0000320193-26-000020:mdna:70",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_cash_dividend_rate_stated",
  "what_changed": "MD&A now states the quarterly cash dividend as $0.27 per share as of June 27, 2026. It repeats that the Company intends to raise the dividend annually, subject to Board declaration. The release (8k_2_02:10) declares a $0.27 dividend payable August 13, 2026.",
  "account": "dividends / financing cash flows",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "quarterly cash dividend was $0.27 per share",
  "paragraph_id": "0000320193-26-000020:mdna:72",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_repurchases_and_dividends_paid_stated_in_mdna",
  "what_changed": "MD&A now states that during the quarter the Company repurchased $25.8 billion of common stock and paid $4.0 billion of dividends and dividend equivalents.",
  "account": "financing cash flows — repurchases of common stock; dividends",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "During the third quarter of 2026, the Company repurchased $25.8 billion of its common stock and paid dividends and dividend equivalents of $4.0 billion.",
  "paragraph_id": "0000320193-26-000020:mdna:73",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_internal_use_software_standard_adoption",
  "what_changed": "insufficient: the paragraph is carried as changed text, but its prior version is not in the input, so I cannot tell which words changed. It now says ASU 2025-06 (internal-use software) is effective for the Company in the first quarter of 2029, that early adoption is permitted, and that the Company is evaluating the timing and method of adoption. The standard requires capitalization once management commits to a project and completion is probable.",
  "account": "capitalized internal-use software / research and development expense",
  "expected_direction": "none",
  "horizon": "beyond 12 months (first quarter of 2029, early adoption permitted)",
  "quote": "ASU 2025-06 will be effective for the Company in its first quarter of 2029, and early adoption is permitted.",
  "paragraph_id": "0000320193-26-000020:mdna:76",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_expense_disaggregation_standard_adoption",
  "what_changed": "insufficient: the paragraph is carried as changed text, but its prior version is not in the input. It now says the Company will adopt ASU 2024-03 (expense disaggregation, including disclosure of selling expenses) in its fourth quarter of 2028 using a prospective transition method.",
  "account": "none (disclosure only)",
  "expected_direction": "none",
  "horizon": "beyond 12 months (fourth quarter of 2028)",
  "quote": "The Company will adopt ASU 2024-03 in its fourth quarter of 2028 using a prospective transition method.",
  "paragraph_id": "0000320193-26-000020:mdna:78",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_adoption",
  "what_changed": "insufficient: the paragraph is carried as changed text, but its prior version is not in the input. It now says the Company will adopt ASU 2023-09 (income tax rate reconciliation and disaggregated taxes paid) in its fourth quarter of 2026 using a prospective transition method. That puts it in the next annual report.",
  "account": "provision for income taxes (disclosure only)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The Company will adopt ASU 2023-09 in its fourth quarter of 2026 using a prospective transition method.",
  "paragraph_id": "0000320193-26-000020:mdna:80",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_record_revenue_and_eps_claim",
  "what_changed": "The earnings release headline claims June-quarter records for total company revenue and EPS.",
  "account": "net sales; diluted earnings per share",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "June quarter records for total company revenue and EPS",
  "paragraph_id": "0000320193-26-000018:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_record_iphone_mac_services_revenue_claim",
  "what_changed": "The release sub-headline claims new June-quarter revenue records for iPhone, Mac and Services.",
  "account": "net sales — iPhone, Mac, Services",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "iPhone, Mac and Services revenue set new June quarter records",
  "paragraph_id": "0000320193-26-000018:8k_2_02:6",
  "explanation": false }
```

```json
{ "id": "earnings_quality_tariff_refund_contribution_to_margin_and_eps",
  "what_changed": "The release says company gross margin of 50.1 percent includes a favorable impact of about 2 percentage points from tariff refunds. It says diluted EPS of $2.02 (stated as up 29 percent) includes a favorable $0.11 from tariff refunds. Part of the reported margin and EPS is attributed to refunds of previously paid tariffs, and the release does not say whether they will recur.",
  "account": "gross margin; diluted earnings per share; products cost of sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Company gross margin was 50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7",
  "explanation": false }
```

```json
{ "id": "across_documents_tariff_refund_sized_only_in_press_release",
  "what_changed": "The 10-Q text in my input names tariff refunds as a cause of the rise in products gross margin (mdna:45) and describes recognizing them in products cost of sales (mdna:13), but gives no amount. The furnished earnings release gives the size: about 2 percentage points of gross margin and $0.11 of diluted EPS. Among my inputs, the refund's size appears only in the release.",
  "account": "products cost of sales; diluted earnings per share",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Diluted earnings per share was $2.02, up 29 percent year over year, and included a favorable impact of $0.11 from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7",
  "explanation": false }
```

```json
{ "id": "across_documents_double_digit_growth_in_every_segment_claim",
  "what_changed": "The CEO quote calls this the strongest June quarter ever. It claims double-digit revenue growth across iPhone, Mac and Services and in every geographic segment, and cites Siri AI and new child safety features from WWDC26. The 10-Q MD&A says net sales rose in every geographic segment (mdna:18 to mdna:26) and for iPhone, Mac and Services (mdna:31, 33, 39). Whether each rate is double-digit is for the numbers reader.",
  "account": "net sales by category and by segment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "double-digit revenue growth across iPhone, Mac and Services, and in every geographic segment",
  "paragraph_id": "0000320193-26-000018:8k_2_02:8",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_record_operating_cash_flow_claim",
  "what_changed": "The CFO quote claims June-quarter records for both EPS and operating cash flow. No 10-Q MD&A paragraph carried as text in my input discusses operating cash flow.",
  "account": "cash generated by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "which set new June quarter records for both EPS and operating cash flow",
  "paragraph_id": "0000320193-26-000018:8k_2_02:9",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_installed_base_all_time_high_claim",
  "what_changed": "The CFO quote claims the installed base of active devices reached a new all-time high across all major product categories and geographic segments. This is a non-financial metric with no figure given.",
  "account": "none (installed base of active devices)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Our installed base of active devices also reached a new all-time high across all major product categories and geographic segments.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:9",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_period_end",
  "what_changed": "After quarter-end, the board declared a cash dividend of $0.27 per share, payable August 13, 2026 to holders of record at the close of business on August 10, 2026. The MD&A (mdna:72) states the quarterly dividend as of June 27, 2026 as $0.27 per share.",
  "account": "dividends / financing cash flows",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The dividend is payable on August 13, 2026, to shareholders of record as of the close of business on August 10, 2026.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:10",
  "explanation": false }
```

## Paragraphs carried as text and not made into items

Notes
- 0000320193-26-000020:notes:4 — heading; period descriptor rolled forward to the three- and nine-month periods (note history shows nothing else changed).
- 0000320193-26-000020:notes:5 — disaggregated revenue table; amounts only.
- 0000320193-26-000020:notes:6 — date rolled forward; the note history shows the same sentence (Greater China iPhone moderately higher proportion) with only the periods updated.
- 0000320193-26-000020:notes:8 — EPS heading; period descriptor rolled forward.
- 0000320193-26-000020:notes:9 — EPS table; amounts only.
- 0000320193-26-000020:notes:11 — marketable securities table lead-in; dates rolled forward.
- 0000320193-26-000020:notes:12 — marketable securities table; amounts only.
- 0000320193-26-000020:notes:24 — derivative notional lead-in; dates rolled forward.
- 0000320193-26-000020:notes:25 — derivative notional table; amounts only.
- 0000320193-26-000020:notes:32 — financial statement details lead-in; dates rolled forward.
- 0000320193-26-000020:notes:33 — "Inventories" heading; covered by the inventory item made on notes:34.
- 0000320193-26-000020:notes:36 — property, plant and equipment table; amounts only.
- 0000320193-26-000020:notes:38 — intangible assets table; amounts only.
- 0000320193-26-000020:notes:39 — headings only ("Debt", "Commercial Paper").
- 0000320193-26-000020:notes:40 — date rolled forward; the note history shows the outstanding commercial paper amounts worded identically.
- 0000320193-26-000020:notes:41 — commercial paper cash-flow table; amounts only (row labels follow the comparative period).
- 0000320193-26-000020:notes:42 — heading only ("Term Debt").
- 0000320193-26-000020:notes:47 — RSU activity lead-in; date rolled forward.
- 0000320193-26-000020:notes:48 — RSU activity table; amounts only.
- 0000320193-26-000020:notes:51 — share-based compensation table lead-in; dates rolled forward.
- 0000320193-26-000020:notes:52 — share-based compensation table; amounts only.
- 0000320193-26-000020:notes:54 — headings only ("Commitments and Contingencies", "Unconditional Purchase Obligations"); insufficient: carried as text with no prior version in the input and no substantive content.
- 0000320193-26-000020:notes:55 — reordered list (licensed IP and content now comes before distribution rights) and date rolled forward, per the note history.
- 0000320193-26-000020:notes:56 — unconditional purchase obligation schedule; amounts only (first column relabeled "remaining three months").
- 0000320193-26-000020:notes:57 — heading only ("Contingencies").
- 0000320193-26-000020:notes:59 — segment information lead-in; dates rolled forward.
- 0000320193-26-000020:notes:60 — segment table (quarter); amounts only.
- 0000320193-26-000020:notes:61 — segment table (nine months); amounts only.

MD&A
- 0000320193-26-000020:mdna:15 — segment net sales table lead-in; dates rolled forward.
- 0000320193-26-000020:mdna:16 — segment net sales table; amounts only.
- 0000320193-26-000020:mdna:28 — category net sales table lead-in; dates rolled forward.
- 0000320193-26-000020:mdna:29 — category net sales table; amounts only.
- 0000320193-26-000020:mdna:41 — gross margin table lead-in; dates rolled forward.
- 0000320193-26-000020:mdna:42 — gross margin table; amounts only.
- 0000320193-26-000020:mdna:43 — gross margin percentage table; amounts only.
- 0000320193-26-000020:mdna:51 — operating expense table lead-in; dates rolled forward.
- 0000320193-26-000020:mdna:52 — operating expense table; amounts only.
- 0000320193-26-000020:mdna:58 — tax table lead-in; dates rolled forward.
- 0000320193-26-000020:mdna:59 — tax table; amounts only.

Item 4 (controls)
- 0000320193-26-000020:item_4_controls:1 — heading only.
- 0000320193-26-000020:item_4_controls:2 — heading only.
- 0000320193-26-000020:item_4_controls:3 — standard effectiveness conclusion with the date rolled forward to June 27, 2026; disclosure controls stated effective.
- 0000320193-26-000020:item_4_controls:4 — heading only.
- 0000320193-26-000020:item_4_controls:5 — standard no-change statement with the quarter rolled forward; no change in internal control over financial reporting reported.
- 0000320193-26-000020:item_4_controls:6 — page footer.

8-K item 2.02 (Exhibit 99.1)
- 0000320193-26-000018:8k_2_02:1 — exhibit wrapper and filename.
- 0000320193-26-000018:8k_2_02:2 — document marker.
- 0000320193-26-000018:8k_2_02:3 — exhibit label.
- 0000320193-26-000018:8k_2_02:4 — release title.
- 0000320193-26-000018:8k_2_02:11 — conference call logistics.
- 0000320193-26-000018:8k_2_02:12 — investor-website boilerplate.
- 0000320193-26-000018:8k_2_02:13 — boilerplate company description; insufficient: no prior release in the input, so I cannot tell whether the employee count ("more than 150,000") or the platform list changed.
- 0000320193-26-000018:8k_2_02:14 — contact label.
- 0000320193-26-000018:8k_2_02:15 — contact name.
- 0000320193-26-000018:8k_2_02:16 — contact affiliation.
- 0000320193-26-000018:8k_2_02:17 — contact email.
- 0000320193-26-000018:8k_2_02:18 — contact phone.
- 0000320193-26-000018:8k_2_02:19 — contact label.
- 0000320193-26-000018:8k_2_02:20 — contact name.
- 0000320193-26-000018:8k_2_02:21 — contact affiliation.
- 0000320193-26-000018:8k_2_02:22 — contact email.
- 0000320193-26-000018:8k_2_02:23 — contact phone.
- 0000320193-26-000018:8k_2_02:24 — note to editors boilerplate.
- 0000320193-26-000018:8k_2_02:25 — copyright and trademark boilerplate.
- 0000320193-26-000018:8k_2_02:26 — statement header (company name).
- 0000320193-26-000018:8k_2_02:27 — statement title.
- 0000320193-26-000018:8k_2_02:28 — units line.
- 0000320193-26-000018:8k_2_02:29 — statements of operations; amounts only.
- 0000320193-26-000018:8k_2_02:30 — statement header (company name).
- 0000320193-26-000018:8k_2_02:31 — statement title.
- 0000320193-26-000018:8k_2_02:32 — units line.
- 0000320193-26-000018:8k_2_02:33 — balance sheets; amounts only.
- 0000320193-26-000018:8k_2_02:34 — statement header (company name).
- 0000320193-26-000018:8k_2_02:35 — statement title.
- 0000320193-26-000018:8k_2_02:36 — units line.
- 0000320193-26-000018:8k_2_02:37 — statements of cash flows; amounts only.

## Insufficient (6)

- 0000320193-26-000020:notes:58 — item made; I cannot tell what changed in the legal contingency paragraph.
- 0000320193-26-000020:mdna:76 — item made; I cannot tell which words of the ASU 2025-06 paragraph changed.
- 0000320193-26-000020:mdna:78 — item made; I cannot tell which words of the ASU 2024-03 paragraph changed.
- 0000320193-26-000020:mdna:80 — item made; I cannot tell which words of the ASU 2023-09 paragraph changed.
- 0000320193-26-000020:notes:54 — no item; headings carried as text with no visible substance.
- 0000320193-26-000018:8k_2_02:13 — no item; I cannot tell whether the boilerplate employee count or platform list changed.

Explanation flags set: 1 (liquidity_and_capital_vendor_non_trade_receivables_concentration). No paragraph in the input explains the inventory balance or any reserve balance.
