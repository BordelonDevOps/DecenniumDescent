# MGT-05C — preservation exposure and controlled opening source/API review

**Status:** Source/API review draft for Codex/GPT alignment. No MGT-05C gameplay code is authorized by this document alone, and no implementation has started. MGT-05A and bounded MGT-05B remain accepted. The next contract must be agreed before implementation begins under the owner's standing engine-development authorization.

## GPT's next-step direction

After accepting MGT-05B, GPT directed Codex to “begin the next bounded MGT-05 source/API review: preservation exposure and controlled opening, provisionally MGT-05C.” It named the next deliverable as “the exposure/opening contract—not another MGT-05B correction or optional test-expansion round.” GPT also directed that this slice reuse the current TEST_ONLY material and vessel, separate a qualifying clean opening from actual protection-ending events, and avoid re-treatment, broader materials, production food/recipes, generalized repackaging, and Unity presentation.

This packet records the source/API facts and asks for agreement on the narrow unresolved contract. It does not reopen MGT-05A or MGT-05B.

## Pinned rule authority

The rule source is `DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md`, pinned at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `b8adb3ac6eb51f333fdb8f2d68ecc7e9c6511e7ee3aded1bfe54cd4728c93479`, section “Preservation and spoilage” (source line 152; the controlling exposure sentence is line 164).

The source establishes these requirements:

- Treatment creates 24 elapsed hours of protection without restoring Fresh condition or removing already accrued unprotected age.
- Actual container breach, contamination, or incompatible heat ends protection.
- Merely opening to portion with clean tools for less than one minute does not end protection.
- Dividing, trading, repackaging, recovering, and reharvesting cannot reset biological age.

It does not spell out whether a clean opening that lasts exactly one minute ends protection, when a still-open container loses protection after the brief-opening exception no longer applies, or whether a removed portion keeps the rest of the container's active protection. Those interpretations must be agreed explicitly.

The pinned candidate data is fixture material only. It does not provide a cleanliness state, breach/contamination event source, or a production container model.

## Confirmed current C# authorities and API boundary

The findings below were inspected in the current pushed Engine revision, code commit `9c0a4e92b7f2af8c62c07326934fad7524f64f9c`, with evidence/docs at `6573b7882ee2f9c6323a2de96d95100820e80629`.

| Responsibility | Existing authority and observed behavior |
| --- | --- |
| Biological origin and derived age | `HarvestMaterialUnitRecord.OriginAt` and `PreservationIntervalSeconds`; `HarvestPreservationRules.TryProjectAt` derives age from the shared `RuleClock`, lineage, and successful treatment history. No mutable current-age field exists. |
| Successful treatment and initial protected interval | `HarvestPreservationTreatmentAttemptRecord` binds the exact treated inventory lot and container, and records `CompletedAt`/`SealedAt`. Schema75 derives the 24-hour interval from this immutable history. |
| Physical contents and custody | `PortableEquipmentRecord` owns current `Open`, `ParentId`, placement, owner and custodian. `PortableHandlingRecord` is append-only and records the actor, operation, revision, and `StartedAt`/`EndedAt`. It has no clean-tool, contamination, breach, or heat fact. |
| Open/close commands | `SharedPortableEquipment` already handles `OpenPortableContainer` and `ClosePortableContainer`. In exploration, the normal operation advances shared time by one second and records the handling interval; in tactical mode it spends the existing interaction allowance and marks the record tactical. Opening/closing currently records only ordinary handling. |
| Protection-time restrictions | `HarvestPreservationTreatmentPortableHandlingFailure` rejects operations affecting protected contents, except intact whole-vessel movement. Opening, content removal, and other active-protection changes therefore remain blocked in schema75. |
| Portioning and quantity | `OrdinaryInventory.Descendant` conserves the `WorkLedger` amount and creates a child `InventoryLotRecord` with the original owner, parent ID, and `CreatedAt = RuleClock`; it registers the physical item at the source ledger lot's location/custodian. `TestOnlyInventoryPolicy` currently rejects portioning a lot while `HarvestPreservationRules.IsProtectedAt` is true. A child can be created while still inside its parent vessel, so `CreatedAt` alone does not establish when it physically leaves protected storage. |
| Save/replay boundary | `SnapshotCodec` appends the treatment history for schema75 and admits explicit schema versions. Schema75 policy/validation is specifically bounded to its current TEST_ONLY profile. Any new durable exposure facts need an explicit compatible version/profile so schemas74 and75 retain their existing bytes, fingerprint, validation and behavior. |

### Concrete seam between accepted MGT-05B and proposed MGT-05C

The MGT-05B accepted projection clips an ancestor treatment interval at the first descendant's `CreatedAt`; that correctly prevents a branch that left treated material from later inheriting protection it did not experience. MGT-05B also rejects portioning while protection is active. MGT-05C proposes allowing a portion during a qualifying clean opening. The existing `PortionInventory` path creates that child at the source lot's current location/custodian, and a later portable retrieval records the actual move out of the vessel. Therefore child creation and physical removal can be different events. If MGT-05C treats creation as the separation point, a child still physically inside the treated vessel could stop receiving protection too early; if it treats every descendant as protected until the container's expiry, a removed child could receive protection it no longer physically experiences.

**Smallest source-aligned proposal for GPT to accept or revise:** allow one portion during a qualifying clean opening; keep that child in the same vessel location until ordinary retrieval; derive its protection only while its physical item remains inside the treated vessel; end future protection for that child at the successful retrieval's recorded completion time, retaining all protected time already experienced and the original biological origin. Continue using `PortableHandlingRecord`/current ancestry to identify the physical move; do not add a second location or age ledger. This proposal is not adopted. The pinned rule does not explicitly define whether the remaining contents stay protected through the qualifying opening, whether a just-created child remains protected while still in the vessel, or the removed child's exact protection cutoff. These are the central MGT-05C rule gaps and are asked below.

### Relevant source links

- [Pinned preservation rule](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md#L164)
- [Portable records](https://github.com/BordelonDevOps/DecenniumDescent/blob/9c0a4e92b7f2af8c62c07326934fad7524f64f9c/engine/com.decennium.foundation/Runtime/Core/PortableEquipmentRecords.cs#L11)
- [Portable open/close handling](https://github.com/BordelonDevOps/DecenniumDescent/blob/9c0a4e92b7f2af8c62c07326934fad7524f64f9c/engine/com.decennium.foundation/Laboratory/Model/SharedPortableEquipment.cs#L209)
- [Active-treatment handling gate](https://github.com/BordelonDevOps/DecenniumDescent/blob/9c0a4e92b7f2af8c62c07326934fad7524f64f9c/engine/com.decennium.foundation/Laboratory/Model/SharedHarvestPreservationTreatment.cs#L114)
- [Derived protection and lineage projection](https://github.com/BordelonDevOps/DecenniumDescent/blob/9c0a4e92b7f2af8c62c07326934fad7524f64f9c/engine/com.decennium.foundation/Runtime/Core/HarvestPreservationRecords.cs#L54)
- [Inventory portioning authority](https://github.com/BordelonDevOps/DecenniumDescent/blob/9c0a4e92b7f2af8c62c07326934fad7524f64f9c/engine/com.decennium.foundation/Laboratory/Model/OrdinaryInventory.cs#L27)
- [Schema75 treatment codec](https://github.com/BordelonDevOps/DecenniumDescent/blob/9c0a4e92b7f2af8c62c07326934fad7524f64f9c/engine/com.decennium.foundation/Runtime/Persistence/HarvestPreservationTreatmentCodec.cs#L1)

## Proposed bounded responsibilities

Subject to GPT agreement, MGT-05C would:

1. Admit a controlled opening of the existing successfully treated TEST_ONLY fish lot's vessel during its derived protection interval.
2. Distinguish a qualifying brief opening with the required clean-tool fact from actual breach, contamination, or incompatible-heat events. A true protection-ending fact ends protection at its recorded shared-clock time without a one-minute grace period.
3. Permit one legal, quantity-conserving portion operation during the qualifying opening and derive which physical inventory branches remain protected from actual vessel placement and history, while preserving `OriginAt` and unprotected age.
4. Persist only the minimum immutable event evidence needed for clean-tool qualification and actual protection-ending causes. Continue deriving current condition/protection from original treatment, exposure, inventory, and handling history; do not add mutable age, a second expiry timer, or duplicate inventory.
5. Preserve schema74 and schema75 bytes, profile fingerprints, validation, and runtime behavior.

## Candidate authority model for review (not yet adopted)

The existing portable handling journal can remain authoritative for open/close operations and their actor, command revision, and shared-clock timestamps. Existing `InventoryLotRecord` ancestry and the portable placement/handling history can remain authoritative for portion identity, quantity, and actual movement into or out of the vessel. `WorkLedger`, the command/receipt transaction, and `RuleClock` remain authoritative for stock, idempotency, and ordering.

Because no current record states whether tools were clean or records an actual preservation-ending event, the smallest candidate is a schema76 TEST_ONLY append-only exposure-event record referencing the existing treatment attempt and vessel. Event kinds and fields would be limited to the source facts required by the agreed slice; existing open/close and portion records should not be duplicated. Schema76 would have its own explicit TEST_ONLY selection/fingerprint and codec section, while the schema75 path remains unchanged. The exact record shape and whether a new schema is necessary are questions for GPT, not settled decisions.

## Specific contract gaps for Codex/GPT to resolve

1. **One-minute boundary:** The pinned exception applies to an opening lasting *less than* one minute. Does a still-open clean vessel lose protection at exactly `openedAt + 60 seconds`, at close once the duration is at least 60 seconds, or under another source-faithful event rule? Confirm that actual breach, contamination, and incompatible heat end protection immediately at their actual event time even if the opening is brief.
2. **Portion protection and the MGT-05B lineage seam:** Confirm or revise the explicitly labeled proposal above: the clean opening leaves the remaining contents protected; a child portion created in-place remains protected only while physically contained in the treated vessel; and a successful retrieval ends that child's future protection at its recorded completion time while preserving accrued protection and original age. This differs from using `CreatedAt` as the cutoff, because the existing portion command leaves the child at the source lot's physical location and retrieval is a separate recorded move. State whether the strict one-minute clean-opening exception protects the remaining vessel contents only, and whether any portion already removed receives any remaining protection.
3. **Clean-tool evidence:** The fixture has a physical Cook's-utensils item but no cleanliness state. Is an explicit, per-opening TEST_ONLY clean-tool fixture fact bound to that physical item sufficient for this bounded slice? Do not infer cleanliness from ownership or presence alone.
4. **Protection-ending event authority:** No current general record supplies breach, contamination, or incompatible heat. Is an explicit typed schema76 TEST_ONLY event, created only from an admitted concrete scenario, the smallest sufficient representation? It must remain distinct from ordinary `Open` and `Close`; an opening alone must not fabricate contamination.
5. **Chronology and tactical scope:** Use the shared `RuleClock`, persisted command revision/receipt order, and the existing half-open treatment deadline so expiry at `CompletedAt + 86,400` is not extended by a simultaneous handling event. Confirm whether the first slice should support protected opening in both exploration and tactical handling, or keep the connected witness in exploration while preserving existing tactical behavior until separately covered.

These are bounded source/API questions. No owner ruling is needed if Codex and GPT agree. Do not infer an exposure event from the `Open` boolean alone.

## Runnable acceptance scenario after contract agreement

Use the accepted MGT-05B TEST_ONLY harvested fish and sealed vessel; do not author new production material or a new container catalogue.

- Starting from a successful treatment, save and restore during protected storage. Open with the agreed clean-tool fact, create one legal portion while preserving total `WorkLedger` mass and the original harvest lineage, retrieve it if the agreed operation includes removal, and close before the agreed strict sub-minute deadline. Verify exact opening duration, both branches' derived age/protection, physical placement/custody, no unprotected-age reset, deterministic replay, and identical encoded state after restore.
- From a separate deterministic branch, record one actual protection-ending event while the treatment interval is active. Verify no protection loss before its event timestamp, immediate loss at that timestamp, correct continued aging from accumulated unprotected age, unchanged original origin, and once-only behavior on duplicate command submission. Save/restore and compare whole versus partitioned clock advances.
- Cover the exact one-minute boundary and the treatment's exact 24-hour endpoint according to the agreed ordering. An actual breach/contamination/heat event must not receive the brief-opening exception.
- Retain schema74 and schema75 roundtrip/replay witnesses and prove the new event record is unavailable to those profiles.

## Deferred scope

Re-treatment, interruption/cancellation settlement, additional materials, new container catalogues, general environmental simulation, broad repackaging, production recipes/food, and Unity presentation remain outside this increment. No code or validation has been run for MGT-05C; this document is the source/API review deliverable.
