# Notes-text reader — FTNT 10-Q 0001262039-26-000021 (quarter ended June 30, 2026)

## Input check

- Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- Nothing in the directory is a trend table, a price series, abnormal returns, short interest, another company's file, a prior run's probability or an outcome window. The 8-K exhibit 99.1 (0001262039-26-000018) carries the release's condensed statements as part of its body. I read them as 8-K text and computed nothing from them.
- Prior predictions: none on record, so there are no earlier flags to follow up.
- Not in the directory, so recorded as insufficient: Item 1A diff, Exhibit 21 diff, any Exhibit 10, and an auditor's report (this is a 10-Q, and input_controls.md carries only Item 4).
- 8-K index: only the Item 2.02 body (2026-07-29) is carried. The index lists no Item 4.01 or 4.02 and no late-filing notification on or before 2026-07-30. The 2026-06-16 Item 5.07 has no body in the input.
- Method: no arithmetic. Where two figures appear in an item, they are as the text states them. Every direction comes from the prose, not from a calculation.

## Items

```json
{ "id": "results_against_expectations_quarter_exceeds_high_end_of_guidance",
  "what_changed": "New in this release: the headline says second-quarter results exceeded the high end of guidance on revenue and profitability. The guidance it refers to is in the prior release, which is not in the input, so this remains management's claim.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Exceeds high end of second quarter guidance on revenue and profitability",
  "paragraph_id": "0001262039-26-000018:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised",
  "what_changed": "New in this release: the headline says full-year 2026 revenue guidance was raised, to 19% year-over-year growth. The earlier guidance is not in the input.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Raises 2026 revenue guidance to 19% year over year growth",
  "paragraph_id": "0001262039-26-000018:8k_2_02:6",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_intel_security_processor_collaboration",
  "what_changed": "New counterparty in the processor supply chain. The release reports a strategic collaboration with Intel on the next security processor (SP6), using Intel's design, packaging and manufacturing capabilities, and says it strengthens the resilience and diversity of the supply chain. No terms, commitment or accounting is given, and none of the 10-Q paragraphs carried as text mention it.",
  "account": "inventory purchase commitments",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Announced a strategic collaboration with Intel to develop Fortinet Security Processor 6 (SP6)",
  "paragraph_id": "0001262039-26-000018:8k_2_02:20",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_revenue_guidance_range",
  "what_changed": "New: a revenue range for the third quarter of 2026. The prose gives no direction, only a level against which next quarter's revenue can be read.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Revenue in the range of $2.010 billion to $2.100 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:28",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_billings_guidance_range",
  "what_changed": "New: a billings range for the third quarter of 2026. The release defines billings as revenue plus the change in deferred revenue. It is a level, and no direction is stated.",
  "account": "deferred revenue (billings)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Billings in the range of $2.250 billion to $2.350 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:29",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_gross_margin_guidance_range",
  "what_changed": "New: a non-GAAP gross margin range for the third quarter of 2026. It is a level with no direction. Separately, MD&A expects pressure on both product and service gross margin for the full year (see the hardware component cost and service gross margin items).",
  "account": "gross profit",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "gross margin in the range of 79.0% to 81.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:30",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_operating_margin_guidance_range",
  "what_changed": "New: a non-GAAP operating margin range for the third quarter of 2026. It is a level with no direction.",
  "account": "operating income",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "operating margin in the range of 35.0% to 37.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:31",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_earnings_per_share_guidance_range",
  "what_changed": "New: a diluted non-GAAP EPS range for the third quarter of 2026. It assumes an 18% non-GAAP tax rate and a diluted share count of 741 million to 745 million. It is a level with no direction.",
  "account": "net income per share, diluted",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "net income per share in the range of $0.83 to $0.87",
  "paragraph_id": "0001262039-26-000018:8k_2_02:32",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_range",
  "what_changed": "The release gives the full-year 2026 revenue range behind the headline raise (the raise itself is the full-year revenue guidance item). The prior range is not in the input.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Revenue in the range of $8.020 billion to $8.180 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:34",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_service_revenue_guidance_range",
  "what_changed": "The release gives a full-year 2026 service revenue range. The prior release is not in the input, so I cannot tell whether the range moved. MD&A separately expects service revenue to keep growing year over year.",
  "account": "service revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Service revenue in the range of $5.180 billion to $5.220 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:35",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_billings_guidance_range",
  "what_changed": "The release gives a full-year 2026 billings range. The input does not show whether it moved from the prior release.",
  "account": "deferred revenue (billings)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Billings in the range of $9.350 billion to $9.550 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:36",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_gross_margin_guidance_range",
  "what_changed": "The release gives a full-year 2026 non-GAAP gross margin range. The input does not show whether it moved. MD&A says product gross margin may decline, and service gross margin will decline slightly, for the full year.",
  "account": "gross profit",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "gross margin in the range of 79.0% to 81.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:37",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_operating_margin_guidance_range",
  "what_changed": "The release gives a full-year 2026 non-GAAP operating margin range. The input does not show whether it moved. MD&A expects operating margin to increase slightly for the full year.",
  "account": "operating income",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "operating margin in the range of 35.0% to 37.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:38",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_earnings_per_share_guidance_range",
  "what_changed": "The release gives a full-year 2026 diluted non-GAAP EPS range, assuming an 18% non-GAAP tax rate and 741 million to 745 million diluted shares. The input does not show whether it moved.",
  "account": "net income per share, diluted",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "net income per share in the range of $3.41 to $3.47",
  "paragraph_id": "0001262039-26-000018:8k_2_02:39",
  "explanation": false }
```

```json
{ "id": "across_documents_adjusted_free_cash_flow_in_release_not_in_quarterly_report",
  "what_changed": "The release defines and reconciles an adjusted free cash flow that adds back cash paid for real estate purchases (8k_2_02:79). The 10-Q's free cash flow definition and reconciliation (mdna:88, mdna:89) show free cash flow without that add-back. The input does not show whether the release carried this measure before. The add-back covers the kind of purchase described in notes:43.",
  "account": "purchases of property and equipment",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "We define adjusted free cash flow as free cash flow plus cash payments associated with real estate related purchases.",
  "paragraph_id": "0001262039-26-000018:8k_2_02:88",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_product_revenue_growth_for_rest_of_year",
  "what_changed": "MD&A attributes product revenue growth to higher unit shipments and recent pricing actions. It also cites demand for higher-performance products, AI-infrastructure deployments, technology upgrades, upsell and new use cases. It expects product revenue to keep growing year over year for the rest of 2026.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect our product revenue to continue to grow year over year for the remainder of 2026 compared to the same periods of 2025.",
  "paragraph_id": "0001262039-26-000021:mdna:66",
  "explanation": false }
```

```json
{ "id": "earnings_quality_product_revenue_attributed_to_pricing_actions_and_selling_prices",
  "what_changed": "The quarter's product revenue explanation names higher average selling prices alongside unit shipments. It attributes those prices to demand for higher-performing models and to recent pricing actions. Pricing actions are also named as the main driver of the quarter's product gross margin increase (mdna:106), and they appear in the billings-factor and liquidity-factor lists (mdna:162, mdna:174). The input does not show whether the prior quarter's text named pricing actions.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by hardware revenue growth resulting from higher unit shipments year over year, higher average selling prices",
  "paragraph_id": "0001262039-26-000021:mdna:100",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_service_revenue_growth_for_rest_of_year",
  "what_changed": "MD&A attributes service revenue growth to recognizing revenue from the growing deferred revenue balance: FortiGuard and other security subscriptions, unified SASE, SecOps and FortiCare. It expects service revenue to keep growing year over year for the rest of 2026.",
  "account": "service revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect our service revenue to continue to grow year over year for the remainder of 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:67",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_hardware_component_costs_in_product_margin_outlook",
  "what_changed": "MD&A says product gross margin may decline for full-year 2026 because hardware component costs remain higher. The quarter's product gross margin paragraph (mdna:106) reports an increase driven by pricing actions. Read together, the prose points to product margin pressure in the remaining quarters of 2026.",
  "account": "product gross profit",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Our product gross margin may decline for the full year 2026 as compared to 2025 primarily due to continued higher hardware component costs.",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_service_gross_margin_slight_decline_for_full_year",
  "what_changed": "MD&A expects service gross margin to decline slightly for full-year 2026. The reason given is the expansion of data center, colocation and cloud hosting capacity to support unified SASE and SecOps. The quarter's service margin paragraph (mdna:107) names the same cost driver.",
  "account": "service gross profit",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "We also expect service gross margin to decline slightly for the full year 2026 as compared to 2025, primarily due to continued expansion of our data center footprint and colocation and cloud hosting capacity",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_tariff_exposure_on_hardware_gross_margin",
  "what_changed": "MD&A says it does not expect U.S. tariffs to have a meaningful impact on gross margin. It adds that changes in trade policy, such as higher rates, reclassification or modified exemptions, could hurt gross margin, mainly on hardware sales to U.S. customers.",
  "account": "cost of product revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We currently do not expect the U.S. tariffs to have a meaningful impact on our gross margin.",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_operating_margin_slight_increase",
  "what_changed": "MD&A expects full-year 2026 operating margin to increase slightly, from operating leverage and measured investments. It expects both revenue and operating expense to rise in 2026, with spending on sales and marketing headcount, product development, data centers and real estate.",
  "account": "operating income",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "For the full year 2026, we expect our operating margin to increase slightly compared to 2025, benefiting from operating leverage and measured investments.",
  "paragraph_id": "0001262039-26-000021:mdna:72",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_chip_costs_in_cost_of_product_revenue",
  "what_changed": "The product gross margin explanation names higher memory chip costs, and a mix shift toward hardware, as offsets to pricing actions. The six-month paragraph (mdna:138) repeats the wording. Rising component costs are also given as a reason for higher inventory purchase commitments (mdna:168).",
  "account": "cost of product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by recent pricing actions, partially offset by a shift in revenue mix to hardware and increased costs of memory chips",
  "paragraph_id": "0001262039-26-000021:mdna:106",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_research_and_development_expense_increase_rest_of_year",
  "what_changed": "MD&A attributes the quarter's R&D increase to personnel costs (headcount and compensation rates) and to 'the impact of the recent acquisitions'. It expects R&D to rise year over year in absolute dollars for the rest of 2026.",
  "account": "research and development",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect research and development expenses to increase in absolute dollars year over year during the remainder of 2026",
  "paragraph_id": "0001262039-26-000021:mdna:111",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_sales_and_marketing_expense_increase_rest_of_year",
  "what_changed": "MD&A attributes the quarter's sales and marketing increase mainly to personnel-related costs. It expects sales and marketing to rise year over year in absolute dollars for the rest of 2026, to capture market share.",
  "account": "sales and marketing",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect our sales and marketing expenses to increase in absolute dollars year over year during the remainder of 2026",
  "paragraph_id": "0001262039-26-000021:mdna:114",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_legal_fees_cited_in_general_and_administrative",
  "what_changed": "The quarter's G&A increase is attributed first to legal and other professional fees, then to personnel costs. In the same quarter, defendants filed a motion to dismiss the securities class action (June 15, 2026, notes:83), and the derivative actions remained stayed. The prose does not tie the fees to any matter.",
  "account": "general and administrative",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase of $2.1 million in legal related fees and other professional services fees",
  "paragraph_id": "0001262039-26-000021:mdna:116",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_general_and_administrative_expense_increase_rest_of_year",
  "what_changed": "MD&A expects G&A to rise year over year in absolute dollars for the rest of 2026, to support growing operations.",
  "account": "general and administrative",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect our general and administrative expenses to increase in absolute dollars year over year during the remainder of 2026",
  "paragraph_id": "0001262039-26-000021:mdna:116",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_income_decline_attributed_to_repurchases_and_debt_repayment",
  "what_changed": "MD&A attributes lower interest income to lower average interest rates and to lower average cash and cash equivalent balances, caused by share repurchases and the debt repayment. The six-month paragraph (mdna:153) gives the same cause. Whether the stated balances bear this out is for the numbers reader.",
  "account": "interest income",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "lower average cash and cash equivalents balances as a result of share repurchases and debt repayment",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_expense_lower_after_senior_note_repayment",
  "what_changed": "MD&A attributes lower interest expense to repaying the 2026 Senior Notes at their March 2026 maturity. Only the 2031 Senior Notes remain outstanding (notes:73).",
  "account": "interest expense",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "primarily due to the repayment of our 2026 Senior Notes at maturity in March 2026",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "across_documents_foreign_exchange_losses_and_dropped_functional_currency_disclosure",
  "what_changed": "MD&A attributes the quarter's decrease in other income, net mainly to higher foreign currency exchange losses; the six months also show a higher FX loss (mdna:153). In the same filing, the policy note dropped two sentences the prior quarter carried (0001262039-26-000013:note_history:13). They said foreign subsidiaries' functional currency is the U.S. dollar and that one subsidiary moved to the U.S. dollar effective January 1, 2026. The text does not link the two, and it does not say whether the functional currency position changed.",
  "account": "other income, net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "a $10.1 million increase in foreign currency exchange losses",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_provision_for_expected_credit_losses_cited_in_general_and_administrative",
  "what_changed": "In the six-month section, the G&A explanation names a higher provision for expected credit losses as its first driver. This is the only mention of the credit loss provision in the carried text. It comes in the year the company adopted ASU 2025-05's practical expedient for estimating credit losses on current receivables (notes:7, adopted January 1, 2026). The prose gives no cause for the higher provision.",
  "account": "accounts receivable, net (allowance for expected credit losses)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase of $1.3 million in provision for expected credit losses",
  "paragraph_id": "0001262039-26-000021:mdna:148",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_moodys_rating_upgrade_after_quarter_end",
  "what_changed": "New subsequent event, in MD&A and in the release (8k_2_02:25): in July 2026 Moody's upgraded certain ratings to A3 from Baa1 and changed the outlook to Stable from Positive. S&P remains BBB+ with a Stable outlook. No new borrowing is described.",
  "account": "long-term debt",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "upgraded certain of our credit ratings to A3 from Baa1 and changed the outlook to Stable from Positive",
  "paragraph_id": "0001262039-26-000021:mdna:162",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_installment_billings_named_among_billings_factors",
  "what_changed": "The capital resources paragraph is carried as changed. It lists 'an increase in installment billings' among the factors further billings growth may depend on. The prior quarter's wording is not in the input, so I cannot tell whether this factor is new; the identifiable new content in the paragraph is the Moody's upgrade. Installment billing affects the timing of billings, deferred revenue and receivables.",
  "account": "deferred revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "an increase in installment billings",
  "paragraph_id": "0001262039-26-000021:mdna:162",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_full_year_capital_expenditure_estimate_range",
  "what_changed": "MD&A gives a full-year 2026 capital expenditure estimate of about $350 million to $550 million. It expects data center, PoP, office and warehouse capacity to keep growing. The prior quarter's estimate is not in the input.",
  "account": "purchases of property and equipment",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We estimate the full year capital expenditures to be between approximately $350 million and $550 million in 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:164",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_inventory_purchase_commitments_increase_explained_by_demand_lead_times_and_component_costs",
  "what_changed": "MD&A says non-cancelable inventory purchase commitments at June 30, 2026 increased from December 31, 2025. It gives the cause: growth trends in customer demand, product lead times and rising component costs. The note states $1.67 billion at June 30, 2026 (notes:79); the prior quarter's note stated $1.37 billion at March 31, 2026 (0001262039-26-000013:note_history:2). The schedule (notes:77) puts commitments in a 2026 column and a thereafter column. The note's description (notes:78) says some commitments secure supply and pricing for multi-year periods. The increase figure is the prose's own; the supervisor reconciles it.",
  "account": "inventory purchase commitments",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "These inventory purchase commitments as of June 30, 2026 totaled $1.67 billion, an increase of $856.5 million compared to $810.6 million as of December 31, 2025, as we continued to work with contract manufacturers and suppliers to optimize our inventory and purchase commitments position based on growth trends in customer demand, product lead times and increasing components cost.",
  "paragraph_id": "0001262039-26-000021:mdna:168",
  "explanation": true }
```

```json
{ "id": "earnings_quality_operating_cash_flow_attributed_to_working_capital_management",
  "what_changed": "MD&A attributes six-month operating cash flow to business growth, better profitability and working capital management. Among the movements it names the higher non-current deferred revenue and the deferred contract costs (mainly sales commissions). It does not discuss receivables or inventory movements.",
  "account": "net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "as a result of the continued growth of our business, improved profitability and our ability to successfully manage our working capital",
  "paragraph_id": "0001262039-26-000021:mdna:179",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_functional_currency_sentences_dropped_from_consolidation_policy",
  "what_changed": "The consolidation paragraph (now notes:2) was rewritten without two sentences the prior quarter carried. One said that as of March 31, 2026 the functional currency of the foreign subsidiaries is the U.S. dollar. The other said one subsidiary moved its functional currency to the U.S. dollar effective January 1, 2026, after its full operational integration. The current text says nothing about functional currency.",
  "account": "other income, net",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Effective January 1, 2026, the Company transitioned the functional currency of one of its subsidiaries to the U.S. dollar following its full operational integration.",
  "paragraph_id": "0001262039-26-000013:note_history:13",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_internal_use_software_standard_adoption_timing",
  "what_changed": "On ASU 2025-06 (capitalizing internal-use software; effective 2028, early adoption permitted), the note says the company is assessing adoption timing and method. The paragraph is carried as changed, but the prior wording is not in the input, so I cannot tell whether 'adoption timing' is new. If it is, it points to possible early adoption, which would change how software development costs are capitalized.",
  "account": "property and equipment, net",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We are currently assessing adoption timing and the method of adoption.",
  "paragraph_id": "0001262039-26-000021:notes:12",
  "explanation": false }
```

```json
{ "id": "earnings_quality_marketable_equity_securities_no_sales_in_second_quarter",
  "what_changed": "The note now says there were no sales of marketable equity securities in the second quarter. It restates the first-quarter sale and its net gain, and gives three- and six-month unrealized amounts on securities still held. MD&A attributes part of the quarter's decrease in other income, net to lower net gains on marketable equity securities (mdna:121). It attributes the six-month increase to the swing from net losses to net gains (mdna:153).",
  "account": "other income, net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "We had no sales of marketable equity securities during the second quarter of 2026 and the six months ended June 30, 2025.",
  "paragraph_id": "0001262039-26-000021:notes:33",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_excess_and_obsolete_inventory_reserve_without_stated_cause",
  "what_changed": "The note gives the excess and obsolete reserve at June 30, 2026 and December 31, 2025. It says write-downs were not material for the three and six months. It gives no cause for any difference between the two balances, and none of the MD&A text carried here discusses the reserve. How reserve movement relates to write-downs is for the numbers reader.",
  "account": "inventory",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The excess and obsolete inventory reserve was $122.8 million and $137.5 million as of June 30, 2026 and December 31, 2025, respectively.",
  "paragraph_id": "0001262039-26-000021:notes:40",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_real_estate_purchase_for_data_center_and_office",
  "what_changed": "New: during the six months the company bought U.S. real estate for $62.1 million, for future data center and office development. It was accounted for as an asset acquisition, with the cost split between land and buildings by relative fair value. The release's adjusted free cash flow adds back real estate purchases (see the adjusted free cash flow item).",
  "account": "property and equipment, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "we purchased certain real estate property in the United States totaling $62.1 million, to be used for future development to expand our data center and office space",
  "paragraph_id": "0001262039-26-000021:notes:43",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_liability_for_excess_inventory_purchase_commitments",
  "what_changed": "The note gives the accrued liability for commitments above forecast demand: $24.0 million at June 30, 2026 and $26.7 million at December 31, 2025. The prior quarter's note stated $27.2 million at March 31, 2026. The liability is measured against demand forecasts on the same basis as the excess and obsolete valuation. It is stated in the same quarter that MD&A says commitments increased (mdna:168). No cause is given for the liability amount.",
  "account": "accrued liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "the liability for these inventory purchase commitments was $24.0 million and $26.7 million, respectively",
  "paragraph_id": "0001262039-26-000021:notes:79",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_prior_year_purchase_commitment_benefit_no_longer_quantified",
  "what_changed": "The prior quarter's note quantified a $4.5 million benefit from this liability in the three months ended March 31, 2025. The current note calls the related expense not material for the three and six months of both 2026 and 2025, so the 2025 benefit is no longer stated.",
  "account": "cost of product revenue",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The expense related to such accrued liability for inventory purchase commitments was not material during the three and six months ended June 30, 2026 and 2025.",
  "paragraph_id": "0001262039-26-000021:notes:79",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_securities_class_action_motion_to_dismiss_filed",
  "what_changed": "The sentence 'The time to respond to the consolidated amended complaint has not yet passed.' is replaced by the June 15, 2026 filing of a motion to dismiss. The company still calls the action without merit, says it cannot estimate the impact, and records no accrual (notes:84). The derivative actions remain stayed until the class action is resolved (notes:85). The paragraph's other edits are wording only ('from' for 'between', the possessive on attorneys fees).",
  "account": "accrued liabilities",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Defendants filed a motion to dismiss the consolidated amended complaint on June 15, 2026.",
  "paragraph_id": "0001262039-26-000021:notes:83",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_remaining_authorization",
  "what_changed": "The note gives six-month repurchases of 12.5 million shares at a $77.73 average price ($972.8 million, excluding a $6.7 million excise tax accrual). It says about $765.8 million remains authorized through February 28, 2027. The first-quarter subsequent-event paragraph, removed this quarter, said about $765.8 million remained as of that filing date (0001262039-26-000013:note_history:27). The supervisor can reconcile what the two statements imply for repurchases between those dates.",
  "account": "repurchase and retirement of common stock",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "As of June 30, 2026, approximately $765.8 million remained available for future share repurchases under the Repurchase Program.",
  "paragraph_id": "0001262039-26-000021:notes:120",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_subsequent_events_note_dropped",
  "what_changed": "The prior quarter had a subsequent-events note on share repurchases made after quarter end. This filing has no subsequent-events note, and the carried text discloses no repurchase after June 30, 2026. The only post-quarter event in the carried text is the July 2026 Moody's upgrade (mdna:162).",
  "account": "repurchase and retirement of common stock",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "we repurchased 1.9 million shares of our common stock at an average price of $77.95 per share, for an aggregate purchase price of $145.9 million, under the Repurchase Program",
  "paragraph_id": "0001262039-26-000013:note_history:27",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_operating_officer_trading_plan_adopted",
  "what_changed": "New: on June 5, 2026 the Chief Operating Officer adopted a Rule 10b5-1 plan to sell up to 56,700 shares from exercises of vested options, at or above a minimum price, between September 4, 2026 and September 30, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Whittle Plan provides for the potential sale by Mr. Whittle of up to 56,700 shares of our common stock",
  "paragraph_id": "0001262039-26-000021:notes:141",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_financial_officer_trading_plan_adopted",
  "what_changed": "New: on June 10, 2026 the Chief Financial Officer adopted a Rule 10b5-1 plan to sell up to 115 shares, plus a not-yet-determinable number of net shares from RSU and PSU vesting, between September 9, 2026 and September 15, 2027. The current chief financial officer is a named defendant in the consolidated securities class action (notes:83).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Ohlgart Plan provides for the potential sale by Mrs. Ohlgart of up to 115 shares of our common stock",
  "paragraph_id": "0001262039-26-000021:notes:142",
  "explanation": false }
```

Items: 48. Items with `explanation` true: 2 (mdna:148, mdna:168).

## Paragraphs read and not made items

### 8-K, 0001262039-26-000018 (Item 2.02, exhibit 99.1)

There is no prior release in the input, so paragraphs here were judged on content alone.

- 0001262039-26-000018:8k_2_02:1 — exhibit header
- 0001262039-26-000018:8k_2_02:2 — header
- 0001262039-26-000018:8k_2_02:3 — header
- 0001262039-26-000018:8k_2_02:4 — headline characterization; the substance is in the guidance-beat item
- 0001262039-26-000018:8k_2_02:7 — heading
- 0001262039-26-000018:8k_2_02:8 — amounts only: revenue growth headline, also stated in MD&A (mdna:57)
- 0001262039-26-000018:8k_2_02:9 — amounts only: product revenue growth headline; drivers are in the product revenue items
- 0001262039-26-000018:8k_2_02:10 — amounts only: billings growth headline (mdna:84)
- 0001262039-26-000018:8k_2_02:11 — amounts only: GAAP operating margin
- 0001262039-26-000018:8k_2_02:12 — amounts only: non-GAAP operating margin
- 0001262039-26-000018:8k_2_02:13 — amounts only: GAAP EPS
- 0001262039-26-000018:8k_2_02:14 — amounts only: non-GAAP EPS
- 0001262039-26-000018:8k_2_02:15 — amounts only: operating cash flow (drivers are in the operating cash flow item)
- 0001262039-26-000018:8k_2_02:16 — amounts only: free cash flow
- 0001262039-26-000018:8k_2_02:17 — dateline
- 0001262039-26-000018:8k_2_02:18 — CEO quote, promotional; no account
- 0001262039-26-000018:8k_2_02:19 — heading
- 0001262039-26-000018:8k_2_02:21 — product launch (FortiGate 1200G, FortiSASE Outpost); no account
- 0001262039-26-000018:8k_2_02:22 — product launch (FortiSOC); no account
- 0001262039-26-000018:8k_2_02:23 — product expansion (FortiEndpoint); no account
- 0001262039-26-000018:8k_2_02:24 — AI partnership announcements; no terms or account
- 0001262039-26-000018:8k_2_02:25 — same event as the Moody's upgrade item (mdna:162); the "highest rating" claim is promotional
- 0001262039-26-000018:8k_2_02:26 — heading
- 0001262039-26-000018:8k_2_02:27 — lead-in to third-quarter guidance
- 0001262039-26-000018:8k_2_02:33 — lead-in to full-year guidance
- 0001262039-26-000018:8k_2_02:40 — standard non-GAAP guidance exclusions and no-reconciliation language
- 0001262039-26-000018:8k_2_02:41 — heading
- 0001262039-26-000018:8k_2_02:42 — call logistics
- 0001262039-26-000018:8k_2_02:43 — conference schedule heading
- 0001262039-26-000018:8k_2_02:44 — conference name
- 0001262039-26-000018:8k_2_02:45 — conference date
- 0001262039-26-000018:8k_2_02:46 — conference name
- 0001262039-26-000018:8k_2_02:47 — conference date
- 0001262039-26-000018:8k_2_02:48 — conference name
- 0001262039-26-000018:8k_2_02:49 — conference date
- 0001262039-26-000018:8k_2_02:50 — conference name
- 0001262039-26-000018:8k_2_02:51 — conference date
- 0001262039-26-000018:8k_2_02:52 — conference name
- 0001262039-26-000018:8k_2_02:53 — conference date
- 0001262039-26-000018:8k_2_02:54 — conference boilerplate
- 0001262039-26-000018:8k_2_02:55 — heading
- 0001262039-26-000018:8k_2_02:56 — company description boilerplate
- 0001262039-26-000018:8k_2_02:57 — heading
- 0001262039-26-000018:8k_2_02:58 — forward-looking statement boilerplate (truncated in input)
- 0001262039-26-000018:8k_2_02:59 — heading
- 0001262039-26-000018:8k_2_02:60 — non-GAAP introduction boilerplate
- 0001262039-26-000018:8k_2_02:61 — statement heading
- 0001262039-26-000018:8k_2_02:62 — statement heading
- 0001262039-26-000018:8k_2_02:63 — statement heading
- 0001262039-26-000018:8k_2_02:64 — amounts only: condensed balance sheet (read, nothing computed)
- 0001262039-26-000018:8k_2_02:65 — statement heading
- 0001262039-26-000018:8k_2_02:66 — statement heading
- 0001262039-26-000018:8k_2_02:67 — statement heading
- 0001262039-26-000018:8k_2_02:68 — amounts only: condensed income statement
- 0001262039-26-000018:8k_2_02:69 — statement heading
- 0001262039-26-000018:8k_2_02:70 — statement heading
- 0001262039-26-000018:8k_2_02:71 — statement heading
- 0001262039-26-000018:8k_2_02:72 — amounts only: condensed cash flow statement
- 0001262039-26-000018:8k_2_02:73 — heading
- 0001262039-26-000018:8k_2_02:74 — heading
- 0001262039-26-000018:8k_2_02:75 — heading
- 0001262039-26-000018:8k_2_02:76 — amounts only: GAAP to non-GAAP reconciliation; the only rows are stock-based compensation, amortization, IP gain and the tax adjustment
- 0001262039-26-000018:8k_2_02:77 — standard footnote on the 18% non-GAAP tax rate
- 0001262039-26-000018:8k_2_02:78 — heading
- 0001262039-26-000018:8k_2_02:79 — amounts only: free cash flow and adjusted free cash flow reconciliation (the measure is in the adjusted free cash flow item)
- 0001262039-26-000018:8k_2_02:80 — heading
- 0001262039-26-000018:8k_2_02:81 — amounts only: billings reconciliation
- 0001262039-26-000018:8k_2_02:82 — footnote
- 0001262039-26-000018:8k_2_02:83 — heading
- 0001262039-26-000018:8k_2_02:84 — non-GAAP boilerplate
- 0001262039-26-000018:8k_2_02:85 — non-GAAP boilerplate
- 0001262039-26-000018:8k_2_02:86 — standard billings definition, also in MD&A (mdna:84)
- 0001262039-26-000018:8k_2_02:87 — standard free cash flow definition
- 0001262039-26-000018:8k_2_02:89 — standard non-GAAP gross profit definition
- 0001262039-26-000018:8k_2_02:90 — standard non-GAAP operating income definition; it allows "other significant non-recurring items", but no such row appears in this quarter's reconciliation
- 0001262039-26-000018:8k_2_02:91 — limitations boilerplate
- 0001262039-26-000018:8k_2_02:92 — standard non-GAAP net income definition
- 0001262039-26-000018:8k_2_02:93 — separator
- 0001262039-26-000018:8k_2_02:94 — trademarks and copyright
- 0001262039-26-000018:8k_2_02:95 — code
- 0001262039-26-000018:8k_2_02:96 — contacts

### Item 4, 0001262039-26-000021

There is no prior Item 4 in the input, and nothing in this text indicates a change.

- 0001262039-26-000021:item_4_controls:1 — heading
- 0001262039-26-000021:item_4_controls:2 — heading
- 0001262039-26-000021:item_4_controls:3 — date rolled forward: evaluation as of June 30, 2026; standard limitations language
- 0001262039-26-000021:item_4_controls:4 — date rolled forward: disclosure controls concluded effective
- 0001262039-26-000021:item_4_controls:5 — heading
- 0001262039-26-000021:item_4_controls:6 — date rolled forward: no material ICFR change in the quarter
- 0001262039-26-000021:item_4_controls:7 — page number

### MD&A, 0001262039-26-000021

- 0001262039-26-000021:mdna:7 — insufficient: forward-looking-statement bullet carried as changed; prior wording not in input; generic risk list (tariffs, wars), no account
- 0001262039-26-000021:mdna:20 — page number
- 0001262039-26-000021:mdna:28 — insufficient: forward-looking-statement bullet on litigation outcomes carried as changed; prior wording not in input; the litigation substance is in the motion-to-dismiss item
- 0001262039-26-000021:mdna:34 — date rolled forward; patent counts and solution-pillar description; no account
- 0001262039-26-000021:mdna:37 — page number
- 0001262039-26-000021:mdna:38 — product description (FortiOS quantum-safe features); no account
- 0001262039-26-000021:mdna:41 — product description (FortiAI, FortiAIGate); no account
- 0001262039-26-000021:mdna:44 — product description (three solution pillars); no account
- 0001262039-26-000021:mdna:45 — product description (Secure Networking); no account
- 0001262039-26-000021:mdna:46 — page number
- 0001262039-26-000021:mdna:47 — product description, continued; no account
- 0001262039-26-000021:mdna:48 — product description (Unified SASE, PoPs, sovereign SASE); no account
- 0001262039-26-000021:mdna:49 — product description (SecOps, FortiSOC); no account
- 0001262039-26-000021:mdna:50 — product description (FortiGuard Labs); no account
- 0001262039-26-000021:mdna:53 — service-offering description (Advanced Support tiers); no account
- 0001262039-26-000021:mdna:55 — training-program description; no account
- 0001262039-26-000021:mdna:57 — amounts only: quarter and six-month revenue summary; drivers are in the product and service revenue items
- 0001262039-26-000021:mdna:58 — amounts only: gross profit summary
- 0001262039-26-000021:mdna:59 — amounts only: gross margin summary
- 0001262039-26-000021:mdna:60 — amounts only: operating income summary
- 0001262039-26-000021:mdna:61 — amounts only: operating margin summary
- 0001262039-26-000021:mdna:62 — amounts only: cash and investments
- 0001262039-26-000021:mdna:63 — amounts only: deferred revenue
- 0001262039-26-000021:mdna:64 — amounts only: operating cash flow; drivers are in the operating cash flow item
- 0001262039-26-000021:mdna:65 — amounts only: regional revenue shares and growth
- 0001262039-26-000021:mdna:68 — page number
- 0001262039-26-000021:mdna:69 — amounts only: billings country concentration
- 0001262039-26-000021:mdna:71 — amounts only: operating expense ratio and headcount; the operating-leverage cause is in the full-year operating margin item
- 0001262039-26-000021:mdna:77 — insufficient: sales-channel description (distributors, MSSPs, cloud provider platforms) carried as changed; prior wording not in input; no amount
- 0001262039-26-000021:mdna:82 — amounts only: key metrics table
- 0001262039-26-000021:mdna:83 — amounts only: deferred revenue balances and their stated increases
- 0001262039-26-000021:mdna:84 — amounts only: billings definition plus the quarter's billings figure
- 0001262039-26-000021:mdna:85 — page number
- 0001262039-26-000021:mdna:87 — amounts only: billings reconciliation table
- 0001262039-26-000021:mdna:88 — standard free cash flow definition; no substantive change identifiable
- 0001262039-26-000021:mdna:89 — amounts only: free cash flow reconciliation table
- 0001262039-26-000021:mdna:92 — date rolled forward: no material change to critical accounting estimates
- 0001262039-26-000021:mdna:96 — heading; date rolled forward
- 0001262039-26-000021:mdna:98 — amounts only: revenue table
- 0001262039-26-000021:mdna:99 — amounts only: total revenue increase and regional attribution
- 0001262039-26-000021:mdna:101 — amounts only: the quarter's service revenue drivers, which are the same drivers as the service revenue item
- 0001262039-26-000021:mdna:102 — amounts only: share of service revenue that came from opening deferred revenue
- 0001262039-26-000021:mdna:104 — amounts only: cost of revenue table
- 0001262039-26-000021:mdna:105 — amounts only: total gross margin and mix shift; the mix cause is also in mdna:70
- 0001262039-26-000021:mdna:107 — amounts only: service gross margin; the data-center cost driver is in the service gross margin item
- 0001262039-26-000021:mdna:109 — amounts only: operating expense table
- 0001262039-26-000021:mdna:112 — page number
- 0001262039-26-000021:mdna:118 — amounts only: operating margin bridge
- 0001262039-26-000021:mdna:120 — amounts only: interest and other income table
- 0001262039-26-000021:mdna:123 — amounts only: tax table
- 0001262039-26-000021:mdna:124 — amounts only: the quarter's tax components (also in notes:121 and notes:122)
- 0001262039-26-000021:mdna:125 — page number
- 0001262039-26-000021:mdna:126 — amounts only: prior-year quarter's tax components
- 0001262039-26-000021:mdna:127 — heading: the six-month section is a format change that comes with the second quarter
- 0001262039-26-000021:mdna:128 — heading
- 0001262039-26-000021:mdna:129 — amounts only: six-month revenue table
- 0001262039-26-000021:mdna:130 — amounts only: six-month total revenue
- 0001262039-26-000021:mdna:131 — six-month restatement of the product revenue drivers in the pricing and product revenue items
- 0001262039-26-000021:mdna:132 — six-month restatement of the service revenue drivers
- 0001262039-26-000021:mdna:133 — amounts only: share of six-month service revenue that came from opening deferred revenue
- 0001262039-26-000021:mdna:134 — page number
- 0001262039-26-000021:mdna:135 — heading
- 0001262039-26-000021:mdna:136 — amounts only: six-month cost of revenue table
- 0001262039-26-000021:mdna:137 — amounts only: six-month gross margin and mix shift
- 0001262039-26-000021:mdna:138 — six-month restatement of the pricing and memory chip drivers in the memory chip item
- 0001262039-26-000021:mdna:139 — amounts only: six-month service gross margin stated as flat
- 0001262039-26-000021:mdna:140 — heading
- 0001262039-26-000021:mdna:141 — amounts only: six-month operating expense table
- 0001262039-26-000021:mdna:142 — heading
- 0001262039-26-000021:mdna:143 — amounts only: six-month research and development
- 0001262039-26-000021:mdna:144 — page number
- 0001262039-26-000021:mdna:145 — heading
- 0001262039-26-000021:mdna:146 — amounts only: six-month sales and marketing
- 0001262039-26-000021:mdna:147 — heading
- 0001262039-26-000021:mdna:149 — heading
- 0001262039-26-000021:mdna:150 — amounts only: six-month operating margin bridge
- 0001262039-26-000021:mdna:151 — heading
- 0001262039-26-000021:mdna:152 — amounts only: six-month interest and other income table
- 0001262039-26-000021:mdna:153 — amounts only: six-month interest and other income drivers (marketable equity gains are in the marketable securities item; the Linksys bargain-purchase gain is prior-year)
- 0001262039-26-000021:mdna:154 — heading
- 0001262039-26-000021:mdna:155 — amounts only: six-month tax table
- 0001262039-26-000021:mdna:156 — amounts only: six-month tax components
- 0001262039-26-000021:mdna:157 — page number
- 0001262039-26-000021:mdna:158 — amounts only: prior-year six-month tax components, including the Linksys deferred tax derecognition
- 0001262039-26-000021:mdna:160 — amounts only: liquidity table
- 0001262039-26-000021:mdna:163 — same facts as the share repurchase item (notes:120)
- 0001262039-26-000021:mdna:165 — page number
- 0001262039-26-000021:mdna:166 — date rolled forward: the 2026 note repayment was already disclosed in the first quarter (notes:70 is unchanged per the history); no intent to retire notes early
- 0001262039-26-000021:mdna:170 — amounts only: other contractual commitments
- 0001262039-26-000021:mdna:172 — date rolled forward: investment mix and liquidity sufficiency
- 0001262039-26-000021:mdna:173 — amounts only: cash held by international subsidiaries
- 0001262039-26-000021:mdna:174 — insufficient: long-term liquidity factor list carried as changed; prior wording not in input; names pricing actions, tariffs and conflicts; no amount
- 0001262039-26-000021:mdna:175 — page number
- 0001262039-26-000021:mdna:176 — date rolled forward: no off-balance-sheet arrangements
- 0001262039-26-000021:mdna:182 — amounts only: investing cash flows
- 0001262039-26-000021:mdna:185 — amounts only: financing cash flows

### Notes, 0001262039-26-000021

- 0001262039-26-000021:notes:1 — date rolled forward (per the change history, the period wording only)
- 0001262039-26-000021:notes:2 — covered by the functional-currency item: this is the prior consolidation paragraph without its functional-currency sentences
- 0001262039-26-000021:notes:4 — date rolled forward: no material policy change
- 0001262039-26-000021:notes:7 — insufficient: carried as changed but not in the change history; it gives the January 1, 2026 adoption of ASU 2025-05 with no material impact, which the first-quarter filing would already have carried; cited in the credit loss item
- 0001262039-26-000021:notes:10 — pending standard (ASU 2024-03) still under evaluation; no adoption
- 0001262039-26-000021:notes:15 — amounts only: revenue disaggregation table, now with six-month columns
- 0001262039-26-000021:notes:17 — amounts only: revenue from opening deferred revenue; period rolled
- 0001262039-26-000021:notes:19 — amounts only: remaining performance obligations; period rolled
- 0001262039-26-000021:notes:21 — amounts only: amortization of deferred contract costs
- 0001262039-26-000021:notes:23 — wording only: one-line introduction to a table
- 0001262039-26-000021:notes:24 — amounts only: investments table
- 0001262039-26-000021:notes:27 — amounts only: unrealized loss table
- 0001262039-26-000021:notes:30 — amounts only: maturities table
- 0001262039-26-000021:notes:36 — amounts only: fair value hierarchy table
- 0001262039-26-000021:notes:37 — date rolled forward: no transfers between levels
- 0001262039-26-000021:notes:39 — amounts only: inventory components table
- 0001262039-26-000021:notes:42 — amounts only: property and equipment table
- 0001262039-26-000021:notes:44 — amounts only: depreciation
- 0001262039-26-000021:notes:48 — accounting for the 2025 Linksys acquisition, split differently at a page break; no new event or amount
- 0001262039-26-000021:notes:49 — continuation of notes:48; no new event
- 0001262039-26-000021:notes:53 — standing statement: acquired companies' results and pro forma figures not material
- 0001262039-26-000021:notes:55 — date rolled forward: goodwill, no impairment
- 0001262039-26-000021:notes:58 — amounts only: intangible assets table
- 0001262039-26-000021:notes:60 — amounts only: amortization expense
- 0001262039-26-000021:notes:62 — amounts only: future amortization table
- 0001262039-26-000021:notes:65 — amounts only: EPS table
- 0001262039-26-000021:notes:67 — amounts only: anti-dilutive securities table
- 0001262039-26-000021:notes:68 — unchanged per the change history: debt heading
- 0001262039-26-000021:notes:69 — unchanged per the change history: senior notes issuance terms
- 0001262039-26-000021:notes:70 — unchanged per the change history: 2026 notes repaid at their March 15, 2026 maturity
- 0001262039-26-000021:notes:71 — unchanged per the change history: redemption and interest terms
- 0001262039-26-000021:notes:72 — unchanged per the change history: lead-in to the table
- 0001262039-26-000021:notes:73 — amounts only: debt table (unamortized discount rolled, per the change history)
- 0001262039-26-000021:notes:74 — amounts only: accrued interest and interest expense, period rolled; the no-covenant statement is standing
- 0001262039-26-000021:notes:75 — amounts only: fair value of the 2031 notes
- 0001262039-26-000021:notes:76 — date rolled forward: commitments heading
- 0001262039-26-000021:notes:77 — amounts only: purchase commitment schedule (cited in the inventory purchase commitments item)
- 0001262039-26-000021:notes:78 — unchanged per the change history: standing description of contract manufacturer agreements, including multi-year supply and pricing arrangements (cited in the inventory purchase commitments item)
- 0001262039-26-000021:notes:80 — amounts only: other contractual commitments; "consist" became "consists"
- 0001262039-26-000021:notes:81 — amounts only: operating lease commitments
- 0001262039-26-000021:notes:82 — date rolled forward: litigation accruals not material
- 0001262039-26-000021:notes:84 — date rolled forward: no accrual for the class action
- 0001262039-26-000021:notes:85 — wording only: "et. seq." became "et seq."; derivative actions still stayed
- 0001262039-26-000021:notes:86 — date rolled forward: Alorica appeal, no accrual
- 0001262039-26-000021:notes:87 — unchanged per the change history: indemnification
- 0001262039-26-000021:notes:88 — unchanged per the change history: cybersecurity threats
- 0001262039-26-000021:notes:90 — amounts only: shares available for grant
- 0001262039-26-000021:notes:93 — amounts only: RSU activity table
- 0001262039-26-000021:notes:96 — amounts only: PSU grants and valuation method
- 0001262039-26-000021:notes:97 — amounts only: PSU assumptions table
- 0001262039-26-000021:notes:98 — amounts only: PSU vesting and forfeitures
- 0001262039-26-000021:notes:99 — amounts only: unrecognized compensation
- 0001262039-26-000021:notes:100 — standing net-settlement description, split differently at a page break
- 0001262039-26-000021:notes:101 — continuation of notes:100
- 0001262039-26-000021:notes:103 — amounts only: shares withheld table
- 0001262039-26-000021:notes:106 — amounts only: option valuation assumptions table
- 0001262039-26-000021:notes:108 — amounts only: option activity table
- 0001262039-26-000021:notes:109 — amounts only: unrecognized option compensation; the definition is standing
- 0001262039-26-000021:notes:111 — amounts only: option values table
- 0001262039-26-000021:notes:114 — amounts only: stock-based compensation by line item
- 0001262039-26-000021:notes:116 — amounts only: stock-based compensation by award type
- 0001262039-26-000021:notes:118 — amounts only: tax benefit from stock-based compensation
- 0001262039-26-000021:notes:121 — amounts only: the quarter's effective tax rate and components
- 0001262039-26-000021:notes:122 — amounts only: continuation of notes:121
- 0001262039-26-000021:notes:123 — amounts only: six-month tax components
- 0001262039-26-000021:notes:124 — date rolled forward: One Big Beautiful Bill Act effects recognized
- 0001262039-26-000021:notes:125 — amounts only: unrecognized tax benefits and accrued interest; no cause stated
- 0001262039-26-000021:notes:126 — insufficient: carried as text but not in the change history; standing list of tax audits (United Kingdom, Canada, Germany; focus on inter-company profit allocation); prior wording not in input
- 0001262039-26-000021:notes:127 — date rolled forward: foreign tax credit regulations and Pillar Two, with no impact for the six months
- 0001262039-26-000021:notes:128 — standing: one segment, with the CEO as CODM
- 0001262039-26-000021:notes:130 — amounts only: segment expense table
- 0001262039-26-000021:notes:134 — amounts only: revenue by geography
- 0001262039-26-000021:notes:135 — amounts only: property and equipment by geography
- 0001262039-26-000021:notes:137 — amounts only: distributor revenue concentration
- 0001262039-26-000021:notes:139 — amounts only: distributor receivable concentration

## Insufficient

Count: 10.

- Sections not in the directory (4): Item 1A diff, Exhibit 21 diff, Exhibit 10, auditor's report.
- Paragraphs where the input does not show what changed (6): mdna:7, mdna:28, mdna:77, mdna:174, notes:7, notes:126.
- Some items are only partly determinable; these are not counted above.
  - notes:12 and the installment-billings item from mdna:162: the prior wording is not in the input.
  - The full-year guidance items from 8k_2_02:35 to 8k_2_02:39: the prior release is not in the input.
