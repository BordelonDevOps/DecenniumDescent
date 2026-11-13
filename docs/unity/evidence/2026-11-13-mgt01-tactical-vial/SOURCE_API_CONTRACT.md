# MGT-01 tactical access to the packed recipe 4 vial

This proposal adds tactical opening and retrieval for the selected hero-worn Explorer's Pack and the same manufactured recipe 4 dose zero. The direct dependencies are FND-01, FND-02 and FND-05. The accepted wire97 composition and shared tactical interaction and alchemy procedures are operational inputs. [Mapped dependencies](../2026-11-03-rule-map/RULE_MAP.json) · [Successor decision](../2026-11-13-mgt01-vial-stow/GPT_FINAL_REVIEW.md)

## Source authority

The pinned revision is `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

| Authority | Exact binding | Rule used |
| --- | --- | --- |
| Combat Action | `72bcb58af57f8bfe27596ec0b1467e4c780a6ef8` | A regular turn grants one ordinary object interaction. A second uses the Action. Surprise preserves an otherwise lawful simple free interaction while denying an Action. |
| Alchemy | `a253486adc64daaaa9d105f8911dcd267c971e06` | Drinking the accessible whole dose requires an Action and one available hand. The surviving empty vial keeps its structural HP and weighs 1/10 lb. |
| Body and Equipment | `60f81c5706857c5528d9d19e3da9ac15dcd7fb85` | Each body counts once. Melded items and contents are inaccessible. |
| Equipment Acquisition | `789e905552aba2ee9a4bbad1ae73aa314b77af10` | Backpack capacity is 30 lb and 1 cubic foot. |
| Adopted ordinary handling §A | `f2c11a5a5509623a3217616fb47f7d6693f8c33b` | Opening a closure and retrieving a readily accessible handheld item are separate interactions. Exploration alone uses one active second per operation. |
| Agreed portable equipment | `25776c3ef2c6287f9dd373b0136a1ad5ad1d9d69` | Use the existing physical-placement, access, capacity and tactical object-interaction procedures. |

[Combat Action](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md) · [Alchemy](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md) · [Adopted inventory decisions](../../INVENTORY_RULE_DECISIONS.md) · [Portable equipment decisions](../../PORTABLE_EQUIPMENT_RULE_DECISIONS.md)

The accepted TEST_ONLY exact fit in the hero's worn pack carries forward. Preserve the exact recipe order, linked body, title and maker with the companion, hero custody, native dose, pack fit members and attachments. Keep the base90 capacity and burden rules. The worn parent must match the accepted identity and arrangement. Opening changes access only. Retrieval moves the direct contained child to the hero's held root, occupies one hand, and synchronizes dose location. Both conserve carried mass and Load. Drinking uses the same held-dose self-use procedure, advances its existing RNG and life resolution, and leaves the same empty vial. [Accepted fit and ordinary path](../2026-11-13-mgt01-vial-stow/SOURCE_API_CONTRACT.md)

## Shared command composition

Propose `ConnectedExpeditionSession.StartWithTacticalVial()` and console selection `-TacticalVial`. Reuse the current public submit surface and existing command payloads. In the genuine later encounter only, admit the hero's `OpenPortableContainer` for the exact closed worn pack containing the selected dose, and `HandlePortableEquipment` with Retrieve, amount one, empty destination for the same vial in that exact open pack. Keep ordinary handling and the existing tactical `UseAlchemyDose` unchanged. The new tactical scope is opening and retrieval. Tactical pickup, stow, close, removal, drop and handover of the selected packed arrangement retain the existing unsupported boundary. Retain mandatory held-item drop through the existing consequence path.

Use the current player grant and revision, normal receipt/duplicate handling, active later encounter, `Encounter.CurrentActor` and current inventory turn ledger. Existing payloads identify the item/container and are bound to the current turn through the expected revision and authoritative active slot. Pending tactical choices and the existing manufacturing-choice gate have precedence before any spend or physical change. Access is restricted to the hero's owning regular turn, actual stationary position, available hand, reachable unmoved root, physical access, and the existing capability, work and inventory guards. Apply existing source condition permissions. The first otherwise legal simple interaction requires no Action permission. The second requires both Action permission and an unused Action. Preserve ordinary command denials and current seat filtering. A revoked grant cannot use a prior successful receipt.

| State on the hero's regular turn | Operation | Effect |
| --- | --- | --- |
| Closed pack, first interaction available | Open | Spend the one free interaction. Vial remains contained, no hand occupied by it. |
| Open pack, first interaction available | Retrieve | Spend the one free interaction. Vial becomes held in one hand and an unused Action remains available. |
| Open pack, first interaction already spent, Action available | Retrieve | Spend the second interaction and the Action. Hold the vial. Drinking waits until a lawful Action is available on a later turn. |
| First interaction already spent, Action already spent | Open or retrieve | Deny unchanged. |
| Open pack with dose still contained | Drink | Deny unchanged even when the Action is available. |
| Same vial held, Action permitted and available | Drink | Spend one Action, resolve the real dice and HP cap, retain the empty vial. |

Reuse `ResolvePortableEquipment`, `WorldIntervalRecord.SpendInteraction`, `InventoryInteractions`, tactical portable records and `UseAlchemy` with its existing `PayAction` and held-body access check. Each tactical manipulation records the current turn and equal start/end through the existing history and receipt linkage. It has zero added RuleClock and no work interval. Advancing the regular turn continues to use the shared clock and defender decisions. An already spent Action can coexist with an unused free interaction. Ordinary open/retrieve still cost their paid second.

## Explicit persistence

Propose wire98/base90 with one new explicit selection, fingerprint and discriminator, composing the existing carried and stowed flags and records. All portable parent/open/held/custody, receipt, dose and tactical interval fields already exist. Add no separate charge, hand, turn or inventory representation. Strict restore verifies marker/fingerprint/profile, existing physical validation and receipt-bound history replay including each tactical spend, then atomically publishes. Reject mismatched selection and inconsistent actor, clock, interaction, Action, parent, access, or duplicate body. Preserve authentic wire95 Default and Fishing Trap, wire96 held-only, and wire97 ordinary stow/retrieve bytes and continuation. Restore from an explicitly selected corresponding profile.

## Acceptance and evidence

1. Run actual manufacture, paid pickup and stow, ordinary close and departure, genuine later encounter entry still packed, and live denial of closed retrieval and direct contained use. Save/restore at real packed entry, after tactical open, after tactical retrieval and after use. The closed route spends free Open then Action Retrieve. Same-turn use is denied atomically. Play through actual intervening turns, including the normal defender path, then use the same held dose on a lawful hero turn. Record actual RNG, HP, cost, body, burden, encounter closure and ordinary continuation.
2. Run a genuine pre-opened branch from a real ordinary boundary. Enter packed with the pack already open, deny direct contained use, spend one free Retrieve, then drink with the same turn's available Action. Include spent-Action or exhausted-interaction contrasts, wrong seat/turn, pending choice, and invalid or duplicate/stale requests. Record which controls arise in live connected play and which require focused tests. Denials must leave revision, state, clock, RNG, counters and ledger unchanged. Check available hand, shape and no tactical work time.
3. Compare actual restored console, uninterrupted console and direct public C# replay for both connected branches, including automatic decisions, with canonical saves and observation records. Validate authentic older wire95/96/97 restores and continuation, plus contradictory or cross-profile restores. Retain exact source and build identity, C# 9 warnings-as-errors compilation, static checks, focused controls and the exact 1,493 predecessors plus new registered cases.

Scope remains TEST_ONLY. Production authority, general tactical inventory, other containers, new recipes and Unity gameplay integration remain deferred.
