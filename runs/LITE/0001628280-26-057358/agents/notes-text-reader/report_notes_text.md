# LITE 10-K (0001628280-26-057358, FY ended June 27, 2026): notes-text reader report

## Scope and input check

- **Files read in full:**
  - input_notes.md (notes:1–542)
  - input_mdna.md (mdna:1–188)
  - input_controls.md (auditors_report:1–26, item_9a:1–26)
  - input_8k.md (8k_2_02:1–83 plus the item-code list)
  - input_notes_history.md (10-Q of 2026-02-04 → 10-Q of 2026-05-06)
  - input_prior_predictions.md (none on record)
- **Missing from the directory:** the Item 1A diff, the Exhibit 21 diff and any triggered Exhibit 10. No item could come from them.
- **Forbidden material:** none found. There is no trend table, price series, abnormal return, short interest, other company's file, prior probability or outcome window.
- **Comparison base:** the note history covers only Q2→Q3 FY2026. No prior-year 10-K text is in the input. So "new" below means either:
  - new against the Q3 10-Q text in the history, or
  - an event the text itself dates to fiscal 2026.

  Where I cannot tell, the item says so.
- **8-K item-code list:** it shows 5.02 filings on 2026-07-30, 2026-01-05 and 2025-12-15, and 3.02 filings on 2026-06-01, 2026-04-08 and 2026-03-02. None of these has a body in the input. I made no item because I had no text to quote. Insufficient.
- **No arithmetic was done.** Amounts are restated as the prose gives them.

## Items

```json
[
{"id":"controls_audit_and_filings_subsequent_events_note_left_as_placeholder","what_changed":"The filed 10-K's Note 19 Subsequent Events consists of the heading and the word TBD. The Q3 10-Q carried a written subsequent-event note on the April 2026 exchange. Post-year-end conversion requests through August 14, 2026 appear only in Note 10 and MD&A.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"TBD","paragraph_id":"0001628280-26-057358:notes:1","explanation":false},
{"id":"controls_audit_and_filings_goodwill_impairment_heading_without_text","what_changed":"Note 9 carries an 'Impairment of Goodwill' heading followed directly by the 'Other Intangibles' heading, with no text under it. The goodwill conclusion appears only in Note 1 (notes:97).","account":"goodwill","expected_direction":"none","horizon":"this quarter","quote":"Impairment of Goodwill","paragraph_id":"0001628280-26-057358:notes:254","explanation":false},
{"id":"controls_audit_and_filings_revenue_table_reference_without_table","what_changed":"Note 18 introduces a revenue-by-product table that does not follow. The next paragraph is contract-balance policy. The product table sits under a separate concentration tag (notes:526).","account":"net revenue","expected_direction":"none","horizon":"this quarter","quote":"The table below discloses our total net revenue by type of product (in millions, except percentage data):","paragraph_id":"0001628280-26-057358:notes:530","explanation":false},
{"id":"controls_audit_and_filings_accounting_pronouncement_cross_references_mismatched","what_changed":"Several pending-ASU paragraphs name a different ASU in the adoption sentence than in the heading sentence: ASU 2026-02 says it will adopt ASU 2025-12; ASU 2026-01 says 2025-01 (notes:152); ASU 2025-03 says 2025-04 (notes:162); ASU 2024-03 says 2024-04 (notes:163). These are drafting errors in the filed notes.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"We plan to adopt ASU No. 2025-12 in the first quarter of fiscal year 2029.","paragraph_id":"0001628280-26-057358:notes:151","explanation":false},
{"id":"controls_audit_and_filings_single_critical_audit_matter_inventory","what_changed":"Deloitte's report carries one critical audit matter, inventory excess and obsolete valuation. Its procedures include a search for contradictory evidence in board communications, press releases and analyst reports. The opinions on the statements and on ICFR are unqualified, and Item 9A reports no Q4 control changes. No CAM addresses the year's US valuation-allowance release, the equitization loss or the Greensboro business combination. There is no prior-year auditor report in the input, so I cannot say whether the CAM itself changed.","account":"inventories","expected_direction":"none","horizon":"this quarter","quote":"We identified the valuation of inventory as a critical audit matter","paragraph_id":"0001628280-26-057358:auditors_report:14","explanation":false},
{"id":"across_documents_assets_held_for_sale_impairment_amount_and_label","what_changed":"The documents describe these charges differently, and the text does not reconcile them:\n- Note 6 states $12.4 million of impairment charges on assets held for sale.\n- The 8-K footnote (7) describes an impairment charge of $7.7 million to write down assets held for sale.\n- Note 7 (notes:219) and MD&A (mdna:105) describe $7.7 million as a loss on sale of two San Jose buildings, in SG&A.","account":"selling, general and administrative","expected_direction":"none","horizon":"this quarter","quote":"we recorded $12.4 million in impairment charges to write-down certain assets held for sale to fair value less cost to sell","paragraph_id":"0001628280-26-057358:notes:143","explanation":false},
{"id":"across_documents_escrow_settlement_presentation_and_attribution","what_changed":"The new FY2026 Cloud Light escrow settlement of $27.5 million is placed differently across the documents:\n- Note 4 and MD&A (mdna:114) say it was recorded as other income, net.\n- The 8-K statement of operations shows it on a separate 'Escrow settlement' line.\n- Note 5's other-income table lists no escrow component.\n- MD&A (mdna:125) attributes interest and investment income growth partly to the escrow settlement.\n\nThe prose treats it as non-recurring.","account":"other income, net","expected_direction":"down","horizon":"12 months","quote":"we recorded the settlement amount of $27.5 million as other income, net in our consolidated statements of operations for the twelve months ended June 27, 2026","paragraph_id":"0001628280-26-057358:notes:181","explanation":false},
{"id":"across_documents_term_loan_interest_rates_transposed","what_changed":"The MD&A contractual-obligations footnote assigns 0.88% to the SMBC 2026 loan and 1.44% to the SMBC 2029 loan. Note 10 (notes:356, notes:357) assigns 0.88% to the 2029 loan and 1.44% to the 2026 loan.","account":"term loans","expected_direction":"none","horizon":"this quarter","quote":"2026 and 2029 Term Loans with a fixed annual interest rate of 0.88% and 1.44%, respectively","paragraph_id":"0001628280-26-057358:mdna:160","explanation":false},
{"id":"earnings_quality_cloud_light_warranty_and_escrow_net_benefit_removed","what_changed":"The earnings release explains a $9.8 million acquisition-related warranty provision for Cloud Light legacy products, recorded in cost of sales. It nets this against the $27.5 million escrow settlement and removes the net benefit from non-GAAP results. This gives management's stated cause for part of the year's warranty provision.","account":"warranty reserve","expected_direction":"up","horizon":"this quarter","quote":"Therefore, for non-GAAP reporting purposes, we have removed the net benefit of $17.7 million for the twelve months ended June 27, 2026.","paragraph_id":"0001628280-26-055726:8k_2_02:69","explanation":true},
{"id":"estimates_and_discretion_warranty_reserve_growth_attribution_without_footnote","what_changed":"The Q2 and Q3 10-Q warranty rollforwards carried a footnote identifying $9.8 million of Cloud Light legacy-product warranty expense (note_history:3). The 10-K full-year warranty table (notes:498) drops that footnote. The cash-flow prose attributes growth in accrued and other liabilities to contractual liabilities and warranty provisions.","account":"warranty reserve","expected_direction":"up","horizon":"this quarter","quote":"a $43.4 million increase in accrued expenses and other current and non-current liabilities driven by contractual liabilities and provision for warranty reserves","paragraph_id":"0001628280-26-057358:mdna:185","explanation":true},
{"id":"earnings_quality_loss_on_debt_extinguishment_from_note_equitizations","what_changed":"There is a new $7,756.6 million non-cash loss on debt extinguishment under ASC 470-50 from the April and May 2026 privately negotiated note-for-share exchanges. It consists mainly of conversion value in excess of principal. It drives the GAAP net loss and is excluded from non-GAAP results. The note adds that substantially all of the loss is non-deductible for tax.","account":"loss on debt extinguishment","expected_direction":"down","horizon":"this quarter","quote":"For income tax purposes, substantially all of the loss was non-deductible, except for approximately $4.4 million primarily related to the write-off of unamortized debt issuance costs and certain interest-related amounts.","paragraph_id":"0001628280-26-057358:notes:287","explanation":false},
{"id":"liquidity_and_capital_second_exchange_of_notes_for_shares","what_changed":"A May 29, 2026 exchange of about $650.4 million of 2028 Notes for about 5.0 million shares, with about 0.8 million shares of incremental dilution, is new since the Q3 10-Q. The April 7 exchange is now stated as $209.7 million of 2029 Notes; the Q3 10-Q stated $209.8 million.","account":"convertible notes","expected_direction":"down","horizon":"this quarter","quote":"On May 29, 2026, we entered into privately negotiated exchange arrangements with certain holders of our 2028 Notes.","paragraph_id":"0001628280-26-057358:notes:286","explanation":false},
{"id":"liquidity_and_capital_post_year_end_conversion_requests_and_settlement_election","what_changed":"Conversion requests are now stated as $757.8 million of principal as of August 14, 2026. The Q3 10-Q stated $500.8 million as of April 30, 2026. During FY2026, $519.4 million of principal was settled in cash. The Q3 text said the excess conversion value 'will be settled in shares of common stock'. The 10-K says the excess will be settled in cash, shares or a combination at the company's election. No 2032 Note conversion requests have been received (notes:303).","account":"cash and cash equivalents","expected_direction":"down","horizon":"next quarter","quote":"which principal amount will be settled in cash and the conversion value in excess thereof will be settled in cash, shares of common stock, or a combination cash and shares of common stock, at our election","paragraph_id":"0001628280-26-057358:notes:283","explanation":false},
{"id":"liquidity_and_capital_all_convertible_notes_classified_current_at_year_end","what_changed":"At fiscal year-end all four note series, including the 2032 Notes, are presented as current portion of long-term debt because they remain convertible through Q1 FY2027. The June 28, 2025 balances were long-term.","account":"current portion of long-term debt","expected_direction":"up","horizon":"next quarter","quote":"all of our Notes remain convertible at the option of the holders during the first quarter of fiscal year 2027","paragraph_id":"0001628280-26-057358:notes:273","explanation":false},
{"id":"liquidity_and_capital_going_concern_doubt_language_absent","what_changed":"The Q2 10-Q said holders' ability to convert raised substantial doubt about going concern. That paragraph was removed in Q3 and does not return in the 10-K. MD&A (mdna:166) now states that cash and operating cash flows are sufficient for at least 12 months. The auditor's report has no going-concern paragraph.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"raises a substantial doubt that we could continue as a going concern","paragraph_id":"0001628280-26-005129:note_history:16","explanation":false},
{"id":"liquidity_and_capital_fourth_quarter_cash_decrease_stated","what_changed":"The earnings release states that cash, cash equivalents and short-term investments decreased from the end of Q3. MD&A financing prose (mdna:187) lists $520.0 million of payments for Notes conversions and $281.0 million of tax payments on net share settlement.","account":"cash and cash equivalents","expected_direction":"down","horizon":"next quarter","quote":"a decrease of $433.9 million from the end of the third quarter of fiscal year 2026","paragraph_id":"0001628280-26-055726:8k_2_02:16","explanation":false},
{"id":"liquidity_and_capital_capped_call_counterparty_exposure","what_changed":"There is a new counterparty-credit disclosure on the 2032 capped calls: no asset is recognized, the exposure is unsecured, and the capped payout is stated. Note 6 (notes:207) adds that the capped calls' fair value is about $200.0 million.","account":"additional paid-in capital","expected_direction":"none","horizon":"12 months","quote":"our exposure is limited to the capped payout on the 2032 Capped Call Options, which is approximately $542.0 million when our stock price is above $268.24 per share","paragraph_id":"0001628280-26-057358:notes:117","explanation":false},
{"id":"estimates_and_discretion_capped_call_deferred_tax_asset_credited_to_equity","what_changed":"The Q3 10-Q carried a $24.4 million capped-call deferred tax asset with a full valuation allowance and a $2.0 million current tax impact. At year end, after the US valuation-allowance release, the deferred tax asset is recognized and $25.0 million is credited to additional paid-in capital.","account":"additional paid-in capital","expected_direction":"up","horizon":"this quarter","quote":"the corresponding $25.0 million deferred tax benefit was recorded as an increase to additional paid-in capital","paragraph_id":"0001628280-26-057358:notes:307","explanation":false},
{"id":"estimates_and_discretion_us_valuation_allowance_release_excluding_extinguishment_loss","what_changed":"In Q4 the company released $236.3 million of valuation allowance on most US federal and state deferred tax assets, although it states a three-year cumulative US loss. Management explains the release this way:\n- It built an objectively verifiable income estimate that excludes the $7,756.6 million extinguishment loss.\n- It cites existing contracts and firm backlog as positive evidence.\n- It keeps an $81.4 million valuation allowance on federal foreign tax credit and California R&D credit carryforwards.\n\nAt Q3 the text said US deferred tax assets were not more likely than not realizable (note_history:35).","account":"deferred tax asset valuation allowance","expected_direction":"down","horizon":"this quarter","quote":"we developed an objectively verifiable estimate of future taxable income based upon our recent U.S. operating results which excluded the loss on debt extinguishment","paragraph_id":"0001628280-26-057358:mdna:60","explanation":true},
{"id":"estimates_and_discretion_goodwill_reporting_unit_reorganization_qualitative_only","what_changed":"A Q3 FY2026 business-unit reorganization changed the reporting units. Goodwill was assessed only qualitatively, at an interim date in Q3 and in the annual Q4 test. No quantitative test was run and no impairment was recorded.","account":"goodwill","expected_direction":"none","horizon":"12 months","quote":"During the third quarter of fiscal year 2026, we completed a reorganization of our business units, which resulted in changes to our reporting unit structure.","paragraph_id":"0001628280-26-057358:notes:97","explanation":false},
{"id":"structure_and_disclosure_changes_single_reportable_segment","what_changed":"The two former segments, Cloud & Networking and Industrial Tech, are replaced by one segment from Q1 FY2026. The CODM uses consolidated net (loss) income, and prior periods are recast.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"Accordingly, following the reorganization, we determined we operate in a single reporting segment.","paragraph_id":"0001628280-26-057358:notes:24","explanation":false},
{"id":"structure_and_disclosure_changes_components_systems_product_disaggregation","what_changed":"Revenue is now disaggregated into Components and Systems, with new definitions. Systems includes optical modules, optical circuit switches and industrial lasers. This replaces segment-based disaggregation.","account":"net revenue","expected_direction":"none","horizon":"this quarter","quote":"We disaggregate revenue by type of product, which are Components and Systems, and by geography.","paragraph_id":"0001628280-26-057358:notes:19","explanation":false},
{"id":"structure_and_disclosure_changes_two_class_earnings_per_share","what_changed":"Basic EPS now uses the two-class method because of the March 2026 Series A Convertible Preferred Stock. Preferred shares are included in weighted shares on an as-converted basis.","account":"weighted average shares","expected_direction":"up","horizon":"next quarter","quote":"We calculate basic net (loss) income per share pursuant to the two-class method as a result of the issuance of the Series A Convertible Preferred Stock","paragraph_id":"0001628280-26-057358:notes:43","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_nvidia_preferred_investment","what_changed":"On March 2, 2026 about 2.9 million Series A Convertible Preferred shares were sold to NVIDIA. They convert one-for-one after HSR clearance and vote with common except on directors. The input does not say whether NVIDIA is also a customer: Customers A and B are unnamed, and no related-party note is present.","account":"stockholders' equity","expected_direction":"up","horizon":"this quarter","quote":"The shares of Preferred Stock were sold at a price of $695.31 per share for an aggregate purchase price of $2.0 billion in cash.","paragraph_id":"0001628280-26-057358:notes:416","explanation":false},
{"id":"revenue_recognition_greensboro_supply_agreement_net_agent_basis","what_changed":"On March 17, 2026 the company bought a Greensboro, NC fab for $38.0 million and accounted for it as a business combination (PP&E $39.5 million, goodwill $8.4 million, preliminary allocation). The deal includes a transitional supply agreement of about 15 months under which the company is agent, and that revenue is recognized net.","account":"net revenue","expected_direction":"none","horizon":"12 months","quote":"Accordingly, revenue is recognized on a net basis, representing the amount of consideration or reasonable margin to which we expect to be entitled","paragraph_id":"0001628280-26-057358:notes:175","explanation":false},
{"id":"estimates_and_discretion_below_market_contract_liability_amount_restated","what_changed":"The Q3 10-Q stated a $6.9 million below-market contract liability, split between current and non-current. The 10-K states $9.9 million, with $2.3 million amortized to revenue and the $7.6 million remainder all current. No reason is given for the different amount; the allocation is still called preliminary (notes:176).","account":"deferred revenue and customer deposits","expected_direction":"up","horizon":"12 months","quote":"We recorded a $9.9 million below-market contract liability related to our acquisition of a business in March 2026","paragraph_id":"0001628280-26-057358:notes:534","explanation":false},
{"id":"revenue_recognition_tariff_charges_billed_recorded_as_revenue","what_changed":"The policy now groups tariffs with shipping and handling: tariffs paid go to cost of sales, and tariff charges billed to customers go to revenue. There is no prior-year policy text in the input to date this wording.","account":"net revenue","expected_direction":"up","horizon":"12 months","quote":"Amounts billed to the customer for shipping and handling costs, including tariff charges, is recorded as revenue when the relevant product is recognized as revenue.","paragraph_id":"0001628280-26-057358:notes:74","explanation":false},
{"id":"estimates_and_discretion_tariff_assessment_trade_restriction_wording_dropped","what_changed":"The Q3 10-Q referred to 'trade restrictions and tariff regulations' and 'import tariffs and other trade restrictions'. The 10-K drops 'trade restrictions' from both phrases. It still concludes there was no material impact on credit losses, goodwill, long-lived assets, inventory or revenue.","account":"none","expected_direction":"none","horizon":"12 months","quote":"particularly with respect to recent changes in tariff regulations","paragraph_id":"0001628280-26-057358:notes:26","explanation":false},
{"id":"narrative_signs_of_operating_pressure_rare_earth_trade_restrictions","what_changed":"The macro paragraph names trade restrictions on certain rare earth minerals among the adverse factors. This does not appear in the change history and there is no prior-year text, so I cannot date when it was added.","account":"cost of sales","expected_direction":"up","horizon":"12 months","quote":"trade restrictions including for certain rare earth minerals","paragraph_id":"0001628280-26-057358:notes:25","explanation":false},
{"id":"structure_and_disclosure_changes_fifty_three_week_fiscal_year_ahead","what_changed":"Fiscal 2027 is a 53-week year, and the extra week falls in the third quarter, which will have 14 weeks. Fiscal 2026 was 52 weeks.","account":"net revenue","expected_direction":"up","horizon":"12 months","quote":"Our fiscal year 2027 ending on July 3, 2027 has a 53-week period.","paragraph_id":"0001628280-26-057358:notes:28","explanation":false},
{"id":"narrative_signs_of_operating_pressure_demand_outpacing_supply_allocation","what_changed":"MD&A says demand exceeds supply and requires allocation decisions. It also says the company is investing in capacity internally and with contract manufacturers.","account":"property, plant and equipment","expected_direction":"up","horizon":"12 months","quote":"This demand is outpacing our current supply which has required us to make decisions on supply allocation.","paragraph_id":"0001628280-26-057358:mdna:14","explanation":false},
{"id":"results_against_expectations_next_quarter_revenue_guidance","what_changed":"Q1 FY2027 guidance:\n- revenue of $1.225 to $1.275 billion\n- non-GAAP operating margin of 39.5% to 40.5%\n- non-GAAP EPS of $4.05 to $4.35\n\nThe CEO adds that the company is 'reaching our target model more than a quarter ahead of schedule' (8k_2_02:12).","account":"net revenue","expected_direction":"up","horizon":"next quarter","quote":"Forecasting first quarter of fiscal year 2027 revenue of $1.225 billion to $1.275 billion","paragraph_id":"0001628280-26-055726:8k_2_02:9","explanation":false},
{"id":"results_against_expectations_components_growth_laser_chip_pricing","what_changed":"Management attributes Components growth mostly to laser chip and assembly shipments. The prose says laser chip average selling prices rose slightly on the shift to 200G lanes, and that data transport products account for the rest of the growth.","account":"net revenue","expected_direction":"up","horizon":"this quarter","quote":"complemented by a slight increase in average selling prices of laser chip products driven primarily by a shift to 200G lane speeds","paragraph_id":"0001628280-26-057358:mdna:88","explanation":false},
{"id":"narrative_signs_of_operating_pressure_transceiver_lower_selling_prices","what_changed":"Management attributes Systems growth to higher cloud transceiver volume, partly offset by lower average selling prices. Optical circuit switch revenue is stated as more than $90.0 million in its initial phase.","account":"net revenue","expected_direction":"none","horizon":"12 months","quote":"our cloud transceiver product lines which increased by more than 173% due to an increase in shipment volume, partially offset by lower average selling prices","paragraph_id":"0001628280-26-057358:mdna:89","explanation":false},
{"id":"earnings_quality_gross_margin_attributed_to_factory_utilization","what_changed":"MD&A gives a percentage attribution of gross margin improvement: factory utilization, product mix, and lower amortization. A margin driven by utilization depends on continued volume.","account":"cost of sales","expected_direction":"none","horizon":"12 months","quote":"Approximately 54% of the gross margin dollar increase was driven by lower manufacturing costs as a percentage of revenue, primarily due to higher internal factory utilization.","paragraph_id":"0001628280-26-057358:mdna:99","explanation":false},
{"id":"narrative_signs_of_operating_pressure_gross_margin_downward_pressure_warning","what_changed":"Management warns of increasing downward pressure on gross margin. It cites AI-driven architecture transitions, high customer concentration, price sensitivity and seasonality. There is no prior text in the input to show whether this wording is new.","account":"gross margin","expected_direction":"down","horizon":"12 months","quote":"our gross margin may be subject to increasing downward pressure due to these factors","paragraph_id":"0001628280-26-057358:mdna:100","explanation":false},
{"id":"earnings_quality_incentive_compensation_shift_from_equity_to_cash","what_changed":"The FY2026 annual incentive is cash-based; the FY2025 plan was mostly equity. R&D and SG&A rose with cash incentives and with payroll taxes on equity, while stock-based compensation fell (mdna:102, mdna:105). Accrued payroll is attributed to cash bonuses and payroll taxes (mdna:185). Non-GAAP results exclude stock compensation but keep the cash bonus.","account":"accrued payroll and related expenses","expected_direction":"up","horizon":"12 months","quote":"whereas the fiscal year 2025 annual incentive plan was mostly equity-based","paragraph_id":"0001628280-26-057358:mdna:102","explanation":false},
{"id":"estimates_and_discretion_bad_debt_expense_reduction_with_flat_allowance","what_changed":"Management cites lower bad debt expense among the SG&A drivers. Note 7 states the allowance for credit losses at $3.5 million at both year ends (notes:210), and Schedule II shows a $0.1 million provision for FY2026. The text also states the largest customer was 30% of gross receivables at June 27, 2026 and 13% at June 28, 2025.","account":"allowance for credit losses","expected_direction":"none","horizon":"this quarter","quote":"a $3.2 million reductions in bad debt expense","paragraph_id":"0001628280-26-057358:mdna:105","explanation":true},
{"id":"revenue_recognition_receivable_concentration_largest_customer","what_changed":"Receivable concentration is now stated at 30% and 11% for two customers; the prior year-end text says 13% and 11%. Revenue concentration for Customer A is stated at 26.6% for FY2026 and 15.4% for FY2025 (mdna:91, notes:519).","account":"accounts receivable, net","expected_direction":"none","horizon":"this quarter","quote":"was concentrated with two customers, which represented 30% and 11% of gross accounts receivable, respectively","paragraph_id":"0001628280-26-057358:notes:114","explanation":false},
{"id":"liquidity_and_capital_receivables_and_inventory_growth_explained","what_changed":"Management attributes the receivables increase to higher revenue and the inventory increase to builds for market demand.","account":"accounts receivable and inventories","expected_direction":"up","horizon":"this quarter","quote":"offset by a $270.4 million increase in accounts receivable mainly driven by higher revenue, a $228.4 million increase in inventories driven by builds to support market demand","paragraph_id":"0001628280-26-057358:mdna:185","explanation":true},
{"id":"liquidity_and_capital_contract_manufacturer_receivables_and_prepayments","what_changed":"The prepayments increase is explained as VAT receivables tied to capex and inventory purchases ($45.3 million), inventory-related prepayments ($24.0 million) and receivables from contract manufacturers.","account":"prepayments and other current assets","expected_direction":"up","horizon":"this quarter","quote":"a $13.2 million increase in receivables from our contract manufacturers driven by increase manufacturing volume","paragraph_id":"0001628280-26-057358:mdna:185","explanation":true},
{"id":"related_parties_contingencies_and_subsequent_events_purchase_obligations_cancellation_wording","what_changed":"Purchase obligations are stated at $2.4 billion; the Q3 10-Q stated $1,795.6 million. The cancellation wording changed from 'the terms generally allow' to 'the terms may allow' the option to cancel. The note still says obligations are generally fulfilled within one year, while the MD&A table (mdna:156) shows an amount due after one year.","account":"purchase commitments","expected_direction":"up","horizon":"12 months","quote":"the terms may allow the option to cancel, reschedule and adjust the requirements based on our business needs","paragraph_id":"0001628280-26-057358:notes:493","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_non_ordinary_course_legal_fees","what_changed":"The earnings release discloses $9.6 million of legal fees for non-ordinary course legal matters, excluded from non-GAAP results. The 10-K does not identify these matters. Note 16 repeats the BIS/DOJ inquiry (outcome unpredictable) and says the litigation accrual is not material.","account":"selling, general and administrative","expected_direction":"none","horizon":"12 months","quote":"mainly includes legal fees of $9.6 million primarily related to non-ordinary course legal matters","paragraph_id":"0001628280-26-055726:8k_2_02:74","explanation":false},
{"id":"earnings_quality_non_gaap_diluted_shares_reduced_for_capped_call","what_changed":"Non-GAAP diluted shares are reduced for the 2032 capped call. Under GAAP the capped call is treated as anti-dilutive and excluded (notes:172).","account":"non-GAAP diluted shares","expected_direction":"down","horizon":"next quarter","quote":"we reduced 0.6 million and 0.8 million shares from the capped call in the calculation of non-GAAP diluted shares","paragraph_id":"0001628280-26-055726:8k_2_02:75","explanation":false},
{"id":"earnings_quality_non_gaap_exclusion_list_expanded_for_year_events","what_changed":"The non-GAAP exclusion list names categories tied to FY2026 events: acquisition-related warranty provision, escrow settlement, loss on debt extinguishment, inducement expense and non-cash interest. There is no prior release text in the input to compare the list against.","account":"non-GAAP net income","expected_direction":"none","horizon":"this quarter","quote":"(ii) acquisition-related warranty provision, (iii) escrow settlement","paragraph_id":"0001628280-26-055726:8k_2_02:58","explanation":false},
{"id":"earnings_quality_inducement_expense_on_partial_note_repurchase","what_changed":"In September 2025 the company repurchased $581.1 million of 2026 Notes for $843.1 million. This was treated as an induced conversion under early-adopted ASU 2024-04, with $256.9 million charged to APIC and $5.9 million to expense.","account":"other income, net","expected_direction":"none","horizon":"this quarter","quote":"recognized an inducement expense of $5.9 million in our consolidated statements of operations during the year ended June 27, 2026","paragraph_id":"0001628280-26-057358:notes:289","explanation":false},
{"id":"structure_and_disclosure_changes_brazilian_entities_sold","what_changed":"The Brazilian entities (from the IPG product lines) were sold in FY2026. Their cumulative translation adjustment was recycled to earnings, and a gain of about $1.6 million was recorded in SG&A (notes:220).","account":"selling, general and administrative","expected_direction":"none","horizon":"this quarter","quote":"In fiscal year 2026, we sold our Brazilian entities, and therefore, recognized the related accumulated translation adjustments to earnings.","paragraph_id":"0001628280-26-057358:notes:119","explanation":false},
{"id":"structure_and_disclosure_changes_san_jose_properties_sold_with_rent_back","what_changed":"Two San Jose buildings were sold in March 2026 for $43.0 million, with a short-term rent-back through July 2026. A $7.7 million loss on sale was recorded in SG&A.","account":"property, plant and equipment","expected_direction":"none","horizon":"this quarter","quote":"included a short-term rental arrangement under which we occupied the properties through July 2026","paragraph_id":"0001628280-26-057358:notes:219","explanation":false},
{"id":"earnings_quality_construction_in_progress_into_service_within_year","what_changed":"The note says construction in progress is expected to be placed in service within 12 months. That would start depreciation on those assets.","account":"depreciation expense","expected_direction":"up","horizon":"12 months","quote":"Our construction in progress primarily includes building and improvements and machinery and equipment that we expect to place in service in the next 12 months.","paragraph_id":"0001628280-26-057358:notes:217","explanation":false},
{"id":"earnings_quality_iprd_write_off_from_neophotonics","what_changed":"FY2026 includes a $2.5 million write-off, charged to R&D, of a NeoPhotonics IPR&D project that will no longer be pursued.","account":"research and development","expected_direction":"none","horizon":"this quarter","quote":"we recorded a $2.5 million write-off of IPR&D intangible asset for project we will no longer pursue","paragraph_id":"0001628280-26-057358:notes:261","explanation":false},
{"id":"narrative_signs_of_operating_pressure_reduction_in_force","what_changed":"FY2026 restructuring of $11.4 million is attributed to reductions in force to improve efficiency and realign investment. This is new prose for the year.","account":"restructuring and related charges","expected_direction":"none","horizon":"this quarter","quote":"primarily related to reduction in forces during the period in order to enhance operational efficiency and realign our investments toward the most critical initiatives","paragraph_id":"0001628280-26-057358:notes:381","explanation":false},
{"id":"estimates_and_discretion_research_expensing_tax_law_change","what_changed":"The OBBBA, enacted in July 2025, ends capitalization of domestic R&D and permits accelerated deduction of previously capitalized amounts. Its impact is included in the FY2026 provision.","account":"income taxes payable","expected_direction":"down","horizon":"12 months","quote":"We have evaluated these changes and included their impact in our tax provision for fiscal year 2026.","paragraph_id":"0001628280-26-057358:mdna:140","explanation":false},
{"id":"earnings_quality_china_tax_incentives_expired","what_changed":"The China tax incentives have now expired. The FY2026 benefit is stated as $0.0.","account":"income tax provision","expected_direction":"up","horizon":"12 months","quote":"have expired at various dates through calendar year 2025","paragraph_id":"0001628280-26-057358:notes:404","explanation":false},
{"id":"estimates_and_discretion_thailand_investment_board_exemption_conclusion","what_changed":"In FY2026 management concluded that the Thailand BOI exemption requirements were met: two projects for FY2025 and three for FY2026. This is a judgment reaching back to the prior year.","account":"income tax provision","expected_direction":"down","horizon":"this quarter","quote":"we concluded that we satisfied the substantive requirements to qualify for exemptions relating to two BOI-promoted projects for fiscal year 2025, and three BOI-promoted projects for fiscal year 2026","paragraph_id":"0001628280-26-057358:notes:405","explanation":false},
{"id":"structure_and_disclosure_changes_income_tax_disclosure_standard_prospective","what_changed":"ASU 2023-09 was adopted prospectively. FY2026 uses the new rate-reconciliation format and a cash-taxes-paid table; FY2025 and FY2024 are shown in the old format (notes:392 to notes:395, notes:413).","account":"income tax provision","expected_direction":"none","horizon":"this quarter","quote":"We have adopted ASU No. 2023-09 in fiscal year 2026 on a prospective basis.","paragraph_id":"0001628280-26-057358:notes:149","explanation":false},
{"id":"estimates_and_discretion_repatriation_assertion_scope","what_changed":"insufficient: The text states an intent to repatriate from the Cayman Islands, BVI, Hong Kong and certain China and Japan subsidiaries, and to indefinitely reinvest elsewhere ($44.1 million of undistributed earnings). There is no prior-year text in the input to tell whether the scope changed.","account":"income tax provision","expected_direction":"none","horizon":"12 months","quote":"We intend to repatriate all or a portion of the earnings of our subsidiaries in the Cayman Islands, the British Virgin Islands and Hong Kong","paragraph_id":"0001628280-26-057358:notes:406","explanation":false,"insufficient":true},
{"id":"liquidity_and_capital_smbc_covenant_compliance_stated","what_changed":"The Q3 10-Q said 'We are expected to maintain' the 1.2 debt-service coverage ratio and the USD deposit. The 10-K states both were maintained for FY2026.","account":"term loans","expected_direction":"none","horizon":"this quarter","quote":"We have maintained a debt service coverage ratio of at least 1.2 for our Japan entity for fiscal year 2026","paragraph_id":"0001628280-26-057358:notes:358","explanation":false},
{"id":"structure_and_disclosure_changes_new_equity_incentive_plan","what_changed":"Stockholders approved the 2025 Equity Incentive Plan in November 2025, with 3.2 million shares plus recycled Prior Plan shares. The 2015 Plan and the Cloud Light Scheme closed to new grants.","account":"stock-based compensation","expected_direction":"none","horizon":"12 months","quote":"In November 2025, our stockholders approved the 2025 Equity Incentive Plan","paragraph_id":"0001628280-26-057358:notes:427","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_executive_trading_plan_changes","what_changed":"In Q4 the CFO and the President of Global Business Units modified Rule 10b5-1 plans first adopted in November 2025. The CEO adopted a new plan (notes:535, notes:537).","account":"none","expected_direction":"none","horizon":"12 months","quote":"adopted a modification of his Rule 10b5-1 trading arrangement entered into on November 28, 2025","paragraph_id":"0001628280-26-057358:notes:536","explanation":false}
]
```

## Paragraphs not made into an item

Format: `section:number` stands for `0001628280-26-057358:section:number`. `8k:number` stands for `0001628280-26-055726:8k_2_02:number`. Each line lists the paragraphs and the reason.

### 8-K (0001628280-26-055726)
- 8k:1, 2, 3, 4, 5 — exhibit wrapper and headings
- 8k:6, 7, 8 — highlight bullets, amounts only
- 8k:10 — dateline
- 8k:11 — CEO promotional narrative, no accounting content
- 8k:12 — covered by results_against_expectations_next_quarter_revenue_guidance
- 8k:13, 17, 21, 24, 29, 35, 37, 39 — headings
- 8k:14, 18, 50, 72 — duplicate of earnings_quality_loss_on_debt_extinguishment_from_note_equitizations
- 8k:15, 19, 20 — amounts only
- 8k:22, 23, 25, 26, 27 — results tables, amounts only
- 8k:28, 34, 57, 60 — non-GAAP boilerplate
- 8k:30, 31, 32, 33 — guidance bullets, covered by the guidance item
- 8k:36 — call logistics
- 8k:38 — company description, wording only
- 8k:40, 41, 42, 43 — contacts and category
- 8k:44, 45, 46, 47, 48, 51, 52, 53, 54, 56, 61, 62, 63, 64, 79, 80, 81, 82 — table headers
- 8k:49, 55, 65, 66, 67, 83 — financial tables, amounts only
- 8k:59 — non-GAAP tax rate stated; no prior text in input to show a change
- 8k:68, 70 — footnote amounts only
- 8k:71 — duplicate of narrative_signs_of_operating_pressure_reduction_in_force
- 8k:73 — duplicate of earnings_quality_inducement_expense_on_partial_note_repurchase
- 8k:76, 77, 78 — duplicate of structure_and_disclosure_changes_two_class_earnings_per_share

### Auditor's report
- auditors_report:1, 2, 3, 6, 9, 11, 12, 16, 26 — headings
- auditors_report:4, 7, 8, 10 — standard opinion and CAM boilerplate
- auditors_report:5 — ICFR cross-reference, date rolled forward
- auditors_report:13, 17, 18, 19, 20, 21 — CAM description and procedures, covered by the CAM item
- auditors_report:15 — page number
- auditors_report:22, 23, 24 — signature, city, date
- auditors_report:25 — auditor tenure, rolled forward

### Item 9A
- item_9a:1, 2, 4, 7, 9, 12, 13, 14, 17, 20 — headings
- item_9a:3, 5 — effective-controls conclusion, standard wording
- item_9a:6, 16 — cross-references
- item_9a:8 — no-change statement, standard wording
- item_9a:10, 18, 19, 21, 22 — limitations and basis boilerplate
- item_9a:11, 26 — page numbers
- item_9a:15 — unqualified ICFR opinion, standard wording (noted in the CAM item)
- item_9a:23, 24, 25 — signature, city, date

### MD&A
- mdna:1, 3, 10, 13, 18, 25, 29, 41, 43, 46, 48, 50, 54, 56, 65, 71, 76, 78, 83, 86, 92, 98, 101, 104, 107, 111, 113, 115, 117, 122, 126, 131, 135, 136, 141, 154, 163, 165, 182, 183 — headings
- mdna:2, 19 — boilerplate
- mdna:4, 5, 6, 9 — business description, wording only
- mdna:7, 8 — duplicate of the components/systems item
- mdna:11, 12 — duplicate of the single-segment item
- mdna:15 — standing supply-chain risk text
- mdna:16, 97 — standing trade-risk text
- mdna:17, 55, 77, 110, 159 — cross-references
- mdna:20, 21, 22, 23, 24 — list of critical policies
- mdna:26, 27, 28 — inventory policy; no change shown
- mdna:30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42 — revenue policy, duplicate of notes text
- mdna:44, 45 — warranty policy
- mdna:47 — duplicate of revenue_recognition_tariff_charges_billed_recorded_as_revenue
- mdna:49, 51 — contract policy
- mdna:52, 53 — contract-balance table, amounts only
- mdna:57, 58, 59, 62, 63, 64 — tax policy
- mdna:61 — FY2025 UK release, carried from prior year
- mdna:66, 67, 68, 69, 70 — business-combination policy
- mdna:72, 73, 74, 75 — goodwill and intangibles policy
- mdna:79 — period rolled forward
- mdna:80, 81, 82, 84, 85 — tables and page number
- mdna:87 — revenue change, amounts only
- mdna:90, 91 — customer concentration, covered by the receivable-concentration item
- mdna:93 — geography wording
- mdna:94, 95, 96 — geography table and amounts
- mdna:103, 106, 108 — standing wording
- mdna:109 — duplicate of the reduction-in-force item
- mdna:112 — FY2025 Shenzhen sale, carried
- mdna:114, 125 — covered by across_documents_escrow_settlement_presentation_and_attribution
- mdna:116 — duplicate of the debt-extinguishment loss item
- mdna:118, 119, 123, 124, 127 — tables
- mdna:120, 121 — interest expense; amounts and drivers covered by the debt items
- mdna:128 — duplicate of the tax-rate explanation (notes:396)
- mdna:129, 130 — standing tax wording
- mdna:132, 133, 134 — pension amounts
- mdna:137, 138 — cash location amounts
- mdna:139 — covered by estimates_and_discretion_repatriation_assertion_scope
- mdna:142, 143, 144, 145 — note fair-value and conversion-price tables
- mdna:146 — duplicate of the current-classification item
- mdna:147 — duplicate of the conversion-requests item
- mdna:148, 149 — duplicates of the exchange item
- mdna:150, 151, 152 — term loan table, amounts only
- mdna:153 — revolver unchanged, no borrowings
- mdna:155, 156 — contractual-obligations table, covered by the purchase-obligations item
- mdna:157, 158 — sublease and pension footnotes
- mdna:161, 162 — standing wording
- mdna:164 — unrecognized tax benefit amount only
- mdna:166 — covered by liquidity_and_capital_going_concern_doubt_language_absent
- mdna:167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181 — standing list of liquidity factors
- mdna:184, 186, 187 — cash flow amounts only
- mdna:188 — page number

### Notes: 1 to 260
- notes:2 — incorporation-by-reference boilerplate
- notes:3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 — cybersecurity governance; no change shown in input
- notes:16, 17, 22, 27, 29, 31, 33, 35, 37, 40, 42, 48, 50, 55, 67, 70, 73, 75, 77, 79, 81, 88, 93, 98, 100, 103, 108, 118, 121, 127, 131, 133, 135, 141 — headings
- notes:18 — duplicate of the single-segment item
- notes:20 — duplicate of the components/systems item
- notes:21, 30 — wording only
- notes:23, 34 — list of critical policies
- notes:32 — duplicate of the Greensboro item
- notes:36 — cash-equivalent composition prose; table figures left to the numbers reader
- notes:38, 39, 41, 46, 47, 49, 51, 52, 53, 54 — policy text; no change shown
- notes:44 — duplicate of the two-class item
- notes:45 — dilutive-share policy, standing
- notes:56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 71, 72, 76, 78, 80 — revenue, warranty and contract policy; no change shown
- notes:69 — deferred revenue amounts, covered by the below-market contract item
- notes:82, 83, 84, 85, 86, 87 — tax policy
- notes:89, 90, 91, 92 — PP&E and business-combination policy
- notes:94, 95, 96 — goodwill policy
- notes:99, 101, 102 — intangibles and long-lived assets policy
- notes:104, 105, 106, 107 — pension policy
- notes:109, 110, 111, 112 — credit-risk policy
- notes:113 — covered by the receivable-concentration item
- notes:115, 116 — standing supplier text
- notes:120 — foreign-currency policy
- notes:122, 123, 124, 125, 126, 128, 129, 132, 134, 136 — policy text
- notes:130 — cross-reference
- notes:137, 138, 139, 140, 142 — fair-value policy
- notes:144 — duplicate contract-balance policy
- notes:145, 146, 150 — headings
- notes:147 — covered by the inducement item
- notes:148 — standard adopted, no impact
- notes:152, 162, 163 — named in the mismatched-ASU-references item
- notes:153, 154, 155, 156, 157, 158, 159, 160, 161 — pending standards, under evaluation
- notes:164, 166, 170 — heading and table introductions
- notes:165 — duplicate of the two-class item
- notes:167, 171 — EPS tables
- notes:168, 169 — EPS policy
- notes:172 — covered by the non-GAAP capped-call share item
- notes:173, 174 — headings
- notes:176, 179 — Greensboro allocation detail, covered by the Greensboro and below-market items
- notes:177 — allocation table
- notes:178 — covered by the below-market contract item
- notes:180 — acquisition costs, amounts only
- notes:182, 183, 187, 190, 193 — heading and table introductions
- notes:184, 188, 191, 194 — investment tables
- notes:185, 186, 195 — investment policy
- notes:189, 192 — amounts only
- notes:196, 197, 202, 204 — heading and table introductions
- notes:198, 200, 205 — fair-value tables
- notes:199, 201, 206 — amounts only
- notes:203 — fair-value method, standing
- notes:207 — covered by the capped-call counterparty item
- notes:208, 209, 211, 212, 214, 215, 224, 225, 229, 230, 236, 237 — heading and table introductions
- notes:210 — covered by the bad-debt allowance item
- notes:213, 216, 226, 231, 238 — balance tables
- notes:218 — duplicate of the Greensboro item
- notes:220 — covered by the Brazilian-entities item
- notes:221, 222, 227, 228, 240 — prior-year events, carried
- notes:223, 239 — amounts only
- notes:232, 233, 234, 235 — cross-references
- notes:241, 244, 246 — heading and table introductions
- notes:242, 243 — lease policy and sublease locations
- notes:245, 247 — lease tables
- notes:248 — amounts only
- notes:249, 250, 255, 259 — heading and table introductions
- notes:251, 260 — goodwill and intangibles tables
- notes:252 — FY2025 Cloud Light goodwill adjustment, carried
- notes:253 — duplicate of the Greensboro item
- notes:256, 257, 258 — intangibles policy

### Notes: 262 to 542
- notes:262, 267, 269 — intangibles tables
- notes:263, 264 — prior-year events, carried
- notes:265 — amounts only
- notes:266, 268 — table introductions
- notes:270, 271, 274, 276, 282, 284, 288, 290, 291, 304, 308, 320, 333, 346, 349, 351, 354, 355, 360, 364 — heading and table introductions
- notes:272, 275, 277, 347, 348, 350, 352 — debt tables
- notes:278, 279, 280, 281, 319, 345 — cross-references
- notes:285 — April exchange, covered by liquidity_and_capital_second_exchange_of_notes_for_shares
- notes:292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302 — 2032 Note terms; wording only versus Q3
- notes:303 — covered by the conversion-requests item
- notes:305, 306 — capped call terms; the dropped tax-impact amount is covered by the capped-call deferred-tax item
- notes:309, 310, 311, 312, 313, 314, 315, 316, 317, 318 — 2029 Note terms, standing
- notes:321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332 — 2028 Note terms, standing
- notes:334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344 — 2026 Note terms, standing
- notes:353 — standing wording
- notes:356, 357, 361 — term loan terms unchanged since Q3
- notes:359, 362, 370 — amounts only
- notes:363 — definition
- notes:365, 366, 367, 368, 369 — revolver terms; no change shown
- notes:371, 373 — heading and table introduction
- notes:372 — AOCI policy
- notes:374 — AOCI table
- notes:375 — duplicate of the Brazilian-entities item
- notes:376 — amounts only
- notes:377, 379 — heading and table introduction
- notes:378, 384, 385 — standing restructuring wording
- notes:380 — restructuring table
- notes:382, 383 — prior-year restructuring, carried
- notes:386, 387, 389, 391, 394, 399, 407, 412 — heading and table introductions
- notes:388, 390, 392, 395, 400, 408, 413 — tax tables; the format change is covered by the ASU 2023-09 item
- notes:393 — state detail under ASU 2023-09
- notes:396 — duplicate of the tax-rate explanation
- notes:397, 398 — prior-year rate explanations, carried
- notes:401, 402 — covered by the US valuation-allowance release item
- notes:403, 409, 410 — tax amounts only
- notes:411 — open tax years rolled forward
- notes:414, 415, 422, 423, 429, 431, 434, 438, 440, 441, 443, 448, 450, 452, 453, 455, 457, 459 — heading and table introductions
- notes:417, 418, 419, 420, 421 — preferred stock terms, covered by the NVIDIA preferred item
- notes:424, 425, 426 — plan history, carried
- notes:428, 433, 436, 439, 447, 458 — equity amounts only
- notes:430, 432, 435, 445 — equity award policy
- notes:437 — covered by the incentive-compensation item
- notes:442, 444, 449, 451, 454, 456, 460 — equity tables
- notes:446 — FY2025 modification, carried
- notes:461, 462, 465, 469, 473, 475, 479, 481, 482, 486, 488 — heading and table introductions
- notes:463, 464, 467, 472, 490 — pension and retirement amounts; limits rolled forward
- notes:466, 468, 476, 477, 478, 485, 487 — pension policy
- notes:470, 474, 480, 483, 484, 489 — pension tables
- notes:471 — footnote, wording only
- notes:491, 492, 495, 497, 499, 501, 503, 505, 508 — heading and table introductions
- notes:494 — standing supplier text
- notes:496 — warranty policy, standing
- notes:498 — warranty table, covered by the warranty-reserve item
- notes:500, 506, 509 — standing contingency wording
- notes:502 — date rolled forward
- notes:504 — BIS/DOJ matter, unchanged since Q3; noted in the legal-fees item
- notes:507 — FY2025 indemnification, carried
- notes:510, 514, 516, 518, 520, 522, 524, 528, 532, 538 — heading and table introductions
- notes:511, 512 — duplicate of the single-segment item
- notes:513, 527 — cross-references
- notes:515 — geography wording
- notes:517, 523, 525, 526, 533, 539, 540 — tables
- notes:519, 521 — covered by the receivable-concentration item
- notes:529, 531 — revenue policy wording
- notes:535, 537 — covered by the executive trading-plan item
- notes:541, 542 — Schedule II footnotes
