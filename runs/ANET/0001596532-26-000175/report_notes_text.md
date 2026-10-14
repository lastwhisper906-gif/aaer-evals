<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes-text reader — ANET 10-Q 0001596532-26-000175 (quarter ended June 30, 2026), diffed against 0001596532-26-000078

Input check: the directory holds only the six permitted files (input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md). There is no trend table, price, abnormal return, short-interest figure, other company's file, prior probability or outcome window. The 8-K body includes the earnings release's financial statement tables. Those are part of the 8-K, and I treated them as amounts for the numbers reader. No prior flags exist for this company (input_prior_predictions.md: "None on record").

Method note: the note change history gives the prior wording only for the commitments-and-contingencies, basis-of-presentation and unrealized-loss-table paragraphs. For every other notes paragraph and every MD&A paragraph carried as text, the prior wording is not in my input. For those items, `what_changed` describes what the text now says. The exact difference from the March 31, 2026 filing cannot be isolated.

## Items

```json
[
  {
    "id": "revenue_recognition_acceptance_periods_and_customer_trials",
    "what_changed": "This MD&A paragraph is carried as changed; its prior wording is not in my input. It now says that new product introductions and expanded use cases, especially in AI Ethernet, have resulted in more customer trials and contracts with acceptance periods. It also says they have increased the volatility and magnitude of evaluation inventory and product deferred revenue balances, which may make revenue vary by quarter and year. Here management names the cause of the evaluation inventory balance: trials and acceptance periods tied to new products.",
    "account": "deferred revenue (product); inventories (evaluation inventory)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "This has resulted in increased customer trials and contracts with acceptance periods, and an increase in the volatility and magnitude of our evaluation inventory and product deferred revenue balances, which in turn may create variability in our revenue results on a quarterly and annual basis.",
    "paragraph_id": "0001596532-26-000175:mdna:11",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_trial_returns_and_inventory_write_down_risk",
    "what_changed": "The same paragraph says that if trial or acceptance requirements are not met, the company may have to accept product returns. It could then not recognize revenue on those transactions and might have to write down inventory. This is stated as a conditional risk, not as an event that happened.",
    "account": "inventories (write-down); revenue (product)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "if we are not able to satisfy the requirements under customer trials or contracts with acceptance periods, we may be required to accept product returns from our customers, which would prevent us from recognizing revenue on such transactions and may result in the write-down of inventory.",
    "paragraph_id": "0001596532-26-000175:mdna:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_customer_reprioritization_toward_ai",
    "what_changed": "The same paragraph says that when large customers prioritized AI, this has at times come with cuts or mix changes in purchases they had planned, and with cost-reduction measures in their non-AI capital spending. It mentions offerings from potential new market entrants. It says the long-term path of AI demand is unknown and that demand for new products is hard to forecast, which can make revenue volatile.",
    "account": "revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "This prioritization of AI related infrastructure investment has, at times, come in conjunction with a reduction or changes in the mix of previously planned purchases and various cost reduction measures by these customers, including optimization and increased efficiency in non-AI related capital expenditures.",
    "paragraph_id": "0001596532-26-000175:mdna:11",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_elevated_excess_obsolete_and_supplier_liability",
    "what_changed": "This MD&A outlook paragraph is carried as changed; its prior wording is not in my input. It now expects inventory and purchase commitments to stay elevated and volatile. The reasons it gives are new product introductions, shifts in customer demand, tightening supply and changing supplier lead times. It says this volatility raises the risk of excess or obsolete inventory charges and supplier liability charges. Here management names causes of the inventory level.",
    "account": "inventories; excess/obsolete inventory reserve; supplier liability accrual",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In addition, we expect inventory and purchase commitments to remain elevated and subject to volatility as a result of new product introductions, shifts in customer demand, tightening supply conditions and fluctuations in supplier lead times. This volatility creates a heightened risk of excess or obsolete inventory and supplier liability charges.",
    "paragraph_id": "0001596532-26-000175:mdna:15",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_and_silicon_supply_tightening",
    "what_changed": "The same paragraph says supply chain inflation and material scarcity have continued to pressure gross margin. It names tightening supply in the memory and silicon markets as an example. The sentence continues into mdna:16: if tariffs escalate or supply worsens and the company cannot pass costs on, gross margins could be further impacted, and broader macroeconomic instability could hurt demand.",
    "account": "gross margin; cost of revenue (product)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Simultaneously, supply chain inflation and material scarcity, such as the tightening of supply conditions in the memory and silicon markets, have continued to put pressure on our gross margin.",
    "paragraph_id": "0001596532-26-000175:mdna:15",
    "explanation": false
  },
  {
    "id": "results_against_expectations_product_revenue_demand_and_shipments",
    "what_changed": "The revenue paragraph is rolled forward to the quarter. It states that product revenue increased by $728.2 million (38.8%) for the three months and $1,347.0 million (37.7%) for the six months. It attributes the increase to healthy customer demand and higher shipments of switching and routing platforms across the customer base.",
    "account": "revenue (product)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "This increase reflects healthy customer demand and higher shipments of our switching and routing platforms across our customer base.",
    "paragraph_id": "0001596532-26-000175:mdna:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_service_revenue_support_contracts",
    "what_changed": "It states that service revenue increased by $102.7 million (31.3%) and $188.1 million (29.4%) for the three and six months. It attributes this to continued growth in initial and renewal support contracts as the installed base expands.",
    "account": "revenue (service)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "service revenue increased by $102.7 million, or 31.3%, and $188.1 million, or 29.4% for the three and six months ended June 30, 2026, compared to the same periods in 2025, as a result of continued growth in initial and renewal support contracts as our customer installed base has continued to expand.",
    "paragraph_id": "0001596532-26-000175:mdna:25",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_non_americas_share_large_customer_geographic_mix",
    "what_changed": "It states that Non-Americas revenue was 23.0% and 19.4% of total revenue for the three and six months, compared with 21.8% and 21.0% a year earlier. It attributes these 'fluctuations' mainly to changes in the geographic mix of sales to large global customers. The prose does not say which way the share moved.",
    "account": "revenue by geography",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "These fluctuations are primarily driven by changes in the geographic mix of sales to our large global customers across our Non-Americas regions.",
    "paragraph_id": "0001596532-26-000175:mdna:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_cost_of_revenue_attributed_to_revenue_growth",
    "what_changed": "It states that cost of revenue increased by $359.2 million (46.9%) and $662.7 million (44.3%). It attributes the increases 'primarily' to a corresponding increase in product and service revenues. This paragraph does not cite the supply-chain inflation named in mdna:15 or the customer mix named in mdna:31. Whether the cost increase actually 'corresponds' to the revenue increase is the numbers reader's check.",
    "account": "cost of revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These increases were primarily driven by a corresponding increase",
    "paragraph_id": "0001596532-26-000175:mdna:28",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_gross_margin_factors_material_scarcity",
    "what_changed": "The list of gross margin factors is carried as changed; its prior wording is not in my input. It now names 'inflationary pressure and scarcity of materials in our supply chain', merchant silicon costs, and excess/obsolete inventory and supplier liability charges among the factors, and says gross margin will fluctuate. Which words are new cannot be isolated from my input.",
    "account": "gross margin",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "inflationary pressure and scarcity of materials in our supply chain, merchant silicon costs, and excess/obsolete inventory and supplier liability charges",
    "paragraph_id": "0001596532-26-000175:mdna:30",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_decrease_large_customer_discounts",
    "what_changed": "It states that gross margin decreased to 62.9% and 62.4% for the three and six months, compared with 65.2% and 64.5% in 2025. The stated main cause is a larger share of sales to large end customers, who get higher discounts. This paragraph does not mention the supply chain inflation and memory/silicon scarcity that mdna:15 says 'have continued to put pressure on our gross margin'.",
    "account": "gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease was primarily driven by an increased proportion of our sales to large end customers who generally receive higher discounts.",
    "paragraph_id": "0001596532-26-000175:mdna:31",
    "explanation": false
  },
  {
    "id": "results_against_expectations_research_and_development_personnel_and_new_product_costs",
    "what_changed": "It states that R&D increased by $51.7 million (17.4%) and $129.0 million (22.9%). The stated drivers are personnel costs of $33.3 million and $59.4 million and new product introduction costs of $8.3 million and $58.8 million for the three and six months.",
    "account": "research and development",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase for the three and six months periods was primarily driven by increased personnel costs of $33.3 million and $59.4 million, as well as an increase in new product introduction costs of $8.3 million and $58.8 million.",
    "paragraph_id": "0001596532-26-000175:mdna:37",
    "explanation": false
  },
  {
    "id": "results_against_expectations_sales_and_marketing_headcount_growth",
    "what_changed": "It states that sales and marketing increased by $23.8 million (18.8%) and $48.8 million. The six-month percentage is printed as '20.1' with no percent sign. The stated driver is personnel costs from headcount growth.",
    "account": "sales and marketing",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "which was primarily driven by increased personnel costs due to headcount growth",
    "paragraph_id": "0001596532-26-000175:mdna:40",
    "explanation": false
  },
  {
    "id": "results_against_expectations_general_and_administrative_increase_without_stated_cause",
    "what_changed": "It states that G&A 'increased slightly' by $4.4 million (15.0%) and $3.8 million (6.0%). The word 'slightly' is the paragraph's own. No driver is given.",
    "account": "general and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "General and administrative expenses increased slightly by $4.4 million, or 15.0%, and $3.8 million, or 6.0% for the three and six months ended June 30, 2026, compared to the same periods in 2025.",
    "paragraph_id": "0001596532-26-000175:mdna:43",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_income_from_larger_cash_and_securities",
    "what_changed": "It attributes the favorable movement in other income (expense), net, to increased interest income of $32.0 million and $50.9 million for the three and six months. The prose says this came from 'an increase in our cash and marketable securities balances'.",
    "account": "interest income; other income (expense), net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "was primarily driven by increased interest income of $32.0 million and $50.9 million due to an increase in our cash and marketable securities balances",
    "paragraph_id": "0001596532-26-000175:mdna:47",
    "explanation": false
  },
  {
    "id": "earnings_quality_effective_tax_rate_equity_compensation_benefit_decrease",
    "what_changed": "It states that the effective tax rate increased for the three and six months, mainly because tax benefits from equity-based compensation decreased. The same sentence appears as notes:85. This bears on the 8-K, which excludes 'tax benefits on stock-based awards' from non-GAAP net income separately.",
    "account": "provision for income taxes; effective tax rate",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in the effective tax rate in the three and six months ended June 30, 2026, as compared to the same periods in 2025, was primarily due to a decrease in tax benefits attributable to equity-based compensation.",
    "paragraph_id": "0001596532-26-000175:mdna:51",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_cash_and_securities_held_outside_united_states",
    "what_changed": "It states cash, cash equivalents and marketable securities of about $13.3 billion at June 30, 2026. About $0.5 billion of that is held by foreign subsidiaries outside the U.S.",
    "account": "cash, cash equivalents and marketable securities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, our total balance of cash, cash equivalents and marketable securities was approximately $13.3 billion, of which approximately $0.5 billion was held outside the U.S. in our foreign subsidiaries.",
    "paragraph_id": "0001596532-26-000175:mdna:53",
    "explanation": false
  },
  {
    "id": "revenue_recognition_extended_payment_terms_large_customers",
    "what_changed": "This liquidity paragraph is carried as changed; its prior wording is not in my input. It says working capital and operating cash flows may see timing differences because certain large customer arrangements include extended payment terms. This is a general statement, not tied to a reported number. It is flagged as an explanation because it names a cause of receivables timing. The six-month receivables explanation in mdna:59 cites billings and does not mention extended payment terms. None of the notes paragraphs carried as text in my input discusses extended payment terms or a financing component.",
    "account": "accounts receivable; operating cash flow",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Additionally, our working capital and operating cash flows may experience timing differences as a result of certain large customer arrangements that include extended payment terms.",
    "paragraph_id": "0001596532-26-000175:mdna:54",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_purchase_commitments_increased_for_memory_and_silicon",
    "what_changed": "The same paragraph says the company has increased its purchase commitments. The reasons given are the rapid deployment of AI networks, tightening supply in memory and silicon, and the aim of reducing lead times. The sentence continues into mdna:55, saying this will increase future working capital requirements. It also expects inventory and purchase commitments to stay elevated as new products ramp.",
    "account": "purchase commitments (off-balance-sheet); inventories; working capital",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In particular, we have increased our purchase commitments to respond to the rapid deployment of AI networks, and to navigate the tightening supply within the memory and silicon markets",
    "paragraph_id": "0001596532-26-000175:mdna:54",
    "explanation": false
  },
  {
    "id": "revenue_recognition_deferred_revenue_acceptance_terms_operating_cash",
    "what_changed": "The six-month operating cash flow paragraph states that deferred revenue increased by $1.5 billion. It says this came mainly from product deferred revenue on customer contracts with acceptance terms, and from customer PCS contracts.",
    "account": "deferred revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in deferred revenue of $1.5 billion primarily resulting from an increase in product deferred revenue related to customer contracts with acceptance terms and an increase in customer PCS contracts",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_assets_deferred_cost_of_sales_cash_flow",
    "what_changed": "It states a $619.7 million increase in other assets, driven by higher deferred cost of sales that goes with higher product revenue deferrals. I flag it as an inventory-type explanation: deferred cost of sales is the product cost of shipped units whose revenue is deferred, and it is carried outside the inventories line.",
    "account": "other assets; prepaid expenses and other current assets (deferred cost of goods sold)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a $619.7 million increase in other assets driven by increased deferred cost of sales associated with higher product revenue deferrals",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_accounts_receivable_increase_attributed_to_billings",
    "what_changed": "It states that accounts receivable increased by $379.3 million in the six months because of higher product and service billings. It does not mention the extended payment terms that mdna:54 says may cause working capital timing differences.",
    "account": "accounts receivable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in accounts receivable of $379.3 million due to increased product and service billings",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_inventory_increase_stated_without_cause",
    "what_changed": "It states a $288.2 million increase in inventory in the six-month operating cash flow discussion. This paragraph gives no cause; causes for the inventory level appear only in mdna:11, mdna:15 and mdna:54.",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a $288.2 million increase in inventory",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_income_tax_payable_timing",
    "what_changed": "It states a $198.4 million increase in income tax payables, attributed to the timing of payments.",
    "account": "income taxes payable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a $198.4 million increase in income tax payables related to timing of payments",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "earnings_quality_deferred_tax_increase_attributed_to_deferred_revenue",
    "what_changed": "It states a $213.1 million increase in deferred taxes, mainly because deferred revenue increased. The six-month 2025 comparative paragraph (mdna:60) cites both deferred revenue and the Section 174 capitalization of R&D costs. The 2026 paragraph cites only deferred revenue.",
    "account": "deferred tax assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "offset by a $213.1 million increase in deferred taxes primarily due to the increase in deferred revenue",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_investing_outflow_marketable_securities_purchases",
    "what_changed": "It states a six-month investing outflow of $2.4 billion: $4.3 billion of marketable securities purchases, 'partially offset' by $2.0 billion of maturities and sales. The paragraph names only marketable securities flows. The 8-K cash flow statement also has a purchases of property and equipment line and an 'Other' investing line, which the paragraph does not mention.",
    "account": "marketable securities; investing cash flows",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "purchases of marketable securities of $4.3 billion. These amounts were partially offset by proceeds from maturities and sales of marketable securities of $2.0 billion.",
    "paragraph_id": "0001596532-26-000175:mdna:62",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_financing_taxes_under_repurchase_plans_without_repurchases",
    "what_changed": "It states a six-month financing outflow of $1.5 million: proceeds from equity plans, offset by 'taxes paid under equity incentive and stock repurchase plans'. Yet mdna:69 says no shares were repurchased in the period. The text does not say what repurchase-plan taxes were paid. The 8-K cash flow statement has an 'Other' financing line.",
    "account": "financing cash flows (other); tax withholding on equity awards",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "cash used in financing activities was $1.5 million, consisting of proceeds from the issuance of stock under equity incentive plans, and offset by taxes paid under equity incentive and stock repurchase plans.",
    "paragraph_id": "0001596532-26-000175:mdna:65",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_not_made_in_six_months",
    "what_changed": "It states that no shares were repurchased during the six months ended June 30, 2026. It says $817.9 million remains under the $1.5 billion program authorized in May 2025; notes:70 says the same. The six-month 2025 comparative (mdna:66) states $983.0 million of open-market repurchases.",
    "account": "repurchases of common stock",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "We did not repurchase any shares during the six months ended June 30, 2026. As of June 30, 2026, the remaining authorized amount for repurchases under the Repurchase Program was $817.9 million.",
    "paragraph_id": "0001596532-26-000175:mdna:69",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_unrealized_loss_aging_table_collapsed",
    "what_changed": "The note change history shows the presentation of unrealized losses changed. The prior table had columns for losses within 12 months and for 12 months or greater, a Total column and a commercial paper row. The new table (notes:19) has only the within-12-months columns and no commercial paper row. A new sentence says positions in loss for 12 months or greater 'were not material'. The prose does not state their amount.",
    "account": "marketable securities; accumulated other comprehensive income (loss)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Debt securities in unrealized losses positions 12 months or greater were not material as of June 30, 2026",
    "paragraph_id": "0001596532-26-000175:notes:20",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_marketable_securities_weighted_average_duration",
    "what_changed": "It states a weighted-average remaining duration of about 1.4 years for marketable debt securities at June 30, 2026. The prior-quarter figure is not in my input.",
    "account": "marketable securities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The weighted-average remaining duration of our marketable debt securities is approximately 1.4 years as of June 30, 2026.",
    "paragraph_id": "0001596532-26-000175:notes:23",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_evaluation_inventory_balance",
    "what_changed": "The inventory footnote states evaluation inventory of $616.0 million at June 30, 2026 and $403.7 million at December 31, 2025. The March 31, 2026 figure is not in my input. The footnote gives no cause. MD&A (mdna:11) says trials and acceptance periods have increased the 'magnitude' of evaluation inventory, and that is the basis for the direction.",
    "account": "inventories (finished goods, evaluation inventory)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The balance includes evaluation inventory totaling $616.0 million and $403.7 million as of June 30, 2026 and December 31, 2025, respectively.",
    "paragraph_id": "0001596532-26-000175:notes:28",
    "explanation": false
  },
  {
    "id": "revenue_recognition_deferred_cost_of_goods_sold_tied_to_deferred_product_revenue",
    "what_changed": "The prepaid footnote now says the increase in deferred cost of goods sold as of June 30, 2026 was driven by a matching increase in deferred product revenue. I flag it as an inventory-type explanation: deferred cost of goods sold is the product cost of shipped units awaiting revenue recognition, and it is carried in prepaid expenses rather than inventories.",
    "account": "prepaid expenses and other current assets (deferred cost of goods sold)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase as of June 30, 2026 was driven by a corresponding increase in deferred product revenue.",
    "paragraph_id": "0001596532-26-000175:notes:32",
    "explanation": true
  },
  {
    "id": "revenue_recognition_other_performance_obligations_binding_product_agreements",
    "what_changed": "It states other performance obligations of $1.3 billion at June 30, 2026. These are $427.8 million of unbilled multi-year PCS and service contracts, and $875.1 million of binding contractual agreements with certain customers, mainly for future product shipments. The prior-quarter amounts are not in my input.",
    "account": "remaining performance obligations (unbilled)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Other performance obligations totaling $1.3 billion as of June 30, 2026 include unbilled multi-year PCS and service contract amounts of $427.8 million, and $875.1 million of binding contractual agreements with certain customers that are primarily related to future product shipments.",
    "paragraph_id": "0001596532-26-000175:notes:45",
    "explanation": false
  },
  {
    "id": "revenue_recognition_remaining_performance_obligations_timing",
    "what_changed": "It states $8.4 billion of future revenue at June 30, 2026 from contract liabilities, deferred revenue and other performance obligations. About 91% is expected over the next two years and 9% in years three to five. The prior-quarter amounts are not in my input.",
    "account": "remaining performance obligations; deferred revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Total revenue from our contract liabilities, deferred revenue and other performance obligations that is expected to be recognized in future periods amounts to $8.4 billion as of June 30, 2026. Approximately 91% of this future revenue is expected to be recognized over the next two years and the remaining 9% is expected to be recognized during the third to the fifth year.",
    "paragraph_id": "0001596532-26-000175:notes:47",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_velocloud_allocation_still_described_as_preliminary",
    "what_changed": "The acquisition note is carried as changed. Its visible change is the period reference: no change in goodwill carrying value for the three and six months ended June 30, 2026. The VeloCloud acquisition closed June 30, 2025, and as of June 30, 2026 the note still calls the purchase price allocation 'preliminary'. The text does not say whether the measurement period has closed, or whether the word is stale or signals open items.",
    "account": "goodwill; intangible assets",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The preliminary purchase price allocation based on the estimated fair values of the assets acquired and liabilities assumed as of the acquisition date, included $268.4 million of intangible assets, $148.0 million of goodwill and $116.4 million of net tangible liabilities assumed as of June 30, 2025.",
    "paragraph_id": "0001596532-26-000175:notes:53",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_purchase_commitments_amount_and_receipt_timing",
    "what_changed": "The note now states $9.7 billion of off-balance-sheet non-cancellable purchase commitments at June 30, 2026: $9.4 billion expected within 12 months and $0.3 billion after. The prior note stated $8.9 billion at March 31, 2026: $7.6 billion within 12 months and $1.3 billion after. MD&A (mdna:74) states the same June 30 amounts. MD&A (mdna:54) says the company 'increased' its purchase commitments, and that is the basis for the direction.",
    "account": "purchase commitments (off-balance-sheet); inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, we had non-cancellable purchase commitments not recorded on our balance sheet of $9.7 billion, of which $9.4 billion have expected receipt dates within 12 months, and $0.3 billion have expected receipt dates greater than 12 months.",
    "paragraph_id": "0001596532-26-000175:notes:60",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_purchase_obligation_scope_sentence_removed",
    "what_changed": "A sentence was removed from the commitments note. It said purchase obligations also cover software and technology licenses, property and equipment, and other corporate goods and services. The remaining text describes commitments for finished goods and strategic components placed through contract manufacturers. The text does not say whether the stated amount now excludes those other categories or the sentence was simply dropped. If the scope narrowed, the March 31 and June 30 amounts are not on the same basis.",
    "account": "purchase commitments (off-balance-sheet)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our purchase obligations also encompass software and technology licenses, property and equipment, and other corporate goods and services.",
    "paragraph_id": "0001596532-26-000078:note_history:1",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_contract_manufacturer_deposits",
    "what_changed": "The note now states deposits with contract manufacturers to secure purchase commitments of $124.4 million at June 30, 2026. The prior note stated $95.5 million at March 31, 2026, and both state $53.0 million at December 31, 2025. The deposits are recorded in prepaid expenses and other current assets and in other assets. The prose does not say which way they moved.",
    "account": "prepaid expenses and other current assets; other assets",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We also had deposits to our contract manufacturers to secure our purchase commitments in the amount of $124.4 million and $53.0 million as of June 30, 2026 and December 31, 2025, respectively",
    "paragraph_id": "0001596532-26-000175:notes:61",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_santa_clara_building_remaining_capex_estimate",
    "what_changed": "Remaining capital expenditures for the Santa Clara office, lab and data center building are now estimated at about $110.0 million to $135.0 million. The prior note estimated $130.0 million to $150.0 million as of March 31, 2026. Completion is still expected by the end of fiscal 2026. mdna:76 says the same, and mdna:54 lists the 'ongoing construction' among capital requirements. The direction reflects the prose saying the remaining spending is still expected.",
    "account": "property and equipment, net (construction-in-process)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, the estimated remaining capital expenditures related to this project are expected to be approximately $110.0 million to $135.0 million through the end of fiscal 2026 when we expect construction to be completed.",
    "paragraph_id": "0001596532-26-000175:notes:63",
    "explanation": false
  },
  {
    "id": "earnings_quality_unamortized_stock_compensation_cost",
    "what_changed": "It states $1.5 billion of unamortized compensation cost for unvested awards at June 30, 2026, to be recognized over a weighted-average period of about 3.9 years. The prior-quarter figures are not in my input.",
    "account": "stock-based compensation",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, there were $1.5 billion of unamortized compensation costs related to all unvested awards. The unamortized compensation costs are expected to be recognized over a weighted-average period of approximately 3.9 years.",
    "paragraph_id": "0001596532-26-000175:notes:78",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_cfo_trading_plan_modified",
    "what_changed": "New disclosure: on June 2, 2026 the CFO, Chantelle Breithaupt, modified her Rule 10b5-1 trading arrangement, first adopted December 11, 2025. It covers the sale of an undetermined number of shares that may be earned from performance-based RSUs and runs until December 31, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On June 2, 2026, Chantelle Breithaupt, our Senior Vice President and Chief Financial Officer, modified her Rule 10b5-1 trading arrangement previously adopted on December 11, 2025",
    "paragraph_id": "0001596532-26-000175:notes:93",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_director_trading_plan_adopted",
    "what_changed": "New disclosure: on June 9, 2026 director Mark Templeton adopted a Rule 10b5-1 trading arrangement to sell up to 50,000 shares. It runs until June 30, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On June 9, 2026, Mark Templeton, a member of our Board of Directors, adopted a Rule 10b5-1 trading arrangement providing for the sale from time to time of an aggregate of up to 50,000 shares of our common stock.",
    "paragraph_id": "0001596532-26-000175:notes:95",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_first_three_billion_revenue_quarter",
    "what_changed": "The Q2 2026 earnings release states revenue of $3.036 billion. It describes this as an increase of 12.1% over Q1 2026 and 37.7% over Q2 2025, and as the company's first $3+ billion quarter; the headline at 8k_2_02:5 and the CEO quote at 8k_2_02:9 repeat this. My input does not include the prior quarter's guidance for Q2.",
    "account": "revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Revenue of $3.036 billion, an increase of 12.1% compared to the first quarter of 2026, and an increase of 37.7% from the second quarter of 2025.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_non_gaap_eps_growth_headline",
    "what_changed": "The release headline claims 40% year-over-year growth in non-GAAP EPS. 8k_2_02:13 states GAAP and non-GAAP diluted EPS of $0.95 and $1.02, compared with $0.70 and $0.73 in Q2 2025. The CFO quote (8k_2_02:15) says 'EPS up 39.7%' without saying which EPS measure. The prior-year non-GAAP base was recast under the changed tax methodology (8k_2_02:40).",
    "account": "non-GAAP diluted net income per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Delivered 40% growth in non-GAAP EPS year-over-year as the company achieved its first $3+ billion revenue quarter.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:5",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_operating_margin_statement",
    "what_changed": "The release states GAAP and non-GAAP operating margins of 45.4% and 49.9%, compared with 44.7% and 48.8% in Q2 2025. The prose does not say which way they moved.",
    "account": "operating margin (GAAP and non-GAAP)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "GAAP and non-GAAP operating margin of 45.4% and 49.9%, respectively, compared to GAAP and non-GAAP operating margin of 44.7% and 48.8% in the second quarter of 2025.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:12",
    "explanation": false
  },
  {
    "id": "across_documents_broad_based_growth_versus_large_customer_mix",
    "what_changed": "The CFO quote calls Q2 'strong, broad-based growth'. The 10-Q MD&A attributes the gross margin decrease to a larger share of sales to large end customers (mdna:31). It also attributes the Non-Americas share fluctuations to the geographic mix of large global customers (mdna:25). The two documents describe where the growth came from differently; whether they conflict is for the supervisor.",
    "account": "revenue (customer mix); gross margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "reflects strong, broad-based growth, with revenue up 37.7% and EPS up 39.7%",
    "paragraph_id": "0001596532-26-000174:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "across_documents_new_ai_platform_launches_and_trial_inventory",
    "what_changed": "The release announces 1.6 Tbps AI fabric platforms, including liquid-cooled options, and the 7060XE7 Series (8k_2_02:19). The 10-Q says new product introductions bring customer trials and acceptance periods that increase evaluation inventory and product deferred revenue (mdna:11). It also cites new product introduction costs as an R&D driver (mdna:37).",
    "account": "inventories (evaluation inventory); deferred revenue (product)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Introduced 1.6 Tbps AI fabric platforms, including liquid-cooled options optimized for scale-up, scale-out, and scale-across networks.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_third_quarter_revenue_guidance",
    "what_changed": "The release guides Q3 2026 revenue to about $3.3 billion. It states a level, not a direction; comparing it with reported revenue is the numbers reader's job.",
    "account": "revenue",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Revenue of approximately $3.3 billion;",
    "paragraph_id": "0001596532-26-000174:8k_2_02:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_third_quarter_operating_margin_guidance",
    "what_changed": "The release guides Q3 2026 non-GAAP operating margin to 48 - 49%. It states a range, not a direction.",
    "account": "non-GAAP operating margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Non-GAAP operating margin of 48 - 49%",
    "paragraph_id": "0001596532-26-000174:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_third_quarter_eps_guidance",
    "what_changed": "The release guides Q3 2026 non-GAAP diluted EPS to between $1.06 and $1.08. It states a range, not a direction. Guidance excludes tax benefits on stock-based awards (8k_2_02:27).",
    "account": "non-GAAP diluted net income per share",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Non-GAAP diluted net income per share between $1.06 and $1.08.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:26",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_tax_methodology_change",
    "what_changed": "The release says the non-GAAP income tax methodology changed effective Q4 2025. Before, it excluded all tax benefits from stock-based awards, both the direct excess benefits and other discrete indirect effects. Now it excludes only the direct excess tax benefits and no longer excludes the discrete indirect effects (continued in 8k_2_02:55). Management says this better matches industry practice. All prior non-GAAP periods in the release are recast.",
    "account": "non-GAAP net income; non-GAAP income tax effect",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Effective the fourth quarter of fiscal year 2025, the company updated its methodology for calculating the income tax effect of non-GAAP adjustments.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:53",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_prior_period_recast_increase",
    "what_changed": "The reconciliation footnote states that applying the change retrospectively increased non-GAAP net income for the three and six months ended June 30, 2025 by $10.7 million and $30.4 million. It increased non-GAAP diluted EPS by nil and $0.03. The release's year-over-year non-GAAP growth claims are measured against these recast comparatives.",
    "account": "non-GAAP net income (prior-year comparatives); non-GAAP diluted net income per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The retrospective application of this change resulted in an increase to non-GAAP net income of $10.7 million and $30.4 million for the three and six months ended June 30, 2025, respectively.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:40",
    "explanation": false
  }
]
```

## Paragraphs carried as text with no item

### MD&A
- 0001596532-26-000175:mdna:8 — business-strategy wording ('network-as-a-service approach'). Prior wording not in input; no account, amount, policy or estimate. Insufficient to call it a substantive change.
- 0001596532-26-000175:mdna:16 — rest of the mdna:15 sentence (tariff, cost pass-through, macro demand). Covered by narrative_signs_of_operating_pressure_memory_and_silicon_supply_tightening.
- 0001596532-26-000175:mdna:18 — heading; period rolled forward.
- 0001596532-26-000175:mdna:20 — revenue/cost table; amounts only.
- 0001596532-26-000175:mdna:22 — geographic revenue table; amounts only.
- 0001596532-26-000175:mdna:29 — rest of the mdna:28 sentence. Covered by results_against_expectations_cost_of_revenue_attributed_to_revenue_growth.
- 0001596532-26-000175:mdna:34 — operating expense table; amounts only.
- 0001596532-26-000175:mdna:46 — other income table; amounts only.
- 0001596532-26-000175:mdna:50 — tax table; amounts only.
- 0001596532-26-000175:mdna:55 — rest of the mdna:54 sentence. Covered by liquidity_and_capital_purchase_commitments_increased_for_memory_and_silicon.
- 0001596532-26-000175:mdna:57 — cash flow summary table; amounts only.
- 0001596532-26-000175:mdna:60 — six-month 2025 comparative operating cash flow description; period rolled forward. Its Section 174 reference is cited in earnings_quality_deferred_tax_increase_attributed_to_deferred_revenue.
- 0001596532-26-000175:mdna:63 — six-month 2025 comparative investing description (VeloCloud acquisition); period rolled forward.
- 0001596532-26-000175:mdna:66 — six-month 2025 comparative financing description; period rolled forward. Cited in liquidity_and_capital_share_repurchases_not_made_in_six_months.
- 0001596532-26-000175:mdna:68 — repurchase program description, continuing into mdna:69. Covered by liquidity_and_capital_share_repurchases_not_made_in_six_months.
- 0001596532-26-000175:mdna:74 — purchase obligations; the same June 30, 2026 amounts as notes:60. Covered by liquidity_and_capital_purchase_commitments_amount_and_receipt_timing.
- 0001596532-26-000175:mdna:76 — building capex estimate, same text as notes:63. Covered by liquidity_and_capital_santa_clara_building_remaining_capex_estimate.
- 0001596532-26-000175:mdna:78 — no off-balance-sheet arrangements; date rolled forward.

### Notes
- 0001596532-26-000175:notes:4 — basis of presentation; date rolled forward (the note change history confirms only the period reference changed).
- 0001596532-26-000175:notes:9 — pending ASU 2024-03, a disclosure-only standard. Carried as changed but prior wording not in input; no amount or policy for the period. Insufficient.
- 0001596532-26-000175:notes:10 — pending ASU 2025-11, a disclosure-only standard. Carried as changed but prior wording not in input, so I cannot tell whether it is new or reworded. Insufficient.
- 0001596532-26-000175:notes:13 — fair value hierarchy table; amounts only.
- 0001596532-26-000175:notes:14 — no transfers between levels; date rolled forward.
- 0001596532-26-000175:notes:16 — amortized cost / unrealized gains and losses table; amounts only.
- 0001596532-26-000175:notes:17 — statement of no intent to sell and no credit losses. It appears that only the period reference was rolled forward; prior wording not in input.
- 0001596532-26-000175:notes:19 — new single-bucket unrealized loss table. Covered by structure_and_disclosure_changes_unrealized_loss_aging_table_collapsed.
- 0001596532-26-000175:notes:21 — no maturities beyond three years; date rolled forward.
- 0001596532-26-000175:notes:22 — maturity table; amounts only.
- 0001596532-26-000175:notes:27 — inventory table; amounts only.
- 0001596532-26-000175:notes:31 — prepaid table; amounts only.
- 0001596532-26-000175:notes:35 — property and equipment table; amounts only.
- 0001596532-26-000175:notes:39 — contract liabilities rollforward table; amounts only.
- 0001596532-26-000175:notes:40 — split of contract liabilities into current and non-current; amounts only.
- 0001596532-26-000175:notes:43 — deferred revenue rollforward table; amounts only.
- 0001596532-26-000175:notes:50 — other income table; amounts only.
- 0001596532-26-000175:notes:56 — intangible assets table; amounts only.
- 0001596532-26-000175:notes:58 — future amortization table; amounts only.
- 0001596532-26-000175:notes:59 — heading.
- 0001596532-26-000175:notes:62 — heading.
- 0001596532-26-000175:notes:64 — heading.
- 0001596532-26-000175:notes:65 — guarantees and indemnifications. The note change history for this tag does not list it as changed; no change in substance.
- 0001596532-26-000175:notes:66 — heading.
- 0001596532-26-000175:notes:67 — legal proceedings lead-in. The note change history does not list it as changed; no change in substance.
- 0001596532-26-000175:notes:68 — contingent-loss provisions; date rolled forward (the note change history confirms only the date changed).
- 0001596532-26-000175:notes:69 — heading.
- 0001596532-26-000175:notes:70 — repurchase program, same content as mdna:68 and mdna:69. Covered by liquidity_and_capital_share_repurchases_not_made_in_six_months.
- 0001596532-26-000175:notes:74 — RSU activity table; amounts only.
- 0001596532-26-000175:notes:77 — stock-based compensation table; amounts only.
- 0001596532-26-000175:notes:80 — EPS table; amounts only.
- 0001596532-26-000175:notes:82 — antidilutive awards table; amounts only.
- 0001596532-26-000175:notes:84 — tax table; amounts only.
- 0001596532-26-000175:notes:85 — same sentence as mdna:51. Covered by earnings_quality_effective_tax_rate_equity_compensation_benefit_decrease.
- 0001596532-26-000175:notes:89 — geographic revenue table; amounts only.
- 0001596532-26-000175:notes:90 — U.S. revenue footnote; amounts only.
- 0001596532-26-000175:notes:92 — long-lived assets by geography table; amounts only.
- 0001596532-26-000175:notes:94 — rest of the notes:93 sentence. Covered by related_parties_contingencies_and_subsequent_events_cfo_trading_plan_modified.

### Note change history (reference only; mapped to the notes paragraphs above)
- 0001596532-26-000175:note_history:1 and 0001596532-26-000078:note_history:1 — the purchase commitments paragraph. Covered by liquidity_and_capital_purchase_commitments_amount_and_receipt_timing and structure_and_disclosure_changes_purchase_obligation_scope_sentence_removed.
- 0001596532-26-000175:note_history:2 and 0001596532-26-000078:note_history:2 — deposits. Covered by liquidity_and_capital_contract_manufacturer_deposits.
- 0001596532-26-000175:note_history:3 and 0001596532-26-000078:note_history:5 — building capex. Covered by liquidity_and_capital_santa_clara_building_remaining_capex_estimate.
- 0001596532-26-000175:note_history:4 and 0001596532-26-000078:note_history:4 — contingent-loss provisions; date rolled forward.
- 0001596532-26-000175:note_history:6 and 0001596532-26-000078:note_history:6 — basis of presentation; date rolled forward.
- 0001596532-26-000175:note_history:7, 0001596532-26-000175:note_history:8 and 0001596532-26-000078:note_history:9 — unrealized loss table. Covered by structure_and_disclosure_changes_unrealized_loss_aging_table_collapsed.

### Item 4 (controls)
- 0001596532-26-000175:item_4_controls:1 — heading.
- 0001596532-26-000175:item_4_controls:2 — heading.
- 0001596532-26-000175:item_4_controls:3 — disclosure controls concluded effective as of June 30, 2026; date rolled forward. No material weakness or remediation language. Prior Item 4 wording not in input.
- 0001596532-26-000175:item_4_controls:4 — heading.
- 0001596532-26-000175:item_4_controls:5 — no changes in internal control over financial reporting during the quarter; date rolled forward.
- 0001596532-26-000175:item_4_controls:6 — heading.
- 0001596532-26-000175:item_4_controls:7 — standard inherent-limitations wording.

### 8-K 0001596532-26-000174 (Items 2.02 and 9.01)
- 0001596532-26-000174:8k_2_02:1 — exhibit header.
- 0001596532-26-000174:8k_2_02:2 — document label.
- 0001596532-26-000174:8k_2_02:3 — exhibit label.
- 0001596532-26-000174:8k_2_02:4 — title.
- 0001596532-26-000174:8k_2_02:6 — Fortune 500 and Gartner recognition; no accounting substance.
- 0001596532-26-000174:8k_2_02:8 — dateline.
- 0001596532-26-000174:8k_2_02:9 — CEO quote on the first $3 billion quarter. Covered by results_against_expectations_release_first_three_billion_revenue_quarter.
- 0001596532-26-000174:8k_2_02:10 — heading.
- 0001596532-26-000174:8k_2_02:13 — GAAP and non-GAAP EPS amounts. Covered by results_against_expectations_release_non_gaap_eps_growth_headline.
- 0001596532-26-000174:8k_2_02:14 — pointer to the reconciliation; standard wording.
- 0001596532-26-000174:8k_2_02:16 — heading.
- 0001596532-26-000174:8k_2_02:17 — webinar promotion; no accounting substance.
- 0001596532-26-000174:8k_2_02:18 — Gartner recognition; no accounting substance.
- 0001596532-26-000174:8k_2_02:19 — 7060XE7 product launch. Covered by across_documents_new_ai_platform_launches_and_trial_inventory.
- 0001596532-26-000174:8k_2_02:20 — technology description; no accounting substance (context for the new-platform item).
- 0001596532-26-000174:8k_2_02:21 — rest of 8k_2_02:20; technology description.
- 0001596532-26-000174:8k_2_02:22 — heading.
- 0001596532-26-000174:8k_2_02:23 — lead-in to the guidance. Covered by the three guidance items.
- 0001596532-26-000174:8k_2_02:27 — list of items excluded from non-GAAP guidance; no amount. Cited in results_against_expectations_release_third_quarter_eps_guidance.
- 0001596532-26-000174:8k_2_02:28 — heading.
- 0001596532-26-000174:8k_2_02:29 — conference call logistics.
- 0001596532-26-000174:8k_2_02:30 — webcast logistics.
- 0001596532-26-000174:8k_2_02:31 — company name header.
- 0001596532-26-000174:8k_2_02:32 — statement title.
- 0001596532-26-000174:8k_2_02:33 — units line.
- 0001596532-26-000174:8k_2_02:34 — income statement table; amounts only.
- 0001596532-26-000174:8k_2_02:35 — page number.
- 0001596532-26-000174:8k_2_02:36 — company name header.
- 0001596532-26-000174:8k_2_02:37 — reconciliation title.
- 0001596532-26-000174:8k_2_02:38 — units line.
- 0001596532-26-000174:8k_2_02:39 — GAAP to non-GAAP reconciliation table; amounts only.
- 0001596532-26-000174:8k_2_02:41 — company name header.
- 0001596532-26-000174:8k_2_02:42 — statement title.
- 0001596532-26-000174:8k_2_02:43 — units line.
- 0001596532-26-000174:8k_2_02:44 — balance sheet table; amounts only.
- 0001596532-26-000174:8k_2_02:45 — page number.
- 0001596532-26-000174:8k_2_02:46 — company name header.
- 0001596532-26-000174:8k_2_02:47 — statement title.
- 0001596532-26-000174:8k_2_02:48 — units line.
- 0001596532-26-000174:8k_2_02:49 — cash flow statement table; amounts only. Its 'Other' investing and financing lines are cited in the mdna:62 and mdna:65 items.
- 0001596532-26-000174:8k_2_02:50 — heading.
- 0001596532-26-000174:8k_2_02:51 — forward-looking statements risk list. No prior release is in my input to compare against. Insufficient.
- 0001596532-26-000174:8k_2_02:52 — heading.
- 0001596532-26-000174:8k_2_02:54 — page number.
- 0001596532-26-000174:8k_2_02:55 — rest of the 8k_2_02:53 methodology description. Covered by earnings_quality_non_gaap_tax_methodology_change.
- 0001596532-26-000174:8k_2_02:56 — standard statement of how non-GAAP measures are used.
- 0001596532-26-000174:8k_2_02:57 — standard non-GAAP limitations wording.
- 0001596532-26-000174:8k_2_02:58 — heading.
- 0001596532-26-000174:8k_2_02:59 — company description.
- 0001596532-26-000174:8k_2_02:60 — trademark notice.
- 0001596532-26-000174:8k_2_02:61 — investor contacts.
- 8-K item-code list and late-filing section — not paragraphs. They show no Item 4.01 or 4.02 and no late-filing notification on or before 2026-08-05. The 2026-06-02 Item 5.07 8-K has no body in my input.

## Insufficient

- Item 1A diff: not in my input. I cannot report risk-factor changes.
- Exhibit 21 diff: not in my input.
- Exhibit 10: none was pulled on trigger; none is in my input.
- Auditor's report (interim review report): not in my input.
- Prior Item 4 wording: not in my input. The current conclusion (effective, no changes in internal control) cannot be diffed against the prior quarter.
- MD&A prior wording: not in my input for any paragraph carried as text. Each MD&A item says what the text now says; the exact delta from the March 31, 2026 10-Q cannot be isolated.
- 0001596532-26-000175:mdna:8, 0001596532-26-000175:notes:9, 0001596532-26-000175:notes:10 and 0001596532-26-000174:8k_2_02:51 — carried as text, but I cannot tell from my input whether anything substantive changed.
