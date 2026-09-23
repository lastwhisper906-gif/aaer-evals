# The project's own interpreter, which is Python 3.12 and has this project's
# site-packages; the entry points refuse any other version. The default is a
# path and not a bare name on purpose: bare `python3.12` on a developer machine
# resolves to an interpreter with no pytest, and every judge command in
# `docs/next_cycle_tasks.md` named that one until six reproduce runs in a row
# exited before collecting a test. Continuous integration overrides this with
# `PYTHON=python`, which is the interpreter it installed the requirements into.
PYTHON ?= .venv/bin/python
BASELINE ?= origin/main

.PHONY: check append-check plain-name-check secret-check test

# The whole gate. Run this before opening a pull request. CI runs this same
# target, so the gate is defined once -- the same rule written in two files is
# two rules until something reads both.
check: append-check plain-name-check secret-check test

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

test:
	$(PYTHON) -m pytest tests -q
