repo: mspaldingworks/Family_Appily_app
branch: main
path: family-hub-assets

## Last sync
date: 2026-08-01T12:24:30Z
commit: 7a02be3deabd77ea3e4db912d91aff24dbbf6f7d

### Updated in this project
- Extracted the unpushed `7a02be3` commit from the uploaded git bundle into `repo/app/` (the GitHub remote still only has `Initial commit`).
- Built `Family Appily.dc.html` from `CLAUDE.md` + `family-hub-assets/` — profile picker, per-child weekly chore chart, reward chart, earn/spend sheets, family rotation.
- Refined the four avatar SVGs and eight motif SVGs into shaded illustration + 24pt small-mark versions; added cheering poses for the all-complete state.
- Proposed one addition not on the wall: an adult-awarded "extra ticket" (inside the existing economy, no new currency).

## Screen map
| Screen | Built from |
| --- | --- |
| Profile picker | CLAUDE.md §3.5, §7.1; family.json `children`; design/avatars/*.svg; design/motifs/* |
| Weekly chore chart (all 3 children) | family.json `schedule` + `chores`; tokens.json `cardFrames`, `layout`; CLAUDE.md §7.2, §7.3 |
| Chore card frames (book / rail / sign) | tokens.json `cardFrames`; CLAUDE.md §7.1 note on Finley's two-page cap |
| Reward chart + Vault | tickets.json `rewardChart`, `chartPalettes`; motifs/star-token.svg, motifs/vault.svg |
| Earn & spend | tickets.json `earnCatalog`, `spendTiers`, `privacyRule`; CLAUDE.md §7.7 |
| Family rotation | rotation.json `formula`, `chores`, `siblingLegend`, `verification` |
| Identity colors, type, a11y | tokens.json `children`, `typography`; CLAUDE.md §3.1–3.7, §7.4, §7.5 |

## Notes
- The API repo `mspaldingworks/Famiy_Appily_api` (typo, missing `l`) holds mirrored contracts; app repo is source of truth until `ARCHITECTURE_DECISION.md` is resolved.
- `rotationEpoch` is still `null` — "this week" is a UI selector in the prototype, not real data.
