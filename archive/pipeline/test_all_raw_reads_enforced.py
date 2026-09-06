"""벌크 corpus 읽기 게이트웨이의 정적·행동 계약."""
import ast
import datetime
import json
from pathlib import Path

import pytest

import build_payload
import cutoff_guard
import payload_v2_extract


PIPELINE = Path(__file__).resolve().parent


# 오염(taint) 시드 — 코퍼스 루트를 가리키는 이름.
CORPUS_ROOT_NAMES = frozenset({"DATA_DIR", "data_dir"})
# 코퍼스 루트를 내주는 **속성** 이름. `cutoff_guard.DEFAULT_EDGAR_DATA`처럼 인라인
# 속성 접근으로 쓰이든, `from cutoff_guard import DEFAULT_EDGAR_DATA`로 모듈에
# 바인딩되든 같은 객체에 닿는다 — 두 형태를 같은 시드로 본다 (R17-2 (a)(iii)).
CORPUS_ROOT_ATTRS = frozenset({"DEFAULT_EDGAR_DATA"})
# 리터럴 경로로 코퍼스에 닿는 세 번째 바인딩 경로.
CORPUS_ROOT_LITERAL = "aaer-data"

# 매칭되는 원시 읽기 형태. R16-1 이전 판은 {read_text, open, load}를 *속성 호출로만*
# 봤고, 그래서 read_bytes·iterdir·builtin open(path)·json.load(open(path))이 전부
# 통과했다 — build_payload.py에 실제 가드 우회를 주입해도 0 red였다.
# R17-2: 열거(enumeration)도 읽기다 — listdir/scandir/walk/glob/rglob는 컷오프
# 이후 파일의 **존재**를 노출하므로 같은 look-ahead 표면이다.
RAW_READ_ATTRS = frozenset({
    "read_text", "read_bytes", "open", "load", "iterdir",
    "glob", "rglob", "listdir", "scandir", "walk",
})
# builtin 호출 형태(수신자가 없어 속성 규칙이 닿지 않는다): open(path)
RAW_READ_BUILTINS = frozenset({"open"})
# 읽기 콜러블을 **감싸는** 호출 — 결과도 읽기 콜러블이다 (functools.partial(open)).
READER_WRAPPERS = frozenset({"partial"})


# ── 스캐너 ───────────────────────────────────────────────────────────────────
# R17-2 (b) 폐쇄성 논증: 파이썬에서 "import 시점 또는 호출 시점에 실행되는 코드"는
# 전부 모듈 AST 안의 ast.Call 노드다 — 함수 본문이든, 모듈 최상위든, 람다 본문이든,
# 컴프리헨션이든, 클래스 본문이든. 종전 스캐너는 ast.FunctionDef 노드만 순회해
# **어느 스코프에서 실행되는지**를 탐지 조건으로 삼았고, 그래서 모듈 최상위
# `open(DATA_DIR/…)`(=import 시점 실행)이 0 red였다. 아래 스캐너는 스코프를
# 탐지 조건에서 빼고 **보고용 라벨**로만 쓴다: 모듈 전체의 Call 노드를 하나도
# 빼지 않고 본다. 남는 자유도는 (1) 읽기 콜러블을 어떻게 이름 짓는가,
# (2) 코퍼스 루트가 어떤 바인딩으로 인자에 닿는가 — 둘 다 아래에서 고정점으로 닫는다.
_SCOPE_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


def _parent_map(tree) -> dict:
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    return parents


def _scope_label(node, parents) -> str:
    """읽기가 실행되는 가장 가까운 스코프 이름 — 탐지가 아니라 보고용."""
    cur = parents.get(node)
    while cur is not None:
        if isinstance(cur, ast.Lambda):
            return "<lambda>"
        if isinstance(cur, _SCOPE_TYPES):
            return cur.name
        cur = parents.get(cur)
    return "<module>"


def _bound(node):
    """이름을 바인딩하는 노드라면 (targets, value) — 아니면 None."""
    if isinstance(node, ast.Assign):
        return node.targets, node.value
    if isinstance(node, ast.AnnAssign) and node.value is not None:
        return [node.target], node.value
    if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
        return [node.target], node.iter
    if isinstance(node, ast.NamedExpr):
        return [node.target], node.value
    if isinstance(node, ast.withitem) and node.optional_vars is not None:
        return [node.optional_vars], node.context_expr
    return None


def _names_bound_by(target) -> set[str]:
    return {n.id for n in ast.walk(target) if isinstance(n, ast.Name)}


def _reaches_root(value, tainted, root_funcs, root_attrs, literal) -> bool:
    """이 식이 코퍼스 루트에 닿는가 — 네 가지 바인딩 경로 전부."""
    if value is None:
        return False
    for n in ast.walk(value):
        if isinstance(n, ast.Name) and (n.id in tainted or n.id in root_attrs):
            return True          # 지역/모듈 별칭, from-import된 심볼
        if isinstance(n, ast.Attribute) and n.attr in root_attrs:
            return True          # 인라인 속성 접근 (cutoff_guard.DEFAULT_EDGAR_DATA)
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and literal in n.value:
            return True          # 리터럴 경로
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in root_funcs:
            return True          # 루트를 돌려주는 헬퍼의 반환값
    return False


def _param_names(func_node) -> list[str]:
    """위치 파라미터(순서 유지) — 키워드 전용은 이름으로만 매칭된다."""
    a = func_node.args
    return [p.arg for p in (*a.posonlyargs, *a.args)]


def _keyword_param_names(func_node) -> set[str]:
    a = func_node.args
    return {p.arg for p in (*a.posonlyargs, *a.args, *a.kwonlyargs)}


def _corpus_taint(tree, roots, root_attrs, literal):
    """모듈 전체를 한 스코프로 보는 오염 고정점 + 루트를 반환하는 헬퍼 이름.

    세 방향으로 전파한다: 대입/루프/with/왈러스 바인딩, 루트를 **반환**하는
    헬퍼의 호출값, 그리고 루트를 **인자로 받는** 헬퍼의 파라미터. 마지막 방향이
    없으면 `def _r(p): return p.read_text()` + `_r(DATA_DIR / …)`가 0 red다 —
    읽기가 실행되는 자리와 루트가 바인딩되는 자리가 갈라지는 형태."""
    funcs = {n.name: n for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    tainted, root_funcs = set(roots), set()
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            binding = _bound(node)
            if binding is not None:
                targets, value = binding
                if _reaches_root(value, tainted, root_funcs, root_attrs, literal):
                    for target in targets:
                        for name in _names_bound_by(target) - tainted:
                            tainted.add(name)
                            changed = True
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                    and node.name not in root_funcs:
                if any(isinstance(r, ast.Return)
                       and _reaches_root(r.value, tainted, root_funcs, root_attrs, literal)
                       for r in ast.walk(node)):
                    root_funcs.add(node.name)
                    changed = True
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                    and node.func.id in funcs:
                params = _param_names(funcs[node.func.id])
                reached = [params[i] for i, a in enumerate(node.args)
                           if i < len(params)
                           and _reaches_root(a, tainted, root_funcs, root_attrs, literal)]
                kwparams = _keyword_param_names(funcs[node.func.id])
                reached += [k.arg for k in node.keywords
                            if k.arg in kwparams
                            and _reaches_root(k.value, tainted, root_funcs,
                                              root_attrs, literal)]
                for name in set(reached) - tainted:
                    tainted.add(name)
                    changed = True
    return tainted, root_funcs


def _is_reader_expr(value, readers, attrs) -> bool:
    if isinstance(value, ast.Name):
        return value.id in readers
    if isinstance(value, ast.Attribute):
        return value.attr in attrs or value.attr in readers
    if isinstance(value, ast.Call):
        func = value.func
        wrapper = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
        if wrapper in READER_WRAPPERS:
            return any(_is_reader_expr(a, readers, attrs) for a in value.args)
    return False


def _reader_aliases(tree, attrs, builtins_) -> set[str]:
    """읽기 콜러블에 바인딩된 이름 전부 — `_opener = open`, `partial(open)` 포함."""
    readers = set(builtins_)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            binding = _bound(node)
            if binding is None:
                continue
            targets, value = binding
            if not _is_reader_expr(value, readers, attrs):
                continue
            for target in targets:
                for name in _names_bound_by(target) - readers:
                    readers.add(name)
                    changed = True
    return readers


def _raw_read_functions(source: str, roots=CORPUS_ROOT_NAMES, *,
                        attrs=RAW_READ_ATTRS, builtins_=RAW_READ_BUILTINS,
                        root_attrs=CORPUS_ROOT_ATTRS,
                        literal=CORPUS_ROOT_LITERAL) -> list[str]:
    """가드를 거치지 않는 원시 코퍼스 읽기가 실행되는 스코프 라벨들 (정렬·중복 제거).

    라벨은 함수/메서드 이름, 람다는 `<lambda>`, 클래스 본문은 클래스 이름,
    모듈 최상위는 `<module>`. 이름이 아니라 **존재 여부**가 위반 판정이다."""
    tree = ast.parse(source)
    parents = _parent_map(tree)
    tainted, root_funcs = _corpus_taint(tree, roots, root_attrs, literal)
    readers = _reader_aliases(tree, attrs, builtins_)
    hits = set()
    for call in (n for n in ast.walk(tree) if isinstance(n, ast.Call)):
        func = call.func
        args_reach = any(
            _reaches_root(a, tainted, root_funcs, root_attrs, literal)
            for a in (*call.args, *(k.value for k in call.keywords)))
        if isinstance(func, ast.Attribute) and func.attr in attrs:
            if args_reach or _reaches_root(func.value, tainted, root_funcs,
                                           root_attrs, literal):
                hits.add(_scope_label(call, parents))
        elif isinstance(func, ast.Name) and func.id in readers and args_reach:
            hits.add(_scope_label(call, parents))
        elif isinstance(func, ast.Name) and func.id == "getattr" and args_reach \
                and len(call.args) >= 2 and isinstance(call.args[1], ast.Constant) \
                and call.args[1].value in (attrs | builtins_):
            # 상수 이름의 동적 속성 접근은 정적으로 결정 가능하다 —
            # getattr(DATA_DIR / t, "read_text")()
            hits.add(_scope_label(call, parents))
    return sorted(hits)


# ── 스캔 대상 로스터 (R17-2 (a)(iv): 깊이 무관) ──────────────────────────────
# 로스터에서 빠지는 모듈은 **선언된** 면제 집합에만 있을 수 있고, 그 집합은
# 아래 핀 리터럴과 동일함이 테스트로 강제된다 — 조용히 자라는 면제는 같은 결함의
# 한 층 위 판본이다.
EXEMPT = frozenset({"cutoff_guard.py"})
EXEMPT_PIN = frozenset({"cutoff_guard.py"})


def scannable_sources(root: Path = PIPELINE):
    """스캔 대상 비-테스트 모듈 — 패키지 루트 아래 **모든 깊이**."""
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root).as_posix()
        if rel in EXEMPT or path.name.startswith("test_"):
            continue
        if "__pycache__" in path.parts:
            continue
        yield path


OLD_SOURCE = '''
def load_pit_series(ticker, cutoff):
    xbrl_dir = DATA_DIR / ticker / "xbrl"
    for path in xbrl_dir.glob("*.json"):
        data = json.loads(path.read_text())
'''

_SRC_READ_BYTES = '''
def load_pit_series(ticker, cutoff):
    blob = (DATA_DIR / ticker / "xbrl" / "CIK1.json").read_bytes()
'''

_SRC_ITERDIR = '''
def load_pit_series(ticker, cutoff):
    return sorted((DATA_DIR / ticker / "xbrl").iterdir())
'''

_SRC_PATH_OPEN = '''
def load_pit_series(ticker, cutoff):
    handle = (DATA_DIR / ticker / "xbrl" / "CIK1.json").open()
'''

_SRC_BUILTIN_OPEN = '''
def load_pit_series(ticker, cutoff):
    for name in os.listdir(DATA_DIR / ticker / "xbrl"):
        handle = open(DATA_DIR / ticker / "xbrl" / name)
'''

_SRC_JSON_LOAD_OPEN = '''
def load_pit_series(ticker, cutoff):
    for name in os.listdir(DATA_DIR / ticker / "xbrl"):
        data = json.load(open(DATA_DIR / ticker / "xbrl" / name))
'''

# 단일 형태 대조 — 각 소스는 **정확히 한** 매칭 형태로만 적색이 된다. 그래야
# test_every_matched_read_form_is_load_bearing이 "그 형태를 규칙에서 빼면 이 소스가
# 초록이 된다"로 형태별 기여를 실측할 수 있다 (라벨이 아니라 행동에 결속).
_SRC_ONLY_READ_TEXT = '''
def load_pit_series(ticker, cutoff):
    data = (DATA_DIR / ticker / "xbrl" / "CIK1.json").read_text()
'''

_SRC_ONLY_LOAD = '''
def load_pit_series(ticker, cutoff):
    handle = DATA_DIR / ticker / "xbrl" / "CIK1.json"
    data = json.load(handle)
'''

_SRC_ONLY_GLOB = '''
def load_pit_series(ticker, cutoff):
    return sorted((DATA_DIR / ticker / "xbrl").glob("*.json"))
'''

_SRC_ONLY_RGLOB = '''
def load_pit_series(ticker, cutoff):
    return sorted((DATA_DIR / ticker).rglob("*.json"))
'''

_SRC_ONLY_LISTDIR = '''
def load_pit_series(ticker, cutoff):
    return os.listdir(DATA_DIR / ticker / "xbrl")
'''

_SRC_ONLY_SCANDIR = '''
def load_pit_series(ticker, cutoff):
    return list(os.scandir(DATA_DIR / ticker / "xbrl"))
'''

_SRC_ONLY_WALK = '''
def load_pit_series(ticker, cutoff):
    return list(os.walk(DATA_DIR / ticker))
'''

_SRC_ONLY_BUILTIN_OPEN = '''
def load_pit_series(ticker, cutoff):
    handle = open(DATA_DIR / ticker / "xbrl" / "CIK1.json")
'''

# 형태별 양성 대조 — 한 형태당 소스 하나. 대조가 없는 형태가 R16-1이 막으려는 결함
# 그 자체이므로, 커버리지는 test_every_matched_read_form_has_a_positive_control이
# RAW_READ_ATTRS | RAW_READ_BUILTINS와의 집합 동일성으로 강제한다.
CONTROL_SOURCES = {
    "read_text": (OLD_SOURCE, {"read_text"}),
    "read_bytes": (_SRC_READ_BYTES, {"read_bytes"}),
    "iterdir": (_SRC_ITERDIR, {"iterdir"}),
    "path_open": (_SRC_PATH_OPEN, {"open"}),
    "builtin_open": (_SRC_BUILTIN_OPEN, {"open"}),
    "json_load_open": (_SRC_JSON_LOAD_OPEN, {"load", "open"}),
    "only_read_text": (_SRC_ONLY_READ_TEXT, {"read_text"}),
    "only_load": (_SRC_ONLY_LOAD, {"load"}),
    "only_glob": (_SRC_ONLY_GLOB, {"glob"}),
    "only_rglob": (_SRC_ONLY_RGLOB, {"rglob"}),
    "only_listdir": (_SRC_ONLY_LISTDIR, {"listdir"}),
    "only_scandir": (_SRC_ONLY_SCANDIR, {"scandir"}),
    "only_walk": (_SRC_ONLY_WALK, {"walk"}),
    "only_builtin_open": (_SRC_ONLY_BUILTIN_OPEN, {"open"}),
}


@pytest.mark.parametrize("form", sorted(CONTROL_SOURCES), ids=sorted(CONTROL_SOURCES))
def test_scanner_flags_raw_read_form(form):
    source, _ = CONTROL_SOURCES[form]
    assert _raw_read_functions(source) == ["load_pit_series"], form


def test_every_matched_read_form_has_a_positive_control():
    covered = set().union(*(forms for _, forms in CONTROL_SOURCES.values()))
    assert covered == set(RAW_READ_ATTRS | RAW_READ_BUILTINS)


# R17-2 (e): 위 테스트는 손으로 적은 **라벨** 집합만 본다 — `readlink`를 규칙에
# 넣고 OLD_SOURCE를 가리키는 대조 항목을 함께 넣으면 초록으로 통과했다(31 passed).
# 라벨이 아니라 행동으로 결속한다: 규칙의 각 원소는 **어떤 대조 소스에서 그 원소를
# 빼면 적색이 사라지는지**로만 커버된 것으로 친다. 실제로 아무것도 걸지 않는 형태를
# 규칙에 추가하면(=대조 라벨을 잘못 적으면) 그 형태 파라미터가 적색이 된다.
_MATCHED_FORMS = ([("attr", f) for f in sorted(RAW_READ_ATTRS)]
                  + [("builtin", f) for f in sorted(RAW_READ_BUILTINS)])


@pytest.mark.parametrize(("kind", "form"), _MATCHED_FORMS,
                         ids=[f"{k}:{f}" for k, f in _MATCHED_FORMS])
def test_every_matched_read_form_is_load_bearing(kind, form):
    attrs = RAW_READ_ATTRS - {form} if kind == "attr" else RAW_READ_ATTRS
    builtins_ = RAW_READ_BUILTINS - {form} if kind == "builtin" else RAW_READ_BUILTINS
    depends = [name for name, (source, _) in CONTROL_SOURCES.items()
               if _raw_read_functions(source)
               and not _raw_read_functions(source, attrs=attrs, builtins_=builtins_)]
    assert depends, (
        f"{kind}:{form}은(는) 어떤 양성 대조도 실제로 exercise하지 않는다 — "
        "규칙에는 있으나 아무것도 걸지 않는 형태(=잘못 적은 대조 라벨)")


def test_ast_scanner_catches_old_source_and_passes_modules():
    assert _raw_read_functions(OLD_SOURCE) == ["load_pit_series"]
    for path in scannable_sources():
        assert not _raw_read_functions(path.read_text(encoding="utf-8")), path.name


def test_scan_roster_exemptions_are_pinned():
    """면제 집합은 핀 리터럴과 같아야 한다 — 조용히 자라는 면제 금지 (R17-2 (a))."""
    assert EXEMPT == EXEMPT_PIN
    assert {p.name for p in scannable_sources()} & EXEMPT == set()


# ── R17-2 (d): 리뷰가 실측한 0-red 표 — 전부 ≥1 red 여야 한다 ────────────────
# 스코프(모듈 최상위·람다)와 바인딩(읽기 콜러블 별칭·인라인 속성·from-import·
# 헬퍼 반환)이 축이며, 어느 것도 'aaer-data' 리터럴을 담지 않는다.
_V_MODULE_LEVEL_OPEN = '''
import json

HANDLE = open(DATA_DIR / "TST" / "xbrl" / "CIK1.json")
'''

_V_LAMBDA = '''
load_pit = lambda ticker: (DATA_DIR / ticker / "xbrl").read_text()
'''

_V_OPENER_ALIAS = '''
_opener = open


def load_pit_series(ticker):
    return _opener(DATA_DIR / ticker / "xbrl" / "CIK1.json")
'''

_V_PARTIAL_OPEN = '''
import functools

_reader = functools.partial(open)


def load_pit_series(ticker):
    return _reader(DATA_DIR / ticker / "xbrl" / "CIK1.json")
'''

_V_OS_SCANDIR = '''
import os


def load_pit_series(ticker):
    return list(os.scandir(DATA_DIR / ticker / "xbrl"))
'''

_V_OS_WALK = '''
import os


def load_pit_series(ticker):
    return list(os.walk(DATA_DIR / ticker))
'''

_V_OS_LISTDIR = '''
import os


def load_pit_series(ticker):
    return os.listdir(DATA_DIR / ticker / "xbrl")
'''

_V_INLINE_ATTRIBUTE = '''
import cutoff_guard


def load_pit_series(ticker):
    return open(cutoff_guard.DEFAULT_EDGAR_DATA / ticker / "xbrl" / "CIK1.json")
'''

_V_FROM_IMPORT_INLINE = '''
from cutoff_guard import DEFAULT_EDGAR_DATA


def load_pit_series(ticker):
    return open(DEFAULT_EDGAR_DATA / ticker / "xbrl" / "CIK1.json")
'''

_V_HELPER_RETURN_ALIAS = '''
import cutoff_guard


def get_root():
    return cutoff_guard.DEFAULT_EDGAR_DATA


CORPUS = get_root()


def load_pit_series(ticker):
    return (CORPUS / ticker / "xbrl" / "CIK1.json").read_bytes()
'''

REVIEW_TABLE_VARIANTS = {
    "module_level_builtin_open": _V_MODULE_LEVEL_OPEN,
    "lambda_read": _V_LAMBDA,
    "opener_alias": _V_OPENER_ALIAS,
    "functools_partial_open": _V_PARTIAL_OPEN,
    "os_scandir": _V_OS_SCANDIR,
    "os_walk": _V_OS_WALK,
    "os_listdir": _V_OS_LISTDIR,
    "inline_attribute_symbol": _V_INLINE_ATTRIBUTE,
    "from_import_inline": _V_FROM_IMPORT_INLINE,
    "helper_return_alias": _V_HELPER_RETURN_ALIAS,
}


# ── R17-2 (c): 리뷰에도 R16-1-B 판정문에도 나오지 않는 빌더 생성 변종 ────────
# 생성 규칙: (스코프: 클래스 본문 · 컴프리헨션 · 기본 인자식 · with 문 · async
# 메서드 · try 본문) × (바인딩: 왈러스(:=) · 2-홉 리더 별칭 · 헬퍼 반환의
# joinpath · partial(json.load)) × (형태: 속성 읽기 · builtin 호출 · 열거)의
# 곱집합에서, 위 표가 덮지 않은 칸을 골랐다 — import 시점에 실행되는 칸 우선.
_G_CLASS_BODY = '''
class Loader:
    CACHE = (DATA_DIR / "TST" / "xbrl").iterdir()
'''

_G_MODULE_COMPREHENSION = '''
INDEX = [p.read_text() for p in (DATA_DIR / "TST" / "xbrl").glob("*.json")]
'''

_G_DEFAULT_ARGUMENT = '''
def load_pit_series(ticker, handle=open(DATA_DIR / "TST" / "xbrl" / "CIK1.json")):
    return handle
'''

_G_MODULE_WITH_STATEMENT = '''
with (DATA_DIR / "TST" / "xbrl" / "CIK1.json").open() as fh:
    BLOB = fh.read()
'''

_G_ASYNC_METHOD_WALRUS = '''
class Loader:
    async def load(self, ticker):
        if (target := DATA_DIR / ticker / "xbrl") is not None:
            return target.read_bytes()
'''

_G_TRY_BODY_TWO_HOP_ALIAS = '''
_o = open
_o2 = _o


def load_pit_series(ticker):
    try:
        return _o2(DATA_DIR / ticker / "xbrl" / "CIK1.json")
    except OSError:
        return None
'''

_G_HELPER_JOINPATH = '''
import cutoff_guard


def _root():
    return cutoff_guard.DEFAULT_EDGAR_DATA


def load_pit_series(ticker):
    return _root().joinpath(ticker, "xbrl").rglob("*.json")
'''

_G_PARTIAL_JSON_LOAD = '''
import functools
import json

_parse = functools.partial(json.load)


def load_pit_series(ticker):
    handle = DATA_DIR / ticker / "xbrl" / "CIK1.json"
    return _parse(handle)
'''

_G_PARAM_PASSTHROUGH = '''
def _read_one(p):
    return p.read_text()


def load_pit_series(ticker):
    return _read_one(DATA_DIR / ticker / "xbrl" / "CIK1.json")
'''

_G_KWONLY_PASSTHROUGH = '''
def _read_one(*, path):
    return path.read_bytes()


def load_pit_series(ticker):
    return _read_one(path=DATA_DIR / ticker / "xbrl")
'''

_G_GETATTR_CONST = '''
def load_pit_series(ticker):
    return getattr(DATA_DIR / ticker / "xbrl" / "CIK1.json", "read_text")()
'''

GENERATED_VARIANTS = {
    "param_passthrough_helper": _G_PARAM_PASSTHROUGH,
    "kwonly_param_passthrough": _G_KWONLY_PASSTHROUGH,
    "getattr_constant_attr": _G_GETATTR_CONST,
    "class_body_iterdir": _G_CLASS_BODY,
    "module_comprehension_glob": _G_MODULE_COMPREHENSION,
    "default_argument_open": _G_DEFAULT_ARGUMENT,
    "module_with_statement_open": _G_MODULE_WITH_STATEMENT,
    "async_method_walrus": _G_ASYNC_METHOD_WALRUS,
    "try_body_two_hop_alias": _G_TRY_BODY_TWO_HOP_ALIAS,
    "helper_return_joinpath_rglob": _G_HELPER_JOINPATH,
    "partial_json_load": _G_PARTIAL_JSON_LOAD,
}

_ALL_BYPASS_VARIANTS = {**REVIEW_TABLE_VARIANTS, **GENERATED_VARIANTS}


@pytest.mark.parametrize("variant", sorted(_ALL_BYPASS_VARIANTS),
                         ids=sorted(_ALL_BYPASS_VARIANTS))
def test_bypass_variant_is_flagged_at_any_scope_and_binding(variant):
    source = _ALL_BYPASS_VARIANTS[variant]
    assert CORPUS_ROOT_LITERAL not in source, variant  # 리터럴에 기대지 않는다
    assert _raw_read_functions(source), variant


def _fixture(tmp_path, *, cutoff="2020-01-31", fact_filed="2020-01-01",
             filing_date="2020-01-01", listed="old-submissions-001.json"):
    ticker, case_id = "TST", "C1"
    registry = tmp_path / "cases.json"
    registry.write_text(json.dumps({"cases": [{"case_id": case_id, "ticker": ticker,
                                                "cutoff_date": cutoff}]}), encoding="utf-8")
    edgar = tmp_path / ticker / "edgar"
    xbrl = tmp_path / ticker / "xbrl"
    edgar.mkdir(parents=True)
    xbrl.mkdir(parents=True)
    accession = "0000000000-20-000001"
    submissions = {"filings": {"recent": {"form": ["8-K"],
                    "filingDate": [filing_date], "accessionNumber": [accession],
                    "items": ["1.01"]}, "files": [{"name": listed}]}}
    (edgar / "CIK1.json").write_text(json.dumps(submissions), encoding="utf-8")
    fact = {"filed": fact_filed, "accn": accession, "end": "2019-12-31", "val": 1}
    companyfacts = {"facts": {"us-gaap": {"Assets": {"units": {"USD": [fact]}}}}}
    (xbrl / "CIK1.json").write_text(json.dumps(companyfacts), encoding="utf-8")
    return case_id, ticker, registry


def test_xbrl_filters_logs_and_fixture_log_is_isolated(tmp_path):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-02-01",
                                     filing_date="2020-02-01")
    default = cutoff_guard.DEFAULT_LOG
    before = (default.stat().st_mtime_ns, default.stat().st_size) if default.exists() else None
    rows, metadata = cutoff_guard.load_xbrl_facts(
        cid, ticker, "2020-01-31", data_dir=tmp_path, registry_path=registry)
    assert rows == []
    assert metadata["namespaces"] == ["us-gaap"]
    records = [json.loads(line) for line in
               (tmp_path / "access_log.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(record["reason"] == "xbrl_accession_index" for record in records)
    assert records[-1]["facts_dropped_post_cutoff"] == 1
    after = (default.stat().st_mtime_ns, default.stat().st_size) if default.exists() else None
    assert after == before


def test_xbrl_accession_date_mismatch_fails(tmp_path):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-01-01",
                                     filing_date="2020-01-02")
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_xbrl_facts(cid, ticker, "2020-01-31",
                                     data_dir=tmp_path, registry_path=registry)


def test_cutoff_mismatch_fails(tmp_path):
    cid, ticker, registry = _fixture(tmp_path)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_xbrl_facts(cid, ticker, "2020-02-01",
                                     data_dir=tmp_path, registry_path=registry)


def test_chronology_filters_but_preserves_pre_filter_listing(tmp_path):
    cid, ticker, registry = _fixture(tmp_path, cutoff="2019-01-01",
                                     filing_date="2020-01-01")
    rows, metadata = cutoff_guard.load_edgar_chronology(
        cid, ticker, datetime.date(2019, 1, 1), data_dir=tmp_path,
        registry_path=registry)
    assert rows == []
    assert metadata["listed_subfiles"] == ["old-submissions-001.json"]


def test_string_ticker_resolves_and_enforces(tmp_path, monkeypatch):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-02-01",
                                     filing_date="2020-02-01")
    monkeypatch.setattr(build_payload, "EVALUATEE_CASES", registry)
    assert build_payload.load_pit_series(ticker, datetime.date(2020, 1, 31),
                                         data_dir=tmp_path) == {}
    with pytest.raises(cutoff_guard.CutoffGuardError):
        build_payload.load_pit_series("UNKNOWN", datetime.date(2020, 1, 31),
                                      data_dir=tmp_path)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        build_payload.load_pit_series(ticker, datetime.date(2020, 2, 1),
                                      data_dir=tmp_path)


def test_custom_registry_refused_for_real_corpus(tmp_path):
    _, _, registry = _fixture(tmp_path)
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_xbrl_facts("C1", "TST", "2020-01-31",
                                     data_dir=cutoff_guard.DEFAULT_EDGAR_DATA,
                                     registry_path=registry)


def test_repo_internal_fixture_does_not_create_access_log(tmp_path):
    fixture_dir = PIPELINE / "fixtures" / "data"
    log = fixture_dir / "access_log.jsonl"
    assert not log.exists()
    registry = {"cases": [{"case_id": "C1", "ticker": "TST",
                            "cutoff_date": "2015-06-30"}]}
    rows, _ = cutoff_guard.load_edgar_chronology(
        "C1", "TST", "2015-06-30", data_dir=fixture_dir,
        registry_path=registry)
    assert rows
    assert not log.exists()


def test_payload_v2_nondefault_registry_and_prefilter_namespaces(tmp_path, monkeypatch):
    cid, ticker, registry = _fixture(tmp_path, fact_filed="2020-02-01",
                                     filing_date="2020-02-01")
    evaluatee = tmp_path / "evaluatee"
    evaluatee.mkdir()
    nondefault = evaluatee / "cases_wave2.json"
    nondefault.write_text(registry.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", evaluatee / "cases.json")
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases_wave2.json"])
    case = {"case_id": cid, "ticker": ticker, "cutoff_date": "2020-01-31"}
    facts, coverage = payload_v2_extract.extract_share_facts(case, datetime.date(2020, 1, 31),
                                                              tmp_path, nondefault)
    assert facts == {}
    assert coverage["facts_namespaces_present"] == ["us-gaap"]
    facts, _ = payload_v2_extract.extract_share_facts(ticker, datetime.date(2020, 1, 31),
                                                       tmp_path, nondefault)
    assert facts == {}


def test_payload_v2_identical_registry_matches_collapse(tmp_path, monkeypatch):
    case = {"case_id": "C1", "ticker": "TST", "cutoff_date": "2020-01-31",
            "cik": "0000000001"}
    evaluatee = tmp_path / "evaluatee"
    evaluatee.mkdir()
    for name in ("cases.json", "cases_v2.json"):
        (evaluatee / name).write_text(json.dumps({"cases": [case]}), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", evaluatee / "cases.json")
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases.json", "cases_v2.json"])
    resolved, registry = payload_v2_extract._case_and_registry(
        "TST", datetime.date(2020, 1, 31), payload_v2_extract.DATA_DIR)
    assert resolved == case
    assert registry == evaluatee / "cases.json"


def test_payload_v2_disagreeing_registry_matches_fail(tmp_path, monkeypatch):
    evaluatee = tmp_path / "evaluatee"
    evaluatee.mkdir()
    for name, cutoff in (("cases.json", "2020-01-31"),
                         ("cases_v2.json", "2020-02-01")):
        case = {"case_id": name, "ticker": "TST", "cutoff_date": cutoff,
                "cik": "0000000001"}
        (evaluatee / name).write_text(json.dumps({"cases": [case]}), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", evaluatee / "cases.json")
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases.json", "cases_v2.json"])
    with pytest.raises(cutoff_guard.CutoffGuardError):
        payload_v2_extract._case_and_registry(
            "TST", datetime.date(2020, 1, 31), payload_v2_extract.DATA_DIR)


@pytest.mark.parametrize("extract", [payload_v2_extract.extract_8k_items,
                                      payload_v2_extract.extract_share_facts])
def test_payload_v2_unknown_ticker_wraps_guard_error(tmp_path, monkeypatch, extract):
    registry = tmp_path / "cases.json"
    registry.write_text(json.dumps({"cases": []}), encoding="utf-8")
    monkeypatch.setattr(payload_v2_extract, "EVALUATEE_CASES", registry)
    monkeypatch.setattr(payload_v2_extract, "CASE_FILES", ["cases.json"])
    with pytest.raises(payload_v2_extract.PayloadV2Error):
        extract("UNKNOWN", datetime.date(2020, 1, 31), payload_v2_extract.DATA_DIR)
