# Tiny App Spec

Build a very small internal expense review tool.

Users can:

- upload or paste a small expense list
- see totals by vendor and category
- flag rows above a configurable threshold
- export the reviewed rows as CSV

The POC should use:

- Python + FastAPI backend
- React + Vite frontend
- local SQLite or in-memory storage
- a polished but lightweight UI

Non-goals:

- SSO
- multi-tenant RBAC
- background jobs
- production deployment
- complex approval workflow

