# GitHub Repository Setup

This repo is meant to be shared as a setup guide and optional agent plugin marketplace.

## Install From GitHub In Codex

After this repository is pushed:

```bash
codex plugin marketplace add paras-rawat-dev/ai-dev-framework
codex plugin add ai-dev-framework@ai-dev-framework
```

Then start a new Codex thread.

This installs only the framework plugin. It does not complete the required companion profile.

## Complete Host Setup

Clone the repo and run the command for the host being configured:

```bash
python3 scripts/install_framework.py --agent codex
python3 scripts/install_framework.py --agent claude
python3 scripts/install_framework.py --agent github-copilot
```

The command installs the framework, Ponytail, `i-have-adhd`, and the reviewed UI capability pack available for that host. Treat a failed required companion as an incomplete setup.

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
