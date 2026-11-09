# Haven-care source contract (schema66, TEST_ONLY)

This records the pre-implementation Codex/GPT design agreement for the existing MGT-03 Haven-care dependency. It does not certify the implementation; implementation review is a separate gate.

## Pinned rules

At ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`:

- `STRAIN_PLAYTEST.md` defines one full day as 24 consecutive hours under qualifying Haven care and location conditions, with actual care, food and water. One active interval belongs to a patient. Interruption grants no completion benefit and restart requires a fresh 24 hours. Completion removes every eligible ordinary `expedition.strain` point; blocked or special points remain. Patient sleep, meals and Morale recreation may occur during care; practitioner work cannot also count as practitioner rest.
- `EXPEDITION_PLAYER_BOOK.md` FL-03 defines daily Small/Medium demand as 2 lb edible food and 8 pints potable water, counted from actual consumption. FL-24 says a Haven name alone does not grant a service or provisions, and compatible patients may rest during care.
- Existing `expedition.strain` point metadata, gain/removal histories, recovery gates, Rest Debt and shared clock remain the authorities. Haven care adds no second Strain counter or intake ledger.

The source names Haven care as a recovery procedure. The nonlethal level-six Expedition Collapse behavior in `STRAIN_PLAYTEST.md` is explicitly `NEW`; this increment does not implement that condition or claim collapse recovery.

## Agreed bounded adapter

- Add an explicitly fingerprinted TEST_ONLY provider, service and site identity; a finite patient roster, availability window, capacity of one and authored site coordinate; and an explicit `CanDeliverReviewedCare` fixture fact.
- Use a half-open 24-hour interval. Qualify food and water from actual consumed `WorkLedger` reservations in existing `IntakeRecord` history, clipped to that interval and freshness. Do not add a care-specific debit ledger.
- Keep the patient at the admitted site. Require compatible rest and allow other actors to perform work. Reject unsupported combat/emergency paths safely; do not invent a general care qualification, labor market, price or free-care rule.
- At a coincident endpoint, finish life/condition and ordinary provisioning/Rest Debt effects first; finish Rest and Morale completion next; assess Haven care and apply its complete Strain batch next; then expose other recovery choices. Morale offers defer across the Haven batch.
- A care completion removes all eligible ordinary points atomically, leaves null-classified Rest Debt gains untouched, spends no Morale or Long Rest allowance, and creates no banked benefit. Each interrupted attempt is independent.
- Append schema66 state after schema65 bytes. Keep schema65 and older branches unchanged and reject Haven provenance under earlier schema versions.

## Acceptance scenario agreed before implementation

Reach the authored care/service site; create two prior supported-day Strain points and Rest Debt through existing provisioning and Rest authorities; begin care; consume actual food and water; let a companion complete real Camp Greens work concurrently; save/restore while care is active; finish Morale Rest at the same boundary; remove exactly the eligible points while retaining Rest Debt points; and prove the restored and receipt-replayed states encode byte-identically. Also cover unsupported care and interruption/restart. Do not claim a collapse-recovery scenario because the current shared simulation does not represent nonlethal Expedition Collapse.
