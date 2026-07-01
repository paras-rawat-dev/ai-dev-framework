# AI Assisted Development Standard

## Required Agent Behavior

AI coding agents must:

- read relevant repository instructions before changing code
- inspect existing patterns before adding new ones
- challenge unclear, risky, or over-broad requests
- fix root causes, not only visible symptoms
- run or explain the required checks
- surface uncertainty and missing information

## Required Human Behavior

Developers must:

- keep project instructions current
- review generated code as their own work
- avoid pasting secrets into agent prompts
- promote repeated corrections into durable guidance
- prefer small scoped tasks over broad vague prompts

## Subagent / Independent Review Guidance

Use independent agents or review passes for:

- RCA
- security-sensitive changes
- concurrency or data-loss risks
- migrations
- cross-component wiring
- large refactors

Independent analysis is valuable because it reduces context bleed. It is not a substitute for tests or owner review.

