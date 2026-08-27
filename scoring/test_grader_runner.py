"""채점자 러너 (개정 #2 경로) — 폴백·멱등·중립 ID 규율 테스트 (subprocess 모킹)."""
import json
import os
import stat
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "scoring"))

import cli_client  # noqa: E402
import grader_runner as gr  # noqa: E402

STUB = r'''#!/usr/bin/env python3
import json, os, sys
if sys.argv[1:] == ["--version"]:
    # 하네스 핀 강제 경로 (C3, D109) — call_ 기록 없이 버전만 응답
    sys.stdout.write(os.environ.get("STUB_VERSION", "STUB-VERSION-UNSET"))
    sys.exit(0)
stub_dir = os.environ["STUB_DIR"]
payload = sys.stdin.read()
n = len([f for f in os.listdir(stub_dir) if f.startswith("call_")])
with open(os.path.join(stub_dir, f"call_{n:02d}.json"), "w") as f:
    json.dump({"argv": sys.argv[1:], "stdin": payload}, f)
responses = json.load(open(os.path.join(stub_dir, "responses.json")))
r = responses[min(n, len(responses) - 1)]
sys.stdout.write(r if isinstance(r, str) else json.dumps(r))
'''

GRADE = {"dim1_probability_band": 2, "dim2_mechanism": None,
         "dim3_genre_mapping": {"mapped_genre": None, "score": None},
         "dim4_evidence_quality": 2, "memorization_suspect_condition2": False,
         "rationale": "test"}


def resp(structured=None, model="claude-fable-5", is_error=False, result="x"):
    body = {"type": "result", "is_error": is_error, "result": result,
            "session_id": "sess-g", "total_cost_usd": 0.0,
            "usage": {"input_tokens": 1, "output_tokens": 1},
            "modelUsage": {model: {"outputTokens": 1}}}
    if structured is not None:
        body["structured_output"] = structured
    return body


@pytest.fixture()
def stub(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    exe = bin_dir / "claude"
    exe.write_text(STUB, encoding="utf-8")
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    stub_dir = tmp_path / "stub"
    stub_dir.mkdir()
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("STUB_DIR", str(stub_dir))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    # 하네스 핀 강제 (C3, D109): 핀 일치 버전 응답 + 프로세스 캐시 리셋
    monkeypatch.setenv("STUB_VERSION", f"{cli_client.HARNESS_PIN} (Claude Code)")
    monkeypatch.setattr(cli_client, "_harness_version_actual", None)
    monkeypatch.setattr(gr, "_HARNESS_VERSION", None)
    monkeypatch.setattr(cli_client, "freeze_state", lambda: {"head": "a" * 40,
                                                              "clean_tree": True})
    monkeypatch.setattr(gr, "answer_key", lambda oid, *a, **k: {"group": "treatment",
                                                       "scheme_summary": "s",
                                                       "scheme_type": ["x"],
                                                       "manipulation_period": [None, None],
                                                       "genre_tag_row": None})

    class Stub:
        dir = stub_dir

        @staticmethod
        def set_responses(*objs):
            (stub_dir / "responses.json").write_text(json.dumps(list(objs)), encoding="utf-8")

        @staticmethod
        def calls():
            return [json.loads(p.read_text(encoding="utf-8"))
                    for p in sorted(stub_dir.glob("call_*.json"))]

    return Stub


OUTPUT = {"case_id": "case_01", "misstatement_probability": 80}


def test_pin_success_no_fallback(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("OK") and "[fallback]" not in status
    grade = json.loads((tmp_path / "g" / "case_01.json").read_text(encoding="utf-8"))
    assert grade["_meta"]["grader_pin_used"] == gr.GRADER_PIN
    assert grade["_meta"]["fallback_used"] is False
    (call,) = stub.calls()
    assert call["argv"][call["argv"].index("--model") + 1] == gr.GRADER_PIN


def test_fallback_triggered_on_pin_failure_and_logged(stub, tmp_path):
    # 핀 모델 2회 실패(error) → 폴백 opus-4-8 성공. D6: 발동 기록.
    stub.set_responses(resp(is_error=True, result="API Error"),
                       resp(is_error=True, result="API Error"),
                       resp(GRADE, model=gr.GRADER_FALLBACK))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("OK") and "[fallback]" in status
    grade = json.loads((tmp_path / "g" / "case_01.json").read_text(encoding="utf-8"))
    assert grade["_meta"]["fallback_used"] is True
    assert grade["_meta"]["grader_pin_used"] == gr.GRADER_FALLBACK
    models = [c["argv"][c["argv"].index("--model") + 1] for c in stub.calls()]
    assert models == [gr.GRADER_PIN, gr.GRADER_PIN, gr.GRADER_FALLBACK]


def test_double_failure_marks_case_fail_and_continues(stub, tmp_path):
    stub.set_responses(resp(is_error=True, result="API Error"))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("FAIL")
    assert not (tmp_path / "g" / "case_01.json").exists()


def test_idempotent_skip_on_valid_existing_grade(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    out = tmp_path / "g"
    gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    original_bytes = (out / "case_01.json").read_bytes()
    status = gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    assert status.startswith("skip")
    assert len(stub.calls()) == 1
    assert (out / "case_01.json").read_bytes() == original_bytes


def test_date_suffixed_served_model_skips_without_sibling(stub, tmp_path):
    stub.set_responses(resp(GRADE, model=f"{gr.GRADER_PIN}-20260101"))
    out = tmp_path / "g"
    gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    call_count = len(stub.calls())

    status = gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")

    assert status.startswith("skip")
    assert len(stub.calls()) == call_count
    assert not list(out.glob("case_01.fp-*.json"))
    grade = json.loads((out / "case_01.json").read_text(encoding="utf-8"))
    assert grade["_meta"]["fingerprint"]["grader_model"] == gr.GRADER_PIN
    assert grade["_meta"]["grader_model_reported"] == f"{gr.GRADER_PIN}-20260101"


def test_grading_payload_contains_answer_key_and_output(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    (call,) = stub.calls()
    payload = json.loads(call["stdin"])
    assert set(payload) == {"answer_key", "evaluatee_output"}
    assert payload["evaluatee_output"]["case_id"] == "case_01"


def test_fingerprint_content_and_each_field_affects_identity(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    out = tmp_path / "g"
    gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    fingerprint = json.loads((out / "case_01.json").read_text())["_meta"]["fingerprint"]
    assert set(fingerprint) == {
        "evaluatee_output_sha256", "answer_key_sha256", "rubric_sha256",
        "grade_schema_sha256", "grader_system_prompt_sha256", "grader_model",
        "grader_harness_version", "pipeline_commit",
    }
    assert fingerprint["evaluatee_output_sha256"] == gr._canonical_sha256(OUTPUT)
    assert fingerprint["answer_key_sha256"] == gr._canonical_sha256(
        gr.answer_key("TXX"))
    assert fingerprint["rubric_sha256"] == fingerprint["grader_system_prompt_sha256"]
    assert fingerprint["grade_schema_sha256"] == gr._canonical_sha256(gr.GRADE_SCHEMA)
    assert fingerprint["grader_model"] == gr.GRADER_PIN
    assert fingerprint["grader_harness_version"] == f"{cli_client.HARNESS_PIN} (Claude Code)"
    assert fingerprint["pipeline_commit"] == "a" * 40
    baseline = gr._canonical_sha256(fingerprint)
    for field in fingerprint:
        changed = dict(fingerprint)
        changed[field] = changed[field] + "-changed"
        assert gr._canonical_sha256(changed) != baseline


def test_legacy_grade_fails_closed_and_opt_in_skips(stub, tmp_path):
    out = tmp_path / "g"
    out.mkdir()
    path = out / "case_01.json"
    path.write_text(json.dumps({**GRADE, "_meta": {"case_id": "case_01"}}), encoding="utf-8")
    original_bytes = path.read_bytes()
    status = gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    assert status.startswith("FAIL (stale_legacy_grade")
    assert "--accept-legacy-grade" in status
    assert path.read_bytes() == original_bytes
    status = gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note",
                          accept_legacy_grade=True)
    assert "ACCEPTED" in status
    assert stub.calls() == []


def test_mismatch_writes_sibling_then_third_run_skips_without_call(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    out = tmp_path / "g"
    gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    original = out / "case_01.json"
    original_bytes = original.read_bytes()
    changed_output = {**OUTPUT, "misstatement_probability": 81}
    status = gr.grade_one("case_01", "TXX", changed_output, out, tmp_path / "l", "note")
    assert status.startswith("OK stale-superseding")
    siblings = list(out.glob("case_01.fp-*.json"))
    assert len(siblings) == 1
    sibling_bytes = siblings[0].read_bytes()
    assert original.read_bytes() == original_bytes

    # A third run must find the matching sibling before invoking the CLI.
    call_count = len(stub.calls())
    status = gr.grade_one("case_01", "TXX", changed_output, out, tmp_path / "l", "note")
    assert status == "skip (멱등 — fp-sibling 일치)"
    assert len(stub.calls()) == call_count
    assert original.read_bytes() == original_bytes
    assert siblings[0].read_bytes() == sibling_bytes


# ── R2-7: dim3 정답지 fail-closed + 장르 표 파라미터화 ─────────────────────

def _answer_key_fixture(tmp_path, group):
    cands = {"candidates": [{"case_id": "T99", "group": group,
                             "scheme_summary": "s", "scheme_type": ["x"]}]}
    cands_path = tmp_path / "cands.json"
    cands_path.write_text(json.dumps(cands), encoding="utf-8")
    genre_path = tmp_path / "genre.md"
    genre_path.write_text("| T01 | other-wave row |\n", encoding="utf-8")
    return str(cands_path), str(genre_path)


def test_answer_key_fails_closed_on_treatment_without_genre_row(tmp_path):
    """R2-7: SYSTEM 프롬프트는 dim3 채점을 요구하는데 정답 장르 행이 없으면
    (wave-2 실측: 9/9 실험군 miss → 즉석 채점) 채점 시작 전에 정지해야 한다."""
    cands_path, genre_path = _answer_key_fixture(tmp_path, "treatment")
    with pytest.raises(gr.AnswerKeyError):
        gr.answer_key("T99", cands_path, genre_path)


def test_answer_key_control_without_genre_row_stays_null(tmp_path):
    cands_path, genre_path = _answer_key_fixture(tmp_path, "control")
    key = gr.answer_key("T99", cands_path, genre_path)
    assert key["genre_tag_row"] is None


def test_answer_key_reads_parameterized_genre_table(tmp_path):
    cands_path, genre_path = _answer_key_fixture(tmp_path, "treatment")
    Path(genre_path).write_text("| T99 | revenue timing |\n", encoding="utf-8")
    key = gr.answer_key("T99", cands_path, genre_path)
    assert key["genre_tag_row"] == "| T99 | revenue timing |"


# ── R3-6: 채점 정본 기록 원자성 (tmp→replace, D67 판형) ────────────────────

def test_grade_write_atomic_crash_leaves_no_corrupt_canonical(stub, tmp_path, monkeypatch):
    """크래시 부분 기록이 정본이 되면 _existing_grade_valid가 영영 False —
    재채점 전부가 fp-sibling으로 우회되고 소비자는 부패 정본에서 죽는다."""
    stub.set_responses(resp(GRADE))
    real_write = Path.write_text

    def crashing(self, text, *args, **kwargs):
        if self.name.endswith(".json.tmp"):
            real_write(self, text[:10], *args, **kwargs)
            raise OSError("simulated crash mid-write")
        return real_write(self, text, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", crashing)
    with pytest.raises(OSError, match="simulated crash"):
        gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert not (tmp_path / "g" / "case_01.json").exists(), \
        "크래시 부분 기록이 정본 채점 파일로 남음"


def test_grade_write_leaves_no_tmp_residue(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("OK")
    assert not list((tmp_path / "g").glob("*.tmp"))
