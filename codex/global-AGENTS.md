# Personal Codex Defaults

Use `/Users/parasrawat/Documents/ponytail` as my AI-assisted development framework whenever it exists.

## Default Behavior

- Keep my prompting style comfortable; do not require me to restate the framework.
- If my request is underspecified, either make a conservative framework-aligned decision or ask the smallest number of blocking questions.
- Push back when I may be wrong, uninformed, over-scoping, adding avoidable dependencies, skipping verification, or asking for a solution that conflicts with project rules.
- Prefer build-vs-buy and reuse before custom platforms.
- Prefer small, correctness-first slices over broad speculative architecture.
- Use Ponytail-style restraint: read the affected flow first, then prefer YAGNI, existing helpers, standard library, native platform features, installed dependencies, and the smallest correct implementation.
- Do not simplify away security, data handling, accessibility, root-cause analysis, or required checks.

## New Project Default

When I ask to start a new project or app, first run the framework kickoff mentally and prompt me only for missing blocking inputs:

1. Product objective and primary users.
2. Selected stack packs.
3. UI member when UI is involved.
4. Explicit non-goals.
5. Data sources and sensitivity.
6. Required checks or deployment constraints.

Create or suggest:

- `PROJECT_CHARTER.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `AI_WORKFLOW.md`
- `AGENTS.md`

Do not begin major implementation until the project contract is clear enough to keep future agent work consistent.

## Existing Project Default

When I ask for changes in an existing repo:

- Inspect whether `AGENTS.md`, `PROJECT_CHARTER.md`, `ARCHITECTURE.md`, `TESTING.md`, and `AI_WORKFLOW.md` exist.
- If missing, offer to create minimal versions from current repo reality.
- Do not invent architecture; document what exists and list gaps separately.
- Read existing patterns before adding files, dependencies, abstractions, or UI systems.

## Non-Trivial Change Loop

For non-trivial code changes:

```text
read project instructions
inspect current code
trace affected flow
challenge unnecessary scope
plan the smallest useful slice
implement
run required checks
review against project, stack, and enterprise rules
summarize verification and risks
```

## Independent Analysis

Use subagents or independent review passes for:

- RCA
- migrations
- security/auth/secrets/data-loss risk
- cross-component wiring
- large UI rewrites
- agent/RAG evaluation
- unclear architecture decisions

Independent review should return concise findings, not raw exploratory logs.

## UI Defaults

Before UI implementation, identify the project UI member from `stacks/ui-react.md`.

Default recommendations:

- custom polished Tailwind app: shadcn/ui + Radix
- fast internal operational tool: Mantine
- analytics/dashboard views: Tremor as a secondary member
- dense enterprise admin: Ant Design or MUI
- design-system primitives: Radix, React Aria, Base UI, or Ark UI

Do not mix full UI systems unless the project tech lead explicitly accepts the tradeoff.

## Personal Style

- Be direct and pragmatic.
- Challenge architecture and scope when needed.
- Surface missing, conflicting, or uncertain facts.
- Keep implementation boring unless the product genuinely needs novelty.
- If answer quality matters, verify with evidence; API success is not enough.

