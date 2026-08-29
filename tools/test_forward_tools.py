"""forward 봉인 도구의 오프라인 테스트 (spec §11, D100). 네트워크 0·호출 0."""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forward_assemble
import forward_common as fc
import forward_prepare
import forward_seal
import forward_validate
import forward_outcome_append


def make_universe(n=12):
    sel = [{"record_id": f"fw001-r{i:02d}", "cik": f"{1000+i:010d}", "ticker": f"TK{i:02d}",
            "name": f"Test Co {i}", "sic": "3674", "float_usd": 2e9 + i} for i in range(1, n + 1)]
    return {"selected": sel, "alternates": [], "rule_ref": "docs/UNIVERSE_SELECTION.md#§6",
            "enumerated_at": "2026-07-20", "candidate_count": n, "excluded_by_reason": {}}


# R3-7: 픽스처 해시는 라이브 동결 파일과 정합해야 validate 3각 대조를 통과
REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_SHA = fc.sha256_file(REPO_ROOT / "pipeline/runner.py")
SCHEMA_SHA = fc.sha256_file(REPO_ROOT / "schemas/llm_output.json")
# R12-8: 픽스처는 prepare가 실제로 쓰는 형태여야 한다 — PIN_SOURCES 전 7건.
# 종전 2건짜리 픽스처는 validate가 2건만 대조하던 시절의 모양이라, 나머지
# 5건(호출 코드 pipeline/cli_client.py 포함)이 무검증인 상태를 드러내지
# 못했다. PIN_SOURCES에서 파생하므로 목록이 늘면 픽스처도 자동으로 따라간다.
PROTOCOL_FIXTURE = (
    "# PROTOCOL fixture\n"
    "- evaluatee_model (pin): `claude-sonnet-5`\n"
    + "".join(f"- `{rel}` sha256 `{fc.sha256_file(REPO_ROOT / rel)}`\n"
              for rel in forward_prepare.PIN_SOURCES))


# R11-4: validate의 runs leg가 러너 출력에서 레코드를 재파생해 대조하므로,
# 픽스처도 생산 경로와 같은 방향이어야 한다 — 출력이 원본, 레코드는 그
# 출력에서 assemble_record로 파생한 값. (종전 픽스처는 레코드를 손으로 쓰고
# 러너 출력은 {"case_id": …} 더미여서, 조립 규칙을 한 줄도 통과하지 않았다.)
_INSUFFICIENT_OF_FIVE = {"sufficient": 0, "partial": 2, "insufficient": 3}


def make_run_output(rid, score=45, suff="sufficient"):
    """llm_output v1.2 형태의 러너 출력 — checklist 비율이 suff를 유도한다."""
    n = _INSUFFICIENT_OF_FIVE[suff]
    checklist = [{"item_id": f"CL{i}", "question": "q",
                  "finding": "insufficient_data" if i < n else "no_flag",
                  "confidence": "medium"} for i in range(5)]
    return {"case_id": rid, "run_id": f"run-{rid}", "model": "claude-sonnet-5",
            "run_timestamp": "2026-11-15T15:00:00Z",
            "misstatement_probability": score, "checklist": checklist,
            "mechanism_hypotheses": [{"affected_line_items": ["rev"]}],
            "overall": {"top_signals": ["s"]},
            "documents_used": [{"accession_no": "0000000000-26-000001"}],
            "fingerprint": {"system_prompt_sha256": "f" * 64,
                            "schema_sha256": SCHEMA_SHA,
                            "pipeline_commit": "a" * 40,
                            "model_requested": "claude-sonnet-5"}}


def make_record(rid, score=45, suff="sufficient", cik=None, out_sha256="b" * 64):
    # make_universe와 동일 규약 — 생산 경로(forward_assemble.main)는 universe
    # 항목을 그대로 rec_meta로 넘기므로 company도 universe에서 파생돼야 한다.
    i = int(rid.rsplit("r", 1)[1])
    meta = {"record_id": rid, "name": f"Test Co {i}", "ticker": f"TK{i:02d}",
            "cik": cik or f"{1000 + i:010d}"}
    return forward_assemble.assemble_record(
        meta, make_run_output(rid, score, suff), out_sha256)


@pytest.fixture
def cycle(tmp_path):
    c = tmp_path / "cycle_t"
    (c / "evidence").mkdir(parents=True)
    fc.write_json(c / "universe.json", make_universe())
    fc.write_json(c / "source_manifest.json", {"sources": [
        {"url": "https://data.sec.gov/x", "filing_date": "2026-11-14",
         "retrieval_date": "2026-11-15", "sha256": "abc", "description": "d",
         "accession_no": "0000000000-26-000001"}]})
    fc.write_json(c / "scores.json", {"records": [
        make_record(f"fw001-r{i:02d}") for i in range(1, 13)]})
    (c / "PROTOCOL.md").write_text(PROTOCOL_FIXTURE, encoding="utf-8")
    (c / "outcome_updates.jsonl").write_text("", encoding="utf-8")
    return c


# R14-2: 실행 창 안의 날짜를 모든 테스트에 고정한다. 이 파일의 봉인 성공
# 경로 19건은 종전에 벽시계를 그대로 읽었고, 2026-11-23부터는 **날짜만의
# 이유로** 영구 red가 됐다 (실측: `today`를 그날로 두면 19 failed / 704
# passed, 하루 앞인 11-20이면 0 red — 붉어지는 원인은 오로지 날짜다).
# 창 게이트 자체를 검사하는 테스트는 EXECUTION_WINDOW_END를 직접
# monkeypatch하므로 이 고정과 무관하게 발화한다.
IN_WINDOW_DAY = datetime.date(2026, 11, 20)


@pytest.fixture(autouse=True)
def pin_seal_clock(monkeypatch):
    monkeypatch.setattr(forward_seal, "_today", lambda: IN_WINDOW_DAY)


# ── 구독 전용 가드 ────────────────────────────────────────────────────────

def test_guard_refuses_metered_credentials(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with pytest.raises(RuntimeError, match="구독 OAuth"):
        fc.assert_subscription_only()
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    with pytest.raises(RuntimeError):
        fc.assert_subscription_only()


# ── universe 정합 ─────────────────────────────────────────────────────────

def test_universe_checks_catch_violations():
    u = make_universe(11)
    assert any("≠ 12" in e for e in forward_prepare.check_universe(u))
    u = make_universe()
    u["selected"][1]["cik"] = u["selected"][0]["cik"]
    assert any("중복 CIK" in e for e in forward_prepare.check_universe(u))
    u = make_universe()
    u["selected"][0]["float_usd"] = 5e8
    assert any("$1B" in e for e in forward_prepare.check_universe(u))
    # R8-3: 서로 다른 CIK인데 1차 티커 공유 — corpus 디렉토리 병합 위험
    u = make_universe()
    u["selected"][1]["ticker"] = u["selected"][0]["ticker"] + "/B"
    assert any("1차 티커 충돌" in e for e in forward_prepare.check_universe(u))
    assert forward_prepare.check_universe(make_universe()) == []


def test_fetch_refuses_primary_ticker_collision_before_any_write(tmp_path):
    """R8-3: fetch 진입점에서도 fail-closed — 파일 0개 쓴 채 거부."""
    import fetch_xbrl_facts as fxf
    u = make_universe()
    u["selected"][1]["ticker"] = u["selected"][0]["ticker"]
    upath = tmp_path / "universe.json"
    fc.write_json(upath, u)
    dest = tmp_path / "dest"
    with pytest.raises(SystemExit, match="1차 티커 충돌"):
        fxf.fetch_forward(upath, dest)
    assert not dest.exists()


class _FetchResp:
    def __init__(self, obj):
        self.content = json.dumps(obj).encode("utf-8")


def _manifest_fixture(tmp_path, monkeypatch, pinned_path, *, on_disk=None):
    """R10-2 픽스처: 밀폐된 REPO(매니페스트만) + DATA_DIR을 fxf에 주입.

    R11-2: 가드는 접두가 아니라 출처로 판정하므로, 핀 경로의 실제 바이트를
    디스크에 둘 수 있어야 한다 (on_disk=b"..." → 그 바이트 + 정합 sha256)."""
    import fetch_xbrl_facts as fxf
    data_dir = tmp_path / "aaer-data"
    repo = tmp_path / "repo"
    (repo / "data/manifests").mkdir(parents=True)
    entry = {"path": pinned_path}
    if on_disk is not None:
        target = data_dir / pinned_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(on_disk)
        entry["sha256"] = hashlib.sha256(on_disk).hexdigest()
    (repo / "data/manifests/aaer_data_manifest.json").write_text(
        json.dumps({"files": [entry]}), encoding="utf-8")
    monkeypatch.setattr(fxf, "DATA_DIR", data_dir)
    monkeypatch.setattr(fxf, "REPO", repo)
    return fxf, data_dir


def test_fetch_refuses_intact_pinned_snapshot_before_any_write(tmp_path, monkeypatch):
    """R10-2(a): 온전한 회고 스냅샷(디스크 바이트 == 매니페스트 기록)과
    충돌하는 수집은 네트워크에 닿기 전 거부 — 7월 CIEN 판형."""
    fxf, data_dir = _manifest_fixture(tmp_path, monkeypatch,
                                      "TK01/xbrl/CIK0000001001.json",
                                      on_disk=b'{"july": "snapshot"}')
    monkeypatch.setattr(fxf, "fetch", lambda url: (_ for _ in ()).throw(
        AssertionError("거부 전에 네트워크 호출")))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe())
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, data_dir)
    assert (data_dir / "TK01/xbrl/CIK0000001001.json").read_bytes() == \
        b'{"july": "snapshot"}', "거부 경로가 핀 바이트를 건드렸다"
    assert not (data_dir / "fetch_log.jsonl").exists()


def test_fetch_refuses_when_pinned_bytes_drifted(tmp_path, monkeypatch):
    """R11-2: 기록 sha256과 디스크 바이트가 어긋난 핀 경로 — 상태 미상이므로
    여전히 거부 (가드 완화가 무조건 통과로 새지 않는다).

    주의: 이 픽스처는 로그를 쓰지 않으므로 거부가 **출처 leg**에서 나온다 —
    sha leg의 변별력은 아래 test_sha_leg_is_the_only_reason_for_refusal이
    따로 고정한다 (R12-1(c))."""
    fxf, data_dir = _manifest_fixture(tmp_path, monkeypatch,
                                      "TK01/xbrl/CIK0000001001.json",
                                      on_disk=b'{"july": "snapshot"}')
    (data_dir / "TK01/xbrl/CIK0000001001.json").write_bytes(b'{"drifted": 1}')
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe())
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, data_dir)


def _commit_canonical_log(fxf) -> None:
    """runbook 2b의 로그 커밋 단계 (D-P98: 감독 수집마다 정본 로그를 커밋).

    R16-2: 출처 권위의 근거가 정본 로그의 **HEAD 판**이 됐으므로, 픽스처도
    실제 절차를 그대로 밟아야 한다 — 작업 트리에만 있는 행은 (위조든 정당한
    수집이든) 권위가 없다는 것이 이 아이템의 성질 전체다. 격리 루트는
    tools/conftest.py가 꽂은 임시 디렉토리이므로 여기서 저장소로 만든다."""
    root = fxf.FETCH_LOG_ROOT
    assert root is not None and root != fxf.REPO, (
        "격리 seam이 꺼진 채로 커밋하려 했다 — 실제 저장소에 커밋할 뻔했다")
    log_path = fxf.fetch_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch()
    if not (root / ".git").exists():
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for key, value in (("user.email", "t@example.invalid"), ("user.name", "t")):
            subprocess.run(["git", "-C", str(root), "config", key, value], check=True)
    subprocess.run(["git", "-C", str(root), "add", "--", fxf.FETCH_LOG_REL],
                   check=True)
    subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false",
                    "commit", "-q", "--allow-empty", "-m", "fetch log"], check=True)


def _log_row_for(data_dir, rel, **extra):
    """실제 _log_row와 같은 형태 — portable_path는 저장소·홈 밖 경로를
    절대 경로로 적는다 (픽스처 tmp_path가 그 경우)."""
    return {"path": str(data_dir / rel), "kind": "companyfacts", **extra}


def _authoritative_log(fxf, vm, data_dir, manifest_path, rows):
    """R12-1: 로그를 쓰고 그 로그까지 포함해 매니페스트를 재생성 —
    로그가 자기 핀과 일치하는 '권위 있는' 상태를 만든다 (runbook 2b 상태)."""
    (data_dir / "fetch_log.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    manifest_path.write_text(json.dumps(vm.build_manifest()), encoding="utf-8")


def _canonical_log(fxf, vm, data_dir, manifest_path, rows):
    """R15-1: 정본 수집 로그(트리 밖·git 관리)에 행을 쓰고 매니페스트 재생성.

    _authoritative_log의 후신 — 종전에는 '로그가 자기 핀과 일치해야 권위'
    였으므로 로그를 DATA_DIR 안에 두고 함께 재핀해야 했다. 이제 권위 판정이
    없으므로 로그는 정본 위치에 있기만 하면 된다."""
    log_path = fxf.fetch_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("".join(json.dumps(r) + "\n" for r in rows),
                        encoding="utf-8")
    _commit_canonical_log(fxf)   # R16-2: 권위의 근거는 HEAD 판이다
    manifest_path.write_text(json.dumps(vm.build_manifest()), encoding="utf-8")


def _fetch_fixture(tmp_path, monkeypatch):
    import fetch_xbrl_facts as fxf
    import verify_manifest as vm
    data_dir = tmp_path / "aaer-data"
    repo = tmp_path / "repo"
    (repo / "data/manifests").mkdir(parents=True)
    manifest_path = repo / "data/manifests/aaer_data_manifest.json"
    manifest_path.write_text(json.dumps({"files": []}), encoding="utf-8")
    monkeypatch.setattr(fxf, "DATA_DIR", data_dir)
    monkeypatch.setattr(fxf, "REPO", repo)
    monkeypatch.setattr(vm, "DATA_DIR", data_dir)
    return fxf, vm, data_dir, manifest_path


def test_forged_log_row_cannot_open_a_frozen_pinned_file(tmp_path, monkeypatch):
    """R12-1(a): 종전 가드의 신뢰 앵커는 보호 대상 트리 안의 서명 없는
    append-only 파일이었다 — 동결 경로를 지목하는 위조 행 한 줄이면
    fetch_forward가 0을 반환하고 복구 불가능한 바이트를 덮어썼다
    (lens B 작동 익스플로잇). 로그는 이제 자기 매니페스트 핀과 일치할
    때만 출처 권위를 갖는다."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    frozen = data_dir / "TK01/xbrl/CIK0000001001.json"
    frozen.parent.mkdir(parents=True)
    frozen.write_bytes(b'{"july": "snapshot"}')
    # 온전한 동결 스냅샷 + (아직 위조 전) 권위 있는 빈 로그
    _authoritative_log(fxf, vm, data_dir, manifest_path, [])

    # 공격: 동결 경로를 자기 것이라 주장하는 한 줄 덧붙이기
    with (data_dir / "fetch_log.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps(_log_row_for(
            data_dir, "TK01/xbrl/CIK0000001001.json",
            sha256=hashlib.sha256(b'{"july": "snapshot"}').hexdigest())) + "\n")

    monkeypatch.setattr(fxf, "fetch", lambda url: (_ for _ in ()).throw(
        AssertionError("거부 전에 네트워크 호출")))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, data_dir)
    assert frozen.read_bytes() == b'{"july": "snapshot"}', "동결 바이트가 열렸다"


def _run_remedy(vm, monkeypatch, manifest_path, *argv, fxf=None) -> int:
    """거부 메시지가 지목하는 복구 명령을 그대로 실행한다 (runbook 2b).

    R16-2: 2b는 재핀과 **정본 로그 커밋** 두 단계다 (D-P98). fxf가 주어지면
    커밋까지 밟는다 — 그것이 방금 수집한 행에 출처 권위를 주는 유일한 단계다.
    fxf 없이 부르면 재핀만 — 위조 행이 2b만으로는 권위를 얻지 못한다는 성질을
    고정하는 테스트가 그 형태를 쓴다."""
    monkeypatch.setattr(vm, "MANIFEST", manifest_path)
    monkeypatch.setattr(sys, "argv", ["verify_manifest.py", "--write", *argv])
    rc = vm.main()
    if fxf is not None:
        _commit_canonical_log(fxf)
    return rc


FROZEN_BYTES = b'{"july": "snapshot"}'


def _custody_fixture(tmp_path, monkeypatch, dest_rel: str):
    """R15-1: 핀된 온전한 동결 스냅샷 + 그 경로를 관할하는 dest.

    dest_rel="" 는 기본 dest(= DATA_DIR), "sub" 는 하위 dest — R14-5/R15-1이
    드러낸 세탁 경로가 정확히 후자다 (가드는 `dest/fetch_log.jsonl`을,
    재핀 검사는 `DATA_DIR/fetch_log.jsonl`을 읽어 서로 다른 파일을 봤다)."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    dest = data_dir / dest_rel if dest_rel else data_dir
    prefix = f"{dest_rel}/" if dest_rel else ""
    frozen = data_dir / f"{prefix}TK01/xbrl/CIK0000001001.json"
    frozen.parent.mkdir(parents=True)
    frozen.write_bytes(FROZEN_BYTES)
    manifest_path.write_text(json.dumps(vm.build_manifest()), encoding="utf-8")
    monkeypatch.setattr(fxf, "fetch", lambda url: (_ for _ in ()).throw(
        AssertionError("거부 전에 네트워크 호출")))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    return fxf, vm, manifest_path, dest, frozen, upath


def _forge(log_path: Path, frozen: Path) -> None:
    """보호 트리 안 임의 위치에 '이 동결 파일은 내가 썼다'는 행을 심는다."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log:
        log.write(json.dumps({
            "record_id": "fw001-r01", "kind": "companyfacts",
            "path": str(frozen),
            "sha256": hashlib.sha256(FROZEN_BYTES).hexdigest()}) + "\n")


@pytest.mark.parametrize("dest_rel", ["", "sub"])
def test_forged_claim_cannot_be_laundered_through_any_dest(
        tmp_path, monkeypatch, dest_rel):
    """R15-1(a): 위조 → 거부 → 가드가 지목하는 복구 명령(2b) → 재시도.
    R13-5의 3단계 시퀀스를 **dest 전건**으로 돌린다.

    replaces test_forged_claim_survives_the_remedy_the_guard_itself_prints:
    그 테스트가 고정하던 성질("위조 행이 2b를 통과해 살아남는다 — 그러니
    2b가 거부해야 한다")은 R15-1에서 한 단계 앞으로 이동했다. 이제 위조 행은
    **읽히지 않아서** 실패한다 — 보호 트리 안 어디에 놓든 정본 로그가 아니다.
    2b는 정상적으로 성공하지만(축복할 주장이 없다) 그것이 아무 권위도 주지
    않는다는 것이 이 테스트의 요점이다.

    dest_rel="sub"가 R14-5가 실증한 세탁 경로다: 종전 코드에서 가드는
    `dest/fetch_log.jsonl`(= sub/)을, 재핀 거부 검사는 `DATA_DIR/`의 로그를
    읽었으므로 하위 dest 위조는 2b에서 걸리지 않고 3단계에서 통과했다."""
    fxf, vm, manifest_path, dest, frozen, upath = _custody_fixture(
        tmp_path, monkeypatch, dest_rel)
    _forge(dest / "fetch_log.jsonl", frozen)

    # 1단계: 거부
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)

    # 2단계: 복구 명령(runbook 2b) — 성공하지만 어떤 출처 주장도 축복하지 않는다
    assert _run_remedy(vm, monkeypatch, manifest_path) == 0
    assert "custody_claims" not in json.loads(manifest_path.read_text()), \
        "재핀 산출물이 다시 출처 주장의 진실 원천이 됐다"

    # 3단계: 재시도 — 여전히 거부, 동결 바이트 무접촉
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)
    assert frozen.read_bytes() == FROZEN_BYTES, "동결 바이트가 열렸다"


@pytest.mark.parametrize("dest_rel,log_rel", [
    ("", "fetch_log.jsonl"),               # 종전 정본 위치
    ("sub", "sub/fetch_log.jsonl"),        # --dest 처리가 닿는 위치 (R14-5 세탁 경로)
    ("", "TK01/fetch_log.jsonl"),          # 티커 디렉토리 안
    ("", "TK01/xbrl/fetch_log.jsonl"),     # 핀 파일 바로 옆
])
def test_no_write_inside_the_corpus_can_create_a_trusted_claim(
        tmp_path, monkeypatch, dest_rel, log_rel):
    """R15-1(b) 속성: 보호 트리(DATA_DIR) **안** 어떤 파일에 행을 덧붙여도
    핀된 경로에 대해 수집이 허가되지 않는다.

    기제가 아니라 속성이 산출물이다 — R11-2·R12-1·R13-5는 각각 특정 파일
    하나를 막았고, 매번 다른 파일이 남아 있었다. 여기서는 위치를 4곳으로
    변주하고, 그 사이에 2b까지 끼워 넣는다."""
    fxf, vm, manifest_path, dest, frozen, upath = _custody_fixture(
        tmp_path, monkeypatch, dest_rel)
    _forge(fxf.DATA_DIR / log_rel, frozen)

    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)
    assert _run_remedy(vm, monkeypatch, manifest_path) == 0   # 2b 후에도
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)
    assert frozen.read_bytes() == FROZEN_BYTES, "동결 바이트가 열렸다"
    assert not fxf.fetch_log_path().is_file(), \
        "거부 경로가 정본 로그에 행을 남겼다"


def test_repin_grants_no_custody_authority_so_no_owner_flag_is_needed(
        tmp_path, monkeypatch):
    """R15-1: replaces test_owner_flag_is_the_only_way_past_a_new_custody_claim.

    그 테스트의 성질("이미 핀된 경로에 대한 새 주장을 통과시키는 유일한 길은
    소유자 플래그 --allow-new-custody-claims")은 존재하지 않게 됐다. 그것을
    불필요하게 만든 **새 불변식**을 대신 고정한다:

      (1) 재핀(2b)은 어떤 출처 주장도 축복하지 않는다 — 산출 매니페스트에
          custody_claims 키가 없고, 재핀 뒤에도 가드 판정이 바뀌지 않는다.
      (2) 그래서 재핀 전용 소유자 플래그도 사라졌다 — 넘기면 argparse가 거부.
      (3) 핀 경로를 실제로 덮어쓰는 유일한 길은 종전과 같이 수집 시점의
          --allow-pinned이며, 그것은 여전히 소유자 판단이고 로그에 남는다.

    즉 우회 경로의 수가 둘에서 하나로 줄었고, 남은 하나는 재핀 도구가 아니라
    수집 도구 쪽에 있다."""
    fxf, vm, manifest_path, dest, frozen, upath = _custody_fixture(
        tmp_path, monkeypatch, "")
    _forge(fxf.DATA_DIR / "fetch_log.jsonl", frozen)

    # (1) 재핀은 성공하되 아무것도 축복하지 않는다
    assert _run_remedy(vm, monkeypatch, manifest_path) == 0
    assert "custody_claims" not in json.loads(manifest_path.read_text())
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)

    # (2) 재핀 전용 소유자 플래그는 존재하지 않는다 (argparse 종료코드 2)
    with pytest.raises(SystemExit) as exc:
        _run_remedy(vm, monkeypatch, manifest_path, "--allow-new-custody-claims")
    assert exc.value.code == 2
    assert not hasattr(vm, "new_custody_claims")

    # (3) 남은 유일한 우회는 수집 시점의 소유자 판단 --allow-pinned
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    assert fxf.fetch_forward(upath, dest, {"TK01"}) == 0
    rows = [json.loads(x) for x in fxf.fetch_log_path()
            .read_text(encoding="utf-8").splitlines()]
    assert [r for r in rows if r.get("kind") == "pinned_override"]


def _forge_into_canonical(fxf, frozen: Path, *, mode: str) -> None:
    """정본 로그의 **작업 트리** 판에 위조 행을 심는다 — 커밋하지 않는다.

    R15-1이 옮겨놓은 신뢰 근원을 그대로 겨눈 R15-1 lens B 익스플로잇의 형태들."""
    row = json.dumps({"record_id": "fw001-r01", "kind": "companyfacts",
                      "path": str(frozen),
                      "sha256": hashlib.sha256(FROZEN_BYTES).hexdigest()}) + "\n"
    log_path = fxf.fetch_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "append_to_empty":            # 추적·커밋된 빈 로그에 덧붙이기
        _commit_canonical_log(fxf)
        with log_path.open("a", encoding="utf-8") as log:
            log.write(row)
    elif mode == "append_to_genuine":        # 진짜 행이 이미 있는 로그에 덧붙이기
        log_path.write_text(json.dumps(
            {"record_id": "fw001-r09", "kind": "companyfacts",
             "path": str(fxf.DATA_DIR / "TK09/xbrl/CIK0000001009.json"),
             "sha256": "0" * 64}) + "\n", encoding="utf-8")
        _commit_canonical_log(fxf)
        with log_path.open("a", encoding="utf-8") as log:
            log.write(row)
    elif mode == "rewrite_tracked":          # 커밋된 내용을 통째로 갈아치우기
        _commit_canonical_log(fxf)
        log_path.write_text(row, encoding="utf-8")
    elif mode == "untracked":                # 커밋이 아예 없는 상태
        log_path.write_text(row, encoding="utf-8")
    else:
        raise AssertionError(mode)


@pytest.mark.parametrize("mode", ["append_to_empty", "append_to_genuine",
                                  "rewrite_tracked", "untracked"])
def test_forged_row_in_the_canonical_log_working_tree_grants_no_authority(
        tmp_path, monkeypatch, mode):
    """R16-2(a): R15-1은 신뢰 근원을 corpus 밖 git 관리 경로로 **옮겼지만**
    옮긴 자리에 인증을 놓지 않았다 — `_log_is_authoritative`가 삭제되고 그
    자리는 비었다. 정본 로그의 작업 트리 판에 위조 행 한 줄이면 fetch_forward가
    0을 반환하며 온전한·핀된·동결 바이트를 덮어썼다 (lens B 작동 익스플로잇,
    logs/verdicts/R15-1-B.md §3).

    이제 권위의 근거는 HEAD 판이다: 커밋되지 않은 행은 위조든 정당한 수집이든
    아무 것도 열지 못하고, 커밋하면 git 이력에 남는다 — R15-1이 앵커라고
    선언했던 성질이 비로소 기계적으로 강제된다.

    네 변주는 전부 '커밋되지 않은 작업 트리 행'이라는 한 성질의 변주다:
    빈 로그에 덧붙이기 / 진짜 행이 있는 로그에 덧붙이기 / 커밋된 내용을 통째로
    갈아치우기 / 커밋이 아예 없는 상태."""
    fxf, vm, manifest_path, dest, frozen, upath = _custody_fixture(
        tmp_path, monkeypatch, "")
    _forge_into_canonical(fxf, frozen, mode=mode)

    assert "TK01/xbrl/CIK0000001001.json" not in fxf._own_writes(), \
        "커밋되지 않은 위조 행이 출처 권위를 얻었다"
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)
    assert frozen.read_bytes() == FROZEN_BYTES, "동결 바이트가 열렸다"

    # 2b(재핀)만으로는 권위가 생기지 않는다 — 커밋이 그 단계다
    assert _run_remedy(vm, monkeypatch, manifest_path) == 0
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, dest)
    assert frozen.read_bytes() == FROZEN_BYTES, "동결 바이트가 열렸다"


def _committed_custody_deadlock(monkeypatch) -> dict:
    """커밋된 universe.json × 커밋된 매니페스트에 대한 가드의 blocked 집합.

    R16-4: 11월 창 step (2)는 파일 하나 쓰기 전에 `universe["selected"]` 전건을
    이 술어로 훑고, 막힌 티커를 **한 dict에 모아 한 번의 SystemExit**을 낸다 —
    즉 한 티커가 막히면 12사 전부가 0건으로 끝난다. 로컬 corpus 유무에 판정이
    흔들리지 않도록 존재 술어는 매니페스트 자체로 둔다 (핀되어 있다 = 그
    바이트는 보호 대상이다)."""
    import fetch_xbrl_facts as fxf
    monkeypatch.setattr(fxf, "FETCH_LOG_ROOT", None)   # 커밋된 정본 로그를 본다
    universe = json.loads(
        (REPO_ROOT / "forward/cycle_001/universe.json").read_text(encoding="utf-8"))
    pinned = {f["path"]: f.get("sha256") for f in json.loads(
        (REPO_ROOT / "data/manifests/aaer_data_manifest.json")
        .read_text(encoding="utf-8"))["files"]}
    blocked = fxf.pinned_conflicts(universe, "", pinned, fxf._own_writes(),
                                   lambda rel: True)
    return {t: sorted(v) for t, v in blocked.items()}


# Q-F21이 미해소인 동안의 **기록된** 교착 상태. 새 핀 티커가 유니버스에 들어오면
# 여기서 즉시 깨진다 — 교착이 이미 있다는 사실이 새 교착을 숨기지 못하게.
RECORDED_CUSTODY_DEADLOCK = {
    "CIEN": ["CIEN/edgar/CIK0000936395-submissions-001.json",
             "CIEN/edgar/CIK0000936395-submissions-002.json",
             "CIEN/edgar/CIK0000936395.json",
             "CIEN/xbrl/CIK0000936395.json"],
}


def test_committed_custody_deadlock_matches_the_recorded_state(monkeypatch):
    """R16-4(c) 상보: 교착의 **현재 범위**를 고정한다.

    아래 xfail 테스트 하나만 두면 '이미 red인 자리'가 새 위반을 흡수한다 —
    핀된 티커가 하나 더 들어와도 여전히 xfail이라 아무도 모른다. 이 테스트는
    범위가 정확히 Q-F21이 기록한 CIEN 4건일 때만 green이다."""
    assert _committed_custody_deadlock(monkeypatch) == RECORDED_CUSTODY_DEADLOCK


@pytest.mark.xfail(strict=True, reason=(
    "Q-F21 미해소 — fw001-r08(CIEN)이 매니페스트 핀 4건과 충돌해 11월 창 "
    "step (2)가 12사 전건 0파일로 중단된다. 옵션 (A) 대기 1순위 승격으로 "
    "해소되면 이 테스트가 XPASS(strict → red)가 되어 마커 제거를 강제한다."))
def test_committed_universe_has_no_pinned_custody_deadlock(monkeypatch):
    """R16-4(c): 소유자가 Q-F21을 해소하면 green이 되어야 하는 성질.

    가드는 `dest.mkdir` 전에, 바이트 하나 쓰기 전에 판정하고 막힌 티커를 모아
    **단일** SystemExit을 던진다. 따라서 CIEN 한 건의 충돌이 step (2) 전체를
    0파일로 끝낸다 — Q-F21이 통계·거버넌스 문제로만 기록돼 있었지 실행 창
    첫날의 교착이라는 사실은 어디에도 없었다.

    strict xfail인 이유: 교착은 지금 **실재**하므로 이 단언은 red이고, 그것을
    green으로 만드는 것은 소유자 결정(INV-18)이지 세션의 코드 변경이 아니다.
    suite를 red로 두면 다른 모든 게이트가 가려지므로 기록된 실패로 격리한다 —
    해소되는 순간 XPASS로 깨져서 조용히 지나갈 수 없다."""
    assert _committed_custody_deadlock(monkeypatch) == {}


def test_canonical_log_is_tracked_in_git(monkeypatch):
    """R16-2(d): 정본 로그가 실제로 저장소에 **추적**되고 있어야 한다.

    R15-1의 앵커 주장("행의 신설은 git diff에 드러난다")은 파일이 추적될
    때만 성립하고, 그 커밋에서는 `data/provenance/`가 생성조차 되지 않았다.
    추적이 끊기면 committed_log_lines가 영구히 빈 리스트를 돌려주므로 가드는
    fail-closed로 굳는다 — 조용한 green이 아니라 여기서 깨진다."""
    import fetch_xbrl_facts as fxf
    monkeypatch.setattr(fxf, "FETCH_LOG_ROOT", None)
    proc = subprocess.run(
        ["git", "-C", str(fxf.REPO), "ls-files", "--error-unmatch", "--",
         fxf.FETCH_LOG_REL], capture_output=True, text=True)
    assert proc.returncode == 0, \
        f"{fxf.FETCH_LOG_REL}가 git에 추적되지 않는다: {proc.stderr.strip()}"
    assert fxf.fetch_log_path().is_file()


def test_canonical_fetch_log_lives_in_git_outside_the_corpus(monkeypatch):
    """R15-1: 정본 해석 자체를 고정한다 — tools/conftest.py의 격리 seam이
    프로덕션 경로를 가리지 않도록, seam을 끄고 실제 값을 확인한다.

    로그가 git 관리 트리 안(REPO 상대)이고 보호 대상 corpus(DATA_DIR) 밖이라는
    두 성질이 R15-1의 앵커 전체다: 앞의 것이 'git diff가 체크포인트'를,
    뒤의 것이 '트리 안 쓰기가 주장을 만들 수 없다'를 성립시킨다."""
    import fetch_xbrl_facts as fxf
    monkeypatch.setattr(fxf, "FETCH_LOG_ROOT", None)
    assert fxf.fetch_log_path() == fxf.REPO / fxf.FETCH_LOG_REL
    assert fxf.fetch_log_path().is_relative_to(fxf.REPO)
    assert not fxf.fetch_log_path().is_relative_to(fxf.DATA_DIR)


def test_every_consumer_reads_the_one_canonical_log(tmp_path, monkeypatch):
    """R15-1: writer·가드·source_manifest가 같은 한 파일을 본다.

    dest 밑에는 로그가 생기지 않고 (writer), 가드의 출처 집합은 정본 로그에서
    나오며 (guard), build_sources는 --fetch-dir이 아니라 정본을 읽는다
    (네 번째 소비자 — R14-5 보고에서 Location 목록에 빠져 있던 자리)."""
    import forward_source_manifest as fsm
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    dest = data_dir / "sub"
    assert fxf.fetch_forward(upath, dest) == 0

    assert fxf.fetch_log_path().is_file()
    assert not (dest / "fetch_log.jsonl").exists()
    assert not (data_dir / "fetch_log.jsonl").exists()
    _commit_canonical_log(fxf)   # R16-2: HEAD 판만이 출처 권위를 준다
    assert fxf._own_writes() == {
        "sub/TK01/xbrl/CIK0000001001.json", "sub/TK01/edgar/CIK0000001001.json"}
    # build_sources가 --fetch-dir에서 로그 경로를 파생하면 여기서 죽는다
    assert fsm.build_sources(dest, "2026-11-15") == []


def test_runbook_repin_loop_still_works(tmp_path, monkeypatch):
    """R13-5(b)(d): 거부 메시지가 지목하는 복구 명령이 정당한 경우에는
    실제로 통한다 — fetch → 2b → 재수집 → 2b 가 전부 0.

    한 번 축복된 주장은 다음 재핀에서 '새 주장'이 아니므로, 창 안 재시도·
    부분 실패 복구(R11-2가 되살린 흐름)가 다시 막히지 않는다."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(2))

    assert fxf.fetch_forward(upath, data_dir) == 0
    assert _run_remedy(vm, monkeypatch, manifest_path, fxf=fxf) == 0   # 2b (최초 핀)
    assert fxf.fetch_forward(upath, data_dir) == 0                     # 재수집
    assert _run_remedy(vm, monkeypatch, manifest_path, fxf=fxf) == 0   # 2b (재핀)
    assert fxf.fetch_forward(upath, data_dir) == 0


def test_runbook_repin_loop_still_works_under_a_sub_dest(tmp_path, monkeypatch):
    """R15-1(d): 정당한 흐름(fetch → 2b → 재수집 → 2b → 재수집)이 **하위
    dest**에서도 전부 0을 반환한다.

    위 test_runbook_repin_loop_still_works가 기본 dest를 고정하고, 이 테스트가
    R14-5의 세탁 경로였던 --dest 하위 트리를 고정한다 — 거부만 강해지고 정당한
    재시도·부분 실패 복구가 막히면 R11-2를 다시 만드는 것이다."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(2))
    dest = data_dir / "sub"

    assert fxf.fetch_forward(upath, dest) == 0
    assert _run_remedy(vm, monkeypatch, manifest_path, fxf=fxf) == 0   # 2b (최초 핀)
    assert fxf.fetch_forward(upath, dest) == 0                         # 재수집
    assert _run_remedy(vm, monkeypatch, manifest_path, fxf=fxf) == 0   # 2b (재핀)
    assert fxf.fetch_forward(upath, dest) == 0
    assert any(f["path"].startswith("sub/TK01/")
               for f in json.loads(manifest_path.read_text())["files"])


def test_sha_leg_is_the_only_reason_for_refusal(tmp_path, monkeypatch):
    """R12-1(c) leg 격리: 경로가 권위 있는 로그에 실재하므로 출처 leg는
    통과한다 — 거부 사유는 오직 디스크 바이트 ≠ 매니페스트 기록이다.
    변이 `if rel in own and recorded and _sha256_bytes_of(disk) == recorded:`
    → `if rel in own:` 는 이 테스트를 red로 만들어야 한다.

    R15-1: 로그 위치가 정본으로 바뀌어 픽스처가 그쪽에 쓴다 — 단언은 무변경."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    mine = data_dir / "TK01/xbrl/CIK0000001001.json"
    mine.parent.mkdir(parents=True)
    mine.write_bytes(b'{"mine": 1}')
    _canonical_log(fxf, vm, data_dir, manifest_path,
                   [_log_row_for(data_dir, "TK01/xbrl/CIK0000001001.json")])
    # 출처 leg는 통과(로그에 있음), sha leg만 실패하도록 디스크만 드리프트
    mine.write_bytes(b'{"mine": 2}')
    assert "TK01/xbrl/CIK0000001001.json" in fxf._own_writes(), \
        "출처 leg가 통과해야 sha leg를 격리 측정할 수 있다"

    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, data_dir)


def test_own_writes_skips_valid_json_non_object_row(tmp_path, monkeypatch):
    """R12-1(d): 독스트링이 약속한 침묵 스킵 — 유효 JSON 비객체 행에서
    AttributeError로 죽지 않는다.

    R15-1: 로그 위치가 정본으로 바뀌어 픽스처가 그쪽에 쓴다 — 단언은 무변경."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    good = data_dir / "TK01/xbrl/CIK0000001001.json"
    good.parent.mkdir(parents=True)
    good.write_bytes(b"{}")
    log_path = fxf.fetch_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "123\n[1, 2]\n\"str\"\nnot json\n"
        + json.dumps(_log_row_for(data_dir, "TK01/xbrl/CIK0000001001.json")) + "\n",
        encoding="utf-8")
    _commit_canonical_log(fxf)   # R16-2: HEAD 판만이 출처 권위를 준다
    manifest_path.write_text(json.dumps(vm.build_manifest()), encoding="utf-8")
    assert fxf._own_writes() == {"TK01/xbrl/CIK0000001001.json"}


def test_fetch_manifest_guard_allows_disjoint_tickers(tmp_path, monkeypatch):
    """R10-2(a) 반대면: 핀 경로와 서로소인 universe는 정상 진행한다."""
    fxf, data_dir = _manifest_fixture(tmp_path, monkeypatch,
                                      "OTHER/xbrl/CIK0000009999.json",
                                      on_disk=b"{}")
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(2))
    assert fxf.fetch_forward(upath, data_dir) == 0
    assert (data_dir / "TK01/xbrl/CIK0000001001.json").is_file()
    assert fxf.fetch_log_path().is_file()   # R15-1: 정본 위치


def test_refetch_after_manifest_rebuild_is_allowed(tmp_path, monkeypatch):
    """R11-2 (runbook 순서 재현): fetch → verify_manifest --write(2b) →
    같은 universe 재수집. 종전 접두 가드는 자기가 방금 쓴 경로를 핀으로
    보고 창 안 재시도·부분 실패 복구를 영구 차단했다."""
    import fetch_xbrl_facts as fxf
    import verify_manifest as vm
    data_dir = tmp_path / "aaer-data"
    repo = tmp_path / "repo"
    (repo / "data/manifests").mkdir(parents=True)
    manifest_path = repo / "data/manifests/aaer_data_manifest.json"
    manifest_path.write_text(json.dumps({"files": []}), encoding="utf-8")
    monkeypatch.setattr(fxf, "DATA_DIR", data_dir)
    monkeypatch.setattr(fxf, "REPO", repo)
    monkeypatch.setattr(vm, "DATA_DIR", data_dir)
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(2))
    assert fxf.fetch_forward(upath, data_dir) == 0

    # 2b: 방금 수집한 forward 파일 전건이 매니페스트에 핀으로 등재된다
    m = vm.build_manifest()
    manifest_path.write_text(json.dumps(m), encoding="utf-8")
    _commit_canonical_log(fxf)   # R16-2: 2b의 두 번째 단계 (정본 로그 커밋)
    assert any(f["path"].startswith("TK01/") for f in m["files"])

    # 재수집(재시도·절단 청크 재당김·창 후반 최신화)이 여전히 가능해야 한다
    assert fxf.fetch_forward(upath, data_dir) == 0


def test_owner_may_override_pinned_collision_and_it_is_logged(tmp_path, monkeypatch):
    """R11-2: 온전한 핀 스냅샷 덮어쓰기는 소유자 명시 --allow-pinned 로만,
    그리고 그 사실이 수집 로그에 남는다 (R15-1: 정본 위치)."""
    fxf, data_dir = _manifest_fixture(tmp_path, monkeypatch,
                                      "TK01/xbrl/CIK0000001001.json",
                                      on_disk=b'{"july": "snapshot"}')
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    assert fxf.fetch_forward(upath, data_dir, {"TK01"}) == 0
    rows = [json.loads(x) for x in
            fxf.fetch_log_path().read_text(encoding="utf-8").splitlines()]
    override = [r for r in rows if r.get("kind") == "pinned_override"]
    assert override and override[0]["tickers"] == ["TK01"]


# ── 컷오프·완결성·서수 컷 검증 ────────────────────────────────────────────

def test_validate_passes_good_cycle(cycle):
    assert forward_validate.validate(cycle) == []


def test_validate_catches_cutoff_violation(cycle):
    sm = fc.read_json(cycle / "source_manifest.json")
    sm["sources"][0]["filing_date"] = "2026-11-16"
    fc.write_json(cycle / "source_manifest.json", sm)
    assert any("cutoff" in e for e in forward_validate.validate(cycle))


def test_validate_completion_fraction(cycle):
    sc = fc.read_json(cycle / "scores.json")
    # 11 scored + 1 not_scored → PASS (사전 등록 ≥11/12)
    sc["records"][11] = {"record_id": "fw001-r12", "status": "not_scored",
                         "company": {"name": "Test"}}
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []
    # 10 scored → FAIL
    sc["records"][10] = {"record_id": "fw001-r11", "status": "not_scored",
                         "company": {"name": "Test"}}
    fc.write_json(cycle / "scores.json", sc)
    assert any("완료 분율" in e for e in forward_validate.validate(cycle))


def test_validate_decision_state_machine_consistency(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["misstatement_risk_score"] = 80  # state는 review 그대로 → 불일치
    fc.write_json(cycle / "scores.json", sc)
    assert any("서수 컷" in e for e in forward_validate.validate(cycle))


def test_validate_abstain_rule(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0] = make_record("fw001-r01", score=90, suff="insufficient")
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []  # insufficient→abstain이 정답


def test_validate_universe_score_bijection(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["record_id"] = "fw001-r99"
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("누락" in e for e in errs) and any("유니버스 밖" in e for e in errs)


# ── §6 전 필드 계약 + 교차 대조 (fail-closed 전환, TASK_FWD 1) ────────────

def test_scored_at_iso_and_window_enforced(cycle):
    """R7-17: 비ISO·창 밖 scored_at은 레코드 오류 — 창 내 정상값은 무오류."""
    for bad, frag in (("not-a-date", "ISO datetime 아님"),
                      ("2026-11-30T00:00:00+00:00", "실행 창 밖"),
                      ("2026-11-01", "실행 창 밖")):
        sc = fc.read_json(cycle / "scores.json")
        sc["records"][0]["scored_at"] = bad
        fc.write_json(cycle / "scores.json", sc)
        errs = forward_validate.validate(cycle)
        assert any("scored_at" in e and frag in e for e in errs), (bad, errs[:5])
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["scored_at"] = "2026-11-16T09:00:00+00:00"
    fc.write_json(cycle / "scores.json", sc)
    assert not any("scored_at" in e for e in forward_validate.validate(cycle))


def test_every_protocol_pin_is_rechecked_against_the_live_file(cycle):
    """R12-8: prepare는 7건을 핀하는데 validate는 PIN_FILES 2건만 재대조했다 —
    무검증 5건에 `pipeline/cli_client.py`(호출 코드 자체)가 있었다. 실측
    당시 5건 중 3건이 이미 드리프트한 상태였다."""
    proto = (cycle / "PROTOCOL.md").read_text(encoding="utf-8")
    corrupted = proto.replace(
        fc.sha256_file(REPO_ROOT / "pipeline/cli_client.py"), "0" * 64)
    assert corrupted != proto, "픽스처가 cli_client.py를 핀하지 않는다"
    (cycle / "PROTOCOL.md").write_text(corrupted, encoding="utf-8")
    errs = forward_validate.validate(cycle)
    assert any("pipeline/cli_client.py" in e and "라이브 파일 해시" in e
               for e in errs), errs


def test_a_new_pin_source_cannot_land_outside_the_check(cycle, monkeypatch):
    """R12-8: 핀 목록이 늘었는데 validate가 모르면 그 파일은 조용히 무검증이
    된다 — 파싱된 핀 집합이 PIN_SOURCES와 같아야 함을 강제한다."""
    monkeypatch.setattr(forward_prepare, "PIN_SOURCES",
                        forward_prepare.PIN_SOURCES + ["docs/HANDOFF.md"])
    errs = forward_validate.validate(cycle)
    assert any("핀 부재" in e and "docs/HANDOFF.md" in e for e in errs), errs


def test_validate_window_compares_in_et(cycle):
    """R10-8: 창은 ET 정의(PROTOCOL) — 마지막 창일 저녁 배치의 UTC 기록
    (다음 UTC 날짜)은 적법, 실제 창 밖 UTC 기록은 여전히 오류."""
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["scored_at"] = "2026-11-23T01:00:00+00:00"  # 11-22 20:00 ET
    fc.write_json(cycle / "scores.json", sc)
    assert not any("실행 창 밖" in e for e in forward_validate.validate(cycle))
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["scored_at"] = "2026-11-24T12:00:00+00:00"  # 11-24 07:00 ET
    fc.write_json(cycle / "scores.json", sc)
    assert any("실행 창 밖" in e for e in forward_validate.validate(cycle))


def test_validate_full_record_contract_fields(cycle):
    for field in ("schema_sha256", "scored_at"):
        sc = fc.read_json(cycle / "scores.json")
        del sc["records"][0][field]
        fc.write_json(cycle / "scores.json", sc)
        assert any(field in e for e in forward_validate.validate(cycle)), field
    for field in ("benign_alternative_explanations", "affected_account_areas",
                  "top_signals"):
        sc = fc.read_json(cycle / "scores.json")
        del sc["records"][0][field]
        fc.write_json(cycle / "scores.json", sc)
        assert any(field in e for e in forward_validate.validate(cycle)), field


def test_validate_empty_arrays_are_legal(cycle):
    # R10-5: top_signals 포함 — 스키마상 []는 적법한 핀 모델 출력이며
    # falsy 검사가 정규 봉인을 막아서는 안 된다
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["benign_alternative_explanations"] = []
    sc["records"][0]["affected_account_areas"] = []
    sc["records"][0]["top_signals"] = []
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []


# ── R13-1: 봉인되는 자유서술의 INV-13 게이트 ──────────────────────────────

@pytest.mark.parametrize("field", ["top_signals", "affected_account_areas"])
@pytest.mark.parametrize("text", [
    "CL1 receivables outrun revenue — possible fraud in the reserve roll",
    "CL3 매출채권 급증과 매출 정체 — 분식 가능성",
    "CL6 충당금이 사업 확대에도 감소 — 조작 정황",
    "CL2 capitalization pattern suggests manipulation of the allowance",
    # 면책 문맥도 위반이다 — INV-13은 단어 사용 자체를 금지한다
    "CL4 margin trend is explained by the acquisition rather than fraud, "
    "but adds governance/reporting-quality uncertainty",
])
def test_fraud_word_in_sealed_free_text_blocks_the_seal(cycle, field, text):
    """R13-1(b)(c): 금지어 4종 전건 + 영/한 + 면책 문맥까지 봉인 전에 막힌다.

    변이 — validate()에서 `errs += fraud_word_errors(r)` 한 줄을 지우면
    이 테스트 전건(10건)이 red가 된다.
    """
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0][field] = [text]
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert [e for e in errs if "INV-13" in e and field in e], errs


def test_clean_free_text_still_seals(cycle):
    """R13-1: 게이트가 정상 출력을 막지 않는다 (over-blocking 대조군)."""
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["top_signals"] = ["CL1", "CL3"]
    sc["records"][0]["affected_account_areas"] = ["revenue", "receivables"]
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []


def test_inv13_gate_scope_is_limited_to_forward_records():
    """R13-1(d): runs/ 하위 회고 레코드는 AAER 집행 대상 기업이라 INV-13
    적용 대상이 아니다 — 게이트가 그 트리로 번지면 동결 산출물이 사후에
    적색이 된다. 실제 회고 레코드가 금지어를 담고 있음을 확인하고, 게이트가
    forward 경로 한 곳에만 배선돼 있음을 정적으로 고정한다."""
    retro = REPO_ROOT / "runs/draw_k3/w1_controls/draw_3/case_22.json"
    signals = " ".join(json.loads(retro.read_text(encoding="utf-8"))
                       ["overall"]["top_signals"]).lower()
    assert [w for w in forward_validate.FRAUD_WORDS if w in signals], \
        "회고 기준선이 사라졌다면 이 테스트의 전제를 다시 확인해야 한다"
    wired = {p.relative_to(REPO_ROOT).as_posix()
             for root in ("pipeline", "tools", "scoring", "analysis", "aaer_eval")
             for p in (REPO_ROOT / root).rglob("*.py")
             if "fraud_word_errors" in p.read_text(encoding="utf-8")}
    assert wired == {"tools/forward_validate.py", "tools/test_forward_tools.py"}


# ── R14-1: 봉인 커밋이 함께 싣는 러너 출력 원본의 INV-13 게이트 ───────────

def _cycle_with_runs(cycle, tmp_path, name, mutate=None):
    """(runs 디렉토리, 변조 대상 rid) — 레코드는 러너 출력에서 재파생하고
    run_output_sha256도 실측으로 다시 잡으므로, 다른 leg(해시·재파생)는
    침묵한 채 새 leg만 발화한다."""
    runs = tmp_path / name
    runs.mkdir()
    records = []
    for i in range(1, 13):
        rid = f"fw001-r{i:02d}"
        out = make_run_output(rid)
        if mutate is not None and i == 1:
            mutate(out)
        out_path = runs / f"{rid}.json"
        out_path.write_text(json.dumps(out), encoding="utf-8")
        meta = {"record_id": rid, "name": f"Test Co {i}", "ticker": f"TK{i:02d}",
                "cik": f"{1000 + i:010d}"}
        records.append(forward_assemble.assemble_record(
            meta, out, fc.sha256_file(out_path)))
    fc.write_json(cycle / "scores.json", {"records": records})
    return runs, "fw001-r01"


def _put_evidence_quote(out):
    out["checklist"][0]["evidence"] = [
        {"quote": "AR=1,234M (FY2026) — consistent with revenue manipulation",
         "source_accession_no": "0000000000-26-000001", "location": "AR (FY2026)"}]


def _put_mechanism_prose(out):
    out["mechanism_hypotheses"][0]["accounting_treatment"] = \
        "충당금 환입을 통한 이익 조작으로 보인다"


def _put_overall_signal(out):
    out["overall"]["top_signals"] = ["CL1 possible fraud in the reserve roll"]


@pytest.mark.parametrize("mutate, jpath", [
    (_put_evidence_quote, "$.checklist[0].evidence[0].quote"),
    (_put_mechanism_prose, "$.mechanism_hypotheses[0].accounting_treatment"),
    (_put_overall_signal, "$.overall.top_signals[0]"),
])
def test_fraud_word_anywhere_in_runner_output_blocks_the_seal(
        cycle, tmp_path, monkeypatch, capsys, mutate, jpath):
    """R14-1(a): R13-1의 게이트는 scores.json의 두 필드만 본다. 봉인 커밋은
    러너 출력 원본을 함께 push하고 universe.json이 record_id를 실명 기업에
    잇는다 — 세 곳(체크리스트 인용·기제 서술·overall)에서 각각 exit 1이며
    레코드·파일명·JSON 경로를 모두 지목해야 소유자가 결정할 수 있다."""
    runs, rid = _cycle_with_runs(cycle, tmp_path, f"runs_{mutate.__name__}", mutate)
    monkeypatch.setattr(sys, "argv",
                        ["x", "--cycle", str(cycle), "--runs", str(runs)])
    assert forward_validate.main() == 1
    out = capsys.readouterr().out
    hit = [ln for ln in out.splitlines() if "R14-1" in ln]
    assert len(hit) == 1, out
    assert rid in hit[0] and f"{rid}.json" in hit[0] and jpath in hit[0], hit


def test_runner_output_gate_is_independent_of_the_scores_json_gate(cycle, tmp_path):
    """R14-1(b): 두 leg는 서로를 대신하지 못한다. 러너 출력에만 있고 레코드로
    복사되지 않는 필드(체크리스트 인용·기제 서술)를 쓰면 R13-1 leg는 침묵한
    채 새 leg만 발화한다 — 반대 방향(R13-1 전용)은 runs 없이 도는
    test_fraud_word_in_sealed_free_text_blocks_the_seal가 고정한다."""
    runs, rid = _cycle_with_runs(cycle, tmp_path, "runs_iso", _put_evidence_quote)
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert [e for e in errs if "R14-1" in e and rid in e], errs
    assert not [e for e in errs if "R13-1" in e], errs
    # 다른 leg(해시·재파생·서수 컷)는 이 픽스처에서 침묵한다
    assert not [e for e in errs if "R14-1" not in e], errs


def test_clean_runner_output_still_seals(cycle, tmp_path):
    """R14-1(c) over-blocking 대조군: 금지어 없는 출력은 그대로 통과한다."""
    runs, _ = _cycle_with_runs(cycle, tmp_path, "runs_clean")
    assert forward_validate.validate(cycle, runs_dir=runs) == []


def test_validate_cited_source_must_be_in_manifest(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["cited_sources"] = ["0000000000-26-999999"]
    fc.write_json(cycle / "scores.json", sc)
    assert any("source_manifest 미등재" in e for e in forward_validate.validate(cycle))
    # URL 내 대시 제거형 출현도 등재로 인정
    sm = fc.read_json(cycle / "source_manifest.json")
    sm["sources"].append({"url": "https://www.sec.gov/Archives/000000000026999999/x.htm",
                          "filing_date": "2026-11-14", "retrieval_date": "2026-11-15",
                          "sha256": "z", "description": "d"})
    fc.write_json(cycle / "source_manifest.json", sm)
    assert forward_validate.validate(cycle) == []


def test_validate_company_cik_must_match_universe(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["company"]["cik"] = "7777777"
    fc.write_json(cycle / "scores.json", sc)
    assert any("universe CIK" in e for e in forward_validate.validate(cycle))


# ── prepare fail-closed 전환 (TASK_FWD 2) ────────────────────────────────

def test_prepare_refuses_after_seal(tmp_path, monkeypatch, capsys):
    """R12-3: 이름이 약속하는 성질(봉인 후 거부)을 실제로 시험한다 —
    종전 픽스처는 MANIFEST만 두어 새 술어 하에서 '잔여물'이었고, PROTOCOL.md가
    있어 R9-7 가드가 먼저 발화했다. 즉 봉인 가드를 통째로 지워도 통과했다."""
    import forward_prepare as fp
    c = tmp_path / "cycle_sealed"
    c.mkdir()
    proto_before = "sealed proto"
    (c / "PROTOCOL.md").write_text(proto_before, encoding="utf-8")
    (c / "MANIFEST.sha256").write_text("x  PROTOCOL.md\n", encoding="utf-8")
    (c / "SEAL_RECORD.md").write_text("- status: sealed\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(c)])
    with pytest.raises(SystemExit):
        fp.main()
    # 거부 사유가 봉인이어야 한다 (R9-7의 PROTOCOL.md 가드가 아니라)
    assert "봉인 완결" in capsys.readouterr().out
    assert (c / "PROTOCOL.md").read_text(encoding="utf-8") == proto_before


def test_prepare_fails_on_missing_pin_source(tmp_path, monkeypatch):
    import forward_prepare as fp
    monkeypatch.setattr(fp, "PIN_SOURCES", fp.PIN_SOURCES + ["nonexistent/ghost.py"])
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(tmp_path / "cycle_new")])
    with pytest.raises(SystemExit):
        fp.main()
    assert not (tmp_path / "cycle_new" / "PROTOCOL.md").exists()


def test_prepare_fails_on_unresolved_model_pin(tmp_path, monkeypatch):
    import forward_prepare as fp
    monkeypatch.setattr(fp, "evaluatee_model", lambda: "UNRESOLVED")
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(tmp_path / "cycle_new")])
    with pytest.raises(SystemExit):
        fp.main()
    assert not (tmp_path / "cycle_new" / "PROTOCOL.md").exists()


# ── enumerate fail-closed + 창 경계 (TASK_FWD 3) ─────────────────────────

def _write_submissions(snap, cik, dates_10k, dates_10q):
    forms = ["10-K"] * len(dates_10k) + ["10-Q"] * len(dates_10q)
    dates = dates_10k + dates_10q
    fc.write_json(snap / f"submissions_CIK{cik}.json", {
        "sic": "3674", "name": f"Co {cik}", "tickers": [f"T{cik[-2:]}"],
        "filings": {"recent": {"form": forms, "filingDate": dates,
                               "items": [""] * len(forms),
                               "isXBRL": [1] * len(forms)}}})


def test_enumerate_trailing_window_is_bounded_by_t0(tmp_path, monkeypatch):
    import forward_enumerate as fe
    snap = tmp_path / "snap"
    snap.mkdir()
    monkeypatch.setattr(fe, "SNAP", snap)
    cik = "0000009001"
    # 10-K는 창 안, 10-Q 전건이 T0(2026-07-20) 이후 → q_recent=0 → 배제되어야 한다
    _write_submissions(snap, cik, ["2025-01-01", "2024-09-01"],
                       ["2026-08-01", "2026-09-01", "2026-10-01", "2026-11-01",
                        "2026-12-01", "2027-01-01"])
    reason, _ = fe.check_candidate(cik, offline=True)
    assert reason == "form_requirement"


# ── R15-2: 사전 등록 유니버스 선정 술어의 실행 가능한 잠금 ────────────────
#
# universe.json은 SEALED_FILE이자 "12곳은 사전 등록된 기계 규칙으로 뽑혔고
# 손으로 고른 것이 아니다"라는 공개 주장의 증거다. 그런데 그 규칙을 만드는
# check_candidate의 여섯 줄(§1-1 외국 발행인 · §2-1 4.02 오염 격리 · §1-3
# XBRL 이력 · §1-4 float ≥ $1B · §2-2 Cycle-1 자기오염 · §3 랭킹)은 어느
# 것을 지워도 스위트가 0 red였다 — 전수 커버는 T₀ 스냅샷 2507건 부재로 skip
# 되는 두 테스트뿐이었기 때문이다 (OB-3, 소유자 커스터디 결정 대기).
#
# 아래는 스냅샷도 네트워크도 필요 없는 픽스처 구동 잠금이다: OB-3이 가리고
# 있던 커버리지 구멍은 OB-3의 해소를 기다리지 않아도 메울 수 있다.

_WINDOW_10K = ["2025-01-01", "2024-09-01"]          # 창 안 10-K 2건 (≥1 필요)
_WINDOW_10Q = ["2025-01-02", "2025-04-02", "2025-07-02",
               "2025-10-02", "2026-01-02", "2026-04-02"]  # 창 안 10-Q 6건 (≥2)


def _enumerate_snapshot(snap, cik, *, float_usd=2.0e9, extra_filings=(),
                        non_xbrl=0):
    """§1·§2 전 조건을 통과하는 기준 후보 스냅샷 (_write_submissions 기반).

    각 테스트는 이 기준선이 'ok'임을 먼저 확인한 뒤 **축 하나만** 무너뜨린다 —
    그래야 배제 사유가 그 축의 것임을 격리 측정할 수 있다 (R13-4 판례).
    기준선의 XBRL 제출은 정확히 8건(10-K 2 + 10-Q 6)으로 §1-3 하한과 같으므로,
    non_xbrl=1이면 그 leg만 무너진다."""
    _write_submissions(snap, cik, list(_WINDOW_10K), list(_WINDOW_10Q))
    path = snap / f"submissions_CIK{cik}.json"
    sub = fc.read_json(path)
    recent = sub["filings"]["recent"]
    for i in range(non_xbrl):
        recent["isXBRL"][-(i + 1)] = 0
    for row in extra_filings:
        recent["form"].append(row.get("form", "8-K"))
        recent["filingDate"].append(row.get("filingDate", "2025-06-01"))
        recent["items"].append(row.get("items", ""))
        recent["isXBRL"].append(row.get("isXBRL", 0))
    fc.write_json(path, sub)
    fc.write_json(snap / f"float_CIK{cik}.json",
                  {"units": {"USD": [{"end": "2026-06-30", "val": float_usd}]}})
    return path


@pytest.fixture
def enumerate_snap(tmp_path, monkeypatch):
    import forward_enumerate as fe
    snap = tmp_path / "snap"
    snap.mkdir()
    monkeypatch.setattr(fe, "SNAP", snap)
    return fe, snap


def test_baseline_candidate_passes_every_screen(enumerate_snap):
    """R15-2 통제: 기준선이 'ok'가 아니면 아래 배제 테스트들은 아무것도
    변별하지 못한다 (어떤 변경도 같은 사유를 낸다)."""
    fe, snap = enumerate_snap
    _enumerate_snapshot(snap, "0000009101")
    reason, info = fe.check_candidate("0000009101", offline=True)
    assert reason == "ok"
    assert info["float_usd"] == 2.0e9


def test_check_candidate_excludes_foreign_filer(enumerate_snap):
    """§1-1: 20-F/40-F/6-K 제출 이력이 있으면 미국 국내 발행인 프레임 밖."""
    fe, snap = enumerate_snap
    cik = "0000009102"
    _enumerate_snapshot(snap, cik, extra_filings=[
        {"form": "20-F", "filingDate": "2025-03-01"}])
    assert fe.check_candidate(cik, offline=True)[0] == "foreign_filer"


def test_check_candidate_excludes_402_restater(enumerate_snap):
    """§2-1 오염 격리: 창 안 8-K Item 4.02(비신뢰 선언)는 사후 트랙 —
    이 스크린이 사라지면 재작성 발표 기업이 유니버스에 들어온다."""
    fe, snap = enumerate_snap
    cik = "0000009103"
    _enumerate_snapshot(snap, cik, extra_filings=[
        {"form": "8-K", "filingDate": "2025-06-01", "items": "4.02"}])
    assert fe.check_candidate(cik, offline=True)[0] == \
        "contamination_402_posthoc_track"


def test_check_candidate_excludes_short_xbrl_history(enumerate_snap):
    """§1-3: XBRL 제출 8건·10-K 2건 하한 — 기준선은 정확히 그 경계에 있다."""
    fe, snap = enumerate_snap
    cik = "0000009104"
    _enumerate_snapshot(snap, cik, non_xbrl=1)
    assert fe.check_candidate(cik, offline=True)[0] == "xbrl_history"


def test_check_candidate_excludes_float_below_1b(enumerate_snap):
    """§1-4: EntityPublicFloat ≥ $1B — 경계 바로 아래는 배제."""
    fe, snap = enumerate_snap
    cik = "0000009105"
    _enumerate_snapshot(snap, cik, float_usd=9.99e8)
    assert fe.check_candidate(cik, offline=True)[0] == "float_below_1b"


def _run_enumerate(fe, snap, monkeypatch, tmp_path, rows, burned=()):
    """rows: [(cik, float_usd)] — 한 SIC 버킷으로 main()을 완주시킨다."""
    monkeypatch.setattr(fe, "SIC_SET", ["3674"])
    monkeypatch.setattr(fe, "_provenance", [])
    monkeypatch.setattr(fe, "_fetch_errors", [])
    monkeypatch.setattr(fe, "cycle1_ciks", lambda: set(burned))
    for cik, float_usd in rows:
        _enumerate_snapshot(snap, cik, float_usd=float_usd)
    (snap / "sic_3674_p0.xml").write_text(
        "".join(f"<cik>{c}</cik>" for c, _ in rows), encoding="utf-8")
    out = tmp_path / "universe_out.json"
    monkeypatch.setattr(sys, "argv", ["x", "--out", str(out)])
    assert fe.main() == 0
    return fc.read_json(out)


def test_burned_cik_is_excluded_as_cycle1_self_contamination(
        enumerate_snap, tmp_path, monkeypatch):
    """§2-2: Cycle-1에서 이미 평가된 회사는 자기 오염 — 배제 사유가 집계에
    남아야 감사 흔적이 성립한다 (universe.excluded_by_reason)."""
    fe, snap = enumerate_snap
    burned = "0000009200"
    rows = [(f"{9200 + i:010d}", 2.0e9 + i) for i in range(13)]
    universe = _run_enumerate(fe, snap, monkeypatch, tmp_path, rows,
                              burned=[burned])
    assert universe["excluded_by_reason"]["cycle1_self_contamination"] == 1
    assert burned not in [r["cik"] for r in universe["selected"]]
    assert burned not in [r["cik"] for r in universe["alternates"]]


def test_bucket_ranking_is_float_descending_then_cik_ascending(
        enumerate_snap, tmp_path, monkeypatch):
    """§3: 버킷 안 정렬은 float 내림차순, 동률은 CIK 오름차순.

    정렬 키 `-r["float_usd"]`의 부호가 뒤집히면 12곳 전체가 다른 회사로
    바뀐다 — 그런데 그 변이는 0 red였다 (R15-2 실측)."""
    fe, snap = enumerate_snap
    # 동률 쌍(9302·9303)을 가운데 두고, 가장 큰 float은 가장 큰 CIK에 준다 —
    # CIK 오름차순으로만 정렬해도 통과하는 배치를 피한다.
    floats = {"0000009301": 3.0e9, "0000009302": 5.0e9, "0000009303": 5.0e9,
              "0000009304": 9.0e9}
    rows = [(c, floats.get(c, 1.0e9 + i))
            for i, c in enumerate(f"{9300 + n:010d}" for n in range(1, 13))]
    universe = _run_enumerate(fe, snap, monkeypatch, tmp_path, rows)
    ranked = [r["cik"] for r in universe["selected"]]
    assert ranked[0] == "0000009304", "최상위 float이 1위가 아니다"
    assert ranked[1:3] == ["0000009302", "0000009303"], \
        "동률 float이 CIK 오름차순으로 갈리지 않았다"
    vals = [r["float_usd"] for r in universe["selected"]]
    assert vals == sorted(vals, reverse=True), "float 내림차순이 깨졌다"
    assert [r["selection_rank"] for r in universe["selected"]] == list(range(1, 13))


def test_enumerate_fails_closed_on_fetch_error(tmp_path, monkeypatch, capsys):
    import urllib.request
    import forward_enumerate as fe
    snap = tmp_path / "snap"
    snap.mkdir()
    monkeypatch.setattr(fe, "SNAP", snap)
    monkeypatch.setattr(fe, "SIC_SET", ["3674"])
    monkeypatch.setattr(fe, "_provenance", [])
    monkeypatch.setattr(fe, "_fetch_errors", [])
    monkeypatch.setattr(fe, "cycle1_ciks", lambda: set())
    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("timeout")))
    good = [f"{9000 + i:010d}" for i in range(1, 13)]
    bad = "0000009999"  # 스냅샷 부재 → fetch 오류
    atom = "".join(f"<cik>{c}</cik>" for c in good + [bad])
    (snap / "sic_3674_p0.xml").write_text(atom, encoding="utf-8")
    for c in good:
        _write_submissions(snap, c, ["2025-01-01", "2024-09-01"],
                           ["2025-01-02", "2025-04-02", "2025-07-02", "2025-10-02",
                            "2026-01-02", "2026-04-02"])
        fc.write_json(snap / f"float_CIK{c}.json",
                      {"units": {"USD": [{"end": "2026-06-30", "val": 2.0e9}]}})
    monkeypatch.setattr(sys, "argv", ["x", "--out", str(tmp_path / "u.json")])
    assert fe.main() == 1  # 12사 선정 완료여도 fetch 오류가 있으면 실패
    out = capsys.readouterr().out
    assert "selected 12" in out and "fail-closed" in out


# ── R14-3(b): 봉인 대상 파일 목록 자체의 고정 ─────────────────────────────

def test_sealed_files_membership_is_locked(tmp_path):
    """R14-3(b): `SEALED_FILES`에서 이름을 빼도 스위트가 알아채지 못했다 —
    실측: `scores.json` 제거는 1 red였지만 `universe.json`·
    `source_manifest.json` 제거는 각각 723 passed(0 red)였고, universe를 뺀
    채 12건 픽스처를 봉인해 `selected[0]`의 cik·ticker·name을 바꿔도
    `forward_verify_seal.main()`이 `PASS — 봉인 무결성`으로 0을 반환했다.

    범위를 정직하게: runs/를 가진 검증자가 `forward_validate --runs`를 다시
    돌리면 바뀐 cik·name은 여전히 잡힌다. 아무도 못 잡는 것은 열거 감사
    흔적(`alternates`·`selection_rank`·`candidate_count`·`excluded_by_reason`·
    `float_usd`·`sic` — "이 12곳은 기계적으로 선정됐고 체리피킹이 아니다"의
    근거)과 `source_manifest.json` 전체(INV-01 증거인 retrieval_date·
    filing_date·url·sha256)다.

    규범 출처는 spec §9 (`specs/FORWARD_WATCHLIST_V1.md`): 그 절은 봉인
    **디렉토리 내용물**(네 파일 + `evidence/` + MANIFEST·SEAL_RECORD·.ots·
    outcome_updates)을 열거한다 — 네 항목짜리 해시 목록을 그대로 옮겨 적은
    것이 아니므로, 목록의 네 이름과 `evidence/` 포함을 함께 고정한다."""
    assert fc.SEALED_FILES == ["PROTOCOL.md", "universe.json",
                               "source_manifest.json", "scores.json"]
    cycle = tmp_path / "cycle_sealed_list"
    (cycle / "evidence").mkdir(parents=True)
    for name in fc.SEALED_FILES:
        (cycle / name).write_text("x", encoding="utf-8")
    (cycle / "evidence" / "note.txt").write_text("e", encoding="utf-8")
    names = [rel for _, rel in fc.sealed_paths(cycle)]
    assert names[:len(fc.SEALED_FILES)] == fc.SEALED_FILES, names
    assert "evidence/note.txt" in names, names


# ── 봉인·검증 왕복 ────────────────────────────────────────────────────────

def seal_argv(cycle):
    """R5-1: 정규 봉인은 runs 디렉토리 실측 재해시가 필수 — 픽스처 러너
    출력을 만들고 scores의 run_output_sha256를 실제 해시로 맞춘다."""
    runs = cycle.parent / "runs_t"
    if not runs.exists():
        runs.mkdir()
        sc = fc.read_json(cycle / "scores.json")
        for r in sc["records"]:
            # R11-4: 레코드가 이 출력의 재파생과 일치해야 봉인이 통과한다
            path = runs / f"{r['record_id']}.json"
            path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
            r["run_output_sha256"] = fc.sha256_file(path)
        fc.write_json(cycle / "scores.json", sc)
    return ["x", "--cycle", str(cycle), "--runs", str(runs)]


def run_seal(cycle, capsys=None):
    sys.argv = ["forward_seal.py", "--cycle", str(cycle)]
    return forward_seal.main()


def stamp_ots(cycle):
    """R11-3: 정규 봉인의 OTS 앵커 — 실제 stamp는 네트워크·클라이언트가 필요
    하므로 테스트에서는 형식(매직)을 갖춘 앵커 파일을 재현한다 (R12-4:
    존재만으로는 더 이상 통과하지 않는다)."""
    import forward_verify_seal as fvs
    (cycle / "MANIFEST.sha256.ots").write_bytes(fvs.OTS_MAGIC + b"\x00fixture")


def test_seal_verify_roundtrip_and_tamper(cycle, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    assert (cycle / "MANIFEST.sha256").exists() and (cycle / "SEAL_RECORD.md").exists()

    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    stamp_ots(cycle)
    assert forward_verify_seal.main() == 0

    # 변조 검출
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["misstatement_risk_score"] = 44
    fc.write_json(cycle / "scores.json", sc)
    assert forward_verify_seal.main() == 1
    out = capsys.readouterr().out
    assert "변조됨: scores.json" in out


def test_seal_refuses_unshippable_evidence_file(cycle, monkeypatch, capsys):
    """R11-6: evidence/에 떨어진 .DS_Store(Finder로 폴더를 열면 생긴다)는
    해시되어 MANIFEST에 실리지만 `git add`는 건너뛴다 — push 이후 모든
    클론에서 검증이 영구 실패하고, 재봉인 금지라 교정 경로가 없다."""
    (cycle / "evidence").mkdir(exist_ok=True)
    (cycle / "evidence/.DS_Store").write_bytes(b"\x00mac")
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    with pytest.raises(SystemExit):
        forward_seal.main()
    assert ".DS_Store" in capsys.readouterr().out
    assert not (cycle / "MANIFEST.sha256").exists(), "거부인데 매니페스트가 쓰였다"

    (cycle / "evidence/.DS_Store").unlink()
    assert forward_seal.main() == 0
    assert (cycle / "MANIFEST.sha256").exists()


def test_shippable_evidence_file_is_sealed_normally(cycle):
    """R11-6 반대면: 무시 규칙에 걸리지 않는 증거 파일은 그대로 봉인된다."""
    (cycle / "evidence").mkdir(exist_ok=True)
    (cycle / "evidence/note.txt").write_text("evidence", encoding="utf-8")
    assert fc.unshippable_sealed_files(cycle, include_runs=False) == []
    assert "evidence/note.txt" in fc.manifest_text(cycle)


# R12-2 계열 경계: 비-ASCII · 따옴표 · 역슬래시 · 개행 — 전부 종전
# 줄 단위 check-ignore가 C-인용 때문에 놓치던 이름들 (lens B 실측 우회).
@pytest.mark.parametrize("relname", [
    "evidence/.DS_Store",             # ASCII 기준선 (종전에도 잡힘)
    "evidence/증거/.DS_Store",         # 비-ASCII
    'evidence/we"ird/.DS_Store',      # 따옴표
    "evidence/back\\slash/.DS_Store",  # 역슬래시
    "evidence/a\nb/.DS_Store",        # 개행 (--stdin 줄 프로토콜 자체가 깨진다)
])
def test_seal_refuses_ignored_names_across_quoting_classes(cycle, relname):
    """R12-2: git이 '무시됨'이라 답한 파일을 문자열 대조 실수로 흘리면
    봉인이 되돌릴 수 없이 깨진다. `-z`(NUL) 프로토콜로 인용을 없앤다."""
    target = cycle / relname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"\x00mac")
    bad = fc.unshippable_sealed_files(cycle, include_runs=False)
    assert any(".DS_Store" in b for b in bad), f"{relname!r} 우회: {bad}"


def test_non_ignored_lookalike_name_stays_shippable(cycle):
    """R12-2 과차단 방지: `.DS_Store거`는 무시 규칙에 걸리지 않는다 —
    `git add -A`가 실제로 추적한다(스크래치 저장소 실측). 실어 나를 수 있는
    파일을 막으면 정당한 봉인을 세우게 되므로 통과해야 한다."""
    (cycle / "evidence").mkdir(exist_ok=True)
    (cycle / "evidence/.DS_Store거").write_bytes(b"x")
    assert fc.unshippable_sealed_files(cycle, include_runs=False) == []


def test_seal_refuses_nested_repo_and_outside_symlink(cycle, tmp_path):
    """R12-2: 무시 규칙 밖의 두 종 — `git add`는 중첩 저장소를 gitlink 하나로
    싣고(내부 파일 미포함), 사이클 밖 심볼릭 링크는 링크만 싣는다. 어느
    쪽이든 매니페스트에는 줄이 있고 클론에는 파일이 없다."""
    ev = cycle / "evidence"
    ev.mkdir(exist_ok=True)
    (ev / "sub/.git").mkdir(parents=True)
    (ev / "sub/.git/config").write_text("[core]\n", encoding="utf-8")
    bad = fc.unshippable_sealed_files(cycle, include_runs=False)
    assert any("중첩 git 저장소" in b for b in bad), bad

    import shutil
    shutil.rmtree(ev / "sub")
    outside = tmp_path / "outside.txt"
    outside.write_text("out", encoding="utf-8")
    (ev / "link.txt").symlink_to(outside)
    bad = fc.unshippable_sealed_files(cycle, include_runs=False)
    assert any("심볼릭 링크" in b for b in bad), bad


def test_unshippable_check_covers_runs_tree(cycle, monkeypatch, tmp_path):
    """R12-2: 봉인 커밋은 runs/forward 출력을 함께 싣고 블라인드 매니페스트는
    runs/ 전체를 해싱한다 — 같은 '해시됐지만 실리지 않음' 피해가 그쪽에서도
    성립하므로 검사 범위에 든다."""
    import subprocess
    fake_repo = tmp_path / "repo"
    (fake_repo / "runs/forward/cycle_t").mkdir(parents=True)
    subprocess.run(["git", "-C", str(fake_repo), "init", "-q"], check=True)
    (fake_repo / ".gitignore").write_text(
        (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    (fake_repo / "runs/forward/cycle_t/leftover.pyc").write_bytes(b"x")
    monkeypatch.setattr(fc, "REPO", fake_repo)
    bad = fc.unshippable_sealed_files(cycle, include_runs=True)
    assert any("leftover.pyc" in b for b in bad), bad


def test_verify_seal_requires_ots_anchor_on_regular_seal(cycle, monkeypatch, capsys):
    """R11-3: 두 앵커 중 tag API 쪽은 서버 기록 시각을 주지 않는다
    (tagger/committer 날짜 = 클라이언트 제출값). 남는 비가역 앵커는 OTS뿐인데
    클라이언트 부재·시간초과 시 pending으로 떨어지고 아무 도구도 .ots 존재를
    확인하지 않았다 — 앵커 0개로 봉인·검증 통과가 가능했다."""
    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0

    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert not (cycle / "MANIFEST.sha256.ots").exists()
    assert forward_verify_seal.main() == 1
    assert "OTS 앵커 부재" in capsys.readouterr().out

    stamp_ots(cycle)
    assert forward_verify_seal.main() == 0


def test_inserted_aborted_line_cannot_flip_verify_seal(cycle, monkeypatch, capsys):
    """R12-4: abort 면제가 미해시 산문(SEAL_RECORD.md)의 부분문자열이면,
    정규 봉인 기록에 한 줄 끼워 넣는 것만으로 앵커 없는 봉인이 exit 1 →
    exit 0으로 뒤집힌다 (lens B 실증). 판정 근거를 매니페스트가 해싱하는
    evidence/ 마커로 옮긴다 — 사후 삽입은 무결성 검사에서 먼저 걸린다."""
    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = cycle / "SEAL_RECORD.md"
    record.write_text("- status: ABORTED (?)\n"
                      + record.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_verify_seal.main() == 1, "산문 한 줄로 앵커 검사가 뒤집혔다"


def test_abort_exemption_rides_on_the_hashed_marker(cycle, monkeypatch):
    """R12-4 반대면: 진짜 abort 봉인은 evidence/ 안의 해시된 마커를 남기고,
    그 근거로 .ots 없이도 통과한다. 마커를 지우면 매니페스트 무결성 검사가
    먼저 발화한다 (판정 근거가 사슬 안에 있다는 뜻)."""
    import forward_verify_seal
    (cycle / "scores.json").unlink()
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--abort", "--reason", "window missed"])
    assert forward_seal.main() == 0
    marker = cycle / "evidence" / forward_seal.ABORT_MARKER
    assert marker.is_file()
    assert marker.name in (cycle / "MANIFEST.sha256").read_text(encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_verify_seal.main() == 0        # abort + .ots 없음 → 통과
    marker.unlink()
    assert forward_verify_seal.main() == 1        # 마커 제거 = 무결성 위반


def test_forged_empty_ots_is_not_accepted_as_an_anchor(cycle, monkeypatch, capsys):
    """R12-4: 0바이트 위조 .ots가 "ots verify" 확언과 함께 통과했다 —
    도구가 존재만 확인했기 때문. 형식(매직)을 보고, 확인하지 못한 것은
    확인하지 못했다고 말한다."""
    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    (cycle / "MANIFEST.sha256.ots").write_bytes(b"")
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_verify_seal.main() == 1
    assert "형식 불일치" in capsys.readouterr().out


def test_seal_record_discloses_receipt_is_outside_the_hash_chain(cycle, monkeypatch):
    """R12-4: push 영수증이 봉인 해시 사슬 밖이라는 사실이 Python 주석에만
    있고 게시 기록에는 없었다 — 제3자에게 '서버 기록'으로 제시되는 파일이
    사후 자유 편집 가능한데 그 사실이 공개되지 않았다."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    section = record.split("## 외부 검증 방법")[1]
    assert "봉인 해시 사슬 밖" in section
    assert "포함되지 않는다" in section


def test_spec_norm_text_no_longer_claims_tag_api_is_server_time():
    """R12-4: 철회한 주장이 SEAL_RECORD가 구현해야 할 규범 원문에 잔존했다 —
    생성 산출물만 고치면 두 게시면 중 하나만 참이 된다."""
    spec = (REPO_ROOT / "specs/FORWARD_WATCHLIST_V1.md").read_text(encoding="utf-8")
    assert "소급 조작 불가" not in spec
    assert "git/refs/tags" not in spec


def test_seal_record_does_not_claim_tag_api_is_server_time(cycle, monkeypatch):
    """R11-3: 게시 문면이 tag API를 '작성자 소급 조작 불가'로 인용하지 않는다
    — 그 필드는 클라이언트가 제출하는 값이다."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    assert "소급 조작 불가" not in record
    assert "git/refs/tags" not in record
    assert "클라이언트가 제출한 값" in record, "태그 날짜의 한계 공개 부재"
    # 앵커 pending은 OTS 줄뿐 아니라 status 줄에도 드러나야 한다
    assert "OTS 앵커 pending" in record.split("- sealed_at")[0]


def test_reseal_refused(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    with pytest.raises(SystemExit):
        forward_seal.main()  # MANIFEST+SEAL_RECORD 존재 → 거부 (spec §3-5)


def test_interrupted_seal_resumes_instead_of_wedging(cycle, monkeypatch):
    """R10-6: ots 단계 중단이 MANIFEST만 남긴 상태 — 재실행이 '재봉인 금지'로
    wedging되지 않고 SEAL_RECORD를 완성한다 (수동 삭제 불요)."""
    argv = seal_argv(cycle)
    (cycle / "MANIFEST.sha256").write_text(fc.manifest_text(cycle),
                                           encoding="utf-8")
    monkeypatch.setattr(sys, "argv", argv)
    assert forward_seal.main() == 0
    assert (cycle / "MANIFEST.sha256").exists()
    assert (cycle / "SEAL_RECORD.md").exists()


def test_interrupt_residue_does_not_wedge_downstream_tools(cycle, monkeypatch, tmp_path):
    """R11-8: SIGHUP이 MANIFEST만 남긴 상태에서 12번째가 재개로 완료되면,
    종전에는 assemble이 '봉인된 사이클'이라 거부하고 seal은 트리 불일치라
    거부해 두 출구가 모두 닫혔다 (R10-6 메시지가 금지한 수동 rm만 남았다).
    잔여물은 봉인이 아니다 — 재조립도 봉인 완결도 가능해야 한다."""
    argv = seal_argv(cycle)
    runs = Path(argv[argv.index("--runs") + 1])
    (cycle / "MANIFEST.sha256").write_text(fc.manifest_text(cycle),
                                           encoding="utf-8")
    # 재개된 러너 출력으로 트리가 바뀐다 (11/12 → 12/12 판형)
    sc = fc.read_json(cycle / "scores.json")
    rid = sc["records"][-1]["record_id"]
    sc["records"][-1] = {"record_id": rid,
                         "company": sc["records"][-1]["company"],
                         "status": "not_scored"}
    fc.write_json(cycle / "scores.json", sc)

    monkeypatch.setattr(sys, "argv", ["forward_assemble.py", "--cycle",
                                      str(cycle), "--runs", str(runs)])
    assert forward_assemble.main() == 0, "잔여물 상태에서 재조립이 막혔다"

    monkeypatch.setattr(sys, "argv", argv)
    assert forward_seal.main() == 0
    assert (cycle / "SEAL_RECORD.md").exists()
    assert (cycle / "MANIFEST.sha256").read_text(encoding="utf-8") == \
        fc.manifest_text(cycle)


def test_sealed_predicate_is_shared_by_downstream_writers(cycle, monkeypatch, capsys):
    """R11-8: 봉인 완결(두 파일)에서는 하류 쓰기 도구가 전부 거부한다 —
    잔여물 판정과 봉인 판정이 도구마다 어긋나지 않게 한 판정식을 공유한다.

    R12-3: prepare 다리는 거부 **사유**까지 단언한다 — 픽스처에 PROTOCOL.md가
    있어 R9-7 가드가 먼저 발화하므로, 사유를 보지 않으면 봉인 술어를 통째로
    지워도 통과하는 공허한 다리였다 (lens B: 가드 삭제 후 582건 전부 green)."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    assert fc.is_sealed(cycle) and fc.seal_residue_notice(cycle) is None

    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--runs", str(cycle.parent / "runs_t")])
    capsys.readouterr()
    assert forward_assemble.main() == 1
    assert "봉인 완결" in capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    with pytest.raises(SystemExit):
        forward_prepare.main()
    assert "봉인 완결" in capsys.readouterr().out, "prepare 거부 사유가 봉인이 아니다"


def test_residue_note_matches_what_each_path_actually_does(cycle, monkeypatch, capsys):
    """R12-3: 잔여물 NOTE는 경로별로 사실이어야 한다 — abort는 validate를
    전혀 돌리지 않는데 종전 문구는 두 경로 모두에 "현재 트리로 검증" 후
    완결한다고 약속했다 (봉인-크리티컬 운영자 표면의 허위 문구).

    abort가 잔여물 위에서 계속 진행하는 것 자체는 의도된 동작이다 (R11-8:
    검증 없이 부분 상태를 동결하는 것이 abort의 계약이고, 그 탈출구까지
    막은 것이 R10-6의 결함이었다) — 여기서 고치는 것은 문구다."""
    (cycle / "MANIFEST.sha256").write_text(fc.manifest_text(cycle), encoding="utf-8")
    (cycle / "scores.json").unlink()  # 검증 통과 불가 상태
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--abort", "--reason", "window missed"])
    capsys.readouterr()
    assert forward_seal.main() == 0
    out = capsys.readouterr().out
    assert "검증 없이" in out, out
    assert "검증·매니페스트 재작성 후 봉인을 완결" not in out, "abort가 돌리지 않는 검증을 약속"


def test_ots_stall_records_pending_and_completes_seal(cycle, monkeypatch):
    """R10-6: ots stamp 시간초과/중단이 봉인을 중단시키지 않는다 — pending
    기록 후 SEAL_RECORD까지 완결 (timeout= 없던 종전엔 무한 대기)."""
    import subprocess as sp
    monkeypatch.setattr(forward_seal.shutil, "which", lambda name: "/fake/ots")
    real_run = sp.run

    def fake_run(cmd, *a, **kw):
        if cmd and cmd[0] == "/fake/ots":
            assert kw.get("timeout"), "ots 호출에 timeout= 부재 (R10-6)"
            raise sp.TimeoutExpired(cmd, kw["timeout"])
        return real_run(cmd, *a, **kw)

    monkeypatch.setattr(forward_seal.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    assert "pending — stamp 미완" in record


def test_seal_refused_on_invalid_cycle(cycle, monkeypatch):
    argv = seal_argv(cycle)
    (cycle / "source_manifest.json").unlink()
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit):
        forward_seal.main()


# ── 결과 append-only ─────────────────────────────────────────────────────

def test_outcome_append_chains_previous_label(cycle, monkeypatch):
    base = ["x", "--cycle", str(cycle), "--record-id", "fw001-r01",
            "--event-date", "2027-03-02", "--event-public-date", "2027-03-02",
            "--source", "acc-x", "--reviewer", "owner", "--rationale", "r"]
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "item_402_nonreliance",
                                             "--new-label", "item_402_nonreliance"])
    scores_before = (cycle / "scores.json").read_bytes()
    assert forward_outcome_append.main() == 0
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "aaer_or_final_enforcement",
                                             "--new-label", "aaer_or_final_enforcement"])
    assert forward_outcome_append.main() == 0
    lines = [json.loads(l) for l in
             (cycle / "outcome_updates.jsonl").read_text().splitlines()]
    assert len(lines) == 2
    assert lines[0]["previous_label"] == "none_observed"
    assert lines[1]["previous_label"] == "item_402_nonreliance"
    assert (cycle / "scores.json").read_bytes() == scores_before  # 원 점수 무접촉


def test_outcome_append_refuses_down_hierarchy(cycle, monkeypatch, capsys):
    """R9-2: spec §7 상향만 — 상위 라벨 뒤 하위 라벨 append는 원장 오염,
    fail-closed. 동일 계층 재기입은 허용."""
    base = ["x", "--cycle", str(cycle), "--record-id", "fw001-r02",
            "--event-date", "2027-03-02", "--event-public-date", "2027-03-02",
            "--source", "acc-x", "--reviewer", "owner", "--rationale", "r"]
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "big_r_restatement",
                                             "--new-label", "big_r_restatement"])
    assert forward_outcome_append.main() == 0
    # 하향 (big_r → none_observed) — 거부, 원장 무추가
    before = (cycle / "outcome_updates.jsonl").read_text()
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "none_observed",
                                             "--new-label", "none_observed"])
    with pytest.raises(SystemExit) as exc:
        forward_outcome_append.main()
    assert exc.value.code == 1
    assert "하향 금지" in capsys.readouterr().out
    assert (cycle / "outcome_updates.jsonl").read_text() == before
    # 동일 계층 재기입 — 허용
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "big_r_restatement",
                                             "--new-label", "big_r_restatement"])
    assert forward_outcome_append.main() == 0
    # 상향 (big_r → aaer) — 허용
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "aaer_or_final_enforcement",
                                             "--new-label", "aaer_or_final_enforcement"])
    assert forward_outcome_append.main() == 0


# ── scores 조립 (사전 등록 유도 규칙) ─────────────────────────────────────

def test_assemble_derivation_rules():
    import forward_assemble as fa
    mk = lambda finding, conf: {"finding": finding, "confidence": conf}
    assert fa.derive_sufficiency([mk("flag", "high")] * 10) == "sufficient"
    assert fa.derive_sufficiency([mk("insufficient_data", "low")] * 3
                                 + [mk("flag", "high")] * 7) == "partial"
    assert fa.derive_sufficiency([mk("insufficient_data", "low")] * 6
                                 + [mk("flag", "high")] * 4) == "insufficient"
    assert fa.derive_confidence([mk("f", "high")] * 3) == "high"
    assert fa.derive_confidence([mk("f", "high"), mk("f", "low")]) == "medium"
    assert fa.derive_state(70, "sufficient") == "flag"
    assert fa.derive_state(69, "sufficient") == "review"
    assert fa.derive_state(39, "partial") == "no_flag"
    assert fa.derive_state(95, "insufficient") == "abstain"


def test_assemble_record_roundtrips_validate(cycle):
    import forward_assemble as fa
    meta = {"record_id": "fw001-r01", "name": "Test Co", "ticker": "T",
            "cik": "0000001001"}
    out = {"misstatement_probability": 72, "model": "claude-sonnet-5",
           # R10-8: 검증이 ET로 환산한다 — 15:00Z = 10:00 ET (창 내 명백).
           # 종전 00:00Z는 ET로 11-14 19:00, 컷오프 전이라 적법하게 거부된다.
           "run_id": "x", "run_timestamp": "2026-11-15T15:00:00Z",
           "checklist": [{"finding": "flag", "confidence": "high"}] * 5,
           "mechanism_hypotheses": [{"affected_line_items": ["revenue", "AR"]}],
           "overall": {"top_signals": ["CL1"]},
           "documents_used": [{"accession_no": "0000000000-26-000001"}],
           "fingerprint": {"system_prompt_sha256": "f" * 64,
                           "schema_sha256": SCHEMA_SHA,
                           "pipeline_commit": "a" * 40,
                           "model_requested": "claude-sonnet-5"}}
    r = fa.assemble_record(meta, out, out_sha256="c" * 64)
    assert r["misstatement_risk_score"] == 72 and r["decision_state"] == "flag"
    assert r["affected_account_areas"] == ["revenue", "AR"]
    assert fa.assemble_record(meta, None)["status"] == "not_scored"
    # 조립 레코드가 forward_validate 검사를 통과하는 형태인지
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0] = r
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []


def test_outcome_append_rejects_unknown_record(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--record-id", "fw001-r99",
                                      "--event-date", "2027-03-02",
                                      "--event-public-date", "2027-03-02", "--event-type",
                                      "sec_complaint", "--source", "s", "--new-label",
                                      "sec_complaint", "--reviewer", "o", "--rationale", "r"])
    with pytest.raises(SystemExit):
        forward_outcome_append.main()


def test_outcome_append_rejects_non_iso_dates(cycle, monkeypatch):
    """R3-10(b): append-only 원장에 비ISO 날짜 유입 금지 — 선파싱 거부."""
    for bad_flag in ("--event-date", "--event-public-date"):
        argv = ["x", "--cycle", str(cycle), "--record-id", "fw001-r01",
                "--event-date", "2027-03-02", "--event-public-date", "2027-03-02",
                "--event-type", "sec_complaint", "--source", "s", "--new-label",
                "sec_complaint", "--reviewer", "o", "--rationale", "r"]
        argv[argv.index(bad_flag) + 1] = "03/02/2027"
        monkeypatch.setattr(sys, "argv", argv)
        with pytest.raises(SystemExit):
            forward_outcome_append.main()
    assert (cycle / "outcome_updates.jsonl").read_text(encoding="utf-8") == ""


def test_assemble_refuses_after_seal(cycle, monkeypatch):
    """R3-10(a): 봉인 후 재조립은 sealed scores.json을 재작성한다 — 거부."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    sealed_bytes = (cycle / "scores.json").read_bytes()
    import forward_assemble
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--runs", str(cycle / "no_runs")])
    assert forward_assemble.main() == 1
    assert (cycle / "scores.json").read_bytes() == sealed_bytes


# ── R2-8 (INV-22): 봉인 후 불변성 자동 게이트 ─────────────────────────────

def test_real_cycles_seal_integrity_gate():
    """실존하는 모든 forward/cycle_*/MANIFEST.sha256를 pytest 스위프마다
    재검증한다. 봉인 전에는 공진(vacuous pass) — 게이트가 봉인을 선행해야
    봉인 직후부터 in-place 변조가 CI에서 잡힌다는 것이 요점."""
    for manifest in sorted((fc.REPO / "forward").glob("cycle_*/MANIFEST.sha256")):
        cycle = manifest.parent
        assert manifest.read_text(encoding="utf-8") == fc.manifest_text(cycle), (
            f"INV-22 위반: 봉인 후 변조 — {cycle.relative_to(fc.REPO)} "
            "(정정은 ERRATA/신규 사이클 경유, in-place 수정 금지)")


def test_sealed_fixture_tamper_fires_the_gate(tmp_path):
    """픽스처 봉인 사이클로 게이트 발화 증명: 변조·추가 각각 red."""
    cycle = tmp_path / "cycle_099"
    cycle.mkdir()
    (cycle / "PROTOCOL.md").write_text("protocol v1\n", encoding="utf-8")
    (cycle / "universe.json").write_text("{}\n", encoding="utf-8")
    manifest = cycle / "MANIFEST.sha256"
    manifest.write_text(fc.manifest_text(cycle), encoding="utf-8")
    assert manifest.read_text(encoding="utf-8") == fc.manifest_text(cycle)

    (cycle / "PROTOCOL.md").write_text("protocol v2 (tampered)\n", encoding="utf-8")
    assert manifest.read_text(encoding="utf-8") != fc.manifest_text(cycle)

    (cycle / "PROTOCOL.md").write_text("protocol v1\n", encoding="utf-8")
    assert manifest.read_text(encoding="utf-8") == fc.manifest_text(cycle)
    evidence = cycle / "evidence"
    evidence.mkdir()
    (evidence / "late_addition.txt").write_text("added after seal\n", encoding="utf-8")
    assert manifest.read_text(encoding="utf-8") != fc.manifest_text(cycle)


# ── R3-7: PROTOCOL 핀 ↔ 라이브 파일 ↔ scores 해시 3각 대조 ────────────────

def test_validate_fails_when_protocol_pin_diverges_from_live_file(cycle):
    proto = (cycle / "PROTOCOL.md").read_text(encoding="utf-8")
    (cycle / "PROTOCOL.md").write_text(proto.replace(SCHEMA_SHA, "0" * 64),
                                       encoding="utf-8")
    errs = forward_validate.validate(cycle)
    assert any("PROTOCOL 핀 ≠ 라이브" in e for e in errs)


def test_validate_fails_when_record_hash_diverges_from_pin(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["schema_sha256"] = "1" * 64
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("≠ PROTOCOL 핀" in e and "fw001-r01" in e for e in errs)


def test_validate_fails_on_run_assemble_fingerprint_drift(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["run_fingerprint"]["schema_sha256"] = "2" * 64
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("런/조립 드리프트" in e for e in errs)


def test_validate_requires_run_fingerprint(cycle):
    sc = fc.read_json(cycle / "scores.json")
    del sc["records"][0]["run_fingerprint"]
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("run_fingerprint 부재" in e for e in errs)


def test_validate_model_id_pin_semantics(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["model_id"] = "claude-haiku-4-5"
    sc["records"][1]["model_id"] = "claude-sonnet-5-20261101"  # 날짜형 접미사 적법
    sc["records"][2]["model_id"] = "claude-sonnet-5-5"         # 임의 확장 위반 (R1-6)
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("fw001-r01: model_id" in e for e in errs)
    assert not any("fw001-r02: model_id" in e for e in errs)
    assert any("fw001-r03: model_id" in e for e in errs)


def test_validate_fails_without_protocol(cycle):
    (cycle / "PROTOCOL.md").unlink()
    errs = forward_validate.validate(cycle)
    assert any("PROTOCOL.md 부재" in e for e in errs)


def test_assemble_copies_run_time_fingerprint(tmp_path, monkeypatch):
    for var in fc.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    cycle = tmp_path / "cycle_a"
    cycle.mkdir()
    fc.write_json(cycle / "universe.json", make_universe())
    runs = tmp_path / "runs"
    runs.mkdir()
    out = {"case_id": "fw001-r01", "misstatement_probability": 45,
           "checklist": [], "mechanism_hypotheses": [],
           "overall": {"top_signals": []}, "documents_used": [],
           "model": "claude-sonnet-5", "run_timestamp": "t", "run_id": "rid",
           "fingerprint": {"system_prompt_sha256": "f" * 64,
                           "schema_sha256": "e" * 64, "pipeline_commit": "a" * 40,
                           "model_requested": "claude-sonnet-5",
                           "harness_version_actual": "v"}}
    (runs / "fw001-r01.json").write_text(json.dumps(out), encoding="utf-8")
    import sys as _sys
    monkeypatch.setattr(_sys, "argv", ["forward_assemble.py", "--cycle", str(cycle),
                                       "--runs", str(runs)])
    import forward_assemble
    assert forward_assemble.main() == 0
    rec = fc.read_json(cycle / "scores.json")["records"][0]
    assert rec["run_fingerprint"]["schema_sha256"] == "e" * 64
    assert rec["run_fingerprint"]["pipeline_commit"] == "a" * 40


# ── R3-8: 봉인 해시 사슬이 러너 출력까지 연장 ─────────────────────────────

def test_run_output_mutation_detectable_from_sealed_content(tmp_path, monkeypatch):
    """scores.json(SEALED_FILES)의 run_output_sha256 ↔ 러너 출력 실측 해시 —
    봉인 후 출력 변조는 봉인 내용만으로 검출된다."""
    for var in fc.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    cycle = tmp_path / "cycle_b"
    cycle.mkdir()
    fc.write_json(cycle / "universe.json", make_universe())
    runs = tmp_path / "runs"
    runs.mkdir()
    out = {"case_id": "fw001-r01", "misstatement_probability": 45,
           "checklist": [], "mechanism_hypotheses": [],
           "overall": {"top_signals": []}, "documents_used": [],
           "model": "claude-sonnet-5", "run_timestamp": "t", "run_id": "rid",
           "fingerprint": {"schema_sha256": SCHEMA_SHA}}
    run_path = runs / "fw001-r01.json"
    run_path.write_text(json.dumps(out), encoding="utf-8")
    import sys as _sys
    monkeypatch.setattr(_sys, "argv", ["forward_assemble.py", "--cycle", str(cycle),
                                       "--runs", str(runs)])
    import forward_assemble
    assert forward_assemble.main() == 0
    sealed = fc.read_json(cycle / "scores.json")["records"][0]
    assert sealed["run_output_sha256"] == fc.sha256_file(run_path)

    tampered = dict(out, misstatement_probability=99)
    run_path.write_text(json.dumps(tampered), encoding="utf-8")
    assert sealed["run_output_sha256"] != fc.sha256_file(run_path), \
        "출력 변조가 봉인 해시로 검출되지 않음"


def test_validate_requires_run_output_sha256(cycle):
    sc = fc.read_json(cycle / "scores.json")
    del sc["records"][0]["run_output_sha256"]
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("run_output_sha256 부재" in e for e in errs)


# ── R3-9: abort 봉인·창 종료 가드·PROTOCOL 제목 ───────────────────────────

def test_abort_seal_freezes_partial_state_and_is_gate_covered(cycle, monkeypatch, capsys):
    (cycle / "scores.json").unlink()  # 창 내 완료 실패 상태 (검증 통과 불가)
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--abort", "--reason", "window missed"])
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    assert "ABORTED" in record and "window missed" in record

    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_verify_seal.main() == 0
    # R2-8 봉인 불변성 게이트와 동일 판정식 — aborted 사이클도 자동 커버
    assert (cycle / "MANIFEST.sha256").read_text(encoding="utf-8") == \
        fc.manifest_text(cycle)

    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    with pytest.raises(SystemExit):
        forward_prepare.main()  # aborted(봉인) 사이클 재작성 거부


def test_abort_requires_reason(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle), "--abort"])
    with pytest.raises(SystemExit):
        forward_seal.main()
    assert not (cycle / "MANIFEST.sha256").exists()


def test_window_gate_itself_refuses_the_past_window_seal(cycle, monkeypatch, capsys):
    """R14-2(a): 종전의 이름값 테스트는 --runs 없이 main()을 불러서, 창
    게이트를 통째로 `if False:`로 죽여도 다음 가드(runs 디렉토리 부재)가
    대신 SystemExit을 냈다 — 실측 0 red. 여기서는 seal_argv로 유효한 runs
    디렉토리를 만들어 다음 가드가 발화할 수 없게 한 뒤, 창 게이트만이 낼 수
    있는 거부 문구까지 확인한다."""
    argv = seal_argv(cycle)
    monkeypatch.setattr(forward_seal, "EXECUTION_WINDOW_END", "2020-01-01")
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit):
        forward_seal.main()
    assert "실행 창 종료" in capsys.readouterr().out
    assert not (cycle / "MANIFEST.sha256").exists()


def test_seal_window_verdict_does_not_depend_on_the_wall_clock(cycle, monkeypatch):
    """R14-2(b): 판정 기준일은 _today() 이음매 하나만 지난다 — 창 종료
    다음날로 이음매를 밀면 거부, 창 안의 날짜면 통과. 스위트가 도는 날짜와는
    무관하다 (autouse pin_seal_clock)."""
    monkeypatch.setattr(forward_seal, "_today", lambda: datetime.date(2026, 11, 23))
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    with pytest.raises(SystemExit):
        forward_seal.main()
    assert not (cycle / "MANIFEST.sha256").exists()
    monkeypatch.setattr(forward_seal, "_today", lambda: datetime.date(2026, 11, 22))
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    assert "past-window" not in (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")


def test_plain_seal_past_window_requires_explicit_flag(cycle, monkeypatch):
    monkeypatch.setattr(forward_seal, "EXECUTION_WINDOW_END", "2020-01-01")
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    with pytest.raises(SystemExit):
        forward_seal.main()  # 조용한 연장 금지 (INV-22)
    assert not (cycle / "MANIFEST.sha256").exists()
    monkeypatch.setattr(sys, "argv", seal_argv(cycle) + ["--past-window"])
    assert forward_seal.main() == 0
    assert "past-window" in (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")


def test_prepare_protocol_title_uses_cycle_name(tmp_path, monkeypatch):
    for var in fc.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    c = tmp_path / "cycle_042"
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(c)])
    assert forward_prepare.main() == 0
    title = (c / "PROTOCOL.md").read_text(encoding="utf-8").splitlines()[0]
    assert "cycle_042" in title and "cycle_001" not in title


def test_prepare_refuses_overwrite_of_unsealed_protocol_without_force(
        tmp_path, monkeypatch, capsys):
    """R9-7 (cycle-8 사건): 준비된-미봉인 사이클에 재실행 = 거부·무변이;
    --force 명시 시에만 재생성; 신규 사이클은 종전대로 생성."""
    for var in fc.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    c = tmp_path / "cycle_043"
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(c)])
    assert forward_prepare.main() == 0            # 신규 사이클 — 종전대로
    before = (c / "PROTOCOL.md").read_bytes()
    with pytest.raises(SystemExit) as exc:        # 재실행 — 거부, 파일 무접촉
        forward_prepare.main()
    assert exc.value.code == 1
    assert "--force" in capsys.readouterr().out
    assert (c / "PROTOCOL.md").read_bytes() == before
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(c), "--force"])
    assert forward_prepare.main() == 0            # 명시적 재생성은 허용


# ── R4-3: 봉인 후 writer 가드 가족 완결 (source_manifest·enumerate --force) ─

def test_source_manifest_refuses_after_seal(cycle, monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    sealed_bytes = (cycle / "source_manifest.json").read_bytes()
    fetch_dir = tmp_path / "fetch"
    fetch_dir.mkdir()
    (fetch_dir / "fetch_log.jsonl").write_text("", encoding="utf-8")
    import forward_source_manifest
    monkeypatch.setattr(sys, "argv", ["x", "--fetch-dir", str(fetch_dir),
                                      "--cycle", str(cycle)])
    assert forward_source_manifest.main() == 1
    assert (cycle / "source_manifest.json").read_bytes() == sealed_bytes


def test_enumerate_force_refuses_on_sealed_cycle(cycle, monkeypatch, capsys):
    """R5-2 재작성: 종전 판형은 빈 스냅샷이라 R4-7(a) 불완전 가드가 먼저
    발화 — 봉인 가드를 지워도 통과하는 공진 테스트였다. 완전 재계산(12사
    스냅샷)으로 제어 흐름이 봉인 가드에 도달하게 하고, 거부 사유가
    MANIFEST.sha256(봉인)임을 출력으로 단언한다. (수정 검증: R4-3 가드
    hunk를 로컬 revert하면 이 테스트가 red — 실측 후 원복.)"""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    sealed_bytes = (cycle / "universe.json").read_bytes()
    import urllib.request
    import forward_enumerate as fe
    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    monkeypatch.setattr(fe, "_provenance", [])
    monkeypatch.setattr(fe, "_fetch_errors", [])
    monkeypatch.setattr(fe, "SIC_SET", ["3674"])
    monkeypatch.setattr(fe, "cycle1_ciks", lambda: set())
    snap = cycle / "snap_full"
    snap.mkdir()
    monkeypatch.setattr(fe, "SNAP", snap)
    ciks = [f"{9000 + i:010d}" for i in range(1, 13)]
    (snap / "sic_3674_p0.xml").write_text(
        "".join(f"<cik>{c}</cik>" for c in ciks), encoding="utf-8")
    for c in ciks:
        _write_submissions(snap, c, ["2025-01-01", "2024-09-01"],
                           ["2025-01-02", "2025-04-02", "2025-07-02", "2025-10-02",
                            "2026-01-02", "2026-04-02"])
        fc.write_json(snap / f"float_CIK{c}.json",
                      {"units": {"USD": [{"end": "2026-06-30", "val": 2.0e9}]}})
    monkeypatch.setattr(sys, "argv", ["x", "--offline", "--force",
                                      "--out", str(cycle / "universe.json")])
    # R12-3: 이 호출의 출력만 본다 — 종전에는 앞서 실행한 forward_seal의
    # stdout(`git add runs/MANIFEST.sha256 …`)이 같은 capsys 버퍼에 남아
    # enumerate 메시지에서 MANIFEST.sha256을 없애도 통과했다. 자기 docstring이
    # R5-2에서 고쳤다고 밝힌 공진 결함이 같은 자리에서 재발한 상태였다.
    capsys.readouterr()
    assert fe.main() == 1
    out = capsys.readouterr().out
    assert "MANIFEST.sha256" in out and "재작성 금지" in out, out[-400:]
    assert (cycle / "universe.json").read_bytes() == sealed_bytes


# ── R4-4: 봉인 사슬 엄격화 — leg별 fail-closed + 실측 재해시 ──────────────

def test_empty_run_fingerprint_fails(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["run_fingerprint"] = {}
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("run_fingerprint.schema_sha256" in e for e in errs)
    assert any("model_requested 부재" in e for e in errs)


def test_wrong_model_requested_in_fingerprint_fails(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["run_fingerprint"]["model_requested"] = "claude-haiku-4-5"
    sc["records"][1]["run_fingerprint"]["model_requested"] = "claude-sonnet-5-20261101"
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("fw001-r01" in e and "model_requested" in e for e in errs)
    assert not any("fw001-r02" in e and "model_requested" in e for e in errs)


def test_garbage_run_output_sha256_fails(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["run_output_sha256"] = "yes"
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("run_output_sha256 부재/비정형" in e for e in errs)


def test_runs_rehash_detects_post_assemble_edit(cycle, tmp_path):
    runs = tmp_path / "runs_check"
    runs.mkdir()
    sc = fc.read_json(cycle / "scores.json")
    for r in sc["records"]:
        out_path = runs / f"{r['record_id']}.json"
        out_path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle, runs_dir=runs) == []

    victim = runs / "fw001-r01.json"
    victim.write_text(json.dumps({**make_run_output("fw001-r01"), "edited": True}),
                      encoding="utf-8")
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("실측 해시 ≠" in e for e in errs)

    missing = runs / "fw001-r02.json"
    missing.unlink()
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("runs 출력 부재" in e and "fw001-r02" in e for e in errs)


def test_runs_leg_rederives_records_from_runner_output(cycle, tmp_path):
    """R11-4: 해시 사슬은 '그 파일이 안 바뀌었다'만 증명한다 — 점수·판정을
    서로 정합하게 함께 고친 레코드는 종전 leg 전부를 통과했다 (35/insufficient/
    abstain → 75/sufficient/flag). 봉인은 '동결 프로토콜의 산출'을 주장하므로
    러너 출력에서 실제로 재파생해 대조한다."""
    runs = tmp_path / "runs_rederive"
    runs.mkdir()
    sc = fc.read_json(cycle / "scores.json")
    for r in sc["records"]:
        out_path = runs / f"{r['record_id']}.json"
        out_path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle, runs_dir=runs) == []

    # 자기 정합적 편집: expected_state(75, "sufficient") == "flag" 이므로
    # 서수 컷 대조는 침묵 통과하고, 러너 출력 파일은 손대지 않아 해시도 정합.
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0].update(misstatement_risk_score=75,
                            evidence_sufficiency="sufficient",
                            decision_state="flag")
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("재파생과 불일치" in e and "fw001-r01" in e for e in errs), errs
    # 해시 leg·서수 컷 leg는 여전히 침묵 — 재파생 leg만이 이걸 잡는다
    assert not any("실측 해시 ≠" in e or "서수 컷 기대" in e for e in errs), errs


def test_not_scored_with_existing_runner_output_is_caught(cycle, tmp_path):
    """R11-7: 레이트 리밋으로 11/12 조립 → 소유자가 러너 재개 → 12번째 완료.
    봉인은 validate만 재실행하고 assemble은 다시 돌리지 않으므로, 완료된
    레코드가 not_scored로 봉인되고 그 출력은 봉인 커밋에 함께 실린다."""
    runs = tmp_path / "runs_resume"
    runs.mkdir()
    sc = fc.read_json(cycle / "scores.json")
    for r in sc["records"]:
        out_path = runs / f"{r['record_id']}.json"
        out_path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    victim = sc["records"][-1]
    rid = victim["record_id"]
    sc["records"][-1] = {"record_id": rid, "company": victim["company"],
                         "status": "not_scored"}
    fc.write_json(cycle / "scores.json", sc)

    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("not_scored인데 러너 출력" in e and rid in e for e in errs), errs

    # 출력이 실제로 없으면(진짜 미채점) 통과 — 11/12는 MIN_SCORED 충족
    (runs / f"{rid}.json").unlink()
    assert forward_validate.validate(cycle, runs_dir=runs) == []


def test_naive_in_window_scored_at_is_accepted(cycle):
    """R12-5: R11-4의 픽스처 재작성이 scored_at을 naive에서 tz-aware로 옮기며
    R10-8의 naive 분기 커버리지를 통째로 없앴다 — 같은 변이가 부모에서는
    23건을 죽였는데 그 뒤로는 0건이었다. naive 창내 값 한 건이면 복원된다
    (러너는 UTC …Z를 쓰므로 naive는 손편집·외래 레코드에서만 온다)."""
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["scored_at"] = "2026-11-16"       # 창 내, tz 없음
    fc.write_json(cycle / "scores.json", sc)
    assert not any("실행 창 밖" in e for e in forward_validate.validate(cycle))

    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["scored_at"] = "2026-11-30"       # 창 밖, tz 없음
    fc.write_json(cycle / "scores.json", sc)
    assert any("실행 창 밖" in e for e in forward_validate.validate(cycle))


def test_rederivation_catches_extra_key_in_sealed_record(cycle, tmp_path):
    """R12-5: 재파생 대조가 `expect.items()`만 돌아 레코드에만 있는 키는
    보이지 않았다 — 봉인 레코드에 없는 필드를 덧붙여도 통과했다."""
    runs = tmp_path / "runs_extra"
    runs.mkdir()
    sc = fc.read_json(cycle / "scores.json")
    for r in sc["records"]:
        out_path = runs / f"{r['record_id']}.json"
        out_path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle, runs_dir=runs) == []

    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["published_score"] = 99
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("published_score" in e for e in errs), errs


def test_rederivation_catches_status_key_on_a_scored_record(cycle, tmp_path):
    """R13-6: status 예외가 반례를 남겼다 — 채점된 봉인 레코드에 status를
    덧붙여도 오류 0이었다(R12-5-A 실측). 이 대조에 도달하는 레코드는 채점된
    것뿐이고(not_scored는 앞서 continue), assemble_record는 not_scored일 때만
    status를 만든다. 변이: `- {"status"}` 복원 시 red."""
    runs = tmp_path / "runs_status"
    runs.mkdir()
    sc = fc.read_json(cycle / "scores.json")
    for r in sc["records"]:
        out_path = runs / f"{r['record_id']}.json"
        out_path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle, runs_dir=runs) == []

    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["status"] = "sealed_by_hand"
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("status" in e and "재파생" in e for e in errs), errs


def test_runs_dir_absent_skips_with_notice(cycle, capsys):
    errs = forward_validate.validate(cycle, runs_dir=cycle / "no_such_runs")
    assert errs == []
    assert "실측 재해시 생략" in capsys.readouterr().out


# ── R7-3: fp-sibling 존재 시 조립·검증 fail-closed ────────────────────────

def test_fp_sibling_fails_assemble_and_validate(cycle, tmp_path, monkeypatch, capsys):
    """창 중간 커밋 후 재실행은 {rid}.fp-*.json을 남긴다 — 정본이 stale일 수
    있으므로 assemble·validate 모두 sibling을 이름으로 지목하며 거부한다."""
    for var in fc.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    runs = tmp_path / "runs_sib"
    runs.mkdir()
    sc = fc.read_json(cycle / "scores.json")
    for r in sc["records"]:
        out_path = runs / f"{r['record_id']}.json"
        out_path.write_text(json.dumps(make_run_output(r["record_id"])),
                            encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle, runs_dir=runs) == []  # sibling 없음 = 무변화

    sib = runs / "fw001-r01.fp-9a3b.json"
    sib.write_text(json.dumps({"case_id": "fw001-r01", "newer": True}), encoding="utf-8")
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("fp-sibling" in e and sib.name in e for e in errs)

    import forward_assemble
    monkeypatch.setattr(sys, "argv", ["forward_assemble.py", "--cycle",
                                      str(cycle), "--runs", str(runs)])
    assert forward_assemble.main() == 1
    assert sib.name in capsys.readouterr().out


# ── R4-7: 소도구 경화 4종 ─────────────────────────────────────────────────

def test_enumerate_incomplete_writes_nothing_even_without_target(tmp_path, monkeypatch):
    """R4-7(a): 불완전 재계산은 대상 부재여도 무기록 — 부분 universe가
    다음 실행을 자기 산출물로 막지 않는다."""
    import urllib.request
    import forward_enumerate
    for var in fc.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    monkeypatch.setattr(forward_enumerate, "_provenance", [])
    monkeypatch.setattr(forward_enumerate, "_fetch_errors", [])
    snap = tmp_path / "snap_empty"
    snap.mkdir()
    monkeypatch.setattr(forward_enumerate, "SNAP", snap)
    target = tmp_path / "fresh" / "universe.json"
    monkeypatch.setattr(sys, "argv", ["x", "--offline", "--out", str(target)])
    assert forward_enumerate.main() == 1
    assert not target.exists(), "불완전 재계산이 부분 universe를 기록함"


def test_cited_source_attestation_requires_accession_shape(cycle):
    """R4-7(b): 'sec'/'20' 류 비정형 인용이 부분 문자열로 인증되면 안 된다."""
    assert not forward_validate._cited_source_attested(
        "sec", [{"url": "https://data.sec.gov/x", "accession_no": "a"}])
    assert not forward_validate._cited_source_attested(
        "20", [{"url": "https://x/2026", "accession_no": None}])
    assert forward_validate._cited_source_attested(
        "0000000000-26-000001", [{"accession_no": "0000000000-26-000001"}])
    assert forward_validate._cited_source_attested(
        "0000000000-26-000001",
        [{"url": "https://www.sec.gov/Archives/000000000026000001/x-index.htm"}])
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["cited_sources"] = ["sec"]
    fc.write_json(cycle / "scores.json", sc)
    assert any("source_manifest 미등재" in e for e in forward_validate.validate(cycle))


def test_outcome_append_rejects_datetime_suffixed_date(cycle, monkeypatch):
    """R4-7(c): parse_date 10자 절단 우회('2027-03-02T00:00') 차단."""
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--record-id", "fw001-r01",
                                      "--event-date", "2027-03-02T00:00",
                                      "--event-public-date", "2027-03-02",
                                      "--event-type", "sec_complaint", "--source", "s",
                                      "--new-label", "sec_complaint",
                                      "--reviewer", "o", "--rationale", "r"])
    with pytest.raises(SystemExit):
        forward_outcome_append.main()
    assert (cycle / "outcome_updates.jsonl").read_text(encoding="utf-8") == ""


def test_portable_path_anchors(tmp_path):
    import fetch_xbrl_facts as fxf
    repo, home = tmp_path / "repo", tmp_path / "home"
    (repo / "runs").mkdir(parents=True)
    (home / "data").mkdir(parents=True)
    assert fxf.portable_path(repo / "runs/x.json", repo=repo, home=home) == "runs/x.json"
    assert fxf.portable_path(home / "data/y.json", repo=repo, home=home) == "~/data/y.json"
    other = tmp_path / "elsewhere.json"
    assert fxf.portable_path(other, repo=repo, home=home) == str(other.resolve())


# ── R5-1: 봉인 시점 재해시 leg 실행 ───────────────────────────────────────

def test_seal_fails_on_tampered_runner_output(cycle, monkeypatch):
    argv = seal_argv(cycle)
    runs = Path(argv[argv.index("--runs") + 1])
    (runs / "fw001-r01.json").write_text(
        json.dumps({"case_id": "fw001-r01", "edited": True}), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit):
        forward_seal.main()
    assert not (cycle / "MANIFEST.sha256").exists(), "변조 출력이 봉인됨"


def test_plain_seal_requires_runs_dir(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--runs", str(cycle / "no_runs")])
    with pytest.raises(SystemExit):
        forward_seal.main()
    assert not (cycle / "MANIFEST.sha256").exists()


def test_abort_seal_record_carries_rehash_skip_line(cycle, monkeypatch):
    (cycle / "scores.json").unlink()
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--abort", "--reason", "window missed"])
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    assert "run_output re-hash: SKIPPED" in record


def test_normal_seal_record_states_rehash_performed(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    assert "run_output re-hash: verified" in record


# ── R5-3: 라이브 수집 사이트의 EDGAR 병렬 배열 정렬성 (R1-13 클래스) ──────

def test_check_candidate_hard_errors_on_truncated_filing_dates(tmp_path, monkeypatch):
    """filingDate가 form보다 짧으면 4.02 오염 스크린 대상 꼬리 제출이
    침묵 탈락 — 후보가 조용히 admit되기 전에 하드 오류."""
    import forward_enumerate as fe
    snap = tmp_path / "snap"
    snap.mkdir()
    monkeypatch.setattr(fe, "SNAP", snap)
    cik = "0000009001"
    fc.write_json(snap / f"submissions_CIK{cik}.json", {
        "sic": "3674", "name": "Co", "tickers": ["T"],
        "filings": {"recent": {
            "form": ["10-K", "8-K"], "filingDate": ["2025-01-01"],
            "items": ["", "4.02"], "isXBRL": [1, 1]}}})
    with pytest.raises(ValueError, match="병렬 배열 길이 불일치"):
        fe.check_candidate(cik, offline=True)


def test_control_screening_filing_counts_hard_errors_on_mismatch(tmp_path, monkeypatch):
    import datetime as _dt
    import control_screening as cs

    class _Resp:
        def __init__(self, obj):
            self._obj = obj

        def json(self):
            return self._obj

    doc = {"filings": {"recent": {"form": ["10-K", "10-Q"],
                                  "filingDate": ["2025-01-01"],
                                  "isXBRL": [1, 1]},
                       "files": []}}
    monkeypatch.setattr(cs, "fetch", lambda url: _Resp(doc))
    with pytest.raises(ValueError, match="병렬 배열 길이 불일치"):
        cs.filing_counts("0000009001", _dt.date(2026, 1, 1), tmp_path / "d")


# ── R2-28: cli_client ↔ forward_common 종량 가족 정합 (복제 교차 대조) ────

def test_cli_client_covers_forward_metered_family():
    """INV-08 방향상 pipeline은 tools/를 import하지 않으므로 목록을 복제한다 —
    이 교차 대조가 두 목록의 드리프트를 잠근다 (cli_client는 재라우팅 변수를
    더한 상위집합이어야 한다)."""
    sys.path.insert(0, str(REPO_ROOT / "pipeline"))
    import cli_client
    assert set(fc.METERED_CREDENTIAL_VARS) <= set(cli_client.METERED_CREDENTIAL_VARS)
    assert {"ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL",
            "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX"} <= \
        set(cli_client.METERED_CREDENTIAL_VARS)
    # R6-4: 세 번째 튜플(codex arm)도 가족에 잠근다 — cli_client 상위집합 +
    # codex 재라우팅 변수
    import crossmodel_gpt
    assert set(cli_client.METERED_CREDENTIAL_VARS) <= set(crossmodel_gpt.METERED_ENV_VARS)
    assert {"OPENAI_BASE_URL", "OPENAI_API_BASE"} <= set(crossmodel_gpt.METERED_ENV_VARS)


# ── R6-7: SEAL_RECORD 이식성 + 검증 완결성 ────────────────────────────────

def test_seal_record_has_no_absolute_paths_and_names_rehash_command(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    # R7-8: 전체 레코드 단정 — 소유자 명령 절(git add {cycle_display})이 R6-7
    # 수정 지점인데 종전 splice가 그 절만 검사에서 도려냈다 (revert 미검출).
    assert "/Users/" not in record and str(cycle.parent) not in record, \
        "SEAL_RECORD에 절대 로컬 경로가 남음"
    assert "forward_validate.py --cycle" in record and "--runs" in record, \
        "run-output 사슬 검증 명령 부재"


def test_seal_owner_commands_stage_runs_dir_and_call_logs(cycle, monkeypatch):
    """R7-16: 봉인 커밋 명령이 runs 출력과 logs/run_* 호출 로그를 staging —
    빠지면 클론 검증자의 run-output re-hash leg가 skip으로 격하된다."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    add_line = next(line for line in record.splitlines()
                    if line.startswith("git add "))
    assert " runs_t" in add_line, add_line   # 픽스처 runs 디렉토리 표기
    assert " logs/run_*" in add_line, add_line


def test_seal_owner_commands_write_and_stage_blindness_manifest(cycle, monkeypatch):
    """R10-3: 봉인 커밋이 runs/forward 출력을 담는 이상, 블라인드 매니페스트
    재생성 + staging이 소유자 명령에 없으면 push된 봉인 커밋이 verify_blindness
    (d) leg에서 정본 CI를 붉힌다.

    R11-9: 그 블록은 `&&` 연쇄여야 한다 — verify_blindness는 스캔 실패(exit 1)
    에도 매니페스트를 쓰고 반환하므로, 줄바꿈 나열이면 붙여넣기 한 번에
    커밋·태그·push까지 흘러간다. push 직전 읽기 전용 재검증 + runs/ 청결
    확인(기록만 되고 staging 안 된 리허설 잔여물)도 같은 사슬 안에 있어야 한다."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    block = record.split("```bash")[1].split("```")[0]
    assert "verify_blindness.py --write-manifest" in block
    add_line = next(line for line in block.splitlines()
                    if line.startswith("git add "))
    assert "runs/MANIFEST.sha256" in add_line, add_line

    # push까지 이어지는 모든 단계가 && 로 묶여 있는가
    steps = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
    push_at = next(i for i, ln in enumerate(steps) if ln.startswith("git push"))
    for line in steps[:push_at]:
        assert line.endswith("&& \\"), f"연쇄 끊김 — 실패가 흘러간다: {line}"
    # push 직전 읽기 전용 재검증 + runs/ 청결 확인
    assert any(ln.startswith("python tools/verify_blindness.py &&")
               for ln in steps[:push_at]), block
    assert any("git status --porcelain" in ln and "runs/" in ln
               for ln in steps[:push_at]), block

    # R15-3: 사이클 디렉토리도 push 전에 재검증된다 — 매니페스트가 불변인
    # 쪽이 그쪽인데 사슬은 runs/만 두 번 보고 있었다.
    assert any(ln.startswith("python tools/forward_verify_seal.py --cycle")
               for ln in steps[:push_at]), block
    assert any("git status --porcelain" in ln and cycle.name in ln
               for ln in steps[:push_at]), block


def test_late_evidence_file_is_caught_by_the_chains_own_verifier(
        cycle, monkeypatch, capsys):
    """R15-3 행동 leg: 봉인 후 evidence/에 떨어진 파일 하나가 무엇을 하는가.

    `git add {cycle}`는 디렉토리 전체를 담고 sealed_paths는 SEALED_FILES +
    evidence/ 전건을 해싱하므로, 매니페스트가 쓰인 **뒤** 생긴 파일은 커밋·
    태그·push까지 실려 가고 그 순간부터 모든 클론에서 manifest_text가 그
    줄만큼 길어진다 (forward_common.py의 자체 주석이 서술하는 실패 모드).
    교정 경로는 없다 — INV-06/INV-22가 매니페스트 재작성을, forward_seal이
    재봉인을 금지한다.

    사슬에 넣은 그 명령이 정확히 이것을 잡는다: 아래 exit 1이 push 직전에
    나오면 push가 일어나지 않는다. 부모 커밋에서는 사슬에 이 단계가 없어
    같은 시퀀스가 push까지 도달했다 (test_seal_owner_commands_…의 새 단언이
    그 부재를 고정한다)."""
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    stamp_ots(cycle)
    assert forward_verify_seal.main() == 0        # 봉인 직후 상태는 정합

    (cycle / "evidence").mkdir(exist_ok=True)
    (cycle / "evidence" / "late.txt").write_text("fetch receipt", encoding="utf-8")
    assert forward_verify_seal.main() == 1
    assert "봉인 후 추가됨: evidence/late.txt" in capsys.readouterr().out


def test_abort_seal_record_also_portable(cycle, monkeypatch):
    (cycle / "scores.json").unlink()
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--abort", "--reason", "window missed"])
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    verify_section = record.split("## 외부 검증 방법")[1]
    assert "/Users/" not in verify_section and str(cycle.parent) not in verify_section
