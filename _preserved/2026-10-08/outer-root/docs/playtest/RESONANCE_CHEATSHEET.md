# Resonance & Dissonance — Table Cheat Sheet

**Canon:** [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md)  
**Use:** quick player/Director reference

## Two limits, not one

| Resource | Meaning | What stops spam? |
|---|---|---|
| **Resonance Points (RP)** | How much magical power you still have available | You cannot pay for a spell you cannot afford |
| **Dissonance** | How badly you are forcing caster, spell, and Weave out of phase | Repetition and Overcasting push you toward a hard casting cutoff |

**Oracle does not use RP/Dissonance.** Oracle uses Mystery + Curse + Revelation Charges (RC). **Soldier and Warrior** have no general Weave pool.

## Shared spells, different lessons

A spell has a **Resonance Rank 0–9**. Rank determines its base magical cost; it is **not** a universal character-level requirement.

The same named spell can belong to several class traditions and be learned at different character levels. That is intentional. Each class has its own acquisition curve and may reach the same pattern earlier, later, or through a different school/rank placement.

Current catalog: **848 unique spells / 936 school-rank placements**. **619** spells currently have more than one class acquisition level.

## RP cost

```text
Base RP = Resonance Rank × 2
Rank 0 cantrip = 0 RP
```

Then apply only explicit class/item specialization, chosen Overcast RP costs, and the current Dissonance surcharge.

**Alignment and faction reputation never automatically make a spell cheaper or more expensive.**

## Dissonance gain

- Rank 0: **0 base**
- Rank 1–5: **+1**
- Rank 6–9: **+2**
- Each Overcast option: **+1**
- **Refrain:** immediately repeating the same named spell adds +1, then +2, then +3 maximum
- Repeated cantrips build Refrain even though they cost 0 RP
- Casting a different named spell breaks Refrain, but does not erase existing Dissonance

### Dissonance Limit

```text
2 + Proficiency Bonus + positive casting-ability modifier
minimum 4
```

| State | Threshold | Ranked-spell effect |
|---|---:|---|
| **In Tune** | below Limit | normal |
| **Frayed** | Limit | +1 RP |
| **Discordant** | Limit +3 | +2 RP; ordinary casters cannot Overcast |
| **Fractured** | Limit +6 | +3 RP; ordinary casters cannot cast Rank 1+ |

## Restore harmony

- **Let the Note Fall:** a turn without a spell/Weave ability removes 1 Dissonance.
- **Ground the Note:** spend your action without casting; remove Dissonance equal to proficiency bonus.
- **Retune:** short rest resets Dissonance to 0 and restores the class's normal short-rest RP.
- **Meditation:** optional rule; reduces Dissonance by PB + positive casting modifier and restores its listed RP.
- **Full Harmony:** long rest restores RP and resets Dissonance.

Dropping below **25% RP** is **Low Resonance**. It is a warning that your power reserve is low, not a separate penalty system.

## Overcast

Each selected option costs extra RP **and adds +1 Dissonance**.

| Option | +RP | Effect |
|---|---:|---|
| Extended | +1 | 2× duration |
| Subtle | +1 | no verbal/somatic components |
| Distant | +1 | 2× range |
| Empowered | +2 | +50% damage/healing |
| Widened | +3 | 2× area |
| Quickened | +3 | cast as bonus action |
| Twinned | +3 | second target |
| Heightened | +4 | +1 effective Rank/level as specified |

## Class rhythm matters

Every class keeps its own power engine. Examples:

- **Bard:** Crescendo rewards varied rhythm.
- **Mage:** Elemental Focus + Nuke Chains reward rotating elemental spells.
- **Wizard:** Spell Matrix rewards rotating prepared matrices.
- **Ranger:** weapon attacks between casts stabilize primal cadence.
- **Shaman:** Totems act as resonators.
- **Crimson Agent:** Blood Gauge can route limited strain through blood.

See [`CLASS_IDENTITY_CANON.md`](../mechanics/CLASS_IDENTITY_CANON.md) for all 17.

## Dark exception: Lich & Necromancer

Lich and Necromancer are explicit evil/transgressive paths. They may force ranked spells through **Fractured** Dissonance and may Overcast while Discordant/Fractured.

After the spell resolves they take **Traumatic Casting** backlash:

- Frayed: **1 × spell Rank**
- Discordant: **2 × spell Rank**
- Fractured: **3 × spell Rank**

Lich stays a **Mage** and keeps its Mage loop. Necromancer stays a **Wizard** and keeps Spell Matrix. Their dark-path feature lets them continue by accepting trauma; it does not replace the parent class mechanic.

## Multiclass RP

```text
max RP = full pool of highest caster-tier Weave class
       + ceil(25% of one secondary Weave caster's pool)
```

Tertiary+ Weave classes add no additional pool. Oracle/Soldier/Warrior do not contribute a Weave pool.
