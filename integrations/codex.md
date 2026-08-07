# Codex Integration

Codex supports durable guidance through global instructions, repository instructions, skills, project config, custom agents, and plugins.

## Enterprise Level

Use one of these:

- Admin-managed skills or plugins when distributing organization-wide workflows.
- Checked-in enterprise docs in this framework repo, referenced by project instructions.
- For an individual machine, copy a short enterprise summary into `~/.codex/AGENTS.md` only if it truly applies to all work.

## Project Level

Recommended files in each project:

```text
AGENTS.md
PROJECT_CHARTER.md
ARCHITECTURE.md
TESTING.md
AI_WORKFLOW.md
.agents/skills/<workflow>/SKILL.md
.codex/agents/<agent>.toml
```

Use `AGENTS.md` for concise rules Codex should always read. Put longer procedures in skills or linked docs.

## Personal Level

Use:

```text
~/.codex/AGENTS.md
~/.codex/agents/<personal-agent>.toml
~/.agents/skills/<personal-skill>/SKILL.md
```

Personal guidance should tune collaboration style, not override project rules.

## Suggested Personal Defaults

- Challenge unclear scope and unnecessary dependencies.
- Use independent analysis for RCA, migrations, and cross-component wiring.
- Prefer small diffs after reading the affected flow.
- State checks run and checks skipped.

## Make It Automatic

Run from this framework repo:

```bash
python3 scripts/install_framework.py --agent codex
```

This installs global defaults, the `ai-dev-framework` skill, custom agents, Ponytail and `i-have-adhd` through framework-managed pinned marketplaces, the pinned Graphify CLI and Codex skill, and the Browser, Visualize, and Sites UI capability plugins. See [docs/codex-default-setup.md](../docs/codex-default-setup.md) and [required framework companions](../docs/companion-plugins.md).

## Project Bootstrap

For a new Codex project:

1. Copy project templates into the repo.
2. Fill `PROJECT_CHARTER.md`.
3. Create `AGENTS.md` with the selected enterprise and stack rules.
4. Add `.agents/skills/` only for repeated workflows.
5. Add `.codex/agents/` only for specialized subagents.
