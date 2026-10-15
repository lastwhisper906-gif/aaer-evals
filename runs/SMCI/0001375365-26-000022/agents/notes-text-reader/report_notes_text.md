# SMCI — notes-text reader report — 10-K 0001375365-26-000022 (FY ended 2026-06-30)

## Input check

Directory holds input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md. There is no trend table, price series, abnormal return, short interest, other company's file, prior run probability or outcome window. Some filing text mentions stock-price movement (mdna:112, notes:494, notes:496 ECD disclosure). That is the company's own prose, and nothing here relies on it as market data. Prior predictions: none on record.

Basis of comparison: the prior 10-K text is not in the directory. The note history covers 10-Q 0001375365-26-000007 → 0001375365-26-000014 (Q2 → Q3 FY2026). An item counts as "new" here if one of three things is true: the note history shows the change; the prose dates the event in FY2026 or later; or the paragraph has no counterpart in the Q3 text. No arithmetic was done anywhere. Directions come from the prose. Where the prose gives no direction word, the direction is `none` and the comparison is left to the numbers reader.

## Items

```json
[
{"id":"controls_audit_and_filings_itgc_material_weakness_remains","what_changed":"ICFR is again not effective, but the stated material weakness is now one ITGC weakness: IT controls did not operate long enough, and user-access monitoring was inconsistent.","account":"none","expected_direction":"none","horizon":"12 months","quote":"did not operate for a sufficient period of time","paragraph_id":"0001375365-26-000022:item_9a:11","explanation":false},
{"id":"controls_audit_and_filings_three_material_weaknesses_remediated","what_changed":"Management now says three FY2025 material weaknesses are remediated: segregation of duties, completeness and accuracy of information produced, and timely recording and disclosure. Actions included an ERP role redesign, new accounting leadership and added close-process reviews.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"we remediated three material weaknesses in internal control over financial reporting","paragraph_id":"0001375365-26-000022:item_9a:21","explanation":false},
{"id":"controls_audit_and_filings_auditor_adverse_icfr_opinion","what_changed":"BDO issues an adverse ICFR opinion as of June 30, 2026, citing the ITGC weakness. The financial statements get an unqualified opinion.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"the Company did not maintain, in all material respects, effective internal control over financial reporting as of June 30, 2026","paragraph_id":"0001375365-26-000022:item_9a:44","explanation":false},
{"id":"controls_audit_and_filings_disclosure_controls_not_effective","what_changed":"Disclosure controls are concluded not effective as of June 30, 2026 because of the material weakness first reported in the FY2025 10-K.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"concluded that our disclosure controls and procedures were not effective at the reasonable assurance level as of June 30, 2026","paragraph_id":"0001375365-26-000022:item_9a:4","explanation":false},
{"id":"controls_audit_and_filings_itgc_remediation_expected_next_fiscal_year","what_changed":"New remediation timetable: management expects the ITGC weakness to be remediated, subject to operating-effectiveness testing during fiscal 2027.","account":"none","expected_direction":"none","horizon":"12 months","quote":"will likely allow us to remediate this material weakness, subject to the completion of operating effectiveness testing during fiscal year 2027","paragraph_id":"0001375365-26-000022:item_9a:32","explanation":false},
{"id":"controls_audit_and_filings_inventory_valuation_critical_audit_matter","what_changed":"The auditor reports inventory valuation as a critical audit matter on a stated $12.9 billion balance. The matter centres on excess and obsolescence write-down percentages by aging category.","account":"inventories","expected_direction":"none","horizon":"this quarter","quote":"write-down percentages for excess and obsolescence applied to the different inventory aging categories","paragraph_id":"0001375365-26-000022:auditors_report:16","explanation":false},
{"id":"controls_audit_and_filings_revenue_critical_audit_matter_credit_memo_cutoff","what_changed":"The revenue critical audit matter, on stated net sales of $39.1 billion, includes period-cutoff testing of credit memos and confirmation of contract terms with customers.","account":"net sales","expected_direction":"none","horizon":"this quarter","quote":"Inspecting a sample of credit memos and the related invoice to assess whether they were recorded in the appropriate period","paragraph_id":"0001375365-26-000022:auditors_report:28","explanation":false},
{"id":"revenue_recognition_extended_payment_terms_financing_component","what_changed":"The policy says extended payment terms are granted to certain customers and that the transaction price is adjusted for a significant financing component. Contract balances say longer terms are offered occasionally. Non-current receivables bear interest at amortized cost.","account":"accounts receivable","expected_direction":"none","horizon":"12 months","quote":"we also grant extended payment terms for certain customers","paragraph_id":"0001375365-26-000022:notes:45","explanation":false},
{"id":"earnings_quality_interest_income_from_customer_financing_arrangements","what_changed":"MD&A attributes the interest-income increase partly to financing arrangements with a customer. The arrangement is not described anywhere else in the input.","account":"interest income","expected_direction":"up","horizon":"this quarter","quote":"financing arrangements with a customer","paragraph_id":"0001375365-26-000022:mdna:100","explanation":false},
{"id":"revenue_recognition_receivable_recorded_before_transfer_of_control","what_changed":"The policy records a receivable together with deferred revenue once billing gives an unconditional right to consideration before transfer of control. This puts receivables and deferred revenue on the balance sheet together.","account":"accounts receivable; deferred revenue","expected_direction":"none","horizon":"this quarter","quote":"We also recognize deferred revenue when we have an unconditional right to consideration (i.e., a receivable) before transfer of control of goods or services to a customer","paragraph_id":"0001375365-26-000022:notes:46","explanation":false},
{"id":"revenue_recognition_non_refundable_customer_advances_deferred_revenue","what_changed":"The prose says deferred revenue increased, partly from a $943.4 million increase in non-refundable customer advances for products expected to ship within 12 months.","account":"deferred revenue; net sales","expected_direction":"up","horizon":"12 months","quote":"a $943.4 million increase in non-refundable advance consideration or cash consideration received from customers","paragraph_id":"0001375365-26-000022:notes:125","explanation":false},
{"id":"revenue_recognition_remaining_performance_obligations_excludes_untransferred_products","what_changed":"Remaining performance obligations are stated at $2,612.0 million, about 60% due within 12 months. The exemption excludes products whose control has not transferred, so product backlog sits outside this figure.","account":"net sales","expected_direction":"none","horizon":"12 months","quote":"and for products where control has not yet been transferred","paragraph_id":"0001375365-26-000022:notes:127","explanation":false},
{"id":"across_documents_record_backlog_claim_versus_disclosed_obligations","what_changed":"The earnings release claims more than $60 billion in new orders and record backlog. The 10-K quantifies backlog only through the RPO disclosure, which excludes untransferred products.","account":"net sales","expected_direction":"up","horizon":"next quarter","quote":"booked record backlog entering fiscal 2027","paragraph_id":"0001375365-26-000021:8k_2_02:14","explanation":false},
{"id":"results_against_expectations_first_quarter_and_fiscal_year_outlook","what_changed":"New guidance: Q1 FY2027 net sales of $14.5–15.5 billion and FY2027 net sales of $65.0–72.0 billion. Comparing these with reported results is left to the numbers reader.","account":"net sales","expected_direction":"none","horizon":"next quarter","quote":"The Company expects net sales in the range of $14.5 billion and $15.5 billion for the first quarter of fiscal year 2027","paragraph_id":"0001375365-26-000021:8k_2_02:21","explanation":false},
{"id":"results_against_expectations_fourth_quarter_gross_margin_step_up","what_changed":"The release states Q4 gross margin of 17.5%, against 9.9% in Q3, and the CEO says profitability is improving through enterprise mix and DCBBS adoption. The 10-K MD&A has no Q4-specific explanation.","account":"gross margin","expected_direction":"up","horizon":"next quarter","quote":"we are improving profitability through a richer enterprise customer mix","paragraph_id":"0001375365-26-000021:8k_2_02:14","explanation":false},
{"id":"narrative_signs_of_operating_pressure_competitive_pricing_full_year_margin","what_changed":"MD&A says full-year gross margin decreased, attributing it to pricing aimed at gaining share, product and customer mix, and higher manufacturing expenses.","account":"gross margin","expected_direction":"down","horizon":"this quarter","quote":"primarily due to our strategy to offer competitive pricing to gain market share","paragraph_id":"0001375365-26-000022:mdna:77","explanation":false},
{"id":"across_documents_customer_diversification_claim_versus_single_customer_share","what_changed":"MD&A credits growth partly to customer diversification and large design wins from a few customers. The notes state that one customer was 28.1% of FY2026 net sales. Reconciling the two is left to the supervisor.","account":"net sales","expected_direction":"none","horizon":"this quarter","quote":"driven by our product mix, customer diversification, growth in enterprise and channel revenues","paragraph_id":"0001375365-26-000022:mdna:15","explanation":false},
{"id":"revenue_recognition_single_customer_share_of_net_sales","what_changed":"New-period concentration: one customer represented 28.1% of FY2026 net sales. FY2025 had four customers above 10%.","account":"net sales","expected_direction":"none","horizon":"this quarter","quote":"sales to one customer represented 28.1% of total net sales","paragraph_id":"0001375365-26-000022:notes:120","explanation":false},
{"id":"revenue_recognition_receivables_three_customer_concentration","what_changed":"Year-end receivables concentration: three customers hold 23.0%, 17.1% and 12.5% of accounts receivable. Q3 named four customers, with A at 32.2%.","account":"accounts receivable","expected_direction":"none","horizon":"this quarter","quote":"three customers accounted for 23.0%, 17.1%, and 12.5% of our accounts receivable balance","paragraph_id":"0001375365-26-000022:notes:89","explanation":false},
{"id":"revenue_recognition_growth_from_rack_scale_gpu_systems","what_changed":"MD&A attributes the sales increase mainly to Hyper Servers, GPU and Super Racks, mostly GB200 and GB300 systems. Services and software are stated at $538.3 million.","account":"net sales","expected_direction":"up","horizon":"this quarter","quote":"primarily related to our GB200, and GB300 systems","paragraph_id":"0001375365-26-000022:mdna:69","explanation":false},
{"id":"revenue_recognition_customer_equity_investee_and_sublicensee","what_changed":"The company has $92.5 million invested in the Vernon data-center sublicensee, which is also a customer. Management concludes the investment, the sublicense and the revenue contracts are separate and at fair value. Sublease income is reported in other income.","account":"net sales; other income; long-term investments","expected_direction":"none","horizon":"12 months","quote":"the Sub-licensee has been a customer of ours, and we concluded that equity investment agreements and sub-licensing agreements are separate from revenue contracts","paragraph_id":"0001375365-26-000022:notes:148","explanation":false},
{"id":"across_documents_other_income_explanation_omits_sublease_income","what_changed":"The notes put Vernon sublease rental income in other income (expense), net. MD&A explains the other-income change with mark-to-market gains, FX and the absent extinguishment loss, and does not mention sublease income.","account":"other income (expense), net","expected_direction":"up","horizon":"this quarter","quote":"the rental income is included in other income (expense), net on the consolidated statements of operations","paragraph_id":"0001375365-26-000022:notes:309","explanation":false},
{"id":"earnings_quality_vendor_rebates_decline_raises_cost_of_sales","what_changed":"MD&A says lower vendor rebates increased cost of sales.","account":"cost of sales","expected_direction":"up","horizon":"this quarter","quote":"a $312.9 million or 24.9% increase due to a decrease in vendor rebates","paragraph_id":"0001375365-26-000022:mdna:76","explanation":false},
{"id":"estimates_and_discretion_inventory_write_down_decrease_from_aged_inventory_sales","what_changed":"Management explains lower inventory write-downs by increased sales of aged inventory products.","account":"inventory reserves; cost of sales","expected_direction":"down","horizon":"this quarter","quote":"a $43.8 million or 18.8% decrease in inventory write-down adjustments resulting from increased sales related to some of our aged inventory products","paragraph_id":"0001375365-26-000022:mdna:76","explanation":true},
{"id":"narrative_signs_of_operating_pressure_tariff_expense_increase","what_changed":"MD&A says tariff expense increased under new trade policies.","account":"cost of sales","expected_direction":"up","horizon":"this quarter","quote":"a $237.7 million or 228.3% increase in tariff expenses driven by new trade policies enacted during the year","paragraph_id":"0001375365-26-000022:mdna:76","explanation":false},
{"id":"estimates_and_discretion_section_two_three_two_tariff_receivable_recognized","what_changed":"New other-asset line for a tariff receivable from Section 232 claims. No recognition criteria or timing are given.","account":"other assets","expected_direction":"none","horizon":"12 months","quote":"Represents receivables related to our claims under Section 232 of the Trade Expansion Act of 1962","paragraph_id":"0001375365-26-000022:notes:171","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_ieepa_tariff_refund_not_recognized","what_changed":"A possible IEEPA tariff refund after the February 2026 Supreme Court ruling is still unrecognized at year end. The date is rolled from Q3.","account":"cost of sales; other assets","expected_direction":"none","horizon":"12 months","quote":"As of June 30, 2026, we have not recognized an asset related to the potential refund","paragraph_id":"0001375365-26-000022:notes:468","explanation":false},
{"id":"estimates_and_discretion_inventory_ordered_ahead_of_lead_times_with_deposits","what_changed":"The inventory estimate text says lead times have exceeded twelve months and that the company places non-cancellable orders ahead of historical lead times, paying premiums and deposits. Prepaid inventory appears as a new line.","account":"inventories; prepaid inventory","expected_direction":"up","horizon":"12 months","quote":"We may place non-cancellable inventory orders for certain product components in advance of our historical lead times, pay premiums and provide deposits to secure future supply and capacity","paragraph_id":"0001375365-26-000022:mdna:33","explanation":false},
{"id":"structure_and_disclosure_changes_asset_held_for_others_unexplained","what_changed":"Prepaid expenses and other current assets has a new line, Asset held for others, with no balance last year. No prose explains it.","account":"prepaid expenses and other current assets","expected_direction":"none","horizon":"this quarter","quote":"Asset held for others","paragraph_id":"0001375365-26-000022:notes:164","explanation":false},
{"id":"structure_and_disclosure_changes_finished_goods_include_gpus","what_changed":"The notes define finished goods as including GPUs and racks. MD&A describes finished goods as finished products and products ready for sale.","account":"inventories","expected_direction":"none","horizon":"this quarter","quote":"finished goods (including GPUs and racks)","paragraph_id":"0001375365-26-000022:notes:30","explanation":false},
{"id":"liquidity_and_capital_working_capital_build_inventory_receivables","what_changed":"Management explains higher inventory and accounts receivable as needed to support future revenue growth.","account":"inventories; accounts receivable","expected_direction":"up","horizon":"this quarter","quote":"an increase in the need for working capital due to higher levels of inventory and accounts receivable required to support future revenue growth","paragraph_id":"0001375365-26-000022:mdna:129","explanation":true},
{"id":"liquidity_and_capital_operating_cash_outflow_inventory_purchases","what_changed":"Operating cash flow is described as decreased, driven by inventory purchases, receivables and operating spending.","account":"cash flow from operations","expected_direction":"down","horizon":"this quarter","quote":"was due to an increase in inventory purchases, accounts receivable from customers, and increased operational spending","paragraph_id":"0001375365-26-000022:mdna:138","explanation":false},
{"id":"liquidity_and_capital_fourth_quarter_operating_cash_inflow","what_changed":"The release states Q4 operating cash was provided, at $747 million. The 10-K gives only the full year, which it describes as cash used.","account":"cash flow from operations","expected_direction":"none","horizon":"next quarter","quote":"of $747 million and capital expenditures and investments of $25 million","paragraph_id":"0001375365-26-000021:8k_2_02:13","explanation":false},
{"id":"liquidity_and_capital_purchase_commitments_scale","what_changed":"Non-cancelable purchase commitments are now stated at $34.2 billion, including $0.2 billion with related parties, mostly due within 12 months. MD&A calls them current obligations.","account":"inventories; purchase commitments","expected_direction":"up","horizon":"12 months","quote":"these remaining non-cancelable commitments were $34.2 billion, including $0.2 billion for related parties","paragraph_id":"0001375365-26-000022:notes:469","explanation":false},
{"id":"estimates_and_discretion_purchase_commitment_loss_liability_amount_dropped","what_changed":"Q3 said $4.1 million of loss liabilities on purchase commitments had been recorded. The 10-K keeps only the review-policy sentence and states no year-end amount.","account":"accrued liabilities","expected_direction":"none","horizon":"this quarter","quote":"We also review and assess the need for expected loss liabilities on a quarterly basis for all products we do not expect to sell but have committed to purchase from suppliers","paragraph_id":"0001375365-26-000022:notes:469","explanation":false},
{"id":"liquidity_and_capital_receivables_sold_under_purchase_agreement","what_changed":"The receivables purchase program was used for the first time: $831.7 million sold and a $5.7 million discount charged to G&A. Nothing sold was outstanding at year end. Q2 had said nothing had been sold.","account":"accounts receivable; general and administrative","expected_direction":"none","horizon":"next quarter","quote":"the full $1,790.0 million facility limit remained unutilized as of June 30, 2026","paragraph_id":"0001375365-26-000022:notes:184","explanation":false},
{"id":"earnings_quality_legal_and_investigation_costs_in_general_and_administrative","what_changed":"G&A increase is attributed mainly to legal and internal-investigation expenses, plus factoring fees and excise tax. It is partly offset by lower audit fees now that the delayed-filing costs are gone.","account":"general and administrative","expected_direction":"up","horizon":"12 months","quote":"an increase in legal and internal investigation-related expenses of $31.7 million or 98.4%","paragraph_id":"0001375365-26-000022:mdna:89","explanation":false},
{"id":"earnings_quality_marketing_development_funds_reduce_sales_and_marketing","what_changed":"Higher supplier marketing development funds are said to have reduced sales and marketing expense.","account":"sales and marketing","expected_direction":"down","horizon":"this quarter","quote":"$29.8 million or 81.6% higher marketing development funds received from certain business partners","paragraph_id":"0001375365-26-000022:mdna:87","explanation":false},
{"id":"across_documents_advertising_expense_description_differs","what_changed":"The notes report advertising expense, net of vendor reimbursements, of $2.0 million, $38.1 million and $10.7 million. MD&A describes a $3.3 million (4.1%) decrease in standard marketing and advertising. Reconciliation is left to the numbers reader.","account":"sales and marketing","expected_direction":"none","horizon":"this quarter","quote":"We incurred advertising expenses of $2.0 million, $38.1 million and $10.7 million","paragraph_id":"0001375365-26-000022:notes:60","explanation":false},
{"id":"narrative_signs_of_operating_pressure_operating_expense_growth_expected","what_changed":"Management expects R&D, S&M and G&A to keep rising with headcount and investment in talent.","account":"operating expenses","expected_direction":"up","horizon":"12 months","quote":"We believe that research and development expenses will continue to increase","paragraph_id":"0001375365-26-000022:mdna:86","explanation":false},
{"id":"narrative_signs_of_operating_pressure_component_supply_constraints","what_changed":"New FY2026 statement that memory, storage, GPU and CPU supply constraints affected delivery timing and pricing.","account":"net sales; cost of sales","expected_direction":"none","horizon":"next quarter","quote":"the computer server industry experienced supply constraints for certain components, including memory and storage, as well as GPU and CPU availability","paragraph_id":"0001375365-26-000022:mdna:11","explanation":false},
{"id":"earnings_quality_effective_tax_rate_rise_on_stock_price","what_changed":"The effective tax rate is said to have increased because a lower stock price reduced stock-compensation deductions and research credits.","account":"income tax provision","expected_direction":"up","horizon":"this quarter","quote":"both driven by the decrease in our stock price","paragraph_id":"0001375365-26-000022:mdna:112","explanation":false},
{"id":"estimates_and_discretion_malaysia_tax_incentive_assumed_before_approval","what_changed":"New: the effective tax rate assumes a Malaysian tax exemption that is not yet approved and depends on an investment threshold by December 16, 2026. If it is not granted, the rate and cash taxes would rise. Notes add that a fully reserved Malaysian NOL deferred tax asset was written off.","account":"income tax provision","expected_direction":"none","horizon":"next quarter","quote":"for which we have applied but have not yet received final approval","paragraph_id":"0001375365-26-000022:mdna:115","explanation":false},
{"id":"estimates_and_discretion_obbba_effects_recognized_unquantified","what_changed":"New: the tax effects of certain provisions of OBBBA (enacted July 4, 2025) are recognized but not quantified.","account":"income tax provision; deferred income taxes","expected_direction":"none","horizon":"12 months","quote":"we have recognized the tax effects of certain OBBBA provisions","paragraph_id":"0001375365-26-000022:mdna:113","explanation":false},
{"id":"estimates_and_discretion_california_credit_limitation_extended","what_changed":"New: California SB 122 (June 29, 2026) extends limits on using business credits. The company concludes there is no material impact on California deferred tax assets.","account":"deferred income taxes","expected_direction":"none","horizon":"12 months","quote":"concluded that the enactment did not have a material impact","paragraph_id":"0001375365-26-000022:mdna:114","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_tax_examinations_united_states_and_india","what_changed":"The notes now state open examinations: the US for FY2024, and India for tax years ended 2024 and 2025.","account":"income taxes payable; unrecognized tax benefits","expected_direction":"none","horizon":"12 months","quote":"we are under examination in certain tax jurisdictions, including the United States for the fiscal year ended June 30, 2024, and India","paragraph_id":"0001375365-26-000022:notes:450","explanation":false},
{"id":"earnings_quality_investment_impairment_then_sale_gain","what_changed":"Within FY2026 an investment was impaired by $12.0 million and then sold later in the year for a $13.3 million gain.","account":"other income (expense), net","expected_direction":"none","horizon":"this quarter","quote":"we recognized an impairment loss of $12.0 million related to an investment, and subsequently realized a gain of $13.3 million upon sale of such investment","paragraph_id":"0001375365-26-000022:notes:149","explanation":false},
{"id":"structure_and_disclosure_changes_unspecified_reclassifications_net","what_changed":"The reclassification note now says no net changes; Q2 said no changes. This implies line items moved while totals held. The reclassified items are not identified.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"Such reclassifications did not result in net changes to consolidated balance sheets","paragraph_id":"0001375365-26-000022:notes:103","explanation":false},
{"id":"structure_and_disclosure_changes_malaysia_operations_and_repatriation","what_changed":"Malaysia is now named among the principal operations (the subsidiary started operating in July 2025). Malaysian earnings are excluded from indefinite reinvestment.","account":"deferred income taxes","expected_direction":"none","horizon":"12 months","quote":"we plan to indefinitely reinvest such earnings except for the Netherlands and Malaysia","paragraph_id":"0001375365-26-000022:notes:70","explanation":false},
{"id":"structure_and_disclosure_changes_two_class_earnings_per_share","what_changed":"New two-class EPS method: the 7% Series A Mandatory Convertible Preferred is a participating security. Preferred dividends and earnings allocated to participating securities are deducted from common earnings.","account":"net income per share","expected_direction":"down","horizon":"next quarter","quote":"is considered a participating security","paragraph_id":"0001375365-26-000022:notes:77","explanation":false},
{"id":"liquidity_and_capital_mandatory_convertible_preferred_issued","what_changed":"New Mandatory Convertible Preferred Stock: $3.75 billion liquidation preference plus the overallotment, mandatory conversion around June 1, 2029, and 4,312,500 preferred shares outstanding.","account":"stockholders' equity","expected_direction":"up","horizon":"this quarter","quote":"The offering represented an aggregate liquidation preference of $3.75 billion","paragraph_id":"0001375365-26-000022:notes:410","explanation":false},
{"id":"liquidity_and_capital_preferred_dividends_accrued_payable_in_shares","what_changed":"New 7% cumulative preferred dividend from September 1, 2026, payable in cash or common shares. It accrues whether or not declared.","account":"accrued liabilities; preferred dividends","expected_direction":"up","horizon":"next quarter","quote":"we accrue dividends whether or not they are declared by our board of directors","paragraph_id":"0001375365-26-000022:notes:413","explanation":false},
{"id":"liquidity_and_capital_common_stock_offering","what_changed":"New June 2026 common stock offering of 45,454,545 shares at $27.50 plus the 6,818,181-share option, about $1.22 billion and $183.4 million net.","account":"stockholders' equity; share count","expected_direction":"up","horizon":"next quarter","quote":"we completed an underwritten public offering of 45,454,545 shares of our common stock at a public offering price of $27.50 per share","paragraph_id":"0001375365-26-000022:notes:402","explanation":false},
{"id":"liquidity_and_capital_at_the_market_program","what_changed":"New $1.25 billion at-the-market common stock program, with sales no earlier than July 2026. Nothing was sold by June 30.","account":"stockholders' equity; share count","expected_direction":"up","horizon":"next quarter","quote":"Sales under the program, if any, are expected to commence no earlier than the third calendar quarter of 2026","paragraph_id":"0001375365-26-000022:notes:428","explanation":false},
{"id":"liquidity_and_capital_jp_morgan_revolver_secured_by_first_priority_lien","what_changed":"Newly described terms of the JP Morgan revolver: a first-priority lien on substantially all assets outside investment-grade periods, a net leverage covenant stepping from 4.00x to 3.00x, and maturity on December 29, 2030.","account":"lines of credit and term loans","expected_direction":"none","horizon":"12 months","quote":"is secured by a first-priority lien on substantially all assets of the applicable loan parties","paragraph_id":"0001375365-26-000022:notes:197","explanation":false},
{"id":"liquidity_and_capital_jp_morgan_collateral_value_disclosed","what_changed":"New sentence: US collateral value under the JP Morgan agreement is estimated at $22.4 billion after excluding ineligible assets.","account":"lines of credit and term loans","expected_direction":"none","horizon":"this quarter","quote":"the estimated collateral value of assets held in the United States was approximately $22.4 billion","paragraph_id":"0001375365-26-000022:notes:195","explanation":false},
{"id":"liquidity_and_capital_credit_agreement_amended_for_preferred_distributions","what_changed":"New June 2026 amendment to the JP Morgan agreement permits distributions on the preferred stock, subject to a pro forma fixed charge coverage test.","account":"lines of credit and term loans; preferred dividends","expected_direction":"none","horizon":"next quarter","quote":"subject to maintaining a pro forma fixed charge coverage ratio of at least 2.00:1.00","paragraph_id":"0001375365-26-000022:notes:198","explanation":false},
{"id":"liquidity_and_capital_ctbc_revolver_repayment_extended","what_changed":"Subsequent event: the CTBC revolver utilization was due July 23, 2026 and its repayment date was extended to January 22, 2027.","account":"lines of credit and term loans, current","expected_direction":"none","horizon":"next quarter","quote":"On July 23, 2026, the repayment date was extended to January 22, 2027","paragraph_id":"0001375365-26-000022:notes:205","explanation":false},
{"id":"liquidity_and_capital_ctbc_subsidiary_receivables_pledged","what_changed":"New disclosure: the parent guarantees the CTBC revolver, and all Taiwan-subsidiary receivables and some term deposits are pledged under a continuing security interest.","account":"accounts receivable; restricted cash","expected_direction":"none","horizon":"12 months","quote":"all receivables of the subsidiary and the related proceeds are subject to a continuing security interest","paragraph_id":"0001375365-26-000022:notes:204","explanation":false},
{"id":"liquidity_and_capital_restricted_cash_controlled_by_lenders","what_changed":"The restricted cash policy now says the balance is mostly cash in lender-controlled accounts under debt agreements. New current restricted-cash line in prepaid expenses.","account":"restricted cash","expected_direction":"none","horizon":"this quarter","quote":"amounts held in bank accounts which are controlled by the lenders pursuant to the terms of certain debt agreements","paragraph_id":"0001375365-26-000022:notes:28","explanation":false},
{"id":"liquidity_and_capital_esun_covenant_verification_waived","what_changed":"New June 26, 2026 amendment changed E.SUN covenants and granted a one-time waiver of the debt-to-net-worth and interest-coverage tests for the period ending October 31, 2026.","account":"lines of credit and term loans","expected_direction":"none","horizon":"next quarter","quote":"A one-time waiver was granted by E.SUN Bank for the verification of the debt-to-net worth and interest coverage ratios for the period ending October 31, 2026","paragraph_id":"0001375365-26-000022:notes:245","explanation":false},
{"id":"liquidity_and_capital_taiwan_bilateral_lines_capped_with_syndicate_participation","what_changed":"New: the E.SUN line, renewed June 3, 2026 to May 12, 2027, and the Mega Bank line now share caps with each bank's participation in the CTBC syndicated revolver: $200.0 million with $150.0 million participation, and $70.0 million with $30.0 million participation.","account":"lines of credit and term loans","expected_direction":"none","horizon":"12 months","quote":"which is included in the outstanding balance under the CTBC Revolving Credit Facilities presented above, may not exceed $200.0 million","paragraph_id":"0001375365-26-000022:notes:237","explanation":false},
{"id":"liquidity_and_capital_ctbc_omnibus_credit_lines_renewed","what_changed":"New 2026 CTBC facility letter dated April 21, 2026. The listed sub-lines no longer include the USD short-term loan line, and the $185.0 million cap is unchanged.","account":"lines of credit and term loans","expected_direction":"none","horizon":"12 months","quote":"On April 21, 2026, our Taiwan Subsidiary received a new facility letter from CTBC Bank","paragraph_id":"0001375365-26-000022:notes:215","explanation":false},
{"id":"liquidity_and_capital_revolver_drawdowns_raise_interest_expense","what_changed":"Interest expense increased partly because of $83.0 million in interest on revolver drawdowns in the second half of FY2026.","account":"interest expense","expected_direction":"up","horizon":"next quarter","quote":"$83.0 million additional interest expense related to the drawdown on our revolving credit facilities during the second half of fiscal 2026","paragraph_id":"0001375365-26-000022:mdna:101","explanation":false},
{"id":"liquidity_and_capital_bank_debt_and_convertibles_stated_in_release","what_changed":"The release states year-end bank debt and convertible notes of $8.7 billion alongside cash of $7.5 billion.","account":"lines of credit and term loans; convertible notes","expected_direction":"none","horizon":"this quarter","quote":"total bank debt and convertible notes were $8.7 billion","paragraph_id":"0001375365-26-000021:8k_2_02:19","explanation":false},
{"id":"liquidity_and_capital_capital_expenditure_guidance","what_changed":"New FY2027 capex guidance of $380.0–400.0 million for manufacturing, tooling, IT and facilities.","account":"property, plant and equipment","expected_direction":"none","horizon":"12 months","quote":"We anticipate our total capital expenditures for the fiscal year 2027 will be in the range of $380.0 million to $400.0 million","paragraph_id":"0001375365-26-000022:mdna:151","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_ablecom_reseller_to_japan_customer","what_changed":"New: related party Ablecom, the contract manufacturer, resells company products to an end customer in Japan. Terms are said to be consistent with third-party resellers.","account":"net sales","expected_direction":"none","horizon":"next quarter","quote":"we entered into an arrangement for Ablecom to resell certain products, to an end customer in Japan","paragraph_id":"0001375365-26-000022:notes:323","explanation":false},
{"id":"articulation_and_the_filed_history_ablecom_reseller_quarter_restated","what_changed":"The same Ablecom resale arrangement is dated to the third quarter (ended March 31, 2026) in the Q3 10-Q but to the fourth quarter in the 10-K.","account":"net sales","expected_direction":"none","horizon":"this quarter","quote":"During the fourth quarter of the fiscal year ended June 30, 2026","paragraph_id":"0001375365-26-000022:notes:323","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_ablecom_land_use_agreement","what_changed":"New 50-year land-use agreement under which the company leases three Taoyuan parcels to Ablecom. Rental income is not material.","account":"other income","expected_direction":"none","horizon":"12 months","quote":"we entered into a 50-year superficies (land-use right) agreement with Ablecom covering three parcels of land in Taoyuan, Taiwan","paragraph_id":"0001375365-26-000022:notes:324","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_compuware_trade_credit_line","what_changed":"New $200.0 million trade credit line on net 90 terms to related-party distributor Compuware, dated November 19, 2025. Ablecom's line is $10.0 million on net 30.","account":"accounts receivable, related party","expected_direction":"none","horizon":"12 months","quote":"We extended a $200.0 million trade credit line on November 19, 2025, with a net 90 days payment term to Compuware","paragraph_id":"0001375365-26-000022:notes:330","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_compuware_finder_fee_rate","what_changed":"The Compuware finder's fee is stated at about $1.8 million, a weighted 0.16% rate, on sales from a customer Compuware referred. FY2025 is stated as 1%.","account":"sales and marketing","expected_direction":"none","horizon":"this quarter","quote":"a weighted average fee rate of approximately 0.16% of the net sales from a customer referred to us by Compuware","paragraph_id":"0001375365-26-000022:notes:334","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_leadtek_board_family_member_added","what_changed":"Steve Liang's wife now sits on the Leadtek board, so three of seven directors are Liang family members. Q3 said two.","account":"net sales, related party","expected_direction":"none","horizon":"this quarter","quote":"Steve Liang, Chang-Jian-Tsun (wife of Steve Liang), and Bill Liang served as three of the seven members of the Leadtek board of directors","paragraph_id":"0001375365-26-000022:notes:336","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_liaw_sibling_ownership_no_longer_disclosed","what_changed":"Q2 disclosed that a sibling of director and SVP Wally Liaw owned about 11.7% of Ablecom and 8.7% of Compuware. Q3 and the 10-K drop both sentences and the no-ownership sentence without explanation.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"a sibling of Yih-Shyan (Wally) Liaw, who is our Senior Vice President, Business Development and a board director","paragraph_id":"0001375365-26-000007:note_history:61","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_ceo_personal_loan_repaid","what_changed":"The CEO's personal loan from Steve Liang's spouse was repaid in full on October 9, 2025.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"On October 9, 2025, the outstanding loan principal and accrued interest through October 8, 2025, totaling $16.9 million was repaid in full","paragraph_id":"0001375365-26-000022:notes:320","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_corporate_venture_divested","what_changed":"The 30% China Corporate Venture was divested on December 23, 2025 and is no longer a related party. Related-party disclosure covers only the first half.","account":"share of loss from equity investees; net sales, related party","expected_direction":"none","horizon":"this quarter","quote":"the divestiture of our 30% interest was completed on December 23, 2025","paragraph_id":"0001375365-26-000022:notes:340","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_director_trading_plan_adopted","what_changed":"Co-founder and director Sara Liu adopted a Rule 10b5-1 plan on May 26, 2026 to sell up to 300,000 shares by February 28, 2027.","account":"none","expected_direction":"none","horizon":"12 months","quote":"Sara Liu (Co-Founder, Senior Vice President and Director)","paragraph_id":"0001375365-26-000022:notes:477","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_officer_option_grants_before_quarterly_filing","what_changed":"New: options were granted on May 8, 2026 to two named executive officers, within the window before the May 11, 2026 10-Q filing.","account":"stock-based compensation","expected_direction":"none","horizon":"this quarter","quote":"David Weigand","paragraph_id":"0001375365-26-000022:notes:494","explanation":false},
{"id":"earnings_quality_equity_plan_reserve_increased","what_changed":"Stockholders approved a 15,000,000-share increase to the 2020 plan reserve in April 2026.","account":"stock-based compensation","expected_direction":"up","horizon":"12 months","quote":"and April 2026 increasing the share reserve","paragraph_id":"0001375365-26-000022:notes:355","explanation":false},
{"id":"earnings_quality_ceo_award_revenue_milestones_all_certified","what_changed":"Certification on August 26, 2025 of the last ($21.0 billion) annualized revenue milestone means all revenue milestones of the CEO award are achieved. Only the $110 stock-price milestone remains.","account":"stock-based compensation","expected_direction":"none","horizon":"this quarter","quote":"certified achievement of the $21.0 billion revenue milestone","paragraph_id":"0001375365-26-000022:notes:378","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_new_securities_class_actions_consolidated","what_changed":"New securities class action (Chung, filed May 12, 2026). The Bhuva, Hialeah and Chung cases were consolidated on July 13, 2026 with institutional lead plaintiffs. The sentence on the lead-plaintiff appeal was removed.","account":"accrued liabilities","expected_direction":"none","horizon":"12 months","quote":"consolidated the cases on July 13, 2026, appointing a coalition of institutional investors as lead plaintiffs","paragraph_id":"0001375365-26-000022:notes:456","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_derivative_suits_added","what_changed":"New derivative suits: Pill (May 19), City of Birmingham (June 24), Cepeda (July 10) and Roy (August 21, 2026). Delaware consolidations took place on May 8 and August 18, 2026.","account":"accrued liabilities","expected_direction":"none","horizon":"12 months","quote":"Three additional substantially similar lawsuits were filed in the Northern District of California","paragraph_id":"0001375365-26-000022:notes:457","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_sec_subpoena_no_longer_called_preliminary","what_changed":"The SEC paragraph now cites the October 22, 2024 SDNY subpoenas, the Hindenburg report and the April 28, 2026 subpoena. It drops the Q3 sentence that the matter is too preliminary to judge and that loss cannot be estimated.","account":"accrued liabilities","expected_direction":"none","horizon":"12 months","quote":"The Company is cooperating and continues to produce responsive documents in response to the subpoenas","paragraph_id":"0001375365-26-000022:notes:458","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_grand_jury_subpoena_compliance_and_internal_controls","what_changed":"New: the company received an SDNY grand jury subpoena tied to the March 19, 2026 export-control indictment. It covers the compliance program and internal controls.","account":"accrued liabilities","expected_direction":"none","horizon":"12 months","quote":"seeking documents and information relating to the individuals and facts referenced in the Indictment","paragraph_id":"0001375365-26-000022:notes:459","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_independent_investigation_disclosure_dropped","what_changed":"Q3 disclosed a board-led independent investigation into the indictment allegations with no conclusion yet. The 10-K's Note 15 has no counterpart paragraph and reports no conclusion. MD&A still cites internal investigation costs.","account":"general and administrative","expected_direction":"none","horizon":"12 months","quote":"The investigations are ongoing and no conclusion has been reached","paragraph_id":"0001375365-26-000014:note_history:7","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_export_enforcement_requests","what_changed":"New: the company routinely receives subpoenas from OEE about GPU exports and several requests remain open. It says it has not been told it is a target, and that being one could bring civil penalties.","account":"accrued liabilities","expected_direction":"none","horizon":"12 months","quote":"it routinely receives subpoenas and other requests to produce information about customers and/or contemplated transactions from OEE","paragraph_id":"0001375365-26-000022:notes:462","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_ontario_class_action_dismissed","what_changed":"The Ontario securities class action was dismissed by the plaintiff on December 8, 2025.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"Plaintiff dismissed the complaint on December 8, 2025","paragraph_id":"0001375365-26-000022:notes:463","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_netlist_trade_commission_complaints","what_changed":"New Netlist USITC actions. The Samsung-related complaints are expected to resolve after the August 5, 2026 settlement. A new August 11, 2026 complaint against Micron and downstream customers, including the company, seeks exclusion and cease-and-desist orders.","account":"none","expected_direction":"none","horizon":"12 months","quote":"seeking a limited exclusion order, cease-and-desist orders and a bond","paragraph_id":"0001375365-26-000022:notes:464","explanation":false},
{"id":"across_documents_earnings_release_preliminary_before_audit","what_changed":"The August 11 release figures are preliminary, with closing procedures incomplete and no auditor procedures performed. The 10-K was audited on August 31. Matching release to 10-K is left to the numbers reader.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"has not audited, reviewed, compiled or performed any procedures with respect to such preliminary data","paragraph_id":"0001375365-26-000021:8k_2_02:29","explanation":false},
{"id":"structure_and_disclosure_changes_income_tax_disclosure_standard_adopted","what_changed":"ASU 2023-09 was adopted retrospectively in FY2026, adding a new rate reconciliation format and cash taxes by jurisdiction. Tennessee is named as the main state driver.","account":"income tax provision","expected_direction":"none","horizon":"this quarter","quote":"We adopted ASU 2023-09 during fiscal year 2026 on a retrospective basis","paragraph_id":"0001375365-26-000022:notes:94","explanation":false}
]
```

Item count: 82. Items with `explanation: true`: 2.

## Insufficient (6)

1. Item 1A diff: not in the directory, so risk-factor changes are unassessed.
2. Exhibit 21 diff: not in the directory, so subsidiary changes (e.g. Malaysia) are unassessed.
3. Exhibit 10: none pulled. The credit agreement amendments, the CTBC extension and the E.SUN waiver were not read in their exhibit text.
4. 8-K bodies other than the 2026-08-11 Item 2.02: only item codes are given. Not readable: 5.02 on 2026-03-20, 2026-04-20 and 2026-05-18; 8.01 on 2026-06-09 and 2026-08-05; 1.01/3.03/5.03 on 2026-06-15; 1.01/7.01 on 2026-06-12; and 1.01 on 2026-01-26 and 2026-01-29. Officer changes around the indictment cannot be assessed.
5. Prior 10-K (FY2025) text is absent. Novelty for 10-K-only paragraphs rests on in-text dates and the Q2→Q3 history.
6. The nature of "Asset held for others" and "Customer-related liabilities", and the reason the Liaw sibling sentences were removed: no explaining prose in the input.

## Paragraphs not made into items

Note-history paragraphs are context, not part of this list. Two of them are quoted as item sources: 0001375365-26-000014:note_history:7 and 0001375365-26-000007:note_history:61.

### Auditor's report
- 0001375365-26-000022:auditors_report:1 heading
- 0001375365-26-000022:auditors_report:2 addressee
- 0001375365-26-000022:auditors_report:3 addressee
- 0001375365-26-000022:auditors_report:4 location
- 0001375365-26-000022:auditors_report:5 heading
- 0001375365-26-000022:auditors_report:6 unqualified opinion, dates rolled forward
- 0001375365-26-000022:auditors_report:7 same change as controls_audit_and_filings_auditor_adverse_icfr_opinion
- 0001375365-26-000022:auditors_report:8 heading
- 0001375365-26-000022:auditors_report:9 standard basis language
- 0001375365-26-000022:auditors_report:10 standard
- 0001375365-26-000022:auditors_report:11 standard
- 0001375365-26-000022:auditors_report:12 heading
- 0001375365-26-000022:auditors_report:13 standard CAM preamble
- 0001375365-26-000022:auditors_report:14 heading
- 0001375365-26-000022:auditors_report:15 same change as inventory CAM item
- 0001375365-26-000022:auditors_report:17 page footer
- 0001375365-26-000022:auditors_report:18 lead-in
- 0001375365-26-000022:auditors_report:19 same change as inventory CAM item
- 0001375365-26-000022:auditors_report:20 same change as inventory CAM item
- 0001375365-26-000022:auditors_report:21 same change as inventory CAM item
- 0001375365-26-000022:auditors_report:22 same change as inventory CAM item
- 0001375365-26-000022:auditors_report:23 heading
- 0001375365-26-000022:auditors_report:24 same change as revenue CAM item
- 0001375365-26-000022:auditors_report:25 same change as revenue CAM item
- 0001375365-26-000022:auditors_report:26 lead-in
- 0001375365-26-000022:auditors_report:27 same change as revenue CAM item
- 0001375365-26-000022:auditors_report:29 same change as revenue CAM item
- 0001375365-26-000022:auditors_report:30 same change as revenue CAM item
- 0001375365-26-000022:auditors_report:31 signature
- 0001375365-26-000022:auditors_report:32 tenure unchanged since 2024
- 0001375365-26-000022:auditors_report:33 location
- 0001375365-26-000022:auditors_report:34 date rolled forward
- 0001375365-26-000022:auditors_report:35 page footer
- 0001375365-26-000022:auditors_report:36 page header

### Item 9A
- 0001375365-26-000022:item_9a:1 heading
- 0001375365-26-000022:item_9a:2 standard
- 0001375365-26-000022:item_9a:3 heading
- 0001375365-26-000022:item_9a:5 heading
- 0001375365-26-000022:item_9a:6 standard definition
- 0001375365-26-000022:item_9a:7 standard
- 0001375365-26-000022:item_9a:8 standard
- 0001375365-26-000022:item_9a:9 standard
- 0001375365-26-000022:item_9a:10 standard, date rolled forward
- 0001375365-26-000022:item_9a:12 page footer
- 0001375365-26-000022:item_9a:13 heading
- 0001375365-26-000022:item_9a:14 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:15 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:16 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:17 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:18 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:19 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:20 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:22 standard fair-presentation assertion
- 0001375365-26-000022:item_9a:23 heading
- 0001375365-26-000022:item_9a:24 standard
- 0001375365-26-000022:item_9a:25 standard
- 0001375365-26-000022:item_9a:26 page footer
- 0001375365-26-000022:item_9a:27 heading
- 0001375365-26-000022:item_9a:28 same change as remediation-timetable item
- 0001375365-26-000022:item_9a:29 same change as remediation-timetable item
- 0001375365-26-000022:item_9a:30 same change as remediation-timetable item
- 0001375365-26-000022:item_9a:31 same change as remediation-timetable item
- 0001375365-26-000022:item_9a:33 standard
- 0001375365-26-000022:item_9a:34 same change as remediation-timetable item
- 0001375365-26-000022:item_9a:35 heading
- 0001375365-26-000022:item_9a:36 same change as three-weaknesses-remediated item
- 0001375365-26-000022:item_9a:37 same change as remediation-timetable item
- 0001375365-26-000022:item_9a:38 page footer
- 0001375365-26-000022:item_9a:39 heading
- 0001375365-26-000022:item_9a:40 addressee
- 0001375365-26-000022:item_9a:41 addressee
- 0001375365-26-000022:item_9a:42 location
- 0001375365-26-000022:item_9a:43 heading
- 0001375365-26-000022:item_9a:45 standard
- 0001375365-26-000022:item_9a:46 cross-reference, date rolled forward
- 0001375365-26-000022:item_9a:47 heading
- 0001375365-26-000022:item_9a:48 standard
- 0001375365-26-000022:item_9a:49 standard
- 0001375365-26-000022:item_9a:50 same change as adverse ICFR item
- 0001375365-26-000022:item_9a:51 same change as adverse ICFR item
- 0001375365-26-000022:item_9a:52 page footer
- 0001375365-26-000022:item_9a:53 heading
- 0001375365-26-000022:item_9a:54 standard
- 0001375365-26-000022:item_9a:55 standard
- 0001375365-26-000022:item_9a:56 signature
- 0001375365-26-000022:item_9a:57 location
- 0001375365-26-000022:item_9a:58 date rolled forward
- 0001375365-26-000022:item_9a:59 page footer

### MD&A
- 0001375365-26-000022:mdna:1 heading
- 0001375365-26-000022:mdna:2 heading
- 0001375365-26-000022:mdna:3 business description
- 0001375365-26-000022:mdna:4 amounts only
- 0001375365-26-000022:mdna:5 strategy description
- 0001375365-26-000022:mdna:6 standard
- 0001375365-26-000022:mdna:7 heading
- 0001375365-26-000022:mdna:8 generic demand narrative
- 0001375365-26-000022:mdna:9 page footer
- 0001375365-26-000022:mdna:10 heading
- 0001375365-26-000022:mdna:12 heading
- 0001375365-26-000022:mdna:13 lead-in
- 0001375365-26-000022:mdna:14 table, amounts only
- 0001375365-26-000022:mdna:16 same change as competitive-pricing margin item
- 0001375365-26-000022:mdna:17 same change as opex-growth item
- 0001375365-26-000022:mdna:18 amounts only
- 0001375365-26-000022:mdna:19 heading
- 0001375365-26-000022:mdna:20 standard
- 0001375365-26-000022:mdna:21 standard
- 0001375365-26-000022:mdna:22 page footer
- 0001375365-26-000022:mdna:23 cross-reference
- 0001375365-26-000022:mdna:24 heading
- 0001375365-26-000022:mdna:25 standard
- 0001375365-26-000022:mdna:26 standard policy, no change evident
- 0001375365-26-000022:mdna:27 standard policy, no change evident
- 0001375365-26-000022:mdna:28 standard policy, no change evident
- 0001375365-26-000022:mdna:29 heading
- 0001375365-26-000022:mdna:30 standard; referenced in finished-goods item
- 0001375365-26-000022:mdna:31 standard policy
- 0001375365-26-000022:mdna:32 page footer
- 0001375365-26-000022:mdna:34 heading
- 0001375365-26-000022:mdna:35 standard
- 0001375365-26-000022:mdna:36 standard
- 0001375365-26-000022:mdna:37 standard
- 0001375365-26-000022:mdna:38 standard
- 0001375365-26-000022:mdna:39 heading
- 0001375365-26-000022:mdna:40 heading
- 0001375365-26-000022:mdna:41 heading
- 0001375365-26-000022:mdna:42 standard
- 0001375365-26-000022:mdna:43 heading
- 0001375365-26-000022:mdna:44 standard
- 0001375365-26-000022:mdna:45 page footer
- 0001375365-26-000022:mdna:46 related-party percentages, amounts only
- 0001375365-26-000022:mdna:47 heading
- 0001375365-26-000022:mdna:48 standard
- 0001375365-26-000022:mdna:49 heading
- 0001375365-26-000022:mdna:50 standard
- 0001375365-26-000022:mdna:51 heading
- 0001375365-26-000022:mdna:52 standard
- 0001375365-26-000022:mdna:53 heading
- 0001375365-26-000022:mdna:54 standard
- 0001375365-26-000022:mdna:55 heading
- 0001375365-26-000022:mdna:56 standard
- 0001375365-26-000022:mdna:57 page footer
- 0001375365-26-000022:mdna:58 lead-in
- 0001375365-26-000022:mdna:59 table, amounts only
- 0001375365-26-000022:mdna:60 footnote
- 0001375365-26-000022:mdna:61 lead-in
- 0001375365-26-000022:mdna:62 table, amounts only
- 0001375365-26-000022:mdna:63 footnote
- 0001375365-26-000022:mdna:64 page footer
- 0001375365-26-000022:mdna:65 heading
- 0001375365-26-000022:mdna:66 lead-in
- 0001375365-26-000022:mdna:67 table, amounts only
- 0001375365-26-000022:mdna:68 heading
- 0001375365-26-000022:mdna:70 heading
- 0001375365-26-000022:mdna:71 prior-year comparison carried
- 0001375365-26-000022:mdna:72 heading
- 0001375365-26-000022:mdna:73 lead-in
- 0001375365-26-000022:mdna:74 table, amounts only
- 0001375365-26-000022:mdna:75 heading
- 0001375365-26-000022:mdna:78 page footer
- 0001375365-26-000022:mdna:79 heading
- 0001375365-26-000022:mdna:80 prior-year comparison carried
- 0001375365-26-000022:mdna:81 prior-year comparison carried
- 0001375365-26-000022:mdna:82 heading
- 0001375365-26-000022:mdna:83 lead-in
- 0001375365-26-000022:mdna:84 table, amounts only
- 0001375365-26-000022:mdna:85 heading
- 0001375365-26-000022:mdna:88 page footer
- 0001375365-26-000022:mdna:90 heading
- 0001375365-26-000022:mdna:91 prior-year comparison carried
- 0001375365-26-000022:mdna:92 prior-year comparison carried
- 0001375365-26-000022:mdna:93 prior-year comparison carried
- 0001375365-26-000022:mdna:94 page footer
- 0001375365-26-000022:mdna:95 heading
- 0001375365-26-000022:mdna:96 lead-in
- 0001375365-26-000022:mdna:97 table, amounts only
- 0001375365-26-000022:mdna:98 heading
- 0001375365-26-000022:mdna:99 same change as sublease-income across-documents item
- 0001375365-26-000022:mdna:102 heading
- 0001375365-26-000022:mdna:103 prior-year comparison carried
- 0001375365-26-000022:mdna:104 prior-year comparison carried
- 0001375365-26-000022:mdna:105 prior-year comparison carried
- 0001375365-26-000022:mdna:106 page footer
- 0001375365-26-000022:mdna:107 heading
- 0001375365-26-000022:mdna:108 lead-in
- 0001375365-26-000022:mdna:109 table, amounts only
- 0001375365-26-000022:mdna:110 heading
- 0001375365-26-000022:mdna:111 amounts; drivers same as tax-rate item
- 0001375365-26-000022:mdna:116 heading
- 0001375365-26-000022:mdna:117 prior-year comparison carried
- 0001375365-26-000022:mdna:118 page footer
- 0001375365-26-000022:mdna:119 heading
- 0001375365-26-000022:mdna:120 same change as Corporate Venture item
- 0001375365-26-000022:mdna:121 lead-in
- 0001375365-26-000022:mdna:122 table, amounts only
- 0001375365-26-000022:mdna:123 footnote
- 0001375365-26-000022:mdna:124 heading
- 0001375365-26-000022:mdna:125 same change as Corporate Venture item
- 0001375365-26-000022:mdna:126 heading
- 0001375365-26-000022:mdna:127 prior-year comparison carried
- 0001375365-26-000022:mdna:128 heading
- 0001375365-26-000022:mdna:130 standard
- 0001375365-26-000022:mdna:131 generic financing-flexibility language
- 0001375365-26-000022:mdna:132 standard liquidity assertion
- 0001375365-26-000022:mdna:133 page footer
- 0001375365-26-000022:mdna:134 lead-in
- 0001375365-26-000022:mdna:135 table, amounts only
- 0001375365-26-000022:mdna:136 heading
- 0001375365-26-000022:mdna:137 standard
- 0001375365-26-000022:mdna:139 heading
- 0001375365-26-000022:mdna:140 standard
- 0001375365-26-000022:mdna:141 amounts only
- 0001375365-26-000022:mdna:142 heading
- 0001375365-26-000022:mdna:143 standard
- 0001375365-26-000022:mdna:144 same change as equity-offering items
- 0001375365-26-000022:mdna:145 heading
- 0001375365-26-000022:mdna:146 cross-reference
- 0001375365-26-000022:mdna:147 page footer
- 0001375365-26-000022:mdna:148 cross-reference
- 0001375365-26-000022:mdna:149 cross-reference
- 0001375365-26-000022:mdna:150 heading
- 0001375365-26-000022:mdna:152 standard
- 0001375365-26-000022:mdna:153 heading
- 0001375365-26-000022:mdna:154 amounts; same change as purchase-commitments item
- 0001375365-26-000022:mdna:155 heading
- 0001375365-26-000022:mdna:156 cross-reference
- 0001375365-26-000022:mdna:157 page footer

### Notes
- 0001375365-26-000022:notes:1 cover entry
- 0001375365-26-000022:notes:2 cybersecurity process, no financial substance
- 0001375365-26-000022:notes:3 cybersecurity process
- 0001375365-26-000022:notes:4 cybersecurity process
- 0001375365-26-000022:notes:5 cybersecurity process
- 0001375365-26-000022:notes:6 heading
- 0001375365-26-000022:notes:7 cybersecurity governance
- 0001375365-26-000022:notes:8 cybersecurity governance
- 0001375365-26-000022:notes:9 cybersecurity governance
- 0001375365-26-000022:notes:10 cybersecurity governance
- 0001375365-26-000022:notes:11 cybersecurity governance
- 0001375365-26-000022:notes:12 heading
- 0001375365-26-000022:notes:13 heading
- 0001375365-26-000022:notes:14 same change as Malaysia operations item
- 0001375365-26-000022:notes:15 heading
- 0001375365-26-000022:notes:16 standard
- 0001375365-26-000022:notes:17 heading
- 0001375365-26-000022:notes:18 standard
- 0001375365-26-000022:notes:19 heading
- 0001375365-26-000022:notes:20 standard
- 0001375365-26-000022:notes:21 standard
- 0001375365-26-000022:notes:22 standard
- 0001375365-26-000022:notes:23 standard
- 0001375365-26-000022:notes:24 same change as extended-payment-terms item
- 0001375365-26-000022:notes:25 heading
- 0001375365-26-000022:notes:26 standard
- 0001375365-26-000022:notes:27 heading
- 0001375365-26-000022:notes:29 heading
- 0001375365-26-000022:notes:31 standard rebate policy
- 0001375365-26-000022:notes:32 heading
- 0001375365-26-000022:notes:33 lead-in
- 0001375365-26-000022:notes:34 table, standard lives
- 0001375365-26-000022:notes:35 standard
- 0001375365-26-000022:notes:36 standard
- 0001375365-26-000022:notes:37 standard
- 0001375365-26-000022:notes:38 heading
- 0001375365-26-000022:notes:39 standard
- 0001375365-26-000022:notes:40 wording only; Q3 "or channel partners" phrase dropped
- 0001375365-26-000022:notes:41 standard
- 0001375365-26-000022:notes:42 standard
- 0001375365-26-000022:notes:43 standard
- 0001375365-26-000022:notes:44 standard
- 0001375365-26-000022:notes:47 standard
- 0001375365-26-000022:notes:48 heading
- 0001375365-26-000022:notes:49 standard
- 0001375365-26-000022:notes:50 standard
- 0001375365-26-000022:notes:51 amounts only
- 0001375365-26-000022:notes:52 heading
- 0001375365-26-000022:notes:53 standard
- 0001375365-26-000022:notes:54 heading
- 0001375365-26-000022:notes:55 standard
- 0001375365-26-000022:notes:56 heading
- 0001375365-26-000022:notes:57 amounts only
- 0001375365-26-000022:notes:58 standard
- 0001375365-26-000022:notes:59 heading
- 0001375365-26-000022:notes:61 heading
- 0001375365-26-000022:notes:62 standard
- 0001375365-26-000022:notes:63 heading
- 0001375365-26-000022:notes:64 standard
- 0001375365-26-000022:notes:65 standard
- 0001375365-26-000022:notes:66 heading
- 0001375365-26-000022:notes:67 standard
- 0001375365-26-000022:notes:68 standard
- 0001375365-26-000022:notes:69 standard
- 0001375365-26-000022:notes:71 heading
- 0001375365-26-000022:notes:72 standard
- 0001375365-26-000022:notes:73 standard
- 0001375365-26-000022:notes:74 heading
- 0001375365-26-000022:notes:75 amounts only
- 0001375365-26-000022:notes:76 heading
- 0001375365-26-000022:notes:78 same change as two-class EPS item
- 0001375365-26-000022:notes:79 same change as two-class EPS item
- 0001375365-26-000022:notes:80 heading
- 0001375365-26-000022:notes:81 standard
- 0001375365-26-000022:notes:82 heading
- 0001375365-26-000022:notes:83 standard
- 0001375365-26-000022:notes:84 amounts only
- 0001375365-26-000022:notes:85 amounts only
- 0001375365-26-000022:notes:86 heading
- 0001375365-26-000022:notes:87 standard
- 0001375365-26-000022:notes:88 same as Q3 text
- 0001375365-26-000022:notes:90 heading
- 0001375365-26-000022:notes:91 standard
- 0001375365-26-000022:notes:92 heading
- 0001375365-26-000022:notes:93 adopted ASU, no impact
- 0001375365-26-000022:notes:95 heading
- 0001375365-26-000022:notes:96 pronouncement not yet adopted
- 0001375365-26-000022:notes:97 pronouncement not yet adopted
- 0001375365-26-000022:notes:98 pronouncement not yet adopted, no expected impact
- 0001375365-26-000022:notes:99 pronouncement not yet adopted, no expected impact
- 0001375365-26-000022:notes:100 pronouncement not yet adopted, no expected impact
- 0001375365-26-000022:notes:101 pronouncement not yet adopted, no expected impact
- 0001375365-26-000022:notes:102 heading
- 0001375365-26-000022:notes:104 heading
- 0001375365-26-000022:notes:105 standard segment text
- 0001375365-26-000022:notes:106 standard segment text
- 0001375365-26-000022:notes:107 standard segment text
- 0001375365-26-000022:notes:108 standard segment text
- 0001375365-26-000022:notes:109 heading
- 0001375365-26-000022:notes:110 lead-in
- 0001375365-26-000022:notes:111 table, amounts only
- 0001375365-26-000022:notes:112 amounts only
- 0001375365-26-000022:notes:113 heading
- 0001375365-26-000022:notes:114 amounts only
- 0001375365-26-000022:notes:115 lead-in
- 0001375365-26-000022:notes:116 table, amounts only
- 0001375365-26-000022:notes:117 amounts only
- 0001375365-26-000022:notes:118 heading
- 0001375365-26-000022:notes:119 generic risk description
- 0001375365-26-000022:notes:121 heading
- 0001375365-26-000022:notes:122 same change as extended-payment-terms item
- 0001375365-26-000022:notes:123 standard
- 0001375365-26-000022:notes:124 same change as customer-advances item
- 0001375365-26-000022:notes:126 heading
- 0001375365-26-000022:notes:128 heading
- 0001375365-26-000022:notes:129 standard
- 0001375365-26-000022:notes:130 standard
- 0001375365-26-000022:notes:131 heading
- 0001375365-26-000022:notes:132 standard
- 0001375365-26-000022:notes:133 heading
- 0001375365-26-000022:notes:134 standard
- 0001375365-26-000022:notes:135 lead-in
- 0001375365-26-000022:notes:136 table, amounts only
- 0001375365-26-000022:notes:137 footnote
- 0001375365-26-000022:notes:138 footnote, amounts only
- 0001375365-26-000022:notes:139 amounts only; see sublease-income item
- 0001375365-26-000022:notes:140 standard
- 0001375365-26-000022:notes:141 heading
- 0001375365-26-000022:notes:142 same change as extended-payment-terms item
- 0001375365-26-000022:notes:143 amounts only
- 0001375365-26-000022:notes:144 amounts only
- 0001375365-26-000022:notes:145 heading
- 0001375365-26-000022:notes:146 lead-in
- 0001375365-26-000022:notes:147 table, amounts only
- 0001375365-26-000022:notes:150 existing investee, amounts only
- 0001375365-26-000022:notes:151 carried from FY2025
- 0001375365-26-000022:notes:152 heading
- 0001375365-26-000022:notes:153 lead-in
- 0001375365-26-000022:notes:154 table, amounts only
- 0001375365-26-000022:notes:155 heading
- 0001375365-26-000022:notes:156 lead-in
- 0001375365-26-000022:notes:157 same change as restricted-cash item
- 0001375365-26-000022:notes:158 heading
- 0001375365-26-000022:notes:159 standard
- 0001375365-26-000022:notes:160 table, amounts only
- 0001375365-26-000022:notes:161 table, amounts only
- 0001375365-26-000022:notes:162 amounts only
- 0001375365-26-000022:notes:163 heading
- 0001375365-26-000022:notes:165 heading
- 0001375365-26-000022:notes:166 table, amounts only
- 0001375365-26-000022:notes:167 amounts only
- 0001375365-26-000022:notes:168 amounts only
- 0001375365-26-000022:notes:169 heading
- 0001375365-26-000022:notes:170 table, amounts only; tariff line in tariff-receivable item
- 0001375365-26-000022:notes:172 heading
- 0001375365-26-000022:notes:173 table, amounts only
- 0001375365-26-000022:notes:174 table, amounts only
- 0001375365-26-000022:notes:175 standard
- 0001375365-26-000022:notes:176 heading
- 0001375365-26-000022:notes:177 amounts only
- 0001375365-26-000022:notes:178 heading
- 0001375365-26-000022:notes:179 carried from Q2
- 0001375365-26-000022:notes:180 carried from Q2 terms
- 0001375365-26-000022:notes:181 lead-in
- 0001375365-26-000022:notes:182 same change as receivables-sold item
- 0001375365-26-000022:notes:183 footnote
- 0001375365-26-000022:notes:185 heading
- 0001375365-26-000022:notes:186 lead-in
- 0001375365-26-000022:notes:187 table, amounts only
- 0001375365-26-000022:notes:188 heading
- 0001375365-26-000022:notes:189 lead-in
- 0001375365-26-000022:notes:190 table, amounts only
- 0001375365-26-000022:notes:191 lead-in
- 0001375365-26-000022:notes:192 table, amounts only
- 0001375365-26-000022:notes:193 heading
- 0001375365-26-000022:notes:194 carried from Q3
- 0001375365-26-000022:notes:196 same change as JP Morgan lien item
- 0001375365-26-000022:notes:199 heading
- 0001375365-26-000022:notes:200 carried from Q3
- 0001375365-26-000022:notes:201 carried from Q3
- 0001375365-26-000022:notes:202 carried from Q3
- 0001375365-26-000022:notes:203 carried from Q3
- 0001375365-26-000022:notes:206 amounts only
- 0001375365-26-000022:notes:207 heading
- 0001375365-26-000022:notes:208 heading
- 0001375365-26-000022:notes:209 carried history
- 0001375365-26-000022:notes:210 carried history
- 0001375365-26-000022:notes:211 carried history
- 0001375365-26-000022:notes:212 heading
- 0001375365-26-000022:notes:213 carried history
- 0001375365-26-000022:notes:214 heading
- 0001375365-26-000022:notes:216 amounts only
- 0001375365-26-000022:notes:217 heading
- 0001375365-26-000022:notes:218 carried history
- 0001375365-26-000022:notes:219 carried history
- 0001375365-26-000022:notes:220 amounts only
- 0001375365-26-000022:notes:221 amounts only
- 0001375365-26-000022:notes:222 heading
- 0001375365-26-000022:notes:223 heading
- 0001375365-26-000022:notes:224 carried history
- 0001375365-26-000022:notes:225 carried history
- 0001375365-26-000022:notes:226 carried history
- 0001375365-26-000022:notes:227 carried from Q2
- 0001375365-26-000022:notes:228 carried from Q2; floor wording only
- 0001375365-26-000022:notes:229 carried history
- 0001375365-26-000022:notes:230 amounts only
- 0001375365-26-000022:notes:231 amounts only
- 0001375365-26-000022:notes:232 heading
- 0001375365-26-000022:notes:233 heading
- 0001375365-26-000022:notes:234 carried history
- 0001375365-26-000022:notes:235 carried history
- 0001375365-26-000022:notes:236 same change as bilateral-cap item
- 0001375365-26-000022:notes:238 amounts only
- 0001375365-26-000022:notes:239 heading
- 0001375365-26-000022:notes:240 carried history
- 0001375365-26-000022:notes:241 carried history, amounts
- 0001375365-26-000022:notes:242 carried history
- 0001375365-26-000022:notes:243 carried history
- 0001375365-26-000022:notes:244 carried history
- 0001375365-26-000022:notes:246 amounts only
- 0001375365-26-000022:notes:247 heading
- 0001375365-26-000022:notes:248 heading
- 0001375365-26-000022:notes:249 carried history
- 0001375365-26-000022:notes:250 carried history
- 0001375365-26-000022:notes:251 carried history
- 0001375365-26-000022:notes:252 same change as bilateral-cap item
- 0001375365-26-000022:notes:253 amounts only
- 0001375365-26-000022:notes:254 heading
- 0001375365-26-000022:notes:255 carried history
- 0001375365-26-000022:notes:256 amounts only
- 0001375365-26-000022:notes:257 heading
- 0001375365-26-000022:notes:258 heading
- 0001375365-26-000022:notes:259 carried history
- 0001375365-26-000022:notes:260 carried history
- 0001375365-26-000022:notes:261 carried from Q3
- 0001375365-26-000022:notes:262 amounts only
- 0001375365-26-000022:notes:263 heading
- 0001375365-26-000022:notes:264 date rolled forward; see E.SUN waiver item
- 0001375365-26-000022:notes:265 heading
- 0001375365-26-000022:notes:266 heading
- 0001375365-26-000022:notes:267 carried terms
- 0001375365-26-000022:notes:268 carried terms
- 0001375365-26-000022:notes:269 carried terms
- 0001375365-26-000022:notes:270 carried terms
- 0001375365-26-000022:notes:271 carried terms
- 0001375365-26-000022:notes:272 carried terms
- 0001375365-26-000022:notes:273 carried terms, date rolled
- 0001375365-26-000022:notes:274 carried terms
- 0001375365-26-000022:notes:275 amounts only
- 0001375365-26-000022:notes:276 carried terms
- 0001375365-26-000022:notes:277 carried terms
- 0001375365-26-000022:notes:278 carried terms
- 0001375365-26-000022:notes:279 heading
- 0001375365-26-000022:notes:280 carried terms
- 0001375365-26-000022:notes:281 carried terms
- 0001375365-26-000022:notes:282 carried terms
- 0001375365-26-000022:notes:283 carried terms
- 0001375365-26-000022:notes:284 carried terms
- 0001375365-26-000022:notes:285 carried terms
- 0001375365-26-000022:notes:286 carried terms, date rolled
- 0001375365-26-000022:notes:287 carried terms
- 0001375365-26-000022:notes:288 amounts only
- 0001375365-26-000022:notes:289 heading
- 0001375365-26-000022:notes:290 carried terms
- 0001375365-26-000022:notes:291 carried terms
- 0001375365-26-000022:notes:292 carried terms, date rolled
- 0001375365-26-000022:notes:293 carried terms
- 0001375365-26-000022:notes:294 carried terms
- 0001375365-26-000022:notes:295 carried terms
- 0001375365-26-000022:notes:296 carried terms
- 0001375365-26-000022:notes:297 carried terms
- 0001375365-26-000022:notes:298 carried terms
- 0001375365-26-000022:notes:299 amounts only
- 0001375365-26-000022:notes:300 carried terms
- 0001375365-26-000022:notes:301 carried terms
- 0001375365-26-000022:notes:302 heading and lead-in
- 0001375365-26-000022:notes:303 table, amounts only
- 0001375365-26-000022:notes:304 amounts only
- 0001375365-26-000022:notes:305 lead-in
- 0001375365-26-000022:notes:306 table, amounts only
- 0001375365-26-000022:notes:307 standard
- 0001375365-26-000022:notes:308 same change as sublicensee item
- 0001375365-26-000022:notes:310 lead-in
- 0001375365-26-000022:notes:311 table; same change as sublease-income item
- 0001375365-26-000022:notes:312 lead-in
- 0001375365-26-000022:notes:313 table; same change as sublicensee item
- 0001375365-26-000022:notes:314 lead-in
- 0001375365-26-000022:notes:315 table, amounts only
- 0001375365-26-000022:notes:316 heading
- 0001375365-26-000022:notes:317 cross-reference
- 0001375365-26-000022:notes:318 heading
- 0001375365-26-000022:notes:319 ownership amounts; removal covered by Liaw item
- 0001375365-26-000022:notes:321 heading
- 0001375365-26-000022:notes:322 standard
- 0001375365-26-000022:notes:325 amounts only
- 0001375365-26-000022:notes:326 standard
- 0001375365-26-000022:notes:327 amounts only
- 0001375365-26-000022:notes:328 heading
- 0001375365-26-000022:notes:329 no change evident
- 0001375365-26-000022:notes:331 standard; amounts
- 0001375365-26-000022:notes:332 standard
- 0001375365-26-000022:notes:333 amounts only
- 0001375365-26-000022:notes:335 heading
- 0001375365-26-000022:notes:337 heading
- 0001375365-26-000022:notes:338 carried history
- 0001375365-26-000022:notes:339 amounts only
- 0001375365-26-000022:notes:341 heading
- 0001375365-26-000022:notes:342 no transactions of note
- 0001375365-26-000022:notes:343 lead-in
- 0001375365-26-000022:notes:344 table, amounts only
- 0001375365-26-000022:notes:345 footnote
- 0001375365-26-000022:notes:346 footnote
- 0001375365-26-000022:notes:347 footnote
- 0001375365-26-000022:notes:348 lead-in
- 0001375365-26-000022:notes:349 table, amounts only
- 0001375365-26-000022:notes:350 same change as Corporate Venture item
- 0001375365-26-000022:notes:351 lead-in
- 0001375365-26-000022:notes:352 table, amounts only
- 0001375365-26-000022:notes:353 heading
- 0001375365-26-000022:notes:354 heading
- 0001375365-26-000022:notes:356 amounts only
- 0001375365-26-000022:notes:357 heading
- 0001375365-26-000022:notes:358 standard
- 0001375365-26-000022:notes:359 amounts only
- 0001375365-26-000022:notes:360 lead-in
- 0001375365-26-000022:notes:361 table, amounts only
- 0001375365-26-000022:notes:362 lead-in
- 0001375365-26-000022:notes:363 table, amounts only
- 0001375365-26-000022:notes:364 heading
- 0001375365-26-000022:notes:365 heading
- 0001375365-26-000022:notes:366 carried
- 0001375365-26-000022:notes:367 lead-in
- 0001375365-26-000022:notes:368 table; same change as CEO award item
- 0001375365-26-000022:notes:369 carried
- 0001375365-26-000022:notes:370 carried certification
- 0001375365-26-000022:notes:371 carried certification
- 0001375365-26-000022:notes:372 carried certification
- 0001375365-26-000022:notes:373 carried certification
- 0001375365-26-000022:notes:374 carried certification
- 0001375365-26-000022:notes:375 carried certification
- 0001375365-26-000022:notes:376 carried certification
- 0001375365-26-000022:notes:377 carried certification
- 0001375365-26-000022:notes:379 amounts only
- 0001375365-26-000022:notes:380 carried methodology
- 0001375365-26-000022:notes:381 lead-in
- 0001375365-26-000022:notes:382 table, amounts only
- 0001375365-26-000022:notes:383 amounts only
- 0001375365-26-000022:notes:384 amounts only
- 0001375365-26-000022:notes:385 lead-in
- 0001375365-26-000022:notes:386 table, amounts only
- 0001375365-26-000022:notes:387 heading
- 0001375365-26-000022:notes:388 lead-in
- 0001375365-26-000022:notes:389 table, amounts only
- 0001375365-26-000022:notes:390 amounts only
- 0001375365-26-000022:notes:391 amounts only
- 0001375365-26-000022:notes:392 amounts only
- 0001375365-26-000022:notes:393 heading
- 0001375365-26-000022:notes:394 heading
- 0001375365-26-000022:notes:395 same change as preferred-issued item
- 0001375365-26-000022:notes:396 heading
- 0001375365-26-000022:notes:397 standard
- 0001375365-26-000022:notes:398 heading
- 0001375365-26-000022:notes:399 carried history
- 0001375365-26-000022:notes:400 carried history
- 0001375365-26-000022:notes:401 carried history
- 0001375365-26-000022:notes:403 same change as common-offering item
- 0001375365-26-000022:notes:404 heading
- 0001375365-26-000022:notes:405 carried history
- 0001375365-26-000022:notes:406 carried history
- 0001375365-26-000022:notes:407 carried history
- 0001375365-26-000022:notes:408 date rolled forward
- 0001375365-26-000022:notes:409 heading
- 0001375365-26-000022:notes:411 same change as preferred-issued item
- 0001375365-26-000022:notes:412 heading
- 0001375365-26-000022:notes:414 heading
- 0001375365-26-000022:notes:415 instrument terms; same change as preferred-issued item
- 0001375365-26-000022:notes:416 lead-in
- 0001375365-26-000022:notes:417 table, instrument terms
- 0001375365-26-000022:notes:418 lead-in
- 0001375365-26-000022:notes:419 table, instrument terms
- 0001375365-26-000022:notes:420 instrument terms
- 0001375365-26-000022:notes:421 instrument terms
- 0001375365-26-000022:notes:422 heading
- 0001375365-26-000022:notes:423 instrument terms
- 0001375365-26-000022:notes:424 heading
- 0001375365-26-000022:notes:425 instrument terms
- 0001375365-26-000022:notes:426 instrument terms
- 0001375365-26-000022:notes:427 heading
- 0001375365-26-000022:notes:429 heading
- 0001375365-26-000022:notes:430 same change as ASU 2023-09 item
- 0001375365-26-000022:notes:431 lead-in
- 0001375365-26-000022:notes:432 table, amounts only
- 0001375365-26-000022:notes:433 lead-in
- 0001375365-26-000022:notes:434 table, amounts only
- 0001375365-26-000022:notes:435 lead-in
- 0001375365-26-000022:notes:436 table, amounts only
- 0001375365-26-000022:notes:437 amounts only
- 0001375365-26-000022:notes:438 lead-in
- 0001375365-26-000022:notes:439 table, amounts only
- 0001375365-26-000022:notes:440 same change as ASU 2023-09 item
- 0001375365-26-000022:notes:441 lead-in
- 0001375365-26-000022:notes:442 table; same change as ASU 2023-09 item
- 0001375365-26-000022:notes:443 amounts only
- 0001375365-26-000022:notes:444 lead-in
- 0001375365-26-000022:notes:445 table, amounts only
- 0001375365-26-000022:notes:446 footnote
- 0001375365-26-000022:notes:447 amounts only
- 0001375365-26-000022:notes:448 amounts only
- 0001375365-26-000022:notes:449 standard
- 0001375365-26-000022:notes:451 same change as OBBBA item
- 0001375365-26-000022:notes:452 same change as California item
- 0001375365-26-000022:notes:453 same change as Malaysia tax-incentive item
- 0001375365-26-000022:notes:454 heading
- 0001375365-26-000022:notes:455 heading
- 0001375365-26-000022:notes:460 generic litigation language
- 0001375365-26-000022:notes:461 generic litigation language
- 0001375365-26-000022:notes:465 heading
- 0001375365-26-000022:notes:466 wording only
- 0001375365-26-000022:notes:467 heading
- 0001375365-26-000022:notes:470 cross-reference
- 0001375365-26-000022:notes:471 heading
- 0001375365-26-000022:notes:472 standard
- 0001375365-26-000022:notes:473 amounts only
- 0001375365-26-000022:notes:474 amounts only
- 0001375365-26-000022:notes:475 amounts only
- 0001375365-26-000022:notes:476 lead-in
- 0001375365-26-000022:notes:478 rule line
- 0001375365-26-000022:notes:479 footnote
- 0001375365-26-000022:notes:480 footnote
- 0001375365-26-000022:notes:481 footnote
- 0001375365-26-000022:notes:482 footnote
- 0001375365-26-000022:notes:483 heading
- 0001375365-26-000022:notes:484 standard grant policy
- 0001375365-26-000022:notes:485 standard grant policy
- 0001375365-26-000022:notes:486 standard grant policy
- 0001375365-26-000022:notes:487 standard grant policy
- 0001375365-26-000022:notes:488 standard grant policy
- 0001375365-26-000022:notes:489 standard grant policy
- 0001375365-26-000022:notes:490 standard grant policy
- 0001375365-26-000022:notes:491 standard grant policy
- 0001375365-26-000022:notes:492 standard grant policy
- 0001375365-26-000022:notes:493 same change as option-grant item
- 0001375365-26-000022:notes:495 footnote
- 0001375365-26-000022:notes:496 footnote; filing's own price-change figure, not used

### 8-K Item 2.02 (0001375365-26-000021)
- 0001375365-26-000021:8k_2_02:1 exhibit header
- 0001375365-26-000021:8k_2_02:2 exhibit header
- 0001375365-26-000021:8k_2_02:3 exhibit header
- 0001375365-26-000021:8k_2_02:4 title
- 0001375365-26-000021:8k_2_02:5 dateline
- 0001375365-26-000021:8k_2_02:6 heading
- 0001375365-26-000021:8k_2_02:7 amounts only
- 0001375365-26-000021:8k_2_02:8 same change as Q4 gross-margin item
- 0001375365-26-000021:8k_2_02:9 amounts only
- 0001375365-26-000021:8k_2_02:10 amounts only
- 0001375365-26-000021:8k_2_02:11 amounts only
- 0001375365-26-000021:8k_2_02:12 amounts only
- 0001375365-26-000021:8k_2_02:15 non-GAAP amounts only
- 0001375365-26-000021:8k_2_02:16 heading
- 0001375365-26-000021:8k_2_02:17 amounts only
- 0001375365-26-000021:8k_2_02:18 non-GAAP amounts only
- 0001375365-26-000021:8k_2_02:20 heading
- 0001375365-26-000021:8k_2_02:22 same change as outlook item
- 0001375365-26-000021:8k_2_02:23 heading
- 0001375365-26-000021:8k_2_02:24 call logistics
- 0001375365-26-000021:8k_2_02:25 call logistics
- 0001375365-26-000021:8k_2_02:26 heading
- 0001375365-26-000021:8k_2_02:27 heading
- 0001375365-26-000021:8k_2_02:28 same change as preliminary-release item
- 0001375365-26-000021:8k_2_02:30 heading
- 0001375365-26-000021:8k_2_02:31 boilerplate
- 0001375365-26-000021:8k_2_02:32 trademarks
- 0001375365-26-000021:8k_2_02:33 trademarks
- 0001375365-26-000021:8k_2_02:34 contact
- 0001375365-26-000021:8k_2_02:35 contact
- 0001375365-26-000021:8k_2_02:36 source line
- 0001375365-26-000021:8k_2_02:37 table header
- 0001375365-26-000021:8k_2_02:38 table header
- 0001375365-26-000021:8k_2_02:39 table header
- 0001375365-26-000021:8k_2_02:40 table header
- 0001375365-26-000021:8k_2_02:41 table, amounts only
- 0001375365-26-000021:8k_2_02:42 table header
- 0001375365-26-000021:8k_2_02:43 table header
- 0001375365-26-000021:8k_2_02:44 table header
- 0001375365-26-000021:8k_2_02:45 table header
- 0001375365-26-000021:8k_2_02:46 table; preferred line covered by two-class EPS item
- 0001375365-26-000021:8k_2_02:47 stock-split footnote, carried
- 0001375365-26-000021:8k_2_02:48 lead-in
- 0001375365-26-000021:8k_2_02:49 table, amounts only
- 0001375365-26-000021:8k_2_02:50 table header
- 0001375365-26-000021:8k_2_02:51 table header
- 0001375365-26-000021:8k_2_02:52 table header
- 0001375365-26-000021:8k_2_02:53 table header
- 0001375365-26-000021:8k_2_02:54 table, amounts only
- 0001375365-26-000021:8k_2_02:55 table header
- 0001375365-26-000021:8k_2_02:56 table header
- 0001375365-26-000021:8k_2_02:57 table header
- 0001375365-26-000021:8k_2_02:58 table header
- 0001375365-26-000021:8k_2_02:59 table, amounts only
- 0001375365-26-000021:8k_2_02:60 table header
- 0001375365-26-000021:8k_2_02:61 table header
- 0001375365-26-000021:8k_2_02:62 table header
- 0001375365-26-000021:8k_2_02:63 table header
- 0001375365-26-000021:8k_2_02:64 heading
- 0001375365-26-000021:8k_2_02:65 standard non-GAAP definitions
- 0001375365-26-000021:8k_2_02:66 lead-in
- 0001375365-26-000021:8k_2_02:67 heading
- 0001375365-26-000021:8k_2_02:68 standard definition
- 0001375365-26-000021:8k_2_02:69 standard definition
- 0001375365-26-000021:8k_2_02:70 standard
- 0001375365-26-000021:8k_2_02:71 table header
- 0001375365-26-000021:8k_2_02:72 table header
- 0001375365-26-000021:8k_2_02:73 table header
- 0001375365-26-000021:8k_2_02:74 table header
- 0001375365-26-000021:8k_2_02:75 heading
- 0001375365-26-000021:8k_2_02:76 table, amounts only
- 0001375365-26-000021:8k_2_02:77 heading
- 0001375365-26-000021:8k_2_02:78 table, amounts only
- 0001375365-26-000021:8k_2_02:79 table header
- 0001375365-26-000021:8k_2_02:80 table header
- 0001375365-26-000021:8k_2_02:81 table header
- 0001375365-26-000021:8k_2_02:82 table header
- 0001375365-26-000021:8k_2_02:83 heading
- 0001375365-26-000021:8k_2_02:84 table, amounts only
- 0001375365-26-000021:8k_2_02:85 table header
- 0001375365-26-000021:8k_2_02:86 table header
- 0001375365-26-000021:8k_2_02:87 table header
- 0001375365-26-000021:8k_2_02:88 table header
- 0001375365-26-000021:8k_2_02:89 heading
- 0001375365-26-000021:8k_2_02:90 table; participating-securities lines covered by two-class EPS item
- 0001375365-26-000021:8k_2_02:91 table header
- 0001375365-26-000021:8k_2_02:92 table header
- 0001375365-26-000021:8k_2_02:93 table header
- 0001375365-26-000021:8k_2_02:94 table header
- 0001375365-26-000021:8k_2_02:95 heading
- 0001375365-26-000021:8k_2_02:96 table, amounts only
- 0001375365-26-000021:8k_2_02:97 heading
- 0001375365-26-000021:8k_2_02:98 table, amounts only
