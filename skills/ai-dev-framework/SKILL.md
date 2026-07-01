---
name: ai-dev-framework
description: >
  Use for AI-assisted software development workflow governance: starting a new
  project, onboarding an existing repo, creating AGENTS.md or project charters,
  choosing stack packs or UI libraries, planning non-trivial code changes,
  applying Ponytail-style restraint, using independent analysis for RCA, or
  helping users who prompt naturally but want agents to push back and align to
  enterprise, project, and personal standards.
---

# AI Development Framework

Use the framework repo as the source of truth. Default location:

```text
/Users/parasrawat/Documents/ponytail
```

If that path does not exist, use the checked-in framework files in the current repository.

## Core Model

Apply three levels:

1. **Enterprise**: non-negotiable floor for security, data, testing, dependencies, observability, review, and AI-assisted development.
2. **Project**: project charter, architecture, testing plan, AI workflow, selected stack packs, selected UI member, and definition of done.
3. **Personal**: collaboration style and desired pushback. Personal rules cannot weaken enterprise or project rules.

## Default Workflow

For new projects:

1. Ask only for missing blocking inputs: objective, users, stack packs, UI member, non-goals, data sources, checks.
2. Create or update `PROJECT_CHARTER.md`, `ARCHITECTURE.md`, `TESTING.md`, `AI_WORKFLOW.md`, and `AGENTS.md`.
3. Select relevant stack packs from `stacks/`.
4. Do not begin major implementation until the project contract is clear enough.

For existing projects:

1. Inspect current files and patterns first.
2. Check for project instructions.
3. If missing, offer to create minimal docs from current reality.
4. Do not invent architecture; list gaps separately.

For non-trivial changes:

1. Read project instructions.
2. Trace the affected flow.
3. Challenge scope, dependencies, abstractions, missing tests, unclear data semantics, and UI-library drift.
4. Implement the smallest correct slice.
5. Run required checks or explain why not.
6. Summarize verification, risks, and any durable rule to promote.

## Ponytail Rule

Use Ponytail-style restraint: understand first, then prefer no code, existing code, standard library, native platform feature, installed dependency, one-line fix, and only then new code.

Never simplify away security, accessibility, data handling, root-cause analysis, or required verification.

## Independent Analysis

Use subagents or independent review passes for RCA, migrations, security-sensitive changes, data-loss risks, cross-component wiring, agent/RAG evaluations, and large UI rewrites.

## UI Member Selection

Read `stacks/ui-react.md` when UI work is involved.

Default fit:

- shadcn/ui + Radix: custom polished Tailwind apps.
- Mantine: fast internal operational tools.
- Tremor: dashboard/chart surfaces as a secondary member.
- Ant Design or MUI: dense enterprise admin.
- HeroUI: polished Tailwind/SaaS surfaces.
- React Aria, Base UI, Ark UI, or Radix: accessible design-system primitives.

Do not mix full UI systems casually.

## References

Read only when needed:

- `references/project-kickoff.md` for creating project docs.
- `references/existing-project.md` for onboarding an existing repo.
- `references/ui-selection.md` for UI library choices.
- `references/personal-style.md` for the user's preferred agent behavior.

