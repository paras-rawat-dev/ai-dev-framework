# Dependency Policy

## Default

Prefer the standard library, native platform features, existing helpers, and already-installed dependencies.

## New Production Dependency Requires

- the problem it solves
- why existing options are insufficient
- maintenance and license check
- bundle/runtime impact when relevant
- owner for future upgrades

## AI Assistant Rules

- Ask before adding a production dependency unless project instructions explicitly allow it.
- For UI dependencies, use the selected project UI member first.
- Do not add overlapping libraries for the same job without a migration plan.

