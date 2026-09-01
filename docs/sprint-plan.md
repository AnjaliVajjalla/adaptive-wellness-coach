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

## Sprint 3: Basic Weekly Plan Foundation

**Goal:** Generate a basic weekly workout plan from a safe, validated fictional profile.

**Acceptance criteria:**

- Output structure is documented
- Plan respects available days, session duration, equipment, and experience level
- Weekly totals are calculated with reliable Python functions
- Plans are not generated for invalid or unsafe profiles
- Automated tests cover representative safe profiles and constraint failures

## Later Planning

After Sprint 3, plan the FastAPI service, vector retrieval, Dockerized application runtime, Azure deployment, security hardening, CI/CD, monitoring, AI-assisted explanations, feedback-based adaptation, broader evaluation, and public presentation.
