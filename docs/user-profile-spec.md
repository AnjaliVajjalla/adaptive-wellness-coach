# Fictional User Profile Specification

## Purpose

This specification defines the fictional profile information used to build and test user-profile validation. It does not represent a user account and must not contain real personal or health information.

## Fields

| Field | Source | Required | Rule |
| --- | --- | --- | --- |
| Profile identifier | System | Yes | Automatically generate a fictional label such as `profile_001` |
| Primary goal | User | Yes | Select exactly one approved goal |
| Additional goals | User | No | Select zero or more approved goals other than the primary goal |
| Experience level | User | Yes | Select one approved experience level |
| Current activity level | User | Yes | Select one approved activity level |
| Available workout days | User | Yes | Select one or more unique weekdays |
| Session duration | User | Yes | Select one approved duration |
| Workout structure | User | Yes | Select one approved strength-training structure |
| Available equipment | User | Yes | Select one or more approved equipment options |
| Preferred activities | User | Yes | Select one or more approved preference options |
| Disliked activities | User | Yes | Select one or more approved dislike options |
| Preferred intensity | User | Yes | Select one approved intensity |

## Allowed Values

### Fitness Goals

- Start exercising regularly
- Improve overall fitness
- Get stronger
- Increase stamina
- Improve flexibility and mobility

### Experience Level

- Complete beginner
- Returning to exercise

### Current Activity Level

- Sedentary
- Light
- Moderate
- Heavy

### Available Workout Days

- Monday
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday
- Sunday

### Session Duration

- 15 minutes
- 30 minutes
- 45 minutes
- 60 minutes

### Workout Structure

- Let the coach choose
- Full body
- Upper/lower
- Push/pull/legs

The structure applies to strength days. Upper/lower requires at least two
strength days, while push/pull/legs requires at least three. When the weekly
mix does not contain enough strength days, the generator uses full-body
strength and returns a visible warning.

### Available Equipment

- No equipment, bodyweight only
- Exercise mat
- Resistance bands
- Dumbbells
- Kettlebell
- Bicycle or stationary bike
- Full gym access

### Preferred and Disliked Activities

- Walking
- Jogging or running
- Cycling
- Strength training
- Bodyweight workouts
- Yoga or mobility

Preferred activities may also use `No preference`. Disliked activities may also use `No disliked activities`.

### Preferred Intensity

- Gentle
- Moderate
- Challenging
- No preference

## Validation Rules

- Every required field must be present.
- Every selected value must match an allowed value.
- Multi-select fields must not contain duplicate values.
- The primary goal must not be repeated as an additional goal.
- `No equipment, bodyweight only` cannot be combined with another equipment option.
- `No preference` and `No disliked activities` must be selected alone in their respective fields.
- The same activity cannot appear in both preferred and disliked activities.
- The system, not the user, creates the profile identifier.

## Complete Fictional Example

| Field | Example value |
| --- | --- |
| Profile identifier | `profile_001` |
| Primary goal | Get stronger |
| Additional goals | Improve overall fitness |
| Experience level | Complete beginner |
| Current activity level | Light |
| Available workout days | Monday, Wednesday, Friday |
| Session duration | 30 minutes |
| Workout structure | Upper/lower |
| Available equipment | Exercise mat, dumbbells |
| Preferred activities | Strength training, bodyweight workouts |
| Disliked activities | Jogging or running |
| Preferred intensity | Moderate
