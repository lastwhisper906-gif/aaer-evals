# Daily — the morning report

The owner's decision of 2026-09-24 (`docs/structure_changes.md`): results
arrive as one morning report, and a model only reads and triages them. The night
itself is `.github/workflows/nightly.yml`, Python with no model. This routine
reads what it left, opens its pull request, and writes the report.

A Claude Code cloud scheduled task, daily at 07:30 US Eastern. Its final message
is the report, and the final message is the notification: there is no
`osascript` in the cloud. It builds nothing, fixes no parser and judges nothing
(`docs/HOW_WE_WORK.md` §4, "routines do not build"). It never touches EDGAR: the
cloud environment may not reach sec.gov, and every EDGAR request happens in
Actions.

---

## 0. Set up

A cloud session has no `.venv`. Without one the Stop hook's `make check` does
not run and says nothing, which has happened in this repository once already.

```sh
python3.12 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
```

## 1. Did last night run?

List the runs of `nightly.yml` (GitHub `actions_list`, `list_workflow_runs`,
resource `nightly.yml`). Last night's run is a run started after 06:00 UTC
**today** -- the schedule fires at 07:00 UTC, and this routine runs hours after
it. A run from yesterday is not last night's, however recent it is.

- **No such run: that is the first line of the report**, before anything else,
  in these words: `LAST NIGHT DID NOT RUN.` Then the newest run there is, with
  its date. A night that did not run and went unnoticed is the worst failure
  this system can have.
- A run whose conclusion is not `success` is a failure line too, with its
  conclusion and the name of the step that failed.

## 2. Read what the night left

The night pushes one branch, `nightly/<date>-<run id>`, and opens no pull
request: a pull request opened with the Actions token starts no CI, so its
auto-merge would never fire. Fetch the branch whose name ends in last
night's run id and read the last line of `history/nightly.jsonl` on it. That
line is the night's summary -- `lookups`, `new`, `not_extracted`,
`extractions`, `failures`, and, once historical collection runs, `history` --
**only if its `run` is last night's run URL.** The push step runs whatever
happened before it, so a night whose Python never ran pushes a branch whose
last line is an earlier night's; reporting that line would report yesterday as
today. A line whose `run` is another run's is the failure line `the night left
no summary line`, and nothing on that branch is reported as last night's.

If the run happened and the branch is missing, that is a failure line too.

## 3. Open its pull request

Open a pull request from the night's branch into `main` with the GitHub tools,
title `the nightly crew's night of <date>`, and turn auto-merge on (squash). A
pull request opened through this connection starts CI, and auto-merge lands it
once CI is green. If an older `nightly/*` pull request is still open, the new
branch already carries its lines (the workflow builds on an unmerged night), so
close the older one with a one-line comment naming the one that replaces it --
**only when the older branch's head is an ancestor of the new branch's**
(`git merge-base --is-ancestor`). When the older night did not merge cleanly
onto `main`, the workflow started from `main` instead and says so in its last
step (`... did not merge cleanly onto main`); the new branch then does not carry
the older lines, the older pull request stays open, and that is a failure line
in the report.

## 4. The report

Readable on a phone in one minute. Plain text, short lines, in this order:

1. **Failures and anomalies.** `LAST NIGHT DID NOT RUN` if it did not. Then
   every entry of the summary's `failures`, one line each, then the run's own
   failure if its conclusion was not `success`, then a red CI on any open
   `nightly/*` pull request. If there are none, say `no failures`.
2. **New filings and what extract did with each**: `lookups 12 of 12`, then one
   line per new filing -- ticker, form, accession, and passed or the stage it
   failed at. `no new filings` if there were none.
3. **Historical collection**: `collected N of M in scope, P passed the four
   checks`, tonight's count, and tonight's failures counted by the stage they
   failed at (the lines are in `history/<ticker>/manifest.jsonl`).
4. **The owner's queue**: the number of `[ ]` rows in `docs/needs_judgment.md`,
   and the open pull requests by number and title (GitHub
   `list_pull_requests`). `tools/daily_summary.sh` prints the rest of what the
   daily summary carries; run it with `sh`, and take the pull requests from the
   GitHub tools rather than from its `gh` line, which prints `(none open)` when
   `gh` is missing.

The report says nothing about signal. The twelve test the pipeline, not the
signal, and no observation about any of them is recorded.

## 5. A new kind of failure

A failure whose kind has not appeared in `history/nightly.jsonl` before gets a
row in `docs/next_cycle_tasks.md` under **Next cycle**, in the file's own
four-field shape, with a judge and an expected value from the source -- the
filing, the index row, the summary line that recorded it. If no judge can be
written, the row goes in `docs/needs_judgment.md` instead. Either way it goes
through its own pull request with auto-merge on. This routine does not fix the
failure.
