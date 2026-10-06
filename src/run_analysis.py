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
record says the model it asked for, and the manifest's `model_override` says why.
The owner's decision of 2026-09-30 runs the analysts on Opus while the Fable
limit holds (`docs/structure_changes.md`).

**A failed call is retried once with identical input**, then recorded as failed.
A retry never changes the input. The run goes on past a failed analyst, so what
did write still reaches the memo, but the manifest's `analysis_failure` names
every agent that did not write and the command exits non-zero: a run missing an
analysis is never reported as finished.

**Every agent's usage is recorded** in `input_manifest.json` under `agents`: the
model asked for, the model that served, input, cache and output tokens, turns,
cost and wall time, so the monthly cost of the pipeline is read off the record
rather than estimated.

    python3.12 -m src.run_analysis --run runs/NVDA/0001045810-26-000075 \\
        --ticker NVDA --form 10-Q --cutoff 2026-08-26 --period-end 2026-07-26 \\
        [--store tests/fixtures] [--prices <directory>] [--model opus]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
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

# The pins: the family the definition names, and the effort it runs at.
# `docs/HOW_WE_WORK.md` §6 -- readers on Opus at xhigh; the analysts inherit the
# supervisors' pin, Fable, and the single-agent control runs on the same model
# as the analysts, because a control on another model measures the model.
EFFORT = "xhigh"
CALL_TIMEOUT_SECONDS = 3600
RETRIES = 1

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


def ask(directory: Path, *, agent: str, writes: tuple[str, ...], message: str,
        spec: dict, log: Path) -> dict:
    """One restricted session in `directory`; the usage record, or a failure."""
    record: dict = {"agent": agent, "writes": list(writes)}
    for attempt in range(1, RETRIES + 2):
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
        record.update(usage_record(result, requested=spec["model"], seconds=seconds,
                                   attempt=attempt))
        written = all((directory / name).is_file() for name in writes)
        if done.returncode == 0 and written and not result.get("is_error"):
            record["result"] = "written"
            return record
        record["result"] = "failed"
        record["reason"] = (f"exit {done.returncode}; wrote "
                            f"{[n for n in writes if (directory / n).is_file()]}")
        for name in writes:        # identical input on the retry: nothing it wrote survives
            (directory / name).unlink(missing_ok=True)
    return record


def definition_for(prompt: str, model: str | None) -> dict:
    """The committed definition, with the owner's model in place of its own if named."""
    spec = definition(prompt)
    return dict(spec, model=model) if model else spec


def run_agent(run: Path, name: str, logs: Path, model: str | None = None) -> dict:
    agent_inputs.build(run, name)
    directory = agent_inputs.session_root(run, name)
    spec = agent_inputs.AGENTS[name]
    files = sorted(path.name for path in directory.iterdir() if path.name != spec.writes)
    message = INSTRUCTION.format(files=", ".join(files), writes=spec.writes)
    return ask(directory, agent=spec.prompt, writes=(spec.writes,), message=message,
               spec=definition_for(spec.prompt, model), log=logs / f"{name}.log")


def parallel(run: Path, names: tuple[str, ...], logs: Path,
             model: str | None = None) -> dict[str, dict]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(names)) as pool:
        futures = {name: pool.submit(run_agent, run, name, logs, model) for name in names}
        return {name: future.result() for name, future in futures.items()}


# --- the gates -----------------------------------------------------------------------------

# One reading of a report's items, shared with the market labels.
report_items = market_labels.report_items


def gate_readers(run: Path) -> dict:
    """The quote gate over both reader reports, and the reports downstream sees.

    Each reader's own report stays in its directory as what it wrote. The copy at
    the run root -- the one the analysts are handed -- carries only the items
    that stood, with a line saying how many the gate removed and that the
    manifest lists them, so no analyst builds on an item that failed its quote.
    """
    reports = []
    for name in ("numbers-reader", "notes-text-reader"):
        directory = agent_inputs.session_root(run, name)
        writes = agent_inputs.AGENTS[name].writes
        written = directory / writes
        if not written.is_file():
            raise RunError(f"{name} wrote no {writes}")
        reports.append({"report": writes, "items": report_items(written.read_text("utf-8")),
                        "input": directory})
    result = quote_gate.gate(reports, run)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    dropped = {row.get("item_id") for row in manifest.get("dropped_items") or []}
    for name in ("numbers-reader", "notes-text-reader"):
        writes = agent_inputs.AGENTS[name].writes
        text = (agent_inputs.session_root(run, name) / writes).read_text(encoding="utf-8")
        removed = 0

        def keep(match: re.Match) -> str:
            nonlocal removed
            items = report_items(match.group(0))
            if items and all(item.get("id") in dropped for item in items):
                removed += 1
                return ""
            return match.group(0)

        gated = re.sub(r"```json\s*.*?```\n?", keep, text, flags=re.S)
        note = (f"<!-- the quote gate removed {removed} item(s) from this copy; "
                f"input_manifest.json lists each with its reason -->\n")
        (run / writes).write_text(note + gated, encoding="utf-8")
    return result


def check_analysis(run: Path, name: str, kind: str) -> dict:
    directory = agent_inputs.session_root(run, name)
    written = directory / agent_inputs.AGENTS[name].writes
    payload = json.loads(written.read_text(encoding="utf-8"))
    seen = next(directory / name for name in (calculator.FILINGS_ONLY, BEFORE_DRIVERS, FINAL)
                if (directory / name).is_file())
    fields = json.loads(seen.read_text(encoding="utf-8"))
    sources = analysis_check.read_sources(directory, analysis_check.SOURCES[kind])
    if kind == "assumptions":
        return analysis_check.check_assumptions(payload, fields=fields, sources=sources)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    dropped = {row.get("item_id") for row in manifest.get("dropped_items") or []
               if row.get("item_id")}
    return analysis_check.check(kind, payload, fields=fields, sources=sources, excluded=dropped)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


# --- the run --------------------------------------------------------------------------------

# The calculator at each stage, each written once, so what an agent was handed is
# still at the run root under the same name when the run is published:
BEFORE_ANALYSTS = "calculator_before_analysts.json"     # the control, and the base
BEFORE_DRIVERS = "calculator_before_drivers.json"       # adjustments applied: first pass
FINAL = "calculator.json"                               # the DCF run: second pass, memo

NO_MARKET_TABLE = ("this run builds no market table: the table needs short interest, which "
                   "no source here serves, so no comparer runs and every reaction-window "
                   "label is absent; prices reach the calculator only")


def run_company(*, run: Path, ticker: str, form: str, cutoff: str, period_end: str,
                store: Path, prices: Path | None, model: str | None = None) -> dict:
    run = Path(run)
    logs = run.parent / f".{run.name}.logs"          # outside the record, beside it
    logs.mkdir(exist_ok=True)
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("cutoff") != cutoff:
        raise RunError(f"--cutoff {cutoff} is not the bundle's own cutoff "
                       f"{manifest.get('cutoff')}; a later date admits later rows")
    stages: dict = {}
    agents: dict = {}

    market_data = calculator.market_inputs(ticker, cutoff_guard.parse_date(cutoff, "cutoff"),
                                           prices)
    decide.mark_market_unavailable(run, market_data.get("missing") or NO_MARKET_TABLE)

    def calculate(name: str, **extra) -> dict:
        payload = calculator.calculate(ticker=ticker, cutoff=cutoff, period_end=period_end,
                                       form=form, accession=manifest.get("accession"),
                                       fixtures_root=store, bundle=run,
                                       market_data=market_data, **extra)
        if (run / name).exists():
            raise RunError(f"{name} is already in the run; each stage is written once")
        write_json(run / name, payload)
        return payload

    # read
    agents.update(parallel(run, ("numbers-reader", "notes-text-reader"), logs, model))
    if any(agents[name]["result"] != "written" for name in ("numbers-reader", "notes-text-reader")):
        return finish(run, agents, stages, "a reader failed twice", model)
    stages["quote_gate"] = {"dropped": len(gate_readers(run).get("dropped", []))}
    # the market labels: Python, on the gated reports; with no market table the
    # record says so and nothing is written
    stages["market_labels"] = market_labels.write(run)

    # calculate, then the two analysts, never merged, on the view with no price
    base = calculate(BEFORE_ANALYSTS)
    write_json(run / calculator.FILINGS_ONLY, calculator.filings_only(base))
    agents.update(parallel(run, ("accounting-analyst", "financial-analyst"), logs, model))
    for name, kind in (("accounting-analyst", "accounting"), ("financial-analyst", "financial")):
        if agents[name]["result"] == "written":
            checked = check_analysis(run, name, kind)
            write_json(run / f"analysis_{kind}.json", checked)
            stages[f"analysis_{kind}"] = {"dropped": checked["dropped_count"]}
    accounting = _load(run / "analysis_accounting.json")

    # value: adjustments first, then drivers, then the reading
    calculate(BEFORE_DRIVERS, accounting=accounting)
    if (run / "analysis_accounting.json").is_file() and (run / "analysis_financial.json").is_file():
        agents["valuation-analyst"] = run_agent(run, "valuation-analyst", logs, model)
        if agents["valuation-analyst"]["result"] == "written":
            assumptions = check_analysis(run, "valuation-analyst", "assumptions")
            write_json(run / "assumptions.json", assumptions)
            stages["assumptions"] = {"dropped": assumptions["dropped_count"]}
            calculate(FINAL, accounting=accounting, assumptions=assumptions)
            agents["valuation-analyst-second-pass"] = run_agent(
                run, "valuation-analyst-second-pass", logs, model)
            if agents["valuation-analyst-second-pass"]["result"] == "written":
                checked = check_analysis(run, "valuation-analyst-second-pass", "valuation")
                write_json(run / "analysis_valuation.json", checked)
                stages["analysis_valuation"] = {"dropped": checked["dropped_count"]}
    if not (run / FINAL).exists():
        calculate(FINAL, accounting=accounting)

    # the formula baselines, Python only, beside the analyses and never merged
    try:
        (run / "baselines.json").write_text(baselines.render(baselines.baselines(
            ticker, form, fixtures_root=store)), encoding="utf-8")
        stages["baselines"] = "written"
    except (baselines.BaselineInputError, trends.TrendInputError,
            cutoff_guard.CutoffGuardError, OSError, ValueError) as exc:
        stages["baselines"] = f"not written: {exc}"

    # the memo -- each section filled from the calculator its analyst read -- then the control
    (run / "memo_ko.md").write_text(memo.memo(
        ticker=ticker, form=form, period_end=period_end, cutoff=cutoff,
        fields=_load(run / FINAL), filings_only=_load(run / calculator.FILINGS_ONLY),
        accounting=_load(run / "analysis_accounting.json"),
        financial=_load(run / "analysis_financial.json"),
        valuation=_load(run / "analysis_valuation.json"),
        baselines=_load(run / "baselines.json")), encoding="utf-8")
    agents["control-single-agent"] = run_control(run, logs, model)
    if agents["control-single-agent"]["result"] == "written":
        stages["control"] = check_control(run)
    silent = [name for name, record in agents.items() if record.get("result") != "written"]
    return finish(run, agents, stages,
                  f"did not write: {', '.join(silent)}" if silent else None, model)


def control_sees(run: Path) -> list[str]:
    """The whole bundle and the calculator as it stood before any analyst wrote.

    Not the market table and not the manifest, as the retired control; and not a
    calculator that carries an analyst's adjustment or a valuation driver, because
    a control that reads what the layers wrote cannot say what they add.
    """
    return sorted([name for name in agent_inputs.BUNDLE_CATALOGUE
                   if name.startswith("input_") and name != agent_inputs.MANIFEST
                   and name != agent_inputs.MARKET_TABLE and (run / name).is_file()]
                  + [BEFORE_ANALYSTS])


def run_control(run: Path, logs: Path, model: str | None = None) -> dict:
    """The single-agent control: the whole bundle and the base calculator, one call."""
    directory = run / CONTROL_DIRNAME
    if directory.exists():
        raise RunError(f"{directory} already exists; the control's directory is built once")
    directory.mkdir()
    sees = control_sees(run)
    prior = run / "input_prior_predictions.md"
    if prior.is_file():
        leak = agent_inputs._probability_leak(prior.read_text(encoding="utf-8"))
        if leak is not None:
            raise RunError(f"{prior} still carries a probability ({leak})")
    for name in sees:
        shutil.copyfile(run / name, directory / name)
    spec = definition_for("accounting-analyst", model)
    control = {"description": "the single-agent control", "prompt": CONTROL_PROMPT.format(
        files=", ".join(sees)), "tools": ["Read", "Write"], "model": spec["model"]}
    return ask(directory, agent="control-single-agent", writes=CONTROL_WRITES,
               message="Write the three files.", spec=control,
               log=logs / "control-single-agent.log")


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
           model: str | None = None) -> dict:
    # Read again: the quote gate and the market marker wrote to it since the start.
    manifest = json.loads((run / "input_manifest.json").read_text(encoding="utf-8"))
    manifest["agents"] = {name: {key: value for key, value in record.items()
                                 if key not in ("writes",)}
                          for name, record in agents.items()}
    manifest["analysis_stages"] = stages
    manifest["analysis_failure"] = failure
    if model:
        manifest["model_override"] = {
            "model": model, "applies_to": "every agent and the control",
            "why": "named with --model in place of each definition's own; the owner's "
                   "decision that names it is in docs/structure_changes.md"}
    manifest["analysed_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    try:
        manifest = run_company(run=Path(args.run), ticker=args.ticker, form=args.form,
                               cutoff=args.cutoff, period_end=args.period_end,
                               store=Path(args.store),
                               prices=Path(args.prices) if args.prices else None,
                               model=args.model)
    except (RunError, agent_inputs.AgentInputError, calculator.CalculatorInputError,
            cutoff_guard.CutoffGuardError, decide.DecideError,
            market_labels.MarketLabelError, OSError, ValueError) as exc:
        print(f"run_analysis: {exc}", file=sys.stderr)
        return BAD_INPUT
    print(json.dumps({name: {k: record.get(k) for k in ("result", "model_served",
                                                        "input_tokens", "output_tokens",
                                                        "cost_usd")}
                      for name, record in manifest["agents"].items()}, indent=1))
    return FAILED if manifest.get("analysis_failure") else 0


if __name__ == "__main__":
    sys.exit(main())
