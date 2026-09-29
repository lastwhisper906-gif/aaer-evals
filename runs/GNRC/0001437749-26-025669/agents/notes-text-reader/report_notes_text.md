# Notes-text reader report: GNRC 10-Q 0001437749-26-025669 (quarter ended June 30, 2026)

## Scope

Files read in full:
- `input_notes.md`
- `input_notes_history.md` (change history 0001437749-26-014882 → 0001437749-26-025669)
- `input_mdna.md`
- `input_controls.md` (Item 4)
- `input_8k.md` (the July 29, 2026 Item 2.02 release, plus the item-code and late-filing lists)
- `input_prior_predictions.md`

Inputs not in my directory:
- No auditor's report (this is a 10-Q).
- No Item 1A diff and no Exhibit 21 diff.
- No Exhibit 10.
- No 8-K bodies other than the 2.02 release.
- The late-filing list shows none.
- Prior flags: none on record.

Nothing out of bounds was found: no trend table, prices, returns, short interest, other companies' files or prior probabilities. The 8-K release includes its own condensed statements as part of the 8-K body. I used them for nothing: no arithmetic and no comparisons.

How to read the items:
- Where the text states a figure, the item repeats it. Where the prose gives no direction, direction is `none`. No item says whether a balance rose or fell unless the prose itself says so.
- `what_changed` starts with `insufficient:` when a paragraph is carried as changed but the prior wording is not in my input, so the edit itself can't be identified. There are 5 such items.
- `explanation` is true on 5 items: 2 on reserves, 1 on inventory, and 2 on receivable-type balances.

## Items

```json
{ "id": "estimates_and_discretion_tariff_refund_loss_recovery_model",
  "what_changed": "New 'Tariff Refund' section. After the February 20, 2026 Supreme Court decision invalidating IEEPA tariffs, the Company elected to account for refunds under a loss recovery model (ASC 410-30). A recovery asset is recognized only when receipt is probable under ASC 450-20. This is a new accounting election plus a new probability judgment; the prior 10-Q had neither. The critical-estimates paragraph (mdna:117) does not name it.",
  "account": "cost of goods sold (tariff recovery credit)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The Company elected to account for the refund of tariffs under a loss recovery model pursuant to Accounting Standards Codification (ASC) 410-30.",
  "paragraph_id": "0001437749-26-025669:notes:9",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_tariff_refund_receivable_deemed_probable",
  "what_changed": "New: a tariff refund receivable of approximately $27,700 is recorded in prepaid expenses and other current assets, on management's judgment that receipt is probable. Separately, refunds of approximately $61,400 were received in cash during the period. The receivable sits outside the accounts receivable line. No collection timing is stated.",
  "account": "prepaid expenses and other current assets (tariff refund receivable)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Additionally, the Company recorded a tariff refund receivable within prepaid expenses and other current assets in the condensed consolidated balance sheets of approximately $27,700 for which the Company has deemed receipt probable to occur.",
  "paragraph_id": "0001437749-26-025669:notes:10",
  "explanation": true }
```

```json
{ "id": "earnings_quality_tariff_refund_credited_to_cost_of_goods_sold",
  "what_changed": "New: approximately $71,100 of tariff recovery was recorded as a reduction of cost of goods sold in Q2. MD&A (mdna:61) and the release (8k:22) attribute about 6% of Q2 gross margin to it; MD&A (mdna:82) attributes about 3% of first-half gross margin. The prose ties it to recovery of tariff amounts previously paid, following a single court decision.",
  "account": "cost of goods sold; gross margin",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Approximately $71,100 of the tariff recovery was recorded as a reduction of cost of goods sold in the condensed consolidated statements of comprehensive income",
  "paragraph_id": "0001437749-26-025669:notes:10",
  "explanation": false }
```

```json
{ "id": "earnings_quality_tariff_refund_remainder_held_in_inventories",
  "what_changed": "New: the part of the tariff recovery not credited to cost of goods sold was recorded in inventories. That lowers inventory carrying cost now and should reach cost of goods sold when the inventory is sold. The prose gives no amount for the remainder (I do not derive one) and no timing. MD&A (mdna:37) says the same: 'the remainder reflected in inventory'.",
  "account": "inventories; cost of goods sold in later periods",
  "expected_direction": "down",
  "horizon": "this quarter for inventories; next quarter for cost of goods sold",
  "quote": "and the remainder was recorded in inventories in the condensed consolidated balance sheets.",
  "paragraph_id": "0001437749-26-025669:notes:10",
  "explanation": true }
```

```json
{ "id": "earnings_quality_tariff_refund_kept_inside_adjusted_metrics",
  "what_changed": "New: the release says net income, adjusted net income and adjusted EBITDA all include the approximately $71 million pre-tax tariff refund. The reconciliations remove disposition losses, legal and regulatory items (a credit this quarter) and Wallbox fair-value changes, but have no line removing the refund. MD&A (mdna:144) says Adjusted EBITDA is a target for senior-executive compensation. The raised full-year margin outlook also includes the refund (8k:36).",
  "account": "adjusted EBITDA; adjusted net income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Net income, adjusted net income, and adjusted EBITDA all include a pre-tax impact of approximately $71 million related to tariff refunds that were recorded during the current year quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:14",
  "explanation": false }
```

```json
{ "id": "across_documents_tariff_refund_gross_margin_wording",
  "what_changed": "The two documents word the same 6% figure differently. The release says the refunds 'contributed approximately 6% to gross margin during the quarter'. The 10-Q MD&A (mdna:61) says 'approximately 6% to gross margin growth during the quarter'. The first reads as a share of the margin level, the second as a share of its change. The numbers reader should check which reading the figures support.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The increase was primarily driven by tariff refunds which contributed approximately 6% to gross margin during the quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:22",
  "explanation": false }
```

```json
{ "id": "earnings_quality_segment_margin_gains_attributed_to_tariff_refunds",
  "what_changed": "New segment attribution. MD&A says the Residential adjusted EBITDA margin increase was primarily driven by tariff refunds: about 9% for Q2 and about 5% for the first half (mdna:88). For C&I it attributes about 2% for Q2 (mdna:66) and about 1% for the first half (mdna:87), together with acquisitions/divestitures and operating leverage. The prose gives these percentages as stated; I draw nothing from them.",
  "account": "Residential and C&I segment adjusted EBITDA",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "This increase was primarily driven by tariff refunds which impacted margins by approximately 9%, as well as favorable sales mix and operational efficiencies resulting in lower operating expenses.",
  "paragraph_id": "0001437749-26-025669:mdna:67",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_underlying_gross_margin_mix_and_input_costs",
  "what_changed": "New Q2 explanation. Apart from the tariff refunds, the prose says unfavorable sales mix and higher input costs were only partly offset by favorable price realization. The first-half paragraph (mdna:82) says mix and input costs 'more than offset favorable price realization'. So the prose describes a gross-margin headwind underneath the refund. It should become visible once the refund no longer contributes. The release (8k:22) repeats the sentence.",
  "account": "gross margin excluding tariff refunds",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Additionally, unfavorable sales mix and higher input costs were partially offset by favorable price realization.",
  "paragraph_id": "0001437749-26-025669:mdna:61",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_margin_guidance_raise_attributed_to_tariff_refund",
  "what_changed": "Full-year 2026 guidance changed. Net income margin (before NCI) is now approximately 9.0 to 10.0%; it was 8.0 to 9.0%. Adjusted EBITDA margin is now approximately 20.0 to 21.0%; it was 18.5 to 19.5%. The release says the increase is primarily due to the Q2 tariff refund, with an approximate 1.5% full-year impact. Net sales growth guidance stays at mid-to-high teens (8k:19). Whether anything besides the refund moved in the outlook is for the numbers reader.",
  "account": "full-year net income margin and adjusted EBITDA margin (guidance)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "This increased outlook is primarily due to the tariff refund included in the second quarter, which is expected to have an approximate 1.5% impact for the full year 2026.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:36",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_c_and_i_sales_guidance_now_low_thirties",
  "what_changed": "The C&I full-year sales outlook is 'now' growth in the low 30% range, which the release credits to continued significant momentum in the data center market. The prior segment outlook is not in my input.",
  "account": "C&I segment net sales (full-year 2026)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "C&I segment sales are now expected to grow in the low 30% range during the year as a result of continued significant momentum in the data center market",
  "paragraph_id": "0001437749-26-024731:8k_2_02:35",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_residential_sales_guidance_high_single_digit",
  "what_changed": "The Residential full-year outlook is 'now' an increase in the high-single-digit range. The prior segment outlook is not in my input. The outlook states a full-year increase. The Q2 prose (mdna:59) and first-half prose (mdna:80) both describe Residential total sales as decreased. What that implies for the second half is for the numbers reader.",
  "account": "Residential segment net sales (full-year 2026)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Residential segment sales are now projected to increase in the high-single digit range from the prior year.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:35",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_first_hyperscale_committed_volume_terms_finalized",
  "what_changed": "New: product-specific terms under the global supply agreement with a leading hyperscale operator were 'recently finalized', committing 'nearly $700 million of volume for 2027'. The agreement itself was disclosed earlier in the quarter. The release does not say whether the terms were finalized before or after June 30. That date decides whether the volume could be in the June 30 remaining-performance-obligation figure (notes:119). The forward-looking list names cancellation rights in certain data center contracts (mdna:8). Neither the release nor the carried 10-Q text says whether these units will be recognized at a point in time or over time under cost-to-cost (notes:117).",
  "account": "C&I net sales; remaining performance obligations; contract assets and liabilities",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In addition, product specific terms related to this agreement were recently finalized, which committed nearly $700 million of volume for 2027.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:16",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_second_hyperscale_agreement_terms_unfinalized",
  "what_changed": "New: a global supply agreement with a second hyperscale customer was signed June 24, 2026. Final product-specific terms for 2027 and 2028 volumes are still being negotiated. The release says the approximately $1.6 billion data center backlog includes no volume from this customer. None of the 10-Q paragraphs carried to me mention this agreement.",
  "account": "C&I net sales (2027 and 2028)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "On June 24th, the Company secured a global supply agreement with a second hyperscale customer and is currently negotiating final product specific terms for 2027 and 2028 volumes.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:17",
  "explanation": false }
```

```json
{ "id": "across_documents_data_center_backlog_versus_remaining_performance_obligations",
  "what_changed": "The release says data center backlog 'has now increased to approximately $1.6 billion as of today' (July 29), with about $1 billion of additional orders since the prior update. It presents the backlog as visibility to 'significant 2027 growth' (8k:5). The 10-Q note gives remaining performance obligations of approximately $143,000 (thousands) at June 30 (notes:119). That figure excludes extended warranty and, by practical expedient, contracts with an original term of one year or less. Neither document reconciles backlog to RPO. The different dates, the one-year expedient and the difference between orders and enforceable contracts are possible reasons. Reconciliation is for the supervisor.",
  "account": "remaining performance obligations (Note 11)",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "In total, our backlog for products serving the data center market has now increased to approximately $1.6 billion as of today, which does not include any committed volumes from the second hyperscale customer.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:20",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations_restated",
  "what_changed": "Rewritten RPO sentence: approximately $143,000 at June 30, 2026, with approximately 80% expected within two years. The March 31 text (history:41) stated approximately $272,000 and approximately 90%. The prose gives no reason and does not mention deliveries, cancellations or a change in scope.",
  "account": "remaining performance obligations",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "the aggregate amount of revenue that the Company expects to recognize on remaining performance obligations (excluding extended warranty) was approximately $143,000, of which approximately 80% is expected to be recognized as revenue over the next two years.",
  "paragraph_id": "0001437749-26-025669:notes:119",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_cost_to_cost_contract_assets_disclosed",
  "what_changed": "New paragraph and a new balance category. Contract assets are unbilled receivables on contracts accounted for under the cost-to-cost (over-time) method, where revenue recognized on costs incurred runs ahead of billing. They sit in prepaid expenses and other current assets, not in accounts receivable. Stated balances: $78,730 at June 30, 2026 and $8,867 at December 31, 2025. The prior 10-Q note named no cost-to-cost method. The contracts involved are not identified. Cost-to-cost revenue depends on management's estimates of cost to complete. The data center 'ramping revenue' prose (mdna:58) points to more of this activity.",
  "account": "contract assets (in prepaid expenses and other current assets); net sales",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Contract assets primarily consist of unbilled receivables associated with contracts accounted for under the cost-to-cost method of revenue recognition, where revenue recognized based on costs incurred exceeds amounts billed to customers.",
  "paragraph_id": "0001437749-26-025669:notes:117",
  "explanation": true }
```

```json
{ "id": "revenue_recognition_c_and_i_over_time_recognition_in_segment_description",
  "what_changed": "insufficient: the paragraph is carried as changed but its prior wording is not in my input. As now written, C&I revenue is recognized at a point in time or, where the performance obligation is satisfied over time, by a method reflecting performance under the contract. The C&I product list includes battery energy storage, mobile heaters and mobile pumps. The over-time language matches the new cost-to-cost disclosure (notes:117), but I cannot confirm from my input that it is newly added.",
  "account": "C&I net sales; contract assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "C&I segment revenues are recorded at either a point in time when control of the product is transferred to the customer, or if the performance obligation is satisfied over time, then revenue is recognized using a method that reflects the performance under the contract.",
  "paragraph_id": "0001437749-26-025669:notes:73",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_contract_liabilities_redefined_as_customer_deposits",
  "what_changed": "Rewritten: contract liabilities are now defined as primarily customer deposits in excess of revenue recognized. Stated balance excluding extended warranty: $117,918 at June 30, 2026 and $151,257 at December 31, 2025, with $90,360 of revenue recognized in the six months from the December 31 balance. The March 31 text (history:41) described 'customer deposits and other contract liabilities' of $137,438, with $46,832 recognized in three months. The other-accrued-liabilities table (notes:99) has a separate 'Current contract liabilities' line that the prose does not tie to this figure. Reconciling the two is for the numbers reader.",
  "account": "contract liabilities (other accrued liabilities; deferred revenue)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Contract liabilities primarily consist of customer deposits that exceed revenue recognized.",
  "paragraph_id": "0001437749-26-025669:notes:118",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_standard_payment_terms_sentence_removed",
  "what_changed": "Removed: the paragraph saying standard customer payment terms are under one year, some customers prepay, and others get open credit after credit evaluation. A general timing-differences sentence replaces it (notes:116). The 10-Q drops its stated payment-term norm in the same quarter it introduces cost-to-cost contracts and large data center supply agreements.",
  "account": "accounts receivable; contract assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "While the Company’s standard payment terms for its customers are less than one year, the specific payment terms and conditions in its customer contracts vary.",
  "paragraph_id": "0001437749-26-014882:note_history:40",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_contract_balances_note_retitled",
  "what_changed": "Note 11 is retitled from 'Contract Liabilities' to 'Contract Balances'. It opens with a new framing sentence naming three categories: billed receivables, unbilled receivables (contract assets) and deferred revenue (contract liabilities). This is the first time the note presents contract assets as a category.",
  "account": "contract assets; contract liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "resulting in the recognition of billed accounts receivable, unbilled receivables (contract assets), or deferred revenue (contract liabilities) within the condensed consolidated balance sheets.",
  "paragraph_id": "0001437749-26-025669:notes:116",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_second_quarter_acquisitions_enercon_and_wolter",
  "what_changed": "New in the basis-of-presentation list and the acquisitions note (notes:19, notes:20). Enercon (custom power equipment and industrial enclosures) was acquired in April 2026. Substantially all assets and liabilities of Wolter Power Systems were acquired in May 2026; Wolter is described as an industrial and residential generator distributor and maintenance/repair provider. The text does not say whether Wolter distributed the Company's own products, which would turn sales to it into intercompany sales. All acquisitions are placed in C&I (notes:22). The release cites higher intangible amortization (8k:23).",
  "account": "goodwill; intangible assets; amortization of intangibles",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "In May 2026, the Company acquired substantially all of the assets and liabilities of the Wolter Power Systems (Wolter) business, headquartered in Brookfield, Wisconsin.",
  "paragraph_id": "0001437749-26-025669:notes:4",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_preliminary_purchase_price_allocation",
  "what_changed": "New: the combined preliminary purchase price for Allmand, Enercon and Wolter is $348,482. It is net of cash and includes holdbacks and estimated contingent consideration; $44,785 of it was funded with treasury stock. The allocation rests on management's fair-value estimates. Purchase accounting will be finalized before March 31, 2027 for Allmand and before June 30, 2027 for Enercon and Wolter. There is no material change to Allmand's allocation so far. The Q1 subsequent-events note (history:43) gave Enercon's preliminary price alone as $122,322. The goodwill and intangibles allocation remains open to measurement-period adjustment.",
  "account": "goodwill; intangible assets",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Company recorded its preliminary purchase price allocation based on its estimates of the fair value of the acquired assets and assumed liabilities.",
  "paragraph_id": "0001437749-26-025669:notes:22",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_enercon_contingent_consideration_earnout",
  "what_changed": "New: the Enercon earnout runs through April 1, 2027, is earned on specified target EBITDA levels, and is payable 35% in restricted shares and the rest in cash. $91,551 of contingent consideration is recorded for Enercon (notes:61); the Q1 subsequent-events note said the earnout could reach a maximum of $112,043. Total contingent consideration is stated as $121,866 at June 30, 2026 and $32,872 at December 31, 2025. The current portion, $105,858, is in other accrued liabilities. The Pramac period ended at December 31, 2025. Fair-value remeasurement is an estimate, and Adjusted EBITDA excludes contingent-consideration adjustments (notes:84 footnote 2).",
  "account": "other accrued liabilities (accrued contingent consideration)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "is earned based on the achievement of specified target EBITDA levels during the earnout period, with 35% payable in restricted shares and the remainder in cash.",
  "paragraph_id": "0001437749-26-025669:notes:58",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_contingent_consideration_settled_in_shares",
  "what_changed": "New: a $3,917 Chilicon earnout payment was settled in shares and treated as non-cash in the cash flow statement. Enercon's upfront $44,785 was paid in treasury shares and 35% of its earnout is payable in restricted shares. So part of the acquisition cost now runs through equity rather than investing or financing cash. The treasury-stock note (notes:139) says shares are reissued for contingent consideration.",
  "account": "treasury stock; contingent consideration",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "(2) Represents payment of $3,917 in shares for the Chilicon acquisition. The payment of common stock is accounted for as a non-cash item in the condensed consolidated statements of cash flows.",
  "paragraph_id": "0001437749-26-025669:notes:62",
  "explanation": false }
```

```json
{ "id": "earnings_quality_diluted_eps_includes_contingent_consideration_shares",
  "what_changed": "insufficient: the paragraph is carried as changed but its prior wording is not in my input. As now written, diluted EPS assumes certain acquisition contingent-consideration conditions are satisfied at period end. That matters because 35% of the Enercon earnout is payable in restricted shares. I cannot confirm the clause is new.",
  "account": "weighted average diluted shares",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "as well as the satisfaction of certain acquisition contingent consideration conditions as of the end of the period.",
  "paragraph_id": "0001437749-26-025669:notes:141",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_pending_new_way_acquisition",
  "what_changed": "New: in June 2026 the Company signed an agreement to buy the assets and assume the liabilities of New Way Power Proprietary Limited, a back-up power supplier in Johannesburg, South Africa. Closing is expected in Q4 2026. No price or segment is stated. It is disclosed inside the acquisitions note, and there is no subsequent-events note.",
  "account": "goodwill; C&I net sales",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "a supplier of back-up power solutions, located in Johannesburg, South Africa. The acquisition is expected to close in the fourth quarter of 2026.",
  "paragraph_id": "0001437749-26-025669:notes:21",
  "explanation": false }
```

```json
{ "id": "across_documents_acquisitions_called_immaterial_while_credited_for_growth",
  "what_changed": "The acquisitions note omits pro forma information because the effects are 'not material'. The same filing and the release credit acquisitions elsewhere:\n- MD&A gives net contribution from non-annualized acquisitions and divestitures of $16.6 million for Q2 (mdna:60) and $34.6 million for the first half (mdna:81), primarily C&I.\n- The release credits about 6% of C&I growth to acquisitions, divestitures and FX (8k:28).\n- MD&A cites acquisitions in the C&I margin increase (mdna:66).\n- The release says Enercon and Belvidere are 'significantly expanding capacity' (8k:18).\nWhether 'not material' fits these statements is a supervisor judgment.",
  "account": "net sales; C&I segment",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Pro forma and other financial information are not presented as the effects of these acquisitions are not material",
  "paragraph_id": "0001437749-26-025669:notes:23",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_june_dispositions_in_both_segments",
  "what_changed": "New: on June 1, 2026 the Company completed two immaterial business dispositions, one in C&I and one in Residential, with a combined loss of $13,392. The businesses are not named. With the two Q1 dispositions, four closed in the first half (mdna:158). The goodwill rollforward table (notes:105) shows a disposition entry only in the C&I column.",
  "account": "loss attributable to business dispositions (other expense); goodwill",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "the Company completed one immaterial business disposition within the Commercial & Industrial segment and one immaterial business disposition within the Residential segment, resulting in a combined loss of $13,392.",
  "paragraph_id": "0001437749-26-025669:notes:28",
  "explanation": false }
```

```json
{ "id": "earnings_quality_disposition_losses_added_back_to_adjusted_metrics",
  "what_changed": "New footnote text. The 'Other' add-back in Adjusted EBITDA and the disposition add-back in adjusted net income now cover four immaterial dispositions in 2026; the prior-year footnote covered one. Disposition losses are taken out of the adjusted metrics, but the tariff refund credit is left in (8k:14). The same footnote appears in notes:86, mdna:171 and 8k:129.",
  "account": "adjusted EBITDA; adjusted net income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The current year loss relates primarily to four immaterial business dispositions with two closing in the first quarter and two closing in the second quarter of 2026.",
  "paragraph_id": "0001437749-26-025669:mdna:158",
  "explanation": false }
```

```json
{ "id": "earnings_quality_wallbox_mark_to_market_gain_reduces_other_expense",
  "what_changed": "New Q2 explanation: MD&A says lower other expense, net was driven primarily by a fair-value gain on the Wallbox warrants and equity securities, plus lower interest expense and higher investment income, partly offset by disposition losses. The notes report Q2 gains on both the warrants (notes:44) and the shares (notes:55). The gain is a non-operating mark-to-market item and is excluded from the adjusted metrics.",
  "account": "other expense, net (change in fair value of investments)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The reduction in other expense, net was driven primarily by a gain in the fair value of our investment in warrants and equity securities of Wallbox N.V as well as lower interest expense and higher investment income in the current year quarter",
  "paragraph_id": "0001437749-26-025669:mdna:63",
  "explanation": false }
```

```json
{ "id": "earnings_quality_effective_tax_rate_prior_year_disposition_discrete_item",
  "what_changed": "The effective tax rate is stated as 24.6% against 20.0% for the six months, and 24.6% against 17.2% for Q2 (mdna:64). The text says the increase came primarily from a non-recurring favorable discrete item in the prior-year period related to a business disposition. The release (8k:24) gives the same explanation without the disposition reference.",
  "account": "provision for income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in effective tax rate was primarily related to a non-recurring favorable discrete item in the prior year period related to a business disposition that did not repeat in the current year period.",
  "paragraph_id": "0001437749-26-025669:notes:146",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_tariff_receipts_and_working_capital",
  "what_changed": "New drivers. MD&A attributes the six-month operating cash flow increase to higher operating earnings, $61 million of tariff refund receipts and lower cash tax payments. These are partly offset by 'a greater use of cash for working capital', which the prose does not break down; no paragraph explains the receivables or inventory movements. The release counts the refund receipts in the free cash flow increase (8k:25). MD&A still expects cash tax savings from OBBBA (mdna:45).",
  "account": "net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in operating cash flows for the six months ended June 30, 2026 was driven by higher operating earnings, cash receipts from tariff refunds totaling $61 million, and lower cash tax payments in the current year period.",
  "paragraph_id": "0001437749-26-025669:mdna:109",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_aggressive_capacity_investment_plan",
  "what_changed": "New: the CEO says the Company is 'investing aggressively' in production and packaging capacity for large megawatt generators and plans more as the pipeline materializes. The prose gives no amount or capex guidance. MD&A (mdna:115) still says there are no material changes to contractual obligations beyond borrowings.",
  "account": "expenditures for property and equipment; property and equipment",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "we are investing aggressively in incremental production and packaging capacity for large megawatt generators and are planning to add further capacity as our pipeline of opportunities materializes",
  "paragraph_id": "0001437749-26-024731:8k_2_02:20",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_belvidere_facility_acquired",
  "what_changed": "New in the release: the Company acquired an additional facility in Belvidere, Illinois during the quarter, for large megawatt generator packaging. None of the 10-Q paragraphs carried to me mention Belvidere. The text does not say whether it was a property purchase or part of a business combination.",
  "account": "property and equipment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "and acquired an additional facility in Belvidere, Illinois, significantly expanding capacity for large megawatt generator packaging.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:18",
  "explanation": false }
```

```json
{ "id": "across_documents_contractual_obligations_said_unchanged",
  "what_changed": "The window is rolled forward to June 30, 2026, and the statement is kept: no material changes to contractual obligations except borrowings and interest rates. The same filing and release add:\n- Enercon contingent consideration, with a current portion of $105,858 (notes:58).\n- A signed agreement to acquire New Way (notes:21).\n- Hyperscale supply agreements with committed 2027 volume (8k:16).\n- Aggressive capacity investment (8k:20).\nWhether any of these belong in contractual obligations is a supervisor judgment.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "There have been no material changes to our contractual obligations between the February 18, 2026, filing of our Annual Report on Form 10-K for the year ended December 31, 2025, and June 30, 2026, except for the changes in outstanding borrowings and interest rates",
  "paragraph_id": "0001437749-26-025669:mdna:115",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_domestic_industrial_distributor_channel",
  "what_changed": "New Q2 C&I prose: outside data center, higher shipments to rental and telecom were 'more than offset' by lower shipments to the domestic industrial distributor channel. The first-half paragraph (mdna:79) lists rental and telecom as growth drivers and the distributor decline only as a partial offset. The Q2 wording is the weaker of the two for the traditional distributor channel. The release (8k:28) repeats it.",
  "account": "C&I net sales (non-data-center channels)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "In addition, increased shipments to rental and telecom channel customers were more than offset by a decrease in shipments to the domestic industrial distributor channel.",
  "paragraph_id": "0001437749-26-025669:mdna:58",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_residential_storage_and_portable_shipments",
  "what_changed": "New Q2 prose: Residential sales decreased, driven by lower energy storage and portable generator shipments and mostly offset by home standby growth. The first-half paragraph (mdna:80) says portable generator shipments were higher for the six months, so the Q2 prose now lists portables among the declines. The release (8k:31) repeats it.",
  "account": "Residential net sales",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "This modest sales decrease was primarily driven by lower energy storage system and portable generator shipments compared to the prior year, mostly offset by growth in home standby generator sales.",
  "paragraph_id": "0001437749-26-025669:mdna:59",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_residential_solar_storage_tax_credit_phase_out",
  "what_changed": "Carried as changed; the prior wording is not in my input. The paragraph now says OBBBA (July 2025) accelerated the phase-out of certain investment tax credits, with a negative impact on the residential solar and storage market thereafter. This matches the energy storage declines cited for Q2 and the first half (mdna:59, mdna:80).",
  "account": "Residential net sales (energy storage systems)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "The OBBBA that was enacted in the United States in July 2025 accelerated the phase out of certain investment tax credits, resulting in a negative impact to the residential solar & storage market thereafter.",
  "paragraph_id": "0001437749-26-025669:mdna:28",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_ollnova_settlement_reserve_reduced",
  "what_changed": "New: on June 4, 2026 the Federal Circuit vacated the $11,500 ecobee judgment and ordered a new trial, set for July 10, 2026. The parties then settled confidentially without admission. In Q2 the Company reduced the reserve for the verdict and interest to the settlement amount. Neither the settlement amount nor its date is stated, so it is unclear whether it was agreed before or after June 30. The legal add-back table (mdna:156) shows a parenthesized patent-lawsuit figure for Q2, so the release is taken out of Adjusted EBITDA. MD&A (mdna:62) cites lower legal expenses in operating expenses.",
  "account": "accrued legal reserve (other accrued liabilities); operating expenses",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "In the second quarter of 2026, the Company reduced the reserve established for the original verdict and interest to the amount of the settlement.",
  "paragraph_id": "0001437749-26-025669:notes:154",
  "explanation": true }
```

```json
{ "id": "articulation_and_the_filed_history_accrued_legal_fees_decrease_explained_by_settlement_payment",
  "what_changed": "New footnote to the other-accrued-liabilities table: the decrease in accrued legal and professional fees primarily reflects the $206,500 payment by the Company and its insurers on the Zawaski settlement. The Zawaski paragraph (notes:155) is unchanged per the note change history. It still says that 'As of March 31, 2026 and December 31, 2025' a $206,500 reserve and a $102,000 insurance receivable were carried, and that payment was made April 1, 2026. The insurance receivable's status at June 30 is not stated.",
  "account": "other accrued liabilities (accrued legal & professional fees); prepaid expenses and other assets (insurance receivable)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "(1) The decrease primarily relates to a $206,500 payment made by the Company and its insurance carriers to satisfy a legal obligation.",
  "paragraph_id": "0001437749-26-025669:notes:100",
  "explanation": true }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_oakland_county_appeal_filed",
  "what_changed": "Changed: the Q1 text said plaintiffs 'may appeal' the April 30, 2026 dismissal with prejudice; it now says they 'have appealed'. The securities class action stays open. A class-action cost line continues in the legal add-back table (mdna:156).",
  "account": "legal expense (class actions)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Plaintiffs have appealed the judgment of dismissal, and the Company intends to vigorously defend the judgment.",
  "paragraph_id": "0001437749-26-025669:notes:151",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_epa_additional_information_request",
  "what_changed": "New: in the DOJ/EPA/CARB portable-generator emissions matter, the Company received a request for additional information from the EPA on May 12, 2026. The text also now says the Company is responding to ancillary requests. No accrual or range is stated.",
  "account": "legal and regulatory accruals",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "including a request for additional information the Company received from the EPA",
  "paragraph_id": "0001437749-26-025669:notes:153",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_florida_standby_class_action_amended_theories",
  "what_changed": "Changed: the text now says the amended complaint added plaintiffs and 'theories of liability'. The allegations are recast in the past tense, and the surviving Florida claims are described as 'claims' (plural) for breach of express warranty. The case concerns home standby generators made or sold 2020–2024. No accrual is stated.",
  "account": "product warranty liability; legal reserves",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Plaintiffs amended their original complaint to include additional plaintiffs and theories of liability.",
  "paragraph_id": "0001437749-26-025669:notes:157",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_walling_matters_removed",
  "what_changed": "Removed from the contingencies note: the Walling securities class action (dismissal final, no appeal) and the related derivative action (voluntarily dismissed, history:7). Both had concluded by the prior 10-Q. The removal drops closed matters and does not change exposure.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Plaintiff did not appeal the dismissal, so it is final.",
  "paragraph_id": "0001437749-26-014882:note_history:6",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_subsequent_events_note_dropped",
  "what_changed": "Removed: the prior 10-Q's Note 17, Subsequent Events (the Enercon acquisition), is gone, and the notes carried to me contain no subsequent-events note. Post-period matters appear only inside other notes or only in the release:\n- The Ollnova settlement, described as 'Subsequently' (notes:154).\n- New Way, signed in June (notes:21).\n- The hyperscale terms 'recently finalized' (8k:16), in the release only.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "17. Subsequent Events",
  "paragraph_id": "0001437749-26-014882:note_history:42",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_executive_trading_plan_adopted",
  "what_changed": "New: on May 5, 2026 Kyle Raabe, EVP and President, Home Power Generation (the residential home power business), adopted a Rule 10b5-1 plan. It covers the sale of up to 1,939 shares and the exercise and sale of up to 1,063 options through December 31, 2026.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Kyle Raabe, Executive Vice President & President, Home Power Generation, adopted a Rule 10b5-1 trading plan",
  "paragraph_id": "0001437749-26-025669:notes:160",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_goodwill_reorganization_impairment_test",
  "what_changed": "insufficient: the paragraph is carried as changed but its prior wording is not in my input, and the event itself is from Q1. As now written:\n- The segment reorganization was a triggering event.\n- An interim quantitative test recorded $1,523 of goodwill impairment for one Residential reporting unit in Q1 2026.\n- The other affected units passed.\n- No headroom is disclosed.\nGoodwill was reassigned by relative fair value (notes:102). The critical-estimates paragraph (mdna:117) names goodwill impairment.",
  "account": "goodwill",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As a result of this test, the Company recorded $1,523 of goodwill impairment for one reporting unit within the Residential segment in the first quarter of 2026.",
  "paragraph_id": "0001437749-26-025669:notes:103",
  "explanation": false }
```

```json
{ "id": "earnings_quality_adjusted_ebitda_legal_addback_definition_open_ended",
  "what_changed": "insufficient: mdna:121 and mdna:135 are carried as changed but their prior wording is not in my input. As now written, the legal and regulatory add-back covers matters outside ordinary routine litigation, 'including but not limited to' class actions, government inquiries and IP litigation. The definition also names 'certain other specific provisions', and the bullet at mdna:135 adds 'large suits and settlements'. The release (8k:88) says 'such as large suits and settlements'. This quarter the add-back line is a credit (the Ollnova reserve reduction). The first half also includes a release of a 2022 clean-energy warranty provision (mdna:156).",
  "account": "adjusted EBITDA; adjusted net income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "including but not limited to class action lawsuits, government inquiries, and certain intellectual property litigation",
  "paragraph_id": "0001437749-26-025669:mdna:121",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_critical_accounting_estimates_list",
  "what_changed": "insufficient: carried as changed but the prior wording is not in my input. As now written, the critical estimates are goodwill and indefinite-lived intangible impairment, and income taxes. The list omits judgments this filing newly introduces:\n- the probability judgment on tariff recovery (notes:9)\n- cost-to-cost revenue (notes:117)\n- the preliminary purchase price allocations (notes:22)\n- the Enercon contingent consideration (notes:58)",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Management believes our most critical accounting estimates and assumptions are in the following areas: goodwill and other indefinite-lived intangible asset impairment assessment; and income taxes.",
  "paragraph_id": "0001437749-26-025669:mdna:117",
  "explanation": false }
```

```json
{ "id": "across_documents_committed_hyperscale_volume_versus_cancellation_rights",
  "what_changed": "The forward-looking list is carried as changed; which bullet is new is not visible to me. It now includes contract risk from terms with certain data center customers, including cancellation rights, delivery requirements and liability exposure. It also includes uncertainty about data center market growth. The release repeats both (8k:58, 8k:59). The same release calls the first hyperscale 2027 volume 'committed' (8k:16) and presents the backlog as 'visibility' (8k:5). The prose does not say whether cancellation rights apply to that committed volume or to the backlog.",
  "account": "C&I net sales; remaining performance obligations",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "increase in contract risk related to terms with certain data center customers, including cancellation rights, delivery requirements, and potential liability exposure tied to our performance obligations or other claimed damages;",
  "paragraph_id": "0001437749-26-025669:mdna:8",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_no_control_change_reported_amid_acquisitions_and_over_time_revenue",
  "what_changed": "The period is rolled forward with the same conclusion: no material ICFR change in Q2. In the same quarter:\n- the Enercon and Wolter acquisitions closed;\n- the notes first disclose cost-to-cost revenue and contract assets (notes:117);\n- the tariff-recovery accounting election was introduced (notes:9).\nItem 4 says nothing about integrating acquired businesses or new revenue processes. There is no auditor's report in the input (10-Q).",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "There have been no changes during the three months ended June 30, 2026 in our internal control over financial reporting",
  "paragraph_id": "0001437749-26-025669:item_4_controls:5",
  "explanation": false }
```

## Paragraphs read and not made into items

Item 4 (controls):
- `0001437749-26-025669:item_4_controls:1` — heading
- `0001437749-26-025669:item_4_controls:2` — heading
- `0001437749-26-025669:item_4_controls:3` — standard disclosure-controls conclusion (effective); no change stated
- `0001437749-26-025669:item_4_controls:4` — heading

MD&A:
- `0001437749-26-025669:mdna:12` — carried as changed, but the edit can't be identified without the prior text; strategic overview (data center / AI framing); no amount, commitment or estimate
- `0001437749-26-025669:mdna:32` — generic commodity, currency and tariff exposure language; edit not identifiable; no amount or commitment
- `0001437749-26-025669:mdna:37` — same tariff-refund facts as notes:10, rounded; itemized there
- `0001437749-26-025669:mdna:42` — July 2025 credit amendment restated; old event
- `0001437749-26-025669:mdna:44` — same ETR explanation as notes:146; itemized there
- `0001437749-26-025669:mdna:45` — OBBBA; period rolled forward; no impact stated (cash-tax expectation cited in the operating cash flow item)
- `0001437749-26-025669:mdna:46` — Pillar Two; period rolled forward; no impact stated
- `0001437749-26-025669:mdna:48` — heading
- `0001437749-26-025669:mdna:50` — results table; amounts only
- `0001437749-26-025669:mdna:52` — segment reorganization announced and effective in Q1; already disclosed
- `0001437749-26-025669:mdna:55` — table; amounts only
- `0001437749-26-025669:mdna:56` — table; amounts only
- `0001437749-26-025669:mdna:57` — table; amounts only
- `0001437749-26-025669:mdna:60` — amount only; used in the acquisitions-immaterial cross-document item
- `0001437749-26-025669:mdna:62` — opex explanation; legal-expense clause used in the Ollnova item, amortization in the acquisitions item
- `0001437749-26-025669:mdna:64` — same tax explanation as the notes:146 item
- `0001437749-26-025669:mdna:65` — amounts only
- `0001437749-26-025669:mdna:66` — C&I tariff-refund attribution; used in the segment tariff item
- `0001437749-26-025669:mdna:68` — amounts only; 'changes in certain add-back items' is generic
- `0001437749-26-025669:mdna:70` — heading
- `0001437749-26-025669:mdna:71` — table intro
- `0001437749-26-025669:mdna:72` — table; amounts only
- `0001437749-26-025669:mdna:73` — heading
- `0001437749-26-025669:mdna:74` — recast statement; reorganization already disclosed
- `0001437749-26-025669:mdna:75` — table intro
- `0001437749-26-025669:mdna:76` — table; amounts only
- `0001437749-26-025669:mdna:77` — table; amounts only
- `0001437749-26-025669:mdna:78` — table; amounts only
- `0001437749-26-025669:mdna:79` — first-half C&I drivers; used in the distributor-channel item
- `0001437749-26-025669:mdna:80` — first-half Residential drivers; used in the Residential items
- `0001437749-26-025669:mdna:81` — amount only; used in the acquisitions-immaterial cross-document item
- `0001437749-26-025669:mdna:82` — first-half gross margin; used in the underlying gross margin item
- `0001437749-26-025669:mdna:83` — first-half opex; same drivers as mdna:62
- `0001437749-26-025669:mdna:84` — first-half other expense; used in the Wallbox and disposition items
- `0001437749-26-025669:mdna:85` — first-half tax; same as the notes:146 item
- `0001437749-26-025669:mdna:86` — amounts only
- `0001437749-26-025669:mdna:87` — first-half C&I tariff attribution; used in the segment tariff item
- `0001437749-26-025669:mdna:88` — first-half Residential tariff attribution; used in the segment tariff item
- `0001437749-26-025669:mdna:89` — amounts only
- `0001437749-26-025669:mdna:90` — cross-reference
- `0001437749-26-025669:mdna:92` — general cash-requirements statement; edit not identifiable; no amount
- `0001437749-26-025669:mdna:93` — credit agreement restated; interest rate rolled forward
- `0001437749-26-025669:mdna:95` — borrowings and unused capacity rolled forward
- `0001437749-26-025669:mdna:96` — rate and leverage ratio rolled forward
- `0001437749-26-025669:mdna:97` — covenant ratios rolled forward
- `0001437749-26-025669:mdna:98` — buyback program; date rolled forward; authorization unchanged
- `0001437749-26-025669:mdna:99` — no repurchases; period rolled forward
- `0001437749-26-025669:mdna:101` — floor plan financing; amounts and percentages rolled forward
- `0001437749-26-025669:mdna:103` — liquidity amounts rolled forward
- `0001437749-26-025669:mdna:106` — heading
- `0001437749-26-025669:mdna:108` — cash flow table; amounts only
- `0001437749-26-025669:mdna:110` — investing cash flow narration; amounts only
- `0001437749-26-025669:mdna:111` — prior-year investing narration; amounts only
- `0001437749-26-025669:mdna:112` — financing cash flow narration; amounts only
- `0001437749-26-025669:mdna:113` — prior-year financing narration; amounts only
- `0001437749-26-025669:mdna:134` — non-GAAP bullet (interest-like fees); wording
- `0001437749-26-025669:mdna:135` — non-GAAP legal-provision bullet; used in the add-back definition item
- `0001437749-26-025669:mdna:144` — compensation and discretion paragraph; credit-agreement naming changed (wording); cited in the tariff-in-adjusted-metrics item
- `0001437749-26-025669:mdna:147` — reconciliation table; amounts only
- `0001437749-26-025669:mdna:153` — footnote (c); credit-agreement naming changed (wording)
- `0001437749-26-025669:mdna:155` — footnote intro
- `0001437749-26-025669:mdna:156` — legal add-back table; amounts; patent line cited in the Ollnova item
- `0001437749-26-025669:mdna:168` — adjusted net income table; amounts only
- `0001437749-26-025669:mdna:171` — same footnote text as mdna:158; itemized there

Notes:
- `0001437749-26-025669:notes:5` — periods rolled forward
- `0001437749-26-025669:notes:8` — heading (Tariff Refund); content itemized from notes:9 and notes:10
- `0001437749-26-025669:notes:12` — wording ('(ASC)' dropped)
- `0001437749-26-025669:notes:13` — pending ASU 2025-06; still assessing; no adoption or effect stated
- `0001437749-26-025669:notes:14` — pending ASU 2024-03; still assessing; no adoption or effect stated
- `0001437749-26-025669:notes:15` — period rolled forward
- `0001437749-26-025669:notes:17` — heading
- `0001437749-26-025669:notes:18` — Allmand (Q1 acquisition) restated; 'rental' added to the description (wording)
- `0001437749-26-025669:notes:19` — Enercon acquisition; used in the acquisitions item
- `0001437749-26-025669:notes:20` — Wolter acquisition; used in the acquisitions item
- `0001437749-26-025669:notes:24` — heading
- `0001437749-26-025669:notes:25` — table intro; restates that there were no material 2025 acquisitions
- `0001437749-26-025669:notes:26` — purchase price allocation table; amounts only
- `0001437749-26-025669:notes:32` — Juffali JV description; no substantive change identifiable
- `0001437749-26-025669:notes:34` — redeemable NCI rollforward; amounts only
- `0001437749-26-025669:notes:40` — interest rate swaps; date rolled forward
- `0001437749-26-025669:notes:41` — swap AOCI amounts rolled forward
- `0001437749-26-025669:notes:43` — Wallbox warrant history restated; no substantive change identifiable
- `0001437749-26-025669:notes:44` — warrant gain/loss amounts; cited in the Wallbox item
- `0001437749-26-025669:notes:47` — table; amounts only
- `0001437749-26-025669:notes:48` — swap fair values rolled forward
- `0001437749-26-025669:notes:51` — term-loan fair values rolled forward; instrument list names contract assets and liabilities, consistent with the contract-balances items
- `0001437749-26-025669:notes:55` — Wallbox share values and gains; amounts only; cited in the Wallbox item
- `0001437749-26-025669:notes:60` — contingent consideration rollforward table; used in the Enercon item
- `0001437749-26-025669:notes:61` — Enercon $91,551 footnote; used in the Enercon item
- `0001437749-26-025669:notes:64` — table intro; periods rolled forward
- `0001437749-26-025669:notes:65` — AOCI table; amounts only
- `0001437749-26-025669:notes:66` — AOCI table; amounts only
- `0001437749-26-025669:notes:67` — AOCI table; amounts only
- `0001437749-26-025669:notes:68` — AOCI table; amounts only
- `0001437749-26-025669:notes:69` — AOCI footnotes; amounts and currency names rolled forward
- `0001437749-26-025669:notes:71` — segment reorganization (Q1) restated; wording
- `0001437749-26-025669:notes:72` — Residential segment description; no substantive change identifiable
- `0001437749-26-025669:notes:76` — table; amounts only
- `0001437749-26-025669:notes:77` — table; amounts only
- `0001437749-26-025669:notes:78` — Adjusted EBITDA / CODM wording
- `0001437749-26-025669:notes:81` — segment table; amounts only
- `0001437749-26-025669:notes:82` — segment table; amounts only
- `0001437749-26-025669:notes:83` — Corporate column footnote; wording
- `0001437749-26-025669:notes:84` — segment table footnote definitions; no substantive change identifiable
- `0001437749-26-025669:notes:85` — legal add-back table; amounts; cited in the Ollnova item
- `0001437749-26-025669:notes:86` — footnotes (7) and (8); (8) is the same text as the mdna:158 item
- `0001437749-26-025669:notes:88` — segment assets table; amounts only
- `0001437749-26-025669:notes:89` — segment D&A table; amounts only
- `0001437749-26-025669:notes:90` — segment capex table; amounts only
- `0001437749-26-025669:notes:91` — U.S. sales and long-lived-asset percentages rolled forward; amounts only
- `0001437749-26-025669:notes:94` — inventory table; amounts only
- `0001437749-26-025669:notes:96` — PP&E table; amounts only
- `0001437749-26-025669:notes:97` — finance lease amounts rolled forward
- `0001437749-26-025669:notes:99` — other accrued liabilities table; amounts only; 'Current contract liabilities' line cited in the contract liabilities item
- `0001437749-26-025669:notes:102` — goodwill reassignment on reorganization; context for the goodwill item
- `0001437749-26-025669:notes:104` — table intro
- `0001437749-26-025669:notes:105` — goodwill rollforward table; amounts; cited in the dispositions item
- `0001437749-26-025669:notes:107` — warranty policy; no substantive change identifiable
- `0001437749-26-025669:notes:108` — warranty rollforward; amounts only (includes a row for acquired warranty reserves)
- `0001437749-26-025669:notes:110` — extended warranty rollforward; amounts only
- `0001437749-26-025669:notes:111` — date rolled forward
- `0001437749-26-025669:notes:112` — deferred revenue timing table; amounts only
- `0001437749-26-025669:notes:114` — warranty balance sheet table; amounts only
- `0001437749-26-025669:notes:115` — note retitled to Contract Balances; used in the contract-balances structure item
- `0001437749-26-025669:notes:120` — heading
- `0001437749-26-025669:notes:121` — short-term borrowings rolled forward
- `0001437749-26-025669:notes:122` — table intro
- `0001437749-26-025669:notes:123` — debt table reordered (Revolving Facility moved first); amounts only
- `0001437749-26-025669:notes:124` — deferred financing costs rolled forward
- `0001437749-26-025669:notes:125` — date rolled forward
- `0001437749-26-025669:notes:126` — maturities table; amounts only
- `0001437749-26-025669:notes:127` — original Term Loan B history; formatting only
- `0001437749-26-025669:notes:128` — rate rolled forward
- `0001437749-26-025669:notes:129` — net secured leverage ratio rolled forward; facility-name wording
- `0001437749-26-025669:notes:130` — wording ('depending on')
- `0001437749-26-025669:notes:131` — rate rolled forward; the 2025 debt-cost sentences from a removed paragraph merged in (reordered)
- `0001437749-26-025669:notes:132` — covenant ratios rolled forward
- `0001437749-26-025669:notes:133` — guarantee and collateral; no substantive change identifiable
- `0001437749-26-025669:notes:134` — date rolled forward
- `0001437749-26-025669:notes:135` — wording
- `0001437749-26-025669:notes:136` — cross-reference to the 10-K added; no substance
- `0001437749-26-025669:notes:139` — no repurchases; period rolled forward
- `0001437749-26-025669:notes:143` — EPS table; amounts only
- `0001437749-26-025669:notes:144` — anti-dilutive share counts; amounts only
- `0001437749-26-025669:notes:147` — heading
- `0001437749-26-025669:notes:148` — floor plan financing; amount rolled forward
- `0001437749-26-025669:notes:149` — PHS arbitration; no change per the note change history
- `0001437749-26-025669:notes:150` — solar MDL settlement; no change per the note change history
- `0001437749-26-025669:notes:152` — shareholder derivative actions; no change per the note change history
- `0001437749-26-025669:notes:155` — Zawaski; no change per the note change history; its stale March 31 balance wording is noted in the accrued-legal item
- `0001437749-26-025669:notes:156` — Champion patent case; no change per the note change history
- `0001437749-26-025669:notes:158` — general litigation statement; no change per the note change history

8-K Item 2.02 release (0001437749-26-024731):
- `0001437749-26-024731:8k_2_02:1` — exhibit header
- `0001437749-26-024731:8k_2_02:2` — file name
- `0001437749-26-024731:8k_2_02:3` — exhibit label
- `0001437749-26-024731:8k_2_02:4` — title
- `0001437749-26-024731:8k_2_02:5` — subtitle; backlog claim used in the backlog and cancellation-rights items
- `0001437749-26-024731:8k_2_02:6` — dateline
- `0001437749-26-024731:8k_2_02:7` — heading
- `0001437749-26-024731:8k_2_02:8` — sales amounts; the 2% acquisition/divestiture/FX note is used in the acquisitions-immaterial item
- `0001437749-26-024731:8k_2_02:9` — amounts only
- `0001437749-26-024731:8k_2_02:10` — amounts only
- `0001437749-26-024731:8k_2_02:11` — amounts only
- `0001437749-26-024731:8k_2_02:12` — amounts only
- `0001437749-26-024731:8k_2_02:13` — amounts only
- `0001437749-26-024731:8k_2_02:15` — cash flow amounts; used in the operating cash flow item
- `0001437749-26-024731:8k_2_02:19` — guidance summary; same content as the 8k:35 and 8k:36 items
- `0001437749-26-024731:8k_2_02:21` — heading
- `0001437749-26-024731:8k_2_02:23` — same as mdna:62
- `0001437749-26-024731:8k_2_02:24` — same as mdna:64, without the disposition reference
- `0001437749-26-024731:8k_2_02:25` — free cash flow narration; tariff receipts used in the operating cash flow item
- `0001437749-26-024731:8k_2_02:26` — heading
- `0001437749-26-024731:8k_2_02:27` — heading
- `0001437749-26-024731:8k_2_02:28` — same as mdna:58
- `0001437749-26-024731:8k_2_02:29` — same as mdna:66
- `0001437749-26-024731:8k_2_02:30` — heading
- `0001437749-26-024731:8k_2_02:31` — same as mdna:59
- `0001437749-26-024731:8k_2_02:32` — same as mdna:67
- `0001437749-26-024731:8k_2_02:33` — page number
- `0001437749-26-024731:8k_2_02:34` — heading
- `0001437749-26-024731:8k_2_02:37` — heading
- `0001437749-26-024731:8k_2_02:38` — webcast logistics
- `0001437749-26-024731:8k_2_02:39` — webcast logistics
- `0001437749-26-024731:8k_2_02:40` — webcast logistics
- `0001437749-26-024731:8k_2_02:41` — heading
- `0001437749-26-024731:8k_2_02:42` — boilerplate company description
- `0001437749-26-024731:8k_2_02:43` — heading
- `0001437749-26-024731:8k_2_02:44` — forward-looking boilerplate
- `0001437749-26-024731:8k_2_02:45` — forward-looking boilerplate
- `0001437749-26-024731:8k_2_02:46` — forward-looking bullet (power outages); same list as mdna:8
- `0001437749-26-024731:8k_2_02:47` — forward-looking bullet (raw materials); same list as mdna:8
- `0001437749-26-024731:8k_2_02:48` — forward-looking bullet (contract manufacturers); same list as mdna:8
- `0001437749-26-024731:8k_2_02:49` — forward-looking bullet (trade policies); same list as mdna:8
- `0001437749-26-024731:8k_2_02:50` — forward-looking bullet (intellectual property); same list as mdna:8
- `0001437749-26-024731:8k_2_02:51` — forward-looking bullet (durable goods spending); same list as mdna:8
- `0001437749-26-024731:8k_2_02:52` — forward-looking bullet (government incentives); same list as mdna:8
- `0001437749-26-024731:8k_2_02:53` — forward-looking bullet (product liability and warranty); same list as mdna:8
- `0001437749-26-024731:8k_2_02:54` — forward-looking bullet (legal proceedings); same list as mdna:8
- `0001437749-26-024731:8k_2_02:55` — forward-looking bullet (share repurchases); same list as mdna:8
- `0001437749-26-024731:8k_2_02:56` — forward-looking bullet (laws and standards); same list as mdna:8
- `0001437749-26-024731:8k_2_02:57` — forward-looking bullet (product acceptance incl. data center); same list as mdna:8
- `0001437749-26-024731:8k_2_02:58` — forward-looking bullet (data center growth uncertainty); used in the cancellation-rights cross-document item
- `0001437749-26-024731:8k_2_02:59` — forward-looking bullet (data center contract risk); used in the cancellation-rights cross-document item
- `0001437749-26-024731:8k_2_02:60` — forward-looking bullet (demand forecasting and inventory); same list as mdna:8
- `0001437749-26-024731:8k_2_02:61` — forward-looking bullet (competition); same list as mdna:8
- `0001437749-26-024731:8k_2_02:62` — forward-looking bullet (dealer network); same list as mdna:8
- `0001437749-26-024731:8k_2_02:63` — forward-looking bullet (pricing and mix); same list as mdna:8
- `0001437749-26-024731:8k_2_02:64` — forward-looking bullet (key management); same list as mdna:8
- `0001437749-26-024731:8k_2_02:65` — forward-looking bullet (labor disputes); same list as mdna:8
- `0001437749-26-024731:8k_2_02:66` — forward-looking bullet (employee retention); same list as mdna:8
- `0001437749-26-024731:8k_2_02:67` — forward-looking bullet (manufacturing disruption); same list as mdna:8
- `0001437749-26-024731:8k_2_02:68` — forward-looking bullet (synergies); same list as mdna:8
- `0001437749-26-024731:8k_2_02:69` — forward-looking bullet (foreign sourcing); same list as mdna:8
- `0001437749-26-024731:8k_2_02:70` — forward-looking bullet (EHS compliance); same list as mdna:8
- `0001437749-26-024731:8k_2_02:71` — forward-looking bullet (sustainability scrutiny); same list as mdna:8
- `0001437749-26-024731:8k_2_02:72` — forward-looking bullet (product regulation); same list as mdna:8
- `0001437749-26-024731:8k_2_02:73` — forward-looking bullet (security breaches); same list as mdna:8
- `0001437749-26-024731:8k_2_02:74` — forward-looking bullet (geopolitical conflict); same list as mdna:8
- `0001437749-26-024731:8k_2_02:75` — forward-looking bullet (debt payments); same list as mdna:8
- `0001437749-26-024731:8k_2_02:76` — forward-looking bullet (credit facility terms); same list as mdna:8
- `0001437749-26-024731:8k_2_02:77` — forward-looking bullet (additional capital); same list as mdna:8
- `0001437749-26-024731:8k_2_02:78` — forward-looking bullet (goodwill impairment); same list as mdna:8
- `0001437749-26-024731:8k_2_02:79` — forward-looking bullet (stock price volatility); same list as mdna:8
- `0001437749-26-024731:8k_2_02:80` — forward-looking bullet (tax liabilities); same list as mdna:8
- `0001437749-26-024731:8k_2_02:81` — forward-looking boilerplate
- `0001437749-26-024731:8k_2_02:82` — page number
- `0001437749-26-024731:8k_2_02:83` — forward-looking boilerplate
- `0001437749-26-024731:8k_2_02:84` — heading
- `0001437749-26-024731:8k_2_02:85` — heading
- `0001437749-26-024731:8k_2_02:86` — core sales definition; boilerplate
- `0001437749-26-024731:8k_2_02:87` — heading
- `0001437749-26-024731:8k_2_02:88` — Adjusted EBITDA definition; used in the add-back definition item
- `0001437749-26-024731:8k_2_02:89` — heading
- `0001437749-26-024731:8k_2_02:90` — adjusted net income definition; boilerplate
- `0001437749-26-024731:8k_2_02:91` — heading
- `0001437749-26-024731:8k_2_02:92` — free cash flow definition; boilerplate
- `0001437749-26-024731:8k_2_02:93` — non-GAAP boilerplate
- `0001437749-26-024731:8k_2_02:94` — source line
- `0001437749-26-024731:8k_2_02:95` — contact heading
- `0001437749-26-024731:8k_2_02:96` — contact name
- `0001437749-26-024731:8k_2_02:97` — contact details
- `0001437749-26-024731:8k_2_02:98` — page number
- `0001437749-26-024731:8k_2_02:99` — table header
- `0001437749-26-024731:8k_2_02:100` — balance sheet; amounts only (numbers reader)
- `0001437749-26-024731:8k_2_02:101` — page number
- `0001437749-26-024731:8k_2_02:102` — table header
- `0001437749-26-024731:8k_2_02:103` — income statement; amounts only (numbers reader)
- `0001437749-26-024731:8k_2_02:104` — page number
- `0001437749-26-024731:8k_2_02:105` — table header
- `0001437749-26-024731:8k_2_02:106` — cash flow statement; amounts only (numbers reader)
- `0001437749-26-024731:8k_2_02:107` — page number
- `0001437749-26-024731:8k_2_02:108` — table header
- `0001437749-26-024731:8k_2_02:109` — segment sales table; amounts only
- `0001437749-26-024731:8k_2_02:110` — segment sales table; amounts only
- `0001437749-26-024731:8k_2_02:111` — segment adjusted EBITDA table; amounts only
- `0001437749-26-024731:8k_2_02:112` — footnote cross-reference
- `0001437749-26-024731:8k_2_02:113` — page number
- `0001437749-26-024731:8k_2_02:114` — table header
- `0001437749-26-024731:8k_2_02:115` — table header
- `0001437749-26-024731:8k_2_02:116` — Adjusted EBITDA reconciliation; amounts only
- `0001437749-26-024731:8k_2_02:117` — page number
- `0001437749-26-024731:8k_2_02:118` — table header
- `0001437749-26-024731:8k_2_02:119` — adjusted net income reconciliation; amounts only
- `0001437749-26-024731:8k_2_02:120` — footnote (1); definition
- `0001437749-26-024731:8k_2_02:121` — footnote (2); definition
- `0001437749-26-024731:8k_2_02:122` — footnote (3); definition ('Amended Credit Agreement' wording)
- `0001437749-26-024731:8k_2_02:123` — footnote (4); definition
- `0001437749-26-024731:8k_2_02:124` — page number
- `0001437749-26-024731:8k_2_02:125` — footnote intro
- `0001437749-26-024731:8k_2_02:126` — legal add-back table; same as mdna:156
- `0001437749-26-024731:8k_2_02:127` — footnote (6); definition
- `0001437749-26-024731:8k_2_02:128` — footnote (7); definition
- `0001437749-26-024731:8k_2_02:129` — footnote (8); same text as the mdna:158 item
- `0001437749-26-024731:8k_2_02:130` — table header
- `0001437749-26-024731:8k_2_02:131` — free cash flow table; amounts only
- `0001437749-26-024731:8k_2_02:132` — page number
