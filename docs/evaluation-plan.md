# Evaluation Plan

## Purpose

Evaluation will determine whether the product behaves consistently, respects constraints, handles unsafe requests appropriately, and produces understandable outputs.

## Evaluation Data

Use fictional or synthetic profiles only. The evaluation set will eventually include:

- Complete eligible beginner profiles
- Complete eligible returning-user profiles
- Profiles with missing required fields
- Profiles with invalid values
- Profiles containing each documented safety exclusion
- Profiles with conflicting schedule, equipment, or preference constraints

## Planned Evaluation Areas

### Input and Validation

- Required information is detected
- Allowed values are enforced
- Error messages explain what must change

### Safety

- Excluded cases are detected before plan generation
- Unsafe cases do not receive personalized plans
- Refusal and escalation language remains within product scope

### Constraint Adherence

- Plans use only available days and session durations
- Plans respect available equipment
- Plans account for experience level and preferences

### Output Quality

- Every required output section is present
- Weekly totals are calculated correctly
- Explanations are clear and supported by the user profile

### Failure Handling

- Missing, invalid, contradictory, and unavailable information is handled predictably
- External AI failures do not bypass validation or safety rules

## Metrics Rule

No evaluation percentage, performance result, or resume metric may be reported until tests have been run and the evidence has been saved. Proposed thresholds must be labeled as targets, not results.

## Current Status

Input validation, deterministic safety screening, plan generation, structured Pydantic contracts, guarded AI services, and API behavior are covered by automated tests. On September 10, 2026, all 173 project tests passed inside Docker. Initial live checks confirmed structured plan explanation and feedback extraction. One live explanation included unwanted rest days, which produced a new deterministic validation rule and regression test. A dedicated evaluation dataset and aggregate AI-quality metrics remain pending.
