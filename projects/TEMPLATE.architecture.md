# Architecture: [Project Name]

## System Context

[Describe the product boundary, users, and external systems.]

## Components

| Component | Responsibility | Owner | Notes |
| --- | --- | --- | --- |
| [component] | [responsibility] | [owner] | [notes] |

## Data Flow

```text
[user/system] -> [component] -> [data source] -> [response/output]
```

## Key Decisions

| Decision | Reason | Alternative Rejected |
| --- | --- | --- |
| [decision] | [reason] | [alternative] |

## Constraints

- [Security, data, performance, cost, compliance, deployment]

## AI Assistant Notes

- Read these boundaries before adding new components.
- Do not introduce new layers unless they support a current component boundary.
- For cross-component wiring, use independent review before finalizing.

