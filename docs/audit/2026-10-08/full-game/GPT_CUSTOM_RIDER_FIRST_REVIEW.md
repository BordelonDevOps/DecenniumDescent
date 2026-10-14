The preservation strategy is correct: **display names stay source-faithful, mechanical IDs are source-qualified, and shared tags exist only for explicit cross-feature recognition.** The packet itself confirms that same-looking labels often carry materially different mechanics. Pasted text

## Proposed semantic-registry model

Each bound rider should carry:

`mechanicalId`, `displayName`, `familyTags`, `effect`, `applicationSource`, `ending`, `stacking`, `immunityTags`, `hookAliases`, and `sourceExceptions`.

A **family tag never imports mechanics**. It only answers questions such as “does this count as Weakened for Judging Light?” or “does Bleed immunity block this?”

### 1. Shaken

| ID | Effect / ending | Hooks |
|---|---|---|
| `warrior.shaken` | `-1 attack rolls` until end of target's next turn. Refresh, no numeric stack. | `warrior.terror-engine-state`; display alias `Shaken`. |
| `thief.shaken` | Disadvantage on the **next fear save**. Ends when that save is rolled/consumed or the printed duration expires, whichever comes first. | `thief.shaken`; display alias `Shaken`. |

Shiver Oil's critical **no Reactions** is a separate card rider and must not become part of `thief.shaken`. Terror Engine recognizes only Warrior-origin Shaken/Frightened/Disoriented because its card expressly says “by your Warrior features.” Pasted text Pasted text

**No notebook-authoritative universal Shaken exists.** Keep these separate.

---

### 2. Weakened

Use a nonmechanical hook tag:

`eligibility.weakened`

but preserve three source-qualified identities:

- `mage.dreadblade.weakened`: `-1 attack rolls` through end of target's next turn.
- `wizard.dreadblade.weakened`: same mechanical text, separate source ID.
- `warrior.weakened`: `-1 damage on each weapon or natural-weapon hit`, minimum 0, for its printed duration; refresh, no stack. Pasted text Pasted text Pasted text

**Judging Light hook:**

`active && hasTag("eligibility.weakened")`

It recognizes either family while active, but applies neither one's penalty itself. A suppressed/immune/inactive record does **not** qualify. Cleric's source only requires an active Cursed or Weakened condition. Pasted text

---

### 3. Crippled

This remains the first genuine unresolved binding.

Define the identity provisionally as:

`thief.crippled`

but **do not bind every slow or Speed penalty to it**.

The strongest evidence supports Crippler as the intended provider:

- ordinary hit: `-1 next attack before end next turn`;
- critical: additionally half Speed for that duration;
- Thief's engine later checks for `your ... Crippled`;
- Vile Tactics names a `Crippled` enemy. Pasted text Pasted text

I would bind Crippler as follows:

> **NEW binding:** a target affected by any still-active part of your Crippler package is `thief.crippled`. On a normal application, consuming the pending `-1 next attack` ends Crippled early; otherwise it expires at the printed endpoint. On a critical application, Crippled persists while either the pending attack penalty or the half-Speed rider remains active.

**Open blocker:** `Crippling Strike` itself is not present in this packet. Inspect that active card before adding it as another provider. No other slow automatically qualifies.

---

## 4. Bleed family

Create:

`family.bleeding`

All hostile Bleed variants may carry that tag, but retain their own mechanical IDs and exact schedules.

Important examples:

- `crimson.bleed`: 1d4 physical, **start** of next 3 target turns; ordinarily refreshes; Blood Echo allows exactly two independent instances. Healer's-kit Action ends all Crimson Bleeds. Pasted text
- `dragoon.bleed`: 1d4 physical, start next 2 turns; healer's-kit Action ends. Pasted text
- `ranger.bleed`: 1d4 on next 2 target turns from the melee-switch hit. Pasted text
- `shaman.blood-curse.bleed`: 1d4 **necrotic**, start next 3 turns; Action + Medicine vs class DC ends; magical healing permits an immediate CON save instead of automatically curing it. Pasted text
- `soldier.overwatch.bleed`: 1d4 start next turn. Pasted text
- `thief.bloodleech.bleed`: 1d4 start next 2 turns, subject to Thief poison-instance rules. Pasted text
- `warrior.bleed`: source mutation variants generally 1d4 start next 2 turns and explicitly refresh rather than stack where printed. Pasted text

### Damage type bridge

For a Bleed record described only as **physical** or lacking a damage type:

> **NEW:** use the applying direct physical hit's bludgeoning/piercing/slashing type when one exists; otherwise use **slashing**.

Explicit types such as Shaman Blood Curse's **necrotic** always win.

### Shared hooks

`family.bleeding` may be used for:

- explicit Bleed immunity, e.g. Mythic Carapace;
- broad effects that literally say `end all Bleed`;
- semantic checks for a Bleeding target.

But owner-qualified wording remains owner-qualified:

- `your Bleed` = source owner must match;
- Crimson Blood Mark/Blood Tithe/etc. do not trigger from another class's Bleed;
- Thief Sneak Attack's `your Bleed` requires a Thief-origin qualifying record. Pasted text Pasted text

`Seal Minor Wound` should remove **one ordinary/minor `family.bleeding` record**, but not a record whose source explicitly replaces ordinary curing with a special procedure. Shaman Blood Curse should therefore retain its printed cure interface rather than being silently trivialized. Pasted text

---

## 5. Burn / ongoing fire

Create:

`family.ongoing-fire`

Do **not** use `Resonance Burn` as part of this family.

Source-qualified examples include:

- `dragoon.burn`: 1d4 fire, start next 2 target turns, nonstacking.
- `druid.charbear.burn`: 1d4 next turn.
- `ranger.fire-burn`: 1d4 next target turn.
- `shaman.flask.burn`: 1d4 next turn.
- `shaman.cinderflame.burn`: 1d4 next turn.
- `tinker.burn-injector`: 1d4 next 2 target turns.
- `tinker.fire-bomb.burn`: 1d4 next turn. Pasted text Pasted text Pasted text Pasted text

For a periodic rider that merely says **“next turn”** without start/end timing:

> **NEW fallback:** resolve it at the **end of the target's next regular turn**.

Printed `start of next turn` wording continues to control where supplied.

`Crown's Burn` remains a feature name, not a condition-family grant. Resonance Burn remains the separate preserved Core condition and inactive under the current Dissonance configuration.

### Mage issue

The Mage engine's phrase that “ordinary Core V2 spell-risk rules still apply where applicable” must **not** reactivate historical Burn/fizzle on top of Dissonance. Wizard already states that explicitly. Pasted text Pasted text

**Open source issue:** this packet references Mage **Focus Burn** but does not supply its full active magnitude/timing profile. Bind `mage.focus-burn` only after that engine record is inspected.

---

## 6. Oracle Dread

Use one Oracle condition identity:

`oracle.dread`

Base mechanical payload:

`-1 attack rolls and -1 saving throws`

Source cards supply duration and repeat-save logic individually. Pasted text

Same-stat instances do not add together; maintain independent source durations only as needed.

Important separation:

- Nightmare Lash / Psychic Lash / Mind Spike may separately remove Reactions.
- That Reaction denial is **not part of Dread**.
- Extending Dread never extends Reaction denial unless the card expressly says so. Pasted text Pasted text

Fear immunity applies only when the application explicitly says it is fear-based, such as Ghost Chant. It does not globally immunize a creature against every Oracle Dread application.

Paladin Dominion's option named “Dread” mechanically applies **Core Frightened**, so its ID should remain something like:

`paladin.dominion.dread-mode → core.frightened`

not `oracle.dread`. Pasted text

---

## 7. Grief and Grief Mark

Keep separate:

- `paladin.grief-mark`: `-1 attack rolls` until end next turn; refresh, no stack.
- `paladin.grief`: `-1 attack rolls` and `-1 saving throws against Fear` until end next turn. Pasted text

No shared mechanical inheritance is justified merely by the shared word **Grief**.

---

## 8. Doomed vs Mark of the Doomed

Keep separate:

- `cleric.doomed`: healing received reduced by `S+M`, minimum 0; positive timed buffs count down one extra round at end of turn; until next Sacrament pulse; failures refresh rather than stack. Pasted text
- `oracle.mark-of-the-doomed`: source-specific mark granting +2 attack rolls for specified attackers, first-critical rider, and concealment interaction. It is a **mark**, not Cleric Doomed. Pasted text

`Mark of the Doomed` grants no global tracking, location knowledge, or generic Marked rights beyond its own text.

---

## 9. Root and Slowed hooks

Use:

`family.root`

Generic semantic payload:

> Speed becomes 0. Root by itself does **not** remove Actions, Bonus Actions or Reactions and does not import Restrained.

This matches the explicit Paladin and Shaman profiles. Pasted text Pasted text

For Druid Snow Leopard, do **not** infer qualification from effective Speed alone. Give applicable effects an explicit hook:

`eligibility.slowed-foe`

It should include:

- explicit hostile Speed reductions;
- explicit hostile Root.

Exclude unless another source explicitly adds the hook:

- Prone;
- difficult terrain;
- cargo/encumbrance movement costs;
- Exhaustion;
- Grappled;
- Restrained;
- voluntary Speed changes. Pasted text

That avoids bizarre qualification from every zero-Speed state.

---

## 10. Cursed and Diseased

Treat these as **classification tags**, not generic conditions:

- `classification.curse`
- `classification.disease`

They have no intrinsic penalty.

`Judging Light` recognizes an **active curse record explicitly tagged as a curse**, not:

- Oracle's protected permanent Curse engine;
- an Oath;
- ancestry;
- flavor text;
- an unrelated feature merely containing “curse” in prose. Pasted text

Likewise disease-removal effects must operate against an actual disease record.

### Tier/removability metadata still needed

Each curse/disease eventually needs fields such as:

- `magical`
- `finiteDuration`
- `ordinaryCleansable`
- `specialCureRequired`
- `artifactLevel`
- `treatmentDC`
- `tier`, where source actually supplies one.

This is necessary because active cards distinguish ordinary, finite, magical, artifact, and special-cure cases. Pasted text Pasted text

That tier taxonomy is a real follow-up dependency, not something this registry should invent globally.

---

## 11. Warrior Disoriented

Use:

`warrior.disoriented`

Source payload is preserved: at start of next turn, no Reactions; first 5 feet of movement go in a random legal horizontal direction; otherwise normal Action and movement. Pasted text

I recommend this exact bridge:

> **NEW:** Disoriented becomes operative at the start of the target's next regular turn and ends at the end of that turn. It cannot take Reactions during that turn. The first time it would voluntarily move, the Director randomly selects among legal horizontal directions and the first up to 5 feet of that movement must follow the selected direction. This does not grant movement or increase Speed.
>
> If Speed is 0 when the directional rider would be resolved, no displacement occurs and the rider is consumed.
>
> If no legal horizontal direction exists, no displacement occurs and the rider is consumed.
>
> The creature retains the rest of its legal Action and movement after that resolution.

That produces no free movement and no Action loss.

Terror Engine recognizes `warrior.disoriented` only when imposed by a Warrior feature.

---

## 12. Cellular Reconstruction Stasis

Use a source state, not a global condition:

`warrior.cellular-reconstruction.stasis`

Exact payload:

- Speed 0;
- no Action;
- no Bonus Action;
- no Reaction;
- attacks against have advantage;
- until start next regular turn;
- then printed healing and cleansing resolve. Pasted text

It is **not**:

- Downed;
- Unconscious;
- Petrified;
- incapacitation unless the card itself is later rewritten to say so.

Therefore it does not automatically cause Prone, dropped items, automatic STR/DEX save failure, death saves, or adjacent automatic criticals.

---

## 13. Descriptor-only vocabulary

Do not create generic conditions merely from these words:

`Bound`, `Disabled`, `Suppressed`, `Hidden`, `Sleep`, `Exposed`.

Registry rule:

> A lexical occurrence becomes a mechanical state only when its operative source defines mechanical consequences and an endpoint. Otherwise it remains description, metadata, or a source-local flag.

Examples:

- `bound` in Analyze Magic can describe a linkage, not restraint;
- `suppressed` means the named effect is temporarily inactive only where its source says so;
- `hidden` remains part of the future stealth/vision model and does not equal Invisible;
- `sleep` does not automatically equal Unconscious without operative text;
- `exposed` provides no universal vulnerability;
- `disabled` needs the defining subsystem's own state record.

---

## 14. Silence

Keep Core `Silenced` exactly separate from concentration.

Generic Silenced:

- blocks verbal components;
- command words;
- Chants;
- audible coordination.

It **does not end concentration** merely because concentration exists. A particular sustained effect can fail if its own text requires continuing audible speech, but that is the effect's requirement, not a universal Silence rule.

Likewise, a concentration-protection clause mentioning “Silence” does not create a generic Silence/concentration interaction.

---

# Cross-feature hook rules

These should be validator-visible:

| Hook | Qualifies |
|---|---|
| `cleric.judging-light.weakened` | Any **active**, unsuppressed `eligibility.weakened` record |
| `cleric.judging-light.cursed` | Active explicitly tagged `classification.curse` record |
| `warrior.terror-engine` | Warrior-origin `warrior.shaken`, Warrior-origin Frightened, or `warrior.disoriented` |
| `thief.sneak-attack.bleed` | Active hostile **Thief-origin** Bleed |
| `thief.sneak-attack.poisoned` | Poisoned state caused by that Thief's qualifying effect |
| `thief.sneak-attack.crippled` | Active `thief.crippled` |
| `thief.vile-tactics` | Its printed Bleeding/Poisoned/Crippled eligibility, without converting arbitrary slows into Crippled |
| `druid.snow-leopard.slowed` | Active `eligibility.slowed-foe` |
| `warrior.mythic-carapace` | Blocks `family.bleeding`, Core Poisoned, and `family.ongoing-fire` |
| Oracle Dread synergies | Only active `oracle.dread` unless card separately says Frightened too |

## Remaining concrete DD16 issues

I would leave only these genuinely open from this packet:

1. **Crippling Strike:** inspect the actual active card before deciding whether it provides `thief.crippled`.
2. **Mage Focus Burn:** recover its exact active magnitude/timing/stacking profile before binding `mage.focus-burn`.
3. **Curse/disease tier vocabulary:** reconcile “ordinary,” “finite,” “artifact-level,” “special cure,” treatment DC, and tier against actual spell/item/hazard records.
4. **Bleed source omissions:** where an individual active class card supplies damage/timing but no stacking/cure text, the binding overlay must either point to that class's engine rule or clearly mark the missing endpoint; do not silently import another class's Bleed behavior.
5. **Custom terms outside this packet:** DD16 remains open until every active class/spell rider is semantically bound, even if its display word happens to match one of these families.

So the right implementation architecture is:

**source-qualified mechanical IDs + narrow family/eligibility tags + exact per-card hooks.**

That preserves the actual class identities instead of turning vocabulary coincidence into shared mechanics.