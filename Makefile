# Python 3.12 is the pinned interpreter; the entry points refuse anything else.
PYTHON ?= python3.12
BASELINE ?= origin/main

.PHONY: check append-check plain-name-check test

# The whole gate. Run this before opening a pull request. CI runs this same
# target, so the gate is defined once -- the same rule written in two files is
# two rules until something reads both.
check: append-check plain-name-check test

# The prediction record is append-only. A violation here is not a finding to
# triage later -- it stops the cycle.
append-check:
	$(PYTHON) -m src.append_check --baseline $(BASELINE)

# Plain names, no letter-number codes. The post-write hook names one on the spot
# for whoever is at the keyboard; this is what makes a pull request red.
plain-name-check:
	$(PYTHON) -m src.plain_name_check --changed --baseline $(BASELINE)

test:
	$(PYTHON) -m pytest tests -q
