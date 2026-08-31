# Prompt for Claude Design — Family Appily

*Copy everything below the line into Claude Design, and attach the files listed in §2.*

---

## 1. What this is

I'm building a family-management app for my household — three kids, four Apple platforms. It replaces a set of physical charts that currently live on our walls and actually work. **The job is to digitize a system that already works, not to redesign it.**

The physical system has three interlocking pieces:

1. **A personal weekly chore chart per child** — seven day-cards, each listing that day's chores.
2. **A shared family rotation chart** — six household chores that rotate between the three kids.
3. **A ticket economy** — kids earn tickets for chores and daily habits, tracked on a 30-slot reward chart, spent on screen time and treats.

Each child has their own complete visual world built around an animal or food mascot. That theming is the heart of it and must carry everywhere — not just the chore chart, but the calendar, the task list, the widget, the watch face.

I need two things from you: **refined mascot artwork**, and **the chore-tracking card components** built around it.

## 2. What's attached

**Photographs of the physical charts** — these are the source of truth for content, layout, and spirit:
- Three `WEEKLY CHORES` charts (one per child: pizza, panda, penguin)
- `FAMILY CHORE CHART` — the colored-dot rotation grid
- `HOW TO EARN TICKETS` / `HOW TO SPEND TICKETS` sheet
- `REWARD CHART` — the 30-circle tracker with the Vault

**Starting-point SVGs** — functional but plain. Treat these as geometry and palette reference, and elevate the craft:
- `finley-pizza.svg`, `finley-pasta.svg`, `arthur-panda.svg`, `maryn-penguin.svg`
- `star-token.svg`, `vault.svg`
- Corner motifs: `finley-cap`, `finley-hoodie`, `arthur-hat`, `arthur-bamboo`, `maryn-flower`, `maryn-icecube`

## 3. Licensing — read before drawing

The original charts were made from a commercial printable template. **Do not trace, copy, or closely reproduce the clip-art characters in the photographs.** Draw original illustrations that match each motif, palette, and personality. My kids should recognize their character instantly; the linework must be yours. The attached SVGs are already original and safe to build from.

## 4. The three visual worlds

| Child | Mascot | Card frame | Corner motifs |
|---|---|---|---|
| **Finley** | Pizza slice and pasta bowl, alternating by day | **Open book** — one chore per facing page | Navy cap (top), green hoodie (bottom) |
| **Arthur** | Panda | **Bamboo fence rail** — chores on the rail, panda peeking over | Conical hat (top), bamboo stalks (bottom) |
| **Maryn** | Penguin | **Held sign** — penguin holds up a rectangular sign | Red flower (top), ice cube (bottom) |

Finley's open-book frame holds **exactly two chores** — one per page. That constraint comes from the physical chart. Respect it, or propose a different frame; don't let a third chore break the metaphor.

## 5. Identity colors — non-negotiable

Two color systems exist in the photos, and they conflict. **The rotation chart's legend wins**, because it's the convention my kids already read off the wall. Mascot artwork colors are decorative fill only.

| Child | Dot fill | Text / UI |
|---|---|---|
| Finley | `#1B4F9C` (blue) | `#1B4F9C` — 7.94:1 |
| Arthur | `#5CB85C` (green) | `#3E7D36` — 5.01:1 |
| Maryn | `#E04E2C` (orange) | `#BF3A1E` — 5.47:1 |

The dot fills for Arthur and Maryn fail AA on white (2.48:1 and 3.97:1). They may be used **as filled shapes only, never as text or as the sole indicator of anything.** Mascot palette colors — pizza gold `#F0B440`, ice blue `#9ED2EE`, bamboo `#7CAD48`, hat orange `#D18B4A` — are illustration fill only, same rule.

Body text and outlines: `#1F1F26`. Paper: `#FFFFFF` light, `#1C1C1E` dark.

## 6. Accessibility — these are hard requirements

Every component you design has to survive all of these. If a design can't, it's the wrong design.

- **Dynamic Type to AX5.** No fixed text sizes, no fixed-height text containers. Cards must grow gracefully; truncation or clipping is a failure, not a tradeoff. Show me each card at default size *and* at AX5.
- **Tap targets** 44×44pt minimum, **60×60pt** for anything a child taps (marking a chore done, picking a profile).
- **Never color alone.** A completed chore changes color *and* gains a mark *and* changes card state.
- **Light and dark mode**, both designed, not auto-derived.
- **Reduce Motion** — any animation needs a static or cross-fade equivalent that still communicates the state change.
- Nothing critical in the top corners; primary actions sit in the lower third.

## 7. Deliverables

### Tier 1 — do these first

**A. Refined mascot set.** Each child's mascot at three sizes: full illustration (chart hero), medium (card header), and a simplified small mark that stays legible at 24pt for a Watch complication and calendar event dot. The small mark is the hard one — it must read as *that specific child* at a glance.

**B. The chore card.** The core component, in all three frame styles. States needed:
- Empty / no chores that day
- One chore, two chores (and Finley's two-page book at both)
- One of two complete
- All complete — this should feel genuinely good
- Today vs. other days
- The rotation-assigned chore, visually distinguished from fixed daily chores

**C. The completion mark.** Currently a hand-drawn black check struck across the chore text. It's the single most recognizable element of the whole system and the thing a kid physically reaches for. Keep the hand-drawn irregularity — not a tidy SF Symbol in a circle. Design the mark, its draw-on animation, and its Reduce Motion fallback.

**D. The weekly chart view.** Seven day-cards in the physical layout: **four across the top row, three across the bottom.** Preserve that grid on iPad and Mac. Show me the iPhone collapse to a vertical list.

### Tier 2

**E. Reward chart.** 30 slots, 5 rows of 6, a star token in each row's last slot, Vault in the bottom-trailing corner. Per-child palette. Progress must be readable *at rest* — a kid should see how close they are to 5 tickets from across the room without tapping.

**F. Earn / spend sheets.** The ticket catalog, themed per child. Spend tiers are identical for all three: 5 = 30 min shared screen, 10 = 30 min solo screen, 15 = fast food, 20 = $20 shopping spree.

**G. Profile picker.** The app's entry point. No login screen — mascot-based selection, one tap, names beneath. Must feel like walking up to the fridge.

**H. Family rotation view.** Six chores × week columns, colored dots per the legend in §5. Include a clear "this is the current week" treatment.

## 8. Things not to do

- **Don't add gamification we didn't design.** No streaks, badges, levels, leaderboards, or confetti storms. The physical system has tickets and a vault. That's the whole economy.
- **Don't make it look like a productivity app.** It should feel like our kitchen wall — handmade, warm, a little whimsical. Not Asana.
- **Don't design a login screen.** Adult-only actions get gated inline at the point of action, never at launch.
- **Don't use a custom display font** unless it supports the full Dynamic Type range. Rounded system fonts are the safe default: rounded heavy uppercase for titles, rounded bold uppercase for day labels, plain system for chore text.

## 9. One privacy constraint

One child's earn list includes therapy-related activities. Anything I flag as private renders **only** in that child's own profile and for adults — never in shared family views, never on a widget on the shared iPad, never in an export. If you design a "family overview" screen, it needs a mechanism for hiding those items that doesn't make their absence conspicuous.

## 10. Output

- Vector throughout, light and dark variants. No fixed-size raster.
- Mascots exported so they scale from 24pt to full screen from one source.
- For each component, show default size and AX5.
- A short spec sheet per component: spacing, corner radii, stroke weights, the color token used for each element.

Target platforms are iPhone, iPad, Apple Watch, and Mac, built in SwiftUI. Design for iPad first — the shared family iPad is where the kids actually use this, and it's the closest analogue to the chart on the wall.
