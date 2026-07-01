# Security Standard

## Required

- Validate input at trust boundaries.
- Keep authentication and authorization checks explicit.
- Do not log secrets, tokens, credentials, or sensitive personal data.
- Do not read `.env`, credentials, or secret directories unless the task explicitly requires it and the user has approved the access path.
- Prefer parameterized database access.
- Treat file uploads, deserialization, shell execution, and external callbacks as high-risk surfaces.

## AI Assistant Rules

- Do not remove security checks to simplify code.
- If a task touches auth, secrets, payments, personal data, or access control, call that out in the final response.
- For security-sensitive changes, recommend a separate review pass.

