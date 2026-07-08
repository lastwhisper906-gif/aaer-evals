"""runner._full_output_error — 조립 출력의 llm_output.json 계약 강제 (캐시/API 불요, CI 상주).

A1 회귀: MODEL_SCHEMA(호출시)는 약해서 계약 위반 출력이 OK로 기록되고 멱등이 깨졌다.
이 테스트는 fail-closed 검증이 위반을 실제로 잡는지 확인한다."""
import runner


def _valid_full(p=65, mechs=1):
    ev = [{"quote": "Revenues=1200 (FY2019)", "source_accession_no": "x", "location": "Revenues|FY2019"}]
    return {
        "case_id": "case_01", "run_id": "perturbed-case_01-r1", "model": "claude-sonnet-5",
        "pipeline_version": "abc123", "run_timestamp": "2020-01-01T00:00:00+00:00",
        "documents_used": [{"accession_no": "0001", "form_type": "10-K", "filing_date": "2019-02-01"}],
        "checklist": [{"item_id": "CL1", "question": "q", "finding": "flag",
                       "confidence": "high", "evidence": ev}],
        "misstatement_probability": p,
        "mechanism_hypotheses": [{"affected_line_items": ["Revenues"], "direction": "overstated",
                                  "accounting_treatment": "t", "rationale_evidence": ev}
                                 for _ in range(mechs)],
        "overall": {"risk_tier": "elevated" if p >= 70 else "watch", "top_signals": ["CL1"]},
    }


def test_valid_full_passes():
    assert runner._full_output_error(_valid_full()) is None


def test_p_ge40_without_mechanism_fails():
    # p>=40 인데 mechanism_hypotheses 비면 계약 위반 (약한 MODEL_SCHEMA가 놓치던 케이스)
    bad = _valid_full(p=45, mechs=0)
    assert runner._full_output_error(bad) is not None


def test_out_of_range_probability_fails():
    assert runner._full_output_error(_valid_full(p=500)) is not None


def test_empty_documents_used_fails():
    bad = _valid_full()
    bad["documents_used"] = []
    assert runner._full_output_error(bad) is not None


def test_empty_evidence_fails():
    bad = _valid_full()
    bad["checklist"][0]["evidence"] = []
    assert runner._full_output_error(bad) is not None


def test_p_below_40_allows_empty_mechanism():
    # p<40 이면 mechanism 비어도 계약상 허용 (조건부가 과잉 차단하지 않음)
    assert runner._full_output_error(_valid_full(p=20, mechs=0)) is None
