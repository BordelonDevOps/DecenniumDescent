# Twelve Enchantment cantrips — actual exact manuscript review

Conversation: Calibration Review
Turn: 7621fa6c-279e-4b42-925d-c41ddcb3dd45

I find **three required repairs** before promotion: **Mental Tap timing, Soothe Animal's maintained classification, and Beguiling Gaze's blinking/aversion wording.** The other nine are approved as authored.

## 1. False Comfort — approved

The exact card correctly uses an **actual Perception check** only. It creates no passive-Perception `-5`, no automatic check, and no hidden modification to the passive DC system.

Approved timing:

- first future target regular-turn end;
- entire current target turn excluded if application occurs during it;
- +6 seconds outside initiative;
- one qualifying check consumes the rider.

The subjective healing sensation remains nonmechanical except for the explicitly authored distraction rider. No actual healing or forced behavior is introduced.

No repair.

## 2. Glimmering Eyes — approved

Approved exactly as authored:

- Self;
- choose Persuasion or Deception at casting;
- printed `+2`;
- every actual check of that chosen skill during the minute;
- proficiency not required;
- strongest-flat-bonus rule;
- no eye-contact requirement;
- one application per caster, with successful recast replacing the chosen skill/application.

No repair.

## 3. Disrupt Memory — approved, including the special concentration interactions

The all-maintained-Concentration interpretation is approved.

On a failed WIS save, **every actual Concentration application personally maintained by the target ends**, including reviewed exceptions that allow more than one maintained spell/effect.

Therefore:

- **Wizard Spell Tether:** both simultaneously maintained concentration spells end. Its current reviewed operational card explicitly treats them as maintained concentration effects and makes one concentration failure end both.
- **Crimson Harmony:** both Veinweaves in the concentration group end.
- **Wizard Tethered Cast:** the tethered concentration spell also ends. Removing it from the ordinary one-slot occupancy does not stop it from being a sustained concentration spell; its own card still expressly subjects it to concentration saves. Its special damage-save handling does not immunize it against an effect that directly ends maintained Concentration.
- Any ordinary concentration effect the target is simultaneously maintaining under those exact exceptions ends as applicable.

The older historical Spell Tether phrase “without concentration” does not override the currently reviewed operational card.

Also approved:

- memory-only immunity can block the memory deletion without automatically blocking the independent concentration-ending component;
- an empty six-second memory window does not prevent concentration ending;
- held concentration spells use their ordinary ending procedures;
- mechanical action histories, completed events and non-Concentration Ready state are not erased merely because autobiographical recollection is lost.

No repair.

## 4. Enthralling Tune — approved

The exact Perception interface is correct.

A check solely concerning caster/tone is unaffected; a broader search that materially concerns other subjects qualifies for disadvantage.

Approved:

- initial hearing gate only;
- V supplies the tone;
- no instrument;
- no continued performance;
- no continuing hearing tether;
- no passive-Perception adjustment;
- no concentration loss;
- first future target regular-turn end, excluding the entire current turn.

No repair.

## 5. Mental Tap — **required timing repair**

The `actualDamageDealt` calculation is correct. The issue is when the +1 benefit comes into existence.

Current text says:

> Finish this spell’s damage packet and its immediately due damage/concentration consequences before establishing the new benefit.

That excludes a concentration save **caused by Mental Tap's own damage**. I do not think the source supports that exclusion.

The source says the caster gains `+1 to next save if damage dealt`. Once defenses/HP handling establish `actualDamageDealt > 0`, the condition has been satisfied. A concentration save subsequently caused by that damage can therefore legitimately be the caster's **next save**.

This is not retroactive: the initial INT save has already resolved, and actual damage must already have occurred before the benefit exists.

Replace the relevant effect text with:

> **After defenses and actual HP handling determine `actualDamageDealt`. If it is greater than zero, establish the +1 benefit immediately at that point. It cannot modify the target’s already-resolved initial Intelligence save or any saving throw that resolved before `actualDamageDealt` became known. A saving throw subsequently caused by that damage, including your own concentration save if you targeted yourself, can be the next qualifying save and may consume the benefit.**

Retain everything else:

- automatic-result save consumes without changing automatic outcome;
- no save event means no consumption;
- later zero damage does not erase an older benefit;
- one pending benefit per caster.

This is the smallest source-faithful timing rule.

## 6. Friends — approved

The exact non-hostile procedure is good:

- hostility checked after payment;
- no free hostility oracle;
- no save;
- no Charmed;
- eligible successful application replaces prior target;
- an ineligible/no-benefit cast does not erase the valid existing application;
- later actual hostility ends that application permanently;
- no continuing 30-ft tether.

Social checks still require their ordinary communication/context.

No repair.

## 7. Soothe Animal — **required maintained-target repair**

Everything is approved **except**:

> “Losing the qualifying Beast/animal classification ends the calm…”

That creates an ongoing target-eligibility tether that neither the source nor the conference established.

The Beast/animal predicate should determine **legal application**, not continuously police the spell after it successfully affects the same continuing creature.

Remove:

> **Losing the qualifying Beast/animal classification ends the calm; the record does not follow a later return to that classification.**

Replace with:

> **The Beast/animal predicate is checked when the spell resolves. A later transformation or classification change does not by itself end an already-applied calm on the same continuing creature unless that transformation’s actual rules expressly end or suppress the effect.**

This is analogous to our other creature-target effects: changing a qualifying characteristic after successful application does not automatically become an unprinted dispel condition.

Everything else is approved:

- hidden eligibility after payment;
- WIS save;
- one minute/no concentration;
- no voluntary initiation of harmful actions;
- hostile commitment by another creature ends calm before that attack/effect resolves, even if it later misses;
- positive resolved damage packet ends it;
- fully prevented zero packet does not;
- no retroactive cancellation of an already committed action;
- no Frightened removal.

## 8. Faction Sympathy — approved

The caster's faction affiliation is an **application-time snapshot**, not a continuing membership tether.

Approved:

- actual affiliation/membership rather than reputation;
- F component and concentration retained;
- WIS save;
- +1 only to faction-related Persuasion;
- later membership change neither retargets the faction nor automatically ends the existing effect;
- caster's own harmful commitment ends it;
- another actor triggers the ending only when the target actually recognizes that actor as acting for the faction.

That recognition requirement does not perform hidden membership detection.

No repair.

## 9. Alignment Empathy — approved

The caster's actual alignment orientation is correctly snapshotted at application.

Approved:

- no axis disclosure;
- no alignment change;
- target alignment need not match;
- one `+1` Persuasion entitlement;
- once spent, the subjective feeling may continue but creates no second bonus;
- one application per caster/target pair;
- later caster alignment change does not rewrite the existing application.

No repair.

## 10. Resonance Whisper — approved; conference typo resolved correctly

Your interpretation is correct.

For **Disturb**:

- target makes WIS save even if willing, absent an independent save-waiver rule;
- **target fails save → `-1` rider applies/replaces existing Whisper**;
- **target succeeds save → no new rider and existing valid Whisper remains**.

My prior sentence saying “failed Disturb save creates no replacement” was contradictory and should be treated as an error. The exact card has the intended procedure.

Also approved:

- Guide `+1` follows strongest-flat-bonus rules;
- Disturb `-1` is a penalty and can arithmetically coexist with an independently permitted Resonance Mote `+1`;
- one cross-caster Whisper record means Guide and Disturb cannot be banked simultaneously.

No repair.

## 11. Minor Suggestion — approved

The exact additions are sound.

Approved:

- language compatibility resolved after payment;
- no hearing requirement for the implanted mental idea;
- V remains audible as a casting component;
- actual harmlessness resolved after payment;
- WIS save;
- one-minute salience;
- first real Persuasion check supporting that exact idea consumes the advantage;
- one application per caster/target pair;
- successful later implant replaces that caster's prior one;
- saved/invalid cast does not erase the old one.

I also approve the **maintained harmlessness** completion here. If circumstances materially change so carrying out the idea becomes non-harmless under the spell's own explicit exclusions, the remaining magical salience and unused mechanical advantage end. The target can still ordinarily remember having had/heard the idea.

That is not forced memory deletion and does not reveal why circumstances became unsafe.

No repair.

## 12. Beguiling Gaze — **required wording repair**

The underlying mechanic is approved, but the present wording unnecessarily makes the voluntary/involuntary distinction depend on whether a blink is “involuntary,” which could create arguments about ordinary conscious blinking.

The source promises **cannot look away**, not “cannot blink.”

Replace this portion:

> While locked, it cannot voluntarily avert its primary gaze from you or voluntarily close/cover its visual organs to break or evade that gaze. In particular, it cannot evade an independently actual gaze rule by claiming that voluntary eye closure has a different intended benefit. Ordinary involuntary blinking or another actual involuntary loss of sight is not a compelled harmful action.

with:

> **While locked, the target cannot voluntarily avert its primary gaze from you or deliberately close, cover or otherwise block its relevant visual organs in a manner that would meaningfully break or evade the maintained gaze, regardless of the stated reason for doing so. Ordinary momentary blinking that does not meaningfully break mutual visual contact remains possible. An actual involuntary loss of sight or visual contact can end the lock normally.**

This does two things:

- closes the “I closed my eyes for another reason” intent loophole;
- makes ordinary blinking explicitly legal without needing to litigate whether each blink was voluntary.

Everything else is approved:

- WIS save;
- real gaze/analogous-sense predicate;
- first future target regular-turn end excluding current turn;
- target may act/move/cast normally;
- target may deliberately move out of range, causing the lock to end;
- no forced following or facing engine;
- caster may release gaze freely;
- later successful save does not mechanically replace old lock, although breaking the old contact to establish the new gaze can independently end it;
- no gaze attack is granted.

## Disposition

Apply exactly these three repairs:

1. **Mental Tap:** establish the +1 immediately after `actualDamageDealt > 0` is known, allowing a subsequently triggered concentration save from that damage to qualify.
2. **Soothe Animal:** remove ongoing Beast/animal-classification maintenance; eligibility is checked at application only unless another actual source expressly ends the effect.
3. **Beguiling Gaze:** replace the eye-closure language with the objective meaningful-gaze-break rule above and explicitly permit ordinary blinking.

After those changes, all twelve Enchantment cantrips may be promoted to:

> **REVIEWED authored operational PLAYTEST manuscript — runtime, human balance, and broader Enchantment/social-control integration pending**

The catalog would then move from **198 → 210 reviewed identities**, leaving **638 unfinished** of the preserved 848.

