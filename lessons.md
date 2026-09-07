# Lessons

One line per mistake, newest last. No judgment, no narrative. The weekly routine
folds rules into `CLAUDE.md` and procedures into skills, merges duplicates, and
strengthens anything that has shown up three or more times.

2026-09-06 read a single test failure on the local Python 3.14 venv as a real regression; the canonical interpreter is 3.12 and it passes there — run the canonical interpreter before drawing a conclusion.
2026-09-06 built a command line in a shell variable and ran it unquoted; zsh does not word-split, so a two-word command was passed as one filename and reported a false failure — run commands literally, not out of variables.
2026-09-06 chained mkdir with a heredoc in one command inside an isolated worktree and had it refused as unverifiable; split file creation into plain single-purpose commands.
2026-09-06 wrote the append check to forbid any change to a published file, which would have blocked every append to events/ledger.jsonl — a .jsonl ledger grows by design; a test written at the same time caught it.
2026-09-06 wrote two letter-number codes into the structure-change record while describing an archived branch; naming an old artifact is not a licence to carry its codes forward — a scan of the new files caught it.
2026-09-06 made the one-time archive relocation exemption require an identical blob, which failed on runs/MANIFEST.sha256 because the baseline branch was 171 commits behind the archived tip; ran the check against the real baseline before trusting it.
2026-09-06 verify-public failed on Python 3.14 (thread pool); would have been reported as a real failure if not rerun on 3.12 — pin the interpreter in scheduled tasks too.
2026-09-06 wrote the append-only rule into CLAUDE.md as "never edit or delete", which the check itself already contradicted by allowing ledger appends; a rule the code disagrees with is a spec error, not a code error.
2026-09-06 put a README inside runs/, which made the directory's own explanation uncorrectable — the append check refused my first edit to it in CI; documentation does not belong in an append-only directory, and the check now says so in one narrow line.
2026-09-07 do not put documentation inside protected directories; the exception was the wrong fix.
2026-09-06 finished a step by opening a pull request and calling it done; a pull request waiting for the owner's click is the signature bottleneck the rules forbid — make the merge automatic before calling a step finished.
