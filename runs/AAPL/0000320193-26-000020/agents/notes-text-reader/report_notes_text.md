# report_notes_text — AAPL 10-Q 0000320193-26-000020 (quarter ended June 27, 2026)

## Directory check

The directory holds six files: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md and input_prior_predictions.md. There is no trend table, price, abnormal return, short-interest figure, other company's file, prior-run probability or outcome window. The 8-K 2.02 body contains the condensed financial statements from Exhibit 99.1. They are part of the 8-K body, and I computed nothing from them. There are no prior flags ("None on record").

## Reading caveats

- For MD&A, and for every notes block other than revenue, debt and commitments/contingencies, my input does not include the prior-period text. The note change history covers only those three blocks. When an item below says the text "now says", it means the current wording of a paragraph that the diff layer marks as changed. It is not a checked sentence-by-sentence comparison with the prior quarter.
- I did no arithmetic and made no magnitude comparisons. Words such as "increased", "decreased", "flat", "record" and "higher" are the filer's own words.
- No item has `explanation: true`. No paragraph in my input has management explaining the cause of a receivables, inventory or reserve number. The tax paragraphs use changes in unrecognized tax benefits to explain the tax rate. They do not explain the reserve itself.

## Items

```json
[
  {
    "id": "across_documents_siri_ai_software_only_quarter_announcements",
    "what_changed": "The quarter's product-announcement paragraph now lists software releases only (iOS 27, macOS 27 Golden Gate, iPadOS 27, watchOS 27, visionOS 27, tvOS 27) and the introduction of Siri AI. It names no hardware. The prior period's announcement paragraphs (prior mdna:8 to prior mdna:14) are not carried. The 8-K release (8k_2_02:8) links Siri AI to WWDC26 and adds 'important new child safety features'. MD&A mdna:54 attributes part of the R&D growth to investments in artificial intelligence.",
    "account": "none (bears on research and development through AI investment)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "and introduced Siri AI.",
    "paragraph_id": "0000320193-26-000020:mdna:8",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_component_supply_constraints",
    "what_changed": "The component paragraph, which the diff layer marks as changed, says in the present tense that the Company is experiencing supply constraints and rising component costs. It names advanced semiconductors, NAND storage and DRAM memory, and says these may materially hurt revenue. The text gives no amount.",
    "account": "products net sales",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "The Company is experiencing a period of supply constraints and increasing costs for components driven by factors such as industry supply-demand imbalances for components, including advanced semiconductors, storage (NAND) and memory (DRAM).",
    "paragraph_id": "0000320193-26-000020:mdna:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_component_cost_trends_expected_to_intensify",
    "what_changed": "Management says it expects the component supply and cost trends to intensify, and that this may materially hurt revenue, costs, gross margin, results of operations and financial condition. In the same filing, the products margin paragraph (mdna:45) already names 'higher costs, including memory' as an offset in the current quarter.",
    "account": "products gross margin",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "The Company expects these trends to intensify",
    "paragraph_id": "0000320193-26-000020:mdna:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_price_increases_taken_may_cut_demand",
    "what_changed": "The text says price increases 'have been' taken as well as possibly in the future. It adds that such actions may not offset the cost impacts and may reduce demand for the Company's products, hurting revenue and gross margin. The text does not say which products or markets had price increases.",
    "account": "products net sales (unit demand)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Actions, such as price increases, that have been and may in the future be taken by the Company may not effectively mitigate these negative impacts, and may also reduce demand",
    "paragraph_id": "0000320193-26-000020:mdna:11",
    "explanation": false
  },
  {
    "id": "earnings_quality_tariff_refunds_booked_in_products_cost_of_sales",
    "what_changed": "The tariff paragraph now says that refunds of tariffs struck down by the Supreme Court's February 20, 2026 IEEPA ruling have been applied for. Any refunds received are recognized as a reduction of products cost of sales, so they land inside gross margin rather than in other income/(expense). No amount appears in this paragraph. The 8-K (8k_2_02:7) sizes the quarter's effect at about 2 percentage points of gross margin and $0.11 of diluted EPS.",
    "account": "products cost of sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "has recognized any refunds received as a reduction of products cost of sales",
    "paragraph_id": "0000320193-26-000020:mdna:13",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tariff_refund_applications_pending",
    "what_changed": "The Company says it has applied for tariff refunds through the U.S. Customs and Border Protection process, and it recognizes only refunds it has received. The text gives no amount applied for, received or still outstanding. Any further receipts would reach products cost of sales in the quarter they arrive. This is an unrecognized gain contingency whose size is not disclosed in my input.",
    "account": "products cost of sales",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "The Company has applied for a refund of tariffs paid, following the processes established by U.S. Customs and Border Protection",
    "paragraph_id": "0000320193-26-000020:mdna:13",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_trade_act_tariffs_newly_imposed",
    "what_changed": "The paragraph now cites 'the recent imposition of tariffs under Section 301 of the Trade Act of 1974'. It lists possible further measures: more under the Section 232 semiconductor investigation, sector-based tariffs, and further Section 301 actions. It names the availability of rare earths among supply-chain effects. It also says the January 14, 2026 Section 232 initial results imposed no additional tariffs on the Company's products. No cost amount is given for the new tariffs.",
    "account": "products cost of sales",
    "expected_direction": "up",
    "horizon": "next quarter to 12 months",
    "quote": "including the recent imposition of tariffs under Section 301 of the Trade Act of 1974",
    "paragraph_id": "0000320193-26-000020:mdna:13",
    "explanation": false
  },
  {
    "id": "results_against_expectations_americas_sales_drivers",
    "what_changed": "For the third quarter and the nine months, the text attributes Americas growth primarily to iPhone, Services and Mac. It names no currency effect for Americas.",
    "account": "Americas net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Americas net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
    "paragraph_id": "0000320193-26-000020:mdna:18",
    "explanation": false
  },
  {
    "id": "results_against_expectations_europe_sales_drivers",
    "what_changed": "For the third quarter and the nine months, the text attributes Europe growth primarily to iPhone, Services and Mac.",
    "account": "Europe net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Europe net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
    "paragraph_id": "0000320193-26-000020:mdna:20",
    "explanation": false
  },
  {
    "id": "earnings_quality_europe_currency_tailwind_nine_months_only",
    "what_changed": "The text names a net favorable currency effect on Europe net sales for the first nine months only. It states no currency effect for the third quarter on its own, so part of the nine-month growth is attributed to currency rather than volume or price.",
    "account": "Europe net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The strength in foreign currencies relative to the U.S. dollar had a net favorable year-over-year impact on Europe net sales during the first nine months of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:20",
    "explanation": false
  },
  {
    "id": "results_against_expectations_greater_china_iphone_driven_sales",
    "what_changed": "For the third quarter and the nine months, the text attributes Greater China growth primarily to iPhone alone, with no other category named. The revenue note (notes:6) repeats that iPhone is a moderately higher share of Greater China net sales.",
    "account": "Greater China net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Greater China net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone.",
    "paragraph_id": "0000320193-26-000020:mdna:22",
    "explanation": false
  },
  {
    "id": "earnings_quality_greater_china_renminbi_tailwind",
    "what_changed": "The text names renminbi strength as a favorable year-over-year effect on Greater China net sales for both the third quarter and the nine months. Part of the reported growth is attributed to currency.",
    "account": "Greater China net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The strength in the renminbi relative to the U.S. dollar had a favorable year-over-year impact on Greater China net sales during the third quarter and first nine months of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:22",
    "explanation": false
  },
  {
    "id": "results_against_expectations_japan_iphone_driven_sales",
    "what_changed": "For the third quarter and the nine months, the text attributes Japan growth to iPhone. The paragraph says 'due to', not 'primarily due to'.",
    "account": "Japan net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Japan net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of iPhone.",
    "paragraph_id": "0000320193-26-000020:mdna:24",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_japan_yen_headwind",
    "what_changed": "The text names yen weakness as an unfavorable year-over-year effect on Japan net sales for both the quarter and the nine months. Japan is the only segment whose paragraph names an adverse currency effect.",
    "account": "Japan net sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The weakness in the yen relative to the U.S. dollar had an unfavorable year-over-year impact on Japan net sales during the third quarter and first nine months of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_rest_of_asia_pacific_sales_drivers",
    "what_changed": "For the third quarter and the nine months, the text attributes Rest of Asia Pacific growth primarily to iPhone, Services and Mac.",
    "account": "Rest of Asia Pacific net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Rest of Asia Pacific net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of iPhone, Services and Mac.",
    "paragraph_id": "0000320193-26-000020:mdna:26",
    "explanation": false
  },
  {
    "id": "earnings_quality_rest_of_asia_pacific_currency_tailwind_quarter_only",
    "what_changed": "The text names a net favorable currency effect on Rest of Asia Pacific net sales for the third quarter only. It states none for the nine months, so part of the quarter's growth is attributed to currency.",
    "account": "Rest of Asia Pacific net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The strength in foreign currencies relative to the U.S. dollar had a net favorable year-over-year impact on Rest of Asia Pacific net sales during the third quarter of 2026.",
    "paragraph_id": "0000320193-26-000020:mdna:26",
    "explanation": false
  },
  {
    "id": "results_against_expectations_iphone_pro_models_driver",
    "what_changed": "For the third quarter and the nine months, the text attributes iPhone growth primarily to higher net sales of Pro models, which points to a mix shift toward higher-priced models.",
    "account": "iPhone net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "iPhone net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales of Pro models.",
    "paragraph_id": "0000320193-26-000020:mdna:31",
    "explanation": false
  },
  {
    "id": "results_against_expectations_mac_laptops_driver",
    "what_changed": "For the third quarter and the nine months, the text attributes Mac growth to laptops. It says 'due to', not 'primarily due to'.",
    "account": "Mac net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Mac net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of laptops.",
    "paragraph_id": "0000320193-26-000020:mdna:33",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_ipad_quarterly_sales_decline",
    "what_changed": "The text says iPad net sales decreased in the third quarter, primarily because of lower iPad mini and iPad Air sales. For the nine months it says iPad increased, primarily on the base iPad, partly offset by iPad mini. iPad is the only category the text describes as decreasing in the quarter.",
    "account": "iPad net sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "iPad net sales decreased during the third quarter of 2026 compared to the third quarter of 2025",
    "paragraph_id": "0000320193-26-000020:mdna:35",
    "explanation": false
  },
  {
    "id": "results_against_expectations_wearables_home_accessories_drivers",
    "what_changed": "For the third quarter and the nine months, the text attributes Wearables, Home and Accessories growth to Accessories and Wearables. Home is not named.",
    "account": "Wearables, Home and Accessories net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Wearables, Home and Accessories net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 due to higher net sales of Accessories and Wearables.",
    "paragraph_id": "0000320193-26-000020:mdna:37",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_advertising_and_cloud_drivers",
    "what_changed": "For the third quarter and the nine months, the text attributes Services growth primarily to advertising and cloud services. App Store is not among the named drivers.",
    "account": "Services net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Services net sales increased during the third quarter and first nine months of 2026 compared to the same periods in 2025 primarily due to higher net sales from advertising and cloud services.",
    "paragraph_id": "0000320193-26-000020:mdna:39",
    "explanation": false
  },
  {
    "id": "across_documents_tariff_refund_margin_driver_unquantified_in_filing",
    "what_changed": "The 10-Q's products gross margin paragraph names tariff refunds, alongside product mix, as a primary driver of the increase. None of the 10-Q text I have gives an amount. The 8-K release (8k_2_02:7) gives about 2 percentage points of company gross margin and $0.11 of diluted EPS. Reconciling the two is for the supervisors.",
    "account": "products gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to a different mix of products and tariff refunds",
    "paragraph_id": "0000320193-26-000020:mdna:45",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_costs_offset_products_margin",
    "what_changed": "The products gross margin paragraph names 'higher costs, including memory' as the offset to this quarter's margin drivers. Memory is named specifically, which ties the current quarter to the component-cost trends management expects to intensify (mdna:11).",
    "account": "products gross margin",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "partially offset by higher costs, including memory",
    "paragraph_id": "0000320193-26-000020:mdna:45",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_gross_margin_drivers",
    "what_changed": "For the quarter and the nine months, the text attributes the Services gross margin increase primarily to higher Services net sales and a different mix of services, partly offset by higher costs.",
    "account": "services gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to higher Services net sales and a different mix of services, partially offset by higher costs",
    "paragraph_id": "0000320193-26-000020:mdna:47",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_margin_percentage_flat_in_quarter",
    "what_changed": "The text says the Services gross margin percentage was flat year over year in the third quarter. For the nine months it says the percentage increased, primarily on mix, partly offset by higher costs.",
    "account": "services gross margin percentage",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Services gross margin percentage was flat during the third quarter of 2026 compared to the third quarter of 2025.",
    "paragraph_id": "0000320193-26-000020:mdna:48",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_ai_infrastructure_research_spending",
    "what_changed": "For the quarter and the nine months, the text attributes the R&D increase primarily to higher infrastructure-related costs, including investments in artificial intelligence, and to headcount-related expenses. With Siri AI introduced (mdna:8), this points to continuing AI infrastructure spending.",
    "account": "research and development expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "primarily due to higher infrastructure-related costs, including investments in artificial intelligence, and headcount-related expenses",
    "paragraph_id": "0000320193-26-000020:mdna:54",
    "explanation": false
  },
  {
    "id": "results_against_expectations_sga_increase_without_significant_driver",
    "what_changed": "The text says SG&A increased in the quarter and the nine months. It says the increase came from various factors, none significant individually or in aggregate, and names no driver.",
    "account": "selling, general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increases were driven by various factors, none of which were significant individually or in the aggregate.",
    "paragraph_id": "0000320193-26-000020:mdna:56",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_unrecognized_tax_benefit_changes_lower_tax_rate",
    "what_changed": "For the quarter and the nine months, the rate narrative lists 'changes in unrecognized tax benefits' as part of the lower effective rate on foreign earnings. It also lists the federal R&D credit and share-based compensation benefits, partly offset by state taxes. Unrecognized tax benefits are a judgmental tax reserve, and the text gives no amount for the change.",
    "account": "provision for income taxes (unrecognized tax benefits)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "including the impact of changes in unrecognized tax benefits, the impact of the U.S. federal R&D credit, and tax benefits from share-based compensation",
    "paragraph_id": "0000320193-26-000020:mdna:60",
    "explanation": false
  },
  {
    "id": "earnings_quality_higher_tax_rate_on_foreign_earnings",
    "what_changed": "The text says the third-quarter effective tax rate was higher than in the prior-year quarter, primarily because of a higher effective rate on foreign earnings. It says this was partly offset by changes in unrecognized tax benefits and share-based compensation tax benefits.",
    "account": "effective tax rate",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "was higher compared to the third quarter of 2025 primarily due to a higher effective tax rate on foreign earnings, partially offset by the impact of changes in unrecognized tax benefits and tax benefits from share-based compensation",
    "paragraph_id": "0000320193-26-000020:mdna:61",
    "explanation": false
  },
  {
    "id": "earnings_quality_prior_year_tax_one_offs_in_nine_month_rate_comparison",
    "what_changed": "The text says the nine-month rate was higher and names two items that belong to the comparison period: foreign currency loss regulations issued by Treasury in December 2024, and the tax impact of foreign currency revaluations in the first quarter of 2025 related to the State Aid Decision. Part of the nine-month rate difference therefore comes from prior-year items, not current operations.",
    "account": "effective tax rate (nine months)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the tax impact from foreign currency revaluations in the first quarter of 2025 related to the State Aid Decision",
    "paragraph_id": "0000320193-26-000020:mdna:61",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_manufacturing_purchase_obligations_stated",
    "what_changed": "The text states manufacturing purchase obligations of $57.0 billion as of June 27, 2026, with $56.2 billion payable within 12 months. This commitment sits beside the supply-constraint and component-cost language in mdna:11. Comparing it with the prior amount is the numbers reader's job.",
    "account": "manufacturing purchase obligations (off-balance-sheet)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 27, 2026, the Company had manufacturing purchase obligations of $57.0 billion, with $56.2 billion payable within 12 months.",
    "paragraph_id": "0000320193-26-000020:mdna:66",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_other_purchase_obligations_stated",
    "what_changed": "The text states other purchase obligations of $29.3 billion as of June 27, 2026, with $9.2 billion payable within 12 months. The category list includes 'the acquisition of capital assets related to product manufacturing'. Comparing it with the prior amount is the numbers reader's job.",
    "account": "other purchase obligations (off-balance-sheet)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 27, 2026, the Company had other purchase obligations of $29.3 billion, with $9.2 billion payable within 12 months.",
    "paragraph_id": "0000320193-26-000020:mdna:68",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_deemed_repatriation_tax_fully_paid",
    "what_changed": "The text says that during the first nine months the Company paid the remaining $8.8 billion of the TCJA deemed repatriation tax payable. The liability is described as fully paid, so no further instalments of this tax should appear in cash taxes. The prior-period wording of this paragraph is not in my input.",
    "account": "deemed repatriation tax payable; cash paid for income taxes",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "the Company paid the remaining $8.8 billion balance of the deemed repatriation tax payable imposed by the U.S. Tax Cuts and Jobs Act of 2017",
    "paragraph_id": "0000320193-26-000020:mdna:70",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_quarterly_dividend_rate_stated_in_mdna",
    "what_changed": "The text gives the quarterly cash dividend as $0.27 per share as of June 27, 2026 and repeats the intent to raise it annually, subject to Board declaration. The 8-K (8k_2_02:10) declares $0.27. The prior-period text of this paragraph is not in my input, and a prior capital-return paragraph in this span has no unchanged counterpart (see Insufficient).",
    "account": "dividends and dividend equivalents",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "quarterly cash dividend was $0.27 per share",
    "paragraph_id": "0000320193-26-000020:mdna:72",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_internal_use_software_standard_evaluation",
    "what_changed": "The text says ASU 2025-06 takes effect in the first quarter of 2029, early adoption is permitted, and the Company is evaluating the timing and method of adoption. Under the standard, internal-use software costs are capitalized once the project is committed and completion is probable, which would change when such costs are expensed.",
    "account": "research and development expense (software capitalization)",
    "expected_direction": "none",
    "horizon": "beyond 12 months (first quarter of 2029 unless adopted early)",
    "quote": "The Company is currently evaluating the timing and method of its adoption of ASU 2025-06.",
    "paragraph_id": "0000320193-26-000020:mdna:76",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_expense_disaggregation_adoption_timing",
    "what_changed": "The text states a definite adoption plan for ASU 2024-03 (expense disaggregation): the fourth quarter of 2028, prospective transition. Selling expenses will be defined and disclosed.",
    "account": "operating expense disclosure",
    "expected_direction": "none",
    "horizon": "beyond 12 months (fourth quarter of 2028)",
    "quote": "The Company will adopt ASU 2024-03 in its fourth quarter of 2028 using a prospective transition method.",
    "paragraph_id": "0000320193-26-000020:mdna:78",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_adoption_next_quarter",
    "what_changed": "The text says ASU 2023-09 will be adopted in the fourth quarter of 2026, which is the next reporting period, using a prospective transition method. The rate reconciliation and income taxes paid will then be disaggregated by federal, state, foreign and significant jurisdictions.",
    "account": "income tax disclosures",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The Company will adopt ASU 2023-09 in its fourth quarter of 2026 using a prospective transition method.",
    "paragraph_id": "0000320193-26-000020:mdna:80",
    "explanation": false
  },
  {
    "id": "revenue_recognition_trade_receivables_customer_concentration",
    "what_changed": "The text says that at both June 27, 2026 and September 27, 2025, one customer represented 10% or more of trade receivables, at 18% and 12% respectively. It says cellular network carriers made up 27% and 34%. It repeats that credit support or collateral is required from certain customers. No reason is given, and the prior-quarter wording is not in my input.",
    "account": "accounts receivable, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of both June 27, 2026 and September 27, 2025, the Company had one customer that represented 10% or more of total trade receivables, which accounted for 18% and 12%, respectively.",
    "paragraph_id": "0000320193-26-000020:notes:29",
    "explanation": false
  },
  {
    "id": "earnings_quality_vendor_non_trade_receivables_concentration",
    "what_changed": "The text says two vendors each represented 10% or more of vendor non-trade receivables: 47% and 22% at June 27, 2026, and 46% and 23% at September 27, 2025. It repeats that gains on component sales to these vendors reduce products cost of sales when the related final products are sold. No reason is given.",
    "account": "vendor non-trade receivables",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 27, 2026, the Company had two vendors that individually represented 10% or more of total vendor non-trade receivables, which accounted for 47% and 22%.",
    "paragraph_id": "0000320193-26-000020:notes:31",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_inventory_breakdown_table_added",
    "what_changed": "The Condensed Consolidated Financial Statement Details note now has an Inventories caption and a table splitting components from finished goods (notes:33, notes:34). Neither paragraph refers to a prior-period paragraph. The next caption (notes:35) is marked unchanged from prior notes:33, which indicates the Inventories disclosure was inserted this period. The note history does not cover this block, so I cannot confirm this. No prose goes with the table, and none of the notes or MD&A text I have explains the inventory balance.",
    "account": "inventories",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Inventories",
    "paragraph_id": "0000320193-26-000020:notes:33",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_general_counsel_trading_plan",
    "what_changed": "This is a new trading-arrangement disclosure. On May 5, 2026, Jennifer Newstead, described as Senior Vice President and General Counsel, adopted a Rule 10b5-1 plan. It covers the sale of up to 24,912 shares plus up to 90% of shares vesting from June 15, 2026 to March 15, 2027, net of tax withholding, and expires May 6, 2027. An item 5.02 8-K was filed during the quarter (2026-04-20), but its body is not in my input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The plan provides for the sale, subject to certain price limits, of up to 24,912 shares of common stock, as well as up to 90% of shares vesting between June 15, 2026 and March 15, 2027",
    "paragraph_id": "0000320193-26-000020:notes:62",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_executive_trading_plan",
    "what_changed": "This is a new trading-arrangement disclosure. On May 28, 2026, CEO Tim Cook adopted a Rule 10b5-1 plan. It covers the sale of up to 16,250 shares plus shares vesting during the plan, net of withholding, and gifts of up to 37,104 shares. It expires October 30, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "of up to 16,250 shares of common stock, as well as shares vesting during the duration of the plan pursuant to certain equity awards granted to Mr. Cook",
    "paragraph_id": "0000320193-26-000020:notes:63",
    "explanation": false
  },
  {
    "id": "across_documents_release_headline_revenue_and_eps_records",
    "what_changed": "The release headline claims June-quarter records for total company revenue and EPS. Checking that against the filed history is for the numbers reader and supervisors.",
    "account": "net sales; diluted earnings per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "June quarter records for total company revenue and EPS",
    "paragraph_id": "0000320193-26-000018:8k_2_02:5",
    "explanation": false
  },
  {
    "id": "across_documents_release_category_revenue_records",
    "what_changed": "The release claims June-quarter records for iPhone, Mac and Services revenue. It does not name iPad or Wearables, Home and Accessories. The 10-Q says iPad net sales decreased in the quarter (mdna:35).",
    "account": "iPhone, Mac and Services net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "iPhone, Mac and Services revenue set new June quarter records",
    "paragraph_id": "0000320193-26-000018:8k_2_02:6",
    "explanation": false
  },
  {
    "id": "earnings_quality_tariff_refund_gross_margin_benefit_quantified_in_release",
    "what_changed": "The release says the 50.1% company gross margin includes a favorable impact of about 2 percentage points from tariff refunds. The 10-Q (mdna:13) describes these as refunds of previously paid tariffs recognized when received, so this part of the margin is not operating margin, and whether it recurs depends on further receipts.",
    "account": "gross margin percentage",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Company gross margin was 50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds.",
    "paragraph_id": "0000320193-26-000018:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "earnings_quality_tariff_refund_diluted_eps_benefit_quantified_in_release",
    "what_changed": "The release says diluted EPS of $2.02 included a favorable $0.11 impact from tariff refunds. That is a non-operating recovery sitting inside reported earnings for the quarter.",
    "account": "diluted earnings per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "and included a favorable impact of $0.11 from tariff refunds",
    "paragraph_id": "0000320193-26-000018:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "across_documents_release_claims_double_digit_growth_everywhere",
    "what_changed": "The CEO quote claims double-digit revenue growth across iPhone, Mac and Services and in every geographic segment. Checking this against the segment and category tables is for the numbers reader.",
    "account": "net sales by category and by segment",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "with double-digit revenue growth across iPhone, Mac and Services, and in every geographic segment",
    "paragraph_id": "0000320193-26-000018:8k_2_02:8",
    "explanation": false
  },
  {
    "id": "across_documents_release_claims_operating_cash_flow_record",
    "what_changed": "The CFO quote claims June-quarter records for both EPS and operating cash flow. The release's cash flow statement covers nine months only, and the quarter's operating cash flow figure is not stated anywhere in my input.",
    "account": "cash generated by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "which set new June quarter records for both EPS and operating cash flow",
    "paragraph_id": "0000320193-26-000018:8k_2_02:9",
    "explanation": false
  },
  {
    "id": "results_against_expectations_installed_base_all_time_high",
    "what_changed": "The CFO says the installed base of active devices reached a new all-time high across all major product categories and geographic segments. No number is given. The prose presents this as support for Services.",
    "account": "Services net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Our installed base of active devices also reached a new all-time high across all major product categories and geographic segments.",
    "paragraph_id": "0000320193-26-000018:8k_2_02:9",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter_end",
    "what_changed": "After quarter end, the board declared a cash dividend of $0.27 per share, payable August 13, 2026 to holders of record on August 10, 2026. The payment falls in the fourth fiscal quarter.",
    "account": "dividends and dividend equivalents",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "has declared a cash dividend of $0.27 per share",
    "paragraph_id": "0000320193-26-000018:8k_2_02:10",
    "explanation": false
  }
]
```

## Insufficient

- **Item 1A diff.** Not in my directory. I cannot report any risk-factor change.
- **Exhibit 21 diff.** Not in my directory.
- **Exhibit 10.** None was pulled into my directory.
- **Auditor's report.** input_controls.md contains only Item 4. There is no auditor's report or review report text.
- **8-K item 5.02 filed 2026-04-20 (0001140361-26-015711).** It falls inside the quarter, but only its item code is in my input, not its body. Whether it relates to the officer named in notes:62 cannot be told. The earlier 5.02s (2026-01-02, 2025-12-05) also have no body.
- **Changed MD&A paragraphs, prior text missing.** The prior-period wording of mdna:11, mdna:13, mdna:70, mdna:72 and the driver paragraphs is not in my input. The specific edits cannot be separated from the period roll, so the items describe current wording only.
- **Prior MD&A paragraphs with no unchanged counterpart.** No current paragraph is marked unchanged from prior mdna:8 through prior mdna:14 (current mdna:8 sits in that position), or from prior mdna:78 through prior mdna:80 (current mdna:72 and mdna:73 sit there). Any prior text dropped from these places is not visible to me, including anything in the capital-return section.
- **notes:58 (legal contingencies).** It is carried as text, but the note history for the commitments and contingencies block records no change for it. I cannot tell what, if anything, changed.
- **Inventories disclosure (notes:33, notes:34).** That it is new is inferred from paragraph references only. The note history does not cover this block.

## Text paragraphs not made into items

### Notes

- 0000320193-26-000020:notes:4: date rolled forward (six-month to nine-month lead-in, per note history)
- 0000320193-26-000020:notes:5: amounts only (disaggregated net sales and deferred-revenue portion table)
- 0000320193-26-000020:notes:6: date rolled forward; the Greater China iPhone-share sentence is otherwise as before (note history)
- 0000320193-26-000020:notes:7: amounts and date only; the realization-timing percentages read as before (note history)
- 0000320193-26-000020:notes:8: date rolled forward (EPS table lead-in)
- 0000320193-26-000020:notes:9: amounts only (EPS table)
- 0000320193-26-000020:notes:11: date rolled forward (investment table lead-in)
- 0000320193-26-000020:notes:12: amounts only (cash, cash equivalents and marketable securities table)
- 0000320193-26-000020:notes:15: amounts only (maturity-mix percentages)
- 0000320193-26-000020:notes:20: amounts and date only (recurring hedge-policy sentence with hedge horizon in years)
- 0000320193-26-000020:notes:24: date rolled forward (notional table lead-in)
- 0000320193-26-000020:notes:25: amounts only (derivative notional table)
- 0000320193-26-000020:notes:26: amounts only (term debt subject to fair value hedges)
- 0000320193-26-000020:notes:32: date rolled forward (note lead-in)
- 0000320193-26-000020:notes:34: amounts only (inventory table); its addition is covered by the notes:33 item
- 0000320193-26-000020:notes:36: amounts only (property, plant and equipment table)
- 0000320193-26-000020:notes:38: amounts only (intangible assets table; no prose accompanies it)
- 0000320193-26-000020:notes:39: heading only
- 0000320193-26-000020:notes:40: date rolled forward; commercial paper balances read as in the prior text (note history)
- 0000320193-26-000020:notes:41: amounts only (commercial paper cash-flow table, nine-month columns)
- 0000320193-26-000020:notes:42: caption only
- 0000320193-26-000020:notes:43: amounts only (term debt carrying and fair value, per note history)
- 0000320193-26-000020:notes:45: amounts only (nine-month repurchases); program wording recurring
- 0000320193-26-000020:notes:47: date rolled forward (RSU table lead-in)
- 0000320193-26-000020:notes:48: amounts only (RSU activity table)
- 0000320193-26-000020:notes:49: amounts only (RSU vesting-date fair value)
- 0000320193-26-000020:notes:51: date rolled forward (share-based compensation table lead-in)
- 0000320193-26-000020:notes:52: amounts only (share-based compensation table)
- 0000320193-26-000020:notes:53: amounts only (unrecognized compensation cost and period)
- 0000320193-26-000020:notes:54: heading only
- 0000320193-26-000020:notes:55: reordered (list of obligation types) and date rolled forward (note history)
- 0000320193-26-000020:notes:56: amounts only (unconditional purchase obligation schedule; period label rolled)
- 0000320193-26-000020:notes:57: caption only
- 0000320193-26-000020:notes:58: no change recorded in the note history; standard statement that no reasonably possible material loss exists (also listed under Insufficient)
- 0000320193-26-000020:notes:59: date rolled forward (segment table lead-in)
- 0000320193-26-000020:notes:60: amounts only (segment table, three months)
- 0000320193-26-000020:notes:61: amounts only (segment table, nine months)

### Note change history (each entry is the history of a notes paragraph handled above)

- 0000320193-26-000020:note_history:1: history of notes:55; reordered and date rolled
- 0000320193-26-000013:note_history:1: prior version of notes:55
- 0000320193-26-000020:note_history:2: history of notes:56; amounts only
- 0000320193-26-000013:note_history:2: prior version of notes:56
- 0000320193-26-000020:note_history:3: history of notes:40; date rolled forward
- 0000320193-26-000013:note_history:3: prior version of notes:40
- 0000320193-26-000020:note_history:4: history of notes:41; amounts only (nine-month table)
- 0000320193-26-000020:note_history:5: history of notes:43; amounts only
- 0000320193-26-000013:note_history:5: prior version of notes:43
- 0000320193-26-000013:note_history:6: prior six-month commercial paper table, replaced by the nine-month table; amounts only
- 0000320193-26-000020:note_history:7: history of notes:4; date rolled forward
- 0000320193-26-000013:note_history:7: prior version of notes:4
- 0000320193-26-000020:note_history:8: history of notes:5; amounts only
- 0000320193-26-000013:note_history:8: prior version of notes:5
- 0000320193-26-000020:note_history:9: history of notes:6; date rolled forward
- 0000320193-26-000013:note_history:9: prior version of notes:6
- 0000320193-26-000020:note_history:10: history of notes:7; amounts and date only
- 0000320193-26-000013:note_history:11: prior version of notes:7; amounts and date only

### MD&A

- 0000320193-26-000020:mdna:15: date rolled forward (segment table lead-in)
- 0000320193-26-000020:mdna:16: amounts only (segment net sales table)
- 0000320193-26-000020:mdna:28: date rolled forward (category table lead-in)
- 0000320193-26-000020:mdna:29: amounts only (category net sales table)
- 0000320193-26-000020:mdna:41: date rolled forward (gross margin table lead-in)
- 0000320193-26-000020:mdna:42: amounts only (gross margin table)
- 0000320193-26-000020:mdna:43: amounts only (gross margin percentage table)
- 0000320193-26-000020:mdna:51: date rolled forward (operating expense table lead-in)
- 0000320193-26-000020:mdna:52: amounts only (operating expense table)
- 0000320193-26-000020:mdna:58: date rolled forward (tax table lead-in)
- 0000320193-26-000020:mdna:59: amounts only (tax provision and rate table)
- 0000320193-26-000020:mdna:73: amounts only (the quarter's repurchases and dividends paid)

### Item 4

- 0000320193-26-000020:item_4_controls:1: heading only
- 0000320193-26-000020:item_4_controls:2: heading only
- 0000320193-26-000020:item_4_controls:3: date rolled forward. Disclosure controls are concluded effective as of June 27, 2026, with no qualification, material weakness or remediation language. The prior Item 4 text is not in my input.
- 0000320193-26-000020:item_4_controls:4: heading only
- 0000320193-26-000020:item_4_controls:5: date rolled forward; no material change in internal control over financial reporting during the third quarter
- 0000320193-26-000020:item_4_controls:6: page footer

### 8-K (0000320193-26-000018, item 2.02)

- 0000320193-26-000018:8k_2_02:1: exhibit file header
- 0000320193-26-000018:8k_2_02:2: document header
- 0000320193-26-000018:8k_2_02:3: exhibit label
- 0000320193-26-000018:8k_2_02:4: release title
- 0000320193-26-000018:8k_2_02:11: conference-call logistics
- 0000320193-26-000018:8k_2_02:12: investor-website boilerplate
- 0000320193-26-000018:8k_2_02:13: company-description boilerplate
- 0000320193-26-000018:8k_2_02:14: press contact label
- 0000320193-26-000018:8k_2_02:15: contact name
- 0000320193-26-000018:8k_2_02:16: contact affiliation
- 0000320193-26-000018:8k_2_02:17: contact email
- 0000320193-26-000018:8k_2_02:18: contact phone
- 0000320193-26-000018:8k_2_02:19: investor relations contact label
- 0000320193-26-000018:8k_2_02:20: contact name
- 0000320193-26-000018:8k_2_02:21: contact affiliation
- 0000320193-26-000018:8k_2_02:22: contact email
- 0000320193-26-000018:8k_2_02:23: contact phone
- 0000320193-26-000018:8k_2_02:24: note to editors boilerplate
- 0000320193-26-000018:8k_2_02:25: copyright and trademark boilerplate
- 0000320193-26-000018:8k_2_02:26: statement header
- 0000320193-26-000018:8k_2_02:27: statement header
- 0000320193-26-000018:8k_2_02:28: units line
- 0000320193-26-000018:8k_2_02:29: amounts only (statement of operations with segment and category sales)
- 0000320193-26-000018:8k_2_02:30: statement header
- 0000320193-26-000018:8k_2_02:31: statement header
- 0000320193-26-000018:8k_2_02:32: units line
- 0000320193-26-000018:8k_2_02:33: amounts only (balance sheet)
- 0000320193-26-000018:8k_2_02:34: statement header
- 0000320193-26-000018:8k_2_02:35: statement header
- 0000320193-26-000018:8k_2_02:36: units line
- 0000320193-26-000018:8k_2_02:37: amounts only (nine-month cash flow statement)
- 8-K item-code list and late-filing section (no paragraph ids): no late-filing notification on or before 2026-07-31; the in-quarter 5.02 is listed under Insufficient
