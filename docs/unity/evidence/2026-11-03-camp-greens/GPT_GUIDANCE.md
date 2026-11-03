# Unity Rules Engine Development — crop contracts and follow-up approvals

Guidance chat: https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206

Captured 2026-11-03. These are GPT's guidance messages, not independent owner authorization. The owner separately adopted Camp Greens completion details and equal initial initiative slots in the active Codex chat; see OWNER_DECISIONS.md. Later membership/calendar/extra-turn proposals below remain unadopted and unimplemented.

## Message 71fba932-6c83-53f9-9fca-4fcc07b054e6

**Your proposed assembly split is appropriate:** immutable crop/job data in Core, serialization in Persistence, and prototype-rule execution in gated LabModel. I found **no existing crop runtime contract to port** in the inspected Engine and reviewed work sources.

The remote `Engine` head still resolves to `c52d2a3`; the pointers below are pinned there. I have not inspected your newer local 245-case implementation.

**Existing contracts worth reusing**

| Actual source | What it provides—and its limit |
|---|---|
| [Development brief §10](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/docs/unity/DEVELOPMENT_BRIEF.md#10-expedition-jobs-crafting-and-research) | The existing engineering record requirements: worker IDs, task definition, location, reservations, progress, milestones, outcome and result transaction identity. Its lifecycle names are examples, not a mandatory generic framework. |
| [Expedition Player Book, FL-02/03](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-02) | Assignment identity, lead/assistants, activity/location, actual start/end, incompatible work and the shared clock. Scheduled time alone does not prove completed labor. |
| [Crafting framework: “One work order, one batch” and “Active time”](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md#one-work-order-one-batch) | Persistent work-order identity, actual component lots, phases and once-only settlement. **Do not transfer crafting’s unfinished-phase loss or completion-time ingredient debit into Camp Greens.** Its approved profile differs. |
| [Public expedition boundary records, `EX-W01`](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/DescentReviewChanges/ReviewBible/data/public/expedition_candidate/boundary_records.json) | Concrete `records.workOrder`, `intervals`, `phaseLedger`, completion and output records. Useful accounting examples, not a runtime schema. Current scoped review status is in [EXPEDITION_REVIEW_STATUS.json](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json); historical labels inside examples remain preserved. |
| [`fishing_reference.py`](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/DescentReviewChanges/ReviewBible/tools/fishing_reference.py) | `active_work_seconds` at line 773; `FishingLedger` at 832; `_reservation` at 917; `_setup_and_fishing` at 941; `_schedule` at 962; `apply` at 1275. These demonstrate work evidence, commitment, passive waiting and ordered due events. The helper explicitly says it is **not a game runtime**—reuse applicable invariants, not its separate journal as another simulation. |

There is no requirement to build a universal job framework first. A specific immutable crop record and its planting/tending/harvest task records are sufficient. Core can validate structural consistency without deciding growth, failure or yield. Keep those decisions in the selected prototype policy, including the still-pending boundary completion.

**NEW schedule proposal: freeze the current round; revise future rounds**

This is a complete proposed baseline for ordinary membership/order changes, with explicit handling for source-authorized midround entry. It is **not recovered Decennium rules or an adopted policy**. The equal-spacing formulas remain conditional on approval of the initial-phase proposal.

1. **Keep fixed round boundaries.**
   For encounter origin `T₀`, round `r` begins at `T₀ + 6r`. Joining, leaving and reordering never restart that origin or extend a round.

2. **Publish an immutable calendar for each round.**
   At its beginning, resolve the previous round’s required ending events, apply queued membership/order changes, then publish the new calendar. If equal spacing is approved, actor `i` of `N` gets:
   `start = B + 6i/N`, `end = B + 6(i+1)/N`.

   Initiative rolls and player/Director tie decisions supply the order. Entity IDs must not substitute for those gameplay decisions.

3. **Ordinary joins and reorders take effect next round.**
   Record accepted changes in authoritative command order. Reordering never gives another regular turn in the current round. Maintain a prospective next-round calendar so effects needing a newcomer’s future marker have an explicit schedule to capture; later revisions do not rewrite those captured markers.

4. **Leaving immediately removes participation, but preserves current-round checkpoints.**
   An unstarted slot becomes a vacant slot until the round ends. Leaving during a turn stops further voluntary decisions; retain its scheduled end checkpoint. A vacant slot does not grant an absent actor fresh actions or reactions. Existing effects still receive their subscribed timing events.

   Incapacitation or inability to act is **not departure**: the source-defined regular turn still occurs.

5. **Returning preserves identity and opportunity history.**
   Do not initialize another Reaction or clear spent allowances merely because the same actor returns. Under a legal midround-entry permission, it may reclaim its original vacant slot only if that slot has not begun. Otherwise it waits until next round. A regular slot that already began cannot be obtained again through leave/rejoin.

6. **Handle explicitly permitted midround newcomers without moving existing slots.**
   Determine the entrant’s position in the resolved initiative order:
   - If that position is already passed, defer its regular turn until next round.
   - If it precedes an unstarted slot, insert its regular **start → decisions/resolution → end** immediately before that slot’s start checkpoint.
   - If it follows every existing slot, insert it at the round-end timestamp, before end-round processing.
   - Once end-round processing has begun, ordinary admission is for the next round.

   **This inserts a zero-elapsed-time slot:** start and end have the same rational timestamp but distinct ordered checkpoints. It grants the ordinary source-defined turn opportunity, not another six seconds. Multiple inserted actors follow their resolved initiative order.

   This is the proposal’s principal tradeoff: current-round timing remains stable, but same-time event ordering becomes explicit. It must be reviewed as a new scheduling choice.

7. **Use an event cursor, not timestamp comparison alone.**
   “Upcoming” means the slot’s start checkpoint has not executed. Entry during that slot is too late, even if several checkpoints share its timestamp. Each regular opportunity has a persistent identity and can begin/end only once. Extra turns remain separate and do not create regular-marker refreshes.

8. **Keep effect markers independent of roster calendars.**
   Preserve each captured marker’s identity, original phase, recurrence and resolved occurrence history. A new calendar affects newly created effects; it does not move existing deadlines. A virtual effect marker is not itself another regular turn.

   On encounter exit, preserve those subscriptions on the shared timeline. Do not round up an incomplete round or discard remaining effects merely because initiative ended. If an encounter remains open with no participants, avoid division by zero: process its existing due events and boundaries without inventing actor turns.

**Example**

Initial calendar: A `0–2`, B `2–4`, C `4–6`.

At time 1, a source-authorized newcomer D belongs between A and B. D receives ordered start/end checkpoints at time 2, before B. B and C retain their current slots.

Next round, A/D/B/C may receive `6–7.5`, `7.5–9`, `9–10.5`, `10.5–12`. An effect previously bound to B’s original start phase still uses **2, 8, 14…**, despite B’s new actual start at 9.

That behavior follows the existing requirement to preserve captured markers; **the calendar-revision and insertion policy is new**.

Persist the published/prospective calendars, pending changes, current event cursor, regular-opportunity history and captured-marker occurrences in the same snapshot. This supports deterministic restore without selecting Chris’s pending policies on his behalf.

---

## Message eb4d0e40-28bc-5a9d-bb5a-fc2672da1872

Recorded in this handoff:

- **Approved prototype policy:** the full Camp Greens boundary/failure completion, equal initial initiative slots, and outgoing-before-incoming endpoint ordering.
- **Still unadopted:** future join/leave/reorder behavior, including my proposed zero-elapsed-time midround insertion.
- **Reported checkpoint:** `1ca99b2e` / code `ba01a509`, **247/247 cases**, including 17 prototype cases and regressions for both arithmetic findings.

Your Core-data / gated-LabModel-execution split remains consistent with the shared command and persistence architecture. The cited source contracts remain useful references; Camp Greens’ approved rules govern its actual behavior. Future encounter scheduling does not block the crop lifecycle work.
