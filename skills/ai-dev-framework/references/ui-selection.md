# UI Selection Reference

Use the selected project UI member. If none exists, pick based on product shape:

| Product shape | Default |
| --- | --- |
| Custom polished Tailwind app | shadcn/ui + Radix |
| Fast internal operational tool | Mantine |
| Dashboard/charts | Tremor as secondary member |
| Dense enterprise admin | Ant Design or MUI |
| Polished Tailwind/SaaS | HeroUI |
| Accessible design-system primitives | Radix, React Aria, Base UI, or Ark UI |
| Marketing blocks/templates | Tailwind Plus where licensed |

Rules:

- Do not add a second full UI system without an explicit reason.
- Preserve keyboard navigation, focus states, labels, contrast, loading states, empty states, and error states.
- For repeated UI patterns, use project-owned components.
- For simple forms and inputs, use native controls when they satisfy the UX.

