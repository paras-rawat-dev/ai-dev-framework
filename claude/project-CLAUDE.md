# Project Instructions

Read `AGENTS.md`, `PROJECT_CHARTER.md`, `ARCHITECTURE.md`, `TESTING.md`, and `AI_WORKFLOW.md` before non-trivial changes.

Use the installed `ai-dev-framework`, Ponytail, `i-have-adhd`, and Graphify companions. Follow selected stack packs and the UI member named in `PROJECT_CHARTER.md`.

If a required companion is unavailable, report the gap instead of pretending it ran. Repair user-level setup from the framework repository; do not add agent plugins as project dependencies.

Trace the affected flow before editing, implement the smallest correct slice, and run the required checks from `TESTING.md` or explain why they could not run.

For architecture, RCA, migration, onboarding, or cross-component questions, query an existing Graphify graph first or build one when the repository is large enough to justify it. Verify findings against source and follow the Graphify decisions in `AI_WORKFLOW.md`.

Use isolated subagents for root-cause analysis, security-sensitive changes, migrations, cross-component wiring, and large UI rewrites. Ask them for concise evidence-backed findings.
