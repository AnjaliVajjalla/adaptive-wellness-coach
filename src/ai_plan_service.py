"""Application service for AI-assisted weekly-plan explanations."""

from collections.abc import Callable

from src.ai_service import (
    deterministic_plan_explanation,
    generate_plan_explanation,
)
from src.models import PlanExplanationResponse, WeeklyPlanResult
from src.openai_provider import (
    OpenAIConfigurationError,
    OpenAIProvider,
    create_openai_provider,
)


def explain_weekly_plan(
    plan: WeeklyPlanResult,
    provider_factory: Callable[[], OpenAIProvider] | None = None,
) -> PlanExplanationResponse:
    """Use OpenAI when configured, otherwise return the safe fallback."""
    factory = provider_factory or create_openai_provider
    try:
        provider = factory()
    except OpenAIConfigurationError:
        return PlanExplanationResponse(
            explanation=deterministic_plan_explanation(plan),
            used_fallback=True,
        )

    explanation, used_fallback = generate_plan_explanation(
        plan,
        provider.responses_client,
        provider.model,
    )
    return PlanExplanationResponse(
        explanation=explanation,
        used_fallback=used_fallback,
    )
