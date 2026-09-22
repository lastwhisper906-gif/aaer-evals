# The planted defect

This directory holds one change that is wrong on purpose, and the note saying
what is wrong with it. `tools/monthly_canary.sh` copies these files onto a
branch in a throwaway worktree, commits them, and asks the `refute-check` lens
what it finds. The lens naming the planted file under the planted rule is a
**hit**; anything else is a **miss**, and the miss is what the routine exists to
catch. A verification layer that has never been shown to catch a defect is not
known to work.

**What is planted.** `tests/fixtures/receivable_days.json` was produced by
running `src/receivable_days.py`, which is the code it is meant to judge, and
the planted test says so in its own docstring. The reader divides by a 360-day
year; the expected file carries the numbers that year produces, so if the reader
were wrong in the obvious way the expected file would have moved with it. That
is rule 1 of `tools/lens_prompt.md`, the rule the lens is told is the most
important thing it checks.

**Why the seed files end in `.planted`.** They are data here and code only in
the throwaway worktree. The suffix keeps them out of `pytest`, out of the plain-
name check's Python reading and out of anything that imports `src/`, and it is
stripped when they land — so the tree the lens reads carries no marker saying it
is a test. A planted defect that announces itself measures nothing.

`plant.json` names where each seed lands, which rule it violates, and the item
title the change is presented under. `tests/test_monthly_canary.py` checks the
arithmetic by hand, so the claim that this is a genuine rule-1 defect does not
rest on running the planted reader either.

**`keep_out` is the other half of the manifest.** This directory ships on
`main`, and the plant grows on a worktree off `main` — so unless something takes
it back out, the tree the lens reads holds this README, `plant.json` and files
byte-identical to what was planted, and a lens that never applies rule 1 still
scores a hit by reading them. `keep_out` lists what the routine takes back
out of that worktree before it plants anything — with
`git update-index --skip-worktree` and a delete, so that `git status` stays
clean. It is not only this directory: the routine's own script and decision,
its document, its test, the task list the prompt sends a lens to, the ledger it
writes, `lessons.md` (which `.claude/settings.json` reads aloud to every session
that starts here) and the two records that describe the mechanism are all on it.
Replace the plant and the list moves with it;
`docs/routines/monthly-canary.md` §6 is the whole argument.

Replace the plant when it stops being interesting — a lens that has seen the
same defect twelve months running is being tested on its memory. Change
`plant.json` with it; nothing in `src/canary.py` knows what is in here.
