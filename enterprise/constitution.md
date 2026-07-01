# Enterprise Engineering Constitution

This file is the minimum engineering floor for AI-assisted development. It applies to every project unless a stricter project rule exists.

## Principles

1. **Correctness before speed**: AI-generated code must be verified with the smallest meaningful check that proves the behavior.
2. **Security is not optional**: do not remove validation, authorization, auditability, or secret handling to reduce code.
3. **Data boundaries are explicit**: data sources, owners, retention expectations, and sensitive fields must be named.
4. **Dependencies are justified**: new production dependencies require a reason and an owner.
5. **Observability follows risk**: user-facing or scheduled workflows need logs, error visibility, and enough context for RCA.
6. **Accessibility is part of UI quality**: interactive UI must preserve keyboard navigation, visible focus, labels, and usable contrast.
7. **Small is good only when it is correct**: prefer minimal code, but never at the cost of root cause, safety, or maintainability.

## AI-Assisted Development Rule

Agents may draft, edit, review, and test code. Humans remain accountable for architecture, data access, security posture, and release decisions.

## Conflict Order

When guidance conflicts, apply the most specific stricter rule:

```text
enterprise floor < stack pack < project rule < current task instruction
```

Personal preferences cannot weaken any required rule.

