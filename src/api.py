"""FastAPI application for the Adaptive Wellness Coach."""

from fastapi import FastAPI

from src.ai_feedback_service import interpret_workout_feedback
from src.ai_plan_service import explain_weekly_plan
from src.models import (
    FeedbackInterpretationRequest,
    FeedbackInterpretationResponse,
    HealthResponse,
    PlanExplanationRequest,
    PlanExplanationResponse,
    PlanGenerationRequest,
    WeeklyPlanResult,
)
from src.plan_service import create_weekly_plan


app = FastAPI(
    title="Adaptive Wellness Coach API",
    version="0.2.0",
    description=(
        "Generate deterministic weekly workout plans and provide "
        "validated AI-assisted explanations and feedback interpretation."
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


@app.post(
    "/ai/feedback-interpretations",
    response_model=FeedbackInterpretationResponse,
)
def interpret_user_feedback(
    request: FeedbackInterpretationRequest,
) -> FeedbackInterpretationResponse:
    """Convert free-text feedback into validated structured signals."""
    return interpret_workout_feedback(request.feedback)
