# GPT Strain counterexample review

Captured from the visible rendered reply.

Agreed. These corrections make the Strain model more coherent and remove several cap/recovery loopholes.

1. Expedition table transcription — CORRECTED

My prior summary misplaced the attack/save penalty. The preserved Gameplay table is:

0: no penalty
1: -1 initiative and expedition checks
2: Speed -10 ft.; -1 attack rolls and saving throws
3: additionally disadvantage on expedition checks and the Dash restriction
4: maximum HP reduced 25%
5: Incapacitated except slow travel and Rest
6: death or permanent collapse according to cause. 
Pasted text

The NEW cumulative interpretation remains; only my summary was wrong.

2. Expedition 6 and further Strain gains — ACCEPT

Use this exact cap rule:

NEW: Whenever a positive, unprevented expedition.strain gain would cause the track to reach or exceed 6, resolve the level-6 endpoint for that gain before clamping the stored track to 6.

Default endpoint: death.

If and only if that specific reviewed gain source explicitly specifies nonlethal collapse, use its collapse endpoint instead.

So a creature already alive at 6 from a nonlethal collapse is not immune to later Strain.

Example:

already 6 and collapsed;
later suffers +1 expedition.strain from a normal source with no nonlethal exception;
the gain is positive and unprevented;
level-6 endpoint is evaluated again → death;
stored track remains 6, not 7.

Record overflow/attempted amount for audit if useful, but never create point 7.

A prevented gain:

adds no point;
causes no level-6 endpoint.

A later nonlethal source cannot revive a dead creature.

Collapse state

Confirm:

expedition.collapse:

does not set HP to 0;
does not make the creature Stable;
does not create death saves by itself.

If the creature is independently at 0 HP and dying, normal death-save rules continue.

Ending expedition.collapse ends only that collapse source; an independent Unconscious condition remains.

3. Expedition point metadata and recovery — ACCEPT

Use each Expedition Strain point as an individual record:

Plain text
pointId
sourceId
ordinaryRemovable
removalGateMet

Optional additional provenance fields are fine, but those four are enough for generic recovery.

Generic recovery eligibility

Long Rest, Morale Rest and Haven care may remove only points where:

ordinaryRemovable == true && removalGateMet == true

A specifically reviewed treatment may override the removal metadata of the named source it covers.

Suppression is not removal

An effect saying:

“ignore Strain penalties”
“suppress Strain effects”

does not:

remove points;
lower the numerical track;
prevent level-6 death/collapse evaluation,

unless it expressly says it does those things.

Nonlethal level-6 collapse

While at Strain 6 with expedition.collapse:

Short Rest does not reduce Expedition Strain;
generic Long Rest does not reduce it;
Morale Rest does not reduce it;
qualifying 24-hour Haven care or explicit treatment may.

If Haven care removes only eligible points but blocked points leave the track at 6, collapse persists.

If a cure changes a point from gated to recoverable, record the metadata transition explicitly. Do not automatically delete that point.

4. Rest Debt ordering / beneficial-rest caps — ACCEPT

The source distinguishes completing a Rest Watch from receiving the beneficial Long Rest package. It also explicitly caps beneficial Long Rests at once per 24 hours and Short Rests at two between Long Rests. 
Pasted text

Safe Rest Watch ordering

For a qualifying completed safe 8-hour Rest Watch:

complete the Rest Watch;
clear any owed Rest Debt that this Rest Watch satisfies;
evaluate whether this Rest Watch is eligible to grant beneficial Long Rest rewards;
if eligible, resolve those rewards, including one eligible Expedition Strain reduction;
persistent food/water/source-specific blocks are then respected.

Thus the same Rest Watch that pays Rest Debt is no longer blocked by that debt when its own legal Strain reduction is evaluated.

Nonbeneficial Rest Watch

Yes:

A safe complete 8-hour Rest Watch may satisfy/clear Rest Debt even if the creature is currently ineligible to receive another beneficial Long Rest because it has already received one within 24 hours.

That Rest Watch does not:

reset the beneficial Long-Rest clock;
restore Long-Rest resources again;
remove another Expedition Strain point;
reset the “two beneficial Short Rests between Long Rests” accounting.

The distinction is:

time spent resting ≠ beneficial Long Rest reward event.

Haven care overlap

Also yes.

A 24-hour Haven-care project is a care/location eligibility window, not 24 hours of uninterrupted active treatment.

Within that same 24 hours the patient may separately complete, without overlap:

sleep/Rest Watch;
a 4-hour Morale Rest;
meals;
passive care.

Actual active practitioner work cannot double-pay incompatible activities where the project rules prohibit it.

One elapsed hour is counted once, but being inside the Haven-care window does not mean every hour is consumed as active treatment.

Supply/food/water/care must actually be available under campaign rules; nothing here creates free Supply.

5. Expedition Dash-lock clock — use preserved original endpoint

Your proposed preserved-clock model is better than switching between unrelated “next turn” and “six quiet seconds” semantics.

NEW Dash-lock state

When a creature at Expedition Strain 3+ legally Dashes, create:

expeditionDashLock

If created during initiative:

unlock at the end of that creature's next regular-turn marker strictly after the Dash.

That next regular turn cannot Dash.

If created outside initiative:

unlock exactly 6 elapsed seconds after that Dash.

Crossing initiative boundaries

Preserve the original endpoint.

If created in initiative and combat ends:

keep that original virtual regular-end marker;
it continues recurring on its six-second virtual schedule;
do not restart a new six-second timer.

If created outside initiative and initiative starts:

keep the original absolute dashTime + 6s deadline;
do not convert it to the new initiative slot.

If initiative order changes, the lock's existing virtual marker does not move.

Falling below Strain 3

Immediately remove the Dash restriction and clear the pending lock.

If Expedition Strain later rises to 3+, the creature begins unlocked. A new legal Dash creates a new lock.

Other non-clearing events

Do not clear the lock from:

an extra turn;
a non-Dash Action;
round boundary;
initiative change.

An off-turn Dash creates a lock through the next regular-turn end just like an own-turn Dash.

This cleanly overrides the otherwise legal multiple-Dash general rule only while Expedition Strain 3+ applies.

6. Serum costs, overcap legality and recipient Strain — ACCEPT WITH SOURCE-SPECIFIC SPLIT
Voluntary Warrior activations with explicit legality checks

For Serum Cocktail, Mutation Overload, Serum Overclock, or another activation that explicitly says it is illegal if Strain would exceed 3:

determine current warrior.serum-strain;
determine printed proposed gain;
apply all legal gain modifiers/reductions;
apply any printed minimum gain, such as Cocktail/Overload not being reducible below 1 where applicable;
compute resulting Strain;
if resulting value > 3, activation is illegal;
no clipping voluntary cost to 3 to make the activation legal.

This preserves the source wording. 
Pasted text

Automatic/involuntary later gains

A profile-ending side effect such as Sanguine Surge's later +1 Strain is not a new voluntary activation cost.

Therefore:

automatic/involuntary Serum Strain gains clamp at 3 rather than causing Expedition damage, overflow death, or an illegal retroactive activation.

warrior.serum-strain remains capped at 3. 
Pasted text

Serum Sharing recipient already at 3

The source says the ally “gains 1 Strain” but does not say the injection becomes illegal at Strain 3. 
Pasted text

Use this NEW integration:

Serum Sharing remains legal for a willing recipient already at Serum Strain 3. Its attempted +1 gain clamps at 3. The recipient keeps all level-3 penalties and receives the serum's actual diluted effect/side effect.

Do not reject the injection unless a later reviewed source explicitly adds such a restriction.

This does not grant Warrior class abilities.

Non-Warrior Serum Strain recovery

Confirm:

A non-Warrior carrying warrior.serum-strain uses the track's own recovery procedure:

qualifying beneficial 1-hour Short Rest → -1
qualifying beneficial 8-hour Long Rest → 0

This is a NEW operational consequence of applying the Warrior track to an external recipient, not a granted class feature.

It does not grant:

serum preparation;
mutation slots;
injections;
Cocktail;
Overclock;
any other Warrior ability.

Campaign beneficial-rest caps still apply.

7. Maximum HP / death / resurrection boundaries — ACCEPT

Keep:

Effective maximum-HP modifiers are calculated first; if the result falls below current HP, clamp current HP downward.

That clamp is:

not damage;
does not cause a Wound save;
does not create death-save failures;
does not trigger damage-based resources.

If the effective maximum later increases:

maximum capacity rises;
current HP remains unchanged;
no healing occurs;
no death counters reset.
Expedition 6 death

Default lethal Expedition 6 uses the normal Dead state.

Reducing Expedition Strain on the corpse afterward:

does not revive;
does not stabilize;
does not restore HP.

The separate track records may remain stored so a later actual resurrection can restore the creature with whatever state the resurrection rules preserve/remove.

No Strain cure is implicitly resurrection.

8. Initiative and Expedition-5 movement — ACCEPT
Initiative penalty

Expedition Strain 1's -1 initiative applies only when an initiative roll is actually made.

Gaining or losing Expedition Strain after encounter order has been established does not reorder the existing initiative.

It affects a later initiative roll if still active then.

Expedition Strain 5

Keep the distinction explicit:

expedition.strain level 5 imposes Core Incapacitated plus a NEW track-specific prohibition on tactical voluntary movement.

Do not redefine Incapacitated globally as Speed 0.

At level 5:

no Action;
no Bonus Action;
no Reaction;
concentration ends under existing rules;
no voluntary tactical movement during combat.

But:

forced movement still works;
teleportation by another valid effect still works;
another creature may carry/move the victim if legal;
the creature's actual Speed statistic is not automatically rewritten to 0.
Slow travel

Outside combat:

Calculate the creature's otherwise legal travel pace after all applicable Speed/load/environment penalties, then halve that result once for Expedition Strain 5 slow travel.

Do not repeatedly rehalve each Watch.

If another source already expressly halves travel pace, combine according to the eventual travel-system stacking rules rather than assuming repeated exponential halving here.

Corrected cumulative Expedition summary

For implementation, use:

Expedition Strain	Cumulative effect
0	None
1	-1 initiative, -1 expedition checks
2	Above + Speed -10 ft, -1 attacks, -1 saves
3	Above + disadvantage expedition checks + Dash lock/restriction
4	Above + effective max HP × 3/4
5	Above + Incapacitated + no tactical voluntary movement; slow travel exception
6	Evaluate each positive unprevented gain reaching/exceeding 6: death by default, explicit reviewed nonlethal source may instead create collapse

That preserves the exact level placement from the Gameplay source while making the cumulative behavior and unresolved level-6 phrase explicitly provisional. 
Pasted text

Implementation status

With these corrections, I see no unresolved conceptual blocker to writing the unified Strain namespace reference and bounded tests.

The key invariants are now:

two independent Strain state machines;
point-level Expedition recovery metadata;
no voluntary Serum overcap clipping;
automatic Serum gains clamp only within the serum track;
Rest Debt completion and beneficial-rest rewards are separate events;
preserved Dash-lock deadlines survive initiative transitions;
Expedition 6 evaluates every positive unprevented gain that reaches or attempts to exceed the cap;
no Strain subsystem implicitly becomes Exhaustion, resurrection, poison, or the other Strain track.

The Strain package itself should remain IN REVIEW until Codex returns the implemented reference and adversarial tests.