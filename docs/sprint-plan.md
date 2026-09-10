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

## Later Planning

After Sprint 5, build a dedicated evaluation dataset, then add observability, CI/CD, a simple web interface, deployment, and public presentation.
