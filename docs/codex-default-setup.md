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
- `i-have-adhd` plugin marketplace and plugin for action-first output

The installer exits non-zero if a companion plugin cannot be installed, while keeping the framework files it installed successfully.

Start a new Codex thread after installation.

## What Changes

Codex should now treat the framework as default behavior:

- prompt you during new-project kickoff
- inspect and document existing repos before big changes
- push back on scope, dependencies, missing checks, weak UI choices, and bad assumptions
- use Ponytail-style restraint
- use ADHD-friendly, action-first output by default
- use independent analysis for RCA, migrations, security/data risks, and cross-component wiring

## If Ponytail Installation Fails

Install manually:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Then open `/hooks` in Codex and trust Ponytail hooks if prompted.

## If i-have-adhd Installation Fails

Install manually:

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

At the reviewed upstream revision (`72c33eee81ea439cf01991e93729adfce2ffc99e`, 2026-07-19), the plugin contains an instruction-only skill and does not require hook trust. Because the upstream marketplace tracks `main` and has no release tags, the installer verifies both upstream and installed revisions against that reviewed SHA. A changed revision fails installation; audit it before updating the pin.
