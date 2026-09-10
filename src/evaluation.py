"""Local evaluation dataset loading, grading, and reporting helpers."""

import json
from collections.abc import Callable
from pathlib import Path

from src.models import FeedbackInterpretation, FeedbackInterpretationResponse


EVALUATED_FEEDBACK_FIELDS = (
    "difficulty",
    "missed_days",
    "disliked_exercises",
    "requested_focus",
    "requires_safety_rescreening",
)

ORDER_INDEPENDENT_FIELDS = {
    "missed_days",
    "disliked_exercises",
}


def grade_feedback_interpretation(
    expected: FeedbackInterpretation,
    actual: FeedbackInterpretation | None,
) -> dict:
    """Compare one actual interpretation with its expected answer."""
    field_results = {}

    for field_name in EVALUATED_FEEDBACK_FIELDS:
        if actual is None:
            field_results[field_name] = False
            continue

        expected_value = getattr(expected, field_name)
        actual_value = getattr(actual, field_name)

        if field_name in ORDER_INDEPENDENT_FIELDS:
            field_results[field_name] = set(actual_value) == set(expected_value)
        else:
            field_results[field_name] = actual_value == expected_value

    return {
        "passed": all(field_results.values()),
        "field_results": field_results,
    }


def load_feedback_cases(dataset_path: str | Path) -> list[dict]:
    """Load and validate fictional feedback cases from a JSONL file."""
    cases = []

    with Path(dataset_path).open(encoding="utf-8") as dataset_file:
        for line_number, line in enumerate(dataset_file, start=1):
            if not line.strip():
                continue

            raw_case = json.loads(line)
            case_id = raw_case.get("case_id")
            feedback = raw_case.get("feedback")
            if not isinstance(case_id, str) or not case_id.strip():
                raise ValueError(f"Line {line_number} has an invalid case_id.")
            if not isinstance(feedback, str) or not feedback.strip():
                raise ValueError(f"Line {line_number} has invalid feedback.")

            cases.append(
                {
                    "case_id": case_id,
                    "feedback": feedback,
                    "expected": FeedbackInterpretation.model_validate(
                        raw_case.get("expected")
                    ),
                }
            )

    if not cases:
        raise ValueError("The evaluation dataset is empty.")

    case_ids = [case["case_id"] for case in cases]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("Evaluation case IDs must be unique.")

    return cases


def evaluate_feedback_cases(
    cases: list[dict],
    interpreter: Callable[[str], FeedbackInterpretationResponse],
) -> list[dict]:
    """Interpret and grade every case in a loaded feedback dataset."""
    results = []

    for case in cases:
        response = interpreter(case["feedback"])
        grade = grade_feedback_interpretation(
            case["expected"], response.interpretation
        )
        results.append(
            {
                "case_id": case["case_id"],
                "feedback": case["feedback"],
                "expected": case["expected"].model_dump(mode="json"),
                "actual": (
                    response.interpretation.model_dump(mode="json")
                    if response.interpretation is not None
                    else None
                ),
                **grade,
            }
        )

    return results


def summarize_feedback_results(results: list[dict]) -> dict:
    """Calculate whole-case and per-field accuracy for evaluation results."""
    if not results:
        raise ValueError("Cannot summarize an empty result set.")

    total_cases = len(results)
    passed_cases = sum(result["passed"] for result in results)
    field_accuracy = {
        field_name: sum(
            result["field_results"][field_name] for result in results
        )
        / total_cases
        for field_name in EVALUATED_FEEDBACK_FIELDS
    }

    return {
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "case_accuracy": passed_cases / total_cases,
        "field_accuracy": field_accuracy,
        "failed_case_ids": [
            result["case_id"] for result in results if not result["passed"]
        ],
    }
