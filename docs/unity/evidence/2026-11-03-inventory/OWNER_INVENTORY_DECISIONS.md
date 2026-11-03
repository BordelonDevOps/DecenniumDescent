# Inventory and ordinary intake prototype decisions

Status: OWNER-APPROVED PROTOTYPE, 2026-11-03. Chris explicitly answered “Adopt ordinary handling,” “Adopt ordinary portioning,” and “Adopt ordinary intake” to the three questions linking this specification. Sections A–C are adopted within their stated scope. Existing reviewed source rules remain separate from these new prototype choices; no release promotion is implied. The C# engine remains on Engine; Unity integration is deferred.

GPT guidance: [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206), response `010b31cb-8fe4-5038-bda6-491583d68ccd`, 2026-11-03. Source findings and exact response are retained in `evidence/2026-11-03-carrying/GPT_GUIDANCE.md`.

## Source-backed foundations

- Combat permits one ordinary object interaction per regular turn; a second interaction or Action-time activation uses an Action. Secure Cargo uses an Action for its specific cargo operation. These do not classify every pickup/drop/handover.
- Expedition TR-12 supplies one active minute for calm handling of a fitting actual bundle up to50lb. FL-05 supplies one active minute per worker for filling a skin/flask or issuing a standard Supply basket. Shorter item-access procedures remain separate.
- Ownership differs from custody/location; borrowed items preserve their owner. Melded storage is inaccessible. Physical carrying requires both mass and Load checks plus anatomy/access.
- Dividing, trading or repackaging does not reset age. Reservations do not suspend aging. Original lots or recorded descendants retain quantity, origin and history.
- Ordinary food/water consumption credits the actual recipient and lot. Supply is2lb edible food +8pints potable water +1pint compatible lamp oil in its flask +0.25lb camp sundries. Eight pounds of Camp Greens is four Small/Medium food-days, not four complete Supply baskets.
- Magical Cooking serving timing, whole-serving interruption loss and expiry exemptions do not automatically apply to ordinary greens or water. The separate consumable-use draft is unsubmitted/unadopted.

## A. Ordinary handling — adopted prototype policy

Classify one readily accessible handheld item's pickup, voluntary drop, retrieval, stowing or willing handover as one ordinary object interaction. In exploration, one operation takes **one active second**. In tactical play, use the existing ordinary-interaction allowance; a second ordinary interaction uses an Action. Do not add six seconds per operation or tactical Action.

Opening an ordinary closure is a separate interaction. Exact equipment/cargo/filling procedures override the generic operation. Handover needs actual reach, consent and receiving capacity; the acting donor pays, with no separate receiver Action. Custody changes at completed handling; ownership remains unchanged unless separately transferred. This grants no hands, access, space, carrying capacity or permission to touch another owner's goods.

## B. Ordinary portions — adopted prototype policy

Permit ordinary edible bulk and water to have explicitly quantified portions. Logical subdivision takes no time and moves nothing; physical handling retains its own applicable cost. Transfer only unreserved quantity through the ordinary transfer command. Existing reservation IDs stay on the retained lot; moving reserved stock requires a job-aware procedure.

Children inherit provenance, restrictions and freshness exactly. Parent and descendants conserve the original quantity. Mixed histories remain constituent lots, even in one container; display grouping need not erase physical records. No time reset, duplicate quantity, automatic Supply conversion or universal0.01 inventory quantum is authorized.

Exact rational quantity representation is an engineering choice already supported by the C# numeric primitive. It does not silently reinterpret legacy saved `long Quantity` or `food-pound` units; any new inventory state requires an explicit versioned schema.

## C. Ordinary self-consumption — adopted prototype policy

Outside combat, ordinary edible food takes **ten active minutes per2/3lb** and potable water takes **one active minute per pint**, proportional to smaller quantities. Food pacing borrows Cooking's duration only; water pacing is a new prototype choice.

Record and debit actual consumed quantities as active work proceeds, by recipient and source lot. Interruption preserves consumed credit and releases untouched stock; it grants no magical meal benefit. Expiry stops further edible consumption, with no magical Cooking expiry exemption. Combat entry interrupts these self-consumption jobs. Tactical ordinary intake remains unavailable until a separately specified profile exists.

These rates do not decide canonical day/watch anchor choices, complete daily provisioning/Strain settlement, magical meals, feeding another creature, special diets or emergency tactical consumables. Existing applicable exact procedures retain their own rules.
