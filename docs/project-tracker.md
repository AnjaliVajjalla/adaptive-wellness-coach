# Project Tracker

Last updated: September 11, 2026, Sprint 9 local completion

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
- Defined strict Pydantic contracts for plan explanations and feedback signals
- Added the OpenAI Responses API provider with environment-based secret configuration
- Added guarded FastAPI endpoints for plan explanations and feedback interpretation
- Kept planning decisions deterministic and limited AI to language explanation and extraction
- Added deterministic checks for unknown exercise identifiers and explanation-day mismatches
- Verified live structured responses for plan explanation and fictional workout feedback
- Identified a live output that included unwanted rest days and added a tested fallback rule
- Isolated automated tests from real credentials so test runs cannot make paid API calls
- Reached the Sprint 5 checkpoint with 173 passing project tests in Docker
- Built a 20-case fictional JSONL dataset for structured feedback evaluation
- Added deterministic whole-case and per-field grading
- Added a local evaluation runner with explicit expected-versus-actual results
- Measured a 95% whole-case live baseline across the harder 20-case dataset
- Identified an ambiguous reference label instead of incorrectly changing the AI prompt
- Clarified the evaluation case and passed a targeted live retest
- Recorded measured results, methodology, and limitations in a baseline report
- Verified all 179 project tests inside Docker with Python 3.12 and pytest 9.1.1
- Added privacy-conscious structured traces for AI requests
- Recorded application trace IDs, OpenAI response IDs, outcomes, latency, and token usage
- Added configurable model-specific cost estimation with separate cached-input pricing
- Added aggregate request counts, status counts, success rate, average and P95 latency, total tokens, and estimated cost
- Integrated operational metrics into the feedback evaluation report
- Verified one live fictional request at 5.13 seconds, 514 tokens, and an estimated cost of $0.000503
- Verified all 188 project tests inside Docker with Python 3.12 and pytest 9.1.1
- Split the Dockerfile into shared, test, and production build stages
- Kept pytest, tests, and evaluation files out of the production image
- Configured the production container to run as the non-root `app` user
- Added a production health check against the FastAPI `/health` endpoint
- Added a GitHub Actions workflow that builds the Docker test target and runs the complete suite
- Locally verified the production container as running and healthy
- Passed the first GitHub Actions Docker test run in 26 seconds
- Built a responsive three-step web interface using HTML, CSS, and vanilla JavaScript
- Added guided profile intake, safety screening, answer review, and seven-day plan display
- Connected the browser to `POST /plans` through the FastAPI application
- Added immediate browser validation for missing and conflicting selections
- Added the existing challenging-intensity confirmation to the browser workflow
- Served the interface and static assets from FastAPI inside the production Docker image
- Verified generated, blocked, conflicting-selection, and confirmation-required browser paths
- Verified all 190 project tests inside Docker with Python 3.12 and pytest 9.1.1

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
- Separating schema validation from application-specific AI business rules
- Connecting the OpenAI Responses API through a replaceable provider boundary
- Preventing secrets and paid external calls from entering automated tests
- Separating schema validation, unit testing, and semantic AI evaluation
- Designing synthetic reference cases and reviewing label ambiguity
- Measuring whole-case and per-field accuracy
- Using failure analysis to decide whether the model, prompt, or dataset should change
- Distinguishing individual request traces from aggregate operational metrics
- Measuring average and P95 latency, token usage, and estimated API cost
- Designing logs that support debugging without storing secrets or raw feedback
- Separating test and production concerns with multi-stage Docker builds
- Distinguishing a running process from a healthy application
- Automating reproducible Docker tests with GitHub Actions continuous integration
- Separating frontend behavior from backend validation and planning logic
- Converting browser form values into a typed JSON API request
- Using client-side validation for immediate feedback while retaining backend validation as the final authority
- Connecting a responsive interface to FastAPI and rendering structured plan responses

## Current Status

- Sprints 0 through 9 are complete locally
- Sprint 9 is ready for commit, push, and GitHub Actions verification
- Sprint 10 deployment and portfolio presentation are next

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
- AI explanations and feedback interpretations satisfy strict Pydantic contracts
- Missing configuration and external AI failures use safe, explicit failure behavior
- Explanations with extra or missing activity days trigger the deterministic fallback
- Unknown exercise identifiers cannot reach later adjustment logic
- Live fictional feedback was correctly classified without directly changing a plan
- The Sprint 5 checkpoint contained 173 passing automated tests in Docker
- The JSONL evaluation dataset loads with 20 unique, schema-valid cases
- The grader detects exact field mismatches while ignoring irrelevant list order
- The evaluation runner reports whole-case and per-field accuracy
- The harder live feedback baseline scored 95% before label clarification
- The corrected ambiguous case passed a targeted live retest
- All 179 automated project tests pass inside Docker
- AI traces omit API keys and raw user feedback while recording safe request metadata
- Cost estimates use configurable prices only when the configured pricing model matches the requested model
- Synthetic trace aggregation reports reliability, average and P95 latency, tokens, and cost
- The evaluation runner combines quality and operational summaries
- All 188 automated project tests pass inside Docker
- The production image excludes pytest and the `/app/tests` directory
- The production container runs with fixed non-root user and group IDs
- Docker reports the running production API as healthy
- The first GitHub Actions workflow run built the test image and passed all 188 tests
- FastAPI serves the web interface and its CSS and JavaScript assets
- Valid browser inputs produce a structured API request and render seven plan days
- Conflicting equipment and activity selections are stopped before navigation
- An unsafe safety answer returns a blocked result with no workout-day cards
- A challenging selection for a beginner or sedentary profile requires explicit confirmation
- All 190 automated project tests pass inside Docker

## Blocked

- None

## Planned

- Commit, push, and verify Sprint 9 through GitHub Actions
- Deploy the application and finish the portfolio presentation in Sprint 10

## Explicitly Out of Scope

- Application code during Sprint 0
- Real user health information
- Medical advice and excluded safety situations
- Meal planning and calorie estimates in the initial version
- Web or mobile interfaces before the Python workflow is tested
