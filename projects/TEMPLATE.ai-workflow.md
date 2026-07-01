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

