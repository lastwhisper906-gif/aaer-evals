"""Semantic constraints for llm_output_v2 that JSON Schema does not express."""

CHECKLIST_IDS = {f"CL{index}" for index in range(1, 9)}


def validate_v2(record: dict) -> list[str]:
    """Return semantic-contract violations; an empty list means pass."""
    violations = []
    item_ids = [item.get("item_id") for item in record.get("checklist", [])]
    present_ids = set(item_ids)

    if present_ids != CHECKLIST_IDS:
        violations.append("checklist item_ids must be exactly CL1..CL8")
    if len(item_ids) != len(present_ids):
        violations.append("checklist item_ids must each appear once")

    score = record.get("misstatement_risk_score")
    tier = record.get("overall", {}).get("risk_tier")
    if isinstance(score, (int, float)):
        if score >= 70 and tier != "elevated":
            violations.append("score >= 70 requires elevated risk_tier")
        if score < 40 and tier == "elevated":
            violations.append("score < 40 forbids elevated risk_tier")

    top_signals = set(record.get("overall", {}).get("top_signals", []))
    if not top_signals <= present_ids:
        violations.append("top_signals must reference checklist item_ids that appear")

    return violations
