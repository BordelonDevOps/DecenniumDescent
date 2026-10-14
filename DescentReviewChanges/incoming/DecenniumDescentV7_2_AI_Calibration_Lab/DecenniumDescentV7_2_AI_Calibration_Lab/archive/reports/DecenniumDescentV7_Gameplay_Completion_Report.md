# Decennium Descent V7 Gameplay Completion Report

**Completed:** August 5, 2026  
**Source:** V6 Consolidated  
**Release line:** V7 Gameplay Complete

## Governing design rule

> Decennium Descent should have 5e's readability and speed, Pathfinder 2e's tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems.

## Gameplay completed

V7 now defines and implements the complete table loop:

1. Objective selection.
2. Financing, sponsorship, and abort conditions.
3. Twelve-member Expedition organization.
4. Supply, transport, Load, and cargo reserve.
5. Dungeon entry and Opening clock.
6. Three eight-hour Watches per day.
7. Team activities for Combat, Reconnaissance, Research, Resource, Support, and Rest.
8. Route Progress, Mapping, Capacity, and Pressure.
9. Encounter Mode, action limits, retreat, Downed, Wounds, and death.
10. Camps, Strain, equipment Integrity, harvesting, and preservation.
11. Cargo priority and Extraction Class.
12. Extraction Tests and visible cargo/casualty risk.
13. Haven quarantine, provenance, appraisal, claims, disposition, settlement, recovery, standing, advancement, and next descent.
14. XP awards based on contribution and objectives rather than body count.
15. End-of-Opening Cycle Records and ten-year persistence/replenishment.

## New canonical artifacts

- `docs/mechanics/DESIGN_DOCTRINE.md`
- `docs/mechanics/GAMEPLAY_LOOP_CANON.md`
- `docs/mechanics/GAMEPLAY_LOOP_EXAMPLES.md`
- `data/public/Decennium_Descent_Gameplay_Loop_v1.json`
- `src/data/gameplay-loop.json`
- `src/lib/gameplay-loop.ts`
- `src/components/ExpeditionTracker.tsx`
- `books/player/Decennium_Descent_Gameplay_Loop_Bible_v1.docx`
- `tools/validate_gameplay_loop.py`

## Companion implementation

The public companion now has a dedicated **EXPEDITION** surface separate from the round-by-round **SESSION** surface. It persists:

- Phase and objective.
- Opening hour, day, Watch, Horn, and seal clocks.
- Roster up to twelve members.
- Team and activity assignments.
- Personal Load, capacity, Strain, and Wounds.
- Route name, Progress, Length, Mapping, and Capacity.
- Pressure, Supply, treasury, and camp.
- Cargo Load, Extraction Class, priority, value, and tags.
- Extraction declaration, Haven arrival, and an expedition log.

## Empirical functions not falsely claimed as complete

Writing can finish procedures, but it cannot prove numerical balance or real player comprehension. Five Cursor multi-agent packs were created:

1. Combat and Class Balance.
2. Expedition and Extraction.
3. Haven Economy and Social Systems.
4. Seasonal and Decennial Persistence.
5. Readability, Speed, and Onboarding.

Each pack has exact orchestrator instructions, fixed scenarios, source manifests, dedicated agents, JSON result schemas, report templates, and a compiler that produces `COMPILED_REPORT.md`.

The combat pack includes seventeen dedicated player files, one for every class, each with an in-world background and explicit instructions for interpreting fights. The expedition pack includes twelve dedicated roster players.

## Validation

```text
TypeScript: PASS
Magic: PASS — 848 spells, 936 placements, 17 classes
Abilities: PASS — 17 classes, 335 feats, 10 oaths, 10 mysteries, 10 curses
Public canon: PASS — 65 known dossiers, documented depth only, public crafting only
Gameplay loop: PASS — preparation through seasonal persistence
DOCX render review: PASS — 24 pages, no clipped text or broken tables
Cursor pack ZIP integrity: PASS — five packs
```

A production Next.js build remains dependent on installing platform-correct packages in a normal local or CI environment. `npm ci` could not complete in this container because its internal registry lacked `yocto-queue@0.1.0`; TypeScript and all repository validators passed using the dependency snapshot supplied in V5.
