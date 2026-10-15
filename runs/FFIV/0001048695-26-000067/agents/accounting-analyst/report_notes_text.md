<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# FFIV notes-text reader — 0001048695-26-000067 (10-Q, quarter ended June 30, 2026)

## Inputs read

- `input_notes.md` — notes after the diff layer, read in full (paragraphs notes:1 to notes:131).
- `input_notes_history.md` — note change history, 0001048695-26-000051 to 0001048695-26-000067. Used only to see what changed in the contingencies, accounting-policies, debt and revenue blocks. It is not reported as a separate list.
- `input_mdna.md` — MD&A after the diff layer, read in full (mdna:1 to mdna:57). The prior-period MD&A wording is not in my input, so for MD&A paragraphs carried as text I report what the text now says.
- `input_controls.md` — Item 4 only (item_4_controls:1 to :6). This is a 10-Q, so there is no auditor's report in the input.
- `input_8k.md` — the 8-K item index and the Item 2.02 earnings release body of 0001048695-26-000063 (8k_2_02:1 to :68). It holds no late-filing notifications. No other 8-K body is carried.
- `input_prior_predictions.md` — none on record.
- Not in my directory: an Item 1A diff, an Exhibit 21 diff, or any Exhibit 10. I did not find anything forbidden in the directory: no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window. The 8-K exhibit's own financial statements are part of the 8-K body.

Counts: 49 items. 5 are marked `insufficient`. 3 have `explanation: true`.

## Items

```json
[
{
    "id": "revenue_recognition_deferred_revenue_growth_attributed_to_systems_maintenance_and_subscriptions",
    "what_changed": "MD&A now says deferred revenue was $2.2 billion at June 30, 2026, against $2.0 billion at September 30, 2025. It says the increase came mainly from maintenance contracts tied to strong systems shipments, plus subscription deferrals. This ties the deferred revenue build to the systems revenue growth the release headlines. The rollforward in notes:16 is for the numbers reader to reconcile against this attribution.",
    "account": "deferred revenue (current and long-term)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Deferred revenues increased to $2.2 billion as of June 30, 2026 from $2.0 billion as of September 30, 2025 primarily due to an increase in maintenance contracts related to strong systems shipments, in addition to an increase in deferred revenue associated with our subscription offerings.",
    "paragraph_id": "0001048695-26-000067:mdna:10",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "structure_and_disclosure_changes_deferred_revenue_rollforward_acquired_balance_line",
    "what_changed": "The deferred revenue rollforward has a new line, 'Deferred revenue acquired through acquisition of businesses'. It is filled in for the current nine months only. The prior six-month rollforward had no such line (history note_history:16). It ties to the SurePath acquisition (notes:34), which the note otherwise calls not material.",
    "account": "deferred revenue (current and long-term)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Deferred revenue acquired through acquisition of businesses",
    "paragraph_id": "0001048695-26-000067:notes:16",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "revenue_recognition_remaining_performance_obligations_timing_estimate",
    "what_changed": "The timing estimate for remaining performance obligations was restated. The note now gives RPO of $2.2 billion at June 30, 2026, with 58.8% expected to be recognized over the next 12 months and 24.9% in year two. The prior note gave $2.1 billion at March 31, 2026, with 59.9% and 24.2%. The prose gives no direction. Whether the recognition profile shifted is for the numbers reader.",
    "account": "remaining performance obligations; deferred revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, the total non-cancelable remaining performance obligations under the Company's contracts with customers was $2.2 billion and the Company expects to recognize revenues on 58.8% of these remaining performance obligations over the next 12 months, 24.9% in year two, and the remaining balance thereafter.",
    "paragraph_id": "0001048695-26-000067:notes:18",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_product_revenue_growth_systems_and_software",
    "what_changed": "MD&A says product revenue increased 19.0% for the three months and 17.3% for the nine months. It attributes this to systems and software. The release uses the same growth figure in its headline (8k_2_02:5, 8k_2_02:8).",
    "account": "net product revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net product revenues increased 19.0% and 17.3% for the three and nine months ended June 30, 2026, respectively, from the comparable periods in the prior year. The increase in net product revenues for the three and nine months ended June 30, 2026 was due to an increase in revenues associated with systems and software.",
    "paragraph_id": "0001048695-26-000067:mdna:23",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_service_revenue_maintenance_contracts",
    "what_changed": "MD&A says service revenue increased 2.7% in both the three- and nine-month periods. It attributes this mainly to increased sales of maintenance contracts.",
    "account": "net service revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in net service revenues for the three and nine months ended June 30, 2026 was primarily the result of increased sales of maintenance contracts.",
    "paragraph_id": "0001048695-26-000067:mdna:24",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "revenue_recognition_systems_revenue_attributed_to_customer_demand",
    "what_changed": "MD&A says systems revenue increased 32.4% for the three months and 31.6% for the nine months. The only cause it names is increases in customer demand. It names no pricing, mix, backlog or shipment-timing factor. The inventory build in notes:50 (table only) and the purchase-commitment text (mdna:56, notes:81) sit alongside this claim, but no changed prose links them.",
    "account": "systems revenue (net product revenues)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Total systems revenue increased 32.4% and 31.6% for the three and nine months ended June 30, 2026, respectively, from the comparable periods in the prior year. The increase in systems revenue was primarily due to increases in customer demand.",
    "paragraph_id": "0001048695-26-000067:mdna:27",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "revenue_recognition_software_revenue_attributed_to_subscription_offerings",
    "what_changed": "MD&A says software revenue increased 7.4% for the three months and 4.3% for the nine months. It attributes this mainly to increased sales of subscription offerings. Unbilled receivables, current and non-current, appear only as table amounts (notes:53, notes:56). No changed prose explains them.",
    "account": "software revenue (net product revenues); unbilled receivables",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Total software revenue increased 7.4% and 4.3% for the three and nine months ended June 30, 2026, respectively, from the comparable periods in the prior year. The increase in software revenue was primarily due to increased sales of subscription offerings.",
    "paragraph_id": "0001048695-26-000067:mdna:27",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_cost_of_product_revenue_attributed_to_systems_growth",
    "what_changed": "MD&A says cost of product revenue increased $4.7 million (5.3%) for the three months and $23.8 million (9.4%) for the nine months. It attributes this mainly to systems revenue growth. The cost definition in the same paragraph lists provisions for excess and obsolete inventory. No provision amount or change is discussed.",
    "account": "cost of net product revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Cost of net product revenues increased $4.7 million, or 5.3% for the three months ended June 30, 2026 and increased $23.8 million, or 9.4% for the nine months ended June 30, 2026 from the comparable periods in the prior year primarily due to systems revenue growth.",
    "paragraph_id": "0001048695-26-000067:mdna:35",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_cost_of_service_revenue_personnel_and_technology",
    "what_changed": "MD&A says cost of service revenue increased $0.2 million (0.4%) for the three months and $2.4 million (1.4%) for the nine months. It attributes this mainly to personnel and technology costs.",
    "account": "cost of net service revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in cost of net service revenues was primarily due to an increase in personnel and technology costs.",
    "paragraph_id": "0001048695-26-000067:mdna:36",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_sales_and_marketing_personnel_costs",
    "what_changed": "MD&A says sales and marketing expense increased $17.6 million (8.0%) for the three months and $57.7 million (9.0%) for the nine months. It says this was mainly personnel costs: $13.5 million and $47.0 million.",
    "account": "sales and marketing expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in sales and marketing expense for the three and nine months ended June 30, 2026 was primarily due to an increase of $13.5 million and $47.0 million, respectively, in personnel costs from the comparable periods in the prior year.",
    "paragraph_id": "0001048695-26-000067:mdna:38",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_research_and_development_technology_and_personnel_costs",
    "what_changed": "MD&A says R&D increased $28.3 million (20.8%) for the three months and $53.4 million (13.2%) for the nine months. It names technology costs first ($13.5 million and $22.7 million), then personnel costs ($10.9 million and $19.5 million).",
    "account": "research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in research and development expenses for the three and nine months ended June 30, 2026 was primarily due to an increase in technology costs of $13.5 million and $22.7 million, respectively, and an increase in personnel costs of $10.9 million and $19.5 million, respectively, from the comparable periods in the prior year.",
    "paragraph_id": "0001048695-26-000067:mdna:39",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "earnings_quality_cyber_incident_professional_services_in_research_and_development",
    "what_changed": "MD&A says professional services expense within R&D increased $2.6 million (three months) and $10.2 million (nine months), driven by Cyber Incident response costs. Two other documents state cyber amounts. The note (notes:96) gives total cyber costs for the three and nine months. The release reconciliation (8k_2_02:67) adds cyber costs back in both gross profit and operating income. How the R&D and G&A attributions tie to those totals is for the numbers reader.",
    "account": "research and development expense; cyber incident costs",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In addition, expenses for professional services increased $2.6 million and $10.2 million, driven by costs incurred in response to the Cyber Incident, for the three and nine months ended June 30, 2026, respectively, from the comparable periods in the prior year.",
    "paragraph_id": "0001048695-26-000067:mdna:39",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_general_and_administrative_personnel_costs",
    "what_changed": "MD&A says G&A increased $16.9 million (21.5%) for the three months and $49.5 million (21.7%) for the nine months. It says this was mainly personnel costs: $11.7 million and $29.7 million. The G&A definition in the same paragraph lists bad debt charges. No bad-debt amount or change is discussed.",
    "account": "general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in general and administrative expenses for the three and nine months ended June 30, 2026 was primarily due to an increase in personnel costs of $11.7 million and $29.7 million, respectively, from the comparable periods in the prior year.",
    "paragraph_id": "0001048695-26-000067:mdna:40",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "earnings_quality_cyber_incident_professional_services_in_general_and_administrative",
    "what_changed": "MD&A says professional services expense within G&A increased $3.2 million (three months) and $15.3 million (nine months), driven by Cyber Incident response costs. Read this with the R&D attribution (mdna:39), the note's total cyber costs (notes:96) and the release reconciliation (8k_2_02:67). The tie between them is for the numbers reader.",
    "account": "general and administrative expense; cyber incident costs",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In addition, expenses for professional services increased $3.2 million and $15.3 million, driven by costs incurred in response to the Cyber Incident, for the three and nine months ended June 30, 2026, respectively, from the comparable periods in the prior year.",
    "paragraph_id": "0001048695-26-000067:mdna:40",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "across_documents_other_income_explanation_omits_cyber_insurance_recoveries",
    "what_changed": "MD&A says the change in other income, net was driven mainly by interest income and expense, investment income and foreign currency gains and losses. The note now says $5.3 million of Cyber Incident insurance recoveries were received this quarter and recorded in other income, net (notes:96). The release adds those recoveries as a new non-GAAP adjustment (8k_2_02:38, 8k_2_02:67). The MD&A explanation of other income does not name the recoveries. The MD&A prose gives no direction for the line.",
    "account": "other income, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The change in other income, net for the three and nine months ended June 30, 2026 compared to the same periods in the prior year was primarily driven by interest income and expense, investment income, and foreign currency transaction gains and losses.",
    "paragraph_id": "0001048695-26-000067:mdna:43",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "estimates_and_discretion_deferred_tax_asset_valuation_allowance",
    "what_changed": "MD&A gives net deferred tax assets of $485.2 million (June 30, 2026) and $444.5 million (September 30, 2025). It gives valuation allowances of $34.8 million and $34.3 million at the same dates. It explains that the allowance relates mainly to certain state and foreign net operating losses and tax credit carryforwards. That is management explaining what a reserve consists of. The prose gives no direction.",
    "account": "deferred tax assets; valuation allowance",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The net deferred tax assets include valuation allowances of $34.8 million and $34.3 million as of June 30, 2026 and September 30, 2025, respectively, which are primarily related to certain state and foreign net operating losses and tax credit carryforwards.",
    "paragraph_id": "0001048695-26-000067:mdna:44",
    "explanation": true,
    "insufficient": false
  },
{
    "id": "liquidity_and_capital_nine_month_cash_sources_and_uses_including_acquisition",
    "what_changed": "MD&A's liquidity summary names operating cash of $841.4 million as the source. As uses it names capex of $63.7 million, repurchases of $501.1 million and 'cash used in acquisition of a business of $47.6 million'; the acquisition is SurePath (notes:34). It repeats that net income from operations will remain the main driver of cash flows and that acquisitions may require cash.",
    "account": "cash and cash equivalents; investments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in cash and investments for the first nine months of fiscal year 2026 was primarily due to cash provided by operating activities of $841.4 million, partially offset by purchases of property and equipment of $63.7 million, cash used to repurchase outstanding common stock under our stock repurchase program, including excise taxes, of $501.1 million, and cash used in acquisition of a business of $47.6 million.",
    "paragraph_id": "0001048695-26-000067:mdna:9",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "liquidity_and_capital_cash_and_investments_balance_increase",
    "what_changed": "MD&A gives cash, cash equivalents and investments of $1,627.8 million at June 30, 2026 and $1,360.0 million at September 30, 2025. It describes this as an increase of $267.8 million, attributed to operating cash, partly offset by repurchases.",
    "account": "cash and cash equivalents; short-term and long-term investments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Cash and cash equivalents, short-term investments, and long-term investments totaled $1,627.8 million as of June 30, 2026, compared to $1,360.0 million as of September 30, 2025, representing an increase of $267.8 million.",
    "paragraph_id": "0001048695-26-000067:mdna:48",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "liquidity_and_capital_operating_cash_flow_attributed_to_collections",
    "what_changed": "MD&A says nine-month operating cash flow increased over the prior-year period mainly because of business growth 'as reflected by increases in collections'. The stated cause is a receivables-side claim (collections). The numbers reader should test it against the accounts receivable, unbilled receivables and deferred revenue movements.",
    "account": "net cash provided by operating activities; accounts receivable; unbilled receivables",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Cash provided by operating activities for the first nine months of fiscal year 2026 increased from the comparable period in the prior year primarily due to growth of our business as reflected by increases in collections during the nine months ended June 30, 2026.",
    "paragraph_id": "0001048695-26-000067:mdna:49",
    "explanation": true,
    "insufficient": false
  },
{
    "id": "liquidity_and_capital_investing_cash_capital_expenditures_and_acquisition",
    "what_changed": "MD&A says nine-month investing cash of $114.2 million was mainly $47.6 million for the acquisition of a business and $63.7 million of capital expenditures. It describes the capex as 'related to maintaining our operations worldwide'. Capex additions imply additions to property and equipment. The geographic PP&E table (notes:124) is amounts only.",
    "account": "property and equipment, net; purchases of property and equipment",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The amount of cash used in investing activities for the nine months ended June 30, 2026 was primarily the result of $47.6 million used in the acquisition of a business and $63.7 million in capital expenditures related to maintaining our operations worldwide.",
    "paragraph_id": "0001048695-26-000067:mdna:51",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "liquidity_and_capital_financing_cash_share_repurchases",
    "what_changed": "MD&A says nine-month financing cash of $464.2 million was mainly $501.1 million of share repurchases including excise taxes. It also names $22.7 million of taxes on net share settlement, partly offset by $59.6 million from option exercises and ESPP. The note gives $422.4 million of authorization remaining (notes:105).",
    "account": "common stock; shares outstanding",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Our financing activities for the nine months ended June 30, 2026 primarily consisted of $501.1 million of cash used to repurchase shares of common stock and the payment of related excise taxes.",
    "paragraph_id": "0001048695-26-000067:mdna:52",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "across_documents_purchase_obligation_named_as_principal_commitment_while_none_remain",
    "what_changed": "The MD&A and notes disagree on the purchase commitment. MD&A lists, among principal commitments at June 30, 2026, 'purchase obligations with one of our component suppliers'. Yet two paragraphs later MD&A (mdna:56) says, as does the note (notes:81), that there were no remaining purchase commitments under the fourth year of the October 2022 agreement. The same passages say there were no non-cancelable long-term purchase commitments at June 30, 2026. The two statements are in tension. Neither paragraph reconciles them.",
    "account": "purchase commitments (off-balance-sheet)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, our principal commitments consisted of obligations outstanding under operating leases and purchase obligations with one of our component suppliers.",
    "paragraph_id": "0001048695-26-000067:mdna:54",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "narrative_signs_of_operating_pressure_component_price_increases_and_supply_constraints",
    "what_changed": "INSUFFICIENT. This paragraph is carried as changed, but the prior MD&A wording is not in my input, so the edit cannot be isolated. It now lists inventory obsolescence, component price increases and global supply chain constraints among factors that could significantly impact gross margins. Its cost list includes hardware costs paid to contract manufacturers and third-party cloud hosting. If 'component price increases' is the new phrase, it is a narrative sign of input-cost pressure on product margins.",
    "account": "gross margin; cost of net product revenues; inventories",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "In addition, factors such as sales price, product and services mix, inventory obsolescence, returns, component price increases, warranty costs, and global supply chain constraints could significantly impact our gross margins.",
    "paragraph_id": "0001048695-26-000067:mdna:7",
    "explanation": false,
    "insufficient": true
  },
{
    "id": "structure_and_disclosure_changes_revenue_description_paragraph_revised",
    "what_changed": "INSUFFICIENT. This paragraph is carried as changed, but the prior MD&A wording is not in my input. It describes three offerings. BIG-IP software is sold on subscription and perpetual license bases. NGINX is sold on subscription as deployable software or SaaS. Distributed Cloud Services are sold on subscription under a unified SaaS platform and managed service platform. I cannot tell which phrase is new. A change in how offerings are described could bear on the split between point-in-time and ratable revenue.",
    "account": "net product revenues (software)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "F5 Distributed Cloud Services are offered on a subscription basis, under a unified SaaS platform and managed service platform.",
    "paragraph_id": "0001048695-26-000067:mdna:5",
    "explanation": false,
    "insufficient": true
  },
{
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_no_material_impact",
    "what_changed": "The note's conclusion on the income tax disclosure standard has changed. Before, the company said it was 'currently evaluating the impact of this standard on its disclosures'. Now it says it does not expect adoption to have a material impact on the consolidated financial statements. The note gives the effective date as annual periods beginning after December 15, 2024.",
    "account": "income tax disclosures",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We do not expect the adoption of this standard will have a material impact on the consolidated financial statements.",
    "paragraph_id": "0001048695-26-000067:notes:7",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "structure_and_disclosure_changes_surepath_acquisition_goodwill",
    "what_changed": "New disclosure: SurePath AI, Inc. was acquired on June 15, 2026 for $50.1 million. It will be integrated into the F5 AI Security Platform. $39.1 million of goodwill was recorded. Acquired assets and liabilities, and the effect on operating results, are called not material. The note does not say the consideration was cash, whereas the CalypsoAI paragraph says 'in cash'. MD&A states 'cash used in acquisition of a business of $47.6 million', and the cash flow line reads 'net of cash acquired'. Tying these together is for the numbers reader. Acquired deferred revenue appears as a new rollforward line (notes:16).",
    "account": "goodwill; acquisition of businesses, net of cash acquired",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The acquired assets and assumed liabilities of the acquisition were not material and the Company recorded $39.1 million of goodwill as a result of the acquisition.",
    "paragraph_id": "0001048695-26-000067:notes:34",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "structure_and_disclosure_changes_calypsoai_acquisition_paragraph_recarried",
    "what_changed": "INSUFFICIENT. The fiscal 2025 CalypsoAI paragraph is carried as text rather than as unchanged. The likely reason is that the new SurePath heading and paragraph (notes:33, notes:34) re-segmented the note. My input has no change history for this note block and does not carry the prior wording. So I cannot tell whether anything in the description was revised, including the stated $145.2 million cash consideration.",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "a provider in enterprise AI security for $145.2 million in cash, with CalypsoAI immediately becoming a wholly-owned subsidiary of the Company upon the closing of the transaction.",
    "paragraph_id": "0001048695-26-000067:notes:36",
    "explanation": false,
    "insufficient": true
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_securities_class_action_motion_to_dismiss",
    "what_changed": "The prior note said Lead Plaintiffs 'will file an amended complaint by May 20, 2026' and that the company intends to defend 'this claim'. The note now says the amended complaint was filed on May 20, 2026, asserting the same claims for the same class period. As a subsequent event dated July 22, 2026, the company and certain executives filed a motion to dismiss. Defendants are now called 'executives' where the note said 'officers', and the note now says 'these claims'. No loss accrual is recorded (notes:93, unchanged).",
    "account": "loss contingency accrual (none recorded)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Lead Plaintiffs filed an amended complaint on May 20, 2026 asserting the same claims for the same putative class period. On July 22, 2026, the Company and certain of its executives filed a motion to dismiss the amended complaint.",
    "paragraph_id": "0001048695-26-000067:notes:90",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_derivative_litigation_stayed",
    "what_changed": "The prior note said the consolidated derivative action 'is in its early stages' and that the parties were negotiating a case schedule. The note now says the derivative claims are stayed until all motions to dismiss in the securities class action are fully resolved.",
    "account": "loss contingency accrual (none recorded)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The derivative claims are stayed until all motions to dismiss the securities class action have been fully resolved.",
    "paragraph_id": "0001048695-26-000067:notes:91",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_cyber_incident_insurance_recoveries",
    "what_changed": "New sentences: $5.3 million of insurance recoveries for Cyber Incident claims was received. The one amount is given for both the three and nine months, and it is recorded in other income, net. The cost sentence moved from $6.0 million and $23.5 million (three and six months ended March 31, 2026) to $3.0 million and $26.5 million (three and nine months ended June 30, 2026). The note still says significant further legal and professional expenses may be incurred in future periods, and that recoveries are booked when probable. Insurance recovery is not a receivables, inventory or reserve explanation.",
    "account": "other income, net; cyber incident costs",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The Company received $5.3 million in insurance recoveries for claims related to the Cyber Incident for the three and nine months ended June 30, 2026, respectively. These recoveries are recorded in other income, net in the accompanying consolidated income statements.",
    "paragraph_id": "0001048695-26-000067:notes:96",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "estimates_and_discretion_effective_tax_rate_attributed_to_unrecognized_tax_benefits",
    "what_changed": "The note gives effective tax rates of 8.0% (three months) and 16.0% (nine months), against 10.8% and 15.4% in the prior year. It attributes the quarter's decrease mainly to a change in unrecognized tax benefits. It attributes the nine-month increase mainly to non-recurring prior-year benefits (foreign operations, stock-based compensation), partly offset by the same UTB change. The note does not say what caused the UTB change. The IRS examination closure (notes:100) appears two paragraphs later, but the note does not link the two. Management explains a reported result by a movement in a tax reserve.",
    "account": "provision for income taxes; unrecognized tax benefits (income tax reserve)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in the effective tax rate for the three months ended June 30, 2026, as compared to the three months ended June 30, 2025, is primarily due to a change in unrecognized tax benefits.",
    "paragraph_id": "0001048695-26-000067:notes:98",
    "explanation": true,
    "insufficient": false
  },
{
    "id": "estimates_and_discretion_unrecognized_tax_benefits_balance_expected_to_change",
    "what_changed": "The note gives $72.7 million of unrecognized tax benefits at June 30, 2026 that would affect the rate if recognized. It says existing UTB liabilities are expected to change within twelve months through audit settlements or statute expirations, and that the change is not expected to be material. The prior balance is not in my input. Whether the balance moved is for the numbers reader. The prose gives no direction.",
    "account": "unrecognized tax benefits; income taxes payable (long-term)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "At June 30, 2026, the Company had $72.7 million of unrecognized tax benefits that, if recognized, would affect the effective tax rate.",
    "paragraph_id": "0001048695-26-000067:notes:99",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "estimates_and_discretion_irs_examination_closed_with_no_adjustments",
    "what_changed": "New sentence: during the third quarter of fiscal 2026 the IRS completed its examination of the fiscal 2019 federal return with no adjustments. The paragraph also says all U.S. federal matters are concluded for fiscal years through September 30, 2022. It lists open audits: various states (FY2018 to FY2024), India (FY2019 to FY2025), Israel (FY2020 to FY2024), Saudi Arabia (FY2015 to FY2021) and Singapore (FY2024). An examination closed with no adjustments implies any reserve held for that year is no longer needed. The note does not say so.",
    "account": "unrecognized tax benefits; provision for income taxes",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the third quarter of fiscal year 2026, the Internal Revenue Service completed its examination of the Company’s fiscal year 2019 U.S. federal income tax return with no adjustments.",
    "paragraph_id": "0001048695-26-000067:notes:100",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "estimates_and_discretion_restructuring_accrual_credit_with_no_new_charges",
    "what_changed": "This paragraph is carried as changed, but the prior wording is not in my input, so the exact edit cannot be isolated. It now says there were no significant subsequent charges under either the first-quarter or the fourth-quarter fiscal 2025 plan. The notes:127 rollforward shows the current-period restructuring line in parentheses and an ending accrual of $4 thousand. The 8-K and MD&A income-statement tables carry the same parenthesized figures. Footnote (1), which may explain the credit, is carried as unchanged (notes:128) and is not in my input. MD&A (mdna:41) discusses only the prior-year charge. No changed prose explains a reversal. The prose gives no direction.",
    "account": "restructuring charges; accrued restructuring (employee severance)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company did not record any significant subsequent charges related to the fourth quarter of fiscal 2025 restructuring plan.",
    "paragraph_id": "0001048695-26-000067:notes:125",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_insider_trading_plan_chief_marketing_officer",
    "what_changed": "New disclosure: John Maddison, EVP and Chief Marketing Officer, adopted a Rule 10b5-1 plan on June 14, 2026, effective until May 31, 2027. It covers up to 5,179 shares from existing awards plus 100% of net shares from future vesting. Other dates in the input: SurePath closed on June 15, 2026 (notes:34), the 8-K index lists a 5.02 filing dated 2026-06-23, and the release that raised the outlook is dated July 27, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On June 14, 2026, John Maddison, EVP, Chief Marketing Officer, adopted a written plan intended to satisfy the affirmative defense of Rule 10b5-1(c) that is designed to be in effect until May 31, 2027, authorizing the sale of up to 5,179 Company shares from existing equity awards",
    "paragraph_id": "0001048695-26-000067:notes:130",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_insider_trading_plan_chief_technology_operations_officer",
    "what_changed": "New disclosure: Michael Montoya, EVP and Chief Technology Operations Officer, adopted a Rule 10b5-1 plan on June 15, 2026, effective until August 31, 2027. It covers up to 13,813 shares from existing awards plus 100% of net shares from future vesting. The plan is dated the same day SurePath closed (notes:34). The Cyber Incident and the related litigation (notes:90, notes:95) concern the company's technology systems.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On June 15, 2026, Michael Montoya, EVP, Chief Technology Operations Officer, adopted a written plan intended to satisfy the affirmative defense of Rule 10b5-1(c) that is designed to be in effect until August 31, 2027, authorizing the sale of up to 13,813 Company shares from existing equity awards",
    "paragraph_id": "0001048695-26-000067:notes:131",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "articulation_and_the_filed_history_eight_consecutive_quarters_double_digit_product_growth",
    "what_changed": "The CEO quote in the release claims eight consecutive quarters of double-digit product growth. It is a claim about the filed history. The numbers reader can test it against product revenue in the filed quarterly reports.",
    "account": "net product revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Eight consecutive quarters of double-digit product growth",
    "paragraph_id": "0001048695-26-000063:8k_2_02:8",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_third_quarter_revenue_by_category_release",
    "what_changed": "The release gives third-quarter revenue of $865 million, described as 11% growth. By category it gives systems $240 million (grew 32%), software $223 million (grew 7%) and services $402 million (grew 3%). These are rounded release figures. Tying them to the 10-Q (mdna:23, mdna:24, mdna:27) is for the numbers reader.",
    "account": "net revenues; systems, software and services revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Third quarter fiscal year 2026 revenue totaled $865 million, representing 11% growth compared with $780 million in the third quarter of fiscal year 2025. Systems revenue of $240 million grew 32% from the year-ago period while software revenue of $223 million grew 7%. Services revenue of $402 million grew 3% from the year-ago period.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:11",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_gross_margin_release",
    "what_changed": "The release gives GAAP gross profit of $712 million and a gross margin of 82.2%, against $632 million and 81.0% a year ago. It gives non-GAAP gross margin of 84.2% against 83.1%. The prose uses no direction word. Read with mdna:7, which names component price increases as a margin factor.",
    "account": "gross profit; gross margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "GAAP gross profit for the third quarter of fiscal year 2026 was $712 million, representing GAAP gross margin of 82.2%. This compares with GAAP gross profit of $632 million in the year-ago period, which represented GAAP gross margin of 81.0%.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:12",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_gaap_operating_margin_release",
    "what_changed": "The release gives GAAP income from operations of $213 million and an operating margin of 24.7%, against $196 million and 25.2% a year ago. The prose uses no direction word.",
    "account": "income from operations; operating margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "GAAP income from operations for the third quarter of fiscal year 2026 was $213 million, representing GAAP operating margin of 24.7%. This compares with GAAP income from operations of $196 million in the year-ago period, which represented GAAP operating margin of 25.2%.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:13",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "earnings_quality_non_gaap_operating_margin_release",
    "what_changed": "The release gives non-GAAP income from operations of $303 million and a margin of 35.0%, against $267 million and 34.3% a year ago. The non-GAAP measure excludes six items: stock-based compensation, amortization, facility-exit costs, acquisition-related charges, cyber incident costs and restructuring (8k_2_02:31, 8k_2_02:67). The release presents the GAAP and non-GAAP margins side by side. Their relationship is for the numbers reader.",
    "account": "non-GAAP income from operations",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "GAAP income from operations for the period was $303 million, representing non-GAAP operating margin of 35.0%. This compares to non-GAAP income from operations of $267 million in the year-ago period, which represented non-GAAP operating margin of 34.3%.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:15",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_net_income_and_diluted_earnings_per_share_release",
    "what_changed": "The release gives GAAP net income of $208 million, or $3.62 per diluted share, against $190 million, or $3.25, a year ago. It gives non-GAAP net income of $272 million, or $4.73, against $243 million, or $4.16. The prose uses no direction word. Read with the tax-rate attribution in notes:98.",
    "account": "net income; diluted earnings per share",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "GAAP net income for the third quarter of fiscal year 2026 was $208 million, or $3.62 per diluted share compared to $190 million, or $3.25 per diluted share, in the third quarter of fiscal year 2025.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:16",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_raised_full_year_revenue_outlook",
    "what_changed": "The release says F5 raised its fiscal 2026 revenue growth outlook to about 9% to 10%, from 7% to 8% before.",
    "account": "net revenues (full fiscal year)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "F5 raised its outlook for its fiscal year 2026, guiding for revenue growth of approximately 9% to 10%, up from 7% to 8% previously.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:21",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_raised_full_year_non_gaap_earnings_outlook",
    "what_changed": "The release raises the fiscal 2026 non-GAAP EPS outlook to $17.21 to $17.33, from $16.25 to $16.55 before. Under 8k_2_02:23, the guided figures exclude cyber incident costs and recoveries, among other items.",
    "account": "non-GAAP diluted earnings per share (full fiscal year)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "F5 expects non-GAAP earnings per share in a range of $17.21 to $17.33, up from $16.25 to $16.55 previously.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:21",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "results_against_expectations_fourth_quarter_revenue_and_earnings_guidance",
    "what_changed": "The release guides fourth-quarter fiscal 2026 revenue to $870 million to $890 million, and non-GAAP EPS to $4.14 to $4.26. The prose gives no direction. How the range relates to the third quarter is for the numbers reader.",
    "account": "net revenues; non-GAAP diluted earnings per share (fourth quarter)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "For the fourth quarter of fiscal year 2026, F5 is guiding to revenue in the range of $870 million to $890 million, with non-GAAP earnings in the range of $4.14 to $4.26 per diluted share.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:22",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "earnings_quality_forward_guidance_excludes_cyber_costs_and_insurance_recoveries",
    "what_changed": "The outlook's list of excluded items names both cyber incident costs and insurance recoveries from cyber incident. So guided non-GAAP figures leave out any future cyber costs and any future recoveries. The prior release is not in my input. The recoveries term appears together with the new recoveries adjustment (8k_2_02:38), and the first recoveries the notes report are this quarter's (notes:96).",
    "account": "non-GAAP earnings guidance",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "cyber incident costs, insurance recoveries from cyber incident, restructuring charges, facility exit costs, or other non-recurring charges that may occur in the period",
    "paragraph_id": "0001048695-26-000063:8k_2_02:23",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "earnings_quality_cyber_incident_costs_labelled_non_recurring",
    "what_changed": "The release calls cyber incident costs 'non-recurring' and excludes them from non-GAAP measures. The 10-Q note (notes:96) states such costs for the three months ended June 30, 2026, and the prior note stated them for the three months ended March 31, 2026. The note also says the company 'may incur significant legal and professional services and other expenses associated with the incident in future periods'. So the label is applied to costs the filings report in successive quarters and expect to continue. The prior release is not in my input, so I cannot see whether the label itself is new.",
    "account": "non-GAAP income from operations (cyber incident cost add-back); cyber incident costs",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Cyber incident costs. F5 has incurred certain non-recurring expenses in connection with the investigation and remediation of the Cyber Incident.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:37",
    "explanation": false,
    "insufficient": false
  },
{
    "id": "earnings_quality_non_gaap_exclusion_of_cyber_insurance_recoveries",
    "what_changed": "The release adds 'Insurance recoveries from cyber incident' as a non-GAAP adjustment. Its stated reason, continued in 8k_2_02:40, is that the recoveries offset the cyber-cost add-back. The reconciliation (8k_2_02:67) has a new row for it, filled in only in the current-year three- and nine-month columns, below operating income in the net income section. The 10-Q records these recoveries in other income, net (notes:96). Removing a recovery from the non-GAAP measure lowers that measure by the recovery.",
    "account": "non-GAAP net income (insurance recovery adjustment); other income, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Insurance recoveries from cyber incident. F5 has received insurance recoveries in connection with the cyber incident costs described above.",
    "paragraph_id": "0001048695-26-000063:8k_2_02:38",
    "explanation": false,
    "insufficient": false
  }
]
```

## Paragraphs carried as text that are not items

### Item 4 (controls)
- 0001048695-26-000067:item_4_controls:1 — heading.
- 0001048695-26-000067:item_4_controls:2 — standard definition of disclosure controls; carried verbatim with no prior to compare; nothing new on its face.
- 0001048695-26-000067:item_4_controls:3 — disclosure controls concluded effective as of June 30, 2026; date rolled forward; no weakness stated.
- 0001048695-26-000067:item_4_controls:4 — heading.
- 0001048695-26-000067:item_4_controls:5 — no change in internal control over financial reporting this quarter; date rolled forward.
- 0001048695-26-000067:item_4_controls:6 — page number.

### MD&A
- 0001048695-26-000067:mdna:22 — revenue table; amounts only.
- 0001048695-26-000067:mdna:26 — systems/software table; amounts only.
- 0001048695-26-000067:mdna:29 — customer revenue concentration table; amounts only.
- 0001048695-26-000067:mdna:31 — receivables concentration table; amounts only.
- 0001048695-26-000067:mdna:33 — cost of revenue and gross margin table; amounts only.
- 0001048695-26-000067:mdna:37 — operating expense table; amounts only.
- 0001048695-26-000067:mdna:41 — prior-year restructuring charge restated for the nine-month comparison; date rolled forward. The current-year credit is covered in the notes:125 item.
- 0001048695-26-000067:mdna:42 — other income and tax table; amounts only.
- 0001048695-26-000067:mdna:46 — page number.
- 0001048695-26-000067:mdna:56 — date rolled forward (the same edit the history shows for notes:81). The conflict with mdna:54 is in the across-documents item.

### Notes
- 0001048695-26-000067:notes:5 — date rolled forward (six to nine months), per history.
- 0001048695-26-000067:notes:8 — the history records no change for this paragraph; ASU 2024-03 and ASU 2025-06 descriptions; nothing identifiable as new.
- 0001048695-26-000067:notes:10 — wording ('significant movements' became 'movements') and date rolled forward.
- 0001048695-26-000067:notes:11 — contract-cost rollforward table; amounts only.
- 0001048695-26-000067:notes:12 — amounts and dates rolled forward, per history; the no-impairment sentence is unchanged.
- 0001048695-26-000067:notes:15 — table header; date rolled forward.
- 0001048695-26-000067:notes:21 — table header; date rolled forward.
- 0001048695-26-000067:notes:22 — fair value table; amounts only.
- 0001048695-26-000067:notes:27 — interest income amounts and dates rolled forward; the unrealized-loss sentence is unchanged on its face.
- 0001048695-26-000067:notes:28 — no credit losses; date rolled forward.
- 0001048695-26-000067:notes:30 — impairment policy text split by a page break; no new substance.
- 0001048695-26-000067:notes:31 — continuation of notes:30; the annual second-quarter goodwill review is restated.
- 0001048695-26-000067:notes:32 — impairment not material; date rolled forward.
- 0001048695-26-000067:notes:33 — heading for the new SurePath disclosure (the item is on notes:34).
- 0001048695-26-000067:notes:35 — heading for the fiscal 2025 CalypsoAI acquisition.
- 0001048695-26-000067:notes:45 — heading.
- 0001048695-26-000067:notes:47 — cash and restricted cash table; amounts only.
- 0001048695-26-000067:notes:50 — inventory table; amounts only. No changed prose explains inventory.
- 0001048695-26-000067:notes:53 — other current assets table; amounts only.
- 0001048695-26-000067:notes:56 — other assets table; amounts only.
- 0001048695-26-000067:notes:59 — accrued liabilities table; amounts only.
- 0001048695-26-000067:notes:62 — other long-term liabilities table; amounts only.
- 0001048695-26-000067:notes:63 — heading.
- 0001048695-26-000067:notes:64 — date rolled forward, per history; the sentence still refers to prior-year periods for the facility that expired.
- 0001048695-26-000067:notes:65 — the history records no change; the facility's expiry on January 31, 2025 was already disclosed.
- 0001048695-26-000067:notes:66 — headquarters lease description; no change identifiable.
- 0001048695-26-000067:notes:67 — table header; date rolled forward.
- 0001048695-26-000067:notes:68 — lease expense table; amounts only.
- 0001048695-26-000067:notes:71 — lease balance table, including term and discount rate; amounts only.
- 0001048695-26-000067:notes:73 — table header; date rolled forward.
- 0001048695-26-000067:notes:74 — lease maturity table; amounts only.
- 0001048695-26-000067:notes:75 — sublease income amounts and periods rolled forward.
- 0001048695-26-000067:notes:76 — no leases signed but not yet commenced; date rolled forward.
- 0001048695-26-000067:notes:77 — heading.
- 0001048695-26-000067:notes:78 — wording only (one comma added), per history.
- 0001048695-26-000067:notes:79 — warranty accrual not material; date rolled forward, per history.
- 0001048695-26-000067:notes:80 — heading.
- 0001048695-26-000067:notes:81 — purchase commitment; date rolled forward, per history. The conflict with mdna:54 is in the across-documents item.
- 0001048695-26-000067:notes:82 — the history records no change.
- 0001048695-26-000067:notes:83 — heading.
- 0001048695-26-000067:notes:84 — heading.
- 0001048695-26-000067:notes:85 — Lynwood complaint background; the history records no change.
- 0001048695-26-000067:notes:86 — Lynwood motions history; the history records no change.
- 0001048695-26-000067:notes:87 — Lynwood judgment and appeal; the history records no change.
- 0001048695-26-000067:notes:88 — Lynwood remand and discovery; the history records no change; no new development stated.
- 0001048695-26-000067:notes:89 — heading.
- 0001048695-26-000067:notes:92 — general legal-proceedings paragraph; the history records no change.
- 0001048695-26-000067:notes:93 — no loss accrual recorded; the history records no change.
- 0001048695-26-000067:notes:94 — heading.
- 0001048695-26-000067:notes:95 — wording only (the defined term moved), per history.
- 0001048695-26-000067:notes:104 — share repurchase table; amounts only.
- 0001048695-26-000067:notes:105 — remaining repurchase authorization restated at the new date; amounts only.
- 0001048695-26-000067:notes:107 — the 2026 Plan was adopted on March 12, 2026, already in the prior period; only the date in the shares-available sentence rolled forward.
- 0001048695-26-000067:notes:110 — EPS table; amounts only.
- 0001048695-26-000067:notes:111 — anti-dilutive awards not material; date rolled forward.
- 0001048695-26-000067:notes:117 — geographic revenue table; amounts only.
- 0001048695-26-000067:notes:119 — systems/software table; amounts only.
- 0001048695-26-000067:notes:121 — customer concentration table; amounts only.
- 0001048695-26-000067:notes:124 — property and equipment by geography table; amounts only.
- 0001048695-26-000067:notes:126 — table header; date rolled forward.
- 0001048695-26-000067:notes:127 — restructuring rollforward table; amounts only. Read with the notes:125 item.

### 8-K item 2.02 (0001048695-26-000063)
- 0001048695-26-000063:8k_2_02:1 — exhibit header.
- 0001048695-26-000063:8k_2_02:2 — document label.
- 0001048695-26-000063:8k_2_02:3 — page header.
- 0001048695-26-000063:8k_2_02:4 — contacts.
- 0001048695-26-000063:8k_2_02:5 — headline repeating the product growth in :8 and :11.
- 0001048695-26-000063:8k_2_02:6 — headline repeating the total revenue growth in :11.
- 0001048695-26-000063:8k_2_02:7 — dateline.
- 0001048695-26-000063:8k_2_02:9 — CEO narrative on AI threats; no account or figure.
- 0001048695-26-000063:8k_2_02:10 — heading.
- 0001048695-26-000063:8k_2_02:14 — page header.
- 0001048695-26-000063:8k_2_02:17 — heading.
- 0001048695-26-000063:8k_2_02:18 — summary table repeating :11 to :16; amounts only.
- 0001048695-26-000063:8k_2_02:19 — pointer to the reconciliation.
- 0001048695-26-000063:8k_2_02:20 — heading.
- 0001048695-26-000063:8k_2_02:24 — page header.
- 0001048695-26-000063:8k_2_02:25 — heading.
- 0001048695-26-000063:8k_2_02:26 — webcast logistics.
- 0001048695-26-000063:8k_2_02:27 — heading.
- 0001048695-26-000063:8k_2_02:28 — page header.
- 0001048695-26-000063:8k_2_02:29 — end of the cautionary statement.
- 0001048695-26-000063:8k_2_02:30 — heading.
- 0001048695-26-000063:8k_2_02:31 — list of non-GAAP adjustments; the new recoveries exclusion is covered by the :38 item.
- 0001048695-26-000063:8k_2_02:32 — introductory sentence.
- 0001048695-26-000063:8k_2_02:33 — stock-based compensation rationale; boilerplate.
- 0001048695-26-000063:8k_2_02:34 — amortization rationale; boilerplate.
- 0001048695-26-000063:8k_2_02:35 — facility-exit rationale; boilerplate.
- 0001048695-26-000063:8k_2_02:36 — acquisition-related charges rationale; boilerplate.
- 0001048695-26-000063:8k_2_02:39 — page header.
- 0001048695-26-000063:8k_2_02:40 — continuation of :38 across a page break; covered by the :38 item.
- 0001048695-26-000063:8k_2_02:41 — restructuring rationale; boilerplate.
- 0001048695-26-000063:8k_2_02:42 — non-GAAP usefulness; boilerplate.
- 0001048695-26-000063:8k_2_02:43 — non-GAAP usefulness; boilerplate.
- 0001048695-26-000063:8k_2_02:44 — pointer to the reconciliation.
- 0001048695-26-000063:8k_2_02:45 — heading.
- 0001048695-26-000063:8k_2_02:46 — company description.
- 0001048695-26-000063:8k_2_02:47 — link.
- 0001048695-26-000063:8k_2_02:48 — link.
- 0001048695-26-000063:8k_2_02:49 — social links.
- 0001048695-26-000063:8k_2_02:50 — trademark notice.
- 0001048695-26-000063:8k_2_02:51 — source line.
- 0001048695-26-000063:8k_2_02:52 — heading.
- 0001048695-26-000063:8k_2_02:53 — heading.
- 0001048695-26-000063:8k_2_02:54 — heading.
- 0001048695-26-000063:8k_2_02:55 — balance sheet; amounts only.
- 0001048695-26-000063:8k_2_02:56 — heading.
- 0001048695-26-000063:8k_2_02:57 — heading.
- 0001048695-26-000063:8k_2_02:58 — heading.
- 0001048695-26-000063:8k_2_02:59 — income statement; amounts only.
- 0001048695-26-000063:8k_2_02:60 — heading.
- 0001048695-26-000063:8k_2_02:61 — heading.
- 0001048695-26-000063:8k_2_02:62 — heading.
- 0001048695-26-000063:8k_2_02:63 — cash flow statement; amounts only.
- 0001048695-26-000063:8k_2_02:64 — heading.
- 0001048695-26-000063:8k_2_02:65 — heading.
- 0001048695-26-000063:8k_2_02:66 — heading.
- 0001048695-26-000063:8k_2_02:67 — GAAP to non-GAAP reconciliation table; amounts only. Its new recoveries row is the subject of the :38 item.
- 0001048695-26-000063:8k_2_02:68 — rounding note.

### Not carried as paragraphs
- `input_8k.md` 8-K item-code list — only the 2026-06-23 entry, which is inside this quarter, gets an item, and it is marked insufficient. The 2026-07-27 entry is the release read above. The other entries are index lines with no body in my input.
- `input_8k.md` late-filing section — says none; no item.
- `input_notes_history.md` — used as the diff reference for the notes; not reported separately.
- `input_prior_predictions.md` — none on record.
