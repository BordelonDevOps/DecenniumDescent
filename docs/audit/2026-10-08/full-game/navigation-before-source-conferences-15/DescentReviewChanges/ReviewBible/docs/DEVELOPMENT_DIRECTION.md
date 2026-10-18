# Decennium Descent — active development direction

Effective 16 October 2026, Decennium Descent is a **video game only**. Tabletop/TTRPG development is retired by the owner. The [verbatim directive](mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md) takes precedence over conflicting tabletop requirements in older plans and the [original accelerated review protocol](mechanics/SPELL_REVIEW_PROTOCOL.md). Both originals remain preserved.

Build a deep, deterministic computer RPG. The engine handles the bookkeeping; the player interface presents understandable choices and results. Retain complexity when it earns its place in gameplay.

## What work continues

Develop source-faithful engine specifications, data schemas, state transitions, deterministic test vectors and useful player descriptions. Preserve spell/class identity, access, rank, school, lore and source provenance. Each operation needs precise eligibility, geometry, timing, resource commitments, ownership, lifecycle and cleanup.

The [143-entry interface registry](../data/director/spell_review/accepted_interface_registry_05.json) is the current reuse index. Its exact source scopes and provisional/pending distinctions still govern. Existing accepted contracts remain usable; a tabletop heading or historical acceptance label does not invalidate their mechanics. Do not reopen them without a genuine contradiction or required narrow digital decision. This registry is documentation, not implemented engine code.

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

**Current position — 18 October 2026:** **505 ordinary spells reviewed / 343 pending**, with 229 complete standalone procedures across all 848 identities. The [current authored index](../data/public/spell_playtests/authored_review_index.json), [checkpoint14](../../../docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_DAMAGE25_APPLIED_PERSISTENT_ACTIVE_14.json) and [review map](../../../REVIEW_MAP.html) are the entry points. Working folder: `C:\Github\DecenniumDescent`. Continue until the review is complete or any reported allowance reaches 20% remaining; the latest observation was 64% remaining.

**Damage/control25 accepted and applied:** Actual GPT accepted all eight Exact10 artifacts unchanged. The [application receipt](../../../docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json) and [1,039-check verification](../../../docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json) bind all 25 procedures, 26 placements, 70 current cases, 36 original scenarios and 77 complete sources. Read the [player chapter](spells/candidates/DAMAGE_CONTROL_25_REVIEWED_10.md), [Director chapter](director-only/spells/DAMAGE_CONTROL_25_REVIEWED_10.md) or [exact model](../data/public/spell_candidates/damage_control_25_reviewed_10.json). Historical pending labels remain inside the sealed files; the actual receipt supplies acceptance. AC6, DE4 and Banishment remain accepted within their existing scopes. Runtime, human gameplay and numerical balance remain unproven.

**GPT is reviewing persistent20:** [Exact07 was submitted](../../../docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_SUBMISSION.json) to Review Continuation Part 4, user turn `82f23f2f-dc41-4814-9d0f-ec6c331ee127`. The packet contains 20 complete procedures, 21 placements, 40 original scenarios and 57 current cases. The [sent update](../../../docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_SUBMITTED_REQUEST.txt) includes damage25's actual final, the verified GitHub backup, companion Current04 and the five unresolved questions. Preserve and verify GPT's actual final before applying it. No persistent20 acceptance is inferred while it runs.

**Companion/life10 is the next case conference:** [Current04](../../../docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_PREPARATION.json) contains all ten returned procedures, twenty original scenario texts and 27 current main cases. Two positive Command Undeath cases remain conditional on a real authoritative exact CR2 Undead. Five questions concern Soulburn with Grand Reservoir, Wraith handling anatomy and mass, Ghast cone geometry, and that missing profile. Three [complete local repairs](../../../docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_LOCAL_DELTAS.json) preserve actual Ghast armor, the full countering Wizard, and a paid command before readied suppression. The full Current04 packet is still **UNSENT**; GPT has received its progress summary only.

**Remaining spell work:** [Queue09](../data/director/spell_review/remaining_work_queue_09.json) retains 343 pending identities: 101 in twelve active/prepared groups, nine other earlier complete proposals, and 233 original-source or receipt tasks. [Registry05](../data/director/spell_review/accepted_interface_registry_05.json) indexes 143 exact scoped interfaces. Its 35 damage25 entries add no global rule, sixth Fate presentation or new source permission. The [registry/queue check](../../../docs/audit/2026-10-08/full-game/DAMAGE25_REGISTRY_QUEUE_05_CHECK.json) preserves all 108 prior interfaces and all original spell identities. Prepared packets for control, illusions, memory, creation, terrain, body/defense, time, transport, magic modifiers and life/matter remain separate reviews.

**GitHub preservation:** [Verified main `19423ad`](../../../docs/audit/2026-10-18/github-snapshot-companions/PUSH_RECEIPT.json) includes companion Current04 and the queued source conferences through checkpoint13: 23,702 expected blobs verified and all 23,461 prior tracked entries retained. The new damage25 final/application, persistent20 submission and checkpoint14 are later local progress. No source information was deleted or history rewritten. All 75 domain gates remain separate; this progress does not establish whole-game flow, runtime, balance, cosmology or release approval.

