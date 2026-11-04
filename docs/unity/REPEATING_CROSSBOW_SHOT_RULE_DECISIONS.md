# Repeating crossbow attack attempt

**Status: TEST_ONLY source-bound pure attack result.** Code commit: `448764e65bff6edbb0ad58a6ec25aa915278f76c`, branch `Engine`. This composes the source-profile Repeating heavy crossbow, the deterministic ranged attack-roll query and the finite magazine model. It does not spend a tactical Action/Reaction or apply the rolled damage to a target.

**Superseded integration status (2026-11-04):** the pure helper is now used by the schema22 TEST_ONLY shared-world combat path, which spends an Action and actual bolt lot, applies the bounded damage/life-state procedure, and persists attack outcomes. This record remains the contract for the reusable shot calculation; see the [integrated combat record](REPEATING_CROSSBOW_COMBAT_RULE_DECISIONS.md) for the additional transaction and its limits.

## Source rules

The source revision is pinned to `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; exact Git blobs, SHA-256 values and locators are in [SOURCE_BINDINGS.json](evidence/2026-11-04-repeating-crossbow-shot/SOURCE_BINDINGS.json).

- The authored Repeating heavy crossbow profile is `1d10 piercing`, range `80/320`, and Repeating 5. The magazine begins empty in the Soldier kit, which provides 20 carried bolts.
- Each legal attack attempt spends one loaded bolt; a miss still spends it. An empty magazine cannot fire.
- The ranged attack uses Dexterity, plus proficiency when the caller establishes proficiency. Normal/long range, unseen status, close-hostile disadvantage, cover and condition modifiers use the existing attack-roll query.
- On a hit, roll the weapon die. A critical doubles weapon dice, then adds the ability modifier once. The attack ability modifier for this source profile is Dexterity. Damage type is piercing.
- Attack d20 randomness is resolved first; damage dice follow only on a hit. An illegal target/profile or empty magazine returns without spending ammunition or RNG.

## Implemented boundary

`RepeatingCrossbowShotRules.Resolve` accepts an explicit 80/320 ranged profile, target/geometry facts, the immutable loaded magazine, carried bolt count, and the deterministic seed. It returns whether an attack was legal/attempted, the ranged roll, updated magazine, damage dice and raw `dice + Dexterity` total before defenses, damage type, and the next random state.

This is not a command or a complete damage event. It does not establish weapon possession/proficiency/hands, perceive targets, derive line of fire or cover, spend turn resources, consume a carried-inventory lot, apply resistance/mitigation, clamp or apply final HP damage, resolve Wounds/death choices, persist a continuation, or support suspected-space attacks. Those facts/outcomes remain in their owning systems. Soldier Overwatch's feature-specific `1d8 + DEX` text versus the crossbow weapon die also remains unresolved; this method is the ordinary weapon attack profile only.

Seven new named cases bring the shared C# suite to **1012/1012**; the 14 static package checks pass. The results are in [evidence/2026-11-04-repeating-crossbow-shot](evidence/2026-11-04-repeating-crossbow-shot). The full engine and Overwatch remain incomplete; Unity stays deferred.
