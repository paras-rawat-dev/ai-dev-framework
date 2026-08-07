# Claude Code Integration

Claude Code supports persistent instructions with `CLAUDE.md`, project rules, skills, hooks, and subagents.

Official docs:

- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/sub-agents

## Enterprise Level

Use organization-managed `CLAUDE.md` only for rules that apply everywhere, such as security and data handling. Keep it short.

## Project Level

Recommended files:

```text
CLAUDE.md
.claude/CLAUDE.md
.claude/rules/*.md
.claude/skills/<workflow>/SKILL.md
PROJECT_CHARTER.md
ARCHITECTURE.md
TESTING.md
AI_WORKFLOW.md
```

Use:

- `CLAUDE.md` for stable project facts and conventions.
- `.claude/rules/` for path-specific guidance.
- `.claude/skills/` for repeated multi-step procedures.
- hooks for mechanical enforcement, not static documentation.

## Personal Level

Use:

```text
~/.claude/CLAUDE.md
```

Start from [claude/global-CLAUDE.md](../claude/global-CLAUDE.md). If `~/.claude/CLAUDE.md` already exists, merge the framework defaults into it instead of overwriting personal instructions.

Install the reusable framework skill for all local Claude Code projects:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/ai-dev-framework" ~/.claude/skills/ai-dev-framework
```

Run the command from the framework repository. If the destination already exists, update it deliberately rather than replacing it blindly.

Personal instructions should cover how you want Claude to collaborate. They cannot weaken enterprise or project requirements.

## Automatic Setup

Run from this framework repository:

```bash
python3 scripts/install_framework.py --agent claude
```

This safely merges the global Claude defaults, installs the framework skill, installs pinned Ponytail and `i-have-adhd` plugins, enables the ADHD SessionStart behavior, installs the pinned Graphify CLI and Claude skill, and installs Frontend Design and Playwright from Claude's official marketplace.

See [required framework companions](../docs/companion-plugins.md) for reviewed revisions and UI-tool boundaries.

## Suggested Project `CLAUDE.md`

```md
# Project Instructions

Read PROJECT_CHARTER.md, ARCHITECTURE.md, TESTING.md, and AI_WORKFLOW.md before non-trivial changes.

Follow the selected stack packs named in PROJECT_CHARTER.md.

Run the required checks from TESTING.md after implementation or explain why they could not run.
```

## Subagent Guidance

Use subagents for RCA, security review, test gap review, and large codebase exploration. Ask subagents to return concise findings rather than raw logs.
