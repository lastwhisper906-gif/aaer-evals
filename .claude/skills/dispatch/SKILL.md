---
name: dispatch
description: Turn one task-list item into a five-field brief before any agent is launched. Refuses to launch when a field is empty. Use before every agent launch that builds or checks something.
---

# Dispatch one item

The item is `$ARGUMENTS`.

An agent launched without a complete brief produces work nobody can judge. This
is the one rule carried over from the old harness's dispatch layer, and it is
carried over because it is the one that kept paying.

Fill all five fields. **If any field is empty, do not launch.** Mark the item
`needs judgment` in `docs/next_cycle_tasks.md` with one line naming the empty
field, and stop.

| Field | Must say |
|---|---|
| **goal** | one sentence, in plain names, of what will be true when this is done |
| **output shape** | the exact files written, and the schema or format of each |
| **allowed tools** | the tools the agent may use, and the paths it may write |
| **boundaries** | what it must not touch: `runs/`, `rules/`, `events/`, another layer's input directory, any test expectation |
| **judge** | the command that decides pass or fail, **and where its expected value comes from** |

## The judge field is two things, not one

A command alone is not a judge. `pytest tests/test_trends.py` is a command; it
becomes a judge only when the numbers it asserts came from somewhere other than
the code it is testing.

So the field reads, for example:

> `python3.12 -m pytest tests/test_trends.py -q` — expected ratios computed by
> hand from `tests/fixtures/AAPL/companyfacts.json`, written out in the test.

and never:

> `python3.12 -m pytest tests/test_trends.py -q` — expected ratios in
> `tests/fixtures/AAPL/expected.json`.

unless that file's provenance is stated and is not "the parser wrote it".

## Then

Hand the five fields to the agent verbatim as its brief. Do not summarize them,
do not add context it did not ask for, and do not tell it what you expect it to
find.
