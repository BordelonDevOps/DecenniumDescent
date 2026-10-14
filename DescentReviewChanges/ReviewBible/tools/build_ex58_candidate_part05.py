"""Author all fourteen transport directions and preserve their complete sources."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import json
import re

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
P=A/'ex58-final-gpt-verdict'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
SECTIONS=[]
def section(n,title,player,director):SECTIONS.append({'id':f'TR-{n:02d}','title':title,'player':player,'director':director})

section(1,'Choose an actual mount',
'''Use the complete [transport catalogue](TRANSPORT_CATALOGUE_CANDIDATE.md) for Camel, Donkey or mule, Elephant, Draft horse, Riding horse, War horse, Mastiff, Pony and Warhound. Each is a separate profile. “Donkey or mule” means one chosen individual.

The printed price, walking Speed and carrying pounds are retained. The additional body size, mass, abilities, defenses, HP, Hit Dice, attack, training, nutrition, draw rating and Load cap are explicit new provisional game values. A carrying rating does not determine Strength or make a template a record of the particular animal being sold.

Use the profile's natural AC, which already includes its Dexterity, and its fixed maximum HP. Record the individual's current HP, remaining Hit Dice, Wounds, conditions, injuries and training. Saves use its ability modifier without an added save proficiency unless an actual source grants it. Ordinary senses do not grant darkvision or automatic detection. These profiles supply no class levels, RP, spellcasting, special immunity or class features.

An independent animal's listed attack costs its Action and makes one attack using that profile's bonus, reach and damage. Core attack criticals apply. It has no automatic charge damage, knockdown or Multiattack, and the rider receives no extra attack. A controlled ridden mount instead uses the restricted Action choices below.

Large mounts occupy a 10-foot square, Medium mounts a 5-foot square, and the new Huge Elephant a 15-foot square. A saddle admits one physically compatible rider at least one size smaller. A Medium character cannot ride a Medium Pony merely because their weight is low. Count the rider, all equipment, tack, containers and contents against both the mount's pounds and Load limits. Its separate harness draw rating is not extra back capacity.

A positive carried burden at or above half either profile limit applies the one Burdened penalty: Speed −10 feet and disadvantage to climbing, swimming or moving silently. Do not apply it twice because both measures qualify. Routine carriage must fit both full limits and the actual body/seat geometry.

A registered ordinary expedition mount is, by this new default, a significant creature using Core Wounds, dying and death saves. Establish that status before the encounter. An actual Ranger Beast bond instead follows its own HP-only, immediate-death lifecycle. No repair, stable fee, new template or replacement purchase revives a dead individual.''',
'''Keep the individual's original body history through purchase, hire, boarding, rescue, bond and sale. A healthy profile does not prove that a merchant's specimen is healthy, willing, trained or available. Significance cannot be changed after a fatal outcome.

The new threat reference level is solely for the expedition encounter-budget comparison. It is neither CR nor class level. An effect requiring a source CR still needs that actual missing predicate. Do not substitute threat reference, purchase value or carrying rating for a bond prerequisite or harvest table.

The catalogue's Load and draw limits are separately authored. They do not follow an inferred Strength formula and cannot be increased by recalculating one. Apply later actual source exceptions only where they govern this same individual.''')

section(2,'Control and training',
'''A physically compatible, trained and willing mount can be controlled. An intelligent or untrained independent mount keeps its own agency. Ownership, restraint and payment do not establish willingness or training.

A conscious, nonincapacitated seated rider can direct intended movement and choose the controlled mount's one allowed Action: **Dash, Disengage or Dodge**. Use an actual trained audible or tactile channel. An audible cue shares the language rules' speech allowance. Reins require an available hand; a trained seat/leg cue works only if that individual knows it and the current seat permits it. Ordinary riding direction adds no separate Bonus Action. It does not issue a class companion command, authorize an attack or transfer rider bonuses to the animal.

A controlled mount with its own regular turn counts toward the controller's existing limit of two commanded independent-turn combat-capable subordinates. The controller's own character is separate. A source-bound companion with only an attached phase retains its own command and offensive budgets; calling it a mount does not give it a full turn. Additional pack animals can be led outside combat through real handling, but do not give a third controlled combat turn. There is no automatic animal swarm.

An independent NPC acting as a party character counts toward the twelve-character roster. A merely ridden animal does not occupy a member seat, although its actions, cargo, provisions and history still matter. Independent animals are directed by their real agency, not treated as free player attack orders.

Recheck control when the mount acts. If the rider is no longer seated or able to cue it, the channel fails, or the mount is unable or unwilling, an unexecuted riding cue cannot compel it. If able, it defensively Dodges and stays still or moves only to an immediately safer available space, chosen through its actual agency. Its existing turn and spent budgets do not reset. An executed cue is not undone. A legitimate trained noncombat lead/follow cue can continue only while its actual conditions and handler remain available.

**New ordinary training course.** A genuinely tame, willing animal can learn one named riding or harness function through 40 active hours, at most four credited training hours per animal per day. The instructor needs Animal Handling proficiency, a suitable safe space, fitting tack and a usable conditioning method. Credit complete 15-minute phases. An interruption loses unfinished prospective phase credit; actual time, feed and fees remain spent. The full-course tuition reference is 5 gp, unless an actual voluntary or paid agreement differs.

Completion requires the real course and demonstrated safe routine behavior. It grants only the practiced function, without an obedience spell, rider proficiency or Ranger bond. A documented already-trained animal needs no repeat course. Wildness or unwillingness cannot be cured by depositing hours. A war-named purchase includes combat habituation only if its actual contract and behavior establish it. Feed, water, tack and stabling are separate unless genuinely included.''',
'''Record the controlling relation, the trained function and cue, seated rider, available hand/channel, animal willingness, actor-cap usage and actual turn. Ordinary riding cues are rechecked at execution; this explicitly differs from a protected already-issued attached companion command that may survive owner incapacity.

Do not import TI04 device binding, a shared companion Bonus Action or an attack allowance into ordinary riding. Carriage and ship control have the separately paid Actions below. Unattended lead/follow is not a programmable tactical routine or unlimited work.

Training is an actual bounded course. Its maximum four hours/day applies to that animal, not a new cap per instructor or per course name. Forty hours means at least ten such training days. Safe completion grants no immunity to later fear, fatigue, pain, anatomy restrictions or changed conditions.''')

section(3,'One complete mount turn',
'''At initiative registration, a controlled mount shares its rider's initiative value and takes one complete regular turn immediately **after** the rider's complete regular turn. Their movement and Actions do not interleave. You cannot move the mount twenty feet, insert a free rider attack segment, then finish the mount's movement.

You may Ready a permitted Action through the normal procedure, paying your Action and later Reaction, with its actual trigger, components and duration. This creates no free attack. An independent mount keeps its own initiative and choices.

The mount has its own regular-start/end markers, movement, normal Action and applicable Reaction budget. Its controlled Actions remain Dash, Disengage and Dodge. Control grants no offensive Reaction or opportunity attack; a specific defensive Reaction works only if actually available. It makes its own death saves when its lifecycle requires them. A rider's extra turn does not create another mount turn, start, recharge or condition tick.

Each physical actor receives at most one scheduled regular turn per numbered round. Mounting, dismounting or changing controllers retains its spent budgets and original allocated slot for that round. A new valid controlled relation takes its new rider-linked position beginning next round. This round, use the existing unspent slot if any; never replay a taken one.

A mount entering mid-round uses a legal not-yet-passed insertion under the combat-entry rules, or starts next round. It does not replay the new rider's earlier slot. Changing to independent behavior also grants no second turn. Separate rider and mount effects still expire at their own stated markers even when initiative values match.''',
'''Record actor ID, numbered round, regular-turn ID, original slot, prospective next-round slot, control history, and movement/Action/Reaction spent. Keep condition and death-save ordering attached to the actual creature.

Ordinary ridden turns are whole turns. The coordinated puller reservation for a drawn vehicle below is a specific exception for one linked vehicle movement, not permission to split every mount's turn. Travel and initiative transitions preserve real movement/work and do not duplicate ticks or rewards.''')

section(4,'Mounting, dismounting and losing the seat',
'''An ordinary mount or voluntary dismount costs half your current walking Speed, rounded down in feet, from your remaining regular movement. A positive Speed whose half is below one instead costs one foot. Speed 0 does not permit it. You may perform at most one mount **or** dismount operation per regular turn; an extra turn supplies no additional operation through this rule. The cost is movement, not a Bonus Action or free object interaction.

Start within five feet of the accessible seat at a reachable height, with a stable approach, one usable supporting hand and a physically fitting destination. A high Elephant saddle needs actual steps, help or a legal route to reach it; an exotic saddle does not lift you. If Prone, first stand using the real cost or use another valid assisted procedure. Mounting does not remove Prone.

To dismount, choose a visible, free adjacent space within five feet of the relevant body boundary at a reachable level. A wall, another creature, an inadequate gap or an unpaid fall is not a legal destination. Insufficient remaining movement or an inaccessible seat prevents the ordinary operation. A specific acquired feature overrides only its actual clause. The animal's remaining movement and Actions stay unchanged.

When one resolved source event moves a seated rider's mount against its will **or** knocks it Prone, the rider makes one DC 10 Dexterity saving throw. If that same event does both, make one save. Distinct events can each trigger a save. This is a binary Core save with no generic natural 1/20 degree shifts.

On failure, leave the seat and land Prone in the first legal adjacent space from your recorded dismount preference, or the Director's neutral accessible ordering. Resolve actual height and falling under the falling rules; unseating adds no fixed damage by itself. On success, retain the seat only if support remains physically possible.

A Prone mount does not automatically make its successful rider Prone, but its awkward body and blocked movement still matter. A rider independently made Prone gains that condition without another seat save. Voluntary ordinary travel alone causes no save. If an exact effect ejects you regardless of a save, use that effect and the actual landing. Impossible support or landing resolves through the real fall/entrapment situation, never placement inside a wall.''',
'''Predeclare the actual saddle point, approach and preferred dismount ordering where relevant. Record the triggering source event so one forced-and-Prone result does not create two saves. Do not infer another trigger from a renamed template or the rider's own Prone condition.

Success is not immunity to falling when no supporting body remains. Keep actual seat compatibility and the control predicates separate from the save. Resolve height, falling, collision and support through their own real sources instead of inserting an automatic unseat-damage packet.''')

section(5,'Position, areas and opportunity attacks',
'''Record the rider's actual saddle point or fitting five-foot subspace on the mount before movement. Attacks, reach, line of effect and area exposure use that position, not every edge of an Elephant's footprint. Moving to another accessible seat position takes your own real movement, path and support.

Rider and mount remain two creatures with separate AC, HP, conditions and resources. An area can affect both if it actually includes each; resolve separate saves and damage histories. Riding grants no automatic cover, shared HP or immunity. Actual barriers and body geometry can supply cover under the normal rules.

When the mount's own voluntary movement provokes a legal opportunity attack, the reactor may choose the mount **or** rider. The chosen target must actually be visible and within legal reach/line at the departure edge. Spend one available Reaction for one permitted ordinary attack before completing that departure step. One provoking move is not an attack on each creature, and a distant rider's seat does not become reachable merely because the mount is adjacent.

The mount's Disengage prevents the opportunity provoked by its movement, including this rider-or-mount choice. The rider's own Disengage protects the rider's own voluntary movement; it does not give the mount Disengage. Your own movement around the seat or while dismounting uses your own opportunity-attack rules.

Forced displacement or teleportation does not provoke a generic movement opportunity attack, although an actual seat-save trigger or other specific effect may apply. An attack against the mount does not automatically damage or unseat its rider; its actual consequence must trigger that result.

Vehicle carriage does not use this living-mount exception. Passive displacement of vehicle occupants gives no generic opportunity attack without a specific source. Moving pullers can provoke for themselves, without granting an attack through a wall against a distant passenger.''',
'''Keep the mount footprint, rider seat, actual movement path and each target's defenses. At a provoking edge, validate the chosen target before spending/rolling the reaction. Actual legal defensive reactions belong to the chosen target; no mount-and-rider pooled defense is created.

The same movement cannot provoke twice merely because both rider and mount moved. Turning travel into initiative is not a movement event. A positional aura reads actual body locations even when carriage does not qualify for a self-powered movement benefit.''')

section(6,'Movement belongs to the actor who performs it',
'''Riding changes your position, but it does not automatically spend your movement, perform your leap, count as your flight or charge, deal your weapon damage or activate a class feature. Track who moves under their own power, who is carried, the path, forced or teleport displacement, the budget spent, and whose turn it is. A rule asking whether someone is within a distance still uses actual positions.

Cavalry and Mounted Combatant remain separate pending feats. Ordinary riding grants neither their attack advantages nor Cavalry's +10 mount Speed. Their different prerequisites and attack scopes are not merged or assumed to stack.

Dragoon Momentum keeps its actual engine: genuine self-powered movement of at least 15 feet toward a tactical destination on the Dragoon's regular turn supplies its one movement gain; a qualifying personal weapon-damage event supplies the other default gain. All gains and refunds remain capped at two per round. Being carried, forced movement, teleportation, movement in place, allies, summons or another actor's hit does not qualify. A mount's leap is not the Dragoon's paid leap technique.

**New narrow transport interpretation:** the Dragoon's separate requirement to move at least twenty feet on its turn before a Weave cast counts actual voluntary self-propelled path, including a legitimately paid source leap. It excludes carriage, forced movement and teleportation. Keep the actual before-cast window and the Dissonance reduction of one, minimum zero. It grants no RP discount or additional Momentum.

Other class, oath, ancestry, spell and companion movement rules retain their exact acquired effects. This interpretation does not rewrite every distance condition or prohibit an actual feature expressly benefiting passive carriage.''',
'''Preserve the literal Dragoon protected interface and complete engine alongside this new interpretation; the old sentence did not explicitly say self-propelled. The fifteen-foot Momentum trigger and twenty-foot casting interaction are separate gates. A legal dismount, self-powered move/leap and personal attack can satisfy the actual engine, without counting the same path twice.

Keep both complete pending feat records, their original flags and current full-review-pending status. Old needsReview:false is not proof of current review. No broad text match across 1,223 class cards establishes movement eligibility. Exact position, actor, turn, movement budget and activation predicates are required.

Nothing here replaces closed companion commands, recipe devices, servicing, recycling, recharge or source-specific casting procedures.''')

section(7,'Tack, food, water and boarding',
'''Use the catalogue's actual tack profiles and fitting times. These new empty masses are separate from the old blank source weights:

| Tack | Empty mass |
|---|---:|
| Bit and bridle | 2 lb |
| Exotic saddle | 36 lb |
| Military saddle | 24 lb |
| Pack saddle | 15 lb |
| Riding saddle | 18 lb |
| Saddlebags | 4 lb |

These ordinary tack bodies have AC 15 and 5 HP. Saddlebags contain two actual cells of 20 lb and 0.5 cubic feet each, for 40 lb and one cubic foot total. Fit, balance, closure and shape still matter; they add no carrying capacity to the animal. A pack saddle is a load frame, not a rider seat. Military or exotic names grant no feat, seat-save advantage or fall immunity.

Fit equipment to the named animal's current anatomy. A new draw harness costs 5 gp and weighs 8 lb per compatible Medium/Large puller; the Huge version is 20 gp and 32 lb. Each has AC 15, 5 HP and five-minute setup. A bridle is not a complete draw harness. An actual purchase already including the fitting harness need not buy it again.

**Barding.** Choose an actual reviewed ordinary armor model. Its price is four times that baseline, replacing rather than compounding the general Large price multiplier. New mass multipliers are ×2 Medium, ×4 Large and ×8 Huge; armor HP multipliers are ×1, ×2 and ×4 respectively. Use that armor's real AC formula, Dexterity cap, Strength requirement and Stealth penalty. Choose between eligible armor and natural-AC formulas; do not add them together. Different grades or magic require their own real records.

New armor habituation takes eight active hours for one named armor category, at most four credited animal-training hours/day, in completed fifteen-minute phases. It requires a tame, willing, trained mount, fitting armor, a competent Animal Handling instructor and actual suitable work. Ordinary full-course tuition reference is 1 gp or the agreed rate. It grants only safe ordinary wearing competence, not rider proficiency or immunity to armor restrictions. Previously documented training needs no repeat course. Donning/doffing takes the actual armor time and a capable helper; changing form does not resize armor.

**Provisions.** The printed 5 cp daily feed reference buys one actual species-compatible animal-day quantity from the catalogue: Camel 12 lb, Donkey/mule 10, Elephant 60, Draft horse 16, Riding horse 12, War horse 16, Mastiff 2, Pony 8, Warhound 3. This is an explicit provisional price/quantity choice. Actual compatible stock is required. Water is separate: respectively 32, 24, 128, 40, 32, 40, 8, 16 and 12 pints/day, with real containers and weight. These replace the human Supply basket for those animals; add no human oil ration or free desert-fasting trait. Unmet daily food/water causes at most one ordinary expedition Strain for that day, not a duplicate for each missing component.

**Stabling.** Five sp/day buys one actual fitting safe stall or pen for 24 hours, ordinary supervision/cleaning and ten active caretaker minutes per animal-day. Food and water are separate unless the real quote includes their quantities. A small stall cannot accommodate an Elephant because the posted price was paid. Real suitable rest can qualify normally; payment does not heal, cure, refill Hit Dice or grant a second Long Rest. Emergencies and treatment require their actual additional work.''',
'''All fourteen original tack/drawn-vehicle/service rows retain their full source records, including comma placeholders, null numerical weights and source status. New physical quantities are separate fields. A service is not a half-pound object; unknown weight is not zero.

Record actual fitting, workers, hands, anatomy, item HP, stock, nutrition and custody. A caretaker cannot supervise incompatible remote pens at the same time. The ten-minute calm care allowance is not emergency veterinary treatment.

Barding cost, mass, HP and worn AC use distinct rules. Apply the actual sized armor reference once for repair, not the animal's purchase value or HP. Fitted tack can be repaired from its actual primary body and compatible subordinate parts; neither repair nor a saddle creates a missing animal.''')

section(8,'Drawn vehicles and the two sleds',
'''The catalogue supplies five distinct new frames: Carriage 100 gp, Cart 15 gp, Chariot 250 gp, Player Sled 20 gp and Wagon 35 gp. The Cart retains its reviewed 30 structural HP. The other body quantities, geometry and handling values are explicitly new. Purchase does not automatically include animals, harnesses, drivers or contents.

The Core Dungeon sled is a separate 25 gp, two-operator item. Its new frame weighs 60 lb and has 30 HP/AC 15, a 6×3×2-foot outer envelope and 5×2.5×1.5-foot bed. Normal payload is 12 Load/120 lb; emergency maximum is 20 Load/200 lb at drag Speed 5 if the real two workers and route can support it. It does not replace the Player snow/ice sled or inherit that sled's animal-drawn profile.

For every frame, check empty mass, full payload pounds and Load, cargo sublimit, seats, draw-team requirement and actual passage geometry. A passenger uses a real seat and counts body, gear and passenger Load. Luggage capacity is part of total payload, not extra. Cart's normal payload limit is 30 Load, Wagon's 80; their empty frame masses are additional support/draw burden.

Only compatible, trained, simultaneously working pullers with fitting harness can combine their explicit gross draw ratings. Gross draw means vehicle plus payload, occupants and attachments. The pullers' own body masses are not part of draw weight, but every animal still counts against a bridge or floor's support. Each puller's own carried burden is checked separately. Above half the combined gross draw rating causes one Burdened speed penalty; above the full rating prohibits routine draw. A check does not waive stairs, gaps, blocked widths, incompatible slopes or terrain.

**New tactical driving procedure.** The actual driver spends an Action through a usable control channel, with reins/controls and one available hand. Required pullers reserve sufficient real movement from their legal turns in the same round. Resolve one coherent vehicle/puller movement after the last required contribution is available, rechecking bodies, load, harness and path. Earlier reserved movement cannot also be spent elsewhere. Consume each contribution once. Motion is limited by the slowest current puller budget/Speed and the vehicle cap.

No future Action is presumed. A later incapacity or broken harness can prevent motion while already spent Actions remain spent. Extra Actions, another driver or another puller do not create a second drive event in that numbered round. The frame has no native Dash, Disengage, Reaction, weapon or attack. Pullers retain only their own actual creature actions and command limits.

Outside initiative, the driver and pullers work for actual travel time. Harnessing takes five active minutes per vehicle with actual workers; loading is separate. Independent workers can fit separate harnesses concurrently where feasible. A moving ninety-degree turn requires clear swept space and at least one vehicle-length of forward travel. Brakes allow an ordinary controlled stop; steep slopes or failed brakes need their actual hazard resolution.

A routine clear feasible road needs no check. For an uncertain driving hazard use DEX with Vehicles (Land), or WIS (Animal Handling) for an animal-response problem, one proficiency once. Use the hazard's DC, or the new references 10 ordinary, 13 hard, 16 severe. Declare consequences first. Success avoids the stated obstacle; a critical adds only declared feasible positioning. Failure stops safely if possible; otherwise an actual bounded low-speed collision deals 1d6 bludgeoning to the frame, or 2d6 on Critical Failure. These fallback packets do not replace specific high-speed, falling or passenger-injury rules.''',
'''Record the coordinated movement reservation as one exceptional vehicle event, not ordinary interleaved riding turns. Each puller needs a legal existing movement budget and actual control; the vehicle does not create free offensive caravan actors. One Action or movement contribution cannot pay a different task too.

Cart, Wagon, Carriage, Chariot and Player Sled retain their complete catalogue dimensions, seats, primary structures and terrain. Do not equate a frame's HP with payload or use an invented five-times-Strength towing formula. An indivisible blocked bend remains a real route problem.

A disabled frame strands its actual cargo until a feasible unload, transfer, support or tow occurs. HP 0 alone does not destroy occupants, contents or source history. Collision, dislodgement and falling are separate actual events with their declared consequences.''')

section(9,'Watercraft need working crews',
'''The catalogue supplies six complete provisional watercraft: Galley 30,000 gp, Keelboat 3,000 gp, Longship 10,000 gp, Rowboat 50 gp, Sailing ship 10,000 gp and Warship 25,000 gp. Their new bodies specify mass, AC 15, structural HP, hull/mast envelope, draft, hold shape, payload, occupants, crew, Speed and repair. A name or price includes no crew, weapons, cargo, berth, lifeboat or feasible route.

| Vessel | Active oar crew, including helm | Active sail crew, including helm |
|---|---:|---:|
| Galley | 41 | 8 |
| Keelboat | 3 | 3 |
| Longship | 11 | 4 |
| Rowboat | 1 | No sail mode |
| Sailing ship | No oar mode | 8 |
| Warship | 21 | 10 |

These are simultaneous real workers in their actual positions. Only the Rowboat combines helm and oar in one person's Action. A person's Action cannot fill two other crew jobs. Replacement crew take over prospectively; they do not supply a missed past stroke. Actual training, appendages and tools still matter. Calm ordinary rowing can be physically attempted untrained without an automatic penalty; a hazardous helm needs the specified trained operator and actual procedure.

Large public-service crews may exist outside the twelve-character party, but remain separately paid, supplied, rested staff. They are not free party helpers or recruited combat allies. Owning a ship with too few personnel does not operate it.

**Tactical movement.** One vessel drive event per numbered round resolves only after the current helm Action and every required propulsion/rigging Action for the selected mode are available. Recheck feasibility after the last contribution. Actions already spent remain spent if a later blocker prevents the event. Extra Actions, turns or helm changes do not grant a second drive. Working crew cannot also use those Actions to attack, Help, guard, command a different device or claim rest. The hull has no creature turn, save, Reaction, Dash, Disengage or creature-condition clock.

**Travel.** Use the catalogue's mph per active staffed travel hour. A stated sail mode needs usable wind and course: no usable wind means zero sail self-propulsion. Adverse but usable wind halves the sail rate unless a specific weather rule says otherwise. Oars need their full crew. Record current as an actual separate vector. A countercurrent can reduce along-route progress to zero while drift still changes position. Missing weather/current information is unknown; only a stated synthetic example may assume calm/current zero. An uncrewed ship can drift under real forces without receiving a free commanded move.

Check total payload and cargo sublimit separately, including all people, their gear, ballast and containers once. Occupant limits still apply to magically light passengers. Require draft plus half a foot of water clearance at allowed payload, the full hull/mast passage and clear swept turn space.

Docking takes one minute for a Rowboat, five minutes for the others, with actual bank/berth, lines, water and workers. Loading is additional. A ninety-degree moving turn requires one hull-length of forward travel and clear sweep; a feasible stationary line/anchor maneuver takes ten crew minutes. Lowering an actually lowerable mast takes twenty active crew minutes and retains the real lowered mast aboard with its clearance.

Hazardous charting uses INT and hazardous helm work DEX with Vehicles (Water), one proficiency once. Use the actual source DC or 10 ordinary/13 hard/16 severe. Routine feasible calm work needs no roll. Declare drift, grounding and obstruction stakes first. Failed bounded low-speed contact stops/grounds where possible, otherwise deals 1d6 hull bludgeoning; Critical Failure deals 2d6 or the declared actual severe hazard, not both by default. Creature harm, drowning, falling and exposure use their own rules. Hull HP 0 follows the finite flooding/rescue procedure below.''',
'''The full profiles preserve each exact active-mode Speed, mph, minimum depth, geometry, occupant count and original-body repair requirements. New operating values do not fill in or overwrite the old source blanks. “Warship” grants no ballista or separate combat-stat package.

Track all paid crew contributions, current availability, the single numbered-round drive event and the actual resulting path. Passive passenger displacement is not personal movement expenditure, Dragoon Momentum or the mounted opportunity-attack exception. Passengers may do compatible tasks only when the actual environment permits; a moving ship is not automatically a full workshop or safe rest site.

No vessel quote supplies a conveniently present rescue boat or crew. Plan escape from actual positions, remaining time, usable lines, boats, bodies and Actions. Real support can preserve a disabled wreck for repair; its contents and history remain real even if submerged.''')

section(10,'Porters, bearers and hired pack animals',
'''| Service | Contracted customer cargo | Base daily price |
|---|---:|---:|
| Porter | 2 Load | 2 sp, plus agreed danger pay |
| Skilled bearer | 3 Load | 1 gp |
| Pack-animal hire | 6 Load | 5 sp, plus feed |

These are customer allowances, not a biological capacity increase. Name the actual worker or animal and check their own gear plus the promised cargo against their real pounds, Load, shape, fatigue and terrain limits. A stronger porter does not automatically owe more work; extra carriage needs a feasible amended agreement.

Core's porter safe 2/maximum 4 and pack-animal safe 6/maximum 10 Load describe emergency offer limits. Extra loads require an expressly accepted feasible operation, with actual burden/drag penalties and risk. They never override the individual's body limits or grant free overflow.

A bought Camel, mule or other mount keeps its own complete profile. A hired six-Load service must provide one identified suitable trained animal; it is not an interchangeable invisible body. Record the operator separately. Hire does not include a human handler, saddle, water, feed or stabling unless the real agreement includes them. Do not charge both purchase and hire for the same delivered ownership interest. Late-return or loss liability must be agreed, not invented from the market price.

A service day is 24 elapsed hours of custody with at most two eight-hour assigned work Watches and actual Rest. Charge a started day once under the agreement; loading again or crossing a Haven gate does not restart the bill. The named service rate takes precedence over generic wages. Accepted dangerous duty defaults to twice that rate once, unless a different prospective agreement applies. Work already performed earns its agreed wage even when a task fails; refunds and liability follow the actual contract.

People hired into ordinary expedition jobs count toward the twelve-member roster. A public carrier's external crew stays on its service roster and supplies no free party jobs. Record consent, duties, knowledge, communication, pay, supplies, HP, Strain, rest, custody and departure. A wounded, exhausted or absent provider requires a real replacement and transfer; treating someone as cargo does not compel obedience.''',
'''Keep service scope separate from anatomy and ownership. A contracted six Load may fit a mule's body but not its actual current burden or route. The rate purchases an agreed service interval, not feed or unlimited extra work unless the offer really includes it.

Apply the service-specific price before the one accepted danger multiplier. Do not add the generic 1/3/10 gp wage schedule to the named porter/bearer rate or double once per danger adjective. Maintain actual paid/owed status without automatic borrowing.

Calm loading uses the transfer schedule below. Dangerous travel uses the real route/encounter procedure, not another service roll that charges the same consequence twice. Actual workers' consent, refusal and information remain distinct from inert inventory.''')

section(11,'The bound hauler and specialist services',
'''**Core transport hauler.** The retained reference is 500 gp plus fuel, with actual Tier-IV-or-higher availability, 20 normal Load and 30 emergency maximum. The new complete profile is a separate transport-only magical nonartifact machine. It is not a creature, summoned body, class companion, AEX automaton, recipe 507/670 or PC. It has no CR, mind, creature turn, attack, spell, RP, corpse/drop or class-command entitlement.

Its empty 120 lb wheeled frame measures 5×3×4 feet with a 4×2×2-foot clear bed, AC 19 and 60 maximum structural HP. Normal payload is 200 lb/20 Load at Speed 30 feet/3 mph. Over either normal rating, emergency carriage is limited to 300 lb/30 Load at Speed 5 feet/0.5 mph. Shape, full supported gross weight and a clear firm route remain necessary; never exceed either emergency maximum.

One real adjacent operator within five feet, with access to the controls and both manipulating hands, spends an Action for one drive event per numbered round, moving at most its current Speed over a feasible path. It cannot Dash, climb, fly, use stairs, act remotely or run an autonomous program. Another Action cannot buy another drive. Outside initiative the operator works continuously. Being aboard does not help if the controls are out of reach. This local mechanism is distinct from TI04's binding, channel and shared offensive-device budgets.

**Fuel.** One actual compatible lamp-oil pint, reference 10 cp/1 lb, powers eight accumulated active propulsion hours. The reservoir holds one pint. Consume exact proportional fuel as it actually operates; pauses consume no propulsion fuel, while leaks/losses persist. Refilling a stationary machine takes one active minute, two hands and available oil. Purchase creates no free oil or flask. Oil already spent for propulsion cannot also light a lamp or remain unspent Supply. This power grants no transferable energy, RP, distillate or spellcasting.

**Service.** At each forty accumulated moving hours, service is due before further propulsion. On the stationary serviceable mechanism, a qualified Vehicles (Land) or appropriate Tinker's-tools practitioner spends one active hour, suitable tools and one actual 1 gp/0.5 lb grease/fastener pack. Routine completed service needs no check. It clears only the due-service counter, restoring no HP, fuel or lost part. An interrupted service retains completed work but provides no completion until finished; it is not rest. A differently named AEX pack is not interchangeable without real compatible quantities.

**Restoration.** This hauler's explicit new magical repair bridge uses actual compatible materials at a 125 gp reference and qualified Vehicles (Land)/Tinker's tools. Positive-HP functional repair takes six active hours at DC 10. HP-0 reconstruction takes eight active hours at DC 15 and requires the original primary frame, drive unit and controller. Use Core task degree shifts, collapsing to success/failure without extra critical effects. Success restores this body's maximum HP/function only. Failure spends work and materials. Subordinate wheels, straps and fasteners can be replaced with real stock; missing primary assemblies or terminal dismantling cannot be recreated by payment. Fuel, service history, ownership and closed claims do not reset.

**Gate caravan.** The retained 100+ Load/10%-of-cargo-value reference is a real large service. Its quote must state a finite offered capacity of at least 100 Load, pounds and geometry, occupants, actual journey/route, staff, containers, custody, appraisal base, danger and schedule. Paying the fee does not cross a restricted Gate or move cargo. Staff do not become free expedition combat support.

**Teleport extraction.** The reference is Tier×100 gp for each accepted Extraction Load. The new default rounds the accepted positive total upward to a whole Load once per commissioned bill, unless an actual finite source contract states another rule. Execution still needs a currently operative acquired effect with its full endpoints, range, person/object/mass/volume limits, consent, access, costs and containment. A price table supplies no spell or destination permission. Without that particular procedure/endpoint, that service is unavailable; ordinary transport remains usable.''',
'''The hauler is bound to the separate core.transport.hauler profile. The 500 gp quote and 20/30 Load references are historical; its mass, body, oil, maintenance, control and repair are explicitly new additions. Do not replace these with a class machine's rules because both are called a hauler.

Track exact accumulated moving time, fuel fractions, refill/consumption events, service-due state and actual completed work. A partial service is not completed service, and one work interval cannot also restore HP or recharge another device. A damaged required mechanism must be made serviceable through its real repair before routine service can qualify.

Caravan availability, a real slot and the actual specialist teleport are world inputs. Do not invent infinite capacity, a current spell, post-Opening access, planar permission or spatial-container capacity from a price. Preserve Living/Changed, Pact and deep-setting labels literally for the later review.''')

section(12,'People, stretchers and cargo transfers',
'''A passenger remains an actor. Check the actual seat/occupant geometry, total effective pounds and separate passenger/casualty Load:

| Body size | Passenger/casualty Load |
|---|---:|
| Tiny | 1.5 |
| Small | 3 |
| Medium | 6 |
| Large | 12 |
| Huge | 24, a new completion for these profiles |

Voluntary seated passengers use these burden units without losing their agency or ability to act/exit. A walking crew member does not count as a passenger on someone else. An animal aboard a ship contributes its full body mass and carried cargo once, as well as its passenger Load; a 5,000 lb Elephant is not weightless because it has 24 Load.

An external carrier counts effective body weight and all associated equipment, including melded equipment, once. Petrified multiplies base-body pounds by ten once, without multiplying gear or casualty Load. Personal transformed inventory uses its own different meld rules. One bag cannot be both omitted and treated as a separate extra copy. Count actual blankets, harnesses, frames and containing vehicles. Preserve a source's explicitly approximate ten-pounds-per-Load fallback as an estimate, never relabel it as measured weight or discard known pounds.

**New ordinary stretcher.** The 5 gp, 10 lb frame measures 7×2.5×0.5 feet, with AC 15/5 HP. It supports one fitting Small/Medium patient, with a 300 lb payload limit including their gear and a six-casualty-Load body limit. The frame's own mass is additional carrier burden. Two carriers each need both hands. Assign actual shares before lifting, normally half the combined stretcher, patient and gear to each; each carrier's own gear plus share must fit both limits and their actual supporting position. Shares total exactly the one burden, including equipment Load separately from casualty Load. Coordinated Speed is the slowest eligible carrier after burden, terrain and Strain; one carrier's Dash does not pay the other's movement. A bigger casualty needs a fitting platform/team or exact effect.

**Calm transfers.** One active minute handles one actual discrete fitting bundle of up to 50 lb. An indivisible heavier object needs enough carriers/hoist/support and a declared positive duration for its real feasible lift; it is not divided into fictional fifty-pound slices. A supported person or ordinary mount transfer takes two active minutes, plus real ramp/securement work. Assembling the stretcher takes one minute. Harnessing and seat fitting have their own additional time. Independent workers can handle disjoint loads concurrently; incompatible pulls on one load do not.

Existing shorter access/retrieval procedures remain where genuinely applicable. In initiative, each actual attach, lift or transfer step uses Secure Cargo or another appropriate Action, with the necessary bodies, hands, access and checks. A two-minute calm transfer is not a promise to finish any battlefield lift with one Action.

Safe cooperative transfer can need no roll. A ledge, enemy interference, resistance or inadequate control uses its actual check, contest or attack with declared consequences. Loading does not grant permission for restraint, surgery or a willing-target spell. Unconsciousness, Prone, dying, Wounds and death/stabilization clocks continue during carriage. A belt applies only its real restraint effect, not universal fall protection. Record the actual sender, receiver, location and body/item identities; custody changes do not renew material age or harvest claims.''',
'''Keep distinct body, gear, containers and shares. Petrification changes only the body pounds and never turns six casualty Load into sixty. Reusing a transformed character's personal meld exemption on the outside carrier would omit real weight.

The stretcher's patient admission and each carrier's total burden are independent checks. Its frame and every gear item still count. An unstable transfer can fail even when numerical limits fit; conversely no roll is needed to invent uncertainty in a genuinely safe supported lift.

Preserve voluntary, unconscious, restrained and disputed-custody states separately. Unknown actual landing space or insufficient support is not repaired by a cargo tag. A dead body remains the same history-bearing body under its real lifecycle, not a fresh generic loot bundle.''')

section(13,'One route rate, with real transfers',
'''Route quality, mapping knowledge and Risk are separate. A well-mapped collapsed bridge remains physically collapsed.

| Physical route quality | Travel-time multiplier |
|---|---:|
| Secured | 0.75 |
| Known | 1 |
| Contested | 1.25 |
| Collapsed | 1.50 |

For the ordinary route-work tranche, use:

`480 active minutes × physical quality × (3 ÷ limiting convoy mph)`

An explicit route mode/duration can replace that reference only through its actual rule. The forced Unknown march's nominal 480-minute attempt uses this same normalization, not an additional eight hours or an unadjusted fast pace. Do not award both a route-progress result and a second distance from those same hours.

For these creatures, ordinary travel mph is current otherwise-legal walking Speed divided by ten, after applicable burden, injury and environmental modifiers. Apply the reviewed Strain-5 half-travel penalty once. Watercraft use the actual available propulsion/current ground rate. The convoy is limited by its slowest necessary moving member, puller or carrier. A passenger contributes the carrier's movement, not their own Speed.

An essential stopped, overloaded or unavailable carrier stops convoy progress until a real transfer, repair or route change. Leaving it behind is an actual split or abandonment. A Speed change affects only the remaining route work; preserve completed distance/fractional progress.

The source Secured −1 and Contested +1 threat modifiers adjust effective Pressure for the **single ordinary travel complication check**, clamped 0–6. They do not change stored Pressure or cause another roll. Collapsed adds the actual physical obstacle's +3 difficulty where that obstacle exists. The extraction checkpoint's specific secured −2/pursuit/exposure formula remains separate; do not add a second route modifier for the same secured condition.

Core's Known one-Load, Contested 10% and Collapsed 20%-or-reroute losses are possible predeclared stakes, not automatic additional penalties on a complication or failed extraction check. Choose the consequence model beforehand. A declared percentage uses the current at-risk manifest and actual eligible lots/portions in a predeclared priority, with permitted unit rounding. Never delete part of a person or indivisible object to satisfy the fraction. Unachievable remainder is not banked. Secured's “none” removes that routine table-loss rider, not actual separate danger.

Changing mount, cart or ship takes a real transfer interval with receivers, crew and route ready. Retain Extraction Class, title, custody, material age, identity and closed claims. A transport-mode rename does not cross a checkpoint again. A genuinely new border, exit or handover can be its own declared finite checkpoint.''',
'''Keep route identity and fraction complete before changing the limiting rate. Record actual physical quality independently of Unknown/Sketched/Mapped/Secured mapping knowledge and Risk 1–5. Apply the 480-minute reference only once to the actual work tranche.

Do not use a zero required-carrier speed as a division shortcut or silently omit that actor. Determine the real transfer, abandonment or repair first. Source-specific route/hazard rules override only their actual scope.

For declared cargo loss, retain the original at-risk manifest, event, chosen eligible lots/portions and indivisibility remainder. Do not stack the Core illustration with a Loop consequence unless they are genuinely independent declared effects. Living/Changed and Pact Interdiction remain literal specialist/deep-setting receipts, without invented geography, causes or permissions.''')

section(14,'Recover living creatures; repair actual structures',
'''Living mounts use creature healing, HP, Hit Dice, Wounds, injuries, conditions, rest eligibility, nutrition and their actual lifecycle. Healing can end dying only as its procedure permits. Repair work, a quarter-price bill, insurance, stabling or buying another animal does not revive the dead individual. The ordinary significant-mount default remains distinct from a Ranger Beast's HP-only exception and finite creations. Actual remains use existing once-only harvest rules, not a resource yield invented from price or carrying capacity.

Objects use structural HP and their real material/object defenses. They receive no creature Wounds, death saves or parallel duplicate Integrity penalties.

For a positive-HP or genuinely reparable mundane HP-0 main body, trained appropriate-tool self-repair uses actual compatible materials at 25% of the applicable undamaged mundane body reference, DC 10, and active work of `max(1 hour, recorded maximum HP ÷ 10 hours)`. Apply Core task shifts with the upper two degrees as success and lower two as failure, without extra critical benefits. A 300-HP hull therefore takes thirty active hours, not one Watch or thirty independent restorations.

The worker needs the actually appropriate carpenter, smith or vehicle tools and a workable supported/dry site. A complete qualified service quote at the source's 10%/15% price is alternative pricing, not another 25% material charge. Recipe-magical equipment keeps its own reviewed procedure; the Core hauler uses its specific new repair bridge above.

Success restores the same body's HP to its existing permitted maximum/function. It does not recreate missing primary structure, restore cargo, fuel, charges, service credit, magical imprint, flaws or closed claims unless an actual rule expressly does so. Compatible subordinate parts use actual stock once; the profile's required original primary members must survive. Failure spends actual materials and work. Another permitted attempt requires new inputs, not a free reroll. Terminal dismantling is not merely HP 0. Custody, material age and source clocks continue during repair and storage.

Drawn frames and the hauler at HP 0 are disabled and strand their real load. Unload, transfer, support or tow only through a feasible method. Occupants are not automatically damaged solely because structural HP reaches zero.

**New afloat-hull emergency.** Without a specific different destruction source, a watercraft reaching HP 0 becomes disabled and starts one ten-minute flooding/evacuation deadline. At that deadline its wreck becomes submerged or stranded according to the real depth and support. It is not deleted, and occupants use actual escape, falling, swimming and drowning rules.

Once per actual hull-breaking episode, two capable workers, at least one trained with carpenter's tools or Vehicles (Water), can spend five uninterrupted active minutes and real compatible patch/bracing supplies at 1% of the undamaged body reference, minimum 1 gp. The work must finish before the flooding deadline. Make the appropriate DC 15 tool task using Core shifts collapsed to success/failure. Success holds that same disabled hull afloat for sixty minutes from completion, without restoring HP or propulsion. Failure spends work/materials and leaves the original deadline. Repeating the label cannot reset the same rupture or bank more time.

Real grounding, docking, towing or a hoist can support the still-present wreck for full repair. Rescue uses actual people, tools, locations, mass, Actions and time. It creates no lifeboat, fresh crew, stretcher, survivor or recovered property. Apply ordinary cargo rescue where appropriate and encounter procedures under actual threat. Insurance pays only an eligible recorded loss; it does not automatically repurchase inaccessible unique bodies.''',
'''Distinguish living treatment, mundane structural repair, recipe-magical restoration, the new hauler bridge and one-time emergency shoring. Each uses its real eligibility and source. A payment is not evidence that a missing body, material, worker or worksite exists.

For a damaged vessel, record damage-event ID, HP-0 time, original deadline, shoring eligibility, workers, uninterrupted interval, supplies, result, any sixty-minute hold deadline, actual support and evacuation. The hull does not regain movement from successful shoring. A failed or interrupted attempt cannot backdate completion beyond the old deadline.

Track rescued actors and goods individually, with actual custody, remaining conditions and source history. Keep family admission, overload, control-loss, interrupted-movement, damage/HP-0, repair/rescue and provenance examples as authored expectations. They do not claim that live transport software or human balance has been tested.''')

FAMILY_CASES=[]
def family(fid, kinds, auxiliary_ids, cases):
    FAMILY_CASES.append({'id':fid,'profileKinds':kinds,'auxiliaryIds':auxiliary_ids,'cases':[
        {'id':fid+'-'+str(i+1).zfill(2),'boundary':boundary,'given':given,'expected':expected,
         'evidenceClass':'Authored synthetic expectation; not executed gameplay'}
        for i,(boundary,given,expected) in enumerate(cases)]})

family('TRF-MOUNT',['living-mount'],[],[
 ('admission','A Small rider, fitting saddle and gear fit a willing trained Medium Pony in both pounds and Load.','The body/seat prerequisites can qualify. A Medium rider is still too large for that saddle rule even if equally light.'),
 ('overload','A mule with a420lb/42Load profile has421lb of actual supported rider, tack and cargo.','Routine carriage is unavailable even if its Load is below42. Transfer a real item or choose another feasible method.'),
 ('control-loss','A seated rider becomes incapacitated before the controlled animal executes its cue.','Recheck the cue. The animal retains its existing turn but defensively Dodges if able and uses only its own immediate-safety movement, without a new player attack order.'),
 ('interrupted-movement','A mount has taken its round’s regular turn; a new rider mounts it afterward.','No second turn or fresh budgets occur. A valid new linked position begins next numbered round.'),
 ('damaged-or-zeroHP','An ordinary mount registered as significant before battle reaches0HP.','Use its actual Core dying/death-save and Wound history. Do not retrospectively designate it insignificant or replace it with the different Ranger Beast lifecycle.'),
 ('rescue-repair','A living injured mount is brought to a paid stable; the owner offers its quarter-price as repair.','Only actual creature treatment/rest/healing can recover it. Stabling or object repair cannot heal or resurrect the individual.'),
 ('provenance','The same rescued mule is later sold or enters a legitimate Ranger bond.','Retain its original identity, body, injury, custody and remains history. The source-specific new lifecycle does not create a second animal.')])
family('TRF-BARDING',['fitted-armor'],[],[
 ('admission','A Large trained mount is fitted with an actual reviewed ordinary armor model.','Use baseline price×4, mass×4 and armorHP×2, with the model’s actual AC formula, Dexterity cap and restrictions. Do not multiply its price by the general Large factor again.'),
 ('overload','The chosen barding makes the animal’s actual supported burden exceed its profile limit.','Wearing competence cannot waive weight. Remove or transfer real burden before routine movement.'),
 ('control-loss','The animal loses its valid riding relation while wearing barding.','Armor supplies no controlling cue, willingness or attack. Use the actual loss-of-control procedure.'),
 ('interrupted-movement','A form change makes the currently fitted armor incompatible.','Record actual fit and body effects; transformation does not resize or refit it. No movement is granted by changing the armor label.'),
 ('damaged-or-zeroHP','The barding’s actual armor body becomes Broken.','Resolve that object under its armor rules separately from the animal’s HP. Its damage is not a duplicate creature Wound.'),
 ('rescue-repair','Compatible original barding survives and a trained worker has real replacement fittings.','Repair that sized armor using its own material/value/time requirements, not the whole animal’s price or maximum HP.'),
 ('provenance','The old Barding row has a comma/blank and null numerical weight.','Preserve that original record. The current selected model and new sizing values are separate operating data, not a recovered source weight.')])
family('TRF-TACK',['tack-or-container'],[],[
 ('admission','A pair of saddlebags has a fitting20lb/0.5ft³ load in each real cell.','Admission also requires actual shape, balance, closure and an animal able to carry the4lb bags and contents.'),
 ('overload','One saddlebag cell contains21lb and the other19lb.','The40lb combined total does not excuse the first cell’s20lb limit. Repack a real fitting portion if possible.'),
 ('control-loss','A rider loses their only usable rein hand and the individual has no trained tactile alternative.','A bridle’s presence does not preserve a usable cue. Recheck control at the animal’s execution.'),
 ('interrupted-movement','A saddle fitting is interrupted before its actual fitting work is complete.','Retain elapsed work/cost and the actual attachment state. Do not declare a safe usable seat merely because the item is owned.'),
 ('damaged-or-zeroHP','The actual saddle body is destroyed while its rider is supported by it.','Resolve the real loss of support and landing. ItemHP0 is neither an automatic fixed injury packet nor magical continued seating.'),
 ('rescue-repair','An intact main bag body needs new straps; a qualified worker has actual compatible materials.','Use the ordinary actual object repair procedure. Repair restores that item, not lost contents or another copy of its cargo.'),
 ('provenance','A pack saddle and a military saddle change owners.','Keep their distinct item identities/functions. Neither the pack saddle’s name nor the military name grants a rider seat or feat beyond its actual profile.')])
family('TRF-PROVISION',['consumable-provision','service'],[],[
 ('admission','A real camel-day feed purchase at5cp supplies12lb of compatible stock, and a fitting24h stall is available.','Record actual feed and stall separately. The camel still needs32pints of real water unless the quoted service actually includes it.'),
 ('overload','A pen fits a dog but cannot physically accommodate the named Elephant.','Paying the posted5sp cannot admit the Elephant; find an actual fitting pen. A service has no invented cargo or half-pound capacity.'),
 ('control-loss','The caretaker is unavailable and no replacement has actually taken custody.','Payment does not create supervision, a handler or an animal command. Keep the real custody gap and consequences.'),
 ('interrupted-movement','A caravan stops during a day in which some feed and water have already been consumed.','Keep consumed stock and elapsed work. A transport-mode change or second gate crossing grants no second free ration or new paid day.'),
 ('damaged-or-zeroHP','Stored feed is spoiled and the stable building becomes inaccessible.','Record actual provision loss and service availability; neither service row has fictional creatureHP or a universal repairable zero-HP body.'),
 ('rescue-repair','An injured animal reaches safe boarding and needs treatment beyond ordinary cleaning/supervision.','Use actual additional care, workers, supplies and time. The included ten caretaker minutes do not cure Wounds or replace emergency treatment.'),
 ('provenance','A bundled boarding offer includes identifiable feed and water quantities.','Charge/consume those actual included quantities once, retain the agreement and custody interval, and do not bill the same provided feed twice.')])
family('TRF-DRAWN',['drawn-vehicle'],['core.transport.dungeon-sled'],[
 ('admission','An actual200lb Cart carries a300lb fitting payload under its30Load cap; a trained mule has a600lb draw rating.','Gross draw is500lb, with the mule’s own burden checked separately. The route, harness, driver and seat/occupant limits must also qualify.'),
 ('overload','That Cart is assigned301lb of payload while the puller could tow the resulting gross weight.','The Cart’s300lb payload cap still prevents routine admission. A stronger puller cannot expand the bed or frame rating.'),
 ('control-loss','The driver paid an Action, but a required harness breaks before the last puller contribution becomes available.','The coordinated drive does not resolve without current feasibility. Retain the spent Action and actual body/cargo positions.'),
 ('interrupted-movement','A driver swaps after one linked vehicle event has already moved this round.','The new driver does not grant a second event or restore spent puller movement. Preserve actor and frame history.'),
 ('damaged-or-zeroHP','The30HP Cart reaches0HP on a firm supported road.','Its transport function is disabled and real cargo is stranded. MereHP0 does not destroy the cargo or injure every occupant.'),
 ('rescue-repair','The original Cart frame, main axle and bed survive; real qualified repair is available.','The mundane reference uses25%of15gp=3.75gp materials,DC10 and3 active hours, unless an actual alternative complete service quote controls. No duplicate quarter-price fee.'),
 ('provenance','A20gp Player Sled and25gp Core Dungeon sled appear in the same inventory.','Keep two distinct bodies and profiles. The Core item has its actual two operators,12/20Load and60lb frame, not the Player animal-drawn snow sled’s ratings.')])
family('TRF-WATER',['watercraft'],[],[
 ('admission','Four actual occupants including one oar/helm operator fit a Rowboat’s600lb/60Load total and400lb/40Load cargo sublimit.','They can qualify only with actual geometry, at least1ft water depth, working oars/controls and a feasible route; the price supplies no fifth seat or crew.'),
 ('overload','A cargo-light Rowboat has five occupants.','The four-person cap still fails. Low body weight does not create another seat.'),
 ('control-loss','A Galley’s selected oar mode lacks one of its41 required active workers.','It cannot perform that staffed drive event. An actually available sail mode needs its own8 workers and usable wind; drift is only actual environmental movement.'),
 ('interrupted-movement','Earlier crew Actions are paid, then the helm becomes unable before the final contribution.','Do not presume a future helm Action. The event fails its current feasibility while paid contributions remain spent; a helm swap cannot yield a second event.'),
 ('damaged-or-zeroHP','An afloat Rowboat reaches0HP at campaign second1000 with no overriding destruction rule.','Disable propulsion and set the one flooding deadline at1600. Touching or renaming the hull does not restart it.'),
 ('rescue-repair','Two eligible workers shore that hull from1050to1350 with an actual1gp minimum patch and succeedDC15.','It remains disabled afloat until4950, sixty minutes after completion. NoHP or propulsion returns. The same rupture cannot buy another shoring interval.'),
 ('provenance','The wreck is grounded on real support and recovered for full repair.','Retain hull/primary-part IDs, actual lost cargo, costs and deadlines. Full repair needs the existing main body; a quotation cannot recreate a missing keel or lifeboat.')])
family('TRF-HAULER',[],['core.transport.hauler'],[
 ('admission','The actual intact hauler has a fitting200lb/20Load payload, available oil and a qualified usable local operator.','NormalSpeed30ft/3mph is possible only on a real clear firm route with the adjacent operator’s two hands and paid Action/time.'),
 ('overload','A fitting emergency load is250lb/25Load; a proposed replacement is301lb.','The first uses emergencySpeed5ft/0.5mph if otherwise feasible. The second exceeds the hard pound cap and cannot move routinely, even if Load fits.'),
 ('control-loss','The operator is more than5ft away with no access to the controls.','No commanded propulsion occurs. A class remote-binding feature is not automatically this separate hauler’s control procedure.'),
 ('interrupted-movement','Two active moving hours consume part of one pint, followed by a stationary pause.','Consume exactly1/4pint for the moving interval. The pause does not consume propulsion fuel or reset that history; actual leaks remain separate.'),
 ('damaged-or-zeroHP','The hauler reaches0HP with its original primary frame, drive and controller still present.','Transport stops. Its explicit reconstruction bridge needs8 active hours,DC15 and125gp actual compatible materials; no creature death saves or mundane magical salvage shortcut.'),
 ('rescue-repair','At40 moving hours the intact mechanism receives one hour of qualified service and an actual1gp/0.5lb pack.','Service clears the due-service counter only. RepairHP, fuel and lost parts remain separate, and the worker cannot claim that hour as rest.'),
 ('provenance','A recipe automaton, a class device and core.transport.hauler share a descriptive name.','Keep their full distinct source identities, controls, resource rules and body histories. This transport body gains noRP, attacks, class commands or harvested magical output.')])
family('TRF-AUXILIARY',[],['NEW.transport.draw-harness','NEW.transport.stretcher'],[
 ('admission','Two capable carriers prepare the10lb stretcher for a180lb Medium patient with20lb gear, using both hands each.','The200lb patient/gear payload and6casualtyLoads fit; each normally supports105lb plus their own gear, with actual equipmentLoad shares and positions also checked.'),
 ('overload','A stretcher is offered a301lb patient/gear payload, or a single Medium harness is proposed for an incompatible Huge puller.','Neither fits its actual profile. More payment or spare unrelated Load cannot substitute the fitting stretcher or32lb Huge harness.'),
 ('control-loss','One stretcher carrier releases the required support, or a puller’s draw harness loses its attachment.','Resolve the real supported load and possible fall/stranding. The auxiliary item does not create another worker, balance or remote control.'),
 ('interrupted-movement','One carrier Dashes while the other has only ordinary movement remaining.','Coordinated motion remains bounded by the slower eligible carrier’s paid movement. No forced free Dash is assigned to the other.'),
 ('damaged-or-zeroHP','The actual stretcher or harness body breaks under load.','Resolve its real loss of support/attachment and actual landing or stranded frame. Its5HP is not an extra patientHP pool.'),
 ('rescue-repair','A suitable replacement fitting is available but the original primary body must be preserved for repair.','Use real compatible parts, qualified work and the actual repair rule; lifting/transferring the patient still takes its own support and time.'),
 ('provenance','The supported patient moves to another carrier after one failed harvest claim on a separate corpse.','Keep each body/item and claim identity distinct. A new carrier does not change material age, revive the patient, or reopen the corpse’s terminal claim.')])

CASES=[
 {'id':'TRX-01','questions':['TR-02'],'given':'A willing animal completes the40-hour ordinary training course at its maximum4 credited hours/day.','expected':'At least10 training days are required; two instructors cannot create an8-hour animal training day.'},
 {'id':'TRX-02','questions':['TR-03','TR-05'],'given':'A rider acts, then its mount begins its whole turn and moves into a new reach.','expected':'The rider has no inserted free turn segment. A previously legal readied Action still needs its Reaction and actual trigger.'},
 {'id':'TRX-03','questions':['TR-04'],'given':'A rider’s current walkingSpeed is31ft with15ft of regular movement left.','expected':'One ordinary mount costs15ft and can fit the budget if all other predicates hold. Speed1 costs1ft; Speed0 cannot mount.'},
 {'id':'TRX-04','questions':['TR-04'],'given':'One source event pushes the mount and knocks it Prone.','expected':'One binaryDC10DEX seat save, not two. Rider success preserves seating only where the real body still supports it.'},
 {'id':'TRX-05','questions':['TR-05'],'given':'A mount voluntarily leaves an enemy’s reach; the seat is outside that enemy’s legal reach.','expected':'The enemy may attack the mount if its own predicates hold, but cannot choose an unreachable rider. OneReaction buys one attack.'},
 {'id':'TRX-06','questions':['TR-05'],'given':'Only the rider used Disengage before the mount’s voluntary provoking movement.','expected':'The mount’s provocation remains. Only the mount’s own valid Disengage removes the mounted target-choice opportunity for its movement.'},
 {'id':'TRX-07','questions':['TR-06'],'given':'A Dragoon rides30ft and then casts without self-propelled movement on its own turn.','expected':'No Momentum movement gain and no new transport-bridge twenty-foot casting benefit; physical position is still real for range/auras.'},
 {'id':'TRX-08','questions':['TR-06'],'given':'A Dragoon actually travels20ft under its own power on its current regular turn before a legal Weave cast.','expected':'Apply the actual one movement gain if its engine predicates hold and the separate Dissonance−1 minimum0. NoRP discount or extra threshold gain.'},
 {'id':'TRX-09','questions':['TR-07'],'given':'A reviewed armor baseline costs50gp and weighs20lb; its compatible Large barding is selected.','expected':'The ordinary references are200gp and80lb. Do not charge400gp by also applying general Large pricing.'},
 {'id':'TRX-10','questions':['TR-08'],'given':'A mule with600lb draw rating pulls a200lb cart plus100lb total payload.','expected':'Gross300lb equals half draw rating, so the strictly-above-half draw condition alone does not apply. Its own positive carried burden at half its separate carry cap still does.'},
 {'id':'TRX-11','questions':['TR-09'],'given':'A sail mode’s stated rate is4mph with adverse but usable wind and a1mph countercurrent.','expected':'Relative propulsion is2mph and along-route ground progress1mph under these stated vectors; no second wind multiplier or unstated calm assumption.'},
 {'id':'TRX-12','questions':['TR-09'],'given':'The ship has no usable wind and the selected mode is sail only.','expected':'Sail self-propulsion is0. The real current may still drift it; purchase, crew Actions or a high check cannot invent wind.'},
 {'id':'TRX-13','questions':['TR-10'],'given':'One porter accepts the named2sp/day service and ordinary double danger rate.','expected':'The agreed rate is4sp for that service day, not generic dangerous unskilled wages plus4sp. Actual contracted cargo and body limits still apply.'},
 {'id':'TRX-14','questions':['TR-11'],'given':'A genuineTierII teleport service accepts a single commissioned2.1Load bill, with an actual operative effect and endpoints.','expected':'Round the total to3Load once, for600gp under this reference. Without the actual effect/endpoint, the price alone supplies no teleport.'},
 {'id':'TRX-15','questions':['TR-12'],'given':'A180lb Medium body becomesPetrified while carrying20lb gear.','expected':'An external carrier bears1820lb and the same6casualtyLoads plus equipmentLoad. Do not multiply gear or casualtyLoad by10.'},
 {'id':'TRX-16','questions':['TR-12'],'given':'Three separate fitting40lb bundles and one indivisible120lb statue require calm loading.','expected':'The three bundles require three actual one-minute units; the statue needs its real team/hoist and separately declared positive duration, not automatic fifty-pound slicing.'},
 {'id':'TRX-17','questions':['TR-13'],'given':'A480-minute nominal route tranche hasContested quality1.25 and an actual2mph limiting convoy.','expected':'It requires900 active minutes. No extra480 minutes or duplicate hourly distance is awarded.'},
 {'id':'TRX-18','questions':['TR-13'],'given':'Half aKnown route tranche is completed at3mph, then the limiting rate falls to1.5mph.','expected':'The first240 active minutes remain completed; the other half needs480 more, for720 total. Do not retroactively double completed work.'},
 {'id':'TRX-19','questions':['TR-13'],'given':'StoredPressure is6 on aContested ordinary travel-complication check.','expected':'EffectivePressure clamps to6 for that one check; storedPressure remains6 and no extra roll is created.'},
 {'id':'TRX-20','questions':['TR-14'],'given':'A300HP mundane hull has an eligible original body and full qualified repair inputs.','expected':'Ordinary self-repair requires30 active work hours, not one eight-hourWatch. A genuine alternative complete service quote is not charged another25%.'},
]

def render(env,audience):
    lines=[f'# {audience.title()} expedition procedures — mounts, transport and rescue','',env['notice'],'',
           'Use with the [complete transport catalogue](TRANSPORT_CATALOGUE_CANDIDATE.md), [body and equipment rules](../BODY_EQUIPMENT_PLAYTEST.md), [Core resolution](../CORE_RESOLUTION_PLAYTEST.md), [routes and extraction](EXPEDITION_PART02_PLAYER.md), and [Haven services](EXPEDITION_PART03_PLAYER.md).','']
    if audience=='director':lines+=['Read the complete [player transport chapter](EXPEDITION_PART05_PLAYER.md) alongside these Director procedures.','']
    for s in env['sections']:lines+=['## '+s['title'],'',s['text'],'']
    if audience=='director':
        lines+=['## Family boundary examples','','These are authored synthetic expectations. They do not authenticate a campaign animal, crew, route, provider or operation.','']
        for f in env['familyCases']:
            lines+=['### '+f['id'],'','Profiles covered: '+', '.join(f['profileIds']+f['auxiliaryIds'])+'.','']
            for c in f['cases']:lines+=['**'+c['boundary']+' — '+c['id']+'.** '+c['given'],'',c['expected'],'']
        lines+=['## Turn, accounting and route examples','']
        for c in env['workedCases']:lines+=['### '+c['id'],'',c['given'],'',c['expected'],'']
    return '\n'.join(lines)

def main():
    paths={'public':R/'data/public/expedition_candidate/part05.json','internal':R/'data/director/expedition_candidate/part05.json',
           'player':R/'docs/mechanics/expedition/EXPEDITION_PART05_PLAYER.md','director':R/'docs/mechanics/expedition/EXPEDITION_PART05_DIRECTOR.md',
           'receipt':A/'EX58_CANDIDATE_PART05_CHECK.json'}
    assert not any(p.exists() for p in paths.values()),'Preserve existing outputs before revision'
    checks=[]
    def ck(n,v):
        checks.append({'name':n,'pass':bool(v)});assert v,n
    manifest=read(P/'FILE_MANIFEST.json')
    for x in manifest['files']:ck('Original verdict unchanged '+x['path'],info(P/x['path'])=={k:x[k] for k in ['bytes','sha256']})
    for correction in ['EX58_EDIT_01_FULFILLMENT.json','EX58_EDIT_02_FULFILLMENT.json']:
        for rel,expected in read(A/correction)['descendants'].items():ck('Confirmed correction descendant '+rel,info(G/rel)==expected)
    for rel,expected in read(A/'EX58_TRANSPORT_CATALOGUE_CANDIDATE_CHECK.json')['outputs'].items():ck('Bound transport catalogue unchanged '+rel,info(G/rel)==expected)
    profiles=read(R/'data/public/expedition_candidate/transport_profiles.json')
    full_catalogue=read(R/'data/director/expedition_candidate/transport_profiles.json')
    ck('Full catalogue public envelope parity',profiles==full_catalogue['publicEnvelope'])
    original_profiles=read(P/'EX58_TRANSPORT_PROFILES.json')
    ck('All original transport source rows preserved',full_catalogue['completeOriginalProfileEnvelope']==original_profiles)
    for f in FAMILY_CASES:f['profileIds']=[p['id'] for p in profiles['profiles'] if p['kind'] in f['profileKinds']]
    boundary_names={'admission','overload','control-loss','interrupted-movement','damaged-or-zeroHP','rescue-repair','provenance'}
    for f in FAMILY_CASES:ck('All seven family boundaries '+f['id'],{c['boundary'] for c in f['cases']}==boundary_names)
    ck('Every original profile has family coverage',{p['id'] for p in profiles['profiles']}=={p for f in FAMILY_CASES for p in f['profileIds']})
    ck('Every auxiliary has family coverage',{p['id'] for p in profiles['auxiliaryProfiles']}=={p for f in FAMILY_CASES for p in f['auxiliaryIds']})
    directions=read(R/'data/director/expedition_candidate/source_register_corrected.json')['directions'];by={d['id']:d for d in directions}
    original_by={d['id']:d for d in read(P/'EX58_AUTHORING_REGISTER.json')['directions']}
    ids=[s['id'] for s in SECTIONS]
    ck('All fourteen transport directions in order',ids==[f'TR-{i:02d}' for i in range(1,15)])
    prior=read(R/'data/director/expedition_candidate/part04.json')['cumulativeAuthoredQuestionIds']
    ck('Prior38directions complete and distinct',len(prior)==len(set(prior))==38)
    for q in ids:ck('Transport source direction unaffected by scoped corrections '+q,by[q]==original_by[q])
    preparation=read(A/'TRANSPORT_SOURCE_PREPARATION.json')
    ck('All29 original equipment rows exactly preserved',preparation['sourceEquipmentRecords']==[p['sourceRecord'] for p in original_profiles['profiles']])
    comparison=read(P/'EX58_CLASS_INTERFACE_DISPOSITIONS.json')
    dragoon_path=R/'data/public/class_playtests/dragoon.json';dragoon=read(dragoon_path)
    bound_dragoon=next(c for c in comparison['classFiles'] if c['path']==dragoon_path.relative_to(G).as_posix())
    ck('Whole Dragoon source unchanged',info(dragoon_path)['sha256']==bound_dragoon['fileSha256'])
    ck('Both original pending mounted feats retained',comparison['pendingMountedFeatComparisons']==preparation['pendingFeatComparisons'])
    names=['CORE_RESOLUTION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md',
           'LANGUAGE_COMMUNICATION_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','CRAFTING_HARVEST_PLAYTEST.md','CLASS_PLAYTEST_RULES.md','STRAIN_PLAYTEST.md','GAMEPLAY_LOOP_CANON.md']
    sources=[R/'docs/mechanics'/n for n in names]
    full_sources=[]
    for p in sources:
        ck('Governing source available '+p.name,p.is_file());full_sources.append({'path':p.relative_to(G).as_posix(),**info(p),'completeText':p.read_text('utf-8-sig')})
    public={'schemaVersion':1,'moduleId':'EX58-PART05','status':'authored-partial-candidate-awaiting-exact-review',
            'notice':'Working chapter module 5, authored from the agreed transport decisions and complete profile catalogue. Reputation and integrated records remain to assemble before exact candidate review.',
            'questionIds':ids,'completeExpeditionCandidate':False,'selectionEnabled':False,
            'catalogue':{'path':'data/public/expedition_candidate/transport_profiles.json',**info(R/'data/public/expedition_candidate/transport_profiles.json')},
            'sections':[{'id':s['id'],'title':s['title'],'text':s['player']} for s in SECTIONS]}
    director={'notice':public['notice'],'sections':[{'id':s['id'],'title':s['title'],'text':s['director']} for s in SECTIONS],'familyCases':FAMILY_CASES,'workedCases':CASES}
    contracts=read(R/'data/director/expedition_candidate/source_contracts_corrected.json')['contracts']
    internal={'schemaVersion':1,'moduleId':public['moduleId'],'status':public['status'],'sourceReview':'EX58-SOURCE-2026-10-11','completeExpeditionCandidate':False,
              'authoredQuestionIds':ids,'cumulativeAuthoredQuestionIds':prior+ids,'remainingSourceDirections':[d['id'] for d in directions if d['id'] not in prior+ids],
              'publicEnvelope':public,'directorModule':director,'completeCurrentDirections':[by[q] for q in ids],'completeOriginalDirections':[original_by[q] for q in ids],
              'completeTransportCatalogueCandidate':full_catalogue,'completeTransportSourcePreparation':preparation,
              'completeCurrentContracts':[c for c in contracts if c['id'] in ['EC-02','EC-03','EC-05','EC-07','EC-08','EC-14','EC-15']],
              'fullGoverningSources':full_sources,'completeClassInterfaceDisposition':comparison,
              'completeDragoonEnvelope':{'path':dragoon_path.relative_to(G).as_posix(),**info(dragoon_path),'completeEnvelope':dragoon},
              'allClassEnvelopesSource':{'path':'DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part04.json',**info(R/'data/director/expedition_candidate/part04.json'),'pointer':'/completeClassDatasetEnvelopes','count':17,'cards':1223},
              'audienceBoundary':'General transport rules and full ordinary profiles only. No faction secrets, real saved history or deep-setting interpretation.',
              'semanticCoverageNote':'Fourteen complete directions authored with full profiles and family boundary examples. Local checks establish preservation and representation/reference consistency, not full campaign simulation or human balance.',
              'newPromotions':0,'runtimeImplemented':False,'examplesAreRuntimeTests':False}
    for rel,expected in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
        if rel!='README_EXPEDITION_INTEGRATED_V3.md':ck('Original submitted current file preserved '+rel,info(G/rel)==expected)
    calculations=[
      ('basic animal training days',Fraction(40,4),10),('armor training days',Fraction(8,4),2),('40hour quarter-hour phases',40*4,160),
      ('odd-speed mounting cost',31//2,15),('positive one-foot speed mounting cost',max(1,1//2),1),
      ('one combined seat event',len({'push-prone-event','push-prone-event'}),1),('one actor turn despite controller labels',len({'mule-round7','mule-round7'}),1),
      ('Large barding price',50*4,200),('Large barding mass',20*4,80),('Huge barding mass',20*8,160),
      ('saddlebag independent cells',20+20,40),('cart gross draw',200+300,500),('cart half-draw comparison',300>600/2,False),
      ('water clearance',Fraction(1,2)+Fraction(1,2),1),('adverse wind then countercurrent',4*Fraction(1,2)-1,1),
      ('named dangerous porter cp',20*2,40),('hauler two-hour fuel fraction',Fraction(2,8),Fraction(1,4)),
      ('hauler forty-hour fuel throughput',Fraction(40,8),5),('teleport round once',-(-Fraction(21,10)//1),3),('TierII rounded teleport quote',2*100*3,600),
      ('Petrified body plus gear',180*10+20,1820),('stretcher equal pound shares',Fraction(180+20+10,2),105),
      ('patient mass not frame mass',180+20,200),('Contested2mph tranche',480*Fraction(5,4)*Fraction(3,2),900),
      ('prospective half-route speed change',240+240*2,720),('effective Pressure clamp',max(0,min(6,6+1)),6),
      ('cart repair material gp',15*Fraction(1,4),Fraction(15,4)),('cart repair hours',max(1,Fraction(30,10)),3),
      ('300HP repair hours',max(1,Fraction(300,10)),30),('rowboat patch minimum gp',max(1,50*Fraction(1,100)),1),
      ('flooding deadline',1000+10*60,1600),('shoring interval',1350-1050,5*60),('successful disabled hold endpoint',1350+60*60,4950),
    ]
    for name,actual,expected in calculations:ck('Bounded reference '+name,actual==expected)
    rendered={'player':render(public,'player'),'director':render(director,'director')}
    save(paths['public'],public);save(paths['internal'],internal)
    for audience in ['player','director']:
        paths[audience].parent.mkdir(parents=True,exist_ok=True);paths[audience].write_text(rendered[audience],encoding='utf-8',newline='\n')
    ck('Complete public envelope parity',read(paths['public'])==read(paths['internal'])['publicEnvelope'])
    ck('Complete player chapter parity',paths['player'].read_text('utf-8')==render(read(paths['public']),'player'))
    ck('Complete Director chapter parity',paths['director'].read_text('utf-8')==render(read(paths['internal'])['directorModule'],'director'))
    ck('Full source preparation preserved',read(paths['internal'])['completeTransportSourcePreparation']==preparation)
    ck('Full catalogue preserved in module',read(paths['internal'])['completeTransportCatalogueCandidate']==full_catalogue)
    links=[]
    for audience in ['player','director']:
        for target in re.findall(r'\]\(([^)]+)\)',paths[audience].read_text('utf-8')):
            ck('Actual local link '+target,(paths[audience].parent/target).resolve().is_file());links.append(target)
    for x in manifest['files']:ck('Original verdict preserved after authorship '+x['path'],info(P/x['path'])=={k:x[k] for k in ['bytes','sha256']})
    receipt={'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'moduleId':public['moduleId'],
             'status':'All fourteen TR directions authored;52of58 directions drafted across five module pairs. Six reputation directions and full integrated records remain before exact review.',
             'questionIds':ids,'cumulativeQuestionIds':prior+ids,'remainingDirections':len(internal['remainingSourceDirections']),
             'familyExamples':sum(len(f['cases']) for f in FAMILY_CASES),'familyCount':len(FAMILY_CASES),'additionalWorkedCases':len(CASES),
             'workedCases':sum(len(f['cases']) for f in FAMILY_CASES)+len(CASES),'referenceChecks':len(calculations),
             'originalProfilesBound':29,'auxiliaryProfilesBound':4,'localLinkChecks':len(links),'checks':len(checks),'failures':[c for c in checks if not c['pass']],
             'outputs':{p.relative_to(G).as_posix():info(p) for k,p in paths.items() if k!='receipt'},'builder':{'path':Path(__file__).resolve().relative_to(G).as_posix(),**info(Path(__file__))},
             'scope':'Source/profile/class preservation, complete chapter/data parity, family-example coverage, real links and finite reference arithmetic. Not live transport, actual crew/world validation or human balance.',
             'runtimeTestsExecuted':0,'newPromotions':0,'realSavesReadOrWritten':0,'sourceInformationDeleted':0,'details':checks}
    save(paths['receipt'],receipt);print(json.dumps({k:receipt[k] for k in ['moduleId','remainingDirections','workedCases','checks','failures','outputs']},indent=2))

if __name__=='__main__':main()
