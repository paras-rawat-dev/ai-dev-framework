# Observability Standard

## Required

User-facing, scheduled, or integration-heavy workflows need enough visibility to debug failures.

Include:

- structured logs for major state transitions
- clear error messages at system boundaries
- correlation/request identifiers where available
- metrics for performance-sensitive paths
- audit trail for compliance-sensitive actions

## AI Assistant Rules

- Do not swallow exceptions without an explicit reason.
- Prefer actionable errors over generic failures.
- For RCA, identify what evidence would have made diagnosis faster.

