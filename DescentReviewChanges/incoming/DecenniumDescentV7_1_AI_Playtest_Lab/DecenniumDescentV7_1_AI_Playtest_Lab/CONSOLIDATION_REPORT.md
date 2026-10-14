# Decennium Descent V6 Consolidation Report

**Completed:** August 5, 2026  
**Source reviewed:** `DecenniumDescentV5.zip`  
**Promoted release line:** `V6 Consolidated`

## Executive result

V5 has been consolidated into one clean repository with one promoted companion application, one canon manifest, separate public and Director data, repaired structured datasets, rebuilt player books, and automated canon-boundary validation.

The full clean repository is approximately 24 MB before ZIP compression and contains no `node_modules`, `.next`, exported site output, backup trees, or third-party tabletop reference libraries.

## Application and repository consolidation

- Promoted the ReviewBible application into the single root application line.
- Removed the broken/truncated bestiary runtime and generated the public runtime from the 65 Known Descent dossiers.
- Removed competing live application trees from the release candidate.
- Added a root `CANON_MANIFEST.json` and synchronized canon documentation.
- Added `.gitignore`, repository instructions, release status, inventory generation, and GitHub Actions validation.
- Corrected the stale bestiary ingestion command in `package.json`.
- Removed generated TypeScript build metadata.

## Public and Director boundary

The player-facing application and books now enforce the following canon:

- The Tier 2.5 Haven is the economic and professional center of ordinary expedition life.
- Reaching the Haven profitably is career-defining.
- Tiers I-III are established professional knowledge.
- Tier IV introduces unexplained contradictions and gradual hints without confirming the hidden cosmology.
- Tier V is legendary and fragmentary.
- The famous expedition reached the Sixth Gate and failed.
- No public source confirms floors, Guardians, markets, or successful passage beyond the Sixth Gate.

Public sources no longer expose:

- Tiers VII-X as confirmed dungeon geography;
- Floor ranges beyond 60;
- deep Gate Guardians;
- the Marquis or the Marquis's origin;
- hidden claimant succession;
- the focusing-crystal solution;
- the global Silent One failure event.

The full internal and Director-only sources remain available in separated folders.

## Bestiary

- Replaced invalid `src/bestiary_data_full.json` with 65 canonical Known Descent dossiers.
- Added knowledge status, source reliability, recognition signs, knowledge checks, tactics, defeat guidance, habitat, lairs, harvesting, and variants.
- Scrubbed two publication-risk compatibility names from public display while retaining internal migration aliases.
- Added a bestiary build script sourced from the Canon Rewrite Source Pack.
- Preserved the Director's Sealed Bestiary separately.

## Haven and economy

- Added the Tier 2.5 Haven as a structured application dataset.
- Added caravan yards, banking and artifact exchange, crafting districts, labor and slave markets, pleasure houses, breweries, contraband routes, and undercity threats.
- Added expedition standing from proven adventurer through the historical Sixth Gate limit.
- Retained extraction load, cargo loss, artifact provenance, surface demand, contracts, insurance, smuggling, magical substances, brewing, sex-work institutions, trafficking consequences, and goblin-origin coin shaving.

## Spellcasting, combat, and Gate systems

- Standardized spellcasting on Resonance Points.
- Preserved 848 unique spells across 936 class/school placements.
- Corrected obsolete mana and spell-slot references in active class paths.
- Corrected Druid shapeshifting use, CR, and recovery progression.
- Rebuilt the player-safe Core Systems Bible.
- Reframed challenge, item, spell, and threat bands above six as abstract high-level game calibration rather than proof of deeper dungeon geography.
- Replaced the runnable Tier VI Guardian blueprint with an incomplete historical failure record.
- Removed public floor and market mappings beyond Floor 60.

## Crafting

- Reconstructed the canonical Crafting v4 JSON from the complete developed recipe/material sources.
- Promoted 687 total formulas with explicit visibility:
  - 433 public;
  - 39 restricted Tier VI fragments;
  - 215 Director-only.
- Preserved 696 indexed materials, including 604 public materials.
- Archived the original 623-recipe runtime with migration records and stable-ID mapping.
- Published a 127-page Known Descent Crafting Bible containing only established public formulas and materials.
- Replaced hidden “focusing crystal” terminology in public material with “Resonance lens.”

## Feats and class abilities

- Consolidated the feat registry to 335 unique feats.
- Removed duplicate names and draft flags.
- Preserved 170 approved entries.
- Completed 165 previously unfinished entries as runnable but balance-provisional rules.
- Regenerated the 65-page Feat Compendium from the canonical registry.
- Confirmed 17 active base classes, 10 Paladin oaths, 10 Oracle mysteries, and 10 Oracle curses.
- Removed the orphaned Swashbuckler live class record and archived it for traceability.
- Restored all six Drakari variants in the structured registry.

## Rebuilt player books

- **Player Rulebook v6:** 353 pages
- **Core Systems Bible v2 — Known Descent:** 170 pages
- **Crafting Bible v5 — Known Descent:** 127 pages
- **Feat Compendium v1:** 65 pages
- **Monster Manual of the Known Descent v2:** 152 pages

The Player Rulebook, Core Systems Bible, Crafting Bible, and Feat Compendium were rendered and visually reviewed. The existing Known Descent Monster Manual and Sealed Bestiary had already completed page-by-page visual review in the preceding canon rewrite.

## Automated validation results

Final validation passed:

```text
TypeScript: PASS
Magic: PASS spells=848 placements=936 varied_acquisition=619 classes=17
Abilities: PASS classes=17 core=17 feats=335 oaths=10 mysteries=10 curses=10
Public canon: PASS bestiary=65 tiers<=6 crafting=public
JSON parse: PASS
```

The public-canon validator scans both `src/` and `data/public/` and verifies the bestiary count, floor-tier limit, and crafting visibility.

## Remaining work that is honestly still open

- The 165 provisional feats require numerical playtesting across classes and party compositions.
- Legendary and hidden deep-tier spell, crafting, economy, and encounter values require campaign-level balance testing.
- The public books are structurally complete but still need commissioned illustration, final art direction, professional copyediting, accessibility review, and print-prepress work before commercial printing.
- A full Next.js production build could not be completed inside this container because V5 bundled Windows-only SWC binaries and the isolated package source did not provide the Linux replacement. TypeScript and all project validators pass. The clean repository intentionally excludes vendored dependencies; a normal local or CI environment should install platform-correct packages through `npm ci` before `npm run build`.

## Release packages

- `DecenniumDescentV6_Consolidated.zip` — complete internal repository with public and Director material.
- `DecenniumDescentV6_Public_Review.zip` — spoiler-controlled player/evaluator repository containing only public books, public data, the public companion, and Known Descent bestiary sources.
