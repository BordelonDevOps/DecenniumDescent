# Prototype rules — owner decisions and original proposal

**Owner decisions received 2026-11-03:** Chris answered “Adopt this clock policy,” “Adopt the proposed traversal rules,” and “Adopt Camp Greens provisionally” to the three concrete questions recorded below. These are new owner-approved prototype policies, not recovered Decennium rules, release promotion or balance certification. Unity remains deferred until the C# work is ready.

| Decision | Approved scope |
|---|---|
| Clock | 1 game second per real second in exploration; solo pause, menus and dialogue pause the whole simulation; tactical decisions pause; one complete combat round advances six seconds total; wait/rest fast-forward; no offline progress. |
| Traversal | Run at twice walking pace using Dash; ten-foot run-up permits horizontal jumps up to STR feet and vertical jumps up to `max(0, 3 + STR modifier)` feet; standing jumps halve limits; ordinary climb/swim adds one movement foot per foot. |
| Camp Greens | The linked full one-crop profile below, provisionally: 10×10-foot plot, one hour planting, seven days of suitable growth, fifteen-minute tending with eight pints, one hour harvest and eight pounds food, including its specified inputs, interruption, failure and freshness behavior. |

The clock question did not select initial initiative phases or cooperative pause semantics. The traversal question did not adopt the proposed five-minute dig-site recipe or the rest of the environment draft. Camp Greens boundary ordering at maturity/care/harvest and disposition on failure still require an explicit specification; Codex sent those remaining questions to **Unity Rules Engine Development** after recording these approvals. Proceed with independent approved mechanics while resolving these details. No earlier negative status in the preserved proposal below overrides these later owner decisions.

Prepared through the owner-requested discussion in [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206). Original proposal response `2d36a873-aa5c-5ac3-9f30-cf00137cf6bb`, 2026-11-03. The following is retained as the original proposal; its request-for-approval wording is historical. Implementation and test status belong in the development handoff and trace, not this product decision receipt.

---

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


## Follow-up boundary proposals — awaiting owner decision

GPT response `76afe920-a4ea-5bd5-a2b4-4619d56b0f40` acknowledged all three approvals and supplied the following remaining specifications. These are explicitly proposed completions, not yet adopted. The approval above continues to govern the already specified mechanics.

### Camp Greens boundary and failure completion

- Credit eligible growth and active labor over the elapsed interval before resolving its endpoint. No rounding into completion.
- Growth reaching 168 hours exactly at care expiry earns maturity; tending finishing exactly at care expiry renews care without an uncovered interval. Growth earned before a season becomes unsuitable is retained.
- At 48 continuous hours of unsuitable conditions or missing care, failure wins over recovery at that same timestamp. Recovery must be strictly earlier.
- After maturity, daily growth care stops; the fixed 48-hour harvest window controls. Tending cannot extend it. Cancel future unnecessary tending but preserve spent inputs and labor.
- Harvest completion exactly at maturity plus 48 hours is timely. Freshness ends at its exact deadline; an output already at its freshness deadline grants no edible food.
- An incomplete harvest at its deadline fails without proportional food. Partial harvest is labor progress, not inventory.
- Tending water is consumed at the first active work; care renews only on completion. Spent seeds/water/labor are not refunded. Release unspent reservations and unused future worker bookings, preserving physical tool/supply locations and history.
- Failed crops remain recorded as nonharvestable biomass at the plot, granting no automatic food, seeds, compost, crafting materials or sale value. Clearing an ordinary failed crop is included in the next planting's existing one-hour task, with new inputs and a new batch ID. Retain the failed batch record.
- A successful harvest closes the crop and creates its once-only output lot separately. Later cleanup cannot remove or duplicate the output.

Example: harvest starts at maturity M, but interruptions delay completion to M+48 hours. It meets the harvest window; freshness also expires then, so it awards zero edible food. Preserve the terminal disposition rather than granting a briefly usable edible lot.

These crop-local priorities do not override separately sourced destructive hazards or define a universal event ordering rule.

### Initial initiative checkpoint allocation

For N initial actors in established initiative order, at encounter start T0:

- Actor i starts at T0+6i/N and ends at T0+6(i+1)/N.
- At a shared boundary, finish the outgoing slot before starting the incoming slot.
- Preserve existing absolute deadlines and already captured virtual markers.
- For three actors, the first-round windows are 0–2, 2–4 and 4–6 seconds. They are scheduling checkpoints, not different action durations.

This proposal is limited to initial allocation. Joining/leaving/reordering participants still requires a separately specified future-schedule policy; existing duration markers may never be rewritten by it.
