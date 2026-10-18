# Decennium Descent — active development direction

Effective 16 October 2026, Decennium Descent is a **video game only**. Tabletop/TTRPG development is retired by the owner. The [verbatim directive](mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md) takes precedence over conflicting tabletop requirements in older plans and the [original accelerated review protocol](mechanics/SPELL_REVIEW_PROTOCOL.md). Both originals remain preserved.

Build a deep, deterministic computer RPG. The engine handles the bookkeeping; the player interface presents understandable choices and results. Retain complexity when it earns its place in gameplay.

## What work continues

Develop source-faithful engine specifications, data schemas, state transitions, deterministic test vectors and useful player descriptions. Preserve spell/class identity, access, rank, school, lore and source provenance. Each operation needs precise eligibility, geometry, timing, resource commitments, ownership, lifecycle and cleanup.

The [49-entry interface registry](../data/director/spell_review/accepted_interface_registry_02.json) is the current reuse index. Its exact source scopes and provisional/pending distinctions still govern. Existing accepted contracts remain usable; a tabletop heading or historical acceptance label does not invalidate their mechanics. Do not reopen them without a genuine contradiction or required narrow digital decision. This registry is documentation, not implemented engine code.

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

- Recorded ordinary-spell coverage remains **451 reviewed / 397 pending**, across 848 identities. The [inventory](../data/director/spell_review/ordinary_spell_inventory_01.json) preserves every pending identity. No spell is promoted by this direction change.
- AC6 Current06 was submitted once to the actual GPT notebook. Later notebook discussion describes AC6 as completed, but its exact Current06 acceptance artifact still needs recovery and verification before local adoption. Do not resend the package or count the 14 as adopted prematurely.
- The next [25-spell semantic delta](../data/director/spell_review/damage_control_25_semantic_delta_01.json) is prepared: 10 routine and 15 interaction-heavy spells. Its 1,349-check preflight verifies source/structure/accounting; it does not validate unwritten procedures, arithmetic, geometry or runtime behavior.
- DE4 current03 remains unadopted. Two identified test-fixture issues need correction: Phantasmal Killer uses an impossible same-class school combination, and Field Repair omits touch/recharge prerequisites. The separate Fate Reversal guard proposal remains pending; this directive does not approve its systemic extension.
- Continue the other digital game domains and final joint whole-game flow review. Cosmology retains its careful source/canon boundaries. Latest verified GitHub backup is `18c6e3a`; newer local work is not represented by that backup.

The [coverage ledger](../data/playtest/game_development_coverage.json), [owner start page](../../../START_HERE.md) and [current checkpoint](../../../docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json) carry this direction. Older checkpoints are historical where they conflict.
