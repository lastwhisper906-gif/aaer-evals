"""build_payload base_id(조기성 스냅샷 시드) 로직 — 캐시 불요(로더 몽키패치), CI 상주.

base_id는 EARLINESS_PLAN §2의 "스냅샷 간 동일 k·동일 마스킹" 요건을 만족시킨다.
스냅샷 case_id(case_39_s3)로 교란하면 k가 스냅샷마다 달라져 궤적 비교가 깨진다 —
이 테스트가 base_id 폴백·마스킹·하위호환을 기계 검증한다.
"""
import build_payload as bp


def _patch(monkeypatch):
    monkeypatch.setattr(bp, "load_pit_series", lambda ticker, cutoff: {})
    monkeypatch.setattr(bp, "load_filing_chronology", lambda ticker, cutoff: [])


def test_base_id_makes_perturb_k_constant_across_snapshots(monkeypatch):
    _patch(monkeypatch)
    base = {"case_id": "case_39", "ticker": "OSIR", "cik": "1",
            "company_name": "OSIRIS", "cutoff_date": "2015-11-05"}
    s1 = {**base, "case_id": "case_39_s1", "base_id": "case_39", "cutoff_date": "2015-08-01"}
    s3 = {**base, "case_id": "case_39_s3", "base_id": "case_39", "cutoff_date": "2015-02-01"}
    k_base = bp.build_payload(base, perturb=True)["_k_internal"]
    k1 = bp.build_payload(s1, perturb=True)["_k_internal"]
    k3 = bp.build_payload(s3, perturb=True)["_k_internal"]
    assert k_base == k1 == k3, "스냅샷 간 교란 k가 달라짐 (base_id 미적용)"
    # 대조: base_id 없이 스냅샷 case_id로 교란하면 k가 갈린다 (버그 재현)
    k_wrong = bp.build_payload({**s1, "base_id": "case_39_s1"}, perturb=True)["_k_internal"]
    assert k_wrong != k_base


def test_base_id_masks_identity_consistently(monkeypatch):
    _patch(monkeypatch)
    s = {"case_id": "case_39_s3", "base_id": "case_39", "ticker": "OSIR", "cik": "1",
         "company_name": "OSIRIS", "cutoff_date": "2015-02-01"}
    f = bp.build_payload(s, perturb=True)["case"]
    assert f["case_id"] == "case_39"           # 평가자는 base 마스킹 정체를 본다
    assert f["ticker"] == "XX39"
    assert f["company_name"] == "Company CASE_39"
    assert "cik" not in f
    assert "base_id" not in f                   # 제어 필드 누출 금지
    assert f["cutoff_date"] == "2015-02-01"     # 날짜(as-of)는 스냅샷별로 다르다


def test_base_id_absent_is_byte_identical_legacy(monkeypatch):
    _patch(monkeypatch)
    case = {"case_id": "case_44", "ticker": "ADAM", "cik": "0001273685",
            "company_name": "ADAMAS TRUST, INC.", "cutoff_date": "2016-02-07"}
    # base_id 부재 → 기존 동작. original·perturbed 양쪽에서 base_id 흔적 없음.
    orig = bp.build_payload(case)
    pert = bp.build_payload(case, perturb=True)
    assert orig["case"]["case_id"] == "case_44"
    assert "base_id" not in orig["case"]
    assert pert["case"]["ticker"] == "XX44"
    assert pert["case"]["case_id"] == "case_44"


def test_original_frame_snapshot_strips_base_id_keeps_real_identity(monkeypatch):
    _patch(monkeypatch)
    s = {"case_id": "case_08_s2", "base_id": "case_08", "ticker": "HTZ", "cik": "47129",
         "company_name": "HERTZ", "cutoff_date": "2014-02-01"}
    f = bp.build_payload(s, perturb=False)["case"]
    assert f["case_id"] == "case_08"            # 프레임 일관 (base id)
    assert f["ticker"] == "HTZ" and f["cik"] == "47129"  # 원본 프레임 = 실제 정체 노출
    assert "base_id" not in f
