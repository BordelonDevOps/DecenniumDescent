# GPT Evocation cantrip source conference

Source: actual Calibration Review notebook reply; conversation 6a7a0fa2-eee0-83ea-92e9-6723a9f67ede, turn 23247d47-4279-4a1d-b1b5-703014114c08. Complete reply preserved below. Source reconciliation authorizes drafting only; no exact-card approval, runtime/balance approval or promotion.

I confirm the **complete Evocation-cantrip packet was available and reviewed**: all **12 identities**, all **14 source placements/Core blocks**, all exact class-access rows, dual-school Dancing Lights and Chill Touch, and every marked conference question. :chatgpt-content-reference{index="0"}

All twelve are **SOURCE-RECONCILED / DRAFTABLE** under the decisions below. No exact-card approval or promotion is implied.

## 1. Freezing Touch

**Action; Touch; one creature perceived and reachable with LoE; V/S; NEW melee spell attack.**

Hit: **1d4 cold** and schedule `−5 ft Speed` for the target's **next regular turn only**.

The movement rider does **not** begin immediately.

Exact timing:

- if cast before the target's next regular START, rider activates at that START;
- if cast during the target's current turn, that current turn is excluded and it begins at the following regular START;
- it ends at that affected regular turn's END;
- extra turns neither begin nor consume the rider.

Outside initiative, model the same “next turn” distinction with a virtual target cycle:

- no immediate Speed penalty;
- onset at application +6 seconds;
- endpoint at application +12 seconds.

If initiative begins before onset, map the pending onset to the target's next actual regular START without replay/reset.

The rider is triggered by the **successful spell attack**, not positive cold damage. Cold immunity can reduce damage to 0 without automatically negating the independent Speed rider unless the defense also covers that effect.

Multiple Freezing Touch riders never add `−5 + −5`; use existing slow-family arbitration against pre-control Speed. Separate applications can occupy different future-turn windows, so a cast during an already slowed turn may schedule the following turn.

No Frozen/Rooted.

**NEW:** melee spell attack and delayed next-turn timing procedure.

---

## 2. Flame Lash

There is a source conflict between effect text **“melee range”** and Core range **30 ft**. Preserve both by treating this as:

**Action; 30 ft; one creature or legally targetable object perceived with LoE; V/S; NEW melee spell attack with 30-ft reach.**

This is intentionally an unusual extended-reach melee spell attack rather than discarding either source statement.

Hit: **1d6 fire**.

If the **attack's actual target is an ordinary flammable object** with adequate fuel, it also ignites under ordinary mundane-fire procedures. The attack must still beat that object's actual defenses.

A creature hit by Flame Lash does **not** automatically have its clothing/carried equipment ignited. An item worn/carried by an unwilling creature must be separately legally targetable under actual object-targeting rules; the spell does not bypass those defenses.

No Burning condition. No ignition of stone, soaked material, metal, or another nonflammable target merely because the attack deals fire damage.

**CONFLICT RULING:** 30-ft melee spell attack preserves both raw range and printed “melee” character.

---

## 3. Soundburst

**Action; choose a perceived point within 5 ft and LoE; V/S; NEW 5-ft-radius sphere centered there.**

Every creature geometrically in the sphere with LoE from its center is affected, including caster/allies when included.

Each makes the printed **CON save**.

- failure: **1d4 thunder** + **Deafened** for one target round;
- success: no damage or Deafened.

Roll the `1d4` once and use the shared result for all failed saves.

Deafened duration ends at that creature's first future regular-turn END, excluding its entire current turn if already underway; outside initiative +6 seconds.

Thunder resistance/immunity affects damage only unless it expressly protects the Deafened rider. Deafened immunity affects Deafened without independently negating thunder damage. Neither component requires positive damage after the failed save.

No continuing aura.

**NEW:** point-centered 5-ft-radius geometry and exact Deafened clock.

---

## 4. Minor Combustion

**Action; 30 ft; one perceived ordinary flammable object/flammable portion with LoE; V/S; instantaneous.**

Operational size boundary:

> a torch, candle, lamp wick, tinder bundle, or comparable ordinary combustible object/portion no larger than roughly **1 cubic foot and 10 lb**.

That size boundary is **NEW**.

The target must possess adequate ordinary fuel capable of sustaining flame. Dry wood, wick/oil, tinder etc. can work. Stone, metal, saturated material, or an object otherwise incapable of mundane ignition does not become combustible.

Legal targets:

- unattended object;
- object the caster holds;
- object held/carried/worn by a **willing** creature.

An unwilling creature's carried/worn item is not a utility auto-target for this spell.

Ignition creates only the ordinary flame appropriate to that material. It conjures no fuel, oil, torch, resource, damage packet or Burning condition.

The resulting mundane flame can later spread/cause ordinary environmental hazards under existing fire rules.

No creature may be targeted directly.

**NEW:** size/fuel/held-object procedure.

---

## 5. Force Needle

**Action; 30 ft; one creature or object perceived with LoE; V/S; NEW ranged spell attack.**

Hit: **1d6 piercing**, exactly as printed.

For this attack, ignore AC bonuses from **partial/intervening cover that does not fully block line of effect**.

**NEW limitation:** total cover still prevents targeting because the spell has no LoE and no perceivable legal target through a solid barrier.

“Ignores cover” therefore does not provide:

- wall penetration;
- position oracle;
- armor bypass;
- resistance bypass;
- Force damage.

The damage type remains **piercing**, despite the name.

---

## 6. Arcane Echo

This needs the most explicit interface.

**Bonus Action; one willing creature perceived within 30 ft and LoE, including yourself; V/S; NEW arming duration up to 1 minute; no concentration.**

Apply one pending Arcane Echo arm.

### Qualifying original cast

The recipient's next legal **Action-activation damaging cantrip** qualifies.

This is an explicit **NEW limitation**: Reaction/Bonus-Action cantrips do not qualify as the triggering original. This avoids manufacturing or bypassing their trigger/action structures.

A cantrip qualifies based on its **selected legal mode having a printed damage payload**, not whether it later hits or actually damages HP.

At that original cantrip's **paid cast commitment**:

- consume the arm;
- record that exact cantrip identity;
- create one Echo-repeat permission.

This happens even if the original is later:

- Counterspelled;
- misses;
- deals 0 through resistance/immunity;
- otherwise fails after legal commitment.

An illegal/uncommitted attempt does not consume the arm.

For a Readied cantrip, qualification/consumption occurs at **preparation**, because that is the actual cast commitment. Release is not another cast.

### Echo-repeat permission

The recipient may cast that **same cantrip once again as a Bonus Action** before the end of their next regular turn after the qualifying commitment.

Outside initiative, repeat permission expires after 6 elapsed seconds.

This is a **genuine new spell cast**, not a copy.

Therefore the repeat:

- requires actual knowledge/repertoire/access to that same cantrip already demonstrated by the original cast;
- uses V/S and legal targeting normally;
- has its own attack/save/damage roll;
- can be Counterspelled;
- triggers ordinary cast hooks/outcome hooks;
- invokes Refrain as another same-ID actual cast;
- commits any real costs normally.

Arcane Echo changes only the repeat's casting type to **Bonus Action**. It grants no extra Bonus Action; one must actually be available.

### Anti-recursion

- One pending Arcane Echo arm per recipient across casters; successful new arm replaces old.
- One pending repeat permission per recipient; a newly triggered one replaces an older unused repeat.
- A cantrip cast **using an Arcane Echo repeat permission cannot itself trigger another Arcane Echo arm**.
- Arcane Echo cannot repeat Arcane Echo because Arcane Echo is not damaging.
- No spell knowledge/repertoire is transferred.
- No indefinite stocking; arm expires in 1 minute and repeat permission has the finite next-turn/+6s window.

**NEW:** willing recipient, one-minute arm, Action-damaging-cantrip qualification, actual-cast repeat, finite repeat window and recursion guard.

---

## 7. Shocking Grasp

Preserve the unusual printed **Reaction / 30 ft** source. Do not convert it to Action/Touch. :chatgpt-content-reference{index="1"}

**Reaction — when a creature you perceive within 30 ft and LoE begins an Action on its own actual turn, after that Action commits/begin hooks but before its first main outcome; V/S.**

The triggering creature is the only target.

Make a **NEW ranged spell attack**.

Hit:

- **1d8 lightning**;
- target cannot make **future Reaction commitments** until the end of its first future regular turn, excluding the entire current target turn if already underway.

Outside initiative, if a legal Reaction trigger exists under an actual action sequence, the denial lasts 6 elapsed seconds; do not manufacture standalone Reaction triggers just for this spell.

The triggering Action:

- is not canceled;
- retains committed costs;
- resumes after Shocking Grasp resolves unless another interrupt stopped it.

The reaction-denial rider is triggered by the **hit**, not by positive lightning damage. Lightning immunity does not automatically negate the independent reaction rider.

The rider:

- does not erase a Reaction already committed on the current LIFO stack;
- does not cancel the Action that triggered Shocking Grasp;
- grants no general Reaction refund/denial beyond its endpoint.

No metal-armor advantage.

An extra turn with an actual Action can provide the trigger.

**NEW:** Action-start Reaction trigger, ranged spell attack and one-round reaction-denial endpoint.

**Balance flag:** this is a very broad repeatable Reaction-damage trigger for a cantrip. Preserve it for source fidelity and test heavily rather than silently converting it to a familiar Action/Touch implementation.

---

## 8. Dancing Lights

Preserve both actual school placements:

- Evocation for its actual classes;
- Illusion for Bard/Mirrorsage/Monk/Thief.

The two modes use the same mechanics; actual school remains the casting class's placement.

**Action; 30 ft; choose up to four perceived legal points with LoE; V/S; NEW concentration up to 1 minute.**

Create up to four nonphysical torch-sized lights.

Each emits:

- **bright light 10 ft**;
- **dim light an additional 10 ft**.

These radii are explicitly **NEW** because no general torch radius exists in the reviewed source.

The lights produce real usable illumination under ordinary lighting rules regardless of whether the generating school is Evocation or Illusion. Illusion school does not make the light mechanically fake unless its source says so.

### Movement

As a **Bonus Action**, the caster may move any/all surviving lights up to **30 ft each** to new legal points.

Each light must remain within **60 ft of the caster** after movement. A light cannot pass through solid total cover/barriers and cannot occupy solid matter.

If a light becomes more than 60 ft away through external movement, it ends.

One Dancing Lights application per caster; successful recast ends/replaces the prior set through ordinary concentration transition.

No:

- heat;
- fuel;
- sunlight;
- damage;
- physical object;
- collision;
- automatic Invisible/Hidden revelation;
- generic magical-darkness dispel.

Ordinary illumination may, of course, remove darkness as the mundane reason a creature was not visible.

**NEW:** concentration minute, illumination radii, Bonus Action movement and 60-ft tether.

---

## 9. Acid Splash

**Action; 30 ft; choose one or two distinct targets perceived with LoE; V/S.**

No proximity requirement between the two targets is added.

Eligible:

- creatures;
- unattended legally targetable objects.

Each creature independently makes a **NEW DEX save**.

An unattended object automatically receives the failed-save damage result; an unwilling creature's worn/carried item is not separately targetable through this procedure unless ordinary object rules independently permit it.

Roll **1d6 acid once** and apply that shared damage to each failed creature/eligible object.

Successful creature save: no damage.

No residual pool, ongoing acid, armor corrosion, condition or splash to nearby entities.

**NEW:** DEX saves, shared roll and object procedure.

---

## 10. Chill Touch

Preserve both actual source schools/access:

- Evocation classes;
- Necromancy classes.

Actual casting school is whichever access row is used; lists are not unioned.

**Action; Touch; one creature perceived/reachable with LoE; V/S; NEW melee spell attack.**

Hit:

- **1d8 necrotic**;
- target cannot regain ordinary HP until the end of its first future regular turn, excluding the entire current target turn if already underway.

Outside initiative, rider lasts 6 elapsed seconds.

The rider triggers on **hit**, not positive necrotic damage. Necrotic immunity can negate damage without automatically negating the independent HP-gain restriction unless the defense says so.

While restricted:

- ordinary healing that would increase HP produces 0 HP gain;
- genuine excess healing is likewise 0;
- ordinary healing costs still commit;
- an actual HP-reserve/resource whose expenditure occurs only on legal positive HP restoration is not expended when gain is 0 under the established healing procedure.

It does **not** block:

- temporary HP;
- stabilization;
- non-HP condition removal;
- other non-HP healing components;
- a resurrection **LIFE TRANSITION's returned HP**.

It creates no corpse/soul seal and no anti-resurrection effect. No special Undead rider.

**NEW:** melee spell attack and one-future-target-END HP-gain rider.

---

## 11. Thunderclap

**Action; Self-centered 5-ft-radius sphere; V/S; instantaneous.**

Because the source explicitly says **all creatures within 5 ft**, the caster is included.

Every creature in the sphere with LoE from the caster independently makes a **NEW CON save**.

- failure: **1d6 thunder**;
- success: no damage.

Roll damage once and use the shared result among failed saves.

No Deafened rider—that belongs to Soundburst.

The sound is ordinarily perceptible according to normal hearing/environmental rules. Do not invent a fixed 100/300/etc.-foot alarm radius.

No persistent aura.

**NEW:** caster-centered geometry and CON save.

---

## 12. Poison Spray

**Action; 10 ft; one creature perceived with LoE; V/S.**

Target makes the printed **CON save**.

- failure: **1d12 poison**;
- success: no damage.

No attack roll.

No Poisoned condition, cloud, ongoing damage, inhalation requirement, breathing requirement, biological target prerequisite, or creature-type exclusion.

Actual poison resistance/immunity handles damage normally.

Damage remains **1d12 at all levels**; no automatic cantrip scaling.

This one needs essentially no substantive completion beyond explicit one-creature targeting.

---

# Shared Evocation-cantrip integration checklist

For exact-card authoring, carry these decisions consistently:

- **No F components** on this batch.
- Base **0 RP** does not bypass Refrain or ordinary casting commitment.
- Added attack/save mechanics above are explicitly **NEW**.
- No automatic cantrip damage scaling.
- Multi-target/AoE damage rolls are shared where specified; saves remain individual.
- A successful attack **hit** can independently establish a rider even when damage becomes 0 unless that spell explicitly uses a positive-damage trigger.
- Thunder/cold/fire/acid/lightning/necrotic damage does not manufacture unrelated conditions.
- Total cover/LoE remains unless a card expressly creates a narrower exception; Force Needle ignores non-total cover AC, not walls.
- Ordinary worn/carried objects are not free secondary targets.
- Slow-family movement arithmetic uses the existing pre-control-Speed strongest-result procedure.
- Reaction denial is prospective only.
- Dual-school identities retain their actual casting-school/access classification per class.
- **Arcane Echo repeat is an actual cast**, not a copy.
- Arcane Echo qualification/consumption occurs at actual cast commitment, including Ready preparation.
- Shocking Grasp is an interrupting spell but **not** an Action cancellation.
- Chill Touch is strictly an ordinary-HP-gain prohibition and does not alter resurrection life-transition rules. This uses the supplied healing/death boundary only and does not enter deferred cosmology. :chatgpt-content-reference{index="2"}

# Human-balance flags

Separate from source fidelity:

- **Shocking Grasp** as a 30-ft Reaction to any Action is exceptionally efficient.
- **Arcane Echo** can effectively enable two damaging cantrip casts through Action+BA across its trigger window and will interact strongly with Refrain/cast hooks.
- **Dancing Lights** four independently movable 10/10 lights provide substantial exploration utility.
- **Chill Touch** repeatable anti-healing can be very strong against healing-dependent enemies.
- **Freezing Touch** allows repeated future-turn slow scheduling, though numerical slowing itself does not stack.
- **Thunderclap** literally including its caster makes it tactically unusual and should be tested rather than silently exempted.

## Disposition

All twelve identities are:

> **SOURCE-RECONCILED / DRAFTABLE — exact authored-card review still required**

Current catalog remains **237 reviewed / 611 unfinished** until exact cards are authored, reviewed and promoted.

Cosmology remains untouched and owner-deferred until **after the authorized GitHub push and remote commit verification**.

