"""Deterministic scheduling helpers for weekly workout plans."""

from itertools import combinations

from src.exercise_library import EXERCISE_LIBRARY
from src.profile_validation import validate_profile
from src.safety_screening import screen_safety


WEEKDAY_ORDER = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

MAX_WORKOUT_DAYS = {
    "Complete beginner": 3,
    "Returning to exercise": 4,
}

SESSION_EXERCISE_COUNTS = {
    15: 3,
    30: 5,
    45: 7,
    60: 8,
}

SESSION_TIMING = {
    15: {"warm_up": 2, "main": 11, "cool_down": 2},
    30: {"warm_up": 5, "main": 20, "cool_down": 5},
    45: {"warm_up": 5, "main": 35, "cool_down": 5},
    60: {"warm_up": 5, "main": 50, "cool_down": 5},
}

GOAL_SESSION_MIXES = {
    "Start exercising regularly": {
        "Complete beginner": (
            "full_body_strength",
            "full_body_strength",
            "preferred_activity",
        ),
        "Returning to exercise": (
            "full_body_strength",
            "full_body_strength",
            "preferred_activity",
            "preferred_activity",
        ),
    },
    "Improve overall fitness": {
        "Complete beginner": (
            "full_body_strength",
            "full_body_strength",
            "cardio",
        ),
        "Returning to exercise": (
            "full_body_strength",
            "full_body_strength",
            "cardio",
            "mobility",
        ),
    },
    "Get stronger": {
        "Complete beginner": (
            "strength",
            "strength",
            "cardio_or_mobility",
        ),
        "Returning to exercise": (
            "strength",
            "strength",
            "strength",
            "cardio_or_mobility",
        ),
    },
    "Increase stamina": {
        "Complete beginner": (
            "cardio",
            "cardio",
            "strength",
        ),
        "Returning to exercise": (
            "cardio",
            "cardio",
            "cardio",
            "strength",
        ),
    },
    "Improve flexibility and mobility": {
        "Complete beginner": (
            "mobility",
            "mobility",
            "strength",
        ),
        "Returning to exercise": (
            "mobility",
            "mobility",
            "strength",
            "cardio",
        ),
    },
}


def _schedule_score(day_indexes):
    """Return a score that favors recovery spacing and even gaps."""
    if len(day_indexes) < 2:
        return (0, 0, 0, 0, day_indexes)

    gaps = tuple(
        later - earlier
        for earlier, later in zip(day_indexes, day_indexes[1:])
    )
    consecutive_pairs = sum(gap == 1 for gap in gaps)
    minimum_gap = min(gaps)
    gap_range = max(gaps) - minimum_gap
    total_span = day_indexes[-1] - day_indexes[0]

    return (
        consecutive_pairs,
        -minimum_gap,
        gap_range,
        -total_span,
        day_indexes,
    )


def select_workout_days(available_days, experience_level):
    """Select a deterministic, recovery-aware subset of available days."""
    day_indexes = tuple(
        index
        for index, day in enumerate(WEEKDAY_ORDER)
        if day in available_days
    )
    target_count = min(
        len(day_indexes),
        MAX_WORKOUT_DAYS[experience_level],
    )

    candidate_schedules = combinations(day_indexes, target_count)
    selected_indexes = min(candidate_schedules, key=_schedule_score)

    return tuple(WEEKDAY_ORDER[index] for index in selected_indexes)


def select_session_focuses(primary_goal, experience_level, workout_count):
    """Return the highest-priority session focuses for the selected days."""
    approved_mix = GOAL_SESSION_MIXES[primary_goal][experience_level]
    return approved_mix[:workout_count]


def resolve_flexible_focus(profile, eligible_exercises):
    """Choose cardio or mobility using goals and available activities."""
    available_types = {
        exercise["activity_type"] for exercise in eligible_exercises
    }
    additional_goals = set(profile.get("additional_goals", []))

    if (
        "Increase stamina" in additional_goals
        and "cardio" in available_types
    ):
        return "cardio"
    if (
        "Improve flexibility and mobility" in additional_goals
        and "mobility" in available_types
    ):
        return "mobility"
    if "cardio" in available_types:
        return "cardio"
    if "mobility" in available_types:
        return "mobility"

    return None


def resolve_preferred_focus(
    profile,
    eligible_exercises,
    preferred_session_index=0,
):
    """Rotate through preferred activities that still have valid exercises."""
    valid_preferences = []
    for preference in profile["preferred_activities"]:
        if preference == "No preference":
            continue
        matching_exercises = tuple(
            exercise
            for exercise in eligible_exercises
            if preference in exercise["preference_tags"]
        )
        if matching_exercises:
            valid_preferences.append((preference, matching_exercises))

    if valid_preferences:
        _, matching_exercises = valid_preferences[
            preferred_session_index % len(valid_preferences)
        ]
        activity_type = matching_exercises[0]["activity_type"]
        return (
            "strength"
            if activity_type in {"strength", "bodyweight"}
            else activity_type
        )

    available_types = {
        exercise["activity_type"] for exercise in eligible_exercises
    }
    if "cardio" in available_types:
        return "cardio"
    if "mobility" in available_types:
        return "mobility"
    if available_types & {"strength", "bodyweight"}:
        return "strength"

    return None


def filter_eligible_exercises(profile, exercise_library=EXERCISE_LIBRARY):
    """Remove exercises that conflict with profile constraints."""
    available_equipment = set(profile["available_equipment"])
    disliked_activities = set(profile["disliked_activities"]) - {
        "No disliked activities"
    }
    experience_level = profile["experience_level"]

    eligible_exercises = []
    for exercise in exercise_library:
        equipment_options = set(exercise["equipment_options"])
        equipment_matches = (
            not equipment_options
            or bool(equipment_options & available_equipment)
        )
        experience_matches = (
            experience_level in exercise["experience_levels"]
        )
        dislikes_match = bool(
            set(exercise["preference_tags"]) & disliked_activities
        )

        if equipment_matches and experience_matches and not dislikes_match:
            eligible_exercises.append(exercise)

    return tuple(eligible_exercises)


def rank_exercises_by_preference(profile, eligible_exercises):
    """Place preferred activities first while preserving neutral options."""
    preferred_activities = set(profile["preferred_activities"]) - {
        "No preference"
    }

    return tuple(
        sorted(
            eligible_exercises,
            key=lambda exercise: not bool(
                set(exercise["preference_tags"]) & preferred_activities
            ),
        )
    )


def select_session_exercises(
    profile,
    session_focus,
    session_duration,
    eligible_exercises,
    selection_offset=0,
):
    """Select preferred, focus-matched exercises with movement variety."""
    strength_focuses = {"strength", "full_body_strength"}
    if session_focus in strength_focuses:
        accepted_types = {"strength", "bodyweight"}
    else:
        accepted_types = {session_focus}

    matching_exercises = tuple(
        exercise
        for exercise in eligible_exercises
        if exercise["activity_type"] in accepted_types
    )
    ranked_exercises = rank_exercises_by_preference(
        profile,
        matching_exercises,
    )
    if ranked_exercises and selection_offset:
        offset = selection_offset % len(ranked_exercises)
        ranked_exercises = (
            ranked_exercises[offset:] + ranked_exercises[:offset]
        )
    if session_focus in strength_focuses:
        exercise_limit = SESSION_EXERCISE_COUNTS[session_duration]
    elif session_focus == "cardio":
        exercise_limit = 1
    elif session_focus == "mobility":
        exercise_limit = 2
    else:
        exercise_limit = SESSION_EXERCISE_COUNTS[session_duration]

    selected = []
    used_patterns = set()
    for exercise in ranked_exercises:
        movement_pattern = exercise["movement_pattern"]
        if movement_pattern not in used_patterns:
            selected.append(exercise)
            used_patterns.add(movement_pattern)
        if len(selected) == exercise_limit:
            return tuple(selected)

    selected_ids = {exercise["exercise_id"] for exercise in selected}
    for exercise in ranked_exercises:
        if exercise["exercise_id"] not in selected_ids:
            selected.append(exercise)
        if len(selected) == exercise_limit:
            break

    return tuple(selected)


def add_exercise_prescriptions(
    profile,
    session_focus,
    session_duration,
    selected_exercises,
):
    """Add structured sets, repetitions, or minutes to selected exercises."""
    if not selected_exercises:
        return ()

    prescribed_exercises = []
    if session_focus in {"strength", "full_body_strength"}:
        sets = (
            2
            if profile["experience_level"] == "Complete beginner"
            else 3
        )
        for exercise in selected_exercises:
            prescribed_exercises.append(
                {
                    **exercise,
                    "prescription": {
                        "sets": sets,
                        "repetitions_min": 8,
                        "repetitions_max": 12,
                    },
                }
            )
        return tuple(prescribed_exercises)

    minutes_per_exercise, extra_minutes = divmod(
        session_duration,
        len(selected_exercises),
    )
    for index, exercise in enumerate(selected_exercises):
        prescribed_exercises.append(
            {
                **exercise,
                "prescription": {
                    "minutes": minutes_per_exercise
                    + (1 if index < extra_minutes else 0),
                },
            }
        )

    return tuple(prescribed_exercises)


def _blocked_result(message, reasons):
    return {
        "status": "blocked",
        "message": message,
        "weekly_summary": None,
        "warnings": [],
        "days": [],
        "totals": None,
        "reasons": reasons,
    }


def _workout_explanation(focus):
    explanations = {
        "strength": "Builds strength using eligible, balanced movements.",
        "full_body_strength": (
            "Builds full-body strength with varied movement patterns."
        ),
        "cardio": "Supports stamina with an eligible cardio activity.",
        "mobility": "Supports mobility using eligible gentle movement.",
    }
    return explanations[focus]


def _exercise_equipment(exercise, profile):
    available = set(profile["available_equipment"])
    required_options = tuple(exercise["equipment_options"])
    if not required_options:
        return []
    if "Full gym access" in available:
        return ["Full gym access"]
    return [item for item in required_options if item in available][:1]


def generate_weekly_plan(
    profile,
    safety_answers,
    challenging_intensity_confirmed=False,
):
    """Generate a gated, deterministic seven-day workout plan."""
    validation_errors = validate_profile(profile)
    if validation_errors:
        return _blocked_result(
            "Profile validation failed. A plan was not generated.",
            validation_errors,
        )

    safety_result = screen_safety(safety_answers)
    if safety_result["status"] != "safe":
        return _blocked_result(
            safety_result["message"],
            safety_result["reasons"],
        )

    needs_confirmation = (
        profile["preferred_intensity"] == "Challenging"
        and (
            profile["experience_level"] == "Complete beginner"
            or profile["current_activity_level"] == "Sedentary"
        )
    )
    if needs_confirmation and not challenging_intensity_confirmed:
        return {
            "status": "confirmation_required",
            "message": (
                "Confirm the challenging intensity before generating this "
                "beginner or sedentary profile's plan."
            ),
            "weekly_summary": None,
            "warnings": [
                "Challenging intensity may not be appropriate as a starting "
                "level."
            ],
            "days": [],
            "totals": None,
            "reasons": [],
        }

    selected_days = select_workout_days(
        profile["available_workout_days"],
        profile["experience_level"],
    )
    planned_focuses = select_session_focuses(
        profile["primary_goal"],
        profile["experience_level"],
        len(selected_days),
    )
    eligible_exercises = filter_eligible_exercises(profile)
    timing = SESSION_TIMING[profile["session_duration"]]

    resolved_focuses = []
    preferred_session_index = 0
    for focus in planned_focuses:
        if focus == "cardio_or_mobility":
            focus = resolve_flexible_focus(profile, eligible_exercises)
        elif focus == "preferred_activity":
            focus = resolve_preferred_focus(
                profile,
                eligible_exercises,
                preferred_session_index,
            )
            preferred_session_index += 1
        resolved_focuses.append(focus)

    if any(focus is None for focus in resolved_focuses):
        return _blocked_result(
            "No eligible exercises were available for every required focus.",
            ["exercise_availability"],
        )

    workout_by_day = dict(zip(selected_days, resolved_focuses))
    days = []
    strength_session_index = 0
    for day in WEEKDAY_ORDER:
        if day not in workout_by_day:
            days.append(
                {
                    "day": day,
                    "day_type": "rest",
                    "focus": "rest",
                    "warm_up": None,
                    "exercises": [],
                    "cool_down": None,
                    "total_minutes": 0,
                    "intensity": None,
                    "equipment": [],
                    "explanation": "Rest day supports recovery between workouts.",
                }
            )
            continue

        focus = workout_by_day[day]
        selection_offset = 0
        if (
            focus in {"strength", "full_body_strength"}
            and profile["experience_level"] == "Returning to exercise"
        ):
            selection_offset = strength_session_index
            strength_session_index += 1
        selected_exercises = select_session_exercises(
            profile,
            focus,
            profile["session_duration"],
            eligible_exercises,
            selection_offset,
        )
        if not selected_exercises:
            return _blocked_result(
                f"No eligible exercises were available for {focus}.",
                [focus],
            )
        prescribed_exercises = add_exercise_prescriptions(
            profile,
            focus,
            timing["main"],
            selected_exercises,
        )
        exercise_entries = [
            {
                "exercise_id": exercise["exercise_id"],
                "name": exercise["name"],
                "activity_type": exercise["activity_type"],
                "equipment": _exercise_equipment(exercise, profile),
                "prescription_type": exercise["prescription_type"],
                **exercise["prescription"],
                "effort_guidance": "Use a manageable, controlled effort.",
            }
            for exercise in prescribed_exercises
        ]
        equipment = sorted(
            {
                item
                for exercise in exercise_entries
                for item in exercise["equipment"]
            }
        )
        days.append(
            {
                "day": day,
                "day_type": "workout",
                "focus": focus,
                "warm_up": {
                    "minutes": timing["warm_up"],
                    "guidance": "Begin with gentle movement.",
                },
                "exercises": exercise_entries,
                "cool_down": {
                    "minutes": timing["cool_down"],
                    "guidance": "Finish with gentle movement.",
                },
                "total_minutes": profile["session_duration"],
                "intensity": profile["preferred_intensity"],
                "equipment": equipment,
                "explanation": _workout_explanation(focus),
            }
        )

    totals = {
        "workout_days": len(selected_days),
        "total_planned_minutes": (
            len(selected_days) * profile["session_duration"]
        ),
        "strength_sessions": sum(
            focus in {"strength", "full_body_strength"}
            for focus in resolved_focuses
        ),
        "cardio_sessions": resolved_focuses.count("cardio"),
        "mobility_sessions": resolved_focuses.count("mobility"),
    }
    return {
        "status": "generated",
        "message": "Weekly workout plan generated successfully.",
        "weekly_summary": (
            f"A {len(selected_days)}-day plan for "
            f"{profile['primary_goal'].lower()}, scheduled around the "
            "profile's availability and recovery time."
        ),
        "warnings": [],
        "days": days,
        "totals": totals,
        "reasons": [],
    }
