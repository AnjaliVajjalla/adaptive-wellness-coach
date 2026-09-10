"""Tests for AI-assisted behavior without external API calls."""

from types import SimpleNamespace

from src.ai_service import generate_plan_explanation
from src.models import WeeklyPlanResult
from src.weekly_plan_generator import generate_weekly_plan


class FakeResponsesClient:
    def __init__(self, output=None, error=None):
        self.output = output
        self.error = error
        self.received = None

    def parse(self, **kwargs):
        self.received = kwargs
        if self.error is not None:
            raise self.error
        return SimpleNamespace(output_parsed=self.output)


def fictional_plan():
    profile = {
        "profile_id": "fictional_ai_service_001",
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
    safety_answers = {
        "pregnant_or_postpartum": False,
        "current_injury_or_rehabilitation": False,
        "eating_disorder_concern": False,
        "complex_or_uncontrolled_medical_condition": False,
        "requests_diagnosis_or_treatment": False,
        "extreme_weight_loss_goal": False,
        "requests_medication_supplement_or_therapeutic_diet": False,
    }
    return WeeklyPlanResult.model_validate(
        generate_weekly_plan(profile, safety_answers)
    )


def test_valid_ai_explanation_is_returned():
    client = FakeResponsesClient(
        output={
            "weekly_summary": "Three approachable sessions build consistency.",
            "day_explanations": [
                {
                    "day": "Monday",
                    "explanation": "This session develops full-body strength.",
                }
            ],
        }
    )

    explanation, used_fallback = generate_plan_explanation(
        fictional_plan(), client, "fictional-model"
    )

    assert explanation.weekly_summary.startswith("Three approachable")
    assert used_fallback is False
    assert client.received["text_format"].__name__ == "PlanExplanation"


def test_client_error_uses_deterministic_fallback():
    plan = fictional_plan()
    client = FakeResponsesClient(error=RuntimeError("service unavailable"))

    explanation, used_fallback = generate_plan_explanation(
        plan, client, "fictional-model"
    )

    assert explanation.weekly_summary == plan.weekly_summary
    assert used_fallback is True


def test_missing_parsed_output_uses_deterministic_fallback():
    plan = fictional_plan()
    client = FakeResponsesClient(output=None)

    explanation, used_fallback = generate_plan_explanation(
        plan, client, "fictional-model"
    )

    assert explanation.weekly_summary == plan.weekly_summary
    assert used_fallback is True


def test_invalid_ai_output_uses_deterministic_fallback():
    plan = fictional_plan()
    client = FakeResponsesClient(
        output={
            "weekly_summary": "",
            "day_explanations": [],
        }
    )

    explanation, used_fallback = generate_plan_explanation(
        plan, client, "fictional-model"
    )

    assert explanation.weekly_summary == plan.weekly_summary
    assert used_fallback is True
