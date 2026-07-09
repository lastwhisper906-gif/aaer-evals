"""E1 홀드아웃 대조군 채점 런북 — HOLDOUT_CONTROLS_PLAN §2–§5 이행 (감독 하, Q-E03 RESOLVED).

run_wave2_scoring.py 패턴 verbatim — 동결 파이프라인 재사용 (build_payload / runner /
grader_runner 무수정). I3: 출력은 runs/holdout/controls/ · scoring/grades_holdout_controls/.

단계 (전부 멱등):
  1 build : _rp08 캐시 → ~/aaer-data/{T}/ 스테이지 (D23-safe, 존재 시 보존) +
            cases_holdout_controls.json (중립 ID hc_NN, 케이스 알파벳순 GNE→HUBG→WMK,
            케이스 내 S2 랭크순 — §5 발사순 사전 고정) + id_mapping_holdout_controls
            (mapping: hc→티커, case_of: hc→case_NN) + candidates_holdout_controls.
  2 probe : 케이스별 recognition gate (tools/holdout_probe.py) — knows_event=False만
            admit (§2). True → 탈락, alternates 승격은 소유자 입회 하 수동 재빌드.
  3 score : runner --cases cases_holdout_controls.json --only <해당 케이스 hc들>
  4 grade : grader_runner → scoring/grades_holdout_controls (human_finalized=false)

케이스 경계마다 freeze·commit·push (§5) — 본 스크립트는 단계 실행만, 커밋은 세션이.
identity frame PRIMARY (§3): 대조군도 실명 노출 — 홀드아웃 프라우드와 동일 프레임.

사용: python3 tools/run_holdout_controls_scoring.py {build|probe|score|grade} [--case case_73]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIG = Path.home() / "aaer-data/_rp08"
DATA = Path.home() / "aaer-data"
SEL = REPO / "runs/holdout/controls/control_group_holdout.json"
CASES_DEST = REPO / "data/evaluatee/cases_holdout_controls.json"
MAP_DEST = REPO / "scoring/id_mapping_holdout_controls.json"
CAND_DEST = REPO / "data/candidates/candidates_holdout_controls.json"
RECOG_DIR = "runs/holdout/controls/recognition"
# §5 케이스 발사순 사전 고정: 알파벳 = GNE → HUBG → WMK
CASE_ORDER = ["case_73", "case_71", "case_72"]


def rows():
    sel = json.loads(SEL.read_text(encoding="utf-8"))["selections"]
    out, n = [], 0
    for cid in CASE_ORDER:
        for s in sel[cid]["selected"]:  # S2 랭크순 유지
            n += 1
            out.append({
                "hc": f"hc_{n:02d}", "case_of": cid,
                "ticker": (s.get("tickers") or ["UNK"])[0].upper(),
                "cik": s["cik"], "name": s["name"],
                "cutoff": sel[cid]["treatment"]["cutoff"],
                "sic": s.get("sic"), "rev_pit": s.get("rev_pit"),
                "size_dist": s.get("size_dist"), "size_flags": s.get("size_flags"),
            })
    return out


def stage(rs):
    for r in rs:
        x, e = DATA / r["ticker"] / "xbrl", DATA / r["ticker"] / "edgar"
        x.mkdir(parents=True, exist_ok=True)
        e.mkdir(parents=True, exist_ok=True)
        src = BIG / f"facts/CIK{r['cik']}.json"
        if not src.exists():
            raise SystemExit(f"companyfacts 캐시 부재: {src}")
        if not (x / src.name).exists():  # D23: 덮어쓰기 금지
            shutil.copy2(src, x / src.name)
        subs = sorted(BIG.glob(f"submissions/CIK{r['cik']}*.json"))
        if not subs:
            raise SystemExit(f"submissions 캐시 부재: CIK{r['cik']}")
        for s in subs:
            if not (e / s.name).exists():
                shutil.copy2(s, e / s.name)


def build():
    rs = rows()
    stage(rs)
    cases = [{"case_id": r["hc"], "ticker": r["ticker"], "cik": r["cik"],
              "company_name": r["name"], "cutoff_date": r["cutoff"]} for r in rs]
    CASES_DEST.write_text(json.dumps({"_meta": {
        "contract": "schemas/evaluatee_input.json",
        "generated_by": "tools/run_holdout_controls_scoring.py (결정론 — S2 랭크순)",
        "frame": "identity-visible PRIMARY (HOLDOUT_CONTROLS_PLAN §3 — 프라우드와 동일)",
        "order_convention": "케이스 알파벳 GNE→HUBG→WMK, 케이스 내 S2 랭크 (§5 발사순)"},
        "cases": cases}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MAP_DEST.write_text(json.dumps({"_meta": {"warning": "채점 전용 — 피평가자 노출 금지"},
        "mapping": {r["hc"]: r["ticker"] for r in rs},
        "case_of": {r["hc"]: r["case_of"] for r in rs}},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAND_DEST.write_text(json.dumps({"_meta": {
        "warning": "채점 정답 키 — 피평가자 노출 금지",
        "source": "runs/holdout/controls/control_group_holdout.json"},
        "candidates": [{"case_id": r["ticker"], "group": "control",
                        "company_name": r["name"], "ticker": r["ticker"], "cik": r["cik"],
                        "cutoff_date": r["cutoff"], "matched_treatment": r["case_of"],
                        "sic": r["sic"], "rev_pit": r["rev_pit"],
                        "scheme_summary": None, "scheme_type": None,
                        "manipulation_period_start": None,
                        "manipulation_period_end": None} for r in rs]},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  build: {len(cases)} controls → {CASES_DEST.name} (hc_01..hc_{len(cases):02d})")


def hcs_of(case):
    m = json.loads(MAP_DEST.read_text(encoding="utf-8"))
    return [hc for hc, c in m["case_of"].items() if case in (None, c)], m["mapping"]


def probe(case):
    hcs, mapping = hcs_of(case)
    cases = {c["case_id"]: c for c in
             json.loads(CASES_DEST.read_text(encoding="utf-8"))["cases"]}
    py = sys.executable
    bad = []
    for hc in hcs:
        c = cases[hc]
        r = subprocess.run([py, "tools/holdout_probe.py", "--ticker", c["ticker"],
                            "--company", c["company_name"], "--out", RECOG_DIR], cwd=REPO)
        if r.returncode == 3:
            bad.append(c["ticker"])
        elif r.returncode != 0:
            raise SystemExit(f"probe 오류 ({c['ticker']}) exit {r.returncode}")
    if bad:
        raise SystemExit(f"knows_event=True 탈락: {bad} — alternates 승격 필요 (§2, 수동)")
    print(f"  probe: {len(hcs)}건 전건 knows_event=False admit")


def run(cmd):
    print(f"\n$ {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode == 2:
        print("  ⚠ 일부 케이스 FAIL (exit 2) — INCOMPLETE 표기", flush=True)
        return
    if r.returncode != 0:
        raise SystemExit(f"단계 exit {r.returncode} — 같은 명령 재실행으로 재개")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["build", "probe", "score", "grade"])
    ap.add_argument("--case", default=None, help="case_71|case_72|case_73 (probe/score 한정)")
    a = ap.parse_args()
    py = sys.executable
    if a.stage == "build":
        build()
    elif a.stage == "probe":
        probe(a.case)
    elif a.stage == "score":
        hcs, _ = hcs_of(a.case)
        run([py, "pipeline/runner.py", "--cases", str(CASES_DEST.relative_to(REPO)),
             "--only", *hcs, "--out", "runs/holdout/controls/scores"])
    elif a.stage == "grade":
        run([py, "scoring/grader_runner.py", "--runs", "runs/holdout/controls/scores",
             "--out", "scoring/grades_holdout_controls",
             "--mapping", str(MAP_DEST.relative_to(REPO)),
             "--candidates", str(CAND_DEST.relative_to(REPO))])
    return 0


if __name__ == "__main__":
    sys.exit(main())
