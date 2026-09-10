"""Create the configured OpenAI client used by AI-assisted features."""

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from src.ai_service import StructuredResponsesClient


class OpenAIConfigurationError(RuntimeError):
    """Raised when required OpenAI settings are unavailable."""


@dataclass(frozen=True)
class OpenAIProvider:
    """Configured Responses API client and the selected model name."""

    responses_client: StructuredResponsesClient
    model: str


def create_openai_provider(
    client_factory: Callable[..., Any] | None = None,
) -> OpenAIProvider:
    """Read local settings and create an OpenAI Responses API provider."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    model = os.environ.get("OPENAI_MODEL", "").strip()

    missing_settings = [
        name
        for name, value in (
            ("OPENAI_API_KEY", api_key),
            ("OPENAI_MODEL", model),
        )
        if not value
    ]
    if missing_settings:
        raise OpenAIConfigurationError(
            "Missing required OpenAI setting(s): "
            + ", ".join(missing_settings)
        )

    factory = client_factory or OpenAI
    client = factory(api_key=api_key)
    return OpenAIProvider(
        responses_client=client.responses,
        model=model,
    )
