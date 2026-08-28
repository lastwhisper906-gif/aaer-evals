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


def sealed_paths(cycle: Path) -> list[tuple[Path, str]]:
    """봉인 매니페스트가 해싱하는 (경로, 기재명) 전건 — 결정론적 순서 (§9).

    manifest_text와 출하 가능성 검사(unshippable_sealed_files)가 같은 목록을
    보게 하는 단일 출처: 둘이 어긋나면 R11-6 구멍이 조용히 다시 열린다."""
    items = [(cycle / name, name) for name in SEALED_FILES
             if (cycle / name).exists()]
    items += [(p, p.relative_to(cycle).as_posix()) for p in evidence_files(cycle)]
    return items


def unshippable_sealed_files(cycle: Path) -> list[str]:
    """R11-6: 봉인 대상 중 git이 실어 나르지 못하는 파일 (무시 규칙 적중).

    seal은 파일 해시를 MANIFEST에 적고, 소유자 명령은 `git add`로 커밋한다.
    `.gitignore`가 무시하는 파일(.DS_Store — macOS에서 Finder로 evidence/를
    열면 생긴다, `__pycache__/`, `*.pyc`)은 해시는 되지만 커밋되지 않는다:
    push 순간부터 모든 클론에서 `manifest_text`가 그 줄만큼 짧아져
    forward_verify_seal이 제3자마다 exit 1, 정본 pytest 게이트도 매 push
    적색이 된다. 재봉인 금지(§3-5) + 매니페스트 불변이므로 사후 교정
    경로가 없다 — 봉인 직전 fail-closed가 유일한 탈출구다. 조용히 건너뛰지
    않는 이유: 누락된 증거 파일이 막힌 봉인보다 나쁘다."""
    names = [name for _, name in sealed_paths(cycle)]
    if not names:
        return []
    try:
        prefix = cycle.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        # 저장소 밖 사이클(테스트 픽스처): 이름 기반 무시 규칙은 위치와
        # 무관하므로 저장소 안 가상 경로로 같은 규칙을 질의한다.
        prefix = "forward/_shipping_probe"
    probe = "\n".join(f"{prefix}/{n}" for n in names)
    r = subprocess.run(["git", "-C", str(REPO), "check-ignore", "--stdin"],
                       input=probe, capture_output=True, text=True)
    if r.returncode not in (0, 1):  # 0=일부 적중, 1=적중 없음, 그 외=오류
        return [f"(git check-ignore 실행 실패 — 출하 가능성 미확인: "
                f"{r.stderr.strip()[:120]})"]
    ignored = {line.strip() for line in r.stdout.splitlines() if line.strip()}
    return sorted(n for n in names if f"{prefix}/{n}" in ignored)


def manifest_text(cycle: Path) -> str:
    """봉인 매니페스트 본문 — 결정론적 순서 (§9)."""
    return "".join(f"{sha256_file(p)}  {name}\n" for p, name in sealed_paths(cycle))


def parse_date(s: str) -> datetime.date:
    return datetime.date.fromisoformat(s[:10])


def fail(msg: str) -> "NoReturn":
    print(f"FAIL — {msg}")
    sys.exit(1)
