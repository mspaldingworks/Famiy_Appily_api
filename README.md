# Family Appily — API / Data Contracts

Companion repository to [`Family_Appily_app`](https://github.com/mspaldingworks/Family_Appily_app).

## Read this first

**There is no service here yet, and there may never need to be one.** See [`ARCHITECTURE_DECISION.md`](./ARCHITECTURE_DECISION.md) — whether this project needs a backend is an open question that should be answered before the app build starts.

What this repo currently holds is the **canonical data contracts**: the schemas describing the family's chore, rotation, and reward-ticket systems, transcribed from their physical wall charts.

## Contracts

| File | Describes |
|---|---|
| `contracts/family.json` | Per-child weekly chore schedules; the chore catalog with per-child display labels |
| `contracts/rotation.json` | Shared family chore rotation. A 3-week cycle, computed from a formula rather than stored as a grid |
| `contracts/tickets.json` | Ticket economy: earn catalog, spend tiers, 30-slot reward chart, Vault |

## Note on duplication

These three files are currently mirrored in the app repo at `family-hub-assets/data/`, because the app needs them locally to seed its data store offline.

**Until the architecture decision is made, treat the app repo as the source of truth** and mirror changes here:

```sh
cp ../Family_Appily_app/family-hub-assets/data/*.json contracts/
```

Once Option A or B is chosen, collapse this to a single owner. Two copies of the same schema will drift, and the drift will be discovered at the worst possible moment.

## Privacy constraint

`contracts/tickets.json` contains entries flagged `private: true`. These are health-adjacent items belonging to one child. Any consumer of these contracts — service, app, or export — must not surface them outside that child's own profile and adult accounts. This is a hard requirement, not a preference.
