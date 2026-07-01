# Testing Plan: [Project Name]

## Required Commands

```bash
[lint]
[unit tests]
[integration tests]
[build]
```

## Test Levels

| Level | Required For | Tool |
| --- | --- | --- |
| unit | pure logic, parsers, validators | [tool] |
| integration | APIs, DB, external boundaries | [tool] |
| UI/browser | changed user flows | [tool/manual] |
| eval | agent/RAG generated output | [tool/artifact] |

## Minimum Verification By Change Type

- API route: endpoint/integration test.
- DB migration: migration test or local apply verification.
- UI flow: screenshot or browser verification.
- LLM/agent behavior: fixture, trace, and qualitative review.
- Bug fix: regression check for root cause.

## AI Assistant Rules

- Do not claim tests pass unless they were run.
- If a check cannot run, explain the blocker and risk.
- Prefer one meaningful regression test over broad shallow coverage.

