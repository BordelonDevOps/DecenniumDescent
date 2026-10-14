The corrections are sound overall. The new V6 evidence closes Prone movement and gives the specific unseen-combat interaction we needed; the alignment text is also enough to bound Corrupted without turning alignment into compulsory behavior. Pasted text Pasted text Pasted text

1. **Corrupted/alignment — ACCEPT.** Use the recorded individual moral axis `Good → Neutral → Evil`; a failed Corrupted long-rest save moves one step toward Evil and leaves law/chaos unchanged. Already-Evil remains Evil. “Evil creature” means an individual explicitly recorded/tagged Evil; never infer it from ancestry, faction, creature type, appearance, or origin. Alignment changes do not compel behavior, PvP, party separation, or oathbreaking; Paladin conduct still keys off actual conduct clauses. This closes the narrow classification interface. Pasted text

2. **A/B — ACCEPT.** Incapacitation ending concentration is already part of the shared integration rules, so correct the provenance rather than relabeling it NEW. The Dazed mid-turn procedure is mechanically correct: previously spent Action/movement constrains the remaining mode immediately, nothing is retroactively undone, Bonus Actions remain unavailable, extra turns make their own mode choice, and extra-Action grants cannot bypass the one-Action ceiling.

3. **C Exhaustion — ACCEPT.** Recompute level-4 maximum HP from the otherwise-applicable maximum rather than repeatedly halving an already-halved number; clamp current HP downward when needed, never heal when the maximum later rises. Apply flat Speed modifications first, then level-2 halving; level 5 sets Speed to 0. Level-6 death remains death until resurrection. A source-specific prerequisite such as Moisture Dependency can block generic Exhaustion removal without itself removing a level unless its own text says so. The six source levels are recovered V6. Pasted text

4. **D Bleeding/Burning — QUALIFIED ACCEPT.** Restrict generic periodic ticks to the **end of regular turns**, with one tick per elapsed 6 seconds outside initiative; extra turns never multiply them. Re-evaluate the strongest active source record at each tick using expected damage, then DC, then earliest application. I agree with changing Bleeding's magical-healing endpoint: a **legal magical healing effect with positive pre-cap healing potential** ends generic Bleeding even if maximum HP or Corrupted reduces actual HP restored to 0. That follows Core's “magical healing ends it” more faithfully than requiring positive actual restoration. Generic ending methods clear all generic records; an effect explicitly ending only its own named source removes only that source.

5. **Invisible/Prone — ACCEPT with specific precedence.** Once Invisible's location is revealed to an observer, do **not** immediately re-grant the same advantage/disadvantage through V6's generic unseen rule solely because the creature is still visually invisible. Core's explicit “until location is revealed” endpoint is the specific rule for that Invisible condition. Actual special senses that see the creature bypass Invisible's penalties entirely. Independent concealment/hiding may still create its own modifiers later. For Prone, retain Core's ranged-attacker disadvantage as the specific conflict winner, while V6 supplies own-attack disadvantage, standing/crawling costs, and disadvantage to other attacks from beyond 5 feet. Pasted text Pasted text

Here is the bridge text I would implement.

## Dazed timing — provisional integration clarification

Dazed applies immediately when gained.

At the start of every affected turn, including an extra turn, choose **Action-mode** or **Movement-mode**.

- Action-mode permits at most one Action total during that turn, regardless of extra-Action grants. The creature cannot voluntarily spend Speed or Dash, though movement or teleportation expressly contained within the permitted Action still resolves.
- Movement-mode permits ordinary voluntary movement but no Action.
- No Bonus Action may be taken in either mode.
- Reactions are unaffected by Dazed.
- Forced movement remains legal.
- Dazed does not itself end concentration.

If Dazed begins after voluntary movement has already been spent that turn, Action-mode is unavailable for the rest of that turn. If an Action has already been taken, Movement-mode is unavailable. If both have already occurred, neither further voluntary movement nor another Action is available. Already resolved actions or movement are never undone.

## Periodic Bleeding and Burning — NEW provisional timing bridge

Generic Bleeding and Burning resolve once at the **end of each regular turn** of the affected creature. Extra turns do not produce additional periodic ticks.

Outside initiative, resolve one periodic tick for every six full elapsed seconds while the condition remains active.

Maintain separately recorded active source records for duration and removal purposes. At each tick, choose the active record with the greatest expected periodic damage. Break ties by higher ending DC, then earliest application. Resolve that record's magnitude, damage type and DC as one unit. Re-evaluate at the next tick if the active records have changed.

A generic condition-ending method that says it ends Bleeding or Burning clears all active generic records of that condition. An effect expressly ending only its own named application removes only that source record.

### Bleeding

Generic Bleeding deals damage equal to the affected creature's current proficiency bonus.

If the applying effect supplies a physical Bleeding damage type, use it. Otherwise generic Bleeding deals slashing damage.

An Action by the affected creature or an adjacent helper may attempt Medicine against the applying effect's DC; if no DC exists, use DC 10. Success ends Bleeding.

A legal magical healing effect with a positive healing amount before maximum-HP caps or condition reductions ends generic Bleeding after it resolves. It still qualifies if the target is already at maximum HP or Corrupted reduces the actual restored HP to 0.

### Burning

If an applying effect supplies a Burning magnitude, use it. Otherwise generic Burning deals **1d4 fire damage**.

An Action by the affected creature or an adjacent helper ends ordinary Burning. Complete immersion of all burning portions also ends ordinary Burning. A magical or otherwise exceptional flame ignores these generic extinguishing methods only when its own reviewed text explicitly says so.

If Burning remains after its end-turn damage, make a Dexterity save against the applying effect's DC; if no DC exists, use DC 10. Success ends Burning.

## Exhaustion derived values — NEW provisional integration clarification

Use the recovered six-level Exhaustion track cumulatively.

At level 4, maximum HP becomes:

`max(1, floor(otherwise-applicable maximum HP / 2))`

Always derive this from the maximum HP the creature would otherwise currently have. Never halve a previously halved Exhaustion value again.

If this lowers maximum HP below current HP, clamp current HP to the new maximum. If maximum HP later increases, current HP does not increase automatically.

For Speed, apply non-Exhaustion flat increases and reductions first, then apply level-2 halving once. Level 5 sets Speed to 0 and overrides that calculation.

Level 6 causes death. Reducing Exhaustion after level-6 death does not restore life.

### Generic Exhaustion recovery — NEW provisional rule

At the end of a completed **beneficial eight-hour long rest**, a living creature at Exhaustion level 1–5 removes **one Exhaustion level** if all of the following are true:

- it met the campaign's required food and water needs for that rest period;
- no active source explicitly blocks removal;
- the underlying cause is no longer actively imposing or refreshing Exhaustion.

Only one level may be removed by this generic long-rest procedure per 24 elapsed hours.

A source-specific recovery rule may remove additional levels exactly as printed.

A prerequisite such as required immersion may remove a block on recovery without itself removing an Exhaustion level unless that source expressly says it does.

## Fictional-substance dependence — NEW provisional endpoints

The existing dose, repeated-dose, tolerance, dependence and overdose procedures remain controlling.

### Maintenance

When an Addicted creature completes a long rest, maintenance becomes due for each named dependent substance.

If no qualifying maintenance dose is taken **after that long rest**, Withdrawal for that substance applies immediately and remains until its symptoms are suppressed or ended.

A dose taken before completion of the long rest does not satisfy that new maintenance requirement.

Taking a maintenance dose may end the current Withdrawal symptoms for that substance but does not remove Addicted.

### Tolerance

Track doses of each named substance in a rolling seven-day window.

After the third use within seven days, that substance's Tolerance rule applies.

A doubled dose counts as two doses for tolerance, repeated-dose and overdose accounting.

Tolerance clears after **seven complete in-world days with no dose of that substance**.

### Dependence recovery project

A creature may attempt to remove one named Addicted condition through a **seven-day recovery project**.

For each of the seven consecutive days:

- no dose of that substance may be taken;
- one hour of treatment or recovery work must be completed;
- one Supply is consumed.

Choose one treatment approach at the start of the project: Medicine, Religion or Alchemy.

At the end of day seven, make one check with that approach against the substance's printed dependence DC. If the existing daily-care rule grants advantage for continuous care, apply that advantage to this final project check.

Success removes Addicted and its associated Withdrawal. Failure leaves Addicted in place. Critical Failure adds no new automatic injury or Wound; the spent time and Supply are the consequence.

A new attempt requires a new seven-day project.

Magic that only removes symptoms can suppress Withdrawal but does not satisfy the seven no-dose days or remove Addicted unless that effect explicitly says it removes dependence.

## Intoxication Track — NEW provisional recovery and emergency bridge

Use the existing source track from 0 through 5.

### Natural reduction

If no new Intoxication is gained:

- levels 1–3 decrease by one level after each full elapsed hour;
- gaining another Intoxication level resets the current hourly reduction timer;
- level 4 uses its special duration below instead of hourly reduction;
- level 5 does not naturally reduce.

### Level 4

Upon first entering level 4, roll **1d4 hours** and record the end time. The creature is Unconscious for that duration unless another reviewed effect ends that Unconscious state.

Also make a **NEW Constitution save DC 14** against poisoning.

On failure, the creature is Poisoned while it remains at Intoxication level 4 or higher. On success, no Poisoned condition is added.

When the recorded 1d4-hour period ends, if the creature is alive, has gained no further Intoxication and is no longer at level 5, reduce the track to level 3.

### Level 5 medical emergency

On reaching level 5, start a **one-hour emergency timer**. Level 5 does not naturally decay.

A helper may spend **10 uninterrupted minutes**, consume one healer's-kit use and make a **Wisdom (Medicine) check DC 15**.

On success:

- end the level-5 emergency;
- reduce Intoxication to level 4;
- apply one Wound, unless the creature already has three Wounds;
- begin the normal level-4 1d4-hour Unconscious duration and poisoning save.

On failure, the creature remains at level 5. Another attempt may be made if sufficient time remains, consuming another healer's-kit use.

If no treatment attempt succeeds before the one-hour emergency timer expires, the creature dies.

An explicit spell, item or feature that removes Intoxication or the emergency state follows its own text instead.

## Corrupted alignment interface — source-grounded clarification

For Corrupted, use the creature's individually recorded moral alignment or explicit Evil tag.

The moral-axis progression is:

`Good → Neutral → Evil`

A failed Corrupted long-rest save moves the creature one step toward Evil. Law/Chaos alignment is unchanged. A creature already recorded as Evil remains Evil.

Never infer Evil from ancestry, species, creature type, homeland, faction membership, appearance or similar identity.

Alignment is descriptive and socially relevant but does not itself compel player conduct, PvP, party separation, confession, belief change or Oath failure. Conduct clauses, divine obligations and similar mechanics continue to evaluate actual actions under their own rules.

## Corrupted cleansing project — NEW provisional rule

An explicit spell, item or feature that says it cleanses or removes Corrupted uses its own procedure.

Otherwise, Corrupted may be removed through an eight-hour cleansing project in a secure location.

The project requires:

- one patient with Corrupted;
- one practitioner using Religion or Arcana;
- one Supply, committed and consumed when the project begins;
- eight uninterrupted elapsed hours.

At completion, the practitioner makes the chosen skill check against **DC 15**.

Success removes Corrupted.

Failure and Critical Failure do not remove Corrupted and add no new automatic condition, Wound or Exposure. The spent time and Supply remain spent.

Only one generic cleansing-project attempt may be completed for the same patient per 24 elapsed hours.

The project is not itself a long rest for the active practitioner. The patient may receive the project while otherwise resting if campaign rest requirements allow it; count elapsed time once.

If a cleansing project and the patient's long rest complete at the same timestamp, resolve the cleansing check first. Apply the Corrupted long-rest alignment save only if Corrupted remains afterward.

## Unity Exposure — NEW provisional PUBLIC playtest track

No owner-approved numerical Unity threshold table is present in the notebook history available to this review. The following is therefore newly authored provisional public mechanics, not recovered setting truth.

Track one Unity Exposure score from **0 to 6**. Use only the mechanical row for the creature's current score; do not add penalties from lower rows unless the current row explicitly says so.

| Score | Public mechanical effect |
|---:|---|
| 0 | No Unity Exposure effect. |
| 1 | Exposure is tracked but has no generic numerical penalty. |
| 2 | -1 on Perception or Investigation checks specifically made to distinguish similar identities, copies, duplicates or conflicting sensory impressions. |
| 3 | -1 on all Intelligence and Wisdom ability checks. |
| 4 | -1 on all Intelligence, Wisdom and Charisma ability checks. |
| 5 | Disadvantage on all Intelligence, Wisdom and Charisma ability checks. |
| 6 | Disadvantage on all Intelligence, Wisdom and Charisma ability checks and saving throws. The character retains full player agency and remains playable. |

These public mechanics never dictate what a character believes, whom they love, whom they obey, what memories are factually erased, or what hidden setting truth has been revealed.

### Unity Exposure recovery project

Unity Exposure does not decrease automatically from an ordinary rest.

A creature may perform a **three-day Anchor Project** in a secure Haven or equivalent safe location.

Each day requires:

- two hours devoted to the project;
- one Supply;
- no increase in Unity Exposure during that project's three-day span.

At completion, make a **Wisdom saving throw with DC 10 + the creature's current Unity Exposure**.

Success reduces Unity Exposure by 1.

Failure leaves the score unchanged.

The project cannot reduce more than one point. Another reduction requires another complete project.

An explicit reviewed effect may reduce Exposure differently.

### Director boundary

Director-only Unity material must remain separately packaged.

The public 0–6 score and penalties above are the entire generic player-facing mechanical consequence until additional source material is separately reviewed.

A Director may use private narrative information associated with Unity only when supported by reviewed Director material. Private information cannot silently impose additional numerical penalties, force player beliefs or choices, change loyalties automatically, delete a character, or reveal hidden plot truth to the player merely because the public score changed.

When future Director threshold material is reviewed, record it in a separate Director-only overlay keyed to the same 0–6 score rather than inserting secret content into the public condition record.

The most speculative numbers here are deliberately isolated as **NEW**: generic Exhaustion recovery, the seven-day dependence project, Intoxication DC 14/DC 15 and one-hour emergency window, Corrupted cleansing DC/time/cost, and the Unity threshold/recovery table. Those are now concrete enough for Codex to adversarially test rather than leaving the conditions indefinitely unresolved.