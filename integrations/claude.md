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

Personal instructions should cover how you want Claude to collaborate.

## Suggested Project `CLAUDE.md`

```md
# Project Instructions

Read PROJECT_CHARTER.md, ARCHITECTURE.md, TESTING.md, and AI_WORKFLOW.md before non-trivial changes.

Follow the selected stack packs named in PROJECT_CHARTER.md.

Run the required checks from TESTING.md after implementation or explain why they could not run.
```

## Subagent Guidance

Use subagents for RCA, security review, test gap review, and large codebase exploration. Ask subagents to return concise findings rather than raw logs.
