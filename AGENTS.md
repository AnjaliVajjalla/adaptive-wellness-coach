# Adaptive Wellness Coach Project Instructions

This repository is dedicated only to designing, learning, building, testing, and explaining the Adaptive Wellness Coach.

## Product Scope

- Serve generally healthy people who are beginners or returning to exercise.
- Start with structured weekly workout planning only.
- Personalize plans using goals, experience, schedule, equipment, and preferences.
- Add feedback-based plan adjustment only after the basic workflow is tested.
- Use fictional or synthetic user data during development and evaluation.

## Safety Boundaries

- This is a general wellness project, not a medical product.
- Do not diagnose, treat, or manage medical conditions.
- Do not create injury-rehabilitation plans.
- Do not provide plans for pregnancy or postpartum situations, eating disorders, or complex health conditions.
- Do not provide extreme weight-loss recommendations, therapeutic diets, supplement advice, or medication advice.
- Escalate excluded or higher-risk situations to an appropriate qualified professional.
- Keep calculations transparent and label estimates clearly.

## Development Rules

- Teach every unfamiliar technical concept before using it in project code.
- Let Anjali make meaningful predictions, modifications, and explanations.
- Treat general Python syntax as known unless Anjali asks for a refresher.
- Focus Anjali's hands-on work on debugging, code review, testing assumptions, and explaining results rather than typing routine boilerplate.
- Do not write the entire project at once.
- Use reliable Python functions for calculations, validation, and safety rules.
- Use an LLM only where language understanding or flexible reasoning adds value.
- Test every important feature before calling it complete.
- Do not add a web interface before the underlying Python workflow works.
- Use synthetic data only and never commit secrets or private health information.
- Keep documentation synchronized with verified behavior.

## Project Workflow

- Work in small sprints with a defined goal and acceptance criteria.
- Track work through GitHub Issues and GitHub Projects.
- Tell Anjali when a GitHub Project item should move and name its destination status; Anjali will make routine board changes in the browser.
- Use meaningful Git commits after a coherent piece of work is reviewed.
- Update the decision log when a major product, safety, or technical choice changes.
- Update the project tracker at the end of each work session.
- Keep unverified metrics, unfinished features, and unsupported claims out of the README.

## Routine Task Procedure

- Handle repetitive, low-risk project maintenance for Anjali when it can be completed directly.
- Ask only for input that would materially affect the result.
- Briefly state the proposed scope and obtain approval before making material updates.
- After approval, complete the approved documentation, formatting, file setup, tracker synchronization, and similar mechanical work without asking for approval for every small substep.
- Verify the completed work and clearly report what changed and what still requires Anjali's review.
- Do not automatically commit, push, close issues, publish, delete, or make other external or difficult-to-reverse changes unless that action was explicitly included in the approved scope.
- Continue using the guided teaching sequence for unfamiliar application code and technical concepts. Routine-task automation does not replace Anjali's hands-on learning.

## Current Sprint Sequence

1. Sprint 0: Repository, project board, backlog, and core documentation
2. Sprint 1: Fictional user-profile structure and required-field validation
3. Sprint 2: Safety screening for safe, unsafe, and incomplete profiles
4. Sprint 3: Basic weekly workout-plan generation from a safe, validated profile
