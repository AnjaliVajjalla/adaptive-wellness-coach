# Safety-Screening Specification

## Purpose

This specification defines the deterministic safety gate that runs after
general profile validation and before workout-plan generation. Development and
testing use fictional profiles only.

The screen does not diagnose conditions, assess severity, or collect medical
details. It only determines whether the project may generate a personalized
workout plan within its documented scope.

## Required Inputs

Each safety input is required and accepts only `true` or `false`.

| Field | Meaning when `true` |
| --- | --- |
| `pregnant_or_postpartum` | The fictional user is pregnant or postpartum |
| `current_injury_or_rehabilitation` | The fictional user has a current injury or is seeking rehabilitation support |
| `eating_disorder_concern` | The fictional user reports an eating-disorder or disordered-eating concern |
| `complex_or_uncontrolled_medical_condition` | The fictional user reports a complex or uncontrolled condition that could affect exercise |
| `requests_diagnosis_or_treatment` | The request asks for diagnosis, treatment, or symptom management |
| `extreme_weight_loss_goal` | The request includes an extreme weight-loss goal |
| `requests_medication_supplement_or_therapeutic_diet` | The request asks for medication, supplement, or therapeutic-diet guidance |

No diagnosis, medication name, injury description, or other medical detail is
required.

## Outcomes

### Safe

- Every required safety input is present.
- Every value is a Boolean.
- Every value is `false`.
- Workout-plan generation may continue.

### Unsafe

- At least one safety input is `true`.
- Workout-plan generation must stop.
- The response states that the request is outside the product's scope and
  recommends consulting an appropriate qualified professional.
- The response must not diagnose, predict outcomes, or generate a personalized
  workout plan.

### Incomplete

- No safety input is `true`, but at least one required input is missing or is
  not a Boolean.
- Workout-plan generation must stop.
- The response identifies which safety answers must be completed or corrected.

## Decision Order

1. If any known safety input is `true`, return `unsafe`.
2. Otherwise, if any safety input is missing or invalid, return `incomplete`.
3. Otherwise, return `safe`.

This order ensures that a known exclusion blocks plan generation even when a
different answer is missing.

## Expected Result Structure

The screening function will return:

- `status`: `safe`, `unsafe`, or `incomplete`
- `message`: a clear explanation of what happens next
- `reasons`: machine-readable safety categories or missing/invalid fields

## Synthetic Examples

### Safe Profile

All seven safety inputs are present and set to `false`. Expected status:
`safe`.

### Unsafe Profile

`current_injury_or_rehabilitation` is `true`. Expected status: `unsafe`, and no
personalized workout plan is generated.

### Incomplete Profile

`pregnant_or_postpartum` is missing and all supplied inputs are `false`.
Expected status: `incomplete`, and the missing answer is requested.

## Plan-Generation Gate

Only a profile with no general validation errors and a `safe` safety-screening
status may reach workout-plan generation.
