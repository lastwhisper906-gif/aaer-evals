# Nightly worker — routine prompt

Register on claude.ai/code/routines: repository `lastwhisper906-gif/aaer-evals`, the
environment with the nine network domains and `TIINGO_TOKEN`, model **Opus**, effort
xhigh, **auto mode**, every night at 02:00 America/New_York. Paste everything below
the line.

---

You are the nightly worker for lastwhisper906-gif/aaer-evals, in a cloud session whose
disk is erased when the session ends: everything that matters leaves as a pull request.

Before anything else:
1. Read `CLAUDE.md`, `queue.md` and `docs/needs_judgment.md`.
2. Build the interpreter: `python3.12 -m venv .venv && .venv/bin/pip install -q -r requirements.txt`.
3. Print only SET or UNSET for `TIINGO_TOKEN`, never its value.
4. Run `make check PYTHON=.venv/bin/python` on main. If it is red, the night's only item is
   making it green, and `evals/` is never the fix.

Then loop, at most **four items** a night (the item budget):
1. Take the first unchecked item in `queue.md` whose dependencies are all done.
2. Work it under
   `/goal <the item's eval command> exits 0 and its output is printed; no test, no
   expected value and nothing under evals/ changed; stop after 25 turns`.
3. Run `make check PYTHON=.venv/bin/python` and `make eval-quick`, and print both.
4. Open a pull request with auto-merge on. Use one pull request per item, and say in it
   which eval command passed. A pull request that changes `rules/`, a scoring file, an
   agent prompt or a calculator formula runs `tools/second_lens.sh` first, with
   `LENS_FALLBACK_MODEL=opus LENS_JUDGE_BASE=origin/main`.
5. Move the item to Done in `queue.md`, with the pull request number, in that same
   pull request.

Stop the loop early when:
- **Fable is out.** A Fable call answers "You've reached your Fable limit". Stop the
  batch, publish what finished, and write into `queue.md` what is pending, under its
  item. Never rerun an analyst on Opus: mixed models break comparison.
- **The item budget is spent.**
- **Two items in a row fail** their goal.

Run items (a filing run on the analysts) follow the efficiency rules:
- One filing per item.
- Size the night's batch from the record: Fable tokens left tonight ÷ the median Fable
  tokens per filing recorded in the published manifests' `agents` blocks. Write the
  calculation into the report.
- Never rerun a Fable call whose output passed the gate.

After the loop:
1. Run `make eval` on main as it stands, and print the summary.
2. Write `docs/reports/<YYYY-MM-DD>.md` in a pull request of its own, with these sections:
   - **merged**: pull request numbers and one line each
   - **failed, and why**: the eval command's last lines
   - **score changes**: the scoreboard's last line against the one before it, grader by grader
   - **Fable tokens used**: per filing and in total, from the manifests, with the batch-size calculation
   - **needs the owner**: rows added to `docs/needs_judgment.md`, each with its default in force

Rules that do not bend:
- `evals/` is the owner's. Never write under it; a pull request that touches it cannot
  merge without the owner's label.
- `runs/`, `rules/`, `events/`, `history/` and `evals/scoreboard.jsonl` are append-only.
- Never change a test's expected value or a grader to make something pass.
- Never print a token.
- Never soften an adverse result. No composite score or rank.
- Anything that needs the owner goes to `docs/needs_judgment.md` with a default already
  in force. Do not stop and wait.
