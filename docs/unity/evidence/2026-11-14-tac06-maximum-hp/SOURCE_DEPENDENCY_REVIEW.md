# TAC-06 Flesh Warden source and dependency review

Wire102 acceptance `cbbb8752-d7aa-41e5-8ce1-0500301594a0` selected an authored capacity bonus with genuine application and removal. TAC-06 directly depends on TAC-04, TAC-05 and MGT-02. This proposal identifies the source and the additional runtime dependency for that source.

## Authored candidate

At ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, `data/public/class_playtests/warrior.json` card `/cards/75` names `warrior.supplement.flesh-warden`. It requires Warrior 1 and Basic Vital, consumes one mutation slot while equipped, and passively adds twice the actor's current Warrior level to their own maximum HP. The printed duration is while equipped. The Warrior engine equips eligible mutations during a completed Short or Long Rest. Flesh Warden's passive operates while equipped without serum activation. The capacity overlay recomputes from base capacity and clamps only current normal HP on removal.

| Pinned source under ReviewBible | Git blob |
| --- | --- |
| `data/public/class_playtests/warrior.json` | `7376db19c5e3c499a994cb06eae06cf25514e922` |
| `docs/mechanics/classes/warrior.md` | `38d086c74348a4a20d1e6aca6832acd11def4241` |
| `docs/mechanics/MAXIMUM_HP_PLAYTEST.md` | `8ffe82b0f964d6b16ac03625f73352087bff9ab9` |
| `docs/mechanics/MAXIMUM_HP_SOURCE_BINDINGS.md` | `ee892349c71a22f436dc39bbdf759dda777c6a93` |
| `docs/mechanics/GAMEPLAY_LOOP_CANON.md` | `36a060e318d51d55cbecb299524a227ad73cb55c` |

The existing connected hero has Warrior 3 and base capacity 26. A future fixture can propose explicit Basic Vital/Flesh Warden access, with the one unlocked mutation slot empty initially. On lawful application, maximum rises to 32. On lawful removal, it returns to 26. Confirm whether an empty slot is lawful on removal or whether the witness needs a source-qualified replacement in that slot.

## Connected feasibility and missing dependency

The retained wire102 late route has genuine injury at 18/26. Its real carried recipe-4 vial rolled 3 and 4 for a potential nine. Ordinary healing at capacity 32 would yield 27/32 from 18, enough for a one-point clamp on removal. The parent run proves those inputs occur without edited HP or forced dice. The successor must independently prove the actual dice and HP after its new commands and timing, including a legal route to a living injured actor and the finished vial. [Parent replay report](../2026-11-14-tac06-temporary-hp/public/results.json)

The public expedition does not expose a completed Short Rest or a mutation loadout. Its ordinary portable wear/remove commands have no mutation authority. The four-hour Morale Rest and the separate secure eight-hour Strain recovery profiles have their own authorities. Neither supplies the public Short Rest needed for this witness. The authored Short Rest takes one hour, allows up to two beneficial completions between Long Rests, permits optional Hit Dice, and resolves applicable class rewards and end effects. A full rest interval requires real clock time, safe access and interruption handling.

**Proposed dependency order:** review and deliver a bounded MGT-03 public Short Rest prerequisite first, then return to TAC-06 Flesh Warden. MGT-03 directly depends on MGT-02 and TAC-05. The candidate is a fixed, source-qualified safe rest site reachable in ordinary connected play. Review how this profile handles applicable Warrior rewards, voluntary zero Hit Dice, two-benefit cadence, interruption and persisted timing before code. Keep source-specific slot changes for the TAC-06 follow-up. The completed rest must authorize the mutation choice according to the approved contract. A named unsupported result should expose any unadmitted Short Rest option.

A Consume Decay grant lasts one hour, which is also the duration of a Short Rest. The accepted tactical source cannot be activated during an ordinary rest to create an overlap. Use a detached shared-operation witness to prove an active temporary grant retains its identity, points and deadline at capacity application/removal. On the connected route, show the grant's own expiry through the shared clock if it crosses that deadline. Any live same-deadline interaction requires source-supported ordering.

Open for GPT agreement: confirm MGT-03 first and its acceptance scope, or identify an exact authored capacity source with both endpoints available through the currently supported public actions. No engine edits have started for this gate.
