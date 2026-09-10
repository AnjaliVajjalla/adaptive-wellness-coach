"""Run the feedback evaluation dataset and print a JSON report."""

import json
from pathlib import Path

from src.ai_feedback_service import interpret_workout_feedback
from src.evaluation import (
    evaluate_feedback_cases,
    load_feedback_cases,
    summarize_feedback_results,
)


DEFAULT_DATASET_PATH = Path("evals/feedback_cases.jsonl")


def run_feedback_evaluation(
    dataset_path: str | Path = DEFAULT_DATASET_PATH,
) -> dict:
    """Run all feedback cases with the configured AI provider."""
    cases = load_feedback_cases(dataset_path)
    results = evaluate_feedback_cases(cases, interpret_workout_feedback)
    return {
        "summary": summarize_feedback_results(results),
        "results": results,
    }


def main() -> None:
    """Print the complete evaluation report for command-line use."""
    report = run_feedback_evaluation()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
