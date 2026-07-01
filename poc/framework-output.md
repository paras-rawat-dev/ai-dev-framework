# Framework-Guided Plan

## Objective

Build a tiny internal expense review POC that proves upload/paste, summary, threshold flagging, and CSV export.

## Users

Finance reviewer who needs a quick local check before doing manual follow-up.

## Non-Goals

- no SSO
- no RBAC
- no background jobs
- no production deployment
- no complex approval workflow

## Selected Stack Packs

- `enterprise/constitution.md`
- `stacks/python-fastapi.md`
- `stacks/react-vite.md`
- `stacks/ui-react.md`

## UI Member

Primary UI member: shadcn/ui + Radix.

Reason: the POC needs a polished small app with forms, table, buttons, and dialogs while keeping component code locally owned.

Secondary allowed member: Tremor only if chart/dashboard widgets are needed.

Not allowed: MUI, Ant Design, Chakra, and Mantine in this POC because mixing full UI systems would create unnecessary inconsistency.

## Architecture

```text
frontend React/Vite -> FastAPI API -> in-memory or SQLite expense store
```

Backend:

- parse pasted CSV text or uploaded file
- validate required columns
- calculate totals by vendor and category
- flag rows above threshold
- return exportable reviewed rows

Frontend:

- upload/paste input
- threshold control
- summary cards
- reviewed rows table
- export button
- loading, empty, error, and success states

## Data Handling

Source: user-provided local expense CSV.

Sensitivity: medium; expense rows can contain vendor and spending data.

Rules:

- do not log raw uploaded rows
- validate columns before processing
- report rejected rows with row number and reason

## Quality Gates

```bash
ruff check .
pytest
npm run lint
npm run build
```

## Minimum Tests

- parser unit test for valid and invalid rows
- API integration test for threshold flagging
- CSV export test for reviewed rows
- frontend smoke/build check

## Performance Target

Handle 1,000 rows locally in under 2 seconds on a developer laptop.

## AI Workflow

- Read existing project files before adding code.
- Challenge any request to add RBAC, jobs, or production deployment during POC.
- Use independent review for RCA if parsing/export totals disagree.
- Do not add a second UI library.
- Fix parser bugs at the shared parser, not in individual API/UI call sites.

## Definition Of Done

- upload/paste works
- totals render
- threshold flags render
- CSV export works
- required checks run or skipped checks are explained

