# Shared world calendar, exploration and transition decisions

Date: 2026-11-03 owner session (implementation receipts extend into 2026-11-04 UTC).
Status: provisional prototype completion under the owner's explicit Codex/GPT consensus delegation. Not recovered source text or release approval.

## Authority and disposition

The owner requires C# first, one shared simulation for direct exploration, tactical combat and resource management, and development on `Engine`. The owner also permits Codex and **Unity Rules Engine Development** to settle rule gaps together without repeated approval requests. [Exact guidance](evidence/2026-11-03-shared-world/GPT_CALENDAR_GUIDANCE.json) preserves the discussion, including the differing proposals. Existing clock, traversal, farming and inventory decisions remain controlling within their scope.

The latest fixed-calendar proposal is response `fcdc9374-9054-5662-becc-668dc147e2b9`; Codex explicitly accepted it in turn `ead5a652-aebf-422c-89f3-6594632fd406`. Response `48dc3272-26cc-5431-8963-af34a7a8a199` agrees with sparse processing subject to observable equivalence. These supersede the conflicting earlier `0dfdc977-3d8b-5a86-aa51-06cb8396dc0e` suggestion against an ordinary outside-combat refresh calendar. The latest response explicitly carries forward outgoing-slot completion on resolved exit, superseding that earlier response's immediate-exit suggestion. Both historical proposals are retained as history, not two selectable defaults.

Source-backed constraints include ordinary Action/Reaction/movement budgets and captured effect markers in `COMBAT_ACTION_PLAYTEST.md`, actual shared elapsed time and compatible companion labor in Expedition FL-01/02/03, continuing retreat/pursuit identity in FL-15, and actual encounter participants rather than the whole expedition roster in FL-16. These sources do not by themselves establish the new calendar initialization or continuous movement execution policy below.

## Adopted fixed calendar

- The bounded host receives a fixed resolved order of `N` actors. Persist one calendar ID and world origin `W`. Actor `i` starts at `W + 6i/N + 6k`; each slot ends at the next slot's Start. Do not fabricate pre-origin events.
- Initialize each actor's ordinary allowance once at `W`, including a single initial Reaction. Process actor 0's origin Start once. Later actors have shortened bootstrap intervals until their first scheduled Start; they may spend their initial allowance and then legitimately refresh less than six seconds after creation. No proportional allowance or retroactive work is granted.
- Exploration walking, paid Dash and other admitted interval spending belong to this calendar. Pause, input changes, save/load and control-mode changes do not refresh it. Skipped intervals never bank Actions, movement or Reactions.
- First tactical entry preserves the calendar, current slot, marker-processing state and spending. It does not initialize another encounter allowance. Entry exactly at a boundary processes outgoing End and incoming Start once before voluntary input. A partial first round advances only its remaining scheduled time; a complete round remains six seconds.
- Outside tactical mode, virtual Starts refresh ordinary interval budgets and expire stance/Press at their captured deadlines. They do not select a stance. Exploration requires no selection. In an actor's active tactical regular slot, require selection before its first applicable voluntary event, or before End if capable and no such event occurs. No off-turn selection or retroactive benefit.
- A persisted running instruction can authorize a fresh legal Dash at an actual Start. Settle prior-interval travel first, resolve boundary effects, then pay the new Dash. If payment or movement becomes illegal, suspend at the actual position. Condition expiry alone does not resume a suspended instruction; explicit resume revalidates it.

The fixed order is an explicitly supplied fixture fact. It does not decide initiative acquisition, surprise, roster changes, a genuinely new encounter, or cooperative pause. Calendar creation is not encounter creation or closure. Remote companions are outside this encounter order and earn actual compatible work independently.

## Exact exploration execution

The first admitted execution geometry is level cardinal movement between existing five-foot grid anchors. Supplied walking Speed `S` means `S` feet per six seconds. Running uses paid Dash and twice walking pace. For distance `d` and approved movement cost multiplier `m`, elapsed seconds are `6*d*m/(paceFactor*S)`. Terrain uses the existing strongest terrain multiplier, plus existing crawl/squeeze additions when applicable. This host admits walking/crawling; full jump, climb, swim and squeeze execution remains separate.

Partial distance is actual position. Keep exact rational feet along the edge; never move a whole cell early, snap back, discard partial distance, refund elapsed time or round movement expenditure. At Speed30,0.4seconds on ordinary ground advances2feet. If movement becomes illegal there, the actor stays2feet along that edge.

Advance to the earliest admitted endpoint, movement-budget boundary, condition deadline or requested time. Credit eligible work and movement through that point, resolve its consequences, recompute capability and continue only if lawful. An active instruction that exhausts its ordinary movement budget can wait for its actual scheduled refresh; a suspended instruction requires explicit resume. The current host stops each instruction at one edge's endpoint.

Existing grid-only access checks cannot use the last completed anchor as if it were a mid-edge actor's actual position. Until richer spatial consumers are implemented, mid-edge inventory/job interaction, mid-edge fall/drop consequences, concurrent hostile movement and hostile approach/departure transitions return explicit unsupported diagnostics. The player does not receive an invented geometry ruling.

## Work and resource continuity

Existing adopted procedures own input consumption, freshness, reservations and completion:

- Credit actual compatible labor before interruption. Crop labor pauses with earned work and spent inputs retained, and unused future worker bookings released. Passive crop care, growth, neglect, maturity and freshness deadlines continue.
- Ordinary intake interruption retains actual consumption and releases unused stock. No proportional refund of consumed food/water.
- A stable supported water fill pauses with progress, source reservations and destination capacity retained. Future worker/hand bookings are released. Liquid transfers only on completion; explicit resume revalidates access and resources.
- A worker who cannot perform the task does not continue earning labor. The current fixture's ordinary bodily work requires awareness and deliberate bodily capability. Unrelated conditions are not a blanket interruption rule. Condition ending does not automatically resume paused crop/fill work.
- Actual tactical participation will pause incompatible jobs for those participants. Compatible remote work continues on shared elapsed time. Tactical decisions pause the shared clock under the prior solo policy. **That tactical handoff is specified but not implemented in this checkpoint.**

Hazardous spills, breakage and unsupported body/vessel consequences remain gated. The synchronous one-second handling procedure cannot yet cross a condition deadline or another actor's active traversal; those combinations reject before costs or time. Ordinary admitted stationary handling preserves its established timing and custody/ownership contract.

## Transition and dying policy awaiting runtime integration

Resolved conflict requires the authoritative predicate: all required hostiles Dead or a specifically authored resolution event. Temporary unconsciousness, paralysis, invisibility or distance alone do not resolve the encounter. All attack/knockout/OA/Press continuations must finish. The adopted exit completion finishes the outgoing slot, processes its actual intervening deadlines and End consequences, revalidates the predicate, then changes control mode. It awards no remaining round, healing, refill or reward. If intervening events reopen conflict or require a decision, retain already elapsed time and consequences and stop closure there. Do not roll them back as a rejected player command.

The continuing fixed calendar and encounter identity survive exploration/reentry. FL-15 retreat remains the same pursuit encounter. A new mode or ID cannot restore encounter uses. Changed rosters and genuine later encounters require their own procedures. Structural closed-encounter archives are prerequisites for genuine closure; they do not authorize archiving a continuing encounter on every mode exit.

Outside-combat dying will use the actor's established virtual Starts once per globally unique marker. If no schedule exists when dying begins, the proposed adopted fallback is onset+6seconds and every6seconds thereafter; entry must not create a competing series. Stable and Dead states skip saves. At a shared marker, resolve expiry, permitted absolute Recovery, the death save, then ordinary later healing; other established local job priorities remain intact. **The current shared exploration fixture begins with positive-HP actors and admits no damage, so this dying integration is not claimed.**

## Current runtime boundary

Schema13 adds structural closed-encounter history and canonical mixed command reconstruction, plus an explicitly selected `TestOnlySharedWorldPolicy`. That policy composes existing condition, farming, food, water and inventory procedures with exact traversal and a sparse fixed calendar. One actor explores, one independent companion works at the supplied plot, and a third supplied actor participates in the calendar. The calendar is not a combat encounter.

Sparse advancement collapses only empty boundaries with equivalent outcomes. The fixture's stationary, positive-HP actors have no per-Start life event; active traversal and condition deadlines are processed explicitly. The final slot and each actor's latest real Start remain persisted. This is not permission to skip dying saves, periodic effects, reactions or future events once those are admitted.

The laboratory assembly now references the engine-free Persistence assembly solely to compare complete canonical snapshots after command replay. This covers nested crop tasks, stock, consumed/released reservations, worker intervals and condition histories without a second incomplete equality list. Core remains independent of Persistence and Unity. Checksums detect corruption; receipt replay proves admitted procedural consistency, not cryptographic authenticity of a hostile save.

The full engine, connected combat handoff, source acquisition, all content and Unity integration remain incomplete. Passing this fixture is evidence for the stated runtime scope only.
