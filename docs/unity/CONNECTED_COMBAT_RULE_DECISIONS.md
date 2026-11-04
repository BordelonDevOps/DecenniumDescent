# Connected tactical control on the shared calendar

Date: 2026-11-03 owner session; implementation evidence extends into 2026-11-04 UTC.
Status: explicit prototype integration under the owner's Codex/GPT delegation. No release promotion.

## Controlling policy

[Shared-world decisions](SHARED_WORLD_RULE_DECISIONS.md) retain the adopted calendar, exact traversal, job interruption and outgoing-slot exit rules. That document describes the earlier schema13 runtime boundary; this record supplies the subsequent schema14 implementation status. GPT response `27c243c7-107e-5183-be6b-6ae7e40c8a85` explicitly confirms that `fcdc9374` plus Codex's adoption controls the world-created calendar and outgoing-slot exit, superseding the conflicting older proposal. [Frozen guidance](evidence/2026-11-03-connected-combat/GPT_CALENDAR_GUIDANCE.json) contains the exact exchange.

The governing source constraints remain ordinary combat budgets and timing, Expedition FL-01/02/03 actual shared time and compatible work, FL-15 encounter continuity and FL-16 actual participants. Existing movement, ordinary attacks, conditions, inventory, filling and farming decisions retain their prior status. Sparse representation and command replay add no new gameplay allowances.

## Sparse schedule identity and processing

Schema14 stores actual command observation revisions separately from absolute calendar ordinals. A first encounter at slot204000 needs one observation, not204000 fabricated Start commands. Actor, round and timestamp derive from the unchanged calendar. Observations are strictly ordered and bounded; old schemas retain their former consecutive meaning and bytes.

The shared clock commits only fully processed boundaries. A command advances admitted work and condition deadlines, refreshes the corresponding interval, resolves required life events, and then records the resulting observation. It does not expose an intermediate boundary phase as a save point. First entry consumes the already processed position; it does not run expiry, refresh, equipment onset or a death save again. Exact-boundary expiry → save/restore → entry and paid interval spending after a boundary are separate regression cases.

Empty stationary intervals may collapse analytically. Active traversal, condition deadlines, tactical slots and admitted dying actors require their meaningful boundaries. The schema14 dispatcher processes condition expiry before recovery and scheduled death saves, retaining actual compatible work credited through that instant. Outside-dying processing is present, but no reachable outside-dying scenario is qualified by this fixture: damage is admitted through tactical attacks and its resolved-exit predicate requires the sole hostile Dead. No schedule-free fallback or general damage source is implemented.

## Connected host

The explicit `SharedCombatFixture` selects schema14 in `TestOnlySharedWorldPolicy`. Schema13 remains available with its original constructor and behavior. Supplied facts are a fixed two-participant calendar, one required hostile, finite grid/terrain and one independent companion at the plot. This supplies no general encounter generator, AI, initiative acquisition or content eligibility.

- First entry preserves position, exact rational movement expenditure, paid Dash, Action, Reaction and calendar identity. Grid-anchor entry is admitted; an actor with any pending exploration edge cannot be snapped into combat. An authored hostile approach triggers entry at the current anchor before the requested departure or its cost.
- Tactical decisions pause the shared clock. End advances only to the next scheduled boundary. Existing Club/unarmed attacks, stances except Mobile, standing, tactical steps, Disengage, OA, Press and knockout continuations use the shared spending records and existing resolvers. Exact fractional exploration costs remain exact after tactical steps.
- Participant intake interrupts with actual consumption retained. Participant crop/fill work pauses with progress and its source-specific reservations retained. Compatible remote work continues with elapsed slot time. A remote companion is neither an attack target nor a tactical actor merely because it belongs to the expedition.
- Pending OA, Press or knockout choices prevent ending or exiting. Resolved exit requires the required hostile Dead, completes only the outgoing slot, revalidates closure, then returns to exploration. It awards no remaining round or reward and preserves already processed consequences. Unconscious or Stable does not meet this predicate.
- Exit and reentry keep the same encounter and calendar identity, without a closed archive or reset. A legitimate incoming Start during exit may refresh its actor; the outgoing actor's spending is retained. Later mode entry performs no additional refresh.
- Restore reconstructs actual commands and compares complete canonical snapshots, including reservations, nested work, life, conditions, random state and pending choices. This establishes admitted procedural consistency; it is not cryptographic save authentication.

## Evidence and remaining scope

The full connected regression starts companion planting, explores into an actual battle, resolves damage and death, exits, continues exploration, grows and harvests Camp Greens, acquires and consumes food, saves/loads, then explores again. Separate disk cases preserve day-seven entry and an unpaid OA continuation. The bounded loop does not generate loot or a reward by defeating the hostile.

Explicit gates remain for continuous Mobile's first-five-foot entitlement, off-grid combat entry and bodily/drop geometry, simultaneous hostile traversal, changed rosters, genuine later encounters, general source acquisition, arbitrary content, new remote management commands during tactical control, and synchronous handling across condition deadlines. Histories retain their existing finite capacities. Unity is deferred under the owner's C#-first direction. This connected prototype is not the complete engine or a release-approved game.
