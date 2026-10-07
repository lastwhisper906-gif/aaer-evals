# Prose rules: every one gets a script or is deleted — 2026-10-06

The owner's research finding of 2026-10-06 (`docs/structure_changes.md`): prose
rules are followed inconsistently and only scripts enforce, so instructions stay
near a hundred lines. The owner's instruction: every prose rule gets a script or
is deleted. This is what that did to the three files a session reads first.

## Line counts

Every number is what a command printed on the file as committed, run from the
repository root on this branch. "Before" is `git show origin/main:<file> | wc -l`,
the base this branch starts from; for `lessons.md` that is the pre-cut file, the
one the hook used to `cat`, and the same command gives it. "After" is
`wc -l <file>` on this branch. A lesson count is
`grep -c '^[0-9]\{4\}-[0-9][0-9]-[0-9][0-9] '` on the same input, and the
hook's line is `sh tools/session_start_lessons.sh | wc -l`.

| File | Before | After |
|---|---|---|
| `CLAUDE.md` | 22 | 22 |
| `docs/HOW_WE_WORK.md` | 477 | 436 |
| `lessons.md` | 320 (314 lessons) | 211 (201 lessons: 197 kept, 4 written this session) |
| what the SessionStart hook prints | 320 (`git show origin/main:lessons.md \| wc -l`, which `cat lessons.md` printed) | 60 (`sh tools/session_start_lessons.sh \| wc -l`) |

Session-start context is `CLAUDE.md` plus the hook's printout: 342 lines before
(22 + 320), 82 after (22 + 60).

## Rules that became scripts

Each is a check that reads files and exits non-zero, with a test that it fires
and one that it does not, and each runs in `make check`.

| Rule | Where it was prose | Script | Test |
|---|---|---|---|
| Work with no judge is not a task | `CLAUDE.md`; `docs/HOW_WE_WORK.md` §1 principle 2 and §2 | `src/task_judge_check.py` — every open row of `docs/next_cycle_tasks.md` names a judge, every open row of `queue.md` an eval command; a list that yields no row under the headings read is refused, not passed | `tests/test_task_judge_check.py` |
| Never create a state that waits for the owner's signature; everything has a default | `CLAUDE.md`; `docs/HOW_WE_WORK.md` §1 principles 2 and 3 | `src/owner_inbox_check.py` — every open row of `docs/needs_judgment.md` names its default, every settled row says `default:`, and no file outside `archive/` is named as a sign-off queue; an inbox that yields no row is refused, not passed | `tests/test_owner_inbox_check.py` |
| `CLAUDE.md` is capped at 22 lines | `docs/HOW_WE_WORK.md` §4, the fold-lessons routine | `src/instruction_length_check.py` | `tests/test_instruction_length_check.py` |
| Every path `CLAUDE.md`'s parentheses name is in the tree | `CLAUDE.md`'s own header: each rule names what enforces it | `src/instruction_length_check.py --paths` — every token containing `/` that ends in `.py`, `.sh`, `.md`, `.json` or `.jsonl`, or a directory written as `evals/`, exists relative to `CLAUDE.md`; the brackets and quotes around a token and the sentence punctuation after it are stripped first, so `tools/session_start_lessons.sh).` on line 19 is checked; a missing one is named, and `--list` prints every path checked with its line | `tests/test_instruction_length_check.py` |
| Where `CLAUDE.md` says `.claude/settings.json denies` the tools, the file denies them | `CLAUDE.md` line 12 | `src/instruction_length_check.py --paths` — the settings file is read as JSON and `permissions.deny` must hold `Edit(evals/**)` and `Write(evals/**)`; a missing key or entry is named | `tests/test_instruction_length_check.py` |
| Every lesson starts with its date, YYYY-MM-DD and a space | nowhere: the hook told a lesson from the header by its date and nothing said so | `src/instruction_length_check.py --lessons` — after the header, every line of `lessons.md` and `archive/lessons_enforced.md` that is not blank and not indented starts with a date; an indented line is the lesson's note or wrapped line | `tests/test_instruction_length_check.py` |
| The old repo is archived, not rewritten | `docs/HOW_WE_WORK.md` §1 principle 10 and §8 | `src/archive_check.py` — a file already under `archive/` on the baseline is never rewritten or deleted; it may grow at the end, like the ledgers, when the baseline ends in a newline (`archive/lessons_enforced.md` takes each lesson a script comes to enforce this way); a new one passes | `tests/test_archive_check.py` |
| The session-start hook prints the lessons | `CLAUDE.md`; `docs/HOW_WE_WORK.md` §4 hooks | `tools/session_start_lessons.sh` — the header and the newest lessons, newest last, at most sixty lines; a lesson is a dated line plus its wrapped lines, printed whole or not at all | `tests/test_session_start_lessons.py` |

The evals rule in `CLAUDE.md` names `src/eval_guard.py` in CI and the deny rules
in `.claude/settings.json` as its judge; both landed with the evals pull request
(#106, head `20b1a70`), which this branch follows on main. Before that merge
`src/eval_guard.py` and `evals/` did not exist on this branch, so
`src/instruction_length_check.py --paths` (and with it `make rule-checks`)
failed here by design, naming both. The deny half of the same line failed the
same way: `--paths` reads `.claude/settings.json` and requires its
`permissions.deny` to hold `Edit(evals/**)` and `Write(evals/**)`, and before
the rebase the file had no `permissions` key, so a third line named that; a
settings file that merely existed would have passed the earlier reading, and
that was the second lens's finding. The fourth refusal was
`evals/scoreboard.jsonl` on `CLAUDE.md` line 7: `.jsonl` joined the path
suffixes after the sixth reading found the ledger named there unchecked, and
the ledger lands with the same `evals/` directory. Four lines, then, from
`make rule-checks`, all by merge order. On 2026-10-07 the branch was rebased
onto `20b1a70`, where all four paths and both deny entries are in the tree, and
`make rule-checks` printed no refusal: the three checks ran and exited 0. The
one conflict on the rebase was the Makefile's `.PHONY` line, resolved by
keeping both sides' targets.

## Rules an existing script already enforced, now named beside the rule

In `CLAUDE.md`, by a parenthesis on the rule's own line; in `docs/HOW_WE_WORK.md`,
by one line under it.

- Plain names: `src/plain_name_check.py`; item ids: `src/quote_gate.py`.
- Append-only under `runs/`, `rules/`, `events/`, `history/`: `src/append_check.py`.
- Verbatim text, every item verified, failures dropped and counted: `src/quote_gate.py`; the committed inputs: `src/agent_inputs.py`.
- Python does the arithmetic: `src/analysis_check.py`.
- Layers: `src/agent_inputs.py`, `tests/test_agent_inputs.py`.
- Expected values come from the source: `tests/expected_values.py`.
- Cutoff: `src/cutoff_guard.py`, with the bypass scan in `tests/test_cutoff_guard.py`.
- Ground truth is the first-reported value: `src/parse_8k.py`, `src/restatement_trace.py`.
- Scored against its own rules version: `src/scorecard.py`; `rules/` is append-only.
- Retry once with identical input (`docs/HOW_WE_WORK.md` §3): `src/run_analysis.py`.
- No prior run's probability in an agent's input (§8): `src/agent_inputs.py`.
- No rule or threshold changed after its results (§8): `src/append_check.py` on `rules/`.
- Daily prediction-tamper check (§4): `src/append_check.py` in CI; missing-filing check: `src/nightly.py`.

## Rules kept with no script

Judgments no script can hold, kept because they are the owner's:

- Never soften an adverse result (`CLAUDE.md`, §1 principle 11, §8's year-one line).
- The twelve companies test the pipeline, not the signal (`CLAUDE.md`, §8).
- No composite score and no rank across companies (`CLAUDE.md`; the owner's decision of 2026-09-28 in §2).
- Write this session's mistakes to `lessons.md` at session end. §4 already says why no hook can do it.
- Start long runs under `caffeinate -s`. It is about the owner's Mac.
- §8: no new identifier families, ledgers, approval procedures or document systems; no "finds alpha".

## Rules deleted

From `CLAUDE.md`: none. Every line either names its script or is in the list above.

From `docs/HOW_WE_WORK.md`:

| Deleted | Why |
|---|---|
| §2 "An item with no judge is 'needs judgment' and is never launched" | duplicate of §1 principle 2; `src/task_judge_check.py` enforces it |
| §3 "Scheduled-task sessions start from a clone, sparse-checked-out to that company's `runs/` only" | superseded by `docs/routines/nightly-worker.md`, which works from a full clone |
| §3 "if the served model differs from the pin the run is recorded as a failure" | the old model pin, replaced by §6 on 2026-10-06 |
| §4 daily cutoff, quote, layer-isolation, rules-precedence and event-gap re-checks | no script ran them; the nightly worker's `make check` and `make eval` are the nightly check now, and the rules they re-checked are held at build time by `src/cutoff_guard.py`, `src/quote_gate.py` and `src/agent_inputs.py` |
| §4 weekly extraction drift (re-extract the twelve, open an issue) | replaced by the drift check `src/nightly.py` runs on every new bundle |
| §4 weekly schema and hash, unreferenced code, dependencies, document numbers, broken links | no script ran them; superseded by `docs/routines/weekly-gardener.md` |
| §4 weekly "a readable result" | duplicate of §1 principle 13 |
| §4 weekly "fold lessons" | superseded: a lesson a script comes to enforce moves to `archive/lessons_enforced.md`, and the 22-line cap is `src/instruction_length_check.py` |
| §4 "Every five minutes" pull-request babysit | no routine does it |
| §4 "On red CI" | superseded by `docs/routines/nightly-worker.md`: a red main is the night's only item |
| §4 monthly seeded-defect canary and monthly scorecard | superseded by `docs/routines/monthly-ablation.md` |
| §4 "Routines do not run the pipeline, do not build parsers, and do not judge" | obsolete: the nightly worker builds items and runs filings |
| §5 the canary in "Kept" | superseded by the monthly ablation |
| §5 "Every other pull request merges on green CI … readable result was produced" | duplicate of §1 principle 13 |
| §7 step 4's expected-value sentence; "Never wait for owner confirmation" | duplicates of `CLAUDE.md` and §1 principle 3 |
| §8 "Rewrite or refactor the archived repo" | duplicate of §1 principle 10, which now names `src/archive_check.py` |
| §8 "Hand summaries to the predictor" | duplicate of §1 principle 4 |
| §8 "Let anything cross a layer" | duplicate of §1 principle 6 (`src/agent_inputs.py`) |
| §8 "Write a prompt at run time" | duplicate of §6, which is not touched |
| §8 "Change or delete existing content under `runs/`, `rules/` or `events/`" | duplicate of §1 principle 7 |
| §8 "Combine indicators into a composite rank" | duplicate of §2 and `CLAUDE.md` |
| §8 "Stop and wait for the owner" | duplicate of §1 principle 3 |
| §8 "Spend more than one day on infrastructure changes" | duplicate of §1 principle 10 |

§1 principle 12 had "a weekly routine folds rules into `CLAUDE.md`"; it now says
where an enforced lesson goes and what prints the rest. §6 is unchanged.

## lessons.md

124 of the 314 lessons moved to `archive/lessons_enforced.md`, each verbatim,
with its old line number and one line naming what enforces it or why it is
obsolete. The second lens then found seven of them that do not belong there:
four (old lines 95, 98, 99 and 100) whose named test records the defect rather
than enforcing the lesson, and three (old lines 19, 20 and 33) marked obsolete
because the artefact each was learned on was retired, which retires the
artefact and not the lesson. On 2026-10-07 those seven went back into
`lessons.md` in their original order; the archive is a record, so its seven
rows stay as they were, and the move is recorded by appending one dated line
per lesson under a `## Moved back` heading at the end of the file, never by
editing a row: `src/archive_check.py` admits an append to an archived file and
refuses an edit, so a note written under the row would have failed `make check`
the day after this merged. 117 are archived: 109 enforced, 8 obsolete. The 197
in `lessons.md` are the ones no script or test holds, in their original order;
four were written this session, after them. Every count here is a `grep -c` on
the file as committed: `^[0-9]\{4\}-[0-9][0-9]-[0-9][0-9] ` for dated lines
(314 on `origin/main:lessons.md`; 201 in `lessons.md`; 131 in the archive, of
which the 7 under `## Moved back`, `^2026-10-07 (was line`, are the move-back
records and the other 124 are the archived lessons), `^  (was line [0-9]*)
enforced by` (113) and `^  (was line [0-9]*) obsolete` (11) in the archive, so
113 + 11 − 7 + 197 = 314: nothing was lost.

The date is now a rule the gate holds. `src/instruction_length_check.py` reads
both files and refuses a line after the header that is neither dated, blank,
indented nor a Markdown heading. The archive's note under each lesson is
indented, which is why "indented" is the shape of a line that belongs to the
lesson above it, and `## Moved back` is the heading that opens the archive's
appended record; a strict reading, every non-blank line after the header
dated, would refuse 125 committed archive lines (the note under each of the 124
lessons and that heading), the first being line 14:

    (was line 7) enforced by: `src/interpreter_pin.py`: every entry point refuses an interpreter other than 3.12 (`tests/test_interpreter_pin.py`).

That file is not changed; the rule is written to the shape its header describes.

The SessionStart hook in `.claude/settings.json` now runs
`sh tools/session_start_lessons.sh` in place of `cat lessons.md`.
