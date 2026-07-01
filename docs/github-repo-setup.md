# GitHub Repository Setup

This repo is meant to be shared as a setup guide and optional Codex plugin marketplace.

## Install From GitHub In Codex

After this repository is pushed:

```bash
codex plugin marketplace add paras-rawat-dev/ai-dev-framework
codex plugin add ai-dev-framework@ai-dev-framework
```

Then start a new Codex thread.

## Manual Setup Without Plugin Install

Clone the repo and run:

```bash
python3 scripts/install_codex_framework.py
```

## Start A New Project

Inside a new project:

```bash
python3 /path/to/ai-dev-framework/scripts/bootstrap_project.py .
```

Then fill:

- `PROJECT_CHARTER.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `AI_WORKFLOW.md`
- `AGENTS.md`

## Claude And Copilot

Use:

- [integrations/claude.md](../integrations/claude.md)
- [integrations/github-copilot.md](../integrations/github-copilot.md)

