# Required Framework Companions

The default framework profile installs three required third-party companions:

- **Ponytail** for minimal, reuse-first, correctness-preserving implementation.
- **i-have-adhd** for action-first communication with visible progress and fewer tangents.
- **Graphify** for persistent repository graphs used in justified architecture, RCA, migration, onboarding, and cross-component work.

Their reviewed sources and revisions live in [profiles/default.json](../profiles/default.json). Do not silently move a pin to a newer commit. Review changed skills, hooks, scripts, and manifests first.

## Compatibility Matrix

| Agent | Ponytail | i-have-adhd | Graphify | UI capability pack |
| --- | --- | --- | --- | --- |
| Codex | Native plugin through a pinned framework marketplace | Native plugin through a pinned framework marketplace plus global output instructions | Pinned CLI plus native Codex Agent Skill | Browser, Visualize, and Sites plugins |
| Claude Code | Native plugin with skills and hooks | Native plugin with always-on SessionStart flag | Pinned CLI plus native Claude Skill | Frontend Design and Playwright plugins |
| GitHub Copilot | Portable Ponytail Agent Skills | Portable Agent Skill plus always-on Copilot instructions | Pinned CLI plus native user Skill or project `.agents/skills` | Framework UI guidance and project-owned browser tests |

Codex, Claude Code, and Copilot do not share one plugin package format. The portable unit is the Agent Skill when a host supports it. Native plugin hooks and tool integrations remain agent-specific.

The upstream Codex marketplace entries for Ponytail and `i-have-adhd` point their plugin source at moving `main`. The Codex installer therefore uses the small overlays in `companions/codex/`, whose plugin sources reference the reviewed commits directly. On macOS and Linux, Graphify is installed from its reviewed Git commit into an isolated virtual environment; Windows setup currently fails closed. Its Agent Skill is governed in staging before publication, and every self-install path is pinned to that same commit. Third-party code remains in its upstream repository; it is not vendored here.

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

The installers preserve existing personal instruction files by maintaining a marked framework block. They install companions at user scope so new projects receive the defaults automatically. Graphify is available globally, but the framework invokes it only when repository breadth justifies graph analysis; see [Graphify in the framework](graphify.md).

GitHub-hosted coding agents cannot see a developer's home directory. For those agents, install project-scoped skills into the target repository and commit `.agents/skills`:

```bash
python3 scripts/install_framework.py --agent github-copilot --scope project --target /path/to/project
```

Use these only when a user or organization deliberately rejects a companion:

```text
--skip-ponytail
--skip-i-have-adhd
--skip-graphify
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

Third-party plugins and tools can execute hooks or scripts with the user's permissions. The default profile pins reviewed revisions, but pinning is not a substitute for organizational approval.

GitHub CLI explicitly treats downloaded Agent Skills as unverified third-party content. Before committing project-scoped skills, review their instructions, scripts, licenses, and generated source metadata.

After installation:

- Start a new agent session.
- Review and trust Ponytail hooks when the agent asks.
- Confirm `graphify --version` reports the reviewed version and that the expected host skill exists.
- Keep Graphify strict hooks and remote semantic backends disabled unless project policy approves them. Ambient provider credentials are ignored by managed Graphify commands; approved remote use also requires `AI_DEV_FRAMEWORK_GRAPHIFY_REMOTE_APPROVED=1`.
- Keep `graphify-out/` ignored unless the project explicitly approves committing derived repository data.
- Confirm the expected skills and plugins are enabled.
- Confirm external connectors or browser tools are authenticated only when needed.
