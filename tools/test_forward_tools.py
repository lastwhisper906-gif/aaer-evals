"""forward 봉인 도구의 오프라인 테스트 (spec §11, D100). 네트워크 0·호출 0."""
import hashlib
import json
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
PROTOCOL_FIXTURE = ("# PROTOCOL fixture\n"
                    "- evaluatee_model (pin): `claude-sonnet-5`\n"
                    f"- `pipeline/runner.py` sha256 `{PROMPT_SHA}`\n"
                    f"- `schemas/llm_output.json` sha256 `{SCHEMA_SHA}`\n")


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


def test_sha_leg_is_the_only_reason_for_refusal(tmp_path, monkeypatch):
    """R12-1(c) leg 격리: 경로가 권위 있는 로그에 실재하므로 출처 leg는
    통과한다 — 거부 사유는 오직 디스크 바이트 ≠ 매니페스트 기록이다.
    변이 `if rel in own and recorded and _sha256_bytes_of(disk) == recorded:`
    → `if rel in own:` 는 이 테스트를 red로 만들어야 한다."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    mine = data_dir / "TK01/xbrl/CIK0000001001.json"
    mine.parent.mkdir(parents=True)
    mine.write_bytes(b'{"mine": 1}')
    _authoritative_log(fxf, vm, data_dir, manifest_path,
                       [_log_row_for(data_dir, "TK01/xbrl/CIK0000001001.json")])
    # 출처 leg는 통과(로그에 있음), sha leg만 실패하도록 디스크만 드리프트
    mine.write_bytes(b'{"mine": 2}')
    assert "TK01/xbrl/CIK0000001001.json" in fxf._own_writes(
        data_dir, {f["path"]: f.get("sha256")
                   for f in json.loads(manifest_path.read_text())["files"]}), \
        "출처 leg가 통과해야 sha leg를 격리 측정할 수 있다"

    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    with pytest.raises(SystemExit, match="매니페스트 핀 경로와 충돌"):
        fxf.fetch_forward(upath, data_dir)


def test_own_writes_skips_valid_json_non_object_row(tmp_path, monkeypatch):
    """R12-1(d): 독스트링이 약속한 침묵 스킵 — 유효 JSON 비객체 행에서
    AttributeError로 죽지 않는다."""
    fxf, vm, data_dir, manifest_path = _fetch_fixture(tmp_path, monkeypatch)
    good = data_dir / "TK01/xbrl/CIK0000001001.json"
    good.parent.mkdir(parents=True)
    good.write_bytes(b"{}")
    (data_dir / "fetch_log.jsonl").write_text(
        "123\n[1, 2]\n\"str\"\nnot json\n"
        + json.dumps(_log_row_for(data_dir, "TK01/xbrl/CIK0000001001.json")) + "\n",
        encoding="utf-8")
    manifest_path.write_text(json.dumps(vm.build_manifest()), encoding="utf-8")
    pinned = {f["path"]: f.get("sha256")
              for f in json.loads(manifest_path.read_text())["files"]}
    assert fxf._own_writes(data_dir, pinned) == {"TK01/xbrl/CIK0000001001.json"}


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
    assert (data_dir / "fetch_log.jsonl").is_file()


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
    assert any(f["path"].startswith("TK01/") for f in m["files"])

    # 재수집(재시도·절단 청크 재당김·창 후반 최신화)이 여전히 가능해야 한다
    assert fxf.fetch_forward(upath, data_dir) == 0


def test_owner_may_override_pinned_collision_and_it_is_logged(tmp_path, monkeypatch):
    """R11-2: 온전한 핀 스냅샷 덮어쓰기는 소유자 명시 --allow-pinned 로만,
    그리고 그 사실이 fetch_log.jsonl에 남는다."""
    fxf, data_dir = _manifest_fixture(tmp_path, monkeypatch,
                                      "TK01/xbrl/CIK0000001001.json",
                                      on_disk=b'{"july": "snapshot"}')
    monkeypatch.setattr(fxf, "fetch",
                        lambda url: _FetchResp({"filings": {"files": []}}))
    upath = tmp_path / "universe.json"
    fc.write_json(upath, make_universe(1))
    assert fxf.fetch_forward(upath, data_dir, {"TK01"}) == 0
    rows = [json.loads(x) for x in
            (data_dir / "fetch_log.jsonl").read_text(encoding="utf-8").splitlines()]
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


def test_abort_seal_record_also_portable(cycle, monkeypatch):
    (cycle / "scores.json").unlink()
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--abort", "--reason", "window missed"])
    assert forward_seal.main() == 0
    record = (cycle / "SEAL_RECORD.md").read_text(encoding="utf-8")
    verify_section = record.split("## 외부 검증 방법")[1]
    assert "/Users/" not in verify_section and str(cycle.parent) not in verify_section
