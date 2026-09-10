"""FastAPI application for the Adaptive Wellness Coach."""

from fastapi import FastAPI

from src.models import HealthResponse, PlanGenerationRequest, WeeklyPlanResult
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
