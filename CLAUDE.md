# Claude Code Instructions

Use [AGENTS.md](AGENTS.md) as the canonical project guidance for this repository.

For teams adopting this framework in Claude Code:

- Put project-level guidance in `CLAUDE.md` or `.claude/CLAUDE.md`.
- Put path-specific rules in `.claude/rules/`.
- Put repeated workflows in `.claude/skills/<skill-name>/SKILL.md`.
- Keep personal preferences in `~/.claude/CLAUDE.md`.
- Use hooks only for mechanical enforcement, not static project facts.
- When configuring this framework, run `python3 scripts/install_framework.py --agent claude`; do not report setup complete if a required companion fails.

See [integrations/claude.md](integrations/claude.md) for the full adoption guide.
