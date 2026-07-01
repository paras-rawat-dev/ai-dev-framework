# Testing Baseline

Every non-trivial change needs a verification path.

## Minimum Checks

- Pure logic: unit test or assert-based self-check.
- API behavior: endpoint or integration test.
- Database schema: migration and rollback/forward validation where applicable.
- UI behavior: browser/manual verification for changed flows.
- Agent/RAG output: fixture, trace, or evaluation artifact with source evidence.

## AI Assistant Rules

- State which checks were run.
- If checks were not run, state why.
- Do not add broad test frameworks for trivial one-line changes.
- Do not claim coverage from tests that do not exercise the changed behavior.

