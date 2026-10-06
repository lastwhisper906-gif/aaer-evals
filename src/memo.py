"""The memo: one company, three analyses, in plain Korean, assembled by Python.

The owner asked for a memo a finance student can read. It is assembled here from
the three checked analyses and from `calculator.json`, and from nothing else:
every sentence is either an analyst's own `summary_ko` sentence with its
`{field}` paths replaced by the numbers Python computed, or a fixed sentence of
this file's. **One section per analysis, kept apart, and no combined verdict** —
there is no line anywhere in the memo that adds the three up, ranks the company,
or says what to do with its shares.

Two top-level sections, by the owner's decision of 2026-10-06: **회계**
(accounting) and **재무** (finance). The financial analysis and the valuation
are the two subsections of 재무; nothing in either is merged with the other.

A sentence the gate dropped is not rewritten here; the memo says it was dropped.

    python3.12 -m src.memo --run <run directory> --out memo_ko.md
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

try:
    from src import analysis_check, calculator, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import analysis_check, calculator, interpreter_pin

BAD_INPUT = 2

ACCOUNTING_KO = {
    "earnings_versus_cash": "이익 대 현금",
    "revenue_recognition": "매출 인식",
    "estimates_and_reserves": "추정치와 충당금",
    "cost_deferral": "비용 이연(자본화)",
    "cash_flow_engineering_and_off_balance_sheet": "현금흐름 조정과 부외 항목",
    "controls_audit_and_filing_signals": "내부통제·감사·공시 신호",
    "cross_document_reconciliation": "문서 간 대조",
    "industry_lens": "업종 관점(반도체·하드웨어)",
}
FINANCIAL_KO = {
    "profitability": "수익성", "efficiency": "효율성", "liquidity": "유동성",
    "solvency": "지급능력", "growth": "성장", "free_cash_flow": "잉여현금흐름",
    "dupont": "듀퐁 분해", "path_to_distress": "압박이 위기로 바뀌는 조건",
}
VALUATION_KO = {
    "value_range": "가치 범위", "price_position": "주가의 위치",
    "market_implied_growth": "시장이 가정한 성장률", "most_sensitive": "가장 민감한 가정",
    "accounting_adjustments": "회계 조정이 바꾼 가치",
}
OUTCOME_KO = {"confirms": "숫자가 설명을 뒷받침", "contradicts": "숫자가 설명과 모순",
              "unresolved": "숫자로 판단 불가"}
LIMITS_KO = {
    "accounting": "이 분석은 숫자와 설명이 어긋나는 곳, 그리고 회사가 자기 과거와 달라진 곳을 "
                  "찾습니다. 의도를 판단하지 않으며, 송장이나 계약서처럼 공시 밖에 있는 "
                  "증거는 볼 수 없습니다.",
    "financial": "이 분석은 회사가 공시한 숫자를 회사 자신의 과거와 비교해 건강 상태를 "
                 "읽습니다. 미래를 예측하지 않으며, 공시에 없는 것은 볼 수 없습니다.",
    "valuation": "이 가치평가는 밝힌 가정을 밝힌 공식에 넣은 결과입니다. 매매를 권하지 "
                 "않으며, 다른 사람이 다른 가정을 고르면 다른 가치가 나옵니다.",
}
# A dropped sentence is named, never quoted: the reason the gate wrote can carry
# the very digit or word it dropped, and the memo prints nothing the gate refused.
DROPPED_KO = "(검증을 통과하지 못해 제외된 문장입니다. 이유는 분석 파일의 dropped_items에 있습니다.)"

RATIO_WORDS = ("margin", "growth", "rate", "ratio", "over", "return", "turnover",
               "multiplier", "share", "premium", "beta", "wacc", "position", "smoothness")
USD_WORDS = ("revenue", "income", "cash", "flow", "debt", "value", "expenditure",
             "compensation", "liabilit", "assets", "equity", "capital", "ebit", "amount",
             "acquisitions", "borrowing", "dividends", "repurchases", "investments")


def field_node(fields: dict, path: str):
    node = fields
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
            node = node[int(part)]
        else:
            return None
    return node


def unit_of(path: str, node) -> str:
    if isinstance(node, dict) and node.get("unit"):
        return node["unit"]
    last = path.rsplit(".", 1)[-1]
    if "per_share" in path or last in ("low", "high", "price_at_cutoff"):
        return "USD per share"
    if last.startswith("days") or "days_" in last:
        return "days"
    if any(word in last for word in RATIO_WORDS):
        return "ratio"
    if any(word in last for word in USD_WORDS):
        return "USD"
    return "ratio"


def korean_number(value: float, unit: str, *, percent: bool = False) -> str:
    """A number as a Korean reader expects it, never rounded to hide a sign."""
    if value is None or not math.isfinite(value):
        return "(값 없음)"
    if percent:
        return f"{value * 100:,.1f}%"
    if unit == "USD":
        if abs(value) >= 1e8:
            return f"{value / 1e8:,.1f}억 달러"
        return f"{value / 1e4:,.0f}만 달러"
    if unit == "USD per share":
        return f"주당 {value:,.2f}달러"
    if unit == "days":
        return f"{value:,.1f}일"
    if unit == "months":
        return f"{value:,.1f}개월"
    if unit == "shares":
        return f"{value / 1e6:,.1f}백만 주"
    return f"{value:,.3f}"


# What an analyst writes straight after a placeholder that the number already
# carries, or that must agree with how the number is read aloud. The unit is
# printed by `korean_number`, so an analyst's own "일" after a days figure would
# print twice; and a particle chosen for a digit the analyst could not see
# ("{x}과" before "달러") reads wrong once the unit is there.
PARTICLES = {"과": ("과", "와"), "와": ("과", "와"), "이": ("이", "가"), "가": ("이", "가"),
             "을": ("을", "를"), "를": ("을", "를"), "은": ("은", "는"), "는": ("은", "는"),
             "으로": ("으로", "로"), "로": ("으로", "로")}
UNIT_AFTER = re.compile(r"달러|개월|일|주|%")
PARTICLE_AFTER = re.compile(r"(으로|과|와|을|를|은|는|이|가|로)(?![가-힣])")
# A digit read aloud: 영 일 이 삼 사 오 육 칠 팔 구. Those ending in a consonant
# take 과, 이, 을, 은; 일, 칠 and 팔 end in ㄹ, which takes 로, not 으로.
DIGIT_FINAL = {"0": "ㅇ", "1": "ㄹ", "3": "ㅁ", "6": "ㄱ", "7": "ㄹ", "8": "ㄹ"}


def _final_consonant(rendered: str) -> str | None:
    last = rendered.rstrip()[-1:]
    if last.isdigit():
        return DIGIT_FINAL.get(last)
    if "가" <= last <= "힣":
        return "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"[
            (ord(last) - 0xAC00) % 28 - 1] if (ord(last) - 0xAC00) % 28 else None
    return None          # "%" is read 퍼센트, and "(값 없음)" ends in a bracket


def _particle(rendered: str, particle: str) -> str:
    with_final, without = PARTICLES[particle]
    final = _final_consonant(rendered)
    if particle in ("으로", "로"):
        return with_final if final and final != "ㄹ" else without
    return with_final if final else without


def fill(text: str | None, fields: dict) -> str:
    """An analyst's sentence with each `{path}` replaced by its number."""
    if not text:
        return "(작성되지 않음)"
    out, last = [], 0
    for match in analysis_check.PLACEHOLDER.finditer(text):
        path, how = match.group(1), match.group(2)
        value = calculator.field_value(fields, path)
        node = field_node(fields, path)
        rendered = korean_number(value, unit_of(path, node), percent=how == "pct")
        at = match.end()
        unit = UNIT_AFTER.match(text, at)
        if unit:
            if not rendered.endswith(unit.group()):
                rendered += unit.group()     # the analyst's unit, where the number has none
            at = unit.end()
        particle = PARTICLE_AFTER.match(text, at)
        if particle:
            rendered += _particle(rendered, particle.group(1))
            at = particle.end()
        out.append(text[last:match.start()] + rendered)
        last = at
    return "".join(out) + text[last:]


def _entry(summary: dict, key: str, analysis: dict, block: str | None, fields: dict) -> str:
    source = (analysis.get(block) or {}).get(key) if block else analysis.get(key)
    if isinstance(source, dict) and "dropped" in source:
        return DROPPED_KO
    text = summary.get(key)
    if text is None and key in summary:
        return DROPPED_KO
    return fill(text, fields)


def accounting_section(analysis: dict | None, fields: dict, *, adjusted: dict | None = None
                       ) -> list[str]:
    out = ["## 1. 회계", "",
           "### 1.1 회계 분석 — 보고된 이익과 현금이 경제적 실질을 반영하는가", ""]
    if analysis is None:
        return out + ["회계 분석이 실행되지 않았습니다.", ""]
    summary = analysis.get("summary_ko") or {}
    for key, name in ACCOUNTING_KO.items():
        out.append(f"- **{name}**: {_entry(summary, key, analysis, 'areas', fields)}")
    anomalies = analysis.get("anomalies") or []
    out += ["", f"**이상 징후 목록** ({len(anomalies)}건, 건수 기준 없이 모두 적음)", ""]
    for item in anomalies:
        name = item.get("name_ko") or item.get("name") or item.get("id")
        outcome = OUTCOME_KO.get(item.get("numbers_vs_prose"), "")
        out.append(f"- {name} — {ACCOUNTING_KO.get(item.get('area'), item.get('area'))}"
                   + (f" · {outcome}" if outcome else ""))
    if not anomalies:
        out.append("- 없음")
    quality = ((adjusted or fields).get("free_cash_flow") or {}).get(
        "free_cash_flow_quality_adjusted") or {}
    applied = quality.get("adjustments_applied") or []
    out += ["", "**회계 조정** (금액은 분석가가 지정한 계산기 항목에서 Python이 읽음)", ""]
    for item in applied:
        verb = "차감" if item["direction"] == "reduce" else "가산"
        out.append(f"- {item.get('name')}: {korean_number(item['amount'], 'USD')} {verb} "
                   f"(`{item['calculator_field']}`)")
    if not applied:
        out.append("- 없음")
    return out + ["", f"_한계: {LIMITS_KO['accounting']}_", ""]


def financial_section(analysis: dict | None, fields: dict) -> list[str]:
    out = ["### 2.1 재무 분석 — 이 회사는 얼마나 건강한가", ""]
    if analysis is None:
        return out + ["재무 분석이 실행되지 않았습니다.", ""]
    summary = analysis.get("summary_ko") or {}
    for key, name in FINANCIAL_KO.items():
        block = "sections" if key in analysis_check.FINANCIAL_SECTIONS else None
        out.append(f"- **{name}**: {_entry(summary, key, analysis, block, fields)}")
    anomalies = analysis.get("anomalies") or []
    out += ["", f"**재무 압박 징후 목록** ({len(anomalies)}건)", ""]
    for item in anomalies:
        out.append(f"- {item.get('name_ko') or item.get('name') or item.get('id')}")
    if not anomalies:
        out.append("- 없음")
    return out + ["", f"_한계: {LIMITS_KO['financial']}_", ""]


def valuation_section(analysis: dict | None, fields: dict) -> list[str]:
    out = ["### 2.2 가치평가 — 이 회사의 가치는 얼마이고, 주가는 무엇을 이미 가정하는가", ""]
    value = fields.get("valuation") or {}
    if "missing" in value:
        out += [f"Python이 가치를 계산하지 못했습니다. 이유: {value['missing']}", ""]
    else:
        band = value.get("value_range_per_share") or {}
        reverse = value.get("reverse_dcf") or {}
        history = (fields.get("earnings_versus_cash") or {}).get("history") or {}
        out += [f"- 주당 가치 범위: {korean_number(band.get('low'), 'USD per share')} ~ "
                f"{korean_number(band.get('high'), 'USD per share')}",
                f"- 기준일 주가: {korean_number(value.get('price_at_cutoff'), 'USD per share')}"
                f" ({value.get('price_position', '위치 계산 안 됨')})",
                f"- 시장이 가정한 10년 매출 성장률: "
                f"{korean_number(reverse.get('value'), 'ratio', percent=True) if 'value' in reverse else '(' + str(reverse.get('missing')) + ')'}"
                f" · 과거 3년 연평균: "
                f"{korean_number(history.get('revenue_growth_three_year_compound'), 'ratio', percent=True)}",
                ""]
    if analysis is None:
        return out + ["가치평가 분석가의 해석이 없습니다.", "",
                      f"_한계: {LIMITS_KO['valuation']}_", ""]
    summary = analysis.get("summary_ko") or {}
    for key, name in VALUATION_KO.items():
        out.append(f"- **{name}**: {_entry(summary, key, analysis, None, fields)}")
    return out + ["", f"_한계: {LIMITS_KO['valuation']}_", ""]


def baselines_section(baselines: dict | None) -> list[str]:
    out = ["## 참고: 공식 기준선 (위 세 분석과 합치지 않음)", ""]
    if not baselines:
        return out + ["- 기준선 파일이 없습니다.", ""]
    for name in ("beneish_m_score", "accruals_over_assets", "net_operating_assets",
                 "piotroski_f_score", "altman_z_score", "ohlson_o_score"):
        row = baselines.get(name) or {}
        shown = (f"{row['value']:,.3f}" if isinstance(row.get("value"), (int, float))
                 else f"계산 안 됨 ({str(row.get('missing', '이유 없음'))[:120]})")
        out.append(f"- {name}: {shown}")
    return out + [""]


def memo(*, ticker: str, form: str, period_end: str, cutoff: str, fields: dict,
         accounting: dict | None, financial: dict | None, valuation: dict | None,
         baselines: dict | None, filings_only: dict | None = None) -> str:
    """`fields` is the final calculator; `filings_only` the view the accounting and
    financial analysts read. Each section's paths are filled from the file its
    analyst was handed, so no sentence prints a number its writer did not see."""
    seen = filings_only if filings_only is not None else fields
    lines = [f"# {ticker} — {form}, {period_end} 기간 (제출일 {cutoff}) 분석 메모", "",
             "세 분석은 따로 적습니다. 세 분석을 합친 점수나 결론, 회사 간 순위는 없습니다. "
             "숫자는 모두 Python이 공시된 값에서 계산했고, 분석가는 숫자를 직접 쓰지 않았습니다.",
             ""]
    lines += accounting_section(accounting, seen, adjusted=fields)
    lines += ["## 2. 재무", ""]
    lines += financial_section(financial, seen)
    lines += valuation_section(valuation, fields)
    lines += baselines_section(baselines)
    missing = fields.get("missing") or []
    if missing:
        lines += ["## 계산하지 못한 항목", ""] + [f"- {line}" for line in missing] + [""]
    return "\n".join(lines).rstrip() + "\n"


def _load(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the plain-Korean memo for one run")
    parser.add_argument("--run", required=True, help="the run directory")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    run = Path(args.run)
    fields = _load(run / "calculator.json")
    filings_only = _load(run / "calculator_filings_only.json")
    if fields is None:
        print("memo: no calculator.json in the run", file=sys.stderr)
        return BAD_INPUT
    text = memo(ticker=fields["ticker"], form=fields["form"], period_end=fields["period_end"],
                cutoff=fields["cutoff"], fields=fields,
                accounting=_load(run / "analysis_accounting.json"),
                financial=_load(run / "analysis_financial.json"),
                valuation=_load(run / "analysis_valuation.json"),
                baselines=_load(run / "baselines.json"), filings_only=filings_only)
    Path(args.out).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
