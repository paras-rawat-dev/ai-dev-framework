# How To Adopt

Use this framework in a real team in four passes.

## Pass 1: Establish The Minimum Floor

Pick the enterprise docs that apply and edit them down to rules people can actually follow. If a rule cannot be checked by a reviewer, test, CI job, or obvious code inspection, rewrite it.

## Pass 2: Ask Tech Leads For Stack Packs

Each tech lead copies [stacks/TEMPLATE.stack.md](../stacks/TEMPLATE.stack.md), fills it for their area, and submits it for review. The review should ask:

- Is this specific enough for an AI agent to follow?
- Does it name build and test commands?
- Does it include anti-patterns?
- Does it separate required rules from preferences?
- Does it avoid overfitting to one project?

See [authoring-guide.md](authoring-guide.md) for stack pack, UI member, project, and personal authoring rules.

## Pass 3: Use Project Templates At Kickoff

Every new project should create:

- `PROJECT_CHARTER.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `AI_WORKFLOW.md`
- agent instruction files for the tools the team uses

Do this before major implementation starts.

Each developer should also run the agent-specific setup command from [required framework companions](companion-plugins.md). This installs the framework, Ponytail, `i-have-adhd`, Graphify, and the host's reviewed UI capability pack where one exists.

## Pass 4: Keep The Loop Alive

Review the guidance after real misses:

- failed PR review
- production incident
- repeated agent mistake
- repeated user correction
- new stack decision

Update the narrowest file that would have prevented the miss.

## Codex Default Setup

For Codex users who want this to become default behavior, run:

```bash
python3 scripts/install_framework.py --agent codex
```

That installs global defaults, the reusable framework skill, required companions, and the Codex UI capability pack. Project teams should still create project-level docs so the defaults have concrete facts to apply.
