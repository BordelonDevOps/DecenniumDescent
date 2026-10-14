# GPT rank-1 Conjuration exact manuscript review

Conversation: Calibration Review
Conversation ID: 6a7a0fa2-eee0-83ea-92e9-6723a9f67ede
Reviewed turn: 8eb53144-0b58-4a7c-9ea9-8c54f9f54fff

The batch is nearly ready. I approve the substantive reconciliations, including Core **2 RP** for Mod Rod, the Minor Weapon equipment profile, Flame Armor's queued retaliation, and the two-phase Alignment Essence vial. I find **three small manuscript repairs** before promotion: Heat Metal's initiative/out-of-initiative pulse bridge, Faction Messenger's ambiguous-description case, and Corruption Sensor's beep cadence.

## 1. Burning Sands — approved

The card matches the conference:

- one creature;
- automatic 2d6 fire subject to ordinary defenses;
- DEX save gates only the Speed rider;
- success does not halve damage;
- failed save halves Speed through the first future target regular-turn end;
- proportional slow uses the existing strongest-slow procedure;
- no field, Burn, blindness, Prone, difficult terrain, or hard denial.

The statement that fire immunity does not by itself remove the need for the slow save is correct because damage and rider are separate components.

No repair.

## 2. Shockwave — approved

The **15 × 5 × 5 ft** line and three-square grid representation are playable and bounded. One shared d10, DEX half rounded down, allies included, individual defenses after save scaling, and total-cover exclusion are correct.

No chain lightning, metal/water propagation, thunder, push, object damage, or persistent field is introduced.

No repair.

## 3. Summon Mod Rod — approved

### Core 2 RP conflict

Confirmed: use **2 RP restored**.

The spellcasting-domain authority explicitly supersedes overlapping Player Rulebook spellcasting conflicts, and the exact Core block says 2 RP. The preserved 1-RP V6/catalog text remains conflict evidence, not the operational value.

### Spent-use ledger correction

Your refinement is correct and preferable to my earlier “successful benefit” wording.

At activation start, commit:

- rod charge;
- original caster's character-wide **supply use**;
- bearer's character-wide **receipt use**;
- activation Action.

If later interrupted/prevented or if RP restoration resolves to 0, those remain spent. This matches the shared commit-before-interruption model and prevents retry farming.

Each character's own ledger refreshes only with that character's beneficial completed long rest under the existing recovery cadence.

Also approved:

- activation requires an actual RP pool;
- full pool remains legal and may restore 0;
- casting itself is not daily limited;
- lost unused rod may be replaced by paying another cast;
- replacing rods cannot refresh either ledger;
- 1 lb / AC12 / HP3 / no Integrity;
- concentration ending destroys the rod and its unused charge;
- no commodity/resource-generation loophole.

No repair.

## 4. Summon Minor Weapon — approved

The proposed physical completion is suitable:

- **3 lb**
- **AC 15**
- **HP 5**
- one-handed
- simple melee weapon
- 1d6
- choose B/P/S
- reach 5 ft
- no unstated Light/Finesse/Thrown/Versatile/Reach/etc.

The important source interpretation remains correct: it is a **wielded weapon**, not an autonomous spell effect.

Therefore:

- STR attack;
- STR damage modifier;
- PB only with actual simple-melee proficiency;
- Extra Attack/OA/weapon features only when their own requirements genuinely accept it;
- no attack granted by the casting itself.

“Magical weapon attack with physical damage type” is also the appropriate distinction.

No repair.

## 5. Flame Armor — approved

Both refinements are correct.

### Retaliation timing

Once a melee **attack roll actually resolves against the ward while active**, the retaliation is earned and queued.

Then:

1. finish that attack;
2. resolve its damage/interception/life consequences;
3. resolve concentration consequences;
4. even if those consequences end Flame Armor, resolve the already-earned 1-fire retaliation.

That avoids the contradictory outcome where an attacker qualifies under the active ward but destroying concentration with that same attack retroactively erases the trigger.

### Shared round guard

Approve the key:

**protected target + attacking creature + numbered round**

across all Flame Armor applications/casters.

Otherwise another caster could replace the ward after the first retaliation and reset the once-round limit. Replacement does not manufacture a fresh retaliation allowance.

The new packet's anti-chain restrictions remain correctly narrow while normal damage defenses, temp HP, concentration, and death consequences still operate.

No repair.

## 6. Heat Metal (Conjured) — one timing repair

The substantive procedure is correct:

- “Conjured” refers to the magical heat, not a conjured-item eligibility restriction;
- actual primarily-metal weapon/armor;
- no cast-resolution pulse;
- future wearer/holder start pulse;
- once per physical item per numbered round across applications/casters;
- handoff/recast cannot reset;
- no stored pulse when unused;
- no forced drop/disadvantage/Bonus Action pulse;
- dropping/doffing/melding suppresses exposure rather than ending the source;
- 1-minute concentration.

The only remaining ambiguity is the phrase:

> “preserve the next not-before deadline through initiative changes”

because the card does not explicitly define that deadline after **every** pulse.

Add this to the effect/limitations:

> **Whenever this spell deals a pulse, record a next-pulse-not-before deadline 6 elapsed seconds after that pulse. No later pulse from this spell on this physical item can occur before that deadline, even if initiative begins, ends or is reordered. In initiative, after that deadline, the first otherwise eligible current-user regular-start in a numbered round may pulse, subject to the shared item/round guard. Leaving initiative preserves the same deadline; the first outside-initiative pulse cannot occur before it. Entering or leaving initiative never resets either the deadline or a spent item/round allowance.**

For a newly cast spell with no prior pulse, its initial not-before deadline is already correctly **application +6 seconds** outside initiative; in initiative its printed first-future-user-start rule controls, provided no preserved transition deadline forbids it.

This makes mode transitions deterministic and closes the only remaining pulse-farming ambiguity.

## 7. Conjure Rope — approved

The exact command cadence is now complete:

- BA per command in initiative;
- one 6-second interval per command outside initiative;
- no zero-time command spam;
- 20-ft surface slither;
- simple tie/untie/coil/slack functions;
- cannot use slack-taking to lift or drag loads;
- physical arrangement persists outside command range.

The 300-lb static support ceiling, actual external anchor/support requirement, 10-lb rope mass, AC11/HP5 whole-object model, and ordinary Falling when support disappears are coherent NEW physical stats.

The command consumes an actual Bonus Action; it creates no additional companion-command/action allowance.

No repair.

## 8. Summon Familiar — approved

The profile correctly prints its own authorized scaling rather than relying on generic spell scaling:

- Small;
- AC `12+floor(PB/2)`;
- HP `2 × casting-class level`;
- Speed 30;
- saves PB;
- checks +0;
- ordinary sight/hearing;
- fixed acid/cold/fire/lightning/thunder choice;
- fixed melee/ranged mode;
- spell attack bonus;
- `S d6`, no ability damage modifier.

It also correctly shares the global owner command/offensive budget and remains distinct from Find Familiar and Summon Fire Pet.

No repair.

## 9. Resonance Bridge — approved

The support-loss addition is correct.

The bridge requires two actual qualifying supports throughout the spell. Loss of either required support ends the bridge immediately, just like:

- 0 HP;
- overload;
- concentration ending;
- spell ending.

The 1,000-lb load includes actual bodies, cargo, gear, melded carried mass where applicable, and real mass-changing states such as Petrified.

The “entry completes, then overload immediately collapses” rule is preferable to a caster veto and prevents the bridge from becoming an involuntary movement barrier.

No repair.

## 10. Faction Messenger — one identification repair

The overall bounded courier procedure is good. It does **not** magically authenticate membership, locate hidden recipients, penetrate disguises, report failure reasons, or find another faction member.

One phrase still needs to be deterministic:

> “identified by name or reliable description”

“Reliable description” can match several creatures at the designated destination.

Add:

> **A description must identify one intended creature well enough that an ordinary observer using only the supplied description and currently perceivable facts could distinguish that creature from other creatures at the destination. If multiple creatures fit the description equally and the courier has no ordinary basis to distinguish the intended recipient, it delivers to none; the spell provides no magical tie-breaker or identity revelation.**

This retains useful descriptions such as “the one-eyed quartermaster in the blue coat” while preventing “give this to one of the hidden faction members” from becoming magical identification.

Everything else is approved:

- known destination ≤300 ft;
- no positive-reputation requirement;
- initial route following without repeated BA command;
- later command requires 60 ft + perception;
- no retarget or second message;
- actual faction membership required but not reported;
- disguise can defeat recognition;
- paper note is conserved mundane matter, delivered or dropped rather than deleted with the summon.

## 11. Alignment Essence — approved

Your two-phase repair is the correct solution.

### Before consumption

- unused vial exists up to 600 seconds;
- ¼ lb;
- AC10;
- HP1.

### On valid full-dose consumption

- liquid disappears;
- snapshot alignment at that moment;
- empty conjured vial remains;
- visible result persists **60 seconds from consumption**, not merely whatever time remained on the unused-vial clock;
- then vial disappears.

Recasting replaces either the unused vial **or** current result-vial.

The result is meaningful and exact:

- Lawful / Neutral / Chaotic;
- Good / Neutral / Evil;
- unknown/protected axis = **Indeterminate**;
- a known unprotected other axis can still display normally.

Protected information is not overridden and the spell does not reveal *why* an axis is Indeterminate.

Voluntary drinking uses an Action. Forced ingestion requires independent actual authorization; the spell itself creates no force-feeding rule or save.

No repair.

## 12. Corruption Sensor — one cadence repair

The physical/detection model is correct:

- Tiny, 1 lb;
- AC12 / HP3;
- no Integrity;
- 1 minute;
- no concentration;
- current 10-ft LoE sensing radius;
- actual canonical Corruption predicate;
- ordinary 30-ft hearing;
- dynamic binary response;
- movable;
- suppression silences/disables without extending duration;
- no direction/severity/count/identity/telemetry.

The one missing playable value is **how often “repeatedly beeps” means**.

Add:

> **When the detection predicate changes from false to true, the sensor emits one beep immediately, then one brief beep each elapsed second while the predicate remains true. It stops immediately when the predicate becomes false. The cadence is fixed and conveys no additional information.**

This provides a deterministic audible procedure without creating a new mechanical benefit. In combat, no one needs six separate mechanical events per round—the beeps are informational sounds only.

---

## Disposition

Apply exactly these three repairs:

1. **Heat Metal (Conjured):** explicitly define and preserve a 6-second `next-pulse-not-before` deadline after every pulse across initiative-mode transitions.
2. **Faction Messenger:** make descriptive recipient designation uniquely distinguishable by ordinary observation or delivery fails without magical tie-breaking.
3. **Corruption Sensor:** immediate first beep, then one fixed beep per elapsed second while the binary predicate remains true.

After those repairs, I approve all twelve for:

> **REVIEWED authored operational PLAYTEST manuscript — runtime and balance validation pending**

The selectable catalog may then move from **132 → 144 reviewed identities**, leaving **704 unfinished** of the preserved 848. The Core/V6 Mod Rod conflict remains preserved, with **Core 2 RP** controlling operationally under the spellcasting authority manifest.

