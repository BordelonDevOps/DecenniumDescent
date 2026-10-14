# Codex of the Heartcell

## BB-01 — Monster Ecology, Gate Seals, and Creature Lexicon

*A Director's bestiary for Decennium Descent. Companion volume to the Player Rulebook and The Director's Crucible. 100% original Aethel material — no foreign tabletop product names appear in this book.*

**Book code:** BB-01
**Editable stats source:** `Bestiary.xlsx` (Monsters sheet) → re-ingested into `src/bestiary_data_full.json`. Edit the workbook, re-run the ingest, regenerate this Codex — never hand-edit stat numbers only in this file.

---

## What this book is

The *Codex of the Heartcell* is built the way an old-school bestiary is built: ecology first, statistics second. Before any Director opens a stat block, they should know what the creature *wants*, where it *lives*, and what it *costs* an Expedition to meet — win or lose. That is the order this book follows, chapter by chapter:

1. **Reading the Codex** — how a Decennium stat line works, and how to read the honesty flags this book uses constantly.
2. **The Ten Gate Seals** — full set-piece chapters for the Gate Guardians that end each tier of the Decennium, in descending order from Floor 10 to Floor 100.
3. **Ecologies and Lexicon of Aethel** — one ecology essay per creature family, immediately followed by every indexed creature of that family, sorted by Challenge Rating.
4. **Floor Cultures** — deeper looks at the living peoples of the Decennium's upper and middle floors, for Directors who want politics instead of pure combat.
5. **The Director's Toolkit** — quick monster creation, lair omens, tier-by-tier random pressure tables, and a short appendix of conditions.
6. **Numeric Challenge Index** — every indexed creature, sorted by Challenge Rating, for fast encounter-budget lookups.

## Draft-stat honesty (read this before you run anything from this book)

The Heartcell's bestiary was seeded from a portable spreadsheet generator before any Director had time to hand-tune every entry. That generator is honest about its own limits, and so is this book. Every lexicon entry below carries one of three provenance tags:

| Tag | What it means | What a Director should do |
|---|---|---|
| **Companion-authored draft** | A person wrote this creature's tactics and numbers on purpose (the ten Gate Guardians, mostly). Still draft, but intentional. | Run as written, adjust to taste. |
| **Excel-sandbox draft** | Numbers came from an automatic Challenge-Rating band generator. Attack names like *Tail Lash*, *Monstrous Claw*, *Freak Bite*, and *Aberrant Lash* are placeholders reused across hundreds of unrelated creatures. | Reflavor the attack name at the table for free. Treat the numbers as a fair starting budget, not gospel. |
| **STUB — Director must re-skin** | The Size/Type/CR combination is nonsensical (a Tiny Undead named after a sky-faring people, for instance), the name is a stock stand-in flagged for an Aethel rename, or the sheet's own `NeedsReview` column caught a size/HP inflation problem. | Do not run this showcase-ready. Reskin the name, correct the Size/Type, or swap in a nearby entry that already makes sense before spotlighting it. |

None of this is embarrassment — it is the difference between a bestiary that lies about being finished and one that tells a Director exactly how much trust to extend to each line. **A draft stat block run honestly at the table is better than a "finished" one that quietly breaks the fiction.**

This Codex does not touch `Bestiary.xlsx` directly. Every rename, stub flag, and correction proposed here is a **recommendation for the next Excel pass**, not a silent edit — see the Naming & IP Reskin Ledger in the Director's Toolkit for the full proposed rename list awaiting owner sign-off.

---

# Part I — Reading the Codex

## How to read a Decennium stat line

Every lexicon entry uses the same seven-field shape:

| Field | Meaning | Director note |
|---|---|---|
| **Size / Type / Alignment** | Fiction tags describing the creature's frame and disposition | Distrust nonsense combinations on sight — see STUB flags |
| **Challenge (XP)** | Encounter-budget aid, not a promise of balance | Draft XP awards should be treated as a starting point for the table, not a contract |
| **Zone** | Where the Excel ingest currently places this creature | A biome/region tag, independent of which tier or floor a party is actually descending through |
| **Armor / Hit Points / Speed** | The combat shell | Pulled directly from the sheet; flagged if the sheet itself flagged it |
| **Attacks** | Name, bonus, and damage | Prefer the sheet's bespoke names; generic sandbox names are called out explicitly |
| **Defenses** | Resistances, immunities, condition immunities | Only populated for companion-authored entries; sandbox entries default to none |
| **Provenance** | Which of the three honesty tags above applies | Announce draft status at the table when it matters |

## Gate Seal & legendary framing (Director rules)

The ten Gate Guardians are not random bosses — they are **seals**. Each one holds a division of the Decennium shut, and defeating one is a Cycle-defining event for the Expedition that manages it, not a Tuesday-night boss fight. Use these house rules to run them:

1. **One seal per division.** Do not reuse a Gate Guardian's stat block as a "harder version" of anything else. If the story needs two, that is a Director decision worth flagging at session zero.
2. **Telegraph before you fight.** A seal should be foreshadowed for a full in-fiction period — omens, lesser encounters, rumors from floor cultures, a research clue that only makes sense in hindsight — before the party ever rolls initiative against it.
3. **Seal Pulses, not foreign jargon.** When a Guardian needs a legendary-feeling turn between player turns, call it a **Seal Pulse**: a terrain effect, an environmental tell escalating, or a single free reaction tied to the room itself. This is Decennium Descent's own framing — do not import "legendary actions" language from other products at the table.
4. **The Canticle soft-quit line is morale, not the Horn.** Floor 50 (Choralith's seal) is where the overwhelming majority of Expeditions choose to turn back — that is a *fiction and morale* pressure point, separate from the Horn's point-of-no-return clock. Do not conflate the two when staging a session.
5. **Victory is bait, not closure.** Every seal's reward should visibly reopen new problems on the surface — see each chapter's "Reward as Bait" section. A Gate Guardian's death should never be the end of a story thread; it should be the opening of three more.
6. **Defeat costs hours and morale, not automatically the party.** Unless your table has explicitly opted into deadlier stakes, a failed seal attempt should cost Opening-calendar time and standing, not a default TPK.
