# Resonance — table cheat sheet

**System:** Resonance / Resonance Points (RP) · **Canon:** Hybrid-B ([`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md))  
**Print:** one page · **Companion:** SessionTracker Retune / Full / overcast stub

---

## Myth-bust: RP pool ≠ spell slots

| 5e habit | Resonance (canon) |
|---|---|
| Separate slots per spell level (1st, 2nd, 3rd…) | **One fungible pool** — spend any amount on any prepared spell |
| Cast = expend **one slot** of tier ≥ spell level | Cast = pay **RP cost** (see formula); cantrips **0 RP** |
| Short rest rarely restores slots (subclass exceptions) | **Retune** ≈ ¼ max pool + casting mod (+ Nature rep) — partial, not full |
| Long rest = all slots back | **Full harmony** = pool to max |
| No overcast menu | **Overcast** surcharges stack on base cost; **Burnout** risk below 25% max |

> **Not player-facing:** "Hybrid-B" is an internal doc/code label only.

---

## Max pool

| Class tier | Classes | L1–20 table |
|---|---|---|
| **Canon** | Wizard, Mage, Cleric, Druid | Rulebook-complete |
| **Draft** | Bard, Paladin, Ranger, Shaman, Mirrorsage, Crimson Agent, Dragoon, Monk, Thief, Tinker | Cleric curve × tier multiplier *(draft badge in UI)* |
| **No RP pool** | **Oracle**, **Soldier**, **Warrior** | Oracle → **Revelation Charges (RC)**; martials → class features only |

**Arcane Guilds rep → max RP:** liked/disliked ±1 · honored/hated ±2 (applied once to merged total).

**L3 canon pools:** Cleric **7** · Mage **8** · Wizard **10** · Druid **7**

---

## Cast cost

```
Cost = (spell level × 2)
     − 1  if school is in-key with your alignment (affinity)
     + 1  if school is dissonant (opposition)
     ± 1  class-relevant faction rep (liked −1, disliked +1)
     − 0…3 specialization (subclass — draft, not wired)
→ floor at 0
```

| Modifier | Track (by class) | Effect |
|---|---|---|
| Max RP | Arcane Guilds | ±1..±2 |
| Spell cost | Religious (Cleric/Paladin/Shaman/Monk/Dragoon) · Academic (Bard/Mirrorsage/Thief) · Arcane (Mage/Wizard/Tinker/Crimson Agent) · Nature (Druid/Ranger) | ±1 |
| Retune bonus | Nature Circles | ±1 RP on short rest |

**Affinity uses moral axis only** (Good / Neutral / Evil): e.g. Good affinity = Abjuration, Divination, Transmutation; opposition = Necromancy, Enchantment.

---

## Recovery

| Rest | Name | Recovery | Table note |
|---|---|---|---|
| **Short** | **Retune** | `round(max÷4)` + **casting ability mod** + Nature Circles rep | Free during short rest *(playtest default)* |
| **Long** | **Full harmony** | Restore to max RP | Dungeon horn clock +8 h per long rest when tracked |
| **Meditation** *(optional)* | — | Casting mod only, 10 min, 1/day | Not wired in companion |

---

## Overcast *(stack surcharges on base cost)*

| Option | +RP | Effect |
|---|---|---|
| Extended | +1 | 2× duration |
| Subtle | +1 | No V/S components |
| Distant | +1 | 2× range |
| Empowered | +2 | +50% dmg/healing |
| Widened | +3 | 2× AoE |
| Quickened | +3 | Bonus action cast |
| Twinned | +3 | Second target |
| Heightened | +4 | +1 effective spell level |

**Total cast** = base cost + sum of chosen overcast options.

### Burnout *(draft stub — badge only)*

- **Risk line:** current RP **< 25% of max** after a cast (`ceil(max × 0.25)`).
- **Companion:** SessionTracker shows **Burnout** badge; **no auto-penalties** wired yet.
- **Draft table effect:** disadvantage on Weave checks; −1 action this turn *(GM adjudicates)*.
- **Mage L17+ high-tier overcast:** concentration save DC 15 + tier *(draft hint only)*.

---

## Multiclass *(approved canon)*

**Max RP** = full pool of **highest caster-tier** Weave class + **⌈25% × one secondary Weave pool⌉**; tertiary+ Weave classes add **0**; Arcane Guilds rep applies **once**.

*Example:* Wizard 10 / Cleric 6 → Wizard L10 pool + ⌈25% × Cleric L6 pool⌉.

---

## Oracle — separate track

| | Weave casters | Oracle |
|---|---|---|
| Resource | **RP** | **Revelation Charges (RC)** — start 3, max 7 |
| Spend on | Prepared Weave spells | **Mystery Revelations** (1/2/3 RC by tier) |
| Recovery | Retune / full harmony | Each Mystery's **Prophecy Trigger** — *not* rest-based |
| Ch9 "Fate Weaving" | — | **Non-canon** — ignore |

Session may grant RC +1 on short rest as **companion convenience**; canon recovery is trigger-based.

---

## L3 quick examples

### Cleric 3 · max **7 RP** · burnout line **2 RP** · Religious Orders spell-cost rep

| Action | Math | Pool after (from full) |
|---|---|---|
| *Sacred Flame* (cantrip) | 0 | 7 |
| *Cure Wounds* L1, in-key Transmutation | 2 − 1 = **1** | 6 |
| *Spiritual Weapon* L2, no affinity | **4** | 2 *(at burnout line)* |
| **Retune** (WIS +2, neutral Nature) | round(7÷4) + 2 = **4** | 6 |

### Mage 3 · max **8 RP** · burnout line **2 RP** · Arcane Guilds spell-cost rep

| Action | Math | Pool after (from full) |
|---|---|---|
| *Shield* L1 Abjuration, Good affinity | 2 − 1 = **1** | 7 |
| *Scorching Ray* L2 Evocation, Neutral opposition | 4 + 1 = **5** | 2 *(burnout risk)* |
| *Fireball* L3 | **6** | need 6+ RP free |
| **Retune** (INT +3) | round(8÷4) + 3 = **5** | — |

### Overcast example (Mage 3, 5 RP left, *Magic Missile* L1 = 2 RP)

Empowered (+2) + Quickened (+3) → **7 RP total** → drops to **−2** without enough pool *(table: can't pay)*; if paid from 8/8 → **1 RP left** → **Burnout badge** (1 < 2).

---

## Companion buttons

| Button | Does |
|---|---|
| **Retune** | +retune amount (cap at max) |
| **Full** | Set current = max RP |
| **Overcast row** | Toggle options; apply spend + Burnout flag |

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Playtest docs — Resonance cheat sheet |
| **Date** | 2026-07-30 |
| **Scope** | `docs/playtest/RESONANCE_CHEATSHEET.md` + `RESONANCE_CHEATSHEET_PRINT.txt` |
| **Sources** | `RESONANCE_CANON.md` · `resonance-economy.js` · `CONTINUITY_GLOSSARY.md` · expedition playtest defaults |
| **Draft flags** | 10 non-core RP tables · Burnout consequences · specialization discount · meditation UI |
| **Open** | Owner ratifies Burnout table effects; promote draft pool tables |
