# GPT Evocation cantrip authoring clarification

Source: actual Calibration Review notebook reply; conversation 6a7a0fa2-eee0-83ea-92e9-6723a9f67ede, turn 10428fac-7205-4501-b5e4-472c28fdb89b. Complete reply preserved below. Clarifications settle drafting scope only; no exact-card approval or promotion.

These are **authoring clarifications only**. No card is approved or promoted; catalog remains **237 reviewed / 611 unfinished**. Prior Evocation-cantrip source rulings remain in force except for the explicit refinements below.

## 1. Freezing Touch timing transition

Use this finite transition:

### Cast outside initiative

Initial virtual schedule is:

- **onset:** application +6 seconds;
- **expiry:** application +12 seconds.

If initiative begins **before +6**, map the pending onset to the target's **next actual regular START**, even if that START occurs before the original +6 timestamp.

There is **no +6 not-before floor after initiative begins**. Entering initiative supplies the actual “next turn” that the virtual +6 marker was representing.

Once onset maps to that regular START:

- the rider ends at that same regular turn's **END**;
- but it can never survive beyond the original absolute **+12-second cap**.

Thus whichever comes first ends it:

1. that affected regular turn's END; or
2. original application +12 seconds.

If initiative begins **after +6 but before +12**, the rider is already active. Do **not** manufacture a new full-turn window. It simply remains active until its original +12 deadline, unless another exact ending occurs.

### Cast initially in initiative, then leave

Confirmed: preserve the originally established future regular START and corresponding END as virtual markers. Do not reset them to “six seconds from when initiative ended.”

The spell always retains the same originally scheduled next-turn window.

### Extra turns

Confirmed. Extra turns:

- do not activate a pending rider;
- do not consume its regular START/END markers;
- do not create another duration window.

But if the `−5 ft` rider is already active during an extra turn, it **does affect voluntary movement during that extra turn**, because the creature is presently inside the rider's active interval.

**NEW timing completion:** pending next-turn effects map to actual regular START on initiative entry, while their original outside absolute maximum remains a hard cap.

---

## 2. Arcane Echo

Your proposed provenance/timing model is approved with one clarification: the repeat permission may be used **after the qualifying original's interrupt stack completely resolves**, including later in that same turn if a Bonus Action is still legally available. “Next regular END” is the expiry marker, not a delayed onset.

### Original qualification

A cantrip qualifies only if its **actual committed activation for that cast is Action**.

Therefore:

- ordinary Action damaging cantrip → qualifies;
- Ready preparation of an Action damaging cantrip → qualifies at preparation;
- a feature actually converting that cast to Bonus Action or Reaction → does **not** qualify.

Qualification keys from the cast that actually occurred, not the card's default activation in isolation.

### Provenance binding

**NEW — Echo provenance binding:** when the arm is consumed, record the qualifying original's:

- spell identity;
- actual casting class/source;
- actual school;
- rank 0 placement;
- selected damaging mode, where the identity has multiple modes.

The repeat must use **that same actual class/school/rank/mode provenance**.

It cannot use the same ID through:

- another class;
- another school placement;
- another rank;
- another source mode

to evade access, cost or other restrictions.

The repeat nevertheless chooses new ordinary legal:

- target(s);
- point(s);
- choices/parameters

per that same mode.

At repeat commitment, revalidate current:

- repertoire/known/prepared legality as applicable;
- class/source access;
- components;
- targets;
- action availability;
- other ordinary cast requirements.

If that provenance is no longer legal, the repeat cannot commit.

### Repeat consumption

The repeat permission is consumed at its own **legal paid Bonus Action cast commitment**.

If that repeat is later:

- Counterspelled;
- misses;
- saved against;
- deals 0 damage,

the permission remains spent. No refund.

The repeat is a fresh actual spell cast and has no continuing parent relationship to the original.

### Stack timing

The Echo repeat cannot be committed while the qualifying original's cast/counter/interrupt stack is still resolving.

Finish that stack first.

Afterward, if an ordinary legal Bonus Action opportunity exists, the repeat may be cast.

Countering the repeat:

- does not alter the original;
- does not revive/refund it;
- does not affect a separately pending Readied original.

### Ready interaction

Confirmed: Ready preparation can consume the arm and generate the repeat while the prepared original remains held for later release.

The repeat is a separate actual cast. Ordinary concentration transitions still apply to both procedures; if another cast legally breaks whatever state the held spell requires, resolve that normally rather than protecting it merely because Echo was involved.

### Anti-recursion

An Arcane-Echo-generated repeat **never qualifies another Arcane Echo arm**, regardless of any feature changing that repeat's activation back to Action.

This is lineage-based, not activation-text based after generation.

### Two separate clocks/records

Confirmed:

**Pending arm**
- anchored to the **Arcane Echo caster's** one-minute clock;
- one pending arm per recipient across casters.

**Generated repeat permission**
- belongs to the **recipient**;
- usable immediately after the qualifying original stack resolves when BA timing permits;
- expires at the recipient's **next future regular-turn END**, excluding the entire currently in-progress recipient turn from being its expiry turn;
- outside initiative: +6 seconds.

The consumed arm's later one-minute expiry cannot erase its generated repeat permission.

Therefore a recipient may simultaneously have:

- one pending unused Arcane Echo arm; and
- one already-generated repeat permission.

Casting a new Arcane Echo arm alone does **not** erase an existing repeat.

When an arm later triggers, the newly generated repeat permission replaces any still-unused older repeat permission.

That gives one arm + one repeat maximum, rather than stockpiling repeat casts.

---

## 3. Dancing Lights movement

Approve your proposed procedure.

### NEW — movement command legality

For each moved light:

- destination must be **perceived by the caster**;
- destination must have ordinary **LoE from the caster** at command time;
- destination must be within **60 ft of the caster**;
- movement follows a continuous legal non-solid path of no more than **30 ft**.

The path may curve around an obstacle rather than moving in a straight line, provided:

- it never passes through solid matter;
- actual path length is ≤30 ft;
- final destination otherwise satisfies perception/LoE/tether requirements.

No teleporting between positions.

### Ongoing existence

Caster-to-light LoE is **not** an ongoing maintenance requirement.

If a wall later blocks LoE:

- an unmoving light remains;
- it continues producing ordinary light, with illumination itself blocked normally by physical barriers;
- it cannot be commanded to a new destination until that destination satisfies command legality.

### Tether

The 60-ft tether is checked **continuously**, including movement of either the caster or the light.

If a light ever exceeds 60 ft, that light ends immediately. It cannot travel outside 60 ft and then return during the same movement.

One light ending does not end the others.

There is:

- no automatic following;
- no formation lock;
- no autonomous movement.

One existing Bonus Action may move **any or all** surviving lights once under the card's movement procedure.

No additional BA is generated.

---

## 4. Chill Touch HP-gain scope

Refine the source conference wording to the broader interpretation.

The source's **“can't regain hit points”** is an actual **broad current-HP-gain prohibition**, not merely an ordinary-healing prohibition.

### While affected

Any event that would increase the target's current HP instead produces **0 HP gain**, including:

- spell/feature healing;
- potions and ordinary healing effects;
- passive regeneration;
- natural recovery;
- a natural-20 death-save effect whose HP component would restore 1 HP;
- Stable-state recovery that would restore 1 HP;
- another direct current-HP restoration mechanism.

This applies to the affected target without adding an Undead/biological predicate.

Normal costs associated with attempted healing still follow the existing healing rules.

### What Chill Touch does not prohibit

It does **not** itself block:

- stabilization;
- successful death-save state changes that do not require HP gain;
- temporary HP;
- condition removal;
- damage prevention;
- maximum-HP changes;
- non-HP healing components.

And, under the already-established boundary, **returned HP belonging to an actual resurrection LIFE TRANSITION is not an ordinary current-HP gain event and is not blocked by Chill Touch**.

Chill Touch therefore creates no corpse/soul/resurrection seal.

This is a mechanical HP-state ruling only; it does not open deferred cosmology.

**NEW exact scope:** broad current-HP-gain prohibition, with LIFE TRANSITION and non-HP effects outside it.

---

## 5. Acid Splash object targeting

Approve the narrower boundary.

### NEW — Acid Splash legal targets

Acid Splash may target:

- one or two creatures; or
- one or two **unattended objects**;
- or a legal mixture thereof.

It does **not** separately target an object currently worn or carried by a creature.

A future rule could override this only by supplying explicit:

1. worn/carried-object eligibility; and
2. its resolution procedure.

This card supplies neither.

For unattended objects, no creature DEX save is invented; apply the spell's ordinary object-damage procedure after legal targeting. If exact object damage rules require immunity/material handling, those remain.

### Related spell boundaries

Confirmed:

- **Flame Lash:** attack spell; legal object targets use actual object AC. The spell itself grants no special permission to target an unwilling creature's worn/carried item.
- **Force Needle:** same principle—actual legal object target + attack versus its defenses; “ignores cover” does not manufacture worn-item targeting.
- **Minor Combustion:** retains its explicit willing held/carried-object utility exception from this conference.

---

## 6. Flame Lash and Shocking Grasp scoped bindings

### Flame Lash

Confirmed.

Its **30-ft melee spell attack** classification applies solely to that spell attack.

It does **not** change the caster's:

- general melee reach;
- threatened area;
- opportunity-attack reach;
- weapon reach;
- other melee spells.

Its object ignition is an independent **successful-hit rider** against a legal flammable object and remains subject to actual ignition/material/fire defenses.

It does not turn a creature hit into a vehicle for automatically igniting:

- clothing;
- armor;
- hair;
- carried gear.

Those would require separately legal object targeting.

### Shocking Grasp parent interruption

Confirmed.

Once Shocking Grasp is legally committed from its Action-start Reaction trigger, it is an independent paid interrupt.

If a nested Counterspell, Distract, or another legal interrupt subsequently removes/cancels the original triggering Action before Shocking Grasp resolves:

- Shocking Grasp still resolves if its own target remains legal;
- its attack may still hit/deal damage/apply prospective Reaction denial;
- it does not revive the removed parent Action;
- it does not refund the parent Action's costs;
- it does not refund Shocking Grasp;
- it does not require the triggering Action to remain pending as an ongoing tether.

The triggering Action was the **permission to commit the Reaction**, not a continuing condition for resolution.

---

## Authoring locks from this clarification

Mark these as **NEW** where they enter the manuscript:

- Freezing Touch initiative-entry transition: actual next regular START may precede original +6, but original +12 remains hard maximum.
- Arcane Echo repeat provenance is locked to the original actual **class/source + school + rank-0 damaging mode**.
- Arcane Echo qualification depends on the original cast's **actual committed Action activation**.
- Echo-generated repeat lineage can never re-arm Echo.
- Arcane Echo arm and generated repeat are separate records/clocks and may coexist.
- Dancing Lights later movement requires perceived/LoE destination, ≤30-ft continuous legal path, continuous 60-ft tether; no ongoing-LoE destruction.
- Chill Touch is a **broad current-HP-gain prohibition**, not healing-only.
- Acid Splash targets creatures and unattended objects only.
- Flame Lash's extended melee reach is spell-local only.
- Shocking Grasp survives removal of its triggering parent once legally committed.

No selection or promotion occurs from these clarifications. Cosmology remains deferred until after the authorized GitHub push and verified remote commit.

