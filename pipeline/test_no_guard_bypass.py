"""가드 우회 정적 스캔 (CLAUDE.md 방법론 규율 1: "우회 코드를 작성하지 않는다"의 기계적 강제).

pipeline/ 안의 모듈(피평가자 쪽 코드)은 cutoff_guard를 제외하고:
  1. 네트워크 라이브러리를 직접 import할 수 없다 — 모든 원격 로딩은
     load_document(loader=...) 콜백 주입으로만.
  2. candidates.json을 직접 참조할 수 없다 — 이 파일은 ground truth
     (scheme_summary, AAER 링크 등 정답지)를 포함하므로, 피평가자 코드가
     읽는 순간 look-ahead와 무관하게 백테스트가 오염된다.
     (cutoff_guard.load_registry는 컷오프 날짜만 추출해 노출 — 유일한 예외.)

규범이 아니라 테스트다: 위반 코드는 커밋 전에 여기서 깨진다.
"""
import ast
import re
from pathlib import Path

import pytest

from test_all_raw_reads_enforced import CORPUS_ROOT_NAMES, _raw_read_functions

PIPELINE_DIR = Path(__file__).resolve().parent
EXEMPT = {"cutoff_guard.py"}  # 게이트웨이 본체만 예외

FORBIDDEN_PATTERNS = {
    "network import": re.compile(
        r"^\s*(import|from)\s+(requests|urllib|http\.client|httpx|aiohttp|socket)\b", re.M
    ),
    "candidates.json direct reference": re.compile(r"candidates\.json"),
    # 중립 ID ↔ 원본 매핑은 채점 전용(OV-001) — 피평가자 코드가 읽으면 그룹 소속 역산 가능
    # R2-27: 웨이브 변형(id_mapping_wave2/_v2/_pilot…)까지 전부 — \w* 확장
    "id_mapping direct reference": re.compile(r"id_mapping\w*\.json"),
    # V7 (threat model): 피평가자 쪽 코드는 채점 모듈을 import할 수 없다 — 채점 자료
    # (정답 키·루브릭)의 역류 차단. 경로 문자열 언급(출력 저장 등)은 허용, import만 금지.
    "scoring import": re.compile(r"^\s*(import\s+scoring|from\s+scoring)\b", re.M),
    "raw aaer-data read": re.compile(r"aaer-data"),
}


# "raw aaer-data read" 규칙은 리터럴 문자열만 본다 — build_payload.py는 코퍼스 루트를
# 심볼(DATA_DIR = cutoff_guard.DEFAULT_EDGAR_DATA)로 들고 있어서 파일 어디에도
# 'aaer-data' 리터럴이 없다. R16-1(e): 리터럴에 의존하지 않는 두 번째 층 —
# 코퍼스 루트를 가리키는 *이름*을 소스에서 유도한 뒤 원시 읽기 호출을 찾는다.
CORPUS_ROOT_ATTRS = frozenset({"DEFAULT_EDGAR_DATA"})
CORPUS_ROOT_LITERAL = "aaer-data"


def corpus_root_aliases(source: str) -> set[str]:
    """코퍼스 루트로 바인딩된 이름 전부 — 리터럴 경로든 import한 심볼이든."""
    tree = ast.parse(source)
    aliases = set(CORPUS_ROOT_NAMES)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets, value = node.targets, node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            else:
                continue
            reaches_root = any(
                (isinstance(n, ast.Attribute) and n.attr in CORPUS_ROOT_ATTRS)
                or (isinstance(n, ast.Name) and n.id in (CORPUS_ROOT_ATTRS | aliases))
                or (isinstance(n, ast.Constant) and isinstance(n.value, str)
                    and CORPUS_ROOT_LITERAL in n.value)
                for n in ast.walk(value))
            if not reaches_root:
                continue
            for target in targets:
                for name in (n.id for n in ast.walk(target) if isinstance(n, ast.Name)):
                    if name not in aliases:
                        aliases.add(name)
                        changed = True
    return aliases


def corpus_reads_via_root(source: str) -> list[str]:
    return _raw_read_functions(source, roots=corpus_root_aliases(source))


# 양성 대조: 'aaer-data' 리터럴이 한 번도 나오지 않는데도 코퍼스를 직접 읽는 모듈.
IMPORTED_ROOT_SOURCE = '''
import json
import os

import cutoff_guard

CORPUS = cutoff_guard.DEFAULT_EDGAR_DATA


def load_pit_series(ticker, cutoff):
    for name in os.listdir(CORPUS / ticker / "xbrl"):
        data = json.load(open(CORPUS / ticker / "xbrl" / name))
'''


def test_imported_corpus_root_read_is_flagged_without_the_literal():
    # 기존 리터럴 규칙은 이 소스를 못 잡는다 — 그래서 두 번째 층이 필요하다.
    assert not FORBIDDEN_PATTERNS["raw aaer-data read"].search(IMPORTED_ROOT_SOURCE)
    assert "CORPUS" in corpus_root_aliases(IMPORTED_ROOT_SOURCE)
    assert corpus_reads_via_root(IMPORTED_ROOT_SOURCE) == ["load_pit_series"]


def test_pipeline_modules_do_not_read_the_corpus_root_directly():
    violations = {path.name: corpus_reads_via_root(path.read_text(encoding="utf-8"))
                  for path in scannable_sources()}
    assert not {k: v for k, v in violations.items() if v}


def scannable_sources():
    for p in sorted(PIPELINE_DIR.glob("*.py")):
        if p.name in EXEMPT or p.name.startswith("test_"):
            continue
        yield p


@pytest.mark.parametrize(("label", "source"), [
    ("network import", "import requests\n"),
    ("candidates.json direct reference", 'Path("candidates.json").read_text()\n'),
    ("id_mapping direct reference", 'open("id_mapping.json")\n'),
    # R2-27 양성 대조: 웨이브 변형 파일명도 스캔에 걸린다
    ("id_mapping direct reference", 'open("scoring/id_mapping_wave2.json")\n'),
    ("id_mapping direct reference", 'open("scoring/id_mapping_v2.json")\n'),
    ("scoring import", "from scoring import rubric\n"),
    ("raw aaer-data read", 'Path("/tmp/aaer-data/raw.pdf").read_bytes()\n'),
])
def test_forbidden_patterns_have_positive_controls(label, source):
    assert FORBIDDEN_PATTERNS[label].search(source), label


def test_pipeline_modules_do_not_bypass_guard():
    violations = []
    for path in scannable_sources():
        source = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            for m in pattern.finditer(source):
                line_no = source[: m.start()].count("\n") + 1
                violations.append(f"{path.name}:{line_no} [{label}] {m.group(0).strip()}")
    assert not violations, (
        "cutoff_guard 우회 의심 코드 발견 — load_document(loader=...) 경유로 수정할 것:\n"
        + "\n".join(violations)
    )
