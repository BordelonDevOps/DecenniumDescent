# Shared character-state derivation

**Status:** implemented and tested as a TEST_ONLY refactor on the schema60 persisted baseline. No snapshot fields, codec branches, or historical save formats changed. This does not complete character creation, advancement, class systems, or production character content.

## Responsibilities and records

`CharacterRuleFacts` is an ephemeral, read-only view that points to the existing `ActorCharacterRecord`. `CharacterAbility` names the record’s stable six-score order: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma. The view derives ability modifiers, total level, proficiency bonus, and rank contribution from the record’s scores and ordered level facts. It does not own or persist a copy.

Authority stays separated by subject:

- `ActorCharacterRecord`: actor/profile identity, six ability scores, and ordered `CharacterLevelFact` values (`ClassName`, `BaseHp`).
- `SkillTrainingRecord`: skill identity and explicit proficiency rank.
- `RangedCombatantRecord`: explicit crossbow training identity/proficiency. Its Dexterity and proficiency integers remain serialized in schema22+ as compatibility projections; attack and damage calculations use `ActorCharacterRecord`.
- `ActorLifeRecord`: maximum/current/temporary HP, injuries, death/stability, posture, and held items. Conditions, equipment, inventory, progression grants, clock, work, RNG, receipts, and save codec retain their existing authorities.

## Consumers covered

Named character facts now feed the existing ability-check routes for mining, mining assays, prospecting, harvest, fishing traps, observation/search, supply-cache locks, periodic-rider medicine, route mapping, and route reconnaissance. The same view supplies melee/ranged attack and target-defense values, represented Constitution saves, Overwatch attack/damage/Push math, the current save-proficiency and armor checks, base maximum HP inputs, and STR/DEX/CON checks in hunting-trap and work/life consequences.

The bounded TEST_ONLY club damage path uses the same STR modifier as its attack, per the existing ordinary-attack source guidance. Unarmed damage continues through the owner-adopted STR formula. These changes do not grant proficiency, alter class rules, create abilities/training, or change the supported actor fixtures’ STR 10 outcomes.

## Connected acceptance

`connected_exploration_combat_and_assigned_mining_share_one_saved_timeline` runs one shared timeline. The assigned companion has WIS 14 in its authoritative character record; the mining attempt records that modifier and derives the proficiency contribution from its explicit mining-tools training record. The hero explores into a tactical encounter and its attack audit is checked against the hero’s stored Strength fact. Tactical time advances the companion’s assigned mining work. The snapshot is saved/restored, mining resolves, duplicate assignment replay is idempotent, and exploration continues.

`repeating_crossbow_attack_uses_character_facts_after_stale_cache_save_restore_and_replay` initializes a deliberately stale serialized proficiency projection using a TEST_ONLY fixture. The snapshot round-trips unchanged; two restored simulations execute the same attack command and produce byte-identical results using the character record’s proficiency. Replaying the command after restore returns `Duplicate` without changing state.

`character_rule_facts_are_ephemeral_queries_over_the_authoritative_record` checks the named ability mapping, scores/modifiers, total level, proficiency, rank contribution, record identity, and rejection of missing or duplicate actor identities.

## Validation

- Full C# 9 warnings-as-errors suite: **PASS, 1,230/1,230**.
- Focused character-facts, connected-loop, and stale-ranged-cache cases: **PASS, 1/1 each**.
- Static package checks: **PASS, 18/18; 270 assets and 270 unique GUIDs**.
- `git diff --check`: **PASS**.

Exact runner outputs are retained in [full results](FULL_RESULTS.json), [package results](PACKAGE_RESULTS.json), the three [focused results](FOCUSED_CHARACTER_FACTS.json), [connected loop](FOCUSED_CONNECTED_LOOP.json), [stale cache replay](FOCUSED_STALE_RANGED_CACHE.json), and [source bindings and hashes](SOURCE_BINDINGS.json). The independent code review is recorded in [review evidence](INDEPENDENT_REVIEW.md). These are headless source/package checks, not a player-build qualification.

## Validation correction

The first stale-cache test edited a post-command snapshot before restoring it. The simulation correctly rejected that fabricated history as `InvalidSharedWorldReplay`, because the snapshot did not match its policy’s initialized state and receipts. I moved the stale compatibility value into the TEST_ONLY fixture’s initial state, then reran normal command execution, save/restore, deterministic replay, the complete suite, and package checks. The final reports above are all passing.

## Remaining limits

Current character values remain bounded authored/test profiles. The tactical fixture uses STR 10, so the nonzero STR weapon-damage branch is source-aligned but its nonzero result is not directly covered by this fixture. Full character creation, generalized skill and weapon training grants, class-derived abilities, all progression branches, production data, and uncovered source rules remain out of scope for this increment.
