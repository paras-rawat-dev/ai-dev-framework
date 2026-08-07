# AI Assisted Development Framework Instructions

This repo is documentation-first. Keep changes small, explicit, and easy for a tech lead to copy into a real project.

## Working Rules

- Preserve the three-level model: enterprise, project, personal.
- Do not bury enforceable policy inside personal preferences.
- Prefer concise templates over long essays.
- When adding guidance, name where it should live and who owns it.
- For UI guidance, include a library selection reason, accessibility expectations, and when not to add a UI dependency.
- For POC work, be honest about what is measured. Do not claim model-quality improvement from a static document check.

## Setup Contract

- `profiles/default.json` is the reviewed source of truth for required companions and host-specific UI tooling.
- When asked to install or adopt this framework, run `python3 scripts/install_framework.py --agent <agent>` for the active host.
- Do not report setup complete when Ponytail, `i-have-adhd`, Graphify, or a required host capability fails to install.
- Do not claim that native Codex or Claude plugins are portable to another agent. Use the mappings in `docs/companion-plugins.md`.

## Verification

Run this after changing the POC or scoring script:

```bash
python3 tools/score_poc.py
```

Run this after changing markdown structure:

```bash
find . -type f -not -path './.git/*' | sort
```
