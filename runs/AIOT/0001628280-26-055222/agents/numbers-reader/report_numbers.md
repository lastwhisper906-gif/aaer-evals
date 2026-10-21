# report_numbers.md — AIOT (Powerfleet, Inc.), 10-Q 0001628280-26-055222, quarter ended 2026-06-30

Read in full: input_trends.json, input_numbers.json, input_8k.md, input_prior_predictions.md.

**What the directory holds and lacks.**
- **Nothing forbidden is present.** The directory holds no prices, no abnormal returns, no short interest, no other company's files, no prior run's probability and no outcome window.
- **Prior predictions:** none on record. The file says this company has no earlier run.
- **Missing inputs.** The directory holds no articulation checks, no restatement traces and no fourth-quarter derivation. So there is no articulation gap I can quote, and no derived fiscal fourth-quarter figure exists for me to use.

**Restated prior values.** I found none.
- input_numbers.json marks facts that a later filing re-reported (`superseded_by`).
- Every superseded pair I checked carries the same value in the later filing. No period is reported differently by an earlier filing.
- No restatement trace exists in my input to confirm this beyond the facts themselves.

**Tag changes inside the trend table.** None. Every filled cell in every period uses the same concepts:
- RevenueFromContractWithCustomerExcludingAssessedTax
- AccountsReceivableNetCurrent
- CostOfGoodsAndServicesSold
- and so on for the other inputs.

The tag changes I did find are between the 10-K and the 10-Q facts. They are itemised below.

**Periods the record does not reach.** These have no cells at all, so there is nothing to quote.
- **quarters-back-1 (target 2026-03-31) and quarters-back-5 (target 2025-04-01).** The reason given is that no quarter ending within 20 days of those dates is in the companyfacts record. The commonest cause is a fiscal fourth quarter, which no filing reports as a duration; the table says it is derived by src/fourth_quarter.py, and that output is not in my directory. As a result, no quarters-back-0 metric has a quarter-over-quarter change.
- **years-back-2, years-back-3 and years-back-4.** The reasons are "no year ending within 20 days of 2024-04-02 is in the companyfacts record", and the same with 2023-04-04 and 2022-04-05. As a result, every year-level metric has at most two filled years, which is insufficient for a trend claim.

**Gaps in other periods the table holds.** These are outside quarters-back-0 and years-back-0, so no item is written for them.
- accruals_over_total_assets is not filled in quarters-back-2, -3, -6 and -7, because operating cash flow is not in the record for those discrete quarters.
- inventory_reserve_ratio is filled only in quarters-back-6 (0.027085938895837054) and quarters-back-7 (0.05662465940054496).
- non_gaap_gap is filled in no period.

**R&D capitalization block (years-back-0).** It prints no paragraph_id, so it cannot be quoted.
- capitalized_development_cost is missing because the record tags no us-gaap:CapitalizedComputerSoftwareAdditions in any period.
- The R&D asset and R&D amortization are missing because years 2 to 5 are not in the record.
- R&D-capitalized earnings and book value therefore do not exist.
- The R&D expense rows are quoted from the facts below.

**8-K header (not quotable).** The item-code and late-filing lists in input_8k.md carry no paragraph ids. They show:
- Item 4.02 on 2024-04-05.
- Item 4.01 on 2024-07-24 and 2024-08-16.
- Item 3.01 on 2024-04-05, 2024-08-09 and 2024-08-16.
- NT 10-K and NT 10-Q notices, the latest an NT 10-K on 2025-06-17.
- Item 5.02 filings on 2026-05-22 and 2026-07-21.

I note these for the reader covering controls; no item is written from them.

**Field conventions.**
- `expected_direction` is the way the quoted figure moved against its comparison as printed in the input. It is `none` where the input supports no direction, which includes every insufficient item and every tag change.
- `horizon` names the comparison the item rests on, or for release statements the period the release points to.
- Values in `what_changed` are copied from the input; nothing is derived.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_accruals_over_total_assets_quarterly_trend",
    "what_changed": "accruals_over_total_assets for 2026-04-01..2026-06-30 is -0.017539649394013063; year-over-year change against quarters-back-4 is -0.0014725144472693581; no quarter-over-quarter change exists (the cell says accruals_over_total_assets is not filled in quarters-back-1). Inputs: NetIncomeLoss -8440000, NetCashProvidedByUsedInOperatingActivities 8443000, Assets 962562000. Position in the filed history: lowest of the 2 filled quarters; two quarters of history is insufficient for a trend claim.",
    "account": "accruals (net income less operating cash flow) over total assets",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:accruals_over_total_assets:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
    "what_changed": "bad_debt_reserve_ratio for 2026-04-01..2026-06-30 is 0.09275086110201206; year-over-year change against quarters-back-4 is -0.0010780293438336502; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 9344000, AccountsReceivableNetCurrent 91399000. Position: third lowest of the 6 filled quarters.",
    "account": "allowance for doubtful accounts over gross receivables",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
    "what_changed": "contract_liabilities_over_revenue for 2026-04-01..2026-06-30 is 0.188251965376874; year-over-year change against quarters-back-4 is 0.02386629870060311; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: ContractWithCustomerLiabilityCurrent 20857000 (current portion only), quarterly revenue 110793000. Position: highest of the 6 filled quarters.",
    "account": "current contract liabilities (deferred revenue) over quarterly revenue",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
    "what_changed": "days_sales_of_inventory for 2026-04-01..2026-06-30 is 39.685988878143135; year-over-year change against quarters-back-4 is -5.95154260800296; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: InventoryNet 21645000, CostOfGoodsAndServicesSold 49632000, 91 days. Position: lowest of the 6 filled quarters.",
    "account": "inventory days",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:days_sales_of_inventory:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
    "what_changed": "days_sales_outstanding for 2026-04-01..2026-06-30 is 75.07070843825873; year-over-year change against quarters-back-4 is 3.8568130665277636; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: AccountsReceivableNetCurrent 91399000, quarterly revenue 110793000, 91 days. Position: second highest of the 6 filled quarters.",
    "account": "accounts receivable days",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:days_sales_outstanding:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_gross_margin_quarterly_trend",
    "what_changed": "gross_margin for 2026-04-01..2026-06-30 is 0.5520294603449677; year-over-year change against quarters-back-4 is 0.00957404789214833; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: revenue 110793000, CostOfGoodsAndServicesSold 49632000. Position: third lowest of the 6 filled quarters, a middle position despite the year-over-year rise.",
    "account": "gross margin",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:gross_margin:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend",
    "what_changed": "insufficient: inventory_reserve_ratio is not filled for 2026-04-01..2026-06-30, so it has no value, no change and no position. The release prints an inventory reserve charge for the quarter (see across_documents_inventory_reserve_charge_untagged), but no reserve balance exists in my input.",
    "account": "inventory valuation reserve over inventory",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
    "paragraph_id": "0001628280-26-055222:trends:inventory_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "results_against_expectations_non_gaap_gap_quarterly_trend",
    "what_changed": "insufficient: non_gaap_gap is not filled for 2026-04-01..2026-06-30 because no us-gaap concept carries a non-GAAP measure. The release's own non-GAAP figures are itemised below; no gap is computed here.",
    "account": "gap between non-GAAP and GAAP net income",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001628280-26-055222:trends:non_gaap_gap:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
    "what_changed": "receivables_over_revenue for 2026-04-01..2026-06-30 is 0.8249528399808652; year-over-year change against quarters-back-4 is 0.04238256117063477; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: AccountsReceivableNetCurrent 91399000, quarterly revenue 110793000. Position: second highest of the 6 filled quarters.",
    "account": "accounts receivable over quarterly revenue",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:receivables_over_revenue:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_soft_asset_share_quarterly_trend",
    "what_changed": "soft_asset_share for 2026-04-01..2026-06-30 is 0.8996178947434036; year-over-year change against quarters-back-4 is 0.0005094031739490967; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: Assets 962562000, PropertyPlantAndEquipmentNet 63800000, CashAndCashEquivalentsAtCarryingValue 32824000. Position: third lowest of the 6 filled quarters.",
    "account": "soft assets (total assets less fixed assets and cash) over total assets",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:soft_asset_share:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend",
    "what_changed": "warranty_reserve_ratio for 2026-04-01..2026-06-30 is 0.01916186040634336; year-over-year change against quarters-back-4 is -0.01452010576762731; no quarter-over-quarter change exists (quarters-back-1 not filled). Inputs: ProductWarrantyAccrual 2123000, quarterly revenue 110793000. Position: lowest of the 6 filled quarters.",
    "account": "product warranty accrual over quarterly revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-055222:trends:warranty_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_annual_trend",
    "what_changed": "accruals_over_total_assets for fiscal 2025-04-01..2026-03-31 is -0.05338517003029621; year-over-year change against years-back-1 is -0.001035408308408578. Inputs: NetIncomeLoss -20552000 and NetCashProvidedByUsedInOperatingActivities 30461000 (10-K 0001628280-26-043187), Assets 955565000 (10-Q 0001628280-26-055222). Position: lowest of the 2 filled years; insufficient for a trend claim.",
    "account": "accruals (net income less operating cash flow) over total assets",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:accruals_over_total_assets:2025-04-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
    "what_changed": "bad_debt_reserve_ratio for fiscal 2025-04-01..2026-03-31 is 0.0890996825150247; year-over-year change against years-back-1 is 0.04003098391802422. Inputs: allowance 9177000 and receivables 93820000 at 2026-03-31; the years-back-1 cell takes allowance 4057000 at 2025-03-31. Position: highest of the 2 filled years; insufficient for a trend claim.",
    "account": "allowance for doubtful accounts over gross receivables",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"highest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:bad_debt_reserve_ratio:2025-04-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
    "what_changed": "contract_liabilities_over_revenue for fiscal 2025-04-01..2026-03-31 is 0.04542596844811696; year-over-year change against years-back-1 is -0.0025030827635570407. Inputs: ContractWithCustomerLiabilityCurrent 20159000, annual revenue 443777000. Position: lowest of the 2 filled years; insufficient for a trend claim.",
    "account": "current contract liabilities over annual revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:contract_liabilities_over_revenue:2025-04-01..2026-03-31"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_annual_trend",
    "what_changed": "days_sales_of_inventory for fiscal 2025-04-01..2026-03-31 is 41.516657799397024; year-over-year change against years-back-1 is 1.6438768399856727. Inputs: InventoryNet 22448000, CostOfGoodsAndServicesSold 197355000, 365 days. Position: highest of the 2 filled years; insufficient for a trend claim.",
    "account": "inventory days",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"highest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:days_sales_of_inventory:2025-04-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_annual_trend",
    "what_changed": "days_sales_outstanding for fiscal 2025-04-01..2026-03-31 is 77.16555837729311; year-over-year change against years-back-1 is -1.9963935419378203. Inputs: AccountsReceivableNetCurrent 93820000, annual revenue 443777000, 365 days. Position: lowest of the 2 filled years; insufficient for a trend claim.",
    "account": "accounts receivable days",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:days_sales_outstanding:2025-04-01..2026-03-31"
  },
  {
    "id": "earnings_quality_gross_margin_annual_trend",
    "what_changed": "gross_margin for fiscal 2025-04-01..2026-03-31 is 0.5552833968412063; year-over-year change against years-back-1 is 0.018651809182764545. Inputs: revenue 443777000, CostOfGoodsAndServicesSold 197355000. Position: highest of the 2 filled years; insufficient for a trend claim.",
    "account": "gross margin",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"highest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:gross_margin:2025-04-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend",
    "what_changed": "insufficient: inventory_reserve_ratio is not filled for fiscal 2025-04-01..2026-03-31; no value, change or position exists.",
    "account": "inventory valuation reserve over inventory",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"missing\": \"no row for inventory_reserve in 2026-03-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
    "paragraph_id": "0001628280-26-055222:trends:inventory_reserve_ratio:2025-04-01..2026-03-31"
  },
  {
    "id": "results_against_expectations_non_gaap_gap_annual_trend",
    "what_changed": "insufficient: non_gaap_gap is not filled for fiscal 2025-04-01..2026-03-31; no value, change or position exists.",
    "account": "gap between non-GAAP and GAAP net income",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001628280-26-055222:trends:non_gaap_gap:2025-04-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_annual_trend",
    "what_changed": "receivables_over_revenue for fiscal 2025-04-01..2026-03-31 is 0.2114124887049126; year-over-year change against years-back-1 is -0.005469571347774871. Inputs: AccountsReceivableNetCurrent 93820000, annual revenue 443777000. Position: lowest of the 2 filled years; insufficient for a trend claim.",
    "account": "accounts receivable over annual revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:receivables_over_revenue:2025-04-01..2026-03-31"
  },
  {
    "id": "earnings_quality_soft_asset_share_annual_trend",
    "what_changed": "soft_asset_share for fiscal 2025-04-01..2026-03-31 is 0.8965073019627131; year-over-year change against years-back-1 is 0.009029292005248268. Inputs: Assets 955565000, PropertyPlantAndEquipmentNet 62398000, cash 36496000. Position: highest of the 2 filled years; insufficient for a trend claim.",
    "account": "soft assets over total assets",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"highest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:soft_asset_share:2025-04-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend",
    "what_changed": "warranty_reserve_ratio for fiscal 2025-04-01..2026-03-31 is 0.004961951610831566; year-over-year change against years-back-1 is -0.005018325067374854. Inputs: ProductWarrantyAccrual 2202000, annual revenue 443777000. Position: lowest of the 2 filled years; insufficient for a trend claim.",
    "account": "product warranty accrual over annual revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-055222:trends:warranty_reserve_ratio:2025-04-01..2026-03-31"
  },
  {
    "id": "structure_and_disclosure_changes_capitalized_software_gross_tag_change",
    "what_changed": "Change of tag, not a restatement. The 10-Q tags the 2026-03-31 gross capitalized software balance 22875000 as CapitalizedComputerSoftwareGross. The 10-K tagged the same period and value as FiniteLivedIntangibleAssetsGross with member ComputerSoftwareIntangibleAssetMember (0001628280-26-043187:facts:FiniteLivedIntangibleAssetsGross:2026-03-31:us-gaap:FiniteLivedIntangibleAssetsByMajorClassAxis=us-gaap:ComputerSoftwareIntangibleAssetMember). The 2026-06-30 balance under the new tag is 27295000.",
    "account": "capitalized software, gross",
    "expected_direction": "none",
    "horizon": "balance at 2026-03-31 as filed in the 10-K against as filed in the 10-Q",
    "quote": "\"value\": \"22875000\"",
    "paragraph_id": "0001628280-26-055222:facts:CapitalizedComputerSoftwareGross:2026-03-31"
  },
  {
    "id": "structure_and_disclosure_changes_intangible_assets_gross_tag_change",
    "what_changed": "Change of tag, not a restatement. The 10-Q tags 2026-03-31 gross finite-lived intangibles 346934000 as IntangibleAssetFiniteLivedAndCapitalizedCostSoftwareToBeSoldLeasedOrMarketedBeforeAccumulatedAmortization. The 10-K tagged the same value as FiniteLivedIntangibleAssetsGross (0001628280-26-043187:facts:FiniteLivedIntangibleAssetsGross:2026-03-31). The 2026-06-30 value under the new tag is 354573000.",
    "account": "finite-lived intangible assets including capitalized software, gross",
    "expected_direction": "none",
    "horizon": "balance at 2026-03-31 as filed in the 10-K against as filed in the 10-Q",
    "quote": "\"value\": \"346934000\"",
    "paragraph_id": "0001628280-26-055222:facts:IntangibleAssetFiniteLivedAndCapitalizedCostSoftwareToBeSoldLeasedOrMarketedBeforeAccumulatedAmortization:2026-03-31"
  },
  {
    "id": "structure_and_disclosure_changes_fixed_asset_software_member_change",
    "what_changed": "Change of member, not a restatement. Software within property and equipment, 11807000 at 2026-03-31, is tagged with member us-gaap:SoftwareAndSoftwareDevelopmentCostsMember in the 10-Q. The 10-K used the custom member aiot:ComputerSoftwareMember for the same value (0001628280-26-043187:facts:PropertyPlantAndEquipmentGross:2026-03-31:us-gaap:PropertyPlantAndEquipmentByTypeAxis=aiot:ComputerSoftwareMember). The 2026-06-30 value is 12421000.",
    "account": "property and equipment, software, gross",
    "expected_direction": "none",
    "horizon": "balance at 2026-03-31 as filed in the 10-K against as filed in the 10-Q",
    "quote": "\"value\": \"11807000\"",
    "paragraph_id": "0001628280-26-055222:facts:PropertyPlantAndEquipmentGross:2026-03-31:us-gaap:PropertyPlantAndEquipmentByTypeAxis=us-gaap:SoftwareAndSoftwareDevelopmentCostsMember"
  },
  {
    "id": "structure_and_disclosure_changes_restructuring_charges_context_change",
    "what_changed": "The same restructuring figure, 3463000, sits on two different periods. The 10-Q tags it to the full fiscal year 2025-04-01..2026-03-31. The 10-K tagged it to the nine-month context 2025-04-01..2025-12-31 (0001628280-26-043187:facts:RestructuringCharges:2025-04-01..2025-12-31). The input does not say which context is right. In the same roll-forward, PaymentsForRestructuring for the fiscal year is 3580000 and the reserve is 1207000 at 2026-03-31.",
    "account": "restructuring charges",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-03-31 as filed in the 10-K against as filed in the 10-Q",
    "quote": "\"value\": \"3463000\"",
    "paragraph_id": "0001628280-26-055222:facts:RestructuringCharges:2025-04-01..2026-03-31"
  },
  {
    "id": "structure_and_disclosure_changes_rmb_general_facility_unit_duplicate",
    "what_changed": "Unit ambiguity. The RMB general facility maximum borrowing capacity at 2026-06-30 is tagged 21332000 in USD and also 21332000 in ZAR (paragraph id ending :unit=iso4217:ZAR). The same facility's drawn line, 18067000, and remaining capacity, 3265000, are tagged only in ZAR. A ZAR fact dated 2024-04-02 carries 350000. The 10-K rows for 2026-03-31 carried 20520000 under both units. The input does not settle which unit is right.",
    "account": "line of credit, RMB general facility",
    "expected_direction": "none",
    "horizon": "balance at 2026-06-30",
    "quote": "\"value\": \"21332000\"",
    "paragraph_id": "0001628280-26-055222:facts:LineOfCreditFacilityMaximumBorrowingCapacity:2026-06-30:us-gaap:DebtInstrumentAxis=aiot:RMBGeneralFacilityMember,us-gaap:ShortTermDebtTypeAxis=us-gaap:LineOfCreditMember"
  },
  {
    "id": "structure_and_disclosure_changes_hapoalim_term_facility_unit_duplicate",
    "what_changed": "Unit ambiguity.\n- Carrying amounts are tagged in ILS: LongTermDebt for Hapoalim Term Facility A is 14260000 ILS and for Facility B is 12267000 ILS (0001628280-26-055222:facts:LongTermDebt:2026-06-30:us-gaap:DebtInstrumentAxis=aiot:HapoalimTermFacilityBMember,us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember:unit=iso4217:ILS).\n- Face amounts carry the same number in both units: Facility A is 20000000 in ILS and 20000000 in USD; Facility B is 10000000 in ILS and 10000000 in USD.\n- The input does not say whether the ILS unit on the carrying amounts is correct.",
    "account": "long-term debt, Hapoalim term facilities",
    "expected_direction": "none",
    "horizon": "balance at 2026-06-30",
    "quote": "\"value\": \"14260000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebt:2026-06-30:us-gaap:DebtInstrumentAxis=aiot:HapoalimTermFacilityAMember,us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember:unit=iso4217:ILS"
  },
  {
    "id": "structure_and_disclosure_changes_financing_cost_amortization_scale",
    "what_changed": "Scaling anomaly in the February 2026 10-Q. Amortization of financing costs on the New RMB Term Facility is tagged 179000000 for the nine months 2025-04-01..2025-12-31.\n- That value exceeds the facility's face amount of 125000000.\n- The current 10-Q tags 58000 (quarter to 2025-06-30) and 64000 (quarter to 2026-06-30) for the same facility.\n- Deferred finance costs at inception (2024-10-01) are 1433000.\nThe tagged nine-month value looks mis-scaled; the correct figure does not exist in my input.",
    "account": "amortization of debt financing costs",
    "expected_direction": "none",
    "horizon": "nine months ended 2025-12-31 as filed in 0001628280-26-006487",
    "quote": "\"value\": \"179000000\"",
    "paragraph_id": "0001628280-26-006487:facts:AmortizationOfFinancingCosts:2025-04-01..2025-12-31:us-gaap:DebtInstrumentAxis=aiot:NewRMBTermFacilityMember"
  },
  {
    "id": "structure_and_disclosure_changes_share_based_compensation_award_duplicate",
    "what_changed": "Tagging anomaly. The same AllocatedShareBasedCompensationExpense value is tagged under three different award types:\n- 2503000 for the quarter to 2026-06-30 and 820000 for the quarter to 2025-06-30, each under PerformanceSharesMember, RestrictedStockUnitsRSUMember and RestrictedStockMember.\n- Unrecognized cost of 13496000 at 2026-06-30 sits under the same three members.\nThe XBRL cannot tell the award types apart. Total ShareBasedCompensation in the cash flow is 3107000 against 1853000.",
    "account": "stock-based compensation by award type",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"value\": \"2503000\"",
    "paragraph_id": "0001628280-26-055222:facts:AllocatedShareBasedCompensationExpense:2026-04-01..2026-06-30:us-gaap:AwardTypeAxis=us-gaap:PerformanceSharesMember"
  },
  {
    "id": "structure_and_disclosure_changes_acquiree_pro_forma_revenue_precision",
    "what_changed": "The RTS Solutions Africa pro forma revenue for the prior-year quarter 2025-04-01..2025-06-30 is printed as 1000000.0 with decimals -5. It is a rounded single figure, unlike the thousands-precision facts around it. The pro forma net loss for the current quarter is -8000.",
    "account": "pro forma revenue, RTS Solutions Africa acquisition",
    "expected_direction": "none",
    "horizon": "quarter ended 2025-06-30, pro forma",
    "quote": "\"value\": \"1000000.0\"",
    "paragraph_id": "0001628280-26-055222:facts:BusinessAcquisitionsProFormaRevenue:2025-04-01..2025-06-30:dei:LegalEntityAxis=aiot:MiXTelematicsAfricaPtyLtd.Member,us-gaap:BusinessAcquisitionAxis=aiot:RTSSolutionsAfricaPtyLtd.Member"
  },
  {
    "id": "earnings_quality_effective_tax_rate_quarterly_fact",
    "what_changed": "The effective tax rate for the quarter is -0.1994, against -0.0367 a year earlier. The company records tax expense on a pre-tax loss: pre-tax loss is -6884000 against -9872000.",
    "account": "income tax",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"-0.1994\"",
    "paragraph_id": "0001628280-26-055222:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_income_tax_expense_quarterly_fact",
    "what_changed": "Income tax expense for the quarter is 1373000 against 362000 a year earlier, while the pre-tax result moved from -9872000 to -6884000.",
    "account": "income tax expense",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"1373000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncomeTaxExpenseBenefit:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_foreign_pretax_income_quarterly_fact",
    "what_changed": "Foreign pre-tax income for the quarter is 3553000 against 473000 a year earlier.",
    "account": "pre-tax income, foreign",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"3553000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesForeign:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_domestic_pretax_loss_quarterly_fact",
    "what_changed": "Domestic (US) pre-tax loss for the quarter is -10437000 against -10345000 a year earlier. For fiscal 2026 the 10-K tags a domestic pre-tax loss of -41764000 and foreign pre-tax income of 30508000.",
    "account": "pre-tax loss, domestic",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"-10437000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_income_taxes_paid_quarterly_fact",
    "what_changed": "Income taxes paid in the quarter are 1721000 against 873000 a year earlier.",
    "account": "cash taxes paid",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"1721000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncomeTaxesPaidNet:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_deferred_income_taxes_quarterly_fact",
    "what_changed": "The deferred income tax line in operating cash flow is -1538000 against -3157000 a year earlier. Deferred tax asset is 5066000 against 4537000; deferred tax liability is 60840000 against 60063000, both comparing 2026-06-30 with 2026-03-31.",
    "account": "deferred income taxes",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"-1538000\"",
    "paragraph_id": "0001628280-26-055222:facts:DeferredIncomeTaxesAndTaxCredits:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_effective_tax_rate_annual_fact",
    "what_changed": "The fiscal 2026 effective tax rate per the 10-K is -0.772, on a fiscal-year net loss of -20552000. I did not retain a prior-year rate from the input, so no direction is stated.",
    "account": "income tax",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"value\": \"-0.772\"",
    "paragraph_id": "0001628280-26-043187:facts:EffectiveIncomeTaxRateContinuingOperations:2025-04-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_deferred_tax_valuation_allowance_fact",
    "what_changed": "The deferred tax asset valuation allowance is 58858000 at 2026-03-31 against 53307000 at 2025-03-31 (10-K).",
    "account": "deferred tax valuation allowance",
    "expected_direction": "up",
    "horizon": "balance at 2026-03-31 against 2025-03-31",
    "quote": "\"value\": \"58858000\"",
    "paragraph_id": "0001628280-26-043187:facts:DeferredTaxAssetsValuationAllowance:2026-03-31"
  },
  {
    "id": "estimates_and_discretion_united_states_valuation_allowance_change_fact",
    "what_changed": "The 10-K rate reconciliation shows a fiscal 2026 change in the US valuation allowance of 7310000.",
    "account": "deferred tax valuation allowance, US",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"value\": \"7310000\"",
    "paragraph_id": "0001628280-26-043187:facts:IncomeTaxReconciliationChangeInDeferredTaxAssetsValuationAllowance:2025-04-01..2026-03-31:us-gaap:IncomeTaxAuthorityAxis=country:US"
  },
  {
    "id": "estimates_and_discretion_receivable_write_offs_quarterly_fact",
    "what_changed": "Receivables written off against the allowance in the quarter are 3705000, against 1634000 a year earlier.",
    "account": "allowance for doubtful accounts, write-offs",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"3705000\"",
    "paragraph_id": "0001628280-26-055222:facts:AllowanceForDoubtfulAccountsReceivableWriteOffs:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_bad_debt_provision_quarterly_fact",
    "what_changed": "Bad debt expense (provision) for the quarter is 2958000 against 1856000 a year earlier. The release's cash flow prints the same figures as 'Bad debts expense'.",
    "account": "bad debt expense",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"2958000\"",
    "paragraph_id": "0001628280-26-055222:facts:ProvisionForDoubtfulAccounts:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_doubtful_accounts_allowance_balance_fact",
    "what_changed": "The allowance for doubtful accounts balance is:\n- 4057000 at 2025-03-31\n- 8437000 at 2025-06-30\n- 9177000 at 2026-03-31\n- 9344000 at 2026-06-30\nThe input does not say what drove the rise between 2025-03-31 and 2025-06-30.",
    "account": "allowance for doubtful accounts",
    "expected_direction": "up",
    "horizon": "balances from 2025-03-31 to 2026-06-30",
    "quote": "\"value\": \"8437000\"",
    "paragraph_id": "0001628280-26-055222:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2025-06-30"
  },
  {
    "id": "estimates_and_discretion_bad_debt_provision_annual_fact",
    "what_changed": "The fiscal 2026 bad debt provision per the 10-K is 10988000, against 9418000 for fiscal 2025.",
    "account": "bad debt expense",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"value\": \"10988000\"",
    "paragraph_id": "0001628280-26-043187:facts:ProvisionForDoubtfulAccounts:2025-04-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_receivable_write_offs_annual_fact",
    "what_changed": "Fiscal 2026 write-offs against the allowance per the 10-K are 12753000. I did not retain a prior-year write-off figure from the input, so no direction is stated.",
    "account": "allowance for doubtful accounts, write-offs",
    "expected_direction": "none",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"value\": \"12753000\"",
    "paragraph_id": "0001628280-26-043187:facts:AllowanceForDoubtfulAccountsReceivableWriteOffs:2025-04-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_product_revenue_quarterly_fact",
    "what_changed": "Product revenue for the quarter is 16480000, against 17657000 a year earlier. Cost of products is 12970000 against 13228000. The release ties part of the shortfall to $3.2 million of product revenue delayed by a production constraint.",
    "account": "product revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"16480000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=us-gaap:ProductMember"
  },
  {
    "id": "revenue_recognition_service_revenue_quarterly_fact",
    "what_changed": "Service revenue for the quarter is 94313000 against 86464000 a year earlier. Cost of services is 36662000 against 34412000.",
    "account": "service revenue",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"94313000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=us-gaap:ServiceMember"
  },
  {
    "id": "revenue_recognition_total_revenue_quarterly_fact",
    "what_changed": "Total revenue for the quarter is 110793000 against 104121000 a year earlier. The company reports one operating and reportable segment (AIoT Asset Management) carrying the same totals.",
    "account": "revenue",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"110793000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_total_revenue_annual_fact",
    "what_changed": "Fiscal 2026 revenue per the 10-K is 443777000, against 362515000 for fiscal 2025. The input tags the Fleet Complete acquisition consideration (190000000) on 2024-09-27, inside fiscal 2025, so the two years may not be on the same scope.",
    "account": "revenue",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"value\": \"443777000\"",
    "paragraph_id": "0001628280-26-043187:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-04-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_product_revenue_annual_fact",
    "what_changed": "Fiscal 2026 product revenue per the 10-K is 83975000 against 85584000 for fiscal 2025. Fiscal 2026 service revenue is 359802000 against 276931000.",
    "account": "product revenue",
    "expected_direction": "down",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"value\": \"83975000\"",
    "paragraph_id": "0001628280-26-043187:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-04-01..2026-03-31:srt:ProductOrServiceAxis=us-gaap:ProductMember"
  },
  {
    "id": "revenue_recognition_united_states_revenue_fact",
    "what_changed": "US revenue for the quarter is 34430000 against 37425000 a year earlier.",
    "account": "revenue, United States",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"34430000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:US"
  },
  {
    "id": "revenue_recognition_africa_revenue_fact",
    "what_changed": "Africa revenue for the quarter is 29230000 against 25462000 a year earlier. It includes RTS Solutions Africa, acquired 2026-02-01, whose revenue since acquisition is 1328000. The release says South African revenue was about $1.6 million lower; see across_documents_south_african_revenue_against_africa_geography.",
    "account": "revenue, Africa",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"29230000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AfricaMember"
  },
  {
    "id": "revenue_recognition_israel_revenue_fact",
    "what_changed": "Israel revenue for the quarter is 17735000 against 13295000 a year earlier.",
    "account": "revenue, Israel",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"17735000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:IL"
  },
  {
    "id": "revenue_recognition_europe_and_middle_east_revenue_fact",
    "what_changed": "Europe and Middle East revenue for the quarter is 12066000 against 12352000 a year earlier.",
    "account": "revenue, Europe and Middle East",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"12066000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=aiot:EuropeAndMiddleEastMember"
  },
  {
    "id": "revenue_recognition_australia_revenue_fact",
    "what_changed": "Australia revenue for the quarter is 11207000 against 10618000 a year earlier.",
    "account": "revenue, Australia",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"11207000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:AU"
  },
  {
    "id": "revenue_recognition_other_geography_revenue_fact",
    "what_changed": "Revenue from other geographies for the quarter is 6125000 against 4969000 a year earlier.",
    "account": "revenue, other geographies",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"6125000\"",
    "paragraph_id": "0001628280-26-055222:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=aiot:OtherMember"
  },
  {
    "id": "revenue_recognition_acquiree_revenue_since_acquisition_fact",
    "what_changed": "RTS Solutions Africa (acquired 2026-02-01 through MiX Telematics Africa) contributed revenue of 1328000 and earnings of 66000 in the quarter. Acquisition-related costs in the quarter were 202000. It had no revenue in the prior-year quarter's consolidated figures.",
    "account": "acquired revenue",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"value\": \"1328000\"",
    "paragraph_id": "0001628280-26-055222:facts:BusinessCombinationProFormaInformationRevenueOfAcquireeSinceAcquisitionDateActual:2026-04-01..2026-06-30:dei:LegalEntityAxis=aiot:MiXTelematicsAfricaPtyLtd.Member,us-gaap:BusinessAcquisitionAxis=aiot:RTSSolutionsAfricaPtyLtd.Member"
  },
  {
    "id": "revenue_recognition_contract_liability_revenue_recognized_fact",
    "what_changed": "Revenue recognized in the quarter from the opening contract liability balance is 6620000; the 10-Q tags 22203000 for fiscal 2026. Total contract liability is 24360000 at 2026-06-30 against 24164000 at 2026-03-31:\n- service member: 23759000 against 23337000\n- product member: 601000 against 827000",
    "account": "contract liabilities (deferred revenue)",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"value\": \"6620000\"",
    "paragraph_id": "0001628280-26-055222:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_asset_balance_fact",
    "what_changed": "The current contract asset is 3536000 at 2026-06-30 against 5017000 at 2026-03-31. The release says recoveries of pre-acquisition Fleet Complete contract assets ($0.9 million this quarter) flow through operating cash flow.",
    "account": "contract assets",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"3536000\"",
    "paragraph_id": "0001628280-26-055222:facts:ContractWithCustomerAssetNetCurrent:2026-06-30"
  },
  {
    "id": "revenue_recognition_deferred_costs_current_fact",
    "what_changed": "Current deferred costs are 172000 at 2026-06-30 against 0 at 2026-03-31. The operating cash flow line for deferred costs (IncreaseDecreaseInDeferredCharges) is 2960000 against 2730000.",
    "account": "deferred contract costs",
    "expected_direction": "up",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"172000\"",
    "paragraph_id": "0001628280-26-055222:facts:DeferredCostsCurrent:2026-06-30"
  },
  {
    "id": "earnings_quality_operating_cash_flow_fact",
    "what_changed": "Operating cash flow for the quarter is 8443000 against 4721000 a year earlier. Net loss attributable is -8440000 against -10234000. Per the release, it includes $0.9 million (prior year $1.5 million) of recoveries of pre-acquisition contract assets.",
    "account": "operating cash flow",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"8443000\"",
    "paragraph_id": "0001628280-26-055222:facts:NetCashProvidedByUsedInOperatingActivities:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_payables_and_accruals_change_fact",
    "what_changed": "The cash flow change in payables and accrued liabilities is 722000 against 9637000 a year earlier. Accounts payable is 44455000 at 2026-06-30 against 46353000 at 2026-03-31.",
    "account": "accounts payable and accrued liabilities",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"722000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncreaseDecreaseInAccountsPayableAndAccruedLiabilities:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_receivables_change_fact",
    "what_changed": "The cash flow change in receivables is -893000 against 2391000 a year earlier. Net receivables are 91399000 at 2026-06-30 against 93820000 at 2026-03-31.",
    "account": "accounts receivable",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"-893000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncreaseDecreaseInAccountsReceivable:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_inventories_change_fact",
    "what_changed": "The cash flow change in inventories is -725000 against 4733000 a year earlier. Net inventory is 21645000 at 2026-06-30 against 22448000 at 2026-03-31.",
    "account": "inventory",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"-725000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncreaseDecreaseInInventories:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_deferred_charges_change_fact",
    "what_changed": "The cash flow change in deferred costs is 2960000 against 2730000 a year earlier.",
    "account": "deferred costs",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"2960000\"",
    "paragraph_id": "0001628280-26-055222:facts:IncreaseDecreaseInDeferredCharges:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_derivative_gain_fact",
    "what_changed": "The net derivative gain for the quarter is 919000 against -104000 a year earlier. It is a non-cash mark-to-market gain that the release removes from adjusted EBITDA.",
    "account": "derivative gain (loss)",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"919000\"",
    "paragraph_id": "0001628280-26-055222:facts:DerivativeGainLossOnDerivativeNet:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_level_three_derivative_fair_value_fact",
    "what_changed": "The net derivative at Level 3 of the fair value hierarchy is 4425000 at 2026-06-30 against 3505000 at 2026-03-31.\n- Current derivative assets: RMB Facility A 1640000 against 1215000, and Facility B 2785000 against 2291000.\n- Unobservable inputs at 2026-06-30: credit spread 0.31 (A) and 0.26 (B); floating spread 0.0410 (A) and 0.0415 (B).",
    "account": "derivative asset, Level 3",
    "expected_direction": "up",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"4425000\"",
    "paragraph_id": "0001628280-26-055222:facts:DerivativeFairValueOfDerivativeNet:2026-06-30:us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel3Member"
  },
  {
    "id": "earnings_quality_share_based_compensation_fact",
    "what_changed": "Stock-based compensation for the quarter is 3107000 against 1853000 a year earlier.",
    "account": "stock-based compensation",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"3107000\"",
    "paragraph_id": "0001628280-26-055222:facts:ShareBasedCompensation:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_other_noncash_items_fact",
    "what_changed": "Other non-cash income or expense is 1168000 against 513000 a year earlier. The release prints it as (1,168) against (513) in operating cash flow.",
    "account": "other non-cash items",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"1168000\"",
    "paragraph_id": "0001628280-26-055222:facts:OtherNoncashIncomeExpense:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_operating_income_fact",
    "what_changed": "Operating income for the quarter is 270000 against -2039000 a year earlier. SG&A is 56531000 against 53663000.",
    "account": "operating income",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"270000\"",
    "paragraph_id": "0001628280-26-055222:facts:OperatingIncomeLoss:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_net_loss_attributable_fact",
    "what_changed": "Net loss attributable to common stockholders is -8440000 against -10234000 a year earlier. Net loss including the non-controlling interest (ProfitLoss) is -8257000. Diluted EPS is -0.06 against -0.08.",
    "account": "net loss",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"-8440000\"",
    "paragraph_id": "0001628280-26-055222:facts:NetIncomeLoss:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_noncontrolling_interest_income_fact",
    "what_changed": "Net income attributable to the non-controlling interest is 183000 against 0 a year earlier. It is tagged as attributable to the redeemable non-controlling interest in RTS Solutions Africa.",
    "account": "non-controlling interest",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"183000\"",
    "paragraph_id": "0001628280-26-055222:facts:NetIncomeLossAttributableToNoncontrollingInterest:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_comprehensive_income_fact",
    "what_changed": "Comprehensive income is 3987000 against 12285000 a year earlier. The foreign currency translation component is 12427000 against 22519000.",
    "account": "comprehensive income",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"3987000\"",
    "paragraph_id": "0001628280-26-055222:facts:ComprehensiveIncomeNetOfTax:2026-04-01..2026-06-30"
  },
  {
    "id": "liquidity_and_capital_capitalized_software_payments_fact",
    "what_changed": "Cash paid to develop software in the quarter is 4100000 against 3724000 a year earlier.",
    "account": "capitalized software development",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"4100000\"",
    "paragraph_id": "0001628280-26-055222:facts:PaymentsToDevelopSoftware:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_capitalized_software_balance_fact",
    "what_changed": "Gross capitalized software is 27295000 at 2026-06-30 against 22875000 at 2026-03-31. Accumulated amortization is 8421000 against 5296000; net is 18874000 against 17579000.",
    "account": "capitalized software",
    "expected_direction": "up",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"27295000\"",
    "paragraph_id": "0001628280-26-055222:facts:CapitalizedComputerSoftwareGross:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_capital_expenditures_fact",
    "what_changed": "Capital expenditures in the quarter are 4873000 against 8114000 a year earlier. Gross installed products in property and equipment are 78073000 at 2026-06-30 against 73750000 at 2026-03-31.",
    "account": "capital expenditures",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"4873000\"",
    "paragraph_id": "0001628280-26-055222:facts:PaymentsToAcquirePropertyPlantAndEquipment:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_intangible_amortization_fact",
    "what_changed": "Amortization of intangible assets is 10463000 against 9859000 a year earlier.\n- Estimated amortization at 2026-06-30: 31760000 for the remainder of the fiscal year, then 41183000, 32364000, 23898000 and 17818000 for years one to four.\n- Customer relationships gross is 214972000 at 2026-06-30 against 213107000 at 2026-03-31.",
    "account": "intangible asset amortization",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"10463000\"",
    "paragraph_id": "0001628280-26-055222:facts:AmortizationOfIntangibleAssets:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_depreciation_and_amortization_fact",
    "what_changed": "Total depreciation and amortization in the cash flow is 16207000 against 16031000 a year earlier. The fixed-asset note's DepreciationAndAmortization tag is 5744000 against 6172000. The segment's D&A within SG&A is 2282000 against 2790000.",
    "account": "depreciation and amortization",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"16207000\"",
    "paragraph_id": "0001628280-26-055222:facts:DepreciationDepletionAndAmortization:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_restructuring_charges_fact",
    "what_changed": "Restructuring charges for the quarter are 727000, all tagged as employee severance; the prior-year quarter's severance charge is 1995000. The reserve is 1158000 at 2026-06-30 against 1207000 at 2026-03-31, after payments of 753000 and translation of -23000. Cumulative cost incurred since 2024-04-01 is 8863000.",
    "account": "restructuring",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"727000\"",
    "paragraph_id": "0001628280-26-055222:facts:RestructuringCharges:2026-04-01..2026-06-30"
  },
  {
    "id": "liquidity_and_capital_cash_balance_fact",
    "what_changed": "Cash and cash equivalents are 32824000 at 2026-06-30 against 36496000 at 2026-03-31. Restricted cash is 3895000 against 4322000. Cash including restricted cash is 36719000 against 40818000.",
    "account": "cash",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"32824000\"",
    "paragraph_id": "0001628280-26-055222:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_remaining_borrowing_capacity_fact",
    "what_changed": "Remaining borrowing capacity under the revolving facilities is 29907000 at 2026-06-30. The 10-K tags 27121000 at 2026-03-31. At 2026-06-30, maximum capacity is 72303000 and drawn lines of credit are 42396000. The release's $29.9 million matches.",
    "account": "revolving credit availability",
    "expected_direction": "up",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"29907000\"",
    "paragraph_id": "0001628280-26-055222:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_debt_maturities_next_twelve_months_fact",
    "what_changed": "Long-term debt principal due in the next twelve months is 5060000; principal due in the remainder of the fiscal year is 0.",
    "account": "debt maturities",
    "expected_direction": "none",
    "horizon": "twelve months from 2026-06-30",
    "quote": "\"value\": \"5060000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_debt_maturities_year_two_fact",
    "what_changed": "Long-term debt principal due in year two is 49247000.",
    "account": "debt maturities",
    "expected_direction": "none",
    "horizon": "year two from 2026-06-30",
    "quote": "\"value\": \"49247000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebtMaturitiesRepaymentsOfPrincipalInYearTwo:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_debt_maturities_year_three_fact",
    "what_changed": "Long-term debt principal due in year three is 57220000.",
    "account": "debt maturities",
    "expected_direction": "none",
    "horizon": "year three from 2026-06-30",
    "quote": "\"value\": \"57220000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebtMaturitiesRepaymentsOfPrincipalInYearThree:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_debt_maturities_year_four_fact",
    "what_changed": "Long-term debt principal due in year four is 125000000. That equals the New RMB Term Facility's face amount, tagged 125000000 with a stated rate of 0.0870.",
    "account": "debt maturities",
    "expected_direction": "none",
    "horizon": "year four from 2026-06-30",
    "quote": "\"value\": \"125000000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebtMaturitiesRepaymentsOfPrincipalInYearFour:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_long_term_debt_fact",
    "what_changed": "Long-term debt is 236527000 at 2026-06-30: current 6682000, noncurrent 229300000. Noncurrent was 229669000 at 2026-03-31. A total long-term debt figure for 2026-03-31 is not among the facts I can quote, so no direction is stated.",
    "account": "long-term debt",
    "expected_direction": "none",
    "horizon": "balance at 2026-06-30",
    "quote": "\"value\": \"236527000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebt:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_total_debt_carrying_amount_fact",
    "what_changed": "The fair value disclosure carries total debt at 278392000 at 2026-06-30 against 280024000 at 2026-03-31. Estimated fair value, all Level 2, is 282435000 against 281081000. The release's total debt of $278.4 million matches the carrying amount.",
    "account": "total debt",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"278392000\"",
    "paragraph_id": "0001628280-26-055222:facts:LongTermDebtFairValue:2026-06-30:us-gaap:FairValueByMeasurementBasisAxis=us-gaap:CarryingReportedAmountFairValueDisclosureMember"
  },
  {
    "id": "liquidity_and_capital_short_term_bank_loans_fact",
    "what_changed": "Short-term bank loans are 42410000 at 2026-06-30 against 44072000 at 2026-03-31. ShortTermBorrowings, which includes current maturities of long-term debt, is 49092000 against 50355000. Net short-term debt cash flow is -2457000 against -5428000.",
    "account": "short-term bank debt",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"42410000\"",
    "paragraph_id": "0001628280-26-055222:facts:ShortTermBankLoansAndNotesPayable:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_hapoalim_term_facility_proceeds_fact",
    "what_changed": "The debt note tags these quarter flows for the Hapoalim term facilities:\n- proceeds: 30000000\n- repayments: 11200000\n- net increase: 18800000\n- interest expense: 624000 (624000 in the prior-year quarter as well)\nThe cash flow statement facts for the quarter show RepaymentsOfLongTermDebt of 1679000 and net short-term debt of -2457000, and no proceeds line. How the note's 30000000 sits in the cash flow statement does not exist in my input.",
    "account": "term debt, Hapoalim facilities",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"value\": \"30000000\"",
    "paragraph_id": "0001628280-26-055222:facts:ProceedsFromLinesOfCredit:2026-04-01..2026-06-30:us-gaap:DebtInstrumentAxis=aiot:HapoalimTermFacilitiesMember"
  },
  {
    "id": "liquidity_and_capital_interest_paid_fact",
    "what_changed": "Interest paid in the quarter is 6444000 against 5994000 a year earlier. Interest expense is 6983000 against 6786000.",
    "account": "interest",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"6444000\"",
    "paragraph_id": "0001628280-26-055222:facts:InterestPaidNet:2026-04-01..2026-06-30"
  },
  {
    "id": "liquidity_and_capital_redeemable_noncontrolling_interest_fact",
    "what_changed": "The redeemable non-controlling interest is 6192000 at 2026-06-30 against 6009000 at 2026-03-31. It arose from the RTS Solutions Africa acquisition:\n- fair value at 2026-02-01: 8765000\n- equity consideration: 8765000, with 127000 shares issued\n- fiscal 2026 TemporaryEquityOtherChanges: -3364000, with an APIC adjustment of 3364000\n- income attributable: 608000 for fiscal 2026 and 183000 for the quarter",
    "account": "redeemable non-controlling interest",
    "expected_direction": "up",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"6192000\"",
    "paragraph_id": "0001628280-26-055222:facts:RedeemableNoncontrollingInterestEquityCarryingAmount:2026-06-30"
  },
  {
    "id": "structure_and_disclosure_changes_rts_acquisition_goodwill_fact",
    "what_changed": "Fiscal 2026 goodwill acquired with RTS Solutions Africa is 5637000; goodwill acquired with Powerfleet Africa Sky is 552000. RTS identifiable intangibles are 1144000 (trade names 586000, developed technology 558000). Cash payment is tagged at 90000000 in ZAR.",
    "account": "goodwill from acquisitions",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"value\": \"5637000\"",
    "paragraph_id": "0001628280-26-055222:facts:GoodwillAcquiredDuringPeriod:2025-04-01..2026-03-31:us-gaap:BusinessAcquisitionAxis=aiot:RTSSolutionsAfricaPtyLtd.Member"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_mtn_possible_loss_fact",
    "what_changed": "The maximum reasonably possible loss under the amended MTN network service agreement is 330000 at 2026-06-30 against 386000 at 2026-03-31.",
    "account": "loss contingency, MTN agreement",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"330000\"",
    "paragraph_id": "0001628280-26-055222:facts:LossContingencyEstimateOfPossibleLoss:2026-06-30:srt:RangeAxis=srt:MaximumMember,us-gaap:LossContingenciesByNatureOfContingencyAxis=aiot:AmendedNetworkServiceAgreementWithMobileTelephoneNetworkProprietaryLimitedMember"
  },
  {
    "id": "estimates_and_discretion_goodwill_translation_quarterly_fact",
    "what_changed": "The goodwill foreign currency translation gain for the quarter is 9067000. Goodwill is 421062000 at 2026-06-30 against 411995000 at 2026-03-31. Translation is the only goodwill movement tagged for the quarter, and no impairment fact appears.",
    "account": "goodwill",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30",
    "quote": "\"value\": \"9067000\"",
    "paragraph_id": "0001628280-26-055222:facts:GoodwillForeignCurrencyTranslationGainLoss:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_goodwill_translation_annual_fact",
    "what_changed": "The fiscal 2026 goodwill foreign currency translation gain is 22660000. The 10-Q and 10-K both tag it. Goodwill is 383146000 at 2025-03-31 and 411995000 at 2026-03-31.",
    "account": "goodwill",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31",
    "quote": "\"value\": \"22660000\"",
    "paragraph_id": "0001628280-26-055222:facts:GoodwillForeignCurrencyTranslationGainLoss:2025-04-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_warranty_accrual_balance_fact",
    "what_changed": "The product warranty accrual is:\n- 3618000 at 2025-03-31\n- 3507000 at 2025-06-30\n- 2202000 at 2026-03-31\n- 2123000 at 2026-06-30\nIts noncurrent portion is 1199000 at 2026-06-30 against 2134000 at 2025-06-30, and its current portion is 924000 against 959000 at 2026-03-31.",
    "account": "product warranty accrual",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"2123000\"",
    "paragraph_id": "0001628280-26-055222:facts:ProductWarrantyAccrual:2026-06-30"
  },
  {
    "id": "estimates_and_discretion_warranties_issued_fact",
    "what_changed": "Warranties issued in the quarter are 225000 against 97000 a year earlier. ProductWarrantyExpense is 334000 against 229000; the translation effect is 30000 against 66000.",
    "account": "product warranty",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"225000\"",
    "paragraph_id": "0001628280-26-055222:facts:ProductWarrantyAccrualWarrantiesIssued:2026-04-01..2026-06-30"
  },
  {
    "id": "narrative_signs_of_operating_pressure_selling_and_marketing_expense_fact",
    "what_changed": "Segment selling and marketing expense is 21168000 against 17597000 a year earlier.",
    "account": "selling and marketing expense",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"21168000\"",
    "paragraph_id": "0001628280-26-055222:facts:SellingAndMarketingExpense:2026-04-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=aiot:AIoTAssetManagementMember"
  },
  {
    "id": "narrative_signs_of_operating_pressure_general_and_administrative_expense_fact",
    "what_changed": "Segment general and administrative expense is 33081000 against 33275000 a year earlier.",
    "account": "general and administrative expense",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"33081000\"",
    "paragraph_id": "0001628280-26-055222:facts:GeneralAndAdministrativeExpense:2026-04-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=aiot:AIoTAssetManagementMember"
  },
  {
    "id": "estimates_and_discretion_research_and_development_expense_annual_fact",
    "what_changed": "Fiscal 2026 R&D expense per the 10-K is 18359000 against 16061000 for fiscal 2025. The trend table's R&D-capitalization adjustment is insufficient: capitalized development cost is not tagged, and years 2 to 5 of R&D are missing. The adjusted earnings and book value therefore do not exist.",
    "account": "research and development",
    "expected_direction": "up",
    "horizon": "fiscal year ended 2026-03-31 against fiscal year ended 2025-03-31",
    "quote": "\"value\": \"18359000\"",
    "paragraph_id": "0001628280-26-043187:facts:ResearchAndDevelopmentExpense:2025-04-01..2026-03-31"
  },
  {
    "id": "earnings_quality_research_and_development_expense_quarterly_fact",
    "what_changed": "R&D expense for the quarter is 4360000 against 4857000 a year earlier. The release prints incurred R&D of 8,559 against 9,283 and capitalized R&D of (3,702) against (4,923), in thousands; see across_documents_research_and_development_capitalized_untagged.",
    "account": "research and development",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "\"value\": \"4360000\"",
    "paragraph_id": "0001628280-26-055222:facts:ResearchAndDevelopmentExpense:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_raw_materials_inventory_fact",
    "what_changed": "Raw materials inventory, net of reserves, is 7272000 at 2026-06-30 against 8495000 at 2026-03-31. Finished goods are 14373000 against 13953000.",
    "account": "inventory components",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"7272000\"",
    "paragraph_id": "0001628280-26-055222:facts:InventoryRawMaterialsNetOfReserves:2026-06-30"
  },
  {
    "id": "across_documents_adjusted_ebitda_definition_change",
    "what_changed": "The release changed its adjusted EBITDA definition. After reviewing SEC guidance on non-GAAP measures, it stopped adding back the recognition of pre-October 1, 2024 Fleet Complete contract assets and conformed comparatives. It still prints those recoveries as 'Other cash items': 1,503 (prior-year quarter) and 851 (this quarter), in thousands. Adjusted EBITDA as now defined is 20,137 and 21,528.",
    "account": "adjusted EBITDA (non-GAAP)",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 and comparatives as re-presented",
    "quote": "Following a detailed review of relevant SEC guidance on disclosure of non-GAAP financial measures, we have stopped including this adjustment in our presentation of adjusted EBITDA.",
    "paragraph_id": "0001493152-26-036746:8k_2_02:83"
  },
  {
    "id": "across_documents_contract_asset_recoveries_in_operating_cash",
    "what_changed": "The release says invoiced recoveries of the pre-acquisition Fleet Complete contract asset ($1.5 million prior year, $0.9 million this quarter) sit inside operating cash flow. The 10-Q tags the current contract asset at 3536000 at 2026-06-30 against 5017000 at 2026-03-31, and operating cash flow at 8443000 against 4721000.",
    "account": "contract assets and operating cash flow",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "During the same periods, we also invoiced recoveries of $1.5 million and $0.9 million, respectively, which are included in cash flows from operating activities in the condensed consolidated statement of cash flows.",
    "paragraph_id": "0001493152-26-036746:8k_2_02:84"
  },
  {
    "id": "revenue_recognition_product_revenue_delayed_by_production_constraint",
    "what_changed": "The release says $3.2 million of product revenue was delayed by a production constraint late in the quarter. It affected a single product line through a compatibility issue with a new component, and production is being restored. Tagged product revenue is 16480000 against 17657000.",
    "account": "product revenue",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30, with recovery expected later in fiscal 2027",
    "quote": "$3.2 million of product revenue was delayed by a production constraint late in the quarter",
    "paragraph_id": "0001493152-26-036746:8k_2_02:29"
  },
  {
    "id": "revenue_recognition_revenue_timing_shift_between_quarters",
    "what_changed": "The release calls the constraint a discrete production and revenue-recognition timing issue. It anticipates some associated second-quarter revenue may shift into the third quarter, with the balance expected to be recaptured within the fiscal year. No figure for the amount shifting exists in my input.",
    "account": "revenue timing",
    "expected_direction": "down",
    "horizon": "fiscal 2027 second and third quarters",
    "quote": "the Company anticipates that some associated Q2 revenue may shift into Q3",
    "paragraph_id": "0001493152-26-036746:8k_2_02:30"
  },
  {
    "id": "across_documents_south_african_revenue_against_africa_geography",
    "what_changed": "The release says South African revenue was about $1.6 million lower in the quarter, reflecting the early impact of the reprioritization; it does not say lower than what. The 10-Q's Africa geography revenue is 29230000 against 25462000 a year earlier, including RTS revenue since acquisition of 1328000. A South Africa-only revenue figure does not exist in my input, so the two cannot be reconciled here.",
    "account": "revenue, South Africa / Africa",
    "expected_direction": "none",
    "horizon": "quarter ended 2026-06-30",
    "quote": "African revenue was approximately $1.6 million lower in the quarter",
    "paragraph_id": "0001493152-26-036746:8k_2_02:29"
  },
  {
    "id": "results_against_expectations_revised_revenue_guidance",
    "what_changed": "Full-year fiscal 2027 revenue guidance is $468 million to $473 million. The release calls it an update reflecting the South African reprioritization, under which the company is forgoing portions of projected non-strategic South African revenue. The prior guidance figure does not exist in my input, so the size of the revision cannot be stated; the direction rests on the release's own words. Fiscal 2026 revenue tagged in the 10-K is 443777000.",
    "account": "revenue guidance",
    "expected_direction": "down",
    "horizon": "fiscal year ending 2027-03-31",
    "quote": "Revenue is expected to range from $468 million to $473 million, representing approximately 6% year-over-year growth at the midpoint.",
    "paragraph_id": "0001493152-26-036746:8k_2_02:38"
  },
  {
    "id": "results_against_expectations_net_loss_guidance",
    "what_changed": "Full-year fiscal 2027 net loss guidance is $6 million to $8 million. The first quarter alone printed a net loss attributable of $8.4 million (NetIncomeLoss -8440000), already above the top of the full-year range. The prior guidance figure does not exist in my input.",
    "account": "net loss guidance",
    "expected_direction": "none",
    "horizon": "fiscal year ending 2027-03-31",
    "quote": "Net loss is expected to range from $6 million to $8 million",
    "paragraph_id": "0001493152-26-036746:8k_2_02:39"
  },
  {
    "id": "results_against_expectations_adjusted_ebitda_guidance",
    "what_changed": "Full-year fiscal 2027 adjusted EBITDA guidance is $111 million to $114 million. It is measured on the definition changed this quarter. First-quarter adjusted EBITDA printed 21,528 thousand. The prior guidance figure does not exist in my input.",
    "account": "adjusted EBITDA guidance (non-GAAP)",
    "expected_direction": "none",
    "horizon": "fiscal year ending 2027-03-31",
    "quote": "Adjusted EBITDA is expected to range from $111 million to $114 million",
    "paragraph_id": "0001493152-26-036746:8k_2_02:40"
  },
  {
    "id": "results_against_expectations_free_cash_flow_guidance",
    "what_changed": "Full-year fiscal 2027 free cash flow guidance is $20 million to $23 million. First-quarter free cash flow printed (529) thousand. The prior guidance figure does not exist in my input.",
    "account": "free cash flow guidance (non-GAAP)",
    "expected_direction": "none",
    "horizon": "fiscal year ending 2027-03-31",
    "quote": "Free cash flow is expected to range from $20 million to $23 million, consistent with the revised adjusted EBITDA guidance.",
    "paragraph_id": "0001493152-26-036746:8k_2_02:41"
  },
  {
    "id": "across_documents_total_debt_against_tagged_debt",
    "what_changed": "The release's total outstanding debt is $278.4 million and net debt is $241.7 million. Its debt table prints 280,024 at 2026-03-31 and 278,392 at 2026-06-30. In the 10-Q, 278392000 is tagged only as the carrying amount in the fair value table (LongTermDebtFairValue). LongTermDebt is 236527000, and short-term bank loans are 42410000. Liquidity in the release is cash of $32.8 million plus capacity of $29.9 million, matching tagged cash of 32824000 and remaining capacity of 29907000.",
    "account": "total debt and net debt",
    "expected_direction": "down",
    "horizon": "balance at 2026-06-30 against 2026-03-31",
    "quote": "was $278.4 million, and net debt (net of cash, cash equivalents, and restricted cash) was $241.7 million.",
    "paragraph_id": "0001493152-26-036746:8k_2_02:35"
  },
  {
    "id": "across_documents_inventory_reserve_charge_untagged",
    "what_changed": "The release's cash flow prints an inventory reserve add-back of 193 (prior-year quarter) and 558 (this quarter), in thousands. The trend table's inventory_reserve_ratio is missing because us-gaap:InventoryValuationReserves is not in the record for this period, and no tagged fact for the quarter in input_numbers.json carries 558. The reserve balance does not exist in my input.",
    "account": "inventory reserve",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Inventory reserve |  |  | 193 |  |  |  | 558 |  |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:74"
  },
  {
    "id": "across_documents_research_and_development_capitalized_untagged",
    "what_changed": "The release prints R&D in thousands:\n- incurred: 8,559 against 9,283\n- capitalized: (3,702) against (4,923)\n- expensed: 4,857 against 4,360\nThe 10-Q tags ResearchAndDevelopmentExpense at 4360000 against 4857000 and cash paid to develop software at 4100000 against 3724000. The trend table says the record tags no us-gaap:CapitalizedComputerSoftwareAdditions in any period. The release's capitalized figure of 4,923 differs from the 4,100 software cash outflow, and the input does not say how they relate.",
    "account": "capitalized research and development",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Research and development capitalized |  |  | (3,702 | ) |  |  | (4,923 | ) |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:90"
  },
  {
    "id": "earnings_quality_products_gross_profit_margin_release",
    "what_changed": "The release prints products gross profit margin of 25.1% (prior-year quarter) against 21.3% (this quarter). Services gross margin is 60.2% against 61.1%; total is 54.2% against 55.2%. Tagged product revenue is 16480000 against 17657000; cost of products is 12970000 against 13228000.",
    "account": "products gross margin",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Products gross profit margin |  |  | 25.1 | % |  |  | 21.3 | % |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:88"
  },
  {
    "id": "narrative_signs_of_operating_pressure_non_gaap_sales_and_marketing_ratio",
    "what_changed": "The release prints non-GAAP sales and marketing expense as a share of revenue at 17.2% against 19.9%. Non-GAAP S&M is 17,958 against 22,043 thousand. Tagged segment S&M is 17597000 against 21168000.",
    "account": "sales and marketing expense ratio (non-GAAP)",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Non-GAAP sales and marketing expenses as a percentage of total revenue |  |  | 17.2 | % |  |  | 19.9 | % |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:90"
  },
  {
    "id": "earnings_quality_adjusted_net_income_release",
    "what_changed": "The release prints adjusted net income (loss) of 961 (prior-year quarter) against (1,690) (this quarter), in thousands. Adjusted EPS is 0.01 against (0.01). The income tax effect of adjustments is (562) against (1,704).",
    "account": "adjusted net income (non-GAAP)",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Adjusted net income (loss) |  | $ | 961 |  |  | $ | (1,690 | ) |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:86"
  },
  {
    "id": "liquidity_and_capital_free_cash_flow_release",
    "what_changed": "The release prints free cash flow of (7,101) against (529) thousand. It is built from operating cash flow (4,721 against 8,443), capitalized software (3,724 against 4,100) and capex (8,114 against 4,873), all of which match the tagged facts.",
    "account": "free cash flow (non-GAAP)",
    "expected_direction": "up",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Free cash flow |  | $ | (7,101 | ) |  | $ | (529 | ) |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:94"
  },
  {
    "id": "across_documents_restructuring_related_expenses_against_tagged_charges",
    "what_changed": "The release adds back restructuring-related expenses of 2,442 (prior-year quarter) and 1,038 (this quarter), in thousands, to adjusted EBITDA and non-GAAP SG&A. The 10-Q tags RestructuringCharges of 727000 for the quarter and 1995000 (severance) for the prior-year quarter. The release figure and the tagged charge differ in both quarters, and the input does not show the bridge.",
    "account": "restructuring",
    "expected_direction": "down",
    "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
    "quote": "| Restructuring-related expenses |  |  | 2,442 |  |  |  | 1,038 |  |",
    "paragraph_id": "0001493152-26-036746:8k_2_02:81"
  },
  {
    "id": "controls_audit_and_filings_chief_financial_officer_change",
    "what_changed": "The release announces a new President & CFO, Paul Lalljie, previously a strategic finance advisor to the company. The prior CFO, David Wilson, stays in a consulting capacity for several months. The 8-K list also shows Item 5.02 filings on 2026-05-22 and 2026-07-21; those lines carry no paragraph id.",
    "account": "chief financial officer",
    "expected_direction": "none",
    "horizon": "from 2026-08-10",
    "quote": "Paul Lalljie joins Powerfleet this week as President & Chief Financial Officer following a role as a strategic finance advisor to the Company in recent months.",
    "paragraph_id": "0001493152-26-036746:8k_2_02:26"
  }
]
```

## Seen in the notes

No fact in input_numbers.json carries a field saying whether its element sat inside a note. The facts carry `id`, `paragraph_id`, `tag`, context, unit, decimals, value, form, source accession, filing date and sometimes `superseded_by`. Deciding which facts came from note tables would mean judging it myself, which the instructions rule out, so this section holds no items. Every fact-based item above stays under the statements heading. These include:
- revenue by geography
- debt maturities and facilities
- the allowance roll-forward
- warranty
- restructuring
- goodwill
- the MTN contingency
- fair value
- share-based compensation

When a later version supplies the in-note marker, those items can be split here without re-deriving anything.

```json
[]
```
