# Proposed prototype rules — owner decision required

Prepared through the owner-requested discussion in [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206). Captured response `2d36a873-aa5c-5ac3-9f30-cf00137cf6bb`,2026-11-03. **None of the new mechanics below is adopted or implemented.** Existing canonical/reviewed procedures retain their scopes. This document is a proposal, not a competing rule registry.

Codex assessment: the shared-clock and per-procedure work architecture is supported. The new pace/pause policy and farming figures are concrete prototype choices that require the owner. The jump formulas resemble familiar RPG conventions and are not recovered Decennium rules; they must not be adopted merely because they are familiar. Authored traversal routes remain a valid alternative for the first prototype. Farming still requires explicit event behavior at care/failure/harvest boundaries before implementation; the proposed numbers have no balance certification.

**Recommend one prototype approach: real-time exploration with explicit pause, continuous state when entering turn-based combat, bounded traversal, and one small tended crop.** Continue the independent C# work while Chris considers these product choices.

I rechecked the pinned sources, environment reconnaissance and supplied rulebook. The precedents support shared time, finite resources and active versus passive work; they still do not supply a complete ordinary farming procedure.

Here, **source-backed** includes reviewed playtest amendments within their existing gates. **Engineering choice** describes representation. **NEW proposal** requires Chris’s decision.

**A. Exploration clock, pause and initiative**

**Source-backed:** [Expedition FL-03](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-03) establishes one elapsed clock. [Combat timing](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#time-and-event-ordering--new) preserves absolute deadlines and original duration markers across initiative changes.

**NEW recommended policy:**

- Unpaused local exploration advances **one game second per real second**. Standing still also advances time.
- In solo play, explicit pause, inventory, map and dialogue choices pause the **whole simulation**, including companions and crops. Activities selected through those interfaces still consume their declared game time.
- Tactical decision-making pauses the simulation. Committed resolution advances it; a complete ordinary round accounts for **six seconds once**, regardless of participant count.
- Wait, rest and travel may fast-forward the same clock. Stop at an encounter, required decision or blocked assignment; process intervening milestones chronologically.
- No progress based on time spent outside the application.
- For eventual co-op, personal menus do not pause everyone; a host-controlled shared pause does.

**Engineering recommendation for initiative mapping:** freeze exploration at its exact timestamp and positions, establish ordered initiative, then assign evenly spaced initial start/end checkpoints across the six-second round. These are resolution checkpoints, not different action durations. Preserve already-created markers when the schedule changes. Process elapsed deadlines between checkpoints rather than postponing everything to round end.

The checkpoint allocation is a proposed scheduling convention—not a recovered rule. Preserve pending traversal and already-paid costs through the transition; no position snapping, extra movement or restarted effects.

**Tradeoff:** movement-only time would allow indefinite free observation while standing still. Accelerated exploration time would make watches pass faster but could expire short effects during very little actual movement. Start at 1:1 and use explicit fast-forward.

**B. Direct movement and contextual digging**

**Source-backed:** the [movement ledger](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#movement-and-geometry) supplies Speed, Dash, terrain expenditure and the five-foot tactical metric. Spell-specific traversal and the provisional Falling bridge remain controlling within their scopes.

**NEW recommended baseline:**

| Interaction | Proposed prototype behavior |
|---|---|
| Walk/run | Walking pace is current walking Speed divided by six, in feet/second. Running uses one ordinary Dash: twice that pace on normal ground and commits the corresponding Action budget. It supplies no extra attack or work allowance. |
| Jump | With ten feet of continuous run-up, maximum horizontal distance is STR score in feet; maximum upward jump is `max(0, 3 + STR modifier)` feet. Standing jumps halve those limits. These are **new strength-scaled defaults**, not recovered Decennium numbers. |
| Jump execution | Choose a reachable landing point, validate the full traversal and clearance, and charge its movement through the shared ledger. The decorative animation arc adds no movement charge or obstacle immunity. Ordinary feasible jumps need no roll; hazardous routes require a declared check and consequences. Preserve an interrupted jump’s state. |
| Climb | Ordinary climbing requires a physically climbable route and usable anatomy. Without a dedicated climb Speed, add one movement-cost foot per foot climbed. Ceilings and unsupported surfaces require an actual feature or equipment procedure. |
| Swim | In calm water, without a dedicated swim Speed, add one movement-cost foot per foot swum. Dedicated modes use their actual Speed. Breathing, buoyancy, burden and hazardous currents remain separate requirements. |
| Dig | Only identified dig sites with a finite target, tools, labor requirement, hazards and resulting world change. No universal terrain-removal rate. |

The ordinary swim surcharge has a precedent in **EF-06**, but that [environment model remains unadopted](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/docs/audit/2026-10-08/full-game/environment-foundations-local-draft-01/MODEL.json). Selecting that surcharge would be a new adoption; it would **not** adopt the draft’s sinking, currents or rescue rules automatically. First-slice water should have calm conditions and accessible exits.

For one concrete **NEW dig-site profile**, use a shallow buried cache: one capable worker, a compatible digging tool, **five active minutes**, no check under safe conditions, and retained partial progress after interruption. Completion exposes the existing cache. It creates neither mining yield nor a tunnel.

That remains distinct from [exposed-deposit mining](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md#choose-the-procedure).

**Tradeoff:** authored jump/climb/swim links would be quicker to deliver and easier to constrain, but offer less direct movement freedom. Unrestricted excavation would require a separate terrain, structural-support and resource-generation system. Neither is necessary for this prototype.

**C. Smallest coherent farming procedure**

**Source precedents:** [FL-04/06](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-04) distinguish physical food from a complete Supply basket and require finite site accounting. [Trap fishing](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_RECIPE_PLAYTEST.md#the-one-shot-unattended-trap) demonstrates active setup, passive elapsed time and later active retrieval. Those are precedents for structure, not permission to reuse their yields or durations.

**NEW proposed crop profile: “Camp Greens.” Every farming number below is a balance proposal, not sourced agronomy.**

| Part | Proposed rule |
|---|---|
| Identity/site | One crop batch occupies one **10 × 10 ft** prepared plot. Record crop, seed-lot and plot IDs, ownership, suitable soil, light, water access and valid growing-season window. |
| Planting | **One active hour**, compatible tools, one **0.1 lb seed packet**, and **eight pints of suitable water**. Commit inputs when work begins; growth starts when planting finishes. |
| Passive growth | Matures after **168 hours of suitable, cared-for growth**. No worker is committed during passive growth. |
| Tending | Planting supplies the first **24 hours** of care. Each later tending task takes **15 active minutes** and eight pints of water, supplying care until 24 hours after completion. Care cannot be stockpiled by repeatedly tending early. |
| Missing care/conditions | Growth pauses while requirements are unmet. After **48 continuous hours** without suitable care/conditions, that crop fails. Restoring conditions earlier resumes retained growth. |
| Harvest | One active hour produces a fixed **eight pounds of ordinary edible food**, once. No random yield, rare reagents, automatic seeds or whole Supply baskets. |
| Maturity/freshness | Harvest must finish within **48 hours of maturity**. Harvested produce has a proposed **48-hour freshness clock beginning with the first harvest work**; interruption or repacking does not renew it. A compatible reviewed preservation procedure may change its subsequent handling. |

Why these numbers: seven days makes farming observable within the hundred-day Opening; eight pounds represents four Small/Medium food-days under existing accounting; short tending creates a useful recurring companion assignment without occupying the worker all day. Yield and water demand still need balance testing.

Additional proposed semantics:

- Planting, tending and harvest retain completed active progress through interruption. Spent inputs remain spent; reserving inputs is separate from spending them.
- Assignment cancellation releases unspent reservations and the worker. It does not erase planted crops, reverse consumption or freeze growth.
- Workers are reserved only for actual labor and travel intervals. Independent expedition companions may perform those jobs; summons gain no new farming entitlement.
- Harvested food appears at the plot’s receiving location. Transport is separate.
- Season changes do not reset plots or grant harvests. They change actual site eligibility; unsuitable conditions follow the same pause/failure rule.
- Saving preserves batch identity, committed inputs, growth, care deadline, interruption progress, maturity/freshness deadlines and harvest receipt. Reload neither advances offline time nor repeats output.
- Druidcraft supplies no farming shortcut; other magic requires its exact applicable procedure.

**Tradeoff:** a Haven-only farming service would be simpler but provide less meaningful companion/world interaction. Longer seasonal crops would support deeper settlement play but delay feedback substantially. Start with this single crop before adding fertility, diseases, variable quality or seed reproduction.

The concrete decision for Chris is whether to adopt **this prototype clock/pause policy, traversal baseline and one-crop profile** as labeled provisional mechanics. The recommendation itself approves none of them; marker/deadline and worker/reservation infrastructure can continue independently.
