# Project Tracker

Last updated: September 1, 2026, Sprint 2 local verification

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

## Currently Learning

- Git and GitHub fundamentals
- Professional sprint organization
- Markdown documentation
- Structured data fields and validation rules
- Pytest scenarios, assertions, fixtures, and parameterized testing
- Docker images, containers, Dockerfiles, layers, caching, and containerized testing
- Docker command overrides, temporary containers, and bind mounts
- Comparing pytest's actual and expected results during failure investigation

## Current Status

- Sprint 2 acceptance criteria are verified locally; final GitHub synchronization is pending

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

## Blocked

- None

## Planned

- Complete the final Sprint 2 documentation review and GitHub sync
- Begin Sprint 3 workout-plan output design after Sprint 2 closes

## Explicitly Out of Scope

- Application code during Sprint 0
- Real user health information
- Medical advice and excluded safety situations
- Meal planning and calorie estimates in the initial version
- Web or mobile interfaces before the Python workflow is tested
