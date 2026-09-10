"""Structured, privacy-conscious observability for AI requests."""

import logging
import os
from collections.abc import Callable
from datetime import datetime, timezone
from math import ceil
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


LOGGER = logging.getLogger("adaptive_wellness_coach.ai")
LOGGER.setLevel(logging.INFO)
if not LOGGER.handlers:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(stream_handler)
LOGGER.propagate = False

AIRequestStatus = Literal["succeeded", "rejected", "fallback", "failed"]


class AIRequestTrace(BaseModel):
    """Operational metadata for one AI request without user-provided text."""

    model_config = ConfigDict(strict=True, extra="forbid")

    trace_id: str = Field(min_length=1)
    created_at: datetime
    operation: str = Field(min_length=1)
    model: str = Field(min_length=1)
    status: AIRequestStatus
    latency_ms: float = Field(ge=0)
    response_id: str | None
    input_tokens: int | None = Field(default=None, ge=0)
    cached_input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    estimated_cost_usd: float | None = Field(default=None, ge=0)


class TokenPricing(BaseModel):
    """Configurable text-token prices expressed in US dollars per 1M tokens."""

    model_config = ConfigDict(strict=True, extra="forbid")

    input_per_million_usd: float = Field(ge=0)
    cached_input_per_million_usd: float = Field(ge=0)
    output_per_million_usd: float = Field(ge=0)


class AIRequestMetrics(BaseModel):
    """Aggregate operational measurements across multiple AI traces."""

    model_config = ConfigDict(strict=True, extra="forbid")

    request_count: int = Field(ge=0)
    status_counts: dict[AIRequestStatus, int]
    success_rate: float = Field(ge=0, le=1)
    average_latency_ms: float | None = Field(default=None, ge=0)
    p95_latency_ms: float | None = Field(default=None, ge=0)
    total_tokens: int = Field(ge=0)
    priced_request_count: int = Field(ge=0)
    estimated_cost_usd: float | None = Field(default=None, ge=0)


TraceSink = Callable[[AIRequestTrace], None]


def load_token_pricing(model: str) -> TokenPricing | None:
    """Load pricing only when every setting exists and matches the model."""
    configured_model = os.environ.get("OPENAI_PRICING_MODEL", "").strip()
    setting_names = (
        "OPENAI_INPUT_COST_PER_1M_TOKENS",
        "OPENAI_CACHED_INPUT_COST_PER_1M_TOKENS",
        "OPENAI_OUTPUT_COST_PER_1M_TOKENS",
    )
    raw_values = [os.environ.get(name, "").strip() for name in setting_names]
    if configured_model != model or not all(raw_values):
        return None

    try:
        return TokenPricing(
            input_per_million_usd=float(raw_values[0]),
            cached_input_per_million_usd=float(raw_values[1]),
            output_per_million_usd=float(raw_values[2]),
        )
    except (TypeError, ValueError):
        return None


def estimate_token_cost_usd(
    input_tokens: int | None,
    cached_input_tokens: int | None,
    output_tokens: int | None,
    pricing: TokenPricing | None,
) -> float | None:
    """Estimate request cost from token counts and configurable pricing."""
    if input_tokens is None or output_tokens is None or pricing is None:
        return None

    cached_tokens = cached_input_tokens or 0
    if cached_tokens > input_tokens:
        return None
    uncached_tokens = input_tokens - cached_tokens
    return (
        uncached_tokens * pricing.input_per_million_usd
        + cached_tokens * pricing.cached_input_per_million_usd
        + output_tokens * pricing.output_per_million_usd
    ) / 1_000_000


def summarize_ai_request_traces(
    traces: list[AIRequestTrace],
) -> AIRequestMetrics:
    """Summarize reliability, latency, token usage, and estimated cost."""
    status_counts: dict[AIRequestStatus, int] = {
        "succeeded": 0,
        "rejected": 0,
        "fallback": 0,
        "failed": 0,
    }
    for trace in traces:
        status_counts[trace.status] += 1

    request_count = len(traces)
    latencies = sorted(trace.latency_ms for trace in traces)
    priced_costs = [
        trace.estimated_cost_usd
        for trace in traces
        if trace.estimated_cost_usd is not None
    ]
    return AIRequestMetrics(
        request_count=request_count,
        status_counts=status_counts,
        success_rate=(
            status_counts["succeeded"] / request_count
            if request_count
            else 0.0
        ),
        average_latency_ms=(
            sum(latencies) / request_count if request_count else None
        ),
        p95_latency_ms=(
            latencies[ceil(0.95 * request_count) - 1]
            if request_count
            else None
        ),
        total_tokens=sum(trace.total_tokens or 0 for trace in traces),
        priced_request_count=len(priced_costs),
        estimated_cost_usd=(sum(priced_costs) if priced_costs else None),
    )


def build_ai_request_trace(
    operation: str,
    model: str,
    status: AIRequestStatus,
    latency_ms: float,
    response=None,
    pricing: TokenPricing | None = None,
) -> AIRequestTrace:
    """Build a trace from safe local metadata and an optional AI response."""
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None)
    input_details = getattr(usage, "input_tokens_details", None)
    cached_input_tokens = getattr(input_details, "cached_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)
    configured_pricing = pricing or load_token_pricing(model)
    return AIRequestTrace(
        trace_id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        operation=operation,
        model=model,
        status=status,
        latency_ms=latency_ms,
        response_id=getattr(response, "id", None),
        input_tokens=input_tokens,
        cached_input_tokens=cached_input_tokens,
        output_tokens=output_tokens,
        total_tokens=getattr(usage, "total_tokens", None),
        estimated_cost_usd=estimate_token_cost_usd(
            input_tokens,
            cached_input_tokens,
            output_tokens,
            configured_pricing,
        ),
    )


def emit_ai_request_trace(trace: AIRequestTrace) -> None:
    """Write one structured trace to the application log."""
    LOGGER.info(trace.model_dump_json())
