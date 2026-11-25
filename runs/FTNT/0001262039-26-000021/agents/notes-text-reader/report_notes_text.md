# report_notes_text — FTNT 10-Q 0001262039-26-000021 (quarter ended June 30, 2026)

## Scope

- **What I read:** all six input files, in full: `input_8k.md`, `input_controls.md`, `input_mdna.md`, `input_notes.md`, `input_notes_history.md` and `input_prior_predictions.md`.
- **Out-of-scope material:** none in the directory. There is no trend table, no prices or returns, no short interest, no other company's files and no probabilities. The 8-K exhibit contains the company's own condensed statements, which are part of the 8-K body.
- **Inputs that are absent:**
  - No Item 1A diff.
  - No Exhibit 21 diff.
  - No Exhibit 10 was pulled.
  - No auditor's report. This is a 10-Q, and `input_controls.md` holds Item 4 only.
- **Prior flags:** none on record (`input_prior_predictions.md`).
- **8-K index:**
  - No late-filing notice.
  - No item 4.01 or 4.02, and no 5.02 after 2025-05-15.
  - The 2026-06-16 item 5.07 is listed, but its body is not in the input.
- **Arithmetic:** none performed. Amounts are quoted as the prose states them. Where the prose says something rose or fell, the item says so. Whether it did is left to the numbers reader.
- **MD&A prior wording:** the MD&A is diffed, but its prior-period wording is not in the input. Only the notes have a change history.
  - So for MD&A paragraphs carried as text, "what changed" is what the paragraph now says.
  - Where the substance depends on whether a sentence is new and that cannot be told, the item's `what_changed` begins with `insufficient:`.

## Items

```json
{ "id": "structure_and_disclosure_changes_functional_currency_sentences_removed",
  "what_changed": "The consolidation paragraph (now notes:2, shown as 'added' in the history) drops two sentences the prior quarter carried. One said the functional currency of the foreign subsidiaries is the U.S. dollar. The other said that, effective January 1, 2026, one subsidiary's functional currency was moved to the U.S. dollar after its full operational integration. The current paragraph keeps only the consolidation and elimination sentences, and no replacement functional-currency disclosure appears in the notes carried as text. In the same filing, MD&A says Q2 other income—net decreased primarily because foreign currency exchange losses increased (mdna:121).",
  "account": "Other income—net (foreign currency remeasurement)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Effective January 1, 2026, the Company transitioned the functional currency of one of its subsidiaries to the U.S. dollar following its full operational integration.",
  "paragraph_id": "0001262039-26-000013:note_history:13",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_securities_class_action_motion_to_dismiss",
  "what_changed": "The prior text said the time to respond to the consolidated amended complaint had not yet passed. That sentence is replaced by a statement that defendants filed a motion to dismiss on June 15, 2026. The company still says the suit is without merit, the outcome is uncertain and it cannot estimate the impact; no loss accrual was recorded as of June 30, 2026 (notes:84). Other changes are wording only: 'between' became 'from' in the class period, plus two typographic fixes. The derivative action is still stayed until this case is finally resolved (notes:85).",
  "account": "Accrued liabilities (litigation loss contingency; none recorded)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Defendants filed a motion to dismiss the consolidated amended complaint on June 15, 2026.",
  "paragraph_id": "0001262039-26-000021:notes:83",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_purchase_commitment_liability_prior_year_benefit_dropped",
  "what_changed": "The period is rolled to June 30, 2026. The note now states $1.67 billion of non-cancelable inventory purchase commitments; the prior text gave $1.37 billion as of March 31, 2026. It states the liability for excess commitments as $24.0 million at June 30, 2026 and $26.7 million at December 31, 2025; the prior text gave $27.2 million at March 31, 2026. The expense sentence also changed. The prior text said the expense was 'immaterial and a $4.5 million benefit' for Q1 2026 and Q1 2025 respectively. The new text says the expense was not material for the three and six months of both 2026 and 2025, so the separately stated $4.5 million prior-year benefit no longer appears. No cause is given for the movement in the liability.",
  "account": "Accrued liabilities (liability for inventory purchase commitments); cost of product revenue",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The expense related to such accrued liability for inventory purchase commitments was not material during the three and six months ended June 30, 2026 and 2025.",
  "paragraph_id": "0001262039-26-000021:notes:79",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_inventory_purchase_commitments_demand_lead_times_component_costs",
  "what_changed": "MD&A says inventory purchase commitments totaled $1.67 billion at June 30, 2026, which it calls 'an increase of $856.5 million compared to $810.6 million as of December 31, 2025'. It attributes this to working with contract manufacturers and suppliers to optimize inventory and commitments, based on growth trends in customer demand, product lead times and increasing component costs. The same paragraph restates the $24.0 million and $26.7 million liability for excess commitments, with no cause given for it. The commitments table (notes:77) splits the total into a 2026 portion and a later portion.",
  "account": "Inventory purchase commitments; inventory; accrued liabilities",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "as we continued to work with contract manufacturers and suppliers to optimize our inventory and purchase commitments position based on growth trends in customer demand, product lead times and increasing components cost",
  "paragraph_id": "0001262039-26-000021:mdna:168",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_multi_year_component_supply_and_pricing_arrangements",
  "what_changed": "insufficient: this paragraph is carried as changed text but is not in the note change history. Its prior wording is therefore not in the input, and the changed sentence cannot be isolated. As it now reads, it says a significant portion of reported purchase commitments are firm, non-cancelable and unconditional. It also says certain commitments with contract manufacturers and suppliers relate to arrangements that secure supply and pricing of certain product components for multi-year periods. If the multi-year sentence is new, it is a new commitment disclosure that bears on future product cost and inventory.",
  "account": "Inventory purchase commitments; inventory; cost of product revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Certain of these inventory purchase commitments with contract manufacturers and suppliers relate to arrangements to secure supply and pricing for certain product components for multi-year periods.",
  "paragraph_id": "0001262039-26-000021:notes:78",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_excess_and_obsolete_inventory_reserve_without_stated_cause",
  "what_changed": "The period is rolled forward. The note states the excess and obsolete inventory reserve as $122.8 million at June 30, 2026 and $137.5 million at December 31, 2025. It says write-downs were not material for the three and six months of 2026 and 2025. Neither the note nor any MD&A paragraph carried as text gives a cause for the change in the reserve. MD&A cites demand, lead times and component costs only for purchase commitments (mdna:168).",
  "account": "Inventory (excess and obsolete reserve); cost of product revenue",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The excess and obsolete inventory reserve was $122.8 million and $137.5 million as of June 30, 2026 and December 31, 2025, respectively.",
  "paragraph_id": "0001262039-26-000021:notes:40",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_without_stated_cause",
  "what_changed": "The period is rolled forward. The note states unrecognized tax benefits of $92.4 million at June 30, 2026 and $90.4 million at December 31, 2025, of which $75.2 million would favorably affect the effective tax rate if recognized. Accrued interest and penalties are $12.6 million and $12.5 million. No cause is given for the movement. The audit paragraph (notes:126) names ongoing audits focused on intercompany profit allocation.",
  "account": "Unrecognized tax benefits (income tax liabilities); provision for income taxes",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As of June 30, 2026 and December 31, 2025, unrecognized tax benefits were $92.4 million and $90.4 million, respectively.",
  "paragraph_id": "0001262039-26-000021:notes:125",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_tax_audits_intercompany_profit_allocation",
  "what_changed": "insufficient: carried as changed text with no history entry, so the prior wording is not in the input. The paragraph now says U.S. federal tax years before 2020, and state and foreign years before 2016 in significant jurisdictions, are generally closed to examination. It says audits are ongoing in the United Kingdom, Canada, Germany and several other jurisdictions, and that they focus mainly on intercompany profit allocation. Whether a jurisdiction or a closed year changed cannot be told from the input.",
  "account": "Unrecognized tax benefits; provision for income taxes",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We currently have ongoing tax audits in the United Kingdom, Canada, Germany and several other jurisdictions.",
  "paragraph_id": "0001262039-26-000021:notes:126",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_pending_indemnification_claims",
  "what_changed": "insufficient: carried as changed text but not in the note change history, so the prior wording is not in the input. The paragraph now says indemnification claims are asserted from time to time, that claims are currently pending, and that there have been no material awards to date. It also says some agreements could expose the company to losses beyond the amount received under the agreement, and in some cases to liability with no contractual limit. Whether the pending-claims clause is new cannot be told.",
  "account": "Accrued liabilities (indemnification; none recorded)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Although from time to time there are indemnification claims asserted against us and currently there are pending indemnification claims, to date there have been no material awards under such indemnification provisions.",
  "paragraph_id": "0001262039-26-000021:notes:87",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_subsequent_event_repurchases_rolled_into_quarter",
  "what_changed": "The prior quarter's Subsequent Event note has been removed, and the current filing has no subsequent-events note (the history shows no current note matched). The removed note said that after March 31, 2026 and through its filing date, 1.9 million shares were repurchased at an average of $77.95, for $145.9 million. It said approximately $765.8 million remained available as of that filing. The current repurchase note (notes:120) says approximately $765.8 million remained available as of June 30, 2026. No repurchase after June 30, 2026 is disclosed in the text carried.",
  "account": "Common stock repurchases (stockholders' equity); cash and cash equivalents",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Subsequent to March 31, 2026 and through the filing of this Quarterly Report on Form 10-Q, we repurchased 1.9 million shares of our common stock at an average price of $77.95 per share, for an aggregate purchase price of $145.9 million, under the Repurchase Program.",
  "paragraph_id": "0001262039-26-000013:note_history:27",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_activity_and_remaining_authorization",
  "what_changed": "The period is rolled to six months. The note now says 12.5 million shares were repurchased in open-market transactions in the six months, at a weighted-average $77.73, for $972.8 million. That figure excludes a $6.7 million accrual for the 1% excise tax. The authorization totals $10.25 billion after a $1.0 billion increase in January 2026, and runs through February 28, 2027. Approximately $765.8 million remained available at June 30, 2026. MD&A (mdna:121) ties lower interest income to lower average cash after share repurchases and debt repayment.",
  "account": "Stockholders' equity (repurchases); cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "As of June 30, 2026, approximately $765.8 million remained available for future share repurchases under the Repurchase Program.",
  "paragraph_id": "0001262039-26-000021:notes:120",
  "explanation": false }
```

```json
{ "id": "earnings_quality_marketable_equity_security_gains_first_quarter_sales_only",
  "what_changed": "A new sentence says no marketable equity securities were sold in Q2 2026, or in the six months of 2025. The Q1 2026 sale ($115.9 million of proceeds, $50.7 million of net gains) is now described as a first-quarter event. Unrealized fair-value gains on securities still held are $5.1 million for Q2 and $1.5 million for the six months. MD&A attributes the six-month increase in other income—net mainly to the swing from net losses to net gains on these securities (mdna:153). It attributes the Q2 decrease partly to lower net gains on them (mdna:121). The realized sale gain therefore sits in the six-month figures and not in the second quarter.",
  "account": "Other income—net; marketable equity securities",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "We had no sales of marketable equity securities during the second quarter of 2026 and the six months ended June 30, 2025.",
  "paragraph_id": "0001262039-26-000021:notes:33",
  "explanation": false }
```

```json
{ "id": "earnings_quality_other_income_foreign_exchange_losses",
  "what_changed": "MD&A says Q2 other income—net decreased $18.0 million. The main causes it gives are a $10.1 million increase in foreign currency exchange losses and a $6.3 million decrease in net gains on marketable equity securities. The six-month discussion cites an $11.0 million increase in FX loss (mdna:153). No note carried as text explains the FX losses. The same filing removed the functional-currency sentences from the consolidation note.",
  "account": "Other income—net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Other income—net decreased $18.0 million during the three months ended June 30, 2026 compared to the same period last year, primarily due to a $10.1 million increase in foreign currency exchange losses and a $6.3 million decrease in net gains on marketable equity securities.",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_income_and_expense_after_repurchases_and_note_repayment",
  "what_changed": "MD&A attributes the $11.8 million decrease in Q2 interest income to lower average interest rates and to lower average cash balances caused by share repurchases and debt repayment. It attributes the $1.4 million decrease in interest expense to repaying the 2026 Senior Notes at maturity in March 2026. Only the 2031 Senior Notes remain outstanding (notes:73). The prose links the interest income decrease directly to cash spent on repurchases and debt repayment.",
  "account": "Interest income; interest expense",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "primarily due to lower average interest rates and lower average cash and cash equivalents balances as a result of share repurchases and debt repayment",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_product_revenue_pricing_actions_and_average_selling_prices",
  "what_changed": "MD&A attributes the Q2 product revenue increase of $264.1 million (52%) mainly to hardware growth. The causes it names are higher unit shipments, higher average selling prices from demand for higher-performing models, and 'recent pricing actions'. It also cites secure networking hardware and term licenses, deployments related to AI infrastructure, technology upgrades, upsell activity and new use cases. Pricing actions also appear in the gross margin discussion (mdna:106) and among the billings and liquidity factors (mdna:162, mdna:174).",
  "account": "Product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "higher average selling prices resulting from customer demand for higher-performing models and recent pricing actions",
  "paragraph_id": "0001262039-26-000021:mdna:100",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_product_revenue_growth_outlook_remainder_of_year",
  "what_changed": "MD&A now says it expects product revenue to keep growing year over year for the rest of 2026, against the same periods of 2025. The drivers it states are higher unit shipments and recent pricing actions.",
  "account": "Product revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We expect our product revenue to continue to grow year over year for the remainder of 2026 compared to the same periods of 2025.",
  "paragraph_id": "0001262039-26-000021:mdna:66",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_service_revenue_growth_outlook_remainder_of_year",
  "what_changed": "MD&A says service revenue increased in Q2 and in the six months, driven by security subscriptions and technical support, with 'strength in unified SASE and SecOps'. It expects service revenue to keep growing year over year for the rest of 2026. The press release gives full-year service revenue guidance of $5.180 billion to $5.220 billion (8k_2_02:35).",
  "account": "Service revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We expect our service revenue to continue to grow year over year for the remainder of 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:67",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_hardware_component_costs_product_margin",
  "what_changed": "MD&A says product gross margin may decline for full-year 2026 against 2025, primarily because hardware component costs remain higher. The word 'continued' suggests the cost pressure was cited before, but the prior wording is not in the input. In the same filing, Q2 product gross margin is said to have increased on pricing actions, partly offset by hardware mix and higher memory chip costs (mdna:106).",
  "account": "Cost of product revenue; product gross margin",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Our product gross margin may decline for the full year 2026 as compared to 2025 primarily due to continued higher hardware component costs.",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_service_margin_data_center_expansion",
  "what_changed": "MD&A expects service gross margin to decline slightly for full-year 2026 against 2025. The reason it gives is the continued expansion of data center, colocation and cloud hosting capacity for unified SASE and SecOps. Q2 service gross margin is described as down 0.1 points for the same reason (mdna:107), and the six-month figure as flat (mdna:139).",
  "account": "Cost of service revenue; service gross margin",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "We also expect service gross margin to decline slightly for the full year 2026 as compared to 2025, primarily due to continued expansion of our data center footprint and colocation and cloud hosting capacity to support the growth in our unified SASE and SecOps offerings.",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_tariff_exposure_on_hardware_sales",
  "what_changed": "MD&A says it currently does not expect U.S. tariffs to have a meaningful effect on gross margin. It adds that changes in trade policy could hurt gross margin, including higher tariff rates, changed customs or tariff classifications, or modified exemptions. Any such effect would fall mainly on hardware sales to U.S. customers. The prior wording is not in the input, so whether this assessment changed cannot be told.",
  "account": "Cost of product revenue; gross margin",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We currently do not expect the U.S. tariffs to have a meaningful impact on our gross margin.",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "earnings_quality_product_gross_margin_pricing_offsets_memory_chip_costs",
  "what_changed": "MD&A says Q2 product gross margin increased 2.4 points, primarily on recent pricing actions. It names two partial offsets: a mix shift toward hardware and higher memory chip costs. The six-month discussion says the same (mdna:138, 1.4 points). The stated cause of the margin gain is price, not cost. The same filing says product gross margin may decline for full-year 2026 because hardware component costs remain higher (mdna:70).",
  "account": "Product gross margin; cost of product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by recent pricing actions, partially offset by a shift in revenue mix to hardware and increased costs of memory chips",
  "paragraph_id": "0001262039-26-000021:mdna:106",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_operating_margin_outlook",
  "what_changed": "MD&A says Q2 operating margin increased 5.6 points (3.8 points for the six months) on operating leverage, partly offset by lower total gross margin. For full-year 2026 it expects operating margin to increase slightly against 2025, with both total revenue and operating expense rising. It says the expense increase will go mainly to sales and marketing headcount, product development, data centers and real estate. The press release separately guides full-year non-GAAP operating margin of 35.0% to 37.0% (8k_2_02:38).",
  "account": "Operating income; operating expenses",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "For the full year 2026, we expect our operating margin to increase slightly compared to 2025, benefiting from operating leverage and measured investments.",
  "paragraph_id": "0001262039-26-000021:mdna:72",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_research_and_development_expense_outlook",
  "what_changed": "MD&A says Q2 research and development expense increased $15.5 million. The main cause it gives is $13.5 million of personnel cost, from headcount, compensation rates and 'the impact of the recent acquisitions'. It expects R&D to rise in absolute dollars year over year for the rest of 2026.",
  "account": "Research and development expense",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We expect research and development expenses to increase in absolute dollars year over year during the remainder of 2026 as we invest to drive continued innovation in our products and services.",
  "paragraph_id": "0001262039-26-000021:mdna:111",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_sales_and_marketing_expense_outlook",
  "what_changed": "MD&A says Q2 sales and marketing expense increased $77.1 million, mainly from $73.4 million of personnel cost. It expects sales and marketing to rise in absolute dollars year over year for the rest of 2026, as the company invests to capture market share. Commission expense is shown separately in the segment table (notes:130).",
  "account": "Sales and marketing expense",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We expect our sales and marketing expenses to increase in absolute dollars year over year during the remainder of 2026 as we continue to invest in our global sales and marketing organization to capture additional market share.",
  "paragraph_id": "0001262039-26-000021:mdna:114",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_legal_fees_in_general_and_administrative",
  "what_changed": "MD&A attributes the Q2 general and administrative increase of $4.2 million mainly to two causes: a $2.1 million increase in legal and other professional services fees, and $1.5 million of personnel cost. It expects G&A to rise in absolute dollars for the rest of 2026. The same quarter's notes record a motion to dismiss in the securities class action (notes:83) and a stayed derivative action (notes:85). MD&A does not say which matters the legal fees relate to.",
  "account": "General and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to an increase of $2.1 million in legal related fees and other professional services fees and an increase of $1.5 million in personnel-related costs",
  "paragraph_id": "0001262039-26-000021:mdna:116",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_provision_for_expected_credit_losses_increase",
  "what_changed": "MD&A attributes the six-month general and administrative increase of $2.6 million mainly to a $1.3 million increase in the provision for expected credit losses, plus $0.9 million of legal and professional fees. No cause is given for the larger credit-loss provision. The only policy text bearing on the allowance is the January 1, 2026 adoption of the ASU 2025-05 practical expedient for current receivables, which the company says had no material impact (notes:7). The Q2 G&A paragraph (mdna:116) does not mention credit losses.",
  "account": "Allowance for credit losses (accounts receivable—net); general and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to an increase of $1.3 million in provision for expected credit losses and $0.9 million in legal related fees and other professional services fees",
  "paragraph_id": "0001262039-26-000021:mdna:148",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_moodys_upgrade_to_single_a",
  "what_changed": "New sentence: in July 2026, Moody's upgraded certain of the company's ratings to A3 from Baa1 and moved the outlook to Stable from Positive. S&P remains at BBB+ with a Stable outlook. The press release reports the same upgrade (8k_2_02:25). The paragraph also lists 'an increase in installment billings' among the factors billings depend on; the prior wording is not in the input, so whether that factor is new cannot be told.",
  "account": "Long-term debt (2031 Senior Notes)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "In July 2026, Moody’s upgraded certain of our credit ratings to A3 from Baa1 and changed the outlook to Stable from Positive.",
  "paragraph_id": "0001262039-26-000021:mdna:162",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_range",
  "what_changed": "insufficient: the paragraph is carried as changed, but the prior MD&A wording is not in the input, so whether the 2026 capital expenditure range itself changed cannot be told. It now estimates full-year 2026 capital expenditures at about $350 million to $550 million, for more data center, PoP, office and warehouse capacity. The notes record a $62.1 million U.S. real estate purchase in the six months (notes:43).",
  "account": "Purchases of property and equipment; property and equipment—net",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We estimate the full year capital expenditures to be between approximately $350 million and $550 million in 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:164",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_non_current_deferred_revenue",
  "what_changed": "MD&A attributes six-month operating cash flow of $2.12 billion to business growth, improved profitability and working capital management. It names two movements: an increase of $354.1 million in non-current deferred revenue, and an increase of $240.5 million in deferred contract costs, mainly sales commissions. The prose gives no explanation specific to receivables.",
  "account": "Net cash provided by operating activities; deferred revenue (non-current); deferred contract costs",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase of $354.1 million in the non-current portion of deferred revenue",
  "paragraph_id": "0001262039-26-000021:mdna:179",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_real_estate_purchase_for_data_center_and_office",
  "what_changed": "The property and equipment note states a U.S. real estate purchase totaling $62.1 million in the six months ended June 30, 2026, for future data center and office development. It was accounted for as an asset acquisition, with $59.5 million allocated to land and $2.6 million to buildings and improvements. The prior wording is not in the input, and the note does not say in which quarter the purchase occurred. The press release's adjusted free cash flow reconciliation adds back a Q2 'Real estate related purchases' line (8k_2_02:79).",
  "account": "Property and equipment—net (land)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "During the six months ended June 30, 2026, we purchased certain real estate property in the United States totaling $62.1 million, to be used for future development to expand our data center and office space.",
  "paragraph_id": "0001262039-26-000021:notes:43",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_operating_officer_trading_plan",
  "what_changed": "New disclosure: on June 5, 2026, the Chief Operating Officer, John Whittle, adopted a Rule 10b5-1 plan. It allows the sale of up to 56,700 shares acquired by exercising vested options, at or above a minimum price, between September 4, 2026 and September 30, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Whittle Plan provides for the potential sale by Mr. Whittle of up to 56,700 shares of our common stock, issued upon the exercise of vested stock options for shares of our common stock, at prices at or above a minimum price specified in the Whittle Plan, all between September 4, 2026 and September 30, 2027.",
  "paragraph_id": "0001262039-26-000021:notes:141",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_financial_officer_trading_plan",
  "what_changed": "New disclosure: on June 10, 2026, the Chief Financial Officer, Christiane Ohlgart, adopted a Rule 10b5-1 plan. It allows the sale of up to 115 shares, plus a not-yet-determinable number of net shares left after tax withholding on RSU and PSU vesting, between September 9, 2026 and September 15, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Ohlgart Plan provides for the potential sale by Mrs. Ohlgart of up to 115 shares of our common stock, plus a number of additional net shares (which is not yet determinable) remaining after shares are withheld to satisfy tax obligations upon vesting and settlement of RSUs and PSUs",
  "paragraph_id": "0001262039-26-000021:notes:142",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_exceeds_high_end_of_quarter_guidance",
  "what_changed": "The earnings release says Q2 results exceeded the high end of the company's own Q2 guidance on both revenue and profitability. The prior guidance is not in the input, so this is management's claim and is not checked here. The highlights report revenue of $2.05 billion, product revenue up 52% and billings up 33%.",
  "account": "Total revenue; operating income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Exceeds high end of second quarter guidance on revenue and profitability",
  "paragraph_id": "0001262039-26-000018:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised",
  "what_changed": "The earnings release says full-year 2026 revenue guidance is raised to 19% year-over-year growth. The full-year ranges it now gives (8k_2_02:34–39) are: revenue $8.020–8.180 billion; service revenue $5.180–5.220 billion; billings $9.350–9.550 billion; non-GAAP gross margin 79.0–81.0%; non-GAAP operating margin 35.0–37.0%; non-GAAP diluted EPS $3.41–3.47 on 741–745 million diluted shares. The previous guidance is not in the input.",
  "account": "Total revenue; service revenue; billings",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Raises 2026 revenue guidance to 19% year over year growth",
  "paragraph_id": "0001262039-26-000018:8k_2_02:6",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_guidance_ranges",
  "what_changed": "The earnings release gives Q3 2026 guidance (8k_2_02:28–32): revenue $2.010–2.100 billion; billings $2.250–2.350 billion; non-GAAP gross margin 79.0–81.0%; non-GAAP operating margin 35.0–37.0%; non-GAAP diluted EPS $0.83–0.87, assuming an 18% non-GAAP tax rate and 741–745 million diluted shares.",
  "account": "Total revenue; billings; operating income",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Revenue in the range of $2.010 billion to $2.100 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:28",
  "explanation": false }
```

```json
{ "id": "across_documents_intel_processor_collaboration_and_supply_commitments",
  "what_changed": "The earnings release announces a strategic collaboration with Intel to develop the SP6 security processor, using Intel's design, development, packaging and manufacturing capabilities. It describes this as strengthening the resilience and diversity of the supply chain. No 10-Q paragraph carried as text mentions Intel or any commitment tied to SP6. The same quarter's 10-Q text does describe multi-year component supply and pricing arrangements (notes:78) and higher memory chip costs (mdna:106). It also describes purchase commitments that MD&A says increased on lead times and component costs (mdna:168).",
  "account": "Inventory purchase commitments; research and development expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Announced a strategic collaboration with Intel to develop Fortinet Security Processor 6 (SP6)",
  "paragraph_id": "0001262039-26-000018:8k_2_02:20",
  "explanation": false }
```

```json
{ "id": "across_documents_adjusted_free_cash_flow_adds_back_real_estate_purchases",
  "what_changed": "The earnings release defines and reconciles a non-GAAP 'adjusted free cash flow', alongside free cash flow, that adds back cash paid for real estate related purchases (8k_2_02:79). The 10-Q MD&A non-GAAP section defines and reconciles only free cash flow (mdna:88, mdna:89) and has no adjusted measure. Earlier releases are not in the input, so whether the adjusted measure is new cannot be told.",
  "account": "Purchases of property and equipment; free cash flow (non-GAAP)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "We define adjusted free cash flow as free cash flow plus cash payments associated with real estate related purchases.",
  "paragraph_id": "0001262039-26-000018:8k_2_02:88",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_litigation_forward_looking_bullet",
  "what_changed": "insufficient: this forward-looking-statement bullet is carried as changed text, but the prior MD&A wording is not in the input. It now lists expected outcomes and liabilities in litigation as a forward-looking topic. Whether the bullet is new or reworded cannot be told. If it is new, it arrives in the same quarter as the motion to dismiss (notes:83).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "expected outcomes and liabilities in litigation;",
  "paragraph_id": "0001262039-26-000021:mdna:28",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_macroeconomic_tariff_forward_looking_bullet",
  "what_changed": "insufficient: this forward-looking-statement bullet is carried as changed text, but the prior MD&A wording is not in the input. It now names macroeconomic and geopolitical disruptions to manufacturing or sales, including tariffs or other trade disruptions, public health issues, wars, natural disasters and economic growth. Which words were added cannot be told.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "macroeconomic, geopolitical factors and other disruptions to our manufacturing or sales, including tariffs or other trade disruptions, public health issues, wars, natural disasters and economic growth;",
  "paragraph_id": "0001262039-26-000021:mdna:7",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_cloud_marketplace_sales_channel",
  "what_changed": "insufficient: the sales-channel paragraph is carried as changed text, but the prior MD&A wording is not in the input. It now says software licenses and cloud-delivered services are also sold through third-party cloud service provider platforms, both directly and through channel partners. If that sentence is new, it adds a channel and counterparty type. No revenue-recognition policy text about this channel appears in the notes carried as text.",
  "account": "Product revenue (software licenses); service revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We also sell our software licenses and cloud delivered services via third-party cloud service provider platforms, both directly and through our channel partners.",
  "paragraph_id": "0001262039-26-000021:mdna:77",
  "explanation": false }
```

### Items marked insufficient

- estimates_and_discretion_multi_year_component_supply_and_pricing_arrangements
- related_parties_contingencies_and_subsequent_events_tax_audits_intercompany_profit_allocation
- related_parties_contingencies_and_subsequent_events_pending_indemnification_claims
- liquidity_and_capital_capital_expenditure_range
- related_parties_contingencies_and_subsequent_events_litigation_forward_looking_bullet
- narrative_signs_of_operating_pressure_macroeconomic_tariff_forward_looking_bullet
- revenue_recognition_cloud_marketplace_sales_channel

### Items with explanation set to true

- estimates_and_discretion_inventory_purchase_commitments_demand_lead_times_component_costs

## Paragraphs carried as text with no item of their own

### Notes

- 0001262039-26-000021:notes:1 — date rolled forward (March 31 three months → June 30 three and six months)
- 0001262039-26-000021:notes:2 — the remaining sentences are unchanged. The removed functional-currency sentences are recorded in the item quoting 0001262039-26-000013:note_history:13.
- 0001262039-26-000021:notes:4 — date rolled forward
- 0001262039-26-000021:notes:7 — ASU 2025-05 adoption statement; prior wording not in input; no new substance found (the credit-loss provision is in the mdna:148 item)
- 0001262039-26-000021:notes:10 — pending ASU 2024-03, still under evaluation; no substance found
- 0001262039-26-000021:notes:12 — pending ASU 2025-06, still being assessed; no substance found
- 0001262039-26-000021:notes:15 — amounts only (six-month columns added to the disaggregation table)
- 0001262039-26-000021:notes:17 — amounts only; period rolled forward
- 0001262039-26-000021:notes:19 — amounts only (remaining performance obligations and their timing)
- 0001262039-26-000021:notes:21 — amounts only
- 0001262039-26-000021:notes:23 — table lead-in; wording only
- 0001262039-26-000021:notes:24 — amounts only
- 0001262039-26-000021:notes:27 — amounts only
- 0001262039-26-000021:notes:30 — amounts only
- 0001262039-26-000021:notes:36 — amounts only
- 0001262039-26-000021:notes:37 — date rolled forward
- 0001262039-26-000021:notes:39 — amounts only
- 0001262039-26-000021:notes:42 — amounts only
- 0001262039-26-000021:notes:44 — amounts only
- 0001262039-26-000021:notes:48 — prior-year Linksys accounting; the paragraph boundary moved (it continues in notes:49); no substance found
- 0001262039-26-000021:notes:49 — continuation of notes:48; same reason
- 0001262039-26-000021:notes:53 — boilerplate that acquisitions are not material; no substance found
- 0001262039-26-000021:notes:55 — date rolled forward; goodwill unchanged in the text, no impairment
- 0001262039-26-000021:notes:58 — amounts only
- 0001262039-26-000021:notes:60 — amounts only
- 0001262039-26-000021:notes:62 — amounts only
- 0001262039-26-000021:notes:65 — amounts only
- 0001262039-26-000021:notes:67 — amounts only
- 0001262039-26-000021:notes:68 — heading
- 0001262039-26-000021:notes:69 — description of the 2021 note issuance; no substance found
- 0001262039-26-000021:notes:70 — the March 2026 repayment was already reported last quarter; no new substance
- 0001262039-26-000021:notes:71 — redemption and interest terms; no substance found
- 0001262039-26-000021:notes:72 — table lead-in
- 0001262039-26-000021:notes:73 — amounts only (per the history, only the discount line and date changed)
- 0001262039-26-000021:notes:74 — amounts only; period rolled forward; still no financial covenants
- 0001262039-26-000021:notes:75 — amounts only (fair value of the 2031 notes)
- 0001262039-26-000021:notes:76 — heading; date rolled forward
- 0001262039-26-000021:notes:77 — amounts only (commitments table; see the mdna:168 item)
- 0001262039-26-000021:notes:80 — amounts only, plus a grammar fix ('consist' → 'consists')
- 0001262039-26-000021:notes:81 — amounts only (operating lease commitments)
- 0001262039-26-000021:notes:82 — date rolled forward
- 0001262039-26-000021:notes:84 — date rolled forward; still no accrual (recorded in the class-action item)
- 0001262039-26-000021:notes:85 — wording only ('et. seq.' → 'et seq.'); the stay is unchanged
- 0001262039-26-000021:notes:86 — date rolled forward (Alorica; no accrual)
- 0001262039-26-000021:notes:88 — standard cybersecurity statement; prior wording not in input; no substance found
- 0001262039-26-000021:notes:90 — amounts only (shares available for grant)
- 0001262039-26-000021:notes:93 — amounts only
- 0001262039-26-000021:notes:96 — amounts only; period rolled forward
- 0001262039-26-000021:notes:97 — amounts only
- 0001262039-26-000021:notes:98 — amounts only
- 0001262039-26-000021:notes:99 — amounts only
- 0001262039-26-000021:notes:100 — paragraph split at a page break; no substance found
- 0001262039-26-000021:notes:101 — continuation of notes:100
- 0001262039-26-000021:notes:103 — amounts only
- 0001262039-26-000021:notes:106 — amounts only
- 0001262039-26-000021:notes:108 — amounts only
- 0001262039-26-000021:notes:109 — amounts only
- 0001262039-26-000021:notes:111 — amounts only
- 0001262039-26-000021:notes:114 — amounts only
- 0001262039-26-000021:notes:116 — amounts only
- 0001262039-26-000021:notes:118 — amounts only
- 0001262039-26-000021:notes:121 — amounts only; period rolled forward (Q2 tax components)
- 0001262039-26-000021:notes:122 — continuation of notes:121; amounts only
- 0001262039-26-000021:notes:123 — amounts only; period rolled to six months
- 0001262039-26-000021:notes:124 — date rolled forward (the Act's effects are recognized)
- 0001262039-26-000021:notes:127 — period rolled forward; the January 2026 OECD guidance came before the prior filing; Pillar Two impact still stated as none
- 0001262039-26-000021:notes:128 — segment boilerplate (one segment); no substance found
- 0001262039-26-000021:notes:130 — amounts only
- 0001262039-26-000021:notes:134 — amounts only
- 0001262039-26-000021:notes:135 — amounts only
- 0001262039-26-000021:notes:137 — amounts only (distributor revenue concentration)
- 0001262039-26-000021:notes:139 — amounts only (distributor receivable concentration)

### MD&A

- 0001262039-26-000021:mdna:20 — page number
- 0001262039-26-000021:mdna:34 — overview; date rolled forward; patent counts are amounts only
- 0001262039-26-000021:mdna:37 — page number
- 0001262039-26-000021:mdna:38 — product description (FortiOS); no account, risk or commitment content
- 0001262039-26-000021:mdna:41 — product description (FortiAI, FortiAIGate); no account, risk or commitment content
- 0001262039-26-000021:mdna:44 — product count and pillar lead-in; wording
- 0001262039-26-000021:mdna:45 — product description (Secure Networking); no account content
- 0001262039-26-000021:mdna:46 — page number
- 0001262039-26-000021:mdna:47 — continuation of the product description
- 0001262039-26-000021:mdna:48 — product description (Unified SASE, sovereign deployments); no account content
- 0001262039-26-000021:mdna:49 — product description (SecOps, FortiSOC); no account content; the FortiSOC launch is also in 8k_2_02:22
- 0001262039-26-000021:mdna:50 — FortiGuard Labs description
- 0001262039-26-000021:mdna:53 — description of support service tiers
- 0001262039-26-000021:mdna:55 — Training Institute; certification count only
- 0001262039-26-000021:mdna:57 — amounts only (revenue highlights; causes in the mdna:100 and mdna:67 items)
- 0001262039-26-000021:mdna:58 — amounts only
- 0001262039-26-000021:mdna:59 — amounts only
- 0001262039-26-000021:mdna:60 — amounts only
- 0001262039-26-000021:mdna:61 — amounts only
- 0001262039-26-000021:mdna:62 — amounts only
- 0001262039-26-000021:mdna:63 — amounts only
- 0001262039-26-000021:mdna:64 — amounts only (cause in the mdna:179 item)
- 0001262039-26-000021:mdna:65 — amounts only (regional mix and growth)
- 0001262039-26-000021:mdna:68 — page number
- 0001262039-26-000021:mdna:69 — amounts only (country concentration of billings; prior count not in input)
- 0001262039-26-000021:mdna:71 — amounts and headcount only (the operating-leverage cause is in the mdna:72 item)
- 0001262039-26-000021:mdna:82 — amounts only
- 0001262039-26-000021:mdna:83 — amounts only (deferred revenue balances); definition unchanged
- 0001262039-26-000021:mdna:84 — definition plus amounts only
- 0001262039-26-000021:mdna:85 — page number
- 0001262039-26-000021:mdna:87 — amounts only
- 0001262039-26-000021:mdna:88 — free cash flow definition; wording (the cross-document point is in the 8k_2_02:88 item)
- 0001262039-26-000021:mdna:89 — amounts only
- 0001262039-26-000021:mdna:92 — date rolled forward (no material change to critical accounting estimates)
- 0001262039-26-000021:mdna:96 — heading; date rolled forward
- 0001262039-26-000021:mdna:98 — amounts only
- 0001262039-26-000021:mdna:99 — amounts only (regional ranking restated in words)
- 0001262039-26-000021:mdna:101 — quarter amounts; cause as in the mdna:67 item
- 0001262039-26-000021:mdna:102 — amounts only
- 0001262039-26-000021:mdna:104 — amounts only
- 0001262039-26-000021:mdna:105 — amounts only; mix-shift cause as in the mdna:70 and mdna:106 items
- 0001262039-26-000021:mdna:107 — quarter amount; cause as in the mdna:70 service-margin item
- 0001262039-26-000021:mdna:109 — amounts only
- 0001262039-26-000021:mdna:112 — page number
- 0001262039-26-000021:mdna:118 — amounts only (operating margin bridge; cause as in the mdna:72 item)
- 0001262039-26-000021:mdna:120 — amounts only
- 0001262039-26-000021:mdna:123 — amounts only
- 0001262039-26-000021:mdna:124 — amounts only (same content as notes:121)
- 0001262039-26-000021:mdna:125 — page number
- 0001262039-26-000021:mdna:126 — prior-year comparative amounts only
- 0001262039-26-000021:mdna:127 — heading
- 0001262039-26-000021:mdna:128 — heading
- 0001262039-26-000021:mdna:129 — amounts only
- 0001262039-26-000021:mdna:130 — amounts only
- 0001262039-26-000021:mdna:131 — six-month amounts; causes as in the mdna:100 item
- 0001262039-26-000021:mdna:132 — six-month amounts; causes as in the mdna:67 item
- 0001262039-26-000021:mdna:133 — amounts only
- 0001262039-26-000021:mdna:134 — page number
- 0001262039-26-000021:mdna:135 — heading
- 0001262039-26-000021:mdna:136 — amounts only
- 0001262039-26-000021:mdna:137 — amounts only; mix-shift cause as in the mdna:70 item
- 0001262039-26-000021:mdna:138 — six-month amounts; causes as in the mdna:106 item
- 0001262039-26-000021:mdna:139 — amounts only (six-month service margin flat)
- 0001262039-26-000021:mdna:140 — heading
- 0001262039-26-000021:mdna:141 — amounts only
- 0001262039-26-000021:mdna:142 — heading
- 0001262039-26-000021:mdna:143 — six-month amounts only
- 0001262039-26-000021:mdna:144 — page number
- 0001262039-26-000021:mdna:145 — heading
- 0001262039-26-000021:mdna:146 — six-month amounts only (personnel and marketing programs)
- 0001262039-26-000021:mdna:147 — heading
- 0001262039-26-000021:mdna:149 — heading
- 0001262039-26-000021:mdna:150 — six-month amounts only (operating margin bridge)
- 0001262039-26-000021:mdna:151 — heading
- 0001262039-26-000021:mdna:152 — amounts only
- 0001262039-26-000021:mdna:153 — six-month amounts; causes (equity-security gains, prior-year Linksys bargain gain, FX loss) are in the notes:33 and mdna:121 items
- 0001262039-26-000021:mdna:154 — heading
- 0001262039-26-000021:mdna:155 — amounts only
- 0001262039-26-000021:mdna:156 — amounts only (six-month tax)
- 0001262039-26-000021:mdna:157 — page number
- 0001262039-26-000021:mdna:158 — prior-year comparative amounts only
- 0001262039-26-000021:mdna:160 — amounts only
- 0001262039-26-000021:mdna:163 — same facts as the notes:120 item
- 0001262039-26-000021:mdna:165 — page number
- 0001262039-26-000021:mdna:166 — date rolled forward; the 2026 note repayment was already reported last quarter
- 0001262039-26-000021:mdna:170 — amounts only (other contractual commitments)
- 0001262039-26-000021:mdna:172 — amounts only; liquidity statement unchanged in substance
- 0001262039-26-000021:mdna:173 — amounts only (cash held internationally)
- 0001262039-26-000021:mdna:174 — list of long-term cash factors (includes 'pricing actions'); prior wording not in input; no change identifiable
- 0001262039-26-000021:mdna:175 — page number
- 0001262039-26-000021:mdna:176 — date rolled forward (no off-balance-sheet arrangements)
- 0001262039-26-000021:mdna:182 — amounts only (investing)
- 0001262039-26-000021:mdna:185 — amounts only (financing)

### Item 4

- 0001262039-26-000021:item_4_controls:1 — heading
- 0001262039-26-000021:item_4_controls:2 — heading
- 0001262039-26-000021:item_4_controls:3 — standard evaluation language; date rolled forward
- 0001262039-26-000021:item_4_controls:4 — date rolled forward; disclosure controls still concluded effective
- 0001262039-26-000021:item_4_controls:5 — heading
- 0001262039-26-000021:item_4_controls:6 — date rolled forward; no change in internal control over financial reporting stated
- 0001262039-26-000021:item_4_controls:7 — page number

### 8-K item 2.02 (0001262039-26-000018)

- 0001262039-26-000018:8k_2_02:1 — exhibit cover
- 0001262039-26-000018:8k_2_02:2 — document label
- 0001262039-26-000018:8k_2_02:3 — heading
- 0001262039-26-000018:8k_2_02:4 — headline; the claim is in the 8k_2_02:5 item
- 0001262039-26-000018:8k_2_02:7 — heading
- 0001262039-26-000018:8k_2_02:8 — amounts only
- 0001262039-26-000018:8k_2_02:9 — amounts only
- 0001262039-26-000018:8k_2_02:10 — amounts only
- 0001262039-26-000018:8k_2_02:11 — amounts only
- 0001262039-26-000018:8k_2_02:12 — amounts only
- 0001262039-26-000018:8k_2_02:13 — amounts only
- 0001262039-26-000018:8k_2_02:14 — amounts only
- 0001262039-26-000018:8k_2_02:15 — amounts only
- 0001262039-26-000018:8k_2_02:16 — amounts only
- 0001262039-26-000018:8k_2_02:17 — dateline
- 0001262039-26-000018:8k_2_02:18 — CEO quote; promotional, no account content
- 0001262039-26-000018:8k_2_02:19 — heading
- 0001262039-26-000018:8k_2_02:21 — product launch (FortiGate 1200G); no account, commitment or risk content
- 0001262039-26-000018:8k_2_02:22 — product launch (FortiSOC); no account, commitment or risk content
- 0001262039-26-000018:8k_2_02:23 — product expansion (FortiEndpoint); no account, commitment or risk content
- 0001262039-26-000018:8k_2_02:24 — partnership announcements with no financial terms
- 0001262039-26-000018:8k_2_02:25 — Moody's upgrade; same fact as the mdna:162 item
- 0001262039-26-000018:8k_2_02:26 — heading
- 0001262039-26-000018:8k_2_02:27 — lead-in
- 0001262039-26-000018:8k_2_02:29 — guidance amount; recorded in the 8k_2_02:28 item
- 0001262039-26-000018:8k_2_02:30 — guidance amount; recorded in the 8k_2_02:28 item
- 0001262039-26-000018:8k_2_02:31 — guidance amount; recorded in the 8k_2_02:28 item
- 0001262039-26-000018:8k_2_02:32 — guidance amount; recorded in the 8k_2_02:28 item
- 0001262039-26-000018:8k_2_02:33 — lead-in
- 0001262039-26-000018:8k_2_02:34 — guidance amount; recorded in the 8k_2_02:6 item
- 0001262039-26-000018:8k_2_02:35 — guidance amount; recorded in the 8k_2_02:6 and mdna:67 items
- 0001262039-26-000018:8k_2_02:36 — guidance amount; recorded in the 8k_2_02:6 item
- 0001262039-26-000018:8k_2_02:37 — guidance amount; recorded in the 8k_2_02:6 item
- 0001262039-26-000018:8k_2_02:38 — guidance amount; recorded in the 8k_2_02:6 and mdna:72 items
- 0001262039-26-000018:8k_2_02:39 — guidance amount; recorded in the 8k_2_02:6 item
- 0001262039-26-000018:8k_2_02:40 — standard non-GAAP guidance exclusions
- 0001262039-26-000018:8k_2_02:41 — conference call logistics
- 0001262039-26-000018:8k_2_02:42 — conference call logistics
- 0001262039-26-000018:8k_2_02:43 — conference schedule
- 0001262039-26-000018:8k_2_02:44 — conference schedule
- 0001262039-26-000018:8k_2_02:45 — conference schedule
- 0001262039-26-000018:8k_2_02:46 — conference schedule
- 0001262039-26-000018:8k_2_02:47 — conference schedule
- 0001262039-26-000018:8k_2_02:48 — conference schedule
- 0001262039-26-000018:8k_2_02:49 — conference schedule
- 0001262039-26-000018:8k_2_02:50 — conference schedule
- 0001262039-26-000018:8k_2_02:51 — conference schedule
- 0001262039-26-000018:8k_2_02:52 — conference schedule
- 0001262039-26-000018:8k_2_02:53 — conference schedule
- 0001262039-26-000018:8k_2_02:54 — conference logistics
- 0001262039-26-000018:8k_2_02:55 — heading
- 0001262039-26-000018:8k_2_02:56 — company boilerplate
- 0001262039-26-000018:8k_2_02:57 — heading
- 0001262039-26-000018:8k_2_02:58 — standard forward-looking statements; the paragraph is cut off mid-sentence in the input ('renewals from existing')
- 0001262039-26-000018:8k_2_02:59 — heading
- 0001262039-26-000018:8k_2_02:60 — non-GAAP lead-in
- 0001262039-26-000018:8k_2_02:61 — heading
- 0001262039-26-000018:8k_2_02:62 — heading
- 0001262039-26-000018:8k_2_02:63 — heading
- 0001262039-26-000018:8k_2_02:64 — amounts only (balance sheet)
- 0001262039-26-000018:8k_2_02:65 — heading
- 0001262039-26-000018:8k_2_02:66 — heading
- 0001262039-26-000018:8k_2_02:67 — heading
- 0001262039-26-000018:8k_2_02:68 — amounts only (income statement)
- 0001262039-26-000018:8k_2_02:69 — heading
- 0001262039-26-000018:8k_2_02:70 — heading
- 0001262039-26-000018:8k_2_02:71 — heading
- 0001262039-26-000018:8k_2_02:72 — amounts only (cash flow statement)
- 0001262039-26-000018:8k_2_02:73 — heading
- 0001262039-26-000018:8k_2_02:74 — heading
- 0001262039-26-000018:8k_2_02:75 — heading
- 0001262039-26-000018:8k_2_02:76 — amounts only (non-GAAP reconciliation)
- 0001262039-26-000018:8k_2_02:77 — standard tax-rate footnote
- 0001262039-26-000018:8k_2_02:78 — heading
- 0001262039-26-000018:8k_2_02:79 — amounts only (free cash flow and adjusted free cash flow reconciliation; see the 8k_2_02:88 item)
- 0001262039-26-000018:8k_2_02:80 — heading
- 0001262039-26-000018:8k_2_02:81 — amounts only (billings reconciliation)
- 0001262039-26-000018:8k_2_02:82 — footnote
- 0001262039-26-000018:8k_2_02:83 — heading
- 0001262039-26-000018:8k_2_02:84 — standard non-GAAP explanation
- 0001262039-26-000018:8k_2_02:85 — standard non-GAAP explanation
- 0001262039-26-000018:8k_2_02:86 — billings definition; standard
- 0001262039-26-000018:8k_2_02:87 — free cash flow definition; standard
- 0001262039-26-000018:8k_2_02:89 — non-GAAP gross profit definition; standard
- 0001262039-26-000018:8k_2_02:90 — non-GAAP operating income definition; standard
- 0001262039-26-000018:8k_2_02:91 — standard non-GAAP explanation
- 0001262039-26-000018:8k_2_02:92 — non-GAAP net income definition; standard
- 0001262039-26-000018:8k_2_02:93 — separator
- 0001262039-26-000018:8k_2_02:94 — trademark notice
- 0001262039-26-000018:8k_2_02:95 — document code
- 0001262039-26-000018:8k_2_02:96 — contacts
