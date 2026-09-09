# Next cycle tasks

This replaces the work ledger. Git and pull requests carry the state; this file
carries the list.

One line per item:

`[ ] title · builds · judge · expected value from · PR`

- **judge** is the command that decides pass or fail.
- **expected value from** is where the judge's numbers came from. It must name
  a source outside the code being built: the filing, the companyfacts JSON, a
  hand computation written into the test, or a value planted on purpose. If the
  honest answer is "a run of the thing this judges", the item is not ready.
- An item with no judge is **needs judgment**. It is never launched. The owner
  reads all of them in one sitting at the next rules version.

Build each item with the `build-item` skill, and brief every agent with the
`dispatch` skill. One worktree, one branch, one pull request per item, auto-merge
on the moment it opens.

The parsers on the git branch `harness/cycle-020` — the numeric extractor, the
note extractor, the MD&A and controls splitters, the 8-K parser, the paragraph
diff, the note history, the trend table, the bundle assembler, the cutoff guard
and the extraction checks — land through their own pull request. Several items
below build on them and assume that has merged.

**They do not arrive judged.** Their fixtures are the ones `lessons.md` records
as self-certified: the expected values were produced by running the code they
judge. Merging that branch imports the parsers and the hole at the same time, so
the first item below re-judges them before anything is built on top. Nothing
lands through its own pull request and thereby escapes the rule this whole file
exists to enforce.

---

## Ready to build

[ ] write the plain-name check · `src/plain_name_check.py` and the post-write hook that calls it · `.venv/bin/python -m pytest tests/test_plain_name_check.py -q` · a letter-number code planted in a fixture file by the test itself, and a filter output that is greped rather than a filter that is inspected — a no-op regular expression fails quietly. It is written rather than ported: the display-name filter lives only inside the old harness, not on this branch and not on the parser branch · PR: #21

[ ] re-judge the parsers that arrive from the parser branch · no new code — a replacement expected-value file per company, and the deletion of every expected value that came from a parser run · `.venv/bin/python -m pytest tests -q` against the replaced fixtures · companyfacts for every numeric expectation, and the filing itself, read by eye, for every section boundary and paragraph count; each replaced value carries a one-line note naming where it came from. Do this before any item below builds on those parsers · PR: #22

[ ] companyfacts fetcher · `src/fetch_companyfacts.py` and one `companyfacts.json` fixture per company, with its sha256 in the manifest · `python3.12 -m pytest tests/test_fetch_companyfacts.py -q` · every `us-gaap` numeric fact in the committed XBRL instance, looked up in companyfacts and matched by value, with every difference listed rather than tolerated · PR: #26

[ ] trend table on companyfacts · `src/trends.py` reading companyfacts instead of a single instance · `python3.12 -m pytest tests/test_trends.py -q` · two claims, because "every ratio for twelve companies over 8 quarters and 5 years" is thousands of values and would become a generator sharing code with the thing it judges: (a) for three named companies and two named periods, every ratio computed by hand and written out term by term in the test; (b) for the rest, each ratio's numerator and denominator asserted equal to the named companyfacts fact and value they came from — a weaker claim than the ratio being right, but one the code under test cannot manufacture · PR:

[ ] fourth-quarter derivation and the dump indicator · `src/fourth_quarter.py` · `python3.12 -m pytest tests/test_fourth_quarter.py -q` · annual and nine-month figures read off the filings for three companies and subtracted by hand in the test · PR:

[ ] quiet-restatement trace · `src/restatement_trace.py` and the ledger line it writes · `python3.12 -m pytest tests/test_restatement_trace.py -q` · a duplicate-period value planted in a copy of the companyfacts fixture, whose planted difference is the expected output · PR:

[ ] articulation checks · `src/articulation.py` · `python3.12 -m pytest tests/test_articulation.py -q` · the cash-flow and balance-sheet lines for receivables, inventory and payables read off the statements of two companies and differenced by hand in the test · PR:

[ ] tag-continuity map · `src/tag_continuity.py` and the map as versioned data · `python3.12 -m pytest tests/test_tag_continuity.py -q` · the two tag names read off the two filings of a company whose revenue tag changed; the expected output is an unbroken series across the change · PR:

[ ] research-and-development-capitalized column · `src/trends.py` · `python3.12 -m pytest tests/test_trends_rnd.py -q` · research and development expense and capitalized development cost read off the filings of two companies and capitalized by hand in the test · PR:

[ ] formula baselines · `src/baselines.py` writing `baselines.json` — Beneish M-score, accruals over assets, net operating assets, Piotroski F-score, Ohlson O-score, Altman Z-score, note cosine similarity, Loughran and McDonald negative share · `python3.12 -m pytest tests/test_baselines.py -q` · each published formula applied by hand to the frozen fixture and written out term by term in the test; the word-list file's sha256 recorded in the manifest · PR:

[ ] Exhibit 21 fetch and diff · `src/exhibits.py` and `input_exhibits.md` · `python3.12 -m pytest tests/test_exhibits.py -q` · the exhibit type read from the submission's SGML header for 12 of 12 companies, never from the filename, plus one subsidiary planted in a copy of a fixture that the diff must report · PR:

[ ] Exhibit 10 fetch on trigger · `src/exhibits.py` · `python3.12 -m pytest tests/test_exhibits_on_trigger.py -q` · a fixture 8-K carrying item 1.01, whose submission index names the exhibit that must be pulled · PR:

[ ] Item 1A splitter and diff · `src/split_sections.py` and `input_risk_factors.md` · `python3.12 -m pytest tests/test_split_risk_factors.py -q` · the section boundaries located by hand in 12 of 12 filings, plus a fixture whose risk factors are reordered without edits, which must yield zero changes · PR: #25

[ ] diff alignment with a multiset and a boilerplate score · `src/diff_periods.py` · `python3.12 -m pytest tests/test_diff_alignment.py -q` · constructed fixtures — one reordered, one retitled, one with a table of a hundred identical cells — whose expected change count is zero by construction · PR: #27

[ ] market module · `src/market.py` writing `input_market.json` · `python3.12 -m pytest tests/test_market.py -q` · abnormal returns computed by hand from a frozen price fixture and written out in the test; an after-close acceptance time that must move reaction day zero to the next trading day and carry the cutoff and the outcome window with it, so the window is still three days and still ends before the outcome window opens; a FINRA row that must attach by publication date and must not attach by settlement date; a two-year short-interest median computed by hand for one company · PR:

[ ] price-source delisting probe · a probe script and one line in `docs/structure_changes.md` · the probe run, exit status checked directly · a ticker known to have been delisted, whose history must come back; the source's own response is the expected value. Probe the three candidates named in the needs-judgment list below, in that order, and stop at the first that returns the history — this item gathers the evidence, it does not pick the source · PR: #24

[ ] per-agent input directory builder · `src/agent_inputs.py` · `python3.12 -m pytest tests/test_agent_inputs.py -q` · the layer table in `docs/INPUT_SPEC.md`, asserted file by file: a reader directory with no price file, a comparer directory with both reader reports and no filing, a supervisor directory with neither a filing nor the market table. The test must also assert the session root, because a directory that holds the right files but sits beside a readable sibling is not isolated — walk up from the root and fail if another agent's directory is reachable · PR: #28

[ ] quote and citation gate at every layer · `src/quote_gate.py` · `python3.12 -m pytest tests/test_quote_gate.py -q` · items planted on purpose — a quote with a changed dash, a quote with trimmed whitespace, a citation naming an id that does not exist — each of which must be dropped, and the drop count written into `input_manifest.json` · PR: #23

[ ] single-agent baseline runner · `src/control_single_agent.py` and the two control files · `python3.12 -m pytest tests/test_control_single_agent.py -q` · the output schema in `docs/CHECKLIST.md`, plus the quote gate, which must pass on the control's own output · PR:

[ ] shuffled-report control runner · `src/control_shuffled.py` and the two control files · `python3.12 -m pytest tests/test_control_shuffled.py -q` · a fixture pair of two companies' reports, where the expected output is that both files are written and that the numbers report and notes report in them came from different companies · PR:

[ ] scorecard template · `src/scorecard.py` and the template it renders · `python3.12 -m pytest tests/test_scorecard.py -q` · a fixture `runs/` directory; the expected output is a rendered scorecard with the Beneish M-score as the first accounting row and both caveat sentences present, with no hand edits anywhere in the path · PR:

[ ] monthly canary scheduled task · the task definition and its ledger line · one dry run, exit status checked directly · a defect planted on a branch on purpose; the expected result is that `refute-check` names it, and either a hit or a miss is appended to `events/ledger.jsonl` · PR:

[ ] narrow the key-note debt rule so it stops sweeping in investment securities · `src/note_history.py` · `python3.12 -m pytest tests/test_note_history.py -q` with the strict expected-failure marks removed · the key-note tag lists recorded per company by the re-judge, read off the two instances with ElementTree and marked against the six topics `docs/INPUT_SPEC.md` names; the rule matches on the bare substring debt, which pulls the available-for-sale and marketable-equity securities tags into four companies' key notes. Found by the re-judge, which widened the recorded blast radius from one company to four · PR:

[ ] stop the cleaner under-dropping, so the carried block count holds for all twelve earnings releases · `src/clean_text.py` · `python3.12 -m pytest tests/test_parse_8k.py tests/test_assemble_bundle.py -q` with the strict expected-failure marks removed · the independently recounted block count already recorded per company, and the bundle's earnings-release paragraph count computed by hand from it; both are strict expected failures today, so a fix turns the suite red until the marks come off. Found by the re-judge · PR:

[ ] pair notes one rule at a time, so a title match cannot take the prior note a later note names by tag · `src/note_history.py` · `python3.12 -m pytest tests/test_note_history.py -q` · a constructed prior and current pair where one current note names a prior note by tag while an earlier current note matches that same prior note by title; the expected change count is zero by construction, and `match_notes` raises `ValueError: list.remove(x): x not in list` on it today. The same defect was found and fixed in `src/diff_periods.pair_sections` by the diff-alignment item, which is where the fix's shape comes from · PR:

[ ] attribute a paragraph that two notes share to both of them · `src/diff_periods.py` · `python3.12 -m pytest tests/test_diff_alignment.py -q`, extended with a pair carried end to end through `notes()` · `notes()` keeps one map of seen paragraphs across sections, so a paragraph printed under two notes goes to whichever prints first; a constructed pair that only reorders the notes then reports changes where its construction says zero. The alignment item's three fixtures hold at the alignment layer, and this is the one path from filing to diff where that zero does not survive · PR:

[ ] stop the cleaner reading the whole document when it is handed a section · `src/clean_text.py` and the splitter call that feeds it · `python3.12 -m pytest tests/test_split_risk_factors.py tests/test_split_mdna.py -q` · the two defects are asserted today, so a fix turns those tests red and the note above them says so. Both values are read off the filings: Seagate's quarterly risk factors span pages 34 to 56 and four bare page numbers arrive in the diff as new risk factors with one as removed; Ciena's whole quarterly risk-factor section is a single safe-harbour paragraph the cleaner drops, so a wording change inside it — `in Item 2 of Part I of this report` where the prior quarter said `in this report` — reads as no change at all. A fix moves `mdna.*.paragraphs`, so every expected value it moves is re-read from the filing in the same change · PR:

[ ] accept a removed paragraph's prior-filing id in the bundle's id list and its resolution gate · `src/assemble_bundle.py` · `python3.12 -m pytest tests/test_assemble_bundle.py -q` · a constructed diff whose removed paragraphs carry the prior filing's ids, which the id list must contain and the resolution gate must resolve. No diff file the bundle carries today has a removed paragraph, so the contract is unwritten rather than broken; the risk-factor diff is the first that will exercise it · PR:

[ ] make the cutoff-guard bypass scan follow indirection · `tests/test_cutoff_guard.py` · `python3.12 -m pytest tests/test_cutoff_guard.py -q` · a fixture read planted by the test through `fetch_fixtures.read_stored`, which the scan must name and does not see today — it reads the call and not what the call is made of, so its claim that no read skips the gate can be true by indirection alone · PR:

---

## Needs judgment

Not launched. No judge exists for these, and inventing one would be inventing the
answer.

[ ] the price source · three candidates, in this order: **Stooq daily bulk zip** — a file download rather than an API call, which is why it survives the scripted-request block, delisted coverage unknown; **WRDS with CRSP through a Stony Brook account** — free if the school subscribes, and delisting returns handled the way the literature handles them, which is the only candidate that answers the delisted question properly; **a low-cost provider such as Tiingo or EODHD** — delisted coverage to be confirmed. Session 1 probed the two obvious free routes and neither served data: Stooq answers a scripted request with a JavaScript proof-of-work under both a plain and a browser user agent, and the Yahoo chart endpoint returns 429 unauthenticated, so the delisted-ticker question is still unanswered and the market module is built against a frozen price fixture. **Must be decided before the pattern study, not before expansion, because the study needs fifteen years of prices.** The project's no-paid-data rule named consensus data, not prices · needs judgment

[ ] thresholds for the four new numeric indicators — `articulation_gap`, `asset_growth_high`, `rnd_capitalization_shift`, `net_stock_issuance` · nothing waits: until rules v0.1 all four report their value and do not flag, so they measure from the first run and contribute nothing to a tier. What size of gap or growth should raise a flag needs the distribution over the 30 past cases, and a threshold is the owner's · needs judgment

[ ] the two-by-two flag thresholds · the accounting flag count grew from 26 to 33 and the pressure count from 16 to 17 while "4 or more" and "3 or more" stayed put, which loosens both tiers · needs judgment

[ ] narrowing the map from SIC code to sector ETF · the default is one ETF per SIC division and it ships with the market module, so nothing waits; whether a finer map by major group gives a better sector return is a modelling choice no test can settle · needs judgment

[ ] whether the review-response branch's published results merge into this history · two published-results histories diverge, and merging them is a claim about the record · needs judgment

[ ] whether the post-write plain-name hook should block the writer · the check names a code on stderr and exits 1; Claude Code hands any non-zero status other than 2 to the person at the keyboard and only 2 back to the agent that wrote the line, so today the writer is not told. Nothing waits: the check runs inside `make check` and CI runs `make check`, so a pull request carrying a code is red either way. Blocking would buy an earlier correction at the price of an interrupted turn, and that price is the owner's · needs judgment

[ ] whether the plain-name check should read source files and directory names · it reads `.py` and `.sh` by name only, because code quotes vocabulary that is not ours — a period offset, a linter's rule in a comment, the codes the check's own test plants — and it reads a file's own name but not the directories above it. The second-vendor lens calls both a blind spot. Widening either needs a rule for which quoted vocabulary is exempt, and a list of language suffixes has no rule to appeal to · needs judgment

[ ] the letter-number codes the archived project left in `CITATION.cff`, `LICENSE` and `LICENSE-docs` · a whole-tree sweep names six occurrences, four in the citation file and one in each licence file. Nothing waits: the check reads what a branch changed, and nothing changes those files. The two licence files are text that is not ours to edit and the citation file is a published record, so what to do with them is not a code change · needs judgment

[ ] the judge line that reads "companyfacts for every numeric expectation" · no expectation in the parser fixtures is a financial figure: each one counts elements, tables or paragraphs inside one document, and companyfacts is the deduplicated standard-taxonomy record across every filing — Apple's annual accession carries 427 facts there against 898 unit-bearing elements in the instance itself. The re-judge sourced every value from the document instead and said so value by value, so nothing waits; whether that line stands as written for the items still to be built is the owner's · needs judgment
[ ] whether the supervisor may see `docs/CHECKLIST.md` · both supervisor prompts say to write against the schema in that document, and from a session rooted at the supervisor's own directory it is unreachable by design. Nothing waits: rules v0.1 does not exist and `docs/INPUT_SPEC.md` section 6 names no file for the checklist keys, so there is nothing to route today. Routing it would put a file that is not a report into a supervisor's directory, which is a change to the layer table and not a code change · needs judgment

[ ] the four branches the second-vendor lens never read · the Codex adversarial review died on an account usage limit, reported as resetting on the ninth of October, against the companyfacts fetcher, the Item 1A splitter, the diff alignment and the per-agent input directories. All four merged on one lens and a green gate. Zero findings from a lens that errored is not an approve, and whether to re-run it over the merged history when the quota returns or to accept those four as read once is the owner's · needs judgment

[ ] the section fallbacks that fire on no committed filing · the annual Item 2 fallback and the quarterly Item 3 through Item 6 fallbacks are exercised by none of the twelve filings on record, and an annual report omitting Item 1B would sweep the cybersecurity item into the risk factors. There is no fixture that judges a rule for it, and constructing one would be inventing the filing rather than reading it · needs judgment
