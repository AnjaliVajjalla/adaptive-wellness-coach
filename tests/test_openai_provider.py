"""Tests for OpenAI configuration without external API calls."""

from types import SimpleNamespace

import pytest

from src.openai_provider import (
    OpenAIConfigurationError,
    create_openai_provider,
)


class FakeOpenAIClientFactory:
    def __init__(self):
        self.received_api_key = None
        self.responses = object()

    def __call__(self, **kwargs):
        self.received_api_key = kwargs["api_key"]
        return SimpleNamespace(responses=self.responses)


def test_missing_settings_are_reported(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    with pytest.raises(OpenAIConfigurationError) as error:
        create_openai_provider(FakeOpenAIClientFactory())

    assert "OPENAI_API_KEY" in str(error.value)
    assert "OPENAI_MODEL" in str(error.value)


def test_missing_model_is_reported(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fictional-test-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    with pytest.raises(OpenAIConfigurationError, match="OPENAI_MODEL"):
        create_openai_provider(FakeOpenAIClientFactory())


def test_configured_provider_exposes_responses_client_and_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fictional-test-key")
    monkeypatch.setenv("OPENAI_MODEL", "fictional-model")
    factory = FakeOpenAIClientFactory()

    provider = create_openai_provider(factory)

    assert factory.received_api_key == "fictional-test-key"
    assert provider.responses_client is factory.responses
    assert provider.model == "fictional-model"
