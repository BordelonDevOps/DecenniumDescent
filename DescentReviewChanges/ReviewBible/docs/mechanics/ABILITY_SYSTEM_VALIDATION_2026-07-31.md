# Class & Ability Validation — 2026-07-31

**Result: PASS**

- Canon selectable base classes: **17 / 17**
- Protected unique-mechanic contracts: **17 / 17**
- Class path datasets present: **17 / 17**
- Feats in structured catalog: **334**
- Paladin Sacred Oaths: **10**
- Oracle Mysteries: **10**
- Oracle Curses: **10**
- Lich parent identity: **Mage — preserved**
- Necromancer parent identity: **Wizard — preserved**
- Lich/Necromancer Traumatic Casting exception: **protected**
- Druid Shapeshifting uses/CR progression: **book ↔ structured data synchronized**

## Path-data coverage

| Class | Protected mechanic | Arch paths | Hero paths | Arch path abilities* | Hero path abilities* |
|---|---|---:|---:|---:|---:|
| Bard | Crescendo | 1 | 3 | 10 | 30 |
| Cleric | Divine Favor / Conviction | 1 | 3 | 12 | 30 |
| Crimson Agent | Blood Mark | 1 | 3 | 12 | 30 |
| Dragoon | Momentum Gauge | 1 | 3 | 12 | 30 |
| Druid | Shapeshifting | 7 | 1 | 44 | 7 |
| Mage | Elemental Focus / Nuke Chains | 1 | 3 | 11 | 28 |
| Monk | Ki Flow | 1 | 3 | 16 | 27 |
| Mirrorsage | Echo Slots / Mirrorbind | 1 | 3 | 11 | 27 |
| Oracle | Mystery, Curse & Revelations | 1 | 1 | 11 | 6 |
| Ranger | Track Target | 1 | 3 | 11 | 27 |
| Shaman | Totem System | 1 | 3 | 10 | 27 |
| Soldier | Palisade / Overwatch | 1 | 3 | 11 | 27 |
| Thief | Sneak Attack / Poison | 1 | 3 | 10 | 27 |
| Tinker | Anacite Drone / Deployables | 1 | 3 | 10 | 27 |
| Warrior | Mutation Slots | 1 | 3 | 12 | 30 |
| Wizard | Spell Matrix System | 1 | 3 | 12 | 32 |
| Paladin | The Oath | 1 | 1 | 8 | 10 |

\*Counts are the passives + actives stored in `class-paths.js`; class base features, level-milestone features, feats, Oaths, Mysteries/Curses, Druid forms, and prestige features are stored in their dedicated modules and are not double-counted here.

## Invariant

Balance may change numbers. It may not flatten the class loop. Resonance/Dissonance is a universal magical law layered **around** the class engine, not a replacement for Crescendo, Conviction, Blood Gauge, Momentum, Shapeshifting, Nuke Chains, Ki, Echo Slots, RC, Track Target, Totems, Palisades, Sneak Attack/Poison, Deployables, Mutations, Spell Matrix, or the Paladin Oath.
