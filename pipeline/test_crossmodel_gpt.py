import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest

import crossmodel_gpt as cross


@pytest.fixture
def case():
    return {"case_id": "C01", "company_name": "Example Co", "ticker": "EX",
            "cik": "0001", "cutoff_date": "2020-12-31"}


@pytest.fixture
def payload():
    return {
        "_variant": "original-C01-r1",
        "_k_internal": None,
        "case": {"company_name": "Example Co", "ticker": "EX"},
        "financial_series_point_in_time": {
            "Revenue": [{"value": 10, "accession": "0001-20-000001",
                         "form": "10-K", "filed": "2020-02-01"}]},
        "filing_chronology": [{"form": "10-K", "filingDate": "2020-02-01"}],
    }


@pytest.fixture
def model_output():
    evidence = [{"quote": "Revenue=10 (FY2019)",
                 "source_accession_no": "0001-20-000001", "location": "Revenue FY2019"}]
    return {
        "checklist": [{"item_id": "CL1", "question": "Receivables trend?",
                       "finding": "insufficient_data", "confidence": "low",
                       "evidence": evidence}],
        "misstatement_probability": 10,
        "mechanism_hypotheses": [],
        "overall": {"risk_tier": "clear", "top_signals": []},
    }


def _event_stream(output, model="gpt-test"):
    return "\n".join([
        json.dumps({"type": "thread.started", "model": model}),
        json.dumps({"type": "item.completed", "item": {
            "type": "agent_message", "text": output}}),
    ]) + "\n"


def _configure_tmp(monkeypatch, tmp_path, payload):
    repo = tmp_path / "repo"
    (repo / "runs" / "crossmodel_gpt").mkdir(parents=True)
    (repo / "schemas").mkdir()
    source_schema = Path(cross.runner.REPO_ROOT) / "schemas" / "llm_output.json"
    (repo / "schemas" / "llm_output.json").write_bytes(source_schema.read_bytes())
    monkeypatch.setattr(cross, "REPO_ROOT", repo)
    monkeypatch.setattr(cross, "ALLOWED_OUT_ROOT", repo / "runs" / "crossmodel_gpt")
    monkeypatch.setattr(cross.build_payload, "build_payload", lambda *a, **k: payload.copy())
    return repo


def test_frozen_frame_reconstruction_has_golden_order(payload):
    expected = ('{"variant": "original-C01-r1", '
                '"perturb_factor_recorded_scoring_side_only": null, '
                '"case": {"company_name": "Example Co", "ticker": "EX"}, '
                '"financial_series_point_in_time": {"Revenue": [{"value": 10, '
                '"accession": "0001-20-000001", "form": "10-K", '
                '"filed": "2020-02-01"}]}, "filing_chronology": '
                '[{"form": "10-K", "filingDate": "2020-02-01"}]}')
    assert cross.frozen_frame_payload(payload) == expected
    assert list(json.loads(expected)) == [
        "variant", "perturb_factor_recorded_scoring_side_only", "case",
        "financial_series_point_in_time", "filing_chronology"]


def test_prompt_contains_model_schema(payload):
    prompt = cross.build_prompt("task text", cross.frozen_frame_payload(payload))
    assert '"mechanism_hypotheses"' in prompt
    assert '"insufficient_data"' in prompt


@pytest.mark.parametrize("name", cross.METERED_ENV_VARS)
def test_metered_environment_is_refused(monkeypatch, name):
    for variable in cross.METERED_ENV_VARS:
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv(name, "present")
    with pytest.raises(RuntimeError, match="metered API"):
        cross.enforce_no_metered_credentials()


def test_output_directory_outside_separated_root_is_refused(monkeypatch, tmp_path):
    monkeypatch.setattr(cross, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(cross, "ALLOWED_OUT_ROOT", tmp_path / "runs" / "crossmodel_gpt")
    with pytest.raises(ValueError, match="runs/crossmodel_gpt"):
        cross.resolve_output_dir(tmp_path / "elsewhere")


def test_invalid_json_retries_once_and_records_failure(
        monkeypatch, tmp_path, case, payload):
    repo = _configure_tmp(monkeypatch, tmp_path, payload)
    calls = []

    def mocked_run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(stdout=_event_stream("not json"), stderr="", returncode=0)

    monkeypatch.setattr(cross.subprocess, "run", mocked_run)
    result = cross.run_case(case, "original", repo / "runs" / "crossmodel_gpt")
    assert result["status"] == "FAIL (invalid_json)"
    assert len(calls) == 2
    meta = json.loads((repo / "runs" / "crossmodel_gpt" /
                       "runmeta_original_C01.json").read_text())
    assert meta["retry_count"] == 1
    assert meta["fail_reason"] == "invalid_json"
    assert not (repo / "runs" / "crossmodel_gpt" / "C01.json").exists()


def test_nonzero_exit_with_valid_json_is_recorded_as_failure(
        monkeypatch, tmp_path, case, payload, model_output):
    repo = _configure_tmp(monkeypatch, tmp_path, payload)

    def mocked_run(command, **kwargs):
        return SimpleNamespace(stdout=_event_stream(json.dumps(model_output)),
                               stderr="failed", returncode=7)

    monkeypatch.setattr(cross.subprocess, "run", mocked_run)
    result = cross.run_case(case, "original", repo / "runs" / "crossmodel_gpt")
    assert result["status"] == "FAIL (codex_exit_7)"
    meta = json.loads((repo / "runs" / "crossmodel_gpt" /
                       "runmeta_original_C01.json").read_text())
    assert meta["fail_reason"] == "codex_exit_7"
    assert not (repo / "runs" / "crossmodel_gpt" / "C01.json").exists()


def test_valid_response_writes_conformant_provenance_and_isolation_command(
        monkeypatch, tmp_path, case, payload, model_output):
    repo = _configure_tmp(monkeypatch, tmp_path, payload)
    commands = []

    def mocked_run(command, **kwargs):
        commands.append((command, kwargs))
        if command[:2] == ["codex", "exec"]:
            return SimpleNamespace(stdout=_event_stream(json.dumps(model_output)),
                                   stderr="", returncode=0)
        if command == ["codex", "--version"]:
            return SimpleNamespace(stdout="codex-cli test\n", stderr="", returncode=0)
        assert command == ["git", "rev-parse", "HEAD"]
        return SimpleNamespace(stdout="abc123\n", stderr="", returncode=0)

    monkeypatch.setattr(cross.subprocess, "run", mocked_run)
    result = cross.run_case(case, "original", repo / "runs" / "crossmodel_gpt")
    assert result["status"] == "OK"
    record = json.loads((repo / "runs" / "crossmodel_gpt" / "C01.json").read_text())
    jsonschema.Draft7Validator(cross.runner.FULL_OUTPUT_SCHEMA).validate(record)
    assert record["run_id"] == "xgpt-original-C01-r1"
    assert record["model"] == "gpt-test"
    assert record["pipeline_version"] == "abc123"
    assert record["fingerprint"]["model_requested"] == "gpt-test"
    assert record["fingerprint"]["harness_version_actual"] == "codex-cli test"
    assert record["fingerprint"]["system_prompt_sha256"]
    command = commands[0][0]
    assert command[:2] == ["codex", "exec"]
    assert ["--sandbox", "read-only"] == command[2:4]
    assert "--ephemeral" in command
    assert "--ignore-user-config" in command
    assert "--ignore-rules" in command
    assert "--json" in command
    assert command[-1] == "-"
    assert "mcp_servers={}" in command
    assert "project_doc_max_bytes=0" in command
    temp_cwd = Path(command[command.index("--cd") + 1])
    assert repo.resolve() not in temp_cwd.parents
    assert (repo / "runs" / "crossmodel_gpt" / "audit_original_C01.jsonl").exists()


def test_unavailable_codex_version_uses_honest_fallback(
        monkeypatch, tmp_path, case, payload, model_output):
    repo = _configure_tmp(monkeypatch, tmp_path, payload)

    def mocked_run(command, **kwargs):
        if command[:2] == ["codex", "exec"]:
            return SimpleNamespace(stdout=_event_stream(json.dumps(model_output)),
                                   stderr="", returncode=0)
        if command == ["codex", "--version"]:
            raise OSError("codex unavailable")
        assert command == ["git", "rev-parse", "HEAD"]
        return SimpleNamespace(stdout="abc123\n", stderr="", returncode=0)

    monkeypatch.setattr(cross.subprocess, "run", mocked_run)
    result = cross.run_case(case, "original", repo / "runs" / "crossmodel_gpt")
    assert result["status"] == "OK"
    record = json.loads((repo / "runs" / "crossmodel_gpt" / "C01.json").read_text())
    assert record["fingerprint"]["harness_version_actual"] == \
        "harness_version_unavailable"


def test_dry_run_has_hashes_and_no_subprocess(
        monkeypatch, tmp_path, capsys, case, payload):
    repo = _configure_tmp(monkeypatch, tmp_path, payload)
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps({"cases": [case]}))

    def forbidden_subprocess(*args, **kwargs):
        pytest.fail("dry-run invoked subprocess")

    monkeypatch.setattr(cross.subprocess, "run", forbidden_subprocess)
    for variable in cross.METERED_ENV_VARS:
        monkeypatch.delenv(variable, raising=False)
    rc = cross.main(["--cases", str(cases_path), "--frame", "original",
                     "--out", str(repo / "runs" / "crossmodel_gpt"), "--dry-run"])
    output = capsys.readouterr().out
    assert rc == 0
    assert "payload_sha256=" in output
    assert "prompt_sha256=" in output
