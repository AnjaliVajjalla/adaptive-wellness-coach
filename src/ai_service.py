"""AI-assisted features with deterministic fallback behavior."""

import json
from typing import Protocol

from src.models import (
    FeedbackInterpretation,
    PlanExplanation,
    WeeklyPlanResult,
)


PLAN_EXPLANATION_INSTRUCTIONS = """
Explain the supplied weekly workout plan in concise, supportive language.
Return one short weekly summary and one sentence for each workout or recovery
day. Do not add or remove exercises, change scheduling, prescriptions, totals,
or safety decisions, and do not provide medical advice.
""".strip()

FEEDBACK_INTERPRETATION_INSTRUCTIONS = """
Extract structured signals from workout feedback. Do not modify a workout
plan, invent exercise identifiers, provide medical advice, or make a safety
decision. Use requires_safety_rescreening=true when the feedback may describe
a new injury, pregnancy or postpartum situation, eating-disorder concern,
complex medical condition, request for diagnosis or treatment, extreme weight
loss goal, or medication, supplement, or therapeutic-diet request.
""".strip()


class StructuredResponsesClient(Protocol):
    """Small interface shared by the OpenAI client and test doubles."""

    def parse(self, **kwargs):
        """Return a response containing a parsed structured output."""


def deterministic_plan_explanation(
    plan: WeeklyPlanResult,
) -> PlanExplanation:
    """Build an explanation from already-validated planner text."""
    return PlanExplanation(
        weekly_summary=plan.weekly_summary,
        day_explanations=[
            {
                "day": day.day,
                "explanation": day.explanation,
            }
            for day in plan.days
            if day.day_type != "rest"
        ],
    )


def generate_plan_explanation(
    plan: WeeklyPlanResult,
    responses_client: StructuredResponsesClient,
    model: str,
) -> tuple[PlanExplanation, bool]:
    """Return an AI explanation, or the deterministic fallback on failure."""
    try:
        response = responses_client.parse(
            model=model,
            instructions=PLAN_EXPLANATION_INSTRUCTIONS,
            input=json.dumps(plan.model_dump(mode="json")),
            text_format=PlanExplanation,
        )
        if response.output_parsed is None:
            raise ValueError("The AI response did not contain parsed output.")
        explanation = PlanExplanation.model_validate(response.output_parsed)
    except Exception:
        return deterministic_plan_explanation(plan), True

    return explanation, False


def interpret_feedback(
    feedback: str,
    known_exercise_ids: list[str],
    responses_client: StructuredResponsesClient,
    model: str,
) -> FeedbackInterpretation | None:
    """Return validated feedback signals, or None when interpretation fails."""
    if not feedback.strip():
        raise ValueError("Feedback cannot be blank.")

    try:
        response = responses_client.parse(
            model=model,
            instructions=FEEDBACK_INTERPRETATION_INSTRUCTIONS,
            input=json.dumps(
                {
                    "feedback": feedback,
                    "known_exercise_ids": known_exercise_ids,
                }
            ),
            text_format=FeedbackInterpretation,
        )
        if response.output_parsed is None:
            raise ValueError("The AI response did not contain parsed output.")
        interpretation = FeedbackInterpretation.model_validate(
            response.output_parsed
        )
        unknown_exercises = set(interpretation.disliked_exercises) - set(
            known_exercise_ids
        )
        if unknown_exercises:
            raise ValueError("AI returned an unknown exercise identifier.")
    except Exception:
        return None

    return interpretation
