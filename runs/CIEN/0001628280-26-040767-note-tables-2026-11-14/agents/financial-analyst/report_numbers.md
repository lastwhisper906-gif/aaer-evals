<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# Ciena — numbers report for the quarterly report for the second quarter of fiscal 2026 (quarter ended May 2, 2026, filed June 4, 2026)

What my input holds, and what it does not:

- My directory holds the earnings release (furnished June 4, 2026), the trend table, the numeric facts, and the prior-flags file. Nothing in it is a price, a return, short interest, another company's file, a prior probability or an outcome window.
- The prior-flags file says no earlier run is on record. There are no flags, explanations or outcomes to carry forward.
- **No articulation checks, restatement traces or fourth-quarter derivation exist in my input.** The numbers file has only four top-level keys: the ticker, the cutoff, the list of documents, and the facts. So no articulation gap and no restated prior value is reported below. The facts carry a field naming a later filing that re-reported the same element and date (`superseded_by`). That field records a re-presentation, not that the value changed. One example is reported as an item.
- **Periods the record does not reach.** Two quarters have no cells at all: the fourth quarter of fiscal 2025 (ending around November 1, 2025) and the fourth quarter of fiscal 2024 (ending around November 2, 2024). The reason the table gives for both: no quarter ending within 20 days of the target date is in the companyfacts record. The commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the annual report states the year and the three quarterly reports state the first three quarters. So it is derived by the project's fourth-quarter script, whose output is not in my input. As a result, the first quarter of fiscal 2026 and the first quarter of fiscal 2025 have no prior-quarter change in the table.
- **The research-and-development capitalisation baseline** prints no paragraph id on its block, so I cannot quote it and write no item from it. Its development-cost input is missing in every year. The reason given: the companyfacts record does not tag the capitalised software additions element in any period. For fiscal 2025 the block prints earnings with research and development capitalised of 329813800.0 and book value with it capitalised of 4999180600.0. I note these and draw nothing from them.
- **How the table's periods are built.** The table is anchored on May 2, 2026. Fiscal 2024 spans 371 days in the table; fiscal 2025 and the other years span 364. The day-based ratios use each period's own day count.
- **Where some inputs come from.** For the second quarter of fiscal 2025, revenue and cost of goods sold come from the comparative column of the current quarterly report, while receivables and inventory come from the report filed June 5, 2025. The same element sits under each, so this is not a change of tag.
- **What `expected_direction` means here.** It is the direction I expect the named account to move over the stated horizon, based only on my input. It is "none" wherever the input gives no forward basis. Only the release's guidance gives one.

## Seen in the statements

**From the trend table — the latest quarter (the second quarter of fiscal 2026)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient. The accruals ratio (net income less operating cash flow, over total assets) has no value for the second quarter of fiscal 2026. The record holds the company's operating cash flow but no three-month figure for the quarter ended May 2, 2026. The quarterly report's cash flow statement covers the six months ended May 2, 2026; that six-month figure is reported below. No change against the first quarter of fiscal 2026 or the second quarter of fiscal 2025 is printed, and I compute none.",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-02-01..2026-05-02: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "The allowance for doubtful accounts over gross receivables is 0.010342535369120387 at May 2, 2026 (allowance 11000000; net receivables 1052569000). The table prints a change of -0.001102292386221896 against the first quarter of fiscal 2026. Against the second quarter of fiscal 2025 it prints a change of negative 8.744593141313782 times ten to the power of minus five (the table writes it in exponent form). The value is the third lowest of the six filled quarters. Two quarters of the eight-quarter window are missing, so this is thin ground for a trend claim. The quarterly cells use the plain allowance element, while the annual cells use the element for the current allowance (item below).",
  "account": "allowance for doubtful accounts over gross accounts receivable",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "Current contract liabilities over the quarter's revenue is 0.1517629599825305 (contract liabilities 238380000 at May 2, 2026; revenue 1570739000). The change is -0.05174751833555685 against the first quarter of fiscal 2026 and -0.045269933457078415 against the second quarter of fiscal 2025. It is the lowest of the six filled quarters. The first quarter of fiscal 2026 was the highest (item below). The balance itself is lower at May 2, 2026 than the 290418000 at January 31, 2026, while revenue is higher than the first quarter's 1427042000. The ratio counts only the current portion; long-term deferred revenue is outside it.",
  "account": "current contract liabilities (deferred revenue) over quarterly revenue",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "Days sales of inventory (net inventory over the quarter's cost of goods and services sold, times the period's 91 days) is 83.678266803915 (inventory 808447000 at May 2, 2026; cost of goods and services sold 879185000). The change is -12.351402999284417 against the first quarter of fiscal 2026 and -34.53709335298505 against the second quarter of fiscal 2025. It is the lowest of the six filled quarters. Net inventory at May 2, 2026 is lower than at any other quarter-end in the table.",
  "account": "days sales of inventory",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_of_inventory:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "Days sales outstanding (period-end net receivables over the quarter's revenue, times 91 days) is 60.98007307388433 (receivables 1052569000; revenue 1570739000). The change is -0.7098617703599146 against the first quarter of fiscal 2026 and -14.171683155476217 against the second quarter of fiscal 2025. It is the lowest of the six filled quarters. Net receivables at May 2, 2026 are higher than the 967408000 at January 31, 2026, yet the ratio is lower. The release reports an average DSO of 71 on its own basis (item below).",
  "account": "days sales outstanding",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_outstanding:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "Gross margin is 0.44027301798707486 (revenue 1570739000; cost of goods and services sold 879185000). The change is 0.0019397383779253263 against the first quarter of fiscal 2026 and 0.038064252916614305 against the second quarter of fiscal 2025. It is the highest of the six filled quarters. The release prints a GAAP gross margin of 44.0% and an adjusted margin of 44.9% for the quarter. By contrast, the latest annual cell (fiscal 2025) is the lowest of the five filled years.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:gross_margin:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
  "what_changed": "Inventory valuation reserves over net inventory is 0.19387170711252563 at May 2, 2026 (reserves 156735000; net inventory 808447000). The change is 0.021326150890952078 against the first quarter of fiscal 2026 and 0.05888658714583128 against the second quarter of fiscal 2025. It is the highest of the six filled quarters. The oldest quarter in the window, the third quarter of fiscal 2024, is the lowest (item below). The reserve balance is higher at each successive quarter-end in the table: 69693000, 108727000, 118021000, 121477000, 145943000, then 156735000. Over the same span, net inventory at May 2, 2026 is the lowest of those quarter-ends. The six-month inventory write-down provision is reported below.",
  "account": "inventory valuation reserves over net inventory",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient. The gap between non-GAAP and GAAP net income has no value: the record carries no non-GAAP measure. The release prints adjusted net income of 240,199 thousand against GAAP net income of 218,220 thousand for the quarter (item below). The table computed no gap from these and I compute none.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-040767:trends:non_gaap_gap:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "Net receivables over the quarter's revenue is 0.670110693119608 (receivables 1052569000; revenue 1570739000). The change is -0.0078006787951638845 against the first quarter of fiscal 2026 and -0.15573278192831008 against the second quarter of fiscal 2025. It is the lowest of the six filled quarters.",
  "account": "accounts receivable, net, over quarterly revenue",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:receivables_over_revenue:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "The share of total assets that is neither cash nor property and equipment is 0.7532543117757928 at May 2, 2026 (assets 6039449000; cash and cash equivalents 1045126000; property, equipment and finance-lease right-of-use assets 445082000). The change is 0.018216273529990112 against the first quarter of fiscal 2026 and -0.017193473364804146 against the second quarter of fiscal 2025. It is the third lowest of the six filled quarters. Cash in this formula excludes short-term and long-term investments; the release shows long-term investments moving (item below).",
  "account": "soft assets over total assets",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the first quarter of fiscal 2026 and the second quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:soft_asset_share:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. None of the three warranty-accrual elements is tagged in any period, so the warranty reserve ratio is empty in every quarter and every year of the table. The table says the record cannot tell whether the company does not tag the accrual or states it only by segment. A six-month warranty provision is tagged under the product warranty expense element (item below). That is an expense, not the accrual balance the ratio needs.",
  "account": "warranty accrual over revenue",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period.",
  "paragraph_id": "0001628280-26-040767:trends:warranty_reserve_ratio:2026-02-01..2026-05-02" }
```

**From the trend table — the latest year (fiscal 2025, November 3, 2024 to November 1, 2025)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "For fiscal 2025 the accruals ratio is -0.11641837464940465 (net income 123338000; operating cash flow 806093000; total assets at November 1, 2025 5864667000). The change against fiscal 2024 is -0.04009320563361991. It is the lowest of the five filled years: of all five years, fiscal 2025 has operating cash flow furthest above net income relative to assets. The quarterly version of this ratio is filled in only two quarters (item below).",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "The allowance for doubtful accounts over gross receivables is 0.011358893206952308 at November 1, 2025. The allowance is 11212000, tagged under the current-allowance element; receivables are 975856000. The change against fiscal 2024 is 0.0006019553631086399. It is the second lowest of the five filled years.",
  "account": "allowance for doubtful accounts over gross accounts receivable",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "Current contract liabilities over annual revenue is 0.043806624038920584 for fiscal 2025 (contract liabilities 208936000 at November 1, 2025; revenue 4769507000). The change against fiscal 2024 is 0.004857495094760564. It is the highest of the five filled years. The denominator is a full year's revenue, so this cell cannot be compared with the quarterly cells.",
  "account": "current contract liabilities (deferred revenue) over annual revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "Days sales of inventory is 108.78630827717673 for fiscal 2025 (inventory 826235000 at November 1, 2025; cost of goods and services sold 2764590000; 364 days). The change against fiscal 2024 is -23.81984804218861. It is the second lowest of the five filled years. Fiscal 2021 is the lowest at 71.75019816137842.",
  "account": "days sales of inventory",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_of_inventory:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "Days sales outstanding is 74.4755346831444 for fiscal 2025 (receivables 975856000 at November 1, 2025; revenue 4769507000; 364 days). The change against fiscal 2024 is -9.482937329617883. It is the lowest of the five filled years.",
  "account": "days sales outstanding",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_outstanding:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "Gross margin is 0.42036147551518427 for fiscal 2025 (revenue 4769507000; cost of goods and services sold 2764590000). The change against fiscal 2024 is -0.007934732038823167. It is the lowest of the five filled years; fiscal 2021 is the highest at 0.47559494283400594. The quarterly cell for the second quarter of fiscal 2026 is the highest of its six quarters.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:gross_margin:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "Inventory valuation reserves over net inventory is 0.1566237208542364 at November 1, 2025 (reserves 129408000; net inventory 826235000). The change against fiscal 2024 is 0.025993441610425216. It is the highest of the five filled years. Fiscal 2022 is the lowest at 0.03811646403937765, and fiscal 2023 is 0.0475839282553543.",
  "account": "inventory valuation reserves over net inventory",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient. The record carries no non-GAAP measure, so the gap between non-GAAP and GAAP net income is empty for fiscal 2025 and for every other year of the table. No fiscal 2025 adjusted figure exists in my input.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-040767:trends:non_gaap_gap:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "Net receivables over annual revenue is 0.20460311726138572 for fiscal 2025 (receivables 975856000; revenue 4769507000). The change against fiscal 2024 is -0.021700041802663578. It is the lowest of the five filled years.",
  "account": "accounts receivable, net, over annual revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:receivables_over_revenue:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "The soft-asset share is 0.7478576362477187 at November 1, 2025 (assets 5864667000; cash and cash equivalents 1091952000; property, equipment and finance-lease right-of-use assets 386779000). The change against fiscal 2024 is -0.026560201225915625. It is the second lowest of the five filled years.",
  "account": "soft assets over total assets",
  "expected_direction": "none",
  "horizon": "fiscal 2025, against fiscal 2024",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:soft_asset_share:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. No warranty-accrual element is tagged in any period, so the warranty reserve ratio is empty for fiscal 2025 and for all five years.",
  "account": "warranty accrual over revenue",
  "expected_direction": "none",
  "horizon": "fiscal 2025",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period.",
  "paragraph_id": "0001628280-26-040767:trends:warranty_reserve_ratio:2024-11-03..2025-11-01" }
```

**From the trend table — other cells that bear on the latest readings**

```json
{ "id": "earnings_quality_accruals_over_total_assets_only_two_quarters_filled",
  "what_changed": "insufficient for a trend. The quarterly accruals ratio is filled only in the first quarter of fiscal 2026 (-0.013129206825313936) and the first quarter of fiscal 2025. The first quarter of fiscal 2026 is the lower of the two. Its change against the first quarter of fiscal 2025 is -0.002515167676590345. Two points support no trend claim.",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2026, against the first quarter of fiscal 2025",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2025-11-02..2026-01-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_peak_before_drop",
  "what_changed": "In the first quarter of fiscal 2026, current contract liabilities over the quarter's revenue was 0.20351047831808736 (contract liabilities 290418000 at January 31, 2026; revenue 1427042000). That was the highest of the six filled quarters. One quarter later the same ratio is the lowest of the six. The swing from top to bottom took a single quarter.",
  "account": "current contract liabilities (deferred revenue) over quarterly revenue",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2026, against the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2025-11-02..2026-01-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_window_high",
  "what_changed": "The bad-debt reserve ratio was 0.011444827755342283 at January 31, 2026 (allowance 11200000; receivables 967408000), the highest of the six filled quarters. The latest quarter sits third lowest. The two quarters' values are close, and six points are thin for a trend claim.",
  "account": "allowance for doubtful accounts over gross accounts receivable",
  "expected_direction": "none",
  "horizon": "the first quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2025-11-02..2026-01-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_window_low",
  "what_changed": "At the start of the window, the third quarter of fiscal 2024 (quarter ended July 27, 2024), the inventory reserve ratio was 0.07434720967272207 (reserves 69693000; net inventory 937399000). That is the lowest of the six filled quarters. The ratio is the highest of the six in the latest quarter, so over the window it runs from the bottom to the top.",
  "account": "inventory valuation reserves over net inventory",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2024 through the second quarter of fiscal 2026",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2024-04-28..2024-07-27" }
```

**Change of tag**

```json
{ "id": "articulation_and_the_filed_history_bad_debt_allowance_tag_differs_annual_from_quarterly",
  "what_changed": "The allowance for doubtful accounts rests on a different element in the annual cells than in the quarterly cells. All five years use the current-allowance element, AllowanceForDoubtfulAccountsReceivableCurrent, with unrounded values such as 11212000 at November 1, 2025. All six filled quarters use the plain allowance element, AllowanceForDoubtfulAccountsReceivable, with values such as 11000000 at May 2, 2026 and 11200000 at January 31, 2026. So the annual and quarterly bad-debt ratios are not built on the same concept. My input does not say whether the two elements measure the same balance.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "fiscal 2021 through fiscal 2025, against the quarters from the third quarter of fiscal 2024 through the second quarter of fiscal 2026",
  "quote": "\"tag\": \"AllowanceForDoubtfulAccountsReceivableCurrent\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2024-11-03..2025-11-01" }
```

**Filed history**

```json
{ "id": "articulation_and_the_filed_history_annual_receivables_carried_forward_unchanged",
  "what_changed": "The annual report's fact for net receivables at November 1, 2025 is marked as superseded by the quarterly report filed June 4, 2026. The trend table takes its fiscal 2025 receivables from that later report, which prints 975856000 for the same date — the same value as the annual report. Many of the annual report's year-end balances carry the same mark. My input holds no restatement trace, so this records a re-presentation, not a restated value.",
  "account": "accounts receivable, net",
  "expected_direction": "none",
  "horizon": "November 1, 2025",
  "quote": "\"superseded_by\": \"0001628280-26-040767\"",
  "paragraph_id": "0001628280-25-056698:facts:AccountsReceivableNetCurrent:2025-11-01" }
```

**From the numeric facts — the quarterly report filed June 4, 2026**

```json
{ "id": "earnings_quality_operating_cash_flow_left_out_of_accruals_ratio",
  "what_changed": "Net cash from operating activities is 487347000 for the six months ended May 2, 2026, against 260669000 for the six months ended May 3, 2025. Net income for the same six months is 368503000, against 53541000. Operating cash flow is above net income in both half-years. This six-month figure is the only operating cash flow the current report states, which is why the table's quarterly accruals ratio is empty. I compute no accrual or quarterly cash flow from it.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"487347000\"",
  "paragraph_id": "0001628280-26-040767:facts:NetCashProvidedByUsedInOperatingActivities:2025-11-02..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_provision",
  "what_changed": "The provision for inventory excess and obsolescence, tagged as an inventory write-down, is 42481000 for the six months ended May 2, 2026, against 23431000 a year earlier. It sits alongside an inventory reserve ratio at the top of its quarterly and annual history.",
  "account": "provision for inventory excess and obsolescence",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"42481000\"",
  "paragraph_id": "0001628280-26-040767:facts:InventoryWriteDown:2025-11-02..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_provision_tagged_as_expense",
  "what_changed": "The provision for warranty, tagged as product warranty expense, is 16685000 for the six months ended May 2, 2026, against 10714000 a year earlier. The warranty accrual balance itself is not tagged anywhere in the record, so this expense is the only warranty figure in my input.",
  "account": "provision for warranty",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"16685000\"",
  "paragraph_id": "0001628280-26-040767:facts:ProductWarrantyExpense:2025-11-02..2026-05-02" }
```

```json
{ "id": "revenue_recognition_receivables_build_in_cash_flow",
  "what_changed": "The increase in accounts receivable in the cash flow statement is 71555000 for the six months ended May 2, 2026, against 20857000 a year earlier. The release prints both as uses of cash, (71,555) and (20,857) thousand. Net receivables are 1052569000 at May 2, 2026, against 975856000 at November 1, 2025.",
  "account": "change in accounts receivable",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"71555000\"",
  "paragraph_id": "0001628280-26-040767:facts:IncreaseDecreaseInAccountsReceivable:2025-11-02..2026-05-02" }
```

```json
{ "id": "revenue_recognition_contract_liability_growth_in_cash_flow",
  "what_changed": "The increase in contract liabilities (deferred revenue) in the cash flow statement is 35442000 for the six months ended May 2, 2026, against 66493000 a year earlier. Deferred revenue added less cash than a year earlier, while the table's contract-liability ratio is at its quarterly low.",
  "account": "change in contract liabilities",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"35442000\"",
  "paragraph_id": "0001628280-26-040767:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-11-02..2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_prepaid_and_other_assets_using_cash",
  "what_changed": "The change in prepaid expenses and other assets is 34047000 for the six months ended May 2, 2026; the release prints it as a use of cash, (34,047) thousand. A year earlier the same element is -84144000, which the release prints as a source of cash, 84,144 thousand. On the balance sheet, prepaid expenses and other are 504,314 thousand at May 2, 2026, against 455,316 thousand at November 1, 2025.",
  "account": "prepaid expenses and other assets",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"34047000\"",
  "paragraph_id": "0001628280-26-040767:facts:IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets:2025-11-02..2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_capital_spending",
  "what_changed": "Payments for equipment, furniture and fixtures are 114933000 for the six months ended May 2, 2026, against 55622000 a year earlier. The release's balance sheet shows equipment, building, furniture and fixtures, net, at 445,082 thousand at May 2, 2026, against 386,779 thousand at November 1, 2025.",
  "account": "capital expenditures",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "\"value\": \"114933000\"",
  "paragraph_id": "0001628280-26-040767:facts:PaymentsToAcquirePropertyPlantAndEquipment:2025-11-02..2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_purchase_obligations",
  "what_changed": "Purchase obligations are 2800000000 at May 2, 2026. The quarterly report filed March 5, 2026 prints 1900000000 at January 31, 2026, so the obligation is larger one quarter later. Both facts are stated to the hundred million. My input gives no breakdown by supplier or timing.",
  "account": "purchase obligations",
  "expected_direction": "none",
  "horizon": "May 2, 2026, against January 31, 2026",
  "quote": "\"value\": \"2800000000\"",
  "paragraph_id": "0001628280-26-040767:facts:PurchaseObligation:2026-05-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_share_repurchases_after_balance_sheet",
  "what_changed": "As a subsequent event, the company repurchased 44628 shares for 25100000 between May 3 and May 29, 2026. It reports a remaining authorized repurchase amount of 481600000 at May 29, 2026. The prior quarterly report states the same kind of event: 83510 shares for 25100000 between February 1 and February 27, 2026, with 564700000 remaining at February 27, 2026.",
  "account": "share repurchases after the balance sheet date",
  "expected_direction": "none",
  "horizon": "May 3, 2026 to May 29, 2026",
  "quote": "\"value\": \"25100000\"",
  "paragraph_id": "0001628280-26-040767:facts:StockRepurchasedDuringPeriodValue:2026-05-03..2026-05-29:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

**From the earnings release (furnished June 4, 2026)**

```json
{ "id": "results_against_expectations_quarterly_revenue_guidance",
  "what_changed": "The release guides revenue for the third quarter of fiscal 2026 at $1.625 billion plus or minus $50 million. The midpoint is above the second quarter's revenue of $1,570.7 million printed in the same release. My input holds no consensus estimate or earlier guidance for the quarter.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "Providing revenue guidance for fiscal third quarter 2026 of $1.625 billion plus or minus $50 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:8" }
```

```json
{ "id": "results_against_expectations_annual_revenue_guidance_raised",
  "what_changed": "The release says it is raising fiscal 2026 revenue guidance to $6.3 billion plus or minus $100 million. It prints the midpoint as a 32% increase on fiscal 2025; the table holds fiscal 2025 revenue of 4769507000. The guidance being replaced is not in my input, so the size of the raise does not exist here.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "fiscal 2026",
  "quote": "Raising revenue guidance for fiscal year 2026 to $6.3 billion plus or minus $100 million, a 32% increase YoY at the midpoint",
  "paragraph_id": "0001628280-26-040614:8k_2_02:9" }
```

```json
{ "id": "results_against_expectations_quarterly_adjusted_gross_margin_guidance",
  "what_changed": "Adjusted gross margin for the third quarter of fiscal 2026 is guided at 45% plus or minus 50 basis points. The midpoint is above the second quarter's adjusted gross margin of 44.9% in the same release. I do not compute the ends of the band.",
  "account": "adjusted (non-GAAP) gross margin",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "Adjusted (non-GAAP) gross margin in the range of 45% plus or minus 50 bps",
  "paragraph_id": "0001628280-26-040614:8k_2_02:24" }
```

```json
{ "id": "results_against_expectations_quarterly_adjusted_operating_expense_guidance",
  "what_changed": "Adjusted operating expense for the third quarter of fiscal 2026 is guided at $410 million plus or minus $10 million. The midpoint is above the second quarter's adjusted operating expense of $397.8 million (397,795 thousand in the reconciliation).",
  "account": "adjusted (non-GAAP) operating expense",
  "expected_direction": "up",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "Adjusted (non-GAAP) operating expense in the range of $410 million plus or minus $10 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:25" }
```

```json
{ "id": "results_against_expectations_quarterly_adjusted_operating_margin_guidance",
  "what_changed": "Adjusted operating margin for the third quarter of fiscal 2026 is guided between 19% and 20%. The second quarter's adjusted operating margin of 19.5% lies inside that range.",
  "account": "adjusted (non-GAAP) operating margin",
  "expected_direction": "none",
  "horizon": "the third quarter of fiscal 2026",
  "quote": "Adjusted (non-GAAP) operating margin between 19% and 20%",
  "paragraph_id": "0001628280-26-040614:8k_2_02:26" }
```

```json
{ "id": "results_against_expectations_annual_adjusted_gross_margin_guidance",
  "what_changed": "Fiscal 2026 adjusted gross margin is guided between 44.5% and 45%. The second quarter's adjusted 44.9% lies inside that range. No fiscal 2025 adjusted gross margin exists in my input to compare with.",
  "account": "adjusted (non-GAAP) gross margin",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "Adjusted (non-GAAP) gross margin between 44.5% and 45%",
  "paragraph_id": "0001628280-26-040614:8k_2_02:29" }
```

```json
{ "id": "results_against_expectations_annual_adjusted_operating_expense_guidance",
  "what_changed": "Fiscal 2026 adjusted operating expense is guided at $1.61 billion plus or minus $20 million. No fiscal 2025 adjusted operating expense exists in my input to compare with.",
  "account": "adjusted (non-GAAP) operating expense",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "Adjusted (non-GAAP) operating expense in the range of $1.61 billion plus or minus $20 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:30" }
```

```json
{ "id": "results_against_expectations_annual_adjusted_operating_margin_guidance",
  "what_changed": "Fiscal 2026 adjusted operating margin is guided at 19% plus or minus 50 basis points. The second quarter printed 19.5% adjusted. No fiscal 2025 adjusted operating margin exists in my input.",
  "account": "adjusted (non-GAAP) operating margin",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "Adjusted (non-GAAP) operating margin in the range of 19% plus or minus 50bps",
  "paragraph_id": "0001628280-26-040614:8k_2_02:31" }
```

```json
{ "id": "earnings_quality_gaap_and_adjusted_earnings_per_share",
  "what_changed": "Diluted earnings per share for the second quarter of fiscal 2026 is $1.49 GAAP and $1.64 adjusted. For the second quarter of fiscal 2025 it was $0.06 GAAP and $0.42 adjusted. In both quarters the adjusted figure is above the GAAP figure.",
  "account": "diluted earnings per share, GAAP and adjusted",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the second quarter of fiscal 2025",
  "quote": "$1.49 GAAP and $1.64 adjusted (non-GAAP) for the fiscal second quarter 2026, compared to $0.06 and $0.42 for fiscal second quarter 2025, respectively",
  "paragraph_id": "0001628280-26-040614:8k_2_02:17" }
```

```json
{ "id": "earnings_quality_adjusted_net_income_in_release_only",
  "what_changed": "The release's reconciliation prints adjusted net income of 240,199 thousand for the second quarter of fiscal 2026, against GAAP net income of 218,220 thousand. For the second quarter of fiscal 2025 the figures are 60,657 and 8,969 thousand. This is the non-GAAP measure the trend table could not find in the record. I do not compute the gap.",
  "account": "adjusted (non-GAAP) net income",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the second quarter of fiscal 2025",
  "quote": "| Adjusted (non-GAAP) net income |  | $ | 240,199 |  |  | $ | 60,657 |  |  |  |  |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:68" }
```

```json
{ "id": "structure_and_disclosure_changes_holdback_arrangement_adjustment",
  "what_changed": "The non-GAAP reconciliation has a new adjustment, the holdback arrangement: 2,411 thousand in the second quarter of fiscal 2026, and a dash for the second quarter of fiscal 2025. The release describes it as part of the merger consideration for Nubis Communications that is held back and treated as contingent compensation under GAAP. It is left out of adjusted operating expense, which is therefore lower by it, and added back to adjusted EBITDA, which is therefore higher by it.",
  "account": "holdback arrangement (acquisition-related contingent compensation)",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "Holdback arrangement - reflects a one-time holdback of a portion of the merger consideration otherwise payable at closing to certain key employee shareholders of Nubis Communications, Inc. who became employees of Ciena, which is treated as contingent compensation for GAAP reporting purposes.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:77" }
```

```json
{ "id": "estimates_and_discretion_non_gaap_tax_rate_lowered",
  "what_changed": "The rate assumed for the non-GAAP tax provision is 20% for the second quarter of fiscal 2026, against 22% for the second quarter of fiscal 2025. The reconciliation prints the non-GAAP tax provision as 60,050 thousand, against 17,108 thousand a year earlier. A lower assumed rate means a smaller non-GAAP provision for a given adjusted pre-tax income. I do not compute how much of adjusted net income this accounts for.",
  "account": "non-GAAP tax provision rate",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the second quarter of fiscal 2025",
  "quote": "utilizes a current, blended U.S. and foreign statutory annual tax rate of 20% for the second quarter of fiscal 2026 and 22% for the second quarter of fiscal 2025",
  "paragraph_id": "0001628280-26-040614:8k_2_02:78" }
```

```json
{ "id": "estimates_and_discretion_gaap_tax_provision",
  "what_changed": "The GAAP provision for income taxes is 12,840 thousand for the second quarter of fiscal 2026, against income before income taxes of 231,060 thousand. For the six months it is 43,672 thousand against 412,175 thousand. A year earlier the quarter shows 10,047 thousand against 19,016 thousand. The non-GAAP provision for the quarter is 60,050 thousand. My input holds no GAAP effective tax rate or explanation for the quarter, and I compute none.",
  "account": "provision for income taxes",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026 and the six months ended May 2, 2026",
  "quote": "| Provision for income taxes | 12,840 |  |  | 10,047 |  |  | 43,672 |  |  | 34,069 |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:55" }
```

```json
{ "id": "across_documents_release_average_days_sales_outstanding",
  "what_changed": "The release reports average days sales outstanding of 71 for the quarter. The trend table prints 60.98007307388433, built from period-end net receivables over the quarter's revenue times 91 days. The two are on different bases, and my input does not reconcile them. The release gives no prior-quarter average to compare with.",
  "account": "days sales outstanding",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "Average days' sales outstanding (DSOs) were 71.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:34" }
```

```json
{ "id": "across_documents_release_inventory_turns",
  "what_changed": "The release reports inventory turns of 3.6 for the quarter. The trend table prints days sales of inventory of 83.678266803915. These are different measures; my input does not reconcile them and I do not convert one into the other.",
  "account": "inventory turns",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "Inventory turns were 3.6.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:35" }
```

```json
{ "id": "earnings_quality_two_customers_concentration",
  "what_changed": "Two customers each accounted for 10% or more of the quarter's revenue, together 34.0%. My input holds no concentration figure for any earlier quarter to compare with.",
  "account": "revenue concentration in customers above ten percent",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "Two customers represented 10%-plus of revenue for a total of 34.0% of revenue.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:33" }
```


```json
{ "id": "earnings_quality_intangible_amortization_in_cost_of_goods",
  "what_changed": "In the gross profit reconciliation, amortization of intangible assets is 6,787 thousand in the second quarter of fiscal 2026, against 2,232 thousand a year earlier. In the operating expense reconciliation the same item is 3,713 thousand, against 6,545 thousand. So more of the amortization now sits in cost of goods sold. GAAP gross margin is at its quarterly high even so.",
  "account": "amortization of intangible assets in cost of goods sold",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026, against the second quarter of fiscal 2025",
  "quote": "| Amortization of intangible assets |  | 6,787 |  |  | 2,232 |  |  |  |  |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:68" }
```

```json
{ "id": "liquidity_and_capital_repurchase_program_buybacks",
  "what_changed": "The company repurchased about 0.2 million shares for $83.1 million in the quarter under its $1 billion program. The six-month cash flow shows repurchases under the program of 164,920 thousand, against 168,197 thousand a year earlier.",
  "account": "share repurchases under the repurchase program",
  "expected_direction": "none",
  "horizon": "the second quarter of fiscal 2026",
  "quote": "Repurchased approximately 0.2 million shares of common stock for an aggregate price of $83.1 million under the $1 billion share repurchase program.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:36" }
```

```json
{ "id": "liquidity_and_capital_tax_withholding_share_repurchases",
  "what_changed": "Shares repurchased for tax withholdings on the vesting of stock unit awards used 179,420 thousand of cash in the six months ended May 2, 2026, against 42,266 thousand a year earlier. The amount is larger than the six-month repurchases under the program. Additional paid-in capital is 5732496000 at May 2, 2026, against 5953057000 at November 1, 2025.",
  "account": "cash paid for tax withholding on vested stock awards",
  "expected_direction": "none",
  "horizon": "the six months ended May 2, 2026, against the six months ended May 3, 2025",
  "quote": "| Shares repurchased for tax withholdings on vesting of stock unit awards | (179,420) |  |  | (42,266) |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:67" }
```

```json
{ "id": "liquidity_and_capital_long_term_investments_increase",
  "what_changed": "Long-term investments are 200,106 thousand at May 2, 2026, against 57,142 thousand at November 1, 2025. Over the same dates, short-term investments are 157,708 against 216,148 thousand, and cash and cash equivalents are 1,045,126 against 1,091,952 thousand. Investment purchases in the six months were 226,731 thousand.",
  "account": "long-term investments",
  "expected_direction": "none",
  "horizon": "May 2, 2026, against November 1, 2025",
  "quote": "| Long-term investments | 200,106 |  |  | 57,142 |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:61" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_decline",
  "what_changed": "Accrued liabilities and other short-term obligations are 439,626 thousand at May 2, 2026, against 531,081 thousand at November 1, 2025. Accounts payable are 606,599 against 542,841 thousand. The six-month cash flow line for accounts payable, accruals and other obligations is a use of 27,945 thousand.",
  "account": "accrued liabilities and other short-term obligations",
  "expected_direction": "none",
  "horizon": "May 2, 2026, against November 1, 2025",
  "quote": "| Accrued liabilities and other short-term obligations | 439,626 |  |  | 531,081 |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:61" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_balance_sheet_movement",
  "what_changed": "Current deferred revenue is 238,380 thousand at May 2, 2026, against 208,936 thousand at November 1, 2025. That is higher than at the year-end but lower than the 290418000 the trend table holds for January 31, 2026. Long-term deferred revenue is 102,107 against 94,850 thousand.",
  "account": "deferred revenue",
  "expected_direction": "none",
  "horizon": "May 2, 2026, against November 1, 2025 and January 31, 2026",
  "quote": "| Deferred revenue | 238,380 |  |  | 208,936 |  |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:61" }
```

## Seen in the notes

None of the facts I read carries the marker for whether its element sat inside a note. Every fact I read has the same fields: an id, a paragraph id, the tag, prefix and namespace, the context and its reference, the unit, decimals, value, number, a nil flag, the form, the source accession and filing date, and sometimes `superseded_by`. That includes facts that plainly belong to note tables: segment revenue, fair-value hierarchy amounts, derivative notional amounts, segment goodwill and intangibles, purchase obligations, and the subsequent-event repurchases. I read the numbers file's layout, the primary-statement facts in full, and samples of its note-table facts.

Because the marker is absent, I cannot tell which facts came from a note, and I place no item here. The facts I used sit above under the statements heading, because that heading takes "the numeric facts". That placement is not a judgment that they came from the face of the statements. The purchase-obligation and subsequent-event items in particular may well come from notes. The later split will have to establish their source; my placement cannot be relied on for it.
