"""Q-F05 발사 전 위생 스캔 (사전 등록 전제조건 ii) — 무호출·읽기 전용.

실측 갱신 (2026-07-13, 62케이스 전수): 페이로드당 날짜가 수백 개라 부호
쌍차 집합이 ±546일 내 7의 배수를 사실상 전부 덮는다 — '충돌 케이스만 필드
검증으로 대체'는 이진 분기로는 무의미 (62/62 충돌). 스펙 의도(원본 문자열이
**설명 없이** 생존하지 않음)를 다음의 상위 호환으로 이행한다:

  1. **필드 단위 이동 검증 — 전 케이스** (분기 없이 항상): 전 날짜 필드가
     정확히 원본+offset, accession 전건 마스킹. (스펙의 '대체 검증'의 전면화
     — 이진 분기보다 강함.)
  2. **no-leak 스캔 + 양성 충돌 회계**: v2 렌더에 생존한 원본 날짜 문자열은
     각각 '양성 충돌'(생존 문자열 − offset ∈ 원본 날짜 집합 — 즉 다른 원본
     날짜의 정당한 이동 결과)로 설명되어야 한다. 설명 불가 생존 = FAIL.
     원본 accession 생존은 무조건 FAIL. (364일=52주 양성 충돌 실증 —
     test_date_shift.py::test_collision_property_documented — 의 일반형.)
  3. offset 자체의 스펙 §2 계약 확인: 7의 배수, |offset| ∈ [182, 546].

출력: runs/diagnostics/v2ds_hygiene/HYGIENE_REPORT.json (발사 전 커밋 대상).
어느 케이스든 실패 = exit 2 (발사 금지).

실행: .venv/bin/python tools/v2ds_hygiene_scan.py
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))

import build_payload as bp  # noqa: E402
import date_shift  # noqa: E402

OUT = REPO / "runs" / "diagnostics" / "v2ds_hygiene" / "HYGIENE_REPORT.json"
ROSTER = [  # Q-F05 사전 등록 62케이스 (8 w1-treatment + 22 w1-control + 32 w2)
    ("wave1_treatment", REPO / "scoring" / "perturbed_cases.json"),
    ("wave1_control", REPO / "data" / "evaluatee" / "cases_v2.json"),
    ("wave2", REPO / "data" / "evaluatee" / "cases_wave2.json"),
]


def payload_dates(payload: dict) -> list[str]:
    """피평가자 가시 날짜 문자열 전수 (스펙 §3 열거 필드)."""
    out = [payload["case"]["cutoff_date"]]
    for vals in payload["financial_series_point_in_time"].values():
        for v in vals:
            for k in ("start", "end", "filed"):
                if v.get(k):
                    out.append(str(v[k]))
    for r in payload["filing_chronology"]:
        out.append(str(r["filing_date"]))
    return out


def payload_accessions(payload: dict) -> set[str]:
    accs = set()
    for vals in payload["financial_series_point_in_time"].values():
        for v in vals:
            if v.get("accession"):
                accs.add(v["accession"])
    return accs


def offset_contract_ok(offset: int) -> bool:
    """스펙 §2: 7의 배수, |offset| ∈ [182, 546]."""
    return offset % 7 == 0 and 182 <= abs(offset) <= 546


def field_level_verify(orig: dict, shifted: dict, offset: int) -> list[str]:
    """충돌 케이스 대체 검증 — 필드 단위 이동 정확성 + accession 마스킹."""
    errs = []

    def chk(o, s, where):
        want = str(datetime.date.fromisoformat(str(o)) + datetime.timedelta(days=offset))
        if str(s) != want:
            errs.append(f"{where}: {o} → {s} (기대 {want})")

    chk(orig["case"]["cutoff_date"], shifted["case"]["cutoff_date"], "case.cutoff_date")
    for tag in orig["financial_series_point_in_time"]:
        ov = orig["financial_series_point_in_time"][tag]
        sv = shifted["financial_series_point_in_time"][tag]
        for i, (o, s) in enumerate(zip(ov, sv, strict=True)):
            for k in ("start", "end", "filed"):
                if o.get(k):
                    chk(o[k], s[k], f"{tag}[{i}].{k}")
            if o.get("accession") and not str(s.get("accession", "")).startswith("acc-"):
                errs.append(f"{tag}[{i}].accession 마스킹 실패: {s.get('accession')}")
    for i, (o, s) in enumerate(zip(orig["filing_chronology"],
                                   shifted["filing_chronology"], strict=True)):
        chk(o["filing_date"], s["filing_date"], f"chronology[{i}]")
    return errs


def scan_case(case: dict) -> dict:
    cid = case["case_id"]
    payload = bp.build_payload(case, perturb=True)
    payload.pop("_k_internal", None)
    offset = date_shift.offset_for_case(cid)
    dates = payload_dates(payload)
    date_set = {datetime.date.fromisoformat(d) for d in dates}
    accs = payload_accessions(payload)
    shifted = date_shift.shift_payload(payload)

    errs = [] if offset_contract_ok(offset) else [f"offset 계약 위반: {offset}"]
    errs += field_level_verify(payload, shifted, offset)          # 검증 1 (전 케이스)

    blob = json.dumps(shifted, ensure_ascii=False)                # 검증 2
    benign = 0
    for d in sorted(set(dates)):
        if d in blob:
            src = datetime.date.fromisoformat(d) - datetime.timedelta(days=offset)
            if src in date_set:
                benign += 1                                       # 다른 원본의 정당한 이동
            else:
                errs.append(f"설명 불가 원본 날짜 생존: {d}")
    errs += [f"원본 accession 생존: {a}" for a in sorted(accs) if a in blob]

    return {"case_id": cid, "offset_days": offset, "n_dates": len(dates),
            "n_accessions": len(accs), "benign_collisions": benign,
            "method": "field_level_all + scan_with_benign_accounting",
            "errors": errs, "pass": not errs}


def main() -> int:
    rows, n = [], 0
    for label, path in ROSTER:
        for case in json.loads(path.read_text(encoding="utf-8"))["cases"]:
            r = scan_case(case)
            r["roster"] = label
            rows.append(r)
            n += 1
            print(f"[{label}] {r['case_id']}: offset={r['offset_days']:+d} "
                  f"benign={r['benign_collisions']} "
                  f"{'PASS' if r['pass'] else 'FAIL ' + str(r['errors'][:2])}")
    ok = all(r["pass"] for r in rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "spec": "specs/perturb_v2.md §5 전제 (Q-F05 해소 조건 ii)",
        "n_cases": n,
        "total_benign_collisions": sum(r["benign_collisions"] for r in rows),
        "all_pass": ok, "rows": rows}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print(f"\n{'PASS' if ok else 'FAIL'} — {n}케이스 · 양성 충돌 총 "
          f"{sum(r['benign_collisions'] for r in rows)}건 (필드 검증이 전 케이스 커버) "
          f"→ {OUT.relative_to(REPO)}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
