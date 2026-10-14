# V6 Consolidated Release Candidate

**Generated:** 2026-08-05

## Completed

- Promoted ReviewBible into the single root application line.
- Replaced the invalid/truncated live bestiary with 65 Known Descent dossiers.
- Added source reliability, knowledge checks, tactics, defeat guidance, lairs, and harvesting to the public monster runtime.
- Removed public Tiers VII-X, deep Guardians, claimant mechanics, Marquis truth, and crystal-path disclosures.
- Added the Tier 2.5 Haven economy and professional standing structure.
- Corrected Druid progression and Lich/Necromancer Resonance terminology.
- Reconstructed and promoted Crafting v4 JSON: 687 total, 433 public, 39 restricted Tier VI, 215 Director-only.
- Archived the legacy 623-recipe runtime with stable-ID migration records.
- Consolidated feats to 335 unique runnable entries: 170 approved and 165 provisional for final balance review.
- Regenerated the Player Rulebook, public Crafting Bible, Feat Compendium, and player-safe Core Systems Bible.
- Added public-canon validation, clean Git exclusions, and GitHub Actions validation.

## Validation

The source candidate passed:

- TypeScript `tsc --noEmit`
- Magic system validator: 848 unique spells / 936 placements / 17 classes
- Ability validator: 17 classes / 335 feats / 10 oaths / 10 mysteries / 10 curses
- Public canon boundary validator: 65 bestiary dossiers, documented tiers only, public crafting formulas only
- JSON parsing for promoted runtime and canonical databases

## Remaining balance work

The 165 provisional feats have complete playable wording but require full-system numerical playtesting. Legendary and deeper Director-only crafting, spell, and encounter values likewise remain subject to final campaign balance testing. These are balance-review items, not missing text or broken runtime records.

## Environment note

A full Next.js production build could not be completed inside the consolidation container because the V5 archive carried Windows-only SWC binaries and the isolated package gateway did not provide the Linux replacement. The clean repository excludes all vendored dependencies; CI and local development install the correct platform package through `npm ci`.
