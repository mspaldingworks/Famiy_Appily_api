# Paste this into Claude in VS Code — Family Appily, Phase 0

> **How to use.** Open the `Family_Appily_app` clone in VS Code with the Claude extension. Attach the files listed under *Attach these* below, then paste everything from the horizontal rule onward as one message. Do not paste your PAT into the chat — it lives in your git remote and `gh auth`, nothing more.

## Attach these

From this handoff bundle:

| Attach | Why |
|---|---|
| `BUILD_SPEC_from_repo.md` | The build specification. Rename it back to `CLAUDE.md` at the repo root so Claude auto-loads it every session. |
| `family-hub-assets/data/family.json` | Per-child weekly schedules + chore catalog |
| `family-hub-assets/data/rotation.json` | The 3-week rotation formula |
| `family-hub-assets/data/tickets.json` | Earn catalog, spend tiers, reward chart |
| `family-hub-assets/design/tokens.json` | Colors, type, frame styles, layout rules |
| `family-hub-assets/design/avatars/*.svg` (4) | Mascots |
| `family-hub-assets/design/motifs/*.svg` (8) | Corner motifs, star token, vault |
| `prototype/Family Appily.dc.html` | The approved visual reference — open it in a browser first |
| `README.md` (this bundle) | Screen-by-screen spec with exact values |

Do **not** attach `contracts-decision.md` — its question is answered in the prompt below.

---

You are implementing **Phase 0 and Phase 1** of Family Appily, a native SwiftUI family-management app for one household. `CLAUDE.md` at the repo root is the binding specification — read it in full before writing code. The attached JSON files in `family-hub-assets/` are the data contracts; the attached HTML file is an approved design reference, not code to port.

## Repository layout

Two repos, both on GitHub under `mspaldingworks`:

- `Family_Appily_app` — this repo. The SwiftUI app.
- `Famiy_Appily_api` — data contracts. **Note the typo** (missing `l`); rename it to `Family_Appily_api` on GitHub before wiring anything to it, then `git remote set-url`.

Both currently contain only `Initial commit` on the remote. Local commit `7a02be3` (build spec + assets) and `1afa004` (contracts) exist but were never pushed — push those first so the remote matches what you are building against.

## Architecture decision — resolved, do not re-litigate

`ARCHITECTURE_DECISION.md` in the API repo asked whether this project needs a backend. It does not need one for family data. The answer is a **split**:

**Device side — all family data.** SwiftData local store + **CloudKit private database** in the family's own iCloud. No accounts, no login, no server. Every chore completion, ticket, and reward record — including the two health-adjacent earn items flagged `private: true` — stays inside Apple's ecosystem and never touches infrastructure we operate. This satisfies decision D4 in `CLAUDE.md` and §9 of the design prompt.

**Hostinger — contracts only, no personal data.** Hostinger serves the three JSON contracts as versioned static files over HTTPS:

```
https://<your-domain>/appily/v1/family.json
https://<your-domain>/appily/v1/rotation.json
https://<your-domain>/appily/v1/tickets.json
https://<your-domain>/appily/v1/manifest.json   ← {"version": 1, "updated": "<ISO8601>", "etag": "<sha256>"}
```

That is the entire backend. No database, no auth, no API framework, no PHP. Rules:

1. The app **ships with the same three files bundled** and seeds from the bundle on first launch. It must work fully in airplane mode forever, per `CLAUDE.md` §3.6. The network fetch is an optimisation, never a dependency.
2. On launch, and at most once per day, `GET manifest.json`. If `version` is higher than the bundled version, fetch the changed contracts, validate against the Codable models, and only then commit. **Any validation failure = keep the existing contracts and log; never partially apply.**
3. **Nothing is ever POSTed to Hostinger.** No completions, no ticket counts, no child names, no timestamps. If you find yourself writing an upload path, stop — that is the line this decision exists to draw.
4. Serve over HTTPS with a long `Cache-Control` on the versioned files and `no-cache` on `manifest.json`. Add `.htaccess` with `Content-Type: application/json; charset=utf-8`.
5. Deploy contracts to Hostinger from the **API** repo via GitHub Actions over SSH (rsync to the public html path, key in `secrets.HOSTINGER_SSH_KEY`). The app repo never deploys anything.

Write this decision into `ARCHITECTURE_DECISION.md` as **Resolved: Option A with a static contract CDN**, and update `CLAUDE.md` §5 and §8 to match.

## What to build now

Follow the phase plan in `CLAUDE.md` §9. In this session deliver Phase 0 and Phase 1 only.

### Phase 0 — foundation

1. **Multiplatform Xcode project.** Target iOS 17 / iPadOS 17 / watchOS 10 / macOS 14. A `FamilyCore` Swift package holds models, data access, rotation logic, and theming; thin per-platform app targets. Design **iPad first** — the shared family iPad is the primary device.
2. **`ChildTheme`** — generated from `tokens.json`, not hand-typed. Two properties per child, and the distinction is load-bearing: `dotFill` (shape fills only) and `textInk` (text, labels, stateful chrome). Finley `#1B4F9C`/`#1B4F9C`; Arthur `#5CB85C`/`#3E7D36`; Maryn `#E04E2C`/`#BF3A1E`. Add a compile-time or unit-test guard that fails if a `decorativeOnly` token is ever used in a text or tint role.
3. **SwiftData models** — `Child`, `Chore`, `ChoreAssignment`, `Completion`, `RotationChore`, `EarnItem`, `SpendTier`, `TicketLedgerEntry`. Completions are an append-only ledger keyed by `(childID, choreID, date)`; ticket balance is derived, never stored as a mutable counter.
4. **Contract loading** — Codable models for the three JSONs, bundle-seeded, with the manifest refresh described above behind a `ContractSource` protocol so it can be stubbed in tests.
5. **Rotation engine** — implement `assignee(chore, weekIndex) = cycle[(chore.offset + weekIndex) % 3]` with `cycle = [finley, maryn, arthur]`. **Unit-test it against all 42 cells in `rotation.json`'s `verification` block; that test must pass before you move on.** `rotationEpoch` is currently `null` — surface it as a one-time adult setup step ("Which Sunday did Week 1 begin?"), persist it, and until it is set show the rotation as a picker rather than guessing a current week.
6. **Vector assets** — import the 12 SVGs as vector-preserved assets (`Preserve Vector Data`, single scale). One source per mascot serves 24pt to full screen. Do not rasterize.

### Phase 1 — the chore system

Build these four screens. The attached HTML prototype is the reference for layout, hierarchy, and state; match its structure, then express it in idiomatic SwiftUI.

1. **Profile picker** — app entry point, no login. Three mascot cards, name beneath, current ticket count. 60×60pt minimum tap target; cards are much larger. A fourth card opens the family rotation.
2. **Weekly chart** — seven day cards, **four across the top row, three across the bottom**, week beginning Sunday. Preserve that grid on iPad and Mac; collapse to a vertical list on iPhone, and also when Dynamic Type is at an accessibility size (the prototype goes two-across at AX5 — that is the intent). Each card carries the day label, that day's chores, and a completion count.
3. **The three card frames** — `open-book` for Finley (two facing pages, one chore per page; a third chore turns a page below the spread rather than adding a third page), `bamboo-fence` for Arthur (chores on the rail, panda peeking over, standing up when the day clears), `held-sign` for Maryn (penguin holds a rectangular sign, chores stacked). The rotation-resolved chore is marked with a dot in the child's identity color plus a "rotation" label — never color alone.
4. **The completion mark** — a hand-drawn-feeling black check struck over the chore text. Not an SF Symbol, not a circle, not a strikethrough. In the prototype it is this path in a `0 0 120 104` viewBox, uniformly scaled and rotated about −8°, stroke width 13, round caps:
   ```
   M10 44C24 42 34 60 47 88 61 62 84 24 110 10
   ```
   Draw it on with a trim animation under 400ms; under **Reduce Motion**, cross-fade the finished mark in instead. Critically: the mark must **not** inherit the completed text's opacity — the text fades to ~45%, the mark stays full black. Completion changes three things at once: text fade, the mark, and the card's background/border state.

### Non-negotiable, verified before you call it done

- Every screen usable at **AX5** with no clipping or truncation. No fixed font sizes, no `.frame(height:)` on text containers.
- 44pt minimum tap target everywhere; **60pt** for anything a child taps.
- VoiceOver labels that name the action and the subject: `"Mark Empty Dishwasher complete for Arthur, Tuesday"` — never `"Button"`.
- Light and dark mode both designed. The approved direction is light-first; dark is a warm charcoal ground, not inverted grey.
- Items flagged `private: true` render **only** in that child's own profile and for adults — never in family views, exports, or a widget on the shared iPad, and their absence leaves no gap, count, or placeholder.
- Children cannot delete anything. Marking complete is reversible by tapping again. Redemption is adult-gated **at the moment of redeeming**, never at launch.
- Works in airplane mode.
- Rotation unit test green against all 42 printed cells.

### Out of scope this session

Reward chart UI, earn/spend sheets, widgets, the Watch complication, EventKit calendar integration. Phase 2+. Do not start them.

## Working agreement

- Commit in small, labelled steps. Push to `main` on `Family_Appily_app`.
- If a requirement in `CLAUDE.md` conflicts with something here, `CLAUDE.md` wins — except the architecture question above, which this prompt resolves.
- If an accessibility constraint and a visual detail conflict, accessibility wins and you tell me what you changed.
- Do not invent an alternative visual system. `family-hub-assets/` is the specification.
- When you hit a genuine ambiguity, ask one question and keep going on everything else.
