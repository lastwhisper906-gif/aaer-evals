<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# SNDK — notes text reader — 10-K 0001628280-26-057406 (fiscal year ended July 3, 2026)

## Input check

Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md. Nothing forbidden is present (no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window). The 8-K carries financial-statement tables; these are part of the 8-K body and were treated as text. No arithmetic was performed: directions come from the words of the prose, and amounts are quoted as stated. Where only percentages or amounts are given, direction is `none` and the comparison is left to the numbers reader.

Prior predictions: none on record.

## Insufficient (4)

- Item 1A diff: not in the input directory. Risk-factor changes cannot be assessed.
- Exhibit 21 diff and any Exhibit 10: not in the input directory. Subsidiary and material-contract changes cannot be assessed. The Nanya agreement, the Kioxia Extension Agreements and the Agreement to Enhance Collaboration are known only from the notes.
- 8-K bodies: only the 2026-08-05 Item 2.02 release is carried. The other filings in the item-code list are codes only, with no text: 2026-03-25 (1.01, 8.01), 2026-05-15 (8.01), 2026-04-30 (2.02, 8.01) and 2026-01-02 (5.02, officer change).
- Prior annual 10-K text is not in the input. Newness against the prior annual period was judged from the note change history (second-quarter to third-quarter 10-Q) and from the dated content of the text itself. Items 1, 2 and 53 carry that caveat.

## Items

```json
[
{"id":"controls_audit_and_filings_auditor_opinion_on_internal_control","what_changed":"KPMG now gives an opinion on ICFR as of July 3, 2026 (effective), alongside a clean opinion on the financial statements. This is the company's first full fiscal year as a standalone filer. Whether the prior 10-K carried an ICFR attestation cannot be confirmed from the input.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"Also in our opinion, the Company maintained, in all material respects, effective internal control over financial reporting as of July 3, 2026","paragraph_id":"0001628280-26-057406:auditors_report:6","explanation":false},
{"id":"controls_audit_and_filings_management_report_on_internal_control","what_changed":"Item 9A carries management's ICFR assessment (effective) and refers to KPMG's attestation report. No changes in ICFR in the fourth quarter.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"has issued an audit report on our internal control over financial reporting","paragraph_id":"0001628280-26-057406:item_9a:6","explanation":false},
{"id":"controls_audit_and_filings_critical_audit_matter_revenue_evidence","what_changed":"The single critical audit matter is the sufficiency of audit evidence over revenue. KPMG cites highly automated revenue processing across IT applications, needing IT specialists, software-assisted data analysis, and sample tracing to contracts and shipping documents. The audited revenue is stated as $20,248 million.","account":"revenue, net","expected_direction":"none","horizon":"this quarter","quote":"We identified the evaluation of the sufficiency of audit evidence over revenue, net, as a critical audit matter.","paragraph_id":"0001628280-26-057406:auditors_report:19","explanation":false},
{"id":"controls_audit_and_filings_drafting_errors_in_annual_notes","what_changed":"The annual notes carry several drafting errors not in the MD&A counterparts. notes:339 says '$3 million shares' where MD&A says '3 million shares', and also 'as July 3, 2026'. notes:389 (legal) is truncated mid-sentence ('immaterial for f'). notes:221 gives an exchange rate '161.26' with no currency sign. notes:329 has a garbled vest-date fair value sentence ending 'of common stock available for future grants'. notes:207 inverts 'total commitment fee expense, including interest expense'. notes:249 states the SDSS discount will be recognized 'over the next five years' where the third-quarter note said 'next four years'. This is a sign of review quality only.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"we repurchased $3 million shares of our common stock","paragraph_id":"0001628280-26-057406:notes:339","explanation":false},
{"id":"structure_and_disclosure_changes_end_markets_renamed","what_changed":"End markets are now named Datacenter (formerly Cloud), Edge (formerly Client) and Consumer. Edge now lists 'physical AI', and Datacenter is described as datacenters, cloud service providers and private cloud. notes:24 says the prior-period segment-note presentation was reclassified. The renaming may move revenue between end-market lines.","account":"revenue by end market","expected_direction":"none","horizon":"this quarter","quote":"(formerly referred to as “Cloud”)","paragraph_id":"0001628280-26-057406:mdna:6","explanation":false},
{"id":"structure_and_disclosure_changes_balance_sheet_lines_reclassified","what_changed":"Three balance sheet lines are newly broken out: contract liabilities and refund liability (both previously in accrued expenses), and non-current income tax payable (previously in other liabilities). Prior periods were reclassified to match.","account":"accrued expenses; other liabilities; contract liabilities; refund liabilities","expected_direction":"none","horizon":"this quarter","quote":"Contract liabilities (previously presented within Accrued expenses), Refund liability (previously presented within Accrued expenses), and Income tax payable, non-current (previously presented within Other liabilities) were reclassified and presented as separate line items in the Consolidated Financial Statements.","paragraph_id":"0001628280-26-057406:notes:24","explanation":false},
{"id":"structure_and_disclosure_changes_segment_measure_adds_operating_income","what_changed":"The CODM's segment profit measures are now operating income (loss) and net income (loss). The second-quarter 10-Q named net income only. Segment expense captions now exclude stock-based compensation, and 'other segment items' now include loss on debt extinguishment.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"based upon the Company’s consolidated operating income (loss) and net income (loss)","paragraph_id":"0001628280-26-057406:notes:43","explanation":false},
{"id":"earnings_quality_fifty_three_week_fiscal_year","what_changed":"Fiscal 2026 had 53 weeks, with a 14-week first quarter. Fiscal 2025 and 2024 each had 52 weeks. Fiscal 2026 annual and first-quarter figures include an extra week, which drops out of the first-quarter comparison next year.","account":"revenue, net","expected_direction":"up","horizon":"this quarter; reverses in the first quarter of next year","quote":"Fiscal year 2026 was comprised of 53 weeks and ended on July 3, 2026, with the first fiscal quarter consisting of 14 weeks.","paragraph_id":"0001628280-26-057406:mdna:8","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_wdc_monetizing_remaining_stake","what_changed":"WDC disposed of 5,821,135 more shares on February 18, 2026 in an offering the company paid for. Restrictions on the remaining 1,691,884 shares lapsed March 19, 2026. WDC has since disposed of more shares and expects to monetize all remaining Sandisk shares by end of 2026.","account":"none","expected_direction":"none","horizon":"12 months","quote":"has announced that it expects to monetize all remaining shares of Sandisk common stock held by it by the end of 2026","paragraph_id":"0001628280-26-057406:mdna:12","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_wdc_no_longer_related_party","what_changed":"WDC ceased to be a related party as of July 3, 2026. Transactions shown with WDC are full-year amounts.","account":"none","expected_direction":"none","horizon":"next quarter","quote":"WDC ceased to be a related party of the Company as of July 3, 2026.","paragraph_id":"0001628280-26-057406:notes:259","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_transition_services_ended","what_changed":"The WDC Transition Services Agreement term ended June 10, 2026. TSA charges are stated as $2 million (fiscal 2026) and $5 million (fiscal 2025). The separation is described as finalized, with no further separation adjustments expected, and MD&A attributes lower business separation costs to completion of the separation.","account":"business separation costs","expected_direction":"down","horizon":"next quarter","quote":"The term of the TSA ended on June 10, 2026.","paragraph_id":"0001628280-26-057406:notes:38","explanation":false},
{"id":"liquidity_and_capital_term_loan_repaid_early","what_changed":"The Term Loan B (due 2032) was settled in full on March 4, 2026 from cash on hand. A $46 million loss on extinguishment came from writing off unamortized issuance costs. The $1.5 billion revolver remains undrawn and the company states covenant compliance.","account":"long-term debt; interest expense","expected_direction":"down","horizon":"this quarter","quote":"On March 4, 2026, the Company settled in full the remaining outstanding principal amounts of the Term Loan Facility, plus accrued interest, using cash on hand.","paragraph_id":"0001628280-26-057406:mdna:20","explanation":false},
{"id":"results_against_expectations_ai_demand_outlook","what_changed":"New outlook language: AI-driven demand has produced pricing shifts that helped the business. The company expects favorable pricing to lift revenue and operating cash flow, and expects AI demand to persist through calendar 2027 and beyond.","account":"revenue, net","expected_direction":"up","horizon":"12 months","quote":"We expect AI-driven demand to persist through calendar year 2027 and beyond.","paragraph_id":"0001628280-26-057406:mdna:23","explanation":false},
{"id":"narrative_signs_of_operating_pressure_tariff_exemptions_at_risk","what_changed":"New disclosure of pending Section 232 and Section 301 investigations. Most products sold in the U.S. are currently tariff-exempt, and losing exemptions or new tariffs would raise cost of goods sold.","account":"cost of revenue","expected_direction":"up","horizon":"12 months","quote":"Currently, the majority of our products sold in the U.S. are exempt from tariffs, but additional tariff increases, or the loss of applicable exemptions, would increase the cost of goods sold for our products sold in the U.S.","paragraph_id":"0001628280-26-057406:mdna:25","explanation":false},
{"id":"revenue_recognition_nbm_agreements_become_predominant","what_changed":"From fiscal 2026 the company entered multi-year New Business Model agreements with Datacenter and Edge customers. These commit volumes, use fixed and variable pricing components, and are backed by financial guarantees. NBMs are expected to become the predominant way of doing business.","account":"revenue, net; contract liabilities; refund liabilities","expected_direction":"up","horizon":"12 months","quote":"As NBMs are expected to become our predominant way of doing business","paragraph_id":"0001628280-26-057406:mdna:26","explanation":false},
{"id":"results_against_expectations_revenue_growth_led_by_pricing","what_changed":"MD&A states net revenue rose 175% while total products sold rose by mid-teens percent on an exabyte basis. The 8-K attributes fiscal-year outperformance to a mix shift toward higher-value customers and higher pricing.","account":"revenue, net","expected_direction":"up","horizon":"this quarter","quote":"Total products sold increased by mid-teens percent on an exabyte basis.","paragraph_id":"0001628280-26-057406:mdna:42","explanation":false},
{"id":"results_against_expectations_datacenter_volume_and_price","what_changed":"Datacenter revenue is stated as up 437% on higher sales and pricing. Exabytes are stated as up almost 120% and revenue per gigabyte up almost 150%.","account":"revenue, net (Datacenter)","expected_direction":"up","horizon":"this quarter","quote":"Total products sold increased by almost 120% on an exabyte basis. Revenue per gigabyte increased by almost 150%.","paragraph_id":"0001628280-26-057406:mdna:43","explanation":false},
{"id":"results_against_expectations_edge_price_per_gigabyte","what_changed":"Edge revenue is stated as up 195%. Exabytes are stated as up high single digits and revenue per gigabyte up almost 180%, so the prose attributes the growth mainly to price.","account":"revenue, net (Edge)","expected_direction":"up","horizon":"this quarter","quote":"Total products sold increased by high single-digits percent on an exabyte basis. Revenue per gigabyte increased by almost 180%.","paragraph_id":"0001628280-26-057406:mdna:44","explanation":false},
{"id":"narrative_signs_of_operating_pressure_consumer_volume_decline","what_changed":"Consumer revenue is stated as up 29% on higher pricing, partly offset by lower sales, with exabytes down mid-teens percent. The 8-K end-market table labels Consumer 'down 32%' sequentially and 'down 5%' year over year for the fourth quarter.","account":"revenue, net (Consumer)","expected_direction":"down","horizon":"next quarter","quote":"Total products sold decreased by mid-teens percent on an exabyte basis.","paragraph_id":"0001628280-26-057406:mdna:45","explanation":false},
{"id":"revenue_recognition_sales_incentives_share_of_gross_revenue","what_changed":"MD&A states price protection and sales incentive programs were 11% of gross revenue in 2026, against 19% in 2025 and 2024. These are variable-consideration estimates recorded as revenue reductions. The prose names no cause for 2026; direction is left to the numbers reader.","account":"revenue, net; variable consideration accruals","expected_direction":"none","horizon":"this quarter","quote":"For 2026, 2025 and 2024, these programs represented 11%, 19%, and 19%, respectively, of gross revenues.","paragraph_id":"0001628280-26-057406:mdna:47","explanation":false},
{"id":"results_against_expectations_gross_margin_on_pricing","what_changed":"Gross margin is stated as up 4,100 basis points and gross profit up $12,260 million, both attributed to higher sales and higher pricing.","account":"gross profit","expected_direction":"up","horizon":"this quarter","quote":"Gross profit margin increased 4,100 basis points in 2026 compared to 2025 primarily due to higher sales and higher pricing.","paragraph_id":"0001628280-26-057406:mdna:50","explanation":false},
{"id":"earnings_quality_variable_compensation_lifts_operating_expense","what_changed":"R&D and SG&A increases are attributed mainly to variable compensation tied to company performance plus headcount: $136 million in R&D and $68 million in SG&A. Stock-based compensation also rose.","account":"research and development; selling, general and administrative; accrued compensation","expected_direction":"up","horizon":"this quarter","quote":"a $136 million increase in compensation and benefits due to variable compensation associated with company performance and increased headcount","paragraph_id":"0001628280-26-057406:mdna:53","explanation":false},
{"id":"earnings_quality_qualification_units_held_in_inventory","what_changed":"Business practice changed: the company gives fewer free samples and now sells qualification units. Their cost is held in inventory until sale and then goes to cost of revenue, rather than to selling expense. MD&A cites a $51 million decrease in materials within SG&A.","account":"selling, general and administrative; inventories; cost of revenue","expected_direction":"down","horizon":"this quarter","quote":"The costs of qualification units are recorded in inventory until sold to customers and recognized as cost of revenue.","paragraph_id":"0001628280-26-057406:mdna:55","explanation":true},
{"id":"results_against_expectations_no_restructuring_actions","what_changed":"Employee termination and other charges are stated as down $23 million because no restructuring actions were taken this period.","account":"employee termination and other","expected_direction":"down","horizon":"this quarter","quote":"as there were no restructuring actions taken in the current period","paragraph_id":"0001628280-26-057406:mdna:63","explanation":false},
{"id":"earnings_quality_nanya_unrealized_gain_through_income","what_changed":"The new Nanya equity stake is carried as a marketable equity security at fair value. An $807 million unrealized gain went through net income and drives most of interest and other income (mdna:67). The 8-K excludes it from non-GAAP.","account":"gain (loss) on equity securities, net","expected_direction":"up","horizon":"this quarter","quote":"The marketable equity securities are measured at fair value with the unrealized gains (losses) amounting to $807 million for the year ended July 3, 2026, recognized through Consolidated Statements of Operations.","paragraph_id":"0001628280-26-057406:notes:183","explanation":false},
{"id":"estimates_and_discretion_nanya_fair_value_under_lockup","what_changed":"The Nanya shares are classified Level 1 at quoted price, yet the same note says they are under a three-year statutory lock-up that restricts sale. The note does not say whether the lock-up affects measurement.","account":"marketable equity securities","expected_direction":"none","horizon":"12 months","quote":"The marketable equity securities owned by the Company are subject to a statutory lock-up period of three years","paragraph_id":"0001628280-26-057406:notes:183","explanation":false},
{"id":"earnings_quality_nanya_bought_at_discount_to_market","what_changed":"Equity Investment Agreement of March 25, 2026: about 139 million Nanya shares (about 3.9%) for $970 million, paid April 8, 2026. The price was set at a 15% discount to the 30-day average, and the stake is then carried at quoted price.","account":"gain (loss) on equity securities, net; marketable equity securities","expected_direction":"up","horizon":"this quarter","quote":"The purchase price reflected a 15% discount to Nanya’s 30-day average trading price","paragraph_id":"0001628280-26-057406:notes:304","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_nanya_dram_supply_commitment","what_changed":"Alongside the equity investment, the company signed a multi-year DRAM supply arrangement with Nanya. It has committed annual volumes at quarterly variable pricing and feeds the new long-term commitments table. MD&A off-balance-sheet arrangements now list Nanya-related commitments.","account":"purchase commitments; inventories","expected_direction":"up","horizon":"12 months","quote":"Concurrently with the Equity Investment Agreement, the Company and Nanya also entered into a multi-year strategic supply arrangement pursuant to which Nanya will supply the Company with DRAM products.","paragraph_id":"0001628280-26-057406:notes:305","explanation":false},
{"id":"across_documents_legal_settlement_charges","what_changed":"New sentence: $93 million of fiscal 2026 legal settlements recognized in other income (expense), net; the sentence is truncated. MD&A (mdna:67) attributes a $118 million increase in other expenses primarily to settling non-operating legal matters. The 8-K excludes these settlements from non-GAAP as Other adjustments. The figures are stated three ways and left for reconciliation.","account":"other income (expense), net","expected_direction":"up","horizon":"this quarter","quote":"During the 2026 fiscal year, the Company recognized $93 million related to legal settlements in Other income/(expense), net.","paragraph_id":"0001628280-26-057406:notes:389","explanation":false},
{"id":"earnings_quality_non_gaap_excludes_equity_securities_gain","what_changed":"Non-GAAP measures now exclude (gain) loss on equity securities: the Nanya mark-to-market plus gains and impairments on equity investments. notes:52 says equity-method earnings are booked in this same line, so the exclusion may also remove equity-method results.","account":"non-GAAP net income","expected_direction":"none","horizon":"this quarter","quote":"(Gain) loss on equity securities, net consists of ongoing mark-to-market adjustments on the Company’s investments in marketable equity securities","paragraph_id":"0001628280-26-053346:8k_2_02:78","explanation":false},
{"id":"earnings_quality_non_gaap_excludes_legal_settlements","what_changed":"The non-GAAP 'Other adjustments' category now holds charges for settling previously existing legal matters in fiscal 2026.","account":"non-GAAP net income; other income (expense), net","expected_direction":"none","horizon":"this quarter","quote":"For the year ended July 3, 2026, Other adjustments include charges for the settlement of certain previously existing legal matters.","paragraph_id":"0001628280-26-053346:8k_2_02:79","explanation":false},
{"id":"liquidity_and_capital_adjusted_free_cash_flow_removes_nbm_payments","what_changed":"New 'Adjusted free cash flow' measure. It deducts NBM prepayments and NBM deposits received or returned, and adds back Flash Ventures activity. The company says NBM cash flows are not indicative of core cash flows.","account":"operating cash flow","expected_direction":"down","horizon":"this quarter","quote":"The Company is adjusting for the NBM Payments because the Company believes that these cash flows are not indicative of the core underlying cash flows of the Company’s business.","paragraph_id":"0001628280-26-053346:8k_2_02:81","explanation":false},
{"id":"revenue_recognition_additional_nbms_signed_after_april","what_changed":"Five more NBM agreements were signed since the April call: three with new customers and two expanding existing NBMs. notes:398 separately reports two NBMs after the balance sheet date; the windows differ.","account":"remaining performance obligations; contract liabilities; refund liabilities","expected_direction":"up","horizon":"next quarter","quote":"we have signed five additional agreements, including three NBMs with new customers and two deals expanding on previously signed NBMs","paragraph_id":"0001628280-26-053346:8k_2_02:8","explanation":false},
{"id":"revenue_recognition_subsequent_nbms_transaction_price","what_changed":"Subsequent event: two more NBMs with an aggregate transaction price of $31.3 billion. Customer obligations are backed by cash deposits and other financial instruments.","account":"remaining performance obligations; refund liabilities; contract liabilities","expected_direction":"up","horizon":"next quarter","quote":"Subsequent to the balance sheet date, the Company entered into two additional NBMs with an aggregate transaction price of $31.3 billion.","paragraph_id":"0001628280-26-057406:notes:398","explanation":false},
{"id":"results_against_expectations_first_quarter_guidance","what_changed":"First-quarter fiscal 2027 guidance: revenue $10.30 to $10.80 billion; non-GAAP EPS $44.00 to $46.00; GAAP gross margin 83.0% to 84.9%. The prose states a range only, with no direction.","account":"revenue, net","expected_direction":"none","horizon":"next quarter","quote":"Expect first quarter 2027 revenue to be in the range of $10.30 billion to $10.80 billion","paragraph_id":"0001628280-26-053346:8k_2_02:10","explanation":false},
{"id":"results_against_expectations_fourth_quarter_pricing_share_of_growth","what_changed":"Fourth-quarter revenue of $8.97 billion is stated as up 51% sequentially. About one-third of the growth is attributed to volume and two-thirds to pricing.","account":"revenue, net","expected_direction":"up","horizon":"this quarter","quote":"Sequential revenue growth came approximately one-third from higher volumes and two-thirds from higher pricing.","paragraph_id":"0001628280-26-053346:8k_2_02:6","explanation":false},
{"id":"estimates_and_discretion_foreign_tax_rate_change_next_year","what_changed":"OBBBA: a $10 million benefit was recorded on the fiscal 2025 provision. MD&A adds that H.R. 1 changes the tax rates on foreign subsidiary income from fiscal 2027 onward, and that these changes can raise the effective tax rate and reduce operating cash flow. The notes version (notes:353) omits the fiscal-year timing.","account":"income tax expense; operating cash flow","expected_direction":"down","horizon":"12 months","quote":"The tax rates for income earned by our foreign subsidiaries will also be changed under H.R. 1, which applies to our fiscal years 2027 and onward.","paragraph_id":"0001628280-26-057406:mdna:69","explanation":false},
{"id":"liquidity_and_capital_minimum_tax_expected_next_year","what_changed":"New expectation that the company will be subject to the 15% corporate alternative minimum tax in fiscal 2027. The parallel note (notes:354) carries the CAMT paragraph without this sentence.","account":"income tax expense; income tax payable","expected_direction":"up","horizon":"12 months","quote":"We expect to be subject to CAMT in fiscal year 2027.","paragraph_id":"0001628280-26-057406:mdna:70","explanation":false},
{"id":"earnings_quality_pillar_two_taxes_in_expense","what_changed":"Pillar Two is now effective in most of the company's jurisdictions, and those taxes are included in fiscal 2026 income tax expense.","account":"income tax expense","expected_direction":"up","horizon":"this quarter","quote":"Accordingly, these taxes are included in the Company’s Income tax expense for the year ended July 3, 2026.","paragraph_id":"0001628280-26-057406:mdna:71","explanation":false},
{"id":"earnings_quality_tax_rate_lowered_by_deduction_and_holidays","what_changed":"A 12% effective tax rate is attributed to jurisdictional mix, foreign-derived deduction-eligible income (a new term), credits and Malaysian tax holidays expiring 2028 through 2031. Notes state the holiday benefit at $492 million (3.18 per share) and show a new rate-reconciliation line for the foreign-derived deduction.","account":"income tax expense","expected_direction":"down","horizon":"this quarter; reverses as holidays expire","quote":"foreign-derived deduction-eligible income, credits, and tax holidays in Malaysia that will expire at various dates during years 2028 through 2031","paragraph_id":"0001628280-26-057406:mdna:75","explanation":false},
{"id":"liquidity_and_capital_capital_expenditure_increase_planned","what_changed":"Capex was described as conservative for fiscal 2025 and 2026. The company now anticipates increased capital investment in fiscal 2027 for the transition to newer nodes.","account":"purchases of property, plant and equipment","expected_direction":"up","horizon":"12 months","quote":"For fiscal year 2027, we anticipate increased capital investments as we transition to newer nodes to meet the demand and technology needs of our product portfolio.","paragraph_id":"0001628280-26-057406:mdna:81","explanation":false},
{"id":"liquidity_and_capital_working_capital_use_attributed_to_volume","what_changed":"MD&A states operating assets and liabilities used $212 million of cash in 2026, against $380 million provided in 2025. It attributes this to higher business volume and adds tax-payment timing as a working-capital factor.","account":"accounts receivable; inventories; changes in operating assets and liabilities","expected_direction":"down","horizon":"this quarter","quote":"reflecting an increase in the volume of our business, as discussed above","paragraph_id":"0001628280-26-057406:mdna:85","explanation":true},
{"id":"liquidity_and_capital_receivable_days_down_on_collections","what_changed":"DSO is stated as down 3 days, attributed to shipment timing and continued strong collections.","account":"accounts receivable, net","expected_direction":"down","horizon":"this quarter","quote":"DSO decreased 3 days when compared to the prior year, primarily due to the timing of shipments and continued strong receivables collections","paragraph_id":"0001628280-26-057406:mdna:89","explanation":true},
{"id":"narrative_signs_of_operating_pressure_inventory_days_up_on_builds","what_changed":"DIO is stated as up 43 days, attributed to inventory builds to meet demand.","account":"inventories","expected_direction":"up","horizon":"this quarter","quote":"DIO increased 43 days over the prior year, primarily due to inventory builds to meet demand","paragraph_id":"0001628280-26-057406:mdna:89","explanation":true},
{"id":"liquidity_and_capital_payable_days_up_on_timing","what_changed":"DPO is stated as up 14 days, attributed to routine timing of purchases and payments. The same section says the company sometimes changes vendor payment timing to manage cash.","account":"accounts payable","expected_direction":"up","horizon":"this quarter","quote":"DPO increased 14 days over the prior year, primarily due to routine variations in the timing of purchases and payments","paragraph_id":"0001628280-26-057406:mdna:89","explanation":false},
{"id":"liquidity_and_capital_customer_advances_raise_cash","what_changed":"Customer advances under long-term agreements increased cash. Contract liabilities are stated at $1,242 million and refundable security deposits (refund liabilities) at $1,500 million.","account":"cash and cash equivalents; contract liabilities; refund liabilities","expected_direction":"up","horizon":"this quarter","quote":"In connection with entering into long-term agreements with certain customers, we received customer advances that increased our available cash and cash equivalents.","paragraph_id":"0001628280-26-057406:mdna:120","explanation":false},
{"id":"liquidity_and_capital_share_repurchase_programs","what_changed":"A $6.0 billion program was approved April 30, 2026, and an additional $14.0 billion on August 5, 2026 (subsequent event). The company repurchased 3 million shares for $4.5 billion in fiscal 2026, with $1.5 billion remaining at year end; the 8-K states total remaining authorization of $15.5 billion. Treasury stock policy has been added, and the liquidity-sufficiency statement now covers funding repurchases.","account":"treasury stock; cash and cash equivalents","expected_direction":"up","horizon":"12 months","quote":"On August 5, 2026, we announced that our Board of Directors had approved an additional $14.0 billion share repurchase program (exclusive of fees and commissions)","paragraph_id":"0001628280-26-057406:mdna:122","explanation":false},
{"id":"across_documents_inventory_reserve_immaterial_versus_charges","what_changed":"MD&A critical estimates say 2026 reserve adjustments were immaterial. Note 5 (notes:162) states inventory charges of $91 million (fiscal 2026) and $45 million (fiscal 2025) in cost of revenue, and provisions of $125 million and $126 million. Left for reconciliation.","account":"inventories; cost of revenue","expected_direction":"none","horizon":"this quarter","quote":"Adjustments to the reserve in 2026 were immaterial.","paragraph_id":"0001628280-26-057406:mdna:132","explanation":false},
{"id":"revenue_recognition_contract_liabilities_from_nbm_advances","what_changed":"Contract liabilities are now primarily NBM advances, stated at $1,242 million at year end; $23 million of the opening $25 million was recognized as revenue. The increase is attributed to NBM customer advances. The second-quarter note described contract liabilities as service and support items and not material.","account":"contract liabilities; revenue, net","expected_direction":"up","horizon":"12 months","quote":"The increase in contract liabilities during the period was driven by customer advances associated with NBMs entered into during the period.","paragraph_id":"0001628280-26-057406:notes:137","explanation":false},
{"id":"liquidity_and_capital_refund_liabilities_from_security_deposits","what_changed":"Refund liabilities (which per notes:74 also hold rebates not netted against receivables) are stated at $1,500 million against $126 million. The increase is attributed to NBM security deposits refundable at contract end.","account":"refund liabilities","expected_direction":"up","horizon":"this quarter","quote":"The increase in refund liabilities during the period was driven by security deposits associated with NBMs entered into during the period ended July 3, 2026.","paragraph_id":"0001628280-26-057406:notes:138","explanation":true},
{"id":"revenue_recognition_nbm_collateral_not_recognized","what_changed":"New policy and disclosure: NBM customers may post collateral with third-party institutions. It is not recognized unless a default occurs, and $5.0 billion is stated as the maximum available on default.","account":"none","expected_direction":"none","horizon":"12 months","quote":"The aggregate amount of collateral issued or held by third-party financial institutions was $5.0 billion as of July 3, 2026","paragraph_id":"0001628280-26-057406:notes:140","explanation":false},
{"id":"revenue_recognition_remaining_performance_obligations_from_nbms","what_changed":"RPO stated at $59.8 billion, entirely NBMs: $58.7 billion unbilled and $1.1 billion in contract liabilities, with about 19% expected within twelve months. MD&A says NBMs include variable pricing components, so the RPO depends on transaction-price estimates. The third-quarter figure was $41.6 billion, and before that RPO was not material.","account":"remaining performance obligations; revenue, net","expected_direction":"none","horizon":"12 months","quote":"As of July 3, 2026, the transaction price allocated to remaining performance obligations was $59.8 billion","paragraph_id":"0001628280-26-057406:notes:141","explanation":false},
{"id":"revenue_recognition_rebates_netted_against_receivables","what_changed":"The policy states sales rebates are netted against open customer receivables when offset criteria are met, and otherwise recorded in refund liabilities. This sits alongside the newly separate refund liability line. Newness against the prior 10-K cannot be confirmed.","account":"accounts receivable, net; refund liabilities","expected_direction":"none","horizon":"this quarter","quote":"The Company nets sales rebates against open customer receivable balances if the criteria to offset are met, otherwise they are recorded in refund liabilities.","paragraph_id":"0001628280-26-057406:notes:74","explanation":false},
{"id":"revenue_recognition_receivable_concentration_three_customers","what_changed":"At year end, three customers held about 19%, 12% and 10% of receivables of $4.7 billion. At the prior year end, one customer held 11% of $1.1 billion. No single customer exceeded 10% of annual revenue, and top-10 customers were 44%.","account":"accounts receivable, net","expected_direction":"none","horizon":"next quarter","quote":"three customers accounted for approximately 19%, 12% and 10%, respectively, of the Company’s outstanding accounts receivable","paragraph_id":"0001628280-26-057406:notes:131","explanation":false},
{"id":"estimates_and_discretion_warranty_estimate_change_pre_existing","what_changed":"The warranty rollforward shows a negative 2026 change in estimate for pre-existing warranties, (28), against positive 4 in 2025, while charges to operations are 62. No prose explains the reversal.","account":"warranty accrual; cost of revenue","expected_direction":"down","horizon":"this quarter","quote":"Changes in estimate related to pre-existing warranties","paragraph_id":"0001628280-26-057406:notes:168","explanation":false},
{"id":"structure_and_disclosure_changes_cash_flow_hedge_designation_ended","what_changed":"At year end all FX forwards are non-designated hedges, whereas the prior year had cash flow hedges. The AOCL derivative component is now nil. FX contract fair-value changes now run through other income (expense) instead of being deferred to cost of revenue.","account":"accumulated other comprehensive loss; other income (expense), net; cost of revenue","expected_direction":"none","horizon":"next quarter","quote":"As of July 3, 2026, the Company had outstanding foreign exchange forward contracts that were designated as non-designated hedges.","paragraph_id":"0001628280-26-057406:notes:186","explanation":false},
{"id":"earnings_quality_flash_ventures_distributions_in_operating_cash_flow","what_changed":"Flash Ventures distributions of $107 million in fiscal 2026 are classified in operating cash flow; fiscal 2025's $176 million was classified in investing. The 8-K cash flow statement shows them netted in 'Equity loss in investees, net of dividends received'.","account":"net cash provided by operating activities","expected_direction":"up","horizon":"this quarter","quote":"The distributions received for the year ended July 3, 2026 were classified as cash flow from operating activities while the distributions received for the year ended June 27, 2025 were classified as cash flow from investing activities in our Consolidated Statements of Cash Flows.","paragraph_id":"0001628280-26-057406:notes:229","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_flash_ventures_term_extended","what_changed":"Extension Agreements of January 29, 2026 extend Flash Alliance and Flash Partners from 2029 to December 31, 2034. All three Flash Ventures now co-terminate in 2034, which lengthens the fixed-cost and guarantee exposure period.","account":"none","expected_direction":"none","horizon":"12 months","quote":"Following the execution of the Extension Agreements, all three of the joint ventures that comprise the Flash Ventures are scheduled to co-terminate on December 31, 2034.","paragraph_id":"0001628280-26-057406:notes:224","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_kioxia_supply_payments","what_changed":"Agreement to Enhance Collaboration: $1.2 billion paid directly to Kioxia over 2026 through 2029 for manufacturing services and supply through 2034. The payments are amortized straight-line into inventory and cost of revenue on sale. MD&A material cash requirements now include these payments within Flash Ventures commitments.","account":"cost of revenue; other current and non-current assets","expected_direction":"up","horizon":"12 months","quote":"These payments are amortized on a straight-line basis and will be recognized as Cost of revenue in the Consolidated Statements of Operations upon sale of inventory.","paragraph_id":"0001628280-26-057406:notes:225","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_new_fab_output_began","what_changed":"Output from the K2 Kitakami fab began in fiscal 2026.","account":"inventories; cost of revenue","expected_direction":"none","horizon":"12 months","quote":"Output from K2 began in the fiscal year ended July 3, 2026.","paragraph_id":"0001628280-26-057406:notes:220","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_building_prepayment_commitments","what_changed":"Flash Ventures building-depreciation prepayments outstanding are stated at $840 million. Committed future prepayments are $402 million, payable through fiscal 2035, and are now described as credited against future wafer purchases. The third-quarter text had a separate sentence on building-depreciation payments through fiscal 2034, which is not carried.","account":"other current assets; other non-current assets; cost of revenue","expected_direction":"none","horizon":"12 months","quote":"payable at varying dates through fiscal year 2035","paragraph_id":"0001628280-26-057406:notes:221","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_sdss_working_capital_amendment","what_changed":"A September 25, 2025 amendment with JCET gave $10 million of working-capital support. This reduced the September 2025 installment to $27 million and was booked as a loss on business divestiture.","account":"loss on business divestiture; consideration receivable","expected_direction":"down","horizon":"this quarter","quote":"included a $10 million provision for working capital support, resulting in a reduction of the September 28, 2025 installment payment from JCET to $27 million","paragraph_id":"0001628280-26-057406:notes:248","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_sdss_penalty_trigger_wording","what_changed":"The SDSS supply-agreement penalty is now worded as payable by the company if SDSS fails to meet the minimum annual commitment; the third-quarter text read 'if it fails'. Fiscal 2026 purchases are stated at $519 million against a $550 million minimum annual commitment. Shortfall-penalty exposure is not quantified.","account":"cost of revenue; accrued expenses","expected_direction":"none","horizon":"12 months","quote":"The Supply Agreement contains specific penalties the Company must pay if SDSS fails to meet its minimum annual commitment.","paragraph_id":"0001628280-26-057406:notes:251","explanation":false},
{"id":"across_documents_equity_method_results_line","what_changed":"The equity-investment policy now says equity-method earnings and losses are recognized in gain (loss) on equity securities, net. The SDSS and Unis notes (notes:250, notes:255) say other income (expense), net. The 8-K non-GAAP excludes gain (loss) on equity securities.","account":"gain (loss) on equity securities, net; other income (expense), net","expected_direction":"none","horizon":"this quarter","quote":"The Company’s equity in the earnings or losses in equity-method investments is recognized in Gain (loss) on equity securities, net, in the Consolidated Statements of Operations.","paragraph_id":"0001628280-26-057406:notes:52","explanation":false},
{"id":"estimates_and_discretion_unrecognized_tax_benefits","what_changed":"Unrecognized tax benefits are stated at $323 million against $140 million. The rollforward shows gross increases for current-year positions of 168, and MD&A says about $259 million could result in cash payments. The rate reconciliation shows a change in unrecognized tax benefits of 70.","account":"income tax payable, non-current; income tax expense","expected_direction":"up","horizon":"12 months","quote":"As of July 3, 2026 and June 27, 2025, the liability for unrecognized tax benefits (excluding accrued interest and penalties) was $323 million and $140 million, respectively.","paragraph_id":"0001628280-26-057406:notes:386","explanation":false},
{"id":"estimates_and_discretion_deferred_tax_assets_and_valuation_allowance","what_changed":"Management attributes the decrease in net deferred tax assets mainly to a deferred tax liability on the unrealized marketable-securities gain, partly offset by lower liabilities on undistributed foreign earnings. Valuation allowances remain on certain loss and credit carryforwards. NOL carryforwards are stated at $0.3 billion against $2.1 billion, mostly in Malaysia.","account":"deferred tax assets; deferred tax liabilities; valuation allowance","expected_direction":"down","horizon":"this quarter","quote":"The decrease in the net deferred tax assets is attributable primarily to unrealized gain on marketable securities, offset by a decrease in deferred tax liabilities on undistributed foreign earnings.","paragraph_id":"0001628280-26-057406:notes:364","explanation":true},
{"id":"structure_and_disclosure_changes_income_tax_disclosure_standard_adopted","what_changed":"ASU 2023-09 was adopted prospectively, with a new disaggregated rate reconciliation and cash taxes paid by jurisdiction ($146 million total). The prior years keep the old format.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"The Company adopted this ASU for the fiscal year ended July 3, 2026, and the resulting incremental disclosures have been applied prospectively.","paragraph_id":"0001628280-26-057406:notes:113","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_executive_trading_plans","what_changed":"New Rule 10b5-1 plans: the CEO (up to 124,192 shares, adopted May 29, 2026), the CFO (up to 11,000 shares, adopted May 22, 2026), and the CTO (adopted June 4, 2026 after terminating a February plan with no sales).","account":"none","expected_direction":"none","horizon":"12 months","quote":"David Goeckeler, Chief Executive Officer of the Company, adopted a Rule 10b5-1 Plan on May 29, 2026.","paragraph_id":"0001628280-26-057406:notes:401","explanation":false},
{"id":"estimates_and_discretion_no_goodwill_impairment","what_changed":"No goodwill impairment in fiscal 2026, after the $1.8 billion charge in fiscal 2025. MD&A states goodwill impairment decreased $1.8 billion.","account":"goodwill impairment","expected_direction":"down","horizon":"this quarter","quote":"For the year ended July 3, 2026, there were no goodwill impairment charges recorded.","paragraph_id":"0001628280-26-057406:mdna:15","explanation":false},
{"id":"structure_and_disclosure_changes_finite_lived_intangibles_reappear","what_changed":"Finite-lived intangible assets now exist, though immaterial; at the prior year end all were fully amortized. Their source is not described.","account":"other non-current assets","expected_direction":"up","horizon":"this quarter","quote":"As of July 3, 2026 the amount of finite-lived intangible assets is immaterial.","paragraph_id":"0001628280-26-057406:notes:165","explanation":false}
]
```

Items: 70. Items flagged `explanation: true`: 6 — qualification units held in inventory, working-capital use attributed to volume, DSO, DIO, refund liabilities, and deferred tax assets/valuation allowance.

## Paragraphs read and not made an item

The note change history (input_notes_history.md) was used only as context for what is new, as instructed, and is not listed here.

### Auditor's report and Item 9A
- 0001628280-26-057406:auditors_report:1 — heading
- 0001628280-26-057406:auditors_report:2 — heading
- 0001628280-26-057406:auditors_report:3 — heading
- 0001628280-26-057406:auditors_report:4 — heading
- 0001628280-26-057406:auditors_report:5 — scope; covered by auditor ICFR item
- 0001628280-26-057406:auditors_report:7 — heading
- 0001628280-26-057406:auditors_report:8 — standard basis language
- 0001628280-26-057406:auditors_report:9 — standard language
- 0001628280-26-057406:auditors_report:10 — standard language
- 0001628280-26-057406:auditors_report:11 — heading
- 0001628280-26-057406:auditors_report:12 — standard ICFR definition
- 0001628280-26-057406:auditors_report:13 — standard limitations
- 0001628280-26-057406:auditors_report:14 — page number
- 0001628280-26-057406:auditors_report:15 — heading
- 0001628280-26-057406:auditors_report:16 — standard CAM preamble
- 0001628280-26-057406:auditors_report:17 — CAM title; covered by CAM item
- 0001628280-26-057406:auditors_report:18 — CAM description; covered by CAM item
- 0001628280-26-057406:auditors_report:20 — CAM procedures; covered by CAM item
- 0001628280-26-057406:auditors_report:21 — signature
- 0001628280-26-057406:auditors_report:22 — tenure unchanged
- 0001628280-26-057406:auditors_report:23 — location
- 0001628280-26-057406:auditors_report:24 — report date
- 0001628280-26-057406:auditors_report:25 — page number
- 0001628280-26-057406:auditors_report:26 — header
- 0001628280-26-057406:item_9a:1 — heading
- 0001628280-26-057406:item_9a:2 — heading
- 0001628280-26-057406:item_9a:3 — disclosure controls effective; standard conclusion
- 0001628280-26-057406:item_9a:4 — heading
- 0001628280-26-057406:item_9a:5 — standard ICFR definition
- 0001628280-26-057406:item_9a:7 — heading
- 0001628280-26-057406:item_9a:8 — no ICFR changes; standard

### MD&A
- 0001628280-26-057406:mdna:1 — heading
- 0001628280-26-057406:mdna:2 — cross-reference; date rolled forward
- 0001628280-26-057406:mdna:3 — definitions boilerplate
- 0001628280-26-057406:mdna:4 — heading
- 0001628280-26-057406:mdna:5 — heading
- 0001628280-26-057406:mdna:7 — end-market description; covered by renaming item
- 0001628280-26-057406:mdna:9 — heading
- 0001628280-26-057406:mdna:10 — separation history unchanged
- 0001628280-26-057406:mdna:11 — separation history unchanged
- 0001628280-26-057406:mdna:13 — heading
- 0001628280-26-057406:mdna:14 — prior-year impairment restated
- 0001628280-26-057406:mdna:16 — heading
- 0001628280-26-057406:mdna:17 — pre-separation financing unchanged
- 0001628280-26-057406:mdna:18 — loan agreement terms unchanged
- 0001628280-26-057406:mdna:19 — loan draw history unchanged
- 0001628280-26-057406:mdna:21 — revolver undrawn; unchanged
- 0001628280-26-057406:mdna:22 — heading
- 0001628280-26-057406:mdna:24 — page number
- 0001628280-26-057406:mdna:27 — generic monitoring statement
- 0001628280-26-057406:mdna:28 — heading
- 0001628280-26-057406:mdna:29 — basis of presentation unchanged
- 0001628280-26-057406:mdna:30 — boilerplate
- 0001628280-26-057406:mdna:31 — carve-out allocation language unchanged
- 0001628280-26-057406:mdna:32 — heading
- 0001628280-26-057406:mdna:33 — heading
- 0001628280-26-057406:mdna:34 — table lead-in
- 0001628280-26-057406:mdna:35 — amounts only
- 0001628280-26-057406:mdna:36 — rounding footnote
- 0001628280-26-057406:mdna:37 — table lead-in
- 0001628280-26-057406:mdna:38 — amounts only
- 0001628280-26-057406:mdna:39 — page number
- 0001628280-26-057406:mdna:40 — end-market description; covered by renaming item
- 0001628280-26-057406:mdna:41 — heading
- 0001628280-26-057406:mdna:46 — geographic attribution; amounts only
- 0001628280-26-057406:mdna:48 — heading
- 0001628280-26-057406:mdna:49 — gross profit amount; covered by gross margin item
- 0001628280-26-057406:mdna:51 — heading
- 0001628280-26-057406:mdna:52 — heading
- 0001628280-26-057406:mdna:54 — heading
- 0001628280-26-057406:mdna:56 — heading
- 0001628280-26-057406:mdna:57 — covered by no-goodwill-impairment item
- 0001628280-26-057406:mdna:58 — heading
- 0001628280-26-057406:mdna:59 — covered by term loan item
- 0001628280-26-057406:mdna:60 — heading
- 0001628280-26-057406:mdna:61 — covered by TSA/separation item
- 0001628280-26-057406:mdna:62 — heading
- 0001628280-26-057406:mdna:64 — heading
- 0001628280-26-057406:mdna:65 — covered by SDSS amendment item
- 0001628280-26-057406:mdna:66 — heading
- 0001628280-26-057406:mdna:67 — covered by Nanya gain and legal settlement items
- 0001628280-26-057406:mdna:68 — heading
- 0001628280-26-057406:mdna:72 — table lead-in
- 0001628280-26-057406:mdna:73 — amounts only
- 0001628280-26-057406:mdna:74 — page number
- 0001628280-26-057406:mdna:76 — prior-year rate drivers
- 0001628280-26-057406:mdna:77 — cross-reference
- 0001628280-26-057406:mdna:78 — heading
- 0001628280-26-057406:mdna:79 — table lead-in
- 0001628280-26-057406:mdna:80 — amounts only
- 0001628280-26-057406:mdna:82 — covered by share repurchase item
- 0001628280-26-057406:mdna:83 — amounts only (cash held abroad)
- 0001628280-26-057406:mdna:84 — heading
- 0001628280-26-057406:mdna:86 — cash conversion definition; wording
- 0001628280-26-057406:mdna:87 — amounts only
- 0001628280-26-057406:mdna:88 — vendor payment-term language, likely carried; referenced in DPO item
- 0001628280-26-057406:mdna:90 — heading
- 0001628280-26-057406:mdna:91 — amounts; covered by Nanya and Flash Ventures items
- 0001628280-26-057406:mdna:92 — heading
- 0001628280-26-057406:mdna:93 — amounts; covered by repurchase and term loan items
- 0001628280-26-057406:mdna:94 — cross-reference
- 0001628280-26-057406:mdna:95 — heading
- 0001628280-26-057406:mdna:96 — Nanya added; covered by Nanya supply item
- 0001628280-26-057406:mdna:97 — heading
- 0001628280-26-057406:mdna:98 — heading
- 0001628280-26-057406:mdna:99 — table lead-in
- 0001628280-26-057406:mdna:100 — amounts only
- 0001628280-26-057406:mdna:101 — Kioxia payments added; covered by Kioxia supply item
- 0001628280-26-057406:mdna:102 — heading
- 0001628280-26-057406:mdna:103 — covered by term loan item
- 0001628280-26-057406:mdna:104 — covered by term loan item
- 0001628280-26-057406:mdna:105 — covenant compliance; date rolled
- 0001628280-26-057406:mdna:106 — heading
- 0001628280-26-057406:mdna:107 — lease guarantee compliance; date rolled
- 0001628280-26-057406:mdna:108 — heading
- 0001628280-26-057406:mdna:109 — purchase-order boilerplate
- 0001628280-26-057406:mdna:110 — page number
- 0001628280-26-057406:mdna:111 — heading
- 0001628280-26-057406:mdna:112 — covered by unrecognized tax benefits item
- 0001628280-26-057406:mdna:113 — heading
- 0001628280-26-057406:mdna:114 — hedging boilerplate
- 0001628280-26-057406:mdna:115 — heading
- 0001628280-26-057406:mdna:116 — tax indemnification; amounts only
- 0001628280-26-057406:mdna:117 — indemnification boilerplate
- 0001628280-26-057406:mdna:118 — indemnification boilerplate
- 0001628280-26-057406:mdna:119 — heading
- 0001628280-26-057406:mdna:121 — heading
- 0001628280-26-057406:mdna:123 — heading
- 0001628280-26-057406:mdna:124 — cross-reference
- 0001628280-26-057406:mdna:125 — heading
- 0001628280-26-057406:mdna:126 — estimates boilerplate
- 0001628280-26-057406:mdna:127 — heading
- 0001628280-26-057406:mdna:128 — variable consideration policy unchanged
- 0001628280-26-057406:mdna:129 — variable consideration method unchanged
- 0001628280-26-057406:mdna:130 — heading
- 0001628280-26-057406:mdna:131 — inventory valuation policy unchanged

### Notes
- 0001628280-26-057406:notes:1 — proxy incorporation boilerplate
- 0001628280-26-057406:notes:2 — cybersecurity boilerplate
- 0001628280-26-057406:notes:3 — cybersecurity boilerplate
- 0001628280-26-057406:notes:4 — cybersecurity boilerplate
- 0001628280-26-057406:notes:5 — cybersecurity; wording (standard revision cited)
- 0001628280-26-057406:notes:6 — cybersecurity boilerplate
- 0001628280-26-057406:notes:7 — cybersecurity boilerplate
- 0001628280-26-057406:notes:8 — cybersecurity; no material incident
- 0001628280-26-057406:notes:9 — cyber governance boilerplate
- 0001628280-26-057406:notes:10 — cyber governance; officer credentials
- 0001628280-26-057406:notes:11 — cyber governance boilerplate
- 0001628280-26-057406:notes:12 — cyber governance boilerplate
- 0001628280-26-057406:notes:13 — heading
- 0001628280-26-057406:notes:14 — description; covered by renaming item
- 0001628280-26-057406:notes:15 — separation history unchanged
- 0001628280-26-057406:notes:16 — separation history unchanged
- 0001628280-26-057406:notes:17 — separation agreements unchanged
- 0001628280-26-057406:notes:18 — covered by term loan item
- 0001628280-26-057406:notes:19 — award conversion unchanged
- 0001628280-26-057406:notes:20 — covered by WDC stake item
- 0001628280-26-057406:notes:21 — heading
- 0001628280-26-057406:notes:22 — basis of presentation unchanged
- 0001628280-26-057406:notes:23 — heading
- 0001628280-26-057406:notes:25 — heading
- 0001628280-26-057406:notes:26 — consolidation policy unchanged
- 0001628280-26-057406:notes:27 — units boilerplate
- 0001628280-26-057406:notes:28 — heading
- 0001628280-26-057406:notes:29 — carve-out history unchanged
- 0001628280-26-057406:notes:30 — carve-out history unchanged
- 0001628280-26-057406:notes:31 — carve-out history unchanged
- 0001628280-26-057406:notes:32 — carve-out history unchanged
- 0001628280-26-057406:notes:33 — allocation history unchanged
- 0001628280-26-057406:notes:34 — stock compensation history unchanged
- 0001628280-26-057406:notes:35 — separate-return method unchanged
- 0001628280-26-057406:notes:36 — heading
- 0001628280-26-057406:notes:37 — date rolled forward
- 0001628280-26-057406:notes:39 — heading
- 0001628280-26-057406:notes:40 — duplicate; covered by fifty-three-week item
- 0001628280-26-057406:notes:41 — heading
- 0001628280-26-057406:notes:42 — single segment unchanged
- 0001628280-26-057406:notes:44 — cross-reference
- 0001628280-26-057406:notes:45 — heading
- 0001628280-26-057406:notes:46 — estimates boilerplate
- 0001628280-26-057406:notes:47 — heading
- 0001628280-26-057406:notes:48 — separation costs policy unchanged
- 0001628280-26-057406:notes:49 — heading
- 0001628280-26-057406:notes:50 — cash equivalents policy; wording
- 0001628280-26-057406:notes:51 — heading
- 0001628280-26-057406:notes:53 — fair-value equity policy; covered by Nanya items
- 0001628280-26-057406:notes:54 — heading
- 0001628280-26-057406:notes:55 — VIE policy unchanged
- 0001628280-26-057406:notes:56 — heading
- 0001628280-26-057406:notes:57 — fair value policy; Nanya mention covered
- 0001628280-26-057406:notes:58 — heading
- 0001628280-26-057406:notes:59 — inventory policy unchanged
- 0001628280-26-057406:notes:60 — inventory policy unchanged
- 0001628280-26-057406:notes:61 — heading
- 0001628280-26-057406:notes:62 — PP&E policy unchanged
- 0001628280-26-057406:notes:63 — heading
- 0001628280-26-057406:notes:64 — goodwill policy unchanged
- 0001628280-26-057406:notes:65 — goodwill policy unchanged
- 0001628280-26-057406:notes:66 — goodwill judgment boilerplate
- 0001628280-26-057406:notes:67 — covered by no-goodwill-impairment item
- 0001628280-26-057406:notes:68 — heading
- 0001628280-26-057406:notes:69 — revenue policy unchanged
- 0001628280-26-057406:notes:70 — revenue policy unchanged
- 0001628280-26-057406:notes:71 — payment terms unchanged
- 0001628280-26-057406:notes:72 — variable consideration policy unchanged
- 0001628280-26-057406:notes:73 — variable consideration method unchanged
- 0001628280-26-057406:notes:75 — multiple-obligation policy unchanged
- 0001628280-26-057406:notes:76 — covered by contract liabilities item
- 0001628280-26-057406:notes:77 — covered by collateral item
- 0001628280-26-057406:notes:78 — covered by collateral item
- 0001628280-26-057406:notes:79 — allowance policy unchanged
- 0001628280-26-057406:notes:80 — heading
- 0001628280-26-057406:notes:81 — warranty policy unchanged
- 0001628280-26-057406:notes:82 — heading
- 0001628280-26-057406:notes:83 — litigation policy unchanged
- 0001628280-26-057406:notes:84 — heading
- 0001628280-26-057406:notes:85 — advertising; amounts only
- 0001628280-26-057406:notes:86 — heading
- 0001628280-26-057406:notes:87 — R&D policy unchanged
- 0001628280-26-057406:notes:88 — heading
- 0001628280-26-057406:notes:89 — tax-law uncertainty boilerplate
- 0001628280-26-057406:notes:90 — tax policy unchanged
- 0001628280-26-057406:notes:91 — uncertain-position policy unchanged
- 0001628280-26-057406:notes:92 — heading
- 0001628280-26-057406:notes:93 — EPS policy unchanged
- 0001628280-26-057406:notes:94 — heading
- 0001628280-26-057406:notes:95 — stock compensation policy unchanged
- 0001628280-26-057406:notes:96 — pre-separation stock compensation unchanged
- 0001628280-26-057406:notes:97 — heading
- 0001628280-26-057406:notes:98 — treasury policy; covered by repurchase item
- 0001628280-26-057406:notes:99 — heading
- 0001628280-26-057406:notes:100 — OCI policy unchanged
- 0001628280-26-057406:notes:101 — heading
- 0001628280-26-057406:notes:102 — derivatives; notional amounts only
- 0001628280-26-057406:notes:103 — hedge policy unchanged
- 0001628280-26-057406:notes:104 — undesignated hedge policy unchanged
- 0001628280-26-057406:notes:105 — heading
- 0001628280-26-057406:notes:106 — lease policy unchanged
- 0001628280-26-057406:notes:107 — duplicate of notes:37 and notes:38
- 0001628280-26-057406:notes:108 — fair-value hierarchy boilerplate
- 0001628280-26-057406:notes:109 — fair-value hierarchy boilerplate
- 0001628280-26-057406:notes:110 — fair-value hierarchy boilerplate
- 0001628280-26-057406:notes:111 — fair-value hierarchy boilerplate
- 0001628280-26-057406:notes:112 — heading
- 0001628280-26-057406:notes:114 — heading
- 0001628280-26-057406:notes:115 — pending standard; no number effect stated
- 0001628280-26-057406:notes:116 — new pending standard; impact not assessed
- 0001628280-26-057406:notes:117 — new pending standard; impact not assessed
- 0001628280-26-057406:notes:118 — new pending standard; impact not assessed
- 0001628280-26-057406:notes:119 — heading
- 0001628280-26-057406:notes:120 — end-market description; covered by renaming item
- 0001628280-26-057406:notes:121 — table lead-in
- 0001628280-26-057406:notes:122 — amounts only
- 0001628280-26-057406:notes:123 — operations description unchanged
- 0001628280-26-057406:notes:124 — amounts only
- 0001628280-26-057406:notes:125 — attribution footnote unchanged
- 0001628280-26-057406:notes:126 — heading
- 0001628280-26-057406:notes:127 — table lead-in
- 0001628280-26-057406:notes:128 — amounts only
- 0001628280-26-057406:notes:129 — heading
- 0001628280-26-057406:notes:130 — customer revenue concentration; amounts only
- 0001628280-26-057406:notes:132 — investment policy unchanged
- 0001628280-26-057406:notes:133 — heading
- 0001628280-26-057406:notes:134 — supplier concentration unchanged
- 0001628280-26-057406:notes:135 — supplier risk; contract assets nil
- 0001628280-26-057406:notes:136 — sales commissions; wording
- 0001628280-26-057406:notes:139 — covered by collateral item
- 0001628280-26-057406:notes:142 — heading
- 0001628280-26-057406:notes:143 — amounts only
- 0001628280-26-057406:notes:144 — heading
- 0001628280-26-057406:notes:145 — table lead-in
- 0001628280-26-057406:notes:146 — amounts only
- 0001628280-26-057406:notes:147 — footnote unchanged
- 0001628280-26-057406:notes:148 — goodwill origin unchanged
- 0001628280-26-057406:notes:149 — reporting unit unchanged
- 0001628280-26-057406:notes:150 — prior-year impairment narrative
- 0001628280-26-057406:notes:151 — prior-year recoverability test
- 0001628280-26-057406:notes:152 — prior-year method
- 0001628280-26-057406:notes:153 — prior-year method
- 0001628280-26-057406:notes:154 — prior-year method
- 0001628280-26-057406:notes:155 — prior-year charge
- 0001628280-26-057406:notes:156 — covered by no-goodwill-impairment item
- 0001628280-26-057406:notes:157 — heading
- 0001628280-26-057406:notes:158 — factoring history unchanged
- 0001628280-26-057406:notes:159 — prior-period factoring amounts
- 0001628280-26-057406:notes:160 — no factoring; date rolled
- 0001628280-26-057406:notes:161 — amounts only
- 0001628280-26-057406:notes:162 — covered by inventory reserve item
- 0001628280-26-057406:notes:163 — amounts only
- 0001628280-26-057406:notes:164 — heading
- 0001628280-26-057406:notes:166 — heading
- 0001628280-26-057406:notes:167 — table lead-in
- 0001628280-26-057406:notes:169 — classification lead-in
- 0001628280-26-057406:notes:170 — amounts only
- 0001628280-26-057406:notes:171 — heading
- 0001628280-26-057406:notes:172 — amounts only
- 0001628280-26-057406:notes:173 — tax indemnification; amounts only
- 0001628280-26-057406:notes:174 — heading
- 0001628280-26-057406:notes:175 — AOCL definition
- 0001628280-26-057406:notes:176 — amounts; covered by hedge item
- 0001628280-26-057406:notes:177 — amounts only
- 0001628280-26-057406:notes:178 — heading
- 0001628280-26-057406:notes:179 — table lead-in
- 0001628280-26-057406:notes:180 — amounts; Nanya Level 1 covered
- 0001628280-26-057406:notes:181 — amounts only
- 0001628280-26-057406:notes:182 — money market description unchanged
- 0001628280-26-057406:notes:184 — FX valuation unchanged
- 0001628280-26-057406:notes:185 — no level transfers; unchanged
- 0001628280-26-057406:notes:187 — amounts; hedge policy covered
- 0001628280-26-057406:notes:188 — heading
- 0001628280-26-057406:notes:189 — table lead-in
- 0001628280-26-057406:notes:190 — amounts; covered by term loan item
- 0001628280-26-057406:notes:191 — loan agreement history
- 0001628280-26-057406:notes:192 — guarantee terms unchanged
- 0001628280-26-057406:notes:193 — covenants unchanged
- 0001628280-26-057406:notes:194 — borrowing history unchanged
- 0001628280-26-057406:notes:195 — security agreement unchanged
- 0001628280-26-057406:notes:196 — guaranty unchanged
- 0001628280-26-057406:notes:197 — heading
- 0001628280-26-057406:notes:198 — term loan rate; tense only
- 0001628280-26-057406:notes:199 — amortization terms; tense only
- 0001628280-26-057406:notes:200 — covered by term loan item
- 0001628280-26-057406:notes:201 — heading
- 0001628280-26-057406:notes:202 — revolver terms unchanged
- 0001628280-26-057406:notes:203 — deferred costs unchanged
- 0001628280-26-057406:notes:204 — covenant compliance; date rolled
- 0001628280-26-057406:notes:205 — revolver capacity; date rolled
- 0001628280-26-057406:notes:206 — heading
- 0001628280-26-057406:notes:207 — amounts; garbling noted in drafting item
- 0001628280-26-057406:notes:208 — covered by segment measure item
- 0001628280-26-057406:notes:209 — covered by segment measure item
- 0001628280-26-057406:notes:210 — amounts only
- 0001628280-26-057406:notes:211 — heading
- 0001628280-26-057406:notes:212 — Flash Ventures structure unchanged
- 0001628280-26-057406:notes:213 — history unchanged
- 0001628280-26-057406:notes:214 — history unchanged
- 0001628280-26-057406:notes:215 — history unchanged
- 0001628280-26-057406:notes:216 — history unchanged
- 0001628280-26-057406:notes:217 — history unchanged
- 0001628280-26-057406:notes:218 — history unchanged
- 0001628280-26-057406:notes:219 — history unchanged
- 0001628280-26-057406:notes:222 — covered by term extension item
- 0001628280-26-057406:notes:223 — covered by term extension item
- 0001628280-26-057406:notes:226 — VIE conclusion unchanged
- 0001628280-26-057406:notes:227 — table lead-in
- 0001628280-26-057406:notes:228 — amounts only
- 0001628280-26-057406:notes:230 — loan terms unchanged
- 0001628280-26-057406:notes:231 — amounts only
- 0001628280-26-057406:notes:232 — exposure lead-in; date rolled
- 0001628280-26-057406:notes:233 — amounts only
- 0001628280-26-057406:notes:234 — cost-sharing terms unchanged
- 0001628280-26-057406:notes:235 — underutilization; amounts, wording
- 0001628280-26-057406:notes:236 — binding orders unchanged
- 0001628280-26-057406:notes:237 — R&D commitment; date rolled
- 0001628280-26-057406:notes:238 — lease guarantees unchanged
- 0001628280-26-057406:notes:239 — table lead-in; date rolled
- 0001628280-26-057406:notes:240 — amounts only
- 0001628280-26-057406:notes:241 — table lead-in; date rolled
- 0001628280-26-057406:notes:242 — amounts only
- 0001628280-26-057406:notes:243 — indemnity; date rolled
- 0001628280-26-057406:notes:244 — heading
- 0001628280-26-057406:notes:245 — SDSS history unchanged
- 0001628280-26-057406:notes:246 — SDSS history unchanged
- 0001628280-26-057406:notes:247 — SDSS installments unchanged
- 0001628280-26-057406:notes:249 — amounts; horizon wording noted in drafting item
- 0001628280-26-057406:notes:250 — amounts; line cited in equity-method item
- 0001628280-26-057406:notes:252 — immaterial transition services
- 0001628280-26-057406:notes:253 — heading
- 0001628280-26-057406:notes:254 — Unis structure unchanged
- 0001628280-26-057406:notes:255 — line cited in equity-method item
- 0001628280-26-057406:notes:256 — Unis revenue and receivable shares; amounts only
- 0001628280-26-057406:notes:257 — heading
- 0001628280-26-057406:notes:258 — heading
- 0001628280-26-057406:notes:260 — heading
- 0001628280-26-057406:notes:261 — agreements lead-in
- 0001628280-26-057406:notes:262 — separation agreement unchanged
- 0001628280-26-057406:notes:263 — covered by TSA/separation item
- 0001628280-26-057406:notes:264 — reimbursement; amounts only
- 0001628280-26-057406:notes:265 — TSA description; covered by TSA item
- 0001628280-26-057406:notes:266 — TSA amounts; covered by TSA item
- 0001628280-26-057406:notes:267 — tax matters agreement unchanged
- 0001628280-26-057406:notes:268 — amounts only
- 0001628280-26-057406:notes:269 — heading
- 0001628280-26-057406:notes:270 — pre-separation history
- 0001628280-26-057406:notes:271 — pre-separation history
- 0001628280-26-057406:notes:272 — table lead-in
- 0001628280-26-057406:notes:273 — amounts only
- 0001628280-26-057406:notes:274 — heading
- 0001628280-26-057406:notes:275 — allocation history
- 0001628280-26-057406:notes:276 — allocation history
- 0001628280-26-057406:notes:277 — table lead-in
- 0001628280-26-057406:notes:278 — amounts only
- 0001628280-26-057406:notes:279 — historical caveat; wording
- 0001628280-26-057406:notes:280 — heading
- 0001628280-26-057406:notes:281 — cash management history
- 0001628280-26-057406:notes:282 — heading
- 0001628280-26-057406:notes:283 — net investment history
- 0001628280-26-057406:notes:284 — heading
- 0001628280-26-057406:notes:285 — table lead-in
- 0001628280-26-057406:notes:286 — amounts only
- 0001628280-26-057406:notes:287 — heading
- 0001628280-26-057406:notes:288 — leases; wording (datacenter space)
- 0001628280-26-057406:notes:289 — lease policy unchanged
- 0001628280-26-057406:notes:290 — table lead-in
- 0001628280-26-057406:notes:291 — amounts only
- 0001628280-26-057406:notes:292 — table lead-in
- 0001628280-26-057406:notes:293 — amounts only
- 0001628280-26-057406:notes:294 — table lead-in
- 0001628280-26-057406:notes:295 — amounts only
- 0001628280-26-057406:notes:296 — table lead-in
- 0001628280-26-057406:notes:297 — amounts only
- 0001628280-26-057406:notes:298 — heading
- 0001628280-26-057406:notes:299 — sale-leaseback history
- 0001628280-26-057406:notes:300 — sale-leaseback terms unchanged
- 0001628280-26-057406:notes:301 — heading
- 0001628280-26-057406:notes:302 — purchase-order boilerplate
- 0001628280-26-057406:notes:303 — covered by Nanya items
- 0001628280-26-057406:notes:306 — covered by Nanya supply item
- 0001628280-26-057406:notes:307 — table lead-in
- 0001628280-26-057406:notes:308 — amounts only
- 0001628280-26-057406:notes:309 — equity plan history
- 0001628280-26-057406:notes:310 — conversion expense; amounts only
- 0001628280-26-057406:notes:311 — plan adoption history
- 0001628280-26-057406:notes:312 — plan description unchanged
- 0001628280-26-057406:notes:313 — heading
- 0001628280-26-057406:notes:314 — plan terms unchanged
- 0001628280-26-057406:notes:315 — share authorization; amounts only
- 0001628280-26-057406:notes:316 — heading
- 0001628280-26-057406:notes:317 — ESPP terms unchanged
- 0001628280-26-057406:notes:318 — ESPP periods unchanged
- 0001628280-26-057406:notes:319 — amounts only
- 0001628280-26-057406:notes:320 — table lead-in
- 0001628280-26-057406:notes:321 — amounts only
- 0001628280-26-057406:notes:322 — amounts only
- 0001628280-26-057406:notes:323 — windfall boilerplate
- 0001628280-26-057406:notes:324 — table lead-in
- 0001628280-26-057406:notes:325 — amounts only
- 0001628280-26-057406:notes:326 — heading
- 0001628280-26-057406:notes:327 — table lead-in
- 0001628280-26-057406:notes:328 — amounts only
- 0001628280-26-057406:notes:329 — amounts; garbling noted in drafting item
- 0001628280-26-057406:notes:330 — PSU terms; amounts
- 0001628280-26-057406:notes:331 — heading
- 0001628280-26-057406:notes:332 — heading
- 0001628280-26-057406:notes:333 — valuation method unchanged
- 0001628280-26-057406:notes:334 — heading
- 0001628280-26-057406:notes:335 — ESPP valuation unchanged
- 0001628280-26-057406:notes:336 — table lead-in
- 0001628280-26-057406:notes:337 — amounts only
- 0001628280-26-057406:notes:338 — heading
- 0001628280-26-057406:notes:340 — EPS share basis unchanged
- 0001628280-26-057406:notes:341 — table lead-in
- 0001628280-26-057406:notes:342 — amounts only
- 0001628280-26-057406:notes:343 — anti-dilution; amounts only
- 0001628280-26-057406:notes:344 — prior-year net loss footnote
- 0001628280-26-057406:notes:345 — EPS method unchanged
- 0001628280-26-057406:notes:346 — EPS method unchanged
- 0001628280-26-057406:notes:347 — heading
- 0001628280-26-057406:notes:348 — table lead-in
- 0001628280-26-057406:notes:349 — amounts only
- 0001628280-26-057406:notes:350 — heading
- 0001628280-26-057406:notes:351 — table lead-in
- 0001628280-26-057406:notes:352 — amounts only
- 0001628280-26-057406:notes:353 — covered by foreign tax rate item
- 0001628280-26-057406:notes:354 — covered by minimum tax item
- 0001628280-26-057406:notes:355 — covered by Pillar Two item
- 0001628280-26-057406:notes:356 — table lead-in
- 0001628280-26-057406:notes:357 — amounts only
- 0001628280-26-057406:notes:358 — duplicate of mdna:75; covered
- 0001628280-26-057406:notes:359 — prior-year rate drivers
- 0001628280-26-057406:notes:360 — prior-year rate drivers
- 0001628280-26-057406:notes:361 — heading
- 0001628280-26-057406:notes:362 — table lead-in
- 0001628280-26-057406:notes:363 — amounts; covered by deferred tax item
- 0001628280-26-057406:notes:365 — permanent reinvestment unchanged
- 0001628280-26-057406:notes:366 — heading
- 0001628280-26-057406:notes:367 — covered by tax disclosure standard item
- 0001628280-26-057406:notes:368 — heading
- 0001628280-26-057406:notes:369 — table lead-in
- 0001628280-26-057406:notes:370 — amounts; new format covered
- 0001628280-26-057406:notes:371 — state tax footnote; new format
- 0001628280-26-057406:notes:372 — definition footnote; new format
- 0001628280-26-057406:notes:373 — table lead-in
- 0001628280-26-057406:notes:374 — prior-year amounts
- 0001628280-26-057406:notes:375 — table lead-in
- 0001628280-26-057406:notes:376 — amounts; new format covered
- 0001628280-26-057406:notes:377 — heading
- 0001628280-26-057406:notes:378 — covered by tax holiday item
- 0001628280-26-057406:notes:379 — amounts; covered by tax holiday item
- 0001628280-26-057406:notes:380 — amounts only
- 0001628280-26-057406:notes:381 — amounts; cited in deferred tax item
- 0001628280-26-057406:notes:382 — heading
- 0001628280-26-057406:notes:383 — presentation policy unchanged
- 0001628280-26-057406:notes:384 — table lead-in
- 0001628280-26-057406:notes:385 — amounts; covered by unrecognized tax benefits item
- 0001628280-26-057406:notes:387 — examination years unchanged
- 0001628280-26-057406:notes:388 — examination boilerplate
- 0001628280-26-057406:notes:390 — summarized-information lead-in
- 0001628280-26-057406:notes:391 — investee history unchanged
- 0001628280-26-057406:notes:392 — scope note unchanged
- 0001628280-26-057406:notes:393 — table lead-in
- 0001628280-26-057406:notes:394 — amounts only
- 0001628280-26-057406:notes:395 — amounts only
- 0001628280-26-057406:notes:396 — heading
- 0001628280-26-057406:notes:397 — covered by share repurchase item
- 0001628280-26-057406:notes:399 — covered by executive trading plans item
- 0001628280-26-057406:notes:400 — covered by executive trading plans item

### 8-K (Item 2.02, exhibit 99.1)
- 0001628280-26-053346:8k_2_02:1 — exhibit header
- 0001628280-26-053346:8k_2_02:2 — header
- 0001628280-26-053346:8k_2_02:3 — header
- 0001628280-26-053346:8k_2_02:4 — headline
- 0001628280-26-053346:8k_2_02:5 — heading
- 0001628280-26-053346:8k_2_02:7 — covered by pricing-led growth item
- 0001628280-26-053346:8k_2_02:9 — covered by share repurchase item
- 0001628280-26-053346:8k_2_02:11 — dateline
- 0001628280-26-053346:8k_2_02:12 — promotional CEO quote
- 0001628280-26-053346:8k_2_02:13 — page number
- 0001628280-26-053346:8k_2_02:14 — heading
- 0001628280-26-053346:8k_2_02:15 — amounts only
- 0001628280-26-053346:8k_2_02:16 — amounts only
- 0001628280-26-053346:8k_2_02:17 — footnote
- 0001628280-26-053346:8k_2_02:18 — heading
- 0001628280-26-053346:8k_2_02:19 — amounts only
- 0001628280-26-053346:8k_2_02:20 — footnote
- 0001628280-26-053346:8k_2_02:21 — heading
- 0001628280-26-053346:8k_2_02:22 — amounts; Consumer decline cited in consumer item
- 0001628280-26-053346:8k_2_02:23 — footnote
- 0001628280-26-053346:8k_2_02:24 — amounts only
- 0001628280-26-053346:8k_2_02:25 — presentation reference
- 0001628280-26-053346:8k_2_02:26 — page number
- 0001628280-26-053346:8k_2_02:27 — heading
- 0001628280-26-053346:8k_2_02:28 — amounts; covered by guidance item
- 0001628280-26-053346:8k_2_02:29 — guidance reconciliation boilerplate
- 0001628280-26-053346:8k_2_02:30 — tax guidance boilerplate
- 0001628280-26-053346:8k_2_02:31 — page number
- 0001628280-26-053346:8k_2_02:32 — heading
- 0001628280-26-053346:8k_2_02:33 — separation history
- 0001628280-26-053346:8k_2_02:34 — basis of presentation unchanged
- 0001628280-26-053346:8k_2_02:35 — heading
- 0001628280-26-053346:8k_2_02:36 — call logistics
- 0001628280-26-053346:8k_2_02:37 — heading
- 0001628280-26-053346:8k_2_02:38 — company description boilerplate
- 0001628280-26-053346:8k_2_02:39 — page number
- 0001628280-26-053346:8k_2_02:40 — heading
- 0001628280-26-053346:8k_2_02:41 — separator
- 0001628280-26-053346:8k_2_02:42 — trademark boilerplate
- 0001628280-26-053346:8k_2_02:43 — page number
- 0001628280-26-053346:8k_2_02:44 — header
- 0001628280-26-053346:8k_2_02:45 — header
- 0001628280-26-053346:8k_2_02:46 — header
- 0001628280-26-053346:8k_2_02:47 — amounts only
- 0001628280-26-053346:8k_2_02:48 — page number
- 0001628280-26-053346:8k_2_02:49 — header
- 0001628280-26-053346:8k_2_02:50 — header
- 0001628280-26-053346:8k_2_02:51 — header
- 0001628280-26-053346:8k_2_02:52 — amounts only
- 0001628280-26-053346:8k_2_02:53 — page number
- 0001628280-26-053346:8k_2_02:54 — header
- 0001628280-26-053346:8k_2_02:55 — header
- 0001628280-26-053346:8k_2_02:56 — header
- 0001628280-26-053346:8k_2_02:57 — amounts only
- 0001628280-26-053346:8k_2_02:58 — page number
- 0001628280-26-053346:8k_2_02:59 — header
- 0001628280-26-053346:8k_2_02:60 — header
- 0001628280-26-053346:8k_2_02:61 — header
- 0001628280-26-053346:8k_2_02:62 — amounts only
- 0001628280-26-053346:8k_2_02:63 — page number
- 0001628280-26-053346:8k_2_02:64 — header
- 0001628280-26-053346:8k_2_02:65 — header
- 0001628280-26-053346:8k_2_02:66 — header
- 0001628280-26-053346:8k_2_02:67 — amounts; adjusted FCF line covered
- 0001628280-26-053346:8k_2_02:68 — page number
- 0001628280-26-053346:8k_2_02:69 — non-GAAP rationale; exclusions covered
- 0001628280-26-053346:8k_2_02:70 — lead-in
- 0001628280-26-053346:8k_2_02:71 — prior-year impairment rationale
- 0001628280-26-053346:8k_2_02:72 — stock compensation rationale unchanged
- 0001628280-26-053346:8k_2_02:73 — page number
- 0001628280-26-053346:8k_2_02:74 — separation costs rationale unchanged
- 0001628280-26-053346:8k_2_02:75 — restructuring rationale unchanged
- 0001628280-26-053346:8k_2_02:76 — covered by SDSS amendment item
- 0001628280-26-053346:8k_2_02:77 — covered by term loan item
- 0001628280-26-053346:8k_2_02:80 — tax adjustment rationale; wording
- 0001628280-26-053346:8k_2_02:82 — margin definitions
- 0001628280-26-053346:8k_2_02:83 — contacts
- 0001628280-26-053346:8k_2_02:84 — page number
