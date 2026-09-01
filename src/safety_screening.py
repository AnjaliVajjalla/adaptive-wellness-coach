"""Deterministic safety screening for fictional wellness profiles."""

from collections.abc import Mapping


REQUIRED_SAFETY_FIELDS = [
    "pregnant_or_postpartum",
    "current_injury_or_rehabilitation",
    "eating_disorder_concern",
    "complex_or_uncontrolled_medical_condition",
    "requests_diagnosis_or_treatment",
    "extreme_weight_loss_goal",
    "requests_medication_supplement_or_therapeutic_diet",
]

SAFE_MESSAGE = (
    "Safety screening passed. Workout-plan generation may continue."
)

UNSAFE_MESSAGE = (
    "This request is outside the Adaptive Wellness Coach's intended scope. "
    "A personalized workout plan will not be generated. Please consult an "
    "appropriate qualified professional."
)


def _display_name(field):
    return field.replace("_", " ")


def _incomplete_result(fields):
    readable_fields = ", ".join(_display_name(field) for field in fields)
    return {
        "status": "incomplete",
        "message": (
            "Safety screening is incomplete. Complete or correct: "
            f"{readable_fields}."
        ),
        "reasons": fields,
    }


def screen_safety(safety_answers):
    """Return a safe, unsafe, or incomplete screening result."""
    if not isinstance(safety_answers, Mapping):
        return _incomplete_result(REQUIRED_SAFETY_FIELDS.copy())

    triggered_fields = [
        field
        for field in REQUIRED_SAFETY_FIELDS
        if safety_answers.get(field) is True
    ]

    missing_or_invalid_fields = [
        field
        for field in REQUIRED_SAFETY_FIELDS
        if field not in safety_answers
        or not isinstance(safety_answers[field], bool)
    ]

    if triggered_fields:
        return {
            "status": "unsafe",
            "message": UNSAFE_MESSAGE,
            "reasons": triggered_fields,
        }

    if missing_or_invalid_fields:
        return _incomplete_result(missing_or_invalid_fields)

    return {
        "status": "safe",
        "message": SAFE_MESSAGE,
        "reasons": [],
    }
