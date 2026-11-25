# Notes text reader — Apple, quarterly report for the third quarter of fiscal 2026 (quarter ended June 27, 2026)

## What I read

All six input files, start to finish:
- the current-report bodies: the earnings release of July 30, 2026, plus the list of item codes and late-filing notices
- the controls and procedures item
- the MD&A diff
- the notes diff
- the note change history
- my prior flags (none on record)

**Missing from the input.** My directory has no auditor's report, no risk-factor diff, no subsidiaries exhibit diff and no material-contract exhibit. The controls file's title mentions the auditor's report, but the file only holds the controls and procedures item.

**Officer-change filing with no body.** The item-code list shows an officer-change current report dated April 20, 2026. That date falls inside the third quarter of fiscal 2026, but the report's body is not in my input, so I cannot say what it covers. No late-filing notices are listed.

**Nothing forbidden.** My directory holds no trend table, prices, returns, short interest, other company's files, prior probabilities or outcome window. The release does include the condensed statements as part of its body.

**How I worked:**
- I did no arithmetic. Every amount appears exactly as printed, and I say nothing about whether one amount is larger than another.
- The MD&A and controls inputs do not carry the prior quarter's wording. Where a paragraph appears as changed text without prior wording, the item says what it states now.

**Counts:**
- Items: 54
- Items marked insufficient: 1
- Items with the management-explanation flag set to true: 0. No changed paragraph has management explaining the cause of a receivables, inventory or reserve figure. Paragraphs that mention receivables or reserves only state concentrations or tax-rate drivers.

## Items

```json
[
  {
    "id": "results_against_expectations_release_record_june_quarter_revenue_and_earnings_per_share",
    "what_changed": "The earnings release for the third quarter of fiscal 2026 opens by claiming June quarter records for total company revenue and earnings per share. This is new release text; the prior release is not in my input.",
    "account": "Total net sales; diluted earnings per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "June quarter records for total company revenue and EPS",
    "paragraph_id": "0000320193-26-000018:8k_2_02:5",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_iphone_mac_services_june_quarter_records",
    "what_changed": "The release says iPhone, Mac and Services revenue each set new June quarter records. The claim does not name iPad or Wearables, Home and Accessories.",
    "account": "iPhone, Mac and Services net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "iPhone, Mac and Services revenue set new June quarter records",
    "paragraph_id": "0000320193-26-000018:8k_2_02:6",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_revenue_and_diluted_earnings_per_share_growth",
    "what_changed": "The release states quarterly revenue of $109.4 billion, up 16 percent year over year, and diluted earnings per share of $2.02, up 29 percent year over year.",
    "account": "Total net sales; diluted earnings per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The Company posted quarterly revenue of $109.4 billion, up 16 percent year over year.",
    "paragraph_id": "0000320193-26-000018:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "earnings_quality_release_tariff_refund_benefit_to_gross_margin",
    "what_changed": "The release attributes part of the quarter's margin to tariff refunds: company gross margin of 50.1 percent includes a favorable impact of approximately 2 percentage points from tariff refunds. The release does not say whether further refunds are expected in later quarters.",
    "account": "Gross margin percentage; products cost of sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Company gross margin was 50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds.",
    "paragraph_id": "0000320193-26-000018:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "across_documents_tariff_refund_amount_stated_in_release_only",
    "what_changed": "The release puts a figure on the tariff-refund benefit: $0.11 of diluted earnings per share, and about two points of gross margin. In the quarterly report, two changed paragraphs in my input mention tariff refunds: the MD&A tariff paragraph and the products gross margin paragraph. Both name refunds as a cause and say refunds received are recorded as a reduction of products cost of sales, but neither gives an amount. Whether an unchanged paragraph gives one is outside my input.",
    "account": "Products cost of sales; diluted earnings per share",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "and included a favorable impact of $0.11 from tariff refunds",
    "paragraph_id": "0000320193-26-000018:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_double_digit_growth_in_every_geographic_segment",
    "what_changed": "In the release, the chief executive claims double-digit revenue growth across iPhone, Mac and Services and in every geographic segment. Checking whether each segment and category clears that bar is left to the numbers reader and the supervisor.",
    "account": "Net sales by category and by reportable segment",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "with double-digit revenue growth across iPhone, Mac and Services, and in every geographic segment",
    "paragraph_id": "0000320193-26-000018:8k_2_02:8",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_release_record_june_quarter_operating_cash_flow",
    "what_changed": "In the release, the chief financial officer claims new June quarter records for operating cash flow and for earnings per share.",
    "account": "Cash generated by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "set new June quarter records for both EPS and operating cash flow",
    "paragraph_id": "0000320193-26-000018:8k_2_02:9",
    "explanation": false
  },
  {
    "id": "results_against_expectations_release_installed_base_all_time_high",
    "what_changed": "The release says the installed base of active devices reached a new all-time high across all major product categories and geographic segments. This is an operating metric and has no line in the statements.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our installed base of active devices also reached a new all-time high across all major product categories and geographic segments.",
    "paragraph_id": "0000320193-26-000018:8k_2_02:9",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter_end",
    "what_changed": "After the quarter closed, the board declared a cash dividend of $0.27 per share, payable August 13, 2026 to holders of record on August 10, 2026. The payment falls in the fourth quarter of fiscal 2026.",
    "account": "Payments for dividends and dividend equivalents",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "has declared a cash dividend of $0.27 per share",
    "paragraph_id": "0000320193-26-000018:8k_2_02:10",
    "explanation": false
  },
  {
    "id": "across_documents_siri_ai_introduced_in_release_and_quarterly_report",
    "what_changed": "The MD&A records that during the third quarter of fiscal 2026 the Company announced its new operating-system releases and introduced Siri AI. The chief executive's quote in the release names the same Siri AI introduction. Elsewhere in the MD&A, higher research and development expense is attributed partly to investment in artificial intelligence.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "and introduced Siri AI",
    "paragraph_id": "0000320193-26-000020:mdna:8",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_component_supply_constraints_and_rising_costs",
    "what_changed": "This paragraph appears as changed text; the prior quarter's wording is not in my input. It says the Company is experiencing supply constraints and rising component costs, driven by industry supply-demand imbalances in advanced semiconductors, NAND storage and DRAM memory. It adds that the Company expects these trends to intensify, which may materially hurt revenue, costs, gross margin, results and financial condition.",
    "account": "Gross margin (products cost of sales)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The Company expects these trends to intensify",
    "paragraph_id": "0000320193-26-000020:mdna:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_price_increases_taken_may_reduce_demand",
    "what_changed": "The same paragraph says the Company has already raised some prices and may raise them again. It warns that these actions may not offset the cost pressure and may reduce demand for its products, which could materially hurt revenue.",
    "account": "Products net sales",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Actions, such as price increases, that have been and may in the future be taken by the Company may not effectively mitigate these negative impacts",
    "paragraph_id": "0000320193-26-000020:mdna:11",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tariff_refunds_recognized_as_received",
    "what_changed": "The tariff paragraph appears as changed text. It refers to the Supreme Court ruling of February 20, 2026, which struck down certain tariffs imposed under the International Emergency Economic Powers Act. It says the Company applied for refunds through the U.S. Customs and Border Protection process and has recognized any refunds received as a reduction of products cost of sales. The wording ties recognition to receipt; it does not describe a receivable for refunds applied for but not yet received.",
    "account": "Products cost of sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "has recognized any refunds received as a reduction of products cost of sales",
    "paragraph_id": "0000320193-26-000020:mdna:13",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_recent_trade_act_tariffs_and_further_measures",
    "what_changed": "The tariff paragraph cites the recent imposition of tariffs under Section 301 of the Trade Act of 1974. It warns of possible further measures, including under the Section 232 semiconductor investigation. It also says the initial results of that investigation, published January 14, 2026, imposed no additional tariffs on the Company's products. The paragraph names effects on the supply chain, rare earths and component availability, pricing and gross margin.",
    "account": "Products cost of sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "including the recent imposition of tariffs under Section 301 of the Trade Act of 1974",
    "paragraph_id": "0000320193-26-000020:mdna:13",
    "explanation": false
  },
  {
    "id": "results_against_expectations_americas_net_sales_drivers",
    "what_changed": "The MD&A says Americas net sales increased in the third quarter and first nine months of fiscal 2026, primarily on higher iPhone, Services and Mac sales. No currency effect is mentioned for the Americas.",
    "account": "Americas net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Americas net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
    "paragraph_id": "0000320193-26-000020:mdna:18",
    "explanation": false
  },
  {
    "id": "results_against_expectations_europe_net_sales_drivers_and_currency",
    "what_changed": "The MD&A says Europe net sales increased in the quarter and the nine months, primarily on higher iPhone, Services and Mac sales. It gives a net favorable currency effect for the first nine months only; the sentence states no currency effect for the third quarter.",
    "account": "Europe net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The strength in foreign currencies relative to the U.S. dollar had a net favorable year-over-year impact on Europe net sales during the first nine months of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:20",
    "explanation": false
  },
  {
    "id": "results_against_expectations_greater_china_iphone_and_renminbi",
    "what_changed": "The MD&A says Greater China net sales increased in the quarter and the nine months, primarily on higher iPhone sales. It says the stronger renminbi had a favorable effect in both periods.",
    "account": "Greater China net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The strength in the renminbi relative to the U.S. dollar had a favorable year-over-year impact on Greater China net sales during the third quarter and first nine months of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:22",
    "explanation": false
  },
  {
    "id": "results_against_expectations_japan_iphone_against_weak_yen",
    "what_changed": "The MD&A says Japan net sales increased in the quarter and the nine months on higher iPhone sales. It says the weaker yen had an unfavorable effect in both periods.",
    "account": "Japan net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The weakness in the yen relative to the U.S. dollar had an unfavorable year-over-year impact on Japan net sales during the third quarter and first nine months of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_rest_of_asia_pacific_drivers_and_currency",
    "what_changed": "The MD&A says Rest of Asia Pacific net sales increased in the quarter and the nine months, primarily on higher iPhone, Services and Mac sales. It gives a net favorable currency effect for the third quarter only; the sentence states no currency effect for the nine months.",
    "account": "Rest of Asia Pacific net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The strength in foreign currencies relative to the U.S. dollar had a net favorable year-over-year impact on Rest of Asia Pacific net sales during the third quarter of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:26",
    "explanation": false
  },
  {
    "id": "results_against_expectations_iphone_pro_models",
    "what_changed": "The MD&A says iPhone net sales increased in the quarter and the nine months, primarily on higher sales of Pro models.",
    "account": "iPhone net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "iPhone net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of Pro models.",
    "paragraph_id": "0000320193-26-000020:mdna:31",
    "explanation": false
  },
  {
    "id": "results_against_expectations_mac_laptops",
    "what_changed": "The MD&A says Mac net sales increased in the quarter and the nine months on higher laptop sales.",
    "account": "Mac net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Mac net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of laptops.",
    "paragraph_id": "0000320193-26-000020:mdna:33",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_ipad_third_quarter_decline",
    "what_changed": "The MD&A says iPad net sales decreased in the third quarter of fiscal 2026 against the prior-year quarter, primarily on lower iPad mini and iPad Air sales. For the nine months it says iPad net sales increased, primarily on the base iPad, partly offset by lower iPad mini sales.",
    "account": "iPad net sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "iPad net sales decreased during the third quarter of 2026 compared to the third quarter of 2025 primarily due to lower net sales of iPad mini",
    "paragraph_id": "0000320193-26-000020:mdna:35",
    "explanation": false
  },
  {
    "id": "results_against_expectations_wearables_home_accessories_increase",
    "what_changed": "The MD&A says Wearables, Home and Accessories net sales increased in the quarter and the nine months on higher Accessories and Wearables sales.",
    "account": "Wearables, Home and Accessories net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "due to higher net sales of Accessories and Wearables",
    "paragraph_id": "0000320193-26-000020:mdna:37",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_advertising_and_cloud",
    "what_changed": "The MD&A says Services net sales increased in the quarter and the nine months, primarily on advertising and cloud services. This paragraph does not name the App Store as a driver.",
    "account": "Services net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to higher net sales from advertising and cloud services",
    "paragraph_id": "0000320193-26-000020:mdna:39",
    "explanation": false
  },
  {
    "id": "earnings_quality_products_gross_margin_mix_and_tariff_refunds",
    "what_changed": "The MD&A says products gross margin and products gross margin percentage increased in the quarter and the nine months. It gives product mix and tariff refunds as the primary drivers, partly offset by higher costs including memory. Tariff refunds, a one-off item, are among the stated primary drivers.",
    "account": "Products gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to a different mix of products and tariff refunds",
    "paragraph_id": "0000320193-26-000020:mdna:45",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_costs_in_products_gross_margin",
    "what_changed": "The same paragraph names higher costs, including memory, as an offset to products gross margin in the quarter and the nine months. The memory-cost pressure that the MD&A describes as intensifying is therefore stated as already affecting reported margin.",
    "account": "Products cost of sales (memory component costs)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by higher costs, including memory",
    "paragraph_id": "0000320193-26-000020:mdna:45",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_gross_margin_increase",
    "what_changed": "The MD&A says Services gross margin increased in the quarter and the nine months, primarily on higher Services net sales and a different mix of services, partly offset by higher costs.",
    "account": "Services gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to higher Services net sales and a different mix of services, partially offset by higher costs",
    "paragraph_id": "0000320193-26-000020:mdna:47",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_gross_margin_percentage_flat_in_quarter",
    "what_changed": "The MD&A describes Services gross margin percentage as flat in the third quarter of fiscal 2026 against the prior-year quarter. For the nine months it says the percentage increased, primarily on services mix, partly offset by higher costs.",
    "account": "Services gross margin percentage",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Services gross margin percentage was flat during the third quarter of 2026 compared to the third quarter of 2025.",
    "paragraph_id": "0000320193-26-000020:mdna:48",
    "explanation": false
  },
  {
    "id": "results_against_expectations_research_and_development_artificial_intelligence_infrastructure",
    "what_changed": "The MD&A says research and development expense increased in the quarter and the nine months. It gives the primary causes as higher infrastructure-related costs, including investments in artificial intelligence, and higher headcount-related expenses.",
    "account": "Research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to higher infrastructure-related costs, including investments in artificial intelligence, and headcount-related expenses",
    "paragraph_id": "0000320193-26-000020:mdna:54",
    "explanation": false
  },
  {
    "id": "results_against_expectations_selling_general_administrative_no_significant_factor",
    "what_changed": "The MD&A says selling, general and administrative expense increased in the quarter and the nine months, driven by various factors, none of them significant individually or in the aggregate. No driver is named.",
    "account": "Selling, general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increases were driven by various factors, none of which were significant individually or in the aggregate.",
    "paragraph_id": "0000320193-26-000020:mdna:56",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_effective_tax_rate_unrecognized_tax_benefits",
    "what_changed": "The MD&A says the effective tax rate for the quarter and the nine months was below the statutory federal rate. The primary reason given is a lower rate on foreign earnings, including the impact of changes in unrecognized tax benefits. The federal R&D credit and share-based compensation tax benefits also lowered the rate, partly offset by state income taxes. Changes in unrecognized tax benefits, a reserve judgment, are named as a factor keeping the rate below statutory.",
    "account": "Provision for income taxes; unrecognized tax benefits",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "lower than the statutory federal income tax rate primarily due to a lower effective tax rate on foreign earnings, including the impact of changes in unrecognized tax benefits",
    "paragraph_id": "0000320193-26-000020:mdna:60",
    "explanation": false
  },
  {
    "id": "earnings_quality_effective_tax_rate_higher_on_foreign_earnings",
    "what_changed": "The MD&A says the effective tax rate for the third quarter of fiscal 2026 was higher than a year earlier, primarily because of a higher rate on foreign earnings, partly offset by changes in unrecognized tax benefits and share-based compensation tax benefits. For the nine months it also says the rate was higher, primarily because of a higher rate on foreign earnings. The nine-month factors it lists are: changes in unrecognized tax benefits; the foreign currency loss regulations the Treasury issued in December 2024; and the tax impact of foreign currency revaluations in the first quarter of fiscal 2025 related to the State Aid Decision. So changes in unrecognized tax benefits are named as an offset for the quarter but among the drivers of the increase for the nine months.",
    "account": "Provision for income taxes (effective tax rate)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "effective tax rate for the third quarter of 2026 was higher compared to the third quarter of 2025 primarily due to a higher effective tax rate on foreign earnings, partially offset by the impact of changes in unrecognized tax benefits and tax benefits from share-based compensation",
    "paragraph_id": "0000320193-26-000020:mdna:61",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_manufacturing_purchase_obligations",
    "what_changed": "The MD&A states manufacturing purchase obligations of $57.0 billion as of June 27, 2026, with $56.2 billion payable within 12 months. The prior quarter's figure is not in my input; the comparison is left to the numbers reader.",
    "account": "Manufacturing purchase obligations (off balance sheet)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 27, 2026, the Company had manufacturing purchase obligations of $57.0 billion, with $56.2 billion payable within 12 months.",
    "paragraph_id": "0000320193-26-000020:mdna:66",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_other_purchase_obligations",
    "what_changed": "The MD&A states other purchase obligations of $29.3 billion as of June 27, 2026, with $9.2 billion payable within 12 months. It describes them as noncancelable obligations for supplier arrangements, licensed intellectual property and content, distribution rights, and capital assets for product manufacturing.",
    "account": "Other purchase obligations (off balance sheet)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 27, 2026, the Company had other purchase obligations of $29.3 billion, with $9.2 billion payable within 12 months.",
    "paragraph_id": "0000320193-26-000020:mdna:68",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_deemed_repatriation_tax_fully_paid",
    "what_changed": "The MD&A says that during the first nine months of fiscal 2026 the Company paid the remaining $8.8 billion balance of the deemed repatriation tax payable imposed by the Tax Cuts and Jobs Act of 2017. Calling it the remaining balance means this liability is now fully paid, so no further payments on it should appear.",
    "account": "Deemed repatriation tax payable (within other current and non-current liabilities)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the Company paid the remaining $8.8 billion balance of the deemed repatriation tax payable imposed by the U.S. Tax Cuts and Jobs Act of 2017",
    "paragraph_id": "0000320193-26-000020:mdna:70",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_quarterly_dividend_rate_and_annual_increase_intent",
    "what_changed": "The MD&A states the quarterly cash dividend was $0.27 per share as of June 27, 2026. It says the Company intends to raise its dividend every year, subject to declaration by the Board, and that the repurchase programs set no minimum amount.",
    "account": "Dividends per share",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "quarterly cash dividend was $0.27 per share",
    "paragraph_id": "0000320193-26-000020:mdna:72",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_third_quarter_repurchases_and_dividends_paid",
    "what_changed": "The MD&A states that in the third quarter of fiscal 2026 the Company repurchased $25.8 billion of its common stock and paid $4.0 billion of dividends and dividend equivalents.",
    "account": "Repurchases of common stock; payments for dividends and dividend equivalents",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "During the third quarter of 2026, the Company repurchased $25.8 billion of its common stock and paid dividends and dividend equivalents of $4.0 billion.",
    "paragraph_id": "0000320193-26-000020:mdna:73",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_internal_use_software_standard_timing_under_evaluation",
    "what_changed": "This MD&A paragraph covers the internal-use software standard (ASU 2025-06). The standard takes effect in the Company's first quarter of fiscal 2029, early adoption is permitted, and the Company is evaluating the timing and method of adoption. Under the standard, software costs are capitalized once management has committed to the project and completion is probable. The wording leaves early adoption open.",
    "account": "Capitalized internal-use software; research and development expense",
    "expected_direction": "none",
    "horizon": "beyond 12 months",
    "quote": "The Company is currently evaluating the timing and method of its adoption",
    "paragraph_id": "0000320193-26-000020:mdna:76",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_expense_disaggregation_standard_adoption",
    "what_changed": "The MD&A says the Company will adopt the expense disaggregation standard (ASU 2024-03) in its fourth quarter of fiscal 2028, on a prospective basis. The standard requires disclosing inventory purchases, employee compensation, depreciation and intangible amortization within expense captions, plus the amount and the Company's definition of selling expenses.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "beyond 12 months",
    "quote": "in its fourth quarter of 2028 using a prospective transition method",
    "paragraph_id": "0000320193-26-000020:mdna:78",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_adoption_next_quarter",
    "what_changed": "The MD&A says the Company will adopt the income tax disclosure standard (ASU 2023-09) in its fourth quarter of fiscal 2026, on a prospective basis. The standard expands the rate reconciliation and splits income taxes paid into federal, state and foreign, with further detail for significant jurisdictions.",
    "account": "Provision for income taxes; cash paid for income taxes (disclosure)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "in its fourth quarter of 2026 using a prospective transition method",
    "paragraph_id": "0000320193-26-000020:mdna:80",
    "explanation": false
  },
  {
    "id": "revenue_recognition_total_deferred_revenue_balance",
    "what_changed": "The revenue note states total deferred revenue of $14.9 billion as of June 27, 2026 and $13.7 billion as of September 27, 2025. The prior quarter's paragraph gave $14.7 billion as of March 28, 2026. The expected realization schedule is worded exactly as last quarter: 64% within a year, 23% in one to two years, 11% in two to three years, 2% beyond three years.",
    "account": "Deferred revenue (current and non-current)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the Company had total deferred revenue of $14.9 billion and $13.7 billion, respectively",
    "paragraph_id": "0000320193-26-000020:notes:7",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_marketable_securities_maturity_profile",
    "what_changed": "The note states the maturity profile of non-current marketable debt securities as of June 27, 2026. Excluding mortgage- and asset-backed securities: 81% mature in one to five years, 16% in five to ten years and 3% beyond ten years. For mortgage- and asset-backed securities the figures are 14%, 21% and 65%. The prior quarter's wording is not in my input.",
    "account": "Non-current marketable securities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "had maturities between 1 and 5 years, 16% between 5 and 10 years, and 3% greater than 10 years",
    "paragraph_id": "0000320193-26-000020:notes:15",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_term_debt_currency_hedge_horizon",
    "what_changed": "The note states that as of June 27, 2026, the Company hedges the variability of cash flows on term-debt-related foreign currency transactions for at most 16 years. The prior quarter's wording is not in my input.",
    "account": "Foreign exchange contracts designated as cash flow hedges; term debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "foreign currency transactions is 16 years",
    "paragraph_id": "0000320193-26-000020:notes:20",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_term_debt_under_fair_value_hedges",
    "what_changed": "The note states the carrying amount of current and non-current term debt subject to fair value hedges: $10.4 billion as of June 27, 2026 and $12.6 billion as of September 27, 2025.",
    "account": "Term debt (portion under fair value hedges)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "current and non-current term debt subject to fair value hedges was $10.4 billion and $12.6 billion, respectively",
    "paragraph_id": "0000320193-26-000020:notes:26",
    "explanation": false
  },
  {
    "id": "revenue_recognition_single_customer_share_of_trade_receivables",
    "what_changed": "The note states that at both dates one customer represented 10% or more of total trade receivables: 18% as of June 27, 2026 and 12% as of September 27, 2025. The customer is not named. The paragraph says the Company requires third-party credit support or collateral from certain customers.",
    "account": "Accounts receivable, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "which accounted for 18% and 12%, respectively",
    "paragraph_id": "0000320193-26-000020:notes:29",
    "explanation": false
  },
  {
    "id": "revenue_recognition_cellular_carrier_share_of_trade_receivables",
    "what_changed": "The note states that third-party cellular network carriers accounted for 27% of total trade receivables as of June 27, 2026 and 34% as of September 27, 2025.",
    "account": "Accounts receivable, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "accounted for 27% and 34% of total trade receivables as of June 27, 2026 and September 27, 2025, respectively",
    "paragraph_id": "0000320193-26-000020:notes:29",
    "explanation": false
  },
  {
    "id": "earnings_quality_vendor_non_trade_receivable_concentration",
    "what_changed": "The note states that two vendors each represented 10% or more of vendor non-trade receivables: 47% and 22% as of June 27, 2026, and 46% and 23% as of September 27, 2025. It describes these receivables as arising from component sales to manufacturing vendors. Any gain on those sales is recognized as a reduction of products cost of sales when the final products are sold.",
    "account": "Vendor non-trade receivables",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 27, 2026, the Company had two vendors that individually represented 10% or more of total vendor non-trade receivables, which accounted for 47% and 22%.",
    "paragraph_id": "0000320193-26-000020:notes:31",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_term_debt_carrying_amount_and_fair_value",
    "what_changed": "The note states the Notes' aggregate carrying amount at $82.3 billion and their fair value, based on Level 2 inputs, at $71.2 billion as of June 27, 2026. The figures for September 27, 2025 are $90.7 billion and $80.4 billion. The prior quarter's paragraph gave $82.7 billion and $70.8 billion as of March 28, 2026.",
    "account": "Term debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "for an aggregate carrying amount of $82.3 billion and $90.7 billion, respectively",
    "paragraph_id": "0000320193-26-000020:notes:43",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_nine_month_share_repurchases",
    "what_changed": "The note states the Company repurchased 215 million shares for $61.8 billion in the nine months ended June 27, 2026. It adds that the programs carry no minimum purchase obligation and that repurchases may use privately negotiated, open market or Rule 10b5-1 plan transactions.",
    "account": "Repurchases of common stock; shares outstanding",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the Company repurchased 215 million shares of its common stock for $61.8 billion",
    "paragraph_id": "0000320193-26-000020:notes:45",
    "explanation": false
  },
  {
    "id": "earnings_quality_restricted_stock_unit_vesting_date_fair_value",
    "what_changed": "The note states the vesting-date fair value of restricted stock units: $8.9 billion for the third quarter of fiscal 2026 and $7.0 billion for the prior-year quarter; $18.4 billion and $16.3 billion for the two nine-month periods.",
    "account": "Share-based compensation (tax benefits; taxes paid on net share settlement)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The total vesting-date fair value of RSUs was $8.9 billion and $7.0 billion for the three months ended June 27, 2026 and June 28, 2025",
    "paragraph_id": "0000320193-26-000020:notes:49",
    "explanation": false
  },
  {
    "id": "earnings_quality_unrecognized_share_based_compensation_cost",
    "what_changed": "The note states total unrecognized compensation cost for outstanding restricted stock units of $26.7 billion as of June 27, 2026, to be recognized over a weighted-average 2.7 years.",
    "account": "Share-based compensation expense",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the total unrecognized compensation cost related to outstanding RSUs was $26.7 billion, which the Company expects to recognize over a weighted-average period of 2.7 years",
    "paragraph_id": "0000320193-26-000020:notes:53",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_legal_contingency_conclusion_carried_as_changed",
    "what_changed": "Insufficient. The contingencies paragraph appears as changed text rather than as unchanged, but my input has no prior wording for it and the note change history lists no change to it. It now gives management's conclusion that a material loss, or a material loss greater than a recorded accrual, is not reasonably possible for asserted legal and other claims. What changed cannot be determined from my input.",
    "account": "Accrued loss contingencies",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "there was not at least a reasonable possibility the Company may have incurred a material loss, or a material loss greater than a recorded accrual",
    "paragraph_id": "0000320193-26-000020:notes:58",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_general_counsel_trading_plan",
    "what_changed": "New trading-plan disclosure. On May 5, 2026, Jennifer Newstead, Senior Vice President and General Counsel, entered a Rule 10b5-1 plan. It allows her to sell up to 24,912 shares, subject to price limits, plus up to 90% of shares vesting between June 15, 2026 and March 15, 2027, net of tax withholding. The plan expires May 6, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The plan provides for the sale, subject to certain price limits, of up to 24,912 shares of common stock",
    "paragraph_id": "0000320193-26-000020:notes:62",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_executive_trading_plan",
    "what_changed": "New trading-plan disclosure. On May 28, 2026, Tim Cook, Chief Executive Officer, entered a Rule 10b5-1 plan. It allows him to sell up to 16,250 shares, subject to price limits, plus shares vesting during the plan, net of tax withholding, and to gift up to 37,104 shares. The plan expires October 30, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "of up to 16,250 shares of common stock, as well as shares vesting during the duration of the plan",
    "paragraph_id": "0000320193-26-000020:notes:63",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### Earnings release body
- `0000320193-26-000018:8k_2_02:1` — exhibit file header lines
- `0000320193-26-000018:8k_2_02:2` — document title line
- `0000320193-26-000018:8k_2_02:3` — exhibit label
- `0000320193-26-000018:8k_2_02:4` — headline only; the claims under it are itemized from the paragraphs that follow
- `0000320193-26-000018:8k_2_02:11` — webcast logistics
- `0000320193-26-000018:8k_2_02:12` — investor website boilerplate
- `0000320193-26-000018:8k_2_02:13` — standard company description; the prior release is not in my input, so no change can be shown
- `0000320193-26-000018:8k_2_02:14` — press contact label
- `0000320193-26-000018:8k_2_02:15` — contact name
- `0000320193-26-000018:8k_2_02:16` — contact employer
- `0000320193-26-000018:8k_2_02:17` — contact email
- `0000320193-26-000018:8k_2_02:18` — contact phone
- `0000320193-26-000018:8k_2_02:19` — investor relations contact label
- `0000320193-26-000018:8k_2_02:20` — contact name
- `0000320193-26-000018:8k_2_02:21` — contact employer
- `0000320193-26-000018:8k_2_02:22` — contact email
- `0000320193-26-000018:8k_2_02:23` — contact phone
- `0000320193-26-000018:8k_2_02:24` — note to editors
- `0000320193-26-000018:8k_2_02:25` — copyright and trademark line
- `0000320193-26-000018:8k_2_02:26` — company name heading
- `0000320193-26-000018:8k_2_02:27` — statement title
- `0000320193-26-000018:8k_2_02:28` — units line
- `0000320193-26-000018:8k_2_02:29` — amounts only (statement of operations)
- `0000320193-26-000018:8k_2_02:30` — company name heading
- `0000320193-26-000018:8k_2_02:31` — statement title
- `0000320193-26-000018:8k_2_02:32` — units line
- `0000320193-26-000018:8k_2_02:33` — amounts only (balance sheet)
- `0000320193-26-000018:8k_2_02:34` — company name heading
- `0000320193-26-000018:8k_2_02:35` — statement title
- `0000320193-26-000018:8k_2_02:36` — units line
- `0000320193-26-000018:8k_2_02:37` — amounts only (cash flow statement)

### Controls and procedures
- `0000320193-26-000020:item_4_controls:1` — heading
- `0000320193-26-000020:item_4_controls:2` — heading
- `0000320193-26-000020:item_4_controls:3` — date rolled forward; conclusion is that disclosure controls were effective, with no deficiency disclosed
- `0000320193-26-000020:item_4_controls:4` — heading
- `0000320193-26-000020:item_4_controls:5` — date rolled forward; states no material change in internal control during the quarter
- `0000320193-26-000020:item_4_controls:6` — page footer

### MD&A
- `0000320193-26-000020:mdna:15` — table introduction, dates rolled forward
- `0000320193-26-000020:mdna:16` — amounts only (net sales by segment)
- `0000320193-26-000020:mdna:28` — table introduction, dates rolled forward
- `0000320193-26-000020:mdna:29` — amounts only (net sales by category)
- `0000320193-26-000020:mdna:41` — table introduction, dates rolled forward
- `0000320193-26-000020:mdna:42` — amounts only (gross margin)
- `0000320193-26-000020:mdna:43` — amounts only (gross margin percentage)
- `0000320193-26-000020:mdna:51` — table introduction, dates rolled forward
- `0000320193-26-000020:mdna:52` — amounts only (operating expenses)
- `0000320193-26-000020:mdna:58` — table introduction, dates rolled forward
- `0000320193-26-000020:mdna:59` — amounts only (tax provision and rates)

### Notes
- `0000320193-26-000020:notes:4` — heading and table introduction, dates rolled forward (the change history shows only the period words changed)
- `0000320193-26-000020:notes:5` — amounts only (disaggregated net sales)
- `0000320193-26-000020:notes:6` — dates rolled forward; the Greater China iPhone sentence is otherwise worded as last quarter (change history)
- `0000320193-26-000020:notes:8` — heading and table introduction, dates rolled forward
- `0000320193-26-000020:notes:9` — amounts only (earnings per share computation)
- `0000320193-26-000020:notes:11` — table introduction, dates rolled forward
- `0000320193-26-000020:notes:12` — amounts only (cash and investments by category)
- `0000320193-26-000020:notes:24` — table introduction, dates rolled forward
- `0000320193-26-000020:notes:25` — amounts only (derivative notional amounts)
- `0000320193-26-000020:notes:32` — heading and table introduction, dates rolled forward
- `0000320193-26-000020:notes:33` — heading
- `0000320193-26-000020:notes:34` — amounts only (inventories)
- `0000320193-26-000020:notes:36` — amounts only (property, plant and equipment)
- `0000320193-26-000020:notes:38` — amounts only (intangible assets)
- `0000320193-26-000020:notes:39` — heading
- `0000320193-26-000020:notes:40` — date rolled forward; outstanding commercial paper amounts worded as last quarter (change history)
- `0000320193-26-000020:notes:41` — amounts only; rows added to carry prior-year comparatives (change history)
- `0000320193-26-000020:notes:42` — heading
- `0000320193-26-000020:notes:47` — table introduction, date rolled forward
- `0000320193-26-000020:notes:48` — amounts only (restricted stock unit activity)
- `0000320193-26-000020:notes:51` — table introduction, dates rolled forward
- `0000320193-26-000020:notes:52` — amounts only (share-based compensation expense and tax benefit)
- `0000320193-26-000020:notes:54` — heading
- `0000320193-26-000020:notes:55` — reordered list of obligation categories; date rolled forward (change history)
- `0000320193-26-000020:notes:56` — amounts only; remaining-period label rolled forward (change history)
- `0000320193-26-000020:notes:57` — heading
- `0000320193-26-000020:notes:59` — heading and table introduction, dates rolled forward
- `0000320193-26-000020:notes:60` — amounts only (segment results, three months)
- `0000320193-26-000020:notes:61` — amounts only (segment results, nine months)

### Note change history
I used these only as the prior-quarter wording for the notes paragraphs they mirror. Each is accounted for under that notes paragraph.
- `0000320193-26-000020:note_history:1` and `0000320193-26-000013:note_history:1` — see notes:55
- `0000320193-26-000020:note_history:2` and `0000320193-26-000013:note_history:2` — see notes:56
- `0000320193-26-000020:note_history:3` and `0000320193-26-000013:note_history:3` — see notes:40
- `0000320193-26-000020:note_history:4` and `0000320193-26-000013:note_history:6` — see notes:41
- `0000320193-26-000020:note_history:5` and `0000320193-26-000013:note_history:5` — see notes:43 (itemized)
- `0000320193-26-000020:note_history:7` and `0000320193-26-000013:note_history:7` — see notes:4
- `0000320193-26-000020:note_history:8` and `0000320193-26-000013:note_history:8` — see notes:5
- `0000320193-26-000020:note_history:9` and `0000320193-26-000013:note_history:9` — see notes:6
- `0000320193-26-000020:note_history:10` and `0000320193-26-000013:note_history:11` — see notes:7 (itemized)
