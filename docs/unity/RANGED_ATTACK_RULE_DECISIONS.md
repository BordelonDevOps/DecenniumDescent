# Ranged attack resolution rules

**Status: TEST_ONLY source-bound attack-roll query.** Code commit: `97c528dea83d123a726af9d0f20551e7d7a259b3`, on branch `Engine`. This query does not create an authoritative attack command, consume ammunition, validate equipment or apply damage. It does not close Soldier Overwatch's unresolved reaction order or feature-specific damage profile.

## Source rules

The source set is pinned to base revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Exact source blobs and hashes are in [SOURCE_BINDINGS.json](evidence/2026-11-04-ranged-attack/SOURCE_BINDINGS.json).

- Attack rolls add the relevant ability modifier and proficiency bonus when proficient. Ranged weapon attacks use Dexterity. A natural 1 misses and a natural 20 hits and critically hits. See Player Rulebook v6, `Making an Attack` and `Attack Rolls`.
- An unseen target imposes disadvantage; attacking while unseen grants advantage. Normal range is inclusive; beyond normal through maximum range imposes disadvantage; beyond maximum range is illegal. A visible, non-incapacitated hostile within 5 feet imposes disadvantage on a ranged attack. See `Unseen Attackers and Targets` and `Ranged Attacks`.
- Half cover adds +2 AC; three-quarters cover adds +5 AC; total cover prevents direct targeting. See `Cover`.
- Soldier's source profile identifies Dexterity for ranged attacks. The query still accepts explicit target AC and the ranged weapon's normal/maximum range; a caller supplies a valid source-specific profile.

## Implemented query contract

`RangedAttackRules.Resolve` combines the existing range, cover, condition and deterministic d20 calculations for one attack roll:

- Adds Dexterity, proficiency only when the caller says the attacker is proficient, and an explicit flat modifier.
- Adds only the strongest listed cover bonus; total cover fails before a die is drawn.
- Uses disadvantage for long range, an unseen target, an eligible nearby hostile and the supplied active attack-condition modifiers; uses advantage for an unseen attacker and supplied advantage sources. Any advantage and disadvantage cancel to a normal roll.
- Uses explicit target-location and line-of-fire facts. Unknown location, blocked line of fire, total cover and out-of-range return a failure without advancing the random stream. The unknown-location case means the caller has not supplied a resolvable target position; this query does not establish a universal game rule against attacks at unobserved spaces.
- Uses existing condition-derived advantage, disadvantage and critical-on-hit facts. A critical condition does not turn a miss into a hit or critical.
- Draws from the caller's deterministic random state only after its explicit target/geometry/range gate succeeds.

The query returns its effective attack modifier, covered AC, d20 selection/result, hit/critical outcome, failure reason and next random state. It does not add a damage die, apply an outcome or mutate shared state.

## Limits and next integration

- The caller remains responsible for action/reaction availability, valid target state, weapon proficiencies, hands, weapon profile, ammunition, magazine/loading state, target location, visibility, line of fire and cover facts.
- The separate source-defined Repeating 5 ammunition state is in [REPEATING_CROSSBOW_RULE_DECISIONS.md](REPEATING_CROSSBOW_RULE_DECISIONS.md); it still is not connected to this query or a tactical command.
- Cover is provided as an explicit classification; this query does not derive it from terrain. `LineOfFireClear` and `TargetVisible` are independent caller-supplied facts.
- No ammunition is consumed, no hidden actor is revealed, no injury or condition is applied, and no damage is rolled.
- Overwatch remains blocked on cross-reaction priority and whether its `1d8 + DEX` feature text replaces the selected weapon die. Its repeating-crossbow source and empty-magazine starting state are pinned in [OVERWATCH_IMPLEMENTATION_GATES.md](OVERWATCH_IMPLEMENTATION_GATES.md).
- Unity compilation, Edit Mode, Play Mode, scene integration, and player builds remain unrun and deferred.

The shared Roslyn suite passes **998/998**, including ten named ranged-attack cases. Static package validation passes **14/14** structural checks. Results and source hashes are retained in [evidence/2026-11-04-ranged-attack](evidence/2026-11-04-ranged-attack). This bounded query is not a complete ranged-combat system.
