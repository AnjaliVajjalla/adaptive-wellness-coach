"""Typed service boundary for weekly-plan generation."""

from src.models import PlanGenerationRequest, WeeklyPlanResult
from src.weekly_plan_generator import generate_weekly_plan


def create_weekly_plan(request: PlanGenerationRequest) -> WeeklyPlanResult:
    """Run the existing planner with validated input and output contracts."""
    result = generate_weekly_plan(
        request.profile.model_dump(),
        request.safety_answers.model_dump(),
        challenging_intensity_confirmed=(
            request.challenging_intensity_confirmed
        ),
    )
    return WeeklyPlanResult.model_validate(result)
