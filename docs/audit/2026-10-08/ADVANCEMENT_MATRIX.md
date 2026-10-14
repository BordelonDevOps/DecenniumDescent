# Structured advancement extraction

Source comparison: main and preserved V7.2, 2026-10-08. This is an audit, not new rules. Full verbatim fields, every class level and source SHA-256 values are in [advancement_matrix.json](advancement_matrix.json). Temporary import adapters were used only in the audit workspace; source modules were not changed.

Both branches still use many plain strings rather than operational ability records. Path-level active/passive entries have no canonical ability IDs or explicit acquisition, action, resource-cost and cooldown fields. The no-colon count is a text-format signal, not proof of a missing description; entries with colons can still lack playable details. Automatic-vs-selected acquisition cannot be inferred from presence in an array.

## V7.2 coverage

| Class | Runtime HD | Protected engine | Arch/Hero paths | Path entries | No-colon entries | Draft level features | Levels with no feature entry |
|---|---|---|---:|---:|---:|---:|---|
| Bard | d8 | Crescendo | 1/3 | 40 | 15 | 10 | 7, 9 |
| Cleric | d8 | Divine Favor / Conviction | 1/3 | 42 | 20 | 10 | 7, 9 |
| Crimson Agent | d8 | Blood Mark | 1/3 | 42 | 15 | 8 | 9, 13, 15, 17 |
| Dragoon | d10 | Momentum Gauge | 1/3 | 42 | 20 | 10 | 7, 9 |
| Druid | d8 | Shapeshifting | 7/1 | 51 | 17 | 4 | 7, 9 |
| Mage | d6 | Elemental Focus / Nuke Chains | 1/3 | 39 | 20 | 11 | 9 |
| Monk | d8 | Ki Flow | 1/3 | 43 | 20 | 10 | 7, 9 |
| Mirrorsage | d6 | Echo Slots / Mirrorbind | 1/3 | 38 | 20 | 10 | 7, 9 |
| Oracle | d8 | Mystery, Curse & Revelations | 1/1 | 17 | 6 | 6 | 7 |
| Ranger | d10 | Track Target | 1/3 | 38 | 20 | 10 | 7 |
| Shaman | d8 | Totem System | 1/3 | 37 | 20 | 9 | 7, 15 |
| Soldier | d10 | Palisade / Overwatch | 1/3 | 38 | 20 | 9 | 7, 15 |
| Thief | d8 | Sneak Attack / Poison | 1/3 | 37 | 20 | 8 | 7 |
| Tinker | d8 | Anacite Drone / Deployables | 1/3 | 37 | 20 | 10 | 7 |
| Warrior | d12 | Mutation Slots | 1/3 | 42 | 20 | 6 | 7 |
| Wizard | d6 | Spell Matrix System | 1/3 | 44 | 20 | 5 | none |
| Paladin | d10 | The Oath | 1/1 | 18 | 3 | 4 | 9 |

Empty levels may legitimately have resource or spell progression elsewhere. They are not automatically defects. Draft features remain author-review drafts even when runtime merges them into a level table. V7.2 validation currently checks identity and presence, not complete operational ability definitions.

## Findings

- Runtime Bard still contains Crescendo die/Bard College/Font of Inspiration level features, while the protected engine and book describe a five-stack rhythm system.
- Druid runtime grants Shapeshifting at L2 while the book and uses function grant it at L1.
- Oracle runtime HD is d8; the detailed book entry says d6 while its overview says d8.
- Slot-era draft wording survives in V7.2 as well as main. Do not assume lab promotion alone repairs it.
- A universal skill-point economy is not implemented in these modules. See exact point/respec search hits in the JSON.
- Arch and Hero entries include names or qualitative effects without complete mechanical fields. They need deliberate design completion, not only document cleanup.

## Scope

The matrix includes all 17 class-level tables and path lists, core contracts, hit dice, feat counts and point/respec references in related structured modules. Druid forms, Oracle Mysteries/Curses, Paladin Oaths, spell progression and prestige text remain separate source modules and must be consulted when completing individual abilities.
