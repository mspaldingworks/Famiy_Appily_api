# Family Appily — API / Data Contracts

Companion repository to [`Family_Appily_app`](https://github.com/mspaldingworks/Family_Appily_app).

## Read this first

See [`ARCHITECTURE_DECISION.md`](./ARCHITECTURE_DECISION.md) for the resolved architecture. Short version: **household data (chores, rotation, tickets) has no backend** — SwiftData + CloudKit private database only, because the ticket-earning catalog contains a child's therapy-related activities. **Job Search is a deliberate, scoped exception** — it's the adult user's own data, not a child's, and a real dynamic API is needed so an external automation (n8n) can push in RSS-sourced job postings.

This repo now holds both:

## `contracts/` — static data, no server

The canonical schemas for the family's chore, rotation, and reward-ticket systems, transcribed from their physical wall charts. Served as versioned static JSON files (no database, no auth, no API framework) once deployed — see `ARCHITECTURE_DECISION.md` for the manifest/versioning scheme.

| File | Describes |
|---|---|
| `contracts/family.json` | Per-child weekly chore schedules; the chore catalog with per-child display labels |
| `contracts/rotation.json` | Shared family chore rotation. A 3-week cycle, computed from a formula rather than stored as a grid |
| `contracts/tickets.json` | Ticket economy: earn catalog, spend tiers, 30-slot reward chart, Vault |

These are mirrored in the app repo at `family-hub-assets/data/`, because the app needs them locally to seed its data store offline and must work fully in airplane mode. Treat the app repo as the source of truth and mirror changes here:

```sh
cp ../Family_Appily_app/family-hub-assets/data/*.json contracts/
```

**Privacy constraint**: `contracts/tickets.json` contains entries flagged `private: true` — health-adjacent items belonging to one child. Any consumer of these contracts must not surface them outside that child's own profile and adult accounts.

## `api/` — Django/DRF, the Job Search backend

A real, running service — the one deliberate exception to the "no backend" rule. Three apps: `tracker` (companies/applications/contacts/timeline), `identity` (professional profile/skills/links/resume versions), `ingestion` (the n8n webhook + promote-to-application). Native app auth is DRF TokenAuthentication (`Authorization: Token <token>`); Django admin uses session auth for browser-based management. See `docker-compose/` and `deploy/` for how it runs and deploys.
