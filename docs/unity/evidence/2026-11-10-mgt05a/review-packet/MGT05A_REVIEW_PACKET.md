# MGT-05A review packet — schema74 harvest preservation and requirement work

**Purpose:** GPT implementation review of the exact C# candidate and its evidence. The implementation remains TEST_ONLY and is not accepted as complete until GPT reviews this packet.

## Scope and rules boundary

This candidate adds a schema74 TEST_ONLY preservation view over an extracted harvest unit and a single `Fresh`-ingredient work adapter. It derives preservation from the existing harvested unit's origin/degradation timing and physical inventory ancestry; it does not persist a second age, freshness, value, mass, clock, or RNG authority. Work uses the shared `RuleClock`, `WorkLedger` reservation, `ActiveWorkProgress`, inventory, command receipt and snapshot codec. Schema73's existing encoding and behavior remain on the prior branch; schema74 is explicitly TEST_ONLY.

Previously agreed in the GPT source/API discussion: keep preservation as a projection over harvested mass; use `OrdinaryInventory` descendants for portioned generic pounds; add schema74-only fixture/codec state for the new work adapter; preserve schema73 profile, bytes and behavior. This packet requests implementation acceptance of the exact revision and asks whether the missing custody-transfer/storage witness blocks acceptance.

## Changed code and exact diff

The committed candidate's full code patch is attached as `MGT05A_CODE_DIFF.patch`. It contains all 22 changed/added package files: 19 C# source files and three Unity `.meta` files. In particular, new files are:

- `Laboratory/Model/SharedHarvestPreservation.cs`
- `Runtime/Core/HarvestPreservationRecords.cs`
- `Runtime/Persistence/HarvestRequirementWorkCodec.cs`

The exact repository revision and GitHub commit URL are in the message accompanying this packet. The parent checkpoint is `9bd8ffc316c5e9835ae0b632e8635ba4598842ca` on `Engine`.

## Acceptance scenario and evidence

The connected test is `mgt05a_harvest_mass_preservation_work_deadline_save_restore_and_replay` in `engine/com.decennium.foundation/Tests/EditMode/HarvestCases.cs:148`. It performs an actual finite harvest; splits one tenth of physical mass while retaining lineage, owner and freshness; retrieves that lot to a carrier through the portable-equipment handler; starts Fresh-required work that reserves the same existing mass; pauses with exact progress; saves/restores byte-identically; compares deterministic replay; and checks exact B1/B2 preservation boundaries with whole versus split clock advancement. At B1 further work is paused while the reservation remains; by B2 the projection is Spoiled with zero multiplier and no additional labor.

**Transfer/storage witness: explicitly outstanding.** The test invokes `HandlingKind.Retrieve` (`HarvestCases.cs:171-174`), but does not exercise actor-to-actor handover, putting the harvested lot into a storage container, or a store/retrieve/repackaging cycle. The current evidence therefore establishes a portion plus portable retrieval and worker use, not a complete transfer-and-storage lifecycle. GPT should decide whether that gap is a concrete blocker for this bounded module or a follow-up acceptance case.

## Retained validation results

The four attached result JSON files are the original retained reports, preserving their existing source-hash arrays:

- Full C# 9 warnings-as-errors regression: **PASS 1,320/1,320**, 279 source hashes; Core/Persistence/LabModel compilation PASS. `full-suite-final/run-20261110T131302203Z-5e2e44ce/results.json`.
- Connected scenario: **PASS 1/1**, same 279 source hashes; `focused-integration-final/run-20261110T130941930Z-7c09553b/results.json`.
- Rejection/compatibility cases: **PASS 1/1**, same 279 source hashes; `focused-rejections-final/run-20261110T131032550Z-94df8b97/results.json`.
- Static Unity package structure: **PASS 18/18**, 305 package assets / 305 unique GUIDs; 599 source-hash entries; `package-validation/static-20261110T131251090Z-bbf9fc7d/results.json`.

I recomputed SHA-256 against the working source and confirmed all **19/19** changed C# implementation/test files match the hashes in both the full-suite report and package-validation report. The exact 19 path/hash pairs follow.

| Source file | SHA-256 bound by full suite |
|---|---|
| `Laboratory/Model/OrdinaryInventory.cs` | `9ba6e9c4772944eb7fe8ab3345316d6a0a05b27102a7cc76551263510f8bf952` |
| `Laboratory/Model/PortableStorage.cs` | `759b34a390274fd6f3d1949734943da02661adcd195ad9bcc50753dc855e1d33` |
| `Laboratory/Model/SharedCraftingConsequences.cs` | `35346cb8b37b9e16838c63eaf468bd3c76db38e0d87446d46e03b82f36e1185d` |
| `Laboratory/Model/SharedHarvest.cs` | `4b129731d6d2b40ea7d3dc73d514f0e06cdac595375169d04a838df4956ceecd` |
| `Laboratory/Model/SharedHarvestPreservation.cs` | `360094bf6a70c560737e35f9697f64251b1aa5d741a9f2889c75966d39cfec62` |
| `Laboratory/Model/SharedToolRepair.cs` | `6fd4f299a78cbe46343c8fa608149524ebab9c92c6f8c33e41d61af23967886e` |
| `Laboratory/Model/SharedWorldCommandQueries.cs` | `e36961790281dc352a93f8af30c670eaeb085793cd61db469a9c23b04fcca2b4` |
| `Laboratory/Model/SharedWorldRangedCombat.cs` | `ac11880745fb3a845d6ba24a98be30c303e2159e6e7a903241a5e58a71393d0a` |
| `Laboratory/Model/TestOnlyInventoryPolicy.cs` | `2ba8d853ec8163382e3626aa12a195e472cca75a6cc4a4296d432f7d0874e4b0` |
| `Laboratory/Model/TestOnlySharedWorldPolicy.cs` | `e54721193b99535198c91d13c84261f5937cbb3e5dc7cd83c1d9e2f5c11c3a4e` |
| `Runtime/Core/ExpeditionPressureRecords.cs` | `2ab46c13fdef6ed392fc49179ad7a1e7ad5378150fe8df72d1dce6784f430c19` |
| `Runtime/Core/HuntingTrapRecords.cs` | `3753365fd29d0d04557449f27cb17720fdaf245b82f89b7780834f6bd73c2ee6` |
| `Runtime/Core/PortableEquipmentRecords.cs` | `7a729d990ce3ec0465c776a22c2183af18abc0ec503b2f32f007205b6116c768` |
| `Runtime/Core/HarvestPreservationRecords.cs` | `61a5f6adfcee07e2e537dffe7fdfa6058da87397d43795d3f2a27fc7a3815719` |
| `Runtime/Core/Simulation.cs` | `82f0c187925438b15eaa2cc35145df3b028396677069d64607d37de7201973a2` |
| `Runtime/Core/WorldActivityRecord.cs` | `f33e816d921f69ae60d6fc1e94d0c943fd204417ab6673971f06d8a61dc034b1` |
| `Runtime/Persistence/SnapshotCodec.cs` | `76a1c390f0f81fce62f0f345a9cb50113d463642095328a3d36752e5c0e8a5cf` |
| `Runtime/Persistence/HarvestRequirementWorkCodec.cs` | `c70918bc0cf4479cd2447b70cc62878bb563118f084b21002314fb31c9b9fc5b` |
| `Tests/EditMode/HarvestCases.cs` | `24d4821bcdaba0e8c24711ef58aa964783b1e2b0b5ae89060ae21a3976128bcd` |

## Known limitations and check boundaries

This candidate does not generalize preservation to all foods, materials, harvest methods, production recipes, or storage conditions. The test does not demonstrate actor handover or stored/repacked freshness. Final C# compilation, focused and full regression, and static package checks passed. Unity Editor import/compilation, Edit Mode, Play Mode, standalone game build, and observed player gameplay were **not run**.

Earlier attempts are retained under the adjacent `attempts/`, `focused-integration/`, `focused-rejections/`, and `package-validation/` directories. They exposed ordinary compile defects (captured `out` parameter in a lambda and an enum member mismatch), a focused clock advance rejected as `InvalidResult`, a schema73 test fixture targeting an unknown inventory lot, and a missing `.meta` check. The final candidate reports above supersede these failed attempts; the focused schema73 rejection now passes with save bytes unchanged.
