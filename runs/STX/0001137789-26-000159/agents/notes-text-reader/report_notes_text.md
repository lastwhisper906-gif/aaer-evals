# report_notes_text: STX 10-K 0001137789-26-000159 (fiscal year ended July 3, 2026)

## Input check

- Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md (lines 1–1176), input_notes_history.md, input_prior_predictions.md.
- No forbidden content is present. There is no trend table, no price series, no abnormal returns, no short interest, no other company's files, no prior-run probability and no outcome window. The 8-K body contains the company's own condensed statements, which are part of the filed 8-K.
- These were not in my directory: the Item 1A diff, the Exhibit 21 diff and any Exhibit 10. No items come from them.
- Prior predictions: none on record, so there is nothing to carry forward.
- Comparator: the notes carry no `[same as prior period ...]` markers, so every paragraph was read as text. The prior 10-K text is not in my input. Where I say something is new, I compare against the Q2 and Q3 10-Q text in the note change history, or against the fiscal 2025 prose that sits next to it in the same document. Where neither lets me tell, the paragraph is marked `insufficient`.
- No arithmetic was done. Every amount below is quoted or restated as the filing states it.

Counts: 49 items; 10 `insufficient`.

## Items

```json
[
  {
    "id": "results_against_expectations_fourth_quarter_exceeded_own_expectations",
    "what_changed": "The earnings release says fourth-quarter revenue and non-GAAP EPS exceeded the company's own expectations. It calls fiscal 2026 profitability and free cash flow records. The CEO says he sees the momentum continuing in 2027.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "exceeded our expectations for revenue and non-GAAP EPS",
    "paragraph_id": "0001137789-26-000153:8k_2_02:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ceo_cites_strengthening_exabyte_demand",
    "what_changed": "The CEO says AI is accelerating data generation. He says the company is positioned for strengthening exabyte demand through the Mozaic platform and the HAMR technology roadmap.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Seagate is well positioned to address strengthening exabyte demand through our Mozaic platform and differentiated HAMR technology roadmap",
    "paragraph_id": "0001137789-26-000153:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_first_quarter_guidance_issued",
    "what_changed": "The release gives new guidance for fiscal Q1 2027: revenue of $4.1 billion plus or minus $100 million, and non-GAAP diluted EPS of $7.30 plus or minus $0.20 (8k_2_02:38). Share-based compensation of $0.26 per share is excluded. The release pairs the guidance with the CEO's statement that momentum continues. Setting the guidance against reported results is left to the numbers reader.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Revenue of $4.1 billion, plus or minus $100 million",
    "paragraph_id": "0001137789-26-000153:8k_2_02:37",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_middle_east_conflict_named_in_guidance",
    "what_changed": "The guidance assumptions name the current conflict in the Middle East next to global tariff policies. They say the expected impact is minimal as of the release date. The prior release is not in my input, so I cannot confirm that the Middle East reference is new.",
    "account": "Revenue",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Minimal expected impact from global tariff policies and/or the current conflict in the Middle East as of the date of this release.",
    "paragraph_id": "0001137789-26-000153:8k_2_02:41",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_fifty_three_week_fiscal_year",
    "what_changed": "Fiscal 2026 is now reported as a 53-week year against a 52-week fiscal 2025. The Q3 10-Q text (note history 0001137789-26-000088:note_history:6) says that in 53-week years the first quarter has 14 weeks, so the extra week sits in fiscal Q1 2026. The MD&A revenue explanation (mdna:28) does not attribute any part of the year-over-year change to the extra week. The fiscal Q1 2027 comparison will be made against a 14-week quarter.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Accordingly, fiscal year 2026 comprised of 53 weeks and ended on July 3, 2026.",
    "paragraph_id": "0001137789-26-000159:mdna:3",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_exchangeable_notes_retired_for_cash_and_shares",
    "what_changed": "A new overview sentence says debt was reduced by $1.4 billion through exchanges of the 2028 Notes for $1.3 billion of cash and about 12.6 million ordinary shares, and through repurchases of Senior Notes. The 8-K item-code list shows six Item 3.02 (unregistered equity) filings between 2025-11-05 and 2026-05-28. That is consistent with shares being issued in these exchanges. The earnings release (8k_2_02:31) states the same debt reduction.",
    "account": "Long-term debt",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "We reduced our outstanding debt by $1.4 billion through exchanges of our 2028 Notes for total consideration of $1.3 billion cash and approximately 12.6 million of our ordinary shares as well as repurchases of Senior Notes.",
    "paragraph_id": "0001137789-26-000159:mdna:13",
    "explanation": false
  },
  {
    "id": "results_against_expectations_data_center_demand_strengthened",
    "what_changed": "MD&A now says demand strengthened in fiscal 2026. It says growth was led by data center nearline demand from global cloud customers and by increasing enterprise edge sales. It cites AI-related applications as supporting growth in storage demand.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "During fiscal year 2026, demand for our data storage solutions strengthened.",
    "paragraph_id": "0001137789-26-000159:mdna:15",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_geopolitics_and_trade_policy",
    "what_changed": "MD&A says the macro environment remains dynamic, with heightened geopolitical uncertainty and evolving trade policies that may affect results. The same paragraph claims that the pricing strategy, supply discipline and long-term customer engagements give greater visibility into future demand.",
    "account": "Revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "At the same time, the macroeconomic environment remains dynamic, marked by heightened geopolitical uncertainty and evolving trade policies.",
    "paragraph_id": "0001137789-26-000159:mdna:16",
    "explanation": false
  },
  {
    "id": "earnings_quality_revenue_growth_attributed_to_pricing_actions",
    "what_changed": "Revenue growth is attributed to more nearline exabytes shipped and to favorable pricing actions undertaken by the company. The explanation does not mention the 53rd week.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to an increase in nearline exabytes shipped reflecting higher demand for nearline products and favorable pricing actions undertaken by the Company",
    "paragraph_id": "0001137789-26-000159:mdna:28",
    "explanation": false
  },
  {
    "id": "earnings_quality_gross_margin_attributed_to_pricing_and_mix",
    "what_changed": "The prose states an 11-percentage-point gross margin improvement. It attributes it to pricing actions and a mix shift to higher-capacity products. It does not name as factors the operating grants credited against Cost of revenue (notes:49) or the extra week.",
    "account": "Gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by pricing actions undertaken by the Company and product mix shift to higher capacity products",
    "paragraph_id": "0001137789-26-000159:mdna:32",
    "explanation": false
  },
  {
    "id": "earnings_quality_product_development_outside_services_increase",
    "what_changed": "New explanation of product development expense. It names a $22 million increase in outside services costs, $7 million in compensation and $7 million in facilities, partly offset by an $8 million decrease in material expenses.",
    "account": "Product development",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to a $22 million increase in outside services costs",
    "paragraph_id": "0001137789-26-000159:mdna:35",
    "explanation": false
  },
  {
    "id": "earnings_quality_marketing_administrative_compensation_and_technology",
    "what_changed": "New explanation of marketing and administrative expense. It names an $11 million increase in compensation and benefits and a $5 million increase in IT expenses.",
    "account": "Marketing and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to an $11 million increase in compensation and other employee benefits and a $5 million increase in information technology expenses",
    "paragraph_id": "0001137789-26-000159:mdna:36",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_charges_recur_but_excluded_from_non_gaap",
    "what_changed": "MD&A reports $27 million of fiscal 2026 restructuring charges, mainly employee termination benefits. The same paragraph reports $25 million of fiscal 2025 restructuring charges in operating expenses. The earnings release (8k_2_02:101) excludes restructuring from non-GAAP results because it does not reflect normal or ongoing performance.",
    "account": "Restructuring and other, net",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In fiscal year 2026, we recorded $27 million of restructuring charges, primarily related to employee related termination benefits.",
    "paragraph_id": "0001137789-26-000159:mdna:38",
    "explanation": false
  },
  {
    "id": "earnings_quality_pillar_two_minimum_tax_now_in_effect",
    "what_changed": "New sentence: from fiscal 2026, major jurisdictions where the company operates have implemented the Pillar Two global minimum tax. The effective tax rate is stated as 13.73% for fiscal 2026 and 2.91% for fiscal 2025. The new rate reconciliation (notes:144) has a 'Qualified Domestic Minimum Top-up Tax' line of $422 million. The other non-current liabilities table (notes:86) has a 'Non-current income tax payable' line of $436 million. The cash cost of the top-up tax should come through later periods.",
    "account": "Provision for income taxes",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Starting from fiscal year 2026, major jurisdictions that we operate in have implemented Pillar Two global minimum tax.",
    "paragraph_id": "0001137789-26-000159:mdna:45",
    "explanation": false
  },
  {
    "id": "earnings_quality_discrete_tax_benefits_obbba_and_share_compensation",
    "what_changed": "The fiscal 2026 provision now includes two named benefits inside the reported rate. One is a discrete benefit from releasing certain valuation allowances in connection with the OBBBA (July 2025). The other is net excess tax benefits from share-based compensation.",
    "account": "Provision for income taxes",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The fiscal year 2026 provision for income taxes also includes a discrete tax benefit related to the release of certain valuation allowances in connection with the OBBBA in July 2025 and net excess tax benefits related to share-based compensation expense.",
    "paragraph_id": "0001137789-26-000159:mdna:46",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_receivables_increase_explained_by_revenue",
    "what_changed": "Management explains the $575 million increase in receivables as due to increased revenue. The fiscal 2025 explanation (mdna:62) cited higher revenue and lower factoring. The fiscal 2026 explanation cites revenue only. Meanwhile the notes say no receivables were sold in fiscal 2026 (notes:70), and they name three customers at 18%, 16% and 10% of receivables (notes:54).",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase of $575 million in accounts receivable, primarily due to increased revenue",
    "paragraph_id": "0001137789-26-000159:mdna:57",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_inventory_increase_explained_by_work_in_process",
    "what_changed": "Management explains the $131 million increase in inventory as primarily work-in-process. The fiscal 2025 explanation (mdna:64) cited purchased materials and finished goods.",
    "account": "Inventories, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase of $131 million in inventory, primarily due to an increase in work-in-process inventory",
    "paragraph_id": "0001137789-26-000159:mdna:58",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_accrued_liabilities_increase_explained_by_taxes_and_settlements",
    "what_changed": "Management explains the $528 million increase in accrued expenses, income taxes and warranty as primarily accrued income taxes and legal settlements. Warranty appears in the line caption but is not named as a driver.",
    "account": "Accrued expenses, income taxes and warranty",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase of $528 million in accrued expenses, income taxes and warranty, primarily due to an increase in accrued income taxes and legal settlements",
    "paragraph_id": "0001137789-26-000159:mdna:59",
    "explanation": true
  },
  {
    "id": "across_documents_payables_explanation_omits_supplier_finance_program",
    "what_changed": "MD&A attributes the $66 million increase in accounts payable to capital expenditures. The supplier finance table (notes:91) states confirmed obligations outstanding of $400 million at the end of fiscal 2026 and $20 million at the beginning, and notes:89 says these are recorded within Accounts payable. The MD&A explanation does not mention the program.",
    "account": "Accounts payable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase of $66 million in accounts payable, primarily due to an increase in capital expenditures",
    "paragraph_id": "0001137789-26-000159:mdna:60",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capex_to_rise_for_hamr_ramp",
    "what_changed": "New forward-looking statement: fiscal 2027 capital expenditures are expected to be higher than fiscal 2026 to support the HAMR volume ramp, while staying within the stated target range as a percentage of revenue. Unconditional equipment commitments are stated at $465 million, of which about $375 million is due within one year.",
    "account": "Acquisition of property, equipment and leasehold improvements",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we expect capital expenditures to be higher than fiscal year 2026 and still within our target range",
    "paragraph_id": "0001137789-26-000159:mdna:96",
    "explanation": false
  },
  {
    "id": "across_documents_debt_maturity_described_beyond_one_year_despite_redemptions",
    "what_changed": "MD&A says the $3.6 billion of principal will mature in more than one year. Yet the same paragraph reports two redemptions. One is a Notice of Full Provisional Redemption for the remaining $185 million of 2028 Notes, with redemption on September 8, 2026. The other is a July 15, 2026 redemption of $1 billion of Senior Notes. The debt note classifies $185 million as current (notes:100), and the principal schedule (notes:132) shows no amount for fiscal 2027.",
    "account": "Long-term debt",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "the future principal payment obligation on our long-term debt was $3.6 billion, which will mature in more than one year",
    "paragraph_id": "0001137789-26-000159:mdna:101",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_legal_settlement_accruals_and_timing",
    "what_changed": "The cash-requirements section now states $225 million accrued for legal settlements at year end. Of that, $150 million is expected to be paid within one year and $75 million thereafter. It refers to Note 12, which carries the BIS settlement and the securities class action settlement.",
    "account": "Accrued expenses; Other non-current liabilities",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "As of July 3, 2026, we accrued a total of $225 million relating to legal settlements, of which $150 million is expected to be paid within one year and $75 million thereafter.",
    "paragraph_id": "0001137789-26-000159:mdna:103",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_business_description_recast_by_end_market",
    "what_changed": "The Q3 10-Q (note history 0001137789-26-000088:note_history:4) described a 'leading provider of data storage technology and infrastructure solutions' whose principal business is HDDs and which offers SSDs. The 10-K now describes a provider of mass-capacity data storage serving two principal end markets, Data Center and Edge IoT. It cites AI-enabled computing and no longer mentions SSDs.",
    "account": "Revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "storage systems and related solutions serving two principal end markets: Data center and Edge / Internet of Things",
    "paragraph_id": "0001137789-26-000159:notes:14",
    "explanation": false
  },
  {
    "id": "earnings_quality_government_grants_credited_against_costs",
    "what_changed": "The note states fiscal 2026 operating grants of about $112 million, $37 million and $14 million, credited against Cost of revenue, Product development and Marketing and administrative. Capital grants reduced gross PP&E by $29 million. Grant receivables of $113 million sit in Other current assets and $13 million in Other assets, net. Fiscal 2025 grant receivables are stated only within Other current assets. Grants are conditional and can be reduced, recaptured or terminated (notes:48).",
    "account": "Cost of revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In fiscal year 2026, approximately $112 million, $37 million and $14 million of operating grants were recognized as reductions to Cost of revenue, Product development and Marketing and administrative, respectively",
    "paragraph_id": "0001137789-26-000159:notes:49",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_receivables_concentrated_in_three_customers",
    "what_changed": "The concentration note now names three customers at 18%, 16% and 10% of accounts receivable at July 3, 2026. For June 27, 2025 it names one customer at 18%. The note says the company does not generally require collateral.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "three customers accounted for 18%, 16% and 10%, respectively",
    "paragraph_id": "0001137789-26-000159:notes:54",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_adopted",
    "what_changed": "ASU 2023-09 is now adopted for fiscal 2026 annual reporting on a prospective basis. The rate reconciliation uses the new format for fiscal 2026 only (notes:144), with fiscal 2025 and 2024 in the old format (notes:146). Cash taxes paid are newly disclosed at $40 million (notes:148).",
    "account": "Provision for income taxes",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company adopted the disclosure requirement for its annual reporting in fiscal year 2026 on a prospective basis.",
    "paragraph_id": "0001137789-26-000159:notes:60",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_induced_conversion_standard_adopted",
    "what_changed": "The 10-K says ASU 2024-04 was adopted in fiscal 2026 on a prospective basis and applied to the 2028 Notes exchanges. The note describes the standard as effective for fiscal years beginning after December 15, 2025, with early adoption permitted. This choice is what routes the exchange cost through Net loss from debt transactions as induced conversion expense (notes:116).",
    "account": "Net loss from debt transactions",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The Company adopted the guidance on a prospective basis in fiscal year 2026 and applied the amendments in the ASU to the exchanges of the 2028 Notes.",
    "paragraph_id": "0001137789-26-000159:notes:61",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_government_grants_standard_issued",
    "what_changed": "New paragraph on ASU 2025-10 (government grants), issued December 2025. The company must adopt it for fiscal 2029, early adoption is permitted, and no material impact is expected.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In December 2025, the FASB issued ASU 2025-10 (ASC Topic 832), Government Grants - Accounting for Government Grants Received by Business Entities.",
    "paragraph_id": "0001137789-26-000159:notes:64",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_no_receivables_factored",
    "what_changed": "New sentence: no accounts receivable were sold to third parties in fiscal 2026. In fiscal 2025, receivables were sold without recourse for $692 million. By the prose, fiscal 2026 receivables and operating cash flow carry no factoring.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During fiscal year 2026, the Company did not sell any accounts receivable to a third party.",
    "paragraph_id": "0001137789-26-000159:notes:70",
    "explanation": false
  },
  {
    "id": "across_documents_intangible_amortization_classification",
    "what_changed": "The note now reports $8 million of intangible amortization in fiscal 2026, after immaterial or no amortization in fiscal 2025 and 2024. It says amortization is charged to Operating expenses. The earnings release reconciliation (8k_2_02:71) adds back 'Amortization of acquired intangible assets' to reach Non-GAAP Gross Profit and does not list it among the operating-expense adjustments. That places the charge in Cost of revenue, so the two documents place it differently.",
    "account": "Cost of revenue; Operating expenses",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Amortization is charged to Operating expenses in the Consolidated Statements of Operations and Comprehensive Income.",
    "paragraph_id": "0001137789-26-000159:notes:98",
    "explanation": false
  },
  {
    "id": "earnings_quality_induced_conversion_expense_on_negotiated_exchanges",
    "what_changed": "The note now lists a third privately negotiated exchange, on May 27, 2026: $186 million of principal for $186 million of cash and about 2 million shares. This sits alongside the November 2025 and February 2026 exchanges. The note states a fiscal 2026 non-cash induced conversion expense of $131 million in Net loss from debt transactions, with the offset in Additional Paid-in Capital. The capped call notional stays at $1.5 billion.",
    "account": "Net loss from debt transactions",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "recognized a non-cash induced conversion expense of $131 million within Net loss from debt transactions",
    "paragraph_id": "0001137789-26-000159:notes:116",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_holder_exchanges_settling_in_august",
    "what_changed": "New paragraph. In May 2026, holders exchanged $28 million of 2028 Notes under the indenture. That was settled in cash for principal plus about 0.3 million shares and accounted for as conversions with no gain or loss. In June 2026, holders of about $35 million exercised exchange rights. Settlement is expected in August 2026, with cash for principal and shares for the excess.",
    "account": "Current portion of long-term debt",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The exchanges are expected to be settled in August 2026 following completion of the applicable observation period under the indenture.",
    "paragraph_id": "0001137789-26-000159:notes:117",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_full_provisional_redemption_of_exchangeable_notes",
    "what_changed": "New: on June 11, 2026 the company issued a Notice of Full Provisional Redemption. Notes not submitted for exchange will be redeemed for cash at principal plus accrued interest on September 8, 2026. Holders may exchange until the second scheduled trading day before that date. The 8-K list shows a 7.01/8.01 filing on 2026-06-12, consistent in timing with the notice; its body is not in my input.",
    "account": "Current portion of long-term debt",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "On June 11, 2026, the Company issued a Notice of Full Provisional Redemption to holders of the 2028 Notes.",
    "paragraph_id": "0001137789-26-000159:notes:119",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_exchange_excess_settled_in_shares",
    "what_changed": "The Q3 10-Q (note history 0001137789-26-000088:note_history:13) said the excess over principal could be settled in cash, shares or a combination, at Seagate HDD's election. The 10-K says that for Redemption Called Notes the excess will be delivered in ordinary shares. The exchange rate is now 12.1368 shares per $1,000, an exchange price of $82.39.",
    "account": "Ordinary shares outstanding; diluted share count",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Upon exchange of any Redemption Called Notes, Seagate HDD will pay cash up to the aggregate principal amount of 2028 Notes to be exchanged and will cause to be delivered ordinary shares of the Company in respect of any remainder of the exchange obligation in excess of such principal amount.",
    "paragraph_id": "0001137789-26-000159:notes:120",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_senior_notes_repurchased_at_discount",
    "what_changed": "New fiscal-year paragraph. The company repurchased for cash, at a discount, $89 million of New June 2029, $2 million of New July 2029, $36 million of New January 2031 and $1 million of Old January 2031 notes, with an immaterial net gain. The Q3 10-Q (note history 0001137789-26-000088:note_history:17) described the March-quarter repurchase of $40 million of New June 2029 Notes as producing an immaterial loss.",
    "account": "Long-term debt",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The Company recorded an immaterial net gain on these repurchases during fiscal year 2026",
    "paragraph_id": "0001137789-26-000159:notes:123",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_july_senior_notes_redemption_loss",
    "what_changed": "New subsequent event. On July 15, 2026 the company redeemed the entire outstanding principal of the Old and New December 2029 Notes (8.25%) and the Old and New 8.50% July 2031 Notes, totaling $1 billion. It expects a net loss of about $45 million in fiscal Q1 2027. These notes were presented as long-term debt at July 3, 2026 (notes:100). The earnings release excludes net loss from debt transactions from its non-GAAP guidance.",
    "account": "Net loss from debt transactions",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The Company expects to record a net loss of approximately $45 million in the first quarter of fiscal year 2027.",
    "paragraph_id": "0001137789-26-000159:notes:125",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_leverage_covenant_without_springing_condition",
    "what_changed": "The covenant paragraph no longer carries a sentence that was in the Q2 10-Q (note history 0001137789-26-000026:note_history:19). That sentence said that until January 2, 2026 the net leverage covenant applied only when revolving loans, swing line loans or letters of credit were outstanding. The covenant now applies every quarter, stepping down to 4.25 to 1.00 for quarters ending after July 2, 2027. MD&A (mdna:88) states compliance at July 3, 2026, and notes:127 says no revolver borrowings were outstanding.",
    "account": "Revolving Credit Facility",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Credit Agreement also contains a financial covenant that requires the Company to maintain a total net leverage ratio of less than or equal to 6.75 to 1.00",
    "paragraph_id": "0001137789-26-000159:notes:129",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_valuation_allowance_release_obbba_and_reorganization",
    "what_changed": "New explanation. The valuation allowance decreased by $86 million in fiscal 2026, mainly from releases tied to the enactment of the One Big Beautiful Bill Act. Changes in tax attributes from an internal reorganization were fully offset by valuation allowance. The rate reconciliation (notes:144) shows an 'Internal Re-organization' line. The internal reorganization is not otherwise described in my input.",
    "account": "Deferred tax asset valuation allowance",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The deferred tax asset valuation allowance decreased by $86 million in fiscal year 2026, primarily due to releases in valuation allowance associated with the enactment of the One Big Beautiful Bill Act and changes in tax attributes associated with an internal reorganization that were fully offset by a valuation allowance.",
    "paragraph_id": "0001137789-26-000159:notes:140",
    "explanation": true
  },
  {
    "id": "earnings_quality_tax_incentive_benefit_net_of_top_up_tax",
    "what_changed": "The Singapore and Thailand tax-incentive benefit is now stated after offsetting the qualified domestic minimum top-up tax. The note gives about $197 million ($0.86 per diluted share) for fiscal 2026, $285 million ($1.32) for fiscal 2025 and $40 million ($0.19) for fiscal 2024. The incentives expire in whole or in part at dates into fiscal 2034.",
    "account": "Provision for income taxes",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "after factoring in offsetting qualified domestic minimum top-up tax",
    "paragraph_id": "0001137789-26-000159:notes:150",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_unrecognized_tax_benefits_current_year_position",
    "what_changed": "The note states unrecognized tax benefits of about $155 million at July 3, 2026 and $107 million at June 27, 2025. The rollforward (notes:154) shows a gross increase of $48 million for current-year tax positions and no prior-year decreases. The rate reconciliation lists 'Changes in unrecognized tax benefits'. MD&A (mdna:105) states a $43 million liability for unrecognized tax benefits, none expected to settle within one year.",
    "account": "Unrecognized tax benefits",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of July 3, 2026 and June 27, 2025, the Company had approximately $155 million and $107 million, respectively, of unrecognized tax benefits excluding interest and penalties.",
    "paragraph_id": "0001137789-26-000159:notes:152",
    "explanation": false
  },
  {
    "id": "earnings_quality_strategic_investment_sale_gain",
    "what_changed": "New: a $14 million net gain on measurement-alternative investments in fiscal 2026, mainly from the sale of an investment. Fiscal 2025 had a $39 million write-down. The carrying value of these investments is stated as $19 million at year end and $26 million a year earlier. The earnings release excludes a $14 million strategic investment gain from Q4 non-GAAP results.",
    "account": "Other, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the Company recorded a net gain of $14 million for fiscal year 2026, primarily due to the sale of an investment",
    "paragraph_id": "0001137789-26-000159:notes:183",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_under_program",
    "what_changed": "New: the company repurchased 0.5 million shares for $176 million under its program in fiscal 2026. The fiscal 2025 financing discussion (mdna:77 to mdna:83) lists no share repurchases. $4.8 billion of authorization remains. MD&A (mdna:109) states the fiscal 2026 count in different terms: approximately 1 million shares, including approximately 0.4 million withheld for taxes. The share repurchase program is listed among liquidity uses (mdna:92).",
    "account": "Repurchases of ordinary shares",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "For the fiscal year ended July 3, 2026, the Company repurchased 0.5 million shares for $176 million under its share repurchase program.",
    "paragraph_id": "0001137789-26-000159:notes:191",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_amended_equity_incentive_plan",
    "what_changed": "New: shareholders approved the Amended EIP on October 25, 2025, replacing the 2022 EIP. The share reserve is 17.9 million shares, with full-value awards capped at 16.1 million. 12.2 million shares were available for full-value awards at July 3, 2026. The 8-K list shows a 5.07 (shareholder vote) filing dated 2025-10-28. Two naming points: this paragraph refers to awards under a '2012 Equity Incentive Plan', and the EPB paragraph (notes:194) refers to an 'Amended 2022 EIP'. Both differ from 'Amended EIP'.",
    "account": "Share-based compensation",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "shareholders of the Company approved the Amended EIP that replaced Seagate Technology Holdings plc 2022 Equity Incentive Plan",
    "paragraph_id": "0001137789-26-000159:notes:193",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_lambeth_patent_retrial",
    "what_changed": "New development: on September 17, 2025 the Federal Circuit vacated the district court's 2022 judgment for Seagate and remanded for a new trial on infringement and enablement. The company says the claims are without merit. No accrual or loss range is disclosed.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "remanded for a new trial on infringement and enablement",
    "paragraph_id": "0001137789-26-000159:notes:234",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_nhk_certiorari_petition",
    "what_changed": "A new sentence since the Q3 10-Q says the Ninth Circuit denied NHK's petition for rehearing and NHK has petitioned the U.S. Supreme Court for certiorari. This is Seagate's own antitrust claim against a supplier, so it is a potential gain and nothing is recorded.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "has since petitioned the U.S. Supreme Court for certiorari",
    "paragraph_id": "0001137789-26-000159:notes:235",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_securities_settlement_preliminary_approval",
    "what_changed": "The Q3 10-Q (note history 0001137789-26-000088:note_history:2) said the $175 million settlement in principle, with about $70 million from insurers and a $105 million charge, was subject to court approval and a definitive agreement. The 10-K says a stipulation of settlement has been executed. Preliminary approval was granted July 7, 2026, and a final approval hearing is set for November 17, 2026.",
    "account": "Accrued expenses (legal settlement)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "On July 7, 2026, the court granted preliminary approval of the settlement, and a final approval hearing will be held on November 17, 2026.",
    "paragraph_id": "0001137789-26-000159:notes:236",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_market_share_based_purchase_commitments",
    "what_changed": "The commitments note states unconditional long-term purchase obligations of about $547 million, mainly inventory components, scheduled for fiscal 2028 onward. It adds long-term market-share-based inventory purchase commitments with no amount given; MD&A (mdna:94) calls them non-cancellable. MD&A states total unconditional purchase obligations of about $2.1 billion, with $1.6 billion due within one year. My input does not show whether the market-share-based sentence is new compared with the prior 10-K.",
    "account": "Purchase obligations; Inventories",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In addition, the Company also had certain long-term market share based inventory purchase commitments as of July 3, 2026.",
    "paragraph_id": "0001137789-26-000159:notes:249",
    "explanation": false
  },
  {
    "id": "across_documents_divestiture_loss_in_non_gaap_reconciliation_only",
    "what_changed": "The divestiture note adds that $15 million of the $40 million indemnification holdback from the SoC sale was received in fiscal 2026, after $25 million in fiscal 2025. It mentions no fiscal 2026 gain or loss. The GAAP income statement shows no Net gain from business divestiture for fiscal 2026. Yet the release's non-GAAP reconciliations (8k_2_02:76 and 8k_2_02:83) add back a $3 million net loss from business divestiture in fiscal 2026, in the April 3, 2026 quarter. My input does not say where that loss sits in the GAAP statements.",
    "account": "Other, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "of which $25 million was received during fiscal year 2025 and $15 million was received during fiscal year 2026",
    "paragraph_id": "0001137789-26-000159:notes:265",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_cfo_trading_plan",
    "what_changed": "New in this period's disclosure: the CFO adopted a Rule 10b5-1 trading plan on April 30, 2026 covering 72,709 shares, running through December 31, 2026. A director's plan adopted March 3, 2026 was terminated on June 2, 2026 (notes:271).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Gianluca Romano | Executive Vice President and Chief Financial Officer",
    "paragraph_id": "0001137789-26-000159:notes:270",
    "explanation": false
  }
]
```

## Insufficient (10)

- 0001137789-26-000153:8k_2_02:40: insufficient. The guidance includes the dilutive impact of the 2028 Notes, but the prior release is not in my input, so I cannot tell whether this line is new.
- 0001137789-26-000153:8k_2_02:109: insufficient. It states a projected fiscal 2026 non-GAAP tax rate of 15.5%; the prior-year rate is not in my input.
- 0001137789-26-000159:mdna:92: insufficient. I cannot tell whether "share repurchase program" was newly added to the list of liquidity uses.
- 0001137789-26-000159:mdna:112: insufficient. The critical estimates are now listed as Revenue - Sales Program Accruals and Income Taxes, with warranty, inventory, goodwill and others named as non-critical. The prior-year list is not in my input, so I cannot tell whether warranty was dropped.
- 0001137789-26-000159:notes:12: insufficient. The CISO reports to the CIO, who reports to the CFO; the prior reporting line is not in my input.
- 0001137789-26-000159:notes:55: insufficient. Cash is held with "four major financial institutions"; the prior count is not in my input.
- 0001137789-26-000159:notes:58: insufficient. The Manufacturing Concentration paragraph may be new, but the prior-year concentrations text is not in my input.
- 8-K 0001137789-25-000191 (2025-08-26, Item 5.02): insufficient. It is an officer or director change filing whose body is not in my input.
- 8-K 0001137789-25-000287 (2025-10-28, Items 5.02 and 5.07): insufficient for the 5.02, whose body is not in my input. The 5.07 is consistent with the Amended EIP approval (see the notes:193 item).
- 8-K 0001137789-26-000093 (2026-05-06, Item 5.02): insufficient. It is an officer or director change filing whose body is not in my input.

## 8-K filings since the prior 10-K (item-code list; these lines carry no paragraph ids)

- 2025-10-28 0001137789-25-000283 (2.02), 2026-01-27 0001137789-26-000016 (2.02), 2026-04-28 0001137789-26-000084 (2.02): earlier quarterly releases; their bodies are not in my input.
- 2025-11-05 0001193125-25-265772, 2025-11-13 0001193125-25-279125, 2026-02-12 0001193125-26-047755, 2026-02-19 0001193125-26-059681, 2026-05-21 0001193125-26-233588, 2026-05-28 0001193125-26-243110 (3.02, 7.01, 8.01): consistent with the note exchanges; covered by the mdna:13 and notes:116 items.
- 2026-06-12 0001193125-26-268170 (7.01, 8.01): body not in my input; consistent in timing with the June 11, 2026 redemption notice (notes:119 item).
- 2026-07-28 0001137789-26-000153 (2.02, 7.01, 9.01): body read in full; items and the list below.
- Late-filing notifications: none, so no item.

## Note change history

- 0001137789-26-000026 and 0001137789-26-000088 note_history:1 to note_history:30 were used only as the comparator, cited inside the items. Per instructions they are not reported as a second list.

## Paragraphs not itemized

### 8-K item 2.02 (0001137789-26-000153)
- 0001137789-26-000153:8k_2_02:1 — exhibit header
- 0001137789-26-000153:8k_2_02:2 — document header
- 0001137789-26-000153:8k_2_02:3 — exhibit label
- 0001137789-26-000153:8k_2_02:4 — contact heading
- 0001137789-26-000153:8k_2_02:5 — contact details
- 0001137789-26-000153:8k_2_02:6 — contact details
- 0001137789-26-000153:8k_2_02:7 — contact heading
- 0001137789-26-000153:8k_2_02:8 — contact details
- 0001137789-26-000153:8k_2_02:9 — contact details
- 0001137789-26-000153:8k_2_02:10 — release title
- 0001137789-26-000153:8k_2_02:11 — heading
- 0001137789-26-000153:8k_2_02:12 — amounts only
- 0001137789-26-000153:8k_2_02:13 — amounts only
- 0001137789-26-000153:8k_2_02:14 — amounts only
- 0001137789-26-000153:8k_2_02:15 — amounts only
- 0001137789-26-000153:8k_2_02:16 — amounts only; debt reduction covered by the mdna:13 item
- 0001137789-26-000153:8k_2_02:17 — heading
- 0001137789-26-000153:8k_2_02:18 — amounts only
- 0001137789-26-000153:8k_2_02:19 — amounts only
- 0001137789-26-000153:8k_2_02:20 — amounts only
- 0001137789-26-000153:8k_2_02:21 — amounts only
- 0001137789-26-000153:8k_2_02:22 — amounts only; covered by the mdna:13 and notes:191 items
- 0001137789-26-000153:8k_2_02:23 — dateline; period-end date
- 0001137789-26-000153:8k_2_02:26 — heading
- 0001137789-26-000153:8k_2_02:27 — table, amounts only
- 0001137789-26-000153:8k_2_02:28 — heading
- 0001137789-26-000153:8k_2_02:29 — table, amounts only
- 0001137789-26-000153:8k_2_02:30 — cross-reference
- 0001137789-26-000153:8k_2_02:31 — amounts only; debt reduction covered by the mdna:13 item
- 0001137789-26-000153:8k_2_02:32 — cross-reference
- 0001137789-26-000153:8k_2_02:33 — heading
- 0001137789-26-000153:8k_2_02:34 — dividend per share same as the Q2 and Q3 declarations in the note history; dates rolled forward
- 0001137789-26-000153:8k_2_02:35 — heading
- 0001137789-26-000153:8k_2_02:36 — lead-in
- 0001137789-26-000153:8k_2_02:38 — EPS guidance amount; covered by the 8k_2_02:37 item
- 0001137789-26-000153:8k_2_02:39 — lead-in
- 0001137789-26-000153:8k_2_02:40 — insufficient (see above)
- 0001137789-26-000153:8k_2_02:42 — amounts only
- 0001137789-26-000153:8k_2_02:43 — boilerplate on the non-GAAP reconciliation
- 0001137789-26-000153:8k_2_02:44 — heading
- 0001137789-26-000153:8k_2_02:45 — webcast logistics
- 0001137789-26-000153:8k_2_02:46 — webcast logistics
- 0001137789-26-000153:8k_2_02:47 — heading
- 0001137789-26-000153:8k_2_02:48 — boilerplate company description
- 0001137789-26-000153:8k_2_02:49 — trademark notice
- 0001137789-26-000153:8k_2_02:50 — heading
- 0001137789-26-000153:8k_2_02:51 — boilerplate
- 0001137789-26-000153:8k_2_02:52 — heading
- 0001137789-26-000153:8k_2_02:53 — heading
- 0001137789-26-000153:8k_2_02:54 — heading
- 0001137789-26-000153:8k_2_02:55 — balance sheet, amounts only
- 0001137789-26-000153:8k_2_02:56 — heading
- 0001137789-26-000153:8k_2_02:57 — heading
- 0001137789-26-000153:8k_2_02:58 — heading
- 0001137789-26-000153:8k_2_02:59 — income statement, amounts only
- 0001137789-26-000153:8k_2_02:60 — heading
- 0001137789-26-000153:8k_2_02:61 — heading
- 0001137789-26-000153:8k_2_02:62 — heading
- 0001137789-26-000153:8k_2_02:63 — cash flow statement, amounts only
- 0001137789-26-000153:8k_2_02:64 — heading
- 0001137789-26-000153:8k_2_02:65 — non-GAAP boilerplate
- 0001137789-26-000153:8k_2_02:66 — non-GAAP boilerplate
- 0001137789-26-000153:8k_2_02:67 — heading
- 0001137789-26-000153:8k_2_02:68 — heading
- 0001137789-26-000153:8k_2_02:69 — heading
- 0001137789-26-000153:8k_2_02:70 — heading
- 0001137789-26-000153:8k_2_02:71 — reconciliation, amounts only; amortization placement used in the notes:98 item
- 0001137789-26-000153:8k_2_02:72 — heading
- 0001137789-26-000153:8k_2_02:73 — heading
- 0001137789-26-000153:8k_2_02:74 — heading
- 0001137789-26-000153:8k_2_02:75 — heading
- 0001137789-26-000153:8k_2_02:76 — reconciliation, amounts only; divestiture add-back used in the notes:265 item
- 0001137789-26-000153:8k_2_02:77 — reconciliation, amounts only
- 0001137789-26-000153:8k_2_02:78 — heading
- 0001137789-26-000153:8k_2_02:79 — heading
- 0001137789-26-000153:8k_2_02:80 — heading
- 0001137789-26-000153:8k_2_02:81 — heading
- 0001137789-26-000153:8k_2_02:82 — free cash flow reconciliation, amounts only
- 0001137789-26-000153:8k_2_02:83 — EBITDA reconciliation, amounts only; used in the notes:265 item
- 0001137789-26-000153:8k_2_02:84 — rule line
- 0001137789-26-000153:8k_2_02:85 — footnote on fiscal 2025 restructuring; prior-period amounts
- 0001137789-26-000153:8k_2_02:86 — if-converted share amounts only
- 0001137789-26-000153:8k_2_02:87 — lead-in
- 0001137789-26-000153:8k_2_02:88 — heading
- 0001137789-26-000153:8k_2_02:89 — definition boilerplate
- 0001137789-26-000153:8k_2_02:90 — heading
- 0001137789-26-000153:8k_2_02:91 — definition boilerplate
- 0001137789-26-000153:8k_2_02:92 — heading
- 0001137789-26-000153:8k_2_02:93 — definition boilerplate
- 0001137789-26-000153:8k_2_02:94 — heading
- 0001137789-26-000153:8k_2_02:95 — definition boilerplate
- 0001137789-26-000153:8k_2_02:96 — heading
- 0001137789-26-000153:8k_2_02:97 — definition boilerplate
- 0001137789-26-000153:8k_2_02:98 — heading
- 0001137789-26-000153:8k_2_02:99 — definition boilerplate
- 0001137789-26-000153:8k_2_02:100 — heading
- 0001137789-26-000153:8k_2_02:101 — definition boilerplate; used in the mdna:38 item
- 0001137789-26-000153:8k_2_02:102 — heading
- 0001137789-26-000153:8k_2_02:103 — definition boilerplate
- 0001137789-26-000153:8k_2_02:104 — heading
- 0001137789-26-000153:8k_2_02:105 — definition boilerplate
- 0001137789-26-000153:8k_2_02:106 — heading
- 0001137789-26-000153:8k_2_02:107 — definition boilerplate
- 0001137789-26-000153:8k_2_02:108 — heading
- 0001137789-26-000153:8k_2_02:109 — insufficient (see above)
- 0001137789-26-000153:8k_2_02:110 — heading
- 0001137789-26-000153:8k_2_02:111 — definition boilerplate
- 0001137789-26-000153:8k_2_02:112 — heading
- 0001137789-26-000153:8k_2_02:113 — definition boilerplate
- 0001137789-26-000153:8k_2_02:114 — heading
- 0001137789-26-000153:8k_2_02:115 — definition boilerplate

### Auditor's report
- 0001137789-26-000159:auditors_report:1 — heading
- 0001137789-26-000159:auditors_report:2 — addressee
- 0001137789-26-000159:auditors_report:3 — heading
- 0001137789-26-000159:auditors_report:4 — unqualified opinion; dates rolled forward
- 0001137789-26-000159:auditors_report:5 — cross-reference to the ICFR report; date rolled forward
- 0001137789-26-000159:auditors_report:6 — heading
- 0001137789-26-000159:auditors_report:7 — standard wording
- 0001137789-26-000159:auditors_report:8 — standard wording
- 0001137789-26-000159:auditors_report:9 — heading
- 0001137789-26-000159:auditors_report:10 — standard CAM introduction
- 0001137789-26-000159:auditors_report:11 — CAM on sales incentive programs, the same subject as the critical estimate in mdna:112; no change evident (prior report not in input)
- 0001137789-26-000159:auditors_report:12 — page number
- 0001137789-26-000159:auditors_report:13 — CAM procedures; no change evident
- 0001137789-26-000159:auditors_report:14 — signature
- 0001137789-26-000159:auditors_report:15 — tenure since 1980, carried
- 0001137789-26-000159:auditors_report:16 — location
- 0001137789-26-000159:auditors_report:17 — date
- 0001137789-26-000159:auditors_report:18 — page number
- 0001137789-26-000159:auditors_report:19 — heading
- 0001137789-26-000159:auditors_report:20 — addressee
- 0001137789-26-000159:auditors_report:21 — heading
- 0001137789-26-000159:auditors_report:22 — unqualified ICFR opinion; date rolled forward
- 0001137789-26-000159:auditors_report:23 — cross-reference; date rolled forward
- 0001137789-26-000159:auditors_report:24 — heading
- 0001137789-26-000159:auditors_report:25 — standard wording
- 0001137789-26-000159:auditors_report:26 — standard wording
- 0001137789-26-000159:auditors_report:27 — standard wording
- 0001137789-26-000159:auditors_report:28 — heading
- 0001137789-26-000159:auditors_report:29 — standard definition
- 0001137789-26-000159:auditors_report:30 — standard limitations wording
- 0001137789-26-000159:auditors_report:31 — signature
- 0001137789-26-000159:auditors_report:32 — location
- 0001137789-26-000159:auditors_report:33 — date
- 0001137789-26-000159:auditors_report:34 — page number

### Item 9A
- 0001137789-26-000159:item_9a:1 — heading
- 0001137789-26-000159:item_9a:2 — heading
- 0001137789-26-000159:item_9a:3 — disclosure controls effective; date rolled forward
- 0001137789-26-000159:item_9a:4 — heading
- 0001137789-26-000159:item_9a:5 — standard wording
- 0001137789-26-000159:item_9a:6 — ICFR effective; date rolled forward
- 0001137789-26-000159:item_9a:7 — heading
- 0001137789-26-000159:item_9a:8 — no ICFR changes; standard wording
- 0001137789-26-000159:item_9a:9 — heading
- 0001137789-26-000159:item_9a:10 — standard limitations wording; date rolled forward
- 0001137789-26-000159:item_9a:11 — page number

### MD&A
- 0001137789-26-000159:mdna:1 — heading
- 0001137789-26-000159:mdna:2 — framing; dates rolled forward
- 0001137789-26-000159:mdna:4 — organization lead-in
- 0001137789-26-000159:mdna:5 — organization bullet
- 0001137789-26-000159:mdna:6 — organization bullet
- 0001137789-26-000159:mdna:7 — organization bullet
- 0001137789-26-000159:mdna:8 — organization bullet
- 0001137789-26-000159:mdna:9 — page number
- 0001137789-26-000159:mdna:10 — cross-reference
- 0001137789-26-000159:mdna:11 — heading
- 0001137789-26-000159:mdna:12 — amounts only; repurchases and dividends covered by the notes:191 item
- 0001137789-26-000159:mdna:14 — heading
- 0001137789-26-000159:mdna:17 — cross-reference
- 0001137789-26-000159:mdna:18 — heading
- 0001137789-26-000159:mdna:19 — lead-in
- 0001137789-26-000159:mdna:20 — table, amounts only
- 0001137789-26-000159:mdna:21 — table, amounts only
- 0001137789-26-000159:mdna:22 — heading
- 0001137789-26-000159:mdna:23 — lead-in
- 0001137789-26-000159:mdna:24 — channel, geography, market and exabyte table, amounts only
- 0001137789-26-000159:mdna:25 — rule line
- 0001137789-26-000159:mdna:26 — footnote, carried
- 0001137789-26-000159:mdna:27 — table, amounts only
- 0001137789-26-000159:mdna:29 — page number
- 0001137789-26-000159:mdna:30 — heading
- 0001137789-26-000159:mdna:31 — table, amounts only
- 0001137789-26-000159:mdna:33 — heading
- 0001137789-26-000159:mdna:34 — table, amounts only
- 0001137789-26-000159:mdna:37 — same $105 million charge as the notes:236 item; covered there
- 0001137789-26-000159:mdna:39 — heading
- 0001137789-26-000159:mdna:40 — table, amounts only
- 0001137789-26-000159:mdna:41 — amounts only; debt-transaction loss covered by the notes:116 and notes:123 items
- 0001137789-26-000159:mdna:42 — heading
- 0001137789-26-000159:mdna:43 — table, amounts only
- 0001137789-26-000159:mdna:44 — amounts only
- 0001137789-26-000159:mdna:47 — prior-year tax explanation, carried
- 0001137789-26-000159:mdna:48 — heading
- 0001137789-26-000159:mdna:49 — carried liquidity boilerplate
- 0001137789-26-000159:mdna:50 — carried boilerplate; date rolled forward
- 0001137789-26-000159:mdna:51 — heading
- 0001137789-26-000159:mdna:52 — table, amounts only
- 0001137789-26-000159:mdna:53 — lead-in
- 0001137789-26-000159:mdna:54 — table, amounts only
- 0001137789-26-000159:mdna:55 — heading
- 0001137789-26-000159:mdna:56 — lead-in, amounts only
- 0001137789-26-000159:mdna:61 — prior-year lead-in, carried
- 0001137789-26-000159:mdna:62 — prior-year receivables explanation, carried; used in the mdna:57 item
- 0001137789-26-000159:mdna:63 — prior-year explanation, carried
- 0001137789-26-000159:mdna:64 — prior-year inventory explanation, carried; used in the mdna:58 item
- 0001137789-26-000159:mdna:65 — prior-year explanation, carried
- 0001137789-26-000159:mdna:66 — heading
- 0001137789-26-000159:mdna:67 — amounts only (capex, investment sale, divestiture receipts)
- 0001137789-26-000159:mdna:68 — prior-year investing discussion, carried
- 0001137789-26-000159:mdna:69 — heading
- 0001137789-26-000159:mdna:70 — lead-in, amounts only
- 0001137789-26-000159:mdna:71 — amounts only; covered by the mdna:13 item
- 0001137789-26-000159:mdna:72 — amounts only
- 0001137789-26-000159:mdna:73 — amounts only; covered by the notes:191 item
- 0001137789-26-000159:mdna:74 — amounts only
- 0001137789-26-000159:mdna:75 — amounts only
- 0001137789-26-000159:mdna:76 — amounts only
- 0001137789-26-000159:mdna:77 — prior-year financing discussion, carried
- 0001137789-26-000159:mdna:78 — prior year, carried
- 0001137789-26-000159:mdna:79 — prior year, carried
- 0001137789-26-000159:mdna:80 — prior year, carried
- 0001137789-26-000159:mdna:81 — prior year, carried
- 0001137789-26-000159:mdna:82 — prior year, carried
- 0001137789-26-000159:mdna:83 — prior year, carried
- 0001137789-26-000159:mdna:84 — page number
- 0001137789-26-000159:mdna:85 — heading
- 0001137789-26-000159:mdna:86 — amounts only
- 0001137789-26-000159:mdna:87 — carried; date rolled forward
- 0001137789-26-000159:mdna:88 — covenant and compliance; covered by the notes:129 item
- 0001137789-26-000159:mdna:89 — carried sufficiency statement
- 0001137789-26-000159:mdna:90 — cross-reference
- 0001137789-26-000159:mdna:91 — heading
- 0001137789-26-000159:mdna:92 — insufficient (see above)
- 0001137789-26-000159:mdna:93 — heading
- 0001137789-26-000159:mdna:94 — amounts only; market-share commitments covered by the notes:249 item
- 0001137789-26-000159:mdna:95 — heading
- 0001137789-26-000159:mdna:97 — heading
- 0001137789-26-000159:mdna:98 — amounts only
- 0001137789-26-000159:mdna:99 — page number
- 0001137789-26-000159:mdna:100 — heading
- 0001137789-26-000159:mdna:102 — heading
- 0001137789-26-000159:mdna:104 — heading
- 0001137789-26-000159:mdna:105 — amounts only; covered by the notes:152 item
- 0001137789-26-000159:mdna:106 — heading
- 0001137789-26-000159:mdna:107 — dates rolled forward; per-share dividend same as the prior declaration
- 0001137789-26-000159:mdna:108 — heading
- 0001137789-26-000159:mdna:109 — covered by the notes:191 item
- 0001137789-26-000159:mdna:110 — carried boilerplate on capital needs
- 0001137789-26-000159:mdna:111 — heading
- 0001137789-26-000159:mdna:112 — insufficient (see above)
- 0001137789-26-000159:mdna:113 — carried sales program accrual policy
- 0001137789-26-000159:mdna:114 — carried income tax policy
- 0001137789-26-000159:mdna:115 — carried income tax policy
- 0001137789-26-000159:mdna:116 — carried income tax policy
- 0001137789-26-000159:mdna:117 — heading
- 0001137789-26-000159:mdna:118 — cross-reference

### Notes
- 0001137789-26-000159:notes:1 — proxy and AGM dates rolled forward
- 0001137789-26-000159:notes:2 — heading
- 0001137789-26-000159:notes:3 — cybersecurity boilerplate; no change evident
- 0001137789-26-000159:notes:4 — cybersecurity boilerplate; no change evident
- 0001137789-26-000159:notes:5 — cybersecurity boilerplate; no change evident
- 0001137789-26-000159:notes:6 — cybersecurity boilerplate; no change evident
- 0001137789-26-000159:notes:7 — heading
- 0001137789-26-000159:notes:8 — governance boilerplate; no change evident
- 0001137789-26-000159:notes:9 — governance boilerplate; no change evident
- 0001137789-26-000159:notes:10 — governance boilerplate; no change evident
- 0001137789-26-000159:notes:11 — governance boilerplate; no change evident
- 0001137789-26-000159:notes:12 — insufficient (see above)
- 0001137789-26-000159:notes:13 — heading
- 0001137789-26-000159:notes:15 — heading
- 0001137789-26-000159:notes:16 — carried consolidation policy
- 0001137789-26-000159:notes:17 — carried estimates wording
- 0001137789-26-000159:notes:18 — heading
- 0001137789-26-000159:notes:19 — covered by the mdna:3 item
- 0001137789-26-000159:notes:20 — heading
- 0001137789-26-000159:notes:21 — carried policy
- 0001137789-26-000159:notes:22 — carried policy
- 0001137789-26-000159:notes:23 — carried inventory policy
- 0001137789-26-000159:notes:24 — carried PP&E policy
- 0001137789-26-000159:notes:25 — carried goodwill policy
- 0001137789-26-000159:notes:26 — carried lease policy
- 0001137789-26-000159:notes:27 — carried lease policy
- 0001137789-26-000159:notes:28 — carried lease policy
- 0001137789-26-000159:notes:29 — carried long-lived asset policy
- 0001137789-26-000159:notes:30 — carried warranty policy
- 0001137789-26-000159:notes:31 — carried revenue policy
- 0001137789-26-000159:notes:32 — carried revenue policy
- 0001137789-26-000159:notes:33 — carried sales incentive policy
- 0001137789-26-000159:notes:34 — carried; date rolled forward
- 0001137789-26-000159:notes:35 — carried commissions policy
- 0001137789-26-000159:notes:36 — carried restructuring policy
- 0001137789-26-000159:notes:37 — amounts only
- 0001137789-26-000159:notes:38 — carried share-based compensation policy
- 0001137789-26-000159:notes:39 — carried tax policy
- 0001137789-26-000159:notes:40 — carried tax policy
- 0001137789-26-000159:notes:41 — carried equity investment policy
- 0001137789-26-000159:notes:42 — carried equity investment policy
- 0001137789-26-000159:notes:43 — carried equity investment policy
- 0001137789-26-000159:notes:44 — carried equity investment policy
- 0001137789-26-000159:notes:45 — carried FX policy
- 0001137789-26-000159:notes:46 — carried business combination policy
- 0001137789-26-000159:notes:47 — carried government incentive policy
- 0001137789-26-000159:notes:48 — carried grant terms; used in the notes:49 item
- 0001137789-26-000159:notes:50 — prior-year grant amounts, carried; used in the notes:49 item
- 0001137789-26-000159:notes:51 — heading
- 0001137789-26-000159:notes:52 — carried use-of-estimates wording
- 0001137789-26-000159:notes:53 — heading
- 0001137789-26-000159:notes:55 — insufficient (see above)
- 0001137789-26-000159:notes:56 — carried counterparty wording
- 0001137789-26-000159:notes:57 — carried supplier concentration
- 0001137789-26-000159:notes:58 — insufficient (see above)
- 0001137789-26-000159:notes:59 — heading
- 0001137789-26-000159:notes:62 — heading
- 0001137789-26-000159:notes:63 — carried pending standard (ASU 2024-03)
- 0001137789-26-000159:notes:65 — heading
- 0001137789-26-000159:notes:66 — lead-in
- 0001137789-26-000159:notes:67 — table, amounts only
- 0001137789-26-000159:notes:68 — heading
- 0001137789-26-000159:notes:69 — carried factoring description
- 0001137789-26-000159:notes:71 — heading
- 0001137789-26-000159:notes:72 — lead-in
- 0001137789-26-000159:notes:73 — inventory table, amounts only; WIP used in the mdna:58 item
- 0001137789-26-000159:notes:74 — heading
- 0001137789-26-000159:notes:75 — lead-in
- 0001137789-26-000159:notes:76 — table, amounts only
- 0001137789-26-000159:notes:77 — heading
- 0001137789-26-000159:notes:78 — lead-in
- 0001137789-26-000159:notes:79 — table, amounts only
- 0001137789-26-000159:notes:80 — amounts only
- 0001137789-26-000159:notes:81 — heading
- 0001137789-26-000159:notes:82 — lead-in
- 0001137789-26-000159:notes:83 — table, amounts only
- 0001137789-26-000159:notes:84 — heading
- 0001137789-26-000159:notes:85 — lead-in
- 0001137789-26-000159:notes:86 — table, amounts only; tax payable line used in the mdna:45 item
- 0001137789-26-000159:notes:87 — heading
- 0001137789-26-000159:notes:88 — carried supplier finance program description
- 0001137789-26-000159:notes:89 — carried classification wording; used in the mdna:60 item
- 0001137789-26-000159:notes:90 — lead-in
- 0001137789-26-000159:notes:91 — supplier finance rollforward, amounts only; used in the mdna:60 item
- 0001137789-26-000159:notes:92 — heading
- 0001137789-26-000159:notes:93 — lead-in
- 0001137789-26-000159:notes:94 — AOCI table, amounts only
- 0001137789-26-000159:notes:95 — heading
- 0001137789-26-000159:notes:96 — carried; dates rolled forward
- 0001137789-26-000159:notes:97 — heading
- 0001137789-26-000159:notes:99 — heading and lead-in; date rolled forward
- 0001137789-26-000159:notes:100 — debt table, amounts only; used in the mdna:101 and notes:125 items
- 0001137789-26-000159:notes:101 — rule line
- 0001137789-26-000159:notes:102 — carried guarantee footnote
- 0001137789-26-000159:notes:103 — carried guarantee footnote
- 0001137789-26-000159:notes:104 — carried interest-date footnote
- 0001137789-26-000159:notes:105 — carried interest-date footnote
- 0001137789-26-000159:notes:106 — carried interest-date footnote
- 0001137789-26-000159:notes:107 — carried interest-date footnote
- 0001137789-26-000159:notes:108 — heading
- 0001137789-26-000159:notes:109 — carried obligor exchange description
- 0001137789-26-000159:notes:110 — carried; the added fee sentence says only "immaterial" with no amount
- 0001137789-26-000159:notes:111 — carried
- 0001137789-26-000159:notes:112 — heading
- 0001137789-26-000159:notes:113 — carried issuance terms
- 0001137789-26-000159:notes:114 — cap price adjustment, amounts only
- 0001137789-26-000159:notes:115 — carried fiscal 2024 history
- 0001137789-26-000159:notes:118 — carried redemption terms; the partial-redemption minimum sentence no longer appears, which is moot after the full call (covered by the notes:119 item)
- 0001137789-26-000159:notes:121 — amounts only
- 0001137789-26-000159:notes:122 — heading
- 0001137789-26-000159:notes:124 — heading
- 0001137789-26-000159:notes:126 — heading
- 0001137789-26-000159:notes:127 — carried; date rolled forward
- 0001137789-26-000159:notes:128 — carried
- 0001137789-26-000159:notes:130 — heading
- 0001137789-26-000159:notes:131 — lead-in; date rolled forward
- 0001137789-26-000159:notes:132 — principal schedule, amounts only; used in the mdna:101 item
- 0001137789-26-000159:notes:133 — heading and lead-in
- 0001137789-26-000159:notes:134 — table, amounts only
- 0001137789-26-000159:notes:135 — lead-in
- 0001137789-26-000159:notes:136 — table, amounts only
- 0001137789-26-000159:notes:137 — lead-in
- 0001137789-26-000159:notes:138 — deferred tax table, amounts only
- 0001137789-26-000159:notes:139 — carried realizability wording; amount only
- 0001137789-26-000159:notes:141 — amounts only; dates rolled forward
- 0001137789-26-000159:notes:142 — amounts only
- 0001137789-26-000159:notes:143 — lead-in; covered by the notes:60 item
- 0001137789-26-000159:notes:144 — rate reconciliation, amounts only; used in the mdna:45 and notes:140 items
- 0001137789-26-000159:notes:145 — lead-in
- 0001137789-26-000159:notes:146 — prior-year rate reconciliation, carried
- 0001137789-26-000159:notes:147 — lead-in
- 0001137789-26-000159:notes:148 — cash taxes table, amounts only; covered by the notes:60 item
- 0001137789-26-000159:notes:149 — context on OBBBA enactment; its effects are itemized at mdna:46 and notes:140
- 0001137789-26-000159:notes:151 — carried reinvestment wording
- 0001137789-26-000159:notes:153 — lead-in
- 0001137789-26-000159:notes:154 — rollforward table, amounts only; covered by the notes:152 item
- 0001137789-26-000159:notes:155 — carried; open tax years rolled forward
- 0001137789-26-000159:notes:156 — carried lease description
- 0001137789-26-000159:notes:157 — carried lease description
- 0001137789-26-000159:notes:158 — carried fiscal 2024 sale-leaseback
- 0001137789-26-000159:notes:159 — lead-in
- 0001137789-26-000159:notes:160 — table, amounts only
- 0001137789-26-000159:notes:161 — amounts only
- 0001137789-26-000159:notes:162 — table, amounts only
- 0001137789-26-000159:notes:163 — lead-in
- 0001137789-26-000159:notes:164 — table, amounts only
- 0001137789-26-000159:notes:165 — lead-in
- 0001137789-26-000159:notes:166 — table, amounts only
- 0001137789-26-000159:notes:167 — heading
- 0001137789-26-000159:notes:168 — fair value boilerplate
- 0001137789-26-000159:notes:169 — heading
- 0001137789-26-000159:notes:170 — fair value boilerplate
- 0001137789-26-000159:notes:171 — fair value boilerplate
- 0001137789-26-000159:notes:172 — fair value boilerplate
- 0001137789-26-000159:notes:173 — fair value boilerplate
- 0001137789-26-000159:notes:174 — fair value boilerplate
- 0001137789-26-000159:notes:175 — heading
- 0001137789-26-000159:notes:176 — lead-in
- 0001137789-26-000159:notes:177 — table, amounts only
- 0001137789-26-000159:notes:178 — amounts only
- 0001137789-26-000159:notes:179 — carried; date rolled forward
- 0001137789-26-000159:notes:180 — carried
- 0001137789-26-000159:notes:181 — heading
- 0001137789-26-000159:notes:182 — carried
- 0001137789-26-000159:notes:184 — heading
- 0001137789-26-000159:notes:185 — carried valuation method
- 0001137789-26-000159:notes:186 — debt fair value table, amounts only
- 0001137789-26-000159:notes:187 — heading
- 0001137789-26-000159:notes:188 — share count, amounts only
- 0001137789-26-000159:notes:189 — heading
- 0001137789-26-000159:notes:190 — carried
- 0001137789-26-000159:notes:192 — heading
- 0001137789-26-000159:notes:194 — carried EPB description; naming point noted in the notes:193 item
- 0001137789-26-000159:notes:195 — amounts only
- 0001137789-26-000159:notes:196 — heading
- 0001137789-26-000159:notes:197 — amounts only
- 0001137789-26-000159:notes:198 — heading
- 0001137789-26-000159:notes:199 — carried vesting terms
- 0001137789-26-000159:notes:200 — lead-in
- 0001137789-26-000159:notes:201 — table, amounts only
- 0001137789-26-000159:notes:202 — amounts only
- 0001137789-26-000159:notes:203 — lead-in
- 0001137789-26-000159:notes:204 — table, amounts only
- 0001137789-26-000159:notes:205 — carried assumption wording
- 0001137789-26-000159:notes:206 — carried liability-award wording
- 0001137789-26-000159:notes:207 — amounts only
- 0001137789-26-000159:notes:208 — heading
- 0001137789-26-000159:notes:209 — carried PSU terms
- 0001137789-26-000159:notes:210 — table, amounts only
- 0001137789-26-000159:notes:211 — amounts only
- 0001137789-26-000159:notes:212 — lead-in
- 0001137789-26-000159:notes:213 — table, amounts only
- 0001137789-26-000159:notes:214 — heading
- 0001137789-26-000159:notes:215 — carried option terms
- 0001137789-26-000159:notes:216 — 401(k) match amounts only
- 0001137789-26-000159:notes:217 — heading
- 0001137789-26-000159:notes:218 — carried indemnification wording
- 0001137789-26-000159:notes:219 — carried indemnification wording
- 0001137789-26-000159:notes:220 — heading
- 0001137789-26-000159:notes:221 — carried indemnification wording
- 0001137789-26-000159:notes:222 — heading
- 0001137789-26-000159:notes:223 — carried guarantee wording
- 0001137789-26-000159:notes:224 — heading
- 0001137789-26-000159:notes:225 — lead-in
- 0001137789-26-000159:notes:226 — warranty rollforward, amounts only; no prose explanation accompanies it
- 0001137789-26-000159:notes:227 — carried EPS method
- 0001137789-26-000159:notes:228 — carried EPS method
- 0001137789-26-000159:notes:229 — lead-in
- 0001137789-26-000159:notes:230 — table, amounts only
- 0001137789-26-000159:notes:231 — carried anti-dilution wording
- 0001137789-26-000159:notes:232 — carried contingency policy
- 0001137789-26-000159:notes:233 — heading
- 0001137789-26-000159:notes:237 — carried IP Bridge case; no new development stated
- 0001137789-26-000159:notes:238 — heading
- 0001137789-26-000159:notes:239 — carried BIS settlement terms
- 0001137789-26-000159:notes:240 — carried BIS audit terms
- 0001137789-26-000159:notes:241 — BIS accrual and payments, amounts only; date rolled forward
- 0001137789-26-000159:notes:242 — heading
- 0001137789-26-000159:notes:243 — carried environmental wording
- 0001137789-26-000159:notes:244 — carried Superfund wording
- 0001137789-26-000159:notes:245 — carried
- 0001137789-26-000159:notes:246 — carried
- 0001137789-26-000159:notes:247 — heading
- 0001137789-26-000159:notes:248 — carried
- 0001137789-26-000159:notes:250 — capex commitments, amounts only; outlook covered by the mdna:96 item
- 0001137789-26-000159:notes:251 — carried segment wording
- 0001137789-26-000159:notes:252 — carried
- 0001137789-26-000159:notes:253 — lead-in
- 0001137789-26-000159:notes:254 — long-lived assets by country, amounts only
- 0001137789-26-000159:notes:255 — heading and lead-in
- 0001137789-26-000159:notes:256 — revenue by channel, amounts only
- 0001137789-26-000159:notes:257 — revenue by country, amounts only
- 0001137789-26-000159:notes:258 — lead-in
- 0001137789-26-000159:notes:259 — carried footnote
- 0001137789-26-000159:notes:260 — heading
- 0001137789-26-000159:notes:261 — carried Intevac acquisition
- 0001137789-26-000159:notes:262 — carried Intevac allocation
- 0001137789-26-000159:notes:263 — heading
- 0001137789-26-000159:notes:264 — heading
- 0001137789-26-000159:notes:266 — carried SoC deferred liability and fiscal 2024 gain
- 0001137789-26-000159:notes:267 — heading
- 0001137789-26-000159:notes:268 — dividend subsequent event; dates rolled forward, per-share amount same as the Q2 and Q3 declarations
- 0001137789-26-000159:notes:269 — lead-in
- 0001137789-26-000159:notes:271 — director plan termination; covered by the notes:270 item
- 0001137789-26-000159:notes:272 — footnote
