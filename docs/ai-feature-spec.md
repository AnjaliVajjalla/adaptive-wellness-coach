# AI Explanation and Feedback Specification

## Purpose

Use AI only where natural-language interpretation adds value. The deterministic Python workflow remains responsible for validation, safety decisions, exercise selection, scheduling, prescriptions, and totals.

## Plan Explanation

The AI receives a completed, validated weekly plan and returns:

- `weekly_summary`: one short summary of the week
- `day_explanations`: one sentence for each workout or recovery day

The AI must not add exercises, change the schedule, alter prescriptions or totals, make medical claims, or override safety decisions.

The returned explanation days must exactly match the plan's workout and recovery days. Extra rest days or missing activity days trigger the deterministic fallback.

## Feedback Interpretation

The AI receives free-text feedback and returns:

- `difficulty`: `too_easy`, `appropriate`, `too_hard`, or `not_stated`
- `missed_days`: zero or more weekdays
- `disliked_exercises`: zero or more exercise identifiers
- `requested_focus`: an optional supported focus extracted from the feedback
- `requires_safety_rescreening`: whether the feedback may contain a new safety concern

The AI extracts signals only. Deterministic Python validates the output and decides which approved adjustment rules to apply.

Exercise identifiers are checked against the server-owned exercise library. The client does not supply the allowed identifier list.

## Required Processing Order

1. Validate the existing profile and safety answers.
2. Generate the plan with deterministic Python.
3. Ask the AI for a schema-constrained explanation or feedback interpretation.
4. Validate the AI response with Pydantic.
5. Allow deterministic Python to use only validated fields.

## Failure Handling

- If the AI request fails, return the existing deterministic explanation or a clear unavailable message.
- If the AI output fails validation, reject it and use the fallback behavior.
- If feedback may indicate a new safety concern, do not automatically adjust the plan. Require safety rescreening.
- Never allow AI output to bypass the existing validation or safety gates.
- Automated tests must use fake clients and must not inherit real API credentials.

## API Endpoints

- `POST /ai/plan-explanations`: returns a validated explanation and whether the deterministic fallback was used
- `POST /ai/feedback-interpretations`: returns validated feedback signals or an explicit unsuccessful result

The provider reads `OPENAI_API_KEY` and `OPENAI_MODEL` from local environment settings. Secrets are not stored in source code or Docker images.

## Acceptance Criteria

- Both AI outputs have strict Pydantic contracts.
- Structured outputs use only documented fields and allowed values.
- Plan explanations cannot change the underlying plan.
- Feedback signals do not directly modify plans.
- API failures, invalid outputs, and possible safety concerns have tested fallback behavior.
