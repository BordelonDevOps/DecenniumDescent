# Player expedition procedures — routes, extraction and retreat

Working chapter module 2. Together with part 1, eighteen of the 58 source directions are drafted. Full transport profiles, Haven, social and reputation chapters remain to assemble before exact review.

Use this with [part 1: organization, time, provisions and camps](EXPEDITION_PART01_PLAYER.md) and the current [Core resolution](../CORE_RESOLUTION_PLAYTEST.md) rules.

## Pressure follows the expedition’s real exposure

Pressure is an integer from 0 to 6 for the actual group travelling or camping together on a route. Its source state names are:

| Pressure | State |
|---:|---|
| 0 | Secured; no routine complication roll |
| 1 | Watched |
| 2 | Unstable |
| 3 | Hostile |
| 4 | Hunted |
| 5 | Overrun |
| 6 | Immediate crisis |

At an active Watch's end, add +1 for each applicable category: open combat/explosion during that Watch; exceeding route Capacity; a missing/captured member or active pursuit; continuing after an agreed abort trigger; and actually using an exposed camp or one known to enemies. Several attacks are one open-combat increase, and several descriptions of the same cause do not multiply it. Different genuine categories can add together.

Attention cargo instead adds +1 for each actual lot's first exposed carriage, newly revealed concealment loss, or genuine re-exposure after concealment was restored. Continuous unchanged exposure does not add another point every Watch. Splitting containers, changing owners or re-entering a route does not renew the cause. Its exposed state can still affect an Extraction Test.

Qualifying Counter-Ambush, a genuine move onto a secured route, a full Watch lying low in a concealed camp, or a completed settlement ending pursuit can each earn −1. The group can receive at most two reduction credits per Watch, including reconnaissance and extraction-critical reductions. Conceal Trail cancels one actual pursuit increase; it does not remove all pursuit or grant an additional free −1. Apply real increases and allowed reductions once, then keep Pressure between the current route's Risk floor and 6. An actually Secured route permits a floor of 0.

Process routine complications once per active Watch. Safe inactive Rest alone produces no routine roll, though real raids and hazards can still happen. At Pressure 6, the due checkpoint produces one Severe complication.

When the group genuinely leaves its last exposed route for safe Haven during a Watch, settle any unprocessed exposure checkpoint at that boundary using causes accrued so far. Do not repeat it at the later Watch end or place a route patrol inside Haven. Safe arrival preserves history; it does not itself set Pressure to 0 or refill resources.

## Complications have a declared cause and a finite response

At Pressure 0 there is no routine complication roll. At Pressure 6 resolve one automatic Severe complication. At Pressure 1–5 use the final lawfully selected natural d6 face n and its final modified total r:

1. If r is greater than Pressure, no complication occurs.
2. Otherwise, a final natural 1 gives Severe.
3. Otherwise, if r equals Pressure and an actually applied modifier or reroll produced that final equality, give Minor.
4. All other triggering results give Standard.

This rule grants no modifier or reroll. A natural 1 modified above Pressure does not trigger. Modified totals can be outside 1–6; do not clamp them. With no modifier or reroll, the full ordinary table is:

| Pressure | Natural 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|
| 0 | None | None | None | None | None | None |
| 1 | Severe | None | None | None | None | None |
| 2 | Severe | Standard | None | None | None | None |
| 3 | Severe | Standard | Standard | None | None | None |
| 4 | Severe | Standard | Standard | Standard | None | None |
| 5 | Severe | Standard | Standard | Standard | Standard | None |
| 6 | Automatic Severe; no die | — | — | — | — | — |

Before checking, establish compatible real stakes. A Minor complication is a 15-minute access/inspection delay or exposure of one actual concealed lot. Standard is a 60-minute obstruction/detour or one actual low-priority unsecured lot placed at risk. Severe is an actual encounter, forced evacuation, route closure, or severe cargo/casualty hazard with a declared resolution. No result invents an enemy, damage, curse or valuable debris.

A successful Patrol can reduce the next actual camp complication one tier—Severe to Standard, Standard to Minor, Minor to none—once, when its warning physically applies. It cannot undo an independent attack already resolved.

## Route travel and mapping

Record the route's directed endpoints, finite Length in Progress, Risk, Mapping, Capacity in Load, actual Sustenance opportunities, clearance and permitted travel methods. Mapping is what you know about the passage. Route quality describes its actual physical/security condition; they are separate.

One travel segment represents **480 nominal minutes of route effort**. Its elapsed moving time is:

`480 minutes × route-quality factor × (3 ÷ current convoy pace in mph)`

| Route quality | Time factor |
|---|---:|
| Secured | 3/4 |
| Known | 1 |
| Contested | 5/4 |
| Collapsed | 3/2 |

The new ordinary reference is 3 mph for fit, unburdened walking Speed 30. Other lawful walking/mount paces use current Speed ÷ 10 mph; vessels use their specific travel profiles. The slowest necessary self-moving member or vehicle limits the convoy; passengers use their carrier. Apply actual environment, Load/Speed and the expedition-Strain-5 slow-travel rule once each where applicable. Strain 5 halves otherwise legal travel once after the other applicable restrictions. Repeated tactical Dash does not create free continuous overland speed.

At completion, the segment's starting Mapping gives 2 Progress for Mapped/Secured, 1 for Sketched, or 0 for Unknown until successful reconnaissance makes that actual traverse feasible, then 1. Unknown or severely obstructed passages need actual successful reconnaissance or a resolved forced march before ordinary advancement. Compatible moving reconnaissance/escort can share a traverse; stationary research or crafting does not move it.

A reconnaissance success can add one shared +1 Progress OR −1 Pressure; a critical can do both. All teams together get at most one such Progress bonus and one such reduction for that group/segment. Successful Map Route also earns one mapping mark, or two on a critical. After max(1, recorded Risk) marks, consume them to improve Mapping one step. New Mapping normally affects the next segment. Unknown travel made feasible by its own reconnaissance gets the permitted base 1, not a retroactive base 2. A Risk-0 Secured route has no further mapping level or reward.

If total convoy Load exceeds route Capacity, subtract 1 Progress once from the completed segment, minimum 0, after allowed base/bonus Progress. Its corresponding Pressure increase is also charged once. This route penalty never permits an individual carrier to exceed its own hard limit.

Progress refers to real traversable sections. You cannot cross a closed bridge, carry an oversized boat through a tunnel or relocate a stranded member by changing a number. A map purchase provides only its actual content and verified rating. Reverse travel can reuse observed geometry, without guaranteeing unchanged currents, slopes, guards or one-way access.

## Forced march and interrupted travel

A forced march is the expedition procedure for attempting Unknown-route travel before mapping is complete. Declare one 480-nominal-minute attempt, with actual travel time adjusted by the route formula. Record participants, feasible transport and extra provisions before starting. The Routekeeper—or the actual permitted capable lead—uses the appropriate route skill, normally WIS (Survival), at **tier DC +6**. Use the generic trained-assistant limit unless an exact source overrides it.

| Task result | Outcome |
|---|---|
| Success or Critical Success | 1 Progress, +2 Pressure, and the actual extra support cost below |
| Failure | No Progress; one Standard complication |
| Critical Failure | No Progress; one Severe complication |

Reserve an additional complete provision basket for each active Small/Medium participant, or two for Large. A successful attempt consumes those extras once for its actual support; real nutrition consumption can credit daily needs once. There is no extra generic critical reward. An expected stock shortage blocks a voluntary attempt before commitment. A specific dietary exemption waives only its actual components, without generating transferable surplus.

On failure, return only genuinely unspent extras. Anything actually consumed or lost during the attempt remains spent. A roll creates no missing transport capacity, suitable route or safe geometry; revise, split or withdraw an infeasible group before starting.

Combat, blocked passages and rest pause unfinished travel and consume their actual minutes. Resume the same unresolved attempt if feasible. A resolved failure cannot be rerolled by renaming it; a materially different method/route requires a new real time/resource commitment. Scheduled Rest and Rest Debt continue. A character at expedition Strain 5 cannot lead this active check; lawful carrying and the actual slow-travel exception remain available.

## Starting extraction and admitting cargo

Extraction begins with a genuine decision and movement toward a real Haven/surface destination. Inventory lots, people, casualties, vehicles and provisions. For each cargo lot record identity, owner/custodian, pounds, Load, Extraction Class, priority 1–5, condition, carrier and relevant tags. Before outcomes, the Quartermaster or Leader resolves priority ties; the lowest-priority appropriate lot is put at risk first.

Extraction Class is handling danger and attention, not mass, title or a promotion in rarity:

| Class | Source examples |
|---:|---|
| 0 | Ordinary trade goods |
| 1 | Common monster parts or durable salvage |
| 2 | Uncommon, fragile or regulated cargo |
| 3 | Rare artifacts, volatile substances or living captives |
| 4 | Very rare strategic cargo or dangerous curses |
| 5 | Epic cargo likely to draw sovereign/faction intervention |
| 6 | Legendary cargo requiring a dedicated extraction operation |

Keep actual Fragile, Volatile, Cursed, Living, Contraband, Perishable and Attention tags. A voluntary passenger is not automatically a Class-3 captive. People retain agency, care needs, legal status and actual consent/restraint facts. A classification grants no authority to bind or own someone.

At extraction's start add Pressure equal to **min(3, floor(highest carried Class ÷ 2))** once. Keep the episode's highest charged surcharge. Acquiring higher-Class cargo later adds only the positive difference; dropping or concealing it refunds nothing. Transferring allied cargo, changing transport or renaming the episode cannot renew or erase that history.

Secure, hidden and medically/chemically safe are different facts. [Secure Cargo](../BODY_EQUIPMENT_PLAYTEST.md) spends an Action on one feasible handling/protective operation. It supplies no free whole-convoy restraint, automatic success, capacity or lowered Class. A concealed volatile core still needs its real containment. Admit Class-6 cargo only with its declared dedicated handling and route operation.

## Extraction checkpoints and checks

At route entry, record a finite ordered set of real checkpoint positions using the Mapping governing that traverse:

| Mapping | Checkpoints |
|---|---|
| Secured | Genuine route transition/exit |
| Mapped | Midpoint and exit for Length at least 6; otherwise exit |
| Sketched | Each positive multiple of 3 below Length, and exit |
| Unknown | Each positive multiple of 2 below Length, and exit |

Fractional midpoints stay exact. A later mapping improvement changes only future cadence and preserves all processed positions. Combine overlapping exit, midpoint, route-transition or multiple-based requests at the same real position/time into one test with all reasons. Changing the name of the same carriage is not a transport transition. A route exit and next entry at the same transfer point share one state test unless a distinct later operation intervenes.

The Quartermaster or a designated capable substitute makes the check using an actual ability modifier, one relevant Survival/vehicle/tool proficiency, and meaningful permitted assistants. Its DC is:

`tier DC + min(7, highest Class + exposed Attention + Burden + min(3, unsecured dangerous lots)) + pursuit − Secured`

Exposed Attention is +1 once if applicable; Burden is +1 once if the actual convoy is Burdened. Count each unsecured Volatile/Cursed/Living lot once even if it has several such tags. Active pursuit adds +2 outside the +7 cap; a Secured route subtracts 2 outside it. The tier DCs are I 12, II 13, III 15, IV 16, V 18 and VI 19. Use Core task degrees and natural shifts.

| Result | Outcome |
|---|---|
| Critical Success | Pass and choose −1 Pressure within the Watch reduction limit, or +1 Progress along an actually reachable compatible onward section |
| Success | Pass |
| Failure | Choose the declared eight-hour delay plus Standard complication, or the stated low-priority lot at risk |
| Critical Failure | Severe complication plus the predeclared two lots, one vehicle or one casualty at risk |

An ordinary check requires **one active minute** of actual convoy/route/receiver verification by the lead and assistants, with necessary hands, tools and access. It fits within travel only when that compatible moving workflow was declared; otherwise stop and add the minute. An exact longer procedure controls its own operation, with no extra generic minute added to already completed exact verification.

## A failed extraction test creates a choice and a real problem

Before the test, the Director states the physical cause, real stakes, affected low-priority cargo/vehicle/person and feasible responses. On Failure, players choose an **eight-hour elapsed delay plus one Standard complication**, or one stated low-priority lot at risk. Critical Failure brings one Severe complication and the predeclared two lots OR one vehicle OR one casualty at risk. “At risk” does not mean automatic destruction, death or transferred ownership. Do not invent another lot or casualty when none exists.

The delay occupies 28,800 actual seconds. Record who must work, guard or handle the obstacle. The stalled convoy earns no Progress for that interval. Others may perform feasible independent activities, including genuinely safe uninterrupted rest, but the failed check does not certify safety. Food, water, protection, Rest Debt, Pressure and rival clocks continue at their real endpoints. This is eight hours once, not eight hours plus another Watch.

The default noncombat cargo response is a **60-active-minute securing/recovery task**, using a capable lead, necessary helpers/rigging and tier DC plus the affected lot's Class, capped at +6. A more specific real source controls instead. Success or Critical Success secures the reachable lot without extra loot, Progress or HP. Failure leaves the lot at its declared reachable stranded/abandoned position or applies its declared compatible hazard once. It does not universally destroy it.

If seconds matter, use actual combat movement, Secure Cargo, attacks, falls and rescue Actions instead of the hour abstraction. Voluntarily leaving a lot changes custody/location while preserving title/claims and insurance exclusions. Later retrieval is a new actual rescue against that position, not a replayed extraction award. Insurance does not replace a merely threatened item.

## Retreat without restarting the encounter

Declare Retreat at the start of an actual round when a plausible escape route exists. Keep the same encounter, numbered rounds, positions, conditions, pursuit actors and spent resources.

Once per round, one withdrawing lead spends its Action on a fixed-DC escape task using its real method. Begin at route tier DC. A declared superior pursuit/obstruction adds +3, a severe version +6, or actual favorable preparation subtracts 3. Use the Core four task degrees and natural shifts. An exact source can provide a distinct opposed chase instead; do not make both checks for the same uncertainty.

| Lead result | Counter gained |
|---|---|
| Critical Success | 2 Escape |
| Success | 1 Escape |
| Failure | 1 Pursuit |
| Critical Failure | 2 Pursuit |

An independently achieved declared round objective, actual sacrificed cargo or blocking maneuver can supply 1 Escape instead of the ordinary lead success. It does not add another generic point. Generic Escape is capped at 1 per round, or 2 when the actual lead critical supplies 2. Losing a real member, route or vehicle can add 1 Pursuit when declared as a consequence; generic Pursuit is capped at 2 per round. Express paid features retain only their exact point permissions.

Each round includes one predeclared meaningful opposing threat: a legal attack, actual hazard or necessary sacrifice. It does not add a full enemy multiattack/nova to another chase punishment. Allies use their real Actions to Help, carry, treat, cast, command, move or create obstacles; they do not make extra lead checks. Combat Help keeps its actual advantage and expiry rules.

Resolve that round's costs, threat and check once, then compare totals. **Escape at least 3 with Pursuit below 3 succeeds. Pursuit at least 3 fails, including simultaneous 3/3.** Success returns to Expedition Mode with +1 Pressure, actual survivors/cargo and pursuit history. RP, recharge and encounter-use resources do not refresh. Failure gives the opponent its actual advantageous next position or capture opportunity; it does not automatically kill everyone or assign ownership.

## Estimate encounters from actual participants

The Expedition roster is not the encounter's participant count. Track who is actually present, participating and able to contribute under their real action/command rules. Reinforcements enter at their actual times; they do not silently grant another unopposed wave.

Encounter budgets are provisional planning estimates, not promises of survival or measured balance. Establish objectives, terrain, exits, cargo, civilians, hazards, starting distance and surprise, then use the current combat rules. Cargo protection, escort and retreat require their own stated success conditions rather than only a kill count.

Boss Tenacity applies only to a declared source-qualified boss with its actual allowance. Size, cost or an encounter budget does not confer boss status. Use [current control/condition rules](../CONDITIONS_PLAYTEST.md), including exact source counters, replacement and duration. Fear, Reaction denial and ordinary Speed penalties are not interchangeable with full-turn denial.

## Transport admission preserves every body and item

Before a move, validate all of these separately:

- The actual body, control permission and current movement/conditions.
- Physical route space, clearance and fit.
- Pounds, including supported living bodies and all their associated gear.
- Load, storage volume and real seats or cargo positions.
- Required crew, pullers, propulsion and their actual work.
- Legal custody and continuing item/effect clocks.

A container contributes its own empty body and each child once. A printed inclusive gross weight/Load covers only its stated contents. Keep pounds and Load distinct. A passenger's melded equipment still burdens an external carrier. Extraction Class changes the handling problem, never the carrier's capacity.

Use the [body/equipment procedure](../BODY_EQUIPMENT_PLAYTEST.md) for real mass, inventory Burden and casualties. With positive carried Load at or above half capacity, and no greater than capacity, the carrier is Burdened; empty inventory is not Burdened even at zero capacity. Hard physical and inventory limits still apply. Vehicles, mounts and their particular sources keep their own completed profiles.

Melding, petrification, changing vehicles, a sale, a service quote or renaming a record cannot restore missing cargo or spend another copy. A transport catalogue does not provide a living mount, available crew, actual route or unacquired feat.

## Durability, old Integrity records and repair

Use actual structural HP for modeled equipment, fixtures and transport bodies. The old 0–3 Integrity track is not another damage pool, and its old Integrity-1 penalty does not automatically apply to a functioning positive-HP item. Keep actual grade, quality, flaws, constituents and custody. Living mounts use living HP and conditions, not structural repair.

At zero structural HP, an object is Broken under the [equipment rules](../EQUIPMENT_ACQUISITION_PLAYTEST.md). It still exists with mass, occupied space and physical drawbacks until actually removed or repaired. A missing wheel or other true primary constituent can make a vehicle incomplete even with positive aggregate HP. Inventing a cheap “pin” target does not disable a whole structure.

Ordinary self-repair requires a relevant trained toolkit and real compatible material worth **25% of the item's proper size/grade baseline**. Spend **max(1 hour, maximum structural HP ÷ 10 hours)** of active work and make the appropriate DC 10 tool task. Collapse Core degrees to success/failure: success restores maximum structural HP; failure spends time/materials and a new attempt needs fresh payment. A critical supplies no extra generic benefit. Repair at zero HP requires the recoverable main body.

An eight-hour Repair Watch is eight hours of available work, not eight completions. A 300-HP mundane vessel needs 30 active hours under this profile. Magical recipe bodies retain their exact functional/Broken bridge, prices, primary identities and persistent flaws. Repair does not recreate missing items, passengers, doses, ammunition, burnt pages, fuel, charges, class gauges or a terminal dismantled source.
