# Lessons a script enforces, or that no longer apply

Moved out of `lessons.md` on 2026-10-06, when the session-start hook was cut to the
lessons nothing enforces (`docs/reports/prose-rules-2026-10-06.md`). Each lesson is
copied verbatim, oldest first, with its line number in `lessons.md` at commit
1174ce3, and under it one line naming what enforces it or why it is obsolete.
`lessons.md` and this file together hold every lesson `lessons.md` held.

2026-09-06 read a single test failure on the local Python 3.14 venv as a real regression; the canonical interpreter is 3.12 and it passes there — run the canonical interpreter before drawing a conclusion.
  (was line 7) enforced by: `src/interpreter_pin.py`: every entry point refuses an interpreter other than 3.12 (`tests/test_interpreter_pin.py`).

2026-09-06 wrote the append check to forbid any change to a published file, which would have blocked every append to events/ledger.jsonl — a .jsonl ledger grows by design; a test written at the same time caught it.
  (was line 10) enforced by: `tests/test_append_check.py` (`test_appending_to_the_ledger_is_clean`): a ledger append passes, a rewrite fails.

2026-09-06 wrote two letter-number codes into the structure-change record while describing an archived branch; naming an old artifact is not a licence to carry its codes forward — a scan of the new files caught it.
  (was line 11) enforced by: `src/plain_name_check.py`, run by `make check` on every changed document.

2026-09-06 made the one-time archive relocation exemption require an identical blob, which failed on runs/MANIFEST.sha256 because the baseline branch was 171 commits behind the archived tip; ran the check against the real baseline before trusting it.
  (was line 12) obsolete: the archive relocation merged; the one-time exemption in `src/append_check.py` matches no path on main any more, as its docstring says.

2026-09-06 verify-public failed on Python 3.14 (thread pool); would have been reported as a real failure if not rerun on 3.12 — pin the interpreter in scheduled tasks too.
  (was line 13) enforced by: `src/interpreter_pin.py`: every entry point refuses an interpreter other than 3.12 (`tests/test_interpreter_pin.py`).

2026-09-06 wrote the append-only rule into CLAUDE.md as "never edit or delete", which the check itself already contradicted by allowing ledger appends; a rule the code disagrees with is a spec error, not a code error.
  (was line 14) enforced by: `tests/test_append_check.py` holds the rule as `CLAUDE.md` now words it: appending to a ledger passes, changing a published line fails.

2026-09-06 put a README inside runs/, which made the directory's own explanation uncorrectable — the append check refused my first edit to it in CI; documentation does not belong in an append-only directory, and the check now says so in one narrow line.
  (was line 15) enforced by: `src/append_check.py`, run by `make check`: the first correction to a file under `runs/` fails, so documentation there cannot survive.

2026-09-07 do not put documentation inside protected directories; the exception was the wrong fix.
  (was line 16) enforced by: `src/append_check.py`, run by `make check` (see the line above).

2026-09-07 wrote the display-name filter with GNU word boundaries, which macOS sed accepts and silently ignores; the output looked untranslated and only the check that greps that output caught it — a no-op regular expression fails quietly, so test the filter's output, never the filter.
  (was line 18) enforced by: `tests/test_plain_name_check.py` reads the output the check printed, never the pattern; its docstring cites this lesson. The display-name filter itself is no longer in the tree.

2026-09-07 the new signature-queue detector fired on every report the old loop ever wrote; a rule about how work is done now must be floored at the cycle it starts, or it turns frozen records into violations.
  (was line 19) obsolete: the signature-queue detector belonged to the archived harness, which `docs/HOW_WE_WORK.md` §5 lists as dropped.

2026-09-07 the documentation-bloat ratio was measuring archive/ — 3,847 frozen files pinned it where nothing the loop does could move it; a metric over a frozen tree is not a metric.
  (was line 20) obsolete: the documentation-bloat penalty was dropped (`docs/HOW_WE_WORK.md` §5: it measured a frozen tree).

2026-09-07 the harness test command was specified as "python3.12 src/append_check.py && python3.12 -m pytest -q" and both halves were broken — the script form could not import its own package, and bare pytest collected the archive; run a command before writing it into a config.
  (was line 21) obsolete: the harness and its test command are gone; the gate is `make check`, defined once in `Makefile` and run by CI.

2026-09-07 picked the 8-K earnings release by filename pattern and it found five of twelve; filers name EX-99.1 anything (q2fy27pr.htm, ex_994826.htm, a99-q22026earningsexhibit.htm) and the document type is stated in the submission header — a heuristic that works on the first sample is not a rule.
  (was line 22) enforced by: `src/fetch_fixtures.py` takes the earnings release by its type in the submission header (`EX-99.1`, then any `EX-99`), not by file name.

2026-09-07 the loop launcher refused a cold cycle start because assigned rows and no build report read as a build in flight; a condition true at the open of every cycle cannot be the test for in-flight work, or --force becomes the normal way to start.
  (was line 25) obsolete: the loop launcher is gone; scheduled tasks replaced it (`docs/HOW_WE_WORK.md` §5).

2026-09-07 asserted that a note's change entries equal the symmetric difference of its two periods' paragraphs; a changed paragraph consumes one from each side and produces one entry, so the identity is off by the changed count — derive the arithmetic before asserting it.
  (was line 27) enforced by: `tests/test_note_history.py` recomputes how much moved per note by a pairing of its own.

2026-09-07 matched every current paragraph against the first prior paragraph with the same masked text, so a table's hundred identical cells all matched cell one and ninety-nine looked removed; matching one list against another needs a multiset, not an index lookup.
  (was line 28) enforced by: `tests/test_diff_alignment.py` matches one paragraph list against the other as a multiset, and cites this lesson.

2026-09-07 nearly dodged the fixture-read bypass scan by naming a local variable "folder" instead of "runs"; a scan that only greps names is evaded by renaming, so put the read behind the gate module instead of renaming around the check.
  (was line 29) enforced by: `tests/test_cutoff_guard.py`: the bypass scan follows a read to the name it was bound to, so renaming does not evade it.

2026-09-07 assumed the fixture set was a point-in-time set for any triggering report; it holds the latest filing of each form, so a 10-K-triggered bundle loses the 8-K for eleven of twelve companies — check what a fixture set is a snapshot *of* before building a cutoff on it.
  (was line 30) enforced by: `src/cutoff_guard.py` refuses any document filed after the triggering report (`tests/test_cutoff_guard.py`, `tests/test_exhibits_on_trigger.py`).

2026-09-08 wrote acceptance criteria whose numbers lived in a file the builder generated by running the code under test, so ten of twelve items certified themselves; the reproduce lens passed on the circular evidence and only the refute lens caught it — an expected value must come from the source document, never from the first run of the thing it is meant to judge.
  (was line 31) enforced by: `tests/expected_values.py` refuses an expected value that names no source, and `tests/test_expected_values.py` keeps the drift baseline apart from the answer key.

2026-09-08 added seven indicators and moved the threshold that counts them in the same edit; caught it on re-read and put the threshold back — a threshold moved inside the change that adds its inputs is a threshold moved invisibly, and silence in the brief means the existing value stands.
  (was line 33) obsolete: the count of flags against a threshold was removed by the owner's decision of 2026-09-23: the prediction is an anomaly register with no count cut.

2026-09-08 the repository's own .venv runs Python 3.14 while the pin is 3.12 and Homebrew's 3.12 has no pytest, so `make check` cannot pass on this machine as written; the Stop hook that runs it is therefore inert here until requirements are installed into a 3.12 environment.
  (was line 37) obsolete: the project's `.venv` is Python 3.12 now and is the `Makefile` default; `src/interpreter_pin.py` refuses 3.14.

2026-09-08 wrote a layer table saying a comparer sees both reader reports and comparer prompts saying each sees one, so the isolation test would have passed a directory its own prompt calls broken — the same rule in two files is two rules until something reads both.
  (was line 38) enforced by: `tests/test_agent_inputs.py` reads the layer table out of `docs/INPUT_SPEC.md`, so the table and the directories are one rule.

2026-09-08 measured the reaction window from the filing date and then shifted its start for an after-close acceptance, which pushed its end onto the first day of the outcome window; two windows counted from different origins will eventually overlap, so give them one origin.
  (was line 39) enforced by: `tests/test_market.py`: the reaction window, the cutoff and the outcome window move together with day zero, and the window ends before the outcome window opens.

2026-09-08 wrote a labelling rule that needs a two-year median into a table with no median column, for an agent forbidden from arithmetic — a rule an agent cannot evaluate from its input is a rule it evaluates by guessing.
  (was line 40) enforced by: `src/market.py` writes the short-interest ratio's two-year median into the market table (`tests/test_market.py`).

2026-09-08 let the parser branch land through its own pull request while its fixtures were the self-certified ones; routing code around the rule is the same as suspending the rule, and "it lands separately" is how that gets written down.
  (was line 41) enforced by: `tests/expected_values.py` refuses an expected value that names no source, and `tests/test_expected_values.py` keeps the drift baseline apart from the answer key.

2026-09-08 marked the sector map "needs judgment" with no default, which would have stopped the market table, both comparers and two whole steps — a needs-judgment item with no default is a signature queue under a new name.
  (was line 43) enforced by: `src/owner_inbox_check.py`, run by `make check`: an open row in `docs/needs_judgment.md` that names no default in force fails.

2026-09-09 wrote a Stop hook calling bare `make check`, which reaches a system interpreter with no pytest; the hook failed every turn and a failing gate hook reports green by saying nothing, so name the interpreter in the hook, not just in the Makefile default.
  (was line 44) enforced by: `Makefile` (`PYTHON ?= .venv/bin/python`) and the Stop hook name the interpreter; `tests/test_judge_commands.py` runs the judge commands on it.

2026-09-09 wrote a notifier that would have announced the state of the world on its first run; a notifier that speaks when nothing happened is one you stop reading, so the first run records a baseline and says nothing.
  (was line 46) enforced by: `.claude/hooks/notify_if_shipped.sh`: the first run on a branch records the baseline and says nothing.

2026-09-09 ran the second-vendor review against a branch with no commits on it and it answered approve on an empty diff; a lens that passes when it was handed nothing has not run.
  (was line 49) enforced by: `tools/second_lens.sh` refuses an empty diff (`tests/test_second_lens.py`).

2026-09-09 named the check's own test fixture with the prefix the check skips, so a silence assertion passed for the wrong reason; the positive control planted in the same file caught it, which is why every silence assertion carries one.
  (was line 50) enforced by: `tests/test_plain_name_check.py`: every silence assertion carries a planted positive control.

2026-09-09 wrote off the undashed shape as a stated limit without checking which shape this repository had actually got wrong; the one violation on the record was exactly the shape I had excused.
  (was line 52) enforced by: `src/plain_name_check.py`, run by `make check`, which reads the undashed shape (`tests/test_plain_name_check.py`).

2026-09-09 planted the codes as literals in the check's own test, which made the post-write hook report that test on every write for good; reading source files by name only was the fix, and the second-vendor lens is what named it.
  (was line 53) enforced by: `src/plain_name_check.py`, run by `make check`, which reads `.py` and `.sh` files by name only.

2026-09-09 the first version of the check read one shape of the thing it forbids and passed the two codes this repository had written into its own record, plus the ones sitting in the licence and citation files; count both shapes over the frozen archive before choosing one, because a filter's coverage is a measurement and not a definition.
  (was line 54) enforced by: `src/plain_name_check.py`, run by `make check`, which reads both shapes (`tests/test_plain_name_check.py`).

2026-09-09 the kept-vocabulary list said words and never shapes and then carried one shape — any capital tag on a four-digit year — which exempted every code family whose serial fell between 1900 and 2099; an exemption written as a shape is the carve-out the list exists to refuse, and neither review lens found it.
  (was line 58) enforced by: `src/plain_name_check.py`, run by `make check`: its year exemption is `FY` and `CY` only, never any tag on a year (`tests/test_plain_name_check.py`).

2026-09-09 wrote the check, wired its hook, and left it out of the gate, so a pull request could carry a code and merge green; a rule with a hook and no gate is a rule the merge does not know about.
  (was line 59) enforced by: `Makefile`: `check` runs `plain-name-check`, and CI runs `make check`.

2026-09-09 An expected value and a drift baseline sharing one file called expected.json is what let a number produced by running a parser pass for an expectation about the filing it read; separate them by filename and by reader and the confusion cannot recur.
  (was line 64) enforced by: `tests/expected_values.py` refuses an expected value that names no source, and `tests/test_expected_values.py` keeps the drift baseline apart from the answer key.

2026-09-09 One test-side reader that refuses an entry naming no source makes a provenance-free expected value impossible to write and then read; a flat file with two members per entry leaves no depth at which a bare integer can hide.
  (was line 65) enforced by: `tests/expected_values.py` refuses an expected value that names no source, and `tests/test_expected_values.py` keeps the drift baseline apart from the answer key.

2026-09-09 The judge line named companyfacts for every numeric expectation and no key in this file is a financial figure; say which source actually applies and why, rather than working around the mismatch silently.
  (was line 71) obsolete: settled by default in `docs/needs_judgment.md`: a parser expectation is sourced from the document and says so value by value.

2026-09-09 tests/test_fixtures.py's on-disk check excludes files by name, so any new file beside the fixtures fails it for all twelve companies until the exclusion is extended — the edit easiest to miss in a fixture-shape change.
  (was line 73) enforced by: `tests/test_fixtures.py` itself: a stray file beside the fixtures fails it for all twelve companies, loudly.

2026-09-09 expected.json is the drift baseline and is the pipeline's own output by construction; writing a hand-computed number into it makes the ±20% band compare two different things and pass on slack (CARR 122 against 104 used 17 of the 20 points).
  (was line 78) enforced by: `tests/expected_values.py` refuses an expected value that names no source, and `tests/test_expected_values.py` keeps the drift baseline apart from the answer key.

2026-09-09 "Non-empty prose" is not a provenance check: it accepts "somewhere". Name a closed set of source kinds and resolve every file the note cites; anything less lets a parser-produced number be relabelled and pass.
  (was line 81) enforced by: `tests/expected_values.py` names a closed set of source kinds and refuses a note outside it.

2026-09-09 tests/test_cutoff_guard.py's bypass scan reads the call and not what the call is made of, so a fixture reached through fetch_fixtures.read_stored is invisible to it and its "no read skips the gate" can be true by indirection alone.
  (was line 87) enforced by: `tests/test_cutoff_guard.py`: the bypass scan follows `fetch_fixtures.read_stored` (task row merged in #55).

2026-09-09 Bare python3.12 on this machine has no pytest, so an item's stated judge command only runs as .venv/bin/python3.12 -m pytest from inside the worktree — a judge that cannot run is not a green judge.
  (was line 89) enforced by: `tests/test_judge_commands.py` runs every judge command in the task list on the interpreter it names.

2026-09-09 A review lens that exited on a quota error has not read the change: say so in the pull request body and in the ledger, because a green gate beside one lens reads as two lenses to whoever merges.
  (was line 90) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. A lens that did not run exits 3 and the pull request opens labelled `one-lens` with auto-merge off.

2026-09-09 The cleaner's page-number and safe-harbour rules read the whole document while every splitter hands it a section, so page tails survive into a diff and a section whose only paragraph is safe-harbour text cleans down to its heading; input_mdna.md has carried both since before the risk-factor splitter existed.
  (was line 95) enforced by: `tests/test_split_risk_factors.py` records what the shared cleaner does when it is handed a section.
  moved back to lessons.md on 2026-10-07: the test named records the defect, it does not enforce the lesson.

2026-09-09 A rule stated as "X, falling back to Y" is two passes and not one: a single greedy pass let a title match take the prior section a later section was named after by tag, and that later section then fell to the fallback too — run each rule to completion before the next starts.
  (was line 98) enforced by: `tests/test_note_history.py` judges `match_notes` on constructed sections.
  moved back to lessons.md on 2026-10-07: the test named records the defect, it does not enforce the lesson.

2026-09-09 src/note_history.py::match_notes carries that same rule-order defect and raises ValueError: list.remove(x): x not in list when a prior note claimed by a title match is later named by another current note's tag.
  (was line 99) enforced by: `tests/test_note_history.py` judges `match_notes` on constructed sections.
  moved back to lessons.md on 2026-10-07: the test named records the defect, it does not enforce the lesson.

2026-09-09 A defect latent on all twelve real pairs still needs a fixture: the pass-order bug changed no company's change count and reported eight on a constructed pair whose construction says zero.
  (was line 100) enforced by: `tests/test_note_history.py` carries the constructed pair.
  moved back to lessons.md on 2026-10-07: the test named records the defect, it does not enforce the lesson.

2026-09-09 A caller that normalizes upstream hides a case bug in the predicate below it — is_furniture("Total") was False while boilerplate_score("Total"), which lowercases first, was 1.0.
  (was line 101) enforced by: `tests/test_diff_alignment.py` (`test_a_paragraph_is_furniture_or_it_makes_a_claim`).

2026-09-09 An allowance that belongs to the run but is written into the layout turns an unfinished run into a finished one: a may-be-absent flag on the supervisor let a full annual run missing one comparer report build over three reports and exit 0. Tie the allowance to the run that earns it.
  (was line 105) obsolete: the supervisor layer left the live pipeline on 2026-09-28 (`docs/structure_changes.md`).

2026-09-09 A gate that names two of a schema's four probability keys still says "the probabilities were removed"; enumerate the source schema's keys one by one and plant each of them, or the sentence is one nobody checked.
  (was line 106) enforced by: `src/agent_inputs.py` refuses a prior-predictions file that still carries any probability key, and `tests/test_agent_inputs.py` plants each.

2026-09-09 Path.exists() and read_bytes() both follow a symlink, so an already-there check reads a link into the bundle as a file already copied; test is_symlink() before either.
  (was line 107) enforced by: `src/agent_inputs.py` refuses a symlink (`tests/test_agent_inputs.py`).

2026-09-09 resolve() does not see a hardlink, so a check on names alone accepts the market table hardlinked in under a report's name; compare the bytes against the run's copy or the check bounds nothing.
  (was line 109) enforced by: `src/agent_inputs.py` compares bytes; `tests/test_agent_inputs.py` plants a hardlink.

2026-09-09 A substring test against a re-rendered JSON node is normalization wearing a substring test's clothes: it accepts key order and whitespace the reader never saw and refuses a slice copied out of the committed file. Render the node, then locate it in the file, and match against the slice.
  (was line 111) enforced by: `src/quote_gate.py` matches a computed row against the slice of the committed file (`tests/test_quote_gate.py`).

2026-09-09 A JSON fixture dumped from a dict by the same call the code under test uses cannot judge that code's layout; plant the file as characters and assert the expected row is a slice of it before using it.
  (was line 112) enforced by: `tests/test_quote_gate.py` writes its inputs as text and quotes slices of them.

2026-09-09 A paragraph id that names a file plus a JSON pointer makes every file in the directory evidence, the manifest's excluded-paragraph text and the market table included; resolve only the ids a committed input declares.
  (was line 113) enforced by: `src/quote_gate.py` resolves only the ids a committed input declares (`tests/test_quote_gate.py`).

2026-09-09 A per-report id set is not a namespace: an item id repeated anywhere in the run leaves a dropped item citable through its twin, so uniqueness has to be checked across the whole run.
  (was line 114) enforced by: `src/quote_gate.py` refuses an id repeated in the run (`tests/test_quote_gate.py`).

2026-09-09 An id shape a document specifies is only resolvable when every component is printed in the file its reader sees; resolve the id the file prints and leave the divergence named rather than minting a name nobody could produce.
  (was line 116) enforced by: `src/quote_gate.py` indexes the ids the files print and composes none (`tests/test_quote_gate.py`).

2026-09-09 A parser judged only on a fixture in its own shape is not judged: the bulk source's real members head their columns differently and write dates without separators, and the probe read a real one as no rows at all while its constructed fixture passed.
  (was line 117) enforced by: `tests/test_probe_price_sources.py` judges the probe against bodies captured from the sources.

2026-09-09 When the source blocks the download, its file layout is still checkable — a public copy of one bulk member gave the real header and date form, and the parser was judged against that instead of a shape invented for it.
  (was line 118) enforced by: `tests/test_probe_price_sources.py` judges the probe against bodies captured from the sources.

2026-09-09 A row that is a date beside any non-null close counts an error payload as history: a close reading "unavailable" exited the probe green, so require a real calendar date and a finite number before a row exists.
  (was line 119) enforced by: `tests/test_probe_price_sources.py` (an answer reading `unavailable` is not a row).

2026-09-09 A blocked source is still capturable verbatim: the committed browser-check page was 478 bytes where the live page is 796, and the trimmed copy dropped the proof-of-work loop it existed to record. Capture the body, then assert the literal equals the captured file.
  (was line 120) enforced by: `tests/test_probe_price_sources.py`: each captured body is committed byte for byte.

2026-09-09 A catalogue has no sanctioned reader: the date gate refuses it because its recorded date is later than every cutoff, load_index admits only the submissions index by role, and the fetcher's helpers are reserved to the fetcher because the bypass scan cannot see a call made through them. Reading it needs one of the three opened deliberately, not routed around.
  (was line 124) obsolete: `load_catalogue` in `src/cutoff_guard.py` is the sanctioned catalogue reader now (`tests/test_cutoff_guard.py`).

2026-09-09 "Latest filing wins" applied to two periods independently pairs a restated figure with an unrestated one: a year recast in 2025 against nine months last stated in 2023 gave a fourth quarter that was neither. Check the two winners were reported on one basis before subtracting them, the same way a subtraction across two tags is already refused.
  (was line 131) enforced by: `tests/test_fourth_quarter.py` refuses two winners reported on different bases.

2026-09-09 An absence list assembled from the manifest is an input like every other: it named a filing three months past the run's cutoff, and the only test of it ran at the newest cutoff, where nothing is later and the leak cannot show.
  (was line 136) enforced by: `tests/test_restatement_trace.py` cuts the absence list off at the run's cutoff.

2026-09-09 Float subtraction wrote a sixteen-decimal residue into a finding built from two two-decimal values, and the assertion that catches it names no example — a difference never needs more decimal places than the two values it came from.
  (was line 137) enforced by: `src/restatement_trace.py` subtracts in decimal (`tests/test_restatement_trace.py`).

2026-09-09 Skipping a whole period because one filing reported it at two values throws away every other filing's disagreement; leave out the filing, not the period, and stay silent only when the ambiguous filing is the first one.
  (was line 138) enforced by: `tests/test_restatement_trace.py` (a filing that reports one period at two values).

2026-09-09 A catalogue fetched once fails the date gate as a whole document: at the bundle's cutoff, which is the trigger's own filing date, the companyfacts record is refused for eleven of twelve annual triggers, so an extractor reading it produces nothing for the annual trigger until the guard filters its rows the way load_index does for the submissions index.
  (was line 143) enforced by: `src/cutoff_guard.py` `load_catalogue` checks the hash and applies the cutoff to the rows (`tests/test_cutoff_guard.py`).

2026-09-09 A cutoff compared as a string cannot fail closed: a filter on the raw field let the word garbage admit the whole record at exit 0. Parse the date before it filters, never after.
  (was line 146) enforced by: `cutoff_guard.parse_date` refuses a cutoff that is not an ISO date (`tests/test_cutoff_guard.py`, `tests/test_empty_cutoff.py`).

2026-09-09 A reader that filters the rows itself inherits none of the gate's refusals; an unparseable cutoff is refused inside the guard, so the modules that read documents through it get that free and the one that reads the catalogue had to ask for it.
  (was line 147) enforced by: `src/cutoff_guard.py` `load_catalogue` checks the hash and applies the cutoff to the rows (`tests/test_cutoff_guard.py`).

2026-09-09 Both review lenses can be gone at once, and a wave that ships anyway ships whatever the gate cannot see: wave E merged six items with no lens, and the lens run afterwards returned fail on five of them, two of those breaking rules in CLAUDE.md. A green gate is not a review, and a workflow that opens pull requests when its review stages errored is a workflow that treats an outage as an approval.
  (was line 154) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. Neither lens running exits 3, never an approval, and auto-merge stays off.

2026-09-09 A comparison between two scores computed over different subsets rewards abstaining: the scorecard printed that the pipeline beat the baseline while scored on one run against two, which is the failure the checklist has a line about, and the fixture already rendered it the other way with the suite asserting that sentence.
  (was line 158) enforced by: `tests/test_scorecard.py` (scores compared over one set of runs).

2026-09-09 A present-but-malformed input file dropped from both the numerator and the denominator moves a ratio with nothing said; a null value already raised and only the absent key was silent.
  (was line 159) enforced by: `tests/test_scorecard.py` (a malformed input file).

2026-09-09 An acceptance timestamp parsed by a call that accepts a zone offset, then compared against a naive close time, gives two answers for one instant -- and the later one put a day past reaction day two on the market table. Refusing a bare date on that reasoning and then accepting an offset is half a rule.
  (was line 160) enforced by: `tests/test_market.py` (an acceptance time with a zone offset).

2026-09-09 A guard written as a denylist admits everything nobody thought of: the single-agent control refused only names it recognised, so a price file carrying the outcome window and another company's notes were both listed to the model as the whole of what it could see.
  (was line 161) enforced by: `tests/test_control_single_agent.py`: the control's guard is an allowlist.

2026-09-09 A control that checks its labels and not its contents can record the real run as the control: two directories both holding one company's reports passed every guard and were written out as the crossed pair.
  (was line 162) obsolete: the shuffled-report control is retired (owner's decision of 2026-09-23).

2026-09-13 A judge command naming an interpreter that has no pytest exits before it collects a test: six of six ledger commands read `python3.12 -m pytest`, and bare python3.12 on this machine answered every one of them with No module named pytest at exit 1. The substitution the lens makes to get a real number is what hides it.
  (was line 171) enforced by: `tests/test_judge_commands.py`.

2026-09-13 A reproduce lens that only runs the substituted command reports the item green and says nothing about the item's own command; running both, and reporting both exit codes, is what made the hole visible.
  (was line 172) enforced by: `tests/test_judge_commands.py` runs each item's own command.

2026-09-13 An inbox that lists what the owner must decide has to name the default already running beside each row, or the list reads as a queue and the work stops at it.
  (was line 174) enforced by: `src/owner_inbox_check.py`, run by `make check`: an open row in `docs/needs_judgment.md` that names no default in force fails.

2026-09-13 `is_file()` and `read_text()` both follow a symlink, so "the run's own copy" has to refuse a link on the run's side too -- every file handed to the control was byte-compared against a copy that was itself a link to another run's.
  (was line 181) enforced by: `tests/test_control_single_agent.py` refuses a link on the run's side too.

2026-09-13 One schema deserves one gate: the shuffled control skipped `market_direction` whenever the basis was empty while the single-agent control dropped it, and the fixture answer that carried an empty basis was what kept the difference invisible.
  (was line 182) enforced by: `src/prediction_schema.py` is the one checker for the schema (`tests/test_prediction_schema.py`).

2026-09-13 A gate that reads citations judges only the fields citations live in: `tier`, `events`, `p_up` and the rest reached the control file in any shape at all with `dropped_items: 0` beside them, and the fixture answer wrote `finding: "yes"`, a word §7 lists nowhere, for as long as the control existed. A fixture that the code accepts is not evidence that the code is right.
  (was line 183) enforced by: `src/prediction_schema.py` checks every field, not only citations (`tests/test_prediction_schema.py`, `tests/test_control_single_agent.py`).

2026-09-13 A falsy fallback is a default for wrong as well as for absent -- `cutoff or default_cutoff(ticker)` turns an empty cutoff into one months later, at ten call sites across eight readers, and only the reader that had already been burned refuses it.
  (was line 185) enforced by: `tests/test_empty_cutoff.py`: an empty cutoff is refused by every reader that takes one.

2026-09-21 gated the reading of a lens's verdict file on that lens's exit status after writing, in the same file, that a valid verdict file is the answer whatever the exit status — the documentation and the code disagreed and the code won silently.
  (was line 191) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-21 started the fallback lens in the caller's directory while giving the cross-vendor lens the worktree explicitly, so the weekly re-lens routine would have read main and filed the answer against a merge commit.
  (was line 192) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-21 never read the exit status of the ledger append, so a pass whose record was never written would have auto-merged with nothing left for the weekly routine to find.
  (was line 193) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 wrote the allowlist's expected value as the module's own comprehension restated (`{name for name in BUNDLE_CATALOGUE if name.startswith('input_')}`), so a prefix reading that swept in a file no layer sees would have moved the test with it; the second lens caught it, and the expected value now comes off `docs/INPUT_SPEC.md` §6's own list.
  (was line 203) enforced by: `tests/test_agent_inputs.py` reads the allowlist off `docs/INPUT_SPEC.md` §6.

2026-09-22 built a guard that reads names and stopped there, twice over: `input_prior_predictions.md` was admitted with a probability still in it, and another company's prose under an allowed name would have made every id in it resolve — an allowlist answers which name, never whose bytes.
  (was line 204) enforced by: `tests/test_control_single_agent.py`: a handed file's bytes are held against the run's own copy.

2026-09-22 answered "the allowlist reads names, not bytes" by refusing symlinks and directories, which is still names; a plain copy of another company's file under an allowed name went through both lens rounds until the bytes were held against the run's own copy.
  (was line 206) enforced by: `tests/test_control_single_agent.py`: a handed file's bytes are held against the run's own copy.

2026-09-22 read the judge out of the branch under review, five separate times in one design, and each time an approval came back; every hole the nine readings found in the lens was the same mistake -- the thing deciding the verdict was reachable from the change being judged.
  (was line 212) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. The prompt, the schema and the verdict module come from a pinned ref.

2026-09-22 `python -m` puts the current directory ahead of `PYTHONPATH` on `sys.path`, so the pinned reader was imported out of the tree it was pinned against; `cd` into the pin and `PYTHONSAFEPATH=1` are what close it.
  (was line 213) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. (`PYTHONSAFEPATH=1`, run from the pin).

2026-09-22 left the SessionStart hook feeding `lessons.md` verbatim into the lens session, which is the tree under review talking to its own judge; measured with a sentinel -- found in one turn with no tool call, absent only under `--restricted`.
  (was line 214) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. (the fallback starts restricted, with its definition inline).

2026-09-22 judged the two-lens routine on a diff that was empty: 44 of 51 tests left HEAD on `main` and so ran against no change at all, in the harness built to find exactly that hole.
  (was line 215) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 let the weekly re-lens routine reach `pass` on an empty diff -- measured at zero lines for merge commits carrying 2220, 2435 and 594 lines of change, because the range was computed against the wrong parent.
  (was line 216) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 added `lessons.md` to the list of files that define the judge, which would have made every pull request this session exit 3, because `CLAUDE.md` requires appending to that file every session; a guard that fires on all of the work and none of the attack is not a guard.
  (was line 217) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. (a test asserts `lessons.md` is not watched).

2026-09-22 ran the fallback lens with `--restricted`, which drops the Bash tool as well as the project's settings, so the lens could not run the `git diff` its own prompt told it to and read nineteen files without ever seeing the change; the lens reported it itself.
  (was line 218) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 threw away a schema-valid `fail` carrying three findings because one sentence preceded it, and recorded the run as `no_lens_ran`; judging a verdict by the prose around it is judging by a string match, which is what reading the exit status was abandoned for.
  (was line 228) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 added an interpreter probe that asked its question by running `src.lens_verdict` out of the worktree -- the branch under review executing before the pin, in the same session that closed four other versions of exactly that.
  (was line 229) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 wrote a weekly selection as the complement of `main` while the routine itself pins `<merge>^1`, so every row the routine wrote re-qualified the following week, forever; and the test meant to cover that invocation passed `main`, which is the one value the loop excludes.
  (was line 230) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 invoked the lens with an item title that is not a row in `docs/next_cycle_tasks.md`, so the ledger row and the task row it was meant to settle could never have found each other, and nothing was checking.
  (was line 231) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 read the last schema-valid object in a lens's answer as its verdict, so a `fail` followed by a quotation of `PASS_VERDICT` -- which sits in the test file every lens reviewing this project opens -- would have exited 0 and auto-merged; two answers are not an answer, and "the verdict is what the lens ends on" is an assumption about model behaviour inside a function written because the model does not obey instructions.
  (was line 232) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 wrote a test for "the tree's own reader runs before the pin" that invoked the script by absolute path, so `REPO_ROOT` was this repository and not the worktree -- the mutation it was written for passed all 72 tests. A harness has to reproduce the production topology, not the half of it that is easy: the build skill runs `tools/second_lens.sh` by relative path from inside the worktree, and that is the only shape in which the defect exists.
  (was line 233) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. (the harness runs the script by relative path from inside the worktree).

2026-09-22 closed one of five looping sources in the weekly routine and recorded the loop as fixed; the other three looped the same way for the same reason, and the second lens found them one field to the left. A queue over an append-only ledger has to be keyed on the item, because the routine appends a row every time it runs.
  (was line 234) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 closed the two-object case in the verdict reader and left the one-object case open: a quota sentence quoting one valid `pass` was still an approval at exit 0. Recovery from prose may return a `fail` or a `needs_judgment` and never a `pass` -- the risk is not symmetric, so the rule must not be.
  (was line 235) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 wrote the test for "a quota sentence does not become a pass" around `{"note": ...}`, which fails the schema, so it could not tell "the prose was ignored" from "the quotation was judged" and the case it was named for went unjudged.
  (was line 236) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 judged "the answer file would not clear" by making the whole `.lens` directory unwritable, which trips the judge-directory check first -- so both answer-file branches were unreachable in the harness and deleting either `cleared` call left the suite green. The failure has to be injected where it happens, which here is one `rm`.
  (was line 237) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 added a guard refusing an item title that is not a row, and left in the append-only ledger the very row that title had written -- a phantom the weekly queue would report every week and could never close, because the new guard forbids appending under it. A guard added to a queue has to retire what it was written for.
  (was line 238) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 closed the weekly queue on a `codex` row whatever `judge_from` said, so a branch could rewrite `tools/lens_prompt.md`, take a Codex `pass` under questions it wrote itself and never be re-read -- while two other documents said a `tree` row is read again. A queue that closes on the lens's name and not on where its questions came from is closing on the wrong fact.
  (was line 239) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 let a correction line retire any item title, in an append-only ledger the branch under review writes to -- one line naming its own row would have taken a fallback `pass` out of the weekly queue permanently. A retirement has to be refused for work still on the list.
  (was line 240) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 handed both lenses `git diff <pin>...HEAD` while the definition-file check read the working tree, with no commit step between `make check` and the lens call: a `pass` on the committed part and a commit of the rest is an approval the lens never gave.
  (was line 241) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`. (an uncommitted worktree is refused).

2026-09-22 kept a clearing check on the fallback's answer file that had no reachable branch, because the shell redirection writing that file truncates it before the command runs; deleting it left every test passing. Judge the property, not the check.
  (was line 242) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 tested the weekly routine with `HEAD == main` and a named ref for thirteen readings, and never in the shape it actually runs -- detached at a merge commit with the pin at its first parent, which is the shape that produced empty diffs in production and the reason the empty-diff refusal exists.
  (was line 243) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 added an uncommitted-changes refusal that would have retired the weekly re-lens routine outright: the script creates `$WORKTREE/.lens` itself forty lines earlier, and `.lens/` reaches `.gitignore` only in the change that builds the lens -- so every commit the routine re-reads shows `?? .lens/` and exits 3, forever. The harness wrote `.gitignore` into every fixture, so the refusal was judged only where it cannot fire.
  (was line 244) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 guarded the retirement path with "not an open row" read line by line over the whole task list, where every row starts with `[ ] ` including the landed ones -- so the one case retirement exists for, a merge that predates the lens, was the one case it could never reach. The section heading is what says whether a row is open.
  (was line 245) enforced by: `tools/second_lens.sh`, judged by `tests/test_second_lens.py`.

2026-09-22 left `LENS_PYTHON` defaulting to `$REPO_ROOT/.venv/bin/python` with `REPO_ROOT` the worktree under review: git-ignored, invisible to the diff, to the new status refusal and to the definition-file list, and it is what runs the pinned reader and writes the ledger row. Named as the fourth trust root rather than implied closed.
  (was line 246) enforced by: `tools/second_lens.sh` records a caveat when the interpreter resolves inside the tree it judges (`tests/test_second_lens.py`).

2026-09-22 anchored a thirteen-period window on the newest period the record happened to hold, which is the run's own period until the record is older than the trigger -- and two of twelve were, so the quarter before the run wore the current-quarter label and the run's own quarter appeared in no slot; the second lens found it, and the same hole was still open one level down in the year window after the first fix.
  (was line 252) enforced by: `tests/test_trends.py` (the window anchored on the run's own period).

2026-09-22 wrote a period label straight out of the code into lessons.md, where the plain-name check reads it as the letter-number code it is -- the exemption is for .py and .sh, and a lesson about the code is not the code.
  (was line 253) enforced by: `src/plain_name_check.py`, run by `make check`, which reads `lessons.md`.

2026-09-22 read a catalogue of every filing's facts as though every row were a financial statement: a proxy statement's pay-versus-performance net income is filed later than the 10-K's and won "the latest filing wins" for five of Generac's years, and an 8-K recast won thirteen of Carrier's terms.
  (was line 254) enforced by: `tests/test_trends.py` (a proxy statement's figure does not win the latest-filing rule).

2026-09-13 `json.dumps` writes an infinity as the bare token `Infinity` and `json.loads` reads it straight back, so a Python round trip is no evidence at all that a file is JSON. `json.loads(text, parse_constant=refuse)` is what asks. A control file carrying `"point": Infinity` was written, re-read and scored by nobody.
  (was line 272) enforced by: `src/prediction_schema.py` reads with `parse_constant` refusing `Infinity` (`tests/test_prediction_schema.py`).

2026-09-14 Two hand-written lists agreeing with each other is not a reading of the document they both cite. `SUPPORT` mistyped identically in both controls passes the test that compares them; only the test that parses §7 out of `docs/CHECKLIST.md` fails.
  (was line 284) enforced by: `tests/test_control_single_agent.py` parses §7 out of `docs/CHECKLIST.md`.

2026-09-23 moved two controls' schema checks into one function and gave it its own refusals of a third question and of a non-object answer, then judged it only through the two controls, which refuse both shapes first in their own words -- so both new guards were unreachable from every test until a sweep over the new module found them green; a guard added to a shared function needs a direct caller in the tests, because its callers are the reason it is never reached.
  (was line 287) enforced by: `tests/test_prediction_schema.py` calls the shared checker directly.

2026-09-23 wrote the stage runner's report parser from one reader's shape, so the notes report's forty items in one JSON list parsed as a single item with no id; the prompts do not fix the container -- read a report's actual shape before gating it.
  (was line 297) enforced by: `tests/test_run_analysis.py` (`test_report_items_are_read_off_the_fenced_blocks`).

2026-09-24 planted a detect judge where every newer filing sat after the older one and carried the larger accession, so "last row" and "largest accession" both passed while its comment said otherwise; the refute lens found it by mutation.
  (was line 301) enforced by: `tests/test_detect_filing.py`: the planted rows make the first row, the last row and the largest accession each name a wrong filing.

2026-09-29 counted the runs finished by their exit code, which was 0 for four runs whose analysts had failed; a run is finished when every agent's record says written, and the runner now exits non-zero otherwise (#102).
  (was line 320) enforced by: `src/run_analysis.py` exits non-zero unless every agent's record says written (`tests/test_run_analysis.py`, `test_a_failed_analyst_is_named_and_the_run_is_not_finished`).
