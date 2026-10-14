# Decennium Descent — Mechanics Roadmap

This roadmap tracks **remaining product work**, not historical migrations that have already been incorporated into the books.

## Completed Baseline

- [x] 17-class selectable roster aligned across Player Rulebook and companion
- [x] Umbrin naming aligned across retained books and production data; legacy Drow aliases remain only for save migration/documented terminology history
- [x] Resonance + Dissonance established as the generic Weave economy; Refrain prevents spell/cantrip spam
- [x] 848 unique spells / 936 school-rank placements reconciled; shared spells support class-specific acquisition levels
- [x] All 17 classes have a protected core-mechanic contract; 14 Weave casters retain distinct Resonance cadence
- [x] Lich and Necromancer locked as evil/transgressive Traumatic Casting exceptions
- [x] Oracle separated from RP through Revelation Charges
- [x] Opening/Horn locked at 2,400 / 1,200 hours
- [x] Player Appendix B reframed as mortal religion/cosmography
- [x] Silent Ones/Old Ones/Heartcell maintained as Director-only deep truth
- [x] Base → Arch → Hero progression language established
- [x] Hero Paths reframed as ethos/philosophy rather than Good/Neutral/Evil labels
- [x] Player peoples tied culturally to the Decennial Opening
- [x] Goblin public history and Director Unity/Moloch material integrated
- [x] Raw bestiary source scrubbed to current Aethel creature names; structured JSON re-ingested

## Priority 1 — Rules Completion

### Class/path authoring
- finish entries that remain explicitly `draft: true` in class, Oracle, Paladin, Druid, or prestige data;
- verify level 11–20 feature density and capstone power against the final Player Rulebook;
- ensure every class-specific resource has an at-table tracking procedure.

### Resonance implementation
- continue UI polish for Dissonance/Refrain visibility and class-specific vent/redirect actions;
- connect more class-native cadence reducers to Session where they can be resolved automatically;
- playtest Dissonance thresholds, Overcast costs, Traumatic Casting backlash, and multiclass pool math under sustained encounter pressure.

### Bestiary combat trust
- continue human review of AC, HP, attack packages, save DCs, recharge actions, conditions, resistances, and target behavior;
- preserve `Bestiary.xlsx` as the portable source of truth;
- re-run `python scripts/ingest_bestiary_from_excel.py` after workbook changes.

## Priority 2 — Dungeon Depth

- deepen Floors 51–100 with encounter specificity equal to early tiers;
- use the Matrix design language to create choices rather than merely harder stat blocks;
- preserve the Level-97 Old God question until owner canon resolves its exact relationship to other deep structures;
- ensure Gate Guardians and tier victory consequences alter surface politics, economy, scholarship, and future expeditions.

## Priority 3 — Expedition and Campaign Systems

- expand camp/upgrading procedures;
- strengthen salvage rights, expedition finance, insurance, faction sponsorship, and surface consequences;
- improve session UI for expedition teams and day-period scheduling;
- add campaign-facing records for persistent choices between Openings.

## Priority 4 — Human Playtesting

Simulation stress tests are useful but do not replace tables.

Run repeated human tests for:

- first-session comprehension;
- combat duration;
- RP/resource bookkeeping;
- class identity at levels 1, 3, 10, and high-level play;
- expedition logistics with 6–12 characters;
- Horn/time-pressure decisions;
- faction and surface-consequence recall;
- Director ability to reveal deep lore without exposition overload.

## Priority 5 — Companion Productization

- production build/deployment verification on a connected environment;
- persistence and campaign-save hardening;
- accessibility and mobile layout pass;
- structured content versioning/migrations;
- optional account/campaign collaboration layer;
- future AI-assisted Director/player tooling only after canonical data boundaries are stable.

## Release Discipline

Before a release candidate:

1. run `npm ci`;
2. run `npm run lint`;
3. run `npm run build`;
4. run current ingestion/validation scripts;
5. search for retired terminology and clock contradictions;
6. render and visually inspect edited Word books;
7. package without dependencies, third-party references, backups, or generated build output.

See `docs/CURRENT_SYSTEM_STATUS.md` for the current snapshot and `docs/mechanics/MAGIC_SYSTEM_VALIDATION_2026-07-31.md` for the current magic-system gate.
