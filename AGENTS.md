# AI Assisted Development Framework Instructions

This repo is documentation-first. Keep changes small, explicit, and easy for a tech lead to copy into a real project.

## Working Rules

- Preserve the three-level model: enterprise, project, personal.
- Do not bury enforceable policy inside personal preferences.
- Prefer concise templates over long essays.
- When adding guidance, name where it should live and who owns it.
- For UI guidance, include a library selection reason, accessibility expectations, and when not to add a UI dependency.
- For POC work, be honest about what is measured. Do not claim model-quality improvement from a static document check.

## Verification

Run this after changing the POC or scoring script:

```bash
python3 tools/score_poc.py
```

Run this after changing markdown structure:

```bash
find . -type f -not -path './.git/*' | sort
```

