"""Author EX58 FL-08..18 as readable partial chapters; no runtime/approval claim."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from fractions import Fraction
import json
import math
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'ex58-final-gpt-verdict'

def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}
def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

SECTIONS = []
def section(i, title, player, director):
    SECTIONS.append({'id': f'FL-{i:02d}', 'title': title, 'player': player, 'director': director})

section(8, 'Pressure follows the expedition’s real exposure',
'''Pressure is an integer from 0 to 6 for the actual group travelling or camping together on a route. Its source state names are:

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

When the group genuinely leaves its last exposed route for safe Haven during a Watch, settle any unprocessed exposure checkpoint at that boundary using causes accrued so far. Do not repeat it at the later Watch end or place a route patrol inside Haven. Safe arrival preserves history; it does not itself set Pressure to 0 or refill resources.''',
'''Maintain one parent Expedition, shared clock and stable physical cause/Watch IDs. Separated groups can have different real exposure. Splitting grants neither a new Pressure pool nor a reduction; on merging use the greatest current Pressure, retain all causes/deadlines and apply the destination floor. An unrelated Expedition does not erase shared pursuit or cargo histories.

Keep continuing Watch causes separate from discrete Attention, forced-march, retreat and extraction-surcharge events. Forced march adds its +2 once; successful retreat its +1 once. A second textual description is not a second charge. Each allowed reduction has a unique source; blocked reduction below the floor is logged, not stored for later. Base Risk is 1–5, with the explicit new completion allowing an already Secured Risk-0 profile; do not infer zero risk otherwise.

A Watch is active when it contains actual expedition travel, work or exposure-bearing activity. Pressure 6 is evaluated at the due checkpoint after the applicable signed batch, not on every intermediate arithmetic value. Immediate real hazards keep their own timestamps.

For partial-Watch safe exit, close that actual exposure's Watch/cause membership once. A later genuinely new exposure uses its real remaining interval and causes, without resetting earlier ones. A later descent retains relevant unresolved Pressure/pursuit history and the new route floor; only an actual qualifying reduction changes it.''')

section(9, 'Complications have a declared cause and a finite response',
'''At Pressure 0 there is no routine complication roll. At Pressure 6 resolve one automatic Severe complication. At Pressure 1–5 use the final lawfully selected natural d6 face n and its final modified total r:

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

A successful Patrol can reduce the next actual camp complication one tier—Severe to Standard, Standard to Minor, Minor to none—once, when its warning physically applies. It cannot undo an independent attack already resolved.''',
'''Select a finite compatible entry with its actual source before committing the check; replace an impossible entry before resolution, never after a successful response to defeat it. Modified/rerolled equality is the explicit replacement for the original impossible phrase “exceeds by exactly 0.” An untouched 3 at Pressure 3 is Standard; a legal −1 taking 4 to 3 is Minor; a final triggering natural 1 stays Severe.

Give each root Watch/checkpoint incident one causal ID. At one timestamp, merge duplicate requests for the same group and physical cause, keeping the highest severity and all reasons. Unrelated real incidents remain distinct.

A Severe complication during extraction can request one subsequent Extraction Test for its changed convoy, recorded as secondary to that root. A complication caused by this secondary test cannot request another test in the same causal batch. The finite route positions, root events and one permitted secondary per root bound the queue. Delays can reach genuinely later Watch/day events on the shared clock; those are new due events, not recursion at the old timestamp.''')

section(10, 'Route travel and mapping',
'''Record the route's directed endpoints, finite Length in Progress, Risk, Mapping, Capacity in Load, actual Sustenance opportunities, clearance and permitted travel methods. Mapping is what you know about the passage. Route quality describes its actual physical/security condition; they are separate.

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

Progress refers to real traversable sections. You cannot cross a closed bridge, carry an oversized boat through a tunnel or relocate a stranded member by changing a number. A map purchase provides only its actual content and verified rating. Reverse travel can reuse observed geometry, without guaranteeing unchanged currents, slopes, guards or one-way access.''',
'''Keep exact rational fractional Progress when shorter intervals are needed to locate crossed checkpoints; splitting a ledger creates no additional completion check or base award. Record position-to-Progress bindings and actual obstacles. Zero Length is a location record, not repeatable travel/reward.

Travel duration changes the same actual traverse; do not also award independent mileage or work-time credit. Genuine environment/quality/pace factors apply once, and the Strain-5 exception never halves again at a new Watch. Actual pauses add their real elapsed time. Section TR-13's full transport procedure still controls specific method changes and transfers.

Apply a route-quality encounter adjustment once in the final difficulty, only when that threat is not already represented. Route-quality cargo-loss rows are declared stakes under the failure-response procedure; they do not create a second automatic loss roll. Mapping marks and route-quality changes require their own real evidence; neither is inferred from the other.''')

section(11, 'Forced march and interrupted travel',
'''A forced march is the expedition procedure for attempting Unknown-route travel before mapping is complete. Declare one 480-nominal-minute attempt, with actual travel time adjusted by the route formula. Record participants, feasible transport and extra provisions before starting. The Routekeeper—or the actual permitted capable lead—uses the appropriate route skill, normally WIS (Survival), at **tier DC +6**. Use the generic trained-assistant limit unless an exact source overrides it.

| Task result | Outcome |
|---|---|
| Success or Critical Success | 1 Progress, +2 Pressure, and the actual extra support cost below |
| Failure | No Progress; one Standard complication |
| Critical Failure | No Progress; one Severe complication |

Reserve an additional complete provision basket for each active Small/Medium participant, or two for Large. A successful attempt consumes those extras once for its actual support; real nutrition consumption can credit daily needs once. There is no extra generic critical reward. An expected stock shortage blocks a voluntary attempt before commitment. A specific dietary exemption waives only its actual components, without generating transferable surplus.

On failure, return only genuinely unspent extras. Anything actually consumed or lost during the attempt remains spent. A roll creates no missing transport capacity, suitable route or safe geometry; revise, split or withdraw an infeasible group before starting.

Combat, blocked passages and rest pause unfinished travel and consume their actual minutes. Resume the same unresolved attempt if feasible. A resolved failure cannot be rerolled by renaming it; a materially different method/route requires a new real time/resource commitment. Scheduled Rest and Rest Debt continue. A character at expedition Strain 5 cannot lead this active check; lawful carrying and the actual slow-travel exception remain available.''',
'''Use the current Core fixed-DC task degrees and natural shifts, not attack or saving-throw rules. Ordinary route tier DCs retained from the source are I 12, II 13, III 15, IV 16, V 18 and VI 19; Severe adds 6. These numbers do not certify Tier VI content readiness.

Count the forced-march +2 once by its cause ID, even when a Watch summary also describes the march. Its extra basket commitment is distinct from an abstract daily Supply debit; actual components, consumers and remaining amounts are tracked under part 1. Retain costs, disturbances and partial progress across legitimate interruptions, with no stock refund for physically consumed material. Do not award another Watch just for reaching a segment endpoint.''')

section(12, 'Starting extraction and admitting cargo',
'''Extraction begins with a genuine decision and movement toward a real Haven/surface destination. Inventory lots, people, casualties, vehicles and provisions. For each cargo lot record identity, owner/custodian, pounds, Load, Extraction Class, priority 1–5, condition, carrier and relevant tags. Before outcomes, the Quartermaster or Leader resolves priority ties; the lowest-priority appropriate lot is put at risk first.

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

Secure, hidden and medically/chemically safe are different facts. [Secure Cargo](../BODY_EQUIPMENT_PLAYTEST.md) spends an Action on one feasible handling/protective operation. It supplies no free whole-convoy restraint, automatic success, capacity or lowered Class. A concealed volatile core still needs its real containment. Admit Class-6 cargo only with its declared dedicated handling and route operation.''',
'''Record the real episode, return destination, cargo lineage and surcharge high-water mark. Room re-entry, allied transfers and a new ID do not reset it. A genuinely concluded return followed by a new descent can begin a new episode, while unresolved original cargo retains condition, clocks and custody.

Reference each securing operation to actual harness/container/care/containment rules. Cargo priority chooses among real eligible stakes; it cannot create nonexistent victims or override legal status. Keep carrier admission separate from extraction risk: Class affects handling DC, not physical pound/Load limits or access.''')

section(13, 'Extraction checkpoints and checks',
'''At route entry, record a finite ordered set of real checkpoint positions using the Mapping governing that traverse:

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

An ordinary check requires **one active minute** of actual convoy/route/receiver verification by the lead and assistants, with necessary hands, tools and access. It fits within travel only when that compatible moving workflow was declared; otherwise stop and add the minute. An exact longer procedure controls its own operation, with no extra generic minute added to already completed exact verification.''',
'''Use actual route-position IDs, not only displayed Progress numbers. Resolve each finite routine checkpoint at most once. Extra Progress queues newly crossed positions in order after the current test; it does not recursively resolve them inside an unfinished result. Exit is not passed until its required final test is resolved. No new room/route IDs can be invented to manufacture critical Progress.

A real Severe complication that changes convoy state can request one test at a previously checked position under the root/secondary limit. Retain all coalesced reasons, distinct actual operations, and pending queue state.

Calculate Burden from actual occupied transport and its correct thresholds; duplicating a body/container record cannot change it. Verification work is real labor, not passive carriage, a free off-turn Action or a ledger update. The DC cap groups only Class, Attention, Burden and unsecured dangerous lots; pursuit and Secured remain outside it.''')

section(14, 'A failed extraction test creates a choice and a real problem',
'''Before the test, the Director states the physical cause, real stakes, affected low-priority cargo/vehicle/person and feasible responses. On Failure, players choose an **eight-hour elapsed delay plus one Standard complication**, or one stated low-priority lot at risk. Critical Failure brings one Severe complication and the predeclared two lots OR one vehicle OR one casualty at risk. “At risk” does not mean automatic destruction, death or transferred ownership. Do not invent another lot or casualty when none exists.

The delay occupies 28,800 actual seconds. Record who must work, guard or handle the obstacle. The stalled convoy earns no Progress for that interval. Others may perform feasible independent activities, including genuinely safe uninterrupted rest, but the failed check does not certify safety. Food, water, protection, Rest Debt, Pressure and rival clocks continue at their real endpoints. This is eight hours once, not eight hours plus another Watch.

The default noncombat cargo response is a **60-active-minute securing/recovery task**, using a capable lead, necessary helpers/rigging and tier DC plus the affected lot's Class, capped at +6. A more specific real source controls instead. Success or Critical Success secures the reachable lot without extra loot, Progress or HP. Failure leaves the lot at its declared reachable stranded/abandoned position or applies its declared compatible hazard once. It does not universally destroy it.

If seconds matter, use actual combat movement, Secure Cargo, attacks, falls and rescue Actions instead of the hour abstraction. Voluntarily leaving a lot changes custody/location while preserving title/claims and insurance exclusions. Later retrieval is a new actual rescue against that position, not a replayed extraction award. Insurance does not replace a merely threatened item.''',
'''Core route-quality loss rows become declared stake guides, not automatic inventory subtraction in addition to the chosen Loop failure branch: Known threatens one actual Load; Contested 10% of current carried Load; Collapsed 20% or a real reroute; Secured has no automatic routine cargo-loss row. Identify real whole lots or divisible portions, preserving indivisibility and actor safety.

Special Living/Changed or Pact Interdiction rows require their actual defined event/seizure/service permission. An absent profile supplies no invented power. Disabled vehicles and casualties use the complete transport-repair/rescue and physical/life rules.

Coalesce coincident duplicate complication requests by physical cause while retaining independent incidents. The response ledger names actual time, labor, resources, current location and realized damage/loss; an abstract risk flag is not proof of an insured loss or destroyed property.''')

section(15, 'Retreat without restarting the encounter',
'''Declare Retreat at the start of an actual round when a plausible escape route exists. Keep the same encounter, numbered rounds, positions, conditions, pursuit actors and spent resources.

Once per round, one withdrawing lead spends its Action on a fixed-DC escape task using its real method. Begin at route tier DC. A declared superior pursuit/obstruction adds +3, a severe version +6, or actual favorable preparation subtracts 3. Use the Core four task degrees and natural shifts. An exact source can provide a distinct opposed chase instead; do not make both checks for the same uncertainty.

| Lead result | Counter gained |
|---|---|
| Critical Success | 2 Escape |
| Success | 1 Escape |
| Failure | 1 Pursuit |
| Critical Failure | 2 Pursuit |

An independently achieved declared round objective, actual sacrificed cargo or blocking maneuver can supply 1 Escape instead of the ordinary lead success. It does not add another generic point. Generic Escape is capped at 1 per round, or 2 when the actual lead critical supplies 2. Losing a real member, route or vehicle can add 1 Pursuit when declared as a consequence; generic Pursuit is capped at 2 per round. Express paid features retain only their exact point permissions.

Each round includes one predeclared meaningful opposing threat: a legal attack, actual hazard or necessary sacrifice. It does not add a full enemy multiattack/nova to another chase punishment. Allies use their real Actions to Help, carry, treat, cast, command, move or create obstacles; they do not make extra lead checks. Combat Help keeps its actual advantage and expiry rules.

Resolve that round's costs, threat and check once, then compare totals. **Escape at least 3 with Pursuit below 3 succeeds. Pursuit at least 3 fails, including simultaneous 3/3.** Success returns to Expedition Mode with +1 Pressure, actual survivors/cargo and pursuit history. RP, recharge and encounter-use resources do not refresh. Failure gives the opponent its actual advantageous next position or capture opportunity; it does not automatically kill everyone or assign ownership.''',
'''Threat attacks preserve real range, costs, defenses, damage and source callbacks. Abstract chase displacement does not also trigger another tactical opportunity-attack sequence. When exact tactical movement/attack exchange is needed, use Encounter Mode and declare that exchange's single contribution to the round before resolution; do not combine full opposing combat and abstract chase punishment.

An Action committed to the lead check is unavailable for another action. Declared cargo sacrifices consume or relocate actual cargo; gestures do not create class-feature output. Maintain unique increment causes and the generic per-round limits, then apply genuine express source exceptions only within their real scope.

A physically trapped route cannot be bypassed by another check. Present real surrender, rescue, alternative fight or route options under their actual permissions. Carrying a casualty still requires the actual carrier and its movement/Load/body limits.''')

section(16, 'Estimate encounters from actual participants',
'''The Expedition roster is not the encounter's participant count. Track who is actually present, participating and able to contribute under their real action/command rules. Reinforcements enter at their actual times; they do not silently grant another unopposed wave.

Encounter budgets are provisional planning estimates, not promises of survival or measured balance. Establish objectives, terrain, exits, cargo, civilians, hazards, starting distance and surprise, then use the current combat rules. Cargo protection, escort and retreat require their own stated success conditions rather than only a kill count.

Boss Tenacity applies only to a declared source-qualified boss with its actual allowance. Size, cost or an encounter budget does not confer boss status. Use [current control/condition rules](../CONDITIONS_PLAYTEST.md), including exact source counters, replacement and duration. Fear, Reaction denial and ordinary Speed penalties are not interchangeable with full-turn denial.''',
'''For this provisional estimate, party level is floor(the arithmetic mean of actual participating characters' character levels), minimum 1. An enemy's actual assigned creature level controls; otherwise retain its exact rational CR. Bin floor(enemy level/CR − party level) using this source table:

| Relative level | Threat Points |
|---:|---:|
| −4 or lower | 5 |
| −3 | 10 |
| −2 | 15 |
| −1 | 25 |
| 0 | 40 |
| +1 | 60 |
| +2 | 90 |
| +3 | 135 |
| +4 or higher | 200 |

CR 1/4 against level 1 bins −1 here. CR supplies no unprinted creature ability or imported stat block.

Compute N_eff as actual participating independent character turns plus 0.5 for each actual limited attached-phase offensive companion/device contributing to that scene. Count no passive gear, absent member, support-only decoration or duplicate actor. A full-turn recruited NPC contributes 1 with its proper roster/service status. Keep the real profiles and command limits; a half actor is not a claim of equal power across all classes. Do not produce an encounter budget for zero participants.

Multiply the following four-character budgets by max(0.2, 1 + 0.2 × (N_eff − 4)). This keeps the source 3/4/5/6 participant multipliers 0.8/1/1.2/1.4 without exponential compounding.

| Difficulty | Base budget | Source success target, not observed performance |
|---|---:|---|
| Routine | 50 | 95–100% |
| Standard | 90 | 70–90% |
| Hard | 130 | 40–65% |
| Severe | 180 | 15–35% |
| Catastrophic | 240 | 0–10% |

Compare enemy totals and budgets, then apply each actual objective, hostile terrain, surprise and active hazard adjustment once in the final label. Cargo/hazard normally adds one step; ordinary surprise adds one; a genuinely warranted full unopposed enemy round adds two, without another automatic addition for that same surprise. Route-quality −1/+1 adjustments apply only where the same threat has not already been counted. Escort needs an explicit progress/survival/movement clock; retreat uses its actual Escape/Pursuit clock.

Retain the calibration limitations: level 1–2 Standard encounters should avoid pairs of above-level enemies; levels 5–16 need meaningful objectives/phases rather than arbitrary HP inflation; levels 17–20 need actual party-composition testing. Proxy estimates justify no global class buffs, nerfs or guarantee of survival. Gate Guardian's second Tenacity use still requires its actual source, and old global control-immunity shorthand does not override the current hard-control procedure.''')

section(17, 'Transport admission preserves every body and item',
'''Before a move, validate all of these separately:

- The actual body, control permission and current movement/conditions.
- Physical route space, clearance and fit.
- Pounds, including supported living bodies and all their associated gear.
- Load, storage volume and real seats or cargo positions.
- Required crew, pullers, propulsion and their actual work.
- Legal custody and continuing item/effect clocks.

A container contributes its own empty body and each child once. A printed inclusive gross weight/Load covers only its stated contents. Keep pounds and Load distinct. A passenger's melded equipment still burdens an external carrier. Extraction Class changes the handling problem, never the carrier's capacity.

Use the [body/equipment procedure](../BODY_EQUIPMENT_PLAYTEST.md) for real mass, inventory Burden and casualties. With positive carried Load at or above half capacity, and no greater than capacity, the carrier is Burdened; empty inventory is not Burdened even at zero capacity. Hard physical and inventory limits still apply. Vehicles, mounts and their particular sources keep their own completed profiles.

Melding, petrification, changing vehicles, a sale, a service quote or renaming a record cannot restore missing cargo or spend another copy. A transport catalogue does not provide a living mount, available crew, actual route or unacquired feat.''',
'''The complete candidate must include all 29 original transport rows and their full operating profiles, plus the distinct Core service/auxiliary profiles under TR-01–14. Those complete profiles are still assembled separately from this module. Keep every NEW profile value separate from the untouched source row, including comma placeholders and null/missing mass, speed or capacity. Preserve Player prices, all nine printed mount speeds/carry limits, and original Cart HP 30 as durability only.

Complete profiles support authoring and synthetic adjudication. Actually acquiring and using an asset still requires its ordinary real provider, access, body, stock, crew and permission. Do not treat a completed mechanical profile as evidence those particular world facts exist. No pending mounted feat or companion ability is promoted by this integration.''')

section(18, 'Durability, old Integrity records and repair',
'''Use actual structural HP for modeled equipment, fixtures and transport bodies. The old 0–3 Integrity track is not another damage pool, and its old Integrity-1 penalty does not automatically apply to a functioning positive-HP item. Keep actual grade, quality, flaws, constituents and custody. Living mounts use living HP and conditions, not structural repair.

At zero structural HP, an object is Broken under the [equipment rules](../EQUIPMENT_ACQUISITION_PLAYTEST.md). It still exists with mass, occupied space and physical drawbacks until actually removed or repaired. A missing wheel or other true primary constituent can make a vehicle incomplete even with positive aggregate HP. Inventing a cheap “pin” target does not disable a whole structure.

Ordinary self-repair requires a relevant trained toolkit and real compatible material worth **25% of the item's proper size/grade baseline**. Spend **max(1 hour, maximum structural HP ÷ 10 hours)** of active work and make the appropriate DC 10 tool task. Collapse Core degrees to success/failure: success restores maximum structural HP; failure spends time/materials and a new attempt needs fresh payment. A critical supplies no extra generic benefit. Repair at zero HP requires the recoverable main body.

An eight-hour Repair Watch is eight hours of available work, not eight completions. A 300-HP mundane vessel needs 30 active hours under this profile. Magical recipe bodies retain their exact functional/Broken bridge, prices, primary identities and persistent flaws. Repair does not recreate missing items, passengers, doses, ammunition, burnt pages, fuel, charges, class gauges or a terminal dismantled source.''',
'''Preserve historical Integrity without migrating a real save. Only where a source-tagged integer I in {0,1,2,3} is the sole condition evidence for a genuinely identified complete body with newly established maximum structural HP H, derive conservative initial HP = floor(H × I / 3). Keep the original raw I and interpretation source. I = 0 maps to 0; I = 3 maps to H only if the source actually asserts intact sound condition and no later damage evidence exists.

Credible current HP/damage controls instead; never raise it from old Integrity. Conflicting chronology remains unresolved until an actual correction event. Unknown, unversioned or malformed values remain raw and nonoperative. Do not inverse-write a derived interpretation into a historical save.

Optional display labels are Broken 0 at HP 0, Damaged 1 at 0 < HP ≤ H/3, Worn 2 above that but below H, and Sound 3 at H. These labels are display only, not another operative condition track. Unmodeled route Integrity may remain condition prose without granting a repair or hauling permission. Camp tier, route security and supply-line function keep their own event/build records.

Use the exact current item's repair procedure. Existing grade/size pricing precedes the material calculation. Service repair is a separate genuine quote under the equipment/service rules; do not add self-repair material cost to an inclusive service bill. Preserve all source fields and actual surviving material. This interpretation does not read or modify actual character/campaign saves.''')

CASES = [
    ('02-01', ['FL-08'], 'Two groups with Pressure 2 and 4 merge on a Risk-3 route.', 'Use Pressure 4 with both histories. The merge does not produce a fresh pool or lower Pressure to the route floor.'),
    ('02-02', ['FL-08'], 'One Attention lot stays exposed through three Watches and changes containers.', 'Its original continuous exposure causes one discrete increase. The same exposed state can still contribute the single Extraction DC modifier; repacking does not renew the cause.'),
    ('02-03', ['FL-08', 'FL-09'], 'A group reaches safe Haven at hour 6, before its current Watch has had its routine exposure checkpoint.', 'Settle that checkpoint at the last exposed boundary using actual accrued causes. Mark it processed. Do not roll it again at hour 8 or create a route patrol inside Haven.'),
    ('02-04', ['FL-09'], 'At Pressure 3, the final natural die is 4 and a lawful −1 yields 3.', 'Minor. An untouched natural 3 would instead give Standard. The procedure itself grants no −1 or reroll.'),
    ('02-05', ['FL-09'], 'At Pressure 3, a final natural 1 has a lawful +3 modifier.', 'The modified 4 does not trigger. Natural 1 is Severe only after the trigger test succeeds.'),
    ('02-06', ['FL-09', 'FL-13'], 'A Severe root complication changes an extracting convoy; its one secondary Extraction Test also generates a Severe complication.', 'Resolve the second complication, but do not generate another secondary test in that same causal batch. A genuinely later due Watch event still has its own timestamp.'),
    ('02-07', ['FL-10'], 'A fit 3-mph convoy traverses a Contested route with a 60-minute pause.', 'Its nominal 480 minutes becomes 600 moving minutes, plus the real 60-minute pause, for 660 elapsed minutes. Do not also award separate mileage or an extra eight-hour Watch.'),
    ('02-08', ['FL-10'], 'An Unknown traverse is made feasible by its own successful moving reconnaissance, with the permitted Progress bonus selected.', 'Use base 1 plus at most one shared reconnaissance +1, then the actual route-capacity penalty if any. A same-tranche mapping improvement does not retroactively grant base 2.'),
    ('02-09', ['FL-11'], 'Three Medium active participants and one Large participant succeed at a feasible forced march with their extras reserved.', 'The extra support commitment is five complete baskets, subject to actual specific diet exceptions and real consumption history. Gain 1 Progress and +2 Pressure once; a critical grants the same march result.'),
    ('02-10', ['FL-12'], 'An extraction episode starts with highest Class 2 and later acquires a genuinely new Class 6 lot.', 'The original surcharge is 1; the high-water value becomes 3, adding only 2. Dropping the Class 6 lot does not refund the surcharge.'),
    ('02-11', ['FL-13'], 'A Mapped route has Length 7.', 'Freeze routine midpoint 3.5 and exit 7. Each uses an actual position. Reaching the midpoint via extra Progress queues it once, not recursively inside the previous result.'),
    ('02-12', ['FL-13'], 'Tier II DC 13, highest Class 4, exposed Attention, Burden, three unsecured dangerous lots, pursued and Secured.', 'The cargo subtotal 9 caps at 7, then +2 and −2 apply outside it: DC 20. A lot with both Volatile and Cursed counts once.'),
    ('02-13', ['FL-13', 'FL-14'], 'A checkpoint requires stationary verification, then its failed test selects the eight-hour delay.', 'Count one actual verification minute and 480 delay minutes. The delay gives no stalled-convoy Progress; independent safe rest is possible only if its actual conditions qualify.'),
    ('02-14', ['FL-14'], 'A reachable Class 3 crate is at risk and no more specific recovery source applies, at Tier II.', 'Declare the actual 60-minute task at DC 16 with required rigging/helpers. Failure uses its declared stranded position or hazard; it does not automatically delete the crate or pay insurance.'),
    ('02-15', ['FL-15'], 'A retreat round would finish at Escape 3 and Pursuit 3 after its declared costs and threat.', 'Pursuit reaches the failure threshold, so the retreat fails. This grants the actual next enemy position/opportunity, not automatic death or ownership.'),
    ('02-16', ['FL-15'], 'The lead rolls a Critical Success while an ally achieves the declared blocking objective.', 'The generic Escape award remains 2 from the lead critical, not 3. The ally does not generate another lead check; any express paid feature needs its actual separate permission.'),
    ('02-17', ['FL-16'], 'Four independent participating characters and one actually contributing limited attached-phase offensive companion face an encounter.', 'N_eff is 4.5 and multiplier 1.1. Standard reference budget is 99. This is a provisional numerical estimate, not a runtime or balance result.'),
    ('02-18', ['FL-16'], 'An enemy has only CR 1/4 and the actual party reference level is 1.', 'floor(1/4 − 1) = −1, giving 25 provisional Threat Points. Its actual stat block still determines its abilities.'),
    ('02-19', ['FL-17'], 'A carrier transports a transformed ally with 20 lb of melded gear.', 'Include the ally’s effective body mass and all melded/external gear in external carriage. The gear is not weightless for the carrier, and the separate casualty/gear Loads still apply.'),
    ('02-20', ['FL-18'], 'A complete cart has only source-qualified Integrity 2 and a newly established maximum of 30 structural HP.', 'Derive 20 HP while preserving raw Integrity 2. If credible current damage instead establishes 7 HP, retain 7; the old Integrity cannot heal it.'),
    ('02-21', ['FL-18'], 'A recoverable ordinary cart has maximum 30 HP and a proper 15-gp baseline.', 'Self-repair takes 3 active hours and 3.75 gp of compatible material, then a DC 10 binary-outcome tool task. It does not restore cargo or grant a second cart.'),
    ('02-22', ['FL-08', 'FL-10', 'FL-17'], 'The convoy exceeds route Capacity but one individual carrier also exceeds its own hard limit.', 'The −1 Progress/+1 Pressure route penalty does not legalize the carrier’s overload. Transfer, drop, split or use a real permitted alternative first.'),
]

def render(envelope, audience):
    title = 'Player' if audience == 'player' else 'Director'
    lines = [f'# {title} expedition procedures — routes, extraction and retreat', '', envelope['notice'], '',
             'Use this with [part 1: organization, time, provisions and camps](EXPEDITION_PART01_PLAYER.md) and the current [Core resolution](../CORE_RESOLUTION_PLAYTEST.md) rules.', '']
    if audience == 'director':
        lines += ['Read the complete [player procedure module](EXPEDITION_PART02_PLAYER.md) alongside this Director material; the two cover the eleven mapped directions together.', '']
    for s in envelope['sections']:
        lines += ['## ' + s['title'], '', s['text'], '']
    if audience == 'director':
        lines += ['## Authored boundary examples', '', 'Expected tabletop outcomes, not executed whole-game scenarios or human playtest evidence.', '']
        for c in envelope['workedCases']:
            lines += ['### ' + c['id'], '', c['given'], '', c['expected'], '']
    return '\n'.join(lines)

def main():
    paths = {'public': R / 'data/public/expedition_candidate/part02.json', 'internal': R / 'data/director/expedition_candidate/part02.json',
             'player': R / 'docs/mechanics/expedition/EXPEDITION_PART02_PLAYER.md', 'director': R / 'docs/mechanics/expedition/EXPEDITION_PART02_DIRECTOR.md',
             'receipt': A / 'EX58_CANDIDATE_PART02_CHECK.json'}
    assert not any(p.exists() for p in paths.values()), 'Preserve previous output before a revision'
    checks = []
    def ck(name, result):
        checks.append({'name': name, 'pass': bool(result)})
        assert result, name
    manifest = read(P / 'FILE_MANIFEST.json')
    for x in manifest['files']:
        ck('Original final verdict preserved: ' + x['path'], info(P / x['path']) == {k: x[k] for k in ['bytes', 'sha256']})
    all_dirs = read(P / 'EX58_AUTHORING_REGISTER.json')['directions']
    dirs = {x['id']: x for x in all_dirs}
    ids = [s['id'] for s in SECTIONS]
    ck('Exactly FL-08 through FL-18', ids == [f'FL-{i:02d}' for i in range(8, 19)])
    prior = read(R / 'data/director/expedition_candidate/part01.json')
    ck('First seven are distinct and office correction confirmed', prior['authoredQuestionIds'] == [f'FL-{i:02d}' for i in range(1, 8)] and prior['officeContractDiscrepancy']['gptCorrectionConfirmedInThisModule'])
    public = {'schemaVersion': 1, 'moduleId': 'EX58-PART02', 'status': 'authored-partial-candidate-awaiting-exact-review',
              'notice': 'Working chapter module 2. Together with part 1, eighteen of the 58 source directions are drafted. Full transport profiles, Haven, social and reputation chapters remain to assemble before exact review.',
              'questionIds': ids, 'completeExpeditionCandidate': False, 'selectionEnabled': False,
              'sections': [{'id': s['id'], 'title': s['title'], 'text': s['player']} for s in SECTIONS]}
    examples = [{'id': 'EX' + i, 'questions': q, 'given': g, 'expected': e} for i, q, g, e in CASES]
    director = {'notice': public['notice'], 'sections': [{'id': s['id'], 'title': s['title'], 'text': s['director']} for s in SECTIONS], 'workedCases': examples}
    current_contracts = read(R / 'data/director/expedition_candidate/source_contracts_corrected.json')['contracts']
    source_paths = [R / 'docs/mechanics' / n for n in ['GAMEPLAY_LOOP_CANON.md', 'CORE_RESOLUTION_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'STRAIN_PLAYTEST.md', 'EQUIPMENT_ACQUISITION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md', 'COMBAT_ACTION_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md', 'CLASS_PLAYTEST_RULES.md']]
    for p in source_paths:
        ck('Governing source exists: ' + p.name, p.is_file())
    internal = {'schemaVersion': 1, 'moduleId': public['moduleId'], 'status': public['status'], 'sourceReview': 'EX58-SOURCE-2026-10-11',
                'sourceAssistantMessageId': 'f9effea2-510e-4529-a141-a3c1932008f3', 'completeExpeditionCandidate': False, 'authoredQuestionIds': ids,
                'cumulativeAuthoredQuestionIds': prior['authoredQuestionIds'] + ids,
                'remainingSourceDirections': [d['id'] for d in all_dirs if d['id'] not in prior['authoredQuestionIds'] + ids],
                'publicEnvelope': public, 'directorModule': director,
                'completeOriginalDirections': [dirs[i] for i in ids],
                'completeCurrentContracts': [c for c in current_contracts if c['id'] in ['EC-05', 'EC-06', 'EC-07', 'EC-08']],
                'governingSourceBindings': [{'path': p.relative_to(G).as_posix(), **info(p), 'completeText': p.read_text('utf-8-sig')} for p in source_paths],
                'sourceChoiceNotice': 'NEW EX58 timing, risk, interpretation and numeric choices remain traceable to the complete original directions. This candidate is not exact-reviewed or runtime implemented.',
                'audienceBoundary': 'Public data contains general player procedures only. Director planning/calibration and full source/evidence layers remain in the internal envelope. No private faction dossiers, hidden plans or campaign actors are projected.',
                'semanticCoverageNote': 'Manual authored treatment of eleven directions; parity and arithmetic do not prove semantic completeness. Complete candidate exact review remains required.',
                'examplesAreRuntimeTests': False, 'runtimeImplemented': False, 'newPromotions': 0}
    frozen = read(A / 'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest']
    for rel, expected in frozen.items():
        if rel != 'README_EXPEDITION_INTEGRATED_V3.md': ck('Submitted current source unchanged: ' + rel, info(G / rel) == expected)
    ck('All eleven directions have authored examples', set(ids) <= {q for c in examples for q in c['questions']})
    arithmetic = [
        ('merged pressure', max(2, 4, 3), 4), ('Contested moving minutes', Fraction(480) * Fraction(5, 4) * Fraction(3, 3), 600),
        ('Contested with pause', 600 + 60, 660), ('Secured nominal travel at3mph', Fraction(480) * Fraction(3, 4), 360),
        ('half-pace Contested minutes', Fraction(480) * Fraction(5, 4) * Fraction(3, 1) / Fraction(3, 2), 1200),
        ('forced march basket count', 3 + 2, 5), ('initial Class2 surcharge', min(3, 2 // 2), 1),
        ('Class6 highwater increment', min(3, 6 // 2) - min(3, 2 // 2), 2),
        ('Length7 midpoint', Fraction(7, 2), Fraction(7, 2)), ('cargoDCcap then pursuit/secured', 13 + min(7, 4 + 1 + 1 + min(3, 3)) + 2 - 2, 20),
        ('delay seconds', 8 * 3600, 28800), ('verification and delay minutes', 1 + 480, 481), ('Class3 recovery DC', 13 + min(6, 3), 16),
        ('N_eff multiplier', max(Fraction(1, 5), 1 + Fraction(1, 5) * (Fraction(9, 2) - 4)), Fraction(11, 10)),
        ('Standard budget4.5', 90 * Fraction(11, 10), 99), ('quarterCR bin', math.floor(Fraction(1, 4) - 1), -1),
        ('Integrity2cartHP', math.floor(Fraction(30 * 2, 3)), 20), ('cart repairgp', 15 * Fraction(1, 4), Fraction(15, 4)),
        ('cart repairhours', max(1, Fraction(30, 10)), 3), ('large vesselhours', max(1, Fraction(300, 10)), 30),
    ]
    for label, actual, expected in arithmetic: ck('Plain arithmetic: ' + label, actual == expected)
    # Finite reference classifications only; they do not drive a campaign state.
    def severity(p, n, mod=0, rerolled=False):
        if p == 0: return 'None'
        if p == 6: return 'Severe'
        r = n + mod
        if r > p: return 'None'
        if n == 1: return 'Severe'
        if r == p and (mod != 0 or rerolled): return 'Minor'
        return 'Standard'
    severity_reference = []
    for pressure in range(7):
        for natural in range(1, 7):
            result = severity(pressure, natural)
            expected = 'None' if pressure == 0 or (pressure < 6 and natural > pressure) else ('Severe' if pressure == 6 or natural == 1 else 'Standard')
            ck(f'Unmodified severity table P{pressure}/d{natural}', result == expected)
            severity_reference.append({'pressure': pressure, 'natural': natural, 'result': result, 'dieActuallyRolled': 0 < pressure < 6})
    for p, n, m, rr, expected in [(3, 4, -1, False, 'Minor'), (3, 3, 0, True, 'Minor'), (3, 3, 0, False, 'Standard'), (3, 1, 0, False, 'Severe'), (3, 1, 3, False, 'None')]:
        ck('Modified severity reference ' + str((p, n, m, rr)), severity(p, n, m, rr) == expected)
    internal['boundedSeverityReference'] = severity_reference
    save(paths['public'], public); save(paths['internal'], internal)
    for audience, envelope in [('player', public), ('director', director)]:
        paths[audience].parent.mkdir(parents=True, exist_ok=True)
        paths[audience].write_text(render(envelope, audience), encoding='utf-8', newline='\n')
    ck('Whole public envelope equals saved internal projection', read(paths['public']) == read(paths['internal'])['publicEnvelope'])
    ck('Whole player chapter equals saved representation', paths['player'].read_text('utf8') == render(read(paths['public']), 'player'))
    ck('Whole Director chapter equals saved representation', paths['director'].read_text('utf8') == render(read(paths['internal'])['directorModule'], 'director'))
    links = []
    for audience in ['player', 'director']:
        for target in re.findall(r'\]\(([^)]+)\)', paths[audience].read_text('utf8')):
            ck('Real local chapter link: ' + target, (paths[audience].parent / target).resolve().is_file()); links.append(target)
    for x in manifest['files']:
        ck('Final verdict unchanged after authoring: ' + x['path'], info(P / x['path']) == {k: x[k] for k in ['bytes', 'sha256']})
    receipt = {'generatedAtUtc': datetime.now(timezone.utc).isoformat(), 'moduleId': public['moduleId'], 'status': 'Eleven directions authored;18/58 cumulative. Complete exact candidate still incomplete and unreviewed.',
               'questionIds': ids, 'cumulativeQuestionIds': internal['cumulativeAuthoredQuestionIds'], 'remainingDirections': len(internal['remainingSourceDirections']),
               'workedCases': len(examples), 'plainArithmeticChecks': len(arithmetic), 'severityReferenceChecks': 47, 'localLinkChecks': len(links),
               'checks': len(checks), 'failures': [c for c in checks if not c['pass']],
               'outputs': {p.relative_to(G).as_posix(): info(p) for k, p in paths.items() if k != 'receipt'},
               'builder': {'path': Path(__file__).resolve().relative_to(G).as_posix(), **info(Path(__file__))},
               'scope': 'Source/archive preservation, actual local links, complete representation parity and bounded mathematical references. Qualitative cases remain authored expectations.',
               'runtimeTestsExecuted': 0, 'newPromotions': 0, 'realSavesReadOrWritten': 0, 'sourceInformationDeleted': 0, 'details': checks}
    save(paths['receipt'], receipt)
    print(json.dumps({k: receipt[k] for k in ['moduleId', 'remainingDirections', 'workedCases', 'checks', 'failures', 'outputs']}, indent=2))

if __name__ == '__main__': main()
