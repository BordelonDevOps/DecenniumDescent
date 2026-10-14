# Decennium Descent — Continuity Glossary

**Purpose:** Approved terms and mechanical labels for all agents and collaborators.  
**Authority:** `rulebook_output.txt` (Classes Table, Oracle chapter, Ch Weave/Resonance) → `canon-classes.js` → this file.  
**When in doubt:** Do not invent. Add an entry under **ASK OWNER** in [`CONTINUITY_REPORT.md`](./CONTINUITY_REPORT.md).

---

## Cosmology & setting (Aethel)

| Term | Approved usage | Avoid |
|------|----------------|-------|
| **Aethel** | The fractured world; product tone and lore namespace. | Real-world MMO names, SWTOR branding, Forgotten Realms deities. |
| **Great Stillness** | Pre-creation state before the First Song (cosmology Ch I). | Treating as a faction or location without author sign-off. |
| **First Song** | Primordial act of resonance that broke the Stillness; source of creation echo. | "First Song" as a spell name unless rulebook defines one. |
| **Choir** | Divine/spiritual chorus medium — breath, voice, distance; linked to Echo Court lore. | Generic "choir" without cosmology context in patron text. |
| **Echo Court** | Ancestral spirit chorus; patron of **Mystery of Ancestor** (Oracle). | Foreign pantheon courts (e.g. Fey courts from other IPs). |
| **Turning Spiral** | Keepers of causality at the edge of the First Song's echo; patron of **Mystery of Time**. | Confusing with **Iron Spiral** (dungeon tier 9 zone) without context. |
| **Hush Beneath the Song** | Silence where even the Choir's echo fades; patron of **Mystery of Shadow**; ties to tier-10 silence lore. | |
| **Tenfold Truths / Tenfold Cycles** | Mythic age and 10-year Shardspire calendar rotation. | "Tenfold" as arbitrary number without cycle context. |
| **Shardspire** | Activates in the tenth year; mortals enter the Great Descent; cycles named after victors. | |
| **Calan'thir** | Architect of the Spiral; melodic weaver who partnered at the First Seal. Attuned to **The Voice**. In Umbrin exile lore (`draft: true`), he and the **First Choir** banished Umbrin forebears from ordered light — see [`docs/mechanics/UMBRIN_LORE.md`](../../docs/mechanics/UMBRIN_LORE.md). | Calling him a generic "light deity" without Spiral/cosmology context; FR deity names. |
| **Lumina** | Primordial radiant counterpart to **Umbra** at creation; ordered light and song (`rulebook_output.txt`). Calan'thir's Spiral calibration and Choir orthodoxy align with bounded Lumina — not a generic "good god" label in player copy. | Conflating Lumina with surface kingdom names (e.g. Luminalis) without context; FR light-deity names. |
| **Umbra** | Primordial abyssal depth paired with **Lumina** at creation; source of the Obsidian Thread (`rulebook_output.txt`). **Umbrin** (the people) derive their demonym from Umbra; Murk cults worship a **perverse** reading — not Choir orthodoxy. Never use "Umbra" as shorthand for Umbrin PCs. | "Dark elves", Drow, Lolth; conflating primordial Umbra with the Umbrin people. |
| **First Choir** | Divine chorus of the Spiral age; language **Celestial**. Shunned and exiled the Umbrin (`draft: true` — **Obsidian Burn**). Distinct from generic Oracle **Choir** patron copy unless context ties to Calan'thir. | Generic "choir" when only describing Echo Court or music groups. |
| **The Murk** | Subterranean realm beneath Aethel; home of the Umbrin, Deep Dwarves, and other denizens. Product term for underworld cavern networks — not "Underdark". | "Underdark" (FR setting name). |
| **Murkish** | Spoken language of The Murk (Umbrin, Deep Dwarves, etc.). | "Undercommon" in player-facing race data. |
| **Umbrin** | Playable race and bestiary humanoid line (was D&D "Drow" in ingest; interim label "Umbral Elf" superseded 2026-07-29 PM). Obsidian-skinned elves exiled by Calan'thir and the First Choir; worship a perverse Umbra; traits **Umbrin Magic**, **Umbrin Weapon Training**. Noble subrace **Obsidian Highborn**. Save id `umbrin` (legacy `drow`, `umbral-elf`, `Drow`, `Umbral Elf` migrated on load). Plural: Umbrin; adj.: Umbrin. Lore: [`docs/mechanics/UMBRIN_LORE.md`](../../docs/mechanics/UMBRIN_LORE.md). | "Drow", "Dark Elf", "Dark elves", "Umbral Elf", Lolth, Underdark as product names. |
| **Obsidian Burn** | `draft: true` — mythic banishment in which Calan'thir and the **First Choir** drove Umbrin forebears from the light; flesh cooled to obsidian sheen. Product metaphor for Umbrin skin tone and Murk exile. | Lolth curses; FR Underdark origin myths; using as a spell name without rulebook definition. |
| **Umbra cult (Murk)** | `draft: true` — heretical Murk faith venerating a twisted reading of primordial **Umbra** (Obsidian Thread, abyssal liberation). Opposed by **Cleansing Orders** and mainstream faith; odd bedfellows with **Dark Cults** / **Underworld** when interests align. | Lolth, spider-goddess FR pantheon; wholesome Choir-Umbra syncretism. |
| **Strange alliances (Umbrin)** | Reputation note: Umbrin are broadly distrusted (civic, mainstream faith) yet Murk expediency yields **very strange alliances** — **Underworld**, **Planar Trading Guilds**, **Corruption Scholars**, **Anti-Cult Alliances** (shared targets), etc. No hard race lock in `reputation.js`; apply via background and story. | Hard-coding all Umbrin as Hated with every faction; "dark elf" stereotype IP. |
| **Great Descent** | 100-floor dungeon structure; tier 10 ends at Silencebound Void. | "Descent" alone when meaning the dungeon (capitalize in product copy). |
| **Binding of the Old God** | Eleventh shard imprisoned at Level 97; pantheon forbade contact. | |
| **Weave of Aethel** | Metaphysical tapestry of magic; eight schools; accessed differently per class. | "Weave" for Oracle **Revelation Charges** (see Oracle section). |

---

## Magic systems

| Term | Approved usage | Avoid |
|------|----------------|-------|
| **Weave** (noun) | Arcane/divine/primal/hybrid spellcasting via **Resonance Points** and spell lists. UI tab label "Weave" = spell browser for Weave casters. | Applying Weave slot language to Oracle. |
| **Resonance** / **Resonance Points (RP)** | **CANON (Director choice, Hybrid-B, 2026-07-29):** single fungible RP pool for **Weave casters** (Wizard, Mage, Cleric, Druid, etc.); cost = spell level × 2, modified by school affinity/opposition, reputation, and specialization. L1 table: Wizard 4, Mage/Cleric/Druid 3. Musical/Choir/First Song flavor lives in the *prose*, not the system name — "Resonance" is the only player-facing name; "Hybrid-B" is an internal ruling label only. See [`docs/mechanics/RESONANCE_CANON.md`](../../docs/mechanics/RESONANCE_CANON.md), helpers in `resonance-economy.js`. | Using RP for Oracle (Oracle uses Revelation Charges); calling the system "Song of the Weave" in player-facing copy. |
| **Multiclass Resonance** | **CANON:** When a hero has two or more Weave-casting classes, max RP = **full pool of the highest caster-tier class** + **⌈25% of one secondary Weave caster's pool⌉** (round up); Arcane Guilds reputation applies once to the merged total. Tertiary+ Weave classes add no further RP. This is written into the rulebook; a merged result is marked draft only when a contributing class pool table is separately still draft. Oracle uses Revelation Charges (RC), never RP. Formula: [`RESONANCE_CANON.md` §7](../../docs/mechanics/RESONANCE_CANON.md). | "Hybrid-B" in UI; treating Oracle/Soldier/Warrior secondary as Weave pools; inventing new merge math. |
| **Revelation Charges** | Oracle-only pool (initially **3**, maximum **7**); powers **Mystery Revelations**, not Weave spells. Abbreviation **RC** OK in Session UI and collaborator docs. | "Spell slots", "RP", or "Weave charges" for Oracle. |
| **Mystery Revelations** | Oracle abilities tied to chosen Mystery; Tier I (1 charge), Tier II (2), Tier III (3). | Generic "spells" in Oracle UI without Mystery context. |
| **Prophecy Trigger** | Per-Mystery rule to recover Revelation Charges thematically. | |
| **Oracle's Curse** | L1 chosen curse with limitations + **Curse Boons** at L3, 6, 9, 12, 15, 20. | |
| **Curse Boon** | Benefit gained despite curse; levels shared across all curses. | |
| **Revelation Caster** | Product label for Oracle spellcasting mode in Builder (`spell-utils.js` excludes Oracle from `isSpellcasterClass()`). | |
| **Reputation** | Per-faction standing in Aethel (Hated → Honored). Save field `reputation` — `{ [factionId]: score }`, scores −3…+3. Background applies starting scores via `reputation.js`. Resonance model is now canon (Hybrid-B); RP modifiers from Academic/Religious/Arcane/Nature standing are **in-scope to implement next**, but **not yet auto-applied** to RP. | Confusing Reputation with Resonance Points (RP); auto-applying RP bonuses before the reputation→RP wiring lands. |

---

## Classes (17 canon base)

**Source of truth:** `canon-classes.js` (`CANON_CLASSES`). Product has **17 selectable base classes**. Rulebook prose "eighteen" is a **book typo** — do not add an 18th without owner decision.

| # | Class | Notes |
|---|-------|-------|
| 1 | Bard | Hybrid Weave caster |
| 2 | Cleric | Divine Weave caster |
| 3 | Crimson Agent | Hybrid Weave |
| 4 | Dragoon | Martial |
| 5 | Druid | Primal Weave; 7 circles |
| 6 | Mage | Arcane Weave |
| 7 | Monk | Martial |
| 8 | Mirrorsage | Arcane hybrid |
| 9 | Oracle | **Revelation Caster** (not Weave RP) |
| 10 | Paladin | 10 Sacred Oaths at L3 |
| 11 | Ranger | Primal hybrid |
| 12 | Shaman | Primal caster |
| 13 | Soldier | Martial |
| 14 | Thief | Martial / hybrid paths |
| 15 | Tinker | Martial support |
| 16 | Warrior | Martial |
| 17 | Wizard | Arcane Weave |

**Not selectable (reference only):**

- **Fighter** — full rulebook chapter, absent from Classes Table; prestige reqs map to Warrior in `prestige.js`.
- **Swashbuckler** — orphan entry in `class-details.js` only; never expose in picker.

---

## Oracle (10 mysteries, 10 curses)

**Mysteries (ids → names):** `ancestor`, `battle`, `bones`, `cataclysm`, `dream`, `flame`, `life`, `shadow`, `stars`, `time`

| Rulebook-complete / Director-promoted | Aethel draft (`draft: true` in data) |
|---------------------------------------|--------------------------------------|
| **Ancestor** (rulebook full tree); **Shadow** (Director-promoted 2026-07-30, `draft: false`) | Battle, Bones, Cataclysm, Dream, Flame, Life, Stars, Time |

**Curses:** `spiral-touched` is rulebook-complete (**Spiral-Touched**). Nine others are playable Aethel drafts.

**Patron names (approved in `oracle-mysteries.js`):** Echo Court, War Chorus, Pale Ledger, Shattered Seal, Veiled Threshold, Crown of First Flame, Verdant Resonance, Hush Beneath the Song, Celestial Concord, Turning Spiral.

Do **not** rewrite mystery trees wholesale; flag `draft: true` and link to rulebook gap tickets.

---

## Paladin & Druid

| Term | Approved usage |
|------|----------------|
| **Sacred Oath** | Chosen L3; save field `sacredOath` (id). **Grief** Director-promoted (`draft: false`, 2026-07-30). **Mercy** has rulebook prose but remains **`draft: true`** in companion until author promotes; 8 other oaths draft. |
| **Revelation spells** (Paladin) | Oath-granted spell list — distinct from Oracle Revelations. |
| **Druid Circle** | One of 7: Land, Moon, Storm, Thorns, Winterfang, Rotshaper, Ashen Grove. Save field `druidCircle` (id). |
| **Wild Shape / hero forms** | `druid-shapeshifting.js`; keyed by circle id. |

---

## Prestige ↔ feats

- Prestige paths live in `prestige-lorebook.json` / `prestige.js`.
- Feat names in prestige **requirements** must exist in `feats.js` (automated gate: 0 missing).
- **Fighter** in prestige text → maps to **Warrior** for eligibility only.
- **Bloodbound** (prestige #4): base classes **Crimson Agent or Thief (Lv 10+)** only — **Director/owner decided 2026-07-29**; Gravetouched is **not** a Bloodbound prerequisite (Gravetouched is prestige #10, separate path).
- Prestige **capstone** prose may say "spell slot" — correct for Weave casters; not for Oracle.

---

## Character save fields

Normalized in `character-storage.js` → `normalizeCharacter()`:

| Field | Type | Purpose |
|-------|------|---------|
| `class` | string | Base class from `CANON_CLASSES` |
| `archClass` | string | Arch / hero path label if set |
| `sacredOath` | string (id) | Paladin oath |
| `druidCircle` | string (id) | Druid circle |
| `oracleMystery` | string (id) | Oracle mystery |
| `oracleCurse` | string (id) | Oracle curse |
| `resonancePoints` | number | Weave RP pool tracker (default **3** on load) |
| `secondaryClass` | string | Optional multiclass — second Weave/martial class name (Builder dropdown) |
| `secondaryLevel` | number | Level in `secondaryClass` (1–20); omitted when no secondary |
| `classLevels` | object | Optional advanced save: `{ Wizard: 10, Cleric: 6 }` — overrides secondary dropdown for RP merge |
| `reputation` | object | Faction standing map `{ [factionId]: score }` — see `reputation.js`; scores −3…+3 |
| `knownSpells` / `preparedSpells` | string[] | Weave casters only; Oracle uses Mystery UI |
| `feats` | string[] | Feat names as in `feats.js` |

**Display rule:** Resolve ids to human names via `getOathById`, `DRUID_CIRCLES`, `getMysteryById`, `getCurseById` — never show raw ids in player-facing notes if avoidable.

---

## Dungeon tiers (gate bosses)

| Tier | Boss | Zone |
|------|------|------|
| 1 | Vaskor, the Stone Maw | Yieldheart Caverns |
| 2 | The Bloom That Hungers | Bloomdeep Marsh |
| 3 | Ashthirst the Hollow | Anvil of Brogi |
| 4 | Gor Vekk, Architect of Ends | Isles of Eternal Radiance |
| 5 | Choralith, Voice Below | Sanctum of Echoing Choirs |
| 6 | Lumen of the Shattered Thread | Crossroads of the Shattered Thread |
| 7 | Xarog, the Pactbound Furnace | Pactbound Arena |
| 8 | Eirfax, the Dusk Crowned | Duskshard Pools |
| 9 | Threxus, the Iron Spiral | Veiled Iron Spiral |
| 10 | The Marquis of Silence | Silencebound Void |

Tier 10 aligns with **Hush / silence** cosmology (Oracle Shadow patron, Echo Court silence themes).

---

## Draft & product boundaries

| Label | Meaning |
|-------|---------|
| `draft: true` | Playable Aethel content pending author promotion; show "(draft)" in UI. |
| **Aethel draft** | Original companion content, not imported rulebook text. |
| **Rulebook canon** | Verbatim or structured from `rulebook_output.txt` / docx. |
| **Private reference** | Ripped MMO assets on disk — never product path (see strategy rule). |

---

## Quick agent checklist

Before adding copy or mechanics:

1. Class in `CANON_CLASSES`?
2. Oracle → Revelation Charges, not Weave/RP?
3. Weave caster → RP table, not Revelation Charges?
4. Cosmology term from this glossary or rulebook?
5. Prestige feat names in `feats.js`?
6. Save fields match table above?
7. Unresolved lore → **ASK OWNER**, not invented prose.
8. Race term **Umbrin** only — never "Umbral Elf" as current product copy (legacy alias migrates on load).
9. Multiclass Weave → show **Draft** badge; use `resolveMaxRp()` merge; never print "Hybrid-B" in UI.

*Last verified: Wave 58 Resonance multiclass clarity pass, 2026-07-30.*

---

## Session tracker persistence (wave 67)

These fields belong to a Session combatant in local storage key `dd_session_tracker`. They are table-state fields, not new Character Builder save requirements; the Session normalizer safely defaults or limits them when older Session data loads.

| Field | Type | Approved behavior |
|-------|------|-------------------|
| `activeTotemIds` | string[] | Shaman table-presence tracker. Valid options are `spirit`, `echo`, `divining`, and `blight`; L6+ permits one active totem, and L13+ permits two under the existing **draft** milestone. Values persist through reload; Long Rest clears them. This records placement only — effects, duration, targeting, damage, and Totem Pulse remain GM-resolved. |
| `attunedArchFormIds` | string[] | Druid L15+ **draft** arch-form attunements, capped at two ids. Shift+clicking an arch form in Session toggles an attunement; the ids persist until changed by the table. |
| `archAttunementSwapUsed` | boolean | Tracks the one free swap between attuned arch forms per encounter. Short Rest and Long Rest reset this flag; they do not erase `attunedArchFormIds`. |
| `alignment` | string | Session **Ethos** row value: one of the nine `PLAYER_ALIGNMENTS` strings (LG through CE). It supports the live overcast school-affinity hint; it is not a new morality subsystem or a second Resonance pool. |
| `burnoutCastHint` | string | Transient post-cast Overcast/Burnout reminder (Mage L17 draft condition or low-RP check). It is not an automated consequence or condition. Clear it through Overcast **Clear**, **Short Rest**, **Long Rest**, or direct **Full** Resonance restore. |

### Library empty-state convention

Items, Spells, and Monsters libraries should show an actionable no-results explanation when the current search, filters, or temporary view yields zero entries. **Clear all filters** resets only discovery controls (including the Spells Learned/Favorites view); it does not erase learned spells, favorites, item data, or Session state.

*Wave 67 continuity addendum — 2026-07-30.*
