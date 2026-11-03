# Inventory source guidance

Chat: https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206

GPT response `010b31cb-8fe4-5038-bda6-491583d68ccd`, captured 2026-11-03. GPT's source findings are guidance, not runtime certification; its three recommendations were subsequently adopted by the owner, as recorded in ../../INVENTORY_RULE_DECISIONS.md. That later receipt, not GPT's recommendation, supplies prototype authority. Formatting whitespace is normalized.

**The sources support the custody and nutrition ledgers, but leave ordinary handling classification and intake timing incomplete.** I checked the files at `377db0e7`; the findings below distinguish reviewed authored PLAYTEST rules from new proposals. I have not rerun your reported tests.

**1. Transfer, pickup and drop**

| Existing source | Established rule | Remaining gap |
|---|---|---|
| [COMBAT_ACTION_PLAYTEST — Encounter and action resources](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#encounter-and-action-resources) | One ordinary free object interaction per turn. A second interaction or Action-time activation uses an Action. | No complete classification of ordinary pickup, voluntary drop, retrieval, stowing and handover. |
| [COMBAT_ACTION_PLAYTEST — Secure Cargo](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#L95) | An **Action** performs one legal attach, lift, transfer or protective operation on an actual cargo unit/bundle with an assigned Extraction Class. Capacity, access, hands and checks still apply. | This does not establish that every handheld object interaction is Secure Cargo. |
| [Expedition TR-12](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#L1065) | Calm handling of one actual fitting bundle up to **50 lb takes one active minute**. Heavier indivisible objects require sufficient support and a declared positive duration. Existing shorter access procedures remain applicable. Tactical handling uses Secure Cargo or another appropriate Action. | The shorter ordinary-access procedure is not completed here. |
| [Expedition FL-05](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-05) | Filling one skin/flask or issuing one standard Supply basket takes **one active minute per worker**. A sealed prepacked handover uses actual item-access time. | No numeric default for that prepacked handover. |

Two important limits:

- Releasing **one grip** on a two-handed weapon costs no Action under the equipment guide. That does **not** establish free dropping of the whole weapon.
- The adopted six-second **round** does not assign six seconds to every exploration Action, or add six seconds for every tactical Action.

Ownership and custody are already distinct. [BODY_EQUIPMENT — What melds](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md#what-melds) explicitly preserves the lender’s ownership of borrowed equipment, requires actual location/custody and prohibits access or consumption through melded storage.

**2. Physical stacks, reservations and freshness**

There are useful existing invariants, but I found no general split/merge command contract:

- [Gathering tools — Preserve the history](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md#preserve-the-history) explicitly permits **original identities or recorded descendant portions**. Parent and descendants cannot both retain the full quantity. Origin restrictions, custody history, condition and material clocks survive transfer.
- [Crafting — Preservation and spoilage](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md#preservation-and-spoilage) expressly prohibits age resets through dividing, trading or repackaging. **Reservation does not suspend aging.**
- Crafting component identity includes the exact source occurrence and properties; matching names alone do not establish interchangeability. Its `0.01` precision for explicitly divisible bulk is procedure-scoped, not a universal inventory quantum.
- [`fishing_reference.py`, `validate_material_successor` and `material_history_to`](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/tools/fishing_reference.py#L648) provide concrete predecessor/history checks. They prohibit unexplained material growth or restoration after irreversible loss. **They are bounded anatomy validators, not a reusable generic stack splitter**—the successor validator actually requires the same recorded unit IDs.

**Engineering recommendation:** keep physical lots separate and let the UI group them. A displayed stack need not erase constituent provenance, reservations or expiry. This avoids needing a gameplay rule for destructive merging.

**3. Eating/drinking versus Supply**

[Expedition FL-04](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-04) supplies the controlling accounting:

- One Supply basket comprises **2 lb edible food, 8 pints potable water, 1 pint compatible lamp oil in its flask, and 0.25 lb camp sundries**.
- Record actual food/water consumption **by recipient and lot**. Ordinary partial rations credit their edible mass.
- Food does not generate water, oil or sundries. Camp Greens’ eight pounds therefore represent **four Small/Medium food-days**, not four complete Supply baskets.
- A procedure charging whole Supply commits the actual basket or its expressly permitted substitute. Ordinary eating is not that conversion.
- Daily shortfall settlement exists, but this does not settle the still-pending calendar-anchor choices.

The timing distinction matters:

- [Common equipment procedures, opening rule](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md#L5): using a consumable normally costs an **Action**, an available hand, actual access and one real unit. This does not define the food mass or water volume constituting an ordinary intake unit.
- [Cooking — Eating, feeding and interruption](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/DescentReviewChanges/ReviewBible/docs/mechanics/COOKING_RECIPE_PLAYTEST.md#eating-feeding-and-interruption): magical recipe servings require **ten uninterrupted active minutes**; in initiative, **100 consecutive regular-turn Actions and at least 600 elapsed seconds**. Whole-serving commitment, interruption loss and permission to finish after expiry belong to that procedure. **Do not silently apply them to Camp Greens or ordinary water.**

The local `core-consumable-use-local-draft-01/USE_MODEL.json` remains explicitly **unsubmitted and unadopted**; it cannot fill these gaps.

**Smallest recommended owner-decision package — NEW, unadopted**

1. **Ordinary handling:** classify one readily accessible handheld item’s pickup, voluntary drop, retrieval, stowing or willing handover as one ordinary object interaction. In exploration, propose **one active second** per operation for responsive direct control. In tactical play, use the existing interaction allowance; do not advance an additional six seconds. Opening an ordinary closure is a separate interaction; specific equipment/cargo procedures override. Handover requires actual reach, consent and receiving capacity; the acting donor pays, with no separate receiver Action. Custody changes at completion; ownership remains unchanged unless separately transferred.

2. **Portioning:** permit ordinary edible bulk and water to have explicitly quantified portions. Logical subdivision costs no time and moves nothing; physical handling retains its applicable cost. Transfer only unreserved quantity through the ordinary transfer command. Preserve existing reservation IDs on the retained lot; moving reserved stock requires a job-aware procedure. Children inherit provenance and freshness exactly. Mixed histories remain constituent lots, even inside one container.

3. **Ordinary intake:** propose **ten active minutes per ⅔ lb food** and **one active minute per pint of water**, proportional for smaller quantities. The food rate borrows Cooking’s pacing; the water rate is a new prototype choice. Credit and debit the quantity actually consumed as work proceeds. Interruption preserves that credit, releases untouched stock and grants no magical benefit. Expiry stops further edible consumption; there is no Cooking-style expiry exemption. For the first slice, enable these as self-consumption jobs outside combat; combat entry interrupts them. Tactical ordinary intake remains explicitly gated pending its own profile.

Those choices are recommendations for Chris, not recovered rules or approvals.

**Concrete integration pointers**

[`WorkLedger.cs`](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/engine/com.decennium.foundation/Runtime/Core/WorkLedger.cs#L24) already supplies lot IDs, units, custody/location, availability and retained settlement receipts. [`CropFoodRecord`](https://github.com/BordelonDevOps/DecenniumDescent/blob/377db0e7/engine/com.decennium.foundation/Runtime/Core/CropRecords.cs#L89) supplies batch provenance and freshness.

Extend those through the existing transaction path. Preserve ownership separately from custody, propagate crop metadata to descendants, and explicitly address quantity precision: `long Quantity` with `food-pound` units cannot represent ⅔ lb. A finer unit or rational quantity is an engineering choice; silently changing the meaning of existing saved units is not.
