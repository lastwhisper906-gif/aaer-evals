# NVDA 10-Q (0001045810-26-000075), notes text reader

Comparison period: 0001045810-26-000052, the prior quarter's 10-Q.

## Input check

- **Files read:** `input_notes.md`, `input_notes_history.md`, `input_mdna.md`, `input_controls.md`, `input_8k.md` and `input_prior_predictions.md`.
- **Forbidden material:** none found. There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no prior-run probabilities and no outcome window.
  - The 8-K earnings release (Ex. 99.1) contains the full condensed statements. That is an 8-K body, which I am allowed to see. I did not do any arithmetic on it.
- **Inputs missing from the directory:**
  - the auditor's report (none is attached for this 10-Q)
  - the Item 1A diff
  - the Exhibit 21 diff
  - any Exhibit 10

  I can say nothing about risk-factor or subsidiary changes.
- **Prior flags:** none on record.
- **Controls file:** it has no unchanged/changed markers, so I cannot tell whether anything in Item 4 is new.

## Summary

- 40 items in total.
- `explanation: true` on 5 items: T01, T10, T12, T13 and T30.
  - T30 is flagged because management explains, and makes a forward statement about, a reserve-type balance, the excess inventory purchase obligations.
- `insufficient: true` on 6 items: T08, T28, T33, T38, T39 and T40.
- Directions are what the prose implies, not something I computed. Where the prose gives two figures without saying which way they moved, the direction is `none` and the comparison is left to the numbers reader.

## Items

```json
[
  {
    "id": "T01",
    "what_changed": "MD&A now says that operating cash flow was partly offset by an increase in accounts receivable, and attributes that increase to extended payment terms on large multi-quarter agreements with investment-grade customers.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by an increase in accounts receivable due to extended payment terms on large multi-quarter agreements with certain investment-grade customers",
    "paragraph_id": "0001045810-26-000075:mdna:84",
    "explanation": true
  },
  {
    "id": "T02",
    "what_changed": "The supplemental note now discloses that the company has given, and may give, investment-grade customers payment terms of 90 days up to one year for large data center builds. The paragraph is not marked as carried unchanged from the prior period.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In certain cases, for investment-grade customer purchases, we have and may in the future provide longer payment terms ranging from 90 days up to one year to assist customers with large data center builds depending on size.",
    "paragraph_id": "0001045810-26-000075:notes:54",
    "explanation": false
  },
  {
    "id": "T03",
    "what_changed": "A forward statement in MD&A says that extended payment terms and financing arrangements with investment-grade customers will keep affecting when operating cash is collected.",
    "account": "Accounts receivable, net / operating cash flow",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Financing arrangements with certain investment-grade customers, including extended payment terms under large, multi-quarter agreements, will continue to affect the timing of our operating cash flows.",
    "paragraph_id": "0001045810-26-000075:mdna:110",
    "explanation": false
  },
  {
    "id": "T04",
    "what_changed": "The receivables concentration disclosure now names five direct customers at 10% or more of accounts receivable as of July 26, 2026. The text names three for January 25, 2026.",
    "account": "Accounts receivable, net (concentration)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Five direct customers accounted for 22%, 14%, 13%, 11%, and 10% of our accounts receivable balance as of July 26, 2026.",
    "paragraph_id": "0001045810-26-000075:notes:53",
    "explanation": false
  },
  {
    "id": "T05",
    "what_changed": "New MD&A language says that AI clouds and AI model makers lack long-term infrastructure contracts and investment-grade financing capacity. This describes the credit profile of a customer group that the company is now supporting with guarantees and commitments.",
    "account": "Accounts receivable, net (collectability) / guarantees",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We believe AI clouds and AI model makers have significant demand for training and inference compute and currently lack the ability to secure long-term infrastructure contracts and investment-grade financing capacity to secure the AI infrastructure necessary to grow.",
    "paragraph_id": "0001045810-26-000075:mdna:17",
    "explanation": false
  },
  {
    "id": "T06",
    "what_changed": "The commitments note has been rewritten. It now says that supply commitments increased from $119 billion last quarter to $279 billion, and that they are primarily for memory and manufacturing facilities, across current and future architectures. MD&A repeats this in mdna:16.",
    "account": "Purchase obligations (off-balance sheet) / Inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "increasing supply commitments from $119 billion last quarter to $279 billion as of July 26, 2026",
    "paragraph_id": "0001045810-26-000075:notes:99",
    "explanation": false
  },
  {
    "id": "T07",
    "what_changed": "The cancelability wording on supplier agreements has changed. The removed prior text said the agreements 'are cancellable, able to be rescheduled, or adjustable'. The current text says they 'may be cancelable, rescheduled, or adjustable'. This is a hedged statement about the company's flexibility under $279 billion of commitments.",
    "account": "Purchase obligations / Excess inventory purchase obligations",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "in certain instances, these agreements may be cancelable, rescheduled, or adjustable for our business needs prior to placing firm orders",
    "paragraph_id": "0001045810-26-000075:notes:99",
    "explanation": false
  },
  {
    "id": "T08",
    "what_changed": "MD&A says that the scale and complexity of production 'has caused and could in the future cause' increased inventory provisions and, continuing into mdna:16, increased warranty costs. The paragraph is not marked unchanged, but the prior text is not in my input, so I cannot confirm that this sentence is new.",
    "account": "Inventory provisions / Product warranty",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The scale and size of our production needs and the complexity of producing our data center systems has caused and could in the future cause delays in production, challenges in managing supply and demand, revenue volatility, quality issues, increased inventory provisions",
    "paragraph_id": "0001045810-26-000075:mdna:14",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "T09",
    "what_changed": "MD&A says the next architecture, Vera Rubin, began production shipments in Q3 FY27 and that the company will ship both Blackwell and Rubin. This is an architecture transition during which inventory and provisions may move.",
    "account": "Inventories / inventory provisions",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Our next-generation Data Center architecture, Vera Rubin, began production shipments in the third quarter of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:14",
    "explanation": false
  },
  {
    "id": "T10",
    "what_changed": "MD&A discloses a $0.4 billion first-half charge for H200 excess inventory and purchase obligations. It attributes the charge to diminished H200 demand after PRC restrictions.",
    "account": "Inventory provisions / Excess inventory purchase obligations",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the first half of fiscal year 2027, we incurred a $0.4 billion charge associated with H200 for excess inventory and purchase obligations, as the demand for H200 products diminished.",
    "paragraph_id": "0001045810-26-000075:mdna:24",
    "explanation": true
  },
  {
    "id": "T11",
    "what_changed": "MD&A says that H200s shipped under the U.S. license carry a 25% import tariff, that none of it has been passed to customers, and that the company does not expect to pass it on.",
    "account": "Cost of revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We have been unable to pass along any of the tariff to our customers, and do not anticipate doing so in the event we are able to sell licensed products into the China market.",
    "paragraph_id": "0001045810-26-000075:mdna:24",
    "explanation": false
  },
  {
    "id": "T12",
    "what_changed": "MD&A attributes provision releases to sales of previously reserved inventory and settlements of excess inventory purchase obligations. This is management's account of what reduced the reserves in Q2 and the first half.",
    "account": "Inventory reserve / Excess inventory purchase obligations",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Sales of previously reserved inventory and settlements of excess inventory purchase obligations resulted in a provision release of $177 million and $280 million for the second quarter and first half of fiscal year 2027, respectively.",
    "paragraph_id": "0001045810-26-000075:mdna:65",
    "explanation": true
  },
  {
    "id": "T13",
    "what_changed": "The warranty roll-forward table has changed: it now shows three- and six-month columns with new additions and utilization figures. The only accompanying prose attributes the additions to the Compute & Networking segment. It does not explain utilization or the level of the balance. The sentence stating the warranty liability balance was removed (note_history:32).",
    "account": "Product warranty liability",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the second quarter and first half of fiscal years 2027 and 2026, the additions in product warranty liabilities primarily related to our Compute & Networking segment.",
    "paragraph_id": "0001045810-26-000075:notes:119",
    "explanation": true
  },
  {
    "id": "T14",
    "what_changed": "The deferred revenue footnote now states the customer-advance amounts included in the balance at July 26, 2026 and at January 25, 2026. The prose does not describe a direction.",
    "account": "Deferred revenue (customer advances)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The balance as of July 26, 2026, and January 25, 2026, included $2.8 billion and $160 million of customer advances, respectively.",
    "paragraph_id": "0001045810-26-000075:notes:61",
    "explanation": false
  },
  {
    "id": "T15",
    "what_changed": "MD&A says a new business model was introduced in Q2 FY27. Select AI cloud partners buy NVIDIA data center infrastructure, and NVIDIA commits to cloud service agreements with them (about $36 billion, typically six years). NVIDIA may also share in the AI clouds' revenue from third parties.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In the second quarter of fiscal year 2027, we introduced a new business model with certain select AI cloud partners, to enable broader access to our data center infrastructure products to serve AI startups, model builders, enterprises, research organizations, and sovereign customers.",
    "paragraph_id": "0001045810-26-000075:mdna:20",
    "explanation": false
  },
  {
    "id": "T16",
    "what_changed": "A new category, 'Additional Commitments', now appears. It says that AI clouds buy NVIDIA's products while NVIDIA commits to buy cloud services from those same AI clouds, and that the AI clouds may stop providing that capacity. This is a two-way arrangement with the same counterparty.",
    "account": "Cloud service commitments (off-balance sheet) / R&D expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Under these agreements, AI clouds procure our data center infrastructure products and we commit to cloud service agreements, which the AI clouds can unilaterally stop providing to us and sell to third-party customers at more advantageous rates.",
    "paragraph_id": "0001045810-26-000075:notes:108",
    "explanation": false
  },
  {
    "id": "T17",
    "what_changed": "The note now discloses the August 2026 SB Energy guarantees, capped at $105 billion, given on behalf of an OpenAI affiliate. The note says each guarantee takes effect when its lease commences, with the first phase expected in fiscal year 2029, and that exposure falls over each phase's 20-year lease. The guarantees table now totals $108.5 billion of maximum gross exposure.",
    "account": "Guarantees / contingent liabilities",
    "expected_direction": "none",
    "horizon": "beyond 12 months (first phase expected fiscal year 2029)",
    "quote": "In August 2026, we entered into guarantees, capped at a total of $105 billion, to provide credit support on a land, power, and shell buildout with affiliates of SB Energy Corp. (SB Energy) on behalf of a customer, an affiliate of OpenAI Group PBC (OpenAI)",
    "paragraph_id": "0001045810-26-000075:notes:113",
    "explanation": false
  },
  {
    "id": "T18",
    "what_changed": "The note now says that, in exchange for the SB Energy guarantees, the site will host only NVIDIA AI infrastructure. The guarantee is tied to future product sales to the guaranteed party's site.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "beyond 12 months",
    "quote": "In exchange for the guarantees, the site will exclusively host NVIDIA AI infrastructure, subject to limited exceptions.",
    "paragraph_id": "0001045810-26-000075:notes:113",
    "explanation": false
  },
  {
    "id": "T19",
    "what_changed": "MD&A discloses August 2026 memorandums of understanding with capital providers for financing platforms meant to mobilize more than $500 billion. It says NVIDIA may, at its option, provide limited residual-value support.",
    "account": "Guarantees / contingent liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "At our option, we may provide limited residual-value support for a portion of specific projects, subject to disciplined risk management and project-by-project evaluation.",
    "paragraph_id": "0001045810-26-000075:mdna:21",
    "explanation": false
  },
  {
    "id": "T20",
    "what_changed": "A new category covers data center leases signed for third parties: about $20 billion in the table, roughly 15-year terms, and commencement expected in FY2028 to FY2029. The company says it expects to reassign these leases to third parties.",
    "account": "Operating lease liabilities / lease commitments",
    "expected_direction": "up",
    "horizon": "beyond 12 months (fiscal years 2028-2029)",
    "quote": "We expect to reassign these data center leases to third parties.",
    "paragraph_id": "0001045810-26-000075:notes:110",
    "explanation": false
  },
  {
    "id": "T21",
    "what_changed": "The equity method paragraph has been rewritten. 'Infrastructure funds' became 'infrastructure financiers'. The paragraph now says some of these investments are VIEs, gives a maximum loss exposure that includes future committed amounts, and states that NVIDIA is not the primary beneficiary and does not consolidate them. The prior text (note_history:72) had no VIE language.",
    "account": "Equity method investments / Non-marketable securities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Those equity method investments deemed to be variable interest entities, or VIEs, had a maximum loss exposure, including carrying values and future committed amounts, of $4.7 billion as of July 26, 2026.",
    "paragraph_id": "0001045810-26-000075:notes:52",
    "explanation": false
  },
  {
    "id": "T22",
    "what_changed": "The equity investment commitments disclosure changed. The prior text (note_history:74) said the commitments were expected to be made through the remainder of fiscal year 2027. They now appear in the commitments table spread over fiscal 2027 to 2030. The recipients are named as AI model makers, infrastructure financiers and other private companies.",
    "account": "Non-marketable securities / equity investment commitments",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We committed to make certain equity investments in AI model makers, infrastructure financiers, and other private companies, subject to certain contingencies.",
    "paragraph_id": "0001045810-26-000075:notes:102",
    "explanation": false
  },
  {
    "id": "T23",
    "what_changed": "The derivatives note has a new section on public company warrants received in Q2 FY27. They are recorded in Other assets with 'the corresponding benefit substantially deferred', later value changes go through Other income, and fair value is a Level 3 measurement. The notional table also adds an equity forward contract line that has no accompanying prose.",
    "account": "Other assets / deferred benefit (liability) / Other income, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These warrants are classified as equity derivatives, initially recognized within Other assets, with the corresponding benefit substantially deferred.",
    "paragraph_id": "0001045810-26-000075:notes:84",
    "explanation": false
  },
  {
    "id": "T24",
    "what_changed": "The lock-up footnote now reports the amount of publicly-held equity investments under short-term lock-up restrictions as of July 26, 2026. The prior-period text gave an April 26, 2026 figure.",
    "account": "Marketable equity securities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Included $36.9 billion of investments that are subject to short-term lock-up restrictions on the ability to sell.",
    "paragraph_id": "0001045810-26-000075:notes:36",
    "explanation": false
  },
  {
    "id": "T25",
    "what_changed": "The Level 2 equity footnote now describes the warrants as 'unregistered'. The prior wording was 'investments in warrants'.",
    "account": "Marketable equity securities (Level 2)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Included investments in unregistered warrants and preferred stock convertible to common stock in public companies.",
    "paragraph_id": "0001045810-26-000075:notes:38",
    "explanation": false
  },
  {
    "id": "T26",
    "what_changed": "MD&A says equity securities gains were driven mainly by unrealized gains, meaning non-cash mark-to-market. The Other income table is not reproduced here.",
    "account": "Other income, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Gains from equity securities, net, were primarily driven by unrealized gains in equity securities.",
    "paragraph_id": "0001045810-26-000075:mdna:73",
    "explanation": false
  },
  {
    "id": "T27",
    "what_changed": "The debt note discloses a $25.0 billion issuance of senior unsecured notes in seven tranches in June 2026.",
    "account": "Long-term debt / Interest expense",
    "expected_direction": "up",
    "horizon": "this quarter (debt); next quarter (interest expense)",
    "quote": "In June 2026, we issued an aggregate of $25.0 billion of senior unsecured notes across seven tranches for general corporate purposes.",
    "paragraph_id": "0001045810-26-000075:notes:90",
    "explanation": false
  },
  {
    "id": "T28",
    "what_changed": "The covenant sentence no longer says the covenants are 'non-financial in nature'; the prior wording is in note_history:40. The text does not say whether the new notes carry financial covenants.",
    "account": "Long-term debt (covenants)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of July 26, 2026, we complied with the required covenants under the outstanding notes.",
    "paragraph_id": "0001045810-26-000075:notes:93",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "T29",
    "what_changed": "The cloud service agreement description now names open-model R&D (Nemotron, Cosmos, GR00T) and autonomous vehicle software. The prior sentence 'Cloud service capacity may be reduced or terminated' was removed (note_history:30).",
    "account": "Cloud service commitments / R&D expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "These commitments provide the cloud infrastructure to support our research and development of our open models, such as NVIDIA Nemotron, Cosmos, and GR00T, and our autonomous vehicle software.",
    "paragraph_id": "0001045810-26-000075:notes:100",
    "explanation": false
  },
  {
    "id": "T30",
    "what_changed": "The supply-commitment paragraph adds a forward warning that changes to supplier agreements may result in additional costs. MD&A (mdna:16) now frames the commitments as having been 'significantly increased' to meet future demand.",
    "account": "Excess inventory purchase obligations",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Changes to these agreements may result in additional costs.",
    "paragraph_id": "0001045810-26-000075:notes:99",
    "explanation": true
  },
  {
    "id": "T31",
    "what_changed": "The securities class action paragraph no longer mentions NVIDIA's April 8, 2026 Rule 23(f) petition to appeal class certification. The current text does not say what happened to the petition. There is still no accrual.",
    "account": "Loss contingency accrual",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "NVIDIA filed a petition with the Ninth Circuit for permission to appeal the district court",
    "paragraph_id": "0001045810-26-000052:note_history:26",
    "explanation": false
  },
  {
    "id": "T32",
    "what_changed": "The tax note now says the effective tax rate increased, and attributes this to benefits from stock-based compensation, foreign-derived income and the research credit making up a smaller share of higher pre-tax income. The 8-K guides full-year GAAP and non-GAAP tax rates of 16% to 18%.",
    "account": "Income tax expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The effective tax rate increased primarily due to a lower percentage of tax benefits from stock-based compensation, foreign-derived deduction eligible income, and the U.S. federal research tax credit relative to the increase in income before income tax.",
    "paragraph_id": "0001045810-26-000075:notes:130",
    "explanation": false
  },
  {
    "id": "T33",
    "what_changed": "MD&A says there were two federal income tax payments in Q2 FY27 and no estimated payments in Q1. The implication is that taxes accrued in Q1 were paid in Q2. The prose does not state any balance direction.",
    "account": "Taxes payable (accrued liabilities) / operating cash flow",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "We made two federal income tax payments in the second quarter of fiscal year 2027, as compared with no estimated tax payments in the first quarter of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:91",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "T34",
    "what_changed": "MD&A says one AI research and deployment company contributed a meaningful amount of revenue indirectly, by buying cloud services from NVIDIA's customers. This reads alongside the SB Energy guarantees given for an OpenAI affiliate (T17).",
    "account": "Revenue (indirect customer concentration)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We estimate that one AI research and deployment company contributed a meaningful amount of our revenue by purchasing cloud services from our customers in the second quarter and first half of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:60",
    "explanation": false
  },
  {
    "id": "T35",
    "what_changed": "A company was moved from ACIE to Hyperscale in Q2 FY27 and its prior-period revenue recast. This is the second market-platform presentation change in two quarters.",
    "account": "Revenue by market platform",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "During the second quarter of fiscal year 2027, we reclassified a company from AI Clouds, Industrial, & Enterprise (ACIE) to Hyperscale due to a change in their business model and recast the prior period revenue associated with this company.",
    "paragraph_id": "0001045810-26-000075:notes:155",
    "explanation": false
  },
  {
    "id": "T36",
    "what_changed": "The Q3 FY27 outlook in the earnings release assumes no Data Center compute revenue from China.",
    "account": "Revenue (China)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "NVIDIA is not assuming any Data Center compute revenue from China in its outlook.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "T37",
    "what_changed": "MD&A cites a payment related to Groq, Inc. in financing cash flows. Accrued purchase consideration in accrued liabilities is footnoted as related to the Groq non-exclusive license agreement (notes:63).",
    "account": "Accrued purchase consideration (accrued and other current liabilities)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a payment related to Groq, Inc. in the first half of fiscal year 2027",
    "paragraph_id": "0001045810-26-000075:mdna:86",
    "explanation": false
  },
  {
    "id": "T38",
    "what_changed": "The note says goodwill increased in the first half and was allocated to Compute & Networking. It does not name the acquisition that produced the goodwill.",
    "account": "Goodwill",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In the first half of fiscal year 2027, goodwill increased by $293 million, which was allocated to our Compute & Networking reporting unit.",
    "paragraph_id": "0001045810-26-000075:notes:32",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "T39",
    "what_changed": "Item 4 reports no material change in ICFR but says a phased ERP upgrade of the core financial systems is continuing. The controls input has no change markers, so I cannot tell whether this language is new this quarter.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "are continuing a phased upgrade of our enterprise resource planning, or ERP, system to update our existing core financial systems.",
    "paragraph_id": "0001045810-26-000075:item_4_controls:7",
    "explanation": false,
    "insufficient": true
  },
  {
    "id": "T40",
    "what_changed": "MD&A warns that customers may postpone buying new architectures because data center infrastructure is unavailable or capital is constrained, which would affect revenue timing and supply chain expenses. The paragraph is changed, but I cannot see the prior text, so I cannot confirm that this sentence is new.",
    "account": "Revenue timing / Inventories / supply chain expenses",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Customers may postpone purchasing new architectures due to the lack of availability of data center infrastructure to deploy our products, constraints on capital to have sufficient funding to purchase our products, or may adopt new technologies more gradually than anticipated, affecting our revenue timing and supply chain expenses.",
    "paragraph_id": "0001045810-26-000075:mdna:16",
    "explanation": false,
    "insufficient": true
  }
]
```

## Notes for the supervisors

- **Management explanations touching receivables, inventory or reserves:** T01, T10, T12, T13 and T30.
  - **T01 (receivables):** the only receivables explanation, and it rests entirely on extended payment terms for investment-grade customers. T02 and T03 give related context.
  - **T13 (warranty):** attributes warranty additions to a segment rather than a cause. I set the flag and did not judge the explanation.
- **Things that relate to each other, noted without comparing any numbers:**
  - The new AI-cloud model (T15/T16): NVIDIA sells to partners and also commits to buy capacity from them.
  - The SB Energy guarantees (T17/T18), given for the same indirect customer that MD&A calls a meaningful revenue source (T34).
  - The customer-financing language (T02, T03, T05).
- **Omitted as no substantive change:**
  - the fiscal-calendar sentence update
  - the ASU 2024-03 wording (an Oxford comma)
  - 'recorded' changed to 'recognized' in the indemnification paragraph
  - date rolls in the paragraphs on commercial paper and accrued contingent liabilities
  - the reordering of the investment tables
