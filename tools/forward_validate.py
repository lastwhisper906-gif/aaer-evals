"""forward 사이클 봉인 전 기계 검증 (spec §3·§4·§6, D100).

usage: python tools/forward_validate.py --cycle forward/cycle_001

검사: ① universe 정합 ② source_manifest 전 항목 filing_date ≤ cutoff +
retrieval/filing 분리 저장 ③ scores 완결성(유니버스 전건 1레코드, not_scored
명시, 완료 분율 ≥11/12) ④ decision_state가 사전 등록 서수 컷과 기계 일치
⑤ 레코드 §6 전 필드 계약(두 배열 존재 의무 포함) + cited_sources ⊆
source_manifest + company.cik ↔ universe 교차 대조 ⑥ 봉인되는 자유서술
(top_signals·affected_account_areas)의 INV-13 금지어 (R13-1) ⑦ 봉인 커밋에
함께 실리는 러너 출력 원본 전체의 INV-13 금지어 (R14-1, runs leg).
네트워크 0 · 모델 호출 0. 위반 시 exit 1.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datetime

import forward_assemble
import forward_prepare
from forward_common import (ET, REPO, SCREENING_CUTOFF, EXECUTION_WINDOW_END,
                            MIN_SCORED, UNIVERSE_SIZE,
                            assert_subscription_only, cutoff_agreement_errors,
                            fp_siblings, read_json, parse_date, sha256_file)
from forward_prepare import check_universe
# R13-1: INV-13 금지어 목록은 발행 린트와 **같은 출처**를 쓴다 — 목록이 한쪽만
# 늘면 봉인 경로에 구멍이 생긴다 (lint_publication은 상수·REPO만 정의하는
# import-safe 모듈이며, 이 방향 의존은 tools/ 내부다).
from lint_publication import FRAUD_WORDS

DECISION_STATES = {"flag", "review", "no_flag", "abstain"}
SUFFICIENCY = {"sufficient", "partial", "insufficient"}
CONFIDENCE = {"high", "medium", "low"}

# R3-7: scores 레코드의 해시 필드 ↔ PROTOCOL.md 핀 ↔ 라이브 파일 3각 대조 대상
PIN_FILES = {"prompt_sha256": "pipeline/runner.py",
             "schema_sha256": "schemas/llm_output.json"}


def parse_protocol_pins(text: str) -> tuple[str | None, dict[str, str]]:
    """PROTOCOL.md에서 (모델 핀, {경로: sha256}) 추출 — forward_prepare 서식."""
    m = re.search(r"evaluatee_model \(pin\): `([^`]+)`", text)
    pins = dict(re.findall(r"- `([^`]+)` sha256 `([0-9a-f]{64})`", text))
    return (m.group(1) if m else None), pins


def _model_matches_pin(model: str, pin: str) -> bool:
    # 날짜형 접미사만 인정 — 임의 하이픈 확장은 다른 모델 (INV-21/R1-6,
    # cli_client._pin_matches 거울)
    return re.fullmatch(re.escape(pin) + r"(-\d{8})?", model) is not None


def _is_sha256(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def expected_state(score: int, sufficiency: str) -> str:
    if sufficiency == "insufficient":
        return "abstain"
    return "flag" if score >= 70 else ("review" if score >= 40 else "no_flag")


def _cited_source_attested(acc: str, sources: list[dict]) -> bool:
    """cited accession이 source_manifest에 등재되어 있는가 (§6 ⊆ 의무).

    R4-7(b): 비정형 인용("sec"·"20" 류)이 부분 문자열 일치로 인증되면
    ⊆ 의무가 장식이 된다 — accession 형태(대시형 10-2-6 또는 무대시 18자리)
    전체 토큰만 인정, accession_no 정확 일치 또는 URL 내 토큰 경계 출현."""
    if not re.fullmatch(r"\d{10}-\d{2}-\d{6}|\d{18}", acc):
        return False
    bare = acc.replace("-", "")
    dashed = f"{bare[:10]}-{bare[10:12]}-{bare[12:]}"
    for s in sources:
        if s.get("accession_no") in (dashed, bare, acc):
            return True
        url = s.get("url") or ""
        for token in (dashed, bare):
            if re.search(rf"(?<!\d){re.escape(token)}(?!\d)", url):
                return True
    return False


# R11-4: 해시 사슬은 "그 파일이 안 바뀌었다"만 증명한다 — scores.json이
# 실제로 그 출력에서 사전 등록 규칙대로 파생됐는지는 별개의 주장이며,
# 정합적으로 함께 고친 레코드(35/insufficient/abstain → 75/sufficient/flag)는
# 기존 leg 전부를 통과했다. 봉인의 값어치는 "동결 프로토콜의 출력임"이므로
# runs leg에서 실제로 재파생해 대조한다.
_REDERIVE_SKIP = ("prompt_sha256", "schema_sha256")


def _rederivation_errors(record: dict, out_path: Path,
                         universe_meta: dict) -> list[str]:
    rid = record.get("record_id")
    meta = universe_meta.get(rid)
    if meta is None:
        return []  # universe 밖 레코드는 상위 extra 검사가 잡는다
    try:
        out = read_json(out_path)
    except (OSError, ValueError) as exc:
        return [f"{rid}: runs 출력 파싱 불가 ({exc}) — 재파생 대조 불가"]
    try:
        expect = forward_assemble.assemble_record(
            {"record_id": rid, "name": meta.get("name"),
             "ticker": meta.get("ticker"), "cik": meta.get("cik")},
            out, record.get("run_output_sha256"))
    except (KeyError, TypeError) as exc:
        return [f"{rid}: 러너 출력에서 재파생 실패 ({exc}) — 조립 규칙과 "
                "출력 형식 불일치"]
    diffs = sorted(k for k, v in expect.items()
                   if k not in _REDERIVE_SKIP and record.get(k) != v)
    # R12-5: 대조가 expect 쪽만 돌면 레코드에만 있는 키는 보이지 않는다 —
    # 조립기가 만들지 않는 필드를 봉인 레코드에 덧붙여도 통과했다.
    # R13-6: status 예외를 뗀다. 이 대조에 도달하는 레코드는 채점된 레코드뿐
    # (not_scored는 :297에서 continue), 그리고 assemble_record는 out is None
    # 일 때만 status를 만든다 — 따라서 여기서의 status는 정의상 조립기가 만든
    # 필드가 아니다. 하필 제어 흐름 의미를 가진 유일한 필드를 대칭 대조 밖에
    # 두고 있었다: "status": "sealed_by_hand"를 실은 봉인 레코드가 오류 0으로
    # 통과했다 (R12-5-A 실측 반례).
    diffs += sorted(set(record) - set(expect))
    if diffs:
        return [f"{rid}: 봉인 레코드가 러너 출력의 재파생과 불일치 {diffs} — "
                "scores.json이 동결 프로토콜 산출이 아님 (조립 후 편집, 또는 "
                "stale 체크아웃 조립: assemble 재실행 필요, R11-4)"]
    return []


# R13-1: 모델 자유서술이 아무 게이트도 통과하지 않고 봉인 레코드에 실린다.
# top_signals의 선언된 계약("checklist item_id 참조만")은 스키마 description에만
# 있었고 runner._strip_descriptions가 송출 전에 그것을 지운다 — 실측 결과 커밋된
# 506개 러너 출력 중 계약을 만족한 것은 0건, 11.9%(60건)는 금지어를 담고 있다.
# forward 사이클의 유니버스는 **집행 대상이 아닌 현재 기업 12곳**이므로 INV-13이
# 무조건 적용되고(면책 문맥의 문장도 그 단어를 쓴다), 봉인 후에는 INV-06/INV-22로
# 수정이 불가능하다 — 봉인 전에 fail-closed로 막는다.
# 범위: forward 사이클 레코드 한정. runs/ 하위 회고 케이스는 AAER 집행 대상이라
# INV-13의 적용 대상이 아니며, 이 함수는 validate()에서만 호출된다.
FREE_TEXT_SEALED_FIELDS = ("top_signals", "affected_account_areas")


def fraud_word_errors(record: dict) -> list[str]:
    """봉인 대상 자유서술 필드의 INV-13 금지어 검사 (R13-1)."""
    rid = record.get("record_id")
    errs = []
    for field in FREE_TEXT_SEALED_FIELDS:
        value = record.get(field)
        if not isinstance(value, list):
            continue  # 부재/비배열은 §6 계약 leg가 별도로 잡는다
        for i, item in enumerate(value):
            low = str(item).lower()
            hits = sorted(w for w in FRAUD_WORDS if w in low)
            if hits:
                errs.append(
                    f"{rid}: {field}[{i}] INV-13 금지어 {hits} — 집행 대상이 "
                    "아닌 현재 기업에 단정 어휘 사용 금지 (면책 문맥도 동일). "
                    "봉인 후에는 정정 불가이므로 봉인 전 차단 (R13-1)")
    return errs


# R14-1: 위 게이트는 scores.json만 본다 — 그런데 봉인 커밋이 공개로 올리는 것은
# 러너 출력 원본(runs/forward/<cycle>/<record_id>.json)까지다. forward_seal의
# stage_extra가 그 트리를 함께 add·push하고, 같이 봉인되는 universe.json이
# record_id → name/ticker/cik를 잇는다. 그 파일 안의 checklist[].evidence·
# mechanism_hypotheses[].*·overall.* 서술은 어떤 게이트도 지나지 않았다
# (verify_blindness의 VOCAB_WARN_MARKERS는 kind가 perturbed/output일 때만,
# 그것도 WARN이며 runs/forward/**는 aux 등록이다; lint_publication은 runs/를
# 읽지 않는다). 범위 근거는 위 R13-1 주석과 동일하며 배선도 동일하게 좁다 —
# 이 함수는 validate()의 runs leg에서만 호출되고 회고 waves는 그 경로를
# 지나지 않는다. 필드 목록을 열거하는 대신 출력 JSON 전체를 훑는 이유는,
# 열거가 곧 다음 사이클의 구멍이기 때문이다(R13-1이 두 필드만 훑어서 생긴
# 구멍이 바로 이 항목이다).
def _json_text_nodes(node, path: str = "$"):
    """JSON 트리를 순회하며 (JSON 경로, 문자열 값) 쌍을 낸다."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _json_text_nodes(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _json_text_nodes(v, f"{path}[{i}]")


def run_output_fraud_word_errors(rid, out_path: Path) -> list[str]:
    """러너 출력 원본 전체의 INV-13 금지어 검사 (R14-1)."""
    try:
        out = read_json(out_path)
    except (OSError, ValueError):
        return []  # 파싱 불가는 _rederivation_errors가 이미 보고한다
    errs = []
    for jpath, text in _json_text_nodes(out):
        hits = sorted(w for w in FRAUD_WORDS if w in text.lower())
        if hits:
            errs.append(
                f"{rid}: {out_path.name} {jpath} INV-13 금지어 {hits} — 이 "
                "러너 출력은 봉인 커밋에 그대로 실려 공개되고 universe.json이 "
                "record_id를 실명 기업에 잇는다. 집행 대상이 아닌 현재 기업에 "
                "단정 어휘 사용 금지(면책 문맥도 동일), 봉인 후 정정 불가 "
                "— 소유자가 봉인 전에 결정해야 한다 (R14-1)")
    return errs


# R17-1: 서명된 런북이 지목하는 피평가자 레지스트리 (§4 (3)·(4)) — 사이클
# 디렉토리 이름에서 기계적으로 유도한다. 모듈 상수라서 테스트가 대체할 수 있다.
EVALUATEE_REGISTRY_DIR = REPO / "data" / "evaluatee"


def evaluatee_registry_path(cycle: Path) -> Path:
    suffix = Path(cycle).name.split("cycle_", 1)[-1]
    return EVALUATEE_REGISTRY_DIR / f"cases_forward_{suffix}.json"


def validate(cycle: Path, runs_dir: Path | None = None) -> list[str]:
    errs = []
    # R17-1: 세 컷오프 표면(PROTOCOL 스냅샷·봉인 매니페스트·피평가자 레지스트리)이
    # 동결 상수 하나에서 파생됐는지 — 봉인 **전에** 판정한다. 종전에는 매니페스트에
    # `cutoff` 키가 아예 없어도, `"2027-12-31"`이어도 오류가 0건이었다.
    errs += cutoff_agreement_errors(cycle, evaluatee_registry_path(cycle))
    u = read_json(cycle / "universe.json")
    errs += [f"universe: {e}" for e in check_universe(u)]
    universe_ids = {r["record_id"] for r in u.get("selected", [])}
    universe_cik = {r["record_id"]: str(r.get("cik", "")).zfill(10)
                    for r in u.get("selected", [])}
    universe_meta = {r["record_id"]: r for r in u.get("selected", [])}

    # R3-7: PROTOCOL 핀 ↔ 라이브 동결 파일 ↔ scores 해시 3각 fail-closed 대조
    model_pin, pins = None, {}
    proto_path = cycle / "PROTOCOL.md"
    if proto_path.exists():
        model_pin, pins = parse_protocol_pins(proto_path.read_text(encoding="utf-8"))
        if not model_pin:
            errs.append("PROTOCOL: evaluatee_model 핀 미해석")
        # R12-8: 드리프트 대조는 PROTOCOL이 핀한 **전건**을 돈다. 종전에는
        # PIN_FILES(2개)만 돌아, prepare가 핀한 7개 중 5개는 어떤 게이트도
        # 재검증하지 않았다 — 그 5개에 `pipeline/cli_client.py`(모델을 호출하는
        # 바로 그 코드)가 들어 있어, 코드가 바뀐 채로 봉인된 사이클이
        # "이 해시의 코드가 이 점수를 냈다"는 봉인의 중심 주장을 거짓으로 만들고도
        # 사슬이 알아차리지 못했다 (실측: 5개 중 3개가 이미 드리프트).
        expected_pins = set(forward_prepare.PIN_SOURCES)
        missing = sorted(expected_pins - set(pins))
        if missing:
            errs.append(f"PROTOCOL: 핀 부재 {missing} — prepare가 핀하는 "
                        "전건이 기재돼야 한다 (PIN_SOURCES 정합)")
        for rel in sorted(expected_pins & set(pins)):
            if sha256_file(REPO / rel) != pins[rel]:
                errs.append(f"PROTOCOL 핀 ≠ 라이브 파일 해시: {rel} — 재핀은 "
                            "FREEZE_REV/supersession 문서로만 (Q-O11)")
        # PIN_FILES는 레코드 필드 ↔ 핀 대조(별개 leg)로 계속 쓰인다 —
        # 그 두 경로가 PROTOCOL에 실제로 있는지만 여기서 확인한다.
        for rel in PIN_FILES.values():
            if rel not in pins:
                errs.append(f"PROTOCOL: `{rel}` 핀 부재 (레코드 대조 leg)")
    else:
        errs.append("PROTOCOL.md 부재 — 핀 대조 불가 (fail-closed)")

    cutoff = parse_date(SCREENING_CUTOFF)
    sources: list[dict] = []
    sm_path = cycle / "source_manifest.json"
    if sm_path.exists():
        sources = read_json(sm_path).get("sources", [])
        for i, e in enumerate(sources):
            for field in ("filing_date", "retrieval_date", "url"):
                if not e.get(field):
                    errs.append(f"source[{i}]: {field} 결측 (retrieval/filing 분리 저장 의무)")
            # R16-5: sha256은 truthiness가 아니라 형식으로 본다 — `"abc"`는
            # 종전 검사를 통과했고 실제로 픽스처에 봉인돼 있었다. 같은 파일의
            # run_output_sha256 leg는 이미 _is_sha256를 쓴다.
            if not _is_sha256(e.get("sha256")):
                errs.append(f"source[{i}]: sha256 부재/비정형 {e.get('sha256')!r} "
                            "— 봉인이 출처 바이트를 가리키지 못한다")
            try:
                if e.get("filing_date") and parse_date(e["filing_date"]) > cutoff:
                    errs.append(f"source[{i}] {e.get('url', '?')[:60]}: filing_date "
                                f"{e['filing_date']} > cutoff {SCREENING_CUTOFF}")
            except ValueError:
                errs.append(f"source[{i}]: filing_date 파싱 불가 {e.get('filing_date')!r}")
    else:
        errs.append("source_manifest.json 부재")

    sc_path = cycle / "scores.json"
    if sc_path.exists():
        records = read_json(sc_path).get("records", [])
        seen = {}
        scored = 0
        for r in records:
            rid = r.get("record_id")
            if rid in seen:
                errs.append(f"{rid}: 중복 레코드")
            seen[rid] = r
            if r.get("status") == "not_scored":
                continue
            scored += 1
            s = r.get("misstatement_risk_score")
            if not isinstance(s, int) or not (0 <= s <= 100):
                errs.append(f"{rid}: misstatement_risk_score 비정상 {s!r} (0–100 정수 서수)")
                continue
            suff = r.get("evidence_sufficiency")
            if suff not in SUFFICIENCY:
                errs.append(f"{rid}: evidence_sufficiency 비정상 {suff!r}")
            if r.get("assessment_confidence") not in CONFIDENCE:
                errs.append(f"{rid}: assessment_confidence 비정상")
            ds = r.get("decision_state")
            if ds not in DECISION_STATES:
                errs.append(f"{rid}: decision_state 비정상 {ds!r}")
            elif suff in SUFFICIENCY and ds != expected_state(s, suff):
                errs.append(f"{rid}: decision_state {ds} ≠ 서수 컷 기대 "
                            f"{expected_state(s, suff)} (score {s}, {suff})")
            for field in ("company", "cited_sources", "model_id",
                          "prompt_sha256", "schema_sha256", "scored_at"):
                if not r.get(field):
                    errs.append(f"{rid}: {field} 결측")
            # R7-17: scored_at은 ISO datetime + 실행 창 내 — 비어있지 않다는
            # 것만으로는 아무 문자열이나 봉인된다. 레코드 수준 오류
            # (--past-window 주석 의미론과 동일 — 추가 봉인 차단 없음).
            sa = r.get("scored_at")
            if sa:
                try:
                    sa_dt = datetime.datetime.fromisoformat(str(sa))
                except ValueError:
                    errs.append(f"{rid}: scored_at {sa!r} ISO datetime 아님")
                else:
                    # R10-8: 창은 ET 정의 — tz-aware 기록(러너는 UTC)은 ET로
                    # 환산 후 날짜 비교. 아니면 마지막 창일 19:00 ET 이후 배치
                    # 전체가 UTC 다음 날짜로 넘어가 "실행 창 밖" 오판정된다.
                    # naive 문자열은 이미 창 로컬(ET) 날짜로 간주.
                    sa_date = (sa_dt.astimezone(ET).date()
                               if sa_dt.tzinfo is not None else sa_dt.date())
                    if not (parse_date(SCREENING_CUTOFF) <= sa_date
                            <= parse_date(EXECUTION_WINDOW_END)):
                        errs.append(
                            f"{rid}: scored_at {sa!r} 실행 창 밖 "
                            f"({SCREENING_CUTOFF}..{EXECUTION_WINDOW_END})")
            # R3-7: 레코드 해시 ↔ PROTOCOL 핀, model_id ↔ 모델 핀, 그리고
            # 런타임 fingerprint(run_fingerprint) ↔ 조립 시점 해시 정합
            for field, rel in PIN_FILES.items():
                if r.get(field) and pins.get(rel) and r[field] != pins[rel]:
                    errs.append(f"{rid}: {field} ≠ PROTOCOL 핀 ({rel}) — "
                                "런/조립 사이 동결 파일 드리프트")
            if model_pin and r.get("model_id") and not _model_matches_pin(
                    str(r["model_id"]), model_pin):
                errs.append(f"{rid}: model_id {r['model_id']!r} ≠ 핀 {model_pin!r}")
            rf = r.get("run_fingerprint")
            if not isinstance(rf, dict):
                errs.append(f"{rid}: run_fingerprint 부재 — 러너 call-time "
                            "fingerprint가 봉인 대상에 실리지 않음 (R3-7)")
            else:
                # R4-4: 각 leg fail-closed — 빈 dict·결측 키가 대조를 침묵
                # 스킵하면 leg 전체가 fail-open이다
                if not _is_sha256(rf.get("schema_sha256")):
                    errs.append(f"{rid}: run_fingerprint.schema_sha256 "
                                f"부재/비정형 {rf.get('schema_sha256')!r}")
                elif r.get("schema_sha256") and rf["schema_sha256"] != r["schema_sha256"]:
                    errs.append(f"{rid}: run-time schema_sha256 ≠ assemble-time — "
                                "런/조립 드리프트 (자기모순 봉인 차단)")
                if model_pin:
                    requested = rf.get("model_requested")
                    if not requested:
                        errs.append(f"{rid}: run_fingerprint.model_requested 부재")
                    elif not _model_matches_pin(str(requested), model_pin):
                        errs.append(f"{rid}: run_fingerprint.model_requested "
                                    f"{requested!r} ≠ 핀 {model_pin!r}")
            # R3-8/R4-4: 봉인 해시 사슬이 러너 출력 파일까지 닿아야 한다 — 64-hex 강제
            if not _is_sha256(r.get("run_output_sha256")):
                errs.append(f"{rid}: run_output_sha256 부재/비정형 "
                            f"{r.get('run_output_sha256')!r} — 봉인이 러너 출력을 "
                            "커버하지 않음 (R3-8/R4-4)")
            # §6: 세 배열은 존재 의무 — 빈 배열은 적법, 키 부재는 위반
            # (top_signals: 스키마 maxItems=5·minItems 없음 — []는 적법한
            #  핀 모델 출력이므로 falsy 검사로 봉인을 막지 않는다)
            for field in ("benign_alternative_explanations", "affected_account_areas",
                          "top_signals"):
                if not isinstance(r.get(field), list):
                    errs.append(f"{rid}: {field} 부재/비배열 (§6 — 빈 배열 허용, 키 생략 불가)")
            errs += fraud_word_errors(r)
            for acc in r.get("cited_sources") or []:
                if not _cited_source_attested(str(acc), sources):
                    errs.append(f"{rid}: cited_sources {acc!r} — source_manifest 미등재 (§6 ⊆ 의무)")
            comp = r.get("company")
            if isinstance(comp, dict) and rid in universe_cik:
                cik = str(comp.get("cik", "")).zfill(10)
                if cik != universe_cik[rid]:
                    errs.append(f"{rid}: company.cik {comp.get('cik')!r} ≠ universe CIK "
                                f"{universe_cik[rid]} — 점수 후 교체 금지 (§1)")
        missing = universe_ids - set(seen)
        if missing:
            errs.append(f"유니버스 레코드 누락 {sorted(missing)} — not_scored라도 명시 등재 의무")
        extra = set(seen) - universe_ids
        if extra:
            errs.append(f"유니버스 밖 레코드 {sorted(extra)} — 점수 후 교체 금지 (§1)")
        if scored < MIN_SCORED:
            errs.append(f"완료 분율 미달: scored {scored} < {MIN_SCORED}/{UNIVERSE_SIZE} "
                        "— 봉인 불가, spec §3-3 (abort 규칙 §3-2 적용)")
        # R4-4: run_output_sha256 실측 재해시 — 어떤 도구도 실제로 재해시하지
        # 않으면 leg는 신뢰 사슬이 아니라 장식이다. runs 부재(클론 검증자)는
        # 공지 후 생략, 존재하면 전건 대조.
        if runs_dir is not None:
            if runs_dir.is_dir():
                # R7-3: fp-sibling 존재 = 정본 모호 — 봉인이 stale 출력을
                # 인증하지 못하게 여기(봉인 시 실행되는 leg)서도 fail-closed
                for s in fp_siblings(runs_dir):
                    errs.append(f"fp-sibling 존재: {s.name} — 어느 런이 정본인지 "
                                "모호, 봉인 전 소유자 해소 필요 (R7-3)")
                for r in records:
                    if r.get("status") == "not_scored":
                        # R11-7: 완료 분율(≥11/12)은 선택 보고에 대한 유일한
                        # 방어인데, 검사가 한 방향뿐이라 stale assemble만으로도
                        # 충족됐다 — 레이트 리밋 후 재개로 완료된 레코드가
                        # not_scored로 봉인되고, 그 출력 파일은 봉인 커밋에
                        # 함께 실린다(제3자에겐 사후 배제와 구분 불가).
                        resumed = runs_dir / f"{r.get('record_id')}.json"
                        if resumed.exists():
                            errs.append(
                                f"{r.get('record_id')}: not_scored인데 러너 출력 "
                                f"{resumed.name} 존재 — assemble 재실행 필요 "
                                "(완료분을 배제한 채 봉인 금지, R11-7)")
                        continue
                    out_path = runs_dir / f"{r.get('record_id')}.json"
                    if not out_path.exists():
                        errs.append(f"{r.get('record_id')}: runs 출력 부재 "
                                    f"({out_path.name}) — run_output_sha256 대조 불가")
                    elif _is_sha256(r.get("run_output_sha256")) and \
                            sha256_file(out_path) != r["run_output_sha256"]:
                        errs.append(f"{r.get('record_id')}: runs 출력 실측 해시 ≠ "
                                    "run_output_sha256 — 조립 후 변조/드리프트")
                    else:
                        errs += _rederivation_errors(r, out_path, universe_meta)
                        errs += run_output_fraud_word_errors(
                            r.get("record_id"), out_path)
            else:
                print(f"NOTICE — runs 디렉토리 부재({runs_dir}): run_output_sha256 "
                      "실측 재해시 생략 (커밋 산출물만 가진 검증자는 정상)")
    else:
        errs.append("scores.json 부재")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--runs", default=None,
                    help="R4-4: 러너 출력 디렉토리 (기본 규약 runs/forward/<cycle명>) "
                         "— 존재 시 run_output_sha256 실측 재해시, 부재 시 공지 후 생략")
    args = ap.parse_args()
    assert_subscription_only()
    runs_dir = REPO / (args.runs or f"runs/forward/{Path(args.cycle).name}")
    errs = validate(REPO / args.cycle, runs_dir=runs_dir)
    if errs:
        print("FAIL — forward 검증 위반:")
        for e in errs:
            print(f"  {e}")
        return 1
    print(f"PASS — forward 검증 (universe·cutoff·scores·decision 컷 정합, "
          f"cutoff {SCREENING_CUTOFF})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
