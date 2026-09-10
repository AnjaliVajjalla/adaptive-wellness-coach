"""Tests for strict Pydantic data contracts."""

import pytest
from pydantic import ValidationError

from src.models import ExerciseEntry, UserProfile, WeeklyPlanResult
from src.weekly_plan_generator import generate_weekly_plan


@pytest.fixture
def valid_profile_data():
    return {
        "profile_id": "fictional_pydantic_001",
        "primary_goal": "Get stronger",
        "additional_goals": ["Improve overall fitness"],
        "experience_level": "Complete beginner",
        "current_activity_level": "Light",
        "available_workout_days": ["Monday", "Wednesday", "Friday"],
        "session_duration": 30,
        "available_equipment": ["No equipment, bodyweight only"],
        "preferred_activities": ["Bodyweight workouts"],
        "disliked_activities": ["Jogging or running"],
        "preferred_intensity": "Moderate",
    }


def test_valid_profile_creates_a_typed_model(valid_profile_data):
    profile = UserProfile.model_validate(valid_profile_data)

    assert profile.profile_id == "fictional_pydantic_001"
    assert profile.session_duration == 30
    assert profile.model_dump() == valid_profile_data


def test_missing_required_field_returns_structured_error(valid_profile_data):
    del valid_profile_data["session_duration"]

    with pytest.raises(ValidationError) as error:
        UserProfile.model_validate(valid_profile_data)

    assert error.value.errors()[0]["loc"] == ("session_duration",)
    assert error.value.errors()[0]["type"] == "missing"


def test_strict_model_rejects_text_instead_of_integer(valid_profile_data):
    valid_profile_data["session_duration"] = "30"

    with pytest.raises(ValidationError):
        UserProfile.model_validate(valid_profile_data)


def test_unsupported_allowed_value_is_rejected(valid_profile_data):
    valid_profile_data["experience_level"] = "Advanced"

    with pytest.raises(ValidationError):
        UserProfile.model_validate(valid_profile_data)


def test_unknown_field_is_rejected(valid_profile_data):
    valid_profile_data["unapproved_note"] = "extra input"

    with pytest.raises(ValidationError) as error:
        UserProfile.model_validate(valid_profile_data)

    assert error.value.errors()[0]["type"] == "extra_forbidden"


def test_duplicate_multi_select_value_is_rejected(valid_profile_data):
    valid_profile_data["available_workout_days"] = ["Monday", "Monday"]

    with pytest.raises(ValidationError):
        UserProfile.model_validate(valid_profile_data)


def test_conflicting_preferences_are_rejected(valid_profile_data):
    valid_profile_data["preferred_activities"] = ["Walking"]
    valid_profile_data["disliked_activities"] = ["Walking"]

    with pytest.raises(ValidationError):
        UserProfile.model_validate(valid_profile_data)


def test_no_equipment_option_must_be_selected_alone(valid_profile_data):
    valid_profile_data["available_equipment"] = [
        "No equipment, bodyweight only",
        "Dumbbells",
    ]

    with pytest.raises(ValidationError):
        UserProfile.model_validate(valid_profile_data)


@pytest.fixture
def safe_answers():
    return {
        "pregnant_or_postpartum": False,
        "current_injury_or_rehabilitation": False,
        "eating_disorder_concern": False,
        "complex_or_uncontrolled_medical_condition": False,
        "requests_diagnosis_or_treatment": False,
        "extreme_weight_loss_goal": False,
        "requests_medication_supplement_or_therapeutic_diet": False,
    }


def test_generated_plan_matches_the_nested_output_contract(
    valid_profile_data,
    safe_answers,
):
    generated = generate_weekly_plan(valid_profile_data, safe_answers)

    validated = WeeklyPlanResult.model_validate(generated)

    assert validated.status == "generated"
    assert len(validated.days) == 7
    assert validated.totals.workout_days == 3


def test_strength_entry_requires_sets_and_repetitions():
    invalid_entry = {
        "exercise_id": "fictional_strength",
        "name": "Fictional strength exercise",
        "activity_type": "strength",
        "equipment": [],
        "prescription_type": "sets_reps",
        "sets": None,
        "repetitions_min": None,
        "repetitions_max": None,
        "minutes": None,
        "effort_guidance": "Use a manageable effort.",
    }

    with pytest.raises(ValidationError):
        ExerciseEntry.model_validate(invalid_entry)


def test_timed_entry_rejects_strength_fields():
    invalid_entry = {
        "exercise_id": "fictional_walk",
        "name": "Fictional walk",
        "activity_type": "cardio",
        "equipment": [],
        "prescription_type": "minutes",
        "sets": 2,
        "repetitions_min": None,
        "repetitions_max": None,
        "minutes": 20,
        "effort_guidance": "Use a manageable effort.",
    }

    with pytest.raises(ValidationError):
        ExerciseEntry.model_validate(invalid_entry)


def test_generated_result_requires_seven_days_and_totals():
    invalid_result = {
        "status": "generated",
        "message": "Generated.",
        "weekly_summary": "A fictional plan.",
        "warnings": [],
        "days": [],
        "totals": None,
        "reasons": [],
    }

    with pytest.raises(ValidationError):
        WeeklyPlanResult.model_validate(invalid_result)
