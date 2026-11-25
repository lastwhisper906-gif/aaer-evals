# report_notes_text — ANET 10-Q 0001596532-26-000175 (quarter ended June 30, 2026)

## Inputs and scope

- Read in full: `input_notes.md`, `input_notes_history.md`, `input_mdna.md`, `input_controls.md`, `input_8k.md`, `input_prior_predictions.md`.
- Directory check: only the six input files are present. There is no trend table, price, return, short-interest or outcome data, and no other company's files. The 8-K section holds the Item 2.02 body (exhibit 99.1), including the release's own financial tables. These are 8-K body text and are allowed.
- Not in my input:
  - Auditor's report: the controls file carries only Item 4, as expected for a 10-Q.
  - Item 1A diff.
  - Exhibit 21 diff.
  - Any Exhibit 10.
  - The body of the 2026-06-02 8-K (Item 5.07). Only its item code is listed.
  - Item-code list: since the prior 10-Q, the 8-Ks are the 2026-06-02 filing (5.07) and the 2026-08-04 filing (2.02, 9.01). There is no 4.01, 4.02 or 5.02. The input lists no late-filing notifications.
- Prior flags: none on record.
- How deltas are stated:
  - MD&A and notes paragraphs marked as text differ from 0001596532-26-000078. The prior wording is in my input only where the note change history shows it, which covers notes:4, 19/20, 60, 61, 63 and 68.
  - For every other paragraph, an item says what the text now says. It cannot quote the old wording.
  - No item compares magnitudes. Where the prose says a balance rose, the item says the prose says so.

## Items

```json
[
  {
    "id": "revenue_recognition_customer_trials_and_acceptance_periods",
    "what_changed": "Carried as changed from the prior 10-Q; the prior wording is not in my input. The text now says the period of new product introductions has led to more customer trials and more contracts with acceptance periods, especially in AI Ethernet. It says this has increased the volatility and magnitude of evaluation inventory and product deferred revenue, which may cause quarterly and annual revenue variability. Management names trials and acceptance terms as the cause of the evaluation-inventory and product-deferral balances. The inventory footnote (notes:28) gives the evaluation-inventory amount.",
    "account": "Inventories (evaluation inventory within finished goods); Deferred revenue (product)",
    "expected_direction": "up",
    "horizon": "this quarter and 12 months",
    "quote": "This has resulted in increased customer trials and contracts with acceptance periods, and an increase in the volatility and magnitude of our evaluation inventory and product deferred revenue balances, which in turn may create variability in our revenue results on a quarterly and annual basis.",
    "paragraph_id": "0001596532-26-000175:mdna:11",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_trial_returns_and_inventory_write_down",
    "what_changed": "Same paragraph, carried as changed; the prior wording is not in my input. It now says that if trial or acceptance requirements are not met, the company may have to accept product returns. That would block revenue recognition on those transactions and may lead to inventory write-downs. This is a stated path from acceptance-term deferrals to an inventory write-down charge.",
    "account": "Inventories / inventory write-downs (cost of revenue); Product revenue",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "if we are not able to satisfy the requirements under customer trials or contracts with acceptance periods, we may be required to accept product returns from our customers, which would prevent us from recognizing revenue on such transactions and may result in the write-down of inventory.",
    "paragraph_id": "0001596532-26-000175:mdna:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_ai_demand_trajectory_unknown",
    "what_changed": "Same paragraph, carried as changed; the prior wording is not in my input. It now makes four points. Large customers' focus on AI has at times come with fewer or differently mixed previously planned purchases and with cost-reduction measures. Some advanced offerings come from potential new market entrants. The long-term path of AI-driven networking demand is unknown. Demand for new products is hard to forecast and can make revenue volatile.",
    "account": "Revenue (product)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "although the focus on deployment of AI-enabled solutions has driven increased demand for networking, the long-term trajectory is unknown",
    "paragraph_id": "0001596532-26-000175:mdna:11",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_inventory_and_purchase_commitments_elevated",
    "what_changed": "Carried as changed; the prior wording is not in my input. The text now says inventory and purchase commitments are expected to stay elevated and volatile. It gives four reasons: new product introductions, shifts in customer demand, tightening supply and changing supplier lead times. These are management's stated causes for the inventory level.",
    "account": "Inventories; Purchase commitments (off-balance sheet)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we expect inventory and purchase commitments to remain elevated and subject to volatility as a result of new product introductions, shifts in customer demand, tightening supply conditions and fluctuations in supplier lead times.",
    "paragraph_id": "0001596532-26-000175:mdna:15",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_excess_obsolete_and_supplier_liability_risk",
    "what_changed": "Same paragraph, carried as changed. It now says this volatility brings a heightened risk of charges for excess or obsolete inventory and for supplier liabilities. This is a forward statement about the excess-and-obsolete inventory reserve and the supplier-liability accrual.",
    "account": "Inventory reserves (excess and obsolete); Supplier liability accrual; Cost of revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "This volatility creates a heightened risk of excess or obsolete inventory and supplier liability charges.",
    "paragraph_id": "0001596532-26-000175:mdna:15",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_and_silicon_gross_margin",
    "what_changed": "Same paragraph, carried as changed. It now gives tightening supply in the memory and silicon markets as an example of supply-chain inflation and material scarcity. It says these 'have continued to put pressure on our gross margin'. The same memory-and-silicon wording appears in the liquidity paragraph (mdna:54) as a reason purchase commitments were increased.",
    "account": "Gross margin; Cost of revenue (product)",
    "expected_direction": "down",
    "horizon": "this quarter and 12 months",
    "quote": "supply chain inflation and material scarcity, such as the tightening of supply conditions in the memory and silicon markets, have continued to put pressure on our gross margin.",
    "paragraph_id": "0001596532-26-000175:mdna:15",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_cost_pass_through_and_tariffs",
    "what_changed": "Continuation of the mdna:15 sentence, carried as changed. It now says gross margins 'could be further impacted' if tariff or non-tariff measures escalate, or supply conditions worsen, and the costs cannot be passed on to customers. It adds that broader macroeconomic instability could hurt demand.",
    "account": "Gross margin; Revenue",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "to pass on these costs to customers, our gross margins could be further impacted.",
    "paragraph_id": "0001596532-26-000175:mdna:16",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_growth_drivers",
    "what_changed": "Carried as changed; the comparison now covers the three and six months to June 30, 2026, and the prior wording is not in my input. It gives three drivers. Product revenue growth comes from healthy customer demand and higher shipments of switching and routing platforms. Service revenue growth comes from initial and renewal support contracts as the installed base expands. Changes in the non-Americas share of revenue come from the geographic mix of sales to large global customers.",
    "account": "Product revenue; Service revenue; Revenue by geography",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "This increase reflects healthy customer demand and higher shipments of our switching and routing platforms across our customer base.",
    "paragraph_id": "0001596532-26-000175:mdna:25",
    "explanation": false
  },
  {
    "id": "earnings_quality_cost_of_revenue_attributed_to_revenue_growth",
    "what_changed": "Carried as changed with new periods and amounts. The text says the cost-of-revenue increase was driven 'primarily' by 'a corresponding increase in product and service revenues'; the sentence finishes in mdna:29. The same paragraph gives its own percentage changes for cost of revenue. Separately, mdna:31 reports a gross margin decline and attributes it to customer mix. Whether the cost increase actually 'corresponds' to revenue is for the numbers reader to test.",
    "account": "Cost of revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These increases were primarily driven by a corresponding increase",
    "paragraph_id": "0001596532-26-000175:mdna:28",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_gross_margin_large_customer_mix",
    "what_changed": "Carried as changed. It now says gross margin decreased for the three and six months against 2025. It attributes the decrease primarily to a larger share of sales going to large end customers, who get higher discounts. It does not mention the memory and silicon cost pressure that mdna:15 says has 'continued to put pressure on our gross margin'.",
    "account": "Gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease was primarily driven by an increased proportion of our sales to large end customers who generally receive higher discounts.",
    "paragraph_id": "0001596532-26-000175:mdna:31",
    "explanation": false
  },
  {
    "id": "earnings_quality_research_and_development_new_product_introduction_costs",
    "what_changed": "Carried as changed. The text now attributes the R&D increase to personnel costs and to new product introduction costs. Each driver is given with separate three-month and six-month amounts. New product introduction costs depend on the timing of the introductions described in mdna:11.",
    "account": "Research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by increased personnel costs of $33.3 million and $59.4 million, as well as an increase in new product introduction costs of $8.3 million and $58.8 million.",
    "paragraph_id": "0001596532-26-000175:mdna:37",
    "explanation": false
  },
  {
    "id": "earnings_quality_sales_and_marketing_headcount_growth",
    "what_changed": "Carried as changed. The text now attributes the sales and marketing increase for the three and six months to personnel costs from headcount growth.",
    "account": "Sales and marketing expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "which was primarily driven by increased personnel costs due to headcount growth.",
    "paragraph_id": "0001596532-26-000175:mdna:40",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_income_on_higher_balances",
    "what_changed": "Carried as changed. It now attributes the favorable movement in other income to higher interest income. It says interest income rose 'due to an increase in our cash and marketable securities balances'.",
    "account": "Other income (expense), net (interest income); Cash, cash equivalents and marketable securities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by increased interest income of $32.0 million and $50.9 million due to an increase in our cash and marketable securities balances.",
    "paragraph_id": "0001596532-26-000175:mdna:47",
    "explanation": false
  },
  {
    "id": "revenue_recognition_large_customer_extended_payment_terms",
    "what_changed": "The liquidity paragraph is carried as changed; the prior wording is not in my input. It now says certain large customer arrangements include extended payment terms, which may cause timing differences in working capital and operating cash flows. That is a stated cause bearing on receivables. The operating cash flow paragraph (mdna:59) attributes the half's receivables increase to billings and does not mention extended terms.",
    "account": "Accounts receivable; Operating cash flow",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "our working capital and operating cash flows may experience timing differences as a result of certain large customer arrangements that include extended payment terms.",
    "paragraph_id": "0001596532-26-000175:mdna:54",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_purchase_commitments_raised_for_ai_and_memory_supply",
    "what_changed": "Same paragraph, carried as changed. It now says the company 'increased' purchase commitments for two reasons: to respond to the rapid deployment of AI networks and to navigate tightening memory and silicon supply. It also says inventory and purchase commitments are expected to stay elevated and volatile as new products ramp.",
    "account": "Purchase commitments (off-balance sheet); Inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we have increased our purchase commitments to respond to the rapid deployment of AI networks, and to navigate the tightening supply within the memory and silicon markets",
    "paragraph_id": "0001596532-26-000175:mdna:54",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_working_capital_requirements_to_increase",
    "what_changed": "Continuation of the mdna:54 sentence. It now says the larger commitments are also meant to reduce overall lead times. It also says they 'will increase our working capital requirements in the future'.",
    "account": "Working capital (inventories, supplier deposits, prepaid); Operating cash flow",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "and reduce overall lead times, which will increase our working capital requirements in the future.",
    "paragraph_id": "0001596532-26-000175:mdna:55",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_attributed_to_billings",
    "what_changed": "The operating cash flow paragraph is rewritten for the six months to June 30, 2026. It says receivables increased and attributes the increase to higher product and service billings. It does not mention the extended payment terms named in mdna:54.",
    "account": "Accounts receivable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in accounts receivable of $379.3 million due to increased product and service billings",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": true
  },
  {
    "id": "revenue_recognition_deferred_revenue_build_from_acceptance_terms",
    "what_changed": "Same paragraph. It attributes the half's deferred revenue increase to product deferred revenue on contracts with acceptance terms, named first, and to PCS contracts, named second. The prior-year comparative (mdna:60) lists them the other way round: PCS contracts first, acceptance-term product deferrals second.",
    "account": "Deferred revenue (product and PCS)",
    "expected_direction": "up",
    "horizon": "this quarter; recognized as revenue when acceptance is obtained, within 12 months",
    "quote": "an increase in deferred revenue of $1.5 billion primarily resulting from an increase in product deferred revenue related to customer contracts with acceptance terms and an increase in customer PCS contracts",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "earnings_quality_inventory_increase_without_stated_cause",
    "what_changed": "Same paragraph. It states that inventory increased in the half but gives no cause. The same paragraph does give causes for receivables, other assets, deferred revenue and tax payables. Forward-looking reasons for elevated inventory appear only in mdna:15 and mdna:54.",
    "account": "Inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "and a $288.2 million increase in inventory.",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "earnings_quality_deferred_taxes_attributed_to_deferred_revenue",
    "what_changed": "Same paragraph. It attributes the change in deferred taxes primarily to the increase in deferred revenue. The prior-year comparative (mdna:60) cites both deferred revenue and the capitalization of R&D costs under IRC Section 174. The 2026 sentence cites deferred revenue only.",
    "account": "Deferred tax assets; Deferred income taxes (cash flow)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "offset by a $213.1 million increase in deferred taxes primarily due to the increase in deferred revenue.",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_income_tax_payable_timing",
    "what_changed": "Same paragraph. It lists higher income tax payables as a working-capital inflow for the half. The text itself says this is 'related to timing of payments'.",
    "account": "Income taxes payable; Operating cash flow",
    "expected_direction": "up",
    "horizon": "this quarter; reverses when the taxes are paid",
    "quote": "a $198.4 million increase in income tax payables related to timing of payments",
    "paragraph_id": "0001596532-26-000175:mdna:59",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_financing_taxes_under_repurchase_plans",
    "what_changed": "The financing paragraph for the six months to June 30, 2026 is carried as changed. It says financing flows were equity-plan proceeds offset by 'taxes paid under equity incentive and stock repurchase plans'. This is in a half in which the notes say no shares were repurchased (notes:70).",
    "account": "Financing cash flows; Stockholders' equity",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "offset by taxes paid under equity incentive and stock repurchase plans.",
    "paragraph_id": "0001596532-26-000175:mdna:65",
    "explanation": false
  },
  {
    "id": "earnings_quality_deferred_cost_of_goods_sold_tied_to_product_deferrals",
    "what_changed": "The footnote to the prepaid expenses table is carried as changed; the prior wording is not in my input. It now attributes the increase in deferred cost of goods sold at June 30, 2026 to a matching increase in deferred product revenue. The balance sits in prepaid expenses and other current assets and is the cost of product shipped whose revenue is deferred. mdna:59 gives the same cause for the increase in other assets: 'deferred cost of sales associated with higher product revenue deferrals'.",
    "account": "Prepaid expenses and other current assets (deferred cost of goods sold)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase as of June 30, 2026 was driven by a corresponding increase in deferred product revenue.",
    "paragraph_id": "0001596532-26-000175:notes:32",
    "explanation": true
  },
  {
    "id": "earnings_quality_effective_tax_rate_lower_stock_award_benefits",
    "what_changed": "The tax note is carried as changed and now covers three and six months. It attributes the 'increase in the effective tax rate' against 2025 primarily to lower tax benefits from equity-based compensation, and mdna:51 repeats the sentence. Separately, the release (8k_2_02:53) describes a change to the non-GAAP method for tax effects of stock-based awards.",
    "account": "Provision for income taxes; Effective tax rate",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "was primarily due to a decrease in tax benefits attributable to equity-based compensation.",
    "paragraph_id": "0001596532-26-000175:notes:85",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_purchase_obligation_scope_sentence_removed",
    "what_changed": "The purchase-commitment note (now 0001596532-26-000175:notes:60) has dropped the prior sentence saying purchase obligations 'also encompass software and technology licenses, property and equipment, and other corporate goods and services'. The note does not say whether the commitment total now excludes those categories. That leaves open whether the totals in the two 10-Qs are comparable. The MD&A version (mdna:74) also lacks the sentence.",
    "account": "Purchase commitments (off-balance sheet)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our purchase obligations also encompass software and technology licenses, property and equipment, and other corporate goods and services.",
    "paragraph_id": "0001596532-26-000078:note_history:1",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_purchase_commitments_amount_and_receipt_timing",
    "what_changed": "The note now states non-cancellable purchase commitments of $9.7 billion at June 30, 2026: $9.4 billion expected within 12 months and $0.3 billion later. The prior 10-Q stated $8.9 billion at March 31, 2026, with $7.6 billion within 12 months and $1.3 billion later (note history). The MD&A prose (mdna:54) says commitments were 'increased'. Any comparison of the figures is the numbers reader's, subject to the scope point in the item on the removed sentence.",
    "account": "Purchase commitments (off-balance sheet); Inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we had non-cancellable purchase commitments not recorded on our balance sheet of $9.7 billion, of which $9.4 billion have expected receipt dates within 12 months, and $0.3 billion have expected receipt dates greater than 12 months.",
    "paragraph_id": "0001596532-26-000175:notes:60",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_campus_construction_remaining_capex_estimate",
    "what_changed": "The remaining capital expenditure on the Santa Clara building is now estimated at approximately $110.0 million to $135.0 million through the end of fiscal 2026. The prior 10-Q stated approximately $130.0 million to $150.0 million; in the note history the old paragraph shows as removed and the new one as added. Completion is still expected by the end of fiscal 2026. The same estimate appears at mdna:76.",
    "account": "Property and equipment (construction-in-process); Capital expenditures",
    "expected_direction": "up",
    "horizon": "next quarter and through the end of fiscal 2026",
    "quote": "the estimated remaining capital expenditures related to this project are expected to be approximately $110.0 million to $135.0 million through the end of fiscal 2026 when we expect construction to be completed.",
    "paragraph_id": "0001596532-26-000175:notes:63",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_unrealized_loss_aging_columns_dropped",
    "what_changed": "The unrealized-loss table (notes:19) now shows only the 'within 12 months' columns. The prior table's '12 months or greater' and 'Total' columns and its commercial paper row are gone (note history). A new sentence says positions in a loss for 12 months or more were not material at June 30, 2026.",
    "account": "Marketable securities; Accumulated other comprehensive income (loss)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Debt securities in unrealized losses positions 12 months or greater were not material as of June 30, 2026",
    "paragraph_id": "0001596532-26-000175:notes:20",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_no_share_repurchases_in_half",
    "what_changed": "The repurchase paragraph now covers the six months to June 30, 2026. It says no shares were repurchased in the half and that $817.9 million of the May 2025 $1.5 billion authorization remains; mdna:69 repeats both statements. MD&A (mdna:47) says cash and marketable securities balances increased.",
    "account": "Common stock repurchases; Cash and marketable securities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We did not repurchase any shares during the six months ended June 30, 2026.",
    "paragraph_id": "0001596532-26-000175:notes:70",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_cfo_trading_plan_modified",
    "what_changed": "New for the quarter: on June 2, 2026 the CFO modified her Rule 10b5-1 trading arrangement, first adopted December 11, 2025. It covers sales of an undetermined number of shares earned from performance-based RSUs and runs until December 31, 2026. The disclosure continues at notes:94.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "through December 31, 2026",
    "quote": "On June 2, 2026, Chantelle Breithaupt, our Senior Vice President and Chief Financial Officer, modified her Rule 10b5-1 trading arrangement previously adopted on December 11, 2025",
    "paragraph_id": "0001596532-26-000175:notes:93",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_director_trading_plan_adopted",
    "what_changed": "New for the quarter: on June 9, 2026 director Mark Templeton adopted a Rule 10b5-1 trading arrangement to sell up to 50,000 shares. It runs until June 30, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months (through June 30, 2027)",
    "quote": "On June 9, 2026, Mark Templeton, a member of our Board of Directors, adopted a Rule 10b5-1 trading arrangement providing for the sale from time to time of an aggregate of up to 50,000 shares of our common stock.",
    "paragraph_id": "0001596532-26-000175:notes:95",
    "explanation": false
  },
  {
    "id": "results_against_expectations_headline_non_gaap_eps_growth",
    "what_changed": "The second-quarter release headline claims 40% year-over-year growth in non-GAAP EPS. It also calls this the company's first quarter with revenue above $3 billion. The prior-year non-GAAP base was recast under the changed tax method (8k_2_02:40, 8k_2_02:53).",
    "account": "Non-GAAP diluted EPS; Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Delivered 40% growth in non-GAAP EPS year-over-year as the company achieved its first $3+ billion revenue quarter.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:5",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_sequential_and_annual_growth",
    "what_changed": "The release states quarterly revenue of $3.036 billion. It gives growth of 12.1% over the first quarter of 2026 and 37.7% over the second quarter of 2025. The outlook for this quarter from the May 5, 2026 release is not in my input, so I cannot tell from my files whether the quarter landed inside guidance.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Revenue of $3.036 billion, an increase of 12.1% compared to the first quarter of 2026, and an increase of 37.7% from the second quarter of 2025.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "across_documents_cfo_quote_eps_growth_basis_unstated",
    "what_changed": "The CFO quote says 'EPS up 39.7%' without saying whether that is GAAP or non-GAAP EPS. The headline bullet (8k_2_02:5) says '40% growth in non-GAAP EPS'. Which measure each figure uses, and whether against the recast or original base, is for the numbers reader to reconcile.",
    "account": "Diluted EPS (GAAP and non-GAAP)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "with revenue up 37.7% and EPS up 39.7%.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "across_documents_broad_based_growth_versus_large_customer_mix",
    "what_changed": "The CFO calls the quarter 'strong, broad-based growth'. The 10-Q attributes the gross margin decline to 'an increased proportion of our sales to large end customers' (mdna:31). The release's own risk list names 'large purchases by a limited number of customers' (8k_2_02:51). The two documents describe the customer make-up of growth differently.",
    "account": "Revenue (customer concentration); Gross margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "reflects strong, broad-based growth",
    "paragraph_id": "0001596532-26-000174:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "results_against_expectations_next_quarter_revenue_outlook",
    "what_changed": "The release gives a third-quarter 2026 revenue outlook of approximately $3.3 billion. The prose states a level, not a direction, so the direction field is 'none'. Comparing the outlook with the quarter just reported is the numbers reader's job.",
    "account": "Revenue",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Revenue of approximately $3.3 billion;",
    "paragraph_id": "0001596532-26-000174:8k_2_02:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_next_quarter_operating_margin_outlook",
    "what_changed": "The release gives a third-quarter 2026 outlook for non-GAAP operating margin as a range. The prose states a level, not a direction. Comparing it with the margin just reported is the numbers reader's job.",
    "account": "Non-GAAP operating margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Non-GAAP operating margin of 48 - 49%",
    "paragraph_id": "0001596532-26-000174:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_next_quarter_eps_outlook",
    "what_changed": "The release gives a third-quarter 2026 outlook range for non-GAAP diluted EPS, on the non-GAAP tax method described in 8k_2_02:53. The prose states a level, not a direction.",
    "account": "Non-GAAP diluted EPS",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Non-GAAP diluted net income per share between $1.06 and $1.08.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:26",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_tax_recast_raises_prior_period_income",
    "what_changed": "A footnote to the non-GAAP reconciliation says prior-period non-GAAP figures were recast for the tax method change. It says the recast increased non-GAAP net income for the three and six months ended June 30, 2025 by the stated amounts. The stated per-share effect is nil for the three months and $0.03 for the six months. The release's year-over-year non-GAAP comparisons therefore use the recast base.",
    "account": "Non-GAAP net income; Non-GAAP diluted EPS",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The retrospective application of this change resulted in an increase to non-GAAP net income of $10.7 million and $30.4 million for the three and six months ended June 30, 2025, respectively.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:40",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_tax_methodology_keeps_indirect_effects",
    "what_changed": "The release describes the non-GAAP tax method change that took effect in the fourth quarter of fiscal 2025. Before, all tax benefits of stock-based awards were excluded, both direct excess benefits and discrete indirect effects. Now only direct excess tax benefits are excluded; the indirect effects stay in non-GAAP results. The description continues at 8k_2_02:55, which says all prior periods were recast. Management says the change better aligns with industry practice. The prior release is not in my input, so I cannot tell whether this description differs from it.",
    "account": "Non-GAAP income tax; Non-GAAP net income",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Effective the fourth quarter of fiscal year 2025, the company updated its methodology for calculating the income tax effect of non-GAAP adjustments.",
    "paragraph_id": "0001596532-26-000174:8k_2_02:53",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### MD&A

- 0001596532-26-000175:mdna:8 — Business-description wording on strategy ('network-as-a-service', 'AI-driven world'). No account, estimate, commitment or risk.
- 0001596532-26-000175:mdna:18 — Heading; period dates rolled forward.
- 0001596532-26-000175:mdna:20 — Table, amounts only.
- 0001596532-26-000175:mdna:22 — Table, amounts only.
- 0001596532-26-000175:mdna:29 — End of the mdna:28 sentence; covered by the mdna:28 item.
- 0001596532-26-000175:mdna:30 — Insufficient: standing list of gross-margin factors carried as changed. Without the prior wording no added or removed factor can be identified, and it ends 'expect our gross margin to fluctuate'.
- 0001596532-26-000175:mdna:34 — Table, amounts only.
- 0001596532-26-000175:mdna:43 — Amounts only; no driver stated ('increased slightly').
- 0001596532-26-000175:mdna:46 — Table, amounts only.
- 0001596532-26-000175:mdna:50 — Table, amounts only.
- 0001596532-26-000175:mdna:51 — Same sentence as notes:85; covered there.
- 0001596532-26-000175:mdna:53 — Amounts only: cash and securities total and the share held outside the U.S.
- 0001596532-26-000175:mdna:57 — Table, amounts only.
- 0001596532-26-000175:mdna:60 — Prior-year comparative rolled to the six months to June 30, 2025; amounts only. Used as a contrast in two mdna:59 items.
- 0001596532-26-000175:mdna:62 — Amounts only (marketable securities purchases and proceeds).
- 0001596532-26-000175:mdna:63 — Prior-year comparative (2025 investing, including VeloCloud).
- 0001596532-26-000175:mdna:66 — Prior-year comparative (2025 financing).
- 0001596532-26-000175:mdna:68 — Standing description of the May 2025 program; terms unchanged.
- 0001596532-26-000175:mdna:69 — Same statements as notes:70; covered there.
- 0001596532-26-000175:mdna:74 — Same commitment figures as notes:60, also without the scope sentence; covered by the notes:60 items.
- 0001596532-26-000175:mdna:76 — Same capex estimate as notes:63; covered there.
- 0001596532-26-000175:mdna:78 — Date rolled forward; still no off-balance-sheet arrangements.

### Notes

- 0001596532-26-000175:notes:4 — Date rolled forward. The history shows only the period wording changed.
- 0001596532-26-000175:notes:9 — Insufficient: pending ASU 2024-03, still under evaluation and disclosure-only. The prior wording is not in my input, so the delta cannot be named.
- 0001596532-26-000175:notes:10 — Insufficient: pending ASU 2025-11 (interim reporting), still under evaluation. I cannot tell whether it is newly added or reworded, and it has no stated effect on amounts.
- 0001596532-26-000175:notes:13 — Table, amounts only.
- 0001596532-26-000175:notes:14 — Date rolled forward; still no transfers between levels.
- 0001596532-26-000175:notes:16 — Table, amounts only.
- 0001596532-26-000175:notes:17 — Date rolled forward; still no credit losses and the same intent-to-hold wording.
- 0001596532-26-000175:notes:19 — Table, amounts only. Its restructuring is covered by the notes:20 item.
- 0001596532-26-000175:notes:21 — Date rolled forward; still no maturities beyond three years.
- 0001596532-26-000175:notes:22 — Table, amounts only.
- 0001596532-26-000175:notes:23 — Amounts only; the duration figure is updated in the same sentence.
- 0001596532-26-000175:notes:27 — Table, amounts only.
- 0001596532-26-000175:notes:28 — Amounts only (evaluation-inventory footnote). It bears on the mdna:11 item.
- 0001596532-26-000175:notes:31 — Table, amounts only.
- 0001596532-26-000175:notes:35 — Table, amounts only.
- 0001596532-26-000175:notes:39 — Table, amounts only.
- 0001596532-26-000175:notes:40 — Amounts only (current portion of contract liabilities).
- 0001596532-26-000175:notes:43 — Table, amounts only.
- 0001596532-26-000175:notes:45 — Amounts only (other performance obligations and their components).
- 0001596532-26-000175:notes:47 — Amounts only (total future revenue and its two-year split). The prior split is not in my input.
- 0001596532-26-000175:notes:50 — Table, amounts only.
- 0001596532-26-000175:notes:53 — Date rolled forward. The VeloCloud allocation is still described as 'preliminary' (wording unchanged), and goodwill did not change in the half.
- 0001596532-26-000175:notes:56 — Table, amounts only.
- 0001596532-26-000175:notes:58 — Table, amounts only.
- 0001596532-26-000175:notes:59 — Heading.
- 0001596532-26-000175:notes:61 — Amounts only. The supplier-deposit figure and as-of date are updated; the history confirms the wording is the same.
- 0001596532-26-000175:notes:62 — Heading.
- 0001596532-26-000175:notes:64 — Heading.
- 0001596532-26-000175:notes:65 — Standing guarantees text; not in the note change history and no change identified.
- 0001596532-26-000175:notes:66 — Heading.
- 0001596532-26-000175:notes:67 — Standing ordinary-course litigation sentence; not in the note change history.
- 0001596532-26-000175:notes:68 — Date rolled forward. The history shows only the as-of date changed.
- 0001596532-26-000175:notes:69 — Heading.
- 0001596532-26-000175:notes:74 — Table, amounts only.
- 0001596532-26-000175:notes:77 — Table, amounts only.
- 0001596532-26-000175:notes:78 — Amounts only (unamortized compensation and weighted period).
- 0001596532-26-000175:notes:80 — Table, amounts only.
- 0001596532-26-000175:notes:82 — Table, amounts only.
- 0001596532-26-000175:notes:84 — Table, amounts only.
- 0001596532-26-000175:notes:89 — Table, amounts only.
- 0001596532-26-000175:notes:90 — Amounts only (U.S. revenue footnote).
- 0001596532-26-000175:notes:92 — Table, amounts only.
- 0001596532-26-000175:notes:94 — Continuation of notes:93; covered there.

### Item 4

- 0001596532-26-000175:item_4_controls:1 — Heading.
- 0001596532-26-000175:item_4_controls:2 — Heading.
- 0001596532-26-000175:item_4_controls:3 — Date rolled forward; disclosure controls still concluded effective.
- 0001596532-26-000175:item_4_controls:4 — Heading.
- 0001596532-26-000175:item_4_controls:5 — Date rolled forward; still no material ICFR changes in the quarter.
- 0001596532-26-000175:item_4_controls:6 — Heading.
- 0001596532-26-000175:item_4_controls:7 — Standing inherent-limitations boilerplate.

### 8-K Item 2.02 (exhibit 99.1)

- 0001596532-26-000174:8k_2_02:1 — Exhibit metadata.
- 0001596532-26-000174:8k_2_02:2 — Exhibit metadata.
- 0001596532-26-000174:8k_2_02:3 — Heading.
- 0001596532-26-000174:8k_2_02:4 — Title.
- 0001596532-26-000174:8k_2_02:6 — Promotional recognition (Fortune 500, Gartner); no account.
- 0001596532-26-000174:8k_2_02:7 — Product announcement; no account, estimate or commitment.
- 0001596532-26-000174:8k_2_02:8 — Dateline and boilerplate company description.
- 0001596532-26-000174:8k_2_02:9 — CEO promotional quote. Its $3 billion milestone is covered by the 8k_2_02:5 item.
- 0001596532-26-000174:8k_2_02:10 — Heading.
- 0001596532-26-000174:8k_2_02:12 — Amounts only (operating margins restated from the tables).
- 0001596532-26-000174:8k_2_02:13 — Amounts only (EPS restated from the tables).
- 0001596532-26-000174:8k_2_02:14 — Boilerplate pointer to the reconciliation.
- 0001596532-26-000174:8k_2_02:16 — Heading.
- 0001596532-26-000174:8k_2_02:17 — Webinar promotion.
- 0001596532-26-000174:8k_2_02:18 — Promotional recognition (Gartner).
- 0001596532-26-000174:8k_2_02:19 — Product announcement.
- 0001596532-26-000174:8k_2_02:20 — Technology description.
- 0001596532-26-000174:8k_2_02:21 — Technology description (continuation).
- 0001596532-26-000174:8k_2_02:22 — Heading.
- 0001596532-26-000174:8k_2_02:23 — Lead-in to the outlook bullets.
- 0001596532-26-000174:8k_2_02:27 — Standard boilerplate on guidance exclusions and reconciliation.
- 0001596532-26-000174:8k_2_02:28 — Heading.
- 0001596532-26-000174:8k_2_02:29 — Call logistics.
- 0001596532-26-000174:8k_2_02:30 — Webcast logistics.
- 0001596532-26-000174:8k_2_02:31 — Heading.
- 0001596532-26-000174:8k_2_02:32 — Heading.
- 0001596532-26-000174:8k_2_02:33 — Heading.
- 0001596532-26-000174:8k_2_02:34 — Table, amounts only.
- 0001596532-26-000174:8k_2_02:35 — Page number.
- 0001596532-26-000174:8k_2_02:36 — Heading.
- 0001596532-26-000174:8k_2_02:37 — Heading.
- 0001596532-26-000174:8k_2_02:38 — Heading.
- 0001596532-26-000174:8k_2_02:39 — Table, amounts only.
- 0001596532-26-000174:8k_2_02:41 — Heading.
- 0001596532-26-000174:8k_2_02:42 — Heading.
- 0001596532-26-000174:8k_2_02:43 — Heading.
- 0001596532-26-000174:8k_2_02:44 — Table, amounts only.
- 0001596532-26-000174:8k_2_02:45 — Page number.
- 0001596532-26-000174:8k_2_02:46 — Heading.
- 0001596532-26-000174:8k_2_02:47 — Heading.
- 0001596532-26-000174:8k_2_02:48 — Heading.
- 0001596532-26-000174:8k_2_02:49 — Table, amounts only.
- 0001596532-26-000174:8k_2_02:50 — Heading.
- 0001596532-26-000174:8k_2_02:51 — Insufficient: standard forward-looking safe-harbor list. The prior release is not in my input, so no addition or removal can be named. It is cited as context in one across_documents item.
- 0001596532-26-000174:8k_2_02:52 — Heading.
- 0001596532-26-000174:8k_2_02:54 — Page number.
- 0001596532-26-000174:8k_2_02:55 — Continuation of 8k_2_02:53; covered there.
- 0001596532-26-000174:8k_2_02:56 — Non-GAAP usefulness boilerplate.
- 0001596532-26-000174:8k_2_02:57 — Non-GAAP limitations boilerplate.
- 0001596532-26-000174:8k_2_02:58 — Heading.
- 0001596532-26-000174:8k_2_02:59 — Company description boilerplate.
- 0001596532-26-000174:8k_2_02:60 — Trademark boilerplate.
- 0001596532-26-000174:8k_2_02:61 — Investor contacts.

## Counts

- Items: 40.
- Items with `explanation` true: 5 (mdna:11, mdna:15, mdna:54, mdna:59 receivables, notes:32).
- Insufficient: 4 (mdna:30, notes:9, notes:10, 8k_2_02:51).
- Not in input: auditor's report, Item 1A diff, Exhibit 21 diff, Exhibit 10, and the body of the 2026-06-02 Item 5.07 8-K.
