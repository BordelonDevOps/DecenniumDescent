# GPT exact combat review

Captured from the visible reply DOM after the browser clipboard retained the outgoing packet. Content below is the rendered reply text.

The bounded periodic-family package remains closed at its stated scope. For this combat candidate, I found two material implementation corrections before I would close the bounded action/timing pass, plus several clarifications that should be written into the guide/tests.

1. end of next target turn — interpretation confirmed, but helper needs a fix

Your semantic interpretation is correct:

If an effect is applied during the target's current regular turn and says “until the end of its next turn,” the current turn's upcoming end does not count. Use the following regular-turn end.

The same applies to bare hostile N rounds: an in-progress target turn is not round 1 of a newly applied effect. 
Pasted text

However, marker_deadline(..., skip_current_end=True) has an edge bug. It blindly adds six seconds after already finding the first strictly future marker. If application happens exactly at the marker, the helper already advances to the next marker and then skip_current_end advances it a second time. 
Pasted text

Material fix

Do not encode this merely as a Boolean “skip.”

Pass the specific current marker that is excluded, and skip it only if it would otherwise be selected.

Conceptually:

Plain text
first = first marker strictly after application_time

if excludedCurrentMarker exists
and first == excludedCurrentMarker:
    first += 6 seconds

deadline = first + (count - 1) * 6 seconds

Thus:

applied at time 1 during target turn, current end = 3 → exclude 3 → next = 9;
applied at time 4 after that target turn ended → first eligible = 9, do not skip to 15;
applied exactly at end marker 3 after that marker has begun resolving → first strictly future marker = 9; do not skip to 15.

Add all three tests. This is the main timing-helper blocker.

2. Bare ally-targeted N rounds — source clock confirmed

For an ally-targeted buff with merely N rounds and no target-turn language, use the source's regular-start clock, same as a self/source buff.

So:

NEW default: A beneficial effect created by a source on another creature and described only as lasting N rounds ends at the Nth future regular-start marker of its source, unless its text explicitly keys duration to the target, an absolute elapsed duration, concentration, pulses, or another clock.

Reasons:

source-controlled buffs/auras use one predictable clock;
changing which ally receives the effect does not alter duration;
target initiative order does not change the source's own duration;
it aligns with the existing source/self convention.

An ally-targeted card saying “through the end of the ally's next turn” or “for 3 of the target's turns” obviously uses the target clock instead.

Your virtual-marker preservation handles initiative reordering/removal afterward.

3. Pin / Silence attempt budget — use an own-turn interval budget

Your recommendation is better than “only on your regular turn.”

Use:

NEW: Each creature has one ordinary Pin attempt and one ordinary Silence the Caster attempt between starts of its regular turns.

Each budget:

refreshes at the start of the owner's regular turn;
may be spent on any otherwise legal qualifying attack during that interval;
therefore may be used on the regular turn, an extra turn, a readied Attack, or another legal off-turn attack;
does not refresh on an extra turn or numbered-round boundary.
Consumption

The attempt is consumed when the creature makes a legal declaration and rolls the attack, whether the attack hits or misses.

An illegal declaration that is rejected before a roll consumes nothing under the existing illegal-activation rule.

The two budgets are independent:

one Pin attempt;
one Silence attempt.

But the same attack still cannot carry both, because one attack permits only one optional tactical maneuver.

Press and stance selection remain explicitly regular-own-turn-only.

Validation gap

The current reference helper validates Pin state and Silence concentration results but does not validate this interval-use budget. 
Pasted text

Before calling this bounded package reference-VALIDATED, add an interval-budget helper/test for:

own-turn miss consumes;
off-turn use works if unused;
extra turn does not refresh;
regular start refreshes;
round boundary does not;
Pin and Silence have independent tokens.

That is the second material correction.

4. Ready spell duration — effect clock begins at release

Confirm.

The spell is cast at preparation, but its actual spell effect has not manifested yet.

At preparation:

pay RP/material/other casting costs;
provide components;
resolve Dissonance/Refrain;
trigger actual “when you cast” mechanics;
create held concentration;
Counterspell/cast-interruption occurs here;
Ready expiry begins here.

At release:

choose/recheck legal target or area as already written;
the spell's effect begins;
its ordinary duration starts now.

Therefore a 1-minute spell does not burn through part of its 1-minute effect duration while being held.

Concentration

For a normally concentration spell:

holding concentration begins at preparation;
once released, that same concentration seamlessly supports the spell;
the spell's normal duration clock begins at release.

For a normally non-concentration spell:

Ready still requires concentration while held;
that holding concentration ends after release/resolution.
Explicit source exception

A spell or feature explicitly tying some consequence to:

“when cast,”
“when you begin casting,”
casting preparation itself,

uses that explicit timing for that particular consequence.

That does not move the normal spell effect duration to preparation unless the source specifically says so.

Add this sentence to the guide because the current Ready section establishes casting at preparation but does not yet explicitly establish the effect-duration anchor. 
Pasted text

And yes: Focused's Reaction prohibition means an ordinary Ready cannot release while that prohibition remains. Ready creates no special Reaction exception.

5. Secure Cargo — current treatment is correct

Leave it open.

Core says:

attach, lift, transfer, or protect up to one Extraction Load class.

That does not itself establish that Secure Cargo:

lowers an Extraction Class;
increases carrying Load;
removes a handling penalty;
grants straps/harnesses;
guarantees cargo safety.

Your candidate correctly limits Secure Cargo to authorizing the operation while deferring the meaning of Load versus Extraction Class, hands, harnesses, checks and actual capacity to the cargo/extraction audit. 
Pasted text

No correction needed.

6. Simultaneous-effects helper scope — sufficient, with one documentation sentence

The ordering rule is coherent:

application timestamp;
same-source printed order encoded in creation sequence;
stable application sequence;
IDs only as final deterministic implementation tie-break.

Periodic-family arbitration occurring before the winning damage packet is dispatched is also correct. A losing periodic record consumes its due tick in the periodic subsystem and never arrives at the HP helper as a second damage packet. 
Pasted text

start_life_sequence() is also properly documented as a selected living-HP transition helper rather than a universal event dispatcher. 
Pasted text

I would add one explicit sentence to prevent future scope creep:

start_life_sequence receives only already-resolved/arbitrated HP-changing events. It does not perform condition family arbitration, cure processing, trigger generation, duration expiration, target legality, damage-defense calculation, or general simultaneous-event dispatch.

With that, its bounded reference scope is appropriate.

Additional adversarial findings

I found no other material mechanical contradiction, but two points deserve explicit text/test treatment.

Ready effect duration needs a test

Add:

prepare a nominal 3-round spell;
hold it through some elapsed setup time;
release;
verify its 3-round effect deadline is generated from release, not preparation.

The current ReadyController intentionally does not model effect-duration clocks, so this can be a separate reference function/test rather than expanding it into a spell engine.

Hide helper is narrower than the prose

The prose correctly says one Hide roll can have different degrees against observers. The helper currently returns only True/False Hidden results. 
Pasted text

That is acceptable for this helper's bounded state question, but document:

hide_results collapses Success/Critical Success to Hidden=true and Failure/Critical Failure to false; it is not a complete task-degree record.

No mechanical change is required.

Everything else survives this pass

I find no blocker in the implemented:

Reaction own-turn interval model;
surprise restrictions;
reinforcement entry;
spent movement-cost ledger;
repeated legal Dash accounting;
separate terrain-paying special movement budgets;
death-save/start-event priority;
Ready one-pending-state rule;
cast-at-preparation/no-recast-at-release model;
multiple-attack readied Attack Action;
Guard/Guarded interaction;
Press one-use interval;
ordinary Grapple opposed procedure;
Pin nonstacking Speed state/highest DC;
Silence zero-damage DC 10 concentration check;
equal-diagonal provisional grid;
observer-specific Hide/Search;
known-position vs sight distinction;
cover best-only rule;
ranged range bands and close-combat disadvantage;
bounded helper scope and source-preservation claims. 
Pasted text
 
Pasted text
Bounded disposition

After:

fixing the marker helper to exclude a specific current marker rather than blindly adding six seconds;
implementing/testing Pin/Silence's one-attempt-per-own-regular-start interval;
adding the Ready effect-duration-begins-at-release rule/test;
recording ally-targeted bare N rounds as source-start by default;

I would close this bounded supplied combat/action/timing/vision integration as REVIEWED and reference-VALIDATED within the helper's declared scope.

That does not close DD03/DD17/DD18/DD19/DD20/DD21 generally. Cargo/extraction, complete movement/environment, sensory systems, area geometry, remaining conditions/control, full event dispatch and human balance remain open.