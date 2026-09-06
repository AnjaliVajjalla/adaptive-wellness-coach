# Exercise Library Specification

## Purpose

The exercise library is a small, reviewed set of activities that the weekly
plan generator may select. The generator filters these records instead of
asking an AI model to invent exercises.

## Exercise Record

Each exercise contains:

- A stable exercise identifier and readable name
- Activity type and movement pattern
- Equipment that can satisfy the exercise requirement
- Optional equipment that may improve comfort
- Supported experience levels and goals
- Matching user-preference tags
- A `sets_reps` or `minutes` prescription type
- One or more source identifiers

An empty `equipment_options` value means the exercise requires no equipment.
When several options are listed, any one of them can satisfy the requirement.

## Selection Rules

- Only records compatible with the fictional profile's equipment and
  experience level may be selected.
- A disliked activity removes every record carrying that preference tag.
- Preferred activities receive priority among the remaining records.
- Neutral records may be used to create a balanced plan.
- `Full gym access` satisfies every supported equipment requirement.
- The library provides exercise choices, not medical advice, exact weights,
  calorie estimates, or predicted outcomes.

## Source Review

The first library uses general activity and exercise references from:

- The U.S. Centers for Disease Control and Prevention
- The United Kingdom National Health Service
- The American Council on Exercise exercise library

Source titles and URLs are stored in `src/exercise_library.py` so exercise
records remain traceable during review and evaluation.

## Development Data Rule

The library contains general exercise metadata only. It does not contain or
derive from a real person's workout history, weights, or health information.
