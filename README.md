# Adaptive Wellness Coach

A personalized AI wellness-planning tool that creates and adapts weekly workout plans using structured feedback and safety rules.

## Project Status

Sprints 1 and 2 are complete. Fictional profile validation and deterministic safety screening are implemented, tested in Docker, documented, and pushed to GitHub.

The current suite contains 62 passing scenarios: 36 profile-validation scenarios and 26 safety-screening scenarios. Workout-plan generation is not implemented yet.

## Product Overview

The Adaptive Wellness Coach is intended for generally healthy people who are complete beginners or returning to exercise. It will create realistic weekly workout plans based on goals, experience, availability, equipment, and preferences.

The first version will focus on workout planning. Meal ideas, calorie estimates, wearable integrations, and a web interface are outside the initial scope.

## Planned Core Features

- Structured fictional user profiles
- Required-field validation
- Safety screening and appropriate refusals
- Beginner and returning-user planning modes
- Seven-day workout-plan generation
- Clear explanations for recommendations
- Feedback-based plan adjustments
- Synthetic testing and documented evaluation

## Safety Position

This is a general wellness-planning project, not a medical product. It will not diagnose conditions, provide medical advice, create rehabilitation plans, or support excluded higher-risk situations.

See [Safety Boundaries](docs/safety-boundaries.md) and the [Safety-Screening Specification](docs/safety-screening-spec.md) for the working safety rules.

## Current Roadmap

- Sprint 0: Repository, project board, backlog, and documentation
- Sprint 1: Fictional user-profile structure and validation
- Sprint 2: Safety-screening rules and tests
- Sprint 3: Basic weekly workout-plan foundation and tests

See [Sprint Plan](docs/sprint-plan.md) for acceptance criteria.

## Run the Validation Tests

With Docker Desktop running:

```bash
docker build -t adaptive-wellness-coach:test .
docker run --rm adaptive-wellness-coach:test
```

Latest verified result: 62 tests passed inside Linux with Python 3.12 and pytest 9.1.1.

## Documentation

- [Product Brief](docs/product-brief.md)
- [Safety Boundaries](docs/safety-boundaries.md)
- [Safety-Screening Specification](docs/safety-screening-spec.md)
- [Weekly Workout-Plan Specification](docs/weekly-plan-spec.md)
- [Sprint Plan](docs/sprint-plan.md)
- [Project Tracker](docs/project-tracker.md)
- [Decision Log](docs/decision-log.md)
- [Evaluation Plan](docs/evaluation-plan.md)
- [Fictional User Profile Specification](docs/user-profile-spec.md)

## Development Note

The repository is being built in small, tested checkpoints. FastAPI, vector retrieval, Azure deployment, CI/CD, and monitoring are later phases and will be documented as implemented only after they are verified.
