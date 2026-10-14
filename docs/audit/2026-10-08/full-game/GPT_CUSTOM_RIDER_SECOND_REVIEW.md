The broader scan changes several bindings, but it does not undermine the source-qualified registry approach. These additions should be implemented as distinct mechanical identities with narrow hook tags. Pasted text

1. **Mage Fire Focus / Inferno Lance — ACCEPT WITH ONE STACKING GROUP**

Use two application IDs:

- `mage.fire-focus.burn`
- `mage.inferno-lance.burn`

Both belong to:

- `family.ongoing-fire`
- `stackGroup: mage.fire-focus-burn:<sourceOwnerId>`

Source effects are:

- Fire Focus passive: `1d4 fire` at the **start of target's next turn**.
- Inferno Lance: `1d6 fire` at the **start of each of target's next 2 turns** on failed save. Pasted text

Use this **NEW binding rule**:

> Maintain each application's remaining tick schedule independently. At any shared tick marker, resolve only the highest-damage active application in this stack group. Do not add the dice together. Do not delete or shorten the weaker application's remaining duration merely because a stronger application won that tick.

So if Inferno Lance and the normal Focus passive both apply to one target on the same turn:

- shared first tick: `1d6`, not `1d6 + 1d4`;
- Inferno's second tick remains;
- a later ordinary Focus Burn may refresh its own one-tick record but cannot overwrite the stronger scheduled Inferno tick.

If Inferno Lance itself qualifies as the once-per-own-turn Fire Mage spell damage event, it may trigger the Fire Focus passive because the card says the passive occurs once on each of your turns when a Fire Mage spell deals damage. The resulting Focus Burn joins the same stack group and therefore does not create an extra shared tick.

`Elemental Surge` pointing to “Focus Burn” binds specifically to `mage.fire-focus.burn`, not Inferno Lance.

---

2. **Crippling Strike — ACCEPT: SLOWED, NOT CRIPPLED**

The active card is explicit: failed CON save halves Speed until end of next target turn, preserving the historical description “Slow effect.” Pasted text

Bind:

- `thief.crippling-strike.slow`
- `eligibility.slowed-foe`

Do **not** grant:

- `thief.crippled`

That identity remains tied to the reconciled Crippler poison package.

This is exactly why lexical similarity cannot determine mechanical identity.

---

3. **Warrior Disoriented — ACCEPT WITH PENDING/OPERATIVE SPLIT**

Use:

- `warrior.disoriented.pending`
- `warrior.disoriented.active`

On failed save, create the pending state until the start of that creature's next regular turn.

At that start marker:

- remove pending;
- create active through end of that same regular turn;
- no Reactions during active state;
- first voluntary movement attempt is direction-constrained. Pasted text

**NEW movement resolution:**

> When the creature first elects to spend voluntary movement during the active turn, determine uniformly among legal horizontal directions available to the movement mode it is actually using. A direction is legal only if the creature has enough remaining movement cost to enter the first required space/segment and that movement is otherwise legal.
>
> The first **up to 5 feet actually traveled** must follow that direction. This state never grants movement.
>
> If Speed/remaining movement is 0, no legal direction exists, or the creature never voluntarily moves, no displacement occurs.

For Terror Engine, only `warrior.disoriented.active` qualifies. The pending next-turn rider does not yet make the creature “currently Disoriented” for that hook.

---

4. **Shadow Rot — BIND AS ITS OWN TWO-STACK TRACK**

Use:

`monk.shadow-rot`

Track:

- `stackCount: 1..2`
- one shared expiry/save schedule;
- maximum two stacks.

Source establishes maximum 2 rounds, start-turn damage per stack, save penalties by stack count, and end-turn WIS removal. Pasted text

Use this **NEW timing/refresh bridge**:

> Applying a first stack starts Shadow Rot through the end of the target's second regular turn after application.
>
> Applying a second stack while Shadow Rot remains increases the stack count to 2 and refreshes the shared maximum duration to two target regular turns from that application.
>
> Applying another stack while already at 2 stacks does not create a third stack; it refreshes the shared duration to two target regular turns.

At the **start of each regular target turn**:

- each active stack deals `1d4 psychic`;
- one stack: `-1` on first saving throw that turn;
- two stacks: `-1` on all saving throws that turn.

This start-turn package occurs once per regular turn, never on extra turns.

At the **end of each regular target turn**, make one WIS save. Success removes **all stacks** immediately. Extra turns do not create extra removal saves.

Initial application still requires the printed damaged-unarmed-strike trigger and 1 Ki payment.

---

5. **Judged — STRAIGHTFORWARD DISTINCT STATE**

Use:

`cleric.judged`

Effect:

- `AC -1`
- two rounds
- refresh, never stacks. Pasted text

`cleric.arch.divine-invocation` Judgment mode applies the **same identity**, not a second condition. Pasted text

No generic “judgment” condition is created.

---

6. **Oracle Decay — PRESERVE THE FULL PACKAGE**

Use:

`oracle.decay`

It is not generic vulnerability.

Exact active components:

- cannot regain HP;
- `-1` saving throws;
- attacks against it receive `+S flat damage` once per attacker per turn;
- maximum three allied hits per round receive that flat bonus;
- corpses within 2 tiles cannot be raised while Decay persists;
- repeat CON save at end of each turn;
- maximum 3 rounds. Pasted text

Use distinct internal flags:

- `blocksHpRecovery = true`
- `savePenalty = -1`
- `alliedAttackFlatDamage = S`
- `perAttackerPerTurn = 1`
- `globalBonusHitCapPerRound = 3`
- `corpseRaiseBlockRadius = 2 tiles`

**NEW timing bridge:**

> Decay begins on the failed initial CON save. At the end of each **regular target turn**, make its repeat CON save. Success ends all Decay components. Failure retains them. After the third regular-turn endpoint following application, Decay ends after resolving that final repeat save regardless of result.

Do not translate the source's colloquial “vulnerability rider” into damage vulnerability or ×2 damage.

---

7. **Vengeance marks — SHARED ELIGIBILITY, SEPARATE RECORDS**

Use three IDs:

- `paladin.vengeance-mark.smite`
- `paladin.vengeance-mark.judgment-brand`
- `paladin.vengeance-mark.retribution`

All carry:

`eligibility.paladin-vengeance-marked:<paladinOwnerId>`

The eligibility is owner-qualified.

### Vengeful Smite
Duration: until end of owner's next regular turn.  
Repeated application refreshes its own record.  
If the target was already Vengeance-marked by that owner when the Smite began, add `S` flat damage. Pasted text

### Judgment Brand
Independent 3-round record with:

- 19–20 melee crit range;
- difficult-terrain pursuit benefit;
- once/round reaction pursuit trigger. Pasted text

### Mark of Retribution
Independent record through end owner's next regular turn:

- next Smite adds `1d8`;
- advantage on opportunity attacks. Pasted text

**Important consumption rule:**

> Consuming Mark of Retribution's next-Smite `1d8` rider consumes only that rider/record as its source requires. It does not delete Judgment Brand, Vengeful Smite's mark, or the owner's shared Vengeance eligibility if another qualifying mark remains.

Do not collapse the marks into one shared timer.

---

8. **Other named links/labels**

### Crimson Blood Mark

Use:

`crimson-agent.blood-mark`

Distinct from every generic `Marked` condition.

Rules remain:

- one target maximum;
- 5 of owner's regular turns;
- previous mark replaced without detonation;
- no automatic damage;
- no vision;
- no cover/planar bypass;
- enables only printed Blood Mark interactions. Pasted text

### Warrior Vulnerable

Use:

`warrior.brutality-vulnerable`

This is an **eligibility flag**, not damage vulnerability.

Applies while:

- visible/perceived hostile;
- within 60 ft;
- current HP ≤ one-quarter maximum HP.

It reveals neither exact HP nor resistances. Pasted text

Only Warrior features explicitly referencing Brutality Sense Vulnerable use it. A `-1 AC` effect, Judged, Decay, or ordinary damage vulnerability does not qualify.

### Turned

Use:

`paladin.last-rites.turned`

Exact payload:

> Until end target's next turn, it must use its **available voluntary movement** to move away from the protected creature by the safest legal route and cannot willingly move closer.

It is **not**:

- Frightened;
- Charmed;
- Dazed;
- an Action denial.

**NEW edge rule:** if no legal movement away exists or Speed is 0, no movement occurs; the creature retains its Action and other legal options, but still cannot willingly move closer. Pasted text

### Bloodbond

`crimson-agent.bloodbond` is a subsystem link, not a generic condition. It creates only its own redirection/temp-HP relationship. Pasted text

### Mirrorbind

`mirrorsage.mirrorbind` is an Action/capture subsystem, not a condition. `bound` in related text does not create a generic Bound state. Pasted text

---

9. **Cleric Doomed timed-buff acceleration — ACCEPT WITH PRECISE CLOCK RULE**

Use:

`cleric.doomed`

The source already states:

- HP healing reduced by `S+M`;
- positive timed buffs count down one additional round at end of target turn;
- lasts until next Sacrament pulse;
- repeated failures refresh, not stack. Pasted text

Adopt your bridge with this wording:

> **NEW timing bridge:** At the end of each **regular turn** of a Doomed creature, each active positive finite-duration buff **on that creature** whose duration is measured in rounds or seconds loses one additional round of remaining duration.
>
> For elapsed-time deadlines, subtract exactly **6 seconds** from that buff's expiry timestamp.
>
> For initiative-marker durations, advance its expiry by exactly one corresponding round toward the present. If this causes the expiry point to be at or before the current endpoint, end the buff immediately.
>
> Apply at most one Doomed acceleration to a given buff per target regular turn, regardless of duplicate/reapplied Doomed sources.

Do not accelerate:

- per-rest uses;
- recharge counters;
- permanent features;
- class path states;
- concentration itself;
- another creature's independent timer;
- hostile debuffs merely because they have positive consequences elsewhere.

If the underlying Sacrament ends before its next pulse, all Doomed records created by it end immediately. No orphan state.

---

10. **Core Charmed wording — CORRECTION ACCEPTED**

The earlier narrower operationalization should be corrected.

Core's phrase is **“Cannot willingly harm the charmer.”**

Use:

> While Charmed by a source, the creature cannot willingly take an action or make a choice it knows would directly harm the charmer, including attacking them, targeting them with a harmful effect, or knowingly placing them inside an area/effect expected to harm them.
>
> Accidental, unforeseeable, or genuinely unknown collateral harm does not retroactively violate Charmed.
>
> Charmed itself does not compel affection, obedience, belief change, allegiance, affirmative protection, or self-harm.

That preserves the broader Core meaning without turning Charmed into mind control.

---

# Shaman Blood Curse and generic Bleed cures

This needs **metadata**, not a blanket immunity.

Shaman Blood Curse says:

- CON save to apply;
- `1d4 necrotic` start of next 3 turns;
- Action + successful Medicine vs class DC ends;
- **magical healing permits an immediate CON save to end**. Pasted text

That specifically replaces the **magical-healing automatic cure endpoint**.

It does **not** prove that an explicit spell saying “end one ordinary Bleed” cannot remove it.

Use cure metadata:

```text
familyTag: bleeding
magicalHealingEndpoint: saveToEnd
ordinaryConditionRemoval: true
specialCureRequired: false
artifactLevel: false
```

Therefore:

- magical healing → immediate CON save, not automatic cure;
- Medicine Action → class DC, as printed;
- an effect explicitly saying **“end one ordinary Bleed”** can end Blood Curse Bleed unless that source is later tagged `specialCureRequired` or otherwise excluded.

For `Seal Minor Wound`, this means Shaman Blood Curse presently qualifies as an **ordinary Bleed** unless separate source evidence says the magical curse requires a special/artifact cure. The fact that it is magical does not by itself create cleansing immunity.

This distinction should generalize:

- **healing-triggered cure**
- **condition-removal cure**
- **special cure**
- **artifact/uncleansable**

are separate axes.

---

## Registry additions from this packet

Add at minimum:

- `cleric.judged`
- `mage.fire-focus.burn`
- `mage.inferno-lance.burn`
- `thief.crippling-strike.slow`
- `warrior.disoriented.pending`
- `warrior.disoriented.active`
- `monk.shadow-rot`
- `oracle.decay`
- `paladin.vengeance-mark.smite`
- `paladin.vengeance-mark.judgment-brand`
- `paladin.vengeance-mark.retribution`
- `paladin.last-rites.turned`
- `crimson-agent.blood-mark`
- `warrior.brutality-vulnerable`

And explicitly classify `Bloodbond` and `Mirrorbind` as **subsystem links/actions, not conditions**.

I see no additional blocker in this packet once those bindings are implemented. DD16 should nevertheless remain open until the registry validator confirms that **every active card reference resolves to a mechanical ID, family/classification tag, or deliberate descriptor-only term** rather than merely matching vocabulary.