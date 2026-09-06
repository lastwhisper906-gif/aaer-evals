"""결과 관측의 append-only 기록 (spec §7·§8, D100).

usage: python tools/forward_outcome_append.py --cycle forward/cycle_001 \
    --record-id fw001-r01 --event-date 2027-03-02 --event-public-date 2027-03-02 \
    --event-type item_402_nonreliance --source "<accession/url>" \
    --new-label item_402_nonreliance --reviewer owner --rationale "..."

- outcome_updates.jsonl 끝에 1행 추가만 한다 — 기존 행·scores.json 무접촉.
- previous_label은 직전 업데이트에서 기계 유도 (없으면 none_observed).
- 원 점수·원 라벨 상태는 영구 보존 (spec §0-5).
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import REPO, parse_date, read_json, fail

EVENT_TYPES = {
    "aaer_or_final_enforcement", "item_402_nonreliance", "big_r_restatement",
    "sec_complaint", "doj_action", "other_material_correction",
    "unresolved_event", "none_observed",
}

# R9-2: spec §7 계층 — 성숙 시 상향만 (숫자 낮을수록 상위). none_observed는
# 기저(최하위). 하향 이동은 append-only 원장의 영구 오염이므로 fail-closed.
# 정정 경로(override)는 만들지 않는다 — 필요해지면 소유자 결정 사안 (INV-18);
# 그때까지 하향은 도구 밖에서 불가능해야 한다.
LABEL_RANK = {
    "aaer_or_final_enforcement": 1, "item_402_nonreliance": 2,
    "big_r_restatement": 3, "sec_complaint": 4, "doj_action": 5,
    "other_material_correction": 6, "unresolved_event": 7, "none_observed": 8,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    for f in ("record-id", "event-date", "event-public-date", "event-type",
              "source", "new-label", "reviewer", "rationale"):
        ap.add_argument(f"--{f}", required=True)
    args = ap.parse_args()
    cycle = REPO / args.cycle

    if args.event_type not in EVENT_TYPES or args.new_label not in EVENT_TYPES:
        fail(f"event_type/new_label은 spec §7 계층 라벨 중 하나여야 함: {sorted(EVENT_TYPES)}")
    # R3-10(b)/R4-7(c): append-only 원장에 비ISO 날짜가 들어가면 영구 오염 —
    # parse_date는 앞 10자만 보므로("2027-03-02T00:00" 통과) 전체 문자열 검증
    for flag, value in (("--event-date", args.event_date),
                        ("--event-public-date", args.event_public_date)):
        try:
            if parse_date(value).isoformat() != value:
                raise ValueError(value)
        except ValueError:
            fail(f"{flag} {value!r} — 정확한 ISO 날짜(YYYY-MM-DD 전체 일치)가 아님")
    records = {r["record_id"]: r for r in read_json(cycle / "scores.json")["records"]}
    if args.record_id not in records:
        fail(f"record_id {args.record_id} 이(가) scores.json에 없음")

    log = cycle / "outcome_updates.jsonl"
    prev = "none_observed"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                e = json.loads(line)
                if e["record_id"] == args.record_id:
                    prev = e["new_label"]

    if LABEL_RANK[args.new_label] > LABEL_RANK[prev]:
        fail(f"라벨 하향 금지 (spec §7 — 상향만): {prev} → {args.new_label}. "
             "원 이력은 보존된다; 정정이 필요하면 소유자 결정 사안이다.")

    entry = {
        "record_id": args.record_id,
        "company": records[args.record_id].get("company"),
        "event_date": args.event_date,
        "event_first_public": args.event_public_date,
        "event_type": args.event_type,
        "source": args.source,
        "previous_label": prev,
        "new_label": args.new_label,
        "update_ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "reviewer": args.reviewer,
        "rationale": args.rationale,
    }
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"APPENDED — {args.record_id}: {prev} → {args.new_label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
