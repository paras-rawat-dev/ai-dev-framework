# Data Handling Standard

## Required

- Name every source system used by a feature.
- Identify owner, freshness expectations, and sensitive fields when known.
- Prefer typed schemas at service boundaries.
- Keep transformations reproducible.
- Avoid silent data drops; log or report rejected records.

## AI Assistant Rules

- Do not invent source semantics.
- Mark unknown mappings as unknown.
- If sample data is used, state sample size and limitation.
- For analytics or agent/RAG systems, separate source evidence from generated interpretation.

