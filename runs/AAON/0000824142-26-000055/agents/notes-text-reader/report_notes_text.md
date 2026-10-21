# report_notes_text — AAON, Form 10-Q 0000824142-26-000055 (quarter ended June 30, 2026)

Reader: notes-text-reader. Prior period of the same kind: 0000824142-26-000036 (Q1 2026 10-Q).

**Inputs read in full:** input_8k.md, input_controls.md, input_mdna.md, input_notes.md (all 1,105 lines), input_notes_history.md and input_prior_predictions.md.

**Forbidden-material check:** none is present. There is no trend table, price, abnormal return, short interest, other company's file, prior-run probability or outcome window. The 8-K earnings release has its own statement tables, company-stated growth percentages and guidance ranges. I read these as 8-K body text and did no arithmetic on them.

**Missing from the input:** no auditor's report is carried for this 10-Q. There is no Item 1A diff, no Exhibit 21 diff and no Exhibit 10. The only 8-K body supplied is the item 2.02 release of 2026-08-10. Prior predictions: none on record.

**No arithmetic.** Where prose and tables may disagree, an item reports what each text says and leaves reconciliation to the numbers reader and the supervisors. Where a paragraph is carried as changed but its prior wording is not in my input, the item says so. Items I could not resolve are marked `"insufficient": true`.

## Items

```json
[
  {
    "id": "results_against_expectations_record_quarterly_net_sales_drivers",
    "what_changed": "The Q2 2026 release says net sales were a record $627.0 million, up 101.2% on the prior-year quarter. It credits demand across both the AAON and BASX brands, better manufacturing throughput and use of recently added capacity. This is the prose claim of an increase; the numbers reader confirms it.",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net sales for the second quarter of 2026 increased 101.2% to a record $627.0 million, compared with $311.6 million in the second quarter of 2025.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:25",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_lead_times_improving_faster_backlog_conversion",
    "what_changed": "The CEO says production rose across the company, lead times are improving in key areas, and backlog is converting 'at a much faster pace'. Faster conversion points to higher near-term revenue and a drawdown of backlog. The release itself (8k_2_02:34) partly blames the sequential backlog decrease on this conversion. MD&A (mdna:13) separately says custom-product contracts allow price adjustments when delivery falls outside standard lead times.",
    "account": "Net sales; backlog",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Production increased across the enterprise, lead times are improving in key areas, and we are converting backlog at a much faster pace while continuing to see strong customer engagement.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:20",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_softer_commercial_hvac_market",
    "what_changed": "The release calls the AAON brand's commercial HVAC end market 'softer' and claims share gains despite it. The same wording comes back in 8k_2_02:33 ('soft end-market conditions') and 8k_2_02:34 ('soft commercial HVAC market backdrop'). None of the MD&A paragraphs carried as text this period mentions it; I cannot see the unchanged MD&A paragraphs. The prose pairs the market softness with share gains, so it implies no direction for reported AAON-branded sales.",
    "account": "Net sales (AAON-branded products)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The AAON brand continues to gain share despite a softer commercial HVAC market.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:21",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_near_term_margin_pressure_from_capacity_ramp",
    "what_changed": "The CEO says the pace of growth and the capacity ramp are causing near-term margin pressure. The rest of the sentence (8k_2_02:23) lists the planned fixes: higher utilization, productivity, sourcing, pricing actions and 'a more favorable backlog profile'.",
    "account": "Gross profit margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The pace of growth and capacity ramp is creating near-term margin pressure",
    "paragraph_id": "0000824142-26-000052:8k_2_02:22",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_outsourced_components_and_inflation_gross_margin",
    "what_changed": "The release states gross margin as 24.3%, against 26.6% a year earlier. It blames ramping new capacity including Memphis, outsourced components bought to support accelerated growth, and inflationary cost pressure. 8k_2_02:28 says these costs are being addressed through pricing, sourcing, productivity and operational initiatives.",
    "account": "Cost of sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Results reflected the impact of ramping recently added manufacturing capacity, including the Memphis facility, the use of outsourced components to support accelerated growth, and inflationary cost pressures.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:27",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_memphis_incentive_fee_called_infrequent_adjusted_out",
    "what_changed": "To reach adjusted EPS, the release adds back a $1.4 million Memphis incentive fee and calls it an 'infrequent expense'. Yet the reconciliation tables (8k_2_02:95, :101, :104) carry a 'Memphis incentive fee' add-back in the current quarter and in both prior-year columns. The footnote describes it as fees owed to the real estate broker as a percentage of incentives awarded by various entities, so it recurs whenever incentives are awarded. The non-GAAP definition (8k_2_02:93) limits adjustments to 'infrequent events, such as litigation settlements'.",
    "account": "Selling, general and administrative expenses (Memphis incentive fee)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "which includes a $1.4 million infrequent expense related to an incentive fee associated with our Memphis, Tenn. facility",
    "paragraph_id": "0000824142-26-000052:8k_2_02:30",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_sequential_backlog_decline_basx_award_timing",
    "what_changed": "New in the release: total backlog is said to have fallen 7.4% from March 31, 2026. The release blames faster conversion and 'the inherent timing variability of large BASX project awards', and adds that award timing 'can vary from quarter to quarter'. AAON-branded backlog is said to have risen sequentially. The backlog table (8k_2_02:32) includes a March 31, 2026 column.",
    "account": "Backlog (BASX-branded products)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Compared to the first quarter of 2026, total backlog decreased 7.4%, primarily reflecting accelerated backlog conversion into record revenue and the inherent timing variability of large BASX project awards.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:34",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_sales_growth_outlook_raised",
    "what_changed": "The full-year 2026 outlook table now shows year-over-year sales growth of 55%-60% under 'Current' and 40%-45% under 'Prior'. The release headlines this as 'Raises Full-Year Outlook'. It bases the outlook on backlog, throughput, capacity and 'current expectations for customer project timing' (8k_2_02:36).",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "YoY Sales Growth | 55%-60% | 40%-45%",
    "paragraph_id": "0000824142-26-000052:8k_2_02:37",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_gross_margin_outlook_revised_for_scaling_costs",
    "what_changed": "The outlook table (8k_2_02:37) now shows a gross profit margin of 25%-26% under 'Current' and 27%-28% under 'Prior'. The CEO puts the revision down to the near-term cost of scaling quickly and to price-cost timing.",
    "account": "Gross profit margin",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "the revised gross margin outlook reflects the near-term cost of scaling rapidly while we bring new capacity to higher utilization and work through price-cost timing",
    "paragraph_id": "0000824142-26-000052:8k_2_02:38",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_sga_percent_outlook_range",
    "what_changed": "The outlook table now shows SG&A as a percent of sales at 13%-14% under 'Current' and 14%-15% under 'Prior'. The release links SG&A percent to 'continued operating leverage and disciplined cost management' (8k_2_02:29). The D&A line shows the same $95M-$100M in both columns.",
    "account": "Selling, general and administrative expenses (percent of sales)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "SG&A as a % of sales | 13%-14% | 14%-15%",
    "paragraph_id": "0000824142-26-000052:8k_2_02:37",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_second_half_sequential_margin_improvement",
    "what_changed": "Management now commits in prose to sequential margin improvement in the second half of 2026. 8k_2_02:28 expects margin to improve as volume, utilization and 'backlog with improved pricing' convert. 8k_2_02:50 says the Coil Products actions are 'not yet fully reflected' and that their benefits should build through the second half.",
    "account": "Gross profit margin",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We expect sequential margin improvement in the second half of the year as higher production volumes, better utilization, pricing actions, sourcing initiatives, and continued operational discipline begin to show more clearly in reported results.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:39",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_aaon_oklahoma_price_realization_and_normalized_comparison",
    "what_changed": "The release states AAON Oklahoma sales growth as 41.7%. It credits part of that growth to favorable price realization, and part to a prior-year quarter held back by the refrigerant transition and company-specific operational problems. In other words, the prose itself says some of the growth is measured against a weak base.",
    "account": "Net sales (AAON Oklahoma)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Performance also benefited from favorable price realization and a more normalized operating environment relative to the prior year, when the industry refrigerant transition and company-specific operational challenges weighed on results.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:43",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_adjusted_segment_margin_excluding_memphis_overhead",
    "what_changed": "The release gives an AAON Oklahoma segment margin that excludes Memphis plant overhead. The text puts that overhead at $18.1 million this quarter and $3.0 million in the prior-year quarter. A non-GAAP reconciliation of 'Adjusted AAON Oklahoma Gross profit' follows (8k_2_02:106 to :108). MD&A (mdna:34) says Memphis builds BASX orders at cost, so the overhead left out is the running cost of a plant whose output is reported in BASX.",
    "account": "Cost of sales (AAON Oklahoma segment)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Excluding these costs, segment margins expanded 70 basis points to 31.2%, compared to 30.5% in the prior-year period.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:44",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_aaon_oklahoma_elevated_outsourcing",
    "what_changed": "At segment level, the release says elevated outsourcing and inflationary cost pressure offset part of AAON Oklahoma's improvement. Management asserts these pressures will not change the segment's long-term margin profile.",
    "account": "Cost of sales (AAON Oklahoma)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These pressures are being addressed through pricing and operational initiatives and are not expected to change the long-term margin profile of the segment.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:45",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_coil_products_freight_and_price_cost_timing",
    "what_changed": "The release states the Coil Products margin as 16.0%, against 17.5%. It blames inflation, outsourcing costs, freight and price-cost timing, partly offset by labor efficiency and overhead absorption. The 10-Q MD&A gives a different cause for the same movement (see across_documents_coil_margin_cause_material_costs_versus_release).",
    "account": "Cost of sales (AAON Coil Products)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Margin performance reflected inflationary cost pressures, outsourcing-related costs, freight pressure, and price-cost timing within the segment.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:49",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_working_capital_initiatives",
    "what_changed": "The CFO credits earnings and 'disciplined working capital initiatives' for six-month operating cash flow of $55.0 million and for better leverage; the text compares this with a $31.0 million use a year earlier. He says working-capital efficiency stays a focus. The prose does not say which working-capital lines drove the result. The release cash flow statement (8k_2_02:89) has separate receivables, inventories, contract asset and contract liability lines for the numbers reader.",
    "account": "Net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our strong earnings performance and disciplined working capital initiatives have driven meaningful improvement in both financial leverage and operating cash flow generation through the first half of 2026.",
    "paragraph_id": "0000824142-26-000052:8k_2_02:57",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "controls_audit_and_filings_officer_change_and_bylaw_amendment_filing",
    "what_changed": "The 8-K item-code index lists a filing on 2026-07-30, after the prior 10-Q, with items 5.02 (departure or appointment of a director or officer) and 5.03 (amendment to articles or bylaws). Its body is not in my input, so I cannot tell who left or joined or what was amended. Insufficient.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "2026-07-30 0000824142-26-000048 — 5.02, 5.03, 9.01",
    "paragraph_id": "input_8k.md item codes list (no bracketed paragraph id)",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_copper_and_aluminum_price_increases",
    "what_changed": "The input-cost update now says year-to-date average copper and aluminum prices rose, while stainless and galvanized steel fell. A three-month cost table (mdna:38) sits alongside.",
    "account": "Cost of sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "At June 30, 2026, the price (year to date average) for copper and aluminum increased by approximately 8.2% and 20.3%, respectively, while stainless steel and galvanized steel decreased approximately 14.1% and 3.4%, respectively.",
    "paragraph_id": "0000824142-26-000055:mdna:11",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_custom_product_price_adjustment_outside_standard_lead_times",
    "what_changed": "The pricing paragraph is carried as changed; its prior wording is not in my input. It now says custom and job-based engineered products are priced per project, under contract terms that allow price changes if fulfillment or delivery falls outside standard lead times. That is a variable-price term affecting the transaction price on long-lead custom work.",
    "account": "Net sales (transaction price on custom and job-based contracts)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "For custom or job-based engineered products, pricing is generally established on a per-project basis, with contractual terms that allow for price adjustments if order fulfillment or delivery falls outside standard lead times.",
    "paragraph_id": "0000824142-26-000055:mdna:13",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_tariff_surcharge_realization_lag",
    "what_changed": "The tariff paragraph is carried as changed; its prior wording is not in my input. It now says vendors 'often pass any additional costs as a result of tariffs through to us', and that the company responds with targeted price adjustments. Collecting the resulting surcharges may lag the cost increases because of production lead times.",
    "account": "Gross profit margin",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Although the realization of these surcharges may lag initial cost increases due to production lead times, we expect pricing actions to help offset tariff-related margin impacts over time, subject to market demand and competitive dynamics.",
    "paragraph_id": "0000824142-26-000055:mdna:15",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_backlog_discussion_omits_sequential_decline",
    "what_changed": "The 10-Q MD&A discusses backlog only against June 30, 2025; its table (mdna:20) has December 31, 2025 and June 30, 2025 columns. It does not mention the decrease from March 31, 2026 that the earnings release states (8k_2_02:34, 'total backlog decreased 7.4%'), nor the BASX award-timing explanation.",
    "account": "Backlog",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "At June 30, 2026, our consolidated backlog is $1,970.8 million, an increase of 98.0%, or $975.5 million, as compared to June 30, 2025.",
    "paragraph_id": "0000824142-26-000055:mdna:21",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_aaon_branded_net_sales_figure",
    "what_changed": "The MD&A summary bullet says AAON-branded net sales rose 39.3% 'to $79.7 million' for the quarter. The earnings release (8k_2_02:26) gives the same 39.3% growth 'to $282.2 million'. The disaggregation table (notes:32) also has an AAON-branded Products total for the quarter. So the two prose texts state different figures for the same quantity at the same growth rate. Which one is right is for the numbers reader.",
    "account": "Net sales (AAON-branded products)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net sales of AAON-branded products also increased 39.3%, to $79.7 million for the three months ended June 30, 2026.",
    "paragraph_id": "0000824142-26-000055:mdna:25",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_coil_growth_tied_to_large_liquid_cooling_data_center",
    "what_changed": "The MD&A now ties Coil Products growth to BASX-branded products 'for a large liquid cooling data center'. The singular wording points to one customer or project. The release (8k_2_02:48) puts BASX-branded liquid cooling sales at Coil Products at $126.6 million. mdna:21 says most backlog orders are BASX-branded data center liquid cooling. Together these suggest revenue concentrated in a single data-center program.",
    "account": "Net sales (AAON Coil Products)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Sales were up 150.9% at AAON Coil Products, primarily driven by growth in BASX-branded products of $85.6 million for a large liquid cooling data center.",
    "paragraph_id": "0000824142-26-000055:mdna:33",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_memphis_overhead_in_oklahoma_sales_in_basx",
    "what_changed": "MD&A explains that Memphis belongs to the AAON Oklahoma segment but builds intercompany sales for BASX at cost. The sales and gross profit on Memphis orders show up in BASX, while the plant's overhead stays in AAON Oklahoma. The text says Memphis added $18.1 million and $3.0 million of cost of sales to AAON Oklahoma in the two quarters. The segment table (notes:230) carries AAON Oklahoma inter-segment sales. Segment margins therefore rest on an at-cost transfer arrangement.",
    "account": "Cost of sales (segment allocation between AAON Oklahoma and BASX)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Memphis is part of AAON Oklahoma, building intercompany sales for the BASX segment at cost. As such, the sales and gross profit from orders completed in Memphis are reflected in the BASX segment, but the additional overhead cost of running the plant is reflected in the AAON Oklahoma segment.",
    "paragraph_id": "0000824142-26-000055:mdna:34",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_coil_margin_cause_material_costs_versus_release",
    "what_changed": "The 10-Q MD&A gives one cause for the Coil Products margin decrease: 'higher material costs'. The earnings release (8k_2_02:49) gives four: inflation, outsourcing costs, freight pressure and price-cost timing. The two documents explain the same movement differently.",
    "account": "Cost of sales (AAON Coil Products)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "as a result of higher material costs.",
    "paragraph_id": "0000824142-26-000055:mdna:34",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_warranty_expense_quarter_historical_claims",
    "what_changed": "MD&A says the quarter's warranty expense rose ($7.4 million per the text) because of 'an increase in our historical claims'. Warranty is accrued from historical claims by product line (notes:41), so more claims raise the accrual rate. The warranty rollforward (notes:89) and segment split (notes:91) are tables for the numbers reader.",
    "account": "Warranty accrual (accrued liabilities); warranty expense in SG&A",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Warranty is up $7.4 million due to an increase in our historical claims.",
    "paragraph_id": "0000824142-26-000055:mdna:41",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_sga_salaries_headcount_and_incentives",
    "what_changed": "MD&A says SG&A rose ($24.5 million per the text) because of added headcount 'to help build out our organizational capacity for future growth', plus bonuses and incentives 'due to better earnings'. Profit sharing also rose on the better earnings.",
    "account": "Selling, general and administrative expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Salaries and benefits have increased as we add additional headcount to help build out our organizational capacity for future growth along with additional bonuses and employee incentives due to better earnings.",
    "paragraph_id": "0000824142-26-000055:mdna:41",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_six_month_growth_against_disrupted_prior_year",
    "what_changed": "The six-month sales discussion says the 2025 comparison periods were held back. AAON-branded products suffered from the refrigerant change in Q1 2025 and a lack of coils in Q2 2025. AAON Coil Products suffered from disruption when it moved to a new ERP system on April 1, 2025. Part of the growth is therefore measured against those disrupted periods.",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "AAON-branded products were impacted in the first quarter of 2025 due to the change in refrigerant and then in the second quarter due to a lack of coils from AAON Coil Products.",
    "paragraph_id": "0000824142-26-000055:mdna:50",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "articulation_and_the_filed_history_basx_six_month_margin_described_flat",
    "what_changed": "MD&A says BASX's six-month gross margin 'remained flat year-over-year', with outsourcing costs limiting the benefit of higher volume. The six-month segment table (mdna:47) has BASX gross profit percentages for both periods; whether they are flat is for the numbers reader. For the quarter alone, the release (8k_2_02:54) describes the BASX margin as 'up from 27.9%'.",
    "account": "Gross profit margin (BASX)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "BASX gross profit margin remained flat year-over-year with additional costs related to outsourcing which limited the benefits realized by the additional volume.",
    "paragraph_id": "0000824142-26-000055:mdna:51",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_warranty_expense_six_months_sales_and_claims",
    "what_changed": "For the six months, MD&A gives two causes for the warranty increase: 'increases in sales and higher historical claims'. The quarterly explanation (mdna:41) names historical claims only.",
    "account": "Warranty accrual (accrued liabilities); warranty expense in SG&A",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Warranty has increased due to increases in sales and higher historical claims.",
    "paragraph_id": "0000824142-26-000055:mdna:57",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_estimated_annual_effective_tax_rate",
    "what_changed": "The paragraph is carried as changed. It puts the estimated annual 2026 effective tax rate at about 25.0% before discrete items. It says discrete benefits, such as excess tax benefits on stock compensation and tax credits, 'consistently' keep the actual rate below that. The prior wording, including any earlier estimate, is not in my input, so I cannot tell whether the estimate moved. The rate reconciliation (notes:116) carries the excess tax benefit line.",
    "account": "Income tax provision",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "estimated annual 2026 effective tax rate, excluding discrete events, is expected to be approximately 25.0%.",
    "paragraph_id": "0000824142-26-000055:mdna:60",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "articulation_and_the_filed_history_unrestricted_cash_increase_statement",
    "what_changed": "MD&A credits the $11.5 million increase to 'unrestricted cash and cash equivalents'. The release balance sheet (8k_2_02:83) shows 'Cash and cash equivalents' and 'Restricted cash' on separate lines. The release text (8k_2_02:56) speaks of 'cash, cash equivalents and restricted cash of $12.7 million'. Whether the increase sits in unrestricted or restricted cash is for the numbers reader to check.",
    "account": "Cash and cash equivalents",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our unrestricted cash and cash equivalents increased $11.5 million from December 31, 2025 to June 30, 2026.",
    "paragraph_id": "0000824142-26-000055:mdna:63",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_revolver_outstanding_and_availability",
    "what_changed": "MD&A gives the revolver balance at June 30, 2026 and December 31, 2025. It lists two standby letters of credit at June 30, 2026 and one at December 31, 2025, and $163.7 million of availability. The note table (notes:100) has the same lines against a $600.0 million commitment. The prose does not say which way the balance moved. mdna:106 says 2026 financing reflects revolver borrowing for working capital, offset by repayments.",
    "account": "Debt, long-term (revolver)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, and December 31, 2025, we had an outstanding balance under the Revolver of $435.0 million and $398.3 million, respectively.",
    "paragraph_id": "0000824142-26-000055:mdna:67",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_nmtc_put_call_expected_debt_forgiveness",
    "what_changed": "The 2019 New Markets Tax Credit (NMTC) paragraph in MD&A is carried as changed; the NMTC note paragraphs are unchanged. It says the seven-year compliance period ends in 2026. The company then expects the put/call to be exercised, 'forgiving a portion of the debt'. The financing is secured by Longview equipment and by a company guarantee that includes an unconditional guarantee of the NMTCs. Settlement in 2026 would reduce the NMTC obligations.",
    "account": "New markets tax credit obligations",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "seven-year compliance period ends in 2026, at which time the Company expects the put/call feature of the transaction to",
    "paragraph_id": "0000824142-26-000055:mdna:76",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_liquidity_sufficiency_through_next_year_and_capital_markets",
    "what_changed": "The liquidity-sufficiency statement is carried as changed. It now refers to 'operations in 2027 and the foreseeable future'. Its sources include a committed revolver 'or comparable financing' and 'our expected ability to access capital markets'. The prior wording is not in my input. The year may simply have rolled forward, and I cannot tell whether capital-markets access is newly cited. Insufficient.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "will satisfy our working capital needs, capital expenditures and other liquidity requirements associated with our operations in 2027 and the foreseeable future.",
    "paragraph_id": "0000824142-26-000055:mdna:93",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "liquidity_and_capital_capital_expenditures_memphis_buildout_and_software",
    "what_changed": "MD&A says six-month capex went to the continued Memphis build-out and Tulsa maintenance. It adds ongoing investment in internal-use software 'in anticipation of future Company growth'.",
    "account": "Property, plant and equipment; capitalized internal-use software",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Capital expenditures during the six months ended June 30, 2026, relate to the continued build out of our Memphis, Tennessee facility and maintenance of our Tulsa facility.",
    "paragraph_id": "0000824142-26-000055:mdna:103",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_revolver_borrowings_for_strategic_inventory_purchases",
    "what_changed": "MD&A explains 2026 financing cash flow as revolver borrowing for working capital, 'especially strategic purchases of inventory to avoid supply chain delays', plus some capex, offset by repayments. This is management's stated cause for the inventory build: deliberate stocking against supply-chain delays. The inventory table (notes:66) and the excess-and-obsolete allowance rollforward (notes:67) are for the numbers reader.",
    "account": "Inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The change in cash from financing activities in 2026 is primarily related to borrowings under our revolving credit facility to manage our working capital needs, especially strategic purchases of inventory to avoid supply chain delays and the funding of certain capital expenditures, offset by repayments we were able to make due to our operating results and financial condition.",
    "paragraph_id": "0000824142-26-000055:mdna:106",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "across_documents_refrigerant_payments_period_label_mdna",
    "what_changed": "MD&A says payments on the 2023 five-year refrigerant commitment were $4.7 million and $2.1 million 'for the three months ended June 30, 2026 and 2025'. The note (notes:211) labels $4.7 million and $2.1 million as six-month figures and gives $1.5 million for each three-month period. The same figures carry different period labels in the two documents. Both give estimated minimum future payments of $5.8 million for 2026 and $11.2 million for 2027.",
    "account": "Purchase commitments (refrigerants, off balance sheet)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the three months ended June 30, 2026 and 2025, the Company made payments of $4.7 million and $2.1 million on this contract, respectively.",
    "paragraph_id": "0000824142-26-000055:mdna:110",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_litigation_trial_and_appellate_costs",
    "what_changed": "A cautionary bullet carried as changed now reads 'costs and results of litigation, including trial and appellate costs'. The prior wording is not in my input, so I cannot tell whether 'trial and appellate costs' is new. The contingencies note (notes:209) names no specific matter and says the company does not expect a material adverse effect. Insufficient.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "costs and results of litigation, including trial and appellate costs;",
    "paragraph_id": "0000824142-26-000055:mdna:128",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "structure_and_disclosure_changes_aaon_oklahoma_basx_branded_external_sales",
    "what_changed": "The quarterly disaggregation table now shows a BASX-branded Products entry for the AAON Oklahoma segment ($107 thousand). The same cell is a dash in the prior-year quarter table (notes:33), the six-month 2025 table (notes:34) and the prior-period Q1 2026 table (note_history:19). AAON Oklahoma now books some external BASX-branded sales. That fits with Memphis, part of AAON Oklahoma, building BASX products.",
    "account": "Net sales (disaggregation by segment and brand)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "BASX-branded Products | 107 |",
    "paragraph_id": "0000824142-26-000055:notes:32",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_current_six_month_disaggregation_table_absent",
    "what_changed": "The revenue note as carried has quarterly tables for 2026 and 2025 and a six-month table for 2025 (added per note_history:21). No six-month 2026 disaggregation table appears in my input. This may be an extraction gap rather than an omission in the filing. Insufficient.",
    "account": "Net sales (disaggregation)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Six Months Ended June 30, 2025",
    "paragraph_id": "0000824142-26-000055:notes:34",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "estimates_and_discretion_warranty_policy_added_to_revenue_note",
    "what_changed": "The change history (note_history:27 to :28) shows a 'Product Warranties' policy newly placed in the revenue note. Warranty cost is provided at sale, based on historical claims by product line and management's estimate of future claims. Changes to prior-year estimates are booked in the current year. I cannot see whether the text was moved from another note, because the basis-of-presentation paragraphs are all unchanged. The policy bears on the warranty accrual that MD&A says rose on higher historical claims.",
    "account": "Warranty accrual",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "A provision is made for the estimated cost of maintaining product warranties to customers at the time the product is sold based upon historical claims experience by product line.",
    "paragraph_id": "0000824142-26-000055:notes:41",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_extended_warranty_deferral_policy_added",
    "what_changed": "Newly placed in the revenue note (note_history:29): extended parts warranties of six months to 10 years are priced separately. Their revenue is deferred and recognized straight-line over the warranty period. The extended-warranty liabilities sit in accrued liabilities (notes:93) and other long-term liabilities (notes:95).",
    "account": "Extended warranties (deferred revenue)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Revenue for these separately priced warranties is deferred and recognized on a straight-line basis over the separately priced warranty period.",
    "paragraph_id": "0000824142-26-000055:notes:42",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_representatives_principal_gross_third_party_liability",
    "what_changed": "Newly placed in the revenue note (note_history:30 to :31). The company bills and collects all sales initiated by Representatives but sets only a 'minimum sales price'. It is principal for its own equipment and books that revenue gross. Third-Party Product amounts are booked as a liability in accrued liabilities, not as revenue. I cannot see whether the text was moved from elsewhere.",
    "account": "Net sales; accrued liabilities (due to representatives)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company is considered the principal for the equipment we design and manufacture and records that revenue gross.",
    "paragraph_id": "0000824142-26-000055:notes:44",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_representatives_paid_after_collection_payments_stated",
    "what_changed": "Newly placed in the revenue note (note_history:32). Amounts due to Representatives are paid only after the customer has paid everything on the order. Payments to Representatives are now given for the three and six months of 2026 and 2025. The 'Due to representatives' line in accrued liabilities (notes:93) therefore depends on collections.",
    "account": "Accrued liabilities (due to representatives)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "are paid only after all amounts associated with the order are collected from the customer. The amount of payments to our Representatives were $18.1 million and $35.3 million for three and six months ended June 30, 2026",
    "paragraph_id": "0000824142-26-000055:notes:45",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_contract_liability_revenue_recognized_from_opening_balance",
    "what_changed": "The note now says revenue recognized from the opening contract liability balance was $76.1 million for the six months of 2026 and $5.9 million for 2025. The prior-period text gave $36.2 million for Q1 2026 (note_history:35). Recognizing revenue from customer advances draws contract liabilities down unless new advance billings replace them. The note says nothing in prose about new advance billings.",
    "account": "Contract liabilities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Revenue recognized in the reporting period that was included in the contract liability balance at the beginning of the period for the six months ended June 30, 2026 and 2025 was $76.1 million and $5.9 million.",
    "paragraph_id": "0000824142-26-000055:notes:49",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tulsa_office_lease_after_quarter",
    "what_changed": "New subsequent event: a six-year Tulsa office operating lease with about $3.7 million of undiscounted payments. It began in July 2026, and a right-of-use asset and lease liability were recorded.",
    "account": "Right of use assets; operating lease liabilities",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Subsequent to June 30, 2026, the Company entered into an operating lease agreement for office space in Tulsa, OK with a total lease term of 6 years.",
    "paragraph_id": "0000824142-26-000055:notes:58",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_tulsa_storage_lease_paragraph_changed",
    "what_changed": "This paragraph covers the November 2022 Tulsa storage lease and its January 2024 amendment, which runs to January 2029. It has no period date to roll forward, yet it is carried as changed. The prior wording is not in my input, so I cannot tell whether the expiry, the square footage or other terms changed. Insufficient.",
    "account": "Right of use assets; operating lease liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In January 2024, we amended the lease for an additional 157,550 square feet for operations and parts distribution. The amended lease term will expire January 2029.",
    "paragraph_id": "0000824142-26-000055:notes:54",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "liquidity_and_capital_leverage_ratio_covenant_stated_in_note",
    "what_changed": "The covenant sentence now gives a leverage ratio of 1.46 to 1.0 at June 30, 2026, against a 3 to 1 ceiling. The prior text (note_history:9) gave 1.71 to 1.0 at March 31, 2026. The CFO calls this a meaningful improvement in financial leverage (8k_2_02:57). MD&A repeats the ratio (mdna:27, mdna:74).",
    "account": "Leverage ratio (revolver covenant)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "At June 30, 2026, our leverage ratio was 1.46 to 1.0, which meets the requirement of not being above 3 to 1.",
    "paragraph_id": "0000824142-26-000055:notes:109",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_tennessee_investment_tax_credit_valuation_allowance",
    "what_changed": "Carried as changed: management now says it is more likely than not that the Tennessee investment tax credit carryforward may not be realized, and it has set up a valuation allowance. The rate reconciliation (notes:116) has 'Changes in valuation allowance' and 'State tax credits' lines with entries in the 2026 columns and dashes in 2025. I infer from the location that the Tennessee credit relates to the Memphis plant.",
    "account": "Deferred tax assets valuation allowance; income tax provision",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "We believe that it is more likely than not that we may not realize the benefit of our Tennessee investment tax credit carryforward and, accordingly, have established a valuation allowance against this deferred tax asset.",
    "paragraph_id": "0000824142-26-000055:notes:119",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_federal_nol_deferred_tax_asset_fully_utilized",
    "what_changed": "New: the federal NOL deferred tax asset recorded at December 31, 2025 is now said to be fully used, after use in the first two quarters of 2026. The state NOL deferred tax asset is called 'negligible'. The text continues in notes:131 and gives this as the reason no valuation allowance is recorded against it. With the NOLs used up, they no longer shelter current federal taxes. The taxes-paid table (notes:85) is for the numbers reader.",
    "account": "Deferred tax assets (NOL carryforwards); income taxes paid",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, the federal deferred tax asset balance has been fully",
    "paragraph_id": "0000824142-26-000055:notes:130",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_self_insurance_hsa_match_rate",
    "what_changed": "The self-insurance paragraph has no date to roll forward, yet it is carried as changed. It now says the company matches 175.0% of employees' allowed health savings account contributions. The prior wording, including any earlier match rate, is not in my input. Insufficient.",
    "account": "Employee benefit costs; medical self-insurance accrual",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the Company matches 175.0% of a participating",
    "paragraph_id": "0000824142-26-000055:notes:174",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_refrigerant_commitment_note_wording",
    "what_changed": "The refrigerant-commitment sentence now covers three- and six-month periods but is garbled. It gives 2026 payments of '$1.5 million and $4.7 million', then runs straight on 'for the three and six months ended June 30, 2025' to 2025 payments of '$1.5 million and $2.1 million'. The prior-period text (note_history:2) gave Q1 payments of $3.2 million for 2026 and $0.6 million for 2025. It also put estimated minimum 2026 payments at $7.3 million; that figure is now $5.8 million, and 2027 still reads $11.2 million. Reconciling the periods is for the numbers reader.",
    "account": "Purchase commitments (refrigerants)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the three and six months ended June 30, 2026, the Company made payments of $1.5 million and $4.7 million for the three and six months ended June 30, 2025, the Company made payments of $1.5 million and $2.1 million on this contract, respectively.",
    "paragraph_id": "0000824142-26-000055:notes:211",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_raw_material_purchase_commitments_remaining",
    "what_changed": "Three one-year raw-material commitments were signed in 2025. Estimated minimum 2026 payments are now $18.8 million; the prior text (note_history:3) said $23.3 million. No new commitment is described, and the text still says there are no other material purchase obligations. MD&A (mdna:111) says the same.",
    "account": "Purchase commitments (raw materials)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Estimated minimum future payments are $18.8 million for 2026.",
    "paragraph_id": "0000824142-26-000055:notes:212",
    "explanation": false,
    "insufficient": false
  }
]
```

Item count: 54. Items marked `insufficient`: 7 (the 2026-07-30 8-K, mdna:60, mdna:93, mdna:128, notes:34, notes:54 and notes:174). Items marked `explanation`: 5. Two concern the warranty reserve (mdna:41, mdna:57), one inventory (mdna:106) and two tax reserves (notes:119, and notes:130 with its continuation notes:131).

## Paragraphs carried as text that are not items

### 8-K item 2.02, earnings release (0000824142-26-000052)
- 8k_2_02:1 — exhibit header and file name.
- 8k_2_02:2 — document label.
- 8k_2_02:3 — exhibit label.
- 8k_2_02:4 — headline. Its content is covered by the items on :25, :27 and :30.
- 8k_2_02:5 — headline growth figures. Amounts only; see :25 and :30.
- 8k_2_02:6 — headline. Covered by the outlook items on :37 and :38.
- 8k_2_02:7 — section header.
- 8k_2_02:8 — note on the comparison basis.
- 8k_2_02:9 — highlight bullet. Makes the same claim as the :20 and :25 items.
- 8k_2_02:10 — highlight bullet. Amounts only; see :25.
- 8k_2_02:11 — highlight bullet. Amounts only; see :27.
- 8k_2_02:12 — highlight bullet. Amounts only; the operating income figure is missing its $ sign, which is typographic.
- 8k_2_02:13 — highlight bullet. Amounts only; see :30.
- 8k_2_02:14 — highlight bullet. Amounts only; see :33 and :34.
- 8k_2_02:15 — highlight bullet. Amounts only; see :57.
- 8k_2_02:16 — section header.
- 8k_2_02:17 — outlook bullet. Same content as the :37 and :38 items.
- 8k_2_02:18 — dateline and company description.
- 8k_2_02:19 — CEO repeats the quarter's growth figures. Amounts only.
- 8k_2_02:23 — continuation of the :22 sentence. The fixes it lists are cited in that item.
- 8k_2_02:24 — section header.
- 8k_2_02:26 — brand-level sales and backlog amounts. Its AAON-branded figure is cited in across_documents_aaon_branded_net_sales_figure.
- 8k_2_02:28 — same margin expectation as the :39 item, and cited there.
- 8k_2_02:29 — SG&A percent amounts, the same claim as mdna:26. Cited in the SG&A outlook item.
- 8k_2_02:31 — section header.
- 8k_2_02:32 — backlog table amounts. Its March 31, 2026 column is cited in the :34 item.
- 8k_2_02:33 — year-over-year backlog amounts. Its 'soft end-market' wording is cited in the :21 item.
- 8k_2_02:35 — section header.
- 8k_2_02:36 — basis for the outlook. Cited in the :37 sales-outlook item.
- 8k_2_02:40 — section header.
- 8k_2_02:41 — segment header.
- 8k_2_02:42 — AAON Oklahoma segment table amounts.
- 8k_2_02:46 — segment header.
- 8k_2_02:47 — Coil Products segment table amounts.
- 8k_2_02:48 — Coil Products sales amounts. Cited in the mdna:33 item.
- 8k_2_02:50 — Coil Products second-half expectation. Cited in the :39 item.
- 8k_2_02:51 — segment header.
- 8k_2_02:52 — BASX segment table amounts.
- 8k_2_02:53 — BASX sales amounts and drivers (Memphis, data center), the same as mdna:33.
- 8k_2_02:54 — BASX quarterly margin amounts and drivers. Cited in the mdna:51 item.
- 8k_2_02:55 — section header.
- 8k_2_02:56 — cash and revolver balance amounts, the same as mdna:67. Cited in the mdna:63 item.
- 8k_2_02:58 — section header.
- 8k_2_02:59 — conference call logistics.
- 8k_2_02:60 — section header.
- 8k_2_02:61 — boilerplate company description.
- 8k_2_02:62 — forward-looking statements heading, with no text carried under it.
- 8k_2_02:63 — contact header.
- 8k_2_02:64 — contact name.
- 8k_2_02:65 — contact title.
- 8k_2_02:66 — contact phone.
- 8k_2_02:67 — contact email.
- 8k_2_02:68 — statement header.
- 8k_2_02:69 — statement header.
- 8k_2_02:70 — "(Unaudited)" label.
- 8k_2_02:71 — income statement table. Amounts only.
- 8k_2_02:72 — page number.
- 8k_2_02:73 — statement header.
- 8k_2_02:74 — statement header.
- 8k_2_02:75 — "(Unaudited)" label.
- 8k_2_02:76 — segment table. Amounts only; the inter-segment structure is covered by the mdna:34 structure item.
- 8k_2_02:77 — footnote.
- 8k_2_02:78 — reconciliation intro.
- 8k_2_02:79 — gross-profit-to-operating-income reconciliation table. Amounts only. It labels a line 'Add: loss on disposal of assets' where :71 has a 'Gain on disposal of assets' line; that labeling is for the numbers reader.
- 8k_2_02:80 — statement header.
- 8k_2_02:81 — statement header.
- 8k_2_02:82 — "(Unaudited)" label.
- 8k_2_02:83 — balance sheet table. Amounts only; cited in the mdna:63 item.
- 8k_2_02:84 — footnote on variable interest entities.
- 8k_2_02:85 — page number.
- 8k_2_02:86 — statement header.
- 8k_2_02:87 — statement header.
- 8k_2_02:88 — "(Unaudited)" label.
- 8k_2_02:89 — cash flow table. Amounts only; cited in the :57 item.
- 8k_2_02:90 — section header.
- 8k_2_02:91 — non-GAAP boilerplate.
- 8k_2_02:92 — section header.
- 8k_2_02:93 — non-GAAP adjusted net income definition. Cited in the :30 item.
- 8k_2_02:94 — table intro.
- 8k_2_02:95 — adjusted net income reconciliation and its footnotes. Cited in the :30 item.
- 8k_2_02:96 — section header.
- 8k_2_02:97 — EBITDA definition boilerplate.
- 8k_2_02:98 — EBITDA boilerplate.
- 8k_2_02:99 — adjusted EBITDA definition.
- 8k_2_02:100 — table intro.
- 8k_2_02:101 — EBITDA reconciliation table. Amounts only; its Memphis fee line is cited in the :30 item.
- 8k_2_02:102 — section header.
- 8k_2_02:103 — table intro.
- 8k_2_02:104 — adjusted SG&A table. Amounts only; its Memphis fee line is cited in the :30 item.
- 8k_2_02:105 — page number.
- 8k_2_02:106 — section header for adjusted AAON Oklahoma gross profit. Cited in the :44 item.
- 8k_2_02:107 — table intro. Cited in the :44 item.
- 8k_2_02:108 — adjusted AAON Oklahoma gross profit table. Amounts only; cited in the :44 item.

### 8-K index and notifications (no bracketed paragraph ids)
- Item-code index, 2026-05-18 (5.07, 8.01, 9.01) and 2026-06-08 (7.01, 9.01), both after the prior 10-Q. Their bodies are not in my input, and the item codes alone (vote results, other events, Reg FD) state no change I can report.
- Item-code index, 2026-08-10. This is the release read above.
- Index entries on or before 2026-05-07 come before the prior 10-Q. They are history, not a change this period.
- Late-filing notifications: "none on or before 2026-08-10". Nothing to report.

### Item 4, controls (10-Q)
- item_4_controls:1 — heading.
- item_4_controls:2 — heading.
- item_4_controls:3 — disclosure controls concluded effective. This is the standard conclusion, with no change in substance stated.
- item_4_controls:4 — heading.
- item_4_controls:5 — states no change in internal control over financial reporting. No change in substance.
- item_4_controls:6 — page number.

### MD&A (0000824142-26-000055)
- mdna:6 — foreign sales amounts, rolled forward.
- mdna:20 — backlog table amounts. Its column set is described in across_documents_backlog_discussion_omits_sequential_decline.
- mdna:23 — income statement table. Amounts only.
- mdna:26 — SG&A percent amounts, the same claim as 8k_2_02:29.
- mdna:27 — leverage ratio and availability amounts. Covered by the notes:109 and mdna:67 items.
- mdna:29 — heading, with the date rolled forward.
- mdna:30 — quarterly segment table. Amounts only.
- mdna:35 — lead-in sentence to the raw-material table. It carries no amount, date or commitment.
- mdna:37 — table heading.
- mdna:38 — three-month raw-material cost table. Amounts only.
- mdna:40 — quarterly SG&A table. Amounts only.
- mdna:43 — quarterly tax table. Amounts only.
- mdna:46 — heading.
- mdna:47 — six-month segment table. Amounts only; cited in the mdna:51 item.
- mdna:48 — table footnote.
- mdna:49 — table footnote.
- mdna:52 — heading.
- mdna:53 — heading.
- mdna:54 — six-month raw-material cost table. Amounts only.
- mdna:55 — heading.
- mdna:56 — six-month SG&A table. Amounts only.
- mdna:58 — heading.
- mdna:59 — six-month tax table. Amounts only.
- mdna:64 — history of the loan agreement, with no new facility, amount or date. The note version (notes:96) is unchanged per the change history; the difference is wording only.
- mdna:70 — unused-commitment fee sentence, with the date rolled forward.
- mdna:72 — interest rate table. Amounts only.
- mdna:74 — covenant compliance sentence, the same as the notes:109 item.
- mdna:77 — 2023 NMTC description, split across a page break. No new fact.
- mdna:78 — continuation of mdna:77. No new fact.
- mdna:86 — repurchase authorization, with the date rolled forward.
- mdna:89 — repurchase table. Amounts only.
- mdna:92 — dividend table. A new row for the May 12, 2026 declaration at $0.10 per share; date rolled forward.
- mdna:95 — page number.
- mdna:97 — cash flow table intro, with the date rolled forward.
- mdna:98 — cash flow table. Amounts only.
- mdna:109 — purchase-obligation lead-in, with the date rolled forward.
- mdna:111 — raw-material commitments, the same as the notes:212 item.
- mdna:113 — no change in critical accounting policies, with the date rolled forward.

### Notes (0000824142-26-000055)
- notes:25 — goodwill. Date rolled forward only (note_history:4).
- notes:29 — intangible assets table. Amounts only.
- notes:33 — prior-year quarter disaggregation table. Amounts only; cited in the notes:32 item.
- notes:35 — aftermarket parts sales amounts, rolled forward.
- notes:39 — seasonality. A trailing heading moved away (note_history:26); the sentence itself is unchanged, so this is a reorder.
- notes:40 — "Product Warranties" heading, added with notes:41.
- notes:43 — "Representatives and Third-Party Products" heading, added with notes:44.
- notes:46 — contract asset and liability table. Amounts only.
- notes:48 — contract cost and billings table. Amounts only.
- notes:51 — lease terms, ranges and discount rates at the new date. Amounts and dates rolled forward.
- notes:52 — lease balance table. Amounts only.
- notes:59 — maturity table intro.
- notes:60 — lease maturity table. Amounts only.
- notes:62 — receivables table. Amounts only; no prose explaining receivables is carried.
- notes:63 — receivables allowance rollforward. Amounts only; no prose explaining the allowance is carried.
- notes:66 — inventory table. Amounts only; the inventory explanation is the mdna:106 item.
- notes:67 — excess-and-obsolete allowance rollforward. Amounts only.
- notes:69 — property, plant and equipment table. Amounts only.
- notes:71 — depreciation table. Amounts only.
- notes:74 — amortization table. Amounts only.
- notes:75 — table intro, with the date rolled forward.
- notes:76 — amortization period table. Amounts only.
- notes:78 — future amortization table. Amounts only.
- notes:81 — goodwill rollforward. Amounts only.
- notes:83 — supplemental cash flow table. Amounts only.
- notes:84 — taxes-paid intro, with the date rolled forward.
- notes:85 — taxes paid by jurisdiction. Amounts only; cited in the notes:130 item.
- notes:89 — warranty accrual rollforward. Amounts only; cited in the warranty items.
- notes:91 — warranty expense by segment. Amounts only; cited in the mdna:41 item.
- notes:93 — accrued liabilities table. Amounts only; cited in the notes:42 and notes:45 items.
- notes:95 — other long-term liabilities table. Amounts only.
- notes:96 — loan agreement history. Unchanged per the change history.
- notes:97 — Fifth Amendment history. Unchanged per the change history.
- notes:98 — Sixth Amendment history. Unchanged per the change history.
- notes:99 — heading.
- notes:100 — revolver availability table, rolled forward (note_history:6 and :10). Amounts only.
- notes:101 — heading.
- notes:102 — SOFR interest terms. Unchanged per the change history.
- notes:103 — margin and fee ranges. Unchanged per the change history.
- notes:104 — unused-commitment fee, with the date rolled forward (note_history:7).
- notes:105 — table intro.
- notes:106 — interest rate table, rolled forward (note_history:8). Amounts only.
- notes:107 — alternative base rate fallback. Unchanged per the change history.
- notes:108 — heading.
- notes:112 — tax provision components table. Amounts only.
- notes:115 — rate reconciliation intro, with the date rolled forward.
- notes:116 — rate reconciliation table. Amounts only; its valuation allowance and state credit lines are cited in the notes:119 item.
- notes:117 — list of contributing state jurisdictions, rolled forward. Its first sentence is the standing explanation for the gap between effective and statutory rates.
- notes:127 — OBBBA charitable-contribution floor effect, restated for the quarter. The text still mentions the 'Q1 tax provision calculation'; this is a date roll with stale wording and no new policy.
- notes:131 — continuation of the notes:130 sentence. Covered by that item, which is flagged as an explanation (it gives the reason no valuation allowance is recorded).
- notes:137 — option assumptions intro, with the date rolled forward.
- notes:138 — option valuation assumptions table. Amounts only.
- notes:141 — table intro.
- notes:142 — vested options table. Amounts only.
- notes:144 — option activity table. Amounts only.
- notes:145 — unrecognized option cost. Amounts only.
- notes:146 — intrinsic value of exercised options and cash received. Amounts only.
- notes:148 — unrecognized restricted stock cost. Amounts only.
- notes:150 — restricted stock activity table. Amounts only.
- notes:153 — unrecognized PSU cost. Amounts only.
- notes:154 — PSU assumptions intro, with the date rolled forward.
- notes:155 — PSU valuation assumptions. Amounts only.
- notes:158 — PSU activity table. Amounts only.
- notes:160 — PSU vesting schedule footnote. Amounts only.
- notes:163 — grant-date fair value table. Amounts only.
- notes:164 — stock compensation expense table. Amounts only.
- notes:165 — stock compensation tax benefit table. Amounts only.
- notes:167 — 401(k) plan description, with the date rolled forward.
- notes:169 — 401(k) contributions table. Amounts only.
- notes:172 — profit-sharing table. Amounts only.
- notes:175 — medical premium and HSA payments table. Amounts only.
- notes:178 — earnings per share table. Amounts only.
- notes:183 — repurchase authorization, with the date rolled forward (same as mdna:86).
- notes:186 — repurchase table. Amounts only.
- notes:191 — dividend table. A new row; date rolled forward.
- notes:208 — "Commitments and Contingencies / Other Matters" heading.
- notes:209 — standing legal-contingency paragraph. Not listed as changed in the change history; cited in the mdna:128 item.
- notes:210 — purchase-contract lead-in, with the date rolled forward (note_history:1).
- notes:213 — related parties heading and intro.
- notes:214 — related-party transactions table, now with three- and six-month columns. Amounts only.
- notes:215 — due-from-affiliates table. The prior table's 'Due to affiliates' line is no longer shown (note_history:13). Amounts only.
- notes:216 — intro.
- notes:217 — related-party relationship (entity managed by a board member's family, also a Representative). Not listed as changed in the change history.
- notes:218 — related-party relationship (supplies from entities controlled by board members and an executive). Not listed as changed in the change history.
- notes:219 — related-party relationship (part sales to a board member). Not listed as changed in the change history.
- notes:220 — related-party relationship (meeting space rental, said to have ceased in Q4 2025). Not listed as changed in the change history.
- notes:221 — related-party relationship (aircraft flight time partly owned by the CEO). Not listed as changed in the change history.
- notes:230 — segment table. Amounts only; cited in the mdna:34 structure item.
- notes:233 — segment reconciliation table. Amounts only; it has the same 'loss'/'gain' label issue as 8k_2_02:79.
- notes:235 — long-lived assets by segment. Amounts only.
- notes:237 — intangible assets and goodwill by segment. Amounts only.

### Note change history (input_notes_history.md)
- note_history:1 to :35 were used only as the record of what changed against 0000824142-26-000036. Each one maps to a note paragraph above (an item or a listed paragraph) and is not reported a second time.
