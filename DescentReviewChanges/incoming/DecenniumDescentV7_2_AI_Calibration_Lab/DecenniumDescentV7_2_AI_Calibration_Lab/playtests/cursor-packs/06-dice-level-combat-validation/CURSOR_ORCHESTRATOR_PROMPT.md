# Cursor Orchestrator Prompt — Pack 06

You are conducting an auditable dice-level combat validation of Decennium Descent V7.2. Do not modify canon.

## Mandatory sources

Read `CANON_MANIFEST.json`, `docs/mechanics/GAMEPLAY_LOOP_CANON.md`, `docs/mechanics/DESIGN_DOCTRINE.md`, `src/data/class-details.js`, `src/data/class-paths.js`, `src/data/class-draft-levels.js`, `src/data/feats.js`, `src/data/spells.js`, `src/data/gameplay-loop.json`, and `src/bestiary_data_full.json`.

## Phase 1 — freeze legal builds

For every class/level used by the scenario matrix, the Build Auditor must create `frozen_builds/<class>-L<level>.json` containing all ability scores, HP, AC, saves, attacks, resources, spells, feats, class/path abilities, conditions, and source references. The Rules Judge validates legality. Hash each frozen file and do not change it after the first encounter seed.

## Phase 2 — freeze encounters

The Encounter Curator copies exact enemy records from `src/bestiary_data_full.json` into `fixtures/<scenario>.json`. Record HP, AC, saves, actions, traits, tactics, terrain, objective, cargo, starting positions, and encounter budget. Do not create hidden bonuses.

## Phase 3 — execute seeds

For each matrix row and seed:

1. Spawn the Director, Rules Judge, Dice Recorder, Metrics Auditor, Exploit Auditor, and listed player agents.
2. Use a deterministic PRNG seeded by the listed integer. Record the generated sequence.
3. Log initiative and every individual die.
4. Log Action, Bonus Action, Reaction, Movement, free interaction, Additional Action Slot, concentration, cooldowns, summons/actors, conditions, resources, damage, healing, prevention, objective progress, and retreat state each round.
5. No average damage. No model-estimated DPR. No unrecorded rerolls.
6. If a rule is unclear, halt, obtain one written Rules Judge ruling, and apply that ruling to every seed for the scenario.
7. Flag illegal action stacking, more than two independent actors, self-reset loops, control without a new save, and any mismatch between written rule and runtime data.
8. Finish at objective completion, retreat, defeat, or round 12.

## Evidence rule

Observed results may support numerical revision only when the exact builds, fixtures, dice, rulings, and round logs are present. A statement based on expected DPR or narrative probability is invalid.

Governing doctrine: Decennium Descent should have 5e's readability and speed, Pathfinder 2e's tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems.
