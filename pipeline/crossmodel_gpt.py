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
import re
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
# R6-4: cli_client의 잠긴 가족(벤더 키 + Claude 재라우팅) 재사용 + codex 쪽
# 재라우팅 변수 — OPENAI_BASE_URL/API_BASE는 구독 codex 호출을 종량/미검증
# 백엔드로 조용히 돌린다 (R2-28의 codex 판형). 정합은 교차 대조 테스트가 잠근다.
METERED_ENV_VARS = tuple(cli_client.METERED_CREDENTIAL_VARS) + (
    "OPENAI_BASE_URL", "OPENAI_API_BASE")
MODEL_FALLBACK = "model_string_unavailable"
PIN_PLACEHOLDER = "OWNER-SET-BEFORE-LAUNCH"
CODEX_MODEL_PIN = PIN_PLACEHOLDER
CODEX_VERSION_PIN = "codex-cli 0.144.6"
_verified_harness_version: str | None = None


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
        "project_doc_max_bytes=0", "-c", f"model={CODEX_MODEL_PIN}", "--json", "-",
    ]


def _pins_are_concrete() -> None:
    if not CODEX_MODEL_PIN or CODEX_MODEL_PIN == PIN_PLACEHOLDER:
        raise RuntimeError("Codex model pin must be owner-set before launch")
    if not CODEX_VERSION_PIN or CODEX_VERSION_PIN == PIN_PLACEHOLDER:
        raise RuntimeError("Codex version pin must be owner-set before launch")


def enforce_harness_pin() -> str:
    global _verified_harness_version
    if _verified_harness_version == CODEX_VERSION_PIN:
        return _verified_harness_version
    try:
        actual = subprocess.run(["codex", "--version"], capture_output=True, text=True,
                                check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError("Codex version check failed") from exc
    if actual != CODEX_VERSION_PIN:
        raise RuntimeError(f"Codex version mismatch: expected {CODEX_VERSION_PIN}, got {actual}")
    _verified_harness_version = actual
    return actual


def _pin_matches(reported: str, pin: str) -> bool:
    # 날짜형 접미사만 인정 — gpt-5가 gpt-5-codex를 수용하는 류의 임의 하이픈
    # 확장은 다른 모델이므로 불일치 (INV-21 fail-closed, cli_client 거울)
    return bool(re.fullmatch(re.escape(pin) + r"(-\d{8})?", reported))


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
    _pins_are_concrete()
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
            # R2-4: 파일명은 case_id만 담는다 — 다른 frame의 기존 기록을
            # 멱등 skip하면 "perturbed" arm 데이터가 조용히 original arm이
            # 된다. run_id 접두사로 frame 일치를 강제, 불일치는 FAIL.
            if not str(existing.get("run_id", "")).startswith(f"xgpt-{frame}-"):
                return {"case_id": cid, "status": "FAIL (frame_collision: "
                        f"existing run_id={existing.get('run_id')!r} vs frame={frame!r})"}
            return {"case_id": cid, "status": "skip"}

    payload = build_payload.build_payload(case, perturb=frame == "perturbed")
    user_payload = frozen_frame_payload(payload)
    task = build_task(case, payload, frame)
    prompt = build_prompt(task, user_payload)
    payload_sha, prompt_sha = _sha(user_payload), _sha(prompt)
    # 송출 경계 전체 스캔: prompt = task + 모델 스키마 + user_payload (INV-09)
    cli_client.guard_payload(prompt, EVALUATEE_FORBIDDEN_MARKERS)
    if dry_run:
        print(f"{cid} payload_sha256={payload_sha} prompt_sha256={prompt_sha}")
        return {"case_id": cid, "status": "dry-run"}

    version = enforce_harness_pin()
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
            cli_client.guard_payload(prompt, EVALUATEE_FORBIDDEN_MARKERS)
            completed = subprocess.run(command, input=prompt, capture_output=True,
                                       text=True, check=False)
            streams.append(completed.stdout)
            answer, reported_model = parse_event_stream(completed.stdout)
            structured, failure = _valid_model_output(answer)
            if reported_model == MODEL_FALLBACK or not _pin_matches(
                    reported_model, CODEX_MODEL_PIN):
                structured, failure = None, "model_pin_mismatch"
            else:
                model = reported_model
            if completed.returncode == 0 and structured is not None:
                ok = True
                break
            if completed.returncode != 0:
                failure = f"codex_exit_{completed.returncode}"
    # R5-5(a): 시도 간 경계를 개행으로 접합 — ""-join은 시도 1의 말미
    # 절단 행과 시도 2의 첫 이벤트를 한 비JSON 행으로 융합해, 깨끗한
    # 재시도 스트림이 audit 게이트(verify_codex_audit)에서 오탐 실패한다
    audit_path.write_text("\n".join(streams), encoding="utf-8")

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
    # 원자적 기록 (D67, R3-6): tmp→replace — 부분 기록의 정본 오염 방지
    tmp_path = out_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(out_path)
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
