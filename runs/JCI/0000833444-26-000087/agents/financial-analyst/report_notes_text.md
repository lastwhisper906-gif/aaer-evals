<!-- the quote gate removed 3 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes-text reader: JCI 10-Q 0000833444-26-000087 (quarter ended June 30, 2026)

Prior period of the same kind: 0000833444-26-000050 (quarter ended March 31, 2026, filed 2026-05-06).

## Input check

- **Files read in full:** input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- **Nothing out of scope is present.** There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no earlier run's probabilities and no outcome window. The 8-K exhibit 99.1 body contains the company's own condensed statements and non-GAAP tables. I read those as 8-K text and computed nothing from them.
- **Missing from my directory although my brief lists them:**
  - An auditor's report. input_controls.md carries Item 4 only.
  - An Item 1A diff, an Exhibit 21 diff and any Exhibit 10.
  - MD&A says risk factors were updated in Part II, Item 1A. I cannot read that update, so it is recorded as insufficient below.
- **Prior predictions:** none on record. There are no earlier flags to carry forward.
- **No arithmetic was done.** Where two figures appear together in an item, I am quoting what the text states. Whether they reconcile is for the numbers reader.

## Items

```json
[
{
    "id": "articulation_and_the_filed_history_cash_flow_debt_gross_presentation_revision",
    "what_changed": "The prior-period revision note now covers the nine months ended June 30, 2025. Proceeds from and repayments of debt for certain short-term debt transactions had been shown net and are now presented gross. The prior 10-Q revised only the six months ended March 31, 2025 and said a similar revision for the nine months would appear in this 10-Q; that revision is now made. The note says financing cash flow totals and the change in cash are unchanged and that the error is not material. Item 4 in the same filing still reports disclosure controls effective and no significant change in internal control during the quarter.",
    "account": "proceeds from debt; repayments of debt (prior-year comparative financing cash flows)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "have been revised for certain short-term debt transactions that occurred in the nine months ended June 30, 2025 and were incorrectly presented on a net basis",
    "paragraph_id": "0000833444-26-000087:notes:8",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_alloy_enterprises_and_nantum_acquisitions_goodwill",
    "what_changed": "New paragraph. In the third quarter the Company closed two acquisitions: Alloy Enterprises (direct liquid cooling components) and Nantum AI (OpenBlue digital ecosystem). Total consideration, net of cash acquired, was approximately $291 million, 'a meaningful component' of which related to Alloy. Both businesses report in Americas. Goodwill of $193 million was recorded, attributed primarily to expected synergies. The goodwill roll-forward now has an Acquisitions row (notes:52), and MD&A cites the acquisitions in investing cash flow (mdna:100).",
    "account": "goodwill; acquisitions of businesses (investing cash flow)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In connection with the acquisitions, the Company recorded goodwill of $193 million, primarily related to the expected synergies from combining the operations into our business",
    "paragraph_id": "0000833444-26-000087:notes:17",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_acquired_developed_technology_fifteen_year_life",
    "what_changed": "New disclosure: $127 million of definite-lived intangible assets from the two acquisitions are developed technology, amortized straight-line over 15 years. Both the useful life and the split between goodwill and developed technology are management estimates. No other intangible category is named for these deals. The text implies new amortization expense from the acquisition dates.",
    "account": "other intangible assets - net; amortization of intangible assets",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "$127 million of definite-lived intangible assets related to developed technology being amortized on a straight-line basis over 15 years",
    "paragraph_id": "0000833444-26-000087:notes:17",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_adt_united_kingdom_residential_held_for_sale",
    "what_changed": "New. During the third quarter the Company signed a definitive agreement to sell its ADT United Kingdom Residential Security business. The business is classified as held for sale but not as a discontinued operation, and the sale is expected to close in fiscal 2027. At June 30, 2026, $229 million of assets and $39 million of liabilities are presented as held for sale. The text does not name the segment.",
    "account": "assets and liabilities held for sale",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the Company signed a definitive agreement to sell its ADT United Kingdom Residential Security business and determined that it met the criteria to be classified as held for sale",
    "paragraph_id": "0000833444-26-000087:notes:20",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_adt_united_kingdom_fair_value_exceeds_carrying_value",
    "what_changed": "New statement: at June 30, 2026 the estimated fair value less costs to sell of the ADT United Kingdom disposal group exceeded its carrying value, so no write-down was recorded. This is a management fair-value judgment. The ADT Spain disposal group, by contrast, was written down in the first quarter (notes:23).",
    "account": "restructuring and impairment costs; assets held for sale",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the estimated fair value less costs to sell of the held for sale business exceeded its carrying value, and therefore, no adjustment was necessary",
    "paragraph_id": "0000833444-26-000087:notes:21",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_adt_spain_sale_completed",
    "what_changed": "New. The ADT Spain Security sale was completed on April 1, 2026 for net proceeds of $98 million, with no gain or loss recorded. The text repeats that a $50 million non-cash impairment was recorded in the first quarter. MD&A cites ADT Spain proceeds in investing cash flow (mdna:100).",
    "account": "assets held for sale; divestitures of businesses (investing cash flow)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "On April 1, 2026, the Company completed the sale of its ADT Spain Security business for net proceeds of $98 million, with no gain or loss recorded on the transaction",
    "paragraph_id": "0000833444-26-000087:notes:23",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_rlc_hvac_final_purchase_price_adjustment_paid",
    "what_changed": "New sentence: in the three months ended June 30, 2026 the Company paid approximately $155 million of final purchase price adjustments on the July 2025 sale of the R&LC HVAC business to the Bosch Group. The text calls these adjustments final.",
    "account": "cash used by investing activities of discontinued operations",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the Company paid approximately $155 million related to final purchase price adjustments associated with the sale of the R&LC HVAC business to the Bosch Group",
    "paragraph_id": "0000833444-26-000087:notes:32",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_goodwill_allocated_to_adt_united_kingdom_disposal_group",
    "what_changed": "The goodwill roll-forward footnote now says the 'foreign currency translation and other' line includes $102 million of goodwill allocated to the ADT United Kingdom Residential Security disposal group, alongside $38 million for ADT Spain. Allocating goodwill to a disposal group is a management estimate, and the allocated goodwill moves into held-for-sale assets.",
    "account": "goodwill",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Includes the allocation of goodwill to the ADT Spain Security business and the ADT United Kingdom Residential Security business disposal groups of $38 million and $102 million, respectively",
    "paragraph_id": "0000833444-26-000087:notes:53",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_yen_net_investment_hedge_no_longer_designated",
    "what_changed": "At June 30, 2026 the net investment hedge paragraph names only €2.9 billion of euro-denominated debt as partial hedges. At September 30, 2025 the designation also included ¥30 billion of yen-denominated obligations (notes:81). The text gives no reason the yen designation is no longer listed. My input does not show whether the March 31, 2026 text still listed it.",
    "account": "accumulated other comprehensive income (CTA); net financing charges (FX results)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, the Company had designated debt obligations of €2.9 billion as partial hedges of its investments in certain euro-denominated subsidiaries",
    "paragraph_id": "0000833444-26-000087:notes:80",
    "explanation": false
  },
{
    "id": "earnings_quality_quarter_effective_tax_rate_above_statutory",
    "what_changed": "Explanation for the new period. The third-quarter effective tax rate of 18.0% is described as higher than the 12.5% statutory rate, primarily because of tax rate differentials, partly offset by global tax planning. The prior-year quarter's 12.3% is described as lower than statutory (notes:112). The earnings release (8k_2_02:164) gives an adjusted rate of approximately 17% for the three and nine months of 2026 and approximately 12% for 2025.",
    "account": "income tax provision",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "was higher than the statutory tax rate of 12.5% primarily due to tax rate differentials",
    "paragraph_id": "0000833444-26-000087:notes:110",
    "explanation": false
  },
{
    "id": "earnings_quality_tax_impact_of_planned_divestitures",
    "what_changed": "The nine-month effective tax rate explanation lists the reasons the rate exceeds statutory. They include the tax impact of the water systems AFFF insurance proceeds and 'the tax impact of current and planned divestitures'. In the current text the planned divestiture is the ADT United Kingdom business, classified as held for sale this quarter. My input does not show the prior-quarter wording, so I cannot confirm that 'planned' is new.",
    "account": "income tax provision",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "the tax impact of current and planned divestitures",
    "paragraph_id": "0000833444-26-000087:notes:111",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_epa_rcra_withdrawal_and_mcl_rescission_proposal",
    "what_changed": "The PFAS regulatory paragraph is updated. EPA withdrew the second proposed RCRA rule, which would have broadened hazardous waste to substances meeting the statutory definition, on May 8, 2026. The first RCRA rule, listing nine PFAS as hazardous constituents, 'has not been finalized'. OMB completed its review of a proposed rule to rescind the Maximum Contaminant Levels for PFHxS, PFNA, HFPO-DA and PFBS on May 1, 2026. That rule was published in the Federal Register on May 20, 2026 and is not final. The prior text said only that the rescission proposal had been sent to OMB in February 2026.",
    "account": "environmental reserves; AFFF contingencies",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "however, the EPA withdrew that proposal on May 8, 2026",
    "paragraph_id": "0000833444-26-000087:notes:147",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_wdnr_draft_rule_adopting_federal_pfas_limits",
    "what_changed": "New sentence: in June 2026 the Wisconsin Department of Natural Resources issued a draft rulemaking to adopt the April 2024 federal Maximum Contaminant Levels and Hazard Index standards as Wisconsin law. The FTC and Stanton Street remediation sites are in Wisconsin. The text implies the limits would stay in force there even if the federal rescission proposal is finalized.",
    "account": "environmental reserves (FTC and Marinette remediation)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In June 2026, the Wisconsin Department of Natural Resources issued a draft rulemaking to adopt as a matter of Wisconsin law the Maximum Contaminant Levels and Hazard Index standards established in the April 2024 NPDWR",
    "paragraph_id": "0000833444-26-000087:notes:147",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_wisconsin_pfas_drinking_water_standards_approved",
    "what_changed": "In January 2026 the Natural Resources Board approved Wisconsin drinking water standards: 4 ng/L for PFOA and PFOS, and 10 ng/L for PFHxS, PFNA and HFPO-DA. The text now says these standards were 'subsequently approved through the state rulemaking process in 2026'. The prior text said they were still subject to further reviews and approvals before becoming final.",
    "account": "environmental reserves",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The standards were subsequently approved through the state rulemaking process in 2026",
    "paragraph_id": "0000833444-26-000087:notes:156",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_wdnr_penalty_uncertainty_sentence_removed",
    "what_changed": "A sentence was removed from the paragraph on the WDNR Notices of Noncompliance (now notes:157). It said the Company cannot predict what regulatory or enforcement actions, including penalties, might follow from WDNR's actions. The paragraph now ends with the companies' belief that they complied with applicable laws. The removal comes with the Stipulation for Judgment that resolved the State enforcement action (notes:158).",
    "account": "environmental contingencies (penalties)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The Company cannot predict what regulatory or enforcement actions, if any, might result from the WDNR",
    "paragraph_id": "0000833444-26-000050:note_history:6",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_wisconsin_doj_enforcement_action_resolved",
    "what_changed": "The Wisconsin DOJ civil enforcement action over the FTC is resolved. On June 4, 2026 the State filed a Stipulation for Judgment. Under it, Tyco Fire Products paid $10 million to a statewide PFAS fund and will continue its ongoing remediation in Marinette and Peshtigo: running the GETS, monitoring water quality and completing PFAS-free deep drinking water wells. Johnson Controls, Inc. was dismissed with prejudice on June 5, 2026. The prior text said WDOJ sought monetary penalties and an injunction, and that the parties were working toward a settlement. The text does not say whether the $10 million was previously accrued or where it was charged.",
    "account": "environmental reserves; selling, general and administrative expenses",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "On June 4, 2026, the State filed a Stipulation for Judgment, resolving the litigation",
    "paragraph_id": "0000833444-26-000087:notes:158",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_water_systems_settlement_exclusion_detail_trimmed",
    "what_changed": "The paragraph on the water systems settlement class is shortened. Two lists were removed: the excluded systems (State- or U.S.-owned systems, systems without PFAS detection as of May 15, 2024, small transient systems, private wells and the City of Marinette system) and the other MDL categories the settlement does not affect (personal injury, property damage, other class actions, state or territory attorney general claims). The opt-out wording changed from systems that 'request exclusion' under a process 'to be established by the MDL court' to systems that 'requested exclusion', so the opt-out is now in the past tense. The no-estimate conclusion is unchanged.",
    "account": "AFFF contingencies (unaccrued)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Certain systems are excluded from the settlement class and the settlement does not resolve claims of public water systems that requested exclusion from the class",
    "paragraph_id": "0000833444-26-000087:notes:172",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_val_d_or_proceeding_names_parent",
    "what_changed": "New. Tyco Fire Products and the parent, Johnson Controls International plc, are named with other manufacturers in an individual proceeding in Quebec. The City of Val D'Or brought it over PFAS contamination of well water from firefighting training at Val D'Or airport (continued in notes:176). The description of the Canadian class actions now also lists indigenous communities among the classes.",
    "account": "AFFF contingencies (unaccrued)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Tyco Fire Products and Johnson Controls International plc have also been named, among other manufacturers, in an individual proceeding in Quebec commenced by the City of Val",
    "paragraph_id": "0000833444-26-000087:notes:175",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_belgium_afff_proceedings_count",
    "what_changed": "The text now says five AFFF property damage proceedings have been filed in Belgium against an affiliate and others; the prior text said four. The cases are still on hold pending efforts to dismiss.",
    "account": "AFFF contingencies (unaccrued)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Five AFFF property damage proceedings have been filed in Belgium against numerous defendants",
    "paragraph_id": "0000833444-26-000087:notes:193",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_environmental_asset_retirement_obligation_sentence_removed",
    "what_changed": "A sentence was removed from the environmental section. It disclosed conditional asset retirement obligations for environmental matters at owned facilities, with an amount at March 31, 2026 and September 30, 2025. The current notes have no replacement sentence, so no June 30, 2026 amount appears in my input.",
    "account": "asset retirement obligations (other liabilities)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Conditional asset retirement obligations were $7 million at both March 31, 2026 and September 30, 2025",
    "paragraph_id": "0000833444-26-000050:note_history:22",
    "explanation": false
  },
{
    "id": "earnings_quality_ieepa_tariff_refund_process",
    "what_changed": "The tariff paragraph says the U.S. Supreme Court invalidated certain IEEPA tariffs in February 2026 and that the United States has since imposed new tariffs and duties in their place. It says the Company is participating in the IEEPA refund process, and that tariffs and refunds claimed have had no material impact to date. My input does not show the prior-quarter wording, so I cannot confirm which sentence is new. Any refund recognized later would be a non-recurring benefit, most plausibly to cost of sales.",
    "account": "cost of sales",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company is participating in the IEEPA refund process",
    "paragraph_id": "0000833444-26-000087:mdna:12",
    "explanation": false
  },
{
    "id": "narrative_signs_of_operating_pressure_middle_east_energy_and_supply_costs",
    "what_changed": "The geopolitical paragraph says the ongoing Middle East conflicts have disrupted energy supplies and supply chains, increased costs for energy and other supplies, and created capital-market volatility. It says the net effect depends on the Company's ability to mitigate and offset these impacts. The mitigation paragraph (mdna:14) now covers 'trade restrictions and geopolitical conflict'. The prior wording is not in my input.",
    "account": "cost of sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The ongoing conflicts in the Middle East have disrupted energy supplies and supply chains, increased costs for energy and other supplies and created volatility in the capital markets",
    "paragraph_id": "0000833444-26-000087:mdna:13",
    "explanation": false
  },
{
    "id": "revenue_recognition_change_orders_asserting_contractual_rights",
    "what_changed": "The listed mitigation actions include in-region-for-region manufacturing, local sourcing, and 'accelerating pricing actions and asserting contractual rights through change orders'. Recovering costs through change orders on long-cycle contracts involves contract modifications and variable consideration. When revenue and contract assets are recognized then depends on management's judgment about whether the change orders are approved. The prior wording is not in my input, so I cannot confirm that change orders are newly cited.",
    "account": "net sales; contract assets (in accounts receivable - net)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "accelerating pricing actions and asserting contractual rights through change orders",
    "paragraph_id": "0000833444-26-000087:mdna:14",
    "explanation": false
  },
{
    "id": "earnings_quality_sga_decrease_attributed_to_afff_insurance_recoveries",
    "what_changed": "MD&A attributes the quarter's SG&A decrease primarily to AFFF insurance recoveries related to the water systems settlement ($16 million). It names no operating driver for the quarter. The nine-month paragraph (mdna:31) names AFFF recoveries ($135 million), the ADT Mexico divestiture gain ($70 million) and ongoing cost actions. These are non-operating credits booked inside SG&A, and the contingency note says the amount and timing of future recoveries cannot be predicted.",
    "account": "selling, general and administrative expenses",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in SG&A for the three months ended June 30, 2026 was primarily due to AFFF insurance recoveries related to the previously disclosed water systems settlement ($16 million)",
    "paragraph_id": "0000833444-26-000087:mdna:30",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_quarter_other_impairments_without_new_explanation",
    "what_changed": "MD&A refers readers to Note 3 (acquisitions and divestitures) and Note 14 (restructuring) for impairment costs. The restructuring and impairment table (mdna:36) shows an 'Other impairments' line for the quarter. The only new impairment prose in my input is in Note 3: the ADT Spain charge recorded in the first quarter, and no adjustment for ADT United Kingdom. The Note 14 paragraphs are unchanged from the prior period. In my input, then, no new text explains the quarter's other impairments.",
    "account": "restructuring and impairment costs",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "restructuring actions and impairment costs",
    "paragraph_id": "0000833444-26-000087:mdna:37",
    "explanation": false
  },
{
    "id": "narrative_signs_of_operating_pressure_emea_growth_constrained_by_middle_east",
    "what_changed": "MD&A says EMEA's quarterly organic growth was 'constrained by continued pressure in the region due to the conflicts in the Middle East', and attributes the reported decline to divestitures. The nine-month paragraph (mdna:58) and the earnings release (8k_2_02:29) say the same. The word 'continued' marks the pressure as ongoing.",
    "account": "net sales (EMEA)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "as growth was constrained by continued pressure in the region due to the conflicts in the Middle East",
    "paragraph_id": "0000833444-26-000087:mdna:54",
    "explanation": false
  },
{
    "id": "earnings_quality_emea_margin_attributed_to_pricing",
    "what_changed": "MD&A attributes the quarter's EMEA Segment EBIT increase primarily to favorable pricing and productivity improvements, partly offset by divestitures. In the same document, EMEA sales growth is described as constrained by the Middle East conflicts (mdna:54). The release says the same (8k_2_02:31). A margin gain explained by price rather than volume holds only as long as the pricing does.",
    "account": "Segment EBIT (EMEA)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in EMEA was primarily driven by favorable pricing and productivity improvements, partially offset by the impact of business divestitures",
    "paragraph_id": "0000833444-26-000087:mdna:65",
    "explanation": false
  },
{
    "id": "results_against_expectations_orders_growth_data_center_projects",
    "what_changed": "MD&A says orders increased 27%, reflecting sustained demand in large projects across core markets, including large-scale data center projects. The release ties Americas orders and backlog to data centers and other mission-critical environments (8k_2_02:24). The orders definition changed in fiscal 2026; see structure_and_disclosure_changes_orders_definition_equipment_only_sales.",
    "account": "net sales (orders as a leading indicator)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Orders increased 27%, reflecting sustained demand in large projects",
    "paragraph_id": "0000833444-26-000087:mdna:80",
    "explanation": false
  },
{
    "id": "results_against_expectations_backlog_growth_led_by_products_and_systems",
    "what_changed": "MD&A says backlog increased 32%, reflecting sustained orders growth, led by Products and Systems. The backlog table and the release state backlog at $21.0 billion. The release says backlog has been restated to include the new equipment-only order category.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Backlog increased 32%, reflecting sustained orders growth and led by growth in Products and Systems",
    "paragraph_id": "0000833444-26-000087:mdna:85",
    "explanation": false
  },
{
    "id": "narrative_signs_of_operating_pressure_americas_services_backlog_decrease",
    "what_changed": "MD&A says Americas backlog growth was led by 47% growth in Products and Systems, 'partially offset by a 1% decrease in Services'. Americas Services orders are described as growing 4% (mdna:81) and APAC Services orders 1% (mdna:83). A decrease in services backlog, stated in the prose, points to pressure on future Americas service revenue. Management elsewhere says it is focused on growing services and recurring revenue (mdna:17).",
    "account": "net sales - services (Americas)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "led by 47% growth in Products and Systems, partially offset by a 1% decrease in Services",
    "paragraph_id": "0000833444-26-000087:mdna:86",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_working_capital_drivers_receivables_and_deferred_revenue",
    "what_changed": "MD&A explains the change in working capital since September 30, 2025. It cites increases in cash and accounts receivable and decreases in accrued compensation and the current portion of long-term debt, partly offset by increases in deferred revenue and accounts payable. The prose states that receivables increased but gives no cause. Whether the stated movements match the balance sheet is for the numbers reader.",
    "account": "accounts receivable - net; deferred revenue; accounts payable; accrued compensation and benefits",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to increases in cash and accounts receivable and decreases in accrued compensation and the current portion of long-term debt",
    "paragraph_id": "0000833444-26-000087:mdna:96",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_capital_expenditures_decrease_cited",
    "what_changed": "MD&A attributes the change in investing cash flows primarily to two things: proceeds from the ADT Mexico and ADT Spain divestitures, and 'a decrease in capital expenditures'. These are partly offset by the Alloy Enterprises and Nantum AI acquisitions. The ADT Spain proceeds and the two acquisitions are new this quarter (notes:17, notes:23).",
    "account": "capital expenditures",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "and a decrease in capital expenditures",
    "paragraph_id": "0000833444-26-000087:mdna:100",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_open_market_share_repurchases_resumed",
    "what_changed": "MD&A says the accelerated share repurchase was completed in the second quarter and that the Company 'resumed open market repurchases after final settlement of the ASR transactions'. It states that $5.0 billion was invested to repurchase 43,693,817 shares at an average of $114.43 per share. Approximately $3.9 billion remains under an authorization with no expiration date.",
    "account": "stock repurchases; weighted average shares outstanding",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "resumed open market repurchases after final settlement of the ASR transactions",
    "paragraph_id": "0000833444-26-000087:mdna:105",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_orders_definition_equipment_only_sales",
    "what_changed": "The release says orders before Q1 fiscal 2026 exclude certain equipment-only sales for longer-cycle projects, and that backlog has been restated to include this new category. Orders were not restated. The year-over-year orders comparisons (27% total, 37% Americas) therefore set a current period that includes the category against a prior-year quarter that excludes it. That flatters reported orders growth until the comparison base also includes the category. The text does not give the size of the category.",
    "account": "orders (non-GAAP metric)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Orders prior to Q1 2026 exclude certain equipment-only sales for longer cycle projects. Backlog has been restated to include this new category.",
    "paragraph_id": "0000833444-26-000083:8k_2_02:18",
    "explanation": false
  },
{
    "id": "across_documents_incentive_compensation_accruals_against_accrued_compensation_decrease",
    "what_changed": "The release attributes the year-over-year increase in adjusted Corporate expense primarily to increased corporate accruals for incentive compensation and to the timing of certain corporate expenses. MD&A lists a decrease in accrued compensation among the working capital movements since September 30, 2025 (mdna:96). The two statements cover different periods: the quarter, and the fiscal year to date. Reconciling them is for the supervisor. 'Timing' implies part of the expense moves between quarters.",
    "account": "corporate expense; accrued compensation and benefits",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase year-over-year is primarily due to increased corporate accruals related to incentive compensation and the timing of certain corporate expenses",
    "paragraph_id": "0000833444-26-000083:8k_2_02:40",
    "explanation": false
  },
{
    "id": "results_against_expectations_fourth_quarter_guidance_initiated",
    "what_changed": "The release initiates fiscal fourth-quarter guidance for continuing operations: organic sales growth of 9% to 10%, operating leverage of 45% to 50%, and adjusted EPS of about $1.55 (8k_2_02:47 to 8k_2_02:49).",
    "account": "net sales; adjusted EPS (non-GAAP)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The Company initiated fiscal 2026 fourth quarter continuing operations guidance",
    "paragraph_id": "0000833444-26-000083:8k_2_02:46",
    "explanation": false
  },
{
    "id": "results_against_expectations_full_year_organic_sales_guidance_raised",
    "what_changed": "Full-year organic sales growth guidance is now about 8%. The release shows the previous guidance as 'previously up ~6%' and its headline says guidance was raised.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Organic sales growth of ~8% (previously up ~6%)",
    "paragraph_id": "0000833444-26-000083:8k_2_02:51",
    "explanation": false
  },
{
    "id": "results_against_expectations_full_year_operating_leverage_guidance_restated",
    "what_changed": "Full-year operating leverage guidance is now 45% to 50%, shown against 'previously ~50%'. The release does not call this item raised or lowered. Where the new range sits relative to the prior figure is for the numbers reader. Operating leverage is defined on adjusted EBIT (8k_2_02:114).",
    "account": "adjusted EBIT (non-GAAP)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Operating leverage of 45% to 50% (previously ~50%)",
    "paragraph_id": "0000833444-26-000083:8k_2_02:52",
    "explanation": false
  },
{
    "id": "results_against_expectations_full_year_adjusted_eps_guidance_raised",
    "what_changed": "Full-year adjusted EPS guidance is now about $5.05, shown against 'previously ~$4.85'. The headline and the CEO quote both call the outlook raised. Adjusted EPS excludes transformation costs, restructuring and impairment, AFFF insurance recoveries, the divestiture gain and other items (8k_2_02:101 to 8k_2_02:111).",
    "account": "adjusted EPS (non-GAAP)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Adjusted EPS of ~$5.05 (previously ~$4.85)",
    "paragraph_id": "0000833444-26-000083:8k_2_02:53",
    "explanation": false
  },
{
    "id": "earnings_quality_prepaid_ip_royalties_excluded_from_adjusted_free_cash_flow",
    "what_changed": "Adjusted free cash flow excludes the prepayment of royalty fees for certain IP licensed to divested businesses. The adjusted FCF table shows an amount for the nine months and none for the quarter. The text implies the Company received cash up front for IP licensed to buyers of divested businesses, so the related royalty income will be recognized later without matching cash. My input has no prior release, so I cannot confirm when this exclusion first appeared.",
    "account": "deferred revenue or royalty income; adjusted free cash flow (non-GAAP)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Prepayment of royalty fees associated with certain IP licensed to divested businesses",
    "paragraph_id": "0000833444-26-000083:8k_2_02:96",
    "explanation": false
  },
{
    "id": "earnings_quality_discrete_tax_payments_excluded_from_adjusted_free_cash_flow",
    "what_changed": "Adjusted free cash flow excludes 'discrete tax payments', defined as non-recurring tax settlements for certain non-US jurisdictions. The table shows an amount for the nine months and none for the quarter. Excluding these cash tax settlements removes them from the non-GAAP measure. My input has no prior release, so I cannot confirm whether the definition is new this period.",
    "account": "income taxes paid; adjusted free cash flow (non-GAAP)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Discrete tax payments are non-recurring tax settlements for certain non-US jurisdictions",
    "paragraph_id": "0000833444-26-000083:8k_2_02:97",
    "explanation": false
  },
{
    "id": "earnings_quality_transformation_costs_excluded_from_adjusted_measures",
    "what_changed": "Transformation costs are defined as incremental expenses for strategic growth initiatives and cost-saving opportunities tied to portfolio simplification and the lifecycle solutions strategy. They are excluded from adjusted EBIT, adjusted EPS and adjusted Corporate expense. The segment paragraphs (8k_2_02:25, 8k_2_02:31, 8k_2_02:36) say they are also excluded from adjusted Segment EBITA in all three segments. The CEO says the Company is 'early in our journey deploying our proprietary business system' (8k_2_02:16), which implies these costs continue. My input does not show whether the segment-level exclusion is new.",
    "account": "adjusted EBIT; adjusted EPS; adjusted Segment EBITA (non-GAAP)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Transformation costs represent incremental expenses incurred in association with strategic growth initiatives and cost saving opportunities",
    "paragraph_id": "0000833444-26-000083:8k_2_02:106",
    "explanation": false
  },
{
    "id": "earnings_quality_jc_capital_loss_without_explanation",
    "what_changed": "The adjusted free cash flow conversion table has a row labelled 'JC Capital net (income) loss'. Under that label, the three-month 2026 figure appears without parentheses and reads as a loss. The three-month 2025 figure appears in parentheses and reads as income. JC Capital is defined (8k_2_02:93) as finance/notes receivable and lease activity, earning mainly interest and sales-type lease profit. No prose in my input explains a JC Capital loss or any credit loss on those receivables.",
    "account": "finance/notes receivable (JC Capital); allowance for credit losses",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "JC Capital net (income) loss",
    "paragraph_id": "0000833444-26-000083:8k_2_02:133",
    "explanation": false
  },
{
    "id": "controls_audit_and_filings_risk_factor_update_not_in_input",
    "what_changed": "insufficient: MD&A says certain risk factors 'have been updated and supplemented in Part II, Item 1A of this Quarterly Report on Form 10-Q'. No Item 1A diff is in my input, so I cannot read the updated risk factors. My input also does not show whether this sentence is new.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Certain of these risk factors have been updated and supplemented in Part II, Item 1A of this Quarterly Report on Form 10-Q",
    "paragraph_id": "0000833444-26-000087:mdna:18",
    "explanation": false
  },
{
    "id": "across_documents_afff_insurance_recovery_figures",
    "what_changed": "The contingency note now says approximately $148 million of AFFF insurance recoveries were recorded in SG&A in the first nine months of fiscal 2026. The prior text said approximately $131 million for the first six months. The note repeats that future recovery amounts and timing cannot be predicted, and drops a redundant sentence on the insurance litigation's factual and legal issues. MD&A cites $16 million for the quarter and $135 million for nine months of AFFF recoveries as drivers of the SG&A decrease (mdna:30, mdna:31). The segment reconciliation shows a separate 'Water systems AFFF insurance recoveries' line (mdna:73, notes:135). I report these figures as stated; whether they are on the same basis is for the numbers reader.",
    "account": "selling, general and administrative expenses; water systems AFFF insurance recoveries",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In the first nine months of fiscal year 2026, the Company recorded approximately $148 million of insurance recoveries",
    "paragraph_id": "0000833444-26-000087:notes:194",
    "explanation": false
  }
]
```

There are 48 items, and none has `explanation` set to true. No paragraph in my input explains the cause of a number in receivables, inventory or reserves:

- **Receivables:** MD&A says they increased (mdna:96) but gives no cause.
- **Inventory:** the inventory note is a table only.
- **Reserves:** the environmental, asbestos, self-insured, warranty and restructuring reserve disclosures are tables or standing text.

## Insufficient

There are 30 insufficient answers: 4 items and 26 unitemized paragraphs.

- **Items (4):**
  - controls_audit_and_filings_earnings_release_amended_next_day
  - controls_audit_and_filings_officer_or_director_change_standalone
  - controls_audit_and_filings_officer_or_director_change_with_regulation_fd_exhibit
  - controls_audit_and_filings_risk_factor_update_not_in_input
- **Unitemized paragraphs (26).** Each is carried as text but my input does not show its prior wording, and the current text does not show what changed:
  - **Notes (10):** notes:10, notes:12, notes:13, notes:14, notes:26, notes:28, notes:29, notes:100, notes:119, notes:120.
  - **MD&A (16):** mdna:17, mdna:26, mdna:64, mdna:66, mdna:75, mdna:119, mdna:120, mdna:121, mdna:122, mdna:123, mdna:124, mdna:125, mdna:126, mdna:127, mdna:128, mdna:130.
- **Inputs absent:**
  - Auditor's report.
  - Item 1A diff, although MD&A says risk factors were updated.
  - Exhibit 21 diff.
  - Exhibit 10.

## Paragraphs carried as text that are not items

### input_controls.md
- 0000833444-26-000087:item_4_controls:1 — heading
- 0000833444-26-000087:item_4_controls:2 — heading
- 0000833444-26-000087:item_4_controls:3 — date rolled forward (evaluation as of June 30, 2026)
- 0000833444-26-000087:item_4_controls:4 — date rolled forward; disclosure controls still concluded effective
- 0000833444-26-000087:item_4_controls:5 — heading
- 0000833444-26-000087:item_4_controls:6 — date rolled forward; no significant change in internal control (contrast with the cash flow revision item)
- 0000833444-26-000087:item_4_controls:7 — page number

### input_notes.md
- 0000833444-26-000087:notes:1 — date rolled forward (three and nine months ended June 30, 2026); history confirms
- 0000833444-26-000087:notes:4 — wording only; company self-description rewritten
- 0000833444-26-000087:notes:5 — wording only; business description rewritten, no change in operations or accounting stated
- 0000833444-26-000087:notes:9 — heading
- 0000833444-26-000087:notes:10 — insufficient: standing ASU 2023-07 adoption text; prior wording not in input
- 0000833444-26-000087:notes:11 — heading
- 0000833444-26-000087:notes:12 — insufficient: ASU 2023-09 adoption timing; prior wording not in input
- 0000833444-26-000087:notes:13 — insufficient: ASU 2024-03 adoption timing; prior wording not in input
- 0000833444-26-000087:notes:14 — insufficient: ASU 2025-06, adoption fiscal 2029, still evaluating; prior wording not in input
- 0000833444-26-000087:notes:15 — boilerplate
- 0000833444-26-000087:notes:16 — heading
- 0000833444-26-000087:notes:18 — heading
- 0000833444-26-000087:notes:19 — heading
- 0000833444-26-000087:notes:22 — heading
- 0000833444-26-000087:notes:24 — heading
- 0000833444-26-000087:notes:25 — date rolled forward; ADT Mexico sale and gain previously disclosed, period label now nine months
- 0000833444-26-000087:notes:26 — insufficient: September 30, 2025 held-for-sale composition restated; prior wording not in input
- 0000833444-26-000087:notes:27 — heading
- 0000833444-26-000087:notes:28 — insufficient: standing R&LC discontinued-operations background; prior wording not in input
- 0000833444-26-000087:notes:29 — insufficient: R&LC discontinued-operations loss and its stated causes for nine months; cannot tell if only the period label changed
- 0000833444-26-000087:notes:30 — table introduction; date rolled forward
- 0000833444-26-000087:notes:31 — table, amounts only
- 0000833444-26-000087:notes:35 — table, amounts only
- 0000833444-26-000087:notes:36 — table, amounts only
- 0000833444-26-000087:notes:40 — table, amounts only (contract balances)
- 0000833444-26-000087:notes:41 — amounts only (revenue from opening contract liabilities); history shows same sentence rolled forward
- 0000833444-26-000087:notes:43 — amounts only (remaining performance obligations total and two-year share); history shows only figures and date changed
- 0000833444-26-000087:notes:47 — table, amounts only
- 0000833444-26-000087:notes:48 — amounts only (contract cost amortization)
- 0000833444-26-000087:notes:50 — table, amounts only (inventories)
- 0000833444-26-000087:notes:52 — table, amounts only; Acquisitions row covered by the acquisition item
- 0000833444-26-000087:notes:55 — table, amounts only
- 0000833444-26-000087:notes:56 — amounts only (intangible amortization)
- 0000833444-26-000087:notes:58 — table, amounts only
- 0000833444-26-000087:notes:60 — amounts only (supplier finance balances)
- 0000833444-26-000087:notes:61 — heading and table introduction
- 0000833444-26-000087:notes:62 — table, amounts only (short-term debt)
- 0000833444-26-000087:notes:63 — date rolled forward (revolver, no draws)
- 0000833444-26-000087:notes:64 — not in note change history; February 2026 repayment previously disclosed
- 0000833444-26-000087:notes:65 — table introduction
- 0000833444-26-000087:notes:66 — table, amounts only
- 0000833444-26-000087:notes:67 — amounts only, plus wording ('offset by gains resulting from changes' became 'offset by changes')
- 0000833444-26-000087:notes:68 — duplicate table introduction
- 0000833444-26-000087:notes:76 — table, amounts only
- 0000833444-26-000087:notes:77 — wording; cross-reference footnote
- 0000833444-26-000087:notes:81 — continuation of the notes:80 item (September 30, 2025 designation incl. yen)
- 0000833444-26-000087:notes:82 — amounts only
- 0000833444-26-000087:notes:83 — amounts only
- 0000833444-26-000087:notes:88 — wording; valuation method sentence with cross-reference
- 0000833444-26-000087:notes:89 — amounts only
- 0000833444-26-000087:notes:91 — date rolled forward
- 0000833444-26-000087:notes:92 — table, amounts only
- 0000833444-26-000087:notes:97 — table, amounts only (share counts)
- 0000833444-26-000087:notes:99 — table, amounts only (AOCI)
- 0000833444-26-000087:notes:100 — insufficient: standing pension introduction; prior wording not in input
- 0000833444-26-000087:notes:101 — table, amounts only
- 0000833444-26-000087:notes:105 — table, amounts only (restructuring by segment)
- 0000833444-26-000087:notes:107 — table, amounts only (restructuring reserve roll-forward)
- 0000833444-26-000087:notes:112 — date rolled forward; prior-year quarter comparative (cited in the notes:110 item)
- 0000833444-26-000087:notes:113 — date rolled forward; prior-year nine-month comparative
- 0000833444-26-000087:notes:114 — wording; cross-reference
- 0000833444-26-000087:notes:116 — amounts only (unrecognized tax benefits, accrued interest)
- 0000833444-26-000087:notes:117 — date rolled forward; prior-year statute-expiry benefit
- 0000833444-26-000087:notes:119 — insufficient: tax years under examination table; prior table not in input
- 0000833444-26-000087:notes:120 — insufficient: statement that tax examinations may conclude within twelve months; cannot tell if new
- 0000833444-26-000087:notes:132 — table, amounts only
- 0000833444-26-000087:notes:133 — table, amounts only
- 0000833444-26-000087:notes:134 — table introduction
- 0000833444-26-000087:notes:135 — table, amounts only
- 0000833444-26-000087:notes:136 — wording; cross-reference footnote
- 0000833444-26-000087:notes:141 — table, amounts only (warranty roll-forward, no prose)
- 0000833444-26-000087:notes:142 — heading
- 0000833444-26-000087:notes:143 — reordered; table-introduction sentence moved (history :27)
- 0000833444-26-000087:notes:144 — table, amounts only (environmental reserves)
- 0000833444-26-000087:notes:145 — unchanged per note change history
- 0000833444-26-000087:notes:146 — unchanged per note change history
- 0000833444-26-000087:notes:148 — reordered; paragraph split at page break (history :3)
- 0000833444-26-000087:notes:149 — reordered; continuation moved (history :4 and removed :21)
- 0000833444-26-000087:notes:150 — heading
- 0000833444-26-000087:notes:151 — heading
- 0000833444-26-000087:notes:152 — unchanged per note change history
- 0000833444-26-000087:notes:153 — unchanged per note change history
- 0000833444-26-000087:notes:154 — unchanged per note change history
- 0000833444-26-000087:notes:155 — heading
- 0000833444-26-000087:notes:157 — its change is a removed sentence, itemized as wdnr_penalty_uncertainty_sentence_removed with the history paragraph id
- 0000833444-26-000087:notes:159 — unchanged per note change history
- 0000833444-26-000087:notes:160 — unchanged per note change history
- 0000833444-26-000087:notes:161 — wording; 'these cases' became 'the active cases', reflecting the WDOJ resolution itemized at notes:158
- 0000833444-26-000087:notes:162 — heading
- 0000833444-26-000087:notes:163 — heading
- 0000833444-26-000087:notes:164 — reordered; paragraph split at page break (history :9)
- 0000833444-26-000087:notes:165 — reordered; paragraph split at page break (history :10)
- 0000833444-26-000087:notes:166 — unchanged per note change history
- 0000833444-26-000087:notes:167 — heading
- 0000833444-26-000087:notes:168 — unchanged per note change history
- 0000833444-26-000087:notes:169 — unchanged per note change history
- 0000833444-26-000087:notes:170 — heading
- 0000833444-26-000087:notes:171 — unchanged per note change history
- 0000833444-26-000087:notes:173 — unchanged per note change history
- 0000833444-26-000087:notes:174 — heading
- 0000833444-26-000087:notes:176 — continuation of the notes:175 item
- 0000833444-26-000087:notes:177 — heading
- 0000833444-26-000087:notes:178 — unchanged per note change history
- 0000833444-26-000087:notes:179 — unchanged per note change history
- 0000833444-26-000087:notes:180 — heading
- 0000833444-26-000087:notes:181 — unchanged per note change history
- 0000833444-26-000087:notes:182 — unchanged per note change history
- 0000833444-26-000087:notes:183 — unchanged per note change history
- 0000833444-26-000087:notes:184 — reordered; paragraph split at page break (history :14)
- 0000833444-26-000087:notes:185 — reordered; paragraph split at page break (history :15)
- 0000833444-26-000087:notes:186 — unchanged per note change history
- 0000833444-26-000087:notes:187 — unchanged per note change history
- 0000833444-26-000087:notes:188 — heading
- 0000833444-26-000087:notes:189 — unchanged per note change history
- 0000833444-26-000087:notes:190 — unchanged per note change history
- 0000833444-26-000087:notes:191 — unchanged per note change history
- 0000833444-26-000087:notes:192 — unchanged per note change history
- 0000833444-26-000087:notes:195 — heading
- 0000833444-26-000087:notes:196 — unchanged per note change history
- 0000833444-26-000087:notes:197 — table introduction
- 0000833444-26-000087:notes:198 — table, amounts only (asbestos liabilities and assets)
- 0000833444-26-000087:notes:199 — table introduction
- 0000833444-26-000087:notes:200 — table, amounts only (asbestos assets)
- 0000833444-26-000087:notes:201 — unchanged per note change history
- 0000833444-26-000087:notes:202 — heading
- 0000833444-26-000087:notes:203 — unchanged per note change history
- 0000833444-26-000087:notes:204 — table introduction
- 0000833444-26-000087:notes:205 — table, amounts only (self-insured liabilities)
- 0000833444-26-000087:notes:206 — heading
- 0000833444-26-000087:notes:207 — unchanged per note change history
- 0000833444-26-000087:notes:208 — duplicate table introduction

### input_mdna.md
- 0000833444-26-000087:mdna:5 — wording only; company self-description
- 0000833444-26-000087:mdna:7 — continuation of mdna:5; wording only
- 0000833444-26-000087:mdna:8 — wording only; business description
- 0000833444-26-000087:mdna:9 — date rolled forward
- 0000833444-26-000087:mdna:15 — continuation of the mdna:14 item; monitoring language
- 0000833444-26-000087:mdna:17 — insufficient: demand-trend narrative (data centers, regulation); prior wording not in input; data-center demand itemized at mdna:80
- 0000833444-26-000087:mdna:20 — table, amounts only
- 0000833444-26-000087:mdna:21 — amounts only; quarterly sales bridge, drivers described as continued
- 0000833444-26-000087:mdna:22 — amounts only; nine-month sales bridge
- 0000833444-26-000087:mdna:25 — table, amounts only
- 0000833444-26-000087:mdna:26 — insufficient: generic gross-profit drivers; prior wording not in input
- 0000833444-26-000087:mdna:29 — table, amounts only
- 0000833444-26-000087:mdna:31 — amounts only; nine-month SG&A drivers, figures carried into the across_documents AFFF item
- 0000833444-26-000087:mdna:32 — wording; cross-references
- 0000833444-26-000087:mdna:36 — table, amounts only; 'Other impairments' line referenced by the mdna:37 item
- 0000833444-26-000087:mdna:38 — page number
- 0000833444-26-000087:mdna:42 — table, amounts only (tax)
- 0000833444-26-000087:mdna:50 — table, amounts only
- 0000833444-26-000087:mdna:52 — amounts only; Americas quarterly bridge, 'continued strength'
- 0000833444-26-000087:mdna:53 — amounts only; EMEA bridge, its continuation itemized at mdna:54
- 0000833444-26-000087:mdna:55 — amounts only; APAC quarterly bridge
- 0000833444-26-000087:mdna:57 — amounts only
- 0000833444-26-000087:mdna:58 — nine-month counterpart of the mdna:54 item; amounts
- 0000833444-26-000087:mdna:59 — amounts only
- 0000833444-26-000087:mdna:61 — table, amounts only
- 0000833444-26-000087:mdna:62 — table, amounts only
- 0000833444-26-000087:mdna:64 — insufficient: Americas EBIT driver (operating leverage); prior wording not in input
- 0000833444-26-000087:mdna:66 — insufficient: APAC EBIT drivers (productivity, mix, revenue); prior wording not in input
- 0000833444-26-000087:mdna:67 — page number
- 0000833444-26-000087:mdna:70 — nine-month counterpart of the mdna:65 item
- 0000833444-26-000087:mdna:73 — table, amounts only
- 0000833444-26-000087:mdna:74 — heading
- 0000833444-26-000087:mdna:75 — insufficient: orders and backlog purpose and caveat; prior wording not in input
- 0000833444-26-000087:mdna:76 — table introduction
- 0000833444-26-000087:mdna:77 — table, amounts only
- 0000833444-26-000087:mdna:78 — date rolled forward
- 0000833444-26-000087:mdna:81 — amounts only; Americas orders by type, services figure used in the mdna:86 item
- 0000833444-26-000087:mdna:82 — amounts only
- 0000833444-26-000087:mdna:83 — amounts only; APAC services figure used in the mdna:86 item
- 0000833444-26-000087:mdna:87 — amounts only
- 0000833444-26-000087:mdna:88 — amounts only
- 0000833444-26-000087:mdna:89 — amounts only (remaining performance obligations)
- 0000833444-26-000087:mdna:95 — table, amounts only
- 0000833444-26-000087:mdna:98 — table, amounts only
- 0000833444-26-000087:mdna:103 — table, amounts only
- 0000833444-26-000087:mdna:106 — amounts only (dividend declared)
- 0000833444-26-000087:mdna:107 — amounts only; standing liquidity adequacy statement
- 0000833444-26-000087:mdna:109 — amounts only (commercial paper)
- 0000833444-26-000087:mdna:111 — date rolled forward (revolver)
- 0000833444-26-000087:mdna:112 — date rolled forward; ratings paragraphs that follow are same as prior
- 0000833444-26-000087:mdna:115 — date rolled forward (covenant compliance)
- 0000833444-26-000087:mdna:119 — insufficient: guaranteed-notes introduction; prior wording not in input
- 0000833444-26-000087:mdna:120 — insufficient: guaranteed-notes list entry; cannot tell whether an issue was added or removed
- 0000833444-26-000087:mdna:121 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:122 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:123 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:124 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:125 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:126 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:127 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:128 — insufficient: guaranteed-notes list entry
- 0000833444-26-000087:mdna:130 — insufficient: obligor group table introduction; prior wording not in input
- 0000833444-26-000087:mdna:131 — table, amounts only
- 0000833444-26-000087:mdna:134 — table, amounts only

### input_8k.md
- 8-K item-code list:
  - New since the prior 10-Q: 0000833444-26-000054, -000058 and -000064, each itemized, and -000083, which is the release read in full below.
  - 0000833444-26-000040 (2026-05-04) predates the prior 10-Q; it is mentioned in the 5.02 item.
  - All other entries are older, so nothing is new there.
- Late-filing list — the NT 10-K from 2023 is not new.
- 0000833444-26-000083:8k_2_02:1 — exhibit header metadata
- 0000833444-26-000083:8k_2_02:2 — document label
- 0000833444-26-000083:8k_2_02:3 — exhibit label
- 0000833444-26-000083:8k_2_02:4 — release label
- 0000833444-26-000083:8k_2_02:5 — headline; guidance raise itemized at :51 and :53
- 0000833444-26-000083:8k_2_02:6 — separator
- 0000833444-26-000083:8k_2_02:7 — headline amounts (sales growth)
- 0000833444-26-000083:8k_2_02:8 — headline amounts (EPS)
- 0000833444-26-000083:8k_2_02:9 — headline amounts (orders); orders itemized at mdna:80 and :18
- 0000833444-26-000083:8k_2_02:10 — headline amounts (backlog); itemized at mdna:85
- 0000833444-26-000083:8k_2_02:11 — non-GAAP boilerplate
- 0000833444-26-000083:8k_2_02:12 — separator
- 0000833444-26-000083:8k_2_02:13 — dateline, amounts only
- 0000833444-26-000083:8k_2_02:14 — amounts only
- 0000833444-26-000083:8k_2_02:15 — amounts only
- 0000833444-26-000083:8k_2_02:16 — CEO quote; tone; raised outlook itemized at :51 and :53; business-system remark used in the :106 item
- 0000833444-26-000083:8k_2_02:17 — heading
- 0000833444-26-000083:8k_2_02:19 — boilerplate (slides)
- 0000833444-26-000083:8k_2_02:20 — page number
- 0000833444-26-000083:8k_2_02:21 — heading
- 0000833444-26-000083:8k_2_02:22 — table
- 0000833444-26-000083:8k_2_02:23 — amounts only; Americas sales, 'continued strength'
- 0000833444-26-000083:8k_2_02:24 — amounts only; data-center driver itemized at mdna:80
- 0000833444-26-000083:8k_2_02:25 — amounts only; segment transformation-cost exclusion carried into the :106 item
- 0000833444-26-000083:8k_2_02:26 — page number
- 0000833444-26-000083:8k_2_02:27 — heading
- 0000833444-26-000083:8k_2_02:28 — table
- 0000833444-26-000083:8k_2_02:29 — same statement as the mdna:54 item
- 0000833444-26-000083:8k_2_02:30 — amounts only; EMEA orders and backlog
- 0000833444-26-000083:8k_2_02:31 — same driver as the mdna:65 item
- 0000833444-26-000083:8k_2_02:32 — heading
- 0000833444-26-000083:8k_2_02:33 — table
- 0000833444-26-000083:8k_2_02:34 — amounts only; APAC sales
- 0000833444-26-000083:8k_2_02:35 — amounts only; APAC orders and backlog
- 0000833444-26-000083:8k_2_02:36 — amounts only; APAC drivers as mdna:66, transformation-cost exclusion in the :106 item
- 0000833444-26-000083:8k_2_02:37 — page number
- 0000833444-26-000083:8k_2_02:38 — heading
- 0000833444-26-000083:8k_2_02:39 — table
- 0000833444-26-000083:8k_2_02:41 — heading
- 0000833444-26-000083:8k_2_02:42 — amounts only (cash flow)
- 0000833444-26-000083:8k_2_02:43 — amounts only (dividends)
- 0000833444-26-000083:8k_2_02:44 — heading
- 0000833444-26-000083:8k_2_02:45 — boilerplate; forward-looking non-GAAP disclaimer
- 0000833444-26-000083:8k_2_02:47 — content of the :46 fourth-quarter guidance item
- 0000833444-26-000083:8k_2_02:48 — content of the :46 fourth-quarter guidance item
- 0000833444-26-000083:8k_2_02:49 — content of the :46 fourth-quarter guidance item
- 0000833444-26-000083:8k_2_02:50 — heading
- 0000833444-26-000083:8k_2_02:54 — prose says unchanged (adjusted free cash flow conversion guidance)
- 0000833444-26-000083:8k_2_02:55 — page number
- 0000833444-26-000083:8k_2_02:56 — heading
- 0000833444-26-000083:8k_2_02:57 — boilerplate (conference call)
- 0000833444-26-000083:8k_2_02:58 — heading
- 0000833444-26-000083:8k_2_02:59 — boilerplate (about the company)
- 0000833444-26-000083:8k_2_02:60 — boilerplate
- 0000833444-26-000083:8k_2_02:61 — boilerplate
- 0000833444-26-000083:8k_2_02:62 — heading
- 0000833444-26-000083:8k_2_02:63 — contacts
- 0000833444-26-000083:8k_2_02:64 — end marker
- 0000833444-26-000083:8k_2_02:65 — page number
- 0000833444-26-000083:8k_2_02:66 — heading; cautionary statement text not carried
- 0000833444-26-000083:8k_2_02:67 — page number
- 0000833444-26-000083:8k_2_02:68 — heading
- 0000833444-26-000083:8k_2_02:69 — heading
- 0000833444-26-000083:8k_2_02:70 — heading
- 0000833444-26-000083:8k_2_02:71 — heading
- 0000833444-26-000083:8k_2_02:72 — table (income statement)
- 0000833444-26-000083:8k_2_02:73 — page number
- 0000833444-26-000083:8k_2_02:74 — heading
- 0000833444-26-000083:8k_2_02:75 — heading
- 0000833444-26-000083:8k_2_02:76 — heading
- 0000833444-26-000083:8k_2_02:77 — table (balance sheet)
- 0000833444-26-000083:8k_2_02:78 — page number
- 0000833444-26-000083:8k_2_02:79 — heading
- 0000833444-26-000083:8k_2_02:80 — heading
- 0000833444-26-000083:8k_2_02:81 — table (cash flows)
- 0000833444-26-000083:8k_2_02:82 — page number
- 0000833444-26-000083:8k_2_02:83 — heading
- 0000833444-26-000083:8k_2_02:84 — heading
- 0000833444-26-000083:8k_2_02:85 — standing description of the July 2025 R&LC sale
- 0000833444-26-000083:8k_2_02:86 — heading
- 0000833444-26-000083:8k_2_02:87 — boilerplate
- 0000833444-26-000083:8k_2_02:88 — heading
- 0000833444-26-000083:8k_2_02:89 — standing definition (organic sales)
- 0000833444-26-000083:8k_2_02:90 — heading
- 0000833444-26-000083:8k_2_02:91 — boilerplate
- 0000833444-26-000083:8k_2_02:92 — introduction
- 0000833444-26-000083:8k_2_02:93 — standing definition (JC Capital); JC Capital loss itemized at :133
- 0000833444-26-000083:8k_2_02:94 — standing (factoring program discontinued March 2024)
- 0000833444-26-000083:8k_2_02:95 — standing (AFFF cash adjustment)
- 0000833444-26-000083:8k_2_02:98 — heading
- 0000833444-26-000083:8k_2_02:99 — boilerplate
- 0000833444-26-000083:8k_2_02:100 — page number
- 0000833444-26-000083:8k_2_02:101 — introduction
- 0000833444-26-000083:8k_2_02:102 — standing definition (mark-to-market)
- 0000833444-26-000083:8k_2_02:103 — standing definition (restructuring and impairment)
- 0000833444-26-000083:8k_2_02:104 — standing definition (AFFF settlement and recoveries)
- 0000833444-26-000083:8k_2_02:105 — standing definition (transaction/separation)
- 0000833444-26-000083:8k_2_02:107 — standing definition of an adjusting item shown only in the trailing-twelve-month table (ERP accelerated depreciation)
- 0000833444-26-000083:8k_2_02:108 — standing definition (divestiture loss or gain)
- 0000833444-26-000083:8k_2_02:109 — standing definition (EMEA joint venture loss)
- 0000833444-26-000083:8k_2_02:110 — standing definition (discrete tax items)
- 0000833444-26-000083:8k_2_02:111 — standing definition (related tax impact)
- 0000833444-26-000083:8k_2_02:112 — boilerplate
- 0000833444-26-000083:8k_2_02:113 — heading
- 0000833444-26-000083:8k_2_02:114 — standing definition (operating leverage); referenced in the :52 item
- 0000833444-26-000083:8k_2_02:115 — heading
- 0000833444-26-000083:8k_2_02:116 — boilerplate
- 0000833444-26-000083:8k_2_02:117 — page number
- 0000833444-26-000083:8k_2_02:118 — heading
- 0000833444-26-000083:8k_2_02:119 — introduction
- 0000833444-26-000083:8k_2_02:120 — table
- 0000833444-26-000083:8k_2_02:121 — table
- 0000833444-26-000083:8k_2_02:122 — page number
- 0000833444-26-000083:8k_2_02:123 — table
- 0000833444-26-000083:8k_2_02:124 — table
- 0000833444-26-000083:8k_2_02:125 — page number
- 0000833444-26-000083:8k_2_02:126 — table
- 0000833444-26-000083:8k_2_02:127 — table
- 0000833444-26-000083:8k_2_02:128 — page number
- 0000833444-26-000083:8k_2_02:129 — heading
- 0000833444-26-000083:8k_2_02:130 — introduction
- 0000833444-26-000083:8k_2_02:131 — table
- 0000833444-26-000083:8k_2_02:132 — introduction
- 0000833444-26-000083:8k_2_02:134 — page number
- 0000833444-26-000083:8k_2_02:135 — heading
- 0000833444-26-000083:8k_2_02:136 — introduction
- 0000833444-26-000083:8k_2_02:137 — table
- 0000833444-26-000083:8k_2_02:138 — footnote boilerplate
- 0000833444-26-000083:8k_2_02:139 — page number
- 0000833444-26-000083:8k_2_02:140 — introduction
- 0000833444-26-000083:8k_2_02:141 — table
- 0000833444-26-000083:8k_2_02:142 — table
- 0000833444-26-000083:8k_2_02:143 — page number
- 0000833444-26-000083:8k_2_02:144 — introduction
- 0000833444-26-000083:8k_2_02:145 — table
- 0000833444-26-000083:8k_2_02:146 — introduction
- 0000833444-26-000083:8k_2_02:147 — table
- 0000833444-26-000083:8k_2_02:148 — heading
- 0000833444-26-000083:8k_2_02:149 — introduction
- 0000833444-26-000083:8k_2_02:150 — table
- 0000833444-26-000083:8k_2_02:151 — rounding note
- 0000833444-26-000083:8k_2_02:152 — page number
- 0000833444-26-000083:8k_2_02:153 — table
- 0000833444-26-000083:8k_2_02:154 — rounding note
- 0000833444-26-000083:8k_2_02:155 — introduction
- 0000833444-26-000083:8k_2_02:156 — table
- 0000833444-26-000083:8k_2_02:157 — page number
- 0000833444-26-000083:8k_2_02:158 — heading
- 0000833444-26-000083:8k_2_02:159 — introduction
- 0000833444-26-000083:8k_2_02:160 — table
- 0000833444-26-000083:8k_2_02:161 — introduction
- 0000833444-26-000083:8k_2_02:162 — table
- 0000833444-26-000083:8k_2_02:163 — heading
- 0000833444-26-000083:8k_2_02:164 — adjusted tax-rate figures; tax-rate theme itemized at notes:110
- 0000833444-26-000083:8k_2_02:165 — page number

### Removed paragraphs in the note change history (prior ids), for completeness
- 0000833444-26-000050:note_history:21 — reordered; text now at notes:149
- 0000833444-26-000050:note_history:22 — itemized (asset retirement obligation sentence removed)
- 0000833444-26-000050:note_history:23 — replaced by notes:158; itemized under the WDOJ resolution item
- 0000833444-26-000050:note_history:24 — replaced by notes:194; itemized under the across_documents AFFF item (redundant sentence dropped)
- 0000833444-26-000050:note_history:25 — prior asbestos table, amounts only
- 0000833444-26-000050:note_history:26 — prior asbestos asset table, amounts only
- 0000833444-26-000050:note_history:32 — duplicate of :25, amounts only
- 0000833444-26-000050:note_history:33 — duplicate of :26, amounts only
- 0000833444-26-000050:note_history:38 — prior self-description, replaced by notes:4, wording only
- 0000833444-26-000050:note_history:39 — prior business description, replaced by notes:5, wording only
- 0000833444-26-000050:note_history:44 — prior short-term debt table, amounts only
- 0000833444-26-000050:note_history:49 — duplicate of :44, amounts only
- 0000833444-26-000050:note_history:60 — prior contract-liability revenue sentence, replaced by notes:41, amounts only
