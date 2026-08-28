"""forward 사이클 공용 헬퍼 (specs/FORWARD_WATCHLIST_V1.md §9, D100).

구독 전용 가드: owner plan 2026-07-20 §0.4 (zero-metered) — 종량 자격증명이
환경에 있으면 forward 도구는 기동을 거부한다. INVARIANT 4
(pipeline/cli_client.assert_no_metered_credentials)의 확장판.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEC_UA = {"User-Agent": "chaeper lastwhisper906@gmail.com"}  # fetch_primary_sources 규약
SCREENING_CUTOFF = "2026-11-15"          # specs/FORWARD_WATCHLIST_V1.md §2
EXECUTION_WINDOW_END = "2026-11-22"
# R10-8: 창은 ET로 정의된다 (PROTOCOL.md — "ET, EDGAR acceptance"). 11월
# 실행 창은 DST 밖이므로 고정 EST(UTC-5)로 충분 — zoneinfo 의존 없이 결정론.
ET = datetime.timezone(datetime.timedelta(hours=-5))
MIN_SCORED = 11                          # §3-3 사전 등록 완료 분율 (12사 중 ≥11)
UNIVERSE_SIZE = 12

# 봉인 대상 파일 (§9 디렉토리 규범 — MANIFEST 자신·.ots는 제외)
SEALED_FILES = ["PROTOCOL.md", "universe.json", "source_manifest.json", "scores.json"]

METERED_CREDENTIAL_VARS = [
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY",
    "MISTRAL_API_KEY", "COHERE_API_KEY", "XAI_API_KEY", "DEEPSEEK_API_KEY",
]


def assert_subscription_only():
    """zero-metered 가드 — 종량 자격증명 존재 시 즉시 거부 (설명 출력)."""
    present = [v for v in METERED_CREDENTIAL_VARS if os.environ.get(v)]
    if present:
        raise RuntimeError(
            f"종량 API 자격증명 {present} 이(가) 환경에 존재한다.\n"
            "이 프로젝트의 모든 모델 실행은 구독 OAuth(claude -p + "
            "CLAUDE_CODE_OAUTH_TOKEN) 전용이다 (owner plan 2026-07-20 §0.4 "
            "zero-metered 명령, INVARIANT 4). 해당 변수를 unset 후 재실행하라. "
            "이 가드는 우발적 종량 과금을 기계적으로 차단한다.")


def assert_parallel_lengths(label: str, **arrays) -> None:
    """R5-3 (R1-13 클래스, 라이브 수집 사이트): EDGAR submissions 병렬 배열의
    길이 불일치는 zip 절단으로 꼬리 제출(8-K 4.02 오염 스크린 대상 포함)을
    침묵 탈락시킨다 — fail-closed로 즉시 오류."""
    lengths = {name: len(values) for name, values in arrays.items()}
    if len(set(lengths.values())) > 1:
        raise ValueError(f"{label}: submissions 병렬 배열 길이 불일치 {lengths} "
                         "— 스냅샷 재수집 필요 (fail-closed)")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fp_siblings(runs_dir: Path) -> list:
    """R7-3: 러너의 fingerprint-mismatch 산출물({rid}.fp-*.json) 목록.

    존재 = 창 중간 커밋(예: Q-O11 re-pin) 후 재실행이 정본 파일을 비켜
    기록했다는 뜻 — 어느 런이 정본인지 모호하므로 assemble/validate는
    fail-closed하고 소유자가 명시적으로 해소한다."""
    return sorted(Path(runs_dir).glob("*.fp-*.json"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_files(cycle: Path):
    ev = cycle / "evidence"
    return sorted(p for p in ev.rglob("*") if p.is_file()) if ev.exists() else []


def is_sealed(cycle: Path) -> bool:
    """봉인 완결 = MANIFEST.sha256 **와** SEAL_RECORD.md 둘 다 존재 (R11-8).

    MANIFEST만 있는 상태는 봉인이 아니라 중단 잔여물이다 (ots 지연·SIGHUP·
    터미널 종료). R10-6이 seal에만 이 구분을 넣었기 때문에 하류 도구는
    여전히 MANIFEST 존재만으로 '봉인됨'으로 거부했다 — 잔여물 상태에서
    assemble은 "봉인된 사이클"이라 거부하고 seal은 트리가 달라졌다고 거부해
    양쪽 출구가 닫혔다. 판정식을 한 곳에 둬 그 어긋남을 없앤다."""
    return (cycle / "MANIFEST.sha256").exists() and (cycle / "SEAL_RECORD.md").exists()


def seal_residue_notice(cycle: Path) -> str | None:
    """중단 잔여물(MANIFEST만 존재) 상태의 설명 — 없으면 None."""
    if (cycle / "MANIFEST.sha256").exists() and not is_sealed(cycle):
        return ("NOTICE — 중단된 봉인 잔여물(MANIFEST.sha256 존재, "
                "SEAL_RECORD.md 부재): 봉인 완결 상태가 아니므로 계속 진행한다. "
                "봉인은 `forward_seal.py`로 이어서 완결하라 (R11-8).")
    return None


def sealed_paths(cycle: Path) -> list[tuple[Path, str]]:
    """봉인 매니페스트가 해싱하는 (경로, 기재명) 전건 — 결정론적 순서 (§9).

    manifest_text와 출하 가능성 검사(unshippable_sealed_files)가 같은 목록을
    보게 하는 단일 출처: 둘이 어긋나면 R11-6 구멍이 조용히 다시 열린다."""
    items = [(cycle / name, name) for name in SEALED_FILES
             if (cycle / name).exists()]
    items += [(p, p.relative_to(cycle).as_posix()) for p in evidence_files(cycle)]
    return items


# verify_blindness.manifest_lines가 runs/에서 해싱 대상에서 빼는 이름과 동일
_BLINDNESS_EXCLUDE = {"MANIFEST.sha256", ".DS_Store"}


def _git_ignored(probe_paths: list[str]) -> set[str] | None:
    """git 무시 규칙 질의 — NUL 프로토콜 (R12-2).

    `check-ignore --stdin`은 줄 단위이고 기본 core.quotePath=true라서
    비-ASCII·`"`·`\\`를 C-따옴표로 감싸 내보낸다. 그래서 문자열 대조가
    빗나가고 git이 "무시됨"이라 답한 파일을 가드가 흘렸다 — 실측 우회:
    `evidence/증거/.DS_Store`, `we"ird/…`, `back\\slash/…`, 개행 포함 이름.
    `-z`는 입출력 모두 NUL 구분이라 인용이 사라진다 (core.quotePath=false만
    으로는 탭·개행이 여전히 인용되어 불충분). 실패 시 None = 판정 불가."""
    if not probe_paths:
        return set()
    r = subprocess.run(["git", "-C", str(REPO), "check-ignore", "-z", "--stdin"],
                       input="\0".join(probe_paths), capture_output=True, text=True)
    if r.returncode not in (0, 1):  # 0=일부 적중, 1=적중 없음, 그 외=오류
        return None
    return {p for p in r.stdout.split("\0") if p}


def _shipping_members(cycle: Path, include_runs: bool) -> list[tuple[Path, str, str]]:
    """출하 가능성을 물어야 할 (디스크 경로, git 질의 경로, 표시명) 전건.

    봉인 대상뿐 아니라 `runs/`도 포함한다 (R12-2): 봉인 커밋은 runs/forward
    출력을 함께 싣고 블라인드 매니페스트가 runs/ 전체를 해싱하므로,
    같은 '해시됐지만 실리지 않음' 피해가 그쪽에서도 성립한다."""
    try:
        cyc_rel = cycle.resolve().relative_to(REPO.resolve()).as_posix()
    except (ValueError, OSError):
        # 저장소 밖 사이클(테스트 픽스처): 이름 기반 무시 규칙은 위치와
        # 무관하므로 저장소 안 가상 경로로 같은 규칙을 질의한다.
        cyc_rel = "forward/_shipping_probe"
    members = [(p, f"{cyc_rel}/{name}", name) for p, name in sealed_paths(cycle)]
    runs = REPO / "runs"
    if include_runs and runs.is_dir():
        members += [(p, p.relative_to(REPO).as_posix(), p.relative_to(REPO).as_posix())
                    for p in sorted(runs.rglob("*"))
                    if p.is_file() and p.name not in _BLINDNESS_EXCLUDE]
    return members


def _unshippable_structure(path: Path, root: Path) -> str | None:
    """무시 규칙 밖의 '실어 나를 수 없음' 두 종 (R12-2).

    ① 중첩 git 저장소: `git add`는 gitlink 하나만 만들고 내부 파일은 싣지
       않는데 매니페스트는 내부를 전건 해싱한다.
    ② 사이클 밖으로 나가는 심볼릭 링크: 매니페스트는 타깃 내용을 해싱하나
       git은 링크만 싣는다 — 클론에서 타깃이 없으면 is_file()이 False가 되어
       그 줄이 통째로 사라진다 (같은 '한 줄 부족' 피해)."""
    try:
        if path.is_symlink() and root.resolve() not in path.resolve().parents:
            return "사이클 밖 심볼릭 링크"
    except OSError:
        return "해석 불가 심볼릭 링크"
    for parent in path.parents:
        if parent == root or root not in parent.parents:
            break
        if (parent / ".git").exists():
            return "중첩 git 저장소 내부"
    return None


def unshippable_sealed_files(cycle: Path, include_runs: bool = True) -> list[str]:
    """R11-6/R12-2: 해시는 되지만 git이 실어 나르지 못하는 파일 전건.

    seal은 파일 해시를 MANIFEST에 적고, 소유자 명령은 `git add`로 커밋한다.
    `.gitignore`가 무시하는 파일(.DS_Store — macOS에서 Finder로 evidence/를
    열면 생긴다, `__pycache__/`, `*.pyc`)은 해시는 되지만 커밋되지 않는다:
    push 순간부터 모든 클론에서 `manifest_text`가 그 줄만큼 짧아져
    forward_verify_seal이 제3자마다 exit 1, 정본 pytest 게이트도 매 push
    적색이 된다. 재봉인 금지(§3-5) + 매니페스트 불변이므로 사후 교정
    경로가 없다 — 봉인 직전 fail-closed가 유일한 탈출구다. 조용히 건너뛰지
    않는 이유: 누락된 증거 파일이 막힌 봉인보다 나쁘다."""
    members = _shipping_members(cycle, include_runs)
    if not members:
        return []
    ignored = _git_ignored([probe for _, probe, _ in members])
    if ignored is None:
        return ["(git check-ignore 실행 실패 — 출하 가능성 미확인)"]
    bad = {display for _, probe, display in members if probe in ignored}
    cycle_root = cycle.resolve()
    runs_root = (REPO / "runs").resolve()
    for path, probe, display in members:
        root = runs_root if probe.startswith("runs/") else cycle_root
        reason = _unshippable_structure(path, root)
        if reason:
            bad.add(f"{display} ({reason})")
    return sorted(bad)


def manifest_text(cycle: Path) -> str:
    """봉인 매니페스트 본문 — 결정론적 순서 (§9)."""
    return "".join(f"{sha256_file(p)}  {name}\n" for p, name in sealed_paths(cycle))


def parse_date(s: str) -> datetime.date:
    return datetime.date.fromisoformat(s[:10])


def fail(msg: str) -> "NoReturn":
    print(f"FAIL — {msg}")
    sys.exit(1)
