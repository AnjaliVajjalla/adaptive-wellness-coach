"""Validation helpers for fictional user profiles."""

from collections.abc import Mapping


FITNESS_GOALS = {
    "Start exercising regularly",
    "Improve overall fitness",
    "Get stronger",
    "Increase stamina",
    "Improve flexibility and mobility",
}

EXPERIENCE_LEVELS = {
    "Complete beginner",
    "Returning to exercise",
}

ACTIVITY_LEVELS = {"Sedentary", "Light", "Moderate", "Heavy"}

WEEKDAYS = {
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
}

SESSION_DURATIONS = {15, 30, 45, 60}

EQUIPMENT_OPTIONS = {
    "No equipment, bodyweight only",
    "Exercise mat",
    "Resistance bands",
    "Dumbbells",
    "Kettlebell",
    "Full gym access",
}

ACTIVITY_OPTIONS = {
    "Walking",
    "Jogging or running",
    "Cycling",
    "Strength training",
    "Bodyweight workouts",
    "Yoga or mobility",
}

INTENSITY_OPTIONS = {"Gentle", "Moderate", "Challenging", "No preference"}

REQUIRED_FIELDS = [
    "profile_id",
    "primary_goal",
    "experience_level",
    "current_activity_level",
    "available_workout_days",
    "session_duration",
    "available_equipment",
    "preferred_activities",
    "disliked_activities",
    "preferred_intensity",
]


def _display_name(field):
    return field.replace("_", " ")


def _is_empty(value):
    return value is None or value == "" or value == []


def _is_text_list(value):
    return isinstance(value, list) and all(
        isinstance(item, str) for item in value
    )


def find_missing_fields(profile):
    """Return the required fields that are absent or empty."""
    if not isinstance(profile, Mapping):
        return REQUIRED_FIELDS.copy()

    return [
        field
        for field in REQUIRED_FIELDS
        if field not in profile or _is_empty(profile[field])
    ]


def _validate_single_choice(profile, field, allowed_values, errors):
    if field not in profile or _is_empty(profile[field]):
        return

    if profile[field] not in allowed_values:
        choices = ", ".join(sorted(map(str, allowed_values)))
        errors.append(
            f"Invalid {_display_name(field)}: {profile[field]!r}. "
            f"Choose one of: {choices}."
        )


def _validate_multi_choice(profile, field, allowed_values, errors):
    if field not in profile or _is_empty(profile[field]):
        return

    values = profile[field]
    if not isinstance(values, list):
        errors.append(f"{_display_name(field).capitalize()} must be a list.")
        return

    if any(not isinstance(value, str) for value in values):
        errors.append(
            f"{_display_name(field).capitalize()} must contain only text values."
        )
        return

    if len(values) != len(set(values)):
        errors.append(
            f"{_display_name(field).capitalize()} cannot contain duplicate values."
        )

    invalid_values = sorted(set(values) - allowed_values)
    if invalid_values:
        errors.append(
            f"Invalid {_display_name(field)}: {', '.join(invalid_values)}."
        )


def validate_profile(profile):
    """Return understandable validation errors for a fictional profile."""
    if not isinstance(profile, Mapping):
        return ["Profile must be a dictionary-like object."]

    errors = []

    for field in find_missing_fields(profile):
        errors.append(f"Missing required field: {_display_name(field)}.")

    if "profile_id" in profile and not _is_empty(profile["profile_id"]):
        if not isinstance(profile["profile_id"], str):
            errors.append("Profile ID must be text.")

    _validate_single_choice(profile, "primary_goal", FITNESS_GOALS, errors)
    _validate_single_choice(
        profile, "experience_level", EXPERIENCE_LEVELS, errors
    )
    _validate_single_choice(
        profile, "current_activity_level", ACTIVITY_LEVELS, errors
    )
    _validate_single_choice(
        profile, "session_duration", SESSION_DURATIONS, errors
    )
    _validate_single_choice(
        profile, "preferred_intensity", INTENSITY_OPTIONS, errors
    )

    _validate_multi_choice(
        profile, "available_workout_days", WEEKDAYS, errors
    )
    _validate_multi_choice(
        profile, "available_equipment", EQUIPMENT_OPTIONS, errors
    )
    _validate_multi_choice(
        profile,
        "preferred_activities",
        ACTIVITY_OPTIONS | {"No preference"},
        errors,
    )
    _validate_multi_choice(
        profile,
        "disliked_activities",
        ACTIVITY_OPTIONS | {"No disliked activities"},
        errors,
    )

    additional_goals = profile.get("additional_goals")
    if additional_goals is not None:
        _validate_multi_choice(
            profile, "additional_goals", FITNESS_GOALS, errors
        )

    equipment = profile.get("available_equipment")
    if (
        isinstance(equipment, list)
        and "No equipment, bodyweight only" in equipment
        and len(equipment) > 1
    ):
        errors.append(
            "No equipment, bodyweight only cannot be combined with other equipment."
        )

    preferred = profile.get("preferred_activities")
    if (
        isinstance(preferred, list)
        and "No preference" in preferred
        and len(preferred) > 1
    ):
        errors.append("No preference must be selected alone.")

    disliked = profile.get("disliked_activities")
    if (
        isinstance(disliked, list)
        and "No disliked activities" in disliked
        and len(disliked) > 1
    ):
        errors.append("No disliked activities must be selected alone.")

    if _is_text_list(preferred) and _is_text_list(disliked):
        overlap = sorted(
            (set(preferred) & set(disliked))
            - {"No preference", "No disliked activities"}
        )
        if overlap:
            errors.append(
                "Activities cannot be both preferred and disliked: "
                f"{', '.join(overlap)}."
            )

    primary_goal = profile.get("primary_goal")
    if (
        isinstance(additional_goals, list)
        and primary_goal in additional_goals
    ):
        errors.append("Primary goal cannot also appear in additional goals.")

    return errors
