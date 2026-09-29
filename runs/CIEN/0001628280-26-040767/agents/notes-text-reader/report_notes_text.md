# Notes-text report: CIEN 10-Q 0001628280-26-040767 (fiscal Q2 2026, quarter ended May 2, 2026)

**What I read.** I read all six files in full:
- `input_notes.md`
- `input_notes_history.md`, which compares against the Q1 10-Q, 0001628280-26-015152
- `input_mdna.md`
- `input_controls.md`
- `input_8k.md`, which holds the 8-K item index and the Item 2.02 release 0001628280-26-040614
- `input_prior_predictions.md`, which says none are on record

**Forbidden material check.** None of the following is in the directory:
- a trend table
- market prices or abnormal returns
- short interest
- another company's files
- any prior probability or outcome window

The per-share repurchase prices in notes:128 and notes:154 are the company's own disclosures. I did not use them.

**Sections not in my input.**
- The controls file header says it holds the auditor's report, but it contains only Item 4. A 10-Q has no audit opinion.
- There is no Item 1A diff, no Exhibit 21 diff and no Exhibit 10.
- The 2026-03-31 8-K (Item 5.07) appears in the index only; its body is not in input.

**MD&A caveat.** MD&A paragraphs marked as changed come without their prior wording. For those items, `what_changed` says what the paragraph now states and notes where I cannot tell whether a phrase is new.

**No arithmetic.** I did no arithmetic, comparison or growth calculation. Where two amounts from different dates appear, I quote both and do not characterise the difference.

## Items

```json
{ "id": "revenue_recognition_remaining_performance_obligations_note_conversion_window_loosened",
  "what_changed": "The RPO paragraph drops the prior 10-Q sentence that Ciena expected approximately 85% of RPO to be recognized as revenue within the next 12 months (0001628280-26-015152:note_history:48). It now gives only a looser window: 'the majority' within a year and any remainder typically within three years. RPO is stated at $2.5 billion as of May 2, 2026; the prior 10-Q stated $2.3 billion as of January 31, 2026. I make no comparison between the two.",
  "account": "remaining performance obligations; revenue (conversion timing)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "performance obligations will be satisfied within a year and any remaining performance obligations are typically recognized within three years.",
  "paragraph_id": "0001628280-26-040767:notes:60",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_supply_conditions_note_fulfillment_timing",
  "what_changed": "New sentence in the RPO paragraph: the timing of fulfilling remaining performance obligations can be affected by supply conditions. The prior 10-Q's RPO paragraph had no supply caveat. The sentence states a risk, not an effect, so it implies no direction.",
  "account": "revenue; remaining performance obligations",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The timing of fulfillment of remaining performance obligations can be impacted by supply conditions.",
  "paragraph_id": "0001628280-26-040767:notes:60",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_long_term_unbilled_software_license_receivables_note",
  "what_changed": "New sentence, not in the prior 10-Q: long-term accounts receivable are unbilled receivables from non-cancellable software licenses. Ciena recognized the revenue when the licenses were made available to customers and will bill later. This is management's statement of what the long-term receivable balance consists of and how it arose. It states no movement.",
  "account": "long-term accounts receivable (unbilled); product revenue (software licenses)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "long-term accounts receivable represent unbilled receivables attributable to non-cancellable software licenses recognized as revenue when made available to customers, to be billed in the future.",
  "paragraph_id": "0001628280-26-040767:notes:53",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_note_forecasted_demand_reductions",
  "what_changed": "The six-month provision for inventory excess and obsolescence is stated at $42.5 million. The note attributes it primarily to reductions in forecasted demand for certain products, and attributes deductions from the reserve to sales and disposal. The paragraph is carried as text with the amount rolled to the six-month period. The note change history records no wording change, so the demand-reduction cause may carry over from the first quarter. This demand-reduction cause stands against MD&A mdna:8, which describes unprecedented increases in demand.",
  "account": "reserve for inventory excess and obsolescence; inventories, net; product cost of goods sold",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Ciena recorded a provision for inventory excess and obsolescence of $42.5 million, primarily driven by reductions in forecasted demand for certain products.",
  "paragraph_id": "0001628280-26-040767:notes:86",
  "explanation": true }
```

```json
{ "id": "earnings_quality_effective_tax_rate_note_share_based_compensation_benefit",
  "what_changed": "The income-tax note says the effective tax rate for the second quarter and first six months of fiscal 2026 was lower than in the fiscal 2025 periods. It attributes this primarily to an income tax benefit from share-based compensation and a shift in earnings mix toward lower-rate jurisdictions. The paragraph is carried as text; its prior wording is not in the note change history. The share-based benefit depends on values at vesting (see notes:149), so it is not an operating source of earnings.",
  "account": "provision for income taxes; effective tax rate",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease was primarily due to an income tax benefit for share-based compensation expense and a change in mix of earnings in jurisdictions with lower tax rates.",
  "paragraph_id": "0001628280-26-040767:notes:71",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_tax_contingency_share_based_deductions_at_vesting",
  "what_changed": "New sentences under Tax Contingencies: share-based compensation affects Ciena's tax rate because the deductions are valued at vesting. They can raise or lower the effective tax rate in the period in which they vest. This was not in the prior 10-Q. It flags the rate as volatile in either direction.",
  "account": "provision for income taxes; effective tax rate",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "These deductions are valued at vesting for tax purposes and can increase or decrease the effective tax rate in the period in which they vest.",
  "paragraph_id": "0001628280-26-040767:notes:149",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_inventory_purchase_order_commitments_note_restated",
  "what_changed": "Outstanding purchase order commitments to contract manufacturers and component suppliers are now stated as $2.8 billion as of May 2, 2026; the prior 10-Q stated $1.9 billion as of January 31, 2026. The note ties these to advanced orders for long lead time components. MD&A mdna:160 names this as the one contractual obligation that has changed materially since November 1, 2025. The prose implies future inventory receipts against these orders.",
  "account": "purchase obligations (off-balance-sheet); inventories; accounts payable",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "As of May 2, 2026, Ciena had $2.8 billion in outstanding purchase order commitments to contract manufacturers and component suppliers for inventory.",
  "paragraph_id": "0001628280-26-040767:notes:152",
  "explanation": false }
```

```json
{ "id": "across_documents_purchase_commitments_cancellable_portion_wording",
  "what_changed": "The two documents describe how much of the purchase order commitments can be cancelled in opposite ways. MD&A says Ciena may cancel, reschedule or adjust 'these orders', so 'only a portion' is firm, non-cancelable and unconditional. The note (notes:152) says Ciena may cancel, reschedule or adjust 'a portion of these orders', which leaves the rest firm. The note wording is unchanged from the prior 10-Q. The prior MD&A wording is not in input, so I cannot tell whether the gap is new.",
  "account": "purchase obligations (firm versus cancellable); inventories",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Consequently, only a portion of this amount relates to firm, non-cancelable and unconditional obligations.",
  "paragraph_id": "0001628280-26-040767:mdna:161",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_tariff_ruling_disclosure_dropped",
  "what_changed": "The prior 10-Q's subsequent-events note disclosed the February 20, 2026 Supreme Court ruling that part of the tariffs Ciena had been subject to were invalid. It also covered the new global tariff that followed and the open questions on the timing and mechanics of any refunds, and said Ciena was evaluating the impact. This 10-Q drops that disclosure. Nothing on the ruling, refunds, a refund receivable or the replacement tariff appears in any note or MD&A paragraph carried as text in my input. The unchanged MD&A paragraphs are not visible to me.",
  "account": "product cost of goods sold (tariff cost); prepaid expenses and other (any tariff refund receivable)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "On February 20, 2026, the U.S. Supreme Court ruled that a portion of the tariffs that Ciena has been subject to were invalid.",
  "paragraph_id": "0001628280-26-015152:note_history:51",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_ten_percent_customer_table_no_service_provider",
  "what_changed": "The 10% customer table now names Cloud provider A and Cloud provider B with amounts in both fiscal 2026 columns. A single 'Service provider' row carries amounts only in the fiscal 2025 columns and shows n/a* for the quarter and six months of fiscal 2026. The prior 10-Q table listed 'Service provider A' with an amount for the first quarter of fiscal 2026. The current table shows no service-provider amount in either fiscal 2026 column.",
  "account": "revenue (customer concentration)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Service provider | n/a*",
  "paragraph_id": "0001628280-26-040767:notes:47",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_ten_percent_customers_segment_breadth_sentence",
  "what_changed": "Removed sentence: 'Service provider A purchased products from each of Ciena's operating segments'. The remaining sentence drops 'other' and now covers all listed 10% customers, which buy from Networking Platforms, Platform Software and Services, and Global Services. No listed 10% customer is now described as buying from Blue Planet Automation Software and Services, the segment whose revenue MD&A says decreased (mdna:32).",
  "account": "Blue Planet Automation Software and Services revenue (customer base)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The 10% customers included in the table above purchased products from",
  "paragraph_id": "0001628280-26-040767:notes:49",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_over_time_revenue_row_relabelled_services",
  "what_changed": "In all four revenue disaggregation tables the timing-of-recognition row is relabelled. It was 'Products and services transferred over time' in the prior 10-Q and is now 'Services transferred over time'. The separate 'Segment' header row is also gone. No explanation is given. The new label says no product revenue is recognized over time, while the Platform Software and Services segment reports its software portion as product revenue (note_history:31).",
  "account": "revenue (timing of recognition; products versus services classification)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Services transferred over time",
  "paragraph_id": "0001628280-26-040767:notes:15",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_environmental_credits_standard_added",
  "what_changed": "New paragraph on ASU 2026-02 (environmental credits and environmental credit obligations), issued in May 2026. It is effective for annual periods beginning after December 15, 2027, applied retrospectively, and Ciena is evaluating its impact. The adjacent ASU 2025-11 sentence changed only in punctuation.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "beyond 12 months",
  "quote": "to clarify the accounting treatment and reporting standards of environmental credits and environmental credit obligations.",
  "paragraph_id": "0001628280-26-040767:notes:11",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_financial_officer_sales_plan",
  "what_changed": "The quarter's trading-arrangement disclosure: on March 25, 2026 the CFO, Marc D. Graff, adopted a Rule 10b5-1 sales arrangement that runs until May 22, 2027. The footnote (notes:157) says it covers up to 33% of the net after-tax shares from vesting of 54,664 restricted stock units on the listed dates. It also covers performance stock units ranging from 0% to 200% of a 2,788-share target, vesting December 20, 2026.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Adoption (March 25, 2026) | Rule 10b5-1 trading arrangement | Sales",
  "paragraph_id": "0001628280-26-040767:notes:156",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_constrained_supply_historically_high_backlog",
  "what_changed": "The overview paragraph is marked changed; its prior wording is not in input. It now says orders for products and services significantly exceeded revenue. It says this, together with an industry-wide constrained supply environment, has produced historically high backlog.",
  "account": "remaining performance obligations (backlog)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "with orders for our products and services significantly exceeding our revenue. This dynamic, together with an industry-wide constrained supply environment, has resulted in historically high backlog.",
  "paragraph_id": "0001628280-26-040767:mdna:8",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_cloud_customer_concentration_mdna",
  "what_changed": "The same paragraph says sales to cloud providers are growing, and that a small number of those customers are becoming a larger portion of the business across multiple revenue segments. I cannot confirm whether this sentence is new because the prior MD&A is not in input. The notes' 10% table (notes:47) now names only cloud providers in the fiscal 2026 columns.",
  "account": "revenue (customer concentration); accounts receivable (counterparty concentration)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "As our sales to cloud providers grow, we are seeing a small number of those customers become a larger portion of our business across multiple revenue segments.",
  "paragraph_id": "0001628280-26-040767:mdna:8",
  "explanation": false }
```

```json
{ "id": "earnings_quality_gross_margin_pricing_optimization_driver",
  "what_changed": "The paragraph is marked changed; its prior wording is not in input. It attributes the quarter's gross margin increase primarily to higher product gross margin from cost reduction, 'pricing optimization' and product mix. Pricing is named as a margin driver alongside cost and mix.",
  "account": "gross margin (products)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to higher product gross margin associated with cost reduction, pricing optimization, and product mix.",
  "paragraph_id": "0001628280-26-040767:mdna:10",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_lower_manufacturing_efficiencies",
  "what_changed": "The product gross margin bullet names an offset: 'lower manufacturing efficiencies' partly offset the gains from cost reduction, pricing optimization and mix. The six-month bullet (mdna:74) repeats it. The paragraph is marked changed and its prior wording is not in input. The direction given is for the offsetting factor, not for product margin overall, which the prose says increased.",
  "account": "product gross margin (manufacturing efficiency offset); product cost of goods sold",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Product gross margin increased by 510 basis points, primarily due to cost reduction, pricing optimization, and product mix, partially offset by lower manufacturing efficiencies.",
  "paragraph_id": "0001628280-26-040767:mdna:70",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_services_margin_less_favorable_mix",
  "what_changed": "Services gross margin is described as decreased, due to a less favorable services mix, partly offset by improved margins on implementation services. The six-month bullet (mdna:75) says the same. The paragraph is marked changed and its prior wording is not in input.",
  "account": "services gross margin",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Services gross margin decreased by 110 basis points, primarily due to a less favorable services mix, partially offset by improved margins on implementation services.",
  "paragraph_id": "0001628280-26-040767:mdna:71",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_blue_planet_revenue_decline_assurance_software",
  "what_changed": "Blue Planet segment revenue is described as decreased, primarily from lower sales of unified assurance and analytics software. The six-month bullet (mdna:39) repeats it.",
  "account": "Blue Planet Automation Software and Services revenue",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Blue Planet Automation Software and Services segment revenue decreased by $4.6 million, primarily reflecting a sales decrease in our unified assurance and analytics software.",
  "paragraph_id": "0001628280-26-040767:mdna:32",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_blue_planet_segment_result_drivers",
  "what_changed": "The six-month Blue Planet segment bullet gives no amount and no direction word, unlike the other segment bullets. It attributes the segment result to lower software sales volume, reduced gross margins and higher research and development costs. The segment table (mdna:99) shows Blue Planet segment results in parentheses in both fiscal 2026 columns. The segment carries allocated goodwill (notes:142). No text in my input discusses impairment indicators or testing for it.",
  "account": "Blue Planet Automation Software and Services segment profit (loss); goodwill allocated to the segment",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Blue Planet Automation Software and Services segment primarily reflects lower software sales volume as described above, reduced gross margins and increased research and development costs.",
  "paragraph_id": "0001628280-26-040767:mdna:110",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_emea_netherlands_cloud_quarter_decrease",
  "what_changed": "The quarter's EMEA bullet names decreased sales to cloud provider customers in the Netherlands as an offset to growth in France. The six-month bullet (mdna:54) names increased Netherlands cloud sales as a driver. So the prose names the same customer group as a positive driver for the six months and a negative one for the quarter.",
  "account": "EMEA revenue (cloud provider customers, Netherlands)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "EMEA revenue increased by $4.5 million, primarily driven by increased sales in France, partially offset by decreased sales to cloud provider customers in the Netherlands.",
  "paragraph_id": "0001628280-26-040767:mdna:50",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_routing_switching_data_center_management_driver",
  "what_changed": "The Routing and Switching bullet names 8100 Coherent IP networking platforms in an out-of-band data center management (DCOM) solution as a growth driver, alongside the 3000 and 5000 series. The six-month bullet (mdna:37) repeats it. The paragraph is marked changed and its prior wording is not in input.",
  "account": "Routing and Switching revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "8100 Coherent IP networking platforms in our out-of-band data center management (DCOM) solution",
  "paragraph_id": "0001628280-26-040767:mdna:30",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_nubis_acquisition_research_headcount",
  "what_changed": "The R&D increase is attributed partly to higher headcount 'from our acquisition of Nubis Communications'. The six-month bullet (mdna:89) repeats it. The acquired headcount appears in the prose as an R&D cost driver. The prior wording is not in input.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Net of hedging, this primarily reflects higher employee headcount and related costs, including from our acquisition of Nubis Communications, technology related costs and engineering design and development costs.",
  "paragraph_id": "0001628280-26-040767:mdna:83",
  "explanation": false }
```

```json
{ "id": "across_documents_intangible_amortization_mdna_operating_line_only",
  "what_changed": "The MD&A bullet says amortization of intangible assets decreased because certain intangibles reached the end of their economic lives. It addresses only the operating-expense line. The release's reconciliation (8k_2_02:68) carries a separate amortization line within gross profit, which no MD&A text in my input explains. Total amortization across both lines is for the numbers reader to reconcile.",
  "account": "amortization of intangible assets (operating expense line; cost of goods sold line)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Amortization of intangible assets decreased by $2.8 million, primarily reflecting certain intangible assets having reached the end of their economic lives.",
  "paragraph_id": "0001628280-26-040767:mdna:87",
  "explanation": false }
```

```json
{ "id": "across_documents_tax_provision_mdna_omits_share_based_benefit",
  "what_changed": "MD&A attributes the quarter's change in the tax provision primarily to higher pre-tax book income and says nothing of a share-based compensation benefit. The income-tax note (notes:71) says the effective rate was lower, primarily because of a share-based compensation tax benefit and jurisdictional mix. The six-month MD&A bullet (mdna:126) gives the same explanation as mdna:121.",
  "account": "provision for income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Provision for income taxes increased by $2.8 million, primarily due to the increase in pre-tax book income.",
  "paragraph_id": "0001628280-26-040767:mdna:121",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capital_purchases_supply_chain_equipment",
  "what_changed": "The capital allocation paragraph now says first-half capital purchases of $115 million went 'primarily for supply chain equipment and research and development'. It is marked changed and its prior wording is not in input. The prose names supply-chain equipment as the main use of capital spending.",
  "account": "equipment, building, furniture and fixtures, net; depreciation",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "we invested $115 million in capital purchases, primarily for supply chain equipment and research and development",
  "paragraph_id": "0001628280-26-040767:mdna:14",
  "explanation": false }
```

```json
{ "id": "earnings_quality_receivables_change_sales_volume_and_collections",
  "what_changed": "The working-capital bullet attributes the change in accounts receivable to increased sales volume, partly offset by improved cash collections. This is a management explanation of the receivables movement for the first six months.",
  "account": "accounts receivable, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The change in accounts receivable primarily reflects increased sales volume, partially offset by improved cash collections",
  "paragraph_id": "0001628280-26-040767:mdna:145",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_finished_goods_build_supply_chain_volatility",
  "what_changed": "The inventory bullet attributes the change in inventories to a deliberate build of finished goods to mitigate supply-chain volatility, partly offset by a reduction in raw materials. This is a management explanation of the inventory movement. It sits alongside notes:86, which attributes reserve provisions to reductions in forecasted demand for certain products.",
  "account": "inventories (finished goods up; raw materials down)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The change in inventories primarily reflects increased finished good inventory to mitigate supply chain volatility, partially offset by reduction in raw materials",
  "paragraph_id": "0001628280-26-040767:mdna:146",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_refundable_advances_to_contract_manufacturer",
  "what_changed": "The prepaid bullet attributes the change in prepaid expenses and other to higher refundable cash advances to a third-party contract manufacturer and higher prepaid VAT. Cash advances to a contract manufacturer are named as a use of working capital.",
  "account": "prepaid expenses and other",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The change in prepaid expenses and other primarily reflects higher refundable cash advances to a third-party contract manufacturer and higher prepaid value-added tax (VAT)",
  "paragraph_id": "0001628280-26-040767:mdna:147",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_incentive_payout_and_supplier_payment_timing",
  "what_changed": "The payables and accruals bullet attributes the change to the timing of annual incentive compensation payments, partly offset by the timing of payments to suppliers. The supplier-timing offset points to higher accounts payable.",
  "account": "accrued liabilities and other short-term obligations (compensation); accounts payable",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The change in accounts payable, accruals, and other obligations primarily reflects the timing of payments associated with our annual incentive compensation plan, partially offset by the timing of payments to suppliers",
  "paragraph_id": "0001628280-26-040767:mdna:148",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_fiscal_year_revenue_guidance_raised",
  "what_changed": "The release raises fiscal 2026 revenue guidance to $6.3 billion plus or minus $100 million and describes it as a 32% year-over-year increase at the midpoint. The prior guidance is not in input. The direction word 'Raising' is the release's own. The repeat at 8k_2_02:28 is covered here.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Raising revenue guidance for fiscal year 2026 to $6.3 billion plus or minus $100 million, a 32% increase YoY at the midpoint",
  "paragraph_id": "0001628280-26-040614:8k_2_02:9",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_third_quarter_revenue_outlook",
  "what_changed": "The release gives third-quarter fiscal 2026 revenue guidance of $1.625 billion plus or minus $50 million. The repeat at 8k_2_02:23 reads '$1.625B billion'. The prose states a level, not a direction. Comparing it with reported revenue is the numbers reader's job.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Providing revenue guidance for fiscal third quarter 2026 of $1.625 billion plus or minus $50 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:8",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_third_quarter_adjusted_gross_margin_outlook",
  "what_changed": "The release gives a third-quarter adjusted (non-GAAP) gross margin outlook of 45% plus or minus 50 bps. This is a level with no direction word. The prior outlook is not in input.",
  "account": "adjusted gross margin",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Adjusted (non-GAAP) gross margin in the range of 45% plus or minus 50 bps",
  "paragraph_id": "0001628280-26-040614:8k_2_02:24",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_third_quarter_adjusted_operating_expense_outlook",
  "what_changed": "The release gives a third-quarter adjusted (non-GAAP) operating expense outlook of $410 million plus or minus $10 million. This is a level with no direction word.",
  "account": "adjusted operating expense",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Adjusted (non-GAAP) operating expense in the range of $410 million plus or minus $10 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:25",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_third_quarter_adjusted_operating_margin_outlook",
  "what_changed": "The release gives a third-quarter adjusted (non-GAAP) operating margin outlook of between 19% and 20%. This is a level with no direction word.",
  "account": "adjusted operating margin",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Adjusted (non-GAAP) operating margin between 19% and 20%",
  "paragraph_id": "0001628280-26-040614:8k_2_02:26",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_fiscal_year_adjusted_gross_margin_outlook",
  "what_changed": "The release gives a fiscal 2026 adjusted (non-GAAP) gross margin outlook of between 44.5% and 45%. The release uses 'raising' only for revenue, so it does not say whether this range moved. The prior outlook is not in input.",
  "account": "adjusted gross margin",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Adjusted (non-GAAP) gross margin between 44.5% and 45%",
  "paragraph_id": "0001628280-26-040614:8k_2_02:29",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_fiscal_year_adjusted_operating_expense_outlook",
  "what_changed": "The release gives a fiscal 2026 adjusted (non-GAAP) operating expense outlook of $1.61 billion plus or minus $20 million. This is a level with no direction word. The prior outlook is not in input.",
  "account": "adjusted operating expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Adjusted (non-GAAP) operating expense in the range of $1.61 billion plus or minus $20 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:30",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_release_fiscal_year_adjusted_operating_margin_outlook",
  "what_changed": "The release gives a fiscal 2026 adjusted (non-GAAP) operating margin outlook of 19% plus or minus 50 bps. This is a level with no direction word. The prior outlook is not in input.",
  "account": "adjusted operating margin",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Adjusted (non-GAAP) operating margin in the range of 19% plus or minus 50bps",
  "paragraph_id": "0001628280-26-040614:8k_2_02:31",
  "explanation": false }
```

```json
{ "id": "across_documents_release_two_customer_concentration_share",
  "what_changed": "The release says two customers each represented 10%-plus of revenue, together 34.0% of revenue. The count matches the two cloud providers named in the notes' 10% table for the quarter (notes:47). I do not check the percentage against the table.",
  "account": "revenue (customer concentration)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Two customers represented 10%-plus of revenue for a total of 34.0% of revenue.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:33",
  "explanation": false }
```

```json
{ "id": "across_documents_release_days_sales_outstanding_against_collections_claim",
  "what_changed": "The release states average DSO of 71. MD&A (mdna:145) claims improved cash collections, which implies DSO should be lower. Whether the stated DSO bears that out is for the numbers reader.",
  "account": "accounts receivable, net (days sales outstanding)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "sales outstanding (DSOs) were 71.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:34",
  "explanation": false }
```

```json
{ "id": "across_documents_release_inventory_turns_against_finished_goods_build",
  "what_changed": "The release states inventory turns of 3.6. MD&A describes a finished-goods build to mitigate supply volatility (mdna:146), and the notes describe demand-driven reserve provisions (notes:86). The prose gives no direction for turns.",
  "account": "inventories (turns)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Inventory turns were 3.6.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:35",
  "explanation": false }
```

```json
{ "id": "earnings_quality_release_nubis_holdback_excluded_from_adjusted_results",
  "what_changed": "The release defines a 'Holdback arrangement' adjustment: part of the Nubis merger consideration was held back from key employee shareholders who joined Ciena. GAAP treats it as contingent compensation. Ciena excludes it from adjusted operating expense and adjusted EBITDA as not part of standard compensation. Appendix A (8k_2_02:68) and Appendix B (8k_2_02:71) show the line for Q2 fiscal 2026 and a dash for Q2 fiscal 2025. The prior release is not in input.",
  "account": "operating expense (acquisition-related compensation); adjusted operating expense; adjusted EBITDA",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "a one-time holdback of a portion of the merger consideration otherwise payable at closing to certain key employee shareholders of Nubis Communications, Inc. who became employees of Ciena, which is treated as contingent compensation for GAAP reporting purposes.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:77",
  "explanation": false }
```

```json
{ "id": "earnings_quality_release_non_gaap_tax_rate_stated",
  "what_changed": "The release says the non-GAAP tax provision uses a blended statutory rate of 20% for Q2 fiscal 2026 and 22% for Q2 fiscal 2025. It adds that the rate may change with tax policy or tax strategy. I report the two stated rates only. Their effect on adjusted EPS is for the numbers reader.",
  "account": "non-GAAP tax provision; adjusted net income per share",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "utilizes a current, blended U.S. and foreign statutory annual tax rate of 20% for the second quarter of fiscal 2026 and 22% for the second quarter of fiscal 2025",
  "paragraph_id": "0001628280-26-040614:8k_2_02:78",
  "explanation": false }
```

Item count: 44. `explanation` is true on 4 of them: notes:53, notes:86, mdna:145 and mdna:146.

## Paragraphs carried as text that are not items

### Notes (0001628280-26-040767:notes)
- notes:7: ASU 2023-09 paragraph. The note change history records no change; standing adoption text.
- notes:8: ASU 2024-03 paragraph. No change recorded; standing.
- notes:9: ASU 2025-05 paragraph. No change recorded; standing.
- notes:10: ASU 2025-06 paragraph. No change recorded; standing.
- notes:14: wording only ('respective periods' became 'periods indicated').
- notes:16: comparative-quarter disaggregation table. Amounts only; the row relabel is covered by the item on notes:15.
- notes:17: six-month disaggregation table, added because the period is now year-to-date. Amounts only.
- notes:18: six-month comparative disaggregation table. Amounts only.
- notes:20: wording only ('AI' spelled out).
- notes:42: wording only ('in' became 'using').
- notes:44: geographic revenue table. Amounts only, period rolled forward.
- notes:45: U.S. revenue sentence. Amounts rolled forward to quarter and six months.
- notes:51: wording only (comma removed).
- notes:52: contract balances table. Amounts only.
- notes:54: wording only ('on' became 'in').
- notes:55: deferred revenue recognized. Amounts and dates rolled forward.
- notes:57: deferred revenue table. Amounts only.
- notes:59: capitalized contract costs. Amounts rolled forward; trailing wording trimmed.
- notes:62: restructuring lead-in. Date rolled forward; no change recorded in history.
- notes:63: restructuring rollforward table. Amounts only.
- notes:65: restructuring lead-in for the comparative period. Date rolled forward.
- notes:66: comparative restructuring table. Amounts only.
- notes:68: interest and other income table. Amounts only.
- notes:72: investments heading and lead-in. No change recorded.
- notes:73: available-for-sale table. Amounts only.
- notes:74: comparative available-for-sale table. Amounts only.
- notes:75: maturity table lead-in. Date rolled forward.
- notes:76: maturity table. Amounts only.
- notes:78: fair value hierarchy table. Amounts only.
- notes:81: fair value by balance sheet line. Amounts only.
- notes:85: inventory components table. Amounts only.
- notes:89: accrued liabilities table. Amounts only.
- notes:92: warranty rollforward table. Amounts only.
- notes:95: cash flow hedge notionals. Amounts and dates rolled forward.
- notes:96: net investment hedge notionals. Amounts and dates rolled forward.
- notes:97: balance-sheet hedge notionals. Amounts and dates rolled forward.
- notes:100: interest rate swap notional. Date rolled forward.
- notes:101: forward-starting swap notional. Date rolled forward.
- notes:104: debt section heading.
- notes:105: subheading.
- notes:106: term loan description. No change recorded in history.
- notes:107: table lead-in. No change.
- notes:108: term loan carrying value table. Amounts only.
- notes:109: 'three months' became 'six months'. Period rolled forward.
- notes:110: term loan fair value. Amount and date rolled forward.
- notes:111: subheading.
- notes:112: subheading.
- notes:113: 2030 Notes description. No change recorded.
- notes:114: table lead-in. No change.
- notes:115: 2030 Notes carrying value table. Amounts only.
- notes:116: 'three months' became 'six months'. Period rolled forward.
- notes:117: 2030 Notes fair value. Amount and date rolled forward.
- notes:118: AOCI heading and lead-in. Date rolled forward.
- notes:119: AOCI table. Amounts only.
- notes:120: comparative AOCI lead-in. Date rolled forward.
- notes:121: comparative AOCI table. Amounts only.
- notes:125: EPS table. Amounts only.
- notes:128: repurchase program. Amounts rolled forward.
- notes:130: tax-withholding repurchases. Amount rolled forward.
- notes:132: share-based compensation table. Amounts only.
- notes:134: unrecognized compensation. Amounts rolled forward.
- notes:137: segment reconciliation description. No change recorded; the list of excluded items reads as standing.
- notes:138: segment profit table. Amounts only.
- notes:140: long-lived assets not reviewed by the CODM (chief operating decision maker). Amounts and date rolled forward.
- notes:141: table lead-in.
- notes:142: segment asset allocation table. Amounts only (read in the Blue Planet item).
- notes:145: long-lived assets by geography. Amounts only.
- notes:146: footnote. Unchanged.
- notes:147: heading.
- notes:148: tax contingencies sentence. No change recorded.
- notes:150: heading.
- notes:151: litigation paragraph re-joined after a split in the prior filing. The removed fragment in the history is the tail of the same sentence, so this is reflow only.
- notes:153: heading.
- notes:154: subsequent-event repurchases. Amounts and dates rolled forward.
- notes:155: standard lead-in to the trading-arrangement table. Covered by the item on notes:156.
- notes:157: footnote detailing the same arrangement. Covered by the item on notes:156.

### MD&A (0001628280-26-040767:mdna)
- mdna:12: amounts rolled forward. The WaveLogic and data-center strategy language cannot be checked for newness (insufficient, see below). The R&D driver is covered by the item on mdna:83.
- mdna:20: revenue growth amounts. The cause is the demand theme covered by the items on mdna:8.
- mdna:23: segment revenue table. Amounts only.
- mdna:27: heading.
- mdna:28: segment revenue amount only.
- mdna:29: Optical driver bullet naming core products (Waveserver, 6500 RLS). Amounts; no new account implication.
- mdna:31: Platform Software driver (Navigator NCS). Amounts; routine.
- mdna:33: Global Services driver (implementation, maintenance). Amounts; routine.
- mdna:34: heading.
- mdna:35: amount only.
- mdna:36: six-month version of mdna:29.
- mdna:37: six-month version of mdna:30. Covered.
- mdna:38: six-month Platform Software bullet; its software consulting offset is a first-quarter carry. Routine.
- mdna:39: six-month version of mdna:32. Covered.
- mdna:40: six-month version of mdna:33.
- mdna:44: geographic revenue table. Amounts only.
- mdna:48: heading.
- mdna:49: Americas driver (cloud and service providers in the United States). Routine.
- mdna:51: APAC driver (India service providers, Australia enterprise). Routine.
- mdna:52: heading.
- mdna:53: six-month Americas bullet. Amounts; routine.
- mdna:54: six-month EMEA bullet. Read in the item on mdna:50.
- mdna:55: six-month APAC bullet. Amounts; routine.
- mdna:57: share of revenue in non-U.S. currency and FX impact. Amounts rolled forward; 'minimal impact'.
- mdna:62: insufficient (see below).
- mdna:64: gross margin table. Amounts only.
- mdna:68: heading.
- mdna:69: summary of mdna:70 and mdna:71. Covered.
- mdna:72: heading.
- mdna:73: six-month summary. Covered.
- mdna:74: six-month version of mdna:70. Covered.
- mdna:75: six-month version of mdna:71. Covered.
- mdna:78: operating expense table. Amounts only.
- mdna:82: heading.
- mdna:84: selling and marketing driver (employee compensation). Routine.
- mdna:85: general and administrative driver (employee compensation). Routine.
- mdna:88: heading.
- mdna:89: six-month R&D bullet. Covered by the item on mdna:83.
- mdna:90: six-month selling and marketing bullet. Routine.
- mdna:91: six-month general and administrative bullet, which adds professional services. Routine.
- mdna:92: restructuring 'relatively unchanged'. No account implication.
- mdna:93: six-month amortization bullet. Covered by the item on mdna:87.
- mdna:96: share of operating expense in non-U.S. currency and FX impact. Amounts rolled forward; 'minimal impact'.
- mdna:99: segment profit table. Amounts only (read in the Blue Planet item).
- mdna:102: heading.
- mdna:103: Networking Platforms segment profit drivers. Routine.
- mdna:104: Platform Software segment profit drivers. Routine.
- mdna:106: Global Services segment profit driver. Routine.
- mdna:107: heading.
- mdna:108: six-month Networking Platforms. Routine.
- mdna:109: six-month Platform Software. Routine.
- mdna:111: six-month Global Services. Routine.
- mdna:114: non-operating items table. Amounts only.
- mdna:116: footnote.
- mdna:117: footnote.
- mdna:118: heading.
- mdna:119: other income FX driver. Amounts; routine.
- mdna:120: interest expense 'relatively unchanged'.
- mdna:122: heading.
- mdna:123: six-month other income FX driver. Routine.
- mdna:124: interest expense, lower floating rates net of hedging. Routine.
- mdna:126: six-month tax provision bullet. Covered by the item on mdna:121.
- mdna:129: liquidity sources and revolver terms. Amounts and dates rolled forward; standing.
- mdna:130: insufficient (see below).
- mdna:131: stock repurchases. Amounts rolled forward (the paragraph contains a doubled 'the').
- mdna:134: cash and investments table. Amounts only.
- mdna:135: sources and uses of cash. Amounts only.
- mdna:137: operating cash components. Amounts only.
- mdna:140: non-cash adjustments table. Amounts only.
- mdna:142: working-capital lead-in. Amounts only.
- mdna:143: working-capital table. Amounts only.
- mdna:144: lead-in.
- mdna:153: interest paid table. Amounts only.
- mdna:154: term loan rate. Amount rolled forward.
- mdna:156: swaps. Standing.
- mdna:157: revolver usage. Standing.
- mdna:160: contractual obligations lead-in. Its 'except for the item listed below' is cited in the item on notes:152.

### Item 4 (0001628280-26-040767:item_4_controls)
- item_4_controls:1: heading.
- item_4_controls:2: heading.
- item_4_controls:3: page number.
- item_4_controls:4: disclosure controls effective. Standard conclusion, no change.
- item_4_controls:5: heading.
- item_4_controls:6: no change in ICFR (internal control over financial reporting). Standard. No acquisition carve-out is mentioned.

### 8-K Item 2.02 (0001628280-26-040614:8k_2_02)
- 8k_2_02:1: exhibit header.
- 8k_2_02:2: document label.
- 8k_2_02:3: release header.
- 8k_2_02:4: title.
- 8k_2_02:5: heading.
- 8k_2_02:6: reported revenue. Amounts only.
- 8k_2_02:7: adjusted EPS. Amounts only.
- 8k_2_02:10: dateline.
- 8k_2_02:11: CEO quote. Promotional; its 'dynamic supply environment' theme is covered by the supply items.
- 8k_2_02:12: CFO quote. Promotional.
- 8k_2_02:13: heading.
- 8k_2_02:14: heading.
- 8k_2_02:15: revenue amounts.
- 8k_2_02:16: heading.
- 8k_2_02:17: EPS amounts.
- 8k_2_02:18: table lead-in.
- 8k_2_02:19: summary table. Amounts only.
- 8k_2_02:20: footnote.
- 8k_2_02:21: heading.
- 8k_2_02:22: heading.
- 8k_2_02:23: repeats 8k_2_02:8. Covered.
- 8k_2_02:27: heading.
- 8k_2_02:28: repeats 8k_2_02:9. Covered.
- 8k_2_02:32: heading.
- 8k_2_02:36: quarter repurchases under the program. Amounts only.
- 8k_2_02:37: heading.
- 8k_2_02:38: segment revenue table. Amounts only.
- 8k_2_02:39: footnote.
- 8k_2_02:40: webcast logistics.
- 8k_2_02:41: webcast logistics.
- 8k_2_02:42: webcast logistics.
- 8k_2_02:43: page number.
- 8k_2_02:44: heading.
- 8k_2_02:45: forward-looking boilerplate that repeats the quotes.
- 8k_2_02:46: insufficient (see below).
- 8k_2_02:47: non-GAAP presentation boilerplate.
- 8k_2_02:48: guidance reconciliation boilerplate.
- 8k_2_02:49: company description.
- 8k_2_02:50: page number.
- 8k_2_02:51: statement header.
- 8k_2_02:52: statement header.
- 8k_2_02:53: statement header.
- 8k_2_02:54: statement header.
- 8k_2_02:55: income statement. Amounts only.
- 8k_2_02:56: dilutive share footnote. Amounts only.
- 8k_2_02:57: statement header.
- 8k_2_02:58: statement header.
- 8k_2_02:59: statement header.
- 8k_2_02:60: statement header.
- 8k_2_02:61: balance sheet. Amounts only.
- 8k_2_02:62: page number.
- 8k_2_02:63: statement header.
- 8k_2_02:64: statement header.
- 8k_2_02:65: statement header.
- 8k_2_02:66: statement header.
- 8k_2_02:67: cash flow statement. Amounts only.
- 8k_2_02:68: Appendix A reconciliation. Amounts only; its holdback and amortization lines are read in the items on 8k_2_02:77 and mdna:87.
- 8k_2_02:69: footnote. Amounts only.
- 8k_2_02:70: page number.
- 8k_2_02:71: Appendix B EBITDA. Amounts only.
- 8k_2_02:72: separator.
- 8k_2_02:73: lead-in.
- 8k_2_02:74: share-based compensation definition. Standard.
- 8k_2_02:75: restructuring definition. Standard.
- 8k_2_02:76: amortization definition. Standard.

### 8-K index and late-filing list
- The 2026-06-04 8-K (0001628280-26-040614, Items 2.02 and 9.01) is the release read above.
- The 2026-03-31 8-K (0001628280-26-022342, Item 5.07) falls in this period, but its body is not in input. Insufficient.
- Late-filing notifications: none on or before 2026-06-04. Nothing to report.

## Insufficient (count: 5)
- mdna:62: the generic sentence on what makes gross margin fluctuate is marked changed, but its prior text is not in input. I cannot tell whether a factor was added or dropped.
- mdna:130: the foreign cash and repatriation paragraph (about $92.3 million expected to be repatriated, the rest indefinitely reinvested, deferred tax liability accrued) is marked changed. Without the prior text I cannot tell whether the repatriation assertion is new or only a rolled amount.
- mdna:12: the R&D and strategy paragraph ('inside and around the data center') is marked changed. Beyond the amounts, I cannot tell whether the strategy language is new.
- 8k_2_02:46: the release's cautionary factor list (AI spending, supply constraints, tariffs). The prior release is not in input, so I cannot identify additions or removals.
- 8-K 0001628280-26-022342 (Item 5.07, 2026-03-31): body not in input.

## Sections absent from input
- Auditor's report: not present; the 10-Q contains none.
- Item 1A diff: not present.
- Exhibit 21 diff: not present.
- Exhibit 10: none pulled.
- Prior flags: none on record.
