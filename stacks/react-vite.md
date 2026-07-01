# Stack Pack: React + Vite

## Applies When

Use for React applications built with Vite or similar client-side React tooling.

## Default Project Shape

```text
src/
  app/          application shell, routing, providers
  components/   reusable UI components
  features/     feature-specific UI and logic
  lib/          small shared helpers
  services/     API clients and integration boundaries
  styles/       global styles and design tokens
tests/
```

## Required Practices

- Keep API calls out of presentational components.
- Keep component state local unless shared state is truly required.
- Use semantic HTML before custom interaction code.
- Preserve keyboard navigation, focus states, labels, and contrast.
- Keep loading, empty, error, and success states explicit for user-facing flows.
- Do not add a second UI system without tech lead approval.

## Quality Gates

Projects should define exact commands. Common defaults:

```bash
npm run lint
npm run test
npm run build
```

## AI Assistant Rules

- Inspect existing component and styling conventions before adding UI.
- Prefer the project-selected UI member from [ui-react.md](ui-react.md).
- Use native controls where they satisfy UX and accessibility.
- Do not create reusable components until there is a second real use.
- For UI changes, verify at desktop and mobile sizes when practical.

## Common Anti-Patterns

- Decorative card-heavy layouts for operational tools.
- Custom dropdowns/date pickers when native or selected UI-system components cover the need.
- Global state for form-local behavior.
- One-off CSS conventions that bypass the project design system.

