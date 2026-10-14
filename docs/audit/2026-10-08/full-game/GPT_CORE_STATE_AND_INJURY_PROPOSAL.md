The new V6 evidence materially closes several provenance questions. I would adopt the following as the **active provisional integration overlay** for this subsystem. It preserves Core V2 authority, restores compatible V6 rules, and labels only actual gaps as new mechanics.

## 1. Exact precedence

For **attacks, damage, Wounds, death, stabilization, and related conditions**:

1. **Explicit approved feature text** governs when it states a specific exception.
2. **Core Systems Known Descent V2** is the domain authority for combat, Wounds, attacks, and conditions.
3. **Approved V6 Player Rulebook** remains active where its rule is compatible with and not displaced by Core V2. This specifically restores the recovered V6 rules for Instant Death, death-save details, Stable, death-counter reset, ordinary monsters at 0 HP, knockout, and temporary HP.
4. **Active Integration Overlay** below resolves sequencing or genuinely missing procedures. Every such rule is marked **NEW PROVISIONAL**.
5. **Review Gameplay Loop / V7.2 evidence** does not override Core/V6. A rule from it operates only when explicitly adopted as a gap-fill overlay, such as the current proposed Wound-treatment procedure.
6. Unresolved source conflicts remain preserved and inactive rather than silently combined.

The named **Wounded** condition should not yet be added on top of Wound-count mechanics. Its relationship to this subsystem belongs to the upcoming 28-condition audit.

---

# 2. General resolution

### Attacks — Core V2

`d20 + appropriate ability modifier + proficiency when proficient`

- Final total **meeting or exceeding AC hits**.
- Natural 1 always misses.
- Natural 20 always hits and critically hits.
- Critical hit doubles **damage dice only**.
- Beating AC by 10 has no generic critical effect.
- Explicit critical-range improvements may broaden the natural critical range, but do not stack.

### Task / skill / tool checks — Gameplay overlay retained where compatible

Use the four degrees:

- Critical Success: total ≥ DC + 10
- Success: total ≥ DC
- Failure: total < DC
- Critical Failure: total ≤ DC - 10

For these checks only:

- natural 20 improves one degree;
- natural 1 worsens one degree;
- bounded at Critical Success/Critical Failure.

If a specific task defines only success/failure, collapse Critical Success → Success and Critical Failure → Failure unless that task prints an additional outcome.

### Saving throws

Saving throws are binary unless the effect explicitly prints a margin result.

- `total ≥ DC` succeeds.
- `total < DC` fails.
- No generic natural-20 automatic success.
- No generic natural-1 automatic failure.
- No natural-roll degree shift.
- Printed `fails by 5`, `fails by 10`, etc. use the final total.

Death saves retain their own specific natural-1/20 rules.

### Opposed checks — NEW PROVISIONAL

- Higher final total wins.
- Exact tie preserves the existing state: the initiating creature fails to change the situation.
- Generic task natural-1/20 degree shifts do not create bonus/penalty values in opposed checks unless the maneuver itself explicitly uses degrees.

---

# 3. Temporary HP and damage accounting

V6 establishes that temporary HP is lost before normal HP, does not restore consciousness at 0 HP, cannot be healed, and does not stack.

For deterministic implementation define:

- `resolvedDamage` = damage remaining after saves, resistance, immunity, DR, and other actual mitigation.
- `tempAbsorbed` = `min(currentTempHP, resolvedDamage)`
- `postTempDamage` = `resolvedDamage - tempAbsorbed`

Reduce temporary HP first, then normal HP by `postTempDamage`.

`postTempDamage` is **not capped by current HP** for massive-damage, Wound-threshold, or excess-damage calculations.

### Half-max Wound threshold — NEW PROVISIONAL interpretation

Use **postTempDamage**, after temporary HP absorption.

A damage event meets the half-maximum Wound trigger when:

`2 × postTempDamage >= maximumHP`

Thus temporary HP genuinely protects against traumatic damage.

Example: max HP 40, 10 temp HP, resolved hit 25:

- temp absorbs 10;
- postTempDamage = 15;
- 15 is below half of 40;
- no half-max Wound trigger unless another trigger applies.

Maiming remains an independent Wound trigger even if temporary HP absorbs all normal damage.

---

# 4. Instant Death — recovered V6

Instant Death is checked **before any Wound save**.

### Creature above 0 HP

If damage reduces normal HP to 0, calculate:

`excessDamage = max(0, postTempDamage - HP_before_damage)`

If:

`excessDamage >= maximumHP`

the creature dies immediately.

### Creature already at 0 HP

If:

`postTempDamage >= maximumHP`

the creature dies immediately.

An instantly dead creature:

- makes no Wound save from that event;
- takes no death-save failures;
- cannot be stabilized or knocked out from that event.

Temporary HP therefore also protects against these thresholds by reducing `postTempDamage`.

---

# 5. Wound triggers and Wound save

Core V2 owns this procedure.

A living creature makes a Wound save when one or more of these occur from an event:

1. it drops from positive HP to 0 HP;
2. `postTempDamage` is at least half maximum HP;
3. the effect is explicitly **Maiming**.

### One-save rule — NEW PROVISIONAL

One damage/effect event produces **at most one Wound save**, even if it satisfies two or all three triggers.

### Wound DC

`DC = max(10, floor(postTempDamage / 2))`

If Maiming is the only trigger and `postTempDamage = 0`, DC is 10.

The save is Constitution.

Existing Wounds apply their Core penalty to this save.

### Original-Wound-count rule — NEW PROVISIONAL

Record `woundsBeforeSave` before rolling.

That number controls whether failure is fatal.

- If `woundsBeforeSave` is 0–2:
  - success: no Wound;
  - failure: gain one Wound;
  - failure by 5+: gain that one Wound and roll once on the provisional Injury table.
- If `woundsBeforeSave` is already 3:
  - success: remain Critically Wounded;
  - failure: **die immediately**.
  - Do not gain a fourth Wound.
  - Do not roll an Injury.

Therefore:

**2 Wounds → fail → 3 Wounds = Critically Wounded, not dead.**

Death occurs on a later failed Wound save that began with 3 Wounds.

No natural-1/20 special rule applies to Wound saves beyond the final numeric result.

---

# 6. Wound effects — Core V2

Each Wound gives:

- `-1` Constitution saves;
- `-1` to the maximum number of Hit Dice recoverable per long rest.

For implementation:

`maximum Hit Dice recovered = max(0, normal recovery maximum - Wound count)`

This arithmetic floor is an operational clarification of the Core penalty, not a new additional penalty.

At **3 Wounds**, the creature is **Critically Wounded**:

- Speed -10 feet;
- cannot regain full HP;
- dies on the next failed Wound save.

---

# 7. “Cannot regain full HP” — NEW PROVISIONAL closure

While Critically Wounded, healing cannot increase current HP above:

`criticalHealingCeiling = max(1, maximumHP - 1)`

This is a **healing ceiling**, not a reduction to the maximum-HP statistic.

Entering Critical does **not** immediately remove HP if the creature already happens to be at maximum HP. The restriction applies when HP would subsequently be regained.

### Maximum HP = 1

A creature whose maximum HP is 1 uses a Critical healing ceiling of **1**, not 0.

This is an explicit edge-case exception to avoid a permanent 0-HP recovery lock. The creature remains Critically Wounded despite being permitted to regain its sole HP.

Removing enough Wounds to fall below three immediately removes the Critical healing ceiling and Speed penalty.

---

# 8. Exact damage → Wound → death sequence

Implement every damaging event in this order:

1. **Resolve hit/save and raw damage.**
2. **Apply defenses**: relevant reductions, resistances, immunities, etc.
3. Record `resolvedDamage`.
4. **Remove temporary HP first.**
5. Calculate `postTempDamage`.
6. Record:
   - HP before damage;
   - Wounds before event;
   - whether target was already at 0 HP;
   - whether hit was critical;
   - whether effect is Maiming.
7. Apply `postTempDamage` to normal HP, flooring current HP at 0 while retaining excess mathematically.
8. **Check Instant Death.**
   - If dead, stop.
9. Determine whether this event triggers a Wound save.
10. If triggered, make **one** Wound save using the pre-save Wound count.
11. Resolve Wound failure / Critical death / Injury completely.
   - If dead, stop.
12. If the target was **already at 0 HP before the event** and `postTempDamage > 0`:
   - one death-save failure;
   - two instead if the damaging hit was a critical hit.
13. If the target newly reached 0 from positive HP:
   - do **not** add a death-save failure from the same damage packet.
14. Resolve knockout eligibility, ordinary dying, Stable state, or ordinary-monster death as applicable.
15. Apply any later consequences whose prerequisites still exist.

This ensures one event cannot accidentally generate duplicate Wounds.

---

# 9. Downed, Unconscious, Prone and death saves

Core V2's **Unconscious** condition already includes Incapacitated, unaware, dropping held items and falling Prone. Therefore Prone is **Core provenance**, not a Gameplay addition.

At 0 HP, a character using death saves is Unconscious and begins dying unless made Stable.

Death saves occur at the **start of each regular turn**.

They are:

`d20 with no modifier`

unless an explicit feature modifies death saves.

- 10+ = one success.
- 9 or lower = one failure.
- natural 20 = regain 1 HP.
- natural 1 = two failures.
- three successes = Stable.
- three failures = Dead.

Extra turns and extra Actions do not generate additional death saves.

---

# 10. Death-counter reset — recovered V6

Reset **both** death-success and death-failure counters when either:

- the creature regains positive HP; or
- the creature becomes Stable.

A natural-20 death save restoring 1 HP therefore also resets both counters.

---

# 11. Stable — recovered V6

A Stable creature:

- remains Unconscious;
- remains at 0 HP;
- makes no death saves.

When it becomes Stable, roll `1d4` once.

If it remains Stable and receives no other healing, it regains **1 HP after that many elapsed hours**.

When it regains that HP:

- it is no longer at 0;
- Unconscious from this cause ends;
- death counters are already cleared.

If a Stable creature suffers `postTempDamage > 0`:

1. resolve Instant Death;
2. resolve any Wound save;
3. if alive, it becomes unstable/dying again;
4. apply the normal damage-at-0 death-save failure(s);
5. resume start-of-turn death saves.

If temporary HP absorbs all resolved damage so that `postTempDamage = 0`, the creature remains Stable.

---

# 12. Stable recovery and rest clocks — NEW PROVISIONAL bookkeeping rule

Elapsed time is counted **once**.

If a Stable creature's `1d4`-hour recovery timer overlaps with a legal rest:

- the same elapsed hours advance both timers;
- do not add the stable-recovery hours on top of the rest duration.

Example:

A Stable character rolls 3 hours and simultaneously satisfies the conditions of an 8-hour rest.

- At elapsed hour 3, it regains 1 HP.
- Three hours have also elapsed toward the rest.
- Five additional qualifying hours remain for the 8-hour rest.

Whether Wound treatment or another activity is compatible with resting remains controlled by its own procedure.

---

# 13. Damage at 0 HP

Recovered V6/Core rules combine as follows:

If a creature already at 0 HP suffers `postTempDamage > 0`:

1. check Instant Death;
2. make a Wound save if half-max/Maiming or another Wound trigger applies;
3. if still alive:
   - one death-save failure;
   - two failures if the damaging hit was critical.

This is distinct from the attack that initially reduced the creature from positive HP to zero.

---

# 14. Knockout — recovered V6 plus sequencing overlay

A qualifying melee hit that reduces a creature to 0 may be designated as a **knockout**.

The declaration cannot bypass lethal rules.

Resolve:

1. damage;
2. Instant Death;
3. required Wound save;
4. fatal three-Wound failure if applicable.

Only if the target remains alive at 0 after those checks does the knockout convert its resulting 0-HP state to **Stable**.

Therefore:

- knockout cannot override Instant Death;
- knockout cannot override death caused by a failed Wound save while already at three Wounds;
- knockout does not suppress the Wound save caused by dropping to 0.

This is the correct interpretation of “stable instead of killing,” not a universal nonlethal exemption from trauma.

---

# 15. Ordinary monsters at 0 HP — recovered V6

- Most monsters die at 0 HP.
- Significant NPCs may use death saves at Director discretion.
- A valid melee knockout may leave a creature Stable, subject to the lethal checks above.

For implementation, creatures that do not use death saves require no dying-counter state.

---

# 16. Resurrection

Retain Core:

Resurrection restores life but does **not automatically remove**:

- Wounds;
- Corruption;
- debt;
- legal death;
- claims upon the recovered body.

Any resurrection spell or feature must separately define its body/soul/time requirements and what else it removes.

---

# 17. Wound treatment

The search establishes that the inspected approved sources reference Wounds and restoration effects but provide no general ordinary Wound-treatment procedure.

Therefore I would retain the Gameplay-derived treatment only as:

**NEW ACTIVE PROVISIONAL INTEGRATION — derived from retained Gameplay review evidence, not recovered Core V2 canon.**

Procedure:

- medical kit;
- 1 Supply;
- 8 elapsed hours;
- Medicine check against applicable tier DC.

Results:

- Critical Success: remove 2 Wounds.
- Success: remove 1 Wound.
- Failure: remove none; Supply is consumed.
- Critical Failure: remove none; Supply is consumed and suffer 1 Strain.

The broader supplies/rest audit can later confirm compatibility of the 8-hour treatment activity with Haven/rest procedures.

---

# 18. Injury table — NEW PROVISIONAL

Core requires an Injury-table roll on a Wound-save failure by 5+, but the table is absent from the inspected current sources.

Use this only until an authoritative historical table is found or the owner replaces it.

### Injury linkage

Every Injury is linked to the **single Wound gained from that same failure-by-5 Wound save**.

No Injury creates another Wound.

If a Wound is removed, its linked Injury immediately ends.

If an effect removes unspecified Wounds, the affected creature chooses which Wound records are removed unless that effect specifies otherwise.

If multiple Wounds have the same Injury result:

- record each linkage separately;
- the identical mechanical penalty applies only once;
- it ends only when no remaining Wound carries that Injury.

Numeric Injury penalties affecting the same roll/stat do not stack with one another; use the strongest Injury penalty.

### Provisional d6 Injury Table

| d6 | Injury | Exact effect |
|---:|---|---|
| **1** | **Concussion** | `-1` Initiative and Perception checks. |
| **2** | **Offensive Trauma** | `-1` attack rolls. |
| **3** | **Mobility Trauma** | All non-teleport Speeds are reduced by `5 ft.`, minimum 0. |
| **4** | **Fine-Motor Trauma** | `-1` tool checks and Dexterity checks whose primary task is manipulating an object, mechanism, lock or device. |
| **5** | **Exertion Trauma** | `-1` Strength and Dexterity ability checks. |
| **6** | **Cognitive Trauma** | `-1` Intelligence, Wisdom and Charisma ability checks. |

These penalties:

- do not remove Actions;
- do not create disadvantage;
- do not impose additional Wounds;
- do not reduce maximum HP;
- do not prevent healing;
- do not create new damage or resource triggers;
- do not become permanent if their linked Wound is removed.

If a creature cannot meaningfully suffer the fictional anatomy suggested by an Injury's name, retain the **mechanical result** and describe an equivalent trauma appropriate to that creature.

---

# 19. Critical Success treatment and linked Injuries — NEW PROVISIONAL bookkeeping

When treatment removes two Wounds:

- the Wound being treated is removed;
- the patient chooses the second Wound removed unless a feature states otherwise;
- each linked Injury ends with its Wound.

This makes the Injury linkage executable rather than leaving ambiguous which penalty disappears.

---

# 20. Required implementation invariants

I would put these directly into automated tests:

1. **Temp HP fully absorbs a half-max hit:** no half-max Wound trigger unless Maiming independently applies.
2. **One packet satisfies drop-to-zero + half-max + Maiming:** exactly one Wound save.
3. **Two Wounds, failed Wound save:** becomes three Wounds/Critical, not dead.
4. **Two Wounds, failure by 5+:** becomes three Wounds, rolls one Injury, remains alive.
5. **Three Wounds before save, failure:** dies; no fourth Wound and no Injury roll.
6. **Drop from positive HP to zero:** no same-packet death-save failure.
7. **Already zero, noncritical positive post-temp damage:** one death failure.
8. **Already zero, critical positive post-temp damage:** two death failures.
9. **Already zero, post-temp damage ≥ max HP:** Instant Death before Wound/death-failure processing.
10. **Positive HP hit with excess ≥ max HP:** Instant Death before Wound save.
11. **Stable + fully temp-absorbed damage:** remains Stable.
12. **Stable + positive post-temp damage:** becomes unstable after lethal/Wound checks and receives proper at-zero failure.
13. **Knockout + ordinary drop to zero:** Wound save still occurs before Stable.
14. **Knockout + Instant Death:** remains dead.
15. **Knockout + starting 3 Wounds + failed Wound save:** remains dead.
16. **Critical max HP 1:** may heal to 1 HP but remains Critical.
17. **Stable 1d4-hour recovery overlaps 8-hour legal rest:** elapsed time is not counted twice.
18. **Natural 20 death save:** 1 HP and both counters reset.
19. **Three successful death saves:** Stable and both counters reset.
20. **Temporary HP at 0:** does not restore consciousness.

With this overlay, the **core resolution / HP / Wound / death subsystem is mechanically implementable for adversarial review**. It should not yet be marked closed until Codex reviews the new post-temp Wound interpretation, Critical-HP edge rule, sequencing, treatment bookkeeping, and six-entry provisional Injury table.