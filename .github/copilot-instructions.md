# GitHub Copilot Instructions

Use [AGENTS.md](../AGENTS.md) as the canonical project guidance for this repository.

For teams adopting this framework in GitHub Copilot:

- Put repository-wide guidance in `.github/copilot-instructions.md`.
- Put path-specific guidance in `.github/instructions/*.instructions.md`.
- Keep this file concise and link to project docs for detailed procedures.
- Use the installed `ai-dev-framework`, Ponytail, `i-have-adhd`, and Graphify Agent Skills.
- When configuring this framework, run `python3 scripts/install_framework.py --agent github-copilot`; do not report setup complete if a required skill or tool fails.
- Apply Ponytail after tracing the affected flow; prefer the smallest correct implementation.
- Use Graphify for justified architecture, RCA, migration, onboarding, and cross-component work. Skip graph generation for localized edits, verify findings against source, and follow project data-handling rules for graph output.
- Lead with the result or next action, number multi-step work, and report verification and remaining risks.
- Select the project UI member before adding UI dependencies and use existing browser tests for visual verification.

See [integrations/github-copilot.md](../integrations/github-copilot.md) for the full adoption guide.
