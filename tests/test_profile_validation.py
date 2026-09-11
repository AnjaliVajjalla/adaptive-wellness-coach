"""Automated tests for fictional user-profile validation."""

import pytest

from src.profile_validation import REQUIRED_FIELDS, validate_profile


@pytest.fixture
def complete_profile():
    return {
        "profile_id": "profile_001",
        "primary_goal": "Get stronger",
        "additional_goals": ["Improve overall fitness"],
        "experience_level": "Complete beginner",
        "current_activity_level": "Light",
        "available_workout_days": ["Monday", "Wednesday", "Friday"],
        "session_duration": 30,
        "workout_split_preference": "Let the coach choose",
        "available_equipment": ["Exercise mat", "Dumbbells"],
        "preferred_activities": [
            "Strength training",
            "Bodyweight workouts",
        ],
        "disliked_activities": ["Jogging or running"],
        "preferred_intensity": "Moderate",
    }


def test_complete_beginner_profile_passes(complete_profile):
    assert validate_profile(complete_profile) == []


def test_complete_returning_profile_passes(complete_profile):
    complete_profile.update(
        {
            "profile_id": "profile_002",
            "primary_goal": "Increase stamina",
            "additional_goals": [],
            "experience_level": "Returning to exercise",
            "current_activity_level": "Moderate",
            "available_workout_days": ["Tuesday", "Thursday"],
            "session_duration": 45,
            "available_equipment": ["No equipment, bodyweight only"],
            "preferred_activities": ["Walking", "Cycling"],
            "disliked_activities": ["No disliked activities"],
            "preferred_intensity": "Challenging",
        }
    )

    assert validate_profile(complete_profile) == []


def test_bicycle_or_stationary_bike_is_supported(complete_profile):
    complete_profile["available_equipment"] = [
        "Bicycle or stationary bike"
    ]

    assert validate_profile(complete_profile) == []


@pytest.mark.parametrize("missing_field", REQUIRED_FIELDS)
def test_each_missing_required_field_is_reported(
    complete_profile,
    missing_field,
):
    complete_profile.pop(missing_field)

    errors = validate_profile(complete_profile)

    readable_field = missing_field.replace("_", " ")
    assert f"Missing required field: {readable_field}." in errors


@pytest.mark.parametrize("empty_value", [None, "", []])
def test_empty_required_field_is_reported(complete_profile, empty_value):
    complete_profile["session_duration"] = empty_value

    errors = validate_profile(complete_profile)

    assert "Missing required field: session duration." in errors


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("primary_goal", "Lose weight quickly"),
        ("experience_level", "Advanced athlete"),
        ("current_activity_level", "Very active"),
        ("session_duration", 20),
        ("workout_split_preference", "Bro split"),
        ("preferred_intensity", "Extreme"),
    ],
)
def test_invalid_single_choice_is_rejected(
    complete_profile,
    field,
    invalid_value,
):
    complete_profile[field] = invalid_value

    errors = validate_profile(complete_profile)

    readable_field = field.replace("_", " ")
    assert any(f"Invalid {readable_field}" in error for error in errors)


def test_profile_id_must_be_text(complete_profile):
    complete_profile["profile_id"] = 101

    errors = validate_profile(complete_profile)

    assert "Profile ID must be text." in errors


def test_additional_goals_must_be_a_list(complete_profile):
    complete_profile["additional_goals"] = "Improve overall fitness"

    errors = validate_profile(complete_profile)

    assert "Additional goals must be a list." in errors


def test_additional_goals_reject_unsupported_value(complete_profile):
    complete_profile["additional_goals"] = ["Build muscle quickly"]

    errors = validate_profile(complete_profile)

    assert "Invalid additional goals: Build muscle quickly." in errors


def test_additional_goals_reject_duplicates(complete_profile):
    complete_profile["additional_goals"] = [
        "Improve overall fitness",
        "Improve overall fitness",
    ]

    errors = validate_profile(complete_profile)

    assert "Additional goals cannot contain duplicate values." in errors


def test_multi_select_field_must_be_a_list(complete_profile):
    complete_profile["available_workout_days"] = "Monday"

    errors = validate_profile(complete_profile)

    assert "Available workout days must be a list." in errors


def test_multi_select_field_rejects_non_text_items(complete_profile):
    complete_profile["preferred_activities"] = [["Walking"]]

    errors = validate_profile(complete_profile)

    assert "Preferred activities must contain only text values." in errors


def test_multi_select_field_rejects_duplicates(complete_profile):
    complete_profile["available_workout_days"] = ["Monday", "Monday"]

    errors = validate_profile(complete_profile)

    assert "Available workout days cannot contain duplicate values." in errors


def test_multi_select_field_rejects_unsupported_value(complete_profile):
    complete_profile["available_workout_days"] = ["Funday"]

    errors = validate_profile(complete_profile)

    assert "Invalid available workout days: Funday." in errors


def test_no_equipment_must_be_selected_alone(complete_profile):
    complete_profile["available_equipment"] = [
        "No equipment, bodyweight only",
        "Dumbbells",
    ]

    errors = validate_profile(complete_profile)

    assert (
        "No equipment, bodyweight only cannot be combined with other equipment."
        in errors
    )


def test_no_preference_must_be_selected_alone(complete_profile):
    complete_profile["preferred_activities"] = ["No preference", "Walking"]

    errors = validate_profile(complete_profile)

    assert "No preference must be selected alone." in errors


def test_no_disliked_activities_must_be_selected_alone(complete_profile):
    complete_profile["disliked_activities"] = [
        "No disliked activities",
        "Jogging or running",
    ]

    errors = validate_profile(complete_profile)

    assert "No disliked activities must be selected alone." in errors


def test_activity_cannot_be_preferred_and_disliked(complete_profile):
    complete_profile["preferred_activities"] = ["Walking"]
    complete_profile["disliked_activities"] = ["Walking"]

    errors = validate_profile(complete_profile)

    assert "Activities cannot be both preferred and disliked: Walking." in errors


def test_primary_goal_cannot_be_an_additional_goal(complete_profile):
    complete_profile["additional_goals"] = ["Get stronger"]

    errors = validate_profile(complete_profile)

    assert "Primary goal cannot also appear in additional goals." in errors


@pytest.mark.parametrize("malformed_profile", [None, [], "profile"])
def test_malformed_profile_fails_without_crashing(malformed_profile):
    assert validate_profile(malformed_profile) == [
        "Profile must be a dictionary-like object."
    ]
