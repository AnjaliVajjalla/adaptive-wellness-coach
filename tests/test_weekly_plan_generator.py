"""Tests for deterministic weekly workout scheduling."""

import pytest

from src.exercise_library import EXERCISE_LIBRARY
from src.weekly_plan_generator import (
    add_exercise_prescriptions,
    filter_eligible_exercises,
    generate_weekly_plan,
    rank_exercises_by_preference,
    resolve_flexible_focus,
    resolve_preferred_focus,
    select_session_exercises,
    select_session_focuses,
    select_workout_days,
)


@pytest.fixture
def planning_profile():
    return {
        "experience_level": "Complete beginner",
        "available_equipment": ["No equipment, bodyweight only"],
        "preferred_activities": ["Bodyweight workouts"],
        "disliked_activities": ["Jogging or running"],
    }


@pytest.fixture
def complete_planning_profile(planning_profile):
    return {
        "profile_id": "fictional_plan_001",
        "primary_goal": "Get stronger",
        "additional_goals": [],
        "current_activity_level": "Light",
        "available_workout_days": ["Monday", "Wednesday", "Friday"],
        "session_duration": 30,
        "preferred_intensity": "Moderate",
        **planning_profile,
    }


@pytest.fixture
def safe_answers():
    return {
        "pregnant_or_postpartum": False,
        "current_injury_or_rehabilitation": False,
        "eating_disorder_concern": False,
        "complex_or_uncontrolled_medical_condition": False,
        "requests_diagnosis_or_treatment": False,
        "extreme_weight_loss_goal": False,
        "requests_medication_supplement_or_therapeutic_diet": False,
    }


def test_beginner_schedule_prefers_evenly_spaced_days():
    selected_days = select_workout_days(
        ["Monday", "Tuesday", "Wednesday", "Friday"],
        "Complete beginner",
    )

    assert selected_days == ("Monday", "Wednesday", "Friday")


def test_returning_schedule_uses_no_more_than_four_days():
    selected_days = select_workout_days(
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        "Returning to exercise",
    )

    assert selected_days == ("Monday", "Wednesday", "Friday", "Sunday")


def test_schedule_uses_all_days_when_fewer_than_the_limit_are_available():
    selected_days = select_workout_days(
        ["Tuesday", "Saturday"],
        "Complete beginner",
    )

    assert selected_days == ("Tuesday", "Saturday")


def test_schedule_returns_days_in_weekday_order():
    selected_days = select_workout_days(
        ["Friday", "Monday", "Wednesday"],
        "Complete beginner",
    )

    assert selected_days == ("Monday", "Wednesday", "Friday")


@pytest.mark.parametrize(
    ("primary_goal", "experience_level", "expected_focuses"),
    [
        (
            "Start exercising regularly",
            "Complete beginner",
            (
                "full_body_strength",
                "full_body_strength",
                "preferred_activity",
            ),
        ),
        (
            "Improve overall fitness",
            "Returning to exercise",
            (
                "full_body_strength",
                "full_body_strength",
                "cardio",
                "mobility",
            ),
        ),
        (
            "Get stronger",
            "Returning to exercise",
            (
                "strength",
                "strength",
                "strength",
                "cardio_or_mobility",
            ),
        ),
        (
            "Increase stamina",
            "Complete beginner",
            ("cardio", "cardio", "strength"),
        ),
        (
            "Improve flexibility and mobility",
            "Returning to exercise",
            ("mobility", "mobility", "strength", "cardio"),
        ),
    ],
)
def test_goal_and_experience_control_session_mix(
    primary_goal,
    experience_level,
    expected_focuses,
):
    assert (
        select_session_focuses(
            primary_goal,
            experience_level,
            len(expected_focuses),
        )
        == expected_focuses
    )


def test_fewer_available_days_keep_the_highest_priority_focuses():
    selected_focuses = select_session_focuses(
        "Increase stamina",
        "Returning to exercise",
        2,
    )

    assert selected_focuses == ("cardio", "cardio")


def test_no_equipment_profile_excludes_equipment_exercises(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)

    assert eligible
    assert all(not item["equipment_options"] for item in eligible)


def test_bicycle_equipment_makes_cycling_eligible(planning_profile):
    planning_profile["available_equipment"] = [
        "Bicycle or stationary bike"
    ]

    eligible = filter_eligible_exercises(planning_profile)
    eligible_ids = {item["exercise_id"] for item in eligible}

    assert "cycling" in eligible_ids
    assert "dumbbell_floor_press" not in eligible_ids


def test_full_gym_access_supports_every_equipment_requirement(
    planning_profile,
):
    planning_profile["experience_level"] = "Returning to exercise"
    planning_profile["available_equipment"] = ["Full gym access"]
    planning_profile["disliked_activities"] = ["No disliked activities"]

    eligible = filter_eligible_exercises(planning_profile)

    assert len(eligible) == len(EXERCISE_LIBRARY)


def test_beginner_profile_excludes_returning_only_exercises(
    planning_profile,
):
    eligible = filter_eligible_exercises(planning_profile)
    eligible_ids = {item["exercise_id"] for item in eligible}

    assert "jogging" not in eligible_ids
    assert "weighted_romanian_deadlift" not in eligible_ids


def test_disliked_activity_removes_every_matching_exercise(
    planning_profile,
):
    eligible = filter_eligible_exercises(planning_profile)

    assert all(
        "Jogging or running" not in item["preference_tags"]
        for item in eligible
    )


def test_preferences_rank_matching_exercises_before_neutral_ones(
    planning_profile,
):
    planning_profile["preferred_activities"] = ["Yoga or mobility"]
    eligible = filter_eligible_exercises(planning_profile)

    ranked = rank_exercises_by_preference(planning_profile, eligible)
    first_neutral_index = next(
        index
        for index, item in enumerate(ranked)
        if "Yoga or mobility" not in item["preference_tags"]
    )

    assert first_neutral_index > 0
    assert all(
        "Yoga or mobility" in item["preference_tags"]
        for item in ranked[:first_neutral_index]
    )


def test_no_preference_preserves_library_order(planning_profile):
    planning_profile["preferred_activities"] = ["No preference"]
    eligible = filter_eligible_exercises(planning_profile)

    assert rank_exercises_by_preference(planning_profile, eligible) == eligible


def test_stamina_additional_goal_selects_cardio(planning_profile):
    planning_profile["additional_goals"] = ["Increase stamina"]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_flexible_focus(planning_profile, eligible) == "cardio"


def test_mobility_additional_goal_selects_mobility(planning_profile):
    planning_profile["additional_goals"] = [
        "Improve flexibility and mobility"
    ]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_flexible_focus(planning_profile, eligible) == "mobility"


def test_flexible_focus_defaults_to_cardio(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_flexible_focus(planning_profile, eligible) == "cardio"


def test_flexible_focus_uses_mobility_when_cardio_is_filtered_out(
    planning_profile,
):
    planning_profile["disliked_activities"] = [
        "Walking",
        "Jogging or running",
        "Cycling",
    ]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_flexible_focus(planning_profile, eligible) == "mobility"


def test_flexible_focus_reports_when_neither_option_is_available(
    planning_profile,
):
    eligible = tuple(
        exercise
        for exercise in filter_eligible_exercises(planning_profile)
        if exercise["activity_type"] not in {"cardio", "mobility"}
    )

    assert resolve_flexible_focus(planning_profile, eligible) is None


def test_preferred_sessions_rotate_through_valid_preferences(
    planning_profile,
):
    planning_profile["preferred_activities"] = [
        "Walking",
        "Yoga or mobility",
    ]
    eligible = filter_eligible_exercises(planning_profile)

    first_focus = resolve_preferred_focus(planning_profile, eligible, 0)
    second_focus = resolve_preferred_focus(planning_profile, eligible, 1)

    assert first_focus == "cardio"
    assert second_focus == "mobility"


def test_preferred_rotation_repeats_after_the_last_preference(
    planning_profile,
):
    planning_profile["preferred_activities"] = [
        "Walking",
        "Yoga or mobility",
    ]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_preferred_focus(planning_profile, eligible, 2) == "cardio"


def test_preferred_focus_skips_a_preference_without_eligible_exercises(
    planning_profile,
):
    planning_profile["preferred_activities"] = [
        "Cycling",
        "Yoga or mobility",
    ]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_preferred_focus(planning_profile, eligible, 0) == "mobility"


def test_strength_preferences_resolve_to_strength(planning_profile):
    planning_profile["preferred_activities"] = ["Bodyweight workouts"]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_preferred_focus(planning_profile, eligible, 0) == "strength"


def test_no_preference_uses_cardio_as_the_default(planning_profile):
    planning_profile["preferred_activities"] = ["No preference"]
    eligible = filter_eligible_exercises(planning_profile)

    assert resolve_preferred_focus(planning_profile, eligible, 0) == "cardio"


@pytest.mark.parametrize(
    ("session_duration", "expected_count"),
    [(15, 3), (30, 5), (45, 7), (60, 8)],
)
def test_session_duration_controls_exercise_count(
    planning_profile,
    session_duration,
    expected_count,
):
    planning_profile["experience_level"] = "Returning to exercise"
    planning_profile["available_equipment"] = ["Full gym access"]
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "strength",
        session_duration,
        eligible,
    )

    assert len(selected) == expected_count


def test_strength_selection_prioritizes_movement_variety(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "full_body_strength",
        30,
        eligible,
    )
    selected_patterns = [item["movement_pattern"] for item in selected]

    assert len(selected_patterns) == len(set(selected_patterns))


def test_session_selection_matches_the_requested_focus(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "mobility",
        30,
        eligible,
    )

    assert selected
    assert all(item["activity_type"] == "mobility" for item in selected)


def test_cardio_session_selects_one_activity(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "cardio",
        60,
        eligible,
    )

    assert len(selected) == 1


def test_session_selection_ranks_preferences_first(planning_profile):
    planning_profile["available_equipment"] = [
        "No equipment, bodyweight only",
        "Bicycle or stationary bike",
    ]
    planning_profile["preferred_activities"] = ["Cycling"]
    planning_profile["disliked_activities"] = ["No disliked activities"]
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "cardio",
        15,
        eligible,
    )

    assert selected[0]["exercise_id"] == "cycling"


def test_session_selection_never_duplicates_an_exercise(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "full_body_strength",
        60,
        eligible,
    )
    selected_ids = [item["exercise_id"] for item in selected]

    assert len(selected_ids) == len(set(selected_ids))


def test_session_can_return_fewer_exercises_than_the_duration_limit(
    planning_profile,
):
    eligible = filter_eligible_exercises(planning_profile)

    selected = select_session_exercises(
        planning_profile,
        "mobility",
        60,
        eligible,
    )

    assert len(selected) == 2


def test_strength_prescriptions_use_two_sets_for_beginners(planning_profile):
    eligible = filter_eligible_exercises(planning_profile)
    selected = select_session_exercises(
        planning_profile,
        "strength",
        15,
        eligible,
    )

    prescribed = add_exercise_prescriptions(
        planning_profile,
        "strength",
        15,
        selected,
    )

    assert all(
        item["prescription"]
        == {"sets": 2, "repetitions_min": 8, "repetitions_max": 12}
        for item in prescribed
    )


def test_returning_prescriptions_use_three_strength_sets(planning_profile):
    planning_profile["experience_level"] = "Returning to exercise"
    eligible = filter_eligible_exercises(planning_profile)
    selected = select_session_exercises(
        planning_profile,
        "strength",
        15,
        eligible,
    )

    prescribed = add_exercise_prescriptions(
        planning_profile,
        "strength",
        15,
        selected,
    )

    assert all(item["prescription"]["sets"] == 3 for item in prescribed)


def test_cardio_prescription_uses_the_full_session_duration(
    planning_profile,
):
    eligible = filter_eligible_exercises(planning_profile)
    selected = select_session_exercises(
        planning_profile,
        "cardio",
        30,
        eligible,
    )

    prescribed = add_exercise_prescriptions(
        planning_profile,
        "cardio",
        30,
        selected,
    )

    assert prescribed[0]["prescription"] == {"minutes": 30}


def test_mobility_prescription_splits_minutes_across_exercises(
    planning_profile,
):
    eligible = filter_eligible_exercises(planning_profile)
    selected = select_session_exercises(
        planning_profile,
        "mobility",
        15,
        eligible,
    )

    prescribed = add_exercise_prescriptions(
        planning_profile,
        "mobility",
        15,
        selected,
    )
    prescribed_minutes = [
        item["prescription"]["minutes"] for item in prescribed
    ]

    assert prescribed_minutes == [8, 7]
    assert sum(prescribed_minutes) == 15


def test_adding_prescriptions_does_not_mutate_the_exercise_library(
    planning_profile,
):
    eligible = filter_eligible_exercises(planning_profile)
    selected = select_session_exercises(
        planning_profile,
        "strength",
        15,
        eligible,
    )

    add_exercise_prescriptions(
        planning_profile,
        "strength",
        15,
        selected,
    )

    assert all("prescription" not in item for item in EXERCISE_LIBRARY)


def test_generated_plan_contains_all_seven_days(
    complete_planning_profile,
    safe_answers,
):
    result = generate_weekly_plan(complete_planning_profile, safe_answers)

    assert result["status"] == "generated"
    assert [entry["day"] for entry in result["days"]] == [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def test_generated_plan_uses_selected_days_and_marks_the_rest(
    complete_planning_profile,
    safe_answers,
):
    result = generate_weekly_plan(complete_planning_profile, safe_answers)
    workout_days = [
        entry["day"]
        for entry in result["days"]
        if entry["day_type"] == "workout"
    ]
    rest_days = [
        entry for entry in result["days"] if entry["day_type"] == "rest"
    ]

    assert workout_days == ["Monday", "Wednesday", "Friday"]
    assert all(entry["exercises"] == [] for entry in rest_days)


def test_generated_plan_reports_calculated_weekly_totals(
    complete_planning_profile,
    safe_answers,
):
    result = generate_weekly_plan(complete_planning_profile, safe_answers)

    assert result["totals"] == {
        "workout_days": 3,
        "total_planned_minutes": 90,
        "strength_sessions": 2,
        "cardio_sessions": 1,
        "mobility_sessions": 0,
    }


def test_workout_entries_include_timing_exercises_and_explanations(
    complete_planning_profile,
    safe_answers,
):
    result = generate_weekly_plan(complete_planning_profile, safe_answers)
    workout_entries = [
        entry for entry in result["days"] if entry["day_type"] == "workout"
    ]

    assert all(entry["warm_up"]["minutes"] == 5 for entry in workout_entries)
    assert all(entry["cool_down"]["minutes"] == 5 for entry in workout_entries)
    assert all(entry["exercises"] for entry in workout_entries)
    assert all(entry["explanation"] for entry in workout_entries)


def test_invalid_profile_is_blocked_before_plan_generation(
    complete_planning_profile,
    safe_answers,
):
    del complete_planning_profile["session_duration"]

    result = generate_weekly_plan(complete_planning_profile, safe_answers)

    assert result["status"] == "blocked"
    assert result["days"] == []
    assert "Missing required field: session duration." in result["reasons"]


def test_unsafe_profile_is_blocked_before_plan_generation(
    complete_planning_profile,
    safe_answers,
):
    safe_answers["current_injury_or_rehabilitation"] = True

    result = generate_weekly_plan(complete_planning_profile, safe_answers)

    assert result["status"] == "blocked"
    assert result["days"] == []
    assert result["reasons"] == ["current_injury_or_rehabilitation"]


def test_challenging_beginner_plan_requires_confirmation(
    complete_planning_profile,
    safe_answers,
):
    complete_planning_profile["preferred_intensity"] = "Challenging"

    result = generate_weekly_plan(complete_planning_profile, safe_answers)

    assert result["status"] == "confirmation_required"
    assert result["days"] == []


def test_confirmed_challenging_beginner_plan_can_be_generated(
    complete_planning_profile,
    safe_answers,
):
    complete_planning_profile["preferred_intensity"] = "Challenging"

    result = generate_weekly_plan(
        complete_planning_profile,
        safe_answers,
        challenging_intensity_confirmed=True,
    )

    assert result["status"] == "generated"


def test_disliked_activities_never_appear_in_the_generated_plan(
    complete_planning_profile,
    safe_answers,
):
    result = generate_weekly_plan(complete_planning_profile, safe_answers)
    exercise_names = {
        exercise["name"]
        for day in result["days"]
        for exercise in day["exercises"]
    }

    assert "Jogging" not in exercise_names
    assert "Walk-jog intervals" not in exercise_names


def test_beginner_strength_sessions_repeat_for_consistency(
    complete_planning_profile,
    safe_answers,
):
    result = generate_weekly_plan(complete_planning_profile, safe_answers)
    strength_sessions = [
        tuple(exercise["exercise_id"] for exercise in day["exercises"])
        for day in result["days"]
        if day["focus"] in {"strength", "full_body_strength"}
    ]

    assert len(strength_sessions) == 2
    assert strength_sessions[0] == strength_sessions[1]


def test_returning_strength_sessions_rotate_exercises(
    complete_planning_profile,
    safe_answers,
):
    complete_planning_profile["experience_level"] = "Returning to exercise"
    complete_planning_profile["available_workout_days"] = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    complete_planning_profile["available_equipment"] = ["Full gym access"]
    complete_planning_profile["disliked_activities"] = [
        "No disliked activities"
    ]

    result = generate_weekly_plan(complete_planning_profile, safe_answers)
    strength_sessions = [
        tuple(exercise["exercise_id"] for exercise in day["exercises"])
        for day in result["days"]
        if day["focus"] in {"strength", "full_body_strength"}
    ]

    assert len(strength_sessions) == 3
    assert len(set(strength_sessions)) == 3
