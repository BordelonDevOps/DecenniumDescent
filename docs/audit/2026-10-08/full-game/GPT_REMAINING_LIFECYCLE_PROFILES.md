ChatGPT said:

Confirmed. These three should be fixed as follows.

Ritual of Undeath Corpse Servant attack delivery

Accept the proposed gap-fill:

NEW bounded profile: Corpse Servant's printed attack is melee, reach 5 ft.

It retains exactly:

Cleric technique attack bonus;
S d6 necrotic damage;
one attack only through the shared BA/offensive companion command;
no ranged mode;
no multiattack;
no imported undead/monster abilities.

That is the same conservative approach used for Ledger Unbound: where attack delivery is omitted, provide one narrow melee implementation rather than silently granting both melee and ranged profiles.

Ledger's Command ordinary-attack damage cap

Use the deterministic noncritical-profile comparison/substitution, not a rolled-damage minimum.

For the controlled undead's selected ordinary native attack:

preserve its native attack bonus;
preserve its native damage type;
preserve its native reach/range;
preserve ordinary attack-roll behavior;
remove multiattack, recharge powers, spell/resource actions as already printed.

Compute:

nativeMax = maximum possible noncritical damage of the permitted ordinary native attack

and:

ledgerCapMax = 8 × S + M

Then:

if nativeMax <= ledgerCapMax, use the native ordinary damage profile unchanged;
if nativeMax > ledgerCapMax, replace only its damage formula with S d8 + M.

After selecting the legal profile, ordinary critical rules apply to that chosen profile.

So this is not:

actualDamage = min(native rolled damage, rolled S d8+M)

and not a post-roll numeric clamp.

That would distort the source attack's probability distribution and require rolling a second unrelated damage profile. The profile-substitution rule is deterministic and matches the Echo of the Fallen treatment.

Ledger / Ledger Unbound first-damage DR 1

Confirm the proposed ledger model.

For each qualifying creature/source application, track by numbered round:

firstDamageReductionOpportunityUsed

The caller identifies that creature's first qualifying positive incoming damage event of the round when it reaches the ordinary flat-reduction stage.

On that event:

Ledger's Command DR1 qualifies if its control is active;
Ledger Unbound's DR1 qualifies if that snapshotted undead is currently controlled and the effect is active;
other simultaneous flat DR sources also qualify normally.

Apply the established strongest-only flat DR arbitration. Do not add two DR1 sources together.

Each qualifying source nevertheless consumes its own first-damage opportunity on that event even if:

another equal DR1 wins the arbitration;
a stronger DR source wins and its numeric contribution is therefore 0.

This prevents a losing DR source from "waiting" for a second packet and effectively gaining another first-damage window.

Example:

Creature has Ledger DR1, Unbound DR1 and another DR2.
First qualifying packet: apply DR2 only. Both Ledger and Unbound first-event opportunities are also marked spent.
Second packet: neither Ledger DR1 can activate.

Control loss and later regain in the same numbered round does not reset a spent opportunity. The key is source application + creature + numbered round, not continuity of control.

If control is absent when the creature's first damage event occurs, that inactive source does not consume an opportunity from an event for which it was not eligible. If control later returns, it may apply to the first qualifying damage event occurring while that source is actually active, unless its opportunity had already been spent earlier that round.

All other 80+5 boundary decisions remain unchanged.
