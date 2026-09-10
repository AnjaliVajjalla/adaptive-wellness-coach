"""Tests for schema-constrained AI feature outputs."""

import pytest
from pydantic import ValidationError

from src.models import FeedbackInterpretation, PlanExplanation


def test_valid_plan_explanation_matches_contract():
    explanation = PlanExplanation.model_validate(
        {
            "weekly_summary": "Three balanced sessions support consistency.",
            "day_explanations": [
                {
                    "day": "Monday",
                    "explanation": "This session develops full-body strength.",
                },
                {
                    "day": "Wednesday",
                    "explanation": "This session reinforces the same movements.",
                },
            ],
        }
    )

    assert explanation.day_explanations[0].day == "Monday"


def test_plan_explanation_rejects_duplicate_days():
    with pytest.raises(ValidationError):
        PlanExplanation.model_validate(
            {
                "weekly_summary": "A fictional weekly summary.",
                "day_explanations": [
                    {"day": "Monday", "explanation": "First explanation."},
                    {"day": "Monday", "explanation": "Duplicate explanation."},
                ],
            }
        )


def test_valid_feedback_interpretation_matches_contract():
    interpretation = FeedbackInterpretation.model_validate(
        {
            "difficulty": "too_hard",
            "missed_days": ["Wednesday"],
            "disliked_exercises": ["wall_push_up"],
            "requested_focus": None,
            "requires_safety_rescreening": False,
        }
    )

    assert interpretation.difficulty == "too_hard"
    assert interpretation.missed_days == ["Wednesday"]


def test_feedback_rejects_unsupported_difficulty():
    with pytest.raises(ValidationError):
        FeedbackInterpretation.model_validate(
            {
                "difficulty": "extremely_difficult",
                "missed_days": [],
                "disliked_exercises": [],
                "requested_focus": None,
                "requires_safety_rescreening": False,
            }
        )


def test_feedback_requires_strict_boolean_safety_signal():
    with pytest.raises(ValidationError):
        FeedbackInterpretation.model_validate(
            {
                "difficulty": "not_stated",
                "missed_days": [],
                "disliked_exercises": [],
                "requested_focus": None,
                "requires_safety_rescreening": "false",
            }
        )


def test_feedback_rejects_duplicate_missed_days():
    with pytest.raises(ValidationError):
        FeedbackInterpretation.model_validate(
            {
                "difficulty": "appropriate",
                "missed_days": ["Friday", "Friday"],
                "disliked_exercises": [],
                "requested_focus": "mobility",
                "requires_safety_rescreening": False,
            }
        )


def test_feedback_rejects_blank_exercise_identifier():
    with pytest.raises(ValidationError):
        FeedbackInterpretation.model_validate(
            {
                "difficulty": "not_stated",
                "missed_days": [],
                "disliked_exercises": [" "],
                "requested_focus": None,
                "requires_safety_rescreening": False,
            }
        )
