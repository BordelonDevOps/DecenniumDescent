# Bestiary Inventory for Monster Manual

**Date:** 2026-08-04  
**Agent:** 2 of 5 (Bestiary Inventory)  
**Authority:** ReviewBible wins on drift (`DescentReviewChanges/ReviewBible/`)  
**Do not invent creatures** — this inventory only catalogs existing sources.

---

## Executive summary

| Metric | Value |
|--------|------:|
| **Unique creatures (authoritative live set)** | **707** |
| Excel `Monsters` named rows (ReviewBible `Bestiary.xlsx`) | 708 (708 unique strings) |
| Excel↔JSON name mismatches | 26 Excel-only / 25 JSON-only |
| Excel scrub-corrupt `Fracture-Kin`×4 rows (not extra creatures) | 25 |
| Intentionally hidden from live JSON | 1 — `Ul’nath, the Hollow Dream` |
| Duplicate names in live JSON | **0** |
| Gate Guardians (trusted) | 10 |
| Mean completeness (0–1) | 0.615 |
| Median completeness | 0.615 |

**Authoritative product set = ReviewBible `src/bestiary_data_full.json` (707 entries).**  
Excel lists 708 unique name strings, but **25** are scrub re-apply corruptions (`Fracture-Kin` repeated four times) whose clean JSON counterparts already exist (`Fracture-Kin Alkilith`, etc.). Separately, **Ul’nath, the Hollow Dream** is intentionally filtered from product JSON (see `BESTIARY_INGEST.md`). **Do not count corrupt Excel strings as additional MM creatures.**

---

## Sources surveyed

| Source | Path | Role | Creature count |
|--------|------|------|---------------:|
| Canonical workbook | `ReviewBible/Bestiary.xlsx` (`Monsters`) | Authoring SoT for identity/loot/combat columns | 708 |
| Metadata supplement | `ReviewBible/bestiary_metadata_source.xlsx` | Backfill blanks on ingest only | (supplement; not a second creature list) |
| Live full JSON (**authoritative for this inventory**) | `ReviewBible/src/bestiary_data_full.json` | Companion / MM data plane | **707** |
| Legacy subset JSON | `ReviewBible/src/bestiary_data.json` | Predates full ingest; **not** UI SoT | 50 |
| Root subset | `bestiary_data.json` / `ReviewBible/bestiary_data.json` | Same legacy class | ~50 |
| Director lore volume | `ReviewBible/docs/manuals/Decennium_Descent_Bestiary_of_Aethel.md` | Generated lexicon + ecology | All **707** live names appear; `###` count (~797) also includes Challenge-band headers + a few alias titles — not extra creatures |
| Publication posture | `ReviewBible/docs/development/BESTIARY_PUBLICATION_STATUS.md` | Scaffold vs commercial clearance | — |
| Ingest / combat schema | `docs/mechanics/BESTIARY_INGEST.md`, `MONSTER_COMBAT_SCHEMA.md` | Field contracts | — |
| IP scrub log | `docs/mechanics/BESTIARY_SCRUB_LOG.md` + `scripts/scrub_bestiary_ip.py` | FR/iconic renames (54 family) | — |
| Floor Encounters | `ReviewBible/src/data/floor-encounters.json` | Encounter budgets / toolkit (not a second bestiary) | name-like strings scanned: 95; exact bestiary matches: 5 |
| Main working tree JSON | `src/bestiary_data_full.json` | Drift check | status: **corrupt_json (JSONDecodeError)**; unique names≈191; symdiff vs ReviewBible≈648 |
| Main `Bestiary.xlsx` | `Bestiary.xlsx` | Mirror of workbook | 708 named rows (matches ReviewBible count) |

**ReviewBible wins:** use ReviewBible JSON/xlsx when main JSON is corrupt or diverges.

Machine index: [`creature-index.json`](./creature-index.json) (dual-written under `DescentReviewChanges/docs/bestiary/monster-manual/`).

---

## Completeness histogram (MM readiness 0–1)

| Band | Count | Notes |
|------|------:|-------|
| 0.0–0.29 | 0 | Shell / combat poke only |
| 0.3–0.49 | 0 | Typical excel-ingest + template ecology |
| 0.5–0.69 | 697 | Better combat provenance or tags |
| 0.7–0.84 | 0 | Near MM-usable (usually ability scores + authored text) |
| 0.85–1.0 | 10 | Closest to full commercial MM entry |

**Histogram counts:** `{'0.5–0.69': 697, '0.85–1.0': 10}`

Scoring weights emphasize: ability scores, attack block quality, authored ecology (penalizes template one-liners), AC/HP/speed, CR/XP, skills/senses/languages, traits. Legendary/lair are optional bonuses.

### Highest completeness (sample)

| Name | Score | Combat source |
|------|------:|---------------|
| Ashthirst the Hollow | 0.94 | gate-guardian-trusted |
| Choralith, Voice Below | 0.94 | gate-guardian-trusted |
| Eirfax, the Dusk Crowned | 0.94 | gate-guardian-trusted |
| Gor Vekk, Architect of Ends | 0.94 | gate-guardian-trusted |
| Lumen of the Shattered Thread | 0.94 | gate-guardian-trusted |
| The Bloom That Hungers | 0.94 | gate-guardian-trusted |
| The Marquis of Silence | 0.94 | gate-guardian-trusted |
| Threxus, the Iron Spiral | 0.94 | gate-guardian-trusted |
| Vaskor, the Stone Maw | 0.94 | gate-guardian-trusted |
| Xarog, the Pactbound Furnace | 0.94 | gate-guardian-trusted |
| Adult Black Dragon | 0.635 | t6-10-trusted |
| Adult Blue Dragon | 0.635 | band-trusted |
| Adult Brass Dragon | 0.635 | band-trusted |
| Adult Bronze Dragon | 0.635 | band-trusted |
| Adult Copper Dragon | 0.635 | band-trusted |

### Lowest completeness (sample)

| Name | Score | Flags (abbrev) |
|------|------:|----------------|
| Lizardfolk Shaman | 0.566 | template_description, draft_combat, missing_ability_scores |
| Swarm of Poisonous Snakes | 0.566 | template_description, draft_combat, missing_ability_scores |
| Unicorn | 0.566 | template_description, draft_combat, missing_ability_scores |
| Vulture | 0.566 | template_description, draft_combat, missing_ability_scores |
| Wretched Grief-Bound | 0.566 | template_description, draft_combat, missing_ability_scores |
| Cow | 0.579 | template_description, draft_combat, missing_ability_scores |
| Hush-Broker Manyclaw | 0.579 | template_description, draft_combat, missing_ability_scores |
| Pixie | 0.579 | template_description, draft_combat, missing_ability_scores |
| Swarm of Ravens | 0.579 | template_description, draft_combat, missing_ability_scores |
| Xvart Warlock of the Nine-Legged Choir | 0.579 | template_description, draft_combat, missing_ability_scores |
| Abjurer | 0.597 | template_description, missing_ability_scores, missing_traits |
| Animated Armor | 0.597 | template_description, missing_ability_scores, missing_traits |
| Annis Hag | 0.597 | template_description, missing_ability_scores, missing_traits |
| Astral Ascetic Anarch | 0.597 | template_description, missing_ability_scores, missing_traits |
| Astral Reaver War-Captain | 0.597 | template_description, missing_ability_scores, missing_traits |

---

## Breakdown by type

| Type | Count |
|------|------:|
| Humanoid | 88 |
| Fiend | 75 |
| Dragon | 73 |
| Beast | 71 |
| Undead | 61 |
| Monstrosity | 59 |
| Giant | 57 |
| Elemental | 51 |
| Aberration | 42 |
| Construct | 42 |
| Fey | 33 |
| Plant | 23 |
| Ooze | 22 |
| Celestial | 10 |

## Breakdown by size

| Size | Count |
|------|------:|
| Large | 197 |
| Huge | 146 |
| Medium | 124 |
| Gargantuan | 90 |
| Small | 84 |
| Tiny | 66 |

## Breakdown by CR band

| CR band | Count |
|--------|------:|
| 5-10 | 232 |
| 0-<1 | 147 |
| 1-4 | 120 |
| 11-16 | 99 |
| 21+ | 75 |
| 17-20 | 34 |

## Breakdown by approximate tier / floor band (from CR)

> DD does not store an explicit `tier` field on every monster; bands below are **CR-derived proxies** aligned to companion combat-trust bands (T1–T5 / T6–10 docs).

| Tier / floor proxy | Count |
|--------------------|------:|
| T1 (approx floors 1-10 / CR≤4) | 267 |
| T2 (approx floors 11-20 / CR≤8) | 161 |
| T3 (approx floors 21-30 / CR≤12) | 132 |
| T6 (approx floors 71-90 / CR≤26) | 51 |
| T4 (approx floors 31-50 / CR≤16) | 38 |
| T5 (approx floors 51-70 / CR≤20) | 34 |
| T7+ / apex (CR≥27) | 24 |

## Zone Found (top 25)

| Zone | Count |
|------|------:|
| Aethel Caves | 62 |
| Aethel Forests | 54 |
| Null Zones | 49 |
| Spiral Nexus | 45 |
| Veiled Iron Spiral | 43 |
| Isles of Eternal Radiance | 43 |
| Bastion of Flame | 42 |
| Aethel Highlands | 42 |
| Aethel Swamps | 35 |
| Duskshard Pools | 30 |
| Aethel Lowlands | 29 |
| Silencebound Void | 27 |
| Aethel Mountains | 25 |
| Yieldheart Caverns | 25 |
| Sanctum of Echoing Choirs | 21 |
| Aethel Lakes | 20 |
| Aethel Tundra | 19 |
| Resonance Fields | 18 |
| Aethel Rivers | 17 |
| Aethel Deserts | 12 |
| Aethel Jungles | 11 |
| The Dungeon | 10 |
| Aethel Oceans | 9 |
| Crossroads of the Shattered Thread | 6 |
| Yieldheart | 3 |

## Combat provenance

| `combat.source` | Count |
|-----------------|------:|
| band-trusted | 430 |
| t1-5-trusted | 154 |
| t6-10-trusted | 102 |
| Bestiary.xlsx:Monsters | 11 |
| gate-guardian-trusted | 10 |

---

## Fields present vs missing (full MM entry checklist)

Target = Pathfinder/DnD-comparable Monster Manual entry. Live JSON is strong on **identity + combat shell + zone + loot tier drops**, weak on **ability scores, skills, senses, languages, traits, legendary/lair, art, stable ids**.

| Field | Group | Present | Missing | MM note |
|-------|-------|--------:|--------:|---------|
| `name` | identity | 707 | 0 | OK |
| `id` | identity | 0 | 707 | GAP for commercial MM |
| `size` | identity | 707 | 0 | OK |
| `type` | identity | 707 | 0 | OK |
| `tags` | identity | 113 | 594 | GAP for commercial MM |
| `alignment` | identity | 707 | 0 | OK |
| `challengeRating` | challenge | 707 | 0 | OK |
| `xp` | challenge | 707 | 0 | OK |
| `armorClass` | defense | 707 | 0 | OK |
| `hitPoints` | defense | 707 | 0 | OK |
| `speed` | defense | 707 | 0 | OK |
| `abilities` | ability_scores | 10 | 697 | GAP for commercial MM |
| `skills` | skills | 10 | 697 | GAP for commercial MM |
| `senses` | senses | 10 | 697 | GAP for commercial MM |
| `languages` | languages | 10 | 697 | GAP for commercial MM |
| `combat.defenses` | defenses | 707 | 0 | OK |
| `combat.attacks` | actions | 707 | 0 | OK |
| `traits` | traits | 0 | 707 | GAP for commercial MM |
| `legendaryActions` | legendary | 0 | 707 | GAP for commercial MM |
| `lairActions` | lair | 0 | 707 | GAP for commercial MM |
| `description` | ecology | 707 | 0 | OK |
| `zoneFound` | ecology | 707 | 0 | OK |
| `loot` | loot | 707 | 0 | OK |
| `lootTable` | loot | 10 | 697 | GAP for commercial MM |
| `image` | art | 0 | 707 | GAP for commercial MM |

### Typical existing vs missing (per creature)

**Almost always present (707/707 unless noted):** `name`, `size`, `type`, `alignment`, `challengeRating`, `xp`, `zoneFound`, `description` (usually **template stub**), `loot.tier*`, `ingestSource`, `armorClass`, `hitPoints`, `speed`, `combat` (schema + ≥1 attack).

**Usually missing (~697/707):** `abilities` (STR–CHA), `skills`, `senses`, `languages` — present mainly on gate-guardian-grade authored rows (~10).

**Missing on all / nearly all:** stable `id`, `traits` (species features), `legendaryActions`, `lairActions`, `image`/art refs; structured `lootTable` only on **10** rows; `tags` on **113**.

**Ecology quality:** descriptions are near-universal but **template** (`A {size} {type} found in {zone}.`) for the bulk — not MM lore.

---

## Stubs, placeholders, duplicates

| Issue | Count | Notes |
|-------|------:|-------|
| Duplicate names | 0 | Live JSON clean |
| Template / stub descriptions | 697 | Heuristic: short or `A <size> <type> found in <zone>.` |
| `draft: true` combat | 11 | |
| Sandbox combat source | 0 | Post trust-pass, mostly cleared |
| Missing ability scores | 697 | Blocks full MM stat block |
| Gate Guardians | 10 | Highest authorship tier |
| Publication posture | — | Per `BESTIARY_PUBLICATION_STATUS.md`: large share remains compatibility/prototype — **not** cleared commercial copy |

**Intentionally hidden Excel row(s):** `Ul’nath, the Hollow Dream`

**Excel scrub corruption (same creatures as clean JSON `Fracture-Kin *`; do not invent duplicates):** 25 rows — e.g. `Fracture-Kin Fracture-Kin Fracture-Kin Fracture-Kin Alkilith` ↔ JSON `Fracture-Kin Alkilith`. Clean JSON Fracture-Kin counterparts in name-diff: 25.

**Markdown lexicon vs JSON:** all 707 live JSON names appear under `###` headings; raw `###` count (~797) also includes Challenge-band section headers and a few alias/legacy titles. Treat MD as a generated view of the same set, not a second inventable list.

**Floor Encounters:** not a creature SoT. Exact name overlaps with bestiary: **5**. Unmatched name-like strings (may be toolkit labels, not monsters): **90** (see index build logs / encounter file — do not promote to MM without bestiary row).

---

## IP / compatibility risk (heuristic — not legal advice)

Owner scrub (2026-07-29) renamed **54** FR/iconic labels (Drow/Lolth, Mind Flayer, Beholder kin, Gith, Duergar, Kuo-toa, Yuan-ti, Svirfneblin, Myconid). Scrub log explicitly left many **generic SRD / classic labels** for a later pass.

| Tag | Count | Meaning |
|-----|------:|---------|
| `scrubbed-aethel-rename` | 55 | Already renamed to Aethel-neutral families |
| `compatibility-classic-label` | 299 | Still uses common MM/SRD-style label (dragon chromatic lines, elementals, many beasts, NPC stat stubs, etc.) |
| `renamed-but-iconic-stem` | 24 | e.g. Fracture-Kin *Balor* — prefix remapped, stem still iconic |
| `possible-compatibility-label` | 30 | Name contains Dragon/Devil/Demon/Hag/Golem/Elemental/Giant without exact list hit |
| `high-ip-residual` | 1 | Scrub targets that may still appear |

### High-IP residual (if any)

- `Ulitharid`

### Examples — compatibility-classic-label (first 40)

- `Aboleth`
- `Abominable Yeti`
- `Abyssal Wretch`
- `Acolyte`
- `Adult Black Dragon`
- `Adult Blue Dracolich`
- `Adult Blue Dragon`
- `Adult Brass Dragon`
- `Adult Bronze Dragon`
- `Adult Copper Dragon`
- `Adult Faerie Dragon`
- `Adult Gold Dragon`
- `Adult Green Dragon`
- `Adult Red Dragon`
- `Adult Silver Dragon`
- `Adult White Dragon`
- `Air Elemental`
- `Allip`
- `Allosaurus`
- `Amnizu`
- `Ancient Black Dragon`
- `Ancient Blue Dragon`
- `Ancient Brass Dragon`
- `Ancient Bronze Dragon`
- `Ancient Copper Dragon`
- `Ancient Gold Dragon`
- `Ancient Green Dragon`
- `Ancient Red Dragon`
- `Ancient Silver Dragon`
- `Ancient White Dragon`
- `Androsphinx`
- `Animated Armor`
- `Ankheg`
- `Ankylosaurus`
- `Ape`
- `Apprentice Wizard`
- `Archdruid`
- `Archer`
- `Archmage`
- `Assassin`
… +259 more

### Examples — renamed-but-iconic-stem

- `Fracture-Kin Armanite`
- `Fracture-Kin Babau`
- `Fracture-Kin Balor`
- `Fracture-Kin Barlgura`
- `Fracture-Kin Bulezau`
- `Fracture-Kin Chasme`
- `Fracture-Kin Dretch`
- `Fracture-Kin Glabrezu`
- `Fracture-Kin Goristro`
- `Fracture-Kin Hezrou`
- `Fracture-Kin Manes`
- `Fracture-Kin Marilith`
- `Fracture-Kin Maurezhi`
- `Fracture-Kin Molydeus`
- `Fracture-Kin Nabassu`
- `Fracture-Kin Nalfeshnee`
- `Fracture-Kin Quasit`
- `Fracture-Kin Shadow Demon`
- `Fracture-Kin Shoosuva`
- `Fracture-Kin Sibriex`
- `Fracture-Kin Vargouille`
- `Fracture-Kin Vrock`
- `Fracture-Kin Wastrilith`
- `Fracture-Kin Yochlol`


### Scrubbed Aethel renames (sample)

- `Astral Ascetic Anarch`
- `Astral Ascetic Enlightened`
- `Astral Ascetic Monk`
- `Astral Ascetic Sentinel`
- `Astral Reaver Knight`
- `Astral Reaver Spellblade`
- `Astral Reaver Supreme Commander`
- `Astral Reaver War-Captain`
- `Astral Reaver Warrior`
- `Cave Gnome`
- `Deep Dwarf`
- `Deep Dwarf Despot`
- `Deep Dwarf Hammerer`
- `Deep Dwarf Kavalrachni`
- `Deep Dwarf Mind Master`
- `Deep Dwarf Screamer`
- `Deep Dwarf Soulblade`
- `Deep Dwarf Stone Guard`
- `Deep Dwarf Warlord`
- `Deep Dwarf Xarrorn`
- `Depth Toad`
- `Depth Toad Archpriest`
- `Depth Toad Taskmaster`
- `Gaze Tyrant`
- `Gaze Tyrant (in lair)`
- `Gaze Tyrant Husk`
- `Gaze Tyrant Sovereign`
- `Gaze Tyrant Sovereign (in lair)`
- `Serpent-Blood Abomination`
- `Serpent-Blood Anathema`
… +25 more

**Note for MM authors:** commercial Monster Manual should replace compatibility placeholders with independently authored Aethel creatures (per publication status), not merely rename stems.

---

## Gate Guardians (authored apex set)

| Name | CR | Completeness |
|------|-----:|-------------:|
| Ashthirst the Hollow | 14 | 0.94 |
| Choralith, Voice Below | 20 | 0.94 |
| Eirfax, the Dusk Crowned | 26 | 0.94 |
| Gor Vekk, Architect of Ends | 17 | 0.94 |
| Lumen of the Shattered Thread | 22 | 0.94 |
| The Bloom That Hungers | 11 | 0.94 |
| The Marquis of Silence | 30 | 0.94 |
| Threxus, the Iron Spiral | 28 | 0.94 |
| Vaskor, the Stone Maw | 8 | 0.94 |
| Xarog, the Pactbound Furnace | 24 | 0.94 |

---

## Implications for Monster Manual build (siblings)

1. **Count to plan against:** **707 unique** live creatures (+ 1 hidden Excel row if resurrected).
2. **Most entries are combat-shell + template ecology** — expect a full authorship pass for ability scores, traits, senses, languages, and real lore.
3. **~353** names carry some compatibility/IP attention flag under heuristics — prioritize original DD replacements for commercial print.
4. **Do not pull new creatures from Floor Encounters** unless they already exist in the bestiary JSON/Excel.
5. Prefer editing **`ReviewBible/Bestiary.xlsx`** then ingest; dual-write product outputs per activity-log rules.

---

## Files written

| File | Dual-write |
|------|------------|
| `docs/bestiary/monster-manual/BESTIARY_INVENTORY_FOR_MM.md` | `DescentReviewChanges/docs/bestiary/monster-manual/BESTIARY_INVENTORY_FOR_MM.md` |
| `docs/bestiary/monster-manual/creature-index.json` | `DescentReviewChanges/docs/bestiary/monster-manual/creature-index.json` |

Activity log: `docs/activity/2026-08-04.md` only (no dual-write).
