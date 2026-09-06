"""Integrity tests for the reviewed exercise library."""

from src.exercise_library import EXERCISE_LIBRARY, SOURCES
from src.profile_validation import (
    ACTIVITY_OPTIONS,
    EQUIPMENT_OPTIONS,
    EXPERIENCE_LEVELS,
    FITNESS_GOALS,
)


REQUIRED_EXERCISE_FIELDS = {
    "exercise_id",
    "name",
    "activity_type",
    "movement_pattern",
    "equipment_options",
    "optional_equipment",
    "experience_levels",
    "goal_tags",
    "preference_tags",
    "prescription_type",
    "source_ids",
}


def test_exercise_ids_are_unique():
    exercise_ids = [item["exercise_id"] for item in EXERCISE_LIBRARY]

    assert len(exercise_ids) == len(set(exercise_ids))


def test_every_exercise_has_the_required_fields():
    for item in EXERCISE_LIBRARY:
        assert set(item) == REQUIRED_EXERCISE_FIELDS


def test_exercise_metadata_uses_approved_values():
    for item in EXERCISE_LIBRARY:
        assert set(item["equipment_options"]) <= EQUIPMENT_OPTIONS
        assert set(item["optional_equipment"]) <= EQUIPMENT_OPTIONS
        assert set(item["experience_levels"]) <= EXPERIENCE_LEVELS
        assert set(item["goal_tags"]) <= FITNESS_GOALS
        assert set(item["preference_tags"]) <= ACTIVITY_OPTIONS
        assert item["prescription_type"] in {"sets_reps", "minutes"}
        assert set(item["source_ids"]) <= set(SOURCES)


def test_every_goal_has_at_least_one_exercise():
    supported_goals = {
        goal
        for item in EXERCISE_LIBRARY
        for goal in item["goal_tags"]
    }

    assert supported_goals == FITNESS_GOALS


def test_every_activity_preference_has_at_least_one_exercise():
    supported_preferences = {
        preference
        for item in EXERCISE_LIBRARY
        for preference in item["preference_tags"]
    }

    assert supported_preferences == ACTIVITY_OPTIONS


def test_every_equipment_category_is_represented():
    required_or_optional_equipment = {
        equipment
        for item in EXERCISE_LIBRARY
        for equipment in (
            item["equipment_options"] + item["optional_equipment"]
        )
    }

    assert EQUIPMENT_OPTIONS - {"No equipment, bodyweight only"} <= (
        required_or_optional_equipment
    )
    assert any(not item["equipment_options"] for item in EXERCISE_LIBRARY)
