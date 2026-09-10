"""Tests for the application-level feedback interpretation service."""

from types import SimpleNamespace

from src.ai_feedback_service import interpret_workout_feedback
from src.openai_provider import OpenAIConfigurationError, OpenAIProvider


class FakeResponsesClient:
    def __init__(self, output):
        self.output = output

    def parse(self, **kwargs):
        return SimpleNamespace(output_parsed=self.output)


def test_configured_provider_returns_validated_feedback_signals():
    client = FakeResponsesClient(
        {
            "difficulty": "too_hard",
            "missed_days": ["Wednesday"],
            "disliked_exercises": ["wall_push_up"],
            "requested_focus": None,
            "requires_safety_rescreening": False,
        }
    )

    result = interpret_workout_feedback(
        "Wednesday was too difficult and I disliked wall push-ups.",
        lambda: OpenAIProvider(client, "fictional-model"),
    )

    assert result.interpretation_succeeded is True
    assert result.interpretation.difficulty == "too_hard"
    assert result.interpretation.disliked_exercises == ["wall_push_up"]


def test_missing_configuration_returns_no_interpretation():
    def missing_provider():
        raise OpenAIConfigurationError("Missing settings")

    result = interpret_workout_feedback(
        "The session was too difficult.",
        missing_provider,
    )

    assert result.interpretation_succeeded is False
    assert result.interpretation is None
