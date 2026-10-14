# Decennium Descent — Investor Overview

## The Product

Decennium Descent is designed as a **repeatable tabletop and digital RPG platform**, not a single linear adventure. Its core campaign structure is a 100-floor dungeon that opens every ten years for 100 days. Adventurers, governments, religions, mercenary companies, banks, scholars, and criminal organizations all organize around that event.

The dungeon therefore generates two games at once:

1. **The descent:** tactical exploration, combat, resource pressure, discovery, faction decisions, and survival.
2. **The consequence:** wealth, relics, casualties, discoveries, political leverage, institutional power, and historical change on the surface.

A campaign can end with an expedition. The setting does not. Each Opening can inherit consequences from the last.

## The Signature Hook

The dungeon publicly appears to be a divine Crucible created by Calan'thir and Asmodeus. That explanation is intentionally sufficient for ordinary players and citizens of Aethel.

Director material contains a deeper explanation: the Crucible encloses an older mechanism whose survival function depends on preserving meaningful possibility, difference, choice, memory, identity, and will. The dungeon's prizes are therefore not merely rewards. They are incentives that draw civilization into consequential action.

This gives conventional RPG activities—loot, rival expeditions, faction conflict, political bargaining, crafting, reputation, risk, even the fixed 100-day clock—a shared thematic purpose.

## Core Design Pillars

### 1. Consequence over reset
The world should remember what players do. Expeditions change markets, factions, scholarship, reputations, settlements, and future access.

### 2. Different truths at different depths
Player-facing mythology remains playable and internally coherent. Director-facing canon reveals deeper layers gradually instead of invalidating the public setting with an exposition dump.

### 3. Build identity through systems
Seventeen base classes use distinct combat resources and progress through Arch and Hero development. Hero Paths express a philosophy of using power rather than a universal Good/Neutral/Evil scoreboard.

### 4. Make the clock matter
The 2,400-hour Opening and 1,200-hour Horn force commitment. Time pressure turns an abstract option into a choice with cost.

### 5. Make the surface part of the dungeon
Expedition finance, salvage rights, insurance, war credit, guilds, faiths, families, and governments all react to each Opening. A recovered object can matter more in Aethel than it did on the floor where it was found.

## Current Product Assets

- Player Rulebook
- Complete Director's Crucible
- Bestiary development pipeline and structured monster database; Aethel-authored material is separated from compatibility/prototype placeholders still awaiting publication rewrite
- 100-floor / 10-tier campaign framework
- Resonance magic framework
- 17 base classes with Arch/Hero paths
- 14 player peoples with variants
- crafting and component systems
- reputation and expedition systems
- curated simulation/playtest corpus
- Next.js companion application
- structured source data and ingestion utilities

## Why the Repository Matters

This package is intentionally organized so an evaluator can see both the **creative IP** and the **implementation discipline** behind it:

- polished sourcebooks show the product vision;
- canon briefs show how hidden lore is controlled;
- mechanics documents show system depth and continuity management;
- playtests show attempts to break and validate the game;
- structured data shows the material is already being translated into a digital product;
- the companion application demonstrates a path toward persistent player tooling and future game integration.

## Suggested Review Path

1. `README.md` — product and repository orientation
2. `decennium descent player rulebook.docx` — player experience
3. `docs/canon/PLAYER_DIRECTOR_BOUNDARY.md` — spoiler architecture
4. `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` — complete Director vision
5. `docs/canon/THEMATIC_DESIGN_LANGUAGE.md` — Matrix-driven encounter design
6. `docs/CURRENT_SYSTEM_STATUS.md` — current implementation and maturity snapshot
7. `src/` — companion implementation

> **Spoiler warning:** Director and `docs/canon/` files contain the setting's deepest secrets and are intended for evaluators, Directors, and development partners rather than ordinary players.
