"""Tests for structured AI request traces."""

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src.ai_service import interpret_feedback
from src.observability import (
    AIRequestTrace,
    TokenPricing,
    build_ai_request_trace,
    estimate_token_cost_usd,
    summarize_ai_request_traces,
)


class ObservableFakeClient:
    def __init__(self, output=None, error=None):
        self.output = output
        self.error = error

    def parse(self, **_kwargs):
        if self.error is not None:
            raise self.error
        return SimpleNamespace(
            id="resp_fictional_123",
            output_parsed=self.output,
            usage=SimpleNamespace(
                input_tokens=100,
                input_tokens_details=SimpleNamespace(cached_tokens=20),
                output_tokens=25,
                total_tokens=125,
            ),
        )


def test_trace_reads_response_id_and_token_usage():
    response = ObservableFakeClient(output={}).parse()

    trace = build_ai_request_trace(
        operation="feedback_interpretation",
        model="fictional-model",
        status="succeeded",
        latency_ms=125.0,
        response=response,
    )

    assert trace.response_id == "resp_fictional_123"
    assert trace.input_tokens == 100
    assert trace.cached_input_tokens == 20
    assert trace.output_tokens == 25
    assert trace.total_tokens == 125


def test_cost_estimate_prices_cached_input_separately():
    pricing = TokenPricing(
        input_per_million_usd=0.25,
        cached_input_per_million_usd=0.025,
        output_per_million_usd=2.00,
    )

    cost = estimate_token_cost_usd(
        input_tokens=100,
        cached_input_tokens=20,
        output_tokens=25,
        pricing=pricing,
    )

    assert cost == pytest.approx(0.0000705)


def test_trace_loads_matching_pricing_from_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_PRICING_MODEL", "fictional-model")
    monkeypatch.setenv("OPENAI_INPUT_COST_PER_1M_TOKENS", "0.25")
    monkeypatch.setenv("OPENAI_CACHED_INPUT_COST_PER_1M_TOKENS", "0.025")
    monkeypatch.setenv("OPENAI_OUTPUT_COST_PER_1M_TOKENS", "2.00")

    response = ObservableFakeClient(output={}).parse()
    trace = build_ai_request_trace(
        operation="feedback_interpretation",
        model="fictional-model",
        status="succeeded",
        latency_ms=125.0,
        response=response,
    )

    assert trace.estimated_cost_usd == pytest.approx(0.0000705)


def test_trace_omits_cost_when_pricing_model_does_not_match(monkeypatch):
    monkeypatch.setenv("OPENAI_PRICING_MODEL", "different-model")
    monkeypatch.setenv("OPENAI_INPUT_COST_PER_1M_TOKENS", "0.25")
    monkeypatch.setenv("OPENAI_CACHED_INPUT_COST_PER_1M_TOKENS", "0.025")
    monkeypatch.setenv("OPENAI_OUTPUT_COST_PER_1M_TOKENS", "2.00")

    response = ObservableFakeClient(output={}).parse()
    trace = build_ai_request_trace(
        operation="feedback_interpretation",
        model="fictional-model",
        status="succeeded",
        latency_ms=125.0,
        response=response,
    )

    assert trace.estimated_cost_usd is None


def test_metrics_summarize_reliability_latency_tokens_and_cost():
    traces = [
        AIRequestTrace(
            trace_id=f"trace-{index}",
            created_at=datetime(2026, 9, 10, 12, 0, tzinfo=timezone.utc),
            operation="feedback_interpretation",
            model="fictional-model",
            status=status,
            latency_ms=latency,
            response_id=f"response-{index}",
            input_tokens=100,
            cached_input_tokens=0,
            output_tokens=25,
            total_tokens=125,
            estimated_cost_usd=0.000075,
        )
        for index, (status, latency) in enumerate(
            [
                ("succeeded", 100.0),
                ("succeeded", 200.0),
                ("fallback", 300.0),
                ("failed", 2000.0),
            ]
        )
    ]

    metrics = summarize_ai_request_traces(traces)

    assert metrics.request_count == 4
    assert metrics.status_counts == {
        "succeeded": 2,
        "rejected": 0,
        "fallback": 1,
        "failed": 1,
    }
    assert metrics.success_rate == pytest.approx(0.5)
    assert metrics.average_latency_ms == pytest.approx(650.0)
    assert metrics.p95_latency_ms == pytest.approx(2000.0)
    assert metrics.total_tokens == 500
    assert metrics.priced_request_count == 4
    assert metrics.estimated_cost_usd == pytest.approx(0.0003)


def test_empty_metrics_do_not_invent_latency_or_cost():
    metrics = summarize_ai_request_traces([])

    assert metrics.request_count == 0
    assert metrics.success_rate == 0.0
    assert metrics.average_latency_ms is None
    assert metrics.p95_latency_ms is None
    assert metrics.estimated_cost_usd is None


def test_feedback_trace_records_latency_without_feedback_text():
    feedback = "Wednesday was too difficult."
    client = ObservableFakeClient(
        output={
            "difficulty": "too_hard",
            "missed_days": [],
            "disliked_exercises": [],
            "requested_focus": None,
            "requires_safety_rescreening": False,
        }
    )
    traces = []
    times = iter([10.0, 10.125])

    interpretation = interpret_feedback(
        feedback,
        ["wall_push_up"],
        client,
        "fictional-model",
        trace_sink=traces.append,
        clock=lambda: next(times),
    )

    assert interpretation is not None
    assert len(traces) == 1
    assert traces[0].status == "succeeded"
    assert traces[0].latency_ms == pytest.approx(125.0)
    assert feedback not in traces[0].model_dump_json()


def test_failed_request_trace_has_no_response_or_usage():
    client = ObservableFakeClient(error=RuntimeError("service unavailable"))
    traces = []
    times = iter([20.0, 20.25])

    interpretation = interpret_feedback(
        "The workout felt difficult.",
        ["wall_push_up"],
        client,
        "fictional-model",
        trace_sink=traces.append,
        clock=lambda: next(times),
    )

    assert interpretation is None
    assert traces[0].status == "failed"
    assert traces[0].response_id is None
    assert traces[0].total_tokens is None
