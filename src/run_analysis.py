"""One run, from an extracted bundle to the memo: read, gate, calculate, analyse, value.

The owner's decision of 2026-09-28 (`docs/structure_changes.md`) turned the
decide stage into three analysts. This is the stage runner that
`src/agent_inputs.py` leaves to "the stage runner", and it runs each agent the
way the second lens already runs its fallback: `claude -p --restricted` started
in the agent's own directory, with the committed definition passed inline and
nothing else, so the session reads that directory and writes its one file there.
`--restricted` confines the file tools to the working directory; a read one step
outside it is refused, which was checked before this file was written.

    extract (done)  ->  numbers reader, notes-text reader   (parallel)
                    ->  quote gate on both reports
                    ->  market_labels.json, by Python, when the run holds a market table
                    ->  calculator.json, and calculator_filings_only.json without any price
                    ->  accounting analyst, financial analyst   (parallel, never merged;
                        they see the filings-only view)
                    ->  the analysis gate on both
                    ->  calculator.json with the accounting adjustments applied
                    ->  valuation analyst, first pass: assumptions.json
                    ->  calculator.json with the DCF run on those drivers
                    ->  valuation analyst, second pass: analysis_valuation.json
                    ->  memo_ko.md, baselines.json, the single-agent control
                    ->  input_manifest.json: every agent's model, tokens and cost

**No prompt is written at run time.** Each agent's instructions are its committed
file under `.claude/agents/`; the message it is sent is `INSTRUCTION` below with
its directory's file names and its one output interpolated, and nothing else.
The control's prompt is `CONTROL_PROMPT` here, because a control is not a layer
and must not become something a session can invoke by name.

**One model for every agent, when the owner names one.** `--model` puts the named
model in place of the one each committed definition carries, for every agent and
the control alike; the definitions themselves are not touched, each agent's
record says the model it asked for, and the manifest's `model_override` says why,
its `applies_to` naming the agents the invocation that wrote it called.
The owner's decision of 2026-09-30 runs the analysts on Opus while the Fable
limit holds (`docs/structure_changes.md`).

**Fable, used efficiently** (the owner's decision of 2026-10-06, `docs/HOW_WE_WORK.md`
§6). A Fable call whose output passed is never run again. A failed Fable call --
no file, a file that is not JSON, or a non-zero exit -- is run again with identical
input at most twice; an Opus call once. A limit is read off the message ("reached
your ... limit") and, for a Fable call, off the shape lessons.md records for
2026-09-29: a failed call that spent no token and ended in under ten seconds is
the limit, whatever it said. A Fable call that answers the limit is never run
again on Fable; what happens next is `--on-fable-limit`, and the owner's decision
of 2026-10-07 (`docs/structure_changes.md`: "fable 사용량이 max 가 되면 오퍼스로
전환시키도록해" -- when Fable usage reaches its limit, switch to Opus) makes
`opus` the default:

* `opus` -- the run goes on. The limit is noted once for the run, with the time
  and the agent, in the manifest under `model_fallback` ({"from": "fable",
  "to": "opus", "at": ..., "first_agent": ...}), written the moment the limit is
  answered so a crash afterwards leaves it on record. That row is the run's
  record that the Fable limit was reached; the key `fable_limit_reached` is not
  written for it, because that key marks a run the limit stopped, which
  `src/fable_batch.py` does not count, the nightly crew does not commit and a
  resume continues. The agent that hit the limit is called again at once on
  `FALLBACK_MODEL`, Opus, its `attempts` listing the limit attempt and then the
  Opus attempt, and every later agent of the run whose definition asks for Fable
  is called on Opus. Each such agent's record says so by name --
  `model_requested: fable` (what the definition or `--model` asked for),
  `model_served` the Opus model the CLI reports, `fallback_from: fable`, and
  `fallback_reason`, which says what set that agent's fallback off -- its own
  call's reading for the agent that hit the limit, the row's `reason` at the
  time for a later one: `fable_limit_reached` when the limit's message said so, and
  `fable_failed_like_the_limit` when the shape alone did -- a Fable call that
  failed in under ten seconds having spent no token, with no limit message,
  still falls back by the owner's reading of that shape, but a mis-installed CLI
  or a bad flag fails the same way, so the label does not claim the limit. Each
  attempt row says what it asked for, and `src/fable_batch.py` leaves a filing
  that fell back out of its median. The rest of the batch carries a fallback the
  limit's message confirmed, and the runner finds it itself (`batch_fallback`):
  a run under `opus` reads every other run's manifest under its root, and the
  most recent limit `carried_fallback` would carry puts it on Opus from its first
  call; `--carry-fallback-from <run>` names one for a run elsewhere, and the run
  that fell back says both on stderr. A run carrying it calls every Fable agent
  on Opus from its first call, never asking Fable again, labelled
  `fable_limit_reached`, its row noted at its first
  Fable agent with `carried_from` naming the run whose manifest records the
  limit and `carried_limit_at` when it was noted -- refused, before anything
  runs, when that manifest records no `model_fallback`, one the shape alone set
  off, or a limit noted more than `CARRY_HOURS` (12) before this run, which is
  another night's and not this batch's, and under `stop`, which does not fall
  back. A shape-only fallback stays inside its own run, and its stderr
  line says why; a row the shape opened is confirmed, `confirmed_by` naming the
  agent, when an analyst already on Fable in parallel answers the limit's
  message. The comparison
  stays honest by the label, not by stopping: nothing is averaged across the two
  models here, and how the graders treat a fallback run beside a Fable run is an
  open row of `docs/needs_judgment.md`. The exit code is the run's own, 0 when
  it finished. A limit the fallback model answers too has nowhere to go: the
  run stops there as it does under `stop`, the agent named under
  `fable_limit_reached`, but the command exits `FAILED`, 1, because exit 4 is
  `stop`'s alone; its stderr line says to stop the batch and carries nothing.
* `stop` -- the rule of 2026-10-06, kept as an option. The run stops where it
  stands, publishes what finished -- the other analyst's output gated into its
  analysis file, `memo_ko.md` and `baselines.json` written from what exists, the
  memo saying which frame is missing and why -- names the agent in the manifest
  under `fable_limit_reached`, and exits `LIMIT_REACHED`, 4, so the batch stops
  too and writes what is pending into `queue.md`. Not 3: that is
  `interpreter_pin.WRONG_INTERPRETER`, which `main` returns before the run
  starts, and the batch has to tell the two apart.

A stopped run is continued in place the next night -- by default when the
manifest records `fable_limit_reached` or `stopped_on`, or with `--resume` --
and every agent whose gated output is already on record is skipped, never called
again; only the stopped agent and those after it run, the calculator stages
re-use a file that is already there with the same content, and the manifest
records `resumed_at` and `resume_skipped`. A run that did not stop is not
resumed: `--resume` on a finished run says "nothing to resume" and exits 0, and
on a run that failed some other way is refused, a correction being a new run. A
resumed run runs under the model the stopped run did: a resume whose `--model`
is not the stopped run's `model_override`, or names one when the stopped run had
none, or names none when it had one, is refused with exit 2, because a run on
two models mixes what the record cannot compare
(`docs/routines/nightly-worker.md`). The one model a resume may name beyond
that is the recorded fallback: a run whose manifest carries `model_fallback` ran
under Opus from the agent it names, so a resume of it with `--model opus` is
accepted, and a resume without `--model` carries the fallback forward, calling
every pending Fable agent on Opus and labelling it with the row's reason. A
resume naming `--model opus` does the same: the row already puts those agents on
Opus, so the flag is read as the fallback carried forward and the run continues
under the stopped run's own choice of model, each pending Fable agent labelled,
with no `model_override` written for it. Under either, each pending agent's definition is still held to its layer, so a
definition edited between the nights is refused; and a resume of it under
`--on-fable-limit stop` is refused, since it would call the pending Fable agents
on Fable after Opus, mixing models the other way. A mix the record does not
explain -- an agent on record that asked for Fable and was served another model
with no `fallback_from`, or one carrying `fallback_from` under a manifest with
no `model_fallback` -- is still refused. The manifest's
`model_override.applies_to` names only the agents the invocation that wrote it
called, each agent on record saying for itself what it asked for, and a stale
override is never carried forward. The single-agent control runs on the golden
filings only, where it is scored against the owner (`--control auto`), and the
manifest's `control_reason` says why it ran or did not, including that this tree
holds no `evals/golden/cases`; the message every agent is sent lists the shared
files first, in a fixed order, so the prompt cache serves them. The run goes on
past a failed analyst, so what did write still reaches the memo, but the
manifest's `analysis_failure` names every agent that did not write and the
command exits non-zero: a run missing an analysis is never reported as finished.

**Every agent's usage is recorded** in `input_manifest.json` under `agents`: the
model asked for, the model that served, input, cache and output tokens, turns,
cost and wall time, so the monthly cost of the pipeline is read off the record
rather than estimated. The record is written the moment each call returns
(`record_agent`), not at the end, so a crash between an analyst's output and
`finish` -- the analysis gate refusing a JSON list, the calculator refusing an
input -- leaves every call that returned on record; `run_company` writes the
error under `stopped_on`, and the next invocation resumes such a run as it
resumes one the limit stopped, calling no agent whose gated output is on record.
`finish` alone writes `analysed_utc`, the mark of a run that finished: a run
carrying it is never resumed. Each agent's record lists every attempt under
`attempts` (attempt, model served, tokens, cost, duration, outcome), and its
token and cost fields are the sums over them, so a retried call costs what the
record says. Under no override on record -- no `--model`, or a fallback run's
`--model opus` -- a resume also reads each pending agent's
definition: a definition whose `model:` line was edited between the nights,
so that it now asks for a model other than the one the agents on record in its
layer ran under, is refused -- the record could not compare them.

    python3.12 -m src.run_analysis --run runs/NVDA/0001045810-26-000075 \\
        --ticker NVDA --form 10-Q --cutoff 2026-08-26 --period-end 2026-07-26 \\
        [--store tests/fixtures] [--prices <directory>] [--model opus] [--control auto] \\
        [--on-fable-limit opus] [--carry-fallback-from runs/<ticker>/<accession>]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import importlib.util
import json
import os
import math
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

try:
    from src import (agent_inputs, analysis_check, baselines, calculator, cutoff_guard, decide,
                     interpreter_pin, market_labels, memo, quote_gate, trends)
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (agent_inputs, analysis_check, baselines, calculator, cutoff_guard, decide,
                     interpreter_pin, market_labels, memo, quote_gate, trends)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFINITIONS = REPO_ROOT / ".claude" / "agents"
BAD_INPUT = 2
FAILED = 1
# The limit's own code: not interpreter_pin.WRONG_INTERPRETER (3), which main()
# returns before the run starts, so the batch can tell the two apart. Returned
# only under `--on-fable-limit stop`; under `opus` a run that finished exits 0,
# and one the fallback model's own limit stopped exits FAILED.
LIMIT_REACHED = 4
# What a Fable call that answers the limit does to the rest of the run
# (`--on-fable-limit`): `opus`, the owner's decision of 2026-10-07, calls the
# agent again on FALLBACK_MODEL and every later Fable agent too, each labelled;
# `stop`, the rule of 2026-10-06, stops the run and exits LIMIT_REACHED.
FALLBACK_MODEL = "opus"          # the name the definitions and --model use for Opus
ON_FABLE_LIMIT = ("stop", "opus")
DEFAULT_ON_FABLE_LIMIT = "opus"
# Why a run fell back, on its row and on each fallback agent's record: the limit's
# own message ("reached your ... limit") confirms it. A Fable call that failed in
# under LIMIT_SECONDS having spent no token, with no limit message, is the shape
# the limit took on 2026-09-29 (lessons.md), and the owner's reading of that shape
# stands: it falls back too, but under its own label, because a mis-installed CLI
# or a bad flag fails the same way, and it never carries into another run.
FALLBACK_REASON = "fable_limit_reached"
SHAPE_FALLBACK_REASON = "fable_failed_like_the_limit"
# A batch is one night (docs/routines/nightly-worker.md: four items at most): a
# fallback is carried into a run only from a limit noted within this many hours
# before it, so a run of another night, after the limit has reset, is never put
# on Opus by an old row.
CARRY_HOURS = 12

# The pins: the family the definition names, and the effort it runs at.
# `docs/HOW_WE_WORK.md` §6 -- readers on Opus at xhigh; the analysts inherit the
# supervisors' pin, Fable, and the single-agent control runs on the same model
# as the analysts, because a control on another model measures the model.
EFFORT = "xhigh"
CALL_TIMEOUT_SECONDS = 3600
RETRIES = 1                 # an Opus call: one more try
FABLE_RETRIES = 2           # a Fable call: at most two more
LIMIT = re.compile(r"reached your \w+ limit", re.IGNORECASE)
# The other shape the limit takes (lessons.md, 2026-09-29): a Fable call that
# fails having spent no token, in about two seconds. Under this many seconds,
# with no token in or out, a failed Fable call is read as the limit first.
LIMIT_SECONDS = 10
# The one key only `finish` writes: a manifest carrying it is a finished run's.
FINISH_MARKER = "analysed_utc"
# The token fields of a usage record, summed over an agent's attempts.
TOKEN_FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
                "output_tokens")
# Each agent's gated output at the run root, which is what says the agent is on
# record and need not be called again on a resumed run.
OUTPUT_ON_RECORD = {"numbers-reader": ("report_numbers.md",),
                    "notes-text-reader": ("report_notes_text.md",),
                    "accounting-analyst": ("analysis_accounting.json",),
                    "financial-analyst": ("analysis_financial.json",),
                    "valuation-analyst": ("assumptions.json",),
                    "valuation-analyst-second-pass": ("analysis_valuation.json",),
                    "control-single-agent": ("control_analysis_accounting.json",
                                             "control_analysis_financial.json",
                                             "control_assumptions.json")}


def is_fable(model) -> bool:
    """The one reading of "is this Fable": the definition's own word, or a full id
    the owner passed with --model. `src/fable_batch.py` reads a served model the
    same way."""
    return isinstance(model, str) and (model == "fable" or model.startswith("claude-fable"))
# The files most sessions share, named first so the prompt cache serves them.
SHARED_FIRST = ("calculator_filings_only.json", "calculator_before_drivers.json",
                "calculator.json", "report_numbers.md", "report_notes_text.md")

INSTRUCTION = ("Your directory holds: {files}. Read every one of them in full, following "
               "your instructions, and write {writes} in your directory. Nothing else, "
               "anywhere.")

CONTROL_DIRNAME = "control-single-agent-analyses"
CONTROL_WRITES = ("control_analysis_accounting.json", "control_analysis_financial.json",
                  "control_assumptions.json")
CONTROL_PROMPT = """You are the single-agent control. One agent does alone what the
pipeline splits between two readers and three analysts, so the record can say what
the layers add. Your directory holds one company's filing bundle and calculator.json,
which Python computed from the same filing before any analyst wrote: {files}.

Answer the three analyses the pipeline answers, each in its own file, and never merge
them: (1) control_analysis_accounting.json -- do reported earnings and cash reflect
economic reality? -- with the same keys as the accounting analyst's analysis: areas
(earnings_versus_cash, revenue_recognition, estimates_and_reserves, cost_deferral,
cash_flow_engineering_and_off_balance_sheet, controls_audit_and_filing_signals,
cross_document_reconciliation, industry_lens, each with finding, verdict, evidence,
fields), reconciliation, anomalies (id, name, name_ko, area, what, numbers_vs_prose,
evidence, fields), adjustments (name, direction, applies_to, calculator_field, quote,
quote_from, evidence), summary_ko, limits; (2) control_analysis_financial.json -- how
healthy is this company? -- with sections (profitability, efficiency, liquidity,
solvency, growth, free_cash_flow), dupont, anomalies, path_to_distress, summary_ko,
limits; (3) control_assumptions.json -- bear, base and bull drivers for a ten-year DCF
(revenue_growth_year_one, terminal_growth no higher than the risk-free rate in
calculator.json, operating_margin_year_one, operating_margin_year_ten,
reinvestment_rate_year_one, reinvestment_rate_year_ten, each a decimal, each with a
reason and a verbatim quote or calculator fields). An anomaly id is its area slug in
full, then what it looks at, in lowercase words joined by underscores.

Rules: you do no arithmetic and write no digit in your own words; a number is written
as a path into calculator_before_analysts.json in braces, like
{{ratios.liquidity.current_ratio}}. Every evidence entry is a paragraph id printed on an
[id] line of one of your input files; every quote is verbatim from the file named in
quote_from. Every anomaly is listed, with no count threshold. The
words fraud, manipulation, buy, sell and alpha never appear. Write the three files in
your directory and nothing else."""


class RunError(Exception):
    """A stage could not run. The run is recorded as failed, never patched."""


class NothingToResume(Exception):
    """`--resume` on a run that finished: nothing is missing, nothing runs, exit 0."""


# --- one agent call ----------------------------------------------------------------------

def definition(name: str) -> dict:
    """A committed agent file as the `--agents` JSON the CLI takes."""
    text = (DEFINITIONS / f"{name}.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not match:
        raise RunError(f"{name}.md has no front matter")
    front = dict(line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
    front = {key.strip(): value.strip() for key, value in front.items()}
    return {"description": front["description"], "prompt": match.group(2),
            "tools": [tool.strip() for tool in front.get("tools", "Read, Write").split(",")],
            "model": front.get("model", "opus")}


def served_model(result: dict) -> str | None:
    usage = result.get("modelUsage") or {}
    return max(usage, key=lambda name: usage[name].get("outputTokens", 0)) if usage else None


def usage_record(result: dict, *, requested: str, seconds: float, attempt: int) -> dict:
    usage = result.get("usage") or {}
    return {"model_requested": requested, "model_served": served_model(result),
            "effort": EFFORT,
            "input_tokens": usage.get("input_tokens"),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
            "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "turns": result.get("num_turns"), "cost_usd": result.get("total_cost_usd"),
            "session": result.get("session_id"), "seconds": round(seconds, 1),
            "attempt": attempt, "is_error": result.get("is_error"),
            "stop_reason": result.get("stop_reason")}


def _attempt_entry(usage: dict, outcome: str) -> dict:
    """One attempt's row under `attempts`: what it was served, what it cost, how
    long it took and how it ended -- written, failed, or limit."""
    return {"attempt": usage.get("attempt"), "model_requested": usage.get("model_requested"),
            "model_served": usage.get("model_served"),
            **{key: usage.get(key) for key in TOKEN_FIELDS},
            "cost_usd": usage.get("cost_usd"), "duration_s": usage.get("seconds"),
            "outcome": outcome}


def attempts_of(record: dict) -> list[dict]:
    """An agent record's attempts: its list, or, for a record written before the
    list existed, its own fields as the one attempt they describe."""
    attempts = record.get("attempts")
    if isinstance(attempts, list) and attempts:
        return [dict(row) for row in attempts]
    outcome = ("limit" if record.get("limit_reached") else
               "written" if record.get("result") == "written" else "failed")
    return [_attempt_entry(dict(record, seconds=record.get("seconds")), outcome)]


def carried_forward(earlier, record: dict) -> dict:
    """The record of a call made again on a resumed run, with every attempt the
    agent already has on record in front of this call's own, numbered through,
    and the token and cost fields summed over all of them: a call that was paid
    for is never dropped from the record because the agent was called again."""
    if not isinstance(earlier, dict) or earlier.get("result") is None:
        return record
    rows = attempts_of(earlier) + attempts_of(record)
    for number, row in enumerate(rows, start=1):
        row["attempt"] = number
    record = with_attempts(record, rows)
    record["attempt"] = len(rows)
    return record


def with_attempts(record: dict, attempts: list[dict]) -> dict:
    """The record with every attempt listed and its token and cost fields summed
    over them, under the names a reader of the record already knows."""
    record["attempts"] = attempts
    for key in (*TOKEN_FIELDS, "cost_usd"):
        values = [row.get(key) for row in attempts if isinstance(row.get(key), (int, float))]
        record[key] = sum(values) if values else record.get(key)
    return record


def ask(directory: Path, *, agent: str, writes: tuple[str, ...], message: str,
        spec: dict, log: Path) -> dict:
    """One restricted session in `directory`; the usage record, or a failure.

    Every attempt is kept under `attempts`, and the record's token and cost
    fields are the sums over them: a call that failed twice before it passed
    cost three calls, and the batch is sized from what calls cost.
    """
    record: dict = {"agent": agent, "writes": list(writes)}
    attempts: list[dict] = []
    fable = is_fable(spec.get("model"))
    retries = FABLE_RETRIES if fable else RETRIES
    for attempt in range(1, retries + 2):
        for name in writes:
            # nothing earlier under the agent's own name: a call never sees its
            # own output from before, and a session that writes nothing is not
            # read as written because a stale file stood there
            (directory / name).unlink(missing_ok=True)
        started = time.monotonic()
        command = ["claude", "-p", "--restricted", "--permission-mode", "acceptEdits",
                   "--agent", agent, "--agents", json.dumps({agent: spec}),
                   "--model", spec["model"], "--effort", EFFORT,
                   "--output-format", "json", message]
        done = subprocess.run(command, cwd=directory, capture_output=True, text=True,
                              timeout=CALL_TIMEOUT_SECONDS)
        seconds = time.monotonic() - started
        log.write_text(done.stderr[-20000:], encoding="utf-8")
        try:
            result = json.loads(done.stdout)
        except ValueError:
            result = {"is_error": True, "result": done.stdout[-2000:]}
        usage = usage_record(result, requested=spec["model"], seconds=seconds, attempt=attempt)
        record.update(usage)
        written = all((directory / name).is_file() for name in writes)
        unreadable = [name for name in writes if written and name.endswith(".json")
                      and not _is_json(directory / name)]
        if done.returncode == 0 and written and not unreadable and not result.get("is_error"):
            record["result"] = "written"
            attempts.append(_attempt_entry(usage, "written"))
            return with_attempts(record, attempts)
        record["result"] = "failed"
        record["reason"] = (f"exit {done.returncode}; wrote "
                            f"{[n for n in writes if (directory / n).is_file()]}"
                            + (f"; not JSON: {unreadable}" if unreadable else ""))
        for name in writes:        # identical input on the retry: nothing it wrote survives
            (directory / name).unlink(missing_ok=True)
        if LIMIT.search(str(result.get("result") or "")):
            record["limit_reached"] = True
            record["limit_read_from"] = "message"
            record["reason"] = str(result.get("result"))[:200]
            attempts.append(_attempt_entry(usage, "limit"))
            return with_attempts(record, attempts)   # a limit is not a failure a retry answers
        if fable and not tokens_spent(result) and seconds < LIMIT_SECONDS:
            record["limit_reached"] = True
            record["limit_read_from"] = "shape"
            record["reason"] = (f"read as the limit: the Fable call failed in {seconds:.1f}s "
                                f"with no token spent (lessons.md 2026-09-29); it said "
                                f"{str(result.get('result') or '')[:120]!r}")
            attempts.append(_attempt_entry(usage, "limit"))
            return with_attempts(record, attempts)
        attempts.append(_attempt_entry(usage, "failed"))
    return with_attempts(record, attempts)


def tokens_spent(result: dict) -> int:
    usage = result.get("usage") or {}
    return sum(usage.get(key) or 0 for key in ("input_tokens", "output_tokens"))


def _is_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def limit_hit(agents: dict) -> list[str]:
    return [name for name, record in agents.items() if record.get("limit_reached")]


def clock() -> dt.datetime:
    """The runner's one clock, in UTC: every time it writes -- a row's `at`,
    `resumed_at`, `analysed_utc` -- is read off it, and so is the time a carry's
    window is measured against, so a test moves both through this one seam and
    never edits a stored row."""
    return dt.datetime.now(dt.timezone.utc)


def utc_now() -> str:
    return clock().strftime("%Y-%m-%dT%H:%M:%SZ")


class LimitPolicy:
    """What a Fable call that answers the limit does to the rest of the run, and
    the one run-level record of it: `fallback` is None until a Fable call answers
    the limit under `opus`, then the manifest's `model_fallback` row, shared by
    every call of the run (the analysts return in parallel, so it is set under a
    lock and written once). A resumed run starts from the row its manifest
    already carries, so the fallback is carried forward, never repeated.

    `carried` is the rest of the batch (`carried_fallback`): `carried_from`, the
    run, as `<ticker>/<accession>`, whose manifest records that Fable answered the
    limit earlier in the batch (`--carry-fallback-from`), and `carried_limit_at`,
    when it did. A run carrying it has fallen back before its first call: every
    Fable request is made on the fallback model, and the row is noted at the first
    one, naming that run and that time.

    Under `stop` nothing falls back, a recorded fallback included: the row is
    kept, so `finish` still writes it, but no call is moved to the fallback model
    by it. A resume under `stop` of a run whose manifest records a fallback is
    refused before this is built (`_run_company`)."""

    def __init__(self, on_limit: str = DEFAULT_ON_FABLE_LIMIT, fallback: dict | None = None,
                 carried: dict | None = None):
        if on_limit not in ON_FABLE_LIMIT:
            raise RunError(f"--on-fable-limit {on_limit!r} is not one of {ON_FABLE_LIMIT}")
        if carried and on_limit != "opus":
            raise RunError(f"--carry-fallback-from {carried.get('carried_from')} carries a "
                           f"fallback to {FALLBACK_MODEL}, and --on-fable-limit {on_limit} "
                           "does not fall back")
        self.on_limit = on_limit
        self.fallback = dict(fallback) if isinstance(fallback, dict) else None
        self.carried = dict(carried) if carried else None
        self._lock = threading.Lock()

    def falls_back(self, requested) -> bool:
        """Whether a limit answered by a call that asked for `requested` falls back."""
        return self.on_limit == "opus" and is_fable(requested)

    def model_for(self, requested: str) -> str:
        """The model a call is made on: the fallback model, for a Fable request,
        once the run -- or the batch it carries -- has fallen back under `opus`;
        otherwise what was asked for."""
        fallen = self.on_limit == "opus" and (self.fallback or self.carried)
        return FALLBACK_MODEL if fallen and is_fable(requested) else requested

    def begin(self, run: Path, agent: str) -> dict:
        """The row a call made on the fallback model is labelled from, because the
        run already fell back; for a run carrying the batch's fallback, noted here
        at its first Fable agent, the limit confirmed by the run it carries."""
        with self._lock:
            if self.fallback is None:
                self._open(run, agent, FALLBACK_REASON)
            return self.fallback

    def note(self, run: Path, agent: str, reason: str) -> dict:
        """The limit, noted once for the run with the time, the agent and why --
        the limit's message or its shape alone -- and written into the manifest
        at once so a crash afterwards leaves it on record and the resume carries
        it. A row the shape alone opened is confirmed when another call of the run
        -- an analyst already on Fable in parallel -- answers the limit's message:
        its reason becomes the limit's, and `confirmed_by` names that agent."""
        with self._lock:
            if self.fallback is None:
                self._open(run, agent, reason)
            elif (reason == FALLBACK_REASON
                  and fallback_reason(self.fallback) != FALLBACK_REASON):
                self.fallback["reason"] = FALLBACK_REASON
                self.fallback["confirmed_by"] = agent
                record_fallback(run, self.fallback)
            return self.fallback

    def _open(self, run: Path, agent: str, reason: str) -> None:
        self.fallback = {"from": "fable", "to": FALLBACK_MODEL, "at": utc_now(),
                         "first_agent": agent, "reason": reason}
        if self.carried:
            self.fallback.update(self.carried)
        record_fallback(run, self.fallback)


def fallback_reason(row) -> str:
    """Why a run fell back, off its `model_fallback` row: the limit's own message
    (`fable_limit_reached`), or a failure shaped like it (`fable_failed_like_the_limit`).
    A row that names no reason is read as the shape: nothing on it confirms the
    limit, so it never carries into another run."""
    confirmed = isinstance(row, dict) and row.get("reason") == FALLBACK_REASON
    return FALLBACK_REASON if confirmed else SHAPE_FALLBACK_REASON


def carried_fallback(earlier: Path, now: dt.datetime | None = None) -> dict:
    """The fallback a run carries from an earlier run of the batch: that run, as
    `<ticker>/<accession>` (`carried_from`), and when the limit was noted
    (`carried_limit_at`: its row's own, or, when that run carried it too, the time
    its row carried, so a chain of runs never stretches the window). Refused
    before the run starts unless the manifest records `model_fallback`, the
    limit's message confirmed it, and the limit was noted at most CARRY_HOURS
    before `now` (the runner's `clock()` unless a caller names one) and not after it: a run is never put on the fallback model
    without a limit on record, a fallback a failure's shape alone set off stays
    inside its own run, and a run of another night is not this batch."""
    earlier = Path(earlier)
    try:
        manifest = json.loads((earlier / "input_manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RunError(f"--carry-fallback-from {earlier}: no manifest to read ({exc})") from exc
    row = recorded_fallback(manifest) if isinstance(manifest, dict) else None
    if not row:
        raise RunError(f"--carry-fallback-from {earlier}: its manifest records no "
                       "model_fallback, so no Fable limit is on record to carry")
    if fallback_reason(row) != FALLBACK_REASON:
        raise RunError(f"--carry-fallback-from {earlier}: its fallback was set off by a "
                       f"Fable failure shaped like the limit ({SHAPE_FALLBACK_REASON}), not "
                       "by the limit's message, so it stays inside its own run")
    limit_at = row.get("carried_limit_at") or row.get("at")
    try:
        noted = dt.datetime.strptime(str(limit_at), "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc)
    except ValueError as exc:
        raise RunError(f"--carry-fallback-from {earlier}: its model_fallback names no time "
                       f"the limit was noted at ({limit_at!r})") from exc
    now = now or clock()
    if not dt.timedelta(0) <= now - noted <= dt.timedelta(hours=CARRY_HOURS):
        raise RunError(f"--carry-fallback-from {earlier}: its limit was noted at {limit_at}, "
                       f"not within the {CARRY_HOURS} hours before this run, so it is not "
                       "this batch's")
    return {"carried_from": f"{earlier.parent.name}/{earlier.name}",
            "carried_limit_at": limit_at}


def batch_fallback(run: Path, now: dt.datetime | None = None) -> dict | None:
    """The fallback the rest of the batch carries, found by the runner itself and
    not left to whoever starts the next run: of every other run under this run's
    root (`<root>/<ticker>/<accession>`), the one whose manifest records the most
    recent limit `carried_fallback` would carry -- confirmed by the limit's
    message, noted within CARRY_HOURS before `now` -- or None. A run whose
    manifest cannot be read, or whose row would be refused, is passed over."""
    run = Path(run).resolve()
    found = None
    for path in sorted(run.parent.parent.glob("*/*/input_manifest.json")):
        if path.parent.resolve() == run:
            continue
        try:
            carried = carried_fallback(path.parent, now)
        except RunError:
            continue
        if found is None or carried["carried_limit_at"] > found["carried_limit_at"]:
            found = carried
    return found


def record_fallback(run: Path, fallback: dict) -> None:
    """`model_fallback` into the manifest, under the record lock, every other key
    left alone."""
    with _RECORD_LOCK:
        path = Path(run) / "input_manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["model_fallback"] = fallback
        write_json(path, manifest)


def as_fallback(record: dict, requested: str, reason: str) -> dict:
    """An agent's record of a call made on the fallback model: what it asked for
    is what its definition or `--model` asked for, and the fallback is named with
    its reason."""
    record["model_requested"] = requested
    record["fallback_from"] = "fable"
    record["fallback_reason"] = reason
    return record


def fallen_back(limit: dict, again: dict) -> dict:
    """The record of an agent called again on the fallback model after the limit:
    the Opus call's own, with the limit attempt listed in front of its attempts,
    numbered through, the token and cost fields summed over all of them. The
    limit attempt was a call and stays on record; the record no longer says
    `limit_reached` unless the fallback call answered a limit too."""
    rows = attempts_of(limit) + attempts_of(again)
    for number, row in enumerate(rows, start=1):
        row["attempt"] = number
    record = with_attempts(dict(again), rows)
    record["attempt"] = len(rows)
    return record


def call(run: Path, directory: Path, *, agent: str, writes: tuple[str, ...], message: str,
         spec: dict, log: Path, policy: LimitPolicy) -> dict:
    """One agent's call under the limit policy: on the model the policy gives it,
    and, when a Fable call answers the limit under `opus`, again at once on the
    fallback model, the run noted as fallen back for every later Fable agent. A
    run carrying the batch's fallback notes it here, at its first Fable agent,
    before the call is made. The agent that hit the limit is labelled by how its
    own call read it; a later agent by the run's row."""
    requested = spec["model"]
    served_on = policy.model_for(requested)
    reason = fallback_reason(policy.begin(run, agent)) if served_on != requested else None
    record = ask(directory, agent=agent, writes=writes, message=message,
                 spec=dict(spec, model=served_on), log=log)
    if served_on == requested and record.get("limit_reached") and policy.falls_back(requested):
        reason = (FALLBACK_REASON if record.get("limit_read_from") == "message"
                  else SHAPE_FALLBACK_REASON)
        policy.note(run, agent, reason)
        again = ask(directory, agent=agent, writes=writes, message=message,
                    spec=dict(spec, model=FALLBACK_MODEL), log=log)
        record, served_on = fallen_back(record, again), FALLBACK_MODEL
    return as_fallback(record, requested, reason) if served_on != requested else record


def definition_for(prompt: str, model: str | None) -> dict:
    """The committed definition, with the owner's model in place of its own if named."""
    spec = definition(prompt)
    return dict(spec, model=model) if model else spec


def message_files(names) -> list[str]:
    """The directory listing an agent is sent: the shared files first, in one fixed
    order, then the rest alphabetically, so two sessions over the same inputs are
    sent the same prefix."""
    names = set(names)
    return [n for n in SHARED_FIRST if n in names] + sorted(names - set(SHARED_FIRST))


_RECORD_LOCK = threading.Lock()


def agent_entry(record: dict, earlier=None) -> dict:
    """An agent's manifest entry: its usage record less the file list it was
    handed, merged with what the manifest on disk already holds for the agent:
    the router's `trimmed` record, and every attempt on record there that this
    record does not already list in front of its own."""
    entry = {key: value for key, value in record.items() if key != "writes"}
    if isinstance(earlier, dict) and agent_inputs.TRIMMED_KEY in earlier:
        entry[agent_inputs.TRIMMED_KEY] = earlier[agent_inputs.TRIMMED_KEY]
    if isinstance(earlier, dict) and isinstance(earlier.get("attempts"), list):
        prior, own = earlier["attempts"], attempts_of(entry)
        if own[:len(prior)] != prior and entry is not earlier:
            entry = carried_forward(earlier, entry)
    return entry


def recorded_agent(run: Path, name: str) -> dict | None:
    """What the manifest on disk holds for an agent, or None."""
    try:
        manifest = json.loads((Path(run) / "input_manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    entry = (manifest.get("agents") or {}).get(name) if isinstance(manifest, dict) else None
    return entry if isinstance(entry, dict) else None


def record_agent(run: Path, name: str, record: dict) -> None:
    """One agent's usage record into the manifest's `agents`, the moment its call
    returned: one key updated, every other left alone, under a lock because the
    readers and the analysts return in parallel. What raises later in the run
    then finds this record on disk, and a resume reads it."""
    with _RECORD_LOCK:
        path = Path(run) / "input_manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        agents = manifest.get("agents") if isinstance(manifest.get("agents"), dict) else {}
        agents[name] = agent_entry(record, agents.get(name))
        # in the pipeline's order, not the order the parallel calls returned in
        ordered = {known: agents[known] for known in OUTPUT_ON_RECORD if known in agents}
        ordered.update({other: entry for other, entry in agents.items() if other not in ordered})
        manifest["agents"] = ordered
        write_json(path, manifest)


def run_agent(run: Path, name: str, logs: Path, model: str | None = None,
              policy: LimitPolicy | None = None, *, check: bool = True) -> dict:
    agent_inputs.build(run, name)
    directory = agent_inputs.session_root(run, name)
    spec = agent_inputs.AGENTS[name]
    names = {path.name for path in directory.iterdir() if path.name != spec.writes}
    message = INSTRUCTION.format(files=", ".join(message_files(names)), writes=spec.writes)
    earlier = recorded_agent(run, name)       # a call made again on a resume
    record = call(run, directory, agent=spec.prompt, writes=(spec.writes,), message=message,
                  spec=definition_for(spec.prompt, model), log=logs / f"{name}.log",
                  policy=policy or LimitPolicy())
    record = carried_forward(earlier, record)
    record_agent(run, name, record)
    if check:
        # not from inside `parallel`: the other call's directory is still being built
        boundary_holds(run, f"after {name} returned")
    return record


def boundary_holds(run: Path, when: str) -> None:
    """The boundary check over the whole run, which only the tests and the
    router's command called before: a file an agent left in its directory, a
    copy that is not the run's, a trim the owner would refuse -- each fails the
    owner's layers_hold or inputs_on_record, so the run stops here, on record
    (`stopped_on`), rather than publishing. The control's directory, which sits
    beside `agents/` and which the router's check does not walk, is held too
    (`control_violations`)."""
    broken = agent_inputs.isolation_violations(run) + control_violations(run)
    if broken:
        raise agent_inputs.AgentInputError(
            f"the boundary is broken {when} ({len(broken)}): " + "; ".join(broken))


def parallel(run: Path, names: tuple[str, ...], logs: Path, model: str | None = None,
             policy: LimitPolicy | None = None) -> dict[str, dict]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(names)) as pool:
        futures = {name: pool.submit(run_agent, run, name, logs, model, policy, check=False)
                   for name in names}
        records = {name: future.result() for name, future in futures.items()}
    boundary_holds(run, f"after {', '.join(names)} returned")
    return records


# --- the gates -----------------------------------------------------------------------------

# One reading of a report's items, shared with the market labels.
report_items = market_labels.report_items


def gate_readers(run: Path, names: tuple[str, ...] = ("numbers-reader", "notes-text-reader")
                 ) -> dict:
    """The quote gate over the reader reports named, and the reports downstream sees.

    Each reader's own report stays in its directory as what it wrote. The copy at
    the run root -- the one the analysts are handed -- carries only the items
    that stood, with a line saying how many the gate removed and that the
    manifest lists them, so no analyst builds on an item that failed its quote.
    `names` is the readers this invocation called: both on a fresh run; when
    the limit stopped one, the other alone, so what finished is on record and
    is never called again; and on the resumed run, the one that had not run.

    The copy is cut item by item, as the gate and the owner's grader read a
    report: a fenced block holding one dropped item is removed whole; a block
    holding a list loses each dropped element and is written again with the
    rest, or removed when none is left; a list with nothing dropped stays byte
    for byte. A dropped item left in a list beside a kept one (ESE's notes
    reader wrote its twenty-seven items in one list, and three dropped ones
    stayed) is an item the analysts read and the owner fails. An item is matched
    to its drop row as the gate wrote the row: by report and by the gate's own
    `quote_gate.item_id`, which is None for an id that is missing, blank or not
    a string; the gate drops every such item, and it leaves the copy with the
    rest. A fenced block that is not JSON holds items nobody can check: it is
    removed, and the gate records one drop row for it (item id null), so it is
    counted, not skipped.
    A run-root copy gated on an earlier night is not written again, and the
    gate keeps the drop rows of a report it is not handed, so the earlier
    night's record stands as it was and this call appends its own rows. The
    gate's one-id-one-item rule holds across the nights: a report gated alone
    is held to its own ids and to the ids standing in the reports already gated
    into the run root, which the gate reads and never writes.
    """
    reports = []
    for name in names:
        directory = agent_inputs.session_root(run, name)
        writes = agent_inputs.AGENTS[name].writes
        written = directory / writes
        if not written.is_file():
            raise RunError(f"{name} wrote no {writes}")
        text = written.read_text("utf-8")
        reports.append({"report": writes, "items": report_items(text), "input": directory,
                        "malformed": sum(1 for block in FENCED.findall(text)
                                         if _parsed(block) is UNREADABLE)})
    result = quote_gate.gate(reports, run)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    # keyed by report too: a row of one report never takes an item out of another
    dropped = {(row.get("report"), row.get("item_id"))
               for row in manifest.get("dropped_items") or []}
    for name in names:
        writes = agent_inputs.AGENTS[name].writes
        text = (agent_inputs.session_root(run, name) / writes).read_text(encoding="utf-8")
        removed, unreadable = 0, 0

        def gone(item) -> bool:
            # keyed as the gate keys its rows: by report, so a row of one report
            # never takes an item out of another, and by `quote_gate.item_id`, not
            # the id as written. An id of "", of spaces, 7 or a list is no id to the
            # gate, which drops the item under a row with no item id; matched by
            # the id as written, the item stayed in the copy (and a list or an
            # object as an id could not be looked up at all), and the owner, whose
            # drop rows are the gate's, held its quote as a kept item's
            return isinstance(item, dict) and (writes, quote_gate.item_id(item)) in dropped

        def keep(match: re.Match) -> str:
            nonlocal removed, unreadable
            data = _parsed(match.group(1))
            if data is UNREADABLE:
                unreadable += 1
                return ""
            if isinstance(data, dict):
                if gone(data):
                    removed += 1
                    return ""
                return match.group(0)
            if not isinstance(data, list):
                return match.group(0)
            remaining = [item for item in data if not gone(item)]
            if len(remaining) == len(data):
                return match.group(0)
            removed += len(data) - len(remaining)
            if not remaining:
                return ""
            return ("```json\n" + json.dumps(remaining, indent=2, ensure_ascii=False)
                    + "\n```\n")

        gated = FENCED_BLOCK.sub(keep, text)
        unread = (f" and {unreadable} fenced block(s) that are not JSON" if unreadable else "")
        note = (f"<!-- the quote gate removed {removed} item(s){unread} from this copy; "
                f"input_manifest.json lists each with its reason -->\n")
        (run / writes).write_text(note + gated, encoding="utf-8")
    return result


# A report's fenced JSON blocks, read as the gate and the owner's grader read them
# (`market_labels.report_items`, `evals/regression/mechanical.py` FENCE); the
# second form takes the block's own trailing line break with it when removed.
FENCED = re.compile(r"```json\s*(.*?)```", re.S)
FENCED_BLOCK = re.compile(r"```json\s*(.*?)```\n?", re.S)


UNREADABLE = object()


def _parsed(block: str):
    """A fenced block's JSON, or UNREADABLE when it does not parse."""
    try:
        return json.loads(block)
    except ValueError:
        return UNREADABLE


def check_analysis(run: Path, name: str, kind: str) -> dict:
    directory = agent_inputs.session_root(run, name)
    written = directory / agent_inputs.AGENTS[name].writes
    payload = json.loads(written.read_text(encoding="utf-8"))
    seen = next(directory / name for name in (calculator.FILINGS_ONLY, BEFORE_DRIVERS, FINAL)
                if (directory / name).is_file())
    fields = json.loads(seen.read_text(encoding="utf-8"))
    sources = analysis_check.read_sources(directory, analysis_check.SOURCES[kind])
    # the valuation analyst's prose is trimmed to the flagged paragraphs, written
    # one after the other: a quote is held to the run's full file as well, so none
    # runs across the junction of two blocks that were not adjacent in the filing
    # (analysis_check.quote_problem)
    filing = {name: (run / name).read_text(encoding="utf-8")
              for name in agent_inputs.TRIMMED_FOR_VALUATION
              if name in sources and (run / name).is_file()}
    if kind == "assumptions":
        return analysis_check.check_assumptions(payload, fields=fields, sources=sources,
                                                filing=filing)
    return analysis_check.check(kind, payload, fields=fields, sources=sources,
                                excluded=excluded_by_report(run), filing=filing)


def excluded_by_report(run: Path) -> dict[str, set[str]]:
    """The ids the gate dropped, keyed by the report they fell from, as its drop
    rows key them. The analysis gate takes each id out of that report's items
    alone for a reconciliation row, which names the report; a bare citation of
    an id dropped from either report is refused, because the dropped item may
    still be printed beside a kept one and by id alone the citation would name
    both -- the gate's own reason for dropping a twin, and what a fresh run,
    which drops both twins, would have answered."""
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    out: dict[str, set[str]] = {}
    for row in manifest.get("dropped_items") or []:
        if isinstance(row, dict) and isinstance(row.get("item_id"), str):
            out.setdefault(Path(str(row.get("report"))).name, set()).add(row["item_id"])
    return out


def write_json(path: Path, payload: dict) -> None:
    """Written whole or not at all: to a file beside it, then moved over it, so a
    reader never sees a half-written manifest while a parallel call's record is
    being written (`record_agent`)."""
    path = Path(path)
    tmp = path.with_name(f".{path.name}.writing")
    tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# --- the run --------------------------------------------------------------------------------

# The calculator at each stage, each written once, so what an agent was handed is
# still at the run root under the same name when the run is published:
BEFORE_ANALYSTS = "calculator_before_analysts.json"     # the control, and the base
BEFORE_DRIVERS = "calculator_before_drivers.json"       # adjustments applied: first pass
FINAL = "calculator.json"                               # the DCF run: second pass, memo

NO_MARKET_TABLE = ("this run builds no market table: the table needs short interest, which "
                   "no source here serves, so no comparer runs and every reaction-window "
                   "label is absent; prices reach the calculator only")

# The owner's golden cases and their reader, under `evals/`: the owner's, read and
# never written. Both are named here so a tree without them says so.
GOLDEN_CASES = REPO_ROOT / "evals" / "golden" / "cases"
GOLDEN_FORMAT = REPO_ROOT / "evals" / "golden_format.py"
NO_GOLDEN_CASES = ("no evals/golden/cases on this tree: the control does not run under "
                   "--control auto")
NO_GOLDEN_FORMAT = ("no evals/golden_format.py on this tree, so no golden case can be read: "
                    "the control does not run under --control auto")

# The frames of the memo, each the agent(s) that write it, in order, and the file
# the run publishes for it.
FRAMES = {"accounting": (("accounting-analyst",), "analysis_accounting.json"),
          "financial": (("financial-analyst",), "analysis_financial.json"),
          "valuation": (("valuation-analyst", "valuation-analyst-second-pass"),
                        "analysis_valuation.json")}


def _module_at(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_golden_filing(accession: str | None) -> tuple[bool, str]:
    """Whether an approved golden case names this filing, and the one line that
    says why: the manifest records it as `control_reason`.

    A case is a YAML file under `evals/golden/cases/`, read by
    `evals/golden_format.py`'s `load_case`, and it names the filing when its
    `approved_by_owner` is true and its `filing.accession` is this one. A tree
    with no cases directory says so rather than answering False as if it had
    looked; this tree holds the directory, empty until the owner approves a case,
    and the answer then names the accession no case names.
    """
    if not GOLDEN_CASES.is_dir():
        return False, NO_GOLDEN_CASES
    if not GOLDEN_FORMAT.is_file():
        return False, NO_GOLDEN_FORMAT
    if not accession:
        return False, "the run's manifest names no accession, so no golden case can name it"
    golden_format = _module_at(GOLDEN_FORMAT)
    unreadable = []
    for path in sorted(GOLDEN_CASES.glob("*.yaml")):
        try:
            case = golden_format.load_case(path)
        except golden_format.GoldenFormatError:
            unreadable.append(path.name)
            continue
        if (case.get("approved_by_owner") is True
                and (case.get("filing") or {}).get("accession") == accession):
            return True, f"the approved golden case {path.name} names {accession}"
    return False, (f"no approved golden case under evals/golden/cases names {accession}"
                   + (f" ({len(unreadable)} case file(s) could not be read: "
                      f"{', '.join(unreadable)})" if unreadable else ""))


def missing_frames(run: Path, agents: dict) -> dict[str, str]:
    """Why each frame the run has no analysis file for is missing, from the agents'
    records: the limit, a failed call, or a stage the run never reached."""
    hit = limit_hit(agents)
    out = {}
    for frame, (names, written) in FRAMES.items():
        if (run / written).is_file():
            continue
        for name in names:
            record = agents.get(name)
            if record is None:
                out[frame] = (f"{name} did not run: the Fable limit was reached at "
                              f"{', '.join(hit)} and the run stopped there" if hit else
                              f"{name} did not run: the stage before it did not finish")
                break
            if record.get("limit_reached"):
                out[frame] = (f"{name} answered the limit on {FALLBACK_MODEL} too, after the "
                              f"Fable limit ({record.get('reason')})"
                              if record.get("fallback_from") else
                              f"{name} answered the Fable limit ({record.get('reason')}); "
                              "nothing fell back to another model")
                break
            if record.get("result") != "written":
                out[frame] = f"{name} did not write: {record.get('reason')}"
                break
        else:
            out[frame] = f"{written} was not published"
    return out


def on_record(run: Path, name: str, record) -> bool:
    """Whether an agent's gated output is on record in this run: its manifest record
    says written, and the file the run publishes for it is there."""
    return (isinstance(record, dict) and record.get("result") == "written"
            and all((Path(run) / written).is_file() for written in OUTPUT_ON_RECORD[name]))


def stopped_under(manifest: dict, agents: dict) -> tuple[str | None, str]:
    """The model a stopped run ran under: the one its manifest's `model_override`
    names, or None for each definition's own -- and the words for it, which name
    the models served to the agents on record when there was no override, and
    the recorded fallback when the run has one."""
    override = manifest.get("model_override")
    named = override.get("model") if isinstance(override, dict) else None
    fallback = recorded_fallback(manifest)
    fell = (f", fallen back to {fallback['to']} from {fallback.get('first_agent')}"
            if fallback else "")
    if isinstance(named, str) and named:
        return named, named + fell
    served = sorted({str(record.get("model_served") or record.get("model_requested"))
                     for record in agents.values()
                     if record.get("model_served") or record.get("model_requested")})
    return None, ("the definitions' own models"
                  + (f" ({', '.join(served)} served)" if served else "") + fell)


def recorded_fallback(manifest: dict) -> dict | None:
    """The manifest's `model_fallback` row, when the run fell back to Opus."""
    fallback = manifest.get("model_fallback")
    return fallback if isinstance(fallback, dict) and fallback.get("to") else None


def unexplained_mix(name: str, record: dict, fallback: dict | None) -> str | None:
    """Why an agent's record mixes models in a way the record does not explain,
    or None: a Fable request served by another model with no `fallback_from`,
    or a `fallback_from` under a manifest that records no `model_fallback`."""
    asked, served = record.get("model_requested"), record.get("model_served")
    if record.get("fallback_from") and not fallback:
        return (f"{name} on record fell back from {record['fallback_from']}, but the manifest "
                "records no model_fallback")
    if (is_fable(asked) and isinstance(served, str) and served and not is_fable(served)
            and not record.get("fallback_from")):
        return f"{name} on record asked for {asked} and was served {served} with no recorded fallback"
    return None


READERS = ("numbers-reader", "notes-text-reader")


def layer_of(name: str) -> str:
    """The two groups a resume compares models within: the readers, and the
    analysts with the control, which runs on the analysts' model."""
    return "readers" if name in READERS else "analysts"


def definition_name(name: str) -> str:
    """The committed definition a pipeline agent runs: its own, or, for the
    control, the accounting analyst's, whose model it runs on."""
    return "accounting-analyst" if name == "control-single-agent" else agent_inputs.AGENTS[name].prompt


def ran_under(record: dict) -> str | None:
    """The model an agent on record ran under: what it asked for, else what served."""
    asked = record.get("model_requested") or record.get("model_served")
    return asked if isinstance(asked, str) and asked else None


def definitions_agree(run: Path, agents: dict) -> None:
    """Under no override, each pending agent's definition is read through the
    code that chooses a call's model, and its `model:` must be the model the
    agents on record in its layer ran under; a definition edited between the
    nights is refused, because the record could not compare the two. In a run
    that fell back, an agent on record that fell back is read by what its
    definition asked for (`model_requested`, Fable) and served the fallback model
    by the row and its label, which `unexplained_mix` holds: so an unchanged
    definition agrees with it, and one edited between the nights -- to the
    fallback model too -- is refused, under no `--model` and under the resume's
    `--model opus` alike."""
    recorded: dict[str, dict[str, list[str]]] = {}
    for name, record in agents.items():
        model = ran_under(record)
        if model:
            recorded.setdefault(layer_of(name), {}).setdefault(model, []).append(name)
    for name in OUTPUT_ON_RECORD:
        if name in agents or layer_of(name) not in recorded:
            continue
        asks = definition_for(definition_name(name), None)["model"]
        for model, who in recorded[layer_of(name)].items():
            if asks == model or (is_fable(asks) and is_fable(model)):
                continue
            raise RunError(f"{run}: the run stopped under {model}; the definition of "
                           f"{definition_name(name)} now asks for {asks}, which the "
                           "record cannot compare")


def resume_plan(run: Path, manifest: dict, resume: bool,
                model: str | None = None) -> dict | None:
    """What a resumed run starts from, or None for a run that has not run.

    The record decides. A manifest carrying `analysed_utc` is a finished run's:
    `--resume` on it raises NothingToResume when it finished clean, and a run
    that finished with a failure is refused, a correction being a new run. A
    manifest without it whose agents are on record stopped before `finish`: at
    the limit (`fable_limit_reached`) or on an error that raised between an
    agent's return and `finish` (`stopped_on`, written by `run_company`); both
    are resumed, by default or with `--resume`, and no agent whose gated output
    is on record is called again. A run with no agent on record has nothing to
    resume: without `--resume` it starts over, with it the flag is refused.

    The resume runs under the model the stopped run did. `model` is this
    invocation's `--model`; it must be the stopped run's `model_override`, and
    absent when the stopped run had none, or the resume is refused: the agents
    on record and the ones this night would call would then be on two models,
    which the record cannot compare. The agents on record are read too: under
    an override, each one's own record must say it asked for that model; under
    none, each pending agent's definition must still ask for the model the
    agents on record in its layer ran under (`definitions_agree`).

    A run that fell back (`model_fallback` in the manifest) ran under Opus from
    the agent the row names: a resume of it may name `FALLBACK_MODEL` as well,
    and one naming no model carries the fallback forward (`plan["fallback"]`),
    so every pending Fable agent is called on Opus and labelled; once resumed
    under `--model opus`, its override names opus, and the agents on record that
    asked for Fable stay explained by the row. With no override on record, each
    pending definition is held to its layer whether the resume names opus or no
    model. A mix the record does not explain is still refused (`unexplained_mix`).
    """
    recorded = manifest.get("agents")
    if not isinstance(recorded, dict) or not recorded:
        if resume:
            raise RunError(f"{run}: nothing to resume, no agent has run in this directory")
        return None
    stopped = manifest.get("fable_limit_reached")
    if not stopped and FINISH_MARKER in manifest:
        if resume and manifest.get("analysis_failure") is None:
            raise NothingToResume(f"{run}: nothing to resume, the run on record finished")
        raise RunError(f"{run}: the run on record did not stop at the limit "
                       f"(analysis_failure: {manifest.get('analysis_failure')!r}), so there "
                       "is nothing to resume; a correction is a new run")
    agents = {name: dict(record) for name, record in recorded.items()
              if on_record(run, name, record)}
    if not stopped and not agents:
        if resume:
            raise RunError(f"{run}: nothing to resume, no agent's gated output is on record")
        return None                      # it stopped before anything passed: it starts over
    reason = (f"the limit at {', '.join(stopped)}" if stopped else
              f"stopped on {manifest.get('stopped_on') or 'an error before finish wrote the record'}")
    named, under = stopped_under(manifest, agents)
    fallback = recorded_fallback(manifest)
    accepted = {named} | ({fallback["to"]} if fallback else set())
    if (model or None) not in accepted:
        raise RunError(f"{run}: the run stopped under {under}; a resume under "
                       f"{model or 'the definitions\' own models'} would mix models, "
                       "which the record cannot compare")
    for name, record in agents.items():
        mixed = unexplained_mix(name, record, fallback)
        if mixed:
            raise RunError(f"{run}: {mixed}; a resume would mix models, which the record "
                           "cannot compare")
    if named:
        for name, record in agents.items():
            asked = record.get("model_requested")
            if fallback and named == fallback["to"] and is_fable(asked):
                # a fallback run resumed once under --model opus: an agent that
                # asked for Fable ran on it before the limit, or is labelled
                # after it (unexplained_mix above holds the label)
                continue
            if isinstance(asked, str) and asked != named:
                raise RunError(f"{run}: the run stopped under {named}, but {name} on "
                               f"record asked for {asked}; a resume would mix models, "
                               "which the record cannot compare")
    else:
        # no override on record: each pending definition is held to its layer,
        # under no --model and under a fallback run's --model opus alike
        definitions_agree(run, agents)
    return {"agents": agents, "skipped": list(agents), "reason": reason, "override": named,
            "stages": dict(manifest.get("analysis_stages") or {}), "stopped": list(stopped or []),
            "fallback": fallback}


def note_stop(run: Path, exc: BaseException) -> None:
    """The error a run stopped on, into its manifest as `stopped_on`, beside the
    records of every agent that returned before it; `finish` removes it."""
    path = Path(run) / "input_manifest.json"
    if not path.is_file():
        return
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return
    manifest["stopped_on"] = f"{type(exc).__name__}: {exc}"
    write_json(path, manifest)


def run_company(**keyword) -> dict:
    """One run, or one resumed. An error that raises after the run started --
    the analysis gate refusing an analyst's file, the calculator refusing an
    input, the router refusing a directory -- is written into the manifest as
    `stopped_on` beside the agents already on record, and raised; the next
    invocation resumes from that record. A refusal before the run starts (a
    RunError) and a run with nothing to resume are not stops and write nothing.
    """
    try:
        return _run_company(**keyword)
    except (analysis_check.AnalysisInputError, calculator.CalculatorInputError,
            agent_inputs.AgentInputError, cutoff_guard.CutoffGuardError, decide.DecideError,
            market_labels.MarketLabelError, quote_gate.QuoteGateError, OSError,
            ValueError) as exc:
        note_stop(Path(keyword["run"]), exc)
        raise


def _run_company(*, run: Path, ticker: str, form: str, cutoff: str, period_end: str,
                 store: Path, prices: Path | None, model: str | None = None,
                 control: str = "auto", resume: bool = False,
                 on_fable_limit: str = DEFAULT_ON_FABLE_LIMIT,
                 carry_fallback_from: Path | None = None) -> dict:
    run = Path(run)
    logs = run.parent / f".{run.name}.logs"          # outside the record, beside it
    logs.mkdir(exist_ok=True)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("cutoff") != cutoff:
        raise RunError(f"--cutoff {cutoff} is not the bundle's own cutoff "
                       f"{manifest.get('cutoff')}; a later date admits later rows")
    # the batch's fallback, read off the earlier run whose manifest records it:
    # the one named, or, under `opus`, the most recent under this run's root
    carried = (carried_fallback(carry_fallback_from) if carry_fallback_from else
               batch_fallback(run) if on_fable_limit == "opus" else None)
    plan = resume_plan(run, manifest, resume, model)
    stages: dict = plan["stages"] if plan else {}
    agents: dict = plan["agents"] if plan else {}
    skipped: list[str] | None = plan["skipped"] if plan else None
    resumed: str | None = plan["reason"] if plan else None
    if plan and plan["fallback"] and on_fable_limit == "stop":
        row = plan["fallback"]
        raise RunError(f"{run}: the run on record fell back to {row.get('to')} at "
                       f"{row.get('first_agent')}; a --on-fable-limit stop resume would call "
                       "its pending Fable agents on Fable after that, mixing models the other "
                       "way, which the record cannot compare")
    if plan and plan["fallback"] and model and model == plan["fallback"].get("to") \
            and plan["override"] != model:
        # a fallback run resumed under --model opus: the row already puts every
        # pending Fable agent on Opus, so the flag is read as the fallback carried
        # forward, the run continuing under the stopped run's own choice of model
        # -- its override, or the definitions' -- with each such agent labelled,
        # rather than as an override that would record them as asking for Opus
        model = plan["override"]
    # the limit policy, starting from the fallback a resumed run already recorded,
    # or from the batch's when this run carries it
    policy = LimitPolicy(on_fable_limit, plan["fallback"] if plan else None, carried)

    def pending(*names: str) -> tuple[str, ...]:
        """The agents of a stage not already on record: the ones this run calls."""
        return tuple(name for name in names if name not in agents)

    market_data = calculator.market_inputs(ticker, cutoff_guard.parse_date(cutoff, "cutoff"),
                                           prices)
    # a run with a market table is labelled by Python after the quote gate; one
    # without says so in its manifest, once
    if not (run / agent_inputs.MARKET_TABLE).is_file():
        decide.mark_market_unavailable(run, market_data.get("missing") or NO_MARKET_TABLE)

    def calculate(name: str, **extra) -> dict:
        """One calculator stage, written once. On a resumed run a stage file that
        is already there with the same content is re-used; `calculator.json`,
        which the stopped run wrote from what had finished, is written again
        from what has finished now; any other difference is refused."""
        payload = calculator.calculate(ticker=ticker, cutoff=cutoff, period_end=period_end,
                                       form=form, accession=manifest.get("accession"),
                                       fixtures_root=store, bundle=run,
                                       market_data=market_data, **extra)
        problems = calculator_problems(payload, cutoff)
        if problems:
            raise calculator.CalculatorInputError(
                f"{name} would carry what the cutoff and the finite-number rule refuse "
                f"({len(problems)}): " + "; ".join(problems[:5]))
        target = run / name
        if target.exists():
            if _same_json(target, payload):
                return payload
            if plan is None or name != FINAL:
                raise RunError(f"{name} is already in the run with other content; each "
                               "stage is written once")
        write_json(target, payload)
        return payload

    # read: a reader on record from the stopped run is not called again
    readers = pending("numbers-reader", "notes-text-reader")
    if readers:
        agents.update(parallel(run, readers, logs, model, policy))
    if limit_hit(agents):
        # what finished is gated into the run root, so it is on record and the
        # resumed run never calls it again
        finished = tuple(name for name in readers if agents[name]["result"] == "written")
        if finished:
            gate_readers(run, finished)
        return finish(run, agents, stages, "the limit was reached", model, skipped=skipped,
                      resumed_from=resumed, fallback=policy.fallback)
    if any(agents[name]["result"] != "written" for name in ("numbers-reader", "notes-text-reader")):
        return finish(run, agents, stages, "a reader failed twice", model, skipped=skipped,
                      resumed_from=resumed,
                      fallback=policy.fallback)
    if readers:
        # the readers this invocation called, and no other: a report gated on
        # the night the limit hit stays as the run root holds it
        stages["quote_gate"] = {"dropped": len(gate_readers(run, readers).get("dropped", []))}
        # the market labels: Python, on the gated reports; with no market table
        # the record says so and nothing is written. The file is re-checked as
        # soon as it is written: every label cites an item standing in its own
        # report.
        stages["market_labels"] = market_labels.write(run)
        if stages["market_labels"]["written"]:
            stages["market_labels_check"] = market_labels.check(run)

    # calculate, then the two analysts, never merged, on the view with no price.
    # What finished is gated and published whether or not the other analyst
    # answered the limit: a limit stops what comes after it, not what stood.
    base = calculate(BEFORE_ANALYSTS)
    write_json(run / calculator.FILINGS_ONLY, calculator.filings_only(base))
    analysts = pending("accounting-analyst", "financial-analyst")
    if analysts:
        agents.update(parallel(run, analysts, logs, model, policy))
    for name, kind in (("accounting-analyst", "accounting"), ("financial-analyst", "financial")):
        if agents[name]["result"] == "written" and not (run / f"analysis_{kind}.json").is_file():
            checked = check_analysis(run, name, kind)
            write_json(run / f"analysis_{kind}.json", checked)
            stages[f"analysis_{kind}"] = {"dropped": checked["dropped_count"]}
    accounting = _load(run / "analysis_accounting.json")

    # value: adjustments first, then drivers, then the reading -- unless the
    # limit stopped the run at the analysts, in which case nothing runs after it
    final_written = False
    if not limit_hit(agents):
        calculate(BEFORE_DRIVERS, accounting=accounting)
        if ((run / "analysis_accounting.json").is_file()
                and (run / "analysis_financial.json").is_file()):
            if pending("valuation-analyst"):
                agents["valuation-analyst"] = run_agent(run, "valuation-analyst", logs, model,
                                                         policy)
            if agents["valuation-analyst"]["result"] == "written":
                if not (run / "assumptions.json").is_file():
                    assumptions = check_analysis(run, "valuation-analyst", "assumptions")
                    write_json(run / "assumptions.json", assumptions)
                    stages["assumptions"] = {"dropped": assumptions["dropped_count"]}
                assumptions = _load(run / "assumptions.json")
                calculate(FINAL, accounting=accounting, assumptions=assumptions)
                final_written = True
                if pending("valuation-analyst-second-pass"):
                    agents["valuation-analyst-second-pass"] = run_agent(
                        run, "valuation-analyst-second-pass", logs, model, policy)
                if (agents["valuation-analyst-second-pass"]["result"] == "written"
                        and not (run / "analysis_valuation.json").is_file()):
                    checked = check_analysis(run, "valuation-analyst-second-pass", "valuation")
                    write_json(run / "analysis_valuation.json", checked)
                    stages["analysis_valuation"] = {"dropped": checked["dropped_count"]}
    if not final_written:
        calculate(FINAL, accounting=accounting)

    # the formula baselines, Python only, beside the analyses and never merged
    try:
        (run / "baselines.json").write_text(baselines.render(baselines.baselines(
            ticker, form, fixtures_root=store)), encoding="utf-8")
        stages["baselines"] = "written"
    except (baselines.BaselineInputError, trends.TrendInputError,
            cutoff_guard.CutoffGuardError, OSError, ValueError) as exc:
        stages["baselines"] = f"not written: {exc}"

    # the memo, from what exists, saying which frame is missing and why -- then
    # the control, unless the limit stopped the run
    (run / "memo_ko.md").write_text(memo.memo(
        ticker=ticker, form=form, period_end=period_end, cutoff=cutoff,
        fields=_load(run / FINAL), filings_only=_load(run / calculator.FILINGS_ONLY),
        accounting=_load(run / "analysis_accounting.json"),
        financial=_load(run / "analysis_financial.json"),
        valuation=_load(run / "analysis_valuation.json"),
        baselines=_load(run / "baselines.json"),
        missing=missing_frames(run, agents)), encoding="utf-8")
    memo_words_hold(run / "memo_ko.md")
    if limit_hit(agents):
        return finish(run, agents, stages, "the limit was reached", model, skipped=skipped,
                      resumed_from=resumed, fallback=policy.fallback)
    if control == "auto":
        golden, control_reason = is_golden_filing(manifest.get("accession"))
    else:
        golden, control_reason = control == "always", f"--control {control}"
    if golden and pending("control-single-agent"):
        agents["control-single-agent"] = run_control(run, logs, model, rebuild=plan is not None,
                                                      policy=policy)
        if limit_hit(agents):
            return finish(run, agents, stages, "the limit was reached", model,
                          control_reason=control_reason, skipped=skipped, resumed_from=resumed,
                          fallback=policy.fallback)
        if agents["control-single-agent"]["result"] == "written":
            stages["control"] = check_control(run)
    elif not golden:
        stages["control"] = f"skipped: {control_reason}"
    silent = [name for name, record in agents.items() if record.get("result") != "written"]
    return finish(run, agents, stages,
                  f"did not write: {', '.join(silent)}" if silent else None, model,
                  control_reason=control_reason, skipped=skipped, resumed_from=resumed,
                  fallback=policy.fallback)


def memo_words_hold(path: Path) -> None:
    """No line of the memo carries a ruled-out word, accusation or recommendation,
    whichever analysis the line came from: the owner's forbidden_words reads the
    memo line by line with both (`evals/regression/coverage.py`). The analysis
    gate already holds what the memo prints to both; this is the memo as written,
    and a hit stops the run rather than publishing it."""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for pattern in (analysis_check.ACCUSATION, analysis_check.RECOMMENDATION):
            hit = pattern.search(line)
            if hit:
                raise analysis_check.AnalysisInputError(
                    f"{path.name}:{number} carries a ruled-out word ({hit.group(0)!r})")


# A date, a date pair or a date-time stamp, as a whole string value or key of a
# calculator file: the owner's ISO_DATE (`evals/regression/mechanical.py`), which
# its nothing_after_cutoff holds to the cutoff. A date inside prose is not one.
ISO_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})(?:[T ][0-9:.+\-Z]*)?(?:\.\.(\d{4}-\d{2}-\d{2}))?")


def calculator_problems(payload, cutoff: str) -> list[str]:
    """Why a calculator stage would fail the owner's graders before it is written:
    a date after the cutoff as any whole string value or key (nothing_after_cutoff
    reads every calculator file, the agents' copies included), and a number that
    is not finite, or a `value` that is neither a finite number, text, a container
    nor null (calculator_finite)."""
    limit = dt.date.fromisoformat(cutoff)
    out: list[str] = []

    def late(text: str, where: str) -> None:
        match = ISO_DATE.fullmatch(text)
        for day in (match.group(1), match.group(2)) if match else ():
            try:
                after = bool(day) and dt.date.fromisoformat(day) > limit
            except ValueError:
                after = False
            if after:
                out.append(f"{where} = {text} is after the cutoff {cutoff}")
                return

    def walk(node, where: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                here = f"{where}.{key}" if where else str(key)
                late(str(key), here)
                if key == "value" and value is not None \
                        and not isinstance(value, (str, list, dict)) and not _finite(value):
                    out.append(f"{here} = {value!r} is not a finite number")
                walk(value, here)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{where}[{index}]")
        elif isinstance(node, str):
            late(node, where)
        elif isinstance(node, float) and not math.isfinite(node):
            out.append(f"{where} = {node!r} is not a finite number")

    walk(payload, "")
    return list(dict.fromkeys(out))         # a `value` that is a float is met twice


def _finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) \
        and math.isfinite(value)


def _same_json(path: Path, payload) -> bool:
    """Whether the file holds this payload: compared as JSON text with sorted keys,
    so a NaN, which is never equal to itself, still reads as the same number."""
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return json.dumps(existing, sort_keys=True) == json.dumps(payload, sort_keys=True)


def control_sees(run: Path) -> list[str]:
    """The whole bundle and the calculator as it stood before any analyst wrote.

    Not the market table and not the manifest, as the retired control; and not a
    calculator that carries an analyst's adjustment or a valuation driver, because
    a control that reads what the layers wrote cannot say what they add. Not the
    three files no builder writes yet either, which the owner's layer table does
    not name for the control (`agent_inputs.NOT_BUILT_YET`).
    """
    return sorted([name for name in agent_inputs.BUNDLE_CATALOGUE
                   if name.startswith("input_") and name != agent_inputs.MANIFEST
                   and name != agent_inputs.MARKET_TABLE
                   and name not in agent_inputs.NOT_BUILT_YET and (run / name).is_file()]
                  + [BEFORE_ANALYSTS])


def control_violations(run: Path) -> list[str]:
    """The single-agent control's directory held as the owner's layers_hold and
    inputs_on_record hold it (`evals/regression/mechanical.py`, which walks the
    control's directory beside the agents'): every file in it is one
    `control_sees` routes, byte for byte the run's, or one the control wrote
    (`control_*`, the owner's `is_own_output`), and nothing in it is a directory
    or a link. A stray file the control leaves fails both of the owner's checks."""
    directory = run / CONTROL_DIRNAME
    if not directory.is_dir():
        return []
    routed = set(control_sees(run))
    found = []
    for path in sorted(directory.iterdir()):
        where = f"{CONTROL_DIRNAME}/{path.name}"
        if path.is_symlink() or not path.is_file():
            found.append(f"{where}: a directory or a link inside the control's, which nothing "
                         "routed")
        elif path.name.startswith("control_"):
            continue                    # what the control writes
        elif path.name not in routed:
            found.append(f"{where}: not a file the control is handed")
        elif path.read_bytes() != (run / path.name).read_bytes():
            found.append(f"{where}: not the run's {path.name}, byte for byte")
    return found


def run_control(run: Path, logs: Path, model: str | None = None, *,
                rebuild: bool = False, policy: LimitPolicy | None = None) -> dict:
    """The single-agent control: the whole bundle and the base calculator, one call.

    The directory is built once. On a resumed run (`rebuild`) the control is
    the stopped agent -- its directory stands from the night the limit hit it,
    and none of its three files reached the run root -- so the directory is
    cleared and built again, like any other agent's rerun with identical input.
    """
    directory = run / CONTROL_DIRNAME
    if directory.exists():
        if not rebuild or any((run / name).is_file() for name in CONTROL_WRITES):
            raise RunError(f"{directory} already exists; the control's directory is built once")
        shutil.rmtree(directory)
    directory.mkdir()
    sees = control_sees(run)
    prior = run / "input_prior_predictions.md"
    if prior.is_file():
        text = prior.read_text(encoding="utf-8")
        leak = agent_inputs._probability_leak(text)
        if leak is not None:
            raise RunError(f"{prior} still carries a probability ({leak})")
        figure = agent_inputs._market_figure(text)
        if figure is not None:
            raise RunError(f"{prior} carries a price or return figure ({figure!r})")
    for name in sees:
        shutil.copyfile(run / name, directory / name)
    spec = definition_for("accounting-analyst", model)
    control = {"description": "the single-agent control", "prompt": CONTROL_PROMPT.format(
        files=", ".join(sees)), "tools": ["Read", "Write"], "model": spec["model"]}
    earlier = recorded_agent(run, "control-single-agent")
    record = call(run, directory, agent="control-single-agent", writes=CONTROL_WRITES,
                  message="Write the three files.", spec=control,
                  log=logs / "control-single-agent.log", policy=policy or LimitPolicy())
    record = carried_forward(earlier, record)
    record_agent(run, "control-single-agent", record)
    boundary_holds(run, "after the control returned")
    return record


def check_control(run: Path) -> dict:
    """The control's three files, held to the same gate as the analysts'."""
    directory = run / CONTROL_DIRNAME
    fields = json.loads((directory / BEFORE_ANALYSTS).read_text(encoding="utf-8"))
    sources = {path.name: path.read_text(encoding="utf-8") for path in directory.iterdir()
               if path.name.startswith("input_")}
    out = {}
    for written, kind in zip(CONTROL_WRITES, ("accounting", "financial", "assumptions")):
        payload = json.loads((directory / written).read_text(encoding="utf-8"))
        checked = (analysis_check.check_assumptions(payload, fields=fields, sources=sources)
                   if kind == "assumptions" else
                   analysis_check.check(kind, payload, fields=fields, sources=sources,
                                        paragraph_ids=True))
        write_json(run / written, checked)
        out[kind] = {"dropped": checked["dropped_count"]}
    return out


def _load(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def finish(run: Path, agents: dict, stages: dict, failure: str | None,
           model: str | None = None, control_reason: str | None = None,
           skipped: list[str] | None = None, resumed_from: str | None = None,
           fallback: dict | None = None) -> dict:
    # Read again: the quote gate, the market marker, the router, every call's
    # own record and the fallback row wrote to it since the start. The router's
    # record of what it trimmed for the valuation analyst (`agents.<name>.trimmed`,
    # src/agent_inputs.py) is kept beside the usage record; the boundary check
    # reads it. `analysed_utc` is written here and nowhere else: it is what says
    # the run finished, and a resume never runs over a manifest that carries it.
    boundary_holds(run, "before the run was recorded as finished")
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    routed = manifest.get("agents") if isinstance(manifest.get("agents"), dict) else {}
    manifest["agents"] = {name: agent_entry(record, routed.get(name))
                          for name, record in agents.items()}
    manifest["analysis_stages"] = stages
    manifest["analysis_failure"] = failure
    manifest.pop("stopped_on", None)                # the stopped run's; this one finished
    if control_reason is not None:
        manifest["control_reason"] = control_reason
    if skipped is not None:
        # a resumed run: the agents on record from the stopped run were not called
        manifest["resumed_at"] = utc_now()
        manifest["resume_skipped"] = skipped
        manifest["resumed_from"] = resumed_from
    if fallback:
        # the run fell back to Opus at the agent the row names: kept, so the
        # graders and the batch sizer can tell a fallback run from a Fable run
        manifest["model_fallback"] = fallback
    else:
        # a row this run's policy does not hold is an earlier attempt's, from a
        # run that started over: it would name a fallback this run never made
        manifest.pop("model_fallback", None)
    hit = limit_hit(agents)
    manifest.pop("fable_limit_reached", None)      # the stopped run's; set again below if hit
    if hit:
        manifest["fable_limit_reached"] = hit
        fell = [name for name in hit if agents[name].get("fallback_from")]
        manifest["analysis_failure"] = (
            f"the limit was reached at {', '.join(hit)}: the run stopped there, "
            + (f"{FALLBACK_MODEL} answered the limit too at {', '.join(fell)}, " if fell else
               "nothing fell back to another model, ")
            + "and the batch stops (docs/needs_judgment.md)")
    # the override is this invocation's record, never the stopped run's carried
    # forward: it names the agents this invocation called, and an agent on record
    # from the stopped run says in its own record what it asked for
    manifest.pop("model_override", None)
    if model:
        manifest["model_override"] = {
            "model": model,
            "applies_to": [name for name in agents if name not in (skipped or ())],
            "why": "named with --model in place of each definition's own, for the agents "
                   "applies_to lists, which this invocation called; the owner's decision "
                   "that names it is in docs/structure_changes.md"}
    manifest[FINISH_MARKER] = utc_now()
    write_json(run / "input_manifest.json", manifest)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="read, analyse and value one extracted run")
    parser.add_argument("--run", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", required=True, choices=["10-K", "10-Q"])
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--period-end", required=True)
    parser.add_argument("--store", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--prices", default=None)
    parser.add_argument("--model", default=None,
                        help="one model for every agent, in place of each definition's own")
    parser.add_argument("--control", default="auto", choices=["auto", "always", "never"],
                        help="the single-agent control: auto runs it on golden filings only")
    parser.add_argument("--resume", action="store_true",
                        help="continue a run the limit stopped: agents on record are not "
                             "called again (the default when the manifest records "
                             "fable_limit_reached)")
    parser.add_argument("--on-fable-limit", default=DEFAULT_ON_FABLE_LIMIT, choices=ON_FABLE_LIMIT,
                        help="what a Fable call answering the limit does to the rest of the "
                             "run: opus (the owner's decision of 2026-10-07) calls the agent "
                             "again on Opus and every later Fable agent too, each recorded as "
                             "a fallback; stop (the rule of 2026-10-06) stops the run, exit 4")
    parser.add_argument("--carry-fallback-from", default=None,
                        help="the run directory, earlier in this batch, whose manifest "
                             "records model_fallback: every Fable agent of this run is "
                             "called on Opus from its first call, recorded as a fallback")
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    try:
        manifest = run_company(run=Path(args.run), ticker=args.ticker, form=args.form,
                               cutoff=args.cutoff, period_end=args.period_end,
                               store=Path(args.store),
                               prices=Path(args.prices) if args.prices else None,
                               model=args.model, control=args.control, resume=args.resume,
                               on_fable_limit=args.on_fable_limit,
                               carry_fallback_from=(Path(args.carry_fallback_from)
                                                    if args.carry_fallback_from else None))
    except NothingToResume as exc:
        print(f"run_analysis: {exc}")
        return 0
    except (RunError, agent_inputs.AgentInputError, analysis_check.AnalysisInputError,
            calculator.CalculatorInputError, cutoff_guard.CutoffGuardError,
            decide.DecideError, market_labels.MarketLabelError, quote_gate.QuoteGateError,
            OSError, ValueError) as exc:
        # the record of every call that returned is already on disk, and the
        # manifest says what the run stopped on; the next invocation resumes it
        print(f"run_analysis: {exc}", file=sys.stderr)
        return BAD_INPUT
    print(json.dumps({name: {k: record.get(k) for k in ("result", "model_served",
                                                        "input_tokens", "output_tokens",
                                                        "cost_usd")}
                      for name, record in manifest["agents"].items()}, indent=1))
    fallback = recorded_fallback(manifest)
    stopped = manifest.get("fable_limit_reached")
    if stopped:
        # a limit stopped the run: nothing is carried. Under `opus` it was the
        # model a Fable limit falls back to, and the batch stops
        # (docs/routines/nightly-worker.md); under `stop`, exit 4 says so
        if args.on_fable_limit == "opus":
            print(f"run_analysis: a limit stopped this run at {', '.join(stopped)} on "
                  f"{FALLBACK_MODEL}, the model a Fable limit falls back to: stop the batch "
                  "(fable_limit_reached in the manifest); nothing is carried", file=sys.stderr)
    elif fallback and fallback_reason(fallback) == FALLBACK_REASON:
        # the rest of the batch carries it: every later run under the same root
        # on its own, a run elsewhere by the flag; on stderr, so the JSON above
        # stays the whole of stdout
        limit_at = fallback.get("carried_limit_at") or fallback.get("at")
        print(f"run_analysis: fell back to {fallback['to']} at {fallback.get('first_agent')} "
              f"(model_fallback in {Path(args.run) / 'input_manifest.json'}); every later run "
              f"under {Path(args.run).parent.parent} carries it on its own for {CARRY_HOURS} "
              f"hours from {limit_at}, and a run elsewhere names it with "
              f"--carry-fallback-from {args.run}", file=sys.stderr)
    elif fallback:
        # the shape alone does not confirm the limit: the fallback stays here
        print(f"run_analysis: fell back to {fallback['to']} at {fallback.get('first_agent')} "
              f"on a Fable failure shaped like the limit ({SHAPE_FALLBACK_REASON}: no token "
              f"spent, under {LIMIT_SECONDS} seconds, no limit message), which does not "
              "confirm the limit; the fallback stays inside this run, and no later run "
              "carries it", file=sys.stderr)
    if manifest.get("fable_limit_reached"):
        # a limit stopped the run: exit 4 under `stop` alone, so the batch stops;
        # under `opus` the limit was the fallback model's own -- answered after
        # a Fable limit, or by an agent that asked for Opus -- and the run failed
        return LIMIT_REACHED if args.on_fable_limit == "stop" else FAILED
    return FAILED if manifest.get("analysis_failure") else 0


if __name__ == "__main__":
    sys.exit(main())
