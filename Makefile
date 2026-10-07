# The project's own interpreter, which is Python 3.12 and has this project's
# site-packages; the entry points refuse any other version. The default is a
# path and not a bare name on purpose: bare `python3.12` on a developer machine
# resolves to an interpreter with no pytest, and every judge command in
# `docs/next_cycle_tasks.md` named that one until six reproduce runs in a row
# exited before collecting a test. Continuous integration overrides this with
# `PYTHON=python`, which is the interpreter it installed the requirements into.
PYTHON ?= .venv/bin/python
BASELINE ?= origin/main

.PHONY: check append-check archive-check plain-name-check secret-check rule-checks test eval eval-quick

# The whole gate. Run this before opening a pull request. CI runs this same
# target, so the gate is defined once -- the same rule written in two files is
# two rules until something reads both.
# `test` runs before `rule-checks` so CI shows the suite's result before a rule
# check that is red by merge order (a judge CLAUDE.md names that lands on a
# branch ahead of this one); make stops at the first failing target.
check: append-check archive-check plain-name-check secret-check test rule-checks

# The prediction record is append-only. A violation here is not a finding to
# triage later -- it stops the cycle.
append-check:
	$(PYTHON) -m src.append_check --baseline $(BASELINE)

# Plain names, no letter-number codes. The post-write hook names one on the spot
# for whoever is at the keyboard; this is what makes a pull request red.
plain-name-check:
	$(PYTHON) -m src.plain_name_check --changed --baseline $(BASELINE)

# No credential belongs in this tree. The price backends read theirs from the
# environment, and this is what says so out loud rather than in a sentence.
secret-check:
	$(PYTHON) -m src.secret_scan --changed --baseline $(BASELINE)

# The archived project is added to, never rewritten.
archive-check:
	$(PYTHON) -m src.archive_check --baseline $(BASELINE)

# Rules CLAUDE.md states in prose, each held by a script that reads the files:
# every open item names a judge, every inbox row names its default (and a list
# that yields no row is refused, not passed), CLAUDE.md stays within its 22
# lines and every path its parentheses name is in the tree, and every lesson in
# lessons.md and its archive starts with its date, so the session-start hook can
# tell it from the header.
rule-checks:
	$(PYTHON) -m src.task_judge_check
	$(PYTHON) -m src.owner_inbox_check
	$(PYTHON) -m src.instruction_length_check --paths

test:
	$(PYTHON) -m pytest tests -q

# The owner's graders over the run directories (evals/README.md). `eval` grades every
# run, regression and capability, and appends one line to evals/scoreboard.jsonl; it
# exits non-zero on any regression failure or a capability score below a floor in
# evals/thresholds.json. `eval-quick` is regression on the runs this branch changed,
# for the Stop hook. CI runs `eval` with main's copy of evals/.
eval:
	$(PYTHON) -m evals

eval-quick:
	$(PYTHON) -m evals --quick
