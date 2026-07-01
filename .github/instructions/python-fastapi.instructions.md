---
applyTo: "**/*.py"
---

For Python/FastAPI work, keep business logic out of route handlers, validate boundaries with typed models, use migrations for schema changes, and prefer existing project helpers before new abstractions.

For bug fixes, trace shared functions and callers before patching the visible symptom.

Run project-defined Python checks from `TESTING.md` or explain why they could not run.

