# Decennium Descent

This is the consolidated V7.2 repository for the Decennium Descent tabletop and companion application. It replaces the competing root/ReviewBible application lines found in V5 and incorporates the V7 playtest evidence review.

## Start here

1. Read `CANON_MANIFEST.json`.
2. Run `npm ci`.
3. Run `npm run validate:rules`.
4. Run `npm run dev` for the companion or `npm run build` for a production build.

## Canon layout

- `src/` — promoted player-facing companion application.
- `books/player/` — public rulebooks and compendia.
- `books/director/` — internal and Director-only full-system publications.
- `data/public/` — player-safe structured data.
- `data/director/` — hidden continuity and full internal datasets.
- `data/crafting/` — canonical 687-recipe crafting database with visibility flags.
- `docs/bestiary/...Known_Descent...` — canonical public monster source entries.
- `docs/bestiary/...Directors_Sealed...` — canonical Director bestiary entries.

## Canon boundary

The public historical record ends at the failed Sixth Gate. Tiers VII-X, the Marquis origin, claimant succession, the Old God crystal path, and global failure consequences are never imported into `src/`. `tools/validate_public_canon.py` enforces this boundary.

## Build note

Dependencies and generated Next.js output are deliberately excluded from the repository. Install dependencies locally with `npm ci`; do not commit `node_modules`, `.next`, or exported site output.

## V7.2 gameplay loop

The complete playable loop is defined in:

- `docs/mechanics/DESIGN_DOCTRINE.md`
- `docs/mechanics/GAMEPLAY_LOOP_CANON.md`
- `data/public/Decennium_Descent_Gameplay_Loop_v1_2.json`
- `books/player/Decennium_Descent_Gameplay_Loop_Bible_v1_2.docx`
- `src/components/ExpeditionTracker.tsx`

The companion now separates round-by-round **SESSION** play from Watch-by-Watch **EXPEDITION** play.

Empirical testing programs are under `playtests/cursor-packs/`. Pack 06 requires fixed builds and complete dice-level transcripts before numerical combat changes are promoted. Each pack includes an orchestrator prompt, fixed scenarios, dedicated agent files, a JSON result schema, and a report compiler.
