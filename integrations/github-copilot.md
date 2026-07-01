# GitHub Copilot Integration

GitHub Copilot supports repository-wide instructions, path-specific instructions, organization instructions, and personal instructions depending on the surface.

Official docs:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/reference/custom-instructions-support
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-organization-instructions

## Enterprise Level

Use GitHub organization custom instructions for rules that apply across repositories. Keep them short and stable.

Good candidates:

- security baseline
- dependency approval policy
- testing expectation
- code review priorities

## Project Level

Recommended files:

```text
AGENTS.md
.github/copilot-instructions.md
.github/instructions/python.instructions.md
.github/instructions/react.instructions.md
PROJECT_CHARTER.md
ARCHITECTURE.md
TESTING.md
AI_WORKFLOW.md
```

Use `.github/copilot-instructions.md` for repository-wide guidance. Use `.github/instructions/*.instructions.md` with `applyTo` frontmatter for path-specific guidance.

Example:

```md
---
applyTo: "frontend/src/**/*.tsx"
---

Follow the selected UI member in PROJECT_CHARTER.md.
Preserve keyboard navigation, labels, focus states, loading states, and error states.
Run `npm run build` after UI changes when practical.
```

## Personal Level

Use personal Copilot instructions where your IDE or GitHub surface supports them. For Copilot CLI, local instructions can live at:

```text
$HOME/.copilot/copilot-instructions.md
```

Personal instructions should tune style, not weaken project rules.

## Important Notes

- Root `AGENTS.md` is useful because some Copilot surfaces treat it as agent guidance.
- If both `AGENTS.md` and `.github/copilot-instructions.md` exist, keep them consistent.
- Avoid copying long enterprise docs into every repo. Link to them and summarize only the rules that affect coding.
