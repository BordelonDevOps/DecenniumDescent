# Reference Monster Manual Benchmark (structure / size / completeness only)

**Role:** Agent 1 of 5 — reference benchmark for a Decennium Descent Monster Manual that *feels* as large and complete as industry MM/Bestiary products.  
**Date:** 2026-08-04  
**Strict rule:** Compare **scope, chapter patterns, entry fields, and completeness bar only**. Do **not** copy WotC, Paizo, or other third-party monster prose, art descriptions, proprietary lore, or verbatim SRD dumps of specific creatures into DD materials. All DD text, mechanics, and presentation remain original.

**Reference tree inspected:** [EllatharTheHalfling/DnD-Books `5e/Books`](https://github.com/EllatharTheHalfling/DnD-Books/tree/master/5e/Books) (GitHub API listing). Tree contents are **PDFs only** — no markdown/HTML TOCs or extractable sample entries in-repo. Structural signals below come from that **filename inventory** plus **public secondary sources** (Wikipedia, published reviews, PathfinderWiki, WotC’s free Volo’s **Contents** PDF). Pirate PDF bodies were **not** used as source material for this brief.

---

## 1. What was in the reference `5e/Books` tree

### Primary Monster Manual–like books (filename signals)

| File (as listed) | Role for benchmarking |
| --- | --- |
| `D&D 5E - Monster Manual.pdf` | Core A–Z bestiary product |
| `D&D 5E - Volo's Guide to Monsters.pdf` | Lore-heavy supplement + bestiary + NPC/beast appendices |
| `D&D 5E - Mordenkainen's Tome of Foes.pdf` | Faction/planar lore + bestiary + monster lists |

### Adjacent books (creatures exist, but not “the MM”)

Useful for knowing what a full line *also* ships, not as the primary size target:

- Setting books with bestiary chapters (e.g. Eberron, Ravnica in this tree)
- Rules expansions with sparse monsters (Tasha’s, Xanathar’s)
- Small packages (e.g. Tortle Package)
- Core PHB / DMG (not monster manuals)

**Readable TOC sample (structure only):** WotC’s free [Volo’s Guide Contents PDF](https://media.wizards.com/2016/dnd/downloads/Volos_TOC.pdf) shows the industry “expanded MM” pattern without requiring the full book:

1. **Monster Lore** — deep family chapters (behavior, society, variants, lair maps)
2. **Optional player-facing material** (playable lineages — *skip or replace for DD unless product wants it*)
3. **Bestiary** — alphabetical new/variant entries
4. **App. A Assorted Beasts** · **App. B Nonplayer Characters** · **App. C Monster Lists**
5. **Index of monster stat blocks** + **lair map** plate list

Pathfinder 2e **Bestiary** (public product description / wiki): ~360 pages, **400+** creatures, **Monsters A–Z** then appendix (ability glossary, trait list, rituals/languages as needed, creatures by type, creatures by level).

---

## 2. Typical book scope signals (size & chapter patterns)

Ranges are **approximate public figures** for “feels like a real hardcover MM,” not a mandate to clone page counts.

| Product class | Approx. pages | Creature / block scale | Chapter pattern |
| --- | --- | --- | --- |
| **Core MM / Bestiary** | ~300–360 | **~300–400+** named entries; **~400–500+** usable blocks if age/rank variants count separately | Intro (how to read / types) → **A–Z main body** → appendices (mundane beasts, stock NPCs, lookup lists) |
| **Lore+bestiary supplement** (Volo-like) | ~200–230 | **~100–130** new/variant blocks + stock NPCs/beasts | **Deep lore families** (often ~⅓–½ of book) → optional PC options → A–Z bestiary → Apps A–C + lair maps |
| **Faction/planar foe tome** (Mordenkainen-like) | ~250 | **~140** new monsters (public marketing figure) | Faction/cosmology essays → bestiary → **monster lists** appendix |
| **PF2 Bestiary-class** | ~360 | **400+** | Intro → A–Z → **rules glossary + taxonomy indices** |

### Appendix types that signal “complete book,” not pamphlet

Industry MM-class books almost always ship **lookup infrastructure**:

- Creatures by **difficulty band** (CR / level / DD tier equivalent)
- Creatures by **type / taxonomy**
- Creatures by **environment / floor / zone** (where the game cares)
- Optional: **beast** appendix, **stock NPC** appendix, **ability glossary** (shared keywords), **lair map** plates, **stat-block index**

### DD implication (scope target, not clone)

A Decennium Descent Monster Manual that “feels like a real MM” should aim at:

- **Core volume:** on the order of **300–400+ fully authored entries** (or fewer entries with rich family variants that still yield **400+** table-ready blocks), **plus** appendices.
- **Not enough alone:** a searchable companion JSON of ~700 sandbox rows without published lore/tactics/lairs — that is a **stat toolkit**, not an MM product.
- Existing DD pipeline note (context only): companion/bestiary coverage is already **broad**; the gap vs this bar is **authored completeness and book presentation**, not raw row count.

---

## 3. Generic RPG monster-entry field checklist

Use as a **DD authorship checklist**. Field names should map to **DD mechanics** (Horn, tiers, floors, Resonance, etc.). Do **not** paste foreign SRD blocks.

### A. Identity & cataloguing

- [ ] Unique **name** (DD-original)
- [ ] **Size / category / tags** (DD taxonomy — type, subtype, rarity, draft/canon flag)
- [ ] **Tier / floor band / difficulty** (DD equivalent of CR/level)
- [ ] **Alignment or disposition model** (only if DD uses one)
- [ ] One-line **role** (skirmisher, controller, boss, swarm, social threat, etc.)

### B. Presentation shell (book feel)

- [ ] Short **flavor hook** (1–3 sentences, original)
- [ ] **Appearance** note (original; no third-party art prose)
- [ ] **Ecology / habitat** (where it lives in Aethel / dungeon / surface)
- [ ] **Society / behavior** (if intelligent or pack-structured)
- [ ] **Treasure / harvest / crafting hooks** (DD-relevant; link Crafting Bible where appropriate)

### C. Core combat block

- [ ] Defenses (AC / equivalent, HP or wound model, saves)
- [ ] Speeds / movement modes
- [ ] Ability scores or DD attribute frame
- [ ] Skills / trained checks that matter at the table
- [ ] Senses + communication
- [ ] Resistances / immunities / vulnerabilities / condition interactions
- [ ] Proficiency / attack math consistent with DD rules
- [ ] **Traits** (always-on)
- [ ] **Actions** (attacks, multiattack-equivalent, specials)
- [ ] **Bonus / reaction / free** options if the system uses them
- [ ] Spellcasting or power lists **only when earned** (not empty stubs)

### D. Escalation & encounter design (separates MM from pamphlet)

- [ ] **Tactics** paragraph (what it opens with, focuses, flees, combo partners)
- [ ] **Legendary / mythic / boss** extras when appropriate (DD naming)
- [ ] **Lair** features / regional effects / terrain tricks when the creature “owns” a site
- [ ] **Variants** (age, rank, corrupted, pack roles, elite) with clear delta from base
- [ ] **Encounter seeds** (1–3 hooks: why the party meets it)
- [ ] **XP / reward / Horn-clock** guidance only if DD awards it that way

### E. Cross-links (product glue)

- [ ] Pointers to **floor / zone / Gate / cosmology** entries
- [ ] Related creatures (family, summons, thralls)
- [ ] Companion ingest fields (id, tags, provenance) kept in sync with book text

### Depth tiers (practical authorship)

| Tier | What it is | When to use |
| --- | --- | --- |
| **Pamphlet** | Name + numbers + 1–2 attacks | Fillers, beasts, one-shot mooks |
| **Standard MM entry** | Pamphlet + ecology + tactics + 1 variant or encounter seed | Most A–Z entries |
| **Signature / family chapter** | Multi-page lore + lair + multiple variants + maps/diagrams | Gate Guardians, iconic Aethel lineages, tier bosses |

---

## 4. Completeness bar — “real MM” vs “stat-block pamphlet”

### Pamphlet (fails the bar)

- Dense tables or JSON with little prose
- No ecology, tactics, or lair guidance
- No appendices / indices for Directors to find monsters by need
- Variants absent or “reskin HP only”
- Inconsistent math and missing senses/languages/traits
- Feels like a **data export**, not a **Director-facing book**

### “Feels like a real Monster Manual” (pass bar)

1. **Hardcover-scale roster:** hundreds of **authored** creatures (or rich families totaling hundreds of blocks), not dozens of fully written entries surrounded by empty shells.
2. **Every standard entry** has identity + combat block + short lore + **tactics** (minimum Standard MM tier above).
3. **Signature creatures / families** get multi-section treatment (behavior, hierarchy, lair, variants) — not only a bigger HP number.
4. **Intro chapter** teaches how to read DD monster blocks, creature roles, and how difficulty maps to Opening / Horn / tiers.
5. **Appendices** exist: at least **by difficulty**, **by type**, **by environment/floor**; strongly preferred: beasts/stock NPCs or DD equivalents, ability glossary, stat-block index.
6. **Lair / site tools** for apex threats (maps optional; rules text mandatory).
7. **Presentation consistency:** same field order, typography, and callout grammar across the book (and companion).
8. **Provenance clean:** no third-party IP names, lore, or art descriptions; draft/sandbox rows are either upgraded or excluded from the published MM.
9. **Director usability:** a GM can build a night’s encounters from indices alone without opening the companion first.
10. **Companion parity:** published book entries dual-write / ingest cleanly; book is not a dump of untrusted sandbox combat.

### Stretch (supplement-class excellence)

- Dedicated **monster-lore chapters** for 6–12 major DD lineages (Volo-pattern depth, DD-original content)
- Lair map plates or diagrammatic strongholds
- Stock adversary templates (guards, cultists, expedition NPCs) as an appendix

---

## 5. Handoff for other agents (use this bar)

**Do:** size and completeness comparable to MM / Volo / Mordenkainen / PF Bestiary **products**.  
**Do not:** copy their prose, creatures, lore, or art text.

Suggested split for Agents 2–5:

- **Corpus plan:** target entry counts + which DD creatures are Signature vs Standard vs Pamphlet
- **Entry template:** DD field schema matching §3 (book + JSON)
- **Chapter/appendix outline:** Intro → families or A–Z → Apps (lists, glossary, harvest crosswalk)
- **Gap audit:** companion `bestiary_data_full` vs publication bar (authored lore/tactics/lair, not row count alone)

---

## 6. Sources used (non-proprietary structure)

- GitHub API listing: `EllatharTheHalfling/DnD-Books` → `5e/Books` (filenames / presence only)
- WotC free Contents PDF for Volo’s Guide (chapter/appendix **pattern** only)
- Public encyclopedia/review figures for page and creature **counts**
- PathfinderWiki / PF2 public rules intros for Bestiary **appendix pattern** and “400+ / ~360 pages” scope signal
- DD internal context: `BESTIARY_PUBLICATION_STATUS.md`, Book Lineup BE-01 *Bestiary of Aethel* (development scaffold ≠ finished MM)

*End of benchmark. No third-party monster text reproduced.*
