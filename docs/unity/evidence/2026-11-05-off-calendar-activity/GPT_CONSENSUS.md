# Schema40 Codex/GPT consensus receipt

**Date:** 2026-11-05  
**GPT conversation:** [Unity Rules Engine Development](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206)

This note records delegated prototype completions, not recovered source text or owner-approved release rules. The pinned Expedition Player Book and combat movement rules support shared-clock activity accounting and paid Dash; they do not define the off-calendar interval adapter or all work-rounding details.

## Activity and labor accounting

- The off-calendar actor uses half-open six-second intervals anchored to `WorldSchedule.Origin`. Movement, pause/resume, job changes and save/load do not reset spending; only the fixed boundary does.
- `None`, `Dash` and `ActiveLabor` share one ordinary Action commitment. Any positive credited active labor commits `ActiveLabor` for that interval. Continuous, adjacent work segments may share it while each job and work interval remains separately recorded.
- Normalize `WorkLedger.WorkerIntervals` with procedure-specific `Working`/setup records. A linked job counts once. An unlinked active procedure remains a labor claim and blocks Dash; contradictory actor/history references fail validation.
- A current or future worker interval overlapping the fixed interval blocks Dash, even if no labor has yet been credited. Paused material/capacity claims, passive crop growth, passive Trap soak and uncommitted assignments do not reserve the Action.
- After Dash, reject new/resumed active labor and prevent scheduler credit in that interval. Pausing/canceling cannot refund Action. After ActiveLabor, only a continuous adjacent work segment can continue sharing that commitment. Ordinary walking can continue if its movement budget and procedure compatibility allow it.
- Activity movement resets only at the fixed six-second boundary. Speed changes preserve movement already spent.

## Running-route renewal

- A still-running off-calendar route automatically attempts exactly one fresh legal Dash at each fixed interval boundary, after the outgoing interval's movement/labor and due shared-clock effects settle. It moves only after payment succeeds.
- Resolve `WorldTraversalRecord.StartedRevision` to exactly one retained, validated `BeginWorldStep(run)` receipt for the same actor. Preserve that receipt's exact ID and revision as Dash authorization. The actor/calendar/interval ordinal identifies each separate renewal; the authorization reference is not a duplicate command execution.
- Missing or mismatched route authorization fails snapshot validation. A failed boundary attempt spends no Dash or movement and leaves the partial edge `Suspended`. Suspension persists across save/load; removing a blocker does not auto-resume it. Explicit resume revalidates current conditions and route legality.
- A voluntarily suspended route never renews automatically. These activity boundaries create no tactical turns, Reactions, death saves or stance refreshes.
- A historical stop reason is not persisted for this increment. The suspended state is the required gameplay state; after loading, report “resume required” and derive current blockers without claiming they caused the earlier stop.

Codex and GPT agreed that these completions need no owner escalation. Automatic renewal and `ActiveLabor` remain TEST_ONLY until broader engine/source validation.
