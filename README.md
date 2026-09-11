# Adaptive Wellness Coach

A personalized AI wellness-planning tool that creates and adapts weekly workout plans using structured feedback and safety rules.

## Project Status

Sprints 0 through 9 are complete locally. The project validates fictional profiles, applies safety screening, generates deterministic seven-day workout plans, provides guarded AI-assisted features through FastAPI, measures feedback interpretation, records privacy-conscious operational metrics, and includes a responsive web interface for profile intake, safety screening, review, and plan display.

The current suite contains 190 passing scenarios covering profile validation, safety screening, exercise-library integrity, scheduling, personalization, prescriptions, structured data contracts, AI failure handling, evaluation, observability, service integration, API behavior, and static-interface delivery.

## Product Overview

The Adaptive Wellness Coach is intended for generally healthy people who are complete beginners or returning to exercise. It will create realistic weekly workout plans based on goals, experience, availability, equipment, and preferences.

The first version focuses on workout planning. Meal ideas, calorie estimates, and wearable integrations remain outside the current scope.

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
- Sprint 4: Pydantic data contracts, structured outputs, and FastAPI endpoints
- Sprint 5: AI-assisted explanations and feedback interpretation
- Sprint 6: Synthetic evaluation dataset, deterministic grading, and measured baseline
- Sprint 7: AI tracing, reliability metrics, latency, token usage, and estimated cost
- Sprint 8: Multi-stage Docker images, runtime safeguards, and automated GitHub Actions testing
- Sprint 9: Responsive user intake, safety, review, and weekly-plan web interface
- Sprint 10: Deployment and portfolio presentation

See [Sprint Plan](docs/sprint-plan.md) for acceptance criteria.

## Run the Application

With Docker Desktop running:

```bash
docker build -t adaptive-wellness-coach:api .
docker run --rm -p 8000:8000 --env-file .env adaptive-wellness-coach:api
```

Open `http://127.0.0.1:8000` to use the web application, or open
`http://127.0.0.1:8000/docs` to use the interactive API documentation.

Run the test suite with:

```bash
docker build --target test -t adaptive-wellness-coach:test .
docker run --rm adaptive-wellness-coach:test
```

Latest verified result: 190 tests passed inside Linux with Python 3.12 and pytest 9.1.1.

## Documentation

- [Product Brief](docs/product-brief.md)
- [Safety Boundaries](docs/safety-boundaries.md)
- [Safety-Screening Specification](docs/safety-screening-spec.md)
- [Weekly Workout-Plan Specification](docs/weekly-plan-spec.md)
- [Exercise Library Specification](docs/exercise-library-spec.md)
- [AI Explanation and Feedback Specification](docs/ai-feature-spec.md)
- [Sprint Plan](docs/sprint-plan.md)
- [Project Tracker](docs/project-tracker.md)
- [Decision Log](docs/decision-log.md)
- [Evaluation Plan](docs/evaluation-plan.md)
- [Feedback Evaluation Baseline](evals/results/feedback-baseline.md)
- [Fictional User Profile Specification](docs/user-profile-spec.md)

## Development Note

The repository is being built in small, tested checkpoints. Continuous integration and the local web interface are active and verified. Deployment will be documented only after it is implemented and verified.
