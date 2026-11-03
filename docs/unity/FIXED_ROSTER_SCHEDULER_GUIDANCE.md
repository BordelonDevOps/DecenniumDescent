# Fixed-roster scheduler source guidance

Guidance obtained after Engine `ac01b64a7b11df3d9d5b77359574277c68cc5e8a`, 2026-11-03. [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206), response `2005215f-4f57-529e-9a32-e3abb613b79f`. This is implementation guidance under existing approvals, not a new owner decision. Schema7 implements only the fixed-roster schedule, completed boundaries, ordinary Action/interaction refresh and Dash. Actor effects, reactions, pending decisions and end-round events described below remain unsupported; this guidance is not evidence that all procedures were implemented.

**The fixed roster can repeat the same equal slots every six seconds without another owner decision.** The source preserves the established initiative order; Chris’s approved allocation supplies its phases. Joining, leaving, reordering and exit remain separate.

I checked the combat sources at `46a4d527…` and the newly pushed Engine checkpoint `ac01b64a…`.

**Round repetition and initiative ties**

[Combat — Encounter and action resources](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#encounter-and-action-resources) says to keep the resulting ordered slots for the encounter. Combined with the [approved initial allocation](https://github.com/BordelonDevOps/DecenniumDescent/blob/529f762f013a00aca6c74317a0290199c0c8a50b/docs/unity/PROTOTYPE_RULE_DECISIONS.md#initial-initiative-checkpoint-allocation--adopted), for numbered round `r ≥ 1` and actor index `i = 0…N−1`:

```text
Start(r,i) = T0 + 6(r−1) + 6i/N
End(r,i)   = T0 + 6(r−1) + 6(i+1)/N
```

Thus the last End of round `r` and first Start of round `r+1` share `T0 + 6r`. **Do not add another six seconds at wrap.** Preserve exact rational timestamps.

Initial initiative ties already have a rule: players choose player/player ties; the Director resolves ties involving NPCs. A bounded fixture can supply that resolved order. An automatic actor-ID tie-break replacing those choices would be a **new policy**, not merely serialization ordering.

**Boundary processing**

[Combat — Time and event ordering](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#time-and-event-ordering--new) establishes:

1. Process intervening deadlines chronologically on the shared timeline.
2. At the boundary, complete the **outgoing regular End**: triggered effects, due damage, saves and maintenance precede end-ending expiration; then finish the slot.
3. At round wrap, process the source’s end-round events—hazards, reinforcements, morale, objectives and boss phases—before beginning the next round. Unsupported events must remain explicitly gated.
4. Process the **incoming regular Start** in this exact order:
   1. Expire start-ending effects and apply their immediate state changes.
   2. Refresh Reaction; tick regular-start recharge/non-action clocks.
   3. Resolve already-due absolute state recovery if now legal, including blocked Stable recovery.
   4. If still alive, dying at zero HP and using death saves, make that turn’s death save.
   5. Resolve other start effects and periodic events in application order.
   6. Permit voluntary decisions.

The approved outgoing-before-incoming convention applies at round wrap too. End-round processing belongs to the closing round; advance the numbered round before its successor’s Start.

**Do not insert a blanket “expire everything at this timestamp” phase between End and Start.** End-bound and start-bound expiration already belong to different phases. Absolute deadlines retain their own source rules. Specific exceptions also exist: [Healing pulses — Shared timing](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_PULSE_PLAYTEST.md#L11) preserves final ticks of explicitly finite sequences before those sequences end.

Where events genuinely share a phase, the reviewed ordering is application timestamp, printed within-source order, stable application sequence, then mechanical/source IDs as deterministic tie-breaks. That ordering does not override an explicit source phase.

**Refresh rules**

| Resource | Required behavior |
|---|---|
| Ordinary Reaction | Initialize on encounter entry, subject to surprise/prohibitions. Refresh only at that actor’s regular Start—not everyone’s round wrap. A later actor can spend its initial Reaction before its first turn and refresh on that Start. |
| Ordinary Action and interaction | Fresh regular-turn allowance: one Action and one ordinary free interaction. The second ordinary interaction spends the **same Action resource** used by other Action commands. |
| Movement | Begin the regular turn with spent movement `0` and paid Dashes `0`. Calculate remaining movement from current Speed; preserve spent cost through subsequent Speed/mode changes. |
| Bonus Action | No free ability is created. Permit a use only when an actual rule grants one, within its allowance and restrictions. |
| Extra full Action | At most one per creature per numbered round, and only with a real grant. Changing round makes the next round eligible; it does not grant an extra Action. |
| Extra turns | Do not refresh the ordinary Reaction or reviewed regular-turn allowances. Keep them unsupported in the first scheduler if their full execution contract is absent. |

Initializing ordinary Action/interaction/movement counters once during Start is bookkeeping. Place it consistently alongside regular-start refresh processing, with voluntary use unavailable until Start finishes. A condition prohibiting an action still prohibits it; refreshing a counter does not remove that condition.

Surprise blocks movement/Action/Bonus Action on the first regular turn and Reaction until that turn ends. It does not delete that slot or its events. The existing [`ReactionClock`](https://github.com/BordelonDevOps/DecenniumDescent/blob/529f762f013a00aca6c74317a0290199c0c8a50b/engine/com.decennium.foundation/Laboratory/Model/PlaytestCombatBudgets.cs#L39) already separates availability from surprise/prohibition. Its `long` marker is a **regular-start ordinal**, not a rounded rational timestamp.

**Effect deadlines to preserve**

The existing rules and [`PlaytestTiming`](https://github.com/BordelonDevOps/DecenniumDescent/blob/529f762f013a00aca6c74317a0290199c0c8a50b/engine/com.decennium.foundation/Laboratory/Model/PlaytestTiming.cs#L23) establish:

- Bare hostile target-bound `N rounds`: Nth future regular target-End, excluding the in-progress target turn’s current End.
- Bare self/source or ally-beneficial `N rounds`: Nth future regular source-Start.
- “Next turn”: the next future regular turn of the named creature; explicit “this turn” is different.
- Outside-initiative bare round duration: original application time plus `6N`, preserved on entry.
- Explicit pulse, absolute, concentration and other source clocks override these defaults.
- Captured markers and returned deadlines never get recomputed from the current cursor on restore.

Keep the tested **strictly future marker** arithmetic. Application at an existing marker’s timestamp does not count that numeric occurrence or trigger an additional exclusion that skips two cycles.

**Minimal command/persistence contract — engineering recommendation**

Use the same Simulation transaction path with two new bounded operations:

- **Begin fixed encounter:** capture `T0`, an immutable resolved roster/order and a unique encounter ID; initialize encounter resources; interrupt ordinary intake through its adopted procedure; execute the first Start without advancing elapsed time. Preserve the pending-fill entry gate and reject incompatible active worker assignments.
- **End regular turn:** require the expected encounter/turn identity; advance to its exact End, process the boundary sequence, then expose the next actor’s decision state. Ending a turn should not require an unused Action. Existing tactical handling commands consume its budgets without independently advancing time.

Persist encounter origin, ordered roster, numbered round/cursor, unique turn/marker identities, per-actor allowances and consumed-marker history, plus supported effect deadlines/order records. Keep Core data separate from LabModel execution.

For the smallest implementation, save only between completed boundary transactions. Mid-boundary suspension is unnecessary until a supported event requires an external decision. Unsupported reactions/effects cannot be silently auto-declined.

**Preserve the initial-turn fixture—and version its assumptions**

The current [`InventoryCases`](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/engine/com.decennium.foundation/Tests/EditMode/InventoryCases.cs#L109) establishes:

- Entry preserves the timestamp and interrupts intake without losing consumed credit.
- First interaction plus Action-paid second interaction consumes no elapsed time or exploration labor.
- Food and vessel handling share that allowance.
- Reentry rejects; tactical intake remains gated.
- Existing frozen-turn schemas reject arbitrary tactical clock advancement.

There are concrete validation assumptions to replace **only in the new schema/profile**. [`OrdinaryInventory.Validate`](https://github.com/BordelonDevOps/DecenniumDescent/blob/ac01b64a7b11df3d9d5b77359574277c68cc5e8a/engine/com.decennium.foundation/Laboratory/Model/OrdinaryInventory.cs#L102) currently requires all tactical records to belong to the current actor, their total to equal the current interaction counter, and historical tactical/intake-interruption timestamps to equal the current clock. Vessel movement has the same frozen-time assumption.

Bind new historical records to their **actual encounter/turn/entry receipt**, rather than today’s cursor and clock. Preserve the old validators and save meanings.

**No new approval is needed for this bounded scheduler.** A universal priority for an otherwise-unmapped absolute-expiry collision, automatic initiative tie adjudication, or broader encounter transitions must not be invented. Keep such cases outside the admitted fixture until their applicable source or a narrowly scoped owner decision supplies the behavior.
