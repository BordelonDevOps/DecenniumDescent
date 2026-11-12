# EXP-03 finite supply cache composition proposal

The proposed object is `TEST_ONLY.supply-cache`, the existing authored stationary chest in the accepted ordinary wire95 session. The source/API review should approve its exact access and projection before gameplay edits begin. The accepted thin session is the starting point. [Final session review](../2026-11-12-int03-connected-session/correction/GPT_FINAL_REVIEW.md) · [EXP-03 work item](../2026-11-03-rule-map/RULE_MAP.json)

## Object and source authority

| Fact | Existing selected authority |
| --- | --- |
| Identity, position and custody | `SupplyCacheFixture.CacheId` at cell `(1,2)`, already discovered, stationary, owned by `TEST_ONLY.actor`. The selected cache is unburied, locked and closed. |
| Finite stock | `TEST_ONLY.ready-rations`, the existing two-pound root ration lot. Its inventory owner and custodian are the hero, its world location is the chest and its initial access is Ground. The finite quantity and ancestry come from the existing inventory and work ledgers. |
| Credential | `TEST_ONLY.thieves-tools`, the existing one-pound physical item in the hero's explorer pack. Its linked equipment location must reach the hero through a successful existing portable Retrieve. The selected portable profile has no physical key. |
| Water composition | The record's `TEST_ONLY.actor-skin` reference is historical structure shared with the original cache fixture. The accepted charter profile selects `ReserveWaterStartsCarried`. The initial and continued saves locate this vessel with the hero. The selected cache contains the ration root only. |
| Lock and opening | The ordinary source procedure in `EQUIPMENT_ITEM_PROCEDURES.md` line 53 uses an Action and physical thieves' tools with a DC 15 DEX check. The previously agreed TEST_ONLY exploration procedure pays the current Action and six active seconds per attempt. It resolves the actual RNG and conditions once, leaves failed attempts locked, and uses a separate one-second opening. |
| Physical pickup | The existing inventory resolver checks actual access, amount, hand, capacity, current work and shared-clock boundaries. A successful pickup depletes the root and creates the carried descendant with exact quantity and provenance. The fixture supplies fit for its admitted items. |

[Exact proposal bindings](SOURCE_BINDINGS.json) · [Pinned source snapshots and hashes](../2026-11-04-supply-cache/SOURCE_BINDINGS.json) · [Ordinary lock source](../2026-11-04-supply-cache/sources/EQUIPMENT_ITEM_PROCEDURES.md) · [Previously agreed TEST_ONLY procedure](../../SUPPLY_CACHE_RULE_DECISIONS.md) · [Shared cache resolver](../../../../engine/com.decennium.foundation/Laboratory/Model/SharedSupplyCache.cs) · [Existing regression](../../../../engine/com.decennium.foundation/Tests/EditMode/SupplyCacheCases.cs)

The accepted `ConnectedExpeditionSession.Start()` already selects `new SupplyCacheFixture()` with the portable kit and the carried-water charter option. The portable kit constructor requires physical tools and rejects a key of unsourced mass. Its initialization puts the linked tools in the pack. The cache, attempts, physical equipment, work and inventory already have persisted wire95 representations. The composition proposes preserving this exact fingerprint, selected state and wire layout. [Session factory](../../../../engine/com.decennium.foundation/Laboratory/Model/ConnectedExpeditionSession.cs) · [Portable initialization](../../../../engine/com.decennium.foundation/Laboratory/Model/PortableEquipment.cs) · [Policy constructor](../../../../engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs) · [Cache persistence](../../../../engine/com.decennium.foundation/Runtime/Persistence/SupplyCacheCodec.cs)

## Bounded public API proposal

The player seat can act as the hero on this chest during ordinary exploration. Publish its current lock/open status and the hero's own pending pick only when the hero is stationary and in actual reach of the existing discovered cache. This scope uses the resolver's adjacency, capability, hand and Action checks. The other human seat and automatic defender have no cache authority. The trusted adapter can continue to advance the same shared clock.

Use existing `HandlePortableEquipment` with `Retrieve` for the actual tools, `Interact` for this exact cache and its `PickWithTools`, `Open` and active-attempt `Interrupt` operations, and `HandleInventory` with `Pickup` for the exact ration root. The pickup uses the existing amount, availability, authority and physical-transfer checks. The walkthrough requests the complete two pounds. New unsupported operation/target combinations use the session's generic response. Actual ordinary work, access and custody remain in the core resolver.

The current owned-items projection includes the hero-custodied ration root even while its physical location is the locked cache. Suppress cache-located stock from the ordinary carried/owned item list and expose the root and current available amount only when the cache is open and actually accessible to the hero. A closed, inaccessible or depleted cache has no visible stock IDs or quantities. Once picked up, the actual descendant appears under existing party inventory projection. Keep current authority checks and exact receipt retry semantics. A new stale, forbidden, guessed or unavailable request must never expose hidden lock, stock or resolver facts. [Current public projection](../../../../engine/com.decennium.foundation/Laboratory/Model/ConnectedExpeditionView.cs) · [Inventory access](../../../../engine/com.decennium.foundation/Laboratory/Model/TestOnlyInventoryPolicy.cs) · [Existing grants and claims](../../../../engine/com.decennium.foundation/Laboratory/Model/SharedToolRepair.cs)

Keep unsupported operations explicit in the bounded session. Its approved object uses a tools pick. General key procurement, hidden discovery, generic loot creation, movable chests, digging, marking, trap handling and tactical cache handling are outside this proposed ordinary session composition. EXP-04/05 and MGT-06 retain their later gates.

## Direct prerequisites and connected witness

| Direct prerequisite | Required evidence |
| --- | --- |
| EXP-01 | Real `BeginWorldStep` and paid shared-clock progress to reach, leave and return. Interactions fail when their spatial or stationary conditions are unmet. |
| MGT-01 | Real tools retrieval, successful separate opening, one finite pickup into existing inventory, preserved exact root/descendant ownership and amount, and no regenerated stock. |
| FND-02 | Current scoped authority, unchanged rejection and duplicate behavior, strict external validation on restore, exact pending/completed history, and byte-identical deterministic continuation for the same inputs. |

The connected public walkthrough should start from the actual accepted initial state and retain its prior 165-commit route. After ordinary continuation it should make a paid approach, retrieve the stowed tools, submit paid picks and use their actual outcomes, open separately, collect the finite stock, leave, save/reload, revisit the same open and depleted chest, then continue. Tests should include closed and remote access, wrong-seat and wrong-actor requests, failed paid picking and exact retry, duplicate delivery, a fresh repeat pickup rejection, and visibility parity for inaccessible versus unknown stock. Compare interrupted/restored and uninterrupted canonical bytes. [Read-only feasibility probe](SOURCE_PROBE.md)

Codex proposes this existing object and command boundary for review. The requested decision is approval of the selected facts, public visibility and ordinary command scope, and the acceptance witness before editing gameplay code.
