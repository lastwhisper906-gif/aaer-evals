# report_notes_text — LOGI 10-Q 0001032975-26-000050 (quarter ended June 30, 2026)

## Scope and input check

- Read in full: input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md (release 0001032975-26-000047, filed 2026-07-28), input_prior_predictions.md.
- Diff layer compares against 0001032975-26-000011 (the 10-Q filed 2026-01-28, quarter ended December 31, 2025). Paragraphs marked `[same as prior period ...]` were not reread.
- Not in the input: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report (this is a 10-Q, and Item 4 is the only controls section). Part II Item 1 Legal Proceedings, which mdna:191 refers to, is also not in the input.
- Prior flags: none on record, so nothing carries forward.
- Forbidden-material check: there is no trend table, price, abnormal return, short interest, other-company file, prior probability or outcome window in the directory. The 8-K exhibit contains the company's own preliminary statements. These are part of the 8-K body and were read as text.
- 8-K index: since the comparator 10-Q, the only filings are 2.02/9.01 earnings filings (2026-05-05 and 2026-07-28). There is no 4.01, 4.02, 5.02 or NT filing in that window. The body of the 2026-05-05 release is not in the input. This is not an item.
- No arithmetic was done. Every direction below is what the prose implies, not a computed value.

## Items

```json
[
  {
    "id": "earnings_quality_tariff_refund_recorded_as_reduction_of_cost_of_goods_sold",
    "what_changed": "New paragraph. The note now says the company received a full $61 million refund of the IEEPA tariffs that the Supreme Court invalidated, and recorded the whole refund as a reduction of cost of goods sold in the first quarter of fiscal 2027. The prose ties the benefit to a single court ruling, so this quarter's cost of goods sold carries a one-time credit. MD&A (mdna:45) lists the tariff refund first among the gross margin drivers, and the CFO says reported results benefited from refunds (8k_2_02:17).",
    "account": "cost of goods sold",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The $61 million refund was recorded as a reduction of costs of goods sold",
    "paragraph_id": "0001032975-26-000050:notes:15",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tariff_refund_receivable_recognized_before_cash_receipt",
    "what_changed": "New sentence. The $46 million of the refund that CBP had approved but not paid by quarter end was recognized in the quarter and booked in other current assets. Part of the gain was therefore recognized before the cash came in. Management is explaining what a receivable-type balance inside other current assets consists of. The note does not say which line of other current assets in notes:47 holds it.",
    "account": "other current assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the $46 million refund approved by CBP, but not yet received, was recorded as other current assets",
    "paragraph_id": "0001032975-26-000050:notes:15",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_tariff_refund_gain_recognized_when_realized_or_realizable",
    "what_changed": "New policy sentence: tariff refunds are recognized when the gain is realized or realizable. It sits in the same note as the policy paragraph (notes:9), which still says there were no material changes in significant accounting policies. The policy covers any later refund, including one for the temporary tariffs that a court invalidated but that stayed in effect pending appeal (notes:16).",
    "account": "cost of goods sold",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company recognizes tariff refunds when the gain is realized or realizable.",
    "paragraph_id": "0001032975-26-000050:notes:15",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tariff_refund_cash_received_after_quarter_end",
    "what_changed": "New in MD&A: of the $61 million of tariff refunds recognized in the first quarter, $15 million was received in cash within the quarter and $46 million after quarter end. This is a subsequent event: the cash for the $46 million arrives in the second quarter, and the other current asset recorded at June 30 converts to cash.",
    "account": "cash and cash equivalents",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "of which $15 million was received in cash within the quarter and $46 million was received subsequent to quarter end",
    "paragraph_id": "0001032975-26-000050:mdna:111",
    "explanation": false
  },
  {
    "id": "earnings_quality_interest_income_on_tariff_refunds",
    "what_changed": "New driver: MD&A attributes the increase in interest income mainly to interest on the IEEPA tariff refunds. That source is tied to the one-time refund, not to the cash balances that usually drive this line.",
    "account": "interest income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by interest income associated with IEEPA tariff refunds",
    "paragraph_id": "0001032975-26-000050:mdna:133",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_results_include_tariff_refunds",
    "what_changed": "The release says GAAP and non-GAAP operating income include the $61 million of tariff refunds; 8k_2_02:11 says the same for gross margin. The non-GAAP exclusion list (8k_2_02:31) does not name tariff refunds, so the one-time refund stays inside the non-GAAP results. The CFO quote (8k_2_02:17) separately gives a non-GAAP operating income growth rate that excludes the refunds.",
    "account": "operating income (GAAP and non-GAAP)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These numbers include $61 million in tariff refunds.",
    "paragraph_id": "0001032975-26-000047:8k_2_02:12",
    "explanation": false
  },
  {
    "id": "earnings_quality_full_year_margin_expectation_helped_by_tariff_refunds",
    "what_changed": "The release expects full-year non-GAAP operating margin to track near the high end of the long-term target range. It says this is helped by operating performance and by this quarter's tariff refunds, so part of the full-year margin expectation rests on the one-time refund.",
    "account": "non-GAAP operating margin",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "helped by strong operating performance and this quarter",
    "paragraph_id": "0001032975-26-000047:8k_2_02:26",
    "explanation": false
  },
  {
    "id": "results_against_expectations_operating_income_outlook_exceeded",
    "what_changed": "The CFO says the first quarter beat the company's operating income outlook, crediting gross margin resilience. He also says non-GAAP operating income grew 14 percent year over year excluding the refunds. The prior outlook itself (in the 2026-05-05 release) is not in the input, so this claim rests on the release alone.",
    "account": "operating income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Strong gross margin resilience allowed us to exceed our operating income outlook",
    "paragraph_id": "0001032975-26-000047:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "results_against_expectations_tenth_consecutive_quarter_of_growth_claim",
    "what_changed": "The release headline says this is the tenth consecutive quarter of growth. That is a claim about the filed history, and checking it falls to the numbers reader.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Strong First Quarter Marks Tenth Consecutive Quarter of Growth",
    "paragraph_id": "0001032975-26-000047:8k_2_02:8",
    "explanation": false
  },
  {
    "id": "results_against_expectations_second_quarter_growth_despite_supplier_headwind",
    "what_changed": "New outlook statement. The midpoint of second-quarter guidance (sales growth of 0 to 3 percent, per 8k_2_02:20) assumes growth even though the supplier incident is expected to cost about $20 million of net sales in the quarter.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The midpoint of the Q2 outlook contemplates growth despite a Q2 headwind of approximately $20 million in net sales caused by this supplier incident.",
    "paragraph_id": "0001032975-26-000047:8k_2_02:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_second_quarter_operating_income_outlook_range",
    "what_changed": "New second-quarter outlook: non-GAAP operating income of $185 to $210 million, on sales of $1,185 to $1,220 million. The release gives no GAAP reconciliation for it (8k_2_02:32). Where this range sits against the first quarter is for the numbers reader.",
    "account": "non-GAAP operating income",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "$185 - $210 million",
    "paragraph_id": "0001032975-26-000047:8k_2_02:20",
    "explanation": false
  },
  {
    "id": "results_against_expectations_third_quarter_supplier_incident_sales_impact",
    "what_changed": "New estimate, based on limited available information: the supplier incident could cut third-quarter net sales by up to $200 million. The incident is expected to be largely resolved by the fourth quarter, with little to no impact there. Per mdna:41 the third quarter is the seasonal sales peak. The release is the only document that quantifies this.",
    "account": "net sales",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "the negative impact of the supplier incident is estimated to be up to $200 million in net sales",
    "paragraph_id": "0001032975-26-000047:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "across_documents_supplier_incident_quantified_only_in_earnings_release",
    "what_changed": "The release quantifies the supplier incident (about $20 million of second-quarter net sales, up to $200 million in the third quarter, largely resolved by the fourth quarter) and says mitigation plans are under way. The 10-Q (notes:17, mdna:29, mdna:6) describes the closure and an impact on meeting demand in the second and third quarters. It gives no amount and says nothing about mitigation plans or when the incident will be resolved.",
    "account": "net sales",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The Company is working on multiple mitigation plans.",
    "paragraph_id": "0001032975-26-000047:8k_2_02:23",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_semiconductor_supplier_facility_closure",
    "what_changed": "New: in late June 2026 a semiconductor component supplier had a serious incident at its manufacturing facilities and closed temporarily. The company expects this to affect its ability to meet demand for certain products in the second and third quarters of fiscal 2027. The note does not say whether inventory, purchase commitments or reserves were affected.",
    "account": "net sales",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The Company currently expects this facility closure will impact its ability to effectively meet demand for certain products in the second and third quarters of fiscal year 2027.",
    "paragraph_id": "0001032975-26-000050:notes:17",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_component_shortages_now_experienced",
    "what_changed": "Changed from the prior quarter. The removed prior paragraph (0001032975-26-000011:note_history:15) said the company may also be affected by demand for memory chips and other components, leading to rising prices. The note now says the company has been affected, widens the scope to electronic components including semiconductor chips, and adds shortages alongside rising prices.",
    "account": "cost of goods sold",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The Company has also been affected by the increases in demand for electronic components, including semiconductor chips, caused by the build out of new AI technologies and data centers, leading to shortages and rising prices for such components",
    "paragraph_id": "0001032975-26-000050:notes:17",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_video_collaboration_component_supplier_language_removed",
    "what_changed": "Removed: the prior quarter's statement that suppliers were moving away from supplying certain components used in some Video Collaboration products. The references to low economic growth in certain regions and to changes in fiscal policies were removed with it. The replacement paragraphs (notes:14 to notes:17) do not repeat the Video Collaboration supplier point and do not say whether it was resolved.",
    "account": "net sales (Video Collaboration)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "suppliers transitioning away from supplying certain components utilized in the manufacturing",
    "paragraph_id": "0001032975-26-000011:note_history:15",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_paragraph_removed",
    "what_changed": "Removed: the paragraph describing ASU 2023-09 (income tax disclosures) as still under evaluation. The quarterly note does not say the standard was adopted. The removed text says it applies to annual periods beginning after December 15, 2024. No effect on any account is stated.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "ASU 2023-09 requires additional disclosures related to rate reconciliation, income taxes paid, and other disclosures.",
    "paragraph_id": "0001032975-26-000011:note_history:16",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_middle_east_conflict_and_energy_prices",
    "what_changed": "New paragraph. The list of conditions affecting the business now names component availability, volatile energy prices and the armed conflicts in the Middle East. The removed prior paragraph named low economic growth in certain regions, changes in fiscal policies and geopolitical conflicts in general.",
    "account": "net sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "volatile energy prices and geopolitical tensions, including the armed conflicts in the Middle East",
    "paragraph_id": "0001032975-26-000050:notes:14",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_emea_sales_hit_by_middle_east_conflict",
    "what_changed": "New sentence: MD&A says the conflict in the Middle East and an overall market decline hurt EMEA sales, alongside lower Keyboards & Combos, Webcams and Headsets sales in the region.",
    "account": "net sales (EMEA)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Sales in the EMEA region were negatively impacted by the conflict in the Middle East and an overall market decline.",
    "paragraph_id": "0001032975-26-000050:mdna:74",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_new_tariffs_after_temporary_tariffs_expired",
    "what_changed": "New: when the temporary tariffs expired, new US tariffs under Section 301 took effect on July 24, 2026, after quarter end. The note says tariff policies have had, and may continue to have, a significant impact on results. This is a new tariff cost from the second quarter onward, following the one-time refund of the invalidated tariffs.",
    "account": "cost of goods sold",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "In July 2026, the U.S. government announced new tariffs under Section 301 of U.S. trade laws which became effective on July 24, 2026 when the temporary tariffs expired.",
    "paragraph_id": "0001032975-26-000050:notes:16",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_temporary_tariffs_invalidated_pending_appeal",
    "what_changed": "New: the US Court of International Trade invalidated the temporary 150-day tariffs that began February 24, 2026, but they stayed in effect pending appeal. The note does not say whether the company paid them, claimed a refund or recognized anything. The new policy in notes:15 (refunds recognized when realized or realizable) would govern any outcome.",
    "account": "cost of goods sold",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "which were subsequently invalidated by the U.S. Court of International Trade, but remained in effect pending appeal",
    "paragraph_id": "0001032975-26-000050:notes:16",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_credit_loss_practical_expedient_adopted",
    "what_changed": "Changed from evaluating to adopted. In the first quarter of fiscal 2027 the company adopted ASU 2025-05. This practical expedient lets it assume that conditions at the balance sheet date persist over the remaining life of current receivables when estimating credit losses. The note says adoption had no material impact.",
    "account": "accounts receivable, net (allowance for credit losses)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company adopted ASU 2025-05 in the first quarter of fiscal year 2027",
    "paragraph_id": "0001032975-26-000050:notes:20",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_effective_tax_rate_share_based_compensation_benefits",
    "what_changed": "The change in the effective tax rate is attributed to the mix of income and losses across jurisdictions and to higher tax benefits from share-based compensation. The second cause is a discrete item linked to equity awards, not to operations.",
    "account": "effective income tax rate / provision for income taxes",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "higher tax benefits from share-based compensation",
    "paragraph_id": "0001032975-26-000050:notes:41",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_obbba_provisions_effective_impact_de_minimis",
    "what_changed": "The note now says the OBBBA provisions (domestic R&D expensing, bonus depreciation, modified international frameworks) apply to the company from fiscal 2027. It expects the final impact for fiscal 2027 to be de minimis and not material to the statements or the tax rate.",
    "account": "provision for income taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the final impact of the OBBBA is expected to be de minimis for fiscal year 2027",
    "paragraph_id": "0001032975-26-000050:notes:42",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_pillar_two_new_safe_harbor_top_up_tax_de_minimis",
    "what_changed": "New assessment against the newly released OECD Administrative Guidance package, which adds a new permanent safe harbor and a one-year extension of the transitional CbCR safe harbor. Most jurisdictions are expected to keep qualifying. Fiscal 2027 top-up tax in the rest is expected to be de minimis, and no material change in the Pillar Two liability is expected.",
    "account": "provision for income taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the broader guidance introduces a new permanent safe harbor and a one-year extension of the transitional Country-by-Country Reporting",
    "paragraph_id": "0001032975-26-000050:notes:43",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_prior_share_repurchase_program_completed",
    "what_changed": "New: the 2023 share repurchase program, raised to $1.6 billion in March 2025, was completed in May 2026.",
    "account": "shares in treasury, at cost",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The 2023 share repurchase program was completed in May 2026.",
    "paragraph_id": "0001032975-26-000050:notes:100",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_completed_repurchase_program_shows_no_quarter_activity",
    "what_changed": "The note says the 2023 program was completed in May 2026, which is inside this quarter. Yet the repurchase table shows a dash for both shares and cost under the 2023 program for the three months ended June 30, 2026. The prose does not say how the program was completed with no repurchases recorded in the quarter. Whether this ties to the cash flow line for share purchases is for the numbers reader.",
    "account": "shares in treasury, at cost",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "2023 Share Repurchase Program:",
    "paragraph_id": "0001032975-26-000050:notes:104",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_new_share_repurchase_program_effective",
    "what_changed": "New program, approved in March 2026: up to $1.4 billion or 16,078,446 shares over three years. It took effect on May 8, 2026 after Swiss Takeover Board approval, and $1.3 billion was available at June 30, 2026. The quarter's repurchases under it were for cancellation (mdna:175, mdna:176).",
    "account": "shares in treasury, at cost",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The program became effective on May 8, 2026, following approval from the Swiss Takeover Board.",
    "paragraph_id": "0001032975-26-000050:notes:102",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_dividend_recommended_for_completed_fiscal_year",
    "what_changed": "New: in May 2026 the Board recommended a fiscal 2026 dividend of CHF 1.36 per share. That is about CHF 195.2 million in aggregate, or about $243.9 million at the March 31, 2026 rate. The dividend is typically paid after the AGM held in September (mdna:41). The paragraph also states the prior year's paid dividend but does not describe the change.",
    "account": "cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "In May 2026, the Board of Directors recommended that we pay cash dividends for fiscal year 2026 of CHF 1.36 per share",
    "paragraph_id": "0001032975-26-000050:mdna:173",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_working_capital_increase_from_receivables_and_other_current_assets",
    "what_changed": "MD&A attributes the increase in working capital at June 30, 2026 mainly to higher accounts receivable and other current assets, partly offset by higher accounts payable. MD&A does not mention here that other current assets include the $46 million tariff refund receivable described in notes:15.",
    "account": "working capital",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily driven by an increase in accounts receivable and other current assets, partially offset by an increase in accounts payable.",
    "paragraph_id": "0001032975-26-000050:mdna:150",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_attributed_to_higher_sales_and_collection_timing",
    "what_changed": "MD&A explains the quarter's increase in accounts receivable, net, as driven mainly by higher sales and by the timing of sales and collections within the quarter.",
    "account": "accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in accounts receivable, net, was primarily driven by higher sales as well as timing of sales and collections within the quarter.",
    "paragraph_id": "0001032975-26-000050:mdna:167",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_payables_increase_from_inventory_purchases_and_timing",
    "what_changed": "MD&A explains the increase in accounts payable as driven by higher inventory purchases to match demand and by the timing of purchases in the quarter.",
    "account": "accounts payable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in accounts payable was driven by higher inventory purchases to align with demand, as well as the timing of purchases during the quarter.",
    "paragraph_id": "0001032975-26-000050:mdna:167",
    "explanation": false
  },
  {
    "id": "earnings_quality_days_sales_outstanding_attributed_to_collection_timing",
    "what_changed": "MD&A says DSO fell by one day and attributes this mainly to the timing of sales and collections within the quarter. It gives the same timing cause for the increase in receivables (mdna:167).",
    "account": "accounts receivable, net (DSO)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to timing of sales and collections within the quarter",
    "paragraph_id": "0001032975-26-000050:mdna:160",
    "explanation": true
  },
  {
    "id": "articulation_and_the_filed_history_payables_days_raised_by_tariff_refund_cost_reduction",
    "what_changed": "MD&A says DPO rose and attributes this mainly to the tariff refund lowering cost of goods sold, together with higher inventory purchases to match improved demand. The first cause is an effect of the one-time refund on how the metric is measured, not a change in payment behavior.",
    "account": "accounts payable (DPO)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to the reduction in cost of goods sold resulting from refunds of IEEPA tariffs and higher inventory purchases to align with improved demand",
    "paragraph_id": "0001032975-26-000050:mdna:161",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_inventory_turnover_lowered_by_tariff_refund",
    "what_changed": "MD&A says inventory turnover fell and attributes this mainly to the tariff refund lowering cost of goods sold, not to any change in inventory. Management explains the inventory metric through the one-time refund.",
    "account": "inventories (inventory turnover)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to the reduction in cost of goods sold resulting from refunds of IEEPA tariffs.",
    "paragraph_id": "0001032975-26-000050:mdna:162",
    "explanation": true
  },
  {
    "id": "revenue_recognition_strategic_promotions_offset_gross_margin",
    "what_changed": "Among the quarter's gross margin drivers, MD&A names spending on strategic promotions as a partial offset. The prose does not say where promotions are recorded. The related balances in the notes are the allowances for pricing and customer incentive programs (notes:47) and accrued customer marketing, pricing and incentive programs (notes:49).",
    "account": "allowances and accruals for pricing, promotion and customer incentive programs",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by investment in strategic promotions",
    "paragraph_id": "0001032975-26-000050:mdna:45",
    "explanation": false
  },
  {
    "id": "results_against_expectations_sales_growth_aided_by_currency",
    "what_changed": "MD&A attributes the quarter's 7 percent sales increase to Gaming, Pointing Devices and Video Collaboration and to favorable currency movements. It gives constant-currency growth of 5 percent (mdna:65), so the prose credits part of reported growth to currency.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "as well as favorable changes in foreign currency exchange rates",
    "paragraph_id": "0001032975-26-000050:mdna:43",
    "explanation": false
  },
  {
    "id": "results_against_expectations_tablet_accessories_prior_year_education_deal",
    "what_changed": "New cause: MD&A attributes the Tablet Accessories decline in Asia Pacific mainly to a large education deal in the prior-year quarter, which makes the comparison base non-recurring.",
    "account": "net sales (Tablet Accessories)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decline in Asia Pacific was primarily due to a large education deal in the prior year.",
    "paragraph_id": "0001032975-26-000050:mdna:100",
    "explanation": false
  },
  {
    "id": "results_against_expectations_pointing_devices_premium_mix_shift",
    "what_changed": "MD&A attributes Pointing Devices growth to wireless mice, particularly MX Master 4, and to a continued shift in mix toward premium products. This fits the favorable product mix listed among the gross margin drivers (mdna:45).",
    "account": "net sales (Pointing Devices)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "A continued mix shift to premium products in our portfolio contributed to sales growth in this category.",
    "paragraph_id": "0001032975-26-000050:mdna:90",
    "explanation": false
  },
  {
    "id": "earnings_quality_intangible_amortization_falling_on_full_amortization",
    "what_changed": "MD&A attributes the decrease in amortization of intangible assets and acquisition-related costs to certain intangible assets becoming fully amortized.",
    "account": "amortization of intangible assets",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "driven by full amortization of certain intangible assets",
    "paragraph_id": "0001032975-26-000050:mdna:127",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_plan_substantially_completed",
    "what_changed": "MD&A now says the restructuring plan started in the fourth quarter of fiscal 2025 was substantially completed in fiscal 2026. This quarter's charges are leftover costs of that plan.",
    "account": "restructuring charges, net",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "which was substantially completed in fiscal 2026",
    "paragraph_id": "0001032975-26-000050:mdna:129",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_forward_looking_bullet_for_supplier_incident",
    "what_changed": "New bullet in the forward-looking statements: the impact of the incident at a semiconductor supplier's manufacturing facilities is now listed as a factor that could make results differ.",
    "account": "net sales",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The impact of the incident in the manufacturing facilities of one of our semiconductor suppliers",
    "paragraph_id": "0001032975-26-000050:mdna:6",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_inventory_managed_to_component_availability",
    "what_changed": "The mitigation list is carried as changed. It names raising prices on certain products and managing inventory levels to match demand and component availability. The prior wording is not in the input, so which clause is new cannot be confirmed. Linking inventory levels to component availability matches the new shortage and supplier-incident language in notes:17.",
    "account": "inventories",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "managing inventory levels to align with demand and component availability",
    "paragraph_id": "0001032975-26-000050:mdna:38",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_legal_officer_trading_plan",
    "what_changed": "New: on June 12, 2026 the Chief Legal Officer adopted a Rule 10b5-1 plan to sell up to 16,265 shares acquired under equity plans. Sales may start on September 11, 2026, and the plan ends June 11, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Samantha Harnett, our Chief Legal Officer, adopted a Rule 10b5-1 trading arrangement providing for the sale of an aggregate of up to 16,265 shares",
    "paragraph_id": "0001032975-26-000050:notes:130",
    "explanation": false
  },
  {
    "id": "results_against_expectations_demand_momentum_without_full_year_outlook",
    "what_changed": "The release gives no formal full-year fiscal 2027 outlook. It says demand momentum from the first quarter should carry through the rest of the year, and the next paragraph says the supplier incident is likely to limit the company's ability to meet that demand.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "While Logitech is not issuing a formal full-year FY27 outlook, demand momentum from Q1 is expected to carry into the remainder of the year.",
    "paragraph_id": "0001032975-26-000047:8k_2_02:22",
    "explanation": false
  },
  {
    "id": "across_documents_share_repurchase_amounts_stated_on_different_bases",
    "what_changed": "The release gives the cash returned to shareholders through share repurchases. The 10-Q gives the aggregate cost of repurchases under the 2026 program (mdna:175, mdna:176, notes:104), part of which was unpaid at quarter end (notes:106), and the cash flow statement shows a separate line for purchases of registered shares. The documents state repurchases on different bases, and reconciling them is for the numbers reader.",
    "account": "shares in treasury, at cost",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company returned $114 million of cash to shareholders through share repurchases.",
    "paragraph_id": "0001032975-26-000047:8k_2_02:15",
    "explanation": false
  }
]
```

## Paragraphs carried as text and not itemized

`insufficient` marks a paragraph that is carried as changed but whose prior wording is not in the input, so no change in substance can be identified.

### Notes
- 0001032975-26-000050:notes:6 — date rolled forward (the 10-K reference and its filing date)
- 0001032975-26-000050:notes:7 — date rolled forward (period names, per change history)
- 0001032975-26-000050:notes:9 — date rolled forward; still says no material policy change (the tariff refund policy is itemized at notes:15)
- 0001032975-26-000050:notes:18 — wording only; trade policy and memory supply wording moved into notes:15 to notes:17, which are itemized
- 0001032975-26-000050:notes:19 — new heading only
- 0001032975-26-000050:notes:22 — paragraph split; change history shows the text is identical
- 0001032975-26-000050:notes:23 — continuation of the split paragraph; text identical
- 0001032975-26-000050:notes:24 — not in change history; standard still pending and under evaluation, nothing for any account
- 0001032975-26-000050:notes:26 — table caption, date rolled forward
- 0001032975-26-000050:notes:27 — EPS table, amounts only
- 0001032975-26-000050:notes:28 — antidilutive share counts, amounts only
- 0001032975-26-000050:notes:31 — date rolled forward; plan list
- 0001032975-26-000050:notes:32 — table caption, date rolled forward
- 0001032975-26-000050:notes:33 — share-based compensation table, amounts only
- 0001032975-26-000050:notes:35 — share-based compensation capitalized in inventory, amounts only
- 0001032975-26-000050:notes:37 — pension cost, amounts only
- 0001032975-26-000050:notes:40 — tax provision and rate, amounts only
- 0001032975-26-000050:notes:44 — continuation of notes:43, itemized there
- 0001032975-26-000050:notes:47 — balance sheet components table, amounts only
- 0001032975-26-000050:notes:49 — accrued and other liabilities table, amounts only
- 0001032975-26-000050:notes:57 — fair value hierarchy table, amounts only
- 0001032975-26-000050:notes:59 — deferred compensation securities, amounts only
- 0001032975-26-000050:notes:61 — equity method carrying value, amounts only; no-impairment statement with date rolled forward
- 0001032975-26-000050:notes:64 — investments without readily determinable fair value, amounts only; no-impairment statement with date rolled forward
- 0001032975-26-000050:notes:65 — no impairment of non-financial assets, date rolled forward
- 0001032975-26-000050:notes:67 — derivative presentation, date rolled forward
- 0001032975-26-000050:notes:70 — hedge notionals and AOCI reclassification, amounts only
- 0001032975-26-000050:notes:71 — table caption, date rolled forward
- 0001032975-26-000050:notes:72 — cash flow hedge table, amounts only
- 0001032975-26-000050:notes:74 — balance sheet hedge notionals, amounts only
- 0001032975-26-000050:notes:76 — no triggering events, date rolled forward
- 0001032975-26-000050:notes:78 — goodwill rollforward, amounts only
- 0001032975-26-000050:notes:80 — intangible assets table, amounts only
- 0001032975-26-000050:notes:81 — heading
- 0001032975-26-000050:notes:82 — Credit Agreement terms, not in change history, no new term
- 0001032975-26-000050:notes:83 — paragraph split of unchanged covenant and pricing text
- 0001032975-26-000050:notes:84 — date rolled forward; lines of credit and bank guarantees, amounts only
- 0001032975-26-000050:notes:85 — heading
- 0001032975-26-000050:notes:86 — heading
- 0001032975-26-000050:notes:87 — table caption, date rolled forward (three and nine months to three months)
- 0001032975-26-000050:notes:88 — warranty rollforward, amounts only
- 0001032975-26-000050:notes:89 — heading
- 0001032975-26-000050:notes:90 — date rolled forward, per change history
- 0001032975-26-000050:notes:91 — not in change history; director and officer indemnity unchanged in substance
- 0001032975-26-000050:notes:92 — heading
- 0001032975-26-000050:notes:93 — not in change history; generic ordinary-course litigation language, no matter named
- 0001032975-26-000050:notes:95 — share capital and treasury share counts, amounts only
- 0001032975-26-000050:notes:99 — heading
- 0001032975-26-000050:notes:101 — heading
- 0001032975-26-000050:notes:103 — table caption, date rolled forward
- 0001032975-26-000050:notes:106 — unpaid repurchase cost, amounts only
- 0001032975-26-000050:notes:107 — Swiss treasury share limit and counts, amounts only
- 0001032975-26-000050:notes:108 — repurchase mechanics boilerplate, no change visible
- 0001032975-26-000050:notes:111 — AOCI table, amounts only
- 0001032975-26-000050:notes:114 — table caption
- 0001032975-26-000050:notes:115 — segment expense table, amounts only
- 0001032975-26-000050:notes:118 — table caption
- 0001032975-26-000050:notes:119 — sales by category table, amounts only
- 0001032975-26-000050:notes:122 — table caption
- 0001032975-26-000050:notes:123 — sales by region table, amounts only
- 0001032975-26-000050:notes:124 — insufficient: countries at 10 percent or more stated for both periods, prior wording not in input
- 0001032975-26-000050:notes:125 — Switzerland share of sales, amounts only
- 0001032975-26-000050:notes:126 — insufficient: number of customers at 10 percent or more stated for both periods, prior wording not in input
- 0001032975-26-000050:notes:128 — long-lived assets by region table, amounts only
- 0001032975-26-000050:notes:129 — long-lived assets by country, amounts only

### MD&A
- 0001032975-26-000050:mdna:4 — insufficient: tariff bullet in the forward-looking statements, prior wording not in input; tariff substance itemized at notes:16
- 0001032975-26-000050:mdna:12 — insufficient: tax bullet in the forward-looking statements, prior wording not in input
- 0001032975-26-000050:mdna:13 — insufficient: indemnification and legal bullet in the forward-looking statements, prior wording not in input
- 0001032975-26-000050:mdna:14 — date rolled forward (fiscal year 2027)
- 0001032975-26-000050:mdna:21 — wording only, company description
- 0001032975-26-000050:mdna:26 — duplicate of notes:14, itemized there
- 0001032975-26-000050:mdna:27 — duplicate of notes:15 without the balance sheet and policy sentences; itemized at notes:15 and mdna:111
- 0001032975-26-000050:mdna:28 — duplicate of notes:16, itemized there
- 0001032975-26-000050:mdna:29 — duplicate of notes:17, itemized there
- 0001032975-26-000050:mdna:30 — duplicate of notes:18, wording only
- 0001032975-26-000050:mdna:34 — insufficient: AI trend narrative, nothing for any account
- 0001032975-26-000050:mdna:35 — insufficient: flexible-work narrative, nothing for any account
- 0001032975-26-000050:mdna:36 — insufficient: gaming trend narrative, nothing for any account
- 0001032975-26-000050:mdna:37 — same substance as notes:14 and notes:17 (component supply, energy prices), itemized there
- 0001032975-26-000050:mdna:41 — insufficient: seasonality paragraph, no change in substance visible
- 0001032975-26-000050:mdna:44 — regional growth rates, amounts only (EMEA cause itemized at mdna:74)
- 0001032975-26-000050:mdna:46 — operating expense summary, duplicate of mdna:115
- 0001032975-26-000050:mdna:47 — tax provision, amounts only
- 0001032975-26-000050:mdna:48 — net income, amounts only
- 0001032975-26-000050:mdna:53 — insufficient: list of critical estimates, prior wording not in input
- 0001032975-26-000050:mdna:54 — date rolled forward
- 0001032975-26-000050:mdna:56 — wording only ("adopted and to be adopted"), reflects the ASU adoption itemized at notes:20
- 0001032975-26-000050:mdna:64 — duplicate of mdna:43
- 0001032975-26-000050:mdna:65 — continuation of mdna:64, constant-currency rate, amounts only
- 0001032975-26-000050:mdna:67 — share of non-US-dollar sales, amounts only
- 0001032975-26-000050:mdna:69 — table caption
- 0001032975-26-000050:mdna:70 — regional growth table, amounts only
- 0001032975-26-000050:mdna:72 — regional drivers for the quarter, categories named only
- 0001032975-26-000050:mdna:76 — regional drivers for the quarter, categories named only
- 0001032975-26-000050:mdna:78 — table caption
- 0001032975-26-000050:mdna:79 — sales by category table, amounts only
- 0001032975-26-000050:mdna:83 — insufficient: Gaming category description carried as changed; cannot tell whether what the category contains changed
- 0001032975-26-000050:mdna:84 — category drivers for the quarter (named product launch), amounts only
- 0001032975-26-000050:mdna:87 — category drivers for the quarter, amounts only
- 0001032975-26-000050:mdna:89 — insufficient: Pointing Devices category description carried as changed
- 0001032975-26-000050:mdna:93 — category drivers for the quarter, amounts only
- 0001032975-26-000050:mdna:94 — page number
- 0001032975-26-000050:mdna:96 — insufficient: Webcams category description carried as changed
- 0001032975-26-000050:mdna:97 — category drivers for the quarter, amounts only
- 0001032975-26-000050:mdna:102 — insufficient: Headsets category description carried as changed
- 0001032975-26-000050:mdna:103 — category drivers for the quarter, amounts only
- 0001032975-26-000050:mdna:106 — category drivers for the quarter, amounts only
- 0001032975-26-000050:mdna:108 — table caption
- 0001032975-26-000050:mdna:109 — gross profit table, amounts only
- 0001032975-26-000050:mdna:113 — table caption
- 0001032975-26-000050:mdna:114 — operating expense table, amounts only
- 0001032975-26-000050:mdna:115 — operating expense drivers for the quarter, ordinary
- 0001032975-26-000050:mdna:117 — insufficient: marketing and selling definition, prior wording not in input
- 0001032975-26-000050:mdna:118 — marketing and selling expense for the quarter, amount and ordinary driver only
- 0001032975-26-000050:mdna:121 — research and development expense for the quarter, amount and ordinary driver only
- 0001032975-26-000050:mdna:124 — general and administrative expense for the quarter, flat
- 0001032975-26-000050:mdna:131 — table caption
- 0001032975-26-000050:mdna:132 — interest income table, amounts only
- 0001032975-26-000050:mdna:135 — table caption
- 0001032975-26-000050:mdna:136 — other income table, amounts only
- 0001032975-26-000050:mdna:137 — deferred compensation gain from market performance, ordinary
- 0001032975-26-000050:mdna:138 — exchange loss for the quarter, currencies named, ordinary
- 0001032975-26-000050:mdna:139 — investment gain or loss not material, date rolled forward
- 0001032975-26-000050:mdna:140 — pension income flat, ordinary
- 0001032975-26-000050:mdna:142 — table caption
- 0001032975-26-000050:mdna:143 — tax table, amounts only
- 0001032975-26-000050:mdna:144 — duplicate of notes:41, itemized there
- 0001032975-26-000050:mdna:145 — duplicate of notes:42, itemized there
- 0001032975-26-000050:mdna:146 — duplicate of notes:43 and notes:44, itemized there
- 0001032975-26-000050:mdna:149 — cash balance and where it is held, amounts only
- 0001032975-26-000050:mdna:151 — duplicate of notes:82, no new term
- 0001032975-26-000050:mdna:152 — duplicate of notes:83 and notes:84, date rolled forward
- 0001032975-26-000050:mdna:153 — lines of credit and guarantees, amounts only
- 0001032975-26-000050:mdna:154 — heading
- 0001032975-26-000050:mdna:155 — table caption
- 0001032975-26-000050:mdna:156 — working capital metrics table, amounts only
- 0001032975-26-000050:mdna:164 — heading
- 0001032975-26-000050:mdna:166 — cash flow summary table, amounts only
- 0001032975-26-000050:mdna:168 — investing cash flow, amounts only
- 0001032975-26-000050:mdna:169 — financing cash flow, amounts only
- 0001032975-26-000050:mdna:170 — exchange rate effect not material, ordinary
- 0001032975-26-000050:mdna:174 — duplicate of notes:100, itemized there
- 0001032975-26-000050:mdna:175 — duplicate of notes:102 plus quarter repurchase amounts
- 0001032975-26-000050:mdna:176 — continuation; amounts only (duplicates notes:102 and notes:106)
- 0001032975-26-000050:mdna:177 — duplicate of notes:107
- 0001032975-26-000050:mdna:178 — insufficient: repurchase method paragraph, no change in substance visible
- 0001032975-26-000050:mdna:180 — heading
- 0001032975-26-000050:mdna:181 — says no material change to obligations, date rolled forward
- 0001032975-26-000050:mdna:183 — inventory purchase commitments and loss liability, amounts only
- 0001032975-26-000050:mdna:184 — capital expenditure commitments, amounts only
- 0001032975-26-000050:mdna:186 — date rolled forward
- 0001032975-26-000050:mdna:188 — duplicate of notes:90, date rolled forward
- 0001032975-26-000050:mdna:190 — heading
- 0001032975-26-000050:mdna:191 — date rolled forward; cross-reference to Part II Item 1, which is not in input
- 0001032975-26-000050:mdna:192 — page number

### Item 4 controls
- 0001032975-26-000050:item_4_controls:1 — heading
- 0001032975-26-000050:item_4_controls:2 — heading
- 0001032975-26-000050:item_4_controls:3 — disclosure controls still concluded effective, no change in substance
- 0001032975-26-000050:item_4_controls:4 — heading
- 0001032975-26-000050:item_4_controls:5 — definition boilerplate
- 0001032975-26-000050:item_4_controls:6 — heading
- 0001032975-26-000050:item_4_controls:7 — limitations boilerplate
- 0001032975-26-000050:item_4_controls:8 — heading
- 0001032975-26-000050:item_4_controls:9 — no change in internal control, date rolled forward
- 0001032975-26-000050:item_4_controls:10 — page number

### 8-K item 2.02 (no earlier release text in input; boilerplate judged on content)
- 0001032975-26-000047:8k_2_02:1 — exhibit header
- 0001032975-26-000047:8k_2_02:2 — document label
- 0001032975-26-000047:8k_2_02:3 — exhibit label
- 0001032975-26-000047:8k_2_02:4 — contacts heading
- 0001032975-26-000047:8k_2_02:5 — contact name
- 0001032975-26-000047:8k_2_02:6 — contact name
- 0001032975-26-000047:8k_2_02:7 — release title
- 0001032975-26-000047:8k_2_02:9 — dateline
- 0001032975-26-000047:8k_2_02:10 — sales and growth rates, amounts only (duplicates mdna:43 and mdna:65)
- 0001032975-26-000047:8k_2_02:11 — gross margin amounts; its refund statement is itemized at 8k_2_02:12
- 0001032975-26-000047:8k_2_02:13 — EPS, amounts only
- 0001032975-26-000047:8k_2_02:14 — operating cash flow and cash balance, amounts only
- 0001032975-26-000047:8k_2_02:16 — CEO commentary; drivers repeat MD&A (mdna:90, mdna:118)
- 0001032975-26-000047:8k_2_02:18 — heading
- 0001032975-26-000047:8k_2_02:19 — outlook lead-in
- 0001032975-26-000047:8k_2_02:21 — heading
- 0001032975-26-000047:8k_2_02:27 — heading
- 0001032975-26-000047:8k_2_02:28 — webcast logistics
- 0001032975-26-000047:8k_2_02:29 — webcast logistics
- 0001032975-26-000047:8k_2_02:30 — heading
- 0001032975-26-000047:8k_2_02:31 — non-GAAP exclusion list, boilerplate (that tariff refunds are not excluded is noted in the 8k_2_02:12 item)
- 0001032975-26-000047:8k_2_02:32 — constant-currency definition and no reconciliation for the outlook, boilerplate
- 0001032975-26-000047:8k_2_02:33 — heading
- 0001032975-26-000047:8k_2_02:34 — Regulation FD boilerplate
- 0001032975-26-000047:8k_2_02:35 — heading
- 0001032975-26-000047:8k_2_02:36 — company description boilerplate
- 0001032975-26-000047:8k_2_02:37 — end mark
- 0001032975-26-000047:8k_2_02:38 — fragment of forward-looking statement, boilerplate
- 0001032975-26-000047:8k_2_02:39 — comparison basis boilerplate
- 0001032975-26-000047:8k_2_02:40 — trademark boilerplate
- 0001032975-26-000047:8k_2_02:41 — tag
- 0001032975-26-000047:8k_2_02:42 — preliminary income statement, amounts only
- 0001032975-26-000047:8k_2_02:43 — preliminary balance sheet, amounts only
- 0001032975-26-000047:8k_2_02:44 — preliminary cash flow statement, amounts only
- 0001032975-26-000047:8k_2_02:45 — sales by category table, amounts only
- 0001032975-26-000047:8k_2_02:46 — footnote (Gaming includes Streamlabs)
- 0001032975-26-000047:8k_2_02:47 — footnote (Other category)
- 0001032975-26-000047:8k_2_02:48 — GAAP to non-GAAP reconciliation, amounts only
- 0001032975-26-000047:8k_2_02:49 — share-based compensation table, amounts only
- 0001032975-26-000047:8k_2_02:50 — caveat on preliminary results, boilerplate
- 0001032975-26-000047:8k_2_02:51 — heading
- 0001032975-26-000047:8k_2_02:52 — non-GAAP rationale boilerplate
- 0001032975-26-000047:8k_2_02:53 — non-GAAP rationale boilerplate
- 0001032975-26-000047:8k_2_02:54 — share-based compensation exclusion boilerplate
- 0001032975-26-000047:8k_2_02:55 — amortization exclusion boilerplate
- 0001032975-26-000047:8k_2_02:56 — acquisition cost exclusion boilerplate
- 0001032975-26-000047:8k_2_02:57 — restructuring exclusion boilerplate
- 0001032975-26-000047:8k_2_02:58 — investment gain or loss exclusion boilerplate
- 0001032975-26-000047:8k_2_02:59 — tax adjustment boilerplate
- 0001032975-26-000047:8k_2_02:60 — non-GAAP limitations boilerplate
- 0001032975-26-000047:8k_2_02:61 — heading
- 0001032975-26-000047:8k_2_02:62 — constant currency boilerplate

### Note change history
I used the change history only to see what is new. Two removed prior-period paragraphs had no current-period counterpart, so I made items from them: 0001032975-26-000011:note_history:15 and 0001032975-26-000011:note_history:16. All other history entries correspond to the current paragraphs itemized or listed above.
