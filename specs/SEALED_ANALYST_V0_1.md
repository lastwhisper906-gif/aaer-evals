# SEALED_ANALYST_V0_1 — Sealed Analyst task contract

> **SPECIFICATION ONLY — D-P50 Phase 2 #10.** This document records the
> owner's direction: “decision-grade output (3-level verdict / falsifiable
> calls / covenant-style triggers)” and the formula list “disclosure-event
> mapping, XBRL trigger recomputation, sector-ETF excess-return windows and
> thresholds.” It does not wire a schema, alter a call path, or authorize a
> model run.
>
> **Scope and disclaimer (INV-14):** 본 결과는 Claude 기반 단일 파이프라인에
> 한정된다. 채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적이며 투자
> 자문이 아니다. 분석 대상에 대한 보유 또는 공매도 포지션은 없다. Every
> published number requires a link to its original filing.

## 1. Task definition

For each sealed case, the evaluatee emits one object containing:

1. a three-level `verdict`, with decision semantics `flag` = escalate for
   immediate human review, `review` = place in the ordinary review queue, and
   `no_flag` = do not escalate under this frozen protocol;
2. one or more **falsifiable calls**, each a proposition, a date on which it
   becomes resolvable, an expected mechanical outcome, and the trigger IDs
   that resolve it; and
3. one or more **covenant-style triggers**, each a threshold condition on one
   named XBRL series during a closed date window.

The task does not ask whether a company committed wrongdoing. Facts and
hypotheses remain separate, and descriptions must follow INV-13's vocabulary
rules. Every numeric input and score must be recomputable from committed
artifacts. Array order is semantic: calls and triggers are ranked from most to
least decision-relevant; IDs are unique within their array.

## 2. Embedded JSON Schema v0.1

This is the only normative schema. It is draft-7 and deliberately embedded,
not installed under `schemas/`. `format: "date"` is an annotation in draft-7;
under the pinned validator it is enforced only when a `FormatChecker` is
explicitly attached. D-P38 records the current boundary: date-only checking is
built in, while date-time and URI checking are not relied upon. Scoring
therefore also parses every date with Python `date.fromisoformat` and rejects
invalid or non-canonical values before arithmetic.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "SEALED_ANALYST_V0_1",
  "title": "Sealed Analyst v0.1 evaluatee output",
  "description": "Decision-grade ordinal output. Values are not probabilities. Descriptions and rationales must separate filed facts from hypotheses and obey INV-13 vocabulary rules.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "case_id",
    "as_of_date",
    "verdict",
    "verdict_rationale_fact_refs",
    "falsifiable_calls",
    "triggers"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "enum": ["0.1"]
    },
    "case_id": {
      "type": "string",
      "minLength": 1,
      "description": "Opaque case identifier; not a company allegation."
    },
    "as_of_date": {
      "type": "string",
      "format": "date",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
      "description": "Sealed information cutoff. All cited facts must have filed dates on or before this date."
    },
    "verdict": {
      "type": "string",
      "enum": ["flag", "review", "no_flag"],
      "description": "Three-level ordinal decision state, not a probability: immediate escalation, ordinary review, or no escalation."
    },
    "verdict_rationale_fact_refs": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "description": "Committed-artifact fact IDs supporting the verdict; hypotheses are not fact references.",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "falsifiable_calls": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["call_id", "proposition", "resolution_date", "expected_resolution", "trigger_ids"],
        "properties": {
          "call_id": {
            "type": "string",
            "pattern": "^C[1-9][0-9]*$"
          },
          "proposition": {
            "type": "string",
            "minLength": 1,
            "description": "Falsifiable statement resolved only by the referenced mechanical triggers; no advice or probability language."
          },
          "resolution_date": {
            "type": "string",
            "format": "date",
            "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
          },
          "expected_resolution": {
            "type": "string",
            "enum": ["crossed", "not_crossed"]
          },
          "trigger_ids": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "pattern": "^T[1-9][0-9]*$"
            }
          }
        }
      }
    },
    "triggers": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "trigger_id",
          "namespace",
          "tag",
          "unit",
          "period_type",
          "duration_days",
          "window_start",
          "window_end",
          "comparator",
          "threshold",
          "rounding_decimals"
        ],
        "properties": {
          "trigger_id": {
            "type": "string",
            "pattern": "^T[1-9][0-9]*$"
          },
          "namespace": {
            "type": "string",
            "minLength": 1,
            "description": "Exact XBRL namespace, such as us-gaap."
          },
          "tag": {
            "type": "string",
            "minLength": 1,
            "description": "Exact XBRL concept name; no fuzzy tag substitution."
          },
          "unit": {
            "type": "string",
            "minLength": 1,
            "description": "Exact XBRL unit; no implicit conversion."
          },
          "period_type": {
            "type": "string",
            "enum": ["instant", "duration"]
          },
          "duration_days": {
            "type": ["integer", "null"],
            "minimum": 1,
            "description": "Null exactly for instant facts; exact inclusive day count for duration facts."
          },
          "window_start": {
            "type": "string",
            "format": "date",
            "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
          },
          "window_end": {
            "type": "string",
            "format": "date",
            "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
          },
          "comparator": {
            "type": "string",
            "enum": ["gt", "gte", "lt", "lte"]
          },
          "threshold": {
            "type": "number",
            "description": "Threshold expressed in the exact named unit."
          },
          "rounding_decimals": {
            "type": "integer",
            "minimum": 0,
            "maximum": 6,
            "description": "Decimal places for ROUND_HALF_EVEN before comparison."
          }
        },
        "allOf": [
          {
            "if": {"properties": {"period_type": {"const": "instant"}}},
            "then": {"properties": {"duration_days": {"type": "null"}}}
          },
          {
            "if": {"properties": {"period_type": {"const": "duration"}}},
            "then": {"properties": {"duration_days": {"type": "integer", "minimum": 1}}}
          }
        ]
      }
    }
  }
}
```

Cross-field validation, performed deterministically in addition to draft-7,
requires unique `call_id` and `trigger_id` values; every `trigger_ids` member
must resolve to a trigger; `as_of_date < window_start <= window_end <=
resolution_date`; and every instant/duration pairing must obey the schema.

## 3. Normative deterministic scoring

### 3.1 Canonical inputs and arithmetic

The scorer consumes only (a) the sealed instance, (b) a committed disclosure
event-registry snapshot identified by SHA-256, and (c) committed XBRL fact
artifacts identified by SHA-256. It sorts records by the keys stated below;
filesystem order never participates. Invalid schema or cross-field structure
produces `invalid_output`, zero total points, and no discretionary repair.

Dates are canonical ISO dates. Numeric strings are parsed as base-10 `Decimal`;
float arithmetic is forbidden. `round_d(x) = Decimal(x).quantize(10^-d,
ROUND_HALF_EVEN)`. Comparators mean exactly `gt: x > threshold`, `gte: x >=
threshold`, `lt: x < threshold`, and `lte: x <= threshold`, after both operands
are rounded with `round_d`. These rounding and comparator choices are
**PRE-REGISTERED CONSTANTS**: decimal arithmetic prevents platform drift;
half-even avoids a directional tie bias; and four explicit operators eliminate
natural-language boundary discretion. The allowed `rounding_decimals` range
0–6 is a **PRE-REGISTERED CONSTANT**, wide enough for whole currency through
common per-share XBRL precision while bounding false precision.

### 3.2 Verdict from disclosure events (30 points)

The registry row key is `(case_id, event_type, event_date, accession_or_release,
source_sha256)`. Only rows with `event_date <= case_cutoff_date +
HORIZON_DAYS` enter, where `HORIZON_DAYS = 730` is a **PRE-REGISTERED
CONSTANT** of this spec (24 months — the repo's existing provisional-label
window convention, HOLDOUT_CONTROLS_PLAN (g)). The horizon is a property of
the CASE and the SPEC, never of the evaluatee's output: submission-chosen
`resolution_date` values MUST NOT alter which registry rows enter ground
truth (a submission-dependent horizon would let early resolution dates
truncate the event window and manufacture `no_flag` truth — rejected at
review, D-P62). Calls whose `resolution_date` exceeds the horizon are
scored against the horizon-bounded registry state.
Source hierarchy, strongest first, is:

1. SEC AAER release naming the issuer (`aaer`) → `flag`;
2. EDGAR 8-K Item 4.02 non-reliance disclosure (`item_402_nonreliance`) →
   `flag`;
3. EDGAR filing that presents restated financial statements without a registry
   Item 4.02 (`restatement_filing`) → `review`;
4. no qualifying committed row through the horizon → `no_flag`.

Precedence is the first applicable level above, independent of event discovery
or insertion order. A row without its committed source hash, event date, and
accession/release identifier is unusable and causes `registry_incomplete`, not
`no_flag`. Thus, given a snapshot, `truth_verdict = precedence(valid rows)` is a
pure recomputation. `verdict` earns 30 points for exact equality, otherwise 0.
The 30-point weight is a **PRE-REGISTERED CONSTANT**: it makes the principal
decision material without allowing it alone to pass the task.

### 3.3 Trigger recomputation and call resolution (60 points)

Fact eligibility follows `pipeline/cutoff_guard.py`: loading must pass through
`load_xbrl_facts`; `filed <= relevant cutoff` includes equality; the fact's
accession filing date must agree with submissions; mismatch, unknown accession,
or unavailable cross-check fails closed. For resolution, `relevant cutoff` is
the call's `resolution_date`; future implementation therefore requires a
signed registry/call path rather than bypassing the guard.

For trigger `t`, select facts whose namespace, tag, and unit exactly equal the
declared values and whose filing date is no later than the linked call's
resolution date. Period alignment is exact:

- instant: `window_start <= fact.end <= window_end` and `duration_days = null`;
- duration: `fact.start = window_start`, `fact.end = window_end`, and
  `(fact.end - fact.start).days + 1 = duration_days`.

Among duplicate eligible facts for the same period, choose the greatest tuple
`(filed, accession)` lexicographically; this latest-filed rule is a
**PRE-REGISTERED CONSTANT** consistent with the repository's point-in-time
alignment convention. No tag, unit, scale, fiscal-period, or nearest-date
substitution is allowed. Apply the declared comparator to the selected fact's
rounded value. No eligible fact, malformed decimals, conflicting duplicate
keys, or missing accession resolution yields `insufficient_data` for that
trigger and its linked calls—never `not_crossed`.

For a call with referenced trigger results `R`, its mechanical actual outcome
is `crossed` iff every member of `R` is `true`; it is `not_crossed` iff at least
one is `false` and none is `insufficient_data`; otherwise it is
`insufficient_data`. Logical AND is a **PRE-REGISTERED CONSTANT** because a
covenant composed of named conditions is satisfied only when all enumerated
conditions hold. The call is correct iff actual outcome exactly equals
`expected_resolution`; insufficient calls earn 0 and are reported separately.

Each trigger earns `20 / number_of_triggers` points when it is determinately
recomputable (true or false), otherwise 0. Each call earns `40 /
number_of_calls` points when correct, otherwise 0. The 20/40 split is a
**PRE-REGISTERED CONSTANT**: call accuracy receives twice the weight of the
supporting data-contract completeness, while array-size normalization prevents
point inflation.

### 3.4 Every remaining field (10 points) and total

The following binary checks each earn the stated points:

| Field | Deterministic check | Points | Constant basis |
|---|---|---:|---|
| `schema_version` | exact `0.1` | 1 | schema version, sourced here |
| `case_id` | exact registry case key | 1 | committed registry identity |
| `as_of_date` | exact sealed cutoff and every evaluatee-visible rationale source filing `<=` it; later resolution facts remain governed by §3.3's resolution-date cutoff | 2 | `cutoff_guard.py` inclusive convention |
| `verdict_rationale_fact_refs` | every unique ID exists in the committed input manifest | 2 | fail-closed provenance rule |
| call `call_id`, `proposition`, `resolution_date`, `trigger_ids` | all cross-field rules pass; proposition normalized with Unicode NFC and whitespace collapse is nonempty | 2 | **PRE-REGISTERED CONSTANT**: structural resolvability, not prose quality |
| trigger `trigger_id`, `namespace`, `tag`, `unit`, `period_type`, `duration_days`, `window_start`, `window_end`, `comparator`, `threshold`, `rounding_decimals` | all schema, referential, and exact-alignment checks pass | 2 | **PRE-REGISTERED CONSTANT**: complete recomputation tuple |

No points assess eloquence. `total = metadata_points + verdict_points +
trigger_points + call_points`, exactly 0–100; report it as an ordinal task score,
never as a probability. No pass threshold is set in v0.1. For context only, the
repository's committed `analysis/decision_table.json` sweeps the ordinal family
40/50/60/70; reusing that family later would require owner signature rather
than silently selecting one here.

## 4. Constant register

| Constant | Value | Status and justification |
|---|---|---|
| verdict order | `flag > review > no_flag` | sourced from `specs/RISK_SCORE_SEMANTICS.md` ordinal decision vocabulary |
| event precedence | AAER, Item 4.02, restatement filing, none | **PRE-REGISTERED CONSTANT**; strongest authoritative disclosure governs, with deterministic ties |
| cutoff boundary | `filed <= cutoff` | sourced from `pipeline/cutoff_guard.py` |
| window boundaries | both inclusive | **PRE-REGISTERED CONSTANT**; matches cutoff equality and eliminates boundary gaps |
| decimal rule | base-10, half-even, 0–6 places | **PRE-REGISTERED CONSTANT**; deterministic and bounded as explained in §3.1 |
| duplicate selection | greatest `(filed, accession)` | **PRE-REGISTERED CONSTANT**; point-in-time latest-filed alignment with stable tie-break |
| multi-trigger connective | AND | **PRE-REGISTERED CONSTANT**; covenant-style conjunction |
| points | metadata 10, verdict 30, calls 40, triggers 20 | **PRE-REGISTERED CONSTANT**; principal decision plus resolution dominate, arrays normalized |
| pass threshold | none | deliberate: `analysis/decision_table.json` supplies only a historical 40/50/60/70 threshold family, not authority for this task |

No other numeric constant is normative in v0.1.

## 5. Worked synthetic example

**Synthetic only:** `SYNTHETIC-SA-001` names no real issuer. Assume the committed
sealed cutoff is 2027-03-31; manifest fact `F-AR-2027Q2` is
`us-gaap:AccountsReceivableNetCurrent`, unit `USD`, instant 125.00 at
2027-06-30, filed 2027-07-20 under accession `0000000000-27-000001`; and the
sealed input manifest contains rationale fact `F-BASE` filed 2027-02-15. The
committed event registry contains an Item 4.02 event dated 2027-07-15. The
instance is:

```json
{
      "schema_version": "0.1",
      "case_id": "SYNTHETIC-SA-001",
      "as_of_date": "2027-03-31",
      "verdict": "flag",
      "verdict_rationale_fact_refs": ["F-BASE"],
      "falsifiable_calls": [
        {
          "call_id": "C1",
          "proposition": "The named receivables series will meet or exceed USD 120 by 2027-07-31.",
          "resolution_date": "2027-07-31",
          "expected_resolution": "crossed",
          "trigger_ids": ["T1"]
        }
      ],
      "triggers": [
        {
          "trigger_id": "T1",
          "namespace": "us-gaap",
          "tag": "AccountsReceivableNetCurrent",
          "unit": "USD",
          "period_type": "instant",
          "duration_days": null,
          "window_start": "2027-04-01",
          "window_end": "2027-07-31",
          "comparator": "gte",
          "threshold": 120,
          "rounding_decimals": 2
        }
      ]
}
```

Walkthrough: schema and cross-field validation pass. The registry hierarchy
maps Item 4.02 to `flag`, so the verdict earns 30/30. The eligible exact-tag,
exact-unit instant is in the inclusive window and filed by resolution;
`round_2(125.00) >= round_2(120)` is true, so T1 earns 20/20. AND over `{true}`
resolves C1 as `crossed`, matching the call for 40/40. Exact metadata,
provenance, call structure, and trigger tuple earn 10/10. Total = 100. Removing
the fact would yield `insufficient_data`, not `not_crossed`: trigger and call
would earn 0, while the other 40 points remain mechanically recomputable.

## 6. Execution preconditions — owner-signature activated

- [ ] Owner signs an append-only D-entry defining the committed event-registry
  schema, source hashes, disclosure dates, hierarchy implementation, and
  snapshot lifecycle.
- [ ] Any price-data acquisition described in Appendix A occurs only in an
  owner-supervised session under INV-23 and is committed with provenance before
  use.
- [ ] Owner signs a future FREEZE_REV before this embedded schema is promoted
  into `schemas/`, validation wiring, scoring code, or a model call path.
- [ ] Tests cover draft-7 plus `FormatChecker`, cross-field rules, Decimal
  boundaries, missing facts, duplicate facts, and registry incompleteness.
- [ ] INV-22 launch and seal gates are independently satisfied. This is a
  candidate for a future forward cycle; it does not modify `cycle_001`'s sealed
  protocol or authorize any run.
- [ ] Human final sign-off and INV-14 publication checks remain mandatory.

## 7. Consistency with risk-score semantics

The relation is explicit, not a supersession:

| Sealed Analyst verdict | `specs/RISK_SCORE_SEMANTICS.md` `decision_state` | Meaning |
|---|---|---|
| `flag` | `flag` | immediate escalation |
| `review` | `review` | ordinary human review |
| `no_flag` | `no_flag` | no escalation under the frozen protocol |

That specification's fourth state, `abstain`, is not a competing fourth verdict.
In this task it is the scorer's fail-closed status for insufficient or invalid
inputs and cannot be emitted to avoid a required three-level choice. Both
systems preserve ordinal discipline: neither verdicts nor the 0–100 task score
carry probability semantics.

## 8. Anti-scope boundary

v0.1 excludes portfolio construction, position sizing, trading rules, expected
returns, valuation targets, advice semantics, price/ETF fields, live data
fetching, schema wiring, call-path changes, and model execution. It makes no
claim that `no_flag` means absence of accounting error or that `flag` establishes
misconduct. The output is a reproducible review-priority contract only.

## Appendix A — NON-NORMATIVE: sector-ETF excess-return preregistration

This appendix is **NON-NORMATIVE**. Price and ETF data are not present in
committed artifacts today; therefore no price, return, ETF, window, or threshold
field appears in the v0.1 schema or score. Promotion requires a new schema
version, owner signature, FREEZE_REV, and committed provenance.

For a future version, pre-register adjusted-close simple returns on trading days:
`R_i[a,b] = P_i[b] / P_i[a] - 1`, where `a` is the last common trading-day close
on or before the event date and `b` is the common trading-day close exactly
`h` trading sessions after `a`. Sector excess return is `ER_h = R_company[a,b]
- R_sectorETF[a,b]`. Use windows `h in {1, 5, 20}` and two-sided materiality
thresholds `|ER_h| >= {0.05, 0.10, 0.20}`. The window set and 5%/10%/20%
threshold grid are **PRE-REGISTERED CONSTANTS**: 1/5/20 represent next-session,
weekly, and approximately monthly horizons; the geometric doubling grid avoids
choosing a cutoff after outcomes. These values are not borrowed from
`analysis/decision_table.json`; that file's 40/50/60/70 grid is an ordinal model
score family with different units.

Required provenance is a committed, content-hashed table containing vendor,
download timestamp, ticker, sector ETF mapping and mapping effective dates,
exchange calendar, raw and adjusted close, split/dividend adjustment factors,
currency, and source URL. Company and ETF must share currency and timestamps;
missing common sessions, stale mapping, absent adjustment factors, or a halted
company produces `insufficient_data`. No interpolation, nearest-ETF
substitution, or zero-fill is allowed. Acquisition is a new external-data fetch
and may occur only with owner supervision under INV-23. The INV-14 posture is
unchanged: no long or short position in an analyzed company, educational and
informational use only, not investment advice, and every published number linked
to its original source.
