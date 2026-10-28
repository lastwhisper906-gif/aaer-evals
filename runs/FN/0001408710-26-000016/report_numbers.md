<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Numbers report: Fabrinet, quarterly report for the third quarter of fiscal 2026 (quarter ended March 27, 2026, filed May 5, 2026)

## What the input holds, and what it does not

- **Sections absent from the input.** My directory holds four inputs: the trend table, the numeric facts, a list of current-report item codes, and a prior-predictions note. It holds no articulation checks, no restatement traces, no fourth-quarter derivation and no earnings-release figures. Because of that:
  - there is no articulation gap to report;
  - no trace of a restated prior value is in my input;
  - no row in my input says a period rests on a different concept, so I report no tag change.
- **Restatements I looked for directly.** Among the earlier-filing facts that this filing supersedes, every one I compared repeats the same value in this filing (for example, equity at December 26, 2025 and at June 27, 2025). I found no restated prior value.
- **No earnings release.**
  - The current-report input says no current report filed on or before May 5, 2026 is on record, so the bundle has no earnings release and no item text.
  - Its own item-code list does name a current report dated May 4, 2026 with the results-of-operations and exhibits item codes. Its text is not in my input, so nothing from it can be quoted, and no comparison across documents or against expectations is possible.
  - The same list shows one late-filing notice, from 2014. It has no paragraph ids and cannot be quoted.
- **No prior flags.** The prior-predictions input says this company has no earlier run, so there are no flags or outcomes to carry forward.
- **Periods the record does not reach.** The trend table has no cells at all for the fourth quarter of fiscal 2025 (target June 27, 2025) or the fourth quarter of fiscal 2024 (target June 28, 2024).
  - The reason given for each is that no quarter ending within 20 days of that date is in the record.
  - The most common cause is a fiscal fourth quarter, which no filing reports as its own duration: the annual report states the year and the three quarterly reports state the first three quarters. Such a quarter has to be derived separately, and no derivation is in my input.
  - So every "of the 6 filled quarters" position below covers the first three quarters of fiscal 2025 and fiscal 2026 only.
- **Research and development capitalization: empty.** Every element of this block in the trend table is missing. The record tags no research and development expense and no capitalized software additions in any period. That block has no paragraph id, so it is reported here and not as an item.
- **Two ratios never filled.** The inventory reserve ratio and the warranty reserve ratio are filled in none of the thirteen periods requested. The non-GAAP gap is filled in none, because the record holds no non-GAAP measure.
- **Accruals ratio, quarterly.** It is filled in only two of the eight quarters requested: the first quarters of fiscal 2026 and of fiscal 2025.
- **How to read `expected_direction`.** It refers to the named account over the stated horizon. It is "none" wherever the input supports no expectation, which is nearly everywhere.
- **How quotes are cut.**
  - Each quote is the row and its value as printed in the input.
  - The two warranty rows are cut just before a dash that the input stores as an escape sequence.
  - A formula input inside a trend cell is described in prose under that cell's quote.

## Seen in the statements

### Trend table: the third quarter of fiscal 2026 (91 days ended March 27, 2026)

```json
{ "id": "earnings_quality_accruals_ratio_quarterly_trend_insufficient", "what_changed": "insufficient. The accruals-to-total-assets ratio for the third quarter of fiscal 2026 could not be filled. The cell's reason: operating cash flow is in the record, but not for this quarter's span. No value, no change and no position exist for this quarter. Across the eight quarters requested the ratio is filled only for the first quarters of fiscal 2026 and fiscal 2025, which does not support a quarterly trend claim. The nine-month cash-flow facts appear as a separate item below.", "account": "accruals over total assets (net income less operating cash flow, over assets)", "expected_direction": "none", "horizon": "not applicable; no quarterly value exists", "quote": "\"missing\": \"no row for operating_cash_flow in 2025-12-27..2026-03-27: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0001408710-26-000016:trends:accruals_over_total_assets:2025-12-27..2026-03-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_quarterly_trend", "what_changed": "The allowance for doubtful accounts over gross receivables is 0.0012981945093297426 at March 27, 2026. Its inputs are an allowance of 1181000.0 against receivables of 908544000.0. Change against the second quarter of fiscal 2026: -0.0003158195161532475. Change against the third quarter of fiscal 2025: -0.0006046007044201134. It is the lowest of the six filled quarters. The second quarter's value, 0.00161401402548299, was second lowest. The reserve is thinner against a larger receivables balance, which was 801671000.0 at December 26, 2025. Six points across two partial fiscal years are thin for a trend claim.", "account": "allowance for doubtful accounts relative to gross trade receivables", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:bad_debt_reserve_ratio:2025-12-27..2026-03-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_ratio_quarterly_trend", "what_changed": "Current contract liabilities over quarterly revenue is 0.04844547403303816. Its inputs are contract liabilities of 58827000.0 against revenue of 1214293000.0. Change against the second quarter of fiscal 2026: 0.03305207239051039. Change against the third quarter of fiscal 2025: 0.038208022510382134. It is the highest of the six filled quarters. The second quarter's 0.01539340164252777 was second highest. Customer advances and deferred revenue rose steeply into quarter end.", "account": "current contract liabilities (customer advances and deferred revenue) relative to revenue", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:contract_liabilities_over_revenue:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_days_inventory_quarterly_trend", "what_changed": "Days sales of inventory is 74.5031169564299. Its inputs are inventory of 875988000.0 against quarterly cost of revenue of 1069954000.0 over 91 days. Change against the second quarter of fiscal 2026: 1.4521003829767807. Change against the third quarter of fiscal 2025: 11.677294728201808. It is the second highest of the six filled quarters. The first quarter of fiscal 2026 holds the highest value, 76.26841470646602. Inventory days remain well above the year-earlier quarter.", "account": "inventory relative to cost of revenue (days)", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:days_sales_of_inventory:2025-12-27..2026-03-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend", "what_changed": "Days sales outstanding is 68.08694771360784. Its inputs are receivables of 908544000.0 against quarterly revenue of 1214293000.0 over 91 days. Change against the second quarter of fiscal 2026: 3.6921787691049417. Change against the third quarter of fiscal 2025: -0.627734225692393. It is the third lowest of the six filled quarters. The second quarter, at 64.3947689445029, was the lowest. Collection days rose against the prior quarter and sit slightly below the year-earlier quarter.", "account": "trade receivables relative to revenue (days)", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:days_sales_outstanding:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend", "what_changed": "Gross margin is 0.1188666985645145. Its inputs are revenue of 1214293000.0 and cost of revenue of 1069954000.0. Change against the second quarter of fiscal 2026: -0.0026651739595125873. Change against the third quarter of fiscal 2025: 0.0016573418205861334. It is the second lowest of the six filled quarters. The second quarter's 0.12153187252402708 was second highest. Margin slipped back sequentially while staying above the year-earlier quarter.", "account": "gross margin", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:gross_margin:2025-12-27..2026-03-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_quarterly_trend_insufficient", "what_changed": "insufficient. The inventory reserve ratio for the third quarter of fiscal 2026 could not be filled. The record holds an inventory valuation reserve element, but not at March 27, 2026. The ratio is filled in none of the thirteen periods requested, so no level, change or position exists. The nine-month inventory write-down fact appears as a separate item below.", "account": "inventory valuation reserve relative to inventory", "expected_direction": "none", "horizon": "not applicable; no value exists", "quote": "\"missing\": \"no row for inventory_reserve in 2026-03-27: us-gaap:InventoryValuationReserves is in the record, but not for this period\"", "paragraph_id": "0001408710-26-000016:trends:inventory_reserve_ratio:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend", "what_changed": "insufficient. The gap between non-GAAP and reported net income cannot be filled. The record holds only standard and entity-information facts, which carry no non-GAAP measure, and the bundle has no earnings release that could supply one. The cell is filled in no period.", "account": "non-GAAP net income against reported net income", "expected_direction": "none", "horizon": "not applicable; no value exists", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001408710-26-000016:trends:non_gaap_gap:2025-12-27..2026-03-27" }
```

```json
{ "id": "revenue_recognition_receivables_ratio_quarterly_trend", "what_changed": "Receivables over quarterly revenue is 0.7482082166330531. Its inputs are receivables of 908544000.0 against revenue of 1214293000.0. Change against the second quarter of fiscal 2026: 0.04057339306708718. Change against the third quarter of fiscal 2025: -0.006898178304312053. It is the third lowest of the six filled quarters. The second quarter's 0.707634823565966 was the lowest. The ratio rose sequentially but sits slightly below the year-earlier quarter.", "account": "trade receivables relative to revenue", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:receivables_over_revenue:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend", "what_changed": "The soft-asset share (assets less property, plant and equipment and cash, over assets) is 0.7487778520632457. Its inputs are assets of 3508986000.0, cash of 356562000.0 and property, plant and equipment of 524973000.0. Change against the second quarter of fiscal 2026: -0.012588642072772327. Change against the third quarter of fiscal 2025: 0.0012856776243399537. It is the third highest of the six filled quarters. The second quarter's 0.761366494136018 was the highest.", "account": "share of total assets other than cash and fixed assets", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"", "paragraph_id": "0001408710-26-000016:trends:soft_asset_share:2025-12-27..2026-03-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_quarterly_trend_insufficient", "what_changed": "insufficient. The warranty reserve ratio for the third quarter of fiscal 2026 could not be filled. The record tags none of the three standard warranty-accrual elements in any period. Either the company does not tag the concept, or it states it only by segment, and the record cannot tell which. The ratio is filled in no period.", "account": "product warranty accrual relative to revenue", "expected_direction": "none", "horizon": "not applicable; no value exists", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001408710-26-000016:trends:warranty_reserve_ratio:2025-12-27..2026-03-27" }
```

### Trend table: fiscal 2025 (364 days ended June 27, 2025)

```json
{ "id": "earnings_quality_accruals_ratio_annual_trend", "what_changed": "The accruals-to-total-assets ratio for fiscal 2025 is 0.001469927584346013. Its inputs are net income of 332527000.0, operating cash flow of 328365000.0 and assets of 2831432000.0. Change against fiscal 2024: 0.05148662618717969. It is the second lowest of the five filled years; fiscal 2024's -0.05001669860283368 is the lowest. In fiscal 2025 operating cash flow ran just below net income, after a year in which it ran well above. Accruals in the current fiscal year are covered by the nine-month cash-flow item below.", "account": "accruals over total assets", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:accruals_over_total_assets:2024-06-29..2025-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_annual_trend", "what_changed": "The allowance for doubtful accounts over gross receivables at June 27, 2025 is 0.0017678674309887167. Its inputs are an allowance of 1344000.0 against receivables of 758894000.0. Change against fiscal 2024: -0.0009741828954819161. It is the second lowest of the five filled years. The quarterly cell above shows the ratio lower still at March 27, 2026.", "account": "allowance for doubtful accounts relative to gross trade receivables", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:bad_debt_reserve_ratio:2024-06-29..2025-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_ratio_annual_trend", "what_changed": "Current contract liabilities over annual revenue for fiscal 2025 is 0.004230949540655222. Its inputs are contract liabilities of 14467000.0 against revenue of 3419327000.0. Change against fiscal 2024: 0.0015094476989761466. It is the highest of the five filled years. The balance has since risen to 58827000 at March 27, 2026, as the quarterly cell shows.", "account": "current contract liabilities relative to revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:contract_liabilities_over_revenue:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_days_inventory_annual_trend", "what_changed": "Days sales of inventory for fiscal 2025 is 70.35629003272811. Its inputs are inventory of 581015000.0 against annual cost of revenue of 3005978000.0 over 364 days. Change against fiscal 2024: 3.6301089273276688. It is the second lowest of the five filled years. Fiscal 2023's 83.48449607702848 was third highest.", "account": "inventory relative to cost of revenue (days)", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:days_sales_of_inventory:2024-06-29..2025-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend", "what_changed": "Days sales outstanding for fiscal 2025 is 80.7870718419151. Its inputs are receivables of 758894000.0 against annual revenue of 3419327000.0 over 364 days. Change against fiscal 2024: 5.984783782426376. It is the highest of the five filled years. The annual and quarterly measures use different day counts and revenue spans, so they are not set against each other here.", "account": "trade receivables relative to revenue (days)", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:days_sales_outstanding:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend", "what_changed": "Gross margin for fiscal 2025 is 0.1208860691007324. Its inputs are revenue of 3419327000.0 and cost of revenue of 3005978000.0. Change against fiscal 2024: -0.0026387579264239985. It is the second lowest of the five filled years. Fiscal 2023's 0.12712395902522156 is the highest.", "account": "gross margin", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:gross_margin:2024-06-29..2025-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_annual_trend_insufficient", "what_changed": "insufficient. The inventory reserve ratio for fiscal 2025 could not be filled. The record holds an inventory valuation reserve element, but not at June 27, 2025. The ratio is filled in none of the five years.", "account": "inventory valuation reserve relative to inventory", "expected_direction": "none", "horizon": "not applicable; no value exists", "quote": "\"missing\": \"no row for inventory_reserve in 2025-06-27: us-gaap:InventoryValuationReserves is in the record, but not for this period\"", "paragraph_id": "0001408710-26-000016:trends:inventory_reserve_ratio:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend_insufficient", "what_changed": "insufficient. No non-GAAP measure exists in the record for fiscal 2025 or any other year, so the gap between non-GAAP and reported earnings cannot be filled.", "account": "non-GAAP net income against reported net income", "expected_direction": "none", "horizon": "not applicable; no value exists", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001408710-26-000016:trends:non_gaap_gap:2024-06-29..2025-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_ratio_annual_trend", "what_changed": "Receivables over annual revenue for fiscal 2025 is 0.2219425050602063. Its inputs are receivables of 758894000.0 against revenue of 3419327000.0. Change against fiscal 2024: 0.016441713687984555. It is the highest of the five filled years. Fiscal 2023's 0.20102811203684207 was third highest.", "account": "trade receivables relative to revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:receivables_over_revenue:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend", "what_changed": "The soft-asset share at June 27, 2025 is 0.7573436338926733. Its inputs are assets of 2831432000.0, cash of 306425000.0 and property, plant and equipment of 380640000.0. Change against fiscal 2024: 0.06403902529210181. It is the highest of the five filled years.", "account": "share of total assets other than cash and fixed assets", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001408710-26-000016:trends:soft_asset_share:2024-06-29..2025-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_annual_trend_insufficient", "what_changed": "insufficient. The warranty reserve ratio for fiscal 2025 could not be filled. None of the three standard warranty-accrual elements is tagged in any period, and the record cannot tell whether the concept is untagged or stated only by segment.", "account": "product warranty accrual relative to revenue", "expected_direction": "none", "horizon": "not applicable; no value exists", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001408710-26-000016:trends:warranty_reserve_ratio:2024-06-29..2025-06-27" }
```

### Numeric facts: income statement

```json
{ "id": "revenue_recognition_quarterly_revenue_fact", "what_changed": "Revenue for the third quarter of fiscal 2026 is 1214293000, against 871799000 in the third quarter of fiscal 2025. Nine-month revenue is 3325309000, against 2509635000. The second-quarter report on record showed 1132888000.", "account": "revenue", "expected_direction": "none", "horizon": "fourth quarter of fiscal 2026, as stated in the fiscal 2026 annual report", "quote": "\"value\": \"1214293000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_operating_income_fact", "what_changed": "Operating income for the quarter is 120044000, against 78856000 a year earlier. Nine-month operating income is 328638000, against 235391000. Gross profit is 144339000 against 102183000 for the quarter, and 398460000 against 302058000 for nine months.", "account": "operating income", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"120044000\"", "paragraph_id": "0001408710-26-000016:facts:OperatingIncomeLoss:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_diluted_earnings_per_share_fact", "what_changed": "Diluted earnings per share for the quarter is 3.45, against 2.25 a year earlier; basic is 3.49 against 2.26. Net income is 125213000 against 81290000. Nine-month diluted earnings per share is 9.22 against 6.75. Diluted weighted shares are 36301000 against 36172000.", "account": "net income and diluted earnings per share", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"3.45\"", "paragraph_id": "0001408710-26-000016:facts:EarningsPerShareDiluted:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_selling_general_administrative_fact", "what_changed": "Selling, general and administrative expense for the quarter is 24295000, against 22063000 a year earlier. The nine-month figure is 69822000 against 65300000.", "account": "selling, general and administrative expense", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"24295000\"", "paragraph_id": "0001408710-26-000016:facts:SellingGeneralAndAdministrativeExpense:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_restructuring_charges_absent_fact", "what_changed": "Restructuring charges are 0 in the third quarter of fiscal 2026, against 1264000 a year earlier. The nine-month figure is 0 against 1367000. The restructuring reserve at March 27, 2026 is 0. Severance costs still appear in the cash-flow reconciliation (see the severance item).", "account": "restructuring charges", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0\"", "paragraph_id": "0001408710-26-000016:facts:RestructuringCharges:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_interest_and_other_income_fact", "what_changed": "Interest and other income for the quarter is 7421000, against 10145000 a year earlier. The nine-month figure is 25393000 against 32392000. Non-operating interest income is lower while operating income is higher.", "account": "interest and other income", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"7421000\"", "paragraph_id": "0001408710-26-000016:facts:InterestAndOtherIncome:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_foreign_currency_gain_fact", "what_changed": "The foreign currency transaction line is a gain of 6989000 in the quarter, against a loss of -2675000 a year earlier. Over nine months it is 1715000 against -5728000. Other non-operating expense is -212000 against -30000. Pretax income is 134242000 against 86296000, so a currency swing from loss to gain sits inside the pretax increase. At the same time, hedges recorded losses in other comprehensive income (see the hedge items).", "account": "foreign currency transaction gain or loss", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"6989000\"", "paragraph_id": "0001408710-26-000016:facts:ForeignCurrencyTransactionGainLossBeforeTax:2025-12-27..2026-03-27" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_fact", "what_changed": "The effective tax rate for the quarter is 0.067, against 0.058 a year earlier. Over nine months it is 0.061 against 0.063. Income tax expense is 9029000 against 5006000 for the quarter, and 21628000 against 16624000 for nine months. The second-quarter report on record showed 0.059 against 0.087.", "account": "effective income tax rate", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0.067\"", "paragraph_id": "0001408710-26-000016:facts:EffectiveIncomeTaxRateContinuingOperations:2025-12-27..2026-03-27" }
```

```json
{ "id": "estimates_and_discretion_uncertain_tax_interest_penalties_fact", "what_changed": "Accrued interest and penalties on unrecognized tax benefits are 4400000 at March 27, 2026, against 2200000 at June 27, 2025.", "account": "accrued interest and penalties on unrecognized tax benefits", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"4400000\"", "paragraph_id": "0001408710-26-000016:facts:UnrecognizedTaxBenefitsIncomeTaxPenaltiesAndInterestAccrued:2026-03-27" }
```

```json
{ "id": "earnings_quality_comprehensive_income_below_net_income_fact", "what_changed": "Comprehensive income for the quarter is 110273000, against net income of 125213000. A year earlier, comprehensive income was 87490000 against net income of 81290000. Nine-month comprehensive income is 322972000 against net income of 333767000. Other comprehensive income turned negative, driven by the cash-flow hedge items below.", "account": "comprehensive income", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"110273000\"", "paragraph_id": "0001408710-26-000016:facts:ComprehensiveIncomeNetOfTax:2025-12-27..2026-03-27" }
```

### Numeric facts: cash flow and working capital (nine months ended March 27, 2026, against nine months ended March 28, 2025)

```json
{ "id": "earnings_quality_operating_cash_flow_below_net_income", "what_changed": "Nine-month operating cash flow is 201758000, against 273272000 a year earlier. Nine-month net income is 333767000, against 245320000. Operating cash flow is below net income and lower than a year earlier, while net income is higher. The working-capital items below are what absorbed the difference. Quarterly operating cash flow is not in the record (see the quarterly accruals item).", "account": "net cash provided by operating activities", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"201758000\"", "paragraph_id": "0001408710-26-000016:facts:NetCashProvidedByUsedInOperatingActivities:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_inventory_cash_outflow_fact", "what_changed": "The increase in inventories in the nine-month cash-flow statement is 297362000, against 68132000 a year earlier. Balance-sheet inventory is 875988000 at March 27, 2026, against 581015000 at June 27, 2025.", "account": "inventories (cash-flow change)", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"297362000\"", "paragraph_id": "0001408710-26-000016:facts:IncreaseDecreaseInInventories:2025-06-28..2026-03-27" }
```

```json
{ "id": "revenue_recognition_receivables_cash_outflow_fact", "what_changed": "The increase in accounts receivable in the nine-month cash-flow statement is 150082000, against 65271000 a year earlier. Receivables are 908544000 at March 27, 2026, against 758894000 at June 27, 2025.", "account": "accounts receivable (cash-flow change)", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"150082000\"", "paragraph_id": "0001408710-26-000016:facts:IncreaseDecreaseInAccountsReceivable:2025-06-28..2026-03-27" }
```

```json
{ "id": "earnings_quality_other_operating_assets_build_fact", "what_changed": "The increase in other operating assets over nine months is 77518000, against 2357000 a year earlier. Other current assets on the balance sheet are 177476000 at March 27, 2026, against 116210000 at June 27, 2025.", "account": "other operating assets", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"77518000\"", "paragraph_id": "0001408710-26-000016:facts:IncreaseDecreaseInOtherOperatingAssets:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_trade_payables_inflow_fact", "what_changed": "The increase in trade accounts payable over nine months is 225741000, against 79196000 a year earlier. Accounts payable on the balance sheet are 859004000 at March 27, 2026, against 637417000 at June 27, 2025. Supplier credit funded part of the inventory build.", "account": "trade accounts payable (cash-flow change)", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"225741000\"", "paragraph_id": "0001408710-26-000016:facts:IncreaseDecreaseInAccountsPayableTrade:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_other_payables_inflow_fact", "what_changed": "The change in other accounts payable over nine months is 91155000, against -152000 a year earlier. Other current liabilities on the balance sheet are 152915000 at March 27, 2026, against 66717000 at June 27, 2025.", "account": "other accounts payable (cash-flow change)", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"91155000\"", "paragraph_id": "0001408710-26-000016:facts:IncreaseDecreaseInOtherAccountsPayable:2025-06-28..2026-03-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_fact", "what_changed": "Inventory write-downs over nine months are 2389000, against 0 a year earlier. This is the only inventory-reserve signal in the input, because the inventory reserve ratio is never filled.", "account": "inventory write-down", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"2389000\"", "paragraph_id": "0001408710-26-000016:facts:InventoryWriteDown:2025-06-28..2026-03-27" }
```

```json
{ "id": "earnings_quality_severance_costs_fact", "what_changed": "Severance costs in the nine-month cash-flow reconciliation are 2663000, against 2131000 a year earlier. Restructuring charges on the income statement are 0 for the same nine months.", "account": "severance costs", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"2663000\"", "paragraph_id": "0001408710-26-000016:facts:SeveranceCosts1:2025-06-28..2026-03-27" }
```

```json
{ "id": "earnings_quality_share_based_compensation_fact", "what_changed": "Share-based compensation for the quarter is 8541000, against 7783000 a year earlier. The nine-month figure is 26369000 against 24903000. The recognized tax benefit is 0 in every period shown, and no compensation cost was capitalized.", "account": "share-based compensation", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"8541000\"", "paragraph_id": "0001408710-26-000016:facts:ShareBasedCompensation:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_depreciation_and_amortization_fact", "what_changed": "Depreciation and amortization over nine months is 48761000, against 39223000 a year earlier.", "account": "depreciation and amortization", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"48761000\"", "paragraph_id": "0001408710-26-000016:facts:DepreciationAndAmortization:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_capital_spending_fact", "what_changed": "Cash paid for property, plant and equipment over nine months is 160634000, against 70668000 a year earlier. Net property, plant and equipment is 524973000 at March 27, 2026, against 380640000 at June 27, 2025. Net cash used in investing is -119817000 against -253126000.", "account": "capital expenditures", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"160634000\"", "paragraph_id": "0001408710-26-000016:facts:PaymentsToAcquirePropertyPlantAndEquipment:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_unpaid_capital_spending_fact", "what_changed": "Capital expenditures incurred but not yet paid over nine months are 65307000, against 33101000 a year earlier.", "account": "capital expenditures incurred but not yet paid", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"65307000\"", "paragraph_id": "0001408710-26-000016:facts:CapitalExpendituresIncurredButNotYetPaid:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_thailand_long_lived_assets_fact", "what_changed": "Non-current assets located in Thailand are 475028000 at March 27, 2026, against 338127000 at June 27, 2025. Total non-current assets are 529407000 against 386408000.", "account": "non-current assets in Thailand", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"475028000\"", "paragraph_id": "0001408710-26-000016:facts:NoncurrentAssets:2026-03-27:srt:StatementGeographicalAxis=country:TH" }
```

### Numeric facts: liquidity, capital returns and financing

```json
{ "id": "liquidity_and_capital_cash_balance_fact", "what_changed": "Cash and cash equivalents are 356562000 at March 27, 2026, against 306425000 at June 27, 2025. Cash including restricted cash is 357256000; non-current restricted cash is 694000, against 0 at March 28, 2025.", "account": "cash and cash equivalents", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"356562000\"", "paragraph_id": "0001408710-26-000016:facts:CashAndCashEquivalentsAtCarryingValue:2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_short_term_investments_fact", "what_changed": "Short-term investments are 588674000 at March 27, 2026, against 627819000 at June 27, 2025. Purchases of short-term investments over nine months are 241255000, against 304189000.", "account": "short-term investments", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"588674000\"", "paragraph_id": "0001408710-26-000016:facts:ShortTermInvestments:2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_fact", "what_changed": "Cash paid for share repurchases over nine months is 5231000, against 103475000 a year earlier. Treasury shares acquired over nine months are 13766, at an average cost of 379.99. Net cash used in financing is -29619000, against -124393000.", "account": "share repurchases", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"5231000\"", "paragraph_id": "0001408710-26-000016:facts:PaymentsForRepurchaseOfCommonStock:2025-06-28..2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_remaining_repurchase_authorization_fact", "what_changed": "The remaining repurchase authorization is 169000000.0 at March 27, 2026. The second-quarter report on record showed 169200000.", "account": "remaining share repurchase authorization", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"169000000.0\"", "paragraph_id": "0001408710-26-000016:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-03-27" }
```

```json
{ "id": "liquidity_and_capital_credit_facility_undrawn_fact", "what_changed": "Borrowings outstanding under the credit facility agreement are 0 at March 27, 2026. The facility's stated maximum borrowing capacity appears as 55000000.0 at March 9, 2023 and 30000000.0 at December 27, 2024.", "account": "borrowings under the revolving credit facility", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0\"", "paragraph_id": "0001408710-26-000016:facts:LongTermDebt:2026-03-27:us-gaap:DebtInstrumentAxis=fn:A2023CreditFacilityAgreementMember,us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember" }
```

```json
{ "id": "liquidity_and_capital_warrants_outstanding_fact", "what_changed": "Warrants outstanding are 70662 at March 27, 2026, against 38192 at June 27, 2025. The second-quarter report on record showed 49652 at December 26, 2025. The warrants were issued on March 12, 2025 for 381922 shares at an exercise price of 208.48.", "account": "warrants outstanding", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"70662\"", "paragraph_id": "0001408710-26-000016:facts:ClassOfWarrantOrRightOutstanding:2026-03-27" }
```

```json
{ "id": "earnings_quality_warrant_dilution_shares_fact", "what_changed": "Incremental diluted shares from options and warrants for the quarter are 224000, against 15000 a year earlier. The nine-month figure is 188000 against 5000.", "account": "dilutive shares from warrants", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"224000\"", "paragraph_id": "0001408710-26-000016:facts:IncrementalCommonSharesAttributableToCallOptionsAndWarrants:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_warrant_paid_in_capital_entry_fact", "what_changed": "The adjustment to additional paid-in capital for warrants is 2000000.0 in the quarter, against 3900000 a year earlier. The nine-month figure is 3200000 against 3900000. The numeric input does not say which income-statement line carries the offset.", "account": "paid-in capital recorded for warrants", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"2000000.0\"", "paragraph_id": "0001408710-26-000016:facts:AdjustmentsToAdditionalPaidInCapitalWarrantIssued:2025-12-27..2026-03-27" }
```

### Numeric facts: contract liabilities, inventory composition and commitments

```json
{ "id": "revenue_recognition_contract_liabilities_balance_fact", "what_changed": "Current contract liabilities are 58827000 at March 27, 2026. Earlier balances: 14467000 at June 27, 2025, 8925000 at March 28, 2025 and 7846000 at June 28, 2024. The second-quarter report showed 17439000 at December 26, 2025, the trend input for that quarter.", "account": "current contract liabilities", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"value\": \"58827000\"", "paragraph_id": "0001408710-26-000016:facts:ContractWithCustomerLiabilityCurrent:2026-03-27" }
```

```json
{ "id": "earnings_quality_work_in_process_inventory_fact", "what_changed": "Work-in-process inventory is 544218000 at March 27, 2026, against 377736000 at June 27, 2025. It is the largest inventory component.", "account": "work-in-process inventory", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"544218000\"", "paragraph_id": "0001408710-26-000016:facts:InventoryWorkInProcess:2026-03-27" }
```

```json
{ "id": "earnings_quality_raw_materials_inventory_fact", "what_changed": "Raw materials inventory is 240422000 at March 27, 2026, against 145128000 at June 27, 2025.", "account": "raw materials inventory", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"240422000\"", "paragraph_id": "0001408710-26-000016:facts:InventoryRawMaterials:2026-03-27" }
```

```json
{ "id": "earnings_quality_inventory_in_transit_fact", "what_changed": "Inventory in transit is 55975000 at March 27, 2026, against 25135000 at June 27, 2025. Finished goods are 35373000 against 33016000.", "account": "inventory in transit and finished goods", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"55975000\"", "paragraph_id": "0001408710-26-000016:facts:OtherInventoryInTransit:2026-03-27" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_inventory_purchase_obligation", "what_changed": "Unrecorded purchase obligations for inventories are 2740000000 at March 27, 2026. The second-quarter report on record showed 1940000000 at December 26, 2025. The obligation is large next to the inventory balance of 875988000.", "account": "inventory purchase obligations", "expected_direction": "none", "horizon": "next quarterly report and the fiscal 2026 annual report", "quote": "\"value\": \"2740000000\"", "paragraph_id": "0001408710-26-000016:facts:PurchaseObligation:2026-03-27:us-gaap:UnrecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:InventoriesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_thailand_purchase_obligation", "what_changed": "A purchase obligation located in Thailand is 164700000 at March 27, 2026. A separate obligation of 132500000 (4450000000 Thai baht) is stated as of February 28, 2025. The numeric input does not name what is being purchased.", "account": "purchase obligations in Thailand", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"164700000\"", "paragraph_id": "0001408710-26-000016:facts:PurchaseObligation:2026-03-27:srt:StatementGeographicalAxis=country:TH" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_thailand_bank_guarantee", "what_changed": "Current guarantee obligations in Thailand are 2300000 at both March 27, 2026 and June 27, 2025 (77300000 against 75700000 Thai baht). In China the guarantee is 700000 (4800000 yuan), backed by 700000 of collateral.", "account": "bank guarantees", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"2300000\"", "paragraph_id": "0001408710-26-000016:facts:GuaranteeObligationsCurrentCarryingValue:2026-03-27:srt:StatementGeographicalAxis=country:TH" }
```

### Numeric facts: currency hedges and other comprehensive income

```json
{ "id": "estimates_and_discretion_derivative_liability_fact", "what_changed": "Derivative liabilities at fair value are 10835000 at March 27, 2026, against 105000 at June 27, 2025. Derivative assets are 0 against 2961000. Of the liability, 8823000 sits in designated hedges (against 93000) and 2012000 in contracts not designated as hedges (against 12000).", "account": "foreign currency derivative liabilities", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"10835000\"", "paragraph_id": "0001408710-26-000016:facts:DerivativeFairValueOfDerivativeLiability:2026-03-27" }
```

```json
{ "id": "earnings_quality_cash_flow_hedge_loss_fact", "what_changed": "The cash-flow hedge result recorded in other comprehensive income before reclassification is -16187000 for the quarter, against 1505000 a year earlier. The nine-month figure is -13678000 against 1448000. Amounts reclassified out of other comprehensive income in the quarter total -2990000: 3399000 through cost of sales, 257000 through selling, general and administrative expense, and -6646000 through the foreign currency line.", "account": "cash-flow hedge gains and losses in other comprehensive income", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"-16187000\"", "paragraph_id": "0001408710-26-000016:facts:OtherComprehensiveIncomeLossCashFlowHedgeGainLossBeforeReclassificationAfterTax:2025-12-27..2026-03-27" }
```

```json
{ "id": "earnings_quality_hedge_reclassification_estimate_fact", "what_changed": "The estimated net amount of hedge gain or loss to be moved from accumulated other comprehensive income into earnings is -8900000, stated with the nine months ended March 27, 2026. For fiscal 2025 the figure was 1500000. The filer's own estimate turned from a gain to a loss to be recognized in earnings.", "account": "hedge losses to be reclassified into earnings", "expected_direction": "down", "horizon": "the period the filer's estimate covers, beginning after March 27, 2026 (span not stated in the numeric input)", "quote": "\"value\": \"-8900000\"", "paragraph_id": "0001408710-26-000016:facts:DerivativeInstrumentsGainLossReclassificationFromAccumulatedOCIToIncomeEstimatedNetAmountToBeTransferred:2025-06-28..2026-03-27:us-gaap:DerivativeInstrumentRiskAxis=us-gaap:ForeignExchangeForwardMember" }
```

```json
{ "id": "earnings_quality_accumulated_hedge_balance_fact", "what_changed": "The cash-flow hedge component of accumulated other comprehensive income is -8048000 at March 27, 2026. It was 1334000 at June 27, 2025, -73000 at March 28, 2025 and -980000 at June 28, 2024.", "account": "accumulated cash-flow hedge gains and losses", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"-8048000\"", "paragraph_id": "0001408710-26-000016:facts:StockholdersEquity:2026-03-27:us-gaap:StatementEquityComponentsAxis=us-gaap:AccumulatedGainLossNetCashFlowHedgeParentMember" }
```

```json
{ "id": "earnings_quality_accumulated_other_comprehensive_income_fact", "what_changed": "Accumulated other comprehensive income is -501000 at March 27, 2026, against 10294000 at June 27, 2025. The unrealized investment gain component is 7389000 against 8714000, and the translation component is 158000 against 246000.", "account": "accumulated other comprehensive income", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"-501000\"", "paragraph_id": "0001408710-26-000016:facts:StockholdersEquity:2026-03-27:us-gaap:StatementEquityComponentsAxis=us-gaap:AccumulatedOtherComprehensiveIncomeMember" }
```

```json
{ "id": "liquidity_and_capital_baht_hedge_notional_fact", "what_changed": "The notional amount of designated Thai baht forward contracts is 253000000.0 across 253 contracts at March 27, 2026, against 165000000.0 across 165 contracts at June 27, 2025. One Canadian dollar contract (400000 Canadian dollars) is outstanding, against one of 500000.", "account": "foreign currency forward contract notional", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"253000000.0\"", "paragraph_id": "0001408710-26-000016:facts:DerivativeNotionalAmount:2026-03-27:srt:CurrencyAxis=currency:THB,us-gaap:DerivativeInstrumentRiskAxis=us-gaap:ForeignExchangeForwardMember,us-gaap:HedgingDesignationAxis=us-gaap:DesignatedAsHedgingInstrumentMember" }
```

### Numeric facts: revenue mix, geography and customers

```json
{ "id": "revenue_recognition_optical_share_of_revenue_fact", "what_changed": "Optical communications is 0.732 of revenue in the quarter, against 0.754 a year earlier, and 0.742 against 0.769 over nine months. Non-optical communications is 0.268 against 0.246. Optical revenue is 888704000 against 657231000; non-optical revenue is 325589000 against 214568000.", "account": "revenue mix: optical against non-optical communications", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0.732\"", "paragraph_id": "0001408710-26-000016:facts:ConcentrationRiskPercentage1:2025-12-27..2026-03-27:srt:ProductOrServiceAxis=fn:OpticalCommunicationsMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:ProductConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_telecom_revenue_fact", "what_changed": "Telecom revenue (optical) is 431366000 in the quarter, against 302736000 a year earlier. The second-quarter report on record showed 412248000. The nine-month figure is 1179334000 against 776373000.", "account": "telecom end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"431366000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:TelecomMember,srt:ProductOrServiceAxis=fn:OpticalCommunicationsMember" }
```

```json
{ "id": "revenue_recognition_datacom_revenue_fact", "what_changed": "Datacom revenue (optical) is 260442000 in the quarter, against 251105000 a year earlier. The second-quarter report on record showed 278142000, so datacom is lower sequentially. The nine-month figure is 811680000, against 879087000 a year earlier.", "account": "datacom end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"260442000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:DatacomMember,srt:ProductOrServiceAxis=fn:OpticalCommunicationsMember" }
```

```json
{ "id": "revenue_recognition_datacenter_interconnect_revenue_fact", "what_changed": "Datacenter interconnect revenue (optical) is 196896000 in the quarter, against 103390000 a year earlier. The second-quarter report on record showed 142200000. The nine-month figure is 477176000 against 275236000.", "account": "datacenter interconnect end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"196896000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:DatacenterInterconnectMember,srt:ProductOrServiceAxis=fn:OpticalCommunicationsMember" }
```

```json
{ "id": "revenue_recognition_automotive_revenue_fact", "what_changed": "Automotive revenue (non-optical) is 115499000 in the quarter, against 129468000 a year earlier. The nine-month figure is 354403000 against 336456000. This is the one end market lower than the year-earlier quarter.", "account": "automotive end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"115499000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:AutomotiveMember,srt:ProductOrServiceAxis=fn:NonOpticalCommunicationsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_high_performance_computing_category", "what_changed": "A high-performance computing end market (non-optical) carries 106746000 in the quarter and 207705000 over nine months. The year-earlier quarter and nine-month columns in this filing hold no such row: their non-optical rows are automotive, industrial laser and others only. This is a new disaggregation category, so year-over-year comparison of the non-optical sub-markets is affected.", "account": "high-performance computing end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"106746000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:HighPerformanceComputingMember,srt:ProductOrServiceAxis=fn:NonOpticalCommunicationsMember" }
```

```json
{ "id": "revenue_recognition_industrial_laser_revenue_fact", "what_changed": "Industrial laser revenue (non-optical) is 44171000 in the quarter, against 40464000 a year earlier. The nine-month figure is 125282000 against 113332000.", "account": "industrial laser end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"44171000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:IndustrialLaserMember,srt:ProductOrServiceAxis=fn:NonOpticalCommunicationsMember" }
```

```json
{ "id": "revenue_recognition_other_non_optical_revenue_fact", "what_changed": "Other non-optical revenue is 59173000 in the quarter, against 44636000 a year earlier. The nine-month figure is 169729000 against 129151000. Because a high-performance computing row is new this year, the year-earlier 'others' row may not cover the same customers.", "account": "other non-optical end-market revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"59173000\"", "paragraph_id": "0001408710-26-000016:facts:Revenues:2025-12-27..2026-03-27:fn:ContractWithCustomerMarketCategoryAxis=fn:OthersMember,srt:ProductOrServiceAxis=fn:NonOpticalCommunicationsMember" }
```

```json
{ "id": "revenue_recognition_north_america_share_fact", "what_changed": "North America is 0.521 of revenue in the quarter, against 0.462 a year earlier. Asia-Pacific is 0.374 against 0.459, and Europe is 0.105 against 0.079.", "account": "geographic revenue concentration", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0.521\"", "paragraph_id": "0001408710-26-000016:facts:ConcentrationRiskPercentage1:2025-12-27..2026-03-27:srt:StatementGeographicalAxis=srt:NorthAmericaMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:GeographicConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_united_states_revenue_fact", "what_changed": "Revenue attributed to the United States is 630218000 in the quarter, against 401769000 a year earlier. Revenue attributed to Israel is 211394000, against 226406000.", "account": "revenue by country", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"630218000\"", "paragraph_id": "0001408710-26-000016:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2025-12-27..2026-03-27:srt:StatementGeographicalAxis=country:US" }
```

```json
{ "id": "structure_and_disclosure_changes_four_customer_revenue_concentration", "what_changed": "The customer-concentration row for nine-month revenue now names four customers at the 0.10 threshold. The year-earlier nine-month row in this filing names two. The second-quarter report on record named three for six months. More customers now cross the ten-percent level.", "account": "customer concentration of revenue", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0.10\"", "paragraph_id": "0001408710-26-000016:facts:ConcentrationRiskPercentage1:2025-06-28..2026-03-27:srt:MajorCustomersAxis=fn:FourCustomersMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "structure_and_disclosure_changes_three_customer_receivables_concentration", "what_changed": "The customer-concentration row for trade receivables at the nine-month mark names three customers at the 0.10 threshold, the same as for fiscal 2025. The second-quarter report on record named two.", "account": "customer concentration of trade receivables", "expected_direction": "none", "horizon": "fiscal 2026 annual report", "quote": "\"value\": \"0.10\"", "paragraph_id": "0001408710-26-000016:facts:ConcentrationRiskPercentage1:2025-06-28..2026-03-27:srt:MajorCustomersAxis=fn:ThreeCustomersMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:TradeAccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

### Numeric facts: subsequent event

```json
{ "id": "related_parties_contingencies_and_subsequent_events_raytek_stake", "what_changed": "As a subsequent event dated March 28, 2026, the filing records a voting interest of 0.160 in Raytek Semiconductor, Inc.", "account": "equity investment acquired after quarter end", "expected_direction": "none", "horizon": "fourth quarter of fiscal 2026, as stated in the fiscal 2026 annual report", "quote": "\"value\": \"0.160\"", "paragraph_id": "0001408710-26-000016:facts:BusinessAcquisitionPercentageOfVotingInterestsAcquired:2026-03-28:us-gaap:BusinessAcquisitionAxis=fn:RaytekSemiconductorInc.Member,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_raytek_consideration", "what_changed": "Consideration for the Raytek Semiconductor stake is 32400000 (1020000000.00 New Taiwan dollars), dated March 28, 2026, after the quarter closed.", "account": "cash consideration for the investment", "expected_direction": "none", "horizon": "fourth quarter of fiscal 2026, as stated in the fiscal 2026 annual report", "quote": "\"value\": \"32400000\"", "paragraph_id": "0001408710-26-000016:facts:BusinessCombinationConsiderationTransferred1:2026-03-28..2026-03-28:us-gaap:BusinessAcquisitionAxis=fn:RaytekSemiconductorInc.Member,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

## Seen in the notes

No fact in my numeric input is marked as having sat inside a note. Every fact carries these fields and no others:

- id
- paragraph id
- tag
- prefix
- namespace
- context
- context reference
- unit
- decimals
- value
- number
- nil flag
- form
- source accession
- filing date
- on some earlier-filing facts, a superseded-by accession

With no marker to read, I place no item under this heading. Several facts above are of kinds that filers usually present in note tables:

- inventory components
- derivatives and hedges
- purchase obligations and guarantees
- revenue disaggregation and concentrations
- share-based pay and warrants
- the subsequent event

The input does not mark any of them, so they stay under "Seen in the statements". A later split cannot rely on this report to tell them apart.
