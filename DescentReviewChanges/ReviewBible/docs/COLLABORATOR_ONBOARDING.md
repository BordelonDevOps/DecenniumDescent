# Collaborator Onboarding

This document is the fastest way for a new developer, writer, designer, or evaluator to enter the Decennium Descent project without reintroducing retired assumptions.

## Start Here

1. `README.md`
2. `REPOSITORY_GUIDE.md`
3. `docs/canon/CANON_CORE.md`
4. `docs/canon/PLAYER_DIRECTOR_BOUNDARY.md`
5. `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`
6. the Player Rulebook or Director's Crucible for the area you are changing

## Non-Negotiable Baselines

- Opening: **2,400 hours / 100 days**
- Horn / point of no return: **1,200 hours / day 50**
- Dungeon: **100 floors / 10 tiers**
- Base classes: **17 selectable classes**
- Fighter and Swashbuckler are legacy aliases only, not selectable classes
- Use **Umbrin**, not the retired Drow product terminology
- Weave casting uses **Resonance Points** unless a class has an explicitly different resource
- Oracle uses **Revelation Charges**
- Player Appendix B is mortal religion/cosmography, not omniscient proof of objective cosmology
- Silent Ones / Old Ones / Heartcell / complete Matrix mechanism are Director-level spoilers

## Canon Ownership

- Player-facing mechanics or public lore: edit the Player Rulebook first.
- Director secrets or deep cosmology: edit the Director's Crucible / `docs/canon/` first.
- UI/data: mirror canon; do not silently redefine it.
- Playtest material: evidence, not automatic canon.

## Class Architecture

The current selectable roster is maintained in `src/data/canon-classes.js`.

Characters use a three-stage identity:

**Base Class → Arch specialization → Hero Path**

Hero Paths describe **philosophy, method, and consequence**, not an objective Good/Neutral/Evil verdict.

## Thematic Test

When adding substantial content, ask:

1. What meaningful alternatives exist?
2. What choice has a real cost?
3. What changes because of the decision?
4. Who remembers or interprets the result differently?
5. What does the event do to identity, will, or future possibility?

Use `docs/canon/THEMATIC_DESIGN_LANGUAGE.md` for the full Matrix design grammar.

## App Development

```bash
npm ci
npm run lint
npm run build
npm run dev
```

The development server runs on port `8500`.

## Before You Finish a Change

- check the authoritative book/canon file;
- update any structured mirror affected by the change;
- search for retired terms or contradictory clocks;
- run `npm run lint` and `npm run build` for app changes;
- visually render and inspect edited Word books;
- leave the repository cleaner than you found it.
