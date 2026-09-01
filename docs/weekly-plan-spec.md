# Weekly Workout-Plan Specification

## Purpose

This specification defines the first deterministic weekly workout-plan output.
It applies only to fictional profiles that pass general profile validation and
safety screening.

The first version uses a small approved exercise library. It does not ask an AI
model to invent exercises, recommend exact weights, or estimate calories.

## Result Statuses

### Generated

- The fictional profile is valid.
- Safety screening returns `safe`.
- Any required intensity warning has been confirmed.
- The result includes a complete seven-day plan and weekly totals.

### Confirmation Required

- The fictional user is a complete beginner or sedentary.
- The selected preferred intensity is `Challenging`.
- The result includes a warning but no workout plan.
- The user's selected intensity is preserved; generation may continue only
  after a separate confirmation is supplied.
- A confirmed challenging plan still uses exercises appropriate for the
  fictional user's experience level.

### Blocked

- General profile validation fails, or safety screening does not return `safe`.
- The result includes the existing validation or safety explanation.
- No workout plan is generated.

## Top-Level Output

The plan result contains:

- `status`: `generated`, `confirmation_required`, or `blocked`
- `message`: a concise explanation of the result
- `weekly_summary`: a brief explanation of the week's structure
- `warnings`: any planning warnings that require attention
- `days`: seven ordered daily entries from Monday through Sunday
- `totals`: calculated weekly totals

## Daily Entry

Every day contains:

- `day`: weekday name
- `day_type`: `workout`, `recovery`, or `rest`
- `focus`: the day's main workout or recovery focus
- `warm_up`: a short timed warm-up when applicable
- `exercises`: the approved exercises scheduled for the day
- `cool_down`: a short timed cool-down when applicable
- `total_minutes`: the complete planned session duration
- `intensity`: the selected planning intensity when applicable
- `equipment`: the equipment required for the day
- `explanation`: one sentence connecting the day to the profile and weekly plan

Rest days use an empty exercise list and do not invent workout instructions.

## Exercise Entry

Every exercise contains:

- `name`: approved exercise name
- `activity_type`: strength, bodyweight, cardio, or mobility
- `equipment`: required equipment
- `prescription_type`: `sets_reps` or `minutes`
- `sets` and `reps`: used for strength and bodyweight exercises
- `minutes`: used for walking, cycling, jogging, mobility, warm-ups, and
  cool-downs
- `effort_guidance`: a brief instruction such as choosing a manageable effort

The generator does not recommend an exact weight.

## Session-Duration Rules

The total session duration includes the warm-up, main exercises, and cool-down.

| Selected duration | Main exercises |
| --- | --- |
| 15 minutes | 2 to 3 |
| 30 minutes | 3 to 4 |
| 45 minutes | 4 to 5 |
| 60 minutes | 5 to 6 |

## Weekly Frequency Rules

- Complete beginners receive no more than three workout days.
- Users returning to exercise receive no more than four workout days.
- The generator never schedules a workout on an unavailable day.
- If fewer days are available, the generator uses only available days.
- The generator avoids more than two consecutive workout days when the
  available schedule permits.
- Remaining days are labeled as rest or light recovery days.

Available days are scheduling options, not a requirement to schedule a workout
on every selected day.

## Personalization Rules

- The primary goal determines the main weekly workout mix.
- Additional goals make smaller adjustments without replacing the primary
  goal.
- Preferred activities are prioritized.
- Disliked activities are never selected.
- Neutral activities may be used when needed for a balanced plan.
- Only equipment listed as available may be selected.
- Intensity is interpreted relative to the fictional user's experience level.
- Each workout day includes one brief explanation of why it was selected.

## Weekly Totals

Reliable Python functions calculate:

- Number of workout days
- Total planned workout minutes
- Number of strength sessions
- Number of cardio sessions
- Number of mobility or recovery sessions

The first version does not calculate calories, lifting volume, or predicted
results.

## Plan-Generation Gate

The workflow order is:

1. Validate the fictional profile.
2. Run deterministic safety screening.
3. Check whether intensity confirmation is required.
4. Generate the seven-day plan only when every gate permits it.

## Development Data Rule

Use fictional or synthetic examples only. Do not copy or commit a real person's
routine, weights, health information, or workout history.
