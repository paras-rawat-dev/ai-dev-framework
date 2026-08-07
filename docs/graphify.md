# Graphify In The Framework

[Graphify](https://github.com/Graphify-Labs/graphify) turns a repository or document corpus into a persistent knowledge graph that agents can query for architecture, relationships, paths, and explanations. The framework installs its CLI and Agent Skill globally, but does not require a graph for every task.

## Default Use

Use Graphify when repository breadth is part of the problem:

- onboarding an unfamiliar or large repository
- architecture and dependency mapping
- root-cause analysis across callers or components
- migrations and broad cross-component wiring
- repeated codebase questions when `graphify-out/graph.json` already exists

Skip graph generation for a trivial, isolated, or single-file change. Direct source inspection remains the authority. A graph is an index and analysis artifact, not proof that current code behaves as described.

## Automatic Installation

The normal host setup installs the reviewed Graphify CLI and native Agent Skill:

```bash
python3 scripts/install_framework.py --agent codex
python3 scripts/install_framework.py --agent claude
python3 scripts/install_framework.py --agent github-copilot
```

Run only the command for the active agent. The installer:

1. On macOS or Linux, finds Python 3.10 or later without modifying the system Python. Windows currently fails closed rather than running an unreviewed install path.
2. Creates a framework-owned virtual environment under `~/.local/share/ai-dev-framework/tools/graphify/`.
3. Installs the exact reviewed Git commit from `profiles/default.json`.
4. Verifies the installed package version and source commit.
5. Exposes `graphify` and `graphify-mcp` in `~/.local/bin` without replacing an unrelated existing command.
6. Wraps those commands so ambient remote-provider credentials are ignored unless explicit project approval is activated.
7. Stages Graphify's skill outside the live agent directory, adds the managed policy block, validates the governed result, and only then publishes it atomically to the selected agent's native user directory.
8. Rewrites the skill's self-install commands to the same reviewed commit, preventing hosted or missing-CLI paths from silently fetching a newer release.

Repair only Graphify with:

```bash
python3 scripts/install_graphify.py --platform codex
python3 scripts/install_graphify.py --platform claude
python3 scripts/install_graphify.py --platform github-copilot
```

For a GitHub-hosted Copilot agent, install the portable project skill and commit the resulting `.agents/skills/graphify` directory after review:

```bash
python3 scripts/install_framework.py \
  --agent github-copilot \
  --scope project \
  --target /path/to/project
```

## Project Decision

The tech lead records these decisions in `AI_WORKFLOW.md`:

- whether `graphify-out/` is generated locally, committed, or prohibited
- whether remote semantic or LLM backends are allowed for the repository's data classification
- whether strict hooks are justified
- when a graph should be refreshed

The framework leaves strict hooks and remote semantic backends off by default. Managed commands remove ambient provider credentials, so an API key already present in the shell is not approval to transmit repository data. Enabling an approved remote backend requires both a recorded project decision and `AI_DEV_FRAMEWORK_GRAPHIFY_REMOTE_APPROVED=1` for that invocation.

Graph output can contain source-derived names, relationships, paths, and summaries, so it follows the same handling rules as the source corpus. New framework projects keep `graphify-out/` local and ignored by default. Query logging is not enabled by the framework.

## Working Flow

1. If `graphify-out/graph.json` exists, query it first for broad relationship questions.
2. Check graph findings against the affected current source before deciding or editing.
3. If no graph exists, build one only when the task meets the project criteria above.
4. Refresh rather than rebuild when an existing graph is stale and Graphify supports the changed inputs.
5. Report whether conclusions came from the graph, source verification, or both.

## Updating The Pin

Do not silently track Graphify's latest branch. A framework maintainer must review upstream code, packaged skills, install behavior, dependency changes, data handling, and release notes, then update the version, tag, and full commit in `profiles/default.json` together.

The root Graphify revision is pinned and verified. Its Python transitive dependencies are resolved from that reviewed package at installation time, not hash-locked by this framework. Organizations requiring a fully locked software supply chain should mirror and constrain those dependencies before broad rollout.
