# CSCO notes-text reader: 0000858877-26-000078 (10-Q, third quarter fiscal 2026, period ended April 25, 2026)

Prior period of the same kind: 0000858877-26-000021 (10-Q, second quarter fiscal 2026).

## Scope of the input

- **Read in full:** input_notes.md, input_mdna.md, input_controls.md, input_notes_history.md, input_8k.md and input_prior_predictions.md.
- **Prior flags:** none on record.
- **Out-of-scope material:** none found. There is no trend table, price, return, short interest, other-company file, prior probability or outcome window in the directory.
- **Sections missing from the input:**
  - No auditor's report text. input_controls.md carries Item 4 only.
  - No Item 1A diff, no Exhibit 21 diff and no Exhibit 10.
  - No verbatim 8-K item body. input_8k.md is a list of item codes only, and it records no late-filing notifications.
- **Note change history:** used only to see what changed from the prior 10-Q. Its paragraphs are not listed separately. Where it shows a text paragraph as unchanged, the list below says so.
- **Arithmetic:** none performed. Directions below are only what the prose says or implies. Where the prose just states two amounts, the direction is `none`, and the comparison is left to the numbers reader.

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_prospective_adoption",
    "what_changed": "The note now says the company expects to adopt the income tax disclosure update (rate reconciliation and taxes paid) on a prospective basis in its fiscal 2026 Form 10-K. The prior text said only that the update would be effective for that 10-K and that the company was evaluating the impact. The transition method is now chosen. This affects the disclosure only.",
    "account": "income tax disclosures (no measurement effect stated)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "We expect to adopt this accounting standard update on a prospective basis in our fiscal 2026 Form 10-K.",
    "paragraph_id": "0000858877-26-000078:notes:6",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_new_restructuring_plan_after_quarter_end",
    "what_changed": "New subsequent-event disclosure. A restructuring plan (the Fiscal 2026 Plan) was announced in the fourth quarter of fiscal 2026 to invest in silicon, optics, security and AI. Total pre-tax charges are estimated at up to $1 billion for severance, other one-time termination benefits and other costs. The plan is expected to be substantially complete by the end of fiscal 2027. The 8-K code list shows a 2026-05-13 filing (0000858877-26-000075) that carries Item 2.05 (exit or disposal costs), which fits this plan. No 8-K body is in the input.",
    "account": "restructuring and other charges",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The total pre-tax charges are estimated to be up to $1 billion consisting of severance and other one-time termination benefits, and other costs.",
    "paragraph_id": "0000858877-26-000078:notes:70",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_fourth_quarter_charge",
    "what_changed": "MD&A adds an amount the note does not give. About $450 million of pre-tax charges under the new plan are expected in the fourth quarter of fiscal 2026, out of a total of up to $1 billion.",
    "account": "restructuring and other charges",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We expect to recognize approximately $450 million in pre-tax charges in the fourth quarter of fiscal 2026.",
    "paragraph_id": "0000858877-26-000078:mdna:200",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_savings_reinvested_not_material",
    "what_changed": "MD&A says substantially all cost savings from the new plan will be reinvested in growth areas, so overall savings are not expected to be material. The prose therefore gives no expectation that operating expenses will fall from the plan.",
    "account": "operating expenses",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We expect to reinvest substantially all of the cost savings from this restructuring plan in our key growth opportunities. As a result, the overall cost savings from this restructuring plan are not expected to be material.",
    "paragraph_id": "0000858877-26-000078:mdna:200",
    "explanation": false
  },
  {
    "id": "earnings_quality_margin_aided_by_lower_restructuring_and_amortization",
    "what_changed": "MD&A attributes the nine-month rise in operating margin partly to lower restructuring and other charges and lower amortization of purchased intangibles, not only to revenue growth. mdna:196 says the amortization decline comes from assets becoming fully amortized and from a fiscal 2025 impairment. mdna:200 now expects about $450 million of restructuring charges in the fourth quarter. The prose therefore points to the restructuring part of this help reversing next quarter.",
    "account": "operating income (GAAP)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "These changes primarily resulted from revenue growth, lower restructuring and other charges and lower amortization of purchased intangible assets in the first nine months of fiscal 2026.",
    "paragraph_id": "0000858877-26-000078:mdna:208",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_costs_in_product_margin",
    "what_changed": "The Q3 product gross margin text now names higher memory costs as eroding productivity benefits. It ties the negative mix to higher Networking revenue and cites pricing as a smaller negative.",
    "account": "product gross margin; product cost of sales",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The negative impacts from product mix were primarily due to higher Networking revenue. Productivity benefits were adversely impacted by higher memory costs.",
    "paragraph_id": "0000858877-26-000078:mdna:145",
    "explanation": false
  },
  {
    "id": "across_documents_product_margin_driver_attribution",
    "what_changed": "The Q3 overview and the detailed product margin discussion give different driver lists. The overview (mdna:12) calls product mix and higher memory costs the primary drivers, offset by productivity and lower amortization, and does not mention pricing. The detailed section (mdna:145) cites mix and, to a lesser extent, pricing, offset by productivity. There memory costs appear as a drag within productivity, and the factor-table footnote (mdna:143) places memory inside productivity. Supervisors should reconcile the attributions against the factor table at mdna:142.",
    "account": "product gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Product gross margin decreased by 2.5 percentage points, primarily driven by negative impacts from product mix and higher memory costs, partially offset by productivity improvements and lower amortization of purchased intangible assets.",
    "paragraph_id": "0000858877-26-000078:mdna:12",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_memory_supply_agreements_variable_pricing",
    "what_changed": "New sentence in the commitments note, repeated in the policy block (notes:209) and in MD&A (mdna:259). Some inventory purchase commitments now come from long-term supply agreements for fixed quantities of certain memory components at variable prices. Quantity is committed while price is not, so the company carries memory price exposure on committed volumes. mdna:145 separately says higher memory costs hurt productivity.",
    "account": "inventory purchase commitments; product cost of sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In addition, certain of these inventory purchase commitments are related to long-term supply agreements for fixed quantities of certain memory components for which pricing is variable.",
    "paragraph_id": "0000858877-26-000078:notes:182",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_purchase_commitment_excess_liability",
    "what_changed": "The excess purchase commitment liability is stated as $209 million at April 25, 2026 and $206 million at July 26, 2025. The Q2 text stated $185 million at January 24, 2026. No cause is given in the prose. The note and MD&A describe inventory purchase commitments as substantially increased over the same period (mdna:256).",
    "account": "other current liabilities (purchase commitment liability)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of April 25, 2026 and July 26, 2025, the liability for these purchase commitments was $209 million and $206 million, respectively, and was included in other current liabilities.",
    "paragraph_id": "0000858877-26-000078:notes:185",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_and_commitment_provisions",
    "what_changed": "MD&A states total provisions for inventory and the purchase-commitment liability of $187 million for the first nine months of fiscal 2026 and $459 million for the same fiscal 2025 period. It gives no cause for the level, alongside inventory and commitments that the prose describes as increased (mdna:256). The accompanying risk language on write-downs is carried unchanged. The comparison is left to the numbers reader.",
    "account": "inventory write-downs and purchase commitment liability (product cost of sales)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Our total provisions for inventory and the liability related to purchase commitments with contract manufacturers and suppliers were $187 million and $459 million for the first nine months of fiscal 2026 and 2025, respectively.",
    "paragraph_id": "0000858877-26-000078:mdna:43",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_inventory_build_for_hyperscaler_demand",
    "what_changed": "MD&A states that inventory rose 49% and inventory purchase commitments 111% from fiscal year-end. It attributes the combined 93% increase primarily to commitments with contract manufacturers and suppliers for Cisco Silicon One and other products, to meet demand from hyperscalers and other customers.",
    "account": "inventories; inventory purchase commitments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Inventory as of April 25, 2026 increased by 49% and inventory purchase commitments with contract manufacturers and suppliers increased by 111% from our balances at the end of fiscal 2025. The combined increase of 93% in our inventory and inventory purchase commitments as compared with the end of fiscal 2025 was primarily related to commitments with contract manufacturers and suppliers related to manufacturing Cisco Silicon One and other products to meet the demand from hyperscalers and other customers.",
    "paragraph_id": "0000858877-26-000078:mdna:256",
    "explanation": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_single_memory_supplier_commitment",
    "what_changed": "New disclosure that in Q3 the company increased purchase commitments with one unnamed supplier to secure memory components. This points to supplier concentration in memory. Combined with the variable-price memory agreements in notes:182, it adds cost and commitment exposure to a single counterparty.",
    "account": "inventory purchase commitments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In the third quarter of fiscal 2026, we increased our purchase commitments with a certain supplier to help secure memory components.",
    "paragraph_id": "0000858877-26-000078:mdna:256",
    "explanation": false
  },
  {
    "id": "results_against_expectations_inventory_expected_to_rise",
    "what_changed": "New forward statement that inventory balances may increase in future quarters as the company works to fulfil hyperscaler and other demand.",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We expect our inventory balances may increase in future quarters as we work to fulfill this demand.",
    "paragraph_id": "0000858877-26-000078:mdna:256",
    "explanation": false
  },
  {
    "id": "across_documents_inventory_increase_two_attributions",
    "what_changed": "A second 'primarily' explanation covers the same build. mdna:257 attributes the nine-month increases primarily to arrangements that secure supply and pricing for certain components, including memory, and to contract-manufacturer commitments to meet demand and manage lead times. mdna:256 attributes the combined increase primarily to Silicon One commitments for hyperscaler demand. Supervisors should weigh the two attributions.",
    "account": "inventories; inventory purchase commitments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increases during the first nine months of fiscal 2026 were primarily due to arrangements to secure supply and pricing for certain product components, including memory, and commitments with contract manufacturers to meet customer demand and help manage lead times.",
    "paragraph_id": "0000858877-26-000078:mdna:257",
    "explanation": true
  },
  {
    "id": "revenue_recognition_receivables_decline_billing_timing",
    "what_changed": "MD&A states accounts receivable, net decreased about 3% from fiscal year-end and attributes this to the timing and amount of billings in Q3 compared with Q4 fiscal 2025. notes:30 states $6.5 billion and $6.7 billion. The same MD&A states Q3 product revenue grew 17% (mdna:11). mdna:267 says channel partner financing can transfer receivables to third parties as true sales that are derecognized. Whether these reconcile is for the numbers reader.",
    "account": "accounts receivable, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Our accounts receivable net, as of April 25, 2026 decreased by approximately 3%, as compared with the end of fiscal 2025, primarily due to timing and amount of product and service billings in the third quarter of fiscal 2026 compared with the fourth quarter of fiscal 2025.",
    "paragraph_id": "0000858877-26-000078:mdna:249",
    "explanation": true
  },
  {
    "id": "revenue_recognition_channel_partner_financing_volume",
    "what_changed": "The note states channel partner financing volume of $7.7 billion for Q3 fiscal 2026 and $5.9 billion for Q3 fiscal 2025, and $21.7 billion and $18.1 billion for the nine-month periods. The Q2 text stated $7.4 billion and $6.2 billion for the second quarters. The prose does not characterize the change. Per mdna:267 these arrangements can transfer receivables to third parties that are derecognized, so volume bears on reported receivables.",
    "account": "accounts receivable, net; product revenue",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The volume of channel partner financing was $7.7 billion and $5.9 billion for the third quarter of fiscal 2026 and 2025, respectively, and $21.7 billion and $18.1 billion for the first nine months of fiscal 2026 and 2025, respectively.",
    "paragraph_id": "0000858877-26-000078:notes:194",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_channel_partner_guarantee_balance",
    "what_changed": "The balance of channel partner financing subject to guarantees is stated at $1.2 billion at April 25, 2026 and $1.3 billion at July 26, 2025. The Q2 text stated $1.3 billion at both dates. The maximum potential future payments table (notes:196) and mdna:268 give $127 million, of which $12 million is recorded as deferred revenue.",
    "account": "financing guarantees; deferred revenue",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The balance of the channel partner financing subject to guarantees was $1.2 billion as of April 25, 2026 and $1.3 billion as of July 26, 2025.",
    "paragraph_id": "0000858877-26-000078:notes:194",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_centripetal_favorable_rulings",
    "what_changed": "Centripetal litigation update. On April 29, 2026, after quarter end, the Federal Circuit affirmed the district court's non-infringement ruling; the appeal was previously pending. At an April 2, 2026 hearing the German court announced a preliminary opinion of non-infringement; the prior text described that hearing as upcoming. A French final hearing is now set for October 8, 2026, where the prior text said none was set. The German invalidity appeal hearing stays at November 10, 2026, and the PTAB remand continues.",
    "account": "none (no accrual described)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "and on April 29, 2026, the Federal Circuit affirmed the District Court",
    "paragraph_id": "0000858877-26-000078:notes:204",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_brazil_asserted_claims_remeasured",
    "what_changed": "Asserted Brazil import-tax claims are restated at the April 25, 2026 exchange rate: $155 million tax, $966 million interest and $320 million penalties. The Q2 text gave $148 million, $902 million and $303 million at the January 24, 2026 rate. Claim years, the joint-liability theory and the statement that no loss can be estimated (notes:203, unchanged per history) are unchanged.",
    "account": "none (unaccrued loss contingency)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The total remaining asserted claims by Brazilian state and federal tax authorities aggregate to $155 million for the alleged evasion of import and other taxes, $966 million for interest, and $320 million for various penalties, all determined using an exchange rate as of April 25, 2026.",
    "paragraph_id": "0000858877-26-000078:notes:202",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_non_marketable_equity_funding_commitments",
    "what_changed": "Funding commitments are now described as primarily related to non-marketable equity securities, where they were previously tied to privately held investments. They are stated at $0.6 billion at April 25, 2026 and $0.3 billion at July 26, 2025; the Q2 text stated $0.7 billion at January 24, 2026. A sentence moved here from the investments note says the commitments plus carrying value are the maximum exposure.",
    "account": "other commitments; non-marketable equity securities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We have certain funding commitments, primarily related to our non-marketable equity securities. The funding commitments were $0.6 billion and $0.3 billion as of April 25, 2026 and July 26, 2025, respectively.",
    "paragraph_id": "0000858877-26-000078:notes:187",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_non_marketable_equity_securities_presentation",
    "what_changed": "The investments note replaces '(c) Investments in Privately Held Companies' with '(c) Non-Marketable Equity Securities'. The category is redefined to include publicly traded entities without readily determinable fair value. A new carrying-value table (notes:137) covers measurement-alternative initial cost, cumulative upward and downward adjustments, a new restricted equity securities line, consolidated investments, and NAV, equity-method and other holdings. Removed prose: the privately held carrying value sentence, the measurement-alternative carrying value sentence with its adjustment table, and the separate NAV private equity fund sentence.",
    "account": "non-marketable equity securities (other assets)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our non-marketable equity securities are investments in privately held entities, venture funds, and publicly traded entities that do not have readily determinable fair value (RDFV).",
    "paragraph_id": "0000858877-26-000078:notes:136",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_restricted_equity_securities_marketability_discount",
    "what_changed": "New investment category: restricted equity securities in publicly traded entities. They are measured at fair value on a recurring basis and classified Level 2, using pricing models that reduce observable inputs by a management-applied discount for lack of marketability. Fair value is $379 million, and unrealized losses of $31 million were recognized for both Q3 and the nine months, so all of it fell in Q3. The table shows no balance in this line at July 26, 2025.",
    "account": "non-marketable equity securities; other income (loss), net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The fair value of these restricted equity securities was $379 million as of April 25, 2026 and we recognized unrealized losses of $31 million for the third quarter and first nine months of fiscal 2026.",
    "paragraph_id": "0000858877-26-000078:notes:139",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_measurement_alternative_observable_transaction_adjustments",
    "what_changed": "The investments note now describes the measurement-alternative basis in its own paragraph. Carrying values are adjusted on observable transactions in identical or similar securities of the same issuer, or on impairment, and are classified Level 3 using unobservable inputs such as volatility, rights and obligations. The new table (notes:137) shows cumulative upward adjustments separately. mdna:216 and mdna:217 attribute the other income change to gains on these securities.",
    "account": "non-marketable equity securities; other income (loss), net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Adjustments are made when observable transactions for identical or similar investments of the same issuer occur, or due to impairment.",
    "paragraph_id": "0000858877-26-000078:notes:138",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_consolidated_venture_funds_investment_company_accounting",
    "what_changed": "Consolidated investments are now described as venture funds that qualify for investment company specific accounting, consolidated under the voting interest entity model. The prior text said only that certain privately held investments are consolidated under that model. Noncontrolling interest is stated at $271 million at April 25, 2026 and $162 million at July 26, 2025; the Q2 text stated $221 million at January 24, 2026.",
    "account": "noncontrolling interests; consolidated investments",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our non-marketable equity securities classified as consolidated investments include venture funds that qualified for investment company specific accounting, the accounts of which are consolidated within our financial statements under the voting interest entity model.",
    "paragraph_id": "0000858877-26-000078:notes:140",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_income_equity_securities_gains",
    "what_changed": "MD&A attributes the Q3 change in other income (loss), net primarily to higher gains on marketable and non-marketable equity securities. These are non-operating gains; for the non-marketable part they are valuation-driven (see notes:138, notes:139). Net income and diluted EPS growth are stated at mdna:6 and mdna:12. How much of that growth this line accounts for is for the numbers reader.",
    "account": "other income (loss), net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "For the third quarter of fiscal 2026, the change in our other income (loss), net was primarily driven by higher gains on our marketable and non-marketable equity securities.",
    "paragraph_id": "0000858877-26-000078:mdna:217",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_subscription_revenue_decline",
    "what_changed": "The Q3 overview states total subscription revenue decreased 2% and total software revenue was $5.7 billion, up 1%, while product revenue grew 17% and services revenue fell 1%.",
    "account": "subscription and software revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In the third quarter of fiscal 2026, total software revenue was $5.7 billion across all product areas and services, an increase of 1%. Total subscription revenue decreased 2%.",
    "paragraph_id": "0000858877-26-000078:mdna:11",
    "explanation": false
  },
  {
    "id": "revenue_recognition_splunk_shift_to_cloud_subscriptions",
    "what_changed": "Q3 Security product revenue is described as flat, with declines in prior-generation products and Splunk offerings. MD&A says customers continued to shift Splunk consumption from on-premise deals to cloud subscriptions. mdna:126 also cites a Splunk decline in Observability. The revenue policy (notes:9) says subscription revenue includes amounts recognized over time as well as upfront, so a mix shift toward cloud moves recognition timing.",
    "account": "product revenue (Security, Observability); deferred revenue",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "We continued to see a change in how our customers consumed Splunk offerings, shifting from fewer on-premise deals to more cloud subscriptions.",
    "paragraph_id": "0000858877-26-000078:mdna:114",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_webex_suite_decline",
    "what_changed": "Q3 Collaboration product revenue is stated as down 1% ($7 million), driven by declines in Webex Suite and partly offset by devices, cloud contact center and CPaaS.",
    "account": "product revenue (Collaboration)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Revenue in our Collaboration product category decreased by 1%, or $7 million, primarily driven by declines in Webex Suite offerings partially offset by growth in Collaboration Devices, Cloud Contact Center and CPaaS offerings.",
    "paragraph_id": "0000858877-26-000078:mdna:119",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_support_services_revenue_decline",
    "what_changed": "Q3 services revenue is stated as down 1%, driven by lower support services revenue and partly offset by professional services, with declines in Americas and APJC.",
    "account": "services revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Services revenue decreased by 1% in the third quarter of fiscal 2026 compared with the third quarter of fiscal 2025, with the decline primarily driven by lower revenue from support services, partially offset by higher professional services.",
    "paragraph_id": "0000858877-26-000078:mdna:133",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_services_remaining_performance_obligations_decline",
    "what_changed": "MD&A states total RPO flat against fiscal year-end, product RPO up 2% and services RPO down 3%.",
    "account": "remaining performance obligations (services); future services revenue",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Remaining performance obligations for services decreased 3%.",
    "paragraph_id": "0000858877-26-000078:mdna:279",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_deferred_services_lower_business_volume",
    "what_changed": "MD&A attributes a 1% decrease in deferred services revenue to lower business volume as well as ongoing amortization. 'Lower business volume' is named as a cause.",
    "account": "deferred revenue (services)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The decrease in deferred services revenue of 1% was driven by lower business volume and ongoing amortization of deferred services revenue.",
    "paragraph_id": "0000858877-26-000078:mdna:282",
    "explanation": false
  },
  {
    "id": "across_documents_ai_infrastructure_demand_links_revenue_mix_and_inventory",
    "what_changed": "Q3 Americas product growth is described as led by the Service Provider and Cloud market, largely from AI Infrastructure revenue. The same demand is named for the inventory and commitment build (mdna:256, hyperscalers) and for the negative mix from higher Networking revenue (mdna:145). The prose thus links revenue growth, margin mix and inventory exposure to one customer group.",
    "account": "product revenue (Networking, Americas)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Product revenue in the Americas segment increased by 20%, with growth across each of our customer markets, led by the Service Provider and Cloud customer market which was largely driven by revenue from our AI Infrastructure solutions.",
    "paragraph_id": "0000858877-26-000078:mdna:87",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_apjc_negative_productivity",
    "what_changed": "The APJC Q3 segment gross margin decrease is attributed to product mix, pricing and negative impacts from productivity. Productivity is a drag in this segment, where it is an offset in the Americas and EMEA paragraphs (mdna:163, mdna:164).",
    "account": "APJC segment gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in the APJC segment gross margin percentage was primarily due to product mix, pricing and negative impacts from productivity.",
    "paragraph_id": "0000858877-26-000078:mdna:165",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tariff_refund_not_recognized",
    "what_changed": "New 'U.S. Tariffs' section. After the February 20, 2026 Supreme Court ruling that IEEPA tariffs were unauthorized, the company may be eligible for refunds of tariffs paid. It has recorded no benefit and will not until amounts are realizable, and it believes any refund will not be material.",
    "account": "product cost of sales (unrecognized gain contingency)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As a result of this ruling, we may be eligible for a refund of tariffs previously paid on imported goods. As the recoverability and timing of any such refund remains uncertain, we have not recorded a benefit for any potential refund and will not until such amounts are realizable.",
    "paragraph_id": "0000858877-26-000078:mdna:151",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_effective_tax_rate_lower_fdii_deduction",
    "what_changed": "The Q3 effective tax rate increase is attributed to a decrease in the foreign-derived intangible income deduction, partly offset by higher research tax credits.",
    "account": "provision for income taxes; effective tax rate",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in the effective tax rate was primarily due to a decrease in foreign derived intangible income deduction partially offset by an increase in research tax credit benefit.",
    "paragraph_id": "0000858877-26-000078:mdna:220",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_commercial_paper_funding_and_escrow_release",
    "what_changed": "MD&A says the nine-month rise in cash and investments came from operating cash flow, $4.9 billion of net commercial paper issuance, and release of about $0.6 billion of restricted cash previously held in escrow. It was partly offset by dividends, buybacks, $1.8 billion of debt repayment, RSU tax withholding and capex. notes:77 describes restricted cash as primarily related to supplier contractual obligations, and notes:76 shows no restricted cash at April 25, 2026. mdna:273 states commercial paper outstanding of $8.4 billion and $3.5 billion at April 25, 2026 and July 26, 2025.",
    "account": "commercial paper (short-term debt); restricted cash",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The net increase in cash and cash equivalents and investments in the first nine months of fiscal 2026 was primarily driven by net cash provided by operating activities of $8.8 billion, $4.9 billion net issuance of commercial paper, and the release to us of approximately $0.6 billion of restricted cash previously held in escrow.",
    "paragraph_id": "0000858877-26-000078:mdna:230",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_interest_expense_lower_average_debt",
    "what_changed": "MD&A attributes lower interest expense in Q3 and the nine months to a lower average debt balance and a lower commercial paper rate against the fiscal 2025 periods. mdna:273 states commercial paper of $8.4 billion at April 25, 2026 and $3.5 billion at July 26, 2025, and mdna:26 lists total debt at both dates. These are period-end figures against year-end, while the prose compares averages year over year. The numbers reader should reconcile, and the stated commercial paper balance bears on interest expense in coming quarters.",
    "account": "interest expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in interest expense was driven by a lower average balance of debt outstanding and lower effective interest rate on commercial paper during the respective periods.",
    "paragraph_id": "0000858877-26-000078:mdna:212",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_executive_trading_plan",
    "what_changed": "New Item 5 disclosure. On February 18, 2026 the Chair and CEO adopted a Rule 10b5-1 trading plan to sell 494,027 gross shares plus related dividend-equivalent shares. It terminates March 27, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "provides for the sale of 494,027 gross shares",
    "paragraph_id": "0000858877-26-000078:notes:250",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_accounting_officer_trading_plan",
    "what_changed": "New Item 5 disclosure. On February 20, 2026 the Senior Vice President and Chief Accounting Officer adopted a Rule 10b5-1 trading plan to sell 21,150 gross shares plus dividend-equivalent and employee stock purchase plan shares. It terminates March 27, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "provides for the sale of 21,150 gross shares",
    "paragraph_id": "0000858877-26-000078:notes:251",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_operations_executive_trading_plan",
    "what_changed": "New Item 5 disclosure. On March 17, 2026 the Executive Vice President, Operations adopted a Rule 10b5-1 trading plan to sell 74,487 gross shares plus related dividend-equivalent shares. It terminates March 27, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "provides for the sale of 74,487 gross shares",
    "paragraph_id": "0000858877-26-000078:notes:252",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### Item 4 (controls)

- 0000858877-26-000078:item_4_controls:1: heading
- 0000858877-26-000078:item_4_controls:2: disclosure controls still concluded effective; no change in substance
- 0000858877-26-000078:item_4_controls:3: date rolled forward to the third quarter; no change in internal control reported

### MD&A

- 0000858877-26-000078:mdna:6: table; amounts only
- 0000858877-26-000078:mdna:10: heading
- 0000858877-26-000078:mdna:13: amounts only (segment revenue increases)
- 0000858877-26-000078:mdna:14: category growth rates; drivers covered by the mdna:87, mdna:114 and mdna:119 items
- 0000858877-26-000078:mdna:19: heading
- 0000858877-26-000078:mdna:20: nine-month overview; drivers repeat mdna:147, mdna:208 and mdna:222
- 0000858877-26-000078:mdna:25: intro; date rolled forward
- 0000858877-26-000078:mdna:26: table; amounts only
- 0000858877-26-000078:mdna:27: table; amounts only
- 0000858877-26-000078:mdna:44: heading
- 0000858877-26-000078:mdna:45: loss contingency policy boilerplate; no change in substance visible
- 0000858877-26-000078:mdna:46: IP claims boilerplate; no change in substance visible
- 0000858877-26-000078:mdna:50: no goodwill impairment; date rolled forward
- 0000858877-26-000078:mdna:59: effective tax rates; amounts only (driver itemized at mdna:220)
- 0000858877-26-000078:mdna:68: table; amounts only
- 0000858877-26-000078:mdna:71: table; amounts only
- 0000858877-26-000078:mdna:73: heading
- 0000858877-26-000078:mdna:74: amounts only; restates mdna:11
- 0000858877-26-000078:mdna:76: heading
- 0000858877-26-000078:mdna:77: amounts only
- 0000858877-26-000078:mdna:78: page number
- 0000858877-26-000078:mdna:83: table; amounts only
- 0000858877-26-000078:mdna:86: heading
- 0000858877-26-000078:mdna:88: heading
- 0000858877-26-000078:mdna:89: nine-month version of the mdna:87 driver; amounts only
- 0000858877-26-000078:mdna:91: heading
- 0000858877-26-000078:mdna:92: EMEA country growth; amounts only
- 0000858877-26-000078:mdna:93: heading
- 0000858877-26-000078:mdna:94: amounts only
- 0000858877-26-000078:mdna:96: heading
- 0000858877-26-000078:mdna:97: APJC country growth; amounts only
- 0000858877-26-000078:mdna:98: heading
- 0000858877-26-000078:mdna:99: amounts only
- 0000858877-26-000078:mdna:105: table; amounts only
- 0000858877-26-000078:mdna:108: heading
- 0000858877-26-000078:mdna:109: Networking drivers; covered by the mdna:87 AI infrastructure item
- 0000858877-26-000078:mdna:110: heading
- 0000858877-26-000078:mdna:111: nine-month Networking drivers; amounts only
- 0000858877-26-000078:mdna:113: heading
- 0000858877-26-000078:mdna:115: heading
- 0000858877-26-000078:mdna:116: nine-month Security drivers; covered by the mdna:114 Splunk item
- 0000858877-26-000078:mdna:118: heading
- 0000858877-26-000078:mdna:120: heading
- 0000858877-26-000078:mdna:121: nine-month Collaboration; amounts and repeated drivers
- 0000858877-26-000078:mdna:125: heading
- 0000858877-26-000078:mdna:126: Observability; Splunk decline covered by the mdna:114 item
- 0000858877-26-000078:mdna:127: heading
- 0000858877-26-000078:mdna:128: nine-month Observability; amounts only
- 0000858877-26-000078:mdna:131: table; amounts only
- 0000858877-26-000078:mdna:134: nine-month services flat; amounts only
- 0000858877-26-000078:mdna:137: table; amounts only
- 0000858877-26-000078:mdna:141: intro; date rolled forward
- 0000858877-26-000078:mdna:142: table; amounts only
- 0000858877-26-000078:mdna:143: insufficient; '(including memory)' may be new wording but the prior text is not visible; covered by the memory items
- 0000858877-26-000078:mdna:144: heading
- 0000858877-26-000078:mdna:146: heading
- 0000858877-26-000078:mdna:147: nine-month product margin; memory wording covered by the mdna:145 item
- 0000858877-26-000078:mdna:150: heading of the new tariff section; covered by the mdna:151 item
- 0000858877-26-000078:mdna:153: services margin; amounts and repeated driver (cost efficiencies)
- 0000858877-26-000078:mdna:159: table; amounts only
- 0000858877-26-000078:mdna:160: footnote on unallocated items; boilerplate
- 0000858877-26-000078:mdna:162: heading
- 0000858877-26-000078:mdna:163: Americas margin drivers; consistent with the consolidated drivers
- 0000858877-26-000078:mdna:164: EMEA margin drivers; repeated driver narrative
- 0000858877-26-000078:mdna:166: heading
- 0000858877-26-000078:mdna:172: table; amounts only
- 0000858877-26-000078:mdna:176: heading
- 0000858877-26-000078:mdna:177: R&D drivers; repeated driver narrative
- 0000858877-26-000078:mdna:178: heading
- 0000858877-26-000078:mdna:179: nine-month R&D drivers; repeated driver narrative
- 0000858877-26-000078:mdna:181: heading
- 0000858877-26-000078:mdna:182: sales and marketing drivers; repeated driver narrative
- 0000858877-26-000078:mdna:183: heading
- 0000858877-26-000078:mdna:184: nine-month sales and marketing drivers; repeated driver narrative
- 0000858877-26-000078:mdna:186: heading
- 0000858877-26-000078:mdna:187: G&A drivers; repeated driver narrative
- 0000858877-26-000078:mdna:188: heading
- 0000858877-26-000078:mdna:189: nine-month G&A drivers; repeated driver narrative
- 0000858877-26-000078:mdna:191: foreign-exchange effect on operating expenses; amounts only
- 0000858877-26-000078:mdna:192: foreign-exchange effect, nine months; amounts only
- 0000858877-26-000078:mdna:195: table; amounts only
- 0000858877-26-000078:mdna:196: amortization decline drivers; covered by the mdna:208 item
- 0000858877-26-000078:mdna:201: prior plan completion; amounts and date rolled forward
- 0000858877-26-000078:mdna:204: table; amounts only
- 0000858877-26-000078:mdna:205: heading
- 0000858877-26-000078:mdna:206: Q3 operating income; drivers duplicate mdna:12
- 0000858877-26-000078:mdna:207: heading
- 0000858877-26-000078:mdna:211: table; amounts only
- 0000858877-26-000078:mdna:216: table; amounts only
- 0000858877-26-000078:mdna:219: heading
- 0000858877-26-000078:mdna:221: heading
- 0000858877-26-000078:mdna:222: nine-month tax rate; prior-year benefit repeated
- 0000858877-26-000078:mdna:229: table; amounts only
- 0000858877-26-000078:mdna:232: securities lending, none outstanding; date rolled forward
- 0000858877-26-000078:mdna:235: table; amounts only
- 0000858877-26-000078:mdna:236: final transition tax payment statement; date rolled forward
- 0000858877-26-000078:mdna:238: page number
- 0000858877-26-000078:mdna:244: table; amounts only
- 0000858877-26-000078:mdna:245: dividend declaration; date rolled forward
- 0000858877-26-000078:mdna:246: remaining repurchase authorization; amounts only
- 0000858877-26-000078:mdna:248: table; amounts only
- 0000858877-26-000078:mdna:251: table; amounts only
- 0000858877-26-000078:mdna:255: table; amounts only
- 0000858877-26-000078:mdna:259: repeats the notes:182 memory sentence; covered by that item
- 0000858877-26-000078:mdna:262: table; amounts only
- 0000858877-26-000078:mdna:263: financing receivables; amounts only
- 0000858877-26-000078:mdna:264: page-split fragment; wording only
- 0000858877-26-000078:mdna:267: page-split continuation; wording only (true-sale text is cited in the receivables items)
- 0000858877-26-000078:mdna:268: duplicates the notes:194 and notes:196 amounts
- 0000858877-26-000078:mdna:271: table; amounts only
- 0000858877-26-000078:mdna:272: covenant compliance; date rolled forward
- 0000858877-26-000078:mdna:273: commercial paper outstanding; amounts only; cited in the mdna:230 and mdna:212 items
- 0000858877-26-000078:mdna:274: credit facility compliance; date rolled forward
- 0000858877-26-000078:mdna:278: table; amounts only
- 0000858877-26-000078:mdna:281: table; amounts only
- 0000858877-26-000078:mdna:287: duplicates notes:141 and notes:187
- 0000858877-26-000078:mdna:293: heading
- 0000858877-26-000078:mdna:294: investor channels boilerplate; wording only

### Notes

- 0000858877-26-000078:notes:2: date rolled forward
- 0000858877-26-000078:notes:3: date rolled forward
- 0000858877-26-000078:notes:7: split out of the prior combined paragraph; wording unchanged
- 0000858877-26-000078:notes:8: split out of the prior combined paragraph; wording unchanged
- 0000858877-26-000078:notes:9: prior version was split across a page break; wording unchanged
- 0000858877-26-000078:notes:17: table; amounts only
- 0000858877-26-000078:notes:26: table; amounts only
- 0000858877-26-000078:notes:30: receivables balance; amounts only; covered by the mdna:249 item
- 0000858877-26-000078:notes:32: table (receivables allowance rollforward); amounts only
- 0000858877-26-000078:notes:35: table; amounts only
- 0000858877-26-000078:notes:36: contract assets; amounts only
- 0000858877-26-000078:notes:37: deferred revenue recognized; amounts only
- 0000858877-26-000078:notes:38: capitalized contract costs; amounts only (prior version was page-split)
- 0000858877-26-000078:notes:43: table; amounts only
- 0000858877-26-000078:notes:44: date rolled forward
- 0000858877-26-000078:notes:46: acquisition transaction costs; amounts only
- 0000858877-26-000078:notes:48: date rolled forward
- 0000858877-26-000078:notes:49: date rolled forward
- 0000858877-26-000078:notes:53: table; amounts only
- 0000858877-26-000078:notes:54: future acquisition compensation estimate; amounts only (prior amount not visible)
- 0000858877-26-000078:notes:56: date rolled forward
- 0000858877-26-000078:notes:57: table; amounts only
- 0000858877-26-000078:notes:59: date rolled forward
- 0000858877-26-000078:notes:62: table; amounts only
- 0000858877-26-000078:notes:65: only the prior-year impairment is stated; date rolled forward
- 0000858877-26-000078:notes:67: table; amounts only
- 0000858877-26-000078:notes:68: date rolled forward
- 0000858877-26-000078:notes:69: table; amounts only
- 0000858877-26-000078:notes:71: fiscal 2025 plan; amounts and dates rolled forward
- 0000858877-26-000078:notes:73: table; amounts only
- 0000858877-26-000078:notes:76: table; amounts only
- 0000858877-26-000078:notes:77: restricted cash description; no change visible; release covered by the mdna:230 item
- 0000858877-26-000078:notes:79: table; amounts only
- 0000858877-26-000078:notes:81: table; amounts only
- 0000858877-26-000078:notes:83: table; amounts only
- 0000858877-26-000078:notes:86: table; amounts only
- 0000858877-26-000078:notes:87: heading
- 0000858877-26-000078:notes:88: intro
- 0000858877-26-000078:notes:89: table; amounts only
- 0000858877-26-000078:notes:90: intro
- 0000858877-26-000078:notes:91: table; amounts only
- 0000858877-26-000078:notes:92: intro
- 0000858877-26-000078:notes:93: table; amounts only
- 0000858877-26-000078:notes:94: lease term and discount rate; amounts only
- 0000858877-26-000078:notes:95: date rolled forward
- 0000858877-26-000078:notes:96: table; amounts only
- 0000858877-26-000078:notes:97: heading
- 0000858877-26-000078:notes:98: lessor interest income; amounts only
- 0000858877-26-000078:notes:99: date rolled forward
- 0000858877-26-000078:notes:100: table; amounts only
- 0000858877-26-000078:notes:101: boilerplate
- 0000858877-26-000078:notes:105: table; amounts only
- 0000858877-26-000078:notes:109: table; amounts only
- 0000858877-26-000078:notes:111: date rolled forward
- 0000858877-26-000078:notes:112: table; amounts only
- 0000858877-26-000078:notes:117: table; amounts only
- 0000858877-26-000078:notes:118: table; amounts only
- 0000858877-26-000078:notes:119: table; amounts only
- 0000858877-26-000078:notes:120: table; amounts only
- 0000858877-26-000078:notes:121: heading
- 0000858877-26-000078:notes:122: intro
- 0000858877-26-000078:notes:123: table; amounts only
- 0000858877-26-000078:notes:124: table; amounts only
- 0000858877-26-000078:notes:125: intro
- 0000858877-26-000078:notes:126: table; amounts only
- 0000858877-26-000078:notes:127: date rolled forward
- 0000858877-26-000078:notes:128: table; amounts only
- 0000858877-26-000078:notes:129: table; amounts only
- 0000858877-26-000078:notes:130: date rolled forward
- 0000858877-26-000078:notes:131: table; amounts only
- 0000858877-26-000078:notes:132: boilerplate
- 0000858877-26-000078:notes:133: heading
- 0000858877-26-000078:notes:134: marketable equity securities; amounts only
- 0000858877-26-000078:notes:135: renamed heading; covered by the notes:136 item
- 0000858877-26-000078:notes:137: new table; covered by the notes:136 item
- 0000858877-26-000078:notes:141: amounts and relabeling; follows the notes:136 item
- 0000858877-26-000078:notes:144: table; amounts only
- 0000858877-26-000078:notes:145: fair value hierarchy boilerplate; no change visible
- 0000858877-26-000078:notes:146: cross-reference relabeled; covered by the notes:136 item
- 0000858877-26-000078:notes:147: heading
- 0000858877-26-000078:notes:148: other fair value disclosures; amounts only
- 0000858877-26-000078:notes:149: heading
- 0000858877-26-000078:notes:150: intro
- 0000858877-26-000078:notes:151: table; amounts only
- 0000858877-26-000078:notes:152: commercial paper program description; no change visible
- 0000858877-26-000078:notes:153: boilerplate
- 0000858877-26-000078:notes:154: heading
- 0000858877-26-000078:notes:155: intro
- 0000858877-26-000078:notes:156: table; amounts only (February 2026 notes repaid; cited in the mdna:230 item)
- 0000858877-26-000078:notes:157: covenant compliance; date rolled forward
- 0000858877-26-000078:notes:158: date rolled forward
- 0000858877-26-000078:notes:159: table; amounts only
- 0000858877-26-000078:notes:160: heading
- 0000858877-26-000078:notes:161: credit facility compliance; date rolled forward
- 0000858877-26-000078:notes:165: table; amounts only
- 0000858877-26-000078:notes:167: table; amounts only
- 0000858877-26-000078:notes:169: table; amounts only
- 0000858877-26-000078:notes:180: heading
- 0000858877-26-000078:notes:181: split from the prior paragraph; wording unchanged
- 0000858877-26-000078:notes:183: intro
- 0000858877-26-000078:notes:184: table; amounts only (prose covered by the mdna:256 items)
- 0000858877-26-000078:notes:186: heading
- 0000858877-26-000078:notes:188: heading
- 0000858877-26-000078:notes:189: intro
- 0000858877-26-000078:notes:190: table; amounts only
- 0000858877-26-000078:notes:191: unchanged per note change history
- 0000858877-26-000078:notes:192: heading
- 0000858877-26-000078:notes:193: unchanged per note change history
- 0000858877-26-000078:notes:195: date rolled forward
- 0000858877-26-000078:notes:196: table; amounts only
- 0000858877-26-000078:notes:197: heading
- 0000858877-26-000078:notes:198: unchanged per note change history
- 0000858877-26-000078:notes:199: unchanged per note change history
- 0000858877-26-000078:notes:200: unchanged per note change history
- 0000858877-26-000078:notes:201: heading
- 0000858877-26-000078:notes:203: unchanged per note change history
- 0000858877-26-000078:notes:205: Ramot; unchanged per note change history
- 0000858877-26-000078:notes:206: unchanged per note change history
- 0000858877-26-000078:notes:207: unchanged per note change history
- 0000858877-26-000078:notes:208: policy block split; wording unchanged
- 0000858877-26-000078:notes:209: repeats the notes:182 memory sentence; covered by that item
- 0000858877-26-000078:notes:211: remaining repurchase authorization; amounts only
- 0000858877-26-000078:notes:212: table; amounts only
- 0000858877-26-000078:notes:213: pending repurchase settlements; amounts only
- 0000858877-26-000078:notes:216: dividend declaration; date rolled forward
- 0000858877-26-000078:notes:218: date rolled forward
- 0000858877-26-000078:notes:221: insufficient; vesting and retirement-eligible wording may be new but the prior text is not visible
- 0000858877-26-000078:notes:222: insufficient; plan term wording, prior text not visible
- 0000858877-26-000078:notes:223: shares authorized for grant; amounts only
- 0000858877-26-000078:notes:225: employee stock purchase plan; amounts only
- 0000858877-26-000078:notes:228: table; amounts only
- 0000858877-26-000078:notes:229: unrecognized compensation; amounts only
- 0000858877-26-000078:notes:232: table; amounts only
- 0000858877-26-000078:notes:233: date rolled forward
- 0000858877-26-000078:notes:234: table; amounts only
- 0000858877-26-000078:notes:235: table; amounts only
- 0000858877-26-000078:notes:237: table; amounts only
- 0000858877-26-000078:notes:238: unrecognized tax benefits; amounts only (prior amount not visible)
- 0000858877-26-000078:notes:242: segment allocation boilerplate
- 0000858877-26-000078:notes:244: table; amounts only
- 0000858877-26-000078:notes:245: U.S. revenue; amounts only
- 0000858877-26-000078:notes:249: table; amounts only

### 8-K (item codes only; no paragraph ids and no bodies in the input)

- 0000858877-26-000075 (2026-05-13; items 2.02, 2.05, 9.01): insufficient, code only with no body; the 2.05 code is cited in the notes:70 restructuring item
- 0000858877-26-000057 (2026-05-01; item 5.02): insufficient, code only with no body
- 0000858877-26-000048 (2026-04-06; item 5.02): insufficient, code only with no body
- Every earlier 8-K in the list is on or before 2026-02-11, before the prior 10-Q of 2026-02-17. These are codes only and outside this period's change.
