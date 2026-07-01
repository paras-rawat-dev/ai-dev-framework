# Stack Pack: React UI Library Members

This stack pack defines the recommended UI library "members" a project can choose from. A project should pick one primary member and document why in `PROJECT_CHARTER.md` or `ARCHITECTURE.md`.

Sources were reviewed on 2026-07-01:

- shadcn/ui: https://ui.shadcn.com/docs
- shadcn registry: https://ui.shadcn.com/docs/registry
- Radix UI: https://www.radix-ui.com/
- Mantine: https://mantine.dev/
- HeroUI: https://www.heroui.com/docs/react/getting-started
- Chakra UI: https://chakra-ui.com/
- MUI: https://mui.com/
- Ant Design: https://ant.design/
- Tremor: https://tremor.so/
- React Aria Components: https://react-aria.adobe.com/
- Base UI: https://base-ui.com/
- Ark UI: https://ark-ui.com/
- Tailwind Plus: https://tailwindcss.com/plus/ui-blocks/documentation

## Default Selection Rule

Pick the smallest UI member that covers the product shape:

| Product shape | Recommended member |
| --- | --- |
| Custom branded app, Tailwind-friendly, wants owned components | shadcn/ui + Radix |
| Data-heavy dashboards | shadcn/ui + Tremor, or Mantine |
| Fast internal operational app | Mantine |
| Enterprise CRUD/admin with dense components | Ant Design or MUI |
| Accessible design-system primitives | Radix Primitives |
| Polished Tailwind/React Aria components | HeroUI |
| Product teams already invested in Chakra | Chakra UI |
| Enterprise-grade accessible behavior with custom visuals | React Aria Components |
| Headless accessible React primitives from the MUI/Radix ecosystem | Base UI |
| Multi-framework accessible design-system primitives | Ark UI |
| Licensed Tailwind templates/blocks | Tailwind Plus |

## Members

### shadcn/ui

Use when the team wants beautiful components copied into the codebase, Tailwind alignment, and ownership of component source. It is a code distribution platform rather than a traditional package-only component library.

Good fit:

- custom design systems
- AI-assisted component reuse
- teams comfortable owning component code
- projects that may later run a private component registry

Watch out:

- copied components become your maintenance responsibility
- needs design discipline to avoid inconsistent local forks

### Radix UI

Use for accessible primitives and design-system foundations. Radix pairs well with shadcn/ui and custom UI systems.

Good fit:

- accessible low-level components
- teams building their own design system
- precise behavior control

Watch out:

- primitives alone are not a finished visual system

### Mantine

Use when the team needs a broad React component library with strong docs, many components, hooks, and fast internal app velocity.

Good fit:

- internal tools
- dashboards
- CRUD apps
- teams that want batteries included

Watch out:

- visual style should be themed early to avoid generic defaults

### HeroUI

Use when the team wants polished React components built around Tailwind CSS and React Aria.

Good fit:

- modern marketing/product apps
- polished SaaS surfaces
- teams already on Tailwind

Watch out:

- confirm maturity for your exact framework/version before standardizing broadly

### Chakra UI

Use when teams want accessible React components and a token-based design-system approach.

Good fit:

- product teams with Chakra experience
- accessible app UIs
- design-token workflows

Watch out:

- avoid mixing with another full component library unless migrating

### MUI

Use when teams need a mature, production-tested, comprehensive React component suite, especially when Material Design or advanced table/date/data components matter.

Good fit:

- enterprise applications
- long-lived products
- teams that need MUI X-style advanced components

Watch out:

- can look generic unless deliberately themed
- heavier than copy-paste or primitive-first options

### Ant Design

Use for enterprise admin, CRUD, workflow, and dense internal systems where Ant's patterns fit the product.

Good fit:

- enterprise operations tools
- data-entry-heavy apps
- admin consoles

Watch out:

- strong design language; custom branding takes planning

### Tremor

Use for dashboard/chart-focused UI, usually alongside a broader UI member such as shadcn/ui.

Good fit:

- metrics dashboards
- analytics views
- quick data visualization

Watch out:

- not a full application UI system by itself

### React Aria Components

Use when accessibility, internationalization, and interaction behavior are critical, but the team wants full control over visual styling.

Good fit:

- custom design systems
- accessible complex controls
- internationalized products

Watch out:

- style-free by design; the team must own visual polish

### Base UI

Use when the team wants unstyled accessible React primitives with strong composition and no imposed visual language.

Good fit:

- accessible custom React component systems
- teams that like the MUI/Radix lineage but do not want Material UI visuals

Watch out:

- visual system and component styling remain the project team's responsibility

### Ark UI

Use when teams need headless accessible components across multiple frontend frameworks.

Good fit:

- design systems spanning React, Vue, Svelte, or Solid
- teams using state-machine-backed component behavior

Watch out:

- not a pre-styled visual system

### Tailwind Plus

Use when the team has a Tailwind Plus license and wants polished Tailwind blocks/templates, especially for marketing, application shells, ecommerce, or documentation pages.

Good fit:

- fast polished layouts
- marketing/product pages
- teams already on Tailwind

Watch out:

- licensing matters
- blocks/templates are not a complete engineering standard by themselves

## Project Kickoff Questions

- What is the primary UI member?
- What is allowed as a secondary member?
- What is forbidden to mix?
- Who owns shared components?
- What accessibility checks are required before merge?
- What screenshots or browser checks prove the UI works?
- Is this a component library, primitive system, dashboard helper, or template/block library?

## AI Assistant Rules

- Do not add a UI library until the project UI member is known.
- If no UI member is selected, ask the tech lead or use native HTML for the smallest POC.
- Do not mix full component systems casually.
- Prefer project-owned components over one-off styling for repeated patterns.
