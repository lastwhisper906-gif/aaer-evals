"""memo_verify.py — 티커 일반화 인용 검증기 (blind_memo_verify.py의 매개변수화 후계, P1+P3).

blind_memo_verify.py는 OUT-GIL-V1 기록으로 동결 — 본 파일은 데이터 디렉토리를
매개변수화하고 판정 라우팅(--adjudication-queue, P3)을 추가한다. 매칭 로직
(normalize·best_window·check_quote·status_of)과 임계(0.95/0.80)는 바이트 동일
상속 (tools/test_memo_pipeline.py가 소스 동일성을 강제).

--adjudication-queue: VERIFIED는 조용히 통과, 비-VERIFIED 항목마다
<flags dir>/adjudication_queue.md에 판정 블록을 낸다 — 인용문·최근접 원문
윈도(유사도 병기)·4택 판정 체크리스트·서명란. GIL의 사후 작성
citation_adjudication.md 형식을 사전 구조화 템플릿으로 바꾼 것.
"수기 판정 소요 분(minutes)" 필드는 서명 시 기입 (메모당 운영 지표).

Usage: python tools/memo_verify.py <flags.json> --data-dir data/<ticker>
       [--adjudication-queue]
corpus 문서 목록: <data-dir>/manifest.json의 documents[].extracted_file
(부재 시 <data-dir>/*.txt 정렬 순).
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def normalize(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("|", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def best_window(quote: str, corpus: str) -> tuple[float, int]:
    """Best difflib ratio of quote vs sliding windows over corpus; returns (ratio, pos)."""
    L = len(quote)
    if L == 0 or L > len(corpus):
        return 0.0, -1
    win = int(L * 1.25) + 8
    step = max(1, L // 4)
    best, best_pos = 0.0, -1
    sm = difflib.SequenceMatcher(autojunk=False)
    sm.set_seq2(quote)  # seq2 is cached
    for pos in range(0, len(corpus) - L + 1, step):
        chunk = corpus[pos:pos + win]
        sm.set_seq1(chunk)
        if sm.real_quick_ratio() < best or sm.quick_ratio() < max(best, 0.6):
            continue
        r = sm.ratio()
        if r > best:
            best, best_pos = r, pos
    return best, best_pos


def check_quote(quote: str, corpora: dict[str, str]) -> dict:
    q = normalize(quote)
    result = {"exact": False, "similarity": 0.0, "matched_doc": None}
    for name, corpus in corpora.items():
        if q in corpus:
            return {"exact": True, "similarity": 1.0, "matched_doc": name}
    for name, corpus in corpora.items():
        r, _ = best_window(q, corpus)
        if r > result["similarity"]:
            result.update(similarity=round(r, 3), matched_doc=name)
    return result


def status_of(res: dict) -> str:
    if res["exact"] or res["similarity"] >= 0.95:
        return "VERIFIED"
    if res["similarity"] >= 0.80:
        return "ALTERED"
    return "NOT FOUND"


def nearest_window_text(quote: str, corpora: dict[str, str], matched_doc: str) -> str:
    """비-VERIFIED 판정 블록용 — 최근접 원문 윈도 추출 (매칭 로직 비변경, 재호출)."""
    if not matched_doc:
        return "(no candidate window found)"
    q = normalize(quote)
    corpus = corpora[matched_doc]
    _, pos = best_window(q, corpus)
    if pos < 0:
        return "(no candidate window found)"
    win = int(len(q) * 1.25) + 8
    return corpus[pos:pos + win]


VERDICT_OPTIONS = ("병합 인용(merged quotation)", "의역(paraphrase)",
                   "날조 의심(suspected fabrication)", "원문 재확인 필요(needs source check)")


def write_adjudication_queue(out_path: Path, source_name: str, rows: list[dict],
                             corpora: dict[str, str]) -> int:
    """비-VERIFIED 행마다 판정 블록 — 반환값은 블록 수 (0이면 파일에 '판정 대상 없음' 기록)."""
    pending = [r for r in rows if r["status"] != "VERIFIED"]
    lines = [
        f"# 인용 판정 큐 — {source_name} (1차: 프로그램 판정, 최종 확정: 인간 서명)",
        "",
        f"- 프로그램 판정: {sum(r['status'] == 'VERIFIED' for r in rows)}/{len(rows)} VERIFIED"
        f" — 비-VERIFIED {len(pending)}건이 아래 판정 대상이다. VERIFIED는 조용히 통과.",
        "- 임계 (사전 고정, blind_memo_verify.py와 동일): VERIFIED = 정확 일치 또는"
        " 유사도 ≥ 0.95 · ALTERED ≥ 0.80 · NOT FOUND < 0.80.",
        "- 판정자 규율: 각 건에 4택 중 하나를 표시하고 근거 1줄(원문 fragment"
        " grep 결과 등)을 남긴다. '날조 의심' 판정 시 해당 인용은 발행 표면에서"
        " 제거하거나 flag 자체를 강등한다.",
        "",
    ]
    if not pending:
        lines.append("**판정 대상 없음 — 전 인용 VERIFIED.**")
    for r in pending:
        lines += [
            "---",
            "",
            f"## {r['flag']}.{r['quote_no']} — {r['status']} (유사도 {r['similarity']})"
            f" · flag: {r['flag_title']}",
            "",
            f"**인용문 (피평가자 출력)**:",
            "```",
            r["quote"],
            "```",
            f"**주장 위치**: {r['claimed_location']}",
            f"**최근접 원문 윈도** ({r['matched_doc'] or '없음'}, 정규화 텍스트):",
            "```",
            nearest_window_text(r["quote"], corpora, r["matched_doc"]),
            "```",
            "**판정 (하나 선택)**:",
            *[f"- [ ] {opt}" for opt in VERDICT_OPTIONS],
            "**근거 (1줄)**: ______",
            "",
        ]
    lines += [
        "---",
        "",
        "## 서명",
        "",
        "- 수기 판정 소요: ______ 분 (메모당 운영 지표 — 서명 시 기입)",
        "- [ ] 위 판정 및 memo 반영 승인 — 사용자: ______ 날짜: ______",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return len(pending)


def corpus_files(data_dir: Path) -> list[str]:
    manifest = data_dir / "manifest.json"
    if manifest.exists():
        docs = json.loads(manifest.read_text(encoding="utf-8"))["documents"]
        return [d["extracted_file"] for d in docs]
    return sorted(p.name for p in data_dir.glob("*.txt"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("flags", type=Path)
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--adjudication-queue", action="store_true",
                    help="비-VERIFIED 판정 블록을 <flags dir>/adjudication_queue.md로 라우팅")
    args = ap.parse_args()

    flags = json.loads(args.flags.read_text(encoding="utf-8"))["flags"]
    corpora = {f: normalize((args.data_dir / f).read_text(encoding="utf-8"))
               for f in corpus_files(args.data_dir)}

    rows, n_verified = [], 0
    for fi, flag in enumerate(flags, 1):
        for qi, q in enumerate(flag["quotes"], 1):
            res = check_quote(q["text"], corpora)
            st = status_of(res)
            n_verified += st == "VERIFIED"
            rows.append({"flag": fi, "flag_title": flag["title"], "quote_no": qi,
                         "quote": q["text"], "claimed_location": q["location"],
                         "status": st, **res})

    out = args.flags.parent / "citation_verification.json"
    out.write_text(json.dumps({"source": str(args.flags.name), "quotes": len(rows),
                               "verified": n_verified, "rows": rows}, indent=2) + "\n",
                   encoding="utf-8")
    print(f"{n_verified}/{len(rows)} VERIFIED — detail: {out}\n")
    print("| # | Quote (truncated) | Claimed location | Status | Sim | Matched doc |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        qt = (r["quote"][:60] + "…") if len(r["quote"]) > 60 else r["quote"]
        qt = qt.replace("|", "\\|")
        print(f"| {r['flag']}.{r['quote_no']} | {qt} | {r['claimed_location']} "
              f"| {r['status']} | {r['similarity']} | {r['matched_doc']} |")

    if args.adjudication_queue:
        qpath = args.flags.parent / "adjudication_queue.md"
        n = write_adjudication_queue(qpath, args.flags.name, rows, corpora)
        print(f"\nadjudication queue: {n}건 → {qpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
