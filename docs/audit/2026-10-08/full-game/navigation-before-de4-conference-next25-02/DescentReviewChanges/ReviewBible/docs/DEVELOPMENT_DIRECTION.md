# Decennium Descent — active development direction

Effective 16 October 2026, Decennium Descent is a **video game only**. Tabletop/TTRPG development is retired by the owner. The [verbatim directive](mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md) takes precedence over conflicting tabletop requirements in older plans and the [original accelerated review protocol](mechanics/SPELL_REVIEW_PROTOCOL.md). Both originals remain preserved.

Build a deep, deterministic computer RPG. The engine handles the bookkeeping; the player interface presents understandable choices and results. Retain complexity when it earns its place in gameplay.

## What work continues

Develop source-faithful engine specifications, data schemas, state transitions, deterministic test vectors and useful player descriptions. Preserve spell/class identity, access, rank, school, lore and source provenance. Each operation needs precise eligibility, geometry, timing, resource commitments, ownership, lifecycle and cleanup.

The [78-entry interface registry](../data/director/spell_review/accepted_interface_registry_03.json) is the current reuse index. Its exact source scopes and provisional/pending distinctions still govern. Existing accepted contracts remain usable; a tabletop heading or historical acceptance label does not invalidate their mechanics. Do not reopen them without a genuine contradiction or required narrow digital decision. This registry is documentation, not implemented engine code.

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

- Ordinary spells: **465 reviewed / 383 pending**, across 848 identities. The [current inventory](../data/director/spell_review/ordinary_spell_inventory_02.json) preserves every pending identity.
- AC6 Current06 is locally applied under the [exact Director acceptance/application receipt](../../../docs/audit/2026-10-08/full-game/AC6_EXACT_ACCEPTANCE_06_RECEIPT.json). All eight accepted files remain byte-identical; 1,367 application checks passed. The registry now includes its scoped interfaces.
- The [next 25-spell semantic delta](../data/director/spell_review/damage_control_25_semantic_delta_01.json) remains prepared: 10 routine and 15 interaction-heavy identities. The earlier preflight is source/structure evidence, not validation of unwritten procedures or engine behavior.
- [DE4 Current04A](../data/director/spell_proposals/divination_enchantment_rank4_current_04a.json) fixes known fixture and evidence-reference errors while retaining all 15 procedures as unadopted. Its Fate guard remains pending consequential conference. Check any AC6 dependencies against accepted Current06 before the DE4 review.
- The actual GPT notebook received the [latest AC6 integration/DE4 status handoff](../../../docs/audit/2026-10-08/full-game/DIRECTOR_LATEST_CHANGES_2026_10_17_SUBMISSION_RECEIPT.json). A full response is still pending; the later registry refresh and 04A citation fix are local follow-through.
- Continue the full 75-domain objective and final joint whole-game flow. Latest verified GitHub backup is `c1e2b7d`; this AC6 integration and later changes are local. Cosmology retains careful source/canon boundaries.
- The owner requests focused development until **20% allowance remains**. Read actual account usage at work boundaries; stop when any reported usage window reaches 80% used. The first reading was 2% weekly used; a separate short-term window was unavailable.

The [coverage ledger](../data/playtest/game_development_coverage.json), [owner start page](../../../START_HERE.md) and [current checkpoint](../../../docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AC6_APPLIED_DE4_04A.json) carry this direction. Older checkpoints remain history.
