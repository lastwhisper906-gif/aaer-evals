# Python 3.12 is the pinned interpreter; the entry points refuse anything else.
PYTHON ?= python3.12
BASELINE ?= origin/main

.PHONY: check append-check test

# The whole gate. Run this before opening a pull request.
check: append-check test

# The prediction record is append-only. A violation here is not a finding to
# triage later -- it stops the cycle.
append-check:
	$(PYTHON) -m src.append_check --baseline $(BASELINE)

test:
	$(PYTHON) -m pytest tests -q
