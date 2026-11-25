# report_notes_text — CARR 10-Q 0001783180-26-000032 (quarter ended June 30, 2026), against 0001783180-26-000026

**Inputs read in full:** `input_notes.md`, `input_notes_history.md`, `input_mdna.md`, `input_controls.md` (Item 4 only), `input_8k.md` (the item-code list plus the Item 2.02 earnings release 0001783180-26-000030), and `input_prior_predictions.md`.

**Not in the input:**
- an auditor's report (this is a 10-Q)
- an Item 1A diff
- an Exhibit 21 diff
- any Exhibit 10

**Forbidden-content check:** none found. The 8-K carries the release's own financial tables. Those tables are part of the 8-K body. There is no trend table, price, return, short-interest figure, other company's file, prior probability or outcome window.

**Prior flags:** none on record.

**How I read it:** I did no arithmetic. Where two stated figures appear, I quote both and leave the comparison to the numbers reader and supervisor. Directions are what the prose implies.

## Items

```json
[
  {
    "id": "revenue_recognition_csa_commercial_decline_attributed_to_delivery_timing",
    "what_changed": "MD&A now attributes the quarter's CSA commercial decline (stated down 6%) to timing of customer deliveries, offset by improved price. Residential (stated up 9%) is attributed to end-market demand and pricing, and light commercial is stated up 10%. Calling it 'timing' means sales were deferred rather than lost.",
    "account": "Net sales (CSA commercial)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "These results were partially offset by volume reductions in our commercial business (down 6%) driven by timing of customer deliveries offset by improved price.",
    "paragraph_id": "0001783180-26-000032:mdna:93",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_csa_commercial_decline_rate_and_noresco_exclusion",
    "what_changed": "The earnings release states CSA Commercial down 8% on delivery timing, with footnote 1 'Excludes NORESCO' (8k_2_02:32). The 10-Q MD&A states the CSA commercial business down 6% (mdna:93) and does not say NORESCO is excluded. The two documents give different figures and possibly different scopes for the same line; the supervisor should reconcile them.",
    "account": "Net sales (CSA commercial)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "partially offset by Commercial1, down 8% due to the timing of customer deliveries.",
    "paragraph_id": "0001783180-26-000030:8k_2_02:26",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_csa_growth_attributed_to_price_versus_volume",
    "what_changed": "The release says CSA 'revenue growth mainly related to price', more than offset by mix and input costs. The 10-Q MD&A credits CSA organic growth to volume: 'improved end-market demand resulted in higher volumes' (mdna:23) and 'driven by volume growth within certain end-markets' (mdna:93). The two documents attribute CSA growth to different drivers.",
    "account": "Net sales (CSA) — price versus volume",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Segment operating margin decreased 260 basis points as revenue growth mainly related to price which was more than offset by unfavorable mix and input costs.",
    "paragraph_id": "0001783180-26-000030:8k_2_02:27",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_organic_growth_attributed_to_higher_volumes",
    "what_changed": "MD&A now reports organic sales growth for the quarter (stated 3%). It credits mainly CSA higher volumes from improved end-market demand, plus improved demand in CSE and CSAME, and says CST was flat.",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The organic increase was primarily due to our Climate Solutions Americas segment as improved end-market demand resulted in higher volumes.",
    "paragraph_id": "0001783180-26-000032:mdna:23",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_csa_six_month_demand_described_both_improved_and_reduced",
    "what_changed": "For the six months, the consolidated sales paragraph (mdna:54) credits the organic increase to 'improved end-market demand across' CSA, CSE and CSAME, and says 'continued end-market demand' in CST also helped. The six-month CSA segment paragraph says residential was flat on 'reduced end-market demand' and commercial was down 2% on 'lower end-market demand'; only light commercial is described with ongoing demand. The six-month CST paragraph (mdna:149) says truck and trailer fell on 'reduced end-market demand across all regions'. Two sections of the same MD&A describe the same period's CSA demand in opposite terms.",
    "account": "Net sales (CSA)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Results in our residential business (flat) was primarily driven by reduced end-market demand offset by product mix.",
    "paragraph_id": "0001783180-26-000032:mdna:127",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_tariffs_and_input_costs_on_gross_margin",
    "what_changed": "MD&A attributes the quarter's gross margin decrease (stated $41 million, 170 basis points) mainly to higher input costs, including tariffs, and unfavorable mix, partly offset by volume and productivity. The same tariff and input-cost cause is cited in other places:\n- CSA operational profit (mdna:96, mdna:131)\n- the six-month gross margin (mdna:58)\n- the release's adjusted margin explanation (8k_2_02:21)",
    "account": "Cost of products sold / gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Gross margin decreased by $41 million compared with the three months ended June 30, 2025, primarily due to higher input costs, including the impact of tariffs, and unfavorable business mix.",
    "paragraph_id": "0001783180-26-000032:mdna:27",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_ieepa_tariff_refund_not_recorded",
    "what_changed": "The paragraph is changed text. It says:\n- In February 2026 the Supreme Court held IEEPA tariffs unauthorized.\n- Carrier was importer of record.\n- In March 2026 the Court of International Trade ordered U.S. Customs and Border Protection to refund them.\n- As of June 30, 2026 no refund benefit is recorded, because it is not probable and reasonably estimable.\nThis is an unrecognized gain contingency on tariffs the MD&A elsewhere says depressed margins. The prior wording is not in the input, so I cannot tell whether only the date rolled forward or the refund-order sentence is also new.",
    "account": "Cost of products sold (unrecognized tariff refund)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, we have not recorded any benefit related to potential refunds of IEEPA tariffs paid, as such amounts were not considered probable and reasonably estimable.",
    "paragraph_id": "0001783180-26-000032:mdna:8",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_riello_impairment_in_other_income",
    "what_changed": "New: a $46 million Riello impairment recognized in Other income (expense), net in the quarter. It appears in three other places:\n- as 'Impairment on held for sale assets' in the held-for-sale table (notes:105)\n- as a separate 'Riello impairment' line excluded from segment and adjusted operating profit (notes:117, mdna:45, 8k_2_02:105)\n- in MD&A, which attributes it to the CSE segment (mdna:34, mdna:65)\nThe tax note (notes:94) calls it non-deductible.",
    "account": "Other income (expense), net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The Company recognized an impairment charge of $46 million recorded in Other income (expense), net on the accompanying Unaudited Condensed Consolidated Statement of Operations during the three months ended June 30, 2026.",
    "paragraph_id": "0001783180-26-000032:notes:102",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_riello_sale_completed_after_period_end",
    "what_changed": "New sentence: the Riello sale to Ariston Group (expected gross proceeds about $430 million) closed on July 1, 2026, after the balance sheet date. The same fact appears in notes:102, mdna:13, mdna:167, 8k_2_02:15 and 8k_2_02:49. Riello's held-for-sale assets and liabilities should leave the balance sheet next quarter. The release cites a ~$225 million year-over-year revenue headwind from the exit; its prior guidance column said ~$250 million.",
    "account": "Assets held for sale / Liabilities held for sale",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The sale of Riello was completed on July 1, 2026.",
    "paragraph_id": "0001783180-26-000032:notes:4",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_noresco_classified_held_for_sale",
    "what_changed": "New paragraph:\n- On May 18, 2026 the Company agreed to sell Noresco to Opterra Energy Services, LLC, a subsidiary of LS Power Development, LLC.\n- Noresco was historically in the CSA segment and is presented as held for sale at June 30, 2026.\n- Closing is expected in Q3 2026.\n- No price, gain, loss or impairment is stated for Noresco.\nRelated text elsewhere:\n- The release cites a ~$125 million revenue headwind from the exit (8k_2_02:48).\n- The release excludes NORESCO from its orders and CSA Commercial figures.\n- The goodwill table (notes:17) shows a CSA amount on its 'Reclassified to held for sale' row.",
    "account": "Assets held for sale / Liabilities held for sale",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "As a result, the assets and liabilities of Noresco are presented as held for sale in the accompanying Unaudited Condensed Consolidated Balance Sheet as of June 30, 2026.",
    "paragraph_id": "0001783180-26-000032:notes:103",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_debt_rows_inside_liabilities_held_for_sale",
    "what_changed": "The held-for-sale table now has rows for 'Short-term borrowings and current portion of long-term debt' and 'Long-term debt'. Each carries a June 30, 2026 amount and shows '—' at December 31, 2025. The table also adds a row 'Impairment on held for sale assets'. The prose does not say which disposal group the debt belongs to (Riello or Noresco). The debt note tables (notes:24, notes:28) and the release's net debt reconciliation (8k_2_02:121) list only the balance-sheet debt lines, so debt classified as held for sale sits outside those presentations.",
    "account": "Liabilities held for sale (debt)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Short-term borrowings and current portion of long-term debt | 52",
    "paragraph_id": "0001783180-26-000032:notes:105",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_commercial_paper_outstanding_and_weighted_rate",
    "what_changed": "The commercial paper paragraph now states $685 million outstanding at June 30, 2026 at a 4.01% weighted average rate. The prior paragraph (0001783180-26-000026:note_history:13) stated $708 million at 4.06% at March 31, 2026. MD&A (mdna:162) repeats the $685 million and says the Revolving Credit Facility has zero borrowings.",
    "account": "Short-term borrowings (commercial paper)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "At June 30, 2026, the Company had $685 million outstanding under its commercial paper facilities with a weighted average interest rate of 4.01%.",
    "paragraph_id": "0001783180-26-000032:notes:26",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_interest_expense_attributed_to_commercial_paper",
    "what_changed": "MD&A attributes the quarter's interest expense increase (stated $126 million, a 10% increase) to commercial paper borrowings outstanding. The six-month paragraph (mdna:69) gives the same cause for its stated $237 million, a 4% increase.",
    "account": "Interest expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase is a result of commercial paper borrowings outstanding during the three months ended June 30, 2026.",
    "paragraph_id": "0001783180-26-000032:mdna:38",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_short_term_borrowings_partly_offset_shareholder_returns",
    "what_changed": "The six-month financing narrative names repurchases of $745 million and dividends of $400 million as the outflows, partly offset by $361 million of short-term borrowings. The prose ties shareholder returns to short-term borrowing inflows.",
    "account": "Short-term borrowings",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These outflows were partially offset by short-term borrowings of $361 million.",
    "paragraph_id": "0001783180-26-000032:mdna:179",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_and_remaining_authorization",
    "what_changed": "The notes state 12.0 million shares repurchased in the six months for an aggregate purchase price of $748 million, with about $4.6 billion of authorization remaining (also mdna:170). The financing cash-flow paragraph (mdna:179) states repurchases totaling $745 million. The two stated figures are not identical (purchase price versus cash-paid wording); the supervisor should reconcile them. The release says ~$640 million was returned through dividends and repurchases in the quarter (8k_2_02:10) and credits a lower share count in its EPS paragraph (8k_2_02:22). Treasury share counts are rolled forward in notes:67.",
    "account": "Treasury stock",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the six months ended June 30, 2026, the Company repurchased 12.0 million shares of common stock for an aggregate purchase price of $748 million.",
    "paragraph_id": "0001783180-26-000032:notes:70",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_dividend_declared_for_august_payment",
    "what_changed": "Six-month dividends paid are stated as $400 million. A June 2026 declaration of $0.24 per share is payable August 10, 2026 to holders of record on July 21, 2026.",
    "account": "Dividends payable / Retained earnings",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "In June 2026, the Board of Directors declared a dividend of $0.24 per share of common stock payable on August 10, 2026, to shareowners of record at the close of business on July 21, 2026.",
    "paragraph_id": "0001783180-26-000032:mdna:172",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_cash_held_by_foreign_subsidiaries",
    "what_changed": "Cash of $1.3 billion at June 30, 2026, of which about 95% was held by foreign subsidiaries. Restricted cash is stated at about $3 million at June 30, 2026 and $2 million at December 31, 2025.",
    "account": "Cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, we had cash and cash equivalents of $1.3 billion, of which approximately 95% was held by our foreign subsidiaries.",
    "paragraph_id": "0001783180-26-000032:mdna:156",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_long_term_note_interest_and_maturity_range",
    "what_changed": "Changed text:\n- Short-term obligations are primarily current maturities of long-term debt.\n- Long-term notes mature between 2027 and 2054.\n- Note interest is expected at about $405 million a year, at about a 3.65% weighted-average rate.\nThe debt note footnote (notes:29) says the 2.493% Notes due February 27, 2027 are classified as current. The prior wording is not in the input, so whether the interest estimate moved cannot be read.",
    "account": "Interest expense / Current portion of long-term debt",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Interest payments related to long-term notes are expected to approximate $405 million per year, reflecting an approximate weighted-average interest rate of 3.65%.",
    "paragraph_id": "0001783180-26-000032:mdna:163",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_project_financing_debt_issued_and_repaid",
    "what_changed": "The project-financing paragraph now gives six-month figures:\n- debt issued: $27 million in 2026, $10 million in 2025\n- repayments: $53 million in 2026, zero in 2025\nThe prior paragraph gave Q1 figures: $14 million issued and $14 million repaid. The debt table's 'Other debt (including project financing obligations and finance leases)' line is in notes:28. The held-for-sale table now carries debt rows (see the held-for-sale debt item).",
    "account": "Long-term debt (other debt including project financing obligations)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Long-term debt repayments associated with these financing arrangements during the six months ended June 30, 2026 and 2025, were $53 million and zero, respectively.",
    "paragraph_id": "0001783180-26-000032:notes:33",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_attributed_to_working_capital",
    "what_changed": "MD&A credits the six-month increase in continuing operating cash flow to favorable working-capital changes, partly offset by lower net earnings. The claim is about receivables, inventories and payables together. The number being explained is operating cash flow, not a receivable, inventory or reserve balance.",
    "account": "Net cash flows from continuing operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The year-over-year increase in net cash provided by continuing operating activities was primarily driven by favorable changes in working capital balances partially offset by lower net earnings compared with the prior period.",
    "paragraph_id": "0001783180-26-000032:mdna:176",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_capital_expenditures_primary_investing_outflow",
    "what_changed": "The six-month investing narrative names $211 million of capital expenditures as the main driver of the $235 million outflow. For 2025 it names $144 million of capex partly offset by an $87 million derivative-settlement inflow. The release separately cites new U.S. factory costs in its outlook (8k_2_02:12).",
    "account": "Capital expenditures",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The primary driver of the outflow related to $211 million of capital expenditures.",
    "paragraph_id": "0001783180-26-000032:mdna:178",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_restructuring_costs_in_gross_margin",
    "what_changed": "The six-month gross margin decrease (stated $242 million, 300 basis points) is now also attributed to higher costs from announced restructuring initiatives, on top of input costs, tariffs and mix. The quarter's gross margin paragraph (mdna:27) does not mention restructuring. Restructuring is excluded from adjusted operating profit.",
    "account": "Cost of products sold (restructuring)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In addition, an increase in costs associated with announced restructuring initiatives further impacted our results.",
    "paragraph_id": "0001783180-26-000032:mdna:58",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_restructuring_and_compensation_drive_six_month_sga",
    "what_changed": "The six-month SG&A increase (stated $1.7 billion, 8% increase) is attributed mainly to announced restructuring initiatives. Higher compensation, commission and employee-related costs added to it, partly offset by lower consulting and other managed expenses.",
    "account": "Selling, general and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase primarily relates to an increase in costs associated with announced restructuring initiatives.",
    "paragraph_id": "0001783180-26-000032:mdna:62",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_incentive_compensation_costs_offset_savings",
    "what_changed": "Quarter SG&A is described as primarily flat at $810 million. Savings from cost reduction initiatives and lower managed expenses are said to be largely offset by higher investment spending and higher incentive compensation costs. The incentive-compensation accrual is newly named as a driver in the same quarter the outlook is raised.",
    "account": "Selling, general and administrative (incentive compensation accrual)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These benefits were largely offset by higher investment spending and incentive compensation costs.",
    "paragraph_id": "0001783180-26-000032:mdna:31",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_restructuring_reserve_primarily_severance",
    "what_changed": "The restructuring accrual is stated at $111 million at June 30, 2026. Management says the balance relates to cost reduction efforts, primarily severance across each segment, and expects to use a majority of it within 12 months, which means cash outflow.",
    "account": "Accrued liabilities (restructuring reserve)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The balance relates to cost reduction efforts, primarily severance related",
    "paragraph_id": "0001783180-26-000032:notes:93",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_inventory_valuation_reserve_stated",
    "what_changed": "Inventory valuation reserves are stated at $328 million at June 30, 2026 and $337 million at December 31, 2025. The assessment method sentence is unchanged and no cause is given for the reserve level.",
    "account": "Inventories, net (valuation reserve)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Raw materials, work-in-process and finished goods are net of valuation reserves of $328 million and $337 million as of June 30, 2026 and December 31, 2025, respectively.",
    "paragraph_id": "0001783180-26-000032:notes:14",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_csa_other_component_timing_and_classification",
    "what_changed": "The CSA segment profit bridge carries an 'Other' component: the table shows 3% for the quarter and 2% for six months (mdna:131). It is described only as adjustments for the timing and classification of amounts recognized in operating profit. No amount, nature or originating period is given.",
    "account": "CSA segment operating profit",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Amounts reported in other represent adjustments related to the timing and classification of amounts recognized in operating profit.",
    "paragraph_id": "0001783180-26-000032:mdna:96",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_csame_gain_on_sale_of_land_in_segment_profit",
    "what_changed": "The CSAME segment profit bridge's 'Other' component is a gain on sale of land; the table shows 17% for the quarter and 9% for six months (mdna:145). The gain is inside segment operating profit and therefore inside adjusted operating profit; no reconciliation lists a land-gain exclusion. The release's CSAME margin explanation (8k_2_02:37) does not mention it.",
    "account": "Other income (expense), net (CSAME segment)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Amounts reported in other represent a gain on sale of land.",
    "paragraph_id": "0001783180-26-000032:mdna:110",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_cse_legal_reserve_no_longer_required",
    "what_changed": "The six-month CSE profit bridge's 'Other' component (table shows 1%) is the benefit of a legal reserve no longer required. This is a reserve release inside segment operating profit, and it is not among the items excluded in the adjusted operating profit reconciliations.",
    "account": "Accrued liabilities (legal reserve)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Amounts reported in other represent the benefit of a legal reserve no longer required.",
    "paragraph_id": "0001783180-26-000032:mdna:138",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_cse_warranty_expense_higher",
    "what_changed": "The six-month CSE operational profit paragraph names higher warranty-related expenses as a further drag, alongside mix, price promotions and SG&A. The warranty note's prose is unchanged (notes:63 and notes:66 are carried as same; notes:65 is a table), so no warranty cause is given there.",
    "account": "Warranty provisions (cost of sales)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "higher warranty-related expenses further impacted the segment",
    "paragraph_id": "0001783180-26-000032:mdna:138",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_europe_pricing_promotions",
    "what_changed": "CSE residential and light commercial growth (stated up 7% for the quarter, up 4% for six months per mdna:135) is described as partly offset by pricing promotions. CSE commercial is stated down 6% on lower volumes. The CSE operational profit paragraphs (mdna:103, mdna:138) name price promotions and higher SG&A as further drags.",
    "account": "Net sales / segment operating profit (CSE)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Results in our residential and light commercial business increased (up 7%) as a result of higher volumes across the region partially offset by pricing promotions.",
    "paragraph_id": "0001783180-26-000032:mdna:100",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_cse_favorable_price_cost_versus_price_promotions",
    "what_changed": "The release lists 'favorable price / cost' as a positive for CSE margin. The 10-Q MD&A describes price promotions as a drag on CSE sales and profit (mdna:100, mdna:103). The release defines price/cost as pricing plus cost inflation plus productivity (8k_2_02:79), so the two may reconcile, but the documents describe CSE pricing differently.",
    "account": "CSE segment operating profit",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Segment operating margin decreased 70 basis points driven by volume growth and favorable price / cost more than offset by unfavorable mix and selling investments.",
    "paragraph_id": "0001783180-26-000030:8k_2_02:31",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_china_demand_and_price",
    "what_changed": "CSAME: China is stated down 14% for the quarter and down 13% for six months (mdna:142), on economic challenges affecting both demand and price. Other geographies are said to more than offset it. The release cites 'continued pressure in RLC in China' (8k_2_02:36).",
    "account": "Net sales (CSAME)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Results in China decreased (down 14%) as end-markets experienced economic challenges impacting both demand and price.",
    "paragraph_id": "0001783180-26-000032:mdna:107",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_lower_joint_venture_earnings",
    "what_changed": "MD&A attributes the quarter's equity method earnings decline (stated $58 million, a 26% decrease) to lower JV earnings in CSA and CSAME. For six months (mdna:64, $89 million, a 27% decrease) it names CSA JVs. The CSA and CSAME operational profit paragraphs (mdna:96, mdna:110) also cite lower equity-method earnings.",
    "account": "Equity method investment net earnings",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease was primarily driven by lower earnings in joint ventures within our Climate Solutions Americas and Climate Solutions Asia Pacific, Middle East & Africa segments.",
    "paragraph_id": "0001783180-26-000032:mdna:33",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_middle_east_conflict_cited_only_in_earnings_release",
    "what_changed": "The release attributes part of the CSAME margin decline to lower JV income 'due to the impacts from the Middle East conflict'. The 10-Q MD&A cites lower equity-method earnings in CSAME without naming the conflict. This external cause is new and appears only in the release. The release also cites double-digit growth in the Middle East (8k_2_02:36).",
    "account": "Equity method investment net earnings (CSAME)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Segment operating margin decreased 350 basis points driven by volume growth and productivity more than offset by unfavorable mix and lower JV income due to the impacts from the Middle East conflict.",
    "paragraph_id": "0001783180-26-000030:8k_2_02:37",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_truck_and_trailer_demand",
    "what_changed": "CST organic sales are described as flat. Container is stated up 39%. Global truck and trailer is stated down 13% on reduced demand in North America and Europe, partly offset by Asia; for six months it is down 10% on reduced demand 'across all regions' (mdna:149). The operational profit paragraphs (mdna:117, mdna:152) cite mix and lower volumes. The release says the same (8k_2_02:40, 8k_2_02:41).",
    "account": "Net sales (CST)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "These results were partially offset by lower volume in our global truck and trailer business (down 13%) primarily due to reduced end-market demand in North America and Europe partially offset by improvements in Asia.",
    "paragraph_id": "0001783180-26-000032:mdna:114",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_quarter_tax_rate_german_rate_and_nondeductible_impairment",
    "what_changed": "The quarter's tax rate is stated at 25.0% against 20.0%. The increase is attributed to the $46 million non-deductible Riello impairment and to a $10 million increase in tax expense from a higher German effective tax rate; the German item is a newly named driver that may recur. The prior-year quarter included a $6 million state capital-loss benefit and a $6 million benefit from closing the UTC 2020 IRS audit. MD&A mdna:42 carries the same text.",
    "account": "Income tax expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a $10 million increase in tax expense associated with a higher German effective tax rate during the three months ended June 30, 2026",
    "paragraph_id": "0001783180-26-000032:notes:94",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_six_month_tax_rate_discrete_benefits",
    "what_changed": "The six-month tax rate is stated at 9.4% against 20.1%. It is attributed to a net $99 million benefit from partly releasing a valuation allowance on a Swiss subsidiary and an $18 million favorable state income tax audit settlement, partly offset by the Riello and German items. The prior-year six months included a $12 million investment-tax-credit purchase benefit. These are discrete benefits. The input cannot show whether they were first disclosed in the Q1 filing. MD&A mdna:72 carries the same content.",
    "account": "Income tax expense / Future income tax benefits",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The year-over-year decrease was primarily driven by a net $99 million tax benefit from the partial release of a valuation allowance associated with our operations in a Swiss subsidiary and a favorable settlement of $18 million related to a state income tax audit in the six months ended June 30, 2026.",
    "paragraph_id": "0001783180-26-000032:notes:95",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tma_transition_tax_paragraph_removed",
    "what_changed": "The prior contingencies note had an 'Income Taxes' subsection. It said a $101 million Tax Matters Agreement transition-tax liability owed to UTC sat in Accrued liabilities at March 31, 2026 and was settled in April 2026. Both the subsection and its heading are removed from the current note. This implies the liability left Accrued liabilities and a payment was made during the quarter.",
    "account": "Accrued liabilities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "This obligation was settled in April 2026.",
    "paragraph_id": "0001783180-26-000026:note_history:7",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_afff_lawsuit_count",
    "what_changed": "The AFFF paragraph now says the Company, KFI and others are named in 'more than 18,000' lawsuits as of June 30, 2026. The prior paragraph said 'more than 17,000' as of March 31, 2026. No change to the recorded liability is stated, and the remaining claims are still described as not estimable (notes:141).",
    "account": "Accrued liabilities / Other long-term liabilities (AFFF)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "have been named as defendants in more than 18,000 lawsuits",
    "paragraph_id": "0001783180-26-000032:notes:136",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_afff_direct_claims_court_approval_timing",
    "what_changed": "Added sentence: the process of seeking court approval for the Direct Claims Settlements with water providers will begin in Q3 2026. The settlement terms in notes:140 ($615 million over five years, KFI sale proceeds estimated at $115 million, insurance rights) change only in date, and no insurance proceeds are recorded. The Chapter 11 plan paragraph (notes:142) still reports no event after the October 6, 2025 hearing.",
    "account": "Accrued liabilities / Other long-term liabilities (AFFF settlement)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The process of seeking court approval for the Direct Claims Settlements with water providers will begin in the third quarter of 2026.",
    "paragraph_id": "0001783180-26-000032:notes:139",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_revenue_from_opening_contract_liabilities",
    "what_changed": "The contract-liability paragraph now states $407 million of six-month revenue from contract liabilities that existed on January 1, 2026. The prior paragraph stated $250 million for the three months ended March 31, 2026. The expectation that a majority of current contract liabilities will be recognized within 12 months is unchanged.",
    "account": "Contract liabilities / Net sales",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company recognized revenue of $407 million during the six months ended June 30, 2026, that related to contract liabilities as of January 1, 2026.",
    "paragraph_id": "0001783180-26-000032:notes:82",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_quarter_better_than_expected_and_organic_return",
    "what_changed": "The CEO says:\n- the quarter was stronger than expected on sales, adjusted EPS and free cash flow\n- organic sales returned to growth 'earlier than expected', led by CSA\n- residential and light commercial markets in CSA and CSE are improving\n- backlog is at record levels\nThe release headline calls results 'better than expected' (8k_2_02:13).",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Organic sales returned to growth earlier than expected, up 3%, driven by strong performance in our CSA segment.",
    "paragraph_id": "0001783180-26-000030:8k_2_02:14",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_full_year_outlook_raised",
    "what_changed": "Current against prior guidance, as stated in the outlook table (8k_2_02:48):\n- Sales: ~$23 billion; was ~$22 billion.\n- Adjusted operating profit: ~$3.5 billion; was ~$3.4 billion.\n- Adjusted EPS: ~$2.90; was ~$2.80.\n- Free cash flow: ~$2 billion; was ~$2 billion.\n- Organic: 'up ~M-HSD'; was 'flat to up LSD'.\n- Net acquisitions/divestitures: '(2%)' with ~$225 million Riello and ~$125 million NORESCO revenue headwinds; was '(1%)' with ~$250 million Riello.\nThe free cash flow figure is the same in both columns while the sales and profit outlook is raised.",
    "account": "Net sales / Adjusted operating profit",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Raises full year outlook to ~$23B sales, ~$3.5B adj. op. profit and ~$2.90 adj. EPS",
    "paragraph_id": "0001783180-26-000030:8k_2_02:11",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_noresco_exit_and_new_factory_costs_in_outlook",
    "what_changed": "New: the raised outlook includes an approximately ($0.05) adjusted EPS impact from the NORESCO exit and from 'new U.S. factory costs'. No factory is mentioned in the 10-Q text in the input.",
    "account": "Adjusted EPS (cost of products sold, NORESCO exit)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Includes ~($0.05) adj. EPS impact from NORESCO exit and new U.S. factory costs",
    "paragraph_id": "0001783180-26-000030:8k_2_02:12",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_orders_and_data_center_demand",
    "what_changed": "The release reports total company orders up ~40%, Commercial HVAC orders up ~65% and data center orders up >300%, all excluding NORESCO and Riello (8k_2_02:15). Orders are defined as commitments that 'may not be subject to penalty if cancelled' (8k_2_02:78). In the same filing period the MD&A describes CSA commercial sales as down on delivery timing (mdna:93) and, for six months, on lower end-market demand (mdna:127).",
    "account": "Net sales (orders and backlog)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Total company orders1 up ~40%; Commercial HVAC1 up ~65%; data centers up >300%",
    "paragraph_id": "0001783180-26-000030:8k_2_02:6",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_free_cash_flow_definition_versus_reconciliation_starting_line",
    "what_changed": "The release defines free cash flow as continuing operating cash flow less capital expenditures. Its free cash flow tables (8k_2_02:44, 8k_2_02:119) and headline (8k_2_02:9, 8k_2_02:45) start from the line 'Net cash flows provided by operating activities': $927 million for the quarter and $649 million for the prior-year quarter. In the release's cash flow statement (8k_2_02:93) those same figures sit on the total operating line, below separate lines for continuing operations ($888 million; $264 million) and discontinued operations ($39 million; $385 million). The reconciliation therefore starts from the total line, not the continuing line the definition names. I found this by matching labels, not by calculating; the supervisor should reconcile it.",
    "account": "Free cash flow / Net cash flows from operating activities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Free cash flow is a non-GAAP financial measure that represents net cash flows provided by continuing operating activities (a GAAP measure) less capital expenditures.",
    "paragraph_id": "0001783180-26-000030:8k_2_02:78",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "controls_audit_and_filings_officer_change_filing_body_not_in_input",
    "what_changed": "The item-code list shows an 8-K filed 2026-07-24 with Items 5.02 and 9.01 (departure or appointment of directors or officers). It was filed after the prior 10-Q. Its body is not in the input, so who changed, and whether a finance or accounting officer is involved, cannot be read. Insufficient.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "2026-07-24 0000950142-26-002161 — 5.02, 9.01",
    "paragraph_id": "input_8k.md item-code list (no paragraph id)",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_unrecognized_tax_benefit_range",
    "what_changed": "The note says a net decrease in unrecognized tax benefits of $5 million to $95 million is reasonably possible within 12 months. The income-tax note is carried whole and the change history does not cover it, so I cannot tell whether this range changed this period. Insufficient.",
    "account": "Income tax liabilities (unrecognized tax benefits)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The Company believes that it is reasonably possible that a net decrease in unrecognized tax benefits of $5 million to $95 million may occur within 12 months",
    "paragraph_id": "0001783180-26-000032:notes:98",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tax_examination_closure_timing",
    "what_changed": "The IRS is examining tax year 2022, with closure expected in 2027. The Australia Tax Office is auditing the 2021 return, including the Chubb Australia disentanglement, with closure expected in early 2027. The prior wording is not in the input, so I cannot tell whether the expected closure dates moved. Insufficient.",
    "account": "Income tax liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "including the review of the disentanglement of the Chubb Australia business, with the audit expected to close in early 2027.",
    "paragraph_id": "0001783180-26-000032:notes:97",
    "explanation": false,
    "insufficient": true
  }
]
```

## Paragraphs read and not made an item of

Each line gives the paragraph id and the reason. "Covered by" names the item that already carries the same change.

### Notes (0001783180-26-000032:notes:N)

- notes:2 — no change I can identify; the change history does not list it
- notes:6 — date rolled forward (TMA sentence; history confirms)
- notes:9 — heading
- notes:10 — no change I can identify; ASU 2024-03 still under assessment; not in the change history
- notes:13 — amounts only (inventory table)
- notes:17 — amounts only (goodwill table); CSA held-for-sale row covered by structure_and_disclosure_changes_noresco_classified_held_for_sale
- notes:20 — amounts only (intangibles table)
- notes:22 — amounts only (amortization table)
- notes:23 — heading and lead-in
- notes:24 — amounts only (short-term borrowings table replacing the March table)
- notes:25 — heading
- notes:27 — lead-in
- notes:28 — amounts only (long-term debt table)
- notes:29 — footnote marker already on the prior-period table (note_history:14); content used in liquidity_and_capital_long_term_note_interest_and_maturity_range
- notes:30 — heading
- notes:31 — date rolled forward (Revolving Credit Facility; history confirms)
- notes:32 — heading
- notes:34 — heading
- notes:35 — date rolled forward (covenant compliance; history confirms)
- notes:45 — amounts only (derivative fair value table)
- notes:49 — amounts only (long-term notes fair value table)
- notes:55 — amounts only (pension contributions table)
- notes:57 — amounts only (net periodic pension table)
- notes:61 — amounts only (stock compensation table)
- notes:64 — lead-in, wording only
- notes:65 — amounts only (warranty rollforward table)
- notes:67 — amounts only (share counts rolled forward); covered by liquidity_and_capital_share_repurchases_and_remaining_authorization
- notes:72 — lead-in with dates rolled forward
- notes:73 — amounts only (AOCI table)
- notes:74 — lead-in with dates
- notes:75 — amounts only (prior-year AOCI table)
- notes:78 — amounts only (sales by type table)
- notes:81 — amounts only (contract assets and liabilities table)
- notes:85 — period rolled forward to three and six months (history confirms)
- notes:86 — amounts only (geographic sales table)
- notes:89 — amounts only (restructuring by segment table)
- notes:92 — amounts only (restructuring reserve rollforward table)
- notes:96 — valuation-allowance method, no change I can identify
- notes:101 — amounts only (EPS table)
- notes:115 — amounts only (segment tables)
- notes:116 — amounts only (prior-year segment table)
- notes:117 — amounts only; the Riello impairment row is covered by earnings_quality_riello_impairment_in_other_income
- notes:119 — heading
- notes:120 — carried verbatim, no change (related-party boilerplate)
- notes:121 — amounts only (sales to and purchases from equity method investees)
- notes:122 — lead-in
- notes:123 — amounts only (receivables from and payables to equity method investees)
- notes:124 — carried verbatim, not in the change history (contingencies policy)
- notes:125 — heading
- notes:126 — carried verbatim, no change (environmental policy)
- notes:127 — lead-in
- notes:128 — amounts only (environmental reserves table; history confirms)
- notes:129 — carried verbatim, no change
- notes:130 — heading
- notes:131 — carried verbatim, no change (asbestos)
- notes:132 — lead-in
- notes:133 — amounts only (asbestos table; history confirms)
- notes:134 — carried verbatim, no change
- notes:135 — heading
- notes:137 — carried verbatim, no change (KFI bankruptcy)
- notes:138 — carried verbatim, no change (Settlement and Plan Support Agreement)
- notes:140 — date rolled forward (history confirms); terms referenced in the AFFF approval-timing item
- notes:141 — carried verbatim, no change
- notes:142 — carried verbatim, no change; the latest event is still the October 6, 2025 hearing
- notes:143 — heading
- notes:144 — carried verbatim; antitrust suits were already disclosed at the prior period (not in the change history)
- notes:145 — heading
- notes:146 — carried verbatim, no change
- notes:147 — carried verbatim, no change

### MD&A (0001783180-26-000032:mdna:N)

- mdna:13 — same Riello impairment and completion; covered by earnings_quality_riello_impairment_in_other_income and the Riello completion item
- mdna:17 — heading
- mdna:19 — amounts only (results table)
- mdna:21 — lead-in restating amounts
- mdna:22 — amounts only (sales components table)
- mdna:25 — lead-in restating amounts
- mdna:26 — amounts only (gross margin table)
- mdna:29 — lead-in restating amounts
- mdna:30 — amounts only (operating expenses table)
- mdna:34 — same Riello impairment; covered by earnings_quality_riello_impairment_in_other_income
- mdna:36 — lead-in restating amounts
- mdna:37 — amounts only (non-operating table)
- mdna:40 — amounts only (tax rate table)
- mdna:42 — same text as notes:94; covered by the quarter tax-rate item
- mdna:45 — amounts only; the Riello impairment row is covered by the Riello impairment item
- mdna:48 — heading
- mdna:49 — lead-in
- mdna:50 — amounts only (six-month results table)
- mdna:51 — heading
- mdna:52 — lead-in restating amounts
- mdna:53 — amounts only
- mdna:54 — covered by across_documents_csa_six_month_demand_described_both_improved_and_reduced
- mdna:55 — heading
- mdna:56 — lead-in restating amounts
- mdna:57 — amounts only
- mdna:59 — heading
- mdna:60 — lead-in restating amounts
- mdna:61 — amounts only
- mdna:63 — generic R&D statement, no amount or cause
- mdna:64 — covered by narrative_signs_of_operating_pressure_lower_joint_venture_earnings
- mdna:65 — covered by earnings_quality_riello_impairment_in_other_income
- mdna:66 — heading
- mdna:67 — lead-in restating amounts
- mdna:68 — amounts only
- mdna:69 — covered by liquidity_and_capital_interest_expense_attributed_to_commercial_paper
- mdna:70 — heading
- mdna:71 — amounts only
- mdna:72 — same content as notes:95; covered by the six-month tax-rate item
- mdna:73 — heading
- mdna:74 — non-GAAP definition boilerplate
- mdna:75 — amounts only (six-month adjusted operating profit reconciliation)
- mdna:76 — non-GAAP caution boilerplate
- mdna:77 — page number
- mdna:85 — heading
- mdna:87 — amounts only (segment table)
- mdna:89 — amounts only
- mdna:91 — lead-in restating amounts
- mdna:92 — amounts only
- mdna:94 — lead-in restating amounts
- mdna:95 — amounts only (CSA profit bridge; 'Other' covered by the CSA other-component item)
- mdna:98 — lead-in restating amounts
- mdna:99 — amounts only
- mdna:101 — lead-in restating amounts
- mdna:102 — amounts only
- mdna:103 — covered by the Europe pricing-promotions item and the CSE price/cost cross-document item
- mdna:105 — lead-in restating amounts
- mdna:106 — amounts only
- mdna:108 — lead-in restating amounts
- mdna:109 — amounts only (CSAME bridge; 'Other' covered by the land-gain item)
- mdna:112 — lead-in restating amounts
- mdna:113 — amounts only
- mdna:115 — lead-in restating amounts
- mdna:116 — amounts only
- mdna:117 — covered by narrative_signs_of_operating_pressure_truck_and_trailer_demand
- mdna:118 — page number
- mdna:119 — heading
- mdna:120 — lead-in
- mdna:121 — amounts only
- mdna:122 — lead-in
- mdna:123 — amounts only
- mdna:124 — heading
- mdna:125 — lead-in restating amounts
- mdna:126 — amounts only
- mdna:128 — lead-in restating amounts
- mdna:129 — amounts only
- mdna:130 — page number
- mdna:131 — covered by the tariffs item, the CSA other-component item and the JV earnings item
- mdna:132 — heading
- mdna:133 — lead-in restating amounts
- mdna:134 — amounts only
- mdna:135 — covered by narrative_signs_of_operating_pressure_europe_pricing_promotions
- mdna:136 — lead-in restating amounts
- mdna:137 — amounts only
- mdna:139 — heading
- mdna:140 — lead-in restating amounts
- mdna:141 — amounts only
- mdna:142 — covered by narrative_signs_of_operating_pressure_china_demand_and_price
- mdna:143 — lead-in restating amounts
- mdna:144 — amounts only
- mdna:145 — covered by the land-gain item and the JV earnings item
- mdna:146 — heading
- mdna:147 — lead-in restating amounts
- mdna:148 — amounts only
- mdna:149 — covered by the truck-and-trailer item and the six-month demand cross-document item
- mdna:150 — lead-in restating amounts
- mdna:151 — amounts only
- mdna:152 — covered by narrative_signs_of_operating_pressure_truck_and_trailer_demand
- mdna:153 — page number
- mdna:160 — amounts only (capitalization table)
- mdna:162 — same $685 million commercial paper figure as notes:26; covered by the commercial paper item
- mdna:164 — date rolled forward (credit ratings lead-in)
- mdna:167 — covered by the Riello completion item
- mdna:170 — same text as notes:70; covered by the share repurchase item
- mdna:175 — amounts only (cash flow summary table)
- mdna:177 — page number

### Item 4 (0001783180-26-000032:item_4_controls:N)

- item_4_controls:1 — heading
- item_4_controls:2 — date rolled forward; disclosure controls still concluded effective
- item_4_controls:3 — date rolled forward; still no change in internal control over financial reporting

### 8-K 0001783180-26-000030, Item 2.02 (8k_2_02:N)

- 8k_2_02:1 — exhibit file header
- 8k_2_02:2 — document label
- 8k_2_02:3 — exhibit label
- 8k_2_02:4 — release title
- 8k_2_02:5 — outlook headline; covered by results_against_expectations_full_year_outlook_raised
- 8k_2_02:7 — results headline, amounts only
- 8k_2_02:8 — results headline, amounts only
- 8k_2_02:9 — operating cash flow and free cash flow headline; covered by the free cash flow cross-document item
- 8k_2_02:10 — shareholder-returns headline; covered by the share repurchase item
- 8k_2_02:13 — 'better than expected'; covered by results_against_expectations_quarter_better_than_expected_and_organic_return
- 8k_2_02:15 — footnote on NORESCO and Riello exclusions; covered by the orders item and the Riello completion item
- 8k_2_02:16 — page number
- 8k_2_02:17 — heading
- 8k_2_02:18 — heading
- 8k_2_02:19 — amounts only (results table)
- 8k_2_02:20 — results restated, amounts only
- 8k_2_02:21 — margin drivers; covered by the tariffs and input-costs item
- 8k_2_02:22 — EPS drivers; covered by the tax-rate and share repurchase items
- 8k_2_02:23 — page number
- 8k_2_02:24 — heading
- 8k_2_02:25 — amounts only (CSA table)
- 8k_2_02:28 — heading
- 8k_2_02:29 — amounts only (CSE table)
- 8k_2_02:30 — CSE sales narrative; covered by the Europe pricing-promotions item
- 8k_2_02:32 — footnote 'Excludes NORESCO'; covered by across_documents_csa_commercial_decline_rate_and_noresco_exclusion
- 8k_2_02:33 — page number
- 8k_2_02:34 — heading
- 8k_2_02:35 — amounts only (CSAME table)
- 8k_2_02:36 — CSAME geographies; covered by the China item and the Middle East cross-document item
- 8k_2_02:38 — heading
- 8k_2_02:39 — amounts only (CST table)
- 8k_2_02:40 — covered by the truck-and-trailer item
- 8k_2_02:41 — covered by the truck-and-trailer item
- 8k_2_02:42 — page number
- 8k_2_02:43 — heading
- 8k_2_02:44 — free cash flow table; covered by the free cash flow cross-document item
- 8k_2_02:45 — free cash flow sentence; covered by the free cash flow cross-document item
- 8k_2_02:46 — page number
- 8k_2_02:47 — heading
- 8k_2_02:48 — guidance table; covered by the outlook item
- 8k_2_02:49 — divestiture status; covered by the Riello completion and Noresco items
- 8k_2_02:50 — forward non-GAAP boilerplate
- 8k_2_02:51 — guidance as-of date
- 8k_2_02:52 — heading
- 8k_2_02:53 — conference-call logistics
- 8k_2_02:54 — page number
- 8k_2_02:55 — heading only; cautionary text not carried
- 8k_2_02:56 — page number
- 8k_2_02:57 — heading
- 8k_2_02:58 — company boilerplate
- 8k_2_02:59 — tagline
- 8k_2_02:60 — release code
- 8k_2_02:61 — contact heading
- 8k_2_02:62 — contact heading
- 8k_2_02:63 — contact name
- 8k_2_02:64 — phone
- 8k_2_02:65 — email
- 8k_2_02:66 — contact heading
- 8k_2_02:67 — contact name
- 8k_2_02:68 — phone
- 8k_2_02:69 — email
- 8k_2_02:70 — page number
- 8k_2_02:71 — heading
- 8k_2_02:72 — boilerplate
- 8k_2_02:73 — heading
- 8k_2_02:74 — non-GAAP boilerplate
- 8k_2_02:75 — non-GAAP list boilerplate
- 8k_2_02:76 — non-GAAP definitions boilerplate
- 8k_2_02:77 — segment profit definition boilerplate
- 8k_2_02:79 — price/cost definition; used in the CSE price/cost cross-document item
- 8k_2_02:80 — forward non-GAAP boilerplate
- 8k_2_02:81 — page number
- 8k_2_02:82 — heading
- 8k_2_02:83 — heading
- 8k_2_02:84 — amounts only (income statement)
- 8k_2_02:85 — page number
- 8k_2_02:86 — heading
- 8k_2_02:87 — heading
- 8k_2_02:88 — amounts only (balance sheet)
- 8k_2_02:89 — page number
- 8k_2_02:90 — heading
- 8k_2_02:91 — heading
- 8k_2_02:92 — label
- 8k_2_02:93 — amounts only (cash flow statement; row labels used in the free cash flow item)
- 8k_2_02:94 — page number
- 8k_2_02:95 — heading
- 8k_2_02:96 — heading
- 8k_2_02:97 — amounts only (segment summary)
- 8k_2_02:98 — page number
- 8k_2_02:99 — heading
- 8k_2_02:100 — amounts only (quarter sales components)
- 8k_2_02:101 — amounts only (six-month sales components)
- 8k_2_02:102 — page number
- 8k_2_02:103 — heading
- 8k_2_02:104 — heading
- 8k_2_02:105 — amounts only; the Riello impairment line is covered by the Riello impairment item
- 8k_2_02:106 — amounts only
- 8k_2_02:107 — page number
- 8k_2_02:108 — heading
- 8k_2_02:109 — heading
- 8k_2_02:110 — heading
- 8k_2_02:111 — amounts only (2026 GAAP to adjusted reconciliation)
- 8k_2_02:112 — page number
- 8k_2_02:113 — heading
- 8k_2_02:114 — heading
- 8k_2_02:115 — heading
- 8k_2_02:116 — amounts only (2025 reconciliation)
- 8k_2_02:117 — page number
- 8k_2_02:118 — heading
- 8k_2_02:119 — free cash flow reconciliation; covered by the free cash flow cross-document item
- 8k_2_02:120 — heading
- 8k_2_02:121 — amounts only (net debt); referenced in the held-for-sale debt item
- 8k_2_02:122 — page number

**8-K item-code and late-filing lists:**
- The 2026-07-24 Item 5.02 filing is made an item (insufficient).
- The 2026-07-28 Item 2.02 filing is this release.
- All other listed filings predate the prior 10-Q.
- Late filings: none.

### Note change history

The history shows what is new. It is not reported as a second list; these lines say where each history entry ended up.

- note_history:1 and :8 — amounts only (environmental table, i.e. notes:128)
- note_history:2 and :9 — amounts only (asbestos table, i.e. notes:133)
- note_history:3 — covered by the AFFF lawsuit-count item
- note_history:4 — covered by the AFFF approval-timing item
- note_history:5 — date rolled forward (notes:140)
- note_history:6 (removed 'Income Taxes' heading) — covered by the TMA paragraph-removed item
- note_history:7 (removed) — itemized as the TMA paragraph-removed item
- note_history:10 — covered by the Riello completion item
- note_history:11 — date rolled forward (notes:6)
- note_history:12 and :20 — amounts only (notes:24)
- note_history:13 — covered by the commercial paper item
- note_history:14 and :19 — amounts only (notes:28)
- note_history:15 — date rolled forward (notes:31)
- note_history:16 — covered by the project financing item
- note_history:17 — date rolled forward (notes:35)
- note_history:18 and :21 (removed March short-term borrowings table) — amounts only, replaced by notes:24
- note_history:22 and :23 — amounts only (related-party tables)
- note_history:24 and :27 — amounts only (sales by type)
- note_history:25 — period rolled forward (notes:85)
- note_history:26 — amounts only (geographic sales)
- note_history:28 — amounts only (contract balances)
- note_history:29 — covered by the contract-liability revenue item
