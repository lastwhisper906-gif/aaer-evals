"""P4 발행 정합 린트 — README + Issue 초안 + 공개 대상 패킷 섹션.

검사 (미션 P4):
  (A) 금지: "0% FPR"/"무오탐"/"0% 오탐" 등 (0% 오탐 헤드라인 금지 §37/L).
  (B) G2/현재 기업에 "fraud/분식/조작" (§6) — HUBG/WMK/GNE + 사명.
  (C) 대조군 회사가 주어인 부정 서술 (모델이 아니라 대조군을 주어로 한 유죄 문장).
  (D) pooled 수치가 standalone 병기 없이 등장.
  (E) E4/교차모델/opus 피평가자 언급에 EXPLORATORY 라벨 누락.
  (F) 수치 정합: 산문 통계가 동결 json(results_stats/wave2_results/synthesis)과 불일치
      + 알려진 stale 값 금지.
  (G) 교란(identity-masked) 프레임을 "lower bound/하한"으로 서술 금지 (D31 0-2, W3) —
      교정 문구("not a clean lower bound"/"하한이 아니다"/구조적 하한=홀드아웃)는 allowlist.
  (M) 철회된 "암기 불가능" 문언 재유입 금지 (D-P83/PKT-R2, R15-5) — 전 DOCS는 철회
      문구 그대로, 살아 있는 영어 정본 4종은 암기+불가능 결합 전반. 교정 맥락은 allowlist.
  (H) README가 E1 결과를 다루면 GRDX·78 co-presence 강제 (D31 0-1 — 누락형 왜곡 기계 차단).
  (I) 발행 표면이 3-arm delta(+6.0pp/−2.0pp/b−a/c−b)를 언급하면 confound(혼입)와
      draw-noise(draw 잡음) 단서 동반 강제 (D39 A-2 — arm (c) 설계 교란변수, L-7).
비영: 위반 0. 위반 시 라인·사유 출력 후 exit 1. `make verify`에 편입.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = ["README.md", "README.ko.md", "analysis/ISSUE_0_DRAFT.md",
        "analysis/ISSUE_1_WAVE2_DRAFT.md", "analysis/ISSUE_2_HOLDOUT_DRAFT.md",
        "docs/reader_validation/ONE_PAGER.md",  # D42: 독자 검증 원페이저도 발행 표면
        "RESULTS.md", "METHOD.md",              # D115: 영어 정본 수치 표·방법 문서
        "RESULTS.ko.md", "METHOD.ko.md",        # D115: 동결 한국어 원본 회귀 감시
        "AUDIT_INDEX.md", "REPRODUCING.md",     # D118: D114 영어화 2종 (F-01/F-02)
        "AUDIT_INDEX.ko.md", "REPRODUCING.ko.md",  # D118: 한국어 원본 회귀 감시
        "analysis/DECISION_TABLE.md", "analysis/DECISION_TABLE.ko.md",
        "docs/methodology_limitations.md",      # D-P50 #4 / Q-F14: 한계 원장 영어 정본
        "analysis/error_analysis_wave2_holdout.md", "ERRATA.md",
        "docs/README_DETAIL.md"]                # R7-12: README:179 연결 상세 서사
        # ko 원본 미편입 (D-P55): 동결 문언은 현행 발행 린트 규칙 제정 이전이다.
        # ERRATA ko 원본 미편입 (D-P55): 동결 스냅샷은 현행 발행 린트 규칙 제정 이전이다.
        # ko 원본 미편입 (D-P55): 동결 스냅샷이 W3/(E) 규칙 제정 이전 문언 —
        # 편입 시 영구 적색. 수치 충실도는 test_translation_equivalence가 잠금.

G2 = {"HUBG": ["hub group"], "WMK": ["weis markets", "weis"], "GNE": ["genie energy", "genie"]}
FRAUD_WORDS = ["fraud", "분식", "조작", "manipulat"]
# 대조군 티커 (unified_table에서 group=control) — 부정 서술의 주어 금지 대상
CONTROL_TICKERS = None  # lazy


def controls():
    global CONTROL_TICKERS
    if CONTROL_TICKERS is None:
        import csv
        rows = csv.DictReader(open(REPO / "analysis/unified_table.csv", encoding="utf-8"))
        CONTROL_TICKERS = {r["ticker"].split("/")[0] for r in rows if r["group"] == "control"}
    return CONTROL_TICKERS


def canon():
    """결과 JSON에서 유도한 정본 수치 — README에 전건 존재해야 (드리프트 기계 검출)."""
    r1 = json.load(open(REPO / "analysis/results_stats.json", encoding="utf-8"))["primary"]
    r2 = json.load(open(REPO / "analysis/wave2_results.json", encoding="utf-8"))["original"]
    return {
        "wave1_perm_p": [f"{r1['perm_p_one_sided']:.5f}".rstrip("0")],  # 0.00114
        "wave2_perm_p": [f"{r2['perm_p']:.5f}".rstrip("0")],            # 0.00116
        "wave2_auc": [f"{r2['auc']:.3f}"],                              # 0.829
        "wave1_fpr": ["13.6%", "3/22"],
        "wave2_fpr": ["21.7%", "5/23"],
        "wave2_ece": ["0.179"],
        "name_id_w2_frozen": ["21.9%"],
        # D31 0-1: 홀드아웃 tier 최고점 = 대조군 오탐 (GRDX 78) — README에 존재 강제.
        # co-presence(GRDX와 78 동시)는 check_canon의 (H) 규칙이 양 README에 검사.
        "e1_top_control_fp": ["GRDX"],
    }


def check_canon():
    """README ↔ 결과 JSON 수치 드리프트 검사 (키당 허용 문자열 중 1개 이상 존재)."""
    text = (REPO / "README.md").read_text(encoding="utf-8")
    viols = [("README.md", 0, f"canon drift: {key} — 기대 {variants} 중 어느 것도 README에 없음")
             for key, variants in canon().items()
             if not any(v in text for v in variants)]
    # (H) D31 0-1: E1 결과를 다루는 README에는 GRDX와 78이 함께 존재해야 PASS.
    for doc in ["README.md", "README.ko.md"]:
        t = (REPO / doc).read_text(encoding="utf-8")
        if re.search(r"\bE1\b|matched controls|매칭 대조군", t):
            if "GRDX" not in t or not re.search(r"\b78\b", t):
                viols.append((doc, 0, "(H) E1 커버 문서에 GRDX·78 co-presence 부재 "
                                      "(홀드아웃 tier 최고점=대조군 오탐 GRDX 78 — D31 0-1)"))
    # (I) D39 A-2: 3-arm delta를 언급하는 발행 표면은 confound·draw-noise 단서 동반.
    for doc in DOCS + ["analysis/synthesis.md"]:
        if not (REPO / doc).exists():
            continue
        t = (REPO / doc).read_text(encoding="utf-8")
        if THREEARM_DELTA.search(t):
            missing = []
            if not CONFOUND_TERM.search(t):
                missing.append("confound(혼입)")
            if not DRAWNOISE_TERM.search(t):
                missing.append("draw-noise(draw 잡음)")
            if missing:
                viols.append((doc, 0, f"(I) 3-arm delta 언급에 {' · '.join(missing)} "
                                      "단서 부재 (arm (c) 설계 교란변수 — D39 A-2, L-7)"))
    return viols


# (I) D39 A-2: 3-arm delta 언급 감지 + 필수 동반 단서 (문서 단위, check_canon에서 검사).
THREEARM_DELTA = re.compile(
    r"median\(\s*b\s*[−-]\s*a\s*\)|median\(\s*c\s*[−-]\s*b\s*\)"
    r"|b[−-]a\s+(contrast|대비)|c[−-]b\s+(contrast|대비)"
    r"|\+6\.0\s*pp|[−-]2\.0\s*pp", re.I)
CONFOUND_TERM = re.compile(r"confound|혼입|혼재|교란변수", re.I)
DRAWNOISE_TERM = re.compile(r"draw[- ]?noise|draw\s*잡음|재추첨\s*잡음", re.I)

# (G) D31 0-2 (W3): 교란 프레임 + lower bound/하한 결합 서술 금지 — 교정 문구는 allowlist.
PERTURB_TERM = re.compile(r"perturb|identity.?mask|identity.?blind|교란|정체[- ]?가림", re.I)
LOWER_BOUND_TERM = re.compile(r"lower\s+bound|하한", re.I)
LOWER_BOUND_ALLOW = re.compile(
    r"not a clean lower bound|clean lower bound|하한이 아니|덜 오염|less.?contaminat"
    r"|structural lower bound|구조적 하한", re.I)


# (M) D-P83 / PKT-R2 (R15-5): 철회된 "암기 불가능" 문언의 재유입 금지.
#     서명된 교정 문언은 "선언(declared) 컷오프 이후 폭로 + 실측 비인지"이며,
#     보증의 전제가 벤더 선언(name-pinned endpoint)이므로 논리적 불가능성
#     주장은 근거가 없다. PKT-R2는 README·METHOD·README_DETAIL을 고쳤으나
#     README_DETAIL의 backbone 문단 한 곳을 놓쳤고, 린트에는 이 문언을 잡는
#     규칙이 없어 grep 없이는 드러나지 않았다.
#
#     두 층으로 건다:
#       - 전 DOCS: 철회 문구 그대로의 재유입 (동결 ISSUE 초안 3종의 역사
#         문언 "structurally impossible"과는 구별된다 — 그 파일들은 게시된
#         역사 텍스트라 수정 금지(INV-06)이며 규칙 (J)와 같은 취급이다).
#       - 살아 있는 영어 정본 표면: "memorization/memory … impossible" 결합
#         전반 (구조적 불가능 주장 자체).
#     교정 맥락(철회 사실을 서술하는 문장)은 allowlist로 허용한다.
MEMO_RETRACTED_PHRASE = re.compile(r"memorization\s+is\s+impossible", re.I)
LIVE_CLAIM_DOCS = ["README.md", "METHOD.md", "RESULTS.md", "docs/README_DETAIL.md"]
MEMO_TERM = re.compile(r"memoriz|memory", re.I)
IMPOSSIBLE_TERM = re.compile(r"impossible", re.I)
MEMO_ALLOW = re.compile(
    r"retracted|철회|D-P83|PKT-R2|declared\s+(training\s+)?cutoff|선언\s*컷오프"
    r"|not\s+impossible|cannot\s+be\s+blocked", re.I)


# (J) D100 (RISK_SCORE_SEMANTICS §4): 서수 점수의 확률화 서술 금지.
#     대상 = README 양어·ONE_PAGER + forward 사이클 문서(존재 시). 동결 ISSUE
#     초안 3종은 게시된 역사 텍스트이므로 제외 (수정은 소유자 서명 diff 전용
#     — RP-15/16 선례). 통계 p-값(p=0.0021, p=3.0e-05)은 소수점/지수로 구별.
ORDINAL_DOCS = ["README.md", "README.ko.md", "docs/reader_validation/ONE_PAGER.md"]
P_INT_SCORE = re.compile(r"\bp\s*=\s*\d{1,3}(?![\d.%eE])")
PCT_PROB = re.compile(
    r"\d{1,3}\s*%\s*(?:probability|likelihood|chance|확률|가능성)"
    r"|(?:확률|가능성)\s*[:=약]?\s*\d{1,3}\s*%"
    r"|(?:probability|likelihood|chance)\s+of\s+\d{1,3}\s*%", re.I)
PROB_ALLOW = re.compile(r"not a|does not mean|≠|아니다|아니라|않는다|금지", re.I)

# (L) D106 ④ (task separation): 결과 언어 문단에 태스크 층위 표지 부재 금지.
#     대상 = ORDINAL_DOCS + forward 문서 (동결 ISSUE 초안 3종 제외 — RP-15/16
#     선례). 실용 규칙: 결과 언어(detection/separation/flagged/AUC/FPR/perm p)를
#     포함한 문단(빈 줄 구분 블록)이 태스크 표지(TASK 1/2/3, 태스크, wave-1/2,
#     holdout, E1/E2/E4, baseline 등 코호트 명명)를 하나도 갖지 않으면 위반 —
#     즉 코호트 무명의 합산형 헤드라인만 잡고, 코호트가 명명된 문장은 통과.
RESULTS_TERM = re.compile(
    r"\bAUC\b|\bFPR\b|perm(utation)?\s*p\b|\bdetect(s|ed|ion)\b|\bseparat(es|ion)\b"
    r"|\bflag(ged|s)?\s+\d+\s*/\s*\d+|오탐률|탐지(율|된|한다)|분리(도)?\s*(유의|성)", re.I)
TIER_TOKEN = re.compile(
    r"TASK\s*[123]|\[T[123]\]|태스크\s*[123]|wave-?\s*[12]|웨이브\s*[12]|holdout|홀드아웃"
    r"|\bE[124]\b|\bL[1-4]\b(?![-.])|baseline|베이스라인|pilot|파일럿|mechanical|기계(적)?\s*(스크린|베이스)"
    r"|per-?tier|티어별|Tier\s*[AB]", re.I)


def check_task_tier():
    """(L) 결과 언어 문단의 태스크 층위 표지 검사 — 문단 단위."""
    viols = []
    for path in ordinal_claim_docs():
        text = (REPO / path).read_text(encoding="utf-8")
        offset_ln = 1
        for block in text.split("\n\n"):
            n_lines = block.count("\n") + 1
            # 거버넌스 관용구("task separation"/"태스크 분리")는 결과 언어가 아님
            scan = re.sub(r"task\s+separation|태스크\s*분리", "", block, flags=re.I)
            if RESULTS_TERM.search(scan) and not TIER_TOKEN.search(block):
                viols.append((path, offset_ln,
                              f"(L) 결과 언어 문단에 태스크 층위 표지 부재 (D106 ④): "
                              f"{block.strip().splitlines()[0][:70]}"))
            offset_ln += n_lines + 1
    return viols


# (K) D100 (CLAIM_HIERARCHY §L4): 현 증거 수준에서 무자격 사용 금지 문구.
CLAIM_FORBIDDEN = [
    (r"predicts\s+fraud\s+in\s+public\s+compan", "predicts fraud in public companies"),
    (r"estimates?\s+real-?world\s+fraud\s+probabilit", "estimates real-world fraud probability"),
    (r"validated\s+fraud[- ]detection\s+system", "validated fraud detection system"),
    (r"population-?level\s+performance", "population-level performance"),
    (r"검증된\s*사기\s*탐지\s*시스템", "검증된 사기 탐지 시스템"),
    (r"모집단\s*수준\s*성능", "모집단 수준 성능"),
]
CLAIM_ALLOW = re.compile(r"\bnot\b|cannot|do(es)? not|없|않|금지|아니|Level 4|지원하지", re.I)


def ordinal_claim_docs():
    """규칙 (J)/(K) 대상 문서 — 고정 3종 + forward 사이클 마크다운(존재 시)."""
    paths = [p for p in ORDINAL_DOCS if (REPO / p).exists()]
    paths += sorted(str(p.relative_to(REPO)) for p in REPO.glob("forward/**/*.md"))
    # D106 ⑥: 실무자 브리프(surface/)도 발행 표면 — J/K/L 규칙 적용
    paths += sorted(str(p.relative_to(REPO)) for p in REPO.glob("surface/**/*.md"))
    return paths


def check_ordinal_and_claims():
    viols = []
    for path in ordinal_claim_docs():
        text = (REPO / path).read_text(encoding="utf-8")
        lines = text.splitlines()
        for m in P_INT_SCORE.finditer(text):
            ln = text[:m.start()].count("\n") + 1
            viols.append((path, ln, f"(J) 정수형 p=NN 케이스 점수 인용 금지 (→ 'score NN', "
                                    f"RP-16/D91): {lines[ln-1].strip()[:70]}"))
        for m in PCT_PROB.finditer(text):
            win = text[max(0, m.start() - 120):m.end() + 120]
            if PROB_ALLOW.search(win):
                continue  # 교정 서술("≠ 70% 확률" 등)은 허용
            ln = text[:m.start()].count("\n") + 1
            viols.append((path, ln, f"(J) 서수 점수의 %확률화 서술 금지 "
                                    f"(RISK_SCORE_SEMANTICS §2): {lines[ln-1].strip()[:70]}"))
        for pat, label in CLAIM_FORBIDDEN:
            for m in re.finditer(pat, text, re.I):
                win = text[max(0, m.start() - 120):m.end() + 120]
                if CLAIM_ALLOW.search(win):
                    continue  # 부정·한정 문맥("does not support …")은 허용
                ln = text[:m.start()].count("\n") + 1
                viols.append((path, ln, f"(K) 무자격 주장 문구 금지 '{label}' "
                                        f"(CLAIM_HIERARCHY): {lines[ln-1].strip()[:70]}"))
    return viols


STALE = [
    (r"316\s*파일", "stale manifest count (→ 402)"),
    (r"0%\s*FPR", "0% FPR 금지"),
    (r"FPR\s*[:=]?\s*0%", "0% FPR 금지"),
    (r"무오탐|오탐\s*0%|오탐률\s*0%", "0% 오탐 헤드라인 금지"),
    (r"0\.86\b(?!4)", None),  # 0.86 단독은 wave1 perturbed 0.864 축약 — 정보용(비차단)
]
ADVERSE = re.compile(r"(overstat|misstat|분식|조작|manipulat|fraudulent|허위|은폐)", re.I)


def lint_doc(path):
    viol = []
    text = (REPO / path).read_text(encoding="utf-8")
    low = text.lower()
    lines = text.splitlines()

    # (A) 0% FPR / 무오탐
    for pat, why in [(r"0%\s*fpr", "0% FPR"), (r"무오탐", "무오탐"),
                     (r"오탐\s*0%|오탐률\s*0%", "0% 오탐"), (r"fpr[^\n]{0,12}0\s*%", "FPR 0%")]:
        for m in re.finditer(pat, low):
            ln = low[:m.start()].count("\n") + 1
            viol.append((ln, f"(A) 0% 오탐류 금지: {lines[ln-1].strip()[:80]}"))

    # (B) G2 + fraud word (동일 문장 내)
    for sent in re.split(r"(?<=[.。\n])", text):
        s = sent.lower()
        if any(fw in s for fw in FRAUD_WORDS):
            for tk, names in G2.items():
                if tk.lower() in s or any(n in s for n in names):
                    # provisional/non-reliance 부인 문맥이면 허용
                    if "provisional" in s or "non-reliance" in s or "restatement" in s or "금지" in s or "쓰지 않" in s:
                        continue
                    ln = text[:text.find(sent)].count("\n") + 1
                    viol.append((ln, f"(B) G2 {tk}에 fraud류 서술: {sent.strip()[:80]}"))

    # (C) 대조군 티커가 부정 서술 주어 — 티커 직후 8단어 내 부정 술어
    for tk in controls():
        for m in re.finditer(rf"\b{re.escape(tk)}\b", text):
            tail = text[m.end():m.end()+80]
            if ADVERSE.search(tail) and not re.search(r"오탐|false.positive|대조군|control|근거됨|양성 오독", tail, re.I):
                ln = text[:m.start()].count("\n") + 1
                viol.append((ln, f"(C) 대조군 {tk} 주어+부정술어 의심: …{tail.strip()[:60]}"))

    # (D) pooled without standalone
    if re.search(r"pooled", low) and "standalone" not in low and "병기 전용" not in text and "2차 병기" not in text:
        viol.append((0, "(D) pooled 언급에 standalone 병기 부재"))

    # (E) EXPLORATORY on cross-model / opus evaluatee
    for m in re.finditer(r"(교차모델|cross-?model|opus-4-8|e4\b)", low):
        win = low[max(0, m.start()-120):m.end()+120]
        if "exploratory" not in win:
            ln = low[:m.start()].count("\n") + 1
            viol.append((ln, f"(E) 교차모델/opus 언급에 EXPLORATORY 라벨 부재: {lines[ln-1].strip()[:70]}"))

    # (G) 교란 프레임을 lower bound/하한으로 서술 (±160자 창, allowlist 문구 예외)
    for m in PERTURB_TERM.finditer(text):
        win = text[max(0, m.start() - 160):m.end() + 160]
        if LOWER_BOUND_TERM.search(win) and not LOWER_BOUND_ALLOW.search(win):
            ln = text[:m.start()].count("\n") + 1
            viol.append((ln, f"(G) 교란 프레임+lower bound/하한 결합 서술 금지 (W3): "
                             f"{lines[ln-1].strip()[:70]}"))

    # (M) 철회된 "암기 불가능" 문언의 재유입 (R15-5) — 두 층, 같은 줄은 1건
    seen_m = set()
    for m in MEMO_RETRACTED_PHRASE.finditer(text):
        win = text[max(0, m.start() - 160):m.end() + 160]
        if MEMO_ALLOW.search(win):
            continue
        ln = text[:m.start()].count("\n") + 1
        seen_m.add(ln)
        viol.append((ln, "(M) 철회 문언 재유입 금지 (D-P83/PKT-R2 — 서명된 "
                         f"교정 문언은 선언 컷오프 + 실측 비인지): {lines[ln-1].strip()[:70]}"))
    if path in LIVE_CLAIM_DOCS:
        for m in MEMO_TERM.finditer(text):
            win = text[max(0, m.start() - 120):m.end() + 120]
            if not IMPOSSIBLE_TERM.search(win) or MEMO_ALLOW.search(win):
                continue
            ln = text[:m.start()].count("\n") + 1
            if ln in seen_m:
                continue
            seen_m.add(ln)
            viol.append((ln, "(M) 살아 있는 정본 표면의 암기 불가능성 주장 금지 "
                             "(엔드포인트는 이름 핀이므로 전제가 벤더 선언이다): "
                             f"{lines[ln-1].strip()[:70]}"))

    # (F) stale forbidden
    for pat, why in STALE:
        if why is None:
            continue
        for m in re.finditer(pat, text):
            ln = text[:m.start()].count("\n") + 1
            viol.append((ln, f"(F) stale/금지 '{why}': {lines[ln-1].strip()[:70]}"))

    return viol


# R1-19: 열거 표면 중 어떤 상태에서 부재가 적법한 파일 (현재 없음 — 항목을
# 추가하려면 사유 주석과 함께; 빈 집합이 기본이자 정상이다)
MISSING_ALLOWED: set[str] = set()


def missing_enumerated_surfaces(allowed: set[str] | None = None) -> list[str]:
    """R1-19: DOCS/ORDINAL_DOCS 열거 표면의 부재는 커버리지 침묵 이탈 —
    삭제·개명된 발행 표면이 린트 범위에서 소리 없이 빠지면 안 된다."""
    allowed = MISSING_ALLOWED if allowed is None else allowed
    enumerated = list(dict.fromkeys(DOCS + ORDINAL_DOCS + ["analysis/synthesis.md"]))
    return [p for p in enumerated
            if p not in allowed and not (REPO / p).exists()]


def main():
    total = 0
    for path in missing_enumerated_surfaces():
        print(f"  {path}:0: (R1-19) 열거 발행 표면 부재 — 삭제/개명은 린트 "
              "커버리지 이탈: DOCS 갱신 또는 MISSING_ALLOWED 등재(사유 주석) 필요")
        total += 1
    for path in DOCS:
        if not (REPO / path).exists():
            continue
        v = lint_doc(path)
        for ln, msg in v:
            print(f"  {path}:{ln}: {msg}")
        total += len(v)
    for path, ln, msg in check_canon():
        print(f"  {path}:{ln}: {msg}")
        total += 1
    for path, ln, msg in check_ordinal_and_claims():
        print(f"  {path}:{ln}: {msg}")
        total += 1
    for path, ln, msg in check_task_tier():
        print(f"  {path}:{ln}: {msg}")
        total += 1
    if total:
        print(f"\nFAIL — 발행 정합 위반 {total}건")
        return 1
    print("PASS — 발행 정합 (0% 오탐·G2-fraud·대조군주어·pooled·EXPLORATORY·stale"
          "·canon·서수확률화(J)·주장위계(K)·태스크층위(L)·철회문언(M) 무위반)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
