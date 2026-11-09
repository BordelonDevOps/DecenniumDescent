# MGT-01 physical storage and transfer contract

**Status:** implemented on `Engine` as additive schema71 TEST_ONLY content. GPT reviewed exact commit `bb4832e23b26a3f71b41bc14be627e22c390ad17` and held acceptance on two portable-handling defects plus missing authentic pre-change schema70 evidence. Codex has corrected those points and rerun validation; GPT’s review of the corrected exact commit is pending. This remains a bounded increment, not production content authority or engine completion.

## Map position and goal

The current implementation map row is **MGT-01 — Inventory, equipment, currency, reservations and custody**, at `IMPLEMENTATION_TRACE.md` around line 661. The unfinished behavior includes general nested storage, transfers and access. This increment selects only physical container storage and physical transfers. Currency, purchases and the remaining MGT-01 catalog stay out of scope.

The accepted schema70 Temporary Camp is the next real storage destination. This closes the current gap between constructing a camp with certified capacity and using that capacity to store expedition goods. It is an existing mapped dependency before crafting and Haven settlement/return preparation, not a new roadmap item. The owner’s full-engine objective remains the connected exploration → encounter → acquire → manage → prepare → continue loop.

## Pinned source requirements

All source references below use ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

| Source | Source-backed behavior |
| --- | --- |
| `EQUIPMENT_ACQUISITION_PLAYTEST.md` (blob `789e905552aba2ee9a4bbad1ae73aa314b77af10`), “Record possessions and permissions” and “Carrying and containers” | Preserve physical identity, quantity, actual owner/custodian, location, known size/contents and source exceptions. Unknown catalog facts stay null. Enforce known weight and volume independently, with actual shape, closure and access. A container’s capacity creates no contents. |
| `BODY_EQUIPMENT_PLAYTEST.md` (blob `60f81c5706857c5528d9d19e3da9ac15dcd7fb85`), “Carrying and Load” | Pounds and Load are distinct. Container and contents count once each, including through nested containers. Source-specific carrying and Burdened limits remain active. |
| `expedition/EXPEDITION_PLAYER_BOOK.md` (blob `466871fc128dc5f06043a874da2b9c1d94ed80a5`), FL-05 and FL-07 | Repacking does not renew freshness or duplicate water mass. A completed Temporary Camp provides 20 Load / 200 lb / 20 ft³ storage; an unbuilt bivouac has no certified storage. |

The source does not supply packed volumes or fit facts for every ordinary physical profile. Do not infer cubic feet from pounds or treat missing catalog fields as zero. This increment admits only explicitly authored, fingerprinted TEST_ONLY physical profiles; unknown or incompatible profiles cannot be placed in profile-based storage.

## Authoritative records and implementation contract

Keep the installed fitting-pack item as the physical camp-storage root. Preserve its item ID, lot link, owner, actor custodian, Ground placement and installation claim. Deposited goods use the existing `PortableEquipmentRecord.ParentId` containment edge. Quantities, ancestry, freshness and ownership remain in existing `ResourceLot`, `InventoryLotRecord`, vessel-content and reservation records. Do not add another inventory, camp-content ledger or mutable capacity balance.

Add immutable Core-readable storage profile facts in an additive snapshot branch so Core snapshot validation and `SnapshotCodec` can validate physical fit and volume without relying on a LabModel-only policy. The selected TEST_ONLY policy must verify that the persisted profile facts exactly match its authored definitions and content fingerprint. Profile facts are keyed by physical `ProfileId`, bounded to selected profiles, and carry explicit packed-volume and compatibility facts. Existing `FitRuleId` / `FitMemberIds` exact-member behavior remains unchanged for historical container profiles. An unknown profile remains unsupported.

One shared storage assessment must be used by query, execution and snapshot validation. For the new profile path, enforce direct-child profile compatibility and packed volume; nested containers contribute their exterior packed volume to their parent, while their internal contents are checked against their own capacities. Enforce mass across the full physical subtree and count Load, pounds and contents exactly once. The Temporary Camp’s additional Load limit and availability derive from `TemporaryCampConstructionValidation.HasTemporaryCamp` / `StorageCapacity`; the pack’s stored capacity values alone do not authorize storage before successful installation.

Reuse `RuleClock`, existing action/interaction costs, `WorkLedger` reservations, ordinary inventory portioning, portable handling records, hand/condition/reach checks, actual water-vessel contents, command receipts, detached transactions and existing persistence. Ordinary opening remains a separate supported operation; camp construction does not silently open its storage. Installed fixtures cannot be picked up, handed over, removed or relocated. A stationary open/close must not release an installation claim; do not exempt unrelated work reservations that require access. Stored goods retain ordinary claims and are inaccessible while their container is closed.

Custody remains an actor ID. Deposit changes the item subtree’s custodian to the destination container’s actor custodian while preserving every item owner; retrieval changes the subtree to the retrieving actor. Link synchronization updates the existing lots, vessels and equipment atomically. Access still requires authority over relevant owners, actual physical reach and an open container. A camp name grants no ownership, consent or remote access. Existing handover consent stays enforced through `Authority.ConsentsToHandover`.

## Bounded responsibilities and exclusions

Implement reusable physical deposit, retrieval and willing handover for admitted whole items/containers and already-supported divisible food portions. Preserve actual quantity, identity, ancestry, owner, freshness, vessel contents, custody and reservations. Enforce nested containment, installation protection, actor carrying burden, camp Load/pound/volume limits and each portable container’s authored pound/volume capacity. Query and execution must agree on admissibility and cost. Storage itself uses no RNG.

This increment does not implement currency, purchases, an arbitrary equipment catalog, automatic stock creation, new splitting semantics, general food density, unmodeled physical dimensions, magical storage, camp upgrades/dismantling, autonomous hauling, new spoilage, new production-site authority or Unity presentation. Existing intake and work handlers continue to own consumption and labor outcomes. Unknown source profiles, dimensions and shape remain explicitly unsupported.

## Runnable acceptance contract

Run a connected scenario through existing authorities:

1. Explore by the existing route, resolve an existing supported encounter, and acquire actual finite food/water supplies through the existing cache path.
2. Complete the accepted schema70 Temporary Camp task with its actual tent and fitting-pack lots, then open the installed fitting-pack root using the existing ordinary handling operation.
3. From an adjacent cell, open and close the stationary installed storage with a companion; verify its ground coordinates, installation claim and synchronized lot location do not change. Deposit an acquired food lot and a filled physical waterskin into camp storage; create and physically transfer an already-authorized food portion. Exercise the same destination resolver with an ordinary portable container using a distinct selected profile.
4. Save while goods are nested and compatible companion work is active. Restore, continue with an authorized actor, retrieve and hand over actual provisions, consume through the existing intake procedure, and continue exploration carrying only withdrawn goods.
5. Pick up the ordinary crate, hand it to the companion, save/restore, and drop it. Verify query/execution agreement, nested contents, preserved ownership, synchronized custody/location and burden. Compare identical restored command histories byte-for-byte and compare uninterrupted versus split shared-clock advancement semantically, including work and RNG outcomes. Verify unchanged ownership/ancestry/freshness, exact vessel contents and water mass, synchronized location/custody links, correct carrying burden and capacity, unchanged installed fixtures, and duplicate-command idempotence.
6. Load the authentic paused schema70 save retained before the schema71 storage change; verify current-code decode/re-encode/restore and deterministic resume through installation.

Required rejection cases leave state, clock, receipts, reservations and RNG unchanged: storage before camp completion; closed or out-of-reach containers; unknown/incompatible profiles; volume, pounds or Load overflow independently; containment cycles; reserved item/subtree movement; and installed-root pickup/handover/removal. Preserve an authentic schema70 save roundtrip and deterministic continuation under its prior profile.

## Validation and review gates

- C# 9 warnings-as-errors compilation and the relevant complete headless suite.
- Core/Persistence/LabModel standalone compile plus static package validation.
- Source/profile bindings, exact profile fingerprints, source hashes, retained connected saves and all failed attempts.
- Historical schema70 roundtrip and replay under the historical content profile; schema71 roundtrip and connected replay under the new TEST_ONLY profile.
- Do not report Unity import, Editor tests, Play Mode, build or observed player behavior; those remain deferred.

Passing case counts do not establish engine completion. Review the exact gameplay commit and retained evidence with GPT before beginning a successor dependency.

## Codex/GPT consensus record — 2026-11-09

GPT selected MGT-01 as the next mapped dependency after accepting schema70 commit `2553c738ed17262b222d296458e6694ed1304ce8`. It explicitly said this is an existing mapped dependency, downstream of the prior command/persistence/source-qualified foundations, and that its order does not require completing every MGT-03 camp subfeature.

Codex checked `engine/AGENTS.md`, the current Engine branch at `2049d2c4`, the MGT-01 map row and recommended build order, the pinned equipment/body/expedition rules, and the current portable records, validator, handling resolver, lot synchronization, camp construction/capacity and codec paths. Codex found the concrete fit/volume and actor-custody integration gap described above and agreed with GPT’s bounded MGT-01 selection.

GPT’s actual design response was:

> Yes—keep the installed fitting-pack record as the physical storage root and use a fingerprinted, explicitly selected fit/packed-volume profile table. This is a resolvable integration gap, not a source conflict or a reason to reopen schema70 acceptance.
>
> Preserve the existing physical identity. Keep the fitting pack’s item ID, linked lot, owner, actor custodian, Ground placement and installation claim. Stored items use its existing ParentId relationship; their quantities remain in the existing lots/vessels. No second camp-content ledger is needed. Storage admission must resolve the root’s actual installation and call HasTemporaryCamp / StorageCapacity. The printed 200 lb / 20 ft³ fields alone must not authorize storage before construction completes. Enforce the 20 Load, 200 lb and 20 ft³ limits.
>
> Introduce an explicit alternative fit mechanism, preserving the old one. The selected profile table can be keyed by physical ProfileId, with bounded admissions, packed-volume facts and any required shape/closure compatibility. Unknown profiles or insufficient facts reject. Keep legacy FitRuleId / FitMemberIds semantics unchanged. Do not put profile IDs into a field that currently means physical item IDs, manufacture dummy members, or append every deposited item to a permissive membership list. One shared destination assessment must serve query, execution and validation. The new profile resolves compatibility from declared facts; historical profiles continue using their existing exact-member rules.
>
> Make those definitions available during codec validation. SnapshotCodec calls Core snapshot validation independently of the LabModel policy. Given that interface, the straightforward solution is Core-readable immutable storage-profile facts in the new additive snapshot branch, bound into the selected content fingerprint. Core validates containment and capacities from those facts; policy restore verifies their exact agreement with the selected authored definitions. This adds content facts, not mutable inventory or capacity totals. Do not simply skip fit validation until policy restore.
>
> Retain actor custody and normalize it on physical transfer. Deposit assigns the item and its descendants to the destination’s actor custodian, preserving each owner. Retrieval assigns that subtree to the retrieving actor. Synchronize the existing inventory/vessel/tool links atomically. Require authorized access; custody normalization grants no permission by itself. A Ground root and its descendants remain excluded from carried burden even though an actor remains their custodian. Do not introduce a fictitious “camp actor” or use the site ID as custodian.
>
> Keep installation protection operation-specific. Open=false should require the ordinary supported opening operation; installation must not silently open storage. Pickup, handover, removal and relocation of the installed root remain prohibited. Depositing or retrieving an unrelated, unreserved child does not release the root’s installation claim. For this selected storage profile, the exact durable anchoring claim should prevent relocation, not stationary opening/closing. Preserve rejection for any other claim whose work requires continued access. Do not broadly exempt installed containers from reservation checks.
>
> Packed volume remains explicitly authored TEST_ONLY data. Nested containers contribute their exterior packed volume to their parent; their internal contents are checked against their own capacity. Mass and Load still count every physical item exactly once.
>
> The minimum regression is: construct the camp, open the same fitting-pack root, have an authorized companion deposit a real filled vessel, save/restore, and retrieve it through another authorized actor. Assert exact parent/custody/link synchronization, unchanged ownership and contents, correct burden, unchanged installation claims, duplicate idempotence and deterministic replay. In branches, reject pre-installation storage, closed access, unknown fit, independent capacity overflow, reserved-child movement and installed-root pickup without mutation. Exercise the same resolver with an ordinary portable destination and retain the historical-profile compatibility test.
>
> Consensus reached on this representation. The table, custody transition and validation integration are implementation prerequisites for the new module; no owner escalation is needed.

GPT inspected the exact current construction, portable records/resolver, link synchronization, capacity derivation, Simulation validation and codec paths at `2049d2c4`. It made no repository changes and ran no compilation or tests. This record reflects its actual design response, not an independent verification of implementation.

## GPT Load clarification — 2026-11-09

In the follow-up source-bound review, GPT confirmed that the pinned BODY_EQUIPMENT_PLAYTEST rule gives printed Load precedence; only when printed Load is absent and physical weight is known does this prototype use known pounds divided by ten. Unknown pounds and Load remain unknown, and the two quantities remain distinct. Existing `PlaytestCarrying.Total` already applies this fallback for ordinary carried burden. The new Core helper is used for storage capacity checks; Core remains independent of LabModel.

GPT’s required arithmetic regression was two pounds of food plus a full waterskin with one-pound tare and four pints of water: seven pounds total, and 0.7 Load when no separate Load is printed. Each physical item and contained liquid counts once. The Temporary Camp’s three limits are checked independently at 20 Load, 200 lb and 20 ft³. The connected case includes that exact total, exact Load-20 acceptance, an above-Load rejection with weight and volume still fitting, and independent weight/volume overflow cases.

## Implementation status — 2026-11-09

Schema71 adds immutable Core-readable `PortableStorageProfileRecord` facts to `Snapshot`, validates and serializes them in the additive persistence branch, and binds the exact selected TEST_ONLY definitions into the policy fingerprint. The shared profile resolver handles explicit compatibility, quantity-based packed volume, full nested subtree pounds/Load, per-container volume and the installed camp’s derived Load/weight/volume limits. Unknown dimensions remain unsupported. Legacy `FitRuleId`/`FitMemberIds` stowing remains on its prior exact-member path.

The LabModel uses the installed fitting-pack record as the camp root and the ordinary portable record as a second destination. Existing parent links, lots, vessels, vessel contents, owner/custodian facts, reservations, handling costs, query/execution transaction, command receipts and `RuleClock` remain authoritative. Deposits update the destination actor’s custody through the item subtree and synchronize existing links; they preserve owner, freshness and provenance. The installed storage root remains anchored while stationarily openable/closable; its durable successful construction claim is the only claim exempted for close. Other installation claims and active work claims retain their prior rejection behavior. Schemas 70 and earlier retain their codec branches.

The connected acceptance covers route exploration, the existing tactical encounter, actual cache acquisition, Temporary Camp construction, stationary adjacent Open/Close, filled-water and food deposits, portioning, retrieval and handover, ordinary crate pickup/handover/save/restore/drop, query/execution agreement, duplicate idempotence, uninstalled/closed/out-of-reach/incompatible rejection, containment/capacity validation, authentic pre-change schema70 decode/re-encode/restore and deterministic continuation, schema71 save/restore, and restored branch replay through intake and route continuation. A separate active-fill comparison checks uninterrupted 60 seconds against a 30-second save/restore plus 30 seconds, including remaining reservation, work-lot settlement, output identity, clock and RNG state.

Codex’s exact commit, changed-file list, reports, source hashes, scenario saves, failed-suite reproductions and non-performed Unity checks are indexed in [MGT-01 evidence](evidence/2026-11-09-mgt01/README.md). GPT held the initial implementation commit; its actual response and the validated corrections are recorded in [GPT_REVIEW.md](evidence/2026-11-09-mgt01/GPT_REVIEW.md). The corrected exact commit awaits GPT’s re-review. No successor dependency begins before acceptance.
