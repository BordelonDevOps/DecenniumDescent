# Decennium Descent

**Decennium Descent** is a tabletop role-playing game and companion application built around a 100-floor dungeon that opens once every ten years for exactly **100 days (2,400 hours)**. At **day 50 / hour 1,200**, the Horn marks the point of no return.

The public promise is simple: descend, survive, recover impossible treasures, and return wealthy enough to change the world.

The deeper game is about what those choices do to people, institutions, history, and Aethel itself.

## What Makes It Distinct

- **A 100-floor campaign engine.** Ten tiers, Gate Guardians at major thresholds, expedition logistics, persistent consequences, and a fixed real in-world clock.
- **The dungeon changes the surface.** Recovered relics, expedition finance, faction decisions, casualties, discoveries, and alliances alter politics and future cycles.
- **17 base classes with layered progression.** Characters begin with a base class, develop through Arch specialization, and reach Hero Paths defined by philosophy and method rather than a simplistic moral label.
- **Resonance-based magic.** The setting's magic system is tied directly to its cosmology and uses Resonance Points or class-specific resources instead of generic multiclass spell-slot logic.
- **Player truth and Director truth are intentionally different.** Players encounter the public history of the Crucible. Director material contains the deeper cosmology, the Heartcell, the Silent Ones, false resonance, and the Matrix of Oblivion.
- **A digital companion.** The Next.js application provides character, class, spell, bestiary, crafting, dungeon, and session-reference tools backed by structured canon data.

## Repository Tour

| Path | Purpose |
|---|---|
| `decennium descent player rulebook.docx` | Authoritative player-facing rules and setting book |
| `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` | Authoritative Director book; contains major spoilers |
| `docs/manuals/` | Current Director supplements, bestiary, Chronicle, and table toolkits |
| `docs/canon/` | Compact canon briefs and player/Director boundaries |
| `docs/mechanics/` | Current rules, balance, progression, continuity, and system design references |
| `docs/playtest/` | Curated campaign simulations and playtest evidence |
| `docs/development/` | Publication-readiness and development-status notes |
| `src/` | Companion application source and structured game data |
| `scripts/`, `tools/` | Maintained ingestion, validation, and content-generation utilities |
| `Bestiary.xlsx` | Structured monster source data |
| `decennium_descent_crafting_recipes_validated.xlsx` | Structured crafting source data |

For a guided review, start with [`INVESTOR_OVERVIEW.md`](./INVESTOR_OVERVIEW.md) and [`REPOSITORY_GUIDE.md`](./REPOSITORY_GUIDE.md).

## Companion App

Requirements: Node.js 20+ and npm.

```bash
npm ci
npm run build
npm run dev
```

Development runs on `http://localhost:8500`.

## Canon Snapshot

- **Opening:** 2,400 hours / 100 days
- **Horn / point of no return:** hour 1,200 / day 50
- **Dungeon:** 100 floors, organized into 10 tiers
- **Selectable base classes:** 17
- **Player cosmology:** mortal religions and the public Calan'thir/Asmodeus Crucible tradition
- **Director cosmology:** Heartcell, Silent Ones/Old Ones, Matrix of Oblivion, true and false resonance

## Content Boundaries

Director files intentionally contain campaign-ending spoilers. The Player Rulebook should never directly reveal the Heartcell's complete purpose, the true identity of the Silent Ones, or the full Matrix mechanism.

Third-party reference books, local dependency folders, generated build output, private backups, and superseded development audits are intentionally excluded from this distributable repository.

## Project Status

The repository contains a playable rules foundation, current player and Director books, structured class/race/spell/bestiary/crafting data, floor and expedition material, multiple simulation/playtest reports, and a functioning web companion. Remaining work is tracked in the current mechanics roadmap rather than in historical audit files.

## Rights

Decennium Descent, Aethel, its setting material, game text, original characters, original mechanics expression, companion application, and associated original content are the property of the project creator unless otherwise noted. This repository is provided for evaluation and development; no license to redistribute or commercialize the IP is granted by its inclusion here.
