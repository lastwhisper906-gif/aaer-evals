"""Run the analysis-grader on one published run and put its grade.json beside it.

The grader is `.claude/agents/analysis-grader.md`, on Opus. It sees the run's
published outputs and `evals/capability/rubric.md`, copied into a directory of its
own outside the run, and never an analyst's directory or log. Its answer is written
into the run as `grade.json`, a new file: nothing the run published before is
touched (runs/ is append-only). `make eval` reports the scores it finds and gates
none of them until the owner sets a floor.

    python3.12 -m src.grade_run --run runs/STX/0001137789-26-000159
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

try:
    from src import interpreter_pin, run_analysis
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, run_analysis

REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC = REPO_ROOT / "evals" / "capability" / "rubric.md"
SEES = ("analysis_accounting.json", "analysis_financial.json", "analysis_valuation.json",
        "assumptions.json", "report_numbers.md", "report_notes_text.md", "calculator.json",
        "calculator_filings_only.json", "input_manifest.json", "memo_ko.md")
WRITES = "grade.json"


class GradeError(RuntimeError):
    pass


def grader_sees(run: Path) -> list[Path]:
    files = [run / name for name in SEES if (run / name).is_file()]
    files += sorted(p for p in run.glob("input_*.md") if p.is_file())
    return files


def grade(run: Path, *, ask=None) -> dict:
    run = Path(run)
    if (run / WRITES).exists():
        raise GradeError(f"{run / WRITES} is already published; a run is graded once")
    ask = ask or run_analysis.ask
    with tempfile.TemporaryDirectory(prefix="analysis-grader-") as tmp:
        directory = Path(tmp)
        for source in grader_sees(run) + [RUBRIC]:
            shutil.copyfile(source, directory / source.name)
        files = sorted(p.name for p in directory.iterdir())
        spec = run_analysis.definition("analysis-grader")
        record = ask(directory, agent="analysis-grader", writes=(WRITES,),
                     message=run_analysis.INSTRUCTION.format(files=", ".join(files),
                                                             writes=WRITES),
                     spec=spec, log=directory / "grader.log")
        if record.get("result") != "written":
            return record
        payload = json.loads((directory / WRITES).read_text(encoding="utf-8"))
    payload["grader"] = {k: record.get(k) for k in ("model_requested", "model_served",
                                                     "input_tokens", "output_tokens",
                                                     "cost_usd", "seconds")}
    (run / WRITES).write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="grade one run with the analysis-grader")
    parser.add_argument("--run", required=True)
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    try:
        record = grade(Path(args.run))
    except (GradeError, OSError, ValueError) as exc:
        print(f"grade_run: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({k: record.get(k) for k in ("result", "model_served", "output_tokens")}))
    return 0 if record.get("result") == "written" else 1


if __name__ == "__main__":
    sys.exit(main())
