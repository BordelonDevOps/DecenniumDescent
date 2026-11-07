# Actor-scoped character, training, and injury facts

**Status:** implemented as a TEST_ONLY read-model increment on persisted schema60. No rule text, character state, snapshot fields, codec branches, command receipts, or content fingerprints changed.

## Responsibilities and authoritative records

`CharacterStateFacts` joins existing immutable records for one actor. It stores references only and must be resolved again after a command replaces snapshot records.

- `ActorCharacterRecord`: `ActorId`, `ProfileId`, six ordered `Abilities`, and ordered `Levels` (`ClassName`, `BaseHp`). `CharacterRuleFacts` continues to derive modifiers, total level, proficiency bonus, and rank contributions from this record.
- Optional `SkillTrainingRecord`: matching `ActorId`, `SkillId`, and explicit `ProficiencyRank`. Missing training remains rank 0; duplicate actor/skill matches fail closed.
- `ActorLifeRecord`: matching `ActorId` and current `LinkedInjuries`. The existing `PlaytestLife.AbilityCheckInjuryPenalty` policy applies the strongest relevant penalty once.

The query rejects missing or duplicate character/life identity, mismatched actor facts, and a check modifier paired with a different actor. HP, death/recovery, conditions, posture, equipment, inventory, progression, clock, RNG, work, and persistence remain under their existing authorities.

## Consumers covered

The snapshot ability-check path now derives the actor's character and optional skill facts through the joined query for Hide/Search, route Mapping/reconnaissance, mining/prospecting/assay, harvest/fishing traps, and Medicine. Injury-aware check resolution uses the same actor-bound facts for Hide/Search, route Mapping/reconnaissance, mining, prospecting, both assay paths, harvest, formula research, manufacturing, tool repair, supply-cache locks, and ordinary-receptacle locks.

Callers retain their ability, training source, DC, timing, dice, disadvantage, costs, and outcomes. Existing persisted attempt records still own their audit facts. The bounded content stays TEST_ONLY.

## Connected acceptance

`connected_exploration_combat_and_assigned_mining_share_one_saved_timeline` checks the hero and companion against their shared character/life records; the companion's mining check derives its ability and training from the same actor's records. The party explores into combat while assigned mining continues, saves/restores active work, then advances two restored simulations identically and compares their full snapshot bytes. It also verifies duplicate assignment replay is idempotent and resumes exploration.

`character_state_facts_join_existing_actor_records_without_copying` checks record identity, explicit training rank, injury application, actor mismatch, and duplicate life rejection. The existing supply-cache injury regression now constructs its injury in the snapshot and exercises the actor-bound lock-check path. The full suite also covers supported historical save fixtures.

## Validation

- Full C# 9 warnings-as-errors suite: **PASS, 1,232/1,232**. See [full results](FULL_RESULTS.json).
- Focused actor-state, connected replay, supply-cache and receptacle cases: **PASS, 4/4**. See [focused results](FOCUSED_RESULTS.json).
- Static package validation: **PASS, 18/18 checks, 271 package assets, 271 unique GUIDs**. See [package results](PACKAGE_RESULTS.json).
- `git diff --check`: **PASS**.
- Read-only independent review: no remaining code blocker after the supply-cache/receptacle join was updated. The reviewer had also flagged stale evidence from the prior increment; this packet contains results and hashes for the current diff.

The headless and static checks do not establish Unity Editor import, Play Mode, player-build, production-content, or release qualification. The independent review is captured in [review notes](INDEPENDENT_REVIEW.md).

## Source and implementation bindings

Pinned rule sources, pre-increment code blob IDs, current changed-source SHA-256 values, compatibility status, and validation-run identities are recorded in [source bindings](SOURCE_BINDINGS.json). Existing character creation, skill, injury, and task rules are reused; this increment adopts no new gameplay policy.

## Remaining limits

Character profiles and training remain bounded authored/test facts. General character creation, training grants, advancement, class rules, generalized condition/equipment aggregation, and production character content remain incomplete. The shared query does not consolidate those separate authorities.
