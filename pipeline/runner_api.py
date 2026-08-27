"""피평가자 러너 — raw API 병렬 변형 (freeze 개정 #3 스캐폴드, D38 — 미배선).

동결 `runner.py`와의 차이는 호출 클라이언트뿐 (api_client.call_model_api).
TASK·MODEL_SCHEMA·build_payload·출력 형식·멱등 skip 전부 동결 모듈 import.
실행은 개정 #3 발효 후에만 (api_client의 이중 안전장치가 차단).

의도된 계약 차이 (R2-3에서 문서화): fingerprint 필드는 이 arm에 없다 —
멱등 skip은 output_is_valid(스키마 유효성)만으로 판정하며, fp-sibling
재실행 의미론은 동치성 테스트 규모(소수 케이스·수동 감독)에 불필요.
composed 기록의 FULL_OUTPUT_SCHEMA 재검증·카나리 runmeta 기록은
runner.run_case와 동일하게 수행한다.

사용 (발효 후):
  AAER_RAW_API_APPROVED=1 python pipeline/runner_api.py --cases <cases.json> --out <dir> \
      [--perturbed] [--only case_NN ...] [--temperature 0]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import jsonschema

import build_payload as bp
import cli_client
from api_client import assert_raw_api_approved, call_model_api
from cli_client import EVALUATEE_FORBIDDEN_MARKERS, freeze_state
from runner import CANARY_MARKERS, EVALUATEE_MODEL, FULL_OUTPUT_SCHEMA, MODEL_SCHEMA, TASK

REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_VISIBLE_KEYS = ("case", "financial_series_point_in_time", "filing_chronology")


def run_case_api(case: dict, perturb: bool, out_dir: Path, log_dir: Path,
                 temperature: float | None) -> dict:
    cid = case["case_id"]
    out_path = out_dir / f"{cid}.json"
    if cli_client.output_is_valid(out_path, FULL_OUTPUT_SCHEMA):
        return {"case_id": cid, "status": "skip (멱등)"}
    payload = bp.build_payload(case, perturb=perturb)
    k = payload.pop("_k_internal")
    cik_part = f", CIK {case['cik']}" if not perturb else ""
    task = TASK.format(company_name=payload["case"]["company_name"],
                       ticker=payload["case"]["ticker"], cik_part=cik_part,
                       cutoff_date=case["cutoff_date"])
    user_payload = json.dumps({key: payload[key] for key in MODEL_VISIBLE_KEYS},
                              ensure_ascii=False)
    variant = "perturbed" if perturb else "original"
    r = call_model_api(EVALUATEE_MODEL, task, user_payload, MODEL_SCHEMA,
                       log_dir=log_dir, log_name=f"evaluatee_api_{variant}_{cid}",
                       forbid_markers=EVALUATEE_FORBIDDEN_MARKERS,
                       temperature=temperature)

    # runner.run_case 거울 (R2-3): 카나리 검사 + runmeta 증거 기록
    canary_hit = any(m in json.dumps(r.structured or {}).lower() for m in CANARY_MARKERS)
    meta = {"case_id": cid, "variant": f"api-{variant}-{cid}-r1",
            "canary_hit": canary_hit, "fail_reason": r.fail_reason,
            "served_models": r.served_models}
    log_dir.mkdir(parents=True, exist_ok=True)
    meta_path = log_dir / f"runmeta_api_{variant}_{cid}.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    if canary_hit:
        # R2-13 (runner 거울): 카나리 출력은 기록 전 fail-closed
        meta["fail_reason"] = "canary_hit"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        return {"case_id": cid, "status": "FAIL (canary_hit)"}
    if not r.ok:
        return {"case_id": cid, "status": f"FAIL ({r.fail_reason})"}
    accessions = {}
    for tag, vals in payload["financial_series_point_in_time"].items():
        for v in vals:
            if v.get("accession"):
                accessions[v["accession"]] = {"accession_no": v["accession"],
                                              "form_type": v.get("form") or "unknown",
                                              "filing_date": v["filed"]}
    full = {"case_id": cid, "run_id": f"api-{variant}-{cid}-r1",
            "model": (r.served_models or [EVALUATEE_MODEL])[0],
            "pipeline_version": freeze_state()["head"],
            "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "documents_used": sorted(accessions.values(), key=lambda d: d["accession_no"]),
            **r.structured}
    # runner.run_case 거울 (R2-3): composed 기록 재검증 — 위반 시 미기록 FAIL
    # (스키마 무효 기록이 남으면 output_is_valid skip이 영영 실패해 종량 호출 반복)
    errors = list(jsonschema.Draft7Validator(
        FULL_OUTPUT_SCHEMA, format_checker=jsonschema.FormatChecker()).iter_errors(full))
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path) or "<root>"
        reason = f"schema_violation: {path}"
        meta["fail_reason"] = reason
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"case_id": cid, "status": f"FAIL ({reason})"}
    out_dir.mkdir(parents=True, exist_ok=True)
    # 원자적 기록 (D67): 크래시 시 부분 파일이 '완료'로 오인되지 않도록 tmp→replace
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(out_path)
    return {"case_id": cid,
            "status": f"OK p={full['misstatement_probability']} (perturb_k={k if perturb else None})"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--perturbed", action="store_true")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--temperature", type=float, default=None)
    args = ap.parse_args()

    assert_raw_api_approved()      # 소유자 스위치 + 키 (개정 #3 발효 전 즉시 예외)
    cli_client.require_clean_tree()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    if args.only:
        cases = [c for c in cases if c["case_id"] in set(args.only)]
    out_dir = REPO_ROOT / args.out
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO_ROOT / "logs" / f"run_{ts}"
    failures = 0
    try:
        for c in cases:  # 순차 — 동치성 테스트 규모(소수 케이스)에 충분
            res = run_case_api(c, args.perturbed, out_dir, log_dir, args.temperature)
            print(f"{res['case_id']}: {res['status']}", flush=True)
            if res["status"].startswith("FAIL"):
                failures += 1
    except cli_client.RateLimitedError as e:
        print(f"HALT — {e} (재개 = 동일 명령, 멱등)", file=sys.stderr)
        return 3
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
