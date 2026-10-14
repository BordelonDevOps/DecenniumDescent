# Decennium Descent — Investor and Development Overview

## The product

Decennium Descent is a repeatable tabletop and digital RPG platform centered on a 100-floor dungeon that opens once every ten years for 100 days. Adventurers, governments, faiths, mercenary companies, banks, scholars, craftspeople, and criminal organizations organize around each Opening.

The design creates two connected games:

1. **The descent:** tactical exploration, combat, resource pressure, discovery, faction decisions, and survival.
2. **The consequence:** recovered wealth, artifacts, casualties, discoveries, political leverage, institutional power, and long-term change in Aethel.

A campaign can end with an expedition. The setting continues into the next Opening, inheriting the consequences of the last.

## Signature strengths

### Persistent consequences
Expeditions change markets, factions, scholarship, reputations, settlements, and future access rather than resetting the setting after a single campaign.

### Layered discovery
Player-facing knowledge is complete enough to support play while deeper truths remain controlled in Director material. The public record ends with the famous expedition that failed at the Sixth Gate.

### Distinct class identities
Seventeen base classes use protected resource loops and progress through Arch and Hero development rather than sharing one generic ability chassis.

### A meaningful clock
The 2,400-hour Opening and the 1,200-hour Horn force expeditions to make logistical and strategic commitments.

### The surface is part of the dungeon
Salvage rights, insurance, artifact finance, guilds, faiths, families, governments, contraband, and the Tier 2.5 Haven all respond to expedition activity.

## Current V6 assets

- A 353-page Player Rulebook
- A 169-page player-safe Core Systems Bible
- A 127-page Known Descent Crafting Bible
- A 65-page Feat Compendium containing 335 unique feats
- A 152-page Monster Manual of the Known Descent
- Separate Director-only system and bestiary volumes
- 848 unique spells across 936 class/school placements
- 17 base classes with Arch and Hero paths
- 14 player peoples with variants
- 687 canonical crafting formulas with visibility controls
- A Next.js companion application
- Structured source data, migration records, validators, and build scripts

## Repository discipline

The V6 package consolidates the competing V5 application lines into one root application. It includes:

- a single canon manifest;
- separate public and Director data;
- automated public-spoiler validation;
- stable-ID migration records;
- clean Git exclusions;
- a CI validation workflow;
- no vendored dependencies or generated Next.js output.

## Suggested review path

1. `README.md` — repository orientation
2. `INVESTOR_OVERVIEW.md` — product summary
3. `books/player/Decennium_Descent_Player_Rulebook_v6.docx`
4. `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`
5. `books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx`
6. `books/player/Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx`
7. `books/player/Decennium_Descent_Feat_Compendium_v1.docx`
8. `RELEASE_CANDIDATE_STATUS.md` — implementation and validation status
9. `src/` — companion application
10. `CANON_MANIFEST.json` — authority and visibility registry

Director-only folders contain spoilers and are intended for internal development, authorized evaluators, and game Directors.
