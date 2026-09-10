# Decision Log

This file records major product, safety, and technical decisions. Git history records the exact wording changes.

| ID | Decision | Reason | Status |
| --- | --- | --- | --- |
| D-001 | Serve both complete beginners and people returning to exercise. | These groups share a need for realistic routines but require different starting difficulty. | Approved |
| D-002 | Focus the initial version on workout planning only. | This keeps the first version useful, testable, and safer while protecting the core personalization goal. | Approved |
| D-003 | Prioritize AI tool use, personalization, and product design as learning goals. | These skills align with the intended early-career AI, product, solutions, and analyst roles. | Approved |
| D-004 | Use deterministic Python for validation, calculations, and safety rules. | These tasks require consistent and testable behavior. | Approved |
| D-005 | Use fictional or synthetic profiles during development. | This avoids collecting private health information and supports repeatable evaluation. | Approved |
| D-006 | Use GitHub Issues and GitHub Projects for work tracking. | This keeps planning connected to repository changes and builds workplace-relevant workflow skills. | Approved |
| D-007 | Plan later AI and feedback features only after the basic validated workflow works. | This limits complexity and allows later design to use evidence from early testing. | Approved |
| D-008 | Do not collect age or use age as an eligibility field in the initial profile. | Keep the first-version intake focused on information directly used for workout personalization. | Approved |
| D-009 | Use controlled-choice user fields and a system-generated identifier for fictional profiles. | This supports consistent validation and keeps test data separate from real identities. | Approved |
| D-010 | Use Docker as the official reproducible test environment. | This keeps the Python version, dependencies, code, and test command consistent across local development, CI/CD, and later deployment work. | Approved |
| D-011 | Use seven required Boolean safety inputs with `safe`, `unsafe`, and `incomplete` outcomes; a known exclusion takes priority over missing answers. | This creates conservative, explainable, and independently testable behavior without collecting medical details. | Approved |
| D-012 | Produce a moderately structured seven-day plan from a small approved exercise library, with activity-appropriate prescriptions, brief explanations, and calculated weekly totals. | This creates useful, explainable, and testable output without inventing exercises, exact weights, calorie estimates, or excessive detail. | Approved |
| D-013 | Treat available days as scheduling options and limit complete beginners to three workout days and returning users to four, with recovery spacing when possible. | This prevents availability from automatically becoming an excessive workout schedule. | Approved |
| D-014 | Preserve a challenging-intensity selection but require confirmation when the fictional user is a complete beginner or sedentary. | This respects user choice while adding a clear warning and keeping exercise selection appropriate to experience. | Approved |
| D-015 | Add `Bicycle or stationary bike` as an equipment option and treat `Full gym access` as access to every supported equipment category. | This lets the generator determine when a cycling preference can be fulfilled without requiring users to list common gym equipment separately. | Approved |
| D-016 | Use goal-based session mixes, recovery-aware scheduling, preference rotation, movement-pattern balance, conservative prescriptions, beginner repetition, and returning-user exercise rotation. | These deterministic rules make plans personalized, explainable, and testable while keeping the first version appropriately limited. | Approved |

## How to Update This Log

Add a new row when a major decision is introduced or changed. Do not silently rewrite an earlier decision. Mark it superseded and add the replacement decision as a new row.
