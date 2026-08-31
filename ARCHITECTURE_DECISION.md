# Open decision: does this project need a backend at all?

**Status: RESOLVED, 2026-08-31, as a split.**

- **Household data (chores, rotation, tickets): Option A, no backend.** See below — unchanged from the original recommendation. `contracts/` in this repo holds versioned static JSON, served with no database, no auth, no API framework.
- **Job Search: Option B, a deliberate scoped exception.** This is the adult user's own data (job applications, professional identity), not a child's, so the privacy rationale below doesn't apply to it the same way. It also has a real, concrete need for a server: a Hostinger-hosted n8n workflow pushes in RSS-sourced job postings via a webhook, which a pure on-device app has no way to receive. The `api/` directory in this repo is a real running Django/DRF service for exactly this — `tracker`, `identity`, and `ingestion` apps, DRF TokenAuthentication for the native app, deployed at its own subdomain, isolated from every other stack on the shared VPS. Nothing about this changes the household-data decision below; it is a narrow, justified carve-out for one feature, not a reopening of the general question.

## The conflict

`CLAUDE.md` in the app repo specifies (decision D4):

> Local-first (SwiftData) + CloudKit private database. No server, no accounts, syncs across family devices via existing Apple IDs, children's data never leaves Apple's ecosystem.

The existence of this repository implies the opposite. Both cannot be true. This needs a deliberate answer, not a default.

## Why it matters more than usual here

The earn catalog (`contracts/tickets.json`) contains health-adjacent items — a proprioception sensory activity and a therapeutic listening activity. That is information about a specific child's therapy, tied to their name, with a daily timestamp attached every time it's marked complete.

Under CloudKit private database, that data sits in the family's own iCloud and is never transmitted to a third party. Under a custom API, it lives on a server someone has to secure, back up, patch, and eventually decommission — and it becomes subject to a materially different set of obligations.

That is not a reason to reject a backend. It is a reason to choose on purpose.

## Option A — No backend (CloudKit only)

**Keep:** this repo as the home of the canonical data contracts in `contracts/`, consumed by the app as seed data. No running service.

- No server to secure, pay for, or maintain
- No accounts; sync uses Apple IDs the family already has
- Health-adjacent data never leaves Apple's ecosystem
- Free
- Apple-only forever; no web access; harder to integrate non-Apple calendars later

## Option B — Custom backend

**Build:** an actual API service in this repo.

- Any platform can reach it, including a future web view
- Full control over the data model and sync semantics
- Real hosting, auth, backup, and security burden — for a household of five
- Children's therapy data now lives on infrastructure you own and must protect
- Ongoing cost and maintenance

## Recommendation

**Option A.** For a single household on all-Apple devices, a backend adds meaningful operational and privacy burden and buys very little. If a non-Apple device or a web surface becomes a requirement later, revisit — the contracts in this repo are exactly what a future service would serve, so nothing is wasted.

If you choose Option B, say so and the app spec (D4, §5, §8) needs rewriting before any code is written.
