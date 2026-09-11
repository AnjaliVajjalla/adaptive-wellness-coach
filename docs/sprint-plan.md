# Sprint Plan

## Sprint 0: Project Foundation

**Goal:** Create a professional, traceable foundation before application development begins.

**Planned work:**

- Initialize the local Git repository
- Create and connect the private GitHub repository
- Create the initial repository documentation
- Create the GitHub Project board
- Create the initial backlog as GitHub Issues
- Make and push the first reviewed commit

**Acceptance criteria:**

- Local repository uses the `main` branch
- GitHub remote is connected as `origin`
- README accurately states the current project status
- Product, safety, sprint, tracking, decision, and evaluation documents exist
- Project board and initial issues exist
- Initial commit is visible on GitHub

### Sprint 0 Review

**Review status:** Complete. Acceptance criteria were verified and the final documentation updates were committed and pushed.

**Completed work:**

- Initialized the local repository on `main` and connected `origin`
- Created and pushed the initial documentation commit
- Created the core product, safety, planning, tracking, decision, and evaluation documents
- Created Sprint Board, Backlog, and Roadmap project views
- Added Sprint, Priority, and Category fields
- Configured new project items to begin in Backlog
- Created GitHub Issue #1 to review and close Sprint 0

### Sprint 0 Retrospective

**What went well:**

- Defined the product scope and safety boundaries before writing application code
- Connected documentation, Git history, GitHub Issues, and the project board
- Used acceptance criteria to make completion measurable

**What can improve:**

- Update the project tracker immediately after completing setup tasks
- Create issues before beginning work so the board reflects the full workflow
- Keep new issues in Backlog until they are selected and ready to start

**Actions for Sprint 1:**

- Update the tracker at the end of each work session
- Move an issue only when its real work status changes
- Review and test each small feature before marking it Done

## Sprint 1: Fictional User Profile and Validation

**Goal:** Build and test a structured fictional user profile with required-field validation.

**Acceptance criteria:**

- Profile fields and allowed values are documented
- One complete fictional profile can be represented
- Missing required fields are detected
- Invalid values are rejected with understandable messages
- Automated tests cover complete, incomplete, and invalid profiles

### Sprint 1 Review

**Review status:** Complete. All acceptance criteria were verified locally.

**Completed work:**

- Documented the fictional user-profile fields and allowed values
- Implemented deterministic required-field, allowed-value, type, duplicate, and cross-field validation
- Added 36 automated pytest scenarios for valid and invalid profile behavior
- Built and ran the test suite inside a Docker image using Python 3.12 and pytest 9.1.1
- Confirmed all 36 scenarios pass

### Sprint 1 Retrospective

**What went well:**

- Defined the profile contract before implementing validation
- Kept safety screening separate from general profile validation
- Added automated coverage before beginning the next feature
- Used Docker to make the test environment reproducible

**What can improve:**

- Review test coverage gaps before declaring a feature complete
- Keep learning explanations focused on their project and interview purpose

**Actions for Sprint 2:**

- Define safety categories and expected outcomes before implementing rules
- Test every documented exclusion category
- Continue running the official test suite inside Docker

## Sprint 2: Safety Screening

**Goal:** Create and test deterministic safety-screening rules.

**Acceptance criteria:**

- Safe, unsafe, and incomplete synthetic profiles are defined
- Excluded situations are detected before plan generation
- Unsafe profiles receive an appropriate refusal and escalation message
- Incomplete profiles request the missing information
- Automated tests cover every documented exclusion category

### Sprint 2 Review

**Review status:** Complete. All acceptance criteria were verified inside Docker, pushed to GitHub, and tracked through closed Issues #5 through #8.

**Completed work:**

- Documented seven required Boolean safety inputs and three screening outcomes
- Implemented deterministic safety screening separately from profile validation
- Prioritized known exclusions over missing answers
- Added 26 automated scenarios covering safe, unsafe, incomplete, invalid, malformed, multiple-exclusion, and rule-priority behavior
- Confirmed all 62 project scenarios pass inside Docker using Python 3.12 and pytest 9.1.1
- Ran focused tests and investigated a controlled failure using a temporary read-only bind mount

### Sprint 2 Retrospective

**What went well:**

- Approved the safety contract before implementing the rules
- Tested every documented exclusion with parameterized scenarios
- Used Docker for full-suite, focused, and controlled-failure runs

**What can improve:**

- Continue distinguishing image creation from container execution
- Read actual and expected pytest values before deciding whether code or a test is wrong

**Actions for Sprint 3:**

- Require both successful profile validation and a safe screening result before plan generation
- Define the plan output contract before implementation
- Continue using Docker as the official test environment

## Sprint 3: Basic Weekly Plan Foundation

**Status:** Complete

**Goal:** Generate a basic weekly workout plan from a safe, validated fictional profile.

**Approved design:** See the [Weekly Workout-Plan Specification](weekly-plan-spec.md).

**Acceptance criteria:**

- Output structure is documented
- Plan respects available days, session duration, equipment, and experience level
- Weekly totals are calculated with reliable Python functions
- Plans are not generated for invalid or unsafe profiles
- Automated tests cover representative safe profiles and constraint failures

**Review:** The completed workflow combines validation, safety screening, recovery-aware scheduling, exercise filtering and ranking, structured prescriptions, explanations, and weekly totals. All 122 project tests pass in Docker.

**Retrospective:** Small deterministic helpers made the planner explainable and easier to test. Future evaluation should expand the exercise library and identify where additional variety is useful.

## Sprint 4: Structured API Service

**Status:** Complete

**Goal:** Expose the validated weekly-plan workflow through strict data models and HTTP endpoints.

**Acceptance criteria:**

- Pydantic models validate the complete request and response structures
- The existing deterministic planner remains the source of planning decisions
- FastAPI provides health and plan-generation endpoints
- Invalid requests return clear validation errors
- Valid unsafe requests remain blocked before plan generation
- The application and full test suite run inside Docker

**Review:** The service now validates API input and output with Pydantic, connects those contracts to the existing planner through a typed service layer, and exposes `GET /health` and `POST /plans`. Swagger testing confirmed generated, blocked, and invalid outcomes. All 144 project tests pass in Docker.

**Retrospective:** Keeping the API, service, and deterministic planning layers separate made each responsibility easier to test. Automatic API documentation also made response behavior visible without building a web interface prematurely.

## Sprint 5: AI-Assisted Explanations and Feedback

**Status:** Complete

**Goal:** Add focused AI behavior without allowing the model to control planning or safety decisions.

**Acceptance criteria:**

- Plan explanations and feedback signals use strict Pydantic contracts
- OpenAI configuration remains outside source control
- Plan explanations cannot alter the underlying plan
- Feedback interpretation cannot invent accepted exercise identifiers
- AI and configuration failures have tested safe behavior
- Automated tests never make paid external requests

**Review:** The API now exposes guarded endpoints for plan explanations and feedback interpretation. Live fictional inputs produced structured outputs, and a live rest-day mismatch led to an additional deterministic business-rule check. All 173 project tests pass in Docker.

**Retrospective:** A response can satisfy its JSON schema while still violating a product rule. Combining structured outputs, Pydantic validation, deterministic business checks, and isolated test doubles provides stronger protection than any one layer alone.

## Sprint 6: Evaluation Dataset and Measured Improvement

**Status:** Complete

**Goal:** Measure AI feedback interpretation with reproducible fictional cases
and use failure analysis to improve the evaluation system.

**Acceptance criteria:**

- A synthetic evaluation dataset covers every feedback output field
- Expected and actual structured outputs are compared deterministically
- Whole-case and per-field accuracy are reported
- Automated evaluation tests cannot make paid API calls
- Live results, failures, corrections, and limitations are documented accurately

**Review:** A 20-case fictional JSONL dataset, local runner, and deterministic
grader now measure feedback interpretation. The harder live baseline scored
95% whole-case accuracy. The only failure came from an ambiguous reference
label, so the case wording was clarified instead of changing the AI prompt. A
targeted live retest passed every field. All 179 project tests pass in Docker.

**Retrospective:** Evaluation quality depends on the reference answers as well
as the model. A failed comparison should be reviewed before changing a prompt,
because an ambiguous label can make reasonable model behavior look incorrect.

## Sprint 7: AI Observability and Cost Tracking

**Status:** Complete

**Goal:** Make AI-assisted behavior traceable and measure its reliability,
latency, token usage, and estimated cost without recording private input text.

**Acceptance criteria:**

- Every attempted AI request records a unique application trace ID and outcome
- Successful responses record the OpenAI response ID and available token usage
- Trace logs exclude API keys and user-provided feedback text
- Token prices are configurable and tied to the selected model
- Multiple traces can be summarized by status, success rate, average and P95 latency, total tokens, and estimated cost
- Evaluation reports combine output-quality and operational measurements

**Review:** Structured traces now record safe operational metadata for plan
explanations and feedback interpretation. A live fictional request completed in
5.13 seconds using 514 total tokens with an estimated cost of $0.000503. This
is one verification sample, not a performance average. The evaluation runner
now combines quality and observability summaries. All 188 project tests pass
in Docker.

**Retrospective:** A correct AI result is not sufficient evidence of production
quality. Reliability, tail latency, token usage, and cost must also be visible.
Keeping pricing configurable avoids presenting stale estimates as billing
facts, and privacy-conscious traces support debugging without storing raw
feedback.

## Sprint 8: Docker and Continuous Integration

**Status:** Complete

**Goal:** Create separate test and production images, strengthen production
container behavior, and automatically run the complete test suite on GitHub.

**Acceptance criteria:**

- A shared Docker base supports separate test and production targets
- The test image contains pytest, tests, and evaluation files
- The production image excludes test-only files and dependencies
- The production application runs as a non-root user
- Docker checks whether the running API responds through its health endpoint
- GitHub Actions builds the test image and runs all tests for pushes and pull requests to `main`
- The first GitHub-hosted workflow run passes

**Review:** The test and production targets build successfully. The production
container runs as `app:app`, Docker reports it as healthy, and all 188 tests
pass in a temporary local test container. The first GitHub Actions run also
built the Docker test image and passed the complete suite in 26 seconds.

**Retrospective:** Using the same Docker test target locally and in GitHub
Actions reduces environment differences. Separating production from testing
also keeps development tools out of the runtime image, while a non-root user
and health check provide practical runtime safeguards.

## Sprint 9: User Intake and Weekly-Plan Web Interface

**Status:** Complete and verified

**Goal:** Let a user enter a fictional profile, complete safety screening,
review the answers, and view the generated seven-day plan in a responsive web
interface.

**Acceptance criteria:**

- The interface collects every approved profile and safety field
- Required and conflicting selections receive clear browser feedback
- Challenging beginner or sedentary selections require confirmation
- The browser sends a structured request to the existing FastAPI endpoint
- Generated plans display weekly totals, seven days, and exercise prescriptions
- Blocked safety outcomes do not display a workout plan
- The interface runs from the production Docker application

**Review:** The responsive HTML, CSS, and JavaScript interface now guides the
user through Profile, Safety, and Review steps. Browser checks verified valid
plan generation, blocked safety behavior, selection-conflict feedback, and the
challenging-intensity confirmation. All 190 project tests pass in Docker.

**Retrospective:** Keeping the browser focused on input collection and display
allowed the existing FastAPI, Pydantic, safety, and deterministic planning
layers to remain the source of truth. Client-side checks improve usability,
while backend validation still protects the application boundary.

**Post-sprint refinement:** Added a required workout-structure choice so users
can request full body, upper/lower, or push/pull/legs rather than having the
goal-based mix silently choose full body. Incompatible requests use an
explicit full-body fallback warning. All 198 tests pass in Docker.

## Later Planning

Sprint 10 will deploy the application and complete the public README,
architecture diagram, measured results, and portfolio presentation.
