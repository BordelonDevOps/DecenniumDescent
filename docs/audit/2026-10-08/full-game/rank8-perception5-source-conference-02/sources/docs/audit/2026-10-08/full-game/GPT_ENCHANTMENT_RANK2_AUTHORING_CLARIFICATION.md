# GPT rank-two Enchantment — authoring clarification

Conversation: Calibration Review
Turn: e0cab35f-f593-40e3-9240-c84cbee97308

These clarifications do **not** promote any card. They refine the seven rank-two Enchantment manuscript before exact authoring. Catalog remains **222 reviewed / 626 unfinished**.

## 1. Dire Charm / Crown of Madness attack orders

**Approve the broader reading.** Do **not** import Confusing Flash's explicit one-attack restriction.

When Dire Charm or Crown of Madness orders the target to take the **Attack Action**, it uses that creature's actual ordinary Attack Action, including any attacks inherently granted by that Action:

- Extra Attack;
- an NPC's ordinary native Multiattack, if Multiattack is actually its ordinary Action;
- ordinary weapon/natural/unarmed attack sequences actually contained in that Action.

The compulsion still grants **no additional Action or attack beyond what that Action normally contains**.

### Ammunition/resources

Required ordinary ammunition that is intrinsic to executing the chosen ordinary attack is spent normally. Examples: arrows, bolts, loaded mundane ammunition.

The compulsion cannot require activation/expenditure of:

- consumable magic items;
- limited-use ammunition with a distinct expendable feature;
- RP;
- spell slots/spellcasting;
- class/monster recharge uses;
- per-rest abilities;
- optional superiority/resource dice;
- charges;
- other optional finite resources.

If the ordered ordinary attack cannot be legally completed without prohibited optional expenditure, choose another legal ordinary attack method where the order leaves that choice to the controller. If none exists, that attack instruction fails; no replacement resource is created.

**NEW CROSS-SPELL RULE — ordinary compelled Attack Action:**  
A compulsion saying to take an ordinary Attack Action grants the Action's native ordinary attack sequence unless that spell expressly says “one attack.” Confusing Flash remains the explicit one-attack exception.

---

## 2. Dire Charm component/replacement architecture

Dire Charm has **two independently applied components**:

- `Charmed(caster → target)`
- one cross-caster `DireCharmServant(target)` control record.

Treat each cast as having its own application ID for repeat-save cleanup.

### New cast: Charmed succeeds, servant blocked

Example: Caster A already owns the servant record. Caster B casts Dire Charm; target fails WIS, can be Charmed, but B's hard servant component is blocked.

Result:

- B establishes its own Charmed relation.
- A's existing servant record **remains**.
- B does not replace the servant record because B never successfully established one.

If B already had a Dire Charm Charmed relation, B's newly successful Charmed component refreshes/replaces **B's own Charmed relation**, not A's.

### New cast: servant succeeds, Charmed immune

If the target is immune to Charmed but the servant component can legally establish:

- new servant component is valid;
- it replaces the previous Dire Charm servant record across casters;
- no Charmed relation is created.

So yes: **servant-only Dire Charm can replace the old servant.**

### What replacement ends

Successful servant replacement ends only the previous **Dire Charm servant component**. It does not erase:

- another caster's independent Charmed relation;
- unrelated Charm effects;
- other control spells.

Successful Charmed establishment replaces/refreshes only that **same caster's Dire Charm Charmed relation**.

### Repeat saves

Each Dire Charm application tracks which components it actually established.

When that application's repeat save succeeds, end **only still-active components originating from that application**.

Therefore:

- B's Charmed-only application save ends B's Charmed relation, not A's servant.
- C's servant-only application save ends C's servant, not unrelated Charmed relations.
- A full application save ends both A components still active.
- If a servant was already replaced by another cast, the old application's later repeat save cannot destroy the replacement.

Hard-control history is never refunded.

**NEW CROSS-SPELL RECORD RULE — split applications:** independently scoped components retain source application IDs; replacement of one component does not silently replace unrelated components from that or another caster.

---

## 3. Conflicting compulsory instructions using the same action economy

A shared arbitration rule is needed.

### NEW CROSS-SPELL RULE — Compelled Budget Arbitration

Whenever two or more active compulsions demand incompatible use of the same ordinary:

- Action;
- movement allowance;
- ordinary interaction;
- or other single-use action budget,

resolve them without creating extra economy.

Each **specific mandatory instruction** receives a priority timestamp when that instruction is established:

- Command / Confusing Flash / Illusive Commands: when the failed-save command is successfully established.
- Dire Charm / Crown of Madness: when that turn's specific order is actually issued.
- simultaneous instructions: use underlying effect application order, then stable source/mechanical ID as neutral tie-break.

At execution:

1. Gather all still-active mandatory instructions.
2. Resolve earlier-priority instructions first.
3. If instructions are **compatible**, use one legal execution to satisfy as many as possible. One Action can satisfy multiple instructions only when the same Action genuinely fulfills them.
4. Once an earlier instruction validly claims an indivisible Action/inter­action budget, an incompatible later instruction cannot claim another copy.
5. A currently impossible/ineligible instruction consumes **no** budget; continue to the next instruction.
6. A losing ongoing instruction is merely ineffective for that conflicting budget **for that turn/opportunity**. It does not automatically end unless its own rule says so.
7. No priority loss refunds hard-control history or deletes the underlying ongoing effect.

Example: an earlier Command requires “Grovel” while a later Crown order requires an Attack Action. If Grovel requires only movement/posture and does not use the Action, both may be satisfied. If two commands require incompatible Actions, the earlier eligible instruction gets the Action.

A later invalid order never erases a valid earlier mandate merely by being issued.

This rule should be included in the exact-review shared spell overlay because it necessarily interfaces with previously reviewed Command and Confusing Flash as well as the new spells.

---

## 4. Dire Charm and Crown ongoing-order interfaces

### Dire Charm

Initial 30-ft/LoE is an **application gate only**.

Each target-turn order thereafter must actually be:

- consciously issued by the caster;
- audible to the target;
- understood by the target.

There is **no new 30-ft tether** after application. Ordinary hearing distance/barriers apply.

If the caster is Unconscious, Incapacitated in a way preventing the necessary communication, silenced, or otherwise incapable of consciously issuing the order, no valid servant order is created for that turn.

One brief Dire Charm order may coherently direct:

- ordinary movement;
- **one ordinary Action**;
- and the target's one ordinary free interaction,

within that same regular turn.

Example: “Go to the door, open it, and attack the guard.”

It does not control:

- Bonus Action;
- Reaction;
- separately granted extra Action;
- other independent permissions,

unless another rule does so.

### Crown of Madness

Initial 30-ft/LoE/Humanoid targeting is also **application-only**.

Later mental orders have no continuing range/LoE tether.

However, Crown grants **no remote sensory feed**. The caster receives no:

- current target location;
- target vision;
- memories;
- battlefield map;
- eligibility diagnostic;
- legal-target oracle.

The caster may mentally order only from information they actually possess. An order may reference an identifiable creature/location/action known to the caster, but legality is resolved from the real current state without revealing hidden failure reasons.

The caster must be consciously capable of forming the order. If they cannot consciously issue one at that turn-start opportunity, the target receives no order and retains ordinary agency for that turn, subject to other active effects.

---

## 5. Orders/repeat saves outside initiative

Yes. These spells cannot become stronger simply because no one formally rolled initiative.

### NEW CROSS-SPELL RULE — Out-of-Initiative Control Cadence

For an ongoing compulsion that explicitly depends on regular-turn **start order opportunities** or **end repeat saves** and begins outside initiative, establish six-second virtual target cycles.

At successful application:

- first virtual **START** occurs immediately after resolution;
- first virtual **END** occurs 6 elapsed seconds later;
- subsequent cycles repeat every 6 seconds;
- the spell's absolute 60-second maximum is unchanged.

The virtual cycle exists only to supply:

- the spell's order opportunity;
- one ordinary six-second behavior budget where needed;
- the spell's repeat save.

It does **not** independently refresh encounter Reactions/recharge/resources or manufacture extra combat turns.

### Entering actual initiative

Do not replay an opportunity already received.

At transition:

- an already-passed virtual START does not become another actual-start order;
- an already-resolved virtual END does not become another repeat save;
- thereafter use the target's actual regular starts/ends for future spell triggers;
- retain the original absolute duration deadline.

### Application during an existing target turn

If cast after that target's regular START:

- **no order opportunity occurs for the already-started turn**;
- if the spell specifies an end-turn repeat save, the current turn's upcoming END **does** grant that save unless the exact spell says otherwise.

This preserves the Dire Charm/Crown source cadence without creating retroactive beginning-of-turn control.

---

## 6. Calm Emotions / Zone of Truth exposure inside fixed zones

Yes to all proposed exposure behavior.

### NEW CROSS-SPELL RULE — Zone Eligibility History

For a fixed zone whose effect requires LoE/exposure from its center:

**Being geometrically inside but completely blocked by total cover is not yet an eligible exposure.**

If total cover later disappears while the creature remains geometrically inside, that moment counts as its **first eligible entry/exposure** for that application.

Then:

- Calm Emotions: willing creature accepts once, or unwilling creature makes its one WIS save.
- Zone of Truth: creature makes its one CHA save.

Once an application has an eligibility result:

- **failed save / accepted:** temporary later total cover suppresses that application's effect; restored exposure resumes it without another save.
- **successful save:** that creature remains unaffected by that application even after cover changes or leave/re-entry.

Independent spell applications retain completely separate:

- save/acceptance histories;
- durations;
- casters;
- concentration;
- zone endpoints.

Overlapping zones do not create extra magnitude from the same mechanic. A creature can nevertheless be affected by one application while having saved against another.

### Calm Emotions willingness

Willing acceptance occurs at first eligible exposure and is not a freely toggled choice afterward. The creature cannot simply decide later that it no longer accepts that already-applied spell absent an actual ending/removal permission.

### New Frightened application while already calmed

Confirmed.

If an affected creature acquires a new **Frightened** condition while Calm Emotions is actively suppressing Frightened:

- create the Frightened record normally;
- its duration clock continues;
- its scheduled repeat saves/maintenance continue;
- its mechanical Frightened effects are suppressed while Calm Emotions applies.

When Calm Emotions stops suppressing it, any still-existing Frightened record resumes its ordinary effects without replaying its initial application.

### Thematic class abilities

Also confirm your interpretation:

Calm Emotions does **not** disable Mooncursed, Momentum Rampage, Divine Fury, Fury of the Host, Beast Empathy, or another feature merely because its name/flavor involves rage, fury, emotion, empathy, moon madness, etc.

Only an exact source saying its mechanical operation depends on maintaining an emotional state would create such an interaction.

An independently actual **Frightened** rider from one of those features can still be suppressed as Frightened while the rest of the feature continues.

---

These are manuscript-integration clarifications only. The seven rank-two Enchantment identities remain **SOURCE-RECONCILED / not yet manuscript-approved**, and the catalog remains **222 / 626**.

