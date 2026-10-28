<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# CIEN notes-text reader — 10-Q 0001628280-26-040767 (quarter ended May 2, 2026)

## Input check

- Read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- Not in my directory: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report (this is a 10-Q and none is carried). This report does not cover changes to risk factors, subsidiaries or material contracts.
- Forbidden-content check: I found no trend table, market price series, abnormal returns, short interest, other-company files, prior probabilities or outcome window. The only per-share prices are Ciena's own average repurchase prices, stated inside the filing text (notes:128, notes:154). I treated them as filing text and used them for nothing.
- Prior flags: none on record (input_prior_predictions.md), so nothing is carried forward.
- My input has no change history for MD&A. For each MD&A paragraph carried as text, I report what the text now says. Where I cannot tell what changed in substance, the item says `insufficient`.
- I did no arithmetic. Where an amount appears in both the current and the prior text, I state both and do not compare them. Directions come only from the prose.

## Items

```json
[
  {
    "id": "narrative_signs_of_operating_pressure_constrained_supply_historically_high_backlog",
    "what_changed": "The MD&A overview now says the growth seen in fiscal 2025 continued into the first half of fiscal 2026. It says orders for products and services significantly exceeded revenue in the quarter, and that this, together with an industry-wide constrained supply environment, has produced historically high backlog.",
    "account": "Revenue; remaining performance obligations (backlog)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "with orders for our products and services significantly exceeding our revenue. This dynamic, together with an industry-wide constrained supply environment, has resulted in historically high backlog.",
    "paragraph_id": "0001628280-26-040767:mdna:8",
    "explanation": false
  },
  {
    "id": "revenue_recognition_cloud_customers_growing_share_of_business",
    "what_changed": "The overview says that as cloud-provider sales grow, a small number of those customers are becoming a larger portion of the business across multiple revenue segments.",
    "account": "Revenue concentration (10% customers); accounts receivable concentration",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As our sales to cloud providers grow, we are seeing a small number of those customers become a larger portion of our business across multiple revenue segments.",
    "paragraph_id": "0001628280-26-040767:mdna:8",
    "explanation": false
  },
  {
    "id": "earnings_quality_gross_margin_pricing_optimization_and_mix",
    "what_changed": "MD&A says gross margin increased to 44.0% from 40.2%. It attributes this primarily to higher product gross margin from cost reduction, pricing optimization and product mix.",
    "account": "Gross margin; products cost of goods sold",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to higher product gross margin associated with cost reduction, pricing optimization, and product mix.",
    "paragraph_id": "0001628280-26-040767:mdna:10",
    "explanation": false
  },
  {
    "id": "earnings_quality_research_and_development_investment_data_center",
    "what_changed": "MD&A states R&D investment of $238 million in the quarter and describes it as an 11% increase. It also says WaveLogic coherent modem investment continued, with the aim of expanding the addressable market inside and around the data center.",
    "account": "Research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "we invested $238 million in research and development activities, an increase of 11% compared to the second quarter of fiscal 2025.",
    "paragraph_id": "0001628280-26-040767:mdna:12",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capital_purchases_supply_chain_equipment",
    "what_changed": "MD&A says $115 million went to capital purchases in the first half, primarily for supply chain equipment and research and development.",
    "account": "Equipment, building, furniture and fixtures, net; payments for equipment, furniture and fixtures",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we invested $115 million in capital purchases, primarily for supply chain equipment and research and development",
    "paragraph_id": "0001628280-26-040767:mdna:14",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_generation_and_share_returns",
    "what_changed": "MD&A says cash generated from operations increased to $487 million, against $261 million a year earlier. It says $344 million went to share repurchases, covering both the buyback program and tax withholding on employee stock awards. It states cash, cash equivalents and investments of $1.4 billion.",
    "account": "Net cash provided by operating activities; repurchases of common stock",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "cash generated from operations increased to $487 million as compared to $261 million as of the end of the first half of fiscal 2025.",
    "paragraph_id": "0001628280-26-040767:mdna:14",
    "explanation": false
  },
  {
    "id": "revenue_recognition_revenue_increase_attributed_to_demand",
    "what_changed": "MD&A attributes the revenue increase to the increased demand described in the overview. It states the increase as approximately 40% ($444.9 million) for the quarter and approximately 36% ($799.6 million) for the six months.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "As a result of the increased demand described above, our revenue increased by approximately 40%, or $444.9 million, in the second quarter of fiscal 2026",
    "paragraph_id": "0001628280-26-040767:mdna:20",
    "explanation": false
  },
  {
    "id": "revenue_recognition_optical_networking_waveserver_and_line_systems",
    "what_changed": "MD&A attributes the $326.3 million increase in Optical Networking revenue primarily to sales of the Waveserver system and the 6500 Reconfigurable Line Systems.",
    "account": "Optical Networking revenue (Networking Platforms segment)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Optical Networking products revenue increased by $326.3 million, primarily driven by increases in sales of our Waveserver",
    "paragraph_id": "0001628280-26-040767:mdna:29",
    "explanation": false
  },
  {
    "id": "revenue_recognition_routing_switching_data_center_out_of_band_management",
    "what_changed": "MD&A attributes the $81.5 million increase in Routing and Switching revenue to the 3000 and 5000 series platforms and to 8100 Coherent IP platforms used in an out-of-band data center management (DCOM) solution. This names a data-center use as a driver.",
    "account": "Routing and Switching revenue (Networking Platforms segment)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "our 8100 Coherent IP networking platforms in our out-of-band data center management (DCOM) solution.",
    "paragraph_id": "0001628280-26-040767:mdna:30",
    "explanation": false
  },
  {
    "id": "revenue_recognition_platform_software_navigator_network_control_suite",
    "what_changed": "MD&A attributes the $8.4 million increase in Platform Software and Services revenue to sales of the Navigator Network Control Suite software.",
    "account": "Platform Software and Services revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Platform Software and Services segment revenue increased by $8.4 million, primarily reflecting a sales increase in our Navigator Network Control Suite (NCS) software solution.",
    "paragraph_id": "0001628280-26-040767:mdna:31",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_blue_planet_assurance_analytics_sales_decline",
    "what_changed": "MD&A says Blue Planet revenue decreased by $4.6 million and attributes this to lower sales of unified assurance and analytics software.",
    "account": "Blue Planet Automation Software and Services revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Blue Planet Automation Software and Services segment revenue decreased by $4.6 million, primarily reflecting a sales decrease in our unified assurance and analytics software.",
    "paragraph_id": "0001628280-26-040767:mdna:32",
    "explanation": false
  },
  {
    "id": "revenue_recognition_global_services_implementation_and_maintenance",
    "what_changed": "MD&A attributes the $33.3 million increase in Global Services revenue to implementation services and to maintenance, support and learning services.",
    "account": "Global Services revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Global Services segment revenue increased by $33.3 million, primarily reflecting sales increases in our implementation services and maintenance, support, and learning services.",
    "paragraph_id": "0001628280-26-040767:mdna:33",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_software_consulting_services_decline",
    "what_changed": "The six-month bullet for Platform Software and Services names an offset that the quarter bullet does not: lower sales of software consulting services.",
    "account": "Platform Software and Services revenue (services portion)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by sales decreases of our software consulting services.",
    "paragraph_id": "0001628280-26-040767:mdna:38",
    "explanation": false
  },
  {
    "id": "revenue_recognition_americas_cloud_and_service_provider_sales",
    "what_changed": "MD&A attributes the $368.4 million increase in Americas revenue to cloud provider and service provider customers in the United States.",
    "account": "Americas revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Americas revenue increased by $368.4 million, primarily driven by increased sales to cloud provider customers as well as service provider customers in the United States.",
    "paragraph_id": "0001628280-26-040767:mdna:49",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_netherlands_cloud_provider_sales_decrease",
    "what_changed": "The quarter EMEA bullet says EMEA revenue increased by $4.5 million on sales in France, partially offset by lower sales to cloud provider customers in the Netherlands.",
    "account": "EMEA revenue (cloud provider customers in the Netherlands)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by decreased sales to cloud provider customers in the Netherlands.",
    "paragraph_id": "0001628280-26-040767:mdna:50",
    "explanation": false
  },
  {
    "id": "revenue_recognition_netherlands_cloud_provider_direction_contrast",
    "what_changed": "The six-month EMEA bullet attributes the $47.1 million EMEA increase primarily to higher sales to cloud provider customers in the Netherlands. The quarter bullet (mdna:50) says Netherlands cloud provider sales decreased. This is a contrast between two pieces of prose, left for the supervisor.",
    "account": "EMEA revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "EMEA revenue increased by $47.1 million, primarily driven by increased sales to cloud provider customers in the Netherlands and increased sales in France.",
    "paragraph_id": "0001628280-26-040767:mdna:54",
    "explanation": false
  },
  {
    "id": "revenue_recognition_apac_india_service_provider_and_australia_enterprise",
    "what_changed": "MD&A attributes the $72.0 million increase in APAC revenue to service provider customers in India and enterprise customers in Australia.",
    "account": "APAC revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "APAC revenue increased by $72.0 million, primarily driven by increased sales to service provider customers in India and enterprise customers in Australia.",
    "paragraph_id": "0001628280-26-040767:mdna:51",
    "explanation": false
  },
  {
    "id": "revenue_recognition_apac_singapore_cloud_provider_sales",
    "what_changed": "The six-month APAC bullet ($61.5 million increase) names cloud provider customers in Singapore as a driver. The quarter APAC bullet does not name them.",
    "account": "APAC revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "cloud provider customers in Singapore",
    "paragraph_id": "0001628280-26-040767:mdna:55",
    "explanation": false
  },
  {
    "id": "earnings_quality_currency_effect_on_revenue_minimal",
    "what_changed": "MD&A says about 9% of revenue was non-U.S. Dollar-denominated in both the quarter and the six months. It says the U.S. Dollar generally weakened, with minimal impact.",
    "account": "Revenue",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the U.S. Dollar generally weakened against other currencies with minimal impact.",
    "paragraph_id": "0001628280-26-040767:mdna:57",
    "explanation": false
  },
  {
    "id": "earnings_quality_gross_margin_fluctuation_factors_list",
    "what_changed": "insufficient: this paragraph is carried as changed from the prior period, but the prior wording is not in my input, so I cannot say which factor was added or dropped. It now lists four factors: technology-based price changes, product and service mix, product lifecycle stage, and cost reductions.",
    "account": "Gross margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Gross margin can fluctuate due to a number of factors, including technology-based price changes, product and service mix, the lifecycle stage of our products and cost reductions.",
    "paragraph_id": "0001628280-26-040767:mdna:62",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_lower_manufacturing_efficiencies",
    "what_changed": "MD&A attributes the 510 basis point increase in product gross margin to cost reduction, pricing optimization and product mix. It names lower manufacturing efficiencies as a partial offset.",
    "account": "Products gross margin; products cost of goods sold",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Product gross margin increased by 510 basis points, primarily due to cost reduction, pricing optimization, and product mix, partially offset by lower manufacturing efficiencies.",
    "paragraph_id": "0001628280-26-040767:mdna:70",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_services_margin_less_favorable_mix",
    "what_changed": "MD&A says services gross margin decreased by 110 basis points because of a less favorable services mix, partly offset by better margins on implementation services.",
    "account": "Services gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Services gross margin decreased by 110 basis points, primarily due to a less favorable services mix, partially offset by improved margins on implementation services.",
    "paragraph_id": "0001628280-26-040767:mdna:71",
    "explanation": false
  },
  {
    "id": "earnings_quality_research_expense_nubis_acquisition_headcount",
    "what_changed": "MD&A attributes the $23.0 million increase in R&D, net of hedging, to higher headcount, including staff from the Nubis Communications acquisition, and to technology and engineering design costs.",
    "account": "Research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Research and development expense increased by $23.0 million. Net of hedging, this primarily reflects higher employee headcount and related costs, including from our acquisition of Nubis Communications",
    "paragraph_id": "0001628280-26-040767:mdna:83",
    "explanation": false
  },
  {
    "id": "earnings_quality_selling_and_marketing_employee_compensation",
    "what_changed": "MD&A attributes the $10.4 million increase in selling and marketing expense to employee-related compensation costs.",
    "account": "Selling and marketing expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Selling and marketing expense increased by $10.4 million, which primarily reflects increases in employee-related compensation costs.",
    "paragraph_id": "0001628280-26-040767:mdna:84",
    "explanation": false
  },
  {
    "id": "earnings_quality_general_and_administrative_employee_compensation",
    "what_changed": "MD&A attributes the $4.3 million increase in general and administrative expense to employee-related compensation costs.",
    "account": "General and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "General and administrative expense increased by $4.3 million, which primarily reflects increases in employee-related compensation costs.",
    "paragraph_id": "0001628280-26-040767:mdna:85",
    "explanation": false
  },
  {
    "id": "earnings_quality_intangible_amortization_assets_reaching_end_of_lives",
    "what_changed": "MD&A says operating-expense amortization of intangibles decreased by $2.8 million because certain intangible assets reached the end of their economic lives.",
    "account": "Amortization of intangible assets (operating expense)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Amortization of intangible assets decreased by $2.8 million, primarily reflecting certain intangible assets having reached the end of their economic lives.",
    "paragraph_id": "0001628280-26-040767:mdna:87",
    "explanation": false
  },
  {
    "id": "earnings_quality_general_and_administrative_professional_services",
    "what_changed": "The six-month G&A bullet ($9.6 million increase) names professional services as a driver alongside employee compensation. The quarter bullet does not mention professional services.",
    "account": "General and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "General and administrative expense increased by $9.6 million, which primarily reflects increases in employee-related compensation costs and professional services.",
    "paragraph_id": "0001628280-26-040767:mdna:91",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_costs_described_relatively_unchanged",
    "what_changed": "The six-month bullet calls significant asset impairments and restructuring costs 'relatively unchanged'. Whether the opex table supports that word is for the numbers reader to check.",
    "account": "Significant asset impairments and restructuring costs",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Significant asset impairments and restructuring costs remained relatively unchanged.",
    "paragraph_id": "0001628280-26-040767:mdna:92",
    "explanation": false
  },
  {
    "id": "earnings_quality_currency_effect_on_operating_expense_minimal",
    "what_changed": "MD&A says about 50% of operating expense was non-U.S. Dollar-denominated. It says the generally weaker U.S. Dollar, net of hedging, had minimal impact.",
    "account": "Operating expense",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "These currency fluctuations, net of hedging, had minimal impact.",
    "paragraph_id": "0001628280-26-040767:mdna:96",
    "explanation": false
  },
  {
    "id": "earnings_quality_networking_platforms_profit_volume_and_margin",
    "what_changed": "MD&A attributes the $210.1 million increase in Networking Platforms segment profit to higher volume and improved gross margin, partly offset by higher R&D.",
    "account": "Networking Platforms segment profit",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Networking Platforms segment profit increased by $210.1 million, primarily due to higher sales volume and improved gross margin as described above, partially offset by higher research and development costs.",
    "paragraph_id": "0001628280-26-040767:mdna:103",
    "explanation": false
  },
  {
    "id": "earnings_quality_platform_software_profit_product_volume_and_margin",
    "what_changed": "MD&A attributes the $9.4 million increase in Platform Software and Services segment profit to higher product sales volume and improved gross margin.",
    "account": "Platform Software and Services segment profit",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Platform Software and Services segment profit increased by $9.4 million, primarily due to higher product sales volume, as described above, and improved gross margin.",
    "paragraph_id": "0001628280-26-040767:mdna:104",
    "explanation": false
  },
  {
    "id": "earnings_quality_global_services_profit_sales_volume",
    "what_changed": "MD&A attributes the $12.0 million increase in Global Services segment profit to increased sales volume.",
    "account": "Global Services segment profit",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Global Services segment profit increased by $12.0 million, primarily due to increased sales volume as described above.",
    "paragraph_id": "0001628280-26-040767:mdna:106",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_platform_software_services_volume_lower",
    "what_changed": "The six-month bullet for Platform Software and Services segment profit ($5.7 million increase) names lower services sales volume and higher R&D as offsets. It describes gross margin as only 'slightly higher'.",
    "account": "Platform Software and Services services revenue and segment profit",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by lower services sales volume and increased research and development costs.",
    "paragraph_id": "0001628280-26-040767:mdna:109",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_blue_planet_margin_and_research_cost",
    "what_changed": "The six-month Blue Planet bullet attributes the segment result to lower software volume, reduced gross margins and higher R&D. Unlike the other segment-profit bullets, it gives no amount and no direction for segment profit. The quarter Blue Planet bullet (mdna:105) is carried unchanged from the prior filing's mdna:83.",
    "account": "Blue Planet Automation Software and Services segment profit (loss)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Blue Planet Automation Software and Services segment primarily reflects lower software sales volume as described above, reduced gross margins and increased research and development costs.",
    "paragraph_id": "0001628280-26-040767:mdna:110",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_income_foreign_exchange_remeasurement",
    "what_changed": "MD&A attributes the $6.2 million increase in interest and other income, net, to foreign exchange effects on assets and liabilities held in non-functional currencies, net of hedging. This is a non-operating source.",
    "account": "Interest and other income, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Interest and other income, net increased by $6.2 million, primarily reflecting the impact of foreign exchange rates on assets and liabilities denominated in a currency other than the relevant functional currency, net of hedging activity.",
    "paragraph_id": "0001628280-26-040767:mdna:119",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_expense_described_relatively_unchanged",
    "what_changed": "The quarter bullet calls interest expense 'relatively unchanged'. Checking that word against the numbers is left to the numbers reader.",
    "account": "Interest expense",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Interest expense remained relatively unchanged.",
    "paragraph_id": "0001628280-26-040767:mdna:120",
    "explanation": false
  },
  {
    "id": "earnings_quality_tax_provision_higher_pre_tax_income",
    "what_changed": "MD&A attributes the $2.8 million increase in the provision for income taxes to the increase in pre-tax book income.",
    "account": "Provision for income taxes",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Provision for income taxes increased by $2.8 million, primarily due to the increase in pre-tax book income.",
    "paragraph_id": "0001628280-26-040767:mdna:121",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_expense_lower_floating_rates",
    "what_changed": "MD&A attributes the $2.4 million six-month decrease in interest expense to lower rates on floating rate debt, net of hedging.",
    "account": "Interest expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Interest expense decreased by $2.4 million, primarily due to lower interest rates on our floating rate debt, net of hedging activity.",
    "paragraph_id": "0001628280-26-040767:mdna:124",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_foreign_cash_and_expected_repatriation",
    "what_changed": "insufficient as to whether the estimate moved: the paragraph is carried as changed, but the prior figures are not in my input. It now states $379.7 million of cash and short-term investments held by foreign subsidiaries. It says approximately $92.3 million of undistributed foreign earnings is expected to be repatriated, with a deferred tax liability accrued for that amount and the rest indefinitely reinvested.",
    "account": "Deferred tax liability; cash held by foreign subsidiaries",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Approximately $92.3 million of undistributed earnings from these foreign subsidiaries is expected to be repatriated, with any remaining amount continuing to be indefinitely reinvested.",
    "paragraph_id": "0001628280-26-040767:mdna:130",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_and_tax_withholding_settlements",
    "what_changed": "MD&A says $163.7 million was repurchased under the program in the first six months, with $506.7 million remaining. Separately, $179.4 million of shares were repurchased to settle employee tax withholding on vesting stock unit awards. The text contains a typo ('the the'), which is wording only.",
    "account": "Additional paid-in capital; cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "we also repurchased $179.4 million of our common stock in settlement of employee tax withholding obligations due upon the vesting of stock unit awards.",
    "paragraph_id": "0001628280-26-040767:mdna:131",
    "explanation": false
  },
  {
    "id": "earnings_quality_working_capital_consumed_operating_cash",
    "what_changed": "MD&A says that in the first six months, net income adjusted for non-cash charges provided $612.0 million and operating assets and liabilities used $124.7 million.",
    "account": "Net operating working capital (changes in operating assets and liabilities)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net income (adjusted for non-cash charges) provided cash of $612.0 million, offset by cash used in operating assets and liabilities of $124.7 million.",
    "paragraph_id": "0001628280-26-040767:mdna:137",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_change_sales_volume_and_collections",
    "what_changed": "MD&A attributes the change in accounts receivable mainly to increased sales volume, partly offset by improved cash collections.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The change in accounts receivable primarily reflects increased sales volume, partially offset by improved cash collections;",
    "paragraph_id": "0001628280-26-040767:mdna:145",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_finished_goods_build_supply_chain_volatility",
    "what_changed": "MD&A attributes the change in inventories mainly to holding more finished goods to mitigate supply chain volatility, partly offset by a reduction in raw materials.",
    "account": "Inventories (finished goods; raw materials)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The change in inventories primarily reflects increased finished good inventory to mitigate supply chain volatility, partially offset by reduction in raw materials;",
    "paragraph_id": "0001628280-26-040767:mdna:146",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_refundable_advances_to_contract_manufacturer",
    "what_changed": "MD&A attributes the change in prepaid expenses and other mainly to higher refundable cash advances to a third-party contract manufacturer and higher prepaid VAT. I flagged this as an explanation because the refundable advances are amounts recoverable from a supplier and are tied to inventory supply.",
    "account": "Prepaid expenses and other (refundable advances to contract manufacturer; prepaid VAT)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The change in prepaid expenses and other primarily reflects higher refundable cash advances to a third-party contract manufacturer and higher prepaid value-added tax (VAT);",
    "paragraph_id": "0001628280-26-040767:mdna:147",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_payables_accruals_incentive_compensation_timing",
    "what_changed": "MD&A attributes the change in accounts payable, accruals and other obligations mainly to the timing of annual incentive compensation payments, partly offset by the timing of supplier payments.",
    "account": "Accrued liabilities and other short-term obligations (compensation); accounts payable",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The change in accounts payable, accruals, and other obligations primarily reflects the timing of payments associated with our annual incentive compensation plan, partially offset by the timing of payments to suppliers;",
    "paragraph_id": "0001628280-26-040767:mdna:148",
    "explanation": false
  },
  {
    "id": "across_documents_purchase_commitments_firm_portion_wording",
    "what_changed": "MD&A (mdna:160 and mdna:161) says the only material change in contractual obligations since November 1, 2025 is $2.8 billion of purchase order obligations as of May 2, 2026. It says only a portion of that amount is firm, non-cancelable and unconditional. The note (notes:152) instead says Ciena may cancel, reschedule or adjust 'a portion' of the orders. The two texts describe the cancellable share from opposite ends, and neither quantifies it.",
    "account": "Purchase order commitments (off-balance sheet); inventories",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Consequently, only a portion of this amount relates to firm, non-cancelable and unconditional obligations.",
    "paragraph_id": "0001628280-26-040767:mdna:161",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_inventory_purchase_commitments_amount_restated",
    "what_changed": "The note now states $2.8 billion of outstanding purchase order commitments to contract manufacturers and component suppliers as of May 2, 2026. The prior filing's sentence (note history) stated $1.9 billion as of January 31, 2026. I make no comparison here. The rest of the paragraph is unchanged.",
    "account": "Purchase order commitments; inventories; accounts payable",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of May 2, 2026, Ciena had $2.8 billion in outstanding purchase order commitments to contract manufacturers and component suppliers for inventory.",
    "paragraph_id": "0001628280-26-040767:notes:152",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_environmental_credits_standard_added",
    "what_changed": "A newly issued standard is added: ASU 2026-02 (environmental credits and environmental credit obligations). It is effective for annual periods beginning after December 15, 2027, and Ciena says it is evaluating it. The ASU 2025-11 sentence in the same paragraph changed in wording only.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "beyond 12 months",
    "quote": "ASU 2026-02 is effective for annual reporting periods beginning after December 15, 2027 and interim reporting periods within those annual reporting periods.",
    "paragraph_id": "0001628280-26-040767:notes:11",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_over_time_revenue_row_relabelled_services_only",
    "what_changed": "In the disaggregated revenue tables, the timing row previously labelled 'Products and services transferred over time' is now 'Services transferred over time' (note history). The 'Segment' header row is dropped, and six-month tables are added.",
    "account": "Revenue by timing of recognition",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Services transferred over time",
    "paragraph_id": "0001628280-26-040767:notes:15",
    "explanation": false
  },
  {
    "id": "revenue_recognition_ten_percent_customer_table_now_two_cloud_providers",
    "what_changed": "The 10% customer table now lists Cloud provider A and Cloud provider B with amounts for fiscal 2026. It has a single 'Service provider' row with amounts only for the fiscal 2025 periods (n/a* for fiscal 2026). The prior filing's table (note history) listed 'Service provider A' as a 10% customer for the first quarter of fiscal 2026. No service provider now appears as a 10% customer for any fiscal 2026 period shown.",
    "account": "Revenue concentration (10% customers)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Service provider | n/a*",
    "paragraph_id": "0001628280-26-040767:notes:47",
    "explanation": false
  },
  {
    "id": "revenue_recognition_service_provider_all_segments_sentence_removed",
    "what_changed": "This sentence was removed: 'Service provider A purchased products from each of Ciena’s operating segments for the periods presented.' The remaining sentence now says the 10% customers in the table bought from Networking Platforms, Platform Software and Services, and Global Services. The prior text is in note history 0001628280-26-015152:note_history:36.",
    "account": "Revenue concentration (10% customers)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The 10% customers included in the table above purchased products from Ciena’s Networking Platforms, Platform Software and Services, and Global Services operating segments for each of the periods presented.",
    "paragraph_id": "0001628280-26-040767:notes:49",
    "explanation": false
  },
  {
    "id": "revenue_recognition_long_term_unbilled_software_license_receivables",
    "what_changed": "New sentence: long-term accounts receivable are unbilled receivables for non-cancellable software licenses that were recognized as revenue when made available to customers and will be billed in the future. The same note shows long-term accounts receivable of $21,265 thousand at May 2, 2026 and $28,610 thousand at November 1, 2025.",
    "account": "Long-term accounts receivable (unbilled)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Ciena’s long-term accounts receivable represent unbilled receivables attributable to non-cancellable software licenses recognized as revenue when made available to customers, to be billed in the future.",
    "paragraph_id": "0001628280-26-040767:notes:53",
    "explanation": true
  },
  {
    "id": "revenue_recognition_remaining_performance_obligations_conversion_percentage_dropped",
    "what_changed": "The prior note said Ciena expected approximately 85% of RPO to be recognized as revenue within the next 12 months. That sentence was removed (0001628280-26-015152:note_history:48). The note now says the majority will be satisfied within a year and the rest is typically recognized within three years, so a quantified 12-month conversion share is no longer given. RPO is now stated as $2.5 billion as of May 2, 2026; the prior text gave $2.3 billion as of January 31, 2026. I make no comparison.",
    "account": "Remaining performance obligations; revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The majority of Ciena’s performance obligations will be satisfied within a year and any remaining performance obligations are typically recognized within three years.",
    "paragraph_id": "0001628280-26-040767:notes:60",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_remaining_performance_obligations_supply_conditions",
    "what_changed": "New sentence in the RPO note: supply conditions can affect when remaining performance obligations are fulfilled. The prior RPO text had no such caveat.",
    "account": "Remaining performance obligations; revenue timing",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The timing of fulfillment of remaining performance obligations can be impacted by supply conditions.",
    "paragraph_id": "0001628280-26-040767:notes:60",
    "explanation": false
  },
  {
    "id": "earnings_quality_effective_tax_rate_lowered_by_share_compensation_benefit",
    "what_changed": "The income tax note now says the effective tax rate for the quarter and the six months was lower than a year earlier. It attributes this mainly to an income tax benefit from share-based compensation and a shift in the mix of earnings toward lower-tax jurisdictions.",
    "account": "Provision for income taxes; effective tax rate",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease was primarily due to an income tax benefit for share-based compensation expense and a change in mix of earnings in jurisdictions with lower tax rates.",
    "paragraph_id": "0001628280-26-040767:notes:71",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_provision_reduced_forecast_demand",
    "what_changed": "The note says the six-month provision for excess and obsolete inventory was $42.5 million, driven mainly by reductions in forecasted demand for certain products. Deductions from the reserve came mainly from sales and disposals. The six-month cause is stated alongside the MD&A's description of strong overall demand.",
    "account": "Reserve for inventory excess and obsolescence",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Ciena recorded a provision for inventory excess and obsolescence of $42.5 million, primarily driven by reductions in forecasted demand for certain products.",
    "paragraph_id": "0001628280-26-040767:notes:86",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_share_based_compensation_tax_rate_swings",
    "what_changed": "Added under tax contingencies: share-based compensation deductions are valued at vesting and can raise or lower the effective tax rate in the period they vest (note history marks this as added).",
    "account": "Effective tax rate; provision for income taxes",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "These deductions are valued at vesting for tax purposes and can increase or decrease the effective tax rate in the period in which they vest.",
    "paragraph_id": "0001628280-26-040767:notes:149",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_financial_officer_trading_plan",
    "what_changed": "New Rule 10b5-1 disclosure: CFO Marc D. Graff adopted a sales plan on March 25, 2026 that runs until May 22, 2027. It covers up to 33% of the net after-tax shares from scheduled vestings of 54,664 restricted stock units, and of performance stock units vesting December 20, 2026 (0% to 200% of 2,788 target shares) (notes:157).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Adoption (March 25, 2026) | Rule 10b5-1 trading arrangement | Sales",
    "paragraph_id": "0001628280-26-040767:notes:156",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tariff_ruling_disclosure_removed",
    "what_changed": "The prior subsequent-events note has been removed. It covered the February 20, 2026 Supreme Court ruling that some tariffs Ciena had been subject to were invalid, the replacement global tariff, and open questions about refunds. The current subsequent-events note covers only share repurchases. No current note text in my input mentions a tariff refund, receivable or resolution. MD&A paragraphs carried as same-as-prior could still discuss tariffs, but I cannot see them.",
    "account": "Cost of goods sold (tariffs); other receivables (potential tariff refunds)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On February 20, 2026, the U.S. Supreme Court ruled that a portion of the tariffs that Ciena has been subject to were invalid.",
    "paragraph_id": "0001628280-26-015152:note_history:51",
    "explanation": false
  },
  {
    "id": "results_against_expectations_headline_revenue_growth",
    "what_changed": "The release headline states revenue of $1.57 billion and describes it as up 40% year-over-year.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Fiscal second quarter 2026 revenue was $1.57 billion, up 40% year-over-year",
    "paragraph_id": "0001628280-26-040614:8k_2_02:6",
    "explanation": false
  },
  {
    "id": "earnings_quality_adjusted_earnings_per_share_growth",
    "what_changed": "The release headline states adjusted (non-GAAP) EPS of $1.64 and describes it as a 290% increase. The same release states GAAP diluted EPS of $1.49 (8k_2_02:17).",
    "account": "Adjusted (non-GAAP) diluted EPS",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "adjusted Earnings Per Share (EPS) was $1.64, an increase of 290% compared to fiscal second quarter 2025",
    "paragraph_id": "0001628280-26-040614:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_near_term_outlook",
    "what_changed": "The release gives third-quarter revenue guidance of $1.625 billion plus or minus $50 million. It does not characterize the direction against the reported quarter, so any comparison is for the numbers reader.",
    "account": "Revenue",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Providing revenue guidance for fiscal third quarter 2026 of $1.625 billion plus or minus $50 million",
    "paragraph_id": "0001628280-26-040614:8k_2_02:8",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_annual_outlook_raised",
    "what_changed": "The release says it is raising fiscal 2026 revenue guidance to $6.3 billion plus or minus $100 million, which it describes as a 32% year-over-year increase at the midpoint. The prior guidance figure is not in my input.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Raising revenue guidance for fiscal year 2026 to $6.3 billion plus or minus $100 million, a 32% increase YoY at the midpoint",
    "paragraph_id": "0001628280-26-040614:8k_2_02:9",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_dynamic_supply_environment",
    "what_changed": "The CEO quote describes 'disciplined execution in a dynamic supply environment' and ties the strategy to AI-driven demand across the WAN and in and around the data center.",
    "account": "Revenue; inventories",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "disciplined execution in a dynamic supply environment",
    "paragraph_id": "0001628280-26-040614:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "results_against_expectations_continued_earnings_expansion_confidence",
    "what_changed": "The CFO quote cites adjusted gross margin expansion and nearly fourfold growth in adjusted EPS. It states confidence that operating leverage will drive continued earnings expansion.",
    "account": "Operating income; adjusted EPS",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Our demonstrated ability to drive operating leverage gives us confidence in continued earnings expansion and long-term value creation for customers and shareholders.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:12",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_near_term_outlook",
    "what_changed": "The release guides third-quarter adjusted (non-GAAP) gross margin to 45% plus or minus 50 bps. It gives no stated direction.",
    "account": "Adjusted (non-GAAP) gross margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Adjusted (non-GAAP) gross margin in the range of 45% plus or minus 50 bps",
    "paragraph_id": "0001628280-26-040614:8k_2_02:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_operating_expense_near_term_outlook",
    "what_changed": "The release guides third-quarter adjusted (non-GAAP) operating expense to $410 million plus or minus $10 million. It gives no stated direction.",
    "account": "Adjusted (non-GAAP) operating expense",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Adjusted (non-GAAP) operating expense in the range of $410 million plus or minus $10 million",
    "paragraph_id": "0001628280-26-040614:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_operating_margin_near_term_outlook",
    "what_changed": "The release guides third-quarter adjusted (non-GAAP) operating margin to between 19% and 20%. It gives no stated direction.",
    "account": "Adjusted (non-GAAP) operating margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Adjusted (non-GAAP) operating margin between 19% and 20%",
    "paragraph_id": "0001628280-26-040614:8k_2_02:26",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_annual_outlook",
    "what_changed": "The release guides fiscal 2026 adjusted (non-GAAP) gross margin to between 44.5% and 45%. It does not say whether this figure was changed from earlier guidance.",
    "account": "Adjusted (non-GAAP) gross margin",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Adjusted (non-GAAP) gross margin between 44.5% and 45%",
    "paragraph_id": "0001628280-26-040614:8k_2_02:29",
    "explanation": false
  },
  {
    "id": "results_against_expectations_operating_expense_annual_outlook",
    "what_changed": "The release guides fiscal 2026 adjusted (non-GAAP) operating expense to $1.61 billion plus or minus $20 million. It does not say whether this figure was changed.",
    "account": "Adjusted (non-GAAP) operating expense",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Adjusted (non-GAAP) operating expense in the range of $1.61 billion plus or minus $20 million",
    "paragraph_id": "0001628280-26-040614:8k_2_02:30",
    "explanation": false
  },
  {
    "id": "results_against_expectations_operating_margin_annual_outlook",
    "what_changed": "The release guides fiscal 2026 adjusted (non-GAAP) operating margin to 19% plus or minus 50bps. It does not say whether this figure was changed.",
    "account": "Adjusted (non-GAAP) operating margin",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Adjusted (non-GAAP) operating margin in the range of 19% plus or minus 50bps",
    "paragraph_id": "0001628280-26-040614:8k_2_02:31",
    "explanation": false
  },
  {
    "id": "across_documents_two_customers_combined_share_of_revenue",
    "what_changed": "The release says two customers each accounted for 10%-plus of revenue, together 34.0% of revenue. The 10-Q note (notes:47) identifies them as Cloud provider A and Cloud provider B. Reconciling the two is for the numbers reader.",
    "account": "Revenue concentration (10% customers)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Two customers represented 10%-plus of revenue for a total of 34.0% of revenue.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:33",
    "explanation": false
  },
  {
    "id": "earnings_quality_days_sales_outstanding_reported",
    "what_changed": "The release states average DSO of 71 days. MD&A (mdna:145) attributes the receivables change to sales volume, partly offset by improved collections. Reconciling the DSO level with that wording is for the numbers reader.",
    "account": "Accounts receivable, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Average days' sales outstanding (DSOs) were 71.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:34",
    "explanation": false
  },
  {
    "id": "earnings_quality_inventory_turns_reported",
    "what_changed": "The release states inventory turns of 3.6. MD&A (mdna:146) says finished goods were increased to mitigate supply chain volatility, and the note (notes:86) cites lower forecast demand for certain products.",
    "account": "Inventories, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Inventory turns were 3.6.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:35",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_buyback_shares_repurchased_under_program",
    "what_changed": "The release says about 0.2 million shares were repurchased in the quarter for $83.1 million under the $1 billion program.",
    "account": "Cash and cash equivalents; additional paid-in capital",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Repurchased approximately 0.2 million shares of common stock for an aggregate price of $83.1 million under the $1 billion share repurchase program.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:36",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_supply_chain_cost_and_lead_time_risk",
    "what_changed": "The release's risk list names supply chain constraints or disruptions, including increased costs and lead times. It also names AI's effect on networking spend and the imposition of tariffs, and points to risk factors in the forthcoming 10-Q. I have no Item 1A diff to check this against.",
    "account": "Cost of goods sold; inventories",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "supply chain constraints or disruptions including increased costs and lead times",
    "paragraph_id": "0001628280-26-040614:8k_2_02:46",
    "explanation": false
  },
  {
    "id": "earnings_quality_holdback_arrangement_excluded_from_adjusted_results",
    "what_changed": "The release adds a 'Holdback arrangement' adjustment ($2,411 thousand in the quarter; shown as a dash for the prior-year quarter) to adjusted operating expense and adjusted EBITDA (Appendices A and B). It is the part of the Nubis Communications merger consideration withheld from key employee shareholders. Under GAAP it is treated as contingent compensation, and it is excluded from non-GAAP results.",
    "account": "Operating expense (GAAP-only compensation charge); adjusted EBITDA",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "reflects a one-time holdback of a portion of the merger consideration otherwise payable at closing to certain key employee shareholders of Nubis Communications, Inc. who became employees of Ciena, which is treated as contingent compensation for GAAP reporting purposes.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:77",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_tax_rate_assumption",
    "what_changed": "The release says the non-GAAP tax provision uses a blended statutory rate of 20% for the second quarter of fiscal 2026 and 22% for the second quarter of fiscal 2025. It adds that the rate may change with tax policy or tax strategy. I make no comparison; the GAAP effective tax rate narrative is at notes:71.",
    "account": "Non-GAAP tax provision; adjusted net income",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "utilizes a current, blended U.S. and foreign statutory annual tax rate of 20% for the second quarter of fiscal 2026 and 22% for the second quarter of fiscal 2025.",
    "paragraph_id": "0001628280-26-040614:8k_2_02:78",
    "explanation": false
  }
]
```

Items marked `insufficient`: `earnings_quality_gross_margin_fluctuation_factors_list` and `liquidity_and_capital_foreign_cash_and_expected_repatriation` (only as to whether the repatriation estimate moved).

## Paragraphs carried as text that I did not make an item of

### 8-K, item 2.02 (exhibit 99.1)

- 0001628280-26-040614:8k_2_02:1 — exhibit file header, no content
- 0001628280-26-040614:8k_2_02:2 — title fragment
- 0001628280-26-040614:8k_2_02:3 — release header
- 0001628280-26-040614:8k_2_02:4 — release title
- 0001628280-26-040614:8k_2_02:5 — section header
- 0001628280-26-040614:8k_2_02:10 — dateline (date only)
- 0001628280-26-040614:8k_2_02:13 — section header
- 0001628280-26-040614:8k_2_02:14 — section header
- 0001628280-26-040614:8k_2_02:15 — amounts only; repeats revenue in 8k_2_02:6
- 0001628280-26-040614:8k_2_02:16 — section header
- 0001628280-26-040614:8k_2_02:17 — amounts only (GAAP and adjusted EPS); cited in the adjusted EPS item
- 0001628280-26-040614:8k_2_02:18 — table description
- 0001628280-26-040614:8k_2_02:19 — amounts only (GAAP/non-GAAP summary table)
- 0001628280-26-040614:8k_2_02:20 — table footnote
- 0001628280-26-040614:8k_2_02:21 — section header
- 0001628280-26-040614:8k_2_02:22 — lead-in to guidance
- 0001628280-26-040614:8k_2_02:23 — repeats the 8k_2_02:8 revenue guidance; typo "$1.625B billion", wording only
- 0001628280-26-040614:8k_2_02:27 — lead-in to guidance
- 0001628280-26-040614:8k_2_02:28 — repeats the 8k_2_02:9 revenue guidance
- 0001628280-26-040614:8k_2_02:32 — section header
- 0001628280-26-040614:8k_2_02:37 — section header
- 0001628280-26-040614:8k_2_02:38 — amounts only (segment revenue table)
- 0001628280-26-040614:8k_2_02:39 — table footnote
- 0001628280-26-040614:8k_2_02:40 — section header
- 0001628280-26-040614:8k_2_02:41 — posting of supplemental materials, procedural
- 0001628280-26-040614:8k_2_02:42 — webcast logistics, procedural
- 0001628280-26-040614:8k_2_02:43 — page number
- 0001628280-26-040614:8k_2_02:44 — section header
- 0001628280-26-040614:8k_2_02:45 — forward-looking boilerplate that repeats the CEO/CFO quotes itemized at 8k_2_02:11 and 8k_2_02:12
- 0001628280-26-040614:8k_2_02:47 — standard non-GAAP presentation boilerplate
- 0001628280-26-040614:8k_2_02:48 — standard statement that guidance cannot be reconciled to GAAP
- 0001628280-26-040614:8k_2_02:49 — company description boilerplate
- 0001628280-26-040614:8k_2_02:50 — page number
- 0001628280-26-040614:8k_2_02:51 — statement header
- 0001628280-26-040614:8k_2_02:52 — statement header
- 0001628280-26-040614:8k_2_02:53 — statement header
- 0001628280-26-040614:8k_2_02:54 — statement header
- 0001628280-26-040614:8k_2_02:55 — amounts only (income statement)
- 0001628280-26-040614:8k_2_02:56 — amounts only (dilutive share footnote)
- 0001628280-26-040614:8k_2_02:57 — statement header
- 0001628280-26-040614:8k_2_02:58 — statement header
- 0001628280-26-040614:8k_2_02:59 — statement header
- 0001628280-26-040614:8k_2_02:60 — statement header
- 0001628280-26-040614:8k_2_02:61 — amounts only (balance sheet)
- 0001628280-26-040614:8k_2_02:62 — page number
- 0001628280-26-040614:8k_2_02:63 — statement header
- 0001628280-26-040614:8k_2_02:64 — statement header
- 0001628280-26-040614:8k_2_02:65 — statement header
- 0001628280-26-040614:8k_2_02:66 — statement header
- 0001628280-26-040614:8k_2_02:67 — amounts only (cash flow statement)
- 0001628280-26-040614:8k_2_02:68 — amounts only (Appendix A); the holdback line is covered by the item at 8k_2_02:77
- 0001628280-26-040614:8k_2_02:69 — amounts only (dilutive share footnote)
- 0001628280-26-040614:8k_2_02:70 — page number
- 0001628280-26-040614:8k_2_02:71 — amounts only (Appendix B); the holdback add-back is covered by the item at 8k_2_02:77
- 0001628280-26-040614:8k_2_02:72 — separator
- 0001628280-26-040614:8k_2_02:73 — lead-in to adjustment definitions
- 0001628280-26-040614:8k_2_02:74 — standard definition of the share-based compensation adjustment
- 0001628280-26-040614:8k_2_02:75 — standard definition of the restructuring adjustment
- 0001628280-26-040614:8k_2_02:76 — standard definition of the amortization adjustment

### Item 4

- 0001628280-26-040767:item_4_controls:1 — header
- 0001628280-26-040767:item_4_controls:2 — header
- 0001628280-26-040767:item_4_controls:3 — page number
- 0001628280-26-040767:item_4_controls:4 — standard conclusion that disclosure controls are effective; no change in substance visible
- 0001628280-26-040767:item_4_controls:5 — header
- 0001628280-26-040767:item_4_controls:6 — standard statement of no material ICFR change; no change in substance visible

### MD&A

- 0001628280-26-040767:mdna:23 — amounts only (segment revenue table)
- 0001628280-26-040767:mdna:27 — section header, date rolled forward
- 0001628280-26-040767:mdna:28 — amounts only (Networking Platforms total); drivers itemized at mdna:29 and mdna:30
- 0001628280-26-040767:mdna:34 — section header, date rolled forward
- 0001628280-26-040767:mdna:35 — amounts only
- 0001628280-26-040767:mdna:36 — six-month repeat of the mdna:29 driver; no new substance
- 0001628280-26-040767:mdna:37 — six-month repeat of the mdna:30 driver; no new substance
- 0001628280-26-040767:mdna:39 — six-month repeat of the mdna:32 driver; no new substance
- 0001628280-26-040767:mdna:40 — six-month repeat of the mdna:33 driver; no new substance
- 0001628280-26-040767:mdna:44 — amounts only (geographic table)
- 0001628280-26-040767:mdna:48 — section header, date rolled forward
- 0001628280-26-040767:mdna:52 — section header, date rolled forward
- 0001628280-26-040767:mdna:53 — six-month repeat of the mdna:49 driver; no new substance
- 0001628280-26-040767:mdna:64 — amounts only (gross margin table)
- 0001628280-26-040767:mdna:68 — section header, date rolled forward
- 0001628280-26-040767:mdna:69 — summary of the drivers itemized at mdna:70 and mdna:71
- 0001628280-26-040767:mdna:72 — section header, date rolled forward
- 0001628280-26-040767:mdna:73 — six-month repeat of the mdna:69 summary
- 0001628280-26-040767:mdna:74 — six-month repeat of the mdna:70 driver
- 0001628280-26-040767:mdna:75 — six-month repeat of the mdna:71 driver
- 0001628280-26-040767:mdna:78 — amounts only (operating expense table)
- 0001628280-26-040767:mdna:82 — section header, date rolled forward
- 0001628280-26-040767:mdna:88 — section header, date rolled forward
- 0001628280-26-040767:mdna:89 — six-month repeat of the mdna:83 driver
- 0001628280-26-040767:mdna:90 — six-month repeat of the mdna:84 driver
- 0001628280-26-040767:mdna:93 — six-month repeat of the mdna:87 driver
- 0001628280-26-040767:mdna:99 — amounts only (segment profit table)
- 0001628280-26-040767:mdna:102 — section header, date rolled forward
- 0001628280-26-040767:mdna:107 — section header, date rolled forward
- 0001628280-26-040767:mdna:108 — six-month repeat of the mdna:103 driver
- 0001628280-26-040767:mdna:111 — six-month repeat of the mdna:106 driver
- 0001628280-26-040767:mdna:114 — amounts only (non-operating table)
- 0001628280-26-040767:mdna:116 — table footnote
- 0001628280-26-040767:mdna:117 — table footnote
- 0001628280-26-040767:mdna:118 — section header, date rolled forward
- 0001628280-26-040767:mdna:122 — section header, date rolled forward
- 0001628280-26-040767:mdna:123 — six-month repeat of the mdna:119 driver
- 0001628280-26-040767:mdna:126 — six-month repeat of the mdna:121 driver
- 0001628280-26-040767:mdna:129 — amounts and dates rolled forward (revolver terms, letters of credit, no borrowings)
- 0001628280-26-040767:mdna:134 — amounts only (cash and investments table)
- 0001628280-26-040767:mdna:135 — amounts only; restates cash flow components already covered by the mdna:14 and mdna:131 items
- 0001628280-26-040767:mdna:140 — amounts only (non-cash adjustments table)
- 0001628280-26-040767:mdna:142 — restates the working-capital total itemized at mdna:137
- 0001628280-26-040767:mdna:143 — amounts only (working-capital table)
- 0001628280-26-040767:mdna:144 — lead-in
- 0001628280-26-040767:mdna:153 — amounts only (interest paid table)
- 0001628280-26-040767:mdna:154 — term loan rate at quarter end rolled forward
- 0001628280-26-040767:mdna:156 — swap terms restated; no new swap or term visible
- 0001628280-26-040767:mdna:157 — period rolled forward (revolver usage, nominal fees)
- 0001628280-26-040767:mdna:160 — lead-in to mdna:161; covered by the across-documents purchase-commitment item

### Notes

- 0001628280-26-040767:notes:7 — ASU 2023-09 standard text; not in note history, no change in substance visible
- 0001628280-26-040767:notes:8 — ASU 2024-03 standard text; not in note history, no change in substance visible
- 0001628280-26-040767:notes:9 — ASU 2025-05 standard text; not in note history, no change in substance visible
- 0001628280-26-040767:notes:10 — ASU 2025-06 standard text; not in note history, no change in substance visible
- 0001628280-26-040767:notes:14 — wording only ("periods indicated")
- 0001628280-26-040767:notes:16 — amounts only; the row relabel is covered by the notes:15 item
- 0001628280-26-040767:notes:17 — amounts only (six-month table added, period expansion)
- 0001628280-26-040767:notes:18 — amounts only (six-month table added, period expansion)
- 0001628280-26-040767:notes:20 — wording only ("AI" spelled out)
- 0001628280-26-040767:notes:42 — wording only ("using" for "in")
- 0001628280-26-040767:notes:44 — amounts only (geographic table)
- 0001628280-26-040767:notes:45 — amounts rolled forward (U.S. revenue; no other 10% country)
- 0001628280-26-040767:notes:51 — wording only (comma)
- 0001628280-26-040767:notes:52 — amounts only
- 0001628280-26-040767:notes:54 — wording only ("in" for "on")
- 0001628280-26-040767:notes:55 — amounts and period rolled forward (deferred revenue recognized)
- 0001628280-26-040767:notes:57 — amounts only (deferred revenue table)
- 0001628280-26-040767:notes:59 — amounts and period rolled forward; wording trimmed
- 0001628280-26-040767:notes:62 — period rolled forward (six months ended May 2, 2026)
- 0001628280-26-040767:notes:63 — amounts only (restructuring rollforward)
- 0001628280-26-040767:notes:65 — period rolled forward
- 0001628280-26-040767:notes:66 — amounts only
- 0001628280-26-040767:notes:68 — amounts only (interest and other income table)
- 0001628280-26-040767:notes:72 — heading and lead-in
- 0001628280-26-040767:notes:73 — amounts only
- 0001628280-26-040767:notes:74 — amounts only
- 0001628280-26-040767:notes:75 — date rolled forward
- 0001628280-26-040767:notes:76 — amounts only
- 0001628280-26-040767:notes:78 — amounts only
- 0001628280-26-040767:notes:81 — amounts only
- 0001628280-26-040767:notes:85 — amounts only (inventory table)
- 0001628280-26-040767:notes:89 — amounts only (accrued liabilities table)
- 0001628280-26-040767:notes:92 — amounts only (warranty rollforward)
- 0001628280-26-040767:notes:95 — amounts and dates rolled forward (cash flow hedge notional)
- 0001628280-26-040767:notes:96 — amounts and dates rolled forward (net investment hedge notional)
- 0001628280-26-040767:notes:97 — amounts and dates rolled forward (balance sheet hedge notional)
- 0001628280-26-040767:notes:100 — date rolled forward
- 0001628280-26-040767:notes:101 — date rolled forward
- 0001628280-26-040767:notes:104 — heading
- 0001628280-26-040767:notes:105 — heading
- 0001628280-26-040767:notes:106 — description of the existing term loan; no new term
- 0001628280-26-040767:notes:107 — lead-in
- 0001628280-26-040767:notes:108 — amounts only
- 0001628280-26-040767:notes:109 — period rolled forward
- 0001628280-26-040767:notes:110 — amount and date rolled forward (term loan fair value)
- 0001628280-26-040767:notes:111 — heading
- 0001628280-26-040767:notes:112 — heading
- 0001628280-26-040767:notes:113 — description of the existing notes; no new term
- 0001628280-26-040767:notes:114 — lead-in
- 0001628280-26-040767:notes:115 — amounts only
- 0001628280-26-040767:notes:116 — period rolled forward
- 0001628280-26-040767:notes:117 — amount and date rolled forward (notes fair value)
- 0001628280-26-040767:notes:118 — heading, period rolled forward
- 0001628280-26-040767:notes:119 — amounts only (AOCI rollforward)
- 0001628280-26-040767:notes:120 — lead-in, period rolled forward
- 0001628280-26-040767:notes:121 — amounts only
- 0001628280-26-040767:notes:125 — amounts only (EPS table)
- 0001628280-26-040767:notes:128 — amounts rolled forward; covered by the mdna:131 and 8k_2_02:36 items
- 0001628280-26-040767:notes:130 — amounts rolled forward; covered by the mdna:131 item
- 0001628280-26-040767:notes:132 — amounts only (share-based compensation table)
- 0001628280-26-040767:notes:134 — amounts rolled forward (unrecognized share-based compensation)
- 0001628280-26-040767:notes:137 — list of CODM exclusions; no new exclusion identifiable from my input
- 0001628280-26-040767:notes:138 — amounts only (segment table)
- 0001628280-26-040767:notes:140 — amounts rolled forward
- 0001628280-26-040767:notes:141 — lead-in
- 0001628280-26-040767:notes:142 — amounts only
- 0001628280-26-040767:notes:145 — amounts only (long-lived assets by country)
- 0001628280-26-040767:notes:146 — table footnote
- 0001628280-26-040767:notes:147 — heading
- 0001628280-26-040767:notes:148 — standard tax-contingency statement; not changed in note history
- 0001628280-26-040767:notes:150 — heading
- 0001628280-26-040767:notes:151 — wording only: re-segmentation; the prior text, split across note_history:2 and note_history:4, reads the same
- 0001628280-26-040767:notes:153 — heading
- 0001628280-26-040767:notes:154 — amounts and dates rolled forward (repurchases after quarter end)
- 0001628280-26-040767:notes:155 — lead-in to the trading-arrangement table
- 0001628280-26-040767:notes:157 — detail of the notes:156 arrangement; covered by that item

## Note change history — where each entry landed (not a second list)

- note_history:1 (added) → notes:149, item `estimates_and_discretion_share_based_compensation_tax_rate_swings`
- note_history:2 (changed) and 0001628280-26-015152:note_history:4 (removed) → notes:151, re-segmentation only
- note_history:3 (changed) → notes:152, item `liquidity_and_capital_inventory_purchase_commitments_amount_restated`
- note_history:5 (added) and 0001628280-26-015152:note_history:6 (removed) → notes:11, item `structure_and_disclosure_changes_environmental_credits_standard_added`; the ASU 2025-11 change is wording only
- note_history:7 and note_history:15 → notes:108, amounts only
- note_history:8 → notes:109, period rolled forward
- note_history:9 → notes:110, amount and date rolled forward
- note_history:10 and note_history:16 → notes:115, amounts only
- note_history:11 → notes:116, period rolled forward
- note_history:12 → notes:117, amount and date rolled forward
- note_history:13 → notes:73, amounts only
- note_history:14 → notes:75, date rolled forward
- note_history:17 and note_history:25 → notes:14, wording only
- note_history:18 and note_history:26 → notes:15, item `structure_and_disclosure_changes_over_time_revenue_row_relabelled_services_only`
- note_history:19 and note_history:27 → notes:16, amounts only (same relabel)
- note_history:20 and note_history:28 → notes:17, amounts only
- note_history:21 and note_history:29 → notes:18, amounts only
- note_history:22 and note_history:33 → notes:44, amounts only
- note_history:23 and note_history:35 (added), 0001628280-26-015152:note_history:24 and :46 (removed) → notes:47, item `revenue_recognition_ten_percent_customer_table_now_two_cloud_providers`
- note_history:30 → notes:20, wording only
- note_history:31 (changed: "the services portion") → wording only. The notes file carries this paragraph as same-as-prior, so the history and the notes file disagree on a one-word change.
- note_history:32 → notes:42, wording only
- note_history:34 (added) and 0001628280-26-015152:note_history:45 (removed) → notes:45, amounts rolled forward
- note_history:36 → notes:49, item `revenue_recognition_service_provider_all_segments_sentence_removed`
- note_history:37 → notes:51, wording only
- note_history:38 → notes:52, amounts only
- note_history:39 (added) → notes:53, item `revenue_recognition_long_term_unbilled_software_license_receivables`
- note_history:40 → notes:54, wording only
- note_history:41 → notes:55, amounts and period rolled forward
- note_history:42 → notes:57, amounts only
- note_history:43 → notes:59, amounts and period rolled forward
- note_history:44 (added) and 0001628280-26-015152:note_history:47 and :48 (removed) → notes:60, items `revenue_recognition_remaining_performance_obligations_conversion_percentage_dropped` and `narrative_signs_of_operating_pressure_remaining_performance_obligations_supply_conditions`
- note_history:49 → notes:154, amounts and dates rolled forward
- 0001628280-26-015152:note_history:50 and :51 (removed) → item `related_parties_contingencies_and_subsequent_events_tariff_ruling_disclosure_removed`
