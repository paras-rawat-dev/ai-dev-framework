# Project Charter: [Project Name]

## Objective

[What are we building and why?]

## Users

[Who uses it? What are their main workflows?]

## Non-Goals

- [What this project will not do yet]

## Selected Stack Packs

- [enterprise/constitution.md]
- [stacks/<stack>.md]

## UI Member

Primary UI member: [shadcn/ui, Mantine, HeroUI, MUI, Ant Design, Chakra, Radix, Tremor, native]

Reason:

[Why this member fits the product shape]

Not allowed:

- [Libraries or patterns not to mix]

## Data Sources

| Source | Owner | Sensitivity | Freshness | Notes |
| --- | --- | --- | --- | --- |
| [source] | [owner] | [low/medium/high] | [expectation] | [notes] |

## Quality Gates

```bash
[build command]
[lint command]
[test command]
```

## Performance / Reliability Targets

- [Target and how it will be measured]

## AI Workflow

- Agents must read this charter before implementation.
- Agents must challenge scope that conflicts with non-goals.
- Agents must run or report quality gates.
- Independent review is required for [RCA/security/data migrations/cross-component wiring].

## Definition Of Done

- [ ] Core user story works.
- [ ] Required checks pass.
- [ ] UI states are covered where applicable.
- [ ] Docs updated only for durable changes.
- [ ] Known risks are documented.

