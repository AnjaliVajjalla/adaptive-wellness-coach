"""Tests for local AI evaluation loading, grading, and reporting."""

from pathlib import Path

from src.evaluation import (
    evaluate_feedback_cases,
    grade_feedback_interpretation,
    load_feedback_cases,
    summarize_feedback_results,
)
from src.models import FeedbackInterpretation, FeedbackInterpretationResponse


def feedback_interpretation(**overrides):
    """Build a valid interpretation with optional field changes."""
    values = {
        "difficulty": "not_stated",
        "missed_days": [],
        "disliked_exercises": [],
        "requested_focus": None,
        "requires_safety_rescreening": False,
    }
    values.update(overrides)
    return FeedbackInterpretation.model_validate(values)


def test_grader_passes_when_every_field_matches():
    expected = feedback_interpretation(
        difficulty="too_hard",
        missed_days=["Tuesday", "Saturday"],
        disliked_exercises=["wall_push_up"],
    )

    result = grade_feedback_interpretation(expected, expected)

    assert result["passed"] is True
    assert all(result["field_results"].values())


def test_grader_ignores_list_order():
    expected = feedback_interpretation(
        missed_days=["Tuesday", "Saturday"],
        disliked_exercises=["wall_push_up", "lat_pulldown"],
    )
    actual = feedback_interpretation(
        missed_days=["Saturday", "Tuesday"],
        disliked_exercises=["lat_pulldown", "wall_push_up"],
    )

    result = grade_feedback_interpretation(expected, actual)

    assert result["passed"] is True


def test_grader_fails_whole_case_when_one_field_is_wrong():
    expected = feedback_interpretation(difficulty="too_hard")
    actual = feedback_interpretation(difficulty="appropriate")

    result = grade_feedback_interpretation(expected, actual)

    assert result["passed"] is False
    assert result["field_results"]["difficulty"] is False
    assert result["field_results"]["missed_days"] is True


def test_grader_fails_every_field_when_interpretation_is_missing():
    expected = feedback_interpretation()

    result = grade_feedback_interpretation(expected, None)

    assert result["passed"] is False
    assert not any(result["field_results"].values())


def test_fictional_feedback_dataset_is_valid():
    dataset_path = Path("evals/feedback_cases.jsonl")

    cases = load_feedback_cases(dataset_path)

    assert len(cases) == 20
    assert len({case["case_id"] for case in cases}) == 20


def test_runner_and_summary_report_a_perfect_fake_run():
    expected = feedback_interpretation(
        difficulty="too_easy",
        requested_focus="strength",
    )
    cases = [
        {
            "case_id": "perfect_case",
            "feedback": "The workout was easy. Add more strength work.",
            "expected": expected,
        }
    ]

    def fake_interpreter(_feedback):
        return FeedbackInterpretationResponse(
            interpretation=expected,
            interpretation_succeeded=True,
        )

    results = evaluate_feedback_cases(cases, fake_interpreter)
    summary = summarize_feedback_results(results)

    assert summary["case_accuracy"] == 1.0
    assert all(accuracy == 1.0 for accuracy in summary["field_accuracy"].values())
    assert summary["failed_case_ids"] == []
