<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# PANW notes-text reader report: 0001327567-26-000015 (10-Q, quarter ended April 30, 2026; prior period 0001327567-26-000005)

## Inputs read

- Read in full: input_notes.md (notes:1 to notes:189), input_mdna.md (mdna:1 to mdna:162), input_controls.md (item_4_controls:1 to :8), input_notes_history.md (note_history:1 to :60), input_8k.md and input_prior_predictions.md.
- Not in my directory:
  - an auditor's report (this is a 10-Q, and no review report text was supplied);
  - an Item 1A diff;
  - an Exhibit 21 diff;
  - any Exhibit 10.
- input_8k.md contains only item codes, with no 8-K body. Its header says no 8-K at or before 2026-06-03 is on record, but it then lists filings up to 2026-06-02. I read that as "no body is on record".
- Prior predictions: none on record.
- Nothing forbidden (no trend table, prices, returns, short interest, other company files, prior probabilities or outcome window) is in the directory.
- No arithmetic was done. Where an item cites amounts, they are the amounts the prose states.

Items: 72, of which 4 are `insufficient`.

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_identities_added_to_business_description",
    "what_changed": "The business description now lists identities among what the platforms secure. The prior text (note_history:4) listed only users, networks, clouds and endpoints. The change reflects the CyberArk acquisition.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "secure their users, networks, clouds, endpoints, and identities by delivering comprehensive cybersecurity",
    "paragraph_id": "0001327567-26-000015:notes:2",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_cyberark_results_included_prospectively",
    "what_changed": "New paragraph: CyberArk was acquired on February 11, 2026, and its results are consolidated from that date forward. The prior filing carried CyberArk only as a subsequent event (note_history:58, removed).",
    "account": "revenue; operating expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The condensed consolidated financial statements include the financial results of CyberArk prospectively from the date of acquisition.",
    "paragraph_id": "0001327567-26-000015:notes:3",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_convertible_notes_and_capped_calls_added_to_estimates_list",
    "what_changed": "The list of management estimates adds the fair value of convertible senior notes and capped calls. The prior list (note_history:15, removed) did not include it.",
    "account": "convertible senior notes; other assets (capped calls)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "fair value of convertible senior notes and capped calls, the assessment of recoverability of our intangibles and goodwill",
    "paragraph_id": "0001327567-26-000015:notes:8",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_fair_value_option_elected_for_assumed_convertible_notes",
    "what_changed": "New policy: the company elected the fair value option for the convertible notes acquired from CyberArk. The notes are remeasured every period instead of bifurcating the embedded features. Changes in earnings go to other income, net, and changes from instrument-specific credit risk go to AOCI. The policy statement (notes:10, note_history:7) now names this CyberArk-driven update as the exception to 'no material changes'.",
    "account": "convertible senior notes; other income, net; AOCI",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For convertible senior notes acquired from CyberArk, we have elected fair value option to simplify the accounting for embedded features that would otherwise require bifurcation from the debt-host",
    "paragraph_id": "0001327567-26-000015:notes:13",
    "explanation": false
  },
  {
    "id": "earnings_quality_capped_calls_remeasured_through_other_income",
    "what_changed": "New policy: the capped calls assumed with CyberArk are carried as derivative assets at fair value in other assets. Fair value changes go to other income, net each period until settlement.",
    "account": "other assets (capped calls); other income, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We account for capped calls as derivative assets, measured at fair value on a recurring basis through maturity or settlement.",
    "paragraph_id": "0001327567-26-000015:notes:14",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_now_expected_to_add_jurisdictional_detail",
    "what_changed": "For the December 2023 income tax disclosure standard, the text no longer says the company is evaluating the impact. It now says adoption will add jurisdiction-level tax information to the consolidated financial statements (note_history:12).",
    "account": "income taxes (disclosure only)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We expect the adoption of this standard will result in disclosure of additional jurisdictional level tax information in our consolidated financial statements.",
    "paragraph_id": "0001327567-26-000015:notes:17",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_credit_loss_practical_expedient_not_expected_material",
    "what_changed": "For the July 2025 credit-loss practical expedient, the text changes from evaluating the impact to not expecting a material impact (note_history:14).",
    "account": "allowance for credit losses on accounts receivable and contract assets",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We do not expect the adoption of this standard will have a material impact on our consolidated financial statements.",
    "paragraph_id": "0001327567-26-000015:notes:21",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_qradar_contingent_consideration_undiscounted_range_restated",
    "what_changed": "The IBM QRadar contingent consideration paragraph is carried as changed text. It now states an undiscounted range of $0.3 billion to $0.5 billion. Payments began in the fiscal quarter ended October 2025 and run through the quarter ending October 2028. The prior range is not in my input; notes:40 says the payment estimate was reduced this quarter.",
    "account": "contingent consideration liability",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The estimated range of undiscounted contingent consideration is between $0.3 billion and $0.5 billion.",
    "paragraph_id": "0001327567-26-000015:notes:38",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_qradar_contingent_consideration_payment_estimate_reduced",
    "what_changed": "New sentence: in the quarter the company reduced its estimate of future contingent cash payments to IBM. It gives three reasons from its quarterly review: the magnitude and likelihood of customers entering qualified new transactions, the competitive industry environment, and current market conditions. mdna:112 records the resulting $110 million fair-value gain in general and administrative expense.",
    "account": "contingent consideration liability",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "we reduced our estimate of future cash payments based on our quarterly assessment of assumptions, including the magnitude and likelihood of customers entering into qualified new transactions, the competitive industry environment, and current market conditions",
    "paragraph_id": "0001327567-26-000015:notes:40",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_qradar_qualified_customer_transactions_and_competition",
    "what_changed": "The reasons given for the lower QRadar payment estimate are about customers: the magnitude and likelihood of customers entering qualified new transactions, and the competitive industry environment. Read as prose, the company now expects fewer or smaller qualifying customer transactions under the QRadar arrangement than it assumed before.",
    "account": "security operations subscription bookings from QRadar customers",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "including the magnitude and likelihood of customers entering into qualified new transactions, the competitive industry environment",
    "paragraph_id": "0001327567-26-000015:notes:40",
    "explanation": false
  },
  {
    "id": "earnings_quality_financing_receivables_sold",
    "what_changed": "The paragraph reports financing receivables sold: $49 million in the quarter and $54 million in the nine months, against $28 million and $30 million in the prior-year periods. Gains and losses were not material. Selling these receivables turns them into cash before customers pay.",
    "account": "financing receivables",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "We sold financing receivables of $49 million and $54 million for the three and nine months ended April 30, 2026, respectively",
    "paragraph_id": "0001327567-26-000015:notes:59",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_cyberark_acquisition_closed_and_consideration_stated",
    "what_changed": "The CyberArk acquisition was a pending subsequent event in the prior filing; it has now closed and been accounted for. Shareholders received $45.00 in cash plus 2.2005 company shares per CyberArk share. Total purchase consideration is $21.1 billion, made up of cash, 112 million shares and replacement awards (notes:75).",
    "account": "goodwill; intangible assets; common stock and additional paid-in capital",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "CyberArk shareholders received $45.00 in cash and 2.2005 shares of our common stock for each CyberArk share.",
    "paragraph_id": "0001327567-26-000015:notes:74",
    "explanation": false
  },
  {
    "id": "earnings_quality_cyberark_replacement_awards_add_future_share_based_compensation",
    "what_changed": "New: the company issued $945 million of replacement equity awards for CyberArk. The part for pre-acquisition service went into purchase consideration, which mdna:65 puts at $265 million. The rest will be expensed as share-based compensation over the remaining service periods.",
    "account": "share-based compensation expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The remaining fair value was allocated to future services and will be expensed over the remaining service periods as share-based compensation.",
    "paragraph_id": "0001327567-26-000015:notes:76",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_cyberark_allocation_brings_acquired_receivables_and_deferred_revenue",
    "what_changed": "New purchase price allocation. It brings acquired accounts receivable, investments, deferred revenue, convertible senior notes and deferred tax liabilities onto the balance sheet, alongside goodwill and identified intangibles. Period-end receivables and deferred revenue therefore include acquired balances, not only organic activity.",
    "account": "accounts receivable; deferred revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Accounts receivable, net of allowance for credit losses",
    "paragraph_id": "0001327567-26-000015:notes:77",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_cyberark_goodwill_deductible_for_us_tax",
    "what_changed": "New: CyberArk goodwill is attributed to the assembled workforce and to synergies from adding the identity platform. Substantially all of it is stated to be deductible for U.S. income tax purposes. By contrast, notes:70 says Chronosphere goodwill is not deductible.",
    "account": "cash income taxes",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Substantially all of goodwill is deductible for U.S. income tax purposes.",
    "paragraph_id": "0001327567-26-000015:notes:78",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_cyberark_intangible_useful_lives",
    "what_changed": "New: the CyberArk intangibles are given useful lives of 5 to 7 years for developed technology, 12 to 14 years for platform renewals, 2 years for customer contracts and 1 year for the trade name. The platform-renewals life is a management judgment that sets how fast most of the amortization comes through.",
    "account": "amortization of intangible assets",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "12 years - 14 years",
    "paragraph_id": "0001327567-26-000015:notes:79",
    "explanation": false
  },
  {
    "id": "earnings_quality_cyberark_transaction_costs_in_general_and_administrative",
    "what_changed": "New: CyberArk transaction costs were $41 million for the quarter and $56 million for the nine months, recorded mainly in general and administrative expense.",
    "account": "general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "transaction costs related to CyberArk acquisition were $41 million and $56 million, respectively, which were primarily included in general and administrative expense",
    "paragraph_id": "0001327567-26-000015:notes:80",
    "explanation": false
  },
  {
    "id": "earnings_quality_cyberark_workforce_optimization_severance_plan",
    "what_changed": "New integration plan to optimize the combined workforce, at a total estimated cost of $59 million, to be substantially complete by the end of fiscal 2027. At April 30, 2026, $12 million had been paid and a $12 million severance liability sat in accrued compensation. notes:83 shows the severance charges spread across cost of subscription and support revenue, R&D, S&M and G&A.",
    "account": "accrued compensation (severance); operating expenses",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "for a total estimated cost of $59 million. The activities associated with this plan are expected to be substantially completed by the end of fiscal 2027.",
    "paragraph_id": "0001327567-26-000015:notes:81",
    "explanation": true
  },
  {
    "id": "structure_and_disclosure_changes_koi_acquisition_closed_consideration_restated",
    "what_changed": "Koi closed on April 14, 2026. In the prior filing it was a pending agreement for total consideration of $300 million in cash and replacement awards, expected to close in the second half of fiscal 2026 (note_history:60, removed). The text now gives purchase consideration of $231 million, substantially all cash, and discloses $61 million of replacement awards separately (notes:86).",
    "account": "goodwill; cash",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The total purchase consideration for the acquisition of Koi was $231 million, substantially all of which is comprised of cash.",
    "paragraph_id": "0001327567-26-000015:notes:85",
    "explanation": false
  },
  {
    "id": "earnings_quality_koi_replacement_awards_add_future_share_based_compensation",
    "what_changed": "New: $61 million of Koi replacement equity awards, all allocated to future service and to be expensed as share-based compensation. They include 0.3 million restricted shares vesting over three years.",
    "account": "share-based compensation expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we issued $61 million of replacement equity awards, which was allocated to future services and will be expensed over the remaining service periods as share-based compensation",
    "paragraph_id": "0001327567-26-000015:notes:86",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_koi_goodwill_deductible_for_us_tax",
    "what_changed": "New: Koi goodwill is attributed to workforce and synergies and is stated to be deductible for U.S. income tax purposes.",
    "account": "cash income taxes",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The goodwill is deductible for U.S. income tax purposes.",
    "paragraph_id": "0001327567-26-000015:notes:88",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_portkey_definitive_agreement",
    "what_changed": "New: on the last day of the quarter the company signed a definitive agreement to acquire Portkey for $140 million in cash and replacement awards, subject to adjustments, to enhance Prisma AIRS.",
    "account": "cash",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "On April 30, 2026, we entered into a definitive agreement to acquire Portkey, Inc., a privately-held AI Gateway company",
    "paragraph_id": "0001327567-26-000015:notes:91",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_portkey_acquisition_completed",
    "what_changed": "The subsequent events note now covers only Portkey, completed on May 29, 2026 and to be accounted for as a business combination in the fourth quarter of fiscal 2026. The prior subsequent events (the CyberArk closing and the Koi agreement) were removed because both deals closed in the quarter (note_history:56 to note_history:60).",
    "account": "goodwill; intangible assets",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "On May 29, 2026, we completed the acquisition of Portkey. This acquisition will be accounted for as a business combination in the fourth quarter of fiscal 2026.",
    "paragraph_id": "0001327567-26-000015:notes:189",
    "explanation": false
  },
  {
    "id": "earnings_quality_chronosphere_and_cyberark_contribution_to_revenue_and_operating_loss",
    "what_changed": "New sentence quantifying what Chronosphere and CyberArk contributed since their acquisition dates: revenue of $388 million for the quarter and $391 million for the nine months, and an operating loss of $523 million and $524 million.",
    "account": "operating income (loss)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the combined net impact of the Chronosphere and CyberArk acquisitions on our condensed consolidated statements of operations was revenue of $388 million and $391 million and operating loss of $523 million and $524 million",
    "paragraph_id": "0001327567-26-000015:notes:93",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_pro_forma_combines_cyberark_on_different_period_ends",
    "what_changed": "New pro forma basis. The company's quarters ending April 30 are combined with CyberArk's historical results for the three and nine months ended March 31, 2026 and 2025. Adjustments cover amortization, replacement-award share-based compensation, transaction costs, workforce-plan severance and income tax.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "with the historical results of CyberArk for the three and nine months ended March 31, 2026 and 2025, respectively",
    "paragraph_id": "0001327567-26-000015:notes:96",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_provisional_purchase_accounting_measurement_period",
    "what_changed": "The measurement-period caveat, carried as changed text, now refers to 'our acquisitions', which this quarter include CyberArk and Koi. Allocations, including income tax and other contingencies, may still change within 12 months of each acquisition date.",
    "account": "goodwill; intangible assets; deferred taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "may become known during the remainder of the measurement period, not to exceed 12 months from the acquisition date, which may result in changes to the amounts and allocations recorded",
    "paragraph_id": "0001327567-26-000015:notes:97",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_headquarters_lease_amendments_extend_term",
    "what_changed": "New: in April 2026 the company signed three amendments extending the Santa Clara headquarters leases by twelve years to July 2040, with renewal options through July 2052. Net lease payments are about $469 million, and the text says right-of-use assets rose by $262 million in exchange for new operating lease liabilities.",
    "account": "operating lease right-of-use assets; operating lease liabilities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In April 2026, we entered into three lease amendments to extend the lease terms of our current corporate headquarters in Santa Clara, California for a period of twelve years through July 2040.",
    "paragraph_id": "0001327567-26-000015:notes:139",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_share_repurchase_authorization_raised_and_extended",
    "what_changed": "New: on March 10, 2026 the board added $1.0 billion to the repurchase program, for a total authorization of $5.1 billion, and extended its expiry to December 31, 2026.",
    "account": "cash; shares outstanding",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "On March 10, 2026, our board of directors authorized an additional $1.0 billion increase to our share repurchase program, bringing the total authorization under this share repurchase program to $5.1 billion",
    "paragraph_id": "0001327567-26-000015:notes:156",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_executed",
    "what_changed": "New: in the quarter the company repurchased and retired 7 million shares for $1.0 billion at an average of $147.70 per share, after no repurchases in the prior-year periods. $1.0 billion of authorization remains.",
    "account": "cash; common stock and additional paid-in capital",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "we repurchased and retired 7 million shares of our common stock under our current repurchase authorization for an aggregate purchase price of $1.0 billion, including transaction costs, at an average price of $147.70 per share",
    "paragraph_id": "0001327567-26-000015:notes:157",
    "explanation": false
  },
  {
    "id": "earnings_quality_accelerated_vesting_charge_from_cyberark_and_koi",
    "what_changed": "New: vesting of certain equity awards was accelerated in connection with CyberArk and Koi, producing $177 million of share-based compensation. Of that, $140 million is in general and administrative, $36 million in sales and marketing and $1 million in cost of subscription and support revenue. mdna:112 cites this as a cause of higher G&A.",
    "account": "share-based compensation; general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the vesting of certain equity awards was accelerated in connection with our acquisitions of CyberArk and Koi; as a result, we recorded share-based compensation of $177 million",
    "paragraph_id": "0001327567-26-000015:notes:176",
    "explanation": false
  },
  {
    "id": "earnings_quality_negative_effective_tax_rate_tied_to_cyberark",
    "what_changed": "The income tax note now names the CyberArk acquisition, along with decreased excess tax benefits from share-based compensation, as what drove the effective tax rates: negative 13.5% for the quarter and 26.8% for the nine months. notes:178 names CyberArk as a reason the rate differs from the statutory rate.",
    "account": "provision for income taxes",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the three months ended April 30, 2026, our provision for income taxes reflected an effective tax rate of negative 13.5%",
    "paragraph_id": "0001327567-26-000015:notes:179",
    "explanation": false
  },
  {
    "id": "earnings_quality_effective_tax_rate_fluctuation_during_cyberark_integration",
    "what_changed": "New forward-looking sentence: the effective tax rate may keep fluctuating as CyberArk is integrated into the corporate structure and intercompany relationships.",
    "account": "provision for income taxes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We may continue to see fluctuations in our effective tax rate as we further integrate CyberArk into our corporate structure and intercompany relationships.",
    "paragraph_id": "0001327567-26-000015:mdna:123",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_diluted_share_count_excludes_assumed_notes_and_capped_calls",
    "what_changed": "New sentence: the 2030 Notes and capped calls are left out of diluted per-share amounts as antidilutive.",
    "account": "diluted weighted-average shares",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our 2030 Notes and capped calls were also excluded from the calculation of diluted net income (loss) per share as the effect would have been antidilutive.",
    "paragraph_id": "0001327567-26-000015:notes:185",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_assumed_cyberark_convertible_notes_exchangeable_into_company_shares",
    "what_changed": "New: through a supplemental indenture the company assumed CyberArk's $1.25 billion of 0.0% Convertible Senior Notes due June 15, 2030. The notes are now exchangeable into about 4.3161 company shares plus $88.2630 in cash per $1,000: 5.4 million shares at an effective conversion price of about $211.24, plus $110 million in cash. The indenture has no financial covenants. Redemption terms, conversion triggers (including the $280.75 sale price condition) and settlement terms are in notes:120 to notes:126.",
    "account": "convertible senior notes",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These modifications result in the 2030 Notes being exchangeable initially for 5.4 million shares of our common stock with an effective initial conversion price of approximately $211.24 per share of common stock, subject to adjustments, and an initial cash amount of $110 million.",
    "paragraph_id": "0001327567-26-000015:notes:119",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_make_whole_conversions_elected_for_cash_settlement",
    "what_changed": "New: the CyberArk deal was both a make-whole fundamental change and a fundamental change under the indenture. The company elected cash settlement for notes surrendered in the make-whole period, and holders surrendered $153 million of principal. No holder used the repurchase right, and both rights expired on March 20, 2026.",
    "account": "convertible senior notes; cash",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "certain holders of the 2030 Notes surrendered $153 million in aggregate principal amount of the 2030 Notes during the make-whole fundamental change period for conversion",
    "paragraph_id": "0001327567-26-000015:notes:127",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_surrendered_convertible_notes_cash_settlement",
    "what_changed": "New: at April 30, 2026 the surrendered notes were a current liability at a fair value of $160 million, based on daily conversion values from March 24 to May 5, 2026. They were paid in cash on May 7, 2026, after quarter-end.",
    "account": "cash; short-term convertible senior notes",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The 2030 Notes surrendered for conversion during the make-whole conversion period were settled in cash for $160 million on May 7, 2026.",
    "paragraph_id": "0001327567-26-000015:notes:128",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_remaining_assumed_notes_long_term_classification_rests_on_sale_price_condition",
    "what_changed": "New: the remaining $1.1 billion of principal is classified as long-term because the sale price condition was not met in the calendar quarter ended March 31, 2026. Its fair value is $1.2 billion, based on the notes' trading price. The condition is tested each calendar quarter (notes:122; mdna:133), so the classification can change.",
    "account": "long-term convertible senior notes; working capital",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "the remaining 2030 Notes with an aggregate principal amount of $1.1 billion were classified as a long-term liability on our condensed consolidated balance sheets since the sale price condition was not met during the calendar quarter ended March 31, 2026",
    "paragraph_id": "0001327567-26-000015:notes:129",
    "explanation": false
  },
  {
    "id": "earnings_quality_fair_value_loss_on_assumed_notes_in_other_income",
    "what_changed": "New: fair value changes on the 2030 Notes were a $37 million loss in earnings (other income, net) and a $12 million loss from instrument-specific credit risk in AOCI. mdna:121 names this loss as one reason other income fell in the quarter.",
    "account": "other income, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "changes in fair value of 2030 Notes included in earnings were a loss of $37 million, and changes in fair value attributable to instrument-specific credit risk included in AOCI were a loss of $12 million",
    "paragraph_id": "0001327567-26-000015:notes:130",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capped_calls_partially_terminated_for_cash",
    "what_changed": "New: in April 2026 the company terminated portions of the assumed capped calls for $10 million in cash, matching the $153 million of surrendered notes. notes:134 puts the remaining capped calls at a fair value of $94 million, with a $1 million loss.",
    "account": "other assets (capped calls)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "In April 2026, we elected to terminate portions of the capped calls in exchange for $10 million in cash",
    "paragraph_id": "0001327567-26-000015:notes:133",
    "explanation": false
  },
  {
    "id": "across_documents_eight_k_financing_obligation_not_described_in_debt_note",
    "what_changed": "The debt note's credit facility text is unchanged; the note change history shows only the balance-date sentence at notes:138 changed. Yet the 8-K index in input_8k.md lists a filing dated 2026-04-13 (0001193125-26-151637) with Items 1.01 (material definitive agreement) and 2.03 (creation of a direct financial obligation), and its body is not in my input. Neither the debt note nor MD&A liquidity (mdna:134) describes any agreement or obligation entered in April 2026. The supervisor should establish what that filing created.",
    "account": "debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Credit Facility matures on April 13, 2028.",
    "paragraph_id": "0001327567-26-000015:notes:136",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_no_internal_control_change_reported_despite_cyberark_close",
    "what_changed": "Item 4 reports no change in internal control over financial reporting during the quarter ended April 30, 2026, the quarter in which CyberArk and Koi closed. The text says nothing about bringing the acquired businesses into the control environment or leaving them out of it. The prior Item 4 is not in my input, so I can't tell whether the wording itself changed.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "There were no changes in our internal control over financial reporting identified in connection with the evaluation",
    "paragraph_id": "0001327567-26-000015:item_4_controls:5",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_identity_security_platform_section_added",
    "what_changed": "New Identity Security section describing the CyberArk-based platform, named Idira (mdna:28 to mdna:34). Its offerings are workforce identity, IT and developer privileged access, machine identity, identity governance and AI agent security.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "our next-generation identity security platform, is designed to secure human, agentic and machine identities across the enterprise with intelligent privilege controls and continuous threat prevention",
    "paragraph_id": "0001327567-26-000015:mdna:29",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_unit_forty_two_frontier_ai_defense_services_launched",
    "what_changed": "New sentence: in April 2026 the company launched a suite of Unit 42 Frontier AI Defense services.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In April 2026, we launched a new suite of Unit 42 Frontier AI Defense services to help customers proactively discover and neutralize threats introduced by next-generation AI models.",
    "paragraph_id": "0001327567-26-000015:mdna:36",
    "explanation": false
  },
  {
    "id": "results_against_expectations_total_revenue_growth_attributed_to_adoption_and_acquisitions",
    "what_changed": "The overview, carried as changed text, gives quarterly total revenue of $3.0 billion against $2.3 billion, which it describes as 31% year-over-year growth. It credits both portfolio adoption and recent acquisitions; notes:93 states the acquired revenue.",
    "account": "total revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our growth reflects the increased adoption of our portfolio, which consists of product, subscriptions, and support, and our recent acquisitions.",
    "paragraph_id": "0001327567-26-000015:mdna:37",
    "explanation": false
  },
  {
    "id": "revenue_recognition_cyberark_on_premise_licenses_now_in_product_revenue",
    "what_changed": "New sentence: since the CyberArk acquisition in February 2026, product revenue includes on-premise software licenses for certain identity security offerings.",
    "account": "product revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "our product revenue also includes on-premise software licenses of certain identity security offerings",
    "paragraph_id": "0001327567-26-000015:mdna:39",
    "explanation": false
  },
  {
    "id": "revenue_recognition_identity_software_licenses_recognized_at_delivery",
    "what_changed": "The product revenue paragraph, carried as changed text, now lists certain identity security offerings among the software licenses in product revenue. It says product revenue is recognized at hardware shipment or software license delivery. It also expects software licenses to grow as a share of product revenue as license contracts are renewed. The identity license revenue therefore lands up front at delivery, not over time.",
    "account": "product revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We recognize product revenue at the time of hardware shipment or delivery of software license.",
    "paragraph_id": "0001327567-26-000015:mdna:70",
    "explanation": false
  },
  {
    "id": "results_against_expectations_product_revenue_increase_drivers_include_cyberark_licenses",
    "what_changed": "The product revenue increase is attributed to software licenses, demand for new-generation hardware and CyberArk software license revenue. CyberArk licenses are named as a driver for the first time.",
    "account": "product revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in product revenue for the three and nine months ended April 30, 2026 was also driven by increased software licenses revenue from our CyberArk acquisition closed in February 2026.",
    "paragraph_id": "0001327567-26-000015:mdna:72",
    "explanation": false
  },
  {
    "id": "results_against_expectations_subscription_and_support_growth_attributed_to_acquisitions",
    "what_changed": "The subscription and support revenue increase is attributed to end-customer demand and to recent acquisitions.",
    "account": "subscription and support revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "due to increased demand for our subscription and support offerings from our end-customers and our recent acquisitions",
    "paragraph_id": "0001327567-26-000015:mdna:77",
    "explanation": false
  },
  {
    "id": "across_documents_regional_revenue_growth_explained_without_acquisitions",
    "what_changed": "The geographic explanation credits revenue growth in the Americas, EMEA and APAC to continued investment in the global sales force and to the Americas' scale. It does not mention acquisitions. Meanwhile mdna:37 and mdna:77 name recent acquisitions as a growth driver, and notes:93 attributes $388 million of the quarter's revenue to Chronosphere and CyberArk.",
    "account": "revenue by geography",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "as we continued to increase investment in our global sales force in order to support our growth and innovation, with the Americas contributing the highest increase in revenue due to its larger scale",
    "paragraph_id": "0001327567-26-000015:mdna:80",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_intangible_amortization_in_cost_of_product_revenue",
    "what_changed": "The cost-of-product-revenue components, carried as changed text, include amortization of intangible assets and tariff costs. notes:107 has a cost-of-product-revenue amortization row with dashes in the prior-year columns. mdna:86 names CyberArk amortization as a cause of higher cost of product revenue.",
    "account": "cost of product revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "inventory excess and obsolete charges, shipping and tariff costs, amortization of intangible assets, product testing costs, and shared costs",
    "paragraph_id": "0001327567-26-000015:mdna:84",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_excess_and_obsolete_charges_decreased",
    "what_changed": "MD&A says inventory excess and obsolete charges decreased and partly offset the rise in cost of product revenue, for both the quarter and the nine months. mdna:95 repeats the point for the nine-month product margin. No reason is given for the lower charges.",
    "account": "inventory excess and obsolete reserve; cost of product revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a decrease in inventory excess and obsolete charges",
    "paragraph_id": "0001327567-26-000015:mdna:86",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_tariff_costs_in_product_cost",
    "what_changed": "Cost of product revenue is said to have risen partly because of higher tariff costs, alongside hardware demand and CyberArk amortization.",
    "account": "cost of product revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "increased demand for our hardware products and higher tariff costs",
    "paragraph_id": "0001327567-26-000015:mdna:86",
    "explanation": false
  },
  {
    "id": "earnings_quality_subscription_cost_increase_from_cloud_hosting_amortization_and_personnel",
    "what_changed": "The cost of subscription and support explanation gives three stated increases, each for the quarter and the nine months: cloud hosting costs up $75 million and $171 million, acquisition amortization up $117 million and $109 million, and personnel costs up $71 million and $97 million, including acquired headcount.",
    "account": "cost of subscription and support revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Cloud hosting service costs, which support our cloud-based subscription offerings, increased $75 million and $171 million for the three and nine months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:91",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_hardware_gross_margin_decline",
    "what_changed": "Product gross margin is said to have fallen mainly because hardware gross margin decreased and amortization rose, partly offset by CyberArk license revenue. For the nine months there was a further offset from the shift in mix toward software and from lower inventory excess and obsolete charges.",
    "account": "product gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to a decrease in gross margin on our hardware products and higher amortization of intangible assets",
    "paragraph_id": "0001327567-26-000015:mdna:95",
    "explanation": false
  },
  {
    "id": "earnings_quality_subscription_margin_decline_attributed_to_acquisition_amortization",
    "what_changed": "The subscription and support gross margin decline is attributed mainly to acquisition amortization. The margin sentence does not name the cloud hosting and personnel cost increases that mdna:91 lists.",
    "account": "subscription and support gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Subscription and support gross margin decreased for the three and nine months ended April 30, 2026 compared to the same periods in 2025 primarily due to higher amortization of intangible assets as a result of our recent acquisitions.",
    "paragraph_id": "0001327567-26-000015:mdna:96",
    "explanation": false
  },
  {
    "id": "earnings_quality_research_and_development_personnel_growth_including_acquired_headcount",
    "what_changed": "R&D growth is attributed to personnel costs, up $192 million for the quarter and $233 million for the nine months, driven by headcount growth that includes headcount from recent acquisitions.",
    "account": "research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "which grew $192 million and $233 million for the three and nine months ended April 30, 2026 compared to the same periods in 2025, largely due to headcount growth, including headcount from our recent acquisitions",
    "paragraph_id": "0001327567-26-000015:mdna:103",
    "explanation": false
  },
  {
    "id": "earnings_quality_sales_and_marketing_personnel_and_acquisition_amortization",
    "what_changed": "S&M growth is attributed to personnel costs, up $254 million for the quarter and $408 million for the nine months including acquired headcount, and to higher acquisition-related amortization of intangibles.",
    "account": "sales and marketing expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in sales and marketing expense in both periods were further driven by higher amortization of intangible assets as a result of our recent acquisitions.",
    "paragraph_id": "0001327567-26-000015:mdna:107",
    "explanation": false
  },
  {
    "id": "results_against_expectations_general_and_administrative_outlook_excludes_acquisition_impact",
    "what_changed": "The G&A outlook, carried as changed text, is now stated excluding the near-term impact of recent acquisitions. The description also says G&A includes changes in fair value of the contingent consideration liability.",
    "account": "general and administrative expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Excluding the near-term impact of our recent acquisitions, we expect general and administrative expense to increase in absolute dollars over time",
    "paragraph_id": "0001327567-26-000015:mdna:110",
    "explanation": false
  },
  {
    "id": "earnings_quality_contingent_consideration_gain_offsets_general_and_administrative_expense",
    "what_changed": "New: G&A growth is attributed to accelerated vesting tied to acquisitions, CyberArk severance, headcount growth and acquisition-related costs. It is partly offset by a $110 million gain in the quarter from remeasuring the contingent consideration liability, which is recorded inside G&A. For the nine months the text also cites the prior-year $40 million partial release of a litigation accrual.",
    "account": "general and administrative expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a gain of $110 million for the change in fair value of contingent consideration liability during the three months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:112",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_income_gains_on_investments_sold_to_fund_acquisitions",
    "what_changed": "Nine-month other income is said to have risen because of gains on investments sold to fund acquisitions and higher interest income, partly offset by the fair-value loss on the notes. notes:187 shows a separate 'Other, net' line.",
    "account": "other income, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "primarily due to increased gains on sales of our investments to fund acquisitions",
    "paragraph_id": "0001327567-26-000015:mdna:121",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_lower_average_cash_balances_reduce_interest_income",
    "what_changed": "The quarterly decline in other income is attributed partly to lower interest income from lower average cash, cash equivalent and investment balances.",
    "account": "interest income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "lower interest income as a result of lower average cash, cash equivalent and investment balances for the three months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:121",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_israel_research_and_development_tax_law",
    "what_changed": "New paragraph: Israel's R&D Law, approved in March 2026, gives a tax credit on qualifying Israeli R&D spending incurred after January 1, 2026. Unused credit is payable in cash after a set period, and further regulations are expected. The impact was not material this period.",
    "account": "provision for income taxes; research and development expense",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "It provides that all or a portion of the unutilized R&D tax credit will be paid in cash upon the lapse of a period stipulated by the R&D Law.",
    "paragraph_id": "0001327567-26-000015:mdna:126",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_foreign_earnings_repatriated_for_cyberark",
    "what_changed": "New sentence: as part of the CyberArk acquisition the company repatriated $3.5 billion of foreign earnings through an intercompany transaction, with immaterial state and other tax. Remaining unremitted earnings are still indefinitely reinvested.",
    "account": "cash; provision for income taxes",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As part of the acquisition of CyberArk, we executed an intercompany transaction to repatriate $3.5 billion of foreign earnings, resulting in immaterial income tax expense related to state and other taxes.",
    "paragraph_id": "0001327567-26-000015:mdna:130",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_assumed_notes_conversion_could_require_cash_principal_settlement",
    "what_changed": "New: the 2030 Notes' sale price condition was not met in the calendar quarter ended March 31, 2026, so there is no price-based conversion right in the June 2026 quarter. If the condition is met in the June quarter and holders convert in the September quarter, the company would owe the $1.1 billion principal in cash. Management says operating cash, existing cash and investments, access to financing and any capped-call proceeds would be enough.",
    "account": "cash; convertible senior notes",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "we would be obligated to settle the $1.1 billion principal amount of the 2030 Notes and a portion of our conversion obligation in excess of the aggregate principal amount of the 2030 Notes, if any, in cash",
    "paragraph_id": "0001327567-26-000015:mdna:133",
    "explanation": false
  },
  {
    "id": "across_documents_operating_cash_flow_attributed_to_collections",
    "what_changed": "MD&A credits the higher nine-month operating cash flow to business growth shown in increased collections, partly offset by higher spending. The notes report financing receivable sales in the same periods (notes:59), and CyberArk receivables arrived through the acquisition (notes:77). The prose does not say whether either fed the collections.",
    "account": "cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to growth of our business as reflected by increases in collections during the nine months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:149",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_investments_liquidated_to_fund_acquisitions",
    "what_changed": "Nine-month investing outflows are attributed to net cash paid for acquisitions, partly offset by higher proceeds from sales and maturities of investments and lower investment purchases.",
    "account": "investments",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to an increase in net cash payments for business acquisitions during the nine months ended April 30, 2026, partially offset by higher proceeds from sales and maturities of investments and lower purchases of investments.",
    "paragraph_id": "0001327567-26-000015:mdna:153",
    "explanation": false
  },
  {
    "id": "earnings_quality_contingent_consideration_payments_classified_in_financing",
    "what_changed": "New: financing outflows now include payments of the QRadar contingent consideration liability as well as share repurchases, and mdna:155 adds these payments to its list of financing activities. Because they are classed as financing, they sit outside operating cash flow and outside free cash flow as mdna:56 defines it.",
    "account": "cash used in financing activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to repurchase of our common stock and payments of our contingent consideration liability during the nine months ended April 30, 2026",
    "paragraph_id": "0001327567-26-000015:mdna:156",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_trust_security_and_prisma_airs_launches",
    "what_changed": "New sentence naming product launches: Next-Generation Trust Security (certificate lifecycle management) and Prisma AIRS 3.0. The same paragraph lists the CyberArk, Koi and Portkey completions, which are covered at notes:74, notes:85 and notes:189.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "we launched Next-Generation Trust Security that unifies certificate lifecycle management",
    "paragraph_id": "0001327567-26-000015:mdna:41",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_component_shortage_wording",
    "what_changed": "insufficient",
    "account": "cost of product revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "supply chain disruptions, including increased memory, storage or other component shortages",
    "paragraph_id": "0001327567-26-000015:mdna:44",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_israel_and_iran_hostilities_wording",
    "what_changed": "insufficient",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The hostilities in Israel, Iran and the surrounding region have continued to result in economic and political uncertainty.",
    "paragraph_id": "0001327567-26-000015:mdna:45",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_chronosphere_goodwill_paragraph",
    "what_changed": "insufficient",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The goodwill is not deductible for U.S. income tax purposes.",
    "paragraph_id": "0001327567-26-000015:notes:70",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_headquarters_land_purchase_timing",
    "what_changed": "insufficient",
    "account": "property and equipment, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "we purchased 14.5 acres of land adjacent to our headquarters in Santa Clara, California, for $91 million to accommodate future expansion of our headquarters",
    "paragraph_id": "0001327567-26-000015:notes:111",
    "explanation": false
  }
]
```

## Why the four `insufficient` items are insufficient

- `narrative_signs_of_operating_pressure_component_shortage_wording` (mdna:44): the macro-risk paragraph is carried as changed text, but its prior version is not in my input. I can't isolate which clause is new: the memory, storage or component shortages clause, the enforcement and administration policies clause, or the export and import controls clause. The shortage language fits with mdna:86 (tariffs) and mdna:95 (lower hardware gross margin), but I can't say it is new.
- `narrative_signs_of_operating_pressure_israel_and_iran_hostilities_wording` (mdna:45): carried as changed text with no prior version in my input. I can't tell whether naming Iran, or the stated intent to keep growing in Israel (relevant now that CyberArk and Koi are Israeli), is the new part.
- `structure_and_disclosure_changes_chronosphere_goodwill_paragraph` (notes:70): Chronosphere closed in the prior period, and this goodwill paragraph is carried as changed text. The prior wording is not in my input, and the note change history does not cover this tag, so I can't identify what moved.
- `liquidity_and_capital_headquarters_land_purchase_timing` (notes:111): the paragraph reports the $91 million land purchase for the nine months. My input doesn't show whether the purchase is new this quarter or only the period label rolled forward. The quarter's HQ lease extension (notes:139) concerns the same site.

## Paragraphs carried as text that are not items

### MD&A
- 0001327567-26-000015:mdna:5 — period label rolled forward (three and nine months).
- 0001327567-26-000015:mdna:11 — the mission statement adds "identities"; the same change is the notes:2 item.
- 0001327567-26-000015:mdna:14 — SASE and Prisma Browser product description; no account affected, and the change can't be isolated without the prior text.
- 0001327567-26-000015:mdna:17 — Prisma AIRS product description; no account affected.
- 0001327567-26-000015:mdna:21 — security operations product description; its Koi mention is covered by the notes:85 and notes:86 items.
- 0001327567-26-000015:mdna:28 — heading of the new Identity Security section (the item is at mdna:29).
- 0001327567-26-000015:mdna:30 — product description inside the new Identity Security section; covered by the mdna:29 item.
- 0001327567-26-000015:mdna:31 — product description inside the new Identity Security section; covered by the mdna:29 item.
- 0001327567-26-000015:mdna:32 — product description inside the new Identity Security section; covered by the mdna:29 item.
- 0001327567-26-000015:mdna:33 — product description inside the new Identity Security section; covered by the mdna:29 item.
- 0001327567-26-000015:mdna:34 — product description inside the new Identity Security section; covered by the mdna:29 item.
- 0001327567-26-000015:mdna:40 — subscription offering description with CyberArk identity subscriptions added; the substance is carried by the mdna:77 and mdna:29 items.
- 0001327567-26-000015:mdna:49 — wording only ("operating income (loss)").
- 0001327567-26-000015:mdna:50 — amounts only (NGS ARR, RPO).
- 0001327567-26-000015:mdna:51 — amounts only (key metrics table).
- 0001327567-26-000015:mdna:56 — amounts only (free cash flow table).
- 0001327567-26-000015:mdna:60 — amounts only (results of operations table).
- 0001327567-26-000015:mdna:62 — amounts only (share-based compensation table).
- 0001327567-26-000015:mdna:64 — heading.
- 0001327567-26-000015:mdna:65 — restates the CyberArk consideration and replacement awards; covered by the notes:74 and notes:76 items.
- 0001327567-26-000015:mdna:66 — comparability statement now naming CyberArk; the substance is covered by the notes:93 and mdna:37 items.
- 0001327567-26-000015:mdna:68 — revenue-variation expectation naming business acquisitions; the substance is covered by the mdna:37 item.
- 0001327567-26-000015:mdna:71 — amounts only (table).
- 0001327567-26-000015:mdna:75 — amounts only (table).
- 0001327567-26-000015:mdna:79 — amounts only (table).
- 0001327567-26-000015:mdna:85 — amounts only (table).
- 0001327567-26-000015:mdna:89 — list of cost components; the change can't be isolated without the prior text, and no direction is implied.
- 0001327567-26-000015:mdna:90 — amounts only (table).
- 0001327567-26-000015:mdna:94 — amounts only (table).
- 0001327567-26-000015:mdna:97 — page marker.
- 0001327567-26-000015:mdna:99 — amounts and date rolled forward ($3.6 billion of unrecognized share-based compensation over 2.6 years, same as notes:177).
- 0001327567-26-000015:mdna:102 — amounts only (table).
- 0001327567-26-000015:mdna:105 — S&M description; no change I can isolate, and no substance identified.
- 0001327567-26-000015:mdna:106 — amounts only (table).
- 0001327567-26-000015:mdna:108 — page marker.
- 0001327567-26-000015:mdna:111 — amounts only (table).
- 0001327567-26-000015:mdna:114 — wording (interest expense definition tied to the matured 2025 Notes).
- 0001327567-26-000015:mdna:115 — amounts only (table).
- 0001327567-26-000015:mdna:116 — date rolled forward (the 2025 Notes' June 2025 maturity was disclosed before).
- 0001327567-26-000015:mdna:117 — page marker.
- 0001327567-26-000015:mdna:119 — other income components now name the fair value changes on the notes and capped calls; covered by the notes:13 and notes:14 items.
- 0001327567-26-000015:mdna:120 — amounts only (table).
- 0001327567-26-000015:mdna:124 — amounts only (table).
- 0001327567-26-000015:mdna:125 — same substance as the notes:179 item.
- 0001327567-26-000015:mdna:127 — page marker.
- 0001327567-26-000015:mdna:129 — amounts only (working capital and cash table).
- 0001327567-26-000015:mdna:132 — MD&A restatement of the 2030 Notes assumption, conversions and cash settlement; covered by the notes:119, notes:127 and notes:128 items.
- 0001327567-26-000015:mdna:134 — date rolled forward; referenced in the item at notes:136.
- 0001327567-26-000015:mdna:136 — restates the repurchase authorization; covered by the notes:156 item.
- 0001327567-26-000015:mdna:137 — page marker.
- 0001327567-26-000015:mdna:139 — lease obligation amount and the fiscal 2040 end date; covered by the notes:139 item.
- 0001327567-26-000015:mdna:140 — amounts only (purchase commitments).
- 0001327567-26-000015:mdna:141 — amounts only (contingent consideration balance); covered by the notes:40 item.
- 0001327567-26-000015:mdna:143 — period label rolled forward.
- 0001327567-26-000015:mdna:144 — amounts only (cash flow table).
- 0001327567-26-000015:mdna:150 — page marker.
- 0001327567-26-000015:mdna:155 — financing-activity list now naming contingent consideration payments; covered by the mdna:156 item.
- 0001327567-26-000015:mdna:161 — cross-reference wording.
- 0001327567-26-000015:mdna:162 — page marker.

### Notes
- 0001327567-26-000015:notes:10 — the policy-exception sentence (note_history:7); covered by the notes:13 and notes:14 items.
- 0001327567-26-000015:notes:11 — heading.
- 0001327567-26-000015:notes:12 — assumption of the notes and capped calls; covered by the notes:119 and notes:14 items.
- 0001327567-26-000015:notes:15 — heading.
- 0001327567-26-000015:notes:19 — wording only ("could be applied" became "can be applied", note_history:13).
- 0001327567-26-000015:notes:28 — amounts only (revenue by geography).
- 0001327567-26-000015:notes:30 — amounts only (revenue by type).
- 0001327567-26-000015:notes:32 — amounts and period rolled forward (revenue recognized from opening deferred revenue).
- 0001327567-26-000015:notes:34 — amounts and date rolled forward (RPO).
- 0001327567-26-000015:notes:35 — date rolled forward.
- 0001327567-26-000015:notes:36 — amounts only.
- 0001327567-26-000015:notes:37 — amounts; the new rows (capped calls, short- and long-term convertible notes) are covered by the notes:13, notes:14, notes:128 and notes:129 items.
- 0001327567-26-000015:notes:42 — amounts only (contingent consideration rollforward); covered by the notes:40 item.
- 0001327567-26-000015:notes:43 — date rolled forward.
- 0001327567-26-000015:notes:44 — heading.
- 0001327567-26-000015:notes:45 — date rolled forward (note_history:45).
- 0001327567-26-000015:notes:46 — amounts only (note_history:46).
- 0001327567-26-000015:notes:47 — amounts only (July 31, 2025 comparative table).
- 0001327567-26-000015:notes:48 — date rolled forward (note_history:47).
- 0001327567-26-000015:notes:49 — date rolled forward (note_history:48).
- 0001327567-26-000015:notes:50 — amounts only.
- 0001327567-26-000015:notes:51 — heading.
- 0001327567-26-000015:notes:52 — amounts and date rolled forward (note_history:49 and :50).
- 0001327567-26-000015:notes:53 — heading and date rolled forward.
- 0001327567-26-000015:notes:54 — amounts only.
- 0001327567-26-000015:notes:56 — amounts only (risk-rating table).
- 0001327567-26-000015:notes:58 — date rolled forward.
- 0001327567-26-000015:notes:61 — amounts and date rolled forward.
- 0001327567-26-000015:notes:62 — amounts and date rolled forward.
- 0001327567-26-000015:notes:63 — amounts and date rolled forward.
- 0001327567-26-000015:notes:75 — amounts (consideration table); covered by the notes:74 item.
- 0001327567-26-000015:notes:82 — table lead-in.
- 0001327567-26-000015:notes:83 — amounts (severance charges by line); covered by the notes:81 item.
- 0001327567-26-000015:notes:84 — heading.
- 0001327567-26-000015:notes:87 — amounts (Koi allocation); covered by the notes:85 item.
- 0001327567-26-000015:notes:89 — amounts (Koi intangibles); covered by the notes:85 item.
- 0001327567-26-000015:notes:90 — heading.
- 0001327567-26-000015:notes:94 — pro forma lead-in now naming CyberArk; covered by the notes:96 item.
- 0001327567-26-000015:notes:95 — amounts only (pro forma table).
- 0001327567-26-000015:notes:98 — duplicate lead-in for the Chronosphere consideration (disclosed in the prior period), in a separate tag block.
- 0001327567-26-000015:notes:99 — duplicate of the notes:74 lead-in, in a separate tag block.
- 0001327567-26-000015:notes:101 — table lead-in, date rolled forward.
- 0001327567-26-000015:notes:102 — amounts only (goodwill table).
- 0001327567-26-000015:notes:104 — table lead-in, date rolled forward.
- 0001327567-26-000015:notes:105 — amounts (intangibles table); the new rows are covered by the notes:79 item.
- 0001327567-26-000015:notes:106 — table lead-in.
- 0001327567-26-000015:notes:107 — amounts (amortization by line); the new cost-of-product row is covered by the mdna:84 item.
- 0001327567-26-000015:notes:108 — table lead-in, date rolled forward.
- 0001327567-26-000015:notes:109 — amounts only (future amortization).
- 0001327567-26-000015:notes:112 — heading.
- 0001327567-26-000015:notes:113 — unchanged according to the note change history.
- 0001327567-26-000015:notes:114 — wording only (tense, note_history:16).
- 0001327567-26-000015:notes:115 — wording only (tense, note_history:17).
- 0001327567-26-000015:notes:116 — period rolled forward; the Q2-only split sentence was dropped (note_history:38).
- 0001327567-26-000015:notes:117 — heading.
- 0001327567-26-000015:notes:118 — heading.
- 0001327567-26-000015:notes:120 — redemption terms of the newly assumed 2030 Notes; part of the notes:119 item.
- 0001327567-26-000015:notes:121 — conversion lead-in for the newly assumed 2030 Notes; part of the notes:119 item.
- 0001327567-26-000015:notes:122 — sale price condition term ($280.75); part of the notes:119, notes:129 and mdna:133 items.
- 0001327567-26-000015:notes:123 — trading-price conversion term; part of the notes:119 item.
- 0001327567-26-000015:notes:124 — corporate-event conversion term; part of the notes:119 item.
- 0001327567-26-000015:notes:125 — conversion term from February 15, 2030; part of the notes:119 item.
- 0001327567-26-000015:notes:126 — settlement and fundamental-change terms; part of the notes:119 and notes:127 items.
- 0001327567-26-000015:notes:131 — heading.
- 0001327567-26-000015:notes:132 — terms of the assumed capped calls (strike and cap prices); part of the notes:14 and notes:133 items.
- 0001327567-26-000015:notes:134 — amounts (capped call fair value and loss); part of the notes:133 item.
- 0001327567-26-000015:notes:135 — heading.
- 0001327567-26-000015:notes:137 — unchanged according to the note change history.
- 0001327567-26-000015:notes:138 — date rolled forward (note_history:37).
- 0001327567-26-000015:notes:140 — heading.
- 0001327567-26-000015:notes:141 — date rolled forward (note_history:1).
- 0001327567-26-000015:notes:142 — amounts only (purchase commitments, note_history:2).
- 0001327567-26-000015:notes:143 — unchanged according to the note change history (only note_history:1 to :3 changed in this block).
- 0001327567-26-000015:notes:144 — heading.
- 0001327567-26-000015:notes:145 — unchanged according to the note change history.
- 0001327567-26-000015:notes:146 — unchanged according to the note change history.
- 0001327567-26-000015:notes:147 — unchanged according to the note change history.
- 0001327567-26-000015:notes:148 — unchanged according to the note change history.
- 0001327567-26-000015:notes:149 — unchanged according to the note change history.
- 0001327567-26-000015:notes:150 — amounts and dates rolled forward (Centripetal accrual and interest, note_history:3).
- 0001327567-26-000015:notes:151 — unchanged according to the note change history.
- 0001327567-26-000015:notes:152 — unchanged according to the note change history.
- 0001327567-26-000015:notes:153 — unchanged according to the note change history.
- 0001327567-26-000015:notes:154 — unchanged according to the note change history.
- 0001327567-26-000015:notes:159 — table lead-in, period rolled forward.
- 0001327567-26-000015:notes:160 — amounts only (RSU and PSU activity).
- 0001327567-26-000015:notes:162 — footnote now naming CyberArk and Koi assumed RSUs; covered by the notes:76 and notes:86 items.
- 0001327567-26-000015:notes:166 — PSU grant paragraph; it reads as the standing program with the period and share counts rolled forward. The prior text is not in my input.
- 0001327567-26-000015:notes:167 — table lead-in, period rolled forward.
- 0001327567-26-000015:notes:168 — amounts only (Monte Carlo assumptions).
- 0001327567-26-000015:notes:170 — date rolled forward.
- 0001327567-26-000015:notes:171 — table lead-in, period rolled forward.
- 0001327567-26-000015:notes:172 — amounts only (PSO activity).
- 0001327567-26-000015:notes:175 — amounts only (share-based compensation table).
- 0001327567-26-000015:notes:177 — amounts and date rolled forward.
- 0001327567-26-000015:notes:178 — same substance as the notes:179 item.
- 0001327567-26-000015:notes:180 — wording ("net income (loss)" labels).
- 0001327567-26-000015:notes:181 — wording ("net income (loss)" labels).
- 0001327567-26-000015:notes:182 — amounts only (EPS table).
- 0001327567-26-000015:notes:183 — wording ("net income (loss)" labels).
- 0001327567-26-000015:notes:184 — amounts only (antidilutive table).
- 0001327567-26-000015:notes:187 — amounts; the new fair-value rows are covered by the notes:130 and notes:134 items.
- 0001327567-26-000015:notes:188 — heading.

### Item 4, controls
- 0001327567-26-000015:item_4_controls:1 — heading.
- 0001327567-26-000015:item_4_controls:2 — heading.
- 0001327567-26-000015:item_4_controls:3 — date rolled forward. It concludes that disclosure controls are effective, citing Rule 13a-15(f); whether that citation is new cannot be seen.
- 0001327567-26-000015:item_4_controls:4 — heading.
- 0001327567-26-000015:item_4_controls:6 — heading.
- 0001327567-26-000015:item_4_controls:7 — limitations boilerplate.
- 0001327567-26-000015:item_4_controls:8 — page marker.

### 8-K
- input_8k.md has item codes only and no item bodies, so there are no 8-K paragraphs to read.
- The 2026-04-13 filing (1.01, 2.03, 9.01) is used in the notes:136 item.
- The other listed filings have no text to report. The 2026-02-11 (1.01, 2.03, 8.01, 9.01) and 2026-03-11 (8.01, 9.01) dates coincide with the supplemental indenture (notes:119) and the March 10 buyback increase (notes:156). That is a match on dates only; I have not seen those bodies.

### Note change history (not reported separately; each entry maps to a notes paragraph above)
- note_history:1, :2 and :3 map to notes:141, :142 and :150.
- :4 maps to notes:2, :5 to notes:3, :6 to notes:8, and :7 to notes:10.
- :8 to :11 map to notes:11 to :14; :12, :13 and :14 map to notes:17, :19 and :21.
- :15 (removed) is the prior estimates list; see the notes:8 item.
- :16, :17 and :18 map to notes:114, :115 and :116.
- :19 to :36 map to notes:117 to :134, and :37 maps to notes:138.
- :38 (removed) is the Q2 warrant split; see notes:116.
- :39 to :42 duplicate notes:11 to :14 under the debt policy tag.
- :43 and :45 map to notes:45; :44 and :46 map to notes:46; :47 maps to notes:48; :48 maps to notes:49; :49 and :50 map to notes:52.
- :51 maps to notes:28, :52 and :55 map to notes:30, :53 maps to notes:32, and :54 maps to notes:34.
- :56 maps to notes:188 and :57 to notes:189.
- :58 (removed CyberArk subsequent event) relates to the notes:3 and notes:74 items.
- :59 and :60 (removed Koi subsequent event) relate to the notes:85 item.
