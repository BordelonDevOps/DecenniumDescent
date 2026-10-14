# Repository Guide

This repository is the **distributable, investor-readable source package** for Decennium Descent. Historical scratch files, dependency caches, generated builds, redundant text extracts, superseded manuals, and third-party reference books are intentionally excluded.

## Canon Hierarchy

1. **Current owner-approved canon locks** documented in `docs/canon/` and `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`.
2. **Player Rulebook** for player-facing mechanics and public setting truth.
3. **The Director's Crucible** for Director-facing truth, secrets, and adjudication.
4. **Current structured companion data** where it faithfully mirrors the books.
5. **Mechanics and playtest documents** as implementation, validation, or design evidence; these do not silently override published canon.

## Primary Books

### Player
- `decennium descent player rulebook.docx`

### Director
- `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx`
- `docs/manuals/Instruments_of_the_Weave.docx`
- `docs/manuals/Chronicle_of_the_Decennial_Opening.docx`
- `docs/manuals/Decennium_Descent_Bestiary_of_Aethel.docx` — development bestiary; see publication-status note
- `docs/manuals/Codex_of_the_Heartcell.docx` — development ecology/stat companion; see publication-status note

Markdown mirrors are retained when they are useful for search, review, or automation.

## Canon Briefs

`docs/canon/` contains compact statements of the current setting architecture. These documents exist to prevent future edits from drifting back toward older generic-fantasy assumptions.

## Mechanics

`docs/mechanics/` retains current authoritative or useful design references. Superseded handoff notes, raw scans, and completed migration-only scripts have been removed. A small number of dated implementation-track documents are retained where they still describe active work or support current toolkits.

## Development Status

`docs/development/` records material that is useful to evaluate the pipeline but is not yet final commercial copy, especially the bestiary scaffold.

## Playtest Evidence

`docs/playtest/` is curated rather than exhaustive. It keeps representative scenarios, campaign reports, newcomer guides, Matrix/creation-purpose material, and current issue/balance evidence without carrying every superseded iteration.

## Structured Data and App

- `src/` — Next.js application and production game data
- `scripts/` — maintained data/content workflows
- `tools/` — maintained canon-ingestion and validation tools
- `Bestiary.xlsx` — monster source table
- `decennium_descent_crafting_recipes_validated.xlsx` — crafting source table

## Deliberately Excluded

- `node_modules/`
- generated `out/`, `.next/`, and local build artifacts
- backups and pre-edit Word files
- third-party D&D/Pathfinder PDFs
- redundant modular Word files already compiled into the Player Rulebook
- unreferenced raw Word/text extraction output (selected UTF-8 ingest/search mirrors are retained where current tools depend on them)
- temporary Python analysis scripts
- superseded Director manual drafts
- historical continuity/audit reports whose decisions are now incorporated into canon

Dependencies are reproducible with `npm ci`; no dependency vendor folder is required in Git.
