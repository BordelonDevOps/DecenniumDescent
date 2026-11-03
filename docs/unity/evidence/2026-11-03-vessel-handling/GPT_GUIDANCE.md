# Intact vessel handling guidance

[Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206), response `286b56c6-fa86-5804-ad89-8ef66bdf9d33`, 2026-11-03. This applies the existing owner-approved ordinary handling policy to a bounded safe intact-transfer profile; it is not a new approval or source promotion.

**Yes. The approved ordinary-handling policy is sufficient for a bounded intact skin/flask transfer.** No additional outcome decision is needed for readily accessible, securely closed vessels, feasible supported placement and transfers free of conflicting reservations.

I reviewed **main `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`**. The one-second timing comes from Chris’s later prototype approval; the pinned sources supply the underlying physical constraints.

**Exact source support**

| Source section | Consequence |
|---|---|
| [Equipment — Record possessions and permissions](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md#record-possessions-and-permissions) | Track each item’s identity, owner/custodian, location, condition and remaining contents. |
| [Body — What melds](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md#what-melds) | Container and contents remain distinct items. Borrowing changes custody without changing ownership. Melded contents are inaccessible. |
| [Body — Carrying and Load](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md#carrying-and-load) | Count container tare and contents once, through nested containers. Check pounds and Load separately; capacity does not grant hands or access. |
| [EX58 EC-03 — Physical lots](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md#ec-03--physical-lots-supply-and-daily-support) | Preserve each lot’s title, actual custodian, nested location, constituent identity, restrictions and clocks. Fit requires mass, volume, shape, closure and material compatibility independently. |
| [FL-05 — Buying, packing and keeping provisions](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-05) | A **sealed prepacked handover uses actual item-access time**, distinct from the one-minute filling procedure. |
| [TR-12 — Transfer provisions](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#L1065) | Existing shorter access procedures remain applicable. Safe cooperative transfer can need no roll; hazards require their actual procedure. Record sender, receiver, location and identities. |

**Application of the approved policy**

- **One intact vessel is one handling operation**, even when its liquid comprises several provenance lots. Moving it is neither filling nor separately handling every constituent.
- Preserve the vessel’s ownership and each liquid lot’s ownership independently. Changing the holder must not transfer title, merge histories or grant permission to consume someone else’s water.
- Move the vessel’s physical location and the contents’ **effective custody/location chain together**. The liquid remains inside that same vessel. Mere relocation needs no new liquid descendant or quantity debit.
- Validate permission, recipient consent, available supporting hand/anatomy and the recipient’s complete resulting burden. The filling profile’s **two-hand requirement does not automatically apply to ordinary handheld transfer**.
- Use the adopted one active second in exploration and existing interaction/Action allowance tactically. Custody changes at completion; process the shared timeline as already specified.

One implementation consequence matters: **movable vessel tare must follow the vessel**. It cannot remain as a fixed charge on its former carrier while also being charged to the recipient. Empty vessels still retain their own tare.

**Reservations and remaining boundaries**

Check the whole containment chain. Moving a vessel containing reserved water would move reserved stock, even if the vessel itself has no quantity claim. The approved ordinary-transfer path cannot bypass that restriction.

For this increment, explicitly gate vessels participating in pending filling or another incompatible job, including paused destination-capacity claims. Do not silently cancel reservations or relocate a paused job. Allowing such movement later needs a specified job-aware operation; reservations do not, by themselves, establish a universal rule that objects are physically immovable.

For pickup/drop, require an actual reachable, supported placement supplied by the fixture. Do not extrapolate the form-reversion rule’s “nearest legal adjacent position” into a universal voluntary-drop algorithm. Falling, breakage, spilling, contested possession and unknown fit remain outside this bounded path. **Those exclusions leave no missing outcome decision for the safe intact-transfer case.**

**Recommended implementation order**

Implement intact vessel movement next, then move to a **fixed-roster tactical scheduler**.

Vessel movement completes the useful sequence **fill → carry → hand over → drink**, exercises nested custody and removes the present fixed-custody assumption without requiring new gameplay rules.

The adopted initial equal slots also support subsequent fixed-roster turn advancement and save/resume. [Combat timing](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#time-and-event-ordering--new) supplies regular-turn events and preservation of captured markers. Joining, leaving, reordering and encounter exit remain separate integration decisions; they need not block that bounded scheduler, but initial slots alone do not complete the encounter lifecycle.

That ordering is an engineering recommendation, not a new owner policy.
