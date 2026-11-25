<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes-text reader — GNRC 10-Q 0001437749-26-025669 (quarter ended June 30, 2026)

Prior period of the same kind: 0001437749-26-014882 (Q1 2026 10-Q).

**What I read, all of it:** input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md (Item 4 only), input_8k.md (the Item 2.02 body of 0001437749-26-024731, filed 2026-07-29, plus the list of item codes), and input_prior_predictions.md (none on record).

**What my directory did not contain:**
- No Item 1A diff.
- No Exhibit 21 diff.
- No Exhibit 10 (nothing was pulled on trigger).
- No auditor's report. The controls file carries Item 4 only.

**Forbidden material:** none found. I saw no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window. The balance sheet, income statement and cash-flow tables in input_8k.md belong to the earnings-release exhibit (8-K body).

**No arithmetic:** I did none. Every direction below is what the prose says or implies. Wherever I give two amounts side by side, I am quoting them, not comparing them.

## Items

```json
[
  {
    "id": "estimates_and_discretion_tariff_refund_loss_recovery_model",
    "what_changed": "A new 'Tariff Refund' policy section has been added (change history: added). The U.S. Supreme Court invalidated IEEPA tariffs on February 20, 2026. The Company has elected to account for refunds under the ASC 410-30 loss recovery model. Under that model a recovery asset is recognized only when receipt is considered probable under ASC 450-20. The prior quarter had no such election. A probability judgment by management now decides when refund amounts reach the balance sheet, cost of goods sold and inventory.",
    "account": "prepaid expenses and other current assets (tariff refund receivable); cost of goods sold; inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The Company elected to account for the refund of tariffs under a loss recovery model pursuant to Accounting Standards Codification (ASC) 410-30.",
    "paragraph_id": "0001437749-26-025669:notes:9",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tariff_refund_receivable_deemed_probable",
    "what_changed": "The note now states a tariff refund receivable of approximately $27,700, recorded in prepaid expenses and other current assets because management has deemed receipt probable. It also states that refunds of approximately $61,400 were received in cash during the three and six months. MD&A (mdna:37) repeats both figures in rounded form ($28 million and $61 million). Management explains this receivable as an IEEPA refund not yet received and judged probable.",
    "account": "prepaid expenses and other current assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the Company recorded a tariff refund receivable within prepaid expenses and other current assets in the condensed consolidated balance sheets of approximately $27,700 for which the Company has deemed receipt probable to occur.",
    "paragraph_id": "0001437749-26-025669:notes:10",
    "explanation": true
  },
  {
    "id": "earnings_quality_tariff_refund_reduced_cost_of_goods_sold",
    "what_changed": "Approximately $71,100 of the tariff recovery was recorded as a reduction of cost of goods sold in Q2 2026. This is a recovery of tariffs paid in earlier periods, not a recurring cost reduction. MD&A says tariff refunds contributed approximately 6% to gross margin in the quarter (mdna:61) and approximately 3% for the six months (mdna:82). The release says the same about the quarter (8k:22).",
    "account": "cost of goods sold; gross profit",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Approximately $71,100 of the tariff recovery was recorded as a reduction of cost of goods sold in the condensed consolidated statements of comprehensive income",
    "paragraph_id": "0001437749-26-025669:notes:10",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tariff_refund_remainder_in_inventories",
    "what_changed": "The part of the tariff recovery not taken to cost of goods sold 'was recorded in inventories'. MD&A (mdna:37) says 'with the remainder reflected in inventory'. The prose implies a lower carrying cost for inventory on hand, which reaches cost of goods sold as that inventory is sold. The release puts the full-year 2026 effect of the tariff refund at approximately 1.5% (8k:36). Management is explaining part of the inventory balance.",
    "account": "inventories; cost of goods sold in later periods",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "and the remainder was recorded in inventories in the condensed consolidated balance sheets.",
    "paragraph_id": "0001437749-26-025669:notes:10",
    "explanation": true
  },
  {
    "id": "earnings_quality_tariff_refund_retained_in_adjusted_measures",
    "what_changed": "The release states that net income, adjusted net income and adjusted EBITDA all include about $71 million pre-tax of tariff refunds. None of the reconciliations has a tariff line, so the refund is not added back: not the Adjusted EBITDA reconciliation (mdna:147, 8k:116) and not the adjusted net income reconciliation (mdna:168, 8k:119). The segment explanations put the tariff effect at about 2% of C&I adjusted EBITDA margin (mdna:66) and about 9% of Residential margin (mdna:67). The non-GAAP measures therefore carry a recovery of prior-period cost.",
    "account": "adjusted EBITDA; adjusted net income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net income, adjusted net income, and adjusted EBITDA all include a pre-tax impact of approximately $71 million related to tariff refunds that were recorded during the current year quarter.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:14",
    "explanation": false
  },
  {
    "id": "earnings_quality_residential_adjusted_ebitda_tariff_concentration",
    "what_changed": "MD&A says the Q2 increase in Residential segment adjusted EBITDA was primarily driven by tariff refunds, which impacted margins by approximately 9%, together with favorable mix and operational efficiencies. For the six months the figure is approximately 5% (mdna:88). For C&I, tariff refunds are put at approximately 2% (mdna:66). The prose implies that this quarter's Residential margin includes a benefit the company ties to refunds of tariffs previously paid. That benefit would not recur unless refunds recur.",
    "account": "Residential segment adjusted EBITDA",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "This increase was primarily driven by tariff refunds which impacted margins by approximately 9%, as well as favorable sales mix and operational efficiencies resulting in lower operating expenses.",
    "paragraph_id": "0001437749-26-025669:mdna:67",
    "explanation": false
  },
  {
    "id": "results_against_expectations_margin_guidance_raised_on_tariff_refund",
    "what_changed": "Full-year 2026 guidance was raised in two places. Net income margin is now about 9.0 to 10.0% (previous guidance 8.0 to 9.0%). Adjusted EBITDA margin is now about 20.0 to 21.0% (previous 18.5 to 19.5%). The release says the raise is primarily due to the Q2 tariff refund, put at about 1.5% for the full year. It does not attribute the raise to operations. The total sales growth guidance was not changed (8k:19, 8k:35).",
    "account": "net income margin; adjusted EBITDA margin",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "This increased outlook is primarily due to the tariff refund included in the second quarter, which is expected to have an approximate 1.5% impact for the full year 2026.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:36",
    "explanation": false
  },
  {
    "id": "results_against_expectations_sales_guidance_maintained_segment_outlook_revised",
    "what_changed": "The release keeps 2026 total net sales growth at the mid-to-high teens percent, including about 2% favorable from FX, acquisitions and divestitures. It now expects C&I growth in the low 30% range and Residential growth in the high-single digits. The word 'now' marks both segment figures as revised, but the earlier segment guidance is not in my input. The 10-Q MD&A says first-half Residential total sales decreased approximately 1% (mdna:80) and Q2 Residential sales decreased approximately 2% (mdna:59). Setting the full-year Residential projection against those statements is for the numbers reader.",
    "account": "net sales (C&I and Residential)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "C&I segment sales are now expected to grow in the low 30% range during the year as a result of continued significant momentum in the data center market, and Residential segment sales are now projected to increase in the high-single digit range from the prior year.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:35",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_tariff_receipts_and_cash_taxes",
    "what_changed": "MD&A now gives three causes for the six-month rise in operating cash flow: higher operating earnings, $61 million of tariff refund receipts, and lower cash tax payments. MD&A (mdna:45) says the OBBBA bonus depreciation and R&D expensing are expected to keep producing cash tax savings. The release (8k:25) says the Q2 rise in free cash flow came from higher operating earnings, including tariff refund receipts. Part of the operating cash flow is therefore described as a one-time recovery.",
    "account": "net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in operating cash flows for the six months ended June 30, 2026 was driven by higher operating earnings, cash receipts from tariff refunds totaling $61 million, and lower cash tax payments in the current year period.",
    "paragraph_id": "0001437749-26-025669:mdna:109",
    "explanation": false
  },
  {
    "id": "across_documents_operating_cash_flow_working_capital_omits_settlement_payment",
    "what_changed": "MD&A names the offset to operating cash flow only as 'a greater use of cash for working capital'. It does not name the Zawaski product-liability settlement. Note 16 says the Company and its insurance carriers satisfied that payment on April 1, 2026, with the Company agreeing to pay $104,500 (notes:155). The other-accrued-liabilities footnote (notes:100) names that payment as the main reason accrued legal and professional fees decreased. The Zawaski paragraph in Note 16 is unchanged from Q1 and still describes the reserve and the $102,000 insurance receivable 'as of March 31, 2026 and December 31, 2025'. The supervisor should reconcile this to the cash-flow line for other accrued liabilities.",
    "account": "net cash provided by operating activities; other accrued liabilities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "These items were partially offset by a greater use of cash for working capital as compared to the prior year period.",
    "paragraph_id": "0001437749-26-025669:mdna:109",
    "explanation": false
  },
  {
    "id": "revenue_recognition_cost_to_cost_unbilled_contract_assets",
    "what_changed": "Note 11 has been retitled 'Contract Balances' (it was 'Contract Liabilities'). It newly discloses contract assets: unbilled receivables on contracts accounted for under the cost-to-cost method, where revenue recognized on costs incurred exceeds billings. These sit in prepaid expenses and other current assets, outside trade receivables. The stated balances are $78,730 at June 30, 2026 and $8,867 at December 31, 2025. The C&I segment description (notes:73) says revenue is recognized over time where the performance obligation is satisfied over time. Revenue under this method depends on estimates of total contract cost. MD&A attributes core C&I growth to ramping data center revenue (mdna:58). Management is explaining what drives the unbilled receivable balance.",
    "account": "prepaid expenses and other current assets (contract assets); net sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Contract assets primarily consist of unbilled receivables associated with contracts accounted for under the cost-to-cost method of revenue recognition, where revenue recognized based on costs incurred exceeds amounts billed to customers.",
    "paragraph_id": "0001437749-26-025669:notes:117",
    "explanation": true
  },
  {
    "id": "revenue_recognition_contract_liabilities_net_of_revenue_recognized",
    "what_changed": "Contract liabilities are now defined as 'customer deposits that exceed revenue recognized'. This replaces the Q1 wording, 'customer deposits and other contract liabilities' arising from advance payment. The stated balance is $117,918 at June 30, 2026 against $151,257 at December 31, 2025. In the six months, $90,360 of revenue was recognized from the December 31, 2025 balance. The new wording implies that on each contract, deposits are reduced by the revenue recognized against them. The balance therefore depends on cost-to-cost progress estimates as well as on cash received. The note gives no direction.",
    "account": "other accrued liabilities (current contract liabilities); deferred revenue",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Contract liabilities primarily consist of customer deposits that exceed revenue recognized.",
    "paragraph_id": "0001437749-26-025669:notes:118",
    "explanation": false
  },
  {
    "id": "revenue_recognition_remaining_performance_obligations_restated",
    "what_changed": "Remaining performance obligations, excluding extended warranty, are now stated at approximately $143,000 (thousands), with approximately 80% expected to be recognized within two years. The removed Q1 text (note_history:41) stated approximately $272,000 and approximately 90%. The practical expedient still excludes contracts with an original term of one year or less. The note does not explain the figure.",
    "account": "remaining performance obligations; net sales",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the aggregate amount of revenue that the Company expects to recognize on remaining performance obligations (excluding extended warranty) was approximately $143,000, of which approximately 80% is expected to be recognized as revenue over the next two years.",
    "paragraph_id": "0001437749-26-025669:notes:119",
    "explanation": false
  },
  {
    "id": "revenue_recognition_standard_payment_terms_statement_removed",
    "what_changed": "A Q1 paragraph has been removed. It said that standard customer payment terms are less than one year, that terms vary by contract, and that some customers prepay while others get open credit with payment in arrears after shipment. The contract-balances framework replaces it. The current filing no longer states the one-year ceiling on standard payment terms, in the same quarter that it introduces unbilled contract assets.",
    "account": "accounts receivable; contract assets",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "While the Company’s standard payment terms for its customers are less than one year, the specific payment terms and conditions in its customer contracts vary.",
    "paragraph_id": "0001437749-26-014882:note_history:40",
    "explanation": false
  },
  {
    "id": "across_documents_data_center_backlog_versus_remaining_performance_obligations",
    "what_changed": "The release says data center backlog has 'now increased to approximately $1.6 billion as of today'. It says about $1 billion of additional orders have come in since the prior update, and that the figure excludes the second hyperscale customer. The headline says the backlog 'provides visibility to significant 2027 growth'. None of the 10-Q text carried to me mentions backlog. Note 11 states remaining performance obligations of approximately $143,000 (thousands), excluding contracts of one year or less (notes:119). The MD&A risk list names cancellation rights in certain data center contracts (mdna:8). The two measures differ in scope. Reconciling backlog to RPO is for the supervisor.",
    "account": "net sales; remaining performance obligations",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In total, our backlog for products serving the data center market has now increased to approximately $1.6 billion as of today, which does not include any committed volumes from the second hyperscale customer.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:20",
    "explanation": false
  },
  {
    "id": "results_against_expectations_first_hyperscale_committed_volume",
    "what_changed": "The release says the product-specific terms of the global supply agreement with a leading hyperscale data center operator were recently finalized, committing nearly $700 million of volume for 2027. It describes the agreement as previously disclosed during the quarter. The item-code list shows no Item 1.01 or 8.01 filing in Q2 2026: the 2026-04-29 filing carried 2.02, 7.01 and 9.01, and the 2026-06-12 filing carried 5.07. No Exhibit 10 is in my input, and the 10-Q text carried to me does not mention the agreement.",
    "account": "net sales (C&I)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In addition, product specific terms related to this agreement were recently finalized, which committed nearly $700 million of volume for 2027.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "results_against_expectations_second_hyperscale_supply_agreement",
    "what_changed": "New: on June 24 the Company secured a global supply agreement with a second hyperscale customer and is negotiating final product-specific terms for 2027 and 2028 volumes. No committed volume is stated, and the release says the backlog figure excludes this customer. The 10-Q text carried to me does not mention it.",
    "account": "net sales (C&I)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "On June 24th, the Company secured a global supply agreement with a second hyperscale customer and is currently negotiating final product specific terms for 2027 and 2028 volumes.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_data_center_capacity_investment",
    "what_changed": "The CEO says the Company is 'investing aggressively' in production and packaging capacity for large megawatt generators and plans further capacity as the pipeline materializes. The release also reports the purchase of a facility in Belvidere, Illinois (8k:18). Segment capital expenditures appear in notes:90 as amounts only. The prose implies higher capital spending ahead.",
    "account": "expenditures for property and equipment; property and equipment, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "To address this accelerating demand, we are investing aggressively in incremental production and packaging capacity for large megawatt generators and are planning to add further capacity as our pipeline of opportunities materializes.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:20",
    "explanation": false
  },
  {
    "id": "across_documents_belvidere_facility_in_release_only",
    "what_changed": "The release says the Company acquired an additional facility in Belvidere, Illinois during the quarter to expand large megawatt generator packaging capacity. None of the 10-Q text carried to me mentions Belvidere. The notes list Allmand, Enercon and Wolter as completed acquisitions and New Way as pending. Nothing states whether Belvidere was an asset purchase recorded in property and equipment.",
    "account": "property and equipment, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "and acquired an additional facility in Belvidere, Illinois, significantly expanding capacity for large megawatt generator packaging.",
    "paragraph_id": "0001437749-26-024731:8k_2_02:18",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_enercon_acquisition_completed",
    "what_changed": "Enercon was a subsequent event in the Q1 10-Q, acquired April 1, 2026. The Q1 text gave a preliminary price of $122,322, of which $44,785 was in restricted shares, and an earnout of up to $112,043 (note_history:43). Enercon now appears as a completed Q2 acquisition in the Business Combinations note and in the Note 1 list (notes:4), inside the C&I segment. The Q1 Subsequent Events note has been dropped. The Q1 text said Enercon strengthens service to hyperscale and enterprise data center markets.",
    "account": "goodwill; intangible assets; net sales (C&I)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the Company acquired Enercon, headquartered in East Peoria, Illinois.",
    "paragraph_id": "0001437749-26-025669:notes:19",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_wolter_asset_acquisition",
    "what_changed": "New: in May 2026 the Company acquired substantially all of the assets and liabilities of Wolter Power Systems (Brookfield, Wisconsin), which is included in C&I. Wolter is an industrial and residential generator distributor that also provides maintenance and repair services. The note does not say whether Wolter previously distributed Generac products. If it did, sales to it would now be internal.",
    "account": "goodwill; net sales (C&I)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the Company acquired substantially all of the assets and liabilities of the Wolter Power Systems business, headquartered in Brookfield, Wisconsin.",
    "paragraph_id": "0001437749-26-025669:notes:20",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_new_way_pending_acquisition",
    "what_changed": "New commitment: in June 2026 the Company signed an agreement to buy the assets and assume the liabilities of New Way Power Proprietary Limited (Johannesburg, South Africa), a supplier of back-up power solutions. Closing is expected in Q4 2026. No price is stated.",
    "account": "goodwill; cash",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the Company signed an agreement to purchase the assets and assume the liabilities of New Way Power Proprietary Limited (New Way), a supplier of back-up power solutions, located in Johannesburg, South Africa.",
    "paragraph_id": "0001437749-26-025669:notes:21",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_preliminary_purchase_price_allocation_open",
    "what_changed": "The combined preliminary purchase price for the 2026 closed acquisitions is stated as $348,482, net of cash and including holdbacks and estimated contingent consideration. Of this, $44,785 was funded with treasury stock. The allocation rests on management's fair-value estimates. Allmand is to be finalized before March 31, 2027, and Enercon and Wolter before June 30, 2027. The allocation table (notes:26) assigns $208,598 to goodwill and $88,900 to intangible assets. Adjustments during the measurement period could change goodwill, intangible assets and future amortization.",
    "account": "goodwill; intangible assets; amortization of intangibles",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company recorded its preliminary purchase price allocation based on its estimates of the fair value of the acquired assets and assumed liabilities.",
    "paragraph_id": "0001437749-26-025669:notes:22",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_acquisition_pro_forma_not_presented",
    "what_changed": "The notes say the results of Allmand, Enercon and Wolter are included from their acquisition dates. Pro forma information is omitted because the effects are deemed not material. MD&A states the net contribution of non-annualized acquisitions and divestitures as $16.6 million for Q2 (mdna:60) and $34.6 million for the first half (mdna:81), mainly in C&I. The release says acquisitions, divestitures and FX added about 6% to Q2 C&I growth (8k:28). Because of the materiality judgment, the notes do not show C&I growth on a like-for-like basis.",
    "account": "net sales (C&I)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Pro forma and other financial information are not presented as the effects of these acquisitions are not material",
    "paragraph_id": "0001437749-26-025669:notes:23",
    "explanation": false
  },
  {
    "id": "earnings_quality_business_disposition_losses_added_back",
    "what_changed": "New: on June 1, 2026 the Company completed two immaterial dispositions, one in C&I and one in Residential, with a combined loss of $13,392. MD&A and the reconciliation footnotes now describe four immaterial dispositions in 2026, two closing in Q1 and two in Q2 (mdna:158, mdna:171, notes:86, 8k:129). The losses are added back in Adjusted EBITDA ('Other') and in adjusted net income. The goodwill rollforward shows a C&I 'Disposition of businesses' line of (15,943) (notes:105). The disposed businesses are not named.",
    "account": "loss attributable to business dispositions (other expense); goodwill",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the Company completed one immaterial business disposition within the Commercial & Industrial segment and one immaterial business disposition within the Residential segment, resulting in a combined loss of $13,392.",
    "paragraph_id": "0001437749-26-025669:notes:28",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_enercon_earnout_fair_value",
    "what_changed": "The contingent consideration liability now includes Enercon: notes:61 records $91,551 as 'Additional contingent consideration' for Enercon. The Enercon earnout runs through April 1, 2027 and is earned on specified target EBITDA levels. 35% is payable in restricted shares and the remainder in cash. Pramac's earnout period ended December 31, 2025. Remeasurements of this estimate go through earnings. The Adjusted EBITDA definition treats contingent consideration adjustments as non-cash items to be added back.",
    "account": "other accrued liabilities (accrued contingent consideration); operating lease and other long-term liabilities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "and is earned based on the achievement of specified target EBITDA levels during the earnout period, with 35% payable in restricted shares and the remainder in cash.",
    "paragraph_id": "0001437749-26-025669:notes:58",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_current_contingent_consideration_obligation",
    "what_changed": "The current portion of contingent consideration, $105,858, is now reported in other accrued liabilities, which makes it payable within twelve months. The non-current portion is $16,008. The next two Ageto increments can be earned on August 1, 2026 and August 1, 2027. The Enercon earnout ends April 1, 2027, with the part not paid in shares paid in cash. Settlement means cash outflows and further issuance of treasury shares.",
    "account": "other accrued liabilities; cash; treasury stock",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The current portion of contingent consideration totals $105,858 and is reported in other accrued liabilities",
    "paragraph_id": "0001437749-26-025669:notes:58",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_chilicon_earnout_paid_in_shares",
    "what_changed": "A new footnote says $3,917 of Chilicon contingent consideration was paid in shares in 2026 and is shown as a non-cash item in the cash flow statement. The treasury stock note says shares are periodically reissued from treasury for acquisition contingent consideration payments (notes:139).",
    "account": "accrued contingent consideration; treasury stock",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Represents payment of $3,917 in shares for the Chilicon acquisition.",
    "paragraph_id": "0001437749-26-025669:notes:62",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_fx_translation_mexican_peso",
    "what_changed": "The AOCI footnote attributes the Q2 2026 foreign-currency translation effect to a weaker U.S. dollar, 'particularly the Mexican Peso'. The six-month 2026 effect is described as unfavorable, from a stronger dollar, particularly the Euro and British Pound. The comparative-period footnotes name the Euro and British Pound.",
    "account": "accumulated other comprehensive income (loss)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Represents a favorable impact from the weakening of the U.S. dollar against foreign currencies during the three months ended June 30, 2026, particularly the Mexican Peso.",
    "paragraph_id": "0001437749-26-025669:notes:69",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_zawaski_settlement_paid",
    "what_changed": "A new footnote to the other-accrued-liabilities table says the decrease in accrued legal and professional fees primarily relates to a $206,500 payment by the Company and its insurers on the Zawaski product-liability settlement. The Zawaski paragraph in Note 16 (notes:155) is unchanged from Q1. It still states the $206,500 reserve and the $102,000 insurance receivable 'as of March 31, 2026 and December 31, 2025', and says the obligation was satisfied on April 1, 2026. The prose implies that both the reserve and the insurance receivable were relieved in Q2. Management is explaining a reserve balance.",
    "account": "other accrued liabilities (accrued legal and professional fees); prepaid expenses and other assets (insurance receivable)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease primarily relates to a $206,500 payment made by the Company and its insurance carriers to satisfy a legal obligation.",
    "paragraph_id": "0001437749-26-025669:notes:100",
    "explanation": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_ollnova_reserve_reduced_to_settlement",
    "what_changed": "In Ollnova v. ecobee, the Federal Circuit vacated the $11,500 judgment on June 4, 2026 and ordered a new trial, which was set for July 10, 2026. The parties then settled confidentially without admission. In Q2 2026 the Company reduced the reserve to the settlement amount. The reserve was $12,669 in 2023, plus $1,826 for interest in Q1 2024 and ongoing post-judgment interest. The settlement amount is not disclosed. The legal-matters reconciliation shows the patent-lawsuit line for Q2 as (3,485) (mdna:156, notes:85), so this credit is excluded from adjusted results. Management is explaining a change in a reserve.",
    "account": "other accrued liabilities (legal reserve); general and administrative expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In the second quarter of 2026, the Company reduced the reserve established for the original verdict and interest to the amount of the settlement.",
    "paragraph_id": "0001437749-26-025669:notes:154",
    "explanation": true
  },
  {
    "id": "across_documents_lower_legal_expense_and_patent_reserve_reduction",
    "what_changed": "MD&A and the release (8k:23) attribute part of the operating-expense change to 'lower legal expenses in the current year'. The other causes named are investment for C&I growth and higher intangible amortization. Neither document says that the lower legal expense includes the Ollnova reserve reduction recorded in Q2 (notes:154). The legal-matters reconciliation shows the patent-lawsuit line as (3,485) for the quarter. The supervisor should work out how much of the lower G&A comes from reversing a reserve rather than from lower spending.",
    "account": "general and administrative expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The increase was primarily driven by increased operating expense investments to support future C&I growth and higher intangible amortization, partially offset by lower legal expenses in the current year.",
    "paragraph_id": "0001437749-26-025669:mdna:62",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_oakland_county_appeal_filed",
    "what_changed": "In Q1 the text said plaintiffs 'may appeal' the April 30, 2026 dismissal with prejudice. It now says they have appealed, and the Company will defend the judgment. The Oakland County securities class action therefore stays open. Class-action legal costs are among the Adjusted EBITDA add-backs.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Plaintiffs have appealed the judgment of dismissal, and the Company intends to vigorously defend the judgment.",
    "paragraph_id": "0001437749-26-025669:notes:151",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_epa_additional_information_request",
    "what_changed": "The note adds that the EPA sent the Company a request for additional information on May 12, 2026. The request belongs to the DOJ/EPA/CARB portable-generator emissions matter. That matter covers approximately 1,850 units, plus approximately 4,850 units whose 2020 certifications the EPA would seek to void. No accrual or range is stated.",
    "account": "none (potential legal reserve)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "responding to other ancillary requests for information, including a request for additional information the Company received from the EPA on",
    "paragraph_id": "0001437749-26-025669:notes:153",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_walling_matters_dropped",
    "what_changed": "Two matters have been removed from Note 16. One is the Walling securities class action, whose dismissal became final without appeal. The other is the related derivative action of February 14, 2024, which was voluntarily dismissed (note_history:7). Both were already described as concluded in Q1. The open securities and derivative matters are now Oakland County (on appeal) and the derivative actions dating from February 3, 2023.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Plaintiff did not appeal the dismissal, so it is final.",
    "paragraph_id": "0001437749-26-014882:note_history:6",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_no_share_repurchases_first_half",
    "what_changed": "The note and MD&A (mdna:98, mdna:99) say no shares were repurchased in Q2 or in the first six months of 2026. The full $500 million February 2026 authorization was unused at June 30, 2026. In the prior year, repurchases in Q2 and the first half are stated as $50,463 and $147,917. MD&A states $211.8 million of cash for acquisitions in the half (mdna:110). No reason is given for the absence of buybacks.",
    "account": "treasury stock; cash",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "there were no share repurchases under the program.",
    "paragraph_id": "0001437749-26-025669:notes:139",
    "explanation": false
  },
  {
    "id": "earnings_quality_effective_tax_rate_prior_year_disposition_discrete_item",
    "what_changed": "The 10-Q explains the higher 2026 effective tax rate as the result of a non-recurring favorable discrete item in the prior-year period 'related to a business disposition'. The rate is 24.6% for the six months (prior year 20.0%) and 24.6% for Q2 (prior year 17.2%, mdna:64). The release (8k:24) gives the same cause without mentioning the disposition. The prose implies that the 2026 rate is the normal rate and that the prior-year rate was lowered by a one-time item.",
    "account": "provision for income taxes",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in effective tax rate was primarily related to a non-recurring favorable discrete item in the prior year period related to a business disposition that did not repeat in the current year period.",
    "paragraph_id": "0001437749-26-025669:notes:146",
    "explanation": false
  },
  {
    "id": "earnings_quality_wallbox_fair_value_gain_in_other_expense",
    "what_changed": "MD&A attributes lower Q2 other expense mainly to a fair-value gain on the Wallbox warrants and equity securities, plus lower interest expense and higher investment income. Losses on two dispositions partly offset these. The notes (notes:44, notes:55) state Q2 gains on the Wallbox warrants and shares. These mark-to-market gains are in GAAP net income and are removed from the adjusted measures.",
    "account": "change in fair value of investments (other expense, net)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The reduction in other expense, net was driven primarily by a gain in the fair value of our investment in warrants and equity securities of Wallbox N.V as well as lower interest expense and higher investment income in the current year quarter",
    "paragraph_id": "0001437749-26-025669:mdna:63",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_domestic_industrial_distributor_channel",
    "what_changed": "MD&A and the release (8k:28) say lower shipments to the domestic industrial distributor channel more than offset higher Q2 shipments to rental and telecom customers. The six-month text (mdna:79) also names lower sales to domestic industrial distributor customers. Core C&I growth is attributed to data center revenue. The traditional distributor channel is described as declining.",
    "account": "net sales (C&I, domestic industrial distributor channel)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In addition, increased shipments to rental and telecom channel customers were more than offset by a decrease in shipments to the domestic industrial distributor channel.",
    "paragraph_id": "0001437749-26-025669:mdna:58",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_residential_storage_and_portable_shipments",
    "what_changed": "MD&A says Q2 Residential total sales decreased approximately 2% because of lower shipments of energy storage systems and portable generators, mostly offset by growth in home standby. The six-month text (mdna:80) attributes the first-half decline to energy storage and says portable generator shipments were higher for the half. This ties to the OBBBA statement in mdna:28.",
    "account": "net sales (Residential)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "This modest sales decrease was primarily driven by lower energy storage system and portable generator shipments compared to the prior year, mostly offset by growth in home standby generator sales.",
    "paragraph_id": "0001437749-26-025669:mdna:59",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_mix_and_input_costs_beneath_tariff_benefit",
    "what_changed": "Apart from the tariff-refund contribution, MD&A says unfavorable sales mix and higher input costs were partially offset by favorable price realization in Q2. The six-month text (mdna:82) says mix and input costs 'more than offset' favorable price realization. The release says the same (8k:22). The prose implies pressure on gross margin once tariff refunds are excluded.",
    "account": "gross profit margin",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Additionally, unfavorable sales mix and higher input costs were partially offset by favorable price realization.",
    "paragraph_id": "0001437749-26-025669:mdna:61",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_obbba_residential_solar_storage",
    "what_changed": "The MD&A paragraph on the residential investment cycle is carried as changed. It now says OBBBA (July 2025) accelerated the phase-out of certain investment tax credits, 'resulting in a negative impact to the residential solar & storage market thereafter'. My input does not show the prior wording. The statement presents the impact as having already happened. It matches the lower energy storage shipments cited in mdna:59 and mdna:80.",
    "account": "net sales (Residential energy storage)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The OBBBA that was enacted in the United States in July 2025 accelerated the phase out of certain investment tax credits, resulting in a negative impact to the residential solar & storage market thereafter.",
    "paragraph_id": "0001437749-26-025669:mdna:28",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_data_center_contract_risk_terms",
    "what_changed": "The MD&A list of forward-looking factors is carried as changed text. It names contract risk with certain data center customers: cancellation rights, delivery requirements, and liability exposure tied to performance obligations. It also lists uncertainty about data center market growth, forecasting and inventory management, and possible withdrawal or reduction of grants already awarded to the Company. The release carries the same bullets (8k:52, 8k:57 to 8k:60). My input does not show which bullets are new, and no Item 1A diff is in my directory. Cancellation rights bear on how much of the stated data center backlog is enforceable.",
    "account": "net sales; remaining performance obligations; contingent liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "increase in contract risk related to terms with certain data center customers, including cancellation rights, delivery requirements, and potential liability exposure tied to our performance obligations or other claimed damages;",
    "paragraph_id": "0001437749-26-025669:mdna:8",
    "explanation": false
  },
  {
    "id": "across_documents_legal_add_back_definition_wording",
    "what_changed": "The 10-Q's Adjusted EBITDA definition (mdna:121) says the legal and regulatory add-back covers matters 'not part of the ordinary routine litigation', 'including but not limited to' class actions, government inquiries and certain IP litigation. The release definition (8k:88) and the 10-Q's own limitations bullet (mdna:135) speak instead of 'significant' matters, and list large suits and settlements among them. The documents describe the scope of the add-back in different words. The prior text of mdna:121 is not in my input.",
    "account": "adjusted EBITDA (provision for legal, regulatory and other costs)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "including but not limited to class action lawsuits, government inquiries, and certain intellectual property litigation.",
    "paragraph_id": "0001437749-26-025669:mdna:121",
    "explanation": false
  },
  {
    "id": "across_documents_contractual_obligations_unchanged_statement",
    "what_changed": "MD&A says contractual obligations have not changed materially since the 10-K, apart from borrowings and interest rates. Over the same period the notes record new items: Enercon contingent consideration with a current portion in other accrued liabilities (notes:58) and a signed agreement to acquire New Way (notes:21). The release describes aggressive capacity investment and the Belvidere facility purchase (8k:18, 8k:20). The supervisor should judge whether the statement is complete.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "There have been no material changes to our contractual obligations between the February 18, 2026, filing of our Annual Report on Form 10-K for the year ended December 31, 2025, and June 30, 2026, except for the changes in outstanding borrowings and interest rates",
    "paragraph_id": "0001437749-26-025669:mdna:115",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_no_icfr_change_amid_new_accounting",
    "what_changed": "Item 4 again reports effective disclosure controls and no change in ICFR during Q2. In the same quarter the notes introduce a tariff refund loss-recovery election that rests on a probability judgment, newly disclose cost-to-cost contract assets, and record the closing of the Enercon and Wolter acquisitions and two dispositions. No auditor's report or review report is in my input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "There have been no changes during the three months ended June 30, 2026 in our internal control over financial reporting",
    "paragraph_id": "0001437749-26-025669:item_4_controls:5",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_critical_estimates_list_unchanged_scope",
    "what_changed": "The critical-accounting-estimates paragraph is carried as changed. It names only goodwill and indefinite-lived intangible impairment and income taxes as most critical, with routine estimates for receivables, inventories, PP&E, prepaid expenses, warranties and other reserves. It does not name three judgments introduced in this filing's notes: the probability of tariff refund receipt, cost-to-cost revenue estimates, and the fair value of acquisitions and earnouts. The prior text is not in my input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Management believes our most critical accounting estimates and assumptions are in the following areas: goodwill and other indefinite-lived intangible asset impairment assessment; and income taxes.",
    "paragraph_id": "0001437749-26-025669:mdna:117",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_officer_trading_plan_adopted",
    "what_changed": "New: on May 5, 2026 Kyle Raabe, EVP and President, Home Power Generation, adopted a Rule 10b5-1 plan. It covers the sale of up to 1,939 shares and the exercise and sale of up to 1,063 options through December 31, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Kyle Raabe, Executive Vice President & President, Home Power Generation, adopted a Rule 10b5-1 trading plan",
    "paragraph_id": "0001437749-26-025669:notes:160",
    "explanation": false
  }
]
```

## Paragraphs read and not made an item

Every paragraph carried as text, one line each. Lines tagged **insufficient** are paragraphs the input marks as changed where the prior text is not in my input and I could not identify any change in substance.

### Notes (0001437749-26-025669:notes:*)
- `notes:4` — The same acquisitions are items at notes:19 and notes:20. The Allmand description adds "rental": wording only.
- `notes:5` — Basis of presentation: dates rolled forward.
- `notes:8` — "Tariff Refund" heading. The substance is in the items at notes:9 and notes:10.
- `notes:12` — Wording only: the "(ASC)" abbreviation was dropped because it is now defined in notes:9.
- `notes:13` — **insufficient**: the ASU 2025-06 disclosure is not in the change history and no change is identifiable.
- `notes:14` — **insufficient**: the ASU 2024-03 disclosure is not in the change history and no change is identifiable.
- `notes:15` — Date rolled forward (six months).
- `notes:17` — Heading.
- `notes:18` — Allmand (January 2026) was disclosed in Q1. The description wording now adds the rental market.
- `notes:24` — Heading.
- `notes:25` — Standing lead-in to the table.
- `notes:26` — Amounts only: the purchase price allocation table, cited in the notes:22 item.
- `notes:32` — **insufficient**: standing description of the Juffali JV and redeemable NCI policy. Prior text not shown.
- `notes:34` — Amounts only: redeemable NCI rollforward.
- `notes:40` — Swap description: date rolled forward.
- `notes:41` — Amounts only: AOCI swap losses.
- `notes:43` — Standing Wallbox description. No new warrant receipt is stated for 2026.
- `notes:44` — Amounts only: warrant gains, cited in the Wallbox item.
- `notes:47` — Amounts only: fair value table.
- `notes:48` — Amounts only, date rolled forward.
- `notes:51` — Amounts only: term loan fair values, date rolled forward.
- `notes:55` — Amounts only: Wallbox share fair value and gains, cited in the Wallbox item.
- `notes:60` — Amounts only: contingent consideration rollforward, cited in the Enercon items.
- `notes:61` — The amount is used in the Enercon earnout item.
- `notes:64` — Table lead-in: date rolled forward.
- `notes:65` — Amounts only: AOCI table.
- `notes:66` — Amounts only: AOCI table.
- `notes:67` — Amounts only: AOCI table.
- `notes:68` — Amounts only: AOCI table.
- `notes:71` — **insufficient**: the segment reorganization was already disclosed in Q1. Prior text not shown.
- `notes:72` — **insufficient**: standing Residential segment description. Prior text not shown.
- `notes:73` — **insufficient**: C&I segment description. Its over-time recognition sentence is cited in the cost-to-cost contract assets item. Prior text not shown.
- `notes:76` — Amounts only: segment sales table.
- `notes:77` — Amounts only: segment sales table.
- `notes:78` — Standing Adjusted EBITDA purpose statement. Wording only.
- `notes:81` — Amounts only: segment reconciliation, quarter.
- `notes:82` — Amounts only: segment reconciliation, six months.
- `notes:83` — Standing definition of the corporate column.
- `notes:84` — Standing definitions of the footnotes.
- `notes:85` — Amounts only: legal-matters table, whose patent line is cited in the Ollnova items.
- `notes:86` — Footnote (7) is standing. Footnote (8) is the same as the disposition item.
- `notes:88` — Amounts only: segment assets.
- `notes:89` — Amounts only: segment depreciation and amortization.
- `notes:90` — Amounts only: segment capex, cited in the capacity item.
- `notes:91` — Amounts only: share of U.S. sales and long-lived assets.
- `notes:94` — Amounts only: inventory components.
- `notes:96` — Amounts only: PP&E components.
- `notes:97` — Amounts only: finance lease assets.
- `notes:99` — Amounts only: other accrued liabilities table. Its footnote is the notes:100 item.
- `notes:102` — The reorganization's goodwill reassignment was disclosed in Q1. No new substance.
- `notes:103` — The goodwill impairment is dated to the first quarter, already reported. No new impairment is stated.
- `notes:104` — Lead-in to the table.
- `notes:105` — Amounts only: goodwill rollforward, whose disposition line is cited in the disposition item.
- `notes:107` — Standing warranty policy.
- `notes:108` — Amounts only: warranty rollforward, including a line for warranty assumed in acquisitions.
- `notes:110` — Amounts only: extended warranty deferred revenue rollforward.
- `notes:111` — Lead-in: date rolled forward.
- `notes:112` — Amounts only: extended warranty recognition schedule.
- `notes:114` — Amounts only: warranty balance sheet split.
- `notes:115` — Heading renamed to "Contract Balances". The substance is in the notes:117 item.
- `notes:116` — Framing sentence on billed, unbilled and deferred balances. Covered by the notes:117 item.
- `notes:120` — Heading.
- `notes:121` — Short-term borrowings: amounts and date rolled forward.
- `notes:122` — Lead-in to the table.
- `notes:123` — Amounts only: debt table, with rows reordered.
- `notes:124` — Amounts only: deferred financing costs.
- `notes:125` — Date rolled forward and a comma added.
- `notes:126` — Amounts only: maturities table.
- `notes:127` — Standing history of the original Term Loan B.
- `notes:128` — Rate and date rolled forward.
- `notes:129` — Ratio and date rolled forward. "New" added to the facility name.
- `notes:130` — Wording only ("depending on" for "based on", a comma added).
- `notes:131` — Rate rolled forward. The ASC 470-50 sentence was moved into this paragraph (reordered).
- `notes:132` — Covenant ratios and date rolled forward.
- `notes:133` — Standing guarantee and collateral description.
- `notes:134` — Date rolled forward.
- `notes:135` — Wording only.
- `notes:136` — Cross-reference to the 10-K added. No new substance.
- `notes:141` — **insufficient**: EPS policy, which includes a contingent-consideration share condition. Prior text not shown, so I cannot tell whether the clause is new.
- `notes:143` — Amounts only: EPS table.
- `notes:144` — Amounts only: anti-dilutive shares.
- `notes:147` — Heading.
- `notes:148` — Floor plan: amounts and date rolled forward.
- `notes:149` — PHS arbitration: unchanged according to the change history (carried verbatim).
- `notes:150` — Solar MDL settlement: unchanged according to the change history.
- `notes:152` — February 3, 2023 derivative actions: unchanged according to the change history.
- `notes:155` — Zawaski: unchanged according to the change history. Its stale "as of March 31, 2026" reference is noted in the notes:100 and mdna:109 items.
- `notes:156` — Champion patent case: unchanged according to the change history.
- `notes:157` — Florida home-standby class action: wording only (past tense, "claims" plural, "theories of liability" added to the description of the existing amended complaint).
- `notes:158` — General loss-reserve statement: unchanged according to the change history.

### MD&A (0001437749-26-025669:mdna:*)
- `mdna:12` — **insufficient**: business overview. The data center sentence may be new or reworded. No amount or commitment.
- `mdna:32` — **insufficient**: commodity, currency and tariff exposure paragraph. Prior text not shown. No amount.
- `mdna:37` — Repeats the notes:9 and notes:10 tariff items in rounded amounts.
- `mdna:42` — Standing description of the July 2025 credit amendment.
- `mdna:44` — Same explanation as the tax item at notes:146.
- `mdna:45` — OBBBA paragraph: date rolled forward. Cash tax savings are cited in the mdna:109 item.
- `mdna:46` — Pillar Two paragraph: date rolled forward, no impact stated.
- `mdna:48` — Heading.
- `mdna:50` — Amounts only: quarterly results table.
- `mdna:52` — The reorganization was disclosed in Q1.
- `mdna:55` — Amounts only.
- `mdna:56` — Amounts only.
- `mdna:57` — Amounts only.
- `mdna:60` — Acquisition contribution amount, covered by the notes:23 item.
- `mdna:64` — Same explanation as the tax item at notes:146.
- `mdna:65` — Amounts only.
- `mdna:66` — C&I tariff of about 2%, mix and opex. Covered by the tariff-in-adjusted-measures, mix/input cost and legal/opex items.
- `mdna:68` — Amounts, with a generic explanation.
- `mdna:70` — Heading.
- `mdna:71` — Lead-in.
- `mdna:72` — Amounts only: six-month results table.
- `mdna:73` — Heading.
- `mdna:74` — Standing statement on recast segment history.
- `mdna:75` — Lead-in.
- `mdna:76` — Amounts only.
- `mdna:77` — Amounts only.
- `mdna:78` — Amounts only.
- `mdna:79` — Six-month version of the mdna:58 item.
- `mdna:80` — Six-month version of the mdna:59 item.
- `mdna:81` — Six-month acquisition contribution, covered by the notes:23 item.
- `mdna:82` — Six-month version of the gross margin tariff and mix items.
- `mdna:83` — Six-month version of the mdna:62 item.
- `mdna:84` — Six-month version of the Wallbox and disposition items.
- `mdna:85` — Same explanation as the tax item at notes:146.
- `mdna:86` — Amounts only.
- `mdna:87` — Six-month C&I tariff effect, covered by the tariff-in-adjusted-measures item.
- `mdna:88` — Six-month Residential tariff effect, cited in the mdna:67 item.
- `mdna:89` — Amounts, with a generic explanation.
- `mdna:90` — Cross-reference.
- `mdna:92` — **insufficient**: standing statement of cash requirements. Prior text not shown.
- `mdna:93` — Credit agreement: rate and date rolled forward.
- `mdna:95` — Amounts only: borrowings and unused capacity.
- `mdna:96` — Amounts only: Term Loan B rate and leverage.
- `mdna:97` — Amounts only: covenant ratios.
- `mdna:98` — Standing buyback program description, date rolled forward. Cited in the no-repurchase item.
- `mdna:99` — Same as the no-repurchase item at notes:139.
- `mdna:101` — Floor plan: amounts only.
- `mdna:103` — Amounts only: liquidity.
- `mdna:106` — Heading.
- `mdna:108` — Amounts only: cash flow table.
- `mdna:110` — Amounts only: investing lines.
- `mdna:111` — Amounts only: prior-year investing.
- `mdna:112` — Amounts only: financing lines.
- `mdna:113` — Amounts only: prior-year financing.
- `mdna:134` — Wording only: non-GAAP limitations bullet.
- `mdna:135` — Non-GAAP limitations bullet, used for comparison in the mdna:121 item.
- `mdna:144` — Wording only ("New and Prior Credit Agreements").
- `mdna:147` — Amounts only: Adjusted EBITDA reconciliation.
- `mdna:153` — Wording only: transaction-costs footnote.
- `mdna:155` — Table heading.
- `mdna:156` — Amounts only: legal-matters table, whose patent line is cited in the Ollnova items.
- `mdna:158` — Same as the disposition item at notes:28.
- `mdna:168` — Amounts only: adjusted net income reconciliation.
- `mdna:171` — Same as the disposition item at notes:28.

### Item 4 (0001437749-26-025669:item_4_controls:*)
- `item_4_controls:1` — Heading.
- `item_4_controls:2` — Heading.
- `item_4_controls:3` — Standing conclusion that disclosure controls are effective.
- `item_4_controls:4` — Heading.

### 8-K Item 2.02, exhibit 99.1 (0001437749-26-024731:8k_2_02:*)
- `8k_2_02:1` — Exhibit header.
- `8k_2_02:2` — File name.
- `8k_2_02:3` — Exhibit label.
- `8k_2_02:4` — Release title.
- `8k_2_02:5` — Headline. The substance is in the 8k:20 backlog item.
- `8k_2_02:6` — Dateline boilerplate.
- `8k_2_02:7` — Heading.
- `8k_2_02:8` — Amounts only: consolidated sales.
- `8k_2_02:9` — Amounts only: C&I sales.
- `8k_2_02:10` — Amounts only: Residential sales.
- `8k_2_02:11` — Amounts only: net income and EPS.
- `8k_2_02:12` — Amounts only: adjusted net income.
- `8k_2_02:13` — Amounts only: adjusted EBITDA.
- `8k_2_02:15` — Amounts only: cash flow and FCF.
- `8k_2_02:19` — The same guidance as the items at 8k:35 and 8k:36.
- `8k_2_02:21` — Heading.
- `8k_2_02:22` — Duplicate of mdna:61 (gross margin items).
- `8k_2_02:23` — Duplicate of the mdna:62 item.
- `8k_2_02:24` — Duplicate of the tax item at notes:146.
- `8k_2_02:25` — Duplicate of the mdna:109 item.
- `8k_2_02:26` — Heading.
- `8k_2_02:27` — Heading.
- `8k_2_02:28` — Duplicate of the mdna:58 item.
- `8k_2_02:29` — Duplicate of mdna:66.
- `8k_2_02:30` — Heading.
- `8k_2_02:31` — Duplicate of the mdna:59 item.
- `8k_2_02:32` — Duplicate of the mdna:67 item.
- `8k_2_02:33` — Page number.
- `8k_2_02:34` — Heading.
- `8k_2_02:37` — Heading.
- `8k_2_02:38` — Conference call logistics.
- `8k_2_02:39` — Webcast boilerplate.
- `8k_2_02:40` — Replay boilerplate.
- `8k_2_02:41` — Heading.
- `8k_2_02:42` — Company description boilerplate.
- `8k_2_02:43` — Heading.
- `8k_2_02:44` — Forward-looking boilerplate.
- `8k_2_02:45` — Forward-looking boilerplate.
- `8k_2_02:46` — Forward-looking bullet (power outages): same list as mdna:8.
- `8k_2_02:47` — Forward-looking bullet (raw materials): same list as mdna:8.
- `8k_2_02:48` — Forward-looking bullet (contract manufacturers): same list as mdna:8.
- `8k_2_02:49` — Forward-looking bullet (trade policy and tariffs): same list as mdna:8.
- `8k_2_02:50` — Forward-looking bullet (intellectual property): same list as mdna:8.
- `8k_2_02:51` — Forward-looking bullet (durable goods spending): same list as mdna:8.
- `8k_2_02:52` — Forward-looking bullet (grants and tax incentives): cited in the mdna:8 item.
- `8k_2_02:53` — Forward-looking bullet (liability and warranty claims): same list as mdna:8.
- `8k_2_02:54` — Forward-looking bullet (legal proceedings): same list as mdna:8.
- `8k_2_02:55` — Forward-looking bullet (share repurchases): same list as mdna:8.
- `8k_2_02:56` — Forward-looking bullet (laws and standards): same list as mdna:8.
- `8k_2_02:57` — Forward-looking bullet (data center product acceptance): cited in the mdna:8 item.
- `8k_2_02:58` — Forward-looking bullet (data center market growth): cited in the mdna:8 item.
- `8k_2_02:59` — Forward-looking bullet (data center contract risk): the same bullet as the mdna:8 item.
- `8k_2_02:60` — Forward-looking bullet (forecasting and inventory): cited in the mdna:8 item.
- `8k_2_02:61` — Forward-looking bullet (competition): same list as mdna:8.
- `8k_2_02:62` — Forward-looking bullet (dealer network): same list as mdna:8.
- `8k_2_02:63` — Forward-looking bullet (prices and mix): same list as mdna:8.
- `8k_2_02:64` — Forward-looking bullet (key management): same list as mdna:8.
- `8k_2_02:65` — Forward-looking bullet (labor disputes): same list as mdna:8.
- `8k_2_02:66` — Forward-looking bullet (employees): same list as mdna:8.
- `8k_2_02:67` — Forward-looking bullet (manufacturing disruption): same list as mdna:8.
- `8k_2_02:68` — Forward-looking bullet (synergies): same list as mdna:8.
- `8k_2_02:69` — Forward-looking bullet (foreign sourcing): same list as mdna:8.
- `8k_2_02:70` — Forward-looking bullet (EHS): same list as mdna:8.
- `8k_2_02:71` — Forward-looking bullet (sustainability): same list as mdna:8.
- `8k_2_02:72` — Forward-looking bullet (product regulation): same list as mdna:8.
- `8k_2_02:73` — Forward-looking bullet (security breaches): same list as mdna:8.
- `8k_2_02:74` — Forward-looking bullet (geopolitics): same list as mdna:8.
- `8k_2_02:75` — Forward-looking bullet (indebtedness): same list as mdna:8.
- `8k_2_02:76` — Forward-looking bullet (credit facility terms): same list as mdna:8.
- `8k_2_02:77` — Forward-looking bullet (additional capital): same list as mdna:8.
- `8k_2_02:78` — Forward-looking bullet (goodwill impairment): same list as mdna:8.
- `8k_2_02:79` — Forward-looking bullet (stock price): same list as mdna:8.
- `8k_2_02:80` — Forward-looking bullet (tax liabilities): same list as mdna:8.
- `8k_2_02:81` — Forward-looking boilerplate.
- `8k_2_02:82` — Page number.
- `8k_2_02:83` — Forward-looking boilerplate.
- `8k_2_02:84` — Heading.
- `8k_2_02:85` — Heading.
- `8k_2_02:86` — Standing core sales definition.
- `8k_2_02:87` — Heading.
- `8k_2_02:88` — Adjusted EBITDA definition, used for comparison in the mdna:121 item.
- `8k_2_02:89` — Heading.
- `8k_2_02:90` — Standing adjusted net income definition.
- `8k_2_02:91` — Heading.
- `8k_2_02:92` — Standing free cash flow definition.
- `8k_2_02:93` — Non-GAAP boilerplate.
- `8k_2_02:94` — Source line.
- `8k_2_02:95` — Contact heading.
- `8k_2_02:96` — Contact name.
- `8k_2_02:97` — Contact details.
- `8k_2_02:98` — Page number.
- `8k_2_02:99` — Balance sheet header.
- `8k_2_02:100` — Amounts only: balance sheet.
- `8k_2_02:101` — Page number.
- `8k_2_02:102` — Income statement header.
- `8k_2_02:103` — Amounts only: income statement.
- `8k_2_02:104` — Page number.
- `8k_2_02:105` — Cash flow header.
- `8k_2_02:106` — Amounts only: cash flow statement.
- `8k_2_02:107` — Page number.
- `8k_2_02:108` — Segment header.
- `8k_2_02:109` — Amounts only: segment sales, quarter.
- `8k_2_02:110` — Amounts only: segment sales, six months.
- `8k_2_02:111` — Amounts only: segment adjusted EBITDA.
- `8k_2_02:112` — Footnote cross-reference.
- `8k_2_02:113` — Page number.
- `8k_2_02:114` — Reconciliation header.
- `8k_2_02:115` — Reconciliation header.
- `8k_2_02:116` — Amounts only: Adjusted EBITDA reconciliation.
- `8k_2_02:117` — Page number.
- `8k_2_02:118` — Reconciliation header.
- `8k_2_02:119` — Amounts only: adjusted net income reconciliation.
- `8k_2_02:120` — Standing footnote definition.
- `8k_2_02:121` — Standing footnote definition.
- `8k_2_02:122` — Standing footnote definition ("Amended Credit Agreement" wording).
- `8k_2_02:123` — Standing footnote definition.
- `8k_2_02:124` — Page number.
- `8k_2_02:125` — Footnote heading.
- `8k_2_02:126` — Amounts only: legal-matters table, whose patent line is cited in the Ollnova items.
- `8k_2_02:127` — Standing footnote definition.
- `8k_2_02:128` — Standing footnote definition.
- `8k_2_02:129` — Same as the disposition item at notes:28.
- `8k_2_02:130` — FCF header.
- `8k_2_02:131` — Amounts only: FCF reconciliation.
- `8k_2_02:132` — Page number.
