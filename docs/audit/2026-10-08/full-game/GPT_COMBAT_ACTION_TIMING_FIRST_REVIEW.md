The **bounded periodic-family package can close** as **REVIEWED / reference-VALIDATED within its stated scope**. The two material fixes are now implemented: source-qualified records exclude duplicate Core fallback creation, and condition-suppressed records keep clocks but do not compete for damaging arbitration, while damage-type immunity is applied only after winner selection. The reported 84 interface checks, 57 definitions, 14 hooks, 114 exact source references, plus the existing generic-condition suite support that bounded status. DD16 correctly remains open. Pasted text

For this next pass, I would use the following precedence: **Core V2 combat rules → compatible V6 detail → existing shared-class integration where it already resolves a gap → clearly marked NEW overlay only where those sources still leave execution ambiguous.** Core establishes the field/initiative/action framework and the action/stance/maneuver lists; V6 supplies the detailed turn, movement, Ready, opportunity-attack, grapple/shove and cover procedures. Pasted text Pasted text

# Combat / time / action integration candidate

## 1. Rounds, initiative, entry, surprise

A **round** is approximately six seconds. A **regular initiative turn** means the creature's normal fixed initiative slot, even when it cannot actually act. Extra turns are not regular turns.

Initiative is:

`d20 + Dexterity modifier + legal initiative bonuses`

Highest acts first. Player/player ties are resolved by those players. Any tie involving an NPC or monster is resolved by the Director. Once resolved, tied order remains fixed for that encounter. Pasted text

### NEW — reinforcement entry

Standard reinforcements arriving through Core's end-of-round encounter clock enter during that end-round phase, roll initiative, and first act at their regular slot in the **next** round.

If an explicit effect introduces a creature during a round:

- roll/assign its initiative immediately;
- if its complete ordered slot is still upcoming, it can take its first regular turn this round;
- if that slot has already passed, its first regular turn is next round;
- entering during the exact slot it would occupy counts as that slot already having passed.

Creature-specific summon timing, such as “acts immediately after owner,” overrides this generic procedure.

### Surprise

V6 explicitly removes movement and the Action on the surprised creature's first turn and blocks Reactions until that turn ends. Pasted text

**NEW clarification:** for this playtest, “cannot take an action” during the surprised first turn also prevents a Bonus Action. It does **not** make the creature Unconscious or Incapacitated.

A surprised first regular turn still:

- exists for recharge counters;
- advances source/target duration clocks;
- resolves start/end-turn periodic effects;
- resolves concentration normally;
- resolves passive effects;
- permits brief communication and an otherwise legal simple free interaction.

The creature cannot voluntarily move, take its Action or Bonus Action, or use a Reaction before that first turn ends.

Extra turns never create additional periodic ticks, recharge ticks, reaction refreshes, or recovery ticks unless an effect expressly says otherwise.

---

# 2. Reaction timing

There is a real wording conflict: Core/V6 summarize this as “one reaction per round,” while V6 and the existing shared class integration refresh the resource at the start of the creature's own turn. Pasted text Pasted text Pasted text

I recommend retaining the already-operational **own-turn interval**.

### Active provisional rule

> A creature has one Reaction resource **between starts of its regular turns**. It refreshes at the start of each regular initiative turn. Extra turns do not refresh it.

This explicitly supersedes a literal global “one per numbered round” interpretation.

### Initial reaction

At encounter start, a non-surprised participant begins with its Reaction available.

Therefore a creature acting late in round 1 can:

1. use its initial Reaction before its first turn;
2. refresh at the start of its first regular turn;
3. potentially use another Reaction afterward in the same numbered round.

That is intentional under this interval model.

A surprised creature's initial Reaction is suppressed until its first regular turn ends.

### Reinforcements

A reinforcement begins with its Reaction available when it enters unless the entry rule explicitly makes it surprised or otherwise reaction-disabled.

### Round boundary

The numerical round changing does **not** refresh Reactions.

An end-of-round hazard may trigger a Reaction if the creature currently has one available and the trigger is legal.

### Extra turns

No refresh.

### Ready

A Ready release spends the normal Reaction resource. If that Reaction has already been spent, the readied action cannot release.

---

# 3. Duration conventions

Keep the shared existing rule that an unqualified `end next turn` refers to the **user/source**, unless the card explicitly says target's. Pasted text

Add these finite conventions.

### Hostile target-bound effects

**NEW:** if a hostile rider says simply **“N rounds”** and supplies no other endpoint, it ends after the end of the target's **Nth future regular turn** after application.

Example:

- Judged applied now for 2 rounds.
- Target's next regular turn ends: 1.
- Following regular turn ends: 2 → Judged ends.

A turn already in progress when the effect is applied does not count unless the source explicitly says “this turn.”

### Self/source buffs and source-controlled auras

If a self/source effect says simply **“N rounds”**, it ends at the **start of the source's Nth future regular turn** after activation.

Example: activated during source turn 1 for 3 rounds → ends at start of source turn 4.

This matches the existing three-pulse convention where activation is pulse 1 and following regular turns supply later pulses. Pasted text

### Skipped or denied turns

The regular slot still occurs and counts. Stun, surprise, Action denial, unconsciousness, etc. do not freeze durations unless the effect explicitly pauses them.

### Extra turns

Never advance a regular-turn duration.

### Out of initiative

One round-equivalent = six elapsed seconds.

A duration already running out of initiative keeps its actual elapsed-time deadline if initiative begins; entering initiative does not restart it.

When a marker-based duration leaves initiative, each remaining regular-turn interval converts to six seconds from the last relevant resolved marker. Do not restart completed intervals.

### Timing order at a regular slot

**NEW deterministic ordering:**

At **start of regular turn**:

1. effects ending “at start of turn” expire;
2. Reaction refreshes;
3. recharge counters tick;
4. start-turn damage/effects resolve;
5. the creature begins normal turn decisions.

At **end of regular turn**:

1. end-turn triggered effects, damage, saves and maintenance checks resolve;
2. effects ending “at end of turn” expire;
3. the initiative slot is complete.

After the final slot, Core end-of-round hazards, reinforcements, morale, objectives and boss phases resolve. Pasted text

---

# 4. Ready

V6 lets a creature Ready either an action or movement up to Speed and specifically says a readied spell is **cast when readied and held with concentration**. Pasted text

### Declaration

Spend the Action now and state:

- the perceivable trigger;
- the action or movement being prepared.

Ready lasts until the start of your next regular turn unless released earlier.

### Trigger timing — NEW

Unless the prepared effect explicitly says it interrupts or occurs before something, the trigger first becomes true, then the readied response resolves **immediately afterward**, before the triggering creature continues with later events.

Opportunity Attacks retain their explicit special timing immediately before the creature leaves reach.

### Legality at release

Re-check:

- Reaction availability;
- target legality;
- range;
- line of effect;
- ammunition;
- other prerequisites.

If release is illegal, nothing is spent at that moment and the Ready remains pending until another valid occurrence or expiry.

### Resource costs

For an ordinary nonspell readied action:

- Ready consumes the Action now;
- feature/resource/ammunition costs are paid when the action releases, unless its text says the setup itself costs them.

For a **readied spell**:

- the spell is cast immediately when Ready is declared;
- RP and other cast costs are paid then;
- Dissonance and Refrain happen then, once;
- its normal concentration is established then;
- beginning that concentration ends any incompatible previous concentration before the held spell is ready;
- losing concentration loses the held spell;
- if never released before Ready expires, the paid spell is lost and costs are not refunded.

### Readied Attack

Because V6 says Ready prepares an **action**, and Attack itself can contain multiple attacks when an explicit class feature grants them, a generic readied **Attack Action uses the attack count that creature's ordinary Attack Action legally has**.

Do **not** invent an off-turn one-attack restriction.

However:

- riders restricted to “your regular turn” remain unavailable;
- once/turn and once/round limitations still apply;
- readied Core **Overwatch** is different because its source expressly says **a ranged attack**, singular. Pasted text

### Readied movement

Ready movement spends:

- Action when prepared;
- Reaction when released.

It grants movement up to Speed, not Dash, and grants no free Action, Bonus Action or object interaction during the release.

Normal opportunity attacks may occur.

---

# 5. Standard Actions

Core's listed Actions remain operative. Pasted text

### Attack
Use attacks legally granted by class and weapon.

### Cast
Cast an Action-time spell or activate a Resonance technique whose activation is an Action.

### Dash
Gain additional movement equal to Speed.

**NEW multiple-speed handling:** for a Dash turn, double each movement mode's available Speed for purposes of the existing mode-switch calculation. Distance already traveled still subtracts from the newly selected mode's available total.

Speed 0 → Dash grants 0.

### Disengage
Voluntary movement does not provoke opportunity attacks for the rest of that turn.

### Dodge
Use the compatible V6 details:

- visible attacks against you have disadvantage;
- Dexterity saves have advantage;
- lasts until start next turn;
- ends/does not function while Incapacitated or Speed 0. Pasted text

### Guard

Gain +2 AC against the **first attack made against you** before your next turn and enable Interpose.

The first attack consumes the +2 benefit whether that attack ultimately hits or misses.

The underlying Guard state persists until the next turn for Interpose even after the +2 has been consumed.

### Guard + Guarded stance

They are separate Core options and may coexist.

Guarded stance's +1 AC and Guard's conditional +2 therefore produce +3 against the first qualifying attack, unless another rule expressly prohibits their combination.

After that attack, only Guarded's +1 remains.

### Interpose

Reaction while Guarding, declared **after an adjacent ally is selected as the attack target but before the attack roll**.

You may move up to 5 feet to a legal position and become the target only if you are yourself a legal target of the same attack after moving:

- in range;
- valid creature type;
- line of effect;
- no total-cover contradiction.

Interpose does not negate the attack or create another attack.

It spends your normal Reaction.

If this is the first attack against you since Guard began, the Guard +2 AC applies and is consumed by this attack.

### Aim

Core says:

> do not move; gain +2 to one ranged or spell attack before end of turn. Pasted text

Do **not** rewrite this into a free bonus.

To Aim:

- you must not already have spent voluntary movement this turn;
- after Aiming you cannot voluntarily move for the rest of that turn;
- forced movement does not cancel the Aim benefit.

Aim consumes the Action. Therefore the +2 is useful only if the character subsequently has another legal ranged/spell attack through:

- a Bonus Action;
- the shared extra-Action allowance;
- another expressly granted attack.

If none exists, the Aim was simply unused.

### Help

Use V6's combat detail:

- ability check: grant advantage to a legal ally's next relevant check before your next turn;
- attack assistance: choose a creature within 5 feet of you; ally's first attack against it before your next turn has advantage. Pasted text

### Hide / Search
Defined under vision below.

### Use Object

One ordinary free interaction exists on your own turn.

A second ordinary object interaction, or an object whose activation requires an Action, uses **Use Object**. Pasted text

### Improvise

Director states before the roll:

- ability;
- proficiency if any;
- DC/opposed method;
- intended consequence.

No hidden extra condition or action grant is inferred from success.

---

## Brace — NEW bounded procedure

Core names the situations but supplies no executable mechanics. Pasted text

Choose one mode when taking Brace:

**Intercept:** choose a doorway/breach edge or your current melee reach. Until start next regular turn, when one hostile creature charges, leaps or breaches into that chosen area, you may spend your Reaction to make **one melee weapon attack** against it immediately after it enters your reach and before it continues later movement/actions.

**Hold Ground:** until start next regular turn, the first time an effect would forcibly move you, spend your Reaction to reduce that forced movement by **5 feet**, minimum 0. This does not prevent other consequences such as damage or Prone unless their source says they depend on the prevented movement.

One Brace gives one Reaction opportunity.

---

## Rally — NEW bounded procedure

Choose one ally within **30 feet** that can perceive your rally by an appropriate sense.

Make a Charisma check against:

1. the Frightened/source morale DC, if one exists;
2. otherwise DC 10.

Success or Critical Success ends one Frightened condition on that ally.

If a separate morale subsystem defines a Rally interaction, use that source instead. Rally does not create temporary HP, advantage, loyalty or compelled behavior by itself.

---

# 6. Combat stances

A creature may have only one standard Core stance at a time.

Choose it once on your turn **before resolving the first attack, spell, save/check or movement event that would be affected by a stance**. You cannot switch retrospectively after seeing that result.

If no stance-relevant event occurs, you may still choose a stance before the turn ends.

The stance lasts until the start of your next regular turn. Extra turns do not expire or refresh it. Pasted text

### Aggressive
+2 weapon-attack damage, -2 AC.

The +2 applies once to each qualifying weapon attack's damage packet, not periodic/copy damage.

### Guarded
+1 AC; advantage on the defender's Athletics/Acrobatics contest or other explicit roll to resist a Shove.

Speed -5 feet, minimum 0.

### Mobile
The first 5 feet of **actual voluntary movement** during the stance does not provoke opportunity attacks. This grants no free movement.

Opportunity attacks you make reduce their **base weapon damage die size** one step:

`d12 → d10 → d8 → d6 → d4`

`d4` is the minimum.

For multi-die base weapon profiles, each base die steps down once. Bonus/rider dice do not step down unless expressly part of the base weapon die.

This die sequence is **NEW**.

### Focused
Choose when casting one spell during the stance:

- +1 to that spell's save DC; **or**
- +1 to one spell attack roll from it.

The bonus applies to one spell only.

After the chosen spell resolves, the stance's Reaction restriction still remains until the stance ends:

> no Reactions except Counterspell.

This exception does **not** teach Counterspell, waive its Reaction, costs, range, target or legality.

### Carrying
Choose **one actual cargo penalty currently affecting you** and ignore that penalty while the stance lasts.

This does not:

- increase carrying capacity;
- let you carry impossible cargo;
- erase equipment limits;
- ignore multiple penalties.

The chosen penalty remains fixed until the stance ends.

You still have disadvantage on Dexterity saves from the stance.

---

# 7. Tactical maneuvers

## Grapple — recovered V6 ordinary procedure

The later condition integration should supersede the older generic fixed-DC sentence in shared class rules **only for ordinary Grapple**.

Ordinary Grapple:

- uses the Attack Action;
- replaces one attack;
- target within reach;
- target no more than one size larger;
- attacker STR (Athletics);
- defender STR (Athletics) or DEX (Acrobatics);
- exact tie preserves current state, so application fails;
- escape uses an Action and the same opposed contest;
- moving the grappled creature halves your Speed unless it is at least two sizes smaller. Pasted text

A class/spell/card that explicitly prints a save/DC instead uses its printed application/escape method.

## Shove

Same reach/size/contest constraints.

Replace one attack.

Success:

- push 5 feet away; or
- knock Prone.

Tie = no state change. Pasted text

## Disarm

Replace one attack.

Use printed:

`Athletics or weapon check vs target Athletics/Acrobatics`

Target must actually be holding the item and the item must be reachable by the chosen attack.

On success, attacker chooses one legal unoccupied space adjacent to the target for the dropped item. If none exists, it falls in the target's space.

An item explicitly unable to be dropped/disarmed because of a bond, attachment or feature is ineligible. Merely being magical or cursed does not automatically create immunity.

Disarm never breaks ownership, attunement, curse or magical bond unless source says so.

## Trip

Replace one melee attack.

Target must be within reach and, **NEW**, no more than one size larger unless a feature says otherwise.

Athletics vs Athletics/Acrobatics. Success → Prone.

## Feint

Bonus Action.

Deception vs Insight.

Tie preserves state → failure.

Success grants advantage on **the next melee attack this turn** only.

## Sunder

Attack the printed object/component/joint.

Damage is applied to the existing durability/object-damage system rather than creature HP.

Do not invent object HP or automatic destruction here. A Sunder target without an operational durability rule remains an equipment/durability dependency.

## Pin — NEW bounded completion

Core gives the rider but not declaration/cap/DC. Pasted text

Before making a ranged weapon attack, declare it a **Pin attempt**.

- maximum one Pin attempt per regular turn;
- cannot combine that attack with another optional tactical maneuver;
- hit resolves normal damage;
- hit also reduces Speed by 10 feet, minimum 0.

Pin DC:

`8 + PB + ability modifier used for that ranged attack`

At the start of each regular target turn, before movement, the target may make one STR (Athletics) check against that DC; success ends Pin.

It may instead spend its Action at any time on its turn to remove Pin automatically.

Pin ends when either endpoint succeeds.

## Silence the Caster — NEW bounded completion

Before one melee attack, declare Silence the Caster.

Maximum one attempt per regular turn and it cannot share that attack with another optional maneuver.

On hit:

- if the target is concentrating, it makes **one** immediate concentration check using the normal concentration DC for that hit;
- do not make a second concentration check for the same damage packet;
- target cannot use Reactions whose activation requires verbal components until the start of its next regular turn.

This is not Core Silenced and does not suppress ordinary speech or Action-time verbal spellcasting.

## Press — NEW bounded timing

Once on each of your regular turns after a melee hit, you may arm Press against that target until the start of your next regular turn.

If that target voluntarily retreats from an adjacent space before then, you may immediately move **up to 5 feet into the space it vacated**, provided the movement is legal.

- no Action/Bonus Action/Reaction;
- does not follow forced movement or teleportation;
- can provoke opportunity attacks normally;
- grants no extra movement beyond that 5 feet.

Only one Press can be armed at a time; a later qualifying hit may replace the chosen target.

## Break Formation

Treat as a special Shove:

- replaces one attack;
- uses normal Shove reach/size contest;
- attacker rolls with disadvantage;
- success pushes target 10 feet.

**NEW snapshot:** when the contest succeeds, record the target's allied creatures adjacent to it **before the push**. Those allies lose their active **Guard Action** benefits.

This does not remove:

- Guarded stance;
- unrelated AC bonuses;
- the target's own Guard unless another rule hits it separately.

## Overwatch

Core Overwatch is a special Ready use:

- spend Action;
- name a lane;
- prepare one ranged attack;
- spend Reaction when qualifying movement crosses/uses that lane;
- ammunition is not consumed until triggered. Pasted text

It is distinct from Soldier's class Overwatch engine.

Both still consume the creature's single Reaction resource if triggered.

---

# 8. Movement

V6 movement-mode switching remains:

> switch modes; subtract total distance already traveled from the newly selected mode's current available Speed. Pasted text

### Speed 0
Prevents voluntary movement and Dash movement.

It does **not** by itself prevent:

- forced movement;
- teleportation.

### Terrain/movement cost composition — NEW

Use additive movement-cost increments rather than multiplying them.

Base movement cost:

- normal: 1 foot per foot;
- difficult: 2 per foot;
- severe: 3 per foot.

Then add:

- crawling: +1 per foot;
- squeezing: +1 per foot.

So:

- crawling normally = 2:1;
- crawling in difficult terrain = 3:1, matching V6;
- squeezing in difficult terrain = 3:1;
- crawling + squeezing in difficult terrain = 4:1.

If the same terrain is both difficult and severe, use **severe**, not both terrain multipliers.

### Prone
Retain the already-closed Core/V6 integration:

- drop Prone at no Speed cost;
- stand costs half current Speed;
- Speed 0 prevents standing;
- crawl uses the costs above;
- Core's ranged-attacker disadvantage overrides V6's generic within-5-foot advantage conflict.

### Occupied spaces

- nonhostile creature's space = difficult terrain;
- hostile space can be entered only if it is at least two sizes larger or smaller;
- cannot willingly end movement in another creature's space. Pasted text

### Squeezing

Can squeeze through a space one size smaller.

While squeezing:

- +1 movement cost per foot;
- own attacks disadvantage;
- DEX saves disadvantage;
- attacks against advantage.

Cannot normally squeeze through a space smaller than that without a feature.

### Forced movement

Does not provoke opportunity attacks.

Cannot place a creature inside solid matter and stops at an obstacle.

Speed 0 does not stop forced movement unless a source explicitly says it does. Pasted text

### Flight

A flying creature falls if:

- knocked Prone;
- Speed becomes 0;
- otherwise unable to remain aloft;

unless it has Hover or magic explicitly holding it aloft. Pasted text

Then use the already-closed provisional Falling bridge.

### Teleport

Teleportation:

- spends no Speed unless printed;
- does not traverse intervening terrain;
- does not provoke opportunity attacks;
- must end in a legal destination unless its source explicitly permits otherwise;
- safely reaching support ends Falling.

### Grid diagonal — NEW playtest choice

For this candidate, **each orthogonal or diagonal adjacent 5-foot space costs 5 feet**.

Use the same tile metric for ordinary range and area counting.

Do not move diagonally through a corner where both orthogonally adjacent sides are completely blocked.

This favors table speed and consistency with the existing “one tile = 5 ft.” convention over geometric precision. If area-shape distortion proves material in playtest, this should be revisited as a map-geometry decision rather than silently altered.

---

# 9. Cover, sight, position knowledge, Hide and Search

## Cover

Use best cover only:

- Half: +2 AC and DEX saves.
- Three-quarters: +5 AC and DEX saves.
- Total: cannot be directly targeted through that obstruction. Pasted text

Multiple cover pieces do not add together.

Determine cover from the attack/effect's origin to the target.

For an area effect, determine cover and line of effect from the **area's origin point** to each affected creature separately.

Total cover from the area origin excludes that creature unless the effect explicitly travels around/through the obstruction.

## Three independent concepts

Track separately:

1. **Visibility:** can observer actually see target?
2. **Position knowledge:** does observer know which space/location target occupies?
3. **Line of effect:** can the attack/effect physically reach that target/location?

Knowing a position does not mean seeing it.

Seeing a target does not automatically grant line of effect.

## Hide — NEW operational bridge

You can attempt Hide from an observer only if:

- that observer cannot currently see you clearly; or
- an explicit feature allows Hide despite visibility.

Roll DEX (Stealth) once.

Passive Perception for this pilot:

`10 + Wisdom (Perception) modifier`, including proficiency when applicable.

For each observer whose passive Perception is below the Stealth result, you are **Hidden** from that observer.

Static-DC tie uses the already-adopted meet-DC success rule.

### Maintaining Hidden

Hidden is tracked per observer.

It persists while:

- you remain unseen by that observer;
- you do not take an action that expressly reveals you;
- you do not cross an area where that observer obtains clear sight.

Moving from cover to cover does not automatically end Hidden if no observer obtains clear sight during the movement.

No universal sound/tracks DC is invented here; explicit sensory effects may reveal position separately.

### Attacking while Hidden

V6:

- attacking something you cannot see → disadvantage;
- attacking while unseen → advantage;
- attack reveals your location after the attack resolves. Pasted text

Thus:

1. resolve the attack with the pre-attack visibility state;
2. afterward, observers able to perceive evidence know the attacker's location.

## Unknown target location — NEW

If you cannot see a target **and do not know its location**, you cannot directly choose that creature as a target for an effect requiring a creature target.

For a weapon/projectile attack against a suspected location, choose a space:

- wrong space → automatic miss;
- correct space while target remains unseen → attack normally suffers disadvantage.

An effect requiring **“a creature you can see”** cannot target a merely known unseen location.

Area effects may target a legal point if their own targeting rules permit it.

## Invisible special rule

Preserve the already-reviewed Core-specific exception:

When an Invisible creature's position is revealed to a particular observer, the **Invisible condition's own attack advantage/disadvantage ends for that observer**.

Do **not** immediately re-grant that identical modifier solely because the creature remains visually Invisible.

Independent darkness, smoke, hiding, blindness, etc. may separately make the creature unseen and invoke their own normal rules.

## Search

Action.

Use:

- WIS (Perception) for immediate sensory detection;
- INT (Investigation) for deduction/traces;
- Arcana or Engineering only where the thing being searched for actually requires that expertise, preserving Core's broader Search list. Pasted text

To locate a Hidden creature directly, default to WIS (Perception) against that creature's recorded Stealth result unless a specific effect provides another method.

Success reveals its location to the searcher.

Communicating that location to allies requires ordinary legal communication; it is not automatically telepathically shared.

## Ranged attacks in close combat

V6 applies disadvantage when making a ranged attack while within 5 feet of a hostile creature that:

- can see you; and
- is not Incapacitated. Pasted text

You do not need to be able to see that hostile creature.

This disadvantage still obeys the universal advantage/disadvantage cancellation rule.

---

# 10. Explicit precedence/supersession notes

I would record these in the implementation header:

- **Reaction resource:** current class-candidate “between starts of regular turns” replaces a literal global numbered-round counter.
- **Ordinary Grapple:** recovered V6 opposed contest supersedes the older shared-class generic fixed-DC sentence; card-specific grapple saves/DCs remain card-specific.
- **Prone:** previously reviewed Core ranged/melee wording remains controlling where V6 conflicts.
- **Invisible:** previously reviewed Core “until location revealed” endpoint remains controlling over generic unseen modifiers caused solely by Invisible.
- **Periodic clocks:** the now-closed family registry retains its regular-turn-only ticking and is not changed by this combat pass.
- **Falling:** the existing provisional fixed Fall Marker remains anchored to regular slots; Bonus Actions and extra turns never move it.
- **One extra full Action:** the existing shared cap remains; nothing in Ready, Brace, stance rules or reactions creates another extra Action. Pasted text

## Deterministic checks Codex should add

A useful minimum test set for this pass is:

1. Late-initiative creature reacts before first turn, refreshes at first turn, reacts again later same numbered round.
2. Round boundary alone does not refresh Reaction.
3. Extra turn does not refresh Reaction/recharge/periodic clock.
4. Surprised first turn advances durations but gives no Action/BA/movement/reaction.
5. Reinforcement entering after its slot waits until next round.
6. Two-round hostile rider survives exactly two future regular target turns.
7. Three-round self aura activated on turn 1 expires at start turn 4.
8. Readied two-attack Attack Action gets both attacks if ordinary Attack legally has two.
9. Readied spell loses paid cost if never released.
10. Starting a readied spell ends previous concentration immediately.
11. Guard + Guarded gives +3 against first qualifying attack; Guard's +2 consumed even on miss.
12. Interpose spends the normal Reaction and requires the new target to be legal.
13. Aim alone produces no attack.
14. Focused does not teach or free Counterspell.
15. Mobile d4 weapon does not step below d4.
16. Ordinary Grapple tie fails to change state.
17. Pin hit + start-turn Athletics success ends Pin before movement.
18. Silence-the-Caster hit causes only one concentration check from that hit.
19. Break Formation removes adjacent allies' Guard Action state, not Guarded stance.
20. Speed 0 prevents standing/Dash but not forced movement or teleport.
21. Flying Speed 0 without Hover invokes Falling.
22. Forced movement never provokes unless source explicitly overrides.
23. Hidden attacker reveals location only after resolving attack.
24. Wrong guessed unseen location automatically misses.
25. Invisible-known-position does not regain Invisible's own attack modifiers through generic unseen wording.
26. Ranged attacker next to unseen hostile that can see attacker still takes close-combat disadvantage.
27. Half + three-quarters cover uses +5 only, not +7.
28. Total cover from area origin excludes target absent explicit around-corner behavior.

This is an **operational playtest proposal** for DD03/DD17/DD18/DD19/DD20/DD21 dependencies, not a claim those rows are closed. Codex should source-conflict it, implement it, and return counterexamples before we mark any of those areas REVIEWED.