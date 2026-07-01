# Review Standards

Review should prioritize:

1. correctness and behavior regressions
2. security and data loss
3. missing verification
4. maintainability
5. performance where relevant
6. over-engineering

## AI Review Prompt Shape

Ask for findings first, ordered by severity, with file and line references where possible. Summaries come after findings.

## Required Review Questions

- Does the change solve the root cause?
- Is the diff smaller than the problem requires or larger than it needs to be?
- Are tests/checks meaningful?
- Are new abstractions justified by current requirements?
- Are data and security boundaries preserved?

