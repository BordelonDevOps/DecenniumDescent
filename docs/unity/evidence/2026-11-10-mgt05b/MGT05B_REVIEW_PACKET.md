# MGT-05B implementation review packet — schema75 TEST_ONLY

**Status: implementation review pending.** This packet covers Engine implementation commit `4d11fdceb25fb6a9f86b419484f3cca70a615211`, based on `e4c8e540ed70081f0ee0e3b4d516261d5e6a9d72`. GPT authorized implementation under the bounded schema75 contract but has not yet reviewed this implementation evidence or accepted MGT-05B. Do not close the module or start the next dependency until GPT reviews this packet and concrete blockers are resolved.

The separate MGT-05A gate is closed: GPT accepted corrected commit `1e0bbc1168808686cec20a1d52ffa33284550646` with “No concrete acceptance blocker remains within the agreed MGT-05A scope.” The pasted rejection concerns superseded commit `300fa051bb40ceb6f535b20bcc58bde0e78d0729`.

## Agreed scope and source requirements

This increment implements one closed-container preservation treatment for a harvested `generic.ordinary-fish-meat` lot, only in schema75 `TEST_ONLY` content. The pinned rule source is `DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md`, revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `b8adb3ac6eb51f333fdb8f2d68ecc7e9c6511e7ee3aded1bfe54cd4728c93479`, “Preservation and spoilage,” source lines 152–166. The pinned candidate fixture manifest supplies fixture bindings, not additional rule authority.

The approved bounded behavior is: treat only Fresh or Degraded material; reject Spoiled material and a job that cannot finish before its spoilage boundary; cap one treated lot at 10 lb; reserve one actual 0.5 lb supply lot; perform 1,800 active seconds using the authored Cooking/Wisdom and Cook’s-utensils fixture; make one DC 10 check through shared check and RNG authorities; on success seal the fitting vessel and protect the material from further natural aging for 24 elapsed hours; on failure spend the consumed supply but grant no protection. Derived state continues to use the original harvest origin and shared RuleClock. Schema74 remains on its established codec and behavior path.

GPT authorized this implementation under the owner’s standing engine authorization. That authorization is not implementation acceptance. The actual contract and clarification are recorded in [GPT_REVIEW.md](GPT_REVIEW.md), the source pin and contract in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json), and the implementation/source-hash bindings in [MGT05B_VALIDATION_BINDINGS.json](MGT05B_VALIDATION_BINDINGS.json).

## Responsibilities and authoritative records

- `HarvestPreservationRules` derives natural age and active protection from the extracted harvest record, inventory ancestry, the physical `WorkLedger` lot and linked portable item, treatment outcome history, and `RuleClock`. It does not write a second freshness clock, value, mass, or inventory ledger.
- `HarvestPreservationTreatmentAttemptRecord` binds the worker, selected Cooking skill, target descendant, vessel, tool, supply, reservations, active work, completion check, and sealing time. `ActiveWorkProgress`, `WorkLedger`, `WorkerIntervals`, shared command receipts, shared deterministic dice, and `SnapshotCodec` remain authoritative.
- The schema75 codec appends the TEST_ONLY attempt history. Nonempty treatment history is rejected below schema75; earlier schema branches remain in place.
- The treatment fixture is one authored actor, material, vessel, tool, supply lot, and check binding. It does not create production food or recipe authority.

## Runnable acceptance scenario

The connected case is `mgt05b_closed_vessel_treatment_lineage_save_restore_and_replay` in [HarvestPreservationTreatmentCases.cs](../../../../engine/com.decennium.foundation/Tests/EditMode/HarvestPreservationTreatmentCases.cs). It performs the existing finite harvest, takes an actual descendant, retrieves and stows that lot and the actual supply into the authored treatment vessel, verifies the descendant’s source lineage and physical parent, starts the scheduled treatment, saves/restores at half work, completes from the same command and RNG history on independent replay runs, confirms consumption/sealing/protection, carries the intact closed vessel, advances exactly to and beyond the 24-hour expiry, verifies the untreated sibling ages independently, then retrieves and portions the protected descendant while conserving mass and inherited age history.

The source and test assertions that establish physical transfer and storage include:

```csharp
PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,treatedLotId,
    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId));
PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,treatedLotId,
    Mgt05bVessel,HandlingKind.Stow,TestOnlyPolicy.ActorId));
PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,Mgt05bSupply,
    Mgt05bVessel,HandlingKind.Stow,TestOnlyPolicy.ActorId));
```

The follow-up assertions verify the harvested child’s parent, both physical parents inside the vessel, and its derived Fresh state before work. At completion they verify the exact target amount is released unconsumed, the 0.5 lb supply is consumed once, the vessel seals, and the successful check is recorded. Whole-vessel movement preserves protection; the exact expiry ends protection without resetting unprotected age; the untreated sibling continues aging; and post-expiry portioning conserves `WorkLedger` mass and inherits the same derived age.

The test uses `SnapshotCodec` byte arrays for save/restore and compares canonical snapshots across independently initialized runs and one-piece versus split time advancement. It does not emit a standalone `.ddsave` file. Focused code excerpts and the complete code diff are in [MGT05B_CODE_DIFF.patch](MGT05B_CODE_DIFF.patch); the exact changed-file list is [CHANGED_FILES.txt](CHANGED_FILES.txt).

Two additional focused cases cover failure settlement and Degraded treatment/spoilage boundaries:

- `mgt05b_failed_treatment_spends_supply_once_without_protection`
- `mgt05b_degraded_treatment_retains_half_value_and_spoilage_deadlines_reject`

## Retained validation

- Full C# 9 warnings-as-errors regression and compile: **PASS, 1,324/1,324**, zero failures, 282 source hashes. Core, Persistence, LabModel, and HeadlessTests assemblies are retained in [full-suite](full-suite/); the complete source-hash-bound report is [results.json](full-suite/results.json). All three MGT-05B cases pass in this full run.
- Focused connected, Degraded, and failure cases: **PASS, 1/1 each**, each retained report binds 282 sources under [focused](focused/).
- Static package validation: **PASS, 18/18**, 308 package assets, 308 unique GUIDs, and 605 source-hash entries; see [the passing report](package-validation/passed/results.json).
- A first static run failed because the two new package source files lacked adjacent `.meta` files. The [retained failure report](package-validation/failed-metadata/results.json) records that cause. Standard unique MonoImporter sidecars were added, then the package check passed.
- The implementation commit passes `git show --check`; the review packet, documentation, and retained reports pass `git diff --check` when the raw patch artifact is excluded. The `.patch` file preserves unified-diff context-prefix spaces verbatim, which a generic text whitespace check reports as trailing spaces. All 23 changed C# files match the full-suite report hashes (**23/23**); per-file bindings are listed in [MGT05B_VALIDATION_BINDINGS.json](MGT05B_VALIDATION_BINDINGS.json).

Unity import/compilation, Unity Edit Mode, Play Mode, player build, and observed gameplay were **not run**. Unity gameplay integration remains deferred.

## Remaining limitations

This is not the complete MGT-05 preservation system. The implementation supports one `TEST_ONLY` harvested material and authored treatment fixture. It does not add an exposure-event system, treatment interruption/cancellation settlement, re-treatment, other materials, production recipes or edible output, currency debit for owned stock, assistants, a general catalog, or generalized container fitting. Tactical entry is gated while this bounded treatment is active. Broader production authority and Unity presentation remain unsupported.

## Review requested

Please review the exact code commit, package diff, source-bound reports, changed-file list, and source/test excerpts above. Confirm whether the implementation satisfies the agreed MGT-05B scope and acceptance criteria. Separate concrete blockers from optional hardening; do not broaden the module contract. If a blocker exists, identify the precise source rule, record/handler, failing assertion, and smallest correction. Until this review is accepted, the implementation remains open and the next module does not begin.
