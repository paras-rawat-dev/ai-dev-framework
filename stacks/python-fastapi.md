# Stack Pack: Python + FastAPI

## Applies When

Use for Python backend APIs built with FastAPI or closely related ASGI services.

## Default Project Shape

```text
app/
  api/          route modules and request/response models
  services/     business logic
  repositories/ data access only when useful and current
  models/       database/domain models
  core/         config, logging, auth helpers
tests/
  unit/
  integration/
  contract/
```

## Required Practices

- Validate request and response boundaries with typed models.
- Keep business logic out of route handlers.
- Use migrations for database schema changes.
- Use parameterized database access.
- Keep environment configuration explicit and documented.
- Return structured errors for expected user/API failures.

## Quality Gates

Projects should define exact commands. Common defaults:

```bash
ruff check .
pytest
```

## AI Assistant Rules

- Inspect existing route, service, and test patterns before adding files.
- Do not introduce repository or service abstractions unless there is a current reason.
- For bugs, trace all callers of the affected service/function before patching.
- Prefer stdlib and existing dependencies over new packages.
- If changing API behavior, update contract docs or OpenAPI expectations.

## Common Anti-Patterns

- Business logic inside FastAPI route functions.
- New dependency for date parsing, HTTP calls, or config when existing project tools cover it.
- Catching broad exceptions and returning generic 500s without logging.
- Creating generic base repositories with only one implementation.

