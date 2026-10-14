# Advancement completion proposal

**New design proposal, not historical canon.** Prepared jointly with the Calibration Review notebook on 2026-10-08. The owner subsequently said, “I like your bard example.” Scheduled feature selections are therefore the working direction for the Bard pilot. The [full Bard draft](BARD_PLAYTEST_v0_1.md) now specifies all 50 abilities; numerical balance and adoption by other classes remain provisional.

## What the evidence establishes

The existing sources protect 17 class identities and use class level for class features. Total character level determines proficiency. No skill-point currency is implemented in the inspected class, feat or prestige registries. Existing Core Systems authority and the Oracle exception remain in force.

The [source matrix](../../../../docs/audit/2026-10-08/ADVANCEMENT_MATRIX.md) records 645 V7.2 path entries and 140 draft level features. Some explicit class tables themselves contain obsolete or conflicting material. A table must be reconciled with its protected class contract before being treated as the final acquisition schedule.

## Proposed general rule

When you gain a level in a class, use that class level to determine which features you acquire. Gain your class's core engine automatically. At a feature-selection milestone, choose previously unselected features from the permitted pool. A selection is not a stored point: it cannot be transferred to another class or banked to purchase a later tier.

Automatic engine grants include only the reconciled class engine, starting proficiencies, Hit Die, resource rules and explicitly automatic features. Merely listing an Arch or Hero ability does not grant it. A feature cannot be acquired twice through both a table and a choice. Do not stack old draft table grants on top of this proposal.

Normal selections exclude ASIs, feats, core engines, resource-capacity increases, and features expressly labelled Capstone, Finale or Final. Those use their own reconciled milestones. A name-only or mechanically incomplete ability remains blocked until its specification is completed; this proposal does not make vague text playable.

## Proposed schedule for ordinary Base → Arch → Hero classes

Applies provisionally to Bard, Cleric, Crimson Agent, Dragoon, Mage, Monk, Mirrorsage, Ranger, Shaman, Soldier, Thief, Tinker, Warrior and Wizard. Each class still needs its source-specific table reconciled. Druid, Oracle and Paladin use the exceptions below.

| Class level | Feature acquisition | Separate milestone |
|---:|---|---|
| 1 | Core engine; choose 4 Base features, at least 2 Active where applicable | Starting class kit |
| 2 | Choose 2 more Base features | |
| 3 | Arch unlock; choose 2 Arch features, at least 1 Active | |
| 4 | Choose 1 Base or Arch feature | ASI or eligible feat |
| 5 | Choose 1 Arch feature | |
| 6 | Choose 1 Base or Arch feature | |
| 7 | Choose 1 Arch feature | |
| 8 | Choose 1 Base or Arch feature | ASI or eligible feat |
| 9 | Choose 1 Arch feature | Reconciled Arch capstone |
| 10 | Choose one Hero path and 2 of its features, at least 1 Active | Hero path locked |
| 11 | Choose 1 Base or Arch feature | |
| 12 | Choose 1 Hero feature | ASI or eligible feat |
| 13 | Choose 1 Base or Arch feature | |
| 14 | Choose 1 Hero feature | |
| 15 | Choose 1 Base or Arch feature | |
| 16 | Choose 1 Hero feature | ASI or eligible feat |
| 17 | Choose 1 Base or Arch feature | |
| 18 | Choose 1 Hero feature | |
| 19 | Choose 1 Base or Arch feature | ASI or eligible feat |
| 20 | Gain the chosen Hero path's reconciled finale | |

All numbers and gates in this schedule are proposed for testing. Before a class uses it, verify that every choice has enough eligible, distinct entries and that every mandatory capstone exists. If a class has no such capstone, do not invent one implicitly. Build an explicit class exception. The same applies to missing active choices or exhausted pools.

## Proposed exceptions

**Druid:** use its bespoke table: Shapeshifting at L1; Circle at L2 with features at L2/6/10/14; Hero Forms at L10; Arch Druid Forms at L11; Timeless Body and Beast Spells at L18; Archdruid at L20. Its existing ASI levels are 4/8/12/16/19. Do not add ordinary Arch/Hero selections. Reconcile RP with Core Systems separately.

**Oracle:** retain Mystery and Curse at L1 and Revelation Charges, not RP. Preserve Tier I Revelation and Curse Boon I at L3, Boon II at L5, Tier II at L6, Tier III at L9, Boon III at L10, Mystic Insight at L12 and Revelation Mastery at L15. Complete the remaining class milestones from its own sources. Resolve the d6/d8 discrepancy explicitly before freezing a character sheet.

**Paladin:** follow its reconciled class and Oath milestones. Its current one-Arch/one-Hero data structure does not justify inventing three Hero choices. Entries with no recoverable acquisition level must be mapped individually.

**ASI/feat default:** where the reconciled class has no contrary explicit schedule, propose one ASI or eligible feat at class levels 4/8/12/16/19. Never award the same milestone again through feature selection or total character level.

**Multiclassing:** a Wizard 19/Bard 1 qualifies only for Bard L1 features. Selections belong to the class being advanced. Preserve the approved RP formula and Oracle exclusion. New class levels do not grant a second character-creation HP maximum.

**Retraining:** propose no general respec unless an explicit rule permits it. A future retraining system would be a separate design decision.

## Bard worked acquisition example

This acquisition example is implemented in the [Bard performance playtest module](BARD_PLAYTEST_v0_1.md), which provides operational cards, resource rules and table-test instructions. Follow that module for the exact new rules; it is not a completed general spellcasting or multiclass integration.

| Level | Example selection or grant |
|---:|---|
| 1 | Crescendo engine; Verse of Courage, Chant of Renewal, Dissonant Note, Echo of Inspiration |
| 2 | Verse Mastery, Lingering Notes |
| 3 | Virtuoso's Verse, Resonant Chant |
| 4 | Signature Sound; ASI/feat |
| 5 | Cascading Echo |
| 6 | Chorus Shield |
| 7 | Tempo Control |
| 8 | Verses Unbound; ASI/feat |
| 9 | Harmonic Convergence; automatic Perfect Pitch capstone |
| 10 | Harmony path: Healing Harmony, Protective Verse |
| 11 | Melodic Instinct |
| 12 | Chorus of Renewal; ASI/feat |
| 13 | Echo Harmonization |
| 14 | Inspiring Performance |
| 15 | Bardic Knowledge, classified as passive despite its old Active heading |
| 16 | Symphony of Serenity; ASI/feat |
| 17 | Fluid Tempo |
| 18 | Song of Serenity |
| 19 | Performance Focus; ASI/feat |
| 20 | Finale: Crescendo of Hope |

## Ability-completion contract

Every selectable ability needs a stable identifier with source mapping; class/path and acquisition level; automatic/selected status; active/passive/reaction classification; exact effect; action cost; range/targets/area; duration; resource cost and generation; attack/save formula; frequency/recharge; scaling; prerequisites; and interaction with the protected engine. Use explicit “not applicable” where appropriate rather than silently missing fields.

Preserve original text alongside new specifications. Label newly chosen mechanics as proposals and record playtest evidence. Spell names, storage slots, mutation slots and magical resources must not be normalized by indiscriminate word replacement.

The full game can be called campaign-playtest-ready only when every selectable option in its declared scope meets this contract and class progression, character sheets and Director procedures agree. AI calibration alone does not establish human balance.
