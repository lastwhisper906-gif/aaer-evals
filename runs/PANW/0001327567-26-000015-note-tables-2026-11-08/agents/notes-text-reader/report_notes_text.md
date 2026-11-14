# Notes text reader: Palo Alto Networks, quarterly report for the third quarter of fiscal 2026 (accession 0001327567-26-000015, quarter ended April 30, 2026)

## What I read, and what was not there

- Read in full: the notes file (paragraphs notes:1 to notes:189), the note change history, the MD&A (mdna:1 to mdna:162), the controls file (Item 4 only), the current-report index and the prior-predictions file.
- Not in my directory: an auditor's report (the controls file carries Item 4 only), a risk-factor section diff, a subsidiaries-exhibit diff, any material-contract exhibit. The current-report file lists item codes only. It carries no item bodies, including for the earnings release dated June 2, 2026, so I cannot compare the release with the quarterly report.
- Prior predictions: none on record, so I have no earlier flags to carry forward.
- Nothing forbidden is in the directory: no trend table, no price series, no abnormal returns, no short interest, no other company's files, no prior probabilities, no outcome window. The per-share amounts I mention below (conversion prices, cap prices, the average repurchase price) are printed in the filing's own prose.
- Method: the note change history covers these text blocks: commitments and contingencies, accounting policies, debt, debt policy, investments, revenue and subsequent events. For those blocks I treat the history as the record of what is new. Where a paragraph comes as text but the history shows it unchanged, I list it below as unchanged. The other note blocks have no history, and neither does the MD&A. There a paragraph that comes as text has changed in some way, but its earlier wording is not in my input. Those items say "as carried", meaning they describe the current text without claiming exactly which words are new.
- I did no arithmetic. Where two amounts appear, I report them as the filing prints them and do not compare them.

## Items

```json
{ "id": "structure_and_disclosure_changes_cyberark_results_consolidated_from_acquisition_date",
  "what_changed": "New paragraph: CyberArk was acquired on February 11, 2026, forming the identity security platform, and its results are included only from that date. In the prior period CyberArk appeared only as a subsequent event. The business description (notes:2) now adds identities to what the platforms secure.",
  "account": "total revenue; operating expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The condensed consolidated financial statements include the financial results of CyberArk prospectively from the date of acquisition.",
  "paragraph_id": "0001327567-26-000015:notes:3",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_convertible_notes_and_capped_calls_join_estimate_list",
  "what_changed": "The list of management estimates now includes the fair value of convertible senior notes and capped calls. The prior period's list (removed paragraph, history 0001327567-26-000005:note_history:15) did not include it. Both instruments came with CyberArk and are remeasured every period.",
  "account": "convertible senior notes; capped calls in other assets; other income, net",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "fair value of convertible senior notes and capped calls",
  "paragraph_id": "0001327567-26-000015:notes:8",
  "explanation": false }
```

```json
{ "id": "earnings_quality_fair_value_option_on_acquired_convertible_notes",
  "what_changed": "New accounting policy: the company has elected the fair value option for the convertible senior notes acquired from CyberArk. The notes are remeasured at fair value every period through maturity or settlement. Changes in fair value go to other income, net, except the part due to the company's own credit risk, which goes to accumulated other comprehensive income. Because the notes are exchangeable into common stock, a non-operating line in earnings now moves with the company's own share price.",
  "account": "other income, net; convertible senior notes",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "we have elected fair value option to simplify the accounting for embedded features",
  "paragraph_id": "0001327567-26-000015:notes:13",
  "explanation": false }
```

```json
{ "id": "earnings_quality_capped_calls_marked_through_other_income",
  "what_changed": "New accounting policy: the assumed capped calls are carried as derivative assets in other assets, measured at fair value every period, with changes recorded in other income, net.",
  "account": "other assets; other income, net",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "We account for capped calls as derivative assets, measured at fair value on a recurring basis through maturity or settlement.",
  "paragraph_id": "0001327567-26-000015:notes:14",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_conclusion",
  "what_changed": "The prior period said the company was still evaluating the income tax disclosure standard that takes effect for fiscal 2026 annual periods. The note now concludes that adopting it will add jurisdiction-level tax disclosure. The effect is on disclosure only.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We expect the adoption of this standard will result in disclosure of additional jurisdictional level tax information in our consolidated financial statements.",
  "paragraph_id": "0001327567-26-000015:notes:17",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_credit_loss_expedient_not_expected_material",
  "what_changed": "The prior period said the company was evaluating the practical expedient for estimating expected credit losses on receivables and contract assets. The note now says adoption is not expected to have a material impact. The standard takes effect in the first quarter of fiscal 2027.",
  "account": "allowance for credit losses; accounts receivable; contract assets",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We do not expect the adoption of this standard will have a material impact on our consolidated financial statements.",
  "paragraph_id": "0001327567-26-000015:notes:21",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_qradar_undiscounted_payment_range",
  "what_changed": "As carried, the QRadar paragraph says payments to IBM began in the fiscal quarter ended October 2025 and are expected to continue through the fiscal quarter ending October 2028. It puts undiscounted contingent consideration at between $0.3 billion and $0.5 billion. The prior wording is not in my input, so I cannot say whether it was the range or the schedule that changed. Read this with the reduced payment estimate in notes:40.",
  "account": "contingent consideration liability",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The estimated range of undiscounted contingent consideration is between $0.3 billion and $0.5 billion.",
  "paragraph_id": "0001327567-26-000015:notes:38",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_qradar_contingent_payment_estimate_reduced",
  "what_changed": "New sentence: in the three months ended April 30, 2026, management reduced its estimate of future cash payments to IBM under the QRadar contingent consideration. It cites the magnitude and likelihood of customers entering into qualified new transactions, the competitive industry environment and current market conditions. The MD&A (mdna:112) books the effect as a $110 million gain inside general and administrative expense, and mdna:141 states the obligation at $240 million.",
  "account": "contingent consideration liability (accrued and other liabilities; other long-term liabilities)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "we reduced our estimate of future cash payments based on our quarterly assessment of assumptions",
  "paragraph_id": "0001327567-26-000015:notes:40",
  "explanation": true }
```

```json
{ "id": "narrative_signs_of_operating_pressure_fewer_qualified_qradar_transactions_expected",
  "what_changed": "The payments are owed only when QRadar customers enter qualified new transactions. The reasons now given for cutting the estimate are the magnitude and likelihood of such transactions and the competitive environment, so the prose implies fewer or smaller migrations of QRadar customers onto the company's platform than management previously expected.",
  "account": "subscription and support revenue from migrated QRadar customers",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "including the magnitude and likelihood of customers entering into qualified new transactions, the competitive industry environment, and current market conditions",
  "paragraph_id": "0001327567-26-000015:notes:40",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_cyberark_purchase_consideration_recorded",
  "what_changed": "The acquisition note now records the CyberArk deal: $45.00 in cash plus 2.2005 company shares for each CyberArk share, for total consideration of $21.1 billion. The table (notes:75) shows cash of $2,308 million, 112 million common shares at $18,488 million and replacement awards at $265 million. The prior period described the deal only as a subsequent event, and that subsequent-event paragraph has been removed.",
  "account": "goodwill; identified intangible assets; common stock and additional paid-in capital",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The total purchase consideration for the acquisition of CyberArk was $21.1 billion",
  "paragraph_id": "0001327567-26-000015:notes:74",
  "explanation": false }
```

```json
{ "id": "earnings_quality_cyberark_replacement_awards_future_expense",
  "what_changed": "New: $945 million of replacement equity awards were issued for CyberArk. The part for service before the acquisition date went into purchase consideration ($265 million per notes:75 and mdna:65). The rest will be expensed as share-based compensation over the remaining service periods. Footnote notes:162 adds that 7 million restricted stock units were assumed across the Chronosphere, CyberArk and Koi acquisitions.",
  "account": "share-based compensation expense",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "we issued $945 million of replacement equity awards, of which the portion attributable to services performed prior to the acquisition date was allocated to purchase consideration",
  "paragraph_id": "0001327567-26-000015:notes:76",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_cyberark_acquired_receivables_and_deferred_revenue",
  "what_changed": "New CyberArk allocation table. It brings onto the balance sheet at the acquisition date: accounts receivable, net ($312 million), short-term and long-term investments ($1,217 million), cash ($743 million), deferred revenue ($776 million), convertible senior notes ($1,303 million) and deferred tax liabilities ($274 million), along with goodwill ($14,802 million) and intangibles ($6,279 million). Over the nine months, part of the movement in receivables, deferred revenue and investments is acquired balance rather than operations. Whether these lines tie is the numbers reader's and the supervisor's call.",
  "account": "accounts receivable, net; deferred revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Accounts receivable, net of allowance for credit losses",
  "paragraph_id": "0001327567-26-000015:notes:77",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_cyberark_goodwill_tax_deductible",
  "what_changed": "New: CyberArk goodwill is attributed to the assembled workforce and expected synergies, and substantially all of it is deductible for U.S. income tax purposes. By contrast, the Chronosphere goodwill (notes:70) is stated as not deductible. Deductible goodwill means U.S. tax deductions in future periods.",
  "account": "cash paid for income taxes; deferred tax liabilities",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Substantially all of goodwill is deductible for U.S. income tax purposes.",
  "paragraph_id": "0001327567-26-000015:notes:78",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_cyberark_intangible_useful_lives",
  "what_changed": "New table of CyberArk intangibles and the useful lives management assigned: developed technology 5 to 7 years, platform renewals 12 to 14 years, customer contracts 2 years, trade name 1 year. The lives are management judgments that set the amortization charge. The intangible asset table (notes:105) now has customer contracts and trade name rows and a row labelled customer relationships and platform renewals.",
  "account": "amortization of intangible assets (cost of revenue; sales and marketing)",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Platform renewals",
  "paragraph_id": "0001327567-26-000015:notes:79",
  "explanation": false }
```

```json
{ "id": "earnings_quality_cyberark_transaction_costs_in_general_and_administrative",
  "what_changed": "New: CyberArk transaction costs were $41 million for the three months and $56 million for the nine months, mostly in general and administrative expense. These are acquisition-specific costs, not recurring ones.",
  "account": "general and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "transaction costs related to CyberArk acquisition were $41 million and $56 million, respectively, which were primarily included in general and administrative expense",
  "paragraph_id": "0001327567-26-000015:notes:80",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_cyberark_workforce_optimization_severance",
  "what_changed": "New workforce optimization plan for the combined company, with a total estimated cost of $59 million, expected to be substantially complete by the end of fiscal 2027. Cash paid so far is $12 million, and a $12 million severance liability sits in accrued compensation. Charges so far (notes:83) total $41 million, including $17 million share-based. Sales and marketing carries $29 million of it. The accrual is explained as coming from the CyberArk integration.",
  "account": "accrued compensation; operating expenses",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "for a total estimated cost of $59 million. The activities associated with this plan are expected to be substantially completed by the end of fiscal 2027.",
  "paragraph_id": "0001327567-26-000015:notes:81",
  "explanation": true }
```

```json
{ "id": "structure_and_disclosure_changes_koi_acquisition_closed",
  "what_changed": "In the prior period, the subsequent-events note described a definitive agreement for Koi Security at $300 million in cash and replacement awards, expected to close in the second half of fiscal 2026. The note now records Koi as closed on April 14, 2026, with purchase consideration of $231 million, substantially all cash. The allocation (notes:87, notes:89) is goodwill of $169 million and developed technology of $35 million over 5 years. The goodwill is deductible for U.S. income tax (notes:88).",
  "account": "goodwill; identified intangible assets",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The total purchase consideration for the acquisition of Koi was $231 million, substantially all of which is comprised of cash.",
  "paragraph_id": "0001327567-26-000015:notes:85",
  "explanation": false }
```

```json
{ "id": "earnings_quality_koi_replacement_awards_future_expense",
  "what_changed": "New: $61 million of Koi replacement equity awards, all allocated to future service and to be expensed as share-based compensation over the remaining service periods. They include 0.3 million restricted shares that vest over three years.",
  "account": "share-based compensation expense",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "we issued $61 million of replacement equity awards, which was allocated to future services",
  "paragraph_id": "0001327567-26-000015:notes:86",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_portkey_agreement_at_quarter_end",
  "what_changed": "New: on April 30, 2026, the last day of the quarter, the company signed a definitive agreement to buy Portkey, an AI gateway company, for total consideration of $140 million in cash and replacement awards, subject to adjustments.",
  "account": "cash and cash equivalents; goodwill",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "in exchange for total consideration of $140 million in cash and replacement awards, subject to adjustments",
  "paragraph_id": "0001327567-26-000015:notes:91",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_portkey_closed_after_quarter",
  "what_changed": "The subsequent-events note now covers Portkey, which closed on May 29, 2026 and will be accounted for as a business combination in the fourth quarter of fiscal 2026. The CyberArk and Koi subsequent-event paragraphs from the prior period are gone because both deals closed within this quarter.",
  "account": "goodwill; identified intangible assets",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "This acquisition will be accounted for as a business combination in the fourth quarter of fiscal 2026.",
  "paragraph_id": "0001327567-26-000015:notes:189",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_acquired_businesses_revenue_and_operating_loss",
  "what_changed": "New disclosure of what Chronosphere and CyberArk together contributed since their acquisition dates: revenue of $388 million (three months) and $391 million (nine months), and an operating loss of $523 million (three months) and $524 million (nine months). This lets the reported growth and the quarter's operating loss be split between acquired and existing business. I have not done that split.",
  "account": "operating income (loss); total revenue",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "the combined net impact of the Chronosphere and CyberArk acquisitions on our condensed consolidated statements of operations was revenue of $388 million and $391 million and operating loss of $523 million and $524 million",
  "paragraph_id": "0001327567-26-000015:notes:93",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_pro_forma_uses_cyberark_calendar_quarters",
  "what_changed": "The pro forma disclosure now includes CyberArk (notes:94, notes:95). It combines the company's periods ended April 30 with CyberArk's three and nine months ended March 31, 2026 and 2025, so the two sets of periods are not aligned. Adjustments cover amortization, replacement-award compensation, transaction costs, severance and tax.",
  "account": "total revenue (pro forma); net income (loss) (pro forma)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "with the historical results of CyberArk for the three and nine months ended March 31, 2026 and 2025, respectively",
  "paragraph_id": "0001327567-26-000015:notes:96",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_acquisition_allocations_open_in_measurement_period",
  "what_changed": "As carried, the measurement-period paragraph covers the company's acquisitions in the plural, which now include CyberArk and Koi. Their allocations, including income tax and other contingencies, may still change within 12 months of each acquisition date. The prior wording is not in my input. The CyberArk allocation is $21.1 billion.",
  "account": "goodwill; identified intangible assets; deferred tax liabilities",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "may become known during the remainder of the measurement period, not to exceed 12 months from the acquisition date, which may result in changes to the amounts and allocations recorded",
  "paragraph_id": "0001327567-26-000015:notes:97",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_headquarters_land_purchase",
  "what_changed": "As carried, for the nine months: the company bought 14.5 acres next to its Santa Clara headquarters for $91 million, recorded in property and equipment, to allow for future expansion. The prior wording is not in my input, so my files cannot tell me whether the purchase is new this quarter or only the period label moved forward. Read this with the headquarters lease extension (notes:139) and the capital spending line in free cash flow (mdna:56).",
  "account": "property and equipment, net; purchases of property, equipment, and other assets",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "we purchased 14.5 acres of land adjacent to our headquarters in Santa Clara, California, for $91 million to accommodate future expansion of our headquarters",
  "paragraph_id": "0001327567-26-000015:notes:111",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_assumed_zero_coupon_exchangeable_notes",
  "what_changed": "New debt: through a supplemental indenture the company took on CyberArk's $1.25 billion of 0.0% convertible senior notes due June 15, 2030. Each $1,000 of principal is now exchangeable for about 4.3161 company shares plus $88.2630 in cash. That is initially 5.4 million shares at an effective conversion price of about $211.24, plus $110 million in cash. The notes are unsecured and the indenture has no financial covenants.",
  "account": "convertible senior notes (short-term and long-term)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "These modifications result in the 2030 Notes being exchangeable initially for 5.4 million shares of our common stock with an effective initial conversion price of approximately $211.24 per share of common stock",
  "paragraph_id": "0001327567-26-000015:notes:119",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_exchangeable_notes_issuer_redemption_right",
  "what_changed": "New: from June 20, 2028 the company may redeem the 2030 Notes for cash at par plus special interest, if its stock has traded at or above $280.75 on at least 20 of 30 consecutive trading days. Holders whose notes are called may convert at an increased conversion rate.",
  "account": "convertible senior notes",
  "expected_direction": "none",
  "horizon": "beyond 12 months",
  "quote": "on or after June 20, 2028 and on or prior to the 31st scheduled trading day immediately preceding the maturity date",
  "paragraph_id": "0001327567-26-000015:notes:120",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_exchangeable_notes_holder_conversion_triggers",
  "what_changed": "New: before February 15, 2030, holders may convert only if a trigger is met (notes:121 to notes:124). The triggers are: a sale price condition (stock at or above $280.75 on at least 20 of the last 30 trading days of the prior calendar quarter); a trading price condition (note price below 98% of conversion value plus the cash component); or specified corporate events. From February 15, 2030, holders may convert freely, with settlement at maturity (notes:125). The sale price test is rerun every calendar quarter and decides whether the notes are classified as current.",
  "account": "convertible senior notes (current versus long-term classification)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "if the last reported sale price of our common stock is greater than or equal to $280.75 per share of our common stock on each applicable trading day for at least 20 trading days",
  "paragraph_id": "0001327567-26-000015:notes:122",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_exchangeable_notes_principal_payable_in_cash",
  "what_changed": "New: on any conversion, holders receive cash for the principal. Any excess is paid in cash or a mix of cash and shares, at the company's election. Make-whole and fundamental-change provisions can raise the conversion rate or require a cash repurchase at par.",
  "account": "cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "holders of the 2030 Notes will receive cash equal to the aggregate principal amount of the 2030 Notes to be converted",
  "paragraph_id": "0001327567-26-000015:notes:126",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_make_whole_conversions_cash_settled",
  "what_changed": "New: the CyberArk acquisition counted as both a make-whole fundamental change and a fundamental change under the indenture. During the make-whole period, holders could convert at about 5.5690 shares plus $113.8860 in cash per $1,000, and the company chose to settle those conversions in cash. Holders surrendered $153 million of principal. No holder used the repurchase right. Both rights expired on March 20, 2026.",
  "account": "short-term convertible senior notes; cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "certain holders of the 2030 Notes surrendered $153 million in aggregate principal amount of the 2030 Notes",
  "paragraph_id": "0001327567-26-000015:notes:127",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_make_whole_notes_paid_after_quarter",
  "what_changed": "New: the surrendered notes are a current liability at April 30, 2026. Their $160 million fair value was estimated from daily conversion values over the 30 trading days from March 24 to May 5, 2026, a window that runs past the balance sheet date. They were settled in cash for $160 million on May 7, 2026. The MD&A (mdna:132) repeats the settlement and puts the remaining principal at $1.1 billion.",
  "account": "short-term convertible senior notes; cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "were settled in cash for $160 million on May 7, 2026",
  "paragraph_id": "0001327567-26-000015:notes:128",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_remaining_exchangeable_notes_long_term_classification",
  "what_changed": "New: the remaining $1.1 billion of principal is classified as long-term only because the sale price condition was not met in the calendar quarter ended March 31, 2026. Fair value of $1.2 billion is based on the notes' closing trading price and moves mainly with the company's stock price and interest rates. The classification is retested each calendar quarter and can move to current.",
  "account": "long-term convertible senior notes",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "since the sale price condition was not met during the calendar quarter ended March 31, 2026",
  "paragraph_id": "0001327567-26-000015:notes:129",
  "explanation": false }
```

```json
{ "id": "earnings_quality_exchangeable_notes_fair_value_loss",
  "what_changed": "New: for the three and nine months, the change in the 2030 Notes' fair value was a $37 million loss in earnings and a $12 million loss in accumulated other comprehensive income (own credit risk). The other income table (notes:187) has new rows for these changes, and the MD&A (mdna:121) names the loss as a driver of lower other income for the quarter.",
  "account": "other income, net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "changes in fair value of 2030 Notes included in earnings were a loss of $37 million",
  "paragraph_id": "0001327567-26-000015:notes:130",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capped_calls_assumed_and_amended",
  "what_changed": "New: on February 11, 2026 the company amended CyberArk's capped calls, taking over CyberArk's rights and obligations, so that they deliver company shares. The strike is about $211.24 and the caps run from about $287.21 to $291.44. Settlement is in cash or a mix of cash and shares, at the company's election. The capped calls are separate from the notes.",
  "account": "other assets (capped calls)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The capped calls have cap prices ranging from approximately $287.21 to $291.44 per share, subject to certain adjustments.",
  "paragraph_id": "0001327567-26-000015:notes:132",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capped_calls_partly_terminated_for_cash",
  "what_changed": "New: in April 2026 the company terminated the portions of the capped calls tied to the $153 million of surrendered notes and received $10 million in cash.",
  "account": "cash and cash equivalents; other assets",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "In April 2026, we elected to terminate portions of the capped calls in exchange for $10 million in cash",
  "paragraph_id": "0001327567-26-000015:notes:133",
  "explanation": false }
```

```json
{ "id": "earnings_quality_capped_calls_fair_value_carried_in_other_assets",
  "what_changed": "New: the outstanding capped calls are valued at $94 million at April 30, 2026, using a Black-Scholes model with inputs including stock price, volatility, remaining term and the risk-free rate. The change in fair value for the three and nine months was a $1 million loss. The fair value table (notes:37) now has a capped-call row in other assets.",
  "account": "other assets; other income, net",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "As of April 30, 2026, the fair value of the outstanding capped calls was $94 million",
  "paragraph_id": "0001327567-26-000015:notes:134",
  "explanation": false }
```

```json
{ "id": "across_documents_financial_obligation_current_report_body_absent",
  "what_changed": "The credit facility paragraph itself is unchanged according to the note history. The current-report index in my bundle lists a filing dated April 13, 2026 (accession 0001193125-26-151637) with items 1.01 and 2.03, which cover a material agreement and the creation of a direct financial obligation. Its body is not in my bundle. The debt note describes only the April 13, 2023 Credit Agreement, maturing April 13, 2028 with nothing drawn. The lease note (notes:139) describes three headquarters lease amendments signed in April 2026. My files cannot tell me which agreement the April 13, 2026 filing reports, or whether the quarterly report describes it in full.",
  "account": "debt; operating lease liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "On April 13, 2023, we entered into a credit agreement",
  "paragraph_id": "0001327567-26-000015:notes:136",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_headquarters_lease_extension",
  "what_changed": "New: in April 2026 the company signed three amendments extending its Santa Clara headquarters leases by twelve years, to July 2040, with renewal options through July 2052. Lease payments net of incentives are about $469 million over the extended term. The amendments added $262 million of right-of-use assets against new operating lease liabilities. The MD&A (mdna:139) now runs lease terms through fiscal 2040 and states operating lease obligations of $778 million.",
  "account": "operating lease right-of-use assets; operating lease liabilities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "In April 2026, we entered into three lease amendments to extend the lease terms of our current corporate headquarters in Santa Clara, California for a period of twelve years through July 2040.",
  "paragraph_id": "0001327567-26-000015:notes:139",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_centripetal_accrual_with_interest",
  "what_changed": "The Centripetal accrual is now stated as $150 million at April 30, 2026. The prior quarter's text stated $149 million at January 31, 2026, and both cite $146 million at July 31, 2025. The interest charge is $1 million for the three months and $4 million for the nine months. Prior-year comparatives are a $2 million charge and a $40 million release. The stated basis is unchanged (the judgment plus estimated interest), the appeal is still pending and the bond is still posted (notes:149, unchanged). The amounts sit in other long-term liabilities and general and administrative expense. The MD&A (mdna:112) cites the prior-year $40 million release as a reason nine-month general and administrative expense is higher.",
  "account": "other long-term liabilities (litigation accrual); general and administrative expense",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "we accrued $150 million and $146 million based on the judgment and estimated interest",
  "paragraph_id": "0001327567-26-000015:notes:150",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_authorization_raised_and_extended",
  "what_changed": "New: on March 10, 2026 the board added $1.0 billion to the repurchase program, bringing total authorization to $5.1 billion. The expiration date was extended to December 31, 2026. The MD&A (mdna:136) repeats this.",
  "account": "common stock and additional paid-in capital; cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "On March 10, 2026, our board of directors authorized an additional $1.0 billion increase to our share repurchase program",
  "paragraph_id": "0001327567-26-000015:notes:156",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_executed_in_quarter",
  "what_changed": "New: during the three months the company repurchased and retired 7 million shares for $1.0 billion, at an average of $147.70 per share. There were no repurchases in the prior-year periods. $1.0 billion of authorization remains. The MD&A (mdna:156) names repurchases as a driver of financing outflows.",
  "account": "weighted-average shares outstanding; cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "we repurchased and retired 7 million shares of our common stock under our current repurchase authorization for an aggregate purchase price of $1.0 billion",
  "paragraph_id": "0001327567-26-000015:notes:157",
  "explanation": false }
```

```json
{ "id": "earnings_quality_accelerated_vesting_from_cyberark_and_koi",
  "what_changed": "New: vesting of certain equity awards was accelerated in connection with the CyberArk and Koi acquisitions, producing $177 million of share-based compensation: $140 million in general and administrative, $36 million in sales and marketing and $1 million in cost of subscription and support revenue. These are acquisition-related, not recurring, charges.",
  "account": "share-based compensation; general and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "the vesting of certain equity awards was accelerated in connection with our acquisitions of CyberArk and Koi",
  "paragraph_id": "0001327567-26-000015:notes:176",
  "explanation": false }
```

```json
{ "id": "earnings_quality_effective_tax_rate_attributed_to_cyberark",
  "what_changed": "The tax note (notes:178, notes:179) now names the CyberArk acquisition, together with lower excess tax benefits from share-based compensation, as the reason the effective tax rate differs. The rate was negative 13.5% for the three months and 26.8% for the nine months. The MD&A (mdna:125) says the same.",
  "account": "provision for income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Our effective tax rates for the three and nine months ended April 30, 2026 were impacted by our CyberArk acquisition",
  "paragraph_id": "0001327567-26-000015:notes:179",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_exchangeable_notes_excluded_from_diluted_shares",
  "what_changed": "New sentence: the 2030 Notes and the capped calls were left out of diluted net income (loss) per share because including them would have been antidilutive. The earnings per share captions now read net income (loss), reflecting the quarter's loss.",
  "account": "diluted weighted-average shares",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Our 2030 Notes and capped calls were also excluded from the calculation of diluted net income (loss) per share as the effect would have been antidilutive.",
  "paragraph_id": "0001327567-26-000015:notes:185",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_unit_forty_two_frontier_ai_defense_launch",
  "what_changed": "As carried, the Unit 42 paragraph adds that in April 2026 the company launched a suite of Unit 42 Frontier AI Defense services to find and neutralize threats from next-generation AI models.",
  "account": "subscription and support revenue (professional services)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "In April 2026, we launched a new suite of Unit 42 Frontier AI Defense services",
  "paragraph_id": "0001327567-26-000015:mdna:36",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_total_revenue_growth_attributed_to_acquisitions",
  "what_changed": "As carried, the overview gives third-quarter revenue of $3.0 billion against $2.3 billion and growth of 31%. It now names the company's recent acquisitions alongside portfolio adoption as a cause of that growth. Notes:93 gives the acquired revenue, so the growth can be split. I have not split it.",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Our growth reflects the increased adoption of our portfolio, which consists of product, subscriptions, and support, and our recent acquisitions.",
  "paragraph_id": "0001327567-26-000015:mdna:37",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_identity_licenses_recognized_on_delivery",
  "what_changed": "As carried, the product revenue description now includes certain identity security offerings among software licenses. Product revenue is recognized when hardware ships or the software license is delivered. The paragraph says software-license revenue will vary from quarter to quarter and grow over time as the company renews its software license contracts. Mdna:39 states that product revenue now includes CyberArk's on-premise identity licenses. So the acquired on-premise license revenue is recognized in full on delivery rather than over time, and product revenue will move with when renewals happen.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "and certain identity security offerings",
  "paragraph_id": "0001327567-26-000015:mdna:70",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_product_revenue_growth_from_cyberark_licenses",
  "what_changed": "As carried, the product revenue increase for both periods is put down to software licenses and demand for the new generation of hardware. It is also put down to software license revenue from CyberArk, which closed in February 2026. Mdna:39 gives third-quarter product revenue of $594 million, 31% growth.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was also driven by increased software licenses revenue from our CyberArk acquisition closed in February 2026",
  "paragraph_id": "0001327567-26-000015:mdna:72",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_subscription_and_support_growth_from_acquisitions",
  "what_changed": "As carried, the subscription and support increase is put down to customer demand and to recent acquisitions. Mdna:40 says subscriptions now include the CyberArk identity platform and the Chronosphere observability platform, and gives third-quarter subscription and support revenue of $2.4 billion, 31% growth.",
  "account": "subscription and support revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "offerings from our end-customers and our recent acquisitions",
  "paragraph_id": "0001327567-26-000015:mdna:77",
  "explanation": false }
```

```json
{ "id": "across_documents_geographic_growth_explained_without_acquisitions",
  "what_changed": "As carried, the geographic explanation puts growth in every region down to continued investment in the global sales force, with the Americas contributing most because of its scale. It does not mention acquisitions. Elsewhere, mdna:37, mdna:72, mdna:77 and notes:93 credit part of the growth to acquisitions. The reasons given in the MD&A for revenue growth are therefore not the same from one paragraph to the next.",
  "account": "revenue by geography",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "with the Americas contributing the highest increase in revenue due to its larger scale",
  "paragraph_id": "0001327567-26-000015:mdna:80",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_and_component_shortages",
  "what_changed": "As carried, the economic-conditions paragraph lists supply chain disruptions, including increased memory, storage or other component shortages, along with tariffs, trade policy and changes in regulators' enforcement and administration as conditions that may hurt results. The prior wording is not in my input. Read this with mdna:86 (higher tariff costs) and mdna:95 (lower hardware gross margin).",
  "account": "cost of product revenue; inventory",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "supply chain disruptions, including increased memory, storage or other component shortages",
  "paragraph_id": "0001327567-26-000015:mdna:44",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_israel_and_iran_hostilities",
  "what_changed": "As carried, the regional-risk paragraph names hostilities in Israel, Iran and the surrounding region. It says the company intends to keep growing its presence in Israel and does not currently expect significant disruption. The prior wording is not in my input. Read this with the Israeli research and development tax law paragraph (mdna:126).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The hostilities in Israel, Iran and the surrounding region have continued to result in economic and political uncertainty.",
  "paragraph_id": "0001327567-26-000015:mdna:45",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_acquisition_impact_disclosure_discretion",
  "what_changed": "New section on the impact of acquisitions (mdna:64, mdna:65, mdna:66). It says the CyberArk deal and other recent acquisitions affect comparability with 2025. It also says management may disclose an acquisition's effect on revenue, costs and expenses, qualitatively or quantitatively, for one year after the acquisition, where it judges that meaningful. How much is disclosed about the acquired businesses is therefore left to management.",
  "account": "total revenue; operating expenses",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "we may qualitatively or quantitatively disclose the impact of our acquisitions on revenue, costs, and expenses for the one year period subsequent to the acquisition date",
  "paragraph_id": "0001327567-26-000015:mdna:66",
  "explanation": false }
```

```json
{ "id": "earnings_quality_cyberark_amortization_in_cost_of_product_revenue",
  "what_changed": "As carried, the higher cost of product revenue is put down first to amortization of intangibles from CyberArk. Mdna:84 now lists amortization of intangible assets among the components of product cost, and the amortization table (notes:107) has a new cost of product revenue row. Cost of product revenue now carries a non-cash acquisition charge.",
  "account": "cost of product revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "primarily due to higher amortization of intangible assets as a result of our CyberArk acquisition",
  "paragraph_id": "0001327567-26-000015:mdna:86",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_lower_inventory_excess_and_obsolete_charges",
  "what_changed": "As carried, management cites a decrease in inventory excess and obsolete charges as partly offsetting higher cost of product revenue in both periods. Mdna:95 cites it again for nine-month product gross margin. No reason is given for the lower charges. This is management's statement about the inventory reserve charge.",
  "account": "inventory excess and obsolete reserve; cost of product revenue",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "partially offset by a decrease in inventory excess and obsolete charges",
  "paragraph_id": "0001327567-26-000015:mdna:86",
  "explanation": true }
```

```json
{ "id": "narrative_signs_of_operating_pressure_higher_tariff_costs",
  "what_changed": "As carried, higher tariff costs, alongside demand for hardware, are named as drivers of higher cost of product revenue. Mdna:84 now lists shipping and tariff costs among the components of product cost.",
  "account": "cost of product revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "increased demand for our hardware products and higher tariff costs",
  "paragraph_id": "0001327567-26-000015:mdna:86",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_cost_of_subscription_and_support_drivers",
  "what_changed": "As carried, the drivers of cost of subscription and support revenue are given in dollars. Cloud hosting rose $75 million (three months) and $171 million (nine months). Amortization of intangibles rose $117 million and $109 million because of recent acquisitions. Personnel costs rose $71 million and $97 million, including headcount from acquisitions. Read this with the cloud purchase commitments in the commitments note (notes:142).",
  "account": "cost of subscription and support revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Amortization of intangible assets increased $117 million and $109 million for the three and nine months ended April 30, 2026",
  "paragraph_id": "0001327567-26-000015:mdna:91",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_hardware_gross_margin_decrease",
  "what_changed": "As carried, product gross margin fell in both periods, mainly because of lower gross margin on hardware and higher amortization. CyberArk license revenue partly offset this. For the nine months, the shift toward software and lower inventory excess and obsolete charges also offset it.",
  "account": "product gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "primarily due to a decrease in gross margin on our hardware products and higher amortization of intangible assets",
  "paragraph_id": "0001327567-26-000015:mdna:95",
  "explanation": false }
```

```json
{ "id": "earnings_quality_subscription_and_support_margin_decrease_from_amortization",
  "what_changed": "As carried, the fall in subscription and support gross margin in both periods is put down mainly to amortization of intangibles from recent acquisitions. That is a non-cash acquisition charge, not a change in service delivery costs.",
  "account": "subscription and support gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "primarily due to higher amortization of intangible assets as a result of our recent acquisitions",
  "paragraph_id": "0001327567-26-000015:mdna:96",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_research_and_development_personnel_growth",
  "what_changed": "As carried, research and development rose because personnel costs grew $192 million (three months) and $233 million (nine months), largely from headcount, including headcount from recent acquisitions.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "which grew $192 million and $233 million for the three and nine months ended April 30, 2026",
  "paragraph_id": "0001327567-26-000015:mdna:103",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_sales_and_marketing_personnel_and_amortization",
  "what_changed": "As carried, sales and marketing rose because personnel costs grew $254 million (three months) and $408 million (nine months), including acquired headcount, and because of higher amortization of intangibles from recent acquisitions. Mdna:105 now lists amortization of intangibles among sales and marketing costs. The CyberArk severance table (notes:83) places $29 million of severance in sales and marketing.",
  "account": "sales and marketing expense",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "further driven by higher amortization of intangible assets as a result of our recent acquisitions",
  "paragraph_id": "0001327567-26-000015:mdna:107",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_general_and_administrative_scope_and_outlook",
  "what_changed": "As carried, the general and administrative description now says the line includes changes in the fair value of the contingent consideration liability. The outlook that the line will grow over time now opens with 'excluding the near-term impact of our recent acquisitions'. The prior wording is not in my input. Gains or losses on the IBM liability therefore land inside an operating expense line.",
  "account": "general and administrative expense",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "General and administrative expense also includes change in fair value of contingent consideration liability.",
  "paragraph_id": "0001327567-26-000015:mdna:110",
  "explanation": false }
```

```json
{ "id": "earnings_quality_general_and_administrative_acquisition_vesting_and_severance",
  "what_changed": "As carried, general and administrative personnel costs grew $195 million (three months) and $237 million (nine months). The causes given are accelerated vesting tied to recent acquisitions, CyberArk severance and headcount growth, plus higher acquisition-related costs. The nine-month comparison is also affected by the prior year's $40 million release of a litigation accrual.",
  "account": "general and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to the accelerated vesting of certain equity awards in connection with our recent acquisitions, employee severance charges in connection with our CyberArk acquisition",
  "paragraph_id": "0001327567-26-000015:mdna:112",
  "explanation": false }
```

```json
{ "id": "earnings_quality_contingent_consideration_gain_inside_general_and_administrative",
  "what_changed": "New in the prose: a $110 million gain from the change in fair value of the contingent consideration liability partly offset higher general and administrative expense in the three months. The gain comes from the reduced IBM payment estimate (notes:40) and sits inside operating expenses in a quarter that shows an operating loss.",
  "account": "general and administrative expense; operating income (loss)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "partially offset by a gain of $110 million for the change in fair value of contingent consideration liability during the three months ended April 30, 2026",
  "paragraph_id": "0001327567-26-000015:mdna:112",
  "explanation": false }
```

```json
{ "id": "earnings_quality_investment_sale_gains_to_fund_acquisitions",
  "what_changed": "As carried, nine-month other income, net is said to have risen mainly because of larger gains on investments sold to fund acquisitions, together with higher interest income, partly offset by the loss on the convertible notes. The prose ties the gains to acquisition funding and does not present them as recurring. The other income table (notes:187) carries them in other, net.",
  "account": "other income, net",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "primarily due to increased gains on sales of our investments to fund acquisitions",
  "paragraph_id": "0001327567-26-000015:mdna:121",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_lower_interest_income_from_lower_balances",
  "what_changed": "As carried, third-quarter other income, net fell because of the loss on the convertible notes and because interest income was lower on lower average cash, cash equivalent and investment balances. This follows the cash paid for CyberArk, Koi and the share repurchases.",
  "account": "interest income (other income, net)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "lower interest income as a result of lower average cash, cash equivalent and investment balances",
  "paragraph_id": "0001327567-26-000015:mdna:121",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_tax_rate_fluctuation_from_cyberark_integration",
  "what_changed": "As carried, the tax discussion names CyberArk as a driver of the effective tax rate and warns that the rate may keep fluctuating as CyberArk is brought further into the corporate structure and intercompany relationships. The California valuation allowance remains.",
  "account": "provision for income taxes",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We may continue to see fluctuations in our effective tax rate as we further integrate CyberArk into our corporate structure and intercompany relationships.",
  "paragraph_id": "0001327567-26-000015:mdna:123",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_israel_research_and_development_tax_credit",
  "what_changed": "New: in March 2026 the Knesset Finance Committee approved an Israeli law giving a tax credit for qualifying research and development spending in Israel after January 1, 2026. Unused credit is to be paid in cash after a set period. Implementing regulations are still to come, and the effect this period was not material.",
  "account": "provision for income taxes; research and development expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "all or a portion of the unutilized R&D tax credit will be paid in cash upon the lapse of a period stipulated by the R&D Law",
  "paragraph_id": "0001327567-26-000015:mdna:126",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_foreign_earnings_repatriated_for_cyberark",
  "what_changed": "New: as part of the CyberArk acquisition, the company used an intercompany transaction to repatriate $3.5 billion of foreign earnings. The income tax cost, for state and other taxes, was immaterial. The remaining unremitted earnings are still indefinitely reinvested. Total cash, cash equivalents and investments are stated at $7.0 billion.",
  "account": "cash and cash equivalents; provision for income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "we executed an intercompany transaction to repatriate $3.5 billion of foreign earnings, resulting in immaterial income tax expense related to state and other taxes",
  "paragraph_id": "0001327567-26-000015:mdna:130",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_exchangeable_notes_cash_settlement_and_sufficiency",
  "what_changed": "New liquidity paragraph. Because the sale price condition was not met in the calendar quarter ended March 31, 2026, the 2030 Notes cannot be converted under that condition in the calendar quarter ending June 30, 2026. If the condition is met in that quarter and all holders convert in the calendar quarter ending September 30, 2026, the company would owe the $1.1 billion principal, and part of any excess, in cash. Management says its operating cash, cash and investments, financing access and any proceeds from the capped calls would be enough.",
  "account": "cash and cash equivalents; convertible senior notes",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "we would be obligated to settle the $1.1 billion principal amount of the 2030 Notes",
  "paragraph_id": "0001327567-26-000015:mdna:133",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_attributed_to_collections",
  "what_changed": "As carried, nine-month operating cash flow of $3.2 billion is stated as up $501 million. Management puts this down to business growth seen in higher collections, partly offset by higher cash spending. This is management's statement about receivable collections. The prior wording is not in my input.",
  "account": "net cash provided by operating activities; accounts receivable collections",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "as reflected by increases in collections during the nine months ended April 30, 2026, partially offset by higher cash expenditure to support our business growth",
  "paragraph_id": "0001327567-26-000015:mdna:149",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_investing_outflow_from_acquisitions_and_investment_sales",
  "what_changed": "As carried, nine-month investing outflow of $2.1 billion is stated as up $656 million. The cause given is higher net cash paid for acquisitions, partly offset by more proceeds from sales and maturities of investments and fewer purchases. Read this with mdna:121, where investments were sold at a gain to fund acquisitions. The prior wording is not in my input.",
  "account": "investments; net cash used in investing activities",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "primarily due to an increase in net cash payments for business acquisitions during the nine months ended April 30, 2026, partially offset by higher proceeds from sales and maturities of investments and lower purchases of investments",
  "paragraph_id": "0001327567-26-000015:mdna:153",
  "explanation": false }
```

```json
{ "id": "earnings_quality_contingent_consideration_payments_in_financing_activities",
  "what_changed": "As carried, nine-month financing outflow of $1.0 billion is stated as up $600 million. The causes given are share repurchases and payments of the contingent consideration liability, partly offset by the absence of 2025 Notes repayments. Mdna:155 now lists contingent consideration payments among financing activities. Because the IBM payments are financing cash flows, they are not in operating cash flow or in the non-GAAP free cash flow measure (mdna:56).",
  "account": "net cash used in financing activities; free cash flow (non-GAAP)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "primarily due to repurchase of our common stock and payments of our contingent consideration liability during the nine months ended April 30, 2026",
  "paragraph_id": "0001327567-26-000015:mdna:156",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_no_control_change_reported_in_acquisition_quarter",
  "what_changed": "No new statement. Item 4 says no change in internal control over financial reporting during the quarter ended April 30, 2026 materially affected it. That is the quarter in which CyberArk ($21.1 billion of consideration, notes:74) and Koi were acquired and consolidated. The section says nothing about bringing CyberArk's processes into the company's controls or setting them aside. The prior quarter's Item 4 is not in my input, and no auditor's report is in my input.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "that occurred during the fiscal quarter ended April 30, 2026 that have materially affected, or are reasonably likely to materially affect, our internal control over financial reporting",
  "paragraph_id": "0001327567-26-000015:item_4_controls:5",
  "explanation": false }
```

## Paragraphs that come as text but are not items

### Notes

- 0001327567-26-000015:notes:2: wording; "and identities" added to the business description because of CyberArk; the substance is in the item on CyberArk being consolidated
- 0001327567-26-000015:notes:10: lead-in saying the policies changed for CyberArk; the substance is in the items on notes:13 and notes:14
- 0001327567-26-000015:notes:11: heading
- 0001327567-26-000015:notes:12: introduces the acquired notes and capped calls; the substance is in the items on notes:119 and notes:132
- 0001327567-26-000015:notes:15: heading; unchanged per the note history
- 0001327567-26-000015:notes:19: wording only ("could be applied" became "can be applied")
- 0001327567-26-000015:notes:28: amounts only (revenue by geography table)
- 0001327567-26-000015:notes:30: amounts only (revenue by type table)
- 0001327567-26-000015:notes:32: amounts only; period rolled forward (revenue recognized from opening deferred revenue)
- 0001327567-26-000015:notes:34: amounts only; date rolled forward (remaining performance obligations)
- 0001327567-26-000015:notes:35: heading and lead-in; date rolled forward
- 0001327567-26-000015:notes:36: amounts only (fair value table, cash equivalents and short-term investments)
- 0001327567-26-000015:notes:37: amounts only; the new convertible note and capped call rows are covered by the items on notes:129, notes:130 and notes:134
- 0001327567-26-000015:notes:42: amounts only (contingent consideration rollforward); covered by the items on notes:40
- 0001327567-26-000015:notes:43: date rolled forward
- 0001327567-26-000015:notes:44: heading
- 0001327567-26-000015:notes:45: date rolled forward
- 0001327567-26-000015:notes:46: amounts only (available-for-sale table at April 30, 2026)
- 0001327567-26-000015:notes:47: amounts only; unchanged per the note history (July 31, 2025 table)
- 0001327567-26-000015:notes:48: period rolled forward
- 0001327567-26-000015:notes:49: date rolled forward
- 0001327567-26-000015:notes:50: amounts only (maturity table)
- 0001327567-26-000015:notes:51: heading
- 0001327567-26-000015:notes:52: amounts and dates only (money market funds)
- 0001327567-26-000015:notes:53: heading and lead-in; date rolled forward
- 0001327567-26-000015:notes:54: amounts only (financing receivables table)
- 0001327567-26-000015:notes:56: amounts only (financing receivables by risk rating and origination year)
- 0001327567-26-000015:notes:58: period rolled forward; still says no significant allowance activity and immaterial past-due amounts
- 0001327567-26-000015:notes:59: amounts only; period rolled forward (financing receivables sold)
- 0001327567-26-000015:notes:61: amounts and dates only (cash flow hedge notional)
- 0001327567-26-000015:notes:62: amounts and dates only (hedge gains in other comprehensive income)
- 0001327567-26-000015:notes:63: amounts and dates only (non-designated notional)
- 0001327567-26-000015:notes:70: insufficient; comes as text, but the prior wording of the business combination note is not in my input and no new fact shows (Chronosphere goodwill, not tax-deductible)
- 0001327567-26-000015:notes:75: amounts only; covered by the item on notes:74
- 0001327567-26-000015:notes:82: lead-in; covered by the item on notes:81
- 0001327567-26-000015:notes:83: amounts only; covered by the item on notes:81
- 0001327567-26-000015:notes:84: heading
- 0001327567-26-000015:notes:87: amounts only; covered by the item on notes:85
- 0001327567-26-000015:notes:88: Koi goodwill deductible; covered by the item on notes:85
- 0001327567-26-000015:notes:89: amounts only; covered by the item on notes:85
- 0001327567-26-000015:notes:90: heading
- 0001327567-26-000015:notes:94: lead-in; covered by the item on notes:96
- 0001327567-26-000015:notes:95: amounts only (pro forma table); covered by the item on notes:96
- 0001327567-26-000015:notes:98: repeats the Chronosphere consideration sentence under a separate tag; no new fact
- 0001327567-26-000015:notes:99: repeats the CyberArk consideration sentence of notes:74 under a separate tag
- 0001327567-26-000015:notes:101: lead-in; period rolled forward
- 0001327567-26-000015:notes:102: amounts only (goodwill rollforward)
- 0001327567-26-000015:notes:104: lead-in; date rolled forward
- 0001327567-26-000015:notes:105: amounts only; the new intangible rows are covered by the item on notes:79
- 0001327567-26-000015:notes:106: lead-in
- 0001327567-26-000015:notes:107: amounts only; the new cost of product revenue row is covered by the item on cost of product revenue amortization (mdna:86)
- 0001327567-26-000015:notes:108: lead-in
- 0001327567-26-000015:notes:109: amounts only (future amortization)
- 0001327567-26-000015:notes:112: heading
- 0001327567-26-000015:notes:113: unchanged per the note history
- 0001327567-26-000015:notes:114: wording only (tense)
- 0001327567-26-000015:notes:115: wording only (tense; the warrants are fully settled)
- 0001327567-26-000015:notes:116: period rolled forward; the earlier quarter's breakdown is dropped; no new fact
- 0001327567-26-000015:notes:117: heading
- 0001327567-26-000015:notes:118: heading
- 0001327567-26-000015:notes:121: lead-in to the conversion triggers; covered by the item on notes:122
- 0001327567-26-000015:notes:123: trading price trigger; covered by the item on notes:122
- 0001327567-26-000015:notes:124: corporate event trigger; covered by the item on notes:122
- 0001327567-26-000015:notes:125: conversion after February 15, 2030; covered by the item on notes:122
- 0001327567-26-000015:notes:131: heading
- 0001327567-26-000015:notes:135: heading
- 0001327567-26-000015:notes:137: unchanged per the note history (credit facility pricing)
- 0001327567-26-000015:notes:138: date rolled forward
- 0001327567-26-000015:notes:140: heading
- 0001327567-26-000015:notes:141: date rolled forward (per the note history)
- 0001327567-26-000015:notes:142: amounts only (purchase commitments table)
- 0001327567-26-000015:notes:143: unchanged per the note history
- 0001327567-26-000015:notes:144: heading
- 0001327567-26-000015:notes:145: unchanged per the note history
- 0001327567-26-000015:notes:146: unchanged per the note history
- 0001327567-26-000015:notes:147: unchanged per the note history
- 0001327567-26-000015:notes:148: heading
- 0001327567-26-000015:notes:149: unchanged per the note history (Centripetal background)
- 0001327567-26-000015:notes:151: heading
- 0001327567-26-000015:notes:152: unchanged per the note history (Finjan)
- 0001327567-26-000015:notes:153: heading
- 0001327567-26-000015:notes:154: unchanged per the note history (Eire OG, resolved December 2025)
- 0001327567-26-000015:notes:159: lead-in; period rolled forward
- 0001327567-26-000015:notes:160: amounts only (restricted and performance stock unit activity)
- 0001327567-26-000015:notes:162: assumed units across three acquisitions; covered by the items on notes:76 and notes:86
- 0001327567-26-000015:notes:166: insufficient; comes as text, but the prior wording of the compensation note is not in my input. It reads like the performance-unit grant description with the period rolled forward. It ties performance conditions to next-generation security annualized recurring revenue and non-GAAP earnings per diluted share, "subject to certain adjustments"
- 0001327567-26-000015:notes:167: lead-in; period rolled forward
- 0001327567-26-000015:notes:168: amounts only (Monte Carlo assumptions)
- 0001327567-26-000015:notes:170: period rolled forward (performance stock options fully vested)
- 0001327567-26-000015:notes:171: lead-in
- 0001327567-26-000015:notes:172: amounts only (performance stock option activity)
- 0001327567-26-000015:notes:175: amounts only (share-based compensation by line)
- 0001327567-26-000015:notes:177: amounts only (unrecognized compensation and weighted-average period)
- 0001327567-26-000015:notes:178: covered by the item on notes:179
- 0001327567-26-000015:notes:180: wording; "(loss)" added to the captions; the loss itself is in the tables
- 0001327567-26-000015:notes:181: lead-in; wording
- 0001327567-26-000015:notes:182: amounts only (earnings per share computation)
- 0001327567-26-000015:notes:183: lead-in; wording
- 0001327567-26-000015:notes:184: amounts only (antidilutive securities)
- 0001327567-26-000015:notes:187: amounts only; the new fair value rows are covered by the items on notes:130 and notes:134 and by the item on investment sale gains (mdna:121)
- 0001327567-26-000015:notes:188: heading (now Portkey)

### MD&A

- 0001327567-26-000015:mdna:5: period rolled forward
- 0001327567-26-000015:mdna:11: wording; identities added to the mission statement; covered by the CyberArk items
- 0001327567-26-000015:mdna:14: insufficient; product description (Prisma Browser) with no account bearing; the prior wording is not in my input
- 0001327567-26-000015:mdna:17: insufficient; product description (Prisma AIRS) with no account bearing; the prior wording is not in my input
- 0001327567-26-000015:mdna:21: product description adding Koi; covered by the item on notes:85
- 0001327567-26-000015:mdna:28: heading (identity security)
- 0001327567-26-000015:mdna:29: description of the acquired identity platform; covered by the CyberArk items
- 0001327567-26-000015:mdna:30: product description; covered by the CyberArk items
- 0001327567-26-000015:mdna:31: product description; covered by the CyberArk items
- 0001327567-26-000015:mdna:32: product description; covered by the CyberArk items
- 0001327567-26-000015:mdna:33: product description; covered by the CyberArk items
- 0001327567-26-000015:mdna:34: product description; covered by the CyberArk items
- 0001327567-26-000015:mdna:39: product revenue now includes on-premise identity licenses; covered by the items on mdna:70 and mdna:72
- 0001327567-26-000015:mdna:40: subscriptions now include the identity and observability platforms; covered by the item on mdna:77
- 0001327567-26-000015:mdna:41: product launches and recap of the CyberArk, Koi and Portkey deals; covered by the acquisition items
- 0001327567-26-000015:mdna:49: wording ("operating income (loss)")
- 0001327567-26-000015:mdna:50: amounts only (key metrics)
- 0001327567-26-000015:mdna:51: amounts only (key metrics table)
- 0001327567-26-000015:mdna:56: amounts only (free cash flow table)
- 0001327567-26-000015:mdna:60: amounts only (results of operations table)
- 0001327567-26-000015:mdna:62: amounts only (share-based compensation table)
- 0001327567-26-000015:mdna:64: heading (impact of acquisitions)
- 0001327567-26-000015:mdna:65: restates the CyberArk consideration and replacement awards; covered by the items on notes:74 and notes:76
- 0001327567-26-000015:mdna:68: adds business acquisitions to the causes of quarter-to-quarter revenue variation; covered by the item on mdna:66
- 0001327567-26-000015:mdna:71: amounts only
- 0001327567-26-000015:mdna:75: amounts only
- 0001327567-26-000015:mdna:79: amounts only
- 0001327567-26-000015:mdna:84: component list now includes amortization and tariffs; covered by the items on mdna:86
- 0001327567-26-000015:mdna:85: amounts only
- 0001327567-26-000015:mdna:89: component list for subscription cost; covered by the items on mdna:91 and mdna:96
- 0001327567-26-000015:mdna:90: amounts only
- 0001327567-26-000015:mdna:94: amounts only (gross margin table)
- 0001327567-26-000015:mdna:97: page number
- 0001327567-26-000015:mdna:99: amounts only (unrecognized share-based compensation); same as notes:177
- 0001327567-26-000015:mdna:102: amounts only
- 0001327567-26-000015:mdna:105: component list now includes amortization; covered by the item on mdna:107
- 0001327567-26-000015:mdna:106: amounts only
- 0001327567-26-000015:mdna:108: page number
- 0001327567-26-000015:mdna:111: amounts only
- 0001327567-26-000015:mdna:114: wording; no new fact (interest expense source)
- 0001327567-26-000015:mdna:115: amounts only
- 0001327567-26-000015:mdna:116: period rolled forward
- 0001327567-26-000015:mdna:117: page number
- 0001327567-26-000015:mdna:119: other income now includes fair value changes on notes and capped calls; covered by the items on notes:13 and notes:14
- 0001327567-26-000015:mdna:120: amounts only
- 0001327567-26-000015:mdna:124: amounts only (tax table)
- 0001327567-26-000015:mdna:125: covered by the item on notes:179
- 0001327567-26-000015:mdna:127: page number
- 0001327567-26-000015:mdna:129: amounts only (working capital and cash table)
- 0001327567-26-000015:mdna:132: restates the 2030 Notes terms and the make-whole settlement; covered by the items on notes:119, notes:127 and notes:128
- 0001327567-26-000015:mdna:134: date rolled forward (credit facility)
- 0001327567-26-000015:mdna:136: restates the repurchase authorization; covered by the item on notes:156
- 0001327567-26-000015:mdna:137: page number
- 0001327567-26-000015:mdna:139: lease term and obligation amount; covered by the item on notes:139
- 0001327567-26-000015:mdna:140: amounts only (purchase commitments total)
- 0001327567-26-000015:mdna:141: amounts only (contingent consideration balance); covered by the items on notes:40
- 0001327567-26-000015:mdna:143: lead-in; period rolled forward
- 0001327567-26-000015:mdna:144: amounts only (cash flow table)
- 0001327567-26-000015:mdna:150: page number
- 0001327567-26-000015:mdna:155: financing activities now list contingent consideration payments; covered by the item on mdna:156
- 0001327567-26-000015:mdna:161: wording; cross-reference only
- 0001327567-26-000015:mdna:162: page number

### Item 4

- 0001327567-26-000015:item_4_controls:1: heading
- 0001327567-26-000015:item_4_controls:2: heading
- 0001327567-26-000015:item_4_controls:3: insufficient; the prior quarter's Item 4 is not in my input. The evaluation cites Rule 13a-15(f), the rule that defines internal control over financial reporting, for its evaluation of disclosure controls. I cannot tell whether earlier periods cite the same rule
- 0001327567-26-000015:item_4_controls:4: heading
- 0001327567-26-000015:item_4_controls:6: heading
- 0001327567-26-000015:item_4_controls:7: standard limitations language; no new fact visible
- 0001327567-26-000015:item_4_controls:8: page number

### Current reports

- The current-report file has no paragraph ids and no item bodies, only an index of item codes. I raised the one filing that matters to the notes (April 13, 2026, items 1.01 and 2.03) in the item on notes:136. The earnings release filed June 2, 2026 has no body here, so I could not compare the release with the quarterly report.
