# GPT healing pulse boundary corrections

Complete connector reply. Source-audited/draftable; exact implementation still pending.

The added sources resolve most of the open scheduling questions. I would revise the prior pulse discussion as follows; none of this closes the 100-source package yet.

## 1. Paid three-pulse maintenance

Retract my earlier generic “no maintenance word means skip/resume” distinction for effects covered by the shared class rule.

For a **paid three-pulse sustained effect** covered by the frozen class paragraph:

- activation = pulse 1;
- pulse 2 is maintained during the next **regular** source turn;
- pulse 3 during the following regular source turn;
- pay the required upkeep and any required Bonus Action by that turn's end;
- missing required maintenance ends the effect at that turn's end;
- it cannot resume later;
- if both maintenance turns succeed, normal duration expires at start of source turn 4.

This controls:

- `cleric.hero.cultist.dark-sacrament`: **BA + 1 RP** for pulses 2/3, because `cleric.engine[5]` makes sustained Cleric maintenance a Bonus Action.
- `cleric.arch.sacrament`: same.
- `ranger.hero.warder.healing-briar`: activation pulse, then BA+1RP on next two regular turns; skipped maintenance ends it that turn end.
- `monk.hero.enlightened-master.circle-of-harmony`: same printed pattern.
- `shaman.engine[1]` Renewal: same.
- `tinker.hero.artificer.restoration-field`: **NEW/default class-pulse integration:** activation pulse, then BA+1RP on next two regular turns; skipped maintenance ends it that turn end.
- Paladin sustained Oath zones under `paladin.engine[11]`: first pulse included; 1RP later upkeep, plus any card-specified action such as Desecrated Ground's BA.

`Nano-Aegis Drone` is different. Its BA+1RP is a **commanded support use**, not maintenance. Missing a command does not end support mode.

---

## 2. Song of Mending is not prepaid

`oracle.supplement.life.song-of-mending` is a persistent healing aura and therefore uses `oracle.engine[26]`.

So its base schedule is:

- activation Action + 3 RC → pulse 1 immediately;
- concentration required;
- before its next regular-start pulse, pay **1 RC**;
- if unpaid, end the effect instead of pulse 2.

Enhanced Song:

- duration becomes 3 rounds;
- second later regular-start pulse is added;
- pay another **1 RC** before that third pulse.

No Bonus Action is invented because engine[26] specifies payment but no upkeep action.

Thus base Song total cost if fully maintained = **4 RC**; Enhanced = **5 RC**.

This is not target-start timing; engine[26] applies to persistent healing zones regardless of whether the card's pulse is source-start or target-start.

`Transcendent Meditation` remains separate: its printed finite limited-use sequence is prepaid and has no Oracle engine involvement.

---

## 3. Burning Blood Boon V

Confirm the proposed disposition.

It is **Curse Boon V**, not the Mystery Final. `oracle.engine[17]` explicitly distinguishes Curse Boon V from the level-20 Final Revelation.

Therefore `oracle.engine[26]` applies to its persistent damage/healing aura:

- activation-funded window 1;
- concentration required;
- pay 1 RC at source-next-regular-start to fund window 2;
- another 1 RC at the following source regular start for window 3;
- missed payment ends the aura.

Its healing remains exactly:

> once on **your turn** when at least one enemy has taken qualifying fire damage from you.

Enemy target-start damage does not create one heal per enemy turn. Multiple enemies can satisfy the gate, but the self-heal remains once/source-turn and capped S+M.

---

## 4. Virtual timing correction

Confirmed. The previously reviewed Combat timing supersedes my ambiguous outside-initiative bridge.

Do **not** define later pulses as “activation time +6/+12” when a source/target already has a virtual regular-turn schedule.

If an effect is created at second 2 and the source's preserved regular-start phase is:

`0, 6, 12, 18...`

then later source-start pulses occur at:

`6, 12...`

not `8, 14`.

Likewise, target-start zones use each target's own preserved virtual regular-start markers.

Reordering, initiative departure/reentry, extra turns, removal and later initiative changes do not restart those markers.

Only where there is genuinely **no pre-existing regular-turn schedule** should the runtime establish one coherent six-second virtual schedule for that creature.

Also retain the existing distinction:

- bare outside-initiative N-round duration → absolute `application + N×6s`;
- explicit periodic profiles → their registered virtual source/target markers and pulse counts.

Never run both clocks for the same component.

---

## 5. Pulse priority versus duration expiry

Explicit periodic text overrides generic duration expiry when required to realize its printed pulse sequence.

### Wound Eater IV

It has **three source-start pulse opportunities**, not “three rounds from activation.”

- activation creates/funds the aura;
- pulse 1 = next source regular start;
- pulse 2 = following source start, after 1RC payment;
- pulse 3 = following source start, after 1RC payment;
- after pulse 3 resolves, effect ends;
- failure to fund pulse 2 or 3 ends it at that due marker before that pulse.

Do not expire it at the third source-start before resolving pulse 3.

### Hemostasis

Exactly three target-start healing opportunities:

- target next regular start;
- second target regular start;
- third target regular start;
- then record ends.

No separate generic source-round expiry erases the third tick.

### Finite three-round auras such as Crown Restored/Garden

These retain the ordinary source-controlled three-round deadline.

If activated during source turn 1, they expire at **source turn 4 start**, and start-expiry resolves before start-triggered effects.

Therefore a self-targeted Crown Restored can indeed receive only:

- source turn 2 self pulse;
- source turn 3 self pulse;

then expiry occurs at source turn 4 before another self start-trigger.

Its “maximum three pulses per creature” is a ceiling, not a guarantee of three.

The same principle applies to Garden/other target-start auras: actual target-marker opportunities inside the source-duration interval determine how many applications occur, up to the printed cap.

---

## 6. Oracle fixed beneficiary sets

Confirm one bounded fixed ally/enemy set per Oracle persistent-zone instance unless the card explicitly establishes separate sets.

For `Eternal Bloom`:

- choose at activation up to **3 living allies currently inside**;
- only those chosen allies receive recorded healing reserves;
- only those chosen allies receive Bloom's 1-HP floor while otherwise legal and inside;
- only those chosen allies receive its necrotic immunity while inside.

New entrants do not become additional Bloom beneficiaries.

For `Crown Restored`:

- fixed chosen ally set ≤3;
- the Oracle counts against that cap if the Oracle is chosen;
- owner is not an automatic fourth beneficiary.

This follows engine[26]'s cap on pulse **and aura benefits**. Do not create separate unlimited beneficiary channels for ancillary benefits.

---

## 7. Target/round arbitration domains

Use source-specific ledger domains rather than one universal rule.

### Oracle engine[26]

Key:

`zoneInstance + target + numberedRound`

A target cannot receive that zone's pulse benefit twice in one numbered round even if:

- a new funded source window opens later that same round;
- it exits and re-enters;
- initiative shifts.

Window eligibility and numbered-round eligibility must **both** pass.

Re-entry creates no healing pulse unless the card says entry healing.

Garden's first-entry/start **cure opportunity** is a distinct once-per-Garden target entitlement and can happen on entry even without HP restoration.

Resonant Seed's cure belongs to the creature's **first healing pulse**, not mere entry.

### Circle of Harmony

Its wording is unusually explicit:

> “A creature receives this named effect at most once per round.”

Use **NEW global named-effect arbitration**:

`"Circle of Harmony" + target + numberedRound`

across owners/instances.

A second Circle cannot heal that target again that round.

### Restoration Field

Use:

`fieldInstance + target + numberedRound`

The text says “same creature once/round” within this Field; it does not state global same-name exclusion across all Tinkers.

### Renewal + Echo

Parent and its Echo are one family instance:

`parentRenewalInstance + target + numberedRound/pulse`

They share:

- pulse ID;
- upkeep;
- ≤3 target budget;
- once-per-pulse/round benefit.

Independent Renewal Totems are separate instances.

Their same-name nonstacking rule means that when multiple Renewal auras offer the **same pulse opportunity/coverage**, use the strongest legal Renewal branch rather than adding them.

I would **not** invent a global once-per-round prohibition across separate Renewal instances at different scheduled pulse times. The source says same-name auras do not stack, not that separately paid pulses from different instances can never heal in the same round.

That distinction should be tested.

---

## 8. Echo Totem arithmetic/lifecycle

Confirmed.

Parent destruction → Echo lifecycle remains **DEFERRED** to the object/device package.

The scheduler receives caller-provided:

- `parentAnchorActive`
- `echoAnchorActive`

and never guesses destruction linkage.

The family target budget does not multiply if both survive.

If only the Echo is legally active for a Renewal pulse:

- Renewal source base = 2 HP;
- Echo numerical healing = `floor(2/2) = 1` **at the Echo source-value stage**;
- then run the applicable healing pipeline.

Do not calculate the full parent final heal after modifiers and simply halve that result.

Where parent and Echo both cover a target, construct both legal source branches with their correct modifier placement and use the stronger legal same-name result under the already-reviewed healing/totem arbitration. Never add both.

---

## 9. Suppression, payment and empty pulses

Confirmed.

Clocks continue during suppression/disablement; missed windows never bank or shift.

For a due paid pulse:

1. verify effect still exists/concentration/etc.;
2. identify due pulse/window ID;
3. declare legal targets where source requires declaration;
4. commit required maintenance cost/action;
5. mark opportunity consumed;
6. resolve output/components.

Full HP, Decay or later reduction to zero does not refund the pulse/payment.

### Independent non-healing components

`Transcendent Meditation` pulse 2's +1 Ki is independent of actual HP gain. If the pulse legally occurs but every heal is blocked, Ki still occurs.

If a suppression effect suppresses the **entire Transcendent Meditation effect**, both healing and Ki component are suppressed for that occurrence. No later catch-up.

If suppression expressly suppresses only healing, the independent Ki component can still resolve.

Helpers therefore should report a due pulse occurrence separately from the set of successful healing applications.

### No eligible recipients

Yes. A legal upkeep can maintain an effect with zero currently eligible recipients when the source allows “up to N” and specifies no minimum recipient requirement.

The pulse/window and costs are still consumed.

---

## 10. Nano-Aegis Drone

Exact bounded schedule:

- Action +2RP enters support mode;
- duration = 3 rounds;
- **no activation heal**;
- each healing/tempHP output requires a later Bonus Action command +1RP;
- at most 3 support pulses total;
- skipping a command does not end support mode;
- no more than one option from that command: heal **or** temp HP.

An extra full Action does not grant another Bonus Action, so it cannot itself create another Nano-Aegis command.

An extra turn does not change:

- the mode's three-pulse ceiling;
- its normal duration markers;
- any already-applicable numbered-round companion command ceiling.

For this pulse package, I would **not hardcode a new universal one-command-per-round rule inside Nano-Aegis itself**.

The caller should apply the existing shared companion command contract if that contract is active for the drone.

To promote that into this helper as an enforced command ledger, the next package needs the exact companion sources governing:

- whether one owner has one BA companion command per numbered round or per regular turn;
- how multiple drones/companions share it;
- whether support commands and damaging commands use the same budget;
- what extra turns do to that command allowance;
- command behavior while owner/drone is incapacitated/disabled.

Until then, this scheduler owns only Nano-Aegis's printed BA+RP requirement, duration and max-three pulse count.

---

## Revised implementation boundary

The pulse package is now **SOURCE-AUDITED / DRAFTABLE** with these corrected scheduler families:

- paid 3-pulse regular-turn maintenance;
- Oracle funded windows, including Song and Burning Blood V;
- explicit source-/target-start installment sequences;
- fixed Oracle target sets;
- source-specific target/round arbitration;
- native passive recurrence without generic three-cap;
- Renewal/Echo shared-family scheduling;
- finite Eternal Bloom reserves;
- source-native independent non-healing pulse components;
- device duration extensions that never create pulse capacity.

Still unresolved before implementation review:

1. Echo Totem parent/Echo destruction relationship — deferred.
2. Full companion command-budget semantics for Nano-Aegis — deferred to prepared companion/device/form package.
3. Any recurring healing/zone behavior in the **770 unfinished ordinary spells**, items, monsters or other unsupplied catalogs.
4. Broader object destruction/concentration/source-death lifecycle beyond already reviewed shared rules.

The scan of the 78 operational spell drafts finding no recurring-heal/zone lexical intersection is useful negative evidence for that catalog only; it does not close the unfinished 770 or other domains.

