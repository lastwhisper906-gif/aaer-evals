"""R1-19: lint_publication — 열거 발행 표면 부재의 fail-closed."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_publication as lp


def test_real_tree_has_no_missing_enumerated_surface():
    assert lp.missing_enumerated_surfaces() == []


def test_renamed_surface_is_named(monkeypatch):
    monkeypatch.setattr(lp, "DOCS", lp.DOCS + ["analysis/RENAMED_AWAY.md"])
    missing = lp.missing_enumerated_surfaces()
    assert missing == ["analysis/RENAMED_AWAY.md"]


def test_allowlist_parameter_exempts_explicitly(monkeypatch):
    monkeypatch.setattr(lp, "DOCS", lp.DOCS + ["analysis/RENAMED_AWAY.md"])
    assert lp.missing_enumerated_surfaces(
        allowed={"analysis/RENAMED_AWAY.md"}) == []


def test_ordinal_docs_covered_too(monkeypatch):
    monkeypatch.setattr(lp, "ORDINAL_DOCS", lp.ORDINAL_DOCS + ["surface/GONE.md"])
    assert "surface/GONE.md" in lp.missing_enumerated_surfaces()


REAL_REPO = lp.REPO   # lp.REPO는 아래 헬퍼가 monkeypatch하므로 원본을 붙잡아 둔다


def _mutated_copy(tmp_path, monkeypatch, rel, added):
    """DOCS 파일 하나만 변이해 놓은 임시 트리 — 현재 트리는 건드리지 않는다.

    R16-3(d): 종전에는 `lp.CONTROL_TICKERS`가 **형제 테스트가 이미 채워 둔**
    모듈 전역이라, 이 헬퍼를 쓰는 테스트를 단독 실행하면 대조군 CSV를 임시
    트리에서 찾다 FileNotFoundError로 죽었다 — 즉 green이 잠금이 아니라 실행
    순서의 부산물이었다. 임시 트리에 CSV를 함께 복사하고 캐시를 비워, 어느
    순서로 돌려도 같은 판정이 나오게 한다."""
    doc = tmp_path / rel
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text((REAL_REPO / rel).read_text(encoding="utf-8") + added,
                   encoding="utf-8")
    table = tmp_path / "analysis" / "unified_table.csv"
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text(
        (REAL_REPO / "analysis/unified_table.csv").read_text(encoding="utf-8"),
        encoding="utf-8")
    monkeypatch.setattr(lp, "CONTROL_TICKERS", None)
    monkeypatch.setattr(lp, "REPO", tmp_path)
    return lp.lint_doc(rel)


def test_retracted_memorization_wording_is_locked_on_every_doc(monkeypatch, tmp_path):
    """R15-5: D-P83/PKT-R2가 철회한 문언이 어느 발행 표면으로도 되돌아오지
    못한다. 종전에는 규칙이 없어 린트가 0을 반환했고, README_DETAIL의 backbone
    문단에 한 건이 남아 있는 것을 리뷰 시점 grep으로만 알 수 있었다."""
    assert lp.lint_doc("docs/README_DETAIL.md") == []      # 현재 트리는 green
    viol = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\nDetection persists where memorization is impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol


def test_retracted_phrase_layer_covers_frozen_drafts_too(monkeypatch, tmp_path):
    """전 DOCS 층은 동결 초안에도 적용된다 — 그 파일들의 **기존** 역사 문언
    ("structurally impossible")과는 구별되는 정확 문구만 잡기 때문에 동결
    텍스트를 붉히지 않으면서 재유입은 막는다."""
    assert lp.lint_doc("analysis/ISSUE_0_DRAFT.md") == []  # 역사 문언은 green
    viol = _mutated_copy(tmp_path, monkeypatch, "analysis/ISSUE_0_DRAFT.md",
                         "\nHere memorization is impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol


def test_live_surface_also_rejects_the_structural_form(monkeypatch, tmp_path):
    """살아 있는 영어 정본 4종에는 결합 전반을 건다 — 문구를 바꿔 적은
    구조적 불가능성 주장도 막아야 잠금이 문자열 매칭에 그치지 않는다.
    동결 초안 3종은 게시된 역사 텍스트이므로 이 층에서 제외한다(규칙 (J) 선례,
    INV-06) — 그래서 같은 문장이 초안 사본에서는 잡히지 않는다."""
    viol = _mutated_copy(tmp_path, monkeypatch, "METHOD.md",
                         "\nIn the holdout tier memorization is structurally impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol

    viol = _mutated_copy(tmp_path, monkeypatch, "analysis/ISSUE_2_HOLDOUT_DRAFT.md",
                         "\nIn the holdout tier memorization is structurally impossible.\n")
    assert not [msg for _, msg in viol if "(M)" in msg], viol


CORRECTIVE_SENTENCE = (
    "The earlier wording — memorization is impossible — was retracted "
    "(D-P83): the endpoint is name-pinned, so the premise was a vendor "
    "declaration.")

# R16-3(a): 철회 문언을 교정 어휘와 **함께** 다시 단언하는 형태. 종전
# allowlist는 주제어로 열렸으므로 20/20 DOCS에서 전부 통과했다.
REASSERTIONS = [
    ("README.md",
     "Because the revelation postdates the declared cutoff, "
     "memorization is impossible."),
    ("docs/README_DETAIL.md",
     "Because the revelation postdates the declared cutoff, "
     "memorization is impossible."),
    ("METHOD.md",
     "The retracted wording stands: memorization is impossible here."),
    ("RESULTS.md",
     "Memorization is impossible for the holdout tier; "
     "the event is not impossible to verify."),
]


@pytest.mark.parametrize("rel,sentence", REASSERTIONS,
                         ids=[r for r, _ in REASSERTIONS])
def test_retracted_claim_cannot_be_reasserted_alongside_corrective_vocabulary(
        monkeypatch, tmp_path, rel, sentence):
    """R16-3(a): 교정 어휘를 곁들인 재단언은 통과하면 안 된다.

    R15-5의 잠금은 allowlist가 **주제어**(retracted·declared cutoff·D-P83)로
    열렸기 때문에, 철회된 문장을 그 어휘와 함께 그대로 다시 쓰면 exit 0이었다 —
    잠금이 열리는 방향이 하필 철회 문언을 되살리는 방향이었다."""
    viol = _mutated_copy(tmp_path, monkeypatch, rel, "\n" + sentence + "\n")
    assert [msg for _, msg in viol if "(M)" in msg], (rel, viol)


# ── D-P101 (i): 교정 논의의 자리는 문장이 아니라 문서 구조다 ────────────────
# 종전 테스트(test_corrective_context_is_allowlisted)는 CORRECTIVE_SENTENCE가
# **산문 그대로** 통과할 것을 고정했다. 서명된 결정이 그 성질을 폐기했으므로
# 테스트는 삭제가 아니라 새 성질로 **교체**된다: 같은 문장이 산문에서는 red이고
# 구조적 자리 안에서는 pass다. 네 번 뚫린 자리가 "문장에 무엇을 적었는가"였기
# 때문에, 이제 판정은 문장을 읽지 않는다.

RETRACTION_MARKER = "<!-- RETRACTED-QUOTE -->\n{}\n<!-- /RETRACTED-QUOTE -->"
CODE_FENCE_QUOTE = "```text\n{}\n```"


def test_corrective_prose_is_no_longer_exempt(monkeypatch, tmp_path):
    """(a) 근접창 allowlist 삭제 — 교정 어휘를 갖춘 산문도 이제 red다."""
    viol = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\n" + CORRECTIVE_SENTENCE + "\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol


@pytest.mark.parametrize("template", [RETRACTION_MARKER, CODE_FENCE_QUOTE],
                         ids=["explicit_marker", "code_fence"])
def test_a_structural_place_carries_the_retraction_instead(monkeypatch, tmp_path,
                                                           template):
    """(a) 철회 사실은 여전히 서술 가능하다 — 구조적 자리 안에서."""
    viol = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\n" + template.format(CORRECTIVE_SENTENCE) + "\n")
    assert not [msg for _, msg in viol if "(M)" in msg], viol

    bare = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\nHere memorization is impossible.\n")
    assert [msg for _, msg in bare if "(M)" in msg], (
        "규칙 (M)이 살아 있지 않으면 위 단언은 아무것도 고정하지 않는다")


# (b) 리뷰·verdict 어디에도 이름이 없는, 이 커밋에서 생성한 우회 시도.
# 생성 규칙: 종전 allowlist의 **각 분기**를 하나씩 열쇠로 삼아 재단언과 한
# 문장에 넣는다 + 마커를 흉내 내되 정확히 일치하지는 않게 쓴다.
GENERATED_EVASIONS = [
    ("README.md",
     "문구가 철회되었습니다. 그래도 memorization is impossible 은 유지된다."),
    ("METHOD.md",
     "We no longer assert the following, which nevertheless holds: "
     "memorization is impossible."),
    ("RESULTS.md",
     "Withdrawn the above — yet memory of these filings is impossible."),
    ("docs/README_DETAIL.md",
     "The phrase was retracted; memorization is impossible nonetheless."),
    ("README.md",
     "<!-- retracted quote -->\nmemorization is impossible\n<!-- /retracted quote -->"),
]


@pytest.mark.parametrize("rel,sentence", GENERATED_EVASIONS,
                         ids=[str(i) for i in range(len(GENERATED_EVASIONS))])
def test_generated_evasions_are_all_flagged(monkeypatch, tmp_path, rel, sentence):
    viol = _mutated_copy(tmp_path, monkeypatch, rel, "\n" + sentence + "\n")
    assert [msg for _, msg in viol if "(M)" in msg], (rel, viol)


def test_an_unclosed_marker_does_not_exempt_the_rest_of_the_document(
        monkeypatch, tmp_path):
    """구간을 열어 둔 채 재단언을 뒤에 붙이는 것이 이 설계의 유일한 우회다."""
    viol = _mutated_copy(
        tmp_path, monkeypatch, "docs/README_DETAIL.md",
        "\n<!-- RETRACTED-QUOTE -->\nHere memorization is impossible.\n")
    assert [msg for _, msg in viol if "(M)" in msg], viol


def test_readme_detail_is_linted_surface_and_g2_rule_bites(monkeypatch, tmp_path):
    """R7-12: README:179가 연결하는 상세 서사도 발행 표면 — DOCS 편입을 잠그고,
    G2-위반 문장이 실제로 red가 됨을 변이 사본으로 증명 (현재 트리는 green)."""
    assert "docs/README_DETAIL.md" in lp.DOCS
    assert lp.lint_doc("docs/README_DETAIL.md") == []
    doc = tmp_path / "docs" / "README_DETAIL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        (lp.REPO / "docs/README_DETAIL.md").read_text(encoding="utf-8")
        + "\nHub Group fraud indicators are clear.\n", encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    viol = lp.lint_doc("docs/README_DETAIL.md")
    assert any("(B) G2" in msg for _, msg in viol), viol


# ── R17-4: 규칙 (G)는 양방향으로 무력했다 ────────────────────────────────────
# (1) 규칙 전체에 테스트가 하나도 없었다 — LOWER_BOUND_TERM을 절대 매칭되지 않는
#     패턴으로 바꿔 규칙을 통째로 무력화해도 0 red(788 passed)였다.
# (2) allowlist가 **강화된** 주장을 흘렸다 — `clean lower bound`·`structural
#     lower bound`·`구조적 하한`·`덜 오염`·`less.?contaminat`가 맨 긍정 분기라,
#     "교란 프레임의 결과는 탐지력의 clean lower bound이다"가 11/11 DOCS에서
#     통과했다. 세 분기는 D31 0-2 교정문 **자신의 어휘**다.
#
# 아래 코퍼스는 리터럴 목록이 아니라 **LOWER_BOUND_ALLOW의 분기에서 실행 시점에
# 파생**된다. 맨 긍정 분기를 추가하면 테스트를 한 줄도 고치지 않아도 적색이 된다.

def _g_probe(literal: str) -> str:
    """교란 프레임 + 하한 + 그 분기를 한 문장에 담는다 — (G)의 발화 조건 그대로."""
    return (f"\n교란(perturbed) 프레임의 결과는 탐지력의 lower bound 이다 "
            f"— {literal}.\n")


def _g_violations(monkeypatch, tmp_path, rel, added):
    return [msg for _, msg in _mutated_copy(tmp_path, monkeypatch, rel, added)
            if "(G)" in msg]


G_ALLOW_BRANCHES = lp.alternation_branches(lp.LOWER_BOUND_ALLOW.pattern)


def test_rule_g_allowlist_has_branches_to_check():
    assert G_ALLOW_BRANCHES, "분기 분해가 비어 있으면 아래 테스트들이 공회전한다"


@pytest.mark.parametrize("branch", G_ALLOW_BRANCHES)
def test_every_rule_g_allow_branch_is_corrective_by_its_own_text(branch):
    """(a): 분기는 자기 텍스트만으로 부정 또는 홀드아웃 귀속이어야 한다.

    맨 긍정어(`clean lower bound`·`구조적 하한`·`덜 오염`)는 어느 쪽도 아니므로
    분기가 될 수 없다 — allowlist에 열쇠를 **추가하는 능력** 자체가 사라진다."""
    assert lp.lower_bound_allow_branch_is_corrective(branch), branch


# 종전 allowlist에 실제로 들어 있던 맨 긍정 분기들 — 술어의 **음성 대조**다.
# 이것이 없으면 술어를 항상 True로 바꿔도 0 red다(실측): 현재 분기가 모두 교정형
# 이라 아래 파라미터화의 else 가지가 한 번도 실행되지 않기 때문이다.
G_HISTORICAL_BARE_AFFIRMATIVE = [
    "clean\\s+lower\\s+bound", "structural\\s+lower\\s+bound",
    "구조적\\s+하한", "덜\\s+오염", "less.?contaminat",
]


@pytest.mark.parametrize("branch", G_HISTORICAL_BARE_AFFIRMATIVE)
def test_bare_affirmative_branches_are_rejected_by_the_predicate(branch):
    """(a) 음성 대조: 교정문 자신의 어휘라도 맨 긍정어는 분기가 될 수 없다."""
    assert not lp.lower_bound_allow_branch_is_corrective(branch), branch


@pytest.mark.parametrize("branch",
                         G_ALLOW_BRANCHES + G_HISTORICAL_BARE_AFFIRMATIVE)
def test_rule_g_corpus_is_derived_from_the_allowlist(monkeypatch, tmp_path, branch):
    """(b): 프로브 문장을 분기에서 파생해 판정한다.

    교정 분기면 통과해야 하고(그래야 철회 사실을 서술할 수 있다), 교정 분기가
    아니면 반드시 걸려야 한다. 맨 긍정 분기를 넣으면 후자 가지가 적색이 된다."""
    literal = lp.allow_branch_literal(branch)
    viol = _g_violations(monkeypatch, tmp_path, "METHOD.md", _g_probe(literal))
    if lp.lower_bound_allow_branch_is_corrective(branch):
        assert not viol, (branch, viol)
    else:
        assert viol, (branch, "맨 긍정 분기가 (G)를 열었다")


# (d) 리뷰가 실측한 네 문장 — 종전에는 0/11 DOCS에서 걸렸다.
G_AFFIRMATIVE_SENTENCES = [
    "\n교란(perturbed) 프레임의 결과는 탐지력의 clean lower bound 이다.\n",
    "\nThe identity-masked arm yields a structural lower bound on detection.\n",
    "\n정체-가림 조건의 수치는 탐지력의 구조적 하한 이다.\n",
    "\nBecause the perturbed frame is less contaminated, its score is a lower bound.\n",
    # 대조(원래도 걸리던 형태) — 규칙이 살아 있음을 확인한다
    "\nThe perturbed arm gives a lower bound on detection.\n",
]


@pytest.mark.parametrize("sentence", G_AFFIRMATIVE_SENTENCES,
                         ids=[str(i) for i in range(len(G_AFFIRMATIVE_SENTENCES))])
def test_strengthened_lower_bound_claim_is_flagged(monkeypatch, tmp_path, sentence):
    assert _g_violations(monkeypatch, tmp_path, "METHOD.md", sentence), sentence


def test_rule_g_still_fires_on_the_plain_form(monkeypatch, tmp_path):
    """(d) LOWER_BOUND_TERM 무력화가 적색이 되게 하는 최소 잠금."""
    assert _g_violations(monkeypatch, tmp_path, "README.md",
                         "\n교란 프레임은 능력의 하한 이다.\n")


def test_genuinely_corrective_passages_stay_pass():
    """(c) 트리에 이미 있는 정직한 철회 문면은 그대로 통과한다."""
    for rel in ("docs/methodology_limitations.md", "docs/README_DETAIL.md",
                "RESULTS.md", "RESULTS.ko.md", "README.ko.md"):
        viol = [msg for _, msg in lp.lint_doc(rel) if "(G)" in msg]
        assert not viol, (rel, viol)


# ── R17-5 (f): 커밋·태그 날짜를 순서/봉인의 증거로 파는 문면 금지 (규칙 N) ──
# surface/의 실무자 브리프 두 종은 git/GitHub 커밋·태그 타임스탬프를 사전 등록과
# 봉인의 증거로 팔고 있었다. specs/FORWARD_WATCHLIST_V1.md의 서명된 2026-08-28
# 개정이 그 값을 **클라이언트 제출**로 규정하고 태그 API를 앵커에서 제외했으며,
# verify_blindness는 날짜를 하나도 읽지 않는다(merge-base --is-ancestor). 규칙이
# DOCS가 아니라 ordinal_claim_docs()에 걸리는 이유는 surface/가 DOCS 밖이라
# 어떤 린트도 그 표면을 보지 않았기 때문이다 — 그것이 이 결함이 남은 이유다.

DATE_EVIDENCE_REINSTATEMENTS = [
    "\nThe pre-registration is git-commit-timestamped, which is the evidence.\n",
    "\nSealed on 2026-11-15 (GitHub server timestamp anchor).\n",
    "\n사전 등록은 git 커밋 타임스탬프로 증빙된다.\n",
    "\n봉인 시각의 앵커는 GitHub 서버 타임스탬프다.\n",
]


@pytest.mark.parametrize("sentence", DATE_EVIDENCE_REINSTATEMENTS,
                         ids=[str(i) for i in range(len(DATE_EVIDENCE_REINSTATEMENTS))])
def test_date_as_ordering_evidence_is_flagged(sentence):
    viol = lp.date_as_evidence_violations("surface/BRIEF.md", sentence)
    assert viol, sentence


@pytest.mark.parametrize("sentence", [
    # 강등·부정 문면은 허용돼야 한다 — 그러지 않으면 이 사실 자체를 쓸 수 없다
    "\nCommit and tag dates are client-submitted (GIT_COMMITTER_DATE) and are "
    "not the evidence of pre-registration.\n",
    "\nGitHub push 기록은 보조 증거이며 커밋 타임스탬프는 앵커에서 제외한다 "
    "(사전 등록의 증거가 아니다).\n",
])
def test_demoting_or_negating_context_is_allowed(sentence):
    assert not lp.date_as_evidence_violations("surface/BRIEF.md", sentence)


def test_rule_n_is_wired_to_the_surface_briefs_not_only_to_DOCS():
    """이 규칙이 보는 집합에 surface/ 브리프가 실제로 들어 있어야 한다."""
    docs = lp.ordinal_claim_docs()
    assert "surface/BRIEF.md" in docs and "surface/BRIEF_KR.md" in docs
    assert "surface/BRIEF.md" not in lp.DOCS


def test_live_briefs_carry_no_date_as_evidence_claim():
    for rel in ("surface/BRIEF.md", "surface/BRIEF_KR.md"):
        text = (lp.REPO / rel).read_text(encoding="utf-8")
        assert not lp.date_as_evidence_violations(rel, text), rel


def test_live_briefs_name_the_mechanism_the_repo_actually_runs():
    """(e): 철회된 근거를 뺀 자리에 실제 기제가 들어와 있어야 한다."""
    en = (lp.REPO / "surface/BRIEF.md").read_text(encoding="utf-8")
    kr = (lp.REPO / "surface/BRIEF_KR.md").read_text(encoding="utf-8")
    for text in (en, kr):
        assert "merge-base --is-ancestor" in text
        assert "OpenTimestamps" in text


def test_rule_n_is_wired_into_the_linter_not_only_callable(monkeypatch, tmp_path):
    """규칙 (N)이 `check_ordinal_and_claims`를 통해 실제로 돈다.

    함수만 직접 부르는 테스트는 배선을 고정하지 못한다 — 실측으로,
    lint_doc/check_ordinal_and_claims에서 (N) 호출을 떼어내도 0 red였다.
    이 테스트가 그 구멍을 닫는다."""
    surface = tmp_path / "surface"
    surface.mkdir()
    (surface / "BRIEF.md").write_text(
        "# brief\n\nThe pre-registration is git-commit-timestamped, which is "
        "the evidence.\n", encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    monkeypatch.setattr(lp, "ORDINAL_DOCS", [])
    viols = lp.check_ordinal_and_claims()
    assert [m for _, _, m in viols if "(N)" in m], viols


def test_rule_n_wired_path_is_clean_on_the_real_tree():
    viols = [(p, m) for p, _, m in lp.check_ordinal_and_claims() if "(N)" in m]
    assert not viols, viols


# ── R18-5: 열한 개 규칙에 양성 대조를 준다 ──────────────────────────────────
# 측정된 사실: 아래 열한 규칙은 각각 정규식 하나를 무력화해도 스위트가 전부
# 초록이었다. 같은 파일의 (G)/LOWER_BOUND_TERM은 19 red다 — 모듈이 도달
# 불가능한 것이 아니라, cycle 15–17이 디스패치한 네 규칙에만 테스트가 있었다.
# 규칙이 존재한다는 것과 규칙이 잠겨 있다는 것은 다른 사실이고, 11월 봉인
# 표면을 지키는 것은 뒤쪽이다.

PAD = "\n" + ("." * 200) + "\n"   # ±120자 창을 실제 문서 꼬리에서 떼어 놓는다


def _plant(tmp_path, monkeypatch, rel, sentence):
    return _mutated_copy(tmp_path, monkeypatch, rel, PAD + sentence + PAD)


def _adverse_control_sentence():
    """(C) 대조군 티커 + 부정 술어 — 티커는 실제 대조군 표에서 가져온다."""
    return f"{sorted(lp.controls())[0]} overstated its reported revenue."


LINT_DOC_CONTROLS = [
    ("A", "README.md", "We report 0% FPR on this cohort."),
    ("D", "METHOD.md", "The pooled figure is given here."),
    ("E", "README.md", "The cross-model arm is summarised here."),
]


@pytest.mark.parametrize("rule,rel,sentence", LINT_DOC_CONTROLS,
                         ids=[r for r, _, _ in LINT_DOC_CONTROLS])
def test_lint_doc_rule_has_a_positive_control(monkeypatch, tmp_path, rule, rel,
                                              sentence):
    viol = _plant(tmp_path, monkeypatch, rel, sentence)
    assert [m for _, m in viol if f"({rule})" in m], (rule, viol)


def test_rule_c_has_a_positive_control(monkeypatch, tmp_path):
    viol = _plant(tmp_path, monkeypatch, "README.md", _adverse_control_sentence())
    assert [m for _, m in viol if "(C)" in m], viol


ORDINAL_CONTROLS = [
    ("J", "The case scored p=70 in the table."),
    ("J", "This corresponds to a 70% probability of misstatement."),
    ("K", "This is a validated fraud-detection system."),
]


@pytest.mark.parametrize("rule,sentence", ORDINAL_CONTROLS,
                         ids=["J_int_score", "J_pct_prob", "K_unqualified"])
def test_ordinal_and_claim_rule_has_a_positive_control(monkeypatch, tmp_path,
                                                       rule, sentence):
    doc = tmp_path / "README.md"
    doc.write_text(PAD + sentence + PAD, encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    monkeypatch.setattr(lp, "ORDINAL_DOCS", ["README.md"])
    viols = lp.check_ordinal_and_claims()
    assert [m for _, _, m in viols if f"({rule})" in m], (rule, viols)


# (L)의 결과 언어는 대안이 여럿이다. 한 문장이 여러 대안에 동시에 걸리면
# 그 문장은 어느 대안도 고정하지 못한다 — 실측으로, `\bAUC\b` 계열만 무력화한
# 변이가 0 red였다(같은 문장의 `separation`이 대신 발화). 대안마다 그 대안
# **하나만** 건드리는 문장을 쓴다.
L_RESULT_LANGUAGE = [
    ("auc", "The AUC is 0.83 for this cohort."),
    ("separation", "The separation is clear."),
    ("detection", "The detection held up."),
    ("perm_p", "The perm p is small."),
    ("fpr_ko", "오탐률은 낮았다."),
]


@pytest.mark.parametrize("label,sentence", L_RESULT_LANGUAGE,
                         ids=[lbl for lbl, _ in L_RESULT_LANGUAGE])
def test_rule_l_has_a_positive_control(monkeypatch, tmp_path, label, sentence):
    """(L) 코호트 무명의 결과 언어 문단."""
    doc = tmp_path / "README.md"
    doc.write_text(f"# t\n\n{sentence}\n", encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    monkeypatch.setattr(lp, "ORDINAL_DOCS", ["README.md"])
    viols = lp.check_task_tier()
    assert [m for _, _, m in viols if "(L)" in m], (label, viols)


def _canon_tree(tmp_path, monkeypatch, readme_text=None, readme_ko_text=None):
    for rel in ("analysis/results_stats.json", "analysis/wave2_results.json"):
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text((REAL_REPO / rel).read_text(encoding="utf-8"),
                       encoding="utf-8")
    for rel, override in (("README.md", readme_text),
                          ("README.ko.md", readme_ko_text)):
        text = (REAL_REPO / rel).read_text(encoding="utf-8")
        (tmp_path / rel).write_text(override if override is not None else text,
                                    encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    monkeypatch.setattr(lp, "DOCS", ["README.md", "README.ko.md"])
    return lp.check_canon()


def test_canon_drift_has_a_positive_control(monkeypatch, tmp_path):
    """정본 수치 하나가 README에서 사라지면 드리프트로 잡힌다."""
    text = (REAL_REPO / "README.md").read_text(encoding="utf-8")
    dropped = lp.canon()["wave2_auc"][0]
    viols = _canon_tree(tmp_path, monkeypatch,
                        readme_text=text.replace(dropped, "0.999"))
    assert [m for _, _, m in viols if "canon drift" in m], viols


def test_rule_h_has_a_positive_control(monkeypatch, tmp_path):
    """(H) E1을 다루면서 GRDX·78 co-presence가 없는 README."""
    text = (REAL_REPO / "README.md").read_text(encoding="utf-8")
    viols = _canon_tree(tmp_path, monkeypatch,
                        readme_text=text.replace("GRDX", "XXXX"))
    assert [m for _, _, m in viols if "(H)" in m], viols


def test_rule_i_has_a_positive_control(monkeypatch, tmp_path):
    """(I) 3-arm delta 언급에 confound·draw-noise 단서가 없는 표면."""
    doc = tmp_path / "README.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# t\n\nThe arm gap is +6.0 pp overall.\n", encoding="utf-8")
    (tmp_path / "README.ko.md").write_text("# t\n", encoding="utf-8")
    for rel in ("analysis/results_stats.json", "analysis/wave2_results.json"):
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text((REAL_REPO / rel).read_text(encoding="utf-8"),
                       encoding="utf-8")
    monkeypatch.setattr(lp, "REPO", tmp_path)
    monkeypatch.setattr(lp, "DOCS", ["README.md"])
    viols = lp.check_canon()
    assert [m for _, _, m in viols if "(I)" in m], viols


# ── R18-5 (b): allowlist는 빈 대안 하나로 조용히 열려서는 안 된다 ───────────
# (G)에서 cycle 017이 건 제약을, 디스패치되지 않아 남아 있던 두 allowlist에
# 같은 형태로 적용한다: 분기 목록에 빈 문자열 분기가 있으면 그 정규식은 모든
# 것을 통과시키므로, 규칙이 사라진 것과 같은데 아무도 붉어지지 않는다.

@pytest.mark.parametrize("name", ["PROB_ALLOW", "CLAIM_ALLOW"])
def test_allow_regex_has_no_empty_branch(name):
    branches = lp.alternation_branches(getattr(lp, name).pattern, keep_empty=True)
    assert branches, name
    assert all(b.strip() for b in branches), (name, branches)
    assert not any(lp.allow_branch_is_vacuous(b) for b in branches), (name, branches)


@pytest.mark.parametrize("name", ["PROB_ALLOW", "CLAIM_ALLOW"])
def test_an_empty_alternative_is_detected_as_vacuous(name):
    """빈 대안을 앞에 붙이는 것이 그 규칙을 여는 방법이었다."""
    opened = "|" + getattr(lp, name).pattern
    branches = lp.alternation_branches(opened, keep_empty=True)
    assert any(lp.allow_branch_is_vacuous(b) for b in branches), branches
