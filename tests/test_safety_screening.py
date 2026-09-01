"""Automated tests for deterministic safety screening."""

import pytest

from src.safety_screening import REQUIRED_SAFETY_FIELDS, screen_safety


@pytest.fixture
def safe_safety_answers():
    return {field: False for field in REQUIRED_SAFETY_FIELDS}


def test_complete_safe_answers_pass(safe_safety_answers):
    result = screen_safety(safe_safety_answers)

    assert result["status"] == "safe"
    assert result["reasons"] == []
    assert "may continue" in result["message"]


@pytest.mark.parametrize("triggered_field", REQUIRED_SAFETY_FIELDS)
def test_each_exclusion_returns_unsafe(
    safe_safety_answers,
    triggered_field,
):
    safe_safety_answers[triggered_field] = True

    result = screen_safety(safe_safety_answers)

    assert result["status"] == "unsafe"
    assert result["reasons"] == [triggered_field]
    assert "will not be generated" in result["message"]
    assert "qualified professional" in result["message"]


def test_multiple_exclusions_are_reported(safe_safety_answers):
    triggered_fields = [
        "current_injury_or_rehabilitation",
        "complex_or_uncontrolled_medical_condition",
    ]
    for field in triggered_fields:
        safe_safety_answers[field] = True

    result = screen_safety(safe_safety_answers)

    assert result["status"] == "unsafe"
    assert result["reasons"] == triggered_fields


@pytest.mark.parametrize("missing_field", REQUIRED_SAFETY_FIELDS)
def test_each_missing_answer_returns_incomplete(
    safe_safety_answers,
    missing_field,
):
    safe_safety_answers.pop(missing_field)

    result = screen_safety(safe_safety_answers)

    assert result["status"] == "incomplete"
    assert result["reasons"] == [missing_field]
    assert missing_field.replace("_", " ") in result["message"]


@pytest.mark.parametrize(
    "invalid_value",
    [None, "false", 0, 1, [], {}],
)
def test_non_boolean_answer_returns_incomplete(
    safe_safety_answers,
    invalid_value,
):
    field = "pregnant_or_postpartum"
    safe_safety_answers[field] = invalid_value

    result = screen_safety(safe_safety_answers)

    assert result["status"] == "incomplete"
    assert result["reasons"] == [field]


@pytest.mark.parametrize("malformed_answers", [None, [], "answers"])
def test_malformed_answers_return_incomplete(malformed_answers):
    result = screen_safety(malformed_answers)

    assert result["status"] == "incomplete"
    assert result["reasons"] == REQUIRED_SAFETY_FIELDS


def test_known_exclusion_takes_priority_over_missing_answer(
    safe_safety_answers,
):
    safe_safety_answers["current_injury_or_rehabilitation"] = True
    safe_safety_answers.pop("pregnant_or_postpartum")

    result = screen_safety(safe_safety_answers)

    assert result["status"] == "unsafe"
    assert result["reasons"] == ["current_injury_or_rehabilitation"]
