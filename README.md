# AI Assisted Development Framework

This repository is a practical operating model for making AI-assisted coding more consistent across teams without forcing everyone to use the same assistant or prompting style.

It uses three levels of guidance:

1. **Enterprise**: the floor every project must meet.
2. **Project**: the concrete rules for one repository or product.
3. **Personal**: the way an individual prefers to work with coding agents.

The goal is not to make one giant prompt. The goal is to keep durable standards in versioned markdown, make project decisions explicit at kickoff, and tell developers how to load those instructions into Codex, Claude Code, GitHub Copilot, or another agent.

## Quick Start

1. Read [docs/flow.md](docs/flow.md).
2. Read [docs/authoring-guide.md](docs/authoring-guide.md) to understand who creates each level.
3. Pick the enterprise rules that apply from [enterprise/](enterprise/).
4. Choose or write stack packs from [stacks/](stacks/).
5. Start a new project using [projects/TEMPLATE.project-charter.md](projects/TEMPLATE.project-charter.md).
6. Add agent instructions using the relevant integration guide:
   - [Codex](integrations/codex.md)
   - [Claude Code](integrations/claude.md)
   - [GitHub Copilot](integrations/github-copilot.md)
7. Install the framework and required companions for your coding agent:

```bash
python3 scripts/install_framework.py --agent codex
python3 scripts/install_framework.py --agent claude
python3 scripts/install_framework.py --agent github-copilot
```

Run only the command for the agent being configured. See [required companion plugins](docs/companion-plugins.md) for portability, reviewed pins, UI tooling, and skip controls.

8. To bootstrap docs in a project, run:

```bash
python3 /path/to/ai-dev-framework/scripts/bootstrap_project.py .
```

9. Run the small POC:

```bash
python3 tools/score_poc.py
```

## Repository Layout

```text
enterprise/   Organization-wide engineering floor.
stacks/       Tech-lead-owned stack packs such as Python/FastAPI or React/Vite.
projects/     Templates created when a new repo or product starts.
personal/     Personal instruction templates for individual working style.
integrations/ How to install the same ideas in Codex, Claude, and Copilot.
profiles/     Reviewed companion-plugin sources, revisions, and host mappings.
companions/   Host-specific pinned marketplace overlays for third-party companions.
checklists/   Reusable review, RCA, project kickoff, and UI-selection checklists.
poc/          Tiny baseline-vs-framework proof of concept.
tools/        Local scripts for validation and experiments.
```

## Current UI Members

The React UI stack pack includes these recommended members:

- shadcn/ui
- Radix UI
- Mantine
- HeroUI
- Chakra UI
- MUI
- Ant Design
- Tremor
- React Aria Components
- Base UI
- Ark UI
- Tailwind Plus

Projects should pick one primary member and document the reason. Mixing full UI systems requires tech lead approval.

## Agent Plugins And Skills

This repo includes Codex and Claude plugin manifests plus a portable Agent Skill:

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
.agents/plugins/marketplace.json
skills/ai-dev-framework/SKILL.md
```

After the repo is pushed to GitHub, users with access can install it with:

```bash
codex plugin marketplace add paras-rawat-dev/ai-dev-framework
codex plugin add ai-dev-framework@ai-dev-framework
```

Those two marketplace commands install only the framework plugin. Use the Quick Start host command to apply required companions and UI tooling.

The framework skill is portable. Plugin packaging, hooks, browser tooling, and install commands remain agent-specific. The cross-agent setup script installs Ponytail and `i-have-adhd` by default and installs the reviewed UI capability pack available for the selected host.

## Core Rule

Personal style can make the agent stricter, more skeptical, or more comfortable to work with. It must not override enterprise or project rules.

If a coding agent repeats the same mistake twice, promote the lesson:

```text
chat correction -> personal instruction -> project rule -> stack pack -> enterprise standard
```

Only promote a rule as far as it is actually reusable.
