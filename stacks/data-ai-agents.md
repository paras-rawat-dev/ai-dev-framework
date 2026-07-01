# Stack Pack: Data, AI, and Agent Systems

## Applies When

Use for projects involving data pipelines, retrieval, LLM calls, agent orchestration, evaluation, or generated outputs.

## Required Practices

- Separate source evidence from generated interpretation.
- Keep prompts, schemas, and eval fixtures versioned.
- Log enough trace information to reproduce failures.
- Define what "good" means before optimizing.
- Use small sampled runs before expensive full runs.
- Do not treat API success as answer quality.

## Quality Gates

Project-specific, but should include:

```bash
[unit tests for parsers/schemas]
[small eval fixture]
[trace or artifact inspection command]
```

## AI Assistant Rules

- Surface missing, conflicting, or uncertain information explicitly.
- Use independent analysis lanes for RCA or high-risk reasoning.
- Preserve net-new discovery when combining graph, database, and web evidence.
- Do not invent data mappings or business semantics.
- Keep secrets in local env files or configured secret stores, not prompts or docs.

## Common Anti-Patterns

- Judging quality only from whether the API returned 200.
- Letting graph-only retrieval suppress net-new discovery.
- Stuffing all agent roles into one prompt.
- Omitting trace artifacts that explain why an answer was produced.

