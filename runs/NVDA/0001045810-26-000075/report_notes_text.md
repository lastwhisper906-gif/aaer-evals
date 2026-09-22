# NVDA — notes and text reader report

Filing read: 10-Q 0001045810-26-000075 (quarter ended July 26, 2026), against the prior-period 10-Q 0001045810-26-000052. Earnings release 8-K 0001045810-26-000073 filed 2026-08-26.

Method note: the notes file I was given is post-diff. Paragraphs marked `[same as prior period, unchanged from ...]` carry no item. Paragraphs printed in full are treated as text that differs from the prior period; where the note change history covers the tag (contingencies, significant accounting policies, debt, debt securities, investments, schedule of debt instruments) I used the explicit added/changed/removed markers instead. I performed no arithmetic: every direction below is what the prose asserts or implies, not a computed value.

## items

```json
[
  {
    "id": "receivables-extended-payment-terms-policy",
    "what_changed": "The supplemental information note now states that for investment-grade customer purchases the company has provided and may provide payment terms of 90 days up to one year to assist customers with large data center builds; the prior period note carried only the general statement that payment is due shortly after delivery.",
    "account": "accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter and next quarter",
    "quote": "Payment from customers is generally due shortly after delivery of our products. In certain cases, for investment-grade customer purchases, we have and may in the future provide longer payment terms ranging from 90 days up to one year to assist customers with large data center builds depending on size.",
    "paragraph_id": "0001045810-26-000075:notes:54"
  },
  {
    "id": "receivables-operating-cash-flow-explanation",
    "what_changed": "MD&A now attributes the offset to operating cash flow specifically to an increase in accounts receivable caused by extended payment terms on large multi-quarter agreements with certain investment-grade customers. This causal attribution for receivables was not in the prior-period liquidity discussion.",
    "account": "accounts receivable, net; net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Cash provided by operating activities increased in the first half of fiscal year 2027 compared to the first half of fiscal year 2026 due to higher revenue, partially offset by an increase in accounts receivable due to extended payment terms on large multi-quarter agreements with certain investment-grade customers.",
    "paragraph_id": "0001045810-26-000075:mdna:84",
    "explanation": true
  },
  {
    "id": "receivables-financing-arrangements-will-continue",
    "what_changed": "MD&A adds a forward statement that customer financing arrangements, including extended payment terms under large multi-quarter agreements, will continue to affect the timing of operating cash flows.",
    "account": "accounts receivable, net; net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Financing arrangements with certain investment-grade customers, including extended payment terms under large, multi-quarter agreements, will continue to affect the timing of our operating cash flows.",
    "paragraph_id": "0001045810-26-000075:mdna:110"
  },
  {
    "id": "receivables-concentration-five-customers",
    "what_changed": "The note now names five direct customers each at or above 10% of the accounts receivable balance at the quarter-end date, where the January 25, 2026 balance date is disclosed with three such customers.",
    "account": "accounts receivable, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Five direct customers accounted for 22%, 14%, 13%, 11%, and 10% of our accounts receivable balance as of July 26, 2026. Three direct customers accounted for 25%, 18%, and 13% of our accounts receivable balance as of January 25, 2026.",
    "paragraph_id": "0001045810-26-000075:notes:53"
  },
  {
    "id": "customer-financing-capacity-constraint",
    "what_changed": "MD&A adds a statement that AI clouds and AI model makers currently lack the ability to secure long-term infrastructure contracts and investment-grade financing capacity, and that the company is itself providing guarantees of land, power, shell and capacity to address this.",
    "account": "accounts receivable, net; revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We believe AI clouds and AI model makers have significant demand for training and inference compute and currently lack the ability to secure long-term infrastructure contracts and investment-grade financing capacity to secure the AI infrastructure necessary to grow.",
    "paragraph_id": "0001045810-26-000075:mdna:17"
  },
  {
    "id": "inventory-provisions-recognized-in-cost-of-revenue",
    "what_changed": "The inventory footnote states the quarter and first-half inventory provisions recognized in cost of revenue for both fiscal years.",
    "account": "inventories; inventory provisions in cost of revenue",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We recognized inventory provisions of $784 million and $886 million for the second quarter, and $1.6 billion and $3.2 billion for the first half, of fiscal years 2027 and 2026, respectively, in Cost of revenue.",
    "paragraph_id": "0001045810-26-000075:notes:57"
  },
  {
    "id": "excess-inventory-purchase-obligation-provisions",
    "what_changed": "The accrued liabilities footnote states the amounts recognized in cost of revenue for excess inventory purchase obligations for the quarter and first half of both fiscal years.",
    "account": "excess inventory purchase obligations (accrued and other current liabilities)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We recognized $201 million and $137 million for the second quarter, and $501 million and $3.1 billion for the first half, of fiscal years 2027 and 2026, respectively, in Cost of revenue.",
    "paragraph_id": "0001045810-26-000075:notes:62"
  },
  {
    "id": "inventory-h200-charge-demand-diminished",
    "what_changed": "MD&A newly discloses a first-half charge for H200 excess inventory and purchase obligations and gives the cause: demand for H200 products diminished. The prior period discussed H20, not H200.",
    "account": "inventories; excess inventory purchase obligations",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the first half of fiscal year 2027, we incurred a $0.4 billion charge associated with H200 for excess inventory and purchase obligations, as the demand for H200 products diminished.",
    "paragraph_id": "0001045810-26-000075:mdna:24",
    "explanation": true
  },
  {
    "id": "inventory-provision-and-release-gross-margin-effect",
    "what_changed": "MD&A quantifies current-year provisions for inventory and excess inventory purchase obligations, the offsetting provision release from sales of previously reserved inventory and settlements, and the net unfavourable gross margin effect.",
    "account": "inventory reserves; gross margin",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Provisions for inventory and excess inventory purchase obligations totaled $985 million and $2.1 billion for the second quarter and first half of fiscal year 2027, respectively. Sales of previously reserved inventory and settlements of excess inventory purchase obligations resulted in a provision release of $177 million and $280 million for the second quarter and first half of fiscal year 2027, respectively. The net effect on our gross margin was an unfavorable impact of 0.8% and 1.0% in the second quarter and first half of fiscal year 2027, respectively.",
    "paragraph_id": "0001045810-26-000075:mdna:65",
    "explanation": true
  },
  {
    "id": "rubin-transition-and-supply-constraints",
    "what_changed": "MD&A states that the next-generation Vera Rubin architecture began production shipments in the third quarter of fiscal 2027, that both Blackwell and Rubin will ship, and that the company is currently experiencing certain supply constraints. A two-architecture ship plus an acknowledged constraint is new.",
    "account": "inventories; revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Our next-generation Data Center architecture, Vera Rubin, began production shipments in the third quarter of fiscal year 2027. We will be shipping both Blackwell and Rubin systems in the future and are currently experiencing certain supply constraints.",
    "paragraph_id": "0001045810-26-000075:mdna:14"
  },
  {
    "id": "supply-and-capacity-commitments-increase",
    "what_changed": "The contingencies note is restructured into a commitments table by fiscal year and states that supply commitments were increased from the prior quarter's figure to the current figure, primarily for memory and manufacturing facilities.",
    "account": "purchase commitments; inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We have partnered with our extensive network to secure the necessary supply and critical components needed to meet demand for the next several years, increasing supply commitments from $119 billion last quarter to $279 billion as of July 26, 2026.",
    "paragraph_id": "0001045810-26-000075:notes:99"
  },
  {
    "id": "china-h200-licenses-unusable",
    "what_changed": "MD&A now says the USG granted H200 licences but PRC restrictions have prevented selling all licensed product, and that shipments made account for less than 1% of Data Center revenue.",
    "account": "revenue (China)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The U.S. government, or USG, granted licenses that would allow us to ship small amounts of H200 products to specific China-based customers, but such sales were restricted by the PRC government, and we have been unable to sell all the products for which we have licenses.",
    "paragraph_id": "0001045810-26-000075:mdna:24"
  },
  {
    "id": "h200-tariff-absorbed",
    "what_changed": "MD&A newly discloses a 25% tariff on H200s imported into the United States under the licensing programme and states the company has been unable to pass any of it to customers and does not anticipate doing so.",
    "account": "cost of revenue; gross margin",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As a result, any H200s shipped under the new licensing program are subject to a 25% tariff upon importation into the United States. We have been unable to pass along any of the tariff to our customers, and do not anticipate doing so in the event we are able to sell licensed products into the China market.",
    "paragraph_id": "0001045810-26-000075:mdna:24"
  },
  {
    "id": "customer-advances-in-deferred-revenue",
    "what_changed": "The deferred revenue footnote now discloses the customer-advance component of the short-term deferred revenue balance at both balance sheet dates; customer advances are now a named, quantified component.",
    "account": "deferred revenue (accrued and other current liabilities)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The balance as of July 26, 2026, and January 25, 2026, included $2.8 billion and $160 million of customer advances, respectively.",
    "paragraph_id": "0001045810-26-000075:notes:61"
  },
  {
    "id": "deferred-revenue-additions-from-advances",
    "what_changed": "The deferred revenue rollforward footnote states that customer advances make up the bulk of first-half deferred revenue additions in both years.",
    "account": "deferred revenue; customer advances",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Included $15.6 billion and $7.5 billion of customer advances for the first half of fiscal years 2027 and 2026, respectively.",
    "paragraph_id": "0001045810-26-000075:notes:70"
  },
  {
    "id": "senior-notes-issued-june-2026",
    "what_changed": "The debt note adds an issuance of senior unsecured notes across seven tranches in June 2026 for general corporate purposes; the debt table adds seven new tranches that showed no balance at the prior fiscal year end.",
    "account": "long-term debt; interest expense",
    "expected_direction": "up",
    "horizon": "this quarter and next quarter",
    "quote": "In June 2026, we issued an aggregate of $25.0 billion of senior unsecured notes across seven tranches for general corporate purposes.",
    "paragraph_id": "0001045810-26-000075:notes:90"
  },
  {
    "id": "covenant-non-financial-qualifier-dropped",
    "what_changed": "The covenant compliance sentence no longer describes the required covenants as non-financial in nature; the prior period sentence said the covenants were non-financial.",
    "account": "long-term debt",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of July 26, 2026, we complied with the required covenants under the outstanding notes.",
    "paragraph_id": "0001045810-26-000075:notes:93"
  },
  {
    "id": "sb-energy-openai-guarantee",
    "what_changed": "A new guarantee, entered in August 2026 after the balance sheet date, capped at $105 billion, supporting an OpenAI affiliate's leases at an SB Energy campus, with amounts stepping up as each of nine construction phases completes and the first effective date expected in fiscal 2029. The guarantee table of maximum gross exposure including this item is new.",
    "account": "guarantees — maximum gross exposure (off-balance-sheet)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In August 2026, we entered into guarantees, capped at a total of $105 billion, to provide credit support on a land, power, and shell buildout with affiliates of SB Energy Corp. (SB Energy) on behalf of a customer, an affiliate of OpenAI Group PBC (OpenAI), related to leases for approximately 4.25 gigawatts of IT load in the aggregate at SB Energy’s PORTS Technology Campus in Pike County, Ohio.",
    "paragraph_id": "0001045810-26-000075:notes:113"
  },
  {
    "id": "ai-cloud-guarantees-as-credit-derivatives",
    "what_changed": "The derivatives note adds a heading and paragraph classifying the land, power and shell guarantees for AI cloud partners as credit derivatives whose fair values are not significant, with changes in fair value in Other income, net; the notional is shown in the derivatives table.",
    "account": "derivative liabilities; other income, net",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We entered into land, power, and shell guarantees for select AI cloud partners’ data center lease obligations in the event of their default. The guarantees are classified as credit derivatives, the fair values of which were not significant, with changes in fair values recognized in Other income, net.",
    "paragraph_id": "0001045810-26-000075:notes:83"
  },
  {
    "id": "public-company-warrants-level-3",
    "what_changed": "New disclosure that warrants on publicly-traded common stock were received during the quarter, recognized in Other assets as equity derivatives with the corresponding benefit substantially deferred, with a Level 3 fair value stated and a new notional line in the derivatives table; an equity forward contract notional also appears for the first time.",
    "account": "other assets; other income, net",
    "expected_direction": "up",
    "horizon": "this quarter and next quarter",
    "quote": "In the second quarter of fiscal year 2027, we received warrants to purchase shares of publicly-traded common stock with terms of three to five years. These warrants are classified as equity derivatives, initially recognized within Other assets, with the corresponding benefit substantially deferred. Subsequent valuation changes are recognized in Other income, net.",
    "paragraph_id": "0001045810-26-000075:notes:84"
  },
  {
    "id": "ecosystem-equity-investments-scale",
    "what_changed": "MD&A now quantifies aggregate ecosystem equity investments and equity investment commitments as of the balance sheet date; the prior period disclosed only an investment commitment total in the notes.",
    "account": "non-marketable securities; marketable equity securities; investing cash flow",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We have made, and may continue to make, investments and commitments in our ecosystem to enhance our growth opportunities, cultivate our ecosystem, and strengthen our competitive position. These include equity investments of $99 billion and equity investment commitments of $25 billion as of July 26, 2026.",
    "paragraph_id": "0001045810-26-000075:mdna:19"
  },
  {
    "id": "equity-method-vie-exposure",
    "what_changed": "The investments note replaces the prior infrastructure-fund equity method paragraph with a new one naming infrastructure financiers, stating a maximum loss exposure including future committed amounts, and adding a VIE non-consolidation conclusion that was not previously disclosed.",
    "account": "non-marketable securities; off-balance-sheet VIE exposure",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We had $3.3 billion of investments in infrastructure financiers accounted for using the equity method as of July 26, 2026. Those equity method investments deemed to be variable interest entities, or VIEs, had a maximum loss exposure, including carrying values and future committed amounts, of $4.7 billion as of July 26, 2026. We have determined we are not the primary beneficiary of our VIE investments and, therefore, do not consolidate the VIEs in our consolidated financial statements.",
    "paragraph_id": "0001045810-26-000075:notes:52"
  },
  {
    "id": "non-marketable-cumulative-unrealized-gains",
    "what_changed": "The cumulative gross unrealized gains and the cumulative losses and impairments on non-marketable equity securities are restated at new levels; the accompanying footnote now says unrealized gains, losses and impairments all run through Other income, net, where the prior footnote referred only to unrealized gains.",
    "account": "non-marketable securities; other income, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Non-marketable equity securities had cumulative gross unrealized gains of $9.1 billion and $661 million, and cumulative gross unrealized losses and impairments of $250 million and $93 million as of July 26, 2026, and July 27, 2025, respectively.",
    "paragraph_id": "0001045810-26-000075:notes:50"
  },
  {
    "id": "publicly-held-equity-unrealized-gains-volatility",
    "what_changed": "The note now gives quarter and first-half net unrealized gains on publicly-held equity securities held at period end for both fiscal years and restates that these securities are subject to market price volatility; the prior period gave a single first-quarter figure.",
    "account": "marketable equity securities; other income, net",
    "expected_direction": "none",
    "horizon": "this quarter and next quarter",
    "quote": "Publicly-held equity securities are subject to market price volatility. Net unrealized gains on investments in publicly-held equity securities held at period end were $1.5 billion and $12.5 billion for the second quarter and first half of fiscal year 2027, respectively.",
    "paragraph_id": "0001045810-26-000075:notes:39"
  },
  {
    "id": "other-income-driven-by-unrealized-marks",
    "what_changed": "MD&A states that gains from equity securities, net, were primarily driven by unrealized gains, making a large share of below-the-line income mark-derived rather than realized.",
    "account": "other income, net; net income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Other income, net, primarily consists of realized or unrealized gains and losses from investments in non-marketable securities and publicly-held equity securities. Gains from equity securities, net, were primarily driven by unrealized gains in equity securities.",
    "paragraph_id": "0001045810-26-000075:mdna:73"
  },
  {
    "id": "ai-cloud-partner-business-model",
    "what_changed": "A new business model introduced this quarter in which AI cloud partners buy NVIDIA data center infrastructure while NVIDIA commits to buy cloud services from them, with a stated commitment total, typical six-year duration, partner right to resell capacity, and a potential revenue share to NVIDIA.",
    "account": "revenue; cloud service commitments",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Under these agreements, AI clouds procure our data center infrastructure products and we commit to cloud service agreements, which the AI clouds can unilaterally stop providing to us and sell to third-party customers at more advantageous rates. Our commitments, which are typically six years in duration, totaled $36 billion as of July 26, 2026, and decrease as capacity is used by third-party customers or by us for our research and development efforts.",
    "paragraph_id": "0001045810-26-000075:mdna:20"
  },
  {
    "id": "indirect-customer-concentration-estimate",
    "what_changed": "MD&A adds an estimate that one AI research and deployment company contributed a meaningful amount of revenue indirectly, by purchasing cloud services from NVIDIA's customers.",
    "account": "revenue concentration",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We estimate that one AI research and deployment company contributed a meaningful amount of our revenue by purchasing cloud services from our customers in the second quarter and first half of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:60"
  },
  {
    "id": "market-platform-reclassification-and-recast",
    "what_changed": "A second presentation change within the year: a company was reclassified from AI Clouds, Industrial, & Enterprise to Hyperscale during the quarter and prior period revenue for that company was recast, on top of the first-quarter change in revenue-by-market-platform presentation.",
    "account": "revenue by market platform (disclosure)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "In the first quarter of fiscal year 2027, we changed our presentation of revenue by market platform, and the comparable periods were recast. During the second quarter of fiscal year 2027, we reclassified a company from AI Clouds, Industrial, & Enterprise (ACIE) to Hyperscale due to a change in their business model and recast the prior period revenue associated with this company.",
    "paragraph_id": "0001045810-26-000075:notes:155"
  },
  {
    "id": "securities-litigation-appeal-sentence-removed",
    "what_changed": "The sentence disclosed last quarter that NVIDIA had petitioned the Ninth Circuit under Rule 23(f) for permission to appeal the class certification order no longer appears; the paragraph now ends at class certification, and the note continues to state no accrued contingent liabilities.",
    "account": "accrued contingent liabilities (loss contingencies)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On April 8, 2026, NVIDIA filed a petition with the Ninth Circuit for permission to appeal the district court’s order pursuant to Federal Rule of Civil Procedure 23(f).",
    "paragraph_id": "0001045810-26-000052:note_history:26"
  },
  {
    "id": "unrealized-loss-disclosure-condensed",
    "what_changed": "The category-by-category table of debt securities in a continuous unrealized loss position, and the sentence attributing those losses to interest rate changes, were removed and replaced by one sentence stating the aggregate amount in a loss position for less than twelve months and calling the related losses not significant.",
    "account": "marketable debt securities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of July 26, 2026, and January 25, 2026, debt securities of $42.0 billion and $13.1 billion, respectively, in a continuous loss position had been so for less than 12 months, and the related unrealized losses were not significant.",
    "paragraph_id": "0001045810-26-000075:notes:43"
  },
  {
    "id": "effective-tax-rate-increase-explained",
    "what_changed": "The tax note states the effective rate increased and gives the cause: a lower percentage of benefits from stock-based compensation, foreign-derived deduction eligible income and the federal research credit relative to the increase in pre-tax income.",
    "account": "income tax expense; effective tax rate",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The effective tax rate increased primarily due to a lower percentage of tax benefits from stock-based compensation, foreign-derived deduction eligible income, and the U.S. federal research tax credit relative to the increase in income before income tax.",
    "paragraph_id": "0001045810-26-000075:notes:130"
  },
  {
    "id": "research-and-development-expense-drivers",
    "what_changed": "MD&A attributes the R&D increase to compute infrastructure and to compensation and benefits, and quantifies the compute infrastructure and compensation growth rates for the first time at this level of detail.",
    "account": "research and development expense",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The increases in research and development expenses for the second quarter and first half of fiscal year 2027 were primarily driven by a 127% and 120% increase in compute infrastructure, respectively, and a 30% increase in each fiscal year 2027 period in compensation and benefits, including stock-based compensation, reflecting employee growth and compensation increases.",
    "paragraph_id": "0001045810-26-000075:mdna:69"
  },
  {
    "id": "dividend-per-share-increase",
    "what_changed": "The equity note states the quarterly dividend was raised from $0.01 to $0.25 per share on May 18, 2026 and gives the resulting cash dividends paid in the quarter and first half; an additional $80.0 billion of repurchase authorization was approved the same day.",
    "account": "dividends paid; financing cash flow",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We paid cash dividends to our shareholders of $6.0 billion and $244 million during the second quarter, and $6.3 billion and $488 million during the first half, of fiscal years 2027 and 2026, respectively. On May 18, 2026, we increased our quarterly cash dividend from $0.01 per share to $0.25 per share.",
    "paragraph_id": "0001045810-26-000075:notes:137"
  },
  {
    "id": "goodwill-increase-compute-networking",
    "what_changed": "The intangibles note states goodwill increased in the first half and that the increase was allocated to the Compute & Networking reporting unit.",
    "account": "goodwill",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In the first half of fiscal year 2027, goodwill increased by $293 million, which was allocated to our Compute & Networking reporting unit.",
    "paragraph_id": "0001045810-26-000075:notes:32"
  },
  {
    "id": "groq-license-payment",
    "what_changed": "MD&A names a payment related to Groq, Inc. as a driver of financing cash flows, and the accrued liabilities footnote now identifies accrued purchase consideration as relating to the Groq, Inc. non-exclusive license agreement.",
    "account": "accrued purchase consideration (accrued and other current liabilities); financing cash flow",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Cash used in financing activities was flat in the first half of fiscal year 2027 compared to the first half of fiscal year 2026, mainly due to higher share repurchases, dividends, and a payment related to Groq, Inc. in the first half of fiscal year 2027, offset by higher cash proceeds from debt issuance.",
    "paragraph_id": "0001045810-26-000075:mdna:86"
  },
  {
    "id": "unearned-stock-based-compensation",
    "what_changed": "The compensation note states aggregate unearned stock-based compensation expense and the weighted average periods over which it will be recognized.",
    "account": "stock-based compensation expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of July 26, 2026, aggregate unearned stock-based compensation expense was $19.4 billion, which is expected to be recognized over a weighted average period of 2.6 years for RSUs, PSUs, and market-based PSUs, and 0.9 years for ESPP.",
    "paragraph_id": "0001045810-26-000075:notes:21"
  },
  {
    "id": "third-party-data-center-leases",
    "what_changed": "New disclosure of approximately fifteen-year data center leases not yet commenced that the company entered into and expects to reassign to third parties, presented in a separate additional-commitments table alongside the AI cloud agreements.",
    "account": "operating lease assets; operating lease liabilities; commitments",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We have entered into data center leases with terms of approximately fifteen years that are expected to commence between fiscal year 2028 and fiscal year 2029. The expected lease start dates are subject to and dependent on timing of construction completion. We expect to reassign these data center leases to third parties.",
    "paragraph_id": "0001045810-26-000075:notes:110"
  },
  {
    "id": "third-party-financing-platform-mous",
    "what_changed": "MD&A discloses August 2026 memorandums of understanding with capital providers to mobilize more than $500 billion of third-party capital, states they may not lead to definitive agreements, and says NVIDIA may at its option provide limited residual-value support on specific projects.",
    "account": "none (off-balance-sheet arrangements)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "In August 2026, we entered into memorandums of understanding with several large capital providers to establish independent financing platforms designed to mobilize more than $500 billion of third-party capital over time to support the deployment of AI infrastructure. These and other preliminary arrangements may not lead to definitive agreements.",
    "paragraph_id": "0001045810-26-000075:mdna:21"
  },
  {
    "id": "q3-revenue-outlook",
    "what_changed": "The earnings release gives a third-quarter revenue outlook and states that no Data Center compute revenue from China is assumed in it.",
    "account": "revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Revenue is expected to be $108.0 billion, plus or minus 2%. NVIDIA is not assuming any Data Center compute revenue from China in its outlook.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:15"
  },
  {
    "id": "q3-gross-margin-outlook",
    "what_changed": "The earnings release gives a third-quarter gross margin outlook on both GAAP and non-GAAP bases, with GAAP and non-GAAP operating expense outlooks stated separately.",
    "account": "gross margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "GAAP and non-GAAP gross margins are expected to be 74.0%, plus or minus 50 basis points.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:16"
  },
  {
    "id": "federal-tax-payment-timing",
    "what_changed": "MD&A adds that two federal income tax payments were made in the second quarter against none in the first quarter, a timing statement that was not in the prior period.",
    "account": "income taxes payable; operating cash flow",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We made two federal income tax payments in the second quarter of fiscal year 2027, as compared with no estimated tax payments in the first quarter of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:91"
  }
]
```

## insufficient

1. **Controls.** `input_controls.md` holds only the current Item 4. It says disclosure controls were effective as of July 26, 2026, that there were no changes in internal control over financial reporting during the quarter that materially affected or are reasonably likely to materially affect it, and that a phased ERP upgrade is continuing. With no prior-period controls text in my directory I cannot say what, if anything, changed, so I raise no item.
2. **Auditor's report.** No auditor's report or interim review report is in my inputs.
3. **Item 1A diff, Exhibit 21 diff, Exhibit 10.** Not present. For 8-Ks other than the 2.02 earnings release I have only the item-code list, so the body of the 2026-08-17 filing carrying items 1.01, 2.03 and 7.01 — the one whose codes suggest a material agreement and a direct financial obligation — was not available to read. That filing sits inside the window and its absence is the largest gap in this report.
4. **Prior predictions.** `input_prior_predictions.md` records none for this company, so no earlier flag or management explanation is carried forward and nothing here is a follow-up.

Counts: 41 items, of which 3 carry `explanation: true` (`receivables-operating-cash-flow-explanation`, `inventory-h200-charge-demand-diminished`, `inventory-provision-and-release-gross-margin-effect`). 4 insufficient.

Not raised as items, on the substance rule: the fiscal-calendar paragraph (only the quarter label changed; the 14-week fourth quarter was already disclosed last quarter), the indemnification paragraph ("recognized" for "recorded"), the warranty attribution sentence (only the period label changed), and the reordering of the commitments note into tabular form where the underlying commitment categories were already disclosed.
