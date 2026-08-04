# Required Companion Plugins

The default framework profile installs two required third-party companions:

- **Ponytail** for minimal, reuse-first, correctness-preserving implementation.
- **i-have-adhd** for action-first communication with visible progress and fewer tangents.

Their reviewed sources and revisions live in [profiles/default.json](../profiles/default.json). Do not silently move a pin to a newer commit. Review changed skills, hooks, scripts, and manifests first.

## Compatibility Matrix

| Agent | Ponytail | i-have-adhd | UI capability pack |
| --- | --- | --- | --- |
| Codex | Native plugin through a pinned framework marketplace | Native plugin through a pinned framework marketplace plus global output instructions | Browser, Visualize, and Sites plugins |
| Claude Code | Native plugin with skills and hooks | Native plugin with always-on SessionStart flag | Frontend Design and Playwright plugins |
| GitHub Copilot | Portable Ponytail Agent Skills | Portable Agent Skill plus always-on Copilot instructions | Framework UI guidance and project-owned browser tests |

Codex, Claude Code, and Copilot do not share one plugin package format. The portable unit is the Agent Skill when a host supports it. Native plugin hooks and tool integrations remain agent-specific.

The upstream Codex marketplace entries for both companions point their plugin source at moving `main`. The Codex installer therefore uses the small overlays in `companions/codex/`, whose plugin sources reference the reviewed commits directly. The third-party plugin code remains in its upstream repository; it is not vendored here.

## Automatic Setup

Run one command from the repository root:

```bash
python3 scripts/install_framework.py --agent codex
python3 scripts/install_framework.py --agent claude
python3 scripts/install_framework.py --agent github-copilot
```

Run only the command for the agent being configured. Preview without changing the machine:

```bash
python3 scripts/install_framework.py --agent claude --dry-run
```

The installers preserve existing personal instruction files by maintaining a marked framework block. They install companions at user scope so new projects receive the defaults automatically.

GitHub-hosted coding agents cannot see a developer's home directory. For those agents, install project-scoped skills into the target repository and commit `.agents/skills`:

```bash
python3 scripts/install_framework.py --agent github-copilot --scope project --target /path/to/project
```

Use these only when a user or organization deliberately rejects a companion:

```text
--skip-ponytail
--skip-i-have-adhd
--skip-ui-plugins
```

## UI Boundary

React members such as shadcn/ui, Radix, Mantine, MUI, and Ant Design are project dependencies, not coding-agent plugins. Select them per project from [stacks/ui-react.md](../stacks/ui-react.md).

UI agent plugins are host tooling:

- Codex receives Browser, Visualize, and Sites from the OpenAI-bundled marketplace.
- Claude receives Frontend Design and Playwright from the official Anthropic marketplace.
- Copilot has no required cross-surface UI plugin in this profile. It uses the framework skill and the project's own browser tests.

Chrome and Computer Use are not installed by this framework. They can expose personal browser or desktop state and require a separate trust decision.

## Security And Verification

Third-party plugins can execute hooks or scripts with the user's permissions. The default profile pins reviewed revisions, but pinning is not a substitute for organizational approval.

GitHub CLI explicitly treats downloaded Agent Skills as unverified third-party content. Before committing project-scoped skills, review their instructions, scripts, licenses, and generated source metadata.

After installation:

- Start a new agent session.
- Review and trust Ponytail hooks when the agent asks.
- Confirm the expected skills and plugins are enabled.
- Confirm external connectors or browser tools are authenticated only when needed.
