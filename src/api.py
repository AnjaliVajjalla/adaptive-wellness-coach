"""FastAPI application for the Adaptive Wellness Coach."""

from fastapi import FastAPI

from src.ai_plan_service import explain_weekly_plan
from src.models import (
    HealthResponse,
    PlanExplanationRequest,
    PlanExplanationResponse,
    PlanGenerationRequest,
    WeeklyPlanResult,
)
from src.plan_service import create_weekly_plan


app = FastAPI(
    title="Adaptive Wellness Coach API",
    version="0.1.0",
    description=(
        "Generate deterministic weekly workout plans from validated "
        "fictional profiles."
    ),
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Report whether the API process is responding."""
    return HealthResponse(status="healthy")


@app.post("/plans", response_model=WeeklyPlanResult)
def generate_plan(request: PlanGenerationRequest) -> WeeklyPlanResult:
    """Validate input and return a generated, blocked, or warning result."""
    return create_weekly_plan(request)


@app.post(
    "/ai/plan-explanations",
    response_model=PlanExplanationResponse,
)
def explain_plan(
    request: PlanExplanationRequest,
) -> PlanExplanationResponse:
    """Explain a generated plan without allowing AI to modify it."""
    return explain_weekly_plan(request.plan)
