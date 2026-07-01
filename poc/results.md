# POC Results

Date: 2026-07-01

Command:

```bash
python3 tools/score_poc.py
```

Result:

```text
POC readiness score
===================
baseline-output.md: 0/12
  passed: none
framework-output.md: 12/12
  passed: objective, users, non_goals, stack_packs, ui_member, data_handling, quality_gates, tests, performance, ai_workflow, dependency_control, definition_of_done

delta: +12 criteria
PASS: framework artifact covers all readiness criteria and improves on baseline
```

Interpretation:

The framework-guided artifact is more project-ready than the loose baseline for this tiny app scenario. It captures scope, non-goals, selected stack packs, UI member choice, data handling, tests, performance, AI workflow, dependency control, and definition of done.

Limitation:

This is a static readiness check. It does not prove that every coding agent will produce better code. To measure real agent impact, run the same tiny app task with and without these instructions, replace the two output files with the generated artifacts, rerun the scorer, and manually review the resulting code.

