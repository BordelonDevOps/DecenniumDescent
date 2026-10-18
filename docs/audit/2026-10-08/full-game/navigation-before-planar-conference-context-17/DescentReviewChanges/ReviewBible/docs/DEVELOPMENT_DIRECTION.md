# Decennium Descent — active development direction

Effective 16 October 2026, Decennium Descent is a **video game only**. Tabletop/TTRPG development is retired by the owner. The [verbatim directive](mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md) takes precedence over conflicting tabletop requirements in older plans and the [original accelerated review protocol](mechanics/SPELL_REVIEW_PROTOCOL.md). Both originals remain preserved.

Build a deep, deterministic computer RPG. The engine handles the bookkeeping; the player interface presents understandable choices and results. Retain complexity when it earns its place in gameplay.

## What work continues

Develop source-faithful engine specifications, data schemas, state transitions, deterministic test vectors and useful player descriptions. Preserve spell/class identity, access, rank, school, lore and source provenance. Each operation needs precise eligibility, geometry, timing, resource commitments, ownership, lifecycle and cleanup.

The [173-entry interface registry](../data/director/spell_review/accepted_interface_registry_06.json) is the current reuse index. Its exact source scopes and provisional/pending distinctions still govern. Existing accepted contracts remain usable; a tabletop heading or historical acceptance label does not invalidate their mechanics. Do not reopen them without a genuine contradiction or required narrow digital decision. This registry is documentation, not implemented engine code.

Dice notation denotes engine RNG. Preserve actual probabilities, eligibility and gameplay-relevant hidden information. Physical rolling and manual adjudication are no longer deliverables. Existing intentional turn/round abstractions remain rules until an explicit design decision changes them.

## What leaves the active backlog

Stop tabletop chapter polishing, physical-dice procedures, paper character-sheet production, manual GM teaching, table-contract publication and print-book layout. Preserve their current files as source/history. Reuse relevant material for digital onboarding, host permissions, encounter/content authoring, information visibility and gameplay testing.

The coverage ledger retains all 75 identities. Updated digital scope governs older issue text. Historical source work and review evidence remain valid within their original scope; no area becomes complete merely because its tabletop requirements are retired.

## Review workflow

1. Freeze source bindings and identify exact class/rank/access requirements.
2. Reuse accepted interfaces and assign risk tiers: routine 25–40, interaction-heavy 15–25, systemic 5–10 where safe.
3. Run source/hash and structure validation; identify genuine semantic differences.
4. Resolve only missing engine decisions. Label narrow additions **NEW scoped authorship** and confer before substantial new systemic rules.
5. Author complete engine behavior and test vectors with initial state, operation, deterministic inputs or seeded RNG, expected intermediate states and final state. Validate arithmetic and geometry where applicable.
6. Confer with the actual GPT notebook on exceptions and exact acceptance. Freeze accepted outputs and register their precise scopes.

Future acceptance means **authored video-game rules candidate**. It does not establish implementation, automated runtime tests, numerical balance, human gameplay testing, cosmology canon, whole-game completion or release approval.

## Current continuation

**Current position — 18 October 2026:** **525 ordinary spells reviewed / 323 pending**, with 249 complete standalone procedures across all 848 identities. The [current authored index](../data/public/spell_playtests/authored_review_index.json), [checkpoint16](../../../docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_PERSISTENT20_APPLIED_COMPANION_ACTIVE_16.json) and [review map](../../../REVIEW_MAP.html) are the entry points. Working folder: `C:\Github\DecenniumDescent`. Continue until the review is complete or any reported allowance reaches 20% remaining; the latest observation was 60% remaining.

**Damage/control25 accepted and applied:** Actual GPT accepted all eight Exact10 artifacts unchanged. The [application receipt](../../../docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json) and [1,039-check verification](../../../docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json) bind all 25 procedures, 26 placements, 70 current cases, 36 original scenarios and 77 complete sources. Read the [player chapter](spells/candidates/DAMAGE_CONTROL_25_REVIEWED_10.md), [Director chapter](director-only/spells/DAMAGE_CONTROL_25_REVIEWED_10.md) or [exact model](../data/public/spell_candidates/damage_control_25_reviewed_10.json). Historical pending labels remain inside the sealed files; the actual receipt supplies acceptance. AC6, DE4 and Banishment remain accepted within their existing scopes. Runtime, human gameplay and numerical balance remain unproven.

**Persistent20 accepted and applied:** Actual GPT accepted the eight Exact07 artifacts unchanged. The [application receipt](../../../docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json) and [1,108-check verification](../../../docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_CHECK.json) bind 20 procedures, 21 placements, 40 preserved original scenarios and 57 current cases. Read the [player chapter](spells/candidates/PERSISTENT_DAMAGE_20_REVIEWED_07.md), [Director chapter](director-only/spells/PERSISTENT_DAMAGE_20_REVIEWED_07.md) or [exact model](../data/public/spell_candidates/persistent_damage_20_reviewed_07.json). Original and sealed pending labels remain history; the actual acceptance receipt controls. Conditional fixtures and pending counterpart permissions retain their limits. Runtime, human gameplay and numerical balance remain unproven.

**GPT is reviewing companion/life10:** The full [Current04 packet](../../../docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_PREPARATION.json) was [actually submitted](../../../docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_ACTUAL_SUBMISSION.json) to Review Continuation Part 4, user turn `3215cb75-04cf-48fb-8d6b-9dbc93d04850`. It contains all ten procedures, twenty original scenario texts, 27 current main cases and five explicit questions. Two Command Undeath cases remain conditional on an authoritative exact CR2 Undead. The [sent update](../../../docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_SUBMITTED_REQUEST.txt) includes persistent20's actual acceptance and the verified GitHub backup. Preserve the complete actual reply and reconcile its decisions before any adoption; no result is inferred while GPT reviews.

**Remaining spell work:** [Queue11](../data/director/spell_review/remaining_work_queue_11.json) retains 323 pending identities: 106 in fourteen active/prepared groups, with 216 other original-source identities and one receipt task. [Registry06](../data/director/spell_review/accepted_interface_registry_06.json) contains 173 scoped interfaces, preserving all 143 earlier entries. Its persistent20 additions retain full procedures and root mappings. The [rank-seven mechanics16 source conference](../../../docs/audit/2026-10-08/full-game/RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_PREPARATION.json) combines the preserved Evocation8 and Enchantment8 preparations, classifies each spell separately (one tier A, twelve B, three C), and asks 33 new questions. It remains UNSENT with no current worked cases or adoption. Information8, Eye of Judgement and the other prepared conferences remain separate reviews.

**GitHub preservation:** [Verified main `3ece00c`](../../../docs/audit/2026-10-18/github-snapshot-damage25/PUSH_RECEIPT.json) includes damage25's application and source conferences through checkpoint15: 23,896 expected blobs verified and all 23,767 prior tracked entries retained. Persistent20's actual final/application, registry06, queue11, companion Current04's actual submission, the combined rank-seven source packet and checkpoint16 are later local progress. No source information was deleted or history rewritten. All 75 domain gates remain separate; this progress does not establish whole-game flow, runtime, balance, cosmology or release approval.

