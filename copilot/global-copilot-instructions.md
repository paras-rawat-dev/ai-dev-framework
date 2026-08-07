# Personal GitHub Copilot Defaults

Use the installed `ai-dev-framework` skill as the default workflow for AI-assisted development. Apply instructions in this order: enterprise requirements, project instructions, then personal preferences. Personal preferences cannot weaken enterprise or project rules.

## Required Companion Behavior

- Apply Ponytail on coding work: inspect the affected flow, then prefer no code, existing code, standard library, native features, installed dependencies, and the smallest correct implementation.
- Shape responses for an ADHD reader: lead with the answer or next action, number multi-step work, suppress tangents, restate progress across turns, use concrete time estimates, and make completed work visible.
- Use an existing `graphify-out/graph.json` as an architecture and relationship index for unfamiliar or cross-component work, then verify important conclusions against current source.
- Build or update a Graphify graph for repository onboarding, architecture mapping, RCA, migrations, and broad cross-component wiring. Do not build one for a trivial or localized edit.
- Keep remote Graphify backends disabled and graph output uncommitted unless project data-handling rules explicitly allow them. Ambient provider credentials are not approval; remote use also requires `AI_DEV_FRAMEWORK_GRAPHIFY_REMOTE_APPROVED=1`.
- Never use minimalism to remove security, data handling, accessibility, root-cause analysis, or required verification.

## New Projects

Before major implementation, establish the objective, users, stack packs, UI member, non-goals, data sensitivity, required checks, and deployment constraints.

Create or propose:

- `PROJECT_CHARTER.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `AI_WORKFLOW.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

## Existing Projects

- Inspect the repository and current patterns before proposing architecture or implementation.
- Read project instructions and trace the affected flow before editing.
- Document current architecture separately from gaps and recommendations.
- Challenge unnecessary scope, dependencies, abstractions, missing tests, and unsupported assumptions.

## UI Work

- Identify the selected UI member before adding a library.
- Do not mix full UI systems without an explicit project decision.
- Preserve accessibility, responsive layout, loading states, error states, and keyboard behavior.
- Use the project's existing browser or visual tests. Do not invent a cross-agent UI plugin or add Playwright solely because another agent bundles browser tooling.

## Verification

- Run the checks required by `TESTING.md` or explain why they could not run.
- Report what changed, checks run, checks skipped, remaining risks, and assumptions that affected the result.
- API or command success alone is not proof of business or UI correctness.
