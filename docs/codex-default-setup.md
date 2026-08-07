# Make Codex Use This Framework By Default

Run from this repository:

```bash
python3 scripts/install_framework.py --agent codex
```

This installs:

- `~/.codex/AGENTS.md` from [codex/global-AGENTS.md](../codex/global-AGENTS.md)
- `~/.agents/skills/ai-dev-framework`
- custom Codex agents in `~/.codex/agents/`
- recommended `[agents]` config if missing
- pinned framework-managed Ponytail marketplace and plugin
- pinned framework-managed `i-have-adhd` marketplace and plugin for action-first output
- pinned Graphify CLI in an isolated environment plus its native Codex skill
- Browser, Visualize, and Sites UI capability plugins

The installer exits non-zero if a companion plugin cannot be installed, while keeping the framework files it installed successfully.

Third-party companion revisions are pinned in [profiles/default.json](../profiles/default.json). Review upstream changes before moving a pin.

Start a new Codex thread after installation.

## What Changes

Codex should now treat the framework as default behavior:

- prompt you during new-project kickoff
- inspect and document existing repos before big changes
- push back on scope, dependencies, missing checks, weak UI choices, and bad assumptions
- use Ponytail-style restraint
- use ADHD-friendly, action-first output by default
- use Graphify selectively for architecture, RCA, migrations, onboarding, and cross-component work
- use independent analysis for RCA, migrations, security/data risks, and cross-component wiring

## If Ponytail Installation Fails

Install manually:

```bash
codex plugin marketplace add /path/to/ai-dev-framework/companions/codex/ponytail
codex plugin add ponytail@ai-dev-framework-ponytail
```

The managed marketplace points the plugin source at the reviewed commit in [profiles/default.json](../profiles/default.json). Then open `/hooks` in Codex and trust Ponytail hooks if prompted.

## If i-have-adhd Installation Fails

Install manually:

```bash
codex plugin marketplace add /path/to/ai-dev-framework/companions/codex/i-have-adhd
codex plugin add i-have-adhd@ai-dev-framework-i-have-adhd
```

The installer verifies the plugin against the reviewed commit in [profiles/default.json](../profiles/default.json). The plugin includes a SessionStart hook; review it and follow Codex's trust prompt rather than bypassing hook approval. The global framework instructions still request ADHD-friendly output when the hook is unavailable.

## If Graphify Installation Fails

Confirm Python 3.10 or later and Git are available, then repair only Graphify:

```bash
python3 scripts/install_graphify.py --platform codex
```

The installer will not modify the system Python or overwrite an unrelated `~/.local/bin/graphify` command. See [Graphify in the framework](graphify.md) for the use and data-handling policy.
