# DECENNIUM DESCENT — VIDEO GAME ONLY DEVELOPMENT DIRECTIVE

Effective immediately, **drop tabletop/TTRPG development as a project goal.**

Decennium Descent is now being developed as a **video game rules system only**.

Do not spend further development or review effort making mechanics practical for manual tabletop execution.

## Primary Design Standard

Every system must be:

- deterministic enough for software implementation;
- internally consistent;
- source-faithful;
- state-machine compatible;
- machine-testable;
- explicit about timing and ordering;
- explicit about costs and transactions;
- explicit about targets and eligibility;
- explicit about geometry;
- explicit about lifecycle and cleanup;
- explicit about stacking/replacement;
- explicit about ownership and provenance;
- explicit about edge cases;
- compatible with existing accepted game interfaces.

Human tabletop convenience is no longer a requirement.

## Remove Tabletop Constraints

Do **not** simplify or change a mechanic merely because it would be difficult for a human Game Master to track manually.

The engine may freely track:

- exact coordinates;
- body volumes;
- sub-second or event-order timing where needed;
- hidden state;
- multiple concurrent clocks;
- operation snapshots;
- exact source provenance;
- individual damage roots;
- nested effects;
- per-body suppression;
- precise collision geometry;
- exact resource transactions;
- individual summoned-body state;
- persistent world-state records;
- deterministic random-selection pools;
- state histories;
- complicated eligibility predicates.

These are acceptable if they improve the video game.

## Dice and Randomness

Traditional tabletop dice notation may remain where it is part of the game's authored mechanics, such as:

- 1d6;
- 2d8;
- d20 attack rolls;
- saves;
- random tables.

However, implementation should treat them as engine RNG operations.

Do not retain cumbersome physical-die procedures merely for tabletop compatibility.

Rules concerning public versus hidden physical dice should only survive where they represent an actual gameplay-information distinction that matters to the digital game.

## Geometry

Prefer mathematically precise digital geometry.

It is acceptable to use:

- actual body volumes;
- collision bounds;
- nearest-point calculations;
- line-of-effect traces;
- spatial queries;
- exact sphere/cube/cone intersection;
- portal apertures;
- occupied volumes;
- continuous movement intersection;
- trajectory checks.

Do not replace precise geometry with approximate tabletop abstractions unless the abstraction is itself an intentional gameplay rule.

## Timing

Prefer explicit engine timing.

Use:

- event ordering;
- triggers;
- interrupts;
- queued operations;
- state transitions;
- exact deadlines;
- round/turn ownership;
- operation snapshots;
- lifecycle callbacks.

Do not distort mechanics merely so a tabletop group could remember them.

## User Interface Versus Rules Engine

Separate:

### Engine rule
The exact deterministic mechanic.

### Player presentation
The understandable information shown to the player.

Complexity may exist internally without exposing every implementation detail to the player.

For example, the engine may track numerous provenance and lifecycle fields while the UI simply tells the player:

> Cannot teleport while anchored.

Do not confuse UI simplicity with mechanical simplicity.

## Spell Review

Continue the remaining spell review, but optimize it for digital implementation.

For every spell, resolve only what the video-game engine actually needs:

- cast requirements;
- RP/resource transaction;
- rank;
- source;
- caster;
- targets;
- range;
- geometry;
- attack/save;
- damage/healing;
- conditions;
- duration;
- concentration;
- movement;
- interruption;
- suppression;
- dispelling;
- Null;
- death;
- summons;
- companions;
- ownership;
- faction/alignment predicates;
- teleportation/planar behavior;
- cleanup;
- edge cases.

Do not spend review time producing procedures whose only purpose is helping a human tabletop Director adjudicate the spell manually.

## Worked Examples

Worked examples remain useful as **test vectors**, not tabletop teaching examples.

Prefer examples that can become automated unit/integration tests.

Each important example should establish:

- initial state;
- operation;
- deterministic inputs or seeded RNG result;
- expected intermediate states;
- expected final state.

Where possible, express examples in machine-verifiable form.

## Accepted Interfaces

Continue reusing previously accepted interfaces.

Do not reopen established systems unless a genuine contradiction appears.

Examples include current accepted versions of:

- pricing;
- Null;
- damage roots;
- death/Stable/Dying;
- healing;
- concentration;
- Ready/interrupt equivalents;
- Falling;
- body geometry;
- antimagic;
- suppression;
- summons;
- companions;
- dispelling;
- Banishment;
- planar travel;
- teleportation;
- alignment;
- faction predicates;
- endpoint placement;
- lifecycle;
- cargo.

These interfaces should now be interpreted primarily as **engine contracts**, not tabletop procedures.

## Accelerated Review

The removal of tabletop requirements should be used to accelerate the remaining spell work.

Use:

1. automated source/hash validation;
2. automated structural validation;
3. accepted-interface inheritance;
4. automated arithmetic/geometry checking;
5. semantic-delta analysis;
6. risk-tiered cohorts;
7. machine-test-oriented worked cases;
8. exception-only conference.

Do not repeatedly re-explain accepted systems.

## Risk Cohorts

Continue using larger cohorts where safe:

- routine/inherited spells: approximately 25–40;
- interaction-heavy spells: approximately 15–25;
- systemic/high-risk spells: approximately 5–10.

Increase cohort size further if automated validation and accepted interfaces make that safe.

## Preserve Source Fidelity

Dropping tabletop development does **not** authorize redesigning the original game casually.

Continue preserving:

- spell identities;
- original source text;
- class access;
- ranks;
- schools;
- histories;
- prior versions;
- frozen source hashes.

If digital implementation requires a missing rule, create the narrowest necessary:

**NEW scoped authorship**

Do not invent new spells, abilities, class features, lore, or cosmology to fill gaps.

## Documentation Direction

Future documentation should prioritize:

1. canonical source;
2. operative engine specification;
3. data/schema representation;
4. state transitions;
5. validation cases;
6. player-facing description where needed.

Do not prioritize tabletop chapter formatting or Game Master adjudication prose.

Existing tabletop-oriented documents may remain as historical/source evidence, but do not spend time polishing them for tabletop publication.

## Project Goal

The goal is now:

> Build Decennium Descent into a deep, deterministic computer RPG whose complexity is handled by software rather than imposed on a tabletop group.

Complexity is acceptable when it produces meaningful gameplay and the engine can resolve it reliably.

Unnecessary complexity should still be removed.

The distinction is:

**Do not simplify because humans would have difficulty tracking it manually. Simplify only when the mechanic itself does not justify its complexity.**

## Approval Boundaries

Current review acceptance still does not automatically mean:

- numerical balance approval;
- implementation completion;
- automated test completion;
- human gameplay testing;
- cosmology canon approval;
- whole-game completion;
- publication/release approval.

It means the mechanic is sufficiently coherent to proceed as an authored video-game rules candidate.