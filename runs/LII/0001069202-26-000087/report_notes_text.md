<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# LII 10-Q for the quarter ended June 30, 2026 (0001069202-26-000087): notes-text reader report

## What I read, and what was missing

- **Files read in full:** input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md and input_prior_predictions.md.
- **Forbidden material:** I found none. There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no prior-run probability and no outcome window. The 8-K body contains the company's own release tables. Those are part of the 8-K body, and I did no arithmetic on them.
- **Missing from my input:**
  - There is no auditor's report. The controls file holds only Item 4, as expected for a 10-Q.
  - There is no Item 1A diff, no Exhibit 21 diff and no Exhibit 10.
  - The 8-K list shows a filing on 2026-05-28 (0001069202-26-000076, items 5.02 and 5.07) whose body is not in my input. The only 8-K body is the 2026-07-29 item 2.02 earnings release.
  - The list shows no late-filing notifications.
  - MD&A refers to "Note 14" for the July 2026 Heat Controller acquisition. Note 14 is not in my notes input, which ends with Note 13.
- **Prior flags:** none. There are no earlier runs.
- **Arithmetic:** none was performed. Wherever two figures appear below, they are quoted as each document states them. Whether they tie is left to the numbers reader.

## Items

```json
{ "id": "narrative_signs_of_operating_pressure_home_comfort_mixed_quarter_market_softness",
  "what_changed": "The MD&A overview now calls second-quarter results 'mixed'. It says Home Comfort Solutions 'faced volume headwinds driven by market softness'. In prose it says segment net sales decreased 7% and segment profit decreased $30 million, while consolidated segment profit was 'relatively flat'.",
  "account": "Home Comfort Solutions net sales and segment profit",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Results for the second quarter of 2026 were mixed as our Home Comfort Solutions segment faced volume headwinds driven by market softness.",
  "paragraph_id": "0001069202-26-000087:mdna:8",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_replacement_tariff_framework_material_costs",
  "what_changed": "New text says the following. The temporary Section 122 global surcharge of 10% ran through July 24, 2026. It was replaced by a Section 301 'forced labor' tariff framework of 10% or 12.5% covering 60 trading partners; Section 232 articles and qualifying USMCA goods are excluded. Section 232 tariffs were modified in April and June 2026. The company is 'evaluating the potential impact of all tariff actions on future material costs and sourcing decisions.' The prose implies that a tariff cost on imported inputs continues after the IEEPA refunds.",
  "account": "cost of goods sold (material and tariff costs)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The temporary surcharge was replaced by a new Section 301 forced labor tariffs framework of 10% or 12.5%, covering imports from 60 trading partners.",
  "paragraph_id": "0001069202-26-000087:mdna:18",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_ieepa_ruling_refunds_in_process",
  "what_changed": "New text says the Supreme Court ruled against IEEPA tariffs in February 2026 and that U.S. Customs and Border Protection 'is now processing valid court-ordered IEEPA refunds'. Section 232 and Section 301 tariffs were not repealed. This is the source of the tariff refunds that MD&A and the release net against product cost this quarter. No notes paragraph carried as text says how or when refunds are recognized (on receipt or on accrual), whether a refund receivable is recorded, or whether more refunds are expected. Whether an unchanged notes paragraph covers this is insufficient: the prior text of unchanged paragraphs is not in my input.",
  "account": "cost of goods sold (tariff refunds); other receivables",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "In February 2026, the U.S. Supreme Court ruled against tariffs imposed under IEEPA, and U.S. Customs and Border Protection is now processing valid court-ordered IEEPA refunds.",
  "paragraph_id": "0001069202-26-000087:mdna:17",
  "explanation": false }
```

```json
{ "id": "earnings_quality_tariff_refunds_netted_in_product_cost",
  "what_changed": "MD&A now says the quarter's gross-margin increase came after higher product costs stated 'net of $30 million in tariff refunds'. The refunds are folded into the product-cost driver rather than shown as a separate line. The text does not say whether the refunds relate to tariffs charged to cost of goods sold in earlier periods, or whether they will recur. The prose implies this quarter's reported gross profit includes a refund benefit.",
  "account": "gross profit (cost of goods sold)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "partially offset by 80 bps from higher product costs, primarily reflecting inflation and factory under absorption, net of $30 million in tariff refunds",
  "paragraph_id": "0001069202-26-000087:mdna:25",
  "explanation": false }
```

```json
{ "id": "earnings_quality_tariff_refunds_earlier_than_expected_release",
  "what_changed": "The earnings release says 'earlier than expected tariff refunds provided a benefit during the quarter' in Home Comfort Solutions. Management is calling the refund timing ahead of its own expectation. None of the MD&A paragraphs carried as text uses 'earlier than expected'; the 10-Q presents the refunds only as a netting item inside product cost. The prose implies a timing benefit in this quarter's cost of goods sold that may not repeat in later quarters.",
  "account": "cost of goods sold (Home Comfort Solutions)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "while earlier than expected tariff refunds provided a benefit during the quarter.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:16",
  "explanation": false }
```

```json
{ "id": "earnings_quality_six_month_gross_margin_decline_product_cost",
  "what_changed": "New six-month text says gross margin 'decreased 20 bps'. The stated headwinds are higher product costs (inflation and factory under absorption, 'net of $30 million in tariff refunds'), freight and distribution, and miscellaneous costs. The stated offsets are mix and price, and completed acquisitions. The six-month text uses the same refund wording, 'net of $30 million in tariff refunds', as the quarter's text.",
  "account": "gross profit",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Gross profit margins for the six months ended June 30, 2026 decreased 20 bps to 33.2% as compared to 33.4% in the same period in 2025.",
  "paragraph_id": "0001069202-26-000087:mdna:55",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_consolidated_sales_bridge_organic_volume_decline",
  "what_changed": "MD&A attributes the quarter's 3% net sales increase to a 3% increase from mix and price and a 4% increase from completed-acquisition volumes. These were partly offset by 'a 4% decrease in sales volumes'. In words, organic volume is declining.",
  "account": "net sales (organic sales volume)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "a 4% increase in sales volumes from completed acquisitions, which were partially offset by a 4% decrease in sales volumes.",
  "paragraph_id": "0001069202-26-000087:mdna:23",
  "explanation": false }
```

```json
{ "id": "across_documents_revenue_growth_attribution_release_versus_mdna",
  "what_changed": "The release's financial-highlights line says revenue was up 3%, 'driven by revenue from completed acquisitions', and names acquisitions only. The 10-Q MD&A (mdna:23) attributes the same increase to mix and price plus completed-acquisition volumes, partly offset by an organic volume decrease. The two documents attribute the growth differently in words. Reconciling them is for the numbers reader.",
  "account": "net sales",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Revenue: $1.5 billion was up 3%, driven by revenue from completed acquisitions.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:21",
  "explanation": false }
```

```json
{ "id": "earnings_quality_sga_discretionary_employee_costs_and_acquisitions",
  "what_changed": "MD&A says SG&A increased $10 million in the quarter, to $183 million. It attributes the increase to 'higher discretionary and employee-related costs' and the fourth-quarter 2025 Duro Dyne and Supco acquisitions. The six-month paragraph (mdna:59) gives the same causes.",
  "account": "selling, general and administrative expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily attributable to higher discretionary and employee-related costs and the acquisition of Duro Dyne and Supco in the fourth quarter of 2025",
  "paragraph_id": "0001069202-26-000087:mdna:27",
  "explanation": false }
```

```json
{ "id": "earnings_quality_equity_method_income_quarter_de_minimis",
  "what_changed": "A new sentence calls second-quarter income from equity method investments 'de minimis' and 'consistent with 2025'. The segment table in the notes (notes:37) is headed '(Loss) Income from Equity Method Investments' and gives segment and Corporate and Other amounts. Whether 'consistent' holds is for the numbers reader.",
  "account": "income from equity method investments",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Income from equity method investments was de minimis in the second quarter of 2026, consistent with 2025.",
  "paragraph_id": "0001069202-26-000087:mdna:32",
  "explanation": false }
```

```json
{ "id": "earnings_quality_equity_method_income_six_months_decreased_slightly",
  "what_changed": "New six-month text says equity method income 'decreased slightly' to $1 million, compared with $3 million in the same period of 2025.",
  "account": "income from equity method investments",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Income from equity method investments decreased slightly to $1 million for the six months ended June 30, 2026 as compared to $3 million the same period in 2025.",
  "paragraph_id": "0001069202-26-000087:mdna:64",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_expense_commercial_paper_and_term_loan",
  "what_changed": "MD&A says net interest expense increased to $15 million from $8 million. The stated causes are increased commercial paper borrowings and the term loan entered into in October 2025. The prose says commercial paper borrowings increased. The six-month paragraph (mdna:66) gives the same causes.",
  "account": "interest expense, net; commercial paper",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to increased borrowings on our commercial paper facility and our term loan agreement entered into in October of 2025.",
  "paragraph_id": "0001069202-26-000087:mdna:34",
  "explanation": false }
```

```json
{ "id": "earnings_quality_effective_tax_rate_higher_tax_jurisdictions",
  "what_changed": "MD&A, and the tax note (notes:108), say the quarter's effective tax rate was 20.8% against 19.4% a year earlier. They attribute the increase to 'higher income in higher tax jurisdictions'. The six-month paragraph (mdna:68) gives the same cause for its 20.6% rate.",
  "account": "provision for income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in the rate is primarily due to higher income in higher tax jurisdictions.",
  "paragraph_id": "0001069202-26-000087:mdna:36",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_home_comfort_volume_decline",
  "what_changed": "MD&A says Home Comfort Solutions net sales 'decreased 7%', primarily because of 'a 12% decrease in sales volumes'. This was partly offset by 3% from mix and price and 2% from completed-acquisition volumes. The six-month text (mdna:73) states a 16% volume decrease.",
  "account": "Home Comfort Solutions net sales",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Net sales decreased 7% in the second quarter of 2026 as compared to the same period in 2025 primarily due to a 12% decrease in sales volumes",
  "paragraph_id": "0001069202-26-000087:mdna:41",
  "explanation": false }
```

```json
{ "id": "earnings_quality_home_comfort_profit_bridge_tariff_refunds",
  "what_changed": "MD&A says Home Comfort Solutions segment profit 'decreased $30 million'. The stated headwinds are a $49 million volume headwind, $3 million of freight and distribution, '$2 million from product cost inflation and lower factory absorption, net of $25 million in tariff refunds', and $8 million of miscellaneous other costs. The stated offsets are $24 million from mix and price, $5 million from acquisitions and $3 million of SG&A improvement. A stated $25 million refund sits inside this segment's product-cost line.",
  "account": "Home Comfort Solutions segment profit",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "$2 million from product cost inflation and lower factory absorption, net of $25 million in tariff refunds",
  "paragraph_id": "0001069202-26-000087:mdna:43",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_building_climate_volume_growth",
  "what_changed": "MD&A says Building Climate Solutions net sales 'increased 24%', from a 12% increase in sales volumes, a 9% increase from completed-acquisition volumes, and 3% from mix and price. The six-month text (mdna:78) states a 14% volume increase.",
  "account": "Building Climate Solutions net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Net sales increased 24% in the second quarter of 2026 as compared to the same period in 2025 primarily due to a 12% increase in sales volumes",
  "paragraph_id": "0001069202-26-000087:mdna:47",
  "explanation": false }
```

```json
{ "id": "earnings_quality_building_climate_profit_bridge_tariff_refunds",
  "what_changed": "MD&A says Building Climate Solutions segment profit 'increased $35 million'. The stated drivers are $23 million from volume, $15 million from mix and price and $11 million from completed-acquisition volumes. These were partly offset by '$9 million in product cost inflation and lower factory absorption, net of $5 million in tariff refunds' and $5 million of other costs. A stated refund amount also sits inside this segment's product-cost line.",
  "account": "Building Climate Solutions segment profit",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$9 million in product cost inflation and lower factory absorption, net of $5 million in tariff refunds",
  "paragraph_id": "0001069202-26-000087:mdna:48",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_working_capital_mdna",
  "what_changed": "MD&A attributes the six-month change in operating cash flow (stated as $188.1 million against $51.0 million) to 'favorable working capital changes'. It does not name which working-capital accounts moved. For the quarter, the release (8k_2_02:25) instead names 'reduced inventory levels'. This is management attributing a cash-flow number to receivables, inventory and payables movements. Whether those accounts moved that way is for the numbers reader.",
  "account": "net cash provided by operating activities (working capital: receivables, inventories, payables)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "is primarily due to favorable working capital changes.",
  "paragraph_id": "0001069202-26-000087:mdna:85",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_capex_land_buildings_innovation_centers",
  "what_changed": "New explanation: six-month capital expenditures were $91 million against $54 million. MD&A says the increase was 'primarily driven by strategic investments in land and buildings that will support future product innovation centers'. In the notes capex table (notes:33), the Corporate and Other line carries part of the six-month spend.",
  "account": "property, plant and equipment (capital expenditures)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The increase in capital expenditures was primarily driven by strategic investments in land and buildings that will support future product innovation centers.",
  "paragraph_id": "0001069202-26-000087:mdna:86",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_financing_outflow_borrowings_and_repurchases",
  "what_changed": "MD&A says net cash used in financing 'decreased to $76 million' from $368 million. It attributes this to 'changes in net borrowings and repayments of long-term debt and repurchases of common stock'. The prose does not say which way each driver moved. The continuation (mdna:88) states $151 million of repurchases and $91 million of dividends.",
  "account": "net cash used in financing activities",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The change was primarily due to changes in net borrowings and repayments of long-term debt and repurchases of common stock",
  "paragraph_id": "0001069202-26-000087:mdna:87",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_debt_to_total_capital_ratio_increase",
  "what_changed": "MD&A says the debt-to-total-capital ratio 'increased to 55%' at June 30, 2026, from 54% at December 31, 2025.",
  "account": "total debt / total capital",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Our debt-to-total-capital ratio increased to 55% at June 30, 2026, as compared to 54% at December 31, 2025.",
  "paragraph_id": "0001069202-26-000087:mdna:104",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_heat_controller_acquisition",
  "what_changed": "New subsequent event: the company acquired Heat Controller in July 2026 for approximately $205 million, with a cross-reference to Note 14. Note 14 is not in my notes input. The notes input ends with Note 13, whose heading now reads 'Prior Year Acquisitions' (notes:150). So the purchase accounting, the funding source and any covenant effect are not in what I read. The same paragraph states cash of $51.5 million, of which $21.8 million is held in foreign locations, and says liquidity is sufficient. The prose implies goodwill, intangible assets and acquisition funding next quarter; the funding source is not stated.",
  "account": "goodwill and intangible assets; borrowings",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "In July 2026, we acquired Heat Controller for approximately $205 million.",
  "paragraph_id": "0001069202-26-000087:mdna:107",
  "explanation": false }
```

```json
{ "id": "across_documents_heat_controller_described_by_brand_names",
  "what_changed": "In the release's CEO quote, the company says it expanded its portfolio 'through the acquisition of Comfort-Aire and Century brands'. The same quote credits the Duro Dyne and Supco acquisitions with mitigating 'the continued softness in the residential end market'. The 10-Q names the July acquisition 'Heat Controller' and gives a price. The release names neither Heat Controller nor a price. The 8-K item-code list shows no separate 8-K for an acquisition: the 2026-07-29 filing carries items 2.02 and 9.01 only. My input does not say whether the brands and Heat Controller are the same transaction.",
  "account": "acquisitions",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "We also expanded our portfolio through the acquisition of Comfort-Aire and Century brands",
  "paragraph_id": "0001069202-26-000085:8k_2_02:15",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_residential_new_construction_and_absorption",
  "what_changed": "The release says the following about Home Comfort Solutions:\n- Residential market conditions 'remained challenging', although demand improved sequentially from the first quarter.\n- Residential new construction 'remained a meaningful headwind'.\n- Segment margin declined 'reflecting lower volumes and related absorption pressures'.\n- Pricing actions 'largely offset' inflation and tariff pressures.\nThe prose implies continued volume and absorption pressure in the segment.",
  "account": "Home Comfort Solutions net sales and segment margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Demand improved across both distribution channels, though residential new construction activity remained a meaningful headwind.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:16",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_building_climate_organic_growth_release",
  "what_changed": "The release states Building Climate Solutions organic revenue growth of 15%. It credits national account customers, emergency replacement and service offerings, says acquisitions added 9%, and cites 'improving commercial market conditions'. The 10-Q MD&A (mdna:47) gives this segment's growth as volume, acquisition-volume and mix-and-price percentages and does not use the word 'organic'. Reconciling the release's organic figure to the MD&A components is for the numbers reader.",
  "account": "Building Climate Solutions net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Organic revenue growth of 15% was driven by strong execution with national account customers, healthy emergency replacement activity, and growth in service offerings, while acquisitions added 9% to revenue growth.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:17",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_reduced_inventory_release",
  "what_changed": "The release attributes the quarter's operating cash flow ($172 million against $87 million) to 'reduced inventory levels'. Management is explaining a cash-flow number by an inventory movement. The release's own balance sheet and cash-flow statement carry inventories and receivables, which the numbers reader can test against the claim. The 10-Q MD&A (mdna:85) uses 'favorable working capital changes' for the six months instead. The release also mentions factory under absorption in its product-cost drivers.",
  "account": "inventories",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Operating cash flow was $172 million compared to $87 million in the prior-year quarter driven by reduced inventory levels.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:25",
  "explanation": true }
```

```json
{ "id": "across_documents_home_comfort_profit_bridge_cost_grouping",
  "what_changed": "The two documents group the costs in the Home Comfort Solutions quarterly profit bridge differently. The release states one figure: 'Distribution, freight, and other costs reduced profit by an additional $11 million'. The 10-Q MD&A (mdna:43) states $3 million from freight and distribution and, separately, $8 million from miscellaneous other costs. Whether the groupings tie is for the numbers reader.",
  "account": "Home Comfort Solutions segment profit",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Distribution, freight, and other costs reduced profit by an additional $11 million",
  "paragraph_id": "0001069202-26-000085:8k_2_02:26",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_acquisition_benefit_updated",
  "what_changed": "Full-year 2026 revenue growth guidance is reaffirmed at approximately 8%, 'including an updated 5% benefit from completed acquisitions'. The release updates the acquisition component while keeping the total. The prior acquisition component is not in my input, and the release's words give no direction for the change.",
  "account": "net sales (full year 2026)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "For full year 2026, we are reaffirming revenue growth guidance at approximately 8% growth, including an updated 5% benefit from completed acquisitions.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:31",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_eps_guidance_range_updated",
  "what_changed": "The release updates full-year 2026 EPS guidance to $23.00 to $24.00 and states that the prior range was $23.50 to $25.00. The headline calls this 'Updating full year EPS guidance range'. The release's words give no direction, and comparing the two ranges is for the numbers reader. Free cash flow guidance is 'still' $750 million to $850 million (8k_2_02:33).",
  "account": "diluted earnings per share (full year 2026)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Earnings per share guidance has been updated to a range of $23.00 to $24.00 compared to the prior range of $23.50 to $25.00.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:32",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_lifo_to_fifo_recast_comparatives",
  "what_changed": "The release says the 2025 amounts in its income statement, segment table and cash-flow statement 'are adjusted to reflect the accounting method change from LIFO to FIFO that occurred in the fourth quarter of 2025'. So the 2025 comparatives shown are on a different basis from the 2025 quarterly figures as originally filed. None of the 10-Q paragraphs carried as text in my input repeats the statement. The inventory note's policy paragraphs are carried as unchanged from the prior quarter, so I cannot see them.",
  "account": "inventories; cost of goods sold (2025 comparatives)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Note: The 2025 amounts are adjusted to reflect the accounting method change from LIFO to FIFO that occurred in the fourth quarter of 2025.",
  "paragraph_id": "0001069202-26-000085:8k_2_02:48",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_warranty_change_in_estimates_pre_existing",
  "what_changed": "The warranty roll-forward now covers six months. It carries a 'Changes in estimates associated with pre-existing liabilities' line of 3.5 (in millions), which is an addition to the liability. The same table shows new-warranty accruals of 29.0 and claims paid of (24.7). The policy text (notes:55: failure rates, cost experience) is unchanged and gives no cause for the revision of prior-period estimates.",
  "account": "product warranty liability",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Changes in estimates associated with pre-existing liabilities",
  "paragraph_id": "0001069202-26-000087:notes:59",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_antitrust_amended_consolidated_complaints",
  "what_changed": "New sentence: on July 10, 2026, the plaintiffs in In re HVAC Equipment Antitrust Litigation filed three amended, consolidated class-action complaints. The company still says it cannot reasonably estimate the range of possible loss and that an adverse outcome could be material (notes:64, unchanged). No accrual is described. The MD&A losses tables (mdna:30, mdna:62) carry a 'Special litigation charges' line, but no prose says which matter it relates to.",
  "account": "litigation contingencies",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "On July 10, 2026, the plaintiffs filed three amended, consolidated class-action complaints.",
  "paragraph_id": "0001069202-26-000087:notes:62",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_home_comfort_direct_versus_distributor_mix",
  "what_changed": "The channel-mix sentence is rolled forward and a six-month sentence is added. Direct sales were 73% and 74% of Home Comfort Solutions revenue for the three months ended June 30, 2026 and 2025, and 73% and 74% for the six months. Independent distributors made up the remainder. The prior quarter's text stated 75% and 73% for the March quarters. The release says demand improved across both distribution channels.",
  "account": "Home Comfort Solutions net sales (distributor channel)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "For the three months ended June 30, 2026 and 2025, direct sales represented 73% and 74% of revenues, respectively, and sales to independent distributors represented the remainder.",
  "paragraph_id": "0001069202-26-000087:notes:77",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_building_climate_equipment_versus_service_mix",
  "what_changed": "The equipment-versus-service sentence is rolled forward and a six-month sentence is added. Equipment sales were 84% and 81% of Building Climate Solutions revenue for the three months ended June 30, 2026 and 2025, and 83% and 80% for the six months, with service making up the remainder. Service revenue is recognized as services are performed, 'based on the relative fair value of the services provided'.",
  "account": "Building Climate Solutions net sales",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "For the three months ended June 30, 2026 and 2025, equipment sales represented 84% and 81% of revenues, respectively, and the remainder of our revenue was generated from our service business.",
  "paragraph_id": "0001069202-26-000087:notes:78",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized",
  "what_changed": "New amounts appear in prose. Revenue recognized from contract liabilities held at January 1 was $2.3 million (2026) and $0.8 million (2025) for the three months, and $3.0 million (2026) and $3.1 million (2025) for the six months. Impairment losses on receivables and contract assets are again called 'de minimis'. The release's cash-flow statement carries a provision for credit losses line, which the numbers reader can set against 'de minimis'.",
  "account": "contract liabilities; allowance for credit losses",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "For the three months ended June 30, 2026 and 2025, we recognized revenue of $2.3 million and $0.8 million and for the six months ended June 30, 2026 and 2025, we recognized revenue of $3.0 million and $3.1 million related to our contract liabilities at January 1, 2026 and 2025, respectively.",
  "paragraph_id": "0001069202-26-000087:notes:81",
  "explanation": false }
```

```json
{ "id": "earnings_quality_hedge_gain_reclassification_next_twelve_months",
  "what_changed": "At June 30, 2026 prices and rates, the company now expects to reclassify $10.2 million of derivative gain from AOCL into earnings within the next 12 months. The reclassification table (notes:138) books derivative gains to 'Cost of goods sold; Losses and other expenses, net'. The prose implies that, if prices hold, hedge gains keep reducing cost of goods sold over the next year.",
  "account": "cost of goods sold (cash flow hedge gains)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Assuming commodity prices and foreign currency exchange rates remain constant, we expect to reclassify $10.2 million of derivative gain as of June 30, 2026 into earnings within the next 12 months.",
  "paragraph_id": "0001069202-26-000087:notes:99",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_irs_audit_cross_border_transactions",
  "what_changed": "This paragraph is carried as text, so it differs from the prior quarter in some respect. The note history has no entry for the tax note, so what exactly changed is insufficient. It now says the following:\n- The IRS is auditing the 2021 and 2022 federal returns, 'including cross border transactions'.\n- State, local and foreign audits cover 2019 through 2024.\n- Adequate amounts are reserved, but final resolution 'could result in settlements or judgments in excess of our reserves'.\nGross unrecognized tax benefits are stated at $5.3 million (notes:107).",
  "account": "income tax reserves (unrecognized tax benefits)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Internal Revenue Service is currently auditing certain aspects of our U.S. federal income tax returns for 2021 and 2022, including cross border transactions.",
  "paragraph_id": "0001069202-26-000087:notes:109",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_revolver_standby_letters_of_credit",
  "what_changed": "The revolving credit paragraph now says $1.7 million was committed to standby letters of credit at June 30, 2026. The prior quarter's text said 'no amounts committed to standby letters of credit as of March 31, 2026'. Availability is now stated as $586.3 million (prior text: $639.0 million), after commercial paper outstanding of $412.0 million (notes:114). The text repeats that availability is reduced by commercial paper borrowings. This is a new commitment where the prior text recorded none.",
  "account": "standby letters of credit; revolving credit availability",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "We had no outstanding borrowings and $1.7 million committed to standby letters of credit as of June 30, 2026.",
  "paragraph_id": "0001069202-26-000087:notes:123",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_duro_dyne_supco_measurement_period_adjustment",
  "what_changed": "The Duro Dyne and Supco purchase-price allocation table now has an 'Adjustment' column between December 31, 2025 and June 30, 2026. Net tangible assets acquired are adjusted by (4.2), goodwill by 6.5 and total investment by 2.3 (in millions), and intangible assets are unchanged. The goodwill roll-forward (notes:88) shows a goodwill adjustment in both segments. The prose paragraph describing the acquisitions (notes:152) is carried as unchanged, so no text explains the measurement-period adjustment or the change to total investment.",
  "account": "goodwill; net tangible assets acquired",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Net tangible assets acquired",
  "paragraph_id": "0001069202-26-000087:notes:153",
  "explanation": false }
```

## Paragraphs carried as text that are not items

Each line gives the paragraph id and why there is no item. "Insufficient" means the paragraph is carried as text but my input does not show the prior wording, so I cannot tell what changed.

### 8-K (0001069202-26-000085)

- 8k_2_02:1 — exhibit file metadata.
- 8k_2_02:2 — document label.
- 8k_2_02:3 — exhibit label.
- 8k_2_02:4 — release title.
- 8k_2_02:5 — rule line.
- 8k_2_02:6 — heading.
- 8k_2_02:7 — comparison-basis note; boilerplate.
- 8k_2_02:8 — revenue amount; amounts only (its attribution is the item at 8k_2_02:21).
- 8k_2_02:9 — operating income amount; amounts only.
- 8k_2_02:10 — diluted EPS; amounts only.
- 8k_2_02:11 — headline of the EPS guidance update; covered by the item at 8k_2_02:32.
- 8k_2_02:12 — rule line.
- 8k_2_02:13 — dateline with headline amounts; amounts only.
- 8k_2_02:14 — revenue, segment profit, margin and adjusted EPS; amounts only. Its "total segment profit" is footnoted as including unallocated corporate expenses.
- 8k_2_02:18 — footnote; definitional.
- 8k_2_02:19 — heading.
- 8k_2_02:20 — comparison-basis note.
- 8k_2_02:22 — operating income and margin; amounts only.
- 8k_2_02:23 — consolidated profit bridge. Its "net of $30 million in tariff refunds" and product-cost drivers are covered by the tariff-refund items (mdna:25, 8k_2_02:16). Otherwise amounts only.
- 8k_2_02:24 — net income and EPS; amounts only.
- 8k_2_02:27 — Building Climate Solutions bridge; same drivers as the item at mdna:48.
- 8k_2_02:28 — corporate expense amount; amounts only.
- 8k_2_02:29 — footnote.
- 8k_2_02:30 — heading.
- 8k_2_02:33 — free cash flow guidance, "still" in the same range by its own wording; no change. Noted in the EPS guidance item.
- 8k_2_02:34 — heading.
- 8k_2_02:35 — conference-call logistics.
- 8k_2_02:36 — heading.
- 8k_2_02:37 — company description boilerplate.
- 8k_2_02:38 — heading.
- 8k_2_02:39 — forward-looking-statement boilerplate.
- 8k_2_02:40 — pointer to the non-GAAP reconciliation; boilerplate.
- 8k_2_02:41 — boilerplate on forward-looking non-GAAP measures.
- 8k_2_02:42 — continuation of 8k_2_02:41; boilerplate.
- 8k_2_02:43 — table heading.
- 8k_2_02:44 — table heading.
- 8k_2_02:45 — table heading.
- 8k_2_02:46 — income statement table; amounts only.
- 8k_2_02:47 — rounding footnote.
- 8k_2_02:49 — table heading.
- 8k_2_02:50 — segment sales and profit table; amounts only.
- 8k_2_02:51 — segment profit definition; boilerplate.
- 8k_2_02:52 — definition bullet.
- 8k_2_02:53 — definition bullet.
- 8k_2_02:54 — definition bullet.
- 8k_2_02:55 — corporate expense footnote; definitional.
- 8k_2_02:56 — LIFO-to-FIFO note repeated; covered by the item at 8k_2_02:48.
- 8k_2_02:57 — heading.
- 8k_2_02:58 — heading.
- 8k_2_02:59 — balance sheet; amounts only.
- 8k_2_02:60 — heading.
- 8k_2_02:61 — heading.
- 8k_2_02:62 — heading.
- 8k_2_02:63 — cash-flow statement; amounts only.
- 8k_2_02:64 — LIFO-to-FIFO note repeated; covered by the item at 8k_2_02:48.
- 8k_2_02:65 — non-GAAP rationale; boilerplate.
- 8k_2_02:66 — free cash flow reconciliation table; amounts only.

### Item 4, controls (0001069202-26-000087)

- item_4_controls:1 — heading.
- item_4_controls:2 — heading.
- item_4_controls:3 — disclosure controls concluded effective as of June 30, 2026; date rolled forward, standard conclusion.
- item_4_controls:4 — heading.
- item_4_controls:5 — no changes in internal control over financial reporting; standard statement, no change in substance evident.

### MD&A (0001069202-26-000087)

- mdna:10 — net sales amount; amounts only.
- mdna:11 — operating income drivers; same drivers as the items at mdna:23 and mdna:25 (this bullet does not mention the tariff refunds).
- mdna:12 — net income amount; amounts only.
- mdna:13 — diluted EPS; amounts only.
- mdna:14 — dividends and repurchases; amounts only.
- mdna:16 — list of tariff authorities; context for the items at mdna:17 and mdna:18. Insufficient to tell what changed.
- mdna:19 — section heading; date rolled forward.
- mdna:21 — consolidated results table; amounts only.
- mdna:28 — heading.
- mdna:29 — table intro; date rolled forward.
- mdna:30 — losses (gains) table; amounts only. Its "Special litigation charges" line is noted in the antitrust item.
- mdna:37 — heading; date rolled forward.
- mdna:39 — table intro.
- mdna:40 — Home Comfort Solutions table; amounts only.
- mdna:42 — sentence tail of mdna:41.
- mdna:45 — table intro.
- mdna:46 — Building Climate Solutions table; amounts only.
- mdna:49 — heading.
- mdna:50 — table intro.
- mdna:51 — six-month results table; amounts only.
- mdna:52 — heading.
- mdna:53 — six-month net sales drivers; same drivers as the item at mdna:23, six-month amounts.
- mdna:54 — heading.
- mdna:56 — page number.
- mdna:57 — sentence tail of mdna:55.
- mdna:58 — heading.
- mdna:59 — six-month SG&A; same causes as the item at mdna:27, amounts only.
- mdna:60 — heading.
- mdna:61 — table intro.
- mdna:62 — six-month losses (gains) table; amounts only. It labels the 0.8 line "Other operating loss", where the quarterly table says "Other items, net"; a label difference only.
- mdna:63 — heading.
- mdna:65 — heading.
- mdna:66 — six-month interest expense; same causes as the item at mdna:34.
- mdna:67 — heading.
- mdna:68 — six-month effective tax rate; same cause as the item at mdna:36.
- mdna:69 — heading.
- mdna:70 — heading.
- mdna:71 — table intro.
- mdna:72 — six-month Home Comfort Solutions table; amounts only.
- mdna:73 — six-month Home Comfort Solutions sales drivers; same drivers as the item at mdna:41.
- mdna:74 — six-month Home Comfort Solutions profit bridge; same drivers as the item at mdna:43, six-month amounts.
- mdna:75 — heading.
- mdna:76 — table intro.
- mdna:77 — six-month Building Climate Solutions table; amounts only.
- mdna:78 — six-month Building Climate Solutions sales drivers; same drivers as the item at mdna:47.
- mdna:79 — six-month Building Climate Solutions profit bridge; same drivers as the item at mdna:48, six-month amounts.
- mdna:83 — table intro.
- mdna:84 — cash-flow summary table; amounts only.
- mdna:88 — tail of mdna:87; repurchase and dividend amounts.
- mdna:90 — table intro; date rolled forward.
- mdna:91 — debt table; amounts only.
- mdna:93 — commercial paper program; amount and date rolled forward. "There are" here versus "There were" in the notes is wording only.
- mdna:95 — revolving credit agreement; same text as the item at notes:123.
- mdna:97 — term loan terms; same substance as notes:119, unchanged per the note history; paragraph split only.
- mdna:98 — tail of mdna:97.
- mdna:99 — term loan covenants; same substance as notes:120, unchanged.
- mdna:102 — senior notes change-of-control and covenants; wording only against notes:135.
- mdna:105 — credit ratings as of June 30, 2026; date rolled forward. Insufficient to tell whether the ratings or outlooks changed, because the prior text is not in my input.
- mdna:109 — Obligor Group description; split across a page.
- mdna:110 — tail of mdna:109.
- mdna:111 — basis of the summarized financial information; boilerplate. Insufficient to identify a change.
- mdna:112 — table intro; dates rolled forward.
- mdna:113 — Obligor Group table; amounts only.
- mdna:116 — heading.
- mdna:117 — cross-reference to Note 4. Insufficient to identify a change.

### Notes (0001069202-26-000087)

- notes:2 — spacing after commas only (note history 9).
- notes:4 — period rolled forward; now names the six-month cash-flow period (note history 10).
- notes:9 — estimates boilerplate; no note-history entry. Insufficient, and no change in substance is evident.
- notes:12 — segment products and markets table; no note-history entry. Insufficient to identify what changed.
- notes:18 — three-month segment table; amounts only.
- notes:19 — six-month segment table; amounts only.
- notes:22 — lead-in to the segment profit definition; wording. Insufficient: no note-history entry.
- notes:26 — reconciliation to operating income; amounts only.
- notes:30 — segment assets; amounts only.
- notes:33 — capex by segment; amounts only (its cause is the item at mdna:86).
- notes:35 — depreciation and amortization by segment; amounts only.
- notes:37 — equity method income by segment; amounts only (characterized in the items at mdna:32 and mdna:64).
- notes:40 — PP&E by geography; amounts only.
- notes:44 — EPS table; amounts only.
- notes:46 — anti-dilutive securities statement; dates rolled forward.
- notes:47 — note heading.
- notes:48 — heading.
- notes:49 — lease policy; unchanged per the note history.
- notes:50 — paragraph break moved; wording only (note history 1).
- notes:51 — "ASC" spelled out; wording only (note history 2).
- notes:52 — paragraph rejoined; wording only (note history 3).
- notes:53 — real-estate share of leases; no note-history entry, so unchanged.
- notes:54 — heading.
- notes:55 — warranty policy; unchanged per the note history.
- notes:56 — table intro; unchanged.
- notes:57 — warranty liability split between accrued expenses and other liabilities; amounts only (note history 4).
- notes:58 — table intro rolled to six months (note history 5).
- notes:60 — heading.
- notes:61 — heading.
- notes:63 — allegations and class definition; unchanged per the note history.
- notes:64 — cannot estimate the loss, adverse outcome could be material; unchanged per the note history. Cited in the antitrust item.
- notes:65 — heading.
- notes:66 — other claims and lawsuits; unchanged.
- notes:67 — opinion on other litigation; unchanged.
- notes:69 — repurchase authorization and remaining availability; amount and date rolled forward.
- notes:70 — shares repurchased and cost; amounts only.
- notes:73 — revenue by geography, quarter 2026; amounts only (note history 25).
- notes:74 — revenue by geography, quarter 2025; amounts only (note history 26).
- notes:75 — six-month 2026 table added; normal period expansion for a second quarter, amounts only (note history 27).
- notes:76 — six-month 2025 table added; same reason (note history 28).
- notes:80 — contract assets and liabilities; amounts only (note history 31).
- notes:84 — inventory components; amounts only.
- notes:88 — goodwill roll-forward; covered by the item at notes:153.
- notes:90 — no goodwill impairments; date rolled forward.
- notes:93 — commodity hedging policy; no note-history entry. Insufficient, and no change in substance is evident.
- notes:97 — hedges mature through December 2027, with reclassification within 18 months; no note-history entry. Insufficient to identify what changed.
- notes:98 — AOCL balances for hedges; amounts only.
- notes:102 — stock-based compensation table; amounts only.
- notes:105 — pension cost table; amounts only.
- notes:107 — gross unrecognized tax benefits; amount and date only. Cited in the IRS item.
- notes:108 — effective tax rate; same text and cause as the item at mdna:36.
- notes:110 — note heading.
- notes:111 — table intro.
- notes:112 — debt table; amounts only (note history 14 and 24).
- notes:113 — heading.
- notes:114 — commercial paper outstanding at June 30, 2026; amount and date rolled forward (note history 15). Used in the letters-of-credit item.
- notes:115 — table intro.
- notes:116 — commercial paper rate; amounts only (note history 11 and 16).
- notes:117 — heading.
- notes:118 — heading.
- notes:119 — term loan terms; unchanged per the note history.
- notes:120 — term loan covenants; unchanged.
- notes:121 — term loan rate; amounts only (note history 12 and 17).
- notes:122 — heading.
- notes:124 — table intro.
- notes:125 — revolver rate shown as a dash; date only (note history 13 and 19).
- notes:126 — guarantors and leverage-ratio covenant; unchanged per the note history.
- notes:127 — events of default; unchanged.
- notes:128 — cross-default threshold; unchanged.
- notes:129 — cross-default condition; unchanged.
- notes:130 — cross-default across debt agreements; unchanged.
- notes:131 — remedies on default; unchanged.
- notes:132 — covenant compliance; unchanged.
- notes:133 — heading.
- notes:134 — senior notes terms; paragraph split only (note history 20).
- notes:135 — remainder of the split paragraph; wording only (note history 21).
- notes:138 — AOCL reclassification table; amounts only. Cited in the hedge item.
- notes:139 — table intro; period rolled forward.
- notes:140 — AOCL roll-forward; amounts only.
- notes:143 — fair value methods unchanged; date rolled forward.
- notes:149 — fair value of the senior notes; amounts only.
- notes:150 — note heading "Prior Year Acquisitions"; cited in the Heat Controller item. The prior title is not in my input.
- notes:151 — heading.

### Note change history

The note history is accounted for here by mapping each entry to the notes paragraph it describes. It is not a second list of items.

- note_history:1 (087) — notes:50; wording only.
- note_history:2 (087 and 054) — notes:51; wording only.
- note_history:3 (087 and 054) — notes:52; wording only.
- note_history:4 (087 and 054) — notes:57; amounts only.
- note_history:5 (087 and 054) — notes:58; period rolled forward.
- note_history:6 (087 and 054) — notes:59; item.
- note_history:7 (087 and 054) — notes:62; item.
- note_history:8 (054, removed) — fragment now inside notes:52; wording only.
- note_history:9 (087 and 054) — notes:2; spacing only.
- note_history:10 (087 and 054) — notes:4; period rolled forward.
- note_history:11 (087 and 054) — notes:116; amounts only.
- note_history:12 (087 and 054) — notes:121; amounts only.
- note_history:13 (087 and 054) — notes:125; date only.
- note_history:14 (087 and 054) — notes:112; amounts only.
- note_history:15 (087 and 054) — notes:114; amount and date rolled forward.
- note_history:16 (087 and 054) — duplicate of note_history:11; amounts only.
- note_history:17 (087 and 054) — duplicate of note_history:12; amounts only.
- note_history:18 (087, added) — notes:123; item.
- note_history:19 (087 and 054) — duplicate of note_history:13; date only.
- note_history:20 (087, added) — notes:134; paragraph split.
- note_history:21 (087 and 054) — notes:135; paragraph split, wording only.
- note_history:22 (054, removed) — tail of the prior commercial paper paragraph; replaced by notes:114.
- note_history:23 (054, removed) — prior revolver paragraph ("no amounts committed to standby letters of credit"); replaced by notes:123, item.
- note_history:24 (087 and 054) — duplicate of note_history:14; amounts only.
- note_history:25 (087 and 054) — notes:73; amounts only.
- note_history:26 (087 and 054) — notes:74; amounts only.
- note_history:27 (087, added) — notes:75; six-month table added.
- note_history:28 (087, added) — notes:76; six-month table added.
- note_history:29 (087 and 054) — notes:77; item.
- note_history:30 (087 and 054) — notes:78; item.
- note_history:31 (087 and 054) — notes:80; amounts only.
- note_history:32 (087 and 054) — notes:81; item.
- note_history:33 (054, removed) — tail of the prior Building Climate Solutions paragraph; replaced by notes:78, item.
