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

## Sprint 1: Fictional User Profile and Validation

**Goal:** Build and test a structured fictional user profile with required-field validation.

**Acceptance criteria:**

- Profile fields and allowed values are documented
- One complete fictional profile can be represented
- Missing required fields are detected
- Invalid values are rejected with understandable messages
- Automated tests cover complete, incomplete, and invalid profiles

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

AI tool use, natural-language explanations, feedback-based adaptation, broader evaluation, interface work, and public presentation will be planned only after Sprint 3 is tested.
