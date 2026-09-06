"""cross_grader_skeleton fail-closed 검증 (BN-09 / D121).

두 성질을 기계적으로 강제한다: ① 스켈레톤 실행은 항상 호출 봉쇄
메시지와 함께 비영 종료한다 ② 스켈레톤 소스에는 실 호출 경로가 존재할
수 없다 (import 허용목록 + 네트워크 문자열 부재).
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

import cross_grader_skeleton as cgs

SKELETON = Path(cgs.__file__).resolve()

# 데이터 적재·해시·경로 처리용 표준 라이브러리만 — 이 목록 밖 import는
# 전부 실 호출 경로 후보로 간주하고 실패시킨다 (INV-12/INV-20 방어선).
ALLOWED_IMPORTS = {"__future__", "ast", "hashlib", "json", "sys", "pathlib"}


def test_skeleton_exits_nonzero_with_calls_disabled_message():
    proc = subprocess.run([sys.executable, str(SKELETON)],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode != 0, "스켈레톤이 0으로 종료 — fail-closed 위반"
    assert "CALLS DISABLED" in proc.stderr


def test_no_live_call_path_imports():
    tree = ast.parse(SKELETON.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    assert imported <= ALLOWED_IMPORTS, f"허용목록 밖 import: {imported - ALLOWED_IMPORTS}"


def test_no_network_strings_in_source():
    # done_when 게이트와 동일 패턴 (grep -nE 'requests|urllib|http').
    source = SKELETON.read_text(encoding="utf-8")
    assert not re.search(r"requests|urllib|http", source)


def test_selection_rule_is_deterministic_and_meets_spec_constraints():
    records = cgs.load_population()
    tier_by_key = {r["key"]: r["tier"] for r in records}
    cells = cgs.stratify(records)
    first = cgs.select_sample(cells)
    second = cgs.select_sample(cells)
    assert first == second, "동일 seed 재실행 불일치 — 결정론 위반"
    assert len(first) == cgs.N_SAMPLE
    assert len(set(first)) == cgs.N_SAMPLE, "중복 선정"
    tier_totals = {}
    for key in first:
        tier_totals[tier_by_key[key]] = tier_totals.get(tier_by_key[key], 0) + 1
    tier_sizes = {}
    for r in records:
        tier_sizes[r["tier"]] = tier_sizes.get(r["tier"], 0) + 1
    for tier, size in tier_sizes.items():
        assert tier_totals.get(tier, 0) >= min(cgs.MIN_PER_TIER, size), \
            f"{tier}: spec §2 tier 최소 보장 위반"
