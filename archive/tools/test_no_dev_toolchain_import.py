"""dev-toolchain import 가드 스캔 (PKT-INV11, D-P83).

INV-11 예외는 개발·CI 전용이다: 런타임 코드(pipeline/·scoring/·analysis/)가
dev 도구 체인을 import하면 예외가 런타임 의존으로 승격되어 5종 동결이
무너진다 — AST 수준으로 스캔해 fail-closed로 차단한다.
"""
import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# requirements-dev.in의 도구들 + 그 import 명칭 변형 (pytest-cov → pytest_cov,
# coverage는 pytest-cov의 하부 모듈, pyright는 mypy 대체 후보로 선제 등재)
DEV_TOOLCHAIN_MODULES = {"ruff", "mypy", "pyright", "pytest_cov", "pip_audit",
                         "coverage"}
RUNTIME_ROOTS = ("pipeline", "scoring", "analysis")


def dev_toolchain_imports(root: Path, subdirs=RUNTIME_ROOTS) -> list[str]:
    hits = []
    for sub in subdirs:
        base = root / sub
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.py")):
            tree = ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or ""] if node.level == 0 else []
                else:
                    continue
                for n in names:
                    top = n.split(".")[0]
                    if top in DEV_TOOLCHAIN_MODULES:
                        hits.append(f"{p.relative_to(root)}:{node.lineno} {top}")
    return hits


def test_runtime_tree_never_imports_dev_toolchain():
    hits = dev_toolchain_imports(REPO)
    assert hits == [], ("런타임 코드가 dev 도구 체인을 import — INV-11 예외의 "
                        f"런타임 승격 금지 위반: {hits}")


def test_planted_plain_import_is_caught(tmp_path):
    (tmp_path / "pipeline").mkdir()
    (tmp_path / "pipeline" / "bad.py").write_text("import ruff\n", encoding="utf-8")
    hits = dev_toolchain_imports(tmp_path)
    assert len(hits) == 1 and "ruff" in hits[0] and "bad.py" in hits[0]


def test_planted_from_import_and_submodule_are_caught(tmp_path):
    (tmp_path / "scoring").mkdir()
    (tmp_path / "scoring" / "bad.py").write_text(
        "from mypy import api\nimport pip_audit.cli\n", encoding="utf-8")
    hits = dev_toolchain_imports(tmp_path)
    assert {h.rsplit(" ", 1)[1] for h in hits} == {"mypy", "pip_audit"}


def test_clean_tree_passes(tmp_path):
    (tmp_path / "analysis").mkdir()
    (tmp_path / "analysis" / "ok.py").write_text(
        "import json\nfrom pathlib import Path\n", encoding="utf-8")
    assert dev_toolchain_imports(tmp_path) == []


if __name__ == "__main__":
    found = dev_toolchain_imports(REPO)
    if found:
        print("FAIL — 런타임 dev-toolchain import:")
        for h in found:
            print(f"  {h}")
        sys.exit(1)
    print("PASS — 런타임 코드에 dev-toolchain import 없음 (INV-11)")
