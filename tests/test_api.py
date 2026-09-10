"""Integration tests for the FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


@pytest.fixture
def valid_plan_request():
    return {
        "profile": {
            "profile_id": "fictional_api_001",
            "primary_goal": "Get stronger",
            "additional_goals": [],
            "experience_level": "Complete beginner",
            "current_activity_level": "Light",
            "available_workout_days": [
                "Monday",
                "Wednesday",
                "Friday",
            ],
            "session_duration": 30,
            "available_equipment": ["No equipment, bodyweight only"],
            "preferred_activities": ["Bodyweight workouts"],
            "disliked_activities": ["Jogging or running"],
            "preferred_intensity": "Moderate",
        },
        "safety_answers": {
            "pregnant_or_postpartum": False,
            "current_injury_or_rehabilitation": False,
            "eating_disorder_concern": False,
            "complex_or_uncontrolled_medical_condition": False,
            "requests_diagnosis_or_treatment": False,
            "extreme_weight_loss_goal": False,
            "requests_medication_supplement_or_therapeutic_diet": False,
        },
        "challenging_intensity_confirmed": False,
    }


def test_health_endpoint_reports_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_plan_endpoint_returns_structured_generated_plan(valid_plan_request):
    response = client.post("/plans", json=valid_plan_request)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "generated"
    assert len(body["days"]) == 7
    assert body["totals"]["workout_days"] == 3


def test_plan_endpoint_rejects_missing_required_field(valid_plan_request):
    del valid_plan_request["profile"]["session_duration"]

    response = client.post("/plans", json=valid_plan_request)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == [
        "body",
        "profile",
        "session_duration",
    ]


def test_plan_endpoint_rejects_wrong_field_type(valid_plan_request):
    valid_plan_request["profile"]["session_duration"] = "30"

    response = client.post("/plans", json=valid_plan_request)

    assert response.status_code == 422


def test_plan_endpoint_returns_blocked_safety_result(valid_plan_request):
    valid_plan_request["safety_answers"][
        "current_injury_or_rehabilitation"
    ] = True

    response = client.post("/plans", json=valid_plan_request)

    assert response.status_code == 200
    assert response.json()["status"] == "blocked"
    assert response.json()["days"] == []


def test_explanation_endpoint_returns_fallback_without_configuration(
    valid_plan_request,
    monkeypatch,
):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    plan_response = client.post("/plans", json=valid_plan_request)

    response = client.post(
        "/ai/plan-explanations",
        json={"plan": plan_response.json()},
    )

    assert response.status_code == 200
    assert response.json()["used_fallback"] is True
    assert response.json()["explanation"]["weekly_summary"]


def test_explanation_endpoint_rejects_blocked_plan(valid_plan_request):
    valid_plan_request["safety_answers"][
        "current_injury_or_rehabilitation"
    ] = True
    plan_response = client.post("/plans", json=valid_plan_request)

    response = client.post(
        "/ai/plan-explanations",
        json={"plan": plan_response.json()},
    )

    assert response.status_code == 422


def test_openapi_schema_documents_all_endpoints():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/health" in response.json()["paths"]
    assert "/plans" in response.json()["paths"]
    assert "/ai/plan-explanations" in response.json()["paths"]
