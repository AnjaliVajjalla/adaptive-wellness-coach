"""Tests for AI-assisted behavior without external API calls."""

from types import SimpleNamespace

import pytest

from src.ai_service import generate_plan_explanation, interpret_feedback
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


def test_valid_ai_explanation_is_returned():
    client = FakeResponsesClient(
        output={
            "weekly_summary": "Three approachable sessions build consistency.",
            "day_explanations": [
                {
                    "day": "Monday",
                    "explanation": "This session develops full-body strength.",
                },
                {
                    "day": "Wednesday",
                    "explanation": "This session repeats core movements.",
                },
                {
                    "day": "Friday",
                    "explanation": "This session develops stamina.",
                },
            ],
        }
    )

    explanation, used_fallback = generate_plan_explanation(
        fictional_plan(), client, "fictional-model"
    )

    assert explanation.weekly_summary.startswith("Three approachable")
    assert used_fallback is False
    assert client.received["text_format"].__name__ == "PlanExplanation"


def test_explanation_for_rest_day_uses_deterministic_fallback():
    plan = fictional_plan()
    client = FakeResponsesClient(
        output={
            "weekly_summary": "Three sessions support steady progress.",
            "day_explanations": [
                {"day": "Monday", "explanation": "Strength session."},
                {"day": "Tuesday", "explanation": "Rest day."},
                {"day": "Wednesday", "explanation": "Strength session."},
                {"day": "Friday", "explanation": "Cardio session."},
            ],
        }
    )

    explanation, used_fallback = generate_plan_explanation(
        plan, client, "fictional-model"
    )

    assert used_fallback is True
    assert explanation.weekly_summary == plan.weekly_summary


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


def test_valid_feedback_interpretation_is_returned():
    client = FakeResponsesClient(
        output={
            "difficulty": "too_hard",
            "missed_days": ["Wednesday"],
            "disliked_exercises": ["wall_push_up"],
            "requested_focus": None,
            "requires_safety_rescreening": False,
        }
    )

    interpretation = interpret_feedback(
        "Wednesday was too hard and I disliked wall push-ups.",
        ["wall_push_up", "sit_to_stand"],
        client,
        "fictional-model",
    )

    assert interpretation is not None
    assert interpretation.difficulty == "too_hard"
    assert interpretation.disliked_exercises == ["wall_push_up"]
    assert client.received["text_format"].__name__ == "FeedbackInterpretation"


def test_feedback_client_error_makes_no_adjustment():
    client = FakeResponsesClient(error=RuntimeError("service unavailable"))

    interpretation = interpret_feedback(
        "The workout felt difficult.",
        ["wall_push_up"],
        client,
        "fictional-model",
    )

    assert interpretation is None


def test_unknown_exercise_identifier_makes_no_adjustment():
    client = FakeResponsesClient(
        output={
            "difficulty": "not_stated",
            "missed_days": [],
            "disliked_exercises": ["invented_exercise"],
            "requested_focus": None,
            "requires_safety_rescreening": False,
        }
    )

    interpretation = interpret_feedback(
        "I disliked an exercise.",
        ["wall_push_up"],
        client,
        "fictional-model",
    )

    assert interpretation is None


def test_possible_new_injury_is_flagged_for_rescreening():
    client = FakeResponsesClient(
        output={
            "difficulty": "not_stated",
            "missed_days": [],
            "disliked_exercises": [],
            "requested_focus": None,
            "requires_safety_rescreening": True,
        }
    )

    interpretation = interpret_feedback(
        "I developed a new injury.",
        ["wall_push_up"],
        client,
        "fictional-model",
    )

    assert interpretation is not None
    assert interpretation.requires_safety_rescreening is True


def test_invalid_feedback_output_makes_no_adjustment():
    client = FakeResponsesClient(
        output={
            "difficulty": "extremely_difficult",
            "missed_days": [],
            "disliked_exercises": [],
            "requested_focus": None,
            "requires_safety_rescreening": False,
        }
    )

    interpretation = interpret_feedback(
        "The workout was extremely difficult.",
        ["wall_push_up"],
        client,
        "fictional-model",
    )

    assert interpretation is None


def test_blank_feedback_is_rejected_before_ai_call():
    client = FakeResponsesClient(output=None)

    with pytest.raises(ValueError, match="Feedback cannot be blank"):
        interpret_feedback("   ", [], client, "fictional-model")

    assert client.received is None
