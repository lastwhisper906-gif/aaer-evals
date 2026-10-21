# OMCL 10-Q 0000926326-26-000022 (quarter ended June 30, 2026): notes-text reader

## Scope

- **Inputs read in full:**
  - input_notes.md (notes:1–171)
  - input_notes_history.md
  - input_mdna.md (mdna:1–158)
  - input_controls.md (item_4_controls:1–9)
  - input_8k.md (the item-code index, plus the Item 2.02 / Exhibit 99.1 body 8k_2_02:1–100)
  - input_prior_predictions.md (none on record)
- **Not in the directory:**
  - no auditor's report (this is a 10-Q, and none is carried)
  - no Item 1A diff
  - no Exhibit 21 diff
  - no Exhibit 10
  - no 8-K bodies other than the 2026-07-30 Item 2.02 release. The 2026-07-01 Item 5.02 and the 2026-05-26 Items 5.02, 5.03 and 5.07 appear on the index only.
- **Late filings:** the only late-filing notice on the index is a 2015 NT 10-K. Nothing is new there.
- **Out-of-bounds material:** none found. There is no trend table, price, return, short-interest or outcome data, and no other company's files. The 8-K body carries its own financial tables. I read them as 8-K text and computed nothing from them.
- **Limits:**
  - No arithmetic or magnitude comparison was done anywhere in this report.
  - Where two documents state different figures, I report the figures as stated and leave reconciliation to the numbers reader and the supervisor.
  - Where a paragraph is carried as changed text but its prior wording is not in my input, the item or the line says so.

## Items

```json
[
  {
    "id": "narrative_signs_of_operating_pressure_purchasing_decision_timing",
    "what_changed": "The forward-looking risk bullet on installation delays is carried as changed text. It now reads 'or in the timing of purchasing decisions'. The prior bullet is not in my input, so I can't confirm that this clause is the edit. It lines up with the 8-K's updated product bookings and ARR guidance language (8k_2_02:25) and the 8-K's Titan XT purchase-timing risk (8k_2_02:36).",
    "account": "product bookings; product revenues",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "delays in installations of our medication management solutions or our more complex medication packaging systems, or in the timing of purchasing decisions",
    "paragraph_id": "0000926326-26-000022:mdna:8",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_semiconductor_chip_supply",
    "what_changed": "The raw-materials risk bullet is carried as changed text and appears to have moved; the prior-period paragraph it replaces is not carried. It now names semiconductor chips in particular, along with price fluctuations and an inability to pass increased costs on to customers. The prior wording is not in my input, so the exact edit is inferred.",
    "account": "cost of product revenues; inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "availability and sources of raw materials and components, in particular with regard to semiconductor chips, price fluctuations and an inability to pass increased costs on to our customers, or shortages or interruptions of supply",
    "paragraph_id": "0000926326-26-000022:mdna:19",
    "explanation": false
  },
  {
    "id": "earnings_quality_ieepa_tariff_refund_reduces_product_cost",
    "what_changed": "New prose. In Q2 2026 the company received refunds of previously paid IEEPA tariffs and recorded them primarily as a reduction to cost of product revenues. Recognition is described on receipt. The prose does not say where the portion not recorded in cost of product revenues went, apart from the $0.5 million of interest income named in mdna:113.",
    "account": "cost of product revenues",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the second quarter of 2026, the Company received $14.5 million in refunds for previously paid IEEPA tariffs, which were recorded primarily as a reduction to cost of product revenues.",
    "paragraph_id": "0000926326-26-000022:mdna:49",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ieepa_refund_not_expected_to_recur",
    "what_changed": "New prose. Management does not expect any further material refunds for IEEPA tariffs paid up to the February 20, 2026 ruling. The Q2 reduction to cost of product revenues is therefore presented as one-time, and the prose implies it will not repeat in later quarters.",
    "account": "cost of product revenues; product gross margin",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The Company does not expect any additional refunds potentially collectible in the future for IEEPA tariffs paid through the U.S. Supreme Court’s February 20, 2026 ruling to be material.",
    "paragraph_id": "0000926326-26-000022:mdna:49",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_replacement_tariffs",
    "what_changed": "New prose. The Section 122 tariff on all imports, imposed effective February 24, 2026, expired on July 24, 2026. Effective the same day, replacement tariffs under Section 301 were implemented or announced, at rates the prose gives as generally ranging from 10% to 12.5%. Management says it does not currently expect these changes to have a material impact. The cost-of-revenue explanations (mdna:101, mdna:103, mdna:106, mdna:108) keep citing 'ongoing tariffs' as a partial offset.",
    "account": "cost of product revenues",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Effective July 24, 2026, the U.S. implemented or announced replacement tariffs under Section 301 of the Trade Act of 1974, at rates generally ranging from 10% to 12.5%, which are intended to replace the expired Section 122 tariffs.",
    "paragraph_id": "0000926326-26-000022:mdna:50",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_long_term_care_customer_financial_strain",
    "what_changed": "The Institutional Pharmacy market description is carried as changed text across mdna:74 and mdna:75; the prior paragraph it replaces is not in my input. It now says legislative and pricing reforms, including Medicare Part D updates, have increased financial strain on smaller LTC providers. Management presents this as speeding a shift to centralized, automation-enabled fulfillment, but it is also a statement about customer financial condition. In the same filing, mdna:112 and mdna:116 report a decrease in the allowance for credit losses.",
    "account": "allowance for credit losses on accounts receivable (long-term care pharmacy customers)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Legislative and pricing reforms, including updates to Medicare Part D, have increased financial strain on smaller LTC providers",
    "paragraph_id": "0000926326-26-000022:mdna:75",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_developmental_disabilities_pharmacy_services",
    "what_changed": "The same rewritten passage now says the company provides pharmacy services to individuals with intellectual and developmental disabilities. It describes this as a market with rising demand that requires specialized packaging and adherence technologies. I can't confirm from my input whether this service line is newly described.",
    "account": "SaaS and Expert Services revenues",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Additionally, we provide pharmacy services to individuals with intellectual and developmental disabilities (“IDD”), a market currently experiencing rising demand due to increased prevalence.",
    "paragraph_id": "0000926326-26-000022:mdna:75",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_robotics_revenue_decline",
    "what_changed": "The Q2 product revenue explanation attributes growth to automated dispensing systems and the XTExtend offering. It says this growth was partially offset by a decrease in robotics revenues, including Central Pharmacy Dispensing Service and IV Compounding Service products. The six-month explanation (mdna:93) repeats the same offset.",
    "account": "product revenues (robotics: Central Pharmacy Dispensing Service, IV Compounding Service)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a decrease in revenues from robotics, including products related to our Central Pharmacy Dispensing Service and IV Compounding Service offering",
    "paragraph_id": "0000926326-26-000022:mdna:89",
    "explanation": false
  },
  {
    "id": "earnings_quality_technical_services_pricing_actions",
    "what_changed": "The Q2 service revenue explanation attributes the technical services increase partly to 'the impact of pricing actions', alongside growth in the installed customer base. It attributes the SaaS and Expert Services increase to continued customer demand, including Specialty Pharmacy Services. The six-month paragraph (mdna:94) repeats both causes.",
    "account": "technical services revenues",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "an increase of $4.8 million in technical services revenues primarily as a result of growth in our installed customer base and the impact of pricing actions",
    "paragraph_id": "0000926326-26-000022:mdna:90",
    "explanation": false
  },
  {
    "id": "across_documents_ieepa_refund_amount_stated_differently",
    "what_changed": "The IEEPA refund appears with different stated figures:\n- the 8-K (8k_2_02:17) says the company received $15 million;\n- MD&A mdna:49 says $14.5 million was received;\n- mdna:101, mdna:103, mdna:106 and mdna:108 say a $14.0 million refund drove the cost of product revenues and gross margin explanations;\n- mdna:113 and mdna:117 say $0.5 million of interest income was received in connection with the refund.\nThe prose itself does not reconcile these figures. Reconciliation is left to the numbers reader and the supervisor.",
    "account": "cost of product revenues; interest and other income (expense), net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "was primarily driven by a $14.0 million refund received during the three months ended June 30, 2026 for previously paid IEEPA tariffs",
    "paragraph_id": "0000926326-26-000022:mdna:101",
    "explanation": false
  },
  {
    "id": "earnings_quality_installation_efficiencies_and_mix",
    "what_changed": "The six-month cost of product revenues explanation gives four reasons cost did not increase proportionally with product revenues:\n- the IEEPA refund;\n- a favorable impact of scale and efficiencies in installations;\n- product mix;\n- customer mix.\nIt cites ongoing tariffs as a partial offset. The Q2 three-month explanation (mdna:101) does not name these operating causes.",
    "account": "product gross margin (cost of product revenues relative to product revenues)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "favorable impact of scale and efficiencies in installations as well as product and customer mix",
    "paragraph_id": "0000926326-26-000022:mdna:106",
    "explanation": false
  },
  {
    "id": "earnings_quality_prior_year_software_upgrade_costs_lapped",
    "what_changed": "The six-month cost of service revenues explanation says the increase was partly offset by non-recurring costs, including software upgrade expenses, incurred in the first half of 2025. Part of the six-month service margin comparison therefore rests on the absence of a one-time prior-year cost, which will not carry into later comparisons. mdna:108 repeats this in the gross margin explanation.",
    "account": "service gross margin (cost of service revenues)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by certain non-recurring costs, including software upgrade expenses, incurred during the six months ended June 30, 2025",
    "paragraph_id": "0000926326-26-000022:mdna:107",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_allowance_for_credit_losses_lower_provision",
    "what_changed": "The Q2 SG&A explanation names a decrease in the allowance for credit losses, against Q2 2025, as an offset to the SG&A increase. The six-month paragraph (mdna:116) names a $4.6 million decrease on the same basis. No cause for the lower credit-loss charge is given anywhere in the prose. It sits alongside two pieces of new prose about customer credit:\n- LTC customer financial strain (mdna:75);\n- the 8-K's lease-financing credit risk clause (8k_2_02:36).",
    "account": "allowance for credit losses (credit loss expense within selling, general, and administrative)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a decrease of $3.5 million in the allowance for credit losses compared to the three months ended June 30, 2025",
    "paragraph_id": "0000926326-26-000022:mdna:112",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_and_severance_charges",
    "what_changed": "The Q2 SG&A increase is attributed to an increase in employee-related expenses and an increase in 'certain restructuring and severance charges'. These line up with the 8-K's new Professional Services and product organization restructuring adjustments (8k_2_02:48, 8k_2_02:49). In the 8-K reconciliation those adjustments show no amounts in the 2025 columns.",
    "account": "selling, general, and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase of $3.3 million in employee-related expenses and an increase of $1.9 million in certain restructuring and severance charges",
    "paragraph_id": "0000926326-26-000022:mdna:112",
    "explanation": false
  },
  {
    "id": "earnings_quality_ieepa_refund_interest_income",
    "what_changed": "New prose. Interest income was received in connection with the IEEPA tariff refund in Q2 2026, and it partially offset the decrease in other income. The prose attributes that decrease to lower interest income on lower cash balances following the 2025 share repurchases and the September 2025 maturity of the 2025 Notes. This is a one-time item inside interest and other income.",
    "account": "interest and other income (expense), net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by $0.5 million of interest income received in connection with the IEEPA tariffs refund during the three months ended June 30, 2026",
    "paragraph_id": "0000926326-26-000022:mdna:113",
    "explanation": false
  },
  {
    "id": "earnings_quality_consulting_expense_increase",
    "what_changed": "The six-month SG&A explanation names an increase in consulting expenses, with no purpose given, alongside an increase in employee-related expenses. The named offsets are:\n- a decrease in the allowance for credit losses;\n- a decrease of $2.7 million in legal and regulatory expenses against the first half of 2025.\nThe 8-K (8k_2_02:45) describes those 2025 legal and regulatory expenses as settlement amounts for claims of non-compliance with government contracts.",
    "account": "selling, general, and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase of $2.6 million in consulting expenses",
    "paragraph_id": "0000926326-26-000022:mdna:116",
    "explanation": false
  },
  {
    "id": "revenue_recognition_receivables_increase_attributed_to_timing",
    "what_changed": "In the first-half 2026 operating cash flow discussion, management attributes the increase in accounts receivable and unbilled receivables primarily to the timing of billings, shipments and collections. This is management's explanation of a receivables movement. The 2025 comparative (mdna:143) used the same timing language for a decrease.",
    "account": "accounts receivable and unbilled receivables",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in accounts receivable and unbilled receivables of $10.2 million primarily due to the timing of billings, shipments, and collections",
    "paragraph_id": "0000926326-26-000022:mdna:142",
    "explanation": true
  },
  {
    "id": "revenue_recognition_deferred_revenue_billings_increase",
    "what_changed": "The deferred revenue increase is attributed primarily to an increase in billings for certain technical services, SaaS and Expert Services, and connected devices offerings. The 2025 comparative instead cited the timing of billings and customers' installation schedules. Read this with notes:47, which now says lump-sum invoicing is 'in advance'.",
    "account": "deferred revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in deferred revenues of $13.1 million, driven primarily by an increase in billings for certain technical services, SaaS and Expert Services, and connected devices offerings",
    "paragraph_id": "0000926326-26-000022:mdna:142",
    "explanation": false
  },
  {
    "id": "earnings_quality_inventory_decrease_without_stated_cause",
    "what_changed": "The operating cash flow discussion lists two working-capital inflows with no cause given for either:\n- a decrease in inventories;\n- a $4.0 million decrease in investment in sales-type leases.\nThe 2025 comparative did give a cause for its inventory movement (production requirements, including advanced purchases of certain components).",
    "account": "inventories",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a decrease in inventories of $4.2 million",
    "paragraph_id": "0000926326-26-000022:mdna:142",
    "explanation": false
  },
  {
    "id": "across_documents_operating_cash_flow_tariff_refund_not_named",
    "what_changed": "The MD&A operating cash flow explanation for the first half of 2026 does not name the IEEPA tariff refund. The 8-K (8k_2_02:17) says the refund increased cash flows in the period, and mdna:49 says no further material refunds are expected. Part of the period's operating inflow is therefore a non-recurring receipt that the cash flow narrative does not identify.",
    "account": "net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Net cash provided by operating activities was $122.8 million for the six months ended June 30, 2026, primarily consisting of operating inflows of $110.7 million and favorable working capital movements of $12.1 million.",
    "paragraph_id": "0000926326-26-000022:mdna:142",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_customer_funds_outflow",
    "what_changed": "The first-half 2026 financing outflow is attributed primarily to a net change in customer funds balances. The 2025 comparative attributed its financing outflow primarily to share repurchases. Funds held for customers (including restricted cash) and customer fund liabilities are separate lines in notes:61 and notes:62. No cause for the change in customer funds is given.",
    "account": "funds held for customers and customer fund liabilities; restricted cash",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to a net change in the customer funds balances of $23.9 million",
    "paragraph_id": "0000926326-26-000022:mdna:148",
    "explanation": false
  },
  {
    "id": "across_documents_contractual_obligations_no_significant_change",
    "what_changed": "MD&A says there have been no significant changes in the first half of 2026 to the contractual obligations disclosed in the 2025 Form 10-K. In the same filing, notes:136 restates non-cancelable purchase commitments at new amounts, and the MD&A table (mdna:153) lists purchase obligations. The 10-K figures are not in my input, so whether the 'no significant changes' statement holds is for the numbers reader and the supervisor.",
    "account": "purchase obligations; contractual obligations",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "There have been no significant changes during the six months ended June 30, 2026 to the contractual obligations disclosed in",
    "paragraph_id": "0000926326-26-000022:mdna:151",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_segment_expenses_recast",
    "what_changed": "The segment note is carried as changed text. It now says two things:\n- adjusted cost of product revenues excludes certain restructuring and severance charges;\n- certain prior-year significant expenses have been recast to match what the CODM received for the three and six months ended June 30, 2026.\nThe segment block is not in the note change history and its prior wording is not in my input, so which part is new can't be confirmed. It lines up with the 8-K excluding Professional Services restructuring from non-GAAP product gross profit (8k_2_02:39, 8k_2_02:48).",
    "account": "segment adjusted cost of product revenues; adjusted operating expenses",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "To align with the significant expenses provided to the CODM for the three and six months ended June 30, 2026, certain prior-year significant expenses have been recast to conform with current-period presentation.",
    "paragraph_id": "0000926326-26-000022:notes:19",
    "explanation": false
  },
  {
    "id": "revenue_recognition_lump_sum_advance_invoicing",
    "what_changed": "The deferred revenue paragraph now says portions of SaaS and Expert Services agreements may be invoiced lump sum 'in advance'. The prior text said only 'invoiced lump sum' (0000926326-26-000012:note_history:41). This makes explicit that some service billing runs ahead of performance, which bears on the timing of deferred revenues and operating cash flow (see mdna:142 on the increase in billings).",
    "account": "deferred revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In certain circumstances, portions of these agreements may be invoiced lump sum in advance.",
    "paragraph_id": "0000926326-26-000022:notes:47",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_conversion_sentence_partially_rolled_forward",
    "what_changed": "The 2029 Notes conversion sentence was only partly rolled forward:\n- rolled forward: 'three months ended June 30, 2026' and 'not convertible during the third quarter of 2026';\n- left as before: 'December 31, 2025' and 'first quarter of 2026'.\nAs filed, the sentence skips March 31, 2026 and the second quarter (compare 0000926326-26-000012:note_history:16). This is a drafting slip, not a change in terms.",
    "account": "convertible senior notes, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "During the three months ended June 30, 2026 and December 31, 2025, none of the conditional conversion features of the 2029 Notes were triggered",
    "paragraph_id": "0000926326-26-000022:notes:99",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_legacy_warrants_expired_unexercised",
    "what_changed": "New sentence: as of June 8, 2026, all warrants issued with the 2025 Notes have expired without exercise. The preceding sentence changed from 'terminate between' to 'expired between' December 15, 2025 and June 8, 2026. The legacy warrant overhang is gone, with no settlement or dilution.",
    "account": "anti-dilutive weighted-average shares related to convertible senior notes and warrants; diluted shares",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "As of June 8, 2026, all such warrants issued in connection with the 2025 Notes have expired without exercise.",
    "paragraph_id": "0000926326-26-000022:notes:115",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_non_cancelable_purchase_commitments",
    "what_changed": "The purchase commitment sentence is restated at June 30, 2026 with new amounts. The prior-quarter text, at March 31, 2026, stated $172.6 million, of which $133.7 million was expected to be paid in 2026 (0000926326-26-000012:note_history:4). No cause or purpose is given. The direction is left to the numbers reader.",
    "account": "purchase obligations (off-balance sheet); inventories",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, the Company had non-cancelable purchase commitments of $192.4 million, of which $134.1 million are expected to be paid within the year ending December 31, 2026.",
    "paragraph_id": "0000926326-26-000022:notes:136",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_irs_examination",
    "what_changed": "The income tax note, carried as changed text, says the company is in the early stages of an IRS examination of tax year 2023. The income tax block is not in the note change history and its prior wording is not in my input. I can't confirm whether the examination is newly disclosed or whether only the date was rolled forward. Gross unrecognized tax benefits are stated at $11.8 million (notes:145).",
    "account": "unrecognized tax benefits; provision for income taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company is currently in early stages of examination by the Internal Revenue Service (“IRS”) for the tax year ended December 31, 2023.",
    "paragraph_id": "0000926326-26-000022:notes:146",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_repurchase_programs_concluded",
    "what_changed": "New sentence: the 2025 Repurchase Program (authorized May 22, 2025) was formally concluded in Q2 2026; the 2016 program concluded in Q2 2025. No repurchases were made in the first half of 2026, and notes:170 now describes the 2025 program in the past tense. The prose does not say whether the authorization was used up or terminated. No new authorization is disclosed.",
    "account": "common stock repurchases (financing cash flow)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The 2016 and 2025 Repurchase Programs were formally concluded during the second quarter of 2025 and 2026, respectively.",
    "paragraph_id": "0000926326-26-000022:notes:171",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_high_end_of_expectations",
    "what_changed": "The earnings release says Q2 revenue came in at the high end of the company's expectations. The prior Q2 guidance is not in my input.",
    "account": "total revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "with quarterly revenue coming in at the high end of our expectations",
    "paragraph_id": "0000926326-26-000019:8k_2_02:9",
    "explanation": false
  },
  {
    "id": "across_documents_press_release_revenue_drivers_omit_robotics",
    "what_changed": "The release attributes the revenue increase to steady execution across the connected devices portfolio, in North America and internationally, plus SaaS and Expert Services and technical services. It mentions neither of two things the 10-Q MD&A discloses:\n- the decrease in robotics revenues (Central Pharmacy Dispensing Service, IV Compounding Service), named as a partial offset in mdna:89 and mdna:93;\n- the role of pricing actions in technical services (mdna:90).",
    "account": "product revenues",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The year-over-year increase in total revenues was driven by steady execution across our connected devices portfolio across both North America and international markets",
    "paragraph_id": "0000926326-26-000019:8k_2_02:13",
    "explanation": false
  },
  {
    "id": "earnings_quality_ieepa_refund_left_in_non_gaap_measures",
    "what_changed": "The release says the IEEPA refund reduced cost of product revenues and also increased GAAP net income, non-GAAP net income, non-GAAP EBITDA and cash flows. The refund is not one of the non-GAAP adjustments a) to i) defined in 8k_2_02:39–49. So a receipt that MD&A presents as non-recurring stays inside non-GAAP EBITDA and non-GAAP EPS, while the new restructuring charges are excluded.",
    "account": "non-GAAP EBITDA; non-GAAP net income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "and also increased the GAAP net income, non-GAAP net income, non-GAAP EBITDA, and cash flows in the period",
    "paragraph_id": "0000926326-26-000019:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_president_and_coo_appointment",
    "what_changed": "Subsequent event, after quarter-end: on July 1, 2026, Nnamdi Njoku was named President and Chief Operating Officer. The CEO stays CEO and Chairman. This corresponds to the 2026-07-01 Form 8-K (Items 5.02, 9.01) on the index, whose body is not in my input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "On July 1, 2026, Nnamdi Njoku was named President and Chief Operating Officer of Omnicell.",
    "paragraph_id": "0000926326-26-000019:8k_2_02:22",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_specialty_pharmacy_executive_roles",
    "what_changed": "Two newly created executive roles are disclosed:\n- Senior Vice President, Chief Pharmacy and Clinical Officer;\n- Senior Vice President and General Manager, Specialty Pharmacy Services, who will lead the expansion of specialty pharmacy and 340B capabilities.\nThis states an intended expansion of the specialty pharmacy line that MD&A names as a SaaS and Expert Services growth driver (mdna:90), and it adds senior headcount cost.",
    "account": "SaaS and Expert Services revenues; selling, general, and administrative",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Mr. Mandoli will lead the expansion of specialty pharmacy and 340B capabilities focused on strengthening customer value and supporting the Company’s long-term growth strategy.",
    "paragraph_id": "0000926326-26-000019:8k_2_02:23",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ebitda_and_eps_guidance_raised",
    "what_changed": "Full-year 2026 non-GAAP EBITDA and non-GAAP EPS guidance ranges are raised, citing strong Q2 profitability. Per 8k_2_02:17, Q2 non-GAAP profitability includes the IEEPA refund, and MD&A (mdna:49) says that refund will not materially recur. The release does not say how much of the raise rests on the refund. The new ranges are in 8k_2_02:26; the prior ranges are not in my input.",
    "account": "non-GAAP EBITDA; non-GAAP earnings per share (full year 2026)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we are increasing our full year 2026 non-GAAP EBITDA and non-GAAP earnings per share guidance ranges",
    "paragraph_id": "0000926326-26-000019:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_guidance_tightened",
    "what_changed": "Full-year 2026 revenue guidance ranges are tightened because the company is through the first half of the year. The release states no direction for the midpoint, and the prior ranges are not in my input.",
    "account": "total revenues (full year 2026)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "we are tightening our full year 2026 revenues guidance ranges",
    "paragraph_id": "0000926326-26-000019:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_product_bookings_guidance_updated",
    "what_changed": "Product bookings guidance is updated to reflect 'our current assessment of the range of potential outcomes'. The release states no direction. The new range is in 8k_2_02:26 and the prior range is not in my input. Read this with the Titan XT purchase-timing risk (8k_2_02:36) and the MD&A risk bullet on the timing of purchasing decisions (mdna:8).",
    "account": "product bookings",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We are also updating our product bookings guidance to reflect our current assessment of the range of potential outcomes for full year 2026",
    "paragraph_id": "0000926326-26-000019:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_arr_growth_opportunities_delayed",
    "what_changed": "ARR guidance is updated because certain growth opportunities are now expected to take longer to develop than previously projected. The release thus says some recurring-revenue growth will arrive later than planned. Related RPO figures:\n- notes:48 states remaining performance obligations not in deferred revenue at $375.1 million as of June 30, 2026;\n- the prior-quarter text stated $382.9 million as of March 31, 2026 (0000926326-26-000012:note_history:42).\nThe comparison is left to the numbers reader.",
    "account": "annual recurring revenue; SaaS and Expert Services revenues",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "our annual recurring revenue guidance to reflect certain growth opportunities that we now expect will take longer to develop than previously projected",
    "paragraph_id": "0000926326-26-000019:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_titan_xt_purchase_deferral_risk",
    "what_changed": "The release's risk list includes two related risks:\n- difficulty forecasting product bookings because of the size and mix of opportunities;\n- the announcement of Titan XT affecting purchasing decisions and their timing, meaning customers may wait for the next-generation platform.\nThe 8-K body is carried whole, not diffed, so whether this clause is new against the prior release is not in my input.",
    "account": "product bookings; product revenues",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "that the announcement of Titan XT may influence or impact purchasing decisions, including the timing of those decisions",
    "paragraph_id": "0000926326-26-000019:8k_2_02:36",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_lease_financing_credit_risk",
    "what_changed": "The release's risk list includes increased credit, collection and operational challenges from offering lease financing to customers. Related disclosures in the 10-Q:\n- notes:121 carries the net investment in sales-type leases;\n- mdna:142 lists a decrease in investment in sales-type leases with no cause given;\n- mdna:112 reports a decrease in the allowance for credit losses in the same period.\nWhether this clause is new against the prior release is not in my input.",
    "account": "net investment in sales-type leases; allowance for credit losses",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "the risk of increased credit, collection, and operational challenges from providing lease financing options to our customers",
    "paragraph_id": "0000926326-26-000019:8k_2_02:36",
    "explanation": false
  },
  {
    "id": "earnings_quality_professional_services_restructuring_excluded",
    "what_changed": "New non-GAAP adjustment h) excludes nonrecurring Professional Services restructuring charges. Per 8k_2_02:39, h) is excluded from non-GAAP product gross profit and gross profit, but not from service gross profit. The reconciliation shows the line under product gross profit and under operating expenses, with no amounts in the 2025 columns. So a restructuring of a services organization is charged to cost of product revenues.",
    "account": "cost of product revenues; operating expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "We excluded from our non-GAAP results nonrecurring restructuring charges related to organizational and resource adjustments within Professional Services to improve scalability and better align with evolving customer needs.",
    "paragraph_id": "0000926326-26-000019:8k_2_02:48",
    "explanation": false
  },
  {
    "id": "earnings_quality_product_organization_restructuring_excluded",
    "what_changed": "New non-GAAP adjustment i) excludes nonrecurring product organization restructuring charges, consisting primarily of severance. The reconciliation shows it under operating expenses, with no amounts in the 2025 columns. MD&A gives no cause for the Q2 R&D decrease (mdna:111) and attributes part of the SG&A increase to restructuring and severance charges (mdna:112).",
    "account": "operating expenses (research and development; selling, general, and administrative)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "We excluded from our non-GAAP results the nonrecurring charges related to the restructuring of the product organization to better align teams, resources, and priorities with our strategic goals and future growth plans.",
    "paragraph_id": "0000926326-26-000019:8k_2_02:49",
    "explanation": false
  }
]
```

## Paragraphs carried as text with no item

Lines marked "insufficient" are paragraphs carried as changed text whose prior wording is not in my input, where I could not identify a substantive edit.

### Item 4 (input_controls.md)

- 0000926326-26-000022:item_4_controls:1 — heading
- 0000926326-26-000022:item_4_controls:2 — heading
- 0000926326-26-000022:item_4_controls:3 — standard evaluation language
- 0000926326-26-000022:item_4_controls:4 — disclosure controls concluded effective. No prior text is carried to diff against, and no change in substance is stated.
- 0000926326-26-000022:item_4_controls:5 — heading
- 0000926326-26-000022:item_4_controls:6 — standard limitations language
- 0000926326-26-000022:item_4_controls:7 — heading
- 0000926326-26-000022:item_4_controls:8 — no ICFR change reported; period rolled forward
- 0000926326-26-000022:item_4_controls:9 — page number

### 8-K Item 2.02 body (input_8k.md)

- 0000926326-26-000019:8k_2_02:1 — exhibit header
- 0000926326-26-000019:8k_2_02:2 — document label
- 0000926326-26-000019:8k_2_02:3 — exhibit label
- 0000926326-26-000019:8k_2_02:4 — contact block
- 0000926326-26-000019:8k_2_02:5 — headline
- 0000926326-26-000019:8k_2_02:6 — promotional headline
- 0000926326-26-000019:8k_2_02:7 — headline; guidance substance itemized from 8k_2_02:25
- 0000926326-26-000019:8k_2_02:8 — dateline
- 0000926326-26-000019:8k_2_02:10 — CEO quote, promotional, no amount or commitment
- 0000926326-26-000019:8k_2_02:11 — CEO quote. The appointment is itemized from 8k_2_02:22; the Titan XT/OmniSphere mention is promotional.
- 0000926326-26-000019:8k_2_02:12 — heading
- 0000926326-26-000019:8k_2_02:14 — amounts only (GAAP net income, EPS)
- 0000926326-26-000019:8k_2_02:15 — amounts only (non-GAAP net income)
- 0000926326-26-000019:8k_2_02:16 — amounts only (non-GAAP EBITDA)
- 0000926326-26-000019:8k_2_02:18 — heading
- 0000926326-26-000019:8k_2_02:19 — amounts only (cash, debt, assets, operating cash flow)
- 0000926326-26-000019:8k_2_02:20 — amounts only; revolver availability and nil balance as before
- 0000926326-26-000019:8k_2_02:21 — heading
- 0000926326-26-000019:8k_2_02:24 — heading
- 0000926326-26-000019:8k_2_02:26 — guidance table, amounts only; the guidance changes are itemized from 8k_2_02:25
- 0000926326-26-000019:8k_2_02:27 — standard no-GAAP-guidance language
- 0000926326-26-000019:8k_2_02:28 — heading
- 0000926326-26-000019:8k_2_02:29 — conference call logistics
- 0000926326-26-000019:8k_2_02:30 — heading
- 0000926326-26-000019:8k_2_02:31 — company description
- 0000926326-26-000019:8k_2_02:32 — Reg FD channels
- 0000926326-26-000019:8k_2_02:33 — trademark notice
- 0000926326-26-000019:8k_2_02:34 — heading
- 0000926326-26-000019:8k_2_02:35 — standard forward-looking scope
- 0000926326-26-000019:8k_2_02:37 — heading
- 0000926326-26-000019:8k_2_02:38 — standard non-GAAP description
- 0000926326-26-000019:8k_2_02:39 — exclusion map; where h) and i) sit is itemized from 8k_2_02:48 and 8k_2_02:49
- 0000926326-26-000019:8k_2_02:40 — standard definition (share-based compensation)
- 0000926326-26-000019:8k_2_02:41 — standard definition (intangible amortization)
- 0000926326-26-000019:8k_2_02:42 — page number
- 0000926326-26-000019:8k_2_02:43 — standard definition (acquisition-related)
- 0000926326-26-000019:8k_2_02:44 — standard definition (debt issuance costs)
- 0000926326-26-000019:8k_2_02:45 — definition used only for 2025 comparatives; cited in earnings_quality_consulting_expense_increase
- 0000926326-26-000019:8k_2_02:46 — definition used only for 2025 comparatives
- 0000926326-26-000019:8k_2_02:47 — definition used only for 2025 comparatives
- 0000926326-26-000019:8k_2_02:50 — standard rationale
- 0000926326-26-000019:8k_2_02:51 — standard rationale
- 0000926326-26-000019:8k_2_02:52 — standard rationale
- 0000926326-26-000019:8k_2_02:53 — standard rationale
- 0000926326-26-000019:8k_2_02:54 — standard rationale
- 0000926326-26-000019:8k_2_02:55 — standard rationale
- 0000926326-26-000019:8k_2_02:56 — standard rationale lead-in
- 0000926326-26-000019:8k_2_02:57 — standard rationale
- 0000926326-26-000019:8k_2_02:58 — standard rationale
- 0000926326-26-000019:8k_2_02:59 — standard definition (non-GAAP diluted shares)
- 0000926326-26-000019:8k_2_02:60 — standard definition (free cash flow)
- 0000926326-26-000019:8k_2_02:61 — standard limitations
- 0000926326-26-000019:8k_2_02:62 — standard limitations
- 0000926326-26-000019:8k_2_02:63 — standard limitations
- 0000926326-26-000019:8k_2_02:64 — standard limitations
- 0000926326-26-000019:8k_2_02:65 — standard pointer to the tables
- 0000926326-26-000019:8k_2_02:66 — heading
- 0000926326-26-000019:8k_2_02:67 — heading
- 0000926326-26-000019:8k_2_02:68 — heading
- 0000926326-26-000019:8k_2_02:69 — income statement table, amounts only
- 0000926326-26-000019:8k_2_02:70 — page number
- 0000926326-26-000019:8k_2_02:71 — heading
- 0000926326-26-000019:8k_2_02:72 — heading
- 0000926326-26-000019:8k_2_02:73 — heading
- 0000926326-26-000019:8k_2_02:74 — balance sheet table, amounts only
- 0000926326-26-000019:8k_2_02:75 — heading
- 0000926326-26-000019:8k_2_02:76 — heading
- 0000926326-26-000019:8k_2_02:77 — heading
- 0000926326-26-000019:8k_2_02:78 — cash flow table, amounts only
- 0000926326-26-000019:8k_2_02:79 — page number
- 0000926326-26-000019:8k_2_02:80 — heading
- 0000926326-26-000019:8k_2_02:81 — heading
- 0000926326-26-000019:8k_2_02:82 — heading
- 0000926326-26-000019:8k_2_02:83 — reconciliation table, amounts only
- 0000926326-26-000019:8k_2_02:84 — heading
- 0000926326-26-000019:8k_2_02:85 — heading
- 0000926326-26-000019:8k_2_02:86 — heading
- 0000926326-26-000019:8k_2_02:87 — reconciliation table, amounts only
- 0000926326-26-000019:8k_2_02:88 — page number
- 0000926326-26-000019:8k_2_02:89 — heading
- 0000926326-26-000019:8k_2_02:90 — heading
- 0000926326-26-000019:8k_2_02:91 — heading
- 0000926326-26-000019:8k_2_02:92 — EBITDA reconciliation table, amounts only
- 0000926326-26-000019:8k_2_02:93 — rule line
- 0000926326-26-000019:8k_2_02:94 — standard tax-effect footnote
- 0000926326-26-000019:8k_2_02:95 — standard EBITDA definition footnote
- 0000926326-26-000019:8k_2_02:96 — heading
- 0000926326-26-000019:8k_2_02:97 — heading
- 0000926326-26-000019:8k_2_02:98 — heading
- 0000926326-26-000019:8k_2_02:99 — free cash flow table, amounts only
- 0000926326-26-000019:8k_2_02:100 — page number

### MD&A (input_mdna.md)

- 0000926326-26-000022:mdna:25 — insufficient: legal and regulatory risk bullet, no edit identifiable
- 0000926326-26-000022:mdna:28 — insufficient: credit-agreement covenant risk bullet, no edit identifiable
- 0000926326-26-000022:mdna:41 — trademark notice; wording
- 0000926326-26-000022:mdna:45 — amounts only (U.S. revenue share)
- 0000926326-26-000022:mdna:48 — insufficient: tariff background (years now '2025 and 2026'). The new tariff substance is itemized from mdna:49 and mdna:50.
- 0000926326-26-000022:mdna:52 — insufficient: KPI lead-in. The metrics named are still product bookings and ARR.
- 0000926326-26-000022:mdna:64 — amounts only (headcount)
- 0000926326-26-000022:mdna:74 — market sizing; first half of the passage itemized from mdna:75
- 0000926326-26-000022:mdna:83 — period rolled forward
- 0000926326-26-000022:mdna:85 — wording (cross-reference)
- 0000926326-26-000022:mdna:88 — amounts only (revenue table)
- 0000926326-26-000022:mdna:91 — amounts only (international share)
- 0000926326-26-000022:mdna:92 — amounts only (revenue table)
- 0000926326-26-000022:mdna:93 — six-month repeat of mdna:89 causes
- 0000926326-26-000022:mdna:94 — six-month repeat of mdna:90 causes
- 0000926326-26-000022:mdna:95 — amounts only (international share)
- 0000926326-26-000022:mdna:96 — insufficient: revenue-growth dependency text
- 0000926326-26-000022:mdna:98 — insufficient: cost-of-revenues composition text
- 0000926326-26-000022:mdna:99 — amounts only (cost table)
- 0000926326-26-000022:mdna:100 — amounts only (split of the change)
- 0000926326-26-000022:mdna:102 — cause is service volume; nothing new
- 0000926326-26-000022:mdna:103 — repeats the mdna:101 causes for gross margin
- 0000926326-26-000022:mdna:104 — amounts only (cost table)
- 0000926326-26-000022:mdna:105 — amounts only (split of the change)
- 0000926326-26-000022:mdna:108 — summarizes causes itemized from mdna:101, mdna:106 and mdna:107
- 0000926326-26-000022:mdna:110 — amounts only (opex table)
- 0000926326-26-000022:mdna:111 — amounts only; no cause given
- 0000926326-26-000022:mdna:114 — amounts only (opex table)
- 0000926326-26-000022:mdna:115 — amounts only; no cause given
- 0000926326-26-000022:mdna:117 — six-month repeat of mdna:113
- 0000926326-26-000022:mdna:118 — page number
- 0000926326-26-000022:mdna:119 — heading
- 0000926326-26-000022:mdna:120 — amounts only (tax table)
- 0000926326-26-000022:mdna:121 — amounts only (tax table)
- 0000926326-26-000022:mdna:122 — cause given as change in pre-tax income; amounts
- 0000926326-26-000022:mdna:125 — amounts and date rolled forward. The concentration sentence is also in notes:55; insufficient to tell whether it is new.
- 0000926326-26-000022:mdna:126 — lead-in
- 0000926326-26-000022:mdna:127 — amounts only (working capital table)
- 0000926326-26-000022:mdna:128 — amounts only (current ratio)
- 0000926326-26-000022:mdna:130 — heading
- 0000926326-26-000022:mdna:131 — credit agreement terms restated, unchanged
- 0000926326-26-000022:mdna:132 — date rolled forward; availability and compliance as before
- 0000926326-26-000022:mdna:133 — wording
- 0000926326-26-000022:mdna:136 — insufficient: liquidity sufficiency statement, which still asserts sufficiency for twelve months
- 0000926326-26-000022:mdna:139 — amounts only (cash flow table)
- 0000926326-26-000022:mdna:143 — prior-year comparative, previously reported
- 0000926326-26-000022:mdna:145 — amounts only (investing)
- 0000926326-26-000022:mdna:146 — prior-year comparative amounts
- 0000926326-26-000022:mdna:149 — prior-year comparative
- 0000926326-26-000022:mdna:152 — lead-in
- 0000926326-26-000022:mdna:153 — amounts only (contractual obligations table); read with across_documents_contractual_obligations_no_significant_change
- 0000926326-26-000022:mdna:158 — footnote cross-reference; wording

### Notes (input_notes.md)

- 0000926326-26-000022:notes:4 — periods rolled forward; 'comprehensive income (loss)' becomes 'comprehensive income' (wording)
- 0000926326-26-000022:notes:8 — date rolled forward; same critical estimates listed
- 0000926326-26-000022:notes:14 — insufficient: ASU 2024-03 still under evaluation; no adoption decision or effect stated
- 0000926326-26-000022:notes:15 — insufficient: ASU 2025-06 still under evaluation; no adoption decision or effect stated
- 0000926326-26-000022:notes:21 — amounts only (segment table)
- 0000926326-26-000022:notes:22 — footnote definition matching notes:19; covered by structure_and_disclosure_changes_segment_expenses_recast
- 0000926326-26-000022:notes:25 — wording only (a comma added, per note history)
- 0000926326-26-000022:notes:31 — amounts only (GPO and IFF fees)
- 0000926326-26-000022:notes:34 — amounts only (disaggregation table)
- 0000926326-26-000022:notes:36 — amounts only (geography table)
- 0000926326-26-000022:notes:41 — amounts only (contract balances)
- 0000926326-26-000022:notes:46 — amounts only (revenue recognized from opening deferred revenue)
- 0000926326-26-000022:notes:48 — amounts only (RPO at the new date); figure cited in results_against_expectations_arr_growth_opportunities_delayed
- 0000926326-26-000022:notes:50 — date rolled forward; still no 10% customer
- 0000926326-26-000022:notes:51 — insufficient: EPS method text, not in note history. The method as stated shows no change.
- 0000926326-26-000022:notes:52 — insufficient: continuation of notes:51
- 0000926326-26-000022:notes:54 — amounts only (EPS table)
- 0000926326-26-000022:notes:55 — amounts and date rolled forward. Insufficient to tell whether the concentration sentence is new.
- 0000926326-26-000022:notes:57 — insufficient: fair-value hierarchy text. The classifications as stated show no change.
- 0000926326-26-000022:notes:59 — amounts only (notes carrying and fair value)
- 0000926326-26-000022:notes:61 — amounts only (supplemental balance sheet)
- 0000926326-26-000022:notes:62 — amounts only (restricted cash)
- 0000926326-26-000022:notes:63 — amounts only (cloud computing costs)
- 0000926326-26-000022:notes:65 — amounts only (AOCI)
- 0000926326-26-000022:notes:67 — amounts only (PP&E)
- 0000926326-26-000022:notes:68 — amounts only (depreciation)
- 0000926326-26-000022:notes:70 — amounts only (PP&E by geography)
- 0000926326-26-000022:notes:72 — amounts only (external-use software)
- 0000926326-26-000022:notes:74 — amounts only (software amortization)
- 0000926326-26-000022:notes:76 — amounts only (software amortization schedule)
- 0000926326-26-000022:notes:79 — amounts only (goodwill; FX only)
- 0000926326-26-000022:notes:82 — amounts only (intangibles)
- 0000926326-26-000022:notes:85 — amounts only (intangible amortization)
- 0000926326-26-000022:notes:87 — amounts only (amortization schedule)
- 0000926326-26-000022:notes:88 — credit agreement terms restated; not marked changed in note history
- 0000926326-26-000022:notes:89 — interest-rate terms restated, unchanged
- 0000926326-26-000022:notes:90 — covenant terms restated, unchanged
- 0000926326-26-000022:notes:91 — guarantee and security terms restated, unchanged
- 0000926326-26-000022:notes:92 — date rolled forward (note history); availability, nil balance and compliance as before
- 0000926326-26-000022:notes:93 — 2025 Notes background, unchanged
- 0000926326-26-000022:notes:94 — 2025 Notes maturity, previously reported
- 0000926326-26-000022:notes:95 — heading
- 0000926326-26-000022:notes:96 — 2029 Notes terms, unchanged
- 0000926326-26-000022:notes:97 — re-segmented (note history); terms unchanged
- 0000926326-26-000022:notes:98 — re-segmented tail of notes:97
- 0000926326-26-000022:notes:100 — settlement terms, unchanged
- 0000926326-26-000022:notes:101 — re-segmented (note history); terms unchanged
- 0000926326-26-000022:notes:102 — date rolled forward
- 0000926326-26-000022:notes:103 — redemption terms, unchanged
- 0000926326-26-000022:notes:104 — date rolled forward; remaining life restated
- 0000926326-26-000022:notes:105 — date rolled forward
- 0000926326-26-000022:notes:106 — table lead-in
- 0000926326-26-000022:notes:107 — amounts only
- 0000926326-26-000022:notes:108 — table lead-in
- 0000926326-26-000022:notes:109 — amounts only (now three- and six-month columns)
- 0000926326-26-000022:notes:110 — heading
- 0000926326-26-000022:notes:111 — hedge and warrant background, unchanged
- 0000926326-26-000022:notes:112 — re-segmented, identical text (note history)
- 0000926326-26-000022:notes:113 — re-segmented; trailing sentences moved to notes:114 and notes:115
- 0000926326-26-000022:notes:114 — tense change 'terminate' to 'expired'; substance itemized from notes:115
- 0000926326-26-000022:notes:119 — amounts only (sales-type lease revenue)
- 0000926326-26-000022:notes:121 — amounts only (net investment in leases)
- 0000926326-26-000022:notes:125 — amounts only (lease receipts schedule)
- 0000926326-26-000022:notes:126 — date rolled forward
- 0000926326-26-000022:notes:128 — amounts only (lessee schedule)
- 0000926326-26-000022:notes:129 — amounts only
- 0000926326-26-000022:notes:130 — amounts only
- 0000926326-26-000022:notes:132 — amounts only
- 0000926326-26-000022:notes:134 — amounts only
- 0000926326-26-000022:notes:135 — heading
- 0000926326-26-000022:notes:137 — heading
- 0000926326-26-000022:notes:138 — recurring statement; not marked changed in note history
- 0000926326-26-000022:notes:139 — re-segmented, identical text (note history)
- 0000926326-26-000022:notes:140 — recurring statement that no material proceedings exist; not marked changed in note history
- 0000926326-26-000022:notes:141 — amounts only (tax expense, discrete items)
- 0000926326-26-000022:notes:142 — period rolled forward; same rate-reconciling items
- 0000926326-26-000022:notes:143 — period rolled forward; OBBBA still not significant
- 0000926326-26-000022:notes:144 — period rolled forward; Pillar Two still no impact
- 0000926326-26-000022:notes:145 — amounts only (unrecognized tax benefits, interest and penalties); cited in the IRS item
- 0000926326-26-000022:notes:149 — amounts only
- 0000926326-26-000022:notes:150 — amounts only
- 0000926326-26-000022:notes:153 — amounts only
- 0000926326-26-000022:notes:154 — amounts only
- 0000926326-26-000022:notes:157 — amounts only
- 0000926326-26-000022:notes:160 — amounts only
- 0000926326-26-000022:notes:161 — amounts only
- 0000926326-26-000022:notes:164 — amounts only
- 0000926326-26-000022:notes:165 — amounts only
- 0000926326-26-000022:notes:167 — date rolled forward
- 0000926326-26-000022:notes:168 — amounts only
- 0000926326-26-000022:notes:170 — past tense, consistent with notes:171; covered by liquidity_and_capital_repurchase_programs_concluded

### Note change history

I used the note change history to locate changes, not as a second list. Each entry maps to a notes paragraph that is accounted for above:

- note_history:1 and :5 map to notes:139. The removed prior entries :2, :3, :6 and :7 are the two halves of the same text.
- note_history:4 maps to notes:136.
- note_history:8 maps to notes:4.
- note_history:9 maps to notes:8.
- note_history:10 and :22 map to notes:109. The removed prior entries :11 and :29 are the old three-month table.
- note_history:12 and :21 map to notes:107.
- note_history:13 maps to notes:92. The removed prior entry :27 is its old tail.
- note_history:14 and :15 map to notes:97 and notes:98.
- note_history:16 maps to notes:99.
- note_history:17 maps to notes:101. The removed prior entry :28 is its old tail.
- note_history:18 maps to notes:102.
- note_history:19 maps to notes:104.
- note_history:20 maps to notes:105.
- note_history:23 maps to notes:112. The removed prior entries :30 and :31 are its old halves.
- note_history:24 maps to notes:113.
- note_history:25 maps to notes:114.
- note_history:26 maps to notes:115.
- note_history:32 maps to notes:59.
- note_history:33 and :37 map to notes:34.
- note_history:34 and :35 map to notes:25.
- note_history:36 maps to notes:31.
- note_history:38 maps to notes:36.
- note_history:39 maps to notes:41.
- note_history:40 maps to notes:46.
- note_history:41 maps to notes:47.
- note_history:42 maps to notes:48.
- note_history:43 maps to notes:50.
