# Repeating crossbow combat integration

**Status: PARTIAL / TEST_ONLY / SOURCE-BOUND / PROVISIONAL.** Schema22 connects one authored Repeating heavy crossbow fixture to the shared tactical command, action, damage, life-state, command-history, save and restore paths. It is not a general ranged combat implementation, a complete Soldier build, or release-approved gameplay.

## Source and adopted rules

The source set is pinned to revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Exact locators, Git blobs, source hashes, implementation hashes and test names are recorded in [SOURCE_BINDINGS.json](evidence/2026-11-04-repeating-crossbow-combat/SOURCE_BINDINGS.json).

- The authored Repeating heavy crossbow is 20 lb, two-handed, range 80/320, and deals 1d10 piercing. Repeating 5 holds up to five bolts and replaces Loading. The kit supplies 20 bolts, with an empty starting magazine.
- Loading uses an Action and an appropriate free hand; each legal attack spends a loaded bolt on hit or miss. Existing handoff, critical-damage, ammunition, condition, life-state and ordinary AC decisions continue to govern their previously bounded scopes.
- Reload and attack each use the acting creature's regular tactical Action. Reload transfers only the requested quantity from its actually carried, accessible ammunition lot. Releasing one grip to load is free in this fixture; attacking re-establishes the two-handed grip as part of use.
- A legal attack consumes the shared deterministic random stream, spends one provenance-linked bolt, applies the source-profile attack and damage procedure through existing bounded combat rules, spends the Action, and records a replayable result. A rejected command does not spend time, Action, ammunition or randomness.

This increment introduces no general target-visibility or line-of-fire formula. The TEST_ONLY fixture supplies a single authored planar lane, target visibility, location knowledge, cover and clear-line facts. Unknown location, blocked line and total cover fail closed before the roll. The authored shooter and target values are test data, not a production character or encounter.

## Implemented boundary

Schema22 persists weapon identity, owner/custodian/holder, grip state, magazine lot lineage, remaining bolt quantities, explicit training facts, attack rolls, damage and effect-roll results. Validation conserves each finite lot as available bolts plus loaded bolts plus expended bolts. The attack and reload commands use the shared Action interval and command-replay ledger. Unconsciousness drops the held weapon while preserving its ownership, custodian and loaded bolts.

The fixture uses the explicitly recorded `TEST_ONLY.soldier-martial-ranged-training` fact when proficiency is enabled. It does not infer proficiency from a class name, weapon possession or the actor's existing numerical profile. The fixture does not construct the source-valid Soldier 1 schedule or its card choices.

The [seven added regressions](evidence/2026-11-04-repeating-crossbow-combat/SOURCE_BINDINGS.json) cover the complete bounded loop: initial save/restore and carried mass, Action-costed reload and replay, a critical attack and applied damage, failure-before-roll rollback, explicit proficiency, unconscious drop, and the negative damage floor used by the composed shot rule. Current C# results are **1019/1019**; static package checks are **14/14**.

## Limits

- Only one authored weapon, one bolt-lot profile, two fixed tactical actors, one lane and one bounded damage context are executable here. Arbitrary weapons, lots, equipment operations, ranges, terrain, cover derivation, target perception and general encounter rosters remain incomplete.
- The current TEST_ONLY actor profile is not a complete Soldier. The automatic level-1 Overwatch feature, its designation/trigger lifecycle, cross-type reaction ordering, riders and feature-specific damage interaction remain open in [OVERWATCH_IMPLEMENTATION_GATES.md](OVERWATCH_IMPLEMENTATION_GATES.md).
- This path does not create Press on a ranged hit or offer opportunity attacks/other reactions. It does not implement the broad tactical ruleset, full character acquisition, general damage/condition scheduling, companion AI, co-op, or the complete three-layer engine.
- Headless Roslyn and static package validation are not Unity import/compilation, Edit Mode, Play Mode, player-build or observed gameplay evidence. Unity remains deferred until the C# engine is complete.
