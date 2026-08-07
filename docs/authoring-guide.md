# Authoring Guide

This guide explains how people create their own guidance at each level.

## Enterprise Authoring

Enterprise guidance should be owned by engineering leadership or the relevant control owner. It should be short, stable, and enforceable.

Good enterprise rule:

```md
Validate input at trust boundaries. Do not remove validation to reduce code.
```

Weak enterprise rule:

```md
Write clean code using best practices.
```

Enterprise files should answer:

- What is never optional?
- What must be checked in review?
- What should CI or hooks enforce?
- What should never be left to personal preference?

Use [enterprise/constitution.md](../enterprise/constitution.md) as the index.

## Tech Lead Stack Pack Authoring

Tech leads own stack packs. Copy [stacks/TEMPLATE.stack.md](../stacks/TEMPLATE.stack.md), then fill it with concrete decisions.

Required sections:

- when the stack pack applies
- default project shape
- required practices
- quality gates
- performance expectations
- AI assistant rules
- common anti-patterns
- project kickoff questions

The stack pack should be narrow enough to be useful. `backend.md` is usually too vague. `python-fastapi.md` is useful.

### Stack Pack Review Rubric

Before approving a stack pack, ask:

- Could an AI agent follow this without asking ten extra questions?
- Are commands concrete enough to run or adapt?
- Are required rules separate from preferences?
- Are anti-patterns specific to this stack?
- Does it avoid one-project-only details?

## UI Member Authoring

When a team wants a new UI library added as a member, the tech lead should submit a short note with:

- library name and official docs link
- product shape it fits
- accessibility posture
- theming/storybook/design-system implications
- bundle/runtime concerns if known
- what it replaces or must not be mixed with
- example project where it should be the default

Do not add a UI member only because it looks good in screenshots. It must have a clear product fit and maintenance owner.

## Project Authoring

At project kickoff, copy:

- [projects/TEMPLATE.project-charter.md](../projects/TEMPLATE.project-charter.md)
- [projects/TEMPLATE.architecture.md](../projects/TEMPLATE.architecture.md)
- [projects/TEMPLATE.testing.md](../projects/TEMPLATE.testing.md)
- [projects/TEMPLATE.ai-workflow.md](../projects/TEMPLATE.ai-workflow.md)

The project tech lead fills these before major implementation starts.

Project guidance should answer:

- What are we building?
- What is out of scope?
- What stack packs apply?
- What UI member is selected?
- What data sources are used?
- What commands prove the work?
- When should independent agent review be used?
- When should Graphify be used, and may its source-derived output be retained or sent to a remote backend?

## Personal Authoring

Individuals copy [personal/TEMPLATE.personal-instructions.md](../personal/TEMPLATE.personal-instructions.md).

Personal guidance can define:

- communication preferences
- desired pushback style
- preferred use of subagents
- how much planning detail they like
- how uncertainty should be reported

Personal guidance cannot:

- disable tests required by project docs
- allow forbidden dependencies
- weaken security or data handling
- override the selected UI member

## Promotion Rule

Promote guidance only as broadly as evidence supports:

```text
one person repeats a correction -> personal
one repo repeats a correction -> project
several repos in one stack repeat it -> stack pack
several stacks repeat it -> enterprise
```

## Minimum Acceptance Criteria

Every new guidance file should be:

- specific enough for an agent to act on
- short enough to stay in context
- owned by a person or group
- linked from the relevant index or template
- tested once in a small task or review scenario
