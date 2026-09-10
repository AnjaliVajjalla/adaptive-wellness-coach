"""Tests for the typed weekly-plan service boundary."""

import pytest
from pydantic import ValidationError

from src.models import PlanGenerationRequest
from src.plan_service import create_weekly_plan


@pytest.fixture
def valid_request_data():
    return {
        "profile": {
            "profile_id": "fictional_service_001",
            "primary_goal": "Get stronger",
            "additional_goals": [],
            "experience_level": "Complete beginner",
            "current_activity_level": "Light",
            "available_workout_days": [
                "Monday",
                "Wednesday",
                "Friday",
            ],
            "session_duration": 30,
            "available_equipment": ["No equipment, bodyweight only"],
            "preferred_activities": ["Bodyweight workouts"],
            "disliked_activities": ["Jogging or running"],
            "preferred_intensity": "Moderate",
        },
        "safety_answers": {
            "pregnant_or_postpartum": False,
            "current_injury_or_rehabilitation": False,
            "eating_disorder_concern": False,
            "complex_or_uncontrolled_medical_condition": False,
            "requests_diagnosis_or_treatment": False,
            "extreme_weight_loss_goal": False,
            "requests_medication_supplement_or_therapeutic_diet": False,
        },
        "challenging_intensity_confirmed": False,
    }


def test_service_returns_a_validated_weekly_plan(valid_request_data):
    request = PlanGenerationRequest.model_validate(valid_request_data)

    result = create_weekly_plan(request)

    assert result.status == "generated"
    assert len(result.days) == 7
    assert result.totals.workout_days == 3


def test_request_rejects_non_boolean_safety_answer(valid_request_data):
    valid_request_data["safety_answers"][
        "current_injury_or_rehabilitation"
    ] = "false"

    with pytest.raises(ValidationError):
        PlanGenerationRequest.model_validate(valid_request_data)


def test_service_returns_typed_blocked_result_for_exclusion(
    valid_request_data,
):
    valid_request_data["safety_answers"][
        "current_injury_or_rehabilitation"
    ] = True
    request = PlanGenerationRequest.model_validate(valid_request_data)

    result = create_weekly_plan(request)

    assert result.status == "blocked"
    assert result.days == []


def test_service_preserves_intensity_confirmation_warning(
    valid_request_data,
):
    valid_request_data["profile"]["preferred_intensity"] = "Challenging"
    request = PlanGenerationRequest.model_validate(valid_request_data)

    result = create_weekly_plan(request)

    assert result.status == "confirmation_required"
    assert result.days == []
