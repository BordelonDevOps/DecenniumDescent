# Resonance & Dissonance — Canon Magic Economy

**Status:** Canon — consolidated 2026-07-31  
**Player terms:** Resonance, Resonance Points (RP), Resonance Rank, Dissonance, Refrain, Retune, Ground the Note  
**Core principle:** RP limits how much magical power a caster has available. Dissonance limits how recklessly or repetitively that power can be forced through the Weave.

## 1. Metaphysical rule

Aethel and the Weave are resonant structures. Life, death, memory, motion, elemental force, prayer, blood, and thought all carry pattern. Spellcasting is the act of sounding one of those patterns strongly enough that the Weave reproduces it.

Magic therefore has two simultaneous limits:

1. **Resonance Points** — remaining power and endurance.
2. **Dissonance** — accumulated phase strain between caster, spell, and Weave.

A caster can still have RP and nevertheless be too dissonant to cast safely. This is intentional and prevents a caster from solving every encounter by repeating one efficient spell until the pool is empty.

## 2. Resonance Rank and spell overlap

Every named spell has a **Resonance Rank (0–9)**. Rank is the spell pattern's complexity/cost basis, not a universal character-level gate.

Each class has three independent pieces of spell access:

- **School/thread access** — which magical traditions the class can learn.
- **Effective Resonance Rank** — which school/rank placement that class uses when a spell appears in more than one school.
- **Class acquisition level** — the character level at which that class can learn that Rank.

This intentionally uses a class-driven spell-learning model: the same named spell may be shared by several classes while arriving at different character levels. The spell is stored once; its class access is not.

Current catalog contract:

- **936 school/rank placements**
- **848 unique named spells**
- **619 spells currently have more than one class acquisition level**
- **14 general Weave-casting base classes**
- **Oracle:** Revelation Charges, not RP
- **Soldier / Warrior:** no general Weave spell list

See `SPELL_CATALOG_CANON.md`, `class_spell_school_mapping.csv`, and `class_spell_progression.csv`.

## 3. RP pools

All fourteen general Weave-casting base classes have an L1–20 pool curve in `src/data/resonance-economy.js`.

Full casters use the largest pools. Half, hybrid, and minor Weave users have smaller pools because their class-specific engine carries part of their power budget.

The RP pool never replaces a class's unique mechanic.

## 4. Base RP cost

```text
Base RP cost = Resonance Rank × 2
```

Rank 0 cantrips cost **0 RP**.

Only explicit **class or item text** may modify this cost, plus the universal Dissonance surcharge and chosen Overcast options. Moral alignment and faction reputation are never automatic cost modifiers.

## 5. Dissonance

### Dissonance Limit

```text
Dissonance Limit = 2 + Proficiency Bonus + positive casting-ability modifier
minimum 4
```

### Dissonance gained per cast

- Rank 0: **0 base Dissonance**
- Rank 1–5: **+1 base Dissonance**
- Rank 6–9: **+2 base Dissonance**
- Every selected Overcast modification: **+1 Dissonance**
- Casting outside a class feature's explicitly permitted key/thread, when a feature says so: **+1 Dissonance**

### Refrain

Immediate repetition of the same named spell adds additional Dissonance:

- first cast: no Refrain penalty
- first immediate repeat: +1
- second immediate repeat: +2
- third and later immediate repeats: +3 maximum

This applies to cantrips. A cantrip is free in RP, not free in phase strain.

Casting a different named spell breaks Refrain, but does not erase accumulated Dissonance.

## 6. Dissonance states

| State | Threshold | Effect |
|---|---:|---|
| **In Tune** | Below Limit | Normal casting |
| **Frayed** | Limit | +1 RP to ranked spells |
| **Discordant** | Limit +3 | +2 RP; ordinary casters cannot Overcast |
| **Fractured** | Limit +6 | +3 RP; ordinary casters cannot cast Rank 1+ spells |

Fracture is the hard anti-spam cutoff for ordinary Weave casters.

## 7. Restoring harmony

- **Let the Note Fall:** a turn with no spell or Weave ability removes 1 Dissonance.
- **Ground the Note:** spend the action without casting; remove Dissonance equal to Proficiency Bonus.
- **Retune (short rest):** reset Dissonance to 0 and restore the class's short-rest RP amount.
- **Meditation:** optional 10-minute, once/day recovery; reduces Dissonance by PB + positive casting modifier and restores its listed RP amount.
- **Long rest:** restores RP to maximum and Dissonance to 0.

## 8. Class cadence is protected

Resonance is a universal law, not a replacement class mechanic.

| Class | Protected mechanic | Resonance interaction |
|---|---|---|
| Bard | Crescendo | Complete/consume rhythm to vent strain; repeating one spell is not rhythm |
| Cleric | Conviction | Rites/Invocations alter cadence and can vent limited strain |
| Crimson Agent | Blood Gauge / Blood Marks | Routes some strain through blood by spending Gauge |
| Dragoon | Momentum | Movement carries the note and reduces limited Dissonance |
| Druid | Shapeshifting | Changing form changes the body sounding the Weave and clears Refrain |
| Mage | Elemental Focus / Nuke Chains / Resonance Surge | Different elemental spells form chains; completing a chain vents strain |
| Monk | Ki Flow / Stances | Ki can stabilize minor Weave techniques without becoming RP |
| Mirrorsage | Echo Slots / Mirrorbind | First replay of a new Echo is protected; repetition still builds Refrain |
| Oracle | Mystery / Curse / Revelation Charges | No RP or Weave Dissonance; RC + Prophecy Triggers are its anti-spam system |
| Ranger | Track Target / Weapon Synergy | Weapon hits between casts break cadence and stabilize the next spell |
| Shaman | Totems / Elemental Attunement | Totems function as resonators that reduce limited Dissonance |
| Soldier | Palisade / Overwatch | No general Weave casting |
| Thief | Sneak Attack / Poison | Hidden delivery stabilizes limited minor Weave tricks |
| Tinker | Drone / Deployables | Devices may absorb limited Dissonance and then disable |
| Warrior | Mutations / Serum / Brutality | No general Weave casting |
| Wizard | Spell Matrix | Rotating prepared matrices is inherently stable; repetition builds Refrain |
| Paladin | Oath / Smite / Aura / Lay on Hands | Oath powers are not ordinary spell spam; martial cadence stabilizes Oath spells |

The authoritative software contract is `src/data/class-core-mechanics.js`.

## 9. Dark-path exception — Lich and Necromancer

**Lich** and **Necromancer** are intentionally evil exceptions to safe Weave practice.

They do not gain a moral discount. They gain the willingness and technique to **force magic through damage that would stop another caster**.

### Traumatic Casting

A Lich or Necromancer may:

- cast Rank 1+ spells while Fractured;
- Overcast while Discordant or Fractured.

After the spell resolves, the caster takes direct magical trauma based on the resulting Dissonance state:

| State | Backlash |
|---|---:|
| Frayed | 1 × spell Rank |
| Discordant | 2 × spell Rank |
| Fractured | 3 × spell Rank |

Minimum backlash is 1. This is direct metaphysical trauma and is not reduced by ordinary damage resistance.

### Lich — Soul Furnace

Lich remains a **Mage**. Elemental Focus, Nuke Chains, and Resonance Surge remain part of the play loop.

- Soul Reservoir converts death/DoT pressure into Resonance recovery.
- Once per rest, Soul Reservoir can absorb one Traumatic Casting backlash.
- Lich does not "harmonize" Dissonance; it burns souls and selfhood to continue through it.

### Necromancer — Grave Conductor

Necromancer remains a **Wizard**. Spell Matrix preparation and rotation remain part of the play loop.

- Once per round, destroy one controlled undead or consume a fresh corpse within 30 ft to absorb one Traumatic Casting backlash.
- The spell still generates its full Dissonance.
- The corpse/minion is functioning as a disposable resonator, not as free RP.

No other alignment, class, school, or path ignores the Fractured cutoff unless an explicit future rule says so.

## 10. Overcasting and Low Resonance

Overcasting increases effect by paying additional RP **and** additional Dissonance. Current options remain Empowered, Extended, Widened, Heightened, Quickened, Subtle, Distant, and Twinned.

Dropping below **25% of maximum RP** is called **Low Resonance**. It is an informational resource warning, not a second strain subsystem and not an automatic penalty. Dissonance is the universal rule that governs repetitive and reckless casting.

This distinction matters: a caster can have 1 RP and remain perfectly In Tune, or have a nearly full RP pool and still be Fractured from forcing the same pattern again and again.

## 11. Reputation

Reputation changes access to teachers, sanctuaries, focuses, libraries, components, recipes, political protection, and faction-specific training. It does **not** change the intrinsic Resonance Rank of a spell, its base RP cost, a caster's natural RP capacity, or Dissonance merely because a faction likes or hates the caster.

A faction reward can still provide a concrete named benefit—such as a temporary focus, a specialized lesson, or a sanctuary effect—but that benefit must be written explicitly as an item, feature, scene reward, or training benefit.

## 12. Multiclass Resonance

When a hero has multiple Weave-casting classes:

```text
max RP = full pool of highest caster-tier class
       + ceil(25% of one secondary Weave caster's pool)
```

Tertiary+ Weave classes add no further pool. Oracle, Soldier, and Warrior do not add a Weave pool.

## 13. Source hierarchy

1. `RESONANCE_CANON.md`
2. Player Rulebook Resonance chapter
3. `src/data/class-core-mechanics.js`
4. `src/data/resonance-economy.js`
5. `SPELL_CATALOG_CANON.md` + class mapping/progression CSVs
6. Companion UI

If an older document refers to mana, universal spell slots, or alignment-based school discounts, this canon supersedes it.
