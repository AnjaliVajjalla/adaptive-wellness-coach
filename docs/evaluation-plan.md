# Evaluation Plan

## Purpose

Evaluation will determine whether the product behaves consistently, respects constraints, handles unsafe requests appropriately, and produces understandable outputs.

## Evaluation Data

Use fictional or synthetic data only. Deterministic behavior is covered by
pytest. The first AI evaluation dataset contains 20 fictional feedback cases
covering:

- Direct and indirect difficulty statements
- One or more missed workout days
- Known disliked exercise identifiers
- Requested workout focus
- Possible safety-rescreening signals
- Negation, contrast, and multiple signals in one statement

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

Input validation, deterministic safety screening, plan generation, structured
Pydantic contracts, guarded AI services, evaluation behavior, and API behavior
are covered by 179 automated tests in Docker.

The live 20-case feedback baseline scored 95% whole-case accuracy. Four fields
scored 100%, while difficulty scored 95%. Review showed that the only failed
case had an ambiguous reference label. The case wording was clarified, and a
targeted live retest passed every field. See the
[Feedback Evaluation Baseline](../evals/results/feedback-baseline.md) for the
measured results and limitations.
