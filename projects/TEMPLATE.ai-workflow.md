# AI Workflow: [Project Name]

## Agent Startup

Agents should read, in order:

1. `AGENTS.md` or tool-specific equivalent
2. `PROJECT_CHARTER.md`
3. `ARCHITECTURE.md`
4. `TESTING.md`
5. relevant stack packs

## Default Work Loop

```text
inspect current code
trace affected flow
challenge unnecessary scope
plan small slice
edit
run checks
review diff
summarize risk and verification
```

## Required Independent Analysis

Use a separate agent or independent review pass for:

- RCA
- auth/security changes
- migrations
- data-loss risk
- cross-component wiring
- large UI rewrites

## Repository Intelligence

- Query an existing `graphify-out/graph.json` first for architecture, RCA, migration, onboarding, and cross-component questions; verify important findings against current source.
- Build or update the graph only when repository breadth justifies the cost. Skip it for trivial or localized edits.
- Graph output policy: local/generated only; keep `graphify-out/` ignored unless the tech lead approves version control.
- Remote semantic backends: [disabled, or approved provider and data boundary]
- Remote execution flag: set `AI_DEV_FRAMEWORK_GRAPHIFY_REMOTE_APPROVED=1` only after that approval; ambient API keys alone do not authorize transmission.
- Strict hooks: [disabled by default, or approved project exception]

## Pushback Rules

Agents should push back when:

- the requested scope conflicts with project non-goals
- a new dependency duplicates existing capability
- an abstraction has only one implementation
- a UI library is added before the UI member is selected
- a fix patches one symptom without tracing shared callers

## Output Expectations

Final responses should include:

- what changed
- checks run
- risks or follow-up work
- any durable rule that should be promoted
