"""knows_event 인지 프로브 러너 — E1 대조군 컷오프-후 비인지 게이트 (HOLDOUT_CONTROLS_PLAN §2).

기존 `runs/holdout/recognition/*.json` transcript는 커밋된 스크립트 없이 생성되었다
(RP-11 P2.1). 본 러너는 그 스키마를 그대로 미러링해 E1 대조군(및 향후 홀드아웃 후보)
프로브를 재현 가능하게 만든다. 게이트 판정은 **event 인지**이지 name-ID(정체 인식)가
아니다 — 정체를 알아도 폭로 미인지면 admit (§2).

- 피평가자 핀 claude-sonnet-5, 핀 불일치 = discard(재실행).
- knows_event=True → 해당 대조군 탈락, 차순위 alternate 승격 (순수 함수 재실행).
- transcript 커밋 위치: runs/holdout/controls/recognition/{TICKER}.json
  (runs/ 신규 파일 → verify_blindness --write-manifest 동반 커밋 필수)

사용:  python tools/holdout_probe.py --ticker HUBG --company "Hub Group, Inc." \
           [--kind holdout-control] [--context "..."] [--out runs/holdout/controls/recognition]
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from pipeline.cli_client import call_model  # noqa: E402

PIN_MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = (
    "You are a factual-recall probe. Answer strictly from your training knowledge. "
    "Do not speculate, do not browse, do not fabricate. If you do not have reliable "
    "specific knowledge, say so and set knows_event to false."
)

USER_TEMPLATE = (
    "Company: {company} (ticker: {ticker}).\n\n"
    "Question: To your knowledge, has this company ever announced an accounting "
    "restatement, an Item 4.02 non-reliance event, a material financial-reporting "
    "misstatement, an SEC accounting investigation, or a finance-executive departure "
    "tied to financial-reporting issues?\n\n"
    "Report only what you actually recall from training data. If you recall such an "
    "event, describe it and give an approximate date. If not, say you have no such "
    "knowledge."
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["knows_event", "event_description", "approx_date", "confidence"],
    "properties": {
        "knows_event": {"type": "boolean"},
        "event_description": {"type": "string"},
        "approx_date": {"type": ["string", "null"]},
        "confidence": {"type": "string", "enum": ["none", "low", "medium", "high"]},
    },
}


def probe(ticker: str, company: str, kind: str, context: str, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    res = call_model(
        model=PIN_MODEL,
        system_prompt=SYSTEM_PROMPT,
        user_payload=USER_TEMPLATE.format(company=company, ticker=ticker),
        schema=SCHEMA,
        log_dir=out_dir / "_logs",
        log_name=f"probe_{ticker}",
    )
    if not res.ok:
        raise RuntimeError(f"probe 실패 ({ticker}): {res.fail_reason}")
    if not res.pin_ok:
        raise RuntimeError(f"핀 불일치 ({ticker}): served={res.served_models} — discard, 재실행")
    record = {
        "ticker": ticker,
        "company": company,
        "kind": kind,
        "context": context,
        **res.structured,
        "served_models": res.served_models,
        "pin_ok": res.pin_ok,
        "session_id": res.session_id,
        "cost_ref_usd": res.total_cost_usd,
    }
    out = out_dir / f"{ticker}.json"
    out.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{ticker}: knows_event={record['knows_event']} confidence={record['confidence']}"
          f" → {out.relative_to(REPO)}")
    return record


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--company", required=True)
    ap.add_argument("--kind", default="holdout-control")
    ap.add_argument("--context", default="E1 control recognition gate (post-cutoff)")
    ap.add_argument("--out", default="runs/holdout/controls/recognition")
    a = ap.parse_args()
    rec = probe(a.ticker, a.company, a.kind, a.context, REPO / a.out)
    return 0 if rec["knows_event"] is False else 3  # 3 = knows_event=True (탈락 신호)


if __name__ == "__main__":
    sys.exit(main())
