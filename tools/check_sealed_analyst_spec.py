"""Fence check for specs/SEALED_ANALYST_V0_1.md (D-P62).

Exactly one draft-07 schema fence (check_schema-clean); every other json
fence validates as an instance against it (worked example machine-checked).
"""
import json, re, sys
import jsonschema

FENCE = chr(96) * 3

def main() -> int:
    text = open("specs/SEALED_ANALYST_V0_1.md", encoding="utf-8").read()
    blocks = re.findall(FENCE + "json" + chr(10) + "(.*?)" + FENCE, text, re.S)
    parsed = [json.loads(b) for b in blocks]
    schemas = [d for d in parsed
               if isinstance(d, dict) and "draft-07" in str(d.get("$schema", ""))]
    if len(schemas) != 1:
        print(f"FAIL: expected exactly one draft-07 schema fence, got {len(schemas)}")
        return 1
    jsonschema.Draft7Validator.check_schema(schemas[0])
    validator = jsonschema.Draft7Validator(schemas[0],
                                           format_checker=jsonschema.FormatChecker())
    n = 0
    for d in parsed:
        if d is not schemas[0]:
            validator.validate(d)
            n += 1
    print(f"PASS: schema valid; {n} instance fence(s) validated")
    return 0

if __name__ == "__main__":
    sys.exit(main())
