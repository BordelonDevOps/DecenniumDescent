# GPT rank-one Evocation authoring clarification

Source: complete actual Calibration Review reply, conversation 6a7a0fa2-eee0-83ea-92e9-6723a9f67ede, turn abaa0fa5-a322-4fd6-901d-3711641a8a54. The earlier rendered-text capture remains separately preserved as GPT_EVOCATION_RANK1_AUTHORING_CLARIFICATION_BROWSER.txt. These are authoring decisions, not exact-card approval or promotion.

These are **authoring clarifications only**. No rank-one Evocation card is approved or promoted; catalog remains **249 reviewed / 599 unfinished**. The source-conference rulings remain unchanged except for the explicit completions below.

## 1. Magic Missile Storm — confirm with exact event order

Your procedure is approved.

At **cast commitment**:

- create missiles **1, 2, 3**;
- assign each missile to one legal creature;
- record that allocation permanently for this cast;
- record missile resolution order as 1 → 2 → 3.

After the ordinary cast/Counterspell window survives, resolve missiles in that fixed order. Each missile remains its own auto-hit and damage packet.

### Shield trigger

**NEW — one Shield targeting opportunity per allocated recipient per Storm cast.**

A creature allocated one or more missiles is considered targeted by the Shield spell's named Magic Missile exception once for that Storm.

That opportunity exists after target allocation is committed and before that recipient's **first missile damage** resolves.

If Shield is legally established during that opportunity:

- every unresolved Magic Missile Storm missile already allocated to that creature is prevented from dealing damage while Shield applies;
- later missiles allocated to the same recipient do **not** create another Shield trigger for that same Storm cast;
- allocations remain spent and cannot be reassigned.

If the recipient does not use the trigger before its first missile damage resolves, later missiles from that same Storm do not reopen it.

Normal nested spell-counter timing applies to Shield itself.

### Target becoming invalid

No retargeting.

If, before an allocated missile resolves, its assigned creature:

- dies and is no longer a legal creature target;
- disappears;
- leaves existence;
- otherwise ceases to be a legal target for that already allocated missile,

that unresolved allocation is simply spent without creating a replacement target. It does not become a corpse/object attack unless an exact source expressly allows that.

This supplies no tracking oracle.

### Bridge scope

Confirmed:

> The Magic Missile Storm ↔ Magic Missile compatibility exists **only for the ordinary Shield spell's expressly named Magic Missile exception**.

It does not:

- rename Magic Missile Storm;
- affect Mage Arcane Missile;
- affect another class feature containing “Missile”;
- create a generic defense against auto-hit effects.

---

## 2. Arcane Shield Shatter — confirm and tighten eligibility

Approve your proposed boundary.

Both must be legal at commitment/resolution:

1. the **selected ongoing shield effect**; and
2. the **designated creature currently protected by that effect**.

Both must be:

- individually perceived;
- within 30 ft;
- within LoE.

### Hidden eligibility

After paid commitment, resolve without diagnostic whether:

- selected effect is actually spell-generated;
- actual generating rank is 0 or 1;
- it is actually an eligible ongoing defensive shield/barrier/ward;
- it currently protects the designated creature;
- it is susceptible to this ending procedure.

Failure of **any** required predicate means:

- selected effect does not end;
- designated creature takes **no 1d8 damage**;
- no alternate target/effect may be chosen;
- no refund.

### “Shield/barrier/ward” meaning

Confirmed: this is a **source-qualified functional identity**, never a text-substring search.

An effect qualifies when its actual spell source expressly establishes it as a magical shield, barrier, ward, or equivalent defensive protective effect.

Therefore a class feature called “Ward Something” does not qualify merely from its name.

Also exclude:

- permanent class engines;
- creature traits;
- magic-item properties;
- ordinary physical shields;
- a spell that merely creates an ordinary physical shield-object with no ongoing magical defensive effect.

An ongoing magical barrier protecting a creature can qualify.

### One effect only

Select exactly **one independent ongoing effect/component**.

Ending invokes its actual parent/dependency callbacks:

- if the component is independently terminable, siblings remain;
- if its actual source says ending it ends the parent or linked siblings, those callbacks operate normally.

No arbitrary sibling purge.

### Damage order

1. successfully end eligible effect;
2. then, if the designated protected creature remains a legal creature recipient, deal one automatic **1d8 force** packet.

If the shield cannot actually be ended, **no damage fallback** occurs.

Approved.

---

## 3. Ignition Bolt — critical and impact center

Confirmed.

Roll the ordinary primary/splash base:

> **base `1d10`**

once.

On an attack critical:

- primary target receives the base `1d10` plus a separate critical-only additional `1d10`;
- splash recipients use **only the original base `1d10`**.

The critical die is never incorporated into the splash value.

### Impact center

Capture the initial target's actual position **when the legal attack resolves, before applying its piercing/fire damage consequences**.

That position becomes the splash center.

Therefore:

- destroying the target does not erase the already-established splash;
- the target disappearing as a consequence of that damage does not relocate it;
- no subsequent damage consequence changes its center.

Other splash creatures require LoE from that captured center.

The primary target still receives only the primary hit packet and is excluded from taking the splash a second time.

Approved.

---

## 4. Earth Tremor — surface topology

Approve.

**NEW — qualifying terrain patch:** the 10-ft-radius patch occupies **one contiguous physical supporting surface associated with the selected center**.

It does not automatically propagate:

- through a floor to a lower story;
- upward through a ceiling;
- through walls;
- onto separate stacked platforms;
- across disconnected surfaces merely because they fit within three-dimensional radius.

A creature is an initial damage target only if it is actually physically supported by that eligible patch and has the required effect LoE from the center.

The caster also makes the DEX save if the caster is physically supported by the affected patch.

### Terrain state

The one-minute difficult terrain is a **temporary magical movement-cost effect on that surface**, not permanent material alteration.

It creates no:

- rubble inventory;
- excavated soil;
- structural cracking/collapse;
- permanent terrain;
- physical difficult-terrain object surviving the spell.

It ends at normal expiry/removal/eligible dispelling.

Later entry never repeats the initial 3d6 damage.

Each cast has its own patch and deadline. Overlap of identical Earth Tremor terrain does not multiply difficult-terrain movement cost.

Approved.

---

## 5. Ice Knife — burst center and LoE

Confirmed.

Before resolving the primary attack's piercing damage, capture the legal initial target's **actual position at attack resolution**.

That becomes the cold-burst center whether the attack subsequently hits or misses.

Every creature:

- within 5 ft of that captured point; and
- with LoE from that point

takes the shared **2d6 cold** packet with **no saving throw**.

This includes, when geometrically eligible:

- initial target;
- caster;
- allies;
- enemies.

The initial target's cold packet is distinct from its possible piercing attack packet.

Only the attack-linked `1d10 piercing` dice can be doubled by a critical. The area `2d6 cold` never becomes critical damage.

### Target invalid before resolution

If the originally selected target becomes illegal **before the attack can legally resolve**, then:

- no attack roll is made;
- no position is captured;
- no cold burst is created.

The spell does not magically discover a last location or convert into a point-target explosion.

Approved.

---

## 6. Thunderwave — push distance

Refine “up to 10 ft” to the stronger source-faithful procedure you proposed:

> **On a failed STR save, the creature is forced directly away from the cone origin toward a total displacement of 10 ft, stopping early only when ordinary forced-movement legality prevents further displacement.**

The target does **not** voluntarily choose a shorter distance.

Use direct radial movement away from the origin.

Possible early stopping includes:

- solid obstacle;
- illegal occupied destination;
- geometry that permits no farther legal displacement;
- actual applicable forced-movement defense/restriction.

Ordinary falling/support rules apply if the forced movement legitimately carries the target beyond an edge.

No new collision/impact damage is created.

The caster is not self-pushed merely because the caster is the cone origin.

The push follows the **failed STR save independently of actual thunder damage**. A target whose damage becomes 0 can still be pushed unless a separate defense prevents the displacement.

**NEW wording refinement:** replace discretionary “up to 10 ft” with mandatory “10 ft, stopping early only as legality requires.”

---

## 7. Witch Bolt — tether, pulse event, and timing bridge

All first-order bindings are confirmed.

### Initial tether

A successful initial **hit** establishes the tether even if the initial lightning packet becomes 0 through damage resistance/immunity, unless an actual defense separately prevents the tether itself.

Initial miss → no tether.

### Maintenance is not a cast

A Witch Bolt maintenance pulse is an **activation of the already-existing spell**, not another spell cast.

Therefore a pulse has:

- no additional RP payment;
- no Dissonance;
- no Refrain;
- no spell cast-begin hooks;
- no new ordinary Counterspell window;
- no second concentration transition.

Its damage still invokes whatever ordinary damage/outcome hooks are actually triggered by that damage event.

### Pulse allowance

At most **one Witch Bolt pulse opportunity per caster regular turn**, starting with the first future regular turn after establishment.

It uses one ordinary Action.

There is:

- no cast-turn pulse;
- no extra-turn pulse;
- no second pulse because another feature granted another Action;
- no pulse multiplication from extra Actions.

A separately granted extra Action can be used for something else according to its own rules, but cannot create another Witch Bolt pulse.

### Expiry ordering

Confirmed:

> the spell's maximum expiry at the caster's tenth future regular START occurs before any new voluntary Witch Bolt pulse from that turn could be declared.

Likewise outside initiative, +60 seconds is an absolute maximum.

### NEW — outside-to-initiative pulse-history bridge

Use a **Witch-Bolt-specific pulse-use ledger**, not a general confiscation of the creature's Action.

If a virtual Witch Bolt pulse was already used during the currently open six-second opportunity before initiative begins:

- the caster enters its first real regular turn with its **ordinary Action fully available** for other legal uses;
- but its **Witch Bolt pulse opportunity for that mapped turn is already consumed**;
- it cannot pulse Witch Bolt again until its next unused regular pulse opportunity.

This conserves spell pulse history without pretending that the virtual pulse permanently spent the real turn's unrelated general Action.

If **no virtual pulse has yet been used** when initiative begins:

- the caster's next actual regular turn becomes the next Witch Bolt pulse opportunity;
- it may therefore pulse on that turn even if that real turn occurs before the originally projected +6 virtual marker;
- using the pulse consumes that real turn's ordinary Action;
- the original +60 absolute maximum is still retained.

Already-resolved virtual pulse opportunities are never replayed.

This is deliberately narrower than the controlled-creature shared-behavior-budget bridge because Witch Bolt tracks **one spell-specific pulse permission plus an Action cost**, not domination of the creature's entire behavior budget.

### Between pulse opportunities

Confirmed: there is no continuous range/LoE/sight/hearing tether that automatically ends the spell between maintenance opportunities.

Those predicates are checked when attempting the next pulse.

Thus temporary:

- cover;
- invisibility/unperceived state;
- range separation

can make a pulse unavailable without automatically terminating concentration.

### Target cessation

If the creature target actually dies and ceases to be a legal creature target, or otherwise ends its existence as that continuing creature, the Witch Bolt tether ends.

It does not remain attached to:

- a corpse object;
- a replacement creature;
- a later resummoned/recreated entity.

A later resurrection does not revive the ended tether.

Approved.

---

## 8. Zephyr Strike — event/source bindings

Confirmed.

### Pending strike consumption

When the recipient successfully **hits** with a qualifying weapon attack, the pending Zephyr Strike damage rider is consumed immediately by that hit event.

Consumption does not require:

- positive post-defense damage;
- ordinary HP loss;
- target survival.

If all resulting damage is later prevented, the rider remains consumed.

### Damage event

The extra `1d8 force` belongs to that one weapon-hit damage event.

On an actual critical hit, it is an actual attack damage die and follows the normal critical-dice rule.

It does not become:

- another attack;
- another hit;
- a separate weapon attack event;
- a second recipient within Multiattack/Extra Attack.

Only that first qualifying hit consuming the rider gets it.

### Independent movement component

Consuming the `1d8` does **not** end the movement/OA protection.

That portion continues until:

- concentration ends;
- spell expires;
- actual removal/replacement occurs.

### Source ownership / stale cleanup

Each application owns its own:

- concentration dependency;
- pending damage rider;
- movement-protection record;
- endpoint.

When a newer successful Zephyr Strike replaces an older application:

- old application ends normally;
- its later stale deadline/removal callback cannot erase the new replacement.

Ending one cast releases only that cast's concentration/effects.

### Range

Confirmed: 30 ft is an **application gate only**.

There is no ongoing 30-ft tether after successful application.

---

## Drafting locks added by this clarification

Mark the following **NEW** in the exact manuscript where relevant:

- Magic Missile Storm missile numbering/allocation/order is fixed at commitment.
- One Shield targeting opportunity per allocated recipient per Storm; later missiles do not reopen it.
- Arcane Shield Shatter requires both effect and protected creature to satisfy perception/range/LoE, and hidden failure yields neither dispel nor damage.
- Arcane Shield Shatter identity is semantic/source-qualified, not name-substring based.
- Ignition Bolt critical bonus die applies only to the primary attack, never splash.
- Earth Tremor occupies one contiguous supporting surface only.
- Ice Knife captures its legal impact position before primary damage consequences.
- Thunderwave's 10-ft push is mandatory toward 10 ft, stopping only for actual legality.
- Witch Bolt tracks a **spell-specific used pulse opportunity** across outside→initiative transition without consuming the first real turn's unrelated general Action.
- Witch Bolt target death/ended creature existence ends its tether.
- Zephyr Strike consumes its strike rider on hit regardless of later damage prevention; movement protection remains independently active.

No cards are promoted by these decisions. Cosmology remains outside this work and deferred until after verified GitHub delivery.

