# Project Tracker

Last updated: September 10, 2026, Sprint 4 completion

## Completed

- Defined the product concept and target user
- Approved the first-version scope
- Defined initial safety boundaries
- Created the private GitHub repository
- Initialized local Git on the `main` branch
- Connected the local repository to the GitHub remote
- Created and pushed the initial documentation commit
- Created the GitHub Project with Sprint Board, Backlog, and Roadmap views
- Added Sprint, Priority, and Category project fields
- Configured new project items to begin in Backlog
- Created GitHub Issue #1 for the Sprint 0 foundation review
- Completed the Sprint 0 review and retrospective
- Committed and pushed the final Sprint 0 documentation updates
- Completed and closed the Sprint 0 foundation-review issue
- Created Sprint 1 Issues #2 through #4
- Approved the Sprint 1 profile fields and allowed values
- Approved the fictional user-profile specification
- Completed the Sprint 1 fictional user-profile specification
- Implemented required-field, allowed-value, and cross-field profile validation
- Manually verified representative valid and invalid profiles
- Added automated pytest coverage for valid, missing, invalid, malformed, duplicate, and conflicting profile inputs
- Added a Docker test image and excluded unnecessary local files from Docker builds
- Verified all 36 profile-validation scenarios inside Docker with Python 3.12 and pytest 9.1.1
- Reviewed a controlled pytest failure and distinguished an incorrect test expectation from an application defect
- Defined and approved seven Boolean safety-screening inputs
- Defined safe, unsafe, and incomplete screening outcomes
- Implemented deterministic safety screening separately from profile validation
- Added 26 automated safety-screening scenarios covering every exclusion, missing and invalid answers, malformed input, and rule priority
- Verified all 62 project scenarios inside Docker with Python 3.12 and pytest 9.1.1
- Used a read-only bind mount for a temporary controlled-failure investigation without changing the repository or image
- Committed and pushed the Sprint 2 implementation, tests, and documentation
- Completed and closed Sprint 2 Issues #5 through #8
- Defined and approved the Sprint 3 weekly workout-plan output contract
- Created Sprint 3 Issues #9 through #13
- Built a reviewed library of 27 cardio, bodyweight, strength, and mobility activities
- Added structured exercise metadata for equipment, experience, goals, preferences, prescriptions, and source traceability
- Added 6 library-integrity tests and verified all 69 project tests in Docker
- Implemented deterministic workout-day scheduling with recovery-aware spacing
- Implemented goal and experience-based session mixes, preference rotation, and flexible-focus resolution
- Implemented exercise filtering, preference ranking, movement-pattern balance, and returning-user exercise rotation
- Added structured strength, cardio, and mobility prescriptions within the selected session duration
- Integrated profile validation, safety screening, intensity confirmation, seven-day output, rest days, explanations, and weekly totals
- Verified all 122 project tests inside Docker with Python 3.12 and pytest 9.1.1
- Reviewed a complete fictional plan and completed the Sprint 3 review and retrospective
- Added strict Pydantic input and output models for profiles, safety answers, requests, plan days, exercises, totals, and results
- Added a typed service boundary between the API models and the deterministic weekly-plan generator
- Added FastAPI health and plan-generation endpoints with automatic OpenAPI documentation
- Updated Docker to run the API by default while supporting test-command overrides
- Tested generated, blocked, and invalid API outcomes through Swagger UI
- Verified all 144 project tests inside Docker with Python 3.12 and pytest 9.1.1

## Currently Learning

- Git and GitHub fundamentals
- Professional sprint organization
- Markdown documentation
- Structured data fields and validation rules
- Pytest scenarios, assertions, fixtures, and parameterized testing
- Docker images, containers, Dockerfiles, layers, caching, and containerized testing
- Docker command overrides, temporary containers, and bind mounts
- Comparing pytest's actual and expected results during failure investigation
- Designing controlled, source-traceable data for deterministic selection
- Combining small deterministic helpers into one gated planning workflow
- Defining strict Pydantic data contracts and nested structured outputs
- Connecting validated application logic to FastAPI endpoints
- Distinguishing HTTP validation errors from valid blocked business outcomes

## Current Status

- Sprints 0 through 4 are complete; Sprint 5 planning is next

## Tested

- Local Git initialization
- GitHub remote configuration
- Initial commit visibility on GitHub
- Automatic addition of repository issues to the project board
- Default Backlog status for newly added project items
- Complete fictional profile passes manual validation
- Missing required field returns a clear error
- Invalid allowed value returns a clear error
- Conflicting preferences return a clear error
- Incorrect multi-select data returns a clear error without crashing
- All 36 automated profile-validation scenarios pass inside Docker
- A single named pytest scenario can be isolated and run inside Docker
- The Docker test image rebuild reuses unchanged dependency and source layers
- Safe answers return `safe` and allow the future workflow to continue
- Every documented exclusion returns `unsafe` with refusal and escalation language
- Missing, invalid, and malformed safety answers return `incomplete`
- A known safety exclusion takes priority over a missing answer
- All 62 automated project scenarios pass inside Docker
- A selected test file can override the Dockerfile's default full-suite command
- A temporary read-only bind mount can add a debugging test without modifying the image
- Exercise records use unique identifiers and complete, approved metadata
- Every approved goal, activity preference, and equipment category is represented
- All 69 automated project tests pass inside Docker
- Invalid, unsafe, and unconfirmed challenging profiles cannot reach plan generation
- Generated plans contain seven ordered days and respect availability, experience, equipment, preferences, dislikes, and duration
- Beginner strength sessions repeat for consistency; returning-user sessions rotate exercises
- All 122 automated project tests pass inside Docker
- Pydantic rejects missing, extra, incorrectly typed, duplicate, and conflicting request data
- FastAPI returns `422` for invalid requests, `200` with `blocked` for valid unsafe requests, and `200` with `generated` for valid safe requests
- Generated API responses satisfy the nested weekly-plan output contract
- All 144 automated project tests pass inside Docker

## Blocked

- None

## Planned

- Plan Sprint 5 AI-assisted explanations and feedback interpretation

## Explicitly Out of Scope

- Application code during Sprint 0
- Real user health information
- Medical advice and excluded safety situations
- Meal planning and calorie estimates in the initial version
- Web or mobile interfaces before the Python workflow is tested
