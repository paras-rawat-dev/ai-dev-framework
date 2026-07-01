# PR Review Checklist

Prioritize findings in this order:

1. correctness and regressions
2. security and data loss
3. missing verification
4. maintainability
5. performance
6. over-engineering

Questions:

- [ ] Does this solve the root cause?
- [ ] Are project and stack rules followed?
- [ ] Are new dependencies justified?
- [ ] Are tests meaningful for the changed behavior?
- [ ] Are UI accessibility states preserved?
- [ ] Are errors observable enough for RCA?
- [ ] Is any new abstraction justified by current requirements?

