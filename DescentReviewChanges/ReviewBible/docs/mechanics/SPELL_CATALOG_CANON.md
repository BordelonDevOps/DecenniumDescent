# Spell Catalog Canon

This file documents the authoritative spell-data contract used by the Player Rulebook and companion app.

- **School placements:** 936
- **Unique spells:** 848
- **Multi-school or multi-level names:** 74
- **Resonance Ranks:** 0–9
- **General Weave casters:** 14 of 17 base classes
- **Acquisition model:** class-specific learning levels; one spell can arrive at different character levels for different classes
- **Oracle:** Revelation Charges only; no general Weave spellbook
- **Soldier / Warrior:** no general Weave spellbook

## Class school access and acquisition

- **Bard:** hybrid Weave; max Rank 7; Enchantment, Illusion, Universal; R0@L1, R1@L1, R2@L4, R3@L7, R4@L10, R5@L13, R6@L16, R7@L19
- **Cleric:** full Weave; max Rank 9; Abjuration, Divination, Necromancy, Universal; R0@L1, R1@L1, R2@L3, R3@L5, R4@L7, R5@L9, R6@L11, R7@L13, R8@L15, R9@L17
- **Crimson Agent:** hybrid Weave; max Rank 6; Enchantment, Evocation, Illusion, Necromancy; R0@L1, R1@L2, R2@L5, R3@L8, R4@L11, R5@L15, R6@L19
- **Dragoon:** minor Weave; max Rank 4; Conjuration, Evocation, Transmutation; R0@L3, R1@L3, R2@L8, R3@L13, R4@L18
- **Druid:** full Weave; max Rank 9; Abjuration, Conjuration, Necromancy, Transmutation; R0@L1, R1@L1, R2@L3, R3@L5, R4@L7, R5@L9, R6@L11, R7@L13, R8@L15, R9@L17
- **Mage:** full Weave; max Rank 9; Abjuration, Conjuration, Evocation, Transmutation, Universal; R0@L1, R1@L1, R2@L3, R3@L5, R4@L7, R5@L9, R6@L11, R7@L13, R8@L15, R9@L17
- **Monk:** minor Weave; max Rank 4; Abjuration, Illusion, Transmutation; R0@L1, R1@L3, R2@L8, R3@L13, R4@L18
- **Mirrorsage:** hybrid Weave; max Rank 7; Divination, Enchantment, Illusion, Universal; R0@L1, R1@L1, R2@L4, R3@L7, R4@L10, R5@L13, R6@L16, R7@L19
- **Oracle:** Revelation Caster — Mystery/Curse/Revelation Charges; no general Weave ranks
- **Ranger:** half Weave; max Rank 5; Conjuration, Divination, Transmutation; R0@L1, R1@L2, R2@L5, R3@L9, R4@L13, R5@L17
- **Shaman:** hybrid Weave; max Rank 7; Conjuration, Divination, Necromancy, Transmutation; R0@L1, R1@L1, R2@L4, R3@L7, R4@L10, R5@L13, R6@L16, R7@L19
- **Soldier:** No general Weave spell access
- **Thief:** minor Weave; max Rank 4; Enchantment, Illusion, Necromancy, Transmutation; R0@L1, R1@L3, R2@L8, R3@L13, R4@L18
- **Tinker:** minor Weave; max Rank 5; Abjuration, Conjuration, Transmutation, Universal; R0@L1, R1@L2, R2@L6, R3@L10, R4@L14, R5@L18
- **Warrior:** No general Weave spell access
- **Wizard:** full Weave; max Rank 9; Abjuration, Conjuration, Divination, Enchantment, Evocation, Illusion, Necromancy, Transmutation, Universal; R0@L1, R1@L1, R2@L3, R3@L5, R4@L7, R5@L9, R6@L11, R7@L13, R8@L15, R9@L17
- **Paladin:** half Weave; max Rank 5; Abjuration, Divination, Enchantment, Universal; R0@L2, R1@L2, R2@L5, R3@L9, R4@L13, R5@L17

## Overlap and acquisition rule

A named spell may appear in more than one school and at more than one Resonance Rank. The catalog stores that spell once while preserving every school/rank placement. For a given class, the lowest eligible placement determines the spell's **Resonance Rank and thread** for that class. The class's own acquisition curve then determines the **character level at which that class can learn it**. This intentionally allows the same spell to be learned by different classes at different character levels, in the tradition of class-driven MMORPG spell lists, without cloning the spell into separate records.

This separation is deliberate: **Resonance Rank is not character level**. A shared spell can be early training for one class and advanced training for another.

## Dissonance contract

Spell access is governed by Resonance Rank and class learning level; repeated casting is governed separately by Dissonance. Rank 1–5 spells generate 1 base Dissonance, Rank 6–9 generate 2, and immediate repetition builds Refrain (+1/+2/+3). Cantrips cost 0 RP but repeated cantrips still build Refrain. Ordinary casters stop ranked casting at Fractured Dissonance; Lich and Necromancer are the explicit Traumatic Casting exceptions defined in `RESONANCE_CANON.md`.

## Metadata status

The current Player Rulebook gives concise rules summaries for all 936 placements but does not specify a complete casting-time/range/components/duration block for every unique spell. The companion therefore labels those four fields as `Not specified in current rulebook` rather than importing incompatible legacy-system metadata. This is deliberate; no missing mechanical field is silently invented.
