<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# NTAP — notes text reader — 10-Q 0001193125-26-380207 (quarter ended July 31, 2026)

## Scope check

- Read in full: input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md (all 908 lines), input_prior_predictions.md.
- Comparison base: the diff markers point to the prior 10-Q, 0001193125-26-076622 (quarter ended January 23, 2026).
- Nothing out of scope is in the directory. There is no trend table, no price, return or short-interest data, no other company's files, no prior-run probability and no outcome window. The 8-K earnings release includes the company's own statements, guidance and supplemental metrics (DSO, DPO, inventory turns, free cash flow margin). These are part of the 8-K body. I read them as text only and did no arithmetic on them.
- Not in the input: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report. input_controls.md is titled to include an auditor's report, but it contains only Item 4. None of the items below comes from those sources.
- Prior flags: none on record (input_prior_predictions.md).

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_fourteen_week_first_quarter",
    "what_changed": "The basis-of-presentation note now says fiscal 2027 is a 53-week year, with 14 weeks in its first quarter and 13 in each later quarter. The prior text described fiscal 2026 and 2025 as 52-week years with 13 weeks in each quarter. So this quarter is set against a 13-week prior-year quarter, and next quarter goes back to 13 weeks. MD&A repeats the sentence at mdna:26.",
    "account": "net revenues; operating expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Fiscal 2027, ending on April 30, 2027, is a 53-week year, with 14 weeks included in its first quarter and 13 weeks in each subsequent quarter.",
    "paragraph_id": "0001193125-26-380207:notes:4",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_datapelago_acquisition",
    "what_changed": "A new Note 3 reports the July 16, 2026 purchase of DataPelago, Inc. for $193 million, with $87 million paid in cash at closing. The preliminary allocation table (notes:14) puts $151 million in goodwill and $22 million in developed technology. The goodwill roll-forward (notes:20) shows the additions split between Hybrid Cloud and Public Cloud. MD&A (mdna:119, mdna:127) gives $78 million paid net of cash acquired.",
    "account": "goodwill and purchased intangible assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "On July 16, 2026, we acquired all the outstanding shares of DataPelago, Inc., (DataPelago), a privately-held company, for $193 million, of which $87 million was paid in cash at closing.",
    "paragraph_id": "0001193125-26-380207:notes:12",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_datapelago_contingent_consideration_accrued",
    "what_changed": "The note says $106 million of the purchase price is contingent consideration. It sits in accrued expenses and is paid only if criteria in the merger agreement are met. The supplemental cash flow table (notes:40) adds a new non-cash line, 'Liabilities incurred to former owners of acquired business'. MD&A (mdna:22) says the remainder will be paid in a future period if the criteria are achieved. None of the documents describes the criteria.",
    "account": "accrued expenses (contingent consideration liability)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The remaining $106 million represents contingent consideration, which we recognized in accrued expenses in our condensed consolidated balance sheet, and which will be paid if certain criteria as defined in the merger agreement are achieved.",
    "paragraph_id": "0001193125-26-380207:notes:12",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_contingent_consideration_level_three_valuation",
    "what_changed": "The fair value table for July 31, 2026 (notes:54) now has a Level 3 column, with a Level 3 contingent consideration liability. The April 24, 2026 table (notes:55) has only Level 1 and Level 2 columns. The note says the liability was valued with a probability-weighted discounted cash flow model. It does not give the probabilities, the discount rate, or where remeasurement changes will be recorded.",
    "account": "accrued expenses (contingent consideration liability)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Our contingent consideration liability is related to the acquisition of DataPelago and was valued using a probability-weighted discounted cash flow model.",
    "paragraph_id": "0001193125-26-380207:notes:59",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_datapelago_developed_technology_useful_life",
    "what_changed": "The note says the acquisition created a developed technology intangible with an estimated useful life of five years. Amortization runs from the July 16, 2026 acquisition date, so next quarter is the first full quarter of amortization on this asset.",
    "account": "amortization of intangible assets",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The acquisition resulted in the recognition of a developed technology intangible asset with an estimated useful life of five years.",
    "paragraph_id": "0001193125-26-380207:notes:15",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_datapelago_preliminary_allocation_goodwill_split",
    "what_changed": "The note says the purchase price allocation is preliminary and may be revised within a measurement period of up to 12 months, and that the split of goodwill among reporting units may also be revised. Per notes:15, the goodwill was split between the Hybrid Cloud and Public Cloud reporting units, is not deductible for income tax purposes, and the values were set with help from third-party valuation specialists.",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The purchase price allocation is preliminary and subject to revision as additional information about the fair value of acquired assets and liabilities assumed becomes available during the remainder of the measurement period, a period not to exceed 12 months from the acquisition date.",
    "paragraph_id": "0001193125-26-380207:notes:16",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_datapelago_no_pro_forma",
    "what_changed": "The note says no pro forma results are presented because the acquisition's impact was not material to consolidated results. DataPelago's results are included from the acquisition date.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Pro forma results of operations have not been presented because the impact from the acquisition was not material to our consolidated results of operations.",
    "paragraph_id": "0001193125-26-380207:notes:17",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_additional_repurchase_authorization",
    "what_changed": "The equity note now says the Board authorized another $1.0 billion of repurchases on May 21, 2026. The repurchase table (notes:78) shows $1,302 million remaining at July 31, 2026, and MD&A (mdna:151) gives $1.3 billion. The quarter's repurchases were 1.5 million shares for $200 million (mdna:20).",
    "account": "common stock repurchases; diluted share count",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "On May 21, 2026, our Board of Directors authorized the repurchase of an additional $1.0 billion of our common stock.",
    "paragraph_id": "0001193125-26-380207:notes:79",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_dividends_charged_to_retained_earnings",
    "what_changed": "The dividend table puts this quarter's dividend payments in retained earnings, with none in additional paid-in capital. The prior-year column does the reverse: all to additional paid-in capital, none to retained earnings. The repurchase table (notes:78) also splits repurchases between additional paid-in capital and retained earnings. The notes do not explain the allocation.",
    "account": "retained earnings; additional paid-in capital",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Dividend payments allocated to retained earnings",
    "paragraph_id": "0001193125-26-380207:notes:82",
    "explanation": false
  },
  {
    "id": "earnings_quality_discrete_tax_benefits_stock_compensation",
    "what_changed": "The tax note now says this quarter's effective tax rate includes higher discrete tax benefits from stock-based compensation than the prior-year quarter. MD&A repeats this at mdna:113. So part of the period's rate comes from a discrete item rather than from the recurring drivers the note lists (foreign earnings taxed at lower rates, offset by non-deductible stock compensation and state taxes).",
    "account": "provision for income taxes",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Our effective tax rate for the three months ended July 31, 2026 includes an increase in discrete tax benefits related to stock-based compensation compared to the corresponding period of the prior year.",
    "paragraph_id": "0001193125-26-380207:notes:98",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_restructuring_plan_reduce_costs",
    "what_changed": "MD&A reports a new restructuring plan executed in the first quarter of fiscal 2027 to redirect resources and reduce costs, with $56 million of charges recorded in the quarter. It comes in a quarter the earnings release calls a record. The release's non-GAAP measures exclude these charges.",
    "account": "restructuring charges",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In the first quarter of fiscal 2027, we executed a restructuring plan to redirect resources to highest return activities and reduce costs.",
    "paragraph_id": "0001193125-26-380207:mdna:24",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_restructuring_reserve_severance_payout",
    "what_changed": "The restructuring note says the new plan's charges were mainly employee severance and that the activities should be substantially complete by the end of fiscal 2027. Per notes:94, the liability is carried in accrued expenses. The roll-forward (notes:93) shows $56 million of net charges, $22 million of cash payments and a $40 million balance at July 31, 2026. Management attributes the charge to severance. The remaining balance should be paid out as the plan finishes.",
    "account": "accrued expenses (restructuring liability)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Charges related to the plan consisted primarily of employee severance-related costs. The activities under the plan are expected to be substantially complete by the end of fiscal 2027.",
    "paragraph_id": "0001193125-26-380207:notes:91",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_inventory_purchase_commitments_amount",
    "what_changed": "The commitments note now gives $1.9 billion of non-cancelable purchase commitments for inventory at July 31, 2026. The prior text gave $0.7 billion at January 23, 2026. The note gives no reason for the amount. Separately, MD&A (mdna:13, mdna:124) describes tight supply, higher memory and component costs, and more strategic component purchases. Comparing the two amounts is left to the numbers reader.",
    "account": "non-cancelable inventory purchase commitments (off-balance-sheet); inventories",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of July 31, 2026, we had $1.9 billion in non-cancelable purchase commitments for inventory.",
    "paragraph_id": "0001193125-26-380207:notes:129",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_excess_purchase_commitment_liability_disclosure_removed",
    "what_changed": "The commitments note no longer contains three things the prior text had. First, the sentence saying a liability is recorded for non-cancelable purchase commitments above demand forecasts, consistent with excess and obsolete inventory valuation. Second, its amount: $26 million at January 23, 2026 and $22 million at April 25, 2025, in accrued expenses. Third, the warning that commitments and accruals may change if forecasts are missed. The current note gives no amount for this liability and does not say whether one is still recorded. The commitment amount stated in the same paragraph is itemized separately above.",
    "account": "accrued expenses (excess purchase commitment liability); inventory valuation",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We record a liability for firm, non-cancelable and unconditional purchase commitments for quantities in excess of our future demand forecasts consistent with the valuation of our excess and obsolete inventory.",
    "paragraph_id": "0001193125-26-076622:note_history:2",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_purchase_commitments_twelve_month_timing",
    "what_changed": "New sentence: of the $2.3 billion of purchase commitments, $2.1 billion is due in the next twelve months and the rest after that. MD&A (mdna:153) gives the same figures and calls these off-balance sheet purchase commitments.",
    "account": "purchase commitments (off-balance-sheet); cash",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Of the total $2.3 billion in purchase commitments, $2.1 billion is due in the next twelve months, with the remainder due thereafter.",
    "paragraph_id": "0001193125-26-380207:notes:131",
    "explanation": false
  },
  {
    "id": "revenue_recognition_customer_financing_receivable_sales_disclosure_removed",
    "what_changed": "The Financing Guarantees section is gone. Its first paragraph said the company sometimes gives long-term financing to creditworthy customers and generally sells those receivables, without recourse, to third-party financing institutions within 10 days. It said $25 million and $42 million of receivables were sold in the nine months ended January 23, 2026 and January 24, 2025. The current notes say nothing about customer financing or receivable sales for this quarter.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "While most of our arrangements for sales include short-term payment terms, from time to time we provide long-term financing to creditworthy customers.",
    "paragraph_id": "0001193125-26-076622:note_history:8",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_recourse_lease_guarantee_disclosure_removed",
    "what_changed": "Also removed with the Financing Guarantees section: the description of hardware sales through leasing companies (076622:note_history:9). Removed with it: the statement that some of those leases are financed with recourse, so the company stays liable for unpaid lease payments if the end user defaults. Also gone: the statement that the exposure above the related liabilities was not significant. The current commitments note has no guarantee disclosure.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Under the terms of recourse leases, which are generally three years or less, we remain liable for the aggregate unpaid remaining lease payments to the third-party leasing companies in the event of end-user customer default.",
    "paragraph_id": "0001193125-26-076622:note_history:10",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_service_contract_financing_disclosure_removed",
    "what_changed": "Removed: the disclosure that some customer service contracts are backed by third-party financing. Under these, the company could have to acquire assets or pay the unpaid financing payments if a contract ends because of its own non-performance. Also removed: the statements that no payments had been required and that the likelihood was considered remote.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "If a service contract is terminated as a result of our non-performance under the contract or our failure to comply with the terms of the financing arrangement, we could, under certain circumstances, be required to acquire certain assets related to the service contract or to pay the aggregate unpaid financing payments under such arrangements.",
    "paragraph_id": "0001193125-26-076622:note_history:11",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_debt_maturity_schedule_removed",
    "what_changed": "The financing note no longer has the table of future principal debt maturities by fiscal year. Instead, the debt table (notes:65) now shows the 2.375% Senior Notes due June 2027 as current portion of long-term debt.",
    "account": "long-term debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of January 23, 2026, our aggregate future principal debt maturities are as follows (in millions):",
    "paragraph_id": "0001193125-26-076622:note_history:23",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_ceo_trading_arrangement",
    "what_changed": "New disclosure: on June 15, 2026, CEO George Kurian adopted a Rule 10b5-1 trading arrangement. It allows sales of up to 150,000 shares and expires June 15, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On June 15, 2026, George Kurian, Chief Executive Officer of the Company, entered into a Rule 10b5-1 trading arrangement intended to satisfy the affirmative defense conditions of Rule 10b5-1(c) promulgated under the Exchange Act.",
    "paragraph_id": "0001193125-26-380207:notes:137",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_audit_committee_chair_trading_arrangement",
    "what_changed": "New disclosure: on June 15, 2026, Audit Committee Chair Deepak Ahuja adopted a Rule 10b5-1 trading arrangement. It allows sales of up to 11,683 shares and expires June 15, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "An aggregate of up to 11,683 shares may be sold pursuant to the trading arrangement.",
    "paragraph_id": "0001193125-26-380207:notes:138",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_component_cost_increases",
    "what_changed": "The Supply Chain section says inflation and supply constraints continued to affect operations in the quarter. It says higher memory and component costs have hurt gross margins, and that costs should stay elevated or keep rising in the near term.",
    "account": "cost of product revenues",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We have experienced increased costs for memory and other components, which have affected our gross margins, and we expect costs will remain elevated, or continue to increase, in the near term.",
    "paragraph_id": "0001193125-26-380207:mdna:13",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_tight_supply_limits_fulfillment",
    "what_changed": "The Supply Chain section says supply of specific products is tight, is expected to stay tight, and could make it hard to meet customer demand for those products.",
    "account": "product revenues",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Additionally, the tight supply environment for specific products, which is anticipated to persist, could pose challenges in meeting customer demand for those products.",
    "paragraph_id": "0001193125-26-380207:mdna:13",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_price_increases_to_offset_costs",
    "what_changed": "MD&A says prices were raised in the fourth quarter of fiscal 2026 and again at the start of the second quarter of fiscal 2027. It expects further price changes as needed to offset rising costs, and says customers need time to adjust. It does not say whether customers bought ahead of the second-quarter increase.",
    "account": "product revenues (selling prices)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We raised our pricing in the fourth quarter of fiscal 2026 and at the beginning of the second quarter of fiscal 2027, in line with market trends.",
    "paragraph_id": "0001193125-26-380207:mdna:15",
    "explanation": false
  },
  {
    "id": "results_against_expectations_product_revenue_supported_by_price_increases",
    "what_changed": "MD&A credits the product revenue increase mainly to higher all-flash array sales, helped by the fourth-quarter fiscal 2026 price increases. The all-flash mix explanation (mdna:52, mdna:53) gives the same price-increase cause.",
    "account": "product revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Total product revenues increased in the first quarter of fiscal 2027 compared to the corresponding period of the prior year primarily due to higher revenues from sales of all-flash array systems, supported by the price increases we implemented in the fourth quarter of fiscal 2026.",
    "paragraph_id": "0001193125-26-380207:mdna:39",
    "explanation": false
  },
  {
    "id": "earnings_quality_extra_week_services_revenue",
    "what_changed": "MD&A says the extra week added about $65 million of services revenue in the quarter. It also says product revenue's share of net revenues increased by seven percentage points. The prose names only services revenue as receiving an extra-week contribution.",
    "account": "services revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The extra week in the first quarter of fiscal 2027 contributed approximately $65 million of additional services revenues to that period.",
    "paragraph_id": "0001193125-26-380207:mdna:33",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_support_growth_primarily_extra_week",
    "what_changed": "MD&A says the support revenue increase came mainly from the extra week, about $50 million. Higher aggregate support contract value on the installed base is named only 'to a lesser extent'. The second quarter has 13 weeks and will not get this boost.",
    "account": "support revenues",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Support revenues increased in the first quarter of fiscal 2027 compared to the corresponding period of the prior year, primarily due to an additional week in the current year period, which contributed approximately $50 million of additional revenues and, to a lesser extent, a higher aggregate support contract value for our installed base.",
    "paragraph_id": "0001193125-26-380207:mdna:44",
    "explanation": false
  },
  {
    "id": "revenue_recognition_keystone_professional_services_growth",
    "what_changed": "MD&A says the increase in professional and other services revenue came mainly from higher revenue from the Keystone storage-as-a-service offering.",
    "account": "professional and other services revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Professional and other services revenues increased in the first quarter of fiscal 2027 compared to the corresponding period of the prior year primarily due to an increase in revenues from our Keystone storage-as-a-service offering.",
    "paragraph_id": "0001193125-26-380207:mdna:45",
    "explanation": false
  },
  {
    "id": "results_against_expectations_public_cloud_demand_and_extra_week",
    "what_changed": "MD&A credits the Public Cloud revenue increase to higher customer demand as the cloud market grew, and to the extra week, which added about $15 million.",
    "account": "public cloud revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Public Cloud revenues increased in the first quarter of fiscal 2027 compared to the corresponding period of the prior year, due to higher customer demand driven by overall growth in the cloud market, and an additional week in the period, which contributed approximately $15 million of additional revenues.",
    "paragraph_id": "0001193125-26-380207:mdna:48",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_slower_americas_commercial_growth",
    "what_changed": "MD&A says every region grew in dollars, but APAC and EMEA grew at a higher rate than the Americas, mainly because Americas Commercial grew more slowly. It says this shifted the geographic mix.",
    "account": "Americas Commercial revenues (share of net revenues)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "APAC and EMEA revenues grew at a higher rate than Americas revenues (primarily due to slower Americas Commercial growth), resulting in a minor shift in geographical revenue mix.",
    "paragraph_id": "0001193125-26-380207:mdna:57",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_materials_costs_component_costs",
    "what_changed": "MD&A says materials costs increased by $152 million, mainly because of higher product revenue and higher component costs. The paragraph before (mdna:65) puts materials at 94% of Hybrid Cloud product cost of revenues this quarter, against 89% a year earlier.",
    "account": "cost of product revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Materials costs increased by $152 million in the first quarter of fiscal 2027 compared to the corresponding period of the prior year, primarily reflecting the increase in product revenues and higher component costs.",
    "paragraph_id": "0001193125-26-380207:mdna:66",
    "explanation": false
  },
  {
    "id": "results_against_expectations_product_margin_flat_prices_offset_costs",
    "what_changed": "MD&A says Hybrid Cloud product gross margins were relatively flat because higher selling prices offset higher component costs.",
    "account": "product gross margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Hybrid Cloud product gross margins were relatively flat in the first quarter of fiscal 2027 compared to the corresponding period of the prior year primarily reflecting higher selling prices offset by higher component costs.",
    "paragraph_id": "0001193125-26-380207:mdna:67",
    "explanation": false
  },
  {
    "id": "results_against_expectations_professional_services_margin_mix",
    "what_changed": "MD&A says Hybrid Cloud support gross margins rose marginally, and professional and other services gross margins rose seven percentage points, mainly because of the mix of services provided.",
    "account": "professional and other services gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Hybrid Cloud professional and other services gross margins increased by seven percentage points in the first quarter of fiscal 2027 compared to the corresponding period of the prior year primarily due to the mix of services provided.",
    "paragraph_id": "0001193125-26-380207:mdna:75",
    "explanation": false
  },
  {
    "id": "earnings_quality_public_cloud_margin_lower_depreciation",
    "what_changed": "MD&A says Public Cloud gross margins rose six percentage points. It says both the lower cost of Public Cloud revenues and the better margin came mainly from cost optimization, including lower depreciation of fixed assets. It does not say why depreciation fell: no asset retirements, impairments or changes in useful lives are mentioned.",
    "account": "cost of public cloud revenues (depreciation)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The decrease in cost of Public Cloud revenues and improved gross margins were primarily due to cost optimization that included a decrease in fixed assets depreciation.",
    "paragraph_id": "0001193125-26-380207:mdna:78",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_higher_incentive_compensation",
    "what_changed": "MD&A says total compensation in sales and marketing, research and development, and general and administrative expenses increased by $75 million, or 15%. It attributes this mainly to higher incentive compensation and the extra week. The line-by-line explanations (mdna:91, mdna:95, mdna:99) each name higher incentive compensation as the main driver. Incentive compensation is an accrual that depends on expected performance.",
    "account": "operating expenses (incentive compensation accrual)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Total compensation costs included in sales and marketing, research and development and general and administrative expenses increased by $75 million, or 15%, in the first quarter of fiscal 2027 compared to the corresponding period of the prior year, primarily attributable to higher incentive compensation expense and the impact of one additional week in the first quarter of fiscal 2027.",
    "paragraph_id": "0001193125-26-380207:mdna:85",
    "explanation": false
  },
  {
    "id": "earnings_quality_extra_week_operating_expenses",
    "what_changed": "MD&A says the extra week added about $22 million of sales and marketing, research and development, and general and administrative expenses.",
    "account": "operating expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The extra week in the first quarter of fiscal 2027 contributed approximately $22 million of additional sales and marketing, research and development and general administrative expenses in that period.",
    "paragraph_id": "0001193125-26-380207:mdna:86",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_lower_average_cash_interest_income",
    "what_changed": "MD&A attributes the lower interest income to lower average cash and investment balances.",
    "account": "interest income",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Interest income decreased in the first quarter of fiscal 2027 compared to the corresponding period of the prior year, primarily due to lower average cash and investment balances.",
    "paragraph_id": "0001193125-26-380207:mdna:108",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_june_twenty_twenty_seven_notes_reclassified_current",
    "what_changed": "MD&A puts working capital at $1.1 billion on July 31, 2026, a decrease of $651 million from April 24, 2026. It says this is mainly because the $550 million of 2.375% Senior Notes due June 2027 moved from long-term to current liabilities. The debt table (notes:65) now shows a $550 million current portion. MD&A (mdna:130) says the company may raise debt, including to refinance upcoming maturities.",
    "account": "current portion of long-term debt",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our working capital was $1.1 billion as of July 31, 2026, a decrease of $651 million compared to April 24, 2026, primarily due to the reclassification of $550 million principal amount of our 2.375% Senior Notes due in June 2027 from long-term to current liabilities in the first quarter of fiscal 2027.",
    "paragraph_id": "0001193125-26-380207:mdna:119",
    "explanation": false
  },
  {
    "id": "revenue_recognition_receivables_decrease_invoicing_linearity",
    "what_changed": "MD&A says accounts receivable decreased by $317 million, mainly because invoicing was more evenly spread (more favorable linearity) in the first quarter of fiscal 2027 than in the fourth quarter of fiscal 2026.",
    "account": "accounts receivable",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Accounts receivable decreased by $317 million, primarily reflecting more favorable invoicing linearity in the first quarter of fiscal 2027 compared to the fourth quarter of fiscal 2026.",
    "paragraph_id": "0001193125-26-380207:mdna:123",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_inventory_build_strategic_component_purchases",
    "what_changed": "MD&A says inventories increased by $176 million, mainly from more strategic component purchases and more finished goods held to meet customer demand. The inventory table (notes:28) shows purchased components and finished goods at July 31, 2026. MD&A does not say whether the purchases were made ahead of the cost and price increases it describes in mdna:13 and mdna:15.",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Inventories increased by $176 million, primarily due to higher strategic purchases of components and an increase in finished goods to fulfill customer demand.",
    "paragraph_id": "0001193125-26-380207:mdna:124",
    "explanation": true
  },
  {
    "id": "results_against_expectations_raised_full_year_guidance",
    "what_changed": "The earnings release says fiscal 2027 revenue and EPS guidance was significantly raised. The full-year outlook (8k_2_02:23) is net revenues of $7.975 billion to $8.225 billion, GAAP EPS of $7.35 to $7.65 and non-GAAP EPS of $9.73 to $10.03. The earlier guidance is not in the input.",
    "account": "net revenues; earnings per share",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Significantly raised fiscal year 2027 revenue and earnings per share guidance",
    "paragraph_id": "0001002047-26-000003:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "results_against_expectations_exceeded_guidance_every_metric",
    "what_changed": "The CEO is quoted saying the quarter beat guidance on every metric and was the strongest first quarter ever. The headlines cite record net revenues of $2.03 billion (8k_2_02:5) and record non-GAAP EPS of $2.58 (8k_2_02:6). The guidance it beat is not in the input.",
    "account": "net revenues; earnings per share",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "NetApp delivered a record-setting start to the year, exceeding guidance on every metric and achieving our strongest first quarter ever",
    "paragraph_id": "0001002047-26-000003:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "results_against_expectations_second_quarter_guidance_ranges",
    "what_changed": "The release gives second-quarter fiscal 2027 guidance: net revenues of $2.025 billion to $2.175 billion; GAAP gross margin of 66.0% to 67.0% (non-GAAP 67.0% to 68.0%); GAAP operating margin of 24.9% to 25.9% (non-GAAP 30.9% to 31.9%); GAAP EPS of $1.97 to $2.07 (non-GAAP $2.54 to $2.64). The prose makes no comparison with the first quarter. That comparison is for the numbers reader.",
    "account": "net revenues; gross margin; operating margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The Company provided the following financial guidance for the second quarter of fiscal year 2027:",
    "paragraph_id": "0001002047-26-000003:8k_2_02:21",
    "explanation": false
  },
  {
    "id": "across_documents_extra_week_absent_from_earnings_release",
    "what_changed": "The release headlines record revenue up 30% year over year and the 'strongest first quarter ever'. Nowhere does it say the quarter had 14 weeks against 13 in the prior-year quarter. The 10-Q does: it states the extra week (notes:4) and gives amounts for its contribution to services, support and Public Cloud revenue and to operating expenses (mdna:33, mdna:44, mdna:48, mdna:86).",
    "account": "net revenues",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Delivers record quarterly net revenues of $2.03 billion, an increase of 30% year-over-year;",
    "paragraph_id": "0001002047-26-000003:8k_2_02:5",
    "explanation": false
  },
  {
    "id": "revenue_recognition_billings_and_deferred_revenue_increase",
    "what_changed": "The release reports billings of $2.06 billion, up 36% year over year. Billings is non-GAAP: net revenues plus the change in total deferred revenue, per 8k_2_02:63. The release's reconciliation (8k_2_02:109) shows the deferred revenue change used.",
    "account": "deferred revenue (billings)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Billings of $2.06 billion for the first quarter of fiscal year 2027, an increase of 36% year-over-year",
    "paragraph_id": "0001002047-26-000003:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_chief_partner_officer_appointed",
    "what_changed": "The release reports that Alvaro Celis was appointed Chief Partner and Ecosystem Officer. His mandate includes modernizing partner incentive programs. The release gives no financial terms. The 8-K item list shows no Item 5.02 filing after January 12, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "NetApp appointed Alvaro Celis as Chief Partner and Ecosystem Officer to lead partner ecosystems, modernize incentive programs, improve partner satisfaction, and drive growth.",
    "paragraph_id": "0001002047-26-000003:8k_2_02:46",
    "explanation": false
  },
  {
    "id": "results_against_expectations_no_restructuring_in_second_quarter_guidance",
    "what_changed": "The second-quarter EPS guidance reconciliation adjusts only for amortization of intangible assets, stock-based compensation and income tax effects. It has no restructuring line. The full-year reconciliations (8k_2_02:117, 8k_2_02:118) do include restructuring charges. The release does not say whether more restructuring charges are expected.",
    "account": "restructuring charges",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Adjustments of Specific Items to Net Income",
    "paragraph_id": "0001002047-26-000003:8k_2_02:116",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### Notes (input_notes.md)

- `0001193125-26-380207:notes:2` — business description reworded (old text at 076622:note_history:16); wording only
- `0001193125-26-380207:notes:5` — basis of presentation; reference year and periods rolled forward
- `0001193125-26-380207:notes:6` — use of estimates; same list of estimates, as-of date rolled forward
- `0001193125-26-380207:notes:7` — heading
- `0001193125-26-380207:notes:8` — insufficient: pending ASU 2025-06 (internal-use software), still under evaluation; prior wording not in input, so the change can't be identified
- `0001193125-26-380207:notes:9` — insufficient: pending ASU 2024-03 (expense disaggregation), still under evaluation; prior wording not in input
- `0001193125-26-380207:notes:10` — heading of the new Business Combination note; its content is itemized
- `0001193125-26-380207:notes:11` — heading
- `0001193125-26-380207:notes:13` — table caption; the allocation is itemized
- `0001193125-26-380207:notes:14` — preliminary allocation table; amounts only, cited in the DataPelago items
- `0001193125-26-380207:notes:18` — heading
- `0001193125-26-380207:notes:19` — table caption
- `0001193125-26-380207:notes:20` — goodwill roll-forward; amounts only (additions are the DataPelago goodwill already itemized)
- `0001193125-26-380207:notes:22` — purchased intangibles table; amounts only
- `0001193125-26-380207:notes:23` — heading
- `0001193125-26-380207:notes:26` — cash and restricted cash table; amounts only
- `0001193125-26-380207:notes:28` — inventories table; amounts only (cause itemized from mdna:124)
- `0001193125-26-380207:notes:30` — property and equipment table; amounts only
- `0001193125-26-380207:notes:32` — accrued expenses table; amounts only
- `0001193125-26-380207:notes:33` — heading
- `0001193125-26-380207:notes:34` — insufficient: definition of deferred revenue; prior wording not in input; no amount or new policy stated
- `0001193125-26-380207:notes:35` — revenue recognized from opening deferred revenue; recurring sentence, amounts and periods rolled
- `0001193125-26-380207:notes:37` — remaining performance obligations; recurring sentence, amount and percentage updated (amounts only)
- `0001193125-26-380207:notes:39` — table caption
- `0001193125-26-380207:notes:40` — supplemental cash flow table; amounts only (the new non-cash line is the contingent consideration already itemized)
- `0001193125-26-380207:notes:41` — heading
- `0001193125-26-380207:notes:48` — table caption; dates rolled
- `0001193125-26-380207:notes:49` — investments at cost table; amounts only
- `0001193125-26-380207:notes:51` — debt investment maturity statement; date rolled forward
- `0001193125-26-380207:notes:53` — table caption
- `0001193125-26-380207:notes:54` — July 31, 2026 fair value table; amounts only (Level 3 row itemized from notes:59)
- `0001193125-26-380207:notes:55` — April 24, 2026 fair value table; amounts only
- `0001193125-26-380207:notes:61` — fair value of debt; amounts and dates rolled
- `0001193125-26-380207:notes:62` — heading
- `0001193125-26-380207:notes:63` — heading
- `0001193125-26-380207:notes:64` — table caption
- `0001193125-26-380207:notes:65` — debt table; the move of the June 2027 notes to current is itemized from mdna:119
- `0001193125-26-380207:notes:66` — heading
- `0001193125-26-380207:notes:67` — standing description of Senior Notes ranking and interest; not listed as changed in the note change history
- `0001193125-26-380207:notes:68` — redemption and covenant terms; date rolled forward
- `0001193125-26-380207:notes:69` — heading reordered (was "Commercial Paper Program and Credit Facility")
- `0001193125-26-380207:notes:70` — credit facility; "In connection with the Program," dropped and date rolled; wording only
- `0001193125-26-380207:notes:71` — commercial paper program; "also" added and dates rolled; wording only
- `0001193125-26-380207:notes:73` — heading
- `0001193125-26-380207:notes:74` — RSU grants and unrecognized compensation; recurring sentence, amounts rolled
- `0001193125-26-380207:notes:76` — standing description of how repurchases may be made
- `0001193125-26-380207:notes:77` — table caption
- `0001193125-26-380207:notes:78` — repurchase activity table; amounts only (allocation covered at notes:82, remaining authorization at notes:79)
- `0001193125-26-380207:notes:83` — recurring quarterly dividend declaration; dates rolled forward
- `0001193125-26-380207:notes:84` — derivatives policy; dates rolled forward
- `0001193125-26-380207:notes:86` — notional amounts table; amounts only
- `0001193125-26-380207:notes:87` — insufficient: presentation sentence for cash flow hedges; prior wording not in input; no amount or policy change stated
- `0001193125-26-380207:notes:88` — table caption
- `0001193125-26-380207:notes:89` — derivative gain/loss table; amounts only
- `0001193125-26-380207:notes:93` — restructuring liability roll-forward; amounts only (cited in the restructuring reserve item)
- `0001193125-26-380207:notes:94` — standing statement that restructuring liabilities sit in accrued expenses
- `0001193125-26-380207:notes:97` — effective tax rate table; amounts only
- `0001193125-26-380207:notes:99` — OBBB legislation; period rolled forward, same no-material-impact conclusion
- `0001193125-26-380207:notes:100` — Pillar Two; as-of date rolled forward; no development after the January 5, 2026 guidance described
- `0001193125-26-380207:notes:102` — insufficient: statement on monitoring tax authority discussions and statute expirations; prior wording not in input; no amount stated
- `0001193125-26-380207:notes:105` — EPS table; amounts only
- `0001193125-26-380207:notes:107` — antidilutive shares table; amounts only
- `0001193125-26-380207:notes:109` — segment description, first half of a paragraph split by a page break; standing
- `0001193125-26-380207:notes:110` — rest of the same split paragraph; standing
- `0001193125-26-380207:notes:114` — table caption
- `0001193125-26-380207:notes:115` — segment table, current quarter; amounts only
- `0001193125-26-380207:notes:116` — segment table, prior-year quarter; amounts only
- `0001193125-26-380207:notes:117` — table caption
- `0001193125-26-380207:notes:118` — storage category table; amounts only
- `0001193125-26-380207:notes:119` — heading
- `0001193125-26-380207:notes:121` — geographic revenue table; amounts only
- `0001193125-26-380207:notes:122` — U.S. sales; amounts and periods rolled
- `0001193125-26-380207:notes:124` — caption: two distributors above 10% of revenue; standing
- `0001193125-26-380207:notes:125` — revenue concentration percentages; amounts only
- `0001193125-26-380207:notes:126` — insufficient: caption naming one distributor above 10% of receivables; prior caption not in input, so a change in the number of concentrated customers can't be ruled out
- `0001193125-26-380207:notes:127` — receivables concentration table; amounts only
- `0001193125-26-380207:notes:128` — note title merged with sub-heading; formatting
- `0001193125-26-380207:notes:130` — other purchase obligations; the note change history shows only the date changed
- `0001193125-26-380207:notes:132` — heading
- `0001193125-26-380207:notes:133` — standing loss-contingency policy; not listed as changed in the note change history
- `0001193125-26-380207:notes:134` — standing patent-litigation description; not listed as changed in the note change history
- `0001193125-26-380207:notes:135` — legal outcome statement; date rolled forward

### MD&A (input_mdna.md)

- `0001193125-26-380207:mdna:2` — page number
- `0001193125-26-380207:mdna:5` — company description; no amount, policy or commitment
- `0001193125-26-380207:mdna:6` — product portfolio description
- `0001193125-26-380207:mdna:7` — strategy description
- `0001193125-26-380207:mdna:10` — Public Cloud segment description
- `0001193125-26-380207:mdna:11` — heading
- `0001193125-26-380207:mdna:12` — heading
- `0001193125-26-380207:mdna:14` — introductory sentence to the mitigation list
- `0001193125-26-380207:mdna:16` — generic supplier-management mitigation statement; no amount, commitment or estimate
- `0001193125-26-380207:mdna:17` — generic product-range mitigation statement; no amount, commitment or estimate
- `0001193125-26-380207:mdna:18` — generic monitoring statement
- `0001193125-26-380207:mdna:19` — heading
- `0001193125-26-380207:mdna:20` — repurchase and dividend amounts for the quarter; amounts only
- `0001193125-26-380207:mdna:21` — heading
- `0001193125-26-380207:mdna:22` — DataPelago in MD&A; covered by the notes:12 items
- `0001193125-26-380207:mdna:23` — heading
- `0001193125-26-380207:mdna:26` — fiscal calendar, same sentence as notes:4; itemized there
- `0001193125-26-380207:mdna:28` — percent-of-revenue table; amounts only
- `0001193125-26-380207:mdna:32` — net revenues table; amounts only
- `0001193125-26-380207:mdna:34` — page number
- `0001193125-26-380207:mdna:36` — product revenues table; amounts only
- `0001193125-26-380207:mdna:38` — insufficient: description of what product revenue includes; prior wording not in input
- `0001193125-26-380207:mdna:41` — services revenues table; amounts only
- `0001193125-26-380207:mdna:49` — heading
- `0001193125-26-380207:mdna:50` — storage category percentage table; amounts only
- `0001193125-26-380207:mdna:51` — rounding note
- `0001193125-26-380207:mdna:52` — all-flash mix explanation, first half of the sentence; price-increase cause itemized from mdna:39
- `0001193125-26-380207:mdna:53` — second half of the same sentence; covered by the mdna:39 item
- `0001193125-26-380207:mdna:54` — heading
- `0001193125-26-380207:mdna:55` — geographic percentage table; amounts only
- `0001193125-26-380207:mdna:56` — rounding note
- `0001193125-26-380207:mdna:61` — insufficient: description of what cost of services revenue includes; prior wording not in input
- `0001193125-26-380207:mdna:63` — cost of product revenues table; amounts only
- `0001193125-26-380207:mdna:65` — cost ratios and materials share; amounts only, no cause stated (cause itemized at mdna:66)
- `0001193125-26-380207:mdna:69` — "relatively flat" description of unallocated product cost; no cause or estimate
- `0001193125-26-380207:mdna:70` — page number
- `0001193125-26-380207:mdna:72` — cost of services revenues table; amounts only
- `0001193125-26-380207:mdna:74` — Hybrid Cloud services cost description and ratios; amounts only, no cause
- `0001193125-26-380207:mdna:77` — Public Cloud cost description and ratios; cause itemized from mdna:78
- `0001193125-26-380207:mdna:79` — heading
- `0001193125-26-380207:mdna:80` — "relatively flat" description of unallocated services cost; no cause
- `0001193125-26-380207:mdna:83` — operating expense ratio; recurring sentence, amounts updated, cause is the revenue increase already itemized
- `0001193125-26-380207:mdna:88` — sales and marketing table; amounts only
- `0001193125-26-380207:mdna:91` — sales and marketing explanation; covered by the mdna:85 item
- `0001193125-26-380207:mdna:93` — research and development table; amounts only
- `0001193125-26-380207:mdna:95` — research and development explanation; covered by the mdna:85 item
- `0001193125-26-380207:mdna:97` — general and administrative table; amounts only
- `0001193125-26-380207:mdna:99` — general and administrative explanation; covered by the mdna:85 item
- `0001193125-26-380207:mdna:101` — restructuring table; amounts only
- `0001193125-26-380207:mdna:103` — restructuring plan, same content as notes:91; itemized there
- `0001193125-26-380207:mdna:104` — heading
- `0001193125-26-380207:mdna:105` — caption
- `0001193125-26-380207:mdna:106` — other expense table; amounts only
- `0001193125-26-380207:mdna:109` — Other, net attributed to foreign exchange swings; no direction or amount in the prose
- `0001193125-26-380207:mdna:111` — tax table; amounts only
- `0001193125-26-380207:mdna:112` — legend
- `0001193125-26-380207:mdna:113` — same sentence as notes:98; itemized there
- `0001193125-26-380207:mdna:115` — liquidity summary table; amounts only
- `0001193125-26-380207:mdna:117` — cash flow summary table; amounts only
- `0001193125-26-380207:mdna:121` — operating cash flow components; amounts only
- `0001193125-26-380207:mdna:122` — caption
- `0001193125-26-380207:mdna:127` — investing activities; amounts only (DataPelago itemized)
- `0001193125-26-380207:mdna:129` — financing activities; amounts only
- `0001193125-26-380207:mdna:130` — insufficient: cash flow factors and financing statement carried as text; prior wording not in input, so the changed words can't be identified (its refinancing sentence is cited in the June 2027 notes item)
- `0001193125-26-380207:mdna:132` — liquidity sources; date rolled forward
- `0001193125-26-380207:mdna:134` — cash and investments table; amounts only
- `0001193125-26-380207:mdna:135` — cash held by foreign subsidiaries; amounts and dates rolled
- `0001193125-26-380207:mdna:137` — generic statement of liquidity uses; no amount or commitment
- `0001193125-26-380207:mdna:138` — investment policy; date rolled forward
- `0001193125-26-380207:mdna:141` — caption; date rolled
- `0001193125-26-380207:mdna:142` — Senior Notes table; amounts only
- `0001193125-26-380207:mdna:143` — standing reference to Note 7
- `0001193125-26-380207:mdna:144` — heading
- `0001193125-26-380207:mdna:145` — credit facility; date rolled forward
- `0001193125-26-380207:mdna:146` — commercial paper program; date rolled forward
- `0001193125-26-380207:mdna:147` — heading
- `0001193125-26-380207:mdna:148` — standing capital expenditure funding statement
- `0001193125-26-380207:mdna:150` — recurring quarterly dividend declaration; dates rolled forward
- `0001193125-26-380207:mdna:151` — repurchase program; the new authorization is itemized from notes:79
- `0001193125-26-380207:mdna:153` — purchase commitments, same figures as notes:131; itemized there
- `0001193125-26-380207:mdna:154` — heading
- `0001193125-26-380207:mdna:155` — standing reference to Note 14
- `0001193125-26-380207:mdna:157` — no material change to critical accounting policies; reference rolled to the 2026 Form 10-K

### Item 4 (input_controls.md)

- `0001193125-26-380207:item_4_controls:1` — heading
- `0001193125-26-380207:item_4_controls:2` — heading
- `0001193125-26-380207:item_4_controls:3` — standing definition of disclosure controls
- `0001193125-26-380207:item_4_controls:4` — disclosure controls concluded effective; evaluation date rolled to July 31, 2026
- `0001193125-26-380207:item_4_controls:5` — heading
- `0001193125-26-380207:item_4_controls:6` — no change in internal control over financial reporting; quarter rolled forward
- `0001193125-26-380207:item_4_controls:7` — page number

### 8-K, Item 2.02 earnings release (input_8k.md)

- `0001002047-26-000003:8k_2_02:1` — exhibit header
- `0001002047-26-000003:8k_2_02:2` — exhibit header
- `0001002047-26-000003:8k_2_02:3` — exhibit header
- `0001002047-26-000003:8k_2_02:4` — release title
- `0001002047-26-000003:8k_2_02:6` — headline EPS amounts; cited in the guidance-beat item
- `0001002047-26-000003:8k_2_02:8` — heading
- `0001002047-26-000003:8k_2_02:9` — headline all-flash amount; cause itemized from mdna:39
- `0001002047-26-000003:8k_2_02:10` — headline Public Cloud amount; cause itemized from mdna:48
- `0001002047-26-000003:8k_2_02:12` — headline operating margin amounts
- `0001002047-26-000003:8k_2_02:13` — DataPelago headline; itemized from notes:12
- `0001002047-26-000003:8k_2_02:14` — dateline and quarter-end date
- `0001002047-26-000003:8k_2_02:16` — heading
- `0001002047-26-000003:8k_2_02:17` — units caption
- `0001002047-26-000003:8k_2_02:18` — GAAP results table; amounts only
- `0001002047-26-000003:8k_2_02:19` — non-GAAP results table; amounts only
- `0001002047-26-000003:8k_2_02:20` — heading
- `0001002047-26-000003:8k_2_02:22` — heading
- `0001002047-26-000003:8k_2_02:23` — full-year guidance table; included in the raised-guidance item
- `0001002047-26-000003:8k_2_02:24` — heading
- `0001002047-26-000003:8k_2_02:25` — recurring dividend payment notice; dates rolled forward
- `0001002047-26-000003:8k_2_02:26` — heading
- `0001002047-26-000003:8k_2_02:27` — heading
- `0001002047-26-000003:8k_2_02:28` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:29` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:30` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:31` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:32` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:33` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:34` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:35` — product announcement; no financial term
- `0001002047-26-000003:8k_2_02:36` — heading
- `0001002047-26-000003:8k_2_02:37` — partner announcement; no financial term
- `0001002047-26-000003:8k_2_02:38` — partner announcement; no financial term
- `0001002047-26-000003:8k_2_02:39` — partner announcement; no financial term
- `0001002047-26-000003:8k_2_02:40` — partner proof of concept; no financial term
- `0001002047-26-000003:8k_2_02:41` — partner agreement; no financial term
- `0001002047-26-000003:8k_2_02:42` — partner announcement; no financial term
- `0001002047-26-000003:8k_2_02:43` — heading
- `0001002047-26-000003:8k_2_02:44` — DataPelago announcement; itemized from notes:12
- `0001002047-26-000003:8k_2_02:45` — heading
- `0001002047-26-000003:8k_2_02:47` — heading
- `0001002047-26-000003:8k_2_02:48` — award; no financial substance
- `0001002047-26-000003:8k_2_02:49` — award; no financial substance
- `0001002047-26-000003:8k_2_02:50` — analyst recognition; no financial substance
- `0001002047-26-000003:8k_2_02:51` — ranking; no financial substance
- `0001002047-26-000003:8k_2_02:52` — workplace ranking; no financial substance
- `0001002047-26-000003:8k_2_02:53` — ranking; no financial substance
- `0001002047-26-000003:8k_2_02:54` — workplace ranking; no financial substance
- `0001002047-26-000003:8k_2_02:55` — heading
- `0001002047-26-000003:8k_2_02:56` — conference call logistics
- `0001002047-26-000003:8k_2_02:57` — insufficient: safe-harbor list of risk factors (it names tariffs, government shutdowns and component costs); the prior release and the Item 1A diff aren't in the input, so new risks can't be identified
- `0001002047-26-000003:8k_2_02:58` — heading
- `0001002047-26-000003:8k_2_02:59` — standing list of non-GAAP measures
- `0001002047-26-000003:8k_2_02:60` — standing non-GAAP rationale
- `0001002047-26-000003:8k_2_02:61` — standing non-GAAP definitions
- `0001002047-26-000003:8k_2_02:62` — standing free cash flow definition
- `0001002047-26-000003:8k_2_02:63` — standing billings definition; cited in the billings item
- `0001002047-26-000003:8k_2_02:64` — introductory sentence
- `0001002047-26-000003:8k_2_02:65` — standing exclusion A, amortization
- `0001002047-26-000003:8k_2_02:66` — standing exclusion B, stock-based compensation
- `0001002047-26-000003:8k_2_02:67` — standing exclusion C, litigation settlements
- `0001002047-26-000003:8k_2_02:68` — standing exclusion D, acquisition-related expenses
- `0001002047-26-000003:8k_2_02:69` — standing exclusion E, restructuring
- `0001002047-26-000003:8k_2_02:70` — standing exclusion F, impairments
- `0001002047-26-000003:8k_2_02:71` — standing exclusion G, gains and losses on asset sales or derecognition
- `0001002047-26-000003:8k_2_02:72` — standing exclusion H, equity security sales
- `0001002047-26-000003:8k_2_02:73` — standing exclusion I, debt extinguishment
- `0001002047-26-000003:8k_2_02:74` — standing exclusion J, income tax effects
- `0001002047-26-000003:8k_2_02:75` — standing non-GAAP caveat
- `0001002047-26-000003:8k_2_02:76` — heading
- `0001002047-26-000003:8k_2_02:77` — standing constant currency policy
- `0001002047-26-000003:8k_2_02:78` — heading
- `0001002047-26-000003:8k_2_02:79` — company boilerplate
- `0001002047-26-000003:8k_2_02:80` — company boilerplate
- `0001002047-26-000003:8k_2_02:81` — company boilerplate
- `0001002047-26-000003:8k_2_02:82` — company boilerplate
- `0001002047-26-000003:8k_2_02:83` — website reference
- `0001002047-26-000003:8k_2_02:84` — trademark notice
- `0001002047-26-000003:8k_2_02:85` — statement header
- `0001002047-26-000003:8k_2_02:86` — statement header
- `0001002047-26-000003:8k_2_02:87` — units caption
- `0001002047-26-000003:8k_2_02:88` — unaudited caption
- `0001002047-26-000003:8k_2_02:89` — balance sheet; amounts only
- `0001002047-26-000003:8k_2_02:90` — statement header
- `0001002047-26-000003:8k_2_02:91` — statement header
- `0001002047-26-000003:8k_2_02:92` — units caption
- `0001002047-26-000003:8k_2_02:93` — unaudited caption
- `0001002047-26-000003:8k_2_02:94` — statement of operations; amounts only
- `0001002047-26-000003:8k_2_02:95` — statement header
- `0001002047-26-000003:8k_2_02:96` — statement header
- `0001002047-26-000003:8k_2_02:97` — units caption
- `0001002047-26-000003:8k_2_02:98` — unaudited caption
- `0001002047-26-000003:8k_2_02:99` — statement of cash flows; amounts only
- `0001002047-26-000003:8k_2_02:100` — GAAP to non-GAAP reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:101` — GAAP to non-GAAP reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:102` — GAAP to non-GAAP reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:103` — gross margin reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:104` — product gross margin reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:105` — services gross margin reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:106` — operating margin reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:107` — effective tax rate reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:108` — free cash flow reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:109` — billings reconciliation; amounts only, cited in the billings item
- `0001002047-26-000003:8k_2_02:110` — supplemental segment data; amounts only
- `0001002047-26-000003:8k_2_02:111` — supplemental geographic data; amounts only
- `0001002047-26-000003:8k_2_02:112` — supplemental non-GAAP data; amounts only
- `0001002047-26-000003:8k_2_02:113` — company-reported deferred revenue, DSO, DPO and inventory turns; amounts only, left to the numbers reader
- `0001002047-26-000003:8k_2_02:114` — company-reported cash flow items and free cash flow margin; amounts only
- `0001002047-26-000003:8k_2_02:115` — second-quarter margin guidance reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:117` — full-year margin guidance reconciliation; amounts only (its restructuring line is cited in the second-quarter guidance item)
- `0001002047-26-000003:8k_2_02:118` — full-year EPS guidance reconciliation; amounts only
- `0001002047-26-000003:8k_2_02:119` — contacts
- `0001002047-26-000003:8k_2_02:120` — contacts
- `0001002047-26-000003:8k_2_02:121` — contacts
- `0001002047-26-000003:8k_2_02:122` — contacts
- `0001002047-26-000003:8k_2_02:123` — contacts
- `0001002047-26-000003:8k_2_02:124` — contacts
- `0001002047-26-000003:8k_2_02:125` — contacts
- `0001002047-26-000003:8k_2_02:126` — contacts
- `0001002047-26-000003:8k_2_02:127` — contacts

The 8-K item-code list and the late-filing section aren't paragraphs. Neither shows a late-filing notice on or before 2026-09-02.

### Prior-period text removed, from the note change history (for completeness)

- `0001193125-26-076622:note_history:1` — old sub-heading, now merged with the note title; formatting
- `0001193125-26-076622:note_history:6` — note title moved; formatting
- `0001193125-26-076622:note_history:7` — "Financing Guarantees" heading, removed with its section (itemized at :8, :10, :11)
- `0001193125-26-076622:note_history:9` — sales through leasing companies without recourse, removed with the section; covered by the recourse lease item
- `0001193125-26-076622:note_history:16` — old business description; wording only
- `0001193125-26-076622:note_history:22` — sentence on the June 2025 note repayment dropped; that repayment is in the prior-year comparative quarter and still described at mdna:129; roll-forward
- `0001193125-26-076622:note_history:24` — maturity table; covered by the maturity schedule item
- `0001193125-26-076622:note_history:25` — old heading order; reordered
- `0001193125-26-076622:note_history:27` — duplicate of :23 under the maturities tag; covered by the maturity schedule item
- `0001193125-26-076622:note_history:28` — duplicate of :24; covered by the maturity schedule item
- The other 076622 history entries (:2, :3, :5, :13, :14, :15, :17, :18, :20, :21, :26) are earlier versions of current paragraphs, accounted for above.

## Insufficient

10 paragraphs were marked insufficient:

- notes:8
- notes:9
- notes:34
- notes:87
- notes:102
- notes:126
- mdna:38
- mdna:61
- mdna:130
- 8k_2_02:57

In each case the paragraph is carried as text, but its prior wording isn't in the input and the paragraph is the kind where a change would matter.

Separately, the Item 1A diff, Exhibit 21 diff, Exhibit 10 and auditor's report are absent from the input. They weren't read because they aren't there.

## Summary

- 47 items, 3 flagged `explanation: true`:
  - receivables, mdna:123
  - inventories, mdna:124
  - restructuring reserve, notes:91
- 10 paragraphs marked insufficient.
