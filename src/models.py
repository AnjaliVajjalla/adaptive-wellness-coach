"""Strict Pydantic models for Adaptive Wellness Coach data contracts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


FitnessGoal = Literal[
    "Start exercising regularly",
    "Improve overall fitness",
    "Get stronger",
    "Increase stamina",
    "Improve flexibility and mobility",
]
ExperienceLevel = Literal["Complete beginner", "Returning to exercise"]
ActivityLevel = Literal["Sedentary", "Light", "Moderate", "Heavy"]
Weekday = Literal[
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
SessionDuration = Literal[15, 30, 45, 60]
Equipment = Literal[
    "No equipment, bodyweight only",
    "Exercise mat",
    "Resistance bands",
    "Dumbbells",
    "Kettlebell",
    "Bicycle or stationary bike",
    "Full gym access",
]
ActivityPreference = Literal[
    "Walking",
    "Jogging or running",
    "Cycling",
    "Strength training",
    "Bodyweight workouts",
    "Yoga or mobility",
    "No preference",
]
DislikedActivity = Literal[
    "Walking",
    "Jogging or running",
    "Cycling",
    "Strength training",
    "Bodyweight workouts",
    "Yoga or mobility",
    "No disliked activities",
]
PreferredIntensity = Literal[
    "Gentle",
    "Moderate",
    "Challenging",
    "No preference",
]
PlanStatus = Literal["generated", "confirmation_required", "blocked"]
DayType = Literal["workout", "recovery", "rest"]
SessionFocus = Literal[
    "strength",
    "full_body_strength",
    "cardio",
    "mobility",
    "recovery",
    "rest",
]
ActivityType = Literal["strength", "bodyweight", "cardio", "mobility"]
PrescriptionType = Literal["sets_reps", "minutes"]
FeedbackDifficulty = Literal[
    "too_easy",
    "appropriate",
    "too_hard",
    "not_stated",
]
RequestedFocus = Literal[
    "strength",
    "full_body_strength",
    "cardio",
    "mobility",
]


class UserProfile(BaseModel):
    """Validated fictional profile accepted by the planning workflow."""

    model_config = ConfigDict(strict=True, extra="forbid")

    profile_id: str = Field(min_length=1)
    primary_goal: FitnessGoal
    additional_goals: list[FitnessGoal] = Field(default_factory=list)
    experience_level: ExperienceLevel
    current_activity_level: ActivityLevel
    available_workout_days: list[Weekday] = Field(min_length=1)
    session_duration: SessionDuration
    available_equipment: list[Equipment] = Field(min_length=1)
    preferred_activities: list[ActivityPreference] = Field(min_length=1)
    disliked_activities: list[DislikedActivity] = Field(min_length=1)
    preferred_intensity: PreferredIntensity

    @field_validator(
        "additional_goals",
        "available_workout_days",
        "available_equipment",
        "preferred_activities",
        "disliked_activities",
    )
    @classmethod
    def reject_duplicate_values(cls, values):
        if len(values) != len(set(values)):
            raise ValueError("Duplicate values are not allowed.")
        return values

    @model_validator(mode="after")
    def validate_field_relationships(self):
        if self.primary_goal in self.additional_goals:
            raise ValueError(
                "Primary goal cannot also appear in additional goals."
            )
        if (
            "No equipment, bodyweight only" in self.available_equipment
            and len(self.available_equipment) > 1
        ):
            raise ValueError(
                "No equipment, bodyweight only must be selected alone."
            )
        if (
            "No preference" in self.preferred_activities
            and len(self.preferred_activities) > 1
        ):
            raise ValueError("No preference must be selected alone.")
        if (
            "No disliked activities" in self.disliked_activities
            and len(self.disliked_activities) > 1
        ):
            raise ValueError("No disliked activities must be selected alone.")

        overlap = (
            set(self.preferred_activities) & set(self.disliked_activities)
        ) - {"No preference", "No disliked activities"}
        if overlap:
            raise ValueError(
                "Activities cannot be both preferred and disliked: "
                f"{', '.join(sorted(overlap))}."
            )
        return self


class SafetyAnswers(BaseModel):
    """Complete, strictly Boolean safety answers accepted by the API."""

    model_config = ConfigDict(strict=True, extra="forbid")

    pregnant_or_postpartum: bool
    current_injury_or_rehabilitation: bool
    eating_disorder_concern: bool
    complex_or_uncontrolled_medical_condition: bool
    requests_diagnosis_or_treatment: bool
    extreme_weight_loss_goal: bool
    requests_medication_supplement_or_therapeutic_diet: bool


class PlanGenerationRequest(BaseModel):
    """Validated input for one weekly-plan request."""

    model_config = ConfigDict(strict=True, extra="forbid")

    profile: UserProfile
    safety_answers: SafetyAnswers
    challenging_intensity_confirmed: bool = False


class HealthResponse(BaseModel):
    """Response returned by the API health endpoint."""

    model_config = ConfigDict(strict=True, extra="forbid")

    status: Literal["healthy"]


class TimedGuidance(BaseModel):
    """Timed warm-up or cool-down instruction."""

    model_config = ConfigDict(strict=True, extra="forbid")

    minutes: int = Field(gt=0)
    guidance: str = Field(min_length=1)


class ExerciseEntry(BaseModel):
    """One exercise and its activity-appropriate prescription."""

    model_config = ConfigDict(strict=True, extra="forbid")

    exercise_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    activity_type: ActivityType
    equipment: list[str]
    prescription_type: PrescriptionType
    sets: int | None = Field(default=None, gt=0)
    repetitions_min: int | None = Field(default=None, gt=0)
    repetitions_max: int | None = Field(default=None, gt=0)
    minutes: int | None = Field(default=None, gt=0)
    effort_guidance: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_prescription_fields(self):
        if self.prescription_type == "sets_reps":
            if None in (
                self.sets,
                self.repetitions_min,
                self.repetitions_max,
            ):
                raise ValueError(
                    "Strength prescriptions require sets and repetitions."
                )
            if self.minutes is not None:
                raise ValueError(
                    "Strength prescriptions cannot include minutes."
                )
            if self.repetitions_min > self.repetitions_max:
                raise ValueError(
                    "Minimum repetitions cannot exceed maximum repetitions."
                )
        elif any(
            value is not None
            for value in (
                self.sets,
                self.repetitions_min,
                self.repetitions_max,
            )
        ):
            raise ValueError(
                "Timed prescriptions cannot include sets or repetitions."
            )
        elif self.minutes is None:
            raise ValueError("Timed prescriptions require minutes.")
        return self


class DailyPlan(BaseModel):
    """One ordered day in a seven-day plan."""

    model_config = ConfigDict(strict=True, extra="forbid")

    day: Weekday
    day_type: DayType
    focus: SessionFocus
    warm_up: TimedGuidance | None
    exercises: list[ExerciseEntry]
    cool_down: TimedGuidance | None
    total_minutes: int = Field(ge=0)
    intensity: PreferredIntensity | None
    equipment: list[str]
    explanation: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_day_structure(self):
        if self.day_type == "rest":
            if self.exercises or self.total_minutes != 0:
                raise ValueError(
                    "Rest days cannot contain exercises or workout minutes."
                )
            if self.warm_up is not None or self.cool_down is not None:
                raise ValueError(
                    "Rest days cannot contain a warm-up or cool-down."
                )
        elif not self.exercises or self.total_minutes == 0:
            raise ValueError(
                "Workout and recovery days require exercises and minutes."
            )
        return self


class WeeklyTotals(BaseModel):
    """Calculated totals for one generated week."""

    model_config = ConfigDict(strict=True, extra="forbid")

    workout_days: int = Field(ge=0)
    total_planned_minutes: int = Field(ge=0)
    strength_sessions: int = Field(ge=0)
    cardio_sessions: int = Field(ge=0)
    mobility_sessions: int = Field(ge=0)


class WeeklyPlanResult(BaseModel):
    """Validated result returned by the complete planning workflow."""

    model_config = ConfigDict(strict=True, extra="forbid")

    status: PlanStatus
    message: str = Field(min_length=1)
    weekly_summary: str | None
    warnings: list[str]
    days: list[DailyPlan]
    totals: WeeklyTotals | None
    reasons: list[str]

    @model_validator(mode="after")
    def validate_result_structure(self):
        if self.status == "generated":
            if len(self.days) != 7 or self.totals is None:
                raise ValueError(
                    "Generated results require seven days and weekly totals."
                )
            if self.weekly_summary is None:
                raise ValueError(
                    "Generated results require a weekly summary."
                )
        elif self.days or self.totals is not None:
            raise ValueError(
                "Blocked or confirmation results cannot contain a plan."
            )
        return self


class DayExplanation(BaseModel):
    """One AI-written explanation for a planned activity day."""

    model_config = ConfigDict(strict=True, extra="forbid")

    day: Weekday
    explanation: str = Field(min_length=1)


class PlanExplanation(BaseModel):
    """Schema-constrained AI explanation of an existing plan."""

    model_config = ConfigDict(strict=True, extra="forbid")

    weekly_summary: str = Field(min_length=1)
    day_explanations: list[DayExplanation] = Field(min_length=1)

    @field_validator("day_explanations")
    @classmethod
    def reject_duplicate_explanation_days(cls, explanations):
        days = [item.day for item in explanations]
        if len(days) != len(set(days)):
            raise ValueError("Each day can have only one explanation.")
        return explanations


class FeedbackInterpretation(BaseModel):
    """Schema-constrained signals extracted from free-text feedback."""

    model_config = ConfigDict(strict=True, extra="forbid")

    difficulty: FeedbackDifficulty
    missed_days: list[Weekday]
    disliked_exercises: list[str]
    requested_focus: RequestedFocus | None
    requires_safety_rescreening: bool

    @field_validator("missed_days", "disliked_exercises")
    @classmethod
    def reject_duplicate_feedback_values(cls, values):
        if len(values) != len(set(values)):
            raise ValueError("Duplicate feedback values are not allowed.")
        return values

    @field_validator("disliked_exercises")
    @classmethod
    def reject_blank_exercise_identifiers(cls, exercise_ids):
        if any(not exercise_id.strip() for exercise_id in exercise_ids):
            raise ValueError("Exercise identifiers cannot be blank.")
        return exercise_ids
