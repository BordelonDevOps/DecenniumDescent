# Soldier Overwatch implementation gates

**Status: source pinned; runtime not implemented.** This is the next C# tactical dependency for the TEST_ONLY Soldier progression slice. Unity stays deferred. The source files below are pinned to repository revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; their exact SHA-256 values are recorded here so later source refreshes cannot silently change this contract.

## Source facts

| Authority | Locator | SHA-256 | Relevant content |
| --- | --- | --- | --- |
| Soldier class playtest profile | `DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json` `/engine/1`, `/schedule/0`, `/cards/0` | `ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0` | Automatic Base Overwatch at Soldier 1; separate level-1 card acquisition; selected Overwatch card upgrades the automatic engine. |
| Equipment acquisition candidate | `DescentReviewChanges/ReviewBible/data/playtest/equipment_acquisition_candidate.json` `/items/195`, `/classKits/12` | `4037e188edb890c971acb39e8679cfd5a142b0042508af30c95d4703d2a2745b` | Authored repeating heavy crossbow and Soldier starting kit. Kit grants 20 bolts, but the repeating magazine starts empty. |
| Equipment acquisition procedure | `DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md` `#new-class-equipment-profiles` | `406c68622102b444c6afb005e2d50cfd75171fe8d90db36a06d02df2d67bf27d` | Repeating 5 holds five bolts, replaces Loading, consumes one bolt per attack, and takes an Action with an appropriate free loading hand to load up to five carried bolts. |
| Class playtest rules | `DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md` `#reading-a-class-card`, `#targets-concentration-and-control`, `#action-and-timing-limits` | `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81` | Feature grants, action timing and target/control boundaries. |
| Player Rulebook v6 source text | `docs/reference/Player_Rulebook_v6_source_text.txt` lines 6738, 6748, 6750, 6816, 6867 | `a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b` | Core ammunition, Loading, range, ordinary heavy-crossbow, and bolt references. The Core profile is `1d10`, range `100/400`, Loading and two-handed. |

The automatic engine is `soldier.json` `/engine/1`. The optional `soldier.base.overwatch` card is a separate selectable card that upgrades the engine; it is not the level-1 grant itself. The level-1 schedule separately chooses four Base cards, at least two active. CHR-03's current Soldier 1-to-2 fixture does not claim to construct a complete level-1 Soldier or satisfy those choices.

## Required implementation boundary

The class profile states that the Soldier spends a Bonus Action to designate a visible 15-foot square within weapon range until the start of the next regular turn. Once during that interval, the Soldier may spend its Reaction when a perceived enemy enters or moves inside the zone, attacks an ally from inside it, or reveals itself inside it. The response is one legal ranged attack with ammunition and line of fire. The profile specifies concealment still applies, then permits a hit rider: Snare (Speed −10 feet through the end of the target's next turn), Bleed (1d4 at the start of its next turn), or Push (5 feet, STR save negates the push). The profile limits the Soldier to one zone and grants no extra Reaction. At level 17 it adds a separate once-per-round 5-foot post-shot movement benefit.

This feature cannot be wired safely by adding a trigger flag to the existing Club attacker. The C# branch now has a source-bound attack-roll query ([decision record](RANGED_ATTACK_RULE_DECISIONS.md)) and an immutable five-bolt magazine model ([decision record](REPEATING_CROSSBOW_RULE_DECISIONS.md)). They still do not form an authoritative ranged attack transaction: tactical turn/action/reaction authority, weapon custody/hands, bolt inventory, range profile selection, spatial visibility, line of fire, damage and persistence are not connected. Current tactical combat has a bounded Club/unarmed attack path and OA/Press continuations; `PlanarCombatGeometry` provides range and cover only, while `ConditionCombatPolicy.CanSee` accounts for condition awareness/invisibility but not spatial visibility or line of fire.

## Open gates before a complete vertical slice

| Gate | Why it blocks faithful execution | Required resolution |
| --- | --- | --- |
| Cross-reaction ordering | A step can offer an opportunity attack and Overwatch from the same movement. Existing source and accepted OA policy do not order different reaction types. | Owner has been asked once to choose among reactor initiative order, OAs first, or Overwatch first after the GPT browser chat timed out. Keep dependent resolution unimplemented until that answer arrives. |
| Weapon damage profile | `soldier.json` `/engine/1` says Overwatch is normally `1d8 + DEX` piercing. The authored repeating heavy crossbow candidate and Core heavy crossbow both list a `1d10` weapon die. The text may define a feature-specific attack, but the interaction is not explicit. | Obtain Codex/GPT consensus on whether Overwatch's specified damage supersedes its weapon die, and record the interpretation before coding. Preserve the source records unchanged. |
| Weapon and magazine transaction | A TEST_ONLY ordinary shot helper now composes the ranged roll, source-profile d10 damage, five-bolt magazine and one-bolt-per-legal-attempt behavior. It does not join actual inventory lots, weapon custody/hands, tactical Action/Reaction spending, defenses or a persistent attack. | Connect magazine transfers/firing to actual carried ammunition, a legal weapon, free-hand/equipment rules, Action/Reaction budgets, damage application and atomic save/replay. An empty magazine cannot fire Overwatch; loading costs the sourced Action. |
| Spatial visibility and line of fire | The current marker/grid model cannot establish visibility to the designated square, visibility/perception of a trigger, or whether terrain blocks a shot. Cover and range helpers alone do not prove line of fire. | Add a source-bound spatial query over explicit tactical obstacles/visibility facts, with unknown geometry failing closed. Do not infer visibility from distance or awareness alone. |
| Zone and event boundaries | The profile uses a visible 15-foot square and an interval ending at the start of the next regular turn. It lists entry/movement, an ally attack, and reveal as triggers; event coalescing, designated-cell ownership and exact trigger transition markers need one deterministic model. | Store a fixed zone and interval identity; identify each trigger event once, and allow at most one accepted shot during the interval. Resolve overlapping triggers without duplicate offers. |
| Attack and rider consequences | A ranged attack must connect ranged modifiers, target AC/cover, condition effects, weapon legality and ammunition with the current deterministic random stream. Bleed needs scheduled damage dispatch; Push needs a legal destination/save DC; Snare changes the target's next-turn movement. | Reuse source-bound attack/damage/condition primitives only after verifying their inputs cover this profile. Keep unresolved save DC and push-interruption cases explicit; do not guess defaults. |
| Persistent continuation | Designation, eligible trigger event, pending reaction, weapon/ammo state, once-per-interval use, rider timer, and deterministic replay must survive save/restore atomically. | Add a new versioned snapshot schema and exact command-history reconstruction; preserve all earlier golden encodings and pending-choice behavior. |

## Existing implementation limits

- `PlanarCombatGeometry` handles planar distance, ranged normal/maximum range, best listed cover and one corner-step rule. It does not perform visibility, line-of-effect, occupied-volume or weapon-legality checks.
- `TacticalMovementPolicy` implements bounded voluntary movement, opportunity-attack offers and Press. It does not implement cross-type reaction priority.
- `TestOnlyClubAttackPolicy` resolves Club and ordinary unarmed melee attacks. `RangedAttackRules` calculates a ranged roll from explicit facts; `RepeatingFiveMagazine` tracks the finite magazine; and `RepeatingCrossbowShotRules` composes an ordinary crossbow attack and its damage dice. They do not validate/charge tactical Actions, prove equipment custody/hands or spatial facts, apply damage to life state, or persist with combat.
- `ConditionCombatPolicy` uses condition-based awareness and invisibility for its current melee fixture. It does not model terrain sight, concealment geometry, scheduled Bleed damage or an Overwatch Push save.

## Intended implementation sequence

1. Record the pending cross-reaction ordering answer and Codex/GPT interpretation of the source damage profile.
2. Implement the smallest reusable ranged-attack transaction with explicit weapon, hand, ammunition, magazine, range, visibility, cover and deterministic-roll facts.
3. Persist designation and trigger identity, then connect Overwatch to ordinary movement and the shared tactical event queue.
4. Implement and persist the three hit outcomes, including turn-bound expiry and save resolution; add competing-trigger, interruption and disk-restore cases.
5. Integrate the level-1 grant into a complete source-valid Soldier 1 build only after its four Base choices and minimum two active cards are represented.

Each stage remains TEST_ONLY until its scope is source-bound, replayable, and independently reviewed. It does not complete all classes, all ranged weapons, the tactical system, or the full three-layer engine.
