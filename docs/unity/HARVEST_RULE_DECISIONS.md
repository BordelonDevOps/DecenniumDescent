# Harvest rule decisions

**Scope:** schema41/42's bounded finite-source harvesting slice on branch `Engine`. The rules below separate pinned playtest source, Codex/GPT interpretation, and test-fixture limits. This is not release approval.

## Agreed source reading

- Generic extraction can be attempted without Fishing training when it is physically possible and all actual tool, site, access, custody, and restricted-material requirements are met. Use Wisdom for Fishing. An untrained lead receives no proficiency contribution and rolls with disadvantage. A qualifying trained lead adds the recorded proficiency contribution once; expertise replaces the ordinary contribution according to its own rule. Fishing level is not added to the check.
- Recipe/formula access restrictions are not a generic-harvest gate. Material-specific authority and consent restrictions still apply.
- A Fishing critical-failure minor accident uses the trade reference's piercing injury type for the fallback `1d4`. If an actual declared hazard applies, resolve that hazard instead. Do not also roll a manufacturing mishap.
- The generic extraction result is one finite attempt against an already-existing source. It never creates a creature, death, ownership right, source unit, or replenishment.

The [pinned source snapshots](evidence/2026-11-05-finite-source-harvesting/sources/CRAFTING_HARVEST_PLAYTEST.md) at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4` define generic access, Wisdom/trade/tool checks, the Tiny 10-minute / one-unit base, four-degree outcomes, and preservation starting at death. The pinned [trade reference](evidence/2026-11-05-finite-source-harvesting/sources/CRAFTING_TRADE_REFERENCE.md) lists Fishing's primary tool as Fishing tackle and assigns piercing to its injury. Exact blob IDs and hashes are in the evidence manifest.

The [GPT consensus receipt](evidence/2026-11-05-finite-source-harvesting/GPT_CONSENSUS.md) records the independent reading through **Unity Rules Engine Development**. The source contradiction was only in the first implementation, which had incorrectly treated skill rank as an access gate.

## Implemented schema41 slice

- One authored `TEST_ONLY` Tiny river-fish remains fixture, fixed manifest/category, preallocated generic-fish-meat unit, unknown sale value, and one lead.
- The work command reserves an exact 10-minute interval. Starting, pausing, resuming, tactical interruption, save/load, and idempotent replay preserve exact credit and RNG ordering.
- The lead must have access to the actual Fishing tackle, knife, stable surface, open receiving tray, adequate receiver capacity, eligible remains, and lawful origin. Untrained generic extraction is allowed after those checks.
- A trained check records Wisdom, proficiency rank and contribution once, and the normal single-die result. An untrained check records Wisdom with rank/contribution zero and disadvantage dice. Existing shared check-degree and RNG systems resolve the result.
- Success settles only the selected unit into linked inventory/cargo and subtracts exactly its mass from the same remains. Failure ruins only the selected finite unit and awards no cargo. Critical failure records and applies the piercing `1d4` fallback through the existing damage/life path.
- Each unit retains its origin timestamp and preservation interval. The unit projection computes Fresh, Degraded, and Spoiled boundaries from death/removal time; harvested food remains generic material with no invented nutrition or price.

## Implemented schema42 fixture extension

- The same TEST_ONLY fish fixture can use a Small 1d2 finite yield, resolved once from the shared RNG when its manifest is created. The source-sized time is 20 minutes. A fixed two-unit base allocation is partitioned across one or two categories, with a preregistered damaged-but-recoverable unit in the fixture.
- A selected category allocation uses one check for all its allocated units. Partial selection uses the source fraction of full time and forfeits the unselected pool when work first advances. Success recovers selected intact units; Critical Success may add the selected preregistered recoverable damaged unit. Failure ruins the unique highest-value unit or honors the recorded tied-unit choice and exhausts the other selected units. Unknown competing values and missing tie choices reject before work.
- Manifest identity and anatomy version stay separate: `Command.Target` selects the manifest record, and `HarvestSelectionRequest.ManifestVersionId` must equal that record's `AnatomyVersionId`. Donor and manifest anatomy profiles must match. These are identity and admission constraints, not new harvest rules.
- Schema42 tests cover finite yield persistence, source allocation, save/load, command reconstruction, duplicate replay and the bounded outcomes. The repair record is in [schema42 harvest validation evidence](evidence/2026-11-05-harvest-validation-repair/README.md).

## Known gaps

- This is not a general harvest engine. It admits one fixed TEST_ONLY fish and one selected lead; its Tiny/Small profiles and one/two-category allocations are fixtures, not general manifest authoring. Identification, runtime-authored anatomy/material profiles, assistants, environmental nodes, plants, mining, salvage, container-volume settlement and the broader gathering catalog remain unimplemented.
- Declared-hazard execution is not represented by this fixture; the test covers the no-hazard Fishing fallback only.
- The snapshot records the accident type, but does not yet generalize damage-type resistance for all harvesting hazards.
- The harvest-unit projection computes two-stage preservation. The older generic inventory lot currently exposes a single `FreshUntil` field, so all generic inventory consumers do not yet use the full Degraded/Spoiled lifecycle.
- The fish death lifecycle event is fixture provenance, not a general creature/death event service. Legal consent and authority records are only admitted as fixture restrictions.
- Unity import, Unity compilation, Edit Mode, Play Mode, player build, and gameplay qualification have not been run. C# headless tests and static package structure checks do not pass those gates.

## Verification evidence

See [the schema41 evidence folder](evidence/2026-11-05-finite-source-harvesting/README.md), the exact [source bindings](evidence/2026-11-05-finite-source-harvesting/SOURCE_BINDINGS.json), and the deterministic [headless result](evidence/2026-11-05-finite-source-harvesting/HEADLESS_RESULTS.json).
