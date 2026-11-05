# Soldier Warning Shot and Covering Fire

**Status: TEST_ONLY prototype implementation.** The Soldier class card source is provisional playtest content. This record binds the implemented slice to that exact source and records the Codex/GPT consensus completions authorized by the owner. It does not promote either card to production or release.

This schema29 record supersedes the earlier schema28 status sentence in `SOLDIER_LEVEL1_LOADOUT_RULE_DECISIONS.md` that describes both cards as non-executable. That earlier file remains byte-stable because its hash is part of the schema27/28 content fingerprint.

## Pinned source contract

All source rows use revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

| Source | Git blob | SHA-256 | Used facts |
| --- | --- | --- | --- |
| `DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json`, `/cards/5` and `/cards/7` | `c414a1d9ba2ce37cde89d0ef73265821bb74ac2d` | `ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0` | Selected Base cards; level 1; Action; one ammunition; Recharge 2; Covering Fire's ranged attack, normal damage, next attack against an ally other than its Soldier, replacement; Warning Shot's visible enemy within 60 ft, weapon die only, disadvantage on its next attack, target-turn expiry. |
| `DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md`, `#action-and-timing-limits` and `#reading-a-class-card` | `5a446dd0dabae096e51f419b5e71756e0169bb3b` | `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81` | Legal misses pay; invalid activation does not; Recharge ticks at each owner's regular Start, including incapacity; outside combat, one tick per six elapsed seconds; an attack written as an Action replaces an ordinary attack. |
| `DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`, `#encounter-and-action-resources`, `#standard-actions`, `#cover-sight-and-search` | `72bcb58af57f8bfe27596ec0b1467e4c780a6ef8` | `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6` | Shared Action budget, ranged attack legality, visibility/perception and cover constraints used by the fixture. |
| `docs/unity/SOLDIER_TACTICAL_TECHNIQUE_RULE_DECISIONS.md` | Recorded in `evidence/2026-11-04-soldier-techniques-build/SOURCE_BINDINGS.json` and pinned by `SoldierTacticalTechniqueFixture` | Recorded in the same binding | Exact implementation completion and bounded scope below. |

The pinned build-example source in schema27 remains the evidence that the fixture selected both cards. The schema22 Repeating-crossbow and schema28 Soldier-build bindings supply the actual weapon, attack, ammunition, AC, damage and life-resolution facts; this increment reuses those records and handlers.

## Codex/GPT consensus completion

- Each card is independently available only when its selected Base grant exists, its own Recharge counter is zero, the actor can take an Action, the existing Repeating crossbow is held and legal, and an actual loaded bolt is available. A legal attack miss spends the Action and one bolt and starts that card's Recharge 2. Failed preflight spends neither. The counters remain separate and each elapsed owner regular Start ticks them once, even while incapacitated. If a noncombat clock advance skips multiple Starts, every elapsed owner Start is counted.
- Warning Shot targets one visible enemy within 60 ft and within the existing weapon's legal range. It makes one ordinary ranged weapon attack. A hit deals weapon damage dice only; ability and Aggressive flat damage are excluded. The hit applies disadvantage to that enemy's next attack, regardless of its target, through the end of its next future regular turn. It does not force an attack or spend the enemy's Action.
- Covering Fire targets one perceived enemy within the existing weapon's legal range. It makes one ordinary ranged weapon attack and uses normal weapon damage. On hit, that enemy takes `-2` on its next attack against an ally of the applying Soldier other than the applying Soldier. A later Covering Fire on the same target replaces the prior Covering Fire rider, including when the later source differs; riders never stack.
- Effects apply on hit even when defenses reduce damage to zero or the target reaches 0 HP/dies. Source death, target incapacity and combat exit do not independently clear an active rider.
- A rider is captured just before any admitted attack roll (melee, unarmed, ranged, opportunity attack or Soldier Overwatch) and is consumed by that attempted attack whether it hits, misses or is a natural 1/20. Rejected declarations, queries, declined reactions and unexecuted attacks do not consume it. Existing advantage/disadvantage cancellation still consumes a Warning Shot rider. One attack can receive both Warning Shot disadvantage and Covering Fire `-2`.
- Warning Shot's applied disadvantage sources on the same target all apply to and are consumed by the same next attack. Covering Fire only applies when the attack target is an ally of its recorded Soldier and is not that Soldier; unrelated attacks do not consume it.
- The fixed TEST_ONLY roster explicitly records the Soldier/companion alliance so an eligible Covering Fire target exists. It includes the companion in this fixture's three-actor regular schedule. Alliance, roster and authored encounter geometry are fixture facts, not a general faction or targeting system.
- The schema28 `SoldierCharacterBuildFixture` constructor remains the default and preserves its prior two-actor schedule and content fingerprint. Schema29 behavior is opt-in through `SoldierCharacterBuildFixture.ForTacticalTechniques(...)`; only that opt-in adds the companion schedule slot, explicit alliance, and tactical-technique source binding.
- The recorded alliance excludes the companion from hostile proximity/disadvantage and ordinary opportunity-attack checks, and prevents walking near that companion from implicitly entering combat. A one-second inventory handling operation is rejected if it would cross a saved tactical-effect deadline, matching the fixture's other timed-boundary guards.

These completion details were already agreed in **Unity Rules Engine Development**. They fill outcomes the card and common-action sources do not specify completely; they are prototype policy, not quoted source text.

## Runtime and persistence boundary

Schema 29 adds separate Warning Shot / Covering Fire Recharge state, explicit fixture alliance, finite rider records and attack-to-rider consumption audits. Effects store their target, source, originating attack and the exact next applicable virtual Start/End expiry marker. Structural validation joins each effect to its attack and exact deadline, verifies the consuming attack's revision and qualifying ally target, and requires one persisted effect for each successful technique hit. All attack handling reuses the existing crossbow, melee, damage, life, visibility, cover, custody, action and ammunition machinery. The feature remains inside the gated TEST_ONLY LabModel; command discovery is read-only and execution uses the normal transaction path.

The schema29 byte layout appends the two Recharge values to character-feature runtime and appends the tactical-feature collections. Schemas 1–28 keep their prior read/write paths. This is a versioned addition, not a save migration.

## Explicit limits

One authored Soldier, Repeating crossbow profile, loaded-bolt ledger, target lane and three-actor schedule are supported. The alliance map is explicit fixture data. Other weapons, generic factions/alliances, generalized ability execution, hidden-target perception beyond the fixture facts, class-wide Recharge scheduler, all Soldier cards, later class levels, arbitrary encounter rosters and release content selection are not claimed. Compilation is not runtime replay, regression, Unity or gameplay validation.
