"""Subscription-Codex cross-model runner for the frozen retrospective frame.

FROZEN-FRAME: pipeline version eafc32b recorded in the published runs emitted the
two marker keys in a stable insertion order.  Reconstructing that dictionary from
the current payload is byte-identical because FB-01/FB-02 did not change the case,
series, or chronology values.  This knowingly reproduces the marker leak for input
parity.  L-9 says the perturbed arm had the extra marker, but the code at eafc32b is
authoritative: both arms contained the perturb-marker key, with value ``None``.

The saved result is the unmodified v1 FULL_OUTPUT_SCHEMA envelope; cross-model,
frame, audit, retry, and dry-run hash facts live in a per-case sidecar because the
top-level schema rejects extra properties and makes fingerprint optional.
In this arm, fingerprint ``system_prompt_sha256`` is the full-prompt hash, identical
to the sidecar ``prompt_sha256``, because the fingerprint schema is closed.

Isolation is weaker than the Claude arm: Codex has no replacement-system-prompt or
disable-tools equivalent, and a read-only sandbox can still read the disk (including
scoring/).  Mitigations are an empty temporary cwd outside the repository, ignored
user configuration/rules, disabled instruction loading and MCP configuration, a
prompt containing only task/schema-output instructions plus payload, and a retained
JSON event audit log.  On parse/schema failure one retry uses identical input and no
schema coaching; this is an asymmetry because the Claude arm received no error
feedback, and the retry count is recorded in the sidecar.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema

import build_payload
import cli_client
import runner
from cli_client import EVALUATEE_FORBIDDEN_MARKERS

REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_OUT_ROOT = REPO_ROOT / "runs" / "crossmodel_gpt"
METERED_ENV_VARS = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY",
                    "GOOGLE_API_KEY")
MODEL_FALLBACK = "model_string_unavailable"


def frozen_frame_payload(payload: dict) -> str:
    frozen = {
        "variant": payload["_variant"],
        "perturb_factor_recorded_scoring_side_only": None,
        **{key: payload[key] for key in (
            "case", "financial_series_point_in_time", "filing_chronology")},
    }
    return json.dumps(frozen, ensure_ascii=False)


def enforce_no_metered_credentials() -> None:
    present = [name for name in METERED_ENV_VARS if name in os.environ]
    if present:
        raise RuntimeError(f"metered API credential environment variable present: {present}")


def resolve_output_dir(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    resolved = path.resolve()
    try:
        resolved.relative_to(ALLOWED_OUT_ROOT.resolve())
    except ValueError as exc:
        raise ValueError("--out must be under runs/crossmodel_gpt/") from exc
    return resolved


def build_task(case: dict, payload: dict, frame: str) -> str:
    cik_part = f", CIK {case['cik']}" if frame == "original" else ""
    return runner.TASK.format(
        company_name=payload["case"]["company_name"],
        ticker=payload["case"]["ticker"], cik_part=cik_part,
        cutoff_date=case["cutoff_date"])


def build_prompt(task: str, user_payload: str) -> str:
    return (task + "\n\nOutput ONLY a JSON object conforming to this JSON Schema "
            "(no prose, no Markdown fences):\n" +
            json.dumps(runner.MODEL_SCHEMA, ensure_ascii=False) +
            "\n\n" + user_payload)


def codex_command(temp_dir: Path) -> list[str]:
    # Verified offline against `codex exec --help` from codex-cli 0.144.6:
    # read-only constrains tools; --cd selects the empty isolated cwd;
    # --skip-git-repo-check permits that cwd; --ephemeral avoids session state;
    # --ignore-user-config excludes config.toml and --ignore-rules excludes rules;
    # the two -c overrides disable MCP servers and AGENTS.md loading; --json
    # retains the audit event stream; and `-` reads the prompt from stdin.
    return [
        "codex", "exec", "--sandbox", "read-only", "--cd", str(temp_dir),
        "--skip-git-repo-check", "--ephemeral", "--ignore-user-config",
        "--ignore-rules", "--config", "mcp_servers={}", "--config",
        "project_doc_max_bytes=0", "--json", "-",
    ]


def _event_value(value, key: str):
    if isinstance(value, dict):
        if isinstance(value.get(key), str) and value[key]:
            return value[key]
        for child in value.values():
            found = _event_value(child, key)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _event_value(child, key)
            if found:
                return found
    return None


def parse_event_stream(stream: str) -> tuple[str | None, str]:
    answer = None
    model = MODEL_FALLBACK
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        reported = _event_value(event, "model")
        if reported:
            model = reported
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            answer = item.get("text") or item.get("content")
    return answer if isinstance(answer, str) else None, model


def _valid_model_output(text: str | None) -> tuple[dict | None, str | None]:
    if not text:
        return None, "empty_response"
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None, "invalid_json"
    errors = list(jsonschema.Draft7Validator(
        runner.MODEL_SCHEMA, format_checker=jsonschema.FormatChecker()).iter_errors(value))
    return (None, "model_schema_validation") if errors else (value, None)


def _documents(payload: dict) -> list[dict]:
    accessions = {}
    for values in payload["financial_series_point_in_time"].values():
        for value in values:
            if value.get("accession"):
                accessions[value["accession"]] = {
                    "accession_no": value["accession"],
                    "form_type": value.get("form") or "unknown",
                    "filing_date": value["filed"],
                }
    return sorted(accessions.values(), key=lambda item: item["accession_no"])


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_case(case: dict, frame: str, out_dir: Path, *, dry_run: bool = False) -> dict:
    out_dir = resolve_output_dir(out_dir)
    cid = case["case_id"]
    out_path = out_dir / f"{cid}.json"
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = None
        if existing is not None and not list(jsonschema.Draft7Validator(
                runner.FULL_OUTPUT_SCHEMA,
                format_checker=jsonschema.FormatChecker()).iter_errors(existing)):
            return {"case_id": cid, "status": "skip"}

    payload = build_payload.build_payload(case, perturb=frame == "perturbed")
    user_payload = frozen_frame_payload(payload)
    task = build_task(case, payload, frame)
    prompt = build_prompt(task, user_payload)
    payload_sha, prompt_sha = _sha(user_payload), _sha(prompt)
    cli_client.guard_payload(user_payload, EVALUATEE_FORBIDDEN_MARKERS)
    if dry_run:
        print(f"{cid} payload_sha256={payload_sha} prompt_sha256={prompt_sha}")
        return {"case_id": cid, "status": "dry-run"}

    out_dir.mkdir(parents=True, exist_ok=True)
    audit_path = out_dir / f"audit_{frame}_{cid}.jsonl"
    meta_path = out_dir / f"runmeta_{frame}_{cid}.json"
    streams = []
    structured = None
    failure = None
    model = MODEL_FALLBACK
    attempts = 0
    ok = False
    with tempfile.TemporaryDirectory(prefix="crossmodel-gpt-") as temp_name:
        temp_dir = Path(temp_name).resolve()
        if temp_dir == REPO_ROOT.resolve() or REPO_ROOT.resolve() in temp_dir.parents:
            raise RuntimeError("Codex temporary cwd must be outside the repository")
        command = codex_command(temp_dir)
        for attempts in (1, 2):
            cli_client.guard_payload(user_payload, EVALUATEE_FORBIDDEN_MARKERS)
            completed = subprocess.run(command, input=prompt, capture_output=True,
                                       text=True, check=False)
            streams.append(completed.stdout)
            answer, reported_model = parse_event_stream(completed.stdout)
            if reported_model != MODEL_FALLBACK:
                model = reported_model
            structured, failure = _valid_model_output(answer)
            if completed.returncode == 0 and structured is not None:
                ok = True
                break
            if completed.returncode != 0:
                failure = f"codex_exit_{completed.returncode}"
    audit_path.write_text("".join(streams), encoding="utf-8")

    meta = {
        "case_id": cid, "crossmodel": "gpt_subscription_codex",
        "frame": "frozen_v1_markers", "requested_frame": frame,
        "audit_log": audit_path.name, "retry_count": attempts - 1,
        "retry_asymmetry": "one identical-input retry; no schema coaching",
        "payload_sha256": payload_sha, "prompt_sha256": prompt_sha,
        "fail_reason": failure,
    }
    if not ok:
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"case_id": cid, "status": f"FAIL ({failure})"}

    try:
        version = subprocess.run(["codex", "--version"], capture_output=True, text=True,
                                 check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        version = "harness_version_unavailable"
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    schema_sha = hashlib.sha256((REPO_ROOT / "schemas" / "llm_output.json").read_bytes()).hexdigest()
    case_sha = _sha(json.dumps(case, sort_keys=True, ensure_ascii=False))
    fingerprint = {
        "case_input_sha256": case_sha, "payload_sha256": payload_sha,
        "system_prompt_sha256": prompt_sha, "schema_sha256": schema_sha,
        "model_requested": model, "harness_version_actual": version,
        "pipeline_commit": head,
    }
    full = {
        "case_id": cid, "run_id": f"xgpt-{frame}-{cid}-r1", "model": model,
        "pipeline_version": head,
        "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "documents_used": _documents(payload), "fingerprint": fingerprint,
        **structured,
    }
    errors = list(jsonschema.Draft7Validator(
        runner.FULL_OUTPUT_SCHEMA,
        format_checker=jsonschema.FormatChecker()).iter_errors(full))
    if errors:
        meta["fail_reason"] = "full_output_schema_validation"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"case_id": cid, "status": "FAIL (full_output_schema_validation)"}
    out_path.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    meta["fail_reason"] = None
    meta["model"] = model
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"case_id": cid, "status": "OK"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(build_payload.EVALUATEE_CASES))
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--frame", choices=("original", "perturbed"), default="original")
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    enforce_no_metered_credentials()
    out_dir = resolve_output_dir(args.out)
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    if args.only:
        selected = set(args.only)
        cases = [case for case in cases if case["case_id"] in selected]
    if args.limit is not None:
        if args.limit < 0:
            parser.error("--limit must be non-negative")
        cases = cases[:args.limit]
    failures = 0
    for case in cases:
        result = run_case(case, args.frame, out_dir, dry_run=args.dry_run)
        print(f"{result['case_id']}: {result['status']}")
        failures += result["status"].startswith("FAIL")
    return 2 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
