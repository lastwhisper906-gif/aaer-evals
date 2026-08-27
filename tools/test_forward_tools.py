"""forward 봉인 도구의 오프라인 테스트 (spec §11, D100). 네트워크 0·호출 0."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
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


def make_record(rid, score=45, suff="sufficient", cik=None):
    state = "abstain" if suff == "insufficient" else (
        "flag" if score >= 70 else "review" if score >= 40 else "no_flag")
    if cik is None:  # make_universe와 정합: fw001-rNN ↔ cik 1000+NN
        cik = f"{1000 + int(rid.rsplit('r', 1)[1]):010d}"
    return {"record_id": rid, "company": {"name": "Test", "ticker": "T", "cik": cik},
            "misstatement_risk_score": score, "decision_state": state,
            "evidence_sufficiency": suff, "assessment_confidence": "medium",
            "top_signals": ["s"], "benign_alternative_explanations": ["b"],
            "affected_account_areas": ["rev"], "cited_sources": ["0000000000-26-000001"],
            "model_id": "claude-sonnet-5", "prompt_sha256": PROMPT_SHA,
            "schema_sha256": SCHEMA_SHA,
            "run_fingerprint": {"system_prompt_sha256": "f" * 64,
                                "schema_sha256": SCHEMA_SHA,
                                "pipeline_commit": "a" * 40,
                                "model_requested": "claude-sonnet-5"},
            "run_output_sha256": "b" * 64,
            "scored_at": "2026-11-15"}


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
    assert forward_prepare.check_universe(make_universe()) == []


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

def test_validate_full_record_contract_fields(cycle):
    for field in ("schema_sha256", "scored_at"):
        sc = fc.read_json(cycle / "scores.json")
        del sc["records"][0][field]
        fc.write_json(cycle / "scores.json", sc)
        assert any(field in e for e in forward_validate.validate(cycle)), field
    for field in ("benign_alternative_explanations", "affected_account_areas"):
        sc = fc.read_json(cycle / "scores.json")
        del sc["records"][0][field]
        fc.write_json(cycle / "scores.json", sc)
        assert any(field in e for e in forward_validate.validate(cycle)), field


def test_validate_empty_arrays_are_legal(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["benign_alternative_explanations"] = []
    sc["records"][0]["affected_account_areas"] = []
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

def test_prepare_refuses_after_seal(tmp_path, monkeypatch):
    import forward_prepare as fp
    c = tmp_path / "cycle_sealed"
    c.mkdir()
    proto_before = "sealed proto"
    (c / "PROTOCOL.md").write_text(proto_before, encoding="utf-8")
    (c / "MANIFEST.sha256").write_text("x  PROTOCOL.md\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(c)])
    with pytest.raises(SystemExit):
        fp.main()
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
            path = runs / f"{r['record_id']}.json"
            path.write_text(json.dumps({"case_id": r["record_id"]}), encoding="utf-8")
            r["run_output_sha256"] = fc.sha256_file(path)
        fc.write_json(cycle / "scores.json", sc)
    return ["x", "--cycle", str(cycle), "--runs", str(runs)]


def run_seal(cycle, capsys=None):
    sys.argv = ["forward_seal.py", "--cycle", str(cycle)]
    return forward_seal.main()


def test_seal_verify_roundtrip_and_tamper(cycle, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    assert (cycle / "MANIFEST.sha256").exists() and (cycle / "SEAL_RECORD.md").exists()

    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_verify_seal.main() == 0

    # 변조 검출
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["misstatement_risk_score"] = 44
    fc.write_json(cycle / "scores.json", sc)
    assert forward_verify_seal.main() == 1
    out = capsys.readouterr().out
    assert "변조됨: scores.json" in out


def test_reseal_refused(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    with pytest.raises(SystemExit):
        forward_seal.main()  # MANIFEST 존재 → 거부 (spec §3-5)


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
           "run_id": "x", "run_timestamp": "2026-11-15T00:00:00Z",
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


def test_enumerate_force_refuses_on_sealed_cycle(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", seal_argv(cycle))
    assert forward_seal.main() == 0
    sealed_bytes = (cycle / "universe.json").read_bytes()
    import urllib.request
    import forward_enumerate
    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    monkeypatch.setattr(forward_enumerate, "_provenance", [])
    monkeypatch.setattr(forward_enumerate, "_fetch_errors", [])
    monkeypatch.setattr(forward_enumerate, "SNAP", cycle / "snap_empty")
    (cycle / "snap_empty").mkdir()
    monkeypatch.setattr(sys, "argv", ["x", "--offline", "--force",
                                      "--out", str(cycle / "universe.json")])
    assert forward_enumerate.main() == 1
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
        out_path.write_text(json.dumps({"case_id": r["record_id"]}), encoding="utf-8")
        r["run_output_sha256"] = fc.sha256_file(out_path)
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle, runs_dir=runs) == []

    victim = runs / "fw001-r01.json"
    victim.write_text(json.dumps({"case_id": "fw001-r01", "edited": True}),
                      encoding="utf-8")
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("실측 해시 ≠" in e for e in errs)

    missing = runs / "fw001-r02.json"
    missing.unlink()
    errs = forward_validate.validate(cycle, runs_dir=runs)
    assert any("runs 출력 부재" in e and "fw001-r02" in e for e in errs)


def test_runs_dir_absent_skips_with_notice(cycle, capsys):
    errs = forward_validate.validate(cycle, runs_dir=cycle / "no_such_runs")
    assert errs == []
    assert "실측 재해시 생략" in capsys.readouterr().out


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
