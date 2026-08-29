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


def test_corrective_context_is_allowlisted(monkeypatch, tmp_path):
    """교정 문맥에서 철회 문구를 **인용**하는 것은 허용된다 — 그러지 않으면
    철회 사실 자체를 서술할 수 없다 (규칙 (G)의 allowlist와 같은 구조).

    R16-3(d): 종전에는 단언이 전부 부정형(`assert not …`)이라 규칙 (M) 자체를
    지워도 green이었다 — 아무것도 고정하지 않았다. 같은 파일·같은 헬퍼로 양성
    대조를 함께 건다: 교정 틀 없이 같은 문구를 단언하면 반드시 red다."""
    viol = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\n" + CORRECTIVE_SENTENCE + "\n")
    assert not [msg for _, msg in viol if "(M)" in msg], viol

    bare = _mutated_copy(tmp_path, monkeypatch, "docs/README_DETAIL.md",
                         "\nHere memorization is impossible.\n")
    assert [msg for _, msg in bare if "(M)" in msg], (
        "규칙 (M)이 살아 있지 않으면 위 allowlist 단언은 아무것도 고정하지 않는다")


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
