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
            "model_id": "claude-sonnet-5", "prompt_sha256": "x", "schema_sha256": "y",
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
    (c / "PROTOCOL.md").write_text("proto", encoding="utf-8")
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

def run_seal(cycle, capsys=None):
    sys.argv = ["forward_seal.py", "--cycle", str(cycle)]
    return forward_seal.main()


def test_seal_verify_roundtrip_and_tamper(cycle, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
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
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_seal.main() == 0
    with pytest.raises(SystemExit):
        forward_seal.main()  # MANIFEST 존재 → 거부 (spec §3-5)


def test_seal_refused_on_invalid_cycle(cycle, monkeypatch):
    (cycle / "source_manifest.json").unlink()
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
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
           "documents_used": [{"accession_no": "0000000000-26-000001"}]}
    r = fa.assemble_record(meta, out)
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
                                      "--record-id", "fw001-r99", "--event-date", "d",
                                      "--event-public-date", "d", "--event-type",
                                      "sec_complaint", "--source", "s", "--new-label",
                                      "sec_complaint", "--reviewer", "o", "--rationale", "r"])
    with pytest.raises(SystemExit):
        forward_outcome_append.main()
