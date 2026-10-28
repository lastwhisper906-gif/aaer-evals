# Notes text reader — Palo Alto Networks quarterly report for the quarter ended April 30, 2026 (accession 0001327567-26-000015)

## What this report read

All six input files were read in full: the notes after the diff layer, the note change history, MD&A, the controls section (Item 4), the 8-K index and my prior flags.

- **Forbidden material.** None found. There is no trend table, price series, abnormal return, short interest, other company's file, prior probability or outcome window. The share prices that appear (conversion price, capped call strike and cap prices, average repurchase price, grant-date fair values) are printed in the filing's own notes.
- **Auditor's report.** None in the input. This is a quarterly report and no review report was supplied.
- **Risk factor diff, subsidiaries exhibit diff, material contract exhibits.** None in the input.
- **8-K bodies.** None in the input. The 8-K file contradicts itself: its header says no 8-K is on record, yet it lists item codes for each filing, including filings within this quarter. Only item codes are available, so the two 8-K items below are marked `insufficient`.
- **Prior flags.** None on record, so nothing is carried forward.
- **No arithmetic.** Every amount below is copied from the prose or tables as printed. Where two figures sit side by side, they are reported side by side and not compared; reconciling them is the numbers reader's and the supervisor's job.
- **Unseen prior wording.** Where a paragraph is carried as changed but the prior wording is not in my input, the item says so.
- **The `insufficient` field.** I added it to each item. `insufficient: true` marks an item whose substance cannot be read from the input.

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_cyberark_results_consolidated_from_february",
    "what_changed": "The business description note now states that CyberArk Software Ltd., an identity security company, was acquired on February 11, 2026, and that its results are included in the condensed consolidated statements prospectively from that date. In the prior quarterly report CyberArk appeared only as a subsequent event.",
    "account": "total revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The condensed consolidated financial statements include the financial results of CyberArk prospectively from the date of acquisition.",
    "paragraph_id": "0001327567-26-000015:notes:3",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_identity_security_platform_section_added",
    "what_changed": "MD&A adds an Identity Security section describing Idira, a platform for human, agentic and machine identities. It lists five offerings: workforce identity security, IT and developer identity security (privileged access management), machine identity security, identity governance and administration, and AI agents security. The notes' business description and the MD&A mission statement now add identities to what the company secures.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "our next-generation identity security platform, is designed to secure human, agentic and machine identities across the enterprise",
    "paragraph_id": "0001327567-26-000015:mdna:29",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_cyberark_on_premise_licenses_in_product_revenue",
    "what_changed": "MD&A now says that, following the February 2026 CyberArk acquisition, product revenue also includes on-premise software licenses of certain identity security offerings. The revenue discussion states that product revenue is recognized at the time of hardware shipment or delivery of the software license, and now lists identity security offerings among product software licenses. It also says the product revenue increase for the three and nine months was driven in part by software license revenue from CyberArk.",
    "account": "product revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "our product revenue also includes on-premise software licenses of certain identity security offerings",
    "paragraph_id": "0001327567-26-000015:mdna:39",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "revenue_recognition_cyberark_identity_subscriptions_in_subscription_revenue",
    "what_changed": "MD&A's description of subscriptions now includes the CyberArk next-generation identity security platform. The explanation of the increase in subscription and support revenue now cites recent acquisitions alongside end-customer demand.",
    "account": "subscription and support revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "With the acquisition of CyberArk, our subscriptions include a next-generation identity security platform",
    "paragraph_id": "0001327567-26-000015:mdna:40",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_revenue_growth_attributed_partly_to_acquisitions",
    "what_changed": "The overview states total revenue of $3.0 billion for the third quarter of fiscal 2026 and $2.3 billion for the third quarter of fiscal 2025, as year-over-year growth of 31%. It now attributes the growth to adoption of the portfolio and to recent acquisitions.",
    "account": "total revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our growth reflects the increased adoption of our portfolio, which consists of product, subscriptions, and support, and our recent acquisitions.",
    "paragraph_id": "0001327567-26-000015:mdna:37",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_acquired_chronosphere_and_cyberark_operating_loss",
    "what_changed": "New sentence. Since their acquisition dates, Chronosphere and CyberArk together contributed revenue of $388 million for the three months and $391 million for the nine months ended April 30, 2026. Over the same periods they contributed operating losses of $523 million and $524 million.",
    "account": "operating income (loss)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the combined net impact of the Chronosphere and CyberArk acquisitions on our condensed consolidated statements of operations was revenue of $388 million and $391 million and operating loss of $523 million and $524 million",
    "paragraph_id": "0001327567-26-000015:notes:93",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_pro_forma_pairs_cyberark_calendar_quarters",
    "what_changed": "The pro forma note now covers CyberArk as well as Chronosphere. It combines the results of Palo Alto Networks and Chronosphere for periods ended April 30 with CyberArk's results for the three and nine months ended March 31, 2026 and 2025. Its adjustments cover amortization of acquired intangibles, stock compensation from replacement awards, transaction costs, severance under the workforce optimization plan, and income tax.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "with the historical results of CyberArk for the three and nine months ended March 31, 2026 and 2025, respectively",
    "paragraph_id": "0001327567-26-000015:notes:96",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_acquisition_impact_disclosed_at_discretion",
    "what_changed": "A new Impact of Acquisitions section in MD&A says that comparability of the three- and nine-month results with the same periods of 2025 is affected by recent acquisitions, including CyberArk. It says the company 'may' disclose the impact of an acquisition, qualitatively or quantitatively, for one year after the acquisition date, where it judges such discussion meaningful. The revenue overview now also names business acquisitions as a cause of quarter-to-quarter variation in revenue.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "we may qualitatively or quantitatively disclose the impact of our acquisitions on revenue, costs, and expenses for the one year period subsequent to the acquisition date where such discussions would be meaningful",
    "paragraph_id": "0001327567-26-000015:mdna:66",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_cyberark_purchase_consideration_and_allocation",
    "what_changed": "The acquisitions note sets out the CyberArk terms: $45.00 in cash and 2.2005 Palo Alto Networks shares per CyberArk share. Total purchase consideration is $21.1 billion: cash of $2,308 million, 112 million shares valued at $18,488 million, and $265 million of replacement awards. The allocation table records goodwill of $14,802 million, identified intangible assets of $6,279 million, assumed convertible senior notes of $(1,303) million and deferred revenue of $(776) million. MD&A repeats the consideration in its new Impact of Acquisitions section.",
    "account": "goodwill",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "CyberArk shareholders received $45.00 in cash and 2.2005 shares of our common stock for each CyberArk share.",
    "paragraph_id": "0001327567-26-000015:notes:74",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_cyberark_goodwill_deductible_for_united_states_tax",
    "what_changed": "New statement that substantially all of the goodwill from the CyberArk acquisition is deductible for U.S. income tax purposes. The Chronosphere goodwill, in the same note, is stated as not deductible.",
    "account": "income taxes payable",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Substantially all of goodwill is deductible for U.S. income tax purposes.",
    "paragraph_id": "0001327567-26-000015:notes:78",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_koi_goodwill_deductible_for_united_states_tax",
    "what_changed": "New statement that the goodwill from the Koi acquisition, closed April 14, 2026, is deductible for U.S. income tax purposes.",
    "account": "income taxes payable",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The goodwill is deductible for U.S. income tax purposes.",
    "paragraph_id": "0001327567-26-000015:notes:88",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_cyberark_platform_renewals_long_useful_life",
    "what_changed": "New useful-life estimates for the CyberArk intangibles: platform renewals of $3,500 million over 12 to 14 years, developed technology of $2,537 million over 5 to 7 years, customer contracts of $219 million over 2 years, and trade name of $23 million over 1 year. The intangible asset table now has a line titled customer relationships and platform renewals, plus new lines for customer contracts and for trade name and trademarks.",
    "account": "amortization of intangible assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "12 years - 14 years",
    "paragraph_id": "0001327567-26-000015:notes:79",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_acquisition_allocations_open_in_measurement_period",
    "what_changed": "The measurement-period statement is carried as changed and applies to the acquisitions in this note, now including CyberArk (closed February 11, 2026) and Koi (closed April 14, 2026). Information about income tax and other contingencies that existed at acquisition may change the recorded amounts and allocations for up to 12 months after each acquisition date.",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "may become known during the remainder of the measurement period, not to exceed 12 months from the acquisition date, which may result in changes to the amounts and allocations recorded",
    "paragraph_id": "0001327567-26-000015:notes:97",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_cyberark_replacement_awards_expensed_over_service",
    "what_changed": "New: the company issued $945 million of CyberArk replacement equity awards. The portion for service before the acquisition went to purchase consideration ($265 million, as stated in MD&A and the consideration table). The remaining fair value will be expensed as share-based compensation over the remaining service periods. The equity note adds that 7 million RSUs were assumed across the Chronosphere, CyberArk and Koi acquisitions.",
    "account": "share-based compensation",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The remaining fair value was allocated to future services and will be expensed over the remaining service periods as share-based compensation.",
    "paragraph_id": "0001327567-26-000015:notes:76",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_koi_replacement_awards_expensed_over_service",
    "what_changed": "New: Koi replacement equity awards of $61 million, including 0.3 million shares of restricted common stock vesting over three years, are allocated entirely to future services. They will be expensed as share-based compensation.",
    "account": "share-based compensation",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we issued $61 million of replacement equity awards, which was allocated to future services and will be expensed over the remaining service periods as share-based compensation",
    "paragraph_id": "0001327567-26-000015:notes:86",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "articulation_and_the_filed_history_koi_consideration_against_prior_subsequent_event",
    "what_changed": "The prior quarterly report's subsequent-events note described the Koi agreement as total consideration of $300 million in cash and replacement awards. It said closing was expected in the second half of fiscal 2026, subject to regulatory clearance, and that the purpose was to expand the security operations platform. This note now says Koi closed on April 14, 2026, for total purchase consideration of $231 million, substantially all cash. Separately, $61 million of replacement equity awards are allocated to future services. Enhancing Prisma AIRS is added to the stated purpose. Whether the two descriptions reconcile is for the supervisor.",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The total purchase consideration for the acquisition of Koi was $231 million, substantially all of which is comprised of cash.",
    "paragraph_id": "0001327567-26-000015:notes:85",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_portkey_agreement_signed_on_last_day_of_quarter",
    "what_changed": "New: on April 30, 2026, the last day of the quarter, the company signed a definitive agreement to acquire Portkey, Inc., a privately-held AI Gateway company. Total consideration is $140 million in cash and replacement awards, subject to adjustments, and the stated purpose is to enhance Prisma AIRS.",
    "account": "cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "in exchange for total consideration of $140 million in cash and replacement awards, subject to adjustments",
    "paragraph_id": "0001327567-26-000015:notes:91",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_portkey_closed_after_quarter_end",
    "what_changed": "The subsequent events note now reports that the Portkey acquisition was completed on May 29, 2026 and will be accounted for as a business combination in the fourth quarter of fiscal 2026. The prior quarter's subsequent events (the CyberArk closing and the Koi agreement) have been removed from this note and now appear in the acquisitions note. MD&A also states the May 29, 2026 completion.",
    "account": "goodwill",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "This acquisition will be accounted for as a business combination in the fourth quarter of fiscal 2026.",
    "paragraph_id": "0001327567-26-000015:notes:189",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_trust_security_and_prisma_airs_launches",
    "what_changed": "MD&A's innovation paragraph now names two product launches: Next-Generation Trust Security, which unifies certificate lifecycle management, and Prisma AIRS 3.0, which protects agentic AI. It also dates the completed acquisitions of CyberArk (February 11, 2026), Koi (April 14, 2026) and Portkey (May 29, 2026).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "we launched Next-Generation Trust Security that unifies certificate lifecycle management and Prisma AIRS 3.0 that discovers, assesses, and protects agentic AI",
    "paragraph_id": "0001327567-26-000015:mdna:41",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_frontier_ai_defense_services_launched",
    "what_changed": "New dated sentence: in April 2026 Unit 42 launched a suite of Frontier AI Defense services to help customers discover and neutralize threats introduced by next-generation AI models.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In April 2026, we launched a new suite of Unit 42 Frontier AI Defense services",
    "paragraph_id": "0001327567-26-000015:mdna:36",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_intangible_amortization_now_in_cost_of_product_revenue",
    "what_changed": "The description of cost of product revenue now lists amortization of intangible assets as a component. The amortization note shows a cost of product revenue line of $37 million for the three and nine months ended April 30, 2026, and a dash for the prior-year periods. MD&A ties the higher amortization to the CyberArk acquisition.",
    "account": "cost of product revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "shipping and tariff costs, amortization of intangible assets, product testing costs",
    "paragraph_id": "0001327567-26-000015:mdna:84",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_tariff_costs_and_lower_inventory_charges",
    "what_changed": "MD&A's explanation of the increase in cost of product revenue for both periods now names three drivers: higher amortization of intangibles from CyberArk, higher demand for hardware products, and higher tariff costs. These are partly offset by a decrease in inventory excess and obsolete charges.",
    "account": "cost of product revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "increased demand for our hardware products and higher tariff costs, partially offset by a decrease in inventory excess and obsolete charges",
    "paragraph_id": "0001327567-26-000015:mdna:86",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_hardware_gross_margin_decrease",
    "what_changed": "Product gross margin decreased for the three and nine months. Management attributes this to a decrease in gross margin on hardware products and to higher intangible amortization, partly offset by CyberArk software license revenue. For the nine months it was further offset by a shift in product revenue mix toward software and a decrease in inventory excess and obsolete charges.",
    "account": "product gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to a decrease in gross margin on our hardware products and higher amortization of intangible assets",
    "paragraph_id": "0001327567-26-000015:mdna:95",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_and_storage_component_shortages",
    "what_changed": "The economic-conditions paragraph, carried as changed, now names supply chain disruptions, including increased memory, storage or other component shortages, as conditions that may adversely affect results, alongside tariffs and trade policy. The prior wording is not in this input, so which phrase is new cannot be confirmed.",
    "account": "cost of product revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "supply chain disruptions, including increased memory, storage or other component shortages",
    "paragraph_id": "0001327567-26-000015:mdna:44",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_israel_and_iran_hostilities",
    "what_changed": "The geopolitical paragraph now refers to hostilities in Israel, Iran and the surrounding region. It states that the company has business operations in Israel and intends to continue growing its presence there, and that it currently does not expect significant disruption. Separately, MD&A describes the new Israeli R&D Law tax credit.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "While we have business operations in Israel, and intend to continue growing our presence in Israel, we currently do not expect significant business disruption.",
    "paragraph_id": "0001327567-26-000015:mdna:45",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_quarterly_operating_loss_language",
    "what_changed": "The key financial metrics text now refers to operating income (loss). The metrics table shows an operating loss of $(183) million and an operating margin of (6.1)% for the three months ended April 30, 2026. The results table shows a net loss of $(177) million for the same three months.",
    "account": "operating income (loss)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "We discuss revenue, gross margin, and the components of operating income (loss) and margin below",
    "paragraph_id": "0001327567-26-000015:mdna:49",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_subscription_cost_hosting_amortization_and_personnel",
    "what_changed": "The explanation of cost of subscription and support revenue now states three increases, each for the three and nine months. Cloud hosting costs increased $75 million and $171 million. Amortization of intangible assets increased $117 million and $109 million as a result of recent acquisitions. Personnel costs grew $71 million and $97 million, including acquired headcount. Checking these stated increases against the amortization and results tables is left to the numbers reader.",
    "account": "cost of subscription and support revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Amortization of intangible assets increased $117 million and $109 million for the three and nine months ended April 30, 2026, respectively, compared to the same periods in 2025 as a result of our recent acquisitions.",
    "paragraph_id": "0001327567-26-000015:mdna:91",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_subscription_gross_margin_down_on_acquired_amortization",
    "what_changed": "New explanation: subscription and support gross margin decreased for both periods, primarily because of higher amortization of intangible assets from recent acquisitions.",
    "account": "subscription and support gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to higher amortization of intangible assets as a result of our recent acquisitions",
    "paragraph_id": "0001327567-26-000015:mdna:96",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_research_and_development_personnel_growth_with_acquired_headcount",
    "what_changed": "The research and development explanation now states personnel cost growth of $192 million for the three months and $233 million for the nine months. It attributes this largely to headcount growth, including headcount from recent acquisitions.",
    "account": "research and development",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "which grew $192 million and $233 million for the three and nine months ended April 30, 2026 compared to the same periods in 2025, largely due to headcount growth, including headcount from our recent acquisitions",
    "paragraph_id": "0001327567-26-000015:mdna:103",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_sales_and_marketing_personnel_and_acquired_amortization",
    "what_changed": "The sales and marketing explanation now states personnel cost growth of $254 million for the three months and $408 million for the nine months, including acquired headcount. It adds higher amortization of intangible assets from recent acquisitions as a further driver in both periods.",
    "account": "sales and marketing",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in sales and marketing expense in both periods were further driven by higher amortization of intangible assets as a result of our recent acquisitions.",
    "paragraph_id": "0001327567-26-000015:mdna:107",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_general_and_administrative_drivers_with_contingent_consideration_gain",
    "what_changed": "The general and administrative explanation now states personnel cost growth of $195 million for the three months and $237 million for the nine months. It attributes that growth to accelerated vesting of equity awards in connection with recent acquisitions, to CyberArk employee severance, and to headcount growth. It adds acquisition-related costs as a driver. As an offset it names a $110 million gain on the change in fair value of the contingent consideration liability in the three months. For the nine months it also cites the $40 million partial release of a litigation-related accrual in the nine months ended April 30, 2025.",
    "account": "general and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by a gain of $110 million for the change in fair value of contingent consideration liability during the three months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:112",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "results_against_expectations_general_and_administrative_outlook_excludes_acquisitions",
    "what_changed": "The general and administrative description now says this expense includes the change in fair value of the contingent consideration liability. It also qualifies the expectation that the expense will increase in absolute dollars over time: that expectation now excludes the near-term impact of recent acquisitions.",
    "account": "general and administrative",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Excluding the near-term impact of our recent acquisitions, we expect general and administrative expense to increase in absolute dollars over time",
    "paragraph_id": "0001327567-26-000015:mdna:110",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_accelerated_vesting_charge_on_cyberark_and_koi",
    "what_changed": "New: vesting of certain equity awards was accelerated in connection with the CyberArk and Koi acquisitions. This produced $177 million of share-based compensation in the three and nine months: $1 million in cost of subscription and support revenue, $36 million in sales and marketing, and $140 million in general and administrative.",
    "account": "share-based compensation",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the vesting of certain equity awards was accelerated in connection with our acquisitions of CyberArk and Koi; as a result, we recorded share-based compensation of $177 million",
    "paragraph_id": "0001327567-26-000015:notes:176",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_cyberark_transaction_costs_in_general_and_administrative",
    "what_changed": "New: CyberArk transaction costs were $41 million for the three months and $56 million for the nine months ended April 30, 2026, primarily in general and administrative expense.",
    "account": "general and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "transaction costs related to CyberArk acquisition were $41 million and $56 million, respectively, which were primarily included in general and administrative expense",
    "paragraph_id": "0001327567-26-000015:notes:80",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_cyberark_workforce_optimization_plan_and_severance_liability",
    "what_changed": "New: an integration plan to optimize the combined workforce, with a total estimated cost of $59 million, expected to be substantially completed by the end of fiscal 2027. Severance is recognized on notification, or ratably where service beyond the minimum retention period is required. Cash payments in the quarter were $12 million, and a $12 million severance liability sat in accrued compensation at April 30, 2026. The charge table shows $41 million of severance charges for the three and nine months, including $17 million of share-based compensation, spread across cost of subscription and support revenue, research and development, sales and marketing, and general and administrative.",
    "account": "accrued compensation",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "for a total estimated cost of $59 million",
    "paragraph_id": "0001327567-26-000015:notes:81",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_qradar_contingent_consideration_estimate_reduced",
    "what_changed": "New sentence: in the quarter the company reduced its estimate of future cash payments to IBM under the QRadar contingent consideration. It cites the magnitude and likelihood of customers entering into qualified new transactions, the competitive industry environment, and current market conditions. The note states an undiscounted range of $0.3 billion to $0.5 billion, with payments through the fiscal quarter ending October 2028. The rollforward shows a change in fair value of $(110) million for the quarter and an ending liability of $240 million. MD&A records the change as a gain within general and administrative expense.",
    "account": "contingent consideration liability",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the three months ended April 30, 2026, we reduced our estimate of future cash payments based on our quarterly assessment of assumptions",
    "paragraph_id": "0001327567-26-000015:notes:40",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_centripetal_accrual_and_interest",
    "what_changed": "The Centripetal accrual is stated as $150 million at April 30, 2026 and $146 million at July 31, 2025, in other long-term liabilities. Interest charges were $1 million for the three months and $4 million for the nine months. The prior-year comparison is now framed as a $2 million charge for the three months and a $40 million release for the nine months ended April 30, 2025. The prior filing gave a $1 million charge and a $42 million release for the three and six months ended January 31, 2025.",
    "account": "other long-term liabilities",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "we accrued $150 million and $146 million based on the judgment and estimated interest, which is recorded in other long-term liabilities",
    "paragraph_id": "0001327567-26-000015:notes:150",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_centripetal_european_proceedings",
    "what_changed": "The Centripetal paragraph is carried as changed. It states the October 3, 2024 judgment on three patents, with damages reduced to $114 million, and the surety bond that prevents execution while appeals are pending. It also states that infringement contentions before the European Patent Office and the Unified Patent Court in Germany are still pending. No accrual or estimate is given for the European matters. Which sentence changed cannot be isolated from this input.",
    "account": "other long-term liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Centripetal filed infringement contentions on certain of their patents in the European Patent Office and Unified Patent Court in Germany, to which we filed appropriate legal challenges. Those matters are still pending.",
    "paragraph_id": "0001327567-26-000015:notes:149",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_assumed_cyberark_convertible_notes",
    "what_changed": "New debt. Through a February 2026 supplemental indenture the company took on CyberArk's $1.25 billion of 0.0% Convertible Senior Notes due June 15, 2030. They are now exchangeable for about 4.3161 Palo Alto Networks shares plus $88.2630 in cash per $1,000 of principal: initially 5.4 million shares and $110 million in cash, at a conversion price of about $211.24. The notes carry no financial covenants. The company may redeem them from June 20, 2028 if the stock is at least $280.75 for the stated period. Holders may convert early under a $280.75 sale price condition, a trading price condition, or specified corporate events.",
    "account": "convertible senior notes",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These modifications result in the 2030 Notes being exchangeable initially for 5.4 million shares of our common stock with an effective initial conversion price of approximately $211.24 per share of common stock, subject to adjustments, and an initial cash amount of $110 million.",
    "paragraph_id": "0001327567-26-000015:notes:119",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_make_whole_conversions_settled_in_cash_by_election",
    "what_changed": "New: the acquisition was both a make-whole fundamental change and a fundamental change under the indenture. Holders surrendered $153 million of principal for conversion at the increased make-whole rate, and the company elected to settle those conversions in cash. No holder exercised the repurchase right, and both rights expired on March 20, 2026.",
    "account": "cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "We elected cash settlement as the settlement method for any 2030 Notes surrendered during the make-whole fundamental change period",
    "paragraph_id": "0001327567-26-000015:notes:127",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_surrendered_notes_valued_on_prices_after_quarter_end",
    "what_changed": "New: the surrendered notes are a current liability at April 30, 2026, measured at $160 million. The measure is the sum of daily conversion values over 30 trading days from March 24, 2026 to May 5, 2026, a window that runs past the balance sheet date. The notes were settled in cash for $160 million on May 7, 2026.",
    "account": "short-term convertible senior notes",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The related fair value of $160 million was estimated based on the sum of the daily conversion values computed from our stock price during the 30 consecutive trading days between March 24, 2026 and May 5, 2026.",
    "paragraph_id": "0001327567-26-000015:notes:128",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_remaining_convertible_notes_classified_long_term",
    "what_changed": "New: the remaining $1.1 billion of principal is classified as long-term because the sale price condition was not met in the calendar quarter ended March 31, 2026. Its fair value of $1.2 billion is taken from the closing trading price and moves with the stock price and market interest rates. The classification depends on the sale price condition, which is tested each calendar quarter.",
    "account": "long-term convertible senior notes",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "the remaining 2030 Notes with an aggregate principal amount of $1.1 billion were classified as a long-term liability on our condensed consolidated balance sheets since the sale price condition was not met during the calendar quarter ended March 31, 2026",
    "paragraph_id": "0001327567-26-000015:notes:129",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_convertible_notes_conversion_window_and_sufficiency",
    "what_changed": "New MD&A paragraph. It says the notes are not convertible under the sale price condition in the calendar quarter ending June 30, 2026. If the condition is met in that quarter and all holders convert in the calendar quarter ending September 30, 2026, the company would settle the $1.1 billion of principal, and part of any excess over principal, in cash. It then states that liquidity will be sufficient if holders convert during the fiscal quarter ending July 31, 2026 or hold to maturity, and names possible proceeds from settling or terminating the assumed capped calls as a source. The paragraph names two differently defined conversion windows.",
    "account": "cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "should the holders choose to convert their 2030 Notes during the fiscal quarter ending July 31, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:133",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_convertible_notes_fair_value_loss_in_other_income",
    "what_changed": "New: for the three and nine months, the fair value change on the 2030 Notes was a $37 million loss in earnings (other income, net) and a $12 million loss in accumulated other comprehensive income (AOCI) for instrument-specific credit risk. MD&A names this loss as one reason other income, net decreased in the quarter.",
    "account": "other income, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "changes in fair value of 2030 Notes included in earnings were a loss of $37 million, and changes in fair value attributable to instrument-specific credit risk included in AOCI were a loss of $12 million",
    "paragraph_id": "0001327567-26-000015:notes:130",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_fair_value_option_elected_for_acquired_convertible_notes",
    "what_changed": "New accounting policy. The company elected the fair value option for the convertible notes acquired from CyberArk, measured at fair value through maturity or settlement. Changes go to earnings in other income, net, except the instrument-specific credit-risk part, which goes to AOCI. Capped calls are derivative assets at fair value, with changes in other income, net. The significant accounting policies paragraph now names this CyberArk-driven exception. MD&A's description of other income now includes these fair value changes.",
    "account": "other income, net",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "we have elected fair value option to simplify the accounting for embedded features that would otherwise require bifurcation from the debt-host and recognition as a separate derivative liability",
    "paragraph_id": "0001327567-26-000015:notes:13",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_convertible_notes_and_capped_calls_added_to_estimates",
    "what_changed": "The list of management estimates now adds the fair value of convertible senior notes and capped calls. The prior list did not include it.",
    "account": "convertible senior notes",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "fair value of convertible senior notes and capped calls",
    "paragraph_id": "0001327567-26-000015:notes:8",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_capped_calls_partly_terminated_for_cash",
    "what_changed": "New: in April 2026 the company terminated portions of the assumed capped calls for $10 million in cash, in connection with the $153 million of notes surrendered during the make-whole period.",
    "account": "other assets",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In April 2026, we elected to terminate portions of the capped calls in exchange for $10 million in cash",
    "paragraph_id": "0001327567-26-000015:notes:133",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_capped_calls_valued_with_black_scholes",
    "what_changed": "New: the assumed capped calls have a strike of about $211.24 and caps of about $287.21 to $291.44, and can be settled in cash or shares at the company's election. They are carried at a fair value of $94 million at April 30, 2026, using a Black-Scholes model, with a $1 million loss in the three and nine months.",
    "account": "other assets",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "the fair value of the outstanding capped calls was $94 million, determined using the Black-Scholes option pricing model",
    "paragraph_id": "0001327567-26-000015:notes:134",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_convertible_notes_excluded_from_diluted_shares",
    "what_changed": "New sentence: the 2030 Notes and capped calls were excluded from diluted net income (loss) per share as antidilutive. The per-share note now reads net income (loss) throughout.",
    "account": "diluted weighted-average shares",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our 2030 Notes and capped calls were also excluded from the calculation of diluted net income (loss) per share as the effect would have been antidilutive.",
    "paragraph_id": "0001327567-26-000015:notes:185",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_foreign_earnings_repatriated_for_cyberark",
    "what_changed": "New: as part of the CyberArk acquisition, the company executed an intercompany transaction that repatriated $3.5 billion of foreign earnings, with immaterial state and other tax expense. Remaining unremitted earnings are stated as indefinitely reinvested. Total cash, cash equivalents and investments of $7.0 billion are stated as held for general corporate purposes.",
    "account": "cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As part of the acquisition of CyberArk, we executed an intercompany transaction to repatriate $3.5 billion of foreign earnings, resulting in immaterial income tax expense related to state and other taxes.",
    "paragraph_id": "0001327567-26-000015:mdna:130",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_lower_average_cash_lowers_interest_income",
    "what_changed": "New explanation: other income, net decreased in the quarter because of the fair value loss on the convertible notes and lower interest income, which MD&A attributes to lower average balances of cash, cash equivalents and investments.",
    "account": "interest income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "lower interest income as a result of lower average cash, cash equivalent and investment balances for the three months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:121",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_gains_on_investment_sales_to_fund_acquisitions",
    "what_changed": "New explanation: other income, net increased for the nine months mainly because of higher gains on sales of investments made to fund acquisitions, and higher interest income. These were partly offset by the loss on the convertible notes. The other income table carries an Other, net line of $76 million for the nine months ended April 30, 2026.",
    "account": "other income, net",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "increased gains on sales of our investments to fund acquisitions",
    "paragraph_id": "0001327567-26-000015:mdna:121",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_effective_tax_rate_fluctuation_from_cyberark_integration",
    "what_changed": "New: the effective tax rate differed from the statutory rate primarily because of the CyberArk acquisition and excess tax benefits from share-based compensation. The company may see continued fluctuations as it integrates CyberArk into its corporate structure and intercompany relationships.",
    "account": "provision for income taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We may continue to see fluctuations in our effective tax rate as we further integrate CyberArk into our corporate structure and intercompany relationships.",
    "paragraph_id": "0001327567-26-000015:mdna:123",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "earnings_quality_negative_quarterly_effective_tax_rate",
    "what_changed": "The income tax note states an effective tax rate of negative 13.5% for the three months and 26.8% for the nine months ended April 30, 2026. The rates for the prior-year periods are 15.6% and 12.3%. It attributes the rates to the CyberArk acquisition and to decreased excess tax benefits from share-based compensation. The note's opening sentence now names the CyberArk acquisition as a reason the rates differ from the statutory rate.",
    "account": "effective tax rate",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "our provision for income taxes reflected an effective tax rate of negative 13.5%",
    "paragraph_id": "0001327567-26-000015:notes:179",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_israel_research_and_development_tax_credit_law",
    "what_changed": "New: in March 2026 the Knesset Finance Committee approved the R&D Law. It gives a tax credit for qualifying research and development spending in Israel incurred after January 1, 2026, and pays all or part of any unused credit in cash after a stipulated period. Further implementing regulations are expected. The impact for the three and nine months is stated as not material.",
    "account": "provision for income taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "It provides that all or a portion of the unutilized R&D tax credit will be paid in cash upon the lapse of a period stipulated by the R&D Law.",
    "paragraph_id": "0001327567-26-000015:mdna:126",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_conclusion",
    "what_changed": "The note on the income tax disclosure standard, effective for annual periods beginning in fiscal 2026, now says adoption will result in disclosure of additional jurisdiction-level tax information. Before, it said the company was 'currently evaluating' the impact.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We expect the adoption of this standard will result in disclosure of additional jurisdictional level tax information in our consolidated financial statements.",
    "paragraph_id": "0001327567-26-000015:notes:17",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "estimates_and_discretion_credit_loss_practical_expedient_not_material",
    "what_changed": "The note on the practical expedient for expected credit losses on accounts receivable and contract assets, effective in the first quarter of fiscal 2027, now says adoption is not expected to have a material impact. Before, it said the company was 'currently evaluating'.",
    "account": "allowance for credit losses",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We do not expect the adoption of this standard will have a material impact on our consolidated financial statements.",
    "paragraph_id": "0001327567-26-000015:notes:21",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_share_repurchase_authorization_raised_and_extended",
    "what_changed": "New: on March 10, 2026 the board added $1.0 billion to the share repurchase program, bringing total authorization to $5.1 billion, and extended the expiration to December 31, 2026. MD&A repeats the authorization and states that $1.0 billion remained available at April 30, 2026.",
    "account": "cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "On March 10, 2026, our board of directors authorized an additional $1.0 billion increase to our share repurchase program, bringing the total authorization under this share repurchase program to $5.1 billion",
    "paragraph_id": "0001327567-26-000015:notes:156",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_executed_in_quarter",
    "what_changed": "New: during the three months the company repurchased and retired 7 million shares for $1.0 billion including transaction costs, at an average price of $147.70. The purchase was recorded against common stock and additional paid-in capital. There were no repurchases in the prior-year periods, and $1.0 billion remains available under the current authorization.",
    "account": "common stock and additional paid-in capital",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "we repurchased and retired 7 million shares of our common stock under our current repurchase authorization for an aggregate purchase price of $1.0 billion, including transaction costs, at an average price of $147.70 per share",
    "paragraph_id": "0001327567-26-000015:notes:157",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_financing_cash_used_for_repurchases_and_contingent_payments",
    "what_changed": "The financing cash flow explanation states nine-month cash used of $1.0 billion, an increase of $600 million. It now attributes this to share repurchases and contingent consideration payments, partly offset by 2025 Notes repayments that did not recur after their maturity. The description of financing activities now includes share repurchases and payments of contingent consideration.",
    "account": "net cash used in financing activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to repurchase of our common stock and payments of our contingent consideration liability during the nine months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:156",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_attributed_to_collections",
    "what_changed": "The operating cash flow explanation states nine-month cash from operations of $3.2 billion, an increase of $501 million. It attributes this to growth of the business as reflected in increased collections, partly offset by higher cash spending to support growth. The financing receivables note separately states sales of financing receivables in the same periods.",
    "account": "net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to growth of our business as reflected by increases in collections during the nine months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:149",
    "explanation": true,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_investing_cash_for_acquisitions_funded_by_investment_sales",
    "what_changed": "The investing cash flow explanation states nine-month cash used of $2.1 billion, an increase of $656 million. It attributes this to higher net cash payments for business acquisitions, partly offset by higher proceeds from sales and maturities of investments and by lower purchases of investments.",
    "account": "investments",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to an increase in net cash payments for business acquisitions during the nine months ended April 30, 2026, partially offset by higher proceeds from sales and maturities of investments and lower purchases of investments.",
    "paragraph_id": "0001327567-26-000015:mdna:153",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_financing_receivables_sold",
    "what_changed": "The financing receivables note states sales of financing receivables of $49 million for the three months and $54 million for the nine months ended April 30, 2026. For the same periods of 2025 it states $28 million and $30 million. The associated gains and losses are stated as not material.",
    "account": "financing receivables",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "We sold financing receivables of $49 million and $54 million for the three and nine months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:notes:59",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_headquarters_lease_term_extended",
    "what_changed": "New: in April 2026 the company signed three amendments extending its Santa Clara headquarters leases by twelve years, through July 2040. The amendments include rent holidays, scheduled rent increases, lease incentives, and renewal options to July 2052. Lease payments net of incentives are about $469 million. Right-of-use assets increased $262 million, against new operating lease liabilities. MD&A now states lease terms through fiscal 2040 and total operating lease obligations of $778 million.",
    "account": "operating lease liabilities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The amendments resulted in an increase of $262 million in our right-of-use assets in exchange for new operating lease liabilities.",
    "paragraph_id": "0001327567-26-000015:notes:139",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_headquarters_adjacent_land_purchase",
    "what_changed": "The property and equipment note, carried as changed, states that during the nine months the company bought 14.5 acres adjacent to its Santa Clara headquarters for $91 million, for future headquarters expansion, recorded in property and equipment, net. Whether the purchase is new this quarter or rolled forward from the prior quarter's text cannot be told from this input. The lease note for the same quarter extends the headquarters leases.",
    "account": "property and equipment, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "we purchased 14.5 acres of land adjacent to our headquarters in Santa Clara, California, for $91 million to accommodate future expansion of our headquarters",
    "paragraph_id": "0001327567-26-000015:notes:111",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_purchase_commitments_total_mdna_against_note",
    "what_changed": "MD&A states commitments to purchase products, components, cloud hosting and other services of $8.6 billion at April 30, 2026. The commitments note table states a total of $8,529 million, of which cloud is $8,092 million. A separate sentence in the note states a $92 million cloud hosting minimum commitment through September 2027 with no annual schedule. The prior quarter's table, as of January 31, 2026, showed a total of $6,789 million, of which cloud was $6,446 million. Reconciling the MD&A figure with the note is for the supervisor.",
    "account": "purchase commitments",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of April 30, 2026, our commitments to purchase products, components, cloud hosting and other services totaled $8.6 billion.",
    "paragraph_id": "0001327567-26-000015:mdna:140",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "liquidity_and_capital_cloud_hosting_minimum_commitment_without_annual_schedule",
    "what_changed": "The commitments note carries a sentence on a $92 million minimum purchase commitment with a cloud hosting provider through September 2027, with no specified annual commitments. The paragraph is marked as changed, but the prior wording is not in this input.",
    "account": "cost of subscription and support revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Additionally, we have a $92 million minimum purchase commitment with a cloud hosting service provider through September 2027 with no specified annual commitments.",
    "paragraph_id": "0001327567-26-000015:notes:143",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "controls_audit_and_filings_no_control_change_reported_in_acquisition_quarter",
    "what_changed": "The controls section, carried in full, reports no change in internal control over financial reporting during the quarter ended April 30, 2026 that materially affected it or is reasonably likely to. CyberArk ($21.1 billion of purchase consideration) and Koi were acquired and consolidated in that quarter. The section does not mention the acquired businesses, their integration, or any exclusion from the evaluation. The prior period's controls text is not in this input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "There were no changes in our internal control over financial reporting identified in connection with the evaluation required by Rule 13a-15(d) and 15d-15(d) of the Exchange Act that occurred during the fiscal quarter ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:item_4_controls:5",
    "explanation": false,
    "insufficient": false
  },
  {
    "id": "across_documents_material_agreement_current_report_without_body",
    "what_changed": "Insufficient. The 8-K index lists a current report dated April 13, 2026, inside the quarter. It carries the items for entry into a material definitive agreement (1.01), creation of a direct financial obligation (2.03), and exhibits. The bundle has no body for it. The quarterly report's financing text describes the April 2023 credit agreement (nothing outstanding at April 30, 2026; matures April 13, 2028) and the 2030 Notes assumed in February 2026. Which agreement or obligation this current report covers cannot be identified from this input.",
    "account": "debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "2026-04-13 0001193125-26-151637 — 1.01, 2.03, 9.01",
    "paragraph_id": "0001193125-26-151637",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "results_against_expectations_earnings_release_body_not_in_bundle",
    "what_changed": "Insufficient. The 8-K index lists an earnings-release current report (items 2.02 and 9.01) dated June 2, 2026, after the quarter. The bundle has no body for it, so no guidance or outlook text is available to set the reported results against.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "2026-06-02 0001327567-26-000012 — 2.02, 9.01",
    "paragraph_id": "0001327567-26-000012",
    "explanation": false,
    "insufficient": true
  }
]
```

## Paragraphs carried as text that are not items

Each line gives the paragraph id and the reason it is not an item. "Covered by" names the item id that carries the same substance.

### Controls section (Item 4)

- `0001327567-26-000015:item_4_controls:1` — heading.
- `0001327567-26-000015:item_4_controls:2` — heading.
- `0001327567-26-000015:item_4_controls:3` — date rolled forward (conclusion that disclosure controls are effective as of April 30, 2026).
- `0001327567-26-000015:item_4_controls:4` — heading.
- `0001327567-26-000015:item_4_controls:6` — heading.
- `0001327567-26-000015:item_4_controls:7` — boilerplate on limitations of controls; no change identifiable.
- `0001327567-26-000015:item_4_controls:8` — page number.

### MD&A

- `0001327567-26-000015:mdna:5` — date rolled forward (three and nine months).
- `0001327567-26-000015:mdna:11` — wording: identities added to the mission statement; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:14` — product description (Prisma Browser); changed words cannot be isolated; bears on no account.
- `0001327567-26-000015:mdna:17` — product description (Prisma AIRS components); bears on no account.
- `0001327567-26-000015:mdna:21` — product description. The Koi part is covered by articulation_and_the_filed_history_koi_consideration_against_prior_subsequent_event; the Chronosphere pipeline integration is product only.
- `0001327567-26-000015:mdna:28` — heading of the new identity section; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:30` — identity platform bullet; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:31` — identity platform bullet; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:32` — identity platform bullet; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:33` — identity platform bullet; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:34` — identity platform bullet; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:mdna:50` — table; amounts only.
- `0001327567-26-000015:mdna:51` — table; amounts only.
- `0001327567-26-000015:mdna:56` — table; amounts only.
- `0001327567-26-000015:mdna:60` — table; amounts only.
- `0001327567-26-000015:mdna:62` — table; amounts only (the acceleration substance is in earnings_quality_accelerated_vesting_charge_on_cyberark_and_koi).
- `0001327567-26-000015:mdna:64` — new heading (Impact of Acquisitions); covered by structure_and_disclosure_changes_acquisition_impact_disclosed_at_discretion.
- `0001327567-26-000015:mdna:65` — CyberArk consideration and replacement awards; covered by structure_and_disclosure_changes_cyberark_purchase_consideration_and_allocation and earnings_quality_cyberark_replacement_awards_expensed_over_service.
- `0001327567-26-000015:mdna:68` — adds business acquisitions as a cause of revenue variability; covered by structure_and_disclosure_changes_acquisition_impact_disclosed_at_discretion.
- `0001327567-26-000015:mdna:70` — product revenue description adds identity security offerings; covered by revenue_recognition_cyberark_on_premise_licenses_in_product_revenue.
- `0001327567-26-000015:mdna:71` — table; amounts only.
- `0001327567-26-000015:mdna:72` — CyberArk licenses as a product revenue driver; covered by revenue_recognition_cyberark_on_premise_licenses_in_product_revenue.
- `0001327567-26-000015:mdna:75` — table; amounts only.
- `0001327567-26-000015:mdna:77` — acquisitions added as a subscription and support driver; covered by revenue_recognition_cyberark_identity_subscriptions_in_subscription_revenue.
- `0001327567-26-000015:mdna:79` — table; amounts only.
- `0001327567-26-000015:mdna:80` — date rolled forward; same geographic explanation.
- `0001327567-26-000015:mdna:85` — table; amounts only.
- `0001327567-26-000015:mdna:89` — description of cost components; covered by earnings_quality_subscription_cost_hosting_amortization_and_personnel.
- `0001327567-26-000015:mdna:90` — table; amounts only.
- `0001327567-26-000015:mdna:94` — table; amounts only.
- `0001327567-26-000015:mdna:97` — page number.
- `0001327567-26-000015:mdna:99` — amounts only (unrecognized share-based compensation of $3.6 billion over 2.6 years, the same figure as notes:177); substance covered by earnings_quality_cyberark_replacement_awards_expensed_over_service.
- `0001327567-26-000015:mdna:102` — table; amounts only.
- `0001327567-26-000015:mdna:105` — description of cost components; covered by earnings_quality_sales_and_marketing_personnel_and_acquired_amortization.
- `0001327567-26-000015:mdna:106` — table; amounts only.
- `0001327567-26-000015:mdna:108` — page number.
- `0001327567-26-000015:mdna:111` — table; amounts only.
- `0001327567-26-000015:mdna:114` — wording only; describes the matured 2025 Notes.
- `0001327567-26-000015:mdna:115` — table; amounts only.
- `0001327567-26-000015:mdna:116` — date rolled forward; same 2025 Notes maturity explanation.
- `0001327567-26-000015:mdna:117` — page number.
- `0001327567-26-000015:mdna:119` — adds fair value changes of convertible notes and capped calls to the description of other income; covered by estimates_and_discretion_fair_value_option_elected_for_acquired_convertible_notes.
- `0001327567-26-000015:mdna:120` — table; amounts only.
- `0001327567-26-000015:mdna:124` — table; amounts only.
- `0001327567-26-000015:mdna:125` — covered by earnings_quality_negative_quarterly_effective_tax_rate.
- `0001327567-26-000015:mdna:127` — page number.
- `0001327567-26-000015:mdna:129` — table; amounts only.
- `0001327567-26-000015:mdna:132` — 2030 Notes summary; covered by liquidity_and_capital_assumed_cyberark_convertible_notes, liquidity_and_capital_make_whole_conversions_settled_in_cash_by_election and estimates_and_discretion_surrendered_notes_valued_on_prices_after_quarter_end.
- `0001327567-26-000015:mdna:134` — date rolled forward (credit agreement, nothing outstanding).
- `0001327567-26-000015:mdna:136` — covered by liquidity_and_capital_share_repurchase_authorization_raised_and_extended and liquidity_and_capital_share_repurchases_executed_in_quarter.
- `0001327567-26-000015:mdna:137` — page number.
- `0001327567-26-000015:mdna:139` — covered by liquidity_and_capital_headquarters_lease_term_extended (the $778 million figure is quoted there).
- `0001327567-26-000015:mdna:141` — covered by estimates_and_discretion_qradar_contingent_consideration_estimate_reduced.
- `0001327567-26-000015:mdna:143` — date rolled forward.
- `0001327567-26-000015:mdna:144` — table; amounts only.
- `0001327567-26-000015:mdna:150` — page number.
- `0001327567-26-000015:mdna:155` — description adds share repurchases and contingent consideration payments; covered by liquidity_and_capital_financing_cash_used_for_repurchases_and_contingent_payments.
- `0001327567-26-000015:mdna:161` — wording only (cross-reference to the accounting pronouncements note).
- `0001327567-26-000015:mdna:162` — page number.

### Notes

- `0001327567-26-000015:notes:2` — wording: identities added to the business description; covered by structure_and_disclosure_changes_identity_security_platform_section_added.
- `0001327567-26-000015:notes:10` — policy exception for CyberArk; covered by estimates_and_discretion_fair_value_option_elected_for_acquired_convertible_notes.
- `0001327567-26-000015:notes:11` — heading.
- `0001327567-26-000015:notes:12` — acquired notes and assumed capped calls; covered by estimates_and_discretion_fair_value_option_elected_for_acquired_convertible_notes and liquidity_and_capital_assumed_cyberark_convertible_notes.
- `0001327567-26-000015:notes:14` — capped call policy; covered by estimates_and_discretion_fair_value_option_elected_for_acquired_convertible_notes and estimates_and_discretion_capped_calls_valued_with_black_scholes.
- `0001327567-26-000015:notes:15` — heading.
- `0001327567-26-000015:notes:19` — wording only ("could be applied" became "can be applied").
- `0001327567-26-000015:notes:28` — table; amounts only.
- `0001327567-26-000015:notes:30` — table; amounts only.
- `0001327567-26-000015:notes:32` — date rolled forward, amounts only (revenue recognized from beginning deferred balances).
- `0001327567-26-000015:notes:34` — date rolled forward, amounts only (remaining performance obligations and the next-12-month portion).
- `0001327567-26-000015:notes:35` — date rolled forward.
- `0001327567-26-000015:notes:36` — table; amounts only.
- `0001327567-26-000015:notes:37` — table; amounts only. The new rows for convertible notes and capped calls are covered by liquidity_and_capital_remaining_convertible_notes_classified_long_term and estimates_and_discretion_capped_calls_valued_with_black_scholes.
- `0001327567-26-000015:notes:38` — QRadar undiscounted range and payment schedule; covered by estimates_and_discretion_qradar_contingent_consideration_estimate_reduced.
- `0001327567-26-000015:notes:42` — table; amounts only; covered by estimates_and_discretion_qradar_contingent_consideration_estimate_reduced.
- `0001327567-26-000015:notes:43` — date rolled forward.
- `0001327567-26-000015:notes:44` — heading.
- `0001327567-26-000015:notes:45` — date rolled forward.
- `0001327567-26-000015:notes:46` — table; amounts only.
- `0001327567-26-000015:notes:47` — table; amounts only.
- `0001327567-26-000015:notes:48` — date rolled forward (unrealized losses wording unchanged per the note history).
- `0001327567-26-000015:notes:49` — date rolled forward.
- `0001327567-26-000015:notes:50` — table; amounts only.
- `0001327567-26-000015:notes:51` — heading.
- `0001327567-26-000015:notes:52` — date rolled forward, amounts only.
- `0001327567-26-000015:notes:53` — date rolled forward.
- `0001327567-26-000015:notes:54` — table; amounts only.
- `0001327567-26-000015:notes:56` — table; amounts only.
- `0001327567-26-000015:notes:58` — date rolled forward.
- `0001327567-26-000015:notes:61` — amounts only (hedge notional).
- `0001327567-26-000015:notes:62` — amounts only (hedge gains in AOCI).
- `0001327567-26-000015:notes:63` — amounts only (non-designated notional).
- `0001327567-26-000015:notes:70` — Chronosphere goodwill (a prior-quarter acquisition); no new fact or amount identifiable.
- `0001327567-26-000015:notes:75` — table; covered by structure_and_disclosure_changes_cyberark_purchase_consideration_and_allocation.
- `0001327567-26-000015:notes:77` — table; covered by structure_and_disclosure_changes_cyberark_purchase_consideration_and_allocation.
- `0001327567-26-000015:notes:82` — table caption.
- `0001327567-26-000015:notes:83` — table; amounts only; covered by estimates_and_discretion_cyberark_workforce_optimization_plan_and_severance_liability.
- `0001327567-26-000015:notes:84` — heading.
- `0001327567-26-000015:notes:87` — table; amounts only.
- `0001327567-26-000015:notes:89` — table; amounts only (Koi developed technology, five years).
- `0001327567-26-000015:notes:90` — heading.
- `0001327567-26-000015:notes:94` — caption; covered by structure_and_disclosure_changes_pro_forma_pairs_cyberark_calendar_quarters.
- `0001327567-26-000015:notes:95` — table; amounts only.
- `0001327567-26-000015:notes:98` — caption (Chronosphere consideration, a prior-quarter acquisition).
- `0001327567-26-000015:notes:99` — caption; covered by structure_and_disclosure_changes_cyberark_purchase_consideration_and_allocation.
- `0001327567-26-000015:notes:101` — caption; date rolled forward.
- `0001327567-26-000015:notes:102` — table; amounts only.
- `0001327567-26-000015:notes:104` — caption; date rolled forward.
- `0001327567-26-000015:notes:105` — table; amounts only. The new line titles are covered by estimates_and_discretion_cyberark_platform_renewals_long_useful_life.
- `0001327567-26-000015:notes:106` — caption.
- `0001327567-26-000015:notes:107` — table; amounts only; covered by earnings_quality_intangible_amortization_now_in_cost_of_product_revenue.
- `0001327567-26-000015:notes:108` — caption; date rolled forward.
- `0001327567-26-000015:notes:109` — table; amounts only.
- `0001327567-26-000015:notes:112` — heading.
- `0001327567-26-000015:notes:113` — matured 2025 Notes; no substantive change identifiable.
- `0001327567-26-000015:notes:114` — wording only (tense).
- `0001327567-26-000015:notes:115` — wording only (tense).
- `0001327567-26-000015:notes:116` — date rolled forward. The prior-quarter detail on the share split was removed; no new settlement.
- `0001327567-26-000015:notes:117` — heading.
- `0001327567-26-000015:notes:118` — heading.
- `0001327567-26-000015:notes:120` — redemption terms of the assumed notes; covered by liquidity_and_capital_assumed_cyberark_convertible_notes.
- `0001327567-26-000015:notes:121` — lead-in to conversion terms; covered by liquidity_and_capital_remaining_convertible_notes_classified_long_term.
- `0001327567-26-000015:notes:122` — sale price condition; covered by liquidity_and_capital_remaining_convertible_notes_classified_long_term.
- `0001327567-26-000015:notes:123` — trading price condition; covered by liquidity_and_capital_assumed_cyberark_convertible_notes.
- `0001327567-26-000015:notes:124` — corporate events condition; covered by liquidity_and_capital_assumed_cyberark_convertible_notes.
- `0001327567-26-000015:notes:125` — conversion on or after February 15, 2030; covered by liquidity_and_capital_assumed_cyberark_convertible_notes.
- `0001327567-26-000015:notes:126` — settlement and fundamental change terms; covered by liquidity_and_capital_make_whole_conversions_settled_in_cash_by_election.
- `0001327567-26-000015:notes:131` — heading.
- `0001327567-26-000015:notes:132` — capped call terms; covered by estimates_and_discretion_capped_calls_valued_with_black_scholes.
- `0001327567-26-000015:notes:135` — heading.
- `0001327567-26-000015:notes:136` — credit facility terms; no change identifiable (see across_documents_material_agreement_current_report_without_body).
- `0001327567-26-000015:notes:137` — credit facility pricing terms; no change identifiable.
- `0001327567-26-000015:notes:138` — date rolled forward (compliance, nothing outstanding).
- `0001327567-26-000015:notes:140` — heading.
- `0001327567-26-000015:notes:141` — date rolled forward (per the note change history).
- `0001327567-26-000015:notes:142` — table; amounts only; covered by across_documents_purchase_commitments_total_mdna_against_note.
- `0001327567-26-000015:notes:144` — heading.
- `0001327567-26-000015:notes:145` — litigation boilerplate; no change identifiable.
- `0001327567-26-000015:notes:146` — litigation boilerplate; no change identifiable.
- `0001327567-26-000015:notes:147` — boilerplate sentence.
- `0001327567-26-000015:notes:148` — heading.
- `0001327567-26-000015:notes:151` — heading.
- `0001327567-26-000015:notes:152` — Finjan; no new event or amount identifiable (latest dated event April 21, 2025).
- `0001327567-26-000015:notes:153` — heading.
- `0001327567-26-000015:notes:154` — Eire OG; resolution dated December 2025, in the prior quarter; no new fact identifiable.
- `0001327567-26-000015:notes:159` — caption; date rolled forward.
- `0001327567-26-000015:notes:160` — table; amounts only.
- `0001327567-26-000015:notes:162` — RSUs assumed in acquisitions; covered by earnings_quality_cyberark_replacement_awards_expensed_over_service and earnings_quality_koi_replacement_awards_expensed_over_service.
- `0001327567-26-000015:notes:166` — date rolled forward, amounts only (performance share grants and approvals).
- `0001327567-26-000015:notes:167` — caption; date rolled forward.
- `0001327567-26-000015:notes:168` — table; amounts only.
- `0001327567-26-000015:notes:170` — date rolled forward.
- `0001327567-26-000015:notes:171` — caption.
- `0001327567-26-000015:notes:172` — table; amounts only.
- `0001327567-26-000015:notes:175` — table; amounts only.
- `0001327567-26-000015:notes:177` — amounts only; the same figure as mdna:99.
- `0001327567-26-000015:notes:178` — covered by estimates_and_discretion_effective_tax_rate_fluctuation_from_cyberark_integration and earnings_quality_negative_quarterly_effective_tax_rate.
- `0001327567-26-000015:notes:180` — wording only ("(loss)" added to the title and definitions).
- `0001327567-26-000015:notes:181` — caption.
- `0001327567-26-000015:notes:182` — table; amounts only.
- `0001327567-26-000015:notes:183` — wording only.
- `0001327567-26-000015:notes:184` — table; amounts only.
- `0001327567-26-000015:notes:187` — table; amounts only; covered by earnings_quality_gains_on_investment_sales_to_fund_acquisitions and earnings_quality_convertible_notes_fair_value_loss_in_other_income.
- `0001327567-26-000015:notes:188` — heading.

### 8-K index

- `0001193125-26-119729` (dated March 23, 2026; other events) — item codes only, no body; content cannot be read.
- `0001327567-26-000009` (dated March 11, 2026; other events and exhibits) — item codes only, no body; content cannot be read.
- All index lines dated on or before February 17, 2026 — filed before the prior quarterly report (February 18, 2026); earlier periods, not new to this one.
- Late-filing notifications — none listed.

### Note change history and prior flags

- Note change history — used only to identify what changed. Each of its current-period paragraphs repeats a notes paragraph accounted for above. Its removed paragraphs are reflected in related_parties_contingencies_and_subsequent_events_portkey_closed_after_quarter_end, articulation_and_the_filed_history_koi_consideration_against_prior_subsequent_event and estimates_and_discretion_convertible_notes_and_capped_calls_added_to_estimates, and in the notes:52 and notes:116 lines above.
- Prior flags — none on record.
