Your correction is right: `4 × HP <= maxHP` means **25/100 qualifies; 26/100 and 30/100 do not**. Preserve that erratum against my earlier example.

## 1. `family.ongoing-fire` arbitration — **AGREE**

Use the same anti-namespacing principle as Bleed, but only for records explicitly classified as **creature-attached ongoing fire**.

I would freeze this **NEW provisional rule**:

> Every creature-attached Burn-style periodic-fire application has a source-qualified `mechanicalId`, a source `stackGroupId`, and the explicit family tag `family.ongoing-fire`.
>
> Records within one source stack group obey that source's printed cap, refresh, duration and instance rules.
>
> Different `family.ongoing-fire` groups may remain independently recorded on the same target for ownership, duration, cures and hooks.
>
> At an identical target timing marker, only **one ongoing-fire stack group deals periodic damage**. Choose the group with the highest expected unmitigated damage due at that marker, then the earliest application on a tie.
>
> The selected group's expressly permitted instances resolve according to that group's own cap. Other ongoing-fire groups due at that exact marker consume their scheduled tick without dealing damage; the tick is not postponed or banked.
>
> Records with genuinely different printed timing markers resolve independently.
>
> A record with replacement timing never also receives a generic Burning tick.

### Classification boundary

Membership must be explicit in the registry.

The family includes things such as:

- Dragoon Burn;
- Mage Fire Focus / Inferno Lance Burn;
- Ranger fire Burn;
- Shaman Burn riders;
- Tinker Burn Injector/fire-bomb Burn;
- other creature-attached periodic fire effects deliberately classified during binding.

It does **not** automatically include:

- ordinary fire damage;
- a direct fire hit;
- fire areas or zones;
- environmental flames;
- hazardous terrain;
- ignition of objects;
- a spell merely having the Fire damage type;
- Resonance Burn;
- a feature whose name happens to contain “Burn.”

An unnamed periodic fire rider can join only through an explicit registry classification. **Fire damage type alone is insufficient.**

### Mythic Carapace

This gives its wording a clean interface:

> Immunity to “Burn-style ongoing fire effects” blocks applications carrying `family.ongoing-fire`.

It does not grant fire-damage immunity or resistance to ordinary fire attacks, zones, hazards, or other fire damage unless another rule supplies that defense.

So yes: **global same-marker arbitration for explicitly registered creature-attached ongoing-fire groups** is the consistent solution.

---

## 2. Magical healing under Decay — **AGREE**

Keep three questions separate:

1. Was a **legal magical healing effect** actually used?
2. Did it have **positive healing potential** before HP caps or recovery prohibitions?
3. Did the target actually regain HP?

Generic Bleed curing depends on **1 and 2**, not 3.

Therefore:

> A legal magical-healing effect with positive potential can trigger an applicable Bleed ending procedure even when `oracle.decay` prevents the target from actually regaining HP.

Decay says the creature **cannot regain HP**. It does not nullify the casting/use of the healing effect and does not inherently block separately printed condition-removal consequences.

Examples:

- generic ordinary Bleed + legal 5-HP magical heal while Decayed → actual HP gained = 0, but generic Bleed ends;
- same at full HP → Bleed still ends;
- Corrupted halves a 1-HP heal to 0 → Bleed still ends;
- healing effect explicitly says “if the target regains HP, end Bleed” → that additional prerequisite would fail under Decay.

### Shaman Blood Curse

Its source-specific exception still controls:

> Magical healing does **not automatically end** `shaman.blood-curse.bleed`; it permits the printed immediate CON save to end it.

The save occurs even if Decay causes the healing effect to restore 0 HP, provided the healing effect was otherwise legal and had positive potential.

### Explicit condition removal

Also confirm:

> An effect explicitly saying it **ends/removes Bleed or another condition** continues to do so while the target has Decay unless that remover itself requires actual HP to be regained or the condition has a specific cure restriction.

Thus Decay blocks **HP recovery**, not:

- Medicine cures;
- explicit condition-removal spells;
- Shaman Blood Curse's healing-triggered save;
- cleanses;
- other separately printed non-HP consequences.

## Disposition

Both rules can be implemented:

- **`family.ongoing-fire` gets the same-marker family arbitration model, restricted to explicitly classified creature-attached periodic fire.**
- **Decay blocks HP gained, not legal healing-triggered or explicit condition-removal procedures unless those procedures expressly require actual HP recovery.**

No new blocker from these interfaces. Continue the remaining source-qualified bindings and cure/stack metadata before DD16's full registry review.