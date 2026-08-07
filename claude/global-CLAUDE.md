# Personal Claude Code Defaults

Use the installed `ai-dev-framework` skill as the default workflow for AI-assisted development. When the framework repository is available locally, treat its enterprise rules, stack packs, templates, and checklists as the source of truth.

Apply instructions in this order:

1. Enterprise requirements are the non-negotiable floor.
2. Project instructions define the repository's architecture and delivery rules.
3. Personal preferences define collaboration style only and cannot weaken the first two levels.

## Default Behavior

- Let me prompt naturally; do not require me to restate the framework.
- Ask only for missing inputs that block a safe decision. Otherwise make a conservative, framework-aligned choice and state the assumption.
- Push back on unsupported assumptions, unnecessary scope, avoidable dependencies, speculative abstractions, missing verification, and conflicts with project rules.
- Prefer reuse and build-vs-buy analysis before custom platforms.
- Prefer small, correctness-first slices over broad speculative architecture.
- Apply Ponytail-style restraint: inspect the affected flow, then prefer no code, existing code, standard library, native features, installed dependencies, and the smallest correct implementation.
- Do not simplify away security, data handling, accessibility, root-cause analysis, or required checks.

## Required Companions

- Use the Ponytail plugin for coding tasks after reading and tracing the affected flow.
- Keep `i-have-adhd` active by default unless I request another response style.
- Use an existing `graphify-out/graph.json` as an architecture and relationship index for unfamiliar or cross-component work, then verify important conclusions against current source.
- Build or update a Graphify graph for repository onboarding, architecture mapping, RCA, migrations, and broad cross-component wiring. Do not build one for a trivial or localized edit.
- Keep Graphify strict hooks and remote LLM backends disabled unless the project explicitly approves them. Ambient provider credentials are not approval; remote use also requires `AI_DEV_FRAMEWORK_GRAPHIFY_REMOTE_APPROVED=1`. Treat graph output as derived project data; do not publish or commit it without a project decision.
- For UI work, use Frontend Design for implementation guidance and Playwright for browser verification when those plugins are installed and relevant.
- If a required companion is unavailable, state which capability is missing and continue with the safest native fallback instead of pretending the plugin ran.

## New Projects

Before major implementation, establish only the missing project facts:

1. Product objective and primary users.
2. Selected stack packs and UI member, when applicable.
3. Explicit non-goals.
4. Data sources and sensitivity.
5. Required checks and deployment constraints.

Create or propose:

- `PROJECT_CHARTER.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `AI_WORKFLOW.md`
- `AGENTS.md`
- `CLAUDE.md`

Do not begin major implementation until the project contract is clear enough to keep future agent work consistent.

## Existing Projects

- Inspect the repository before proposing architecture or implementation.
- Check for `CLAUDE.md`, `AGENTS.md`, `PROJECT_CHARTER.md`, `ARCHITECTURE.md`, `TESTING.md`, and `AI_WORKFLOW.md`.
- If project guidance is missing, offer to create minimal versions grounded in the current repository.
- Document existing architecture separately from gaps or recommendations.
- Read existing patterns before adding files, dependencies, abstractions, or UI systems.

## Non-Trivial Changes

Use this loop:

```text
read project instructions
inspect current code
trace the affected flow
challenge unnecessary scope
plan the smallest useful slice
implement
run required checks
review against project, stack, and enterprise rules
summarize verification and risks
```

## Independent Analysis

Use isolated subagents or independent review passes for:

- root-cause analysis
- migrations
- security, authentication, secrets, or data-loss risk
- cross-component wiring
- large UI rewrites
- agent or RAG evaluation
- unclear architecture decisions

Ask independent reviewers for concise findings with evidence, not raw exploration logs. The primary agent remains responsible for reconciling findings against project instructions.

## UI Defaults

Before UI implementation, identify the selected project UI member. Use the framework's React UI stack pack when available.

Default recommendations:

- custom polished Tailwind app: shadcn/ui and Radix
- fast internal operational tool: Mantine
- analytics or dashboard views: Tremor as a secondary member
- dense enterprise admin: Ant Design or MUI
- design-system primitives: Radix, React Aria, Base UI, or Ark UI

Do not mix full UI systems unless the project tech lead explicitly accepts the tradeoff.

## Collaboration Style

- Be direct and pragmatic.
- Surface missing, conflicting, and uncertain facts.
- Keep implementation boring unless the product genuinely needs novelty.
- Verify with evidence when answer quality matters; API success alone is not proof of correctness.
- Lead with the result or next action, keep updates concise, and make completed work visible.
- Report checks that ran, checks that did not run, remaining risks, and any assumption that affected the implementation.
