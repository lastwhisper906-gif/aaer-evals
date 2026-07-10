"""raw Anthropic SDK 병렬 클라이언트 — freeze 개정 #3 스캐폴드 (D38, 미배선).

`cli_client.call_model`과 동일한 CallResult 인터페이스. 하네스(`claude -p`) 대신
순수 SDK 직호출 — system-reminder(userEmail·currentDate) 주입 0 (J13-e 해소 경로,
L-2·W8). **어떤 동결 러너도 이 모듈을 import하지 않는다** — 실행 전환은 freeze
개정 #3 발효(소유자 승인, OWNER_QUEUE Q-R02) 후 다음 실행 배치부터.

이중 안전장치:
  1. AAER_RAW_API_APPROVED=1 (소유자 스위치) 부재 시 즉시 예외 — 우발 실행 차단.
  2. ANTHROPIC_API_KEY 필요 (종량 과금 경로 — INVARIANT 4 개정 필요, 초안 §1).
동결 규약 재사용: 페이로드 가드 · 스키마 검증 + 1회 재시도 · 레이트 리밋 예외 ·
호출별 JSON 로그 (SR 11-7 — 서빙 모델 핀 대조 포함).
"""
from __future__ import annotations

import datetime
import json
import os
import time
from pathlib import Path

import jsonschema

from cli_client import (CallResult, PayloadGuardError, RateLimitedError,  # noqa: F401
                        guard_payload)

REPO_ROOT = Path(__file__).resolve().parent.parent
STRUCTURED_TOOL = "submit_structured_output"
DEFAULT_MAX_TOKENS = 8192


def assert_raw_api_approved() -> None:
    if os.environ.get("AAER_RAW_API_APPROVED") != "1":
        raise RuntimeError(
            "raw API 경로 미승인 — freeze 개정 #3은 초안 상태다 "
            "(docs/FREEZE_REV3_DRAFT.md, OWNER_QUEUE Q-R02). "
            "소유자 승인 후 AAER_RAW_API_APPROVED=1로만 실행.")
    if "ANTHROPIC_API_KEY" not in os.environ:
        raise RuntimeError("ANTHROPIC_API_KEY 부재 — raw API 경로는 종량 키 필요 "
                           "(개정 #3 §1, 소유자 인프라).")


def call_model_api(model: str, system_prompt: str, user_payload: str,
                   schema: dict, log_dir: Path, log_name: str,
                   forbid_markers: list[str] | None = None,
                   temperature: float | None = None,
                   max_tokens: int = DEFAULT_MAX_TOKENS) -> CallResult:
    """cli_client.call_model 동일 계약 — 구조화 출력은 강제 tool-use로 수취."""
    assert_raw_api_approved()
    if forbid_markers:
        guard_payload(user_payload, forbid_markers)  # SDK import 이전 — 가드 항상 선행

    import anthropic  # 지연 import — 스캐폴드 단계에서 패키지 의존 강제하지 않음

    client = anthropic.Anthropic()
    tool = {"name": STRUCTURED_TOOL, "description":
            "Submit the structured analysis result.", "input_schema": schema}
    kwargs = dict(model=model, max_tokens=max_tokens, system=system_prompt,
                  messages=[{"role": "user", "content": user_payload}],
                  tools=[tool], tool_choice={"type": "tool", "name": STRUCTURED_TOOL})
    if temperature is not None:
        kwargs["temperature"] = temperature  # 개정 #3 부수 이득 — L-3 부분 해소

    t0 = time.monotonic()
    structured, fail, served, usage, attempts = None, None, [], None, 0
    for attempts in (1, 2):  # 동결 규약: 스키마 실패·빈 응답 1회 재시도
        try:
            resp = client.messages.create(**kwargs)
        except anthropic.RateLimitError as e:
            raise RateLimitedError(str(e)) from e
        except anthropic.APIStatusError as e:
            if e.status_code == 429 or "overloaded" in str(e).lower():
                raise RateLimitedError(str(e)) from e
            fail = f"error ({e.status_code})"
            continue
        served = [resp.model]
        usage = {"input_tokens": resp.usage.input_tokens,
                 "output_tokens": resp.usage.output_tokens}
        blocks = [b for b in resp.content if b.type == "tool_use"
                  and b.name == STRUCTURED_TOOL]
        if not blocks:
            fail = "empty"
            continue
        try:
            jsonschema.validate(blocks[0].input, schema)
            structured, fail = blocks[0].input, None
            break
        except jsonschema.ValidationError:
            fail = "schema_failure"

    pin_ok = bool(served) and all(m == model or m.startswith(model + "-")
                                  for m in served)
    if structured is not None and not pin_ok:
        structured, fail = None, "pin_mismatch"
    result = CallResult(
        ok=structured is not None, structured=structured, fail_reason=fail,
        served_models=served, pin_ok=pin_ok, session_id=None, usage=usage,
        total_cost_usd=None,  # 종량 과금 — 비용은 Console이 진실원 (개정 #3 §5)
        attempts=attempts, wall_seconds=round(time.monotonic() - t0, 2),
        raw_result_text=None if structured is not None else str(usage))

    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"{log_name}.json").write_text(json.dumps({
        "path": "raw-api (freeze rev3)", "model_requested": model,
        "served_models": served, "pin_ok": pin_ok, "ok": result.ok,
        "fail_reason": fail, "usage": usage, "attempts": attempts,
        "temperature": temperature,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
