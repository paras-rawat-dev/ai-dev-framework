# Operating Flow

This flow is for teams that want AI-assisted development to stay uniform across projects while still letting people use Codex, Claude Code, GitHub Copilot, or other assistants.

## 1. Enterprise Sets The Floor

Enterprise guidance is broad, stable, and non-negotiable. It should define the minimum bar for:

- security and privacy
- data handling
- dependency approval
- testing and verification
- observability
- accessibility
- code review
- AI-assisted development boundaries

It should not prescribe every framework detail. That belongs in stack packs and project charters.

## 2. Tech Leads Own Stack Packs

A stack pack defines what good looks like for a technology family. Examples:

- Python + FastAPI
- React + Vite
- Node + TypeScript
- data pipelines
- AI agents and retrieval systems
- UI component systems

Each stack pack should include defaults, quality gates, anti-patterns, and AI-assistant rules.

## 3. Project Kickoff Creates The Project Contract

At the start of a project, the lead creates a project charter and supporting docs. The project level is where vague standards become concrete:

- selected stack packs
- repository layout
- build, test, and run commands
- data sources
- API contracts
- performance targets
- UI library choice
- explicit non-goals
- agent workflow expectations

This is the most important layer for day-to-day AI coding.

## 4. Personal Instructions Tune Collaboration

Personal guidance should describe interaction style:

- challenge unclear scope
- use independent review for RCA
- prefer small diffs
- surface uncertainty
- ask fewer questions when a safe assumption exists

Personal guidance must not relax enterprise or project requirements.

## 5. Daily Agent Loop

For non-trivial work, use this loop:

```text
read current project instructions
understand affected flow
challenge unnecessary scope
plan smallest useful slice
implement
run required checks
review against project and stack rules
update docs only when a durable rule changed
```

## 6. Feedback Promotion

When a repeated issue appears, promote it to the narrowest durable layer:

| Repeated issue | Where it belongs |
| --- | --- |
| Individual prompting preference | `personal/` |
| One repo pattern | project `AGENTS.md` or `AI_WORKFLOW.md` |
| Stack-specific issue | `stacks/<stack>.md` |
| Organization-wide risk | `enterprise/` |

Do not promote one-off fixes into broad policy.

