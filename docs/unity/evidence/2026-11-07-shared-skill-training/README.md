# Shared skill-training read path

**Status:** implemented as a TEST_ONLY read-path consolidation on schema60. It adds no persisted character data, save fields, rule outcomes, or training grants.

## Responsibilities and records

`CharacterSkillTrainingFacts` reads the existing `SkillTrainingRecord` by actor and skill. `AbilityCheckRules.Derive(snapshot, actorId, skillId, ability)` resolves the matching skill record and the same actor's `ActorCharacterRecord`. The saved records remain authoritative; the query returns the original immutable record rather than a copied rank. Missing rows resolve to rank 0, and duplicate actor/skill rows fail closed.

Migrated consumers: Hide and Search, route Mapping and reconnaissance, mining extraction, prospecting, both mineral-assay paths, harvesting, unattended fishing traps, Medicine, and route-mapping assistant discovery. Fixture seeding and structural snapshot validation continue to access the array directly because they create or validate those authoritative rows.

Caller-owned ability/skill selection and each procedure's DC, timing, dice, costs, and outcomes are unchanged. The query is not a character-creation or training-grant system. Schema60 and all earlier codec branches are unchanged.

## Validation

- Focused query case `character_skill_training_queries_share_the_persisted_rank_records`: **1/1 PASS**.
- Full C# 9 warnings-as-errors suite: **1,231/1,231 PASS**.
- Static package validation: **18/18 PASS; 271 package assets and 271 unique GUIDs**.
- `git diff --check`: **PASS**.

The full suite includes connected exploration/combat/mining save/restore/replay and the existing observation, route, harvesting, fishing, mining, assay, prospecting, and Medicine cases using the new read path. Machine-readable outputs are in [focused](FOCUSED_SKILL_TRAINING.json), [full](FULL_RESULTS.json), and [package](PACKAGE_RESULTS.json) results. Source revisions, record ownership, and changed-file SHA-256 values are in [source bindings](SOURCE_BINDINGS.json). Independent review is in [review notes](INDEPENDENT_REVIEW.md).

## Review note and limits

Independent review found no blocker. The focused case proves lookup identity, rank handling, query purity, and duplicate rejection; it does not itself serialize or replay a snapshot. Save/restore and replay are exercised by the full connected and procedure-specific regressions. `Find` ignores null array entries, while snapshot validation rejects null training records before runtime consumers execute.

This remains a shared read path over finite explicit training records. It does not add generalized character creation, proficiency grants, skill-to-ability mappings, class-derived training, production content, or release approval.
