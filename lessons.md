# Lessons

One line per mistake, newest last. No judgment, no narrative. The weekly routine
folds rules into `CLAUDE.md` and procedures into skills, merges duplicates, and
strengthens anything that has shown up three or more times.

2026-09-06 read a single test failure on the local Python 3.14 venv as a real regression; the canonical interpreter is 3.12 and it passes there — run the canonical interpreter before drawing a conclusion.
2026-09-06 built a command line in a shell variable and ran it unquoted; zsh does not word-split, so a two-word command was passed as one filename and reported a false failure — run commands literally, not out of variables.
2026-09-06 chained mkdir with a heredoc in one command inside an isolated worktree and had it refused as unverifiable; split file creation into plain single-purpose commands.
2026-09-06 wrote the append check to forbid any change to a published file, which would have blocked every append to events/ledger.jsonl — a .jsonl ledger grows by design; a test written at the same time caught it.
2026-09-06 made the one-time archive relocation exemption require an identical blob, which failed on runs/MANIFEST.sha256 because the baseline branch was 171 commits behind the archived tip; ran the check against the real baseline before trusting it.
