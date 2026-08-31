# Handoff: Family Appily — chore tracking

## Overview

A native SwiftUI family-management app for one household with three children (Finley 14, Arthur 11, Maryn 8) across iPhone, iPad, Apple Watch and Mac. It digitizes a set of physical wall charts that already work: a personal weekly chore chart per child, a shared six-chore rotation, and a ticket economy tracked on a 30-slot reward chart.

**The job is to digitize a system that already works, not to redesign it.**

Start with **`PHASE0_PROMPT.md`** — that is the message to paste into Claude in VS Code, and it lists exactly what to attach.

## About the design files

`prototype/Family Appily.dc.html` is a **design reference created in HTML** — a prototype showing intended look and behavior. It is not production code to port. The task is to recreate it in SwiftUI using idiomatic Apple patterns.

To view it: open `prototype/Family Appily.dc.html` in a browser. It needs `support.js` and `_ds/` alongside it, both included.

## Fidelity

**High fidelity.** Colors, type, spacing, states and interactions are final and reviewed. Recreate the UI faithfully. Where a value here disagrees with `family-hub-assets/design/tokens.json`, **tokens.json wins** — it is the source of truth and the prototype was built from it.

## Design tokens

### Identity colors — non-negotiable

Two color systems exist in the physical materials and they conflict. The **rotation chart's printed legend wins**, because it is the convention the children already read off the wall. Mascot artwork colors are decorative fill only.

| Child | `dotFill` (shapes only) | `textInk` (text, labels, stateful UI) | Contrast on white |
|---|---|---|---|
| Finley | `#1B4F9C` | `#1B4F9C` | 7.94:1 — passes AAA |
| Arthur | `#5CB85C` | `#3E7D36` | fill 2.48:1 **fails**; ink 5.01:1 passes AA |
| Maryn | `#E04E2C` | `#BF3A1E` | fill 3.97:1 **fails**; ink 5.47:1 passes AA |

Arthur's and Maryn's `dotFill` values may be used **as filled shapes only, never as text and never as the sole indicator of anything.**

### Shared

| Token | Value | Use |
|---|---|---|
| ink | `#1F1F26` | Body text, outlines, character linework |
| paper | `#FFFFFF` | Card background, light |
| paperDark | `#1C1C1E` | Card background, dark |
| wall | `#F5EAD8` | Page ground behind the cards |
| chartTitleGreen | `#3F6B2B` | Chart title — Finley, Arthur |
| chartTitleRed | `#CE3626` | Chart title — Maryn |
| completionMark | `#1F1F26` | The hand-drawn check. Always full-opacity black. |
| hairline | `#D9CFBC` | Dividers, dashed empty states |
| muted text | `#6B6459` | Secondary labels, counts |

Decorative-only illustration fills: pizza gold `#F0B440`, crust `#D98A4E`, pepperoni `#C4372F`, cap navy `#2E3A80`, hoodie green `#4E7A3A`, bamboo `#7CAD48` / `#8ABB55`, hat orange `#D18B4A`, ice blue `#9ED2EE` / `#DCF0FA`, beak `#E08A5A`, blush `#F2A9A4`. **Never text.**

### Reward chart row palettes

Row N uses `cycle[(N-1) mod 3]`.

| Child | Cycle |
|---|---|
| Arthur | `#E8B44A`, `#4FA83D`, `#9FCFC4` |
| Finley | `#D9642E`, `#F0B440`, `#2E3A80` |
| Maryn | `#CE3626`, `#9ED2EE`, `#E08A5A` |

### Typography

The physical charts use a rounded marker face for titles and a plain sans for chore text. **Reproduce with system fonts** — `.system(.largeTitle, design: .rounded)` heavy uppercase for chart titles, `.system(.caption, design: .rounded)` bold uppercase +1.0 tracking for day labels, `.system(.body)` regular for chore text. No hardcoded sizes.

The prototype renders titles in Caprasimo and body in Nunito because SF Rounded is not available in a browser. **Do not ship a custom display font** unless it supports the full Dynamic Type range — treat Caprasimo as a stand-in for SF Rounded Heavy.

Relative scale used in the prototype (multiply by the Dynamic Type factor, never fix):

| Role | Size | Weight | Case | Tracking |
|---|---|---|---|---|
| Screen title | 52 | heavy | sentence | −0.015em |
| Chart title | 38 | heavy | UPPER | −0.015em |
| Child name | 36 | heavy | sentence | −0.015em |
| Section title | 30–34 | heavy | UPPER | — |
| Chore text | 15 | semibold (600) | sentence | — |
| Day label | 13 | black (900) | UPPER | +0.16em |
| Micro label / kicker | 10–12 | black (900) | UPPER | +0.10–0.20em |
| Ticket count | 26 | black | — | — |

### Geometry

| Token | Value |
|---|---|
| Card radius | 26px |
| Profile card radius | 32px |
| Panel radius | 24–28px |
| Chore row radius (rail) | 12px |
| Sign frame radius | 6px, inner rows 3px |
| Book frame radius | 8px top, 14px bottom |
| Pill / button radius | 999px |
| Border weight | 3px on every card, panel and chore row; 2px on hairlines and micro-chips |
| Grid gap | 24px row / 22px column |
| Card padding | 15px horizontal, 16px footer |
| Elevation, resting | `0 6px 16px rgba(90,70,40,.14)` |
| Elevation, today | `0 10px 26px rgba(0,0,0,.18)` |
| Elevation, hover | `0 20px 38px rgba(0,0,0,.18)` |

Everything is over-rounded and hard-outlined. No hairline-only geometry, no sharp corners.

## Screens

### 1. Profile picker

**Purpose.** App entry point. No login screen — the shared iPad opens here. Should feel like walking up to the fridge.

**Layout.** Wrapping horizontal row of cards, 34px gap, left-aligned under a `Who's here?` title and one line of body copy. Kicker `FAMILY APPILY` above the title, followed by a 2px rule filling the remaining width.

**Child card.** 270px min width, 38/30/26px padding, `#FFFFFF` on 3px `#22201E`, 32px radius. Contents, vertically centered, 14px gaps: a tape strip at the top edge (92×26px, `rgba(196,178,140,.5)`, rotated −2°, half outside the card), the child's corner motif at 38px in the top-right, the full mascot illustration at 158px, the child's name at 32px heavy in their `textInk`, then a 16px `dotFill` circle with a 2px outline followed by `N tickets · age N`. Hover lifts 7px and rotates −0.7°.

**Rotation card.** Same footprint, `#F1E7D5` fill, 3px **dashed** border. Three legend dots at 26px across the top; title `Family rotation` and `Six chores · 3-week cycle · week N of 3` at the bottom.

**Tap targets.** The cards are far above 60pt. Nothing critical sits in the top corners.

### 2. Weekly chart (per child)

**Purpose.** The core screen. A child answers "what do I still have to do today?" from across the room.

**Header.** Back button (60×60pt circle, 3px border), the child's 60pt small mark, name at 36px in their `textInk`, subtitle `Week beginning Sunday · rotation week N`. Right side: ticket pill (star token, count at 26px black, `TICKETS` micro-label, 3px border, 999px radius) and an `Adult mode` toggle pill. Below: three tab pills — `Weekly chores`, `Reward chart`, `Earn & spend` — 52pt min height, active tab filled with `textInk` and white text.

**Chart title row.** The child's top motif at 44px, `WEEKLY CHORES` at 38px heavy uppercase in their title color, a 3px rule filling the gap, then the motif mirrored. Bottom motifs mirror the same treatment under the grid, flanking one line of body copy about that child's frame.

**Grid.** 12-column grid. Top row: four cards at `span 3`. Bottom row: three cards at `span 4`. This is the physical layout and must be preserved on iPad and Mac. Collapse to a vertical list on iPhone and Watch; go two-across (`span 6`) at accessibility text sizes.

**Day card.** 26px radius, 3px border, `#FFFFFF`. Structure top to bottom:
1. A 92px illustration well (scales with Dynamic Type) holding the frame's mascot, overflowing the card edges.
2. The frame (see below) holding that day's chores.
3. A footer row: day label at 13px black uppercase +0.16em, and on the right either `N of M` in muted text or, when the day is clear, a `✓ DONE` pill outlined 2.5px in the child's `textInk`. The row wraps rather than overflowing at large text.

**States.**
- *Today* — border switches to the child's `textInk`, day label takes the same color, elevation rises to the "today" shadow, and a `TODAY` pill sits half-outside the top edge in `textInk` with white text.
- *All complete* — background `#F2F7EA`, border `textInk`, mascot switches to its cheering pose, and the `✓ DONE` pill pops in over 300ms.
- *Empty* — a dashed 3px placeholder, 60pt tall: `Free day` (rail) or `Nothing today — go outside` (sign).
- *Partially complete* — footer shows `1 of 2`; completed rows fade to 45% and gain the mark.

### 3. The three card frames

| Child | Frame | Construction |
|---|---|---|
| Finley | `open-book` | Two facing pages on `#FBF7EF`, 3px `#8C7B5E` border, a 3px center gutter, one chore per page as a full-height 60pt tap target. Page text is centered, 15px semibold. |
| Arthur | `bamboo-fence` | The panda peeks over a bamboo rail (17px tall, `linear-gradient(180deg,#8FBF57,#5E8934)`, 2px `#4E7329`, three node ticks). Chores below as 12px-radius rows on white with 3px black borders, 7px gaps. |
| Maryn | `held-sign` | The penguin holds a `#FFFDF8` sign with a 3px black border, 6px radius, 5px padding. Chores stack as 3px-radius rows with 3px gaps. |

**Finley's two-chore cap is a constraint, not a suggestion.** A third chore renders as a *turned page*: a peeking leaf below the spread (`#F2ECE0`, 12px, border-top removed) plus a 60pt `#F7F1E4` button with a `TURNED PAGE` micro-label pinned bottom-right. Never a third open page.

**Rotation-assigned chore.** Marked with a 13px circle in the child's `dotFill` with a 2px outline, plus — on the book frame, where there is room — a `● ROTATION` micro-label. Never color alone. Its label comes from `rotation.json`, resolved automatically; an adult never types it in.

### 4. The completion mark

The single most recognizable element of the whole system, and the thing a child physically reaches for. Get this right.

- Path, in a `0 0 120 104` viewBox: `M10 44C24 42 34 60 47 88 61 62 84 24 110 10`
- Stroke `#1F1F26`, width 13, round caps and joins, no fill.
- **Uniformly scaled** — roughly 54×47pt at default type, scaling with Dynamic Type — and rotated about **−8°**. Do not stretch it to the label's width; a squashed version loses the V and reads as a tilde.
- Positioned absolutely over the center of the chore row, on top of the text, as a **sibling** of the label — not a child. The label fades to 45%; if the mark inherits that opacity it renders grey and stops reading as a drawn check.
- Draw-on: trim from 0 to 1 over ~340ms ease-out. **Reduce Motion:** cross-fade the finished mark in over ~200ms. The state change stays perceptible either way.
- Reward-chart slots use the same path at 72% of the slot, stroke width 13, no rotation.
- Per the accessibility rules the mark cannot be the only signal: text fade + mark + card background/border all change together, and the accessibility value updates to `completed`.

### 5. Reward chart

30 slots, 5 rows of 6, each row's last slot carrying the star token. Slots are circles: filled slots take the row's palette color with a 3px solid border and the completion mark; empty slots are `#F6F1E6` with a 3px dashed hairline border. 10px gaps, scaling with type. The Vault sits bottom-trailing at 96×78px with `VAULT` above it in the child's title color and `N slots to a full chart` beneath.

Progress must be readable **at rest** — a line above the grid states it in words: `N earned — M more to 30 minutes of individual screens.`

Beside it, the spend tiers, identical for all three children: 5 = 30 min shared screen, 10 = 30 min solo screen, 15 = fast food, 20 = $20 shopping spree. Each is a 56pt row with a 48pt cost chip; affordable tiers gain the child's border color, full opacity and a `READY` label. Unaffordable tiers drop to 60% opacity.

### 6. Earn & spend

The earn catalog as 56pt rows, each with a 15px `dotFill` bullet, the label at 16px, and an optional muted note beneath (`+1 for trying new food`; `Trampoline · Monkey bars · Bike riding · Roller skating`).

**Privacy.** Two of Arthur's earn items are health-adjacent and flagged `private: true` in `tickets.json`. They render **only** in Arthur's own profile and for adults. With Adult mode on they carry a `🔒 PRIVATE` chip (Lucide lock, stroke 2.75, 2px hairline border, 999px radius) and a tinted row. With it off they are **absent** — no gap, no count, no placeholder, nothing that reveals something was removed. The explanatory paragraph beneath the list changes wording rather than referencing a hidden item count.

Also on this tab: a clearly-labelled **proposal**, not part of the printed system — one adult-awarded "extra ticket" for a job nobody asked for. It stays inside the ticket economy: no streaks, badges, levels, or second currency. It exists because the parent said Maryn takes on extra tasks and the older two need more pull. It is safe to delete; nothing depends on it.

### 7. Family rotation

Six chores × three week columns. Header row first (`CHORE`, `WK1 · NOW`, `WK2`, `WK3`), then one row per chore. Each cell shows a 30px dot in the assignee's `dotFill` with a 2px outline **and their name beneath in their `textInk`** — never the dot alone. The current week's column is tinted `rgba(198,113,57,.09)`. Grid is `minmax(0,1.6fr) repeat(3, minmax(70px,1fr))`, 2px hairline rules, 26px outer radius, clipped.

Above the table: week selector pills and the legend. Below: an adult-only note that `rotationEpoch` is still `null`.

## Interactions & behavior

- **Navigation.** Profile picker → child chart (three tabs) → back. A separate route to the family rotation from the picker or the bottom bar. No modal stack, no login.
- **Marking a chore.** Tap anywhere in the row. Mark draws on ~340ms, text fades to 45%, card border/background update, ticket count increments, footer count updates. Tapping again reverses all of it. Reversible by children; nothing destructive is.
- **Reward slot.** Tapping slot *N* sets the balance to *N*, or to *N−1* if it was already *N* — so a child can correct by one tap either direction.
- **Adult mode.** A visible toggle in the header for the prototype only. In the app this is a PIN or Face ID gate **at the point of the action** — never at launch.
- **Hover** (Mac / pointer): profile cards lift and tilt; chore rows tint or shift border color; reward slots scale 1.06.
- **Focus.** Every interactive element takes a 3px focus ring in `#1B4F9C` at 2–4px offset. Never the browser or system default.
- **Reduce Motion.** Draw-on becomes a cross-fade; the `✓ DONE` pop becomes a fade. Nothing is removed, only re-expressed.
- **Prototype-only controls.** The bottom bar (`AX5 text`, `Family rotation`) is a review affordance. Do not build it.

## State

| State | Shape | Notes |
|---|---|---|
| Selected profile | child id | Determines role: child vs adult. Not a session. |
| Rotation week | 1–3 | Derived from `rotationEpoch` once set; a picker until then. |
| Completions | `{childID, choreID, date} → bool` | Append-only ledger. Ticket balance is derived, never a stored mutable counter. |
| Ticket balance | derived int, 0–30 | |
| Adult mode | bool | Gated per action in the real app. |
| Dynamic Type | system | Drives every size. Nothing fixed. |

## Assets

All in `family-hub-assets/design/`, all original vector work, all safe to ship. Import as vector-preserved single-scale assets — one source per mascot must serve a 24pt Watch complication and a full-screen iPad chart.

| File | Use |
|---|---|
| `avatars/finley-pizza.svg`, `avatars/finley-pasta.svg` | Finley, alternating by day index so no two adjacent cards repeat |
| `avatars/arthur-panda.svg` | Arthur |
| `avatars/maryn-penguin.svg` | Maryn |
| `motifs/finley-cap.svg`, `motifs/finley-hoodie.svg` | Finley's corners — navy cap top, green hoodie bottom |
| `motifs/arthur-hat.svg`, `motifs/arthur-bamboo.svg` | Arthur's corners — conical hat top, bamboo bottom |
| `motifs/maryn-flower.svg`, `motifs/maryn-icecube.svg` | Maryn's corners — red flower top, ice cube bottom |
| `motifs/star-token.svg` | Reward chart milestone slot |
| `motifs/vault.svg` | Reward chart, bottom-trailing |

The prototype additionally contains **refined** versions of the mascots — shaded illustration variants, cheering poses for the all-complete state, and simplified 24pt small marks — drawn from the same geometry and palette as the SVGs above. Lift them from the `<symbol>` definitions at the top of the HTML file (`illPanda`, `illPandaPeek`, `illPandaCheer`, `illPenguin`, `illPenguinCheer`, `illPizza`, `illPasta`, `mkPanda`, `mkPenguin`, `mkPizza`) and export each as its own asset.

**Licensing.** The original wall charts came from a commercial printable template. Every asset here is original line work matching the motif and palette — none of it traces the clip-art in the photographs. Keep it that way.

## Files in this bundle

| File | What it is |
|---|---|
| `PHASE0_PROMPT.md` | **Start here.** The prompt to paste into Claude in VS Code, plus the attach list. |
| `README.md` | This document. |
| `BUILD_SPEC_from_repo.md` | The repo's `CLAUDE.md` build spec — rename it back to `CLAUDE.md` at the repo root. |
| `contracts-decision.md` | The original open backend question. Answered in `PHASE0_PROMPT.md`. |
| `family-hub-assets/data/*.json` | The three data contracts. |
| `family-hub-assets/design/tokens.json` | Source of truth for color and type. |
| `family-hub-assets/design/avatars/`, `motifs/` | The 12 SVGs. |
| `family-hub-assets/preview.html` | The repo's own asset preview page. |
| `prototype/Family Appily.dc.html` | The approved design reference. Open in a browser. |
| `prototype/support.js`, `prototype/_ds/` | Runtime the prototype needs. Not app code. |
