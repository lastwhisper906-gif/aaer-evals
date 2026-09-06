"""오염 프로브 러너 (freeze 개정 #2 — 구독 헤드리스 경로) — scoring/probes.md 설계의 실행부.

  python pipeline/probe_runner.py --recognition --cases <교란 대상 케이스 파일>
  python pipeline/probe_runner.py --verbatim   --cases <원본 케이스 파일>

출력: scoring/probe_results/{recognition,verbatim}/{case_id}.json + logs/run_<ts>/.
판정(일치 여부)은 채점 쪽 스크립트가 수행 — 이 러너는 모델 응답 수집만.
헤더 의무: these controls BOUND memorization risk; they do not eliminate it.
멱등: 출력 존재+스키마 통과 = skip. 레이트 리밋 = 재개 명령 출력 후 중단.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import shlex
import sys
from pathlib import Path

import build_payload as bp
import cli_client
from runner import CANARY_MARKERS, EVALUATEE_MODEL

REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_VISIBLE_KEYS = ("case", "financial_series_point_in_time", "filing_chronology")
# R2-29: 동결 프로브 트리 — 이 아래 '신규' 케이스 파일 생성은 probe_case가
# 거부한다 (기존 파일의 R1-14 멱등 skip·fp 사이드카는 종전대로).
FROZEN_PROBE_ROOTS = (REPO_ROOT / "scoring" / "probe_results",
                      REPO_ROOT / "scoring" / "probe_results_wave2")

RECOG_SCHEMA = {"type": "object", "additionalProperties": False,
                "required": ["company_guess", "confidence"],
                "properties": {"company_guess": {"type": "string"},
                               "confidence": {"type": "string", "enum": ["high", "medium", "low"]}}}
RECOG_TASK = ("Based on the structured filing data above, which specific company is this? "
              "Answer with the company's real name, or 'unknown'.")

VERBATIM_SCHEMA = {"type": "object", "additionalProperties": False,
                   "required": ["revenue", "net_income", "filing_date", "known"],
                   "properties": {"revenue": {"type": ["number", "null"]},
                                  "net_income": {"type": ["number", "null"]},
                                  "filing_date": {"type": ["string", "null"]},
                                  "known": {"type": "boolean"}}}
VERBATIM_TASK = ("Without any documents: state {company_name}'s exact reported total revenue "
                 "and net income (USD) for the fiscal year ending immediately before "
                 "{cutoff_date}, and the filing date of that annual report. "
                 "If you do not know, set known=false and use nulls.")


def _probe_fingerprint(kind: str, variant_tag: str, system: str, user: str,
                       schema: dict) -> dict:
    """R1-14: 프로브 호출의 구성 정체 — 스키마 유효성만으로는 stale-but-valid
    출력이 바뀐 구성을 조용히 충족한다 (runner.compute_fingerprint 판형)."""
    return {
        "kind": kind, "variant_tag": variant_tag, "model": EVALUATEE_MODEL,
        "system_prompt_sha256": hashlib.sha256(system.encode("utf-8")).hexdigest(),
        "payload_sha256": hashlib.sha256(user.encode("utf-8")).hexdigest(),
        "schema_sha256": hashlib.sha256(
            json.dumps(schema, sort_keys=True).encode("utf-8")).hexdigest(),
    }


def probe_case(kind: str, case: dict, out: Path, log_dir: Path,
               v2_dateshift: bool = False, *,
               accept_legacy_probe: bool = False) -> dict:
    cid = case["case_id"]
    variant_tag = "_v2ds" if v2_dateshift else ""
    out_path = out / f"{cid}{variant_tag}.json"
    schema = RECOG_SCHEMA if kind == "recognition" else VERBATIM_SCHEMA

    if kind == "recognition":
        payload = bp.build_payload(case, perturb=True)
        if v2_dateshift:
            # Q-F05 (specs/perturb_v2.md §3): 컷오프 가드는 상류 진짜 날짜에서
            # 이미 완료 — 렌더 직전 균일 이동 + accession 마스킹만 적용
            import date_shift
            payload = date_shift.shift_payload(payload)
        user_payload = {key: payload[key] for key in MODEL_VISIBLE_KEYS}
        system, user = RECOG_TASK, json.dumps(user_payload, ensure_ascii=False)
        markers = cli_client.EVALUATEE_FORBIDDEN_MARKERS
    else:
        system = VERBATIM_TASK.format(company_name=case["company_name"],
                                      cutoff_date=case["cutoff_date"])
        user = "Answer now."
        markers = cli_client.EVALUATEE_FORBIDDEN_MARKERS

    # R1-14: 멱등 skip은 스키마 유효성 + 구성 fingerprint 일치여야 한다.
    # 동결 프로브 트리 보호(I3): 구성 불일치는 덮어쓰지 않고 FAIL — 새
    # --out-root로 실행하라. fingerprint는 사이드카(fp_*.json — case_* 글롭과
    # 충돌하지 않는 이름)에 둔다: 동결 출력 파일 무접촉.
    fingerprint = _probe_fingerprint(kind, variant_tag, system, user, schema)
    fp_path = out / f"fp_{cid}{variant_tag}.json"
    if cli_client.output_is_valid(out_path, schema):
        if fp_path.exists():
            try:
                recorded = json.loads(fp_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                recorded = None
            if recorded == fingerprint:
                return {"case_id": cid, "status": "skip (멱등 — fingerprint 일치)"}
            return {"case_id": cid, "status":
                    "FAIL (config_changed — 기존 출력은 다른 구성의 산출; 동결 "
                    "경로 보호를 위해 덮어쓰지 않음. 새 --out-root로 실행)"}
        if accept_legacy_probe:
            return {"case_id": cid, "status":
                    "skip (legacy probe ACCEPTED via --accept-legacy-probe — "
                    "fingerprint 사이드카 없음)"}
        return {"case_id": cid, "status":
                "FAIL (stale_legacy_probe — fingerprint 사이드카 없음; "
                "--accept-legacy-probe로 명시 수용)"}

    # R2-29: 기본 --out-root가 동결 트리 그 자체다 — 동결 루트 아래 '신규'
    # 케이스 파일 생성은 거부한다 (호출 전, 쓰기 전). 기존 파일의 멱등 skip
    # (R1-14)은 위에서 이미 처리됐다; 신규 산출은 비동결 --out-root 전용.
    resolved_out = out.resolve()
    frozen = [p.resolve() for p in FROZEN_PROBE_ROOTS]
    if any(p == resolved_out or p in resolved_out.parents for p in frozen) \
            and not out_path.exists():
        return {"case_id": cid, "status":
                "FAIL (frozen_root_new_file — 동결 프로브 트리에 신규 케이스 "
                "파일 생성 금지; 비동결 --out-root로 실행)"}

    r = cli_client.call_model(EVALUATEE_MODEL, system, user, schema,
                              log_dir=log_dir,
                              log_name=f"probe_{kind}{variant_tag}_{cid}",
                              forbid_markers=markers)
    if not r.ok:
        return {"case_id": cid, "status": f"FAIL ({r.fail_reason})"}
    # R6-5 (R2-13 판형): 카나리 GUID 출력은 append-only 트리에 싣지 않는다
    if any(m in json.dumps(r.structured or {}).lower() for m in CANARY_MARKERS):
        return {"case_id": cid, "status": "FAIL (canary_hit)"}
    out.mkdir(parents=True, exist_ok=True)
    # 원자적 기록 (D67, R1-12): tmp→replace — 부분 기록이 정본을 오염 금지
    tmp_path = out_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(r.structured, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    tmp_path.replace(out_path)
    # R1-14: 구성 fingerprint 사이드카 (출력 파일 스키마 무접촉)
    fp_tmp = fp_path.with_suffix(".json.tmp")
    fp_tmp.write_text(json.dumps(fingerprint, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    fp_tmp.replace(fp_path)
    if kind == "recognition":
        return {"case_id": cid, "status": f"OK guess={r.structured['company_guess']!r} "
                f"({r.structured['confidence']})"}
    return {"case_id": cid, "status": f"OK known={r.structured['known']} "
            f"rev={r.structured['revenue']}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--recognition", action="store_true")
    ap.add_argument("--verbatim", action="store_true")
    ap.add_argument("--cases", default=str(bp.EVALUATEE_CASES))
    ap.add_argument("--concurrency", type=int, default=3,
                    help="RP-09 3d: 대조군 16-24건 확장 대비 — runner.py와 동일 패턴")
    ap.add_argument("--out-root", default=str(REPO_ROOT / "scoring" / "probe_results"),
                    help="RP-09 3b: v2 대조군 프로브는 별도 루트 (I3 — 기존 "
                         "probe_results 동결 경로에 추가 기입 금지)")
    ap.add_argument("--v2-dateshift", action="store_true",
                    help="Q-F05: 렌더 직전 date_shift.shift_payload 적용 "
                         "(specs/perturb_v2.md §3/§5 — recognition 전용)")
    ap.add_argument("--accept-legacy-probe", action="store_true",
                    help="R1-14: fingerprint 사이드카 없는 동결 프로브 출력의 "
                         "멱등 skip 명시 수용 (기본은 FAIL)")
    args = ap.parse_args()
    if args.verbatim and args.v2_dateshift:
        # R1-15: v2-dateshift는 recognition 전용(help 문구 그대로) — 조합 시
        # 무이동 verbatim 출력이 _v2ds 파일명으로 오표기 기록되던 침묵 결함.
        ap.error("--verbatim은 --v2-dateshift와 함께 쓸 수 없다 "
                 "(v2-dateshift는 recognition 전용 — specs/perturb_v2.md §3)")

    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    out_root = Path(args.out_root)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO_ROOT / "logs" / f"run_{ts}"
    resume_cmd = "python pipeline/probe_runner.py " + " ".join(
        shlex.quote(a) for a in sys.argv[1:])

    kinds = [k for k, on in (("recognition", args.recognition),
                             ("verbatim", args.verbatim)) if on]
    failures = 0
    for kind in kinds:
        out = out_root / kind
        # RP-09 3d: 병렬화 (runner.py와 동일 ThreadPool 패턴 — 호출 격리는
        # cli_client가 호출 단위로 보장, 케이스 간 상태 공유 없음)
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=args.concurrency) as pool:
            futs = {pool.submit(probe_case, kind, case, out, log_dir,
                                args.v2_dateshift,
                                accept_legacy_probe=args.accept_legacy_probe): case
                    for case in cases}
            try:
                for fut in concurrent.futures.as_completed(futs):
                    res = fut.result()
                    if res["status"].startswith("FAIL"):
                        failures += 1
                    print(f"[{kind}] {res['case_id']}: {res['status']}", flush=True)
            except cli_client.RateLimitedError as e:
                # R2-11 (runner.py 거울): with-블록 밖에서 잡으면 __exit__가
                # 대기 futures를 전부 소진 — 이미 리밋 걸린 구독에 ~수십 호출
                # 추가 발사. 큐 취소 후 HALT.
                pool.shutdown(cancel_futures=True)
                print(f"\nHALT — {e}", file=sys.stderr)
                print(f"재개 명령 (완료분 자동 skip):\n  {resume_cmd}")
                return 3
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
