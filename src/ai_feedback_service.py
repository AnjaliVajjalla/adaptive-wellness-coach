"""Application service for structured workout-feedback interpretation."""

from collections.abc import Callable

from src.ai_service import interpret_feedback
from src.exercise_library import EXERCISE_LIBRARY
from src.models import FeedbackInterpretationResponse
from src.observability import TraceSink, emit_ai_request_trace
from src.openai_provider import (
    OpenAIConfigurationError,
    OpenAIProvider,
    create_openai_provider,
)


KNOWN_EXERCISE_IDS = [
    exercise["exercise_id"] for exercise in EXERCISE_LIBRARY
]


def interpret_workout_feedback(
    feedback: str,
    provider_factory: Callable[[], OpenAIProvider] | None = None,
    trace_sink: TraceSink = emit_ai_request_trace,
) -> FeedbackInterpretationResponse:
    """Return validated signals, or no interpretation on AI failure."""
    factory = provider_factory or create_openai_provider
    try:
        provider = factory()
    except OpenAIConfigurationError:
        return FeedbackInterpretationResponse(
            interpretation=None,
            interpretation_succeeded=False,
        )

    interpretation = interpret_feedback(
        feedback,
        KNOWN_EXERCISE_IDS,
        provider.responses_client,
        provider.model,
        trace_sink=trace_sink,
    )
    return FeedbackInterpretationResponse(
        interpretation=interpretation,
        interpretation_succeeded=interpretation is not None,
    )
