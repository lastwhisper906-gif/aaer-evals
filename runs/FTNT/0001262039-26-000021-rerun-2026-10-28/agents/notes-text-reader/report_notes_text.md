# FTNT 10-Q 0001262039-26-000021 (quarter ended June 30, 2026): notes-text reader

## Scope and input check

- **Files read in full:** input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md, input_prior_predictions.md.
- **Forbidden material:** none of it is in the directory. There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no prior-run probability and no outcome window. The 8-K exhibit 99.1 contains financial-statement tables, but it is an 8-K body, which my inputs allow.
- **Absent from my input:**
  - No auditor's report. This is a 10-Q, and input_controls.md has no report section.
  - No Item 1A diff and no Exhibit 21 diff.
  - No Exhibit 10 was pulled.
  - Of the 8-K bodies, only the 2026-07-29 item 2.02 release is in my input. The body of the 2026-06-16 item 5.07 filing is not.
- **Prior flags:** none on record.
- **Comparison basis:** the prior period is the Q1 10-Q, 0001262039-26-000013. Wherever a paragraph is carried as text but its Q1 wording is not in my input, the item says so.
- **No arithmetic:** directions below are what the prose says or implies. None is computed.

## Items

```json
{ "id": "structure_and_disclosure_changes_functional_currency_transition_sentences_removed",
  "what_changed": "The consolidation paragraph (now 0001262039-26-000021:notes:2) drops two Q1 sentences. One said that as of March 31, 2026 the functional currency of the foreign subsidiaries is the U.S. dollar. The other said that one subsidiary switched to a U.S. dollar functional currency effective January 1, 2026, after full operational integration. No sentence on functional currency replaces them. In the same filing, MD&A credits part of the quarter's other income—net decrease to a $10.1 million increase in foreign currency exchange losses (mdna:121). The text does not connect the two.",
  "account": "other income—net (foreign currency remeasurement); accumulated other comprehensive loss",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Effective January 1, 2026, the Company transitioned the functional currency of one of its subsidiaries to the U.S. dollar following its full operational integration.",
  "paragraph_id": "0001262039-26-000013:note_history:13",
  "explanation": false }
```

```json
{ "id": "earnings_quality_marketable_equity_realized_gains_without_further_sales",
  "what_changed": "New sentence: there were no sales of marketable equity securities in the second quarter of 2026. The note places the $50.7 million of realized net gains (on $115.9 million of net proceeds) in the first quarter of 2026. For this quarter it gives a $5.1 million unrealized gain on securities still held, and $1.5 million for the six months. The six-month MD&A explanation of other income—net rests on the move to net gains on marketable equity securities (mdna:153). Nothing in the text says more sales are planned.",
  "account": "other income—net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "We had no sales of marketable equity securities during the second quarter of 2026 and the six months ended June 30, 2025.",
  "paragraph_id": "0001262039-26-000021:notes:33",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_real_estate_purchase_for_data_center_and_office_development",
  "what_changed": "The PP&E note states a $62.1 million purchase of U.S. real estate during the six months, for future development of data center and office space. It was accounted for as an asset acquisition: $59.5 million to land and $2.6 million to buildings and improvements. Paragraph-id alignment with the Q1 filing suggests this paragraph had no Q1 counterpart, but the Q1 PP&E wording is not in my input, so I cannot confirm it is new. The release separately adds back 'real estate related purchases' in adjusted free cash flow (8k_2_02:79).",
  "account": "property and equipment—net (land)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "During the six months ended June 30, 2026, we purchased certain real estate property in the United States totaling $62.1 million, to be used for future development to expand our data center and office space.",
  "paragraph_id": "0001262039-26-000021:notes:43",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_securities_class_action_motion_to_dismiss_filed",
  "what_changed": "Q1 said the time to respond to the consolidated amended complaint had not yet passed. Q2 replaces that with the sentence that defendants moved to dismiss on June 15, 2026. The rest stands:\n- the company still calls the action without merit;\n- it still says the outcome is uncertain and the impact cannot be estimated;\n- it still records no loss accrual as of June 30, 2026 (notes:84);\n- the claims are as in Q1, including Section 20A and the Section 10(b) claim against the head of investor relations.\nThe other edits are wording only: 'between' became 'from' for the class period, 'Officer' is lowercased, and an apostrophe was added to 'attorneys fees'. The consolidated derivative action is still stayed (notes:85).",
  "account": "accrued liabilities (litigation loss contingency)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Defendants filed a motion to dismiss the consolidated amended complaint on June 15, 2026.",
  "paragraph_id": "0001262039-26-000021:notes:83",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_subsequent_event_repurchase_note_dropped",
  "what_changed": "The Q1 10-Q had a Subsequent Event note. It said that after March 31, 2026 and through the filing date the company repurchased 1.9 million shares for $145.9 million, and that $765.8 million remained available through February 28, 2027. This 10-Q has no subsequent-events note; the change history matches the Q1 note to no current note. The repurchase note now states that $765.8 million remained available as of June 30, 2026 (notes:120). None of the text I have discloses a repurchase after June 30, 2026.",
  "account": "stockholders' equity (repurchase and retirement of common stock)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Subsequent to March 31, 2026 and through the filing of this Quarterly Report on Form 10-Q, we repurchased 1.9 million shares of our common stock at an average price of $77.95 per share, for an aggregate purchase price of $145.9 million, under the Repurchase Program.",
  "paragraph_id": "0001262039-26-000013:note_history:27",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_operating_officer_trading_plan_adopted",
  "what_changed": "New trading-arrangement disclosure. On June 5, 2026 the Chief Operating Officer adopted a Rule 10b5-1 sales plan for up to 56,700 shares, to come from exercising vested stock options. Sales are at or above a minimum price, between September 4, 2026 and September 30, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Whittle Plan provides for the potential sale by Mr. Whittle of up to 56,700 shares of our common stock, issued upon the exercise of vested stock options for shares of our common stock, at prices at or above a minimum price specified in the Whittle Plan, all between September 4, 2026 and September 30, 2027.",
  "paragraph_id": "0001262039-26-000021:notes:141",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_financial_officer_trading_plan_adopted",
  "what_changed": "New trading-arrangement disclosure. On June 10, 2026 the Chief Financial Officer adopted a Rule 10b5-1 sales plan for up to 115 shares, plus a not-yet-determinable number of net shares left after tax withholding on RSU and PSU vesting. The sales window runs from September 9, 2026 to September 15, 2027. In the same filing, the securities class action names 'our current chief financial officer' among the defendants, and the amended complaint adds a Section 20A claim (notes:83).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Ohlgart Plan provides for the potential sale by Mrs. Ohlgart of up to 115 shares of our common stock, plus a number of additional net shares (which is not yet determinable) remaining after shares are withheld to satisfy tax obligations upon vesting and settlement of RSUs and PSUs, in each case, at prices determined in accordance with the terms of the Ohlgart Plan, all between September 9, 2026 and September 15, 2027.",
  "paragraph_id": "0001262039-26-000021:notes:142",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_product_revenue_continued_growth_outlook",
  "what_changed": "The overview now covers the three and six months. It credits product revenue growth to hardware, citing higher unit shipments and 'recent pricing actions'. It also names demand for higher-performance products, AI-infrastructure deployments, technology upgrades, upsell and new use cases. It says product revenue should keep growing year over year for the rest of 2026. The Q1 wording is not in my input, so I cannot say which of these phrases are new.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect our product revenue to continue to grow year over year for the remainder of 2026 compared to the same periods of 2025.",
  "paragraph_id": "0001262039-26-000021:mdna:66",
  "explanation": false }
```

```json
{ "id": "earnings_quality_product_revenue_attributed_to_pricing_actions_and_selling_prices",
  "what_changed": "For the quarter, MD&A credits product revenue growth to three causes together: higher unit shipments, higher average selling prices from demand for higher-performing models, and recent pricing actions. The prose does not split volume from price. It does not say whether customers bought ahead of the pricing actions. The release headline figure for product revenue growth is at 8k_2_02:9.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by hardware revenue growth resulting from higher unit shipments year over year, higher average selling prices resulting from customer demand for higher-performing models and recent pricing actions",
  "paragraph_id": "0001262039-26-000021:mdna:100",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_service_revenue_from_growing_deferred_balance_and_outlook",
  "what_changed": "MD&A credits service revenue growth mainly to recognizing the growing deferred revenue balance (FortiGuard and other subscriptions, on-premise and cloud). It adds strength in unified SASE and SecOps and in FortiCare support. It says service revenue should keep growing year over year for the rest of 2026. The release sets a separate full-year service revenue range (8k_2_02:35). The Q1 wording is not in my input.",
  "account": "service revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "We expect our service revenue to continue to grow year over year for the remainder of 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:67",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_hardware_component_costs_in_gross_margin_outlook",
  "what_changed": "The full-year 2026 gross margin outlook has four parts:\n- product gross margin 'may decline' against 2025, mainly because of continued higher hardware component costs;\n- service gross margin is expected to decline slightly, from data center, colocation and cloud-hosting expansion for SASE and SecOps;\n- total margin depends on the revenue mix;\n- U.S. tariffs are not expected to have a meaningful impact, but trade-policy changes could hurt gross margin, mainly through hardware sales to U.S. customers.\nThe Q1 wording is not in my input.",
  "account": "product gross margin; service gross margin; cost of product revenue",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Our product gross margin may decline for the full year 2026 as compared to 2025 primarily due to continued higher hardware component costs.",
  "paragraph_id": "0001262039-26-000021:mdna:70",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_chip_costs_offset_product_margin",
  "what_changed": "The quarter's product gross margin explanation names two offsets to the pricing actions: increased memory-chip costs and a revenue-mix shift toward hardware. The six-month paragraph (mdna:138) uses the same words. Memory-chip cost is a named cost pressure on product cost.",
  "account": "cost of product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by recent pricing actions, partially offset by a shift in revenue mix to hardware and increased costs of memory chips",
  "paragraph_id": "0001262039-26-000021:mdna:106",
  "explanation": false }
```

```json
{ "id": "across_documents_product_gross_margin_increase_against_possible_decline_outlook",
  "what_changed": "The same MD&A makes two statements. Six-month product gross margin increased 1.4 percentage points on pricing actions (this paragraph). Full-year 2026 product gross margin 'may decline' from 2025 on continued higher hardware component costs (mdna:70). I only note that both are in the text. Reconciling them takes arithmetic, which belongs to the numbers reader and the supervisor.",
  "account": "product gross margin",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Product gross margin increased 1.4 percentage points during the six months ended June 30, 2026 compared to the same period last year",
  "paragraph_id": "0001262039-26-000021:mdna:138",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_operating_margin_slight_increase_outlook",
  "what_changed": "MD&A expects full-year 2026 operating margin to 'increase slightly' against 2025, through operating leverage and measured investments. It says expense growth will come mainly from sales and marketing headcount, product development, and continued data center and real estate investment. The release gives full-year non-GAAP operating margin guidance (8k_2_02:38). The Q1 wording is not in my input.",
  "account": "operating margin; operating expenses",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "For the full year 2026, we expect our operating margin to increase slightly compared to 2025, benefiting from operating leverage and measured investments.",
  "paragraph_id": "0001262039-26-000021:mdna:72",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_legal_fees_drive_general_and_administrative_increase",
  "what_changed": "The quarter's G&A increase is credited first to a $2.1 million increase in legal-related and other professional fees, then to personnel costs. In the same quarter, defendants moved to dismiss the securities class action (notes:83). The six-month G&A paragraph (mdna:148) also names legal fees. The text does not say which matters the fees relate to.",
  "account": "general and administrative expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to an increase of $2.1 million in legal related fees and other professional services fees and an increase of $1.5 million in personnel-related costs",
  "paragraph_id": "0001262039-26-000021:mdna:116",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_income_reduced_by_repurchases_and_debt_repayment",
  "what_changed": "MD&A credits the decrease in interest income to lower average interest rates and lower average cash balances, which the prose ties to share repurchases and debt repayment. It credits the decrease in interest expense to repaying the 2026 Senior Notes at maturity in March 2026. The six-month paragraph (mdna:153) gives the same causes. The repurchase authorization runs through February 28, 2027 (notes:120).",
  "account": "interest income",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "primarily due to lower average interest rates and lower average cash and cash equivalents balances as a result of share repurchases and debt repayment",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "earnings_quality_other_income_hit_by_foreign_exchange_losses",
  "what_changed": "MD&A credits the quarter's other income—net decrease to a $10.1 million increase in foreign currency exchange losses and a $6.3 million decrease in net gains on marketable equity securities. In the same filing, the functional-currency sentences were removed from the consolidation note (see the structure_and_disclosure_changes item), and the note says no marketable equity securities were sold in the quarter (notes:33).",
  "account": "other income—net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "primarily due to a $10.1 million increase in foreign currency exchange losses and a $6.3 million decrease in net gains on marketable equity securities",
  "paragraph_id": "0001262039-26-000021:mdna:121",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_provision_for_expected_credit_losses_increase",
  "what_changed": "The six-month G&A increase is credited first to a $1.3 million increase in the provision for expected credit losses; legal fees are named second. The prose gives no reason for the higher provision. The policies note says the company adopted the ASU 2025-05 practical expedient for estimating credit losses on current receivables on January 1, 2026, with no material impact (notes:7). The receivables-concentration table gives Distributor A's and B's shares of receivables at both dates (notes:139).",
  "account": "allowance for credit losses; accounts receivable—net; general and administrative expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to an increase of $1.3 million in provision for expected credit losses and $0.9 million in legal related fees and other professional services fees",
  "paragraph_id": "0001262039-26-000021:mdna:148",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_moodys_rating_upgrade_with_stable_outlook",
  "what_changed": "New sentence: in July 2026 Moody's upgraded certain of the company's credit ratings to A3 from Baa1 and changed the outlook to Stable from Positive. S&P stays at BBB+ with a Stable outlook. The release adds that the senior unsecured shelf rating moved to (P)A3 (8k_2_02:25). The same paragraph lists pricing actions and 'an increase in installment billings' among the factors further billings growth depends on. I cannot tell whether those phrases are new.",
  "account": "long-term debt (borrowing cost and access)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "In July 2026, Moody’s upgraded certain of our credit ratings to A3 from Baa1 and changed the outlook to Stable from Positive.",
  "paragraph_id": "0001262039-26-000021:mdna:162",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_estimate_range",
  "what_changed": "MD&A estimates full-year 2026 capital expenditures at about $350 million to $550 million. It says the company will keep increasing data center, PoP, office and warehouse capacity. The Q1 estimate is not in my input, so I cannot say whether the range changed. The PP&E note records a U.S. real estate purchase for data center and office development (notes:43).",
  "account": "purchases of property and equipment; property and equipment—net",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We estimate the full year capital expenditures to be between approximately $350 million and $550 million in 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:164",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_inventory_purchase_commitments_increase_on_demand_lead_times_and_component_cost",
  "what_changed": "MD&A states that inventory purchase commitments at June 30, 2026 rose $856.5 million from December 31, 2025. It gives the cause: working with contract manufacturers and suppliers to optimize the inventory and commitment position, based on growth trends in customer demand, product lead times and increasing component costs. Related text in the notes:\n- the commitments note states the $1.67 billion total and the liability for commitments above forecast demand at both dates (notes:79);\n- some commitments secure supply and pricing for multi-year periods (notes:78);\n- the table splits the total between 2026 and thereafter (notes:77).\nThe prose does not say how the excess-commitment liability, or the excess and obsolete inventory reserve (notes:40), was assessed against the increased commitments.",
  "account": "inventory; inventory purchase commitments; accrued liabilities (excess purchase commitment liability)",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "These inventory purchase commitments as of June 30, 2026 totaled $1.67 billion, an increase of $856.5 million compared to $810.6 million as of December 31, 2025, as we continued to work with contract manufacturers and suppliers to optimize our inventory and purchase commitments position based on growth trends in customer demand, product lead times and increasing components cost.",
  "paragraph_id": "0001262039-26-000021:mdna:168",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_attributed_to_non_current_deferred_revenue",
  "what_changed": "MD&A credits six-month operating cash flow to growth, improved profitability and 'our ability to successfully manage our working capital'. Among changes in operating assets and liabilities, it names a $354.1 million increase in non-current deferred revenue and a $240.5 million increase in deferred contract costs, mostly sales commissions. It does not name accounts receivable as a cause. The deferred revenue paragraph (mdna:83) separately states the total and short-term increases since December 31, 2025.",
  "account": "deferred revenue (non-current); net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Changes in operating assets and liabilities were primarily driven by working capital movements, as well as an increase of $354.1 million in the non-current portion of deferred revenue, and an increase of $240.5 million in deferred contract costs which primarily consisted of sales commissions during the six months ended June 30, 2026.",
  "paragraph_id": "0001262039-26-000021:mdna:179",
  "explanation": false }
```

```json
{ "id": "across_documents_fortisoc_and_sovereign_sase_offerings_added",
  "what_changed": "The MD&A business description now names two offerings:\n- FortiSOC, a unified cloud-delivered SaaS offering that combines the FortiAnalyzer, FortiSIEM and FortiSOAR capabilities (this paragraph);\n- sovereign SASE deployments on infrastructure the customer controls (mdna:48).\nThe release lists the FortiSOC launch, and the FortiGate 1200G with FortiSASE Outpost, as Q2 business highlights (8k_2_02:21, 8k_2_02:22). The Q1 MD&A wording is not in my input; the release dates both launches to this quarter.",
  "account": "service revenue (security subscription and SaaS)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "FortiSOC brings these core capabilities together in a unified cloud-delivered SaaS offering.",
  "paragraph_id": "0001262039-26-000021:mdna:49",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_results_exceeded_high_end_of_guidance",
  "what_changed": "The release headline says second-quarter revenue and profitability came in above the high end of guidance. The earlier guidance is not in my input.",
  "account": "total revenue; operating margin",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Exceeds high end of second quarter guidance on revenue and profitability",
  "paragraph_id": "0001262039-26-000018:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_revenue_guidance_raised",
  "what_changed": "The release raises 2026 revenue guidance to 19% year-over-year growth. It gives a full-year range of $8.020 billion to $8.180 billion (8k_2_02:34). The earlier guidance is not in my input.",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Raises 2026 revenue guidance to 19% year over year growth",
  "paragraph_id": "0001262039-26-000018:8k_2_02:6",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_near_term_revenue_billings_and_margin_guidance",
  "what_changed": "Third-quarter 2026 guidance:\n- revenue of $2.010 billion to $2.100 billion;\n- billings of $2.250 billion to $2.350 billion (8k_2_02:29);\n- non-GAAP gross margin of 79.0% to 81.0% (8k_2_02:30);\n- non-GAAP operating margin of 35.0% to 37.0% (8k_2_02:31);\n- non-GAAP diluted EPS of $0.83 to $0.87, at an 18% non-GAAP tax rate on 741 million to 745 million diluted shares (8k_2_02:32).\nI do not set these against any actual.",
  "account": "total revenue; billings; non-GAAP margins",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "•Revenue in the range of $2.010 billion to $2.100 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:28",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_service_revenue_guidance_range",
  "what_changed": "The release gives a full-year 2026 service revenue range of $5.180 billion to $5.220 billion, separately from total revenue. MD&A says service revenue should keep growing year over year for the rest of 2026 (mdna:67).",
  "account": "service revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "•Service revenue in the range of $5.180 billion to $5.220 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:35",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_billings_guidance_range",
  "what_changed": "The release gives full-year 2026 billings guidance of $9.350 billion to $9.550 billion. Billings are non-GAAP: revenue plus the change in deferred revenue, less acquired deferred revenue (8k_2_02:86).",
  "account": "billings; deferred revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "•Billings in the range of $9.350 billion to $9.550 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:36",
  "explanation": false }
```

```json
{ "id": "across_documents_non_gaap_margin_guidance_beside_gaap_margin_outlook",
  "what_changed": "The release gives full-year 2026 non-GAAP margin guidance: gross margin 79.0% to 81.0% (8k_2_02:37) and operating margin 35.0% to 37.0% (this paragraph). The third-quarter lines (8k_2_02:30, 8k_2_02:31) are worded identically. The 10-Q MD&A speaks on a GAAP basis, against 2025:\n- product gross margin may decline (mdna:70);\n- service gross margin is expected to decline slightly (mdna:70);\n- operating margin is expected to increase slightly (mdna:72).\nThe two documents use different bases, and neither ties the non-GAAP ranges to the GAAP direction.",
  "account": "gross margin; operating margin",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "•Non-GAAP operating margin in the range of 35.0% to 37.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:38",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_earnings_per_share_guidance_and_diluted_share_count",
  "what_changed": "The release gives full-year 2026 non-GAAP diluted EPS guidance of $3.41 to $3.47, at an 18% non-GAAP tax rate, assuming 741 million to 745 million diluted shares. The third-quarter guidance (8k_2_02:32) states the same share-count range. The repurchase note gives $765.8 million available through February 28, 2027 (notes:120).",
  "account": "diluted weighted-average shares; net income per share",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "•Diluted non-GAAP net income per share in the range of $3.41 to $3.47, assuming a non-GAAP effective tax rate of 18%.",
  "paragraph_id": "0001262039-26-000018:8k_2_02:39",
  "explanation": false }
```

```json
{ "id": "across_documents_intel_security_processor_collaboration_for_supply_chain",
  "what_changed": "The release announces a strategic collaboration with Intel to develop the SP6 security processor. It uses Intel's design, development, packaging and manufacturing capabilities to speed SP6 development and to strengthen the 'resilience and diversity' of the supply chain. None of the 10-Q text in my input mentions Intel or a change in chip supply: not the notes, not Item 4, and not the MD&A paragraphs carried as text. The MD&A paragraphs marked same-as-prior are not visible to me. The commitments note describes multi-year supply and pricing arrangements without naming counterparties (notes:78).",
  "account": "inventory purchase commitments; research and development",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "•Announced a strategic collaboration with Intel to develop Fortinet Security Processor 6 (SP6)",
  "paragraph_id": "0001262039-26-000018:8k_2_02:20",
  "explanation": false }
```

```json
{ "id": "across_documents_adjusted_free_cash_flow_adds_back_real_estate_purchases",
  "what_changed": "The release defines adjusted free cash flow as free cash flow plus cash payments for real estate purchases. It reports a Q2 'Real estate related purchases' add-back and an adjusted margin (8k_2_02:79). The 10-Q MD&A defines and reconciles free cash flow only (mdna:88, mdna:89) and has no adjusted measure. No earlier release is in my input, so I cannot tell whether the measure is new.",
  "account": "purchases of property and equipment; free cash flow (non-GAAP)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Adjusted free cash flow (non-GAAP). We define adjusted free cash flow as free cash flow plus cash payments associated with real estate related purchases.",
  "paragraph_id": "0001262039-26-000018:8k_2_02:88",
  "explanation": false }
```

## Paragraphs carried as text that are not items

The list below covers every carried-as-text paragraph not chosen as an item's `paragraph_id`. Where a paragraph is folded into an item, the line names the item.

**Labels used in the list:**
- **amounts only:** the same statement, with figures or the period updated.
- **date rolled forward:** only the period changed.
- **page break:** the paragraph boundary moved; no change in substance is visible.
- **insufficient:** the paragraph is carried as text, but I cannot see what changed.

### Notes (0001262039-26-000021:notes:…)

- notes:1 — date rolled forward (three months to March 31 → three and six months to June 30)
- notes:2 — folded into structure_and_disclosure_changes_functional_currency_transition_sentences_removed (the current, shortened paragraph)
- notes:4 — date rolled forward
- notes:7 — insufficient: the ASU 2025-05 adoption paragraph shows no change in the change history and Q1 wording is not visible; referenced in the credit-loss item
- notes:10 — insufficient: ASU 2024-03 paragraph; no change in the change history
- notes:12 — insufficient: ASU 2025-06 paragraph; no change in the change history
- notes:15 — amounts only (the table adds six-month columns)
- notes:17 — amounts only, date rolled forward (revenue from opening deferred revenue)
- notes:19 — amounts only, date rolled forward (remaining performance obligations and their timing)
- notes:21 — amounts only (deferred contract cost amortization)
- notes:23 — insufficient: investments intro sentence; this tag is not covered by the change history
- notes:24 — amounts only (table)
- notes:27 — amounts only (table)
- notes:30 — amounts only (table)
- notes:36 — amounts only (table)
- notes:37 — date rolled forward (no Level 1/2 transfers)
- notes:39 — amounts only (table)
- notes:40 — amounts only, date rolled forward (E&O reserve; write-downs not material; no cause given); referenced in the commitments item
- notes:42 — amounts only (table)
- notes:44 — amounts only (depreciation)
- notes:48 — page break (continues at notes:49); Linksys accounting from 2025
- notes:49 — page break continuation of notes:48
- notes:53 — insufficient: acquisitions not material; this tag is not covered by the change history
- notes:55 — date rolled forward (goodwill; no impairments)
- notes:58 — amounts only (table)
- notes:60 — amounts only (amortization)
- notes:62 — amounts only (table)
- notes:65 — amounts only (table)
- notes:67 — amounts only (table)
- notes:68 — insufficient: debt heading; no change in the change history
- notes:69 — insufficient: Senior Notes issuance terms; no change in the change history
- notes:70 — insufficient: 2026 notes repaid at maturity (a Q1 event); no change in the change history
- notes:71 — insufficient: 2031 notes redemption and interest terms; no change in the change history
- notes:72 — insufficient: table caption; no change in the change history
- notes:73 — amounts only (debt table)
- notes:74 — amounts only, date rolled forward (adds six-month interest expense)
- notes:75 — amounts only (2031 notes fair value)
- notes:76 — date rolled forward (commitments heading)
- notes:77 — amounts only (commitments table); referenced in the commitments item
- notes:78 — insufficient: commitment terms, including multi-year supply and pricing; no change in the change history; referenced in the commitments and Intel items
- notes:79 — amounts only, date rolled forward; folded into the commitments item. Q1 mentioned a $4.5 million benefit for Q1 2025; with three- and six-month comparatives, both 2025 periods are now 'not material'.
- notes:80 — amounts only; 'consist' → 'consists'
- notes:81 — amounts only (operating lease commitments)
- notes:82 — date rolled forward (litigation accruals not material)
- notes:84 — date rolled forward (no class-action loss accrual)
- notes:85 — wording only ('et. seq.' → 'et seq.')
- notes:86 — date rolled forward (Alorica)
- notes:87 — insufficient: indemnification; no change in the change history
- notes:88 — insufficient: cybersecurity incidents; no change in the change history
- notes:90 — amounts only, date rolled forward (shares available for grant)
- notes:93 — amounts only (table)
- notes:96 — amounts only, date rolled forward (PSU grants)
- notes:97 — amounts only (table)
- notes:98 — amounts only, date rolled forward
- notes:99 — amounts only (unrecognized compensation)
- notes:100 — page break (continues at notes:101)
- notes:101 — page break continuation of notes:100
- notes:103 — amounts only (table)
- notes:106 — amounts only (table)
- notes:108 — amounts only (table)
- notes:109 — amounts only
- notes:111 — amounts only (table)
- notes:114 — amounts only (table)
- notes:116 — amounts only (table)
- notes:118 — amounts only (table)
- notes:120 — amounts only, date rolled forward (repurchases; excise-tax accrual); referenced in the subsequent-event and EPS-guidance items
- notes:121 — amounts only; page break (continues at notes:122)
- notes:122 — amounts only (continuation)
- notes:123 — amounts only (six-month tax)
- notes:124 — date rolled forward (One Big Beautiful Bill Act effects recognized)
- notes:125 — amounts only (unrecognized tax benefits, interest and penalties)
- notes:126 — insufficient: tax audit jurisdictions; this tag is not covered by the change history
- notes:127 — date rolled forward (Pillar Two: no impact for the six months)
- notes:128 — insufficient: segment intro; this tag is not covered by the change history
- notes:130 — amounts only (table)
- notes:134 — amounts only (table)
- notes:135 — amounts only (table)
- notes:137 — amounts only (table)
- notes:139 — amounts only (receivables concentration table); referenced in the credit-loss item

### MD&A (0001262039-26-000021:mdna:…)

- mdna:7 — insufficient: forward-looking factor bullet (tariffs, wars, natural disasters); Q1 wording not visible
- mdna:20 — page number
- mdna:28 — insufficient: forward-looking bullet on litigation outcomes and liabilities; Q1 wording not visible
- mdna:34 — date rolled forward; patent counts (amounts only)
- mdna:37 — page number
- mdna:38 — page break continuation of the FortiOS product description
- mdna:41 — insufficient: FortiAI product description; Q1 wording not visible
- mdna:44 — insufficient: "three solution pillars" lead-in; Q1 wording not visible
- mdna:45 — page break (continues at mdna:47); Secure Networking product description
- mdna:46 — page number
- mdna:47 — page break continuation of mdna:45
- mdna:48 — folded into across_documents_fortisoc_and_sovereign_sase_offerings_added (sovereign SASE)
- mdna:50 — insufficient: FortiGuard Labs description; Q1 wording not visible
- mdna:53 — insufficient: Advanced Support options (paragraph truncated in input); Q1 wording not visible
- mdna:55 — insufficient: Training Institute certification count; Q1 wording not visible
- mdna:57 — amounts only (revenue overview)
- mdna:58 — amounts only (gross profit)
- mdna:59 — amounts only (gross margin)
- mdna:60 — amounts only (operating income)
- mdna:61 — amounts only (operating margin)
- mdna:62 — amounts only (cash and investments)
- mdna:63 — amounts only (deferred revenue)
- mdna:64 — amounts only (operating cash flow)
- mdna:65 — amounts only (regional mix and growth)
- mdna:68 — page number
- mdna:69 — amounts only (billings country concentration)
- mdna:71 — amounts only (opex ratio; headcount)
- mdna:77 — insufficient: sales channels, including third-party cloud platforms; Q1 wording not visible
- mdna:82 — amounts only (table)
- mdna:83 — amounts only (deferred revenue changes since December 31, 2025); referenced in the operating-cash-flow item
- mdna:84 — amounts only (the quarter's billings; definition unchanged in kind)
- mdna:85 — page number
- mdna:87 — amounts only (table)
- mdna:88 — insufficient: free cash flow definition; Q1 wording not visible; referenced in the adjusted-FCF item
- mdna:89 — amounts only (table); referenced in the adjusted-FCF item
- mdna:92 — date rolled forward (no change to critical accounting estimates)
- mdna:96 — heading, date
- mdna:98 — amounts only (table)
- mdna:99 — amounts only (total revenue; EMEA named as largest contributor)
- mdna:101 — amounts only; same causes as the itemized mdna:67
- mdna:102 — amounts only (share of service revenue from opening deferred revenue)
- mdna:104 — amounts only (table)
- mdna:105 — amounts only; mix cause as in the itemized mdna:70
- mdna:107 — amounts only; data center and cloud cost cause as in the itemized mdna:70
- mdna:109 — amounts only (table)
- mdna:111 — amounts only; routine R&D outlook (rises in absolute dollars)
- mdna:112 — page number
- mdna:114 — amounts only; routine sales and marketing outlook
- mdna:118 — amounts only (operating margin bridge)
- mdna:120 — amounts only (table)
- mdna:123 — amounts only (table)
- mdna:124 — amounts only (quarter tax; FDDEI; excess tax benefits)
- mdna:125 — page number
- mdna:126 — amounts only (prior-year quarter tax)
- mdna:127 — heading (the six-month section, standard in a second-quarter report)
- mdna:128 — heading
- mdna:129 — amounts only (table)
- mdna:130 — amounts only
- mdna:131 — amounts only; causes as in the itemized mdna:66 and mdna:100
- mdna:132 — amounts only; causes as in mdna:67
- mdna:133 — amounts only
- mdna:134 — page number
- mdna:135 — heading
- mdna:136 — amounts only (table)
- mdna:137 — amounts only; mix cause
- mdna:139 — amounts only (service gross margin flat)
- mdna:140 — heading
- mdna:141 — amounts only (table)
- mdna:142 — heading
- mdna:143 — amounts only
- mdna:144 — page number
- mdna:145 — heading
- mdna:146 — amounts only (personnel; marketing programs)
- mdna:147 — heading
- mdna:149 — heading
- mdna:150 — amounts only (six-month operating margin bridge)
- mdna:151 — heading
- mdna:152 — amounts only (table)
- mdna:153 — amounts only. Its causes are folded into the items from notes:33 and mdna:121: equity-securities gains, the prior-year Linksys bargain-purchase gain, and foreign exchange losses.
- mdna:154 — heading
- mdna:155 — amounts only (table)
- mdna:156 — amounts only (six-month tax)
- mdna:157 — page number
- mdna:158 — amounts only (prior-year six-month tax; Linksys deferred tax asset derecognition)
- mdna:160 — amounts only (table)
- mdna:163 — amounts only, date rolled forward (repurchase program; same facts as notes:120)
- mdna:165 — page number
- mdna:166 — amounts only, date rolled forward (2026 notes repaid in Q1; 2031 notes outstanding)
- mdna:170 — amounts only (other contractual commitments)
- mdna:172 — amounts only, date rolled forward (liquidity sufficiency statement)
- mdna:173 — amounts only (cash held by international subsidiaries)
- mdna:174 — insufficient: long-term liquidity factors (names pricing actions and tariffs); Q1 wording not visible
- mdna:175 — page number
- mdna:176 — date rolled forward (no off-balance-sheet arrangements)
- mdna:182 — amounts only (investing activities)
- mdna:185 — amounts only (financing activities)

### Item 4 (0001262039-26-000021:item_4_controls:…)

- item_4_controls:1 — heading
- item_4_controls:2 — heading
- item_4_controls:3 — standard evaluation text, date rolled forward
- item_4_controls:4 — date rolled forward; disclosure controls still concluded effective
- item_4_controls:5 — heading
- item_4_controls:6 — date rolled forward; still no ICFR change in the quarter
- item_4_controls:7 — page number

### 8-K item 2.02, exhibit 99.1 (0001262039-26-000018:8k_2_02:…)

- 8k_2_02:1 — exhibit cover header
- 8k_2_02:2 — header
- 8k_2_02:3 — header
- 8k_2_02:4 — headline; its claims are itemized at :5 and :6
- 8k_2_02:7 — heading
- 8k_2_02:8 — amounts only (revenue)
- 8k_2_02:9 — amounts only (product revenue); referenced in the pricing item
- 8k_2_02:10 — amounts only (billings)
- 8k_2_02:11 — amounts only (GAAP operating margin)
- 8k_2_02:12 — amounts only (non-GAAP operating margin)
- 8k_2_02:13 — amounts only (GAAP EPS)
- 8k_2_02:14 — amounts only (non-GAAP EPS)
- 8k_2_02:15 — amounts only (operating cash flow)
- 8k_2_02:16 — amounts only (free cash flow)
- 8k_2_02:17 — dateline
- 8k_2_02:18 — CEO quote; product positioning, with no account, amount or commitment
- 8k_2_02:19 — heading
- 8k_2_02:21 — folded into across_documents_fortisoc_and_sovereign_sase_offerings_added (FortiGate 1200G / FortiSASE Outpost)
- 8k_2_02:22 — folded into across_documents_fortisoc_and_sovereign_sase_offerings_added (FortiSOC launch)
- 8k_2_02:23 — product announcement (FortiEndpoint); no account, amount or commitment
- 8k_2_02:24 — partnership announcements (Anthropic, OpenAI, NVIDIA); no financial terms
- 8k_2_02:25 — folded into liquidity_and_capital_moodys_rating_upgrade_with_stable_outlook
- 8k_2_02:26 — heading
- 8k_2_02:27 — heading
- 8k_2_02:29 — folded into results_against_expectations_near_term_revenue_billings_and_margin_guidance (billings)
- 8k_2_02:30 — folded into the same item (gross margin)
- 8k_2_02:31 — folded into the same item (operating margin)
- 8k_2_02:32 — folded into the same item (EPS, tax rate, share count)
- 8k_2_02:33 — heading
- 8k_2_02:34 — folded into results_against_expectations_revenue_guidance_raised (the full-year range)
- 8k_2_02:37 — folded into across_documents_non_gaap_margin_guidance_beside_gaap_margin_outlook (gross margin range)
- 8k_2_02:40 — boilerplate: what non-GAAP guidance excludes; no earlier release in input to compare
- 8k_2_02:41 — heading
- 8k_2_02:42 — call logistics
- 8k_2_02:43 — heading
- 8k_2_02:44 — conference name
- 8k_2_02:45 — conference date
- 8k_2_02:46 — conference name
- 8k_2_02:47 — conference date
- 8k_2_02:48 — conference name
- 8k_2_02:49 — conference date
- 8k_2_02:50 — conference name
- 8k_2_02:51 — conference date
- 8k_2_02:52 — conference name
- 8k_2_02:53 — conference date
- 8k_2_02:54 — boilerplate (webcasts)
- 8k_2_02:55 — heading
- 8k_2_02:56 — company boilerplate
- 8k_2_02:57 — heading
- 8k_2_02:58 — forward-looking boilerplate (truncated in input)
- 8k_2_02:59 — heading
- 8k_2_02:60 — boilerplate
- 8k_2_02:61 — header
- 8k_2_02:62 — header
- 8k_2_02:63 — header
- 8k_2_02:64 — amounts only (balance sheet)
- 8k_2_02:65 — header
- 8k_2_02:66 — header
- 8k_2_02:67 — header
- 8k_2_02:68 — amounts only (income statement)
- 8k_2_02:69 — header
- 8k_2_02:70 — header
- 8k_2_02:71 — header
- 8k_2_02:72 — amounts only (cash flow statement)
- 8k_2_02:73 — heading
- 8k_2_02:74 — header
- 8k_2_02:75 — heading
- 8k_2_02:76 — amounts only (non-GAAP reconciliation)
- 8k_2_02:77 — footnote: 18% non-GAAP tax rate; boilerplate
- 8k_2_02:78 — heading
- 8k_2_02:79 — amounts only (free cash flow reconciliation); the adjusted-FCF line is folded into across_documents_adjusted_free_cash_flow_adds_back_real_estate_purchases
- 8k_2_02:80 — heading
- 8k_2_02:81 — amounts only (billings reconciliation)
- 8k_2_02:82 — footnote boilerplate
- 8k_2_02:83 — heading
- 8k_2_02:84 — non-GAAP boilerplate
- 8k_2_02:85 — non-GAAP boilerplate
- 8k_2_02:86 — billings definition; the same text MD&A gives at mdna:84
- 8k_2_02:87 — free cash flow definition; boilerplate
- 8k_2_02:89 — non-GAAP gross margin definition; boilerplate
- 8k_2_02:90 — non-GAAP operating income definition; boilerplate
- 8k_2_02:91 — non-GAAP boilerplate
- 8k_2_02:92 — non-GAAP net income definition; boilerplate
- 8k_2_02:93 — separator
- 8k_2_02:94 — trademark boilerplate
- 8k_2_02:95 — filing code
- 8k_2_02:96 — contacts

## Observations with no current paragraph

- **Inventory note alignment (insufficient):** current notes:39–40 sit where Q1 had 13:notes:39–41. Either a Q1 paragraph was split across a page or one was dropped. The Q1 inventory text is not in my input.
- **8-K index:** the filings after the Q1 10-Q are item 5.07 (2026-06-16) and items 2.02/9.01 (2026-07-29). The index shows no late-filing notification on or before 2026-07-30, and the period has no item 4.01, 4.02 or 5.02 filing. The 5.07 body is not in my input.

## Counts

- Items: 32. One has `explanation: true` (the inventory purchase commitments item, from mdna:168).
- Paragraphs marked insufficient: 25 (15 in the notes, 10 in MD&A). One more insufficient observation, the inventory note alignment, has no current paragraph.
