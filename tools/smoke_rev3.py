"""smoke_rev3.py — freeze 개정 #3 동치성 스모크 테스트 러너 (FREEZE_REV3 §3·§6-3).

래치 조건 3의 실행 가능 형태: 소유자 행동 전체 = `export ANTHROPIC_API_KEY=… &&
make smoke` (실행 절차는 docs/RESUME.md 스모크 절). E2 본 발사는 본 스모크 결과
커밋 전 금지 (§6-3).

설계 (동결 스펙 §3 그대로 — 게이트가 아니라 측정):
  대상: pilot 2케이스 (case_90 VRX·case_91 GE — 본채점 비병합, pilot/ 경로)
  arm A `harness`      : `claude -p` 구독 경로 k=5 (temperature 제어 불능 — 현행 조건)
  arm B `api_unpinned` : raw API k=5, temperature 명시적 미핀(None) — §3-2 "현행과
                         동일 조건" 문면 그대로
  arm C `api_temp0`    : raw API k=5, temperature=0.0 — §3-4 L-3 비결정론 실측 상한
  = 2케이스 × 5draw × 3arm = 30호출 (§3-5 산술과 동일)
판독 (사전 고정): |median(B) − median(A)| > 2×σ(3.2pp) = 6.4pp 이면 발행물 L-2
문단 병기 대상으로 플래그. temp0 arm의 draw 범위 = L-3 상한 문서화. FAIL은
게이트 아님 — 전부 기록.

모드:
  --dry-run (기본): 첫 호출 직전에 멈추고 계획 호출 매니페스트 전량을
                    runs/smoke_rev3/DRYRUN_MANIFEST.json 에 기록·출력 (결정론,
                    네트워크·데이터 접근 0 — 커밋 대상).
  --live          : 매니페스트 순서대로 실행 (멱등 — 유효 출력 존재 시 skip).
                    arm A 동안 ANTHROPIC_API_KEY를 환경에서 임시 제거(INVARIANT 4:
                    구독 경로는 키 부재 assert), arm B/C에서 복원.
  --analyze       : 기존 출력만으로 SMOKE_REPORT.md 재생성 (무호출).

runs/ 밑에 파일을 추가하므로 결과 커밋 전 `python tools/verify_blindness.py
--write-manifest` 필수 (전역 MANIFEST 규약).
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))

OUT_DIR = REPO / "runs" / "smoke_rev3"
MANIFEST_PATH = OUT_DIR / "DRYRUN_MANIFEST.json"
PILOT_CASES = REPO / "pilot" / "cases_pilot.json"
EVALUATEE_MODEL = "claude-sonnet-5"   # runner.EVALUATEE_MODEL과 동일 핀 (D6)
K_DRAWS = 5
SIGMA_PP = 3.2                        # E3 실측 per-case σ (FREEZE_REV3 §3-3)
ARMS = [
    {"arm": "harness", "path": "subscription-cli", "temperature": None,
     "temperature_note": "제어 불능 — 하네스 경로 현행 조건 (L-3)"},
    {"arm": "api_unpinned", "path": "raw-api", "temperature": None,
     "temperature_note": "명시적 미핀 — §3-2 '현행과 동일 조건' 문면"},
    {"arm": "api_temp0", "path": "raw-api", "temperature": 0.0,
     "temperature_note": "0.0 고정 — §3-4 L-3 비결정론 실측 상한"},
]


def build_manifest() -> dict:
    """계획 호출 매니페스트 — 순수 함수 (데이터·네트워크 접근 0, 결정론)."""
    cases = json.loads(PILOT_CASES.read_text(encoding="utf-8"))["cases"]
    calls, seq = [], 0
    for arm in ARMS:
        for case in cases:
            for draw in range(1, K_DRAWS + 1):
                seq += 1
                calls.append({
                    "seq": seq, "arm": arm["arm"], "call_path": arm["path"],
                    "case_id": case["case_id"], "ticker": case["ticker"],
                    "cutoff_date": case["cutoff_date"],
                    "draw": draw, "model": EVALUATEE_MODEL,
                    "temperature": arm["temperature"],
                    "payload_variant": "original (perturb=False)",
                    "output_file": f"runs/smoke_rev3/{arm['arm']}/{case['case_id']}_d{draw}.json",
                })
    return {
        "spec": "docs/FREEZE_REV3_DRAFT.md §3 (설계) · §6-3 (래치 조건)",
        "purpose": "동치성 측정 — 게이트 아님 (§3-3)",
        "reading_rule": f"|median(api_unpinned) − median(harness)| > 2×σ({SIGMA_PP}pp) "
                        f"= {2 * SIGMA_PP}pp → 발행물 L-2 문단 병기 대상",
        "model_pin": EVALUATEE_MODEL, "k_draws": K_DRAWS,
        "n_calls_total": len(calls),
        "n_calls_by_arm": {a["arm"]: sum(1 for c in calls if c["arm"] == a["arm"])
                           for a in ARMS},
        "arms": ARMS,
        "sample_list": [c["case_id"] for c in cases],
        "e2_gate": "본 스모크 결과 커밋 전 E2 본 발사 금지 (§6-3)",
        "calls": calls,
    }


def cmd_dry_run() -> int:
    manifest = build_manifest()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "calls"},
                     ensure_ascii=False, indent=1))
    for c in manifest["calls"]:
        print(f"  {c['seq']:2d}. [{c['arm']:12s}] {c['case_id']} draw {c['draw']} "
              f"temp={c['temperature']} -> {c['output_file']}")
    print(f"\nDRY-RUN: 첫 호출 직전 정지 — 계획 {manifest['n_calls_total']}호출, "
          f"매니페스트 {MANIFEST_PATH.relative_to(REPO)}")
    return 0


# ── live 실행 (여기부터는 소유자 래치 뒤에서만 도달) ─────────────────────────

def _run_call(call: dict, case: dict) -> dict:
    """단일 호출 — arm별 클라이언트. 반환: 점수 레코드 (측정 산출물)."""
    import build_payload as bp
    import cli_client
    from runner import MODEL_SCHEMA, TASK

    out_path = REPO / call["output_file"]
    if out_path.exists():
        try:
            rec = json.loads(out_path.read_text(encoding="utf-8"))
            if rec.get("ok"):
                return {"status": "skip (멱등)", **rec}
        except json.JSONDecodeError:
            pass
    payload = bp.build_payload(case, perturb=False)
    payload.pop("_k_internal", None)
    task = TASK.format(company_name=payload["case"]["company_name"],
                       ticker=payload["case"]["ticker"],
                       cik_part=f", CIK {case['cik']}",
                       cutoff_date=case["cutoff_date"])
    user_payload = json.dumps({k: v for k, v in payload.items()
                               if not k.startswith("_")}, ensure_ascii=False)
    log_dir = OUT_DIR / "logs"
    log_name = f"smoke_{call['arm']}_{call['case_id']}_d{call['draw']}"

    if call["arm"] == "harness":
        stash = os.environ.pop("ANTHROPIC_API_KEY", None)  # INVARIANT 4: 구독 경로는 키 부재
        try:
            r = cli_client.call_model(call["model"], task, user_payload, MODEL_SCHEMA,
                                      log_dir=log_dir, log_name=log_name,
                                      forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS)
        finally:
            if stash is not None:
                os.environ["ANTHROPIC_API_KEY"] = stash
    else:
        from api_client import call_model_api
        r = call_model_api(call["model"], task, user_payload, MODEL_SCHEMA,
                           log_dir=log_dir, log_name=log_name,
                           forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS,
                           temperature=call["temperature"])

    rec = {"ok": r.ok, "arm": call["arm"], "case_id": call["case_id"],
           "draw": call["draw"], "temperature": call["temperature"],
           "misstatement_probability": (r.structured or {}).get("misstatement_probability"),
           "fail_reason": r.fail_reason, "served_models": r.served_models,
           "pin_ok": r.pin_ok, "usage": r.usage, "wall_seconds": r.wall_seconds,
           "structured": r.structured}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"status": f"OK p={rec['misstatement_probability']}" if r.ok
            else f"FAIL ({r.fail_reason})", **rec}


def cmd_live() -> int:
    from api_client import assert_raw_api_approved
    assert_raw_api_approved()  # 래치: AAER_RAW_API_APPROVED=1 + ANTHROPIC_API_KEY
    if not MANIFEST_PATH.exists():
        print("DRYRUN_MANIFEST.json 부재 — 먼저 --dry-run을 실행·커밋하라 (§6-3 순서)",
              file=sys.stderr)
        return 2
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    regenerated = build_manifest()
    if manifest["calls"] != regenerated["calls"]:
        print("커밋된 매니페스트 ≠ 재생성 매니페스트 — 스펙/케이스 변경 후 매니페스트 "
              "미갱신 (fail-closed)", file=sys.stderr)
        return 2
    cases = {c["case_id"]: c for c in
             json.loads(PILOT_CASES.read_text(encoding="utf-8"))["cases"]}
    failures = 0
    for call in manifest["calls"]:
        res = _run_call(call, cases[call["case_id"]])
        print(f"{call['seq']:2d}/{manifest['n_calls_total']} [{call['arm']}] "
              f"{call['case_id']} d{call['draw']}: {res['status']}", flush=True)
        if res["status"].startswith("FAIL"):
            failures += 1
    cmd_analyze()
    print("\n다음: git add runs/smoke_rev3 && python tools/verify_blindness.py "
          "--write-manifest && git add runs/MANIFEST.sha256 && 커밋 — 커밋 후에만 E2 발사 가능")
    return 0 if failures == 0 else 2


def cmd_analyze() -> int:
    rows = []
    for arm in ARMS:
        for p in sorted((OUT_DIR / arm["arm"]).glob("case_*_d*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            rows.append(rec)
    if not rows:
        print("출력 없음 — --live 이후에 실행", file=sys.stderr)
        return 2
    summary: dict = {"per_arm_case": {}, "flags": []}
    for arm in (a["arm"] for a in ARMS):
        for cid in sorted({r["case_id"] for r in rows}):
            ps = [r["misstatement_probability"] for r in rows
                  if r["arm"] == arm and r["case_id"] == cid and r["ok"]]
            if ps:
                summary["per_arm_case"][f"{arm}/{cid}"] = {
                    "n_ok": len(ps), "median": statistics.median(ps),
                    "min": min(ps), "max": max(ps), "range": max(ps) - min(ps)}
    for cid in sorted({r["case_id"] for r in rows}):
        h = summary["per_arm_case"].get(f"harness/{cid}")
        b = summary["per_arm_case"].get(f"api_unpinned/{cid}")
        if h and b:
            dev = abs(b["median"] - h["median"])
            if dev > 2 * SIGMA_PP:
                summary["flags"].append(
                    f"{cid}: |median(api)−median(harness)| = {dev}pp > {2*SIGMA_PP}pp "
                    "— 발행물 L-2 문단 병기 대상 (사전 고정 판독)")
    summary["n_fail"] = sum(1 for r in rows if not r["ok"])
    summary["pin_mismatch"] = sum(1 for r in rows if r["ok"] and not r.get("pin_ok"))
    (OUT_DIR / "smoke_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = ["# SMOKE_REPORT — freeze 개정 #3 동치성 측정 (게이트 아님, §3-3)", "",
          "| arm/case | n_ok | median | min–max | range |", "|---|---|---|---|---|"]
    for key, s in summary["per_arm_case"].items():
        md.append(f"| {key} | {s['n_ok']} | {s['median']} | {s['min']}–{s['max']} | {s['range']} |")
    md += ["", f"- FAIL {summary['n_fail']}건 · pin 불일치 {summary['pin_mismatch']}건",
           "- 판독 플래그: " + ("; ".join(summary["flags"]) if summary["flags"]
                                else f"없음 (전 케이스 편차 ≤ {2*SIGMA_PP}pp)"),
           "- temp0 arm의 range = L-3 비결정론 실측 상한 (FREEZE_REV3 §3-4).", ""]
    (OUT_DIR / "SMOKE_REPORT.md").write_text("\n".join(md), encoding="utf-8")
    print(f"분석 갱신: {OUT_DIR / 'SMOKE_REPORT.md'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--analyze", action="store_true")
    args = ap.parse_args()
    if args.live:
        return cmd_live()
    if args.analyze:
        return cmd_analyze()
    return cmd_dry_run()


if __name__ == "__main__":
    sys.exit(main())
