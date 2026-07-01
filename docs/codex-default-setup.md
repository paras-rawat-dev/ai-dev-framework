# Make Codex Use This Framework By Default

Run from this repository:

```bash
python3 scripts/install_codex_framework.py
```

This installs:

- `~/.codex/AGENTS.md` from [codex/global-AGENTS.md](../codex/global-AGENTS.md)
- `~/.agents/skills/ai-dev-framework`
- custom Codex agents in `~/.codex/agents/`
- recommended `[agents]` config if missing
- Ponytail plugin marketplace and plugin when the local `codex` CLI can install it

Start a new Codex thread after installation.

## What Changes

Codex should now treat the framework as default behavior:

- prompt you during new-project kickoff
- inspect and document existing repos before big changes
- push back on scope, dependencies, missing checks, weak UI choices, and bad assumptions
- use Ponytail-style restraint
- use independent analysis for RCA, migrations, security/data risks, and cross-component wiring

## If Ponytail Installation Fails

Install manually:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Then open `/hooks` in Codex and trust Ponytail hooks if prompted.

