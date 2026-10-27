<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Seen in the statements

Periods the record does not reach (no cells, nothing to quote): quarters-back-2 (target 2025-12-30) and quarters-back-6 (target 2024-12-31). The reason each gives: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py" (the same text with 2024-12-31 for quarters-back-6). The fourth-quarter derivation itself is not in my directory, so no fourth-quarter value exists for me.

Inputs my instructions name that are not in my directory: the articulation checks, the restatement traces and the fourth-quarter derivation. Without articulation checks I have no articulation gap to report, and I do not compute one. Without restatement traces I have only the facts file. In it, every row marked superseded_by that I compared carries the same value as the later filing's row, so I report no restated prior value. I found one place where the same period rests on a different concept: current deferred revenue at 2025-12-31. It is reported as an item below. That an input is absent is a fact about my directory, not a finding that nothing of that kind exists.

The trend table's research-and-development capitalisation baseline for years-back-0 prints no paragraph_id, so I cannot quote it as an item. Its printed values are: book_value_with_rnd_capitalized 3284520000.0, earnings_with_rnd_capitalized 2147180000.0, research_and_development_asset 2047020000.0 and research_and_development_amortization 521720000.0. capitalized_development_cost and capitalized_over_expense are missing, with the reason "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period." That makes them insufficient.

Notes placement: the facts in my input carry no field saying whether their element sat inside a note. I placed a fact under "Seen in the notes" when its element or dimension is a note disclosure, for example concentration, disaggregation, remaining performance obligations, inventory components, PP&E classes, debt, commitments, contingencies, stock compensation, repurchase programme, tax or segment. That placement is my reading of the element, not a marker.

Other contents of my input, reported for whoever checks this run:
- The facts file includes the 10-K cover-page fact EntityPublicFloat (an aggregate market value at 2025-06-30, as the company printed it). The equity-award and repurchase notes carry per-share fair values, exercise prices and an average repurchase cost.
- These are figures inside the filings, not a price series, a return or an outcome window. I did not use them.
- The 8-K file lists the company's 8-K item codes and states "none on or before 2026-07-30" for late-filing notifications. Those lines print no paragraph_id, so neither is an item.
- input_prior_predictions.md says no earlier run is on record.

expected_direction:
- Trend items: the sign of the printed change(s). It is "none" where the quarter-over-quarter and year-over-year changes disagree in sign, or where the item is insufficient.
- Release rows and filed facts: the direction the quoted figure moved from its printed comparative. For a cash-flow adjustment line it follows the size of the printed amount, not its sign. It is "none" where the figures are equal, where printed comparisons disagree, or where no comparative exists in my input.
- Guidance items: which side of the latest printed actual the range sits on.

It is a reading of my inputs, not a forecast.

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly_insufficient",
  "what_changed": "insufficient — accruals_over_total_assets is not filled in quarters-back-0 (2026-04-01..2026-06-30): the record holds no three-month operating cash flow row for the quarter, so no value, no quarter-over-quarter change and no year-over-year change exist",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "none — no value exists for the quarter",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly_insufficient",
  "what_changed": "insufficient — bad_debt_reserve_ratio is not filled in quarters-back-0: the record holds no allowance row at 2026-06-30, so no value and no change exist",
  "account": "allowance for doubtful accounts over gross receivables",
  "expected_direction": "none",
  "horizon": "none — no value exists for the quarter",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_quarterly",
  "what_changed": "value 1.8759705063723815 (ContractWithCustomerLiabilityCurrent 3841800000.0 over quarterly revenue 2047900000.0); quarter_over_quarter change -0.13868131023661512 against quarters-back-1 (2.0146518166089966); year_over_year change -0.21758777583620725 against quarters-back-4 (2.0935582822085887)",
  "account": "current contract liabilities over quarterly revenue",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_quarterly",
  "what_changed": "value 95.85693106004447 days (InventoryNet 426300000.0, CostOfGoodsAndServicesSold 404700000.0, 91 days); quarter_over_quarter change 4.597671800785221 against quarters-back-1 (91.25925925925925, lowest of the 6 filled quarters); year_over_year change -21.238019717980308 against quarters-back-4 (117.09495077802478)",
  "account": "days sales of inventory",
  "expected_direction": "none",
  "horizon": "next quarterly filing — the two printed changes disagree in sign",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_quarterly",
  "what_changed": "value 64.68069729967284 days (AccountsReceivableNetCurrent 1455600000.0 over quarterly revenue 2047900000.0, 91 days); quarter_over_quarter change -7.636560485794277 against quarters-back-1 (72.31725778546712, highest of the 6 filled quarters); year_over_year change -3.1896707984866595 against quarters-back-4 (67.8703680981595)",
  "account": "days sales outstanding",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_quarterly",
  "what_changed": "value 0.8023829288539479 (revenue 2047900000.0, cost of revenue 404700000.0); quarter_over_quarter change -0.0005474344678514376 against quarters-back-1 (0.8029303633217993); year_over_year change -0.004426887096972365 against quarters-back-4 (0.8068098159509203)",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_quarterly",
  "what_changed": "value 0.2880600516068496 (InventoryValuationReserves 122800000.0 over InventoryNet 426300000.0); quarter_over_quarter change -0.05095509990830188 against quarters-back-1 (0.3390151515151515, inputs reserve 125300000.0 and inventory 369600000.0); year_over_year change -0.07324300861032712 against quarters-back-4 (0.36130306021717673)",
  "account": "inventory valuation reserve over net inventory",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_quarterly_insufficient",
  "what_changed": "insufficient — non_gaap_gap is not filled in quarters-back-0, nor in any of the 13 periods the table holds; the record carries no non-GAAP measure. The release prints a non-GAAP net income figure, but no gap value exists in my input and I do not derive one",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "none — no value exists",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001262039-26-000021:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_quarterly",
  "what_changed": "value 0.7107768934029982 (AccountsReceivableNetCurrent 1455600000.0 over quarterly revenue 2047900000.0); quarter_over_quarter change -0.09274819310219207 against quarters-back-1 (0.8035250865051903, highest of the 6 filled quarters); year_over_year change -0.03505132745589745 against quarters-back-4 (0.7458282208588957)",
  "account": "receivables over quarterly revenue",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_quarterly",
  "what_changed": "value 0.5732282304405482 (Assets 10859200000.0, PropertyPlantAndEquipmentNet 1699500000.0, cash 2934900000.0); quarter_over_quarter change -0.030626679257433342 against quarters-back-1 (0.6038549096979815); year_over_year change 0.03494379418216109 against quarters-back-4 (0.5382844362583871)",
  "account": "soft assets over total assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing — the two printed changes disagree in sign",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_quarterly_insufficient",
  "what_changed": "insufficient — warranty_reserve_ratio is not filled in quarters-back-0, nor in any of the 13 periods the table holds (filled 0); the record holds no warranty accrual row for these periods",
  "account": "warranty accrual ratio",
  "expected_direction": "none",
  "horizon": "none — no value exists",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly_history_too_short",
  "what_changed": "insufficient for a trend — the quarterly accruals series is filled in only 2 quarters: quarters-back-1 -0.054899580108261244 and quarters-back-5 -0.04130873450562122 (year_over_year change -0.013590845602640025); two points do not support a trend claim",
  "account": "accruals over total assets, quarterly series",
  "expected_direction": "none",
  "horizon": "none — two filled quarters",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly_history_too_short",
  "what_changed": "insufficient for a trend — the quarterly bad-debt series is filled in one quarter only, quarters-back-7 (value 0.004481311975591152, allowance 4700000.0); every later quarter in the window is unfilled",
  "account": "allowance for doubtful accounts over gross receivables, quarterly series",
  "expected_direction": "none",
  "horizon": "none — one filled quarter",
  "quote": "\"position_in_history\": \"the only filled quarter\"",
  "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2024-07-01..2024-09-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_annual",
  "what_changed": "value -0.07095830285296269 (NetIncomeLoss 1853400000.0, NetCashProvidedByUsedInOperatingActivities 2590600000.0, Assets 10389200000.0); year_over_year change -0.01842375952143889 against years-back-1 (-0.0525345433315238, highest of the 5 filled years)",
  "account": "accruals over total assets",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_annual",
  "what_changed": "value 0.0043565289061580125 (AllowanceForDoubtfulAccountsReceivable 7400000.0, AccountsReceivableNetCurrent 1691200000.0); year_over_year change 0.00034101131274618356 against years-back-1 (0.004015517593411829)",
  "account": "allowance for doubtful accounts over gross receivables",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_annual",
  "what_changed": "value 0.5347373374904406 (ContractWithCustomerLiabilityCurrent 3636000000.0 over annual revenue 6799600000.0); year_over_year change -0.015348293323220075 against years-back-1 (0.5500856308136607, highest of the 5 filled years)",
  "account": "current contract liabilities over annual revenue",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_annual",
  "what_changed": "value 109.72797050191888 days (InventoryNet 399500000.0, CostOfGoodsAndServicesSold 1328900000.0, 365 days); year_over_year change 9.975897246908517 against years-back-1 (99.75207325501036)",
  "account": "days sales of inventory",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_annual",
  "what_changed": "value 90.78298723454321 days (AccountsReceivableNetCurrent 1691200000.0 over annual revenue 6799600000.0, 365 days); year_over_year change 0.8531037596112157 against years-back-1 (89.929883474932)",
  "account": "days sales outstanding",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_annual",
  "what_changed": "value 0.8045620330607682 (revenue 6799600000.0, cost of revenue 1328900000.0); year_over_year change -0.0010728102852138877 against years-back-1 (0.8056348433459821, highest of the 5 filled years)",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_annual",
  "what_changed": "value 0.344180225281602 (InventoryValuationReserves 137500000.0 over InventoryNet 399500000.0); year_over_year change -0.11477381592283536 against years-back-1 (0.4589540412044374, highest of the 4 filled years); the series holds 4 filled years because years-back-4 is unfilled: \"no row for inventory_reserve in 2021-12-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "account": "inventory valuation reserve over net inventory",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 4 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_annual_insufficient",
  "what_changed": "insufficient — non_gaap_gap is not filled in years-back-0 nor in any other period; the record carries no non-GAAP measure",
  "account": "gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "none — no value exists",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001262039-26-000021:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_annual",
  "what_changed": "value 0.24872051297135125 (AccountsReceivableNetCurrent 1691200000.0 over annual revenue 6799600000.0); year_over_year change 0.003010448832192786 against years-back-1 (0.24571006413915847)",
  "account": "receivables over annual revenue",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_annual",
  "what_changed": "value 0.6039829823278019 (Assets 10389200000.0, PropertyPlantAndEquipmentNet 1619000000.0, cash 2495300000.0); year_over_year change 0.0367758452504392 against years-back-1 (0.5672071370773627, lowest of the 5 filled years)",
  "account": "soft assets over total assets",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_annual_insufficient",
  "what_changed": "insufficient — warranty_reserve_ratio is not filled in years-back-0 nor in any other year of the table",
  "account": "warranty accrual ratio",
  "expected_direction": "none",
  "horizon": "none — no value exists",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-12-31: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

Change of tag (from the numeric facts):

```json
{ "id": "structure_and_disclosure_changes_current_deferred_revenue_tag_differs_between_annual_and_quarterly_filings",
  "what_changed": "The 10-K (0001262039-26-000007) tags current deferred revenue at 2025-12-31 as us-gaap:DeferredRevenueCurrent, value 3636000000, and the row carries no superseded_by mark. Both 10-Qs tag the same instant as us-gaap:ContractWithCustomerLiabilityCurrent at 3636000000: 0001262039-26-000013:facts:ContractWithCustomerLiabilityCurrent:2025-12-31 and 0001262039-26-000021:facts:ContractWithCustomerLiabilityCurrent:2025-12-31. The amount is the same as printed, so this is a change of tag, not a restatement. The trend table's contract_liabilities input is ContractWithCustomerLiabilityCurrent in every period I read. Its year-end values come from 10-Q rows, not from the 10-Ks: years-back-0 from 0001262039-26-000021, years-back-1 from 0001262039-25-000039 (3276200000.0, where the 10-K's DeferredRevenueCurrent:2024-12-31 row also reads 3276200000), and years-back-2 from 0001262039-24-000043. The same pattern therefore appears at the prior year-end. The 10-K's DeferredRevenueNoncurrent:2025-12-31 row (3479800000) also carries no superseded_by mark. I did not locate the concept the 10-Qs use for that instant and make no claim about it",
  "account": "current deferred revenue / current contract liabilities",
  "expected_direction": "none",
  "horizon": "next annual filing, where the year-end balance is tagged again",
  "quote": "\"value\": \"3636000000\"",
  "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueCurrent:2025-12-31" }
```

From the 8-K earnings release (0001262039-26-000018), guidance and headline results:

```json
{ "id": "results_against_expectations_quarter_above_high_end_of_guidance_release",
  "what_changed": "The release states second-quarter revenue and profitability exceeded the high end of guidance. The earlier guidance figures are not in my input, so the size of the beat does not exist for me",
  "account": "second-quarter revenue and profitability against prior guidance",
  "expected_direction": "up",
  "horizon": "second quarter 2026 (reported)",
  "quote": "Exceeds high end of second quarter guidance on revenue and profitability",
  "paragraph_id": "0001262039-26-000018:8k_2_02:5" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised_release",
  "what_changed": "Full-year 2026 revenue guidance was raised to 19% year-over-year growth as printed. The previous guidance figure is not in my input",
  "account": "full-year 2026 revenue guidance",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "Raises 2026 revenue guidance to 19% year over year growth",
  "paragraph_id": "0001262039-26-000018:8k_2_02:6" }
```

```json
{ "id": "results_against_expectations_third_quarter_revenue_guidance_release",
  "what_changed": "The third-quarter 2026 revenue range of $2.010-$2.100 billion brackets the printed second-quarter revenue of $2,047.9 million",
  "account": "third-quarter revenue guidance",
  "expected_direction": "none",
  "horizon": "third quarter 2026 (next quarterly filing)",
  "quote": "Revenue in the range of $2.010 billion to $2.100 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:28" }
```

```json
{ "id": "results_against_expectations_third_quarter_billings_guidance_release",
  "what_changed": "The third-quarter 2026 billings range of $2.250-$2.350 billion sits below the printed second-quarter total billings of $2,372.1 million. Billings is a non-GAAP measure printed only in the release",
  "account": "third-quarter billings guidance",
  "expected_direction": "down",
  "horizon": "third quarter 2026 (next quarterly filing)",
  "quote": "Billings in the range of $2.250 billion to $2.350 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:29" }
```

```json
{ "id": "results_against_expectations_third_quarter_gross_margin_guidance_release",
  "what_changed": "The third-quarter non-GAAP gross margin range of 79.0%-81.0% brackets the printed second-quarter non-GAAP gross margin of 80.9% (second-quarter 2025: 81.6%)",
  "account": "third-quarter non-GAAP gross margin guidance",
  "expected_direction": "none",
  "horizon": "third quarter 2026 (next quarterly filing)",
  "quote": "Non-GAAP gross margin in the range of 79.0% to 81.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:30" }
```

```json
{ "id": "results_against_expectations_third_quarter_operating_margin_guidance_release",
  "what_changed": "The third-quarter non-GAAP operating margin range of 35.0%-37.0% sits below the printed second-quarter non-GAAP operating margin of 38.0% (second-quarter 2025: 33.1%)",
  "account": "third-quarter non-GAAP operating margin guidance",
  "expected_direction": "down",
  "horizon": "third quarter 2026 (next quarterly filing)",
  "quote": "Non-GAAP operating margin in the range of 35.0% to 37.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:31" }
```

```json
{ "id": "results_against_expectations_third_quarter_earnings_per_share_guidance_release",
  "what_changed": "The third-quarter diluted non-GAAP EPS range of $0.83-$0.87 assumes an 18% non-GAAP tax rate and 741-745 million diluted shares. It sits below the printed second-quarter non-GAAP diluted EPS of $0.90 (second-quarter 2025: $0.64)",
  "account": "third-quarter non-GAAP diluted EPS guidance",
  "expected_direction": "down",
  "horizon": "third quarter 2026 (next quarterly filing)",
  "quote": "Diluted non-GAAP net income per share in the range of $0.83 to $0.87, assuming a non-GAAP effective tax rate of 18%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:32" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_range_release",
  "what_changed": "The full-year 2026 revenue range of $8.020-$8.180 billion sits above the 10-K's 2025 revenue of 6799600000 (0001262039-26-000007:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-01-01..2025-12-31). The prior range is not in my input",
  "account": "full-year revenue guidance",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "Revenue in the range of $8.020 billion to $8.180 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:34" }
```

```json
{ "id": "results_against_expectations_full_year_service_revenue_guidance_release",
  "what_changed": "The full-year 2026 service revenue range of $5.180-$5.220 billion sits above the 10-K's 2025 service revenue of 4581200000 (srt:ProductOrServiceAxis=us-gaap:ServiceMember). The prior range is not in my input",
  "account": "full-year service revenue guidance",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "Service revenue in the range of $5.180 billion to $5.220 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:35" }
```

```json
{ "id": "results_against_expectations_full_year_billings_guidance_release",
  "what_changed": "The full-year 2026 billings range is $9.350-$9.550 billion. Insufficient for a comparison: no 2025 billings figure and no prior range exist in my input",
  "account": "full-year billings guidance",
  "expected_direction": "none",
  "horizon": "fiscal year 2026",
  "quote": "Billings in the range of $9.350 billion to $9.550 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:36" }
```

```json
{ "id": "results_against_expectations_full_year_gross_margin_guidance_release",
  "what_changed": "The full-year 2026 non-GAAP gross margin range of 79.0%-81.0% is the same text as the third-quarter range. Insufficient for a comparison: no 2025 or six-month non-GAAP gross margin exists in my input",
  "account": "full-year non-GAAP gross margin guidance",
  "expected_direction": "none",
  "horizon": "fiscal year 2026",
  "quote": "Non-GAAP gross margin in the range of 79.0% to 81.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:37" }
```

```json
{ "id": "results_against_expectations_full_year_operating_margin_guidance_release",
  "what_changed": "The full-year 2026 non-GAAP operating margin range of 35.0%-37.0% is the same text as the third-quarter range. Insufficient for a comparison: no 2025 or six-month non-GAAP operating margin exists in my input",
  "account": "full-year non-GAAP operating margin guidance",
  "expected_direction": "none",
  "horizon": "fiscal year 2026",
  "quote": "Non-GAAP operating margin in the range of 35.0% to 37.0%",
  "paragraph_id": "0001262039-26-000018:8k_2_02:38" }
```

```json
{ "id": "results_against_expectations_full_year_earnings_per_share_guidance_release",
  "what_changed": "The full-year 2026 diluted non-GAAP EPS range is $3.41-$3.47. Insufficient for a comparison: no 2025 non-GAAP EPS and no prior range exist in my input",
  "account": "full-year non-GAAP diluted EPS guidance",
  "expected_direction": "none",
  "horizon": "fiscal year 2026",
  "quote": "Diluted non-GAAP net income per share in the range of $3.41 to $3.47",
  "paragraph_id": "0001262039-26-000018:8k_2_02:39" }
```

```json
{ "id": "earnings_quality_guidance_not_reconciled_to_gaap_release",
  "what_changed": "All margin and EPS guidance is non-GAAP and the release states it is not reconciled to GAAP. The excluded items it names are stock-based compensation, amortization of acquired intangibles, gain on intellectual property matters and a tax adjustment",
  "account": "guidance basis",
  "expected_direction": "none",
  "horizon": "third quarter and fiscal year 2026",
  "quote": "We have not reconciled our guidance with respect to non-GAAP financial measures to the corresponding GAAP measures",
  "paragraph_id": "0001262039-26-000018:8k_2_02:40" }
```

```json
{ "id": "revenue_recognition_total_revenue_growth_release",
  "what_changed": "Second-quarter revenue grew 26% year over year to $2.05 billion as printed. The table prints total revenue of 2,047.9 against 1,630.0",
  "account": "total revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "Revenue grew 26% year over year to $2.05 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:8" }
```

```json
{ "id": "revenue_recognition_product_revenue_growth_release",
  "what_changed": "Product revenue grew 52% year over year to $773 million as printed. The table prints 773.0 against 508.9 for the quarter and 1,418.1 against 968.0 for six months. Product revenue grew faster than service revenue in the printed figures",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "Product revenue grew 52% year over year to $773 million",
  "paragraph_id": "0001262039-26-000018:8k_2_02:9" }
```

```json
{ "id": "revenue_recognition_service_revenue_release",
  "what_changed": "Service revenue is 1,274.9 against 1,121.1 for the quarter and 2,479.4 against 2,201.7 for six months. The release prints no growth rate for service revenue",
  "account": "service revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Service | 1,274.9 |  |  | 1,121.1 |  |  | 2,479.4 |  |  | 2,201.7 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "revenue_recognition_billings_growth_release",
  "what_changed": "Billings grew 33% year over year to $2.37 billion as printed. The reconciliation prints total billings of 2,372.1 against 1,778.4. Billings is non-GAAP; no billings figure exists in the filed facts",
  "account": "billings",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "Billings grew 33% year over year to $2.37 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:10" }
```

```json
{ "id": "revenue_recognition_billings_change_in_deferred_revenue_release",
  "what_changed": "The change in deferred revenue added in the billings reconciliation is 324.2 against 149.2 for the quarter. Deferred revenue acquired is a dash against (0.8)",
  "account": "change in deferred revenue (billings bridge)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Add: Change in deferred revenue | 324.2 |  |  | 149.2 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:81" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_cash_flow_release",
  "what_changed": "The operating cash-flow line for deferred revenue is 559.9 for six months against 204.8",
  "account": "change in deferred revenue (cash flow, six months)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Deferred revenue | 559.9 |  |  | 204.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "revenue_recognition_current_deferred_revenue_balance_release",
  "what_changed": "Current deferred revenue is 3,841.8 at 2026-06-30 against 3,636.0 at 2025-12-31. The trend table's contract-liabilities ratio uses the same 3841800000.0 and still sits lowest of its 6 filled quarters, because quarterly revenue rose",
  "account": "current deferred revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Deferred revenue | 3,841.8 |  |  | 3,636.0 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "revenue_recognition_noncurrent_deferred_revenue_balance_release",
  "what_changed": "Non-current deferred revenue is 3,833.9 at 2026-06-30 against 3,479.8 at 2025-12-31",
  "account": "non-current deferred revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| DEFERRED REVENUE | 3,833.9 |  |  | 3,479.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "revenue_recognition_receivables_balance_release",
  "what_changed": "Accounts receivable, net, is 1,455.6 at 2026-06-30 against 1,691.2 at 2025-12-31. The trend table places quarterly DSO and receivables-over-revenue third lowest of 6 filled quarters",
  "account": "accounts receivable, net",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Accounts receivable—net | 1,455.6 |  |  | 1,691.2 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_release",
  "what_changed": "The operating cash-flow line for accounts receivable is 235.1 for six months against 262.7. It is positive in both periods, and the current amount is smaller",
  "account": "change in accounts receivable (cash flow, six months)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Accounts receivable—net | 235.1 |  |  | 262.7 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_gaap_gross_margin_release",
  "what_changed": "GAAP gross margin is 80.2% against 80.7%. The non-GAAP gross margin row prints 80.9% against 81.6%. The trend table independently places quarterly gross margin lowest of its 6 filled quarters",
  "account": "GAAP gross margin",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| GAAP gross margin | 80.2 | % |  | 80.7 | % |  |  |  |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:76" }
```

```json
{ "id": "earnings_quality_gaap_operating_margin_release",
  "what_changed": "GAAP operating margin is 33.7% against 28.1%. The non-GAAP operating margin row prints 38.0% against 33.1%",
  "account": "GAAP operating margin",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| GAAP operating margin | 33.7 | % |  | 28.1 | % |  |  |  |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:76" }
```

```json
{ "id": "earnings_quality_operating_income_release",
  "what_changed": "Operating income is 689.3 against 458.0 for the quarter and 1,269.3 against 911.8 for six months",
  "account": "operating income",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| OPERATING INCOME | 689.3 |  |  | 458.0 |  |  | 1,269.3 |  |  | 911.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_net_income_release",
  "what_changed": "Net income is 606.3 against 440.1 for the quarter and 1,140.8 against 873.5 for six months",
  "account": "net income",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| NET INCOME | $ | 606.3 |  |  | $ | 440.1 |  |  | $ | 1,140.8 |  |  | $ | 873.5 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_gaap_earnings_per_share_growth_release",
  "what_changed": "GAAP diluted EPS grew 44% year over year to $0.82 as printed. The table prints $0.82 against $0.57 for the quarter and $1.54 against $1.13 for six months",
  "account": "GAAP diluted EPS",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "GAAP earnings per share grew 44% year over year to $0.82",
  "paragraph_id": "0001262039-26-000018:8k_2_02:13" }
```

```json
{ "id": "earnings_quality_non_gaap_earnings_per_share_growth_release",
  "what_changed": "Non-GAAP diluted EPS grew 41% year over year to $0.90 as printed. The reconciliation prints $0.90 against $0.64, with non-GAAP adjustments of 0.08 against 0.07 per share",
  "account": "non-GAAP diluted EPS",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "Non-GAAP earnings per share grew 41% year over year to $0.90",
  "paragraph_id": "0001262039-26-000018:8k_2_02:14" }
```

```json
{ "id": "earnings_quality_non_gaap_net_income_release",
  "what_changed": "Non-GAAP net income is 665.0 against 491.1, beside GAAP net income of 606.3 against 440.1. The add-backs are stock-based compensation 80.8 against 69.9, amortization of acquired intangibles 9.9 against 13.2, gain on intellectual property matters (1.3) against (1.3), and the tax adjustment (30.7) against (30.8). The trend table's non_gaap_gap is unfilled and I do not derive it",
  "account": "non-GAAP net income",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Non-GAAP net income | $ | 665.0 |  |  | $ | 491.1 |  |  |  |  |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:76" }
```

```json
{ "id": "earnings_quality_non_gaap_tax_adjustment_release",
  "what_changed": "The non-GAAP tax adjustment is (30.7) against (30.8). The release states non-GAAP results are adjusted to an 18% effective tax rate in both periods, while the filed GAAP effective tax rate is 0.16 against 0.15 (see notes)",
  "account": "non-GAAP tax adjustment",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "| Tax adjustment (a) | (30.7) |  |  | (30.8) |  |  |  |  |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:76" }
```

```json
{ "id": "earnings_quality_product_cost_of_revenue_release",
  "what_changed": "Product cost of revenue is 233.8 against 165.9 for the quarter and 442.1 against 315.8 for six months. Product gross profit is 539.2 against 343.0",
  "account": "product cost of revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Product | 233.8 |  |  | 165.9 |  |  | 442.1 |  |  | 315.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_service_cost_of_revenue_release",
  "what_changed": "Service cost of revenue is 170.9 against 149.0 for the quarter and 327.1 against 292.2 for six months. Service gross profit is 1,104.0 against 972.1",
  "account": "service cost of revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Service | 170.9 |  |  | 149.0 |  |  | 327.1 |  |  | 292.2 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_research_and_development_expense_release",
  "what_changed": "Research and development is 225.0 against 209.5 for the quarter and 439.0 against 408.1 for six months",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Research and development | 225.0 |  |  | 209.5 |  |  | 439.0 |  |  | 408.1 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_sales_and_marketing_expense_release",
  "what_changed": "Sales and marketing is 669.1 against 592.0 for the quarter and 1,305.4 against 1,134.7 for six months",
  "account": "sales and marketing expense",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Sales and marketing | 669.1 |  |  | 592.0 |  |  | 1,305.4 |  |  | 1,134.7 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_general_and_administrative_expense_release",
  "what_changed": "General and administrative is 61.1 against 56.9 for the quarter and 117.3 against 114.7 for six months",
  "account": "general and administrative expense",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| General and administrative | 61.1 |  |  | 56.9 |  |  | 117.3 |  |  | 114.7 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_gain_on_intellectual_property_matters_release",
  "what_changed": "The gain on intellectual property matters, shown within operating expenses, is (1.3) against (1.3) for the quarter and (2.7) against (7.6) for six months. The non-GAAP measures exclude it",
  "account": "gain on intellectual property matters",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "| Gain on intellectual property matters | (1.3) |  |  | (1.3) |  |  | (2.7) |  |  | (7.6) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_interest_income_release",
  "what_changed": "Interest income is 33.2 against 45.0 for the quarter and 66.1 against 89.3 for six months, lower in both",
  "account": "interest income",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| INTEREST INCOME | 33.2 |  |  | 45.0 |  |  | 66.1 |  |  | 89.3 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_interest_expense_release",
  "what_changed": "Interest expense is (3.2) against (4.6) for the quarter and (7.4) against (9.5) for six months. The 2026 senior notes were repaid on 2026-03-15 (see notes)",
  "account": "interest expense",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| INTEREST EXPENSE | (3.2) |  |  | (4.6) |  |  | (7.4) |  |  | (9.5) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_other_income_release",
  "what_changed": "Other income, net, is 0.9 against 18.9 for the quarter but 48.8 against 45.0 for six months. The quarter is lower and the six months higher",
  "account": "other income, net",
  "expected_direction": "none",
  "horizon": "next quarterly filing — the quarter and six-month comparisons disagree",
  "quote": "| OTHER INCOME—NET | 0.9 |  |  | 18.9 |  |  | 48.8 |  |  | 45.0 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_provision_for_income_taxes_release",
  "what_changed": "The provision for income taxes is 115.0 against 77.1 for the quarter and 237.0 against 173.6 for six months",
  "account": "provision for income taxes",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| PROVISION FOR INCOME TAXES | 115.0 |  |  | 77.1 |  |  | 237.0 |  |  | 173.6 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_equity_method_investment_result_release",
  "what_changed": "The gain (loss) from equity method investments is 1.1 against (0.1) for the quarter and 1.0 against 10.5 for six months. The six-month 2025 comparative contains the 2025-01-31 Linksys transaction (see notes)",
  "account": "gain (loss) from equity method investments",
  "expected_direction": "none",
  "horizon": "next quarterly filing — the quarter and six-month comparisons disagree",
  "quote": "| GAIN (LOSS) FROM EQUITY METHOD INVESTMENTS | 1.1 |  |  | (0.1) |  |  | 1.0 |  |  | 10.5 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "earnings_quality_stock_based_compensation_cash_flow_release",
  "what_changed": "Stock-based compensation added back in operating cash flow is 151.8 for six months against 135.2",
  "account": "stock-based compensation",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Stock-based compensation | 151.8 |  |  | 135.2 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_deferred_contract_costs_capitalized_release",
  "what_changed": "The cash-flow line for deferred contract costs is (240.5) for six months against (202.5). It is larger, while amortization of deferred contract costs is 190.9 against 160.0",
  "account": "deferred contract costs (cash flow, six months)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Deferred contract costs | (240.5) |  |  | (202.5) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_deferred_contract_costs_amortized_release",
  "what_changed": "Amortization of deferred contract costs is 190.9 for six months against 160.0",
  "account": "amortization of deferred contract costs",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Amortization of deferred contract costs | 190.9 |  |  | 160.0 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_deferred_contract_costs_balance_release",
  "what_changed": "The deferred contract costs balance is 785.1 at 2026-06-30 against 735.5 at 2025-12-31",
  "account": "deferred contract costs",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| DEFERRED CONTRACT COSTS | 785.1 |  |  | 735.5 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "earnings_quality_deferred_tax_assets_cash_flow_release",
  "what_changed": "The cash-flow line for deferred tax assets is (3.6) for six months against (75.3), a smaller amount. The deferred tax assets balance is 1,319.4 against 1,314.9",
  "account": "deferred tax assets (cash flow, six months)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Deferred tax assets | (3.6) |  |  | (75.3) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_inventory_balance_release",
  "what_changed": "Inventory is 426.3 at 2026-06-30 against 399.5 at 2025-12-31. The trend table places quarterly DSI second lowest of 6 filled quarters",
  "account": "inventory",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Inventory | 426.3 |  |  | 399.5 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "earnings_quality_inventory_cash_flow_release",
  "what_changed": "The cash-flow line for inventory is (38.0) for six months against (79.6), a smaller amount",
  "account": "inventory (cash flow, six months)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Inventory | (38.0) |  |  | (79.6) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_accrued_liabilities_cash_flow_release",
  "what_changed": "The cash-flow line for accrued liabilities is 54.5 for six months against (9.7). The sign changed from a use to a source",
  "account": "accrued liabilities (cash flow, six months)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Accrued liabilities | 54.5 |  |  | (9.7) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_investment_discount_amortization_release",
  "what_changed": "Amortization of investment discounts is (9.3) for six months against (19.4), a smaller amount",
  "account": "amortization of investment discounts",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Amortization of investment discounts | (9.3) |  |  | (19.4) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_quarterly_operating_cash_flow_release",
  "what_changed": "Second-quarter net cash provided by operating activities is 1,043.6 against 451.9. The release highlight prints $1.04 billion",
  "account": "operating cash flow (quarter)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Net cash provided by operating activities | $ | 1,043.6 |  |  | $ | 451.9 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

```json
{ "id": "liquidity_and_capital_six_month_operating_cash_flow_release",
  "what_changed": "Six-month net cash provided by operating activities is 2,120.7 against 1,315.2",
  "account": "operating cash flow (six months)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Net cash provided by operating activities | 2,120.7 |  |  | 1,315.2 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_free_cash_flow_release",
  "what_changed": "Second-quarter free cash flow (non-GAAP) is 965.6 against 284.1, after purchases of property and equipment of (78.0) against (167.8). Adjusted free cash flow is 995.9 against 427.9",
  "account": "free cash flow",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Free cash flow | $ | 965.6 |  |  | $ | 284.1 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

```json
{ "id": "liquidity_and_capital_free_cash_flow_margin_release",
  "what_changed": "Free cash flow margin is 47.2% against 17.4%. Adjusted free cash flow margin is 48.6% against 26.3%",
  "account": "free cash flow margin",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Free cash flow margin | 47.2 | % |  | 17.4 | % |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

```json
{ "id": "liquidity_and_capital_real_estate_purchases_release",
  "what_changed": "Real estate related purchases added back for adjusted free cash flow are 30.3 against 143.8 for the quarter",
  "account": "real estate related purchases",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Add: Real estate related purchases | 30.3 |  |  | 143.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_release",
  "what_changed": "Purchases of property and equipment are (148.6) for six months against (234.3), a smaller amount",
  "account": "capital expenditure (six months)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Purchases of property and equipment | (148.6) |  |  | (234.3) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_release",
  "what_changed": "Repurchase and retirement of common stock is (972.8) for six months against (401.1)",
  "account": "share repurchases",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Repurchase and retirement of common stock | (972.8) |  |  | (401.1) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_senior_notes_repaid_release",
  "what_changed": "Repayment of senior notes is (500.0) for six months against a dash. Net cash used in financing activities is (1,490.8) against (446.9)",
  "account": "senior notes repayment",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Repayment of senior notes | (500.0) |  |  | — |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_current_debt_cleared_release",
  "what_changed": "The current portion of long-term debt is a dash at 2026-06-30 against 499.7 at 2025-12-31. Long-term debt is 496.9 against 496.6",
  "account": "current portion of long-term debt",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Current portion of long-term debt | — |  |  | 499.7 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_release",
  "what_changed": "Cash and cash equivalents are 2,934.9 at 2026-06-30 against 2,495.3 at 2025-12-31",
  "account": "cash and cash equivalents",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Cash and cash equivalents | $ | 2,934.9 |  |  | $ | 2,495.3 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_short_term_investments_release",
  "what_changed": "Short-term investments are 1,134.7 against 1,087.2. Long-term investments are 399.1 against 339.7",
  "account": "short-term investments",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Short-term investments | 1,134.7 |  |  | 1,087.2 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_sales_of_investments_release",
  "what_changed": "Sales of investments are 118.4 for six months against 5.7. Purchases of investments are (756.0) against (976.5) and maturities 587.5 against 869.6",
  "account": "sales of investments",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Sales of investments | 118.4 |  |  | 5.7 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_release",
  "what_changed": "Accounts payable is 282.5 at 2026-06-30 against 230.8 at 2025-12-31",
  "account": "accounts payable",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Accounts payable | $ | 282.5 |  |  | $ | 230.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_balance_release",
  "what_changed": "Accrued liabilities are 393.7 at 2026-06-30 against 354.6. Accrued payroll and compensation is 322.8 against 312.9",
  "account": "accrued liabilities",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Accrued liabilities | 393.7 |  |  | 354.6 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_stockholders_equity_release",
  "what_changed": "Total stockholders' equity is 1,551.1 at 2026-06-30 against 1,237.5 at 2025-12-31",
  "account": "total stockholders' equity",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Total stockholders’ equity | 1,551.1 |  |  | 1,237.5 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_accumulated_deficit_release",
  "what_changed": "The accumulated deficit is (316.7) at 2026-06-30 against (507.9) at 2025-12-31, a smaller deficit",
  "account": "accumulated deficit",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Accumulated deficit | (316.7) |  |  | (507.9) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "liquidity_and_capital_diluted_share_count_release",
  "what_changed": "Weighted-average diluted shares are 739.9 against 772.7 for the quarter and 741.3 against 774.8 for six months. Basic shares are 733.1 against 765.5",
  "account": "diluted weighted-average shares",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Diluted | 739.9 |  |  | 772.7 |  |  | 741.3 |  |  | 774.8 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:68" }
```

```json
{ "id": "liquidity_and_capital_proceeds_from_share_issuance_release",
  "what_changed": "Proceeds from issuance of common stock are 62.3 for six months against 31.3",
  "account": "proceeds from issuance of common stock",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "| Proceeds from issuance of common stock | 62.3 |  |  | 31.3 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_taxes_paid_on_share_settlement_release",
  "what_changed": "Taxes paid related to net share settlement of equity awards are (59.1) for six months against (77.0), a smaller amount",
  "account": "taxes paid on net share settlement",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Taxes paid related to net share settlement of equity awards | (59.1) |  |  | (77.0) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_quarterly_financing_cash_flow_release",
  "what_changed": "Second-quarter net cash used in financing activities is (147.9) against (414.2). Second-quarter net cash used in investing activities is (184.6) against (266.2)",
  "account": "financing cash flow (quarter)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "| Net cash used in financing activities | $ | (147.9) |  |  | $ | (414.2) |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

```json
{ "id": "liquidity_and_capital_credit_rating_upgrade_release",
  "what_changed": "Moody's upgraded the senior unsecured notes rating to A3 from Baa1, and the shelf rating to (P)A3 from (P)Baa1, as stated in the release",
  "account": "credit rating",
  "expected_direction": "up",
  "horizon": "none stated",
  "quote": "Moody’s Ratings upgraded Fortinet’s senior unsecured notes rating to A3 from Baa1",
  "paragraph_id": "0001262039-26-000018:8k_2_02:25" }
```

From the filed statements (10-Q 0001262039-26-000021) and across documents:

```json
{ "id": "liquidity_and_capital_income_taxes_paid_filed_fact",
  "what_changed": "Income taxes paid are 209500000 for six months against 264000000.0 (0001262039-26-000021:facts:IncomeTaxesPaid:2025-01-01..2025-06-30). They are lower while the provision for income taxes is higher (237.0 against 173.6 in the release)",
  "account": "income taxes paid",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"209500000\"",
  "paragraph_id": "0001262039-26-000021:facts:IncomeTaxesPaid:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_not_yet_paid_filed_fact",
  "what_changed": "Capital expenditures incurred but not yet paid are 25900000 for six months against 19400000",
  "account": "capital expenditures incurred but not yet paid",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"25900000\"",
  "paragraph_id": "0001262039-26-000021:facts:CapitalExpendituresIncurredButNotYetPaid:2026-01-01..2026-06-30" }
```

```json
{ "id": "across_documents_release_figures_agree_with_filed_facts",
  "what_changed": "Each release figure I compared reads the same as the 10-Q fact for the same period, release in millions and fact in units. These are: total revenue 2,047.9 / 2047900000; product revenue 773.0 / 773000000.0; service revenue 1,274.9 / 1274900000; net income 606.3 / 606300000; diluted EPS 0.82 / 0.82; diluted shares 739.9 / 739900000; current deferred revenue 3,841.8 / 3841800000.0; receivables 1,455.6 / 1455600000.0; inventory 426.3 / 426300000; PP&E 1,699.5 / 1699500000; six-month repurchases 972.8 / 972800000; tax provision 115.0 / 115000000.0. I found no difference",
  "account": "release against filing",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"2047900000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "across_documents_quarterly_operating_cash_flow_only_in_release",
  "what_changed": "The release prints a three-month operating cash flow of 1,043.6. The trend table could not fill quarterly accruals_over_total_assets because the record holds no three-month operating cash flow row (the 10-Q states six months). That quarterly figure therefore exists only in the release in my input, and I do not use it to derive the missing ratio",
  "account": "quarterly operating cash flow",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "| Net cash provided by operating activities | $ | 1,043.6 |  |  | $ | 451.9 |  |",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

# Seen in the notes

As stated above: my input carries no in-note marker. These facts sit here because their element or dimension is a note disclosure. Several repeat an item above, and are kept separate as instructed.

```json
{ "id": "revenue_recognition_remaining_performance_obligation_note",
  "what_changed": "Remaining performance obligations are 7730000000 at 2026-06-30. The Q1 10-Q's row at 2026-03-31 reads 7450000000 (0001262039-26-000013:facts:RevenueRemainingPerformanceObligation:2026-03-31) and the 10-K's row at 2025-12-31 reads 7180000000, so the value is higher at each successive filing in my input. Three points only: insufficient for a trend claim",
  "account": "remaining performance obligations",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"7730000000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueRemainingPerformanceObligation:2026-06-30" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_first_timing_band_note",
  "what_changed": "The amount tagged to an expected-timing start date of 2026-07-01 is 3860000000 at 2026-06-30. I have no earlier value for this band in my notes, so it is insufficient for a comparison",
  "account": "remaining performance obligations, timing band starting 2026-07-01",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"3860000000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueRemainingPerformanceObligation:2026-06-30:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-07-01" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_second_timing_band_note",
  "what_changed": "The amount tagged to an expected-timing start date of 2027-07-01 is 3080000000.00 at 2026-06-30. I have no earlier value for this band in my notes, so it is insufficient for a comparison",
  "account": "remaining performance obligations, timing band starting 2027-07-01",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"3080000000.00\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueRemainingPerformanceObligation:2026-06-30:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2027-07-01" }
```

```json
{ "id": "revenue_recognition_revenue_recognized_from_opening_contract_liabilities_note",
  "what_changed": "Service revenue recognized from contract liabilities is 996900000 for the quarter against 876800000. For six months it is 2090000000.00 against 1850000000, both tagged with decimals -7",
  "account": "revenue recognized from contract liabilities (service)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"996900000\"",
  "paragraph_id": "0001262039-26-000021:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember" }
```

```json
{ "id": "revenue_recognition_security_subscription_revenue_note",
  "what_changed": "Security subscription revenue is 729700000 for the quarter against 644400000, and 1423700000 against 1267500000 for six months",
  "account": "security subscription revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"729700000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=ftnt:SecuritySubscriptionMember" }
```

```json
{ "id": "revenue_recognition_technical_support_revenue_note",
  "what_changed": "Technical support and other revenue is 545200000 for the quarter against 476700000, and 1055700000 against 934200000 for six months",
  "account": "technical support and other revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"545200000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=ftnt:TechnicalSupportandOtherMember" }
```

```json
{ "id": "revenue_recognition_product_revenue_note",
  "what_changed": "Product revenue in the disaggregation table is 773000000.0 for the quarter against 508900000, and 1418100000 against 968000000.0 for six months",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"773000000.0\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "earnings_quality_contract_cost_amortization_note",
  "what_changed": "Amortization of capitalized contract costs is 96700000 for the quarter against 82000000.0, and 190900000 against 160000000.0 for six months",
  "account": "capitalized contract cost amortization",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"96700000\"",
  "paragraph_id": "0001262039-26-000021:facts:CapitalizedContractCostAmortization:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_distributor_a_revenue_share_note",
  "what_changed": "Distributor A's share of revenue is 0.27 for the quarter against 0.27, and 0.28 against 0.27 for six months. The 10-K printed 0.28 / 0.29 / 0.28 for 2025 / 2024 / 2023",
  "account": "revenue concentration, distributor A",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.27\"",
  "paragraph_id": "0001262039-26-000021:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:MajorCustomersAxis=ftnt:DistributorAMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_distributor_b_revenue_share_note",
  "what_changed": "Distributor B's share of revenue is 0.15 for the quarter against 0.15, and 0.15 against 0.15 for six months. The 10-K printed 0.15 for each of 2025, 2024 and 2023",
  "account": "revenue concentration, distributor B",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.15\"",
  "paragraph_id": "0001262039-26-000021:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:MajorCustomersAxis=ftnt:DistributorBMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_distributor_c_revenue_share_note",
  "what_changed": "Distributor C's share of revenue is 0.11 for the quarter against 0.12, and 0.12 against 0.12 for six months. The 10-K printed 0.12 / 0.13 / 0.13 for 2025 / 2024 / 2023",
  "account": "revenue concentration, distributor C",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.11\"",
  "paragraph_id": "0001262039-26-000021:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:MajorCustomersAxis=ftnt:DistributorCMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_distributor_a_receivables_share_note",
  "what_changed": "Distributor A's share of accounts receivable is 0.26 for the 2026-01-01..2026-06-30 context against 0.32 for 2025-01-01..2025-12-31. The Q1 10-Q printed 0.28 and the 10-K printed 0.32 / 0.31 for 2025 / 2024",
  "account": "receivables concentration, distributor A",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.26\"",
  "paragraph_id": "0001262039-26-000021:facts:ConcentrationRiskPercentage1:2026-01-01..2026-06-30:srt:MajorCustomersAxis=ftnt:DistributorAMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_distributor_b_receivables_share_note",
  "what_changed": "Distributor B's share of accounts receivable is 0.13 against 0.12 for 2025. A disclosure change: the Q2 10-Q tags receivables concentration for distributors A and B only. It carries no distributor C receivables row, whereas the Q1 10-Q printed 0.11 for C and the 10-K printed 0.09 / 0.10 for C for 2025 / 2024",
  "account": "receivables concentration, distributor B (and the absent distributor C row)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.13\"",
  "paragraph_id": "0001262039-26-000021:facts:ConcentrationRiskPercentage1:2026-01-01..2026-06-30:srt:MajorCustomersAxis=ftnt:DistributorBMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_americas_revenue_note",
  "what_changed": "Americas revenue is 808200000 for the quarter against 658800000, and 1548000000 against 1288600000 for six months. Within it, Other Americas is 228500000 against 185800000",
  "account": "revenue, Americas",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"808200000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AmericasMember" }
```

```json
{ "id": "revenue_recognition_emea_revenue_note",
  "what_changed": "EMEA revenue is 871700000 for the quarter against 667100000, and 1656500000 against 1295500000 for six months. EMEA is the largest region in both quarters as printed",
  "account": "revenue, EMEA",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"871700000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "revenue_recognition_asia_pacific_revenue_note",
  "what_changed": "Asia Pacific revenue is 368000000.0 for the quarter against 304100000, and 693000000.0 against 585600000 for six months",
  "account": "revenue, Asia Pacific",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"368000000.0\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "revenue_recognition_united_states_revenue_note",
  "what_changed": "United States revenue is 579700000 for the quarter against 473000000.0, and 1106200000 against 928400000 for six months",
  "account": "revenue, United States",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"579700000\"",
  "paragraph_id": "0001262039-26-000021:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:US" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_note",
  "what_changed": "The inventory valuation reserve is 122800000 at 2026-06-30 against 137500000 at 2025-12-31. The Q1 10-Q printed 125300000 at 2026-03-31, so the reserve is lower at each filing this year, while net inventory is higher (426300000 against 399500000). The trend table places the reserve ratio lowest of 6 filled quarters",
  "account": "inventory valuation reserve",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"122800000\"",
  "paragraph_id": "0001262039-26-000021:facts:InventoryValuationReserves:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_note",
  "what_changed": "Inventory write-down is tagged 0 for the quarter, and also 0 for six months and for both 2025 comparatives. The inventory firm purchase commitment loss is tagged 0 for the quarter and six months. The Q1 10-Q also tagged a 0 write-down. So the reserve went down with no write-down expense tagged",
  "account": "inventory write-down",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001262039-26-000021:facts:InventoryWriteDown:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_finished_goods_inventory_note",
  "what_changed": "Finished goods, net of reserves, are 353600000 at 2026-06-30 against 334600000. Raw materials are 70300000 against 61900000; work in process is 2400000 against 3000000.0",
  "account": "finished goods inventory",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"353600000\"",
  "paragraph_id": "0001262039-26-000021:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_property_and_equipment_gross_note",
  "what_changed": "Gross property and equipment is 2227000000 at 2026-06-30 against 2100900000. Computer equipment is 400200000 against 341000000.0; construction in progress 86500000 against 74600000; evaluation units 18500000 against 24100000; buildings 974800000 against 974000000.0. Accumulated depreciation is 527500000 against 481900000",
  "account": "property and equipment, gross",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2227000000\"",
  "paragraph_id": "0001262039-26-000021:facts:PropertyPlantAndEquipmentGross:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_land_holdings_note",
  "what_changed": "Land is 649000000.0 at 2026-06-30 against 592400000. Real-estate asset acquisitions tagged for six months are land 59500000 and building 2600000; PaymentsToAcquireProductiveAssets for six months is 62100000. The 10-K's subsequent-events note had named a Sunnyvale land purchase of 47000000.0",
  "account": "land",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"649000000.0\"",
  "paragraph_id": "0001262039-26-000021:facts:PropertyPlantAndEquipmentGross:2026-06-30:us-gaap:PropertyPlantAndEquipmentByTypeAxis=us-gaap:LandMember" }
```

```json
{ "id": "earnings_quality_depreciation_note",
  "what_changed": "Depreciation is 31500000 for the quarter against 25100000, and 61000000.0 against 49100000 for six months",
  "account": "depreciation",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"31500000\"",
  "paragraph_id": "0001262039-26-000021:facts:Depreciation:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_note",
  "what_changed": "Goodwill is 257400000 at 2026-06-30, the same as the 257400000 at 2025-12-31. Goodwill impairment loss is tagged 0 for six months 2026 and 2025",
  "account": "goodwill",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"257400000\"",
  "paragraph_id": "0001262039-26-000021:facts:Goodwill:2026-06-30" }
```

```json
{ "id": "earnings_quality_intangible_amortization_note",
  "what_changed": "Amortization of intangible assets is 9900000 for the quarter against 13200000, and 20200000 against 25000000.0 for six months. Net finite-lived intangibles are 77100000 against 97300000. Expected amortization is 17000000.0 for the rest of 2026, then 27500000, 20000000.0, 9300000 and 1000000.0 in later years as tagged",
  "account": "intangible asset amortization",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"9900000\"",
  "paragraph_id": "0001262039-26-000021:facts:AmortizationOfIntangibleAssets:2026-04-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_linksys_acquisition_note",
  "what_changed": "The Q2 10-Q repeats the Linksys acquisition of 2025-01-31: a bargain purchase gain of 39900000, a gain on the prior equity-method interest of 10800000, payments of 20800000, total consideration of 42300000, and 1 for voting interest acquired. This sits in the six-month 2025 comparative only; the 2026 periods carry no such rows",
  "account": "business combination, Linksys",
  "expected_direction": "none",
  "horizon": "six-month comparisons against 2025",
  "quote": "\"value\": \"39900000\"",
  "paragraph_id": "0001262039-26-000021:facts:BusinessCombinationBargainPurchaseGainRecognizedAmount:2025-01-31..2025-01-31:us-gaap:BusinessAcquisitionAxis=ftnt:LinksysMember" }
```

```json
{ "id": "liquidity_and_capital_senior_notes_repayment_note",
  "what_changed": "The 2026 senior notes (1.0% stated rate) were repaid on 2026-03-15 at 500000000.0. Their carrying amount is 0 at 2026-06-30 against 500000000.0. Total notes carrying amount is 500000000.0 against 1000000000; only the 2031 notes (2.2% stated, 0.023 effective) remain",
  "account": "senior notes",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"500000000.0\"",
  "paragraph_id": "0001262039-26-000021:facts:RepaymentsOfSeniorDebt:2026-03-15..2026-03-15:us-gaap:DebtInstrumentAxis=ftnt:A2026SeniorNotesMember,us-gaap:LongtermDebtTypeAxis=us-gaap:SeniorNotesMember" }
```

```json
{ "id": "liquidity_and_capital_senior_notes_fair_value_note",
  "what_changed": "The Level 2 fair value of the senior notes is 449500000 at 2026-06-30, against a carrying principal of 500000000.0 for the remaining 2031 notes. I have no prior-period fair value in my notes, so it is insufficient for a comparison",
  "account": "senior notes fair value",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"449500000\"",
  "paragraph_id": "0001262039-26-000021:facts:LongTermDebtFairValue:2026-06-30:us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel2Member,us-gaap:LongtermDebtTypeAxis=us-gaap:SeniorNotesMember" }
```

```json
{ "id": "earnings_quality_senior_notes_interest_expense_note",
  "what_changed": "Interest expense on the senior notes is 2900000 for the quarter against 4500000, and 7100000 against 9000000.0 for six months. Interest capitalized is tagged 0. Interest payable is 3200000 against 4700000",
  "account": "interest expense on senior notes",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2900000\"",
  "paragraph_id": "0001262039-26-000021:facts:InterestExpenseDebt:2026-04-01..2026-06-30:us-gaap:LongtermDebtTypeAxis=us-gaap:SeniorNotesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_other_commitments_note",
  "what_changed": "Other commitments are 110900000 at 2026-06-30. The Q1 10-Q printed 127800000 at 2026-03-31",
  "account": "other commitments",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"110900000\"",
  "paragraph_id": "0001262039-26-000021:facts:OtherCommitment:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_securities_litigation_accrual_note",
  "what_changed": "The Q2 10-Q tags a loss contingency accrual of 0 at 2026-06-30 for a litigation member naming Oklahoma Firefighters Pension and Retirement System v. Fortinet Inc. et al and State of Rhode Island Office of the General Treasurer v. Fortinet Inc. et al. Unlike the Alorica matter, this member has no 2025-12-31 row in the Q2 10-Q. A zero accrual is a recorded amount, not an estimate of exposure; no other amount for this case exists in my input",
  "account": "loss contingency accrual, securities litigation",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001262039-26-000021:facts:LossContingencyAccrualAtCarryingValue:2026-06-30:srt:LitigationCaseAxis=ftnt:OklahomaFirefightersPensionAndRetirementSystemV.FortinetInc.EtAlAndStateOfRhodeIslandOfficeOfTheGeneralTreasurerV.FortinetInc.EtAlMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_alorica_litigation_accrual_note",
  "what_changed": "The loss contingency accrual for Alorica v. Fortinet is tagged 0 at 2026-06-30 and 0 at 2025-12-31",
  "account": "loss contingency accrual, Alorica",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001262039-26-000021:facts:LossContingencyAccrualAtCarryingValue:2026-06-30:srt:LitigationCaseAxis=ftnt:AloricaV.FortinetMember" }
```

```json
{ "id": "earnings_quality_stock_based_compensation_note",
  "what_changed": "Stock-based compensation expense is 80800000 for the quarter against 69900000, and 154000000.0 against 136800000 for six months. By line, sales and marketing is 36700000 against 29700000 and research and development 26900000 against 25100000. The release's six-month cash-flow add-back prints 151.8",
  "account": "stock-based compensation expense",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"80800000\"",
  "paragraph_id": "0001262039-26-000021:facts:AllocatedShareBasedCompensationExpense:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_unrecognized_restricted_stock_unit_cost_note",
  "what_changed": "Unrecognized compensation cost is 659800000 for RSUs at 2026-06-30, 56400000 for options and 25100000 for performance shares. I have no prior-period value in my notes, so it is insufficient for a comparison",
  "account": "unrecognized stock compensation cost",
  "expected_direction": "none",
  "horizon": "future periods",
  "quote": "\"value\": \"659800000\"",
  "paragraph_id": "0001262039-26-000021:facts:EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized:2026-06-30:us-gaap:AwardTypeAxis=us-gaap:RestrictedStockUnitsRSUMember" }
```

```json
{ "id": "earnings_quality_option_exercise_tax_benefit_note",
  "what_changed": "The tax benefit from stock-based compensation exercises is 17700000 for the quarter against 15300000, and 33700000 against 30000000.0 for six months",
  "account": "tax benefit from share-based compensation",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"17700000\"",
  "paragraph_id": "0001262039-26-000021:facts:EmployeeServiceShareBasedCompensationTaxBenefitFromExerciseOfStockOptions:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_repurchase_program_note",
  "what_changed": "Repurchases under the programme are 972800000 for six months, covering 12500000 shares, with excise tax of 6700000. The equity statement prints 401100000 for the second quarter of 2025",
  "account": "share repurchase programme",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"972800000\"",
  "paragraph_id": "0001262039-26-000021:facts:StockRepurchasedAndRetiredDuringPeriodValue:2026-01-01..2026-06-30:srt:ShareRepurchaseProgramAxis=ftnt:ShareRepurchaseProgramMember" }
```

```json
{ "id": "liquidity_and_capital_remaining_repurchase_authorization_note",
  "what_changed": "The remaining repurchase authorization is 765800000 at 2026-06-30. The Q1 10-Q printed 911700000 at 2026-03-31, and 765800000 at 2026-05-07 as a subsequent event. The 10-K printed 1270000000 at 2026-02-24. The 2026-06-30 value reads the same as the Q1 10-Q's 2026-05-07 value",
  "account": "remaining repurchase authorization",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"765800000\"",
  "paragraph_id": "0001262039-26-000021:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-06-30:srt:ShareRepurchaseProgramAxis=ftnt:ShareRepurchaseProgramMember" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_note",
  "what_changed": "The effective tax rate is 0.16 for the quarter against 0.15, and 0.17 against 0.17 for six months. The Q1 10-Q printed 0.19 for its quarter. The release adjusts non-GAAP results to 18%",
  "account": "effective income tax rate",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0.16\"",
  "paragraph_id": "0001262039-26-000021:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_foreign_derived_income_deduction_note",
  "what_changed": "The FDII amount in the rate reconciliation is 33900000 for the quarter against 25100000, and 68000000.0 against 50900000 for six months",
  "account": "foreign-derived intangible income deduction",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"33900000\"",
  "paragraph_id": "0001262039-26-000021:facts:EffectiveIncomeTaxRateReconciliationFdiiAmount:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_note",
  "what_changed": "Unrecognized tax benefits are 92400000 at 2026-06-30 against 90400000 at 2025-12-31; the Q1 10-Q printed 91700000. The portion that would affect the rate is 75200000. Accrued interest and penalties are 12600000 against 12500000",
  "account": "unrecognized tax benefits",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"92400000\"",
  "paragraph_id": "0001262039-26-000021:facts:UnrecognizedTaxBenefits:2026-06-30" }
```

```json
{ "id": "earnings_quality_segment_other_items_note",
  "what_changed": "The segment 'other item' amount for the single reportable segment is -33300000 for the quarter against -60500000, and -111200000 against -142900000 for six months; it is smaller in both. The 10-Q tags 1 reportable and 1 operating segment",
  "account": "segment other items",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"-33300000\"",
  "paragraph_id": "0001262039-26-000021:facts:SegmentReportingOtherItemAmount:2026-04-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=ftnt:ReportableSegmentMember" }
```

```json
{ "id": "earnings_quality_segment_sales_commissions_note",
  "what_changed": "Segment sales commissions and fees are 131300000 for the quarter against 108300000, and 252800000 against 211300000 for six months",
  "account": "segment sales commissions",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"131300000\"",
  "paragraph_id": "0001262039-26-000021:facts:SalesCommissionsAndFees:2026-04-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=ftnt:ReportableSegmentMember" }
```

```json
{ "id": "liquidity_and_capital_equity_securities_fair_value_note",
  "what_changed": "Equity securities measured at fair value through net income are 34500000 at 2026-06-30 against 98200000 at 2025-12-31. The release prints six-month sales of investments of 118.4 against 5.7",
  "account": "equity securities at fair value",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"34500000\"",
  "paragraph_id": "0001262039-26-000021:facts:EquitySecuritiesFvNi:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_unrealized_losses_on_debt_securities_note",
  "what_changed": "Gross unrealized losses on available-for-sale debt securities are 2900000 at 2026-06-30 against 100000 at 2025-12-31. Quarterly other comprehensive income on securities is -1400000, against -300000 for the second quarter of 2025",
  "account": "unrealized losses on available-for-sale debt securities",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2900000\"",
  "paragraph_id": "0001262039-26-000021:facts:AvailableForSaleDebtSecuritiesAccumulatedGrossUnrealizedLossBeforeTax:2026-06-30" }
```
