# Project Tracker

Last updated: September 1, 2026, Sprint 1 completion

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

## Currently Learning

- Git and GitHub fundamentals
- Professional sprint organization
- Markdown documentation
- Structured data fields and validation rules
- Pytest scenarios, assertions, fixtures, and parameterized testing
- Docker images, containers, Dockerfiles, layers, caching, and containerized testing

## Current Status

- Sprint 1 is complete and Sprint 2 safety-screening design is next

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

## Blocked

- None

## Planned

- Define safe, unsafe, and incomplete fictional profiles for Sprint 2
- Implement deterministic safety screening before plan generation

## Explicitly Out of Scope

- Application code during Sprint 0
- Real user health information
- Medical advice and excluded safety situations
- Meal planning and calorie estimates in the initial version
- Web or mobile interfaces before the Python workflow is tested
