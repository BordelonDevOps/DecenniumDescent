# MGT-05C implementation review packet

**Status: implementation committed; GPT implementation review pending.** Code commit: [`27dea8d0343b385539b8703255064301974c6e27`](https://github.com/BordelonDevOps/DecenniumDescent/commit/27dea8d0343b385539b8703255064301974c6e27) on branch `Engine`. The actual GPT source/API contract approval is recorded in [GPT_REVIEW.md](GPT_REVIEW.md); it is not implementation acceptance. The exact code diff is [MGT05C_IMPLEMENTATION.patch](MGT05C_IMPLEMENTATION.patch), SHA-256 `31542e1b05224a88edf6865f1334ed86d6f69f3e08adf5e36da040df30733dd3` (108,094 bytes).

## Agreed responsibility and authority

This schema76 `TEST_ONLY` increment implements the approved clean-opening, in-vessel portion, physical retrieval and actual exposure slice. Its requirements and adopted interpretation are in [MGT05C_RULE_DECISIONS.md](MGT05C_RULE_DECISIONS.md), based on the pinned “Preservation and spoilage” source at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

It reuses the shared simulation and these authoritative records:

- Successful treatment history, harvest origin and shared `RuleClock` derive half-open coverage and unprotected age.
- `PortableHandlingRecord` supplies actual open, close and retrieval completion times; `PortableEquipmentRecord` supplies current placement, containment, owner and custodian.
- `InventoryLotRecord`, `OrdinaryInventory.Descendant` and `WorkLedger` supply ancestry, provenance and conserved available mass.
- Command receipts and revisions bind evidence to the command that caused it.
- A fingerprinted clean-utensil fact and three fixed typed exposure occurrences provide this fixture’s explicit TEST_ONLY trust boundary.

The new append-only evidence does not store age, current location, quantity, a mutable protection flag or a second clock. New evidence is rejected below schema76, and the binary evidence section is appended only for schema76. Schemas74 and75 retain their own codec branches, profiles and rules.

## Implementation and changed code

The commit changes these 14 files:

- `engine/com.decennium.foundation/Runtime/Core/Simulation.cs`
- `engine/com.decennium.foundation/Runtime/Core/HarvestPreservationRecords.cs`
- `engine/com.decennium.foundation/Runtime/Core/ExpeditionPressureRecords.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/SnapshotCodec.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/HarvestPreservationEvidenceCodec.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/HarvestPreservationEvidenceCodec.cs.meta`
- `engine/com.decennium.foundation/Laboratory/Model/SharedCraftingConsequences.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedHarvest.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedHarvestPreservation.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedHarvestPreservationTreatment.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldRangedCombat.cs`
- `engine/com.decennium.foundation/Laboratory/Model/TestOnlyInventoryPolicy.cs`
- `engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs`
- `engine/com.decennium.foundation/Tests/EditMode/HarvestPreservationTreatmentCases.cs`

The new profile is an explicit schema76 extension of the existing MGT-05B TEST_ONLY fixture. It records a controlled opening only when the existing worker, vessel, physical tool and shared clock qualify. A directly treated lot may be split once for that opening while still physically inside the vessel. The child retains the source lot’s biological origin and freshness fact, and receives the existing zero-duration split semantics. Protection for the child continues while eligible in the vessel and ends permanently at its successful `Retrieve.EndedAt`; putting it back later cannot reactivate this treatment.

Coverage remains bounded by the original `CompletedAt + 86,400 seconds`, a prospectively unresolved opening cutoff at `O + 60 seconds`, the actual exposure time, and the child’s actual removal time. These are derived from treatment/evidence/handling history. Protected-age intervals are combined by union. Three known occurrence IDs map to breach, contamination and incompatible heat. Unknown and duplicate occurrences reject; an exposure records the current clock and consumes no RNG.

The profile rejects protected portions outside a qualifying opening, a second portion for the same opening, recursive protected portioning, protected-child retrieval in tactical mode, fixture exposure in tactical mode, and a tactical transition while a controlled opening is still unresolved.

## Acceptance evidence

The exact-source focused runner compiled Core, Persistence, LabModel and HeadlessTests using C# 9 with warnings treated as errors. All seven reports use the same 283 source-file hashes; the sorted source/hash set digest is `acd1b210be70141d00ca887ec40a3d833823a10e5a5a5cf2d582aa212cdf6e98`. The report and binary index is [BINDINGS.json](validation/BINDINGS.json); the four representative compiled assemblies are retained in [validation/assemblies](validation/assemblies/).

| Case | Result | Retained report |
| --- | --- | --- |
| MGT-05B closed-vessel treatment, lineage, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230641383Z-6e762f84/results.json) |
| MGT-05B failed treatment and one-time supply settlement | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230713806Z-d681399a/results.json) |
| MGT-05B degraded treatment and spoilage deadlines | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230742338Z-25cf86ba/results.json) |
| MGT-05B lineage cutoff, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230810849Z-f2dca79f/results.json) |
| MGT-05B closed-vessel handover, custody, ownership and replay | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230843269Z-7405d561/results.json) |
| MGT-05C controlled opening, conserved in-vessel portion, retrieval cutoff, return-to-vessel rejection of resumed protection, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230912332Z-5a0167b7/results.json) |
| MGT-05C exact O+59/O+60 closure, clock crossings, typed exposure, duplicate/unknown events, exact expiry, no RNG change, post-removal history, schema downgrade and partitioned-clock outcome | PASS 1/1 | [results](validation/attempt-results/final-focused/run-20261110T230944000Z-24aa6b21/results.json) |

The cases save and restore snapshots through `SnapshotCodec`, compare identical replays byte-for-byte, and check equal derived age/state/RNG for whole versus partitioned advances. The main path verifies original `FreshUntil`, `NutritionKind.None`, owner, `WorkLedger` quantity and current physical custody. Exposure after retrieval leaves the removed child’s already-earned protection history unchanged.

### Transfer-and-storage witness in code

- [Eligibility and existing split authority](../../../../engine/com.decennium.foundation/Laboratory/Model/TestOnlyInventoryPolicy.cs#L114) permits a protected lot only when a live controlled opening qualifies, then delegates mass splitting to `OrdinaryInventory.Descendant`.
- [Causal portion evidence](../../../../engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs#L869) captures the current opening, invokes the existing inventory resolver, identifies the created child, and binds the child to the same vessel, command and revision.
- [Evidence validation](../../../../engine/com.decennium.foundation/Runtime/Core/HarvestPreservationRecords.cs#L126) verifies the causal portion command, treatment root, child ancestry, unchanged origin/freshness semantics, physical vessel containment (or a first later retrieval from that vessel), and available mass amount.
- [Derived removal cutoff](../../../../engine/com.decennium.foundation/Runtime/Core/HarvestPreservationRecords.cs#L352) reads the first physical `Retrieve` completion for the evidenced child; the test [saves before retrieval, then retrieves and checks the child/remainder separately](../../../../engine/com.decennium.foundation/Tests/EditMode/HarvestPreservationTreatmentCases.cs#L442).

The same source/test bodies are included in the exact commit diff at [MGT05C_IMPLEMENTATION.patch](MGT05C_IMPLEMENTATION.patch); the in-repository validation reports bind the compiled code to all 283 source hashes.

Static package validation passed **18/18** checks over **309 assets**, **309 unique GUIDs**, and **607 file hashes**. The retained report is [package/results.json](validation/package/results.json). It is structural validation; it is not a Unity import or Unity compilation result.

## Failed attempts and validation not performed

Earlier implementation attempts and their `results.json` reports are preserved under [attempt-results](validation/attempt-results/). Corrections addressed: a nonexistent `CampGreens.Subtract` API in test arithmetic; passing two names to the runner’s single-case `-CaseName` argument; schema76’s need to be explicitly admitted by the existing empty TEST_ONLY pressure and harvest-profile gates; and test assertions that either compared serialized bytes across different command histories or referenced custody on the wrong record. The current seven source-bound reports pass.

The all-cases suite was started, then stopped before it produced `results.json` after code and test files changed while it was compiling. It is explicitly not counted as a pass; see [INCOMPLETE_FULL_SUITE.txt](validation/INCOMPLETE_FULL_SUITE.txt). A full-suite run against this exact commit remains unperformed. Unity import/compilation, Edit Mode, Play Mode, player build, scenes and observed gameplay were not run; Unity gameplay integration remains deferred by the project instructions.

## Limits and review gate

This is a bounded TEST_ONLY witness for the already authored fish, one vessel, one treatment and one physical Cook’s-utensils item. Cleanliness and exposure are explicit fixture facts, not production environmental simulation. Other foods/materials, generic contamination, production recipes, re-treatment, generalized repackaging and recursive protected subdivision remain unsupported. No broader mechanics or unresolved rule gaps were added.

GPT must review this exact code commit and retained packet before the next mapped module begins. No successor implementation has started.
