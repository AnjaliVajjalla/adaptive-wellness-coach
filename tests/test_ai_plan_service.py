"""Tests for the application-level plan explanation service."""

from types import SimpleNamespace

from src.ai_plan_service import explain_weekly_plan
from src.models import WeeklyPlanResult
from src.openai_provider import OpenAIConfigurationError, OpenAIProvider
from src.weekly_plan_generator import generate_weekly_plan


class FakeResponsesClient:
    def __init__(self, output):
        self.output = output

    def parse(self, **kwargs):
        return SimpleNamespace(output_parsed=self.output)


def fictional_plan():
    profile = {
        "profile_id": "fictional_ai_plan_service_001",
        "primary_goal": "Get stronger",
        "additional_goals": [],
        "experience_level": "Complete beginner",
        "current_activity_level": "Light",
        "available_workout_days": ["Monday", "Wednesday", "Friday"],
        "session_duration": 30,
        "workout_split_preference": "Let the coach choose",
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


def test_configured_provider_returns_validated_ai_explanation():
    client = FakeResponsesClient(
        {
            "weekly_summary": "Three sessions support steady progress.",
            "day_explanations": [
                {
                    "day": "Monday",
                    "explanation": "This day develops full-body strength.",
                },
                {
                    "day": "Wednesday",
                    "explanation": "This day repeats core movements.",
                },
                {
                    "day": "Friday",
                    "explanation": "This day develops stamina.",
                },
            ],
        }
    )

    result = explain_weekly_plan(
        fictional_plan(),
        lambda: OpenAIProvider(client, "fictional-model"),
    )

    assert result.used_fallback is False
    assert result.explanation.weekly_summary.startswith("Three sessions")


def test_missing_configuration_returns_deterministic_fallback():
    plan = fictional_plan()

    def missing_provider():
        raise OpenAIConfigurationError("Missing settings")

    result = explain_weekly_plan(plan, missing_provider)

    assert result.used_fallback is True
    assert result.explanation.weekly_summary == plan.weekly_summary
