# GPT five-spell implementation findings

ChatGPT said:

The candidate is close, but I find two reproducible integration blockers. The other six named interpretation points can be settled without changing the five spell proposals or the 12 finite profiles. The validation evidence is strong—191 contract checks, 729 exhaustive Mass-occupancy comparisons, preserved spell/Core hashes, and the prior Druid suite still passing—but those tests do not cover the two cases below. 
Pasted text
 
Pasted text

1. Same-caster concentration preflight

Accepted, subject to blocker #1 below.

The projected-root procedure is correct:

preflight the prospective cast against the anatomy that will exist after the caster's currently maintained concentration necessarily ends;
reject impossible casts before payment;
after commitment, end the old concentration;
resolve countering/saves;
never restore the old concentration if the new spell fails.

The implementation correctly distinguishes this from another caster's still-active transformation, which remains until actual successful replacement. It also correctly allows a shaping object-creature slot that will necessarily be released by same-caster concentration commitment to count as available during preflight. 
Pasted text
 
Pasted text

The Mass example also correctly ends all old same-caster links before the new target save. 
Pasted text

2. Slot sponsorship across another caster's recast

Accepted.

For an object-origin creature sponsored by caster A:

caster B successfully applying another legal creature-profile True Polymorph does not acquire the slot;
B does not acquire control;
A remains slot_sponsor;
the current form can use B's new True Polymorph stat snapshot while command allegiance remains A's;
continuous replacement does not release/reacquire the sponsor;
an actual replacement into object anatomy releases it.

That is correctly represented by preserving slot_sponsor during continuous=True replacement and only initializing sponsor/controller when the slot has no existing sponsor. 
Pasted text

The cross-caster command regression demonstrates the intended split: A commands; the subject owns the attack; B's True snapshot provides the attack numbers. 
Pasted text

3. Equipment while suppressed

Settle this as:

NEW bridge: the original meld set remains inaccessible while the transformation is antimagic-suppressed.

Suppression changes the expressed anatomy, not the transformation record's inventory ownership state.

Therefore, while suppressed:

root anatomy is expressed;
original melded items remain in the same meld set;
they do not temporarily become equipped, wielded, usable, or material-component-accessible;
no unmeld/remeld inventory transaction occurs;
no gear identity is duplicated;
no recapture occurs when antimagic ends.

External gear that was legitimately acquired after transformation remains an external real item. Whether root anatomy can actually use it while suppressed requires ordinary anatomy/equipment compatibility certification; this helper does not invent that compatibility.

This matches the implementation's deliberate "same meld set, no gear recapture" behavior. 
Pasted text

This is intentionally conservative. A future full equipment/antimagic system could revise that broader game rule, but this selected transformation interface should not temporarily materialize melded inventory by implication.

4. Shapechange switching while suppressed

Confirmed: no internal Shapechange switch is allowed while suppressed.

Suppression means the spell record persists but its granted anatomy/interface is not operative. Therefore the caster may use normal root-anatomy Actions and may release concentration normally, but cannot invoke the spell's internal Bonus Action profile-switch permission until Shapechange is no longer suppressed.

The current _active() requirement correctly blocks switch_shapechange() while suppressed. 
Pasted text
 
Pasted text

There is, however, a separate suppressed willing-rejection defect described as blocker #2 below.

5. Mandatory-reversion geometry

Accepted exactly as implemented.

This helper's responsibility ends at:

restore root anatomy at the same spatial anchor;
report a placement check;
report placementConflict if it cannot fit;
do not teleport;
do not deal invented crushing damage;
do not use overlap to authorize movement/targeting through barriers.

The actual collision/squeezing/forced-placement resolution remains a named whole-game geometry dependency rather than being fabricated here. 
Pasted text

That dependency does not block closure of the bounded spell adapter once the two actual defects below are fixed.

6. Magical-attack classification

Do not add a generic magicalAttack=true flag.

Keep the current exact-source taxonomy:

profile damage type is exactly what the finite profile says;
attack category is natural/form;
it is not automatically a weapon attack;
it is not automatically caster spell damage;
being granted by a spell does not by itself make the resulting claw/bite/etc. a "magical attack" for resistance/immunity bypass.

A later exact global natural/magical-attack taxonomy may grant such recognition. This package should not invent it.

The current profiles and packets are correct to omit blanket magical-attack authorization. 
Pasted text
 
Pasted text

Blocker 1 — True Polymorph cannot correctly replace an active True object anatomy

This is the most important defect.

Reproduction
Creature B is True Polymorphed willingly into an object.
The effect stabilizes permanently.
Another caster legally attempts True Polymorph on that same physical identity, selecting spellform.predator to return it to creature anatomy.

The rules we settled expressly permit a new True Polymorph to replace an existing permanent True record. Creature→object→creature also remains the same original creature identity.

But the helper evaluates current anatomy:

Python
creature = self._current_creature(b)

An unsuppressed object-form link has profile is None, so creature=False.

It then reaches:

Python
if not creature:
    require(spell_id=='true-polymorph' and s.object_input_eligible,
            'Eligible unattended mundane discrete object required')

Pasted text

The documented fresh-object admission rule says object_input_eligible means a discrete nonmagical, unattended outside object. But this target is neither a new external object nor an ordinary nonmagical object—it is an existing True Polymorph anatomy belonging to a creature-origin identity. 
Pasted text

A correct caller therefore cannot honestly certify the flag, so the allowed replacement is rejected.

There is a second problem in the same case. Initial-save logic is:

Python
needs_save=self._current_creature(body) and not s.willing

Pasted text

Because current anatomy is object, an original creature-origin person receives no save against a cross-caster True Polymorph replacement. That launders away the retained creature's agency simply because its current anatomy is object-shaped.

Required behavior

Add a distinct concept:

activeTransformedObjectAnatomy

An active True Polymorph object record is already inside the transformation system and may be targeted by another True Polymorph without re-proving the fresh external-object admission predicates.

It should not require object_input_eligible merely because its current anatomy is object.

Then use immutable origin for agency:

If earliestPhysicalOrigin == creature

Even while current anatomy is object:

creature-profile replacement by True Polymorph:
willing may waive;
unwilling gets the normal True Polymorph CON save;
object-profile replacement:
requires willingness;
retain the same HP/Wounds/class/soul identity;
no companion slot is created merely by returning to creature anatomy.
If earliestPhysicalOrigin == object

An active transformed-object record can be True-Polymorphed again without a fresh "unattended/nonmagical outside object" admission check.

It still retains:

immutable object origin;
mass/value ceilings;
no-soul/no-healing rules;
sponsor/slot rules.

The fresh object_input_eligible gate should remain mandatory when introducing an ordinary outside object into the transformation system, not when replacing an already-registered transformed object identity.

Add regressions for at least:

creature → permanent object → creature by second caster, unwilling/save success;
same case save failure;
creature → permanent object → new object requires willingness;
object-origin object → creature recast retains object origin;
no fresh-object certification required for an already active True object record.

Until this is fixed, True Polymorph's permanent object mode is not internally reversible through the very replacement procedure the draft promises.

Blocker 2 — Suppression incorrectly removes a willing target's rejection Action

The suppression model says:

the link remains alive;
its timer/concentration continues;
root anatomy is expressed;
root-anatomy Actions are handled normally. 
Pasted text

And the agency rule says a willing temporary recipient may spend its Action on an original regular turn to end its Polymorph/Mass/shaping-True link. 
Pasted text

But:

Python
def reject(...):
    link=self._active(target,now)

uses _active() without allow_suppressed=True, so any suppressed link is rejected before the target can use its Action. 
Pasted text
 
Pasted text

Reproduction
B willingly accepts Polymorph.
B enters antimagic; Polymorph is suppressed.
B's root creature anatomy is expressed and has an ordinary Action.
B wants to spend that Action to terminate its willing Polymorph link.
reject() throws because the link is suppressed.

That contradicts the retained agency permission.

It is even clearer for willing creature→object True shaping:

while unsuppressed, object anatomy is actionless and cannot reject;
while suppressed, root creature anatomy returns and does have an Action;
therefore suppression should create a legal opportunity to use the already-existing rejection permission.
Required behavior

reject() should inspect suppressed links:

Plain text
link = active(... allow_suppressed=True)

actionCapable =
    unsuppressed and current profile is creature anatomy
    OR
    suppressed and immutable origin is creature

Then require:

state == shaping;
willing == true;
actual original regular turn;
actual Action;
not Shapechange;
action-capable current expressed anatomy.

Thus:

willing Polymorph suppressed → rejection Action legal;
willing Mass target suppressed → legal;
willing creature→creature True shaping suppressed → legal;
willing creature→object True shaping suppressed → legal because root creature is expressed;
unsuppressed creature→object → still cannot reject because actionless;
object-origin identities do not gain a player-style rejection right.

Add explicit regressions for these.

Review disposition

I find no other reproducible blocker in the submitted bounded procedures after reviewing:

Harmonic credited-RP/payment ordering;
concentration replacement;
Mass simultaneous occupancy preflight;
attack/stat provenance;
permanent True stabilization;
immutable physical origin;
sponsor/control separation;
one object-creature slot;
equipment close-and-recapture;
structural-HP conservation;
suppression clocks;
Druid transformation exclusion;
same-anchor geometry handoff;
12 finite profiles.

The candidate should therefore remain:

IMPLEMENTED CANDIDATE — two integration blockers remain. DO NOT PROMOTE.

Once the transformed-object True-recast/agency path and suppressed willing-rejection path are corrected and regression-tested, I would expect the package to be ready for a final bounded implementation review.

The broader nonblockers remain explicitly open: mandatory-reversion geometry resolution, complete item/anatomy compatibility, global natural/weapon/magical-attack taxonomy, numerical balance, broader spell catalog integration, human playtesting, and the full runtime.
