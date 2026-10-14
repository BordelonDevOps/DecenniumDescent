# GPT Strain review and bounded combat disposition

Captured from the visible rendered reply.

The corrected combat/action/timing package can close at its bounded scope as REVIEWED / reference-VALIDATED: the two material timing/budget issues were fixed, the clarified Ready/duration behavior is represented, and validation now reports 112 checks plus 285 movement-state invariants. The broader DD03/DD17/DD18/DD19/DD20/DD21 rows remain open. 
Pasted text

Mind Shock extra Reaction — confirmed

The proposed boundary is correct.

warrior.supplement.mind-shock grants a separate limited extra-Reaction token, not a refresh or second copy of the ordinary Reaction resource.

Use:

An explicit feature granting an additional Reaction creates only the additional use described by that feature. It does not refresh the creature's ordinary Reaction and does not alter the ordinary Reaction interval.

Mind Shock's extra Reaction may be spent once during that serum-profile duration only on a legal movement, defense, already-known Counterspell-like disruption, or other non-attack Reaction. It cannot make an attack.

Using the ordinary Reaction does not consume the Mind Shock token; using the Mind Shock token does not consume or refresh the ordinary Reaction.

Global restrictions still win:

Surprise: no Reaction of either kind until the surprised first turn ends.
Incapacitated: neither can be used.
Focused stance: only Counterspell is permitted; Mind Shock does not broaden that exception.
It does not teach Counterspell or waive costs/targeting.
Extra turns do not refresh either token.

Per-dose stacking/reapplication remains correctly deferred to the all-source semantic pass. The ordinary ReactionClock helper should not pretend to model explicit extra-Reaction grants.

Strain namespace conference
1. Two distinct Strain systems — ACCEPT

Freeze the identities:

warrior.serum-strain
expedition.strain

Also keep distinct:

core.exhaustion
oracle.revelation-backlash
spell Dissonance
any future explicitly named resource.

No automatic conversion, shared cap, shared recovery or immunity exists merely because two systems display Strain.

Binding rule

Contextual Warrior serum/mutation references bind to warrior.serum-strain. The Warrior engine explicitly defines a 0–3 track, its costs and its rest recovery. 
Pasted text

This includes Serum Sharing's pilot Strain on the recipient: a non-Warrior can temporarily possess warrior.serum-strain when a Warrior serum effect explicitly gives it.

Contextual campaign/survival references bind to expedition.strain, including:

Rest Debt;
unsupported Supply;
Quickglass crash;
Morale Rest;
generic Wound-treatment Critical Failure.

The Gameplay Loop defines the 0–6 campaign track, while Core's Quickglass and Morale references use unqualified Strain in campaign contexts. 
Pasted text
 
Pasted text

Future ambiguous unqualified Strain remains unbound until reviewed.

The generic condition documentation should therefore replace “Strain is the expedition track” with:

Strain is not globally unique. Always resolve the source-qualified Strain identity. The active candidate currently contains at least expedition.strain and warrior.serum-strain.

2. Expedition Strain 0–6 and level 6 — NEW cumulative interpretation

The table does not explicitly say “cumulative,” so mark this decision honestly:

NEW: Expedition Strain effects are cumulative. A creature at level N suffers that row and all lower-level rows unless a row supersedes a lower result.

Thus:

1: -1 initiative/expedition checks
2: additionally Speed -10
3: additionally -1 attacks/saves, disadvantage expedition checks, Dash restriction
4: additionally maximum HP -25%
5: additionally the bounded Incapacitated state below
6: catastrophic endpoint.
Level 6

The source phrase “death or permanent collapse, as appropriate to the cause” is not executable without arbitrary adjudication. 
Pasted text

I recommend this NEW default:

Reaching Expedition Strain 6 causes death unless the source that creates the sixth point explicitly specifies a nonlethal collapse outcome.

That is deterministic and does not let the Director choose death after the fact.

Explicit nonlethal exception

If the sixth-point source expressly says collapse/nonlethal collapse instead of death:

Apply expedition.collapse: the creature remains alive but becomes Unconscious, Speed 0 and unable to act or travel. It does not make death saves merely from this state. Ordinary Short Rest, Long Rest and Morale Rest cannot reduce Strain 6 while collapsed. A full qualifying Haven-care day or an explicit treatment must reduce Expedition Strain below 6 before the collapse ends.

This preserves the source's alternative without making “permanent collapse” an undefined forced character retirement.

warrior.serum-strain can never reach this endpoint merely because it shares the word Strain; its cap remains 3.

3. Independent penalties and maximum HP

Yes: independent tracks can affect the same statistic.

Speed

Use this order:

establish otherwise-applicable Speed;
apply flat increases/reductions, including:
Expedition Strain 2: -10 ft
Serum Strain 2: -5 ft
stance/equipment/etc.;
floor at 0;
apply multiplicative/halving effects such as Exhaustion level 2;
a rule setting Speed to 0 overrides the result.

Example:

30 Speed -10 expedition -5 serum = 15, then Exhaustion halves → 7 ft after normal fraction-rounding rules.

Neither Strain track's Speed penalty suppresses the other.

Saves

At expedition level 2+ and serum level 3:

expedition: -1 saves
serum: -1 saves

These are independent systems, so total is -2 saves.

Maximum HP

At Expedition Strain 4:

× 3/4

At Exhaustion 4:

× 1/2

NEW combination rule:

Apply compatible maximum-HP multipliers to the same otherwise-applicable maximum as exact rational factors, multiply them together, then floor once; minimum effective maximum HP is 1.

Example:

100 normal maximum:

100 × 3/4 × 1/2 = 37.5 → 37

Do not calculate 75 then repeatedly halve already-modified values in a way that compounds rounding.

If effective maximum falls below current HP, clamp current HP downward. That loss is not damage and does not trigger Wounds.

Removing a modifier raises maximum capacity but does not heal current HP.

Critically Wounded healing ceiling

This is applied after effective maximum HP is calculated:

max(1, effectiveMaximumHP - 1)

because Critical's rule is a healing ceiling, not another maximum-HP multiplier.

4. Expedition Strain 3 Dash restriction

Use a finite lock rather than trying to interpret individual Action adjacency.

NEW — Dash lock

When a creature at Expedition Strain 3+ takes any Dash, set:

expeditionDashLocked = true

While locked, it cannot take another Dash.

The lock clears at the end of the creature's next regular turn during which it took no Dash.

Consequences:

no two Dashes in one turn;
no Dash on consecutive regular turns;
a Bonus Action Dash counts;
an extra-Action Dash counts;
an extra-turn Dash counts;
extra turns never clear the lock;
a non-Dash Action between two Dash attempts during the same turn does not clear it.

Example:

Turn 1: Dash → locked.
Extra turn: cannot Dash.
Turn 2: cannot Dash; completes turn with no Dash → lock clears.
Turn 3: Dash legal again.

Outside initiative:

after a Dash-equivalent burst, the creature must spend six uninterrupted elapsed seconds without Dashing before the lock clears.

This is explicitly track-specific and supersedes the general rule allowing multiple legal Dash Actions while Expedition Strain 3+ is active.

5. Expedition Strain 5

The source says:

“Incapacitated except for slow travel and Rest.” 
Pasted text

Use Core Incapacitated consequences as the baseline:

no Action;
no Bonus Action;
no Reaction;
concentration ends under the existing shared rule.
NEW slow-travel exception

The exception is out-of-combat only.

At Expedition Strain 5, the creature:

cannot voluntarily move for tactical/combat positioning while initiative is active;
outside combat may participate in slow travel at half its otherwise legal travel pace / walking movement rate;
cannot Dash;
may be carried normally by another legal system.

Do not invent a new miles-per-hour value here; the travel subsystem supplies the underlying pace.

Communication

Incapacitated alone does not prohibit speech, so the creature may communicate briefly if no other condition prevents it.

Consumables

It cannot voluntarily drink/use/administer an item requiring an Action because Incapacitated denies Actions.

Another creature may:

feed it;
administer a potion/food/water;
provide treatment;

if the recipient is a legal willing target and the helper pays the actual required Action/activity/cost.

No free action is created.

Rest

It may receive Short/Long Rest and Haven-care benefits if all other eligibility requirements are met.

6. Recovery

Preserve all campaign rest caps.

The Gameplay Loop explicitly says:

Short Rest = 1 hour;
maximum 2 beneficial Short Rests between Long Rests;
Long Rest = one 8-hour Rest Watch;
maximum 1 beneficial Long Rest per 24 hours. 
Pasted text

These limits also govern Warrior serum-Strain recovery when that recovery is obtained from the relevant rest.

Warrior serum Strain

Source rules remain exact:

completed eligible Short Rest → -1 warrior.serum-strain
completed eligible Long Rest → reset to 0

No Expedition Strain is removed by these class-specific reductions unless the same rest separately satisfies the campaign rule below.

Expedition Strain source records

For recovery bookkeeping, represent each Expedition Strain point with source metadata:

sourceId
ordinaryRemovable
optional removalGate

Overall level = active point count, capped at 6.

Secure Long Rest

A qualifying secure 8-hour Long Rest removes one legally removable Expedition Strain point.

The patient chooses among eligible points.

If Rest Debt, food/water failure or another source blocks reduction, no point is removed.

Haven care

“one full day” means:

24 consecutive elapsed hours in a qualifying Haven under Haven-care conditions.

At completion:

remove all ordinary removable Expedition Strain;
source-blocked points remain until their removal gate is met.

Only one Haven-care interval for the same patient may be active at a time. Interrupting it before 24 hours gives no completion benefit; restarting begins a fresh 24-hour interval.

Do not replay the same completed interval repeatedly.

Morale Rest

Core says:

“A safe evening of chosen recreation removes 1 Strain, never a Wound.” 
Pasted text

NEW finite endpoint

Define a Morale Rest as:

4 consecutive hours
in a safe location;
spent in voluntarily chosen recreation;
not work, expedition travel, Short Rest or Long Rest sleep;
no forced substance use;
at most one beneficial Morale Rest per 24 elapsed hours.

On completion remove one legally removable expedition.strain point.

Morale Rest + Long Rest

Yes, a character can legitimately remove two Expedition Strain in the same 24-hour period if it separately completes:

one qualifying 4-hour Morale Rest; and
one qualifying secure 8-hour Long Rest.

They are separate sourced benefits and require separate elapsed activities.

Do not impose a new combined cap.

A Haven-care day may later clear remaining ordinary Strain when its own full 24-hour requirement is satisfied.

7. Strain and Exhaustion from one event

Use explicit-source-only application.

One actual event applies both Expedition Strain and Exhaustion only when its operative source expressly applies both.

Never infer a second fatigue mechanic because their fiction overlaps.

Therefore:

Quickglass crash → +1 expedition.strain, plus its printed 1-hour DEX-check disadvantage; no Exhaustion. 
Pasted text
ordinary Wound-treatment Critical Failure → +1 expedition.strain to the patient; no extra Wound or Exhaustion beyond the treatment procedure.
Warrior serum usage → warrior.serum-strain; no Expedition Strain unless a feature explicitly says so.
Exhaustion removal does not remove either Strain track.
8. Immunities / removal

Do not create a universal “Strain immunity” rule.

These are not one shared condition family.

warrior.serum-strain

Only effects explicitly referring to:

serum Strain;
Warrior Strain;
mutation activation Strain;

may alter/prevent it.

Poison immunity, Exhaustion immunity and Expedition Strain immunity do nothing to it unless their source explicitly says otherwise.

Serum Tolerance is already explicit that it suppresses serum-profile side effects but not Strain generation or penalties. 
Pasted text

expedition.strain

Likewise, only effects explicitly covering Expedition Strain/campaign Strain alter it.

Do not automatically apply the generic condition-immunity rule where immunity suppresses active penalties and clocks continue.

If a future feature says merely “immune to Strain” with no namespace or operational explanation, leave it unbound pending source review.

If a future reviewed feature says:

“cannot gain Expedition Strain” → block new gains only;
“ignore Expedition Strain penalties” → track persists but penalties are suppressed;
“remove X Expedition Strain” → actually remove points.

Do not infer one meaning from another.

One additional namespace consequence: Serum Sharing

Because Warrior-context Strain means warrior.serum-strain, Serum Sharing's:

“The ally gains 1 Strain for this pilot” 
Pasted text

means the injected ally gains 1 warrior.serum-strain, even if that ally is not a Warrior.

That recipient therefore uses:

the 0–3 cap;
Speed penalty at 2;
AC/save penalties at 3;
ordinary serum-Strain rest recovery.

The activation lock at 3 applies only to serum/Cocktail/Overclock/Surge actions that creature actually possesses.

This does not grant the ally any Warrior serum abilities.

Proposed implementation invariants

I would test at least these:

Warrior serum Strain 3 never becomes Expedition Strain 3.
Expedition Strain 6 never arises from Warrior serum cap overflow.
Quickglass increments Expedition only.
Wound-treatment Critical Failure increments Expedition only.
Serum Sharing gives non-Warrior recipient serum Strain.
Serum Strain 2 + Expedition Strain 2 → Speed -15 before Exhaustion halving.
Serum Strain 3 + Expedition Strain 2 → saves -2.
Expedition Strain 4 + Exhaustion 4 on max HP 100 → 37 effective max.
Increasing effective max later does not heal.
Dash at Expedition 3 locks same-turn second Dash.
Extra turn does not clear Dash lock.
Next regular turn cannot Dash and clears lock at its end.
Expedition 5 prevents combat Action/BA/Reaction and tactical voluntary movement.
Expedition 5 can receive treatment from another creature.
Eligible serum Short Rest lowers serum Strain only.
Secure Long Rest may both reset/lower serum Strain and remove one Expedition point because those are separate sourced benefits.
Third beneficial Short Rest before a Long Rest grants no further Short-Rest benefit.
Second beneficial Long Rest inside 24 hours grants no second Long-Rest benefit.
Four-hour Morale Rest + separate secure Long Rest may remove two Expedition points.
Haven care removes all ordinary removable points but preserves source-blocked points.
Exhaustion immunity leaves both Strain tracks unchanged.
Serum Tolerance leaves serum Strain unchanged.
An ambiguous future “Strain immunity” fails binding validation rather than guessing a track.
Reaching Expedition 6 defaults to death unless the sixth-point source explicitly declares its nonlethal collapse endpoint.

This gives a complete operational namespace/recovery candidate without silently converting the Gameplay 0–6 table into Core canon. The 0–6 Expedition track remains an explicit retained/provisional campaign overlay; the Warrior 0–3 track remains the class engine.