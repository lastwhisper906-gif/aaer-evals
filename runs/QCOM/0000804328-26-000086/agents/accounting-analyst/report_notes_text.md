<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_notes_text — QCOM 10-Q 0000804328-26-000086 (third quarter fiscal 2026, ended June 28, 2026)

## Inputs

- Read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- Nothing forbidden is in the directory: no trend table, prices, abnormal returns, short interest, other companies' files, prior probabilities or outcome window. The 8-K earnings release (0000804328-26-000085) includes condensed financial statements. That is 8-K body text and is allowed.
- Missing from the directory: an auditor's report (the controls file holds only Item 4), an Item 1A diff, an Exhibit 21 diff and any Exhibit 10. I cannot report on them.
- Prior predictions: none on record, so there is nothing to carry forward.
- The 8-K item-code list has no paragraph ids. It shows an Item 3.02 filed 2026-06-24 (0001104659-26-077071), inside the quarter, but its body is not in my input. I cannot say what was issued. With no paragraph to quote, it is noted here and not made an item.
- Paragraphs marked `[same as prior period ...]` are not listed below.
- No arithmetic was done. Where two figures appear together, they are given as the text gives them.

## Items

```json
{ "id": "results_against_expectations_quarter_revenue_and_net_income_decline",
  "what_changed": "The overview is carried as changed text and now covers the third quarter of fiscal 2026. It says revenues decreased 4% and net income decreased 25% against the year-ago quarter. The prior-period overview wording is not in my input.",
  "account": "revenues; net income",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Revenues for the third quarter of fiscal 2026 were $9.9 billion, a decrease of 4% compared to the year ago quarter, with net income of $2.0 billion, a decrease of 25% compared to the year ago quarter.",
  "paragraph_id": "0000804328-26-000086:mdna:5",
  "explanation": false, "insufficient": false }
```


```json
{ "id": "earnings_quality_qsi_ipo_gains_lift_investment_income",
  "what_changed": "The overview now reports a $656 million increase in investment and other income. It says this came mainly from gains on initial public offerings of certain QSI equity investments. mdna:58 and mdna:112 give the same cause. The release (8k_2_02:66) says QSI results are left out of Non-GAAP because they are viewed as unrelated to operational performance.",
  "account": "investment and other income, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Investment and other income, net increased by $656 million compared to the year ago quarter, primarily due to higher net gains from initial public offerings of certain QSI equity investments.",
  "paragraph_id": "0000804328-26-000086:mdna:8",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_unrealized_marketable_equity_gains",
  "what_changed": "The footnote to net gains on marketable securities in the investment and other income table now says these gains are mainly net unrealized gains on certain marketable equity securities. In other words, they are mark-to-market gains, not cash realized.",
  "account": "net gains on marketable securities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Primarily consist of net unrealized gains related to certain marketable equity securities.",
  "paragraph_id": "0000804328-26-000086:notes:28",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_qsi_ipo_holdings_under_lockup",
  "what_changed": "The fair value footnote is carried as changed. It says the Level 1 equity securities are mainly shares in QSI investees that have completed IPOs, and that these shares are still under short-term lock-up restrictions on sale. Together with notes:28, the text says the quarter's unrealized gains sit in holdings the company cannot yet sell.",
  "account": "marketable securities (equity securities, Level 1); investment and other income, net",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Primarily consists of equity securities in certain QSI investees that have completed initial public offerings, which remain subject to short-term lock-up restrictions on the ability to sell.",
  "paragraph_id": "0000804328-26-000086:notes:60",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_observable_price_change_gains",
  "what_changed": "The nine-month QSI discussion now gives three causes for the EBT increase: $380 million of gains from investee IPOs, $207 million of gains from observable price changes on non-marketable equity investments, and a $136 million increase in the company's share of equity-method earnings. Observable-price-change gains are remeasurements of holdings that have no market price. mdna:59 gives the same causes for nine-month gains on other investments and equity-method earnings.",
  "account": "net gains on other investments; equity in net earnings of investees",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$207 million in higher net gains from observable price changes on certain of our non-marketable equity investments and a $136 million increase in our share of earnings in equity method investments",
  "paragraph_id": "0000804328-26-000086:mdna:114",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_lower_interest_income_lower_balances",
  "what_changed": "The text now says nine-month interest and dividend income decreased mainly because balances of interest-bearing securities were lower.",
  "account": "interest and dividend income",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease in interest and dividend income in the first nine months of fiscal 2026 was primarily due to lower balances of interest-bearing securities.",
  "paragraph_id": "0000804328-26-000086:mdna:59",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_data_center_revenue_from_acquisition",
  "what_changed": "The revenue bridge now shows $88 million of higher equipment and services revenues from the Data Center segment, mainly from the Alphawave acquisition in the first quarter of fiscal 2026. The nine-month figure is $182 million (mdna:26). The text credits this revenue to an acquisition, not to existing operations. Data Center is a nonreportable segment (notes:49), and the MD&A text I can see does not discuss its profitability.",
  "account": "equipment and services revenues (Data Center)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$88 million in higher equipment and services revenues from our Data Center segment, primarily driven by our acquisition of Alphawave in the first quarter of fiscal 2026",
  "paragraph_id": "0000804328-26-000086:mdna:21",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_gross_margin_decline_qct",
  "what_changed": "The text says gross margin percentage decreased in both the third quarter and the first nine months, mainly because QCT gross margin percentage decreased. This paragraph does not say why QCT gross margin fell. The release (8k_2_02:29) points to higher input costs.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Gross margin percentage decreased in the third quarter and first nine months of fiscal 2026 primarily due to a decrease in QCT gross margin percentage.",
  "paragraph_id": "0000804328-26-000086:mdna:30",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_research_and_development_lower_engineering_reimbursements",
  "what_changed": "The R&D bridge now puts a $244 million increase mainly down to lower non-recurring engineering cost reimbursements for product-related development work. The nine-month figure is $541 million and also cites employee-related expenses (mdna:39). The text says reported R&D increased partly because reimbursements that offset it were lower.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$244 million increase driven by higher costs related to the development of wireless and integrated circuit technologies (including investments in key growth and diversification opportunities), primarily driven by lower non-recurring engineering cost reimbursements for product-related development work",
  "paragraph_id": "0000804328-26-000086:mdna:35",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_share_based_compensation_named_as_rd_driver",
  "what_changed": "The R&D bridge lists a $101 million increase in share-based compensation expense for the quarter. The SG&A bridge lists $62 million (mdna:45). The nine-month figures are $269 million (mdna:40) and $184 million (mdna:50).",
  "account": "share-based compensation expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$101 million increase in share-based compensation expense",
  "paragraph_id": "0000804328-26-000086:mdna:36",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_acquisition_related_sga_expenses",
  "what_changed": "The nine-month SG&A bridge lists a $91 million increase in acquisition-related expenses. The Modular acquisition closed after quarter-end (notes:75), and the fourth-quarter guidance says its other items are mainly acquisition-related (8k_2_02:33).",
  "account": "selling, general and administrative expense (acquisition-related)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$91 million increase in acquisition-related expenses",
  "paragraph_id": "0000804328-26-000086:mdna:51",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_restructuring_severance_charges",
  "what_changed": "The note says other expenses for the quarter and the nine months were $68 million and $97 million of restructuring and restructuring-related charges, nearly all severance. mdna:55 says the same without amounts.",
  "account": "other expenses (restructuring)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Other expenses in the three months and nine months ended June 28, 2026 consisted of $68 million and $97 million in restructuring and restructuring-related charges (substantially all of which related to severance costs), respectively.",
  "paragraph_id": "0000804328-26-000086:notes:26",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "across_documents_restructuring_charge_amount_release_versus_note",
  "what_changed": "The release footnote lists $70 million of restructuring and restructuring-related charges among the items excluded from Non-GAAP for the quarter. The 10-Q note (notes:26) says other expenses for the quarter were $68 million of restructuring and restructuring-related charges. Both figures are given as stated. Reconciling them is the supervisor's job.",
  "account": "other expenses (restructuring)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Other items excluded from Non-GAAP results included $101 million of acquisition-related charges, $70 million of restructuring and restructuring-related charges",
  "paragraph_id": "0000804328-26-000085:8k_2_02:78",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "across_documents_european_commission_fine_interest_not_in_contingencies_note",
  "what_changed": "The release says $1 million of interest expense on a fine imposed by the European Commission in 2019 was excluded from Non-GAAP results. This means a liability for that fine is still accruing interest. Note 5 as it appears in my input (notes:39 to notes:46, all carried as text) covers only the ParkerVision and Arm matters and does not mention a European Commission fine.",
  "account": "interest expense; other current liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "$1 million of interest expense related to a fine imposed on us by the European Commission in 2019",
  "paragraph_id": "0000804328-26-000085:8k_2_02:78",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_may_change_within_twelve_months",
  "what_changed": "The text gives unrecognized tax benefits of $3.0 billion at June 28, 2026 and $2.7 billion at September 28, 2025. It says they could reasonably change within the next twelve months, but gives no cause and no direction. Whether and how the balance moved is for the numbers reader.",
  "account": "unrecognized tax benefits",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Unrecognized tax benefits were $3.0 billion and $2.7 billion at June 28, 2026 and September 28, 2025, respectively. We believe that it is reasonably possible that our unrecognized tax benefits will change within the next twelve months.",
  "paragraph_id": "0000804328-26-000086:mdna:68",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "results_against_expectations_automotive_price_mix_and_shipments",
  "what_changed": "The QCT bridge now gives two causes for higher automotive revenues: a $381 million increase in revenues per unit from favorable mix and higher average selling prices, and $223 million of higher shipments from new vehicle launches. The nine-month figures are $560 million and $551 million (mdna:87).",
  "account": "QCT revenues (automotive)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "higher automotive revenues, due to a $381 million increase in revenues per unit driven by favorable mix and higher average selling prices and $223 million in higher shipments primarily from new vehicle launches",
  "paragraph_id": "0000804328-26-000086:mdna:79",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_qct_ebt_margin_decline_drivers_not_visible",
  "what_changed": "The lead-in says QCT EBT as a percentage of revenues decreased in the third quarter. The cause bullets below it (mdna:82, mdna:83) are marked unchanged from paragraphs in the prior filing that are not in my input. I cannot say what causes the company gives this quarter.",
  "account": "QCT EBT",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "QCT EBT as a percentage of revenues decreased in the third quarter of fiscal 2026 primarily due to:",
  "paragraph_id": "0000804328-26-000086:mdna:81",
  "explanation": false, "insufficient": true }
```

```json
{ "id": "narrative_signs_of_operating_pressure_lower_revenues_added_to_nine_month_qct_margin_drivers",
  "what_changed": "The nine-month list of reasons for the lower QCT EBT margin now has a bullet reading 'lower revenues'. It is carried as new text, while the bullets around it (mdna:90, mdna:91, mdna:93) are unchanged from the prior period's list. The nine-month lead-in (mdna:85) now reads 'The decrease in QCT revenues in the first nine months'. The prior six-month lead-in is not in my input.",
  "account": "QCT EBT; QCT revenues",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "lower revenues",
  "paragraph_id": "0000804328-26-000086:mdna:92",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "revenue_recognition_qtl_lower_estimated_cellular_sales",
  "what_changed": "The QTL bridge now puts part of the quarter's licensing revenue decrease down to a $67 million decrease in estimated sales of cellular products. In this bridge, QTL royalties rest on estimates of licensees' sales. The nine-month bridge (mdna:106) instead lists a $53 million increase in estimated sales. mdna:99 lists a $59 million increase in revenues per unit from favorable mix.",
  "account": "licensing revenues (QTL)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "$67 million decrease in estimated sales of cellular products",
  "paragraph_id": "0000804328-26-000086:mdna:97",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "revenue_recognition_qtl_lower_prior_period_royalties",
  "what_changed": "The QTL bridge lists $25 million less royalty revenue recognized on devices sold in prior periods for the quarter, and $65 million for the nine months (mdna:107). The revenue note's table of revenues from previously satisfied performance obligations (notes:21) gives this period's amounts.",
  "account": "licensing revenues (QTL)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "$25 million in lower royalty revenues recognized related to devices sold in prior periods",
  "paragraph_id": "0000804328-26-000086:mdna:98",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_qtl_higher_sga",
  "what_changed": "The text now says higher operating expenses, mainly higher SG&A, are one reason QTL EBT as a percentage of revenues decreased this quarter. It gives no cause for the higher SG&A.",
  "account": "QTL costs and expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "higher operating expenses, primarily driven by higher selling, general and administrative expenses",
  "paragraph_id": "0000804328-26-000086:mdna:101",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_supplier_cost_increases_on_margins",
  "what_changed": "The Looking Forward bullet is carried as changed. It describes a broad-based rise in input costs and capacity constraints across wafer fabrication, assembly, test, advanced packaging, memory and other materials, partly driven by demand for leading-edge technologies, AI and data center applications. It says the company keeps seeing higher product costs from certain key suppliers, which could negatively impact margins.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "As a result, we continue to see increased product costs from certain of our key suppliers, which could negatively impact our margins.",
  "paragraph_id": "0000804328-26-000086:mdna:120",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_supply_constraints_may_limit_revenue",
  "what_changed": "The same bullet warns that if supply and capacity constraints limit the components, manufacturing capacity or services available from suppliers, the company may not be able to fully meet customer demand. That could mean lost or delayed revenue.",
  "account": "revenues",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "if these supply and capacity constraints limit the availability of components, manufacturing capacity or related services from our suppliers, we may be unable to fully satisfy customer demand, which could result in lost or delayed revenue",
  "paragraph_id": "0000804328-26-000086:mdna:120",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_trade_policy_excess_obsolete_inventory_risk",
  "what_changed": "The trade-policy bullet is carried as changed, but the prior wording is not in my input, so I cannot isolate the edit. It says shifts in global trade policy make customer demand harder to estimate, which may lead to more excess or obsolete inventory or reserve charges. Read it with mdna:135, which says inventory increased.",
  "account": "inventories (excess and obsolete reserves)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Changes to global trade policies may negatively impact demand, pricing and cost for our products and technologies, and contribute to the inherent uncertainties in estimating future customer demand, which may result in increased excess or obsolete inventory or reserve charges, negatively impacting our results of operations and cash flows.",
  "paragraph_id": "0000804328-26-000086:mdna:121",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_current_notes_maturity_and_commercial_paper",
  "what_changed": "The debt footnote now says that at June 28, 2026 debt includes $2.0 billion classified as current and maturing in May 2027, plus $498 million of commercial paper reported as short-term debt. The credit facility was undrawn.",
  "account": "short-term debt",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Consists of our issued debt, including $2.0 billion classified as current and maturing in May 2027, and $498 million of outstanding commercial paper reported as short-term debt as of June 28, 2026. At June 28, 2026, our credit facility was undrawn.",
  "paragraph_id": "0000804328-26-000086:mdna:131",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_cash_decline_from_buybacks_dividends_capex_acquisitions",
  "what_changed": "The text says the nine-month net decrease in cash, cash equivalents and marketable securities (including restricted cash) came mainly from these uses: $6.8 billion of share repurchases (42 million shares), $2.9 billion of dividends, $1.6 billion of capital expenditures, $1.6 billion for acquisitions and other investments, and $888 million of tax withholdings on share-based awards. These were partly offset by operating cash flow and $495 million of net commercial paper proceeds.",
  "account": "cash, cash equivalents and marketable securities",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The net decrease in cash, cash equivalents and marketable securities (including restricted cash) for the first nine months of fiscal 2026 was primarily due to $6.8 billion in payments to repurchase 42 million shares of our common stock",
  "paragraph_id": "0000804328-26-000086:mdna:133",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_repurchases_offsetting_acquisition_share_issuance",
  "what_changed": "The text says the nine-month repurchases include buybacks that offset shares issued for the Alphawave acquisition. Modular closed on July 28, 2026, paid for mainly with 18 million shares (notes:75). The text does not say whether those shares will also be offset.",
  "account": "common stock repurchases; shares outstanding",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "(which includes repurchases that offset share issuances in connection with the acquisition of Alphawave)",
  "paragraph_id": "0000804328-26-000086:mdna:133",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_lower_future_cash_tax_payments",
  "what_changed": "The text says OBBB permanently restores immediate deduction of domestic R&D expenditures. It expects this to help cash flows from operations through significantly lower cash tax payments. notes:32 says the same.",
  "account": "net cash provided by operating activities (cash taxes)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We expect this change will have a favorable effect on our cash flows from operations due to significantly lower cash tax payments.",
  "paragraph_id": "0000804328-26-000086:mdna:134",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_final_repatriation_tax_installment_paid",
  "what_changed": "The text says income taxes paid in the nine months were greater than the provision. It gives two main reasons: the $5.7 billion valuation allowance release in the second quarter, and the final $663 million installment of the one-time U.S. repatriation tax accrued in fiscal 2018. Calling it the final installment implies no more payments of that tax.",
  "account": "income taxes paid; net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "our final installment payment for a one-time U.S. repatriation tax accrued in fiscal 2018 of $663 million",
  "paragraph_id": "0000804328-26-000086:mdna:134",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_inventory_build_memory_supply_constraints",
  "what_changed": "The text now says changes in operating assets and liabilities reduced operating cash flow, mainly because inventory increased. It ties the increase to certain customer demand impacts from memory supply constraints. This is management's stated cause for the inventory increase.",
  "account": "inventories",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Net changes in our operating assets and liabilities for the first nine months of fiscal 2026 negatively impacted our operating cash flows primarily driven by an increase in inventory reflecting certain customer demand impacts from memory supply constraints",
  "paragraph_id": "0000804328-26-000086:mdna:135",
  "explanation": true, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_advance_supply_payments_utilized",
  "what_changed": "The text says other assets decreased mainly because earlier advance supply agreement payments were used up. notes:10 gives advance payments under multi-year capacity purchase commitments at June 28, 2026 and September 28, 2025, split between other current assets and other assets.",
  "account": "other current assets; other assets (advance supply payments)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease in other assets is primarily due to the utilization of prior advanced supply agreement payments.",
  "paragraph_id": "0000804328-26-000086:mdna:135",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_accrued_customer_incentives_and_payment_timing",
  "what_changed": "The text says payroll, benefits and other liabilities increased mainly because accrued customer incentives increased, partly due to the timing of related payments. Employee cash incentive payments partly offset this. This is management's stated cause for the customer-incentive accrual, which notes:11 shows as customer incentives and other customer-related liabilities.",
  "account": "other current liabilities (customer incentives and other customer-related liabilities)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in payroll, benefits and other liabilities is primarily due to an increase in accrued customer incentives, which included the impact of timing of related payments, partially offset by payments related to our employee cash incentive program.",
  "paragraph_id": "0000804328-26-000086:mdna:135",
  "explanation": true, "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_income_tax_disclosure_prospective_adoption",
  "what_changed": "On the December 2023 FASB income tax disclosure requirements, the text now says the company will adopt them for annual periods starting in fiscal 2026 on a prospective basis. The prior text only said they could be applied on a retrospective or prospective basis (note_history:7). The company has now chosen its transition method.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "We will adopt the new requirements for our annual periods starting in fiscal 2026 on a prospective basis.",
  "paragraph_id": "0000804328-26-000086:notes:6",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_short_term_debt_schedule_added",
  "what_changed": "The note history marks a short-term debt schedule as added, with no prior note (note_history:8). It lists commercial paper and the current portion of long-term debt at June 28, 2026 and September 28, 2025.",
  "account": "short-term debt",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Short-term Debt (in millions)",
  "paragraph_id": "0000804328-26-000086:notes:12",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_interest_rate_swap_notional_stated",
  "what_changed": "The note describes interest rate swaps designated as fair value hedges, which convert fixed-rate payments to floating on part of long-term debt. Aggregate notional amounts are $5.0 billion at June 28, 2026 and $3.6 billion at September 28, 2025. The text gives no reason, and whether the notional changed is for the numbers reader.",
  "account": "interest expense; long-term debt",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "we had outstanding interest rate swaps with an aggregate notional amount of $5.0 billion and $3.6 billion, respectively, that are designated as fair value hedges",
  "paragraph_id": "0000804328-26-000086:notes:13",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_iot_category_redefined",
  "what_changed": "The IoT footnote has replaced its old categories: consumer, edge networking, and industrial (including utilities). The new ones are personal AI and compute, and industrial, networking and robotics. The latter now covers handhelds, retail, tracking and logistics, and other commercial and home applications. Utilities no longer appears (note_history:10). The segment description in notes:49 uses the new categories too. The text does not say whether any revenue was reclassified.",
  "account": "QCT revenues (IoT)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "personal AI and compute (including personal computers (PCs), extended reality (XR) and other personal computing devices) and industrial, networking and robotics (including mobile broadband, wireless access points, handhelds, retail, tracking and logistics, and other commercial and home applications)",
  "paragraph_id": "0000804328-26-000086:notes:19",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "revenue_recognition_key_oem_license_expirations",
  "what_changed": "The remaining performance obligations paragraph is carried as changed, though I cannot see the exact edit. It says patent license agreements with key OEMs have remaining terms that expire between fiscal 2027 and 2031, and that the company usually tries to renew or renegotiate before they expire. Under the fiscal year described in notes:3, fiscal 2027 starts at the end of September 2026.",
  "account": "licensing revenues (QTL)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Our patent license agreements with key OEMs are generally long-term, with remaining terms expiring between fiscal 2027 and 2031. We generally seek to renew or renegotiate such license agreements prior to expiration.",
  "paragraph_id": "0000804328-26-000086:notes:22",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_annual_effective_tax_rate_estimate",
  "what_changed": "The tax note now estimates the fiscal 2026 annual effective tax rate at a 40% benefit, mainly because of the $5.7 billion valuation allowance release in the second quarter. It says the third-quarter rate of 19% is higher than the estimated annual rate for that same reason. It attributes the year-ago quarter's 10% to net discrete tax benefits. The prior-period estimate is not in my input.",
  "account": "income tax expense (benefit)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "We estimate our annual effective income tax rate to be 40% benefit for fiscal 2026, primarily due to the $5.7 billion benefit in the second quarter of fiscal 2026 from releasing of our valuation allowance on our federal deferred tax assets.",
  "paragraph_id": "0000804328-26-000086:notes:32",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_fddei_benefit_reduced_by_research_expensing",
  "what_changed": "The tax note says FDDEI benefits for fiscal 2026 will be reduced compared to fiscal 2025, because domestic R&D expenditures can now be deducted currently under OBBB. The same note says this deduction lowers cash taxes.",
  "account": "income tax expense",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Such benefits from FDDEI for fiscal 2026 will be reduced compared to fiscal 2025 as a result of the current deduction of domestic R&D expenditures under OBBB.",
  "paragraph_id": "0000804328-26-000086:notes:32",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_parkervision_appeal_hearing_held",
  "what_changed": "New: the Federal Circuit heard ParkerVision's appeal on June 1, 2026 (note_history:1). The company still records no accrual for the matters described (notes:46).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "ParkerVision has appealed to the Federal Circuit, and a hearing on the appeal was held on June 1, 2026.",
  "paragraph_id": "0000804328-26-000086:notes:41",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_arm_good_faith_claim_added",
  "what_changed": "New: on March 30, 2026 the complaint against Arm Ltd. was amended to add a claim that Arm breached the Qualcomm ALA by failing to negotiate certain license terms in good faith (note_history:4).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "On March 30, 2026, our complaint against Arm Ltd. was amended to include an additional claim for breach of the Qualcomm ALA based on Arm’s failure to negotiate certain license terms in good faith.",
  "paragraph_id": "0000804328-26-000086:notes:44",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_arm_motion_to_strike_denied_trial_pending",
  "what_changed": "New: on July 14, 2026 the court denied Arm's motion to strike the amended complaint. Removed: the sentence 'Arm has moved to dismiss our amended complaint.' The trial date is still October 5, 2026, which is after the filing date (note_history:4).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The court denied Arm’s motion to strike our amended complaint against Arm Ltd. on July 14, 2026. Trial is scheduled to begin on October 5, 2026.",
  "paragraph_id": "0000804328-26-000086:notes:44",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_modular_acquisition_completed",
  "what_changed": "New subsequent-event paragraph; note_history:11 marks it as added. The Modular acquisition closed on July 28, 2026. It is valued at about $3.1 billion based on Qualcomm's closing stock price, and was paid for mainly with 18 million newly issued common shares. The note says it is not yet practicable to disclose the preliminary purchase price allocation. The release headline (8k_2_02:14) announces the same deal.",
  "account": "goodwill; other intangible assets; shares outstanding",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "The transaction values Modular at approximately $3.1 billion based on the closing price of Qualcomm stock on the acquisition date, with consideration transferred consisting primarily of 18 million shares issued of our common stock.",
  "paragraph_id": "0000804328-26-000086:notes:75",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_modular_executive_shares_compensation_expense",
  "what_changed": "Of the Modular consideration, 4 million shares (fair value about $700 million) went to certain executives and carry a four-year service requirement. Part of their value will be recognized as compensation expense and the rest counted in the purchase price.",
  "account": "share-based compensation expense",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "This included 4 million shares with an estimated fair value of approximately $700 million that were issued to certain executives and are subject to a four-year service requirement post-acquisition, of which a portion will be recognized as compensation expense and the remaining amount included as a component of the purchase price.",
  "paragraph_id": "0000804328-26-000086:notes:75",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_seven_other_business_acquisitions",
  "what_changed": "The paragraph is carried as changed. It says that in the first nine months the company bought seven other businesses for a total accounting purchase price of $1.1 billion. These brought $295 million of intangible assets and $737 million of goodwill, with $661 million of the goodwill allocated to QCT and $76 million to the Data Center operating segment. The goodwill is mainly attributed to assembled workforce and expected synergies. The prior period's count and amounts are not in my input.",
  "account": "goodwill; other intangible assets",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "During the first nine months of fiscal 2026, we acquired seven other businesses for a total accounting purchase price of $1.1 billion.",
  "paragraph_id": "0000804328-26-000086:notes:76",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_alphawave_purchase_price_allocation_table_changed",
  "what_changed": "The Alphawave purchase price allocation table is carried as changed from the prior filing. The surrounding Alphawave text (notes:67, notes:68, notes:70, notes:72 to notes:74) is unchanged, and nothing in my input describes a measurement-period adjustment. I cannot tell which lines moved or why.",
  "account": "goodwill",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "In-process research and development (IPR&D)",
  "paragraph_id": "0000804328-26-000086:notes:71",
  "explanation": false, "insufficient": true }
```

```json
{ "id": "across_documents_release_headlines_feature_non_handset_growth",
  "what_changed": "The release headlines highlight 28% combined growth in QCT automotive and IoT revenues and 23 consecutive quarters of double-digit automotive growth. No headline mentions handsets. Yet the release's own QCT revenue table (8k_2_02:24) shows handsets with a change of (20%), and the MD&A (mdna:6) blames lower handset revenues for the QCT decrease.",
  "account": "QCT revenues",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Combined QCT Automotive and IoT Revenues Grew 28% Year-Over-Year",
  "paragraph_id": "0000804328-26-000085:8k_2_02:12",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_and_supply_environment",
  "what_changed": "The CEO's quote opens with 'Despite a challenging memory and supply environment'. Separately, the MD&A (mdna:135) ties the inventory increase to customer demand impacts from memory supply constraints.",
  "account": "QCT revenues; inventories",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Despite a challenging memory and supply environment",
  "paragraph_id": "0000804328-26-000085:8k_2_02:16",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "results_against_expectations_revenue_at_high_end_of_guidance",
  "what_changed": "The CEO says quarterly revenues came in at the high end of guidance. The prior quarter's guidance is not in my input.",
  "account": "revenues",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "with quarterly revenues at the high end of guidance",
  "paragraph_id": "0000804328-26-000085:8k_2_02:16",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "results_against_expectations_non_handset_long_range_target",
  "what_changed": "The CEO cites an Investor Day target of $40 billion in total non-handset revenues by fiscal 2029. The release calls this nearly double the target shared in November 2024. The target year is beyond the horizon field's 12 months.",
  "account": "non-handset revenues (automotive, IoT, Data Center)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "with total non-handset revenues growing to $40 billion by fiscal 2029",
  "paragraph_id": "0000804328-26-000085:8k_2_02:16",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "results_against_expectations_non_handset_growth_acceleration_next_fiscal_year",
  "what_changed": "The CEO says year-over-year growth in non-handset revenues, including Data Center, should accelerate from 24% in fiscal 2026 to more than 60% in fiscal 2027.",
  "account": "non-handset revenues (automotive, IoT, Data Center)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "we expect year-over-year growth in non-handset revenues, including Data Center, to accelerate from 24% in fiscal 2026 to greater than 60% in fiscal 2027",
  "paragraph_id": "0000804328-26-000085:8k_2_02:16",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_quarterly_capital_return_release",
  "what_changed": "The release says the company returned $2.3 billion in the third quarter: $973 million of dividends ($0.92 per share) and $1.4 billion of repurchases covering 8 million shares.",
  "account": "cash; shares outstanding",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "During the third quarter of fiscal 2026, we returned $2.3 billion to stockholders, including $973 million, or $0.92 per share, of cash dividends paid and $1.4 billion through repurchases of 8 million shares of common stock.",
  "paragraph_id": "0000804328-26-000085:8k_2_02:27",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_input_costs_in_results_and_guidance",
  "what_changed": "The release's Business Outlook describes a broad-based rise in industry input costs across wafer fabrication, assembly, test, advanced packaging, memory and other materials. It says these factors show up in both third-quarter performance and fourth-quarter guidance.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "These factors are reflected in both our fiscal 2026 third quarter performance and fourth quarter guidance.",
  "paragraph_id": "0000804328-26-000085:8k_2_02:29",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "across_documents_pricing_actions_in_release_not_in_mdna",
  "what_changed": "The release says the company is taking concrete steps to pass the higher input costs into product pricing. It expects this to help gross margins over time as the price changes gradually take effect. The changed MD&A Looking Forward paragraph on the same costs (mdna:120) says they could hurt margins and, in the text I can see, does not mention any pricing actions.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We are taking concrete actions to reflect the higher input costs in our product pricing and expect these actions to benefit our gross margins over time as the pricing changes gradually come into effect.",
  "paragraph_id": "0000804328-26-000085:8k_2_02:29",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "results_against_expectations_fourth_quarter_guidance_ranges",
  "what_changed": "Fourth-quarter fiscal 2026 guidance: revenues $9.7B to $10.5B (QCT $8.4B to $9.0B, QTL $1.2B to $1.4B); GAAP diluted EPS $1.22 to $1.42; share-based compensation ($0.72) and other items ($0.11) per diluted share; Non-GAAP diluted EPS $2.05 to $2.25. The footnote (8k_2_02:32) says guidance includes pending business combinations expected to close in the quarter. I make no comparison with the third quarter.",
  "account": "revenues; diluted EPS",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Current Guidance Q4 FY26 Estimates",
  "paragraph_id": "0000804328-26-000085:8k_2_02:31",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_fourth_quarter_guidance_acquisition_related_items",
  "what_changed": "The release says the fourth-quarter EPS guidance for other items is mainly acquisition-related. Modular closed on July 28, 2026, inside that quarter (notes:75).",
  "account": "acquisition-related charges",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Our guidance for diluted EPS attributable to other items for the fourth quarter of fiscal 2026 is primarily related to acquisition-related items.",
  "paragraph_id": "0000804328-26-000085:8k_2_02:33",
  "explanation": false, "insufficient": false }
```

```json
{ "id": "earnings_quality_fixed_non_gaap_tax_rate_adjustment",
  "what_changed": "The release says the Other Items tax adjustment brings Non-GAAP tax to a fixed estimated rate of 12.5% for the quarter. The adjustment includes the effect of amortizing previously capitalized domestic R&D for U.S. federal tax. The initial benefit of that capitalization was earlier excluded from Non-GAAP. By its own text (8k_2_02:71), the fixed-rate method has applied since the first quarter of fiscal 2026.",
  "account": "income tax expense (Non-GAAP)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "represents an adjustment to arrive at our fixed estimated Non-GAAP tax rate of 12.5% for the third quarter of fiscal 2026 and includes the impact of the amortization of previously capitalized domestic research and development expenditures for U.S. federal income tax purposes (for which the initial benefit was previously excluded from our Non-GAAP results)",
  "paragraph_id": "0000804328-26-000085:8k_2_02:79",
  "explanation": false, "insufficient": false }
```

## Counts

- Items: 58
- Items with `explanation: true`: 2 (inventory increase from memory supply constraints; accrued customer incentives and payment timing)
- Items with `insufficient: true`: 2 (QCT EBT margin causes carried as unchanged and not visible; Alphawave allocation table changed with no text explaining it)

## Paragraphs carried as text with no item

### Item 4 (controls)
- 0000804328-26-000086:item_4_controls:1 — heading
- 0000804328-26-000086:item_4_controls:2 — disclosure controls concluded effective; standard conclusion, no change in substance
- 0000804328-26-000086:item_4_controls:3 — no ICFR changes; quarter rolled forward
- 0000804328-26-000086:item_4_controls:4 — page number

### MD&A
- 0000804328-26-000086:mdna:4 — heading; period rolled forward
- 0000804328-26-000086:mdna:7 — QTL decrease summary; cause covered by revenue_recognition_qtl_lower_estimated_cellular_sales and revenue_recognition_qtl_lower_prior_period_royalties
- 0000804328-26-000086:mdna:12 — corporate-structure boilerplate, re-split across a page break with mdna:13; wording only
- 0000804328-26-000086:mdna:13 — continuation of mdna:12; wording only
- 0000804328-26-000086:mdna:16 — amounts only (revenue table)
- 0000804328-26-000086:mdna:17 — heading; period rolled forward
- 0000804328-26-000086:mdna:18 — lead-in; period rolled forward
- 0000804328-26-000086:mdna:19 — amount in a recurring revenue-bridge bullet; cause covered by narrative_signs_of_operating_pressure_handset_revenue_decline
- 0000804328-26-000086:mdna:20 — amount in a recurring revenue-bridge bullet; covered by the QTL revenue items
- 0000804328-26-000086:mdna:22 — heading
- 0000804328-26-000086:mdna:23 — lead-in
- 0000804328-26-000086:mdna:24 — nine-month QCT amount; covered by narrative_signs_of_operating_pressure_lower_revenues_added_to_nine_month_qct_margin_drivers
- 0000804328-26-000086:mdna:26 — nine-month version of mdna:21; amount only; covered by earnings_quality_data_center_revenue_from_acquisition
- 0000804328-26-000086:mdna:27 — nine-month QTL amount; covered by the QTL revenue items
- 0000804328-26-000086:mdna:28 — amounts only (cost of revenues and gross margin table)
- 0000804328-26-000086:mdna:29 — heading
- 0000804328-26-000086:mdna:31 — page number
- 0000804328-26-000086:mdna:32 — amounts only (R&D table)
- 0000804328-26-000086:mdna:33 — heading
- 0000804328-26-000086:mdna:34 — lead-in
- 0000804328-26-000086:mdna:37 — heading
- 0000804328-26-000086:mdna:38 — lead-in
- 0000804328-26-000086:mdna:39 — nine-month version of mdna:35; covered by earnings_quality_research_and_development_lower_engineering_reimbursements
- 0000804328-26-000086:mdna:40 — nine-month share-based compensation amount; covered by earnings_quality_share_based_compensation_named_as_rd_driver
- 0000804328-26-000086:mdna:42 — amounts only (SG&A table)
- 0000804328-26-000086:mdna:43 — heading
- 0000804328-26-000086:mdna:44 — lead-in
- 0000804328-26-000086:mdna:45 — share-based compensation amount in SG&A; covered by earnings_quality_share_based_compensation_named_as_rd_driver
- 0000804328-26-000086:mdna:46 — amount in the recurring sales-and-marketing bullet; standard cause wording
- 0000804328-26-000086:mdna:47 — amount; by its own text, the deferred compensation revaluation is offset in investment income
- 0000804328-26-000086:mdna:48 — heading
- 0000804328-26-000086:mdna:49 — lead-in
- 0000804328-26-000086:mdna:50 — nine-month share-based compensation amount; covered by earnings_quality_share_based_compensation_named_as_rd_driver
- 0000804328-26-000086:mdna:52 — nine-month sales-and-marketing amount; recurring bullet
- 0000804328-26-000086:mdna:53 — amounts only (other expense table)
- 0000804328-26-000086:mdna:54 — heading
- 0000804328-26-000086:mdna:55 — same content as notes:26, without amounts; covered by narrative_signs_of_operating_pressure_restructuring_severance_charges
- 0000804328-26-000086:mdna:57 — amounts only (interest expense and investment income table)
- 0000804328-26-000086:mdna:58 — same cause as mdna:8; covered by earnings_quality_qsi_ipo_gains_lift_investment_income
- 0000804328-26-000086:mdna:62 — amounts only (tax reconciliation table; includes a foreign-currency line on the foreign withholding tax receivable that no text explains)
- 0000804328-26-000086:mdna:64 — OBBB background, re-split across a page break; wording only
- 0000804328-26-000086:mdna:66 — background on the fiscal 2025 valuation allowance, re-split; wording only
- 0000804328-26-000086:mdna:70 — cross-reference; period rolled forward
- 0000804328-26-000086:mdna:72 — amounts only (QCT table)
- 0000804328-26-000086:mdna:75 — amounts rolled forward; standard product description
- 0000804328-26-000086:mdna:76 — heading
- 0000804328-26-000086:mdna:77 — lead-in
- 0000804328-26-000086:mdna:84 — heading
- 0000804328-26-000086:mdna:85 — lead-in; covered by narrative_signs_of_operating_pressure_lower_revenues_added_to_nine_month_qct_margin_drivers
- 0000804328-26-000086:mdna:87 — nine-month version of mdna:79; covered by results_against_expectations_automotive_price_mix_and_shipments
- 0000804328-26-000086:mdna:89 — lead-in; covered by narrative_signs_of_operating_pressure_lower_revenues_added_to_nine_month_qct_margin_drivers
- 0000804328-26-000086:mdna:94 — amounts only (QTL table)
- 0000804328-26-000086:mdna:95 — heading
- 0000804328-26-000086:mdna:96 — lead-in
- 0000804328-26-000086:mdna:99 — offsetting cause, amount only; covered by revenue_recognition_qtl_lower_estimated_cellular_sales
- 0000804328-26-000086:mdna:100 — lead-in; covered by narrative_signs_of_operating_pressure_qtl_higher_sga
- 0000804328-26-000086:mdna:102 — "lower revenues" bullet for QTL; covered by the QTL revenue items
- 0000804328-26-000086:mdna:103 — heading
- 0000804328-26-000086:mdna:104 — lead-in
- 0000804328-26-000086:mdna:105 — nine-month amount; covered by revenue_recognition_qtl_lower_estimated_cellular_sales
- 0000804328-26-000086:mdna:106 — nine-month amount; covered by revenue_recognition_qtl_lower_estimated_cellular_sales
- 0000804328-26-000086:mdna:107 — nine-month amount; covered by revenue_recognition_qtl_lower_prior_period_royalties
- 0000804328-26-000086:mdna:108 — nine-month QTL margin described as approximately flat; amounts and wording only
- 0000804328-26-000086:mdna:110 — amounts only (QSI table)
- 0000804328-26-000086:mdna:111 — heading
- 0000804328-26-000086:mdna:112 — same cause as mdna:8; covered by earnings_quality_qsi_ipo_gains_lift_investment_income
- 0000804328-26-000086:mdna:113 — heading
- 0000804328-26-000086:mdna:124 — litigation boilerplate pointing to Note 5
- 0000804328-26-000086:mdna:128 — sources of liquidity; dates rolled forward
- 0000804328-26-000086:mdna:129 — amounts only (liquidity table)
- 0000804328-26-000086:mdna:132 — amounts only (cash flow summary)
- 0000804328-26-000086:mdna:137 — "no other material changes" statement; date rolled forward
- 0000804328-26-000086:mdna:138 — regulatory and litigation boilerplate

### Notes
- 0000804328-26-000086:notes:3 — dates rolled forward (note_history:6)
- 0000804328-26-000086:notes:9 — amounts only (inventory components)
- 0000804328-26-000086:notes:10 — amounts rolled forward; topic covered by liquidity_and_capital_advance_supply_payments_utilized
- 0000804328-26-000086:notes:11 — amounts only; customer-incentive line covered by estimates_and_discretion_accrued_customer_incentives_and_payment_timing
- 0000804328-26-000086:notes:16 — amounts only (QCT disaggregation; note_history:9)
- 0000804328-26-000086:notes:21 — amounts only; covered by revenue_recognition_qtl_lower_prior_period_royalties
- 0000804328-26-000086:notes:24 — amounts only (customer concentration; the legend for "*" is in notes:25, which is marked unchanged and not visible)
- 0000804328-26-000086:notes:27 — amounts only (investment and other income table)
- 0000804328-26-000086:notes:34 — amounts and dates rolled forward; the program was announced March 17, 2026, in the prior quarter
- 0000804328-26-000086:notes:35 — date rolled forward
- 0000804328-26-000086:notes:36 — amounts only (share roll-forward)
- 0000804328-26-000086:notes:38 — amounts only (dilutive shares)
- 0000804328-26-000086:notes:39 — heading
- 0000804328-26-000086:notes:40 — heading
- 0000804328-26-000086:notes:42 — paragraph boundary moved; text unchanged per note_history:2 and note_history:3
- 0000804328-26-000086:notes:43 — paragraph boundary moved; text unchanged per note_history:3
- 0000804328-26-000086:notes:45 — no change shown in the note history; events from 2024 and 2025
- 0000804328-26-000086:notes:46 — date rolled forward (note_history:5); still no accrual
- 0000804328-26-000086:notes:48 — segment organization wording; no visible change in substance
- 0000804328-26-000086:notes:49 — IoT wording covered by structure_and_disclosure_changes_iot_category_redefined
- 0000804328-26-000086:notes:52 — amounts only (segment table)
- 0000804328-26-000086:notes:55 — amounts only (segment reconciliation)
- 0000804328-26-000086:notes:56 — period rolled forward
- 0000804328-26-000086:notes:58 — date rolled forward
- 0000804328-26-000086:notes:59 — amounts only (fair value table)
- 0000804328-26-000086:notes:61 — boilerplate footnote (deferred compensation, Level 1)
- 0000804328-26-000086:notes:62 — amount rolled forward
- 0000804328-26-000086:notes:63 — date rolled forward
- 0000804328-26-000086:notes:65 — amounts only (maturity table)
- 0000804328-26-000086:notes:69 — date rolled forward (exchangeable shares outstanding as of June 28, 2026); terms as previously disclosed
- 0000804328-26-000086:notes:77 — no trading arrangements adopted or terminated; quarter rolled forward

### 8-K item 2.02 (exhibit 99.1)
- 0000804328-26-000085:8k_2_02:1 — exhibit header
- 0000804328-26-000085:8k_2_02:2 — document header
- 0000804328-26-000085:8k_2_02:3 — exhibit label
- 0000804328-26-000085:8k_2_02:4 — release header
- 0000804328-26-000085:8k_2_02:5 — contact header
- 0000804328-26-000085:8k_2_02:6 — investor relations contact name
- 0000804328-26-000085:8k_2_02:7 — contact title
- 0000804328-26-000085:8k_2_02:8 — contact phone and email
- 0000804328-26-000085:8k_2_02:9 — release title
- 0000804328-26-000085:8k_2_02:10 — headline amount only
- 0000804328-26-000085:8k_2_02:11 — headline amounts only
- 0000804328-26-000085:8k_2_02:13 — automotive growth-streak headline; covered by across_documents_release_headlines_feature_non_handset_growth
- 0000804328-26-000085:8k_2_02:14 — Modular headline; covered by related_parties_contingencies_and_subsequent_events_modular_acquisition_completed
- 0000804328-26-000085:8k_2_02:15 — dateline
- 0000804328-26-000085:8k_2_02:17 — heading
- 0000804328-26-000085:8k_2_02:18 — amounts only (results table)
- 0000804328-26-000085:8k_2_02:19 — Non-GAAP reference footnote; boilerplate
- 0000804328-26-000085:8k_2_02:20 — heading
- 0000804328-26-000085:8k_2_02:21 — amounts only (segment table)
- 0000804328-26-000085:8k_2_02:22 — page header
- 0000804328-26-000085:8k_2_02:23 — heading
- 0000804328-26-000085:8k_2_02:24 — amounts only (QCT revenue streams); handsets row cited in across_documents_release_headlines_feature_non_handset_growth
- 0000804328-26-000085:8k_2_02:25 — disaggregation footnote; boilerplate
- 0000804328-26-000085:8k_2_02:26 — heading
- 0000804328-26-000085:8k_2_02:28 — heading
- 0000804328-26-000085:8k_2_02:30 — lead-in to guidance table
- 0000804328-26-000085:8k_2_02:32 — outlook exclusions footnote; boilerplate (cited in results_against_expectations_fourth_quarter_guidance_ranges)
- 0000804328-26-000085:8k_2_02:34 — page header
- 0000804328-26-000085:8k_2_02:35 — heading
- 0000804328-26-000085:8k_2_02:36 — conference call logistics
- 0000804328-26-000085:8k_2_02:37 — conference call logistics
- 0000804328-26-000085:8k_2_02:38 — investor relations website boilerplate
- 0000804328-26-000085:8k_2_02:39 — heading
- 0000804328-26-000085:8k_2_02:40 — corporate description; marketing wording
- 0000804328-26-000085:8k_2_02:41 — corporate structure and trademark boilerplate
- 0000804328-26-000085:8k_2_02:42 — heading; the forward-looking statement text itself is not in my input
- 0000804328-26-000085:8k_2_02:43 — page header
- 0000804328-26-000085:8k_2_02:44 — heading
- 0000804328-26-000085:8k_2_02:45 — heading
- 0000804328-26-000085:8k_2_02:46 — heading
- 0000804328-26-000085:8k_2_02:47 — heading
- 0000804328-26-000085:8k_2_02:48 — amounts only (balance sheet)
- 0000804328-26-000085:8k_2_02:49 — page header
- 0000804328-26-000085:8k_2_02:50 — heading
- 0000804328-26-000085:8k_2_02:51 — heading
- 0000804328-26-000085:8k_2_02:52 — heading
- 0000804328-26-000085:8k_2_02:53 — heading
- 0000804328-26-000085:8k_2_02:54 — amounts only (statement of operations)
- 0000804328-26-000085:8k_2_02:55 — page header
- 0000804328-26-000085:8k_2_02:56 — heading
- 0000804328-26-000085:8k_2_02:57 — heading
- 0000804328-26-000085:8k_2_02:58 — heading
- 0000804328-26-000085:8k_2_02:59 — heading
- 0000804328-26-000085:8k_2_02:60 — amounts only (cash flow statement)
- 0000804328-26-000085:8k_2_02:61 — page header
- 0000804328-26-000085:8k_2_02:62 — heading
- 0000804328-26-000085:8k_2_02:63 — Non-GAAP boilerplate
- 0000804328-26-000085:8k_2_02:64 — Non-GAAP usage boilerplate
- 0000804328-26-000085:8k_2_02:65 — list of exclusions; boilerplate
- 0000804328-26-000085:8k_2_02:66 — reason for excluding QSI; boilerplate (cited in earnings_quality_qsi_ipo_gains_lift_investment_income)
- 0000804328-26-000085:8k_2_02:67 — reason for excluding share-based compensation; boilerplate
- 0000804328-26-000085:8k_2_02:68 — lead-in
- 0000804328-26-000085:8k_2_02:69 — definition of acquisition-related items; policy text, no visible change
- 0000804328-26-000085:8k_2_02:70 — definition of other excluded items; boilerplate
- 0000804328-26-000085:8k_2_02:71 — fixed Non-GAAP tax rate policy, dated by its own text to the first quarter of fiscal 2026; covered by earnings_quality_fixed_non_gaap_tax_rate_adjustment
- 0000804328-26-000085:8k_2_02:72 — page header
- 0000804328-26-000085:8k_2_02:73 — heading
- 0000804328-26-000085:8k_2_02:74 — amounts only (reconciliation table)
- 0000804328-26-000085:8k_2_02:75 — reconciliation footnote; boilerplate
- 0000804328-26-000085:8k_2_02:76 — rounding note
- 0000804328-26-000085:8k_2_02:77 — amounts only (supplemental reconciliation table)
- 0000804328-26-000085:8k_2_02:80 — rounding note

## Where each note-history entry leads (for tracing, not a second list)

- note_history:1 leads to notes:41 (item: parkervision_appeal_hearing_held)
- note_history:2 and note_history:3 lead to notes:42 and notes:43 (paragraph re-split only)
- note_history:4 leads to notes:44 (items: arm_good_faith_claim_added, arm_motion_to_strike_denied_trial_pending)
- note_history:5 leads to notes:46 (date rolled forward)
- note_history:6 leads to notes:3 (dates rolled forward)
- note_history:7 leads to notes:6 (item: income_tax_disclosure_prospective_adoption)
- note_history:8 leads to notes:12 (item: short_term_debt_schedule_added)
- note_history:9 leads to notes:16 (amounts only)
- note_history:10 leads to notes:19 (item: iot_category_redefined)
- note_history:11 leads to notes:75 (items: modular_acquisition_completed, modular_executive_shares_compensation_expense)
