# MGT-05A implementation review packet — schema74 TEST_ONLY

This packet requests GPT's review of the corrected MGT-05A candidate. GPT has **not** accepted the correction yet. The review gate remains open; do not begin MGT-05B until GPT accepts the exact revision identified in the handoff message.

## Prior review and agreed resolution

GPT reviewed commit 300fa051bb40ceb6f535b20bcc58bde0e78d0729 and returned **CHANGES REQUIRED**. It identified three concrete blockers and one associated acceptance-coverage gap:

1. Demonstrate actual transfer and storage for a harvested descendant, including ownership/origin, custody/location, ledger quantity, and freshness through the natural B1 boundary.
2. Correct positive-gap Fresh-work resume validation across a paused interval, including the boundary-partition comparison, save/restore, and deterministic replay.
3. Limit the empty Pressure history exception to schema74 TEST_ONLY while preserving schema73 Pressure validation and a genuine schema73 save roundtrip.
4. Add the query-only eligibility matrix: Fresh satisfies Fresh and Ordinary; Degraded satisfies Ordinary; Spoiled fails Ordinary and satisfies Spoiled. The persisted work adapter remains Fresh-only.

GPT's follow-up on worker scheduling chose **Option A**: hand the real harvested descendant to an existing actor in WorldSchedule.Order and let that scheduled actor perform the adapter work. GPT explicitly said not to edit schedules, rewrite ownership, create stock, bypass the resolver, or add a MGT-05A exception to the shared off-calendar gate. No disagreement remains on that point.

## Responsibilities, authorities, and scope

This is a bounded schema74 TEST_ONLY increment over the existing finite-harvest fixture. HarvestPreservationRules derives state from the existing extracted HarvestUnitRecord, InventoryLot ancestry, physical WorkLedger mass, PortableEquipment identity, FreshUntil, and the shared RuleClock. It introduces no second age, clock, mass, value, inventory, or RNG authority.

The adapter stores only its TEST_ONLY worker, lot, Fresh requirement, reservation, status, pause reason, timestamps, and ActiveWorkProgress. WorkLedger remains the reservation and interval authority; existing commands, receipts, RuleClock, SnapshotCodec, and deterministic RNG remain authoritative. Ordinary and Spoiled are query-only requirements; they do not create new persisted adapter lifecycles. Schema74's empty-Pressure exception is limited to TEST_ONLY. Schema73 codec layout and ordinary profile behavior remain on their existing path.

The source-bound preservation and no-pausing-aging requirements remain those reviewed for MGT-05A. New work-adapter behavior is explicitly TEST_ONLY. No general food/material/recipe preservation system is claimed.

## Exact code diff and added files

MGT05A_CODE_DIFF.patch is the complete package diff from the pre-MGT-05A Engine checkpoint 9bd8ffc316c5e9835ae0b632e8635ba4598842ca. It contains 22 package files: 19 C# source files and 3 Unity metadata files. The three new source files are:

- Laboratory/Model/SharedHarvestPreservation.cs
- Runtime/Core/HarvestPreservationRecords.cs
- Runtime/Persistence/HarvestRequirementWorkCodec.cs

Each new source has its adjacent .meta file. The remaining 16 package sources modify existing harvest, inventory, portable-storage, shared simulation, persistence, and test authorities. The review message identifies the exact pushed correction commit and links its GitHub diff. Relative to rejected commit 300fa051, the correction changes ExpeditionPressureRecords.cs, HarvestPreservationRecords.cs, and HarvestCases.cs; it also updates the handoff, implementation map, review packet, and retains the final reports and scenario saves.

## Source and test excerpts establishing the transfer/storage witness

HarvestCases.cs, the named connected case mgt05a_harvest_mass_preservation_work_deadline_save_restore_and_replay, uses the ordinary portable handler for retrieval, handover, and authored-tray stow:

    PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,storageChild.LotId,
        handling:HandlingKind.Retrieve,actor:HarvestWorker));
    PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,storageChild.LotId,
        TestOnlyPolicy.ActorId,HandlingKind.Handover,HarvestWorker));
    PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,child.LotId,
        handling:HandlingKind.Retrieve,actor:HarvestWorker));
    PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,child.LotId,
        TestOnlyPolicy.ActorId,HandlingKind.Handover,HarvestWorker));
    PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,storageChild.LotId,
        SharedHarvestFixture.ContainerId,HandlingKind.Stow,TestOnlyPolicy.ActorId));

The following assertions bind the witness to the existing records: carried custody changes to the scheduled actor; the inventory owner remains the original owner; WorkLedger location follows the actor or tray; the stored descendant remains physically contained; handling history records the handover and stow; and the root plus both descendants still equal the harvested mass. The test keeps the stored descendant in the authored tray across B1, verifies its derived state becomes Degraded there, saves/restores at B1, then retrieves it after B1 and verifies owner, amount, FreshUntil, origin HarvestUnitId, custody, location, and derived state remain consistent. See the complete assertions at HarvestCases.cs lines 193–220 and 278–330 in the exact diff.

The custody, owner, location, storage, and ledger witness includes these assertions:

    Require(carried.ParentId==""&&carried.Placement==PortablePlacement.Carried&&carried.CustodianId==TestOnlyPolicy.ActorId
        &&retrieved.InventoryLots.Single(x=>x.LotId==child.LotId).OwnerId==storageOwner
        &&retrieved.Work.Lots.Single(x=>x.Id==child.LotId).LocationId==TestOnlyPolicy.ActorId
        &&retrieved.Work.Lots.Single(x=>x.Id==storageChild.LotId).LocationId==SharedHarvestFixture.ContainerId
        &&stored.ParentId==SharedHarvestFixture.ContainerId&&stored.Placement==PortablePlacement.Contained
        &&retrieved.Work.Lots.Where(x=>x.Id==source.Id||x.Id==child.LotId||x.Id==storageChild.LotId)
            .Aggregate(default(RuleQuantity),(sum,x)=>sum+x.Amount)==source.MassPounds,
        "Actual retrieval, handover, and authored-tray storage did not preserve ownership, lineage, custody, or ledger quantity.");

At B1 the stored descendant is still in the authored tray and the same harvested unit is the origin. After restoring from the B1 save, retrieval advances the shared clock by one second and keeps the original owner, amount, FreshUntil, and derived degradation:

    &&HarvestPreservationRules.TryProject(atB1,storageChild.LotId,out var storedDegraded)
    &&storedDegraded.State==HarvestPreservationState.Degraded
    &&atB1.PortableEquipment.Single(x=>x.Id==storageChild.LotId).ParentId==SharedHarvestFixture.ContainerId
    &&atB1.Work.Lots.Single(x=>x.Id==storageChild.LotId).LocationId==SharedHarvestFixture.ContainerId,
    ...
    &&retrievedAfterB1.Work.Lots.Single(x=>x.Id==storageChild.LotId).Amount==storageAmount
    &&retrievedAfterB1.InventoryLots.Single(x=>x.LotId==storageChild.LotId).OwnerId==storageOwner
    &&retrievedAfterB1.InventoryLots.Single(x=>x.LotId==storageChild.LotId).FreshUntil==storageFreshUntil
    &&HarvestPreservationRules.TryProject(retrievedAfterB1,storageChild.LotId,out var retrievedDegraded)
    &&retrievedDegraded.State==HarvestPreservationState.Degraded
    &&retrievedDegraded.HarvestUnitId==source.Id&&retrievedDegraded.EvaluatedAt==b1.AddSeconds(1),
    "Retrieval after B1 changed custody without preserving the original harvested item's owner, amount, age, and degraded state.");

The same case gives the scheduled actor the other unreserved descendant before reservation. It starts and pauses the same Fresh-required work, waits one active second while paused, saves/restores at B1−7, and performs a pure admissible resume query. The full eight-second branch ends at B1+1 with nine active seconds credited (two before pause and seven before B1); the comparison branch advances seven seconds to B1, saves/restores at the boundary, then advances one more second. The test compares clock, status, pause reason, retained progress, and the same reservation. Identical resumed branches produce byte-identical snapshots.

The runtime validator now checks booked active duration against required duration while Working and earned Labor while Paused, rather than rejecting resumed work because its absolute finish exceeds StartedAt plus the freshness window:

    RuleTime booked=default;
    foreach(var interval in intervals)booked=Add(booked,Subtract(interval.End,interval.Start));
    RuleTime expectedBooked=job.Status==HarvestRequirementWorkStatus.Working
        ?job.Work.Required:job.Work.Labor;
    if(booked!=expectedBooked)throw new ArgumentException(
        "Harvest requirement work booking does not match active or retained work.");

The schema74 query-only matrix is implemented in HarvestPreservationRules.SatisfiesRequirement. The adapter still validates and persists only Fresh. ExpeditionPressureRecords.cs now grants the empty-history exception only when SchemaVersion equals HarvestPreservationSchema, TestOnly is true, and every Pressure array is empty. A separate test uses a genuine schema73 recipe profile for encode/decode/restore and directly verifies schema73 still rejects empty Pressure history.

## Retained current-source validation

- Full C# 9 warnings-as-errors regression: **PASS, 1,321/1,321**; Core, Persistence, LabModel, and headless test assemblies compile; 279 source hashes. Report: full-suite-correction-final/run-20261110T155718363Z-5808ab67/results.json (started 2026-11-10 15:57:18 UTC; finished 16:20:28 UTC).
- Focused connected MGT-05A scenario: **PASS, 1/1**, same 279 current source hashes. Report: focused-corrected-final/run-20261110T162052717Z-062d75eb/results.json.
- Static Unity package validation: **PASS, 18/18**, 305 package assets and 305 unique GUIDs, with 599 source-hash entries. Report: package-correction-final/static-20261110T155700611Z-acdaf9bb/results.json.
- All **19/19** C# files changed since the pre-MGT-05A checkpoint match byte-for-byte in the full-suite and static-package source-hash records. The exact per-file hashes are listed below.
- The full-suite run retained the two scenario saves mgt05a-paused.ddsave and mgt05a-at-b1.ddsave under its saves/mgt05a_harvest_mass_preservation_work_deadline_save_restore_and_replay/ directory. They are included with the review evidence.
- Reproduction evidence: the first positive-gap companion test correctly hit the shared OffCalendarActionAlreadySpent gate before the preservation validator; GPT selected the scheduled-worker path. The broad schema73 Pressure exception reproduced and was narrowed. These are retained at attempts/gpt-review-reproduction/run-20261110T150018878Z-e9c2bc2b/results.json and run-20261110T150739613Z-8e594f0e/results.json. The corrected schema73 handler and genuine profile/Pressure focused passes are retained alongside the final reports; the full suite now passes both cases against final source.

| Changed C# source | SHA-256 (also present in full-suite and package reports) |
|---|---|
| Laboratory/Model/OrdinaryInventory.cs | 9ba6e9c4772944eb7fe8ab3345316d6a0a05b27102a7cc76551263510f8bf952 |
| Laboratory/Model/PortableStorage.cs | 759b34a390274fd6f3d1949734943da02661adcd195ad9bcc50753dc855e1d33 |
| Laboratory/Model/SharedCraftingConsequences.cs | 35346cb8b37b9e16838c63eaf468bd3c76db38e0d87446d46e03b82f36e1185d |
| Laboratory/Model/SharedHarvest.cs | 4b129731d6d2b40ea7d3dc73d514f0e06cdac595375169d04a838df4956ceecd |
| Laboratory/Model/SharedHarvestPreservation.cs | 360094bf6a70c560737e35f9697f64251b1aa5d741a9f2889c75966d39cfec62 |
| Laboratory/Model/SharedToolRepair.cs | 6fd4f299a78cbe46343c8fa608149524ebab9c92c6f8c33e41d61af23967886e |
| Laboratory/Model/SharedWorldCommandQueries.cs | e36961790281dc352a93f8af30c670eaeb085793cd61db469a9c23b04fcca2b4 |
| Laboratory/Model/SharedWorldRangedCombat.cs | ac11880745fb3a845d6ba24a98be30c303e2159e6e7a903241a5e58a71393d0a |
| Laboratory/Model/TestOnlyInventoryPolicy.cs | 2ba8d853ec8163382e3626aa12a195e472cca75a6cc4a4296d432f7d0874e4b0 |
| Laboratory/Model/TestOnlySharedWorldPolicy.cs | e54721193b99535198c91d13c84261f5937cbb3e5dc7cd83c1d9e2f5c11c3a4e |
| Runtime/Core/ExpeditionPressureRecords.cs | 8dd71d26913c453a785be1e51570acf071317acd215d49993ad5a7cf1b17e996 |
| Runtime/Core/HuntingTrapRecords.cs | 3753365fd29d0d04557449f27cb17720fdaf245b82f89b7780834f6bd73c2ee6 |
| Runtime/Core/PortableEquipmentRecords.cs | 7a729d990ce3ec0465c776a22c2183af18abc0ec503b2f32f007205b6116c768 |
| Runtime/Core/HarvestPreservationRecords.cs | ec325d704977a60aea2f0cbed276086ed19e3f28f5608179b01559eb2a0f9875 |
| Runtime/Core/Simulation.cs | 82f0c187925438b15eaa2cc35145df3b028396677069d64607d37de7201973a2 |
| Runtime/Core/WorldActivityRecord.cs | f33e816d921f69ae60d6fc1e94d0c943fd204417ab6673971f06d8a61dc034b1 |
| Runtime/Persistence/SnapshotCodec.cs | 76a1c390f0f81fce62f0f345a9cb50113d463642095328a3d36752e5c0e8a5cf |
| Runtime/Persistence/HarvestRequirementWorkCodec.cs | c70918bc0cf4479cd2447b70cc62878bb563118f084b21002314fb31c9b9fc5b |
| Tests/EditMode/HarvestCases.cs | 24656060e0d70c75a89c47cd395d04aecd29bcf95f74d76e56fcab003d5c64c3 |

## Limitations and checks not run

MGT-05A remains TEST_ONLY and deliberately supports only the finite harvest fixture, its physical generic-pound descendants, one authored tray profile, and a Fresh-only work adapter. General production preservation, other foods/materials, recipe consumption, and broader storage semantics remain unsupported. The scheduled worker path preserves the shared off-calendar rule. Unity Editor import/compilation, Unity Edit Mode, Play Mode, standalone build, and observed player gameplay were **not run**; Unity remains deferred.

Please review the exact pushed candidate revision for the four criteria above. Confirm acceptance or identify a concrete reproducible blocker within this agreed scope. An attempted contact is not acceptance; MGT-05B remains closed until GPT explicitly signs off.
