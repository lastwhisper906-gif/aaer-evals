<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes text reader: JCI 10-Q 0000833444-26-000087 (quarter ended June 30, 2026)

## Scope and input check

- I read all six input files in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md and input_prior_predictions.md.
- Nothing forbidden is in the directory. There is no trend table, no prices, no returns, no short interest, no other company's files and no outcome window. The 8-K earnings release includes its own financial statement tables. Those tables are part of the 8-K body.
- Some inputs named in my instructions are missing:
  - There is no Item 1A diff, no Exhibit 21 diff and no Exhibit 10.
  - There is no auditor's report. This is a 10-Q, and only Item 4 is carried.
  - MD&A (mdna:18) says the risk factors were updated in Part II, Item 1A. I cannot read that update.
- Prior predictions: none on record.
- I did no arithmetic. Every amount below is taken as the prose states it.

## Items

```json
[
{"id":"related_parties_contingencies_and_subsequent_events_wisconsin_doj_case_settled","what_changed":"The Wisconsin DOJ enforcement action over the FTC was described last quarter as pending, with a settlement being finalized and penalties plus an injunction sought. It is now resolved. The State filed a Stipulation for Judgment on June 4, 2026. Tyco Fire Products paid $10 million to a statewide PFAS fund and will continue its remediation work in Marinette and Peshtigo: running the GETS, monitoring water quality and completing PFAS-free deep drinking water wells. Johnson Controls, Inc. was dismissed with prejudice on June 5, 2026.","account":"environmental reserves (other current/noncurrent liabilities); cash","expected_direction":"down","horizon":"this quarter","quote":"On June 4, 2026, the State filed a Stipulation for Judgment, resolving the litigation.","paragraph_id":"0000833444-26-000087:notes:158","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_wdnr_penalty_uncertainty_sentence_removed","what_changed":"A sentence was removed from the WDNR Notices of Noncompliance paragraph. It said the Company could not predict regulatory or enforcement actions arising from the WDNR's actions, including possible penalties. The removal coincides with the WDOJ stipulated judgment.","account":"environmental reserves","expected_direction":"none","horizon":"this quarter","quote":"The Company cannot predict what regulatory or enforcement actions, if any, might result from the WDNR’s actions, or the consequences of any such actions, including the potential assessment of penalties.","paragraph_id":"0000833444-26-000050:note_history:6","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_ftc_litigation_defense_limited_to_active_cases","what_changed":"The FTC litigation defense sentence changed from 'each of these cases' to 'each of the active cases'. The prose now separates resolved FTC cases (the WDOJ matter) from those still active (the Town of Peshtigo case and the Dane County individual actions).","account":"none","expected_direction":"none","horizon":"12 months","quote":"The Company is vigorously defending each of the active cases and believes that it has meritorious defenses","paragraph_id":"0000833444-26-000087:notes:161","explanation":false},
{"id":"estimates_and_discretion_wisconsin_pfas_drinking_water_standards_final","what_changed":"Last quarter the Wisconsin drinking water standards (4 ng/L for PFOA and PFOS; 10 ng/L for PFHxS, PFNA and HFPO-DA) were 'subject to further reviews and approvals before they become final'. They are now stated as approved through the state rulemaking process in 2026. The note ties FTC and Marinette remediation reserves to changes in permissible levels.","account":"environmental reserves","expected_direction":"up","horizon":"12 months","quote":"The standards were subsequently approved through the state rulemaking process in 2026.","paragraph_id":"0000833444-26-000087:notes:156","explanation":false},
{"id":"estimates_and_discretion_wisconsin_draft_rule_adopting_federal_pfas_limits","what_changed":"New sentence: in June 2026 the WDNR issued a draft rulemaking to adopt the April 2024 federal NPDWR Maximum Contaminant Levels and Hazard Index as Wisconsin law. This is a state-level adoption of the stricter federal limits, in the region where the Company's main PFAS remediation sits.","account":"environmental reserves","expected_direction":"up","horizon":"12 months","quote":"In June 2026, the Wisconsin Department of Natural Resources issued a draft rulemaking to adopt as a matter of Wisconsin law the Maximum Contaminant Levels and Hazard Index standards established in the April 2024 NPDWR.","paragraph_id":"0000833444-26-000087:notes:147","explanation":false},
{"id":"estimates_and_discretion_federal_pfas_rules_withdrawn_or_proposed_for_rescission","what_changed":"Federal PFAS rule status updated: (a) EPA withdrew the second RCRA hazardous waste proposal on May 8, 2026, and the first RCRA proposal is described as not finalized; (b) OMB completed its review on May 1, 2026 of the proposed rescission of MCLs for PFHxS, PFNA, HFPO-DA and PFBS, the proposal was published May 20, 2026, and the rescission is not finalized. Last quarter the rescission had only been sent to OMB. 'Published' became 'finalized' for the April 2024 NPDWR.","account":"environmental reserves","expected_direction":"none","horizon":"12 months","quote":"however, the EPA withdrew that proposal on May 8, 2026","paragraph_id":"0000833444-26-000087:notes:147","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_afff_insurance_recoveries_nine_months","what_changed":"AFFF insurance recoveries recorded in SG&A are now stated as approximately $148 million for the first nine months of fiscal 2026. Last quarter the note said approximately $131 million for the first six months. Settlements with certain insurers continue, litigation with the remaining carriers continues in Wisconsin state court, and future amount and timing remain unpredictable. A duplicated sentence about insurance litigation issues was dropped (wording only).","account":"SG&A (insurance recoveries)","expected_direction":"down","horizon":"this quarter","quote":"In the first nine months of fiscal year 2026, the Company recorded approximately $148 million of insurance recoveries related to settlements with its insurance carriers in selling, general and administrative expenses in the consolidated statements of income.","paragraph_id":"0000833444-26-000087:notes:194","explanation":false},
{"id":"across_documents_afff_insurance_recovery_amounts_mdna_versus_note","what_changed":"Different documents state different AFFF insurance recovery figures for the same periods. MD&A attributes the SG&A decrease to AFFF insurance recoveries of $135 million (nine months, mdna:31) and $16 million (three months, mdna:30). Note 18 prose (notes:194) says approximately $148 million was recorded in SG&A for the nine months. The segment reconciliation (notes:135, mdna:73) and 8-K footnotes show 'Water systems AFFF insurance recoveries' lines for both periods. mdna:31 also names the $70 million ADT Mexico gain recorded within SG&A. I have not reconciled these figures; that is for the numbers reader and the supervisors.","account":"SG&A","expected_direction":"none","horizon":"this quarter","quote":"primarily due to AFFF insurance recoveries related to the previously disclosed water systems settlement ($135 million)","paragraph_id":"0000833444-26-000087:mdna:31","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_belgium_afff_proceedings_added","what_changed":"The count of AFFF property damage proceedings in Belgium naming a Company affiliate went from four to five. The cases are still on hold pending efforts to dismiss. No accrual is described.","account":"none","expected_direction":"none","horizon":"12 months","quote":"Five AFFF property damage proceedings have been filed in Belgium against numerous defendants, including an affiliate of the Company.","paragraph_id":"0000833444-26-000087:notes:193","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_val_dor_quebec_proceeding_names_parent","what_changed":"New disclosure: Tyco Fire Products and the parent, Johnson Controls International plc, are named in an individual proceeding in Quebec brought by the City of Val D'Or over PFAS well-water contamination from airport firefighting training (notes:175-176). The Canadian class action members now also include indigenous communities. No accrual or estimate is given.","account":"none","expected_direction":"none","horizon":"12 months","quote":"Tyco Fire Products and Johnson Controls International plc have also been named, among other manufacturers, in an individual proceeding in Quebec commenced by the City of Val D’Or","paragraph_id":"0000833444-26-000087:notes:175","explanation":false},
{"id":"structure_and_disclosure_changes_water_settlement_exclusions_condensed","what_changed":"The water systems settlement scope paragraph was shortened. Two lists were removed: the named excluded systems (State/federal systems, small transient systems, private wells, Marinette's own system) and the named categories of MDL cases the settlement does not cover (personal injury, property damage, other class actions, state/territory AG claims, stormwater/wastewater claims). The opt-out is now in the past tense ('requested'), where it used to refer to a process 'to be established'. The 'unable to estimate' conclusion is unchanged. The disclosure is less specific about the unresolved exposure.","account":"none","expected_direction":"none","horizon":"12 months","quote":"Certain systems are excluded from the settlement class and the settlement does not resolve claims of public water systems that requested exclusion from the class","paragraph_id":"0000833444-26-000087:notes:172","explanation":false},
{"id":"articulation_and_the_filed_history_prior_year_cash_flow_debt_presentation_revised","what_changed":"Last quarter's note said a similar revision for the nine months ended June 30, 2025 would come in this 10-Q. It is now made: 'Proceeds from debt' and 'Repayments of debt' for the prior-year nine months are revised from an incorrect net presentation. The Company calls it not material, and states that financing cash flow totals and the change in cash are unchanged. Item 4 in the same filing reports effective disclosure controls and no significant change in internal control.","account":"proceeds from debt; repayments of debt (prior-year comparative, financing activities)","expected_direction":"up","horizon":"this quarter","quote":"have been revised for certain short-term debt transactions that occurred in the nine months ended June 30, 2025 and were incorrectly presented on a net basis","paragraph_id":"0000833444-26-000087:notes:8","explanation":false},
{"id":"structure_and_disclosure_changes_asset_retirement_obligation_sentence_removed","what_changed":"The sentence disclosing conditional asset retirement obligations for environmental matters at owned facilities was removed from the environmental note. No replacement disclosure appears in the current text.","account":"other liabilities (conditional asset retirement obligations)","expected_direction":"none","horizon":"this quarter","quote":"Conditional asset retirement obligations were $7 million at both March 31, 2026 and September 30, 2025.","paragraph_id":"0000833444-26-000050:note_history:22","explanation":false},
{"id":"structure_and_disclosure_changes_alloy_and_nantum_acquisitions","what_changed":"New: in Q3 the Company closed the acquisitions of Alloy Enterprises (direct liquid cooling components) and Nantum AI (OpenBlue digital). Aggregate consideration net of cash was about $291 million, 'a meaningful component' of it for Alloy. Both are reported in Americas. The prose states goodwill of $193 million and $127 million of developed technology intangibles. MD&A (mdna:100) and the 8-K cash flow statement show the cash outflow in investing activities.","account":"goodwill; other intangible assets; acquisitions of businesses (investing cash flow)","expected_direction":"up","horizon":"this quarter","quote":"During the third quarter of fiscal 2026, the Company closed the acquisitions of Alloy Enterprises and Nantum AI.","paragraph_id":"0000833444-26-000087:notes:17","explanation":false},
{"id":"estimates_and_discretion_acquired_developed_technology_useful_life","what_changed":"New estimate: acquired developed technology is amortized straight-line over 15 years. The prose does not call the allocation preliminary or provisional.","account":"amortization of intangible assets","expected_direction":"up","horizon":"next quarter","quote":"$127 million of definite-lived intangible assets related to developed technology being amortized on a straight-line basis over 15 years","paragraph_id":"0000833444-26-000087:notes:17","explanation":false},
{"id":"structure_and_disclosure_changes_adt_united_kingdom_residential_held_for_sale","what_changed":"New: in Q3 the Company signed a definitive agreement to sell its ADT United Kingdom Residential Security business and classified it as held for sale, not as a discontinued operation. Closing is expected in fiscal 2027. As of June 30, 2026, held-for-sale assets of $229 million and liabilities of $39 million are attributed to it.","account":"noncurrent assets and liabilities held for sale","expected_direction":"up","horizon":"this quarter","quote":"signed a definitive agreement to sell its ADT United Kingdom Residential Security business and determined that it met the criteria to be classified as held for sale","paragraph_id":"0000833444-26-000087:notes:20","explanation":false},
{"id":"estimates_and_discretion_adt_united_kingdom_fair_value_exceeds_carrying_value","what_changed":"New judgment: management concludes that the ADT UK disposal group's estimated fair value less costs to sell exceeds its carrying value, so no held-for-sale write-down is recorded. Contrast: the ADT Spain disposal group took a $50 million impairment in Q1.","account":"restructuring and impairment costs","expected_direction":"none","horizon":"next quarter","quote":"the estimated fair value less costs to sell of the held for sale business exceeded its carrying value, and therefore, no adjustment was necessary","paragraph_id":"0000833444-26-000087:notes:21","explanation":false},
{"id":"estimates_and_discretion_goodwill_allocated_to_disposal_groups","what_changed":"The goodwill rollforward footnote now states that goodwill of $102 million was allocated to the ADT United Kingdom Residential Security disposal group, alongside $38 million for ADT Spain. The amounts sit in the 'Foreign currency translation and other' line, not a separate disposal line.","account":"goodwill","expected_direction":"down","horizon":"this quarter","quote":"Includes the allocation of goodwill to the ADT Spain Security business and the ADT United Kingdom Residential Security business disposal groups of $38 million and $102 million, respectively.","paragraph_id":"0000833444-26-000087:notes:53","explanation":false},
{"id":"structure_and_disclosure_changes_adt_spain_sale_completed","what_changed":"New: the ADT Spain Security sale closed on April 1, 2026 for net proceeds of $98 million, with no gain or loss on the transaction. The Q1 impairment of $50 million is restated in the prose. MD&A (mdna:100) cites ADT Spain proceeds as an investing cash flow driver.","account":"divestitures of businesses (investing cash flow); assets held for sale","expected_direction":"up","horizon":"this quarter","quote":"On April 1, 2026, the Company completed the sale of its ADT Spain Security business for net proceeds of $98 million, with no gain or loss recorded on the transaction.","paragraph_id":"0000833444-26-000087:notes:23","explanation":false},
{"id":"liquidity_and_capital_residential_hvac_final_purchase_price_payment","what_changed":"New: in Q3 the Company paid about $155 million in final purchase price adjustments on the R&LC HVAC sale to the Bosch Group. The 8-K cash flow statement shows the outflow in discontinued operations investing. notes:29 says the nine-month discontinued operations loss of $27 million reflects post-closing working capital, net debt and other adjustments.","account":"cash used by investing activities of discontinued operations","expected_direction":"down","horizon":"this quarter","quote":"the Company paid approximately $155 million related to final purchase price adjustments associated with the sale of the R&LC HVAC business to the Bosch Group","paragraph_id":"0000833444-26-000087:notes:32","explanation":false},
{"id":"earnings_quality_quarter_tax_rate_above_statutory","what_changed":"New quarter rate explanation: the three-month effective tax rate of 18.0% is above the 12.5% statutory rate, primarily because of tax rate differentials, partly offset by global tax planning. The prior-year quarter was described as below statutory. The 8-K (8k_2_02:164) states an adjusted effective tax rate of about 17% for the current periods and about 12% for the prior-year periods.","account":"income tax provision","expected_direction":"up","horizon":"this quarter","quote":"effective tax rate for continuing operations was 18.0% and was higher than the statutory tax rate of 12.5% primarily due to tax rate differentials","paragraph_id":"0000833444-26-000087:notes:110","explanation":false},
{"id":"earnings_quality_nine_month_tax_rate_divestiture_and_insurance_effects","what_changed":"The nine-month rate explanation attributes the above-statutory rate to the tax on AFFF insurance proceeds, the tax impact of current and 'planned' divestitures, and rate differentials. 'Planned' now lines up with the new ADT UK held-for-sale classification. Last quarter's six-month wording is not in my input, so I cannot say which drivers are new.","account":"income tax provision","expected_direction":"up","horizon":"next quarter","quote":"the tax impact of current and planned divestitures","paragraph_id":"0000833444-26-000087:notes:111","explanation":false},
{"id":"structure_and_disclosure_changes_yen_net_investment_hedge_designation_absent","what_changed":"The net investment hedge paragraph lists only EUR 2.9 billion of designated debt at June 30, 2026. At September 30, 2025 it lists the euro designation plus a yen 30 billion designation for yen subsidiaries, so the yen designation is no longer listed at period end. Last quarter's text is not in my input, so I cannot tell which quarter the yen designation ended in.","account":"accumulated other comprehensive income (CTA); net financing charges","expected_direction":"none","horizon":"this quarter","quote":"As of June 30, 2026, the Company had designated debt obligations of €2.9 billion as partial hedges of its investments in certain euro-denominated subsidiaries.","paragraph_id":"0000833444-26-000087:notes:80","explanation":false},
{"id":"narrative_signs_of_operating_pressure_middle_east_energy_and_supply_costs","what_changed":"The geopolitical paragraph now says plainly that the ongoing Middle East conflicts have disrupted energy supplies and supply chains, raised energy and other supply costs, and created capital market volatility. The paragraph is carried as changed; last quarter's wording is not in my input.","account":"cost of sales","expected_direction":"up","horizon":"next quarter","quote":"The ongoing conflicts in the Middle East have disrupted energy supplies and supply chains, increased costs for energy and other supplies and created volatility in the capital markets, among other impacts.","paragraph_id":"0000833444-26-000087:mdna:13","explanation":false},
{"id":"narrative_signs_of_operating_pressure_emea_growth_constrained_by_middle_east","what_changed":"Q3 EMEA sales prose says organic growth was constrained by continued pressure from the Middle East conflicts. The nine-month EMEA prose (mdna:58) and the 8-K EMEA paragraph (8k_2_02:29) say the same. The prose attributes EMEA's reported decrease to divestitures, partly offset by organic growth and currency.","account":"net sales (EMEA segment)","expected_direction":"down","horizon":"next quarter","quote":"as growth was constrained by continued pressure in the region due to the conflicts in the Middle East","paragraph_id":"0000833444-26-000087:mdna:54","explanation":false},
{"id":"estimates_and_discretion_ieepa_tariff_refund_participation","what_changed":"The tariff paragraph reports that certain IEEPA tariffs were invalidated by the U.S. Supreme Court in February 2026 and replaced by new tariffs. The Company says it is participating in the IEEPA refund process, and that refunds claimed have not had a material impact to date. No receivable or gain is described.","account":"other current assets (tariff refund claims); cost of sales","expected_direction":"none","horizon":"12 months","quote":"The Company is participating in the IEEPA refund process.","paragraph_id":"0000833444-26-000087:mdna:12","explanation":false},
{"id":"revenue_recognition_change_orders_asserted_for_tariff_and_conflict_costs","what_changed":"The mitigation paragraph now names geopolitical conflict next to trade restrictions. The listed actions include accelerating pricing and 'asserting contractual rights through change orders'. Change orders are contract modifications or variable consideration under long-term contracts, which bear on revenue estimates. The paragraph is carried as changed; last quarter's wording is not in my input.","account":"net sales; contract assets","expected_direction":"up","horizon":"next quarter","quote":"accelerating pricing actions and asserting contractual rights through change orders","paragraph_id":"0000833444-26-000087:mdna:14","explanation":false},
{"id":"controls_audit_and_filings_risk_factors_updated_but_not_in_input","what_changed":"MD&A says risk factors were updated and supplemented in Part II, Item 1A of this 10-Q. My directory has no Item 1A diff, so the content of the update is insufficient for this reader.","account":"none","expected_direction":"none","horizon":"this quarter","quote":"Certain of these risk factors have been updated and supplemented in Part II, Item 1A of this Quarterly Report on Form 10-Q.","paragraph_id":"0000833444-26-000087:mdna:18","explanation":false},
{"id":"results_against_expectations_full_year_guidance_raised","what_changed":"The 8-K raises full-year fiscal 2026 guidance: organic sales growth of ~8% (previously ~6%) and adjusted EPS of ~$5.05 (previously ~$4.85). Adjusted free cash flow conversion stays at ~100%. It also starts Q4 guidance: organic growth of 9% to 10%, operating leverage of 45% to 50%, adjusted EPS of ~$1.55.","account":"net sales; adjusted EPS (non-GAAP)","expected_direction":"up","horizon":"next quarter","quote":"Organic sales growth of ~8% (previously up ~6%)","paragraph_id":"0000833444-26-000083:8k_2_02:51","explanation":false},
{"id":"results_against_expectations_operating_leverage_guidance_changed_to_range","what_changed":"Full-year operating leverage guidance went from a point estimate (~50%) to a range (45% to 50%), in the same release that raised sales and EPS guidance. I have not judged the size of the change.","account":"adjusted EBIT (non-GAAP)","expected_direction":"none","horizon":"next quarter","quote":"Operating leverage of 45% to 50% (previously ~50%)","paragraph_id":"0000833444-26-000083:8k_2_02:52","explanation":false},
{"id":"across_documents_orders_growth_compares_unrestated_prior_orders","what_changed":"The 8-K says orders before Q1 2026 exclude certain equipment-only sales for longer-cycle projects, and that backlog, but not prior orders, has been restated to include this new category. The headline year-over-year orders growth (27% total, 37% Americas, repeated in mdna:77-81) is therefore measured against prior-period orders on the narrower definition. The MD&A orders table footnote (mdna:78) does not mention this.","account":"orders (non-GAAP operating metric)","expected_direction":"none","horizon":"this quarter","quote":"Orders prior to Q1 2026 exclude certain equipment-only sales for longer cycle projects. Backlog has been restated to include this new category.","paragraph_id":"0000833444-26-000083:8k_2_02:18","explanation":false},
{"id":"results_against_expectations_orders_and_backlog_growth_data_centers","what_changed":"Q3 MD&A says orders rose 27% on sustained demand for large projects, including large-scale data center projects. Backlog rose 32%, led by Products and Systems, to $21.0 billion. Americas orders rose 37%, led by 55% Products and Systems growth. The 8-K (8k_2_02:24) credits data centers and other mission-critical environments. Per the prose, this implies revenue growth over the coming year.","account":"net sales","expected_direction":"up","horizon":"12 months","quote":"Orders increased 27%, reflecting sustained demand in large projects across the","paragraph_id":"0000833444-26-000087:mdna:80","explanation":false},
{"id":"narrative_signs_of_operating_pressure_americas_services_backlog_decrease","what_changed":"Q3 MD&A states that Americas Services backlog decreased 1% while Products and Systems backlog grew. Americas Services orders grew 4% (mdna:81). This is the only segment and line where the prose reports a backlog decrease.","account":"net sales (Americas services)","expected_direction":"down","horizon":"12 months","quote":"led by 47% growth in Products and Systems, partially offset by a 1% decrease in Services","paragraph_id":"0000833444-26-000087:mdna:86","explanation":false},
{"id":"liquidity_and_capital_working_capital_receivables_increase_without_stated_cause","what_changed":"MD&A attributes the working capital change since September 30, 2025 to higher cash and accounts receivable and lower accrued compensation and current long-term debt, partly offset by higher deferred revenue and accounts payable. It names the receivables increase as a driver but gives no cause for it: no mention of collections, terms, mix or contract assets. Contract assets are carried inside accounts receivable (notes:40).","account":"accounts receivable - net","expected_direction":"up","horizon":"this quarter","quote":"primarily due to increases in cash and accounts receivable and decreases in accrued compensation and the current portion of long-term debt, partially offset by increases in deferred revenue and accounts payable","paragraph_id":"0000833444-26-000087:mdna:96","explanation":false},
{"id":"liquidity_and_capital_open_market_repurchases_resumed_after_asr","what_changed":"MD&A states that the ASR completed in Q2 and that open market repurchases resumed after final settlement. Total repurchases since the program began: $5.0 billion for 43,693,817 shares at an average of $114.43. About $3.9 billion of authorization remains, with no expiration. The 8-K cash flow statement shows stock repurchases in the quarter.","account":"stock repurchases (financing cash flow); shares outstanding","expected_direction":"down","horizon":"next quarter","quote":"resumed open market repurchases after final settlement of the ASR transactions","paragraph_id":"0000833444-26-000087:mdna:105","explanation":false},
{"id":"earnings_quality_corporate_expense_incentive_accruals_and_timing","what_changed":"The 8-K attributes the year-over-year rise in adjusted Corporate expense to higher corporate incentive compensation accruals and to the 'timing of certain corporate expenses'. The timing language implies some expense moved between periods.","account":"corporate expense; accrued compensation and benefits","expected_direction":"up","horizon":"this quarter","quote":"The increase year-over-year is primarily due to increased corporate accruals related to incentive compensation and the timing of certain corporate expenses.","paragraph_id":"0000833444-26-000083:8k_2_02:40","explanation":false},
{"id":"earnings_quality_adjusted_free_cash_flow_royalty_and_tax_exclusions","what_changed":"The adjusted free cash flow definition excludes several items: prepaid royalty fees for IP licensed to divested businesses, discrete non-US tax settlement payments, JC Capital cash flows, and AFFF settlement payments and insurance cash receipts. The reconciliation (8k_2_02:133) shows nine-month adjustments for the royalty prepayment and discrete tax lines. The prior release is not in my input, so I cannot confirm which exclusions are new this year.","account":"adjusted free cash flow (non-GAAP)","expected_direction":"none","horizon":"this quarter","quote":"Prepayment of royalty fees associated with certain IP licensed to divested businesses.","paragraph_id":"0000833444-26-000083:8k_2_02:96","explanation":false},
{"id":"across_documents_quarter_other_impairments_cause_not_stated","what_changed":"The MD&A restructuring and impairment table (mdna:36) shows an 'Other impairments' line for the three months. The prose (mdna:37) points to Note 3 and Note 14. In my input, Note 3 text reports no write-down for ADT UK and puts the ADT Spain impairment in Q1. The restructuring note narrative (notes:102-104) is unchanged from last quarter. No text I have names the cause of the Q3 other impairments.","account":"restructuring and impairment costs","expected_direction":"none","horizon":"this quarter","quote":"restructuring actions and impairment costs.","paragraph_id":"0000833444-26-000087:mdna:37","explanation":false}
]
```

Count: 37 items. None is flagged `explanation`: nowhere in my input does management explain the cause of a receivables, inventory or reserve number. mdna:96 names the receivables increase without giving a cause.

## Paragraphs carried as text that are not items

The short IDs below belong to filing 0000833444-26-000087 unless they start with `8k_2_02` (filing 0000833444-26-000083) or carry a full accession number. "Insufficient" means the paragraph changed but the prior text is not in my input, so I cannot determine what changed.

### Item 4 (input_controls.md)
- item_4_controls:1 — heading
- item_4_controls:2 — heading
- item_4_controls:3 — evaluation-date sentence, date rolled forward
- item_4_controls:4 — effectiveness conclusion unchanged, date rolled forward
- item_4_controls:5 — heading
- item_4_controls:6 — "no significant changes" sentence, date rolled forward (cited in the cash flow revision item)
- item_4_controls:7 — page number

### MD&A (input_mdna.md)
- mdna:5 — business description reworded (same text as notes:4); no accounting substance
- mdna:7 — continuation of mdna:5; wording only
- mdna:8 — business description reworded ("fully integrated industrial technology company"); no accounting substance
- mdna:9 — period references, dates rolled forward
- mdna:15 — continuation of mdna:14; insufficient
- mdna:17 — AI and data center demand trend paragraph; insufficient (its substance overlaps the orders item)
- mdna:20 — net sales table, amounts only
- mdna:21 — Q3 sales bridge, amounts only; drivers restated for the quarter
- mdna:22 — nine-month sales bridge, amounts only
- mdna:25 — gross profit table, amounts only
- mdna:26 — gross profit drivers (organic growth, productivity, leverage) restated for the period; no estimate or policy change
- mdna:29 — SG&A table, amounts only
- mdna:30 — three-month SG&A driver ($16 million AFFF recoveries); covered by the AFFF across-documents item
- mdna:32 — cross-reference to Note 18
- mdna:36 — restructuring and impairment table, amounts only; covered by the other-impairments item
- mdna:38 — page number
- mdna:42 — tax table, amounts only
- mdna:50 — segment sales table, amounts only
- mdna:52 — Americas Q3 sales bridge, amounts only
- mdna:53 — EMEA Q3 bridge first half, amounts only (second half is an item)
- mdna:55 — APAC Q3 bridge, amounts only
- mdna:57 — Americas nine-month bridge, amounts only
- mdna:58 — EMEA nine-month bridge; Middle East constraint covered by the EMEA item
- mdna:59 — APAC nine-month bridge, amounts only
- mdna:61 — segment EBIT table, amounts only
- mdna:62 — segment EBITA table, amounts only
- mdna:64 — Americas EBIT driver (operating leverage), period results narrative
- mdna:65 — EMEA EBIT driver (pricing, productivity, divestitures), period results narrative
- mdna:66 — APAC EBIT driver (productivity, mix, revenue), period results narrative
- mdna:67 — page number
- mdna:70 — EMEA nine-month EBIT driver, period results narrative
- mdna:73 — segment EBIT reconciliation table, amounts only
- mdna:74 — heading
- mdna:75 — orders and backlog definition; insufficient (the definition change is covered from the 8-K side)
- mdna:76 — table lead-in
- mdna:77 — orders and backlog table, amounts only
- mdna:78 — table footnote, dates rolled forward (cited in the orders definition item)
- mdna:81 — Americas orders split; covered by the orders growth item
- mdna:82 — EMEA orders split, amounts only
- mdna:83 — APAC orders split, amounts only
- mdna:85 — backlog increase sentence; covered by the orders growth item
- mdna:87 — EMEA backlog split, amounts only
- mdna:88 — APAC backlog split, amounts only
- mdna:89 — RPO amount and date rolled forward, amounts only
- mdna:95 — working capital table, amounts only
- mdna:98 — cash flow summary table, amounts only
- mdna:100 — investing drivers; covered by the acquisition, ADT Spain and ADT Mexico items
- mdna:103 — capitalization table, amounts only
- mdna:106 — dividend declaration, period roll
- mdna:107 — liquidity adequacy statement, amount and date rolled forward
- mdna:109 — commercial paper outstanding, amounts only
- mdna:111 — revolver, no draws, date rolled forward
- mdna:112 — credit ratings lead-in, date rolled forward
- mdna:115 — covenant compliance, date rolled forward
- mdna:119 — guarantor notes lead-in; insufficient
- mdna:120 — guaranteed note listing; insufficient (prior list not in input)
- mdna:121 — guaranteed note listing; insufficient
- mdna:122 — guaranteed note listing; insufficient
- mdna:123 — guaranteed note listing; insufficient
- mdna:124 — guaranteed note listing; insufficient
- mdna:125 — guaranteed note listing; insufficient
- mdna:126 — guaranteed note listing; insufficient
- mdna:127 — guaranteed note listing; insufficient
- mdna:128 — guaranteed note listing; insufficient
- mdna:130 — Obligor Group lead-in, wording unchanged in substance
- mdna:131 — Obligor Group loss table, amounts only
- mdna:134 — Obligor Group balance table, amounts only

### Notes (input_notes.md)
- notes:1 — basis of presentation, period rolled forward
- notes:4 — business description reworded; no accounting substance
- notes:5 — business description reworded; no accounting substance
- notes:9 — heading
- notes:10 — ASU 2023-07 adoption; insufficient (no change identified)
- notes:11 — heading
- notes:12 — ASU 2023-09 pending; insufficient (no change identified)
- notes:13 — ASU 2024-03 pending; insufficient (no change identified)
- notes:14 — ASU 2025-06 pending; insufficient (no change identified)
- notes:15 — boilerplate
- notes:16 — heading
- notes:18 — heading
- notes:19 — heading
- notes:22 — heading
- notes:24 — heading
- notes:25 — ADT Mexico sale (Q1 event) repeated, period label rolled forward
- notes:26 — ADT Mexico held-for-sale history repeated
- notes:27 — heading
- notes:28 — R&LC background repeated
- notes:29 — R&LC discontinued operations loss, period rolled forward; cited in the R&LC payment item
- notes:30 — table lead-in
- notes:31 — prior-year discontinued operations table, amounts only
- notes:35 — revenue disaggregation table, amounts only
- notes:36 — revenue disaggregation table, amounts only
- notes:40 — contract balances table, amounts only
- notes:41 — revenue recognized from contract liabilities, amounts only
- notes:43 — RPO amount and two-year percentage, amounts only
- notes:47 — contract cost assets table, amounts only
- notes:48 — contract cost amortization, amounts only
- notes:50 — inventory table, amounts only
- notes:52 — goodwill rollforward, amounts only (footnote is an item)
- notes:55 — intangibles table, amounts only
- notes:56 — amortization, amounts only
- notes:58 — ROU supplemental table, amounts only
- notes:60 — supply chain finance balance, amounts only
- notes:61 — heading and lead-in
- notes:62 — short-term debt table, amounts only
- notes:63 — revolver, date rolled forward
- notes:64 — February 2026 note repayment; not shown as changed in the note change history (no new event this quarter)
- notes:65 — table lead-in
- notes:66 — net financing charges table, amounts only
- notes:67 — derivative gains and losses, amounts and wording only
- notes:68 — table lead-in
- notes:76 — fair value table, amounts only
- notes:77 — footnote cross-reference
- notes:81 — continuation of notes:80; covered by the yen hedge item
- notes:82 — fair value of foreign-currency debt, amounts only
- notes:83 — net investment hedge gains and losses, amounts only
- notes:88 — ETF valuation method; insufficient (no change identified)
- notes:89 — unrealized gains, amounts only
- notes:91 — table lead-in, date rolled forward
- notes:92 — long-term debt fair value table, amounts only
- notes:97 — EPS share table, amounts only
- notes:99 — AOCI table, amounts only
- notes:100 — pension heading and lead-in; insufficient (no change identified)
- notes:101 — pension cost table, amounts only
- notes:105 — restructuring by segment table, amounts only
- notes:107 — restructuring reserve rollforward table, amounts only
- notes:112 — prior-year quarter rate explanation, comparative period
- notes:113 — prior-year nine-month rate explanation, comparative period
- notes:114 — cross-reference
- notes:116 — unrecognized tax benefits and interest, amounts rolled forward
- notes:117 — prior-year statute expiration benefit, comparative period
- notes:119 — tax years under examination table; insufficient (prior table not in input)
- notes:120 — reasonably-possible tax conclusion sentence; insufficient (no change identified)
- notes:132 — segment table, amounts only
- notes:133 — segment table, amounts only
- notes:134 — table lead-in
- notes:135 — segment reconciliation table, amounts only (cited in the AFFF across-documents item)
- notes:136 — footnote cross-reference
- notes:141 — warranty rollforward table, amounts only
- notes:142 — heading; unchanged per note change history
- notes:143 — environmental accrual policy; unchanged per note change history
- notes:144 — environmental reserves table, amounts only
- notes:145 — environmental estimate period and range statement; unchanged per note change history
- notes:146 — FTC/Stanton Street reserve description; unchanged per note change history
- notes:148 — paragraph split with notes:149; wording only
- notes:149 — continuation of notes:148; wording only
- notes:150 — heading
- notes:151 — heading
- notes:152 — unchanged per note change history
- notes:153 — unchanged per note change history
- notes:154 — unchanged per note change history
- notes:155 — heading
- notes:157 — remaining text unchanged; the removed sentence is an item
- notes:159 — Town of Peshtigo case; unchanged per note change history
- notes:160 — Dane County actions; unchanged per note change history
- notes:162 — heading
- notes:163 — heading
- notes:164 — paragraph split with notes:165; wording only
- notes:165 — continuation; wording only
- notes:166 — unchanged per note change history
- notes:167 — heading
- notes:168 — municipal case count; unchanged per note change history
- notes:169 — unchanged per note change history
- notes:170 — heading
- notes:171 — settlement terms; unchanged per note change history
- notes:173 — unchanged per note change history
- notes:174 — heading
- notes:176 — continuation of notes:175; covered by the Val D'Or item
- notes:177 — heading
- notes:178 — mass action count; unchanged per note change history
- notes:179 — unchanged per note change history
- notes:180 — heading
- notes:181 — unchanged per note change history
- notes:182 — unchanged per note change history
- notes:183 — unchanged per note change history
- notes:184 — paragraph split with notes:185; wording only
- notes:185 — continuation; wording only
- notes:186 — state AG count; unchanged per note change history
- notes:187 — unchanged per note change history
- notes:188 — heading
- notes:189 — unchanged per note change history
- notes:190 — unchanged per note change history
- notes:191 — unchanged per note change history
- notes:192 — unchanged per note change history
- notes:195 — heading
- notes:196 — unchanged per note change history
- notes:197 — table lead-in
- notes:198 — asbestos table, amounts only
- notes:199 — table lead-in
- notes:200 — asbestos assets table, amounts only
- notes:201 — asbestos estimate assumptions; unchanged per note change history
- notes:202 — heading
- notes:203 — self-insurance policy; unchanged per note change history
- notes:204 — table lead-in
- notes:205 — self-insured table, amounts only
- notes:206 — heading
- notes:207 — other matters; unchanged per note change history
- notes:208 — table lead-in

### Note change history (input_notes_history.md)
I used this file to find changes. It is not a second list to report. Its entries map to the notes as follows:
- note_history:1–33 map to notes:142–205
- note_history:34–39 map to notes:1, notes:4, notes:5 and notes:8
- note_history:40–49 map to notes:61–68 and notes:91–92
- note_history:50–60 map to notes:35–48

Two removed prior-period paragraphs are cited directly as items: 0000833444-26-000050:note_history:6 and 0000833444-26-000050:note_history:22. The other removed ones are:
- 0000833444-26-000050:note_history:21 — re-split into notes:149; wording only
- 0000833444-26-000050:note_history:23 — replaced by notes:158 (item)
- 0000833444-26-000050:note_history:24 — replaced by notes:194 (item)
- 0000833444-26-000050:note_history:25, 26, 32, 33 — prior tables, amounts only
- 0000833444-26-000050:note_history:38, 39 — prior business description; wording only
- 0000833444-26-000050:note_history:44, 49 — prior debt tables, amounts only
- 0000833444-26-000050:note_history:60 — prior contract liability amounts only

### 8-K 0000833444-26-000083, Item 2.02 / Exhibit 99.1 (input_8k.md)
The item-code list for earlier 8-Ks gives codes only, with no bodies, so there is no text to assess. One late filing is listed: NT 10-K for fiscal 2023, filed 2023-11-29. It is historical and not new this period.
- 8k_2_02:1 — exhibit header
- 8k_2_02:2 — header
- 8k_2_02:3 — header
- 8k_2_02:4 — header
- 8k_2_02:5 — headline; guidance raise covered by item
- 8k_2_02:6 — rule
- 8k_2_02:7 — Q3 sales growth, amounts only
- 8k_2_02:8 — Q3 EPS, amounts only
- 8k_2_02:9 — orders growth; covered by the orders items
- 8k_2_02:10 — backlog; covered by the orders items
- 8k_2_02:11 — non-GAAP boilerplate
- 8k_2_02:12 — rule
- 8k_2_02:13 — Q3 EPS, amounts only
- 8k_2_02:14 — Q3 sales, amounts only
- 8k_2_02:15 — net income, amounts only
- 8k_2_02:16 — CEO quote; no estimate, policy or commitment
- 8k_2_02:17 — heading
- 8k_2_02:19 — website reference
- 8k_2_02:20 — page number
- 8k_2_02:21 — heading
- 8k_2_02:22 — Americas table, amounts only
- 8k_2_02:23 — Americas sales narrative, amounts only
- 8k_2_02:24 — Americas orders and backlog; covered by the orders growth item
- 8k_2_02:25 — Americas margin driver, period results narrative
- 8k_2_02:26 — page number
- 8k_2_02:27 — heading
- 8k_2_02:28 — EMEA table, amounts only
- 8k_2_02:29 — EMEA sales narrative; covered by the EMEA Middle East item
- 8k_2_02:30 — EMEA orders and backlog, amounts only
- 8k_2_02:31 — EMEA margin driver, period results narrative
- 8k_2_02:32 — heading
- 8k_2_02:33 — APAC table, amounts only
- 8k_2_02:34 — APAC sales narrative, amounts only
- 8k_2_02:35 — APAC orders and backlog, amounts only
- 8k_2_02:36 — APAC margin driver, period results narrative
- 8k_2_02:37 — page number
- 8k_2_02:38 — heading
- 8k_2_02:39 — corporate expense table, amounts only
- 8k_2_02:41 — heading
- 8k_2_02:42 — operating and free cash flow, amounts only
- 8k_2_02:43 — dividends paid, amounts only
- 8k_2_02:44 — heading
- 8k_2_02:45 — forward-looking non-GAAP boilerplate
- 8k_2_02:46 — Q4 guidance lead-in; covered by the guidance item
- 8k_2_02:47 — Q4 organic growth guidance; covered by the guidance item
- 8k_2_02:48 — Q4 operating leverage guidance; covered by the guidance item
- 8k_2_02:49 — Q4 adjusted EPS guidance; covered by the guidance item
- 8k_2_02:50 — lead-in
- 8k_2_02:53 — full-year EPS guidance; covered by the guidance item
- 8k_2_02:54 — FCF conversion guidance unchanged
- 8k_2_02:55 — page number
- 8k_2_02:56 — heading
- 8k_2_02:57 — call logistics
- 8k_2_02:58 — heading
- 8k_2_02:59 — boilerplate
- 8k_2_02:60 — boilerplate
- 8k_2_02:61 — boilerplate
- 8k_2_02:62 — heading
- 8k_2_02:63 — contacts
- 8k_2_02:64 — separator
- 8k_2_02:65 — page number
- 8k_2_02:66 — heading (the forward-looking statement text is not carried)
- 8k_2_02:67 — page number
- 8k_2_02:68 — heading
- 8k_2_02:69 — heading
- 8k_2_02:70 — heading
- 8k_2_02:71 — heading
- 8k_2_02:72 — income statement, amounts only
- 8k_2_02:73 — page number
- 8k_2_02:74 — heading
- 8k_2_02:75 — heading
- 8k_2_02:76 — heading
- 8k_2_02:77 — balance sheet, amounts only
- 8k_2_02:78 — page number
- 8k_2_02:79 — heading
- 8k_2_02:80 — heading
- 8k_2_02:81 — cash flow statement, amounts only
- 8k_2_02:82 — page number
- 8k_2_02:83 — heading
- 8k_2_02:84 — heading
- 8k_2_02:85 — R&LC sale background repeated
- 8k_2_02:86 — heading
- 8k_2_02:87 — non-GAAP boilerplate
- 8k_2_02:88 — heading
- 8k_2_02:89 — organic sales definition
- 8k_2_02:90 — heading
- 8k_2_02:91 — FCF rationale boilerplate
- 8k_2_02:92 — lead-in
- 8k_2_02:93 — JC Capital exclusion definition; covered by the adjusted FCF item
- 8k_2_02:94 — factoring program discontinued March 2024, repeated
- 8k_2_02:95 — AFFF cash exclusion definition; covered by the adjusted FCF item
- 8k_2_02:97 — discrete tax payments definition; covered by the adjusted FCF item
- 8k_2_02:98 — heading
- 8k_2_02:99 — boilerplate
- 8k_2_02:100 — page number
- 8k_2_02:101 — lead-in
- 8k_2_02:102 — mark-to-market definition
- 8k_2_02:103 — restructuring and impairment definition
- 8k_2_02:104 — AFFF definition
- 8k_2_02:105 — transaction/separation definition
- 8k_2_02:106 — transformation costs definition
- 8k_2_02:107 — ERP accelerated depreciation definition (trailing-twelve-month item from earlier quarters)
- 8k_2_02:108 — divestiture gain/loss definition
- 8k_2_02:109 — EMEA joint venture loss definition (prior-year trailing-twelve-month item)
- 8k_2_02:110 — discrete tax items definition
- 8k_2_02:111 — related tax impact definition
- 8k_2_02:112 — boilerplate
- 8k_2_02:113 — heading
- 8k_2_02:114 — operating leverage definition
- 8k_2_02:115 — heading
- 8k_2_02:116 — debt ratio rationale
- 8k_2_02:117 — page number
- 8k_2_02:118 — heading
- 8k_2_02:119 — lead-in
- 8k_2_02:120 — sales bridge table, amounts only
- 8k_2_02:121 — sales bridge table, amounts only
- 8k_2_02:122 — page number
- 8k_2_02:123 — products and systems bridge table, amounts only
- 8k_2_02:124 — products and systems bridge table, amounts only
- 8k_2_02:125 — page number
- 8k_2_02:126 — service bridge table, amounts only
- 8k_2_02:127 — service bridge table, amounts only
- 8k_2_02:128 — page number
- 8k_2_02:129 — heading
- 8k_2_02:130 — lead-in
- 8k_2_02:131 — cash flow conversion table, amounts only
- 8k_2_02:132 — lead-in
- 8k_2_02:133 — adjusted FCF table, amounts only (cited in the adjusted FCF item)
- 8k_2_02:134 — page number
- 8k_2_02:135 — heading
- 8k_2_02:136 — lead-in
- 8k_2_02:137 — EBIT reconciliation table, amounts only
- 8k_2_02:138 — footnote
- 8k_2_02:139 — page number
- 8k_2_02:140 — lead-in
- 8k_2_02:141 — segment reconciliation table, amounts only
- 8k_2_02:142 — segment reconciliation table, amounts only
- 8k_2_02:143 — page number
- 8k_2_02:144 — lead-in
- 8k_2_02:145 — adjusted segment EBITA margin table, amounts only
- 8k_2_02:146 — lead-in
- 8k_2_02:147 — corporate expense reconciliation table, amounts only
- 8k_2_02:148 — heading
- 8k_2_02:149 — lead-in
- 8k_2_02:150 — EPS reconciliation table, amounts only
- 8k_2_02:151 — footnote
- 8k_2_02:152 — page number
- 8k_2_02:153 — EPS reconciliation table, amounts only
- 8k_2_02:154 — footnote
- 8k_2_02:155 — lead-in
- 8k_2_02:156 — share count table, amounts only
- 8k_2_02:157 — page number
- 8k_2_02:158 — heading
- 8k_2_02:159 — lead-in
- 8k_2_02:160 — debt ratio table, amounts only
- 8k_2_02:161 — lead-in
- 8k_2_02:162 — trailing-twelve-month adjusted EBITDA table, amounts only
- 8k_2_02:163 — heading
- 8k_2_02:164 — adjusted effective tax rate; covered by the quarter tax rate item
- 8k_2_02:165 — page number

## Insufficient count

28 paragraphs are marked insufficient, plus 1 item (the Item 1A update, whose content is not in my input). The 28:
- mdna: 15, 17, 75, 119–128 (13)
- notes: 10, 12, 13, 14, 88, 100, 119, 120 (8)
- 8-K: none
- Inputs absent from the directory: Item 1A diff, Exhibit 21 diff, Exhibit 10, auditor's report (4 inputs, not paragraphs)

The remaining 3 come from the item list's own caveats: notes:80 (which quarter the yen designation ended), notes:111 (which tax drivers are new) and 8k_2_02:96 (which adjusted FCF exclusions are new). The prior-period text for each is not in my input.
